"""
Custom User model.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """ Manager for users. """

    def create_user(self, email, password=None, **extra_fields):
        """ Create, save and return a new user. """
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Create and return a new superuser. """
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ User in the system. """
    GENDER_CHOICES = (
        ('man', "Kişi"),
        ('woman', "Qadın"),
    )
    mobile_number_regex = RegexValidator(
        regex=r'^(\+[0-9]{1,3})?[0-9]{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    mobile_number = models.CharField(
        max_length=15, validators=[mobile_number_regex], unique=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.email


class OTP(models.Model):
    otp = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()

    def is_expired(self):
        return self.expiration_time < timezone.now()

    def __str__(self):
        return self.otp
