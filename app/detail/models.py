from django.db import models
from django.utils import timezone

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FAQ(BaseModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()


class TermAndCondition(BaseModel):
    terms_and_conditions = models.TextField()

    def __str__(self):
        return 'Our Terms&Conditions'


class PrivacyPolicy(BaseModel):
    privacy_policy = models.TextField()

    def __str__(self):
        return 'Our Privacy Policy'


class Offer(BaseModel):
    title = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to='offers_images')

    def __str__(self):
        return self.title


class Status(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class StatusImages(BaseModel):
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='status_images')

    def __str__(self):
        return self.status


class OTP(models.Model):
    otp = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()

    def is_expired(self):
        return self.expiration_time < timezone.now()

    def __str__(self):
        return self.otp
