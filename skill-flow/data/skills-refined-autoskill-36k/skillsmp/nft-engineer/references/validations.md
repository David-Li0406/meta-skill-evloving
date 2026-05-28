# Nft Engineer - Validations

## SafeMint Reentrancy Protection

### **Id**
check-safemint-reentrancy
### **Description**
Verify state updates happen BEFORE _safeMint calls to prevent reentrancy
### **Pattern**
_safeMint\s*\([^)]+\)[^}]*\n[^}]*(minted\[|claimed\[|numberMinted\[|hasMinted\[)
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
CRITICAL: State update after _safeMint - reentrancy vulnerability! Update state BEFORE minting.
### **Severity**
error
### **Autofix**


## Avoid transfer() for ETH

### **Id**
check-transfer-usage
### **Description**
Using .transfer() can fail for contracts and multi-sigs
### **Pattern**
\.transfer\s*\(|payable\([^)]+\)\.send\s*\(
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Use .call{value:}('') instead of .transfer() - transfer can fail for multi-sigs
### **Severity**
error
### **Autofix**


## Avoid Blockhash for Randomness

### **Id**
check-blockhash-randomness
### **Description**
Blockhash can be manipulated by miners
### **Pattern**
blockhash\s*\([^)]*\)\s*%|uint256\s*\(\s*blockhash
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Blockhash randomness can be manipulated - use commit-reveal or Chainlink VRF
### **Severity**
warning
### **Autofix**


## Batch Mint Limit Required

### **Id**
check-batch-limit
### **Description**
Mint functions should have a maximum quantity per transaction
### **Pattern**
function\s+(public)?mint\s*\([^)]*quantity[^)]*\)\s*[^{]*\{(?!.*require.*quantity\s*<=|.*if\s*\(quantity\s*>)
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Add batch size limit: require(quantity <= MAX_PER_TX) to prevent gas limit failures
### **Severity**
warning
### **Autofix**


## Supply Limit Check

### **Id**
check-supply-limit
### **Description**
Mint functions should verify max supply isn't exceeded
### **Pattern**
function.*mint.*\{(?!.*(MAX_SUPPLY|maxSupply|totalSupply\s*\(\s*\)\s*\+|_totalMinted))
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Add max supply check in mint function to prevent over-minting
### **Severity**
error
### **Autofix**


## Zero Quantity Check

### **Id**
check-zero-quantity
### **Description**
Mint functions should reject zero quantity mints
### **Pattern**
function.*mint.*quantity.*\{(?!.*require.*quantity.*>\s*0|.*if.*quantity.*==.*0)
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Add zero quantity check: require(quantity > 0)
### **Severity**
warning
### **Autofix**


## Token Existence Check in tokenURI

### **Id**
check-token-exists
### **Description**
tokenURI should verify the token has been minted
### **Pattern**
function\s+tokenURI\s*\([^)]*\)[^{]*\{(?!.*(_exists|_ownerOf|ownerOf|require))
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
tokenURI should check token exists before returning URI
### **Severity**
warning
### **Autofix**


## Metadata Freeze Capability

### **Id**
check-metadata-freeze
### **Description**
Contracts with setBaseURI should have a freeze mechanism
### **Pattern**
function\s+setBaseURI
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
frozen|metadataFrozen|freeze|immutable
### **Context Match**
absent
### **Message**
Consider adding metadata freeze functionality for collector trust
### **Severity**
info
### **Autofix**


## ERC-2981 Royalty Interface

### **Id**
check-royalty-interface
### **Description**
NFT contracts should implement ERC-2981 for royalty support
### **Pattern**
(ERC721A?|ERC1155)\s*(,|\{)
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
ERC2981|royaltyInfo|_setDefaultRoyalty
### **Context Match**
absent
### **Message**
Consider implementing ERC-2981 for marketplace royalty support
### **Severity**
info
### **Autofix**


## supportsInterface Override

### **Id**
check-supports-interface
### **Description**
Contracts implementing multiple interfaces should override supportsInterface
### **Pattern**
(ERC2981|ERC721A?Royalty)
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
function\s+supportsInterface
### **Context Match**
absent
### **Message**
Override supportsInterface to include all implemented interfaces
### **Severity**
warning
### **Autofix**


## IPFS Protocol URL

### **Id**
check-ipfs-protocol
### **Description**
Use ipfs:// protocol instead of gateway-specific URLs
### **Pattern**
https?://(gateway\.pinata\.cloud|ipfs\.io|cloudflare-ipfs|dweb\.link|nftstorage\.link)
### **File Glob**
**/*.json
### **Match**
present
### **Message**
Use ipfs:// protocol URL instead of gateway URL for resilience
### **Severity**
warning
### **Autofix**


## Metadata Name Field

### **Id**
check-metadata-name
### **Description**
NFT metadata must include a name field
### **Pattern**
"name"\s*:\s*"
### **File Glob**
**/metadata/**/*.json
### **Match**
absent
### **Message**
Metadata must include 'name' field
### **Severity**
error
### **Autofix**


## Metadata Image Field

### **Id**
check-metadata-image
### **Description**
NFT metadata must include an image field
### **Pattern**
"image"\s*:\s*"
### **File Glob**
**/metadata/**/*.json
### **Match**
absent
### **Message**
Metadata must include 'image' field
### **Severity**
error
### **Autofix**


## OpenSea Attributes Format

### **Id**
check-attributes-format
### **Description**
Attributes should use trait_type/value format
### **Pattern**
"attributes"\s*:\s*\[
### **File Glob**
**/metadata/**/*.json
### **Match**
present
### **Context Pattern**
"trait_type"\s*:\s*"[^"]+"\s*,\s*"value"
### **Context Match**
absent
### **Message**
Attributes must use OpenSea format: {trait_type, value}
### **Severity**
warning
### **Autofix**


## Withdraw Function Exists

### **Id**
check-withdraw-exists
### **Description**
Payable contracts should have a withdraw function
### **Pattern**
function\s+mint[^}]+payable
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
function\s+withdraw
### **Context Match**
absent
### **Message**
Contract receives ETH but has no withdraw function - funds may be stuck
### **Severity**
error
### **Autofix**


## Withdraw Access Control

### **Id**
check-withdraw-owner-only
### **Description**
Withdraw function should be owner-only
### **Pattern**
function\s+withdraw\s*\([^)]*\)\s*(external|public)(?!.*onlyOwner)
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Withdraw function should be restricted to owner
### **Severity**
error
### **Autofix**


## ERC-1155 Supply Tracking

### **Id**
check-erc1155-supply
### **Description**
ERC-1155 contracts should use ERC1155Supply for supply tracking
### **Pattern**
is\s+ERC1155[^S]|is\s+ERC1155\s*\{
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
ERC1155Supply|totalSupply\s*\(\s*uint256
### **Context Match**
absent
### **Message**
Use ERC1155Supply extension for supply tracking
### **Severity**
warning
### **Autofix**


## Merkle Proof Verification

### **Id**
check-merkle-verification
### **Description**
Merkle proofs should be properly verified
### **Pattern**
merkleRoot|merkle_root
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
MerkleProof\.verify|MerkleProofLib\.verify
### **Context Match**
absent
### **Message**
Ensure merkle proofs are verified using MerkleProof library
### **Severity**
error
### **Autofix**


## Allowlist Double-Claim Prevention

### **Id**
check-allowlist-claimed
### **Description**
Allowlist mints should track claimed status
### **Pattern**
function\s+(allowlist|whitelist|presale)Mint
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
(claimed\[|hasMinted\[|allowlistMinted\[)
### **Context Match**
absent
### **Message**
Track claimed status to prevent double-claiming allowlist
### **Severity**
error
### **Autofix**


## Mint Event Emission

### **Id**
check-mint-events
### **Description**
Minting should emit Transfer events (handled by ERC721)
### **Pattern**
function.*mint.*_mint\s*\(
### **File Glob**
**/*.sol
### **Match**
present
### **Message**
Ensure mint function uses _mint or _safeMint which emit Transfer events
### **Severity**
info
### **Autofix**


## Metadata Update Event

### **Id**
check-metadata-update-event
### **Description**
setBaseURI should emit BatchMetadataUpdate (EIP-4906)
### **Pattern**
function\s+setBaseURI
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
BatchMetadataUpdate|MetadataUpdate
### **Context Match**
absent
### **Message**
Consider emitting EIP-4906 BatchMetadataUpdate event for marketplace refresh
### **Severity**
info
### **Autofix**


## Reveal Randomness Source

### **Id**
check-reveal-safety
### **Description**
Reveal should use secure randomness
### **Pattern**
function\s+reveal
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
blockhash\s*\([^)]*block\.number[^)]*\)
### **Context Match**
present
### **Message**
Using current block's blockhash is predictable - use commit-reveal or Chainlink VRF
### **Severity**
warning
### **Autofix**


## Pre-Reveal URI Check

### **Id**
check-pre-reveal-uri
### **Description**
tokenURI should handle unrevealed state
### **Pattern**
function\s+tokenURI
### **File Glob**
**/*.sol
### **Match**
present
### **Context Pattern**
revealed|preReveal|unrevealed
### **Context Match**
absent_optional
### **Message**
Consider handling pre-reveal state in tokenURI if using reveal mechanics
### **Severity**
info
### **Autofix**
