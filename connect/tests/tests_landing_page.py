from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse

from connect.models import UserProfile, Map

class LandingPageTests(TestCase):
    """Landing page test cases"""

    def test_landing_page_contains_info_message(self):
        response = self.client.get(reverse('landing'))
        self.assertIn(b'primary objective', response.content)

    def test_landing_page_using_template(self):
        response = self.client.get(reverse('landing'))
        self.assertTemplateUsed(response, 'connect/landing.html')

    def test_landing_page_has_title(self):
	response = self.client.get(reverse('landing'))
        self.assertIn(b'<title>UofG Connect</title>', response.content)

