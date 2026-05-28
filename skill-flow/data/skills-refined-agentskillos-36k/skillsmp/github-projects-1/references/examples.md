# Examples: GitHub Projects (V2)

The following examples demonstrate how to use the `gh project` CLI for common tasks.

## 1. Discovery

### List Projects for an Organization
```bash
gh project list --owner StaytunedLLP --format json
```

### List Fields in a Project
```bash
# Find the project ID first, then list fields
gh project field-list 1 --owner StaytunedLLP --format json
```

---

## 2. Item Management

### Add an Issue to a Project
```bash
# REPO_URL is the full URL of the issue to add
gh project item-add 1 --owner StaytunedLLP --url "https://github.com/StaytunedLLP/dhoom/issues/101"
```

### Update the 'Status' of a Project Item
1. Find the `item-id` using `gh project item-list`.
2. Find the `field-id` for "Status" and the `option-id` for "In Progress" using `gh project field-list`.
3. Update the item:
```bash
gh project item-edit --id "PVTI_..." --field-id "PVTSSF_..." --project-id "PVT_..." --single-select-option-id "98234..."
```

---

## 3. Project Creation & Linking

### Create a New Project
```bash
gh project create --owner StaytunedLLP --title "Deployment Roadmap"
```

### Link Project to a Repository
```bash
gh project link 1 --owner StaytunedLLP --repo "dhoom"
```
