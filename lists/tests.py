from django.test import TestCase
from lists.models import Item

class HomePageTest(TestCase):
    def test_uses_home_temp(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

class NewListTest(TestCase):
    def test_can_save_POST_req(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")
    
    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text":"A new list item"})
        self.assertRedirects(response, "/lists/only-list/")

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/only-list/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self):
        Item.objects.create(text="item 1")
        Item.objects.create(text="item 2")

        response = self.client.get("/lists/only-list/")

        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")

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
