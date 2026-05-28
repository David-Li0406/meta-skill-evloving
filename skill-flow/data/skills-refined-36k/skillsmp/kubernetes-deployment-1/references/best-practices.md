# Kubernetes Best Practices Reference

## Configuration Best Practices

### Resource Management
- Always specify resource requests and limits for containers
- Use appropriate CPU and memory values based on application needs
- Implement Quality of Service (QoS) classes by setting consistent requests and limits

### Health Checks
- Implement liveness probes to detect and recover from deadlocks
- Use readiness probes to ensure traffic is only sent to ready containers
- Set appropriate initial delay and timeout values

### Security
- Run containers as non-root users
- Use secrets for sensitive configuration data
- Implement network policies for service isolation
- Apply least-privilege principle for RBAC permissions

## Deployment Strategies

### Rolling Updates
- Use rolling updates to ensure zero-downtime deployments
- Configure appropriate maxSurge and maxUnavailable values
- Implement proper health checks to validate new pods

### Blue-Green Deployments
- Maintain two identical production environments
- Switch traffic between environments after validation
- Provides quick rollback capability

## Scaling Guidelines

### Horizontal Pod Autoscaling (HPA)
- Use CPU utilization as the primary metric
- Consider custom metrics for application-specific scaling
- Ensure metrics-server is deployed in the cluster

### Vertical Pod Autoscaling (VPA)
- Use when application resource requirements change over time
- Monitor resource usage patterns to optimize requests

## Storage Considerations

### Persistent Volumes
- Use dynamic provisioning with StorageClasses
- Implement appropriate retention policies
- Consider backup and disaster recovery strategies

### Volume Mounts
- Separate storage for logs, data, and temporary files
- Use appropriate access modes (ReadWriteOnce, ReadWriteMany)

## Networking

### Service Discovery
- Use Kubernetes DNS for service-to-service communication
- Implement proper naming conventions for services
- Use headless services for stateful applications when needed

### Ingress Configuration
- Use TLS termination at the ingress controller
- Implement proper path-based routing
- Configure load balancing algorithms appropriately

## Monitoring and Observability

### Logging
- Use structured logging formats
- Implement centralized logging solutions
- Ensure logs are accessible for debugging

### Metrics
- Expose application metrics via standard endpoints
- Use Prometheus for metric collection and storage
- Implement alerting rules for critical metrics

## Helm Best Practices

### Chart Structure
- Organize templates logically (deployment, service, ingress, etc.)
- Use values.yaml for configurable parameters
- Implement proper dependency management

### Testing
- Use helm template for local validation
- Implement tests within charts
- Validate charts against different Kubernetes versions

## Minikube Specific Considerations

### Resource Allocation
- Allocate sufficient CPU and memory for development
- Configure appropriate disk space for persistent volumes
- Enable necessary addons (ingress, metrics-server)

### Image Management
- Use minikube image load to add local images to the cluster
- Configure image pull policies appropriately
- Consider using minikube's built-in Docker daemon
