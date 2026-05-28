# Two-Factor Authentication (2FA) Examples

## Server Setup

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { twoFactor } from "better-auth/plugins";

export const auth = betterAuth({
  appName: "My App", // Used as TOTP issuer
  plugins: [
    twoFactor({
      issuer: "My App", // Optional, defaults to appName
      otpLength: 6, // Default: 6
      period: 30, // Default: 30 seconds
    }),
  ],
});
```

## Client Setup

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/client";
import { twoFactorClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [
    twoFactorClient({
      onTwoFactorRedirect() {
        // Called when 2FA verification is required
        window.location.href = "/2fa";
      },
    }),
  ],
});
```

## Enable 2FA for User

```typescript
// Step 1: Generate TOTP secret
const { data } = await authClient.twoFactor.enable();

// data contains:
// - totpURI: otpauth://totp/... (for QR code)
// - backupCodes: ["abc123", "def456", ...] (save these!)

// Show QR code using a library like qrcode.react
<QRCode value={data.totpURI} />

// Step 2: Verify and activate
await authClient.twoFactor.verifyTotp({
  code: "123456", // From authenticator app
});
```

## React Enable 2FA Component

```tsx
"use client";

import { useState } from "react";
import { authClient } from "@/lib/auth-client";
import { QRCodeSVG } from "qrcode.react";

export function Enable2FA() {
  const [step, setStep] = useState<"start" | "scan" | "verify" | "done">("start");
  const [totpURI, setTotpURI] = useState("");
  const [backupCodes, setBackupCodes] = useState<string[]>([]);
  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  const handleEnable = async () => {
    const { data, error } = await authClient.twoFactor.enable();

    if (error) {
      setError(error.message);
      return;
    }

    setTotpURI(data.totpURI);
    setBackupCodes(data.backupCodes);
    setStep("scan");
  };

  const handleVerify = async () => {
    const { error } = await authClient.twoFactor.verifyTotp({ code });

    if (error) {
      setError("Invalid code. Please try again.");
      return;
    }

    setStep("done");
  };

  if (step === "start") {
    return (
      <button onClick={handleEnable}>Enable Two-Factor Authentication</button>
    );
  }

  if (step === "scan") {
    return (
      <div>
        <h3>Scan QR Code</h3>
        <QRCodeSVG value={totpURI} size={200} />
        <p>Scan with Google Authenticator, Authy, or similar app</p>

        <h4>Backup Codes</h4>
        <p>Save these codes in a safe place:</p>
        <ul>
          {backupCodes.map((code, i) => (
            <li key={i}><code>{code}</code></li>
          ))}
        </ul>

        <input
          type="text"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Enter 6-digit code"
          maxLength={6}
        />
        {error && <p className="error">{error}</p>}
        <button onClick={handleVerify}>Verify & Activate</button>
      </div>
    );
  }

  if (step === "done") {
    return (
      <div>
        <h3>2FA Enabled!</h3>
        <p>Your account is now protected with two-factor authentication.</p>
      </div>
    );
  }
}
```

## Sign In with 2FA

```typescript
// Normal sign in - will trigger onTwoFactorRedirect if 2FA is enabled
const { data, error } = await authClient.signIn.email({
  email: "user@example.com",
  password: "password",
});

// The onTwoFactorRedirect callback will redirect to /2fa
// On /2fa page, verify the TOTP:
await authClient.twoFactor.verifyTotp({
  code: "123456",
});
```

## 2FA Verification Page

```tsx
"use client";

import { useState } from "react";
import { authClient } from "@/lib/auth-client";
import { useRouter } from "next/navigation";

export function TwoFactorVerify() {
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [useBackup, setUseBackup] = useState(false);
  const router = useRouter();

  const handleVerify = async () => {
    const { error } = useBackup
      ? await authClient.twoFactor.verifyBackupCode({ code })
      : await authClient.twoFactor.verifyTotp({ code });

    if (error) {
      setError(useBackup ? "Invalid backup code" : "Invalid code");
      return;
    }

    router.push("/dashboard");
  };

  return (
    <div>
      <h2>Two-Factor Authentication</h2>
      <p>
        {useBackup
          ? "Enter a backup code"
          : "Enter the 6-digit code from your authenticator app"}
      </p>

      <input
        type="text"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder={useBackup ? "Backup code" : "6-digit code"}
        autoComplete="one-time-code"
      />

      {error && <p className="error">{error}</p>}

      <button onClick={handleVerify}>Verify</button>

      <button onClick={() => setUseBackup(!useBackup)}>
        {useBackup ? "Use authenticator app" : "Use backup code"}
      </button>
    </div>
  );
}
```

## Disable 2FA

```typescript
await authClient.twoFactor.disable({
  password: "currentPassword", // May be required
});
```

## Regenerate Backup Codes

```typescript
const { data } = await authClient.twoFactor.generateBackupCodes();
// data.backupCodes contains new codes
// Old codes are invalidated
```

## Check 2FA Status

```typescript
const session = await authClient.getSession();

if (session?.user) {
  // Check if 2FA is enabled
  const { data } = await authClient.twoFactor.status();
  console.log("2FA enabled:", data.enabled);
}
```

## Trust Device (Remember this device)

```typescript
// During 2FA verification
await authClient.twoFactor.verifyTotp({
  code: "123456",
  trustDevice: true, // Skip 2FA on this device for configured period
});
```

## Server Configuration Options

```typescript
twoFactor({
  // TOTP settings
  issuer: "My App",
  otpLength: 6,
  period: 30,

  // Backup codes
  backupCodeLength: 10,
  numberOfBackupCodes: 10,

  // Trust device
  trustDeviceCookie: {
    name: "trusted_device",
    maxAge: 60 * 60 * 24 * 30, // 30 days
  },

  // Skip 2FA for certain conditions
  skipVerificationOnEnable: false,
})
```

## Using with Sign In Callback

```typescript
const authClient = createAuthClient({
  plugins: [
    twoFactorClient({
      onTwoFactorRedirect() {
        // Store the intended destination
        sessionStorage.setItem("redirectAfter2FA", window.location.pathname);
        window.location.href = "/2fa";
      },
    }),
  ],
});

// After 2FA verification
const redirect = sessionStorage.getItem("redirectAfter2FA") || "/dashboard";
sessionStorage.removeItem("redirectAfter2FA");
router.push(redirect);
```

## Database Changes

After adding the twoFactor plugin, regenerate and migrate:

```bash
npx @better-auth/cli generate
npx @better-auth/cli migrate
```

This creates the `twoFactor` table with:
- `id`
- `userId`
- `secret` (encrypted TOTP secret)
- `backupCodes` (hashed backup codes)
