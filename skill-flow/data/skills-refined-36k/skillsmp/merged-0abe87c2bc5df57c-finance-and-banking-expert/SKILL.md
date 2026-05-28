---
name: finance-and-banking-expert
description: Use this skill for expert guidance on financial systems, banking technology, regulatory compliance, and payment processing.
---

# Finance and Banking Expert

Expert guidance for financial systems, banking platforms, regulatory compliance, and payment processing technologies.

## Core Concepts

### Financial and Banking Systems
- Core banking systems (CBS)
- Payment processing (ACH, SWIFT, SEPA)
- Trading platforms
- Risk management
- Regulatory compliance (PCI-DSS, SOX, Basel III, KYC, AML)
- Financial reporting
- Account management
- Loan management

### FinTech and Banking Technology
- Payment gateways (Stripe, PayPal, Square)
- Banking APIs (Plaid, Yodlee)
- Blockchain/crypto
- Open Banking APIs
- Mobile banking
- Digital wallets
- Real-time payment processing
- AI for fraud detection

### Key Challenges
- Security and fraud prevention
- Real-time processing
- High availability (99.999%)
- Regulatory compliance
- Data privacy
- Transaction accuracy

## Payment Processing

```python
# Payment gateway integration (Stripe)
import stripe
from decimal import Decimal

stripe.api_key = "sk_test_..."

class PaymentService:
    def create_payment_intent(self, amount: Decimal, currency: str = "usd"):
        """Create payment intent with idempotency"""
        return stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            payment_method_types=["card"],
            metadata={"order_id": "12345"}
        )

    def process_refund(self, payment_intent_id: str, amount: Decimal = None):
        """Process full or partial refund"""
        return stripe.Refund.create(
            payment_intent=payment_intent_id,
            amount=int(amount * 100) if amount else None
        )
```

## Banking Integration

```python
# Open Banking API integration (Plaid)
from plaid import Client

class BankingService:
    def __init__(self):
        self.client = Client(
            client_id="...",
            secret="...",
            environment="sandbox"
        )

    def create_link_token(self, user_id: str):
        """Create link token for Plaid Link"""
        response = self.client.LinkToken.create({
            "user": {"client_user_id": user_id},
            "client_name": "My App",
            "products": ["auth", "transactions"],
            "country_codes": ["US"],
            "language": "en"
        })
        return response["link_token"]
```

## Financial Calculations

```python
from decimal import Decimal, ROUND_HALF_UP

class FinancialCalculator:
    @staticmethod
    def calculate_interest(principal: Decimal, rate: Decimal, periods: int) -> Decimal:
        """Calculate compound interest"""
        return principal * ((1 + rate) ** periods - 1)

    @staticmethod
    def calculate_loan_payment(principal: Decimal, annual_rate: Decimal, months: int) -> Decimal:
        """Calculate monthly loan payment (amortization)"""
        monthly_rate = annual_rate / 12
        payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
                  ((1 + monthly_rate) ** months - 1)
        return payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
```

## KYC/AML Compliance

```python
class KYCService:
    def verify_customer(self, customer_data: dict) -> dict:
        """Perform KYC verification"""
        verification_results = {
            "identity_verified": False,
            "address_verified": False,
            "sanctions_clear": False,
            "pep_check_clear": False,
            "risk_level": "HIGH"
        }
        # Identity verification and other checks...
        return verification_results
```

## Best Practices

### Security
- Never log sensitive financial data (PAN, CVV)
- Use tokenization for card storage
- Implement strong encryption (AES-256)
- Use TLS 1.2+ for all communications
- Regular security audits

### Data Handling
- Use Decimal type for money (never float)
- Store amounts in smallest currency unit (cents)
- Implement idempotency for all transactions
- Maintain complete audit trails

### Transaction Processing
- Implement two-phase commits
- Use database transactions (ACID)
- Handle network failures gracefully
- Implement retry logic with exponential backoff

## Anti-Patterns

❌ Using float for money calculations  
❌ Storing credit card data unencrypted  
❌ No transaction logging/audit trail  
❌ Ignoring regulatory compliance  
❌ No fraud detection mechanisms  

## Resources

- PCI-DSS: https://www.pcisecuritystandards.org/
- Stripe API: https://stripe.com/docs/api
- Plaid: https://plaid.com/docs/
- Basel Committee: https://www.bis.org/bcbs/
- SWIFT Standards: https://www.swift.com/standards