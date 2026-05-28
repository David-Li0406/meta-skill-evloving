# Testing

## Testing Philosophy

OctoBot-Trading uses `pytest` for comprehensive test coverage across:
- Unit tests for individual components
- Integration tests for exchange connections
- Async tests for trading operations
- Mock tests for external dependencies

**Coverage goal**: >80% for core modules

---

## Test Structure

### Directory Layout
```
octobot_trading/
├── exchanges/
│   ├── abstract_exchange.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py         # Fixtures
│       └── test_exchanges.py
├── personal_data/
│   ├── orders/
│   │   ├── order.py
│   │   └── tests/
│   │       ├── conftest.py
│   │       └── test_order.py
│   └── portfolio/
│       ├── portfolio.py
│       └── tests/
└── tests/                       # Top-level integration tests
    ├── conftest.py
    └── test_integration.py
```

---

## Pytest Basics

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest octobot_trading/exchanges/tests/test_exchanges.py

# Run specific test
pytest octobot_trading/exchanges/tests/test_exchanges.py::test_exchange_initialization

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=octobot_trading --cov-report=html
```

### Test Discovery
Pytest automatically discovers:
- Files named `test_*.py` or `*_test.py`
- Functions named `test_*`
- Classes named `Test*`

---

## Fixtures

### Basic Fixtures
```python
import pytest

@pytest.fixture
def mock_config():
    """Mock exchange configuration"""
    return {
        'api_key': 'test_key',
        'api_secret': 'test_secret',
        'exchange_name': 'binance',
        'simulated': True
    }

@pytest.fixture
def mock_exchange_manager(mock_config):
    """Mock exchange manager"""
    from octobot_trading.exchanges import ExchangeManager
    return ExchangeManager(mock_config, 'binance')
```

### Async Fixtures
```python
import pytest
import asyncio

@pytest.fixture
async def initialized_exchange(mock_exchange_manager):
    """Initialized exchange instance"""
    exchange = mock_exchange_manager.exchange
    await exchange.initialize()
    yield exchange
    await exchange.stop()
```

### Parameterized Fixtures
```python
@pytest.fixture(params=['binance', 'coinbase', 'kraken'])
def exchange_name(request):
    """Test multiple exchanges"""
    return request.param

def test_exchange_creation(exchange_name):
    from octobot_trading.exchanges import create_exchange
    exchange = create_exchange(exchange_name)
    assert exchange.get_name() == exchange_name.lower()
```

### Shared Fixtures (conftest.py)
```python
# octobot_trading/tests/conftest.py
import pytest
from unittest.mock import AsyncMock, Mock

@pytest.fixture
def mock_ccxt_exchange():
    """Mock CCXT exchange client"""
    mock = AsyncMock()
    mock.fetch_balance.return_value = {
        'BTC': {'free': 1.0, 'used': 0.0, 'total': 1.0},
        'USDT': {'free': 10000.0, 'used': 0.0, 'total': 10000.0}
    }
    mock.fetch_ticker.return_value = {
        'symbol': 'BTC/USDT',
        'last': 50000.0,
        'bid': 49999.0,
        'ask': 50001.0
    }
    return mock
```

---

## Async Testing

### Basic Async Tests
```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_operation():
    """Test async function"""
    result = await some_async_function()
    assert result == expected_value
```

### Async Fixtures
```python
@pytest.fixture
async def async_resource():
    """Setup and teardown async resource"""
    resource = await create_resource()
    yield resource
    await resource.cleanup()

@pytest.mark.asyncio
async def test_with_async_fixture(async_resource):
    result = await async_resource.do_something()
    assert result is not None
```

### Testing Concurrent Operations
```python
@pytest.mark.asyncio
async def test_concurrent_orders():
    """Test creating multiple orders concurrently"""
    order_manager = OrderManager(mock_trader)
    
    # Create orders concurrently
    tasks = [
        order_manager.create_order('limit', 'buy', 'BTC/USDT', 1.0, 49000),
        order_manager.create_order('limit', 'sell', 'BTC/USDT', 1.0, 51000)
    ]
    orders = await asyncio.gather(*tasks)
    
    assert len(orders) == 2
    assert orders[0].side == 'buy'
    assert orders[1].side == 'sell'
```

---

## Mocking

### Mock Objects
```python
from unittest.mock import Mock, AsyncMock, MagicMock

def test_order_creation():
    """Test order creation with mocked trader"""
    mock_trader = Mock()
    mock_trader.exchange = Mock()
    
    order = Order(mock_trader)
    order.initialize('limit', 'buy', 'BTC/USDT', 1.0, 50000)
    
    assert order.side == 'buy'
    assert order.amount == 1.0
```

### Mock Async Functions
```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_exchange_balance():
    """Test balance fetching with mocked exchange"""
    mock_exchange = AsyncMock()
    mock_exchange.fetch_balance.return_value = {
        'BTC': {'free': 1.0, 'used': 0.0, 'total': 1.0}
    }
    
    balance = await mock_exchange.fetch_balance()
    assert balance['BTC']['total'] == 1.0
    mock_exchange.fetch_balance.assert_called_once()
```

### Patch Decorators
```python
from unittest.mock import patch

@patch('octobot_trading.exchanges.ccxt_connector.ccxt')
def test_ccxt_initialization(mock_ccxt):
    """Test CCXT connector initialization"""
    mock_ccxt.binance.return_value = Mock()
    
    connector = CCXTConnector({'api_key': 'test'}, mock_exchange_manager)
    connector.initialize()
    
    mock_ccxt.binance.assert_called_once()
```

---

## Testing Exchange Operations

### Test Balance Fetching
```python
@pytest.mark.asyncio
async def test_fetch_balance(initialized_exchange, mock_ccxt_exchange):
    """Test balance fetching"""
    initialized_exchange.connector.client = mock_ccxt_exchange
    
    balance = await initialized_exchange.fetch_balance()
    
    assert 'BTC' in balance
    assert balance['BTC']['total'] == 1.0
    assert 'USDT' in balance
```

### Test Order Creation
```python
@pytest.mark.asyncio
async def test_create_order(initialized_exchange, mock_ccxt_exchange):
    """Test order creation"""
    mock_ccxt_exchange.create_order.return_value = {
        'id': '12345',
        'status': 'open',
        'type': 'limit',
        'side': 'buy',
        'symbol': 'BTC/USDT',
        'amount': 1.0,
        'price': 50000.0,
        'filled': 0.0,
        'remaining': 1.0
    }
    
    initialized_exchange.connector.client = mock_ccxt_exchange
    
    order = await initialized_exchange.create_order(
        'limit', 'buy', 'BTC/USDT', 1.0, 50000.0
    )
    
    assert order['id'] == '12345'
    assert order['status'] == 'open'
    mock_ccxt_exchange.create_order.assert_called_once_with(
        'BTC/USDT', 'limit', 'buy', 1.0, 50000.0, {}
    )
```

### Test Error Handling
```python
from ccxt import NetworkError

@pytest.mark.asyncio
async def test_network_error_handling(initialized_exchange, mock_ccxt_exchange):
    """Test handling of network errors"""
    mock_ccxt_exchange.fetch_balance.side_effect = NetworkError("Connection failed")
    initialized_exchange.connector.client = mock_ccxt_exchange
    
    with pytest.raises(NetworkError):
        await initialized_exchange.fetch_balance()
```

---

## Testing Orders

### Test Order Lifecycle
```python
@pytest.mark.asyncio
async def test_order_lifecycle():
    """Test complete order lifecycle"""
    mock_trader = Mock()
    order = Order(mock_trader)
    
    # Initialize
    await order.initialize('limit', 'buy', 'BTC/USDT', 1.0, 50000)
    assert order.status == 'open'
    
    # Update to filled
    await order.update({
        'id': '123',
        'status': 'closed',
        'filled': 1.0,
        'remaining': 0.0
    })
    assert order.status == 'closed'
    assert order.filled == 1.0
```

### Test Order Manager
```python
@pytest.mark.asyncio
async def test_order_manager_create_order(mock_trader):
    """Test order manager order creation"""
    order_manager = OrderManager(mock_trader)
    mock_trader.exchange.create_order = AsyncMock(return_value={
        'id': '123',
        'status': 'open',
        'filled': 0.0,
        'remaining': 1.0
    })
    
    order = await order_manager.create_order(
        order_type='limit',
        side='buy',
        symbol='BTC/USDT',
        amount=1.0,
        price=50000
    )
    
    assert order.order_id == '123'
    assert '123' in order_manager.orders
```

---

## Testing Portfolio

### Test Portfolio Updates
```python
@pytest.mark.asyncio
async def test_portfolio_update(mock_trader):
    """Test portfolio balance updates"""
    portfolio = Portfolio(mock_trader)
    mock_trader.exchange.fetch_balance = AsyncMock(return_value={
        'BTC': {'free': 1.0, 'used': 0.5, 'total': 1.5},
        'USDT': {'free': 10000.0, 'used': 5000.0, 'total': 15000.0}
    })
    
    await portfolio.update_portfolio_balance()
    
    btc_portfolio = portfolio.get_currency_portfolio('BTC')
    assert btc_portfolio['total'] == 1.5
    assert btc_portfolio['free'] == 1.0
```

### Test PNL Calculation
```python
def test_pnl_calculation():
    """Test profit/loss calculation"""
    portfolio = Portfolio(mock_trader)
    portfolio.initial_portfolio = {
        'USDT': {'total': 10000.0}
    }
    portfolio.portfolio = {
        'USDT': {'total': 12000.0}
    }
    
    pnl = portfolio.calculate_pnl('USDT')
    assert pnl == 2000.0
```

---

## Parameterized Tests

### Multiple Inputs
```python
@pytest.mark.parametrize("order_type,side,expected_status", [
    ('market', 'buy', 'closed'),
    ('limit', 'buy', 'open'),
    ('market', 'sell', 'closed'),
    ('limit', 'sell', 'open'),
])
@pytest.mark.asyncio
async def test_order_types(order_type, side, expected_status):
    """Test different order types"""
    order = Order(mock_trader)
    await order.initialize(order_type, side, 'BTC/USDT', 1.0, 50000)
    # Simulate exchange response
    assert order.status in ['open', 'closed']
```

### Multiple Exchanges
```python
@pytest.mark.parametrize("exchange_name", [
    'binance', 'coinbase', 'kraken'
])
def test_exchange_creation(exchange_name):
    """Test exchange creation for multiple exchanges"""
    config = {'exchange_name': exchange_name, 'simulated': True}
    exchange_manager = ExchangeManager(config, exchange_name)
    assert exchange_manager.exchange_name == exchange_name
```

---

## Coverage

### Measure Coverage
```bash
pytest --cov=octobot_trading --cov-report=term-missing
```

### Generate HTML Report
```bash
pytest --cov=octobot_trading --cov-report=html
open htmlcov/index.html
```

### Coverage Configuration
```ini
# .coveragerc or pyproject.toml
[coverage:run]
source = octobot_trading
omit = 
    */tests/*
    */test_*.py
    */__pycache__/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

---

## Integration Tests

### Test Full Trading Workflow
```python
@pytest.mark.asyncio
async def test_full_trading_workflow():
    """Test complete trading workflow"""
    # Setup
    config = {'exchange_name': 'binance', 'simulated': True}
    exchange_manager = ExchangeManager(config, 'binance')
    await exchange_manager.initialize()
    
    # Fetch balance
    balance = await exchange_manager.exchange.fetch_balance()
    assert 'USDT' in balance
    
    # Create order
    order = await exchange_manager.exchange.create_order(
        'limit', 'buy', 'BTC/USDT', 0.1, 50000
    )
    assert order['id'] is not None
    
    # Fetch order status
    order_status = await exchange_manager.exchange.fetch_order(order['id'])
    assert order_status['status'] in ['open', 'closed']
    
    # Cleanup
    await exchange_manager.stop()
```

---

## Best Practices

### 1. Test Independence
Each test should be independent:
```python
# ✅ Good - uses fixtures
@pytest.mark.asyncio
async def test_order_creation(mock_trader):
    order = Order(mock_trader)
    await order.initialize('limit', 'buy', 'BTC/USDT', 1.0, 50000)
    assert order.status == 'open'

# ❌ Bad - relies on global state
global_order = None

def test_order_creation():
    global global_order
    global_order = Order(mock_trader)
```

### 2. Mock External Dependencies
```python
# ✅ Good - mocks exchange API
@patch('ccxt.binance')
async def test_with_mock(mock_exchange):
    mock_exchange.fetch_balance.return_value = {...}

# ❌ Bad - makes real API calls
async def test_without_mock():
    exchange = ccxt.binance({'apiKey': 'real_key'})
    balance = await exchange.fetch_balance()
```

### 3. Clear Test Names
```python
# ✅ Good - describes what is tested
def test_order_creation_with_valid_parameters()
def test_order_creation_fails_with_insufficient_balance()

# ❌ Bad - vague names
def test1()
def test_order()
```

### 4. Arrange-Act-Assert Pattern
```python
def test_portfolio_update():
    # Arrange
    portfolio = Portfolio(mock_trader)
    initial_balance = 10000.0
    
    # Act
    portfolio.update_balance('USDT', 15000.0)
    
    # Assert
    assert portfolio.get_balance('USDT') == 15000.0
```
