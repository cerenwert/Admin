from datetime import date
from django.core.management.base import BaseCommand
from contracts.models import Contract

class Command(BaseCommand):
    help = 'Sözleşme durumlarını tarihe göre günceller (active/expired).'

    def handle(self, *args, **options):
        today = date.today()
        n_active = n_expired = 0
        for c in Contract.objects.all():
            if not (c.start_date and c.end_date): 
                continue
            if c.status != 'canceled' and c.end_date < today and c.status != 'expired':
                c.status = 'expired'
                c.save(update_fields=['status'])
                n_expired += 1
            elif c.status != 'canceled' and c.start_date <= today <= c.end_date and c.status != 'active':
                c.status = 'active'
                c.save(update_fields=['status'])
                n_active += 1
        self.stdout.write(self.style.SUCCESS(f'Updated: active={n_active}, expired={n_expired}'))
