from django.urls import path, include
from . import apis

app_name = 'users'

urlpatterns = [
    path('register/', apis.RegisterApiView.as_view(), name='register'),
    path("login/", apis.LoginApiView.as_view(), name="login"),
    path('activate_account/<str:uidb64>/<str:token>', apis.ActivateUserApiView.as_view(), name='activate_user'),
    path('send_verification_code/', apis.SendSMSAPIView.as_view(), name='send_sms'),
    #path("login_by_verification_code/", apis.ValidateSMSCodeApiView.as_view(), name="validate_code"),
    path("user/", apis.UserDetasilsApiView.as_view(), name="user-dateails")
]
