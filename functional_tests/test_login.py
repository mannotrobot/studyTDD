from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re


from .base import FunctionalTest


TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    """тест регистрации в системе"""
    def test_can_get_email_link_to_log_in(self):
        """тест: можно получить ссылку по почте для регистрации"""
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        # появляется сообщение, что пиьсмо отправлено
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element(By.TAG_NAME, 'body').text
        ))

        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # в письме ссылка на url-adress
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # переход по ссылку
        self.browser.get(url)

        # регестрация в системе
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Log out')
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)
        
