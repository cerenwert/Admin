from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# DOĞRU: view'ları modüllerinden import et
from contracts.views import metrics_summary
from contracts.api import ModelPersonListCreateView, OfferListCreateView  # varsa

urlpatterns = [
    path("", lambda r: redirect("/admin/", permanent=False)),
    path("metrics/summary/", metrics_summary, name="metrics-summary"),

    # API uçları (önceki adımlarda eklediğimiz DRF view'ları)
    path("api/wp/models/", ModelPersonListCreateView.as_view(), name="models-list-create"),
    path("api/wp/offers/", OfferListCreateView.as_view(), name="offers-list-create"),

    path("admin/", admin.site.urls),
]

from django.urls import include

urlpatterns += [ path('admin-tools/', include('contracts.urls')), ]
