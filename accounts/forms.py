from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Account
import re

special_char_list = r"!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
email_special_char_list = r"!\"#$%&'()*+,/:;<=>?@[\\]^`{|}~"

def num_checker(string):
    return any(i.isdigit() for i in string)

def special_char_checker(string):
    return any(i in special_char_list for i in string)

def email_special_char_checker(string):
    if "@" in string:
        email = re.split(r'@+', string)
        return any(i in email_special_char_list for i in email[0])
    return True

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['username', 'email', 'phone', 'first_name', 'last_name', 'password']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if num_checker(first_name):
            raise ValidationError("First Name can't contain numbers.")
        if special_char_checker(first_name):
            raise ValidationError("First Name can't contain special characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if num_checker(last_name):
            raise ValidationError("Last Name can't contain numbers.")
        if special_char_checker(last_name):
            raise ValidationError("Last Name can't contain special characters.")
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if special_char_checker(username):
            raise ValidationError("Username can't contain special characters.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_special_char_checker(email):
            raise ValidationError("Email can't contain special characters.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Password and Confirm Password do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if num_checker(first_name):
            raise ValidationError("First Name can't contain numbers.")
        if special_char_checker(first_name):
            raise ValidationError("First Name can't contain special characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if num_checker(last_name):
            raise ValidationError("Last Name can't contain numbers.")
        if special_char_checker(last_name):
            raise ValidationError("Last Name can't contain special characters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_special_char_checker(email):
            raise ValidationError("Email can't contain special characters.")
        return email

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}),
        label="Old Password",
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        label="New Password",
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        label="Confirm New Password",
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
