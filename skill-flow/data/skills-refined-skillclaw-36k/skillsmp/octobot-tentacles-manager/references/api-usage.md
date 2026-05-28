# API Usage

## Installation

```python
from octobot_tentacles_manager.api import install_tentacles

await install_tentacles(
    tentacles_path="tentacles",
    tentacle_package_url="https://example.com/package.zip"
)
```

## Listing

```python
from octobot_tentacles_manager.api import get_installed_tentacles

tentacles = await get_installed_tentacles("tentacles")
for t in tentacles:
    print(f"{t.name} v{t.version}")
```

## Package Creation

```python
from octobot_tentacles_manager.api import create_tentacles_package

await create_tentacles_package(
    tentacles_folder="./OctoBot-Tentacles",
    output_file="package.zip"
)
```

## Configuration

```python
from octobot_tentacles_manager.api import get_tentacle_config

config = await get_tentacle_config("binance", "tentacles")
```
