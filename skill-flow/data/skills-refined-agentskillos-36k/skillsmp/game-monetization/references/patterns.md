# Game Monetization & Economy Design

## Patterns


---
  #### **Name**
Dual Currency System
  #### **Description**
    Implement soft currency (earned) and hard currency (purchased) separation.
    Soft currency for progression, hard currency for convenience and cosmetics.
    
  #### **Example**
    // Currency configuration
    const currencies = {
      soft: {
        name: 'Gold',
        earnedThrough: ['gameplay', 'dailyRewards', 'achievements'],
        spentOn: ['basicItems', 'upgrades', 'repairs'],
        inflationControl: 'sinkMechanics'
      },
      hard: {
        name: 'Gems',
        earnedThrough: ['purchase', 'rareAchievements', 'seasonRewards'],
        spentOn: ['premiumItems', 'speedups', 'cosmetics'],
        conversionRate: null  // Never allow soft->hard conversion
      }
    };
    
  #### **Rationale**
Separates earnable and purchasable economies, preventing inflation from devaluing purchases

---
  #### **Name**
Sink-Source Balance
  #### **Description**
    Every currency faucet (source) must have corresponding drains (sinks).
    Track net currency flow and adjust dynamically.
    
  #### **Example**
    // Economy balance tracking
    class EconomyManager {
      trackTransaction(playerId, currency, amount, source) {
        const isSource = amount > 0;
        this.metrics.record({
          currency,
          type: isSource ? 'source' : 'sink',
          amount: Math.abs(amount),
          source,
          timestamp: Date.now()
        });
    
        // Alert if economy is inflating
        const netFlow = this.calculateNetFlow(currency, '24h');
        if (netFlow > this.thresholds[currency].maxInflation) {
          this.alertEconomyTeam('INFLATION_WARNING', { currency, netFlow });
        }
      }
    }
    
  #### **Rationale**
Prevents economy inflation that devalues player purchases and progression

---
  #### **Name**
Value Anchoring
  #### **Description**
    Establish clear value perception through anchor pricing and bundle comparisons.
    Best value should be obvious without being manipulative.
    
  #### **Example**
    // IAP pricing with anchoring
    const gemPackages = [
      { gems: 100, price: 0.99, perGem: 0.0099, label: null },
      { gems: 550, price: 4.99, perGem: 0.0091, label: null },
      { gems: 1200, price: 9.99, perGem: 0.0083, label: 'Popular' },
      { gems: 2500, price: 19.99, perGem: 0.0080, label: null },
      { gems: 6500, price: 49.99, perGem: 0.0077, label: 'Best Value' },
      { gems: 14000, price: 99.99, perGem: 0.0071, label: null }
    ];
    // Note: ~30% value increase from smallest to largest is standard
    
  #### **Rationale**
Clear value progression encourages larger purchases without deception

---
  #### **Name**
Progression Pacing
  #### **Description**
    Battle pass should be completable with reasonable play time.
    Never require more than 1-2 hours daily for free track completion.
    
  #### **Example**
    // Battle pass configuration
    const battlePassConfig = {
      duration: 70, // days
      totalLevels: 100,
      xpPerLevel: 1000,
    
      // XP sources - completable in ~1hr/day
      dailyQuests: { count: 3, xpEach: 300 },  // 900 XP
      weeklyQuests: { count: 7, xpEach: 1500 }, // 10,500 XP/week
      gameplayXP: { perMatch: 50, avgMatchTime: 15 }, // ~200 XP/hr
    
      // Catch-up mechanics
      catchUpBonus: {
        enabled: true,
        afterWeek: 4,
        bonusMultiplier: 1.5
      },
    
      // Premium track value
      premiumPrice: 9.99,
      premiumValue: 25.00, // Always 2-3x price in perceived value
      premiumCurrencyReturn: 1000 // Enough for next pass
    };
    
  #### **Rationale**
Completable passes build trust; impossible passes cause frustration and churn

---
  #### **Name**
FOMO Without Exploitation
  #### **Description**
    Create urgency through seasonal content, not artificial scarcity of essentials.
    Cosmetics can be exclusive; gameplay advantages should not be.
    
  #### **Example**
    // Ethical seasonal content
    const seasonalContent = {
      exclusive: {
        // OK to be time-limited
        cosmetics: ['Winter Warrior Skin', 'Holiday Emote'],
        titles: ['2024 Champion'],
        profileItems: ['Seasonal Border']
      },
      returning: {
        // Must return or have alternatives
        gameplayItems: ['Frostbite Weapon'], // Returns next year
        characters: ['Santa Helper'], // Available in off-season shop
        modes: ['Snowball Fight'] // Annual event
      },
      never_exclusive: {
        // Always available somehow
        progression: ['Level unlocks'],
        balance: ['Meta weapons'],
        social: ['Chat features']
      }
    };
    
  #### **Rationale**
FOMO for cosmetics is acceptable; FOMO for gameplay creates toxic community

---
  #### **Name**
Loot Box Transparency
  #### **Description**
    Always disclose exact probabilities. Implement pity systems.
    Consider regulatory requirements across regions.
    
  #### **Example**
    // Ethical gacha implementation
    const gachaConfig = {
      baseRates: {
        common: 0.60,
        rare: 0.30,
        epic: 0.08,
        legendary: 0.02
      },
    
      // Pity system - guaranteed after N pulls
      pity: {
        epic: { threshold: 30, guarantee: true },
        legendary: { threshold: 90, guarantee: true }
      },
    
      // Transparency requirements
      disclosure: {
        showRates: true, // Always visible before purchase
        showPity: true,  // Show current pity counter
        pullHistory: true, // Viewable pull history
        consolidatedRates: true // For items in rate-up pools
      },
    
      // Regional compliance
      regions: {
        BE: { enabled: false }, // Belgium - banned
        NL: { enabled: false }, // Netherlands - banned
        JP: { requireKompu: true }, // Japan - kompu gacha banned
        CN: { requireRates: true, maxSpendPerDay: 500 }
      }
    };
    
  #### **Rationale**
Transparency builds trust; hidden rates destroy it and may be illegal

---
  #### **Name**
Spending Safeguards
  #### **Description**
    Implement spending limits, cooldowns, and notifications to protect players.
    This reduces refunds and regulatory risk while building goodwill.
    
  #### **Example**
    // Player spending protection
    class SpendingProtection {
      async validatePurchase(playerId, amount) {
        const player = await this.getPlayer(playerId);
    
        // Daily limit check
        const dailySpend = await this.getDailySpend(playerId);
        if (dailySpend + amount > player.dailyLimit) {
          return { blocked: true, reason: 'DAILY_LIMIT', resetIn: this.timeUntilReset() };
        }
    
        // Monthly limit check
        const monthlySpend = await this.getMonthlySpend(playerId);
        if (monthlySpend + amount > player.monthlyLimit) {
          return { blocked: true, reason: 'MONTHLY_LIMIT' };
        }
    
        // Velocity check - too many purchases too fast
        const recentPurchases = await this.getRecentPurchases(playerId, '1h');
        if (recentPurchases.length > 5) {
          await this.triggerCooldown(playerId, '15m');
          return { blocked: true, reason: 'COOLDOWN', resumeIn: '15m' };
        }
    
        // Large purchase confirmation
        if (amount > 50) {
          return { requireConfirmation: true, message: 'Large purchase - please confirm' };
        }
    
        return { allowed: true };
      }
    }
    
  #### **Rationale**
Protecting players from regret purchases reduces chargebacks and builds loyalty

---
  #### **Name**
LTV Cohort Analysis
  #### **Description**
    Track player lifetime value by acquisition cohort and segment.
    Use predictive LTV to optimize acquisition and retention spend.
    
  #### **Example**
    // LTV tracking and prediction
    const ltvMetrics = {
      // Track by cohort
      cohorts: {
        definition: 'installWeek',
        segments: ['organic', 'paid_social', 'paid_search', 'influencer']
      },
    
      // Key milestones
      milestones: {
        d1: { retention: 0.40, arpu: 0.05 },
        d7: { retention: 0.15, arpu: 0.20 },
        d30: { retention: 0.05, arpu: 0.80 },
        d90: { retention: 0.02, arpu: 2.00 },
        d365: { retention: 0.01, arpu: 5.00 }
      },
    
      // Predictive model
      predictLTV: (player) => {
        const features = {
          d1Retention: player.returnedDay1,
          d1Sessions: player.sessionsDay1,
          d1Engagement: player.engagementScoreDay1,
          firstPurchase: player.firstPurchaseAmount,
          source: player.acquisitionSource
        };
        return model.predict(features);
      },
    
      // Segment definitions
      segments: {
        nonPayer: { ltv: [0, 0], percentage: 0.95 },
        minnow: { ltv: [0.01, 10], percentage: 0.03 },
        dolphin: { ltv: [10, 100], percentage: 0.015 },
        whale: { ltv: [100, 1000], percentage: 0.004 },
        superWhale: { ltv: [1000, Infinity], percentage: 0.001 }
      }
    };
    
  #### **Rationale**
Understanding LTV by segment enables targeted retention and acquisition strategies

## Anti-Patterns


---
  #### **Name**
Pay-to-Win Mechanics
  #### **Description**
    NEVER sell gameplay advantages that cannot be earned through play.
    This destroys competitive integrity and community trust.
    
  #### **Bad Example**
    // TERRIBLE: Direct power purchase
    const store = {
      items: [
        { id: 'superSword', damage: 500, price: 49.99, earnableAlternative: null },
        { id: 'godMode', invincibility: 60, price: 9.99 }
      ]
    };
    
  #### **Good Example**
    // BETTER: Time-saver, not power advantage
    const store = {
      items: [
        { id: 'xpBoost', bonus: '2x', duration: '24h', price: 4.99 },
        { id: 'characterUnlock', character: 'ninja', price: 9.99,
          earnableAfter: '40 hours' }, // Can be earned!
        { id: 'skinBundle', cosmetic: true, price: 14.99 }
      ]
    };
    
  #### **Consequence**
Pay-to-win causes 90%+ negative reviews and community abandonment

---
  #### **Name**
Uncapped Gacha Spending
  #### **Description**
    Never allow unlimited spending on gacha without pity systems.
    Players spending $1000+ without guaranteed reward creates legal and PR risk.
    
  #### **Bad Example**
    // TERRIBLE: No pity, no limits
    function pullGacha() {
      const roll = Math.random();
      if (roll < 0.001) return 'SSR';  // 0.1% forever
      if (roll < 0.01) return 'SR';
      return 'R';
    }
    
  #### **Good Example**
    // BETTER: Guaranteed pity
    function pullGacha(playerId) {
      const pityCounter = getPityCounter(playerId);
    
      if (pityCounter >= 90) {
        resetPity(playerId);
        return 'SSR'; // Guaranteed at 90
      }
    
      // Soft pity: increasing rates from 75+
      let ssrRate = 0.006;
      if (pityCounter >= 75) {
        ssrRate += (pityCounter - 74) * 0.06; // +6% per pull
      }
    
      incrementPity(playerId);
      return rollWithRates({ ssr: ssrRate, sr: 0.051, r: 1 - ssrRate - 0.051 });
    }
    
  #### **Consequence**
Uncapped gacha leads to lawsuits, refunds, and regulatory action

---
  #### **Name**
Hidden Currency Conversion
  #### **Description**
    Never obscure real money costs through complex currency conversions.
    Players should always understand what they're spending.
    
  #### **Bad Example**
    // TERRIBLE: Obfuscated pricing
    // $9.99 = 1000 gems
    // Skin costs 850 gems
    // Player thinks: "Is that $8.50?"
    // Actually: Must buy 1000, leftover 150 is useless
    
  #### **Good Example**
    // BETTER: Clear pricing
    const storeItem = {
      name: 'Dragon Skin',
      priceGems: 850,
      priceUSD: 8.49, // Show real price!
      gemPackageNeeded: '1000 gems ($9.99)',
      leftoverGems: 150,
      leftoverCanBuy: ['3x Daily Rewards Unlock']
    };
    
  #### **Consequence**
Players feel tricked, leading to refund requests and trust loss

---
  #### **Name**
Aggressive Monetization Popups
  #### **Description**
    Never interrupt gameplay with purchase prompts.
    Players buy when they want to, not when forced.
    
  #### **Bad Example**
    // TERRIBLE: Death = purchase prompt
    onPlayerDeath() {
      showPopup({
        title: 'Continue for just $0.99?',
        buttons: ['Pay $0.99', 'Watch Ad', 'Lose Progress']
      });
    }
    
  #### **Good Example**
    // BETTER: Contextual, non-blocking offers
    onPlayerDeath() {
      showDeathScreen({
        stats: playerRunStats,
        rewards: calculateRewards(),
        // Small, non-intrusive upsell
        suggestion: hasWatchedAd ? null : 'Watch ad for 2x rewards?'
      });
    
      // Store is always accessible but never forced
      showStoreButton({ position: 'corner', style: 'subtle' });
    }
    
  #### **Consequence**
Aggressive popups have 10x higher uninstall rates than contextual offers

---
  #### **Name**
Economy Hyperinflation
  #### **Description**
    Never increase currency rewards without proportional sinks.
    Inflation devalues purchases and breaks progression.
    
  #### **Bad Example**
    // TERRIBLE: Escalating rewards without sinks
    const levelRewards = {
      1: 100,
      10: 1000,
      20: 10000,
      30: 100000,
      40: 1000000 // Exponential inflation!
    };
    // Items still cost 500-5000... currency is meaningless
    
  #### **Good Example**
    // BETTER: Controlled economy
    const economyDesign = {
      rewards: {
        linear: true,
        level1: 100,
        level50: 500, // Only 5x, not 10000x
      },
      costs: {
        earlyGame: { min: 50, max: 500 },
        midGame: { min: 200, max: 2000 },
        endGame: { min: 500, max: 5000 },
      },
      sinks: {
        repairs: 'percentage of power',
        consumables: 'required for high-end content',
        cosmetics: 'expensive vanity items',
        prestige: 'reset for permanent bonuses'
      }
    };
    
  #### **Consequence**
Inflation makes early purchases feel worthless, destroying trust