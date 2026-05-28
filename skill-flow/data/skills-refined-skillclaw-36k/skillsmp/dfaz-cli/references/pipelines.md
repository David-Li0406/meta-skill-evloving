# Azure Pipelines CLI Reference

## Pipeline Management

### az pipelines list

List pipelines in a project.

```bash
az pipelines list [--name <filter>] [--top <n>] [--org] [--project]
```

### az pipelines show

Get pipeline details.

```bash
az pipelines show --name <pipeline-name> [--open] [--org] [--project]
az pipelines show --id <pipeline-id>
```

### az pipelines create

Create a new YAML pipeline.

```bash
az pipelines create \
  --name "My Pipeline" \
  --repository <repo-name> \
  --branch main \
  --yml-path azure-pipelines.yml \
  [--folder-path "\\folder"] \
  [--skip-first-run]
```

### az pipelines update

Update pipeline settings.

```bash
az pipelines update --id <id> --name "New Name" [--new-folder-path "\\new-folder"]
```

### az pipelines delete

Delete a pipeline.

```bash
az pipelines delete --id <pipeline-id> [--yes]
```

## Running Pipelines

### az pipelines run

Queue/run a pipeline.

```bash
# Simple run
az pipelines run --name "pipeline-name"

# Run specific branch
az pipelines run --name "pipeline-name" --branch feature/branch

# Run with parameters
az pipelines run --name "pipeline-name" --parameters "param1=value1 param2=value2"

# Run with variables
az pipelines run --name "pipeline-name" --variables "var1=value1 var2=value2"

# Run by ID
az pipelines run --id <pipeline-id>
```

## Pipeline Runs

### az pipelines runs list

List pipeline runs.

```bash
# Recent runs
az pipelines runs list --top 10

# Filter by pipeline
az pipelines runs list --pipeline-ids <id>

# Filter by status
az pipelines runs list --status completed|inProgress|notStarted|cancelling

# Filter by result
az pipelines runs list --result succeeded|failed|canceled

# Filter by branch
az pipelines runs list --branch refs/heads/main
```

### az pipelines runs show

Show run details.

```bash
az pipelines runs show --id <run-id> [--open]
```

## Run Artifacts

### az pipelines runs artifact list

List artifacts from a run.

```bash
az pipelines runs artifact list --run-id <id>
```

### az pipelines runs artifact download

Download an artifact.

```bash
az pipelines runs artifact download --run-id <id> --artifact-name <name> --path <download-path>
```

## Run Tags

### az pipelines runs tag list

List tags on a run.

```bash
az pipelines runs tag list --run-id <id>
```

### az pipelines runs tag add

Add tag to a run.

```bash
az pipelines runs tag add --run-id <id> --tags "tag1" "tag2"
```

## Builds (Classic)

### az pipelines build list

List builds.

```bash
az pipelines build list [--definition-ids <id>] [--top <n>]
```

### az pipelines build show

Show build details.

```bash
az pipelines build show --id <build-id>
```

### az pipelines build cancel

Cancel a running build.

```bash
az pipelines build cancel --id <build-id>
```

## Pipeline Variables

### az pipelines variable list

List pipeline variables.

```bash
az pipelines variable list --pipeline-name <name>
az pipelines variable list --pipeline-id <id>
```

### az pipelines variable create

Create a variable.

```bash
az pipelines variable create \
  --pipeline-name <name> \
  --name <var-name> \
  --value <value> \
  [--secret true] \
  [--allow-override true]
```

### az pipelines variable update

Update a variable.

```bash
az pipelines variable update \
  --pipeline-name <name> \
  --name <var-name> \
  --value <new-value>
```

### az pipelines variable delete

Delete a variable.

```bash
az pipelines variable delete --pipeline-name <name> --name <var-name> [--yes]
```

## Variable Groups

### az pipelines variable-group list

List variable groups.

```bash
az pipelines variable-group list [--group-name <filter>]
```

### az pipelines variable-group show

Show variable group details.

```bash
az pipelines variable-group show --id <group-id>
az pipelines variable-group show --group-name <name>
```

### az pipelines variable-group create

Create a variable group.

```bash
az pipelines variable-group create \
  --name "My Variables" \
  --variables "var1=value1" "var2=value2" \
  [--authorize true]
```

### az pipelines variable-group variable list

List variables in a group.

```bash
az pipelines variable-group variable list --group-id <id>
```

### az pipelines variable-group variable create

Add variable to group.

```bash
az pipelines variable-group variable create \
  --group-id <id> \
  --name <var-name> \
  --value <value> \
  [--secret true]
```

## Pipeline Folders

### az pipelines folder list

List folders.

```bash
az pipelines folder list [--path "\\"]
```

### az pipelines folder create

Create a folder.

```bash
az pipelines folder create --path "\\folder\\subfolder"
```

### az pipelines folder delete

Delete a folder.

```bash
az pipelines folder delete --path "\\folder" [--yes]
```

## Agents and Pools

### az pipelines agent list

List agents in a pool.

```bash
az pipelines agent list --pool-id <id>
```

### az pipelines agent show

Show agent details.

```bash
az pipelines agent show --pool-id <id> --agent-id <id>
```

### az pipelines pool list

List agent pools.

```bash
az pipelines pool list [--pool-name <filter>]
```

### az pipelines pool show

Show pool details.

```bash
az pipelines pool show --id <pool-id>
```

### az pipelines queue list

List agent queues.

```bash
az pipelines queue list [--queue-name <filter>]
```

## Releases (Classic)

### az pipelines release list

List releases.

```bash
az pipelines release list [--definition-id <id>] [--top <n>]
```

### az pipelines release show

Show release details.

```bash
az pipelines release show --id <release-id>
```

### az pipelines release create

Create a release.

```bash
az pipelines release create --definition-id <id> [--description "Release notes"]
```

### az pipelines release-definition list

List release definitions.

```bash
az pipelines release-definition list [--name <filter>]
```

### az pipelines release-definition show

Show release definition.

```bash
az pipelines release-definition show --id <id>
```
