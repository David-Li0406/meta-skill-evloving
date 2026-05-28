---
name: Business Logic Expert
description: Expert knowledge of job taxonomies, compliance rules, matching algorithm, and domain-specific configurations.
---

# Business Logic Skill - SocioPulse V2

## Overview

Business logic is encoded as "Logic-as-Config" in `lib/sos-config.ts` and `lib/domain-config.ts`.

---

## 1. Job Taxonomies (`lib/sos-config.ts`)

### Medical Hierarchy

```typescript
export const MEDICAL_JOBS = {
  IDE: {
    label: 'Infirmier Diplômé d\'État',
    specialties: ['URGENCES', 'RÉANIMATION', 'GÉRIATRIE', 'PÉDIATRIE'],
    requires: {
      adeli: true,
      diploma: 'Diplôme d\'État Infirmier',
      rcp: true,
    },
  },
  AS: {
    label: 'Aide-Soignant',
    specialties: ['EHPAD', 'SSIAD', 'HAD'],
    requires: {
      adeli: false,
      diploma: 'Diplôme AS',
      rcp: true,
    },
  },
  // ... IBODE, AES, etc.
};
```

### Social Hierarchy

```typescript
export const SOCIAL_JOBS = {
  ES: {
    label: 'Éducateur Spécialisé',
    specialties: ['MECS', 'IME', 'ITEP', 'AUTISME'],
    requires: {
      diploma: 'DEES',
      driverLicense: true,
      criminalRecord: true,
    },
  },
  ME: {
    label: 'Moniteur Éducateur',
    specialties: ['FOYERS', 'HANDICAP', 'PETITE_ENFANCE'],
    requires: {
      diploma: 'DEME',
      driverLicense: true,
      criminalRecord: true,
    },
  },
  // ... EJE, AS, etc.
};
```

---

## 2. Compliance Rules

### Medical Requirements

```typescript
// domain-config.ts
const MEDICAL_COMPLIANCE: ComplianceRules = {
  requiredDocuments: [
    { type: 'DIPLOMA', label: 'Diplôme d\'État', required: true },
    { type: 'ADELI_PROOF', label: 'Attestation ADELI', required: true },
    { type: 'INSURANCE', label: 'RCP', required: true, expiresAfterMonths: 12 },
    { type: 'ID_CARD', label: 'CNI', required: true },
  ],
  requiresADELI: true,
  requiresDriverLicense: false,
  professionalBodyCheck: 'ADELI',
};
```

### Social Requirements

```typescript
const SOCIAL_COMPLIANCE: ComplianceRules = {
  requiredDocuments: [
    { type: 'DIPLOMA', label: 'Diplôme DEES/DEASS', required: true },
    { type: 'DRIVER_LICENSE', label: 'Permis B', required: true },
    { type: 'INSURANCE', label: 'RC Pro', required: true, expiresAfterMonths: 12 },
    { type: 'CRIMINAL_RECORD', label: 'Casier B3', required: true, expiresAfterMonths: 6 },
    { type: 'ID_CARD', label: 'CNI', required: true },
  ],
  requiresADELI: false,
  requiresDriverLicense: true,
  professionalBodyCheck: 'DRJSCS',
};
```

---

## 3. Matching Algorithm

### MatchingEngine Logic

```typescript
class MatchingEngineService {
  async findMatches(mission: ReliefMission): Promise<Profile[]> {
    // Step 1: Geo filter (Haversine)
    const inRadius = await this.geoFilter(mission);
    
    // Step 2: Job filter (exact match)
    const jobMatch = inRadius.filter(p => p.jobId === mission.jobId);
    
    // Step 3: Compliance check
    const compliant = jobMatch.filter(p => {
      if (mission.requiresDiploma) return p.complianceStatus === 'VALIDATED';
      if (mission.requiresCar) return p.hasDriverLicense;
      if (mission.requiresNight) return p.canDoNightShift;
      return true;
    });
    
    // Step 4: Specialty scoring (0-100)
    const scored = compliant.map(talent => ({
      talent,
      score: this.scoreSpecialties(talent.specialties, mission.specialtiesTags),
    }));
    
    // Step 5: Sort by score + rating
    return scored
      .sort((a, b) => {
        if (b.score !== a.score) return b.score - a.score;
        return b.talent.averageRating - a.talent.averageRating;
      })
      .slice(0, 3)
      .map(s => s.talent);
  }
  
  private scoreSpecialties(talentSpecs: string[], missionSpecs: string[]): number {
    const overlap = talentSpecs.filter(s => missionSpecs.includes(s)).length;
    return (overlap / missionSpecs.length) * 100;
  }
}
```

---

## 4. Terminology Mapping

### Dynamic Terms

```typescript
// Usage in components
import { getTerm } from '@/lib/domain-config';

<h1>{getTerm('mission')}</h1>
// Medical: "Vacation"
// Social: "Mission"

<p>{getTerm('urgentAction')}</p>
// Medical: "Vacation urgente"
// Social: "Mission SOS"
```

### Full Mapping

```typescript
MEDICAL_TERMS = {
  mission: 'Vacation',
  talent: 'Soignant',
  client: 'Établissement',
  booking: 'Garde',
  urgentAction: 'Vacation urgente',
};

SOCIAL_TERMS = {
  mission: 'Mission',
  talent: 'Intervenant',
  client: 'Structure',
  booking: 'Réservation',
  urgentAction: 'Mission SOS',
};
```

---

## 5. Feature Flags

### Conditional Features

```typescript
import { isFeatureEnabled } from '@/lib/domain-config';

// Show workshops only in Social mode
{isFeatureEnabled('enableWorkshops') && (
  <CatalogueSection />
)}

// Show critical urgency only in Medical mode
{isFeatureEnabled('enableCriticalUrgency') && (
  <UrgencyBadge level="CRITICAL" />
)}
```

### Full Feature Matrix

```typescript
MEDICAL_FEATURES = {
  enableWorkshops: false,
  enableShiftView: true,
  enablePortfolio: false,
  enableJobTicker: true,
  enableCriticalUrgency: true,
  enableProjects: false,
};

SOCIAL_FEATURES = {
  enableWorkshops: true,
  enableShiftView: false,
  enablePortfolio: true,
  enableJobTicker: false,
  enableCriticalUrgency: false,
  enableProjects: true,
};
```

---

## 6. Best Practices

### DO

✅ Use `getTerm()` instead of hardcoded strings  
✅ Check `isFeatureEnabled()` before rendering  
✅ Validate compliance before matching  
✅ Use typed enums from `@sociopulse/types`

### DON'T

❌ Hardcode job labels (use `sos-config.ts`)  
❌ Skip compliance checks (legal risk)  
❌ Create new enums in code (extend `schema.prisma`)

---

*This business logic architecture ensures legal compliance and domain-specific behavior through configuration-driven design.*
