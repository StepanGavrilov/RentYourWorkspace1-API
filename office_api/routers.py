from django.urls import path, include

from .views import OfficeAPI, ReservationAPI

app_name = 'office_system_api'

urlpatterns = [

    path('offices/<int:id>', OfficeAPI.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update',
    })),

    path('offices/', OfficeAPI.as_view({
        'post': 'create',
        'get': 'list',
    })),

    path('reservations/<int:id>', ReservationAPI.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update',
    })),

    path('reservations/', ReservationAPI.as_view({
        'post': 'create',
        'get': 'list',
    }))
]