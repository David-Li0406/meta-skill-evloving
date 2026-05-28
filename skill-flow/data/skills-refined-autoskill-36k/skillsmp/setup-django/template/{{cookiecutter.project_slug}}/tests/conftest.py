"""Pytest configuration."""

import django
from django.conf import settings


def pytest_configure():
    """Configure Django settings for pytest."""
    if not settings.configured:
        django.setup()
