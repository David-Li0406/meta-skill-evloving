# Deployment Strategies

## Overview
This document describes various deployment strategies, when to use each, and how to implement them. Choose the right strategy based on your risk tolerance, downtime requirements, and infrastructure capabilities.

## Strategy Comparison Matrix

| Strategy | Downtime | Rollback Speed | Complexity | Cost | Best For |
|----------|----------|----------------|------------|------|----------|
| Recreate | Yes (minutes) | Fast | Low | Low | Dev environments |
| Rolling | No | Medium | Low | Low | Standard deployments |
| Blue-Green | No | Instant | Medium | High (2x infrastructure) | Critical services |
| Canary | No | Fast | High | Medium | High-risk changes |
| A/B Testing | No | Fast | High | Medium | Feature validation |
| Shadow | No | N/A | High | High | Testing in production |

## 1. Recreate Deployment

### Description
Stop all instances of the old version, then start new version instances.

### Flow
```yaml
1. Stop all old version instances
2. Wait for complete shutdown
3. Start all new version instances
4. Verify health checks
```

### Characteristics
- **Downtime**: Yes (minutes to tens of minutes)
- **Rollback**: Fast (redeploy old version)
- **Complexity**: Low
- **Cost**: Low (no additional infrastructure)

### When to Use
- Development environments
- Maintenance windows acceptable
- Non-critical applications
- Cost is primary concern

### When NOT to Use
- Production critical services
- 24/7 availability required
- Customer-facing applications

### Implementation

**Kubernetes:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  strategy:
    type: Recreate  # All pods terminated before new ones created
  template:
    spec:
      containers:
      - name: app
        image: myapp:v2
```

**Manual:**
```bash
# Stop all instances
systemctl stop myapp

# Deploy new version
cp /releases/myapp-v2 /production/myapp

# Start new version
systemctl start myapp
```

### Pros
- Simple to understand and implement
- No additional infrastructure cost
- Clean state between versions

### Cons
- Downtime during deployment
- Not suitable for production
- No gradual rollout

---

## 2. Rolling Deployment

### Description
Gradually replace instances of the old version with new version, one or a few at a time.

### Flow
```yaml
1. Start new version instance
2. Wait for health checks to pass
3. Stop one old version instance
4. Repeat until all instances replaced
5. Monitor throughout process
```

### Characteristics
- **Downtime**: None
- **Rollback**: Medium speed (reverse the rollout)
- **Complexity**: Low
- **Cost**: Low (no additional infrastructure)

### When to Use
- Standard production deployments
- Zero-downtime requirement
- Limited infrastructure budget
- Kubernetes or similar orchestration

### When NOT to Use
- Database schema breaking changes
- Cannot run old and new versions together
- Need instant rollback capability

### Implementation

**Kubernetes:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Max 2 extra pods during update
      maxUnavailable: 1  # Max 1 pod unavailable during update
  template:
    spec:
      containers:
      - name: app
        image: myapp:v2
        readinessProbe:   # Critical for rolling updates
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

**Manual script:**
```bash
#!/bin/bash
INSTANCES=(instance-1 instance-2 instance-3 instance-4)

for instance in "${INSTANCES[@]}"; do
  # Deploy new version to instance
  ssh $instance "deploy-new-version.sh"

  # Wait for health check
  while ! curl -f http://$instance/health; do
    sleep 5
  done

  # Add to load balancer
  add-to-lb $instance

  # Wait before next instance
  sleep 30
done
```

### Pros
- Zero downtime
- No additional infrastructure
- Gradual rollout reduces risk
- Native to Kubernetes

### Cons
- Old and new versions run simultaneously
- Rollback slower than blue-green
- Cannot control traffic percentage precisely

### Best Practices
```yaml
- Set proper maxSurge and maxUnavailable
- Configure readiness probes correctly
- Monitor error rates during rollout
- Set reasonable progressDeadlineSeconds
- Test backward compatibility
```

---

## 3. Blue-Green Deployment

### Description
Maintain two identical production environments (blue and green). Deploy to inactive environment, then switch traffic.

### Flow
```yaml
1. Blue environment serves production traffic
2. Deploy new version to green environment
3. Test green environment thoroughly
4. Switch traffic from blue to green
5. Monitor green environment
6. Keep blue ready for instant rollback
```

### Characteristics
- **Downtime**: None
- **Rollback**: Instant (switch traffic back)
- **Complexity**: Medium
- **Cost**: High (2x infrastructure during deployment)

### When to Use
- Critical production services
- Need instant rollback capability
- Zero downtime requirement
- Can afford 2x infrastructure temporarily

### When NOT to Use
- Database schema changes (shared state)
- Cost constraints
- Stateful applications without shared storage

### Implementation

**AWS with Elastic Beanstalk:**
```bash
# Deploy to green environment
eb create my-app-green --cname my-app-green

# Test green environment
curl https://my-app-green.elasticbeanstalk.com/health

# Swap URLs (blue ↔ green)
eb swap my-app-blue --destination-name my-app-green
```

**Kubernetes with Services:**
```yaml
# Blue deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: blue
  template:
    metadata:
      labels:
        app: my-app
        version: blue
    spec:
      containers:
      - name: app
        image: myapp:v1

---
# Green deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: green
  template:
    metadata:
      labels:
        app: my-app
        version: green
    spec:
      containers:
      - name: app
        image: myapp:v2

---
# Service (switch by changing selector)
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
    version: blue  # Change to "green" to switch
  ports:
  - port: 80
    targetPort: 8080
```

**Traffic switch:**
```bash
# Switch to green
kubectl patch service my-app -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback to blue
kubectl patch service my-app -p '{"spec":{"selector":{"version":"blue"}}}'
```

### Pros
- Instant rollback
- Full testing before traffic switch
- Clean cutover
- Zero downtime

### Cons
- Requires 2x infrastructure
- Database migrations complex
- Shared state challenges
- Higher cost

### Best Practices
```yaml
- Test green environment thoroughly before switch
- Automate traffic switch
- Keep blue environment for 24-48 hours
- Monitor closely after switch
- Have automated rollback triggers
- Use smoke tests before and after switch
```

---

## 4. Canary Deployment

### Description
Deploy new version to a small subset of instances, gradually increase traffic, monitor, and rollback if issues detected.

### Flow
```yaml
1. Deploy canary version (10% of instances)
2. Route 10% of traffic to canary
3. Monitor metrics for 15-30 minutes
4. If healthy, increase to 50% traffic
5. Monitor for 15-30 minutes
6. If healthy, increase to 100% traffic
7. Remove old version
```

### Characteristics
- **Downtime**: None
- **Rollback**: Fast (stop routing to canary)
- **Complexity**: High
- **Cost**: Medium

### When to Use
- High-risk deployments
- Major feature releases
- Need gradual validation
- Want to limit blast radius

### When NOT to Use
- Cannot measure canary metrics separately
- Low-traffic applications
- Need immediate full rollout

### Implementation

**Kubernetes with Flagger:**
```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: my-app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  service:
    port: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
```

**Manual canary with Nginx:**
```nginx
upstream backend {
  server backend-v1:8080 weight=9;  # 90% traffic
  server backend-v2:8080 weight=1;  # 10% traffic
}

# Gradually adjust weights
# 90/10 → 50/50 → 0/100
```

**AWS with ALB:**
```bash
# Register canary target group with 10% weight
aws elbv2 modify-listener \
  --listener-arn $LISTENER_ARN \
  --default-actions \
    Type=forward,ForwardConfig='{
      "TargetGroups":[
        {"TargetGroupArn":"'$TG_V1'","Weight":90},
        {"TargetGroupArn":"'$TG_V2'","Weight":10}
      ]
    }'
```

### Monitoring During Canary

**Key metrics to compare:**
```yaml
Canary vs Stable:
  - Error rate (should be equal or lower)
  - Response time (should be equal or lower)
  - Throughput (should be proportional)
  - CPU/Memory usage (should be similar)
  - Business metrics (conversion, signups, etc.)
```

**Automated rollback triggers:**
```yaml
Rollback if:
  - Canary error rate > stable + 5%
  - Canary p95 latency > stable + 50%
  - Canary error rate > 5% absolute
  - Manual intervention requested
```

### Progressive Traffic Shift

**Standard canary progression:**
```yaml
Phase 1: 10% traffic, 15 min
  - Initial validation
  - Catch obvious issues

Phase 2: 25% traffic, 15 min
  - Broader validation
  - More data points

Phase 3: 50% traffic, 30 min
  - Significant validation
  - Database impact visible

Phase 4: 100% traffic
  - Complete rollout
  - Monitor for 1-2 hours
```

### Pros
- Limits blast radius
- Gradual validation
- Real production traffic testing
- Automated rollback possible

### Cons
- Complex implementation
- Requires traffic routing control
- Needs robust monitoring
- Longer deployment time

### Best Practices
```yaml
- Define clear success metrics
- Automate traffic shifting
- Monitor continuously
- Set conservative thresholds
- Test rollback procedure
- Use for high-risk changes only
```

---

## 5. A/B Testing Deployment

### Description
Similar to canary, but routes specific user segments to different versions for feature comparison.

### Flow
```yaml
1. Deploy both versions simultaneously
2. Route users based on criteria:
   - User ID hash
   - Geographic location
   - User segment
   - Random assignment
3. Collect metrics on both versions
4. Analyze performance and user behavior
5. Choose winning version
```

### Characteristics
- **Downtime**: None
- **Rollback**: Fast
- **Complexity**: High
- **Cost**: Medium to High

### When to Use
- Testing feature variations
- Validating UX changes
- Measuring business impact
- Data-driven decision making

### When NOT to Use
- Bug fixes (deploy to all)
- Security updates (deploy to all)
- Infrastructure changes

### Implementation

**Feature flag based:**
```javascript
// Server-side feature flag
app.get('/checkout', async (req, res) => {
  const userId = req.user.id;
  const variation = await featureFlags.getVariation('new-checkout', userId);

  if (variation === 'new') {
    res.render('checkout-v2');
  } else {
    res.render('checkout-v1');
  }
});
```

**Traffic routing based:**
```nginx
# Route based on cookie or header
map $http_x_ab_test $backend {
  "variant-a" backend-a;
  "variant-b" backend-b;
  default     backend-a;
}

server {
  location / {
    proxy_pass http://$backend;
  }
}
```

### Metrics to Track

```yaml
Business Metrics:
  - Conversion rate
  - Revenue per user
  - User engagement
  - Feature adoption
  - User satisfaction

Technical Metrics:
  - Performance (response time)
  - Error rates
  - Resource utilization
  - API call patterns
```

---

## 6. Shadow Deployment

### Description
Deploy new version alongside production, send copy of production traffic to new version, but don't return its responses to users.

### Flow
```yaml
1. Deploy shadow version
2. Mirror production traffic to shadow
3. Compare responses (optional)
4. Collect metrics on shadow version
5. If shadow performs well, promote to production
```

### Characteristics
- **Downtime**: None
- **Rollback**: N/A (shadow doesn't affect users)
- **Complexity**: High
- **Cost**: High (running extra instances)

### When to Use
- Testing with real production load
- Performance testing
- Validating rewrites or migrations
- No user impact tolerance

### When NOT to Use
- Limited infrastructure budget
- Cannot handle side effects (writes to DB)
- Low-traffic applications

### Implementation

**Istio (Kubernetes):**
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: my-app
spec:
  hosts:
  - my-app
  http:
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: my-app-v1
      weight: 100
    mirror:
      host: my-app-v2  # Shadow traffic
    mirrorPercentage:
      value: 100
```

**Nginx (mirroring):**
```nginx
location / {
  mirror /mirror;
  proxy_pass http://backend-v1;
}

location /mirror {
  internal;
  proxy_pass http://backend-v2$request_uri;
  proxy_ignore_client_abort on;
}
```

### Pros
- No user impact
- Real production testing
- Performance validation
- Compare implementations

### Cons
- Expensive (extra infrastructure)
- Side effects need handling
- Complex setup
- Mirrored traffic may differ

---

## Database Migration Strategies

### 1. Backward Compatible Migrations

**Pattern:**
```yaml
Phase 1: Add new column (nullable)
  - Deploy app supporting both old and new columns
  - Gradual data migration

Phase 2: Deprecate old column
  - Deploy app using only new column
  - Remove old column in next release
```

### 2. Expand-Contract Pattern

**Pattern:**
```yaml
1. Expand: Add new schema alongside old
2. Migrate: Dual-write to both schemas
3. Contract: Remove old schema

Deployment:
  - V1: Writes to old schema only
  - V2: Writes to both schemas, reads from old
  - V3: Writes to both, reads from new
  - V4: Writes to new only
  - V5: Remove old schema
```

### 3. Read-Write Split

**Pattern:**
```yaml
For schema changes:
  1. Create new tables/columns
  2. Deploy code writing to both old and new
  3. Backfill data
  4. Deploy code reading from new
  5. Remove old tables/columns
```

---

## Feature Flag Deployment

### Description
Deploy code with features toggled off, enable for specific users or environments.

### Implementation

```javascript
// LaunchDarkly, Unleash, or custom
const features = {
  newCheckout: {
    enabled: false,
    rollout: {
      percentage: 25,  // 25% of users
    }
  }
};

if (featureFlags.isEnabled('newCheckout', user)) {
  // New checkout flow
} else {
  // Old checkout flow
}
```

### Benefits
```yaml
- Decouple deployment from release
- Gradual feature rollout
- Instant feature disable (kill switch)
- A/B testing capability
- Trunk-based development
```

---

## Choosing the Right Strategy

### Decision Tree

```yaml
Can you tolerate downtime?
  ├─ Yes → Recreate
  └─ No → Continue

Is this a high-risk change?
  ├─ Yes → Canary or Blue-Green
  └─ No → Rolling

Need instant rollback?
  ├─ Yes → Blue-Green
  └─ No → Continue

Testing feature variations?
  ├─ Yes → A/B Testing
  └─ No → Continue

Need real traffic testing with no user impact?
  ├─ Yes → Shadow
  └─ No → Rolling
```

### Recommendations by Application Type

**Stateless web applications:**
- Standard: Rolling deployment
- High-risk: Canary deployment

**Stateful applications:**
- Blue-Green (with shared storage)
- Careful database migration planning

**Microservices:**
- Rolling or Canary
- Service mesh for traffic control

**Monolithic applications:**
- Blue-Green or Rolling
- Feature flags for large features

**Critical services (payment, auth):**
- Blue-Green or Canary
- Extensive monitoring
- Automated rollback

---

## Best Practices Across All Strategies

### Pre-Deployment
```yaml
- Test deployment in staging
- Verify backward compatibility
- Prepare rollback plan
- Review monitoring dashboards
- Brief team on deployment
```

### During Deployment
```yaml
- Monitor error rates
- Watch response times
- Check logs for errors
- Verify health checks
- Track business metrics
```

### Post-Deployment
```yaml
- Verify deployment success
- Monitor for 24+ hours
- Document issues encountered
- Update runbooks
- Conduct retrospective
```

### Always
```yaml
- Automate deployments
- Test rollback procedures
- Monitor continuously
- Document strategy
- Practice deployments
```
