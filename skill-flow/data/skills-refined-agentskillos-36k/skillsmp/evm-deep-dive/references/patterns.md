# EVM Deep Dive

## Patterns


---
  #### **Name**
Storage Packing
  #### **Description**
Pack multiple variables into single 32-byte slots
  #### **When**
Multiple variables under 32 bytes used together
  #### **Example**
    // Bad: 3 storage slots (96 bytes of storage)
    contract Bad {
        uint256 a;  // slot 0
        uint128 b;  // slot 1
        uint128 c;  // slot 2
    }
    
    // Good: 2 storage slots
    contract Good {
        uint256 a;  // slot 0
        uint128 b;  // slot 1 (lower 128 bits)
        uint128 c;  // slot 1 (upper 128 bits)
    }
    
    // Best: Consider access patterns
    contract Best {
        // Packed together if accessed together
        uint128 balance;    // slot 0
        uint64 timestamp;   // slot 0
        uint32 nonce;       // slot 0
        bool active;        // slot 0 (still fits!)
        uint256 data;       // slot 1
    }
    

---
  #### **Name**
Calldata Optimization
  #### **Description**
Use calldata and tight packing for function parameters
  #### **When**
Functions receive array or struct parameters
  #### **Example**
    // Bad: Memory copy
    function process(uint256[] memory data) external {
        for (uint i = 0; i < data.length; i++) {
            // Uses MLOAD
        }
    }
    
    // Good: Direct calldata access
    function process(uint256[] calldata data) external {
        for (uint i = 0; i < data.length; i++) {
            // Uses CALLDATALOAD - cheaper
        }
    }
    
    // Best: Custom packed encoding
    function processPacked(bytes calldata data) external {
        // Decode manually for maximum efficiency
        uint256 len = data.length / 32;
        for (uint i = 0; i < len; ) {
            uint256 value;
            assembly {
                value := calldataload(add(data.offset, mul(i, 32)))
            }
            unchecked { ++i; }
        }
    }
    

---
  #### **Name**
Unchecked Arithmetic
  #### **Description**
Skip overflow checks when mathematically safe
  #### **When**
Values are bounded or overflow is impossible
  #### **Example**
    // Safe unchecked patterns
    function sum(uint256[] calldata arr) external pure returns (uint256 total) {
        uint256 len = arr.length;
        for (uint256 i = 0; i < len; ) {
            total += arr[i];  // Could overflow - keep checked
            unchecked { ++i; }  // i < len, can't overflow
        }
    }
    
    // Unchecked for bounded values
    function calculateFee(uint256 amount) external pure returns (uint256) {
        unchecked {
            // amount * 30 / 10000 can't overflow for reasonable amounts
            // Max safe: type(uint256).max / 30 ≈ 3.8e75
            return (amount * 30) / 10000;
        }
    }
    

---
  #### **Name**
Assembly Storage Access
  #### **Description**
Direct storage manipulation for complex patterns
  #### **When**
Need precise control over storage slots
  #### **Example**
    // Efficient mapping access
    function getBalanceSlot(address user) internal pure returns (bytes32) {
        // balances mapping at slot 0
        return keccak256(abi.encode(user, uint256(0)));
    }
    
    function getBalance(address user) external view returns (uint256 bal) {
        bytes32 slot = getBalanceSlot(user);
        assembly {
            bal := sload(slot)
        }
    }
    
    // Transient storage (EIP-1153)
    function setTransient(bytes32 key, uint256 value) internal {
        assembly {
            tstore(key, value)
        }
    }
    

---
  #### **Name**
Minimal Proxy (EIP-1167)
  #### **Description**
Deploy cheap clones that delegatecall to implementation
  #### **When**
Deploying many instances of same contract
  #### **Example**
    // Clone factory
    function clone(address implementation) internal returns (address instance) {
        assembly {
            // Load free memory pointer
            let ptr := mload(0x40)
    
            // Clone bytecode
            mstore(ptr, 0x3d602d80600a3d3981f3363d3d373d3d3d363d73000000000000000000000000)
            mstore(add(ptr, 0x14), shl(0x60, implementation))
            mstore(add(ptr, 0x28), 0x5af43d82803e903d91602b57fd5bf30000000000000000000000000000000000)
    
            // Deploy
            instance := create(0, ptr, 0x37)
        }
        require(instance != address(0), "Clone failed");
    }
    

---
  #### **Name**
Bitmap Flags
  #### **Description**
Pack boolean flags into single uint256
  #### **When**
Multiple boolean states per entity
  #### **Example**
    contract BitmapFlags {
        // Single slot holds 256 boolean flags
        mapping(address => uint256) private userFlags;
    
        uint256 constant FLAG_ACTIVE = 1 << 0;
        uint256 constant FLAG_VERIFIED = 1 << 1;
        uint256 constant FLAG_PREMIUM = 1 << 2;
    
        function setFlag(address user, uint256 flag) external {
            userFlags[user] |= flag;
        }
    
        function clearFlag(address user, uint256 flag) external {
            userFlags[user] &= ~flag;
        }
    
        function hasFlag(address user, uint256 flag) external view returns (bool) {
            return userFlags[user] & flag != 0;
        }
    }
    

## Anti-Patterns


---
  #### **Name**
Unnecessary SLOAD
  #### **Description**
Reading same storage variable multiple times
  #### **Why**
Each SLOAD costs 2100 gas (cold) or 100 gas (warm)
  #### **Instead**
    // Bad
    function bad() external {
        require(balance > 0);
        uint256 fee = balance / 100;
        balance = balance - fee;
    }
    
    // Good
    function good() external {
        uint256 _balance = balance; // Single SLOAD
        require(_balance > 0);
        uint256 fee = _balance / 100;
        balance = _balance - fee;
    }
    

---
  #### **Name**
String Error Messages
  #### **Description**
Using require with string messages
  #### **Why**
Strings are expensive to store and return
  #### **Instead**
    // Bad: ~20k gas overhead
    require(balance >= amount, "Insufficient balance");
    
    // Good: Custom error
    error InsufficientBalance(uint256 available, uint256 required);
    if (balance < amount) revert InsufficientBalance(balance, amount);
    

---
  #### **Name**
Redundant Zero Checks
  #### **Description**
Checking for zero when transfer will revert anyway
  #### **Why**
Unnecessary gas for checks that provide no value
  #### **Instead**
    // Bad: Redundant check
    function withdraw(uint256 amount) external {
        require(amount > 0, "Zero amount");  // Remove this
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;  // Will revert on underflow
    }
    

---
  #### **Name**
Loop Length Recalculation
  #### **Description**
Reading array length in each loop iteration
  #### **Why**
Storage/memory read on every iteration
  #### **Instead**
    // Bad
    for (uint i = 0; i < array.length; i++) { }
    
    // Good
    uint256 len = array.length;
    for (uint i = 0; i < len; ) {
        unchecked { ++i; }
    }
    

---
  #### **Name**
Default Variable Values
  #### **Description**
Explicitly setting variables to default values
  #### **Why**
Variables are already zero-initialized by EVM
  #### **Instead**
    // Bad
    uint256 counter = 0;
    bool active = false;
    address owner = address(0);
    
    // Good - omit initialization
    uint256 counter;
    bool active;
    address owner;
    

---
  #### **Name**
Memory Over Calldata
  #### **Description**
Using memory for read-only external parameters
  #### **Why**
Memory requires copying, calldata is direct access
  #### **Instead**
    // Bad
    function process(bytes memory data) external { }
    
    // Good
    function process(bytes calldata data) external { }
    