# Audit Checklist

Complete security checklist for smart contract auditing. Apply relevant sections based on contract type.

## Access Control

- [ ] Missing access modifiers on sensitive functions
- [ ] Incorrect modifier logic (e.g., `||` vs `&&`)
- [ ] Role misconfiguration (wrong addresses, missing setup)
- [ ] Privilege escalation paths
- [ ] Missing `onlyOwner`/`onlyRole` on admin functions
- [ ] Centralization risks (single admin key)
- [ ] Two-step ownership transfer not used
- [ ] Default admin role not renounced

```solidity
// BAD: Missing access control
function setPrice(uint256 _price) external {
    price = _price;
}

// GOOD: Protected
function setPrice(uint256 _price) external onlyOwner {
    price = _price;
}
```

## Reentrancy

- [ ] External calls before state updates (CEI violation)
- [ ] Callbacks in ERC777, ERC721, ERC1155 hooks
- [ ] Cross-function reentrancy
- [ ] Cross-contract reentrancy
- [ ] Read-only reentrancy (view functions reading stale state)
- [ ] Missing `nonReentrant` modifier on fund-handling functions
- [ ] Unsafe `transfer`/`call` patterns

```solidity
// BAD: State update after external call
function withdraw() external {
    uint256 amount = balances[msg.sender];
    (bool success,) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] = 0;  // TOO LATE
}

// GOOD: CEI pattern
function withdraw() external nonReentrant {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;  // State first
    (bool success,) = msg.sender.call{value: amount}("");
    require(success);
}
```

## Arithmetic & Precision

- [ ] Overflow/underflow in unchecked blocks
- [ ] Rounding errors in division (especially fee calculations)
- [ ] Decimal mismatch between tokens (6 vs 18 decimals)
- [ ] Precision loss in intermediate calculations
- [ ] Division before multiplication
- [ ] Zero amount edge cases
- [ ] Type casting truncation (uint256 → uint128)

```solidity
// BAD: Precision loss
uint256 fee = amount / 1000 * feeRate;

// GOOD: Multiply first
uint256 fee = amount * feeRate / 1000;
```

## Oracle & Price Manipulation

- [ ] Spot price usage (manipulable in single tx)
- [ ] Missing TWAP or insufficient TWAP window
- [ ] Stale price data (no freshness check)
- [ ] Single oracle dependency
- [ ] Missing price bounds validation
- [ ] Sandwich attack vectors
- [ ] Flash loan price manipulation
- [ ] Chainlink heartbeat not checked

```solidity
// BAD: No staleness check
(, int256 price,,,) = priceFeed.latestRoundData();

// GOOD: With staleness check
(uint80 roundId, int256 price,, uint256 updatedAt,) = priceFeed.latestRoundData();
require(price > 0, "Invalid price");
require(updatedAt > block.timestamp - MAX_STALENESS, "Stale price");
require(answeredInRound >= roundId, "Stale round");
```

## MEV & Economic Attacks

- [ ] Frontrunning opportunities (predictable profitable txs)
- [ ] Sandwich attack vectors (swaps, liquidations)
- [ ] Backrunning opportunities (arbitrage after state change)
- [ ] Griefing attacks (DoS by intentional revert)
- [ ] Liquidity manipulation
- [ ] Flash loan attack vectors
- [ ] Auction manipulation (last-block bidding)
- [ ] Missing slippage protection
- [ ] Missing deadline parameters

```solidity
// BAD: No slippage protection
function swap(uint256 amountIn) external {
    uint256 amountOut = getAmountOut(amountIn);
    token.transfer(msg.sender, amountOut);
}

// GOOD: With slippage and deadline
function swap(uint256 amountIn, uint256 minAmountOut, uint256 deadline) external {
    require(block.timestamp <= deadline, "Expired");
    uint256 amountOut = getAmountOut(amountIn);
    require(amountOut >= minAmountOut, "Slippage");
    token.transfer(msg.sender, amountOut);
}
```

## Upgradability

- [ ] Missing `initializer` modifier
- [ ] `constructor` used instead of `initialize`
- [ ] `initialize` callable multiple times
- [ ] Storage layout collisions on upgrade
- [ ] Missing storage gaps in base contracts
- [ ] `delegatecall` to untrusted contracts
- [ ] UUPS `_authorizeUpgrade` not protected
- [ ] Transparent proxy selector clashing
- [ ] Missing `_disableInitializers` in implementation constructor

```solidity
// BAD: Re-initializable
function initialize(address _owner) external {
    owner = _owner;
}

// GOOD: Protected
function initialize(address _owner) external initializer {
    __Ownable_init(_owner);
}

// GOOD: Implementation constructor
constructor() {
    _disableInitializers();
}
```

## Signature Schemes

- [ ] EIP-712 domain separator incorrect
- [ ] Missing chain ID in domain
- [ ] Signature replay across chains
- [ ] Signature replay on same chain (missing nonce)
- [ ] Nonce not incremented on use
- [ ] Missing deadline in signed messages
- [ ] `ecrecover` returns `address(0)` not checked
- [ ] Signature malleability (use OpenZeppelin ECDSA)
- [ ] Missing domain separation between functions

```solidity
// BAD: No replay protection
function executeWithSig(bytes calldata data, bytes calldata sig) external {
    address signer = recover(keccak256(data), sig);
    require(signer == authorized);
    // execute...
}

// GOOD: With nonce and deadline
function executeWithSig(bytes calldata data, uint256 nonce, uint256 deadline, bytes calldata sig) external {
    require(block.timestamp <= deadline, "Expired");
    require(nonces[msg.sender] == nonce, "Invalid nonce");
    nonces[msg.sender]++;
    bytes32 hash = keccak256(abi.encodePacked(data, nonce, deadline, block.chainid));
    address signer = ECDSA.recover(hash, sig);
    require(signer == authorized);
}
```

## Token Handling

- [ ] Fee-on-transfer tokens not supported
- [ ] Rebasing tokens break accounting
- [ ] ERC20 `transfer`/`approve` return value not checked
- [ ] Missing `safeTransfer`/`safeApprove` usage
- [ ] Double approval race condition (use `safeIncreaseAllowance`)
- [ ] ETH and WETH handling inconsistency
- [ ] Token with multiple addresses (proxied tokens)
- [ ] Tokens with blacklists (USDC, USDT)
- [ ] Missing zero address validation

```solidity
// BAD: Doesn't handle fee-on-transfer
function deposit(uint256 amount) external {
    token.transferFrom(msg.sender, address(this), amount);
    balances[msg.sender] += amount;  // Wrong if fee taken
}

// GOOD: Measure actual received
function deposit(uint256 amount) external {
    uint256 before = token.balanceOf(address(this));
    token.safeTransferFrom(msg.sender, address(this), amount);
    uint256 received = token.balanceOf(address(this)) - before;
    balances[msg.sender] += received;
}
```

## DoS & Gas

- [ ] Unbounded loops over user-controlled arrays
- [ ] Block gas limit issues in batch operations
- [ ] Unexpected revert propagation
- [ ] External call failures blocking execution
- [ ] Push-over-pull pattern (should be pull)
- [ ] Missing array length limits
- [ ] Expensive operations in loops

```solidity
// BAD: Unbounded loop
function distributeRewards(address[] calldata users) external {
    for (uint i = 0; i < users.length; i++) {
        token.transfer(users[i], rewards[users[i]]);
    }
}

// GOOD: Pull pattern
function claimReward() external {
    uint256 reward = rewards[msg.sender];
    rewards[msg.sender] = 0;
    token.safeTransfer(msg.sender, reward);
}
```

## Chain & Environment Assumptions

- [ ] `block.timestamp` manipulation (miners have ~15s leeway)
- [ ] `block.number` used for time (varies by chain)
- [ ] Hardcoded chain-specific values
- [ ] `tx.origin` used for auth
- [ ] Contract size assumptions (post-merge changes)
- [ ] `SELFDESTRUCT` deprecation impact
- [ ] L2-specific behaviors not handled

## Events & Monitoring

- [ ] Missing events on state changes
- [ ] Incorrect event parameters
- [ ] Missing indexed parameters for filtering
- [ ] Events not emitted on failure paths
- [ ] Admin actions not logged

## Invariants & State

- [ ] Value conservation (in == out)
- [ ] State transition validity
- [ ] Pausable behavior gaps
- [ ] Emergency withdrawal missing
- [ ] Stuck funds scenarios
- [ ] Contract balance assumptions
