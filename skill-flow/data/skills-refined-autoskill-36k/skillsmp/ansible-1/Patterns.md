# Ansible Patterns - Your Lab Cookbook

## Service Deployment Template

Standard structure for a new Docker-based service:

```yaml
---
# playbook.yml - {{ service_name }}

- name: Configure {{ service_name }} VM
  hosts: service
  become: yes

  vars:
    service_name: myservice
    service_port: 8080
    data_path: /opt/{{ service_name }}

  pre_tasks:
    - name: Load vault secrets if available
      include_vars:
        file: vault.yml
      ignore_errors: yes
      no_log: yes

  tasks:
    # === System Setup ===
    - name: Update system packages
      apt:
        update_cache: yes
        upgrade: dist
        autoremove: yes

    - name: Install base utilities
      apt:
        name: [curl, wget, git, vim, htop, nfs-common]
        state: present

    # === Docker ===
    - name: Install Docker prerequisites
      apt:
        name: [ca-certificates, gnupg, lsb-release]
        state: present

    - name: Add Docker GPG key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present

    - name: Add Docker repository
      apt_repository:
        repo: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
        state: present

    - name: Install Docker
      apt:
        name: [docker-ce, docker-ce-cli, containerd.io, docker-compose-plugin]
        state: present
        update_cache: yes

    - name: Add ansible user to docker group
      user:
        name: ansible
        groups: docker
        append: yes

    - name: Start Docker service
      systemd:
        name: docker
        enabled: yes
        state: started

    # === NFS Mount (if needed) ===
    - name: Create mount point
      file:
        path: /mnt/media
        state: directory

    - name: Mount NFS share
      mount:
        path: /mnt/media
        src: "10.0.0.42:/tank/media"
        fstype: nfs
        state: mounted
        opts: defaults,_netdev
      ignore_errors: yes

    # === Application ===
    - name: Create application directory
      file:
        path: "{{ data_path }}"
        state: directory
        owner: ansible
        group: ansible

    - name: Deploy docker-compose.yml
      copy:
        src: files/docker-compose.yml
        dest: "{{ data_path }}/docker-compose.yml"
        owner: ansible
        group: ansible

    - name: Start services
      community.docker.docker_compose_v2:
        project_src: "{{ data_path }}"
        state: present
        pull: always

    # === Health Check ===
    - name: Wait for service
      uri:
        url: "http://localhost:{{ service_port }}"
        status_code: [200, 302, 401]
      register: health
      until: health.status in [200, 302, 401]
      retries: 30
      delay: 5
      failed_when: false

    - name: Display status
      debug:
        msg: "{{ service_name }} is {{ 'UP' if health.status is defined else 'DOWN' }} at http://{{ ansible_host }}:{{ service_port }}"
```

---

## Inventory Patterns

### Standard Service Inventory
```yaml
# inventory.yml
all:
  hosts:
    service:
      ansible_host: 10.0.0.155
      ansible_user: ansible
      ansible_become: yes
      ansible_python_interpreter: /usr/bin/python3
```

### Multi-Host with Proxmox
```yaml
all:
  children:
    proxmox:
      hosts:
        pve:
          ansible_host: 10.0.0.42
          ansible_user: root
    services:
      hosts:
        arr:
          ansible_host: 10.0.0.155
        kestra:
          ansible_host: 10.0.0.153
        immich:
          ansible_host: 10.0.0.154
  vars:
    ansible_user: ansible
    ansible_become: yes
```

---

## Vault Patterns

### Create Vault
```bash
# Create new encrypted file
ansible-vault create ansible/vault.yml

# Encrypt existing file
ansible-vault encrypt ansible/secrets.yml

# Edit encrypted file
ansible-vault edit ansible/vault.yml

# View without editing
ansible-vault view ansible/vault.yml
```

### Vault File Structure
```yaml
# vault.yml
vault_db_password: "supersecret123"
vault_api_key: "abc123def456"
vault_smtp_password: "mailpass"
```

### Using Vault Variables
```yaml
pre_tasks:
  - name: Load vault secrets
    include_vars:
      file: vault.yml
    ignore_errors: yes  # Allow running without vault
    no_log: yes         # Don't log secret values

tasks:
  - name: Configure database
    template:
      src: db.conf.j2
      dest: /opt/app/db.conf
    vars:
      db_password: "{{ vault_db_password }}"
```

### Running with Vault
```bash
# Prompt for password
ansible-playbook -i inventory.yml playbook.yml --ask-vault-pass

# Use password file
ansible-playbook -i inventory.yml playbook.yml --vault-password-file ~/.vault_pass

# Environment variable
export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass
ansible-playbook -i inventory.yml playbook.yml
```

---

## Docker Compose Patterns

### Basic Deployment
```yaml
- name: Deploy with docker-compose
  community.docker.docker_compose_v2:
    project_src: /opt/myapp
    state: present
```

### With Pull and Recreate
```yaml
- name: Deploy with fresh images
  community.docker.docker_compose_v2:
    project_src: /opt/myapp
    state: present
    pull: always
    recreate: always
```

### Using Shell (when module unavailable)
```yaml
- name: Start services via shell
  shell: |
    sg docker -c "cd /opt/myapp && docker compose pull && docker compose up -d"
  become_user: ansible
```

---

## File Management Patterns

### Copy Static Files
```yaml
- name: Deploy config
  copy:
    src: files/config.json
    dest: /opt/app/config.json
    owner: app
    group: app
    mode: '0644'
```

### Template with Variables
```yaml
- name: Deploy templated config
  template:
    src: templates/config.json.j2
    dest: /opt/app/config.json
    owner: app
    group: app
    mode: '0644'
```

### Synchronize Directory
```yaml
- name: Sync application files
  synchronize:
    src: app/
    dest: /opt/app/
    delete: yes  # Remove files not in source
```

### Modify Existing File
```yaml
# Single line
- name: Set timezone
  lineinfile:
    path: /etc/environment
    regexp: '^TZ='
    line: 'TZ=America/Chicago'

# Block of text
- name: Add custom config
  blockinfile:
    path: /etc/app.conf
    marker: "# {mark} ANSIBLE MANAGED BLOCK"
    block: |
      setting1=value1
      setting2=value2
```

---

## Service Management

### Systemd Service
```yaml
- name: Ensure service is running
  systemd:
    name: myservice
    enabled: yes
    state: started
    daemon_reload: yes  # If unit file changed
```

### Docker Container (standalone)
```yaml
- name: Run container
  community.docker.docker_container:
    name: myapp
    image: myapp:latest
    state: started
    restart_policy: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - /opt/myapp/data:/data
```

---

## Conditional Execution

### Based on Variable
```yaml
- name: Configure production
  template:
    src: prod.conf.j2
    dest: /opt/app/config.conf
  when: env == 'production'
```

### Based on Fact
```yaml
- name: Install on Ubuntu only
  apt:
    name: some-package
  when: ansible_distribution == 'Ubuntu'
```

### Based on File Existence
```yaml
- name: Check if initialized
  stat:
    path: /opt/app/.initialized
  register: init_file

- name: Initialize app
  command: /opt/app/init.sh
  when: not init_file.stat.exists
```

### Based on Previous Task
```yaml
- name: Check service status
  uri:
    url: http://localhost:8080/health
  register: health
  failed_when: false

- name: Restart if unhealthy
  systemd:
    name: myservice
    state: restarted
  when: health.status != 200
```

---

## Loops

### Simple List
```yaml
- name: Create directories
  file:
    path: "{{ item }}"
    state: directory
  loop:
    - /opt/app/data
    - /opt/app/logs
    - /opt/app/config
```

### With Index
```yaml
- name: Create numbered files
  copy:
    content: "File {{ idx }}"
    dest: "/opt/file{{ idx }}.txt"
  loop: "{{ range(1, 5) | list }}"
  loop_control:
    loop_var: idx
```

### Dict Items
```yaml
- name: Create users
  user:
    name: "{{ item.key }}"
    groups: "{{ item.value.groups }}"
  loop: "{{ users | dict2items }}"
  vars:
    users:
      alice:
        groups: [docker, sudo]
      bob:
        groups: [docker]
```

---

## Proxmox-Specific

### Create Directory on ZFS
```yaml
- name: Create ZFS directory structure
  file:
    path: "{{ item }}"
    state: directory
    mode: '2775'  # setgid for group inheritance
  loop:
    - /tank/media/downloads
    - /tank/media/library
```

### Check ZFS Properties
```yaml
- name: Check NFS export
  command: zfs get sharenfs tank/media
  register: sharenfs
  changed_when: false
```

### LXC Container Operations
```yaml
- name: Start LXC container
  command: pct start {{ container_id }}
  when: container_state != 'running'
```
