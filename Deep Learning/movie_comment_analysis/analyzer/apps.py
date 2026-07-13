"""
analyzer/apps.py
Loads the ML model once at startup to avoid repeated disk I/O on each request.
"""

from django.apps import AppConfig


class AnalyzerConfig(AppConfig):
    default_auto_field = "django.db.backends.sqlite3"
    name = "analyzer"

    def ready(self):
        # Pre-load artifacts into the module-level cache inside views.
        # This is called once when Django starts.
        from . import views  # noqa: F401 – triggers load_artifacts() at import time
