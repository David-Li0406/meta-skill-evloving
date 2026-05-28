# Cross Chain - Validations

## No finality confirmation check

### **Id**
no-finality-check
### **Severity**
error
### **Type**
regex
### **Pattern**
  - processMessage(?!.*confirmations|.*finality)
### **Message**
Cross-chain messages must wait for source chain finality
### **Fix Action**
Add block confirmation requirements before processing
### **Applies To**
  - *.sol

## Single relayer without decentralization

### **Id**
single-relayer
### **Severity**
error
### **Type**
regex
### **Pattern**
  - onlyRelayer(?!.*multisig|.*threshold)
### **Message**
Bridges should use decentralized relayer set or multi-sig
### **Fix Action**
Implement threshold signatures or use established bridge
### **Applies To**
  - *.sol

## No message deduplication

### **Id**
no-message-dedup
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function.*receive.*Message(?!.*processed|.*nonce)
### **Message**
Must prevent replay of cross-chain messages
### **Fix Action**
Track processed message IDs or nonces
### **Applies To**
  - *.sol

## Bridge without pause capability

### **Id**
no-pause-function
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - contract.*Bridge(?!.*Pausable|.*pause)
### **Message**
Bridges should have emergency pause functionality
### **Fix Action**
Inherit Pausable and add pause controls
### **Applies To**
  - *.sol

## Hardcoded gas limits for destination

### **Id**
hardcoded-gas
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - gasLimit\s*[=:]\s*\d+(?!.*configurable)
### **Message**
Gas limits should be configurable per chain/message type
### **Fix Action**
Make gas limits adjustable or estimate dynamically
### **Applies To**
  - *.sol