# URL Patterns

## Directory Structure

```
app/urls/
├── __init__.py           # Main router
└── gameline/
    ├── __init__.py       # Gameline router
    ├── list.py
    ├── detail.py
    ├── create.py
    └── update.py
```

## Main Router

```python
# app/urls/__init__.py
from django.urls import path, include

app_name = "app_name"

urlpatterns = [
    path("index/", IndexView.as_view(), name="index"),
    path("mygameline/", include("app.urls.mygameline", namespace="mygameline")),
]
```

## Gameline Router

```python
# app/urls/mygameline/__init__.py
from django.urls import path, include

app_name = "mygameline"

urlpatterns = [
    path("", include("app.urls.mygameline.list", namespace="list")),
    path("", include("app.urls.mygameline.detail", namespace="detail")),
    path("create/", include("app.urls.mygameline.create", namespace="create")),
    path("update/", include("app.urls.mygameline.update", namespace="update")),
]
```

## List URLs

```python
# app/urls/mygameline/list.py
from django.urls import path
from app.views.mygameline.list import MyCharacterListView, MyReferenceListView

app_name = "list"

urlpatterns = [
    path("my_character/", MyCharacterListView.as_view(), name="my_character"),
    path("my_reference/", MyReferenceListView.as_view(), name="my_reference"),
]
```

## Detail URLs

```python
# app/urls/mygameline/detail.py
from django.urls import path
from app.views.mygameline.detail import MyCharacterDetailView, MyReferenceDetailView

app_name = "detail"

urlpatterns = [
    path("my_character/<int:pk>/", MyCharacterDetailView.as_view(), name="my_character"),
    path("my_reference/<int:pk>/", MyReferenceDetailView.as_view(), name="my_reference"),
]
```

## Create URLs

```python
# app/urls/mygameline/create.py
app_name = "create"

urlpatterns = [
    path("my_character/", MyCharacterCreateView.as_view(), name="my_character"),
    path("my_reference/", MyReferenceCreateView.as_view(), name="my_reference"),
]
```

## Update URLs

```python
# app/urls/mygameline/update.py
app_name = "update"

urlpatterns = [
    path("my_character/<int:pk>/", MyCharacterUpdateView.as_view(), name="my_character"),
    path("my_reference/<int:pk>/", MyReferenceUpdateView.as_view(), name="my_reference"),
]
```

## Namespace Convention

```
app:gameline:action:model_type
```

Examples:
- `characters:vampire:detail:vampire`
- `items:mage:create:wonder`
- `locations:werewolf:update:caern`
