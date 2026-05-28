# Web3 Integration with ThirdWeb SDK

## ThirdWeb SDK v5 Setup

### Provider Configuration

```typescript
// src/providers/SimpleWeb3Provider.tsx
'use client';

import { ThirdwebProvider } from 'thirdweb/react';

export function SimpleWeb3Provider({ children }: { children: React.ReactNode }) {
  return (
    <ThirdwebProvider>
      {children}
    </ThirdwebProvider>
  );
}
```

### Wallet Provider

The project uses a unified WalletProvider that bridges ThirdWeb hooks:

```typescript
// src/providers/WalletProvider.tsx
'use client';

import { createContext, useContext } from 'react';
import { useActiveAccount, useActiveWallet, useConnect, useDisconnect } from 'thirdweb/react';

interface WalletContextValue {
  account: {
    address: string;
    isConnected: boolean;
    balance?: string;
  } | null;
  chain: {
    id: number;
    name: string;
    symbol: string;
  } | null;
  connect: () => Promise<void>;
  disconnect: () => Promise<void>;
  switchChain: (chainId: number) => Promise<void>;
  signMessage: (message: string) => Promise<string>;
  isConnected: boolean;
  isConnecting: boolean;
  isDisconnecting: boolean;
  error: { message: string; code?: number } | null;
  clearError: () => void;
}

const WalletContext = createContext<WalletContextValue | null>(null);

export function WalletProvider({ children }: { children: React.ReactNode }) {
  const activeAccount = useActiveAccount();
  const activeWallet = useActiveWallet();
  const { connect: thirdwebConnect } = useConnect();
  const { disconnect: thirdwebDisconnect } = useDisconnect();

  const contextValue: WalletContextValue = {
    account: activeAccount ? {
      address: activeAccount.address,
      isConnected: true,
      balance: undefined, // Fetch separately if needed
    } : null,
    chain: activeWallet?.getChain() || null,
    connect: async () => {
      // Implementation using thirdwebConnect
    },
    disconnect: async () => {
      // Implementation using thirdwebDisconnect
    },
    switchChain: async (chainId: number) => {
      // Implementation
    },
    signMessage: async (message: string) => {
      // Implementation
    },
    isConnected: !!activeAccount,
    isConnecting: false,
    isDisconnecting: false,
    error: null,
    clearError: () => {},
  };

  return (
    <WalletContext.Provider value={contextValue}>
      {children}
    </WalletContext.Provider>
  );
}

export function useWalletProvider() {
  const context = useContext(WalletContext);
  if (!context) {
    throw new Error('useWalletProvider must be used within WalletProvider');
  }
  return context;
}
```

## Wallet Connection

### Connect Button

```typescript
import { useWalletProvider } from '@/providers/WalletProvider';

export function ConnectWalletButton() {
  const { account, connect, disconnect, isConnected, isConnecting } = useWalletProvider();

  if (isConnected && account) {
    return (
      <div className="flex items-center gap-4">
        <div className="text-sm text-gray-400">
          {account.address.slice(0, 6)}...{account.address.slice(-4)}
        </div>
        <button
          onClick={disconnect}
          className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg"
        >
          Disconnect
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={connect}
      disabled={isConnecting}
      className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg"
    >
      {isConnecting ? 'Connecting...' : 'Connect Wallet'}
    </button>
  );
}
```

### Wallet Modal

```typescript
import { useWalletProvider } from '@/providers/WalletProvider';
import * as Dialog from '@radix-ui/react-dialog';

export function WalletModal({ open, onOpenChange }: ModalProps) {
  const { connect, error } = useWalletProvider();

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-gray-900 rounded-lg p-6 w-full max-w-md z-50">
          <Dialog.Title className="text-xl font-bold mb-4">
            Connect Wallet
          </Dialog.Title>

          {error && (
            <div className="bg-red-900/20 border border-red-500 rounded-lg p-3 mb-4">
              <p className="text-red-400 text-sm">{error.message}</p>
            </div>
          )}

          <button
            onClick={async () => {
              await connect();
              onOpenChange(false);
            }}
            className="w-full px-4 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-semibold"
          >
            Connect Wallet
          </button>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

## Chain Management

### Supported Chains

```typescript
// src/config/chains.ts
import { ethereum, polygon, arbitrum } from "thirdweb/chains";

export const SUPPORTED_CHAINS = [ethereum, polygon, arbitrum] as const;

export const DEFAULT_CHAIN = ethereum;

export function getChainName(chainId: number): string {
  const chain = SUPPORTED_CHAINS.find(c => c.id === chainId);
  return chain?.name || "Unknown Chain";
}

export function getChainSymbol(chainId: number): string {
  const chain = SUPPORTED_CHAINS.find(c => c.id === chainId);
  return chain?.nativeCurrency.symbol || "ETH";
}
```

### Chain Switcher

```typescript
import { useWalletProvider } from '@/providers/WalletProvider';
import { SUPPORTED_CHAINS } from '@/config/chains';

export function ChainSwitcher() {
  const { chain, switchChain, isConnected } = useWalletProvider();

  if (!isConnected) return null;

  return (
    <select
      value={chain?.id || ''}
      onChange={(e) => switchChain(Number(e.target.value))}
      className="bg-gray-800 text-white rounded-lg px-3 py-2"
    >
      {SUPPORTED_CHAINS.map((c) => (
        <option key={c.id} value={c.id}>
          {c.name}
        </option>
      ))}
    </select>
  );
}
```

## Transaction Execution

### Intent-Based Transactions

```typescript
// src/services/intentService.ts
export interface ZapInRequest {
  userId: string;
  poolId: string;
  amount: string;
  slippage: number;
  tokenAddress?: string;
}

export async function executeZapIn(request: ZapInRequest): Promise<TransactionResult> {
  const response = await fetch("/api/intents/zap-in", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "ZapIn failed");
  }

  return response.json();
}
```

### Transaction Component

```typescript
import { useMutation } from '@tanstack/react-query';
import { useWalletProvider } from '@/providers/WalletProvider';
import * as intentService from '@/services/intentService';

export function ZapInButton({ poolId, amount }: ZapInButtonProps) {
  const { account } = useWalletProvider();

  const { mutate: executeZapIn, isPending } = useMutation({
    mutationFn: intentService.executeZapIn,
    onSuccess: (result) => {
      console.log('ZapIn successful:', result.transactionHash);
      // Show success notification
    },
    onError: (error) => {
      console.error('ZapIn failed:', error);
      // Show error notification
    },
  });

  if (!account) {
    return <div>Please connect wallet</div>;
  }

  return (
    <button
      onClick={() => executeZapIn({
        userId: account.address,
        poolId,
        amount,
        slippage: 0.5,
      })}
      disabled={isPending}
      className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg disabled:opacity-50"
    >
      {isPending ? 'Processing...' : 'Zap In'}
    </button>
  );
}
```

### Transaction Status Tracking

```typescript
import { useQuery } from '@tanstack/react-query';

export function TransactionStatus({ txHash }: { txHash: string }) {
  const { data: status, isLoading } = useQuery({
    queryKey: ['transaction-status', txHash],
    queryFn: () => web3Service.getTransactionStatus(txHash),
    refetchInterval: (data) => {
      // Stop polling when confirmed or failed
      return data?.status === 'pending' ? 5000 : false;
    },
  });

  if (isLoading) {
    return <div className="text-gray-400">Checking status...</div>;
  }

  const statusColor = {
    pending: 'text-yellow-400',
    confirmed: 'text-green-400',
    failed: 'text-red-400',
  }[status?.status || 'pending'];

  return (
    <div className={`font-semibold ${statusColor}`}>
      Status: {status?.status}
    </div>
  );
}
```

## Token Operations

### Token Balance

```typescript
export function useTokenBalance(tokenAddress: string, userAddress: string) {
  return useQuery({
    queryKey: ['token-balance', tokenAddress, userAddress],
    queryFn: () => web3Service.getTokenBalance(tokenAddress, userAddress),
    enabled: !!tokenAddress && !!userAddress,
  });
}

// Usage
function TokenBalance({ tokenAddress }: { tokenAddress: string }) {
  const { account } = useWalletProvider();
  const { data: balance, isLoading } = useTokenBalance(tokenAddress, account?.address || '');

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="text-lg font-semibold">
      Balance: {balance?.formatted} {balance?.symbol}
    </div>
  );
}
```

### Token Approval

```typescript
export function useTokenApproval() {
  return useMutation({
    mutationFn: async ({ tokenAddress, spender, amount }: ApprovalParams) => {
      return await web3Service.approveToken(tokenAddress, spender, amount);
    },
    onSuccess: () => {
      console.log('Token approved');
    },
  });
}

// Usage
function ApprovalButton({ tokenAddress, spender, amount }: ApprovalButtonProps) {
  const { mutate: approve, isPending } = useTokenApproval();

  return (
    <button
      onClick={() => approve({ tokenAddress, spender, amount })}
      disabled={isPending}
    >
      {isPending ? 'Approving...' : 'Approve Token'}
    </button>
  );
}
```

## Error Handling

### Web3 Error Codes

```typescript
export const WEB3_ERROR_CODES = {
  USER_REJECTED: 4001,
  UNAUTHORIZED: 4100,
  UNSUPPORTED_METHOD: 4200,
  DISCONNECTED: 4900,
  CHAIN_DISCONNECTED: 4901,
} as const;

export function handleWeb3Error(error: any): string {
  if (error.code === WEB3_ERROR_CODES.USER_REJECTED) {
    return "Transaction was rejected";
  }

  if (error.code === WEB3_ERROR_CODES.CHAIN_DISCONNECTED) {
    return "Chain is disconnected";
  }

  return error.message || "An unknown error occurred";
}
```

### Error Display

```typescript
function TransactionForm() {
  const { mutate, error } = useMutation({
    mutationFn: executeTransaction,
  });

  return (
    <div>
      <form onSubmit={(e) => {
        e.preventDefault();
        mutate(formData);
      }}>
        {/* Form fields */}
      </form>

      {error && (
        <div className="mt-4 bg-red-900/20 border border-red-500 rounded-lg p-3">
          <p className="text-red-400 text-sm">
            {handleWeb3Error(error)}
          </p>
        </div>
      )}
    </div>
  );
}
```

## Bundle Sharing (Project-Specific)

### Bundle URL Generation

```typescript
// src/services/bundleService.ts
export function generateBundleURL(userId: string): string {
  const baseURL =
    typeof window !== "undefined" ? window.location.origin : process.env.NEXT_PUBLIC_BASE_URL || "";

  return `${baseURL}/bundle?userId=${userId}`;
}

export function isOwner(connectedAddress: string | null, bundleUserId: string): boolean {
  if (!connectedAddress) return false;
  return connectedAddress.toLowerCase() === bundleUserId.toLowerCase();
}
```

### Bundle Page Component

```typescript
'use client';

import { useSearchParams } from 'next/navigation';
import { useWalletProvider } from '@/providers/WalletProvider';
import { isOwner } from '@/services/bundleService';

export function BundlePageClient() {
  const searchParams = useSearchParams();
  const userId = searchParams.get('userId');
  const { account } = useWalletProvider();

  if (!userId) {
    return <div>Invalid bundle URL</div>;
  }

  const isUserOwner = isOwner(account?.address || null, userId);

  return (
    <div>
      {!isUserOwner && account && (
        <SwitchPromptBanner targetUserId={userId} />
      )}
      <PortfolioAllocation userId={userId} readOnly={!isUserOwner} />
    </div>
  );
}
```

## Best Practices

1. **Always Check Connection**: Verify wallet is connected before operations
2. **Handle Rejections**: User can reject transactions - handle gracefully
3. **Chain Validation**: Ensure user is on correct chain before transactions
4. **Error Messages**: Provide clear, user-friendly error messages
5. **Loading States**: Show transaction progress and status
6. **Gas Estimation**: Estimate gas before executing transactions
7. **Token Approvals**: Handle token approvals before transfers
8. **Security**: Never expose private keys or sensitive data
9. **Testing**: Test on testnets before mainnet deployment
10. **Address Validation**: Always validate Ethereum addresses
