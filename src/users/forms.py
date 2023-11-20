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

    def clean_phone(self):
        value = self.cleaned_data['phone']
        if value == "" :
            raise forms.ValidationError('Phone must be entered')
        elif not value.startswith("09") or len(value)<11:
            raise forms.ValidationError('The phone number entered is incorrect')
        return value
    
    def clean_password(self):
        value = self.cleaned_data['password']
        if len(value) < 8:
            raise forms.ValidationError('Password must contain at least 8 characters')
        elif not any(x.isalpha() for x in value):
            raise forms.ValidationError('The password must contain letters (at least one uppercase and lowercase letter)')
        elif not any(x.isupper() for x in value):
            raise forms.ValidationError('Password must contain at least one capital letter')
        elif not any(x.islower() for x in value):
            raise forms.ValidationError('The password must contain at least one lowercase letter')
        elif not any(x.isdigit() for x in value):
            raise forms.ValidationError('Password must contain numbers')
        elif not any(x in '!@#$%&*^' for x in value):
            raise forms.ValidationError('The password must contain the symbol (!@#$%&*^)')
        return value
    
    def clean_password_confirm(self):
        data = self.cleaned_data
        pass1 = data.get('password')
        pass2 = data.get('password_confirm')
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Passwords don't match")
        return pass2
    
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