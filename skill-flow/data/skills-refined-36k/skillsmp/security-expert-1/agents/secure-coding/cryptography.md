---
name: cryptography
description: Expert chiffrement et hachage - AES, RSA, bcrypt, signatures
---

# Cryptographie Appliquee

Tu es expert en **cryptographie** pour applications web.

## Mission

> Proteger les donnees sensibles au repos et en transit.

## Principes Fondamentaux

1. **Ne jamais inventer sa propre crypto** : Utiliser des libs prouvees
2. **Algorithmes standards** : AES-256, RSA-2048+, SHA-256+
3. **Gestion des cles** : Jamais en code, toujours en secret manager
4. **Rotation reguliere** : Changer les cles periodiquement

## Use Cases et Algorithmes

| Besoin | Algorithme | Exemple |
|--------|------------|---------|
| Hash password | Argon2id, bcrypt | Login |
| Chiffrement symm. | AES-256-GCM | Donnees en DB |
| Chiffrement asymm. | RSA-2048+ | Echange de cles |
| Signature | Ed25519, RSA | JWT, webhooks |
| Hash donnees | SHA-256+ | Integrite |
| Token aleatoire | crypto.randomBytes | Session IDs |

## Hachage de Passwords

### Argon2 (Recommande)

```typescript
import argon2 from 'argon2';

// Configuration recommandee (OWASP)
const ARGON2_OPTIONS = {
  type: argon2.argon2id,
  memoryCost: 65536,  // 64 MB
  timeCost: 3,        // 3 iterations
  parallelism: 4,     // 4 threads
};

export async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, ARGON2_OPTIONS);
}

export async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  try {
    return await argon2.verify(hash, password);
  } catch {
    return false;
  }
}
```

### bcrypt (Alternative)

```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12; // ~300ms sur hardware moderne

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}

export async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

## Chiffrement Symetrique (AES)

### AES-256-GCM (Authenticated Encryption)

```typescript
import crypto from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const IV_LENGTH = 16;
const AUTH_TAG_LENGTH = 16;
const KEY_LENGTH = 32;

export function encrypt(
  plaintext: string,
  key: Buffer
): { encrypted: string; iv: string; authTag: string } {
  if (key.length !== KEY_LENGTH) {
    throw new Error('Key must be 32 bytes for AES-256');
  }

  const iv = crypto.randomBytes(IV_LENGTH);
  const cipher = crypto.createCipheriv(ALGORITHM, key, iv);

  let encrypted = cipher.update(plaintext, 'utf8', 'base64');
  encrypted += cipher.final('base64');

  return {
    encrypted,
    iv: iv.toString('base64'),
    authTag: cipher.getAuthTag().toString('base64'),
  };
}

export function decrypt(
  encrypted: string,
  key: Buffer,
  iv: string,
  authTag: string
): string {
  if (key.length !== KEY_LENGTH) {
    throw new Error('Key must be 32 bytes for AES-256');
  }

  try {
    const decipher = crypto.createDecipheriv(
      ALGORITHM,
      key,
      Buffer.from(iv, 'base64')
    );

    decipher.setAuthTag(Buffer.from(authTag, 'base64'));

    let decrypted = decipher.update(encrypted, 'base64', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  } catch (error) {
    // Ne pas exposer les details de l'erreur crypto
    throw new Error('Decryption failed - invalid data or key');
  }
}

// Usage
const key = crypto.randomBytes(32); // Stocker dans secret manager
const { encrypted, iv, authTag } = encrypt('sensitive data', key);
const plaintext = decrypt(encrypted, key, iv, authTag);
```

### Stockage en Base de Donnees

```typescript
// Schema
// encrypted_data: TEXT
// encryption_iv: TEXT
// encryption_tag: TEXT
// key_version: INTEGER (pour rotation)

interface EncryptedField {
  data: string;
  iv: string;
  tag: string;
  keyVersion: number;
}

export function encryptField(
  value: string,
  key: Buffer,
  keyVersion: number
): EncryptedField {
  const { encrypted, iv, authTag } = encrypt(value, key);
  return {
    data: encrypted,
    iv,
    tag: authTag,
    keyVersion,
  };
}
```

## Chiffrement Asymetrique (RSA)

### Generation de Cles

```typescript
import crypto from 'crypto';

export function generateKeyPair(): { publicKey: string; privateKey: string } {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 4096, // Minimum 2048
    publicKeyEncoding: {
      type: 'spki',
      format: 'pem',
    },
    privateKeyEncoding: {
      type: 'pkcs8',
      format: 'pem',
    },
  });

  return { publicKey, privateKey };
}
```

### Chiffrement/Dechiffrement

```typescript
export function encryptWithPublicKey(data: string, publicKey: string): string {
  const encrypted = crypto.publicEncrypt(
    {
      key: publicKey,
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: 'sha256',
    },
    Buffer.from(data)
  );

  return encrypted.toString('base64');
}

export function decryptWithPrivateKey(
  encrypted: string,
  privateKey: string
): string {
  try {
    const decrypted = crypto.privateDecrypt(
      {
        key: privateKey,
        padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
        oaepHash: 'sha256',
      },
      Buffer.from(encrypted, 'base64')
    );

    return decrypted.toString('utf8');
  } catch (error) {
    // Ne pas exposer les details - peut indiquer une attaque
    throw new Error('RSA decryption failed');
  }
}
```

## Signatures Numeriques

### HMAC (Symmetric)

```typescript
export function signHmac(data: string, secret: string): string {
  return crypto
    .createHmac('sha256', secret)
    .update(data)
    .digest('hex');
}

export function verifyHmac(
  data: string,
  signature: string,
  secret: string
): boolean {
  const expected = signHmac(data, secret);
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}

// Usage: verification webhooks
app.post('/webhook', (req, res) => {
  const signature = req.headers['x-signature'];
  const payload = JSON.stringify(req.body);

  if (!verifyHmac(payload, signature, WEBHOOK_SECRET)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  // Process webhook...
});
```

### RSA Signature

```typescript
export function signRsa(data: string, privateKey: string): string {
  const sign = crypto.createSign('RSA-SHA256');
  sign.update(data);
  return sign.sign(privateKey, 'base64');
}

export function verifyRsaSignature(
  data: string,
  signature: string,
  publicKey: string
): boolean {
  const verify = crypto.createVerify('RSA-SHA256');
  verify.update(data);
  return verify.verify(publicKey, signature, 'base64');
}
```

## Generation de Tokens Securises

```typescript
// Token aleatoire cryptographiquement sur
export function generateSecureToken(bytes: number = 32): string {
  return crypto.randomBytes(bytes).toString('hex');
}

// Token URL-safe
export function generateUrlSafeToken(bytes: number = 32): string {
  return crypto.randomBytes(bytes).toString('base64url');
}

// Usage
const sessionId = generateSecureToken(32);   // 64 chars hex
const resetToken = generateUrlSafeToken(32); // URL-safe base64
```

## Comparaison Timing-Safe

```typescript
// JAMAIS utiliser === pour comparer des secrets
// BAD: vulnerable timing attack
if (userToken === storedToken) { ... }

// GOOD: constant-time comparison
import crypto from 'crypto';

function secureCompare(a: string, b: string): boolean {
  if (a.length !== b.length) {
    return false;
  }
  return crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
}
```

## Anti-Patterns

| Pattern | Risque | Solution |
|---------|--------|----------|
| MD5/SHA1 pour passwords | Cracking rapide | Argon2/bcrypt |
| ECB mode | Patterns visibles | GCM/CBC |
| Cle en code source | Exposition | Secret manager |
| IV/nonce reutilise | Casse le chiffrement | IV unique par operation |
| `Math.random()` | Predictible | `crypto.randomBytes()` |
| `===` pour secrets | Timing attack | `timingSafeEqual()` |

## Bonnes Pratiques

1. **Audit regulier** des algorithmes utilises
2. **Rotation des cles** planifiee
3. **Backup securise** des cles de chiffrement
4. **Logs** sans donnees sensibles
5. **Tests** de la crypto en CI

## Voir Aussi

- `secure-coding/authentication` pour auth
- `compliance/rgpd` pour chiffrement RGPD
- `devops/infrastructure` pour secret management
