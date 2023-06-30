from unittest import skip

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm
from lists.forms import (
    ItemForm, EMPTY_ITEM_ERROR,
    ExistingListItemForm, DUPLICATE_ITEM_ERROR)

# Create your tests here.

def write_log(res):
    with open('log.txt', 'w') as file:
        file.write(str(res))



class HomePageTest(TestCase):
    """ test home page """


    def test_home_page_returns_correct_html(self):
        """ тест: домашняя страница возращает правильный html"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_home_page_uses_item_form(self):
        """тест: домашняя страница использует форму для элемента"""
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class ListViewTest(TestCase):
    """тест представления списка"""

    def test_uses_list_template(self):
        """тест: используется шаблон списка"""
        #response = self.client.get("/lists/uniq-url-for-lists/")
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_only_for_that_list(self):
        """тест: отображаются все элементы списка"""
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='другой элемент 1 списка', list=other_list)
        Item.objects.create(text='другой элемент 2 списка', list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, 'другой элемент 1 списка')
        self.assertNotContains(response, 'другой элемент 2 списка')


    def test_can_save_a_POST_request_to_an_existing_list(self):
        """тест: можно сохранить post-запрос в сущ. список"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_POST_redirects_to_list_view(self):
        """тест: post-запрос переадресуется в представление списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def post_invalid_input(self):
        """отправляет не допустимый ввод"""
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )


    def test_for_invalid_input_nothing_saved_to_db(self):
        """тест: на недопустимый ввод -- ничего не сохраняется в БД"""
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)


    def test_for_invalid_input_renders_list_template(self):
        """тест: на недопустимый ввод -- отображается шаблон списка"""
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')


    def test_for_invalid_input_passes_form_to_template(self):
        """тест: на недопустимый ввод -- форма передается в шаблон"""
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)


    def test_for_invalid_input_shows_error_on_page(self):
        """тест: на недопустимый ввод -- на странице показывается ошибка"""
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))


    def test_dublicate_item_validation_errors_end_up_on_lists_page(self):
        """тест: ошибки валидации повторяющегося элемента
           оканчиваются на странице списков"""
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'textey'}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)

    def test_displays_item_form(self):
        """тест: отображения формы для элемента"""
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, "text")




class NewListTest(TestCase):
    """тест нового списка"""


    def test_can_save_a_POST_request(self):
        """тест: можно сохранить новый список"""
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        """тест: переадресация после post-запроса"""
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


    def test_invalid_list_items_arent_saved(self):
        """тест: сохраняются недопустимые элементы списка"""
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


    def test_for_invalid_input_renders_home_template(self):
        """тест: ошибки валидации отсылают назад в шаблон дом.страницы"""
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    def test_validation_errors_are_shown_on_home_page(self):
        '''тест: ошибки валидации выводятся на домашней странице'''
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))


    def test_for_invalid_input_passes_form_to_template(self):
        """тест: на недопустимый ввод -- форма передается в шаблон"""
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)
        
