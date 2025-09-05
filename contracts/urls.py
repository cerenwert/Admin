from django.urls import path
from . import views

urlpatterns = [
    path("contracts/<int:pk>/pdf/preview/", views.contract_pdf_preview, name="contract_pdf_preview"),
    path("contracts/<int:pk>/pdf/generate/", views.contract_pdf_generate, name="contract_pdf_generate"),
]
from django.urls import path
from . import views_offer_pdf

urlpatterns += [
    path('offers/<int:pk>/pdf/preview/', views_offer_pdf.offer_pdf_preview, name='offer_pdf_preview'),
    path('offers/<int:pk>/pdf/generate/', views_offer_pdf.offer_pdf_generate, name='offer_pdf_generate'),
    path('offers/<int:pk>/pdf/send/', views_offer_pdf.offer_pdf_send, name='offer_pdf_send'),
]
