import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uofgconnect.settings')

import django
django.setup()

from connect.models import UserProfile, Course, Map
from django.contrib.auth.models import User

def populate():
    maps = [ {
        "latitude": "55.87356",
        "longitude": "-4.28885"
        }, {
        "latitude": "55.87252",
        "longitude": "-4.28153"} ]

    courses = [{
        "course": Course.objects.get(id=7)
        }, {
        "course":  Course.objects.get(id=15)
        }]


    users = [{
        "password": "pbkdf2_sha256$30000$V5fTmm30eA25$UsNd22UTI2YYBpbHnPbcorOworBH95Ly8WWb6pTDG4k=",
        "last_login": "2017-03-20T20:07:48.329Z",
        "is_superuser": True,
        "username": "anakin",
        "first_name": "Darth",
        "last_name": "Vader",
        "email": "2286121R@student.gla.ac.uk",
        }, {
        "password": "pbkdf2_sha256$30000$NTXfemSRMy53$H66xl+MUNA2562P3LY6GjdYlJAgDkr6qH7pus9Y2TQg=",
        "last_login": "2017-03-20T20:06:27.666Z",
        "is_superuser": False,
        "username": "rick",
        "first_name": "Rick",
        "last_name": "Grimes",
        "email": "2272891T@student.gla.ac.uk",
	}]

    for index, user_data in enumerate(users):
        user = add_user(user_data)
        user_profile = add_user_profile(user=user, course=courses[index]["course"])
        add_coordinates(user_profile, maps[index])

#def add_user(password, last_login, username, first_name, last_name, email):
#    user = User.object.get_or_create(**users)
#    return user
def add_user(user_data):
    user = User.objects.get_or_create(**user_data)[0]
    user.save()
    return user

def add_user_profile(user, course):
    user_profile = UserProfile.objects.get_or_create(user=user, course=course)[0]
    return user_profile

def add_coordinates(user, coordinates):
    Map.objects.create(**coordinates)
    map_info = Map.objects.get(id=user.user_id)
    user.location = map_info
    return user.save()

if __name__ == '__main__':
    print("Populating data to the database..")
    populate()
