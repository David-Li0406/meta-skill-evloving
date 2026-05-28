# Wallet Integration - Validations

## MetaMask Only Detection

### **Id**
metamask-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - window\.ethereum(?!.*providers)
  - ethereum\.isMetaMask
  - detectMetaMask
### **Message**
Hardcoded MetaMask detection excludes other wallet users.
### **Fix Action**
Use wallet aggregator (RainbowKit, Web3Modal) or multi-wallet detection
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Unhandled Connection Rejection

### **Id**
unhandled-connect-rejection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - await.*connect\(\)(?!.*catch)
  - ethereum\.request.*eth_requestAccounts(?!.*catch)
  - \.connect\(\)\.then(?!.*catch)
### **Message**
Wallet connection rejection not handled - UI may break.
### **Fix Action**
Handle connection rejection with try/catch and user message
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Unhandled Transaction Rejection

### **Id**
unhandled-tx-rejection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - await.*sendTransaction(?!.*catch)
  - await.*write(?!.*catch)
  - await.*signMessage(?!.*catch)
### **Message**
Transaction/signature rejection not handled.
### **Fix Action**
Handle rejection, show message, and allow retry
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## No Chain ID Check

### **Id**
no-chain-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - sendTransaction(?!.*chainId)
  - write(?!.*chain)
  - contract\.(?!.*verifyChain)
### **Message**
Transaction without chain check - user may be on wrong network.
### **Fix Action**
Check chainId before transactions, prompt switch if needed
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Unlimited Token Approval

### **Id**
unlimited-approval
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - approve.*MAX_UINT
  - approve.*2\*\*256
  - approve.*type\(uint256\)\.max
  - MaxUint256
### **Message**
Unlimited approval is risky if contract is compromised.
### **Fix Action**
Approve exact amounts or use permit (EIP-2612)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.sol

## Raw Error Display

### **Id**
raw-error-display
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - alert\(error
  - toast.*error\.message
  - setError\(e\.message
  - console\.error\(.*\)\s*$
### **Message**
Raw wallet/RPC errors shown to users are confusing.
### **Fix Action**
Parse errors and show user-friendly messages
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Aggressive Auto-Connect

### **Id**
auto-connect-aggressive
### **Severity**
info
### **Type**
regex
### **Pattern**
  - useEffect.*connect\(
  - componentDidMount.*connect
  - autoConnect:\s*true
### **Message**
Aggressive auto-connect may annoy users with prompts.
### **Fix Action**
Let user initiate connection, persist state across sessions
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## No Pending State

### **Id**
no-pending-state
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await.*sendTransaction(?!.*setPending|.*setLoading|.*isLoading)
  - await.*write(?!.*isPending|.*isLoading)
### **Message**
Transaction submitted without pending state - user may resubmit.
### **Fix Action**
Show pending state, disable button, update on confirmation
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Hardcoded RPC URL

### **Id**
hardcoded-rpc
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - https://mainnet\.infura\.io
  - https://eth-mainnet\.g\.alchemy\.com
  - rpc.*=.*["']https://(?!.*env)
### **Message**
Hardcoded RPC URL - should be configurable via environment.
### **Fix Action**
Use environment variable for RPC URL
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Excludes**
  - **/.env*
  - **/config.*