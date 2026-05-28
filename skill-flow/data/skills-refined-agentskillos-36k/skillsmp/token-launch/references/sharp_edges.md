# Token Launch - Sharp Edges

## Vesting Timestamp Manipulation

### **Id**
vesting-timestamp-manipulation
### **Summary**
Block timestamp can be manipulated by miners
### **Severity**
medium
### **Situation**
  You use block.timestamp for vesting calculations. Miners can
  manipulate timestamps within ~15 second range, potentially
  allowing early claims.
  
### **Why**
  Ethereum allows miners to set block timestamps within a window.
  For long vesting periods this is negligible, but for short cliffs
  or frequent claims, it can be exploited.
  
### **Solution**
  # USE BLOCK NUMBERS FOR PRECISION
  
  // WRONG: Timestamp-based (manipulable)
  function claimable() public view returns (uint256) {
      uint256 elapsed = block.timestamp - startTime;
      return (totalAmount * elapsed) / vestingDuration;
  }
  
  // RIGHT: Block-based for critical timing
  uint256 public startBlock;
  uint256 public constant BLOCKS_PER_DAY = 7200; // ~12s blocks
  
  function claimable() public view returns (uint256) {
      uint256 elapsedBlocks = block.number - startBlock;
      uint256 vestingBlocks = vestingDays * BLOCKS_PER_DAY;
      return (totalAmount * elapsedBlocks) / vestingBlocks;
  }
  
  // For most vesting, timestamp is fine - block numbers
  // are overkill for 1-year cliffs. Use judgment.
  
### **Symptoms**
  - Users claim slightly before expected
  - Edge cases in vesting math
  - Inconsistent claim amounts
### **Detection Pattern**
block\.timestamp.*vesting|cliff

## Erc20 Approval Race

### **Id**
erc20-approval-race
### **Summary**
Token approval race condition in vesting deposits
### **Severity**
high
### **Situation**
  Your vesting contract requires users to approve, then deposit.
  Between approval and deposit, tokens can be front-run.
  
### **Why**
  The standard approve-then-transfer pattern has a known race
  condition. Attacker can front-run the second transaction.
  
### **Solution**
  # USE PERMIT OR INCREASE ALLOWANCE
  
  // WRONG: Standard approve pattern
  token.approve(vestingContract, amount);
  vestingContract.deposit(amount);
  
  // RIGHT: Use permit (ERC-2612)
  function depositWithPermit(
      uint256 amount,
      uint256 deadline,
      uint8 v, bytes32 r, bytes32 s
  ) external {
      IERC20Permit(address(token)).permit(
          msg.sender, address(this), amount, deadline, v, r, s
      );
      _deposit(msg.sender, amount);
  }
  
  // Alternative: Use increaseAllowance
  token.increaseAllowance(vestingContract, amount);
  
### **Symptoms**
  - Failed deposits after approval
  - Missing token transfers
  - Users reporting stolen tokens
### **Detection Pattern**
approve.*transferFrom

## Cliff Off By One

### **Id**
cliff-off-by-one
### **Summary**
Off-by-one error at cliff boundary
### **Severity**
medium
### **Situation**
  Your vesting math allows claims exactly at cliff end, but you
  use > instead of >= (or vice versa), causing 1-block errors.
  
### **Why**
  Boundary conditions in vesting are common bugs. Users should
  be able to claim at cliff end, not cliff end + 1.
  
### **Solution**
  # GET BOUNDARY CONDITIONS RIGHT
  
  // WRONG: Off-by-one (misses exact cliff moment)
  function isCliffPassed() public view returns (bool) {
      return block.timestamp > startTime + cliffDuration;
  }
  
  // RIGHT: Include exact boundary
  function isCliffPassed() public view returns (bool) {
      return block.timestamp >= startTime + cliffDuration;
  }
  
  // Write explicit tests for boundaries
  function test_cliffBoundary() public {
      vm.warp(startTime + cliffDuration - 1);
      assertEq(vesting.claimable(user), 0);
  
      vm.warp(startTime + cliffDuration);
      assertGt(vesting.claimable(user), 0); // Should be claimable
  }
  
### **Symptoms**
  - Users can't claim at expected time
  - Claims work "a second later"
  - Test failures at exact boundaries
### **Detection Pattern**
block\.timestamp\s*>\s*\w+.*cliff

## Tge Unlock Precision Loss

### **Id**
tge-unlock-precision-loss
### **Summary**
TGE unlock calculation loses precision
### **Severity**
high
### **Situation**
  You calculate TGE unlock as percentage of total. Using integer
  division, you lose tokens or allow overclaiming.
  
### **Why**
  Solidity integer division truncates. 25% of 1000 tokens = 250,
  but 25% of 999 = 249 (loses 0.75 tokens worth of value).
  
### **Solution**
  # USE PROPER PRECISION MATH
  
  // WRONG: Precision loss
  uint256 public constant TGE_PERCENT = 25;
  uint256 tgeUnlock = totalAmount * TGE_PERCENT / 100;
  
  // RIGHT: Higher precision constants
  uint256 public constant TGE_BPS = 2500; // 25% in basis points
  uint256 public constant BPS_DENOMINATOR = 10000;
  
  uint256 tgeUnlock = (totalAmount * TGE_BPS) / BPS_DENOMINATOR;
  
  // Store remaining for vesting to avoid accumulation errors
  uint256 vestingAmount = totalAmount - tgeUnlock;
  
  // BEST: Pre-compute exact amounts, not percentages
  struct Allocation {
      uint256 tgeAmount;      // Exact TGE tokens
      uint256 vestingAmount;  // Exact vesting tokens
      // Sum should equal totalAmount
  }
  
### **Symptoms**
  - Total claimed != total allocated
  - Dust amounts left in contract
  - Last claimer gets slightly more/less
### **Detection Pattern**
\*\s*\d+\s*/\s*100(?!\d)

## Launchpad Integration Reentrancy

### **Id**
launchpad-integration-reentrancy
### **Summary**
Launchpad callback reentrancy vulnerability
### **Severity**
critical
### **Situation**
  Your token sale contract has a callback to the launchpad.
  The callback can be exploited to re-enter before state updates.
  
### **Why**
  Launchpads often require callbacks for integration. If you
  update user balances after the callback, an attacker can
  re-enter and claim multiple times.
  
### **Solution**
  # CHECKS-EFFECTS-INTERACTIONS PATTERN
  
  // WRONG: State update after external call
  function claim() external {
      uint256 amount = pendingClaims[msg.sender];
      token.safeTransfer(msg.sender, amount);  // External call
      pendingClaims[msg.sender] = 0;  // State update AFTER
      launchpad.notifyClaim(msg.sender, amount);  // Another external
  }
  
  // RIGHT: Update state first
  function claim() external nonReentrant {
      uint256 amount = pendingClaims[msg.sender];
      require(amount > 0, "Nothing to claim");
  
      // Effects BEFORE interactions
      pendingClaims[msg.sender] = 0;
  
      // Then external calls
      token.safeTransfer(msg.sender, amount);
      launchpad.notifyClaim(msg.sender, amount);
  }
  
### **Symptoms**
  - Users claim more than allocated
  - Contract drains unexpectedly
  - Transaction traces show recursive calls
### **Detection Pattern**
safeTransfer.*=\s*0|transfer.*pending\w+\s*=

## Multi Round Allocation Conflict

### **Id**
multi-round-allocation-conflict
### **Summary**
Private and public round allocations conflict
### **Severity**
high
### **Situation**
  Same wallet participates in private and public rounds. Your
  contract tracks only one allocation per address, overwriting
  the first.
  
### **Why**
  Many early investors also participate in public sales. Naive
  mapping(address => uint256) overwrites their private allocation.
  
### **Solution**
  # SEPARATE ALLOCATIONS PER ROUND
  
  // WRONG: Single allocation mapping
  mapping(address => uint256) public allocations;
  
  function allocatePrivate(address user, uint256 amount) external {
      allocations[user] = amount;  // Overwrites!
  }
  
  // RIGHT: Per-round allocations
  enum Round { Seed, Private, Public }
  
  mapping(address => mapping(Round => uint256)) public allocations;
  
  function allocate(address user, Round round, uint256 amount) external {
      allocations[user][round] = amount;
  }
  
  function totalAllocation(address user) public view returns (uint256) {
      return allocations[user][Round.Seed]
           + allocations[user][Round.Private]
           + allocations[user][Round.Public];
  }
  
### **Symptoms**
  - Investors report missing allocations
  - Total distributed != expected
  - Allocation proofs don't match contract
### **Detection Pattern**


## Decimal Mismatch

### **Id**
decimal-mismatch
### **Summary**
Token decimal mismatch causes wrong amounts
### **Severity**
critical
### **Situation**
  You assume 18 decimals for all tokens. A 6-decimal stablecoin
  (USDC) causes calculations to be off by 10^12.
  
### **Why**
  ERC20 has no standard decimals. USDC/USDT are 6 decimals,
  WBTC is 8 decimals. Hardcoding 18 decimals causes major errors.
  
### **Solution**
  # ALWAYS QUERY DECIMALS
  
  // WRONG: Hardcoded decimals
  uint256 public constant DECIMALS = 18;
  uint256 price = amount * tokenPrice / (10 ** DECIMALS);
  
  // RIGHT: Query from token contract
  function _getDecimals(address token) internal view returns (uint8) {
      return IERC20Metadata(token).decimals();
  }
  
  function calculateTokens(uint256 paymentAmount) public view returns (uint256) {
      uint8 paymentDecimals = _getDecimals(paymentToken);
      uint8 saleDecimals = _getDecimals(saleToken);
  
      // Normalize to 18 decimals for calculation
      uint256 normalizedPayment = paymentAmount * 10**(18 - paymentDecimals);
      uint256 tokensNormalized = normalizedPayment * tokensPerUnit / 1e18;
  
      // Convert back to sale token decimals
      return tokensNormalized / 10**(18 - saleDecimals);
  }
  
### **Symptoms**
  - Users receive 10^12x more/fewer tokens
  - Sale ends immediately or never fills
  - Price displays incorrectly
### **Detection Pattern**
10\s*\*\*\s*18|1e18.*decimals

## Unchecked Whitelist Removal

### **Id**
unchecked-whitelist-removal
### **Summary**
Whitelist removal during active vesting
### **Severity**
medium
### **Situation**
  Admin removes user from whitelist mid-vesting. User loses
  access to unvested tokens they legitimately own.
  
### **Why**
  Whitelists should only control initial eligibility, not
  ongoing vesting rights. Once allocated, tokens belong to user.
  
### **Solution**
  # SEPARATE ELIGIBILITY FROM VESTING
  
  // WRONG: Whitelist gates claiming
  function claim() external {
      require(isWhitelisted[msg.sender], "Not whitelisted");
      _claim(msg.sender);
  }
  
  // RIGHT: Whitelist only for initial allocation
  function allocate(address user, uint256 amount) external onlyOwner {
      require(isWhitelisted[user], "Not whitelisted");
      vestingSchedules[user] = VestingSchedule(...);
      // Whitelist no longer relevant after allocation
  }
  
  function claim() external {
      require(vestingSchedules[msg.sender].totalAmount > 0, "No allocation");
      _claim(msg.sender);
  }
  
### **Symptoms**
  - Users locked out of earned tokens
  - Support tickets about missing claims
  - Legal disputes over vested amounts
### **Detection Pattern**
whitelist.*claim|claim.*whitelist

## Launch Time Timezone

### **Id**
launch-time-timezone
### **Summary**
Launch time timezone confusion
### **Severity**
low
### **Situation**
  You announce launch at "12:00 PM" without timezone. Half your
  community misses the launch, others arrive 12 hours early.
  
### **Why**
  Crypto is global. UTC is the only timezone that works for
  everyone. Local times cause confusion and missed opportunities.
  
### **Solution**
  # ALWAYS USE UTC
  
  // In announcements
  ❌ "Launch: December 15, 12:00 PM"
  ✅ "Launch: December 15, 12:00 UTC"
  ✅ "Launch: December 15, 12:00 UTC (convert to local time)"
  
  // In contracts, store unix timestamp
  uint256 public launchTime = 1702641600; // Fixed point in time
  
  // Provide timezone conversion tool in UI
  function formatLaunchTime() external view returns (string memory) {
      // Frontend should handle timezone conversion
      return "See contract for UTC timestamp";
  }
  
  // Frontend
  const launchDate = new Date(launchTime * 1000);
  const localTime = launchDate.toLocaleString();
  const utcTime = launchDate.toUTCString();
  
### **Symptoms**
  - Community confusion about times
  - Some users miss launch entirely
  - Support overload pre-launch
### **Detection Pattern**


## Gas Spike Launch

### **Id**
gas-spike-launch
### **Summary**
Gas price spikes during launch block liquidity
### **Severity**
high
### **Situation**
  Your launch coincides with high network activity. Gas prices
  10x, and small buyers get priced out or fail transactions.
  
### **Why**
  Popular launches create gas wars. Bots pay extreme gas to
  get priority. Regular users can't compete and waste gas on
  failed transactions.
  
### **Solution**
  # DESIGN FOR GAS SPIKES
  
  // Prevent gas wars with max gas price
  uint256 public maxGasPrice = 100 gwei;
  
  modifier reasonableGas() {
      require(tx.gasprice <= maxGasPrice, "Gas price too high");
      _;
  }
  
  function buy() external payable reasonableGas {
      // Regular users have a chance
  }
  
  // Better: Use commit-reveal or queue system
  mapping(address => bytes32) public commitments;
  mapping(address => uint256) public revealWindow;
  
  function commit(bytes32 hash) external {
      commitments[msg.sender] = hash;
      revealWindow[msg.sender] = block.number + 10;
  }
  
  function reveal(uint256 amount, bytes32 salt) external {
      require(block.number >= revealWindow[msg.sender], "Too early");
      require(keccak256(abi.encode(amount, salt)) == commitments[msg.sender]);
      _processBuy(msg.sender, amount);
  }
  
### **Symptoms**
  - Failed transactions during launch
  - Only bots get allocations
  - Gas costs exceed purchase value
### **Detection Pattern**
