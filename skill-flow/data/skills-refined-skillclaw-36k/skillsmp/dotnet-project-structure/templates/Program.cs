// =============================================================================
// .NET 10 Program.cs Template
// =============================================================================
// This is the entry point for ASP.NET Core applications.
// Replaces Laravel's bootstrap/app.php and config/app.php
// =============================================================================

using Microsoft.EntityFrameworkCore;
using ProjectName.Data;
using ProjectName.Infrastructure.Extensions;

var builder = WebApplication.CreateBuilder(args);

// =============================================================================
// Service Registration (replaces Laravel Service Providers)
// =============================================================================

// Add MVC with Razor Views
builder.Services.AddControllersWithViews();

// OR for API only:
// builder.Services.AddControllers();

// OR for Minimal APIs:
// builder.Services.AddEndpointsApiExplorer();
// builder.Services.AddSwaggerGen();

// Database Context (replaces config/database.php)
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("DefaultConnection")));

// Caching (replaces config/cache.php)
builder.Services.AddMemoryCache();
// OR for distributed cache:
// builder.Services.AddStackExchangeRedisCache(options =>
// {
//     options.Configuration = builder.Configuration.GetConnectionString("Redis");
// });

// Session (if needed - replaces Laravel session)
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

// Authentication (replaces Laravel Auth)
builder.Services.AddAuthentication()
    .AddCookie(options =>
    {
        options.LoginPath = "/login";
        options.LogoutPath = "/logout";
    });

// OR for JWT:
// builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
//     .AddJwtBearer(options => { /* configure */ });

builder.Services.AddAuthorization();

// Application Services (replaces AppServiceProvider)
builder.Services.AddApplicationServices();

// Health Checks
builder.Services.AddHealthChecks()
    .AddDbContextCheck<ApplicationDbContext>();

// =============================================================================
// Build the Application
// =============================================================================

var app = builder.Build();

// =============================================================================
// Middleware Pipeline (replaces Laravel Kernel middleware)
// =============================================================================

// Development-only middleware
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
    // app.UseSwagger();
    // app.UseSwaggerUI();
}
else
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

// HTTPS Redirection
app.UseHttpsRedirection();

// Static Files (serves wwwroot/)
app.UseStaticFiles();

// Routing
app.UseRouting();

// Authentication & Authorization (replaces auth middleware)
app.UseAuthentication();
app.UseAuthorization();

// Session (if using)
app.UseSession();

// =============================================================================
// Route Registration (replaces routes/web.php and routes/api.php)
// =============================================================================

// MVC Routes
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

// API Routes
app.MapControllers();

// Health Check Endpoint
app.MapHealthChecks("/health");

// Minimal API Endpoints (if using)
// app.MapProductEndpoints();
// app.MapUserEndpoints();

// =============================================================================
// Run the Application
// =============================================================================

app.Run();
