# Ansible Reference - Module Quick Guide

## Package Management

### apt (Debian/Ubuntu)
```yaml
- apt:
    name: nginx              # Single package
    name: [nginx, curl]      # Multiple packages
    state: present           # Install (default)
    state: latest            # Upgrade to latest
    state: absent            # Remove
    update_cache: yes        # apt update first
    cache_valid_time: 3600   # Cache validity in seconds
```

### package (Generic)
```yaml
- package:
    name: nginx
    state: present
```

---

## File Operations

### file
```yaml
- file:
    path: /opt/app
    state: directory         # Create directory
    state: touch             # Create empty file
    state: absent            # Delete
    state: link              # Symlink (requires src)
    owner: app
    group: app
    mode: '0755'             # Always quote octal
    recurse: yes             # Apply to contents (dir only)
```

### copy
```yaml
- copy:
    src: files/config.json   # Local file
    dest: /opt/app/config.json
    content: "inline content" # OR inline content
    owner: app
    group: app
    mode: '0644'
    backup: yes              # Backup existing file
```

### template
```yaml
- template:
    src: config.j2           # Jinja2 template
    dest: /opt/app/config
    owner: app
    mode: '0644'
```

### lineinfile
```yaml
- lineinfile:
    path: /etc/hosts
    regexp: '^127\.0\.0\.1'  # Match pattern
    line: '127.0.0.1 localhost myhost'
    state: present           # Ensure line exists
    state: absent            # Remove matching lines
    create: yes              # Create file if missing
    backup: yes
```

### blockinfile
```yaml
- blockinfile:
    path: /etc/config
    marker: "# {mark} MANAGED BY ANSIBLE"
    block: |
      setting1=value1
      setting2=value2
    insertafter: EOF         # Where to insert
```

### fetch (remote -> local)
```yaml
- fetch:
    src: /var/log/app.log
    dest: ./logs/
    flat: yes                # Don't create host subdirs
```

### synchronize (rsync)
```yaml
- synchronize:
    src: app/
    dest: /opt/app/
    delete: yes              # Mirror (remove extra files)
    rsync_opts:
      - "--exclude=*.log"
```

---

## User/Group Management

### user
```yaml
- user:
    name: appuser
    state: present
    groups: [docker, sudo]   # Additional groups
    append: yes              # Don't remove from other groups
    shell: /bin/bash
    home: /home/appuser
    create_home: yes
    password: "{{ password_hash }}"
    generate_ssh_key: yes
```

### group
```yaml
- group:
    name: appgroup
    state: present
    gid: 1000
```

### authorized_key
```yaml
- authorized_key:
    user: appuser
    key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
    state: present
```

---

## Service Management

### systemd
```yaml
- systemd:
    name: nginx
    state: started           # Start now
    state: stopped
    state: restarted
    state: reloaded
    enabled: yes             # Start on boot
    daemon_reload: yes       # Reload unit files
```

### service (generic)
```yaml
- service:
    name: nginx
    state: started
    enabled: yes
```

---

## Network

### uri (HTTP requests)
```yaml
- uri:
    url: http://localhost:8080/health
    method: GET              # GET, POST, PUT, DELETE
    status_code: [200, 201]  # Expected codes
    body_format: json
    body:
      key: value
    headers:
      Authorization: "Bearer {{ token }}"
    return_content: yes      # Include response body
    timeout: 30
```

### get_url (download)
```yaml
- get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz
    checksum: sha256:abc123...
    mode: '0644'
```

### wait_for
```yaml
- wait_for:
    host: localhost
    port: 8080
    state: started
    delay: 5                 # Wait before checking
    timeout: 300
```

---

## Mount

### mount
```yaml
- mount:
    path: /mnt/data
    src: 10.0.0.42:/tank/data
    fstype: nfs
    opts: defaults,_netdev
    state: mounted           # Mount and add to fstab
    state: present           # Add to fstab only
    state: unmounted         # Unmount but keep in fstab
    state: absent            # Unmount and remove from fstab
```

---

## Docker

### docker_container
```yaml
- community.docker.docker_container:
    name: myapp
    image: myapp:latest
    state: started
    restart_policy: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - /host/path:/container/path
    env:
      DEBUG: "true"
    networks:
      - name: mynetwork
```

### docker_compose_v2
```yaml
- community.docker.docker_compose_v2:
    project_src: /opt/myapp
    state: present           # Up
    state: absent            # Down
    pull: always             # Pull before up
    recreate: always         # Force recreate
    remove_orphans: yes
```

### docker_image
```yaml
- community.docker.docker_image:
    name: myapp
    tag: latest
    source: pull             # Pull from registry
    state: present
```

### docker_network
```yaml
- community.docker.docker_network:
    name: mynetwork
    driver: bridge
    state: present
```

---

## Command Execution

### command (simple)
```yaml
- command: /opt/app/init.sh
  args:
    chdir: /opt/app          # Working directory
    creates: /opt/app/.done  # Skip if exists
```

### shell (with pipes, etc)
```yaml
- shell: cat /etc/passwd | grep root
  args:
    executable: /bin/bash
  register: result
  changed_when: false        # Never report changed
```

### script (run local script remotely)
```yaml
- script: scripts/setup.sh
  args:
    creates: /opt/.setup-done
```

---

## Variables and Facts

### set_fact
```yaml
- set_fact:
    my_var: "computed value"
    another_var: "{{ some_var | upper }}"
```

### include_vars
```yaml
- include_vars:
    file: vars/{{ env }}.yml

- include_vars:
    dir: vars/
    extensions: [yml, yaml]
```

### debug
```yaml
- debug:
    var: ansible_facts       # Print variable
    msg: "Value is {{ var }}" # Print message
    verbosity: 2             # Only at -vv or higher
```

---

## Control Flow

### include_tasks
```yaml
- include_tasks: tasks/docker.yml
  when: install_docker | bool
```

### import_tasks
```yaml
- import_tasks: tasks/common.yml
```

### block/rescue/always
```yaml
- block:
    - name: Risky task
      command: /opt/risky.sh
  rescue:
    - name: Handle failure
      debug:
        msg: "Task failed, cleaning up"
  always:
    - name: Always run
      debug:
        msg: "Cleanup complete"
```

---

## Common Filters

```yaml
# String manipulation
"{{ var | upper }}"
"{{ var | lower }}"
"{{ var | replace('old', 'new') }}"
"{{ var | regex_replace('^prefix_', '') }}"

# Default values
"{{ var | default('fallback') }}"
"{{ var | default(omit) }}"  # Omit parameter entirely

# Lists
"{{ list | first }}"
"{{ list | last }}"
"{{ list | unique }}"
"{{ list | flatten }}"
"{{ list | join(',') }}"

# Dicts
"{{ dict | dict2items }}"
"{{ items | items2dict }}"

# JSON/YAML
"{{ var | to_json }}"
"{{ var | to_yaml }}"
"{{ json_string | from_json }}"

# Path manipulation
"{{ path | basename }}"
"{{ path | dirname }}"
"{{ path | expanduser }}"

# Type conversion
"{{ var | int }}"
"{{ var | bool }}"
"{{ var | string }}"
```

---

## Useful Lookups

```yaml
# File content
"{{ lookup('file', '/path/to/file') }}"

# Environment variable
"{{ lookup('env', 'HOME') }}"

# Password generation
"{{ lookup('password', '/dev/null length=16 chars=ascii_letters,digits') }}"

# Template
"{{ lookup('template', 'template.j2') }}"

# First found file
"{{ lookup('first_found', ['file1.yml', 'file2.yml']) }}"
```
