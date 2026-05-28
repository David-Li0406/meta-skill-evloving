# Web3 Gaming - Validations

## Missing token emission cap

### **Id**
no-emission-cap
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function\s+mint.*\{(?!.*cap|.*limit|.*max)
### **Message**
Token minting should have emission caps to prevent inflation
### **Fix Action**
Add dailyEmissionCap and enforce in mint function
### **Applies To**
  - *.sol

## Missing cooldown on reward claims

### **Id**
no-cooldown
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+(claim|harvest|collect).*\{(?!.*cooldown|.*lastClaim)
### **Message**
Reward claims should have cooldown to prevent rapid farming
### **Fix Action**
Add mapping for lastClaimTime and enforce minimum interval
### **Applies To**
  - *.sol

## Trusting client-provided reward amounts

### **Id**
client-trusted-amount
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function\s+claim.*uint256\s+amount.*\{(?!.*signature|.*verify)
### **Message**
Reward amounts should be server-signed, not client-provided
### **Fix Action**
Implement server-side signing of reward claims
### **Applies To**
  - *.sol

## Centralized metadata URL

### **Id**
centralized-metadata
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - tokenURI.*"https://|baseURI.*"http://
### **Message**
NFT metadata should use IPFS or on-chain storage
### **Fix Action**
Use ipfs:// or arweave:// for metadata permanence
### **Applies To**
  - *.sol

## No burn mechanism for items

### **Id**
missing-item-burn
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ERC1155(?!.*burn)
### **Message**
Game items should have burn mechanism for economic sinks
### **Fix Action**
Implement burn function for item consumption
### **Applies To**
  - *.sol

## Game functions without role protection

### **Id**
unprotected-game-functions
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function\s+(mint|reward|upgrade).*public(?!.*onlyRole|.*onlyGame)
### **Message**
Game state-changing functions need access control
### **Fix Action**
Add onlyRole(GAME_ROLE) or similar modifier
### **Applies To**
  - *.sol

## No pause functionality

### **Id**
missing-pause
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - contract\s+\w+(?!.*Pausable)
### **Message**
Game contracts should have pause for emergencies
### **Fix Action**
Inherit from Pausable and add whenNotPaused modifier
### **Applies To**
  - *.sol

## Signature without expiry

### **Id**
missing-expiry
### **Severity**
error
### **Type**
regex
### **Pattern**
  - keccak256.*signature(?!.*expiry|.*deadline)
### **Message**
Signed messages should include expiry timestamp
### **Fix Action**
Add expiry to hash and verify block.timestamp < expiry
### **Applies To**
  - *.sol

## Signature without chain ID

### **Id**
missing-chain-id
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - keccak256.*abi\.encode(?!.*chainid)
### **Message**
Include chain ID in signature to prevent cross-chain replay
### **Fix Action**
Add block.chainid to the signed hash
### **Applies To**
  - *.sol

## Signature without nonce

### **Id**
missing-nonce
### **Severity**
error
### **Type**
regex
### **Pattern**
  - verify.*signature(?!.*nonce)
### **Message**
Signatures should use nonces to prevent replay
### **Fix Action**
Track per-user nonces and include in signed hash
### **Applies To**
  - *.sol

## No rate limiting on actions

### **Id**
no-rate-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - function\s+play|function\s+battle(?!.*rateLimit|.*lastAction)
### **Message**
Game actions should be rate-limited to prevent automation
### **Fix Action**
Add per-action cooldowns and daily limits
### **Applies To**
  - *.sol