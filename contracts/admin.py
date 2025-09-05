from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.urls import reverse
from dateutil.relativedelta import relativedelta
from datetime import date
from .models import Company, ModelPerson, Offer, Contract

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id','name','email')
    search_fields = ('name','email')

@admin.register(ModelPerson)
class ModelPersonAdmin(admin.ModelAdmin):
    list_display = ('id','full_name')
    search_fields = ('full_name',)

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id','company','model','start_date','end_date','price','status','offer_pdf_generated_at')
    list_filter = ('status','start_date','end_date')
    search_fields = ('company__name','model__full_name')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id','service_name','company_name','start_date','end_date','days_left','status','auto_renew','renewal_period_months','last_renewal_proposal_at')
    list_filter = ('status','auto_renew','start_date','end_date')
    search_fields = ('service_name','offer__company__name','offer__model__full_name')
    actions = ['renew_now']

    def company_name(self, obj):
        return obj.offer.company.name if obj.offer_id else "-"
    company_name.short_description = "Company"

    def renew_now(self, request, queryset):
        cnt = 0
        today = date.today()
        for c in queryset:
            months = c.renewal_period_months or 12
            # dönem, mevcut bitişten itibaren başlasın
            start = (c.end_date + relativedelta(days=+1)) if c.end_date else today
            end   = (start + relativedelta(months=+months) - relativedelta(days=1))
            c.start_date, c.end_date, c.status = start, end, "active"
            c.save(update_fields=['start_date','end_date','status'])
            cnt += 1
        self.message_user(request, f"{cnt} sözleşme {months} ay uzatıldı.", level=messages.SUCCESS)
    renew_now.short_description = "Seçilenleri hemen yenile (+N ay)"
