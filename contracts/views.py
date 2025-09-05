from django.http import JsonResponse

def metrics_summary(request):
    data = {
        "ok": True,
        "users_total": 0,
        "offers_total": 0,
        "timestamp": request.META.get("REQUEST_TIME_FLOAT", None),
    }
    return JsonResponse(data)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.files.base import ContentFile

from .models import Contract
from .utils import render_contract_html, html_to_pdf_bytes

@staff_member_required
def contract_pdf_preview(request, pk: int):
    contract = get_object_or_404(Contract, pk=pk)
    html = render_contract_html(contract)
    pdf = html_to_pdf_bytes(html)
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = f'inline; filename=""'
    return resp

@staff_member_required
def contract_pdf_generate(request, pk: int):
    contract = get_object_or_404(Contract, pk=pk)
    html = render_contract_html(contract)
    pdf = html_to_pdf_bytes(html)
    fname = f"contract_{contract.pk}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    contract.pdf_file.save(fname, ContentFile(pdf), save=True)
    contract.pdf_generated_at = timezone.now()
    contract.save(update_fields=["pdf_generated_at"])
    return redirect("admin:contracts_contract_change", contract.pk)
