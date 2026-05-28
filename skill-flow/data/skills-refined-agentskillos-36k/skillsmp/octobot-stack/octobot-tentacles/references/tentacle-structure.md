# Tentacle Structure

## Directory Layout

### Standard Tentacle
```
my_tentacle/
├── __init__.py              # Exports tentacle class
├── my_tentacle.py           # Main implementation
├── metadata.json            # Tentacle metadata
├── resources/               # Optional: icons, configs
│   ├── icon.png
│   └── default_config.json
└── tests/                   # Test files
    ├── __init__.py
    └── test_my_tentacle.py
```

### Complex Tentacle (Multiple Files)
```
advanced_strategy/
├── __init__.py
├── advanced_strategy.py     # Main class
├── indicators.py            # Helper module
├── risk_manager.py          # Risk management
├── metadata.json
├── resources/
│   ├── presets/
│   └── templates/
└── tests/
    ├── test_strategy.py
    └── test_risk_manager.py
```

## metadata.json Schema

### Minimal Metadata
```json
{
    "version": "1.0.0",
    "origin_package": "OctoBot-Default-Tentacles",
    "tentacles": ["MyTentacle"]
}
```

### Complete Metadata
```json
{
    "version": "2.1.0",
    "origin_package": "OctoBot-Default-Tentacles",
    "tentacles": ["AdvancedStrategy"],
    "tentacles-requirements": ["RSI", "MACD"],
    "requirements": ["pandas>=1.3.0", "numpy>=1.21.0"],
    "config-files": ["resources/default_config.json"],
    "config-schema-files": ["resources/config_schema.json"]
}
```

### Metadata Fields

- **version**: Semantic version (major.minor.patch)
- **origin_package**: Source package name (always "OctoBot-Default-Tentacles" for this repo)
- **tentacles**: List of tentacle class names exported
- **tentacles-requirements**: Other tentacles this depends on
- **requirements**: Python package dependencies
- **config-files**: Default configuration files
- **config-schema-files**: JSON schema for validation

## __init__.py Pattern

### Single Tentacle
```python
from .my_tentacle import MyTentacle

__all__ = ["MyTentacle"]
```

### Multiple Tentacles
```python
from .strategy_a import StrategyA
from .strategy_b import StrategyB
from .base_strategy import BaseStrategy

__all__ = ["StrategyA", "StrategyB", "BaseStrategy"]
```

## Requirements

### Python Dependencies
Add to metadata.json:
```json
{
    "requirements": [
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0"
    ]
}
```

### Tentacle Dependencies
Specify other required tentacles:
```json
{
    "tentacles-requirements": [
        "Binance",
        "RSIEvaluator",
        "MovingAverageStrategy"
    ]
}
```

## Resource Files

### Default Configuration
```json
// resources/default_config.json
{
    "period": 14,
    "overbought": 70,
    "oversold": 30,
    "enabled": true
}
```

### Configuration Schema
```json
// resources/config_schema.json
{
    "type": "object",
    "properties": {
        "period": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
        },
        "overbought": {
            "type": "number",
            "minimum": 50,
            "maximum": 100
        }
    }
}
```

## Naming Conventions

- **Directory**: lowercase_with_underscores
- **Class**: PascalCase
- **Files**: match directory name (lowercase_with_underscores.py)
- **Tests**: test_*.py
