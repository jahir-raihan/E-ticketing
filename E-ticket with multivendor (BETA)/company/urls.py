from django.urls import path
from . import views

urlpatterns = [
    path('verify-superuser-to-add-company/', views.verify_superuser, name='verify_superuser'),
    path('add-company/', views.register_company, name='register_company')

]