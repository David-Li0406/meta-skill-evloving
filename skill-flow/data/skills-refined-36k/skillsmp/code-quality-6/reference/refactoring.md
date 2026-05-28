# リファクタリングガイド

## 目次
- リファクタリングの原則
- コードスメル
- リファクタリングパターン
- 安全なリファクタリング
- ツール

## リファクタリングの原則

### いつリファクタリングするか

1. **ボーイスカウトルール**: コードを見つけたときよりも綺麗にして去る
2. **3回ルール**: 同じパターンが3回出てきたら抽象化を検討
3. **機能追加前**: 新機能を追加しやすくするため
4. **バグ修正時**: 問題の根本原因を解決

### リファクタリングしないとき

- 締め切り直前
- 動作するコードを理解せずに変更
- テストがない状態

## コードスメル

### 長いメソッド

```python
# ❌ 長すぎるメソッド
def process_order(order):
    # バリデーション (20行)
    # 在庫チェック (15行)
    # 価格計算 (25行)
    # 決済処理 (30行)
    # 通知送信 (20行)
    pass

# ✅ 責務ごとに分割
def process_order(order):
    validate_order(order)
    check_inventory(order)
    total = calculate_total(order)
    process_payment(order, total)
    send_notifications(order)
```

### 長いパラメータリスト

```python
# ❌ パラメータが多すぎる
def create_user(name, email, phone, address, city, country, zip_code, birth_date):
    pass

# ✅ オブジェクトにまとめる
@dataclass
class UserCreateRequest:
    name: str
    email: str
    phone: str
    address: Address
    birth_date: date

def create_user(request: UserCreateRequest):
    pass
```

### 重複コード

```python
# ❌ 重複
def get_active_users():
    users = db.query(User).filter(User.status == 'active').all()
    return [{"id": u.id, "name": u.name} for u in users]

def get_premium_users():
    users = db.query(User).filter(User.plan == 'premium').all()
    return [{"id": u.id, "name": u.name} for u in users]

# ✅ 共通化
def get_users(filter_condition) -> list[dict]:
    users = db.query(User).filter(filter_condition).all()
    return [{"id": u.id, "name": u.name} for u in users]

def get_active_users():
    return get_users(User.status == 'active')

def get_premium_users():
    return get_users(User.plan == 'premium')
```

### 条件の複雑化

```python
# ❌ 複雑な条件分岐
def calculate_discount(user, order):
    if user.is_premium:
        if order.total > 10000:
            if user.years_member > 5:
                return 0.25
            else:
                return 0.20
        else:
            return 0.15
    else:
        if order.total > 10000:
            return 0.10
        else:
            return 0.05

# ✅ ポリモーフィズムまたはテーブル駆動
DISCOUNT_RULES = [
    {"condition": lambda u, o: u.is_premium and o.total > 10000 and u.years_member > 5, "rate": 0.25},
    {"condition": lambda u, o: u.is_premium and o.total > 10000, "rate": 0.20},
    {"condition": lambda u, o: u.is_premium, "rate": 0.15},
    {"condition": lambda u, o: o.total > 10000, "rate": 0.10},
    {"condition": lambda u, o: True, "rate": 0.05},
]

def calculate_discount(user, order):
    for rule in DISCOUNT_RULES:
        if rule["condition"](user, order):
            return rule["rate"]
```

## リファクタリングパターン

### Extract Method

```python
# Before
def print_invoice(invoice):
    print("=== Invoice ===")
    print(f"Customer: {invoice.customer.name}")
    print(f"Address: {invoice.customer.address}")
    
    total = 0
    for item in invoice.items:
        print(f"  {item.name}: {item.price}")
        total += item.price
    
    print(f"Total: {total}")

# After
def print_invoice(invoice):
    print_header()
    print_customer_info(invoice.customer)
    total = print_items(invoice.items)
    print_total(total)

def print_header():
    print("=== Invoice ===")

def print_customer_info(customer):
    print(f"Customer: {customer.name}")
    print(f"Address: {customer.address}")

def print_items(items) -> float:
    total = 0
    for item in items:
        print(f"  {item.name}: {item.price}")
        total += item.price
    return total

def print_total(total):
    print(f"Total: {total}")
```

### Replace Conditional with Polymorphism

```python
# Before
class Employee:
    def calculate_pay(self):
        if self.type == "hourly":
            return self.hours * self.rate
        elif self.type == "salaried":
            return self.salary / 12
        elif self.type == "commissioned":
            return self.base + self.sales * self.commission_rate

# After
class Employee(ABC):
    @abstractmethod
    def calculate_pay(self) -> float:
        pass

class HourlyEmployee(Employee):
    def calculate_pay(self) -> float:
        return self.hours * self.rate

class SalariedEmployee(Employee):
    def calculate_pay(self) -> float:
        return self.salary / 12

class CommissionedEmployee(Employee):
    def calculate_pay(self) -> float:
        return self.base + self.sales * self.commission_rate
```

### Introduce Parameter Object

```python
# Before
def search_orders(start_date, end_date, min_amount, max_amount, status, customer_id):
    pass

# After
@dataclass
class OrderSearchCriteria:
    start_date: date | None = None
    end_date: date | None = None
    min_amount: float | None = None
    max_amount: float | None = None
    status: str | None = None
    customer_id: int | None = None

def search_orders(criteria: OrderSearchCriteria):
    pass
```

### Replace Magic Number with Constant

```python
# Before
if user.age >= 18:
    pass

if order.total > 10000:
    discount = 0.1

# After
LEGAL_AGE = 18
DISCOUNT_THRESHOLD = 10000
STANDARD_DISCOUNT_RATE = 0.1

if user.age >= LEGAL_AGE:
    pass

if order.total > DISCOUNT_THRESHOLD:
    discount = STANDARD_DISCOUNT_RATE
```

## 安全なリファクタリング

### 手順

1. **テストを確認**: 既存テストがパスすることを確認
2. **小さな変更**: 一度に1つのリファクタリング
3. **テスト実行**: 各変更後にテスト
4. **コミット**: 動作する状態でコミット

### チェックリスト

```
□ 変更前にすべてのテストがパスする
□ 変更の影響範囲を把握している
□ 変更は小さく、アトミック
□ 変更後にすべてのテストがパスする
□ コードカバレッジが下がっていない
```

## ツール

### Python

```bash
# 複雑度測定
radon cc src/ -a -s

# コードスメル検出
pylint src/ --disable=all --enable=R

# 重複コード検出
pylint src/ --disable=all --enable=duplicate-code
```

### IDE機能

```
- Rename (変数/関数/クラス名変更)
- Extract Method (メソッド抽出)
- Extract Variable (変数抽出)
- Inline (インライン化)
- Move (移動)
- Change Signature (シグネチャ変更)
```
