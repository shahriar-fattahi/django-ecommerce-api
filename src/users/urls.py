from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "users"

router = DefaultRouter()
router.register(r"", views.AddressViewSet)

urlpatterns = [
    path("register/", views.RegisterApiView.as_view(), name="register"),
    path(
        "activate_account/<str:uidb64>/<str:token>",
        views.ActivateUserApiView.as_view(),
        name="activate_user",
    ),
    path("login/", views.LoginApiView.as_view(), name="login"),
    path("send_verification_code/", views.SendSMSAPIView.as_view(), name="send_sms"),
    path(
        "login_by_verification_code/",
        views.ValidateSMSCodeApiView.as_view(),
        name="validate_code",
    ),
    path("logout/", views.LogoutApiViwe.as_view(), name="logout"),
    path("me/", views.UserDetasilsApiView.as_view(), name="user-dateails"),
    path(
        "change_info/",
        views.ChangeUserDetasilsApiView.as_view(),
        name="change-user-information",
    ),
    path("delete_account/", views.DeleteUserApiView.as_view(), name="delete-user"),
    path("addresses/", include(router.urls)),
]
