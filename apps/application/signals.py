from django.db.models.signals import post_save,pre_save
from django.dispatch.dispatcher import receiver
from django.db.transaction import atomic

from .models import Application,ApplicationPayment,ApplicationReconciliators,ApplicationTotalAmount,CANCELED

@receiver(signal=post_save,sender=ApplicationReconciliators)
def update_application_status(sender, instance, created, **kwargs):
    if instance.status == CANCELED:
        instance.application.current_status =CANCELED
    instance.application._to_chek_reconciliations_statuses()
    instance.application.save(update_fields=['current_status'])
    print("send request to 1c")
    
    if created :
        print("send notification to users")
        pass
