from datetime import date
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Contract

REMIND_DAYS = (30, 7, 1)

def run_contract_reminders():
    today = date.today()
    sent = skipped = 0
    qs = Contract.objects.all().select_related('offer__company')
    for c in qs:
        if not (c.start_date and c.end_date and c.offer_id):
            continue
        days_left = (c.end_date - today).days
        if days_left not in REMIND_DAYS:
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
            EmailMessage(subject, body, getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'), [to_email]).send(fail_silently=True)
            sent += 1
        else:
            print(f"[remind] Contract #{c.pk}: {days_left} gün kaldı, fakat şirket e-postası boş.")
            skipped += 1
    stamp = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[remind] sent={sent} skipped={skipped} @ {stamp}")
    return {"sent": sent, "skipped": skipped}
