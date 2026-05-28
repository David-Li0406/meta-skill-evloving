---
name: python-django
description: Django framework, ORM, class-based views, DRF patterns, project structure
license: MIT
compatibility: opencode
metadata:
  audience: python-developers
  focus: web-frameworks
---

## What I do

I provide guidance on building applications with Django, including:

- Django app structure and organization
- Models, migrations, and database design
- QuerySet optimization (select_related, prefetch_related)
- Views and class-based views
- Django REST Framework patterns
- Django Admin customization
- Middleware and signals
- Templates and static files
- Authentication and permissions
- Testing Django applications

## When to use me

Use me when:
- Building web applications with Django
- Designing Django models and migrations
- Optimizing QuerySets
- Creating views and class-based views
- Working with Django REST Framework
- Customizing Django Admin
- Implementing authentication and permissions
- Testing Django applications
- Configuring Django settings

## Best Practices

### ✅ Optimized QuerySets with select_related/prefetch_related

```python
from django.db import models
from typing import Iterable

# Model definitions
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

# ❌ BAD: N+1 query problem
def get_all_books_bad() -> Iterable[Book]:
    books = Book.objects.all()
    for book in books:
        print(book.author.name)  # Generates N queries

# ✅ GOOD: Use select_related for foreign keys
def get_all_books_good() -> Iterable[Book]:
    return (
        Book.objects
        .select_related('author')
        .all()
    )

# ✅ GOOD: Use prefetch_related for many-to-many or reverse relations
class Category(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='categories')

def get_books_with_categories() -> Iterable[Book]:
    return (
        Book.objects
        .prefetch_related('categories')
        .all()
    )

# ✅ GOOD: Chain both for complex queries
def get_author_with_books_and_categories(author_id: int) -> Author:
    return (
        Author.objects
        .prefetch_related(
            'book_set',
            'book_set__categories'
        )
        .get(id=author_id)
    )
```

### ✅ Class-Based Views with Mixins

```python
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post

class PostListView(ListView):
    """List all posts."""
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

class PostDetailView(DetailView):
    """Detail view for a single post."""
    model = Post
    template_name = 'posts/detail.html'
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'

class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post."""
    model = Post
    template_name = 'posts/form.html'
    fields = ['title', 'content', 'category']
    success_url = reverse_lazy('posts:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

### ✅ Django REST Framework Patterns

```python
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'category_name']

    def validate_price(self, value: float) -> float:
        """Validate price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product CRUD operations."""
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'price']

    @action(detail=False, methods=['get'])
    def expensive(self, request):
        """Get expensive products."""
        threshold = float(request.query_params.get('threshold', 100))
        products = self.queryset.filter(price__gte=threshold)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
```

### ✅ Custom Django Admin

```python
from django.contrib import admin
from .models import User, Order, Product

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Custom admin for User model."""
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_login']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('orders')

class OrderItemInline(admin.TabularInline):
    """Inline for order items."""
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Custom admin for Order model."""
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
```

### ✅ Signals for Decoupled Logic

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification

@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    """Create notification when order is created."""
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"Order #{instance.id} created",
            notification_type='order'
        )

# Alternative: Use apps.py for signal registration
# apps.py
from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        import orders.signals
```

### ✅ Django Middleware

```python
from django.http import HttpRequest, HttpResponse
import time

class TimingMiddleware:
    """Middleware to time requests."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Time the request processing."""
        start_time = time.time()
        response = self.get_response(request)
        process_time = time.time() - start_time
        response['X-Process-Time'] = str(process_time)
        return response

# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'myapp.middleware.TimingMiddleware',
]
```

### ✅ Testing Django Applications

```python
from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, User

class PostModelTest(TestCase):
    """Test Post model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )

    def test_post_creation(self):
        """Test post is created correctly."""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)

    def test_post_str(self):
        """Test post __str__ method."""
        self.assertEqual(str(self.post), 'Test Post')

class PostViewTest(TestCase):
    """Test Post views."""

    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )

    def test_post_list_view(self):
        """Test post list view."""
        response = self.client.get(reverse('posts:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'posts/list.html')

    def test_post_detail_view(self):
        """Test post detail view."""
        response = self.client.get(
            reverse('posts:detail', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
```

### ✅ Django Settings Organization

```python
# settings/base.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'myapp',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # ... other middleware
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['example.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}
```

### ✅ Django Model Managers and QuerySets

```python
from django.db import models
from django.db.models import QuerySet, Manager

class PostQuerySet(models.QuerySet):
    """Custom QuerySet for Post model."""

    def published(self) -> 'PostQuerySet':
        """Filter published posts."""
        return self.filter(status='published')

    def by_author(self, author_id: int) -> 'PostQuerySet':
        """Filter posts by author."""
        return self.filter(author_id=author_id)

    def with_comment_count(self) -> 'PostQuerySet':
        """Annotate posts with comment count."""
        return self.annotate(
            comment_count=models.Count('comments')
        )

class PostManager(models.Manager):
    """Custom manager for Post model."""

    def get_queryset(self) -> PostQuerySet:
        """Return custom queryset."""
        return PostQuerySet(self.model, using=self._db)

    def active(self) -> 'PostQuerySet':
        """Get active posts."""
        return self.get_queryset().published()

class Post(models.Model):
    """Blog post model."""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def __str__(self) -> str:
        return self.title
```

## Common Pitfalls

### ❌ Don't Create N+1 Query Problems

```python
# BAD: N+1 queries
posts = Post.objects.all()
for post in posts:
    print(post.author.email)  # Generates N queries

# GOOD: Use select_related
posts = Post.objects.select_related('author').all()
for post in posts:
    print(post.author.email)  # Single query
```

### ❌ Don't Put Business Logic in Views

```python
# BAD: Business logic in view
def order_view(request):
    order = Order.objects.get(id=request.GET['order_id'])
    # Complex logic here
    if order.status == 'pending' and order.total > 100:
        # ...
    return render(request, 'order.html')

# GOOD: Use model methods or services
class Order(models.Model):
    def can_be_processed(self) -> bool:
        """Check if order can be processed."""
        return self.status == 'pending' and self.total > 100

def order_view(request):
    order = Order.objects.get(id=request.GET['order_id'])
    if not order.can_be_processed():
        return HttpResponseForbidden()
    return render(request, 'order.html')
```

### ❌ Don't Forget to Run Migrations

```python
# Always run migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Check for unapplied migrations
python manage.py showmigrations
```

## Project Structure

```
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── serializers.py
│   │   └── tests/
│   ├── users/
│   │   └── ...
│   └── products/
│       └── ...
├── templates/
│   └── base.html
├── static/
│   ├── css/
│   ├── js/
│   └── img/
└── media/
```

## References

- Django documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Two Scoops of Django: https://www.feldroy.com/books/two-scoops-of-django-3-x
- Django Best Practices: https://django-styleguide.readthedocs.io/
