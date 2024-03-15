from django.core.management.base import BaseCommand
from src.models import *


class Command(BaseCommand):
    help = 'CAUTION!! Inserts initial data into the database FOR TEST PURPOSES IN LOCAL ENVIRONMENT'

    def handle(self, *args, **kwargs):
        u = User.objects.filter(username='testuser').first()
        if u:
            return
        u = User.objects.create_user(username='testuser', password='password123', is_staff=True, is_superuser=True)
        Account.objects.create(user=u, balance=100.00)
        Cryptocurrency.objects.create(name='ABAN', price=4.00)
        Cryptocurrency.objects.create(name='BTC', price=67.00)

        self.stdout.write(self.style.SUCCESS('Successfully inserted data into database'))
