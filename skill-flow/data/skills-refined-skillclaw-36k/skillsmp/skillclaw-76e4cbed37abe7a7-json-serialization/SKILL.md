---
name: json-serialization
description: Use this skill when you need to implement high-performance JSON serialization in .NET using System.Text.Json, including support for custom converters and polymorphism.
---

# JSON Serialization (System.Text.Json)

High-performance JSON serialization patterns using System.Text.Json.

## Overview

| Feature | Implementation |
|---------|----------------|
| Library | System.Text.Json (.NET built-in) |
| Polymorphism | JsonPolymorphic + JsonDerivedType attributes |
| Performance | Utf8Parser for high-speed parsing |
| Custom converters | DateOnly, TimeOnly, Decimal, Int32 |

## Why System.Text.Json?

- **Performance**: 2-3x faster than Newtonsoft.Json
- **Memory**: Lower allocations with Utf8JsonReader/Writer
- **Native**: Built into .NET, no external dependency
- **AOT-friendly**: Works with Native AOT compilation

## Entity Polymorphism

```csharp
// Entity base class with polymorphism support
[JsonPolymorphic(TypeDiscriminatorPropertyName = "$type")]
[JsonDerivedType(typeof(Rental), nameof(Rental))]
[JsonDerivedType(typeof(Renter), nameof(Renter))]
[JsonDerivedType(typeof(Motorbike), nameof(Motorbike))]
[JsonDerivedType(typeof(Payment), nameof(Payment))]
[JsonDerivedType(typeof(Deposit), nameof(Deposit))]
[JsonDerivedType(typeof(DamageReport), nameof(DamageReport))]
[JsonDerivedType(typeof(Document), nameof(Document))]
[JsonDerivedType(typeof(Insurance), nameof(Insurance))]
[JsonDerivedType(typeof(Accessory), nameof(Accessory))]
[JsonDerivedType(typeof(Shop), nameof(Shop))]
[JsonDerivedType(typeof(RentalAgreement), nameof(RentalAgreement))]
public abstract class Entity
{
    public string? WebId { get; set; }

    [JsonIgnore]
    public string? CreatedBy { get; set; }

    [JsonIgnore]
    public DateTimeOffset CreatedTimestamp { get; set; }

    [JsonIgnore]
    public string? ChangedBy { get; set; }

    [JsonIgnore]
    public DateTimeOffset ChangedTimestamp { get; set; }

    public abstract int GetId();
    public abstract void SetId(int value);
}
```

## JsonSerializerService

```csharp
// MotoRent.Domain/Core/JsonSerializerService.cs
public static class JsonSerializerService
{
    private static readonly JsonSerializerOptions s_defaultOptions = CreateOptions();
    private static readonly JsonSerializerOptions s_camelCaseOptions = CreateOptions(camelCase: true);

    private static JsonSerializerOptions CreateOptions(bool camelCase = false, bool pretty = false)
    {
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            // Additional options can be set here
        };
        return options;
    }
}
```