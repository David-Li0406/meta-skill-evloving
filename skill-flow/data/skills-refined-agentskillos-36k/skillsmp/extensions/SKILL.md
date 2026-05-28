---
name: extensions
description: Generic extension methods for strings, collections, DateTime, decimals, and entities.
---
# Extension Methods

Generic extension methods for common operations.

## String Extensions

```csharp
// Extensions/StringExtensions.cs
public static class StringExtensions
{
    /// <summary>
    /// Check if string is null, empty, or whitespace
    /// </summary>
    public static bool IsNullOrEmpty(this string? value)
        => string.IsNullOrWhiteSpace(value);

    /// <summary>
    /// Check if string has content
    /// </summary>
    public static bool HasValue(this string? value)
        => !string.IsNullOrWhiteSpace(value);

    /// <summary>
    /// Truncate string to max length with ellipsis
    /// </summary>
    public static string Truncate(this string value, int maxLength, string suffix = "...")
    {
        if (string.IsNullOrEmpty(value) || value.Length <= maxLength)
            return value;

        return value[..(maxLength - suffix.Length)] + suffix;
    }

    /// <summary>
    /// Convert to title case
    /// </summary>
    public static string ToTitleCase(this string value)
        => CultureInfo.CurrentCulture.TextInfo.ToTitleCase(value.ToLower());

    /// <summary>
    /// Format phone number for Thailand
    /// </summary>
    public static string FormatThaiPhone(this string phone)
    {
        var digits = new string(phone.Where(char.IsDigit).ToArray());
        return digits.Length == 10
            ? $"{digits[..3]}-{digits[3..6]}-{digits[6..]}"
            : phone;
    }
}
```

## Collection Extensions

```csharp
// Extensions/CollectionExtensions.cs
public static class CollectionExtensions
{
    /// <summary>
    /// Add or replace item in list
    /// </summary>
    public static void AddOrReplace<T>(this List<T> list, T item, Func<T, bool> predicate)
    {
        var index = list.FindIndex(x => predicate(x));
        if (index >= 0)
            list[index] = item;
        else
            list.Add(item);
    }

    /// <summary>
    /// Clear and add range
    /// </summary>
    public static void ClearAndAddRange<T>(this List<T> list, IEnumerable<T> items)
    {
        list.Clear();
        list.AddRange(items);
    }

    /// <summary>
    /// Check if collection is empty
    /// </summary>
    public static bool IsEmpty<T>(this IEnumerable<T> source)
        => !source.Any();

    /// <summary>
    /// Check if collection has items
    /// </summary>
    public static bool HasItems<T>(this IEnumerable<T> source)
        => source.Any();

    /// <summary>
    /// Safe first or default with predicate
    /// </summary>
    public static T? SafeFirst<T>(this IEnumerable<T>? source, Func<T, bool>? predicate = null)
    {
        if (source is null)
            return default;

        return predicate is null
            ? source.FirstOrDefault()
            : source.FirstOrDefault(predicate);
    }

    /// <summary>
    /// ForEach for IEnumerable
    /// </summary>
    public static void ForEach<T>(this IEnumerable<T> source, Action<T> action)
    {
        foreach (var item in source)
            action(item);
    }

    /// <summary>
    /// Batch items into chunks
    /// </summary>
    public static IEnumerable<IEnumerable<T>> Batch<T>(this IEnumerable<T> source, int size)
    {
        var batch = new List<T>(size);
        foreach (var item in source)
        {
            batch.Add(item);
            if (batch.Count == size)
            {
                yield return batch;
                batch = new List<T>(size);
            }
        }
        if (batch.Count > 0)
            yield return batch;
    }
}
```

## DateTime Extensions

```csharp
// Extensions/DateTimeExtensions.cs
public static class DateTimeExtensions
{
    /// <summary>
    /// Get Thailand timezone (UTC+7)
    /// </summary>
    private static readonly TimeZoneInfo ThailandTimeZone =
        TimeZoneInfo.FindSystemTimeZoneById("SE Asia Standard Time");

    /// <summary>
    /// Convert to Thailand local time
    /// </summary>
    public static DateTimeOffset ToThailandTime(this DateTimeOffset utc)
        => TimeZoneInfo.ConvertTime(utc, ThailandTimeZone);

    /// <summary>
    /// Get current Thailand time
    /// </summary>
    public static DateTimeOffset ThailandNow()
        => TimeZoneInfo.ConvertTime(DateTimeOffset.UtcNow, ThailandTimeZone);

    /// <summary>
    /// Format for Thai display
    /// </summary>
    public static string ToThaiDateString(this DateTimeOffset date)
        => date.ToThailandTime().ToString("dd MMM yyyy");

    /// <summary>
    /// Format with time
    /// </summary>
    public static string ToThaiDateTimeString(this DateTimeOffset date)
        => date.ToThailandTime().ToString("dd MMM yyyy HH:mm");

    /// <summary>
    /// Get start of day
    /// </summary>
    public static DateTimeOffset StartOfDay(this DateTimeOffset date)
        => new(date.Year, date.Month, date.Day, 0, 0, 0, date.Offset);

    /// <summary>
    /// Get end of day
    /// </summary>
    public static DateTimeOffset EndOfDay(this DateTimeOffset date)
        => new(date.Year, date.Month, date.Day, 23, 59, 59, 999, date.Offset);

    /// <summary>
    /// Calculate age from birthdate
    /// </summary>
    public static int CalculateAge(this DateOnly birthDate)
    {
        var today = DateOnly.FromDateTime(DateTime.Today);
        var age = today.Year - birthDate.Year;
        if (birthDate > today.AddYears(-age))
            age--;
        return age;
    }

    /// <summary>
    /// Calculate rental days
    /// </summary>
    public static int CalculateRentalDays(this DateTimeOffset start, DateTimeOffset end)
        => (int)Math.Ceiling((end - start).TotalDays);
}
```

## Decimal Extensions

```csharp
// Extensions/DecimalExtensions.cs
public static class DecimalExtensions
{
    /// <summary>
    /// Format as Thai Baht
    /// </summary>
    public static string ToThb(this decimal amount)
        => $"{amount:N0} THB";

    /// <summary>
    /// Format as Thai Baht with decimals
    /// </summary>
    public static string ToThbDecimal(this decimal amount)
        => $"{amount:N2} THB";

    /// <summary>
    /// Round to 2 decimal places
    /// </summary>
    public static decimal RoundMoney(this decimal amount)
        => Math.Round(amount, 2, MidpointRounding.AwayFromZero);

    /// <summary>
    /// Check if zero
    /// </summary>
    public static bool IsZero(this decimal amount)
        => amount == 0m;

    /// <summary>
    /// Check if positive
    /// </summary>
    public static bool IsPositive(this decimal amount)
        => amount > 0m;
}
```

## Entity Extensions

```csharp
// Extensions/EntityExtensions.cs
public static class EntityExtensions
{
    /// <summary>
    /// Check if entity is new (not yet saved)
    /// </summary>
    public static bool IsNew(this Entity entity)
        => entity.GetId() == 0;

    /// <summary>
    /// Check if entity exists (already saved)
    /// </summary>
    public static bool Exists(this Entity entity)
        => entity.GetId() > 0;
}
```

## Usage Examples

```csharp
// String
var truncated = "Very long text".Truncate(10);  // "Very lo..."
var phone = "0812345678".FormatThaiPhone();     // "081-234-5678"

// Collection
m_rentals.AddOrReplace(rental, r => r.RentalId == rental.RentalId);
m_items.ClearAndAddRange(newItems);

// DateTime
var thaiNow = DateTimeExtensions.ThailandNow();
var displayDate = rental.StartDate.ToThaiDateString();  // "07 Jan 2026"
var days = rental.StartDate.CalculateRentalDays(rental.ExpectedEndDate);

// Decimal
var display = rental.TotalAmount.ToThb();  // "3,500 THB"
```

## File Location

```
MotoRent.Domain/
└── Extensions/
    ├── StringExtensions.cs
    ├── CollectionExtensions.cs
    ├── DateTimeExtensions.cs
    ├── DecimalExtensions.cs
    └── EntityExtensions.cs
```
