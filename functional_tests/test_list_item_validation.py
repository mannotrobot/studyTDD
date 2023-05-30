from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest



class ItemValidationTest(FunctionalTest):
    """тест валидации элемента списка"""
    @skip
    def test_cannot_add_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""
        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.ID, value='id_new_item').send_keys(Keys.Enter)
        
        
        # домашная страница обновляется, появляется сообщение об ошибке,
        # которое говорит, что элементы спсика не должны быть пустыми
        self.assertEqual(
            self.browser.find_element('.has_error').text,
            "You cant't have an empty list item"
        )   
        
        # новая попытка с неким текстом для элемента, и теперь все ок.
        self.fail("Закончить текст!")

        # Домашняя страница обновляется, и появляется сообщение об ошибке,
        # которое говорит, что элементы списка не должны быть пустыми
        self.wait_for(lambda: self.assertEqual( 
        self.browser.find_element_by_css_selector('.has-error').text,
        "You can't have an empty list item"))
