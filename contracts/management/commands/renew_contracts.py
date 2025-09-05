from django.core.management.base import BaseCommand
from contracts.models import Contract
from datetime import date
from dateutil.relativedelta import relativedelta  # python-dateutil yüklü olmalı

class Command(BaseCommand):
    help = 'auto_renew=True olan ve süresi dolmuş sözleşmeleri renewal_period_months kadar ileri taşır.'

    def handle(self, *args, **options):
        today = date.today()
        renewed = 0
        for c in Contract.objects.filter(auto_renew=True, end_date__lt=today):
            months = c.renewal_period_months or 12
            delta = relativedelta(months=+months)
            old_start, old_end = c.start_date, c.end_date
            # yeni dönem: bitişten itibaren
            c.start_date = (old_end + relativedelta(days=+1)) if old_end else today
            c.end_date = (c.start_date + delta - relativedelta(days=1))
            c.status = "active"
            c.save(update_fields=['start_date','end_date','status'])
            renewed += 1
            print(f"[auto-renew] Contract #{c.pk}: {old_start}{old_end} -> {c.start_date}{c.end_date}")
        self.stdout.write(self.style.SUCCESS(f"Auto-renew completed: {renewed} contract(s)"))
