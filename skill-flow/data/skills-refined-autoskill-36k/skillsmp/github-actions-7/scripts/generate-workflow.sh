#!/usr/bin/env bash
#
# generate-workflow.sh - Generate custom workflow based on project config
# Usage: bash generate-workflow.sh [options]
#

set -e

# Default values
WORKFLOW_TYPE=""
PROJECT_NAME="${PROJECT_NAME:-my-project}"
REGISTRY="${REGISTRY:-ghcr.io}"
DOCKER_IMAGE="${DOCKER_IMAGE:-}"
LANGUAGE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --type|-t)
            WORKFLOW_TYPE="$2"
            shift 2
            ;;
        --project-name|-p)
            PROJECT_NAME="$2"
            shift 2
            ;;
        --registry|-r)
            REGISTRY="$2"
            shift 2
            ;;
        --image|-i)
            DOCKER_IMAGE="$2"
            shift 2
            ;;
        --language|-l)
            LANGUAGE="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: bash generate-workflow.sh [options]"
            echo ""
            echo "Options:"
            echo "  --type, -t <type>          Workflow type (nodejs, python, go, docker, k8s)"
            echo "  --project-name, -p <name>  Project name (default: my-project)"
            echo "  --registry, -r <registry>  Container registry (default: ghcr.io)"
            echo "  --image, -i <image>        Docker image name"
            echo "  --language, -l <lang>      Programming language"
            echo "  --help, -h                 Show this help message"
            echo ""
            echo "Examples:"
            echo "  bash generate-workflow.sh --type nodejs"
            echo "  bash generate-workflow.sh --type docker --image myorg/myapp"
            echo "  bash generate-workflow.sh --type k8s --project-name my-app"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Auto-detect if not specified
if [ -z "$WORKFLOW_TYPE" ] && [ -z "$LANGUAGE" ]; then
    if [ -f "package.json" ]; then
        WORKFLOW_TYPE="nodejs"
        LANGUAGE="javascript"
    elif [ -f "requirements.txt" ]; then
        WORKFLOW_TYPE="python"
        LANGUAGE="python"
    elif [ -f "go.mod" ]; then
        WORKFLOW_TYPE="go"
        LANGUAGE="go"
    elif [ -f "Dockerfile" ]; then
        WORKFLOW_TYPE="docker"
    elif [ -d "k8s" ]; then
        WORKFLOW_TYPE="k8s"
    else
        echo "❌ Unable to detect project type. Please specify --type"
        exit 1
    fi
fi

# Validate workflow type
VALID_TYPES=("nodejs" "python" "go" "docker" "k8s")
if [[ ! " ${VALID_TYPES[@]} " =~ " ${WORKFLOW_TYPE} " ]]; then
    echo "❌ Invalid workflow type: $WORKFLOW_TYPE"
    echo "Valid types: ${VALID_TYPES[*]}"
    exit 1
fi

# Generate workflow
generate_workflow() {
    local type=$1
    local output_file=".github/workflows/generated-${type}.yml"

    echo "📝 Generating workflow: $output_file"

    # Create .github/workflows directory
    mkdir -p .github/workflows

    # Generate based on type
    case $type in
        nodejs)
            cat > "$output_file" <<EOF
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
EOF
            ;;
        python)
            cat > "$output_file" <<EOF
name: Python CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: \${{ matrix.python-version }}
          cache: 'pip'
      - run: pip install -r requirements.txt
      - run: pytest
EOF
            ;;
        docker)
            cat > "$output_file" <<EOF
name: Docker Build and Push

on:
  push:
    branches: [main]

env:
  REGISTRY: $REGISTRY
  IMAGE_NAME: $DOCKER_IMAGE

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: \${{ env.REGISTRY }}
          username: \${{ github.actor }}
          password: \${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: \${{ env.REGISTRY }}/\${{ env.IMAGE_NAME }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
EOF
            ;;
        k8s)
            cat > "$output_file" <<EOF
name: Kubernetes Deploy

on:
  push:
    branches: [main]

env:
  REGISTRY: $REGISTRY
  IMAGE_NAME: $DOCKER_IMAGE

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: azure/k8s-set-context@v4
        with:
          method: kubeconfig
          kubeconfig: \${{ secrets.KUBE_CONFIG }}
      - run: |
          kubectl set image deployment/$PROJECT_NAME \\
            $PROJECT_NAME=\${{ env.REGISTRY }}/\${{ env.IMAGE_NAME }}:latest
          kubectl rollout status deployment/$PROJECT_NAME
EOF
            ;;
        *)
            echo "❌ Unsupported workflow type: $type"
            exit 1
            ;;
    esac

    echo "✅ Workflow generated: $output_file"
    echo ""
    echo "Next steps:"
    echo "1. Review and customize the workflow"
    echo "2. Commit to your repository"
    echo "3. Push to trigger the workflow"
}

# Run generation
generate_workflow "$WORKFLOW_TYPE"
