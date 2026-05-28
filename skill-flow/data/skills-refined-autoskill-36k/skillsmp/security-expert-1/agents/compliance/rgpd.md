---
name: rgpd
description: Expert implementation RGPD - Consentement, droits, donnees personnelles
---

# RGPD Implementation

Tu es expert en **implementation technique du RGPD**.

## Mission

> Implementer les exigences RGPD dans le code et l'infrastructure.

## Principes Cles du RGPD

| Principe | Description | Implementation |
|----------|-------------|----------------|
| **Licite** | Base legale pour traitement | Consentement explicite |
| **Finalite** | But specifique et limite | Metadata sur donnees |
| **Minimisation** | Collecter le strict minimum | Schema DB optimise |
| **Exactitude** | Donnees a jour | Processus de mise a jour |
| **Limitation** | Conservation limitee | TTL, purge automatique |
| **Integrite** | Securite des donnees | Chiffrement, access control |

## Gestion du Consentement

### Implementation

```typescript
// Schema consentement
interface Consent {
  userId: string;
  purpose: string;
  granted: boolean;
  grantedAt: Date;
  revokedAt?: Date;
  source: 'web' | 'app' | 'api';
  version: string;
  ipAddress: string;
}

// Base de donnees
const ConsentSchema = {
  userId: { type: 'string', required: true },
  consents: [{
    purpose: { type: 'string', enum: ['marketing', 'analytics', 'necessary'] },
    granted: { type: 'boolean', required: true },
    grantedAt: { type: 'date', required: true },
    revokedAt: { type: 'date' },
    source: { type: 'string' },
    version: { type: 'string' }, // Version des conditions
  }]
};

// API de gestion
app.post('/api/consent', async (req, res) => {
  const { purposes, granted } = req.body;

  for (const purpose of purposes) {
    await db.consent.upsert({
      where: { userId_purpose: { userId: req.user.id, purpose } },
      update: {
        granted,
        grantedAt: granted ? new Date() : undefined,
        revokedAt: granted ? undefined : new Date(),
        version: CURRENT_CONSENT_VERSION,
        source: 'web',
      },
      create: {
        userId: req.user.id,
        purpose,
        granted,
        grantedAt: granted ? new Date() : undefined,
        version: CURRENT_CONSENT_VERSION,
        source: 'web',
        ipAddress: req.ip,
      }
    });
  }

  res.json({ success: true });
});
```

### Banniere Cookie

```typescript
// Cookie consent management
interface CookieConsent {
  necessary: boolean;  // Toujours true
  functional: boolean;
  analytics: boolean;
  marketing: boolean;
  timestamp: number;
}

// Verification avant tracking
function canTrack(type: keyof CookieConsent): boolean {
  const consent = getCookieConsent();
  return consent?.[type] === true;
}

// Conditionner le chargement
if (canTrack('analytics')) {
  loadGoogleAnalytics();
}

if (canTrack('marketing')) {
  loadFacebookPixel();
}
```

## Droits des Personnes

### Droit d'Acces (Art. 15)

```typescript
// Export des donnees utilisateur
app.get('/api/privacy/export', authMiddleware, async (req, res) => {
  const userId = req.user.id;

  const userData = await Promise.all([
    db.user.findUnique({ where: { id: userId } }),
    db.order.findMany({ where: { userId } }),
    db.consent.findMany({ where: { userId } }),
    db.activityLog.findMany({ where: { userId } }),
  ]);

  const exportData = {
    exportedAt: new Date().toISOString(),
    user: sanitizeUserData(userData[0]),
    orders: userData[1],
    consents: userData[2],
    activities: userData[3],
  };

  res.setHeader('Content-Disposition', 'attachment; filename=my-data.json');
  res.json(exportData);
});
```

### Droit a l'Effacement (Art. 17)

```typescript
// Suppression des donnees
app.delete('/api/privacy/delete', authMiddleware, async (req, res) => {
  const userId = req.user.id;

  // Verification: pas d'obligation legale de conservation
  const hasLegalHold = await checkLegalHold(userId);
  if (hasLegalHold) {
    return res.status(400).json({
      error: 'Cannot delete: legal retention period applies'
    });
  }

  // Transaction pour suppression complete
  await db.$transaction(async (tx) => {
    // Anonymiser plutot que supprimer (audit trail)
    await tx.user.update({
      where: { id: userId },
      data: {
        email: `deleted-${userId}@anonymous.local`,
        name: 'Deleted User',
        phone: null,
        deletedAt: new Date(),
      }
    });

    // Supprimer les donnees non-essentielles
    await tx.activityLog.deleteMany({ where: { userId } });
    await tx.preference.deleteMany({ where: { userId } });

    // Garder les transactions (obligation comptable)
    await tx.order.updateMany({
      where: { userId },
      data: { userId: null, anonymizedAt: new Date() }
    });
  });

  // Supprimer des systemes externes
  await Promise.all([
    mailchimpClient.removeSubscriber(req.user.email),
    analyticsClient.deleteUser(userId),
    crmClient.anonymizeContact(userId),
  ]);

  res.json({ success: true, message: 'Data deleted' });
});
```

### Droit a la Portabilite (Art. 20)

```typescript
// Export format machine-readable
app.get('/api/privacy/portability', authMiddleware, async (req, res) => {
  const format = req.query.format || 'json';

  const data = await collectUserData(req.user.id);

  if (format === 'csv') {
    const csv = convertToCSV(data);
    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', 'attachment; filename=my-data.csv');
    return res.send(csv);
  }

  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Content-Disposition', 'attachment; filename=my-data.json');
  res.json(data);
});
```

## Chiffrement des Donnees Sensibles

```typescript
import crypto from 'crypto';

const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY!;

// Chiffrement cote application
function encryptPII(data: string): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', ENCRYPTION_KEY, iv);

  let encrypted = cipher.update(data, 'utf8', 'base64');
  encrypted += cipher.final('base64');

  const authTag = cipher.getAuthTag();

  return `${iv.toString('base64')}:${authTag.toString('base64')}:${encrypted}`;
}

function decryptPII(encryptedData: string): string {
  const [ivB64, tagB64, data] = encryptedData.split(':');

  const decipher = crypto.createDecipheriv(
    'aes-256-gcm',
    ENCRYPTION_KEY,
    Buffer.from(ivB64, 'base64')
  );

  decipher.setAuthTag(Buffer.from(tagB64, 'base64'));

  let decrypted = decipher.update(data, 'base64', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}

// Utilisation dans le modele
const UserSchema = {
  email: String,
  encryptedSSN: String,  // Chiffre
  encryptedPhone: String, // Chiffre
};
```

## Retention et Purge

```typescript
// Job de purge automatique
async function purgeExpiredData() {
  const retentionPolicies = {
    activityLogs: 365,      // 1 an
    marketingConsent: 730,  // 2 ans
    deletedUsers: 30,       // 30 jours apres suppression
    tempFiles: 7,           // 7 jours
  };

  const now = new Date();

  // Purger les logs d'activite
  await db.activityLog.deleteMany({
    where: {
      createdAt: { lt: subDays(now, retentionPolicies.activityLogs) }
    }
  });

  // Purger les consentements expires
  await db.consent.deleteMany({
    where: {
      purpose: 'marketing',
      revokedAt: { lt: subDays(now, retentionPolicies.marketingConsent) }
    }
  });

  // Supprimer definitivement les utilisateurs
  await db.user.deleteMany({
    where: {
      deletedAt: { lt: subDays(now, retentionPolicies.deletedUsers) }
    }
  });
}

// Cron job
cron.schedule('0 2 * * *', purgeExpiredData); // 2h du matin
```

## Notification de Breach

```typescript
// En cas de violation de donnees
interface DataBreach {
  detectedAt: Date;
  affectedUsers: number;
  dataTypes: string[];
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
}

async function handleDataBreach(breach: DataBreach) {
  // 1. Logger l'incident
  await db.securityIncident.create({ data: breach });

  // 2. Notifier le DPO (< 72h pour CNIL)
  await notifyDPO(breach);

  // 3. Si risque eleve: notifier les utilisateurs
  if (breach.severity === 'high' || breach.severity === 'critical') {
    const affectedUsers = await getAffectedUsers(breach);
    await notifyUsers(affectedUsers, breach);
  }

  // 4. Preparer le rapport CNIL
  const cnilReport = generateCNILReport(breach);
  await saveCNILReport(cnilReport);
}
```

## Checklist RGPD

### Collecte
- [ ] Base legale documentee
- [ ] Consentement explicite et granulaire
- [ ] Information claire (finalite, duree)
- [ ] Minimisation des donnees

### Stockage
- [ ] Chiffrement at-rest
- [ ] Access control strict
- [ ] Localisation EU (ou adequacy)
- [ ] Retention policies definies

### Traitement
- [ ] Logging des acces
- [ ] Pseudonymisation si possible
- [ ] Sous-traitants conformes (DPA)
- [ ] PIA pour traitements risques

### Droits
- [ ] Acces implemente
- [ ] Rectification possible
- [ ] Effacement fonctionnel
- [ ] Portabilite disponible
- [ ] Opposition respectee

### Securite
- [ ] Chiffrement in-transit (TLS)
- [ ] Authentification forte
- [ ] Procedure breach
- [ ] Tests reguliers

## Voir Aussi

- `secure-coding/cryptography` pour chiffrement
- `secure-coding/authorization` pour access control
- `compliance/soc2` pour controles associes
