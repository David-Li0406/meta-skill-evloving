# deep-env - Universal Credential Manager

Secure environment variable management across all your Macs via macOS Keychain + iCloud.

## Quick Setup on a New Mac

Tell Claude Code:
```
Read ~/Library/Mobile Documents/com~apple~CloudDocs/.deep-env/README.md and set up deep-env
```

Or manually:

### 1. Install the CLI

```bash
mkdir -p ~/.local/bin
cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/.deep-env/deep-env ~/.local/bin/
chmod +x ~/.local/bin/deep-env
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Pull Credentials from iCloud

```bash
deep-env pull
# Enter sync password when prompted
```

### 3. Sync to Any Project

```bash
cd ~/your-project
deep-env sync .
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│  ANY PROJECT with .env.example                                  │
│                                                                 │
│  .env.example defines:          deep-env sync .                 │
│    ANTHROPIC_API_KEY=           ─────────────────►  .env.local  │
│    DATABASE_URL=                reads from Keychain             │
│    STRIPE_KEY=                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Mac #1                           Mac #2                        │
│  ┌─────────┐  deep-env push  ┌─────────────┐  deep-env pull    │
│  │Keychain │ ──────────────► │iCloud Drive │ ──────────────►   │
│  └─────────┘   encrypted     │credentials  │   decrypted       │
│                              │   .enc      │                    │
│                              └─────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

## Commands

| Command | Description |
|---------|-------------|
| `deep-env sync .` | Generate .env.local in current directory |
| `deep-env sync ~/path` | Generate .env.local at path |
| `deep-env list` | Show all stored credentials (masked) |
| `deep-env store KEY VALUE` | Store a new credential |
| `deep-env get KEY` | Get single value (for scripts) |
| `deep-env push` | Push to iCloud (for other Macs) |
| `deep-env pull` | Pull from iCloud |
| `deep-env backup` | Create timestamped backup |
| `deep-env restore` | Restore from backup |
| `deep-env validate` | Check data integrity |
| `deep-env import file` | Import from .env file |
| `deep-env --version` | Show version number |

## Workflow

### Adding a New Credential

```bash
# Store it
deep-env store NEW_API_KEY "sk-xxx-yyy"

# Push to iCloud so other Macs get it
deep-env push

# Sync to project
cd ~/my-project
deep-env sync .
```

### Starting a New Project

```bash
cd ~/new-project

# If project has .env.example:
deep-env sync .
# Will show which keys are missing

# Add missing keys:
deep-env store MISSING_KEY "value"
deep-env push
```

## Project Detection

deep-env automatically reads `.env.example` (or `.env.template`, `.env.sample`) to determine which keys a project needs:

```
my-project/
├── .env.example      ← deep-env reads this
├── .env.local        ← deep-env generates this
└── ...
```

If no template exists, it syncs ALL stored credentials.

## Security

- Credentials stored in macOS Keychain (hardware-backed encryption on Apple Silicon)
- Sync password stored locally in `~/.config/deep-env/.sync_pass` (not in iCloud)
- OpenSSL encryption uses stdin for passwords (hidden from `ps aux`)
- iCloud sync uses AES-256-CBC with PBKDF2
- .env.local files created with mode 600 (owner only)
- Automatic backup created before pull operations
- Multi-line values (PEM keys, etc.) fully supported

## Files

```
~/.local/bin/deep-env                    # CLI tool
~/.config/deep-env/                      # Local config
  ├── keys.txt                           # Tracked key names
  ├── project-keys.json                  # Project assignments
  ├── .sync_pass                         # Sync password (local only)
  └── backups/                           # Automatic backups (last 5 kept)

~/Library/Mobile Documents/.../
  └── .deep-env/
      ├── credentials.enc                # Encrypted credentials
      ├── deep-env                       # CLI tool (for new Macs)
      └── README.md                      # This file
```

## For Claude Code

When setting up on a new Mac:

```bash
# 1. Copy CLI from iCloud
mkdir -p ~/.local/bin
cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/.deep-env/deep-env ~/.local/bin/
chmod +x ~/.local/bin/deep-env

# 2. Pull credentials (ASK USER FOR PASSWORD)
~/.local/bin/deep-env pull

# 3. Validate installation
~/.local/bin/deep-env validate
~/.local/bin/deep-env list | head -5

# 4. Sync to project
cd ~/project-directory
~/.local/bin/deep-env sync .
```

When working on any project:
- If you see `.env.example` but no `.env.local`, run `deep-env sync .`
- If user provides a new credential, store it with `deep-env store KEY VALUE` then `deep-env push`

## Troubleshooting

```bash
# Validate data integrity
deep-env validate

# List available backups
deep-env restore

# Restore from backup
deep-env restore ~/.config/deep-env/backups/<filename>.json

# Re-pull from iCloud if local is corrupted
deep-env pull
```

### Large Credential Sets (80+ keys)

If you have many credentials, the JSON payload may exceed macOS Keychain's limit (~16KB per entry).

**Solution: Use Project-Specific Storage**

Instead of storing everything globally:
```bash
# Global (shared across all projects)
deep-env store ANTHROPIC_API_KEY "sk-ant-..." --global
deep-env store OPENAI_API_KEY "sk-..." --global

# Project-specific (only for this project)
cd ~/my-project
deep-env store CRON_SECRET "abc123" --project
deep-env store SESSION_SECRET "xyz789" --project
```

This splits the credentials into smaller chunks that fit within Keychain limits.

## Sync Password

Ask the user - they set it when first running `deep-env push`.
On other Macs, check `~/.config/deep-env/.sync_pass` if you need to find it.
