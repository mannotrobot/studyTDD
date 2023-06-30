from django.test import TestCase
from lists.models import Item, List
from lists.forms import (
    EMPTY_ITEM_ERROR, ItemForm,
    DUPLICATE_ITEM_ERROR, ExistingListItemForm)



class ExistingListItemFormTest(TestCase):
    """тест формы для элемента"""


    def test_form_renders_item_text_input(self):
        """тест: форма отображает текстовое поле ввода"""
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())


    def test_form_validation_for_blank_items(self):
        """тест: валидации формы для пустых элементов"""
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )


    def test_form_validation_for_duplicate_items(self):
        """тест: валидации формы для повторных элементов"""
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])


    def test_form_save(self):
        """тест: сохранение формы"""
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': "hi"})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
