from django.urls import resolve
from django.test import TestCase
from lists.views import home_page

# Create your tests here.

class HomePageTest(TestCase):
    """ test home page """
    def test_root_url_resolves_to_home_page_view(self):
        """ тест: корневой url преобразуется во вьюшку дом
            страницы """
        found = resolve('/')
        self.assertEqual(found.func, home_page)
