from datetime import date, timedelta
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from celery import shared_task
from .models import Contract

REMIND_DAYS = (30, 7, 1)

def _should_remind(days_left:int) -> bool:
    return days_left in REMIND_DAYS

@shared_task
def remind_expiring_contracts():
    today = date.today()
    count_sent, count_skipped = 0, 0

    qs = Contract.objects.all().select_related('offer__company')
    for c in qs:
        if not (c.start_date and c.end_date and c.offer_id):
            continue
        days_left = (c.end_date - today).days
        if not _should_remind(days_left):
            continue

        company = c.offer.company if c.offer_id else None
        to_email = getattr(company, 'email', None) if company else None
        subject = f"Sözleşme {c.pk} {days_left} gün içinde bitiyor"
        body = (
            f"Merhaba,\n\n"
            f"{c.start_date:%d.%m.%Y}{c.end_date:%d.%m.%Y} tarihli sözleşmeniz {days_left} gün içinde sona eriyor.\n"
            f"Gerekirse uzatma için yanıtlayabilirsiniz.\n\n"
            f" Otomatik bildirim"
        )

        if to_email:
            EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [to_email]).send(fail_silently=True)
            count_sent += 1
        else:
            # e-posta yoksa sadece log
            print(f"[remind] Contract #{c.pk}: {days_left} gün kaldı, fakat şirket e-postası boş.")
            count_skipped += 1

    print(f"[remind] sent={count_sent} skipped={count_skipped} @ {timezone.now()}")
    return {"sent": count_sent, "skipped": count_skipped}
