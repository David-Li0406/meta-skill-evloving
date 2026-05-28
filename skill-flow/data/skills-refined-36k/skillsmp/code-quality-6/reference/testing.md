# テスト作成ガイド

## 目次
- テストの原則
- ユニットテスト
- 統合テスト
- モック・スタブ
- テストパターン
- カバレッジ

## テストの原則

### FIRST原則

- **F**ast: 高速に実行できる
- **I**ndependent: テスト間に依存がない
- **R**epeatable: 何度実行しても同じ結果
- **S**elf-validating: 成功/失敗が明確
- **T**imely: プロダクションコードと同時に書く

### AAA パターン

```python
def test_add_item_to_cart():
    # Arrange (準備)
    cart = ShoppingCart()
    item = Item(name="Book", price=1000)
    
    # Act (実行)
    cart.add(item)
    
    # Assert (検証)
    assert len(cart.items) == 1
    assert cart.total == 1000
```

## ユニットテスト

### pytest基本

```python
import pytest

def test_basic():
    assert 1 + 1 == 2

def test_exception():
    with pytest.raises(ValueError):
        int("not a number")

def test_approximate():
    assert 0.1 + 0.2 == pytest.approx(0.3)

@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

### Fixture

```python
import pytest

@pytest.fixture
def user():
    return User(name="Test User", email="test@example.com")

@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()
    session.close()

def test_user_creation(user, db_session):
    db_session.add(user)
    db_session.commit()
    
    assert db_session.query(User).count() == 1
```

### クラスベーステスト

```python
class TestShoppingCart:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.cart = ShoppingCart()
        self.item = Item(name="Book", price=1000)
    
    def test_add_item(self):
        self.cart.add(self.item)
        assert len(self.cart.items) == 1
    
    def test_remove_item(self):
        self.cart.add(self.item)
        self.cart.remove(self.item)
        assert len(self.cart.items) == 0
    
    def test_total(self):
        self.cart.add(self.item)
        self.cart.add(Item(name="Pen", price=500))
        assert self.cart.total == 1500
```

## 統合テスト

### APIテスト（FastAPI）

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={"name": "Test", "email": "test@example.com"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test"

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
```

### データベーステスト

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()

def test_user_repository(db_session):
    repo = UserRepository(db_session)
    
    user = repo.create(name="Test", email="test@example.com")
    
    assert user.id is not None
    assert repo.get(user.id).name == "Test"
```

## モック・スタブ

### unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock

# 基本的なモック
def test_with_mock():
    mock_service = Mock()
    mock_service.get_user.return_value = {"id": 1, "name": "Test"}
    
    result = mock_service.get_user(1)
    
    assert result["name"] == "Test"
    mock_service.get_user.assert_called_once_with(1)

# patch デコレータ
@patch("app.services.external_api.call")
def test_with_patch(mock_call):
    mock_call.return_value = {"status": "ok"}
    
    result = process_data()
    
    assert result["status"] == "ok"

# コンテキストマネージャ
def test_with_context():
    with patch("app.services.send_email") as mock_send:
        mock_send.return_value = True
        
        result = notify_user(user_id=1)
        
        assert result is True
        mock_send.assert_called_once()
```

### 副作用のモック

```python
def test_side_effect():
    mock = Mock()
    
    # 例外を発生させる
    mock.side_effect = ValueError("Invalid")
    with pytest.raises(ValueError):
        mock()
    
    # 複数回呼び出しで異なる値を返す
    mock.side_effect = [1, 2, 3]
    assert mock() == 1
    assert mock() == 2
    assert mock() == 3
    
    # 関数を設定
    mock.side_effect = lambda x: x * 2
    assert mock(5) == 10
```

### 非同期モック

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_service():
    mock_service = AsyncMock()
    mock_service.fetch_data.return_value = {"data": "test"}
    
    result = await mock_service.fetch_data()
    
    assert result["data"] == "test"
```

## テストパターン

### 境界値テスト

```python
@pytest.mark.parametrize("age,expected", [
    (17, False),   # 境界値-1
    (18, True),    # 境界値
    (19, True),    # 境界値+1
    (0, False),    # 最小値
    (150, True),   # 最大値
])
def test_is_adult(age, expected):
    assert is_adult(age) == expected
```

### エラーケーステスト

```python
def test_invalid_input():
    with pytest.raises(ValueError, match="must be positive"):
        calculate_price(-100)

def test_not_found():
    repo = UserRepository(db_session)
    
    with pytest.raises(NotFoundError):
        repo.get(9999)
```

### テストダブル

```python
# Stub: 固定値を返す
class StubEmailService:
    def send(self, to, subject, body):
        return True

# Fake: 簡易実装
class FakeUserRepository:
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def create(self, user):
        user.id = self.next_id
        self.users[self.next_id] = user
        self.next_id += 1
        return user
    
    def get(self, id):
        return self.users.get(id)

# Spy: 呼び出しを記録
class SpyLogger:
    def __init__(self):
        self.logs = []
    
    def info(self, message):
        self.logs.append(("info", message))
```

## カバレッジ

### 設定

```ini
# pytest.ini
[pytest]
addopts = --cov=src --cov-report=html --cov-report=term-missing

# .coveragerc
[run]
source = src
omit = 
    */tests/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    if TYPE_CHECKING:
    raise NotImplementedError
```

### 実行

```bash
# カバレッジ付きテスト実行
pytest --cov=src --cov-report=html

# 特定ファイルのカバレッジ
pytest --cov=src/services tests/test_services.py

# 最小カバレッジを強制
pytest --cov=src --cov-fail-under=80
```

### カバレッジ目標

```
ユニットテスト: 80%以上
重要なビジネスロジック: 90%以上
ユーティリティ関数: 100%
```
