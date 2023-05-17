from datetime import datetime, timedelta

from django.db.models import Sum
from ticket.models import ParentBus, Routes, Substations, Schedule, Transaction, User, Bus


class Dashboard:
    def __init__(self, transaction, user):
        self.transaction = transaction
        self.user = user

    def get_dashboard_data(self):

        """Aggregate and get data to show in dashboard.
            This interface will be dynamic in case if we build multiple vendor
            System"""

        total_passenger = self.__get_total_passenger()
        total_income, total_refund = self.__get_month_total_income_and_refund()
        reg_user = self.__get_registered_user()
        total_earning_this_year, diff_prev_year = self.__get_total_earning_and_diff_amount()
        recent_bookings = self.__get_recent_bookings()
        staffs, normal_users = self.__get_staffs_and_normal_users()
        current_year = datetime.today().year
        chart_data = self.__get_data_for_chart()

        # satisfaction = self.determine_satisfaction(Review)

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
            'current_year': current_year,
            'chart_data': chart_data

            # 'satisfaction': satisfaction
        }
        return context

    def __get_total_passenger(self):

        """Getting total passenger that have used our services ,
            This method will behave differently in case of multiple vendor
            system."""

        return self.transaction.objects.filter(refund=False).count()

    def __get_month_total_income_and_refund(self):

        """Returns total income and refund"""

        income = self.transaction.objects.filter(refund=False).aggregate(Sum('amount'))['amount__sum']
        refund = self.transaction.objects.filter(refund=True).aggregate(Sum('amount'))['amount__sum']
        if income is None:
            income = 0
        if refund is None:
            refund = 0

        return income, refund

    def __get_registered_user(self):

        """Returns all registered users , excluding staff and admins."""

        return self.user.objects.filter(is_staff=False).count()

    def __get_total_earning_and_diff_amount(self):

        """Returns this year total earning and difference from previous year."""

        amount = self.transaction.objects.filter(refund=False, date_time__year__gte=datetime.today().year,
                                                 date_time__year__lte=datetime.today().year).aggregate(Sum('amount'))['amount__sum']
        prev_year = self.transaction.objects.filter(refund=False, date_time__year__gte=datetime.today().year - 1,
                                                    date_time__year__lte=datetime.today().year - 1).aggregate(
                                                                                              Sum('amount'))
        diff = 0

        if prev_year['amount__sum'] is not None:
            diff = amount['amount__sum'] - prev_year['amount__sum']
        if amount is None:
            amount = 0
        return amount, diff

    def __get_recent_bookings(self):

        """Returns recent bookings of bus, this will also behave differently in case of
            multiple vendor system."""

        return self.transaction.objects.filter(refund=False, date_time__date__gte=datetime.today() - timedelta(days=10))

    def __get_staffs_and_normal_users(self):

        """Return staffs and normal users."""

        normal_users = self.user.objects.filter(is_staff=False)
        staffs = self.user.objects.filter(is_staff=True)
        return staffs, normal_users

    def __get_data_for_chart(self):
        current_year = datetime.today().year
        current_month = datetime.today().month
        chart_data = []

        for i in range(1, current_month+1):
            data = self.transaction.objects.filter(refund=False, date_time__year=current_year,
                                                   date_time__month=i).aggregate(Sum('amount'))
            month = datetime(current_year, i, 1).strftime('%B')

            chart_data.append({'month': month, 'amount': data['amount__sum']})

        return chart_data


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
        print(schedule_departure_time[i])
        time = datetime.strptime(schedule_departure_time[i], "%H:%M")
        s_time = time.strftime("%I:%M")
        schedule = Schedule(bus_type=schedule_bus_type[i], bus_no=schedule_bus_no[i],
                            bus_capacity=seat_capacity[i], departure_time=s_time, route=route)
        schedule.save()


def get_earning_data(filter_by='day'):
    context = []
    i = 0
    print('function triggered')
    while True:

        data = Bus.objects.filter(departure_date=datetime.date(datetime.today() - timedelta(days=i)))

        if len(data) == 0:
            break
        count = data.count()
        date = datetime.date(datetime.today() - timedelta(days=i))
        earning = 0
        for sub_data in data:
            for tran_data in sub_data.transaction_set.filter(refund=False):
                earning += tran_data.amount
        context.append(
            {'date': date, 'count': count, 'amount': earning}
        )
        if filter_by == 'monthly':
            i += 30
        elif filter_by == 'yearly':
            i += 365
        else:
            i += 1

    return context


