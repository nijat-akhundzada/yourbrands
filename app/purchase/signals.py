from django.db.models.signals import post_save
from django.dispatch import receiver
from purchase.models import Order


@receiver(post_save, sender=Order)
def update_is_paid(sender, instance, created, **kwargs):
    if instance.status == 'Delivered':
        instance.is_paid = True
        instance.save(update_fields=['is_paid'])
