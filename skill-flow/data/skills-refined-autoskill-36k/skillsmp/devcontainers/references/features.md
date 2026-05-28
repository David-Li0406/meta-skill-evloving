# Feature Reference

Detailed configuration options for each DuploCloud devcontainer feature.

## Complete Feature List

| Feature | Description |
|---------|-------------|
| `duploctl` | DuploCloud CLI (required) |
| `aws-cli` | AWS CLI with JIT credentials |
| `gcloud-cli` | Google Cloud CLI |
| `terraform` | Terraform with `tf` wrapper |
| `kubernetes` | kubectl with JIT kubeconfig |
| `github` | GitHub CLI with optional Copilot |
| `git` | Git config, signing, plugins |
| `ai` | Base AI dependencies (auto-installed) |
| `ai-claude` | Anthropic Claude Code CLI |
| `ai-codex` | OpenAI Codex CLI |
| `ai-gemini` | Google Gemini CLI |
| `onepassword-cli` | 1Password CLI with SSH |
| `direnv` | direnv with DuploCloud direnvrc |
| `openvpn` | OpenVPN client |

---

## duploctl (Required)

**Always include this feature.** All other DuploCloud features depend on it.

```json
"ghcr.io/duplocloud/devcontainers/duploctl:latest": {}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `version` | string | `latest` | Version to install (e.g., `v0.3.8`) |

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/duploctl/README.md

---

## aws-cli

AWS CLI with JIT credentials from DuploCloud.

```json
"ghcr.io/duplocloud/devcontainers/aws-cli:latest": {
  "jit": true,
  "jitAdmin": true
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `jit` | boolean | `false` | Enable JIT AWS CLI config on container creation |
| `jitAdmin` | boolean | `false` | Use admin credentials (`--admin` flag) |
| `jitInteractive` | boolean | `false` | Enable interactive mode (`--interactive` flag) |

**Environment variables to set:**

```json
"containerEnv": {
  "AWS_CONFIG_FILE": "${containerWorkspaceFolder}/config/aws",
  "AWS_DEFAULT_REGION": "us-east-1",
  "AWS_REGION": "us-east-1",
  "AWS_PROFILE": "default"
}
```

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/aws-cli/README.md

---

## gcloud-cli

Google Cloud CLI with multi-architecture support.

```json
"ghcr.io/duplocloud/devcontainers/gcloud-cli:1": {}
```

No configurable options.

**Environment variables to set:**

```json
"containerEnv": {
  "CLOUDSDK_CONFIG": "${containerWorkspaceFolder}/config/gcloud",
  "CLOUDSDK_PYTHON": "/usr/local/bin/python",
  "GOOGLE_APPLICATION_CREDENTIALS": "${containerWorkspaceFolder}/config/gcloud/application_default_credentials.json"
}
```

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/gcloud-cli/README.md

---

## kubernetes

kubectl with JIT kubeconfig from DuploCloud.

```json
"ghcr.io/duplocloud/devcontainers/kubernetes:1": {
  "jit": true,
  "jitAdmin": true,
  "plan": "nonprod01"
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `jit` | boolean | `true` | Enable JIT authentication on container creation |
| `jitAdmin` | boolean | `false` | Use admin privileges (requires admin token) |
| `jitInteractive` | boolean | `false` | Use interactive browser auth |
| `plan` | string | - | DuploCloud infrastructure name (requires admin) |
| `tenant` | string | - | DuploCloud tenant name to scope into |

**Environment variables to set:**

```json
"containerEnv": {
  "KUBECONFIG": "${containerWorkspaceFolder}/config/kubeconfig.yaml"
}
```

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/kubernetes/README.md

---

## terraform

Terraform with DuploCloud `tf` wrapper script.

```json
"ghcr.io/duplocloud/devcontainers/terraform:1": {}
```

No configurable options. Provides `tf` command with:
- Automatic backend configuration
- Variable file detection
- Workspace management (`tf ctx`)

**VS Code settings:**

```json
"customizations": {
  "vscode": {
    "extensions": ["hashicorp.terraform"],
    "settings": {
      "[terraform]": {
        "editor.defaultFormatter": "hashicorp.terraform",
        "editor.formatOnSave": true
      }
    }
  }
}
```

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/terraform/README.md

---

## github

GitHub CLI with optional Copilot and skills support.

```json
"ghcr.io/duplocloud/devcontainers/github:latest": {
  "installCopilot": true,
  "skills": "tf-module"
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `installCopilot` | boolean | `false` | Install GitHub Copilot CLI extension |
| `skills` | string | - | Comma-separated skills to install |

**VS Code Extension**: `github.vscode-pull-request-github`

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/github/README.md

---

## git

Git configuration with user settings, signing keys, and plugins.

```json
"ghcr.io/duplocloud/devcontainers/git:1": {
  "userName": "${localEnv:GIT_USERNAME}",
  "userEmail": "${localEnv:GIT_EMAIL}",
  "signingKey": "github.pub"
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `provider` | string | `none` | Git provider (future use) |
| `userName` | string | - | Git user.name (fallback: `GIT_USER` env) |
| `userEmail` | string | - | Git user.email (fallback: `GIT_EMAIL` env) |
| `signingKey` | string | - | Path to signing key relative to `~/.ssh` |
| `installGitKraken` | boolean | `false` | Install GitKraken CLI |

**Included plugins:**
- `git-bump` - Semantic version bumping (`git bump -v patch/minor/major`)
- `git-setenv` - Export CI env vars (`eval $(git setenv bitbucket)`)

**VS Code Extension**: `eamodio.gitlens`

**Integration with 1Password:**
```json
{
  "ghcr.io/duplocloud/devcontainers/onepassword-cli:1": {
    "autoSsh": true,
    "sshSecretNames": "GitHub SSH Key"
  },
  "ghcr.io/duplocloud/devcontainers/git:1": {
    "signingKey": "GitHub_SSH_Key.pub"
  }
}
```

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/git/README.md

---

## ai (Base)

Base dependencies for AI CLI tools. **Automatically installed** by ai-claude, ai-codex, ai-gemini.

```json
"ghcr.io/duplocloud/devcontainers/ai:1": {}
```

Provides:
- Node.js installation
- `duplo-skills` CLI for downloading skills from duplocloud/skills releases

**Manual skill installation:**
```bash
duplo-skills --dir ~/.claude/skills --skill tf-module
DUPLO_SKILLS_VERSION=v0.0.2 duplo-skills --dir ~/.gemini/skills --skill api-design
```

**Environment variables:**
- `DUPLO_SKILLS_VERSION` - Pin to specific release version
- `GITHUB_TOKEN` / `GH_TOKEN` - Avoid API rate limits

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/ai/README.md

---

## ai-claude

Anthropic's Claude Code CLI with VS Code integration.

```json
"ghcr.io/duplocloud/devcontainers/ai-claude:1": {
  "skills": "tf-module,devcontainers"
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `skills` | string | - | Comma-separated skills to install |

**Skills location**: `~/.claude/skills/`

**VS Code Extension**: `anthropic.claude-code`

**Skill discovery:**
- User: `~/.claude/skills/`
- Project: `.claude/skills/`
- Plugin: Provided by extensions

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/ai-claude/README.md

---

## ai-codex

OpenAI Codex CLI with VS Code integration.

```json
"ghcr.io/duplocloud/devcontainers/ai-codex:1": {
  "skills": "tf-module,tf-gen-module"
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `skills` | string | - | Comma-separated skills to install |

**Environment variables to set:**

```json
"containerEnv": {
  "CODEX_HOME": "${containerWorkspaceFolder}/.codex"
}
```

**Available skills** (from duplocloud/skills releases):
- `tf-module` - Terraform module patterns
- `tf-gen-module` - Terraform module generation

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/ai-codex/README.md

---

## ai-gemini

Google's Gemini CLI with VS Code integration.

```json
"ghcr.io/duplocloud/devcontainers/ai-gemini:1": {
  "skills": "tf-module"
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `skills` | string | - | Comma-separated skills to install |

**Skills location**: `~/.gemini/skills/`

**VS Code Extension**: `Google.geminicodeassist`

**Skill discovery (precedence):**
1. Workspace: `.gemini/skills/`
2. User: `~/.gemini/skills/`
3. Extension: Provided by extensions

**Interactive commands:**
- `/skills list` - View all skills
- `/skills disable <name>` - Disable skill
- `/skills enable <name>` - Re-enable skill
- `/skills reload` - Refresh list

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/ai-gemini/README.md

---

## onepassword-cli

1Password CLI with automatic SSH key configuration.

```json
"ghcr.io/duplocloud/devcontainers/onepassword-cli:1": {
  "autoSsh": true,
  "sshSecretNames": "${localEnv:OP_SSH_SECRET}",
  "vault": "Employee",
  "account": "duplocloudinc.1password.com"
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable the feature |
| `vault` | string | - | Default vault name |
| `vaultID` | string | - | Default vault ID (preferred over name) |
| `account` | string | `my.1password.com` | 1Password account domain |
| `userEmail` | string | - | User email for account |
| `autoSsh` | boolean | `false` | Fetch and configure SSH keys |
| `sshSecretNames` | string | - | Comma-separated secret names for SSH keys |
| `sshSecretTags` | string | `ssh` | Tags to search for SSH secrets |
| `disableInteractive` | boolean | `false` | Disable interactive login prompt |

**Common account domains:**
- `my.1password.com` (default)
- `duplocloudinc.1password.com` (DuploCloud employees)

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/onepassword-cli/README.md

---

## git

Git configuration with signing keys and plugins.

```json
"ghcr.io/duplocloud/devcontainers/git:latest": {
  "userName": "${localEnv:GIT_USERNAME}",
  "userEmail": "${localEnv:GIT_EMAIL}",
  "signingKey": "Github.pub"
}
```

---

## direnv

direnv with DuploCloud-specific direnvrc.

```json
"ghcr.io/duplocloud/devcontainers/direnv:1": {}
```

No configurable options. Installs direnv and places DuploCloud direnvrc at `$HOME/direnv/direnvrc`.

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/direnv/README.md

---

## openvpn

OpenVPN client for connecting to VPN networks.

```json
"ghcr.io/duplocloud/devcontainers/openvpn:1": {
  "autoConnect": true
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable the feature |
| `autoConnect` | boolean | `true` | Auto-connect on container start |
| `configDir` | string | - | Custom config directory |

**Required in devcontainer.json:**
```json
"runArgs": ["--device=/dev/net/tun"]
```

**Config location**: `$XDG_CONFIG_HOME/openvpn` or `~/.config/openvpn`

**README**: https://raw.githubusercontent.com/duplocloud/devcontainers/refs/heads/main/src/openvpn/README.md

---

## docker-outside-of-docker (External)

Not a DuploCloud feature, but commonly included:

```json
"ghcr.io/devcontainers/features/docker-outside-of-docker:1": {
  "moby": "false"
}
```

Enables Docker commands inside the devcontainer using the host's Docker daemon.
