from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    """
        A form for creating new users in admin panel.
    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone']

    def clean_password_confirm(self):
        data = self.cleaned_data
        if data['password'] and data['password_confirm'] and data['password'] != data['password_confirm']:
            raise forms.ValidationError("Passwords don't match")
        return data['password_confirm']
    def save(self, commit: True):
        user = super().save(commit=False)
        user.set_password(self.data['password'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """
        A form for updating users in admin panel.
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = '__all__'