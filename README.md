CRUD Code Generator in Django


Project Overview:-
This project is a CRUD (Create, Read, Update, Delete) code generator built with Django. It generates Django project files such as models.py, views.py, and HTML templates based on user input, which includes database name, table name, and column details.

Technologies Used:-
Django: The web framework used for building the application.
Bootstrap: Used for styling and responsive design.
HTML/CSS: Basic web technologies for structure and style.

Installation and Setup:-
python manage.py makemigrations
python manage.py migrate
Access the Application:
Open your browser and go to http://127.0.0.1:8000/.

Usage
Input Details: Fill in the form with your database name, table name, and column details.
Generate Code: Click the "Generate Code" button to create models.py, views.py, and HTML templates.
View and Download: The generated code will be displayed on the page, and you can download the files.
Project Structure
models.py: Defines the database models.
views.py: Contains the logic for handling requests and rendering templates.
templates/: HTML templates for the application.
static/: Static files such as CSS and JS.
code_generator.py: Contains functions to generate code dynamically.
