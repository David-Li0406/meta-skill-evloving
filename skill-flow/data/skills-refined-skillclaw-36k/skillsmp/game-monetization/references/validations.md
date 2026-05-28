# Game Monetization - Validations

## Client-Side Currency Manipulation

### **Id**
client-side-currency
### **Category**
security
### **Severity**
critical
### **Description**
  Currency values stored or calculated on client can be modified by cheaters.
  All currency operations must be validated server-side.
  
### **Pattern**
  #### **Regex**
(localStorage|sessionStorage|PlayerPrefs)\.(set|get).*(currency|gold|gems|coins|credits|money)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
  - csharp
### **Bad Example**
  // VULNERABLE: Client-side currency storage
  function addGold(amount) {
    const current = parseInt(localStorage.getItem('gold') || '0');
    localStorage.setItem('gold', current + amount);
  }
  
### **Good Example**
  // SECURE: Server-validated currency
  async function addGold(amount, transactionId) {
    const response = await fetch('/api/currency/add', {
      method: 'POST',
      body: JSON.stringify({
        currency: 'gold',
        amount,
        transactionId,
        signature: await signRequest(transactionId)
      })
    });
    return response.json(); // Server is source of truth
  }
  
### **Fix**
Move all currency operations to server-side with proper validation

## Unvalidated In-App Purchase

### **Id**
unvalidated-purchase
### **Category**
security
### **Severity**
critical
### **Description**
  IAP receipts must be validated server-side with Apple/Google.
  Client-only validation can be bypassed to get free items.
  
### **Pattern**
  #### **Regex**
(purchaseProduct|buyProduct|makePurchase).*(?!.*validateReceipt|verifyPurchase|serverValidate)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
  - swift
  - kotlin
### **Bad Example**
  // VULNERABLE: No receipt validation
  async function completePurchase(productId) {
    const result = await iap.purchaseProduct(productId);
    if (result.success) {
      grantItem(productId); // Directly granting without validation!
    }
  }
  
### **Good Example**
  // SECURE: Server-side receipt validation
  async function completePurchase(productId) {
    const result = await iap.purchaseProduct(productId);
    if (result.success) {
      // Validate receipt with server (which validates with Apple/Google)
      const validation = await fetch('/api/iap/validate', {
        method: 'POST',
        body: JSON.stringify({
          receipt: result.receipt,
          productId,
          platform: Platform.OS
        })
      });
  
      if (validation.ok) {
        const { granted } = await validation.json();
        updateInventory(granted); // Server already granted items
      }
    }
  }
  
### **Fix**
Always validate IAP receipts server-side before granting items

## Pricing Logic Exposed to Client

### **Id**
exposed-pricing-logic
### **Category**
security
### **Severity**
high
### **Description**
  Discount calculations, dynamic pricing, and special offer logic
  should not be in client code where it can be reverse-engineered or manipulated.
  
### **Pattern**
  #### **Regex**
(discount|price|offer).*=.*\d+.*[%\*\/]|calculatePrice|applyDiscount
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
### **Bad Example**
  // VULNERABLE: Client-side discount calculation
  function getDiscountedPrice(basePrice, userLevel) {
    let discount = 0;
    if (userLevel > 10) discount = 0.1;
    if (userLevel > 50) discount = 0.2;
    if (isWhale(user)) discount = 0.3; // Exposes whale detection!
    return basePrice * (1 - discount);
  }
  
### **Good Example**
  // SECURE: Server provides final prices
  async function getStoreItems() {
    const response = await fetch('/api/store/items', {
      headers: { Authorization: getAuthToken() }
    });
    // Server calculates all discounts and returns final prices
    return response.json();
  }
  
### **Fix**
Fetch final prices from server; don't calculate discounts client-side

## Unbounded Currency Grant

### **Id**
unbounded-currency-grant
### **Category**
economy
### **Severity**
high
### **Description**
  Currency grants without upper bounds can be exploited or cause
  hyperinflation through bugs or exploits.
  
### **Pattern**
  #### **Regex**
(grant|add|give)(Currency|Gold|Gems|Coins)\s*\([^)]*\)(?!.*Math\.min|limit|cap|max)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
  - csharp
  - python
### **Bad Example**
  // RISKY: No bounds on currency grant
  function grantDailyReward(player, streak) {
    const reward = 100 * Math.pow(2, streak); // Exponential = disaster
    player.addGold(reward);
  }
  
### **Good Example**
  // SAFE: Bounded currency grants
  const DAILY_REWARD_CAP = 10000;
  
  function grantDailyReward(player, streak) {
    const baseReward = 100 * Math.min(streak, 30); // Linear, capped at 30 days
    const reward = Math.min(baseReward, DAILY_REWARD_CAP);
  
    // Log for economy monitoring
    economyLogger.log('GRANT', {
      player: player.id,
      type: 'daily_reward',
      amount: reward,
      streak
    });
  
    player.addGold(reward);
  }
  
### **Fix**
Always cap currency grants and log for economy monitoring

## Currency Source Without Sink

### **Id**
missing-currency-sink
### **Category**
economy
### **Severity**
medium
### **Description**
  Every currency faucet needs corresponding drains, or the economy inflates.
  Check that new currency sources have matching sinks.
  
### **Pattern**
  #### **Regex**
(reward|grant|earn|receive)(Currency|Gold|Coins|Gems).*(?!.*spend|cost|consume|sink)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
### **Bad Example**
  // RISKY: Reward without corresponding sink
  function onLevelComplete(player, level) {
    player.grantGold(level * 500);
    player.grantGems(level * 10);
    // Where does this currency go? No sinks mentioned!
  }
  
### **Good Example**
  // BALANCED: Document and track economy flow
  function onLevelComplete(player, level) {
    const goldReward = level * 500;
    const gemReward = level * 10;
  
    player.grantGold(goldReward);
    player.grantGems(gemReward);
  
    // Track for economy balance
    economyTracker.recordSource({
      player: player.id,
      source: 'level_complete',
      gold: goldReward,
      gems: gemReward
    });
  
    // Economy design doc specifies sinks:
    // - Gold: Equipment upgrades (level*300), repairs (level*100)
    // - Gems: Cosmetics (500-2000), skips (50-100)
  }
  
### **Fix**
Document currency sinks for every source and track flow

## Hardcoded Economy Values

### **Id**
hardcoded-economy-values
### **Category**
economy
### **Severity**
medium
### **Description**
  Economy values (prices, rewards, rates) hardcoded in client make
  live balancing impossible without app updates.
  
### **Pattern**
  #### **Regex**
(price|cost|reward|rate)\s*[:=]\s*\d{2,}
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
  - csharp
### **Bad Example**
  // INFLEXIBLE: Hardcoded prices
  const STORE = {
    sword: { price: 500 },
    shield: { price: 350 },
    potion: { price: 50 }
  };
  
### **Good Example**
  // FLEXIBLE: Server-driven prices
  class StoreManager {
    async loadPrices() {
      const config = await fetch('/api/config/store');
      this.prices = await config.json();
      this.lastUpdate = Date.now();
    }
  
    getPrice(item) {
      // Fallback to defaults, but prefer server values
      return this.prices[item] ?? FALLBACK_PRICES[item];
    }
  }
  
### **Fix**
Load economy values from server/remote config for live tuning

## Loot Box Without Probability Disclosure

### **Id**
missing-probability-disclosure
### **Category**
compliance
### **Severity**
critical
### **Description**
  Many jurisdictions require displaying gacha/loot box probabilities.
  Missing disclosures can result in store removal or legal action.
  
### **Pattern**
  #### **Regex**
(lootbox|gacha|randomBox|chest|pack)\.(open|pull|buy)(?!.*showRates|displayProbability|rateDisclosure)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
### **Bad Example**
  // NON-COMPLIANT: No rate disclosure
  function openLootBox(boxId) {
    const roll = Math.random();
    if (roll < 0.01) return 'legendary';
    if (roll < 0.10) return 'epic';
    return 'common';
  }
  
### **Good Example**
  // COMPLIANT: Rates disclosed and accessible
  const LOOT_BOX_RATES = {
    legendary: 0.01,  // 1%
    epic: 0.09,       // 9%
    rare: 0.20,       // 20%
    common: 0.70      // 70%
  };
  
  function openLootBox(boxId) {
    // Rates are displayed in UI before purchase
    // Button: "View Drop Rates" -> shows LOOT_BOX_RATES
  
    const roll = Math.random();
    let cumulative = 0;
    for (const [rarity, rate] of Object.entries(LOOT_BOX_RATES)) {
      cumulative += rate;
      if (roll < cumulative) return rarity;
    }
  }
  
  function showLootBoxRates(boxId) {
    ui.showModal({
      title: 'Drop Rates',
      content: Object.entries(LOOT_BOX_RATES)
        .map(([r, p]) => `${r}: ${(p * 100).toFixed(1)}%`)
        .join('\n')
    });
  }
  
### **Fix**
Display probability rates before any random purchase

## IAP Without Age Verification

### **Id**
missing-age-gate
### **Category**
compliance
### **Severity**
high
### **Description**
  Games with IAP targeting or accessible to children need age gates
  and parental consent mechanisms for COPPA/GDPR-K compliance.
  
### **Pattern**
  #### **Regex**
(purchase|buy|iap)(?!.*ageVerify|parentalConsent|ageGate)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
### **Bad Example**
  // NON-COMPLIANT: No age consideration
  async function buyGems(amount) {
    await iap.purchase(`gems_${amount}`);
    grantGems(amount);
  }
  
### **Good Example**
  // COMPLIANT: Age-aware purchase flow
  async function buyGems(amount) {
    const user = await getUser();
  
    if (user.age < 13 || !user.ageVerified) {
      const parentalApproval = await requestParentalConsent({
        action: 'purchase',
        amount,
        item: 'gems'
      });
  
      if (!parentalApproval) {
        return { blocked: true, reason: 'PARENTAL_CONSENT_REQUIRED' };
      }
    }
  
    await iap.purchase(`gems_${amount}`);
    grantGems(amount);
  }
  
### **Fix**
Implement age verification and parental consent for minors

## Region-Unaware Monetization Feature

### **Id**
region-unaware-monetization
### **Category**
compliance
### **Severity**
high
### **Description**
  Loot boxes, certain payment methods, and pricing must respect
  regional regulations. Serving banned features causes legal issues.
  
### **Pattern**
  #### **Regex**
(gacha|lootbox|gambling)(?!.*checkRegion|regionAllowed|geoCheck)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
### **Bad Example**
  // NON-COMPLIANT: No regional awareness
  function showGachaShop() {
    ui.showScreen('gacha_shop');
  }
  
### **Good Example**
  // COMPLIANT: Region-aware features
  const BANNED_GACHA_REGIONS = ['BE', 'NL'];
  
  async function showGachaShop() {
    const region = await getPlayerRegion();
  
    if (BANNED_GACHA_REGIONS.includes(region)) {
      ui.showScreen('direct_purchase_shop');
      return;
    }
  
    ui.showScreen('gacha_shop');
  }
  
### **Fix**
Check player region before showing region-restricted features

## Real Currency Price Hidden

### **Id**
hidden-real-price
### **Category**
ux
### **Severity**
high
### **Description**
  Showing only premium currency price without real money equivalent
  is a dark pattern that regulators are targeting.
  
### **Pattern**
  #### **Regex**
(price|cost).*gems|diamonds|crystals(?!.*\$|USD|EUR|real|currency)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
### **Bad Example**
  // DARK PATTERN: Only shows gems
  function renderStoreItem(item) {
    return `
      <div class="item">
        <span>${item.name}</span>
        <span class="price">${item.gems} Gems</span>
      </div>
    `;
  }
  
### **Good Example**
  // TRANSPARENT: Shows both currencies
  function renderStoreItem(item) {
    const realPrice = convertToRealCurrency(item.gems);
    return `
      <div class="item">
        <span>${item.name}</span>
        <span class="price">${item.gems} Gems</span>
        <span class="real-price">(~${realPrice})</span>
      </div>
    `;
  }
  
### **Fix**
Always show approximate real currency value alongside premium currency

## Purchase Without Confirmation

### **Id**
purchase-without-confirmation
### **Category**
ux
### **Severity**
medium
### **Description**
  One-click purchases without confirmation lead to accidental purchases,
  refunds, and negative reviews.
  
### **Pattern**
  #### **Regex**
(onClick|onPress|onTap).*purchase|buy(?!.*confirm|modal|dialog)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
### **Bad Example**
  // RISKY: One-click purchase
  <Button onClick={() => buyItem(item.id)}>
    Buy for 500 Gems
  </Button>
  
### **Good Example**
  // SAFE: Confirmation required
  <Button onClick={() => showPurchaseConfirmation(item)}>
    Buy for 500 Gems
  </Button>
  
  function showPurchaseConfirmation(item) {
    ui.showModal({
      title: 'Confirm Purchase',
      content: `Buy ${item.name} for ${item.price} Gems (~$${item.realPrice})?`,
      buttons: [
        { text: 'Cancel', action: 'close' },
        { text: 'Confirm', action: () => buyItem(item.id) }
      ]
    });
  }
  
### **Fix**
Require confirmation for all purchases, especially premium currency

## Aggressive Monetization Popup

### **Id**
aggressive-popup
### **Category**
ux
### **Severity**
medium
### **Description**
  Popups that interrupt gameplay to push purchases cause player frustration
  and have high uninstall rates.
  
### **Pattern**
  #### **Regex**
(onDeath|onFail|onGameOver).*showOffer|showPurchase|showAd
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
### **Bad Example**
  // AGGRESSIVE: Death triggers purchase prompt
  function onPlayerDeath() {
    showPopup({
      title: 'Continue?',
      message: 'Buy a revive for just 50 gems!',
      buttons: ['Buy', 'Watch Ad', 'Give Up']
    });
  }
  
### **Good Example**
  // RESPECTFUL: Non-blocking offer
  function onPlayerDeath() {
    showDeathScreen({
      stats: getRunStats(),
      rewards: calculateRewards(),
      // Optional, non-pushy upsell
      tip: canAffordRevive() ? 'Tap menu for revive options' : null
    });
  }
  
### **Fix**
Avoid interrupting gameplay with purchase prompts

## Purchase Without Analytics

### **Id**
untracked-purchase
### **Category**
analytics
### **Severity**
high
### **Description**
  All purchases must be tracked for revenue attribution, LTV calculation,
  and fraud detection. Untracked purchases are invisible to business.
  
### **Pattern**
  #### **Regex**
(purchase|buy|grant)(?!.*analytics|track|log|event)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
### **Bad Example**
  // BLIND: No tracking
  async function completePurchase(item) {
    await iap.purchase(item.sku);
    grantItem(item.id);
  }
  
### **Good Example**
  // TRACKED: Full analytics
  async function completePurchase(item) {
    const result = await iap.purchase(item.sku);
  
    analytics.track('purchase_complete', {
      item_id: item.id,
      item_name: item.name,
      price_usd: item.priceUSD,
      price_local: item.priceLocal,
      currency: item.currency,
      sku: item.sku,
      transaction_id: result.transactionId,
      is_first_purchase: await isFirstPurchase(),
      session_number: getSessionNumber(),
      days_since_install: getDaysSinceInstall()
    });
  
    grantItem(item.id);
  }
  
### **Fix**
Track all purchase events with full context for LTV analysis

## Purchase Funnel Not Tracked

### **Id**
missing-funnel-tracking
### **Category**
analytics
### **Severity**
medium
### **Description**
  Without funnel tracking, you can't identify where players drop off
  in the purchase flow. Every step needs an event.
  
### **Pattern**
  #### **Regex**
showStore|openShop(?!.*analytics|track|funnel)
  #### **Flags**
i
### **Languages**
  - javascript
  - typescript
### **Bad Example**
  // BLIND: No funnel visibility
  function openStore() {
    ui.showScreen('store');
  }
  
### **Good Example**
  // TRACKED: Full funnel
  function openStore(source) {
    analytics.track('store_opened', { source });
    ui.showScreen('store');
  }
  
  function viewItem(item) {
    analytics.track('item_viewed', {
      item_id: item.id,
      price: item.price,
      time_in_store: getTimeInStore()
    });
  }
  
  function addToCart(item) {
    analytics.track('add_to_cart', { item_id: item.id });
  }
  
  function initiateCheckout(items) {
    analytics.track('checkout_started', {
      items: items.map(i => i.id),
      total: calculateTotal(items)
    });
  }
  
  function completePurchase(result) {
    analytics.track('purchase_complete', { ... });
  }
  
  function abandonCart(items) {
    analytics.track('cart_abandoned', {
      items: items.map(i => i.id),
      total: calculateTotal(items),
      time_in_checkout: getTimeInCheckout()
    });
  }
  
### **Fix**
Track every step of purchase funnel for optimization