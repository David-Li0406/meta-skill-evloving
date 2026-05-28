# Rwa Tokenization - Validations

## Missing Transfer Compliance Check

### **Id**
missing-transfer-compliance-check
### **Severity**
critical
### **Title**
Transfer Without Compliance Check
### **Description**
  Security token transfers MUST check compliance before execution.
  Transfers without compliance checks violate securities laws.
  
### **Pattern**
  function\s+transfer\s*\([^)]*\)\s*(?:public|external)[^{]*\{(?:(?!compliance|canTransfer|isCompliant|checkCompliance)[^}])*\}
  
### **Languages**
  - solidity
### **Message**
  CRITICAL: Transfer function lacks compliance check.
  
  Security tokens must verify compliance before every transfer:
  - Identity verification (is recipient verified?)
  - Investor qualification (are they eligible?)
  - Transfer restrictions (holding period, jurisdiction, limits)
  
  Fix: Add compliance check before transfer
  ```solidity
  function transfer(address _to, uint256 _amount) public returns (bool) {
      require(compliance.canTransfer(msg.sender, _to, _amount), "Transfer not compliant");
      return super.transfer(_to, _amount);
  }
  ```
  
### **Fix Example**
  require(compliance.canTransfer(msg.sender, _to, _amount), "Transfer not compliant");
  

## Missing Identity Verification

### **Id**
missing-identity-verification
### **Severity**
critical
### **Title**
Transfer Without Identity Verification
### **Description**
  Both sender and recipient must have verified identities for
  security token transfers. Anonymous transfers are prohibited.
  
### **Pattern**
  function\s+transfer\s*\([^)]*\)\s*(?:public|external)[^{]*\{(?:(?!identityRegistry|isVerified|identity)[^}])*\}
  
### **Languages**
  - solidity
### **Message**
  CRITICAL: Transfer function lacks identity verification.
  
  All parties in a security token transfer must be verified:
  - Sender identity verified
  - Recipient identity verified
  - Identity not expired
  
  Fix: Check identity registry before transfer
  ```solidity
  require(identityRegistry.isVerified(msg.sender), "Sender not verified");
  require(identityRegistry.isVerified(_to), "Recipient not verified");
  ```
  

## Permissionless Minting

### **Id**
permissionless-minting
### **Severity**
critical
### **Title**
Permissionless Token Minting
### **Description**
  Security tokens represent real-world assets. Minting must be
  controlled and tied to actual asset issuance.
  
### **Pattern**
  function\s+mint\s*\([^)]*\)\s*(?:public|external)\s*(?!.*only|.*require\s*\(\s*msg\.sender)
  
### **Languages**
  - solidity
### **Message**
  CRITICAL: Mint function appears to be permissionless.
  
  Security token minting must be:
  - Restricted to authorized issuers
  - Tied to actual asset issuance
  - Recorded with proper documentation
  
  Fix: Add access control
  ```solidity
  function mint(address _to, uint256 _amount) external onlyIssuer {
      require(identityRegistry.isVerified(_to), "Recipient not verified");
      _mint(_to, _amount);
  }
  ```
  

## No Forced Transfer

### **Id**
no-forced-transfer
### **Severity**
critical
### **Title**
Missing Forced Transfer Capability
### **Description**
  Securities must support forced transfers for court orders,
  estate settlements, and regulatory requirements.
  
### **Pattern**
  contract\s+\w+[^{]*\{(?:(?!forcedTransfer|forceTransfer|recoverTokens)[^}])*\}
  
### **Languages**
  - solidity
### **File Pattern**
Token.sol|SecurityToken.sol|RWA.sol
### **Message**
  CRITICAL: Contract lacks forced transfer mechanism.
  
  Legal requirements may mandate token recovery/transfer:
  - Court orders
  - Estate settlements
  - Regulatory seizures
  - Lost key recovery
  
  Fix: Implement forced transfer with proper controls
  ```solidity
  function forcedTransfer(
      address _from,
      address _to,
      uint256 _amount,
      bytes32 _legalOrderHash
  ) external onlyAgent {
      require(_legalOrderHash != bytes32(0), "Legal order required");
      emit ForcedTransfer(_from, _to, _amount, _legalOrderHash);
      _transfer(_from, _to, _amount);
  }
  ```
  

## No Holding Period Check

### **Id**
no-holding-period-check
### **Severity**
high
### **Title**
Missing Holding Period Enforcement
### **Description**
  Reg D, Reg S, and Rule 144 require holding periods before
  resale. Transfers must check holding period compliance.
  
### **Pattern**
  function\s+(?:transfer|canTransfer)\s*\([^)]*\)[^{]*\{(?:(?!holdingPeriod|acquisitionDate|lockup|vestingEnd)[^}])*\}
  
### **Languages**
  - solidity
### **Message**
  HIGH: Transfer logic lacks holding period enforcement.
  
  Securities laws require holding periods:
  - Reg D 506(b/c): 12 months
  - Reg S: 40 days (distribution compliance period)
  - Rule 144: 6-12 months
  
  Fix: Track and enforce holding periods
  ```solidity
  require(
      block.timestamp - acquisitionDate[_from] >= HOLDING_PERIOD,
      "Holding period not met"
  );
  ```
  

## Oracle No Staleness Check

### **Id**
oracle-no-staleness-check
### **Severity**
high
### **Title**
Oracle Without Staleness Check
### **Description**
  Oracle data can become stale. Using stale data for asset
  valuations creates arbitrage opportunities.
  
### **Pattern**
  oracle\.(?:getPrice|getValuation|getValue)\s*\([^)]*\)(?:(?!lastUpdated|staleness|timestamp|fresh)[^;]*);
  
### **Languages**
  - solidity
### **Message**
  HIGH: Oracle call without staleness check.
  
  Stale oracle data is dangerous:
  - Arbitrage attacks
  - Incorrect NAV calculations
  - Wrong dividend amounts
  
  Fix: Always check oracle freshness
  ```solidity
  (uint256 value, uint256 timestamp) = oracle.getValuation(assetId);
  require(block.timestamp - timestamp < STALENESS_THRESHOLD, "Oracle data stale");
  ```
  

## Kyc No Expiration

### **Id**
kyc-no-expiration
### **Severity**
high
### **Title**
KYC Verification Without Expiration
### **Description**
  KYC/accreditation status changes over time. Verifications
  must have expiration dates and be rechecked.
  
### **Pattern**
  isVerified\s*\[\s*\w+\s*\]\s*=\s*true\s*;(?:(?!expir|validUntil)[^;]*);
  
### **Languages**
  - solidity
### **Message**
  HIGH: KYC verification set without expiration.
  
  Investor status changes:
  - Accreditation can be lost
  - Sanctions lists update
  - PEP status changes
  
  Fix: Include expiration in verification
  ```solidity
  verifications[_investor] = Verification({
      isValid: true,
      verifiedAt: block.timestamp,
      expiresAt: block.timestamp + 90 days
  });
  ```
  

## No Investor Limit Check

### **Id**
no-investor-limit-check
### **Severity**
high
### **Title**
Missing Investor Count Limits
### **Description**
  Reg D 506(b) limits non-accredited investors to 35.
  Section 12(g) triggers at 2000 investors. Must enforce limits.
  
### **Pattern**
  function\s+(?:transfer|onboard|whitelist)\s*\([^)]*\)[^{]*\{(?:(?!investorCount|holderCount|maxInvestors)[^}])*\}
  
### **Languages**
  - solidity
### **File Pattern**
Compliance.sol|Token.sol|Whitelist.sol
### **Message**
  HIGH: No investor count limit enforcement.
  
  Regulatory limits:
  - Reg D 506(b): 35 non-accredited
  - Section 12(g): 2000 total triggers registration
  
  Fix: Track and enforce investor limits
  ```solidity
  if (balanceOf(_to) == 0) {
      require(investorCount < MAX_INVESTORS, "Investor limit reached");
      investorCount++;
  }
  ```
  

## No Jurisdiction Check

### **Id**
no-jurisdiction-check
### **Severity**
high
### **Title**
Missing Jurisdiction Verification
### **Description**
  Different jurisdictions have different rules. Must verify
  investor jurisdiction and apply appropriate restrictions.
  
### **Pattern**
  function\s+canTransfer\s*\([^)]*\)[^{]*\{(?:(?!country|jurisdiction|region)[^}])*\}
  
### **Languages**
  - solidity
### **Message**
  HIGH: Compliance check lacks jurisdiction verification.
  
  Jurisdiction matters:
  - US: Reg D, Reg S, Reg A+ rules
  - EU: MiCA requirements
  - Singapore: MAS rules
  - Sanctions: OFAC blocked countries
  
  Fix: Check jurisdiction in compliance
  ```solidity
  uint16 country = identityRegistry.getCountry(_to);
  require(!blockedCountries[country], "Jurisdiction blocked");
  require(jurisdictionCompliance[country].isCompliant(_to), "Jurisdiction not compliant");
  ```
  

## Integer Division Dividend

### **Id**
integer-division-dividend
### **Severity**
high
### **Title**
Integer Division in Dividend Calculation
### **Description**
  Integer division without precision handling causes rounding
  errors that accumulate across many investors.
  
### **Pattern**
  (?:dividend|distribution|amount)\s*[=/]\s*\w+\s*\/\s*(?:totalSupply|supply|holders)
  
### **Languages**
  - solidity
### **Message**
  HIGH: Integer division in dividend calculation.
  
  At scale, rounding errors are material:
  - 10,000 investors with $0.01 error each = $100 per distribution
  - Compounds over time
  
  Fix: Use high precision with proper rounding
  ```solidity
  uint256 constant PRECISION = 1e18;
  
  function calculateDividend(address _holder) internal view returns (uint256) {
      uint256 preciseAmount = (totalDividend * PRECISION) / totalSupply;
      return (preciseAmount * balanceOf(_holder)) / PRECISION;
  }
  ```
  

## No Transfer Event Reason

### **Id**
no-transfer-event-reason
### **Severity**
medium
### **Title**
Transfer Rejection Without Reason
### **Description**
  When transfers are rejected, emit specific reason codes for
  audit trail and debugging.
  
### **Pattern**
  revert\s*\(\s*\)\s*;|require\s*\([^,]+\)\s*;(?:(?!,)[^;])*$
  
### **Languages**
  - solidity
### **Message**
  MEDIUM: Transfer rejection lacks reason code.
  
  Audit trails require:
  - Why was transfer rejected?
  - Which compliance rule failed?
  - What can investor do to resolve?
  
  Fix: Include reason in rejection
  ```solidity
  require(isVerified[_to], "RECIPIENT_NOT_VERIFIED");
  require(holdingPeriodMet[_from], "HOLDING_PERIOD_NOT_MET");
  require(!sanctioned[_to], "RECIPIENT_SANCTIONED");
  ```
  

## No Compliance Event

### **Id**
no-compliance-event
### **Severity**
medium
### **Title**
Compliance Action Without Event
### **Description**
  All compliance actions should emit events for audit trail.
  Silent state changes make auditing impossible.
  
### **Pattern**
  function\s+(?:verify|whitelist|blacklist|freeze|unfreeze)\s*\([^)]*\)[^{]*\{(?:(?!emit)[^}])*\}
  
### **Languages**
  - solidity
### **Message**
  MEDIUM: Compliance action lacks event emission.
  
  Audit requirements:
  - All verifications logged
  - All freezes with reason
  - All compliance changes traceable
  
  Fix: Emit event for compliance actions
  ```solidity
  function verify(address _investor) external onlyAgent {
      isVerified[_investor] = true;
      emit InvestorVerified(_investor, msg.sender, block.timestamp);
  }
  ```
  

## Upgrade Without Timelock

### **Id**
upgrade-without-timelock
### **Severity**
medium
### **Title**
Upgradeable Contract Without Timelock
### **Description**
  Compliance modules should have timelocks on upgrades to prevent
  instant rule changes that could harm investors.
  
### **Pattern**
  function\s+(?:upgrade|setCompliance|setModule)\s*\([^)]*\)\s*(?:external|public)[^{]*\{(?:(?!timelock|delay)[^}])*\}
  
### **Languages**
  - solidity
### **Message**
  MEDIUM: Upgrade function lacks timelock.
  
  Investor protection requires:
  - Advance notice of rule changes
  - Time to exit if they disagree
  - Governance oversight
  
  Fix: Add timelock to upgrades
  ```solidity
  uint256 public constant UPGRADE_DELAY = 48 hours;
  
  function proposeUpgrade(address _newModule) external onlyOwner {
      pendingUpgrade = _newModule;
      upgradeTime = block.timestamp + UPGRADE_DELAY;
      emit UpgradeProposed(_newModule, upgradeTime);
  }
  
  function executeUpgrade() external {
      require(block.timestamp >= upgradeTime, "Timelock not expired");
      complianceModule = pendingUpgrade;
      emit UpgradeExecuted(pendingUpgrade);
  }
  ```
  

## Single Admin Control

### **Id**
single-admin-control
### **Severity**
medium
### **Title**
Single Admin Controls Critical Functions
### **Description**
  Critical compliance functions should require multi-sig or
  governance, not single admin control.
  
### **Pattern**
  modifier\s+onlyOwner|require\s*\(\s*msg\.sender\s*==\s*owner\s*\)
  
### **Languages**
  - solidity
### **File Pattern**
Compliance.sol|Identity.sol|Token.sol
### **Message**
  MEDIUM: Single admin controls compliance functions.
  
  Risk of:
  - Single point of failure
  - Insider abuse
  - Key compromise
  
  Fix: Use multi-sig or DAO governance
  ```solidity
  modifier onlyGovernance() {
      require(
          governance.hasRole(msg.sender, COMPLIANCE_ADMIN),
          "Not authorized"
      );
      _;
  }
  ```
  

## Missing Natspec

### **Id**
missing-natspec
### **Severity**
low
### **Title**
Missing NatSpec Documentation
### **Description**
  Compliance functions should have thorough NatSpec documentation
  for legal review and audit purposes.
  
### **Pattern**
  ^\s*function\s+(?!_)\w+\s*\([^)]*\)[^{/]*\{
  
### **Languages**
  - solidity
### **File Pattern**
Compliance.sol|Token.sol|Identity.sol
### **Message**
  LOW: Function lacks NatSpec documentation.
  
  Documentation helps:
  - Legal review understanding
  - Audit clarity
  - Maintenance
  
  Fix: Add NatSpec
  ```solidity
  /// @notice Verifies an investor's identity and qualification
  /// @dev Only callable by authorized verification agents
  /// @param _investor Address of the investor to verify
  /// @param _country ISO 3166-1 numeric country code
  /// @param _qualification Type of investor qualification
  function verify(
      address _investor,
      uint16 _country,
      QualificationType _qualification
  ) external onlyAgent {
      // ...
  }
  ```
  

## Magic Numbers

### **Id**
magic-numbers
### **Severity**
low
### **Title**
Magic Numbers in Compliance Logic
### **Description**
  Compliance thresholds and limits should be named constants
  for clarity and maintainability.
  
### **Pattern**
  (?:require|if)\s*\([^)]*(?:365|90|35|2000)\s*(?:days|)\s*[^)]*\)
  
### **Languages**
  - solidity
### **Message**
  LOW: Magic number in compliance logic.
  
  Use named constants for:
  - Clarity of intent
  - Easy updates
  - Audit clarity
  
  Fix: Use named constants
  ```solidity
  uint256 public constant REG_D_HOLDING_PERIOD = 365 days;
  uint256 public constant KYC_VALIDITY_PERIOD = 90 days;
  uint256 public constant MAX_NON_ACCREDITED = 35;
  uint256 public constant SEC_12G_THRESHOLD = 2000;
  ```
  