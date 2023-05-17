from django.urls import path
from . import views

urlpatterns = [
    path('add-route/', views.add_route, name='add_route'),
    path('add-route-success/<str:route>/', views.add_route_success, name='add_route_success'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('add-staff-success/<str:user>/', views.add_staff_success, name='add_staff_success'),

    path('dashboard/', views.view_dashboard, name='dashboard'),

]