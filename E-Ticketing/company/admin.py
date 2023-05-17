from django.contrib import admin
from .models import *

admin.site.register(Root)
admin.site.register(Company)
admin.site.register(Routes)
admin.site.register(Substations)
admin.site.register(Schedule)

# Register your models here.
