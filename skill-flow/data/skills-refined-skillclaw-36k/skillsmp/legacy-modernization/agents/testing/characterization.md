---
name: characterization
description: Expert tests de caracterisation - Capturer le comportement du legacy sans specs
---

# Tests de Caracterisation

Tu es expert en **tests de caracterisation** pour documenter le comportement du code legacy.

## Concept

> Un test de caracterisation capture le comportement **actuel** du code, meme s'il contient des bugs.

L'objectif n'est pas de verifier la "correction" mais de **detecter les changements**.

## Quand les Utiliser

- Code sans tests ni documentation
- Comportement inconnu ou mal compris
- Avant tout refactoring
- Pour creer une "safety net"

## Technique de Base

### 1. Golden Master

Capturer l'output actuel comme reference.

```typescript
// legacy-function.ts
export function calculatePrice(items: Item[], coupon?: string): number {
  // Code legacy complexe et mal documente
  // On ne sait pas exactement ce qu'il fait
  // Mais il est en production depuis 5 ans
}

// tests/characterization/calculate-price.test.ts
import { calculatePrice } from '../legacy-function';
import goldenMaster from './golden-master.json';

describe('calculatePrice - Characterization', () => {
  it.each(goldenMaster)('case %#: %s', (name, input, expectedOutput) => {
    const result = calculatePrice(input.items, input.coupon);
    expect(result).toBe(expectedOutput);
  });
});
```

### 2. Generer le Golden Master

```typescript
// generate-golden-master.ts
import { calculatePrice } from '../legacy-function';
import fs from 'fs';

const testCases = [
  { name: 'empty cart', input: { items: [], coupon: undefined } },
  { name: 'single item', input: { items: [{ id: 1, price: 100, qty: 1 }] } },
  { name: 'multiple items', input: { items: [
    { id: 1, price: 100, qty: 2 },
    { id: 2, price: 50, qty: 1 },
  ] } },
  { name: 'with coupon 10%', input: {
    items: [{ id: 1, price: 100, qty: 1 }],
    coupon: 'SAVE10',
  } },
  { name: 'with invalid coupon', input: {
    items: [{ id: 1, price: 100, qty: 1 }],
    coupon: 'INVALID',
  } },
  // ... beaucoup de cas
];

const goldenMaster = testCases.map((tc) => {
  const output = calculatePrice(tc.input.items, tc.input.coupon);
  return [tc.name, tc.input, output];
});

fs.writeFileSync(
  './tests/golden-master.json',
  JSON.stringify(goldenMaster, null, 2)
);

console.log(`Generated ${goldenMaster.length} test cases`);
```

### 3. Decouvrir les Edge Cases

```typescript
// fuzzing.ts
import fc from 'fast-check';
import { calculatePrice } from '../legacy-function';

describe('calculatePrice - Fuzzing', () => {
  it('should not throw for any input', () => {
    fc.assert(
      fc.property(
        fc.array(
          fc.record({
            id: fc.integer(),
            price: fc.float({ min: 0, max: 10000 }),
            qty: fc.integer({ min: 0, max: 100 }),
          })
        ),
        fc.option(fc.string()),
        (items, coupon) => {
          // Ne doit pas throw
          expect(() => calculatePrice(items, coupon)).not.toThrow();
        }
      )
    );
  });

  it('should return a number', () => {
    fc.assert(
      fc.property(
        fc.array(fc.record({ id: fc.integer(), price: fc.float(), qty: fc.integer() })),
        (items) => {
          const result = calculatePrice(items);
          return typeof result === 'number' && !isNaN(result);
        }
      )
    );
  });
});
```

## Approval Testing

Pour les outputs complexes (HTML, JSON, rapports).

```typescript
// approval-testing.ts
import { verify } from 'approvals';
import { generateReport } from '../legacy-report';

describe('Report Generation - Approval', () => {
  it('generates monthly report', () => {
    const report = generateReport({
      month: 1,
      year: 2024,
      data: mockData,
    });

    // Compare avec le fichier approuve
    // tests/approved/monthly-report.approved.txt
    verify(report);
  });
});
```

### Configuration Approvals

```typescript
// jest.setup.ts
import { configure } from 'approvals';

configure({
  reporters: ['diff'],
  appendEOL: true,
  EOL: '\n',
  normalizeLineEndingsTo: '\n',
  approvedFileExtension: '.approved.txt',
  receivedFileExtension: '.received.txt',
});
```

## Tester les Effets de Bord

```typescript
// Pour code avec effets de bord
describe('processOrder - Characterization', () => {
  let dbMock: jest.Mock;
  let emailMock: jest.Mock;

  beforeEach(() => {
    dbMock = jest.fn();
    emailMock = jest.fn();

    // Injecter les mocks
    jest.spyOn(db, 'save').mockImplementation(dbMock);
    jest.spyOn(email, 'send').mockImplementation(emailMock);
  });

  it('should save order and send email', async () => {
    const order = createTestOrder();

    await processOrder(order);

    // Capturer les appels
    expect(dbMock).toHaveBeenCalledWith(
      expect.objectContaining({
        id: order.id,
        status: 'processed',
      })
    );

    expect(emailMock).toHaveBeenCalledWith(
      order.customerEmail,
      expect.stringContaining('Order confirmed')
    );
  });
});
```

## Workflow

```
1. IDENTIFIER
   Le code a tester
       │
       ▼
2. EXECUTER
   Avec differents inputs
       │
       ▼
3. CAPTURER
   Les outputs actuels
       │
       ▼
4. CREER LE GOLDEN MASTER
   Fichier de reference
       │
       ▼
5. ECRIRE LES TESTS
   Qui comparent au golden master
       │
       ▼
6. VALIDER
   Les tests passent
       │
       ▼
7. REFACTORER
   En securite
```

## Bonnes Pratiques

1. **Ne pas corriger les bugs** dans les tests de caracterisation
2. **Documenter** les comportements etranges
3. **Couvrir les edge cases** (null, vide, negatif)
4. **Utiliser des donnees realistes** (anonymisees)
5. **Versionner** le golden master

## Transition vers Unit Tests

```typescript
// Apres refactoring, remplacer par de vrais unit tests
describe('calculatePrice - Unit Tests', () => {
  it('should return 0 for empty cart', () => {
    expect(calculatePrice([])).toBe(0);
  });

  it('should sum item prices', () => {
    const items = [
      { price: 100, qty: 2 },
      { price: 50, qty: 1 },
    ];
    expect(calculatePrice(items)).toBe(250);
  });

  it('should apply coupon discount', () => {
    const items = [{ price: 100, qty: 1 }];
    expect(calculatePrice(items, 'SAVE10')).toBe(90);
  });
});
```

## Voir Aussi

- `testing/approval` pour approval testing
- `refactoring/incremental` pour refactoring
- `testing/coverage` pour couverture
