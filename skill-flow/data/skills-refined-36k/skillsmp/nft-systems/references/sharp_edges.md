# Nft Systems - Sharp Edges

## Metadata Returns 404 During Indexing

### **Id**
metadata-404
### **Severity**
CRITICAL
### **Description**
Marketplaces cache metadata - 404s during indexing permanently break display
### **Symptoms**
  - NFTs show as "content not available"
  - Images don't load on marketplaces
  - Collection delisted or flagged
### **Detection Pattern**
tokenURI|baseURI|metadata
### **Solution**
  // 1. Upload ALL metadata before contract deployment
  // 2. Verify every tokenURI returns valid JSON
  // 3. Use IPFS directory uploads (CID stays same)
  
  // Verification script:
  async function verifyMetadata(baseURI, totalSupply) {
      for (let i = 0; i < totalSupply; i++) {
          const response = await fetch(`${baseURI}${i}.json`);
          if (!response.ok) {
              throw new Error(`Token ${i} metadata not found`);
          }
          const metadata = await response.json();
          // Verify required fields
          if (!metadata.name || !metadata.image) {
              throw new Error(`Token ${i} missing required fields`);
          }
      }
  }
  
### **References**
  - https://docs.opensea.io/docs/metadata-standards

## IPFS Gateway Single Point of Failure

### **Id**
ipfs-gateway-dependency
### **Severity**
CRITICAL
### **Description**
Using specific IPFS gateway URL instead of ipfs:// protocol
### **Symptoms**
  - Images break when gateway goes down
  - Pinata/Infura outages break collection
  - Different gateways show different content
### **Detection Pattern**
ipfs\.io|gateway\.pinata|cloudflare-ipfs
### **Solution**
  // Bad: Gateway-specific URL
  "image": "https://gateway.pinata.cloud/ipfs/Qm..."
  
  // Good: Protocol URL (marketplaces resolve)
  "image": "ipfs://Qm..."
  
  // Best: Multiple pinning services
  // - Pin to Pinata
  // - Pin to nft.storage
  // - Pin to Filebase
  // Use same CID, multiple providers for redundancy
  
### **References**
  - https://docs.ipfs.tech/concepts/ipfs-gateway/

## Reentrancy in Mint Function

### **Id**
reentrancy-mint
### **Severity**
CRITICAL
### **Description**
_safeMint callback allows reentrant minting
### **Symptoms**
  - Users mint more than allowed
  - Supply exceeded
  - Max per wallet bypassed
### **Detection Pattern**
_safeMint.*before.*state.*update
### **Solution**
  // Bad: State update after safeMint
  function mint(uint256 quantity) external {
      require(minted[msg.sender] + quantity <= maxPerWallet);
      for (uint i = 0; i < quantity; i++) {
          _safeMint(msg.sender, tokenIdCounter++);  // Callback here!
      }
      minted[msg.sender] += quantity;  // Too late!
  }
  
  // Good: Update state first
  function mint(uint256 quantity) external {
      require(minted[msg.sender] + quantity <= maxPerWallet);
      minted[msg.sender] += quantity;  // Update first
      for (uint i = 0; i < quantity; i++) {
          _safeMint(msg.sender, tokenIdCounter++);
      }
  }
  
  // Best: Use reentrancy guard
  function mint(uint256 quantity) external nonReentrant {
      // ...
  }
  
### **References**
  - https://blog.openzeppelin.com/reentrancy-after-istanbul/

## Royalties Easily Bypassed

### **Id**
royalty-bypass
### **Severity**
HIGH
### **Description**
ERC-2981 is not enforced, wrappers bypass royalties
### **Symptoms**
  - Royalties not paid on secondary sales
  - Revenue drops after launch hype
  - Wrapper contracts created
### **Detection Pattern**
royaltyInfo|ERC2981
### **Solution**
  // Royalties are NOT enforceable on-chain
  // Options:
  
  // 1. Operator filter (blocks known bypasses)
  import {DefaultOperatorFilterer} from "operator-filter-registry/DefaultOperatorFilterer.sol";
  
  contract NFT is ERC721, DefaultOperatorFilterer {
      function setApprovalForAll(address operator, bool approved)
          public override onlyAllowedOperatorApproval(operator)
      {
          super.setApprovalForAll(operator, approved);
      }
  }
  
  // 2. Accept reality: treat royalties as voluntary
  // 3. Build utility that requires holding (staking, access)
  
### **References**
  - https://github.com/ProjectOpenSea/operator-filter-registry

## Reveal Can Be Front-Run

### **Id**
reveal-frontrun
### **Severity**
HIGH
### **Description**
On-chain randomness or predictable reveal allows sniping
### **Symptoms**
  - Rares concentrated in few wallets
  - Sniper bots profit
  - Community loses trust
### **Detection Pattern**
reveal|blockhash|block\.timestamp
### **Solution**
  // Bad: Predictable randomness
  function reveal() external {
      offset = uint256(blockhash(block.number - 1)) % totalSupply;
  }
  
  // Good: Commit-reveal with future block
  function commitReveal(bytes32 commitment) external onlyOwner {
      require(revealBlock == 0, "Already committed");
      _commitment = commitment;
      revealBlock = block.number + 100;  // 100 blocks in future
  }
  
  function reveal(uint256 seed) external {
      require(block.number > revealBlock, "Too early");
      require(block.number < revealBlock + 256, "Blockhash expired");
      require(keccak256(abi.encodePacked(seed)) == _commitment, "Bad seed");
  
      offset = uint256(keccak256(abi.encodePacked(
          seed, blockhash(revealBlock)
      ))) % totalSupply;
  }
  
  // Best: Use Chainlink VRF
  
### **References**
  - https://docs.chain.link/vrf

## Large Batch Mints Fail

### **Id**
batch-gas-failure
### **Severity**
HIGH
### **Description**
No limit on batch size causes out-of-gas failures
### **Symptoms**
  - Transactions fail after paying gas
  - Users lose ETH on failed mints
  - Frustrated community
### **Detection Pattern**
mint.*quantity|for.*_safeMint
### **Solution**
  uint256 public constant MAX_BATCH = 20;
  
  function mint(uint256 quantity) external payable {
      require(quantity > 0 && quantity <= MAX_BATCH, "Invalid quantity");
      require(totalSupply() + quantity <= MAX_SUPPLY, "Exceeds supply");
  
      // Use ERC721A for gas-efficient batch mints
      _mint(msg.sender, quantity);
  }
  
  // Gas estimates per batch size (ERC721 vs ERC721A):
  // 1 token:  ~80k vs ~50k gas
  // 5 tokens: ~400k vs ~55k gas
  // 10 tokens: ~800k vs ~60k gas
  
### **References**
  - https://www.erc721a.org/

## Metadata Can Be Changed After Sale

### **Id**
metadata-mutability
### **Severity**
MEDIUM
### **Description**
No mechanism to freeze metadata permanently
### **Symptoms**
  - Rug pull concerns
  - Collectors don't trust collection
  - Legal liability for changes
### **Detection Pattern**
setBaseURI|setTokenURI
### **Solution**
  bool public metadataFrozen;
  
  event MetadataFrozen(string finalBaseURI);
  event BatchMetadataUpdate(uint256 fromTokenId, uint256 toTokenId);
  
  function freezeMetadata() external onlyOwner {
      require(!metadataFrozen, "Already frozen");
      metadataFrozen = true;
      emit MetadataFrozen(baseURI);
      // EIP-4906 refresh signal
      emit BatchMetadataUpdate(0, type(uint256).max);
  }
  
  function setBaseURI(string calldata _uri) external onlyOwner {
      require(!metadataFrozen, "Metadata is frozen");
      baseURI = _uri;
  }
  
### **References**
  - https://eips.ethereum.org/EIPS/eip-4906

## Metadata Doesn't Match OpenSea Schema

### **Id**
opensea-metadata-schema
### **Severity**
MEDIUM
### **Description**
Missing or incorrect metadata fields
### **Symptoms**
  - Traits don't display
  - Rarity tools can't parse
  - Collection looks broken
### **Detection Pattern**
attributes|trait_type|value
### **Solution**
  // Required OpenSea metadata format:
  {
      "name": "Token #1",
      "description": "Description here",
      "image": "ipfs://...",
      "attributes": [
          {
              "trait_type": "Background",
              "value": "Blue"
          },
          {
              "trait_type": "Power Level",
              "value": 95,
              "display_type": "number"
          },
          {
              "trait_type": "Birthday",
              "value": 1609459200,
              "display_type": "date"
          }
      ],
      "external_url": "https://yoursite.com/token/1",
      "animation_url": "ipfs://..." // For video/audio
  }
  
### **References**
  - https://docs.opensea.io/docs/metadata-standards

## ERC-1155 Missing Total Supply

### **Id**
erc1155-supply-tracking
### **Severity**
MEDIUM
### **Description**
No way to query total supply per token ID
### **Symptoms**
  - Can't verify scarcity
  - Marketplaces show "?" for supply
  - Rarity calculation impossible
### **Detection Pattern**
ERC1155(?!Supply)
### **Solution**
  // Use ERC1155Supply extension
  import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
  
  contract MyNFT is ERC1155Supply {
      function mint(address to, uint256 id, uint256 amount) external {
          _mint(to, id, amount, "");
      }
  
      // Now available:
      // totalSupply(id) - tokens minted for this ID
      // exists(id) - whether any tokens exist for ID
  }
  
### **References**
  - https://docs.openzeppelin.com/contracts/4.x/api/token/erc1155#ERC1155Supply

## Unverified Creator on Solana

### **Id**
solana-creator-verification
### **Severity**
MEDIUM
### **Description**
Creator not verified in Metaplex metadata
### **Symptoms**
  - Collection not indexed by Magic Eden
  - Can't prove authenticity
  - Royalties not enforced
### **Detection Pattern**
metaplex|candy.*machine|creators
### **Solution**
  // In Metaplex metadata, creators must be verified
  {
      "creators": [
          {
              "address": "YOUR_WALLET",
              "verified": true,  // Must be true!
              "share": 100
          }
      ]
  }
  
  // Verify using Metaplex SDK:
  const { nft } = await metaplex.nfts().create({
      // ...
      creators: [
          {
              address: metaplex.identity().publicKey,
              share: 100,
              // Automatically verified when using identity
          }
      ]
  });
  
### **References**
  - https://docs.metaplex.com/programs/token-metadata/accounts

## Allowlist Merkle Root Changed Mid-Mint

### **Id**
allowlist-timing-attack
### **Severity**
MEDIUM
### **Description**
Root can be changed while users are minting
### **Symptoms**
  - Valid proofs suddenly invalid
  - User transactions fail
  - Community outrage
### **Detection Pattern**
merkleRoot|setMerkleRoot
### **Solution**
  // Lock merkle root during mint window
  uint256 public mintStartTime;
  uint256 public mintEndTime;
  bool public merkleRootLocked;
  
  function setMerkleRoot(bytes32 _root) external onlyOwner {
      require(
          block.timestamp < mintStartTime || !merkleRootLocked,
          "Root locked during mint"
      );
      merkleRoot = _root;
  }
  
  function lockMerkleRoot() external onlyOwner {
      merkleRootLocked = true;
  }
  
### **References**
  - https://www.rareskills.io/post/merkle-tree-solidity