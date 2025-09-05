from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Offer, Contract

@receiver(post_save, sender=Offer)
def create_contract_on_offer_approval(sender, instance, created, **kwargs):
    # created=False ve status 'approved' ise çalıştır
    if not created and instance.status == "approved":
        obj, made = Contract.objects.get_or_create(
            offer=instance,
            defaults={
                "start_date": instance.start_date,
                "end_date": instance.end_date,
                "status": "active",
            },
        )
        print(f"[signals] Offer #{instance.pk} approved -> Contract #{obj.pk} (created={made})")
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import date
from .models import Company, Contract
from .tasks import remind_expiring_contracts

@receiver(post_save, sender=Company)
def trigger_remind_when_email_added(sender, instance, created, **kwargs):
    # Yeni e-posta girildiyse hızlı kontrol
    if not instance.email:
        return
    today = date.today()
    has_due = Contract.objects.filter(
        offer__company=instance,
        end_date__gte=today
    ).exists()
    if has_due:
        # Toplu taramayı tetikle (ince ayar gerekirse company-id bazlı özel task yazabiliriz)
        remind_expiring_contracts.delay()
