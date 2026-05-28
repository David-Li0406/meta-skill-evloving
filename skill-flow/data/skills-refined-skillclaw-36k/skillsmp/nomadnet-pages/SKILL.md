---
name: nomadnet-pages
description: This skill should be used when the user asks about "NomadNet page development", "creating .mu pages", "hosting files on NomadNet nodes", "dynamic NomadNet pages", "NomadNet page authentication", "node page serving", ".allowed files", or needs to create, configure, or troubleshoot NomadNet node pages.
---

# NomadNet Page Development

NomadNet nodes can host pages similar to web pages, written in Micron markup (`.mu` files). Pages can be static or dynamic (executable scripts), support file downloads, and include authentication.

## Page Locations

Default storage paths (configurable in `~/.nomadnetwork/config`):

| Type | Path | URL Prefix |
|------|------|------------|
| Pages | `~/.nomadnetwork/storage/pages/` | `/page/` |
| Files | `~/.nomadnetwork/storage/files/` | `/file/` |

Create `index.mu` as the default landing page.

## URL Format

```
<destination_hash>:/page/path.mu
```

Examples:
```
e9eafceea9e3664a5c55611c5e8c420a:/page/index.mu
:/page/local_page.mu          # Local path (same node)
:/file/document.pdf           # File download
```

## Page Headers

Place optional headers at the top of `.mu` files:

```micron
#!c=3600        # Cache for 1 hour (seconds)
#!c=0           # Never cache (dynamic content)
#!fg=ddd        # Default foreground color
#!bg=222        # Default background color
```

Cache header must be first line if present. Default cache time is 12 hours.

## Static Pages

Create `.mu` files with Micron markup:

```micron
#!c=3600
>Welcome

`cWelcome to my NomadNet node!
`a

>>Navigation
`[About`:/page/about.mu]
`[Files`:/page/files.mu]
`[Contact`:/page/contact.mu]
```

## Dynamic Pages

Make `.mu` files executable to generate content dynamically:

```bash
chmod +x page.mu
```

Include shebang and generate Micron output:

```python
#!/usr/bin/env python3
import os
import time

print(">Dynamic Page")
print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Access form data from environment variables
username = os.environ.get('field_username', 'Guest')
print(f"Hello, {username}!")
```

### Environment Variables

Form data passed to dynamic pages:

| Prefix | Source | Example |
|--------|--------|---------|
| `field_` | Form input fields | `field_username`, `field_password` |
| `var_` | Request link variables | `var_action`, `var_page` |

## Authentication

Restrict page access using `.allowed` files:

1. Create `pagename.mu.allowed` alongside the page
2. Add one identity hash per line (32 hex characters):

```
d454bcdac0e64fb68ba8e267543ae110
2b9ff3fb5902c9ca5ff97bdfb239ef50
```

Make `.allowed` executable to generate dynamic access lists.

**Client requirement**: Enable "Identify When Connecting" in node settings to access restricted pages.

## Common Page Patterns

### Navigation Menu

```micron
>Main Menu
-
`F0af`_`[Home`:/page/index.mu]`_`f
`F0af`_`[About`:/page/about.mu]`_`f
`F0af`_`[Files`:/page/files.mu]`_`f
```

### Login Form

```micron
>Login

Username: `B444`<16|username`>`b
Password: `B444`<!16|password`>`b

`[Sign In`:/page/auth.mu`*]
```

### File Listing

```micron
>Available Downloads

`[Document.pdf`:/file/document.pdf]
`[Archive.zip`:/file/archive.zip]
```

### Status Page (Dynamic)

```python
#!/usr/bin/env python3
import time
import os

print("#!c=0")  # No caching
print(">Node Status")
print(f"Uptime: {os.popen('uptime -p').read().strip()}")
print(f"Updated: {time.strftime('%H:%M:%S')}")
```

## Troubleshooting

**Page not found**: Verify file exists in `~/.nomadnetwork/storage/pages/` and path matches URL

**Dynamic page not executing**: Check shebang line, file permissions (`chmod +x`), and script errors

**Form data not received**: Verify field names match environment variable lookups (`field_` prefix)

**Authentication failing**: Confirm identity hash format (32 hex chars), client has "Identify When Connecting" enabled

**Cache issues**: Set `#!c=0` for dynamic content, clear client cache if testing changes

## Additional Resources

### Reference Files

For detailed documentation, consult:
- **`references/page-structure.md`** - Complete page configuration and headers
- **`references/file-serving.md`** - File hosting and download URLs
- **`references/authentication.md`** - Authentication patterns and .allowed files

### Configuration

Node configuration in `~/.nomadnetwork/config`:

```ini
[node]
enable_node = yes
node_name = My Node
pages_path = ~/.nomadnetwork/storage/pages
files_path = ~/.nomadnetwork/storage/files
```
