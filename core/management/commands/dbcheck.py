from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Checks if the database connection is working'

    def handle(self, *args, **kwargs):
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS("✅ Database is connected"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Database not connected: {e}"))
