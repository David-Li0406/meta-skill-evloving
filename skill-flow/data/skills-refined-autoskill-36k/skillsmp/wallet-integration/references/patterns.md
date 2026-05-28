# Wallet Integration Specialist

## Patterns


---
  #### **Name**
Progressive Wallet Connection
  #### **Description**
Guide users through connection step by step
  #### **When**
Building wallet connection flow
  #### **Implementation**
    - Detect available wallet providers
    - Show clear connection options
    - Handle installation prompts for missing wallets
    - Persist connection state across sessions
    - Support multiple wallet types
    

---
  #### **Name**
Transaction Preview
  #### **Description**
Show clear transaction details before signing
  #### **When**
Any write transaction
  #### **Implementation**
    - Decode function call to human-readable format
    - Show token amounts and recipients
    - Display gas estimates and total cost
    - Warn about unusual or high-value transactions
    - Allow transaction simulation preview
    

---
  #### **Name**
Optimistic Updates
  #### **Description**
Update UI before transaction confirms
  #### **When**
Improving perceived performance
  #### **Implementation**
    - Update UI immediately on tx submission
    - Show pending state clearly
    - Handle tx failure and revert UI
    - Use tx receipt for final confirmation
    - Clear pending state on confirmation
    

---
  #### **Name**
Chain Awareness
  #### **Description**
Handle multi-chain gracefully
  #### **When**
DApp supports multiple networks
  #### **Implementation**
    - Detect current chain on connection
    - Prompt chain switch when needed
    - Handle chain switch errors gracefully
    - Support adding custom chains
    - Show chain-specific assets and data
    

---
  #### **Name**
Signature Authentication
  #### **Description**
Use wallet signatures for auth
  #### **When**
Need authenticated sessions without passwords
  #### **Implementation**
    - Generate server-side nonce
    - Sign structured message (EIP-712 preferred)
    - Verify signature server-side
    - Issue session token on success
    - Handle signature rejection gracefully
    

---
  #### **Name**
Batch Transactions
  #### **Description**
Group multiple operations
  #### **When**
User needs multiple contract calls
  #### **Implementation**
    - Multicall for read operations
    - Multicall3 for write batching
    - Show aggregated gas savings
    - Handle partial failures
    - Support smart account batching
    

## Anti-Patterns


---
  #### **Name**
Wallet Lock-in
  #### **Description**
Only supporting one wallet provider
  #### **Problem**
Excludes users with other wallets
  #### **Solution**
Use wallet aggregators (RainbowKit, Web3Modal)

---
  #### **Name**
Silent Transactions
  #### **Description**
Submitting transactions without clear user consent
  #### **Problem**
Users sign things they don't understand, lose trust
  #### **Solution**
Always preview transaction details, get explicit approval

---
  #### **Name**
Ignoring Rejection
  #### **Description**
Not handling user rejection of wallet prompts
  #### **Problem**
Broken UI state, confused users
  #### **Solution**
Catch rejections, show helpful messages, allow retry

---
  #### **Name**
Chain Confusion
  #### **Description**
Not checking or handling wrong chain
  #### **Problem**
Users submit to wrong network, lose funds
  #### **Solution**
Check chain before transactions, auto-prompt switch

---
  #### **Name**
Connection Spam
  #### **Description**
Repeatedly prompting for wallet connection
  #### **Problem**
Annoying users, looking desperate
  #### **Solution**
Prompt once, remember connection, let user initiate

---
  #### **Name**
Raw Error Display
  #### **Description**
Showing raw wallet/RPC errors to users
  #### **Problem**
Confusing, unprofessional, unhelpful
  #### **Solution**
Parse errors, show human-readable messages with actions