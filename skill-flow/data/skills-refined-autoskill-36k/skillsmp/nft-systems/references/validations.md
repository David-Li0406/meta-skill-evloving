# Nft Systems - Validations

## SafeMint Reentrancy Protection

### **Id**
check-safemint-reentrancy
### **Description**
Verify state updates before _safeMint calls
### **Pattern**
_safeMint.*\n.*minted\[|_safeMint.*\n.*claimed\[
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Update state BEFORE _safeMint to prevent reentrancy
### **Severity**
error
### **Autofix**


## Batch Mint Limit

### **Id**
check-batch-limit
### **Description**
Verify batch minting has a reasonable limit
### **Pattern**
function.*mint.*quantity.*\{(?!.*require.*quantity.*<=)
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Add batch size limit: require(quantity <= MAX_BATCH)
### **Severity**
warning
### **Autofix**


## Token Existence Check in tokenURI

### **Id**
check-token-exists
### **Description**
Verify tokenURI checks token exists
### **Pattern**
function tokenURI.*\{(?!.*_exists|.*_ownerOf|.*require)
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Add token existence check in tokenURI function
### **Severity**
warning
### **Autofix**


## ERC-2981 Royalty Interface

### **Id**
check-royalty-interface
### **Description**
NFT contracts should implement ERC-2981
### **Pattern**
ERC721|ERC1155
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
ERC2981|royaltyInfo
### **Message**
Consider implementing ERC-2981 for royalty support
### **Severity**
info
### **Autofix**


## IPFS Protocol URL

### **Id**
check-ipfs-protocol
### **Description**
Use ipfs:// protocol instead of gateway URLs
### **Pattern**
https://.*(ipfs\.io|pinata|cloudflare-ipfs)
### **File Glob**
**/*.json
### **Match**
present
### **Message**
Use ipfs:// protocol URL instead of gateway URL
### **Severity**
warning
### **Autofix**


## Metadata Required Fields

### **Id**
check-metadata-required-fields
### **Description**
Verify metadata has required fields
### **Pattern**
"name".*"image"
### **File Glob**
**/metadata/**/*.json
### **Match**
absent
### **Message**
Metadata must include 'name' and 'image' fields
### **Severity**
error
### **Autofix**


## Attributes Format

### **Id**
check-attributes-format
### **Description**
Verify attributes use correct OpenSea format
### **Pattern**
"attributes".*\[.*"trait_type".*"value"
### **File Glob**
**/metadata/**/*.json
### **Match**
absent_in_context
### **Context Pattern**
"attributes"
### **Message**
Attributes must use {trait_type, value} format
### **Severity**
warning
### **Autofix**


## Supply Limit Enforcement

### **Id**
check-supply-limit
### **Description**
Verify mint function checks max supply
### **Pattern**
function.*mint.*\{(?!.*MAX_SUPPLY|.*maxSupply|.*totalSupply)
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Add supply limit check in mint function
### **Severity**
error
### **Autofix**


## Metadata Freeze Capability

### **Id**
check-metadata-freeze
### **Description**
Contract should have ability to freeze metadata
### **Pattern**
setBaseURI|setTokenURI
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
frozen|immutable|lock
### **Message**
Consider adding metadata freeze functionality
### **Severity**
info
### **Autofix**


## Secure Withdraw Function

### **Id**
check-withdraw-function
### **Description**
Verify withdraw uses call instead of transfer
### **Pattern**
\.transfer\(|payable.*\.send\(
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Use .call{value:}('') instead of .transfer() for withdrawals
### **Severity**
warning
### **Autofix**
