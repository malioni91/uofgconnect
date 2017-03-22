# UofG Connect


UofG Connect’s primary objective is to help students find their friends’ location
  around the campus and provide an intuitive interface to keep them in touch.
  Students can register only through their university e-mail address and once logged in,
  they can search for their friends that are UofG users.
  The app will then display the friends’ locations on the map
  and allow the user to send a message to their friends.

### Authors

* Pavlos Ratis

* Nikolaos Theodosis

* Anastasis Agathokleous

* Malion Hoxhallari

### Demo Site
[http://victoriancode.pythonanywhere.com/](http://victoriancode.pythonanywhere.com/)

Please browse the above link from **Mozilla Firefox**. The Google Map Geolocation API does not work from Google Chrome if the app is not hosted on a secure site.
For more information on the issue, please consult the [link](https://sites.google.com/a/chromium.org/dev/Home/chromium-security/deprecating-powerful-features-on-insecure-origins)

### Demo Credentials

Please enter the following credentials if you want to take a quick look into the app without registering:

    username: john
    password: smith

This project template creates a Django 1.9/1.10 project with a base set of applications.


### Installation Process

If you want to test the app in your local machine please do the following:

Clone the repository:

    git clone https://github.com/uofgconnect/uofgconnect.git

Install all python prerequisites:

    pip install -r requirements.txt

Navigate to the folder uofgconnect, and once there run:

    python manage.py makemigrations

Run the following to migrate the data:

    python manage.py migrate

In order to load all the course titles please run:

    python manage.py loaddata Courses

In order to run the tests:
    python manage.py test connect.test

In order to populate new users:  
    python populate_connect.py
