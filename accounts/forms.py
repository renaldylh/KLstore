from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Account
import re

class CustomValidationMixin:
    special_char_list = r"!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    email_special_char_list = r"!\"#$%&'()*+,/:;<=>?@[\\]^`{|}~"

    def num_checker(self, string):
        return any(i.isdigit() for i in string)

    def special_char_checker(self, string):
        return any(i in self.special_char_list for i in string)

    def email_special_char_checker(self, string):
        if "@" in string:
            email = re.split(r'@+', string)
            return any(i in self.email_special_char_list for i in email[0])
        return True

class RegisterForm(forms.ModelForm, CustomValidationMixin):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['username', 'email', 'phone', 'first_name', 'last_name', 'password']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if self.num_checker(first_name):
            raise ValidationError("First Name can't contain numbers.")
        if self.special_char_checker(first_name):
            raise ValidationError("First Name can't contain special characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if self.num_checker(last_name):
            raise ValidationError("Last Name can't contain numbers.")
        if self.special_char_checker(last_name):
            raise ValidationError("Last Name can't contain special characters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.email_special_char_checker(email):
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

class ProfileEditForm(forms.ModelForm, CustomValidationMixin):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if self.num_checker(first_name):
            raise ValidationError("First Name can't contain numbers.")
        if self.special_char_checker(first_name):
            raise ValidationError("First Name can't contain special characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if self.num_checker(last_name):
            raise ValidationError("Last Name can't contain numbers.")
        if self.special_char_checker(last_name):
            raise ValidationError("Last Name can't contain special characters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.email_special_char_checker(email):
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

