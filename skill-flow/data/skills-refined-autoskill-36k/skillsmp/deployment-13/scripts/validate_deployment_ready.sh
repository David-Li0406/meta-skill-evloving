#!/bin/bash
# validate_deployment_ready.sh - Pre-deployment validation
#
# Validates configuration and infrastructure before deployment.
# Fails fast if prerequisites are missing.
#
# Usage:
#   ENV=dev ./validate_deployment_ready.sh
#   ENV=staging ./validate_deployment_ready.sh
#   ENV=production ./validate_deployment_ready.sh

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
error() {
    echo -e "${RED}❌ $1${NC}" >&2
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

info() {
    echo "ℹ️  $1"
}

# Check environment variable
if [ -z "$ENV" ]; then
    error "ENV variable not set"
    info "Usage: ENV=dev ./validate_deployment_ready.sh"
    exit 1
fi

if [[ ! "$ENV" =~ ^(dev|staging|production)$ ]]; then
    error "Invalid ENV: $ENV (must be dev, staging, or production)"
    exit 1
fi

success "Environment: $ENV"
echo ""

# ===================================================================
# Section 1: Doppler Configuration
# ===================================================================

echo "=== Section 1: Doppler Configuration ==="

# Check if Doppler CLI is installed
if ! command -v doppler &> /dev/null; then
    error "Doppler CLI not installed"
    info "Install: brew install dopplerhq/cli/doppler"
    exit 1
fi
success "Doppler CLI installed"

# Check if Doppler is configured for this project
if ! doppler projects get &> /dev/null; then
    error "Doppler not configured for this project"
    info "Run: doppler setup"
    exit 1
fi
success "Doppler configured"

# Validate Doppler project exists
PROJECT_NAME=$(doppler projects get --json | jq -r '.name')
if [ -z "$PROJECT_NAME" ]; then
    error "Doppler project not found"
    exit 1
fi
success "Doppler project: $PROJECT_NAME"

# Validate Doppler config exists for environment
if ! ENV=$ENV doppler configs get &> /dev/null; then
    error "Doppler config not found for environment: $ENV"
    info "Available configs:"
    doppler configs --json | jq -r '.[] | .name'
    exit 1
fi
success "Doppler config exists for $ENV"

echo ""

# ===================================================================
# Section 2: Required Environment Variables (Runtime Secrets)
# ===================================================================

echo "=== Section 2: Runtime Secrets (from Doppler) ==="

# List of required runtime secrets
REQUIRED_SECRETS=(
    "AURORA_HOST"
    "AURORA_USERNAME"
    "AURORA_PASSWORD"
    "AURORA_DATABASE"
    "OPENROUTER_API_KEY"
    "PDF_BUCKET_NAME"
)

MISSING_SECRETS=()

for SECRET in "${REQUIRED_SECRETS[@]}"; do
    VALUE=$(ENV=$ENV doppler secrets get $SECRET --plain 2>/dev/null || echo "")
    if [ -z "$VALUE" ]; then
        error "Missing secret: $SECRET"
        MISSING_SECRETS+=("$SECRET")
    else
        # Mask secret value (show first 4 chars only)
        MASKED="${VALUE:0:4}***"
        success "Secret $SECRET: $MASKED"
    fi
done

if [ ${#MISSING_SECRETS[@]} -gt 0 ]; then
    error "Missing ${#MISSING_SECRETS[@]} required secrets"
    info "Set missing secrets in Doppler:"
    for SECRET in "${MISSING_SECRETS[@]}"; do
        echo "  ENV=$ENV doppler secrets set $SECRET"
    done
    exit 1
fi

success "All ${#REQUIRED_SECRETS[@]} required secrets configured"
echo ""

# ===================================================================
# Section 3: AWS Resources
# ===================================================================

echo "=== Section 3: AWS Resources ==="

# Check AWS CLI installed
if ! command -v aws &> /dev/null; then
    error "AWS CLI not installed"
    info "Install: brew install awscli"
    exit 1
fi
success "AWS CLI installed"

# Check AWS credentials configured
if ! aws sts get-caller-identity &> /dev/null; then
    error "AWS credentials not configured"
    info "Run: aws configure"
    exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
USER_ARN=$(aws sts get-caller-identity --query 'Arn' --output text)
success "AWS credentials: $USER_ARN"

# Validate Lambda functions exist
info "Validating Lambda functions..."

LAMBDA_FUNCTIONS=(
    "dr-daily-report-worker-$ENV"
    "dr-daily-report-scheduler-$ENV"
)

for FUNC in "${LAMBDA_FUNCTIONS[@]}"; do
    if aws lambda get-function --function-name $FUNC &> /dev/null; then
        success "Lambda function exists: $FUNC"
    else
        error "Lambda function not found: $FUNC"
        info "Create with: cd terraform/environments/$ENV && terraform apply"
        exit 1
    fi
done

# Validate S3 buckets exist
info "Validating S3 buckets..."

S3_BUCKETS=(
    "dr-daily-report-data-$ENV"
    "dr-daily-report-pdf-reports-$ENV"
)

for BUCKET in "${S3_BUCKETS[@]}"; do
    if aws s3 ls s3://$BUCKET &> /dev/null; then
        success "S3 bucket exists: $BUCKET"
    else
        error "S3 bucket not found: $BUCKET"
        info "Create with: cd terraform/environments/$ENV && terraform apply"
        exit 1
    fi
done

# Validate DynamoDB tables exist
info "Validating DynamoDB tables..."

DYNAMODB_TABLES=(
    "dr-daily-report-telegram-jobs-$ENV"
    "dr-daily-report-telegram-cache-$ENV"
)

for TABLE in "${DYNAMODB_TABLES[@]}"; do
    if aws dynamodb describe-table --table-name $TABLE &> /dev/null; then
        success "DynamoDB table exists: $TABLE"
    else
        error "DynamoDB table not found: $TABLE"
        info "Create with: cd terraform/environments/$ENV && terraform apply"
        exit 1
    fi
done

# Validate Aurora cluster exists
info "Validating Aurora cluster..."

CLUSTER_ID="dr-daily-report-$ENV"
if aws rds describe-db-clusters --db-cluster-identifier $CLUSTER_ID &> /dev/null; then
    CLUSTER_STATUS=$(aws rds describe-db-clusters \
        --db-cluster-identifier $CLUSTER_ID \
        --query 'DBClusters[0].Status' --output text)

    if [ "$CLUSTER_STATUS" == "available" ]; then
        success "Aurora cluster available: $CLUSTER_ID"
    else
        warning "Aurora cluster status: $CLUSTER_STATUS (expected: available)"
    fi
else
    error "Aurora cluster not found: $CLUSTER_ID"
    info "Create with: cd terraform/environments/$ENV && terraform apply"
    exit 1
fi

echo ""

# ===================================================================
# Section 4: Python Dependencies
# ===================================================================

echo "=== Section 4: Python Dependencies ==="

# Check Python version
if ! command -v python3 &> /dev/null; then
    error "Python 3 not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
success "Python version: $PYTHON_VERSION"

# Check required Python packages (for local testing)
REQUIRED_PACKAGES=(
    "boto3"
    "pytest"
    "requests"
)

info "Checking Python packages..."

MISSING_PACKAGES=()

for PACKAGE in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $PACKAGE" &> /dev/null; then
        success "Package installed: $PACKAGE"
    else
        warning "Package not installed: $PACKAGE"
        MISSING_PACKAGES+=("$PACKAGE")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    warning "Missing ${#MISSING_PACKAGES[@]} Python packages (optional for deployment)"
    info "Install: pip install ${MISSING_PACKAGES[*]}"
fi

echo ""

# ===================================================================
# Section 5: Docker
# ===================================================================

echo "=== Section 5: Docker ==="

# Check Docker installed
if ! command -v docker &> /dev/null; then
    error "Docker not installed"
    info "Install: brew install --cask docker"
    exit 1
fi
success "Docker installed"

# Check Docker daemon running
if ! docker ps &> /dev/null; then
    error "Docker daemon not running"
    info "Start Docker Desktop"
    exit 1
fi
success "Docker daemon running"

# Check ECR access
info "Validating ECR access..."

ECR_REGISTRY="$ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com"
ECR_REPO="$ECR_REGISTRY/dr-daily-report-worker"

if aws ecr describe-repositories --repository-names dr-daily-report-worker &> /dev/null; then
    success "ECR repository accessible: dr-daily-report-worker"
else
    error "ECR repository not found: dr-daily-report-worker"
    info "Create with: aws ecr create-repository --repository-name dr-daily-report-worker"
    exit 1
fi

echo ""

# ===================================================================
# Section 6: GitHub CLI (for CI/CD monitoring)
# ===================================================================

echo "=== Section 6: GitHub CLI (optional) ==="

if command -v gh &> /dev/null; then
    success "GitHub CLI installed"

    if gh auth status &> /dev/null; then
        success "GitHub CLI authenticated"
    else
        warning "GitHub CLI not authenticated"
        info "Run: gh auth login"
    fi
else
    warning "GitHub CLI not installed (optional)"
    info "Install: brew install gh"
fi

echo ""

# ===================================================================
# Summary
# ===================================================================

echo "=========================================="
echo "✅ Deployment Validation Passed"
echo "=========================================="
echo ""
echo "Environment: $ENV"
echo "AWS Account: $ACCOUNT_ID"
echo "Doppler Project: $PROJECT_NAME"
echo ""
echo "Ready to deploy!"
echo ""
echo "Next steps:"
echo "  1. Run tests: pytest --tier=1"
echo "  2. Build image: docker build -t worker:latest ."
echo "  3. Deploy: git push origin $ENV"
echo ""
