from company.models import *


class Date(models.Model):
    date = models.DateField()
    route = models.ForeignKey(Routes, on_delete=models.CASCADE)

    def __str__(self):
        return f'Buses of route { self.route}, on {self.date}'


class CompanyRouteDate(models.Model):
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    route = models.ForeignKey(Routes, on_delete=models.CASCADE)


class Bus(models.Model):
    bus_type = models.CharField(max_length=30)
    bus_specification = models.CharField(max_length=30)
    bus_id = models.IntegerField()
    bus_capacity = models.IntegerField()
    departure_time = models.TimeField()
    departure_date = models.DateField()
    is_departure = models.BooleanField(default=False)
    seats_available = models.IntegerField(default=22)
    seat_price = models.IntegerField(default=700)

    leaving_station = models.CharField(max_length=100)
    crd = models.ForeignKey(CompanyRouteDate, on_delete=models.CASCADE)

    def __str__(self):
        return f'Bus of date {self.departure_time}, leaving from {self.leaving_station}'


class Seats(models.Model):
    seat_name = models.CharField(max_length=5, blank=False)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)

    # below field will be used if the seat is sold
    booking_time = models.DateTimeField(blank=True, null=True)
    boarding_point = models.CharField(max_length=100, blank=True, null=True)
    passenger_name = models.CharField(max_length=50, blank=True, null=True)
    passenger_phone = models.CharField(max_length=11, blank=True, null=True)
    passenger_email = models.EmailField(max_length=30, blank=True, null=True)
    freeze = models.BooleanField(default=False)
    freeze_time = models.CharField(max_length=30, null=True, blank=True)
    freeze_user_ip = models.GenericIPAddressField(null=True, blank=True)
    #   rest are optional
    passenger = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f'Seat Name: {self.seat_name} of Bus Id {self.bus.id}'


class InfoQueue(models.Model):
    route = models.CharField(default='', max_length=50)
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    bus_no = models.IntegerField()
    seats = models.CharField(max_length=100)
    amount = models.IntegerField()
    passenger_name = models.CharField(max_length=20, blank=True, null=True)
    passenger_phone = models.CharField(max_length=11, blank=True, null=True)
    passenger_email = models.EmailField(blank=True, null=True)
    boarding_point = models.CharField(max_length=50)
    purchased = models.BooleanField(default=False)
    unavailable_seats = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)


class FreezeList(models.Model):
    user_name = models.CharField(max_length=20)
    user_ip = models.GenericIPAddressField()

    time = models.CharField(max_length=30)


class Transaction(models.Model):
    amount = models.IntegerField()
    seats = models.CharField(max_length=30)
    bus_no = models.IntegerField()
    bus = models.ForeignKey(Bus, on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField(auto_now_add=True)
    tran_id = models.CharField(max_length=20)
    validation_id = models.CharField(max_length=30)
    bank_transaction_id = models.CharField(max_length=50, default='')
    route = models.CharField(max_length=50)
    user_name = models.CharField(max_length=20)
    user_phone = models.CharField(max_length=11)
    user_email = models.EmailField()
    boarding_point = models.CharField(max_length=50)
    user_ip = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    refund = models.BooleanField(default=False, null=True, blank=True)
    refund_time = models.DateTimeField(blank=True, null=True)


class CancelCode(models.Model):
    code = models.CharField(max_length=6)
    tran_id = models.CharField(max_length=20)
    gen_time = models.CharField(max_length=20)
