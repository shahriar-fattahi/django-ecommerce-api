from rest_framework import views, response, exceptions, permissions, status
from .serializer import *
from . import tasks
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from . import utils

class RegisterApiView(views.APIView):
    """
    Register new users using phone number, email and password.
    """
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.create_user(
            email=data['email'],
            phone=data['phone'],
            password=data['password_confirm'],
        )
        #tasks.send_activation_link_by_email(request, user, data['email'])
        return response.Response({'message': 'Check your email to activate your account'}, status.HTTP_201_CREATED)

class LoginApiView(views.APIView):
    """
    Login user using email and password - JWT authenication
    """
    def post(self, request):
        serializer = UserLoginSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(email=data['email'])
        except (User.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid Credentilas')
        
        if not user.check_password(data['password']):
            raise exceptions.AuthenticationFailed('Invalid Credentilas')
        
        token = utils.creat_token(user_id=user.id)

        resp = response.Response()
        resp.set_cookie(key="jwt", value=token, httponly=True)
        return resp

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
            return response.Response({'message': 'Your account is activated'})
        return response.Response({'message': 'Invalid link'}, status.HTTP_404_NOT_FOUND)

class SendSMSAPIView(views.APIView):
    """
    Check if submitted phone number is a valid phone number and send OTP.
    """
    def post(self, request):
        serializer = PhoneSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        verificationCode=tasks.send_verification_code_by_phone(data['phone'])
        return response.Response(
            {'message': 'We sent a Code to your phone number', 'time':f'{verificationCode.validity_time}'},
            status=status.HTTP_200_OK
            )
        
        