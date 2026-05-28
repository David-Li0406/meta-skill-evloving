# Wagtail CMS Testing Rules

**For pytest-based testing of Wagtail 6.0+/7.x Page/Snippet models, views, and templates**

## Rule 1: Test Framework Setup

### Required Dependencies

```toml
# pyproject.toml
[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-django>=4.8.0",
    "pytest-cov>=4.1.0",
    "factory-boy>=3.3.0",
    "wagtail-factories>=4.1.0",
]
```

### pytest Configuration

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = synnovator.settings.dev
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    wagtail: marks tests requiring Wagtail setup
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

### Root conftest.py

```python
# conftest.py
import pytest
from django.contrib.auth import get_user_model
from wagtail.models import Page, Site

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Ensure database is ready for tests."""
    pass


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    user = User.objects.create_superuser(
        username="admin",
        email="admin@test.com",
        password="password123",
    )
    return user


@pytest.fixture
def regular_user(db):
    """Create a regular user."""
    user = User.objects.create_user(
        username="user",
        email="user@test.com",
        password="password123",
    )
    return user


@pytest.fixture
def wagtail_root(db):
    """Get or create Wagtail root page."""
    root = Page.objects.filter(depth=1).first()
    if not root:
        root = Page.add_root(title="Root", slug="root")
    return root


@pytest.fixture
def default_site(db, wagtail_root):
    """Ensure default site exists."""
    site, _ = Site.objects.get_or_create(
        is_default_site=True,
        defaults={
            "hostname": "localhost",
            "root_page": wagtail_root,
            "site_name": "Test Site",
        },
    )
    return site
```

---

## Rule 2: Factory Pattern for Test Data

### ❌ Incorrect: Inline Object Creation

```python
# ❌ Bad: Verbose, hard to maintain
def test_hackathon_page(db):
    user = User.objects.create_user(
        username="testuser",
        email="test@test.com",
        password="password123",
    )
    root = Page.objects.get(depth=1)
    hackathon = HackathonPage(
        title="Test Hackathon",
        slug="test-hackathon",
        status="upcoming",
        team_min_size=2,
        team_max_size=5,
        # ... 10 more fields
    )
    root.add_child(instance=hackathon)
```

**Problems**:
- Verbose, repetitive across tests
- Hard to update when model changes
- Doesn't handle relationships cleanly

### ✅ Correct: Factory Boy Factories

```python
# synnovator/hackathons/tests/factories.py
import factory
from factory.django import DjangoModelFactory
from wagtail_factories import PageFactory
from synnovator.hackathons.models import (
    HackathonPage, HackathonIndexPage, Quest, Team, TeamMember,
    Submission, Phase, Prize
)
from synnovator.users.tests.factories import UserFactory


class HackathonIndexPageFactory(PageFactory):
    """Factory for HackathonIndexPage."""

    class Meta:
        model = HackathonIndexPage

    title = "Hackathons"
    slug = factory.LazyAttribute(lambda o: f"hackathons-{factory.Faker('uuid4').generate()[:8]}")


class HackathonPageFactory(PageFactory):
    """Factory for HackathonPage."""

    class Meta:
        model = HackathonPage

    title = factory.Faker("sentence", nb_words=3)
    slug = factory.LazyAttribute(lambda o: f"hackathon-{factory.Faker('uuid4').generate()[:8]}")
    status = "upcoming"
    team_min_size = 2
    team_max_size = 5
    allow_solo_participation = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to handle Wagtail page tree structure."""
        parent = kwargs.pop("parent", None)
        if parent is None:
            # Find or create HackathonIndexPage as parent
            index = HackathonIndexPage.objects.first()
            if not index:
                root = Page.objects.get(depth=1)
                index = HackathonIndexPageFactory(parent=root)
            parent = index
        instance = model_class(*args, **kwargs)
        parent.add_child(instance=instance)
        return HackathonPage.objects.get(pk=instance.pk)


class QuestFactory(DjangoModelFactory):
    """Factory for Quest snippet."""

    class Meta:
        model = Quest

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    quest_type = "technical"
    difficulty = "intermediate"
    xp_reward = factory.Faker("random_int", min=10, max=100)
    is_active = True


class TeamFactory(DjangoModelFactory):
    """Factory for Team."""

    class Meta:
        model = Team

    name = factory.Faker("company")
    hackathon = factory.SubFactory(HackathonPageFactory)
    status = "forming"

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                TeamMemberFactory(team=self, user=user)


class TeamMemberFactory(DjangoModelFactory):
    """Factory for TeamMember through model."""

    class Meta:
        model = TeamMember

    team = factory.SubFactory(TeamFactory)
    user = factory.SubFactory(UserFactory)
    role = "hacker"
    is_leader = False


class SubmissionFactory(DjangoModelFactory):
    """Factory for Submission."""

    class Meta:
        model = Submission

    user = factory.SubFactory(UserFactory)
    quest = factory.SubFactory(QuestFactory)
    repository_url = factory.Faker("url")
    verification_status = "pending"


class PhaseFactory(DjangoModelFactory):
    """Factory for Phase inline model."""

    class Meta:
        model = Phase

    page = factory.SubFactory(HackathonPageFactory)
    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    start_date = factory.Faker("date_object")
    end_date = factory.Faker("future_date")


class PrizeFactory(DjangoModelFactory):
    """Factory for Prize inline model."""

    class Meta:
        model = Prize

    page = factory.SubFactory(HackathonPageFactory)
    title = factory.Faker("sentence", nb_words=3)
    ranking = factory.Sequence(lambda n: n + 1)
    monetary_value = factory.Faker("random_int", min=100, max=10000)
```

### User Factory (synnovator/users/tests/factories.py)

```python
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory for custom User model."""

    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    preferred_role = "hacker"
    xp_points = 0
    reputation_score = 0


class AdminUserFactory(UserFactory):
    """Factory for admin users."""

    is_staff = True
    is_superuser = True
```

---

## Rule 3: Model Test Patterns

### Test Categories for Each Model

| Category | What to Test | Example |
|----------|-------------|---------|
| Creation | Model can be created with valid data | `test_quest_creation` |
| Validation | Invalid data raises ValidationError | `test_quest_invalid_difficulty` |
| Relationships | Related objects work correctly | `test_team_has_members` |
| Methods | Model methods return expected values | `test_team_get_leader` |
| Constraints | Unique/Check constraints work | `test_team_member_unique_per_team` |
| Permissions | Access control works | `test_submission_user_can_edit_own` |

### ✅ Correct: Comprehensive Model Test

```python
# synnovator/hackathons/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from synnovator.hackathons.tests.factories import (
    QuestFactory, TeamFactory, TeamMemberFactory, SubmissionFactory,
    HackathonPageFactory, PhaseFactory
)
from synnovator.users.tests.factories import UserFactory


class TestQuest:
    """Tests for Quest snippet model."""

    def test_quest_creation(self, db):
        """Quest can be created with valid data."""
        quest = QuestFactory()
        assert quest.pk is not None
        assert quest.title
        assert quest.quest_type in ["technical", "commercial", "operational", "mixed"]

    def test_quest_str_representation(self, db):
        """Quest __str__ returns title."""
        quest = QuestFactory(title="Build an API")
        assert str(quest) == "Build an API"

    def test_quest_difficulty_choices(self, db):
        """Quest difficulty must be valid choice."""
        quest = QuestFactory(difficulty="expert")
        assert quest.difficulty == "expert"

    def test_quest_xp_reward_positive(self, db):
        """Quest XP reward must be positive."""
        quest = QuestFactory(xp_reward=50)
        assert quest.xp_reward > 0


class TestTeam:
    """Tests for Team model."""

    def test_team_creation(self, db):
        """Team can be created with hackathon."""
        team = TeamFactory()
        assert team.pk is not None
        assert team.hackathon is not None

    def test_team_with_members(self, db):
        """Team can have members through TeamMember."""
        user1 = UserFactory()
        user2 = UserFactory()
        team = TeamFactory()
        TeamMemberFactory(team=team, user=user1, is_leader=True)
        TeamMemberFactory(team=team, user=user2)

        assert team.members.count() == 2

    def test_team_get_leader(self, db):
        """Team.get_leader() returns the leader."""
        leader = UserFactory()
        member = UserFactory()
        team = TeamFactory()
        TeamMemberFactory(team=team, user=leader, is_leader=True)
        TeamMemberFactory(team=team, user=member, is_leader=False)

        assert team.get_leader() == leader

    def test_team_no_leader_returns_none(self, db):
        """Team without leader returns None."""
        team = TeamFactory()
        member = UserFactory()
        TeamMemberFactory(team=team, user=member, is_leader=False)

        assert team.get_leader() is None

    def test_team_member_unique_constraint(self, db):
        """User cannot join same team twice."""
        user = UserFactory()
        team = TeamFactory()
        TeamMemberFactory(team=team, user=user)

        with pytest.raises(IntegrityError):
            TeamMemberFactory(team=team, user=user)

    def test_team_status_transitions(self, db):
        """Team status follows valid transitions."""
        team = TeamFactory(status="forming")
        assert team.status == "forming"

        team.status = "active"
        team.save()
        assert team.status == "active"


class TestSubmission:
    """Tests for Submission model."""

    def test_submission_for_quest(self, db):
        """Submission can be for a quest."""
        user = UserFactory()
        quest = QuestFactory()
        submission = SubmissionFactory(user=user, quest=quest, team=None, hackathon=None)

        assert submission.quest == quest
        assert submission.user == user

    def test_submission_for_hackathon_team(self, db):
        """Submission can be for hackathon from team."""
        hackathon = HackathonPageFactory()
        team = TeamFactory(hackathon=hackathon)
        submission = SubmissionFactory(
            user=None,
            team=team,
            quest=None,
            hackathon=hackathon
        )

        assert submission.team == team
        assert submission.hackathon == hackathon

    def test_submission_verification_workflow(self, db):
        """Submission verification status transitions."""
        submission = SubmissionFactory(verification_status="pending")
        assert submission.verification_status == "pending"

        submission.verification_status = "verified"
        submission.save()
        assert submission.verification_status == "verified"


class TestHackathonPage:
    """Tests for HackathonPage Wagtail model."""

    def test_hackathon_page_creation(self, db):
        """HackathonPage can be created in page tree."""
        hackathon = HackathonPageFactory(title="AI Challenge 2026")
        assert hackathon.pk is not None
        assert hackathon.title == "AI Challenge 2026"
        assert hackathon.live is True

    def test_hackathon_page_with_phases(self, db):
        """HackathonPage can have phases."""
        hackathon = HackathonPageFactory()
        phase1 = PhaseFactory(page=hackathon, title="Registration")
        phase2 = PhaseFactory(page=hackathon, title="Submission")

        assert hackathon.phases.count() == 2

    def test_hackathon_team_size_validation(self, db):
        """Team size validation works."""
        hackathon = HackathonPageFactory(team_min_size=2, team_max_size=5)
        assert hackathon.team_min_size < hackathon.team_max_size

    def test_hackathon_get_leaderboard(self, db):
        """get_leaderboard returns top teams by score."""
        hackathon = HackathonPageFactory()
        team1 = TeamFactory(hackathon=hackathon, final_score=100)
        team2 = TeamFactory(hackathon=hackathon, final_score=80)
        team3 = TeamFactory(hackathon=hackathon, final_score=90)

        leaderboard = hackathon.get_leaderboard(limit=10)
        assert list(leaderboard) == [team1, team3, team2]
```

---

## Rule 4: Wagtail Page Testing Patterns

### Testing Wagtail Page Hierarchy

```python
# synnovator/hackathons/tests/test_pages.py
import pytest
from wagtail.models import Page
from synnovator.hackathons.tests.factories import (
    HackathonIndexPageFactory, HackathonPageFactory
)


class TestHackathonPageHierarchy:
    """Tests for Wagtail page tree structure."""

    def test_hackathon_index_under_root(self, db, wagtail_root):
        """HackathonIndexPage can be child of root."""
        index = HackathonIndexPageFactory(parent=wagtail_root)
        assert index.get_parent() == wagtail_root

    def test_hackathon_page_under_index(self, db, wagtail_root):
        """HackathonPage must be child of HackathonIndexPage."""
        index = HackathonIndexPageFactory(parent=wagtail_root)
        hackathon = HackathonPageFactory(parent=index)
        assert hackathon.get_parent() == index

    def test_hackathon_index_max_count(self, db, wagtail_root):
        """Only one HackathonIndexPage should exist."""
        index1 = HackathonIndexPageFactory(parent=wagtail_root)
        # Wagtail's max_count=1 should prevent this
        # Test depends on your model's max_count setting

    def test_hackathon_url_path(self, db, wagtail_root, default_site):
        """HackathonPage has correct URL path."""
        index = HackathonIndexPageFactory(parent=wagtail_root, slug="hackathons")
        hackathon = HackathonPageFactory(parent=index, slug="ai-challenge")

        assert hackathon.url_path == "/hackathons/ai-challenge/"


class TestHackathonPageContext:
    """Tests for HackathonPage.get_context()."""

    def test_context_includes_phases(self, db, client):
        """Page context includes ordered phases."""
        hackathon = HackathonPageFactory()
        phase1 = PhaseFactory(page=hackathon, title="Phase 1")
        phase2 = PhaseFactory(page=hackathon, title="Phase 2")

        context = hackathon.get_context(None)
        # Test your specific context additions

    def test_context_includes_teams(self, db):
        """Page context includes registered teams."""
        hackathon = HackathonPageFactory()
        team1 = TeamFactory(hackathon=hackathon)
        team2 = TeamFactory(hackathon=hackathon)

        context = hackathon.get_context(None)
        # Test your specific context additions
```

### Testing Page Rendering

```python
@pytest.mark.django_db
class TestHackathonPageRendering:
    """Tests for HackathonPage template rendering."""

    def test_hackathon_page_renders(self, client, default_site, wagtail_root):
        """HackathonPage renders without errors."""
        index = HackathonIndexPageFactory(parent=wagtail_root)
        hackathon = HackathonPageFactory(parent=index)

        response = client.get(hackathon.url)
        assert response.status_code == 200

    def test_hackathon_page_contains_title(self, client, default_site, wagtail_root):
        """Rendered page contains title."""
        index = HackathonIndexPageFactory(parent=wagtail_root)
        hackathon = HackathonPageFactory(parent=index, title="My Hackathon")

        response = client.get(hackathon.url)
        assert b"My Hackathon" in response.content

    def test_hackathon_page_lists_phases(self, client, default_site, wagtail_root):
        """Rendered page lists all phases."""
        index = HackathonIndexPageFactory(parent=wagtail_root)
        hackathon = HackathonPageFactory(parent=index)
        PhaseFactory(page=hackathon, title="Registration Phase")

        response = client.get(hackathon.url)
        assert b"Registration Phase" in response.content
```

---

## Rule 5: Template-Model Synchronization Tests

### The Problem

When backend models change (field renamed, removed, type changed), templates may break silently. These tests catch sync issues.

### ✅ Correct: Template Integration Tests

```python
# synnovator/hackathons/tests/test_template_sync.py
import pytest
from django.template import Template, Context, TemplateSyntaxError, VariableDoesNotExist
from django.template.loader import render_to_string
from synnovator.hackathons.tests.factories import (
    HackathonPageFactory, TeamFactory, QuestFactory, PhaseFactory
)
from synnovator.users.tests.factories import UserFactory


@pytest.mark.integration
class TestHackathonTemplateSync:
    """Tests that templates stay in sync with model changes."""

    def test_hackathon_index_template_renders(self, db, default_site, wagtail_root):
        """hackathon_index_page.html renders with model data."""
        from synnovator.hackathons.tests.factories import HackathonIndexPageFactory

        index = HackathonIndexPageFactory(parent=wagtail_root)
        hackathon1 = HackathonPageFactory(parent=index)
        hackathon2 = HackathonPageFactory(parent=index)

        # Test template renders without error
        html = render_to_string(
            "hackathons/hackathon_index_page.html",
            {"page": index, "hackathons": [hackathon1, hackathon2]},
        )

        assert hackathon1.title in html
        assert hackathon2.title in html

    def test_hackathon_page_template_uses_correct_fields(self, db, default_site, wagtail_root):
        """hackathon_page.html uses fields that exist on model."""
        from synnovator.hackathons.tests.factories import HackathonIndexPageFactory

        index = HackathonIndexPageFactory(parent=wagtail_root)
        hackathon = HackathonPageFactory(
            parent=index,
            title="Test Hackathon",
            status="upcoming",
        )
        PhaseFactory(page=hackathon, title="Phase 1")

        # This will fail if template references non-existent fields
        html = render_to_string(
            "hackathons/hackathon_page.html",
            {"page": hackathon, "self": hackathon},
        )

        # Verify expected content is rendered
        assert "Test Hackathon" in html

    def test_team_detail_template_uses_correct_fields(self, db):
        """team_detail_page.html uses correct Team model fields."""
        team = TeamFactory(name="Dream Team")
        leader = UserFactory(username="leader_user")
        TeamMemberFactory(team=team, user=leader, is_leader=True)

        html = render_to_string(
            "pages/team_detail_page.html",
            {"team": team, "members": team.teammember_set.all()},
        )

        assert "Dream Team" in html
        assert "leader_user" in html

    def test_quest_list_template_uses_correct_fields(self, db):
        """quest_list_page.html uses correct Quest model fields."""
        quest1 = QuestFactory(title="Build API", difficulty="beginner")
        quest2 = QuestFactory(title="Design UI", difficulty="intermediate")

        html = render_to_string(
            "pages/quest_list_page.html",
            {"quests": [quest1, quest2]},
        )

        assert "Build API" in html
        assert "Design UI" in html


@pytest.mark.integration
class TestUserTemplateSync:
    """Tests that user templates stay in sync with User model."""

    def test_user_profile_template_uses_correct_fields(self, db):
        """user_profile_page.html uses correct User model fields."""
        user = UserFactory(
            username="testuser",
            preferred_role="hacker",
            xp_points=100,
        )

        html = render_to_string(
            "pages/user_profile_page.html",
            {"profile_user": user},
        )

        assert "testuser" in html


@pytest.mark.integration
class TestComponentTemplateSync:
    """Tests that component templates render correctly."""

    def test_team_card_component(self, db):
        """components/team-card.html renders Team correctly."""
        team = TeamFactory(name="Test Team")

        html = render_to_string(
            "components/team-card.html",
            {"team": team},
        )

        assert "Test Team" in html

    def test_event_card_component(self, db, wagtail_root):
        """components/event-card.html renders HackathonPage correctly."""
        from synnovator.hackathons.tests.factories import HackathonIndexPageFactory

        index = HackathonIndexPageFactory(parent=wagtail_root)
        hackathon = HackathonPageFactory(parent=index, title="Hackathon Event")

        html = render_to_string(
            "components/event-card.html",
            {"event": hackathon},
        )

        assert "Hackathon Event" in html
```

---

## Rule 6: API Endpoint Tests

### Testing Wagtail API v2

```python
# synnovator/hackathons/tests/test_api.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.integration
class TestHackathonAPI:
    """Tests for Wagtail API v2 endpoints."""

    @pytest.fixture
    def api_client(self):
        return APIClient()

    def test_pages_endpoint_returns_hackathons(self, db, api_client, default_site, wagtail_root):
        """API pages endpoint returns hackathon pages."""
        from synnovator.hackathons.tests.factories import (
            HackathonIndexPageFactory, HackathonPageFactory
        )

        index = HackathonIndexPageFactory(parent=wagtail_root)
        hackathon = HackathonPageFactory(parent=index, title="API Test Hackathon")

        response = api_client.get("/api/v2/pages/", {"type": "hackathons.HackathonPage"})

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 1
        titles = [item["title"] for item in data["items"]]
        assert "API Test Hackathon" in titles

    def test_api_serializes_richtext_correctly(self, db, api_client, default_site, wagtail_root):
        """RichText fields serialize as HTML, not internal format."""
        from synnovator.hackathons.tests.factories import (
            HackathonIndexPageFactory, HackathonPageFactory
        )

        index = HackathonIndexPageFactory(parent=wagtail_root)
        hackathon = HackathonPageFactory(parent=index)

        response = api_client.get(f"/api/v2/pages/{hackathon.pk}/", {"fields": "*"})

        assert response.status_code == 200
        data = response.json()
        # Verify no internal embed tags in RichText output
        # (specific assertion depends on your fields)


class TestCalendarEventsAPI:
    """Tests for calendar_events_api view."""

    @pytest.fixture
    def api_client(self):
        return APIClient()

    def test_calendar_api_returns_events(self, db, api_client, wagtail_root):
        """Calendar API returns phase events."""
        from synnovator.hackathons.tests.factories import (
            HackathonIndexPageFactory, HackathonPageFactory, PhaseFactory
        )

        index = HackathonIndexPageFactory(parent=wagtail_root)
        hackathon = HackathonPageFactory(parent=index)
        phase = PhaseFactory(page=hackathon, title="Submission Period")

        response = api_client.get(reverse("hackathons:calendar_events"))

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
```

---

## Rule 7: Running Tests with Coverage

### Commands

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=synnovator --cov-report=html --cov-report=term-missing

# Run specific app tests
uv run pytest synnovator/hackathons/tests/

# Run specific test class
uv run pytest synnovator/hackathons/tests/test_models.py::TestTeam

# Run specific test
uv run pytest synnovator/hackathons/tests/test_models.py::TestTeam::test_team_creation

# Run integration tests only
uv run pytest -m integration

# Skip slow tests
uv run pytest -m "not slow"

# Run in parallel (requires pytest-xdist)
uv run pytest -n auto
```

### Coverage Configuration

```toml
# pyproject.toml
[tool.coverage.run]
source = ["synnovator"]
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/__pycache__/*",
    "*/management/commands/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
fail_under = 80
```

### Coverage Targets

| Component | Target | Priority |
|-----------|--------|----------|
| Models | >90% | High |
| Views | >80% | High |
| Templates (integration) | >70% | Medium |
| Management commands | >50% | Low |

---

## Rule 8: Test Organization

### Directory Structure

```
synnovator/
├── hackathons/
│   ├── models/
│   ├── templates/
│   ├── views.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py      # App-specific fixtures
│       ├── factories.py     # Factory Boy factories
│       ├── test_models.py   # Model unit tests
│       ├── test_pages.py    # Wagtail page tests
│       ├── test_views.py    # View tests
│       ├── test_api.py      # API endpoint tests
│       └── test_template_sync.py  # Template integration tests
├── users/
│   └── tests/
│       ├── __init__.py
│       ├── factories.py
│       └── test_models.py
├── community/
│   └── tests/
│       ├── __init__.py
│       ├── factories.py
│       └── test_models.py
└── conftest.py              # Root fixtures
```

### App-Specific conftest.py

```python
# synnovator/hackathons/tests/conftest.py
import pytest
from synnovator.hackathons.tests.factories import (
    HackathonIndexPageFactory,
    HackathonPageFactory,
    QuestFactory,
    TeamFactory,
)


@pytest.fixture
def hackathon_index(db, wagtail_root):
    """Create a HackathonIndexPage."""
    return HackathonIndexPageFactory(parent=wagtail_root)


@pytest.fixture
def hackathon(db, hackathon_index):
    """Create a HackathonPage."""
    return HackathonPageFactory(parent=hackathon_index)


@pytest.fixture
def quest(db):
    """Create a Quest."""
    return QuestFactory()


@pytest.fixture
def team(db, hackathon):
    """Create a Team for hackathon."""
    return TeamFactory(hackathon=hackathon)
```

---

## Complete Test Checklist

### Before Merging New Code

- [ ] All new models have corresponding test file
- [ ] All model methods have test coverage
- [ ] All Wagtail pages have page rendering tests
- [ ] All templates have template-sync tests
- [ ] All API endpoints have integration tests
- [ ] Coverage is >80% for new code
- [ ] No failing tests: `uv run pytest`
- [ ] Coverage report reviewed: `uv run pytest --cov --cov-report=term-missing`

### After Model Changes

- [ ] Run template-sync tests: `uv run pytest -m integration`
- [ ] Check for template errors in rendered pages
- [ ] Update factories if fields changed
- [ ] Update test assertions for new behavior

---

## Summary

**5 Critical Testing Rules**:
1. Use Factory Boy for test data, not inline creation
2. Test model creation, validation, relationships, methods, constraints
3. Test Wagtail page hierarchy and context
4. Add template-sync tests to catch model-template mismatches
5. Maintain >80% coverage on models, >60% overall

**Commands to remember**:
```bash
uv run pytest                           # Run all tests
uv run pytest --cov=synnovator          # With coverage
uv run pytest -m integration            # Integration tests only
uv run pytest -k "test_team"            # Tests matching pattern
```

**See also**:
- `SKILL.md` - Main Wagtail development guidelines
- `rules/data-models.md` - Model design patterns
- `rules/i18n.md` - Internationalization testing
