from django.test import TestCase
from django.urls import reverse


class AccountsViewsTest(TestCase):
    def test_login_page_status(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_register_page_status(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_page_status(self):
        response = self.client.get(reverse("accounts:forgot_password"))
        self.assertEqual(response.status_code, 200)

    def test_otp_verify_page_status(self):
        response = self.client.get(reverse("accounts:otp_verify"))
        self.assertEqual(response.status_code, 200)

    def test_login_uses_correct_template(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertTemplateUsed(response, "accounts/login.html")
