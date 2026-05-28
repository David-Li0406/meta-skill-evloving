# Azure DevOps CLI Reference

## Authentication & Configuration

### az devops configure

Configure CLI defaults.

```bash
# Set organization and project defaults
az devops configure --defaults organization=https://dev.azure.com/YOUR_ORG project=YOUR_PROJECT

# View current configuration
az devops configure --list

# Clear a default
az devops configure --defaults project=
```

### az devops login

Set credentials for an organization.

```bash
# Interactive login (prompts for PAT)
az devops login --organization https://dev.azure.com/YOUR_ORG

# Login with PAT from environment variable
echo $AZURE_DEVOPS_EXT_PAT | az devops login --organization https://dev.azure.com/YOUR_ORG
```

### az devops logout

Clear stored credentials.

```bash
# Logout from specific org
az devops logout --organization https://dev.azure.com/YOUR_ORG

# Logout from all orgs
az devops logout
```

## Projects

### az devops project list

List projects in organization.

```bash
az devops project list [--top <n>] [--skip <n>] [--state all|deleting|new|wellFormed]
```

### az devops project show

Show project details.

```bash
az devops project show --project <project-name> [--open]
```

### az devops project create

Create a new project.

```bash
az devops project create \
  --name "New Project" \
  --description "Project description" \
  [--process Agile|Scrum|Basic|CMMI] \
  [--source-control git|tfvc] \
  [--visibility private|public]
```

### az devops project delete

Delete a project.

```bash
az devops project delete --id <project-id> [--yes]
```

## Teams

### az devops team list

List teams in project.

```bash
az devops team list [--top <n>] [--skip <n>]
```

### az devops team show

Show team details.

```bash
az devops team show --team "Team Name"
```

### az devops team create

Create a team.

```bash
az devops team create --name "New Team" [--description "Team description"]
```

### az devops team delete

Delete a team.

```bash
az devops team delete --id <team-id> [--yes]
```

### az devops team update

Update team settings.

```bash
az devops team update --team "Team Name" --name "New Team Name" --description "Updated description"
```

### az devops team list-member

List team members.

```bash
az devops team list-member --team "Team Name" [--top <n>] [--skip <n>]
```

## Users

### az devops user list

List users in organization.

```bash
az devops user list [--top <n>] [--skip <n>]
```

### az devops user show

Show user details.

```bash
az devops user show --user user@email.com
```

### az devops user add

Add user to organization.

```bash
az devops user add \
  --email-id user@email.com \
  --license-type express|stakeholder|basic|professional \
  [--send-email-invite true]
```

### az devops user update

Update user license.

```bash
az devops user update --user user@email.com --license-type basic
```

### az devops user remove

Remove user from organization.

```bash
az devops user remove --user user@email.com [--yes]
```

## Service Endpoints (Connections)

### az devops service-endpoint list

List service connections.

```bash
az devops service-endpoint list
```

### az devops service-endpoint show

Show connection details.

```bash
az devops service-endpoint show --id <endpoint-id>
```

### az devops service-endpoint create

Create service connection (general).

```bash
az devops service-endpoint create --service-endpoint-configuration <config-file>
```

### az devops service-endpoint azurerm create

Create Azure Resource Manager connection.

```bash
az devops service-endpoint azurerm create \
  --name "Azure Connection" \
  --azure-rm-service-principal-id <sp-id> \
  --azure-rm-subscription-id <sub-id> \
  --azure-rm-subscription-name "Subscription Name" \
  --azure-rm-tenant-id <tenant-id>
```

### az devops service-endpoint github create

Create GitHub connection.

```bash
az devops service-endpoint github create \
  --name "GitHub Connection" \
  --github-url https://github.com
```

### az devops service-endpoint delete

Delete a service connection.

```bash
az devops service-endpoint delete --id <endpoint-id> [--yes]
```

### az devops service-endpoint update

Update service connection.

```bash
az devops service-endpoint update --id <endpoint-id> --enable-for-all true
```

## Extensions

### az devops extension list

List installed extensions.

```bash
az devops extension list [--include-built-in] [--include-disabled]
```

### az devops extension show

Show extension details.

```bash
az devops extension show --extension-id <id> --publisher-id <publisher>
```

### az devops extension search

Search marketplace extensions.

```bash
az devops extension search --search-query "search term"
```

### az devops extension install

Install an extension.

```bash
az devops extension install --extension-id <id> --publisher-id <publisher>
```

### az devops extension uninstall

Uninstall an extension.

```bash
az devops extension uninstall --extension-id <id> --publisher-id <publisher> [--yes]
```

### az devops extension enable/disable

Enable or disable an extension.

```bash
az devops extension enable --extension-id <id> --publisher-id <publisher>
az devops extension disable --extension-id <id> --publisher-id <publisher>
```

## Wiki

### az devops wiki list

List wikis in project.

```bash
az devops wiki list
```

### az devops wiki show

Show wiki details.

```bash
az devops wiki show --wiki <wiki-name>
```

### az devops wiki create

Create a wiki.

```bash
# Project wiki
az devops wiki create --name "Project Wiki" --type projectWiki

# Code wiki (from repo)
az devops wiki create \
  --name "Code Wiki" \
  --type codeWiki \
  --repository <repo-id> \
  --mapped-path /docs \
  --version <branch>
```

### az devops wiki delete

Delete a wiki.

```bash
az devops wiki delete --wiki <wiki-name> [--yes]
```

### az devops wiki page show

Show wiki page.

```bash
az devops wiki page show --wiki <wiki-name> --path "/Page Name"
```

### az devops wiki page create

Create a wiki page.

```bash
az devops wiki page create \
  --wiki <wiki-name> \
  --path "/New Page" \
  --content "# Page Content"
```

### az devops wiki page update

Update a wiki page.

```bash
az devops wiki page update \
  --wiki <wiki-name> \
  --path "/Page Name" \
  --content "# Updated Content" \
  --version <etag>
```

### az devops wiki page delete

Delete a wiki page.

```bash
az devops wiki page delete --wiki <wiki-name> --path "/Page Name" [--yes]
```

## Security

### az devops security group list

List security groups.

```bash
az devops security group list [--scope organization|project]
```

### az devops security group show

Show group details.

```bash
az devops security group show --id <group-descriptor>
```

### az devops security group create

Create a security group.

```bash
az devops security group create --name "Group Name" [--description "Description"]
```

### az devops security group membership list

List group members.

```bash
az devops security group membership list --id <group-descriptor>
```

### az devops security group membership add

Add member to group.

```bash
az devops security group membership add --group-id <group-id> --member-id <member-id>
```

### az devops security permission list

List permissions.

```bash
az devops security permission list --namespace-id <namespace-id> --token <security-token>
```

## Invoke (Raw API Calls)

### az devops invoke

Make arbitrary API calls.

```bash
# GET request
az devops invoke \
  --area core \
  --resource projects \
  --api-version 6.0

# POST request with body
az devops invoke \
  --area wit \
  --resource workitems \
  --route-parameters project=MyProject type=Bug \
  --http-method POST \
  --in-file body.json \
  --api-version 6.0

# With query parameters
az devops invoke \
  --area core \
  --resource projects \
  --query-parameters "\$top=10" "stateFilter=wellFormed"
```

## Admin (Organization Level)

### az devops admin banner list

List organization banners.

```bash
az devops admin banner list
```

### az devops admin banner add

Add an organization banner.

```bash
az devops admin banner add \
  --id <banner-id> \
  --message "Important announcement" \
  --type info|warning|error \
  [--expiration 2024-12-31]
```

### az devops admin banner remove

Remove a banner.

```bash
az devops admin banner remove --id <banner-id>
```

### az devops admin banner update

Update a banner.

```bash
az devops admin banner update --id <banner-id> --message "Updated message"
```
