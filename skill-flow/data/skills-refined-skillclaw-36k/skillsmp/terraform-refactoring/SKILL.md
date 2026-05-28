---
name: terraform-refactoring
description: 'Safely refactor Terraform modules using moved blocks to rename resources, reorganize module structure, and migrate state without destroying infrastructure. Use when asked to "rename resource", "refactor module", "reorganize Terraform", "move resources", "split module", "change resource name", or when restructuring code while preserving existing infrastructure.'
---

# Terraform Refactoring

Safely refactor Terraform modules using `moved` blocks to update resource addresses without destroying existing infrastructure. This skill focuses on preserving state while improving code organization.

## When to Use This Skill

- User asks to "rename a resource", "change resource name", "refactor module structure"
- Need to reorganize module code without destroying infrastructure
- Splitting a large module into smaller, focused modules
- Migrating from single-instance to multi-instance resources (count/for_each)
- Restructuring module hierarchy or nesting
- Consolidating or separating module calls
- Following up on breaking changes that would destroy/recreate resources
- **Critical:** Preventing infrastructure destruction during code refactoring

## Requirements

**Terraform Version:** >= 1.1

For older versions, use the `terraform state mv` CLI command instead of `moved` blocks.

## Core Concept: The `moved` Block

### Basic Syntax

```hcl
moved {
  from = <old_address>
  to   = <new_address>
}
```

**How it works:**
1. Before creating a plan for the `to` address, Terraform checks state for an existing object at the `from` address
2. If found, Terraform renames the object in state to the `to` address
3. Plan proceeds as if the object was originally created at the `to` address
4. **No infrastructure is destroyed**

### Placement

**In module files:** Add `moved` blocks anywhere in your `.tf` files alongside resource definitions.

**Best practice:** Create a dedicated `moved.tf` file for large refactorings to keep history clear.

## Common Refactoring Patterns

### Pattern 1: Rename a Resource

**Scenario:** You want to give a resource a more descriptive name.

**Before:**
```hcl
resource "aws_instance" "server" {
  # ... configuration ...
}
```

**After:**
```hcl
resource "aws_instance" "web_server" {
  # ... configuration ...
}

moved {
  from = aws_instance.server
  to   = aws_instance.web_server
}
```

**What happens:**
- Existing object at `aws_instance.server` is renamed to `aws_instance.web_server` in state
- No infrastructure changes
- Future plans reference `aws_instance.web_server`

### Pattern 2: Rename a Resource with Count/For_Each

**Scenario:** Renaming a resource that has multiple instances.

**Before:**
```hcl
resource "aws_security_group" "sg" {
  count = 2
  # ... configuration ...
}
```

**After:**
```hcl
resource "aws_security_group" "security_group" {
  count = 2
  # ... configuration ...
}

moved {
  from = aws_security_group.sg
  to   = aws_security_group.security_group
}
```

**Important:** The `moved` block without instance keys applies to ALL instances automatically:
- `aws_security_group.sg[0]` → `aws_security_group.security_group[0]`
- `aws_security_group.sg[1]` → `aws_security_group.security_group[1]`

### Pattern 3: Add Count to Single-Instance Resource

**Scenario:** Converting a single resource to multiple instances while preserving the original.

**Before:**
```hcl
resource "aws_instance" "web" {
  # ... configuration ...
}
```

**After:**
```hcl
locals {
  instances = {
    small = { instance_type = "t2.micro" }
    large = { instance_type = "t2.large" }
  }
}

resource "aws_instance" "web" {
  for_each = local.instances

  instance_type = each.value.instance_type
  # ... configuration ...
}

moved {
  from = aws_instance.web
  to   = aws_instance.web["small"]
}
```

**What happens:**
- Original object at `aws_instance.web` becomes `aws_instance.web["small"]`
- Terraform creates `aws_instance.web["large"]` as new infrastructure
- Original instance preserved

**Alternative with count:**
```hcl
resource "aws_instance" "web" {
  count = 3
  # ... configuration ...
}

moved {
  from = aws_instance.web
  to   = aws_instance.web[0]
}
```

**Best practice:** Always write explicit `moved` blocks when adding `count` (even though Terraform auto-maps to index 0).

### Pattern 4: Change Instance Keys (For_Each)

**Scenario:** Renaming keys in a for_each resource.

**Before:**
```hcl
resource "aws_instance" "app" {
  for_each = {
    small = { type = "t2.micro" }
  }
  # ... configuration ...
}
```

**After:**
```hcl
resource "aws_instance" "app" {
  for_each = {
    tiny = { type = "t2.micro" }
  }
  # ... configuration ...
}

moved {
  from = aws_instance.app["small"]
  to   = aws_instance.app["tiny"]
}
```

### Pattern 5: Convert Count to For_Each

**Scenario:** Migrating from count-based to for_each-based instances.

**Before:**
```hcl
resource "aws_instance" "app" {
  count = 2
  # ... configuration ...
}
```

**After:**
```hcl
resource "aws_instance" "app" {
  for_each = {
    primary   = { type = "t2.small" }
    secondary = { type = "t2.micro" }
  }
  # ... configuration ...
}

moved {
  from = aws_instance.app[0]
  to   = aws_instance.app["primary"]
}

moved {
  from = aws_instance.app[1]
  to   = aws_instance.app["secondary"]
}
```

### Pattern 6: Rename a Module Call

**Scenario:** Giving a module call a better name.

**Before:**
```hcl
module "network" {
  source = "./modules/vpc"
  # ... configuration ...
}
```

**After:**
```hcl
module "vpc" {
  source = "./modules/vpc"
  # ... configuration ...
}

moved {
  from = module.network
  to   = module.vpc
}
```

**What happens:**
- All resources in the module are moved:
  - `module.network.aws_vpc.this` → `module.vpc.aws_vpc.this`
  - `module.network.aws_subnet.public[0]` → `module.vpc.aws_subnet.public[0]`
  - etc.

### Pattern 7: Add Count/For_Each to Module Call

**Scenario:** Converting a single module call to multiple instances.

**Before:**
```hcl
module "app" {
  source = "./modules/service"
  # ... configuration ...
}
```

**After:**
```hcl
module "app" {
  source = "./modules/service"
  count  = 3
  # ... configuration ...
}

moved {
  from = module.app
  to   = module.app[2]
}
```

**What happens:**
- Original module instance becomes `module.app[2]`
- Terraform creates `module.app[0]` and `module.app[1]` as new infrastructure

### Pattern 8: Move Resource Into a Module

**Scenario:** Extracting resources into a child module.

**Before:**
```hcl
# In root module
resource "aws_instance" "web" {
  # ... configuration ...
}

resource "aws_security_group" "web" {
  # ... configuration ...
}
```

**After:**
```hcl
# In root module
module "web_server" {
  source = "./modules/web-server"
  # ... configuration ...
}

moved {
  from = aws_instance.web
  to   = module.web_server.aws_instance.web
}

moved {
  from = aws_security_group.web
  to   = module.web_server.aws_security_group.web
}
```

```hcl
# In ./modules/web-server/main.tf
resource "aws_instance" "web" {
  # ... configuration ...
}

resource "aws_security_group" "web" {
  # ... configuration ...
}
```

### Pattern 9: Split a Module

**Scenario:** Breaking a large module into multiple smaller, focused modules.

**Before (monolithic module):**
```hcl
# In ./modules/app/main.tf
resource "aws_instance" "web" {
  # ... configuration ...
}

resource "aws_instance" "worker" {
  # ... configuration ...
}

resource "aws_db_instance" "db" {
  # ... configuration ...
}
```

**After (split into 3 modules):**

**Create new focused modules:**
```hcl
# ./modules/web/main.tf
resource "aws_instance" "web" {
  # ... configuration ...
}
```

```hcl
# ./modules/worker/main.tf
resource "aws_instance" "worker" {
  # ... configuration ...
}
```

```hcl
# ./modules/database/main.tf
resource "aws_db_instance" "db" {
  # ... configuration ...
}
```

**Convert original module to shim for backward compatibility:**
```hcl
# ./modules/app/main.tf (now a compatibility shim)
module "web" {
  source = "../web"
  # ... pass through variables ...
}

module "worker" {
  source = "../worker"
  # ... pass through variables ...
}

module "database" {
  source = "../database"
  # ... pass through variables ...
}

moved {
  from = aws_instance.web
  to   = module.web.aws_instance.web
}

moved {
  from = aws_instance.worker
  to   = module.worker.aws_instance.worker
}

moved {
  from = aws_db_instance.db
  to   = module.database.aws_db_instance.db
}
```

**What happens:**
- Existing users can upgrade to the shim version without infrastructure changes
- New users can use the focused modules directly
- Original module can be deprecated over time

**Important:** This violates the "child module as closed box" principle - only do this when all modules are maintained together in the same package.

### Pattern 10: Module Call with Instance Keys

**Scenario:** Moving resources into a module that uses count/for_each.

**Before:**
```hcl
resource "aws_instance" "app" {
  # ... configuration ...
}
```

**After:**
```hcl
module "apps" {
  source = "./modules/app"
  count  = 3
  # ... configuration ...
}

moved {
  from = aws_instance.app
  to   = module.apps[1].aws_instance.app
}
```

**What happens:**
- Original resource moves to `module.apps[1]`
- Terraform creates resources in `module.apps[0]` and `module.apps[2]`

## Chaining Moves

**Scenario:** Resource has been renamed multiple times over module evolution.

```hcl
moved {
  from = aws_instance.server
  to   = aws_instance.web_server
}

moved {
  from = aws_instance.web_server
  to   = aws_instance.application_server
}
```

**What happens:**
- Configurations with objects at `aws_instance.server` upgrade successfully
- Configurations with objects at `aws_instance.web_server` upgrade successfully
- Both end up at `aws_instance.application_server`

**Why chain:** Supports users upgrading from any previous version.

## Best Practices

### 1. Test Refactoring Before Applying

```bash
# Make your changes with moved blocks
terraform plan

# Verify output shows:
# - "moved" operations (not "destroy" + "create")
# - No unexpected changes
# - Correct addressing
```

**Expected plan output:**
```
Terraform will perform the following actions:

  # aws_instance.server has moved to aws_instance.web_server
    resource "aws_instance" "web_server" {
        # ... (no changes) ...
    }

Plan: 0 to add, 0 to change, 0 to destroy.
```

### 2. Create Dedicated moved.tf File

**For large refactorings:**
```
terraform-aws-module/
├── main.tf
├── variables.tf
├── outputs.tf
└── moved.tf              # All moved blocks here
```

**Benefits:**
- Clear refactoring history
- Easy to review changes
- Simple to remove old moves later

### 3. Document Why in Comments

```hcl
# Renamed to follow module naming convention (resource type in identifier is redundant)
moved {
  from = aws_security_group.security_group
  to   = aws_security_group.web
}

# Split networking resources into dedicated module
moved {
  from = aws_vpc.main
  to   = module.networking.aws_vpc.main
}
```

### 4. Group Related Moves

```hcl
# === Networking refactoring (v2.0.0) ===
moved {
  from = aws_vpc.vpc
  to   = aws_vpc.main
}

moved {
  from = aws_subnet.subnet
  to   = aws_subnet.private
}

# === Security refactoring (v2.1.0) ===
moved {
  from = aws_security_group.sg
  to   = module.security.aws_security_group.app
}
```

### 5. Keep Historical Moves (Usually)

**❌ Don't remove `moved` blocks unless:**
- You're certain ALL users have upgraded
- Module is private/internal only
- You can coordinate with all users

**✅ Do keep `moved` blocks:**
- For public modules (indefinitely)
- For any module with external users
- When uncertain about user upgrade status

**Reason:** Removing `moved` blocks is a **breaking change** - users on old versions will plan to destroy infrastructure.

### 6. Use Version Tags for Refactorings

```bash
# Before refactoring
git tag v1.5.0

# After refactoring
git tag v2.0.0

# Document in CHANGELOG
# v2.0.0
# - BREAKING: Removed moved blocks for v1.0.0 → v1.5.0 transitions
# - Users must upgrade to v1.5.0 first, then to v2.0.0
```

### 7. Validate State After Apply

```bash
terraform apply

# Verify state has new addresses
terraform state list

# Check specific resource
terraform state show aws_instance.web_server
```

### 8. Handle Provider-Specific Resource Type Changes

**Some providers allow moving between resource types:**

```hcl
# Check provider documentation first!
moved {
  from = aws_security_group_rule.ingress
  to   = aws_vpc_security_group_ingress_rule.ingress
}
```

**Important:** Not all resource type changes are supported. Consult provider docs.

**Cannot do:** Move from `resource` to `data` block (managed → data source).

## Advanced Patterns

### Conditional Moves Based on Module Input

**Not possible directly, but can structure code:**

```hcl
# ❌ This doesn't work - moved blocks don't support conditional logic
moved {
  from = var.use_new_name ? aws_instance.old : aws_instance.new
  to   = aws_instance.final
}
```

**✅ Instead, use separate configurations or branches**

### Moving Resources Across Module Boundaries

**Scenario:** Move resource from parent to child module.

```hcl
# In parent module
module "child" {
  source = "./modules/child"
  # ... configuration ...
}

moved {
  from = aws_instance.example
  to   = module.child.aws_instance.example
}
```

**Reverse (child to parent):** Not directly supported by `moved` block. Use `terraform state mv` CLI command.

### Preserving Outputs During Refactoring

**Before:**
```hcl
output "instance_id" {
  value = aws_instance.server.id
}
```

**After (with refactoring):**
```hcl
resource "aws_instance" "web_server" {
  # ... configuration ...
}

moved {
  from = aws_instance.server
  to   = aws_instance.web_server
}

output "instance_id" {
  value = aws_instance.web_server.id
}
```

**Maintain backward compatibility:**
```hcl
output "instance_id" {
  value       = aws_instance.web_server.id
  description = "ID of the web server instance"
}

# Deprecated output for backward compatibility
output "server_id" {
  value       = aws_instance.web_server.id
  description = "DEPRECATED: Use instance_id instead. ID of the web server instance."
}
```

## Troubleshooting

### Issue: "Resource not found in state"

**Problem:**
```
Error: Resource not found in state

The resource aws_instance.old was not found in the state.
```

**Causes:**
- Typo in `from` address
- Resource never existed in state
- Resource was already moved

**Solution:**
```bash
# Check what's actually in state
terraform state list

# Verify exact address
terraform state show aws_instance.old
```

### Issue: "Cannot move to existing resource"

**Problem:**
```
Error: Resource already exists

Cannot move aws_instance.old to aws_instance.new because
aws_instance.new already exists in state.
```

**Cause:** Target address already has an object in state.

**Solution:**
```bash
# Remove the conflicting resource first (if safe)
terraform state rm aws_instance.new

# Or move the existing resource somewhere else
terraform state mv aws_instance.new aws_instance.backup
```

### Issue: Plan Shows Destroy + Create Instead of Move

**Problem:** `terraform plan` shows `-/+` instead of moved.

**Causes:**
- `moved` block has incorrect addresses
- `moved` block is in wrong module
- Significant configuration changes that require replacement

**Solution:**
```bash
# Verify moved block syntax
terraform validate

# Check addresses exactly match
terraform state list | grep <resource>

# Review configuration changes
git diff
```

### Issue: Circular Move Dependencies

**Problem:**
```
Error: Circular moved block dependency

The moved blocks create a circular dependency.
```

**Cause:**
```hcl
moved {
  from = aws_instance.a
  to   = aws_instance.b
}

moved {
  from = aws_instance.b
  to   = aws_instance.a
}
```

**Solution:** Remove circular reference or chain correctly.

## Migration Checklist

**Before Refactoring:**
- [ ] Review current state: `terraform state list`
- [ ] Plan is clean: `terraform plan` shows no changes
- [ ] Backup state: `terraform state pull > backup.tfstate`
- [ ] Document refactoring goals
- [ ] Check Terraform version >= 1.1

**During Refactoring:**
- [ ] Make code changes (rename resources, reorganize files)
- [ ] Add `moved` blocks for each address change
- [ ] Run `terraform validate`
- [ ] Run `terraform plan` and verify:
  - [ ] Shows "moved" operations (not destroy/create)
  - [ ] No unexpected infrastructure changes
  - [ ] Addresses are correct

**After Refactoring:**
- [ ] Apply changes: `terraform apply`
- [ ] Verify state: `terraform state list`
- [ ] Test outputs: Check that outputs still work
- [ ] Update documentation (README, CHANGELOG)
- [ ] Tag release (if applicable)
- [ ] Communicate changes to users

## Real-World Example

**Scenario:** Refactor ECS service module to follow naming conventions.

**Before:**
```hcl
# main.tf
resource "aws_ecs_service" "service" {
  name = "my-service"
  # ... configuration ...
}

resource "aws_security_group" "security_group" {
  name = "service-sg"
  # ... configuration ...
}

resource "aws_iam_role" "task_role" {
  name = "task-role"
  # ... configuration ...
}

resource "aws_iam_role" "execution_role" {
  name = "execution-role"
  # ... configuration ...
}
```

**After:**
```hcl
# main.tf
resource "aws_ecs_service" "this" {
  name = "my-service"
  # ... configuration ...
}

# security-group.tf
resource "aws_security_group" "this" {
  name = "service-sg"
  # ... configuration ...
}

# iam-role-policies.tf
resource "aws_iam_role" "task" {
  name = "task-role"
  # ... configuration ...
}

resource "aws_iam_role" "execution" {
  name = "execution-role"
  # ... configuration ...
}

# moved.tf
# Refactoring to follow naming conventions (v2.0.0)

moved {
  from = aws_ecs_service.service
  to   = aws_ecs_service.this
}

moved {
  from = aws_security_group.security_group
  to   = aws_security_group.this
}

moved {
  from = aws_iam_role.task_role
  to   = aws_iam_role.task
}

moved {
  from = aws_iam_role.execution_role
  to   = aws_iam_role.execution
}
```

**Results:**
```bash
$ terraform plan
aws_ecs_service.service has moved to aws_ecs_service.this
aws_security_group.security_group has moved to aws_security_group.this
aws_iam_role.task_role has moved to aws_iam_role.task
aws_iam_role.execution_role has moved to aws_iam_role.execution

Plan: 0 to add, 0 to change, 0 to destroy.
```

**No infrastructure destroyed!**

## References

- **Terraform Refactoring Guide**: <https://developer.hashicorp.com/terraform/language/modules/develop/refactoring>
- **moved Block Reference**: <https://developer.hashicorp.com/terraform/language/block/moved>
- **State Move Tutorial**: <https://developer.hashicorp.com/terraform/tutorials/configuration-language/move-config>
- **terraform state mv**: <https://developer.hashicorp.com/terraform/cli/commands/state/mv>
- **Terraform Code Style**: `.github/instructions/terraform.instructions.md`
- **File Structure**: `.github/instructions/file-structure.instructions.md`

## Quick Decision Tree

**Need to refactor? Ask:**

1. **Is it just a rename?** → Use simple `moved` block (Pattern 1)
2. **Multiple instances involved?** → Use `moved` with instance keys (Pattern 2-5)
3. **Module reorganization?** → Use `moved` with module paths (Pattern 6-8)
4. **Splitting a module?** → Create shim module (Pattern 9)
5. **Cross-module move?** → Use `moved` to/from module (Pattern 8, 10)
6. **Provider version <1.1?** → Use `terraform state mv` CLI

**Always:**
- Test with `terraform plan` first
- Keep `moved` blocks for backward compatibility
- Document WHY in comments
