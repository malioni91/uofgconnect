from django.test import TestCase
from django.core.urlresolvers import reverse

from populate_script import populate

class LoginTests(TestCase):
   """Login page test cases"""
   fixtures = ['connect/fixtures/Courses.json',]

   def setUp(self):
       try:
           populate()
       except ImportError:
           print('The module populate_script does not exist')
       except NameError:
           print('The function populate() does not exist or is not correct')
       except Exception as e :
           print('Something went wrong in the populate() function')

   def test_login_using_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'connect/login.html')

   def test_login(self):
        login = self.client.login(username='anakin', password='pavlos')
        self.assertTrue(login)
