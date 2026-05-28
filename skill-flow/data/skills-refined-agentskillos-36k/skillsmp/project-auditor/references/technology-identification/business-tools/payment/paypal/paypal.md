# PayPal

**Category**: business-tools/payment
**Description**: PayPal payment processing
**Homepage**: https://developer.paypal.com

## Package Detection

### NPM
*PayPal Node.js SDKs*

- `@paypal/checkout-server-sdk`
- `@paypal/paypal-js`
- `@paypal/react-paypal-js`

### PYPI
*PayPal Python SDKs*

- `paypalrestsdk`
- `paypal-checkout-serversdk`

### RUBYGEMS
*PayPal Ruby SDK*

- `paypal-sdk-rest`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@paypal/`
- Type: esm_import

### Python

**Pattern**: `import\s+paypalrestsdk`
- Type: python_import

## Environment Variables


## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
