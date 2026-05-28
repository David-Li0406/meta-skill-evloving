# Amazon EKS (Elastic Kubernetes Service)

**Category**: cloud-providers/aws-services
**Description**: Managed Kubernetes service
**Homepage**: https://aws.amazon.com/eks

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*EKS JavaScript packages*

- `@aws-sdk/client-eks` - EKS SDK v3

#### PYPI
*EKS Python packages*

- `boto3` - AWS SDK (includes EKS)

#### GO
*EKS Go packages*

- `github.com/aws/aws-sdk-go-v2/service/eks` - EKS SDK v2
- `sigs.k8s.io/aws-iam-authenticator` - IAM authenticator

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate EKS usage*

- `eksctl.yaml` - eksctl configuration
- `cluster.yaml` - Cluster configuration

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@aws-sdk/client-eks['"]`
- EKS SDK v3 import
- Example: `import { EKSClient } from '@aws-sdk/client-eks';`

#### Python
Extensions: `.py`

**Pattern**: `boto3\.client\(['"]eks['"]\)`
- Boto3 EKS client
- Example: `eks = boto3.client('eks')`

### Code Patterns

**Pattern**: `EKS|eksctl|eks\.amazonaws\.com`
- EKS references
- Example: `eksctl create cluster`

**Pattern**: `EKS_CLUSTER|EKS_CLUSTER_NAME`
- EKS environment variables
- Example: `EKS_CLUSTER_NAME=my-cluster`

**Pattern**: `arn:aws:eks:[a-z0-9-]+:[0-9]+:cluster/`
- EKS cluster ARN
- Example: `arn:aws:eks:us-east-1:123456789:cluster/my-cluster`

**Pattern**: `Type:\s*['"]?AWS::EKS::Cluster`
- CloudFormation EKS resource

**Pattern**: `apiVersion:\s*eksctl\.io/`
- eksctl configuration
- Example: `apiVersion: eksctl.io/v1alpha5`

**Pattern**: `aws eks update-kubeconfig|aws eks get-token`
- AWS CLI EKS commands
- Example: `aws eks update-kubeconfig --name my-cluster`

---

## Environment Variables

- `EKS_CLUSTER_NAME` - Cluster name
- `AWS_EKS_CLUSTER_NAME` - Alternative cluster name
- `KUBECONFIG` - Kubeconfig path

## Detection Notes

- Managed Kubernetes control plane
- Uses IAM for authentication
- eksctl is the official CLI tool
- Integrates with AWS services via IRSA
- Fargate profiles for serverless pods

---

## TIER 3: Configuration Extraction

### Cluster Name Extraction

**Pattern**: `(?:cluster[_-]?name|EKS_CLUSTER_NAME|name)\s*[=:]\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- EKS cluster name
- Extracts: `cluster_name`
- Example: `EKS_CLUSTER_NAME=my-cluster`

### Region Extraction

**Pattern**: `(?:region|AWS_REGION)\s*[=:]\s*['"]?([a-z]{2}-[a-z]+-[0-9]+)['"]?`
- AWS region
- Extracts: `region`
- Example: `region: us-east-1`
