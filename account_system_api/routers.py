from django.urls import path, include

from .views import AccountAPI


app_name = 'account_system_api'

urlpatterns = [

    path('auth/', include('djoser.urls.jwt')),  # Create/Update/Refresh JWTtoken

    path('accounts/<int:id>', AccountAPI.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update',
    })),
    path('accounts/', AccountAPI.as_view({
        'post': 'create',
        'get': 'list',
    }))
]