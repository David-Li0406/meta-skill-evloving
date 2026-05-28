# Common Vulnerability Patterns

Real-world vulnerability patterns with detection strategies and fixes.

## Reentrancy Patterns

### Classic Reentrancy
```solidity
// VULNERABLE
function withdraw() external {
    uint256 bal = balances[msg.sender];
    (bool sent,) = msg.sender.call{value: bal}("");  // Attacker re-enters here
    require(sent);
    balances[msg.sender] = 0;
}

// Attacker contract
receive() external payable {
    if (address(victim).balance >= 1 ether) {
        victim.withdraw();  // Re-enter before balance zeroed
    }
}
```

**Detection**: Look for `call`, `transfer`, `send` before state updates.

**Fix**: CEI pattern + `nonReentrant` modifier.

### Read-Only Reentrancy
```solidity
// Protocol A - VULNERABLE
function getPrice() public view returns (uint256) {
    return totalValue / totalShares;  // Read during callback
}

// Protocol B uses A's price during A's callback
// Attacker manipulates A's state, triggers callback, B reads stale price
```

**Detection**: View functions called by external protocols during state transitions.

**Fix**: Reentrancy locks on view functions or snapshot pattern.

### Cross-Function Reentrancy
```solidity
// VULNERABLE - Both use same balance
function transfer(address to, uint256 amount) external {
    balances[msg.sender] -= amount;
    (bool sent,) = to.call{value: amount}("");  // Can re-enter withdraw
    require(sent);
}

function withdraw() external {
    uint256 bal = balances[msg.sender];  // Still has old balance
    balances[msg.sender] = 0;
    payable(msg.sender).transfer(bal);
}
```

---

## Oracle Manipulation Patterns

### Flash Loan Price Manipulation
```solidity
// VULNERABLE - Uses spot price
function getCollateralValue(address user) public view returns (uint256) {
    uint256 balance = collateral.balanceOf(user);
    uint256 price = dex.getSpotPrice(collateral);  // Manipulable
    return balance * price;
}

// Attack:
// 1. Flash loan large amount
// 2. Manipulate DEX price
// 3. Borrow against inflated collateral
// 4. Repay flash loan, keep borrowed funds
```

**Fix**: TWAP oracles, Chainlink, or multiple oracle sources.

### Stale Oracle Data
```solidity
// VULNERABLE
(, int256 price,,,) = priceFeed.latestRoundData();
return uint256(price);  // Could be hours old

// SAFE
(uint80 roundId, int256 price,, uint256 updatedAt, uint80 answeredInRound) =
    priceFeed.latestRoundData();
require(price > 0, "Invalid price");
require(answeredInRound >= roundId, "Stale round");
require(block.timestamp - updatedAt < HEARTBEAT, "Stale price");
```

---

## Access Control Patterns

### Missing Access Control
```solidity
// VULNERABLE - Anyone can call
function setFeeRecipient(address _recipient) external {
    feeRecipient = _recipient;
}

// VULNERABLE - Wrong modifier logic
function emergencyWithdraw() external {
    require(msg.sender == owner || paused);  // Should be &&
    // ...
}
```

### Unprotected Initialize
```solidity
// VULNERABLE - Can be front-run
function initialize(address _owner) external {
    require(owner == address(0));
    owner = _owner;
}

// SAFE
function initialize(address _owner) external initializer {
    __Ownable_init(_owner);
}
```

---

## MEV Patterns

### Sandwich Attack
```solidity
// User submits swap: 1 ETH → USDC
// Attacker sees in mempool:
// 1. Front-run: Buy USDC (price goes up)
// 2. User's tx executes at worse price
// 3. Back-run: Sell USDC at higher price

// VULNERABLE
function swap(uint256 amountIn) external returns (uint256) {
    return _executeSwap(amountIn);  // No slippage protection
}

// SAFE
function swap(uint256 amountIn, uint256 minOut, uint256 deadline) external {
    require(block.timestamp <= deadline);
    uint256 out = _executeSwap(amountIn);
    require(out >= minOut, "Slippage");
    return out;
}
```

### Predictable Randomness
```solidity
// VULNERABLE - Miners can manipulate
function getWinner() external view returns (address) {
    uint256 random = uint256(blockhash(block.number - 1));
    return participants[random % participants.length];
}

// SAFE - Use Chainlink VRF or commit-reveal
```

---

## Signature Patterns

### Signature Replay
```solidity
// VULNERABLE - No nonce, replayable
function executeWithSig(address to, uint256 amount, bytes calldata sig) external {
    bytes32 hash = keccak256(abi.encodePacked(to, amount));
    address signer = ECDSA.recover(hash, sig);
    require(signer == owner);
    token.transfer(to, amount);  // Can replay same sig
}

// SAFE
mapping(bytes32 => bool) public usedHashes;

function executeWithSig(
    address to,
    uint256 amount,
    uint256 nonce,
    uint256 deadline,
    bytes calldata sig
) external {
    require(block.timestamp <= deadline);
    bytes32 hash = keccak256(abi.encodePacked(to, amount, nonce, deadline, block.chainid));
    require(!usedHashes[hash], "Already used");
    usedHashes[hash] = true;

    address signer = ECDSA.recover(hash, sig);
    require(signer == owner);
    token.transfer(to, amount);
}
```

### Missing Domain Separation
```solidity
// VULNERABLE - Same sig works for different functions
bytes32 hash = keccak256(abi.encodePacked(user, amount));

// SAFE - Include function selector
bytes32 hash = keccak256(abi.encodePacked(
    "\x19\x01",
    DOMAIN_SEPARATOR,
    keccak256(abi.encode(
        TRANSFER_TYPEHASH,  // Unique per function
        to,
        amount,
        nonce
    ))
));
```

---

## Token Patterns

### Fee-on-Transfer
```solidity
// VULNERABLE
function deposit(uint256 amount) external {
    token.transferFrom(msg.sender, address(this), amount);
    shares[msg.sender] += amount;  // Wrong if fee taken
}

// SAFE
function deposit(uint256 amount) external {
    uint256 before = token.balanceOf(address(this));
    token.safeTransferFrom(msg.sender, address(this), amount);
    uint256 received = token.balanceOf(address(this)) - before;
    shares[msg.sender] += received;
}
```

### Approval Race Condition
```solidity
// VULNERABLE - Allows double-spend
token.approve(spender, newAmount);

// SAFE - Reset to 0 first, or use safe methods
token.approve(spender, 0);
token.approve(spender, newAmount);

// Or use OpenZeppelin
token.safeIncreaseAllowance(spender, additionalAmount);
```

---

## Upgradability Patterns

### Storage Collision
```solidity
// V1
contract TokenV1 {
    address public owner;      // slot 0
    uint256 public totalSupply;  // slot 1
}

// V2 - VULNERABLE (adds slot before existing)
contract TokenV2 {
    address public admin;      // slot 0 - COLLISION with owner!
    address public owner;      // slot 1 - COLLISION with totalSupply!
    uint256 public totalSupply;
}

// SAFE - Add at end, use gaps
contract TokenV2 {
    address public owner;
    uint256 public totalSupply;
    address public admin;      // New storage at end
    uint256[48] private __gap; // Reserve space for future
}
```

### Unprotected UUPS
```solidity
// VULNERABLE
function _authorizeUpgrade(address) internal override {}  // Anyone can upgrade!

// SAFE
function _authorizeUpgrade(address) internal override onlyOwner {}
```

---

## DoS Patterns

### Unbounded Operations
```solidity
// VULNERABLE - Can exceed block gas limit
function distributeToAll() external {
    for (uint i = 0; i < users.length; i++) {  // Unbounded
        token.transfer(users[i], amounts[i]);
    }
}

// SAFE - Pagination or pull pattern
function distribute(uint256 start, uint256 end) external {
    require(end <= users.length && end - start <= MAX_BATCH);
    for (uint i = start; i < end; i++) {
        token.transfer(users[i], amounts[i]);
    }
}
```

### Revert Griefing
```solidity
// VULNERABLE - One bad actor blocks all
function batchTransfer(address[] calldata recipients) external {
    for (uint i = 0; i < recipients.length; i++) {
        require(token.transfer(recipients[i], amounts[i]));  // One revert blocks all
    }
}

// SAFE - Continue on failure
function batchTransfer(address[] calldata recipients) external {
    for (uint i = 0; i < recipients.length; i++) {
        try token.transfer(recipients[i], amounts[i]) {} catch {}
    }
}
```
