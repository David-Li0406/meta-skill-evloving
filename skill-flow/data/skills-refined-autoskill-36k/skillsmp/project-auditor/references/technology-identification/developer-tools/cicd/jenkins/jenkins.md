# Jenkins

**Category**: developer-tools/cicd
**Description**: Open source automation server for CI/CD
**Homepage**: https://www.jenkins.io

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
- `jenkins` - Jenkins API client for Node.js
- `jenkins-api` - Jenkins API wrapper

#### PYPI
- `python-jenkins` - Python wrapper for Jenkins REST API
- `jenkinsapi` - Python API to access Jenkins CI
- `jenkins-job-builder` - Jenkins Job Builder

#### MAVEN
- `org.jenkins-ci.main:jenkins-core` - Jenkins core library
- `org.jenkins-ci.plugins:*` - Jenkins plugins
- `io.jenkins.plugins:*` - Jenkins plugins (newer)

#### GO
- `github.com/bndr/gojenkins` - Jenkins Go client

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### Configuration Files
*Known configuration files that indicate Jenkins usage*

- `Jenkinsfile` - Pipeline definition file (strong indicator)
- `jenkins.yml` - Jenkins configuration as code
- `jenkins.yaml` - Jenkins configuration as code
- `jenkins-jobs.yml` - Jenkins Job Builder config
- `jenkins-jobs.yaml` - Jenkins Job Builder config
- `.jenkins/` - Jenkins configuration directory

### Import Patterns

#### Python
Extensions: `.py`

**Pattern**: `^import\s+jenkins`
- Jenkins Python import
- Example: `import jenkins`

**Pattern**: `^from\s+jenkins\s+import`
- Jenkins Python from import
- Example: `from jenkins import Jenkins`

**Pattern**: `^from\s+jenkinsapi`
- JenkinsAPI import
- Example: `from jenkinsapi.jenkins import Jenkins`

#### Groovy
Extensions: `.groovy`

**Pattern**: `import\s+jenkins\.`
- Jenkins Groovy import
- Example: `import jenkins.model.Jenkins`

**Pattern**: `import\s+hudson\.`
- Hudson (Jenkins predecessor) import
- Example: `import hudson.model.Build`

### Code Patterns
*Jenkinsfile (Groovy DSL) patterns*

**Pattern**: `^pipeline\s*\{`
- Declarative pipeline start
- Example: `pipeline {`

**Pattern**: `^\s*agent\s+(any|none|\{)`
- Agent specification
- Example: `agent any`

**Pattern**: `^\s*stages\s*\{`
- Stages block
- Example: `stages {`

**Pattern**: `^\s*stage\s*\(['"]\w+['"]\)\s*\{`
- Stage definition
- Example: `stage('Build') {`

**Pattern**: `^\s*steps\s*\{`
- Steps block
- Example: `steps {`

**Pattern**: `^\s*post\s*\{`
- Post actions block
- Example: `post {`

**Pattern**: `^\s*environment\s*\{`
- Environment block
- Example: `environment {`

**Pattern**: `^\s*parameters\s*\{`
- Parameters block
- Example: `parameters {`

**Pattern**: `^\s*triggers\s*\{`
- Triggers block
- Example: `triggers {`

**Pattern**: `^\s*options\s*\{`
- Options block
- Example: `options {`

**Pattern**: `^\s*tools\s*\{`
- Tools block
- Example: `tools {`

**Pattern**: `^\s*when\s*\{`
- Conditional execution
- Example: `when {`

**Pattern**: `^\s*parallel\s*\{`
- Parallel execution
- Example: `parallel {`

**Pattern**: `^\s*input\s*\{`
- Input step
- Example: `input {`

**Pattern**: `^\s*sh\s+['""]`
- Shell command step
- Example: `sh 'npm install'`

**Pattern**: `^\s*bat\s+['""]`
- Batch command step (Windows)
- Example: `bat 'npm install'`

**Pattern**: `^\s*checkout\s+scm`
- Source checkout
- Example: `checkout scm`

**Pattern**: `^\s*withCredentials\s*\(`
- Credentials binding
- Example: `withCredentials([string(...)]) {`

**Pattern**: `^\s*node\s*\(`
- Scripted pipeline node
- Example: `node('linux') {`

---

## Environment Variables

- `JENKINS_URL` - Jenkins server URL
- `JENKINS_HOME` - Jenkins home directory
- `BUILD_NUMBER` - Build number
- `BUILD_ID` - Build ID
- `BUILD_URL` - URL to build
- `JOB_NAME` - Job name
- `JOB_URL` - Job URL
- `WORKSPACE` - Workspace path
- `NODE_NAME` - Node name
- `NODE_LABELS` - Node labels
- `EXECUTOR_NUMBER` - Executor number
- `GIT_COMMIT` - Git commit SHA
- `GIT_BRANCH` - Git branch
- `GIT_URL` - Git repository URL
- `CHANGE_ID` - Pull request ID
- `CHANGE_URL` - Pull request URL
- `CHANGE_TITLE` - Pull request title
- `CHANGE_AUTHOR` - Pull request author
- `CHANGE_TARGET` - Target branch for PR
- `BRANCH_NAME` - Branch name
- `TAG_NAME` - Tag name (if building a tag)

## Detection Notes

- `Jenkinsfile` is the strongest indicator of Jenkins usage
- Jenkins uses Groovy DSL for pipeline definitions
- Declarative pipelines use `pipeline { }` syntax
- Scripted pipelines use `node { }` syntax
- Jenkins supports both self-hosted and CloudBees managed
- Many Jenkins-specific steps like `withCredentials`, `sh`, `bat`
- `hudson.*` packages indicate older Jenkins/Hudson code
