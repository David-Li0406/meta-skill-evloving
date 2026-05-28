# Ansible

**Category**: developer-tools/infrastructure
**Description**: Ansible - agentless automation platform for configuration management and deployment
**Homepage**: https://www.ansible.com

## Package Detection

### PYPI
- `ansible`
- `ansible-core`
- `ansible-lint`
- `molecule`

## Configuration Files

- `ansible.cfg`
- `playbook.yml`
- `playbook.yaml`
- `site.yml`
- `site.yaml`
- `inventory`
- `inventory.yml`
- `inventory.yaml`
- `hosts`
- `hosts.yml`
- `requirements.yml`
- `galaxy.yml`
- `meta/main.yml`

## Directory Patterns

- `roles/`
- `playbooks/`
- `inventories/`
- `group_vars/`
- `host_vars/`
- `templates/`
- `files/`
- `handlers/`
- `tasks/`
- `vars/`
- `defaults/`

## Environment Variables

- `ANSIBLE_CONFIG`
- `ANSIBLE_INVENTORY`
- `ANSIBLE_ROLES_PATH`
- `ANSIBLE_VAULT_PASSWORD_FILE`
- `ANSIBLE_HOST_KEY_CHECKING`

## Detection Notes

- Look for ansible.cfg in repository root
- Check for playbooks/ or roles/ directories
- YAML files with tasks, handlers, vars sections
- Look for Jinja2 templates (.j2)
- Check for ansible-vault encrypted files

## Detection Confidence

- **ansible.cfg Detection**: 95% (HIGH)
- **Directory Structure Detection**: 90% (HIGH)
- **Package Detection**: 90% (HIGH)
