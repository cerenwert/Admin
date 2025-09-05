from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Offer
from .utils import render_offer_html, html_to_pdf_bytes

@staff_member_required
def offer_pdf_preview(request, pk:int):
    offer = get_object_or_404(Offer, pk=pk)
    html = render_offer_html(offer)
    pdf = html_to_pdf_bytes(html)
    resp = HttpResponse(pdf, content_type='application/pdf')
    resp['Content-Disposition'] = f'inline; filename=""'
    return resp

@staff_member_required
def offer_pdf_generate(request, pk:int):
    offer = get_object_or_404(Offer, pk=pk)
    html = render_offer_html(offer)
    pdf = html_to_pdf_bytes(html)
    fname = f"offer_{offer.pk}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    offer.offer_pdf_file.save(fname, ContentFile(pdf), save=True)
    offer.offer_pdf_generated_at = timezone.now()
    offer.status = 'sent' if offer.status == 'pending' else offer.status
    offer.save(update_fields=['offer_pdf_generated_at','status'])
    return redirect('admin:contracts_offer_change', offer.pk)

@staff_member_required
def offer_pdf_send(request, pk:int):
    offer = get_object_or_404(Offer, pk=pk)
    to_email = getattr(offer.company, 'email', None)
    if not to_email:
        return HttpResponseBadRequest('Şirket için e-posta adresi tanımlı değil.')

    # PDF varsa kullan, yoksa üret
    if offer.offer_pdf_file:
        pdf_bytes = offer.offer_pdf_file.read()
        fname = offer.offer_pdf_file.name.split('/')[-1]
    else:
        html = render_offer_html(offer)
        pdf_bytes = html_to_pdf_bytes(html)
        fname = f"offer_{offer.pk}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        offer.offer_pdf_file.save(fname, ContentFile(pdf_bytes), save=True)
        offer.offer_pdf_generated_at = timezone.now()
        offer.save(update_fields=['offer_pdf_generated_at'])

    subject = f"Teklif #{offer.pk} - {offer.company.name}"
    body = (
        f"Merhaba,\n\nEkte {offer.start_date:%d.%m.%Y}-{offer.end_date:%d.%m.%Y} tarihleri için teklifimizi bulabilirsiniz.\n"
        "Her türlü sorunuz için bu e-postayı yanıtlayabilirsiniz.\n\nSaygılarımızla"
    )
    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [to_email])
    email.attach(fname, pdf_bytes, 'application/pdf')
    email.send(fail_silently=False)

    # durum güncelle
    if offer.status in ('draft','pending'):
        offer.status = 'sent'
        offer.save(update_fields=['status'])
    return redirect('admin:contracts_offer_change', offer.pk)
