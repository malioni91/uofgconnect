from django.test import TestCase
from django.contrib.staticfiles import finders

class GeneralTests(TestCase):
    """General page test cases"""

    def test_static_files(self):
        result = finders.find("css/main.css")
        self.assertIsNotNone(result)

