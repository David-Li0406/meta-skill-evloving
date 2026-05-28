# Layer2 Scaling - Sharp Edges

## Sequencer Downtime Causes Complete Outage

### **Id**
sequencer-downtime
### **Severity**
CRITICAL
### **Description**
Single sequencer going down stops all transactions
### **Symptoms**
  - Transactions not being included
  - dApp appears frozen
  - Users panic about stuck funds
### **Detection Pattern**
sendTransaction|write.*contract
### **Solution**
  // 1. Use Chainlink sequencer uptime feed
  AggregatorV2V3Interface sequencerFeed = AggregatorV2V3Interface(
      // Arbitrum: 0xFdB631F5EE196F0ed6FAa767959853A9F217697D
      // Optimism: 0x371EAD81c9102C9BF4874A9075FFFf170F2Ee389
      SEQUENCER_FEED
  );
  
  function isSequencerUp() public view returns (bool) {
      (, int256 answer, , , ) = sequencerFeed.latestRoundData();
      return answer == 0;
  }
  
  // 2. Implement graceful degradation
  // 3. Show users clear status messages
  // 4. Document forced inclusion path
  
### **References**
  - https://docs.chain.link/data-feeds/l2-sequencer-feeds

## L1 Gas Spike Makes L2 Transactions Expensive

### **Id**
l1-data-cost-spike
### **Severity**
CRITICAL
### **Description**
L2 costs tied to L1 gas prices, which are volatile
### **Symptoms**
  - Sudden 10-100x cost increase
  - Transactions failing due to insufficient gas
  - User complaints about fees
### **Detection Pattern**
getL1Fee|l1BaseFee|estimateGas
### **Solution**
  // Dynamic fee handling
  async function safeTransaction(tx) {
      // Get current L1 fee
      const l1Fee = await oracle.getL1Fee(tx.data);
      const l2Fee = tx.gasLimit * await provider.getGasPrice();
  
      // Check against max acceptable
      const totalFee = l1Fee.add(l2Fee);
      if (totalFee.gt(maxAcceptableFee)) {
          // Option 1: Wait for lower fees
          // Option 2: Use fee estimator with buffer
          // Option 3: Alert user to high fees
          throw new Error(`Fee too high: ${formatEther(totalFee)}`);
      }
  
      // Add 20% buffer for L1 volatility
      tx.gasPrice = tx.gasPrice.mul(120).div(100);
      return sendTransaction(tx);
  }
  
### **References**
  - https://community.optimism.io/docs/developers/build/transaction-fees/

## 7-Day Withdrawal Delay on Optimistic Rollups

### **Id**
seven-day-withdrawal
### **Severity**
HIGH
### **Description**
Funds locked for 7 days when withdrawing to L1
### **Symptoms**
  - Users expecting instant withdrawals
  - Liquidity issues
  - Support tickets about "stuck" funds
### **Detection Pattern**
withdraw|bridge.*l1|finalize
### **Solution**
  // Educate users upfront
  function initiateWithdrawal(uint256 amount) external {
      // Show warning in UI
      emit WithdrawalInitiated(
          msg.sender,
          amount,
          block.timestamp + 7 days // Estimated finalization
      );
  
      // Alternative: Use fast bridge (Across, Hop)
      // Trade-off: Fee vs speed
  }
  
  // Fast bridge integration
  async function fastWithdraw(amount) {
      // Across/Hop take 2-10 minutes
      // Fee: 0.1-0.3%
      const quote = await acrossProtocol.getQuote(amount);
      return acrossProtocol.deposit(amount, quote);
  }
  
### **References**
  - https://docs.across.to/

## zkSync State Diff Costs Differ from EVM

### **Id**
zk-state-diff-costs
### **Severity**
HIGH
### **Description**
zkSync charges for state changes, not calldata
### **Symptoms**
  - Gas estimates wildly different from actual
  - Contract deployments much more expensive
  - Storage-heavy operations cost more than expected
### **Detection Pattern**
zksync|zkSync|era
### **Solution**
  // zkSync gas = L2 execution + L1 pubdata
  
  // Pubdata cost factors:
  // 1. Storage slot changes (not reads)
  // 2. Contract bytecode
  // 3. Event logs
  
  // Optimization strategies:
  // 1. Batch storage writes
  // 2. Use smaller data types
  // 3. Minimize events
  
  // Test on zkSync specifically
  const zkSyncProvider = new Provider("https://mainnet.era.zksync.io");
  const gasEstimate = await zkSyncProvider.estimateGas(tx);
  // This includes pubdata costs
  
### **References**
  - https://docs.zksync.io/build/developer-reference/fee-model

## Block Times Vary Significantly Across L2s

### **Id**
block-time-differences
### **Severity**
HIGH
### **Description**
L2 block times range from 250ms to 2 seconds
### **Symptoms**
  - Timing-based logic fails
  - Rate limiting doesn't work as expected
  - Time-locked operations behave unexpectedly
### **Detection Pattern**
block\.timestamp|block\.number
### **Solution**
  // Block times by L2:
  // Arbitrum: ~250ms
  // Optimism: 2 seconds
  // Base: 2 seconds
  // zkSync: Variable
  
  // Don't assume consistent block times
  // Use timestamps, not block numbers
  
  // Bad
  require(block.number > lastBlock + 100, "Too soon");
  
  // Good
  require(block.timestamp > lastTimestamp + 1 hours, "Too soon");
  
  // For cross-L2 apps, use oracle timestamps
  
### **References**
  - https://docs.arbitrum.io/build-decentralized-apps/arbitrum-vs-ethereum

## CREATE2 Addresses Differ on zkSync

### **Id**
address-derivation-zksync
### **Severity**
HIGH
### **Description**
zkSync uses different address derivation than EVM
### **Symptoms**
  - Contracts deploy to unexpected addresses
  - Cross-chain address matching fails
  - Factory patterns break
### **Detection Pattern**
create2|CREATE2|deploy.*address
### **Solution**
  // zkSync uses different hash for CREATE2
  // address = keccak256(
  //   0xff ++ deployer ++ salt ++ keccak256(bytecode_hash ++ constructor_args)
  // )
  
  // Use zkSync SDK for address calculation
  import { utils } from "zksync-web3";
  
  const address = utils.create2Address(
      deployerAddress,
      bytecodeHash,
      salt,
      constructorArgs
  );
  
  // For cross-chain deployments, deploy separately
  // and register addresses in a registry
  
### **References**
  - https://docs.zksync.io/build/developer-reference/ethereum-differences/evm-instructions

## Soft Confirmations Can Reorg

### **Id**
reorg-risk
### **Severity**
MEDIUM
### **Description**
Sequencer confirmations aren't final until L1 inclusion
### **Symptoms**
  - Confirmed transactions disappear
  - State reverts unexpectedly
  - Double-spend in edge cases
### **Detection Pattern**
await.*wait|confirmation|finality
### **Solution**
  // Finality levels:
  // 1. Sequencer confirm: ~2s (CAN REORG)
  // 2. L1 batch submission: ~5-15 min (safer)
  // 3. L1 finality: ~15 min (very safe)
  // 4. Challenge complete: 7 days (final)
  
  // For high-value operations
  async function waitForSafeConfirmation(txHash) {
      const receipt = await provider.waitForTransaction(txHash);
  
      // Wait for L1 batch inclusion
      const l1BatchNumber = await getL1BatchNumber(receipt.blockNumber);
      await waitForL1Finality(l1BatchNumber);
  
      return receipt;
  }
  
### **References**
  - https://docs.optimism.io/builders/app-developers/transactions/statuses

## Precompiles May Differ on L2s

### **Id**
precompile-differences
### **Severity**
MEDIUM
### **Description**
Some precompiles missing or behave differently
### **Symptoms**
  - Cryptographic operations fail
  - Gas costs different than expected
  - Contract reverts on specific L2
### **Detection Pattern**
ecrecover|sha256|ripemd|modexp
### **Solution**
  // Check precompile support per L2:
  // - ecrecover: Supported everywhere
  // - sha256: Supported everywhere
  // - ripemd160: May not be supported
  // - modexp: May have different gas costs
  // - bn128: Varies by L2
  
  // For ZK rollups, some precompiles need ZK circuits
  // which may not be implemented
  
  // Test all cryptographic operations on target L2
  function testPrecompiles() public view {
      // Test each precompile you use
      bytes32 hash = sha256("test");
      require(hash != bytes32(0), "sha256 failed");
  }
  
### **References**
  - https://docs.zksync.io/build/developer-reference/ethereum-differences/precompiles

## L1 Block Info Access Patterns

### **Id**
l1-block-info
### **Severity**
MEDIUM
### **Description**
Accessing L1 block data requires special handling on L2
### **Symptoms**
  - L1 blockhash unavailable
  - L1 timestamp stale
  - Cross-layer timing issues
### **Detection Pattern**
L1Block|l1BlockNumber|blockhash
### **Solution**
  // Optimism L1 Block predeploy
  import {L1Block} from "@eth-optimism/contracts/L2/L1Block.sol";
  
  contract L1Aware {
      L1Block constant l1Block = L1Block(
          0x4200000000000000000000000000000000000015
      );
  
      function getL1Info() public view returns (
          uint64 number,
          uint64 timestamp,
          uint256 basefee,
          bytes32 hash
      ) {
          return (
              l1Block.number(),
              l1Block.timestamp(),
              l1Block.basefee(),
              l1Block.hash()
          );
      }
  }
  
  // Note: L1 info may be delayed by seconds/minutes
  
### **References**
  - https://docs.optimism.io/builders/chain-operators/architecture

## Some L2s Use Custom Gas Tokens

### **Id**
gas-token-differences
### **Severity**
MEDIUM
### **Description**
Not all L2s use ETH for gas
### **Symptoms**
  - Transaction fee calculation wrong
  - Wallet shows incorrect balance
  - Bridge calculations off
### **Detection Pattern**
gasPrice|tx\.gasprice|msg\.value
### **Solution**
  // L2 gas tokens:
  // Optimism/Arbitrum/Base: ETH
  // zkSync Era: ETH
  // Mantle: MNT
  // Metis: METIS
  
  // For non-ETH gas L2s:
  // 1. Users need gas token, not just ETH
  // 2. Fee estimation uses gas token price
  // 3. msg.value is still in ETH
  
  // Check chain and adapt
  function getGasToken() public view returns (address) {
      if (block.chainid == 5000) return MANTLE_TOKEN;
      if (block.chainid == 1088) return METIS_TOKEN;
      return address(0); // ETH
  }
  
### **References**
  - https://docs.mantle.xyz/network/introduction/overview

## Different Contract Size Limits on L2s

### **Id**
contract-size-limits
### **Severity**
MEDIUM
### **Description**
L2s may have different or additional size constraints
### **Symptoms**
  - Deployment fails on specific L2
  - Works on testnet but not mainnet
  - Bytecode too large errors
### **Detection Pattern**
deploy|bytecode|contract.*size
### **Solution**
  // Size limits:
  // Ethereum: 24KB max
  // Arbitrum: 24KB but different initcode limits
  // zkSync: Different due to circuit constraints
  
  // Solutions:
  // 1. Use proxy patterns (smaller deployment)
  // 2. Split into multiple contracts
  // 3. Use libraries
  
  // Check size during build
  forge build --sizes
  
  // Diamond pattern for complex contracts
  // Deploy logic in facets, under 24KB each
  
### **References**
  - https://docs.arbitrum.io/build-decentralized-apps/solidity-support