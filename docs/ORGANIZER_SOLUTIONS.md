# Organizer-only solutions — NOVA CTF 2026 starter set

**Do not share this file or its contents with participants.** It exists for organizers to verify
challenges, write support/hint scripts, and debug participant questions during the event.

All 12 flags below are verified against `challenges/management/commands/seed_challenges.py`
(the source of truth — if you edit a challenge's flag in Django Admin, update this file too) and
covered by an automated check in `python manage.py test` indirectly via the scoring service tests.

| # | Category | Title | Difficulty | Points | Flag |
|---|---|---|---|---|---|
| 1 | Web Security | Robots Only | Easy | 100 | `NOVA{robots_dot_txt_isnt_a_secret}` |
| 2 | Web Security | Cookie Jar | Medium | 250 | `NOVA{c00ki3s_lie_about_trust}` |
| 3 | Cryptography | Caesar's Welcome | Easy | 100 | `NOVA{caesar_says_hi}` |
| 4 | Cryptography | XOR Marks the Spot | Medium | 250 | `NOVA{xor_keys_are_fun}` |
| 5 | Digital Forensics | Metadata Doesn't Lie | Easy | 100 | `NOVA{strings_find_what_grep_misses}` |
| 6 | Digital Forensics | The Deleted Log | Medium | 250 | `NOVA{logs_never_really_disappear}` |
| 7 | OSINT | Profile Recon | Easy | 100 | `NOVA{osint_is_just_reading_closely}` |
| 8 | OSINT | EXIF Breadcrumbs | Medium | 250 | `NOVA{metadata_tells_a_story}` |
| 9 | Reverse Engineering | Baby's First Disassembly | Easy | 100 | `NOVA{reversing_is_just_reading}` |
| 10 | Reverse Engineering | Stack Machine | Hard | 500 | `NOVA{virtual_machines_hide_secrets}` |
| 11 | Miscellaneous | Warm Up | Easy | 100 | `NOVA{welcome_to_the_network}` |
| 12 | Miscellaneous | Binary Breakfast | Medium | 250 | `NOVA{binary_is_base_two}` |

## Solution notes

1. **Robots Only** — download `robots.txt`, note the `Disallow: /internal/status-9f21.html` line,
   download that file too, read the HTML comment.
2. **Cookie Jar** — base64-decode the `Set-Cookie` value to get JSON with a `flag_hex` field;
   hex-decode that field.
3. **Caesar's Welcome** — ROT13 the ciphertext (`ABIN{pnrfne_fnlf_uv}` → the flag). Any Caesar
   brute-forcer (shift 0–25) also finds it.
4. **XOR Marks the Spot** — ciphertext[0] (`0x0c`) XOR `'N'` (`0x4e`) = `0x42`, the key. XOR every
   ciphertext byte with `0x42`.
5. **Metadata Doesn't Lie** — `grep NOVA firmware_strings.txt` (or just read the file).
6. **The Deleted Log** — scan the `user_agent` column for a base64-looking token; it's embedded in
   the `ReportBot/1.0 (+...)` row. Base64-decode it.
7. **Profile Recon** — base64-decode the "Profile Notes" field.
8. **EXIF Breadcrumbs** — hex-decode the `Comment` field.
9. **Baby's First Disassembly** — `EXPECTED[i] == ord(c) ^ 0x1A`, so `c = chr(EXPECTED[i] ^ 0x1A)`
   for each index.
10. **Stack Machine** — reverse `b = ((c XOR 0x37) + 5) mod 256`: for each byte, `v = (b - 5) mod
    256`, then `c = v XOR 0x37`.
11. **Warm Up** — plain base64-decode.
12. **Binary Breakfast** — split into 8-bit groups, convert each to its ASCII character.

## Verifying all flags at once

```bash
python manage.py shell -c "
from challenges.models import Challenge
for c in Challenge.objects.all():
    print(c.title, '->', c.check_flag(input(f'flag for {c.title}: ')))
"
```

Or non-interactively, adapt `challenges/tests.py::FlagSubmissionTests` as a template — it exercises
`Challenge.check_flag()` directly against known-good and known-bad inputs.
