# Code Smell Examples

Concrete examples of patterns to flag during review, with suggested improvements.

## Repeated Code

### Problem

```python
def create_user(data: dict) -> User:
    if not data.get("email"):
        raise ValidationError("email is required")
    if not data.get("name"):
        raise ValidationError("name is required")
    if not data.get("password"):
        raise ValidationError("password is required")
    # ... creation logic

def update_user(user_id: int, data: dict) -> User:
    if not data.get("email"):
        raise ValidationError("email is required")
    if not data.get("name"):
        raise ValidationError("name is required")
    # ... update logic
```

### Improvement

```python
REQUIRED_USER_FIELDS = ["email", "name"]
REQUIRED_CREATE_FIELDS = [*REQUIRED_USER_FIELDS, "password"]

def validate_required(data: dict, fields: list[str]) -> None:
    for field in fields:
        if not data.get(field):
            raise ValidationError(f"{field} is required")

def create_user(data: dict) -> User:
    validate_required(data, REQUIRED_CREATE_FIELDS)
    # ... creation logic

def update_user(user_id: int, data: dict) -> User:
    validate_required(data, REQUIRED_USER_FIELDS)
    # ... update logic
```

---

## Complex Conditionals

### Problem

```python
def can_publish(article: Article, user: User) -> bool:
    if article.status == "draft":
        if user.role == "admin" or (user.role == "editor" and article.author_id == user.id):
            if article.word_count >= 100:
                if not article.flagged or user.role == "admin":
                    return True
    return False
```

### Improvement

```python
def can_publish(article: Article, user: User) -> bool:
    if article.status != "draft":
        return False
    
    if article.word_count < 100:
        return False
    
    if article.flagged and user.role != "admin":
        return False
    
    is_admin = user.role == "admin"
    is_own_article = article.author_id == user.id
    is_editor = user.role == "editor"
    
    return is_admin or (is_editor and is_own_article)
```

---

## Bumpy Road

### Problem

```python
def process_order(order: Order) -> Receipt:
    # High level
    validated = validate_order(order)
    
    # Suddenly low level
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (order.account_id,))
    row = cursor.fetchone()
    balance = row[0] if row else 0
    
    # Back to high level
    if balance < order.total:
        raise InsufficientFunds()
    
    # Low level again
    cursor.execute(
        "UPDATE accounts SET balance = balance - ? WHERE id = ?",
        (order.total, order.account_id)
    )
    connection.commit()
    
    # High level
    return generate_receipt(order)
```

### Improvement

```python
def process_order(order: Order) -> Receipt:
    validated = validate_order(order)
    balance = accounts.get_balance(order.account_id)
    
    if balance < order.total:
        raise InsufficientFunds()
    
    accounts.debit(order.account_id, order.total)
    return generate_receipt(order)
```

---

## High Similarity

### Problem

```python
def send_welcome_email(user: User) -> None:
    template = load_template("welcome")
    body = template.render(name=user.name, email=user.email)
    mailer.send(to=user.email, subject="Welcome!", body=body)
    log.info(f"Sent welcome email to {user.email}")

def send_password_reset_email(user: User, token: str) -> None:
    template = load_template("password_reset")
    body = template.render(name=user.name, email=user.email, token=token)
    mailer.send(to=user.email, subject="Password Reset", body=body)
    log.info(f"Sent password reset email to {user.email}")

def send_invoice_email(user: User, invoice: Invoice) -> None:
    template = load_template("invoice")
    body = template.render(name=user.name, email=user.email, invoice=invoice)
    mailer.send(to=user.email, subject=f"Invoice #{invoice.id}", body=body)
    log.info(f"Sent invoice email to {user.email}")
```

### Improvement

```python
@dataclass
class EmailSpec:
    template: str
    subject: str
    context: dict[str, Any]

def send_email(user: User, spec: EmailSpec) -> None:
    template = load_template(spec.template)
    base_context = {"name": user.name, "email": user.email}
    body = template.render(**base_context, **spec.context)
    mailer.send(to=user.email, subject=spec.subject, body=body)
    log.info(f"Sent {spec.template} email to {user.email}")

def send_welcome_email(user: User) -> None:
    send_email(user, EmailSpec("welcome", "Welcome!", {}))

def send_password_reset_email(user: User, token: str) -> None:
    send_email(user, EmailSpec("password_reset", "Password Reset", {"token": token}))

def send_invoice_email(user: User, invoice: Invoice) -> None:
    send_email(user, EmailSpec("invoice", f"Invoice #{invoice.id}", {"invoice": invoice}))
```

---

## Magic Literals

### Problem

```python
def calculate_shipping(weight: float, distance: float) -> float:
    base = 5.99
    if weight > 10:
        base += (weight - 10) * 0.5
    if distance > 100:
        base *= 1.15
    if distance > 500:
        base *= 1.25
    return min(base, 49.99)
```

### Improvement

```python
BASE_SHIPPING_COST = 5.99
WEIGHT_THRESHOLD_KG = 10
EXCESS_WEIGHT_RATE = 0.50  # per kg over threshold
MEDIUM_DISTANCE_KM = 100
LONG_DISTANCE_KM = 500
MEDIUM_DISTANCE_MULTIPLIER = 1.15
LONG_DISTANCE_MULTIPLIER = 1.25
MAX_SHIPPING_COST = 49.99

def calculate_shipping(weight_kg: float, distance_km: float) -> float:
    cost = BASE_SHIPPING_COST
    
    if weight_kg > WEIGHT_THRESHOLD_KG:
        excess = weight_kg - WEIGHT_THRESHOLD_KG
        cost += excess * EXCESS_WEIGHT_RATE
    
    if distance_km > LONG_DISTANCE_KM:
        cost *= LONG_DISTANCE_MULTIPLIER
    elif distance_km > MEDIUM_DISTANCE_KM:
        cost *= MEDIUM_DISTANCE_MULTIPLIER
    
    return min(cost, MAX_SHIPPING_COST)
```

---

## Feature Envy

### Problem

```python
def format_address(order: Order) -> str:
    addr = order.shipping_address
    lines = [addr.line1]
    if addr.line2:
        lines.append(addr.line2)
    lines.append(f"{addr.city}, {addr.state} {addr.postal_code}")
    if addr.country != "US":
        lines.append(addr.country)
    return "\n".join(lines)
```

### Improvement

```python
# In Address class
class Address:
    # ... fields ...
    
    def format(self, include_country: bool = True) -> str:
        lines = [self.line1]
        if self.line2:
            lines.append(self.line2)
        lines.append(f"{self.city}, {self.state} {self.postal_code}")
        if include_country and self.country != "US":
            lines.append(self.country)
        return "\n".join(lines)

# Usage
def format_shipping_label(order: Order) -> str:
    return order.shipping_address.format()
```

---

## Long Parameter Lists

### Problem

```python
def create_report(
    title: str,
    author: str,
    start_date: date,
    end_date: date,
    include_charts: bool,
    chart_style: str,
    include_summary: bool,
    summary_length: int,
    output_format: str,
    template_id: str,
) -> Report:
    ...
```

### Improvement

```python
@dataclass
class DateRange:
    start: date
    end: date

@dataclass
class ChartOptions:
    include: bool = False
    style: str = "bar"

@dataclass
class SummaryOptions:
    include: bool = True
    max_length: int = 500

@dataclass
class ReportConfig:
    title: str
    author: str
    date_range: DateRange
    charts: ChartOptions = field(default_factory=ChartOptions)
    summary: SummaryOptions = field(default_factory=SummaryOptions)
    output_format: str = "pdf"
    template_id: str = "default"

def create_report(config: ReportConfig) -> Report:
    ...
```

---

## Primitive Obsession

### Problem

```python
def process_payment(
    amount: int,  # cents? dollars? who knows
    currency: str,  # "USD"? "usd"? "840"?
    card_number: str,
    card_expiry: str,  # "12/25"? "2025-12"? "1225"?
) -> str:  # transaction ID, presumably
    ...
```

### Improvement

```python
@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: Currency
    
    @classmethod
    def dollars(cls, amount: Decimal) -> "Money":
        return cls(int(amount * 100), Currency.USD)

class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"

@dataclass(frozen=True)
class CardDetails:
    number: str  # could validate format
    expiry_month: int
    expiry_year: int
    
    @classmethod
    def from_expiry_string(cls, number: str, expiry: str) -> "CardDetails":
        # Parse "MM/YY" format
        month, year = expiry.split("/")
        return cls(number, int(month), 2000 + int(year))

@dataclass(frozen=True)
class TransactionId:
    value: str

def process_payment(amount: Money, card: CardDetails) -> TransactionId:
    ...
```
