from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    phone = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, write_only=True)
    password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_phone(self, value):
        if value == "" :
            raise serializers.ValidationError('Phone must be entered')
        elif not value.startswith("09") or len(value)<11:
            raise serializers.ValidationError('The phone number entered is incorrect')
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must contain at least 8 characters')
        elif not any(x.isalpha() for x in value):
            raise serializers.ValidationError('The password must contain letters (at least one uppercase and lowercase letter)')
        elif not any(x.isupper() for x in value):
            raise serializers.ValidationError('Password must contain at least one capital letter')
        elif not any(x.islower() for x in value):
            raise serializers.ValidationError('The password must contain at least one lowercase letter')
        elif not any(x.isdigit() for x in value):
            raise serializers.ValidationError('Password must contain numbers')
        elif not any(x in '!@#$%&*^' for x in value):
            raise serializers.ValidationError('The password must contain the symbol (!@#$%&*^)')
        return value
    
    def validate(self, attrs):
        #passwords validator
        pass1 = attrs.get('password')
        pass2 = attrs.get('password_confirm')
        if pass1 and pass2 and pass1 != pass2:
            raise serializers.ValidationError('passwords must be matche')
        print(attrs)
        return attrs
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    def validate_phone(self, value):
        if value == "" :
            raise serializers.ValidationError('Phone must be entered')
        elif not value.startswith("09") or len(value)<11:
            raise serializers.ValidationError('The phone number entered is incorrect')
        elif not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('The phone number entered does not exist')
        return value

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fiels = '__all__'