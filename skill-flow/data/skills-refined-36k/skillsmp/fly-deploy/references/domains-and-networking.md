# Custom Domains and Networking

## Default fly.dev Domain

Every app gets a free `.fly.dev` subdomain:

```
https://<app-name>.fly.dev
```

This works immediately after deployment with automatic HTTPS via Let's Encrypt.

---

## Adding a Custom Domain

### Step 1: Add Certificate

```bash
# Add domain to your app
fly certs add example.com

# Add subdomain
fly certs add www.example.com

# Add wildcard (requires DNS challenge)
fly certs add *.example.com
```

This command:
1. Registers the domain with your app
2. Shows DNS configuration options
3. Prepares for automatic SSL certificate generation

### Step 2: Configure DNS

After running `fly certs add`, you'll see DNS instructions:

**Option A: A and AAAA Records (Recommended)**

Get your app's IP addresses:
```bash
fly ips list
```

Configure DNS with your provider:
```
A     @     213.188.195.131        (IPv4)
AAAA  @     2a09:8280:1::1:2f3a    (IPv6)
```

**Option B: CNAME Record (Subdomains)**

For `www.example.com`:
```
CNAME  www   <app-name>.fly.dev
```

**Important for apex domains (example.com):**
- Most DNS providers don't allow CNAME on apex domains
- Use A and AAAA records instead
- Or use ALIAS/ANAME if your DNS provider supports it (Cloudflare, DNSimple)

### Step 3: Verify Certificate

Check certificate status:
```bash
fly certs show example.com
```

Output shows:
- Certificate status (issued, pending, failed)
- Validation method used
- Expiration date
- Domain verification status

**Certificate validation happens automatically** via:
1. **TLS-ALPN** (preferred, ~30 seconds)
2. **HTTP-01** (fallback, ~1-2 minutes)
3. **DNS-01** (manual, for wildcards)

### Step 4: Test

```bash
# Test your domain
curl https://example.com

# Check SSL certificate
curl -vI https://example.com 2>&1 | grep -A 5 "SSL"
```

---

## Multiple Domains

Add multiple domains to the same app:

```bash
fly certs add example.com
fly certs add www.example.com
fly certs add app.example.com
```

All domains will serve the same application.

**Redirect www to apex (or vice versa):**

Handle redirects in your application code:

```js
// Express.js
app.use((req, res, next) => {
  if (req.hostname === 'www.example.com') {
    return res.redirect(301, `https://example.com${req.url}`)
  }
  next()
})
```

```python
# FastAPI
from fastapi import Request
from fastapi.responses import RedirectResponse

@app.middleware("http")
async def redirect_www(request: Request, call_next):
    if request.url.hostname == "www.example.com":
        url = str(request.url).replace("www.example.com", "example.com")
        return RedirectResponse(url=url, status_code=301)
    return await call_next(request)
```

---

## Wildcard Certificates

For `*.example.com` (all subdomains):

```bash
fly certs add *.example.com
```

**Requires DNS-01 challenge:**

1. Run the command
2. Add TXT record shown:
   ```
   _acme-challenge.example.com  TXT  "abc123..."
   ```
3. Wait for DNS propagation (can take up to 48 hours, usually minutes)
4. Certificate issues automatically

**Verify DNS propagation:**
```bash
dig TXT _acme-challenge.example.com
# or
nslookup -type=TXT _acme-challenge.example.com
```

---

## Using Cloudflare

### Full SSL (Recommended)

Cloudflare settings:
- SSL/TLS → Full (strict)
- Always Use HTTPS → On
- Automatic HTTPS Rewrites → On

DNS configuration:
```
AAAA  @  2a09:8280:1::1:2f3a  (Proxied - orange cloud)
```

**Why only AAAA (IPv6)?**
- Cloudflare requires IPv6 for certificate validation
- IPv4 can be added after certificate issues

### Certificate Generation with Cloudflare

**Option 1: Proxy disabled (gray cloud)**
- Fastest, works with A/AAAA records
- No Cloudflare features (CDN, firewall)

**Option 2: Proxy enabled (orange cloud)**
- Use AAAA record only initially
- Add A record after certificate issues
- Full Cloudflare features available

---

## SSL/TLS Configuration

### Automatic HTTPS

fly.io automatically:
- Provisions Let's Encrypt certificates
- Renews certificates before expiration
- Redirects HTTP → HTTPS (if configured)

### Force HTTPS in fly.toml

```toml
[http_service]
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
```

This redirects all HTTP traffic to HTTPS.

### Custom SSL Certificates

For custom/purchased SSL certificates:

```bash
# Not commonly needed - Let's Encrypt is automatic
# Contact support for enterprise custom certificate needs
```

---

## DNS Providers

### Common Providers Configuration

**Cloudflare:**
```
Type: AAAA
Name: @
Content: 2a09:8280:1::1:2f3a
Proxy: Enabled (orange cloud)
```

**Namecheap:**
```
Type: AAAA
Host: @
Value: 2a09:8280:1::1:2f3a
TTL: Automatic
```

**Google Domains:**
```
Type: AAAA
Name: @
Data: 2a09:8280:1::1:2f3a
```

**Route 53 (AWS):**
```
Type: AAAA
Name: example.com
Value: 2a09:8280:1::1:2f3a
Routing Policy: Simple
```

---

## Managing Certificates

### List Certificates

```bash
fly certs list
```

Shows all certificates for your app.

### Check Certificate Details

```bash
fly certs show example.com
```

Output includes:
- Hostname
- DNS validation status
- Certificate status
- Issued date
- Expires date

### Remove Certificate

```bash
fly certs delete example.com
```

Removes the certificate and stops serving that domain.

---

## Rate Limits

Let's Encrypt has rate limits:
- **50 certificates per domain per week**
- **5 duplicate certificates per week**
- **5 failed validations per hostname per hour**

**Best practices:**
- Don't repeatedly delete and recreate certificates
- Use staging domain for testing
- Wait for DNS propagation before adding certificate

**Exceeded rate limit?**
- Wait for the weekly window to reset
- Use different subdomain
- Contact Let's Encrypt support for rate limit increase

---

## Networking Features

### Private Networking

Apps on the same fly.io organization can communicate over private network:

**Internal DNS:**
```
<app-name>.internal
```

**Example:**
```js
// API app connecting to database app
const DB_HOST = 'my-postgres.internal'
const DB_PORT = 5432
```

**In fly.toml:**
```toml
[env]
  DATABASE_URL = "postgresql://user:pass@my-postgres.internal:5432/db"
```

### IPv6 and IPv4

fly.io provides:
- **IPv6:** Free, automatic
- **IPv4:** Requires allocation

**Allocate dedicated IPv4:**
```bash
fly ips allocate-v4
```

**Check IPs:**
```bash
fly ips list
```

**Why IPv4?**
- Some legacy systems only support IPv4
- Some DNS providers require it
- Most modern apps work fine with IPv6 only

### Regions

List available regions:
```bash
fly regions list
```

Add regions to your app:
```bash
fly regions add iad lhr
```

DNS automatically routes users to nearest region.

---

## Troubleshooting Domains

### Certificate Won't Issue

**Check DNS propagation:**
```bash
dig example.com
dig AAAA example.com
```

Should return fly.io IP addresses.

**Check certificate status:**
```bash
fly certs show example.com
```

Look for validation errors.

**Common issues:**
1. **DNS not propagated** - Wait 5-60 minutes
2. **Wrong IP addresses** - Verify A/AAAA records match `fly ips list`
3. **CAA records** - Ensure CAA allows Let's Encrypt: `letsencrypt.org`
4. **Cloudflare full proxy** - Use AAAA record, not A

### Domain Shows "Not Found"

**Check app is deployed:**
```bash
fly status
```

**Check domain is added:**
```bash
fly certs list
```

**Check DNS points to correct IPs:**
```bash
dig example.com
```

### Certificate Expired

**Shouldn't happen** - Certificates auto-renew.

If it does:
```bash
# Delete and recreate certificate
fly certs delete example.com
fly certs add example.com
```

### Redirect Loop

**Check force_https configuration:**

```toml
[http_service]
  force_https = true
```

**If using Cloudflare:**
- Set SSL to "Full" or "Full (strict)"
- Don't use "Flexible" SSL mode

---

## Advanced Configuration

### Custom Headers

Add security headers in your app:

```js
// Express
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
  res.setHeader('X-Frame-Options', 'DENY')
  res.setHeader('X-Content-Type-Options', 'nosniff')
  next()
})
```

### Health Checks for Multiple Domains

```toml
[[http_service.checks]]
  path = "/health"
  headers = { Host = "example.com" }
```

### Path-Based Routing

Handle different domains in your app:

```js
app.use((req, res, next) => {
  if (req.hostname === 'api.example.com') {
    // API routes
  } else if (req.hostname === 'admin.example.com') {
    // Admin routes
  } else {
    // Main app routes
  }
  next()
})
```

---

## Quick Reference

```bash
# Add domain
fly certs add example.com

# Check certificate
fly certs show example.com

# List all certificates
fly certs list

# Get IP addresses
fly ips list

# Remove domain
fly certs delete example.com

# Test domain
curl -I https://example.com
```

**Typical timeline:**
1. Run `fly certs add` - Instant
2. Configure DNS - 5-15 minutes
3. Certificate issues - 1-5 minutes after DNS propagates
4. **Total:** 10-30 minutes for new domain
