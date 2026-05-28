---
name: market_appraiser
description: Appraises products by searching for competitive prices on MercadoLibre Uruguay using Playwright.
---

# Market Appraiser Skill

This skill uses Playwright to scrape MercadoLibre Uruguay and find the minimum market price for a given product to determine competitive pricing.

## Capabilities

- Smart query generation (cleans titles).
- Filter application (avoids comparing Basic vs Pro models).
- Price extraction and comparison.
- Alert generation (Opportunity, High Price, OK).

## Usage

```python
from src.skills.market_appraiser.appraiser import obtener_precio_ml, generar_query_inteligente

price = obtener_precio_ml("Monitor Gamer 144hz")
```

## Dependencies

- `playwright`
- `pandas`
