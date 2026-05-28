# NomadNet Page Authentication

Guide to implementing access control for NomadNet pages.

## Overview

NomadNet supports page-level authentication using `.allowed` files. When a user requests a protected page, the node verifies their identity against an allowed list.

## Identity Hashes

### Format

Identity hashes are 32 hexadecimal characters (16 bytes):

```
d454bcdac0e64fb68ba8e267543ae110
```

### Finding Your Identity Hash

Users can find their identity hash in NomadNet:
1. Go to `[ Network ]` section
2. Select `Local Peer Info`
3. Copy the identity hash

### Identity vs Destination Hash

| Type | Length | Purpose |
|------|--------|---------|
| Identity Hash | 32 hex chars | Identifies a user's cryptographic identity |
| Destination Hash | 32 hex chars | Addresses a specific endpoint (LXMF address) |

For authentication, use the identity hash.

## Creating .allowed Files

### Basic Setup

For each page that needs authentication, create a companion `.allowed` file:

```
pages/
├── public.mu              # No authentication
├── private.mu             # Protected page
└── private.mu.allowed     # Access control for private.mu
```

### Static Allowed List

Create a text file with one identity hash per line:

```
# private.mu.allowed
d454bcdac0e64fb68ba8e267543ae110
2b9ff3fb5902c9ca5ff97bdfb239ef50
7106d5abbc7208bfb171f2dd84b36490
```

### Comments in Allowed Files

Lines starting with `#` are treated as comments:

```
# Admin users
d454bcdac0e64fb68ba8e267543ae110

# Staff members
2b9ff3fb5902c9ca5ff97bdfb239ef50
7106d5abbc7208bfb171f2dd84b36490

# Temporary access
abc123def456789012345678901234ab
```

## Dynamic Allowed Lists

Make the `.allowed` file executable to generate access lists dynamically.

### Python Dynamic Auth

```python
#!/usr/bin/env python3
import os
import time

# Read allowed users from database or file
allowed_users = [
    "d454bcdac0e64fb68ba8e267543ae110",
    "2b9ff3fb5902c9ca5ff97bdfb239ef50",
]

# Check time-based access
current_hour = time.localtime().tm_hour
if 9 <= current_hour <= 17:  # Business hours only
    for user in allowed_users:
        print(user)
```

### Bash Dynamic Auth

```bash
#!/bin/bash

# Read from a config file
cat /etc/nomadnet/allowed_users.txt

# Or from a database
# sqlite3 /var/db/users.db "SELECT identity_hash FROM allowed_users"
```

### Database-Backed Auth

```python
#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/var/db/nomadnet_users.db')
cursor = conn.cursor()

# Get all active users
cursor.execute("""
    SELECT identity_hash
    FROM users
    WHERE is_active = 1
    AND access_level >= 2
""")

for row in cursor.fetchall():
    print(row[0])

conn.close()
```

## Client Configuration

### Enabling Identity

Clients must enable "Identify When Connecting" to access protected pages:

1. Go to `[ Network ]` section
2. Select `Known Nodes` list
3. Find the node and select `< Info >`
4. Enable `Identify When Connecting`

Without this setting, the client connects anonymously and cannot access protected pages.

### Per-Node Setting

Identity settings are per-node, allowing users to:
- Identify to trusted nodes
- Stay anonymous on untrusted nodes

## Authentication Patterns

### Admin-Only Page

```
# admin.mu.allowed
# Only the admin can access
d454bcdac0e64fb68ba8e267543ae110
```

### Group Access

```
# team.mu.allowed
# Development team
d454bcdac0e64fb68ba8e267543ae110
2b9ff3fb5902c9ca5ff97bdfb239ef50

# Operations team
7106d5abbc7208bfb171f2dd84b36490
abc123def456789012345678901234ab
```

### Directory-Level Protection

Protect all pages in a directory:

```
pages/
└── admin/
    ├── index.mu
    ├── index.mu.allowed     # Protects index.mu
    ├── users.mu
    ├── users.mu.allowed     # Protects users.mu
    ├── settings.mu
    └── settings.mu.allowed  # Protects settings.mu
```

Or use a single dynamic script that checks against a shared list:

```python
#!/usr/bin/env python3
# admin/index.mu.allowed, users.mu.allowed, settings.mu.allowed
# Can all be symlinks to this script

admin_users = [
    "d454bcdac0e64fb68ba8e267543ae110",
]

for user in admin_users:
    print(user)
```

### Time-Based Access

```python
#!/usr/bin/env python3
import time

# Full access users (always allowed)
always_allowed = [
    "d454bcdac0e64fb68ba8e267543ae110",
]

# Limited access users (business hours only)
limited_users = [
    "2b9ff3fb5902c9ca5ff97bdfb239ef50",
]

# Print always-allowed users
for user in always_allowed:
    print(user)

# Check if business hours
hour = time.localtime().tm_hour
if 9 <= hour <= 17:
    for user in limited_users:
        print(user)
```

### Subscription-Based Access

```python
#!/usr/bin/env python3
import os
import json
from datetime import datetime

# Load subscription database
with open('/etc/nomadnet/subscriptions.json') as f:
    subscriptions = json.load(f)

now = datetime.now()

for user_hash, expiry_str in subscriptions.items():
    expiry = datetime.fromisoformat(expiry_str)
    if now < expiry:
        print(user_hash)
```

## Combining with Dynamic Pages

### Access Control in Dynamic Pages

Even with `.allowed` files, dynamic pages can implement additional logic:

```python
#!/usr/bin/env python3
import os

# The connecting user's identity (if identified)
# This would need to be passed by NomadNet
# Currently .allowed is the primary mechanism

print("#!c=0")
print(">Protected Page")
print("")
print("You have been authenticated!")
print("")
print(">>Sensitive Information")
print("This content is only for authorized users.")
```

### Login Flow

While `.allowed` handles authentication, you can create a user-friendly login flow:

**public login.mu:**
```micron
>Login Required

This area requires authentication.

To access protected content:
1. Enable "Identify When Connecting" for this node
2. Ensure your identity hash is registered

Your identity hash can be found in `![ Network ] > Local Peer Info`!

`[Try accessing protected area`:/page/protected/index.mu]
```

**protected/index.mu + protected/index.mu.allowed:**
```micron
>Welcome, Authenticated User!

You have access to the protected area.

>>Available Resources
`[Admin Dashboard`:/page/protected/admin.mu]
`[User Management`:/page/protected/users.mu]
```

## Error Handling

### Access Denied

When authentication fails, NomadNet returns an error to the client. The exact behavior depends on the client implementation.

### Debugging Authentication

1. Verify the identity hash is correct (32 hex chars)
2. Check `.allowed` file permissions
3. If dynamic, test the script directly:
   ```bash
   chmod +x page.mu.allowed
   ./page.mu.allowed
   ```
4. Ensure client has "Identify When Connecting" enabled

## Security Considerations

### Hash Verification

- Always verify identity hashes before adding to allowed lists
- Consider requiring out-of-band verification for sensitive access

### File Permissions

- Set restrictive permissions on `.allowed` files
- Protect dynamic auth scripts from unauthorized modification

### Audit Logging

For sensitive pages, consider logging access:

```python
#!/usr/bin/env python3
import os
import time

# Log access attempt
with open('/var/log/nomadnet_access.log', 'a') as f:
    f.write(f"{time.time()}: Access check for protected page\n")

# Return allowed users
allowed = ["d454bcdac0e64fb68ba8e267543ae110"]
for user in allowed:
    print(user)
```

### Regular Review

- Periodically review allowed user lists
- Remove access for users who no longer need it
- Consider expiration dates for temporary access
