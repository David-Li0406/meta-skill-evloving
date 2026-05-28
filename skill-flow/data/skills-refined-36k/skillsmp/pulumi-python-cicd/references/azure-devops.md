# Azure DevOps Pipeline Templates

## Basic Pipeline

```yaml
# azure-pipelines.yml
trigger:
  - main

pr:
  - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: pulumi-secrets  # Contains PULUMI_ACCESS_TOKEN

stages:
  - stage: Preview
    condition: eq(variables['Build.Reason'], 'PullRequest')
    jobs:
      - job: Preview
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '3.11'
          
          - script: pip install -r requirements.txt
            displayName: 'Install dependencies'
          
          - task: Pulumi@1
            inputs:
              command: 'preview'
              stack: 'org/project/dev'
              azureSubscription: 'Azure-Connection'
            env:
              PULUMI_ACCESS_TOKEN: $(PULUMI_ACCESS_TOKEN)

  - stage: DeployDev
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployDev
        environment: 'development'
        strategy:
          runOnce:
            deploy:
              steps:
                - checkout: self
                
                - task: UsePythonVersion@0
                  inputs:
                    versionSpec: '3.11'
                
                - script: pip install -r requirements.txt
                  displayName: 'Install dependencies'
                
                - task: Pulumi@1
                  inputs:
                    command: 'up'
                    stack: 'org/project/dev'
                    args: '--yes'
                    azureSubscription: 'Azure-Connection'
                  env:
                    PULUMI_ACCESS_TOKEN: $(PULUMI_ACCESS_TOKEN)

  - stage: DeployProd
    dependsOn: DeployDev
    condition: succeeded()
    jobs:
      - deployment: DeployProd
        environment: 'production'  # Requires approval
        strategy:
          runOnce:
            deploy:
              steps:
                - checkout: self
                
                - task: UsePythonVersion@0
                  inputs:
                    versionSpec: '3.11'
                
                - script: pip install -r requirements.txt
                  displayName: 'Install dependencies'
                
                - task: Pulumi@1
                  inputs:
                    command: 'up'
                    stack: 'org/project/prod'
                    args: '--yes'
                    azureSubscription: 'Azure-Connection'
                  env:
                    PULUMI_ACCESS_TOKEN: $(PULUMI_ACCESS_TOKEN)
```

## Multi-Stack Pipeline

```yaml
# azure-pipelines.yml
parameters:
  - name: stacks
    type: object
    default:
      - name: 'networking'
        path: 'infrastructure/networking'
        order: 1
      - name: 'database'
        path: 'infrastructure/database'
        order: 2
      - name: 'application'
        path: 'infrastructure/application'
        order: 3

trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

stages:
  - ${{ each stack in parameters.stacks }}:
    - stage: Deploy_${{ stack.name }}
      dependsOn: ${{ if gt(stack.order, 1) }}Deploy_${{ parameters.stacks[stack.order - 2].name }}${{ else }}[]${{ /if }}
      jobs:
        - deployment: Deploy
          environment: 'production'
          strategy:
            runOnce:
              deploy:
                steps:
                  - checkout: self
                  
                  - task: UsePythonVersion@0
                    inputs:
                      versionSpec: '3.11'
                  
                  - script: |
                      cd ${{ stack.path }}
                      pip install -r requirements.txt
                    displayName: 'Install dependencies'
                  
                  - task: Pulumi@1
                    inputs:
                      command: 'up'
                      stack: 'org/${{ stack.name }}/prod'
                      args: '--yes'
                      cwd: '${{ stack.path }}'
                    env:
                      PULUMI_ACCESS_TOKEN: $(PULUMI_ACCESS_TOKEN)
```

## With AWS OIDC

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

jobs:
  - job: Deploy
    steps:
      - task: UsePythonVersion@0
        inputs:
          versionSpec: '3.11'
      
      - script: pip install -r requirements.txt
        displayName: 'Install dependencies'
      
      # Configure AWS credentials via service connection
      - task: AWSShellScript@1
        inputs:
          awsCredentials: 'AWS-Service-Connection'
          regionName: 'us-west-2'
          scriptType: 'inline'
          inlineScript: |
            pulumi stack select org/project/prod
            pulumi up --yes
        env:
          PULUMI_ACCESS_TOKEN: $(PULUMI_ACCESS_TOKEN)
```

## Reusable Template

```yaml
# templates/pulumi-deploy.yml
parameters:
  - name: stack
    type: string
  - name: environment
    type: string
  - name: workingDirectory
    type: string
    default: '.'

jobs:
  - deployment: Deploy
    environment: ${{ parameters.environment }}
    strategy:
      runOnce:
        deploy:
          steps:
            - checkout: self
            
            - task: UsePythonVersion@0
              inputs:
                versionSpec: '3.11'
            
            - script: |
                cd ${{ parameters.workingDirectory }}
                pip install -r requirements.txt
              displayName: 'Install dependencies'
            
            - task: Pulumi@1
              inputs:
                command: 'up'
                stack: ${{ parameters.stack }}
                args: '--yes'
                cwd: ${{ parameters.workingDirectory }}
              env:
                PULUMI_ACCESS_TOKEN: $(PULUMI_ACCESS_TOKEN)
```

Usage:
```yaml
# azure-pipelines.yml
stages:
  - stage: DeployProd
    jobs:
      - template: templates/pulumi-deploy.yml
        parameters:
          stack: 'org/project/prod'
          environment: 'production'
          workingDirectory: 'infrastructure'
```

## Variable Groups Setup

Create these variable groups in Azure DevOps:

**pulumi-secrets:**
- `PULUMI_ACCESS_TOKEN` (secret)

**aws-credentials** (if using AWS):
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY` (secret)
- `AWS_REGION`

**azure-credentials** (if using Azure):
- Use service connection instead

## Environment Protection Rules

1. Go to Pipelines → Environments
2. Create environments: `development`, `staging`, `production`
3. For `production`, add:
   - Approvals (required reviewers)
   - Branch filters (only main)
   - Deployment windows (business hours)
