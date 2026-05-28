---
name: add-container
description: Use when adding a new LXC container to the Proxmox homelab - complete checklist covering Terraform provisioning, Ansible configuration, and documentation updates.
---

# Add Container Workflow

## Overview

Adding a container requires **Terraform for provisioning** and **Ansible for configuration**. This checklist ensures nothing is missed.

## Before Starting

1. Check `docs/reference/current-state.md` for:
   - Next available CTID (containers are 3XX)
   - Next available IP in the subnet
   - Existing patterns to follow

2. Identify a similar container to use as template:
   - Basic service: `backup.tf`
   - GPU workload: `jellyfin.tf` or `transcoder.tf`
   - Optical drive: `ripper.tf`

## Phase 1: Terraform Provisioning

### 1.1 Create Container Definition

Create `terraform/proxmox-homelab/<name>.tf`:

```hcl
resource "proxmox_virtual_environment_container" "<name>" {
  description = "<Description>"
  node_name   = "homelab"
  vm_id       = <CTID>

  initialization {
    hostname = "<name>"
    ip_config {
      ipv4 {
        address = "192.168.1.<IP>/24"
        gateway = "192.168.1.1"
      }
    }
    dns {
      servers = [local.dns_server]
    }
    user_account {
      keys = local.ssh_keys
    }
  }

  cpu {
    cores = <cores>
  }

  memory {
    dedicated = <memory_mb>
  }

  disk {
    datastore_id = "local-lvm"
    size         = <disk_gb>
  }

  operating_system {
    template_file_id = local.debian_template
    type             = "debian"
  }

  network_interface {
    name   = "eth0"
    bridge = "vmbr0"
  }

  # Add mount points if needed for media access
  # mount_point {
  #   volume = "/mnt/storage/media"
  #   path   = "/mnt/media"
  # }

  features {
    nesting = true  # Required for Docker/systemd
  }

  startup {
    order = "3"
  }

  lifecycle {
    ignore_changes = [initialization[0].user_account]
  }
}

output "<name>_container_id" {
  value = proxmox_virtual_environment_container.<name>.vm_id
}
```

### 1.2 Update Locals (if needed)

If adding new shared values, update `terraform/proxmox-homelab/locals.tf`.

### 1.3 Run Terraform Workflow

```bash
cd terraform/proxmox-homelab
terraform fmt
terraform validate
terraform plan
```

**Present plan to user. Get approval before applying.**

```bash
terraform apply
```

### 1.4 Verify Container Created

```bash
ssh <name>   # Uses ~/.ssh/config alias
```

## Phase 2: Ansible Configuration

### 2.1 Add to Inventory

Edit `ansible/inventory/hosts.yml`:

```yaml
all:
  children:
    containers:
      hosts:
        <name>:
          ansible_host: 192.168.1.<IP>
```

### 2.2 Create Playbook

Create `ansible/playbooks/<name>.yml`:

```yaml
---
- name: Configure <name>
  hosts: <name>
  become: true
  roles:
    - common
    # Add service-specific roles
```

### 2.3 Create Service Role (if needed)

```bash
mkdir -p ansible/roles/<service>/{tasks,handlers,templates,defaults,files}
```

Create `ansible/roles/<service>/tasks/main.yml`:

```yaml
---
- name: Install packages
  ansible.builtin.apt:
    name:
      - package1
      - package2
    state: present
    update_cache: true

- name: Configure service
  ansible.builtin.template:
    src: config.j2
    dest: /etc/<service>/config
    mode: "0644"
  notify: Restart <service>
```

Create `ansible/roles/<service>/handlers/main.yml`:

```yaml
---
- name: Restart <service>
  ansible.builtin.systemd:
    name: <service>
    state: restarted
    daemon_reload: true
```

### 2.4 Run Ansible Workflow

```bash
cd ansible
ansible-lint --offline
ansible-playbook playbooks/<name>.yml --syntax-check
ansible-playbook playbooks/<name>.yml --check
```

**Present dry-run output to user. Get approval before applying.**

```bash
ansible-playbook playbooks/<name>.yml
```

### 2.5 Verify Configuration

```bash
ssh <name>
systemctl status <service>
journalctl -u <service> -f
```

## Phase 3: Documentation

### 3.1 Update current-state.md

Add container to `docs/reference/current-state.md`:
- CTID and hostname
- IP address
- Purpose
- Any special notes (GPU, mount points, etc.)

### 3.2 Commit Changes

```bash
git add terraform/proxmox-homelab/<name>.tf
git add ansible/inventory/hosts.yml
git add ansible/playbooks/<name>.yml
git add ansible/roles/<service>/
git add docs/reference/current-state.md
git commit -m "feat: Add <name> container"
```

## Checklist Summary

Use TodoWrite to track each step:

- [ ] Check current-state.md for next CTID and IP
- [ ] Choose template container to copy from
- [ ] Create Terraform definition
- [ ] Run terraform fmt and validate
- [ ] Run terraform plan and review
- [ ] Get user approval for Terraform apply
- [ ] Run terraform apply
- [ ] Verify SSH access to new container
- [ ] Add to Ansible inventory
- [ ] Create playbook
- [ ] Create service role (if needed)
- [ ] Run ansible-lint and syntax-check
- [ ] Run ansible --check and review
- [ ] Get user approval for Ansible apply
- [ ] Run ansible-playbook
- [ ] Verify service is running
- [ ] Update current-state.md
- [ ] Commit all changes

## Special Cases

### GPU Passthrough

For containers needing GPU access:
1. Set `features.nesting = true` in Terraform
2. Add `privileged = true` if needed
3. Use `intel_gpu_passthrough` or `dual_gpu_passthrough` Ansible role
4. Role delegates to Proxmox host for IOMMU setup

### Optical Drive Passthrough

For containers needing optical drive:
1. Add device passthrough in Terraform
2. Use `optical_drive_passthrough` Ansible role

### Media Mount Points

For containers accessing media storage:
```hcl
mount_point {
  volume = "/mnt/storage/media"
  path   = "/mnt/media"
}
```

### Tailscale Access

After container is configured, add to Tailscale ACLs in `terraform/tailscale/`.
