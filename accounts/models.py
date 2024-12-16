from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import (
    RegexValidator,
    EmailValidator,
    MinLengthValidator,
    MaxLengthValidator,
)

class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, phone, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone=phone
        )
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, phone, email, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone=phone,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        help_text="First name must contain at least 2 characters."
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        validators=[MinLengthValidator(2)],
        help_text="Last name must contain at least 2 characters."
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message="Username may contain only letters, numbers, and @/./+/-/_ characters."
            ),
            MinLengthValidator(3),
        ],
        help_text="Username must be at least 3 characters long."
    )
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            ),
        ],
        help_text="Enter a valid phone number."
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Enter a valid email address."
    )

    registered_on = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'phone']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
