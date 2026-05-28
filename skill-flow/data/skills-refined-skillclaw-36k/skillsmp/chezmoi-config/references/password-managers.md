# Chezmoi Password Manager Integrations

## Overview

Chezmoi integrates with 20+ password managers and secret stores, allowing you to securely retrieve secrets in templates without hardcoding them.

## Supported Password Managers

### 1Password

**Template functions:**
```go
{{ onepasswordItemFields "item-name" }}
{{ onepasswordDocument "document-id" }}
{{ onepassword "item-name" "vault" "account" "field" }}
```

**Examples:**
```go
{{ (onepasswordItemFields "GitHub").password.value }}
{{ (onepasswordItemFields "Work Email").password.value }}
{{ onepasswordDocument "api-keys" }}
```

**Configuration (.chezmoi.toml.tmpl):**
```toml
[onepassword]
    account = "my-account.1password.com"
```

### LastPass

**Template functions:**
```go
{{ lastpass "entry-id" }}
{{ lastpassRaw "entry-id" }}
```

**Examples:**
```go
{{ (index (lastpass "github.com") 0).password }}
{{ (index (lastpass "github.com") 0).username }}
```

**Configuration:**
```toml
[lastpass]
    # No configuration needed if lpass CLI is configured
```

### Bitwarden

**Template functions:**
```go
{{ bitwarden "item-id" }}
{{ bitwardenRaw "item-id" }}
{{ bitwardenFields "item-id" }}
{{ bitwardenAttachment "item-id" "attachment-name" }}
```

**Examples:**
```go
{{ (bitwarden "github").login.password }}
{{ (bitwarden "github").login.username }}
{{ (bitwarden "work").notes }}
```

**Bitwarden Secrets Manager:**
```go
{{ bitwardenSecrets "secret-id" }}
{{ bitwardenSecrets "secret-id" "access-token" }}
{{ (bitwardenSecrets "api-key").value }}
```

### KeePassXC

**Template functions:**
```go
{{ keepassxc "entry-name" }}
{{ keepassxcAttribute "entry-name" "attribute" }}
```

**Examples:**
```go
{{ (keepassxc "GitHub").Password }}
{{ keepassxcAttribute "GitHub" "UserName" }}
{{ keepassxcAttribute "GitHub" "URL" }}
```

### Pass (Password Store)

**Template functions:**
```go
{{ pass "path/to/entry" }}
{{ passRaw "path/to/entry" }}
```

**Examples:**
```go
{{ pass "email/work" }}
{{ pass "github/personal" }}
```

**Use alternative command (e.g., passage):**
```toml
[pass]
    command = "passage"
```

### Gopass

**Template functions:**
```go
{{ gopass "path/to/secret" }}
{{ gopassRaw "path/to/secret" }}
```

**Examples:**
```go
{{ gopass "work/api-keys/github" }}
{{ gopass "personal/tokens" }}
```

### Vault (HashiCorp)

**Template functions:**
```go
{{ vault "secret/data/item" }}
{{ vaultWithParameters "path" "key" (dict "field1" "value1") }}
```

**Examples:**
```go
{{ (vault "secret/data/github").data.password }}
{{ (vault "secret/data/aws").access_key }}
{{ (vault "secret/database").data.api_key }}
```

**Configuration:**
```toml
[vault]
    address = "https://vault.example.com:8200"
    # Use VAULT_TOKEN environment variable for authentication
```

### Dashlane

**Template functions:**
```go
{{ dashlane "item-id" }}
{{ dashlanePassword "item-id" }}
{{ dashlaneLogin "item-id" }}
```

**Examples:**
```go
{{ (dashlane "github").password }}
{{ (dashlane "work").login.email }}
```

### Doppler

**Template functions:**
```go
{{ doppler "SECRET_NAME" }}
```

**Examples:**
```go
{{ doppler "GITHUB_TOKEN" }}
{{ doppler "AWS_ACCESS_KEY_ID" }}
```

**Configuration:**
```toml
[doppler]
    # Use DOPPLER_TOKEN environment variable
```

### Generic Keyring

**Template functions:**
```go
{{ keyring "service" "user" }}
```

**Examples:**
```go
{{ keyring "github" "john@example.com" }}
{{ keyring "work VPN" "john" }}
```

### AWS Secrets Manager

**Template functions:**
```go
{{ awsSecretsManager "secret-name" }}
```

**Examples:**
```go
{{ (awsSecretsManager "github/token").password }}
{{ (awsSecretsManager "prod/db").username }}
```

### Azure Key Vault

**Template functions:**
```go
{{ azureKeyVault "secret-name" }}
{{ azureKeyVaultWithVersion "secret-name" "version" }}
```

**Examples:**
```go
{{ azureKeyVault "github-token" }}
{{ azureKeyVaultWithVersion "api-key" "version-id" }}
```

## Complete Template Examples

### Git Configuration with Secrets

**dot_gitconfig.tmpl:**
```go
[user]
    name = {{ .name }}
    email = {{ .email }}

{{- if (bitwarden "github") }}
[github]
    token = {{ (bitwarden "github").login.password }}
{{- end }}

{{- if eq .chezmoi.os "darwin" }}
[credential]
    helper = osxkeychain
{{- else if eq .chezmoi.os "linux" }}
[credential]
    helper = cache
{{- end }}
```

### SSH Configuration

**dot_ssh/config.tmpl:**
```go
Host github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

{{- if (keepassxc "Work SSH") }}
Host work.example.com
    User {{ keepassxcAttribute "Work SSH" "UserName" }}
    IdentityFile ~/.ssh/work_key
    Port {{ keepassxcAttribute "Work SSH" "Port" }}
{{- end }}
```

### Environment Variables

**run_once_set-env-secrets.sh.tmpl:**
```bash
#!/bin/bash
{{ if eq .chezmoi.os "darwin" -}}
{{- if (bitwarden "aws-credentials") }}
export AWS_ACCESS_KEY_ID="{{ (bitwarden "aws-credentials").login.username }}"
export AWS_SECRET_ACCESS_KEY="{{ (bitwarden "aws-credentials").login.password }}"
{{- end }}
{{- end }}
```

### Shell Configuration

**dot_zshrc.tmpl:**
```go
# GitHub CLI authentication
{{- if (onepasswordItemFields "GitHub") }}
export GITHUB_TOKEN="{{ (onepasswordItemFields "GitHub").password.value }}"
{{- end }}

# Docker Hub
{{- if (pass "docker-hub") }}
export DOCKERHUB_TOKEN="{{ pass "docker-hub" }}"
{{- end }}
```

## Best Practices

1. **Never commit secrets** - Only commit template code
2. **Use password managers** - Don't hardcode sensitive data
3. **Check availability** - Use conditional logic to handle missing secrets
4. **Test templates** - Verify secrets are retrieved correctly
5. **Document dependencies** - Note which password managers are required
6. **Use fallbacks** - Provide defaults when secrets are unavailable
7. **Secure access** - Ensure password manager CLI tools are authenticated

## Error Handling

**Check if secret exists:**
```go
{{- if (bitwarden "github") }}
token = {{ (bitwarden "github").login.password }}
{{- end }}
```

**Provide default:**
```go
{{ $token := (bitwarden "github").login.password | default "" }}
{{ if $token }}
token = {{ $token }}
{{ end }}
```

## Security Notes

- Password manager CLI tools must be installed and configured
- Secrets are retrieved at template execution time
- Ensure `.chezmoi.toml` (with any secrets) is in `.chezmoiignore`
- Use encrypted `.chezmoi.toml.tmpl` for sensitive configuration
- Never commit actual secrets to version control
