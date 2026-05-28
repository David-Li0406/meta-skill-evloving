# RWA Tokenization Specialist

## Patterns


---
  #### **Name**
ERC-3643 (T-REX) Implementation
  #### **Description**
    The gold standard for compliant security tokens. Always implement the full
    T-REX stack: Token, Identity Registry, Compliance, and Claims.
    
  #### **Example**
    // CORRECT: Full T-REX implementation with compliance checks
    contract RWAToken is Token {
        IIdentityRegistry public identityRegistry;
        ICompliance public compliance;
    
        function transfer(address _to, uint256 _value)
            public
            override
            returns (bool)
        {
            require(
                identityRegistry.isVerified(_to),
                "Recipient not verified"
            );
            require(
                compliance.canTransfer(msg.sender, _to, _value),
                "Transfer not compliant"
            );
            return super.transfer(_to, _value);
        }
    }
    
  #### **Why**
    ERC-3643 is the only standard with real regulatory adoption. It's been
    approved by multiple regulators and has a proven track record. Rolling
    your own compliance logic is asking for trouble.
    

---
  #### **Name**
Layered Compliance Architecture
  #### **Description**
    Build compliance in layers: identity verification, investor qualification,
    transfer restrictions, and jurisdictional rules. Each layer is independent
    and can be updated without affecting others.
    
  #### **Example**
    // Layer 1: Identity - Is this a real, verified person/entity?
    contract IdentityRegistry {
        mapping(address => Identity) public identities;
        mapping(address => bool) public isVerified;
    
        function registerIdentity(
            address _investor,
            uint16 _country,
            bytes32 _identityHash
        ) external onlyAgent {
            identities[_investor] = Identity({
                country: _country,
                identityHash: _identityHash,
                verifiedAt: block.timestamp,
                expiresAt: block.timestamp + 90 days
            });
            isVerified[_investor] = true;
        }
    }
    
    // Layer 2: Qualification - Are they eligible to hold this security?
    contract InvestorQualification {
        mapping(address => QualificationStatus) public qualifications;
    
        enum QualificationType {
            ACCREDITED_US,      // Rule 501
            QUALIFIED_PURCHASER, // >$5M investments
            NON_US_PERSON,      // Reg S eligible
            RETAIL_REG_A        // Reg A+ retail
        }
    
        function setQualification(
            address _investor,
            QualificationType _type,
            uint256 _expiresAt
        ) external onlyCompliance {
            qualifications[_investor] = QualificationStatus({
                qualificationType: _type,
                verifiedAt: block.timestamp,
                expiresAt: _expiresAt
            });
        }
    }
    
    // Layer 3: Transfer Rules - Can this specific transfer happen?
    contract TransferCompliance {
        function canTransfer(
            address _from,
            address _to,
            uint256 _amount
        ) external view returns (bool) {
            // Check holding period (Reg D = 12 months)
            if (holdingPeriod[_from] < 12 months) {
                // Can only transfer to other accredited investors
                require(
                    qualifications[_to].qualificationType == ACCREDITED_US,
                    "Holding period not met"
                );
            }
    
            // Check investor count limits (Reg D 506(b) = 35 non-accredited)
            if (!isAccredited[_to] && balanceOf(_to) == 0) {
                require(
                    nonAccreditedCount < 35,
                    "Non-accredited investor limit reached"
                );
            }
    
            return true;
        }
    }
    
  #### **Why**
    Regulations change. Layered architecture means you can update KYC
    requirements without touching transfer logic, or add a new jurisdiction
    without rewriting identity verification. I've seen monolithic compliance
    contracts become unmaintainable nightmares.
    

---
  #### **Name**
Oracle Integration for Off-Chain Assets
  #### **Description**
    Real-world assets exist off-chain. You need reliable oracle infrastructure
    to bring asset state (valuations, ownership records, physical condition)
    on-chain with appropriate safeguards.
    
  #### **Example**
    contract RWAOracle {
        struct AssetState {
            uint256 valuation;
            uint256 lastUpdated;
            bytes32 documentHash;  // IPFS hash of valuation report
            address appraiser;
            bool isValid;
        }
    
        uint256 public constant STALENESS_THRESHOLD = 24 hours;
        uint256 public constant MAX_PRICE_DEVIATION = 10; // 10%
    
        mapping(bytes32 => AssetState) public assetStates;
        mapping(address => bool) public authorizedAppraisers;
    
        function updateValuation(
            bytes32 _assetId,
            uint256 _newValuation,
            bytes32 _documentHash
        ) external onlyAuthorizedAppraiser {
            AssetState storage state = assetStates[_assetId];
    
            // Circuit breaker: reject wild price swings
            if (state.valuation > 0) {
                uint256 deviation = calculateDeviation(
                    state.valuation,
                    _newValuation
                );
                require(
                    deviation <= MAX_PRICE_DEVIATION,
                    "Price deviation too high - manual review required"
                );
            }
    
            state.valuation = _newValuation;
            state.lastUpdated = block.timestamp;
            state.documentHash = _documentHash;
            state.appraiser = msg.sender;
            state.isValid = true;
    
            emit ValuationUpdated(_assetId, _newValuation, msg.sender);
        }
    
        function getValuation(bytes32 _assetId)
            external
            view
            returns (uint256, bool)
        {
            AssetState memory state = assetStates[_assetId];
    
            // Check staleness
            bool isFresh = block.timestamp - state.lastUpdated < STALENESS_THRESHOLD;
    
            return (state.valuation, state.isValid && isFresh);
        }
    }
    
  #### **Why**
    The oracle is your bridge to reality. If it fails, your token's
    connection to the underlying asset is broken. I've seen catastrophic
    arbitrage when oracles go stale. Build in staleness checks, circuit
    breakers, and multiple data sources.
    

---
  #### **Name**
Dividend Distribution Automation
  #### **Description**
    Automate dividend and distribution payments with proper record dates,
    claim periods, and tax withholding.
    
  #### **Example**
    contract DividendDistributor {
        struct Distribution {
            uint256 totalAmount;
            uint256 recordDate;
            uint256 paymentDate;
            uint256 claimDeadline;
            uint256 amountPerToken;
            IERC20 paymentToken;
            bool isProcessed;
        }
    
        mapping(uint256 => Distribution) public distributions;
        mapping(uint256 => mapping(address => bool)) public hasClaimed;
        mapping(address => uint256) public withholdingRate; // Basis points
    
        function createDistribution(
            uint256 _totalAmount,
            uint256 _recordDate,
            address _paymentToken
        ) external onlyIssuer {
            require(
                _recordDate > block.timestamp,
                "Record date must be in future"
            );
    
            uint256 distId = distributionCount++;
    
            distributions[distId] = Distribution({
                totalAmount: _totalAmount,
                recordDate: _recordDate,
                paymentDate: _recordDate + 5 days,
                claimDeadline: _recordDate + 90 days,
                amountPerToken: _totalAmount / totalSupplyAtRecordDate,
                paymentToken: IERC20(_paymentToken),
                isProcessed: false
            });
    
            // Snapshot balances at record date
            _snapshotBalances(distId, _recordDate);
        }
    
        function claimDividend(uint256 _distId) external {
            Distribution storage dist = distributions[_distId];
    
            require(block.timestamp >= dist.paymentDate, "Payment date not reached");
            require(block.timestamp < dist.claimDeadline, "Claim period expired");
            require(!hasClaimed[_distId][msg.sender], "Already claimed");
    
            uint256 balance = snapshotBalances[_distId][msg.sender];
            require(balance > 0, "No tokens at record date");
    
            uint256 grossAmount = balance * dist.amountPerToken;
            uint256 withholding = grossAmount * withholdingRate[msg.sender] / 10000;
            uint256 netAmount = grossAmount - withholding;
    
            hasClaimed[_distId][msg.sender] = true;
    
            dist.paymentToken.transfer(msg.sender, netAmount);
            if (withholding > 0) {
                dist.paymentToken.transfer(taxWithholdingAddress, withholding);
            }
    
            emit DividendClaimed(_distId, msg.sender, netAmount, withholding);
        }
    }
    
  #### **Why**
    Manual dividend distribution is error-prone and doesn't scale. On-chain
    automation with proper record dates and withholding ensures every investor
    gets exactly what they're owed, with audit trails for tax reporting.
    

---
  #### **Name**
Transfer Agent Integration
  #### **Description**
    Securities must have a registered transfer agent. Build integration
    points that allow the transfer agent to maintain the official
    shareholder registry while blockchain handles the operational layer.
    
  #### **Example**
    contract TransferAgentBridge {
        address public transferAgent;
    
        struct PendingTransfer {
            address from;
            address to;
            uint256 amount;
            uint256 submittedAt;
            TransferStatus status;
        }
    
        enum TransferStatus { PENDING, APPROVED, REJECTED, SETTLED }
    
        mapping(bytes32 => PendingTransfer) public pendingTransfers;
    
        // Two-phase commit for transfer agent approval
        function initiateTransfer(
            address _to,
            uint256 _amount
        ) external returns (bytes32) {
            bytes32 transferId = keccak256(
                abi.encodePacked(msg.sender, _to, _amount, block.timestamp)
            );
    
            // Lock tokens
            _lock(msg.sender, _amount);
    
            pendingTransfers[transferId] = PendingTransfer({
                from: msg.sender,
                to: _to,
                amount: _amount,
                submittedAt: block.timestamp,
                status: TransferStatus.PENDING
            });
    
            emit TransferInitiated(transferId, msg.sender, _to, _amount);
    
            return transferId;
        }
    
        function approveTransfer(bytes32 _transferId)
            external
            onlyTransferAgent
        {
            PendingTransfer storage transfer = pendingTransfers[_transferId];
            require(transfer.status == TransferStatus.PENDING, "Invalid status");
    
            transfer.status = TransferStatus.APPROVED;
    
            // Execute the transfer
            _unlock(transfer.from, transfer.amount);
            _transfer(transfer.from, transfer.to, transfer.amount);
    
            transfer.status = TransferStatus.SETTLED;
    
            emit TransferSettled(_transferId);
        }
    
        function rejectTransfer(
            bytes32 _transferId,
            string calldata _reason
        ) external onlyTransferAgent {
            PendingTransfer storage transfer = pendingTransfers[_transferId];
            require(transfer.status == TransferStatus.PENDING, "Invalid status");
    
            transfer.status = TransferStatus.REJECTED;
    
            // Return tokens
            _unlock(transfer.from, transfer.amount);
    
            emit TransferRejected(_transferId, _reason);
        }
    }
    
  #### **Why**
    In the US, SEC Rule 17Ad requires registered transfer agents for
    securities. The blockchain is an operational layer, but the transfer
    agent maintains the legal record. Build bridges, not replacements.
    

## Anti-Patterns


---
  #### **Name**
Treating Security Tokens Like Utility Tokens
  #### **Description**
    Security tokens are fundamentally different from utility tokens. They
    represent ownership in real assets and are subject to securities laws.
    You cannot use the same permissionless, anonymous patterns.
    
  #### **Bad Example**
    // WRONG: Permissionless transfer like a utility token
    contract BadSecurityToken is ERC20 {
        function transfer(address to, uint256 amount)
            public
            override
            returns (bool)
        {
            // No compliance checks!
            return super.transfer(to, amount);
        }
    }
    
  #### **Good Example**
    // CORRECT: Compliance-gated transfers
    contract CompliantSecurityToken is Token {
        ICompliance public compliance;
        IIdentityRegistry public identityRegistry;
    
        function transfer(address _to, uint256 _amount)
            public
            override
            returns (bool)
        {
            require(identityRegistry.isVerified(msg.sender), "Sender not verified");
            require(identityRegistry.isVerified(_to), "Recipient not verified");
            require(
                compliance.canTransfer(msg.sender, _to, _amount),
                "Transfer not compliant"
            );
            return super.transfer(_to, _amount);
        }
    }
    
  #### **Why**
    This is how projects get SEC enforcement actions. A security token
    without transfer restrictions is an illegal unregistered security
    offering. Full stop.
    

---
  #### **Name**
Hardcoding Compliance Rules
  #### **Description**
    Regulations change. Jurisdictions have different rules. Hardcoding
    compliance logic makes your token inflexible and requires contract
    upgrades (which may not even be possible) when rules change.
    
  #### **Bad Example**
    // WRONG: Hardcoded compliance
    function canTransfer(address from, address to) internal view returns (bool) {
        // Hardcoded 12-month holding period
        require(block.timestamp - purchaseTime[from] > 365 days);
        // Hardcoded US-only
        require(country[to] == "US");
        // Hardcoded accredited-only
        require(isAccredited[to]);
        return true;
    }
    
  #### **Good Example**
    // CORRECT: Modular compliance with upgradeable rules
    contract ModularCompliance is ICompliance {
        mapping(address => bool) public complianceModules;
    
        function addComplianceModule(address _module) external onlyOwner {
            complianceModules[_module] = true;
        }
    
        function removeComplianceModule(address _module) external onlyOwner {
            complianceModules[_module] = false;
        }
    
        function canTransfer(
            address _from,
            address _to,
            uint256 _amount
        ) external view override returns (bool) {
            address[] memory modules = getActiveModules();
    
            for (uint i = 0; i < modules.length; i++) {
                if (!IComplianceModule(modules[i]).checkCompliance(
                    _from, _to, _amount
                )) {
                    return false;
                }
            }
            return true;
        }
    }
    
  #### **Why**
    I've seen offerings have to be completely restructured because
    compliance rules were hardcoded. Modular compliance lets you
    adapt without contract replacement.
    

---
  #### **Name**
Ignoring Holding Period Requirements
  #### **Description**
    Most private securities have mandatory holding periods (Rule 144,
    Reg D, Reg S). Tokens that allow immediate trading violate these
    restrictions and expose issuers to liability.
    
  #### **Bad Example**
    // WRONG: No holding period enforcement
    function transfer(address to, uint256 amount) public returns (bool) {
        // Anyone can transfer anytime
        _transfer(msg.sender, to, amount);
        return true;
    }
    
  #### **Good Example**
    // CORRECT: Enforce holding periods per regulation
    contract HoldingPeriodCompliance is IComplianceModule {
        mapping(address => uint256) public acquisitionDate;
    
        // Different holding periods for different exemptions
        uint256 public constant REG_D_HOLDING = 365 days;   // 12 months
        uint256 public constant REG_S_HOLDING = 40 days;    // Distribution compliance period
        uint256 public constant RULE_144_HOLDING = 180 days; // 6 months if reporting
    
        function checkCompliance(
            address _from,
            address _to,
            uint256 _amount
        ) external view override returns (bool) {
            uint256 holdingPeriod = getRequiredHoldingPeriod(_from);
            uint256 heldFor = block.timestamp - acquisitionDate[_from];
    
            if (heldFor < holdingPeriod) {
                // During holding period, can only transfer to qualified buyers
                return isQualifiedBuyer(_to);
            }
    
            return true;
        }
    }
    
  #### **Why**
    Holding period violations are one of the most common issues in
    tokenized securities. They expose the issuer to rescission rights
    and potential SEC action.
    

---
  #### **Name**
Single Point of Failure for Identity
  #### **Description**
    Relying on a single identity provider creates fragility. If that
    provider goes down or loses their license, your entire token stops
    functioning.
    
  #### **Bad Example**
    // WRONG: Single identity provider
    contract SingleProviderIdentity {
        address public kycProvider;
    
        function isVerified(address _user) external view returns (bool) {
            return IKYCProvider(kycProvider).isVerified(_user);
        }
    }
    
  #### **Good Example**
    // CORRECT: Multiple identity providers with fallback
    contract MultiProviderIdentity {
        address[] public kycProviders;
        uint256 public requiredVerifications = 1;
    
        function isVerified(address _user) external view returns (bool) {
            uint256 verificationCount = 0;
    
            for (uint i = 0; i < kycProviders.length; i++) {
                if (IKYCProvider(kycProviders[i]).isVerified(_user)) {
                    verificationCount++;
                    if (verificationCount >= requiredVerifications) {
                        return true;
                    }
                }
            }
    
            return false;
        }
    
        function addProvider(address _provider) external onlyOwner {
            kycProviders.push(_provider);
        }
    }
    
  #### **Why**
    KYC providers can have outages, lose licenses, or go out of business.
    Multiple provider support ensures business continuity and gives
    investors options.
    

---
  #### **Name**
Missing Forced Transfer Capability
  #### **Description**
    Legal systems sometimes require forced transfers (court orders,
    estate settlements, regulatory seizures). Tokens without this
    capability may be non-compliant.
    
  #### **Bad Example**
    // WRONG: No mechanism for legal forced transfers
    contract NoForcedTransfer is ERC20 {
        // Only voluntary transfers possible
        // What happens when an investor dies?
        // What happens with a court order?
    }
    
  #### **Good Example**
    // CORRECT: Agent-controlled forced transfer for legal compliance
    contract CompliantToken is Token {
        mapping(address => bool) public agents;
    
        // For court orders, estate settlements, regulatory requirements
        function forcedTransfer(
            address _from,
            address _to,
            uint256 _amount,
            bytes32 _legalOrderHash  // Hash of legal document
        ) external onlyAgent returns (bool) {
            require(_legalOrderHash != bytes32(0), "Legal order required");
    
            emit ForcedTransfer(_from, _to, _amount, _legalOrderHash, msg.sender);
    
            _transfer(_from, _to, _amount);
    
            return true;
        }
    
        // For regulatory freeze requirements
        function freeze(address _account) external onlyAgent {
            frozen[_account] = true;
            emit AccountFrozen(_account, msg.sender);
        }
    }
    
  #### **Why**
    Securities laws require issuers to be able to enforce legal orders.
    A token that can't accommodate court orders is legally problematic
    and may be considered non-compliant.
    