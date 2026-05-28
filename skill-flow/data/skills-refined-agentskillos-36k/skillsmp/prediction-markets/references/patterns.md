# Prediction Markets Engineer

## Patterns


---
  #### **Id**
conditional-tokens
  #### **Name**
Conditional Tokens Framework
  #### **Description**
    Gnosis CTF for creating outcome tokens that represent positions
    in prediction markets
    
  #### **When To Use**
    - Building prediction market platform
    - Creating event-based tokens
    - Composable prediction markets
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    import "@gnosis.pm/conditional-tokens-contracts/contracts/ConditionalTokens.sol";
    
    contract PredictionMarket {
        ConditionalTokens public ctf;
        IERC20 public collateral;
    
        struct Market {
            bytes32 conditionId;
            bytes32 questionId;
            address oracle;
            uint256 outcomeCount;
            uint256 resolutionTime;
            bool resolved;
        }
    
        mapping(bytes32 => Market) public markets;
    
        constructor(address _ctf, address _collateral) {
            ctf = ConditionalTokens(_ctf);
            collateral = IERC20(_collateral);
        }
    
        function createMarket(
            bytes32 questionId,
            address oracle,
            uint256 outcomeCount,
            uint256 resolutionTime
        ) external returns (bytes32 marketId) {
            // Prepare condition in CTF
            ctf.prepareCondition(oracle, questionId, outcomeCount);
            bytes32 conditionId = ctf.getConditionId(oracle, questionId, outcomeCount);
    
            marketId = keccak256(abi.encode(conditionId, block.timestamp));
            markets[marketId] = Market({
                conditionId: conditionId,
                questionId: questionId,
                oracle: oracle,
                outcomeCount: outcomeCount,
                resolutionTime: resolutionTime,
                resolved: false
            });
    
            return marketId;
        }
    
        function buyOutcome(
            bytes32 marketId,
            uint256 outcomeIndex,
            uint256 amount
        ) external {
            Market storage market = markets[marketId];
            require(!market.resolved, "Market resolved");
    
            // Transfer collateral
            collateral.transferFrom(msg.sender, address(this), amount);
            collateral.approve(address(ctf), amount);
    
            // Create index set for desired outcome
            uint256 indexSet = 1 << outcomeIndex;
            uint256[] memory partition = new uint256[](1);
            partition[0] = indexSet;
    
            // Split position to get outcome tokens
            bytes32 parentCollectionId = bytes32(0);
            ctf.splitPosition(
                collateral,
                parentCollectionId,
                market.conditionId,
                partition,
                amount
            );
    
            // Transfer outcome tokens to user
            bytes32 collectionId = ctf.getCollectionId(
                parentCollectionId,
                market.conditionId,
                indexSet
            );
            uint256 positionId = ctf.getPositionId(collateral, collectionId);
            // User now holds outcome tokens
        }
    }
    
    CTF Position Structure:
    ┌─────────────────────────────────────────────────────────┐
    │ Market: "Will ETH reach $5000 by Dec 2025?"             │
    ├─────────────────────────────────────────────────────────┤
    │ Condition ID: 0x123...                                  │
    │ Outcomes: [YES, NO]                                     │
    ├─────────────────────────────────────────────────────────┤
    │ YES Token: ERC1155 position, pays $1 if YES             │
    │ NO Token: ERC1155 position, pays $1 if NO               │
    │                                                         │
    │ $1 collateral = 1 YES token + 1 NO token                │
    │ After resolution, winning token redeemable for $1       │
    └─────────────────────────────────────────────────────────┘
    
  #### **Security Notes**
    - Oracle security is critical
    - Consider dispute period before resolution
    - Handle edge cases (market cancellation)

---
  #### **Id**
uma-optimistic-oracle
  #### **Name**
UMA Optimistic Oracle Integration
  #### **Description**
    Dispute-based oracle for real-world event resolution with
    economic guarantees
    
  #### **When To Use**
    - Resolving prediction markets
    - Any real-world data on-chain
    - When decentralized resolution needed
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    import "@uma/core/contracts/optimistic-oracle-v3/interfaces/OptimisticOracleV3Interface.sol";
    
    contract UMAMarketResolver {
        OptimisticOracleV3Interface public oracle;
        IERC20 public bondToken;
        uint256 public constant BOND_AMOUNT = 5000e18; // 5000 USDC
        uint64 public constant LIVENESS = 7200; // 2 hours
    
        struct Resolution {
            bytes32 assertionId;
            bytes32 marketId;
            bool outcome;
            bool resolved;
        }
    
        mapping(bytes32 => Resolution) public resolutions;
    
        function proposeResolution(
            bytes32 marketId,
            bool outcome,
            string calldata explanation
        ) external returns (bytes32 assertionId) {
            // Build claim
            bytes memory claim = abi.encodePacked(
                "Market ", marketId,
                " resolved to ", outcome ? "YES" : "NO",
                ". ", explanation
            );
    
            // Approve bond
            bondToken.transferFrom(msg.sender, address(this), BOND_AMOUNT);
            bondToken.approve(address(oracle), BOND_AMOUNT);
    
            // Submit assertion
            assertionId = oracle.assertTruth(
                claim,
                msg.sender,      // asserter
                address(this),   // callback recipient
                address(0),      // escalation manager (none)
                LIVENESS,
                bondToken,
                BOND_AMOUNT,
                bytes32(0),      // identifier
                bytes32(0)       // domain
            );
    
            resolutions[assertionId] = Resolution({
                assertionId: assertionId,
                marketId: marketId,
                outcome: outcome,
                resolved: false
            });
    
            return assertionId;
        }
    
        // UMA callback when assertion settles
        function assertionResolvedCallback(
            bytes32 assertionId,
            bool assertedTruthfully
        ) external {
            require(msg.sender == address(oracle), "Only oracle");
    
            Resolution storage res = resolutions[assertionId];
            if (assertedTruthfully) {
                // Resolution accepted - finalize market
                res.resolved = true;
                _resolveMarket(res.marketId, res.outcome);
            } else {
                // Disputed and overturned - proposer loses bond
                delete resolutions[assertionId];
            }
        }
    }
    
    UMA Resolution Flow:
    1. Proposer asserts outcome with bond
    2. 2-hour dispute window
    3. If disputed:
       - Goes to UMA DVM (decentralized voting)
       - UMA token holders vote on truth
       - Wrong party loses bond
    4. If undisputed: assertion accepted
    
  #### **Security Notes**
    - Bond amount must deter false proposals
    - Liveness period for dispute opportunity
    - Handle callback failures gracefully

---
  #### **Id**
amm-prediction
  #### **Name**
CPMM for Prediction Markets
  #### **Description**
    Constant Product Market Maker adapted for binary outcome
    token trading
    
  #### **When To Use**
    - Providing liquidity to prediction markets
    - Automated market making
    - Price discovery for outcomes
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    contract PredictionAMM {
        IERC1155 public outcomeTokens;
        uint256 public yesTokenId;
        uint256 public noTokenId;
    
        uint256 public yesReserve;
        uint256 public noReserve;
        uint256 public constant FEE_BPS = 20; // 0.2%
    
        function addLiquidity(uint256 amount) external {
            // Add equal amounts of both outcomes
            outcomeTokens.safeTransferFrom(msg.sender, address(this), yesTokenId, amount, "");
            outcomeTokens.safeTransferFrom(msg.sender, address(this), noTokenId, amount, "");
    
            yesReserve += amount;
            noReserve += amount;
    
            // Mint LP tokens
            _mintLP(msg.sender, amount);
        }
    
        function buyYes(uint256 noIn) external returns (uint256 yesOut) {
            // Constant product: (yesReserve - yesOut) * (noReserve + noIn) = k
            uint256 noInWithFee = noIn * (10000 - FEE_BPS) / 10000;
            yesOut = (yesReserve * noInWithFee) / (noReserve + noInWithFee);
    
            outcomeTokens.safeTransferFrom(msg.sender, address(this), noTokenId, noIn, "");
            outcomeTokens.safeTransfer(msg.sender, yesTokenId, yesOut);
    
            yesReserve -= yesOut;
            noReserve += noIn;
        }
    
        function getYesPrice() public view returns (uint256) {
            // Price of YES token in terms of NO token
            // price = noReserve / (yesReserve + noReserve)
            return (noReserve * 1e18) / (yesReserve + noReserve);
        }
    
        function getImpliedProbability() public view returns (uint256) {
            // YES price = implied probability of YES outcome
            return getYesPrice();
        }
    }
    
    Price Interpretation:
    ┌─────────────────────────────────────────────────────────┐
    │ YES Price = $0.65                                       │
    │ → Market implies 65% probability of YES outcome         │
    │                                                         │
    │ If you think YES probability > 65%, buy YES             │
    │ If you think YES probability < 65%, buy NO (sell YES)   │
    └─────────────────────────────────────────────────────────┘
    
  #### **Security Notes**
    - Consider impermanent loss for LPs
    - Handle resolution and payout
    - Prevent manipulation near resolution

## Anti-Patterns


---
  #### **Id**
centralized-oracle
  #### **Name**
Single entity resolves markets
  #### **Severity**
critical
  #### **Description**
    One address has sole authority to resolve markets.
    They can resolve incorrectly for profit.
    
  #### **Detection**
    - Single EOA as oracle
    - No dispute mechanism
    - No multi-sig or DAO
    
  #### **Consequence**
    Market operator can steal all losing bets by
    resolving markets incorrectly
    

---
  #### **Id**
no-dispute-period
  #### **Name**
Instant resolution without dispute
  #### **Severity**
high
  #### **Description**
    Markets resolve immediately without opportunity
    to challenge incorrect resolution
    
  #### **Detection**
    - resolve() callable anytime
    - No liveness/challenge period
    
  #### **Consequence**
    Incorrect resolutions become final, losing
    traders have no recourse
    

---
  #### **Id**
outcome-token-imbalance
  #### **Name**
Outcome tokens don't sum to collateral
  #### **Severity**
critical
  #### **Description**
    Creating outcome tokens that don't properly back
    1:1 with collateral creates insolvency
    
  #### **Detection**
    - Minting tokens without locking collateral
    - Unbalanced split positions
    
  #### **Consequence**
    Winning traders cannot redeem full value
    