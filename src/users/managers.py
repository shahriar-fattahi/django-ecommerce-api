from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, email, password, is_superuser=False):
        if not email:
            raise ValueError('Email must be entered')
        if not phone:
            raise ValueError('Phone must be entered')
        user = self.model(
            email=self.normalize_email(email),
            phone=phone
        )
        user.set_password(password)
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, email, password):
        user = self.create_user(phone, email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using= self._db)
        return user