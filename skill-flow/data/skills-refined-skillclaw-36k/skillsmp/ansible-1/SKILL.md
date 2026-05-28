---
name: Ansible
version: 1.0.0
description: Infrastructure automation for Proxmox lab services. USE WHEN deploying services, configuring VMs/LXCs, managing Docker stacks, or automating lab infrastructure.
---

# Ansible - Infrastructure as Code for Lab Services

**Declarative service deployment.** Ansible manages your Proxmox lab - VMs, LXCs, Docker stacks, NFS mounts, and secrets.

---

## Your Lab Pattern

Every service follows the same structure:

```
<service>/
├── ansible/
│   ├── playbook.yml      # Main entrypoint
│   ├── inventory.yml     # Target hosts
│   ├── vars.yml          # Service-specific variables (optional)
│   ├── vault.yml         # Encrypted secrets (optional)
│   ├── files/            # Static files (docker-compose.yml, configs)
│   ├── templates/        # Jinja2 templates (.j2)
│   └── roles/            # Reusable role (optional)
│       └── <service>/
│           ├── tasks/main.yml
│           ├── handlers/main.yml
│           └── files/
└── terraform/            # VM/LXC provisioning (if applicable)
```

**Run from service directory:**
```bash
cd /home/beau/src/personal/lab/<service>
ansible-playbook -i ansible/inventory.yml ansible/playbook.yml
```

---

## Philosophy: Idempotent by Default

Ansible's power is **idempotency** - run it once or 100 times, same result.

**Good (idempotent):**
```yaml
- name: Ensure Docker is installed
  apt:
    name: docker-ce
    state: present  # Only installs if missing
```

**Bad (not idempotent):**
```yaml
- name: Install Docker
  shell: curl -fsSL https://get.docker.com | sh  # Runs every time
```

If you MUST use `shell`/`command`, add `creates:` or `when:` guards:
```yaml
- name: Initialize something
  shell: /opt/init.sh
  args:
    creates: /opt/.initialized  # Skip if file exists
```

---

## Common Patterns

### 1. Docker Stack Deployment

Your standard pattern for services like arr, kestra, immich:

```yaml
- name: Deploy {{ service_name }}
  hosts: service
  become: yes

  tasks:
    - name: Create app directory
      file:
        path: /opt/{{ service_name }}
        state: directory
        owner: ansible
        group: ansible

    - name: Deploy docker-compose.yml
      copy:
        src: files/docker-compose.yml
        dest: /opt/{{ service_name }}/docker-compose.yml

    - name: Start services
      community.docker.docker_compose_v2:
        project_src: /opt/{{ service_name }}
        state: present
        pull: always
```

### 2. NFS Mount (from Proxmox ZFS)

```yaml
- name: Mount NFS share
  mount:
    path: /mnt/media
    src: "10.0.0.42:/tank/media"
    fstype: nfs
    state: mounted
    opts: defaults,_netdev
```

### 3. Vault for Secrets

```bash
# Create encrypted vault
ansible-vault create ansible/vault.yml

# Edit existing vault
ansible-vault edit ansible/vault.yml

# Run playbook with vault
ansible-playbook -i ansible/inventory.yml ansible/playbook.yml --ask-vault-pass
```

In playbook:
```yaml
pre_tasks:
  - name: Load vault secrets
    include_vars:
      file: vault.yml
    ignore_errors: yes
    no_log: yes
```

### 4. Health Check Pattern

```yaml
- name: Wait for service to be ready
  uri:
    url: http://localhost:8080
    status_code: [200, 302, 401]
  register: service_ready
  until: service_ready.status in [200, 302, 401]
  retries: 30
  delay: 5
  failed_when: false
```

---

## Inventory Patterns

### Single Host
```yaml
all:
  hosts:
    service:
      ansible_host: 10.0.0.155
      ansible_user: ansible
      ansible_become: yes
```

### Multi-Host with Groups
```yaml
all:
  children:
    proxmox:
      hosts:
        pve:
          ansible_host: 10.0.0.42
    services:
      hosts:
        arr:
          ansible_host: 10.0.0.155
        kestra:
          ansible_host: 10.0.0.153
```

---

## Quick Command Reference

```bash
# Dry run (check mode)
ansible-playbook -i inventory.yml playbook.yml --check

# Run specific tags
ansible-playbook -i inventory.yml playbook.yml --tags "docker,deploy"

# Limit to specific host
ansible-playbook -i inventory.yml playbook.yml --limit "arr"

# Extra variables
ansible-playbook -i inventory.yml playbook.yml -e "service_version=2.0"

# Verbose output
ansible-playbook -i inventory.yml playbook.yml -vvv
```

---

## Context Files

- `Philosophy.md` - Deep dive on idempotency, roles vs inline, when to abstract
- `Patterns.md` - Your lab-specific patterns, Docker, NFS, Proxmox integration
- `Reference.md` - Module quick reference for common tasks

---

## Decision Tree

```
What are you automating?
        │
        ├─→ New service? → Copy template-vm or template-lxc structure
        │
        ├─→ Single playbook task? → Inline in playbook.yml
        │
        ├─→ Reusable across services? → Extract to role
        │
        └─→ Secrets involved? → Use vault.yml + include_vars
```
