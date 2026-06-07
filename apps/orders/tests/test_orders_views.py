from django.test import TestCase
from django.urls import reverse


class OrdersViewsTest(TestCase):
    def test_checkout_page_status(self):
        response = self.client.get(reverse("orders:checkout"))
        self.assertEqual(response.status_code, 200)
