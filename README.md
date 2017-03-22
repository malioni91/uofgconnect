# UofG Connect
UofG Connect’s primary objective is to help students find their friends’ location around the campus and provide an intuitive interface to keep them in touch. Students can register only through their university e-mail address and once logged in,
they can search for their friends that are UofG users. The app will then display the friends’ locations on the map 
and allow the user to send a message to their friends.

### Authors

* Pavlos Ratis

* Nikolaos Theodosis

* Anastasis Agathokleous

* Malion Hoxhallari

### Demo Site

The application is deployed to the [PythonAnywhere](https://www.pythonanywhere.com/) hosting service.

UofG Connect at Python Anywhere: [http://victoriancode.pythonanywhere.com/](http://victoriancode.pythonanywhere.com/)

*Note:*Please browse the above link from **Mozilla Firefox**.
The Google Map Geolocation API does not work from Google Chrome if the app is not hosted on a secure site.
For more information on the issue, please consult the [link](https://sites.google.com/a/chromium.org/dev/Home/chromium-security/deprecating-powerful-features-on-insecure-origins)

### Demo Credentials

Please enter the following credentials if you want to take a quick look into the app without registering:

    username: john
    password: smith

This project template creates a Django 1.9/1.10 project with a base set of applications.


### Installation Process
In order to install and test the application locally, you need to execute the following sequence of commands.

Clone the repository from Github:

    git clone https://github.com/uofgconnect/uofgconnect.git

Install all necessary Python prerequisites:

    pip install -r requirements.txt

Create database migrations:

    python manage.py makemigrations

The following command applies the migrations:

    python manage.py migrate

In order to load all the course titles into the database, execute the following command:

    python manage.py loaddata Courses

To populate the database with a set of new users run: 

    python populate_script.py
    
To run the test suite you need to execute:

    python manage.py test connect.tests
