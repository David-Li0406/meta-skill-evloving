# Python Usage (Market Data, Account, Positions, Orders)

Use this for quick imports and examples. For full field definitions, read `ibkr_core/models.py` and `docs/SCHEMAS.md`.

## Imports

```python
from ibkr_core.client import IBKRClient
from ibkr_core.simulation import get_ibkr_client
from ibkr_core.models import SymbolSpec, OrderSpec
from ibkr_core.market_data import (
    QuoteMode,
    get_quote,
    get_quotes,
    get_quote_with_mode,
    get_historical_bars,
    get_streaming_quote,
)
from ibkr_core.account import (
    get_account_summary,
    get_positions,
    get_pnl,
    get_account_status,
    list_managed_accounts,
)
from ibkr_core.orders import (
    preview_order,
    place_order,
    get_order_status,
    cancel_order,
    get_open_orders,
    cancel_order_set,
)
```

## Account Summary and Positions

```python
client = IBKRClient(mode="paper")
client.connect()

summary = get_account_summary(client)
positions = get_positions(client)

client.disconnect()
```

## Market Data (Snapshot)

```python
client = IBKRClient(mode="paper")
client.connect()

spec = SymbolSpec(symbol="AAPL", securityType="STK", exchange="SMART", currency="USD")
quote = get_quote(spec, client)
bars = get_historical_bars(spec, client, bar_size="1d", duration="5d", what_to_show="TRADES")

client.disconnect()
```

## Market Data (Streaming)

```python
client = IBKRClient(mode="paper")
client.connect()

spec = SymbolSpec(symbol="AAPL", securityType="STK")
stream = get_streaming_quote(spec, client)
with stream:
    for update in stream.updates(max_updates=5):
        print(update.bid, update.ask)

client.disconnect()
```

## Order Preview and Placement

```python
client = IBKRClient(mode="paper")
client.connect()

order_spec = OrderSpec(
    instrument=SymbolSpec(symbol="AAPL", securityType="STK", exchange="SMART", currency="USD"),
    side="BUY",
    quantity=10,
    orderType="LMT",
    limitPrice=150.00,
)

preview = preview_order(client, order_spec)
result = place_order(client, order_spec)

client.disconnect()
```

## Simulation Mode (Optional)

Use this to avoid IBKR connectivity during testing:

```python
client = get_ibkr_client(mode="simulation")
client.connect()

summary = get_account_summary(client)

client.disconnect()
```
