from django.core.mail import EmailMessage
from .models import VerificationCode
from random import randint
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from.utils import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse

def send_activation_link_by_email(request, user, email):
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    url = reverse('users:active',kwargs={
        'uidb64': uidb64,
        'token':account_activation_token.make_token(user)
    })
    link = f'http://+{domain}+{url}'
    EmailMessage(
    f'Activation link',
    link,
    'from@yourdjangoapp.com',
    [email],
    ).send(fail_silently=False)

def send_verification_code_by_phone(phone):
    if VerificationCode.objects.filter(phone = phone).exists():
        inc = VerificationCode.objects.get(phone=phone)
        if inc.is_valid():
            #sms.send(inc.code) - deponds on your services 
            return True
    code = randint(100000,1000000)
    VerificationCode.objects.create(
        phone=phone,
        code=code
    )
    #sms.send(code) - deponds on your services 
    return True