from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .algorithms import find_routes, route_validity, get_or_create_date_data, format_seats_data, get_boarding_points, \
    get_client_ip, verify_seats_availability, in_freeze_list, verify_seats_availability_without_freeze, \
    add_to_freeze_list, initiate_payment, occupie_seat, send_code, data_is_valid, validate_code, check_date_validity, \
    get_trips_data
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from .models import Routes, Date, Bus, InfoQueue, Transaction, Substations
# Create your views here.
import datetime


def home(request):

    """Home page"""

    if request.method == 'POST':

        route = route_validity(request.POST)
        date_validity = check_date_validity(request.POST)
        if route and date_validity:
            bus_data = get_or_create_date_data(route, request.POST).order_by('departure_time')
            date_for_render = datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d')
            context_for_template = {
                'buses': bus_data,

                'to': route.to_location,
                'from': route.from_location,
                'date': date_for_render,
            }

            template = render_to_string('ticket/bus_list_template.html', context_for_template, request)

            context = {
                'url': f"/bus-list/{request.POST['date']}/{route.from_location}+{route.to_location}/",
                'site_title': f'Bus List of | {date_for_render}',
                'template': template

            }

            return JsonResponse(context)

        else:
            context_for_error = {


                'title': 'Invalid Route OR Date',
                'msg1': 'Sorry for the inconvenience. ',
                'msg2': f"You've Entered a Invalid date or Invalid Route .",
                'btn_name': 'Search Again'
            }
            template = render_to_string('ticket/err_msg_template_short.html', context_for_error, request)

            return JsonResponse({
                'url': f"/unavailable-route/{request.POST['from']}+{request.POST['to']}/",
                'site_title': 'Invalid Route OR Date',
                'error': True,
                'template': template
            })

    min_date_picker = datetime.date.today()

    from_loc, to_loc = find_routes()
    context = {
        'from': from_loc,
        'to': to_loc,
        'date_range': min_date_picker
    }
    return render(request, 'ticket/search_for_bus.html', context)


def error_route(request, route):
    from_loc, to_loc = route.split('+')
    context = {
        'title': 'Invalid Route OR Date',
        'msg1': 'Sorry for the inconvenience',
        'msg2': f"You've Entered a Invalid date or Invalid Route .",
        'btn_name': 'Select Again'
    }
    return render(request, 'ticket/err_msg_template.html', context)


def get_bus_list(request, date, route):

    """This view will return bus list according to a date.
        If the bus data is already in database it will return
        existing data, else it will create new data. """

    from_loc, to_loc = route.split('+')

    route = route_validity(
        {'from': from_loc,
         'to': to_loc}
    )
    date_validity = check_date_validity({'date':date})
    if route and date_validity:
        bus_data = get_or_create_date_data(route, {'date': date}).order_by('departure_time')
        date_for_render = datetime.datetime.strptime(date, '%Y-%m-%d')
        context = {
            'buses': bus_data,
            'site_title': f'Bus List of | {date_for_render}',
            'to': to_loc,
            'from': from_loc,
            'date': date_for_render,
        }
        return render(request, 'ticket/bus_list.html', context)

    else:
        context = {
            'title': 'Invalid Route OR Date',
            'msg1': 'Sorry for the inconvenience',
            'msg2': f"You've Entered a Invalid date or Invalid Route .",
            'btn_name': 'Select Again'
        }

        return render(request, 'ticket/err_msg_template.html', context)


def get_bus_data(request):
    bus = Bus.objects.get(pk=request.POST['bus_id'])
    seats_data = format_seats_data(bus.seats_set.all(), bus.bus_capacity)
    boarding_points = get_boarding_points(bus.date.route)
    context = {
        'bus': bus,
        'seats_data': seats_data,
        'bus_id': bus.id,
        'bus_no': bus.bus_id,
        'boarding_points': boarding_points,
        'route': request.POST['route']
    }
    return render(request, 'ticket/bus_seat_template.html', context)


def refresh_bus_data(request):
    bus = Bus.objects.get(pk=request.POST['bus_id'])
    seats_data = format_seats_data(bus.seats_set.all())
    print("program came here")
    context = {
        'seats_data': seats_data,

    }
    return render(request, 'ticket/seat_template_for_refresh.html', context)


def buy_seats(request):
    # if request.user.is_authenticated:
    #     # do something
    #     pass
    # else

    seats = request.POST.getlist('seats[]')

    total = int(request.POST['total'])

    data = InfoQueue(
        ip_address=get_client_ip(request),
        bus=Bus.objects.get(pk=request.POST['bus_id']),
        bus_no=request.POST['bus_no'],
        seats=f'{",".join(seats)}',
        boarding_point=request.POST['boarding_point'],
        amount=total,
        route=request.POST['route']

    )
    data.save()
    return JsonResponse({'url': 'wgs-starlineservicesecurechannel@456-bt75/', 'queue_id': data.id})


def passenger_info(request, pk):

    queue_data = InfoQueue.objects.get(pk=pk)
    if get_client_ip(request) == queue_data.ip_address:

        seats = queue_data.seats.split(',')

        context = {
            'seats': seats,
            'queue_id': pk,

        }

        return render(request, 'ticket/add_passenger_info.html', context)


def proceed_to_payment(request):
    if request.method == 'POST':
        error = False
        if in_freeze_list(request):
            verify = verify_seats_availability_without_freeze(request, request.POST)
            if verify[0]:
                url = initiate_payment(request, request.POST)
                return JsonResponse({
                    'error': error,
                    'url': url
                })
                # Go to payment page
            else:
                error = True
                data = InfoQueue.objects.get(pk=request.POST['queue_id'])
                data.unavailable_seats = f'{",".join(verify[1])}'
                data.save()
                return JsonResponse({
                    'error': error,
                    'queue_id': request.POST['queue_id']
                })
        verify = verify_seats_availability(request, request.POST)
        if verify[0]:

            add_to_freeze_list(request, request.POST)
            url = initiate_payment(request, request.POST)
            return JsonResponse({
                'error': error,
                'url': url
            })

        else:
            error = True
            data = InfoQueue.objects.get(pk=request.POST['queue_id'])
            data.unavailable_seats = f'{",".join(verify[1])}'
            data.save()
            return JsonResponse({
                'error': error,
                'queue_id': request.POST['queue_id'],

            })


def error_page(request, pk):
    try:
        queue_data = InfoQueue.objects.get(pk=pk)
        context = {
            'title': 'Seats Unavailable',
            'msg1': f'Sorry for the inconvenience your selected seats "{queue_data.unavailable_seats}" are',
            'msg2': ' already SOLD, or has been selected by another Passenger first.',
            'btn_name': 'Select a Different Seat'
        }

        return render(request, 'ticket/err_msg_template.html', context)
    except:
        return '404 page'


@csrf_exempt
def purchase_success(request, pk):
    data = InfoQueue.objects.get(pk=pk)
    data.purchased = True
    print(data.route)
    route = data.route.split(' ')
    print('route', route)
    tran = Transaction(
        user_ip=get_client_ip(request),
        user_name=data.passenger_name,
        user_phone=data.passenger_phone,
        user_email=data.passenger_email,
        boarding_point=data.boarding_point,
        amount=data.amount,
        bus=data.bus,
        bus_no=data.bus_no,
        seats=data.seats,
        tran_id=request.POST['tran_id'],
        validation_id=request.POST['val_id'],
        bank_transaction_id=request.POST['bank_tran_id'],
        route=f'{route[0]} -> {route[1]}',

    )
    tran.save()
    if data.user:
        tran.user = data.user
        tran.save()
    occupie_seat(data)
    return redirect(f'/view-ticket/{tran.tran_id}/{tran.id}/')


def view_ticket(request, t_id,  pk):
   
    try:
        data = Transaction.objects.get(tran_id=t_id, pk=pk, refund=False)
        if not data.bus.is_departure:
            delay_time = Substations.objects.get(station_name=data.boarding_point).distance_time_from_main_station
            url = 'http://' + request.META['HTTP_HOST'] + f'/{t_id}/{pk}/'
            from_loc, to_loc = data.route.split('->')

            seats = data.seats.split(',')
            context = {
                'url': url,
                'data': data,
                'from': from_loc,
                'to': to_loc,
                'delay': delay_time,
                'seats': seats
            }
            return render(request, 'ticket/ticket.html', context)
    except:

        context = {

            'title': 'Invalid Ticket',
            'msg1': 'Sorry for the inconvenience, ',
            'msg2': f"Your Ticket  {t_id} is Invalid or Does not exists. Permission Denied.",
            'btn_name': 'Back'
        }
        return render(request, 'ticket/err_msg_template.html', context)


# SPA Navigation system views

# Cancel Ticket Section


def cancel_tickets(request):
    if request.method == 'POST':

        template = render_to_string('spa_nav_templates/cancel_ticket_template.html', request=request)
        url = request.META['HTTP_ORIGIN'] + reverse('cancel_ticket')
        return JsonResponse({
            'template': template,
            'url': url,
            'title': 'Cancel Ticket',

        })

    return render(request, 'ticket/cancel_ticket.html', {})


def cancel_ticket_send_code(request):
    if request.method == 'POST':
        if data_is_valid(request.POST):

            send_code(request.POST)
            context = {
                'trans_id': request.POST['trans_id'],
                'number': request.POST['number'],
                'hash_num': f'{request.POST["number"][:3]}****{request.POST["number"][8:]}'

            }
            template = render_to_string('ticket/cancel_ticket_code_template.html', context, request)

            return JsonResponse({
                'title': 'Submit Code',
                'template': template,
                'error': False,

            })

        return JsonResponse({
            'url': f"/invalid-id/{request.POST['trans_id']}/",
            'error': True,
        })


def error_cancel_ticket(request, trans_id):
    context = {

        'title': 'Invalid ID',
        'msg1': 'Sorry for the inconvenience, ',
        'msg2': f"Your Ticket ID {trans_id} is Invalid or Does not exists."
                f" More possible reasons can be: The bus will Departure in range of 2 days.",
        'btn_name': 'Back'
    }
    return render(request, 'ticket/err_msg_template.html', context)


def validate_code_view(request):
    if request.method == 'POST':
        title = 'Refund Failed!'
        context = {
            'msg1': f'You\'re request for Cancel Ticket is >Failed<',
            'msg2': f"Reason : Verification Failed.",
            'btn_name': 'Back'
        }
        if validate_code(request.POST):
            title = 'Cancel Ticket Success'
            context = {
                'msg1': f"You're request for Cancel Ticket is Successful.",
                'msg2': f"Your Ticket ID was {request.POST['trans_id']}. Thank You for Sticking with US.",
                'btn_name': 'Back To Home'
            }
        template = render_to_string('ticket/err_msg_template_short.html', context, request)

        return JsonResponse({

            'title': title,
            'template': template


        })
#  Home page


def main_home(request):
    if request.method == 'POST':
        min_date_picker = datetime.date.today()

        from_loc, to_loc = find_routes()
        context = {
            'from': from_loc,
            'to': to_loc,
            'date_range': min_date_picker
        }

        template = render_to_string('spa_nav_templates/home_template.html', context, request=request)
        url = request.META['HTTP_ORIGIN'] + reverse('main_home')
        return JsonResponse({
            'template': template,
            'url': url,
            'title': 'Search for Bus',

        })

    return redirect('/')

# Trips page


def trips(request):
    future_trips, recent_trips, history = get_trips_data(request)
    context = {
        'future_trips': future_trips,
        'recent_trips': recent_trips,
        'history': history
    }
    if request.method == 'POST':
        template = render_to_string('spa_nav_templates/trips_template.html', context, request=request)
        url = request.META['HTTP_ORIGIN'] + reverse('trips')
        return JsonResponse({
            'template': template,
            'url': url,
            'title': 'Trips',

        })

    return render(request, 'ticket/trips.html', context)

# Counter page


def counter_info(request):
    if request.method == 'POST':
        route_data = Routes.objects.all()
        template = render_to_string('spa_nav_templates/counter_info_template.html',{'routes': route_data},
                                    request=request)
        url = request.META['HTTP_ORIGIN'] + reverse('counter_info')
        return JsonResponse({
            'template': template,
            'url': url,
            'title': 'Counter Information',

        })
    route_data = Routes.objects.all()
    return render(request, 'ticket/counter_infos.html', {'routes': route_data})
