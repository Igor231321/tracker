from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Status, Transaction


@receiver(pre_delete, sender=Transaction)
def update_balance_before_delete(sender, instance, **kwargs):
    if instance.status == Status.EXPENSE:
        instance.user.balance += instance.amount
    else:
        instance.user.balance -= instance.amount

    instance.user.save()
