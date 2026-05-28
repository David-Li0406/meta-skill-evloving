# Golden Image Configuration Reference

## Packer Template

```hcl
# packer/vault-ssh-image.pkr.hcl

packer {
  required_plugins {
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = "~> 1"
    }
  }
}

variable "vault_url" {
  type        = string
  description = "Vault cluster URL"
}

variable "vault_namespace" {
  type        = string
  description = "Vault namespace"
  default     = "admin"
}

source "amazon-ebs" "rhel9" {
  ami_name      = "aap-vault-ssh-{{timestamp}}"
  instance_type = "t3.medium"
  region        = "us-east-1"

  source_ami_filter {
    filters = {
      name                = "RHEL-9*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    owners      = ["309956199498"]
    most_recent = true
  }

  ssh_username = "ec2-user"
}

build {
  sources = ["source.amazon-ebs.rhel9"]

  provisioner "ansible" {
    playbook_file = "./ansible/configure-ssh-ca.yml"
    extra_arguments = [
      "-e", "vault_url=${var.vault_url}",
      "-e", "vault_namespace=${var.vault_namespace}"
    ]
  }
}
```

## Ansible Provisioner Playbook

```yaml
# ansible/configure-ssh-ca.yml
---
- name: Configure SSH CA Trust for Vault
  hosts: all
  become: true
  vars:
    vault_url: "{{ lookup('env', 'VAULT_URL') }}"
    vault_namespace: "{{ lookup('env', 'VAULT_NAMESPACE') | default('admin') }}"
    ssh_ca_path: /etc/ssh/trusted-user-ca-keys.pem
    aap_user: aap

  tasks:
    - name: Create AAP service user
      ansible.builtin.user:
        name: "{{ aap_user }}"
        comment: "Ansible Automation Platform service account"
        shell: /bin/bash
        create_home: true
        state: present

    - name: Add AAP user to sudoers
      ansible.builtin.lineinfile:
        path: /etc/sudoers.d/aap
        line: "{{ aap_user }} ALL=(ALL) NOPASSWD: ALL"
        create: true
        mode: '0440'
        validate: 'visudo -cf %s'

    - name: Download Vault SSH CA public key
      ansible.builtin.get_url:
        url: "{{ vault_url }}/v1/ssh/public_key"
        headers:
          X-Vault-Namespace: "{{ vault_namespace }}"
        dest: "{{ ssh_ca_path }}"
        mode: '0644'
      register: ca_download

    - name: Configure SSH to trust Vault CA
      ansible.builtin.blockinfile:
        path: /etc/ssh/sshd_config
        block: |
          # Vault SSH CA Configuration
          TrustedUserCAKeys {{ ssh_ca_path }}
          PubkeyAuthentication yes
          AuthorizedPrincipalsFile none
        marker: "# {mark} VAULT SSH CA CONFIG"
      notify: Restart SSH

    - name: Ensure PubkeyAuthentication is enabled
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PubkeyAuthentication'
        line: 'PubkeyAuthentication yes'
      notify: Restart SSH

  handlers:
    - name: Restart SSH
      ansible.builtin.service:
        name: sshd
        state: restarted
```

## Cloud-Init UserData (Alternative)

```yaml
#cloud-config
# For dynamic configuration without baking into image

write_files:
  - path: /etc/ssh/fetch-vault-ca.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      VAULT_URL="${VAULT_URL:-https://vault.example.com:8200}"
      VAULT_NS="${VAULT_NAMESPACE:-admin}"

      curl -sf -H "X-Vault-Namespace: $VAULT_NS" \
        "$VAULT_URL/v1/ssh/public_key" \
        -o /etc/ssh/trusted-user-ca-keys.pem

      chmod 644 /etc/ssh/trusted-user-ca-keys.pem

      grep -q "TrustedUserCAKeys" /etc/ssh/sshd_config || \
        echo "TrustedUserCAKeys /etc/ssh/trusted-user-ca-keys.pem" >> /etc/ssh/sshd_config

      systemctl restart sshd

runcmd:
  - /etc/ssh/fetch-vault-ca.sh

users:
  - name: aap
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
```

## Terraform EC2 with UserData

```hcl
resource "aws_instance" "managed_node" {
  ami           = data.aws_ami.vault_ssh_enabled.id
  instance_type = "t3.medium"

  user_data = templatefile("${path.module}/userdata.tftpl", {
    vault_url       = var.vault_url
    vault_namespace = var.vault_namespace
  })

  tags = {
    Name        = "managed-node-${count.index}"
    ManagedBy   = "AAP"
    VaultSSH    = "enabled"
  }
}
```

## Verification Script

```bash
#!/bin/bash
# verify-ssh-ca.sh - Run on target hosts to verify configuration

echo "=== Vault SSH CA Verification ==="

# Check CA file exists
if [[ -f /etc/ssh/trusted-user-ca-keys.pem ]]; then
    echo "✅ CA file exists"
    echo "   Fingerprint: $(ssh-keygen -lf /etc/ssh/trusted-user-ca-keys.pem)"
else
    echo "❌ CA file missing: /etc/ssh/trusted-user-ca-keys.pem"
fi

# Check sshd_config
if grep -q "TrustedUserCAKeys" /etc/ssh/sshd_config; then
    echo "✅ TrustedUserCAKeys configured"
else
    echo "❌ TrustedUserCAKeys not in sshd_config"
fi

# Check PubkeyAuthentication
if grep -E "^PubkeyAuthentication\s+yes" /etc/ssh/sshd_config; then
    echo "✅ PubkeyAuthentication enabled"
else
    echo "⚠️  PubkeyAuthentication may not be enabled"
fi

# Check AAP user
if id aap &>/dev/null; then
    echo "✅ AAP user exists"
else
    echo "❌ AAP user missing"
fi

# Check sudo access
if sudo -l -U aap &>/dev/null; then
    echo "✅ AAP user has sudo access"
else
    echo "❌ AAP user lacks sudo access"
fi

echo "=== Verification Complete ==="
```
