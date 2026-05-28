---
name: dg-plus-init
description: Dagster+ Cloud Onboarding Skill This skill automates the setup of Dagster+ Cloud projects, including
- Setting up a serverless and Hybrid deployments
- scaffodling a dbt and Airlift integrations
- Configuring and checksing CI/CD workflows
- Setting up Dagster+ Agents and deploying code locations
license: MIT
---

# Dagster+ Cloud Onboarding Skills - Modular Documentation

## Overview

The Dagster+ onboarding toolkit has been refactored into a modular skill system, making it easier to use, maintain, and understand. Instead of one monolithic 7,586-line script, the functionality is now split into focused, single-purpose modules.

## Architecture

### Module Structure

```
dagster_utils.py              (Shared utilities - ~500 lines)
├── dagster_new_project.py    (New project creation - ~320 lines)
├── dagster_prepare_deployment.py (Deployment prep - ~350 lines)
├── dagster_deploy.py         (Cloud deployment - ~280 lines)
├── dagster_agent_setup.py    (Agent configuration - ~250 lines)
└── dagster_integrations.py   (Integration setup - ~220 lines)
```

### Benefits of Modular Design

✅ **Faster execution** - Load only what you need
✅ **Easier maintenance** - Changes isolated to specific modules
✅ **Better testing** - Test individual skills independently
✅ **Clearer purpose** - Each script has one clear responsibility
✅ **Token efficient** - Smaller context windows for Claude Code
✅ **Composable** - Chain scripts together for complex workflows

---

## Module Reference

### 1. dagster_utils.py

**Purpose**: Shared utility functions used across all skill scripts.

**Key Functions**:

- **Environment Detection**
  - `detect_python_executable()` - Current Python interpreter
  - `detect_virtual_environment()` - venv/conda detection
  - `detect_python_version()` - Python version string

- **Project Analysis**
  - `detect_package_name()` - Intelligent package name resolution
  - `detect_definitions_type()` - Components vs traditional detection
  - `detect_monorepo_structure()` - Multi-project repository analysis
  - `detect_components_project()` - Components architecture check

- **Token Management**
  - `validate_and_extract_token_info()` - Token parsing and validation
  - `get_organization_and_token()` - Interactive credential collection

- **Utilities**
  - `choose()` - Interactive menu selection
  - `has_cmd()` - Command availability check
  - `install_python_packages()` - Package installation
  - `ensure_project_table()` - pyproject.toml validation

**Usage**: Imported by other modules, not run directly.

---

### 2. dagster_new_project.py

**Purpose**: Create new Dagster projects from various sources.

**Capabilities**:

- ✨ Scaffold new empty projects using `create-dagster`
- 📥 Clone official quickstart templates (serverless/hybrid)
- 🎯 Import curated example projects
- 🔗 Clone custom GitHub repositories
- 📂 Use existing directory as project base

**Usage**:

```bash
python dagster_new_project.py
```

**Interactive Flow**:

1. Choose package manager (pip/uv)
2. Select project source
3. Configure project name/location
4. Install dependencies
5. Display next steps

**Outputs**:

- New Dagster project directory
- Initialized package structure
- Basic configuration files
- Installed dependencies

**Example**:

```bash
$ python dagster_new_project.py

Choose your Python package manager:
   1. pip
   2. uv
Enter your choice (1-2): 2

Choose your project source:
   1. Create new empty Dagster project (recommended)
   2. Dagster quickstart templates
   3. Eric Thomas's example projects
   4. Custom GitHub repository
   5. Use current directory
Enter your choice (1-5): 1

Enter project name: my-data-pipeline
✅ Successfully created new Dagster project!
```

**When to Use**:

- Starting a new Dagster project from scratch
- Exploring example implementations
- Need a clean Components-compatible structure

---

### 3. dagster_prepare_deployment.py

**Purpose**: Prepare existing projects for Dagster+ Cloud deployment.

**Capabilities**:

- 📄 Generate/fix `pyproject.toml` configuration
- ☁️ Create `dagster_cloud.yaml` deployment config
- 🔧 Update dependencies (add dagster-cloud)
- 🏗️ Support monorepo structures
- 🚀 Generate CI/CD workflows (GitHub/GitLab/Azure/Bitbucket)
- 🧩 Handle both Components and traditional projects

**Usage**:

```bash
python dagster_prepare_deployment.py [project_dir]
```

**Interactive Flow**:

1. Select project directory
2. Detect structure (monorepo vs single project)
3. Choose deployment type (serverless/hybrid)
4. Generate configuration files
5. Create CI/CD workflows
6. Display deployment instructions

**Outputs**:

- `pyproject.toml` - Project metadata
- `dagster_cloud.yaml` - Deployment configuration
- `README.md` - Project documentation (if missing)
- `.github/workflows/*.yml` - GitHub Actions (if applicable)
- Updated `requirements.txt` (if exists)

**Example**:

```bash
$ python dagster_prepare_deployment.py

Where is your Dagster project?
   1. Current directory
   2. Specify different directory
Enter your choice (1-2): 1

🔍 Analyzing project structure...
📁 Single Dagster project detected

What type of Dagster+ deployment will you use?
   1. Serverless
   2. Hybrid
Enter your choice (1-2): 1

✅ Dagster+ preparation completed!
```

**When to Use**:

- Existing Dagster project needs Cloud deployment
- Missing configuration files
- Setting up CI/CD for the first time
- Migrating from Dagster OSS to Dagster+

---

### 4. dagster_deploy.py

**Purpose**: Deploy Dagster projects to Dagster+ Cloud.

**Capabilities**:

- 🚀 Serverless deployment (PEX or Docker)
- 🐳 Hybrid deployment (requires agent)
- 🐍 Automatic Python version detection
- 📦 Package name auto-detection
- 🧩 Components project support
- 🔒 Token validation

**Usage**:

```bash
python dagster_deploy.py [project_dir]
```

**Interactive Flow**:

1. Select project directory
2. Enter Dagster+ credentials (org + token)
3. Choose deployment name
4. Select deployment type (serverless/hybrid)
5. For serverless: Choose build method (PEX/Docker)
6. Execute deployment
7. Display deployment URL

**Deployment Methods**:

**Serverless PEX**:

- Fast builds (~30 seconds)
- Smaller artifact size
- Pure Python projects
- Requires pip in venv

**Serverless Docker**:

- Flexible configuration
- Custom dependencies
- System packages
- Container-based

**Hybrid**:

- Requires agent (see `dagster_agent_setup.py`)
- Self-hosted execution
- VPC/network access
- Custom compute

**Example**:

```bash
$ python dagster_deploy.py

Where is your Dagster project?
   1. Current directory
Enter your choice: 1

Enter your Dagster+ API token: agent:my-org:abc123...
✅ Valid agent token detected

Enter deployment name (prod): prod

Choose deployment type:
   1. Serverless
Enter your choice: 1

Choose deployment method:
   1. PEX (Python executable)
   2. Docker
Enter your choice: 1

🚀 Deploying serverless Python executable...
✅ Deployment successful!
💡 View at: https://cloud.dagster.io/my-org/prod
```

**When to Use**:

- Manual deployment needed
- Testing deployment before CI/CD
- Deploying to non-production environments
- Initial project deployment

---

### 5. dagster_agent_setup.py

**Purpose**: Set up Dagster+ hybrid deployment agents.

**Capabilities**:

- ☁️ ECS agent (AWS CloudFormation)
- 🐳 Docker agent (local/remote)
- ⚓ Kubernetes agent (Helm guidance)
- 🔄 Stop/replace existing agents
- 🔐 Agent token validation

**Usage**:

```bash
python dagster_agent_setup.py
```

**Interactive Flow**:

1. Enter Dagster+ credentials
2. Validate agent token
3. Choose deployment name
4. Select agent type
5. Configure agent
6. Launch agent
7. Display monitoring commands

**Agent Types**:

**ECS Agent** (AWS):

- CloudFormation deployment
- Managed infrastructure
- Auto-scaling support
- Requires: AWS CLI, credentials

**Docker Agent** (Local):

- Quick setup
- Development/testing
- Local execution
- Requires: Docker Desktop

**Kubernetes Agent**:

- Production deployments
- Helm chart installation
- Scalable execution
- Manual setup with guidance

**Example**:

```bash
$ python dagster_agent_setup.py

Enter your Dagster+ API token: agent:my-org:abc123...
✅ Valid agent token detected

Enter deployment name (prod): prod

What type of agent?
   1. ECS Agent (AWS)
   2. Docker Agent (Local)
   3. Kubernetes Agent
Enter your choice: 2

🐳 Setting up Docker Agent...
✅ Dagster Cloud agent started successfully!

💡 Useful commands:
   View logs:  docker logs -f dagster-cloud-agent-prod
   Stop agent: docker stop dagster-cloud-agent-prod
```

**When to Use**:

- Setting up hybrid deployment
- Need VPC/private network access
- Custom compute requirements
- Testing agent locally

---

### 6. dagster_integrations.py

**Purpose**: Add integration capabilities to Dagster projects.

**Capabilities**:

- 🔧 dbt (Data Build Tool)
- ✈️ Airlift (Airflow migration)
- 🔌 Fivetran (ELT connector)
- 🌊 Airbyte (data integration)
- 📊 Power BI (business intelligence)

**Usage**:

```bash
python dagster_integrations.py [project_dir]
```

**Interactive Flow**:

1. Select project directory
2. Choose package manager
3. Select integration to add
4. Install dependencies
5. Display next steps
6. Repeat or exit

**Integrations**:

**dbt**:

- Packages: `dagster-dbt`, `dbt-core`, `dbt-duckdb`
- Transform data with SQL
- Dagster orchestration
- Asset lineage

**Airlift**:

- Packages: `dagster-airlift[core]`, `apache-airflow`
- Migrate Airflow DAGs
- Proxy existing workflows
- Gradual migration path

**Fivetran**:

- Packages: `dagster-fivetran`
- Orchestrate connectors
- Managed ELT
- 150+ data sources

**Airbyte**:

- Packages: `dagster-airbyte`
- Open-source integration
- Custom connectors
- Self-hosted option

**Power BI**:

- Packages: `dagster-powerbi`
- BI asset management
- Refresh orchestration
- Lineage tracking

**Example**:

```bash
$ python dagster_integrations.py

Where is your Dagster project?
   1. Current directory
Enter your choice: 1

Choose package manager:
   1. pip
Enter your choice: 1

Which integration?
   1. dbt
   2. Airlift
   3. Fivetran
   4. Airbyte
   5. Power BI
   6. Done
Enter your choice: 1

📦 Installing dbt dependencies...
✅ dbt integration dependencies installed

💡 Next steps:
   1. Initialize dbt: dbt init
   2. Create dbt asset
   3. See: https://docs.dagster.io/integrations/dbt
```

**When to Use**:

- Adding new integration to project
- Setting up data transformations (dbt)
- Migrating from Airflow
- Connecting external data sources

---

## Common Workflows

### Workflow 1: New Project → Local Development

```bash
# 1. Create new project
python dagster_new_project.py
# Choose: Create new empty project
# Result: my-data-pipeline/

# 2. Add integrations (optional)
cd my-data-pipeline
python ../dagster_integrations.py
# Choose: dbt

# 3. Develop locally
dagster dev
```

### Workflow 2: New Project → Cloud Deployment

```bash
# 1. Create new project
python dagster_new_project.py

# 2. Prepare for deployment
cd my-data-pipeline
python ../dagster_prepare_deployment.py
# Choose: Serverless deployment

# 3. Deploy to Cloud
python ../dagster_deploy.py
# Enter credentials
# Choose: PEX deployment
```

### Workflow 3: Existing Project → Cloud

```bash
# 1. Navigate to project
cd my-existing-project

# 2. Prepare for Cloud
python ../dagster_prepare_deployment.py
# Generates configuration files

# 3. Deploy
python ../dagster_deploy.py
```

### Workflow 4: Hybrid Deployment Setup

```bash
# 1. Set up agent
python dagster_agent_setup.py
# Choose: ECS Agent (AWS)
# Result: Agent running in AWS

# 2. Prepare project
cd my-project
python ../dagster_prepare_deployment.py
# Choose: Hybrid deployment

# 3. Deploy (uses agent)
python ../dagster_deploy.py
```

### Workflow 5: Add Integration to Existing

```bash
# 1. Navigate to project
cd my-project

# 2. Add integration
python ../dagster_integrations.py
# Choose: Airlift (Airflow migration)

# 3. Configure integration
# Follow printed instructions

# 4. Test locally
dagster dev
```

---

## Migration from Monolithic Script

### If You Were Using `dagster_get_started.py`:

| Old Goal | New Skill(s) |
|----------|--------------|
| New project (local) | `dagster_new_project.py` → `dagster_integrations.py` |
| New project (cloud) | `dagster_new_project.py` → `dagster_prepare_deployment.py` → `dagster_deploy.py` |
| Prepare existing | `dagster_prepare_deployment.py` |
| Install agent | `dagster_agent_setup.py` |
| Deploy existing | `dagster_deploy.py` |

### Why the Change?

❌ **Monolithic Script Problems**:
- 7,586 lines - difficult to understand
- 75 functions - hard to navigate
- 5+ workflows mixed together
- High token usage for simple tasks
- Testing complexity

✅ **Modular Skills Benefits**:
- ~300 lines per skill - easy to read
- Single purpose per script
- Composable workflows
- Fast execution
- Independent testing
- Token efficient

---

## Requirements

### All Scripts

- Python 3.8+
- Virtual environment (recommended)

### Script-Specific

**dagster_new_project.py**:

- `git` command
- Package manager (pip/uv)

**dagster_prepare_deployment.py**:

- Git repository (for CI/CD generation)

**dagster_deploy.py**:

- `dagster-cloud` CLI
- Dagster+ account and token
- Docker (for Docker deployments)

**dagster_agent_setup.py**:

- Dagster+ agent token
- ECS: AWS CLI + credentials
- Docker: Docker Desktop
- K8s: Helm + kubectl

**dagster_integrations.py**:

- Package manager (pip/uv)
- Integration-specific requirements

---

## Troubleshooting

### Common Issues

**"Module not found: dagster_utils"**

- Ensure all scripts are in the same directory
- Run from the directory containing the scripts

**"Invalid token format"**

- User tokens: `user:abc123...`
- Agent tokens: `agent:org-name:abc123...`
- Get tokens from: `https://YOUR_ORG.dagster.cloud/settings/tokens`

**"Docker daemon not running"**

- Start Docker Desktop
- Or: `sudo systemctl start docker` (Linux)

**"Package name detection failed"**

- Ensure `pyproject.toml` exists
- Check `[tool.dagster]` or `[tool.dg.project]` sections
- Manually specify in `dagster_cloud.yaml`

**"PEX build failed - pip not found"**

- Install pip in venv: `uv pip install --python .venv/bin/python pip`
- Or use Docker deployment instead

---

## Best Practices

### 1. Use Virtual Environments

Always run in a virtual environment to avoid dependency conflicts:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python dagster_new_project.py
```

### 2. Start with New Projects

For learning, use `dagster_new_project.py` to create a clean project structure.

### 3. Test Locally First

Before deploying to Cloud:

```bash
dagster dev  # Test locally
```

### 4. Use Serverless for Prototyping

Serverless is faster to set up and deploy. Use hybrid for production with special requirements.

### 5. Integrate Early

Add integrations (dbt, Airlift, etc.) during initial setup rather than retrofitting later.

### 6. Version Control Everything

Commit generated files (`pyproject.toml`, `dagster_cloud.yaml`, workflows) to Git.

---

## Support & Resources

### Documentation

- **Dagster Docs**: https://docs.dagster.io/
- **Dagster+ Docs**: https://docs.dagster.io/dagster-plus
- **Components Guide**: https://docs.dagster.io/guides/build/projects/moving-to-components

### Getting Help

- **Dagster Slack**: https://dagster.io/slack
- **GitHub Issues**: https://github.com/dagster-io/dagster/issues

### Example Projects

- **Eric Thomas Examples**: Included in `dagster_new_project.py`
- **Official Quickstarts**: https://github.com/dagster-io/

---

## Summary

The modular Dagster+ skills provide focused, efficient tools for each stage of the Dagster development lifecycle:

1. **Create** → `dagster_new_project.py`
2. **Integrate** → `dagster_integrations.py`
3. **Prepare** → `dagster_prepare_deployment.py`
4. **Deploy** → `dagster_deploy.py`
5. **Scale** → `dagster_agent_setup.py`

Each skill is:
- ✅ Single-purpose
- ✅ Independently executable
- ✅ Well-documented
- ✅ Easy to maintain
- ✅ Composable

This modular approach makes it easier to understand, use, and extend the Dagster+ onboarding experience.
