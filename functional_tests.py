from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    """тест нового посетителя"""

    def setUp(self):
        """установка"""
        self.browser = webdriver.Firefox()



    def tearDown(self):
        """демонтаж"""
        self.browser.quit()



    def test_can_start_a_list_and_retieve_it_later(self):
        """тест: можно начать список и получить его позже"""
        # Эдит слышала про крутое новое онлайн-приложение со списком
        # неотложных дел.

        self.browser.get("http://localhost:8000")
        # title страницы равен 'To-Do'
        self.assertIn('To-Do', self.browser.title)


        # Сразу видно текстовое поле
        # Набор текста в текстовом поле
        # Принажатие enter, страница обновляется
        # Теперь страница содержит : "1. Buy pies" - в качестве элемента списка
        # Текстовое поле по прежнему приглашает добавить еще один элемент.
        # Новая задача -> enter -> Теперь два элемента в списке
        # Генерация уникального url ->  список дел, сохранен.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
