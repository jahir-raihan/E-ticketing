# Algorithms for finding out routes
import random
from datetime import datetime, timedelta

from django.shortcuts import redirect
from sslcommerz_lib import SSLCOMMERZ
from twilio.rest import Client
import shortuuid
from django.conf import settings
from .models import Routes, Date, InfoQueue, Bus, Seats, FreezeList, CancelCode, Transaction
from counter.seat_info import seats_for_economy_non_ac


def find_routes():

    """Finding all routes to show on search for bus page."""

    routes = Routes.objects.all()
    from_location = []
    to_location = []
    for i in routes:
        from_location.append(i.from_location)
        to_location.append(i.to_location)

    return [sorted(set(from_location)), sorted(set(to_location))]


def route_validity(data):

    """This function checks if the service is available on this
        route or not."""

    try:
        route = Routes.objects.get(from_location=data['from'], to_location=data['to'])
        return route
    except:
        return False


def check_date_validity(data):

    """This algorithm checks if searched bus for a
        date is valid or not."""

    time = datetime.date(datetime.strptime(data['date'], "%Y-%m-%d")) >= datetime.date(datetime.now())
    if time:
        return True
    return False


def get_or_create_date_data(route, data):

    """This function creates or returns a existing data of bus
        based on route and date given.
        To make this function work , we need to make sure that
        Our defined route should have a departure schedule."""

    try:
        print('came here')
        bus_data = Date.objects.get(date=data['date'], route=route).bus_set.filter(is_departure=False)

        return bus_data

    except:
        bus_data = Date(date=data['date'], route=route)
        bus_data.save()
        schedules = route.schedule_set.all()
        for s in schedules:
            seat_price = (route.price_b_non_ac if s.bus_type == 'Business Non AC'
                          else route.price_b_ac if s.bus_type == 'Business AC' else route.price_e_non_ac if
                          s.bus_type == 'Economy Non AC' else route.price_e_ac)
            bus_set = bus_data.bus_set
            bus_data_for_seat = bus_set.create(
                bus_type=s.bus_type,
                bus_id=s.bus_no,
                bus_capacity=s.bus_capacity,
                departure_time=s.departure_time,
                departure_date=data['date'],
                leaving_station=route.from_location,

            )
            bus_data_for_seat.save()

            seat_data = bus_data_for_seat.seats_set
            for i in range(bus_data_for_seat.bus_capacity):
                seat_data.create(
                    seat_name=seats_for_economy_non_ac[i],

                )

        return bus_data.bus_set.all()


def format_seats_data(data, cap):

    """This function returns a bus seats into 10 parts with 4 element each,
        in form of a list to separate them in html file inside table tag with tr. """

    """Based on different bus capacity , will change and modify this algorithm in future if required."""

    seat_lst = [[], [], [], [], [], [], [], [], [], [], []]
    i = 0
    j = 0

    for d in sorted(data, key=lambda x: x.seat_name):

        if j == 4:
            i += 1
            j = 1
            seat_lst[i].append(d)

        else:
            if j == 2:
                seat_lst[i].append('')

            seat_lst[i].append(d)
            j += 1

    return seat_lst


def get_boarding_points(route):

    """This function gets boarding points for a route"""

    sub_stations = []

    for station in route.substations_set.all():
        tmp = {
            'station_name': station.station_name,
            'distance_time': station.distance_time_from_main_station,
            'main_station': False
        }
        sub_stations.append(tmp)
    return sub_stations


def get_client_ip(request):

    """Takes request object as input
        and returns ip address of the request client"""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def verify_seats_availability(request, data):

    """This algorithm checks if the seats are available or not,
        This one works after submitting Passenger Information"""

    queue_data = InfoQueue.objects.get(pk=data['queue_id'])
    queue_data.passenger_name = data['name']
    queue_data.passenger_phone = data['number']
    queue_data.passenger_email = data['email']
    if request.user.is_authenticated:
        queue_data.user = request.user
    queue_data.save()

    bus = queue_data.bus
    seats = queue_data.seats.split(',')

    action = True
    unavailable_seats = []
    for seat in seats:
        seat_data = Seats.objects.filter(seat_name=seat, bus=bus)[0]

        if seat_data is None: return False

        if seat_data.is_sold or seat_data.freeze:
            freeze_time = (datetime.now() - datetime.strptime(seat_data.freeze_time, "%Y-%m-%d %H:%M:%S")).seconds // 60

            if freeze_time <= 3 and seat_data.freeze_user_ip == get_client_ip(request):
                continue
            elif freeze_time <= 3:

                action = False
                unavailable_seats.append(seat)
                continue
    if action:
        return [freeze_seats(request, seats, bus), unavailable_seats]

    return [action, unavailable_seats]


def freeze_seats(request, seats, bus):

    """If the current passenger is not in freeze list
        this algorithm freezes selected seats for 3 min ,
        """

    for seat in seats:
        seat_data = Seats.objects.filter(seat_name=seat, bus=bus)[0]
        seat_data.freeze_user_ip = get_client_ip(request)
        seat_data.freeze = True
        seat_data.freeze_time = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        seat_data.save()
        print('freezed seat 1: ', seat_data.seat_name)
    return True


def verify_seats_availability_without_freeze(request, data):

    """Same algorithm as above to verify seats availability , but this one do not freezes
        seats , because the passenger is already in freeze list.
        And the freezing time is < 30 minutes."""

    queue_data = InfoQueue.objects.get(pk=data['queue_id'])
    queue_data.passenger_name = data['name']
    queue_data.passenger_phone = data['number']
    queue_data.passenger_email = data['email']
    if request.user.is_authenticated:
        queue_data.user = request.user

    queue_data.save()
    bus = queue_data.bus
    seats = queue_data.seats.split(',')
    action = True
    unavailable_seats = []

    for seat in seats:
        seat_data = Seats.objects.filter(seat_name=seat, bus=bus)[0]

        if seat_data is None: return False

        if seat_data.is_sold or seat_data.freeze:
            freeze_time = (datetime.now() - datetime.strptime(seat_data.freeze_time, "%Y-%m-%d %H:%M:%S")).seconds // 60

            if freeze_time <= 3 and seat_data.freeze_user_ip == get_client_ip(request):
                continue
            elif freeze_time <= 3:

                action = False
                unavailable_seats.append(seat)
                continue

    if action:
        return [freeze_seats(request, seats, bus), unavailable_seats]

    return [action, unavailable_seats]


def in_freeze_list(request):

    """This algorithm checks if the passenger already in
        freeze list"""

    try:
        ip_address = get_client_ip(request)
        data = FreezeList.objects.get(user_ip=ip_address)
        freeze_time = (datetime.now() - datetime.strptime(data.time, "%Y-%m-%d %H:%M:%S")).seconds // 60
        if freeze_time >= 30:
            data.delete()
            return False
        return True
    except:
        return False


def add_to_freeze_list(request, data):

    """Adds a passenger to freeze list """

    ip = get_client_ip(request)

    fz_list = FreezeList(
        user_name=data['name'],
        user_ip=ip,
        time=f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    )
    fz_list.save()


def initiate_payment(request, data):

    """Payment Gateway"""

    tran_id = shortuuid.ShortUUID('1234567890WqQZzLlSsXx').random(15)
    purchase_data = InfoQueue.objects.get(pk=data['queue_id'])
    purchase_data.user_name = data['name']
    purchase_data.user_phone = data['number']
    purchase_data.user_email = data['email']
    purchase_data.save()
    setting = {'store_id': settings.STORE_ID, 'store_pass': settings.STORE_PASS, 'issandbox': True}
    sslcz = SSLCOMMERZ(setting)
    post_body = {'total_amount': purchase_data.amount, 'currency': "BDT", 'tran_id': f'{tran_id}',
                 'success_url': f"{request.META['HTTP_ORIGIN']}/purchase-success/view-ticket/{purchase_data.id}/",
                 'fail_url': f"{request.META['HTTP_ORIGIN']}", 'cancel_url': f"{request.META['HTTP_ORIGIN']}",
                 'emi_option': 0,
                 'cus_name': data['name'],
                 'cus_email': data['email'], 'cus_phone': data['number'], 'cus_add1': "Null",
                 'cus_city': "Null", 'cus_country': "Bangladesh", 'shipping_method': "NO", 'multi_card_name': "",
                 'num_of_item': 1, 'product_name': purchase_data.seats, 'product_category': "Bus Seats",
                 'product_profile': "general"}

    response = sslcz.createSession(post_body)  # API response

    return response['GatewayPageURL']


def occupie_seat(data):

    """After payment is success, this algorithm books selected seats
        for the passenger."""

    seats = data.seats.split(',')
    bus = data.bus
    for seat in seats:
        seat_data = Seats.objects.filter(seat_name=seat, bus=data.bus)[0]
        seat_data.is_sold = True
        seat_data.booking_time = datetime.now()
        seat_data.boarding_point = data.boarding_point
        seat_data.passenger_name = data.passenger_name
        seat_data.passenger_phone = data.passenger_phone
        seat_data.passenger_email = data.passenger_email

        if data.user:
            seat_data.passenger = data.user
        seat_data.save()
        bus.seats_available -= 1

        bus.save()


# Cancel ticket section

def data_is_valid(data):

    """To Cancel ticket , this algorithm checks if the credentials
        are valid or not"""

    number = data['number']
    trans_id = data['trans_id']
    try:
        tran_data = Transaction.objects.get(user_phone=number, tran_id=trans_id, refund=False)
        bus = tran_data.bus
        time = (datetime.strptime(f'{bus.departure_date} {bus.departure_time}', "%Y-%m-%d %H:%M:%S") - datetime.now()).seconds
        if bus.is_departure or 24/(time//60//60) < 2:

            return False
        return False
    except:
        return False


def send_code(data):

    """ If the credentials are valid this  algorithm
        sends a verification code to the passenger ticket
        registered number"""

    number = data['number']
    account_sid = settings.MSG_AUTH_ID
    auth_token = settings.MSG_AUTH_PASS
    client = Client(account_sid, auth_token)
    code = generate_code(data['trans_id'])

    message = client.messages \
        .create(
            body=f"Your verification code for cancelling ticket is: {code} , This code is valid for only 3 minutes.",
            from_=settings.MSG_NUMBER,
            to=f'+88{number}'
        )


def generate_code(trans_id):

    """Generates 5 digit codes to send as message"""

    code = random.randint(1, 99999)
    data = CancelCode(
        code=code,
        tran_id=trans_id,
        gen_time=f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    )
    data.save()
    return code


def validate_code(data):

    """Validates code , if the code is valid and code generate time and submit time <=3
        Refund process starts  and marks those seats as unbooked , returns True, else False"""

    code = data['code']
    tran_id = data['trans_id']
    try:
        cancel_data = CancelCode.objects.get(code=code, tran_id=tran_id)
        tran_obj = Transaction.objects.get(tran_id=tran_id)
        time = (datetime.now() - datetime.strptime(cancel_data.gen_time, "%Y-%m-%d %H:%M:%S")).seconds // 60
        if time <= 3:

            tran_obj.refund = True
            tran_obj.refund_time = datetime.now()
            tran_obj.save()
            bus = tran_obj.bus
            seats = tran_obj.seats.split(',')
            for seat in seats:
                seat_data = Seats.objects.filter(seat_name=seat, bus=bus)[0]
                seat_data.is_sold = False
                seat_data.booking_time = None
                seat_data.boarding_point = None
                seat_data.passenger_name = None
                seat_data.passenger_phone = None
                seat_data.passenger_email = None
                seat_data.freeze = False
                seat_data.freeze_time = None
                seat_data.freeze_user_ip = None
                if seat_data.passenger:
                    seat_data.passenger = None
                bus.seats_available += 1
                bus.save()
                seat_data.save()
            cancel_data.delete()
            refund(tran_obj)
            return True
        cancel_data.delete()
        return False

    except:
        return False


def refund(data):

    """Refund request"""

    setting = {'store_id': settings.STORE_ID, 'store_pass': settings.STORE_PASS, 'issandbox': True}
    sslcz = SSLCOMMERZ(setting)

    bank_tran_id = data.bank_transaction_id
    refund_amount = f'{data.amount}'
    refund_remarks = 'Cancel Ticket'
    response = sslcz.init_refund(bank_tran_id, refund_amount, refund_remarks)


# Trips

def get_trips_data(data):
    if data.user.is_authenticated:
        trip_data = Transaction.objects.filter(user=data.user)

    else:
        ip = get_client_ip(data)
        trip_data = Transaction.objects.filter(user_ip=ip)

    future_trips = []
    recent_trips = []
    history = []

    for t_data in trip_data:
        bus = t_data.bus
        time = (datetime.date(datetime.now()) - bus.departure_date).days

        if not t_data.bus.is_departure:
            future_trips.append(t_data)
        elif time <= 10:
            recent_trips.append(t_data)
        else:
            history.append(t_data)
    return future_trips, recent_trips, history



