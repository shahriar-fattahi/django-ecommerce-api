from rest_framework import views, response, exceptions, permissions, status
from .serializer import *



class RegisterApi(views.APIView):
    """
    Register new users using phone number, email and password.
    """
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        User.objects.create_user(
            email=data['email'],
            phone=data['phone'],
            password=data['password_confirm'],
        )
        return response.Response({'message': 'Check your email'}, status.HTTP_201_CREATED)
        