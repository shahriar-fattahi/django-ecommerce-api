from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import datetime
from pytz import timezone
from django.conf import settings
import jwt

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        return (text_type(user.is_active)+text_type(user.id)+text_type(timestamp))
    
account_activation_token = AccountActivationTokenGenerator()


def creat_token(user_id) ->str:
    payload = dict(
        id = user_id,
        exp = datetime.datetime.now(timezone(settings.TIME_ZONE)) + datetime.timedelta(hours=24),
        iat=datetime.datetime.now(timezone(settings.TIME_ZONE))
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token