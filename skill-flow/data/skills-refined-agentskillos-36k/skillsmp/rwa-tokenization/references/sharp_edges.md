# Rwa Tokenization - Sharp Edges

## Unregistered Securities Offering

### **Id**
unregistered-securities-offering
### **Severity**
critical
### **Description**
  Selling tokens that represent real-world assets without proper
  securities registration or exemption is a federal crime. The SEC
  has shut down hundreds of projects and pursued criminal charges.
  
### **Symptoms**
  - We're not a security because it's on blockchain
  - We'll call it a utility token
  - Only selling to our community, not the public
  - We're outside the US so SEC doesn't apply
### **Why Dangerous**
  The Howey Test doesn't care about your terminology. If investors
  are putting money into a common enterprise expecting profits from
  others' efforts, it's a security. Period.
  
  Consequences:
  - SEC enforcement action
  - Criminal referral to DOJ
  - Investor rescission rights (must return all money)
  - Personal liability for founders
  - Permanent industry ban
  
### **Prevention**
  - Always work with securities counsel BEFORE token design
  - Assume you ARE a security until counsel confirms otherwise
  - File proper exemption (Reg D, Reg S, Reg A+)
  - Use compliant platforms (Securitize, Tokeny, etc.)
### **Detection Patterns**
  - permissionless.*transfer
  - anyone.*can.*buy
  - no.*kyc.*required
  - utility.*token.*represents.*ownership

## Bypassing Transfer Agent Requirements

### **Id**
transfer-agent-bypass
### **Severity**
critical
### **Description**
  In the US, SEC Rule 17Ad requires registered transfer agents for
  securities. The blockchain cannot replace this legal requirement.
  Your on-chain transfers must reconcile with official records.
  
### **Symptoms**
  - The blockchain IS the shareholder registry
  - We don't need a transfer agent, it's decentralized
  - Smart contract handles all record-keeping
### **Why Dangerous**
  Without a registered transfer agent:
  - Token transfers may not be legally valid
  - Investors may not have enforceable rights
  - Corporate actions (dividends, votes) may be invalid
  - SEC can halt all trading
  
  Transfer agents provide:
  - Legal shareholder registry
  - Lost token recovery
  - Estate processing
  - Court order compliance
  
### **Prevention**
  - Partner with registered transfer agent (Securitize, tZero, etc.)
  - Build integration bridge, not replacement
  - Sync on-chain and off-chain records
  - Transfer agent approves or can block transfers
### **Detection Patterns**
  - no.*transfer.*agent
  - blockchain.*replaces.*registry
  - decentralized.*cap.*table

## Single Oracle for Asset Valuation

### **Id**
oracle-single-point-of-failure
### **Severity**
critical
### **Description**
  Real-world assets need off-chain data (valuations, ownership status,
  physical condition). A single oracle point of failure can break your
  entire token's connection to reality.
  
### **Symptoms**
  - Using one appraiser's API for all valuations
  - No staleness checks on oracle data
  - No circuit breakers for price anomalies
  - Oracle updates controlled by single key
### **Why Dangerous**
  Oracle failure scenarios:
  - Oracle goes stale (price doesn't update) -> arbitrage attack
  - Oracle is compromised -> false valuations
  - Oracle provider goes bankrupt -> no data source
  - Flash manipulation -> incorrect NAV
  
  For a $100M real estate token with stale oracle:
  - Arbitrageurs buy cheap tokens
  - Redeem at stale (higher) price
  - Protocol takes the loss
  
### **Prevention**
  - Multiple oracle sources with aggregation
  - Staleness thresholds (halt if data > X hours old)
  - Price deviation circuit breakers (halt if > 10% change)
  - Manual override capability for emergencies
  - Decentralized oracle networks where possible
### **Detection Patterns**
  - single.*oracle
  - oracle\.get.*Price\(\).*without.*staleness
  - trustedOracle
  - owner.*can.*set.*price

## Gap Between Token and Asset Custody

### **Id**
custody-gap
### **Severity**
critical
### **Description**
  A token is only as valuable as the legal claim it represents. If
  the underlying asset isn't properly custodied, token holders have
  nothing.
  
### **Symptoms**
  - Trust us, we own the real estate
  - No third-party custodian
  - No proof of reserves
  - Asset held in founder's personal name
### **Why Dangerous**
  Without proper custody:
  - Issuer can sell asset without token holder consent
  - Bankruptcy doesn't protect token holders
  - No recourse if asset disappears
  - Due diligence is impossible
  
  Famous failures:
  - Multiple "gold-backed" tokens with no actual gold
  - Real estate tokens where property was never transferred
  - Art tokens where art was sold separately
  
### **Prevention**
  - Third-party qualified custodian
  - Regular proof of reserves audits
  - Legal structure that isolates assets (SPV per asset)
  - On-chain attestations from custodian
  - Insurance coverage
### **Detection Patterns**
  - trust.*the.*issuer
  - no.*custodian
  - self.*custody.*of.*underlying

## Holding Period Non-Enforcement

### **Id**
holding-period-violation
### **Severity**
high
### **Description**
  Most private securities have mandatory holding periods before resale.
  Reg D requires 12 months. Reg S has distribution compliance periods.
  Rule 144 has 6-12 month holding periods.
  
### **Symptoms**
  - Immediate trading enabled after purchase
  - No tracking of acquisition dates
  - Same transfer rules for all investors
  - Holding periods are just guidance
### **Why Dangerous**
  Holding period violations:
  - Create rescission rights for ALL investors
  - Violate the exemption (offering becomes unregistered)
  - Personal liability for issuer officers
  - SEC can require unwinding of all trades
  
  These violations often surface during audits or when
  investors try to exit and realize their tokens are tainted.
  
### **Prevention**
  - Track acquisition date per token
  - Enforce holding periods in transfer logic
  - Different rules for primary vs secondary sales
  - Whitelist qualified transferees during holding period
### **Detection Patterns**
  - transfer.*without.*holding.*period
  - immediate.*liquidity
  - no.*lockup

## Exceeding Investor Limits

### **Id**
investor-count-explosion
### **Severity**
high
### **Description**
  Reg D 506(b) limits non-accredited investors to 35. Exceeding this
  voids the exemption. 506(c) requires ALL investors to be verified
  accredited. Section 12(g) triggers at 2000 investors or $10M assets.
  
### **Symptoms**
  - Not tracking investor counts by qualification
  - Allowing unlimited transfers
  - No checks before new investor onboarding
  - We'll deal with limits later
### **Why Dangerous**
  Investor limit violations:
  - 506(b) with 36+ non-accredited = exemption void
  - 506(c) with one non-accredited = exemption void
  - 2000+ holders = mandatory SEC registration
  - These cannot be fixed retroactively
  
### **Prevention**
  - On-chain tracking of investor counts by type
  - Block transfers that would exceed limits
  - Re-verify accreditation periodically
  - Monitor for 12(g) threshold
### **Detection Patterns**
  - no.*investor.*limit
  - unlimited.*transfers
  - count.*investors.*after

## Cross-Border Regulatory Violations

### **Id**
cross-border-compliance-failure
### **Severity**
high
### **Description**
  Each jurisdiction has its own securities laws. A token legal in the
  US under Reg D may be illegal in the EU without proper prospectus.
  Reg S carve-outs have strict flow-back restrictions.
  
### **Symptoms**
  - We're US-based so only US law matters
  - No jurisdiction checks in transfer logic
  - Reg S tokens flowing back to US persons
  - Selling to retail in MiCA-regulated jurisdictions
### **Why Dangerous**
  Multi-jurisdictional failures:
  - EU regulators can block your token
  - Reg S flow-back voids the exemption
  - Each violation is a separate offense
  - Investors in one country can't be made whole
  
  I've seen a token that was compliant in US but violated
  securities laws in 8 other countries where investors resided.
  
### **Prevention**
  - Jurisdiction mapping in identity registry
  - Transfer restrictions by geography
  - Reg S flow-back prevention (12 month distribution compliance)
  - Local counsel in major investor markets
  - Geofencing for token purchases
### **Detection Patterns**
  - no.*jurisdiction.*check
  - global.*offering
  - anyone.*worldwide

## Stale KYC/AML Verification

### **Id**
kyc-expiration-blind-spot
### **Severity**
high
### **Description**
  KYC verification is not one-time. Accredited investor status changes,
  PEP status changes, sanctions lists update. Stale verification creates
  compliance gaps.
  
### **Symptoms**
  - One-time KYC at onboarding
  - No expiration on verification claims
  - No re-verification process
  - Not monitoring sanctions list updates
### **Why Dangerous**
  Stale KYC issues:
  - Investor loses accredited status (divorce, job loss)
  - Investor added to sanctions list (OFAC)
  - Investor becomes PEP (political appointment)
  - AML red flags emerge after onboarding
  
  Regulators expect ongoing monitoring, not point-in-time checks.
  
### **Prevention**
  - 90-day verification expiration
  - Automated re-verification triggers
  - Sanctions screening on every transfer
  - Accreditation re-attestation annually
  - Pause transfers for expired verifications
### **Detection Patterns**
  - verified.*=.*true.*permanent
  - no.*expiration
  - kyc.*once

## Dividend/Distribution Calculation Errors

### **Id**
dividend-calculation-errors
### **Severity**
high
### **Description**
  Incorrect dividend calculations create accounting nightmares, tax
  issues, and potential securities violations. Rounding errors at
  scale become material.
  
### **Symptoms**
  - Integer division without precision handling
  - No record date snapshot
  - Dust accumulation in contract
  - Missing tax withholding logic
### **Why Dangerous**
  Calculation errors cause:
  - Investors receive wrong amounts
  - Tax withholding mismatches (IRS issues)
  - Unclaimed dividends stuck forever
  - Audit failures
  
  At 10,000 investors, a $0.01 rounding error per distribution
  is $100 per cycle. Over 4 quarterly distributions, that's $400
  per year unaccounted for.
  
### **Prevention**
  - Use high precision (18 decimals minimum)
  - Proper rounding with dust collection
  - Snapshot balances at record date
  - Claim period with unclaimed recovery
  - Tax withholding by jurisdiction
### **Detection Patterns**
  - amount.*\/.*supply
  - no.*snapshot
  - no.*withholding

## Upgradeable Contracts Without Governance

### **Id**
upgrade-without-governance
### **Severity**
medium
### **Description**
  Compliance modules often need updates (new regulations, new
  jurisdictions). But upgrades without proper governance create
  centralization and trust issues.
  
### **Symptoms**
  - Single admin can upgrade any contract
  - No timelock on upgrades
  - No investor notification
  - Compliance rules can change silently
### **Why Dangerous**
  Governance failures:
  - Admin can add themselves to whitelist
  - Compliance modules can be gutted
  - Investors don't know rules changed
  - Audit trail is broken
  
  "Trust me" doesn't work in securities. Investors need
  assurance that rules won't change arbitrarily.
  
### **Prevention**
  - Multi-sig governance for upgrades
  - Timelock (48-72 hours minimum)
  - On-chain upgrade proposals
  - Investor notification system
  - Immutable core rights
### **Detection Patterns**
  - owner.*can.*upgrade
  - no.*timelock
  - single.*admin

## No Forced Transfer Mechanism

### **Id**
missing-forced-transfer
### **Severity**
medium
### **Description**
  Legal systems require the ability to execute court orders, estate
  transfers, and regulatory seizures. Tokens without this capability
  may be non-compliant.
  
### **Symptoms**
  - Only voluntary transfers supported
  - Private keys are sacred
  - No freeze capability
  - No recovery for lost keys
### **Why Dangerous**
  Missing forced transfer creates:
  - Court order non-compliance
  - Estate settlement impossible
  - Regulatory seizure blocked
  - Lost key = permanent loss
  
  Securities law requires issuers to comply with legal orders.
  A token that cannot do this is problematic.
  
### **Prevention**
  - Agent role with forced transfer capability
  - Freeze/unfreeze for investigations
  - Recovery mechanism for lost keys
  - Audit trail for all forced actions
  - Legal document hash requirement
### **Detection Patterns**
  - only.*owner.*can.*transfer
  - no.*agent.*role
  - no.*freeze

## Unplanned Secondary Market

### **Id**
secondary-market-blind-spot
### **Severity**
medium
### **Description**
  If your token can trade on secondary markets, you need to plan for
  it. Uncontrolled secondary trading may require ATS registration
  or broker-dealer involvement.
  
### **Symptoms**
  - We'll figure out secondary later
  - Tokens can be transferred to any DEX
  - No exchange/ATS relationship
  - Market making without BD license
### **Why Dangerous**
  Secondary market issues:
  - Unlicensed exchange operation
  - Market manipulation liability
  - No trade surveillance
  - Price discovery problems
  
  Operating an exchange without registration is a serious offense.
  Even "decentralized" venues have faced enforcement.
  
### **Prevention**
  - Plan secondary strategy from day one
  - Partner with registered ATS
  - Whitelist only compliant venues
  - Implement trade surveillance
  - Consider bulletin board only initially
### **Detection Patterns**
  - any.*exchange
  - dex.*listing
  - permissionless.*trading

## Insufficient Audit Trail

### **Id**
missing-audit-trail
### **Severity**
low
### **Description**
  Regulators expect complete audit trails. Every transfer, every
  verification, every compliance check should be logged with
  enough detail to reconstruct history.
  
### **Symptoms**
  - Minimal event emissions
  - No reason codes for rejections
  - No timestamp on verifications
  - No document hash linking
### **Why Dangerous**
  Audit failures cause:
  - Regulatory exam complications
  - Inability to prove compliance
  - Dispute resolution difficulties
  - Costly manual reconstruction
  
### **Prevention**
  - Comprehensive event emissions
  - Reason codes for all rejections
  - Document hash linking
  - Indexed events for efficient querying
  - Off-chain event storage
### **Detection Patterns**
  - no.*event
  - silent.*failure
  - no.*reason.*code

## Optimizing Gas at Expense of Compliance

### **Id**
gas-optimization-over-compliance
### **Severity**
low
### **Description**
  Gas optimization is important, but not at the cost of compliance
  checks. Skipping verifications to save gas creates vulnerabilities.
  
### **Symptoms**
  - Batched transfers skip individual checks
  - "Gas efficient mode" bypasses compliance
  - Cached verification to avoid re-checks
  - We check off-chain before on-chain
### **Why Dangerous**
  Gas shortcuts create:
  - Compliance bypass vectors
  - Race condition vulnerabilities
  - Audit findings
  - Potential enforcement issues
  
  Regulators don't care about gas costs. They care about compliance.
  
### **Prevention**
  - Always check compliance on-chain
  - Optimize within compliance bounds
  - If batching, still check each transfer
  - Layer 2 for gas reduction, not fewer checks
### **Detection Patterns**
  - skip.*compliance.*batch
  - gas.*efficient.*mode
  - cached.*verification