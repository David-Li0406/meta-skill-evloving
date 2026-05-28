# Solidity Patterns & Anti-Patterns

Reference guide for common patterns in smart contract development. Use these as building blocks and avoid the anti-patterns.

---

## Access Control Patterns

### Pattern: Role-Based Access Control

```solidity
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

contract Treasury is AccessControl {
    bytes32 public constant WITHDRAWER_ROLE = keccak256("WITHDRAWER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    constructor(address admin) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
    }

    function withdraw(address to, uint256 amount) external onlyRole(WITHDRAWER_ROLE) {
        // ...
    }
}
```

**When to use**: Multiple roles with different permissions, granular access control.

### Pattern: Two-Step Ownership Transfer

```solidity
import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";

contract MyContract is Ownable2Step {
    constructor(address initialOwner) Ownable(initialOwner) {}
}
```

**When to use**: Always prefer over single-step `Ownable` to prevent accidental transfers to wrong address.

### Anti-Pattern: tx.origin Authentication

```solidity
// ❌ NEVER DO THIS
function withdraw() external {
    require(tx.origin == owner, "Not owner");
}

// ✅ CORRECT
function withdraw() external onlyOwner {
    // ...
}
```

**Why bad**: Phishing attacks can trick users into calling malicious contracts that then call your contract.

---

## Reentrancy Protection

### Pattern: Check-Effects-Interactions (CEI)

```solidity
function withdraw(uint256 amount) external {
    // 1. CHECKS
    require(balances[msg.sender] >= amount, "Insufficient balance");

    // 2. EFFECTS (state changes)
    balances[msg.sender] -= amount;

    // 3. INTERACTIONS (external calls)
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

### Pattern: ReentrancyGuard

```solidity
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract Vault is ReentrancyGuard {
    function withdrawAll() external nonReentrant {
        uint256 amount = balances[msg.sender];
        balances[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

**When to use**: Any function that modifies state AND makes external calls.

### Anti-Pattern: State Change After External Call

```solidity
// ❌ VULNERABLE
function withdraw(uint256 amount) external {
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] -= amount; // State change AFTER call
}
```

---

## Payment Patterns

### Pattern: Pull Over Push

```solidity
// ✅ PULL PATTERN (preferred)
mapping(address => uint256) public pendingWithdrawals;

function claimReward() external {
    uint256 amount = pendingWithdrawals[msg.sender];
    require(amount > 0, "Nothing to claim");

    pendingWithdrawals[msg.sender] = 0;

    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}

// ❌ PUSH PATTERN (risky)
function distributeRewards(address[] calldata recipients) external {
    for (uint256 i = 0; i < recipients.length; i++) {
        // One failed transfer blocks everyone
        payable(recipients[i]).transfer(reward);
    }
}
```

**Why pull is better**: Failed transfers don't block other users; no unbounded gas costs.

### Pattern: Safe ETH Transfer

```solidity
function safeTransferETH(address to, uint256 amount) internal {
    (bool success, ) = to.call{value: amount}("");
    if (!success) {
        // Option 1: Revert
        revert TransferFailed();

        // Option 2: Record for later claim (pull pattern)
        // pendingWithdrawals[to] += amount;
    }
}
```

---

## Token Patterns

### Pattern: SafeERC20

```solidity
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract Vault {
    using SafeERC20 for IERC20;

    function deposit(IERC20 token, uint256 amount) external {
        // Handles non-standard tokens (USDT, BNB, etc.)
        token.safeTransferFrom(msg.sender, address(this), amount);
    }
}
```

**When to use**: Always when interacting with arbitrary ERC20 tokens.

### Pattern: Fee-on-Transfer Token Handling

```solidity
function deposit(IERC20 token, uint256 amount) external {
    uint256 balanceBefore = token.balanceOf(address(this));
    token.safeTransferFrom(msg.sender, address(this), amount);
    uint256 actualAmount = token.balanceOf(address(this)) - balanceBefore;

    // Use actualAmount, not amount
    deposits[msg.sender] += actualAmount;
}
```

**When to use**: If your protocol accepts arbitrary tokens that might have transfer fees.

### Pattern: ERC721/1155 Safe Receiver

```solidity
import {IERC721Receiver} from "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";

contract NFTVault is IERC721Receiver {
    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes calldata data
    ) external override returns (bytes4) {
        // Custom logic here
        return IERC721Receiver.onERC721Received.selector;
    }
}
```

---

## Upgradeability Patterns

### Pattern: UUPS Proxy

```solidity
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract MyContractV1 is UUPSUpgradeable, OwnableUpgradeable {
    uint256 public value;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address initialOwner) public initializer {
        __Ownable_init(initialOwner);
        __UUPSUpgradeable_init();
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}
```

### Pattern: Storage Gaps

```solidity
contract MyContractV1 is UUPSUpgradeable {
    uint256 public value;
    address public admin;

    // Reserve storage slots for future versions
    uint256[48] private __gap;
}

contract MyContractV2 is UUPSUpgradeable {
    uint256 public value;
    address public admin;
    uint256 public newValue; // Uses one gap slot

    uint256[47] private __gap; // Reduced by 1
}
```

### Pattern: ERC-7201 Namespaced Storage

```solidity
contract MyContract {
    /// @custom:storage-location erc7201:mycontract.main
    struct MainStorage {
        uint256 value;
        mapping(address => uint256) balances;
    }

    // keccak256(abi.encode(uint256(keccak256("mycontract.main")) - 1)) & ~bytes32(uint256(0xff))
    bytes32 private constant MAIN_STORAGE_LOCATION =
        0x...;

    function _getMainStorage() private pure returns (MainStorage storage $) {
        assembly {
            $.slot := MAIN_STORAGE_LOCATION
        }
    }
}
```

### Anti-Pattern: Constructor in Upgradeable Contract

```solidity
// ❌ WRONG - constructor runs on implementation, not proxy
contract BadUpgradeable {
    address public owner;

    constructor() {
        owner = msg.sender; // This sets owner on implementation!
    }
}

// ✅ CORRECT
contract GoodUpgradeable is Initializable {
    address public owner;

    function initialize(address _owner) public initializer {
        owner = _owner;
    }
}
```

---

## Signature Patterns

### Pattern: EIP-712 Typed Signatures

```solidity
import {EIP712} from "@openzeppelin/contracts/utils/cryptography/EIP712.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract Permit is EIP712 {
    bytes32 private constant PERMIT_TYPEHASH =
        keccak256("Permit(address owner,address spender,uint256 value,uint256 nonce,uint256 deadline)");

    mapping(address => uint256) public nonces;

    constructor() EIP712("MyToken", "1") {}

    function permit(
        address owner,
        address spender,
        uint256 value,
        uint256 deadline,
        uint8 v, bytes32 r, bytes32 s
    ) external {
        require(block.timestamp <= deadline, "Expired");

        bytes32 structHash = keccak256(abi.encode(
            PERMIT_TYPEHASH,
            owner,
            spender,
            value,
            nonces[owner]++,
            deadline
        ));

        bytes32 hash = _hashTypedDataV4(structHash);
        address signer = ECDSA.recover(hash, v, r, s);

        require(signer == owner, "Invalid signature");

        _approve(owner, spender, value);
    }
}
```

### Pattern: SignatureChecker (Supports Smart Contract Wallets)

```solidity
import {SignatureChecker} from "@openzeppelin/contracts/utils/cryptography/SignatureChecker.sol";

function verify(address signer, bytes32 hash, bytes memory signature) internal view returns (bool) {
    // Works with both EOAs and ERC-1271 smart contract wallets
    return SignatureChecker.isValidSignatureNow(signer, hash, signature);
}
```

---

## Gas Optimization Patterns

### Pattern: Storage Packing

```solidity
// ❌ UNOPTIMIZED (3 storage slots)
struct BadStruct {
    uint256 id;      // slot 0
    address owner;   // slot 1
    uint256 amount;  // slot 2
}

// ✅ OPTIMIZED (2 storage slots)
struct GoodStruct {
    uint256 id;      // slot 0
    uint96 amount;   // slot 1 (12 bytes)
    address owner;   // slot 1 (20 bytes) - packed!
}
```

### Pattern: Calldata vs Memory

```solidity
// ❌ EXPENSIVE (copies array to memory)
function process(uint256[] memory data) external {
    // ...
}

// ✅ CHEAPER (reads directly from calldata)
function process(uint256[] calldata data) external {
    // ...
}
```

### Pattern: Unchecked Arithmetic

```solidity
function sum(uint256[] calldata values) external pure returns (uint256 total) {
    uint256 len = values.length;
    for (uint256 i = 0; i < len;) {
        total += values[i];
        unchecked { ++i; } // Safe: i can't overflow
    }
}
```

### Pattern: Custom Errors

```solidity
// ❌ EXPENSIVE
require(balance >= amount, "Insufficient balance for withdrawal");

// ✅ CHEAPER
error InsufficientBalance(uint256 available, uint256 required);

if (balance < amount) {
    revert InsufficientBalance(balance, amount);
}
```

---

## Emergency Patterns

### Pattern: Pausable

```solidity
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";

contract Vault is Pausable {
    function deposit() external whenNotPaused {
        // ...
    }

    function emergencyPause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }
}
```

### Pattern: Emergency Withdrawal

```solidity
function emergencyWithdraw(IERC20 token) external onlyOwner {
    uint256 balance = token.balanceOf(address(this));
    token.safeTransfer(owner(), balance);

    emit EmergencyWithdrawal(address(token), balance);
}
```

---

## Oracle Patterns

### Pattern: Chainlink Price Feed with Staleness Check

```solidity
import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

function getPrice(AggregatorV3Interface feed) internal view returns (uint256) {
    (
        uint80 roundId,
        int256 answer,
        ,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = feed.latestRoundData();

    require(answer > 0, "Invalid price");
    require(updatedAt > block.timestamp - 1 hours, "Stale price");
    require(answeredInRound >= roundId, "Stale round");

    return uint256(answer);
}
```

### Pattern: TWAP for Manipulation Resistance

```solidity
// Use time-weighted average price over a window
// to resist single-block manipulation
uint256 public constant TWAP_PERIOD = 30 minutes;

function getTWAP() internal view returns (uint256) {
    // Implementation depends on DEX (Uniswap V3, etc.)
}
```

---

## Testing Patterns

### Pattern: Fork Testing

```solidity
// foundry.toml
// [rpc_endpoints]
// mainnet = "${MAINNET_RPC_URL}"

contract ForkTest is Test {
    function setUp() public {
        vm.createSelectFork("mainnet", 18_000_000);
    }

    function test_interactWithMainnet() public {
        IERC20 usdc = IERC20(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
        // Test against real mainnet state
    }
}
```

### Pattern: Invariant Testing

```solidity
contract InvariantTest is Test {
    Vault vault;

    function setUp() public {
        vault = new Vault();
        targetContract(address(vault));
    }

    function invariant_totalSupplyMatchesBalances() public {
        assertEq(
            vault.totalSupply(),
            sumAllBalances()
        );
    }
}
```

### Pattern: Fuzz Testing

```solidity
function testFuzz_deposit(uint256 amount) public {
    amount = bound(amount, 1, type(uint128).max);

    token.mint(user, amount);

    vm.prank(user);
    vault.deposit(amount);

    assertEq(vault.balanceOf(user), amount);
}
```
