# Stripe - Security

**Pages:** 4

---

## Security at Stripe

**URL:** https://docs.stripe.com/security

**Contents:**
- Security at Stripe
- Learn how Stripe handles security.
- Standards and regulations compliance
  - PCI-certified
  - System and Organization Controls (SOC) reports
  - EMVCo standard for card terminals
  - NIST Cybersecurity Framework
  - Privacy and data protection
- Stripe product securement
  - Sensitive action authentication

Our users trust Stripe with their sensitive data and rely on us to be good custodians of their customers’ data as well. As a payments infrastructure company, our security posture continually evolves to meet the rigorous standards of the global financial industry.

Stripe uses best-in-class security practices to maintain a high level of security.

A PCI-certified auditor evaluated Stripe and certified us to PCI Service Provider Level 1. This is the most stringent level of certification available in the payments industry. This audit includes both Stripe’s Card Data Vault (CDV) and the secure software development of our integration code.

We provide our users with features to automate some aspects of PCI compliance.

Stripe’s systems, processes, and controls are regularly audited as part of our SOC 1 and SOC 2 compliance programs. SOC 1 and SOC 2 Type II reports are produced annually and can be provided upon request.

The Auditing Standards Board of the American Institute of Certified Public Accountants’ (AICPA) Trust Service Criteria (TSC) developed the SOC 3 report. Stripe’s SOC 3 is a public report of internal controls over security, availability, and confidentiality. View our recent SOC 3 report.

Stripe Terminal is certified to the EMVCo Level 1 and 2 standards of EMV® Specifications for card and terminal security and interoperability. Terminal is also certified to the PCI Payment Application Data Security Standard (PA-DSS), the global security standard that aims to prevent payment applications developed for third parties from storing prohibited secure data.

Stripe’s suite of information security policies and their overarching design are aligned with the NIST Cybersecurity Framework. Our security practices meet the standards of our enterprise customers who must provide secure products like on-demand cloud computing and storage platforms (for example, DigitalOcean and Slack).

The Stripe privacy practices comply with CBPR and PRP systems as evidenced by the CBPR and PRP certifications Stripe has obtained. See the status of our CBPR and PRP certifications. Stripe also complies with the US Data Privacy Framework (“EU-US DPF”), the UK Extension to the EU-US DPF, and the Swiss-US Data Privacy Framework as set forth by the US Department of Commerce. See our certifications.

We continuously implement evolving privacy and data protection processes, procedures, and best practices under all applicable privacy and data protection regimes. For more information, see the following Stripe resources:

Security is one of Stripe’s guiding principles for all our product design and infrastructure decisions. We offer a range of features to help our users better protect their Stripe data.

The Stripe Dashboard supports several forms of multi-factor authentication (MFA) including: SMS, time-based one-time password algorithm (TOTP), hardware security keys, and passkeys. We also support single sign-on through Security Assertion Markup Language (SAML) 2.0, allowing you to mandate sign-in requirements, configure access control, and instantly onboard team members through just-in-time (JIT) account provisioning.

You must authenticate user support requests by sending them from the Dashboard after login, or by verifying account access before we offer a support response. By requiring authentication, we minimize the risk of providing any information to non-authorized people.

From the Dashboard, you can assign different detailed roles to enable least-privilege access for your employees, and create restricted access keys to reduce the security and reliability risk of API key exposure.

You can also view audit logs of important account changes and activity in your security history. These audit logs contain records of sensitive account activity, such as logging in or changing bank account information. We monitor logins and note:

You can export historical information from the logs. For time-sensitive activities, such as logins from unknown IPs and devices, we send automatic notifications so you don’t need to review logs manually.

We mandate the use of HTTPS for all services using TLS (SSL), including our public website and the Dashboard. We regularly audit the details of our implementation, including the certificates we serve, the certificate authorities we use, and the ciphers we support. We use HSTS to make sure that browsers interact with Stripe only over HTTPS. Stripe is also on the HSTS preloaded lists for all modern major browsers.

All server-to-server communication is encrypted using mutual transport layer security (mTLS) and Stripe has dedicated PGP keys for you to encrypt communications with Stripe, or verify signed messages you receive from us. Our systems automatically block requests made using older, less secure versions of TLS, requiring use of at least TLS 1.2.

The stripe.com domain, including the Dashboard and API subdomains, are on the top domains list for Chrome, providing extra protection against homoglyph attacks. This makes it harder to create fake pages that look like stripe.com in Chrome (for example, strípe.com), which renders as punycode (xn–strpe-1sa.com), in turn making it harder for Stripe credentials to be phished.

We proactively scan the internet for our merchants’ API keys. If we find a compromised key, we take appropriate action, advising the user to roll their API key. We use the GitHub Token Scanner to alert us when a user’s API keys have been leaked on GitHub. If we find external phishing pages that might catch our users, we work proactively with our vendors to take those down and report them to Google Safe Browsing.

Our security teams test our infrastructure regularly by scanning for vulnerabilities and conducting penetration tests and red team exercises. We hire industry-leading security companies to perform third-party scans of our systems, and we immediately address their findings. Our servers are frequently and automatically replaced to maintain server health and discard stale connections or resources. Server operating systems are upgraded well in advance of their security end of life (EOL) date.

Stripe encrypts sensitive data both in transit and at rest. The Stripe infrastructure for storing, decrypting, and transmitting primary account numbers (PANs), such as credit card numbers, runs in a separate hosting infrastructure and doesn’t share any credentials with the rest of our services. A dedicated team manages our CDV in an isolated Amazon Web Services (AWS) environment that’s separate from the rest of the Stripe infrastructure. Access to this separate environment is restricted to a small number of specially trained engineers and access is reviewed quarterly.

All card numbers are encrypted at rest with AES-256. Decryption keys are stored on separate machines. We tokenize PANs internally, isolating raw numbers from the rest of our infrastructure. None of the Stripe internal servers and daemons can obtain plain text card numbers, but they can request that cards are sent to a service provider on a static allowlist. The Stripe infrastructure for storing, decrypting, and transmitting card numbers runs in a separate hosting environment, and doesn’t share any credentials with primary Stripe services, including our API and website. We treat other sensitive data, such as bank account information, similarly to how we tokenize PANs.

Stripe takes a zero-trust approach to employee access management. Employees are authenticated with SSO, two-factor authentication (2FA) using a hardware-based token, and mTLS through a cryptographic certificate on Stripe-issued machines. After connecting to the network, sensitive internal systems and those outside the scope of the employee’s standard work require additional access permissions.

We monitor audit logs to detect abnormalities and watch for intrusions and suspicious activity, and also monitor changes to sensitive files in our code base. All of Stripe’s code goes through multiparty review and automated testing. Code changes are recorded in an immutable, tamper-evident log.

We constantly collect information about Stripe-issued laptops to monitor for malicious processes, connections to fraudulent domains, and intruder activity. We have a comprehensive process for allowlisting permitted software on employee laptops, preventing the installation of non-approved applications.

Our developers work with security experts early in a project’s life cycle. As part of our Security Review process, security experts develop threat models and trust boundaries that help guide the implementation of the project. Developers use this same process to make changes to sensitive pieces of code.

We have a number of dedicated security teams that specialize in different areas of security, including infrastructure, operations, privacy, users, and applications. Security experts are available 24/7 through on-call rotations. We’re focused on constantly raising the bar on best practices to minimize cybersecurity risks.

We require every Stripe employee to complete annual security education, and we provide secure software development training to Stripe engineers. We run internal phishing campaigns to test everyone at Stripe on recognizing phishing attempts and flagging them to the appropriate security team.

We have a formal process for granting access to systems and information, and we regularly review and automatically remove inactive access. Actions within the most sensitive areas of the infrastructure need a human review. To enable best practices for access control, our security experts build primitives to assist Stripe teams in implementing the principle of least privilege. To minimize our exposure, we have a data retention policy that reduces the data we keep while complying with regulatory and business requirements.

We maintain a vulnerability disclosure and reward (“bug bounty”) program that compensates independent security researchers who help us keep our users safe. By submitting a security bug or vulnerability to Stripe through HackerOne, you acknowledge that you’ve read and agreed to the program terms and conditions. Refer to our policy on HackerOne for more information about how to participate in our bug bounty program.

---

## Python PGP key

**URL:** https://docs.stripe.com/security/python-client-pgp-key

**Contents:**
- Python PGP key
- Learn how to use the Python client library PGP key.
    - Note
  - Python PGP key

If you’re unfamiliar with PGP, see GPG and start by importing a public key. After you familiarize yourself with the basics of PGP, use this PGP key as it’s marked as trusted for the Python client library.

If you have any questions, or encounter any issues, please contact us at support-migrations@stripe.com.

After you import the key, you can encrypt files by running:

This creates FILENAME.gpg with the following information:

**Examples:**

Example 1 (unknown):
```unknown
gpg --encrypt --recipient 05D02D3D57ABFF46 FILENAME
```

Example 2 (unknown):
```unknown
gpg --encrypt --recipient 05D02D3D57ABFF46 FILENAME
```

---

## Understand fraud

**URL:** https://docs.stripe.com/disputes/prevention

**Contents:**
- Understand fraud
- Learn how to identify fraud, and design a strategy to prevent it.

Stripe provides resources and tools to help you develop a strategy for detecting and preventing fraud and other types of disputed payments.

Learn about the different types of fraud and the best strategies to prevent each type.

Learn how to monitor decline activity to identify card testing and how to prevent it.

Familiarize yourself with the most common fraud indicators so you can implement safeguards against them.

Learn about different safeguards you can implement, such as strong communication with your customers, collecting comprehensive customer data, and multi-factor authentication.

---

## Integration security guide

**URL:** https://docs.stripe.com/security/guide

**Contents:**
- Integration security guide
- Ensure PCI compliance and secure customer-server communications.
- Validate your PCI compliance
- Use low risk integrations
  - Out-of-scope card data that you can safely store
- Use TLS and HTTPS
  - Serve resources securely
  - Set up TLS
- Security considerations
  - Content Security Policy

PCI DSS is the global security standard for all entities that store, process, or transmit cardholder or sensitive authentication data. PCI DSS sets a baseline level of protection for consumers and helps reduce fraud and data breaches across the entire payment ecosystem. Anyone involved with the processing, transmission, or storage of card data must comply with the Payment Card Industry Data Security Standard (PCI DSS).

PCI compliance is a shared responsibility and applies to both Stripe and your business:

Review the documentation requirements for your business in your Dashboard and continue reading this guide to learn how Stripe can help you become PCI compliant.

Some business models require the intake of untokenized PANs on a payment page. If your business handles sensitive credit card data directly when accepting payments, you might be required to meet the more than 300+ security controls in PCI DSS. This might require you to purchase, implement, and maintain dedicated security software and hardware, and hire external auditors to support your annual assessment requirements.

Many business models don’t need to handle sensitive card data. You can instead use one of our low risk payment integrations to securely collect and transmit payment information directly to Stripe without it passing through your servers, reducing your PCI obligations.

Stripe returns non-sensitive card information in the response to a charge request. This includes the card type, the last four digits of the card, and the expiration date. This information isn’t subject to PCI compliance, so you can store any of these properties in your database. Additionally, you can store anything returned by our API.

TLS refers to the process of securely transmitting data between the client—the app or browser that your customer is using—and your server. The Secure Sockets Layer (SSL) protocol originally performed this, but is outdated and no longer secure. TLS replaced SSL, but the term SSL continues to be used colloquially when referring to TLS and its function to protect transmitted data.

Payment pages must use a recent version (TLS 1.2 or above) because it significantly reduces the risk of man-in-the-middle attacks for both you and your customers. TLS attempts to accomplish the following:

Make sure any resources (for example, JavaScript, CSS, and images) are also served over TLS to avoid your customers seeing a mixed content warning in their browser.

Using TLS requires a digital certificate—a file issued by a certification authority (CA). Installing this certificate assures the client that it’s actually communicating with the server it expects to be talking to, and not an impostor. Obtain a digital certificate from a reputable certificate provider, such as:

You can test your integration without using HTTPS if you need to, and enable it when you’re ready to accept live charges. However, all interactions between your server and Stripe must use HTTPS (that is, when using our libraries).

As TLS is a complex suite of cryptographic tools, it’s easy to miss a few details. We recommend using the SSL Server Test by Qualys SSL Labs to make sure you set up everything in a secure way.

Including JavaScript from other sites makes your security dependent on theirs and poses a security risk. If they’re ever compromised, an attacker could execute arbitrary code on your page. In practice, many sites use JavaScript for services like Google Analytics, even on secure pages. Nonetheless, we recommend trying to minimize it.

If you’re using webhooks, use TLS for the endpoint to avoid traffic being intercepted and having notifications altered (sensitive information is never included in a webhook event).

While complying with the Data Security Standards is important, it shouldn’t be where you stop thinking about security. Some good resources to learn about web security are:

If you’ve deployed a Content Security Policy, the full set of directives that Checkout, Connect embedded components, and Stripe.js require are:

Currently, we don’t support Cross-origin isolated sites.

Cross-origin isolation requires support by all dependencies, and several key dependencies that enable our payment offerings don’t yet provide support for this feature.

---
