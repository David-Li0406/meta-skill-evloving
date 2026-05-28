---
name: 1password
description: Complete 1Password CLI (op) for managing secrets, credentials, and secure storage. Use when working with: (1) Retrieving passwords, API keys, and secrets from vaults, (2) Managing items, documents, and secure notes, (3) Injecting secrets into environment variables and config files, (4) Automating credential rotation and management, (5) Accessing SSH keys and certificates, (6) Vault and item CRUD operations, (7) Secret references for CI/CD pipelines, (8) User and group management.
---

# 1Password CLI Skill

Complete 1Password operations for secure secret management and automation.

## Authentication

Before using any `op` commands, you must authenticate:

```bash
# Interactive sign-in (opens browser)
op signin

# Check authentication status
op account list

# Get current account info
op whoami

# Sign out
op signout
```

Once signed in, your session remains active for CLI operations.

## Vault Management

### List and Get Vaults

```bash
# List all vaults
op vault list

# List vaults with detailed output
op vault list --format json

# Get specific vault details
op vault get <vault-name-or-id>

# Get vault by name
op vault get "Private"
op vault get "Work"
```

### Create and Manage Vaults

```bash
# Create a new vault
op vault create <vault-name>
op vault create "DevOps Secrets"

# Delete a vault
op vault delete <vault-name-or-id>

# Grant user access to vault
op vault user grant --vault <vault-id> --user <user-email>

# Revoke user access
op vault user revoke --vault <vault-id> --user <user-email>
```

## Item Management

### Retrieving Items

```bash
# List all items
op item list

# List items in specific vault
op item list --vault "Private"

# List items with filtering
op item list --categories Login
op item list --tags production
op item list --format json

# Get complete item details
op item get <item-name-or-id>
op item get "GitHub Token"
op item get "AWS Credentials" --vault "Work"

# Get item in JSON format
op item get "GitHub Token" --format json
```

### Retrieving Specific Fields

```bash
# Get a specific field value
op item get <item-name> --fields <field-name>

# Examples
op item get "GitHub Token" --fields token
op item get "AWS Credentials" --fields "access key"
op item get "Database" --fields password

# Get multiple fields as JSON
op item get "AWS Credentials" --fields "access key,secret key" --format json

# Using field notation (for scripting)
op read "op://<vault>/<item>/<field>"
op read "op://Private/GitHub Token/token"
op read "op://Work/AWS Credentials/access key"
```

### Creating and Updating Items

```bash
# Create a new login item
op item create --category Login \
  --title "New Service" \
  --vault "Private" \
  --url "https://example.com" \
  username=user@example.com \
  password=<generate-password>

# Create item with custom fields
op item create --category Password \
  --title "API Key" \
  --vault "Work" \
  api_key=sk-xxx \
  environment=production

# Create secure note
op item create --category "Secure Note" \
  --title "Deployment Notes" \
  --vault "Work" \
  notesPlain="Important deployment information"

# Update an existing item
op item edit <item-name> <field>=<value>
op item edit "GitHub Token" token=ghp_newtoken123

# Add tags to item
op item edit "AWS Credentials" --tags production,terraform

# Generate and update password
op item edit "Database Login" password=<generate-password>
```

### Deleting Items

```bash
# Delete an item
op item delete <item-name-or-id>
op item delete "Old API Key" --vault "Work"

# Delete with confirmation skip
op item delete "Old Token" --archive
```

## Secret References

Use secret references to inject 1Password secrets into applications without exposing them:

```bash
# Secret reference syntax
op://[vault]/[item]/[field]

# Examples
op://Private/GitHub Token/token
op://Work/AWS Credentials/access key
op://DevOps/Database/password

# Using op run to inject secrets into commands
op run -- env
op run -- npm run build
op run -- terraform apply

# Using op inject with templates
echo 'DB_PASSWORD=op://Work/Database/password' | op inject
cat .env.template | op inject > .env
```

### Environment Variable Injection

```bash
# Create a template file with secret references
cat <<EOF > .env.template
DATABASE_URL=op://Work/Database/connection_string
API_KEY=op://Work/Service/api_key
SECRET_TOKEN=op://Work/Service/secret
EOF

# Inject secrets and write to file
op inject -i .env.template -o .env

# Or pipe directly
cat .env.template | op inject > .env

# Use with op run for temporary injection
op run --env-file=.env.template -- node app.js
```

## Document Management

```bash
# List documents
op document list

# Get a document
op document get <document-name> --output <local-path>
op document get "SSL Certificate" --output ./cert.pem

# Create/upload a document
op document create <file-path> --title "Document Name" --vault "Work"
op document create ./config.yaml --title "K8s Config" --vault "DevOps"

# Delete a document
op document delete <document-name>
```

## SSH Key Management

```bash
# List SSH keys
op item list --categories "SSH Key"

# Get SSH private key
op item get "GitHub SSH Key" --fields "private key" > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa

# Get SSH public key
op item get "GitHub SSH Key" --fields "public key" > ~/.ssh/id_rsa.pub

# Using secret reference for SSH key
op read "op://Private/GitHub SSH Key/private key" > ~/.ssh/id_rsa
```

## Password Generation

```bash
# Generate a password with defaults
op item create --generate-password

# Generate password with specific requirements
op item create --generate-password=<length>,letters,digits,symbols

# Examples
op item create --category Login \
  --title "New Service" \
  --generate-password=32,letters,digits,symbols

# Generate password manually
op generate --length 20 --symbols

# Generate PIN
op generate --length 6 --digits
```

## User and Group Management

```bash
# List users
op user list

# Get user details
op user get <user-email>

# Provision new user
op user provision --email user@example.com --name "User Name"

# Suspend user
op user suspend <user-email>

# Reactivate user
op user confirm <user-email>

# List groups
op group list

# Get group details
op group get <group-name>

# Add user to group
op group user grant --group <group-name> --user <user-email>

# Remove user from group
op group user revoke --group <group-name> --user <user-email>
```

## Template-Based Item Creation

```bash
# List available item templates
op item template list

# Get template for specific category
op item template get Login
op item template get Password
op item template get "API Credential"

# Create item from template with JSON
cat <<EOF | op item create -
{
  "vault": "Work",
  "title": "New API",
  "category": "API_CREDENTIAL",
  "fields": [
    {
      "id": "username",
      "type": "STRING",
      "label": "username",
      "value": "api_user"
    },
    {
      "id": "credential",
      "type": "CONCEALED",
      "label": "credential",
      "value": "secret_api_key"
    }
  ]
}
EOF
```

## Common Workflows

### Automated Secret Rotation

```bash
# Get current API key
CURRENT_KEY=$(op item get "Service API" --fields api_key)

# Generate new key (external service)
NEW_KEY=$(curl -X POST https://api.service.com/rotate \
  -H "Authorization: Bearer $CURRENT_KEY")

# Update 1Password
op item edit "Service API" api_key="$NEW_KEY"
```

### CI/CD Integration

```bash
# Store secrets in 1Password
op item create --category Password \
  --title "GitHub Actions Token" \
  --vault "CI/CD" \
  token=ghp_xxxxx

# Reference in scripts using op run
op run --env-file=.env.template -- ./deploy.sh

# Or use secret references directly
export GITHUB_TOKEN=$(op read "op://CI/CD/GitHub Actions Token/token")
```

### Backup Configuration with Secrets

```bash
# Create config template
cat <<EOF > config.template.yaml
database:
  host: db.example.com
  user: op://Work/Database/username
  password: op://Work/Database/password
api:
  key: op://Work/API/key
  secret: op://Work/API/secret
EOF

# Generate actual config
op inject -i config.template.yaml -o config.yaml

# Use in application
op run --env-file=config.template.yaml -- ./app
```

### SSH Key Deployment

```bash
# Deploy SSH key from 1Password
op item get "GitHub Deploy Key" --fields "private key" > ~/.ssh/deploy_key
chmod 600 ~/.ssh/deploy_key

# Add to SSH config
cat <<EOF >> ~/.ssh/config
Host github-deploy
  HostName github.com
  User git
  IdentityFile ~/.ssh/deploy_key
EOF

# Use it
git clone git@github-deploy:org/repo.git
```

### Database Connection Strings

```bash
# Store connection string in 1Password as item
op item create --category Password \
  --title "Production DB" \
  --vault "Work" \
  connection_string="postgresql://user:pass@host:5432/db"

# Retrieve and use
export DATABASE_URL=$(op item get "Production DB" --fields connection_string)
psql "$DATABASE_URL"

# Or use with op run
op run -- psql $(op read "op://Work/Production DB/connection_string")
```

## Output Formats

```bash
# JSON output (for parsing)
op item list --format json
op vault list --format json
op item get "Item" --format json

# Human-readable table (default)
op item list

# Piping to jq for filtering
op item list --format json | jq '.[] | select(.vault.id == "vaultid")'
op item get "AWS" --format json | jq -r '.fields[] | select(.label == "access key") | .value'
```

## Advanced Filtering and Queries

```bash
# Filter items by category
op item list --categories Login,Password
op item list --categories "API Credential"

# Filter by tags
op item list --tags production
op item list --tags "production,critical"

# Filter by vault
op item list --vault "Work"

# Combine filters
op item list --vault "Work" --categories Login --tags production --format json

# Search items
op item list --format json | jq '.[] | select(.title | contains("AWS"))'
```

## Service Account Integration

For automation and CI/CD without human interaction:

```bash
# Using service account token
export OP_SERVICE_ACCOUNT_TOKEN=<token>

# All commands work with service account
op item list
op read "op://Work/API/key"

# In CI/CD pipeline
echo $OP_SERVICE_ACCOUNT_TOKEN | op signin
op run -- ./deploy.sh
```

## Shell Plugins

1Password CLI integrates with shell for autocompletion and aliases:

```bash
# Enable shell completion (add to .bashrc/.zshrc)
eval "$(op completion zsh)"
eval "$(op completion bash)"

# Shell plugin for biometric unlock
# Automatically unlocks 1Password using Touch ID/biometric
# Install and configure via 1Password app settings
```

## Error Handling

```bash
# Check if item exists before operations
if op item get "Service Token" &>/dev/null; then
  TOKEN=$(op item get "Service Token" --fields token)
else
  echo "Item not found"
  exit 1
fi

# Handle missing fields gracefully
TOKEN=$(op item get "Service" --fields token 2>/dev/null || echo "")
if [ -z "$TOKEN" ]; then
  echo "Token field not found"
fi

# Verify authentication before operations
if ! op account list &>/dev/null; then
  echo "Not signed in to 1Password"
  op signin
fi
```

## Security Best Practices

1. **Use Secret References**: Always use `op://` references in templates instead of hardcoding secrets
2. **Limit Service Account Permissions**: Create service accounts with minimal required vault access
3. **Rotate Regularly**: Automate secret rotation workflows
4. **Audit Access**: Regularly review vault access and user permissions
5. **Use Categories**: Organize items by category for better access control
6. **Tag Appropriately**: Use tags for environment (prod, staging) and criticality
7. **Document Items**: Add notes and metadata to items for context
8. **Never Log Secrets**: When using `op run`, ensure applications don't log injected secrets

## Troubleshooting

```bash
# Check CLI version
op --version

# Update CLI
brew upgrade 1password-cli  # macOS
# or download latest from 1password.com/downloads

# Clear session
op signout --all

# Verbose output for debugging
op item get "Item" --debug

# Check account status
op account list
op whoami

# Verify vault access
op vault list
op vault get "Vault Name"
```

## Integration Examples

### Terraform

```terraform
# .env.template
export TF_VAR_api_key=op://Work/Service/api_key
export TF_VAR_secret=op://Work/Service/secret

# Run terraform with injected secrets
op run --env-file=.env.template -- terraform apply
```

### Docker Compose

```yaml
# docker-compose.template.yml
services:
  app:
    environment:
      DB_PASSWORD: op://Work/Database/password
      API_KEY: op://Work/Service/api_key

# Run with secret injection
op run -- docker-compose -f docker-compose.template.yml up
```

### Kubernetes

```bash
# Create secret from 1Password
kubectl create secret generic app-secrets \
  --from-literal=api-key=$(op read "op://Work/API/key") \
  --from-literal=db-password=$(op read "op://Work/DB/password")
```

For more information, see the [1Password CLI documentation](https://developer.1password.com/docs/cli/).
