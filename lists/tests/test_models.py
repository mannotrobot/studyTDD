from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List

# Create your tests here.
class ItemModelTest(TestCase):
    """тест представления элемента списка"""

    def test_default_text(self):
        """тест: заданного по умолчанию текста"""
        item = Item()
        self.assertEqual(item.text, '')


    def test_item_is_related_to_list(self):
        """тест: элемент связан со списком"""
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()




class ListModelTest(TestCase):
    """тест представления списка"""

    def test_get_absolute_url(self):
        """тест: получен абсолютный url"""
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')


    def test_duplicate_items_are_invalid(self):
        """тест: повторы элементов не допустимы"""
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='da-da')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='da-da')
            item.full_clean()


    def test_CAN_save_same_item_to_different_lists(self):
        """тест: МОЖЕТ сохранить тот же элемент в разные списки"""
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='da-da')
        item = Item(list=list2, text='da-da')
        item.full_clean()


    def test_list_ordering(self):
        """тест: элементы списка идут по порядку добавления"""
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='one')
        item2 = Item.objects.create(list=list1, text='two')
        item3 = Item.objects.create(list=list1, text='three')
        self.assertEqual(
            list(Item.objects.all()), [item1, item2, item3]
        )


    def test_string_representation(self):
        """тест: тест строкого представления"""
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
