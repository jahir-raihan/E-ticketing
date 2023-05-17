from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
User = get_user_model()


class UserAdministrator(UserAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')
    filter_horizontal = ()
    ordering = ['name', 'phone']
    fieldsets = ()
    list_filter = ['name', ]
    readonly_fields = ()


    add_fieldsets = (
        (None, {
            'classes' : 'wide',
            'fields': ('name', 'email', 'phone',  'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdministrator)
# Register your models here.
