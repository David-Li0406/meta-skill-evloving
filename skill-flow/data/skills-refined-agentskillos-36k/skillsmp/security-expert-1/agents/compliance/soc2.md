---
name: soc2
description: Expert conformite SOC2 - Trust Services Criteria, controles et evidence
---

# SOC 2 Implementation

Tu es expert en **implementation technique SOC 2**.

## Mission

> Implementer les controles techniques pour satisfaire les Trust Services Criteria.

## Trust Services Criteria (TSC)

| Critere | Focus | Obligatoire |
|---------|-------|-------------|
| **Security** | Protection contre acces non-autorise | Oui |
| **Availability** | Systeme disponible | Optionnel |
| **Processing Integrity** | Traitement correct | Optionnel |
| **Confidentiality** | Donnees confidentielles protegees | Optionnel |
| **Privacy** | Donnees personnelles protegees | Optionnel |

## Security (Common Criteria)

### CC1: Control Environment

```typescript
// Documentation des politiques (automatisee)
interface SecurityPolicy {
  id: string;
  title: string;
  version: string;
  approvedBy: string;
  approvedAt: Date;
  reviewedAt: Date;
  nextReviewDate: Date;
}

// Tracking des revisions
app.get('/admin/policies', adminMiddleware, async (req, res) => {
  const policies = await db.policy.findMany({
    where: { status: 'active' },
    include: { approvals: true, reviews: true }
  });
  res.json(policies);
});
```

### CC2: Communication

```typescript
// Notification des changements de politique
async function notifyPolicyChange(policy: SecurityPolicy) {
  const employees = await db.employee.findMany({
    where: { status: 'active' }
  });

  await Promise.all(employees.map(emp =>
    sendEmail({
      to: emp.email,
      subject: `Policy Update: ${policy.title}`,
      template: 'policy-update',
      data: { policy, acknowledgeUrl: `/policies/${policy.id}/acknowledge` }
    })
  ));
}

// Tracking des acknowledgements
app.post('/policies/:id/acknowledge', authMiddleware, async (req, res) => {
  await db.policyAcknowledgement.create({
    data: {
      policyId: req.params.id,
      userId: req.user.id,
      acknowledgedAt: new Date(),
      ipAddress: req.ip,
    }
  });
  res.json({ success: true });
});
```

### CC3: Risk Assessment

```typescript
// Risk register automatise
interface Risk {
  id: string;
  title: string;
  category: string;
  likelihood: 1 | 2 | 3 | 4 | 5;
  impact: 1 | 2 | 3 | 4 | 5;
  controls: string[];
  owner: string;
  reviewedAt: Date;
}

function calculateRiskScore(risk: Risk): number {
  return risk.likelihood * risk.impact;
}

// Dashboard des risques
app.get('/admin/risks', adminMiddleware, async (req, res) => {
  const risks = await db.risk.findMany({
    include: { controls: true, mitigations: true }
  });

  const summary = {
    critical: risks.filter(r => calculateRiskScore(r) >= 20).length,
    high: risks.filter(r => calculateRiskScore(r) >= 12).length,
    medium: risks.filter(r => calculateRiskScore(r) >= 6).length,
    low: risks.filter(r => calculateRiskScore(r) < 6).length,
  };

  res.json({ risks, summary });
});
```

### CC5: Control Activities

```typescript
// Access control logging (evidence automatique)
const accessLogger = (req: Request, res: Response, next: NextFunction) => {
  const log = {
    timestamp: new Date(),
    userId: req.user?.id,
    action: `${req.method} ${req.path}`,
    ip: req.ip,
    userAgent: req.headers['user-agent'],
    success: true,
  };

  // Log asynchrone (non-bloquant)
  db.accessLog.create({ data: log }).catch(console.error);

  res.on('finish', () => {
    if (res.statusCode >= 400) {
      db.accessLog.update({
        where: { id: log.id },
        data: { success: false, statusCode: res.statusCode }
      });
    }
  });

  next();
};

// Appliquer a toutes les routes sensibles
app.use('/admin', accessLogger);
app.use('/api', accessLogger);
```

### CC6: Logical & Physical Access

```typescript
// MFA obligatoire pour acces sensibles
const requireMFA = async (req: Request, res: Response, next: NextFunction) => {
  if (!req.user.mfaVerified) {
    return res.status(403).json({
      error: 'MFA required',
      mfaUrl: '/auth/mfa/verify'
    });
  }
  next();
};

// Role-based access avec audit
const requireRole = (roles: string[]) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const hasRole = roles.includes(req.user.role);

    // Logger la tentative d'acces
    await db.accessAttempt.create({
      data: {
        userId: req.user.id,
        resource: req.path,
        requiredRoles: roles,
        userRole: req.user.role,
        granted: hasRole,
        timestamp: new Date(),
      }
    });

    if (!hasRole) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    next();
  };
};
```

### CC7: System Operations

```typescript
// Change management automatise
interface ChangeRequest {
  id: string;
  type: 'feature' | 'bugfix' | 'security' | 'infrastructure';
  description: string;
  requestedBy: string;
  approvedBy?: string;
  implementedAt?: Date;
  rollbackPlan: string;
}

// Pipeline CI/CD avec approbation
// .github/workflows/deploy.yml
const deployWorkflow = `
name: Production Deploy

on:
  push:
    branches: [main]

jobs:
  approval:
    runs-on: ubuntu-latest
    environment: production  # Requiert approbation manuelle
    steps:
      - name: Await approval
        run: echo "Deployment approved"

  deploy:
    needs: approval
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: ./deploy.sh
      - name: Log change
        run: |
          curl -X POST $CHANGE_LOG_URL \\
            -d '{"commit": "$GITHUB_SHA", "deployer": "$GITHUB_ACTOR"}'
`;
```

### CC8: Change Management

```typescript
// Tracking des changements systeme
app.post('/admin/changes', adminMiddleware, async (req, res) => {
  const change = await db.changeRequest.create({
    data: {
      ...req.body,
      requestedBy: req.user.id,
      status: 'pending_approval',
      createdAt: new Date(),
    }
  });

  // Notifier les approbateurs
  await notifyApprovers(change);

  res.json(change);
});

// Approbation avec audit trail
app.post('/admin/changes/:id/approve', adminMiddleware, async (req, res) => {
  await db.changeRequest.update({
    where: { id: req.params.id },
    data: {
      status: 'approved',
      approvedBy: req.user.id,
      approvedAt: new Date(),
    }
  });

  res.json({ success: true });
});
```

## Evidence Collection

```typescript
// Collecte automatique d'evidence
async function collectSOC2Evidence() {
  const evidence = {
    accessLogs: await db.accessLog.count({
      where: { createdAt: { gte: subDays(new Date(), 90) } }
    }),
    mfaAdoption: await calculateMFAAdoption(),
    policyAcknowledgements: await db.policyAcknowledgement.findMany({
      where: { acknowledgedAt: { gte: subDays(new Date(), 365) } }
    }),
    changeRequests: await db.changeRequest.findMany({
      where: { createdAt: { gte: subDays(new Date(), 90) } }
    }),
    vulnerabilityScans: await getVulnerabilityScans(),
    incidentReports: await db.incident.findMany({
      where: { createdAt: { gte: subDays(new Date(), 365) } }
    }),
  };

  return evidence;
}

// Export pour auditeurs
app.get('/admin/soc2/evidence', adminMiddleware, async (req, res) => {
  const evidence = await collectSOC2Evidence();
  res.json(evidence);
});
```

## Monitoring & Alerting

```typescript
// Alertes SOC2-required
const securityAlerts = {
  // Tentatives de connexion echouees
  failedLogins: {
    threshold: 5,
    window: '15m',
    action: 'alert_security_team'
  },

  // Acces admin hors heures
  afterHoursAdminAccess: {
    hours: { start: 18, end: 8 },
    action: 'alert_manager'
  },

  // Changements de configuration
  configChanges: {
    action: 'log_and_notify'
  }
};

// Implementation
app.use('/admin', (req, res, next) => {
  const hour = new Date().getHours();

  if (hour >= 18 || hour < 8) {
    alertManager({
      type: 'after_hours_access',
      user: req.user,
      action: req.path,
      timestamp: new Date()
    });
  }

  next();
});
```

## Checklist SOC2 Type II

### Security
- [ ] Access control implemente
- [ ] MFA active
- [ ] Logging complet
- [ ] Vulnerability scanning
- [ ] Incident response

### Availability
- [ ] SLA definis
- [ ] Monitoring actif
- [ ] Backup teste
- [ ] DR plan documente

### Confidentiality
- [ ] Classification des donnees
- [ ] Chiffrement
- [ ] Access restrictions
- [ ] Data disposal

### Processing Integrity
- [ ] Validation des inputs
- [ ] Error handling
- [ ] Audit trails
- [ ] Reconciliation

## Voir Aussi

- `compliance/iso27001` pour SMSI
- `devops/monitoring` pour observabilite
- `secure-coding/authentication` pour MFA
