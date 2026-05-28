# ccmds Command Reference

Complete reference for all ccmds commands and options.

## Global Options

Available on all commands:

| Flag | Description |
|------|-------------|
| `--config <path>` | Use specific config file |
| `--no-config` | Ignore config files, use defaults |
| `--doc <name>` | Search only named documentation (prefix match) |

---

## ccmds find

Fuzzy/semantic search for discovering relevant documents.

```bash
ccmds find <query> [directories...]
```

**Options:**

| Flag | Description | Config Key |
|------|-------------|------------|
| `-l, --limit <n>` | Max results (default: 10) | `limit` |
| `-o, --output <mode>` | compact, detailed, files, json | `outputMode` |
| `-e, --exclude <patterns...>` | Exclude glob patterns | `exclude` |
| `--doc <name>` | Named doc filter (prefix) | - |
| `-r, --raw` | Disable adaptive previews | - |

**Extended Search Syntax:**

| Pattern | Meaning | Example |
|---------|---------|---------|
| `word1 word2` | AND (all must match) | `auth setup` |
| `word1 \| word2` | OR (either matches) | `install \| setup` |
| `'exact` | Exact substring | `'authentication` |
| `^prefix` | Starts with | `^Config` |
| `suffix$` | Ends with | `Guide$` |

**Examples:**

```bash
ccmds find "authentication"
ccmds find "auth setup" -l 5
ccmds find "setup | installation" -o files
ccmds find "error handling" -l 3 -o detailed
ccmds find "endpoints" --doc api           # Search only API docs
```

---

## ccmds grep

Pattern/regex search for exact matches.

```bash
ccmds grep <pattern> [directories...]
```

**Options:**

| Flag | Description | Config Key |
|------|-------------|------------|
| `-o, --output <mode>` | compact, detailed, files, json | `outputMode` |
| `-e, --exclude <patterns...>` | Exclude glob patterns | `exclude` |
| `--doc <name>` | Named doc filter (prefix) | - |
| `-c, --context <n>` | Context lines (with --raw) | - |
| `-s, --case-sensitive` | Case sensitive matching | - |
| `-r, --raw` | Line-based context (not smart) | - |

**Examples:**

```bash
ccmds grep "ERROR_[0-9]+"
ccmds grep "TODO|FIXME" -o files
ccmds grep "GraphQL" --case-sensitive
ccmds grep "pattern" --raw -c 3
ccmds grep "TODO" --doc api              # Grep only in API docs
```

---

## ccmds outline

Show document structure (headings only).

```bash
ccmds outline [paths...]
```

**Options:**

| Flag | Description |
|------|-------------|
| `-d, --depth <n>` | Max heading depth (default: 6) |
| `-o, --output <mode>` | text, json |
| `-e, --exclude <patterns...>` | Exclude glob patterns |
| `--doc <name>` | Named doc filter (prefix) |

**Examples:**

```bash
ccmds outline
ccmds outline ./docs/guide.md
ccmds outline -d 2
ccmds outline -o json
ccmds outline --doc guides               # Outline only guides docs
```

---

## ccmds section

Extract a specific section by heading.

```bash
ccmds section <file> <heading>
```

**Options:**

| Flag | Description |
|------|-------------|
| `-o, --output <mode>` | text, json |

**Examples:**

```bash
ccmds section ./docs/setup.md "Installation"
ccmds section ./docs/guide.md "Setup > Prerequisites"
ccmds section ./docs/api.md "Authentication" -o json
```

---

## ccmds list

List markdown files.

```bash
ccmds list [directories...]
```

**Options:**

| Flag | Description |
|------|-------------|
| `-c, --count` | Show only count |
| `-e, --exclude <patterns...>` | Exclude glob patterns |
| `--doc <name>` | Named doc filter (prefix) |

**Examples:**

```bash
ccmds list
ccmds list --count
ccmds list -e "**/archive/**"
ccmds list --doc api                     # List only API doc files
```

---

## ccmds show

Display full file content.

```bash
ccmds show <file>
```

**Options:**

| Flag | Description |
|------|-------------|
| `-f, --frontmatter-only` | Show only YAML frontmatter |
| `-b, --body-only` | Show only body content |

**Examples:**

```bash
ccmds show ./docs/api/auth.md
ccmds show ./docs/guide.md --frontmatter-only
ccmds show ./docs/guide.md --body-only
```

---

## ccmds config

Show current configuration.

```bash
ccmds config
```

**Options:**

| Flag | Description |
|------|-------------|
| `-p, --path` | Show only config file path |
| `-o, --output <mode>` | text, json |

**Examples:**

```bash
ccmds config
ccmds config --path
ccmds config -o json
```

---

## ccmds init

Create a configuration file.

```bash
ccmds init
```

**Options:**

| Flag | Description |
|------|-------------|
| `-d, --directories <dirs...>` | Default directories |
| `-f, --force` | Overwrite existing config |

**Examples:**

```bash
ccmds init
ccmds init -d ./docs ./wiki
ccmds init --force
```
