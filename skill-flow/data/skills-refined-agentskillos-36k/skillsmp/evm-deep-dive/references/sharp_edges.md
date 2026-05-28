# Evm Deep Dive - Sharp Edges

## Optimizer Reorders Storage Operations

### **Id**
optimizer-reordering
### **Severity**
CRITICAL
### **Description**
Solidity optimizer may reorder SLOAD/SSTORE in unexpected ways
### **Symptoms**
  - State reads return stale values
  - Reentrancy guards bypassed
  - Cross-function state inconsistencies
### **Detection Pattern**
optimizer.*enabled|runs.*[0-9]+
### **Solution**
  // Use memory barriers with assembly
  function criticalOperation() external {
      uint256 _state = state; // Cache
      assembly {
          // Memory barrier - prevents reordering
          mstore(0x00, _state)
      }
      // Continue with operation
  }
  
  // Or disable optimizer for specific functions
  // via assembly blocks that optimizer won't touch
  
### **References**
  - https://github.com/ethereum/solidity/issues/12820

## Storage Collision in Proxy Patterns

### **Id**
storage-collision-proxy
### **Severity**
CRITICAL
### **Description**
Implementation and proxy storage slots overlap
### **Symptoms**
  - Admin variables overwritten by implementation
  - Proxy becomes unusable after upgrade
  - Funds locked in contract
### **Detection Pattern**
delegatecall|proxy|implementation
### **Solution**
  // Use EIP-1967 storage slots
  bytes32 constant IMPLEMENTATION_SLOT =
      bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1);
  
  bytes32 constant ADMIN_SLOT =
      bytes32(uint256(keccak256("eip1967.proxy.admin")) - 1);
  
  function _getImplementation() internal view returns (address impl) {
      assembly {
          impl := sload(IMPLEMENTATION_SLOT)
      }
  }
  
### **References**
  - https://eips.ethereum.org/EIPS/eip-1967

## SELFDESTRUCT Behavior Changed

### **Id**
selfdestruct-deprecation
### **Severity**
CRITICAL
### **Description**
Post-Cancun, SELFDESTRUCT only sends ETH, doesn't delete code
### **Symptoms**
  - Contract still exists after selfdestruct
  - Storage persists
  - CREATE2 resurrection blocked
### **Detection Pattern**
selfdestruct|SELFDESTRUCT
### **Solution**
  // Don't rely on selfdestruct for:
  // - Contract removal
  // - Storage clearing
  // - CREATE2 redeployment
  
  // Instead, use disable patterns
  contract Disableable {
      bool public disabled;
  
      modifier notDisabled() {
          require(!disabled, "Contract disabled");
          _;
      }
  
      function disable() external onlyOwner {
          disabled = true;
          // Send remaining ETH
          payable(owner).transfer(address(this).balance);
      }
  }
  
### **References**
  - https://eips.ethereum.org/EIPS/eip-6780

## Transient Storage Only Lasts One Transaction

### **Id**
transient-storage-scope
### **Severity**
HIGH
### **Description**
TSTORE/TLOAD values cleared after transaction
### **Symptoms**
  - Values disappear between calls
  - Cross-transaction state lost
  - Confusion with regular storage
### **Detection Pattern**
tstore|tload|transient
### **Solution**
  // Transient storage use cases:
  // - Reentrancy guards (cheaper than storage)
  // - Callback context
  // - Single-tx caching
  
  contract ReentrancyGuard {
      bytes32 constant LOCKED_SLOT = keccak256("REENTRANCY_GUARD");
  
      modifier nonReentrant() {
          assembly {
              if tload(LOCKED_SLOT) { revert(0, 0) }
              tstore(LOCKED_SLOT, 1)
          }
          _;
          assembly {
              tstore(LOCKED_SLOT, 0)
          }
      }
  }
  
### **References**
  - https://eips.ethereum.org/EIPS/eip-1153

## Memory Expansion Has Quadratic Cost

### **Id**
memory-expansion-cost
### **Severity**
HIGH
### **Description**
Memory cost grows quadratically with size
### **Symptoms**
  - Gas usage spikes unexpectedly
  - Large array operations fail
  - Out of gas on memory allocation
### **Detection Pattern**
new.*\[|memory.*length
### **Solution**
  // Memory cost = 3 * words + words^2 / 512
  // At 724 words (23KB), quadratic term equals linear term
  
  // Avoid large memory allocations
  // Use calldata for input, return minimal data
  
  // Process in chunks
  function processLarge(bytes calldata data) external {
      uint256 chunkSize = 1000;
      for (uint256 i = 0; i < data.length; i += chunkSize) {
          uint256 end = min(i + chunkSize, data.length);
          _processChunk(data[i:end]);
      }
  }
  
### **References**
  - https://www.evm.codes/about#memoryexpansion

## Cold vs Warm Storage Access Costs

### **Id**
cold-warm-access
### **Severity**
HIGH
### **Description**
First access to storage slot costs 2100 gas, subsequent 100 gas
### **Symptoms**
  - First transaction in block costs more
  - Gas estimates don't match execution
  - Inconsistent gas usage
### **Detection Pattern**
sload|SLOAD|storage
### **Solution**
  // Cache storage in memory for multiple reads
  function process() external {
      // Cold read: 2100 gas
      uint256 _value = storageValue;
  
      // Use _value multiple times (free after first read)
      uint256 a = _value * 2;
      uint256 b = _value / 3;
      uint256 c = _value + 1;
  
      // Single warm write: 2900 gas (vs 20000 for cold)
      storageValue = c;
  }
  
  // Access pattern matters for gas estimation
  
### **References**
  - https://eips.ethereum.org/EIPS/eip-2929

## Returndata Can Be Used to Grief

### **Id**
returndata-bomb
### **Severity**
HIGH
### **Description**
External calls can return massive data causing OOG
### **Symptoms**
  - External calls fail unexpectedly
  - Gas griefing attacks
  - Memory expansion from returndata copy
### **Detection Pattern**
call\(|staticcall\(|delegatecall\(
### **Solution**
  // Limit returndata copy
  assembly {
      let success := call(gas(), target, value, 0, 0, 0, 0)
      // Don't copy all returndata
      if success {
          // Only copy what you need
          returndatacopy(0, 0, min(returndatasize(), 64))
      }
  }
  
  // Or use low-level call with explicit size
  (bool success, bytes memory result) = target.call{gas: 100000}(data);
  // result is bounded by gas provided
  
### **References**
  - https://github.com/ethereum/solidity/issues/12306

## ABI Decode Can Revert Unexpectedly

### **Id**
abi-decode-revert
### **Severity**
MEDIUM
### **Description**
Malformed returndata causes decode to revert
### **Symptoms**
  - External calls revert on success
  - Can't handle non-standard tokens
  - Integration failures
### **Detection Pattern**
abi.decode|returns.*\(
### **Solution**
  // Handle non-standard ERC20 (like USDT)
  function safeTransfer(IERC20 token, address to, uint256 amount) internal {
      (bool success, bytes memory data) = address(token).call(
          abi.encodeWithSelector(token.transfer.selector, to, amount)
      );
      require(
          success && (data.length == 0 || abi.decode(data, (bool))),
          "Transfer failed"
      );
  }
  
  // Check returndata length before decode
  if (returndata.length >= 32) {
      result = abi.decode(returndata, (uint256));
  }
  
### **References**
  - https://github.com/d-xo/weird-erc20

## Immutables Increase Deployment Cost

### **Id**
immutable-deployment-cost
### **Severity**
MEDIUM
### **Description**
Immutable values are embedded in bytecode
### **Symptoms**
  - Higher deployment gas than expected
  - Bytecode size increase
  - Factory patterns become expensive
### **Detection Pattern**
immutable
### **Solution**
  // Trade-off: deployment cost vs runtime cost
  // Immutable: +200 gas deploy, -3 gas per read
  
  // For frequently deployed contracts (factories):
  // Consider storage over immutable if:
  // - Deployed many times
  // - Read infrequently
  
  // For singleton contracts:
  // Immutable is almost always better
  
  // Break-even: ~67 reads to justify immutable
  // deploy_cost_increase / read_cost_savings = 200 / 3 ≈ 67
  
### **References**
  - https://docs.soliditylang.org/en/latest/contracts.html#immutable

## Custom Errors Aren't Always Smaller

### **Id**
custom-error-size
### **Severity**
MEDIUM
### **Description**
Custom errors with data can exceed string error size
### **Symptoms**
  - Gas savings not realized
  - Larger revert data than strings
  - ABI encoding overhead
### **Detection Pattern**
error.*\(.*\)|revert.*\(
### **Solution**
  // String error: 4 (selector) + 32 (offset) + 32 (length) + string
  // Custom error: 4 (selector) + 32 per parameter
  
  // Error with no params: Always better
  error Unauthorized();
  
  // Error with 1 param: Usually better
  error InsufficientBalance(uint256 required);
  
  // Error with many params: May be larger
  // revert InsufficientBalance(a, b, c, d) = 132 bytes
  // vs "Insufficient balance" = 68 + 20 = 88 bytes
  
  // Best practice: Max 2 parameters in custom errors
  
### **References**
  - https://soliditylang.org/blog/2021/04/21/custom-errors/

## SSTORE Refund Mechanics Changed

### **Id**
sstore-gas-refund
### **Severity**
MEDIUM
### **Description**
Gas refunds capped at 20% of total gas used
### **Symptoms**
  - Expected refunds not received
  - Clearing storage costs more than expected
  - Gas estimation off
### **Detection Pattern**
delete|= 0|sstore.*0
### **Solution**
  // Refund only happens when changing non-zero to zero
  // Max refund: 20% of gas used in transaction
  
  // Setting to zero: 2900 gas, refund 4800
  // Net cost: -1900 (gain) BUT capped at 20% of total
  
  // If tx uses 50000 gas, max refund = 10000
  // Multiple deletions may not all get refunded
  
  // Don't design around refunds - they're unreliable
  
### **References**
  - https://eips.ethereum.org/EIPS/eip-3529

## Yul Stack Depth Limit

### **Id**
yul-stack-depth
### **Severity**
MEDIUM
### **Description**
EVM has 16 accessible stack slots limit
### **Symptoms**
  - "Stack too deep" errors in assembly
  - Cannot access all local variables
  - Complex functions fail to compile
### **Detection Pattern**
assembly|function.*\{[^}]*\{[^}]*\}
### **Solution**
  // Use memory for intermediate values
  assembly {
      // Instead of many stack variables
      let ptr := mload(0x40)
      mstore(ptr, value1)
      mstore(add(ptr, 0x20), value2)
      // ... access via mload(add(ptr, offset))
  }
  
  // Break into helper functions
  function helper(uint256 a, uint256 b) internal pure returns (uint256) {
      // Separate stack frame
  }
  
### **References**
  - https://www.evm.codes/about#stack