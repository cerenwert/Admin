from django.core.management.base import BaseCommand
from contracts.renewals import run_renewal_proposals

class Command(BaseCommand):
    help = 'Bitişe 30/7 gün kala firmalara yenileme önerisi e-postası gönderir.'

    def handle(self, *args, **options):
        res = run_renewal_proposals()
        self.stdout.write(self.style.SUCCESS(f'Done: {res}'))
