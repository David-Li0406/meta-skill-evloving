"""Django app configuration for the data layer."""

from django.apps import AppConfig


class DataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{{ cookiecutter.package_name }}.data"
    label = "data"
