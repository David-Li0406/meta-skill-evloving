---
name: fnox-secrets
description: Manages fnox encrypted secrets for the micelio project. Use when setting up secrets, adding new environment variables, configuring deployment credentials, or troubleshooting fnox/age encryption.
allowed-tools: Bash, Read, Grep
---

# fnox Secrets Management

This project uses [fnox](https://fnox.jdx.dev/) with age encryption to manage secrets. Secrets are encrypted in the repository and can be shared between local development and CI.

## Configuration

- **Config file**: `fnox.toml` in the project root
- **Age key location**: `~/.config/fnox/micelio-age.txt`
- **Public key**: `age147aml8dcjnfyj8gacmx8fvskkrg0gq9lfcrfvmquj28ft3rag5sqyq3nss`

## Current Secrets

| Secret | Purpose |
|--------|---------|
| `KAMAL_REGISTRY_PASSWORD` | Docker registry authentication |
| `POSTGRES_PASSWORD` | Database password |
| `SECRET_KEY_BASE` | Phoenix secret key |
| `SSH_PRIVATE_KEY` | Server SSH access for deployments |

## Common Commands

```bash
# List all secrets
fnox list

# Get a secret value (decrypted)
fnox get SECRET_NAME

# Set a new secret (interactive)
fnox set SECRET_NAME

# Set a secret from stdin
echo "value" | fnox set SECRET_NAME

# Run a command with secrets in environment
fnox exec -- command
```

## Adding a New Secret

1. Add the secret definition to `fnox.toml`:
   ```toml
   NEW_SECRET = { provider = "age" }
   ```

2. Set the secret value:
   ```bash
   fnox set NEW_SECRET
   ```

3. If needed in Kamal, add to `config/deploy.yml`:
   ```yaml
   env:
     secret:
       - NEW_SECRET
   ```

4. Commit `fnox.toml` (encrypted values are safe to commit)

## Setting Up on a New Machine

1. Get the age private key from a secure source (password manager, team member)

2. Create the key file:
   ```bash
   mkdir -p ~/.config/fnox
   # Paste the key content into this file:
   vim ~/.config/fnox/micelio-age.txt
   chmod 600 ~/.config/fnox/micelio-age.txt
   ```

3. Verify access:
   ```bash
   fnox list
   fnox get POSTGRES_PASSWORD
   ```

## Setting Up GitHub Actions

1. Copy the age private key:
   ```bash
   cat ~/.config/fnox/micelio-age.txt | pbcopy
   ```

2. Add to GitHub:
   - Go to repository Settings > Secrets and variables > Actions
   - Create new secret named `FNOX_AGE_KEY`
   - Paste the key content

## Generating Secure Values

```bash
# 32-byte hex string (good for passwords)
openssl rand -hex 32

# 64-byte hex string (good for secret keys)
openssl rand -hex 64
```

## Troubleshooting

**Error: "unknown field `identity`"**
- Use `key_file` instead of `identity` in fnox.toml

**Error: "could not decrypt"**
- Verify the age key file exists at `~/.config/fnox/micelio-age.txt`
- Check file permissions: `chmod 600 ~/.config/fnox/micelio-age.txt`
- Ensure you have the correct private key for this project

**Secret not available in deployment**
- Verify it's listed in `config/deploy.yml` under `env.secret`
- Ensure `FNOX_AGE_KEY` is set in GitHub Actions secrets
