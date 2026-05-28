# Smart Contract Vulnerability Patterns

Detailed vulnerability patterns with code examples, detection strategies, and fixes.

---

## 1. Reentrancy

### 1.1 Classic Reentrancy

**Vulnerable:**
```solidity
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);

    (bool success, ) = msg.sender.call{value: amount}("");  // External call
    require(success);

    balances[msg.sender] -= amount;  // State update AFTER call
}
```

**Attack:**
```solidity
contract Attacker {
    Victim victim;

    function attack() external payable {
        victim.deposit{value: 1 ether}();
        victim.withdraw(1 ether);
    }

    receive() external payable {
        if (address(victim).balance >= 1 ether) {
            victim.withdraw(1 ether);  // Re-enter before balance updated
        }
    }
}
```

**Fix:**
```solidity
function withdraw(uint256 amount) external nonReentrant {
    require(balances[msg.sender] >= amount);

    balances[msg.sender] -= amount;  // Effects BEFORE interactions

    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
}
```

**Detection:**
- `slither --detect reentrancy-eth,reentrancy-no-eth`
- Look for: external call → state change pattern

### 1.2 Cross-Function Reentrancy

**Vulnerable:**
```solidity
function withdraw() external {
    uint256 amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] = 0;
}

function transfer(address to, uint256 amount) external {
    require(balances[msg.sender] >= amount);
    balances[msg.sender] -= amount;
    balances[to] += amount;
}
```

**Attack:** During `withdraw` callback, call `transfer` to move balance that's about to be zeroed.

**Fix:** ReentrancyGuard on ALL state-changing functions, or CEI in all paths.

### 1.3 Read-Only Reentrancy

**Vulnerable:**
```solidity
// In protocol A
function getPrice() external view returns (uint256) {
    return totalAssets / totalShares;  // Reads mid-operation
}

// In protocol B (victim)
function liquidate(address user) external {
    uint256 collateralValue = protocolA.getPrice() * userCollateral[user];
    // ...
}
```

**Attack:** Reenter during Protocol A's deposit/withdraw to manipulate price view.

**Detection:** Check if view functions are called by external protocols during state transitions.

---

## 2. Access Control

### 2.1 Missing Access Control

**Vulnerable:**
```solidity
function setPrice(uint256 newPrice) external {
    price = newPrice;  // Anyone can call!
}
```

**Fix:**
```solidity
function setPrice(uint256 newPrice) external onlyOwner {
    price = newPrice;
}
```

### 2.2 Unprotected Initializer

**Vulnerable:**
```solidity
function initialize(address _owner) external {
    owner = _owner;  // Can be front-run on deployment
}
```

**Fix:**
```solidity
function initialize(address _owner) external initializer {
    __Ownable_init(_owner);
}
```

### 2.3 tx.origin Authentication

**Vulnerable:**
```solidity
function withdraw() external {
    require(tx.origin == owner);  // Phishing vulnerable
    // ...
}
```

**Attack:** Trick owner into calling malicious contract that calls `withdraw()`.

**Fix:** Use `msg.sender`.

### 2.4 Privilege Escalation via Delegatecall

**Vulnerable:**
```solidity
function execute(address target, bytes calldata data) external onlyOwner {
    target.delegatecall(data);  // Can overwrite owner slot
}
```

**Fix:** Whitelist targets or use call instead of delegatecall.

---

## 3. Signature Vulnerabilities

### 3.1 Signature Replay

**Vulnerable:**
```solidity
function executeWithSig(address to, uint256 amount, bytes memory sig) external {
    bytes32 hash = keccak256(abi.encodePacked(to, amount));
    address signer = ECDSA.recover(hash, sig);
    require(signer == owner);
    // Execute... (same sig works forever)
}
```

**Fix:**
```solidity
mapping(bytes32 => bool) public usedHashes;

function executeWithSig(address to, uint256 amount, uint256 nonce, uint256 deadline, bytes memory sig) external {
    require(block.timestamp <= deadline, "Expired");
    bytes32 hash = keccak256(abi.encodePacked(to, amount, nonce, deadline, block.chainid, address(this)));
    require(!usedHashes[hash], "Replayed");
    usedHashes[hash] = true;
    // ...
}
```

### 3.2 Signature Malleability

**Vulnerable:**
```solidity
bytes32 hash = keccak256(...);
address signer = ecrecover(hash, v, r, s);  // Raw ecrecover
```

**Issue:** ECDSA signatures have two valid (r, s) pairs. Can bypass uniqueness checks.

**Fix:** Use OpenZeppelin's ECDSA library which rejects malleable signatures.

### 3.3 ecrecover Returns Zero

**Vulnerable:**
```solidity
address signer = ecrecover(hash, v, r, s);
require(signer == authorizedSigner);  // If ecrecover fails, signer = address(0)
```

**Attack:** If `authorizedSigner` is ever `address(0)`, invalid signatures pass.

**Fix:**
```solidity
address signer = ECDSA.recover(hash, sig);  // Reverts on invalid sig
require(signer == authorizedSigner && signer != address(0));
```

---

## 4. Accounting Vulnerabilities

### 4.1 First Depositor Inflation Attack

**Vulnerable:**
```solidity
function deposit(uint256 assets) external returns (uint256 shares) {
    shares = totalSupply == 0 ? assets : (assets * totalSupply) / totalAssets;
    // ...
}
```

**Attack:**
1. Attacker deposits 1 wei → gets 1 share
2. Attacker donates 1000 ETH directly to vault
3. Victim deposits 1000 ETH → gets 0 shares (rounds down)
4. Attacker withdraws → gets ~2000 ETH

**Fix:**
```solidity
// Virtual offset (ERC4626 style)
function _convertToShares(uint256 assets) internal view returns (uint256) {
    return assets.mulDiv(totalSupply() + 1, totalAssets() + 1, Math.Rounding.Floor);
}
```

Or: Require minimum initial deposit, burn initial shares.

### 4.2 Fee-on-Transfer Token Issues

**Vulnerable:**
```solidity
function deposit(IERC20 token, uint256 amount) external {
    token.transferFrom(msg.sender, address(this), amount);
    balances[msg.sender] += amount;  // Assumes full amount received
}
```

**Issue:** Fee-on-transfer tokens deliver less than `amount`.

**Fix:**
```solidity
function deposit(IERC20 token, uint256 amount) external {
    uint256 before = token.balanceOf(address(this));
    token.safeTransferFrom(msg.sender, address(this), amount);
    uint256 received = token.balanceOf(address(this)) - before;
    balances[msg.sender] += received;
}
```

### 4.3 Rounding Direction Exploitation

**Vulnerable:**
```solidity
// Always rounds down, attacker can extract value
uint256 shares = (amount * totalShares) / totalAssets;
```

**Issue:** Many small operations accumulate rounding in attacker's favor.

**Fix:** Round against the user (down on deposit, up on withdraw for vault).

---

## 5. Oracle Manipulation

### 5.1 Spot Price Manipulation

**Vulnerable:**
```solidity
function getPrice() public view returns (uint256) {
    return uniswapPool.slot0().sqrtPriceX96;  // Manipulable in one tx
}
```

**Attack:** Flash loan → swap to move price → exploit protocol → swap back.

**Fix:** Use TWAP (time-weighted average price):
```solidity
function getTWAP() public view returns (uint256) {
    uint32[] memory secondsAgos = new uint32[](2);
    secondsAgos[0] = 1800;  // 30 min ago
    secondsAgos[1] = 0;     // now

    (int56[] memory tickCumulatives, ) = pool.observe(secondsAgos);
    // Calculate TWAP from tick cumulatives
}
```

### 5.2 Stale Oracle Data

**Vulnerable:**
```solidity
(, int256 price, , , ) = priceFeed.latestRoundData();
return uint256(price);  // No freshness check
```

**Fix:**
```solidity
(uint80 roundId, int256 price, , uint256 updatedAt, uint80 answeredInRound) =
    priceFeed.latestRoundData();

require(price > 0, "Invalid price");
require(updatedAt > block.timestamp - 1 hours, "Stale price");
require(answeredInRound >= roundId, "Stale round");
```

### 5.3 Oracle Decimal Mismatch

**Issue:** Chainlink ETH/USD = 8 decimals, token might be 18.

**Fix:** Always normalize:
```solidity
uint256 priceNormalized = uint256(price) * 10**(18 - priceFeed.decimals());
```

---

## 6. MEV Vulnerabilities

### 6.1 Sandwich Attack

**Vulnerable:**
```solidity
function swap(uint256 amountIn, uint256 minOut) external {
    // Executes at current pool price
}
```

**Attack:**
1. Attacker sees victim's swap in mempool
2. Front-run: buy token (price goes up)
3. Victim's swap executes at worse price
4. Back-run: attacker sells at higher price

**Mitigation:**
- Tight slippage bounds
- Private mempools (Flashbots)
- Commit-reveal schemes

### 6.2 Frontrunning Initialization

**Vulnerable:**
```solidity
function initialize(address _owner) external {
    require(owner == address(0));
    owner = _owner;
}
```

**Attack:** Watch for deployment, front-run initialize call.

**Fix:** Initialize in constructor or same tx as deployment.

---

## 7. Denial of Service

### 7.1 Unbounded Loop

**Vulnerable:**
```solidity
function distributeRewards() external {
    for (uint256 i = 0; i < users.length; i++) {
        payable(users[i]).transfer(rewards[users[i]]);
    }
}
```

**Attack:** Add many users → function exceeds gas limit.

**Fix:** Pull pattern or paginated distribution.

### 7.2 Revert on Transfer

**Vulnerable:**
```solidity
function withdraw() external {
    payable(msg.sender).transfer(balance);  // Fails if recipient reverts
}
```

**Fix:**
```solidity
(bool success, ) = msg.sender.call{value: balance}("");
if (!success) {
    pendingWithdrawals[msg.sender] += balance;  // Store for later claim
}
```

### 7.3 Block Gas Limit DoS

**Issue:** Single tx requires more gas than block limit.

**Detection:** Look for unbounded operations that grow with user count.

---

## 8. Upgradeability Issues

### 8.1 Storage Collision

**Vulnerable:**
```solidity
// V1
contract V1 {
    address public owner;     // slot 0
    uint256 public value;     // slot 1
}

// V2 (WRONG)
contract V2 {
    uint256 public newValue;  // slot 0 - collides with owner!
    address public owner;     // slot 1
    uint256 public value;     // slot 2
}
```

**Fix:** Only append new variables; use storage gaps.

### 8.2 Missing Storage Gap

**Vulnerable:**
```solidity
contract Base {
    uint256 public baseValue;
    // No gap - can't add variables in upgrades
}
```

**Fix:**
```solidity
contract Base {
    uint256 public baseValue;
    uint256[49] private __gap;
}
```

### 8.3 Uninitialized Implementation

**Vulnerable:**
```solidity
// Implementation can be initialized by attacker
contract Implementation {
    function initialize() external {
        owner = msg.sender;
    }
}
```

**Attack:** Call `initialize` on implementation directly → become owner → selfdestruct.

**Fix:**
```solidity
constructor() {
    _disableInitializers();
}
```

---

## 9. Flash Loan Attacks

### 9.1 Governance Takeover

**Attack Pattern:**
1. Flash loan governance tokens
2. Create/vote on malicious proposal
3. Execute proposal (drain treasury)
4. Return loan

**Mitigation:** Snapshot voting power, timelock on proposals.

### 9.2 Price Oracle Manipulation via Flash Loan

**Attack Pattern:**
1. Flash loan large amount
2. Swap to manipulate spot price
3. Interact with victim protocol using manipulated price
4. Profit
5. Swap back, repay loan

**Mitigation:** TWAP oracles, Chainlink, multiple sources.

---

## 10. Logic Errors

### 10.1 Off-by-One

**Vulnerable:**
```solidity
for (uint256 i = 0; i <= users.length; i++) {  // Should be <
```

### 10.2 Incorrect Comparison

**Vulnerable:**
```solidity
require(block.timestamp > deadline);  // Should be >=
```

### 10.3 Missing Return Value Check

**Vulnerable:**
```solidity
token.transfer(to, amount);  // Doesn't check return
```

**Fix:**
```solidity
require(token.transfer(to, amount), "Transfer failed");
// Or use SafeERC20
```

---

## Detection Commands

```bash
# Comprehensive scan
slither . --print human-summary

# Specific vulnerability classes
slither . --detect reentrancy-eth,reentrancy-no-eth,reentrancy-benign
slither . --detect unprotected-upgrade,arbitrary-send-eth
slither . --detect controlled-delegatecall,suicidal

# Function visibility
slither . --print function-summary

# Variable ordering (storage layout)
slither . --print variable-order
```
