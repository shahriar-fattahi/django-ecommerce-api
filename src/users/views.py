from rest_framework import (
    views,
    response,
    exceptions,
    permissions,
    status,
    generics,
    viewsets,
)
from .serializer import *
from . import tasks
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from . import utils
from . import authentication
from .permissions import IsAdminOrOwner


class RegisterApiView(views.APIView):
    """
    Register new users using phone number, email and password.
    """

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.create_user(
            email=data["email"],
            phone=data["phone"],
            password=data["password_confirm"],
        )
        # tasks.send_activation_link_by_email(request, user, data['email'])
        return response.Response(
            {"message": "Check your email to activate your account"},
            status.HTTP_201_CREATED,
        )


class ActivateUserApiView(views.APIView):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and utils.account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return response.Response({"message": "Your account is activated"})
        return response.Response({"message": "Invalid link"}, status.HTTP_404_NOT_FOUND)


class LoginApiView(views.APIView):
    """
    Login user using email and password - JWT authenication
    """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid Credentilas")

        if not user.check_password(data["password"]):
            raise exceptions.AuthenticationFailed("Invalid Credentilas")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("Your account has not been activated")

        token = utils.creat_jwt_token(user_id=user.id)

        resp = response.Response()
        resp.set_cookie(key="jwt", value=token, httponly=True)
        resp.data = {"message": "Successfully Logged In"}
        return resp


class SendSMSAPIView(views.APIView):
    """
    Check if submitted phone number is a valid phone number and send OTP.
    """

    def post(self, request):
        serializer = SendCodeSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        verificationCode = tasks.send_verification_code_by_phone(data["phone"])
        return response.Response(
            {
                "message": "We sent a Code to your phone number",
                "time": f"{verificationCode.validity_time}",
            },
            status=status.HTTP_200_OK,
        )


class ValidateSMSCodeApiView(views.APIView):
    """
    Login with verification code
    """

    def post(self, request):
        serializer = ValidationCodeSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.get(phone=data["phone"])
        token = utils.creat_jwt_token(user_id=user.id)
        resp = response.Response()
        resp.set_cookie(key="jwt", value=token, httponly=True)
        resp.data = {"message": "Successfully Logged In"}
        return resp


class LogoutApiViwe(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "Successfully Logged Out"}
        return resp


class UserDetasilsApiView(views.APIView):
    """
    Get user details. This endpoint can only be used if user is authenticated
    """

    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return response.Response(data=serializer.data)


class ChangeUserDetasilsApiView(generics.UpdateAPIView):
    """
    Change Information of user. This endpoint can only be used if user is authenticated
    """

    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class DeleteUserApiView(generics.DestroyAPIView):
    """
    Delete acoount. This endpoint can only be used if user is authenticated
    """

    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "Your Account Successfully Deleted"}
        resp.status_code = status.HTTP_204_NO_CONTENT
        return resp


class AddressViewSet(viewsets.ModelViewSet):
    """
    CRUD addresses
    """

    authentication_classes = (authentication.CustomUserAuthentication,)
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()

    def get_queryset(self):
        if self.request.user.is_admin:
            return UserAddress.objects.all()
        else:
            return UserAddress.objects.filter(owner_id=self.request.user.id)

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (IsAdminOrOwner,)

        return super().get_permissions()
