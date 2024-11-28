from django.db.models.signals import post_save,pre_save
from django.dispatch.dispatcher import receiver
from django.db.transaction import atomic

from .models import Application,ApplicationPayment,ApplicationReconciliators,ApplicationTotalAmount,CANCELED,CONFIRMED

@receiver(signal=post_save,sender=ApplicationReconciliators)
def update_application_status(sender, instance:ApplicationReconciliators, created, **kwargs):
    if instance.status == CANCELED:
        instance.application.current_status =CANCELED

    instance.application._to_chek_reconciliations_statuses()
    instance.application.save(update_fields=['current_status'])
    print("send request to 1c")
    
    if created :
        print("send notification to users")
        pass
    
    
@receiver(signal=pre_save,sender=ApplicationReconciliators)
def update_reconciliators_sequence_hierarchy(sender, instance:ApplicationReconciliators, **kwargs):
    if not instance.pk and instance.sequence_hierarchy == 1:
        instance.is_current = True
        return 
    
    if instance.status == CONFIRMED:
        instance.is_current = False
        next_reconciliators = instance.application.reconciliators.filter(sequence_hierarchy__gt=instance.sequence_hierarchy).first()
        if next_reconciliators:
            next_reconciliators.is_current = True
            next_reconciliators.save(update_fields=['is_current'])    
        else:
            print("is closed")
