# Onchain Analytics - Validations

## Hardcoded token decimals

### **Id**
hardcoded-decimals
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - POWER\(10,\s*18\)|1e18|10\^18
### **Message**
Token decimals vary - query from tokens.erc20
### **Fix Action**
JOIN tokens.erc20 and use decimals column
### **Applies To**
  - *.sql

## Missing blockchain filter in cross-chain query

### **Id**
no-blockchain-filter
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - FROM\s+\w+\s+WHERE(?!.*blockchain)
### **Message**
Specify blockchain for cross-chain tables
### **Fix Action**
Add WHERE blockchain = 'ethereum' or similar
### **Applies To**
  - *.sql