from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page

class HomePAgeTest(TestCase):
    def test_homepage_return_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")
    
    def test_can_save_POST_req(self):
        response = self.client.post("/", data={"item_text":"A new list item"})
        self.assertContains(response, "A new list item")
        self.assertTemplateUsed(response, "home.html")