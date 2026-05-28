# Owner Management

Manage data ownership, encryption, and cross-device sync.

## Complete Example

```typescript
"use client";

import { useEvolu, useOwner } from "@evolu/react";

function OwnerSettings() {
  const evolu = useEvolu();
  const owner = useOwner();

  // Get mnemonic for backup/restore
  const showMnemonic = async () => {
    const mnemonic = await evolu.getMnemonic();
    // Display in secure modal - NEVER log to console in production
    // mnemonic is the master key to all encrypted data
    displaySecureModal(mnemonic);
  };

  // Restore data on new device
  const restoreFromMnemonic = (mnemonic: string) => {
    // WARNING: This calls resetAppOwner first, clearing local data
    evolu.restoreAppOwner(mnemonic);
  };

  // Reset all local data
  const resetAllData = () => {
    // WARNING: This deletes all local data irreversibly
    evolu.resetAppOwner();
  };

  // Export database for backup
  const exportData = async () => {
    const data = await evolu.exportDatabase();
    // Save as file
    const blob = new Blob([data], { type: "application/octet-stream" });
    const url = URL.createObjectURL(blob);
    // Trigger download...
  };

  return (
    <div>
      <p>Owner ID: {owner?.id}</p>
      <button onClick={showMnemonic}>Show Recovery Phrase</button>
      <button onClick={resetAllData}>Reset All Data</button>
    </div>
  );
}
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Mnemonic** | 12-word recovery phrase - store securely, used to restore data on new devices |
| **Encryption** | All data encrypted with key derived from mnemonic |
| **Sync** | Automatic sync via WebSocket (defaults to free.evoluhq.com) |
| **Privacy** | Data is end-to-end encrypted; server cannot read it |

## Dangerous Operations

| Operation | Method | Warning |
|-----------|--------|---------|
| Reset | `resetAppOwner()` | Deletes ALL local data - **irreversible** |
| Restore | `restoreAppOwner(mnemonic)` | Clears local data first, then restores from sync |

## Security Checklist

- NEVER log mnemonic to console in production
- Store mnemonic in secure password manager or encrypted storage
- Warn users before displaying mnemonic (it grants full access to data)
- Use environment variables or secure storage for sync URL if self-hosting
- Validate mnemonic format before restore operations
- Remember: **mnemonic = master key to ALL encrypted data**
