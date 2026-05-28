---
name: agent-browser
description: Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, test web applications, or extract information from web pages.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# Browser Automation with agent-browser

## Quick start

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Core workflow

1. Navigate: `agent-browser open <url>`
2. Snapshot: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes

## Commands

### Navigation
```bash
agent-browser open <url>      # Navigate to URL
agent-browser back            # Go back
agent-browser forward         # Go forward  
agent-browser reload          # Reload page
agent-browser close           # Close browser
```

### Snapshot (page analysis)
```bash
agent-browser snapshot        # Full accessibility tree
agent-browser snapshot -i     # Interactive elements only (recommended)
agent-browser snapshot -c     # Compact output
agent-browser snapshot -d 3   # Limit depth to 3
```

### Interactions (use @refs from snapshot)
```bash
agent-browser click @e1           # Click
agent-browser dblclick @e1        # Double-click
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter         # Press key
agent-browser press Control+a     # Key combination
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown
agent-browser scroll down 500     # Scroll page
agent-browser scrollintoview @e1  # Scroll element into view
```

### Get information
```bash
agent-browser get text @e1        # Get element text
agent-browser get value @e1       # Get input value
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
```

### Screenshots
```bash
agent-browser screenshot          # Screenshot to stdout
agent-browser screenshot path.png # Save to file
agent-browser screenshot --full   # Full page
```

### Wait
```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait milliseconds
agent-browser wait --text "Success"        # Wait for text
agent-browser wait --load networkidle      # Wait for network idle
```

### Semantic locators (alternative to refs)
```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
```

## Example: Form submission

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output shows: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## Example: Authentication with saved state

```bash
# Login once
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Later sessions: load saved state
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## Sessions (parallel browsers)

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

## JSON output (for parsing)

Add `--json` for machine-readable output:
```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

## Debugging

```bash
agent-browser open example.com --headed  # Show browser window
agent-browser console                    # View console messages
agent-browser errors                     # View page errors
```

---

## Web3 Testing (Anchor Integration)

For Web3 dApps, agent-browser integrates with **Anchor** to provide wallet mocking and contract state injection.

### Prerequisites

```bash
# Anchor must be installed
anchor --version

# Create a development session with Anvil fork
anchor session create --network mainnet --block 18500000
anchor fork create --session <id> --rpc-url $ETH_RPC_URL
```

### Web3 Mock Mode

Launch browser with mock wallet state:

```bash
# Basic mock - inject address and balance
agent-browser open http://localhost:3000 --web3-mock \
  --address 0x1234...abcd \
  --balance 1000000000000000000

# Full mock with contract reads
agent-browser open http://localhost:3000 --web3-mock \
  --address 0x1234...abcd \
  --balance 1eth \
  --mock-reads mock-state.json
```

### Mock State File Format

Create `mock-state.json` for complex contract mocking:

```json
{
  "wallet": {
    "address": "0x1234567890abcdef1234567890abcdef12345678",
    "balance": "1000000000000000000",
    "chainId": 1
  },
  "contracts": {
    "0xVaultAddress": {
      "balanceOf(address)": {
        "0x1234...": "500000000000000000"
      },
      "totalSupply()": "10000000000000000000000"
    }
  },
  "badges": {
    "count": 5,
    "rebatePercentage": 1666
  }
}
```

### Anchor Fork Integration

Use Anchor to manage blockchain state for testing:

```bash
# 1. Create fork at specific block
anchor fork create --session dev --rpc-url $ETH_RPC_URL --block 18500000

# 2. Save current state as snapshot
anchor snapshot create <fork-id>

# 3. Open browser against fork RPC
agent-browser open http://localhost:3000 --web3-mock \
  --rpc-url http://localhost:8545 \
  --address 0x1234...

# 4. Take screenshot for PR documentation
agent-browser screenshot rewards-card.png

# 5. Revert to snapshot for next test
anchor snapshot revert <snapshot-id>
```

### Transaction Flow Testing

Test pessimistic sync flows without real transactions:

```bash
# Mock pending state
agent-browser open http://localhost:3000 --web3-mock \
  --address 0x1234... \
  --tx-state pending

# Take screenshot of pending UI
agent-browser screenshot claim-pending.png

# Mock success state
agent-browser open http://localhost:3000 --web3-mock \
  --address 0x1234... \
  --tx-state success \
  --tx-hash 0xabc...

# Take screenshot of success UI
agent-browser screenshot claim-success.png
```

### Example: Screenshot Wallet-Dependent Component

```bash
# 1. Setup Anchor fork
anchor session create --network mainnet --block latest
anchor fork create --session dev --rpc-url $ETH_RPC_URL

# 2. Open app with mocked wallet
agent-browser open http://localhost:3000/rewards --web3-mock \
  --address 0x1234567890abcdef1234567890abcdef12345678 \
  --balance 10eth \
  --mock-reads ./test-fixtures/rewards-state.json

# 3. Wait for component to render
agent-browser wait --text "Fee Rebate"
agent-browser wait 500  # Allow animations

# 4. Screenshot the component
agent-browser screenshot pr-assets/rewards-card.png

# 5. Cleanup
agent-browser close
anchor fork kill <fork-id>
```

### Environment Variables

```bash
# Set defaults for Web3 testing
export ANCHOR_SESSION_ID=dev
export WEB3_MOCK_ADDRESS=0x1234...
export WEB3_MOCK_RPC=http://localhost:8545
```

### Limitations

- Mock state is injected via localStorage/window, not actual chain
- Complex contract interactions may need Anchor fork with actual state
- Transaction signing still requires mock connector setup in app
