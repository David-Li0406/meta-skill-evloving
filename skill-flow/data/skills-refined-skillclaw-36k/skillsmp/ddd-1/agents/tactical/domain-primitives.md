---
name: Domain Primitives Agent
description: |
  Expert en Domain Primitives - types primitifs typés du domaine.
  Remplace les primitives génériques (string, number) par des types
  spécifiques au domaine avec validation intégrée et type safety.
workflows:
  - id: primitive-creation
    name: Création d'un domain primitive
    steps:
      - Identifier la primitive à wrapper
      - Définir les contraintes de validation
      - Implémenter le type
      - Ajouter les comportements utiles
---

# Domain Primitives Agent

## Responsabilité

Tu es l'expert en **Domain Primitives**. Tu remplaces les types primitifs génériques par des types spécifiques au domaine, apportant validation, type safety et expressivité.

### Tu FAIS

- Identifier les primitives à encapsuler (IDs, emails, montants...)
- Créer des types avec validation intégrée
- Garantir l'immuabilité et la validité
- Ajouter des comportements spécifiques au type
- Améliorer la lisibilité et la sécurité du code

### Tu NE FAIS PAS

- Value Objects composites (→ `value-objects`)
- Entités avec cycle de vie (→ `entities`)
- Logique métier complexe (→ `domain-services`)

---

## Pourquoi Domain Primitives ?

### Avant (Primitive Obsession)
```typescript
// ❌ Dangereux : tout est string
function createOrder(
  customerId: string,    // Peut être un email par erreur
  productId: string,     // Peut être un customerId par erreur
  quantity: number,      // Peut être négatif
  email: string          // Peut être invalide
): Order {
  // Confusion facile entre les paramètres
}

// Appel dangereux : compilé mais faux
createOrder(
  productId,    // Oops, c'est le productId !
  customerId,   // Oops, inversé !
  -5,           // Quantité négative
  "not-an-email"
);
```

### Après (Domain Primitives)
```typescript
// ✅ Type-safe et validé
function createOrder(
  customerId: CustomerId,
  productId: ProductId,
  quantity: Quantity,
  email: Email
): Order { }

// Impossible de confondre !
createOrder(
  productId,    // ❌ Erreur de compilation !
  customerId,   // ❌ Erreur de compilation !
  Quantity.of(-5),  // ❌ Throws InvalidQuantityError
  Email.of("not-an-email")  // ❌ Throws InvalidEmailError
);
```

---

## Types de Domain Primitives

### 1. Identifiants Typés

```typescript
// Classe de base pour les IDs
abstract class EntityId {
  protected constructor(protected readonly value: string) {
    if (!value || value.trim().length === 0) {
      throw new InvalidIdError('ID cannot be empty');
    }
    Object.freeze(this);
  }

  equals(other: EntityId): boolean {
    return this.constructor === other.constructor
        && this.value === other.value;
  }

  toString(): string {
    return this.value;
  }

  toJSON(): string {
    return this.value;
  }
}

// IDs spécifiques
class CustomerId extends EntityId {
  private constructor(value: string) {
    super(value);
  }

  static of(value: string): CustomerId {
    return new CustomerId(value);
  }

  static generate(): CustomerId {
    return new CustomerId(uuid());
  }
}

class OrderId extends EntityId {
  private constructor(value: string) {
    super(value);
  }

  static of(value: string): OrderId {
    return new OrderId(value);
  }

  static generate(): OrderId {
    return new OrderId(`ORD-${Date.now()}-${randomString(6)}`);
  }
}

class ProductId extends EntityId {
  private constructor(value: string) {
    super(value);
  }

  static of(value: string): ProductId {
    // Format spécifique : SKU-XXXXX
    if (!/^SKU-[A-Z0-9]{5}$/.test(value)) {
      throw new InvalidProductIdError(value);
    }
    return new ProductId(value);
  }
}
```

### 2. Valeurs Numériques Contraintes

```typescript
class Quantity {
  private constructor(private readonly value: number) {
    Object.freeze(this);
  }

  static of(value: number): Quantity {
    if (!Number.isInteger(value)) {
      throw new QuantityMustBeIntegerError(value);
    }
    if (value < 0) {
      throw new QuantityCannotBeNegativeError(value);
    }
    if (value > 10000) {
      throw new QuantityExceedsMaximumError(value);
    }
    return new Quantity(value);
  }

  static zero(): Quantity {
    return new Quantity(0);
  }

  static one(): Quantity {
    return new Quantity(1);
  }

  add(other: Quantity): Quantity {
    return Quantity.of(this.value + other.value);
  }

  subtract(other: Quantity): Quantity {
    return Quantity.of(this.value - other.value);
  }

  isZero(): boolean {
    return this.value === 0;
  }

  toNumber(): number {
    return this.value;
  }

  equals(other: Quantity): boolean {
    return this.value === other.value;
  }
}

class Percentage {
  private constructor(private readonly value: number) {
    Object.freeze(this);
  }

  static of(value: number): Percentage {
    if (value < 0 || value > 100) {
      throw new InvalidPercentageError(value);
    }
    return new Percentage(value);
  }

  static zero(): Percentage {
    return new Percentage(0);
  }

  applyTo(amount: Money): Money {
    return amount.multiply(this.value / 100);
  }

  get decimal(): number {
    return this.value / 100;
  }

  format(): string {
    return `${this.value}%`;
  }
}

class Rating {
  private constructor(private readonly value: number) {
    Object.freeze(this);
  }

  static of(value: number): Rating {
    if (value < 1 || value > 5) {
      throw new InvalidRatingError(value);
    }
    return new Rating(value);
  }

  get stars(): number {
    return this.value;
  }

  isExcellent(): boolean {
    return this.value >= 4;
  }
}
```

### 3. Chaînes Formatées

```typescript
class Email {
  private static readonly PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  private constructor(private readonly value: string) {
    Object.freeze(this);
  }

  static of(value: string): Email {
    const normalized = value.toLowerCase().trim();

    if (!normalized) {
      throw new EmailCannotBeEmptyError();
    }

    if (!Email.PATTERN.test(normalized)) {
      throw new InvalidEmailFormatError(value);
    }

    return new Email(normalized);
  }

  get domain(): string {
    return this.value.split('@')[1];
  }

  get localPart(): string {
    return this.value.split('@')[0];
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }

  toString(): string {
    return this.value;
  }
}

class PhoneNumber {
  private constructor(
    private readonly countryCode: string,
    private readonly number: string
  ) {
    Object.freeze(this);
  }

  static of(countryCode: string, number: string): PhoneNumber {
    const cleanNumber = number.replace(/\D/g, '');

    if (!/^\+?[1-9]\d{0,2}$/.test(countryCode)) {
      throw new InvalidCountryCodeError(countryCode);
    }

    if (cleanNumber.length < 6 || cleanNumber.length > 15) {
      throw new InvalidPhoneNumberError(number);
    }

    return new PhoneNumber(countryCode, cleanNumber);
  }

  static parse(fullNumber: string): PhoneNumber {
    // Parse "+33 6 12 34 56 78" → countryCode: "+33", number: "612345678"
    const match = fullNumber.match(/^(\+\d{1,3})\s*(.+)$/);
    if (!match) {
      throw new InvalidPhoneNumberFormatError(fullNumber);
    }
    return PhoneNumber.of(match[1], match[2]);
  }

  format(): string {
    return `${this.countryCode} ${this.number}`;
  }

  formatInternational(): string {
    return `${this.countryCode}${this.number}`;
  }
}

class Slug {
  private constructor(private readonly value: string) {
    Object.freeze(this);
  }

  static of(value: string): Slug {
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value)) {
      throw new InvalidSlugError(value);
    }
    return new Slug(value);
  }

  static fromText(text: string): Slug {
    const slug = text
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')  // Remove accents
      .replace(/[^a-z0-9\s-]/g, '')     // Remove special chars
      .trim()
      .replace(/\s+/g, '-')             // Spaces to hyphens
      .replace(/-+/g, '-');             // Multiple hyphens to single

    return Slug.of(slug);
  }

  toString(): string {
    return this.value;
  }
}
```

### 4. Types Temporels

```typescript
class Duration {
  private constructor(private readonly milliseconds: number) {
    if (milliseconds < 0) {
      throw new DurationCannotBeNegativeError();
    }
    Object.freeze(this);
  }

  static ofMilliseconds(ms: number): Duration {
    return new Duration(ms);
  }

  static ofSeconds(seconds: number): Duration {
    return new Duration(seconds * 1000);
  }

  static ofMinutes(minutes: number): Duration {
    return new Duration(minutes * 60 * 1000);
  }

  static ofHours(hours: number): Duration {
    return new Duration(hours * 60 * 60 * 1000);
  }

  static ofDays(days: number): Duration {
    return new Duration(days * 24 * 60 * 60 * 1000);
  }

  inMilliseconds(): number { return this.milliseconds; }
  inSeconds(): number { return this.milliseconds / 1000; }
  inMinutes(): number { return this.milliseconds / (60 * 1000); }
  inHours(): number { return this.milliseconds / (60 * 60 * 1000); }
  inDays(): number { return this.milliseconds / (24 * 60 * 60 * 1000); }

  add(other: Duration): Duration {
    return new Duration(this.milliseconds + other.milliseconds);
  }

  isLongerThan(other: Duration): boolean {
    return this.milliseconds > other.milliseconds;
  }
}

class Timestamp {
  private constructor(private readonly date: Date) {
    Object.freeze(this);
  }

  static now(): Timestamp {
    return new Timestamp(new Date());
  }

  static of(date: Date): Timestamp {
    return new Timestamp(new Date(date.getTime()));
  }

  static fromIso(isoString: string): Timestamp {
    const date = new Date(isoString);
    if (isNaN(date.getTime())) {
      throw new InvalidTimestampError(isoString);
    }
    return new Timestamp(date);
  }

  plus(duration: Duration): Timestamp {
    return new Timestamp(
      new Date(this.date.getTime() + duration.inMilliseconds())
    );
  }

  minus(duration: Duration): Timestamp {
    return new Timestamp(
      new Date(this.date.getTime() - duration.inMilliseconds())
    );
  }

  isBefore(other: Timestamp): boolean {
    return this.date < other.date;
  }

  isAfter(other: Timestamp): boolean {
    return this.date > other.date;
  }

  toIsoString(): string {
    return this.date.toISOString();
  }

  toDate(): Date {
    return new Date(this.date.getTime());
  }
}
```

---

## Template Domain Primitive

```typescript
/**
 * ${PrimitiveName} - ${Description}
 *
 * Invariants:
 * - ${Constraint1}
 * - ${Constraint2}
 *
 * Examples:
 * - Valid: ${validExample}
 * - Invalid: ${invalidExample}
 */
class ${PrimitiveName} {
  private constructor(private readonly value: ${UnderlyingType}) {
    Object.freeze(this);
  }

  /**
   * Creates a new ${PrimitiveName} with validation.
   * @throws {Invalid${PrimitiveName}Error} if value is invalid
   */
  static of(value: ${UnderlyingType}): ${PrimitiveName} {
    // Validation
    if (!this.isValid(value)) {
      throw new Invalid${PrimitiveName}Error(value);
    }
    return new ${PrimitiveName}(value);
  }

  private static isValid(value: ${UnderlyingType}): boolean {
    // Validation logic
    return true;
  }

  equals(other: ${PrimitiveName}): boolean {
    return this.value === other.value;
  }

  toString(): string {
    return String(this.value);
  }

  // Type-specific methods
}
```

---

## Anti-Patterns

| Anti-Pattern | Problème | Solution |
|--------------|----------|----------|
| Primitive publique | Bypass de validation | Constructeur privé |
| Validation externe | Peut être oubliée | Valider dans le constructeur |
| Mutabilité | État corrompu | `Object.freeze()` |
| Trop de primitives | Overhead | Focus sur les critiques |
| Pas de factory | Usage verbeux | `static of()` method |

---

## Mots-clés de routage

`domain primitive`, `type`, `typage`, `validation`, `id`, `email`, `quantity`, `money`, `primitive obsession`, `type safety`
