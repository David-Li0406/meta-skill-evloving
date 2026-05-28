---
name: cost-firebase
description: Estimate Firebase costs for any project using live pricing data. Use when user asks about Firebase pricing, Firestore costs, or Google BaaS costs.
---

# Firebase Cost Evaluator

Estimate costs for Firebase-based projects using current pricing data.

## Before Answering Firebase Cost Questions

**IMPORTANT**: Always verify tool availability before providing cost estimates.

### Step 1: Check Available Tools

Check if the following tools are available:

**Firebase CLI** (preferred):
- `firebase` CLI for project information
- `firebase projects:list` - List projects
- `firebase use` - Select project

**GCP Console / gcloud** (for billing):
- Firebase uses GCP billing
- `gcloud billing` commands work for Firebase

**Firebase Management API**:
- REST API for project information

### Step 2: If Tools Are Unavailable

If Firebase CLI is not accessible, help the user set them up:

**Option A: Firebase CLI**
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# List projects
firebase projects:list
```

**Option B: gcloud CLI (for billing)**
```bash
# Firebase billing is via GCP
gcloud auth login

# Link to Firebase project's GCP project
gcloud config set project YOUR_GCP_PROJECT_ID

# View billing
gcloud billing accounts list
```

**Option C: Firebase Management API**
```bash
# Get access token
# Use Firebase Admin SDK or Google OAuth

# List projects
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://firebase.googleapis.com/v1beta1/projects"
```

Ask the user which option fits their environment before proceeding.

### Step 3: Fallback to Web Search

If no tools are available and user cannot install them, use web search to fetch current pricing from:
- https://firebase.google.com/pricing
- https://cloud.google.com/firestore/pricing
- https://cloud.google.com/functions/pricing

## How to Get Live Pricing

### Using Firebase CLI

```bash
# List all projects
firebase projects:list

# Get project details
firebase use YOUR_PROJECT_ID

# Open Firebase Console (for usage stats)
firebase open
```

### Using GCP Billing (Firebase uses GCP)

```bash
# Firebase billing is through GCP
# Get cost breakdown
gcloud billing accounts list

# Export billing data
bq query --use_legacy_sql=false '
  SELECT service.description, SUM(cost) as total_cost
  FROM `PROJECT.dataset.gcp_billing_export_v1_*`
  WHERE service.description LIKE "%Firebase%"
     OR service.description LIKE "%Firestore%"
     OR service.description LIKE "%Cloud Functions%"
  GROUP BY service.description'
```

### Using Firebase Console API

```bash
# Get project usage (requires Firebase Admin)
# https://console.firebase.google.com/project/PROJECT_ID/usage

# Or use the REST API
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://firebasehosting.googleapis.com/v1beta1/projects/PROJECT_ID/sites"
```

### Using GCP Cloud Billing API

```bash
# Get SKUs for Firebase services
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://cloudbilling.googleapis.com/v1/services"

# Firestore service ID: example lookup
# Cloud Functions: same as GCP pricing
```

## Standalone Usage

Can be invoked directly for cost estimation:
- "How much does Firebase cost for 100k users?"
- "Estimate Firestore costs for my app"
- "What's in Firebase free tier?"

## Cost Estimation Process

1. **Identify plan** (Spark free vs Blaze pay-as-you-go)
2. **Query current pricing** using available tools
3. **Estimate usage** based on app requirements
4. **Calculate costs** above free tier
5. **Identify cost drivers** (usually Firestore reads)

## Pricing Structure (Query for Current Values)

### Plans

| Plan | Query Method |
|------|-------------|
| Spark (Free) | `firebase.google.com/pricing` |
| Blaze (Pay-as-you-go) | GCP Billing API |

### Service Pricing (Use GCP Billing API)

| Service | GCP Service Name |
|---------|-----------------|
| Firestore | Cloud Firestore |
| Cloud Functions | Cloud Functions |
| Cloud Storage | Cloud Storage |
| Hosting | Firebase Hosting |
| Authentication | Identity Platform |

### Get Current Usage

```bash
# Via GCP Monitoring
gcloud monitoring metrics list --filter="metric.type:firestore"

# Via Firebase Console
# https://console.firebase.google.com/project/PROJECT_ID/usage

# Firestore usage via API
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://firestore.googleapis.com/v1/projects/PROJECT_ID/databases/(default)"
```

## Output Contract

```yaml
firebase_cost_estimate:
  description: "<what's being estimated>"
  pricing_source: "<cli|api|web|gcp-billing>"
  pricing_date: "<when pricing was fetched>"

  recommended_plan: "<spark|blaze>"

  usage_estimate:
    firestore_reads_per_day: <N>
    firestore_writes_per_day: <N>
    firestore_storage_gb: <N>
    function_invocations_per_month: <N>
    storage_gb: <N>
    bandwidth_gb: <N>
    mau: <N>

  free_tier_usage:
    firestore_reads: "<within/exceeds>"
    firestore_writes: "<within/exceeds>"
    functions: "<within/exceeds>"
    storage: "<within/exceeds>"

  baseline_monthly:
    firestore_reads: "<$X>"
    firestore_writes: "<$X>"
    firestore_storage: "<$X>"
    cloud_functions: "<$X>"
    storage: "<$X>"
    hosting: "<$X>"
    auth: "<$X>"
    total: "<$X>"

  at_10x_scale:
    firestore: "<$X>"
    functions: "<$X>"
    total: "<$X>"

  cost_drivers:
    - "<primary driver>"

  warnings:
    - "<cost warning if applicable>"

  optimization_tips:
    - "<tip 1>"
    - "<tip 2>"
```

## Cost Optimization Strategies

### Monitor Firestore Usage

```bash
# Enable Firestore usage tracking
# In Firebase Console: Firestore > Usage tab

# Or via GCP Monitoring
gcloud monitoring dashboards create \
  --config-from-file=firestore-dashboard.json
```

### Analyze Read Patterns

```javascript
// Enable Firestore debug logging (client-side)
firebase.firestore.setLogLevel('debug');

// Use Firebase Performance Monitoring
// Tracks Firestore operations automatically
```

### Optimize Queries

```javascript
// BAD: Fetching entire collection
const snapshot = await db.collection('users').get();

// GOOD: Paginate and limit
const snapshot = await db.collection('users')
  .orderBy('createdAt')
  .limit(20)
  .get();

// GOOD: Select specific fields
const snapshot = await db.collection('users')
  .select('name', 'email')
  .get();
```

### Use Caching

```javascript
// Enable offline persistence
firebase.firestore().enablePersistence()
  .catch((err) => console.log('Persistence failed:', err));

// Use cache-first queries where appropriate
const snapshot = await db.collection('config')
  .get({ source: 'cache' });
```

## Firebase Cost Considerations

**Watch out for**:
- Firestore reads scale quickly (every listener = reads)
- Realtime listeners multiply read costs
- Phone auth SMS costs ($0.01-0.06 per verification)
- Large document reads (charged per document, not size)

**Cost traps**:
- Listening to large collections without limits
- Not using pagination
- Fetching entire documents for small fields
- Not enabling offline persistence

## Firebase vs Alternatives

When comparing costs, use the respective cost evaluator skills:
- **vs Supabase**: Use `cost-supabase` for comparison
- **vs AWS**: Use `cost-aws` for comparison
- Generally: Firebase cheaper for small apps, can get expensive at scale due to read costs
