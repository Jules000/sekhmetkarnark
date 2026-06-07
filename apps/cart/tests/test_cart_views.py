from django.test import TestCase
from django.urls import reverse


class CartViewsTest(TestCase):
    def test_cart_detail_status(self):
        response = self.client.get(reverse("cart:cart_detail"))
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_uses_correct_template(self):
        response = self.client.get(reverse("cart:cart_detail"))
        self.assertTemplateUsed(response, "cart/cart_detail.html")
