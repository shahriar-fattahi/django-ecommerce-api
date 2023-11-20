from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        ordering = ['-id']
    
    #identifier
    email = models.EmailField(max_length=254, unique=True)

    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone',]

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    def __str__(self) -> str:
        return self.email


class UserAddress(models.Model):
    class Meta:
        ordering = ['-id']
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=11)
    country = models.CharField(max_length=50, default='Iran')
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    details = models.TextField()
    house_number = models.CharField(max_length=20)
    unit = models.IntegerField(null=True, blank=True)
    postal_code = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.country} - {self.province} - {self.city}'
    