# Security Guide - Content Management

Guide de sécurité pour la gestion de contenu, les uploads et l'accès aux ressources.

## File Upload Validation

### Type Checking

```yaml
file_validation:
  images:
    allowed_types:
      - image/jpeg
      - image/png
      - image/gif
      - image/webp
      - image/svg+xml
    max_size: 10MB
    magic_bytes_check: true  # Vérifie les bytes, pas juste l'extension

  videos:
    allowed_types:
      - video/mp4
      - video/webm
      - video/quicktime
    max_size: 500MB
    max_duration: 3600  # 1 heure

  documents:
    allowed_types:
      - application/pdf
      - application/msword
      - application/vnd.openxmlformats-officedocument.wordprocessingml.document
    max_size: 50MB

  blocked_extensions:
    - .exe
    - .bat
    - .sh
    - .php
    - .js
    - .html
    - .htm
```

### Magic Bytes Validation

```javascript
// Simple magic bytes for most formats
const MAGIC_BYTES = {
  'image/jpeg': [0xFF, 0xD8, 0xFF],
  'image/png': [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A],
  'image/gif': [0x47, 0x49, 0x46, 0x38],  // GIF8 (GIF87a or GIF89a)
  'application/pdf': [0x25, 0x50, 0x44, 0x46]  // %PDF
};

// WebP requires special handling (RIFF container + WEBP signature)
const WEBP_RIFF = [0x52, 0x49, 0x46, 0x46];  // "RIFF" at offset 0
const WEBP_SIG = [0x57, 0x45, 0x42, 0x50];   // "WEBP" at offset 8

function validateMagicBytes(buffer, expectedType) {
  if (buffer.length < 12) return false;

  // Special case for WebP: check both RIFF header and WEBP signature
  if (expectedType === 'image/webp') {
    const isRIFF = WEBP_RIFF.every((byte, i) => buffer[i] === byte);
    const isWEBP = WEBP_SIG.every((byte, i) => buffer[8 + i] === byte);
    return isRIFF && isWEBP;
  }

  const expected = MAGIC_BYTES[expectedType];
  if (!expected) return false;

  return expected.every((byte, i) => buffer[i] === byte);
}

// Additional validation for AVIF (ISO Base Media File Format)
const AVIF_FTYP = [0x00, 0x00, 0x00];  // Starts with size (variable)
// AVIF has 'ftyp' at offset 4, then 'avif' or 'avis' brand

function validateAVIF(buffer) {
  if (buffer.length < 12) return false;
  const ftyp = String.fromCharCode(...buffer.slice(4, 8));
  if (ftyp !== 'ftyp') return false;
  const brand = String.fromCharCode(...buffer.slice(8, 12));
  return ['avif', 'avis', 'mif1'].includes(brand);
}
```

### Size Limits

| Contexte | Limite | Raison |
|----------|--------|--------|
| Image upload | 10 MB | Performance optimisation |
| Video upload | 500 MB | Transcoding capacity |
| Batch upload | 100 MB total | Memory limits |
| API payload | 5 MB | Request timeout |
| Base64 inline | 100 KB | Page weight |

## Virus Scanning

### Configuration

```yaml
virus_scanning:
  enabled: true
  provider: clamav  # ou: virustotal, crowdstrike

  scan_on:
    - upload
    - before_publish
    - scheduled  # scan quotidien des assets

  actions:
    on_threat:
      - quarantine_file
      - notify_security_team
      - block_user_temporarily
      - log_incident

  exclusions:
    - file_types: [svg]  # Scanné différemment
    - max_size: 100MB    # Files > 100MB scannés async
```

### Quarantine Process

```
┌─────────────────────────────────────────────────────────────┐
│                    QUARANTINE PROCESS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────┐      ┌──────────┐      ┌──────────┐         │
│   │  Upload  │─────►│  Scan    │─────►│ Threat?  │         │
│   └──────────┘      └──────────┘      └────┬─────┘         │
│                                            │                │
│                          ┌─────────────────┼────────────┐   │
│                          ▼                 ▼            │   │
│                     ┌────────┐        ┌────────┐        │   │
│                     │  Yes   │        │   No   │        │   │
│                     └───┬────┘        └───┬────┘        │   │
│                         │                 │             │   │
│                         ▼                 ▼             │   │
│                   ┌──────────┐      ┌──────────┐        │   │
│                   │Quarantine│      │ Process  │        │   │
│                   │ + Alert  │      │ normally │        │   │
│                   └──────────┘      └──────────┘        │   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Content Sanitization

### XSS Prevention

```javascript
const sanitizeConfig = {
  allowedTags: [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'hr',
    'ul', 'ol', 'li',
    'blockquote', 'pre', 'code',
    'a', 'strong', 'em', 'u', 's',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'img', 'figure', 'figcaption'
  ],

  allowedAttributes: {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height', 'loading'],
    'code': ['class'],  // Pour syntax highlighting
    '*': ['id', 'class']
  },

  allowedSchemes: ['http', 'https', 'mailto'],

  // Transformations
  transformTags: {
    'a': (tagName, attribs) => ({
      tagName,
      attribs: {
        ...attribs,
        rel: 'noopener noreferrer',
        target: attribs.target === '_blank' ? '_blank' : undefined
      }
    })
  },

  // Strip dangerous content
  disallowedTagsMode: 'discard',
  allowProtocolRelative: false
};
```

### SVG Sanitization

> **Recommended Libraries**: Use battle-tested libraries for SVG sanitization:
> - [DOMPurify](https://github.com/cure53/DOMPurify) (recommended)
> - [svg-sanitizer](https://github.com/nickcaballero/svg-sanitizer)
> - [sanitize-svg](https://www.npmjs.com/package/@braintree/sanitize-svg)

```javascript
// Using DOMPurify (recommended)
import DOMPurify from 'dompurify';

const sanitizeSVG = (svgContent) => {
  return DOMPurify.sanitize(svgContent, {
    USE_PROFILES: { svg: true, svgFilters: true },
    ADD_TAGS: ['use'],  // If needed for icon systems
    FORBID_TAGS: ['script', 'foreignObject'],
    FORBID_ATTR: ['onclick', 'onerror', 'onload', 'xlink:href'],
  });
};
```

```yaml
svg_sanitization:
  enabled: true
  library: dompurify  # Use proven library, not custom implementation

  remove:
    - script
    - foreignObject
    - use[href^="data:"]
    - use[href^="javascript:"]
    - "*[onclick]"
    - "*[onerror]"
    - "*[onload]"
    - "*[onmouseover]"
    - set  # Can be used for XSS
    - animate[attributeName="href"]

  allowed_elements:
    - svg
    - g
    - path
    - rect
    - circle
    - ellipse
    - line
    - polyline
    - polygon
    - text
    - tspan
    - defs
    - clipPath
    - mask
    - linearGradient
    - radialGradient
    - stop
    - symbol  # For icon systems
    - use     # Only with sanitized href

  allowed_attributes:
    - viewBox
    - width
    - height
    - fill
    - stroke
    - stroke-width
    - d
    - transform
    - class
    - id
    - xmlns
    - xmlns:xlink
    - aria-label
    - aria-hidden
    - role

  # Additional security checks
  post_sanitize:
    - validate_no_external_refs
    - validate_no_data_uris_in_use
    - validate_viewbox_bounds
```

### Markdown Sanitization

```yaml
markdown_sanitization:
  # Désactiver les features dangereuses
  disable:
    - html_inline
    - html_block

  # Valider les liens
  link_validation:
    allowed_protocols: [http, https, mailto]
    validate_external: true
    nofollow_external: true

  # Valider les images
  image_validation:
    allowed_sources:
      - cdn.example.com
      - images.example.com
    require_alt: true
    max_dimensions: [4000, 4000]
```

## API Key Management

### Secret Storage

```yaml
secrets:
  storage: vault  # Options: vault, aws_secrets_manager, env

  rotation:
    enabled: true
    interval: 90d
    notify_before: 14d

  keys:
    translation_api:
      provider: deepl
      env_var: DEEPL_API_KEY
      rotation: 90d

    cdn_api:
      provider: cloudflare
      env_var: CLOUDFLARE_API_TOKEN
      rotation: 180d

    storage_api:
      provider: s3
      use_iam_role: true  # Pas de clé statique
```

### Access Patterns

```yaml
api_access:
  translation_service:
    allowed_ips:
      - internal_vpc
    rate_limit: 1000/hour
    timeout: 30s

  cdn_api:
    authentication: bearer_token
    allowed_operations:
      - purge_cache
      - upload_asset
      - get_analytics
    denied_operations:
      - delete_zone
      - modify_dns
```

## CDN Access Control

### Signed URLs

```javascript
function generateSignedUrl(assetPath, expiresIn = 3600) {
  const expires = Math.floor(Date.now() / 1000) + expiresIn;
  const stringToSign = `${assetPath}${expires}`;
  const signature = crypto
    .createHmac('sha256', CDN_SIGNING_KEY)
    .update(stringToSign)
    .digest('hex');

  return `${CDN_URL}${assetPath}?expires=${expires}&sig=${signature}`;
}

// Usage
const privateAssetUrl = generateSignedUrl('/private/document.pdf', 3600);
```

### Access Policies

```yaml
cdn_access:
  public_assets:
    path: /public/*
    access: public
    cache: aggressive

  protected_assets:
    path: /protected/*
    access: signed_url
    expires: 3600
    cache: private

  private_assets:
    path: /private/*
    access: authenticated
    requires: [valid_session, asset_permission]
    cache: no-store

  admin_assets:
    path: /admin/*
    access: ip_whitelist
    allowed_ips:
      - office_ip
      - vpn_range
```

### CORS Configuration

```yaml
cors:
  allowed_origins:
    - https://www.example.com
    - https://app.example.com
    - https://admin.example.com

  allowed_methods:
    - GET
    - POST
    - PUT
    - DELETE

  allowed_headers:
    - Content-Type
    - Authorization
    - X-Requested-With

  expose_headers:
    - X-Request-Id
    - X-RateLimit-Remaining

  max_age: 86400
  credentials: true
```

## Content Security

### Content Security Policy

> **Security Note**: Avoid `'unsafe-inline'` - use nonces or hashes instead.

```javascript
// Generate CSP nonce per request
import crypto from 'crypto';

function generateCSPNonce() {
  return crypto.randomBytes(16).toString('base64');
}

// Middleware example
app.use((req, res, next) => {
  res.locals.cspNonce = generateCSPNonce();
  res.setHeader('Content-Security-Policy', buildCSP(res.locals.cspNonce));
  next();
});

// In templates: <style nonce="{{cspNonce}}">...</style>
```

```yaml
csp:
  default-src: "'self'"

  script-src:
    - "'self'"
    - "'nonce-{CSP_NONCE}'"  # Dynamic nonce per request
    - "https://cdn.example.com"
    # Fallback for older browsers: use strict-dynamic
    - "'strict-dynamic'"

  style-src:
    - "'self'"
    - "'nonce-{CSP_NONCE}'"  # Use nonce instead of unsafe-inline
    - "https://fonts.googleapis.com"
    # For CMS inline styles, inject with nonce attribute

  img-src:
    - "'self'"
    - "https://cdn.example.com"
    - "https://images.example.com"
    - "data:"  # Pour base64 thumbnails (limited use)
    - "blob:"  # For image previews

  font-src:
    - "'self'"
    - "https://fonts.googleapis.com"
    - "https://fonts.gstatic.com"

  connect-src:
    - "'self'"
    - "https://api.example.com"
    - "https://cdn.example.com"

  media-src:
    - "'self'"
    - "https://cdn.example.com"
    - "blob:"

  frame-ancestors: "'none'"
  base-uri: "'self'"
  form-action: "'self'"
  upgrade-insecure-requests: true

  # Reporting
  report-uri: "/api/csp-report"
  report-to: "csp-endpoint"
```

```yaml
# CSP Reporting endpoint configuration
csp_reporting:
  endpoint: /api/csp-report
  log_level: warning
  alert_threshold: 10  # Alert if >10 violations/hour
  ignore_patterns:
    - browser_extension
    - moz-extension
    - chrome-extension
```

### Permissions Policy

```yaml
permissions_policy:
  camera: ()
  microphone: ()
  geolocation: ()
  payment: ()
  usb: ()
  autoplay: (self)
  fullscreen: (self)
```

## Authentication & Authorization

### Role-Based Access

| Role | Create | Edit | Publish | Delete | Admin |
|------|--------|------|---------|--------|-------|
| Viewer | ❌ | ❌ | ❌ | ❌ | ❌ |
| Contributor | ✅ | Own | ❌ | Own | ❌ |
| Editor | ✅ | ✅ | ❌ | ✅ | ❌ |
| Publisher | ✅ | ✅ | ✅ | ✅ | ❌ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |

### Permission Checks

```javascript
const permissions = {
  'content:create': ['contributor', 'editor', 'publisher', 'admin'],
  'content:edit': ['editor', 'publisher', 'admin'],
  'content:publish': ['publisher', 'admin'],
  'content:delete': ['editor', 'publisher', 'admin'],
  'asset:upload': ['contributor', 'editor', 'publisher', 'admin'],
  'asset:delete': ['editor', 'publisher', 'admin'],
  'settings:manage': ['admin']
};

function checkPermission(user, action) {
  const allowedRoles = permissions[action];
  if (!allowedRoles) return false;
  return allowedRoles.includes(user.role);
}
```

## Audit Logging

### Events à Logger

```yaml
audit_events:
  content:
    - content.created
    - content.updated
    - content.published
    - content.unpublished
    - content.deleted

  assets:
    - asset.uploaded
    - asset.replaced
    - asset.deleted

  access:
    - user.login
    - user.logout
    - user.permission_denied
    - api.rate_limited

  security:
    - file.quarantined
    - content.sanitized
    - suspicious_activity.detected
```

### Log Format

```json
{
  "timestamp": "2025-01-10T14:30:00Z",
  "event": "content.published",
  "actor": {
    "id": "user-123",
    "email": "editor@example.com",
    "role": "publisher",
    "ip": "192.168.1.100"
  },
  "resource": {
    "type": "article",
    "id": "CONTENT-456",
    "title": "Guide SEO 2025"
  },
  "changes": {
    "status": ["approved", "published"],
    "published_at": [null, "2025-01-10T14:30:00Z"]
  },
  "metadata": {
    "request_id": "req-789",
    "user_agent": "Mozilla/5.0...",
    "session_id": "sess-abc"
  }
}
```

## Incident Response

### Classification

| Severity | Description | Response Time | Escalation |
|----------|-------------|---------------|------------|
| P1 | Data breach, malware | Immediate | Security team + Management |
| P2 | Unauthorized access | 1 hour | Security team |
| P3 | Suspicious activity | 4 hours | Ops team |
| P4 | Policy violation | 24 hours | Team lead |

### Response Procedures

```yaml
incident_response:
  malware_detected:
    immediate:
      - isolate_asset
      - block_source_ip
      - notify_security_team
    investigation:
      - analyze_upload_chain
      - check_related_uploads
      - review_user_activity
    remediation:
      - remove_infected_files
      - scan_related_assets
      - update_detection_rules

  unauthorized_access:
    immediate:
      - revoke_session
      - lock_account
      - notify_security
    investigation:
      - review_access_logs
      - identify_compromised_data
      - check_lateral_movement
    remediation:
      - force_password_reset
      - review_permissions
      - implement_additional_controls
```

## Compliance

### GDPR Considerations

| Requirement | Implementation |
|-------------|----------------|
| Data minimization | Only store necessary metadata |
| Right to erasure | Content deletion removes all versions |
| Access logging | All access logged with retention |
| Encryption at rest | AES-256 for stored content |
| Encryption in transit | TLS 1.3 required |

### Data Retention

```yaml
retention:
  published_content: indefinite
  draft_content: 1y
  deleted_content: 30d (soft delete)
  audit_logs: 2y
  access_logs: 90d
  error_logs: 30d
```

## Références

- [SKILL.md](./SKILL.md) - Vue d'ensemble du skill
- [OPERATIONS.md](./OPERATIONS.md) - Guide opérationnel
- [legal-compliance/SKILL.md](../legal-compliance/SKILL.md) - Conformité légale
