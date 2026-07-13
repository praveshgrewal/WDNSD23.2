"""
analyzer/urls.py
"""

from django.urls import path
from . import views

app_name = "analyzer"

urlpatterns = [
    path("", views.home, name="home"),
    path("predict/", views.predict_view, name="predict"),
    path("about/", views.about, name="about"),
]
