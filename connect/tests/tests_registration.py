from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse

from connect.models import UserProfile, Map
from populate_script import populate

class RegistrationTests(TestCase):
    fixtures = ['connect/fixtures/Courses.json',]

    def setUp(self):
        try:
            populate()
        except ImportError:
            print('The module populate_script does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except Exception as e :
            print('Something went wrong in the populate() function :-(')

    def get_user(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        return user

    def get_user_profile(self, username):
        try:
            user = self.get_user(username)
            user = UserProfile.objects.get(user=user)
        except User.DoesNotExist:
            user = None
        return user

    def test_user_added(self):
        user = self.get_user('anakin')
        self.assertIsNotNone(user)

    def test_map_coordinates_added(self):
        user = self.get_user_profile('anakin')
        # the coordinates are returned as a Decimal object,
        # so they need to be converted into strings
        self.assertEquals(str(user.location.latitude), "55.87356")
        self.assertEquals(str(user.location.longitude), "-4.28885")

    def test_courses_added(self):
        user = self.get_user_profile('anakin')
        self.assertEquals(user.course.id, 7)

