from rest_framework import serializers
from django.core.validators import RegexValidator

from detail.models import Status, StatusImages, Offer


class SendOTPSerializer(serializers.Serializer):
    mobile_number_regex = RegexValidator(
        regex=r'^(\+[0-9]{1,3})?[0-9]{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_number = serializers.CharField(
        max_length=15, validators=[mobile_number_regex])


class CheckOTPSerializer(serializers.Serializer):
    otp_id = serializers.IntegerField()
    otp = serializers.IntegerField()


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image']


class StatusSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Status
        fields = ['id', 'title', 'images']

    def get_images(self, obj):
        images = StatusImages.objects.filter(status=obj)
        return [image.image.url for image in images]
