# PropTraderAI Firm Rules Database

**Version:** 1.0  
**Last Updated:** January 10, 2026  
**Purpose:** Offline reference for prop firm rules, constraints, and automation policies

---

## Overview

This directory contains JSON files for prop trading firms, providing Claude with up-to-date rules for strategy validation. These files serve as:

1. **Offline Reference** - Instant access without API calls
2. **Fallback Data** - Used when API is unavailable
3. **Static Rules** - Profit targets, drawdown types, contract limits
4. **Automation Policies** - Which firms allow automated trading

---

## Directory Structure

```
firm_rules/
├── README.md (this file)
├── topstep.json ✅ Automation allowed
├── myfundedfutures.json ✅ Automation allowed
├── tradeify.json ✅ Automation allowed
├── alpha-futures.json ✅ Automation allowed
├── ftmo.json ✅ Automation allowed
└── fundednext.json ✅ Automation allowed
```

---

## Automation Policy Key

| Symbol | Policy | Description |
|--------|--------|-------------|
| ✅ | **Allowed** | Firm explicitly permits automated trading |
| ⚠️ | **Restricted** | Allowed with specific conditions/limitations |
| ❌ | **Prohibited** | Firm does not allow automated trading |
| ❓ | **Unclear** | Policy not publicly documented |

---

## Included Firms

### Tier 1: Automation-Friendly (PropTraderAI Focus)

These firms explicitly allow automated trading and are the primary focus for PropTraderAI integration.

#### 1. **Topstep** ✅
- **Founded:** 2012 (Most established)
- **Automation:** Explicitly allowed, TopstepX API available ($29/mo)
- **Key Feature:** Best education and coaching
- **Restrictions:** No VPS/VPN (must trade from personal device), no HFT
- **File:** `topstep.json`
- **Last Verified:** 2026-01-10

#### 2. **MyFundedFutures** ✅
- **Founded:** 2023 (Fast-growing)
- **Automation:** Updated July 2025 to explicitly permit
- **Key Feature:** Consistency rule removed after funding (Expert plan)
- **Restrictions:** Active supervision required, no HFT (>200 trades/day)
- **File:** `myfundedfutures.json`
- **Last Verified:** 2026-01-10

#### 3. **Tradeify** ✅
- **Founded:** 2021
- **Automation:** Allowed with ownership verification
- **Key Feature:** One-time fee (no monthly subscription)
- **Restrictions:** Must prove sole ownership, cannot deploy across multiple firms
- **File:** `tradeify.json`
- **Last Verified:** 2026-01-10

#### 4. **Alpha Futures** ✅
- **Founded:** 2023
- **Automation:** Allows bots/EAs
- **Key Feature:** Tiered scaling system
- **Restrictions:** Standard (no HFT, no exploitation)
- **File:** `alpha-futures.json`
- **Last Verified:** 2026-01-10

#### 5. **FTMO** ✅
- **Founded:** 2015
- **Automation:** Explicitly allows Expert Advisors
- **Key Feature:** Largest international firm (200K+ traders), weekend holding
- **Restrictions:** Standard restrictions, 30-day time limit
- **File:** `ftmo.json`
- **Last Verified:** 2026-01-10

#### 6. **FundedNext** ✅
- **Founded:** 2022
- **Automation:** Explicitly allows automated trading
- **Key Feature:** Multiple challenge types, 40% consistency rule
- **Restrictions:** Stricter consistency rule (40% vs typical 50%)
- **File:** `fundednext.json`
- **Last Verified:** 2026-01-10

---

## JSON File Structure

Each firm file follows this schema:

```json
{
  "firm_name": "String",
  "slug": "url-safe-identifier",
  "website": "https://...",
  "founded": 2023,
  "headquarters": "Location",
  "trustpilot_rating": 4.8,
  "automation_policy": "allowed|prohibited|semi_allowed|unclear",
  "automation_notes": "Detailed policy explanation",
  "last_verified": "2026-01-10",
  "account_sizes": [25000, 50000, 100000],
  "rules": {
    "50000": {
      "profit_target": 3000,
      "daily_loss_limit": 2000,
      "max_drawdown": 2500,
      "drawdown_type": "eod_trailing|static|trailing",
      "max_contracts": { "ES": 10, "NQ": 10, ... },
      "consistency_rule": 0.50,
      "allows_overnight": true,
      "allows_news_trading": false,
      ...
    }
  },
  "payout_structure": { ... },
  "scaling_requirements": { ... }
}
```

---

## How Claude Uses These Files

### Discovery Phase
When user mentions a firm name:
```
User: "I'm with Topstep"
Claude: [Reads firm_rules/topstep.json]
```

### Validation Phase
When validating strategy against firm rules:
```javascript
// Example validation logic
const firmRules = readFirmRules(firm_slug);
const userContracts = 5;
const firmMaxContracts = firmRules.rules[accountSize].max_contracts.ES;

if (userContracts > firmMaxContracts) {
  WARNING: "Exceeds contract limit"
}
```

### Automation Check
Before allowing automation:
```javascript
if (firmRules.automation_policy === "prohibited") {
  ERROR: "This firm does not allow automated trading"
}
```

---

## Update Process

### When to Update

1. **Quarterly Review** - Check all firms every 3 months
2. **Policy Changes** - Update immediately when firms announce changes
3. **User Reports** - If users report rule discrepancies
4. **New Firms** - Add new automation-friendly firms as they emerge

### How to Update

1. **Visit Firm Website** - Check official rules page
2. **Verify Automation Policy** - Look for explicit statements
3. **Update JSON File** - Modify relevant fields
4. **Update `last_verified` Field** - Set to current date
5. **Test Validation** - Ensure Claude can read and use updated rules
6. **Commit Changes** - Version control for audit trail

### Update Checklist

- [ ] Profit targets still accurate?
- [ ] Drawdown limits unchanged?
- [ ] Contract limits current?
- [ ] Automation policy still the same?
- [ ] Payout structure updated?
- [ ] New restrictions added?
- [ ] Trustpilot rating current?
- [ ] `last_verified` date updated?

---

## Adding New Firms

To add a new automation-friendly firm:

1. **Create JSON file:** `firm-slug.json`
2. **Follow schema structure** (see above)
3. **Research thoroughly:**
   - Official rules page
   - Terms of service
   - Automation policy statement
   - Trustpilot/reviews
   - Community discussions
4. **Verify automation policy** - Look for explicit statements
5. **Set initial `last_verified` date**
6. **Update this README** with firm details
7. **Test with Claude** - Ensure proper loading

---

## Firms NOT Included (Prohibited Automation)

These firms **prohibit** automated trading and are NOT included in this directory:

### Apex Trader Funding ❌
- **Policy:** "The use of automation is strictly prohibited on PA and Live accounts"
- **Why Not Included:** PropTraderAI focuses on automation-friendly firms
- **Note:** Despite being very popular, explicit prohibition makes them incompatible

### Take Profit Trader ❌
- **Policy:** "We do not allow any automated or bot trading of any kind"
- **Why Not Included:** All trades must be manually executed
- **Note:** Clear prohibition statement

**Should we include these for reference?**

If you want to warn users about prohibited firms, we could add them with:
```json
{
  "automation_policy": "prohibited",
  "automation_notes": "AUTOMATION NOT ALLOWED - included for reference only"
}
```

This would allow Claude to say: "Apex does not allow automation. Consider these alternatives instead: [list of allowed firms]"

---

## Data Sources

Firm rules are compiled from:

1. **Official Websites** - Primary source
2. **Terms of Service** - Legal documentation
3. **TradersPost Integration List** - Verified integrations
4. **Community Knowledge** - Verified trader reports
5. **Direct Contact** - Email verification when unclear

---

## Relationship to MCP Server (PATH 3)

These static firm rules serve as:

1. **Phase 1A (Current)**: Primary data source for strategy validation
2. **Phase 3+ (Future)**: Fallback when MCP server unavailable
3. **Testing**: Offline reference for development and testing

### How It Works

Once the PropTraderAI MCP server is live (PATH 3), the skill will:

1. **Check if MCP server is available**
   - Attempt to call `get_firm_rules(firm_name)`
   - If successful, use real-time data
   
2. **Use MCP for real-time data** (when available)
   - Current challenge status (user's P&L, drawdown %)
   - Latest promo codes and discounts
   - Firm policy updates (like MyFundedFutures July 2025 automation policy)
   - Contract limit increases based on profit milestones
   
3. **Fall back to Level 3 resources** (if MCP unavailable)
   - Read static JSON files from this directory
   - Use offline validation
   - Warn user that real-time data unavailable

### Why This Architecture

✅ **Reliability**: Skill works even if MCP server is down  
✅ **Performance**: No network latency for static rules  
✅ **Offline Support**: Can test/develop without API access  
✅ **Graceful Degradation**: Never fails completely  

**Example Flow:**
```
User: "I'm with Topstep"

Skill Logic:
1. Try: MCP.get_firm_rules("topstep")
   → Success: Use real-time data + user's challenge status
   → Fail: Read firm_rules/topstep.json (static fallback)
   
2. Validate strategy against firm rules
3. Proceed with strategy extraction
```

This ensures the skill works reliably in all scenarios.

---

## Limitations & Disclaimers

### What This Database Covers
✅ Static firm rules (profit targets, drawdown limits)  
✅ Automation policies (allowed/prohibited)  
✅ Contract limits by instrument  
✅ General payout structures  

### What This Database Does NOT Cover
❌ Real-time account balances  
❌ User-specific challenge status  
❌ Dynamic rule changes (updated quarterly, not real-time)  
❌ Promo codes or current discounts  

### Important Notes

- **Verify Before Trading:** Always check the firm's official website for current rules
- **Rules Change:** Firms can update policies at any time
- **No Guarantees:** This database is for reference only
- **API is Primary:** These files are fallback data; PropTraderAI's API provides real-time info
- **User Responsibility:** Traders must verify automation compliance with their specific firm

---

## Maintenance Schedule

| Frequency | Task |
|-----------|------|
| **Monthly** | Check for major policy announcements |
| **Quarterly** | Full review of all 6 firms |
| **On Demand** | Update when users report discrepancies |
| **Annually** | Comprehensive audit and cleanup |

**Next Scheduled Review:** April 10, 2026

---

## Contact & Contributions

**Questions about firm rules?**
- Check firm's official website first
- Contact the firm directly for clarification
- Report discrepancies to PropTraderAI support

**Found outdated information?**
- Note which firm and what changed
- Include source (URL) for verification
- Submit update request with `last_verified` date

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| **1.0** | 2026-01-10 | Initial release with 6 automation-friendly firms |

---

## Quick Reference: Automation Policies

| Firm | Policy | Key Restriction |
|------|--------|-----------------|
| **Topstep** | ✅ Allowed | No VPS/VPN |
| **MyFundedFutures** | ✅ Allowed | No HFT (>200 trades/day) |
| **Tradeify** | ✅ Allowed | Ownership verification required |
| **Alpha Futures** | ✅ Allowed | Standard restrictions |
| **FTMO** | ✅ Allowed | Standard restrictions |
| **FundedNext** | ✅ Allowed | Standard restrictions |

**Standard Restrictions** = No HFT, no exploitation of sim environment, must comply with all other firm rules.

---

**For more information on prop firm integration, see:**
- `../SKILL.md` - Main skill file with conversation framework
- `../schemas/` - JSON schemas for validation
- PropTraderAI API documentation (when available)
