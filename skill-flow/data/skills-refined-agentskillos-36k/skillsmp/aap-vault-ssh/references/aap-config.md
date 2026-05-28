# AAP Configuration Reference

## Credential Types

### HashiCorp Vault Signed SSH Credential

```yaml
- name: Configure Vault SSH AppRole Credential
  ansible.controller.credential:
    name: "hashicorp_vault_ssh_approle_{{ tenant }}"
    organization: "{{ organization_name }}"
    credential_type: "HashiCorp Vault Signed SSH"
    inputs:
      url: "{{ vault_url }}"
      role_id: "{{ role_id }}"
      secret_id: "{{ secret_id }}"
      default_auth_path: "{{ auth_path | default('approle') }}"
      namespace: "{{ vault_namespace | default(omit) }}"
    validate_certs: true
    state: present
```

### Machine Credential with Vault Source

```yaml
# Step 1: Create machine credential
- name: Create Machine Credential
  ansible.controller.credential:
    name: "vault_ssh_machine_{{ tenant }}"
    organization: "{{ organization_name }}"
    credential_type: "Machine"
    inputs:
      username: "{{ ssh_username | default('aap') }}"
    state: present
  register: machine_credential

# Step 2: Link to Vault as credential source
- name: Configure Vault as SSH Key Source
  ansible.controller.credential_input_source:
    input_field_name: "ssh_public_key_data"
    target_credential: "{{ machine_credential.id }}"
    source_credential: "hashicorp_vault_ssh_approle_{{ tenant }}"
    metadata:
      auth_path: "{{ auth_path | default('approle') }}"
      role: "{{ vault_ssh_role | default(tenant) }}"
      secret_path: "{{ ssh_secret_path | default('ssh') }}"
    state: present
```

## Organization Setup

```yaml
- name: Create Tenant Organization
  ansible.controller.organization:
    name: "{{ tenant }}"
    description: "Organization for {{ tenant }} team"
    state: present

- name: Configure Organization Credentials
  ansible.controller.credential:
    name: "vault_ssh_{{ tenant }}"
    organization: "{{ tenant }}"
    credential_type: "HashiCorp Vault Signed SSH"
    inputs:
      url: "{{ vault_url }}"
      role_id: "{{ role_id }}"
      secret_id: "{{ secret_id }}"
      default_auth_path: "approle"
      namespace: "admin/{{ tenant }}"
    state: present
```

## Job Template Configuration

```yaml
- name: Create Job Template with Vault SSH
  ansible.controller.job_template:
    name: "{{ job_template_name }}"
    organization: "{{ organization_name }}"
    project: "{{ project_name }}"
    playbook: "{{ playbook_path }}"
    inventory: "{{ inventory_name }}"
    credentials:
      - "vault_ssh_machine_{{ tenant }}"
    extra_vars:
      ansible_ssh_common_args: "-o StrictHostKeyChecking=no"
    state: present
```

## Inventory Configuration

```yaml
- name: Create Dynamic Inventory
  ansible.controller.inventory:
    name: "{{ inventory_name }}"
    organization: "{{ organization_name }}"
    state: present

- name: Add Inventory Source
  ansible.controller.inventory_source:
    name: "{{ source_name }}"
    inventory: "{{ inventory_name }}"
    source: "scm"
    source_project: "{{ project_name }}"
    source_path: "inventory/"
    update_on_launch: true
    state: present
```

## RBAC Configuration

```yaml
# Team with credential access
- name: Create Team
  ansible.controller.team:
    name: "{{ tenant }}_operators"
    organization: "{{ tenant }}"
    state: present

# Grant credential use permission
- name: Grant Credential Access
  ansible.controller.role:
    team: "{{ tenant }}_operators"
    role: "use"
    credentials:
      - "vault_ssh_machine_{{ tenant }}"
    state: present

# Grant job template execute permission
- name: Grant Job Template Access
  ansible.controller.role:
    team: "{{ tenant }}_operators"
    role: "execute"
    job_templates:
      - "{{ job_template_name }}"
    state: present
```

## Credential Rotation Job Template

```yaml
- name: Create Rotation Job Template
  ansible.controller.job_template:
    name: "Rotate Vault Credentials - {{ tenant }}"
    organization: "{{ organization_name }}"
    project: "{{ project_name }}"
    playbook: "playbooks/rotate_vault_creds.yml"
    inventory: "localhost"
    credentials:
      - "vault_approle_admin"
    survey_enabled: true
    survey_spec:
      name: "Rotation Parameters"
      spec:
        - question_name: "Tenant"
          variable: "tenant"
          type: "text"
          required: true
        - question_name: "Current Secret ID"
          variable: "current_secret_id"
          type: "password"
          required: true
    state: present

# Schedule rotation
- name: Schedule Credential Rotation
  ansible.controller.schedule:
    name: "Daily Vault Rotation - {{ tenant }}"
    unified_job_template: "Rotate Vault Credentials - {{ tenant }}"
    rrule: "DTSTART:20240101T000000Z RRULE:FREQ=DAILY;INTERVAL=1"
    state: present
```

## Complete Tenant Onboarding Playbook

```yaml
---
- name: Onboard New Tenant to AAP with Vault SSH
  hosts: localhost
  gather_facts: false
  vars:
    tenant: "{{ tenant_name }}"
    vault_url: "{{ lookup('env', 'VAULT_ADDR') }}"
    vault_namespace: "admin/{{ tenant }}"

  tasks:
    - name: Create organization
      ansible.controller.organization:
        name: "{{ tenant }}"
        state: present

    - name: Create Vault SSH credential
      ansible.controller.credential:
        name: "vault_ssh_approle_{{ tenant }}"
        organization: "{{ tenant }}"
        credential_type: "HashiCorp Vault Signed SSH"
        inputs:
          url: "{{ vault_url }}"
          role_id: "{{ vault_role_id }}"
          secret_id: "{{ vault_secret_id }}"
          default_auth_path: "approle"
          namespace: "{{ vault_namespace }}"
        state: present
      register: vault_cred

    - name: Create machine credential
      ansible.controller.credential:
        name: "machine_{{ tenant }}"
        organization: "{{ tenant }}"
        credential_type: "Machine"
        inputs:
          username: "aap"
        state: present
      register: machine_cred

    - name: Link machine credential to Vault
      ansible.controller.credential_input_source:
        input_field_name: "ssh_public_key_data"
        target_credential: "{{ machine_cred.id }}"
        source_credential: "{{ vault_cred.id }}"
        metadata:
          auth_path: "approle"
          role: "{{ tenant }}"
          secret_path: "ssh"
        state: present

    - name: Create operator team
      ansible.controller.team:
        name: "{{ tenant }}_operators"
        organization: "{{ tenant }}"
        state: present

    - name: Grant credential access
      ansible.controller.role:
        team: "{{ tenant }}_operators"
        role: "use"
        credentials:
          - "machine_{{ tenant }}"
        state: present
```
