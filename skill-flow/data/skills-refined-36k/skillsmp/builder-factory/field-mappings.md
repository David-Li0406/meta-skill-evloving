# Builder Field Mappings

Mapping field types to appropriate Faker methods.

> **Note:** Check `.claude/project-context.md` for locale-specific values (currency, country, etc.)

## Identifiers

```typescript
id: sequence()
id: sequence((n) => `user-${n}`)
uuid: perBuild(() => faker.string.uuid())
slug: perBuild(() => faker.helpers.slugify(faker.lorem.words(3)))
```

## Personal Data

```typescript
firstName: perBuild(() => faker.person.firstName())
lastName: perBuild(() => faker.person.lastName())
email: perBuild(() => faker.internet.email())
email: sequence((n) => `user${n}@test.com`)  // Unique sequential
phone: perBuild(() => faker.phone.number())
avatar: perBuild(() => faker.image.avatar())
```

## Addresses

```typescript
street: perBuild(() => faker.location.streetAddress())
city: perBuild(() => faker.location.city())
zipCode: perBuild(() => faker.location.zipCode())
country: perBuild(() => faker.location.country())
// Or use static value for your locale:
// country: "USA"  // Check project-context.md for your locale
```

## Commerce

```typescript
productName: perBuild(() => faker.commerce.productName())
price: perBuild(() => parseFloat(faker.commerce.price({ min: 10, max: 1000 })))
currency: "USD"  // Check project-context.md for your locale currency
category: perBuild(() => faker.commerce.department())
```

## Text Content

```typescript
title: perBuild(() => faker.lorem.sentence())
description: perBuild(() => faker.lorem.paragraph())
text: perBuild(() => faker.lorem.text())
```

## Numbers

```typescript
amount: perBuild(() => faker.number.float({ min: 0, max: 1000, fractionDigits: 2 }))
count: perBuild(() => faker.number.int({ min: 0, max: 100 }))
percentage: perBuild(() => faker.number.int({ min: 0, max: 100 }))
```

## Dates

```typescript
createdAt: perBuild(() => faker.date.past())
updatedAt: perBuild(() => faker.date.recent())
scheduledAt: perBuild(() => faker.date.future())
birthDate: perBuild(() => faker.date.birthdate({ min: 18, max: 65, mode: 'age' }))
```

## Booleans

```typescript
isActive: perBuild(() => faker.datatype.boolean())
isPredefined: true  // Static value
```

## Enums/Unions

```typescript
status: perBuild(() => faker.helpers.arrayElement(["active", "inactive", "pending"]))
role: perBuild(() => faker.helpers.arrayElement(["admin", "user", "guest"] as const))
```

## Arrays

```typescript
tags: perBuild(() => faker.helpers.arrayElements(["tag1", "tag2", "tag3"], { min: 1, max: 3 }))
items: perBuild(() => Array.from({ length: 3 }, () => itemBuilder.one()))
images: perBuild(() => Array.from({ length: 3 }, () => faker.image.url()))
```

## Common Patterns

```typescript
// Percentage/Allocation
allocation: perBuild(() => faker.number.int({ min: 0, max: 100 }))

// Currency Amounts
amount: perBuild(() => faker.number.float({ min: 0, max: 10000, fractionDigits: 2 }))

// Icons (common icon names)
icon: perBuild(() => faker.helpers.arrayElement(["home", "user", "settings", "search"]))

// Colors (Tailwind palette)
color: perBuild(() => faker.helpers.arrayElement(["red", "blue", "green", "yellow"]))
```
