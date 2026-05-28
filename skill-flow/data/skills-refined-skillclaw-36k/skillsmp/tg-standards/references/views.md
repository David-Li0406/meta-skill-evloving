# View Patterns

## Imports

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import (
    ViewPermissionMixin,
    EditPermissionMixin,
    MessageMixin,
    VisibilityFilterMixin,
    STRequiredMixin,
)
```

## Mixin Stacking Order

Always left to right:
```python
class MyUpdateView(EditPermissionMixin, MessageMixin, UpdateView): pass
class MyListView(VisibilityFilterMixin, ListView): pass
class MyCreateView(LoginRequiredMixin, MessageMixin, CreateView): pass
class MySTView(STRequiredMixin, MessageMixin, CreateView): pass
```

## ListView

```python
class MyCharacterListView(VisibilityFilterMixin, ListView):
    model = MyCharacter
    template_name = "app/mygameline/my_character/list.html"
    context_object_name = "objects"
    paginate_by = 50

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("owner", "chronicle")
            .prefetch_related("my_ratings__reference")
        )
```

## DetailView

```python
class MyCharacterDetailView(ViewPermissionMixin, DetailView):
    model = MyCharacter
    template_name = "app/mygameline/my_character/detail.html"
    context_object_name = "object"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("owner", "chronicle", "faction")
            .prefetch_related("my_ratings__reference", "merits_and_flaws__meritflaw")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_items"] = self.object.items.all()
        return context
```

## CreateView

```python
class MyCharacterCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = MyCharacter
    form_class = MyCharacterCreationForm
    template_name = "app/mygameline/my_character/form.html"
    success_message = "Character '{name}' created successfully!"

    def form_valid(self, form):
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
```

## UpdateView

```python
class MyCharacterUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = MyCharacter
    template_name = "app/mygameline/my_character/form.html"
    success_message = "Character '{name}' updated successfully!"

    def get_form_class(self):
        if self.request.user.profile.is_st() or self.request.user.is_staff:
            return MyCharacterForm
        return LimitedMyCharacterEditForm

    def get_queryset(self):
        return super().get_queryset().select_related("owner", "chronicle")
```

## Cached Reference View

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 15), name="dispatch")
class MyReferenceDetailView(DetailView):
    model = MyReference
    template_name = "app/mygameline/my_reference/detail.html"
```

## Key Rules

- Always use `select_related` for ForeignKey, `prefetch_related` for M2M
- Use `ViewPermissionMixin` for detail views, `EditPermissionMixin` for update views
- Use `VisibilityFilterMixin` for list views to auto-filter by visibility
- Choose form class based on `is_st()` in UpdateView
