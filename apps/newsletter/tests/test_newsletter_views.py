from django.test import TestCase
from django.urls import reverse


class NewsletterViewsTest(TestCase):
    def test_subscribe_page_status(self):
        response = self.client.get(reverse("newsletter:subscribe"))
        self.assertEqual(response.status_code, 200)

    def test_subscribe_uses_correct_template(self):
        response = self.client.get(reverse("newsletter:subscribe"))
        self.assertTemplateUsed(response, "newsletter/subscribe.html")
