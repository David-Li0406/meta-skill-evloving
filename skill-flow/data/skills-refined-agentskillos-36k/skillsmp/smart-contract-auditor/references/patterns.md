# Smart Contract Auditor

## Patterns


---
  #### **Name**
Reentrancy Guard Pattern
  #### **Description**
Protect against all reentrancy variants with proper mutex
  #### **When**
Any function with external calls or state changes
  #### **Example**
    // Good: OpenZeppelin's ReentrancyGuard
    import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
    
    contract Vault is ReentrancyGuard {
        mapping(address => uint256) public balances;
    
        // nonReentrant modifier prevents ALL reentrancy
        function withdraw(uint256 amount) external nonReentrant {
            require(balances[msg.sender] >= amount, "Insufficient");
            balances[msg.sender] -= amount;
            (bool success, ) = msg.sender.call{value: amount}("");
            require(success, "Transfer failed");
        }
    }
    
    // Even better: Transient storage reentrancy guard (EIP-1153)
    contract ModernVault {
        bytes32 constant LOCKED = keccak256("REENTRANCY_LOCK");
    
        modifier nonReentrant() {
            assembly {
                if tload(LOCKED) { revert(0, 0) }
                tstore(LOCKED, 1)
            }
            _;
            assembly {
                tstore(LOCKED, 0)
            }
        }
    }
    

---
  #### **Name**
Checks-Effects-Interactions (CEI)
  #### **Description**
Order operations to minimize attack surface
  #### **When**
Any function that modifies state and makes external calls
  #### **Example**
    function withdraw(uint256 amount) external {
        // CHECKS - validate all conditions first
        require(balances[msg.sender] >= amount, "Insufficient balance");
        require(amount > 0, "Zero amount");
    
        // EFFECTS - update all state before external calls
        balances[msg.sender] -= amount;
        totalWithdrawn += amount;
    
        emit Withdrawal(msg.sender, amount);
    
        // INTERACTIONS - external calls last
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
    

---
  #### **Name**
Pull Over Push
  #### **Description**
Let users withdraw rather than pushing funds to them
  #### **When**
Distributing funds to multiple parties
  #### **Example**
    // BAD: Push pattern - vulnerable to griefing and reentrancy
    function distribute(address[] calldata recipients, uint256[] calldata amounts) external {
        for (uint i = 0; i < recipients.length; i++) {
            payable(recipients[i]).transfer(amounts[i]); // Can fail, blocking everyone
        }
    }
    
    // GOOD: Pull pattern - each user claims their own funds
    contract PullPayment {
        mapping(address => uint256) public pendingWithdrawals;
    
        function recordPayment(address to, uint256 amount) internal {
            pendingWithdrawals[to] += amount;
        }
    
        function withdraw() external {
            uint256 amount = pendingWithdrawals[msg.sender];
            require(amount > 0, "Nothing to withdraw");
            pendingWithdrawals[msg.sender] = 0;
            (bool success, ) = msg.sender.call{value: amount}("");
            require(success, "Transfer failed");
        }
    }
    

---
  #### **Name**
Oracle Price Validation
  #### **Description**
Validate oracle data freshness and sanity
  #### **When**
Using any external price feed
  #### **Example**
    interface AggregatorV3Interface {
        function latestRoundData() external view returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );
    }
    
    function getPrice(address feed) public view returns (uint256) {
        AggregatorV3Interface oracle = AggregatorV3Interface(feed);
        (
            uint80 roundId,
            int256 price,
            ,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = oracle.latestRoundData();
    
        // Check for stale data
        require(updatedAt > block.timestamp - MAX_ORACLE_DELAY, "Stale price");
    
        // Check round completeness
        require(answeredInRound >= roundId, "Incomplete round");
    
        // Sanity check price
        require(price > 0, "Invalid price");
        require(price < MAX_REASONABLE_PRICE, "Price too high");
    
        return uint256(price);
    }
    

---
  #### **Name**
Access Control Hierarchy
  #### **Description**
Implement granular role-based access with separation of concerns
  #### **When**
Contract requires privileged operations
  #### **Example**
    import "@openzeppelin/contracts/access/AccessControl.sol";
    
    contract SecureVault is AccessControl {
        bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR");
        bytes32 public constant GUARDIAN_ROLE = keccak256("GUARDIAN");
    
        bool public paused;
        uint256 public withdrawalDelay = 1 days;
    
        // Operators can manage funds
        function setWithdrawalLimit(uint256 limit) external onlyRole(OPERATOR_ROLE) {
            withdrawalLimit = limit;
        }
    
        // Guardians can only pause (emergency)
        function pause() external onlyRole(GUARDIAN_ROLE) {
            paused = true;
            emit Paused(msg.sender);
        }
    
        // Only DEFAULT_ADMIN can unpause (requires multisig)
        function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
            paused = false;
        }
    
        // Critical operations require timelock
        mapping(bytes32 => uint256) public timelocks;
    
        function queueWithdrawal(bytes32 id, uint256 amount) external onlyRole(OPERATOR_ROLE) {
            timelocks[id] = block.timestamp + withdrawalDelay;
        }
    
        function executeWithdrawal(bytes32 id, uint256 amount) external onlyRole(OPERATOR_ROLE) {
            require(timelocks[id] != 0 && timelocks[id] <= block.timestamp, "Not ready");
            delete timelocks[id];
            // ... execute
        }
    }
    

---
  #### **Name**
Signature Replay Protection
  #### **Description**
Prevent signature reuse across transactions, chains, and contracts
  #### **When**
Implementing meta-transactions or permit functionality
  #### **Example**
    contract SecurePermit {
        mapping(address => uint256) public nonces;
        bytes32 public immutable DOMAIN_SEPARATOR;
    
        constructor() {
            DOMAIN_SEPARATOR = keccak256(abi.encode(
                keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
                keccak256("SecurePermit"),
                keccak256("1"),
                block.chainid,  // Chain-specific
                address(this)   // Contract-specific
            ));
        }
    
        function executeWithSignature(
            address signer,
            bytes32 dataHash,
            uint256 deadline,
            uint8 v, bytes32 r, bytes32 s
        ) external {
            // Check expiration
            require(block.timestamp <= deadline, "Signature expired");
    
            // Include nonce to prevent replay
            bytes32 structHash = keccak256(abi.encode(
                PERMIT_TYPEHASH,
                signer,
                dataHash,
                nonces[signer]++,  // Increment nonce
                deadline
            ));
    
            bytes32 digest = keccak256(abi.encodePacked(
                "\x19\x01",
                DOMAIN_SEPARATOR,
                structHash
            ));
    
            address recovered = ecrecover(digest, v, r, s);
            require(recovered == signer && recovered != address(0), "Invalid signature");
        }
    }
    

---
  #### **Name**
Invariant Testing Pattern
  #### **Description**
Define and test critical system invariants
  #### **When**
Any DeFi protocol or system with economic guarantees
  #### **Example**
    // In your test file (Foundry)
    contract VaultInvariantTest is Test {
        Vault vault;
        Handler handler;
    
        function setUp() public {
            vault = new Vault();
            handler = new Handler(vault);
    
            // Target the handler for fuzzing
            targetContract(address(handler));
        }
    
        // This MUST always be true
        function invariant_solvency() public {
            assertGe(
                address(vault).balance,
                vault.totalDeposits(),
                "Vault is insolvent"
            );
        }
    
        // Total shares must match deposited amounts
        function invariant_shareAccounting() public {
            uint256 totalShares;
            for (uint i = 0; i < handler.actorCount(); i++) {
                totalShares += vault.balanceOf(handler.actors(i));
            }
            assertEq(totalShares, vault.totalSupply(), "Share mismatch");
        }
    
        // No user can have more than they deposited
        function invariant_noFreeValue() public {
            for (uint i = 0; i < handler.actorCount(); i++) {
                address actor = handler.actors(i);
                assertLe(
                    vault.maxWithdraw(actor),
                    handler.totalDeposited(actor),
                    "Free value detected"
                );
            }
        }
    }
    
    contract Handler is Test {
        Vault vault;
        address[] public actors;
        mapping(address => uint256) public totalDeposited;
    
        constructor(Vault _vault) {
            vault = _vault;
            // Create test actors
            for (uint i = 0; i < 10; i++) {
                actors.push(makeAddr(string(abi.encodePacked("actor", i))));
            }
        }
    
        function deposit(uint256 actorSeed, uint256 amount) public {
            address actor = actors[actorSeed % actors.length];
            amount = bound(amount, 1, 1e24);
            deal(actor, amount);
            vm.prank(actor);
            vault.deposit{value: amount}();
            totalDeposited[actor] += amount;
        }
    
        function withdraw(uint256 actorSeed, uint256 amount) public {
            address actor = actors[actorSeed % actors.length];
            uint256 maxWithdraw = vault.maxWithdraw(actor);
            if (maxWithdraw == 0) return;
            amount = bound(amount, 1, maxWithdraw);
            vm.prank(actor);
            vault.withdraw(amount);
        }
    }
    

## Anti-Patterns


---
  #### **Name**
External Call Before State Update
  #### **Description**
Making external calls before updating contract state
  #### **Why**
Classic reentrancy vulnerability - attacker can reenter and exploit stale state
  #### **Instead**
    // VULNERABLE - state updated after external call
    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount);
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
        balances[msg.sender] -= amount;  // TOO LATE!
    }
    
    // SECURE - state updated before external call
    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;  // Update first
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
    }
    

---
  #### **Name**
Unchecked Return Values
  #### **Description**
Ignoring return values from external calls
  #### **Why**
Failed transfers can silently succeed, leading to accounting errors
  #### **Instead**
    // VULNERABLE - ignoring return value
    IERC20(token).transfer(recipient, amount);
    
    // SECURE - check return value
    require(IERC20(token).transfer(recipient, amount), "Transfer failed");
    
    // BEST - use SafeERC20 for weird tokens (USDT, etc.)
    import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
    using SafeERC20 for IERC20;
    IERC20(token).safeTransfer(recipient, amount);
    

---
  #### **Name**
tx.origin Authentication
  #### **Description**
Using tx.origin for access control
  #### **Why**
Phishing attacks can trick users into calling malicious contracts
  #### **Instead**
    // VULNERABLE - can be phished
    function withdraw() external {
        require(tx.origin == owner, "Not owner");  // BAD
        // ...
    }
    
    // SECURE - use msg.sender
    function withdraw() external {
        require(msg.sender == owner, "Not owner");  // GOOD
        // ...
    }
    

---
  #### **Name**
Unbounded Loops
  #### **Description**
Loops that iterate over unbounded arrays
  #### **Why**
Gas limit DoS - attacker can add enough elements to make function unusable
  #### **Instead**
    // VULNERABLE - unbounded loop
    function distributeRewards() external {
        for (uint i = 0; i < stakers.length; i++) {  // Can be 10000+ users
            // ... expensive operation
        }
    }
    
    // SECURE - paginated processing
    function distributeRewards(uint256 start, uint256 end) external {
        require(end <= stakers.length && end > start);
        for (uint i = start; i < end; i++) {
            // Process batch
        }
    }
    

---
  #### **Name**
Block Timestamp Manipulation
  #### **Description**
Relying on block.timestamp for critical logic
  #### **Why**
Miners can manipulate timestamp by ~15 seconds
  #### **Instead**
    // VULNERABLE - tight time window
    function claim() external {
        require(block.timestamp == deadline, "Wrong time");  // Miner can manipulate
    }
    
    // SECURE - reasonable time ranges
    function claim() external {
        require(block.timestamp >= startTime, "Too early");
        require(block.timestamp <= endTime, "Too late");
        // Use ranges that exceed manipulation window
    }
    

---
  #### **Name**
Single Oracle Dependency
  #### **Description**
Relying on a single price oracle without fallbacks
  #### **Why**
Oracle manipulation, downtime, or stale data can break the protocol
  #### **Instead**
    // VULNERABLE - single point of failure
    function getPrice() public view returns (uint256) {
        return chainlinkOracle.latestAnswer();
    }
    
    // SECURE - multiple oracles with fallback
    function getPrice() public view returns (uint256) {
        (uint256 chainlinkPrice, bool chainlinkValid) = getChainlinkPrice();
        if (chainlinkValid) return chainlinkPrice;
    
        (uint256 uniswapPrice, bool uniswapValid) = getUniswapTWAP();
        if (uniswapValid) return uniswapPrice;
    
        revert("No valid oracle");
    }
    

---
  #### **Name**
Missing Slippage Protection
  #### **Description**
Swaps without minimum output or deadline
  #### **Why**
Front-running and sandwich attacks will extract maximum value
  #### **Instead**
    // VULNERABLE - no protection
    function swap(uint256 amountIn) external {
        router.swapExactTokensForTokens(amountIn, 0, path, msg.sender, type(uint256).max);
    }
    
    // SECURE - slippage and deadline
    function swap(
        uint256 amountIn,
        uint256 minAmountOut,  // User specifies minimum
        uint256 deadline       // Transaction expires
    ) external {
        require(block.timestamp <= deadline, "Expired");
        uint256 amountOut = router.swapExactTokensForTokens(
            amountIn,
            minAmountOut,
            path,
            msg.sender,
            deadline
        );
        require(amountOut >= minAmountOut, "Slippage");
    }
    

---
  #### **Name**
Hardcoded Addresses
  #### **Description**
Hardcoding external contract addresses
  #### **Why**
No upgrade path, network-specific bugs, deployment errors
  #### **Instead**
    // VULNERABLE - hardcoded
    address constant UNISWAP_ROUTER = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    
    // SECURE - configurable with access control
    address public router;
    address public immutable INITIAL_ROUTER;
    
    constructor(address _router) {
        INITIAL_ROUTER = _router;
        router = _router;
    }
    
    function setRouter(address _router) external onlyOwner {
        require(_router != address(0), "Zero address");
        emit RouterUpdated(router, _router);
        router = _router;
    }
    

---
  #### **Name**
Insufficient Input Validation
  #### **Description**
Missing validation on function parameters
  #### **Why**
Attackers will find every edge case your tests missed
  #### **Instead**
    // VULNERABLE - no validation
    function setFee(uint256 newFee) external onlyOwner {
        fee = newFee;  // Could be 100% or more!
    }
    
    // SECURE - comprehensive validation
    function setFee(uint256 newFee) external onlyOwner {
        require(newFee <= MAX_FEE, "Fee too high");
        require(newFee >= MIN_FEE, "Fee too low");
        require(newFee != fee, "Same fee");
        emit FeeUpdated(fee, newFee);
        fee = newFee;
    }
    