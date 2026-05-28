---
name: django-drf
description: Use this skill when building REST APIs with Django, focusing on ViewSets, Serializers, and Filters.
---

# Body of the merged SKILL.md

## Critical Patterns

- ALWAYS separate serializers by operation: Read / Create / Update / Include.
- ALWAYS use `filterset_class` for complex filtering (not `filterset_fields`).
- ALWAYS validate unknown fields in write serializers (inherit `BaseWriteSerializer`).
- ALWAYS use `select_related`/`prefetch_related` in `get_queryset()` to avoid N+1.
- ALWAYS handle `swagger_fake_view` in `get_queryset()` for schema generation.
- ALWAYS use `@extend_schema_field` for OpenAPI docs on `SerializerMethodField`.
- NEVER put business logic in serializers - use services/utils.
- NEVER use auto-increment PKs - use UUIDv4 or UUIDv7.
- NEVER use trailing slashes in URLs (`trailing_slash=False`).

> **Note:** `swagger_fake_view` is specific to **drf-spectacular** for OpenAPI schema generation.

## Implementation Checklist

When implementing a new endpoint, review these patterns in order:

| # | Pattern | Reference | Key Points |
|---|---------|-----------|------------|
| 1 | **Models** | `api/models.py` | UUID PK, `inserted_at`/`updated_at`, `JSONAPIMeta.resource_name` |
| 2 | **ViewSets** | `api/base_views.py`, `api/v1/views.py` | Inherit `BaseRLSViewSet`, `get_queryset()` with N+1 prevention |
| 3 | **Serializers** | `api/v1/serializers.py` | Separate Read/Create/Update/Include, inherit `BaseWriteSerializer` |
| 4 | **Filters** | `api/filters.py` | Use `filterset_class`, inherit base filter classes |
| 5 | **Permissions** | `api/base_views.py` | `required_permissions`, `set_required_permissions()` |
| 6 | **Pagination** | `api/pagination.py` | Custom pagination class if needed |
| 7 | **URL Routing** | `api/v1/urls.py` | `trailing_slash=False`, kebab-case paths |
| 8 | **OpenAPI Schema** | `api/v1/views.py` | `@extend_schema_view` with drf-spectacular |
| 9 | **Tests** | `api/tests/test_views.py` | JSON:API content type, fixture patterns |

## ViewSet Pattern

```python
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"status": "activated"})
```

## Serializer Patterns

```python
from rest_framework import serializers

# Read Serializer
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

# Create Serializer
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Update Serializer
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
```

## Filters

```python
from django_filters import rest_framework as filters

class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr="icontains")
    is_active = filters.BooleanFilter()
    created_after = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte"
    )
    created_before = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte"
    )

    class Meta:
        model = User
        fields = ["email", "is_active"]
```

## Permissions

```python
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user.is_staff
```

## Pagination

```python
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

# settings.py
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "api.pagination.StandardPagination",
}
```

## URL Routing

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
```

## Testing

```python
import pytest
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.mark.django_db
class TestUserViewSet:
    def test_list_users(self, authenticated_client):
        response = authenticated_client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_200_OK

    def test_create_user(self, authenticated_client):
        data = {"email": "new@test.com", "password": "pass123"}
        response = authenticated_client.post("/api/v1/users/", data)
        assert response.status_code == status.HTTP_201_CREATED
```

## Commands

```bash
# Development
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell
```

## Keywords
django, drf, rest framework, viewset, serializer, api, rest api