from django.urls import path, include
from . import apis

app_name = 'users'

urlpatterns = [
    path('register/', apis.RegisterApi.as_view(), name='register'),
    path('activate_account/<str:uidb64>/<str:token>', apis.ActivateUserApiView.as_view(), name='activate_user'),
]
