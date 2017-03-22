from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse

from connect.models import UserProfile, Map

class AboutPageTests(TestCase):
   """About page test cases """

   def test_about_using_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'connect/about.html')

