# Django Patterns Reference

Best practices and anti-patterns for Django development.

## Query Optimization

### select_related vs prefetch_related

```python
# select_related: ForeignKey, OneToOne (SQL JOIN)
Order.objects.select_related('customer', 'customer__company')

# prefetch_related: ManyToMany, reverse FK (separate query)
Customer.objects.prefetch_related('orders', 'orders__items')

# Combined
Order.objects.select_related('customer').prefetch_related('items')

# Prefetch with filtering
from django.db.models import Prefetch
Customer.objects.prefetch_related(
    Prefetch('orders', queryset=Order.objects.filter(status='active'))
)
```

### F() Expressions

```python
from django.db.models import F

# Avoid race conditions in updates
Product.objects.filter(id=1).update(stock=F('stock') - 1)

# Compare fields
Entry.objects.filter(comments__gt=F('pingbacks'))

# Arithmetic
Entry.objects.filter(rating__lt=F('comments') + F('pingbacks'))
```

### Q Objects

```python
from django.db.models import Q

# OR conditions
Article.objects.filter(Q(published=True) | Q(author=user))

# NOT
Article.objects.filter(~Q(status='draft'))

# Complex combinations
Article.objects.filter(
    (Q(published=True) & Q(category='news')) | Q(author=user)
)
```

### Aggregation

```python
from django.db.models import Count, Sum, Avg, Max, Min

# Single aggregate
Order.objects.aggregate(total=Sum('amount'))

# Annotate each object
Customer.objects.annotate(order_count=Count('orders'))

# Conditional aggregation
from django.db.models import Case, When
Order.objects.aggregate(
    completed=Count(Case(When(status='done', then=1))),
    pending=Count(Case(When(status='pending', then=1)))
)
```

### Efficient Patterns

```python
# .exists() instead of .count() > 0
if Order.objects.filter(user=user).exists():
    ...

# .only() / .defer() for partial loading
User.objects.only('name', 'email')
User.objects.defer('bio', 'avatar')

# .values() / .values_list() for raw data
names = User.objects.values_list('name', flat=True)

# Subqueries
from django.db.models import Subquery, OuterRef
newest = Order.objects.filter(customer=OuterRef('pk')).order_by('-created')[:1]
Customer.objects.annotate(last_order=Subquery(newest.values('created')))
```

## Model Design

### Fields Best Practices

```python
class Article(models.Model):
    # Use TextChoices
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
    
    status = models.CharField(max_length=20, choices=Status.choices)
    
    # Don't use null=True on string fields
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, default='')
    
    # Use db_index for frequent lookups
    slug = models.SlugField(db_index=True)
    
    # Always set related_name
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    
    # Auto timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['status', 'created_at'])]
    
    def __str__(self):
        return self.title
```

### Model Methods vs Managers

```python
# Model method: single instance
class Order(models.Model):
    def total_with_tax(self):
        return self.total * Decimal('1.1')

# Custom QuerySet: chainable
class OrderQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status='active')
    
    def for_customer(self, customer):
        return self.filter(customer=customer)

# Manager entry point
class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

class Order(models.Model):
    objects = OrderManager()

# Usage
Order.objects.active().for_customer(user)
```

## Views

### Function vs Class-Based

```python
# FBV for simple logic
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'article.html', {'article': article})

# CBV for standard CRUD with mixins
# Avoid over-customized CBVs (6+ overrides)
```

### Thin Views

```python
# Move logic to model
def order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    result = order.process()  # Logic in model
    return render(request, 'order.html', {'result': result})
```

## Signals vs Explicit

```python
# Prefer explicit methods
class Order(models.Model):
    def complete(self):
        self.status = 'completed'
        self.save()
        self._update_inventory()  # Explicit, traceable

# Use signals only for:
# - Decoupled apps
# - Cross-cutting concerns (audit logging)
# - Django internals
```

## Security

```python
# Check ownership
order = get_object_or_404(Order, id=id, owner=request.user)

# Safe HTML
from django.utils.html import format_html
format_html('<p>{}</p>', user_input)  # Not mark_safe()

# Environment variables for secrets
SECRET_KEY = os.environ.get('SECRET_KEY')
```

## Template Best Practices

```python
# Move logic to view
context['show_offer'] = user.orders.count() > 5

# Avoid nested loops without prefetch
# In view:
customers = Customer.objects.prefetch_related('orders')
```
