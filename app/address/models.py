from django.db import models
from django.core.validators import RegexValidator
from account.models import CustomUser

# Create your models here.


class Address(models.Model):
    mobile_number_regex = RegexValidator(
        regex=r'^(\+[0-9]{1,3})?[0-9]{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name_surname = models.CharField(max_length=255)
    mobile_number = models.CharField(
        max_length=15, validators=[mobile_number_regex])
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'address of {self.user.name
                             } {self.user.surname}'
