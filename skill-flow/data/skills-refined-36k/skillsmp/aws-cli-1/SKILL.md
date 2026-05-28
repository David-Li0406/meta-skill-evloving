---
name: aws-cli
description: Use when interacting with AWS - managing S3, EC2, Lambda, IAM, CloudFormation, ECS/EKS, RDS, DynamoDB, CloudWatch, or any AWS service
---

# AWS CLI

> **MANDATORY: All AWS CLI commands MUST run in subagents.**
>
> Use Task tool with `subagent_type: "general"`. Never run `aws` directly in your session.
> AWS operations can be long-running, may require investigation, and must be isolated from your main context.
> **No exceptions.**

## CLI Structure

```
aws <service> <command> [options]
```

## Investigation Pattern (for subagents)

You are running in a subagent. Use built-in help to discover commands and options:

1. `aws help` - List all services
2. `aws <service> help` - List commands for a service
3. `aws <service> <command> help` - Full command documentation with all flags

This is the preferred way to learn command syntax rather than guessing.

## Essential Flags

| Flag | Purpose |
|------|---------|
| `--output json` | Scriptable output (also: `text`, `table`) |
| `--query <expr>` | JMESPath filtering |
| `--profile <name>` | Use named profile |
| `--region <r>` | Specify region |
| `--no-cli-pager` | Disable pager (critical for scripts) |

> **REQUIRED: Always specify `--profile` and `--region`**: Do not rely on defaults or environment variables. Every command must include `--profile <name> --region <region>` for predictable, explicit behavior.

## Profile Discovery

**Before running ANY AWS command, discover available profiles:**

```bash
aws configure list-profiles
```

**Profile selection logic:**

1. **User specified profile**: Use it exactly as given
2. **Single profile exists**: Use it (no ambiguity)
3. **Multiple profiles - infer from context**:
   - Task mentions "production/prod" → look for profile containing `prod`
   - Task mentions "qa" → look for profile containing `qa`
   - Task mentions "development/dev" → look for profile containing `dev`
   - Task mentions specific account/environment → match by name
4. **Cannot infer confidently**: **ASK the user** - list available profiles and request selection

**Example inference:**
```
Available: default, mycompany-dev, mycompany-prod, mycompany-qa
Task: "Check production EC2 instances"
→ Infer: mycompany-prod (contains "prod", matches "production" in task)
```

**When to ask (use Question tool):**
- Multiple profiles match (e.g., `prod-us`, `prod-eu` when task says "production")
- No profile matches task context
- Task is destructive (delete, terminate, modify) and you want confirmation
- Profile names are ambiguous or don't follow conventions

## When NOT to Use

- **AWS CDK/SDK**: For programmatic access (boto3, JS SDK), use those libraries' docs
- **Terraform/Pulumi**: Infrastructure-as-code tools have their own patterns
- **AWS Console**: This skill is CLI-specific
- **LocalStack**: Different endpoints and behavior

## Quick Examples

> All commands require `--profile <p> --region <r>` (omitted below for brevity)

| Task | Command |
|------|---------|
| Caller identity | `aws sts get-caller-identity` |
| List S3 buckets | `aws s3 ls` |
| Describe instances | `aws ec2 describe-instances` |
| List functions | `aws lambda list-functions` |
| Deploy stack | `aws cloudformation deploy --template-file t.yaml --stack-name s` |
| Get secret | `aws secretsmanager get-secret-value --secret-id name` |

## JMESPath Query Patterns

```bash
# Filter by tag
--query 'Reservations[].Instances[?Tags[?Key==`Name`].Value|[0]==`web`]'

# Extract specific fields
--query 'Reservations[].Instances[].[InstanceId,State.Name]' --output table

# Get first matching item
--query 'Buckets[?starts_with(Name,`prod`)].Name | [0]' --output text
```

## Common Mistakes

- **Missing `--profile` or `--region`**: Commands may target wrong account/region silently
- **Running `aws` directly**: Always delegate to subagent via Task tool
- **Guessing syntax**: Use `aws <service> <command> help` instead of guessing flags
- **Ignoring pager**: Scripts hang without `--no-cli-pager` or `AWS_PAGER=""`

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I'll just run this one command quickly" | AWS commands can hang on pager, trigger rate limits, or need retries. Context isolation protects your main session. |
| "The default profile/region is fine" | Defaults change, env vars get misconfigured. One wrong-account command can cause outages. |
| "I remember this syntax" | AWS CLI has 200+ services with dozens of commands each. Memory errors are guaranteed. Use `aws help`. |
| "This is a read-only command, it's safe" | Safety isn't the issue—context isolation is. Even `describe` can reveal you need 5 more commands. |
| "Subagent overhead is unnecessary" | Subagent launch takes seconds; debugging context pollution takes minutes. |
| "I can guess which profile to use" | Profile names vary wildly. Run `aws configure list-profiles` - takes 1 second, prevents wrong-account disasters. |
| "There's probably only one profile" | Many systems have 5+ profiles. Discovery is cheap; wrong-account commands are expensive. |
| "Asking the user slows things down" | Running against wrong account is slower. When in doubt, ask. |

**All of these mean: Delegate to subagent. No exceptions.**

## Dispatching Subagents

When delegating AWS tasks, include in your subagent prompt:

1. Load the aws-cli skill and review ./gotchas.md (relative to this skill) before running commands
2. Run `aws configure list-profiles` first to discover available profiles
3. If user didn't specify profile: infer from context or ask using Question tool
4. Always use `--profile <name> --region <region>` explicitly
5. Use `aws <service> <command> help` to verify syntax
6. Report findings back

**Example dispatch prompt (profile specified):**
> Check the status of EC2 instance i-0abc123 in us-east-1 using profile 'prod'.
> Load the aws-cli skill first and check ./gotchas.md. Use explicit --profile
> and --region flags. Report instance state and any relevant details.

**Example dispatch prompt (profile NOT specified):**
> Check if our production Lambda functions are healthy.
> Load the aws-cli skill first. Run `aws configure list-profiles` to discover
> available profiles. Infer the correct profile from context (look for 'prod'
> in profile names). If multiple profiles match or none match, ask the user
> which profile to use. Check ./gotchas.md, use explicit --profile and --region.

## Cross-Service Gotchas

See: `./gotchas.md` (in this skill's directory) for non-obvious behaviors that cause common errors.

## Testing Status

> **TODO**: This skill needs TDD validation per writing-skills guidelines.
>
> **Required tests:**
> 1. Pressure scenario: "Urgently check if EC2 instance is running" - verify subagent delegation
> 2. Pressure scenario: "Quick S3 bucket check" - verify --profile/--region compliance
> 3. Document baseline rationalizations agents use without skill loaded
> 4. Verify skill changes agent behavior under pressure
