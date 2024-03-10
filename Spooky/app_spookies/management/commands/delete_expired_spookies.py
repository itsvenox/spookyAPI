# app_spookies/management/commands/delete_expired_spookies.py
from django.core.management.base import BaseCommand
from app_spookies.models import delete_expired_spookies

class Command(BaseCommand):
    help = 'Deletes expired spookies'

    def handle(self, *args, **options):
        delete_expired_spookies()
        self.stdout.write(self.style.SUCCESS('Expired spookies deleted successfully'))
