from django.contrib import admin
from detail.models import FAQ, Offer, PrivacyPolicy, Status, StatusImages, TermAndCondition, OTP

# Register your models here.
admin.site.register(FAQ)
admin.site.register(Offer)
admin.site.register(PrivacyPolicy)
admin.site.register(Status)
admin.site.register(StatusImages)
admin.site.register(TermAndCondition)
admin.site.register(OTP)
