from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('bus-list/<str:date>/<str:route>/', views.get_bus_list, name='get_bus_list'),
    path('bus-list/show-bus-data/', views.get_bus_data, name='get_bus_data'),
    path('buy-seats/', views.buy_seats, name='buy_seats'),
    path(f'passenger-info/wgs-starlineservicesecurechannel@456-bt75/<str:pk>/', views.passenger_info,
         name='passenger_info'),
    path('buy-seats/passenger-contact-info/', views.proceed_to_payment, name='proceed_to_payment'),
    path('unavailable/<str:pk>/', views.error_page, name='error_page'),
    path('unavailable-route/<str:route>/', views.error_route, name='error_route_page'),
    path('get-bus-seat-by-refresh/', views.refresh_bus_data, name='refresh_bus_data'),
    # purchase success url
    path('purchase-success/view-ticket/<str:pk>/', views.purchase_success, name='purchase_success'),
    # show ticket
    path('view-ticket/<str:t_id>/<str:pk>/', views.view_ticket, name='view_ticket'),


    # cancel ticket url
    path('cancel-tickets/', views.cancel_tickets, name='cancel_ticket'),
    path('cancel-tickets/send-code/', views.cancel_ticket_send_code, name='send_code'),
    #   path('validate-code/', views.validate_code, name='validate_code'),
    path('invalid-id/<str:trans_id>/', views.error_cancel_ticket, name='error_cancel_ticket'),
    path('cancel-tickets/submit-code/', views.validate_code_view, name='submit_code'),


    path('counter-info/', views.counter_info, name='counter_info'),
    path('nav-home/', views.main_home, name='main_home'),
    path('trips/', views.trips, name='trips'),

    # path('options-settings/', views., name='cancel_ticket'),


]