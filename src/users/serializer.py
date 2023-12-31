from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "first_name",
            "last_name",
            "profile_picture",
            "is_active",
        )

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.save()
        return instance


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(required=True, write_only=True)
    password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_phone(self, value):
        if value == "":
            raise serializers.ValidationError("Phone must be entered")
        elif not value.startswith("09") or len(value) < 11:
            raise serializers.ValidationError("The phone number entered is incorrect")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must contain at least 8 characters"
            )
        elif not any(x.isalpha() for x in value):
            raise serializers.ValidationError(
                "The password must contain letters (at least one uppercase and lowercase letter)"
            )
        elif not any(x.isupper() for x in value):
            raise serializers.ValidationError(
                "Password must contain at least one capital letter"
            )
        elif not any(x.islower() for x in value):
            raise serializers.ValidationError(
                "The password must contain at least one lowercase letter"
            )
        elif not any(x.isdigit() for x in value):
            raise serializers.ValidationError("Password must contain numbers")
        elif not any(x in "!@#$%&*^" for x in value):
            raise serializers.ValidationError(
                "The password must contain the symbol (!@#$%&*^)"
            )
        return value

    def validate(self, attrs):
        # passwords validator
        pass1 = attrs.get("password")
        pass2 = attrs.get("password_confirm")
        if pass1 and pass2 and pass1 != pass2:
            raise serializers.ValidationError("passwords must be matche")
        return attrs


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

    def validate_phone(self, value):
        if value == "":
            raise serializers.ValidationError("Phone must be entered")
        elif not value.startswith("09") or len(value) < 11:
            raise serializers.ValidationError("The phone number entered is incorrect")
        elif not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("The phone number entered does not exist")
        elif not User.objects.get(phone=value).is_active:
            raise serializers.ValidationError("Your account has not been activated")
        return value


class ValidationCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        if not User.objects.filter(phone=attrs["phone"]).exists():
            raise serializers.ValidationError(
                {"Phone": ["The number entered is not registered"]}
            )
        if not User.objects.get(phone=attrs["phone"]).is_active:
            raise serializers.ValidationError(
                {"Phone": ["Your account has not been activated"]}
            )

        try:
            inc = VerificationCode.objects.get(user__phone=attrs["phone"])
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError(
                {"Code": ["You must first receive a verification code"]}
            )
        if not inc.is_valid:
            raise serializers.ValidationError(
                {"Code": ["Your verification code has expired"]}
            )
        if inc.code != attrs["code"]:
            raise serializers.ValidationError(
                {"Code": ["The verification code entered is invalid"]}
            )
        return attrs


class UserAddressSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAddress
        fields = "__all__"

    def update(self, instance, validated_data):
        validated_data.pop("owner")
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must contain at least 8 characters"
            )
        elif not any(x.isalpha() for x in value):
            raise serializers.ValidationError(
                "The password must contain letters (at least one uppercase and lowercase letter)"
            )
        elif not any(x.isupper() for x in value):
            raise serializers.ValidationError(
                "Password must contain at least one capital letter"
            )
        elif not any(x.islower() for x in value):
            raise serializers.ValidationError(
                "The password must contain at least one lowercase letter"
            )
        elif not any(x.isdigit() for x in value):
            raise serializers.ValidationError("Password must contain numbers")
        elif not any(x in "!@#$%&*^" for x in value):
            raise serializers.ValidationError(
                "The password must contain the symbol (!@#$%&*^)"
            )
        return value

    def validate(self, attrs):
        # passwords validator
        pass1 = attrs.get("new_password")
        pass2 = attrs.get("new_password_confirm")
        if pass1 and pass2 and pass1 != pass2:
            raise serializers.ValidationError("New passwords must be matche")
        return attrs


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
