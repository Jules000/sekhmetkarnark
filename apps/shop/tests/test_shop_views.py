from django.test import TestCase
from django.urls import reverse


class ShopViewsTest(TestCase):
    def test_product_list_status(self):
        response = self.client.get(reverse("shop:product_list"))
        self.assertEqual(response.status_code, 200)

    def test_product_list_uses_correct_template(self):
        response = self.client.get(reverse("shop:product_list"))
        self.assertTemplateUsed(response, "shop/product_list.html")
