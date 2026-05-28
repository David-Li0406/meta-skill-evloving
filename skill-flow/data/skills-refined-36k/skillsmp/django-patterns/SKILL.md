---
name: django-patterns
description: Django patterns for models, views, Django REST Framework, and best practices
license: MIT
---

# Django Patterns Skill

Modern Django development patterns including models, class-based views, Django REST Framework, and production best practices.

## When to Use

- Building Django web applications
- Implementing REST APIs with Django REST Framework
- Structuring Django projects
- Working with Django ORM

## Project Structure

```
myproject/
├── manage.py
├── config/                 # Project configuration
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py        # Common settings
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_views.py
│   │       └── test_services.py
│   └── posts/
│       └── ...
├── core/                   # Shared utilities
│   ├── __init__.py
│   ├── models.py          # Base models
│   ├── permissions.py
│   └── pagination.py
└── requirements/
    ├── base.txt
    ├── development.txt
    └── production.txt
```

## Model Patterns

### Base Model

```python
# core/models.py
from django.db import models
import uuid


class TimeStampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract base model with UUID primary key."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel):
    """Combined base model with UUID and timestamps."""

    class Meta:
        abstract = True
```

### Model with Manager

```python
# apps/posts/models.py
from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel

User = get_user_model()


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Post.Status.PUBLISHED)

    def draft(self):
        return self.filter(status=Post.Status.DRAFT)

    def by_author(self, user):
        return self.filter(author=user)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Post(BaseModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    published_at = models.DateTimeField(null=True, blank=True)

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', '-published_at']),
        ]

    def __str__(self):
        return self.title

    def publish(self):
        from django.utils import timezone
        self.status = self.Status.PUBLISHED
        self.published_at = timezone.now()
        self.save(update_fields=['status', 'published_at', 'updated_at'])
```

### Model Validation

```python
from django.core.exceptions import ValidationError
from django.db import models


class Event(BaseModel):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_attendees = models.PositiveIntegerField(default=0)

    def clean(self):
        super().clean()
        if self.end_date and self.start_date:
            if self.end_date <= self.start_date:
                raise ValidationError({
                    'end_date': 'End date must be after start date.'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
```

## Service Layer Pattern

```python
# apps/posts/services.py
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from .models import Post


class PostService:
    @staticmethod
    @transaction.atomic
    def create_post(*, author, title: str, content: str, publish: bool = False) -> Post:
        """Create a new post with optional immediate publishing."""
        slug = slugify(title)

        # Ensure unique slug
        base_slug = slug
        counter = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        post = Post.objects.create(
            author=author,
            title=title,
            slug=slug,
            content=content,
            status=Post.Status.PUBLISHED if publish else Post.Status.DRAFT,
            published_at=timezone.now() if publish else None,
        )

        return post

    @staticmethod
    def update_post(*, post: Post, title: str = None, content: str = None) -> Post:
        """Update post fields."""
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content

        post.full_clean()
        post.save()
        return post

    @staticmethod
    def publish_post(*, post: Post) -> Post:
        """Publish a draft post."""
        if post.status == Post.Status.PUBLISHED:
            raise ValueError("Post is already published")

        post.publish()
        return post
```

## Selector Layer Pattern

```python
# apps/posts/selectors.py
from django.db.models import QuerySet, Count, Q
from .models import Post


class PostSelector:
    @staticmethod
    def get_published_posts() -> QuerySet[Post]:
        """Get all published posts."""
        return Post.objects.published().select_related('author')

    @staticmethod
    def get_post_by_slug(slug: str) -> Post:
        """Get a single post by slug."""
        return Post.objects.select_related('author').get(slug=slug)

    @staticmethod
    def get_posts_by_author(author_id: str) -> QuerySet[Post]:
        """Get all posts by a specific author."""
        return Post.objects.filter(author_id=author_id).select_related('author')

    @staticmethod
    def search_posts(query: str) -> QuerySet[Post]:
        """Search posts by title or content."""
        return Post.objects.published().filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    @staticmethod
    def get_posts_with_stats() -> QuerySet[Post]:
        """Get posts with comment count annotation."""
        return Post.objects.published().annotate(
            comment_count=Count('comments')
        ).select_related('author')
```

## Django REST Framework

### Serializers

```python
# apps/posts/serializers.py
from rest_framework import serializers
from .models import Post
from apps.users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'author',
            'status', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'published_at', 'created_at', 'updated_at']


class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    publish = serializers.BooleanField(default=False)

    def create(self, validated_data):
        from .services import PostService
        return PostService.create_post(
            author=self.context['request'].user,
            **validated_data
        )


class PostUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    content = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        from .services import PostService
        return PostService.update_post(post=instance, **validated_data)
```

### ViewSets

```python
# apps/posts/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer
from .selectors import PostSelector
from .services import PostService
from core.permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        if self.action == 'list':
            return PostSelector.get_published_posts()
        return Post.objects.select_related('author')

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        if self.action in ['update', 'partial_update']:
            return PostUpdateSerializer
        return PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, slug=None):
        """Publish a draft post."""
        post = self.get_object()

        if post.author != request.user:
            return Response(
                {'detail': 'You can only publish your own posts.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            post = PostService.publish_post(post=post)
            return Response(PostSerializer(post).data)
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """Get current user's posts."""
        posts = PostSelector.get_posts_by_author(request.user.id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
```

### Custom Permissions

```python
# core/permissions.py
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow authors to edit their own content."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow admins to modify, others can only read."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
```

### Pagination

```python
# core/pagination.py
from rest_framework.pagination import PageNumberPagination, CursorPagination


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CursorPaginationByCreated(CursorPagination):
    page_size = 20
    ordering = '-created_at'
    cursor_query_param = 'cursor'
```

### URL Configuration

```python
# apps/posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]
```

## Authentication

### Custom User Model

```python
# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import UUIDModel


class User(UUIDModel, AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]
```

### JWT Authentication Setup

```python
# config/settings/base.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.StandardPagination',
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

## Testing

```python
# apps/posts/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User
from apps.posts.models import Post


class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test content',
            author=self.user,
            status=Post.Status.PUBLISHED
        )

    def test_list_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'content': 'New content',
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_create_post_unauthenticated(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'Content'}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_publish_post(self):
        self.client.force_authenticate(user=self.user)
        draft_post = Post.objects.create(
            title='Draft',
            slug='draft',
            content='Draft content',
            author=self.user,
            status=Post.Status.DRAFT
        )
        url = reverse('post-publish', kwargs={'slug': draft_post.slug})

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        draft_post.refresh_from_db()
        self.assertEqual(draft_post.status, Post.Status.PUBLISHED)
```

## Best Practices

1. **Use services for business logic** - keep views thin
2. **Use selectors for queries** - centralize data access patterns
3. **Always use select_related/prefetch_related** - avoid N+1 queries
4. **Validate at model level** - use `clean()` method
5. **Use transactions** - wrap multi-step operations
6. **Custom user model from start** - even if using defaults
7. **Environment-specific settings** - split settings files
8. **Use UUID primary keys** - better for distributed systems
9. **Index frequently queried fields** - check slow queries
10. **Write tests** - especially for services and API endpoints
