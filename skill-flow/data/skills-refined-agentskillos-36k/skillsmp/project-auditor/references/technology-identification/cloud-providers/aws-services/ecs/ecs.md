# Amazon ECS (Elastic Container Service)

**Category**: cloud-providers/aws-services
**Description**: Container orchestration service
**Homepage**: https://aws.amazon.com/ecs

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*ECS JavaScript packages*

- `@aws-sdk/client-ecs` - ECS SDK v3

#### PYPI
*ECS Python packages*

- `boto3` - AWS SDK (includes ECS)
- `ecs-deploy` - ECS deployment tool

#### GO
*ECS Go packages*

- `github.com/aws/aws-sdk-go-v2/service/ecs` - ECS SDK v2

#### MAVEN
*ECS Java packages*

- `software.amazon.awssdk:ecs` - SDK v2

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate ECS usage*

- `ecs-params.yml` - ECS CLI parameters
- `docker-compose.ecs.yml` - ECS Docker Compose
- `task-definition.json` - ECS task definition
- `appspec.yml` - CodeDeploy for ECS

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@aws-sdk/client-ecs['"]`
- ECS SDK v3 import
- Example: `import { ECSClient } from '@aws-sdk/client-ecs';`

#### Python
Extensions: `.py`

**Pattern**: `boto3\.client\(['"]ecs['"]\)`
- Boto3 ECS client
- Example: `ecs = boto3.client('ecs')`

### Code Patterns

**Pattern**: `ECS|taskDefinition|RunTask|DescribeServices|UpdateService`
- ECS operations
- Example: `client.run_task(cluster='...', taskDefinition='...')`

**Pattern**: `ECS_CLUSTER|ECS_SERVICE|ECS_TASK_DEFINITION`
- ECS environment variables
- Example: `ECS_CLUSTER=my-cluster`

**Pattern**: `arn:aws:ecs:[a-z0-9-]+:[0-9]+:`
- ECS ARN
- Example: `arn:aws:ecs:us-east-1:123456789:cluster/my-cluster`

**Pattern**: `Type:\s*['"]?AWS::ECS::`
- CloudFormation ECS resources

**Pattern**: `"containerDefinitions"|"executionRoleArn"|"taskRoleArn"`
- Task definition JSON
- Example: Task definition file

---

## Environment Variables

- `ECS_CLUSTER` - ECS cluster name
- `ECS_SERVICE` - ECS service name
- `ECS_TASK_DEFINITION` - Task definition name
- `ECS_CONTAINER_METADATA_URI` - Container metadata endpoint
- `ECS_AGENT_URI` - ECS agent URI

## Detection Notes

- Fargate for serverless containers
- EC2 launch type for more control
- Task definitions define containers
- Services maintain desired count
- Integration with ALB/NLB for load balancing

---

## TIER 3: Configuration Extraction

### Cluster Name Extraction

**Pattern**: `(?:cluster|ECS_CLUSTER)\s*[=:]\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- ECS cluster name
- Extracts: `cluster_name`
- Example: `ECS_CLUSTER=my-cluster`

### Task Definition Extraction

**Pattern**: `(?:taskDefinition|task[_-]?definition|ECS_TASK_DEFINITION)\s*[=:]\s*['"]?([a-zA-Z0-9_:-]+)['"]?`
- Task definition name/ARN
- Extracts: `task_definition`
- Example: `taskDefinition: my-task:1`
