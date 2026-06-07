from django.test import TestCase
from django.urls import reverse


class BlogViewsTest(TestCase):
    def test_article_list_status(self):
        response = self.client.get(reverse("blog:article_list"))
        self.assertEqual(response.status_code, 200)

    def test_article_list_uses_correct_template(self):
        response = self.client.get(reverse("blog:article_list"))
        self.assertTemplateUsed(response, "blog/article_list.html")
