import json

from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_endpoint_returns_ok(self):
        response = self.client.get(reverse("core:health"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["status"], "ok")


class HomePageTests(TestCase):
    def test_home_page_renders_without_fabricated_stats(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["stats"]["teams"], 0)
        self.assertEqual(response.context["stats"]["solves"], 0)

    def test_rules_page_renders(self):
        response = self.client.get(reverse("core:rules"))
        self.assertEqual(response.status_code, 200)
