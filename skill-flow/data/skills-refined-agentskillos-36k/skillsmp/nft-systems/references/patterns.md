# NFT Systems

## Patterns


---
  #### **Name**
Lazy Minting
  #### **Description**
Generate token IDs and metadata on-demand at mint time
  #### **When**
Large collections where pre-generating all metadata is expensive
  #### **Example**
    contract LazyMint is ERC721 {
        uint256 private _tokenIdCounter;
        string public baseURI;
    
        function mint(uint256 quantity) external payable {
            require(msg.value >= price * quantity, "Insufficient payment");
    
            for (uint256 i = 0; i < quantity; ) {
                uint256 tokenId = _tokenIdCounter;
                _safeMint(msg.sender, tokenId);
                unchecked {
                    ++_tokenIdCounter;
                    ++i;
                }
            }
        }
    
        function tokenURI(uint256 tokenId) public view override returns (string memory) {
            require(_exists(tokenId), "Token does not exist");
            return string(abi.encodePacked(baseURI, tokenId.toString(), ".json"));
        }
    }
    

---
  #### **Name**
Merkle Tree Allowlist
  #### **Description**
Gas-efficient allowlist verification using merkle proofs
  #### **When**
Private/early access mints with large allowlists
  #### **Example**
    contract AllowlistMint is ERC721 {
        bytes32 public merkleRoot;
        mapping(address => bool) public claimed;
    
        function allowlistMint(bytes32[] calldata proof) external {
            require(!claimed[msg.sender], "Already claimed");
            require(
                MerkleProof.verify(proof, merkleRoot, keccak256(abi.encodePacked(msg.sender))),
                "Invalid proof"
            );
    
            claimed[msg.sender] = true;
            _safeMint(msg.sender, _tokenIdCounter++);
        }
    
        function setMerkleRoot(bytes32 _root) external onlyOwner {
            merkleRoot = _root;
        }
    }
    

---
  #### **Name**
Commit-Reveal for Fair Mint
  #### **Description**
Prevent sniping by committing to randomness before reveal
  #### **When**
Rare traits or sequential mint with varying rarity
  #### **Example**
    contract CommitReveal is ERC721 {
        bytes32 public commitment;
        uint256 public revealBlock;
        bool public revealed;
    
        function setCommitment(bytes32 _commitment, uint256 _revealBlock) external onlyOwner {
            commitment = _commitment;
            revealBlock = _revealBlock;
        }
    
        function reveal(uint256 seed) external {
            require(block.number >= revealBlock, "Too early");
            require(keccak256(abi.encodePacked(seed)) == commitment, "Invalid seed");
    
            // Use seed + blockhash for final randomness
            uint256 randomness = uint256(keccak256(abi.encodePacked(
                seed,
                blockhash(revealBlock)
            )));
    
            _assignTraits(randomness);
            revealed = true;
        }
    }
    

---
  #### **Name**
ERC-2981 Royalty Standard
  #### **Description**
On-chain royalty information for marketplace compliance
  #### **When**
Need to specify royalty percentage and recipient
  #### **Example**
    contract RoyaltyNFT is ERC721, ERC2981 {
        constructor() ERC721("MyNFT", "NFT") {
            // 5% royalty to deployer
            _setDefaultRoyalty(msg.sender, 500);
        }
    
        function setTokenRoyalty(
            uint256 tokenId,
            address receiver,
            uint96 feeNumerator
        ) external onlyOwner {
            _setTokenRoyalty(tokenId, receiver, feeNumerator);
        }
    
        function supportsInterface(bytes4 interfaceId)
            public view override(ERC721, ERC2981)
            returns (bool)
        {
            return super.supportsInterface(interfaceId);
        }
    }
    

---
  #### **Name**
Soulbound Token (SBT)
  #### **Description**
Non-transferable NFTs for credentials, achievements, identity
  #### **When**
Tokens should be permanently bound to original recipient
  #### **Example**
    contract SoulboundToken is ERC721 {
        error Soulbound();
    
        function _beforeTokenTransfer(
            address from,
            address to,
            uint256 tokenId,
            uint256 batchSize
        ) internal override {
            // Allow minting (from == 0) and burning (to == 0)
            // Block all transfers
            if (from != address(0) && to != address(0)) {
                revert Soulbound();
            }
            super._beforeTokenTransfer(from, to, tokenId, batchSize);
        }
    
        // Override approve functions to prevent marketplace listings
        function approve(address, uint256) public pure override {
            revert Soulbound();
        }
    
        function setApprovalForAll(address, bool) public pure override {
            revert Soulbound();
        }
    }
    

---
  #### **Name**
On-Chain Metadata
  #### **Description**
Store metadata directly in contract for permanence
  #### **When**
Simple metadata, gas budget allows, no external dependencies
  #### **Example**
    contract OnChainNFT is ERC721 {
        struct TokenData {
            string name;
            string description;
            string image; // Base64 or data URI
        }
    
        mapping(uint256 => TokenData) private _tokenData;
    
        function tokenURI(uint256 tokenId) public view override returns (string memory) {
            TokenData memory data = _tokenData[tokenId];
    
            string memory json = Base64.encode(bytes(string(abi.encodePacked(
                '{"name":"', data.name,
                '","description":"', data.description,
                '","image":"', data.image, '"}'
            ))));
    
            return string(abi.encodePacked("data:application/json;base64,", json));
        }
    }
    

## Anti-Patterns


---
  #### **Name**
Centralized Metadata Hosting
  #### **Description**
Hosting metadata on a server you control
  #### **Why**
Server goes down, collection dies. Rug pull risk.
  #### **Instead**
    // Use decentralized storage
    // IPFS with pinning service (Pinata, nft.storage)
    // Arweave for permanent storage
    // On-chain for small data
    
    function setBaseURI(string calldata _uri) external onlyOwner {
        require(
            bytes(_uri).length > 7 &&
            (keccak256(abi.encodePacked(_uri[:7])) == keccak256("ipfs://") ||
             keccak256(abi.encodePacked(_uri[:5])) == keccak256("ar://")),
            "Must use decentralized storage"
        );
        baseURI = _uri;
    }
    

---
  #### **Name**
Sequential Token ID Reveals
  #### **Description**
Revealing metadata in token ID order
  #### **Why**
Snipers can see upcoming rare tokens and front-run mints
  #### **Instead**
    // Use random offset or batch reveals
    uint256 public revealOffset;
    
    function reveal(uint256 randomSeed) external onlyOwner {
        revealOffset = randomSeed % totalSupply;
    }
    
    function tokenURI(uint256 tokenId) public view returns (string memory) {
        uint256 metadataId = (tokenId + revealOffset) % totalSupply;
        return string(abi.encodePacked(baseURI, metadataId.toString(), ".json"));
    }
    

---
  #### **Name**
Unbounded Batch Mints
  #### **Description**
Allowing unlimited tokens per transaction
  #### **Why**
Gas limits cause failed transactions, poor UX
  #### **Instead**
    uint256 public constant MAX_BATCH_SIZE = 20;
    
    function mint(uint256 quantity) external payable {
        require(quantity <= MAX_BATCH_SIZE, "Batch too large");
        require(quantity > 0, "Quantity must be positive");
        // ...
    }
    

---
  #### **Name**
Missing Token Existence Checks
  #### **Description**
tokenURI doesn't verify token exists
  #### **Why**
Returns invalid URI for non-existent tokens, confuses indexers
  #### **Instead**
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "ERC721: URI query for nonexistent token");
        return string(abi.encodePacked(baseURI, tokenId.toString(), ".json"));
    }
    

---
  #### **Name**
Hardcoded Royalty Recipient
  #### **Description**
Royalty address can't be changed
  #### **Why**
Lost keys, company changes, multi-sig upgrades impossible
  #### **Instead**
    address public royaltyRecipient;
    
    function setRoyaltyRecipient(address _recipient) external onlyOwner {
        require(_recipient != address(0), "Invalid recipient");
        royaltyRecipient = _recipient;
    }
    

---
  #### **Name**
No Metadata Freeze Mechanism
  #### **Description**
Metadata can be changed forever
  #### **Why**
Collectors want assurance their NFT won't change
  #### **Instead**
    bool public metadataFrozen;
    
    function freezeMetadata() external onlyOwner {
        metadataFrozen = true;
        emit MetadataFrozen();
    }
    
    function setBaseURI(string calldata _uri) external onlyOwner {
        require(!metadataFrozen, "Metadata frozen");
        baseURI = _uri;
    }
    