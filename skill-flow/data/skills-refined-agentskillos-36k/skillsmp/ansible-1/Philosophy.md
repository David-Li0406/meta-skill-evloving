# Ansible Philosophy - The Right Way to Automate

## Core Principle: Declarative > Imperative

Ansible describes **desired state**, not steps to get there.

**Imperative (scripting):**
```bash
if ! dpkg -l | grep -q docker-ce; then
    apt-get update
    apt-get install -y docker-ce
fi
```

**Declarative (Ansible):**
```yaml
- name: Docker is installed
  apt:
    name: docker-ce
    state: present
```

The declarative version:
- Handles the conditional automatically
- Reports `changed` vs `ok` status
- Works across different system states
- Self-documents intent

---

## Idempotency: The Golden Rule

**Every task must be safe to run multiple times.**

Ask yourself: "If I run this twice, will it break anything?"

### Idempotent Modules (prefer these)
- `apt`, `yum`, `package` - package management
- `file` - create directories, set permissions
- `copy`, `template` - deploy files
- `lineinfile`, `blockinfile` - modify files
- `systemd`, `service` - manage services
- `user`, `group` - manage accounts
- `mount` - manage mounts

### Non-Idempotent (use carefully)
- `shell`, `command` - raw commands
- `raw` - bypass Python requirement
- `script` - run local scripts remotely

When using `shell`/`command`, always add guards:
```yaml
# Guard with creates (file existence)
- name: Initialize database
  command: /opt/init-db.sh
  args:
    creates: /opt/.db-initialized

# Guard with when condition
- name: Join cluster
  command: /opt/join-cluster.sh
  when: not cluster_joined.stat.exists

# Guard with changed_when
- name: Check something
  command: cat /etc/something
  register: result
  changed_when: false  # Never reports changed
```

---

## Roles vs Inline Tasks: When to Abstract

### Use Inline Tasks When:
- Single-use playbook
- Simple, linear deployment
- Few tasks (< 20)
- No reuse anticipated

### Extract to Role When:
- Same tasks across multiple services
- Complex logic with handlers
- Need to parameterize behavior
- Publishing for others to use

**Your lab pattern:** Most services are single-use Docker deployments. Inline tasks are fine. Only extract to role when you see copy-paste across services.

---

## Variables: Layering and Precedence

Ansible has 22+ levels of variable precedence. For sanity, use these:

1. **inventory.yml** - Host-specific facts (IP, user)
2. **vars.yml** - Service configuration (ports, paths)
3. **vault.yml** - Secrets (passwords, API keys)
4. **-e flag** - One-off overrides

```yaml
# inventory.yml - WHERE to deploy
all:
  hosts:
    service:
      ansible_host: 10.0.0.155

# vars.yml - WHAT to deploy
service_port: 8080
data_path: /opt/service

# vault.yml - SECRETS
api_key: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  ...
```

---

## Handlers: React to Changes

Handlers run once at end of play, only if notified:

```yaml
tasks:
  - name: Deploy nginx config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: restart nginx

handlers:
  - name: restart nginx
    systemd:
      name: nginx
      state: restarted
```

**Key behaviors:**
- Handlers run in definition order, not notification order
- Multiple notifications = single handler run
- Use `meta: flush_handlers` to run immediately

---

## Error Handling

### Ignore Errors (when failure is acceptable)
```yaml
- name: Check if service exists
  command: systemctl status myservice
  register: result
  ignore_errors: yes
```

### Failed When (custom failure conditions)
```yaml
- name: Run health check
  uri:
    url: http://localhost/health
  register: health
  failed_when: health.json.status != 'ok'
```

### Block/Rescue (try/catch pattern)
```yaml
- block:
    - name: Try risky operation
      command: /opt/risky.sh
  rescue:
    - name: Handle failure
      debug:
        msg: "Operation failed, cleaning up..."
```

---

## Tags: Selective Execution

```yaml
tasks:
  - name: Install Docker
    apt:
      name: docker-ce
      state: present
    tags: [docker, install]

  - name: Deploy app
    copy:
      src: app/
      dest: /opt/app/
    tags: [deploy]
```

```bash
# Run only docker tasks
ansible-playbook playbook.yml --tags docker

# Skip deploy tasks
ansible-playbook playbook.yml --skip-tags deploy
```

---

## Debug Strategies

### Print Variables
```yaml
- debug:
    var: ansible_facts

- debug:
    msg: "Service IP is {{ ansible_host }}"
```

### Step Through
```bash
ansible-playbook playbook.yml --step  # Confirm each task
```

### Start at Task
```bash
ansible-playbook playbook.yml --start-at-task="Deploy config"
```

### Check Mode (Dry Run)
```bash
ansible-playbook playbook.yml --check --diff
```

---

## Anti-Patterns to Avoid

1. **Shell for everything** - Use modules first
2. **Hardcoded values** - Use variables
3. **No error handling** - Add `failed_when`, `ignore_errors` thoughtfully
4. **Massive playbooks** - Split into roles or includes
5. **Secrets in plain text** - Always use vault
6. **No idempotency guards** - Always test by running twice
