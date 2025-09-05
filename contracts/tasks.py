from datetime import date, timedelta
from celery import shared_task
from .models import Contract

@shared_task
def schedule_expiry_notifications():
    soon = date.today() + timedelta(days=7)
    qs = Contract.objects.filter(end_date__lte=soon, status="active")
    # MVP: sadece sayısını logla
    return {"expiring_7_days_or_less": qs.count()}
