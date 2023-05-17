from django.shortcuts import render
from ticket.models import Routes, Substations, Schedule, ParentBus, Transaction
from django.shortcuts import redirect
from django.http import JsonResponse
from .algorithms import create_route, Dashboard, get_earning_data
from .forms import UserRegisterForm, UserRegisterForm2
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum

User = get_user_model()


def view_dashboard(request):
    if request.user.is_authenticated and request.user.is_admin:

        data = Dashboard(Transaction, User).get_dashboard_data()
        context = {

            'data': data
        }
        return render(request, 'administrator/dashboard.html', context)
    else:
        return redirect('/')


def add_route(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            create_route(request.POST)
            return JsonResponse({
                'url': request.META['HTTP_ORIGIN'] + f'/administrator/'
                                                     f'add-route-success/{request.POST["from"]}+{request.POST["to"]}/'
            })

        else:
            return render(request, 'administrator/add_routes_and_sub_station.html')

    else:
        return redirect('/')


def add_route_success(request, route):
    route = route.split('+')
    context = {
        'title': 'Success ',
        'msg1': 'Successfully added Route ',
        'msg2': f'{route[0]} -> {route[1]}.',

        'btn_name': 'Add Another Route'
    }
    return render(request, 'ticket/err_msg_template.html', context)


def add_staff(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':

            form = UserRegisterForm2(request.POST)

            if form.is_valid():
                form.save()
                user = User.objects.get(name=request.POST['name'], email=request.POST['email'],
                                        phone=request.POST['phone'])

                if request.POST['permission'] == 'staff':
                    user.is_staff = True
                    st = Substations.objects.get(pk=request.POST['station_name'])
                    user.station_name = st
                if request.POST['permission'] == 'admin':
                    user.is_staff = True
                    user.is_admin = True
                user.save()

                url = request.META['HTTP_ORIGIN'] + f'/administrator/add-staff-success/{user.name}/'
                return JsonResponse({
                    'register': True,
                    'url': url

                })
            else:
                email = False
                phone = False
                if 'email' in form.errors:
                    email = True
                if 'phone' in form.errors:
                    phone = True
                return JsonResponse({
                    'register': False,
                    'email': email,
                    'phone': phone,
                })

        else:
            form = UserRegisterForm()
            return render(request, 'administrator/register_staff.html', {'form': form})

    else:
        return redirect('/')


def add_staff_success(request, user):

    context = {
        'title': 'Success ',
        'msg1': 'Successfully created Staff account for  ',
        'msg2': f'{user}.',

        'btn_name': 'Add Another '
    }
    return render(request, 'ticket/err_msg_template.html', context)


def search_user_staff(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        users = User.objects.filter(
            Q(name__startswith=keyword) | Q(phone__startswith=keyword) | Q(email__startswith=keyword)
        )
        return render(request, 'administrator/search_template_user_staff.html', {'users': users})


def search_recent_bookings(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        data = Transaction.objects.filter(
            Q(user_name__startswith=keyword) | Q(user_phone__startswith=keyword) | Q(user_email__startswith=keyword) |
            Q(bus_no__startswith=keyword) | Q(tran_id__startswith=keyword) | Q(route__startswith=keyword)
        )
        return render(request, 'administrator/recent_bookings_template.html', {'data': data})


def view_user_profile(request, pk):
    if request.user.is_authenticated and request.user.is_admin:
        user = User.objects.get(pk=pk)
        trans_data = Transaction.objects.filter(user=user)
        count = trans_data.count()
        amount = trans_data.aggregate(Sum('amount'))['amount__sum']
        if amount is None:
            amount = 0

        context = {
            'trans_data': trans_data,
            'user': user,
            'count': count,
            'amount': amount
        }
        return render(request, 'administrator/view_profile.html', context)
    return redirect('/')


def view_all_earning_information(request):
    if request.method == 'POST':
        pass
    context = {'data': get_earning_data()}
    return render(request, 'administrator/show_earning_data.html', context)


def filter_earning_data(request):
    if request.method == 'POST':
        context = {
            'data': get_earning_data(request.POST['filter_by'])
        }
        return render(request, 'administrator/earning_data_filter_template.html', context)