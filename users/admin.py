from django.contrib import admin
from .models import CustomUser


# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    list_display = ("nickname", "login", "password", "email", "role", "is_active")
    search_fields = ("nickname", "login", "password", "email", "role")
    list_filter = ("role", "is_active")
    list_per_page = 50

    readonly_fields = ("password",)


admin.site.site_header = "Administration"
admin.site.register(CustomUser, UsersAdmin)
