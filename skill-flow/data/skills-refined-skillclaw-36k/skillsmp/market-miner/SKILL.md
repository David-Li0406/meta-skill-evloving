---
name: market_miner
description: Scrapes product data from provider websites (CDR) and updates the market database.
---

# Market Miner Skill

This skill is responsible for extracting product information from target supplier websites.

## Capabilities

- Scrape full categories from CDR Medios.
- Extract product details (Name, Price, Stock, URL).
- Save data to `CDR_MASTER_DB.csv` (legacy mode) or `market.db`.

## Usage

```python
from src.skills.market_miner.miner import minar_categoria_completa

minar_categoria_completa("https://url...", "Categoria")
```

## Configuration

Requires `CDR_FULL_COOKIE` in `.env`.
