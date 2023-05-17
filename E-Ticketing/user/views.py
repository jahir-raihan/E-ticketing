from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from ticket.algorithms import get_client_ip
from ticket.models import Transaction

User = get_user_model()

from .forms import UserRegisterForm
# Create your views here.


def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    """View for register"""

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            get_user = User.objects.get(email=request.POST['email'], phone=request.POST['phone'],
                                        name=request.POST['name'])
            get_user.ip = get_client_ip(request)
            get_user.save()
            user = authenticate(request, email=request.POST['email'], password=request.POST['password1'])
            login(request, user)
            return JsonResponse({
                'login': True
            })
        else:
            email = False
            phone = False
            if 'email' in form.errors:
                email = True
            if 'phone' in form.errors:
                phone = True

            return JsonResponse({
                'login': False,
                'email': email,
                'phone': phone,
            })

    form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    """Login view """
    if request.method == 'POST' and not request.user.is_authenticated:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])

        if user:
            login(request, user)
            return JsonResponse({
                'login': True
            })
        else:
            return JsonResponse({
                'login': False
            })
    return render(request, 'user/login.html')


@login_required
def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    """Logs out a user"""

    logout(request)
    return redirect('/')


def profile(request):
    if request.user.is_authenticated:
        trans_data = Transaction.objects.filter(user=request.user)
        count = trans_data.count()
        amount = trans_data.aggregate(Sum('amount'))['amount__sum']
        if amount is None:
            amount = 0

        context = {
            'trans_data': trans_data,
            'count': count,
            'amount': amount
        }
        return render(request, 'user/profile.html', context)
    else:
        ip = get_client_ip(request)
        trans_data = Transaction.objects.filter(user_ip=ip)
        count = trans_data.count()
        amount = trans_data.aggregate(Sum('amount'))['amount__sum']
        context = {
            'trans_data': trans_data,
            'count': count,
            'amount': amount
        }
        return render(request, 'user/profile.html', context)
