# platformdirs - Cross-Platform Directory Handling

## Overview

`platformdirs` provides XDG-compliant directory paths across platforms. Use it instead of hardcoding paths like `~/.local/var/log/`.

## Installation

```bash
uv add platformdirs
# or
pip install platformdirs
```

## Log Directories

```python
import platformdirs
from pathlib import Path

# Get OS-specific log directory
log_dir = Path(platformdirs.user_log_dir(
    appname="my-app",
    ensure_exists=True  # Create if missing
))
```

**Platform paths**:

| Platform | Path                                         |
| -------- | -------------------------------------------- |
| macOS    | `~/Library/Logs/my-app/`                     |
| Linux    | `~/.local/state/my-app/log/`                 |
| Windows  | `C:\Users\<user>\AppData\Local\my-app\Logs\` |

## Other Useful Directories

```python
# Configuration files
config_dir = platformdirs.user_config_dir("my-app")
# macOS: ~/Library/Application Support/my-app
# Linux: ~/.config/my-app

# Cache files
cache_dir = platformdirs.user_cache_dir("my-app")
# macOS: ~/Library/Caches/my-app
# Linux: ~/.cache/my-app

# Data files
data_dir = platformdirs.user_data_dir("my-app")
# macOS: ~/Library/Application Support/my-app
# Linux: ~/.local/share/my-app

# State files (runtime state, not config)
state_dir = platformdirs.user_state_dir("my-app")
# macOS: ~/Library/Application Support/my-app
# Linux: ~/.local/state/my-app
```

## Best Practices

1. **Always use `ensure_exists=True`** - Creates directory if missing
2. **Use `appname` parameter** - Keeps logs organized by application
3. **Convert to Path** - `Path(platformdirs.user_log_dir(...))` for pathlib operations
4. **Don't hardcode** - Never use `~/.local/var/log/` directly

## Example: Complete Logger Setup

```python
import platformdirs
from loguru import logger
from pathlib import Path

def setup_logging(app_name: str):
    log_dir = Path(platformdirs.user_log_dir(
        appname=app_name,
        ensure_exists=True
    ))

    logger.add(
        str(log_dir / f"{app_name}.jsonl"),
        rotation="10 MB",
        retention="7 days",
        compression="gz"
    )

    return log_dir  # Return for debugging
```
