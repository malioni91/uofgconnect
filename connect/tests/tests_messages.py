from django.test import TestCase
from django.core.urlresolvers import reverse

from populate_connect import populate

class MessagesPageTests(TestCase):
   """Messages page test cases """
   fixtures = ['connect/fixtures/Courses.json',]
   def setUp(self):
       try:
           populate()
       except ImportError:
           print('The module populate_rango does not exist')
       except NameError:
           print('The function populate() does not exist or is not correct')

           print('Something went wrong in the populate() function :-(')
       # login is required
       self.client.login(username='anakin', password='pavlos')

   def test_messages_using_template(self):
        response = self.client.get(reverse('messages'))
        self.assertTemplateUsed(response, 'connect/messages.html')

