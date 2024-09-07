from django.test import TestCase
from lists.models import Item

class HomePageTest(TestCase):
    def test_homepage_return_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")
    
    def test_can_save_POST_req(self):
        response = self.client.post("/", data={"item_text":"A new list item"})
        self.assertContains(response, "A new list item")
        self.assertTemplateUsed(response, "home.html")

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "the first (ever) list Item"
        first_item.save()
        
        second_item = Item()
        second_item.text = "the second list Item"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, "the first (ever) list Item")
        self.assertEqual(second_saved_item.text, "the second list Item")
    