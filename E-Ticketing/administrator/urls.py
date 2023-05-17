from django.urls import path
from . import views

urlpatterns = [
    path('add-route/', views.add_route, name='add_route'),
    path('add-route-success/<str:route>/', views.add_route_success, name='add_route_success'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('add-staff-success/<str:user>/', views.add_staff_success, name='add_staff_success'),
    path('search-user-staff/', views.search_user_staff, name='search_user_staff'),
    path('search-recent-bookings-data/', views.search_recent_bookings, name='search_recent_bookings'),

    path('dashboard/', views.view_dashboard, name='dashboard'),
    path('private-link/administrator/<str:pk>/view-user-profile/', views.view_user_profile, name='view_user_profile'),

    path('view-all-earning-information/', views.view_all_earning_information, name='view_all_ear_info'),
    path('filter-earning-data/', views.filter_earning_data, name='filter_earning_data'),

]