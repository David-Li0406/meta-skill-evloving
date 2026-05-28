---
id: jenkins-pipelines
name: "Jenkins Pipelines"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Jenkins Pipelines

## Overview

Jenkins is an open-source automation server for building CI/CD pipelines. It uses Groovy-based Declarative or Scripted Pipeline syntax defined in Jenkinsfiles, supporting complex workflows, distributed builds, and extensive plugin ecosystem.

## When to Use

- Enterprise environments with existing Jenkins infrastructure
- Complex build requirements needing extensive customization
- On-premises deployments with strict security requirements
- Multi-branch projects with complex branching strategies
- Pipelines requiring custom plugins or integrations

## Key Concepts

| Concept | Description |
|---------|-------------|
| Pipeline | Automated workflow defined in Jenkinsfile |
| Stage | Logical division of pipeline (Build, Test, Deploy) |
| Step | Single task within a stage |
| Agent | Executor running pipeline (controller, node, docker) |
| Declarative | Structured pipeline syntax with predefined sections |
| Scripted | Flexible Groovy-based pipeline syntax |
| Shared Library | Reusable pipeline code |
| Blue Ocean | Modern pipeline visualization UI |

### Pipeline Types Comparison

| Feature | Declarative | Scripted |
|---------|-------------|----------|
| Syntax | Structured, predefined | Flexible Groovy |
| Error handling | Built-in post sections | try-catch blocks |
| Readability | Easier for beginners | More complex |
| Flexibility | Limited | Full Groovy power |
| Validation | Syntax validation | Runtime only |

## Implementation

### Declarative Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: node
                    image: node:20-alpine
                    command:
                    - cat
                    tty: true
                  - name: docker
                    image: docker:24-dind
                    securityContext:
                      privileged: true
                    volumeMounts:
                    - name: docker-socket
                      mountPath: /var/run/docker.sock
                  volumes:
                  - name: docker-socket
                    emptyDir: {}
            '''
        }
    }

    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        APP_NAME = 'myapp'
        VERSION = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
        DOCKER_CREDENTIALS = credentials('docker-registry')
        KUBECONFIG = credentials('kubeconfig-staging')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        ansiColor('xterm')
    }

    triggers {
        pollSCM('H/5 * * * *')
        cron('H 2 * * *') // Nightly build
    }

    parameters {
        choice(
            name: 'DEPLOY_ENV',
            choices: ['staging', 'production'],
            description: 'Environment to deploy to'
        )
        booleanParam(
            name: 'SKIP_TESTS',
            defaultValue: false,
            description: 'Skip test stage'
        )
        string(
            name: 'CUSTOM_TAG',
            defaultValue: '',
            description: 'Custom Docker tag (optional)'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_MSG = sh(
                        script: 'git log -1 --pretty=%B',
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                container('node') {
                    sh 'npm ci'
                }
            }
        }

        stage('Lint') {
            steps {
                container('node') {
                    sh 'npm run lint'
                }
            }
        }

        stage('Test') {
            when {
                not {
                    expression { params.SKIP_TESTS }
                }
            }
            parallel {
                stage('Unit Tests') {
                    steps {
                        container('node') {
                            sh 'npm run test:unit -- --coverage'
                        }
                    }
                    post {
                        always {
                            junit 'junit.xml'
                            publishHTML(target: [
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'coverage/lcov-report',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }
                    }
                }
                stage('Integration Tests') {
                    steps {
                        container('node') {
                            sh 'npm run test:integration'
                        }
                    }
                }
            }
        }

        stage('Build') {
            steps {
                container('node') {
                    sh 'npm run build'
                }
            }
        }

        stage('Security Scan') {
            parallel {
                stage('SAST') {
                    steps {
                        container('node') {
                            sh 'npm audit --audit-level=high'
                        }
                    }
                }
                stage('Container Scan') {
                    steps {
                        container('docker') {
                            sh '''
                                docker run --rm \
                                    -v /var/run/docker.sock:/var/run/docker.sock \
                                    aquasec/trivy:latest image \
                                    --severity HIGH,CRITICAL \
                                    --exit-code 1 \
                                    ${DOCKER_REGISTRY}/${APP_NAME}:${VERSION}
                            '''
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    script {
                        def tag = params.CUSTOM_TAG ?: env.VERSION
                        sh """
                            docker login -u ${DOCKER_CREDENTIALS_USR} -p ${DOCKER_CREDENTIALS_PSW} ${DOCKER_REGISTRY}
                            docker build -t ${DOCKER_REGISTRY}/${APP_NAME}:${tag} .
                            docker push ${DOCKER_REGISTRY}/${APP_NAME}:${tag}
                        """
                        env.IMAGE_TAG = tag
                    }
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                anyOf {
                    branch 'main'
                    expression { params.DEPLOY_ENV == 'staging' }
                }
            }
            steps {
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig-staging', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl set image deployment/${APP_NAME} \
                                ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${IMAGE_TAG} \
                                -n staging
                            kubectl rollout status deployment/${APP_NAME} -n staging --timeout=5m
                        """
                    }
                }
            }
        }

        stage('Deploy to Production') {
            when {
                allOf {
                    branch 'main'
                    expression { params.DEPLOY_ENV == 'production' }
                }
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
                submitter "admin,deployers"
                parameters {
                    string(name: 'CONFIRM', defaultValue: '', description: 'Type "deploy" to confirm')
                }
            }
            steps {
                script {
                    if (CONFIRM != 'deploy') {
                        error('Deployment not confirmed')
                    }
                }
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig-prod', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl set image deployment/${APP_NAME} \
                                ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${IMAGE_TAG} \
                                -n production
                            kubectl rollout status deployment/${APP_NAME} -n production --timeout=10m
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            slackSend(
                color: 'good',
                message: "Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            )
            emailext(
                subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    Build ${env.BUILD_NUMBER} failed.
                    Commit: ${env.GIT_COMMIT}
                    Message: ${env.GIT_COMMIT_MSG}
                    Check console output at ${env.BUILD_URL}
                """,
                recipientProviders: [culprits(), requestor()]
            )
        }
        unstable {
            slackSend(
                color: 'warning',
                message: "Build Unstable: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}
```

### Shared Library Structure

```
vars/
├── buildApp.groovy          # Global variables/functions
├── deployToK8s.groovy
├── notifySlack.groovy
└── runTests.groovy
src/
└── com/
    └── example/
        ├── Docker.groovy    # Classes
        └── Kubernetes.groovy
resources/
└── templates/
    └── deployment.yaml      # Resource files
```

### Shared Library - vars/buildApp.groovy

```groovy
// vars/buildApp.groovy
def call(Map config = [:]) {
    def appName = config.appName ?: error('appName is required')
    def registry = config.registry ?: 'registry.example.com'
    def dockerfile = config.dockerfile ?: 'Dockerfile'
    def buildArgs = config.buildArgs ?: [:]

    def buildArgsString = buildArgs.collect { k, v -> "--build-arg ${k}=${v}" }.join(' ')

    pipeline {
        agent any

        stages {
            stage('Build') {
                steps {
                    script {
                        docker.withRegistry("https://${registry}", 'docker-credentials') {
                            def image = docker.build(
                                "${registry}/${appName}:${env.BUILD_NUMBER}",
                                "-f ${dockerfile} ${buildArgsString} ."
                            )
                            image.push()
                            image.push('latest')
                        }
                    }
                }
            }
        }
    }
}
```

### Shared Library - vars/deployToK8s.groovy

```groovy
// vars/deployToK8s.groovy
def call(Map config = [:]) {
    def namespace = config.namespace ?: error('namespace is required')
    def deployment = config.deployment ?: error('deployment is required')
    def image = config.image ?: error('image is required')
    def kubeconfig = config.kubeconfig ?: 'kubeconfig'
    def timeout = config.timeout ?: '5m'

    withCredentials([file(credentialsId: kubeconfig, variable: 'KUBECONFIG')]) {
        sh """
            kubectl set image deployment/${deployment} \
                ${deployment}=${image} \
                -n ${namespace}
            kubectl rollout status deployment/${deployment} \
                -n ${namespace} \
                --timeout=${timeout}
        """
    }
}
```

### Shared Library - src/com/example/Docker.groovy

```groovy
// src/com/example/Docker.groovy
package com.example

class Docker implements Serializable {
    def steps

    Docker(steps) {
        this.steps = steps
    }

    def build(String imageName, String dockerfile = 'Dockerfile', Map buildArgs = [:]) {
        def buildArgsString = buildArgs.collect { k, v -> "--build-arg ${k}=${v}" }.join(' ')

        steps.sh """
            docker build \
                -t ${imageName} \
                -f ${dockerfile} \
                ${buildArgsString} \
                .
        """

        return imageName
    }

    def push(String imageName, String registry, String credentialsId) {
        steps.withCredentials([
            steps.usernamePassword(
                credentialsId: credentialsId,
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASS'
            )
        ]) {
            steps.sh """
                echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin ${registry}
                docker push ${imageName}
            """
        }
    }

    def scan(String imageName, String severity = 'HIGH,CRITICAL') {
        def result = steps.sh(
            script: """
                docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    aquasec/trivy:latest image \
                    --severity ${severity} \
                    --exit-code 1 \
                    ${imageName}
            """,
            returnStatus: true
        )

        if (result != 0) {
            steps.error("Security vulnerabilities found in ${imageName}")
        }
    }
}
```

### Using Shared Library

```groovy
// Jenkinsfile using shared library
@Library('my-shared-library@main') _

import com.example.Docker

pipeline {
    agent any

    stages {
        stage('Build and Deploy') {
            steps {
                script {
                    def docker = new Docker(this)

                    def imageName = docker.build(
                        'registry.example.com/myapp:latest',
                        'Dockerfile',
                        [VERSION: env.BUILD_NUMBER]
                    )

                    docker.scan(imageName)

                    docker.push(imageName, 'registry.example.com', 'docker-creds')

                    deployToK8s(
                        namespace: 'staging',
                        deployment: 'myapp',
                        image: imageName
                    )
                }
            }
        }
    }
}
```

### Multibranch Pipeline

```groovy
// Jenkinsfile with branch-specific behavior
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }

        stage('Deploy Feature') {
            when {
                branch 'feature/*'
            }
            steps {
                echo "Deploying feature branch ${env.BRANCH_NAME}"
                // Deploy to feature environment
            }
        }

        stage('Deploy Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo "Deploying to staging"
                // Deploy to staging
            }
        }

        stage('Deploy Production') {
            when {
                branch 'main'
                beforeInput true
            }
            input {
                message "Deploy to production?"
                ok "Yes, deploy"
            }
            steps {
                echo "Deploying to production"
                // Deploy to production
            }
        }
    }
}
```

### Scripted Pipeline (Complex Logic)

```groovy
// Jenkinsfile - Scripted Pipeline
node('docker') {
    def services = ['api', 'web', 'worker']
    def parallelStages = [:]

    try {
        stage('Checkout') {
            checkout scm
        }

        stage('Detect Changes') {
            def changedFiles = sh(
                script: "git diff --name-only HEAD~1",
                returnStdout: true
            ).trim().split('\n')

            services = services.findAll { service ->
                changedFiles.any { it.startsWith("services/${service}/") }
            }

            if (services.isEmpty()) {
                currentBuild.result = 'SUCCESS'
                return
            }

            echo "Building services: ${services.join(', ')}"
        }

        stage('Build Services') {
            services.each { service ->
                parallelStages["Build ${service}"] = {
                    node('docker') {
                        checkout scm
                        dir("services/${service}") {
                            sh 'docker build -t ${service}:${BUILD_NUMBER} .'
                        }
                    }
                }
            }
            parallel parallelStages
        }

        stage('Test Services') {
            parallelStages = [:]
            services.each { service ->
                parallelStages["Test ${service}"] = {
                    node('docker') {
                        checkout scm
                        dir("services/${service}") {
                            sh 'npm test'
                        }
                    }
                }
            }
            parallel parallelStages
        }

        stage('Deploy') {
            services.each { service ->
                deployService(service, env.BUILD_NUMBER)
            }
        }

    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        slackSend(color: 'danger', message: "Build failed: ${e.message}")
        throw e

    } finally {
        cleanWs()
    }
}

def deployService(String service, String version) {
    timeout(time: 5, unit: 'MINUTES') {
        sh """
            kubectl set image deployment/${service} ${service}=${service}:${version}
            kubectl rollout status deployment/${service} --timeout=5m
        """
    }
}
```

## Best Practices

1. **Use Declarative Pipeline** - Prefer declarative syntax for readability and validation
2. **Implement Shared Libraries** - Centralize common pipeline code
3. **Use Kubernetes agents** - Dynamic, isolated build environments
4. **Parallelize stages** - Reduce build time with parallel execution
5. **Secure credentials** - Use Jenkins Credentials plugin, never hardcode
6. **Set timeouts** - Prevent stuck builds with stage/pipeline timeouts
7. **Clean workspace** - Always clean workspace in post section
8. **Use Blue Ocean** - Modern UI for better pipeline visualization
9. **Version Jenkinsfiles** - Store in source control with application
10. **Implement proper post sections** - Handle success, failure, always conditions

## Common Pitfalls

1. **Scripted for simple pipelines** - Declarative is simpler and validates syntax. Use scripted only when needed.

2. **No timeout limits** - Builds can hang indefinitely. Always set timeouts.

3. **Hardcoded credentials** - Security risk. Use Jenkins Credentials plugin.

4. **Missing post cleanup** - Resources leak without cleanup. Use `cleanWs()` in post always.

5. **Sequential when parallel is possible** - Wasted time. Use parallel stages for independent jobs.

6. **Ignoring agent scope** - Wrong agent for job. Specify agent per stage when needed.

## References

- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
- [Blue Ocean](https://www.jenkins.io/doc/book/blueocean/)
