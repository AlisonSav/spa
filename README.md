# SPA
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center">This is Testing project</h3>
Overview
This web application where Users can create Reviews and any users can comment its
Any Users can see Lasted reviews with Comments, Users list and User detail.
Any Users can write comments under the Review, but only logged Users can create Review.
Any Users can send contact form for admin.
Logged Users can create Posts and Comments, can delete Posts. 
Logged Users can update his Profile information.

The main features that have currently been implemented are:

There are models for CustomUsers, Reviews and Comments.
Users can view list and detail information for models.
Admin users can create and manage models. The admin has been optimised (the basic registration is present in admin.py).

Quick Start
To get this project up and running locally on your computer:

Set up the Python development environment. We recommend using a Python virtual environment.
Assuming you have Python setup, run the following commands (if you're on Windows you may use py instead of python to start Python):
pip3 install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py collectstatic
py manage.py createsuperuser # Create a superuser
py manage.py runserver
The project has built-in verification:
- command "tox" run this verification (flake8, black, unittests)
Open a browser to http://127.0.0.1:8000/admin/ to open the admin site
Create a few test objects of each type.
Or you can download fixtures with tested data from fixtures.json file
Open tab to http://127.0.0.1:8000 to see the main site, with your new objects.

If you to create some objects - you need to run custom management commands:
- first create Users -py manage.py create_users int
- after create Reviews -py manage.py create_reviews int
- create Comments -py manage.py create_comments int
