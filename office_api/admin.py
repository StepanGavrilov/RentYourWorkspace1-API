from django.contrib import admin

from .models import Office, Reservation


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(Reservation)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('customer', 'office', 'datetime_from', 'datetime_to')
