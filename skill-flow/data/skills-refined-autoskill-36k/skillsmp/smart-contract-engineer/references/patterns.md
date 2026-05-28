# Smart Contract Engineer

## Patterns


---
  #### **Name**
Secure Token Implementation
  #### **Description**
ERC20 with common security patterns
  #### **When**
Creating any token contract
  #### **Example**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.20;
    
    import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
    import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";
    import "@openzeppelin/contracts/access/Ownable2Step.sol";
    import "@openzeppelin/contracts/security/Pausable.sol";
    
    contract SecureToken is ERC20, ERC20Permit, Ownable2Step, Pausable {
        uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18;
    
        mapping(address => bool) public blacklisted;
    
        event Blacklisted(address indexed account, bool status);
    
        error ExceedsMaxSupply();
        error AccountBlacklisted();
        error ZeroAddress();
    
        constructor()
            ERC20("Secure Token", "SECURE")
            ERC20Permit("Secure Token")
            Ownable(msg.sender)
        {
            _mint(msg.sender, 100_000_000 * 10**18);
        }
    
        function mint(address to, uint256 amount) external onlyOwner {
            if (to == address(0)) revert ZeroAddress();
            if (totalSupply() + amount > MAX_SUPPLY) revert ExceedsMaxSupply();
            _mint(to, amount);
        }
    
        function setBlacklist(address account, bool status) external onlyOwner {
            blacklisted[account] = status;
            emit Blacklisted(account, status);
        }
    
        function pause() external onlyOwner {
            _pause();
        }
    
        function unpause() external onlyOwner {
            _unpause();
        }
    
        function _update(
            address from,
            address to,
            uint256 amount
        ) internal override whenNotPaused {
            if (blacklisted[from] || blacklisted[to]) revert AccountBlacklisted();
            super._update(from, to, amount);
        }
    }
    

---
  #### **Name**
Reentrancy Protection
  #### **Description**
Preventing reentrancy attacks
  #### **When**
Any external calls or ETH transfers
  #### **Example**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.20;
    
    import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
    
    contract SecureVault is ReentrancyGuard {
        mapping(address => uint256) public balances;
    
        error InsufficientBalance();
        error TransferFailed();
    
        // Checks-Effects-Interactions pattern
        function withdraw(uint256 amount) external nonReentrant {
            // CHECKS
            if (balances[msg.sender] < amount) revert InsufficientBalance();
    
            // EFFECTS (state changes BEFORE external call)
            balances[msg.sender] -= amount;
    
            // INTERACTIONS (external call LAST)
            (bool success, ) = msg.sender.call{value: amount}("");
            if (!success) revert TransferFailed();
        }
    
        // BAD - vulnerable to reentrancy
        function withdrawBad(uint256 amount) external {
            require(balances[msg.sender] >= amount);
    
            // External call BEFORE state update = reentrancy!
            (bool success, ) = msg.sender.call{value: amount}("");
            require(success);
    
            balances[msg.sender] -= amount;  // Too late!
        }
    
        function deposit() external payable {
            balances[msg.sender] += msg.value;
        }
    }
    

---
  #### **Name**
Gas Optimization
  #### **Description**
Reducing transaction costs
  #### **When**
Optimizing contract operations
  #### **Example**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.20;
    
    contract GasOptimized {
        // Pack structs - slot efficiency
        // BAD: Uses 3 slots (96 bytes)
        struct BadUser {
            uint256 balance;    // slot 0
            bool active;        // slot 1 (wastes 31 bytes)
            uint256 timestamp;  // slot 2
        }
    
        // GOOD: Uses 2 slots (64 bytes)
        struct GoodUser {
            uint256 balance;    // slot 0
            uint128 timestamp;  // slot 1
            bool active;        // slot 1 (packed)
        }
    
        // Use calldata for read-only arrays
        function processBad(uint256[] memory data) external pure returns (uint256) {
            return data.length;
        }
    
        function processGood(uint256[] calldata data) external pure returns (uint256) {
            return data.length;  // Saves ~600 gas per call
        }
    
        // Cache array length
        function sumBad(uint256[] calldata arr) external pure returns (uint256 total) {
            for (uint256 i = 0; i < arr.length; i++) {  // reads length each iteration
                total += arr[i];
            }
        }
    
        function sumGood(uint256[] calldata arr) external pure returns (uint256 total) {
            uint256 len = arr.length;  // cache length
            for (uint256 i = 0; i < len; ) {
                total += arr[i];
                unchecked { ++i; }  // safe: can't overflow
            }
        }
    
        // Use custom errors instead of strings
        error Unauthorized();
        error InvalidAmount(uint256 provided, uint256 required);
    
        function checkBad(uint256 amount) external pure {
            require(amount > 0, "Amount must be greater than zero");  // Expensive string
        }
    
        function checkGood(uint256 amount) external pure {
            if (amount == 0) revert InvalidAmount(amount, 1);  // Cheaper
        }
    }
    

---
  #### **Name**
Upgradeable Contract Pattern
  #### **Description**
Safe upgrade patterns when needed
  #### **When**
Contracts requiring future upgrades
  #### **Example**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.20;
    
    import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
    import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
    import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
    
    contract VaultV1 is Initializable, UUPSUpgradeable, OwnableUpgradeable {
        // Storage slot 0 - never change order in upgrades!
        uint256 public totalDeposits;
    
        // Storage slot 1
        mapping(address => uint256) public balances;
    
        /// @custom:oz-upgrades-unsafe-allow constructor
        constructor() {
            _disableInitializers();
        }
    
        function initialize(address owner_) public initializer {
            __Ownable_init(owner_);
            __UUPSUpgradeable_init();
        }
    
        function deposit() external payable {
            balances[msg.sender] += msg.value;
            totalDeposits += msg.value;
        }
    
        function getVersion() external pure virtual returns (string memory) {
            return "1.0.0";
        }
    
        function _authorizeUpgrade(address newImplementation)
            internal
            override
            onlyOwner
        {}
    }
    
    // Upgrade - must maintain storage layout!
    contract VaultV2 is VaultV1 {
        // Add NEW storage at END only
        uint256 public withdrawalFee;  // New slot, safe
    
        function setWithdrawalFee(uint256 fee) external onlyOwner {
            withdrawalFee = fee;
        }
    
        function getVersion() external pure override returns (string memory) {
            return "2.0.0";
        }
    }
    

## Anti-Patterns


---
  #### **Name**
tx.origin Authentication
  #### **Description**
Using tx.origin instead of msg.sender
  #### **Why**
Allows phishing attacks through malicious contracts
  #### **Instead**
Always use msg.sender for authentication

---
  #### **Name**
Unbounded Loops
  #### **Description**
Loops without gas limits
  #### **Why**
Can exceed block gas limit, DoS the contract
  #### **Instead**
Use pagination, batch processing, or mappings

---
  #### **Name**
Hardcoded Addresses
  #### **Description**
Embedding addresses in contract code
  #### **Why**
Can't update if external contract upgrades
  #### **Instead**
Use constructor parameters or admin-settable addresses

---
  #### **Name**
Missing Access Control
  #### **Description**
Sensitive functions without authorization
  #### **Why**
Anyone can call, drain funds, change state
  #### **Instead**
Use OpenZeppelin AccessControl or Ownable

---
  #### **Name**
Floating Pragma
  #### **Description**
Using ^0.8.0 instead of fixed version
  #### **Why**
Different compiler versions have different behaviors
  #### **Instead**
Lock to specific version (0.8.20)