# Test Data Factories

Patterns for creating test data consistently and efficiently.

## Factory Pattern Implementations

### Python - Factory Boy

```python
import factory
from factory import fuzzy
from myapp.models import User, Order, Item

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker('name')
    email = factory.LazyAttribute(lambda o: f"{o.name.lower().replace(' ', '.')}@example.com")
    status = "active"
    created_at = factory.LazyFunction(datetime.utcnow)

    class Params:
        admin = factory.Trait(
            role="admin",
            permissions=["read", "write", "delete"]
        )

class ItemFactory(factory.Factory):
    class Meta:
        model = Item

    name = factory.Faker('word')
    price = fuzzy.FuzzyDecimal(1.00, 1000.00)
    quantity = fuzzy.FuzzyInteger(1, 100)

class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    status = "pending"

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if extracted:
            for item in extracted:
                self.items.append(item)
        elif create:
            self.items.append(ItemFactory())
```

**Usage:**
```python
# Simple creation
user = UserFactory()

# With overrides
admin = UserFactory(admin=True, name="Admin User")

# With relationships
order = OrderFactory(
    user=UserFactory(name="Customer"),
    items=[ItemFactory(price=100), ItemFactory(price=50)]
)

# Batch creation
users = UserFactory.create_batch(10)
```

### TypeScript - Factories

```typescript
import { faker } from '@faker-js/faker';

interface User {
  id: string;
  name: string;
  email: string;
  status: 'active' | 'inactive';
}

const createUser = (overrides: Partial<User> = {}): User => ({
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  status: 'active',
  ...overrides
});

interface Order {
  id: string;
  userId: string;
  items: OrderItem[];
  total: number;
}

const createOrder = (overrides: Partial<Order> = {}): Order => {
  const items = overrides.items ?? [createOrderItem(), createOrderItem()];
  return {
    id: faker.string.uuid(),
    userId: faker.string.uuid(),
    items,
    total: items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    ...overrides
  };
};

// Usage
const user = createUser({ status: 'inactive' });
const order = createOrder({ userId: user.id });
```

### Ruby - FactoryBot

```ruby
FactoryBot.define do
  factory :user do
    name { Faker::Name.name }
    email { Faker::Internet.email }
    status { "active" }

    trait :admin do
      role { "admin" }
      permissions { %w[read write delete] }
    end

    trait :with_orders do
      transient do
        orders_count { 3 }
      end

      after(:create) do |user, evaluator|
        create_list(:order, evaluator.orders_count, user: user)
      end
    end
  end

  factory :order do
    user
    status { "pending" }

    trait :with_items do
      transient do
        items_count { 2 }
      end

      after(:create) do |order, evaluator|
        create_list(:item, evaluator.items_count, order: order)
      end
    end
  end
end
```

**Usage:**
```ruby
# Simple
user = create(:user)

# With traits
admin = create(:user, :admin)

# With nested data
user_with_orders = create(:user, :with_orders, orders_count: 5)
```

## Fixture Strategies

### JSON Fixtures

```json
// fixtures/users.json
{
  "basic_user": {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com",
    "status": "active"
  },
  "admin_user": {
    "id": 2,
    "name": "Admin User",
    "email": "admin@example.com",
    "status": "active",
    "role": "admin"
  }
}
```

```python
import json

@pytest.fixture
def fixtures():
    with open('fixtures/users.json') as f:
        return json.load(f)

def test_with_fixture(fixtures):
    user_data = fixtures['basic_user']
    # Use user_data in test
```

### Database Seeding

```python
class TestDataSeeder:
    def __init__(self, session):
        self.session = session
        self._created = {}

    def seed_all(self):
        self.seed_users()
        self.seed_products()
        self.seed_orders()
        return self._created

    def seed_users(self):
        users = [
            User(email="admin@test.com", role="admin"),
            User(email="user1@test.com", role="user"),
            User(email="user2@test.com", role="user"),
        ]
        self.session.add_all(users)
        self.session.flush()
        self._created['users'] = users
        return users

    def seed_products(self):
        products = [
            Product(name="Widget", price=10.00, stock=100),
            Product(name="Gadget", price=25.00, stock=50),
        ]
        self.session.add_all(products)
        self.session.flush()
        self._created['products'] = products
        return products

@pytest.fixture
def seeded_db(db_session):
    seeder = TestDataSeeder(db_session)
    return seeder.seed_all()
```

## Advanced Factory Patterns

### Sequences

```python
class UserFactory(factory.Factory):
    # Unique email for each instance
    email = factory.Sequence(lambda n: f"user{n}@example.com")

    # Unique username
    username = factory.Sequence(lambda n: f"user_{n}")
```

### Lazy Attributes

```python
class OrderFactory(factory.Factory):
    # Computed from other fields
    total = factory.LazyAttribute(
        lambda o: sum(item.price for item in o.items) if o.items else 0
    )

    # Computed at creation time
    created_at = factory.LazyFunction(datetime.utcnow)
```

### Circular References

```python
class CommentFactory(factory.Factory):
    class Meta:
        model = Comment

    author = factory.SubFactory('tests.factories.UserFactory')
    post = factory.SubFactory('tests.factories.PostFactory')

    # Self-referential (replies)
    parent = None  # Set explicitly when needed
```

### State-Based Factories

```python
class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    class Params:
        # State traits
        pending = factory.Trait(
            status="pending",
            paid_at=None,
            shipped_at=None
        )
        paid = factory.Trait(
            status="paid",
            paid_at=factory.LazyFunction(datetime.utcnow),
            shipped_at=None
        )
        shipped = factory.Trait(
            status="shipped",
            paid_at=factory.LazyFunction(lambda: datetime.utcnow() - timedelta(days=1)),
            shipped_at=factory.LazyFunction(datetime.utcnow)
        )
```

## Data Generation Utilities

### Realistic Data with Faker

```python
from faker import Faker

fake = Faker()

def generate_user_data():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "country": fake.country(),
            "zip": fake.postcode()
        },
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "company": fake.company()
    }
```

### Locale-Specific Data

```python
from faker import Faker

fake_en = Faker('en_US')
fake_de = Faker('de_DE')
fake_jp = Faker('ja_JP')

def generate_localized_user(locale='en_US'):
    fake = Faker(locale)
    return {
        "name": fake.name(),
        "address": fake.address(),
        "phone": fake.phone_number()
    }
```

### Deterministic Random Data

```python
from faker import Faker

fake = Faker()
Faker.seed(12345)  # Same seed = same data

# These will always be the same
user1 = fake.name()  # Always "John Smith" (or whatever seed produces)
user2 = fake.name()  # Always "Jane Doe"
```

## Performance Considerations

### Batch Creation

```python
# SLOW - Creates one at a time
users = [UserFactory() for _ in range(1000)]

# FAST - Batch insert
users = UserFactory.build_batch(1000)
session.bulk_save_objects(users)
session.commit()
```

### Minimal Factories

```python
# SLOW - Creates all associations
class OrderFactory(factory.Factory):
    user = factory.SubFactory(UserFactory)
    items = factory.RelatedFactoryList(ItemFactory, size=3)

# FAST - Minimal for most tests
class MinimalOrderFactory(factory.Factory):
    user_id = 1  # Reference existing user
    status = "pending"
    # No items by default
```

### Shared Fixtures

```python
@pytest.fixture(scope="module")
def shared_user(db_session):
    """Create once, use in all tests in module"""
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    return user

# All tests in module share this user
def test_one(shared_user):
    pass

def test_two(shared_user):
    pass
```
