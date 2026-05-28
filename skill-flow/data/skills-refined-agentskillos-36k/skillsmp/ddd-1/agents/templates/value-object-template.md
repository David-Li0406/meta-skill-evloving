---
name: Value Object Template
description: |
  Template de scaffolding pour créer des Value Objects DDD.
  Génère des objets immuables définis par leurs attributs.
workflows:
  - id: scaffold-vo
    name: Scaffolding Value Object
    steps:
      - Identifier les attributs
      - Définir les validations
      - Implémenter l'égalité
      - Ajouter les comportements
---

# Value Object Template

## Responsabilité

Tu génères des **templates de Value Objects** immuables et auto-validants.

### Tu FAIS

- Générer des VO immuables
- Inclure validations et égalité
- Proposer les comportements métier
- Adapter au langage cible

### Tu NE FAIS PAS

- Créer des entities (→ `entities`)
- Gérer l'identité (→ `aggregates`)

---

## Template Structure

```mermaid
classDiagram
    class ValueObject~T~ {
        -props: T
        +equals(other: ValueObject~T~) boolean
        #validate() void
    }

    class Email {
        -value: string
        +create(value: string)$ Email
        +equals(other: Email) boolean
        +domain() string
    }

    class Money {
        -amount: Decimal
        -currency: Currency
        +of(amount, currency)$ Money
        +add(other: Money) Money
        +equals(other: Money) boolean
    }

    class Address {
        -street: string
        -city: string
        -postalCode: PostalCode
        +create(props)$ Address
        +format() string
    }

    ValueObject <|-- Email
    ValueObject <|-- Money
    ValueObject <|-- Address
```

---

## Patterns de Value Objects

### 1. Simple Value (Wrapper)

```typescript
// Email - Simple wrapper avec validation
export class Email {
  private static readonly REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  private constructor(private readonly _value: string) {}

  static create(value: string): Email {
    const normalized = value.trim().toLowerCase();
    if (!this.REGEX.test(normalized)) {
      throw new InvalidEmailError(value);
    }
    return new Email(normalized);
  }

  equals(other: Email): boolean {
    return this._value === other._value;
  }

  get value(): string { return this._value; }
  get domain(): string { return this._value.split('@')[1]; }

  toString(): string { return this._value; }
}
```

### 2. Composite Value

```typescript
// Address - Multiple attributs
export class Address {
  private constructor(
    private readonly _street: string,
    private readonly _city: string,
    private readonly _postalCode: PostalCode,
    private readonly _country: Country
  ) {}

  static create(props: AddressProps): Address {
    if (!props.street?.trim()) {
      throw new InvalidAddressError('Street is required');
    }
    if (!props.city?.trim()) {
      throw new InvalidAddressError('City is required');
    }
    return new Address(
      props.street.trim(),
      props.city.trim(),
      PostalCode.create(props.postalCode),
      Country.fromCode(props.countryCode)
    );
  }

  equals(other: Address): boolean {
    return this._street === other._street
      && this._city === other._city
      && this._postalCode.equals(other._postalCode)
      && this._country.equals(other._country);
  }

  format(): string {
    return `${this._street}\n${this._postalCode.value} ${this._city}\n${this._country.name}`;
  }

  get street(): string { return this._street; }
  get city(): string { return this._city; }
}
```

### 3. Range Value

```typescript
// DateRange - Intervalle avec invariants
export class DateRange {
  private constructor(
    private readonly _start: Date,
    private readonly _end: Date
  ) {}

  static create(start: Date, end: Date): DateRange {
    if (end <= start) {
      throw new InvalidDateRangeError('End must be after start');
    }
    return new DateRange(start, end);
  }

  contains(date: Date): boolean {
    return date >= this._start && date <= this._end;
  }

  overlaps(other: DateRange): boolean {
    return this._start < other._end && this._end > other._start;
  }

  durationInDays(): number {
    const ms = this._end.getTime() - this._start.getTime();
    return Math.ceil(ms / (1000 * 60 * 60 * 24));
  }

  equals(other: DateRange): boolean {
    return this._start.getTime() === other._start.getTime()
      && this._end.getTime() === other._end.getTime();
  }
}
```

### 4. Money (Classic DDD)

```typescript
// Money - Pattern classique avec opérations
export class Money {
  private constructor(
    private readonly _amount: Decimal,
    private readonly _currency: Currency
  ) {}

  static of(amount: number, currency: string): Money {
    return new Money(
      new Decimal(amount),
      Currency.fromCode(currency)
    );
  }

  static zero(currency: string): Money {
    return Money.of(0, currency);
  }

  add(other: Money): Money {
    this.ensureSameCurrency(other);
    return new Money(this._amount.plus(other._amount), this._currency);
  }

  subtract(other: Money): Money {
    this.ensureSameCurrency(other);
    return new Money(this._amount.minus(other._amount), this._currency);
  }

  multiply(factor: number): Money {
    return new Money(this._amount.times(factor), this._currency);
  }

  allocate(ratios: number[]): Money[] {
    // Martin Fowler's allocation algorithm
    const total = ratios.reduce((a, b) => a + b, 0);
    let remainder = this._amount;
    const results: Money[] = [];

    for (let i = 0; i < ratios.length - 1; i++) {
      const share = this._amount.times(ratios[i]).dividedBy(total).floor();
      results.push(new Money(share, this._currency));
      remainder = remainder.minus(share);
    }
    results.push(new Money(remainder, this._currency));

    return results;
  }

  isPositive(): boolean { return this._amount.greaterThan(0); }
  isNegative(): boolean { return this._amount.lessThan(0); }
  isZero(): boolean { return this._amount.equals(0); }

  equals(other: Money): boolean {
    return this._amount.equals(other._amount)
      && this._currency.equals(other._currency);
  }

  private ensureSameCurrency(other: Money): void {
    if (!this._currency.equals(other._currency)) {
      throw new CurrencyMismatchError(this._currency, other._currency);
    }
  }

  get amount(): number { return this._amount.toNumber(); }
  get currency(): Currency { return this._currency; }
}
```

---

## Checklist Value Object

| Check | Description |
|-------|-------------|
| [ ] **Immuable** | Pas de setters, tous les champs readonly |
| [ ] **Validé** | Factory method avec validation |
| [ ] **Égalité** | equals() compare les attributs |
| [ ] **Comportement** | Méthodes métier incluses |

---

## Mots-clés de routage

`value object`, `template vo`, `créer vo`, `money`, `email`, `address`
