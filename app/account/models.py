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
from product.models import Product


class CustomUserManager(BaseUserManager):
    """ Manager for users. """

    def create_user(self, password=None, **extra_fields):
        """ Create, save and return a new user. """
        email = extra_fields.pop(
            'email', None)  # Extract email from extra_fields
        if email:
            email = self.normalize_email(email)  # Normalize email if provided
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, **extra_fields):
        """ Create and return a new superuser. """
        user = self.create_user(password=password, **extra_fields)
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

    email = models.EmailField(
        max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True)
    mobile_number = models.CharField(
        max_length=15, validators=[mobile_number_regex], unique=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    wishlist = models.OneToOneField(
        'Wishlist', on_delete=models.CASCADE, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.mobile_number


class Wishlist(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='user_wishlist')
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f'Wishlist of {self.user.name} {self.user.surname}'
