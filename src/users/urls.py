from django.urls import path, include
from . import apis

app_name = 'users'

urlpatterns = [
    path('register/', apis.RegisterApiView.as_view(), name='register'),
    path('activate_account/<str:uidb64>/<str:token>', apis.ActivateUserApiView.as_view(), name='activate_user'),
    path("login/", apis.LoginApiView.as_view(), name="login"),
    path('send_verification_code/', apis.SendSMSAPIView.as_view(), name='send_sms'),
    path("login_by_verification_code/", apis.ValidateSMSCodeApiView.as_view(), name="validate_code"),
    path("logout/", apis.LogoutApiViwe.as_view(), name="logout"),
    path("me/", apis.UserDetasilsApiView.as_view(), name="user-dateails"),
    path("change_info/", apis.ChangeUserDetasilsApiView.as_view(), name="change-user-information"),
    path("delete_account/", apis.DeleteUserApiView.as_view(), name="delete-user")
    
]
