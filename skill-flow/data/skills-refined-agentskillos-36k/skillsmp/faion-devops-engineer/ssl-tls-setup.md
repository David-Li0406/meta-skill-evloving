---
id: ssl-tls-setup
name: "SSL/TLS Setup"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# SSL/TLS Setup

## Overview

SSL/TLS (Secure Sockets Layer/Transport Layer Security) provides encryption and authentication for network communications. This methodology covers certificate management, configuration best practices, and implementation across various platforms.

## When to Use

- Securing web applications with HTTPS
- Protecting API communications
- Implementing mutual TLS (mTLS) for service-to-service auth
- Meeting compliance requirements (PCI-DSS, HIPAA)
- Securing internal services

## Process/Steps

### 1. TLS Fundamentals

**TLS Versions:**
| Version | Status | Notes |
|---------|--------|-------|
| TLS 1.0 | Deprecated | Do not use |
| TLS 1.1 | Deprecated | Do not use |
| TLS 1.2 | Supported | Minimum recommended |
| TLS 1.3 | Preferred | Best performance and security |

**Certificate Types:**
```yaml
certificate_types:
  domain_validated:
    validation: "Domain ownership"
    trust_level: "Basic"
    use_case: "Blogs, personal sites"
    issuance_time: "Minutes"

  organization_validated:
    validation: "Domain + organization"
    trust_level: "Medium"
    use_case: "Business websites"
    issuance_time: "1-3 days"

  extended_validation:
    validation: "Domain + organization + legal"
    trust_level: "High"
    use_case: "E-commerce, banking"
    issuance_time: "1-5 days"

  wildcard:
    validation: "Covers subdomains"
    example: "*.example.com"
    use_case: "Multiple subdomains"

  multi_domain:
    validation: "Multiple domains (SAN)"
    example: "example.com, example.org"
    use_case: "Related domains"
```

### 2. Let's Encrypt with Certbot

**Installation:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo dnf install certbot python3-certbot-nginx
```

**Certificate Generation:**
```bash
# Nginx automatic
sudo certbot --nginx -d example.com -d www.example.com

# Standalone (if web server not running)
sudo certbot certonly --standalone -d example.com

# Webroot (existing web server)
sudo certbot certonly --webroot -w /var/www/html -d example.com

# DNS challenge (for wildcard)
sudo certbot certonly --manual --preferred-challenges=dns -d "*.example.com"

# Non-interactive
sudo certbot certonly --nginx \
  --non-interactive \
  --agree-tos \
  --email admin@example.com \
  -d example.com
```

**Certificate Locations:**
```
/etc/letsencrypt/live/example.com/
├── cert.pem       # Server certificate
├── chain.pem      # Intermediate certificates
├── fullchain.pem  # cert.pem + chain.pem
├── privkey.pem    # Private key
└── README
```

**Auto-Renewal:**
```bash
# Test renewal
sudo certbot renew --dry-run

# Renewal cron (usually auto-installed)
0 0,12 * * * /usr/bin/certbot renew --quiet

# Systemd timer (preferred)
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### 3. Self-Signed Certificates

**Generate Self-Signed Certificate:**
```bash
# Generate private key and certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/selfsigned.key \
  -out /etc/ssl/certs/selfsigned.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=example.com"

# Generate with SAN (Subject Alternative Names)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/selfsigned.key \
  -out /etc/ssl/certs/selfsigned.crt \
  -subj "/CN=example.com" \
  -addext "subjectAltName=DNS:example.com,DNS:*.example.com,IP:10.0.0.1"
```

**Generate CA and Sign Certificates:**
```bash
# Create CA private key
openssl genrsa -out ca.key 4096

# Create CA certificate
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 \
  -out ca.crt -subj "/CN=My CA"

# Create server private key
openssl genrsa -out server.key 2048

# Create CSR
openssl req -new -key server.key -out server.csr \
  -subj "/CN=example.com"

# Sign with CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt -days 365 -sha256 \
  -extfile <(printf "subjectAltName=DNS:example.com,DNS:*.example.com")
```

### 4. Nginx SSL Configuration

**Modern Configuration:**
```nginx
# /etc/nginx/snippets/ssl-params.conf

# Protocols
ssl_protocols TLSv1.2 TLSv1.3;

# Ciphers (TLS 1.2)
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;

# TLS 1.3 ciphers (automatic, but can be set)
# ssl_conf_command Ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256;

# Session
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# DH parameters (generate: openssl dhparam -out /etc/nginx/dhparam.pem 2048)
ssl_dhparam /etc/nginx/dhparam.pem;

# HSTS
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

**Server Block:**
```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### 5. Apache SSL Configuration

```apache
# /etc/apache2/sites-available/example.com-ssl.conf

<VirtualHost *:80>
    ServerName example.com
    Redirect permanent / https://example.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName example.com
    DocumentRoot /var/www/example.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem

    # Protocols
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1

    # Ciphers
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off

    # HSTS
    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"

    # OCSP Stapling
    SSLUseStapling on
    SSLStaplingResponderTimeout 5
    SSLStaplingReturnResponderErrors off

    <Directory /var/www/example.com>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>

# Stapling cache (outside VirtualHost)
SSLStaplingCache shmcb:/var/run/ocsp(128000)
```

### 6. Mutual TLS (mTLS)

**Nginx mTLS Configuration:**
```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;

    # Server certificate
    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;

    # Client certificate verification
    ssl_client_certificate /etc/nginx/ssl/ca.crt;
    ssl_verify_client on;
    ssl_verify_depth 2;

    # Pass client cert info to backend
    location / {
        proxy_pass http://backend;
        proxy_set_header X-SSL-Client-Cert $ssl_client_cert;
        proxy_set_header X-SSL-Client-DN $ssl_client_s_dn;
        proxy_set_header X-SSL-Client-Verify $ssl_client_verify;
    }
}
```

**Generate Client Certificate:**
```bash
# Create client key
openssl genrsa -out client.key 2048

# Create CSR
openssl req -new -key client.key -out client.csr \
  -subj "/CN=client1/O=MyOrg"

# Sign with CA
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out client.crt -days 365 -sha256

# Create PKCS12 bundle (for browser import)
openssl pkcs12 -export -out client.p12 \
  -inkey client.key -in client.crt -certfile ca.crt

# Test connection
curl --cert client.crt --key client.key \
  --cacert ca.crt https://api.example.com/
```

### 7. Certificate Verification

**Check Certificate Details:**
```bash
# View certificate
openssl x509 -in cert.pem -text -noout

# Check expiration
openssl x509 -in cert.pem -enddate -noout

# Verify certificate chain
openssl verify -CAfile ca.crt server.crt

# Check remote certificate
openssl s_client -connect example.com:443 -servername example.com

# Check certificate with specific TLS version
openssl s_client -connect example.com:443 -tls1_3

# Get certificate expiration from remote
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -dates
```

**SSL Labs Testing:**
```bash
# Command line test (using API)
curl "https://api.ssllabs.com/api/v3/analyze?host=example.com&publish=off&all=done"

# Or use: https://www.ssllabs.com/ssltest/
```

### 8. Kubernetes TLS

**TLS Secret:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: example-tls
  namespace: default
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-cert>
  tls.key: <base64-encoded-key>

# Create from files:
# kubectl create secret tls example-tls \
#   --cert=server.crt --key=server.key
```

**Ingress with TLS:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - example.com
        - www.example.com
      secretName: example-tls
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
```

**Cert-Manager (Automatic Certificates):**
```yaml
# ClusterIssuer for Let's Encrypt
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx

---
# Certificate request
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-cert
  namespace: default
spec:
  secretName: example-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: example.com
  dnsNames:
    - example.com
    - www.example.com
```

## Best Practices

### Certificate Management
1. **Automate renewal** - Never let certs expire
2. **Monitor expiration** - Alert before expiry
3. **Use short-lived certs** - 90 days max
4. **Secure private keys** - Proper permissions

### Configuration
1. **TLS 1.2 minimum** - Disable older versions
2. **Strong ciphers** - Follow Mozilla recommendations
3. **Enable HSTS** - Prevent downgrade attacks
4. **OCSP stapling** - Faster verification

### Security
1. **Certificate Transparency** - Monitor for rogue certs
2. **CAA records** - Restrict CA issuance
3. **Key rotation** - Regular key changes
4. **Revocation handling** - Plan for compromised keys

### Monitoring
1. **Certificate expiry alerts** - 30, 14, 7 days
2. **SSL Labs grade** - Maintain A+ rating
3. **CT log monitoring** - Detect unauthorized certs
4. **Protocol version monitoring** - Track TLS versions in use

## Templates/Examples

### Certificate Monitoring Script

```bash
#!/bin/bash
# check_ssl_expiry.sh

DOMAINS=("example.com" "api.example.com" "www.example.com")
ALERT_DAYS=30

for domain in "${DOMAINS[@]}"; do
    expiry_date=$(echo | openssl s_client -connect "$domain:443" -servername "$domain" 2>/dev/null | \
        openssl x509 -noout -enddate | cut -d= -f2)

    expiry_epoch=$(date -d "$expiry_date" +%s)
    current_epoch=$(date +%s)
    days_left=$(( (expiry_epoch - current_epoch) / 86400 ))

    if [ $days_left -lt $ALERT_DAYS ]; then
        echo "WARNING: $domain certificate expires in $days_left days"
        # Send alert here
    else
        echo "OK: $domain certificate valid for $days_left days"
    fi
done
```

### DNS CAA Record

```
# DNS records to restrict certificate issuance
example.com.  IN  CAA  0  issue "letsencrypt.org"
example.com.  IN  CAA  0  issuewild "letsencrypt.org"
example.com.  IN  CAA  0  iodef "mailto:security@example.com"
```

## References

- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [SSL Labs](https://www.ssllabs.com/)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [OpenSSL Documentation](https://www.openssl.org/docs/)
