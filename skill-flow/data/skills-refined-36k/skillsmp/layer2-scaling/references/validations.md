# Layer2 Scaling - Validations

## L1 Gas Cost Handling

### **Id**
check-l1-gas-handling
### **Description**
Verify L1 data costs are considered
### **Pattern**
getL1Fee|l1BaseFee|GasPriceOracle
### **File Glob**
**/*.sol
### **Match**
absent_in_context
### **Context Pattern**
estimateGas|gasPrice|fee
### **Message**
Consider L1 data costs in gas estimation for L2
### **Severity**
warning
### **Autofix**


## Sequencer Uptime Handling

### **Id**
check-sequencer-awareness
### **Description**
Critical operations should check sequencer status
### **Pattern**
sequencerFeed|isSequencerUp
### **File Glob**
**/*.sol
### **Match**
absent_in_context
### **Context Pattern**
oracle|price|liquidat
### **Message**
Consider sequencer uptime checks for price-sensitive operations
### **Severity**
warning
### **Autofix**


## Finality Awareness

### **Id**
check-finality-handling
### **Description**
High-value operations should wait for appropriate finality
### **Pattern**
waitForTransaction|confirmations?:\s*[12]\s*[,}]
### **File Glob**
**/*.ts
### **Match**
present
### **Message**
1-2 confirmations may not be sufficient for L2 finality
### **Severity**
info
### **Autofix**


## Bridge Message Authentication

### **Id**
check-bridge-authentication
### **Description**
Verify bridge receivers authenticate messages
### **Pattern**
xDomainMessageSender|sourceSender
### **File Glob**
**/*.sol
### **Match**
absent_in_context
### **Context Pattern**
receive.*Message|cross.*domain
### **Message**
Bridge receivers must authenticate message source
### **Severity**
error
### **Autofix**


## L2-Specific Addresses

### **Id**
check-hardcoded-addresses
### **Description**
Check for hardcoded L2-specific addresses
### **Pattern**
0x4200000000000000000000000000000
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Verify L2 predeploy addresses are correct for target chain
### **Severity**
info
### **Autofix**


## Calldata Optimization

### **Id**
check-calldata-size
### **Description**
Large calldata increases L2 costs significantly
### **Pattern**
bytes\s+memory|string\s+memory
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
external|public
### **Message**
Consider calldata instead of memory for external functions on L2
### **Severity**
info
### **Autofix**


## Block Timing Assumptions

### **Id**
check-block-timestamp
### **Description**
Block times vary across L2s
### **Pattern**
block\.number.*\+|block\.number.*-
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Use block.timestamp instead of block.number for timing on L2
### **Severity**
warning
### **Autofix**


## CREATE2 L2 Compatibility

### **Id**
check-create2-usage
### **Description**
CREATE2 addresses differ on some L2s
### **Pattern**
create2|CREATE2
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
CREATE2 address derivation differs on zkSync - test on target L2
### **Severity**
info
### **Autofix**


## Withdrawal Period Handling

### **Id**
check-withdrawal-handling
### **Description**
Verify withdrawal delay is handled
### **Pattern**
withdraw.*L1|bridge.*out
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
7.*day|delay|finalize
### **Message**
Document 7-day withdrawal delay for optimistic rollups
### **Severity**
info
### **Autofix**


## Multi-Chain Configuration

### **Id**
check-multi-chain-config
### **Description**
Chain-specific configurations should be parameterized
### **Pattern**
chainId.*==|block\.chainid.*==
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Consider using configuration contracts for multi-chain deployments
### **Severity**
info
### **Autofix**
