---
name: security-and-widget-security
description: Use this skill when implementing security patterns for handling user data and loading third-party widgets in the 3SC application.
---

# Security and Widget Security

## Overview

This skill covers security patterns for protecting user data and safely loading, validating, and running third-party widgets within the 3SC application. It includes credential storage, input validation, secure coding practices, sandboxing, permissions, and trust levels.

## Definition of Done (DoD)

- [ ] Credentials stored securely using DPAPI
- [ ] User input validated before use
- [ ] Sensitive data never logged
- [ ] File paths validated to prevent traversal attacks
- [ ] Widget manifests validated before loading
- [ ] Unsigned widgets require explicit user consent
- [ ] Widget permissions declared and enforced
- [ ] Security-sensitive operations are audited
- [ ] Error messages do not expose internal details
- [ ] Resource limits prevent runaway widgets

## Credential Storage

### Windows Data Protection API (DPAPI)

```csharp
public class SecureStorageService : ISecureStorage
{
    private readonly string _storePath;
    
    public SecureStorageService()
    {
        _storePath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "3SC", "secure");
        Directory.CreateDirectory(_storePath);
    }
    
    public void Store(string key, string value)
    {
        ArgumentException.ThrowIfNullOrEmpty(key);
        
        var plainBytes = Encoding.UTF8.GetBytes(value);
        var protectedBytes = ProtectedData.Protect(
            plainBytes, 
            entropy: null, 
            scope: DataProtectionScope.CurrentUser);
        
        var filePath = GetFilePath(key);
        File.WriteAllBytes(filePath, protectedBytes);
        
        Log.Debug("Credential stored: {Key}", key);
    }
    
    public string? Retrieve(string key)
    {
        var filePath = GetFilePath(key);
        
        if (!File.Exists(filePath))
            return null;
        
        try
        {
            var protectedBytes = File.ReadAllBytes(filePath);
            var plainBytes = ProtectedData.Unprotect(
                protectedBytes,
                entropy: null,
                scope: DataProtectionScope.CurrentUser);
            
            return Encoding.UTF8.GetString(plainBytes);
        }
        catch (CryptographicException ex)
        {
            Log.Warning(ex, "Failed to decrypt credential: {Key}", key);
            return null;
        }
    }
    
    public void Delete(string key)
    {
        var filePath = GetFilePath(key);
        
        if (File.Exists(filePath))
        {
            File.WriteAllBytes(filePath, new byte[64]);
            File.Delete(filePath);
        }
    }
    
    private string GetFilePath(string key)
    {
        var safeKey = Path.GetFileName(key);
        return Path.Combine(_storePath, $"{safeKey}.dat");
    }
}
```

## Input Validation

### Path Validation

```csharp
public static class PathValidator
{
    private static readonly char[] InvalidChars = Path.GetInvalidPathChars()
        .Concat(new[] { '*', '?', '"', '<', '>', '|' })
        .ToArray();
    
    public static string ValidatePath(string basePath, string relativePath)
    {
        ArgumentException.ThrowIfNullOrEmpty(basePath);
        ArgumentException.ThrowIfNullOrEmpty(relativePath);
        
        if (relativePath.IndexOfAny(InvalidChars) >= 0)
        {
            throw new ArgumentException("Path contains invalid characters", nameof(relativePath));
        }
        
        var fullPath = Path.GetFullPath(Path.Combine(basePath, relativePath));
        var normalizedBase = Path.GetFullPath(basePath);
        
        if (!fullPath.StartsWith(normalizedBase, StringComparison.OrdinalIgnoreCase))
        {
            throw new SecurityException($"Path traversal attempt detected: {relativePath}");
        }
        
        return fullPath;
    }
}
```

### Widget Manifest Validation

```csharp
public class ManifestValidator
{
    private static readonly string[] RequiredFields = 
    {
        "packageId", "widgetKey", "displayName", 
        "version", "entry", "minAppVersion"
    };
    
    public ValidationResult Validate(WidgetManifest manifest, string widgetPath)
    {
        var errors = new List<string>();
        
        if (string.IsNullOrEmpty(manifest.PackageId))
            errors.Add("Missing required field: packageId");
        if (string.IsNullOrEmpty(manifest.WidgetKey))
            errors.Add("Missing required field: widgetKey");
        if (string.IsNullOrEmpty(manifest.Entry))
            errors.Add("Missing required field: entry");
        
        if (!InputValidator.IsValidWidgetKey(manifest.WidgetKey))
            errors.Add($"Invalid widget key format: {manifest.WidgetKey}");
        
        if (!SemanticVersion.TryParse(manifest.Version, out _))
            errors.Add($"Invalid version format: {manifest.Version}");
        
        if (!PathValidator.IsValidEntryPoint(widgetPath, manifest.Entry))
            errors.Add($"Invalid or missing entry point: {manifest.Entry}");
        
        return new ValidationResult(errors.Count == 0, errors);
    }
}

public record ValidationResult(bool IsValid, IReadOnlyList<string> Errors);
```

## Security Model for Widgets

```
┌─────────────────────────────────────────────────────────────┐
│                      Trust Levels                           │
├─────────────────────────────────────────────────────────────┤
│  Built-in Widgets     │ Full trust, bundled with app        │
│  Signed Widgets       │ Verified publisher, permission-based│
│  Community Widgets    │ User consent required, sandboxed    │
│  Unknown Widgets      │ Blocked by default                  │
└─────────────────────────────────────────────────────────────┘
```

## Secure Widget Loading

### Widget Load Context

```csharp
public class WidgetLoadContext : AssemblyLoadContext
{
    private readonly AssemblyDependencyResolver _resolver;
    private readonly string _widgetPath;
    
    public WidgetLoadContext(string widgetPath) 
        : base(isCollectible: true)
    {
        _widgetPath = widgetPath;
        _resolver = new AssemblyDependencyResolver(widgetPath);
    }
    
    protected override Assembly? Load(AssemblyName assemblyName)
    {
        var assemblyPath = _resolver.ResolveAssemblyToPath(assemblyName);
        
        if (assemblyPath != null)
        {
            return LoadFromAssemblyPath(assemblyPath);
        }
        
        return null;
    }
}
```

## Permission System

### Permission Enforcement

```csharp
public class PermissionEnforcer
{
    private readonly ConcurrentDictionary<string, WidgetPermissions> _grantedPermissions = new();
    
    public void GrantPermissions(string widgetKey, WidgetPermissions permissions)
    {
        _grantedPermissions[widgetKey] = permissions;
    }
    
    public void EnforcePermission(string widgetKey, string permission)
    {
        if (!HasPermission(widgetKey, permission))
        {
            throw new SecurityException($"Widget '{widgetKey}' does not have '{permission}' permission");
        }
    }
}
```

## Security Best Practices

### Widget Development Guidelines

1. **Declare all required permissions** in manifest.
2. **Handle permission denial gracefully** with fallback behavior.
3. **Never store credentials** - use host's secure storage API.
4. **Validate all external data** before use.
5. **Minimize permission requests** - only ask for what's needed.

## References

- [OWASP Desktop App Security](https://owasp.org/www-project-desktop-app-security-top-10/)
- [Data Protection in .NET](https://docs.microsoft.com/en-us/aspnet/core/security/data-protection/)
- [.NET Assembly Loading](https://docs.microsoft.com/en-us/dotnet/core/dependency-loading/understanding-assemblyloadcontext)
- [Secure Coding Guidelines](https://docs.microsoft.com/en-us/dotnet/standard/security/secure-coding-guidelines)