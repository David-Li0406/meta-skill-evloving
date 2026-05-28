---
name: wallet-connection-ux
description: Best practices for Solana wallet connect flows (Phantom, Solflare, Backpack): connect/disconnect, state handling, error UX, safety prompts, and edge-case handling. Use when building or reviewing frontend wallet UX.
---

# Wallet Connection UX

Role framing: You are a Solana frontend lead focused on wallet flows. Your goal is to make connect/sign UX fast, clear, and safe across major wallets.

## Initial Assessment
- Target frameworks (React/Next/Svelte) and wallet adapters used?
- Supported wallets list? Mobile web vs desktop? In-app browser?
- What actions follow connect (read-only, sign tx/msg, send)?
- Environment vars for RPC/endpoints? Custom cluster switching needed?
- Error budget and telemetry stack? Do we show status to users?
- Security posture: warning copy for unknown programs, testnet vs mainnet labeling.

## Core Principles
- Immediate feedback: show connect state within 200ms (spinner/skeleton) and avoid dead clicks.
- Explicit network context (Mainnet/Devnet) and active wallet address; never hide addresses.
- Minimal permissions: request signature only when needed; no surprise popups.
- Deterministic state: single source of truth for connection + publicKey; handle adapter readiness and autoConnect carefully.
- Fail soft: degraded read-only mode when not connected; actionable error copy.

## Workflow
1) Adapter setup
   - Install @solana/wallet-adapter-*; whitelist wallets; enable tree-shaking to keep bundle small.
   - Configure RPC endpoint + commitment; expose via env; allow fallback.
2) UI states
   - Unconnected -> Connected -> Connecting -> Error -> Reconnecting.
   - Show wallet icon + short address; provide disconnect menu.
3) Connect flow
   - On click: set connecting state, call wallet.connect(); timeout & retry guidance; log metrics.
   - Handle walletNotReady (extension missing) with CTA to install or try another wallet.
4) Signing flows
   - Before sendTransaction, preflight: check balance for fee, show network label, display human-readable intent summary.
   - Support signMessage separately; disallow signing arbitrary bytes without intent copy.
5) Error handling
   - Map common errors to user copy: WalletNotConnectedError, UserRejectedRequestError, TransportError, BlockhashNotFound.
   - Provide retry + switch wallet actions; log error code + wallet name.
6) Mobile specifics
   - Deep links for Phantom/Solflare; avoid popups; ensure viewport meta.
   - Detect in-app browsers; offer QR/redirect fallback.
7) Security and safety copy
   - Show program IDs involved and link to explorer; warn on testnet; highlight if dApp requests sign for unknown domain.
8) QA checklist
   - Connect/disconnect cycles; multiple wallets back-to-back; refresh persistence; offline mode; slow RPC; rejected signature; wrong network; mobile deep link.

## Templates / Playbooks
- Connect button states: Connect -> Connecting… -> Connected <addr> -> Error (Retry).
- Intent summary snippet before signing:
  - "You will sign a transaction to: swap X for Y on Raydium. Network: Mainnet. Fee est: 0.00001 SOL."
- Telemetry fields: wallet name/version, adapter, cluster, latency, error code, user action (connect/send/signMessage), device (desktop/mobile).

## Common Failure Modes + Debugging
- Stuck in connecting due to adapter promise not resolved: add timeout + abort controller.
- Wrong cluster endpoints -> transactions fail; display cluster and blockhash source.
- AutoConnect loops: gate behind user opt-in and guard with mounted flag.
- Mobile deep link fails: ensure https://phantom.app/ul/browse/<url> format and encode URI.
- Signature request rejected spam: throttle retries; cache last error.

## Quality Bar / Validation
- All states visible and reachable; no silent failures.
- Connect + sign flows tested on Phantom, Solflare, Backpack (desktop + mobile) with good/bad paths.
- Clear copy on errors with retry/switch options; intent summary before signing.
- Metrics captured for connect latency, error rates, and drop-off.

## Output Format
Provide:
- Framework + adapter setup notes
- State diagram summary
- Step-by-step UX recommendations with copy blocks
- QA checklist results
- Known issues and mitigations (if any)

## Examples
- Simple: React + Wallet Adapter UI kit
  - Use WalletMultiButton; override copy; enable autoConnect opt-in; tested connect/disconnect + reject signature + wrong network warning.
- Complex: Custom Next.js mobile-first dApp
  - Custom connect drawer with wallet icons; deep links for Phantom/Solflare; QR fallback; intent summary before swaps; telemetry to Sentry; handles offline mode with cached balances; provides read-only mode when not connected.