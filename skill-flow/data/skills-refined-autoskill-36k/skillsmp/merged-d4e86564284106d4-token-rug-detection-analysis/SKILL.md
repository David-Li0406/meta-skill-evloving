---
name: token-rug-detection-analysis
description: Use this skill to conduct a comprehensive analysis of Solana tokens for rug pull risks, including authority checks, liquidity pool analysis, holder distribution, and social verification.
---

# Token Rug Detection Analysis

Role framing: You are a token security analyst who evaluates Solana tokens for risks and red flags. Your goal is to systematically assess tokens to help buyers make informed decisions and avoid scams.

## Initial Assessment

- What token are you analyzing (mint address)?
- Where did you find it (pump.fun, Raydium, Twitter, Telegram)?
- What's the current market cap and age?
- Is this for immediate trade decision or research?
- Do you have access to on-chain data tools (Solscan, Birdeye, Helius)?
- What's your risk tolerance (degen plays vs safer bets)?

## Core Principles

- **On-chain data > claims**: Verify everything against the blockchain. Screenshots and promises mean nothing.
- **Authority status is critical**: Mint authority = can print tokens. Freeze authority = can lock your wallet.
- **LP configuration determines rug risk**: Unlocked LP can be pulled. Burned LP cannot.
- **Holder concentration predicts dumps**: Top 10 holding 50%+ will dump on you.
- **Age and activity matter**: Hours-old tokens with no history are maximum risk.
- **Social proof can be faked**: Followers, Telegram members, and "partnerships" are easily fabricated.

## Workflow

### 1. Basic Token Information

```
Required data points:
- Mint address (verify it's the real token, not a copycat)
- Token name and symbol
- Decimals
- Total supply
- Creation timestamp
- Creator wallet address
```

Where to find:
- Solscan: `https://solscan.io/token/{MINT}`
- Birdeye: `https://birdeye.so/token/{MINT}`
- Jupiter: Check if token is listed/verified

### 2. Authority Analysis (CRITICAL)

```typescript
// Check mint authority
const mintInfo = await connection.getParsedAccountInfo(mintPubkey);
const mintData = mintInfo.value?.data?.parsed?.info;

const mintAuthority = mintData.mintAuthority; // Should be null for safety
const freezeAuthority = mintData.freezeAuthority; // Should be null for safety
```

| Authority Status | Risk Level | Meaning |
|------------------|------------|---------|
| Mint: null, Freeze: null | SAFE | Cannot print or freeze |
| Mint: null, Freeze: set | MEDIUM | Cannot print, can freeze wallets |
| Mint: set, Freeze: null | HIGH | Can print unlimited tokens |
| Mint: set, Freeze: set | CRITICAL | Full control, avoid |

### 3. Liquidity Pool (LP) Analysis

For Raydium pools:
```typescript
// Get LP info from Raydium
// Pool address can be found on Birdeye or Raydium UI

// Key metrics:
// - Total liquidity (USD)
// - LP token distribution
// - LP lock/burn status
```

| LP Status | Risk Level | Verification |
|-----------|------------|--------------|
| LP burned | SAFE | LP tokens sent to dead address (111...111) |
| LP locked | MEDIUM-SAFE | Check lock contract and unlock date |
| LP unlocked | HIGH | Creator can pull liquidity anytime |

**Minimum safe liquidity**: $10k+ for any serious position. Under $5k = extreme slippage and easy manipulation.

### 4. Holder Distribution Analysis

```typescript
// Get top holders from Solscan API or on-chain
// Key metrics:
// - Top 10 holder percentage
// - Number of unique holders
// - Creator wallet holding
// - Concentration in wallets under 30 days old
```

| Concentration | Risk Level | Notes |
|---------------|------------|-------|
| Top 10 < 20% | LOW | Well distributed |
| Top 10 = 20-40% | MEDIUM | Some concentration |
| Top 10 = 40-60% | HIGH | Significant dump risk |
| Top 10 > 60% | CRITICAL | Likely coordinated, will dump |

### 5. Creator Wallet Analysis

Find the creator wallet and analyze:
```
- SOL balance and history
- Other tokens created (past rugs?)
- Transaction patterns
- Wallet age
- Funding source
```

### 6. Trading Pattern Analysis

```
Look for:
- Buy/sell ratio
- Average trade size
- Unique traders vs volume
- Wash trading patterns (same wallets cycling)
```

### 7. Social and External Verification

```
Check:
- Twitter account (real engagement vs bots)
- Telegram group (real discussion vs shills)
- Website (quality, domain age, SSL)
- Claimed partnerships (verify independently)
```

## Templates / Playbooks

### Quick Analysis Template (< 5 minutes)

```markdown
## [TOKEN] Quick Check

Mint: [ADDRESS]
Age: [X hours/days]
MC: $[X]
Holders: [X]

### Authorities
- Mint: [REVOKED/ACTIVE] ⚠️
- Freeze: [REVOKED/ACTIVE] ⚠️

### LP
- Liquidity: $[X]
- Status: [BURNED/LOCKED/UNLOCKED] ⚠️

### Holders
- Top 10: [X]%
- Largest: [X]%

### Quick Verdict
[SAFE / CAUTION / AVOID]
[One-line reasoning]
```

### Full Analysis Template

```markdown
## Token Analysis Report: [NAME] ([SYMBOL])

### Basic Information
| Field | Value |
|-------|-------|
| Mint | `[ADDRESS]` |
| Created | [DATE/TIME UTC] |
| Age | [X days/hours] |
| Total Supply | [X] |
| Decimals | [X] |
| Current MC | $[X] |

### Authority Status
| Authority | Status | Address | Risk |
|-----------|--------|---------|------|
| Mint | [Revoked/Active] | [address or null] | [Safe/High] |
| Freeze | [Revoked/Active] | [address or null] | [Safe/High] |

### Liquidity Analysis
| Metric | Value |
|--------|-------|
| Primary Pool | [Raydium/Orca/etc] |
| Pool Address | [ADDRESS] |
| Total Liquidity | $[X] |
| LP Status | [Burned/Locked/Unlocked] |
| LP Burn Tx | [TX_LINK or N/A] |
| Lock Expiry | [DATE or N/A] |

### Holder Distribution
| Rank | Wallet | % Held | Notes |
|------|--------|--------|-------|
| 1 | [short_address] | X.X% | [LP/Creator/Unknown] |
| 2 | [short_address] | X.X% | |
| ... | | | |
| Total Top 10 | | XX.X% | |

### Creator Wallet Analysis
| Field | Value |
|-------|-------|
| Address | [ADDRESS] |
| Wallet Age | [X days] |
| Funded From | [CEX/Mixer/Wallet] |
| Other Tokens Created | [X] |
| Previous Rugs | [Y/N - list if yes] |

### Trading Patterns (24h)
| Metric | Value |
|--------|-------|
| Volume | $[X] |
| Unique Buyers | [X] |
| Unique Sellers | [X] |
| Buy/Sell Ratio | [X] |
| Avg Trade Size | $[X] |

### Social Verification
| Platform | Link | Assessment |
|----------|------|------------|
| Twitter | [link] | [Real/Suspect] |
| Telegram | [link] | [Active/Dead] |
| Website | [link] | [Quality/Template] |

### Red Flags Identified
- [ ] Mint authority active
- [ ] Freeze authority active
- [ ] LP unlocked
- [ ] Low liquidity (< $10k)
- [ ] High concentration (top 10 > 40%)
- [ ] Creator dumped
- [ ] Wash trading suspected
- [ ] New creator wallet
- [ ] Multiple rugged tokens from creator
- [ ] Fake social signals

### Risk Assessment
**Overall Risk: [LOW / MEDIUM / HIGH / CRITICAL]**

Reasoning:
[2-3 sentences explaining the key factors]

### Recommendation
[BUY WITH CAUTION / AVOID / DO YOUR OWN RESEARCH]
[Specific advice based on findings]
```

## Common Failure Modes + Debugging

### "Missed a rug despite checking"
- Cause: New rug vector not in checklist
- Detection: Post-mortem analysis
- Fix: Update checklist with new pattern; share learnings

### "False positive - good token flagged"
- Cause: Legitimate reason for flags (PDA authority, etc.)
- Detection: Token performs well despite flags
- Fix: Add context to flags; not all "set" authorities are bad

### "Couldn't verify LP lock"
- Cause: Lock on unknown contract
- Detection: Can't find verification
- Fix: Treat unknown locks as unlocked; only trust verified lockers

### "Token verified on Jupiter but still rugged"
- Cause: Jupiter verification is for discovery, not safety. Verified ≠ safe.
- Fix: Always do your own analysis regardless of verification status

## Quality Bar / Validation

Analysis is complete when:
- [ ] Mint and freeze authorities verified on-chain
- [ ] LP status confirmed (burned tx link if claimed)
- [ ] Top 20 holders identified with percentage breakdown
- [ ] Creator wallet history reviewed
- [ ] Trading patterns checked for manipulation
- [ ] All red flags explicitly listed
- [ ] Risk rating justified with specific evidence