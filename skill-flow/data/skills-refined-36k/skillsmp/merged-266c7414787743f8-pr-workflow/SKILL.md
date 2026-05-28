---
name: pr-workflow
description: Use this skill when creating pull requests for esphome or esphome-docs, submitting changes, or preparing contributions.
---

# ESPHome PR Workflow

When creating a pull request for esphome or esphome-docs, follow these steps:

## 1. Create Branch from Upstream

Always base your branch on **upstream** (not origin/fork) to ensure you have the latest code:

```bash
git fetch upstream
git checkout -b <branch-name> upstream/<branch>
```

Use `upstream/dev` for esphome changes, `upstream/current` for documentation fixes, or `upstream/next` for new component docs.

## 2. Read the PR Template

Before creating a PR, read `.github/PULL_REQUEST_TEMPLATE.md` to understand required fields.

## 3. Create the PR

Use `gh pr create` with the **full template** filled in. Never skip or abbreviate sections.

### Required fields for esphome:
- **What does this implement/fix?**: Brief description of changes
- **Types of changes**: Check ONE appropriate box (Bugfix, New feature, Breaking change, etc.)
- **Related issue**: Use `fixes <link>` syntax if applicable
- **Pull request in esphome-docs**: Link if docs are needed
- **Test Environment**: Check platforms you tested on
- **Example config.yaml**: Include working example YAML
- **Checklist**: Verify code is tested and tests added

### Required fields for esphome-docs:
- **Description**: What changes are being made
- **Related issue**: Use `fixes <link>` syntax if applicable
- **Pull request in esphome**: Link if this documents a new feature
- **Checklist**: Check the appropriate boxes for branch type

## 4. Example PR Body

For esphome:

```markdown
# What does this implement/fix?

<describe your changes here>

## Types of changes

- [ ] Bugfix
- [x] New feature
- [ ] Breaking change
- [ ] Developer breaking change
- [ ] Code quality improvements
- [ ] Other

**Related issue or feature (if applicable):**

- fixes https://github.com/esphome/esphome/issues/XXX

**Pull request in [esphome-docs](https://github.com/esphome/esphome-docs) with documentation (if applicable):**

- esphome/esphome-docs#XXX

## Test Environment

- [x] ESP32
- [x] ESP32 IDF
- [ ] ESP8266
- [ ] RP2040

## Example entry for `config.yaml`:

```yaml
# Example config.yaml
component_name:
  id: my_component
  option: value
```

## Checklist:
  - [x] The code change is tested and works locally.
  - [x] Tests have been added to verify that the new code works.
```

For esphome-docs:

```markdown
## Description:

<describe your changes here>

**Related issue (if applicable):** fixes https://github.com/esphome/esphome-docs/issues/XXX

**Pull request in [esphome](https://github.com/esphome/esphome) with YAML changes (if applicable):**

- N/A (or esphome/esphome#XXX)

## Checklist:

  - [ ] I am merging into `next` because this is new documentation that has a matching pull-request in [esphome](https://github.com/esphome/esphome).
  - [x] I am merging into `current` because this is a fix, change and/or adjustment in the current documentation.
```

## 5. Push and Create PR

```bash
git push -u origin <branch-name>
gh pr create --repo esphome/<repo> --base <branch> --title "[component] Brief description"
```

Use `--repo esphome/esphome` for esphome changes and `--repo esphome/esphome-docs` for documentation changes. Use `--base next` if documenting a new feature with a matching esphome PR.