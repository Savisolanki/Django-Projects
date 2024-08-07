from django.urls import path
from . import views
from .django_development_server import *


urlpatterns=[
    path('',views.generate_code,name='generate_code'),
    path('create_django_project', create_django_project_view, name='create_django_project'),
    # urls.py
]

