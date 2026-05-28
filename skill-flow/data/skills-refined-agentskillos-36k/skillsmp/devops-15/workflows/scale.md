# Workflow: Scale Infrastructure

## Purpose
Implement scaling strategies to handle increased load, ensure high availability, and optimize resource utilization. This workflow covers both horizontal scaling (more instances) and vertical scaling (bigger instances).

## When to Use
- Application experiencing high load or traffic growth
- Need to handle traffic spikes (planned or unplanned)
- Improving availability and reliability
- Optimizing resource costs
- Preparing for anticipated growth
- Reducing resource waste during low-traffic periods

## Prerequisites
- Application is containerized or easily scalable
- Monitoring shows current resource utilization
- Load patterns are understood
- Performance bottlenecks identified
- Target capacity and SLAs defined

## Workflow Steps

### 1. Analyze Current State

**Gather scaling context:**
- What is current load and capacity?
- What are the bottlenecks? (CPU, memory, I/O, database)
- What is the target capacity?
- What are traffic patterns? (steady, spiky, seasonal)
- What is the current architecture?

**Ask clarifying questions:**
- "What is the current request rate and target rate?"
- "What resource is the bottleneck? (CPU, memory, database?)"
- "Do you have predictable traffic patterns or sudden spikes?"
- "What is your budget for infrastructure?"
- "What is the acceptable response time under load?"

**Review monitoring data:**
```yaml
Check current metrics:
  - Current request rate (req/s)
  - Response time under load
  - CPU utilization per instance
  - Memory utilization per instance
  - Database connection pool usage
  - Queue depths and wait times
  - Error rate under load
```

### 2. Identify Scaling Strategy

**Horizontal Scaling (recommended for most cases):**
- Add more instances of the application
- Better for stateless applications
- Provides redundancy and high availability
- Easier to scale up and down dynamically
- Better fault tolerance

**Vertical Scaling:**
- Increase instance size (more CPU/memory)
- Simpler for stateful applications
- Limited by maximum instance size
- May require downtime
- Single point of failure

**Auto-scaling (best for variable load):**
- Automatically adjust instance count based on metrics
- Handles traffic spikes automatically
- Optimizes costs during low-traffic periods
- Requires proper configuration and testing

### 3. Design Scaling Plan

**For Horizontal Scaling:**

**Define scaling parameters:**
```yaml
Scaling Configuration:
  Minimum instances: 2 (for high availability)
  Maximum instances: 20 (cost limit)
  Desired instances: 5 (normal load)

  Scale up when:
    - CPU utilization > 70% for 5 minutes
    - Memory utilization > 80% for 5 minutes
    - Request queue depth > 100

  Scale down when:
    - CPU utilization < 30% for 10 minutes
    - Memory utilization < 50% for 10 minutes
    - Request queue depth < 10

  Cool-down periods:
    - Scale up: 60 seconds (respond quickly to load)
    - Scale down: 300 seconds (avoid flapping)
```

**Calculate capacity needs:**
```yaml
Capacity Planning:
  Current: 100 req/s with 5 instances
  Capacity per instance: 20 req/s
  Target load: 500 req/s
  Required instances: 25 instances
  Safety buffer: 25% = 31 instances
  Configuration: min=5, desired=10, max=35
```

### 4. Implement Horizontal Auto-Scaling

**For Kubernetes (Horizontal Pod Autoscaler):**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
```

**Deploy HPA:**
```bash
# Apply HPA configuration
kubectl apply -f hpa.yaml

# Verify HPA is working
kubectl get hpa

# Watch HPA in action
kubectl get hpa -w

# Check HPA events
kubectl describe hpa my-app-hpa
```

**For AWS (Auto Scaling Group):**

```yaml
# Auto Scaling Group configuration
AutoScalingGroup:
  MinSize: 2
  MaxSize: 20
  DesiredCapacity: 5
  HealthCheckType: ELB
  HealthCheckGracePeriod: 300
  TargetGroupARNs:
    - <load-balancer-target-group>

ScalingPolicies:
  - Name: scale-up-policy
    PolicyType: TargetTrackingScaling
    TargetValue: 70
    MetricType: CPUUtilization

  - Name: scale-down-policy
    PolicyType: TargetTrackingScaling
    TargetValue: 30
    MetricType: CPUUtilization
```

**For GCP (Managed Instance Group):**

```bash
# Create autoscaler
gcloud compute instance-groups managed set-autoscaling my-instance-group \
  --max-num-replicas 20 \
  --min-num-replicas 2 \
  --target-cpu-utilization 0.7 \
  --cool-down-period 60
```

### 5. Implement Load Balancing

**Load balancer is essential for horizontal scaling:**

**For Kubernetes (Service):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  sessionAffinity: None  # or ClientIP for sticky sessions
```

**For cloud platforms:**
```yaml
# AWS: Application Load Balancer (ALB)
# GCP: Cloud Load Balancing
# Azure: Azure Load Balancer

Configure:
  - Health checks
  - Connection draining
  - Session affinity (if needed)
  - SSL termination
  - Request routing rules
```

**Health check configuration:**
```yaml
HealthCheck:
  Path: /health
  Interval: 30 seconds
  Timeout: 5 seconds
  HealthyThreshold: 2
  UnhealthyThreshold: 3
  SuccessCode: 200
```

### 6. Implement Vertical Scaling

**When vertical scaling is appropriate:**
- Stateful applications (databases)
- Single-instance limitations
- Memory-intensive workloads
- Temporary solution before re-architecture

**For Kubernetes:**
```yaml
# Update deployment with larger resources
spec:
  containers:
  - name: my-app
    resources:
      requests:
        memory: "2Gi"  # Increased from 1Gi
        cpu: "1000m"   # Increased from 500m
      limits:
        memory: "4Gi"  # Increased from 2Gi
        cpu: "2000m"   # Increased from 1000m
```

**Apply changes:**
```bash
# Update deployment
kubectl apply -f deployment.yaml

# Monitor rollout
kubectl rollout status deployment/my-app

# Verify new pod resources
kubectl describe pod <pod-name> | grep -A 5 "Limits\|Requests"
```

**For cloud platforms:**
```bash
# AWS: Change instance type
# GCP: Change machine type
# Azure: Resize VM

# Usually requires brief downtime
# Plan during maintenance window
```

### 7. Scale Database Layer

**Database scaling strategies:**

**Read replicas (for read-heavy workloads):**
```yaml
Primary Database:
  - Handles all writes
  - Handles critical reads

Read Replicas:
  - Handle read traffic
  - Reduce load on primary
  - Can be in different regions
  - Auto-failover available

Configuration:
  - 1 primary instance
  - 2-5 read replicas
  - Load balance reads across replicas
  - Route writes to primary only
```

**Connection pooling:**
```javascript
// Application-level connection pooling
const pool = new Pool({
  max: 20,           // Maximum connections
  min: 5,            // Minimum connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});
```

**Database vertical scaling:**
```yaml
# Increase database instance size
# For RDS, CloudSQL, etc.

Considerations:
  - Requires brief downtime
  - Plan during maintenance window
  - Test performance after scaling
  - Monitor query performance
```

**Database sharding (for extreme scale):**
```yaml
# Distribute data across multiple databases
# Complex but highly scalable
# Consider when:
  - Single database can't handle load
  - Data can be partitioned logically
  - Read replicas aren't sufficient
```

### 8. Implement Caching

**Reduce load through caching:**

**Application-level caching (Redis/Memcached):**
```javascript
// Redis caching example
const redis = require('redis');
const client = redis.createClient();

async function getUser(userId) {
  // Check cache first
  const cached = await client.get(`user:${userId}`);
  if (cached) {
    return JSON.parse(cached);
  }

  // Cache miss - fetch from database
  const user = await database.getUser(userId);

  // Store in cache (expire after 1 hour)
  await client.setex(`user:${userId}`, 3600, JSON.stringify(user));

  return user;
}
```

**CDN for static assets:**
```yaml
# Use CloudFront, Cloudflare, or similar
# Cache static assets (images, CSS, JS)
# Reduce origin load
# Improve response times globally
```

**HTTP caching:**
```javascript
// Set cache headers
app.get('/api/data', (req, res) => {
  res.set('Cache-Control', 'public, max-age=300'); // 5 minutes
  res.json(data);
});
```

### 9. Test Scaling

**Load testing before production:**

**Using load testing tools:**
```bash
# k6 load testing
k6 run --vus 100 --duration 5m loadtest.js

# Apache Bench
ab -n 10000 -c 100 https://myapp.com/

# Artillery
artillery quick --count 100 --num 50 https://myapp.com/

# Locust (Python-based)
locust -f locustfile.py --host=https://myapp.com
```

**Test scenarios:**
```yaml
Test Cases:
  1. Gradual ramp-up:
     - Start: 10 users
     - Ramp to: 1000 users over 10 minutes
     - Verify: Auto-scaling triggers appropriately

  2. Sudden spike:
     - Jump from 10 to 1000 users instantly
     - Verify: Quick scale-up response
     - Check: Error rate during spike

  3. Sustained load:
     - Maintain 500 users for 30 minutes
     - Verify: Stable performance
     - Check: Resource utilization

  4. Scale down:
     - Drop from 500 to 10 users
     - Verify: Gradual scale-down
     - Check: No service disruption
```

**Monitor during load tests:**
```yaml
Watch metrics:
  - Response time (should stay within SLA)
  - Error rate (should stay < 1%)
  - Instance count (should scale up/down)
  - CPU/Memory utilization per instance
  - Database connections
  - Queue depths
```

### 10. Optimize and Fine-Tune

**Review scaling performance:**
```yaml
Optimization areas:
  1. Scaling thresholds:
     - Too aggressive? Causing flapping?
     - Too conservative? Slow to respond?

  2. Cool-down periods:
     - Scale-up too slow?
     - Scale-down too fast (wasting resources)?

  3. Resource limits:
     - Instances under-provisioned?
     - Instances over-provisioned (waste)?

  4. Application efficiency:
     - Memory leaks?
     - Inefficient queries?
     - Missing indexes?
```

**Common optimizations:**
```yaml
- Reduce scale-up cooldown for faster response
- Increase scale-down cooldown to avoid flapping
- Adjust CPU/memory thresholds based on actual usage
- Implement request queuing for burst traffic
- Optimize application code for efficiency
- Add database indexes for slow queries
- Implement connection pooling
- Use caching more aggressively
```

## Deliverables

**Scaling infrastructure:**
- Auto-scaling configuration deployed
- Load balancer configured
- Health checks operational
- Monitoring for scaling metrics

**Documentation:**
- Scaling strategy documented
- Auto-scaling thresholds documented
- Load testing results
- Capacity planning calculations
- Troubleshooting guide

**Validation:**
- Load test results showing successful scaling
- Monitoring dashboards for scaling metrics
- Runbooks for scaling operations

## Validation Checklist

Before completing this workflow:
- [ ] Auto-scaling configuration deployed
- [ ] Minimum instance count ensures high availability (≥ 2)
- [ ] Maximum instance count prevents runaway costs
- [ ] Scaling thresholds tested and validated
- [ ] Load balancer distributes traffic evenly
- [ ] Health checks detect unhealthy instances
- [ ] Load testing shows scaling works under load
- [ ] Monitoring tracks scaling events
- [ ] Scale-up responds quickly to load (< 2 min)
- [ ] Scale-down is gradual to avoid disruption
- [ ] No service disruption during scaling
- [ ] Documentation is complete

## Common Patterns

**Predictive scaling:**
```yaml
# Schedule scaling for known traffic patterns
# Scale up before traffic arrives
# Scale down after peak hours

Example:
  - Scale to 20 instances at 8 AM (workday start)
  - Scale to 5 instances at 6 PM (workday end)
  - Scale to 2 instances on weekends
```

**Multi-tier scaling:**
```yaml
# Scale different layers independently
Application Layer:
  - Scale based on request rate
  - Quick scale-up for traffic spikes

Database Layer:
  - Scale read replicas for read load
  - Vertical scale primary for write load

Cache Layer:
  - Scale cache cluster for cache misses
  - Ensure cache hit rate > 80%
```

## Troubleshooting

**Auto-scaling not triggering:**
```bash
# Check HPA status
kubectl get hpa
kubectl describe hpa <name>

# Verify metrics are available
kubectl top pods

# Check metrics server
kubectl get apiservice v1beta1.metrics.k8s.io

# Verify resource requests are set
kubectl describe deployment <name>
```

**Scaling too slow:**
- Reduce scale-up cooldown period
- Adjust scaling policies to add more pods per interval
- Check if maximum instances limit is too low
- Verify metrics are reporting accurately

**Scaling causing instability:**
- Increase scale-down cooldown to prevent flapping
- Adjust thresholds to avoid oscillation
- Ensure health checks are reliable
- Check for memory leaks causing scale-up cycles

**Performance not improving with scaling:**
- Identify actual bottleneck (may not be application)
- Check database performance
- Verify load balancer is distributing evenly
- Look for shared resource contention
- Profile application for inefficiencies

## Cost Optimization

**Reduce scaling costs:**
```yaml
Strategies:
  1. Right-size instances:
     - Use smaller instances with more of them
     - Better for horizontal scaling

  2. Use spot/preemptible instances:
     - Mix of on-demand and spot instances
     - Save 60-90% on compute costs
     - For non-critical workloads

  3. Aggressive scale-down:
     - Scale down quickly during low traffic
     - Set low minimum instance count

  4. Schedule scaling:
     - Reduce instances during known low-traffic periods
     - Scale proactively for known peaks

  5. Optimize application:
     - Reduce resource usage per instance
     - Handle more load with fewer instances
```

## Success Metrics

A successful scaling implementation achieves:
- **High availability** - Multiple instances, no single point of failure
- **Responsive scaling** - Scales up in < 2 minutes for load spikes
- **Stable performance** - Response time within SLA under all loads
- **Cost efficient** - Scales down during low traffic, optimized costs
- **Zero disruption** - Scaling events don't cause errors or downtime
- **Predictable** - Auto-scaling behavior is well understood
- **Monitored** - Scaling events and capacity tracked in dashboards
