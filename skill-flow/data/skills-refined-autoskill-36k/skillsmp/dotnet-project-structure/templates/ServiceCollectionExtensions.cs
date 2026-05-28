// =============================================================================
// .NET 10 Service Collection Extensions Template
// =============================================================================
// Extension methods for registering services in the DI container.
// Replaces Laravel's Service Providers (app/Providers/).
// =============================================================================

using ProjectName.Services;
using ProjectName.Services.Interfaces;

namespace ProjectName.Infrastructure.Extensions;

/// <summary>
/// Extension methods for IServiceCollection to register application services.
/// Replaces Laravel's AppServiceProvider and other service providers.
/// </summary>
public static class ServiceCollectionExtensions
{
    /// <summary>
    /// Registers all application services.
    /// Call this in Program.cs: builder.Services.AddApplicationServices();
    /// </summary>
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {
        // Core Services
        services.AddCoreServices();
        
        // Domain Services
        services.AddDomainServices();
        
        // Infrastructure Services
        services.AddInfrastructureServices();

        return services;
    }

    /// <summary>
    /// Registers core/shared services.
    /// </summary>
    private static IServiceCollection AddCoreServices(this IServiceCollection services)
    {
        // Scoped = One instance per HTTP request (most common for web apps)
        // Replaces Laravel's singleton bindings in AppServiceProvider
        
        // Example: Email service
        // services.AddScoped<IEmailService, EmailService>();
        
        // Example: File storage service
        // services.AddScoped<IStorageService, AzureBlobStorageService>();

        return services;
    }

    /// <summary>
    /// Registers domain/business services.
    /// These are the main application services migrated from PHP.
    /// </summary>
    private static IServiceCollection AddDomainServices(this IServiceCollection services)
    {
        // Register your migrated PHP services here
        // Each PHP service class should have an interface
        
        services.AddScoped<IProductService, ProductService>();
        services.AddScoped<IOrderService, OrderService>();
        services.AddScoped<IUserService, UserService>();
        services.AddScoped<ICategoryService, CategoryService>();
        
        // Add more services as you migrate them...

        return services;
    }

    /// <summary>
    /// Registers infrastructure services.
    /// </summary>
    private static IServiceCollection AddInfrastructureServices(this IServiceCollection services)
    {
        // HTTP Client (replaces Guzzle)
        services.AddHttpClient();
        
        // Named HTTP clients for external APIs
        // services.AddHttpClient("StripeApi", client =>
        // {
        //     client.BaseAddress = new Uri("https://api.stripe.com/");
        // });

        return services;
    }
}

// =============================================================================
// Service Lifetime Reference
// =============================================================================
/*
Laravel vs .NET Service Lifetimes:

| Laravel                          | .NET                    | Description                              |
|----------------------------------|-------------------------|------------------------------------------|
| $app->singleton()                | AddSingleton<T>()       | One instance for the entire app          |
| $app->bind() (default)           | AddScoped<T>()          | One instance per HTTP request            |
| $app->bind() with new each time  | AddTransient<T>()       | New instance every time it's requested   |

Common patterns:
- DbContext: Scoped (one per request)
- HttpClient: Singleton (via AddHttpClient)
- Services with state: Scoped
- Stateless utilities: Singleton or Transient
- Loggers: Singleton (handled by framework)
*/

// =============================================================================
// Configuration Options Extensions
// =============================================================================

/// <summary>
/// Extension methods for registering configuration options.
/// Replaces Laravel's config() helper and config/*.php files.
/// </summary>
public static class ConfigurationExtensions
{
    /// <summary>
    /// Registers strongly-typed configuration options.
    /// Call this in Program.cs: builder.Services.AddAppConfiguration(builder.Configuration);
    /// </summary>
    public static IServiceCollection AddAppConfiguration(
        this IServiceCollection services, 
        IConfiguration configuration)
    {
        // Bind configuration sections to strongly-typed options
        // Replaces: config('app.name'), config('mail.from'), etc.
        
        services.Configure<AppSettings>(configuration.GetSection("App"));
        services.Configure<MailSettings>(configuration.GetSection("Mail"));
        services.Configure<StorageSettings>(configuration.GetSection("Storage"));

        return services;
    }
}

// =============================================================================
// Configuration Classes (replace config/*.php files)
// =============================================================================

/// <summary>
/// Application settings. Replaces config/app.php
/// </summary>
public class AppSettings
{
    public string Name { get; set; } = "My Application";
    public string Environment { get; set; } = "production";
    public string Url { get; set; } = "https://localhost";
    public string Timezone { get; set; } = "UTC";
}

/// <summary>
/// Mail settings. Replaces config/mail.php
/// </summary>
public class MailSettings
{
    public string From { get; set; } = string.Empty;
    public string FromName { get; set; } = string.Empty;
    public string Host { get; set; } = string.Empty;
    public int Port { get; set; } = 587;
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}

/// <summary>
/// Storage settings. Replaces config/filesystems.php
/// </summary>
public class StorageSettings
{
    public string DefaultDisk { get; set; } = "local";
    public string AzureConnectionString { get; set; } = string.Empty;
    public string AzureContainer { get; set; } = string.Empty;
}

// =============================================================================
// Usage in Services (inject IOptions<T>)
// =============================================================================
/*
public class EmailService : IEmailService
{
    private readonly MailSettings _mailSettings;

    public EmailService(IOptions<MailSettings> mailSettings)
    {
        _mailSettings = mailSettings.Value;
    }

    public async Task SendAsync(string to, string subject, string body)
    {
        // Use _mailSettings.Host, _mailSettings.Port, etc.
    }
}
*/
