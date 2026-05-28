# Layer 2 Scaling

## Patterns


---
  #### **Name**
Calldata Packing
  #### **Description**
Minimize calldata to reduce L2 transaction costs
  #### **When**
Any L2 deployment where gas optimization matters
  #### **Example**
    // Bad: Full addresses and amounts
    function transfer(address to, uint256 amount) external;
    // Calldata: 4 + 32 + 32 = 68 bytes
    
    // Good: Packed encoding for known users
    mapping(uint16 => address) public userRegistry;
    
    function transferPacked(uint16 toId, uint128 amount) external;
    // Calldata: 4 + 2 + 16 = 22 bytes (68% reduction!)
    
    // Best: Batch multiple operations
    function batchTransfer(bytes calldata packed) external {
        // Decode: [toId1, amount1, toId2, amount2, ...]
        uint256 offset = 0;
        while (offset < packed.length) {
            uint16 toId = uint16(bytes2(packed[offset:offset+2]));
            uint128 amount = uint128(bytes16(packed[offset+2:offset+18]));
            _transfer(userRegistry[toId], amount);
            offset += 18;
        }
    }
    

---
  #### **Name**
Cross-L2 Messaging
  #### **Description**
Communicate between L2s through canonical bridges or protocols
  #### **When**
Multi-chain application requiring state sync
  #### **Example**
    // Using Optimism CrossDomainMessenger
    import {ICrossDomainMessenger} from "@eth-optimism/contracts/libraries/bridge/ICrossDomainMessenger.sol";
    
    contract L1Bridge {
        ICrossDomainMessenger public messenger;
        address public l2Target;
    
        function sendToL2(bytes memory data) external {
            messenger.sendMessage(
                l2Target,
                data,
                1000000 // gas limit for L2 execution
            );
        }
    }
    
    contract L2Receiver {
        address public l1Source;
    
        modifier onlyFromL1() {
            require(
                msg.sender == address(messenger) &&
                messenger.xDomainMessageSender() == l1Source,
                "Not from L1"
            );
            _;
        }
    
        function receiveFromL1(bytes memory data) external onlyFromL1 {
            // Process L1 message
        }
    }
    

---
  #### **Name**
Sequencer Uptime Monitoring
  #### **Description**
Check sequencer status before critical operations
  #### **When**
Operations that need guaranteed inclusion
  #### **Example**
    // Chainlink Sequencer Uptime Feed
    import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV2V3Interface.sol";
    
    contract SequencerAware {
        AggregatorV2V3Interface public sequencerFeed;
        uint256 public constant GRACE_PERIOD = 3600; // 1 hour
    
        function checkSequencer() internal view {
            (, int256 answer, uint256 startedAt, , ) = sequencerFeed.latestRoundData();
    
            // Answer: 0 = up, 1 = down
            bool isDown = answer == 1;
            bool inGracePeriod = block.timestamp - startedAt < GRACE_PERIOD;
    
            require(!isDown, "Sequencer is down");
            require(!inGracePeriod, "Grace period active");
        }
    
        function criticalOperation() external {
            checkSequencer();
            // Proceed with operation
        }
    }
    

---
  #### **Name**
EIP-4844 Blob Optimization
  #### **Description**
Leverage blob data for cheaper L1 data availability
  #### **When**
Post-Dencun upgrade L2 deployments
  #### **Example**
    // L2s now post to blobs instead of calldata
    // This changes cost calculation
    
    // Old cost (calldata):
    // 16 gas per non-zero byte
    // ~1000 gwei per byte at 30 gwei base fee
    
    // New cost (blobs):
    // ~1 gwei per byte (variable blob gas market)
    
    // Impact on your dApp:
    // 1. L2 fees are 5-10x cheaper
    // 2. Batch sizes can be larger
    // 3. Consider moving more data on-chain
    
    // Check if L2 uses blobs
    function isPostDencun() public view returns (bool) {
        // L2s updated their fee calculation
        // Your app should handle both models
        return block.number > DENCUN_FORK_BLOCK;
    }
    

---
  #### **Name**
Forced Transaction Inclusion
  #### **Description**
Submit transactions directly to L1 if sequencer censors
  #### **When**
Decentralization-critical applications
  #### **Example**
    // Arbitrum: DelayedInbox for forced inclusion
    interface IInbox {
        function sendL2Message(bytes calldata messageData)
            external returns (uint256);
    }
    
    contract ForcedInclusionBridge {
        IInbox public inbox;
        uint256 public constant FORCE_DELAY = 24 hours;
    
        function forceInclude(
            address target,
            bytes calldata data
        ) external payable {
            // After 24 hours, anyone can force-include
            // this transaction even if sequencer censors
            bytes memory message = abi.encodeWithSignature(
                "executeTransaction(address,bytes)",
                target,
                data
            );
            inbox.sendL2Message(message);
        }
    }
    

---
  #### **Name**
L2-Aware Gas Estimation
  #### **Description**
Calculate gas including L1 data posting costs
  #### **When**
Any transaction cost estimation on L2
  #### **Example**
    // Optimism gas calculation
    import {GasPriceOracle} from "@eth-optimism/contracts/L2/predeploys/GasPriceOracle.sol";
    
    contract L2GasEstimator {
        GasPriceOracle constant oracle = GasPriceOracle(
            0x420000000000000000000000000000000000000F
        );
    
        function estimateTotalCost(
            bytes memory txData,
            uint256 l2GasLimit
        ) public view returns (uint256) {
            // L1 data fee (posting calldata to L1)
            uint256 l1Fee = oracle.getL1Fee(txData);
    
            // L2 execution fee
            uint256 l2Fee = l2GasLimit * tx.gasprice;
    
            return l1Fee + l2Fee;
        }
    }
    

## Anti-Patterns


---
  #### **Name**
Ignoring L1 Data Costs
  #### **Description**
Only considering L2 execution gas in estimates
  #### **Why**
L1 data posting often dominates total transaction cost
  #### **Instead**
    // Bad: Only L2 gas
    uint256 cost = gasLimit * tx.gasprice;
    
    // Good: Include L1 data fee
    uint256 l1Fee = GasPriceOracle(L1_ORACLE).getL1Fee(txData);
    uint256 l2Fee = gasLimit * tx.gasprice;
    uint256 totalCost = l1Fee + l2Fee;
    

---
  #### **Name**
Hardcoded L1 Gas Prices
  #### **Description**
Assuming static L1 gas prices in contracts
  #### **Why**
L1 gas is volatile, EIP-4844 changed economics entirely
  #### **Instead**
    // Bad
    uint256 constant L1_GAS_PRICE = 30 gwei;
    
    // Good: Query oracle
    function getL1GasPrice() public view returns (uint256) {
        return GasPriceOracle(oracle).l1BaseFee();
    }
    

---
  #### **Name**
Assuming Instant Finality
  #### **Description**
Treating L2 transactions as final immediately
  #### **Why**
Sequencer soft confirmations can be reorged
  #### **Instead**
    // Understand finality levels:
    // 1. Sequencer confirmation: ~2 seconds (can reorg)
    // 2. L1 inclusion: ~12 minutes (safer)
    // 3. L1 finality: ~15 minutes (final)
    // 4. Challenge period: 7 days (optimistic rollups)
    
    // For high-value operations, wait for appropriate finality
    mapping(bytes32 => uint256) public confirmationTime;
    
    function confirmWithDelay(bytes32 txHash) external {
        require(
            block.timestamp >= confirmationTime[txHash] + DELAY,
            "Not yet final"
        );
        // Proceed
    }
    

---
  #### **Name**
Single Sequencer Dependency
  #### **Description**
No handling for sequencer downtime
  #### **Why**
Sequencers can go down, censoring all transactions
  #### **Instead**
    // Implement fallback paths
    // 1. Use sequencer uptime feed
    // 2. Implement forced inclusion path
    // 3. Add circuit breakers for critical functions
    
    function safeOperation() external {
        if (isSequencerDown()) {
            // Switch to fallback mode or pause
            _pauseUntilSequencerRecovery();
        }
        // Normal operation
    }
    

---
  #### **Name**
Ignoring L2-Specific Opcodes
  #### **Description**
Assuming all EVM opcodes work identically on L2
  #### **Why**
Some opcodes have different behavior or cost on L2s
  #### **Instead**
    // L2-specific considerations:
    // - TIMESTAMP: May batch blocks differently
    // - BASEFEE: L2 has separate fee market
    // - DIFFICULTY/PREVRANDAO: May not be available
    // - BLOCKHASH: Limited history on some L2s
    
    // Test on target L2, don't assume L1 behavior
    

---
  #### **Name**
Unprotected Bridge Receivers
  #### **Description**
Bridge message receivers without authentication
  #### **Why**
Anyone can call receiver if not properly protected
  #### **Instead**
    // Bad
    function receiveMessage(bytes memory data) external {
        _process(data);
    }
    
    // Good
    function receiveMessage(bytes memory data) external {
        require(
            msg.sender == address(messenger),
            "Not messenger"
        );
        require(
            messenger.xDomainMessageSender() == trustedL1Contract,
            "Wrong sender"
        );
        _process(data);
    }
    