from django.contrib import admin
from .models import Users


# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'login', 'password', 'email', 'role', 'is_active')
    search_fields = ('username', 'login', 'password', 'email', 'role')
    list_filter = ('role', 'is_active')
    list_per_page = 50

    readonly_fields = ('password',)


admin.site.site_header = 'Administration'
admin.site.register(Users, UsersAdmin)
