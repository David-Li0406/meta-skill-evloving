# Security & Best Practices

Secure WhatsApp Flows with sensitive data handling, authentication, and protection patterns.

## Sensitive Data Handling

### What Is Sensitive Data?

- **Personal Identifiable Information (PII)**: Names, email addresses, phone numbers, SSNs
- **Financial Data**: Credit card numbers, bank accounts, payment tokens
- **Authentication Secrets**: Passwords, API keys, tokens, session IDs
- **Health Information**: Medical history, diagnoses, prescriptions
- **Location Data**: Home/work addresses, GPS coordinates

### Marking Sensitive Fields

Mark fields for masking in server logs:

```json
{
  "type": "TextInput",
  "name": "credit_card",
  "label": "Credit Card Number",
  "input-type": "text",
  "sensitive": true
}
```

**Effect:**
- Flow logs mask this field's value
- Server endpoints should also mask in their logs
- Reduces exposure if logs are compromised

### Best Practices for Sensitive Data

1. **Never display sensitive data on screen** - Don't show full credit cards
   ```json
   // Wrong:
   { "type": "TextBody", "text": "Card: ${form.credit_card}" }

   // Right: Show last 4 digits only
   { "type": "TextBody", "text": "Card ending in ${`${form.credit_card}.substring(${form.credit_card}.length - 4)`}" }
   ```

2. **Transmit only via server** - Send sensitive data through data_exchange, never in navigate payloads
   ```json
   // Wrong: Exposing in navigate
   {
     "action": "navigate",
     "next_screen": "CONFIRM",
     "payload": { "ssn": "${form.ssn}" }
   }

   // Right: Transmit via data_exchange
   {
     "action": "data_exchange",
     "payload": { "ssn": "${form.ssn}" }
   }
   ```

3. **Process server-side** - Never validate or process sensitive data on client
   ```json
   // Wrong: Client validation
   {
     "type": "If",
     "condition": "${`${form.password}.length >= 8`}"
   }

   // Right: Server validation via data_exchange
   {
     "action": "data_exchange",
     "payload": { "password": "${form.password}" }
   }
   ```

4. **Minimal retention** - Delete sensitive data after use
   ```python
   # Server example
   @app.route('/whatsapp/flow', methods=['POST'])
   def handle_flow():
       data = request.json
       ssn = data['data']['data']['ssn']

       # Process immediately
       result = validate_ssn(ssn)

       # Clear variable
       del ssn

       return jsonify({...})
   ```

5. **Audit logging** - Log access to sensitive data
   ```python
   import logging
   logger = logging.getLogger('sensitive_data')

   @app.route('/whatsapp/flow', methods=['POST'])
   def handle_flow():
       data = request.json
       user_id = get_user_from_token(data['flow_token'])

       # Log access, not the data itself
       logger.info(f"User {user_id} accessed sensitive form at {datetime.now()}")

       # Process form...
   ```

---

## HTTPS & Encryption

### HTTPS Requirement

**ALL communication must use HTTPS, never HTTP.**

```json
// Wrong:
{ "src": "http://example.com/image.jpg" }
{ "url": "http://example.com/policy" }

// Right:
{ "src": "https://example.com/image.jpg" }
{ "url": "https://example.com/policy" }
```

**Check every URL in your flow:**
- Image URLs in Image components
- Link URLs in open_url actions
- OptIn policy URLs
- Data endpoint URLs

### Certificate Validation

Use proper SSL/TLS certificates:
```bash
# Test your server's certificate
openssl s_client -connect your-server.com:443

# Check certificate validity
openssl x509 -in your-cert.pem -text -noout
```

### Encryption in Transit

WhatsApp Flows uses TLS 1.2+. Ensure your server:
```python
# Good: Force TLS 1.2+
app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Bad: Allowing old protocols
# Don't do this - it reduces security
```

---

## Authentication & Authorization

### Validating Flow Tokens

Every request includes `flow_token` - validate it:

```python
from flask import request
import json

@app.route('/whatsapp/flow', methods=['POST'])
def handle_flow():
    data = request.json
    flow_token = data['flow_token']
    flow_id = data['flow_id']

    # Verify token is genuine
    if not verify_flow_token(flow_token, flow_id):
        return jsonify({
            'version': '3.0',
            'screen': 'ERROR',
            'errors': {'auth': 'Invalid token'}
        }), 401

    # Process request...
```

### Extracting User Identity

Use flow_token to identify user:

```python
import jwt

def verify_flow_token(token, flow_id):
    try:
        # Decode token (signature verified by WhatsApp)
        decoded = jwt.decode(
            token,
            algorithms=['RS256'],
            options={'verify_signature': False}  # Signature verified server-side
        )

        user_phone = decoded.get('sub')
        return user_phone
    except:
        return None

@app.route('/whatsapp/flow', methods=['POST'])
def handle_flow():
    data = request.json
    user_phone = verify_flow_token(data['flow_token'], data['flow_id'])

    if not user_phone:
        return jsonify({'version': '3.0', 'screen': 'ERROR'}), 401

    # Now you know who this user is
    user = database.find_user(user_phone)
    # ...
```

### Rate Limiting

Prevent abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/whatsapp/flow', methods=['POST'])
@limiter.limit("10 per minute")
def handle_flow():
    # Endpoint is limited to 10 requests per minute per IP
    # ...
```

---

## Input Validation

### Server-Side Validation Is Required

**Never trust client validation alone.** Always validate on server:

```python
import re

@app.route('/whatsapp/flow', methods=['POST'])
def handle_flow():
    data = request.json
    form_data = data['data']['data']

    # Validate email
    email = form_data.get('email', '')
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return jsonify({
            'version': '3.0',
            'screen': 'CURRENT_SCREEN',
            'errors': {'email': 'Invalid email format'}
        })

    # Validate length
    if len(email) > 254:  # RFC 5321
        return jsonify({
            'version': '3.0',
            'screen': 'CURRENT_SCREEN',
            'errors': {'email': 'Email too long'}
        })

    # Validate against business rules
    if is_email_banned(email):
        return jsonify({
            'version': '3.0',
            'screen': 'CURRENT_SCREEN',
            'errors': {'email': 'This email is not allowed'}
        })

    # Valid, proceed
    return jsonify({
        'version': '3.0',
        'screen': 'NEXT_SCREEN'
    })
```

### Sanitizing User Input

Prevent injection attacks:

```python
import html

@app.route('/whatsapp/flow', methods=['POST'])
def handle_flow():
    data = request.json
    user_input = data['data']['data'].get('comment', '')

    # Escape HTML/special characters
    safe_input = html.escape(user_input)

    # If storing in database, use parameterized queries
    cursor.execute(
        "INSERT INTO comments (user_id, text) VALUES (?, ?)",
        (user_id, safe_input)
    )
```

### Length Validation

Enforce character limits:

```python
MAX_LENGTHS = {
    'first_name': 100,
    'email': 254,
    'address': 500,
    'comment': 4096
}

for field, max_length in MAX_LENGTHS.items():
    value = form_data.get(field, '')
    if len(value) > max_length:
        return jsonify({
            'version': '3.0',
            'screen': 'CURRENT_SCREEN',
            'errors': {field: f'Maximum {max_length} characters'}
        })
```

---

## Data Protection

### At Rest

Encrypt data in database:

```python
from cryptography.fernet import Fernet

cipher = Fernet(encryption_key)

# Encrypt before storing
encrypted_data = cipher.encrypt(sensitive_value.encode())
database.store(encrypted_data)

# Decrypt when retrieving
decrypted_data = cipher.decrypt(encrypted_data).decode()
```

### In Transit

Always use HTTPS. Verify with certificate pinning for extra security:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SSLAdapter())
```

### In Logs

Never log sensitive data:

```python
import logging

def sanitize_for_logging(data):
    """Remove sensitive fields before logging"""
    safe_data = data.copy()
    sensitive_fields = ['password', 'ssn', 'credit_card', 'api_key']

    for field in sensitive_fields:
        if field in safe_data:
            safe_data[field] = '[REDACTED]'

    return safe_data

logger.info(f"Processing form: {sanitize_for_logging(form_data)}")
```

---

## GDPR & Privacy Compliance

### Data Minimization

Only collect data you need:

```json
// Wrong: Collect everything
{
  "type": "TextInput",
  "name": "full_history",
  "label": "Tell us your entire history"
}

// Right: Collect only required data
{
  "type": "TextInput",
  "name": "email",
  "label": "Email for order confirmation"
}
```

### User Consent

Get explicit consent for data usage:

```json
{
  "type": "OptIn",
  "name": "marketing_consent",
  "label": "I agree to receive marketing emails",
  "description": "We'll send you weekly deals and product updates",
  "required": true,
  "action-text": "View Privacy Policy",
  "action-url": "https://example.com/privacy"
}
```

### Data Retention

Delete data after retention period:

```python
from datetime import datetime, timedelta

@app.route('/delete-old-submissions', methods=['POST'])
def delete_old_data():
    """Delete form submissions older than 90 days"""
    cutoff_date = datetime.now() - timedelta(days=90)

    deleted = database.delete_where(
        table='form_submissions',
        condition=f'created_at < {cutoff_date}'
    )

    logger.info(f"Deleted {deleted} old submissions")
    return {'deleted': deleted}
```

### Right to Deletion

Allow users to delete their data:

```python
@app.route('/delete-user-data/<user_id>', methods=['POST'])
def delete_user_data(user_id):
    """User requests deletion of all their data"""

    # Verify user identity
    if not verify_user_identity(user_id):
        return {'error': 'Unauthorized'}, 401

    # Delete all their data
    database.delete_user_data(user_id)

    logger.info(f"User {user_id} requested data deletion")
    return {'status': 'deleted'}
```

---

## API Security

### Endpoint Protection

Require authentication:

```python
from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if not verify_api_key(api_key):
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/whatsapp/flow', methods=['POST'])
@require_api_key
def handle_flow():
    # ...
```

### Request Validation

Validate request format:

```python
from jsonschema import validate, ValidationError

REQUEST_SCHEMA = {
    'type': 'object',
    'properties': {
        'flow_id': {'type': 'string'},
        'flow_token': {'type': 'string'},
        'data': {
            'type': 'object',
            'properties': {
                'screen': {'type': 'string'},
                'data': {'type': 'object'}
            },
            'required': ['screen', 'data']
        }
    },
    'required': ['flow_id', 'flow_token', 'data']
}

@app.route('/whatsapp/flow', methods=['POST'])
def handle_flow():
    try:
        validate(instance=request.json, schema=REQUEST_SCHEMA)
    except ValidationError as e:
        return {'error': f'Invalid request: {e.message}'}, 400

    # Process valid request...
```

### Response Security

Don't leak information:

```python
@app.route('/whatsapp/flow', methods=['POST'])
def handle_flow():
    try:
        data = request.json
        screen = data['data']['screen']

        if screen == 'LOGIN':
            result = authenticate_user(data)
            if not result:
                # Don't reveal why login failed
                return jsonify({
                    'version': '3.0',
                    'screen': 'LOGIN_ERROR',
                    'errors': {'auth': 'Invalid credentials'}
                })
    except Exception as e:
        # Don't expose error details to client
        logger.error(f"Server error: {e}")
        return jsonify({
            'version': '3.0',
            'screen': 'ERROR',
            'errors': {'system': 'An error occurred. Please try again.'}
        }), 500
```

---

## Monitoring & Incident Response

### Error Tracking

Monitor for security issues:

```python
import sentry_sdk

sentry_sdk.init("your-sentry-dsn")

@app.route('/whatsapp/flow', methods=['POST'])
def handle_flow():
    try:
        # Process request
        pass
    except Exception as e:
        # Automatically report to Sentry
        sentry_sdk.capture_exception(e)
        return {'error': 'Server error'}, 500
```

### Audit Logging

Log all significant events:

```python
def audit_log(event_type, user_id, details, severity='INFO'):
    """Log security-relevant events"""
    logger.log(
        getattr(logging, severity),
        f"AUDIT [{event_type}] user={user_id} details={details}"
    )

@app.route('/whatsapp/flow', methods=['POST'])
def handle_flow():
    data = request.json
    user_phone = verify_flow_token(data['flow_token'], data['flow_id'])

    screen = data['data']['screen']
    audit_log('FLOW_ACCESS', user_phone, f'screen={screen}')

    # Process...
```

### Security Headers

Include security headers in responses:

```python
@app.after_request
def set_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

---

## Security Checklist

Before deploying:

- [ ] All URLs use HTTPS
- [ ] Sensitive data marked with `sensitive: true`
- [ ] All user input validated server-side
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (HTML escaping)
- [ ] CSRF tokens if needed
- [ ] Rate limiting enabled
- [ ] Flow token validation implemented
- [ ] Sensitive data not logged
- [ ] Error messages don't leak information
- [ ] Data encrypted at rest
- [ ] HTTPS/TLS 1.2+ configured
- [ ] Security headers configured
- [ ] Audit logging implemented
- [ ] Monitoring/alerting set up
- [ ] Data retention policy implemented
- [ ] GDPR compliance verified
- [ ] Access controls verified
- [ ] Third-party dependencies updated
- [ ] Penetration testing completed

---

## Common Security Mistakes

### Exposing Sensitive Data in Global References

```json
// Wrong: Credit card visible on review screen
{
  "type": "TextBody",
  "text": "Card: ${screen.PAYMENT.form.card_number}"
}

// Right: Show masked version
{
  "type": "TextBody",
  "text": "Card: ••••••••••••${`${screen.PAYMENT.form.card_number}.substring(12)`}"
}
```

### Client-Side Validation Only

```json
// Wrong: Only client validation
{
  "type": "If",
  "condition": "${`${form.age} >= 18`}"
}

// Right: Server validation via data_exchange
{
  "action": "data_exchange",
  "payload": { "age": "${form.age}" }
}
```

### Hardcoding Secrets

```python
# Wrong:
API_KEY = "sk-12345abcde"

# Right:
import os
API_KEY = os.environ.get('WHATSAPP_API_KEY')
```

### Not Sanitizing User Input

```python
# Wrong:
message = form_data['comment']
database.execute(f"INSERT INTO comments VALUES ('{message}')")

# Right:
message = form_data['comment']
cursor.execute(
    "INSERT INTO comments VALUES (?)",
    (message,)
)
```

### Logging Sensitive Data

```python
# Wrong:
logger.info(f"User submitted: {form_data}")

# Right:
safe_data = {k: v for k, v in form_data.items() if k not in ['password', 'ssn']}
logger.info(f"User submitted form: {safe_data}")
```

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [GDPR Compliance](https://gdpr-info.eu/)
- [WhatsApp Business Security](https://developers.facebook.com/docs/whatsapp/security/)
