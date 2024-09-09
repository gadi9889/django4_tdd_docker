from django.test import TestCase
from lists.models import Item, List

class HomePageTest(TestCase):
    def test_uses_home_temp(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

class NewListTest(TestCase):
    def test_can_save_POST_req(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/add_item", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")
        self.assertEqual(new_item.list, correct_list)
    
    def test_redirects_after_POST(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f"/lists/{correct_list.id}/add_item", data={"item_text":"A new list item"})
        self.assertRedirects(response, f"/lists/{correct_list.id}/")

class ListViewTest(TestCase):
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)
    
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self):
        correct_list = List.objects.create()
        Item.objects.create(text="item 1", list=correct_list)
        Item.objects.create(text="item 2", list=correct_list)

        other_list = List.objects.create()

        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")
        self.assertNotContains(response, "other list item")

class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        mylist = List()
        mylist.save()

        first_item = Item()
        first_item.text = "the first (ever) list Item"
        first_item.list = mylist
        first_item.save()
        
        second_item = Item()
        second_item.text = "the second list Item"
        second_item.list = mylist
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, mylist)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, "the first (ever) list Item")
        self.assertEqual(second_saved_item.text, "the second list Item")
        self.assertEqual(first_saved_item.list, mylist)
        self.assertEqual(second_saved_item.list, mylist)
