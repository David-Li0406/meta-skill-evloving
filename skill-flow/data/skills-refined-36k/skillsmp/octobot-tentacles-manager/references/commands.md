# Commands

## Install Commands

```bash
# Install all tentacles
python start.py tentacles --install --all

# Install specific tentacles
python start.py tentacles --install binance rsi_evaluator

# Install from URL
python start.py tentacles --install --url https://example.com/package.zip
```

## Update Commands

```bash
# Update all
python start.py tentacles --update --all

# Update specific
python start.py tentacles --update binance
```

## List Commands

```bash
# List installed
python start.py tentacles --list

# List available
python start.py tentacles --list --available
```

## Package Creation

```bash
# Export tentacles
python start.py tentacles -p output.zip -d ./OctoBot-Tentacles
```
