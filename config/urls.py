from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from contracts.views import metrics_summary

urlpatterns = [
    path("", lambda r: redirect("/admin/", permanent=False)),
    path("metrics/summary/", metrics_summary, name="metrics-summary"),  # herkese açık (admin dışı)
    path("admin/", admin.site.urls),
]
