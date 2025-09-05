from io import BytesIO
from django.template.loader import get_template
from django.utils import timezone
# xhtml2pdf kullanıyoruz (WeasyPrint yok)
from xhtml2pdf import pisa

def render_contract_html(contract):
    tpl = get_template('contracts/contract_pdf.html')
    return tpl.render({'contract': contract, 'now': timezone.localtime()})

def render_offer_html(offer):
    tpl = get_template('offers/offer_pdf.html')
    return tpl.render({'offer': offer, 'now': timezone.localtime()})

def html_to_pdf_bytes(html: str) -> bytes:
    pdf_io = BytesIO()
    result = pisa.CreatePDF(src=html, dest=pdf_io, encoding='utf-8')
    if result.err:
        raise RuntimeError('PDF oluşturma hatası (xhtml2pdf).')
    return pdf_io.getvalue()
