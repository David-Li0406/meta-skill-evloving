# Account Abstraction Engineer

## Patterns


---
  #### **Id**
erc4337-account
  #### **Name**
ERC-4337 Smart Account
  #### **Description**
    Standard smart contract wallet compatible with ERC-4337
    bundler infrastructure
    
  #### **When To Use**
    - Building smart wallet product
    - Gasless user experience
    - Advanced wallet features
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    import "@account-abstraction/contracts/core/BaseAccount.sol";
    import "@account-abstraction/contracts/samples/callback/TokenCallbackHandler.sol";
    
    contract SmartAccount is BaseAccount, TokenCallbackHandler {
        address public owner;
        IEntryPoint private immutable _entryPoint;
    
        constructor(IEntryPoint anEntryPoint, address _owner) {
            _entryPoint = anEntryPoint;
            owner = _owner;
        }
    
        function entryPoint() public view override returns (IEntryPoint) {
            return _entryPoint;
        }
    
        function _validateSignature(
            UserOperation calldata userOp,
            bytes32 userOpHash
        ) internal view override returns (uint256 validationData) {
            bytes32 hash = MessageHashUtils.toEthSignedMessageHash(userOpHash);
            address signer = ECDSA.recover(hash, userOp.signature);
    
            if (signer != owner) {
                return SIG_VALIDATION_FAILED;
            }
            return 0; // Valid
        }
    
        function execute(
            address dest,
            uint256 value,
            bytes calldata data
        ) external {
            _requireFromEntryPoint();
            (bool success, bytes memory result) = dest.call{value: value}(data);
            if (!success) {
                assembly {
                    revert(add(result, 32), mload(result))
                }
            }
        }
    
        function executeBatch(
            address[] calldata dests,
            uint256[] calldata values,
            bytes[] calldata datas
        ) external {
            _requireFromEntryPoint();
            require(dests.length == values.length && values.length == datas.length);
            for (uint i = 0; i < dests.length; i++) {
                (bool success,) = dests[i].call{value: values[i]}(datas[i]);
                require(success);
            }
        }
    
        receive() external payable {}
    }
    
    User Operation Flow:
    1. User creates UserOperation (calldata, gas limits, signature)
    2. Sends to Bundler (via RPC or API)
    3. Bundler validates and bundles with others
    4. Bundler calls EntryPoint.handleOps()
    5. EntryPoint validates and executes each UserOp
    6. Gas paid from account or Paymaster
    
  #### **Security Notes**
    - Validate all signatures carefully
    - Handle replay protection (nonces)
    - Consider upgrade mechanisms

---
  #### **Id**
paymaster
  #### **Name**
Gas Sponsorship Paymaster
  #### **Description**
    Contract that pays gas fees on behalf of users for
    gasless transaction experience
    
  #### **When To Use**
    - Onboarding users without ETH
    - Sponsored transactions
    - Subscription-based gas
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    import "@account-abstraction/contracts/core/BasePaymaster.sol";
    
    contract SponsorPaymaster is BasePaymaster {
        mapping(address => bool) public sponsoredAccounts;
        uint256 public maxGasCost = 0.01 ether;
    
        constructor(IEntryPoint _entryPoint) BasePaymaster(_entryPoint) {}
    
        function addSponsoredAccount(address account) external onlyOwner {
            sponsoredAccounts[account] = true;
        }
    
        function _validatePaymasterUserOp(
            UserOperation calldata userOp,
            bytes32 /*userOpHash*/,
            uint256 maxCost
        ) internal view override returns (bytes memory context, uint256 validationData) {
            // Check if account is sponsored
            require(sponsoredAccounts[userOp.sender], "Not sponsored");
    
            // Check gas limit
            require(maxCost <= maxGasCost, "Gas too high");
    
            // Return context for postOp (if needed)
            return (abi.encode(userOp.sender), 0);
        }
    
        function _postOp(
            PostOpMode mode,
            bytes calldata context,
            uint256 actualGasCost
        ) internal override {
            // Optional: Track gas usage per user
            address sender = abi.decode(context, (address));
            emit GasSponsored(sender, actualGasCost);
        }
    
        // Deposit ETH for gas sponsorship
        function deposit() external payable {
            entryPoint().depositTo{value: msg.value}(address(this));
        }
    }
    
    Paymaster Types:
    - Verifying Paymaster: Requires off-chain signature
    - Deposit Paymaster: Users pre-deposit tokens
    - Sponsor Paymaster: Free gas for approved accounts
    - Token Paymaster: Pay gas in ERC20 tokens
    
  #### **Security Notes**
    - Prevent DoS by rate limiting
    - Validate userOp thoroughly
    - Monitor deposit balance

---
  #### **Id**
session-keys
  #### **Name**
Session Keys for Delegated Access
  #### **Description**
    Temporary keys with limited permissions for improved UX
    without compromising security
    
  #### **When To Use**
    - Gaming with frequent transactions
    - Automated DeFi strategies
    - Mobile app sessions
  #### **Implementation**
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.19;
    
    contract SessionKeyAccount is SmartAccount {
        struct SessionKey {
            address key;
            uint256 validAfter;
            uint256 validUntil;
            address[] allowedTargets;
            uint256 spendLimit;
            uint256 spent;
        }
    
        mapping(bytes32 => SessionKey) public sessionKeys;
    
        function createSessionKey(
            address key,
            uint256 duration,
            address[] calldata targets,
            uint256 spendLimit
        ) external onlyOwner returns (bytes32 keyId) {
            keyId = keccak256(abi.encode(key, block.timestamp));
            sessionKeys[keyId] = SessionKey({
                key: key,
                validAfter: block.timestamp,
                validUntil: block.timestamp + duration,
                allowedTargets: targets,
                spendLimit: spendLimit,
                spent: 0
            });
        }
    
        function _validateSignature(
            UserOperation calldata userOp,
            bytes32 userOpHash
        ) internal view override returns (uint256 validationData) {
            // Try owner signature first
            bytes32 hash = MessageHashUtils.toEthSignedMessageHash(userOpHash);
            address signer = ECDSA.recover(hash, userOp.signature);
    
            if (signer == owner) {
                return 0;
            }
    
            // Check session keys
            bytes32 keyId = _extractKeyId(userOp.signature);
            SessionKey storage sk = sessionKeys[keyId];
    
            if (signer != sk.key) return SIG_VALIDATION_FAILED;
            if (!_isValidTarget(userOp.callData, sk.allowedTargets)) {
                return SIG_VALIDATION_FAILED;
            }
    
            // Return validity window
            return _packValidationData(
                false,
                uint48(sk.validUntil),
                uint48(sk.validAfter)
            );
        }
    }
    
  #### **Security Notes**
    - Limit session key permissions strictly
    - Short validity windows (hours, not days)
    - Revocation mechanism required

## Anti-Patterns


---
  #### **Id**
no-nonce-validation
  #### **Name**
Missing UserOperation nonce validation
  #### **Severity**
critical
  #### **Description**
    Not properly validating nonces allows replay attacks
    where the same UserOperation is executed multiple times
    
  #### **Consequence**
    Attackers can replay valid UserOperations
    

---
  #### **Id**
unlimited-paymaster
  #### **Name**
Paymaster without spending limits
  #### **Severity**
high
  #### **Description**
    Paymaster that sponsors unlimited gas is vulnerable
    to draining attacks
    
  #### **Consequence**
    Attackers can drain paymaster's deposit
    