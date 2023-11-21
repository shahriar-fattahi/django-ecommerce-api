from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import *


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'phone', 'first_name', 'last_name', 'is_admin']
    list_filter = ['is_admin', 'email_verified']

    fieldsets = [
        ('Identify', {"fields": ["email", "phone"]}),
        ("Personal Information", {"fields": ["first_name", "last_name", "password", "profile_picture"]}),
        ("Permissons", {"fields": ["is_superuser","is_admin", "is_active", "email_verified"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "phone", "first_name", "last_name", "password", "password_confirm"],
            },
        ),
    ]
    search_fields = ["email", "phone"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)


 
@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
	list_display = ('owner', 'country', 'province', 'city')
      
@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
	list_display = ('phone', 'code', 'start')
	


