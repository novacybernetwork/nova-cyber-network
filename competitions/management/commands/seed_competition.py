from datetime import datetime
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand

from accounts.models import School
from challenges.models import ChallengeCategory
from competitions.models import Competition

EASTERN = ZoneInfo("America/New_York")

DEFAULT_CATEGORIES = [
    ("Web Security", "globe"),
    ("Cryptography", "lock"),
    ("Digital Forensics", "search"),
    ("OSINT", "radar"),
    ("Reverse Engineering", "cpu"),
    ("Miscellaneous", "puzzle"),
]

DEFAULT_SCHOOLS = [
    "John Champe High School",
    "Academies of Loudoun",
    "Lightridge High School",
    "Freedom High School",
]

DEFAULT_RULES = """\
Only the challenges hosted on this platform are in scope for this competition.
Do not attack the competition website, other participants, or any external service.
Do not share flags between teams, even across your own school.
Collaboration within your own team is encouraged and allowed.
Automated traffic designed to disrupt the platform (scanners, brute-force scripts, DoS) is prohibited.
Treat other participants, mentors, and organizers with respect at all times.
Administrator decisions are final and resolve all scoring or conduct disputes.
Flag submissions close automatically the instant the competition ends; late submissions are not accepted.
"""


class Command(BaseCommand):
    help = "Idempotently creates/updates the NOVA Cyber Network CTF 2026 competition, categories, and schools."

    def handle(self, *args, **options):
        for name in DEFAULT_SCHOOLS:
            School.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS(f"Ensured {len(DEFAULT_SCHOOLS)} participating schools."))

        for order, (name, icon) in enumerate(DEFAULT_CATEGORIES):
            ChallengeCategory.objects.update_or_create(name=name, defaults={"icon_name": icon, "order": order})
        self.stdout.write(self.style.SUCCESS(f"Ensured {len(DEFAULT_CATEGORIES)} challenge categories."))

        start = datetime(2026, 10, 17, 0, 0, 0, tzinfo=EASTERN)
        end = datetime(2026, 10, 19, 0, 0, 0, tzinfo=EASTERN)  # exclusive boundary: submissions stop at midnight 10/19 ET

        competition, created = Competition.objects.get_or_create(
            slug="nova-ctf-2026",
            defaults={
                "name": "NOVA Cyber Network CTF 2026",
                "tagline": "Connect. Compete. Secure.",
                "description": (
                    "A student-led cybersecurity community bringing together the next generation of security "
                    "professionals across Northern Virginia."
                ),
                "start_time": start,
                "end_time": end,
                "is_published": True,
                "registration_open": True,
                "max_team_size": 5,
                "rules_text": DEFAULT_RULES,
                "contact_email": "contact@novacybernetwork.org",
            },
        )
        verb = "Created" if created else "Found existing"
        self.stdout.write(self.style.SUCCESS(f"{verb} competition '{competition.name}' (slug={competition.slug})."))
        self.stdout.write(
            f"Window: {competition.start_time_local:%Y-%m-%d %H:%M %Z} -> {competition.end_time_local:%Y-%m-%d %H:%M %Z}"
        )
