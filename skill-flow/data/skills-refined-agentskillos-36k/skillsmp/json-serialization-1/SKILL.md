---
name: json-serialization
description: High-performance JSON serialization patterns using System.Text.Json with custom converters and polymorphism.
---
# JSON Serialization (System.Text.Json)

High-performance JSON serialization patterns from forex project.

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
            WriteIndented = pretty,
            DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
        };

        if (camelCase)
            options.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;

        // Add custom converters
        options.Converters.Add(new JsonStringEnumConverter());
        options.Converters.Add(new DateOnlyConverter());
        options.Converters.Add(new NullableDateOnlyConverter());
        options.Converters.Add(new TimeOnlyConverter());
        options.Converters.Add(new NullableTimeOnlyConverter());
        options.Converters.Add(new DecimalConverterWithStringSupport());
        options.Converters.Add(new NullableDecimalConverterWithStringSupport());
        options.Converters.Add(new Int32ConverterWithStringSupport());
        options.Converters.Add(new NullableInt32ConverterWithStringSupport());

        return options;
    }

    // Extension methods
    public static T? DeserializeFromJson<T>(this string json, JsonSerializerOptions? options = null)
    {
        if (string.IsNullOrWhiteSpace(json))
            return default;
        options ??= s_defaultOptions;
        return JsonSerializer.Deserialize<T>(json, options);
    }

    public static string ToJsonString<T>(this T value, bool pretty = false, bool camelCase = false)
    {
        if (pretty)
            return JsonSerializer.Serialize(value, s_prettyOptions);
        if (camelCase)
            return JsonSerializer.Serialize(value, s_camelCaseOptions);
        return JsonSerializer.Serialize(value, s_defaultOptions);
    }

    // Polymorphic serialization for entities
    public static string ToJson(this Entity entity)
    {
        return JsonSerializer.Serialize<Entity>(entity, s_defaultOptions);
        // Produces: { "$type": "Rental", "RentalId": 1, ... }
    }

    public static Entity? DeserializeEntity(string json)
    {
        return JsonSerializer.Deserialize<Entity>(json, s_defaultOptions);
        // Automatically resolves to correct derived type
    }

    // Deep clone via JSON
    public static T Clone<T>(this T source) where T : class
    {
        var json = source.ToJsonString();
        return json.DeserializeFromJson<T>()!;
    }
}
```

## High-Performance Converters

### DecimalConverterWithStringSupport

```csharp
using System.Buffers;
using System.Buffers.Text;

public class DecimalConverterWithStringSupport : JsonConverter<decimal>
{
    public override decimal Read(ref Utf8JsonReader reader, Type type, JsonSerializerOptions options)
    {
        if (reader.TokenType == JsonTokenType.String)
        {
            // Use Utf8Parser for maximum performance
            var span = reader.HasValueSequence
                ? reader.ValueSequence.ToArray()
                : reader.ValueSpan;

            if (Utf8Parser.TryParse(span, out decimal number, out int bytesConsumed) &&
                span.Length == bytesConsumed)
                return number;

            // Fallback to string parsing
            if (decimal.TryParse(reader.GetString(), out number))
                return number;
        }
        return reader.GetDecimal();
    }

    public override void Write(Utf8JsonWriter writer, decimal value, JsonSerializerOptions options)
        => writer.WriteNumberValue(value);
}
```

### DateOnlyConverter

```csharp
public class DateOnlyConverter : JsonConverter<DateOnly>
{
    private const string Format = "yyyy-MM-dd";

    public override DateOnly Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        var value = reader.GetString();
        if (string.IsNullOrEmpty(value))
            return default;

        if (value.Length >= 10)
            return DateOnly.ParseExact(value[..10], Format);

        return DateOnly.Parse(value);
    }

    public override void Write(Utf8JsonWriter writer, DateOnly value, JsonSerializerOptions options)
        => writer.WriteStringValue(value.ToString(Format));
}
```

## Usage Examples

### Basic Serialization

```csharp
var rental = new Rental { RentalId = 1, Status = "Active" };

// Serialize
string json = rental.ToJsonString();

// Serialize pretty
string prettyJson = rental.ToJsonString(pretty: true);

// Serialize for API (camelCase)
string apiJson = rental.ToJsonString(camelCase: true);

// Deserialize
var restored = json.DeserializeFromJson<Rental>();
```

### Polymorphic Serialization

```csharp
// Serialize with type discriminator (for messaging)
Entity entity = new Rental { RentalId = 1, Status = "Active" };
string json = entity.ToJson();
// Output: { "$type": "Rental", "RentalId": 1, "Status": "Active", ... }

// Deserialize polymorphically
Entity restored = JsonSerializerService.DeserializeEntity(json)!;
if (restored is Rental rental)
{
    Console.WriteLine(rental.Status);  // "Active"
}
```

### Clone Pattern

```csharp
// Clone entity before editing in dialog
var originalRental = await context.LoadOneAsync<Rental>(r => r.RentalId == id);
var editCopy = originalRental.Clone();

// Pass editCopy to dialog, original unchanged if cancelled
```

## File Locations

```
MotoRent.Domain/
├── Core/
│   └── JsonSerializerService.cs
└── JsonSupports/
    ├── DateOnlyConverter.cs
    ├── TimeOnlyConverter.cs
    ├── DecimalConverterWithStringSupport.cs
    └── Int32ConverterWithStringSupport.cs
```

## Source
- From: `D:\project\work\forex` project
