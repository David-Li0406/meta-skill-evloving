# Package Format

## Structure

```
package.zip
├── Trading/Exchange/binance/
│   ├── __init__.py
│   ├── binance_exchange.py
│   └── metadata.json
├── Evaluator/TA/rsi/
└── metadata.json
```

## Package Metadata

```json
{
    "name": "My-Tentacles",
    "version": "1.0.0",
    "tentacles": ["binance", "rsi_evaluator"]
}
```

## Tentacle Metadata

```json
{
    "version": "1.0.0",
    "origin_package": "OctoBot-Default-Tentacles",
    "tentacles": ["Binance"],
    "requirements": [],
    "tentacles-requirements": []
}
```
