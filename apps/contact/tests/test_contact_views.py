from django.test import TestCase
from django.urls import reverse


class ContactViewsTest(TestCase):
    def test_contact_page_status(self):
        response = self.client.get(reverse("contact:contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_uses_correct_template(self):
        response = self.client.get(reverse("contact:contact"))
        self.assertTemplateUsed(response, "contact/contact.html")
