import time
import unittest

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """тест нового посетителя"""

    def setUp(self):
        """установка"""
        self.browser = webdriver.Firefox()



    def tearDown(self):
        """демонтаж"""
        self.browser.quit()


    def wait_for_row_in_list_table(self, row_text):
        """ожидать строку в таблице списка"""
        start_time = time.time()

        while True:

            try:
                table = self.browser.find_element(by=By.ID, value='id_list_table')
                rows = table.find_elements(by=By.TAG_NAME, value='tr')
                self.assertIn(row_text, [row.text for row in rows])
                return

            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_and_retieve_it_later(self):
        """тест: можно начать список и получить его позже"""
        # Эдит слышала про крутое новое онлайн-приложение со списком
        # неотложных дел.

        self.browser.get(self.live_server_url)
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
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Текстовое поле по прежнему приглашает добавить еще один элемент.
        inputbox = self.browser.find_element(By.ID, 'id_new_item')


        # Вводить новую задачу 'Сделать мушку из павлиньих перьев'
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)


        # страница снова обновляется и показывает два элемента
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')


    def test_multiple_users_can_start_lists_at_different_urls(self):
        """ тест: разные пользователи разные url для списков"""
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Генерация уникального url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Новый пользователь | закрываем старую сессию  -- запускаем новую
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Создаем новый список дел
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # получаем уникальный url для списка
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)


        # проверка что списки не перемешались
        page_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

#        self.fail("ЗАКОНЧИТЬ ТЕСТ")


