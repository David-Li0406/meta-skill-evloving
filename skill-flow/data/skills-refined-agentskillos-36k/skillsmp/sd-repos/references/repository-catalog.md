# SD/SIC Repository Catalog

## Terminology

**SD = Sustainability Dashboard = SIC = Sustainability Insight Center**

These terms are used interchangeably to refer to the same product and codebase.

**ADS = Application Deployment Service**

ADS refers to applications tagged with the `ads-app` GitHub topic. This does NOT stand for "Anomaly Detection Service" or "Application Delivery Service".

## Repository Locations

### Local Repositories
All SD/SIC repositories are cloned in: `/Users/kevin/git/glcp/sd/`

### Remote Repositories
All SD/SIC repositories are in the `glcp` GitHub organization: `https://github.com/glcp/`

## Complete Repository List

### ADS Applications (14 total)

These repositories are tagged with both `sustainability-dashboard` and `ads-app` GitHub topics:

1. **sd-ad-inference-workflow** - Anomaly detection inference workflow
2. **sd-ad-model** - Anomaly detection model
3. **sd-ai-agent** - AI agent service
4. **sd-ai-worker** - AI worker service
5. **sd-auth-service** - Authentication service
6. **sd-backend-template** - Backend service template
7. **sd-ccs-event-endpoint** - CCS event endpoint
8. **sd-collector-service** - Data collector service
9. **sd-data-service** - Data service
10. **sd-frontend** - Frontend application (TypeScript)
11. **sd-ml-forecasting** - Machine learning forecasting
12. **sd-query-service** - Query service
13. **sd-test-data-injector** - Test data injector
14. **sd-test-harness** - Test harness

### Non-ADS Repositories

These are infrastructure and operations repositories (tagged with `sustainability-dashboard` but NOT `ads-app`):

1. **sd-deploy-repo** - Infrastructure and deployment coordination
2. **sd-ops** - Operations and infrastructure
3. **sd-ml-models** - ML model storage
4. **sd-terraform-alerts** - Terraform alerting configuration
5. **sd-ops-frontend** - Operations frontend (TypeScript)

## Repository Categories

### Backend Services (Kotlin)
11 microservices including:
- sd-*-service repos
- sd-ai-* repos
- sd-test-* repos

### Frontend Applications (TypeScript)
- sd-frontend
- sd-ops-frontend

### ML/Data Science (Python)
- sd-ad-inference-workflow
- sd-ad-model
- sd-ml-forecasting
- sd-ml-models

### Infrastructure (HCL/Shell)
- sd-deploy-repo
- sd-ops
- sd-terraform-alerts

## Management Scripts

Located in `/Users/kevin/git/glcp/sd/`:
- `create_*_prs.sh` - PR creation automation
- `update_*.sh` - Repository update scripts
- `check_*.sh` - Verification scripts
- `verify_*.sh` - Validation scripts
- `merge_all_prs.sh` - PR merge automation

## Kubernetes & Deployment Information

For comprehensive deployment and cluster access information, see:
`/Users/kevin/git/glcp/sd/sd-ops/copilot/comprehensive-cluster-guide.md`

This includes:
- Kubernetes cluster access (staging, production)
- Deployment procedures
- Cluster configuration details
- Troubleshooting guides
