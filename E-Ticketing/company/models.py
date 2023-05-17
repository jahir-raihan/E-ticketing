from django.db import models
from django.contrib.auth import get_user_model

"""Doing it as a test purpose , if it works we will stick with it"""

User = get_user_model()


class Root(models.Model):
    app_name = models.CharField(max_length=20)


class Company(models.Model):
    root = models.ForeignKey(Root, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    licence_key = models.CharField(max_length=30)
    owner_name = models.CharField(max_length=30)
    owner_nid_number = models.CharField(max_length=17)
    ceo_name = models.CharField(max_length=30)
    ceo_nid_number = models.CharField(max_length=17)

    def __str__(self):
        return f'{self.company_name} owned by {self.owner_name} , ceo {self.ceo_name}'


class Routes(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=50, blank=False)
    to_location = models.CharField(max_length=50, blank=False)
    price_b_non_ac = models.IntegerField()
    price_b_ac = models.IntegerField()
    price_e_non_ac = models.IntegerField()
    price_e_ac = models.IntegerField()

    date_created = models.DateTimeField(auto_now_add=True)
    # number_of_bus = models.IntegerField()

    def __str__(self):
        return f'{self.company.company_name}, Route {self.from_location} - {self.to_location}.'


class Substations(models.Model):
    station_name = models.CharField(max_length=50)
    distance_time_from_main_station = models.IntegerField()
    contact = models.CharField(max_length=11)
    route = models.ForeignKey(Routes, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.station_name}, Sub Station of {self.route}'


class Schedule(models.Model):
    bus_type = models.CharField(max_length=50)
    bus_no = models.CharField(max_length=6)
    bus_capacity = models.IntegerField()
    departure_time = models.TimeField()
    route = models.ForeignKey(Routes, on_delete=models.CASCADE)

    def __str__(self):
        return f'scheduled bus of route { self.route}'
