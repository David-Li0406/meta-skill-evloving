---
name: wordpress-best-practices
description: WordPress development standards. Triggers when working with WordPress plugins, themes, hooks, REST API, or Gutenberg blocks.
trigger_patterns:
  - wordpress
  - wp-content
  - add_action
  - add_filter
  - get_option
  - wp_enqueue
  - functions.php
auto_load_with:
  - php-best-practices
  - mysql-best-practices
---

# WordPress Best Practices

Comprehensive coding standards for WordPress development, optimized for AI agents and LLMs.

## Overview

This skill provides 25 rules organized across 8 categories:

1. **Security Hardening (security-)** - Output escaping, input sanitization, nonces [CRITICAL]
2. **Database Optimization (database-)** - Autoload options, transients, meta queries [HIGH]
3. **Performance (perf-)** - Asset enqueuing, lazy loading, heartbeat [HIGH]
4. **Plugin Development (plugin-)** - Prefixing, hooks, activation/deactivation [MEDIUM-HIGH]
5. **Theme Development (theme-)** - Template hierarchy, child themes, customizer [MEDIUM]
6. **REST API (api-)** - Permissions, schemas, namespacing [MEDIUM]
7. **Multisite (multisite-)** - Network admin, site switching [LOW-MEDIUM]
8. **Gutenberg/Blocks (blocks-)** - Block patterns, InnerBlocks [LOW-MEDIUM]

## Usage

Reference this skill when:
- Developing WordPress plugins
- Creating or modifying themes
- Building custom Gutenberg blocks
- Implementing REST API endpoints
- Optimizing WordPress performance

## Build

```bash
pnpm build    # Compile rules to AGENTS.md
pnpm validate # Validate rule files
```
