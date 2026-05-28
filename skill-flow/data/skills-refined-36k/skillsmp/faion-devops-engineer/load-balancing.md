---
id: load-balancing
name: "Load Balancing"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Load Balancing

## Overview

Load balancing distributes network traffic across multiple servers to ensure high availability, reliability, and performance. This methodology covers load balancing strategies, algorithms, health checks, and implementation across different technologies.

## When to Use

- Scaling applications horizontally
- Ensuring high availability (HA)
- Improving application performance
- Implementing zero-downtime deployments
- Managing traffic spikes

## Process/Steps

### 1. Load Balancing Concepts

**Architecture Patterns:**
```
                           ┌─────────────────┐
                           │   Load Balancer  │
                           │    (L4 or L7)    │
                           └────────┬────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
        ┌─────▼─────┐         ┌─────▼─────┐         ┌─────▼─────┐
        │  Server 1  │         │  Server 2  │         │  Server 3  │
        │  (Active)  │         │  (Active)  │         │  (Standby) │
        └───────────┘         └───────────┘         └───────────┘
```

**Load Balancer Types:**
| Type | OSI Layer | Features | Use Case |
|------|-----------|----------|----------|
| L4 (Transport) | Layer 4 | TCP/UDP routing, fast | High throughput |
| L7 (Application) | Layer 7 | HTTP routing, SSL termination | Web applications |
| DNS | Layer 3 | Geographic distribution | Global load balancing |
| Global | Multi-layer | Cross-region failover | Multi-cloud, DR |

### 2. Load Balancing Algorithms

**Common Algorithms:**
```yaml
algorithms:
  round_robin:
    description: "Distributes requests sequentially"
    use_case: "Equal capacity servers"
    pros: ["Simple", "Fair distribution"]
    cons: ["Ignores server load"]

  weighted_round_robin:
    description: "Round robin with server weights"
    use_case: "Different capacity servers"
    pros: ["Accounts for server capacity"]
    cons: ["Static weights"]

  least_connections:
    description: "Routes to server with fewest connections"
    use_case: "Long-lived connections"
    pros: ["Adapts to server load"]
    cons: ["Overhead tracking connections"]

  weighted_least_connections:
    description: "Least connections with weights"
    use_case: "Mixed capacity, long connections"
    pros: ["Best overall distribution"]
    cons: ["Complex calculation"]

  ip_hash:
    description: "Routes based on client IP"
    use_case: "Session persistence needed"
    pros: ["Sticky sessions"]
    cons: ["Uneven distribution possible"]

  least_response_time:
    description: "Routes to fastest responding server"
    use_case: "Performance critical"
    pros: ["Optimizes response time"]
    cons: ["Requires health probes"]

  random:
    description: "Random server selection"
    use_case: "Stateless applications"
    pros: ["Simple, no state"]
    cons: ["May cause uneven distribution"]
```

### 3. HAProxy Configuration

**Basic Configuration:**
```haproxy
# /etc/haproxy/haproxy.cfg

global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

    # SSL/TLS settings
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets
    tune.ssl.default-dh-param 2048

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    option  forwardfor
    option  http-server-close
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

# Stats dashboard
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    stats admin if LOCALHOST

# Frontend - HTTP redirect to HTTPS
frontend http_front
    bind *:80
    redirect scheme https code 301 if !{ ssl_fc }

# Frontend - HTTPS
frontend https_front
    bind *:443 ssl crt /etc/haproxy/certs/example.com.pem
    http-request add-header X-Forwarded-Proto https

    # ACL routing
    acl is_api path_beg /api
    acl is_static path_beg /static

    use_backend api_servers if is_api
    use_backend static_servers if is_static
    default_backend web_servers

# Backend - Web Servers
backend web_servers
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200

    server web1 10.0.0.1:8080 check weight 5
    server web2 10.0.0.2:8080 check weight 5
    server web3 10.0.0.3:8080 check weight 3 backup

# Backend - API Servers
backend api_servers
    balance leastconn
    option httpchk GET /api/health
    http-check expect status 200

    # Sticky sessions via cookie
    cookie SERVERID insert indirect nocache

    server api1 10.0.1.1:8000 check cookie api1
    server api2 10.0.1.2:8000 check cookie api2
    server api3 10.0.1.3:8000 check cookie api3

# Backend - Static Content
backend static_servers
    balance roundrobin
    option httpchk GET /health

    server static1 10.0.2.1:80 check
    server static2 10.0.2.2:80 check
```

### 4. Nginx Load Balancing

```nginx
# Upstream definitions
upstream web_backend {
    # Load balancing method
    least_conn;

    # Servers with weights and health checks
    server 10.0.0.1:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.2:8080 weight=5 max_fails=3 fail_timeout=30s;
    server 10.0.0.3:8080 weight=2 backup;

    # Keepalive connections to backend
    keepalive 32;
}

upstream api_backend {
    # IP hash for sticky sessions
    ip_hash;

    server 10.0.1.1:8000;
    server 10.0.1.2:8000;
    server 10.0.1.3:8000;
}

# Server configuration
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;

    location / {
        proxy_pass http://web_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Retry configuration
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 10s;
    }

    location /api {
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### 5. AWS Application Load Balancer

```yaml
# CloudFormation template
AWSTemplateFormatVersion: '2010-09-09'
Description: Application Load Balancer

Resources:
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: my-alb
      Scheme: internet-facing
      Type: application
      IpAddressType: ipv4
      SecurityGroups:
        - !Ref ALBSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      LoadBalancerAttributes:
        - Key: idle_timeout.timeout_seconds
          Value: '60'
        - Key: routing.http2.enabled
          Value: 'true'
        - Key: access_logs.s3.enabled
          Value: 'true'
        - Key: access_logs.s3.bucket
          Value: my-alb-logs

  HTTPSListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 443
      Protocol: HTTPS
      SslPolicy: ELBSecurityPolicy-TLS-1-2-2017-01
      Certificates:
        - CertificateArn: !Ref SSLCertificate
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref DefaultTargetGroup

  # Target Group for web servers
  WebTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: web-targets
      Port: 8080
      Protocol: HTTP
      VpcId: !Ref VPC
      TargetType: instance
      HealthCheckEnabled: true
      HealthCheckIntervalSeconds: 30
      HealthCheckPath: /health
      HealthCheckProtocol: HTTP
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3
      Matcher:
        HttpCode: '200'
      TargetGroupAttributes:
        - Key: deregistration_delay.timeout_seconds
          Value: '30'
        - Key: stickiness.enabled
          Value: 'true'
        - Key: stickiness.type
          Value: lb_cookie
        - Key: stickiness.lb_cookie.duration_seconds
          Value: '86400'

  # Listener Rule for API
  APIListenerRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HTTPSListener
      Priority: 10
      Conditions:
        - Field: path-pattern
          Values:
            - /api/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref APITargetGroup
```

### 6. Kubernetes Load Balancing

**Service Types:**
```yaml
# ClusterIP (internal only)
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080

---
# NodePort (external via node ports)
apiVersion: v1
kind: Service
metadata:
  name: web-nodeport
spec:
  type: NodePort
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080

---
# LoadBalancer (cloud provider LB)
apiVersion: v1
kind: Service
metadata:
  name: web-loadbalancer
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - port: 443
      targetPort: 8080

---
# Ingress (L7 routing)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  tls:
    - hosts:
        - example.com
      secretName: example-tls
  rules:
    - host: example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
```

### 7. Health Checks

**Health Check Types:**
```yaml
health_checks:
  tcp:
    description: "TCP connection check"
    use_case: "Basic connectivity"
    example:
      haproxy: "option tcp-check"
      nginx: "server ... check"

  http:
    description: "HTTP endpoint check"
    use_case: "Application health"
    example:
      endpoint: "/health"
      expected_status: 200
      expected_body: "OK"

  https:
    description: "HTTPS endpoint check"
    use_case: "SSL-enabled services"
    verify_ssl: true

  script:
    description: "Custom script check"
    use_case: "Complex health logic"
    example: "/usr/local/bin/check-app.sh"

  grpc:
    description: "gRPC health check"
    use_case: "gRPC services"
    example: "grpc.health.v1.Health/Check"
```

**Health Check Implementation:**
```python
# Python Flask health endpoint
from flask import Flask, jsonify
import psycopg2
import redis

app = Flask(__name__)

@app.route('/health')
def health():
    """Basic health check"""
    return jsonify({"status": "healthy"}), 200

@app.route('/health/live')
def liveness():
    """Liveness probe - is the process running?"""
    return jsonify({"status": "alive"}), 200

@app.route('/health/ready')
def readiness():
    """Readiness probe - can we serve traffic?"""
    checks = {
        "database": check_database(),
        "cache": check_cache(),
        "dependencies": check_dependencies()
    }

    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503

    return jsonify({
        "status": "ready" if all_healthy else "not ready",
        "checks": checks
    }), status_code

def check_database():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        return True
    except:
        return False

def check_cache():
    try:
        r = redis.Redis.from_url(REDIS_URL)
        r.ping()
        return True
    except:
        return False
```

## Best Practices

### High Availability
1. **Multiple LB instances** - Avoid single point of failure
2. **Cross-zone balancing** - Distribute across AZs
3. **Health check tuning** - Balance sensitivity and stability
4. **Graceful degradation** - Handle partial failures

### Performance
1. **Connection pooling** - Reduce connection overhead
2. **Keepalive connections** - Reuse backend connections
3. **SSL termination** - Offload to load balancer
4. **Caching** - Cache static content at LB

### Security
1. **DDoS protection** - Rate limiting, WAF
2. **SSL/TLS** - Use TLS 1.2+ only
3. **Security groups** - Restrict access
4. **Access logging** - Audit trail

### Monitoring
1. **Metrics collection** - Response times, error rates
2. **Alerting** - Unhealthy backends, high latency
3. **Logging** - Request logging for troubleshooting
4. **Dashboards** - Real-time visibility

## Templates/Examples

### Terraform AWS ALB

```hcl
resource "aws_lb" "main" {
  name               = "main-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = true

  access_logs {
    bucket  = aws_s3_bucket.lb_logs.bucket
    prefix  = "alb"
    enabled = true
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_lb_target_group" "web" {
  name     = "web-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }

  stickiness {
    type            = "lb_cookie"
    cookie_duration = 86400
    enabled         = true
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}
```

## References

- [HAProxy Documentation](https://www.haproxy.org/documentation.html)
- [Nginx Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)
- [AWS ELB Documentation](https://docs.aws.amazon.com/elasticloadbalancing/)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Load Balancing Algorithms](https://www.nginx.com/resources/glossary/load-balancing/)
