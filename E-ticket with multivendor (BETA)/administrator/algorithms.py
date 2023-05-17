from datetime import datetime, timedelta

from django.db.models import Sum
from ticket.models import ParentBus, Routes, Substations, Schedule, Transaction, User


class Dashboard:
    def __init__(self, transaction , user):
        self.transaction = transaction
        self.user = user

    def get_dashboard_data(self):
        """I will implement it tomorrow if i live .
            We are going to make everything object oriented based """
        pass


def get_dashboard_data(data):
    total_passenger = get_total_passenger(Transaction)
    total_income, total_refund = get_month_total_income_and_refund(Transaction)
    reg_user = get_registered_user(User)
    total_earning_this_year, diff_prev_year = get_total_earning_and_diff_amount(Transaction)
    recent_bookings = get_recent_bookings(Transaction)
    staffs, normal_users = get_staffs_and_normal_users(User)
    current_year = datetime.today().year
    context = {
        'total_passenger': total_passenger,
        'total_income': total_income,
        'total_refund': total_refund,
        'reg_user': reg_user,
        'total_earning_this_year': total_earning_this_year,
        'diff_prev_year': diff_prev_year,
        'recent_bookings': recent_bookings,
        'staffs': staffs,
        'normal_users': normal_users,
        'current_year': current_year
    }
    return context


def get_total_passenger(data):
    return data.objects.filter(refund=False).count()


def get_month_total_income_and_refund(data):
    income = data.objects.filter(refund=False).aggregate(Sum('amount'))
    refund = data.objects.filter(refund=True).aggregate(Sum('amount'))

    return income['amount__sum'], refund['amount__sum']


def get_registered_user(data):
    return data.objects.filter(is_staff=False).count()


def get_total_earning_and_diff_amount(data):
    amount = data.objects.filter(refund=False, date_time__year__gte=datetime.today().year,
                                 date_time__year__lte=datetime.today().year).aggregate(Sum('amount'))
    prev_year = data.objects.filter(refund=False, date_time__year__gte=datetime.today().year-1,
                                    date_time__year__lte=datetime.today().year-1).aggregate(Sum('amount'))
    diff = amount['amount__sum'] - prev_year['amount__sum']
    return amount, diff


def get_recent_bookings(data):
    return data.objects.filter(refund=False, date_time__date__gte=datetime.today() - timedelta(days=10))


def get_staffs_and_normal_users(data):
    normal_users = data.objects.filter(is_staff=False)
    staffs = data.objects.filter(is_staff=True)
    return staffs, normal_users


def create_route(data):
    parent = ParentBus.objects.get(id=1)
    route = Routes(parent=parent, from_location=data['from'], to_location=data['to'],
                   price_b_non_ac=int(data['cost_b_non_ac']), price_b_ac=int(data['cost_b_ac']),
                   price_e_non_ac=int(data['cost_e_non_ac']), price_e_ac=int(data['cost_e_ac']))
    route.save()
    main_station = Substations(station_name=data['main_station'], distance_time_from_main_station=0,
                               contact=data['main_station_c_number'], route=route)
    main_station.save()
    sub_stations = data.getlist('sub_station')
    distance_times = data.getlist('distance_time')
    sub_station_contacts = data.getlist('sub_station_contact')

    for i in range(len(sub_stations)):
        station = Substations(station_name=sub_stations[i], distance_time_from_main_station=int(distance_times[i]),
                              contact=sub_station_contacts[i], route=route)
        station.save()

    schedule_bus_type = data.getlist('bus_type')
    schedule_bus_no = data.getlist('bus_no')
    schedule_departure_time = data.getlist('departure_time')
    seat_capacity = data.getlist('seat_capacity')

    for i in range(len(schedule_bus_type)):
        time = datetime.strptime(schedule_departure_time[i], "%H:%M")
        s_time = time.strftime("%I:%M %p")
        schedule = Schedule(bus_type=schedule_bus_type[i], bus_no=schedule_bus_no[i],
                            bus_capacity=seat_capacity[i], departure_time=s_time, route=route)
        schedule.save()

