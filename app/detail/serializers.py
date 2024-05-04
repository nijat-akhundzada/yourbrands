from rest_framework import serializers
from django.core.validators import RegexValidator


class SendOTPSerializer(serializers.Serializer):
    mobile_number_regex = RegexValidator(
        regex=r'^(\+[0-9]{1,3})?[0-9]{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_number = serializers.CharField(
        max_length=15, validators=[mobile_number_regex])


class CheckOTPSerializer(serializers.Serializer):
    otp_id = serializers.IntegerField()
    otp = serializers.IntegerField()
