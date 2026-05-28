# Smart Contract Security Checklists

Comprehensive checklists for secure Solidity development. Use these during code review, before deployment, and as part of your testing workflow.

---

## Pre-Implementation Checklist

Before writing code, confirm:

- [ ] **Requirements clear**: Functional spec, roles, trust assumptions documented
- [ ] **Standards identified**: ERC20/721/1155/4626/2771 or custom
- [ ] **Chain target**: Mainnet, L2, specific EVM quirks (e.g., no PUSH0 on some chains)
- [ ] **Compiler version**: Pinned version, optimizer settings decided
- [ ] **Upgradeability decision**: Immutable vs proxy pattern chosen with rationale
- [ ] **Dependencies reviewed**: OpenZeppelin version, other libs audited

---

## Verification Checklist (Post-Implementation)

Run through after every feature/bugfix:

### Security

- [ ] **Reentrancy / external call safety reviewed**
  - CEI pattern followed
  - ReentrancyGuard on state-changing + external call functions
  - No callbacks to untrusted contracts mid-state-change

- [ ] **Access control correct + least privilege**
  - All privileged functions gated
  - Role hierarchy makes sense
  - No leftover `public` that should be `internal`/`private`

- [ ] **Accounting invariants preserved**
  - `sum(balances) == totalSupply` (or equivalent)
  - No phantom mints/burns
  - Fee calculations don't break invariants

- [ ] **Input validation complete**
  - Zero address checks where needed
  - Array length bounds
  - Amount > 0 where required

### Events & Errors

- [ ] **Events emitted for state changes**
  - All storage mutations have corresponding events
  - Events include old + new values for updates
  - Indexed parameters for filtering

- [ ] **Revert reasons consistent**
  - Custom errors preferred over strings
  - Error names descriptive (`InsufficientBalance`, not `Error1`)
  - All revert paths have reasons

### Upgradeability (if applicable)

- [ ] **No constructors in implementation**
  - Using `initializer` modifier
  - `_disableInitializers()` in constructor

- [ ] **Storage layout safe**
  - Append-only additions
  - No type changes to existing slots
  - Storage gaps for future versions (`uint256[50] private __gap`)

- [ ] **Upgrade authorization explicit**
  - `_authorizeUpgrade` properly restricted
  - Timelock or multisig for upgrades

### Code Quality

- [ ] **Lint/format OK** (`forge fmt`, `solhint`)
- [ ] **NatSpec complete** for external/public functions
- [ ] **Gas considerations reviewed** (see Gas Checklist below)
- [ ] **No compiler warnings**

---

## Secure Coding Checklist

Reference while writing code:

### Access Control & Authentication

| Check | Status |
|-------|--------|
| All privileged functions gated (Ownable/AccessControl/custom) | ☐ |
| Admin flows explicit (2-step ownership transfer preferred) | ☐ |
| No `tx.origin` usage | ☐ |
| Allowlists justified if used | ☐ |

### Signature Verification

| Check | Status |
|-------|--------|
| EIP-712 domain separator includes chainId | ☐ |
| Nonce handling prevents replay | ☐ |
| Deadline/expiry enforced | ☐ |
| `ecrecover` returns checked against zero | ☐ |
| Using OpenZeppelin ECDSA or SignatureChecker | ☐ |

### Accounting & Precision

| Check | Status |
|-------|--------|
| No under/overflow in custom math (Solidity ^0.8 helps) | ☐ |
| Fee-on-transfer tokens handled if accepting arbitrary ERC20s | ☐ |
| Rebasing tokens handled or explicitly unsupported | ☐ |
| Rounding direction explicit (favor protocol or user?) | ☐ |
| Decimal normalization correct (18 vs 6 vs 8) | ☐ |

### External Calls

| Check | Status |
|-------|--------|
| No unbounded loops with external calls | ☐ |
| Pull payments preferred over push | ☐ |
| If push: failure handled (try/catch or continue) | ☐ |
| Low-level calls check return value | ☐ |
| `delegatecall` target is trusted/immutable | ☐ |

### Oracle & Price Data

| Check | Status |
|-------|--------|
| Staleness check on oracle data | ☐ |
| Price bounds / sanity checks | ☐ |
| Decimal handling explicit | ☐ |
| Fallback oracle or circuit breaker | ☐ |
| TWAP or manipulation resistance if needed | ☐ |

### Time-Based Logic

| Check | Status |
|-------|--------|
| No exact `block.timestamp` comparisons (use `>=`, `<=`) | ☐ |
| Tolerance for minor timestamp drift | ☐ |
| No reliance on `block.number` for time (L2s vary) | ☐ |

### Token Integrations

| Check | Status |
|-------|--------|
| SafeERC20 used for transfers | ☐ |
| Return values checked (or using SafeERC20) | ☐ |
| Approval race condition mitigated | ☐ |
| ERC721/1155 receiver hooks considered | ☐ |

---

## Gas Optimization Checklist

**Only after correctness is verified:**

| Optimization | Status |
|--------------|--------|
| Storage reads cached in memory variables | ☐ |
| Storage writes minimized (batch updates) | ☐ |
| Struct packing optimized (smaller types together) | ☐ |
| `calldata` instead of `memory` for read-only arrays | ☐ |
| Custom errors instead of revert strings | ☐ |
| `unchecked` blocks where overflow impossible | ☐ |
| No redundant SLOAD (same slot read twice) | ☐ |
| Loops bounded and gas-conscious | ☐ |
| Events use indexed params efficiently (max 3) | ☐ |

---

## Pre-Deployment Checklist

Before mainnet deployment:

### Code

- [ ] All tests passing (`forge test`)
- [ ] Coverage acceptable (`forge coverage`)
- [ ] Static analysis clean (`slither .`)
- [ ] Formal verification (if applicable)
- [ ] External audit complete (for significant value)

### Configuration

- [ ] Constructor/initializer arguments verified
- [ ] Admin addresses are multisig/timelock (not EOA)
- [ ] Fee parameters within expected bounds
- [ ] Oracle addresses correct for target chain

### Deployment

- [ ] Deployment script tested on fork
- [ ] Contract verification ready (Etherscan API key)
- [ ] Post-deployment verification script ready
- [ ] Monitoring/alerting configured
- [ ] Incident response plan documented

---

## Test Coverage Checklist

For each feature, ensure:

| Test Type | Coverage |
|-----------|----------|
| Happy path (normal operation) | ☐ |
| Boundary conditions (0, 1, max) | ☐ |
| Revert cases (all require/revert paths) | ☐ |
| Access control (unauthorized callers) | ☐ |
| Reentrancy attempts | ☐ |
| Invariant/property tests | ☐ |
| Fuzz tests (amounts, addresses, ordering) | ☐ |
| Fork tests (mainnet state) | ☐ |
| Gas snapshots (regression detection) | ☐ |

---

## Quick Reference: Common Vulnerabilities

| Vulnerability | Mitigation |
|---------------|------------|
| Reentrancy | CEI pattern + ReentrancyGuard |
| Access control bypass | Consistent modifier usage |
| Integer overflow | Solidity ^0.8 + logic review |
| Oracle manipulation | TWAP, bounds, staleness checks |
| Front-running | Commit-reveal, private mempools |
| Signature replay | Nonces, deadlines, chainId |
| Proxy storage collision | Storage gaps, ERC-7201 namespaces |
| Denial of service | Bounded loops, pull payments |
| Precision loss | Explicit rounding, scale factors |
| Unchecked return values | SafeERC20, explicit checks |
