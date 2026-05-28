---
name: feature-file-organization
description: 'Organize and structure Gherkin feature files for Terraform modules following best practices for maintainability and scalability. Use when asked to "organize features", "structure feature files", "split scenarios", "refactor features", or when feature files become large, complex, or hard to maintain. Provides patterns for grouping scenarios, avoiding duplication, and creating reusable step definitions.'
---

# Feature File Organization

Organize Gherkin feature files into a maintainable, scalable structure for Terraform module development. This skill focuses on file organization, scenario grouping, and step definition patterns - complementing the gherkin-scenarios skill which covers syntax.

## When to Use This Skill

- User asks to "organize features", "structure feature files", "split large features"
- Feature files become too large (>200 lines or >10 scenarios)
- Scenarios are duplicated across multiple feature files
- Feature files are hard to navigate or understand
- Starting a new Terraform module with multiple capabilities
- Refactoring existing feature files for better maintainability
- Creating a consistent pattern across team projects

## Directory Structure

### Standard Layout

**For Terraform modules:**
```
docs/features/
├── README.md                           # Feature index and overview
├── core-functionality.feature          # Primary module capability
├── security-configuration.feature      # Security-related scenarios
├── networking-integration.feature      # Network-related scenarios
└── advanced-features/                  # Complex or optional features
    ├── auto-scaling.feature
    ├── service-connect.feature
    └── observability.feature
```

### Location

**Always use:** `docs/features/` directory (platform-independent)

**Not:** `.github/features/` (platform-specific, legacy)

**File Extension:** `.feature` (required for Gherkin parsers)

### File Naming

**Pattern:** `domain-concept.feature`

**Examples:**
```
✅ Good:
- ecs-service-creation.feature
- load-balancer-integration.feature
- auto-scaling-policies.feature
- security-group-rules.feature
- cloudwatch-logging.feature

❌ Bad:
- test.feature (not descriptive)
- ECS_Service.feature (use kebab-case)
- service-creation-with-auto-scaling-and-load-balancer.feature (too long)
- features.feature (too generic)
```

## Grouping Principles

### One Feature = One Domain Concept

**Rule:** Each feature file should focus on ONE major domain object or capability.

**For Terraform modules, group by:**
- **Core resources** (primary infrastructure)
- **Integration points** (load balancers, DNS, service mesh)
- **Security** (IAM, security groups, encryption)
- **Observability** (logging, monitoring, tracing)
- **Scaling** (auto-scaling, capacity planning)
- **Networking** (VPC integration, routing, DNS)

**Example Structure for ECS Module:**
```
docs/features/
├── ecs-service-creation.feature        # Core: Creating the service
├── load-balancer-integration.feature   # Integration: ALB/NLB
├── security-configuration.feature      # Security: IAM roles, security groups
├── auto-scaling-policies.feature       # Scaling: Auto-scaling setup
├── cloudwatch-logging.feature          # Observability: Logs and metrics
└── service-connect.feature             # Advanced: Service mesh
```

### Scenario Count Per Feature

**Target:** 5-15 scenarios per feature file

**If you have:**
- **<5 scenarios:** Consider merging with related feature
- **>15 scenarios:** Split into more focused features

**Too many scenarios example:**
```gherkin
Feature: Complete ECS Configuration
  # 30+ scenarios covering everything
  # This should be split!
```

**Better organization:**
```
ecs-service-creation.feature      # 8 scenarios
load-balancer-integration.feature # 6 scenarios
auto-scaling-policies.feature     # 7 scenarios
```

### Background vs Feature Splitting

**Use Background when:**
- Setup is identical for all scenarios in the feature
- 3+ scenarios share the same Given steps

**Split into separate features when:**
- Different backgrounds are needed
- Scenarios test different capabilities
- Natural domain boundaries exist

**Example - Keep Together (shared background):**
```gherkin
Feature: Auto-scaling Policies

  Background:
    Given an ECS service with 2 running tasks
    And CloudWatch metrics are enabled

  Scenario: CPU-based scaling
  Scenario: Memory-based scaling
  Scenario: Request count scaling
  # All share the same background
```

**Example - Split Apart (different contexts):**
```gherkin
# ecs-service-creation.feature
Feature: ECS Service Creation
  Background:
    Given a VPC and subnets
    And an ECS cluster
  # Scenarios about creating services

# load-balancer-integration.feature
Feature: Load Balancer Integration
  Background:
    Given an existing ECS service
    And a load balancer
  # Scenarios about LB integration
```

## Avoiding Duplication

### Pattern 1: Parameterized Scenarios

**❌ Duplicate Scenarios:**
```gherkin
Scenario: Service with 256 CPU and 512 memory
  Given task definition with CPU 256 and memory 512
  When I create the service
  Then it should be created successfully

Scenario: Service with 512 CPU and 1024 memory
  Given task definition with CPU 512 and memory 1024
  When I create the service
  Then it should be created successfully

# 10+ more similar scenarios...
```

**✅ Scenario Outline:**
```gherkin
Scenario Outline: Service with various CPU/memory configurations
  Given task definition with CPU <cpu> and memory <memory>
  When I create the service
  Then it should be created successfully

  Examples: Valid Fargate configurations
    | cpu  | memory |
    | 256  | 512    |
    | 512  | 1024   |
    | 1024 | 2048   |
    | 2048 | 4096   |
```

### Pattern 2: Reusable Step Definitions

**❌ Similar but separate steps:**
```gherkin
Given I navigate to the service creation page
Given I open the service configuration screen
Given I go to the new service form
```

**✅ Generic step with parameter:**
```gherkin
Given I navigate to the "{page}" page
```

**Implementation Note:** The step definition handles different pages:
```python
@given('I navigate to the "{page}" page')
def navigate_to_page(page):
    page_factory.open(page)
```

### Pattern 3: Abstract Helper Steps

**❌ Over-specific scenarios:**
```gherkin
Scenario: Create service with CloudWatch logs
  Given a log group "/ecs/production/app"
  And log stream prefix "app"
  And retention period 7 days
  And log driver awslogs with region us-east-1
  And log options {"awslogs-stream-prefix": "app"}
  When I create the service
  Then logs should be sent to CloudWatch
```

**✅ Abstract scenario with implementation details hidden:**
```gherkin
Scenario: Create service with CloudWatch logs
  Given CloudWatch logging is configured
  When I create the service
  Then container logs should be sent to CloudWatch
  And logs should be retained according to policy
```

**Why better:**
- Scenario focuses on behavior, not implementation
- Implementation details handled in step definitions
- Easier to maintain when AWS API changes
- More readable for non-technical stakeholders

## File Organization Patterns

### Pattern A: Flat Structure (Simple Modules)

**When to use:** Modules with <5 major capabilities

```
docs/features/
├── README.md
├── core-functionality.feature
├── security-config.feature
├── networking.feature
└── observability.feature
```

**Example: S3 Bucket Module**
```
docs/features/
├── README.md
├── bucket-creation.feature         # Core functionality
├── encryption-configuration.feature # Security
├── lifecycle-policies.feature       # Advanced
└── access-logging.feature          # Observability
```

### Pattern B: Grouped Structure (Complex Modules)

**When to use:** Modules with 5-15 capabilities or clear domain groupings

```
docs/features/
├── README.md
├── core/
│   ├── service-creation.feature
│   └── task-definition.feature
├── integration/
│   ├── load-balancer.feature
│   ├── service-discovery.feature
│   └── service-connect.feature
├── security/
│   ├── iam-roles.feature
│   ├── security-groups.feature
│   └── secrets-management.feature
└── observability/
    ├── cloudwatch-logs.feature
    ├── cloudwatch-metrics.feature
    └── container-insights.feature
```

**Example: ECS Service Module**
```
docs/features/
├── README.md
├── core/
│   ├── fargate-service.feature
│   └── ec2-service.feature
├── networking/
│   ├── vpc-integration.feature
│   ├── load-balancer.feature
│   └── service-mesh.feature
└── scaling/
    ├── auto-scaling.feature
    └── capacity-planning.feature
```

### Pattern C: Layered Structure (Very Complex Modules)

**When to use:** Modules with >15 capabilities or multiple integration patterns

```
docs/features/
├── README.md
├── 01-essentials/
│   ├── basic-setup.feature
│   └── minimal-config.feature
├── 02-common-patterns/
│   ├── web-application.feature
│   ├── api-service.feature
│   └── background-worker.feature
├── 03-integrations/
│   ├── aws-services/
│   │   ├── alb-integration.feature
│   │   ├── nlb-integration.feature
│   │   └── route53-integration.feature
│   └── service-mesh/
│       ├── app-mesh.feature
│       └── service-connect.feature
└── 04-advanced/
    ├── multi-region.feature
    ├── blue-green-deployment.feature
    └── canary-deployment.feature
```

## Terraform-Specific Patterns

### Core Infrastructure Features

**Group by resource lifecycle:**
```
docs/features/
├── resource-creation.feature      # terraform apply
├── resource-updates.feature       # terraform apply (updates)
├── resource-deletion.feature      # terraform destroy
└── state-management.feature       # import, state operations
```

### Integration Testing Features

**Group by integration points:**
```
docs/features/
├── aws-integration.feature        # AWS provider
├── module-composition.feature     # Using other modules
├── data-sources.feature          # External data
└── provider-configuration.feature # Multi-region, aliases
```

### Validation Features

**Group by validation type:**
```
docs/features/
├── input-validation.feature      # Variable validation
├── output-validation.feature     # Output values
├── state-validation.feature      # State file checks
└── plan-validation.feature       # Plan output checks
```

## README.md Organization

### Feature Index Template

```markdown
# Gherkin Feature Specifications

Feature files documenting the behavior of this Terraform module.

## Core Features

Essential functionality:
- [Service Creation](./ecs-service-creation.feature) - Creating ECS Fargate services
- [Task Definition](./task-definition-config.feature) - Task configuration and containers

## Integration Features

External service integrations:
- [Load Balancer](./load-balancer-integration.feature) - ALB/NLB integration
- [Service Connect](./service-connect.feature) - Service mesh integration
- [Route53](./route53-dns.feature) - DNS configuration

## Security Features

Security and compliance:
- [IAM Roles](./iam-configuration.feature) - Task and execution roles
- [Security Groups](./security-groups.feature) - Network security
- [Secrets](./secrets-management.feature) - Secrets Manager integration

## Observability Features

Monitoring and logging:
- [CloudWatch Logs](./cloudwatch-logging.feature) - Container logging
- [CloudWatch Metrics](./cloudwatch-metrics.feature) - Service metrics
- [Container Insights](./container-insights.feature) - Enhanced monitoring

## Advanced Features

Optional capabilities:
- [Auto-scaling](./auto-scaling-policies.feature) - Service auto-scaling
- [Blue-Green](./blue-green-deployment.feature) - Deployment strategies

## Test-Driven Workflow

1. Write feature scenarios (this directory)
2. Generate tests from scenarios (`tests/`)
3. Implement module code (`main.tf`, etc.)
4. Validate with `terraform test`
5. Document in README.md
6. Create examples (`examples/`)

## Conventions

- **File naming:** kebab-case.feature
- **Location:** `docs/features/`
- **One feature per file:** Focus on single capability
- **Scenario count:** 5-15 scenarios per feature
- **Background:** Shared setup when 3+ scenarios need it
```

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Feature-Coupled Step Definitions

**Problem:** Steps that only work in specific features

```gherkin
# ecs-service.feature
Scenario: Create ECS service
  Given I have ECS prerequisites
  # Step only defined for ECS features
```

**Solution:** Generic, reusable steps

```gherkin
Scenario: Create ECS service
  Given I have the following resources:
    | type    | name       |
    | VPC     | vpc-123    |
    | Cluster | production |
  # Generic "I have resources" step works everywhere
```

### ❌ Anti-Pattern 2: Too Many Feature Files

**Problem:** One feature per scenario

```
docs/features/
├── scenario-1.feature (1 scenario)
├── scenario-2.feature (1 scenario)
├── scenario-3.feature (1 scenario)
# 50+ feature files...
```

**Solution:** Group related scenarios

```
docs/features/
├── service-creation.feature (10 scenarios)
├── load-balancer.feature (8 scenarios)
└── auto-scaling.feature (7 scenarios)
```

### ❌ Anti-Pattern 3: Everything in One File

**Problem:** All scenarios in one massive file

```gherkin
Feature: Complete ECS Module
  # 50+ scenarios covering everything
  # 1000+ lines
  # Impossible to navigate
```

**Solution:** Split by domain

```
docs/features/
├── core/
│   ├── service-creation.feature
│   └── task-definition.feature
└── integration/
    ├── load-balancer.feature
    └── service-discovery.feature
```

### ❌ Anti-Pattern 4: Inconsistent Naming

**Problem:** Mixed naming conventions

```
docs/features/
├── ECS_Service.feature
├── load-balancer-integration.feature
├── autoScaling.feature
└── Security.Groups.feature
```

**Solution:** Consistent kebab-case

```
docs/features/
├── ecs-service-creation.feature
├── load-balancer-integration.feature
├── auto-scaling-policies.feature
└── security-group-rules.feature
```

## Migration Strategies

### From Monolithic to Organized

**Step 1: Analyze current feature**
```bash
# Count scenarios
grep "^  Scenario:" docs/features/everything.feature | wc -l

# Identify groups
grep "^  Scenario:" docs/features/everything.feature | \
  sed 's/Scenario: //' | \
  sort
```

**Step 2: Create groups**
```
# Identify natural boundaries
- Service creation scenarios → service-creation.feature
- Load balancer scenarios → load-balancer.feature
- Security scenarios → security-configuration.feature
```

**Step 3: Split file**
```bash
# Extract scenarios by pattern
# Create new feature files
# Move related scenarios
# Update README.md index
```

**Step 4: Validate**
```bash
# Run tests to ensure nothing broke
terraform test

# Check for duplicate steps
grep "^  Given\|^  When\|^  Then" docs/features/*.feature | \
  sort | uniq -d
```

## Best Practices Checklist

**File Organization:**
- [ ] Features grouped by domain concept
- [ ] File names use kebab-case
- [ ] 5-15 scenarios per feature file
- [ ] README.md indexes all features
- [ ] Directory structure matches module complexity

**Scenario Organization:**
- [ ] Background used for shared setup (3+ scenarios)
- [ ] Scenario Outline used for parameterized tests
- [ ] Each scenario tests one specific behavior
- [ ] Scenarios are independent (can run in any order)

**Step Definition Organization:**
- [ ] Steps are reusable across features
- [ ] No feature-coupled step definitions
- [ ] Generic steps with parameters preferred
- [ ] Implementation details abstracted into helpers

**Maintenance:**
- [ ] No duplicate scenarios
- [ ] Consistent naming across all files
- [ ] Clear feature descriptions
- [ ] Tags used for organization (@smoke, @integration)

## Integration with Terraform Module Structure

### Alignment with Module Files

```
terraform-aws-ecs-service/
├── docs/
│   └── features/
│       ├── ecs-service.feature          ← Tests main.tf
│       ├── security-groups.feature      ← Tests security-group.tf
│       ├── iam-roles.feature           ← Tests iam-role-policies.tf
│       └── auto-scaling.feature        ← Tests scaling.tf
├── main.tf
├── security-group.tf
├── iam-role-policies.tf
└── scaling.tf
```

### Alignment with Tests

```
tests/
├── basic.tftest.hcl                     ← From ecs-service.feature
├── security-groups.tftest.hcl           ← From security-groups.feature
├── iam-roles.tftest.hcl                ← From iam-roles.feature
└── auto-scaling.tftest.hcl             ← From auto-scaling.feature
```

## References

- **Step Organization**: <https://cucumber.io/docs/gherkin/step-organization/>
- **Anti-Patterns**: <https://cucumber.io/docs/guides/anti-patterns/>
- **File Structure Instructions**: `.github/instructions/file-structure.instructions.md`
- **Scenario Shaper Agent**: `.github/agents/scenario-shaper.md`
- **Gherkin Scenarios Skill**: `.github/skills/gherkin-scenarios/SKILL.md`

## Quick Start

1. **Identify domain concepts** in your module
2. **Create feature files** following naming convention
3. **Group related scenarios** (5-15 per file)
4. **Use Background** for shared setup
5. **Abstract steps** for reusability
6. **Update README.md** with feature index
7. **Validate** with `terraform test`
