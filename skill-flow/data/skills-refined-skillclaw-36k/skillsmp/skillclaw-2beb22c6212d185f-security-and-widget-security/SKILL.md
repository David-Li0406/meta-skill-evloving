---
name: security-and-widget-security
description: Use this skill when implementing security measures for applications that handle user data and load third-party widgets, ensuring safe coding practices and proper validation.
---

# Security and Widget Security

## Overview

This skill encompasses security patterns for both protecting user data in applications and safely loading third-party widgets. It covers credential storage, input validation, secure coding practices, sandboxing, permissions, and trust levels.

## Definition of Done (DoD)

- [ ] Credentials stored using DPAPI (Windows Data Protection)
- [ ] User input validated before use
- [ ] Sensitive data never logged
- [ ] File paths validated to prevent traversal attacks
- [ ] Error messages don't expose internal details
- [ ] Security-sensitive operations are audited
- [ ] Widget manifests validated before loading
- [ ] Unsigned widgets require explicit user consent
- [ ] Widget permissions declared and enforced
- [ ] Widget loading failures logged with context
- [ ] Widgets isolated via AssemblyLoadContext
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
            entropy: null,  // Add entropy for additional security
            scope: DataProtectionScope.CurrentUser);
        
        var filePath = GetFilePath(key);
        File.WriteAllBytes(filePath, protectedBytes);
        
        Log.Debug("Credential stored: {Key}", key);  // Never log the value!
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
            File.Delete(filePath);
            Log.Debug("Credential deleted: {Key}", key);
        }
    }
}
```

## Widget Security

### Security Model

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

### Manifest Validation

```csharp
public class ManifestValidator
{
    private static readonly string[] RequiredFields = 
    {
        "packageId", "widgetKey", "displayName", 
        "version", "entry", "minAppVersion"
    };
    
    private static readonly string[] AllowedPermissions =
    {
        "network", "filesystem", "clipboard", 
        "notifications", "process"
    };
    
    public ValidationResult Validate(WidgetManifest manifest, string widgetPath)
    {
        var errors = new List<string>();
        
        // Required fields
        if (string.IsNullOrEmpty(manifest.PackageId))
            errors.Add("Missing required field: packageId");
        if (string.IsNullOrEmpty(manifest.WidgetKey))
            errors.Add("Missing required field: widgetKey");
        if (string.IsNullOrEmpty(manifest.Entry))
            errors.Add("Missing required field: entry");
        
        // Widget key format
        if (!InputValidator.IsValidWidgetKey(manifest.WidgetKey))
            errors.Add($"Invalid widget key format: {manifest.WidgetKey}");
        
        // Version format
        if (!SemanticVersion.TryParse(manifest.Version, out _))
            errors.Add($"Invalid version format: {manifest.Version}");
        
        // Check permissions
        foreach (var permission in manifest.Permissions)
        {
            if (!AllowedPermissions.Contains(permission))
                errors.Add($"Disallowed permission: {permission}");
        }
        
        return errors.Count > 0 ? ValidationResult.Invalid(errors) : ValidationResult.Valid();
    }
}
```