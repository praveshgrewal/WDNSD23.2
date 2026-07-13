"""
sentiment_app URL configuration – project-level router.
"""

from django.urls import path, include

urlpatterns = [
    path("", include("analyzer.urls")),
]
