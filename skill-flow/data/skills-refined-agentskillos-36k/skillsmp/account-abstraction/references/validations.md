# Account Abstraction - Validations

## Banned opcodes in validation

### **Id**
banned-opcodes
### **Severity**
error
### **Type**
regex
### **Pattern**
  - _validateSignature.*\{[^}]*(block\.|tx\.|gasleft)
### **Message**
Validation cannot use banned opcodes (block.*, tx.*, etc.)
### **Fix Action**
Remove time-dependent or gas-dependent logic from validation
### **Applies To**
  - *.sol

## Missing nonce validation

### **Id**
no-replay-protection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - _validateSignature(?!.*nonce)
### **Message**
UserOperation validation must check nonces
### **Fix Action**
Nonces are handled by EntryPoint, ensure getNonce() is correct
### **Applies To**
  - *.sol