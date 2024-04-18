from rest_framework import serializers
from account.models import CustomUser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.core.validators import RegexValidator


class CustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for CustomUser model. """

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'name', 'surname',
                  'birth_date', 'mobile_number', 'gender', 'is_active', 'is_staff']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['mobile_number'] = user.mobile_number

        return token


class SendOTPSerializer(serializers.Serializer):
    mobile_number_regex = RegexValidator(
        regex=r'^(\+[0-9]{1,3})?[0-9]{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_number = serializers.CharField(
        max_length=15, validators=[mobile_number_regex])


class PostSerializer(serializers.ModelSerializer):
    otp_id = serializers.IntegerField()
    otp = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['otp_id', 'otp', 'id', 'email', 'password', 'name', 'surname',
                  'birth_date', 'mobile_number', 'gender', 'is_active', 'is_staff']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}, 'otp_id': {
            'write_only': True}, 'otp': {'write_only': True}}
