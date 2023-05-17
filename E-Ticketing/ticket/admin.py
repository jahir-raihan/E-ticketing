from django.contrib import admin
from .models import *

admin.site.register(Routes)
admin.site.register(Bus)
admin.site.register(Date)
admin.site.register(ParentBus)
admin.site.register(Seats)
admin.site.register(Schedule)
admin.site.register(Substations)
admin.site.register(InfoQueue)
admin.site.register(FreezeList)
admin.site.register(Transaction)
# Register your models here.
