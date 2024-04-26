from rest_framework import serializers
from account.models import CustomUser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.core.validators import RegexValidator

from drf_spectacular.utils import extend_schema_field


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


class PostSerializer(serializers.Serializer):
    mobile_number_regex = RegexValidator(
        regex=r'^(\+[0-9]{1,3})?[0-9]{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    password = serializers.CharField()  # Include password field explicitly
    otp_id = serializers.IntegerField()
    otp = serializers.IntegerField()
    email = serializers.EmailField(max_length=255)
    name = serializers.CharField(max_length=255)
    surname = serializers.CharField(max_length=255, required=False)
    birth_date = serializers.DateField(required=False)
    mobile_number = serializers.CharField(
        max_length=15, validators=[mobile_number_regex])
    gender = serializers.CharField(
        max_length=6)

    class Meta:
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}, 'otp_id': {
            'write_only': True}, 'otp': {'write_only': True}}

    @extend_schema_field(serializers.CharField())
    def get_password(self, obj):
        # This function is necessary to make DRF Spectacular include password field in the schema
        return '********'  # Return some placeholder value

    def create(self, validated_data):
        # Create and return a new instance of CustomUser using the validated data
        return CustomUser.objects.create(**validated_data)


class ResetPasswordSerializer(serializers.Serializer):
    mobile_number_regex = RegexValidator(
        regex=r'^(\+[0-9]{1,3})?[0-9]{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    mobile_number = serializers.CharField(
        max_length=15, validators=[mobile_number_regex])
    otp = serializers.CharField(max_length=6)
    otp_id = serializers.IntegerField()
    new_password = serializers.CharField(max_length=128)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
