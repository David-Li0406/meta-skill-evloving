# Security & Safety (Web3)

## Table of Contents

1. [Input Validation](#input-validation)
2. [Address Handling](#address-handling)
3. [Numeric Safety](#numeric-safety)
4. [Transaction Safety](#transaction-safety)
5. [Display Safety](#display-safety)
6. [State & Storage Security](#state--storage-security)
7. [Error Handling](#error-handling)
8. [Logging](#logging)

---

## Input Validation

### Always Use Zod

Validate all user input at the boundary—forms, URL params, API responses.

```tsx
import { z } from 'zod'
import { isAddress } from 'ethers'

// Schema with custom refinements
const transferSchema = z.object({
  recipient: z.string().refine(isAddress, 'Invalid address'),
  amount: z
    .string()
    .min(1, 'Amount required')
    .refine(val => {
      try {
        return BigInt(val) > 0n
      } catch {
        return false
      }
    }, 'Invalid amount'),
  memo: z.string().max(256, 'Memo too long').optional(),
})
```

### Validate API Responses

Never trust external data. Validate responses before use.

```tsx
const orderResponseSchema = z.object({
  id: z.string(),
  status: z.enum(['pending', 'filled', 'cancelled']),
  amount: z.string(),
  price: z.string(),
  timestamp: z.number(),
})

async function fetchOrder(id: string) {
  const response = await api.get(`/orders/${id}`)
  return orderResponseSchema.parse(response.data) // Throws if invalid
}
```

### Never Infer Intent

Do not infer user actions from URL, props, or stored values. Always require explicit confirmation.

```tsx
// BAD: Auto-executing based on URL params
useEffect(() => {
  const action = searchParams.get('action')
  if (action === 'approve') {
    executeApproval() // Dangerous!
  }
}, [searchParams])

// GOOD: Show confirmation, require explicit action
function ApprovalPage() {
  const action = searchParams.get('action')

  if (action === 'approve') {
    return (
      <ConfirmationDialog
        title="Confirm Approval"
        description="You are about to approve this transaction"
        onConfirm={executeApproval}
        onCancel={() => navigate('/')}
      />
    )
  }
}
```

---

## Address Handling

### Validation

Use chain utilities, never regex.

```tsx
import { isAddress, getAddress } from 'ethers'

// Validate
if (!isAddress(input)) {
  throw new Error('Invalid address')
}

// Normalize to checksum format
const checksumAddress = getAddress(input)
```

### Comparison

Always normalize before comparing.

```tsx
// BAD: Case-sensitive comparison may fail
if (address1 === address2) {
}

// GOOD: Normalize both addresses
if (getAddress(address1) === getAddress(address2)) {
}

// Or use lowercase for comparison
if (address1.toLowerCase() === address2.toLowerCase()) {
}
```

### Display

Truncate only when the full address is accessible.

```tsx
interface AddressDisplayProps {
  address: string
  truncate?: boolean
}

function AddressDisplay({ address, truncate = true }: AddressDisplayProps) {
  const checksumAddress = getAddress(address)
  const displayAddress = truncate
    ? `${checksumAddress.slice(0, 6)}...${checksumAddress.slice(-4)}`
    : checksumAddress

  return (
    <Tooltip content={checksumAddress}>
      <button onClick={() => navigator.clipboard.writeText(checksumAddress)} className="font-mono">
        {displayAddress}
      </button>
    </Tooltip>
  )
}
```

### User-Owned Address Verification

When displaying "your address" or taking actions on behalf of users, verify ownership.

```tsx
// BAD: Trusting address from props/URL
function UserDashboard({ address }: { address: string }) {
  return <WalletBalance address={address} />
}

// GOOD: Use connected wallet address
function UserDashboard() {
  const { address } = useAccount() // From wallet connection

  if (!address) return <ConnectWallet />

  return <WalletBalance address={address} />
}
```

---

## Numeric Safety

### Never Use `number` for Token Math

JavaScript `number` loses precision beyond 2^53. Token amounts can exceed this.

```tsx
// BAD: Precision loss
const amount = 1000000000000000000 // 1 ETH in wei - WRONG
const total = amount * 2 // Precision lost

// GOOD: Use BigInt
const amount = 1000000000000000000n // 1 ETH in wei
const total = amount * 2n // Correct

// GOOD: Use string for serialization
const amountStr = '1000000000000000000'
const amount = BigInt(amountStr)
```

### Decimal Handling

Use ethers utilities for human-readable conversions.

```tsx
import { parseUnits, formatUnits } from 'ethers'

// User input (string) -> BigInt (wei)
const weiAmount = parseUnits(userInput, 18) // "1.5" -> 1500000000000000000n

// BigInt (wei) -> Display string
const displayAmount = formatUnits(weiAmount, 18) // -> "1.5"

// With custom decimals (e.g., USDC has 6)
const usdcAmount = parseUnits('100', 6) // 100000000n
```

### Safe Arithmetic

Guard against overflow and division by zero.

```tsx
function calculatePercentage(value: bigint, total: bigint): number {
  if (total === 0n) return 0

  // Multiply first to maintain precision, then convert
  const scaled = (value * 10000n) / total
  return Number(scaled) / 100
}

function safeMultiply(a: bigint, b: bigint, decimals: number): bigint {
  const scale = 10n ** BigInt(decimals)
  return (a * b) / scale
}
```

### Display Formatting

Format large numbers for readability.

```tsx
function formatTokenAmount(amount: bigint, decimals: number, maxDecimals = 4): string {
  const formatted = formatUnits(amount, decimals)
  const [whole, fraction = ''] = formatted.split('.')

  // Truncate decimals for display
  const truncatedFraction = fraction.slice(0, maxDecimals)

  // Add thousand separators
  const formattedWhole = Number(whole).toLocaleString()

  return truncatedFraction ? `${formattedWhole}.${truncatedFraction}` : formattedWhole
}
```

---

## Transaction Safety

### Confirmation Dialogs

Always confirm before signing or submitting transactions.

```tsx
interface TransactionConfirmProps {
  action: string
  details: {
    label: string
    value: string
  }[]
  onConfirm: () => Promise<void>
  onCancel: () => void
}

function TransactionConfirm({ action, details, onConfirm, onCancel }: TransactionConfirmProps) {
  // Use the useTransaction hook (defined below) for consistent state handling
  const { execute, isPending } = useTransaction(onConfirm)

  const handleConfirm = async () => {
    try {
      await execute()
    } catch {
      // Error is already handled by the hook
    }
  }

  return (
    <Dialog open onOpenChange={open => !open && onCancel()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Confirm {action}</DialogTitle>
        </DialogHeader>

        <div className="space-y-2">
          {details.map(({ label, value }) => (
            <div key={label} className="flex justify-between">
              <span className="text-muted-foreground">{label}</span>
              <span className="font-mono">{value}</span>
            </div>
          ))}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onCancel} disabled={isPending}>
            Cancel
          </Button>
          <Button onClick={handleConfirm} disabled={isPending}>
            {isPending ? 'Confirming...' : 'Confirm'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

### Prevent Double Submission

Disable UI and guard against duplicate actions.

```tsx
function useTransaction<T>(executeFn: () => Promise<T>) {
  const [state, setState] = useState<{
    status: 'idle' | 'pending' | 'success' | 'error'
    data?: T
    error?: Error
  }>({ status: 'idle' })

  const execute = useCallback(async () => {
    // Guard: prevent if already pending
    if (state.status === 'pending') return

    setState({ status: 'pending' })

    try {
      const data = await executeFn()
      setState({ status: 'success', data })
      return data
    } catch (error) {
      setState({ status: 'error', error: error as Error })
      throw error
    }
  }, [executeFn, state.status])

  return {
    ...state,
    execute,
    isPending: state.status === 'pending',
    isDisabled: state.status === 'pending',
  }
}
```

### Approval Patterns

For token approvals, show clear information about what is being approved.

```tsx
interface ApprovalRequestProps {
  token: {
    symbol: string
    address: string
  }
  spender: {
    name: string
    address: string
  }
  amount: bigint // MaxUint256 for unlimited
  onApprove: () => Promise<void>
  onCancel: () => void
}

function ApprovalRequest({ token, spender, amount, onApprove, onCancel }: ApprovalRequestProps) {
  const isUnlimited = amount === MaxUint256

  return (
    <TransactionConfirm
      action="Token Approval"
      details={[
        { label: 'Token', value: token.symbol },
        { label: 'Token Address', value: truncateAddress(token.address) },
        { label: 'Spender', value: spender.name },
        { label: 'Spender Address', value: truncateAddress(spender.address) },
        {
          label: 'Amount',
          value: isUnlimited ? 'Unlimited' : formatTokenAmount(amount),
        },
      ]}
      onConfirm={onApprove}
      onCancel={onCancel}
    />
  )
}
```

---

## Display Safety

### No Dangerous HTML

Never use `dangerouslySetInnerHTML` with external data.

```tsx
// BAD: XSS vulnerability
function UserBio({ bio }: { bio: string }) {
  return <div dangerouslySetInnerHTML={{ __html: bio }} />
}

// GOOD: Render as text
function UserBio({ bio }: { bio: string }) {
  return <div>{bio}</div>
}

// If HTML is required, sanitize first
import DOMPurify from 'dompurify'

function UserBio({ bio }: { bio: string }) {
  const sanitized = DOMPurify.sanitize(bio, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em'],
    ALLOWED_ATTR: [],
  })
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />
}
```

### URL Safety

Validate URLs before rendering links or images.

```tsx
function isValidUrl(url: string): boolean {
  try {
    const parsed = new URL(url)
    return ['http:', 'https:'].includes(parsed.protocol)
  } catch {
    return false
  }
}

function ExternalLink({ href, children }: { href: string; children: React.ReactNode }) {
  if (!isValidUrl(href)) {
    return <span>{children}</span> // Render as text if invalid
  }

  return (
    <a href={href} target="_blank" rel="noopener noreferrer">
      {children}
    </a>
  )
}
```

### Sensitive Data Display

Mask sensitive data by default, reveal on explicit action.

```tsx
function PrivateKeyDisplay({ privateKey }: { privateKey: string }) {
  const [isRevealed, setIsRevealed] = useState(false)

  return (
    <div className="flex items-center gap-2">
      <code className="font-mono">{isRevealed ? privateKey : '••••••••••••••••••••••••'}</code>
      <Button variant="ghost" size="sm" onClick={() => setIsRevealed(!isRevealed)}>
        {isRevealed ? 'Hide' : 'Reveal'}
      </Button>
    </div>
  )
}
```

---

## State & Storage Security

### Never Store Sensitive Data in State

Private keys, seeds, and decrypted secrets should never be in React state.

```tsx
// BAD: Private key in state
const [privateKey, setPrivateKey] = useState<string>()

// GOOD: Keep in secure context, clear after use
async function signTransaction(tx: Transaction) {
  const signer = await getSigner() // Get from wallet provider
  return signer.signTransaction(tx)
}
```

### Clear Sensitive Data

Clear sensitive data from memory when no longer needed.

```tsx
function ImportWallet({ onImport }: { onImport: (address: string) => void }) {
  const [seed, setSeed] = useState('')

  const handleImport = async () => {
    try {
      const wallet = Wallet.fromPhrase(seed)
      onImport(wallet.address)
    } finally {
      // Clear sensitive data
      setSeed('')
    }
  }

  // Clear on unmount
  useEffect(() => {
    return () => setSeed('')
  }, [])

  return (
    <form onSubmit={handleImport}>
      <Input
        type="password"
        value={seed}
        onChange={e => setSeed(e.target.value)}
        autoComplete="off"
      />
    </form>
  )
}
```

### LocalStorage Caution

Never store private keys or seeds in localStorage. Use for non-sensitive preferences only.

```tsx
// OK: Theme preference
localStorage.setItem('theme', 'dark')

// OK: Dismissed banners
localStorage.setItem('dismissed-banner-v1', 'true')

// NEVER: Sensitive data
localStorage.setItem('privateKey', key) // NEVER DO THIS
localStorage.setItem('seed', seed) // NEVER DO THIS
```

---

## Error Handling

**For a complete and unified strategy on error handling, including Error Boundaries, structured logging, and user-facing error patterns, refer to the [Error Handling & Reporting Strategy Guide](error-handling.md).**

### Don't Leak Sensitive Information

Error messages should be helpful but not expose internal details.

```tsx
// BAD: Exposes internal error
catch (error) {
  setError(`Transaction failed: ${error.message}`);
  // Could expose: "insufficient funds at address 0x..."
}

// GOOD: User-friendly error
catch (error) {
  logger.error('transaction_failed', { error });

  if (isInsufficientFundsError(error)) {
    setError('Insufficient balance. Please add funds and try again.');
  } else if (isUserRejectedError(error)) {
    setError('Transaction was cancelled.');
  } else {
    setError('Transaction failed. Please try again.');
  }
}
```

### Error Type Guards

Create type guards for common error scenarios.

```tsx
function isInsufficientFundsError(error: unknown): boolean {
  if (error instanceof Error) {
    return error.message.toLowerCase().includes('insufficient funds')
  }
  return false
}

function isUserRejectedError(error: unknown): boolean {
  if (error instanceof Error) {
    const message = error.message.toLowerCase()
    return (
      message.includes('user rejected') ||
      message.includes('user denied') ||
      message.includes('user cancelled')
    )
  }
  return false
}

function isNetworkError(error: unknown): boolean {
  return error instanceof Error && error.name === 'NetworkError'
}
```

---

## Logging

### Use LogTape

Never use `console.*` directly. Use structured logging.

```tsx
import { getLogger } from '@logtape/logtape'

const logger = getLogger(['app', 'orders'])

// Structured logging
logger.info('order_created', { orderId: order.id, type: order.type })
logger.error('order_failed', { orderId, error: error.message })
```

### Never Log Sensitive Data

```tsx
// NEVER log these
logger.info('wallet_connected', { privateKey }) // NEVER
logger.info('transaction_signed', { seed }) // NEVER
logger.info('user_action', { fullAddress }) // AVOID

// Safe logging patterns
logger.info('wallet_connected', {
  address: truncateAddress(address), // Truncated
})

logger.info('transaction_submitted', {
  txHash: tx.hash,
  type: 'transfer',
  // No amounts, no full addresses
})
```

### Log Levels

Use appropriate log levels.

```tsx
// Debug: Development only, verbose
logger.debug('render_cycle', { componentName, props })

// Info: Normal operations worth tracking
logger.info('order_placed', { orderId })

// Warn: Unexpected but handled situations
logger.warn('retry_attempted', { attempt: 3, maxAttempts: 5 })

// Error: Failures that need attention
logger.error('transaction_failed', { error: error.message })
```

### No Debug Logs in Production

Configure LogTape to filter debug logs in production.

```tsx
import { configure } from '@logtape/logtape'

configure({
  sinks: {
    console: getConsoleSink(),
  },
  loggers: [
    {
      category: ['app'],
      sinks: ['console'],
      level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
    },
  ],
})
```
