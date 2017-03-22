from django.test import TestCase
from django.core.urlresolvers import reverse

class AboutPageTests(TestCase):
   """About page test cases """

   def test_about_using_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'connect/about.html')

