import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    """тест нового посетителя"""

    def setUp(self):
        """установка"""
        self.browser = webdriver.Firefox()



    def tearDown(self):
        """демонтаж"""
        self.browser.quit()


    def check_for_row_in_list_table(self, row_text):
        """подверждения строки в таблице списка"""
        table = self.browser.find_element(by=By.ID, value='id_list_table')
        rows = table.find_elements(by=By.TAG_NAME, value='tr')
        self.assertIn(row_text, [row.text for row in rows])



    def test_can_start_a_list_and_retieve_it_later(self):
        """тест: можно начать список и получить его позже"""
        # Эдит слышала про крутое новое онлайн-приложение со списком
        # неотложных дел.

        self.browser.get("http://localhost:8000")
        # title страницы равен 'To-Do'
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn('To-Do', header_text)

        # Сразу видно текстовое поле
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Набор текста в текстовом поле
        inputbox.send_keys('Купить павлиньи перья')
        # Принажатие enter, страница обновляется
        # Теперь страница содержит : "1. Buy pies" - в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Купить павлиньи перья')

        # Текстовое поле по прежнему приглашает добавить еще один элемент.
        inputbox = self.browser.find_element(By.ID, 'id_new_item')

        # Вводить новую задачу 'Сделать мушку из павлиньих перьев'
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # страница снова обновляется и показывает два элемента
        self.check_for_row_in_list_table('1: Купить павлиньи перья')
        self.check_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')
        # Генерация уникального url ->  список дел, сохранен.


        self.fail("ЗАКОНЧИТЬ ТЕСТ")



if __name__ == '__main__':
    unittest.main(warnings='ignore')
