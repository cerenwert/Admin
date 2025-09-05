from django.contrib import admin
from .models import Company, ModelPerson, Offer, Contract

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(ModelPerson)
class ModelPersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("company","model","start_date","end_date","status","created_at")
    list_filter = ("status","start_date","end_date")
    search_fields = ("company__name","model__full_name")

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("offer","start_date","end_date","status","created_at")
    list_filter = ("status","start_date","end_date")
