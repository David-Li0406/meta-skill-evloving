"""URL configuration for {{ cookiecutter.project_name }}."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("{{ cookiecutter.package_name }}.interfaces.http.api.urls")),
]
