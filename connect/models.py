from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


class Map(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=5)

class Course(models.Model):
    course_name = models.CharField(max_length=30)

    def __str__(self):
        return self.course_name

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.OneToOneField(Course)

    def __str__(self):
        return self.course_name