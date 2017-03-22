from django.test import TestCase
from django.core.urlresolvers import reverse

from populate_script import populate

class IndexPageTests(TestCase):
    """Index page test cases"""
    fixtures = ['connect/fixtures/Courses.json',]

    def setUp(self):
       try:
           populate()
       except ImportError:
           print('The module populate_script does not exist')
       except NameError:
           print('The function populate() does not exist or is not correct')

           print('Something went wrong in the populate() function.')
       # login is required
       self.client.login(username='anakin', password='itech')


    def test_index_using_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'connect/index.html')

    def test_index_page_contains_info_message(self):
        response = self.client.get(reverse('index'))
        self.assertIn(b'Available Users', response.content)

    def test_sidebar_displayed(self):
        response = self.client.get(reverse('index'))
        self.assertIn(b'<div id="sidebar-wrapper">', response.content)
