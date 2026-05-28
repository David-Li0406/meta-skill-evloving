---
name: gherkin-scenarios
description: 'Create and write Gherkin scenarios using Given/When/Then syntax for behavior-driven development (BDD) and test specifications. Use when asked to "write scenarios", "create features", "add Given/When/Then", "write BDD specs", or when documenting expected behavior, acceptance criteria, or test cases in a human-readable format. Supports Background, Scenario Outline, Examples, and Data Tables.'
---

# Gherkin Scenarios

Write behavior-driven development (BDD) scenarios using Gherkin syntax. Gherkin uses Given/When/Then steps to describe expected behavior in plain language that both technical and non-technical stakeholders can understand.

## When to Use This Skill

- User asks to "write scenarios", "create features", "add Given/When/Then", or "write BDD specs"
- Documenting expected behavior for Terraform modules or infrastructure
- Creating acceptance criteria for features
- Writing test specifications in human-readable format
- Converting requirements into executable specifications
- Documenting workflows or processes in structured format
- Creating scenario-driven tests (e.g., for terraform-tester agent)

## Gherkin File Structure

### Feature File Format

````gherkin
Feature: Brief description of the feature

  Optional longer description that provides
  more context about the feature.

  Background:
    Given common setup steps
    And shared preconditions

  Scenario: Description of specific scenario
    Given a precondition
    And another precondition
    When an action occurs
    And another action
    Then expect this outcome
    And expect another outcome

  Scenario Outline: Parameterized scenario
    Given a <parameter>
    When I perform <action>
    Then I expect <result>

    Examples:
      | parameter | action  | result  |
      | value1    | action1 | result1 |
      | value2    | action2 | result2 |
````

### File Location

Store Gherkin feature files in:
```
docs/features/
├── README.md
├── feature-name.feature
├── another-feature.feature
└── nested/
    └── specific-feature.feature
```

## Keywords and Structure

### Feature

**Purpose:** High-level description of a software feature or module capability.

**Format:**
```gherkin
Feature: Name of the feature
  Optional free-form description
  that can span multiple lines
```

**Example:**
```gherkin
Feature: ECS Service Creation
  As a DevOps engineer
  I want to create ECS Fargate services
  So that I can deploy containerized applications
```

### Background

**Purpose:** Common steps that run before each scenario in the feature.

**When to Use:**
- Setup steps needed for all scenarios
- Common preconditions
- Shared test data

**Example:**
```gherkin
Background:
  Given a VPC with ID "vpc-12345678"
  And subnets in availability zones "us-east-1a" and "us-east-1b"
  And an ECS cluster named "production"
```

**Note:** Background runs before EACH scenario, not just once per feature.

### Scenario

**Purpose:** Concrete example of business rule or acceptance criterion.

**Format:**
```gherkin
Scenario: Descriptive title
  Given [precondition]
  When [action]
  Then [expected outcome]
```

**Example:**
```gherkin
Scenario: Create service with auto-scaling enabled
  Given a task definition with CPU 1024 and memory 2048
  And auto-scaling configuration with min 2 and max 10 tasks
  When I create the ECS service
  Then the service should be created successfully
  And auto-scaling should be configured with target CPU utilization 70%
  And the service should have 2 running tasks initially
```

### Given (Preconditions)

**Purpose:** Set up the initial state/context for the scenario.

**Best Practices:**
- Describe the state BEFORE the action
- Use past tense or present tense ("is configured", "exists")
- Avoid action words like "create", "setup" (those are implementation details)

**Examples:**
```gherkin
Given a container definition for "nginx:latest"
Given the module is configured with enable_access_logs set to true
Given an existing S3 bucket for access logs
Given a load balancer listener on port 443
```

### When (Actions)

**Purpose:** Describe the key action/event in the scenario.

**Best Practices:**
- Use present tense
- Focus on the trigger or action
- Usually only ONE When per scenario (use And for related actions)

**Examples:**
```gherkin
When I create the ECS service
When I apply the Terraform configuration
When the health check fails
When I update the task definition
```

### Then (Expected Outcomes)

**Purpose:** Describe the expected result or observable outcome.

**Best Practices:**
- Use present tense
- Focus on observable outcomes
- Avoid implementation details
- Can have multiple Then statements (use And)

**Examples:**
```gherkin
Then the service should be running
Then terraform plan should show no changes
Then the security group should allow HTTPS traffic
Then the task count should be 3
And the service should have tags "Environment: Production"
```

### And / But

**Purpose:** Additional steps of the same type (Given/When/Then).

**Usage:**
```gherkin
Given a VPC
And two subnets
And a security group

When I create the service
And I enable auto-scaling

Then the service should be created
And it should have 2 tasks
But it should not have public IP addresses
```

**Note:** And/But are syntactic sugar - they inherit the type (Given/When/Then) from the previous step.

## Scenario Outline (Parameterization)

**Purpose:** Run the same scenario with different input values.

**Format:**
```gherkin
Scenario Outline: Title with <placeholder>
  Given a <parameter>
  When I do <action>
  Then I expect <result>

  Examples:
    | parameter | action  | result  |
    | value1    | action1 | result1 |
    | value2    | action2 | result2 |
```

**Example:**
```gherkin
Scenario Outline: Create service with different CPU and memory configurations
  Given a task definition with CPU <cpu> and memory <memory>
  When I create the ECS service
  Then the task should be configured with <cpu> CPU units
  And the task should be configured with <memory> MB memory

  Examples: Valid Fargate configurations
    | cpu  | memory |
    | 256  | 512    |
    | 256  | 1024   |
    | 512  | 1024   |
    | 1024 | 2048   |
```

### Multiple Example Tables

```gherkin
Scenario Outline: Service creation with various configurations
  Given CPU <cpu> and memory <memory>
  When I create the service
  Then it should be <status>

  Examples: Valid configurations
    | cpu  | memory | status  |
    | 256  | 512    | success |
    | 1024 | 2048   | success |

  Examples: Invalid configurations
    | cpu  | memory | status |
    | 128  | 256    | error  |
    | 256  | 128    | error  |
```

## Data Tables

**Purpose:** Pass structured data to a step.

**Format:**
```gherkin
Given the following container environment variables:
  | name        | value       |
  | ENVIRONMENT | production  |
  | LOG_LEVEL   | info        |
  | REGION      | us-east-1   |
```

**With Headers:**
```gherkin
Then the service should have the following tags:
  | key         | value      |
  | Environment | production |
  | ManagedBy   | Terraform  |
  | CostCenter  | engineering|
```

**Without Headers (Lists):**
```gherkin
Given the following allowed ports:
  | 80   |
  | 443  |
  | 8080 |
```

## Tags

**Purpose:** Organize and filter scenarios.

**Format:**
```gherkin
@integration @aws
Feature: ECS Service Creation

@smoke @fast
Scenario: Basic service creation
  Given minimal configuration
  When I create the service
  Then it should succeed

@slow @network
Scenario: Service with load balancer
  Given a load balancer configuration
  When I create the service
  Then it should be registered with the load balancer
```

**Common Tag Patterns:**
- `@smoke` - Quick smoke tests
- `@integration` - Integration tests
- `@unit` - Unit tests
- `@wip` - Work in progress
- `@skip` - Skip this scenario
- `@aws`, `@azure`, `@gcp` - Cloud provider specific
- `@slow`, `@fast` - Execution time hints

## Doc Strings (Multiline Text)

**Purpose:** Pass large blocks of text to a step.

**Format:**
```gherkin
Given the following IAM policy:
  """
  {
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::bucket/*"
    }]
  }
  """
```

**Alternative Syntax:**
```gherkin
Given the following container definition:
  """json
  {
    "name": "app",
    "image": "nginx:latest",
    "portMappings": [{
      "containerPort": 80,
      "protocol": "tcp"
    }]
  }
  """
```

## Comments

**Format:**
```gherkin
# This is a comment
# Comments can appear anywhere
# They are ignored during parsing

Feature: ECS Service
  # This feature creates ECS services

  Scenario: Basic creation
    # Setup phase
    Given a task definition
    # Execute phase
    When I create the service
    # Verify phase
    Then it should be running
```

## Best Practices

### 1. Write Declarative Steps (Not Imperative)

**❌ Bad (Imperative - How):**
```gherkin
Given I click the "Create Service" button
And I enter "my-service" in the name field
And I select "Fargate" from the launch type dropdown
When I click "Submit"
```

**✅ Good (Declarative - What):**
```gherkin
Given a service configuration named "my-service"
And the launch type is set to Fargate
When I create the service
```

### 2. One Scenario = One Behavior

**❌ Bad (Multiple behaviors):**
```gherkin
Scenario: Service creation and scaling
  Given a service configuration
  When I create the service
  Then it should be running
  When I update the desired count to 5
  Then it should have 5 tasks
  When I enable auto-scaling
  Then it should scale based on CPU
```

**✅ Good (Separate scenarios):**
```gherkin
Scenario: Service creation
  Given a service configuration
  When I create the service
  Then it should be running with the desired task count

Scenario: Service scaling
  Given an existing service
  When I update the desired count to 5
  Then it should have 5 running tasks

Scenario: Auto-scaling configuration
  Given an existing service
  When I enable auto-scaling with CPU target 70%
  Then it should scale based on CPU utilization
```

### 3. Use Background for Common Setup

**❌ Bad (Repeated setup):**
```gherkin
Scenario: Create service
  Given a VPC and subnets
  And an ECS cluster
  When I create the service
  Then it should succeed

Scenario: Service with load balancer
  Given a VPC and subnets
  And an ECS cluster
  And a load balancer
  When I create the service
  Then it should be registered
```

**✅ Good (Background):**
```gherkin
Background:
  Given a VPC with subnets
  And an ECS cluster named "production"

Scenario: Create service
  When I create the service
  Then it should succeed

Scenario: Service with load balancer
  Given a load balancer configuration
  When I create the service
  Then it should be registered with the load balancer
```

### 4. Keep Scenarios Focused and Short

**Target:**
- 3-7 steps per scenario
- 5-10 scenarios per feature
- Each scenario tests ONE thing

**If scenarios are too long:**
- Split into multiple scenarios
- Use Background for common setup
- Use Scenario Outline for variations

### 5. Use Meaningful Scenario Titles

**❌ Bad:**
```gherkin
Scenario: Test 1
Scenario: Service creation works
Scenario: Check if it works
```

**✅ Good:**
```gherkin
Scenario: Create service with minimum required configuration
Scenario: Service creation fails when VPC is missing
Scenario: Auto-scaling enables when min and max capacity are defined
```

### 6. Avoid Technical Implementation Details

**❌ Bad (Too technical):**
```gherkin
Given I execute "aws ecs create-service" command
And I pass the "--cluster" flag with "production"
When the API returns 200
Then the JSON response contains "serviceArn"
```

**✅ Good (Business language):**
```gherkin
Given a service configuration for cluster "production"
When I create the service
Then the service should be created successfully
And it should have a valid ARN
```

## Terraform Module Scenarios Example

### Complete Feature File

```gherkin
Feature: ECS Fargate Service Creation
  As a DevOps engineer
  I want to create ECS Fargate services using Terraform
  So that I can deploy containerized applications with proper configuration

  Background:
    Given a VPC with ID "vpc-12345678"
    And private subnets in two availability zones
    And an ECS cluster named "production"
    And a CloudPosse label context with namespace "luscii" and environment "prod"

  @smoke @essential
  Scenario: Create service with minimum required configuration
    Given a container definition for "nginx:latest" on port 80
    And a task definition with 256 CPU and 512 MB memory
    When I create the ECS service with name "web-app"
    Then the service should be created in the "production" cluster
    And it should have 1 running task
    And it should use Fargate launch type
    And it should have CloudPosse generated name "luscii-prod-web-app"

  @networking
  Scenario: Service with load balancer integration
    Given a container definition with port mapping for port 8080
    And a task definition with 512 CPU and 1024 MB memory
    And an Application Load Balancer target group for port 8080
    When I create the ECS service with load balancer configuration
    Then the service should be registered with the target group
    And health checks should be configured on path "/health"
    And the service should wait for load balancer to become healthy

  @scaling
  Scenario Outline: Service with auto-scaling
    Given a task definition with <cpu> CPU and <memory> MB memory
    And auto-scaling configuration with min <min> and max <max> tasks
    And target tracking policy for <metric> at <target>%
    When I create the ECS service
    Then auto-scaling should be enabled
    And it should scale between <min> and <max> tasks
    And it should target <target>% for <metric>

    Examples: CPU-based scaling
      | cpu  | memory | min | max | metric | target |
      | 512  | 1024   | 2   | 10  | CPU    | 70     |
      | 1024 | 2048   | 3   | 15  | CPU    | 60     |

    Examples: Memory-based scaling
      | cpu  | memory | min | max | metric | target |
      | 512  | 1024   | 2   | 8   | Memory | 80     |
      | 1024 | 2048   | 2   | 10  | Memory | 75     |

  @security
  Scenario: Service with security group configuration
    Given a container definition for "api:v1.2.3"
    And a security group allowing HTTPS from load balancer
    When I create the ECS service
    Then the service should use the configured security group
    And it should only allow inbound traffic on port 443
    And all outbound traffic should be allowed

  @observability
  Scenario: Service with CloudWatch logging
    Given a container definition with CloudWatch log configuration
    And log group "/ecs/production/web-app"
    And log retention period of 7 days
    When I create the ECS service
    Then container logs should be sent to CloudWatch
    And logs should be retained for 7 days
    And log streams should be created per task

  @secrets
  Scenario: Service with secrets from Secrets Manager
    Given a container definition for "app:latest"
    And the following secrets from AWS Secrets Manager:
      | name          | secret_arn                                        |
      | DATABASE_URL  | arn:aws:secretsmanager:us-east-1:123:secret:db   |
      | API_KEY       | arn:aws:secretsmanager:us-east-1:123:secret:api  |
    When I create the ECS service
    Then the task should have access to the secrets
    And the execution role should have secretsmanager:GetSecretValue permission
    And secrets should be injected as environment variables

  @negative @validation
  Scenario: Service creation fails with invalid configuration
    Given a task definition with 128 CPU and 256 MB memory
    When I attempt to create the ECS service
    Then the creation should fail
    And the error should indicate "Invalid CPU/memory combination for Fargate"
```

## Language Support

Gherkin supports keywords in multiple languages:

```gherkin
# language: nl
Functionaliteit: ECS Service Aanmaken

  Achtergrond:
    Gegeven een VPC met ID "vpc-12345678"
    En subnets in twee availability zones

  Scenario: Basis service aanmaken
    Gegeven een container definitie voor "nginx:latest"
    Als ik de ECS service aanmaak
    Dan zou de service succesvol aangemaakt moeten worden
```

**Specify language:**
```gherkin
# language: es
# language: fr
# language: de
# language: nl
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Scenarios too long | Split into multiple scenarios, use Background |
| Too much repetition | Use Scenario Outline with Examples |
| Too technical | Focus on behavior, not implementation |
| Unclear intent | Add feature description, use descriptive titles |
| Hard to understand | Use Given/When/Then structure clearly |

## Validation

**Good Scenario Checklist:**
- [ ] Has descriptive title
- [ ] Uses Given (setup), When (action), Then (verify)
- [ ] Tests one specific behavior
- [ ] Written in business language
- [ ] Avoids implementation details
- [ ] Could be understood by non-technical stakeholder
- [ ] 3-7 steps total

## References

- **Gherkin Reference**: <https://cucumber.io/docs/gherkin/reference/>
- **Gherkin Best Practices**: <https://cucumber.io/docs/bdd/>
- **Given/When/Then Guide**: <https://martinfowler.com/bliki/GivenWhenThen.html>
- **Writing Better Scenarios**: <https://cucumber.io/docs/bdd/better-gherkin/>

## Quick Start

1. **Identify the feature** - What capability are you documenting?
2. **Write feature description** - High-level purpose
3. **List scenarios** - What specific behaviors exist?
4. **For each scenario:**
   - Given: What's the starting state?
   - When: What action triggers the behavior?
   - Then: What's the expected outcome?
5. **Add tags** for organization
6. **Review** for clarity and business language
7. **Store** in `docs/features/` directory
