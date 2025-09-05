from datetime import date
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Contract

PROPOSAL_DAYS = (30, 7)  # 30 ve 7 gün kala sor

def run_renewal_proposals():
    today = date.today()
    sent = skipped = 0
    qs = Contract.objects.select_related('offer__company').all()

    for c in qs:
        if not (c.start_date and c.end_date and c.offer_id):
            continue

        days_left = (c.end_date - today).days
        if days_left not in PROPOSAL_DAYS:
            continue

        company = c.offer.company if c.offer_id else None
        to_email = getattr(company, 'email', None) if company else None

        subject = f"{c.service_name or 'Hizmet'} sözleşmesi {days_left} gün içinde bitiyor  Yenilemek ister misiniz?"
        body = (
            f"Merhaba {company.name if company else ''},\n\n"
            f"{c.start_date:%d.%m.%Y}{c.end_date:%d.%m.%Y} tarihli {c.service_name or 'hizmet'} sözleşmeniz {days_left} gün içinde sona eriyor.\n"
            f"İsterseniz {c.renewal_period_months} ay süreyle aynı koşullarla yenileyebiliriz.\n\n"
            f"Yanıt seçenekleri:\n"
            f"- EVET, yenileyelim.\n"
            f"- HAYIR, sonlandıracağız.\n"
            f"- FARKLI şartlarla teklif isteği.\n\n"
            f"Bu e-postayı yanıtlamanız yeterlidir.\n\n"
            f"Saygılarımızla"
        )

        if to_email:
            EmailMessage(subject, body, getattr(settings,'DEFAULT_FROM_EMAIL','noreply@example.com'), [to_email]).send(fail_silently=True)
            c.last_renewal_proposal_at = timezone.now()
            c.save(update_fields=['last_renewal_proposal_at'])
            sent += 1
        else:
            print(f"[renew-proposal] Contract #{c.pk}: {days_left} gün kaldı, e-posta yok -> atlandı")
            skipped += 1

    stamp = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[renew-proposal] sent={sent} skipped={skipped} @ {stamp}")
    return {"sent": sent, "skipped": skipped}
