---
name: generic-extension-methods
description: Use this skill when you need to implement common extension methods for strings, collections, and other types in C#.
---

# Skill body

## Extension Methods

Generic extension methods for common operations.

### String Extensions

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

### Collection Extensions

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
}
```