# Web3 Gaming - Sharp Edges

## Death Spiral Tokenomics

### **Id**
death-spiral-tokenomics
### **Summary**
Inflationary rewards without sinks cause death spiral
### **Severity**
critical
### **Situation**
  Your game rewards players with tokens, but spending mechanisms
  are weak. Token supply inflates, price crashes, new players
  can't earn meaningful value, game dies.
  
### **Why**
  P2E games must balance earn vs burn. When earning exceeds
  burning, supply inflates. When price drops, players farm
  harder (more inflation) or leave. This is the death spiral.
  
### **Solution**
  # DESIGN STRONG TOKEN SINKS
  
  Token Sink Categories:
  ┌─────────────────────────────────────────────────────────┐
  │ REQUIRED SINKS (players must use)                       │
  │ - Entry fees for competitive modes                      │
  │ - Repair/maintenance costs for items                    │
  │ - Breeding/crafting costs                               │
  │ - Transaction fees (small %)                            │
  └─────────────────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────────────────┐
  │ OPTIONAL SINKS (players want to use)                    │
  │ - Cosmetic upgrades                                     │
  │ - Speed-ups and convenience                             │
  │ - Land/property purchases                               │
  │ - Guild creation and upgrades                           │
  └─────────────────────────────────────────────────────────┘
  
  Key Metrics to Monitor:
  - Daily Emission / Daily Burn ratio (target: < 1.0)
  - Token velocity (turnover rate)
  - Active sink usage percentage
  
  Emergency Levers:
  - Increase breeding costs
  - Add new sink activities
  - Reduce reward rates
  - Implement token buyback
  
### **Symptoms**
  - Token price in continuous decline
  - Earn rate exceeds burn rate
  - Player count dropping despite activity
### **Detection Pattern**


## Bot Farming

### **Id**
bot-farming
### **Summary**
Bots farm rewards faster than humans
### **Severity**
critical
### **Situation**
  Your game has predictable reward mechanics. Bots automate
  gameplay 24/7, extracting all value before humans can earn.
  
### **Why**
  If rewards are worth real money, someone will automate.
  Simple games with predictable rewards are trivially botted.
  Even complex games face multi-accounting.
  
### **Solution**
  # ANTI-BOT STRATEGIES
  
  // 1. Rate limiting per wallet
  mapping(address => uint256) public lastRewardTime;
  uint256 public constant COOLDOWN = 1 hours;
  
  function claimReward() external {
      require(
          block.timestamp >= lastRewardTime[msg.sender] + COOLDOWN,
          "Cooldown active"
      );
      lastRewardTime[msg.sender] = block.timestamp;
      // Process reward
  }
  
  // 2. Diminishing returns
  mapping(address => uint256) public dailyEarned;
  uint256[] public rewardTiers = [100, 80, 60, 40, 20, 10];
  
  function getRewardMultiplier(address player) public view returns (uint256) {
      uint256 earned = dailyEarned[player];
      uint256 tierIndex = earned / 100 ether;
      if (tierIndex >= rewardTiers.length) return 5; // Minimum
      return rewardTiers[tierIndex];
  }
  
  // 3. Server-side verification
  // - Validate game state transitions
  // - Check for impossible actions
  // - Behavioral analysis (click patterns)
  // - CAPTCHA for high-value claims
  // - Phone verification for accounts
  
  // 4. Social verification
  // - Guild requirements for earning
  // - Tournament participation
  // - Achievement gates
  
### **Symptoms**
  - Unusual 24/7 activity patterns
  - Perfect action sequences
  - Accounts with no social activity
### **Detection Pattern**


## Gas On Every Action

### **Id**
gas-on-every-action
### **Summary**
Requiring gas for every game action kills UX
### **Severity**
high
### **Situation**
  Every move, attack, or item use requires an on-chain transaction.
  Players spend more on gas than they earn, and gameplay is slow.
  
### **Why**
  Traditional games have instant actions. Blockchain transactions
  take seconds to minutes and cost money. Putting every action
  on-chain makes the game unplayable.
  
### **Solution**
  # HYBRID ON/OFF-CHAIN ARCHITECTURE
  
  Architecture Pattern:
  ┌─────────────────────────────────────────────────────────┐
  │                    GAME CLIENT                          │
  │                        │                                │
  │           ┌────────────┼────────────┐                   │
  │           ▼            ▼            ▼                   │
  │     [Gameplay]   [Inventory]   [Marketplace]            │
  │     Off-chain     Off-chain     On-chain                │
  │         │             │             │                   │
  │         └──────┬──────┘             │                   │
  │                ▼                    ▼                   │
  │         [Game Server]      [Smart Contracts]            │
  │                │                    │                   │
  │                └────────┬───────────┘                   │
  │                         ▼                               │
  │              [Session Settlement]                       │
  │              (batch on-chain once)                      │
  └─────────────────────────────────────────────────────────┘
  
  What goes ON-CHAIN:
  - Asset ownership (NFTs)
  - Token transfers
  - Marketplace trades
  - Session settlements (batched)
  - Tournament results
  
  What stays OFF-CHAIN:
  - Combat mechanics
  - Movement
  - Crafting process
  - Quest progress
  - Most gameplay
  
  // Session-based settlement
  function settleSession(
      address player,
      uint256 rewardAmount,
      bytes calldata serverSignature
  ) external {
      // Verify server signed this session result
      // Mint/transfer rewards
      // Update on-chain stats if needed
  }
  
### **Symptoms**
  - $5 gas cost for $0.01 reward
  - 30 second delays between actions
  - Players abandoning mid-game
### **Detection Pattern**


## Nft Metadata Centralized

### **Id**
nft-metadata-centralized
### **Summary**
Game NFT metadata on centralized servers
### **Severity**
high
### **Situation**
  Your NFT points to a centralized URL for metadata. The server
  goes down, company goes bankrupt, or someone changes the
  metadata - NFTs become worthless.
  
### **Why**
  Most NFT standards store tokenURI pointing to metadata.
  If that URL dies or changes, the NFT's "properties" disappear
  or can be silently modified.
  
### **Solution**
  # DECENTRALIZED METADATA
  
  // Option 1: On-chain metadata (expensive but permanent)
  contract OnChainItems is ERC721 {
      struct ItemData {
          string name;
          uint16 power;
          uint16 rarity;
      }
  
      mapping(uint256 => ItemData) public items;
  
      function tokenURI(uint256 tokenId) public view override returns (string) {
          ItemData memory item = items[tokenId];
          return string(abi.encodePacked(
              'data:application/json,{"name":"', item.name,
              '","attributes":[{"trait_type":"Power","value":', item.power,
              '}]}'
          ));
      }
  }
  
  // Option 2: IPFS with on-chain hash
  contract IPFSItems is ERC721 {
      mapping(uint256 => bytes32) public metadataHashes;
  
      function tokenURI(uint256 tokenId) public view returns (string) {
          bytes32 hash = metadataHashes[tokenId];
          return string(abi.encodePacked(
              "ipfs://",
              Base58.encode(hash)
          ));
      }
  }
  
  // Option 3: Arweave for permanent storage
  // Store on Arweave, reference by transaction ID
  
  Best Practice:
  - Store critical attributes on-chain
  - Store images on IPFS/Arweave
  - Pin IPFS content with multiple services
  - Document metadata standard publicly
  
### **Symptoms**
  - Broken NFT images
  - "Unknown" items in marketplaces
  - Metadata changes without warning
### **Detection Pattern**
tokenURI.*https://|metadata.*http://

## Rug Pull Upgrade

### **Id**
rug-pull-upgrade
### **Summary**
Upgradeable game contracts enable rug pulls
### **Severity**
critical
### **Situation**
  Your game uses upgradeable proxy contracts. The admin can
  change game logic, drain funds, or break the economy at will.
  
### **Why**
  Upgradeability is needed for bug fixes but creates trust
  issues. Players investing in NFTs must trust the admin won't
  rugpull via upgrade.
  
### **Solution**
  # TIMELOCKED UPGRADES WITH GOVERNANCE
  
  import "@openzeppelin/contracts/governance/TimelockController.sol";
  
  // 1. Use Timelock for all upgrades
  TimelockController public timelock;
  uint256 public constant UPGRADE_DELAY = 7 days;
  
  // 2. Announce upgrades publicly
  event UpgradeScheduled(address newImpl, uint256 executeTime);
  
  function scheduleUpgrade(address newImplementation) external onlyOwner {
      bytes memory data = abi.encodeWithSignature(
          "upgradeTo(address)",
          newImplementation
      );
  
      timelock.schedule(
          address(this),
          0,
          data,
          bytes32(0),
          bytes32(0),
          UPGRADE_DELAY
      );
  
      emit UpgradeScheduled(newImplementation, block.timestamp + UPGRADE_DELAY);
  }
  
  // 3. Immutable core rules
  // - Token supply caps CANNOT change
  // - NFT ownership CANNOT be revoked
  // - Earned rewards CANNOT be taken back
  
  // 4. DAO governance for major changes
  // - Community votes on upgrades
  // - Multisig cannot bypass DAO
  
### **Symptoms**
  - Sudden game rule changes
  - Surprise contract upgrades
  - Community trust erosion
### **Detection Pattern**
upgradeTo|upgradeToAndCall

## Cross Chain Item Duplication

### **Id**
cross-chain-item-duplication
### **Summary**
Item duplication via cross-chain exploits
### **Severity**
critical
### **Situation**
  Your game supports items on multiple chains. A user bridges
  an item, then exploits a race condition to use it on both
  chains simultaneously.
  
### **Why**
  Cross-chain bridges have finality delays. If the source chain
  doesn't lock/burn the item before the destination mints, or
  if the lock can be reversed, duplication occurs.
  
### **Solution**
  # SECURE CROSS-CHAIN ITEMS
  
  // Lock-and-Mint pattern with finality wait
  contract SourceChainLocker {
      mapping(uint256 => bool) public lockedItems;
      uint256 public constant FINALITY_BLOCKS = 64; // Chain-specific
  
      struct PendingBridge {
          uint256 tokenId;
          address owner;
          uint256 lockBlock;
          bool executed;
      }
  
      mapping(bytes32 => PendingBridge) public pendingBridges;
  
      function initiateBridge(uint256 tokenId, uint256 destChain) external {
          require(nft.ownerOf(tokenId) == msg.sender);
          nft.transferFrom(msg.sender, address(this), tokenId);
          lockedItems[tokenId] = true;
  
          bytes32 bridgeId = keccak256(abi.encode(tokenId, destChain, block.number));
          pendingBridges[bridgeId] = PendingBridge({
              tokenId: tokenId,
              owner: msg.sender,
              lockBlock: block.number,
              executed: false
          });
      }
  
      // Oracle/relayer confirms after FINALITY_BLOCKS
      function confirmBridge(bytes32 bridgeId) external onlyRelayer {
          PendingBridge storage pb = pendingBridges[bridgeId];
          require(block.number >= pb.lockBlock + FINALITY_BLOCKS);
          require(!pb.executed);
          pb.executed = true;
          // Signal to destination chain to mint
      }
  
      // Cancellation only if not confirmed
      function cancelBridge(bytes32 bridgeId) external {
          PendingBridge storage pb = pendingBridges[bridgeId];
          require(msg.sender == pb.owner);
          require(!pb.executed);
          require(block.number < pb.lockBlock + FINALITY_BLOCKS);
          lockedItems[pb.tokenId] = false;
          nft.transferFrom(address(this), msg.sender, pb.tokenId);
      }
  }
  
### **Symptoms**
  - Same item appearing on multiple chains
  - Item supply exceeding expected
  - Bridge arbitrage exploits
### **Detection Pattern**


## Replay Attack Rewards

### **Id**
replay-attack-rewards
### **Summary**
Reward signatures replayable across sessions
### **Severity**
high
### **Situation**
  Your server signs reward claims, but the signature can be
  replayed to claim the same reward multiple times.
  
### **Why**
  Without nonces or expiry, a valid signature is valid forever.
  Attackers save signatures and replay them repeatedly.
  
### **Solution**
  # INCLUDE NONCE AND EXPIRY
  
  // WRONG: Replayable signature
  bytes32 hash = keccak256(abi.encode(player, amount));
  
  // RIGHT: Include nonce and expiry
  mapping(address => uint256) public nonces;
  
  function claimReward(
      uint256 amount,
      uint256 nonce,
      uint256 expiry,
      bytes calldata signature
  ) external {
      require(nonce == nonces[msg.sender], "Invalid nonce");
      require(block.timestamp < expiry, "Expired");
  
      bytes32 hash = keccak256(abi.encode(
          msg.sender,
          amount,
          nonce,
          expiry,
          address(this), // Contract address
          block.chainid  // Chain ID
      ));
  
      require(verify(hash, signature), "Invalid signature");
      nonces[msg.sender]++;
  
      _distributeReward(msg.sender, amount);
  }
  
### **Symptoms**
  - Same reward claimed multiple times
  - Nonce gaps in claim history
  - Unexpected token minting
### **Detection Pattern**
keccak256.*msg\.sender.*amount(?!.*nonce)