---
name: performance-profiler
description: Analyze and optimize code performance
trigger: "slow query OR high memory OR performance issue OR optimize"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(dotnet build)
  - Bash(dotnet test)
  - Edit
---

# Performance Profiler

Analyzes code for performance issues and suggests optimizations.

## Analysis Categories

### 1. Database Query Performance

#### N+1 Query Detection

```csharp
// ❌ N+1 Problem
var orders = await _context.Orders.ToListAsync();
foreach (var order in orders)
{
    // Each iteration = 1 query = N additional queries
    var items = order.Items.ToList();  // Lazy loading
}
// Total: 1 + N queries

// ✅ Eager Loading Solution
var orders = await _context.Orders
    .Include(o => o.Items)
    .AsSplitQuery()  // Prevents cartesian explosion
    .ToListAsync();
// Total: 2 queries (split query)
```

**Detection:**
```bash
# Find foreach with navigation property access
grep -rn "foreach.*await" --include="*.cs" -A5 | \
  grep -E "\.(Items|Products|Orders|Reviews)\."

# Find ToListAsync without Include
grep -rn "ToListAsync\(\)" --include="*.cs" -B10 | \
  grep -v "Include\|AsNoTracking\|Select"
```

#### Missing AsNoTracking

```csharp
// ❌ Tracked query (unnecessary overhead for read-only)
var products = await _context.Products.ToListAsync();

// ✅ Untracked query (faster, less memory)
var products = await _context.Products
    .AsNoTracking()
    .ToListAsync();
```

**Detection:**
```bash
# Find query handlers without AsNoTracking
grep -rln "QueryHandler" Merge.Application/ --include="*.cs" | \
  xargs grep -L "AsNoTracking"
```

#### Missing Projections

```csharp
// ❌ Loading entire entity when only need Name
var productNames = await _context.Products
    .ToListAsync()  // Loads ALL columns
    .Select(p => p.Name);

// ✅ Projection - only loads Name column
var productNames = await _context.Products
    .Select(p => p.Name)
    .ToListAsync();

// ✅ With AutoMapper projection
var productDtos = await _context.Products
    .ProjectTo<ProductListDto>(_mapper.ConfigurationProvider)
    .ToListAsync();
```

#### Missing Indexes

```csharp
// Check for queries without index support
// Common candidates:
// - Foreign keys (UserId, CategoryId)
// - Frequently filtered columns (Status, IsActive)
// - Sorted columns (CreatedAt, Name)

// Entity Configuration
entity.HasIndex(e => e.UserId);
entity.HasIndex(e => e.Status);
entity.HasIndex(e => new { e.CategoryId, e.IsActive });  // Composite
```

**Detection:**
```bash
# Find WHERE clauses in raw SQL
grep -rn "Where\|where" --include="*.cs" | \
  grep -E "\.(Status|UserId|CategoryId|IsActive|CreatedAt)"

# Cross-reference with configurations
grep -rn "HasIndex" Merge.Infrastructure/ --include="*.cs"
```

### 2. Memory Performance

#### Large Object Allocations

```csharp
// ❌ Loading entire table into memory
var allProducts = await _context.Products.ToListAsync();  // Could be millions

// ✅ Paginated loading
var products = await _context.Products
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .ToListAsync();

// ✅ Streaming for large datasets
await foreach (var product in _context.Products.AsAsyncEnumerable())
{
    yield return product;
}
```

#### String Concatenation

```csharp
// ❌ String concatenation in loop
string result = "";
foreach (var item in items)
{
    result += item.Name + ", ";  // Creates new string each iteration
}

// ✅ StringBuilder
var sb = new StringBuilder();
foreach (var item in items)
{
    sb.Append(item.Name).Append(", ");
}
var result = sb.ToString();

// ✅ String.Join for simple cases
var result = string.Join(", ", items.Select(i => i.Name));
```

#### LINQ Materialization Issues

```csharp
// ❌ Multiple enumerations
var products = GetProducts();  // IEnumerable
var count = products.Count();  // Enumeration 1
var first = products.First();  // Enumeration 2

// ✅ Materialize once
var products = GetProducts().ToList();  // Single enumeration
var count = products.Count;
var first = products[0];

// ❌ Deferred execution surprise
IEnumerable<Product> GetProducts()
{
    using var context = new DbContext();
    return context.Products;  // Context disposed before enumeration!
}

// ✅ Eager execution
async Task<List<Product>> GetProductsAsync()
{
    await using var context = new DbContext();
    return await context.Products.ToListAsync();
}
```

### 3. Async/Await Performance

#### Unnecessary Async

```csharp
// ❌ Async overhead without benefit
public async Task<int> GetCountAsync()
{
    return await Task.FromResult(42);  // No actual async work
}

// ✅ Synchronous when no I/O
public int GetCount() => 42;

// ❌ Async void (fire and forget, unobserved exceptions)
public async void ProcessAsync() { }

// ✅ Async Task
public async Task ProcessAsync() { }
```

#### Missing ConfigureAwait

```csharp
// In library code (not ASP.NET Core controllers)
// ❌ Captures synchronization context unnecessarily
var result = await GetDataAsync();

// ✅ Better performance in libraries
var result = await GetDataAsync().ConfigureAwait(false);

// Note: In ASP.NET Core, there's no sync context, so this is less critical
```

#### Parallel vs Sequential

```csharp
// ❌ Sequential when parallel possible
var result1 = await GetData1Async();
var result2 = await GetData2Async();
var result3 = await GetData3Async();

// ✅ Parallel when independent
var (result1, result2, result3) = await (
    GetData1Async(),
    GetData2Async(),
    GetData3Async()
);

// Or with Task.WhenAll
var tasks = new[] { GetData1Async(), GetData2Async(), GetData3Async() };
var results = await Task.WhenAll(tasks);
```

### 4. Caching Analysis

#### Missing Cache

```csharp
// ❌ Repeated expensive query
public async Task<ProductDto> GetProductAsync(Guid id)
{
    return await _context.Products
        .Where(p => p.Id == id)
        .ProjectTo<ProductDto>(_mapper)
        .FirstOrDefaultAsync();  // Hits DB every time
}

// ✅ With caching
public async Task<ProductDto?> GetProductAsync(Guid id, CancellationToken ct)
{
    var cacheKey = $"product:{id}";

    return await _cache.GetOrCreateAsync(cacheKey, async entry =>
    {
        entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);

        return await _context.Products
            .AsNoTracking()
            .Where(p => p.Id == id)
            .ProjectTo<ProductDto>(_mapper)
            .FirstOrDefaultAsync(ct);
    });
}
```

#### Cache Stampede Prevention

```csharp
// ❌ Multiple simultaneous cache misses = multiple DB queries
var product = await _cache.GetOrCreateAsync(key, async _ =>
    await _repository.GetAsync(id));

// ✅ With lock/semaphore
private static readonly SemaphoreSlim _semaphore = new(1, 1);

public async Task<ProductDto?> GetProductAsync(Guid id)
{
    var cacheKey = $"product:{id}";
    var cached = await _cache.GetStringAsync(cacheKey);

    if (cached is not null)
        return JsonSerializer.Deserialize<ProductDto>(cached);

    await _semaphore.WaitAsync();
    try
    {
        // Double-check after acquiring lock
        cached = await _cache.GetStringAsync(cacheKey);
        if (cached is not null)
            return JsonSerializer.Deserialize<ProductDto>(cached);

        var product = await _repository.GetAsync(id);
        await _cache.SetStringAsync(cacheKey,
            JsonSerializer.Serialize(product),
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
            });

        return product;
    }
    finally
    {
        _semaphore.Release();
    }
}
```

### 5. API Performance

#### Response Size

```csharp
// ❌ Returning too much data
[HttpGet]
public async Task<ActionResult<List<ProductDetailDto>>> GetAll()
{
    return await _context.Products
        .Include(p => p.Reviews)
        .Include(p => p.Images)
        .ProjectTo<ProductDetailDto>(_mapper)
        .ToListAsync();  // Returns everything, including all reviews
}

// ✅ List endpoint returns minimal data
[HttpGet]
public async Task<ActionResult<PagedResult<ProductListDto>>> GetAll(
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 20)
{
    return await _context.Products
        .AsNoTracking()
        .ProjectTo<ProductListDto>(_mapper)  // Minimal fields
        .ToPagedResultAsync(page, pageSize);
}
```

#### Missing Compression

```csharp
// In Program.cs
builder.Services.AddResponseCompression(options =>
{
    options.EnableForHttps = true;
    options.Providers.Add<BrotliCompressionProvider>();
    options.Providers.Add<GzipCompressionProvider>();
});

app.UseResponseCompression();
```

## Performance Metrics

### Query Performance Targets

| Operation | Target | Warning | Critical |
|-----------|--------|---------|----------|
| Simple GET | < 50ms | > 100ms | > 500ms |
| List GET (paginated) | < 100ms | > 200ms | > 1s |
| Complex query | < 200ms | > 500ms | > 2s |
| Create/Update | < 100ms | > 200ms | > 1s |

### Memory Targets

| Metric | Target | Warning |
|--------|--------|---------|
| Gen 0 GC/min | < 10 | > 50 |
| Gen 2 GC/min | < 1 | > 5 |
| LOH allocations | Minimal | Frequent |

## Detection Commands

```bash
# Find potential performance issues
# Missing AsNoTracking in queries
grep -rln "QueryHandler" --include="*.cs" | xargs grep -L "AsNoTracking"

# ToListAsync without pagination
grep -rn "ToListAsync\(\)" --include="*.cs" | grep -v "Take\|Skip"

# String concatenation in loops
grep -rn "+=" --include="*.cs" | grep "string\|String"

# Multiple awaits that could be parallel
grep -rn "await.*await.*await" --include="*.cs"

# Missing caching in handlers
grep -rln "QueryHandler" --include="*.cs" | xargs grep -L "IDistributedCache\|IMemoryCache"
```

## Output Format

```markdown
# Performance Analysis Report

**Analyzed Files:** 45
**Issues Found:** 12

## Critical Issues

### 1. N+1 Query Detected
- **File:** Merge.Application/Orders/Queries/GetOrdersQueryHandler.cs:34
- **Impact:** 1000 orders = 1001 queries
- **Fix:** Add `.Include(o => o.Items).AsSplitQuery()`

## High Issues

### 2. Missing AsNoTracking
- **File:** Merge.Application/Products/Queries/GetProductQueryHandler.cs:28
- **Impact:** Unnecessary change tracking overhead
- **Fix:** Add `.AsNoTracking()` to query

## Medium Issues

### 3. Large Object Loading
- **File:** Merge.Application/Reports/Queries/GetSalesReportHandler.cs:45
- **Impact:** Loads all orders into memory
- **Fix:** Implement streaming or pagination

## Recommendations

1. Add database indexes for frequently queried columns
2. Implement Redis caching for product catalog
3. Add response compression
4. Consider read replicas for heavy read operations

## Estimated Impact

| Fix | Performance Gain |
|-----|------------------|
| N+1 fix | ~95% faster |
| AsNoTracking | ~20% faster |
| Caching | ~80% faster |
```

## Execution Flow

```
1. Scan Source Files
   ↓
2. Pattern Detection
   - N+1 queries
   - Missing optimizations
   - Memory issues
   ↓
3. Analyze Query Plans (if possible)
   ↓
4. Generate Recommendations
   ↓
5. Prioritize by Impact
   ↓
6. Output Report
```
