from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page

class HomePAgeTest(TestCase):
    def test_homepage_return_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")