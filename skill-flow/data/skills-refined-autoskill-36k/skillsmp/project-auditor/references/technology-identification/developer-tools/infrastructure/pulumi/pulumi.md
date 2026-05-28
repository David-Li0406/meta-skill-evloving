# Pulumi

**Category**: developer-tools/infrastructure
**Description**: Pulumi - Infrastructure as Code using general-purpose programming languages
**Homepage**: https://www.pulumi.com

## Package Detection

### NPM
- `@pulumi/pulumi`
- `@pulumi/aws`
- `@pulumi/azure-native`
- `@pulumi/gcp`
- `@pulumi/kubernetes`
- `@pulumi/docker`

### PYPI
- `pulumi`
- `pulumi-aws`
- `pulumi-azure-native`
- `pulumi-gcp`
- `pulumi-kubernetes`

### GO
- `github.com/pulumi/pulumi/sdk/v3`
- `github.com/pulumi/pulumi-aws/sdk/v6`

## Configuration Files

- `Pulumi.yaml`
- `Pulumi.*.yaml` (stack configs)
- `Pulumi.dev.yaml`
- `Pulumi.prod.yaml`

## Environment Variables

- `PULUMI_ACCESS_TOKEN`
- `PULUMI_CONFIG_PASSPHRASE`
- `PULUMI_BACKEND_URL`

## Detection Notes

- Look for Pulumi.yaml in repository root
- Uses TypeScript, Python, Go, C#, Java, or YAML
- Stack configs contain environment-specific values
- Check for pulumi in dependencies

## Detection Confidence

- **Pulumi.yaml Detection**: 95% (HIGH)
- **Package Detection**: 95% (HIGH)
