# NomadNet Page Structure

Comprehensive guide to NomadNet page configuration, headers, and organization.

## Storage Locations

### Default Paths

| Type | Default Path | Configurable Via |
|------|--------------|------------------|
| Pages | `~/.nomadnetwork/storage/pages/` | `pages_path` in config |
| Files | `~/.nomadnetwork/storage/files/` | `files_path` in config |

### Directory Mapping

Subdirectories automatically map to URL paths:

```
~/.nomadnetwork/storage/pages/
├── index.mu              → :/page/index.mu
├── about.mu              → :/page/about.mu
├── docs/
│   ├── guide.mu          → :/page/docs/guide.mu
│   └── api.mu            → :/page/docs/api.mu
└── apps/
    └── calculator.mu     → :/page/apps/calculator.mu
```

### Default Page

`index.mu` is served when a peer connects without specifying a path.

## Page Headers

Headers must appear at the very top of `.mu` files, before any content.

### Cache Control

```micron
#!c=3600
```

| Value | Behavior |
|-------|----------|
| `#!c=0` | Never cache (always fetch fresh) |
| `#!c=3600` | Cache for 1 hour |
| `#!c=43200` | Cache for 12 hours (default if not specified) |
| `#!c=86400` | Cache for 24 hours |

**Important:** Cache control header must be the first line if present.

### Page Colors

Set default foreground and background colors:

```micron
#!fg=ddd
#!bg=222
```

**Important:** Color headers must come after cache control if both are present.

### Complete Header Example

```micron
#!c=300
#!fg=ddd
#!bg=333
>My Page Title
```

## Static Pages

### Basic Static Page

```micron
#!c=3600
>Welcome

`cWelcome to this NomadNet node!
`a

>>About
This page provides information about our services.

>>Contact
Send a message to: `[lxmf@e9eafceea9e3664a5c55611c5e8c420a]
```

### Organization Tips

1. **Use index.mu as entry point**: Link to other pages from here
2. **Group related pages in subdirectories**: `/page/docs/`, `/page/apps/`
3. **Set appropriate cache times**: Static content can cache longer
4. **Include navigation links**: Help users explore your node

## Dynamic Pages

### Making Pages Executable

```bash
chmod +x ~/.nomadnetwork/storage/pages/status.mu
```

### Python Dynamic Page

```python
#!/usr/bin/env python3
import os
import time

# Output cache header first
print("#!c=0")

# Generate Micron content
print(">Server Status")
print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("")

# Access form data
username = os.environ.get('field_username', 'Guest')
print(f"Hello, {username}!")
```

### Bash Dynamic Page

```bash
#!/bin/bash

echo "#!c=0"
echo ">System Information"
echo ""
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"
echo "Load: $(cat /proc/loadavg | cut -d' ' -f1-3)"
```

### PHP Dynamic Page

```php
#!/usr/bin/env php
<?php
echo "#!c=0\n";
echo ">Dynamic Content\n\n";
echo "Generated at: " . date('Y-m-d H:i:s') . "\n";

$name = getenv('field_name') ?: 'Anonymous';
echo "\nHello, `!{$name}`!\n";
?>
```

## Environment Variables

Form data is passed to dynamic pages as environment variables.

### Field Data

Fields from forms use `field_` prefix:

| Field Name | Environment Variable |
|------------|---------------------|
| `username` | `field_username` |
| `password` | `field_password` |
| `message` | `field_message` |

### Request Variables

Variables from request links use `var_` prefix:

| Link Syntax | Environment Variable |
|-------------|---------------------|
| `action=view` | `var_action` |
| `page=1` | `var_page` |
| `sort=name` | `var_sort` |

### Example Usage

```python
#!/usr/bin/env python3
import os

# Get field data (from form inputs)
username = os.environ.get('field_username', '')
query = os.environ.get('field_query', '')

# Get variables (from request links)
action = os.environ.get('var_action', 'view')
page = os.environ.get('var_page', '1')

print("#!c=0")
print(f">Results for: {query}")
print(f"Action: {action}, Page: {page}")
```

## Configuration

Node configuration in `~/.nomadnetwork/config`:

```ini
[node]
# Enable node hosting
enable_node = yes

# Node display name
node_name = My NomadNet Node

# Announce on network at startup
announce_at_start = yes

# Announce interval in minutes
announce_interval = 360

# Page storage path
pages_path = ~/.nomadnetwork/storage/pages

# Interval in minutes to rescan pages (0 = startup only)
page_refresh_interval = 0

# File storage path
files_path = ~/.nomadnetwork/storage/files

# Interval in minutes to rescan files (0 = startup only)
file_refresh_interval = 0
```

## Best Practices

### Page Organization

```
pages/
├── index.mu              # Landing page with navigation
├── about.mu              # Node information
├── contact.mu            # Contact details
├── apps/
│   ├── index.mu          # App directory
│   ├── calculator.mu     # Interactive app
│   └── search.mu         # Search functionality
└── docs/
    ├── index.mu          # Documentation index
    ├── guide.mu          # User guide
    └── api.mu            # API documentation
```

### Cache Strategy

| Page Type | Recommended Cache |
|-----------|------------------|
| Static info pages | 3600-86400 seconds |
| Navigation menus | 1800-3600 seconds |
| Dynamic status | 0 (no cache) |
| Forms | 0 (no cache) |
| File listings | 300-600 seconds |

### Error Handling in Dynamic Pages

```python
#!/usr/bin/env python3
import os
import sys

try:
    # Your page logic here
    print("#!c=0")
    print(">Page Title")
    # ...
except Exception as e:
    print("#!c=0")
    print(">Error")
    print(f"`Ff00Error: {str(e)}`f")
    sys.exit(1)
```

### Debugging Dynamic Pages

Test pages directly from command line:

```bash
# Set environment variables for testing
export field_username="testuser"
export var_action="view"

# Run the page
python3 ~/.nomadnetwork/storage/pages/mypage.mu
```

## Page Lifecycle

1. **Request received**: Client sends request with path and optional form data
2. **Path resolution**: Server looks up page in storage directory
3. **Permission check**: If `.allowed` file exists, verify identity
4. **Execution**: If executable, run with environment variables; otherwise read file
5. **Response**: Return Micron content to client
6. **Caching**: Client caches based on `#!c=` header
