---
title: Fee Flow Controller Mechanics
impact: MEDIUM
impactDescription: Understanding protocol revenue and fee distribution
tags: fees, feeflow, auction, revenue, protocol
---

## Fee Flow Controller Mechanics

FeeFlowController implements continuous Dutch auctions to sell accumulated protocol fees. It sells any assets it holds (typically vault shares from interest fees) in exchange for payment tokens sent to the DAO.

**Incorrect (expecting direct fee claiming):**

```solidity
// WRONG: Fees are not claimed directly from vaults
IEVault vault = IEVault(vaultAddress);
vault.claimFees(); // This doesn't exist!
```

**Correct (understanding fee flow architecture):**

```solidity
import {IEVault} from "evk/EVault/IEVault.sol";

IEVault vault = IEVault(vaultAddress);

// Interest fees accumulate in the vault as shares
// interestFee is the percentage of interest that goes to protocol
uint16 interestFee = vault.interestFee(); // e.g., 0.1e4 = 10%

// Accumulated fees are in vault shares
uint256 accumulatedFees = vault.accumulatedFees();

// The fee receiver is typically the FeeFlowController
address feeReceiver = vault.feeReceiver();

// convertFees() converts accumulated shares to the fee receiver
// Anyone can call this to trigger the conversion
// This must be called BEFORE buying from FeeFlowController
vault.convertFees();
```

**Correct (interacting with FeeFlowController):**

```solidity
import {FeeFlowController} from "fee-flow/FeeFlowController.sol";

FeeFlowController feeFlow = FeeFlowController(feeFlowAddress);

// Get current auction state
uint256 currentPrice = feeFlow.getPrice();
FeeFlowController.Slot0 memory slot0 = feeFlow.getSlot0();

// Auction parameters (immutable)
uint256 epochPeriod = feeFlow.epochPeriod();         // Auction duration
uint256 priceMultiplier = feeFlow.priceMultiplier(); // Price scaling (1.1e18 - 3e18)
uint256 minInitPrice = feeFlow.minInitPrice();       // Minimum starting price

// Payment token (what buyer pays)
address paymentToken = address(feeFlow.paymentToken());

// Payment receiver (where payment goes - DAO treasury)
address paymentReceiver = feeFlow.paymentReceiver();
```

**Correct (buying from the auction):**

```solidity
import {IERC20} from "openzeppelin-contracts/token/ERC20/IERC20.sol";

// Dutch auction: price starts high and decreases over epoch
// Anyone can buy all assets held by FeeFlowController at current price

// Step 1: Ensure fees have been converted to FeeFlowController
// (convertFees must be called on vaults separately)
vault.convertFees();

// Step 2: Check current price and epoch
FeeFlowController.Slot0 memory slot0 = feeFlow.getSlot0();
uint256 price = feeFlow.getPrice();

// Step 3: Specify which assets to receive (vault shares held by FeeFlowController)
address[] memory assets = new address[](2);
assets[0] = vault1Address;  // Vault 1 shares
assets[1] = vault2Address;  // Vault 2 shares

// Step 4: Approve payment token
IERC20(paymentToken).approve(address(feeFlow), price);

// Step 5: Buy all assets
// Transfers payment to paymentReceiver, sends assets to buyer
feeFlow.buy(
    assets,                    // Asset addresses to receive
    msg.sender,                // Receiver of assets
    slot0.epochId,             // Current epoch ID (prevents front-running)
    block.timestamp + 1 hours, // Deadline
    price * 101 / 100          // Max payment (with 1% slippage)
);
```

**Key FeeFlow Concepts:**

1. **Dutch Auction**: Price decreases linearly over epoch period (price = initPrice - initPrice * timePassed / epochPeriod)
2. **Epoch Reset**: After each buy, new auction starts with adjusted initial price
3. **Price Adaptation**: New initPrice = settlementPrice * priceMultiplier (clamped to min/max)
4. **Price at Epoch End**: If no one buys, price reaches 0 (assets are free)
5. **Manual Fee Conversion**: `convertFees()` must be called on vaults separately before buying

Reference: [FeeFlowController.sol](https://github.com/euler-xyz/fee-flow/blob/master/src/FeeFlowController.sol)
