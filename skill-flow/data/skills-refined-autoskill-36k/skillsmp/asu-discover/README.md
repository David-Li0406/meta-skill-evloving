# ASU Discovery Skill

Smart discovery across ASU GitHub repositories. Provides domain-aware search, pattern documentation, and integration guidance for ASU infrastructure.

## Requirements

### Required

| Requirement | Purpose | Installation |
|-------------|---------|--------------|
| `gh` CLI | GitHub API access | `brew install gh` then `gh auth login` |
| `sqlite3` | Local repository index | Usually pre-installed on macOS/Linux |
| `yq` | YAML parsing | `brew install yq` |

## Quick Start

```bash
# Build the local index (first time only, ~30 seconds)
./scripts/discover.sh index build

# Check index statistics
./scripts/discover.sh index stats

# Search for repos
./scripts/discover.sh search --query "PeopleSoft integration"

# View a design pattern
./scripts/discover.sh pattern --name vault
./scripts/discover.sh pattern --name vault --brief
```

## Directory Structure

```
asu-discover/
├── SKILL.md              # Skill definition and documentation
├── README.md             # This file
├── config/
│   └── domains.yaml      # Domain taxonomy and pattern config
├── data/
│   └── asu-repos.db      # SQLite index (auto-generated)
├── patterns/             # Design pattern documentation
│   ├── eel.md
│   ├── cicd.md
│   ├── terraform-modules.md
│   ├── vault.md
│   ├── observability.md
│   └── dns.md
├── scripts/
│   ├── discover.sh       # Main script
│   └── lib/
│       ├── db.sh         # Database helpers
│       ├── dns.sh        # DNS scaffolding
│       └── yaml.sh       # YAML parsing (requires yq)
└── templates/
    └── dns/              # DNS Terraform templates
```

## Commands

### Core Commands

| Command | Description |
|---------|-------------|
| `search --query <query>` | Domain-aware repository search |
| `repos --domain <domain>` | Find repos by domain |
| `code --query <query>` | Search code (rate-limited, cached) |
| `context --query <query>` | Build integration context |
| `pattern --name <name>` | Show design pattern documentation |

### Index Commands

| Command | Description |
|---------|-------------|
| `index build` | Build full index from scratch |
| `index refresh` | Incremental update |
| `index stats` | Show repository counts and statistics |
| `index verify` | Check if referenced repos still exist |

### DNS Commands

| Command | Description |
|---------|-------------|
| `dns-validate --domain <domain>` | Validate domain and show provider |
| `dns-scaffold --domain <domain>` | Generate Terraform code |
| `dns-examples` | Show example repos |

## Design Patterns

| Pattern | Description |
|---------|-------------|
| `eel` | Enterprise Event Lake (Kafka) |
| `cicd` | Jenkins + GitHub Actions |
| `terraform-modules` | ASU Terraform modules on JFrog |
| `vault` | HashiCorp Vault secrets |
| `observability` | Datadog, Logging Lake, CloudWatch |
| `dns` | Infoblox + Cloudflare DNS |

## Options

| Option | Description |
|--------|-------------|
| `--brief` | Show condensed output (patterns only) |
| `--limit N` | Maximum results (default: 30) |
| `--local-only` | Only search local index |
| `--cached-only` | Only use cached results |
| `--json` | JSON output format |

## Maintenance

### Verify Repository References

The skill references specific ASU repositories in `config/domains.yaml`. To check if these still exist:

```bash
./scripts/discover.sh index verify
```

### Update Index

```bash
# Full rebuild
./scripts/discover.sh index build

# Incremental update (faster)
./scripts/discover.sh index refresh
```
