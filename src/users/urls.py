from django.urls import path, include
from . import apis

app_name = 'users'

urlpatterns = [
    path('register/', apis.RegisterApi.as_view(), name='register'),
]
