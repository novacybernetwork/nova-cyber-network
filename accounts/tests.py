from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ApprovedMember, Profile, School


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="player1", password="StrongPass123!")

    def test_login_with_correct_credentials_succeeds(self):
        ok = self.client.login(username="player1", password="StrongPass123!")
        self.assertTrue(ok)

    def test_login_with_wrong_password_fails(self):
        ok = self.client.login(username="player1", password="wrong-password")
        self.assertFalse(ok)

    def test_login_page_renders(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_requires_post(self):
        self.client.login(username="player1", password="StrongPass123!")
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 405)
        response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_profile_auto_created_for_new_user(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        self.assertFalse(self.user.profile.is_approved)

    def test_superuser_profile_is_auto_approved(self):
        admin = User.objects.create_superuser(username="root", email="root@example.org", password="RootPass123!")
        self.assertTrue(admin.profile.is_approved)


class MembershipApprovalTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name="John Champe High School")
        self.member = ApprovedMember.objects.create(
            name="Taylor Rivera", email="taylor@example.org", school=self.school
        )

    def test_claim_page_loads_for_valid_unclaimed_token(self):
        response = self.client.get(reverse("accounts:claim_invite", args=[self.member.invite_token]))
        self.assertEqual(response.status_code, 200)

    def test_claim_creates_approved_account(self):
        url = reverse("accounts:claim_invite", args=[self.member.invite_token])
        response = self.client.post(
            url, {"username": "taylorr", "password1": "ClaimMe123!", "password2": "ClaimMe123!"}
        )
        self.assertEqual(response.status_code, 302)
        self.member.refresh_from_db()
        self.assertTrue(self.member.is_claimed)
        user = User.objects.get(username="taylorr")
        self.assertEqual(self.member.claimed_by, user)
        self.assertTrue(user.profile.is_approved)
        self.assertEqual(user.profile.display_name, "Taylor Rivera")

    def test_claim_link_cannot_be_reused(self):
        url = reverse("accounts:claim_invite", args=[self.member.invite_token])
        self.client.post(url, {"username": "taylorr", "password1": "ClaimMe123!", "password2": "ClaimMe123!"})
        self.client.logout()
        response = self.client.get(url)
        self.assertRedirects(response, reverse("accounts:login"))

    def test_unapproved_roster_member_cannot_claim_without_review(self):
        pending = ApprovedMember.objects.create(
            name="No One Yet", email="pending@example.org", pending_review=True
        )
        response = self.client.get(reverse("accounts:claim_invite", args=[pending.invite_token]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pending")

    def test_request_access_creates_pending_approved_member(self):
        response = self.client.post(
            reverse("accounts:request_access"),
            {"name": "New Student", "email": "new.student@example.org", "school_other": "Freedom High School"},
        )
        self.assertEqual(response.status_code, 302)
        member = ApprovedMember.objects.get(email="new.student@example.org")
        self.assertTrue(member.pending_review)
        self.assertFalse(member.is_claimed)

    def test_request_access_blocks_duplicate_email(self):
        self.client.post(
            reverse("accounts:request_access"),
            {"name": "Dup", "email": self.member.email, "school_other": ""},
        )
        self.assertEqual(ApprovedMember.objects.filter(email=self.member.email).count(), 1)


class UnauthorizedAdminAccessTests(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(username="regular", password="RegularPass123!")
        self.staff_user = User.objects.create_user(
            username="organizer", password="OrganizerPass123!", is_staff=True
        )

    def test_anonymous_cannot_reach_admin_overview(self):
        response = self.client.get(reverse("core:admin_overview"))
        self.assertEqual(response.status_code, 302)

    def test_regular_user_cannot_reach_admin_overview(self):
        self.client.login(username="regular", password="RegularPass123!")
        response = self.client.get(reverse("core:admin_overview"))
        self.assertEqual(response.status_code, 302)

    def test_staff_user_can_reach_admin_overview(self):
        self.client.login(username="organizer", password="OrganizerPass123!")
        response = self.client.get(reverse("core:admin_overview"))
        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_reach_django_admin(self):
        self.client.login(username="regular", password="RegularPass123!")
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)

    def test_regular_user_cannot_export_results(self):
        self.client.login(username="regular", password="RegularPass123!")
        response = self.client.get(reverse("core:admin_export_results"))
        self.assertEqual(response.status_code, 302)


class ClaimLinkExportTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="organizer", password="OrganizerPass123!", is_staff=True, is_superuser=True
        )
        self.member = ApprovedMember.objects.create(name="Jordan Lee", email="jordan@example.org")

    def test_export_action_returns_csv_with_absolute_claim_link(self):
        self.client.login(username="organizer", password="OrganizerPass123!")
        response = self.client.post(
            "/admin/accounts/approvedmember/",
            {"action": "export_claim_links", "_selected_action": [self.member.pk]},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        body = b"".join(response.streaming_content).decode() if response.streaming else response.content.decode()
        self.assertIn("Jordan Lee", body)
        self.assertIn("jordan@example.org", body)
        self.assertIn(f"/accounts/claim/{self.member.invite_token}/", body)
        # Built from an absolute URL, not just the bare path.
        self.assertIn("http://testserver/accounts/claim/", body)

    def test_regular_user_cannot_export_claim_links(self):
        regular = User.objects.create_user(username="regular2", password="RegularPass123!")
        self.client.login(username="regular2", password="RegularPass123!")
        response = self.client.post(
            "/admin/accounts/approvedmember/",
            {"action": "export_claim_links", "_selected_action": [self.member.pk]},
        )
        self.assertNotEqual(response.status_code, 200)
