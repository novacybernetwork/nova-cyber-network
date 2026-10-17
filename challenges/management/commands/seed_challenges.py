from django.core.management.base import BaseCommand, CommandError

from challenges.models import Challenge, ChallengeAttachment, ChallengeCategory
from competitions.models import Competition

# Each entry: category name, title, difficulty, points, description, flag, [hints], [(display_name, relative_path)]
STARTER_CHALLENGES = [
    (
        "Web Security",
        "Robots Only",
        Challenge.DIFFICULTY_EASY,
        100,
        "A small sample site shipped its robots.txt. Crawlers are told to stay out of one path — but robots.txt "
        "is public, and so is whatever it points to. Download both files and see what the crawler was told to skip.",
        "NOVA{robots_dot_txt_isnt_a_secret}",
        ["robots.txt only tells well-behaved crawlers where NOT to go — it doesn't block humans."],
        [("robots.txt", "web-security/robots.txt"), ("status-9f21.html", "web-security/status-9f21.html")],
    ),
    (
        "Web Security",
        "Cookie Jar",
        Challenge.DIFFICULTY_MEDIUM,
        250,
        "We captured a raw HTTP response from a demo shop. Something about that session cookie looks off once "
        "you actually decode it.",
        "NOVA{c00ki3s_lie_about_trust}",
        [
            "Cookies are often base64 — decode it and see what's inside.",
            "One of the decoded JSON fields is itself encoded again.",
        ],
        [("session_dump.txt", "web-security/session_dump.txt")],
    ),
    (
        "Cryptography",
        "Caesar's Welcome",
        Challenge.DIFFICULTY_EASY,
        100,
        "A short welcome message was intercepted. It's encrypted with one of the oldest tricks in the book.",
        "NOVA{caesar_says_hi}",
        ["There are only 25 possible shifts — or just think about who this cipher is named after."],
        [("caesars_welcome.txt", "cryptography/caesars_welcome.txt")],
    ),
    (
        "Cryptography",
        "XOR Marks the Spot",
        Challenge.DIFFICULTY_MEDIUM,
        250,
        "A flag was XOR-encrypted with a single repeating byte key. We don't know the key, but we know how "
        "every NOVA flag starts.",
        "NOVA{xor_keys_are_fun}",
        ["XOR the first ciphertext byte with the letter 'N' to recover the key, then XOR the rest."],
        [("xor_ciphertext.txt", "cryptography/xor_ciphertext.txt")],
    ),
    (
        "Digital Forensics",
        "Metadata Doesn't Lie",
        Challenge.DIFFICULTY_EASY,
        100,
        "This looks like a `strings` dump pulled from a device firmware image. Somewhere in the noise, a flag "
        "was left behind by a careless developer.",
        "NOVA{strings_find_what_grep_misses}",
        ["Searching a text dump for 'NOVA{' is a perfectly legitimate forensics technique."],
        [("firmware_strings.txt", "digital-forensics/firmware_strings.txt")],
    ),
    (
        "Digital Forensics",
        "The Deleted Log",
        Challenge.DIFFICULTY_MEDIUM,
        250,
        "A web server's access log was exported as CSV. Most rows are mundane — but one request's User-Agent "
        "string hides something that isn't a browser fingerprint.",
        "NOVA{logs_never_really_disappear}",
        ["Scan the user_agent column for anything that looks like base64, not a real browser string."],
        [("server_access.log.csv", "digital-forensics/server_access.log.csv")],
    ),
    (
        "OSINT",
        "Profile Recon",
        Challenge.DIFFICULTY_EASY,
        100,
        "A fictional training dossier (not a real person) was left with public notes. Read closely — OSINT is "
        "mostly about noticing what other people overlook.",
        "NOVA{osint_is_just_reading_closely}",
        ["The 'Profile Notes' field isn't plain text."],
        [("dossier.txt", "osint/dossier.txt")],
    ),
    (
        "OSINT",
        "EXIF Breadcrumbs",
        Challenge.DIFFICULTY_MEDIUM,
        250,
        "Photos carry more than pixels. This synthetic metadata dump (no real photo attached) includes a "
        "Comment field most people never check.",
        "NOVA{metadata_tells_a_story}",
        ["The Comment field is hex — decode it to ASCII."],
        [("photo_metadata.txt", "osint/photo_metadata.txt")],
    ),
    (
        "Reverse Engineering",
        "Baby's First Disassembly",
        Challenge.DIFFICULTY_EASY,
        100,
        "A tiny license checker compares your input against a hardcoded list of numbers using a simple "
        "transformation. Read the source, figure out the transform, and work backwards to the valid input.",
        "NOVA{reversing_is_just_reading}",
        ["The check is `ord(c) ^ KEY == expected`. XOR is its own inverse."],
        [("checker.py", "reverse-engineering/checker.py")],
    ),
    (
        "Reverse Engineering",
        "Stack Machine",
        Challenge.DIFFICULTY_HARD,
        500,
        "A custom stack VM encoded a flag byte-by-byte. We have the documented transform and the captured "
        "output — but not the original binary. Reverse the math to recover the input.",
        "NOVA{virtual_machines_hide_secrets}",
        [
            "Undo the operations in reverse order: subtract before you XOR.",
            "Writing a 5-line Python script beats doing 34 bytes by hand.",
        ],
        [("stackvm.txt", "reverse-engineering/stackvm.txt")],
    ),
    (
        "Miscellaneous",
        "Warm Up",
        Challenge.DIFFICULTY_EASY,
        100,
        "Every challenge submits the same way. Here's a gentle warm-up to make sure your workflow works.",
        "NOVA{welcome_to_the_network}",
        ["This encoding uses the characters A-Z, a-z, 0-9, +, / and sometimes trailing ="],
        [("warmup.txt", "miscellaneous/warmup.txt")],
    ),
    (
        "Miscellaneous",
        "Binary Breakfast",
        Challenge.DIFFICULTY_MEDIUM,
        250,
        "The flag was left in its most fundamental form: 1s and 0s.",
        "NOVA{binary_is_base_two}",
        ["Each 8-bit group is one ASCII character."],
        [("binary_breakfast.txt", "miscellaneous/binary_breakfast.txt")],
    ),
]


class Command(BaseCommand):
    help = "Idempotently creates the 12 starter NOVA CTF 2026 challenges (safe to re-run)."

    def add_arguments(self, parser):
        parser.add_argument("--competition-slug", default="nova-ctf-2026")

    def handle(self, *args, **options):
        try:
            competition = Competition.objects.get(slug=options["competition_slug"])
        except Competition.DoesNotExist:
            raise CommandError(
                f"No competition with slug '{options['competition_slug']}'. Run `seed_competition` first."
            )

        created_count = 0
        for order, (cat_name, title, difficulty, points, description, flag, hints, attachments) in enumerate(
            STARTER_CHALLENGES
        ):
            try:
                category = ChallengeCategory.objects.get(name=cat_name)
            except ChallengeCategory.DoesNotExist:
                raise CommandError(f"Category '{cat_name}' not found. Run `seed_competition` first.")

            challenge, created = Challenge.objects.get_or_create(
                competition=competition,
                category=category,
                title=title,
                defaults={
                    "description": description,
                    "difficulty": difficulty,
                    "points": points,
                    "is_published": True,
                    "order": order,
                    "author": "NOVA Cyber Network organizers",
                },
            )
            if created:
                challenge.set_flag(flag)
                challenge.save()
                for hint_order, hint_text in enumerate(hints):
                    challenge.hints.create(order=hint_order, text=hint_text)
                for display_name, relative_path in attachments:
                    ChallengeAttachment.objects.create(
                        challenge=challenge, display_name=display_name, relative_path=relative_path
                    )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Ensured {len(STARTER_CHALLENGES)} starter challenges ({created_count} newly created).")
        )
