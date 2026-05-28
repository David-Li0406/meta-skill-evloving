# Secrets Management

Chezmoi supports multiple password managers and encryption methods for secrets.

## 1Password

### Setup

```toml
# In chezmoi.toml
[onepassword]
    prompt = true  # Enable interactive sign-in
```

### Usage in Templates

```text
{{ onepasswordRead "op://vault/item/field" }}
{{ (onepassword "item-uuid").fields.password.value }}
{{ onepasswordDocument "document-uuid" }}
```

## Bitwarden

### Setup

```bash
export BW_SESSION=$(bw unlock --raw)
```

### Usage in Templates

```text
{{ (bitwarden "item" "example.com").login.password }}
{{ (bitwardenFields "item" "example.com").api_key.value }}
{{ bitwardenAttachment "id_rsa" "item-uuid" }}
```

## macOS Keychain

### Setup

```bash
chezmoi secret keyring set --service=github --user=myuser
```

### Usage in Templates

```text
{{ keyring "github" "myuser" }}
```

## Age Encryption

### Setup

```bash
# Generate key
mkdir -p ~/.config/chezmoi
chezmoi age-keygen -o ~/.config/chezmoi/key.txt
```

```toml
# In chezmoi.toml
encryption = "age"
[age]
    identity = "~/.config/chezmoi/key.txt"
    recipient = "age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p"
```

### Usage

```bash
chezmoi add --encrypt ~/.ssh/id_rsa
chezmoi edit ~/.ssh/id_rsa  # Decrypts automatically
```

Encrypted files get the `encrypted_` prefix in the source state.

## GPG Encryption

### Setup

```toml
# In chezmoi.toml
encryption = "gpg"
[gpg]
    recipient = "your-email@example.com"
```

### Usage

```bash
chezmoi add --encrypt ~/.ssh/id_rsa
```

## Generic Secret Commands

Use the `secret` template function to run external commands:

```text
{{ secret "pass" "path/to/secret" }}
{{ secretJSON "vault" "kv/data/myapp" | fromJson | dig "data" "password" }}
```

## Best Practices

1. **Never commit unencrypted secrets** to version control
2. **Use `private_` prefix** for files containing secrets (sets 0600 permissions)
3. **Prefer password managers** over encrypted files when possible
4. **Store encryption keys securely** outside the repo
5. **Use environment variables** for CI/CD secrets

## Example: SSH Config with 1Password

```text
# private_dot_ssh/config.tmpl
Host github.com
    IdentityFile ~/.ssh/id_github
    IdentitiesOnly yes

Host work-server
    HostName {{ onepasswordRead "op://Work/Server/hostname" }}
    User {{ onepasswordRead "op://Work/Server/username" }}
    IdentityFile ~/.ssh/id_work
```

## Example: Git Config with Keychain

```text
# dot_gitconfig.tmpl
[user]
    name = Your Name
    email = your@email.com
    signingkey = {{ keyring "git" "signingkey" }}

[commit]
    gpgsign = true
```

## Debugging Secrets

```bash
# Test secret retrieval
chezmoi execute-template '{{ onepasswordRead "op://vault/item/field" }}'

# View decrypted content
chezmoi cat ~/.ssh/id_rsa

# Check what would be written
chezmoi diff
```
