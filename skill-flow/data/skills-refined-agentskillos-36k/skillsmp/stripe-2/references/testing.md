# Stripe - Testing

**Pages:** 6

---

## Testing

**URL:** https://docs.stripe.com/testing?testing-method=tokens

**Contents:**
- Testing
- Simulate payments to test your integration.
- How to use test cards
    - Don't use real card details
  - Testing interactively
  - Test code
- Cards by brand
- Cards by country
    - Security tip
    - Regional considerationsIndia

To test your integration, simulate transactions without moving any money using special testing values in a sandbox. You can access your sandboxes using the account picker at the top right of the page or in the Dashboard.

Test cards act as fake credit cards, and allow you to simulate the following scenarios:

Testing non-card payments works similarly. Non-card payments are payment methods that aren’t credit or debit cards. Stripe supports various non-card payment options, such as digital wallets and bank transfers. Each payment method has its own special values.

Don’t use testing environments to load test your integration because you might hit rate limits. To load test your integration, see load testing.

Any time you work with a test card, use test API keys in all API calls. This is true whether you’re serving a payment form to test interactively or writing test code.

Don’t use real card details. The Stripe Services Agreement prohibits testing in live mode using real payment method details. Use your test API keys and the card numbers below.

When testing interactively, use a card number, such as 4242 4242 4242 4242. Enter the card number in the Dashboard or in any payment form.

When writing test code, use a PaymentMethod such as pm_card_visa instead of a card number. We don’t recommend using card numbers directly in API calls or server-side code, even in testing environments. If you do use them, your code might not be PCI-compliant when you go live. By default, a PaymentMethod isn’t attached to a Customer.

Most integrations don’t use Tokens anymore, but we make test Tokens such as tok_visa available if you need them.

When you’re ready to take your integration live, replace your test publishable and secret API keys with live ones. You can’t process live payments if your integration is still using your test API keys.

To simulate a successful payment for a specific card brand, use test cards from the following list.

Cross-border fees are assessed based on the country of the card issuer. Cards where the issuer country isn’t the US (such as JCB and UnionPay) might be subject to a cross-border fee, even in testing environments.

Most Cartes Bancaires and eftpos cards are co-branded with either Visa or Mastercard. The test cards in the following table simulate successful payments with co-branded cards.

To simulate successful payments from specific countries, use test cards from the following sections.

Strong Customer Authentication regulations require 3D Secure authentication for online payments within the European Economic Area. The test cards in the Europe and Middle East section simulate a payment that succeeds without authentication. We also recommend testing authentication scenarios using 3D Secure test cards.

To test subscriptions that require mandates and pre-debit notifications, see India recurring payments.

Below are test card numbers for simulating transactions using Health Savings Accounts (HSA) and Flexible Spending Accounts (FSA). These accounts are commonly used for medical expenses, and testing with them ensures proper handling of healthcare-related transactions within your application.

To test your integration’s error-handling logic by simulating payments that the issuer declines for various reasons, use test cards from this section. Using one of these cards results in a card error with the given error code and decline code.

To simulate an incorrect CVC, you must provide one using any three-digit number. If you don’t provide a CVC, Stripe doesn’t perform the CVC check, so the check can’t fail.

The cards in the previous table can’t be attached to a Customer object. To simulate a declined payment with a successfully attached card, use the next one.

Stripe’s fraud prevention system, Radar, can block payments when they have a high risk level or fail verification checks. You can use the cards in this section to test your Radar settings. You can also use them to test how your integration responds to blocked payments.

Each card simulates specific risk factors. Your Radar settings determine which risk factors cause it to block a payment. Blocked payments result in card errors with an error code of fraud.

To simulate a failed CVC check, you must provide a CVC using any three-digit number. To simulate a failed postal code check, you must provide any valid postal code. If you don’t provide those values, Radar doesn’t perform the corresponding checks, so the checks can’t fail.

The charge has a risk level of “highest”

Radar always blocks it.

The charge has a risk level of “highest”

Radar might block it depending on your settings.

tok_riskLevelElevated

The charge has a risk level of “elevated”

If you use Radar for Fraud Teams, Radar might queue it for review.

If you provide a CVC number, the CVC check fails.

Radar might block it depending on your settings.

Postal code check fails

If you provide a postal code, the postal code check fails.

Radar might block it depending on your settings.

CVC check fails with elevated risk

tok_cvcCheckFailElevatedRisk

If you provide a CVC number, the CVC check fails with a risk level of “elevated”

Radar might block it depending on your settings.

Postal code check fails with elevated risk

tok_avsZipFailElevatedRisk

If you provide a postal code, the postal code check fails with a risk level of “elevated”

Radar might block it depending on your settings.

The address line 1 check fails.

The payment succeeds unless you block it with a custom Radar rule.

The address postal code check and address line 1 check both fail.

Radar might block it depending on your settings.

The address postal code check and address line 1 check are both unavailable.

The payment succeeds unless you block it with a custom Radar rule.

To test errors resulting from invalid data, provide invalid details. You don’t need a special test card for this. Any invalid value works. For instance:

To simulate a disputed transaction, use the test cards in this section. Then, to simulate winning or losing the dispute, provide winning or losing evidence.

To simulate winning or losing the dispute, respond with one of the evidence values from the table below.

In live mode, refunds are asynchronous: a refund can appear to succeed and later fail, or can appear as pending at first and later succeed. To simulate refunds with those behaviors, use the test cards in this section. (With all other test cards, refunds succeed immediately and don’t change status after that.)

You can cancel a card refund only by using the Dashboard. In live mode, you can cancel a card refund within a short but nonspecific period of time. Testing environments simulate that period by allowing you to cancel a card refund within 30 minutes.

To send the funds from a test transaction directly to your available balance, use the test cards in this section. Other test cards send funds from a successful payment to your pending balance.

3D Secure requires an additional layer of authentication for credit card transactions. The test cards in this section allow you to simulate triggering authentication in different payment flows.

Only cards in this section effectively test your 3D Secure integration by simulating defined 3DS behavior, such as a challenge flow or an unsupported card. Other Stripe testing cards might still trigger 3DS, but we return attempt_acknowledged to bypass the additional steps since 3DS testing isn’t the objective for those cards.

3D Secure redirects won’t occur for payments created directly in the Stripe Dashboard. Instead, use your integration’s own frontend or an API call.

To simulate payment flows that include authentication, use the test cards in this section. Some of these cards can also be set up for future payments, or have already been.

Stripe requests authentication when required by regulation or when triggered by your Radar rules or custom code. Even if authentication is requested, it can’t always be performed—for instance, the customer’s card might not be enrolled, or an error might occur. Use the test cards in this section to simulate various combinations of these factors.

All 3DS references indicate 3D Secure 2.

In a mobile payment, several challenge flows for authentication—where the customer has to interact with prompts in the UI—are available. Use the test cards in this section to trigger a specific challenge flow for test purposes. These cards aren’t useful in browser-based payment forms or in API calls. In those environments, they work but don’t trigger any special behavior. Because they’re not useful in API calls, we don’t provide any PaymentMethod or Token values to test with.

To prevent fraud, Stripe might display a captcha challenge to the user on the payment page. Use the test cards below to simulate this flow.

Use the test cards in this section to simulate successful in-person payments where a PIN is involved. There are many other options for testing in-person payments, including a simulated reader and physical test cards. See Test Stripe Terminal for more information.

To test your webhook endpoint or event destination, choose one of these two options:

If your requests in your testing environments begin to receive 429 HTTP errors, make them less frequently. These errors come from our rate limiter, which is more strict in testing environments than in live mode.

We don’t recommend load testing your integration using the Stripe API in testing environments. Because the load limiter is stricter in testing environments, you might see errors that you wouldn’t see in production. See load testing for an alternative approach.

Any time you use a test non-card payment method, use test API keys in all API calls. This is true whether you’re serving a payment form you can test interactively or writing test code.

Different payment methods have different test procedures:

Learn how to test scenarios with instant verifications using Financial Connections.

After you collect the bank account details and accept a mandate, send the mandate confirmation and microdeposit verification emails in a sandbox.

If your domain is {domain} and your username is {username}, use the following email format to send test transaction emails: {username}+test_email@{domain}.

For example, if your domain is example.com and your username is info, use the format info+test_email@example.com for testing ACH Direct Debit payments. This format ensures that emails route correctly. If you don’t include the +test_email suffix, we won’t send the email.

You need to activate your Stripe account before you can trigger these emails while testing.

Stripe provides several test account numbers and corresponding tokens you can use to make sure your integration for manually-entered bank accounts is ready for production.

Before test transactions can complete, you need to verify all test accounts that automatically succeed or fail the payment. To do so, use the test microdeposit amounts or descriptor codes below.

To mimic different scenarios, use these microdeposit amounts or 0.01 descriptor code values.

Test transactions settle instantly and are added to your available test balance. This behavior differs from livemode, where transactions can take multiple days to settle in your available balance.

Don’t store real user data in sandbox Link accounts. Treat them as if they’re publicly available, because these test accounts are associated with your publishable key.

Currently, Link only works with credit cards, debit cards, and qualified US bank account purchases. Link requires domain registration.

You can create sandbox accounts for Link using any valid email address. The following table shows the fixed one-time passcode values that Stripe accepts for authenticating sandbox accounts:

As Stripe adds additional funding source support, you don’t need to update your integration. Stripe automatically supports them with the same transaction settlement time and guarantees as card and bank account payments.

To test your integration’s redirect-handling logic by simulating a payment that uses a redirect flow (for example, iDEAL), use a supported payment method that requires redirects.

To create a test PaymentIntent that either succeeds or fails:

Make sure that the page (corresponding to return_url) on your website provides the status of the payment.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=500 \
  -d currency=gbp \
  -d payment_method=pm_card_visa \
  -d "payment_method_types[]"=card
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=500 \
  -d currency=gbp \
  -d payment_method=pm_card_visa \
  -d "payment_method_types[]"=card
```

---

## Test your integration

**URL:** https://docs.stripe.com/testing/overview

**Contents:**
- Test your integration
- Test your Stripe integration before going live.

Test your Stripe integration in a safe environment, like a sandbox, before going live. Our tools let you simulate transactions, verify webhooks, and test payment flows.

Find test values to simulate payment activity and best practices for applying them.

Explore common testing scenarios and how to handle them.

Create and manage test environments for your integration.

Verify your digital wallet integration works correctly.

---

## Testing

**URL:** https://docs.stripe.com/testing?testing-method=card-numbers

**Contents:**
- Testing
- Simulate payments to test your integration.
- How to use test cards
    - Don't use real card details
  - Testing interactively
  - Test code
- Cards by brand
- Cards by country
    - Security tip
    - Regional considerationsIndia

To test your integration, simulate transactions without moving any money using special testing values in a sandbox. You can access your sandboxes using the account picker at the top right of the page or in the Dashboard.

Test cards act as fake credit cards, and allow you to simulate the following scenarios:

Testing non-card payments works similarly. Non-card payments are payment methods that aren’t credit or debit cards. Stripe supports various non-card payment options, such as digital wallets and bank transfers. Each payment method has its own special values.

Don’t use testing environments to load test your integration because you might hit rate limits. To load test your integration, see load testing.

Any time you work with a test card, use test API keys in all API calls. This is true whether you’re serving a payment form to test interactively or writing test code.

Don’t use real card details. The Stripe Services Agreement prohibits testing in live mode using real payment method details. Use your test API keys and the card numbers below.

When testing interactively, use a card number, such as 4242 4242 4242 4242. Enter the card number in the Dashboard or in any payment form.

When writing test code, use a PaymentMethod such as pm_card_visa instead of a card number. We don’t recommend using card numbers directly in API calls or server-side code, even in testing environments. If you do use them, your code might not be PCI-compliant when you go live. By default, a PaymentMethod isn’t attached to a Customer.

Most integrations don’t use Tokens anymore, but we make test Tokens such as tok_visa available if you need them.

When you’re ready to take your integration live, replace your test publishable and secret API keys with live ones. You can’t process live payments if your integration is still using your test API keys.

To simulate a successful payment for a specific card brand, use test cards from the following list.

Cross-border fees are assessed based on the country of the card issuer. Cards where the issuer country isn’t the US (such as JCB and UnionPay) might be subject to a cross-border fee, even in testing environments.

Most Cartes Bancaires and eftpos cards are co-branded with either Visa or Mastercard. The test cards in the following table simulate successful payments with co-branded cards.

To simulate successful payments from specific countries, use test cards from the following sections.

Strong Customer Authentication regulations require 3D Secure authentication for online payments within the European Economic Area. The test cards in the Europe and Middle East section simulate a payment that succeeds without authentication. We also recommend testing authentication scenarios using 3D Secure test cards.

To test subscriptions that require mandates and pre-debit notifications, see India recurring payments.

Below are test card numbers for simulating transactions using Health Savings Accounts (HSA) and Flexible Spending Accounts (FSA). These accounts are commonly used for medical expenses, and testing with them ensures proper handling of healthcare-related transactions within your application.

To test your integration’s error-handling logic by simulating payments that the issuer declines for various reasons, use test cards from this section. Using one of these cards results in a card error with the given error code and decline code.

To simulate an incorrect CVC, you must provide one using any three-digit number. If you don’t provide a CVC, Stripe doesn’t perform the CVC check, so the check can’t fail.

The cards in the previous table can’t be attached to a Customer object. To simulate a declined payment with a successfully attached card, use the next one.

Stripe’s fraud prevention system, Radar, can block payments when they have a high risk level or fail verification checks. You can use the cards in this section to test your Radar settings. You can also use them to test how your integration responds to blocked payments.

Each card simulates specific risk factors. Your Radar settings determine which risk factors cause it to block a payment. Blocked payments result in card errors with an error code of fraud.

To simulate a failed CVC check, you must provide a CVC using any three-digit number. To simulate a failed postal code check, you must provide any valid postal code. If you don’t provide those values, Radar doesn’t perform the corresponding checks, so the checks can’t fail.

The charge has a risk level of “highest”

Radar always blocks it.

The charge has a risk level of “highest”

Radar might block it depending on your settings.

The charge has a risk level of “elevated”

If you use Radar for Fraud Teams, Radar might queue it for review.

If you provide a CVC number, the CVC check fails.

Radar might block it depending on your settings.

Postal code check fails

If you provide a postal code, the postal code check fails.

Radar might block it depending on your settings.

CVC check fails with elevated risk

If you provide a CVC number, the CVC check fails with a risk level of “elevated”

Radar might block it depending on your settings.

Postal code check fails with elevated risk

If you provide a postal code, the postal code check fails with a risk level of “elevated”

Radar might block it depending on your settings.

The address line 1 check fails.

The payment succeeds unless you block it with a custom Radar rule.

The address postal code check and address line 1 check both fail.

Radar might block it depending on your settings.

The address postal code check and address line 1 check are both unavailable.

The payment succeeds unless you block it with a custom Radar rule.

To test errors resulting from invalid data, provide invalid details. You don’t need a special test card for this. Any invalid value works. For instance:

To simulate a disputed transaction, use the test cards in this section. Then, to simulate winning or losing the dispute, provide winning or losing evidence.

To simulate winning or losing the dispute, respond with one of the evidence values from the table below.

In live mode, refunds are asynchronous: a refund can appear to succeed and later fail, or can appear as pending at first and later succeed. To simulate refunds with those behaviors, use the test cards in this section. (With all other test cards, refunds succeed immediately and don’t change status after that.)

You can cancel a card refund only by using the Dashboard. In live mode, you can cancel a card refund within a short but nonspecific period of time. Testing environments simulate that period by allowing you to cancel a card refund within 30 minutes.

To send the funds from a test transaction directly to your available balance, use the test cards in this section. Other test cards send funds from a successful payment to your pending balance.

3D Secure requires an additional layer of authentication for credit card transactions. The test cards in this section allow you to simulate triggering authentication in different payment flows.

Only cards in this section effectively test your 3D Secure integration by simulating defined 3DS behavior, such as a challenge flow or an unsupported card. Other Stripe testing cards might still trigger 3DS, but we return attempt_acknowledged to bypass the additional steps since 3DS testing isn’t the objective for those cards.

3D Secure redirects won’t occur for payments created directly in the Stripe Dashboard. Instead, use your integration’s own frontend or an API call.

To simulate payment flows that include authentication, use the test cards in this section. Some of these cards can also be set up for future payments, or have already been.

Stripe requests authentication when required by regulation or when triggered by your Radar rules or custom code. Even if authentication is requested, it can’t always be performed—for instance, the customer’s card might not be enrolled, or an error might occur. Use the test cards in this section to simulate various combinations of these factors.

All 3DS references indicate 3D Secure 2.

In a mobile payment, several challenge flows for authentication—where the customer has to interact with prompts in the UI—are available. Use the test cards in this section to trigger a specific challenge flow for test purposes. These cards aren’t useful in browser-based payment forms or in API calls. In those environments, they work but don’t trigger any special behavior. Because they’re not useful in API calls, we don’t provide any PaymentMethod or Token values to test with.

To prevent fraud, Stripe might display a captcha challenge to the user on the payment page. Use the test cards below to simulate this flow.

Use the test cards in this section to simulate successful in-person payments where a PIN is involved. There are many other options for testing in-person payments, including a simulated reader and physical test cards. See Test Stripe Terminal for more information.

To test your webhook endpoint or event destination, choose one of these two options:

If your requests in your testing environments begin to receive 429 HTTP errors, make them less frequently. These errors come from our rate limiter, which is more strict in testing environments than in live mode.

We don’t recommend load testing your integration using the Stripe API in testing environments. Because the load limiter is stricter in testing environments, you might see errors that you wouldn’t see in production. See load testing for an alternative approach.

Any time you use a test non-card payment method, use test API keys in all API calls. This is true whether you’re serving a payment form you can test interactively or writing test code.

Different payment methods have different test procedures:

Learn how to test scenarios with instant verifications using Financial Connections.

After you collect the bank account details and accept a mandate, send the mandate confirmation and microdeposit verification emails in a sandbox.

If your domain is {domain} and your username is {username}, use the following email format to send test transaction emails: {username}+test_email@{domain}.

For example, if your domain is example.com and your username is info, use the format info+test_email@example.com for testing ACH Direct Debit payments. This format ensures that emails route correctly. If you don’t include the +test_email suffix, we won’t send the email.

You need to activate your Stripe account before you can trigger these emails while testing.

Stripe provides several test account numbers and corresponding tokens you can use to make sure your integration for manually-entered bank accounts is ready for production.

Before test transactions can complete, you need to verify all test accounts that automatically succeed or fail the payment. To do so, use the test microdeposit amounts or descriptor codes below.

To mimic different scenarios, use these microdeposit amounts or 0.01 descriptor code values.

Test transactions settle instantly and are added to your available test balance. This behavior differs from livemode, where transactions can take multiple days to settle in your available balance.

Don’t store real user data in sandbox Link accounts. Treat them as if they’re publicly available, because these test accounts are associated with your publishable key.

Currently, Link only works with credit cards, debit cards, and qualified US bank account purchases. Link requires domain registration.

You can create sandbox accounts for Link using any valid email address. The following table shows the fixed one-time passcode values that Stripe accepts for authenticating sandbox accounts:

As Stripe adds additional funding source support, you don’t need to update your integration. Stripe automatically supports them with the same transaction settlement time and guarantees as card and bank account payments.

To test your integration’s redirect-handling logic by simulating a payment that uses a redirect flow (for example, iDEAL), use a supported payment method that requires redirects.

To create a test PaymentIntent that either succeeds or fails:

Make sure that the page (corresponding to return_url) on your website provides the status of the payment.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=500 \
  -d currency=gbp \
  -d payment_method=pm_card_visa \
  -d "payment_method_types[]"=card
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=500 \
  -d currency=gbp \
  -d payment_method=pm_card_visa \
  -d "payment_method_types[]"=card
```

---

## Testing

**URL:** https://docs.stripe.com/testing

**Contents:**
- Testing
- Simulate payments to test your integration.
- How to use test cards
    - Don't use real card details
  - Testing interactively
  - Test code
- Cards by brand
- Cards by country
    - Security tip
    - Regional considerationsIndia

To test your integration, simulate transactions without moving any money using special testing values in a sandbox. You can access your sandboxes using the account picker at the top right of the page or in the Dashboard.

Test cards act as fake credit cards, and allow you to simulate the following scenarios:

Testing non-card payments works similarly. Non-card payments are payment methods that aren’t credit or debit cards. Stripe supports various non-card payment options, such as digital wallets and bank transfers. Each payment method has its own special values.

Don’t use testing environments to load test your integration because you might hit rate limits. To load test your integration, see load testing.

Any time you work with a test card, use test API keys in all API calls. This is true whether you’re serving a payment form to test interactively or writing test code.

Don’t use real card details. The Stripe Services Agreement prohibits testing in live mode using real payment method details. Use your test API keys and the card numbers below.

When testing interactively, use a card number, such as 4242 4242 4242 4242. Enter the card number in the Dashboard or in any payment form.

When writing test code, use a PaymentMethod such as pm_card_visa instead of a card number. We don’t recommend using card numbers directly in API calls or server-side code, even in testing environments. If you do use them, your code might not be PCI-compliant when you go live. By default, a PaymentMethod isn’t attached to a Customer.

Most integrations don’t use Tokens anymore, but we make test Tokens such as tok_visa available if you need them.

When you’re ready to take your integration live, replace your test publishable and secret API keys with live ones. You can’t process live payments if your integration is still using your test API keys.

To simulate a successful payment for a specific card brand, use test cards from the following list.

Cross-border fees are assessed based on the country of the card issuer. Cards where the issuer country isn’t the US (such as JCB and UnionPay) might be subject to a cross-border fee, even in testing environments.

Most Cartes Bancaires and eftpos cards are co-branded with either Visa or Mastercard. The test cards in the following table simulate successful payments with co-branded cards.

To simulate successful payments from specific countries, use test cards from the following sections.

Strong Customer Authentication regulations require 3D Secure authentication for online payments within the European Economic Area. The test cards in the Europe and Middle East section simulate a payment that succeeds without authentication. We also recommend testing authentication scenarios using 3D Secure test cards.

To test subscriptions that require mandates and pre-debit notifications, see India recurring payments.

Below are test card numbers for simulating transactions using Health Savings Accounts (HSA) and Flexible Spending Accounts (FSA). These accounts are commonly used for medical expenses, and testing with them ensures proper handling of healthcare-related transactions within your application.

To test your integration’s error-handling logic by simulating payments that the issuer declines for various reasons, use test cards from this section. Using one of these cards results in a card error with the given error code and decline code.

To simulate an incorrect CVC, you must provide one using any three-digit number. If you don’t provide a CVC, Stripe doesn’t perform the CVC check, so the check can’t fail.

The cards in the previous table can’t be attached to a Customer object. To simulate a declined payment with a successfully attached card, use the next one.

Stripe’s fraud prevention system, Radar, can block payments when they have a high risk level or fail verification checks. You can use the cards in this section to test your Radar settings. You can also use them to test how your integration responds to blocked payments.

Each card simulates specific risk factors. Your Radar settings determine which risk factors cause it to block a payment. Blocked payments result in card errors with an error code of fraud.

To simulate a failed CVC check, you must provide a CVC using any three-digit number. To simulate a failed postal code check, you must provide any valid postal code. If you don’t provide those values, Radar doesn’t perform the corresponding checks, so the checks can’t fail.

The charge has a risk level of “highest”

Radar always blocks it.

The charge has a risk level of “highest”

Radar might block it depending on your settings.

The charge has a risk level of “elevated”

If you use Radar for Fraud Teams, Radar might queue it for review.

If you provide a CVC number, the CVC check fails.

Radar might block it depending on your settings.

Postal code check fails

If you provide a postal code, the postal code check fails.

Radar might block it depending on your settings.

CVC check fails with elevated risk

If you provide a CVC number, the CVC check fails with a risk level of “elevated”

Radar might block it depending on your settings.

Postal code check fails with elevated risk

If you provide a postal code, the postal code check fails with a risk level of “elevated”

Radar might block it depending on your settings.

The address line 1 check fails.

The payment succeeds unless you block it with a custom Radar rule.

The address postal code check and address line 1 check both fail.

Radar might block it depending on your settings.

The address postal code check and address line 1 check are both unavailable.

The payment succeeds unless you block it with a custom Radar rule.

To test errors resulting from invalid data, provide invalid details. You don’t need a special test card for this. Any invalid value works. For instance:

To simulate a disputed transaction, use the test cards in this section. Then, to simulate winning or losing the dispute, provide winning or losing evidence.

To simulate winning or losing the dispute, respond with one of the evidence values from the table below.

In live mode, refunds are asynchronous: a refund can appear to succeed and later fail, or can appear as pending at first and later succeed. To simulate refunds with those behaviors, use the test cards in this section. (With all other test cards, refunds succeed immediately and don’t change status after that.)

You can cancel a card refund only by using the Dashboard. In live mode, you can cancel a card refund within a short but nonspecific period of time. Testing environments simulate that period by allowing you to cancel a card refund within 30 minutes.

To send the funds from a test transaction directly to your available balance, use the test cards in this section. Other test cards send funds from a successful payment to your pending balance.

3D Secure requires an additional layer of authentication for credit card transactions. The test cards in this section allow you to simulate triggering authentication in different payment flows.

Only cards in this section effectively test your 3D Secure integration by simulating defined 3DS behavior, such as a challenge flow or an unsupported card. Other Stripe testing cards might still trigger 3DS, but we return attempt_acknowledged to bypass the additional steps since 3DS testing isn’t the objective for those cards.

3D Secure redirects won’t occur for payments created directly in the Stripe Dashboard. Instead, use your integration’s own frontend or an API call.

To simulate payment flows that include authentication, use the test cards in this section. Some of these cards can also be set up for future payments, or have already been.

Stripe requests authentication when required by regulation or when triggered by your Radar rules or custom code. Even if authentication is requested, it can’t always be performed—for instance, the customer’s card might not be enrolled, or an error might occur. Use the test cards in this section to simulate various combinations of these factors.

All 3DS references indicate 3D Secure 2.

In a mobile payment, several challenge flows for authentication—where the customer has to interact with prompts in the UI—are available. Use the test cards in this section to trigger a specific challenge flow for test purposes. These cards aren’t useful in browser-based payment forms or in API calls. In those environments, they work but don’t trigger any special behavior. Because they’re not useful in API calls, we don’t provide any PaymentMethod or Token values to test with.

To prevent fraud, Stripe might display a captcha challenge to the user on the payment page. Use the test cards below to simulate this flow.

Use the test cards in this section to simulate successful in-person payments where a PIN is involved. There are many other options for testing in-person payments, including a simulated reader and physical test cards. See Test Stripe Terminal for more information.

To test your webhook endpoint or event destination, choose one of these two options:

If your requests in your testing environments begin to receive 429 HTTP errors, make them less frequently. These errors come from our rate limiter, which is more strict in testing environments than in live mode.

We don’t recommend load testing your integration using the Stripe API in testing environments. Because the load limiter is stricter in testing environments, you might see errors that you wouldn’t see in production. See load testing for an alternative approach.

Any time you use a test non-card payment method, use test API keys in all API calls. This is true whether you’re serving a payment form you can test interactively or writing test code.

Different payment methods have different test procedures:

Learn how to test scenarios with instant verifications using Financial Connections.

After you collect the bank account details and accept a mandate, send the mandate confirmation and microdeposit verification emails in a sandbox.

If your domain is {domain} and your username is {username}, use the following email format to send test transaction emails: {username}+test_email@{domain}.

For example, if your domain is example.com and your username is info, use the format info+test_email@example.com for testing ACH Direct Debit payments. This format ensures that emails route correctly. If you don’t include the +test_email suffix, we won’t send the email.

You need to activate your Stripe account before you can trigger these emails while testing.

Stripe provides several test account numbers and corresponding tokens you can use to make sure your integration for manually-entered bank accounts is ready for production.

Before test transactions can complete, you need to verify all test accounts that automatically succeed or fail the payment. To do so, use the test microdeposit amounts or descriptor codes below.

To mimic different scenarios, use these microdeposit amounts or 0.01 descriptor code values.

Test transactions settle instantly and are added to your available test balance. This behavior differs from livemode, where transactions can take multiple days to settle in your available balance.

Don’t store real user data in sandbox Link accounts. Treat them as if they’re publicly available, because these test accounts are associated with your publishable key.

Currently, Link only works with credit cards, debit cards, and qualified US bank account purchases. Link requires domain registration.

You can create sandbox accounts for Link using any valid email address. The following table shows the fixed one-time passcode values that Stripe accepts for authenticating sandbox accounts:

As Stripe adds additional funding source support, you don’t need to update your integration. Stripe automatically supports them with the same transaction settlement time and guarantees as card and bank account payments.

To test your integration’s redirect-handling logic by simulating a payment that uses a redirect flow (for example, iDEAL), use a supported payment method that requires redirects.

To create a test PaymentIntent that either succeeds or fails:

Make sure that the page (corresponding to return_url) on your website provides the status of the payment.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=500 \
  -d currency=gbp \
  -d payment_method=pm_card_visa \
  -d "payment_method_types[]"=card
```

Example 2 (unknown):
```unknown
curl https://api.stripe.com/v1/payment_intents \
  -u "sk_test_YOUR_TEST_KEY_HERE:" \
  -d amount=500 \
  -d currency=gbp \
  -d payment_method=pm_card_visa \
  -d "payment_method_types[]"=card
```

---

## Test Apple and Google wallet rendering

**URL:** https://docs.stripe.com/testing/wallets

**Contents:**
- Test Apple and Google wallet rendering
- Compare your integration against working demo integrations to identify possible rendering issues.
- Check your device and browser setup
- Check your integration
  - Register your domains
  - (Apple Pay) Register all domains when using iframes
  - Enable wallets for your integration

The following demo shows different Stripe payment integrations with Apple Pay and Google Pay set up. Use the demo to visually compare how these wallets display in the demo integrations and your own integration.

For this integration path, Stripe.js detects and supports the following wallets based on the state of your device.

Running canMakePayment(), results will be shown soon

If you can’t see your expected wallet in the demos, your device or browser might not meet the following Apple Pay or Google Pay conditions.

If you see the expected wallet payment methods in the demo payment forms, but they don’t display in your own integration, the following checkpoints might resolve the issue.

Check your Stripe Dashboard to confirm your domain registrations. You must register every domain and sub-domain separately for each environment, including live mode and each sandbox.

Connect users must also consider the funds flow configuration (direct or destination charge) for correct domain registration.

To see Apple Pay in an integration using iframes you must:

---

## Stripe.js testing assistant

**URL:** https://docs.stripe.com/sdks/stripejs-testing-assistant

**Contents:**
- Stripe.js testing assistant
- Test and debug your Elements integration directly on your website using your browser.
- Elements autofill
- Integration insights
- Customer location simulation
- Elements inspector
    - Note
- Hide the testing assistant

You can use the Stripe.js testing assistant to set up your integration.

The testing assistant appears on the bottom right of the page.

The testing assistant appears on your website on any page with Elements loaded in a sandbox and doesn’t appear in live mode. The testing assistant provides tools that allow you to:

The testing assistant automatically shows payment method presets for the payment methods included in your integration. You can use these presets to autofill the Payment Element for different payment scenarios.

Use the payment method presets to autofill Elements.

For example, you can select Magic Fill to autofill all Elements present on the page at the same time.

The testing assistant highlights integration errors and warnings to help you follow best practices. It also suggests optimization techniques to help manage your integration’s effectiveness, such as using dynamic payment methods if you aren’t already doing so.

View integration errors and warnings

The testing assistant simulates your customer’s location to view what payment methods display to your customers around the world.

Simulate your customer’s location to view your integration in various countries

If you use the Currency Selector Element, you can also simulate the customer’s location to view which payment methods display based on the customer’s chosen currency.

The Elements inspector is only available when using Elements with the Checkout Sessions API.

The Elements inspector helps you debug your integration by displaying real-time information about payment method availability, Adaptive Pricing, and your payment method configuration. For example, you can use the Elements inspector to troubleshoot why specific payment methods aren’t appearing for your customers or why Adaptive Pricing is not active.

Debug your integration with the Elements inspector

By default, Stripe automatically enables the testing assistant for integrations using Elements with the Checkout Sessions API or for those using Elements with the Payment Intents API on Clover version or later.

To hide the testing assistant, set the developerTools.assistant.enabled option to false when you set up Elements.

**Examples:**

Example 1 (javascript):
```javascript
const stripe = new Stripe(publicKey, {
  developerTools: {
    assistant: {
      enabled: false,
    },
  },
});
```

Example 2 (javascript):
```javascript
const stripe = new Stripe(publicKey, {
  developerTools: {
    assistant: {
      enabled: false,
    },
  },
});
```

---
