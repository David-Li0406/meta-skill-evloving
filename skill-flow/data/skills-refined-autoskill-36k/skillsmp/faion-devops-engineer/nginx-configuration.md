---
id: nginx-configuration
name: "Nginx Configuration"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Nginx Configuration

## Overview

Nginx is a high-performance HTTP server, reverse proxy, and load balancer. This methodology covers configuration patterns for web serving, reverse proxy setups, SSL/TLS termination, caching, and security hardening.

## When to Use

- Setting up web servers for static or dynamic content
- Configuring reverse proxy for backend services
- Implementing SSL/TLS termination
- Setting up load balancing
- Optimizing web application performance
- Implementing security headers and access controls

## Process/Steps

### 1. Directory Structure

```
/etc/nginx/
├── nginx.conf              # Main configuration
├── mime.types              # MIME type definitions
├── conf.d/                 # Additional configurations
│   └── default.conf
├── sites-available/        # Available site configs
│   ├── example.com
│   └── api.example.com
├── sites-enabled/          # Enabled sites (symlinks)
│   └── example.com -> ../sites-available/example.com
├── snippets/               # Reusable config snippets
│   ├── ssl-params.conf
│   ├── security-headers.conf
│   └── proxy-params.conf
└── ssl/                    # SSL certificates
    ├── example.com.crt
    └── example.com.key
```

### 2. Main Configuration

```nginx
# /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log warn;

# Load modules
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    # Basic Settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    # MIME Types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    log_format json escape=json '{'
        '"time": "$time_iso8601",'
        '"remote_addr": "$remote_addr",'
        '"request_method": "$request_method",'
        '"request_uri": "$request_uri",'
        '"status": $status,'
        '"body_bytes_sent": $body_bytes_sent,'
        '"request_time": $request_time,'
        '"upstream_response_time": "$upstream_response_time",'
        '"http_referrer": "$http_referer",'
        '"http_user_agent": "$http_user_agent"'
    '}';

    access_log /var/log/nginx/access.log main;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 256;
    gzip_types
        application/atom+xml
        application/javascript
        application/json
        application/rss+xml
        application/vnd.ms-fontobject
        application/x-font-ttf
        application/x-web-app-manifest+json
        application/xhtml+xml
        application/xml
        font/opentype
        image/svg+xml
        image/x-icon
        text/css
        text/plain
        text/x-component;

    # SSL Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
    limit_conn_zone $binary_remote_addr zone=addr:10m;

    # Upstream Backends
    include /etc/nginx/conf.d/upstreams/*.conf;

    # Virtual Hosts
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### 3. Static Site Configuration

```nginx
# /etc/nginx/sites-available/example.com

server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com www.example.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    # Security Headers
    include /etc/nginx/snippets/security-headers.conf;

    # Root Directory
    root /var/www/example.com/public;
    index index.html index.htm;

    # Logging
    access_log /var/log/nginx/example.com.access.log main;
    error_log /var/log/nginx/example.com.error.log warn;

    # Locations
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Static Assets Caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

### 4. Reverse Proxy Configuration

```nginx
# /etc/nginx/sites-available/api.example.com

# Upstream definition
upstream api_backend {
    least_conn;
    server 127.0.0.1:8000 weight=5;
    server 127.0.0.1:8001 weight=5;
    server 127.0.0.1:8002 backup;

    keepalive 32;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.example.com;

    # SSL
    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    # Security Headers
    include /etc/nginx/snippets/security-headers.conf;

    # Logging
    access_log /var/log/nginx/api.example.com.access.log json;
    error_log /var/log/nginx/api.example.com.error.log warn;

    # Rate Limiting
    limit_req zone=api burst=50 nodelay;
    limit_conn addr 100;

    # Proxy Settings
    location / {
        proxy_pass http://api_backend;
        include /etc/nginx/snippets/proxy-params.conf;
    }

    # Health Check Endpoint
    location /health {
        proxy_pass http://api_backend/health;
        access_log off;
    }

    # WebSocket Support
    location /ws {
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

### 5. Configuration Snippets

**SSL Parameters:**
```nginx
# /etc/nginx/snippets/ssl-params.conf

ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;

ssl_session_cache shared:SSL:10m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# DH Parameters
ssl_dhparam /etc/nginx/ssl/dhparam.pem;
```

**Security Headers:**
```nginx
# /etc/nginx/snippets/security-headers.conf

# HSTS
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# Content Security Policy
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://api.example.com; frame-ancestors 'none';" always;

# XSS Protection
add_header X-XSS-Protection "1; mode=block" always;

# Content Type Options
add_header X-Content-Type-Options "nosniff" always;

# Frame Options
add_header X-Frame-Options "DENY" always;

# Referrer Policy
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Permissions Policy
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

**Proxy Parameters:**
```nginx
# /etc/nginx/snippets/proxy-params.conf

proxy_http_version 1.1;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-Port $server_port;
proxy_set_header Connection "";

# Timeouts
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;

# Buffering
proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 16k;
proxy_busy_buffers_size 24k;

# Error handling
proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
proxy_next_upstream_tries 3;
```

### 6. Load Balancing

```nginx
# Round Robin (default)
upstream backend_rr {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080;
}

# Least Connections
upstream backend_lc {
    least_conn;
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080;
}

# IP Hash (sticky sessions)
upstream backend_ip {
    ip_hash;
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080;
}

# Weighted
upstream backend_weighted {
    server 10.0.0.1:8080 weight=5;
    server 10.0.0.2:8080 weight=3;
    server 10.0.0.3:8080 weight=2;
}

# Health Checks (nginx plus or open source with module)
upstream backend_health {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080;

    # Passive health checks
    server 10.0.0.1:8080 max_fails=3 fail_timeout=30s;
}
```

### 7. Caching Configuration

```nginx
# Cache zone definition (in http block)
proxy_cache_path /var/cache/nginx/api
    levels=1:2
    keys_zone=api_cache:10m
    max_size=1g
    inactive=60m
    use_temp_path=off;

# Caching in server/location
location /api {
    proxy_pass http://api_backend;

    # Enable caching
    proxy_cache api_cache;
    proxy_cache_key "$scheme$request_method$host$request_uri";
    proxy_cache_valid 200 10m;
    proxy_cache_valid 404 1m;
    proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
    proxy_cache_background_update on;
    proxy_cache_lock on;

    # Cache headers
    add_header X-Cache-Status $upstream_cache_status;

    # Bypass cache
    proxy_cache_bypass $http_cache_control;
    proxy_no_cache $http_pragma $http_authorization;
}
```

## Best Practices

### Performance
1. **Enable gzip** - Compress responses
2. **Use keepalive** - Reduce connection overhead
3. **Buffer tuning** - Match to response sizes
4. **Worker processes** - Match CPU cores

### Security
1. **Hide version** - server_tokens off
2. **Use HTTPS** - TLS 1.2+ only
3. **Security headers** - HSTS, CSP, X-Frame-Options
4. **Rate limiting** - Prevent abuse

### Configuration
1. **Use includes** - Modular configuration
2. **Snippets for reuse** - DRY principle
3. **Test before reload** - nginx -t
4. **Version control** - Track changes

### Monitoring
1. **Access logs** - JSON format for parsing
2. **Error logs** - Monitor for issues
3. **Stub status** - Basic metrics
4. **Real-time monitoring** - Prometheus exporter

## Templates/Examples

### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renewal test
sudo certbot renew --dry-run

# Cron for renewal
0 0,12 * * * /usr/bin/certbot renew --quiet
```

### Configuration Testing

```bash
# Test configuration syntax
sudo nginx -t

# Test configuration and show parsed result
sudo nginx -T

# Reload configuration
sudo nginx -s reload

# Check running config
nginx -V 2>&1 | grep -o -- '--[^ ]*'
```

### Performance Testing

```bash
# Basic benchmark with ab
ab -n 10000 -c 100 https://example.com/

# wrk benchmark
wrk -t12 -c400 -d30s https://example.com/

# Check open connections
ss -s
netstat -an | grep :80 | wc -l
```

### Monitoring Endpoint

```nginx
# Status endpoint for monitoring
location /nginx_status {
    stub_status on;
    allow 127.0.0.1;
    allow 10.0.0.0/8;
    deny all;
}

# Output:
# Active connections: 291
# server accepts handled requests
#  16630948 16630948 31070465
# Reading: 6 Writing: 179 Waiting: 106
```

## References

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Nginx Admin Guide](https://docs.nginx.com/nginx/admin-guide/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Nginx Best Practices](https://www.nginx.com/resources/wiki/start/)
- [Digital Ocean Nginx Tutorials](https://www.digitalocean.com/community/tags/nginx)
