import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Idempotently ensures a superuser exists, reading credentials from "
        "DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_EMAIL / DJANGO_SUPERUSER_PASSWORD env vars. "
        "Safe to run on every deploy: never overwrites the password of an existing account, "
        "and does nothing if the required env vars are not set."
    )

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_USERNAME/DJANGO_SUPERUSER_PASSWORD not set; skipping admin bootstrap."
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists; leaving password unchanged."))
            return

        # create_superuser sets is_staff/is_superuser before the row is first saved, so the
        # accounts.signals.ensure_profile receiver sees the correct is_superuser value on creation.
        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
