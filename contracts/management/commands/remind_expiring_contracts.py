from django.core.management.base import BaseCommand
from contracts.reminders import run_contract_reminders

class Command(BaseCommand):
    help = 'Bitmesi yaklaşan sözleşmeler için e-posta hatırlatmaları gönderir (30/7/1 gün kala).'

    def handle(self, *args, **options):
        res = run_contract_reminders()
        self.stdout.write(self.style.SUCCESS(f"Done: {res}"))
