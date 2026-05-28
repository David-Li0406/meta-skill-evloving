# AWS Step Functions

**Category**: cloud-providers/aws-services
**Description**: Serverless workflow orchestration service
**Homepage**: https://aws.amazon.com/step-functions

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Step Functions packages*

- `@aws-sdk/client-sfn` - Step Functions SDK v3
- `aws-sdk-client-mock` - SDK mock (commonly used)

#### PYPI
*Step Functions Python packages*

- `boto3` - AWS SDK (includes Step Functions)

#### GO
*Step Functions Go packages*

- `github.com/aws/aws-sdk-go-v2/service/sfn` - Step Functions SDK

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Step Functions usage*

- `statemachine.asl.json` - State machine definition
- `workflow.asl.json` - Alternative definition file

### Code Patterns

**Pattern**: `states\.[a-z0-9-]+\.amazonaws\.com`
- Step Functions endpoint

**Pattern**: `StartExecution|DescribeExecution|StopExecution`
- Step Functions operations

**Pattern**: `"Type":\s*"(?:Task|Choice|Wait|Parallel|Map|Pass|Succeed|Fail)"`
- Amazon States Language types

**Pattern**: `arn:aws:states:[a-z0-9-]+:[0-9]+:stateMachine:`
- State machine ARN

**Pattern**: `Type:\s*['"]?AWS::StepFunctions::`
- CloudFormation Step Functions resources

**Pattern**: `"StartAt"|"States"|"Resource":\s*"arn:aws:lambda`
- State machine definition patterns

---

## Environment Variables

- `STATE_MACHINE_ARN` - State machine ARN
- `STEP_FUNCTIONS_ARN` - Alternative ARN variable

## Detection Notes

- Amazon States Language (ASL) for definitions
- Standard and Express workflows
- Integrates with Lambda, ECS, DynamoDB
- Map state for parallel iteration
- Error handling built-in

---

## TIER 3: Configuration Extraction

### State Machine ARN Extraction

**Pattern**: `(?:stateMachineArn|state[_-]?machine[_-]?arn|STATE_MACHINE_ARN)\s*[=:]\s*['"]?(arn:aws:states:[^\s'"]+)['"]?`
- State machine ARN
- Extracts: `state_machine_arn`
