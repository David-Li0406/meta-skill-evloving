# AWS CloudFormation

**Category**: developer-tools/infrastructure
**Description**: AWS CloudFormation - Infrastructure as Code service for AWS resources
**Homepage**: https://aws.amazon.com/cloudformation/

## Package Detection

### NPM
- `aws-cdk`
- `aws-cdk-lib`
- `@aws-cdk/*`

### PYPI
- `aws-cdk-lib`
- `aws-cdk.core`
- `troposphere`
- `sceptre`

## Configuration Files

- `template.yaml`
- `template.yml`
- `template.json`
- `cloudformation.yaml`
- `cloudformation.yml`
- `*.template.yaml`
- `*.template.yml`
- `*.template.json`
- `samconfig.toml` (SAM)
- `cdk.json` (CDK)
- `cdk.context.json`

## File Patterns

- Files with `AWSTemplateFormatVersion`
- Files with `Transform: AWS::Serverless`

## Environment Variables

- `AWS_DEFAULT_REGION`
- `AWS_REGION`
- `AWS_PROFILE`
- `CDK_DEFAULT_ACCOUNT`
- `CDK_DEFAULT_REGION`

## Detection Notes

- Look for YAML/JSON with AWSTemplateFormatVersion
- Check for cdk.json (AWS CDK projects)
- SAM templates have AWS::Serverless transform
- Check for nested stacks pattern
- Look for cfn-lint configuration

## Detection Confidence

- **Template Detection**: 95% (HIGH)
- **CDK Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
