---
name: Blockchain and Web3
description: This skill should be used when the user asks to "smart contract, deploy contract, DeFi protocol, NFT infrastructure, Web3, blockchain, Solidity, Foundry, Hardhat, IPFS, wallet integration", or needs help with Smart contracts, DeFi, NFT infrastructure, and blockchain deployment.
version: 1.0.0
---

# Blockchain and Web3

Comprehensive guidance for building, deploying, and operating blockchain applications, smart contracts, and Web3 infrastructure.

## Development Environment

### Foundry Setup

```bash
# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Create new project
forge init my-project
cd my-project

# Project structure
# ├── src/           # Smart contracts
# ├── test/          # Forge tests
# ├── script/        # Deployment scripts
# └── foundry.toml   # Configuration
```

### Hardhat Setup

```bash
# Initialize project
mkdir my-project && cd my-project
npm init -y
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox

# Create project
npx hardhat init
```

```javascript
// hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    hardhat: {
      forking: {
        url: process.env.MAINNET_RPC_URL,
        blockNumber: 18000000
      }
    },
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL,
      accounts: [process.env.PRIVATE_KEY],
      chainId: 11155111
    },
    mainnet: {
      url: process.env.MAINNET_RPC_URL,
      accounts: [process.env.PRIVATE_KEY],
      chainId: 1
    }
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY
  },
  gasReporter: {
    enabled: true,
    currency: "USD"
  }
};
```

## Smart Contract Development

### ERC-20 Token

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";

contract MyToken is ERC20, ERC20Burnable, ERC20Pausable, AccessControl, ERC20Permit {
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18; // 1 billion tokens

    constructor(address defaultAdmin)
        ERC20("MyToken", "MTK")
        ERC20Permit("MyToken")
    {
        _grantRole(DEFAULT_ADMIN_ROLE, defaultAdmin);
        _grantRole(PAUSER_ROLE, defaultAdmin);
        _grantRole(MINTER_ROLE, defaultAdmin);
    }

    function pause() public onlyRole(PAUSER_ROLE) {
        _pause();
    }

    function unpause() public onlyRole(PAUSER_ROLE) {
        _unpause();
    }

    function mint(address to, uint256 amount) public onlyRole(MINTER_ROLE) {
        require(totalSupply() + amount <= MAX_SUPPLY, "Exceeds max supply");
        _mint(to, amount);
    }

    // Required overrides
    function _update(address from, address to, uint256 value)
        internal
        override(ERC20, ERC20Pausable)
    {
        super._update(from, to, value);
    }
}
```

### ERC-721 NFT Collection

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract MyNFT is ERC721, ERC721Enumerable, ERC721URIStorage, ERC721Royalty, Ownable, ReentrancyGuard {
    uint256 private _nextTokenId;

    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MINT_PRICE = 0.08 ether;
    uint256 public constant MAX_PER_WALLET = 5;

    string private _baseTokenURI;
    bool public mintingEnabled;

    mapping(address => uint256) public mintedPerWallet;

    event Minted(address indexed to, uint256 indexed tokenId);

    constructor(
        address initialOwner,
        string memory baseURI,
        address royaltyReceiver
    )
        ERC721("MyNFT", "MNFT")
        Ownable(initialOwner)
    {
        _baseTokenURI = baseURI;
        _setDefaultRoyalty(royaltyReceiver, 500); // 5% royalty
    }

    function mint(uint256 quantity) external payable nonReentrant {
        require(mintingEnabled, "Minting not enabled");
        require(quantity > 0 && quantity <= MAX_PER_WALLET, "Invalid quantity");
        require(mintedPerWallet[msg.sender] + quantity <= MAX_PER_WALLET, "Exceeds wallet limit");
        require(_nextTokenId + quantity <= MAX_SUPPLY, "Exceeds max supply");
        require(msg.value >= MINT_PRICE * quantity, "Insufficient payment");

        mintedPerWallet[msg.sender] += quantity;

        for (uint256 i = 0; i < quantity; i++) {
            uint256 tokenId = _nextTokenId++;
            _safeMint(msg.sender, tokenId);
            emit Minted(msg.sender, tokenId);
        }
    }

    function setMintingEnabled(bool enabled) external onlyOwner {
        mintingEnabled = enabled;
    }

    function setBaseURI(string memory baseURI) external onlyOwner {
        _baseTokenURI = baseURI;
    }

    function withdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        (bool success, ) = payable(owner()).call{value: balance}("");
        require(success, "Withdrawal failed");
    }

    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    // Required overrides
    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721, ERC721Enumerable)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._increaseBalance(account, value);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable, ERC721URIStorage, ERC721Royalty)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

### Upgradeable Contract Pattern

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract MyContractV1 is Initializable, UUPSUpgradeable, OwnableUpgradeable {
    uint256 public value;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address initialOwner) public initializer {
        __Ownable_init(initialOwner);
        __UUPSUpgradeable_init();
    }

    function setValue(uint256 _value) external onlyOwner {
        value = _value;
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}

    function version() public pure virtual returns (string memory) {
        return "1.0.0";
    }
}

// V2 with new functionality
contract MyContractV2 is MyContractV1 {
    uint256 public newValue;

    function setNewValue(uint256 _newValue) external onlyOwner {
        newValue = _newValue;
    }

    function version() public pure override returns (string memory) {
        return "2.0.0";
    }
}
```

## Testing

### Foundry Tests

```solidity
// test/MyToken.t.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/MyToken.sol";

contract MyTokenTest is Test {
    MyToken public token;
    address public admin = address(1);
    address public user = address(2);

    function setUp() public {
        vm.startPrank(admin);
        token = new MyToken(admin);
        vm.stopPrank();
    }

    function test_InitialState() public view {
        assertEq(token.name(), "MyToken");
        assertEq(token.symbol(), "MTK");
        assertEq(token.totalSupply(), 0);
    }

    function test_Mint() public {
        vm.prank(admin);
        token.mint(user, 1000e18);
        assertEq(token.balanceOf(user), 1000e18);
    }

    function test_RevertWhen_NonMinterMints() public {
        vm.prank(user);
        vm.expectRevert();
        token.mint(user, 1000e18);
    }

    function testFuzz_Mint(uint256 amount) public {
        vm.assume(amount <= token.MAX_SUPPLY());

        vm.prank(admin);
        token.mint(user, amount);

        assertEq(token.balanceOf(user), amount);
    }

    function test_Transfer() public {
        vm.prank(admin);
        token.mint(user, 1000e18);

        vm.prank(user);
        token.transfer(admin, 500e18);

        assertEq(token.balanceOf(user), 500e18);
        assertEq(token.balanceOf(admin), 500e18);
    }
}
```

### Hardhat Tests

```javascript
// test/MyToken.test.js
const { expect } = require("chai");
const { ethers } = require("hardhat");
const { loadFixture } = require("@nomicfoundation/hardhat-toolbox/network-helpers");

describe("MyToken", function () {
    async function deployFixture() {
        const [owner, user1, user2] = await ethers.getSigners();

        const MyToken = await ethers.getContractFactory("MyToken");
        const token = await MyToken.deploy(owner.address);

        return { token, owner, user1, user2 };
    }

    describe("Deployment", function () {
        it("Should set the right name and symbol", async function () {
            const { token } = await loadFixture(deployFixture);

            expect(await token.name()).to.equal("MyToken");
            expect(await token.symbol()).to.equal("MTK");
        });

        it("Should grant admin role to deployer", async function () {
            const { token, owner } = await loadFixture(deployFixture);

            const adminRole = await token.DEFAULT_ADMIN_ROLE();
            expect(await token.hasRole(adminRole, owner.address)).to.be.true;
        });
    });

    describe("Minting", function () {
        it("Should mint tokens to address", async function () {
            const { token, user1 } = await loadFixture(deployFixture);

            await token.mint(user1.address, ethers.parseEther("1000"));
            expect(await token.balanceOf(user1.address)).to.equal(ethers.parseEther("1000"));
        });

        it("Should revert when non-minter tries to mint", async function () {
            const { token, user1, user2 } = await loadFixture(deployFixture);

            await expect(
                token.connect(user1).mint(user2.address, ethers.parseEther("1000"))
            ).to.be.reverted;
        });
    });
});
```

## Deployment

### Foundry Deployment Script

```solidity
// script/Deploy.s.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/MyToken.sol";

contract DeployScript is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        address admin = vm.envAddress("ADMIN_ADDRESS");

        vm.startBroadcast(deployerPrivateKey);

        MyToken token = new MyToken(admin);

        console.log("MyToken deployed to:", address(token));

        vm.stopBroadcast();
    }
}
```

```bash
# Deploy with Foundry
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url $SEPOLIA_RPC_URL \
  --broadcast \
  --verify \
  -vvvv
```

### Hardhat Deployment

```javascript
// scripts/deploy.js
const { ethers, upgrades } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying with account:", deployer.address);

    // Deploy regular contract
    const MyToken = await ethers.getContractFactory("MyToken");
    const token = await MyToken.deploy(deployer.address);
    await token.waitForDeployment();

    console.log("MyToken deployed to:", await token.getAddress());

    // Deploy upgradeable contract
    const MyContract = await ethers.getContractFactory("MyContractV1");
    const proxy = await upgrades.deployProxy(MyContract, [deployer.address], {
        initializer: "initialize",
        kind: "uups"
    });
    await proxy.waitForDeployment();

    console.log("Proxy deployed to:", await proxy.getAddress());

    // Verify on Etherscan
    if (network.name !== "hardhat") {
        console.log("Waiting for confirmations...");
        await token.deploymentTransaction().wait(5);

        await hre.run("verify:verify", {
            address: await token.getAddress(),
            constructorArguments: [deployer.address],
        });
    }
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
```

## Web3 Frontend Integration

### Wallet Connection (wagmi + viem)

```typescript
// lib/wagmi.ts
import { createConfig, http } from 'wagmi';
import { mainnet, sepolia } from 'wagmi/chains';
import { injected, walletConnect } from 'wagmi/connectors';

export const config = createConfig({
    chains: [mainnet, sepolia],
    connectors: [
        injected(),
        walletConnect({
            projectId: process.env.NEXT_PUBLIC_WC_PROJECT_ID!,
        }),
    ],
    transports: {
        [mainnet.id]: http(),
        [sepolia.id]: http(),
    },
});
```

```typescript
// components/ConnectWallet.tsx
'use client';

import { useAccount, useConnect, useDisconnect } from 'wagmi';

export function ConnectWallet() {
    const { address, isConnected } = useAccount();
    const { connect, connectors } = useConnect();
    const { disconnect } = useDisconnect();

    if (isConnected) {
        return (
            <div>
                <p>Connected: {address}</p>
                <button onClick={() => disconnect()}>Disconnect</button>
            </div>
        );
    }

    return (
        <div>
            {connectors.map((connector) => (
                <button
                    key={connector.id}
                    onClick={() => connect({ connector })}
                >
                    Connect {connector.name}
                </button>
            ))}
        </div>
    );
}
```

### Contract Interaction

```typescript
// hooks/useMyToken.ts
import { useReadContract, useWriteContract, useWaitForTransactionReceipt } from 'wagmi';
import { parseEther, formatEther } from 'viem';
import { myTokenAbi } from '@/lib/abis/myToken';

const CONTRACT_ADDRESS = '0x...';

export function useMyToken() {
    const { writeContract, data: hash, isPending } = useWriteContract();
    const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({ hash });

    // Read balance
    const { data: balance } = useReadContract({
        address: CONTRACT_ADDRESS,
        abi: myTokenAbi,
        functionName: 'balanceOf',
        args: [userAddress],
    });

    // Write: Transfer tokens
    const transfer = (to: string, amount: string) => {
        writeContract({
            address: CONTRACT_ADDRESS,
            abi: myTokenAbi,
            functionName: 'transfer',
            args: [to, parseEther(amount)],
        });
    };

    return {
        balance: balance ? formatEther(balance) : '0',
        transfer,
        isPending,
        isConfirming,
        isSuccess,
    };
}
```

## IPFS / Decentralized Storage

### Pinata Integration

```typescript
// lib/pinata.ts
import axios from 'axios';

const PINATA_API_KEY = process.env.PINATA_API_KEY;
const PINATA_SECRET_KEY = process.env.PINATA_SECRET_KEY;

export async function uploadToIPFS(file: File): Promise<string> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
        'https://api.pinata.cloud/pinning/pinFileToIPFS',
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
                pinata_api_key: PINATA_API_KEY,
                pinata_secret_api_key: PINATA_SECRET_KEY,
            },
        }
    );

    return `ipfs://${response.data.IpfsHash}`;
}

export async function uploadMetadataToIPFS(metadata: object): Promise<string> {
    const response = await axios.post(
        'https://api.pinata.cloud/pinning/pinJSONToIPFS',
        metadata,
        {
            headers: {
                'Content-Type': 'application/json',
                pinata_api_key: PINATA_API_KEY,
                pinata_secret_api_key: PINATA_SECRET_KEY,
            },
        }
    );

    return `ipfs://${response.data.IpfsHash}`;
}

// NFT metadata example
const nftMetadata = {
    name: "My NFT #1",
    description: "Description of my NFT",
    image: "ipfs://QmXxx...",
    attributes: [
        { trait_type: "Background", value: "Blue" },
        { trait_type: "Rarity", value: "Legendary" }
    ]
};
```

## Security Best Practices

### Common Vulnerabilities

| Vulnerability | Prevention |
|---------------|------------|
| Reentrancy | Use ReentrancyGuard, checks-effects-interactions |
| Integer Overflow | Solidity 0.8+ has built-in checks |
| Access Control | Use OpenZeppelin AccessControl |
| Front-running | Commit-reveal schemes, flashbots |
| Oracle Manipulation | Use Chainlink, TWAP |

### Security Checklist

```solidity
// Security patterns
contract SecureContract is ReentrancyGuard, Pausable, Ownable {
    // 1. Use checks-effects-interactions pattern
    function withdraw() external nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");

        // Effects before interactions
        balances[msg.sender] = 0;

        // External call last
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
    }

    // 2. Validate all inputs
    function setConfig(uint256 value) external onlyOwner {
        require(value > 0 && value <= MAX_VALUE, "Invalid value");
        config = value;
    }

    // 3. Use pull over push for payments
    mapping(address => uint256) public pendingWithdrawals;

    function claimPayment() external {
        uint256 amount = pendingWithdrawals[msg.sender];
        require(amount > 0, "Nothing to claim");

        pendingWithdrawals[msg.sender] = 0;

        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

## Monitoring & Operations

### Event Indexing (The Graph)

```graphql
# schema.graphql
type Transfer @entity {
  id: ID!
  from: Bytes!
  to: Bytes!
  value: BigInt!
  timestamp: BigInt!
  blockNumber: BigInt!
}

type Token @entity {
  id: ID!
  totalSupply: BigInt!
  holders: [Holder!]! @derivedFrom(field: "token")
}

type Holder @entity {
  id: ID!
  token: Token!
  balance: BigInt!
}
```

```typescript
// src/mapping.ts
import { Transfer as TransferEvent } from '../generated/MyToken/MyToken';
import { Transfer, Token, Holder } from '../generated/schema';

export function handleTransfer(event: TransferEvent): void {
    // Create Transfer entity
    let transfer = new Transfer(
        event.transaction.hash.toHex() + '-' + event.logIndex.toString()
    );
    transfer.from = event.params.from;
    transfer.to = event.params.to;
    transfer.value = event.params.value;
    transfer.timestamp = event.block.timestamp;
    transfer.blockNumber = event.block.number;
    transfer.save();

    // Update holder balances
    updateHolder(event.params.from, event.params.value.neg());
    updateHolder(event.params.to, event.params.value);
}

function updateHolder(address: Bytes, delta: BigInt): void {
    let holder = Holder.load(address.toHex());
    if (!holder) {
        holder = new Holder(address.toHex());
        holder.balance = BigInt.zero();
    }
    holder.balance = holder.balance.plus(delta);
    holder.save();
}
```

## CI/CD for Smart Contracts

```yaml
# .github/workflows/contracts.yml
name: Smart Contract CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Install Foundry
        uses: foundry-rs/foundry-toolchain@v1

      - name: Run tests
        run: forge test -vvv

      - name: Run coverage
        run: forge coverage --report lcov

      - name: Check gas snapshots
        run: forge snapshot --check

  slither:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Slither
        uses: crytic/slither-action@v0.3.0
        with:
          target: 'src/'
          slither-args: '--filter-paths "test|script"'

  deploy-testnet:
    needs: [test, slither]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Install Foundry
        uses: foundry-rs/foundry-toolchain@v1

      - name: Deploy to Sepolia
        run: |
          forge script script/Deploy.s.sol:DeployScript \
            --rpc-url ${{ secrets.SEPOLIA_RPC_URL }} \
            --broadcast \
            --verify
        env:
          PRIVATE_KEY: ${{ secrets.DEPLOYER_PRIVATE_KEY }}
          ETHERSCAN_API_KEY: ${{ secrets.ETHERSCAN_API_KEY }}
```
