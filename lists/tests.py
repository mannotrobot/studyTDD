from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

# Create your tests here.

class HomePageTest(TestCase):
    """ test home page """


    def test_home_page_returns_correct_html(self):
        """ тест: домашняя страница возращает правильный html"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')



class ItemModelTest(TestCase):
    """тест модели элемента списка"""


    def test_saving_and_retrieving_items(self):
        """тест сохранение и получение элемента списка"""
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')



class ListViewTest(TestCase):
    """тест представления списка"""

    def test_uses_list_template(self):
        """тест: используется шаблон списка"""
        response = self.client.get("/lists/uniq-url-for-lists/")
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_all_items(self):
        """тест: отображаются все элементы списка"""
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get("/lists/uniq-url-for-lists/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

class NewListTest(TestCase):
    """тест нового списка"""


    def test_can_save_a_POST_request(self):
        """тест: можно сохранить новый список"""
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        """тест: переадресация после post-запроса"""
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/uniq-url-for-lists/')



