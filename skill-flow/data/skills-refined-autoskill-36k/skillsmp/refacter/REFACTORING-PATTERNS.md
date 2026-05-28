# Refactoring Patterns

Common refactoring techniques with before/after examples.

**Source**: Martin Fowler's "Refactoring" + "Fundamentals of Software Architecture" (connascence) + project-specific patterns

---

## Refactoring Strategy Selection

### Complexity-Based Patterns (Traditional)

| Smell | Pattern | Benefit |
|-------|---------|---------|
| Long function (> 50 LOC) | Extract Method | Improve readability |
| Complex conditionals (CC > 10) | Simplify Conditionals | Reduce complexity |
| Duplicated code | Extract Common Logic | DRY principle |
| Too many parameters (> 4) | Introduce Parameter Object | Simplify interface |
| God class (> 500 LOC) | Extract Class | Separation of concerns |
| Deep nesting (> 3 levels) | Guard Clauses | Flatten structure |

### Connascence-Based Patterns (Coupling)

| Connascence Type | Strength | Pattern | Benefit |
|-----------------|----------|---------|---------|
| CoP (Position) | Medium | Named Parameters | Self-documenting |
| CoM (Meaning) | Medium | Named Constants | Clear intent |
| CoE (Execution) | Strong | Encapsulate Order | Hide complexity |
| CoV (Values) | Very Strong | Event-Driven | Eliminate shared state |

**Refactoring Priority**: Fix strongest connascence first (CoV > CoE > CoM > CoP)

---

## Connascence-Based Refactoring Patterns

### Pattern C1: CoP → CoN (Position to Name)

**Problem**: Connascence of Position - must remember parameter order

```python
# ❌ Connascence of Position (CoP)
def generate_report(ticker, price, sma20, sma50, rsi, macd, volume):
    """7 positional parameters - error-prone"""
    ...

# Caller must remember exact order
generate_report("NVDA19", 150.25, 145.0, 140.0, 45.2, {...}, 1000000)
#                ↑ Easy to swap price and sma20 accidentally
```

**Refactoring**: Convert to Connascence of Name (CoN)

```python
# ✅ Connascence of Name (CoN) - weaker form
from dataclasses import dataclass

@dataclass
class MarketData:
    ticker: str
    price: float
    sma20: float
    sma50: float
    rsi: float
    macd: dict
    volume: int

def generate_report(data: MarketData):
    """Single parameter object - self-documenting"""
    ...

# Caller uses names, not positions
generate_report(MarketData(
    ticker="NVDA19",
    price=150.25,
    sma20=145.0,
    sma50=140.0,
    rsi=45.2,
    macd={...},
    volume=1000000
))
```

**Benefits**: CoN < CoP (weaker connascence), compiler helps, self-documenting

---

### Pattern C2: CoM → CoN (Meaning to Name)

**Problem**: Connascence of Meaning - magic numbers require shared understanding

```python
# ❌ Connascence of Meaning (CoM)
def process_market(ticker, status):
    if status == 1:        # What does 1 mean?
        activate(ticker)
    elif status == 0:
        deactivate(ticker)

# Multiple places must know: 1 = active, 0 = inactive
db.execute("UPDATE markets SET status = 1 WHERE ticker = ?", ticker)
assert market.status == 1
```

**Refactoring**: Convert to Connascence of Name (CoN)

```python
# ✅ Connascence of Name (CoN) - weaker form
from enum import Enum

class MarketStatus(Enum):
    ACTIVE = 1
    INACTIVE = 0

def process_market(ticker, status: MarketStatus):
    if status == MarketStatus.ACTIVE:    # Self-documenting
        activate(ticker)
    elif status == MarketStatus.INACTIVE:
        deactivate(ticker)

# Meaning is explicit everywhere
db.execute("UPDATE markets SET status = ? WHERE ticker = ?",
           MarketStatus.ACTIVE.value, ticker)
assert market.status == MarketStatus.ACTIVE
```

**Benefits**: CoN < CoM (weaker connascence), centralized meaning, type-safe

---

### Pattern C3: CoE → Encapsulation (Execution Order to Hidden)

**Problem**: Connascence of Execution - must call methods in specific order

```python
# ❌ Connascence of Execution (CoE) - exposed to caller
class DatabaseClient:
    def connect(self):
        self.connected = True

    def authenticate(self, creds):
        if not self.connected:
            raise RuntimeError("Must connect first!")
        self.authenticated = True

    def query(self, sql):
        if not self.authenticated:
            raise RuntimeError("Must authenticate first!")
        # Execute query

# Caller must remember exact order (CoE)
client = DatabaseClient()
client.connect()           # Step 1
client.authenticate(creds) # Step 2
client.query("SELECT ...")  # Step 3
```

**Refactoring**: Encapsulate execution order (hide CoE internally)

```python
# ✅ CoN externally, CoE hidden internally
class DatabaseClient:
    def __init__(self, credentials):
        self.credentials = credentials
        self._connected = False
        self._authenticated = False

    def query(self, sql):
        """Caller just calls query - order handled internally"""
        self._ensure_ready()  # Hide CoE inside class
        # Execute query

    def _ensure_ready(self):
        """Encapsulate execution order (CoE internal only)"""
        if not self._connected:
            self._connect()
        if not self._authenticated:
            self._authenticate()

    def _connect(self):
        self._connected = True

    def _authenticate(self):
        self._authenticated = True

# Caller has CoN (just call query by name)
client = DatabaseClient(credentials)
client.query("SELECT ...")  # Order handled automatically
```

**Benefits**: External callers have weak CoN, CoE hidden as implementation detail

---

### Pattern C4: CoV → Event-Driven (Shared Values to Eventual Consistency)

**Problem**: Connascence of Values - distributed services must agree on exact values

```python
# ❌ Connascence of Values (CoV) - very strong, dangerous across services
# Service A (Orders)
def place_order(product_id, quantity):
    # Check inventory (CoV - must match Service B's value)
    inventory = inventory_service.get_count(product_id)
    if inventory >= quantity:
        # Decrement (CoV - distributed transaction)
        inventory_service.decrement(product_id, quantity)
        order_service.create(product_id, quantity)
        return "Success"
    return "Out of stock"

# Problem: Race condition! Two orders can see inventory=10,
# both decrement by 5, result: -0 inventory but sold 10 units
```

**Refactoring**: Eliminate CoV with event-driven architecture

```python
# ✅ No CoV across services - eventual consistency
# Service A (Orders)
def place_order(product_id, quantity):
    # Create pending order (no CoV with inventory)
    order_id = order_service.create_pending(product_id, quantity)

    # Publish event (no shared values)
    event_bus.publish(OrderPlaced(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity
    ))

    return order_id

# Service B (Inventory) - owns its data (no CoV)
def on_order_placed(event: OrderPlaced):
    if inventory.reserve(event.product_id, event.quantity):
        event_bus.publish(InventoryReserved(order_id=event.order_id))
    else:
        event_bus.publish(InventoryInsufficient(order_id=event.order_id))

# Service A listens to inventory events
def on_inventory_reserved(event: InventoryReserved):
    order_service.confirm(event.order_id)

def on_inventory_insufficient(event: InventoryInsufficient):
    order_service.cancel(event.order_id)
```

**Benefits**: No CoV (each service owns data), eventual consistency, scales independently

---

## Complexity-Based Refactoring Patterns

### Pattern 1: Extract Method

**When**: Function > 50 lines or does multiple things

**Goal**: Break down large functions into smaller, focused functions

### Before

```python
# Cyclomatic Complexity: 12
# LOC: 68
def process_ticker_report(ticker: str) -> dict:
    """Generate complete ticker report"""
    # Fetch data (12 lines)
    info = yf.Ticker(ticker).info
    hist = yf.Ticker(ticker).history(period='1y')
    if hist.empty:
        logger.warning(f"No data for {ticker}")
        return None

    # Calculate indicators (18 lines)
    sma_20 = hist['Close'].rolling(20).mean()
    sma_50 = hist['Close'].rolling(50).mean()
    rsi = calculate_rsi(hist['Close'])
    macd = calculate_macd(hist['Close'])

    # Analyze trends (15 lines)
    current_price = hist['Close'].iloc[-1]
    is_uptrend = sma_20.iloc[-1] > sma_50.iloc[-1]
    is_oversold = rsi < 30
    is_overbought = rsi > 70

    # Generate report (23 lines)
    report = f"Analysis for {ticker}\n"
    report += f"Price: ${current_price:.2f}\n"
    if is_uptrend:
        report += "Trend: Bullish\n"
    else:
        report += "Trend: Bearish\n"
    # ... more report generation

    return {'report': report, 'indicators': {...}}
```

### After

```python
# Main function - Cyclomatic Complexity: 3, LOC: 12
def process_ticker_report(ticker: str) -> dict:
    """Generate complete ticker report (orchestrator)"""
    data = _fetch_ticker_data(ticker)
    if not data:
        return None

    indicators = _calculate_indicators(data)
    analysis = _analyze_trends(data, indicators)
    report_text = _generate_report_text(ticker, data, analysis)

    return {'report': report_text, 'indicators': indicators}

# Extracted methods - each CC: 2-4, LOC: 10-15
def _fetch_ticker_data(ticker: str) -> Optional[pd.DataFrame]:
    """Fetch historical data for ticker"""
    info = yf.Ticker(ticker).info
    hist = yf.Ticker(ticker).history(period='1y')

    if hist.empty:
        logger.warning(f"No data for {ticker}")
        return None

    return hist

def _calculate_indicators(data: pd.DataFrame) -> dict:
    """Calculate technical indicators"""
    return {
        'sma_20': data['Close'].rolling(20).mean(),
        'sma_50': data['Close'].rolling(50).mean(),
        'rsi': calculate_rsi(data['Close']),
        'macd': calculate_macd(data['Close']),
    }

def _analyze_trends(data: pd.DataFrame, indicators: dict) -> dict:
    """Analyze market trends"""
    current_price = data['Close'].iloc[-1]
    sma_20 = indicators['sma_20'].iloc[-1]
    sma_50 = indicators['sma_50'].iloc[-1]
    rsi = indicators['rsi']

    return {
        'current_price': current_price,
        'is_uptrend': sma_20 > sma_50,
        'is_oversold': rsi < 30,
        'is_overbought': rsi > 70,
    }

def _generate_report_text(ticker: str, data: pd.DataFrame, analysis: dict) -> str:
    """Generate report text from analysis"""
    trend = "Bullish" if analysis['is_uptrend'] else "Bearish"

    report = f"Analysis for {ticker}\n"
    report += f"Price: ${analysis['current_price']:.2f}\n"
    report += f"Trend: {trend}\n"
    # ... rest of report generation

    return report
```

**Benefits:**
- ✅ Each function has single responsibility
- ✅ Easier to test (test each step separately)
- ✅ Easier to read (self-documenting function names)
- ✅ Easier to modify (change one step without affecting others)

---

## Pattern 2: Simplify Conditionals

**When**: Cyclomatic complexity > 10, deep nesting

**Goal**: Reduce nested if/else, make logic clearer

### Before

```python
# Cyclomatic Complexity: 11
def should_buy_stock(price, sma_20, sma_50, rsi, macd):
    """Complex buy signal logic"""
    if price:
        if sma_20 and sma_50:
            if sma_20 > sma_50:
                if rsi:
                    if rsi < 30:
                        if macd:
                            if macd['histogram'] > 0:
                                return True
    return False
```

### After: Guard Clauses (Early Returns)

```python
# Cyclomatic Complexity: 7
def should_buy_stock(price, sma_20, sma_50, rsi, macd):
    """Simplified buy signal logic with guard clauses"""
    # Guard clauses - exit early for invalid inputs
    if not price:
        return False
    if not sma_20 or not sma_50:
        return False
    if sma_20 <= sma_50:  # Not in uptrend
        return False
    if not rsi or rsi >= 30:  # Not oversold
        return False
    if not macd or macd['histogram'] <= 0:  # MACD not bullish
        return False

    return True  # All conditions met
```

### After: Extract Condition to Function

```python
# Cyclomatic Complexity: 2 (per function)
def should_buy_stock(price, sma_20, sma_50, rsi, macd):
    """Buy signal logic with extracted conditions"""
    return (
        _has_valid_price(price)
        and _is_in_uptrend(sma_20, sma_50)
        and _is_oversold(rsi)
        and _has_bullish_macd(macd)
    )

def _has_valid_price(price):
    """Check if price is valid"""
    return price is not None and price > 0

def _is_in_uptrend(sma_20, sma_50):
    """Check if stock is in uptrend"""
    return sma_20 and sma_50 and sma_20 > sma_50

def _is_oversold(rsi):
    """Check if RSI indicates oversold"""
    return rsi and rsi < 30

def _has_bullish_macd(macd):
    """Check if MACD is bullish"""
    return macd and macd.get('histogram', 0) > 0
```

**Benefits:**
- ✅ Self-documenting (function names explain logic)
- ✅ Easier to test (test each condition separately)
- ✅ Easier to modify (change one condition without affecting others)

---

## Pattern 3: Replace Magic Numbers with Constants

**When**: Hardcoded numbers throughout code

**Goal**: Make values explicit and centralized

### Before

```python
def calculate_rsi(prices):
    """Calculate RSI with hardcoded period"""
    gain = prices.diff().clip(lower=0)
    loss = -prices.diff().clip(upper=0)

    avg_gain = gain.rolling(14).mean()  # Magic number!
    avg_loss = loss.rolling(14).mean()  # Magic number!

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def is_oversold(rsi):
    return rsi < 30  # Magic number!

def is_overbought(rsi):
    return rsi > 70  # Magic number!
```

### After

```python
# Constants at module level
RSI_PERIOD = 14
RSI_OVERSOLD_THRESHOLD = 30
RSI_OVERBOUGHT_THRESHOLD = 70

def calculate_rsi(prices, period=RSI_PERIOD):
    """Calculate RSI with configurable period"""
    gain = prices.diff().clip(lower=0)
    loss = -prices.diff().clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def is_oversold(rsi, threshold=RSI_OVERSOLD_THRESHOLD):
    """Check if RSI indicates oversold condition"""
    return rsi < threshold

def is_overbought(rsi, threshold=RSI_OVERBOUGHT_THRESHOLD):
    """Check if RSI indicates overbought condition"""
    return rsi > threshold
```

**Benefits:**
- ✅ Centralized configuration (change once, affects everywhere)
- ✅ Self-documenting (constant names explain purpose)
- ✅ Easier to test (can override thresholds in tests)

---

## Pattern 4: Introduce Parameter Object

**When**: Function has > 4 parameters

**Goal**: Group related parameters into object

### Before

```python
# Too many parameters (7!)
def generate_report(
    ticker: str,
    price: float,
    sma_20: float,
    sma_50: float,
    rsi: float,
    macd: dict,
    volume: int
) -> str:
    """Generate report with too many parameters"""
    trend = "Bullish" if sma_20 > sma_50 else "Bearish"

    report = f"{ticker}: ${price:.2f}\n"
    report += f"Trend: {trend}\n"
    report += f"RSI: {rsi:.1f}\n"
    # ...
    return report
```

### After

```python
from dataclasses import dataclass

@dataclass
class MarketData:
    """Parameter object for market data"""
    ticker: str
    price: float
    sma_20: float
    sma_50: float
    rsi: float
    macd: dict
    volume: int

    @property
    def trend(self) -> str:
        """Derived property: bullish or bearish"""
        return "Bullish" if self.sma_20 > self.sma_50 else "Bearish"

    @property
    def is_oversold(self) -> bool:
        """Derived property: RSI oversold"""
        return self.rsi < 30

# Simplified function signature
def generate_report(data: MarketData) -> str:
    """Generate report from market data object"""
    report = f"{data.ticker}: ${data.price:.2f}\n"
    report += f"Trend: {data.trend}\n"
    report += f"RSI: {data.rsi:.1f}\n"
    # ...
    return report
```

**Benefits:**
- ✅ Fewer parameters (1 instead of 7)
- ✅ Grouped related data
- ✅ Can add derived properties
- ✅ Type-safe with dataclass

---

## Pattern 5: Extract Class

**When**: Class has > 500 LOC or multiple responsibilities

**Goal**: Separate concerns into focused classes

### Before

```python
# God class - does everything (850 LOC)
class TickerAnalyzer:
    """Analyzes tickers, fetches data, generates reports, scores reports"""

    def fetch_data(self, ticker):
        # 80 lines of data fetching logic
        ...

    def calculate_indicators(self, data):
        # 120 lines of indicator calculation
        ...

    def fetch_news(self, ticker):
        # 90 lines of news fetching logic
        ...

    def analyze_fundamentals(self, data):
        # 110 lines of fundamental analysis
        ...

    def generate_report(self, data, indicators, news):
        # 200 lines of report generation
        ...

    def score_report(self, report):
        # 150 lines of scoring logic
        ...

    def cache_results(self, ticker, report):
        # 100 lines of caching logic
        ...
```

### After

```python
# Separated concerns - each class has single responsibility

class TickerDataFetcher:
    """Fetches ticker data from external sources (100 LOC)"""

    def fetch_price_data(self, ticker):
        ...

    def fetch_fundamental_data(self, ticker):
        ...

class TechnicalAnalyzer:
    """Calculates technical indicators (150 LOC)"""

    def calculate_sma(self, prices, period):
        ...

    def calculate_rsi(self, prices):
        ...

    def calculate_macd(self, prices):
        ...

class NewsService:
    """Fetches and processes news (120 LOC)"""

    def fetch_news(self, ticker):
        ...

    def filter_relevant_news(self, news, ticker):
        ...

class ReportGenerator:
    """Generates reports from analysis (250 LOC)"""

    def generate_technical_section(self, indicators):
        ...

    def generate_fundamental_section(self, data):
        ...

    def generate_news_section(self, news):
        ...

class ReportScorer:
    """Scores report quality (180 LOC)"""

    def score_faithfulness(self, report, data):
        ...

    def score_completeness(self, report):
        ...

class ReportCache:
    """Caches generated reports (130 LOC)"""

    def get(self, ticker):
        ...

    def set(self, ticker, report):
        ...

# Orchestrator - coordinates classes
class TickerAnalyzer:
    """Orchestrates ticker analysis workflow (50 LOC)"""

    def __init__(self):
        self.fetcher = TickerDataFetcher()
        self.analyzer = TechnicalAnalyzer()
        self.news_service = NewsService()
        self.report_gen = ReportGenerator()
        self.scorer = ReportScorer()
        self.cache = ReportCache()

    def analyze(self, ticker):
        """Main workflow - delegates to specialized classes"""
        data = self.fetcher.fetch_price_data(ticker)
        indicators = self.analyzer.calculate_all(data)
        news = self.news_service.fetch_news(ticker)
        report = self.report_gen.generate(data, indicators, news)
        score = self.scorer.score(report, data)
        self.cache.set(ticker, report)
        return report
```

**Benefits:**
- ✅ Each class has single responsibility (SRP)
- ✅ Easier to test (test each class separately)
- ✅ Easier to modify (change one class without affecting others)
- ✅ Reusable components (use NewsService elsewhere)

---

## Pattern 6: Guard Clauses (Early Returns)

**When**: Deep nesting (> 3 levels), cognitive complexity > 15

**Goal**: Flatten structure, improve readability

### Before

```python
# Deeply nested (cognitive complexity: 18)
def process_order(order):
    result = None
    if order:
        if order.is_valid():
            if order.customer:
                if order.customer.has_credit():
                    if order.items:
                        for item in order.items:
                            if item.in_stock():
                                item.ship()
                            else:
                                result = "Item out of stock"
                    else:
                        result = "No items"
                else:
                    result = "No credit"
            else:
                result = "No customer"
        else:
            result = "Invalid order"
    else:
        result = "No order"
    return result
```

### After

```python
# Flattened with guard clauses (cognitive complexity: 7)
def process_order(order):
    # Guard clauses - exit early for errors
    if not order:
        return "No order"

    if not order.is_valid():
        return "Invalid order"

    if not order.customer:
        return "No customer"

    if not order.customer.has_credit():
        return "No credit"

    if not order.items:
        return "No items"

    # Happy path - no nesting
    for item in order.items:
        if not item.in_stock():
            return "Item out of stock"
        item.ship()

    return "Success"
```

**Benefits:**
- ✅ Reduced nesting (1 level instead of 6)
- ✅ Easier to read (happy path at end, not buried)
- ✅ Reduced cognitive complexity (18 → 7)

---

## Pattern 7: Replace Conditional with Polymorphism

**When**: Large switch/if-elif chain, strategy pattern needed

**Goal**: Use inheritance/polymorphism instead of conditionals

### Before

```python
# Large if-elif chain (cyclomatic complexity: 8)
def calculate_shipping(order_type, weight):
    if order_type == "standard":
        if weight < 5:
            return 5.00
        else:
            return 5.00 + (weight - 5) * 0.50
    elif order_type == "express":
        if weight < 5:
            return 10.00
        else:
            return 10.00 + (weight - 5) * 1.00
    elif order_type == "overnight":
        if weight < 5:
            return 20.00
        else:
            return 20.00 + (weight - 5) * 2.00
    else:
        return 0
```

### After

```python
# Polymorphic strategy (cyclomatic complexity: 2 per class)
from abc import ABC, abstractmethod

class ShippingStrategy(ABC):
    """Abstract base class for shipping strategies"""

    @abstractmethod
    def calculate_cost(self, weight: float) -> float:
        pass

class StandardShipping(ShippingStrategy):
    BASE_RATE = 5.00
    RATE_PER_KG = 0.50
    FREE_WEIGHT = 5.0

    def calculate_cost(self, weight: float) -> float:
        if weight <= self.FREE_WEIGHT:
            return self.BASE_RATE
        return self.BASE_RATE + (weight - self.FREE_WEIGHT) * self.RATE_PER_KG

class ExpressShipping(ShippingStrategy):
    BASE_RATE = 10.00
    RATE_PER_KG = 1.00
    FREE_WEIGHT = 5.0

    def calculate_cost(self, weight: float) -> float:
        if weight <= self.FREE_WEIGHT:
            return self.BASE_RATE
        return self.BASE_RATE + (weight - self.FREE_WEIGHT) * self.RATE_PER_KG

class OvernightShipping(ShippingStrategy):
    BASE_RATE = 20.00
    RATE_PER_KG = 2.00
    FREE_WEIGHT = 5.0

    def calculate_cost(self, weight: float) -> float:
        if weight <= self.FREE_WEIGHT:
            return self.BASE_RATE
        return self.BASE_RATE + (weight - self.FREE_WEIGHT) * self.RATE_PER_KG

# Factory for creating strategies
SHIPPING_STRATEGIES = {
    "standard": StandardShipping,
    "express": ExpressShipping,
    "overnight": OvernightShipping,
}

def calculate_shipping(order_type: str, weight: float) -> float:
    """Calculate shipping cost using strategy pattern"""
    strategy_class = SHIPPING_STRATEGIES.get(order_type)
    if not strategy_class:
        return 0

    strategy = strategy_class()
    return strategy.calculate_cost(weight)
```

**Benefits:**
- ✅ Open/Closed Principle (add new strategies without modifying existing code)
- ✅ Each strategy independently testable
- ✅ No complex conditionals
- ✅ Easier to add new shipping types

---

## Quick Reference: Refactoring Decision Tree

```
What's the problem?
├─ Tight coupling (connascence)?
│  ├─ CoV (shared values)? → Event-Driven Architecture
│  ├─ CoE (execution order)? → Encapsulate Order
│  ├─ CoP (positional params)? → Named Parameters
│  └─ CoM (magic numbers)? → Named Constants
│
├─ Function too long (> 50 LOC)
│  └─ Extract Method
│
├─ Too many parameters (> 4)
│  └─ Introduce Parameter Object (also fixes CoP!)
│
├─ Complex conditionals (CC > 10)
│  ├─ Deep nesting? → Guard Clauses
│  ├─ Long if-elif chain? → Polymorphism
│  └─ Unclear logic? → Extract Condition
│
├─ Duplicated code
│  └─ Extract Common Logic
│
├─ Class too large (> 500 LOC)
│  └─ Extract Class (separate concerns)
│
└─ Magic numbers
   └─ Replace with Constants (also fixes CoM!)
```

**Refactoring Priority**:
1. **Connascence** (fix strongest first: CoV > CoE > CoM > CoP)
2. **Hotspots** (high churn + high complexity)
3. **Complexity** (CC > 10, cognitive > 15)
4. **Code smells** (long functions, God classes)

---

## References

- **Refactoring (2nd Edition)** by Martin Fowler - Comprehensive catalog
- **Fundamentals of Software Architecture** by Mark Richards & Neal Ford - Connascence
- **Clean Code** by Robert C. Martin - Code quality principles
- **Complexity Metrics**: See [CODE-COMPLEXITY.md](CODE-COMPLEXITY.md)
- **Hotspot Analysis**: See [HOTSPOT-ANALYSIS.md](HOTSPOT-ANALYSIS.md)
