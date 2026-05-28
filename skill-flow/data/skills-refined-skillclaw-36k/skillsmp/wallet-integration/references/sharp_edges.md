# Wallet Integration - Sharp Edges

## Single Wallet Support

### **Id**
single-wallet-support
### **Summary**
Only supporting MetaMask or single wallet
### **Severity**
high
### **Situation**
Hardcoding MetaMask detection or connection
### **Why**
  Users have different wallets (Coinbase Wallet, WalletConnect, Rainbow,
  etc.). Supporting only MetaMask excludes a significant portion of users.
  Mobile users especially use non-MetaMask wallets.
  
### **Solution**
  Use wallet aggregators:
  - RainbowKit or Web3Modal for wallet selection
  - wagmi for standardized connection hooks
  - Support WalletConnect for mobile
  - Detect and list available wallets
  
### **Symptoms**
  - Users can't connect their wallet
  - Mobile users report issues
  - Low wallet connection rates
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
window\.ethereum(?!.*providers)|ethereum\.isMetaMask|detectMetaMask

## Unhandled Rejection

### **Id**
unhandled-rejection
### **Summary**
Not handling user wallet rejection
### **Severity**
high
### **Situation**
Wallet prompts can be rejected by user
### **Why**
  Users reject wallet prompts for many reasons - wrong account, changed
  mind, accidental click. Unhandled rejections leave UI in broken state
  or show cryptic errors.
  
### **Solution**
  Handle all rejection cases:
  - Connection rejection → clear UI state, show retry
  - Transaction rejection → revert optimistic updates
  - Signature rejection → allow retry without restart
  - Show user-friendly messages
  
### **Symptoms**
  - UI stuck after user cancels
  - Cryptic error messages
  - Users confused about state
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
await.*connect\(\)(?!.*catch)|await.*sendTransaction(?!.*catch)

## Wrong Chain Blindness

### **Id**
wrong-chain-blindness
### **Summary**
Not checking or handling wrong chain
### **Severity**
critical
### **Situation**
User on different chain than app expects
### **Why**
  Users submit transactions to wrong network and can't understand why
  things don't work. Worse, they might send tokens to wrong chain
  addresses, losing funds.
  
### **Solution**
  Chain awareness:
  - Check chainId on connection
  - Prompt switch to correct chain
  - Block transactions on wrong chain
  - Show clear chain indicator in UI
  
### **Symptoms**
  - Transactions fail with unclear errors
  - Users confused about which chain
  - Support tickets about lost funds
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
sendTransaction(?!.*chainId)|contract\.(?!.*verifyChain)

## No Transaction Preview

### **Id**
no-transaction-preview
### **Summary**
Signing transactions without preview
### **Severity**
high
### **Situation**
Direct transaction submission without showing details
### **Why**
  Users sign transactions they don't understand. This erodes trust and
  can lead to accidental high-value transfers or approval of malicious
  contracts. Users deserve to know what they're signing.
  
### **Solution**
  Transaction preview:
  - Decode function call to human-readable
  - Show token amounts and recipients
  - Display gas estimate and total cost
  - Simulate transaction before submission
  
### **Symptoms**
  - Users unsure what they signed
  - Unexpected transaction results
  - Low user trust
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
sendTransaction\(|contract\.write(?!.*preview|.*simulate)

## Raw Error Display

### **Id**
raw-error-display
### **Summary**
Showing raw RPC/wallet errors to users
### **Severity**
medium
### **Situation**
Displaying error.message directly
### **Why**
  Wallet and RPC errors are technical and unhelpful to users. Messages
  like "insufficient funds for gas * price + value" or "nonce too low"
  confuse users and look unprofessional.
  
### **Solution**
  Error translation:
  - Parse common error codes
  - Map to user-friendly messages
  - Include actionable next steps
  - Log technical details for debugging
  
### **Symptoms**
  - Confused users
  - Support requests about errors
  - Unprofessional appearance
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
alert\(error|toast.*error\.message|setError\(e\.message

## Unlimited Approval

### **Id**
unlimited-approval
### **Summary**
Requesting unlimited token approval
### **Severity**
high
### **Situation**
Approving type(uint256).max for convenience
### **Why**
  Unlimited approval means if the approved contract is compromised, all
  tokens can be drained. Users are increasingly aware of this risk and
  distrust DApps that request unlimited approvals.
  
### **Solution**
  Exact approvals:
  - Approve only the amount needed
  - Or use permit signatures (EIP-2612)
  - Explain approval amounts to users
  - Show current approvals and allow revocation
  
### **Symptoms**
  - Security-conscious users refuse
  - Risk of total loss if contract hacked
  - Bad security reputation
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
approve.*MAX_UINT|approve.*2\*\*256|approve.*type\(uint256\)\.max

## Connection Spam

### **Id**
connection-spam
### **Summary**
Repeatedly prompting for wallet connection
### **Severity**
medium
### **Situation**
Showing connect prompt on every page/action
### **Why**
  Constant connection prompts are annoying and desperate-looking. Users
  should connect once and stay connected. Aggressive prompting drives
  users away.
  
### **Solution**
  Respectful connection flow:
  - Persist connection state
  - Single, clear connect button
  - Remember user preference
  - Don't block content behind wallet
  
### **Symptoms**
  - Users annoyed by prompts
  - High bounce rate
  - Users report aggressive UX
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
useEffect.*connect\(|componentDidMount.*connect|autoConnect.*true

## No Pending State

### **Id**
no-pending-state
### **Summary**
Not showing transaction pending state
### **Severity**
medium
### **Situation**
UI unchanged while transaction confirms
### **Why**
  Blockchain transactions take time. Without pending state, users think
  the action failed or click again, potentially submitting duplicate
  transactions.
  
### **Solution**
  Clear pending UX:
  - Show pending state immediately
  - Link to block explorer
  - Disable repeat actions
  - Update on confirmation
  
### **Symptoms**
  - Users submit duplicate transactions
  - Confusion about transaction status
  - Support requests about 'stuck' transactions
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
await.*sendTransaction(?!.*setPending|.*setLoading)