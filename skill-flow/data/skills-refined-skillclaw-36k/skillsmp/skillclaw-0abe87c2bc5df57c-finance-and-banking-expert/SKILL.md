---
name: finance-and-banking-expert
description: Use this skill when you need expert guidance on financial systems, banking technology, and regulatory compliance in the finance sector.
---

# Skill body

## Core Concepts

### Financial and Banking Systems
- Core banking systems (CBS)
- Payment processing (ACH, SWIFT, SEPA)
- Trading platforms
- Risk management
- Regulatory compliance (PCI-DSS, SOX, Basel III, KYC, AML, GDPR, PSD2)
- Financial reporting
- Loan management
- Account management

### FinTech and Banking Technology Stack
- Payment gateways (Stripe, PayPal, Square)
- Banking APIs (Plaid, Yodlee)
- Blockchain/crypto
- Open Banking APIs
- Mobile banking
- Digital wallets
- AI for fraud detection

### Key Challenges
- Security and fraud prevention
- Real-time processing
- High availability (99.999%)
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

    def handle_webhook(self, payload: str, signature: str):
        """Handle Stripe webhook events"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )

            if event.type == "payment_intent.succeeded":
                payment_intent = event.data.object
                self.handle_successful_payment(payment_intent)
            elif event.type == "payment_intent.payment_failed":
                payment_intent = event.data.object
                self.handle_failed_payment(payment_intent)

            return {"status": "success"}
        except ValueError:
            return {"status": "invalid_payload"}
```

## Account Management

```python
from decimal import Decimal
from datetime import datetime
from enum import Enum

class AccountType(Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"
    LOAN = "loan"

class Account:
    def __init__(self, account_number: str, account_type: AccountType,
                 customer_id: str, balance: Decimal = Decimal('0')):
        self.account_number = account_number
        self.type = account_type
        self.customer_id = customer_id
        self.balance = balance
        self.status = "ACTIVE"
        self.created_at = datetime.now()

    def deposit(self, amount: Decimal) -> dict:
        """Deposit funds with validation"""
        if amount <= 0:
            raise ValueError("Amount must be positive")

        self.balance += amount

        return {
            "transaction_id": self.generate_transaction_id(),
            "type": "DEPOSIT",
            "amount": amount,
            "balance": self.balance,
            "timestamp": datetime.now()
        }

    def withdraw(self, amount: Decimal) -> dict:
        """Withdraw funds with balance check"""
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if self.balance < amount:
            raise ValueError("Insufficient funds")

        self.balance -= amount

        return {
            "transaction_id": self.generate_transaction_id(),
            "type": "WITHDRAWAL",
            "amount": amount,
            "balance": self.balance,
            "timestamp": datetime.now()
        }
```