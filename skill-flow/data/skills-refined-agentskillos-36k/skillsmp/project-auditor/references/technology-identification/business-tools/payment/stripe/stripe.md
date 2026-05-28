# Stripe

**Category**: business-tools/payment
**Description**: Stripe payment processing platform
**Homepage**: https://stripe.com

## Package Detection

### NPM
*Stripe JavaScript SDKs*

- `stripe`
- `@stripe/stripe-js`
- `@stripe/react-stripe-js`

### PYPI
*Stripe Python SDK*

- `stripe`

### GO
*Stripe Go SDK*

- `github.com/stripe/stripe-go`

### MAVEN
*Stripe Java SDK*

- `com.stripe:stripe-java`

### RUBYGEMS
*Stripe Ruby SDK*

- `stripe`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]stripe['"]`

**Pattern**: `require\(['"]stripe['"]\)`

**Pattern**: `from\s+['"]@stripe/`

### Python

**Pattern**: `import\s+stripe`

**Pattern**: `from\s+stripe`

## Environment Variables

- `STRIPE_SECRET_KEY` - Stripe secret API key
- `STRIPE_PUBLISHABLE_KEY` - Stripe publishable key (client-side)
- `STRIPE_WEBHOOK_SECRET` - Webhook signing secret

## Secrets Detection

### API Keys

#### Stripe Live Secret Key
**Pattern**: `sk_live_[0-9a-zA-Z]{24,}`
**Severity**: critical
**Description**: Stripe live mode secret key - provides full access to production payment processing
**Example**: `sk_live_EXAMPLEKEYDONOTUSE00000`
**Environment Variable**: `STRIPE_SECRET_KEY`

#### Stripe Test Secret Key
**Pattern**: `sk_test_[0-9a-zA-Z]{24,}`
**Severity**: medium
**Description**: Stripe test mode secret key - test environment only, but still sensitive
**Example**: `sk_test_EXAMPLEKEYDONOTUSE00000`
**Note**: Test keys can reveal account structure and be used for sandbox testing

#### Stripe Live Publishable Key
**Pattern**: `pk_live_[0-9a-zA-Z]{24,}`
**Severity**: low
**Description**: Stripe live publishable key - intended for client-side use, limited access
**Example**: `pk_live_51xxxxxxxxxxxxxxxxxxxxxx`

#### Stripe Restricted Key
**Pattern**: `rk_live_[0-9a-zA-Z]{24,}`
**Severity**: high
**Description**: Stripe restricted API key - limited permissions, still sensitive
**Example**: `rk_live_EXAMPLEKEYDONOTUSE00000`

#### Stripe Webhook Signing Secret
**Pattern**: `whsec_[A-Za-z0-9]{32,}`
**Severity**: high
**Description**: Webhook signing secret for verifying webhook authenticity
**Example**: `whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
**Environment Variable**: `STRIPE_WEBHOOK_SECRET`

### Validation

#### API Documentation
- **API Reference**: https://stripe.com/docs/api
- **Authentication**: https://stripe.com/docs/api/authentication
- **API Keys**: https://stripe.com/docs/keys
- **Webhooks**: https://stripe.com/docs/webhooks

#### Validation Endpoint
**API**: Stripe Balance API
**Endpoint**: `https://api.stripe.com/v1/balance`
**Method**: GET
**Headers**:
- `Authorization: Bearer <your_secret_key>`
**Purpose**: Validates API key by checking account balance (read-only)

```bash
# Validate Stripe API key
curl -s https://api.stripe.com/v1/balance \
  -u "$STRIPE_SECRET_KEY:"
```

#### Validation Code (Python)
```python
import stripe
from stripe.error import AuthenticationError

def validate_stripe_key(api_key):
    """Validate Stripe API key by fetching balance"""
    try:
        stripe.api_key = api_key
        balance = stripe.Balance.retrieve()
        return {
            'valid': True,
            'livemode': balance.livemode,
            'available': balance.available
        }
    except AuthenticationError as e:
        return {'valid': False, 'error': str(e)}
```

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **Secret Pattern Detection**: 99% (HIGH) - Very distinctive prefixes
