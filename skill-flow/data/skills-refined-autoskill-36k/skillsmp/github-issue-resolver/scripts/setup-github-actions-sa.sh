#!/bin/bash
#
# Setup GitHub Actions Service Account for OpenShift Cluster Health MCP
#
# This script creates a service account with read-only cluster access
# for GitHub Actions integration tests.
#
# Usage:
#   ./scripts/setup-github-actions-sa.sh
#

set -euo pipefail

# Configuration
SA_NAME="github-actions-sa"
SA_NAMESPACE="${SA_NAMESPACE:-default}"
TOKEN_DURATION="8760h"  # 1 year

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}GitHub Actions Service Account Setup${NC}"
echo -e "${GREEN}==================================================${NC}"
echo ""

# Check if oc is installed
if ! command -v oc &> /dev/null; then
    echo -e "${RED}Error: 'oc' command not found${NC}"
    echo "Please install the OpenShift CLI: https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html"
    exit 1
fi

# Check if logged in to OpenShift
if ! oc whoami &> /dev/null; then
    echo -e "${RED}Error: Not logged in to OpenShift${NC}"
    echo "Please login first: oc login --token=<token> --server=<server>"
    exit 1
fi

CURRENT_USER=$(oc whoami)
CLUSTER_URL=$(oc whoami --show-server)

echo -e "Current user: ${GREEN}${CURRENT_USER}${NC}"
echo -e "Cluster: ${GREEN}${CLUSTER_URL}${NC}"
echo -e "Service account: ${GREEN}${SA_NAME}${NC}"
echo -e "Namespace: ${GREEN}${SA_NAMESPACE}${NC}"
echo ""

# Ask for confirmation
read -p "Create service account with read-only cluster access? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo -e "${YELLOW}Step 1: Creating service account...${NC}"

# Create namespace if it doesn't exist
if ! oc get namespace "$SA_NAMESPACE" &> /dev/null; then
    echo "Creating namespace: $SA_NAMESPACE"
    oc create namespace "$SA_NAMESPACE"
fi

# Create service account
if oc get sa "$SA_NAME" -n "$SA_NAMESPACE" &> /dev/null; then
    echo -e "${YELLOW}Service account '$SA_NAME' already exists. Recreating...${NC}"
    oc delete sa "$SA_NAME" -n "$SA_NAMESPACE"
fi

oc create sa "$SA_NAME" -n "$SA_NAMESPACE"
echo -e "${GREEN}✓ Service account created${NC}"

echo ""
echo -e "${YELLOW}Step 2: Creating ClusterRole with read-only permissions...${NC}"

cat <<EOF | oc apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: github-actions-readonly
rules:
  # Cluster health monitoring
  - apiGroups: [""]
    resources: ["nodes", "pods", "namespaces", "events", "persistentvolumes", "persistentvolumeclaims"]
    verbs: ["get", "list", "watch"]

  # Deployments and workloads
  - apiGroups: ["apps"]
    resources: ["deployments", "statefulsets", "daemonsets", "replicasets"]
    verbs: ["get", "list", "watch"]

  # KServe InferenceServices
  - apiGroups: ["serving.kserve.io"]
    resources: ["inferenceservices", "inferenceservices/status"]
    verbs: ["get", "list", "watch"]

  # OpenShift-specific resources
  - apiGroups: ["route.openshift.io"]
    resources: ["routes"]
    verbs: ["get", "list", "watch"]

  - apiGroups: ["project.openshift.io"]
    resources: ["projects"]
    verbs: ["get", "list", "watch"]
EOF

echo -e "${GREEN}✓ ClusterRole created${NC}"

echo ""
echo -e "${YELLOW}Step 3: Binding ClusterRole to service account...${NC}"

# Create ClusterRoleBinding
if oc get clusterrolebinding github-actions-readonly-binding &> /dev/null; then
    oc delete clusterrolebinding github-actions-readonly-binding
fi

oc create clusterrolebinding github-actions-readonly-binding \
    --clusterrole=github-actions-readonly \
    --serviceaccount="${SA_NAMESPACE}:${SA_NAME}"

echo -e "${GREEN}✓ ClusterRoleBinding created${NC}"

echo ""
echo -e "${YELLOW}Step 4: Generating long-lived token...${NC}"

# Generate token
TOKEN=$(oc create token "$SA_NAME" -n "$SA_NAMESPACE" --duration="$TOKEN_DURATION" 2>&1)

if [ $? -ne 0 ]; then
    echo -e "${RED}Error generating token: $TOKEN${NC}"
    echo ""
    echo "Trying alternative method (create Secret)..."

    # Create token secret (older OpenShift versions)
    cat <<EOF | oc apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: ${SA_NAME}-token
  namespace: ${SA_NAMESPACE}
  annotations:
    kubernetes.io/service-account.name: ${SA_NAME}
type: kubernetes.io/service-account-token
EOF

    # Wait for token to be populated
    echo "Waiting for token to be generated..."
    sleep 3

    TOKEN=$(oc get secret "${SA_NAME}-token" -n "$SA_NAMESPACE" -o jsonpath='{.data.token}' | base64 -d)
fi

if [ -z "$TOKEN" ]; then
    echo -e "${RED}Error: Failed to generate token${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Token generated${NC}"

echo ""
echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}==================================================${NC}"
echo ""
echo -e "${YELLOW}Add these secrets to your GitHub repository:${NC}"
echo ""
echo -e "${GREEN}OPENSHIFT_SERVER:${NC}"
echo "$CLUSTER_URL"
echo ""
echo -e "${GREEN}OPENSHIFT_TOKEN:${NC}"
echo "$TOKEN"
echo ""
echo -e "${YELLOW}GitHub Repository Setup:${NC}"
echo "1. Go to: https://github.com/tosin2013/openshift-cluster-health-mcp/settings/secrets/actions"
echo "2. Click 'New repository secret'"
echo "3. Create secret 'OPENSHIFT_SERVER' with value: $CLUSTER_URL"
echo "4. Create secret 'OPENSHIFT_TOKEN' with the token above"
echo ""
echo -e "${YELLOW}Token Details:${NC}"
echo "- Duration: $TOKEN_DURATION (1 year)"
echo "- Permissions: Read-only cluster access"
echo "- Namespace: $SA_NAMESPACE"
echo ""
echo -e "${YELLOW}Test the service account:${NC}"
echo "  oc auth can-i get pods --as=system:serviceaccount:${SA_NAMESPACE}:${SA_NAME}"
echo "  oc auth can-i list nodes --as=system:serviceaccount:${SA_NAMESPACE}:${SA_NAME}"
echo "  oc auth can-i delete pods --as=system:serviceaccount:${SA_NAMESPACE}:${SA_NAME}  # Should be 'no'"
echo ""
echo -e "${RED}⚠️  Security Reminder:${NC}"
echo "- This token provides cluster access for 1 year"
echo "- Store it securely in GitHub Secrets only"
echo "- Rotate the token before expiration"
echo "- Monitor service account activity in audit logs"
echo ""
