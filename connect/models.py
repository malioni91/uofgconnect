from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


class Map(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=5)

class Course(models.Model):
    course = models.CharField(max_length=60)

    def __str__(self):
        return self.course

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.OneToOneField(Course)
    location = models.OneToOneField(Map, null=True)

    def __str__(self):
        return self.user.username
