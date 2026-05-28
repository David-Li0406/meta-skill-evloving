# Vault SSH Configuration Reference

## Terraform Configuration

### AppRole Authentication

```hcl
# Enable AppRole auth method
resource "vault_auth_backend" "approle" {
  type = "approle"
  path = "approle"
}

# Create AppRole role for AAP
resource "vault_approle_auth_backend_role" "aap" {
  backend        = vault_auth_backend.approle.path
  role_name      = var.tenant
  token_policies = [vault_policy.aap_ssh.name]

  # Security settings
  token_ttl     = 3600   # 1 hour
  token_max_ttl = 7200   # 2 hours
  secret_id_ttl = 86400  # 24 hours (rotate daily)
}

# Get role_id and secret_id for AAP configuration
resource "vault_approle_auth_backend_role_secret_id" "aap" {
  backend   = vault_auth_backend.approle.path
  role_name = vault_approle_auth_backend_role.aap.role_name
}

output "role_id" {
  value     = vault_approle_auth_backend_role.aap.role_id
  sensitive = true
}

output "secret_id" {
  value     = vault_approle_auth_backend_role_secret_id.aap.secret_id
  sensitive = true
}
```

### SSH Secrets Engine

```hcl
# Enable SSH secrets engine
resource "vault_mount" "ssh" {
  path        = "ssh"
  type        = "ssh"
  description = "SSH CA for AAP signed certificates"
}

# Configure SSH CA
resource "vault_ssh_secret_backend_ca" "ssh" {
  backend              = vault_mount.ssh.path
  generate_signing_key = true
}

# Create SSH signing role per tenant
resource "vault_ssh_secret_backend_role" "aap_tenant" {
  backend                 = vault_mount.ssh.path
  name                    = var.tenant
  key_type                = "ca"
  allow_user_certificates = true

  # User restrictions
  default_user  = "aap"
  allowed_users = "aap,ansible,root"

  # Certificate TTL (2 hours recommended)
  ttl     = "7200"
  max_ttl = "7200"

  # SSH extensions
  default_extensions = {
    "permit-pty" = ""
  }
  allowed_extensions = "permit-pty,permit-port-forwarding"
}
```

### Vault Policy

```hcl
resource "vault_policy" "aap_ssh" {
  name   = "aap-ssh-${var.tenant}"
  policy = <<-EOT
    # Allow SSH certificate signing for this tenant
    path "ssh/sign/${var.tenant}" {
      capabilities = ["read", "update"]
    }

    # Allow reading SSH CA public key
    path "ssh/config/ca" {
      capabilities = ["read"]
    }
  EOT
}

# Policy using identity templating (multi-tenant)
resource "vault_policy" "aap_ssh_templated" {
  name   = "aap-ssh-templated"
  policy = <<-EOT
    # Dynamic path based on entity identity
    path "ssh/sign/{{identity.entity.name}}" {
      capabilities = ["read", "update"]
    }
  EOT
}
```

### Multi-Tenancy with Namespaces (Enterprise)

```hcl
# Create tenant namespace
resource "vault_namespace" "tenant" {
  path = var.tenant
}

# SSH secrets engine in namespace
resource "vault_mount" "ssh_namespaced" {
  namespace   = vault_namespace.tenant.path
  path        = "ssh"
  type        = "ssh"
  description = "SSH CA for ${var.tenant}"
}
```

## Variables

```hcl
variable "tenant" {
  description = "Tenant/team name for multi-tenancy"
  type        = string
}

variable "vault_url" {
  description = "Vault cluster URL"
  type        = string
}

variable "vault_namespace" {
  description = "Vault namespace (Enterprise only)"
  type        = string
  default     = "admin"
}
```

## Credential Rotation

### Self-Rotation Policy

```hcl
# Allow AAP to rotate its own secret_id
path "auth/approle/role/${var.tenant}/secret-id" {
  capabilities = ["update"]
}
```

### Rotation Playbook Trigger

```yaml
# AAP job template for credential rotation
- name: Rotate Vault AppRole Secret ID
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Generate new secret_id
      community.hashi_vault.vault_write:
        url: "{{ vault_url }}"
        path: "auth/approle/role/{{ tenant }}/secret-id"
        auth_method: approle
        role_id: "{{ role_id }}"
        secret_id: "{{ current_secret_id }}"
      register: new_secret

    - name: Update AAP credential
      ansible.controller.credential:
        name: "vault_approle_{{ tenant }}"
        inputs:
          secret_id: "{{ new_secret.data.secret_id }}"
```
