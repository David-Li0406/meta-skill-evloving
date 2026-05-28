# NFT Engineer

## Patterns


---
  #### **Name**
Gas-Optimized ERC721A Mint
  #### **Description**
Batch minting with minimal gas per token
  #### **When**
Collections over 5k tokens, batch mints expected
  #### **Example**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.20;
    
    import "erc721a/contracts/ERC721A.sol";
    import "@openzeppelin/contracts/access/Ownable.sol";
    
    contract OptimizedNFT is ERC721A, Ownable {
        uint256 public constant MAX_SUPPLY = 10000;
        uint256 public constant MAX_PER_TX = 10;
        uint256 public constant PRICE = 0.05 ether;
    
        bool public mintActive;
        string private _baseTokenURI;
    
        error MintNotActive();
        error ExceedsMaxPerTx();
        error ExceedsMaxSupply();
        error InsufficientPayment();
    
        constructor() ERC721A("Optimized NFT", "ONFT") Ownable(msg.sender) {}
    
        function mint(uint256 quantity) external payable {
            if (!mintActive) revert MintNotActive();
            if (quantity > MAX_PER_TX) revert ExceedsMaxPerTx();
            if (_totalMinted() + quantity > MAX_SUPPLY) revert ExceedsMaxSupply();
            if (msg.value < PRICE * quantity) revert InsufficientPayment();
    
            _mint(msg.sender, quantity);
        }
    
        function _baseURI() internal view override returns (string memory) {
            return _baseTokenURI;
        }
    
        function setBaseURI(string calldata uri) external onlyOwner {
            _baseTokenURI = uri;
        }
    
        function toggleMint() external onlyOwner {
            mintActive = !mintActive;
        }
    
        function withdraw() external onlyOwner {
            (bool success, ) = msg.sender.call{value: address(this).balance}("");
            require(success);
        }
    }
    

---
  #### **Name**
Merkle Allowlist with Allocation
  #### **Description**
Gas-efficient allowlist with per-address allocation limits
  #### **When**
Multiple mint tiers with different allocations
  #### **Example**
    import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
    
    contract AllowlistNFT is ERC721A, Ownable {
        bytes32 public merkleRoot;
        mapping(address => uint256) public allowlistMinted;
    
        error InvalidProof();
        error ExceedsAllocation(uint256 requested, uint256 remaining);
        error AllowlistNotActive();
    
        // Leaf: keccak256(abi.encodePacked(address, allocation))
        function allowlistMint(
            uint256 quantity,
            uint256 allocation,
            bytes32[] calldata proof
        ) external payable {
            if (!allowlistActive) revert AllowlistNotActive();
    
            bytes32 leaf = keccak256(abi.encodePacked(msg.sender, allocation));
            if (!MerkleProof.verify(proof, merkleRoot, leaf)) revert InvalidProof();
    
            uint256 alreadyMinted = allowlistMinted[msg.sender];
            if (alreadyMinted + quantity > allocation) {
                revert ExceedsAllocation(quantity, allocation - alreadyMinted);
            }
    
            // State update BEFORE mint (reentrancy protection)
            allowlistMinted[msg.sender] = alreadyMinted + quantity;
            _mint(msg.sender, quantity);
        }
    
        function setMerkleRoot(bytes32 _root) external onlyOwner {
            merkleRoot = _root;
        }
    }
    
    // Generate merkle tree off-chain:
    // const { MerkleTree } = require('merkletreejs');
    // const leaves = addresses.map(([addr, allocation]) =>
    //   ethers.solidityPackedKeccak256(['address', 'uint256'], [addr, allocation])
    // );
    // const tree = new MerkleTree(leaves, keccak256, { sortPairs: true });
    

---
  #### **Name**
Commit-Reveal Fair Launch
  #### **Description**
Prevent front-running of reveal by committing to randomness ahead of time
  #### **When**
Collection has varying rarity and fairness is critical
  #### **Example**
    contract FairRevealNFT is ERC721A, Ownable {
        bytes32 public commitment;
        uint256 public revealBlockNumber;
        uint256 public randomOffset;
        bool public revealed;
    
        string public preRevealURI;
        string public revealedBaseURI;
    
        error RevealNotReady();
        error RevealExpired();
        error InvalidRevealSeed();
        error AlreadyRevealed();
    
        // Step 1: Owner commits hash of secret seed + future block
        function commitReveal(bytes32 _commitment, uint256 _revealBlock) external onlyOwner {
            require(_revealBlock > block.number + 10, "Too soon");
            commitment = _commitment;
            revealBlockNumber = _revealBlock;
        }
    
        // Step 2: After revealBlockNumber, reveal with seed
        function reveal(uint256 seed) external onlyOwner {
            if (revealed) revert AlreadyRevealed();
            if (block.number <= revealBlockNumber) revert RevealNotReady();
            if (block.number > revealBlockNumber + 256) revert RevealExpired();
    
            // Verify seed matches commitment
            if (keccak256(abi.encodePacked(seed)) != commitment) {
                revert InvalidRevealSeed();
            }
    
            // Combine seed with blockhash for final randomness
            randomOffset = uint256(keccak256(abi.encodePacked(
                seed,
                blockhash(revealBlockNumber)
            ))) % _totalMinted();
    
            revealed = true;
        }
    
        function tokenURI(uint256 tokenId) public view override returns (string memory) {
            if (!_exists(tokenId)) revert URIQueryForNonexistentToken();
    
            if (!revealed) {
                return preRevealURI;
            }
    
            // Map tokenId to metadata with offset
            uint256 metadataId = (tokenId + randomOffset) % _totalMinted();
            return string(abi.encodePacked(revealedBaseURI, _toString(metadataId), ".json"));
        }
    }
    

---
  #### **Name**
Dutch Auction Mint
  #### **Description**
Price decreases over time until sellout or floor reached
  #### **When**
Price discovery needed, high demand expected
  #### **Example**
    contract DutchAuctionNFT is ERC721A, Ownable {
        uint256 public constant START_PRICE = 1 ether;
        uint256 public constant END_PRICE = 0.1 ether;
        uint256 public constant PRICE_DROP = 0.1 ether;
        uint256 public constant DROP_INTERVAL = 10 minutes;
    
        uint256 public auctionStartTime;
    
        error AuctionNotStarted();
        error AuctionEnded();
    
        function currentPrice() public view returns (uint256) {
            if (auctionStartTime == 0) return START_PRICE;
    
            uint256 elapsed = block.timestamp - auctionStartTime;
            uint256 drops = elapsed / DROP_INTERVAL;
            uint256 totalDrop = drops * PRICE_DROP;
    
            if (totalDrop >= START_PRICE - END_PRICE) {
                return END_PRICE;
            }
    
            return START_PRICE - totalDrop;
        }
    
        function mint(uint256 quantity) external payable {
            if (auctionStartTime == 0) revert AuctionNotStarted();
    
            uint256 price = currentPrice();
            if (msg.value < price * quantity) revert InsufficientPayment();
    
            _mint(msg.sender, quantity);
    
            // Refund excess payment
            uint256 excess = msg.value - (price * quantity);
            if (excess > 0) {
                (bool success, ) = msg.sender.call{value: excess}("");
                require(success);
            }
        }
    
        function startAuction() external onlyOwner {
            auctionStartTime = block.timestamp;
        }
    }
    

---
  #### **Name**
On-Chain SVG Generation
  #### **Description**
Fully on-chain metadata with dynamic SVG rendering
  #### **When**
Simple generative art, maximum decentralization required
  #### **Example**
    import "@openzeppelin/contracts/utils/Base64.sol";
    import "@openzeppelin/contracts/utils/Strings.sol";
    
    contract OnChainNFT is ERC721A, Ownable {
        using Strings for uint256;
    
        struct Traits {
            uint8 background;
            uint8 pattern;
            uint8 color;
        }
    
        mapping(uint256 => Traits) public tokenTraits;
    
        string[5] private backgrounds = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"];
        string[4] private patterns = ["circle", "square", "triangle", "hexagon"];
    
        function generateSVG(uint256 tokenId) internal view returns (string memory) {
            Traits memory t = tokenTraits[tokenId];
    
            string memory svg = string(abi.encodePacked(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">',
                '<rect width="100" height="100" fill="', backgrounds[t.background], '"/>',
                _renderPattern(t.pattern, t.color),
                '</svg>'
            ));
    
            return svg;
        }
    
        function tokenURI(uint256 tokenId) public view override returns (string memory) {
            if (!_exists(tokenId)) revert URIQueryForNonexistentToken();
    
            Traits memory t = tokenTraits[tokenId];
            string memory svg = generateSVG(tokenId);
    
            string memory json = string(abi.encodePacked(
                '{"name":"OnChain #', tokenId.toString(),
                '","description":"Fully on-chain generative NFT",',
                '"image":"data:image/svg+xml;base64,', Base64.encode(bytes(svg)), '",',
                '"attributes":[',
                '{"trait_type":"Background","value":"', backgrounds[t.background], '"},',
                '{"trait_type":"Pattern","value":"', patterns[t.pattern], '"}',
                ']}'
            ));
    
            return string(abi.encodePacked(
                "data:application/json;base64,",
                Base64.encode(bytes(json))
            ));
        }
    
        function _mintWithTraits(address to, uint256 quantity) internal {
            uint256 startId = _nextTokenId();
            _mint(to, quantity);
    
            // Generate pseudo-random traits
            for (uint256 i = 0; i < quantity; i++) {
                uint256 tokenId = startId + i;
                uint256 seed = uint256(keccak256(abi.encodePacked(
                    tokenId, block.timestamp, block.prevrandao, msg.sender
                )));
    
                tokenTraits[tokenId] = Traits({
                    background: uint8(seed % 5),
                    pattern: uint8((seed >> 8) % 4),
                    color: uint8((seed >> 16) % 6)
                });
            }
        }
    }
    

---
  #### **Name**
Royalty with Operator Filter
  #### **Description**
ERC-2981 royalties with OpenSea operator filter for enforcement
  #### **When**
Royalty revenue is critical to project economics
  #### **Example**
    import "@openzeppelin/contracts/token/common/ERC2981.sol";
    import "operator-filter-registry/src/DefaultOperatorFilterer.sol";
    
    contract RoyaltyNFT is ERC721A, ERC2981, DefaultOperatorFilterer, Ownable {
        constructor() ERC721A("Royalty NFT", "RNFT") Ownable(msg.sender) {
            // 5% royalty (500 basis points)
            _setDefaultRoyalty(msg.sender, 500);
        }
    
        // Override transfer functions to use operator filter
        function setApprovalForAll(
            address operator,
            bool approved
        ) public override onlyAllowedOperatorApproval(operator) {
            super.setApprovalForAll(operator, approved);
        }
    
        function approve(
            address operator,
            uint256 tokenId
        ) public payable override onlyAllowedOperatorApproval(operator) {
            super.approve(operator, tokenId);
        }
    
        function transferFrom(
            address from,
            address to,
            uint256 tokenId
        ) public payable override onlyAllowedOperator(from) {
            super.transferFrom(from, to, tokenId);
        }
    
        function safeTransferFrom(
            address from,
            address to,
            uint256 tokenId
        ) public payable override onlyAllowedOperator(from) {
            super.safeTransferFrom(from, to, tokenId);
        }
    
        function safeTransferFrom(
            address from,
            address to,
            uint256 tokenId,
            bytes memory data
        ) public payable override onlyAllowedOperator(from) {
            super.safeTransferFrom(from, to, tokenId, data);
        }
    
        // Update royalty recipient (in case of wallet change)
        function setRoyaltyInfo(address receiver, uint96 feeNumerator) external onlyOwner {
            _setDefaultRoyalty(receiver, feeNumerator);
        }
    
        function supportsInterface(bytes4 interfaceId)
            public view override(ERC721A, ERC2981)
            returns (bool)
        {
            return ERC721A.supportsInterface(interfaceId) ||
                   ERC2981.supportsInterface(interfaceId);
        }
    }
    

---
  #### **Name**
Soulbound Token (Non-Transferable)
  #### **Description**
Tokens that cannot be transferred after minting
  #### **When**
Credentials, achievements, identity tokens, POAPs
  #### **Example**
    contract SoulboundNFT is ERC721A, Ownable {
        error Soulbound();
    
        constructor() ERC721A("Soulbound", "SOUL") Ownable(msg.sender) {}
    
        // Block all transfers (allow mint and burn)
        function _beforeTokenTransfers(
            address from,
            address to,
            uint256 startTokenId,
            uint256 quantity
        ) internal override {
            // Allow minting (from == 0) and burning (to == 0)
            if (from != address(0) && to != address(0)) {
                revert Soulbound();
            }
            super._beforeTokenTransfers(from, to, startTokenId, quantity);
        }
    
        // Block approvals to prevent marketplace listings
        function approve(address, uint256) public payable override {
            revert Soulbound();
        }
    
        function setApprovalForAll(address, bool) public override {
            revert Soulbound();
        }
    
        // Admin mint function
        function adminMint(address to, uint256 quantity) external onlyOwner {
            _mint(to, quantity);
        }
    
        // Allow holders to burn their own tokens
        function burn(uint256 tokenId) external {
            if (ownerOf(tokenId) != msg.sender) revert NotOwner();
            _burn(tokenId);
        }
    }
    

---
  #### **Name**
Multi-Phase Mint with Price Tiers
  #### **Description**
Multiple mint phases with different prices and access controls
  #### **When**
Complex launches with OG, allowlist, and public phases
  #### **Example**
    contract MultiPhaseMint is ERC721A, Ownable {
        enum Phase { CLOSED, OG, ALLOWLIST, PUBLIC }
    
        Phase public currentPhase;
        bytes32 public ogMerkleRoot;
        bytes32 public allowlistMerkleRoot;
    
        uint256 public constant OG_PRICE = 0.03 ether;
        uint256 public constant ALLOWLIST_PRICE = 0.05 ether;
        uint256 public constant PUBLIC_PRICE = 0.08 ether;
    
        uint256 public constant OG_MAX = 3;
        uint256 public constant ALLOWLIST_MAX = 2;
        uint256 public constant PUBLIC_MAX = 5;
    
        mapping(address => uint256) public ogMinted;
        mapping(address => uint256) public allowlistMinted;
        mapping(address => uint256) public publicMinted;
    
        error WrongPhase();
        error InvalidProof();
        error ExceedsPhaseLimit();
    
        function ogMint(uint256 quantity, bytes32[] calldata proof) external payable {
            if (currentPhase != Phase.OG) revert WrongPhase();
            if (ogMinted[msg.sender] + quantity > OG_MAX) revert ExceedsPhaseLimit();
            if (msg.value < OG_PRICE * quantity) revert InsufficientPayment();
    
            bytes32 leaf = keccak256(abi.encodePacked(msg.sender));
            if (!MerkleProof.verify(proof, ogMerkleRoot, leaf)) revert InvalidProof();
    
            ogMinted[msg.sender] += quantity;
            _mint(msg.sender, quantity);
        }
    
        function allowlistMint(uint256 quantity, bytes32[] calldata proof) external payable {
            if (currentPhase != Phase.ALLOWLIST) revert WrongPhase();
            if (allowlistMinted[msg.sender] + quantity > ALLOWLIST_MAX) revert ExceedsPhaseLimit();
            if (msg.value < ALLOWLIST_PRICE * quantity) revert InsufficientPayment();
    
            bytes32 leaf = keccak256(abi.encodePacked(msg.sender));
            if (!MerkleProof.verify(proof, allowlistMerkleRoot, leaf)) revert InvalidProof();
    
            allowlistMinted[msg.sender] += quantity;
            _mint(msg.sender, quantity);
        }
    
        function publicMint(uint256 quantity) external payable {
            if (currentPhase != Phase.PUBLIC) revert WrongPhase();
            if (publicMinted[msg.sender] + quantity > PUBLIC_MAX) revert ExceedsPhaseLimit();
            if (msg.value < PUBLIC_PRICE * quantity) revert InsufficientPayment();
    
            publicMinted[msg.sender] += quantity;
            _mint(msg.sender, quantity);
        }
    
        function setPhase(Phase _phase) external onlyOwner {
            currentPhase = _phase;
        }
    }
    

## Anti-Patterns


---
  #### **Name**
State Update After SafeMint
  #### **Description**
Updating state variables after _safeMint allows reentrancy
  #### **Why**
_safeMint calls onERC721Received on recipient, allowing callback to re-enter mint
  #### **Severity**
critical
  #### **Instead**
    // BAD - state update after external call
    function mint(uint256 quantity) external {
        for (uint i = 0; i < quantity; i++) {
            _safeMint(msg.sender, tokenIdCounter++);
        }
        minted[msg.sender] += quantity;  // TOO LATE - already re-entered
    }
    
    // GOOD - state update before external call
    function mint(uint256 quantity) external {
        minted[msg.sender] += quantity;  // Update FIRST
        _mint(msg.sender, quantity);     // Then mint
    }
    
    // BEST - use nonReentrant modifier
    function mint(uint256 quantity) external nonReentrant {
        minted[msg.sender] += quantity;
        _safeMint(msg.sender, quantity);
    }
    

---
  #### **Name**
Unbounded Loop Mints
  #### **Description**
No limit on quantity parameter in mint functions
  #### **Why**
Large quantities hit block gas limit, users lose gas on failed txs
  #### **Severity**
high
  #### **Instead**
    // BAD - unbounded quantity
    function mint(uint256 quantity) external payable {
        _mint(msg.sender, quantity);  // quantity = 1000 will fail
    }
    
    // GOOD - explicit bounds
    uint256 public constant MAX_PER_TX = 10;
    
    function mint(uint256 quantity) external payable {
        require(quantity > 0 && quantity <= MAX_PER_TX, "Invalid quantity");
        _mint(msg.sender, quantity);
    }
    

---
  #### **Name**
Using transfer() for ETH
  #### **Description**
Using .transfer() or .send() for ETH withdrawals
  #### **Why**
2300 gas stipend fails for contracts, multi-sigs, and some EOAs
  #### **Severity**
high
  #### **Instead**
    // BAD - transfer has 2300 gas stipend
    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
    
    // GOOD - call with success check
    function withdraw() external onlyOwner {
        (bool success, ) = owner().call{value: address(this).balance}("");
        require(success, "Withdraw failed");
    }
    

---
  #### **Name**
Blockhash for Randomness
  #### **Description**
Using blockhash or block.timestamp for random number generation
  #### **Why**
Miners can manipulate, reveal can be front-run
  #### **Severity**
high
  #### **Instead**
    // BAD - predictable randomness
    function reveal() external onlyOwner {
        offset = uint256(blockhash(block.number - 1)) % totalSupply;
    }
    
    // GOOD - commit-reveal scheme
    // 1. Commit hash of seed before mint
    // 2. Reveal seed after mint, use future blockhash
    // See commit-reveal pattern above
    
    // BEST - Chainlink VRF
    // https://docs.chain.link/vrf/v2/introduction
    

---
  #### **Name**
Centralized Metadata Hosting
  #### **Description**
Hosting metadata on AWS, Vercel, or other centralized servers
  #### **Why**
Server goes down = collection dies. Rug pull risk.
  #### **Severity**
high
  #### **Instead**
    // BAD - centralized URL
    baseURI = "https://api.myproject.com/metadata/";
    
    // GOOD - IPFS with protocol URL
    baseURI = "ipfs://QmXxx.../";
    
    // BEST - Arweave for permanence
    baseURI = "ar://xxxx/";
    
    // Validate decentralized storage in setBaseURI
    function setBaseURI(string calldata _uri) external onlyOwner {
        require(
            bytes(_uri).length > 7 &&
            (keccak256(bytes(_uri[0:7])) == keccak256("ipfs://") ||
             keccak256(bytes(_uri[0:5])) == keccak256("ar://")),
            "Use decentralized storage"
        );
        baseURI = _uri;
    }
    

---
  #### **Name**
Missing Token Existence Check
  #### **Description**
tokenURI doesn't verify the token has been minted
  #### **Why**
Returns invalid URIs for unminted tokens, confuses indexers
  #### **Severity**
medium
  #### **Instead**
    // BAD - no existence check
    function tokenURI(uint256 tokenId) public view returns (string memory) {
        return string(abi.encodePacked(baseURI, tokenId.toString(), ".json"));
    }
    
    // GOOD - explicit check
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        if (!_exists(tokenId)) revert URIQueryForNonexistentToken();
        return string(abi.encodePacked(baseURI, _toString(tokenId), ".json"));
    }
    

---
  #### **Name**
No Metadata Freeze Mechanism
  #### **Description**
baseURI can be changed forever with no lockdown option
  #### **Why**
Collectors can't trust that their NFT won't change
  #### **Severity**
medium
  #### **Instead**
    // BAD - always mutable
    function setBaseURI(string calldata _uri) external onlyOwner {
        baseURI = _uri;
    }
    
    // GOOD - freezable
    bool public metadataFrozen;
    
    function freezeMetadata() external onlyOwner {
        metadataFrozen = true;
        emit PermanentURI(baseURI);  // OpenSea listens for this
    }
    
    function setBaseURI(string calldata _uri) external onlyOwner {
        require(!metadataFrozen, "Metadata is frozen");
        baseURI = _uri;
        emit BatchMetadataUpdate(0, type(uint256).max);  // EIP-4906
    }
    

---
  #### **Name**
Hardcoded Royalty Recipient
  #### **Description**
Royalty address set in constructor with no update function
  #### **Why**
Can't change if wallet compromised or project transitions
  #### **Severity**
medium
  #### **Instead**
    // BAD - hardcoded
    constructor() {
        _setDefaultRoyalty(0x1234..., 500);
    }
    
    // GOOD - updateable
    function setRoyaltyInfo(address receiver, uint96 feeNumerator) external onlyOwner {
        require(receiver != address(0), "Invalid receiver");
        _setDefaultRoyalty(receiver, feeNumerator);
    }
    

---
  #### **Name**
Sequential Reveal
  #### **Description**
Revealing metadata in token ID order
  #### **Why**
Snipers can predict upcoming rares from existing reveals
  #### **Severity**
medium
  #### **Instead**
    // BAD - sequential mapping
    function tokenURI(uint256 tokenId) public view returns (string memory) {
        return string(abi.encodePacked(baseURI, tokenId.toString(), ".json"));
    }
    
    // GOOD - offset mapping
    uint256 public revealOffset;
    
    function tokenURI(uint256 tokenId) public view returns (string memory) {
        if (!revealed) return preRevealURI;
        uint256 metadataId = (tokenId + revealOffset) % totalSupply;
        return string(abi.encodePacked(baseURI, metadataId.toString(), ".json"));
    }
    

---
  #### **Name**
ERC-1155 Without Supply Tracking
  #### **Description**
Using ERC-1155 without ERC1155Supply extension
  #### **Why**
Can't verify scarcity, marketplaces show unknown supply
  #### **Severity**
medium
  #### **Instead**
    // BAD - base ERC1155 only
    contract MyNFT is ERC1155 { }
    
    // GOOD - with supply tracking
    import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
    
    contract MyNFT is ERC1155Supply {
        // Now have totalSupply(id) and exists(id)
    }
    