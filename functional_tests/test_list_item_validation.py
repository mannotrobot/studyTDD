from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from unittest import skip
from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):
    """тест валидации элемента списка"""

    def test_cannot_add_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)


        # Домашняя страница обновляется, и появляется сообщение об ошибке,
        # которое говорит, что элементы списка не должны быть пустыми
        self.wait_for(lambda: self.browser.find_element(
            By.CSS_SELECTOR, '#id_text:invalid'))

        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element(
            By.CSS_SELECTOR, '#id_text:valid'))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')


        # повторная попытка отправить пустой элемент списка
        self.get_item_input_box().send_keys(Keys.ENTER)


        # повторное предупреждение на странице списка
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))


        # отправка корректных данных
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')


    def test_cannot_add_duplicate_items(self):
        """тест: нельзя добавлять повторяющиеся элементы"""
        # открываем дом. страницу т начтнается новый список
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')


        #попытка добавить повторяющий элемент
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)


        #появление сообщения об ошибки
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
            "You've already got this in your list"
        ))

