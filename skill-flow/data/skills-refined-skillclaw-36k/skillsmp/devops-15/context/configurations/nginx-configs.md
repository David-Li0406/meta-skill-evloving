# Nginx Configuration Templates

## Overview
This document provides production-ready Nginx configurations for common deployment scenarios including reverse proxying, load balancing, SSL termination, and caching.

## Basic Reverse Proxy

```nginx
# /etc/nginx/nginx.conf

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/rss+xml font/truetype font/opentype
               application/vnd.ms-fontobject image/svg+xml;

    include /etc/nginx/conf.d/*.conf;
}
```

## Simple Backend Proxy

```nginx
# /etc/nginx/conf.d/app.conf

upstream backend {
    server app:3000;
}

server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Load Balancing

```nginx
# /etc/nginx/conf.d/load-balanced.conf

upstream backend {
    # Load balancing method (default: round-robin)
    # Other options: least_conn, ip_hash, hash $variable

    least_conn;  # Route to server with least connections

    server app1:3000 weight=3;  # Weighted routing
    server app2:3000 weight=2;
    server app3:3000 weight=1;
    server app4:3000 backup;     # Backup server

    # Health checks
    keepalive 32;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
        proxy_connect_timeout 2s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## SSL/TLS Configuration (Let's Encrypt)

```nginx
# /etc/nginx/conf.d/ssl.conf

server {
    listen 80;
    server_name example.com www.example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # SSL Certificate (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;

    # SSL Session Cache
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Resolver for OCSP
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Caching Configuration

```nginx
# /etc/nginx/conf.d/cached.conf

# Cache path configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=app_cache:10m max_size=1g
                 inactive=60m use_temp_path=off;

upstream backend {
    server app:3000;
}

server {
    listen 80;
    server_name example.com;

    # Cache status header (for debugging)
    add_header X-Cache-Status $upstream_cache_status;

    location / {
        proxy_pass http://backend;

        # Cache configuration
        proxy_cache app_cache;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_valid any 5m;

        # Cache bypass
        proxy_cache_bypass $http_cache_control;
        add_header X-Cache-Status $upstream_cache_status;

        # Proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Static files - aggressive caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://backend;
        proxy_cache app_cache;
        proxy_cache_valid 200 30d;
        expires 30d;
        add_header Cache-Control "public, immutable";
        add_header X-Cache-Status $upstream_cache_status;
    }

    # API - no caching
    location /api/ {
        proxy_pass http://backend;
        proxy_cache_bypass 1;
        proxy_no_cache 1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## Static File Serving with SPA

```nginx
# /etc/nginx/conf.d/spa.conf

server {
    listen 80;
    server_name example.com;

    root /usr/share/nginx/html;
    index index.html;

    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types text/plain text/css application/json application/javascript
               text/xml application/xml application/xml+rss text/javascript;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files with versioning - long cache
    location ~* \.(jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    location ~* \.(css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # index.html and service-worker.js - no cache
    location = /index.html {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        expires 0;
    }

    location = /service-worker.js {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        expires 0;
    }

    # API proxy
    location /api/ {
        proxy_pass http://backend:3000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # SPA routing - fallback to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

## WebSocket Support

```nginx
# /etc/nginx/conf.d/websocket.conf

map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

upstream websocket_backend {
    server app:3000;
}

server {
    listen 80;
    server_name ws.example.com;

    location / {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;

        # WebSocket headers
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        # Standard headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

## Rate Limiting

```nginx
# /etc/nginx/conf.d/rate-limited.conf

# Define rate limit zones
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

# Connection limits
limit_conn_zone $binary_remote_addr zone=addr:10m;

server {
    listen 80;
    server_name example.com;

    # General rate limiting
    location / {
        limit_req zone=general burst=20 nodelay;
        limit_conn addr 10;

        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # API rate limiting
    location /api/ {
        limit_req zone=api burst=50 nodelay;
        limit_req_status 429;

        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Login endpoint - strict rate limiting
    location /api/auth/login {
        limit_req zone=login burst=5 nodelay;
        limit_req_status 429;

        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Multiple Backends (Microservices)

```nginx
# /etc/nginx/conf.d/microservices.conf

upstream user_service {
    server user-service:3001;
}

upstream order_service {
    server order-service:3002;
}

upstream payment_service {
    server payment-service:3003;
}

server {
    listen 80;
    server_name api.example.com;

    # User service
    location /api/users {
        proxy_pass http://user_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Order service
    location /api/orders {
        proxy_pass http://order_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Payment service
    location /api/payments {
        proxy_pass http://payment_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

## Blue-Green Deployment

```nginx
# /etc/nginx/conf.d/blue-green.conf

# Blue environment (current production)
upstream blue {
    server blue-app-1:3000;
    server blue-app-2:3000;
    server blue-app-3:3000;
}

# Green environment (new version)
upstream green {
    server green-app-1:3000;
    server green-app-2:3000;
    server green-app-3:3000;
}

# Active environment (change to switch traffic)
upstream active {
    server blue-app-1:3000;  # Change to green-app-* to switch
    server blue-app-2:3000;
    server blue-app-3:3000;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://active;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Direct access to blue (for testing)
    location /blue/ {
        proxy_pass http://blue/;
        proxy_set_header Host $host;
    }

    # Direct access to green (for testing)
    location /green/ {
        proxy_pass http://green/;
        proxy_set_header Host $host;
    }
}
```

## Canary Deployment

```nginx
# /etc/nginx/conf.d/canary.conf

# Stable version
upstream stable {
    server stable-app-1:3000;
    server stable-app-2:3000;
    server stable-app-3:3000;
}

# Canary version
upstream canary {
    server canary-app:3000;
}

split_clients $remote_addr $backend_pool {
    10%     canary;   # 10% to canary
    *       stable;   # 90% to stable
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://$backend_pool;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Add header to identify backend
        add_header X-Backend-Pool $backend_pool;
    }
}
```

## Monitoring and Logging

```nginx
# /etc/nginx/conf.d/monitored.conf

# Custom log format with timing information
log_format detailed '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

server {
    listen 80;
    server_name example.com;

    access_log /var/log/nginx/access.log detailed;
    error_log /var/log/nginx/error.log warn;

    # Metrics endpoint for Prometheus
    location /metrics {
        access_log off;
        allow 10.0.0.0/8;  # Only internal network
        deny all;
        # Nginx Prometheus exporter would serve here
        proxy_pass http://nginx-exporter:9113/metrics;
    }

    # Status endpoint
    location /nginx_status {
        stub_status on;
        access_log off;
        allow 10.0.0.0/8;
        deny all;
    }

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Track timing
        add_header X-Response-Time $request_time;
    }
}
```

## Best Practices

### 1. Security Headers
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

### 2. Proxy Headers
```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-Port $server_port;
```

### 3. Timeouts
```nginx
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
send_timeout 60s;
```

### 4. Buffer Sizes
```nginx
proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 4k;
proxy_busy_buffers_size 8k;
```

### 5. Client Limits
```nginx
client_max_body_size 10M;
client_body_buffer_size 128k;
client_header_buffer_size 1k;
large_client_header_buffers 4 8k;
```

## Testing Configuration

```bash
# Test configuration syntax
nginx -t

# Reload configuration without downtime
nginx -s reload

# View configuration
nginx -T

# Check which process is listening
netstat -tlnp | grep nginx
```

## Common Issues and Solutions

### 502 Bad Gateway
```nginx
# Increase timeouts
proxy_connect_timeout 600s;
proxy_send_timeout 600s;
proxy_read_timeout 600s;

# Increase buffer size
proxy_buffers 8 16k;
proxy_buffer_size 32k;
```

### 413 Request Entity Too Large
```nginx
client_max_body_size 100M;
```

### Slow Response Times
```nginx
# Enable caching
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g;
proxy_cache my_cache;
```

### WebSocket Connection Drops
```nginx
# Increase timeouts for WebSocket
proxy_read_timeout 3600s;
proxy_send_timeout 3600s;
```
