# Entity Framework Core Patterns

## DbContext Configuration

```csharp
public class AppDbContext : DbContext
{
    public DbSet<User> Users => Set<User>();
    public DbSet<Order> Orders => Set<Order>();

    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }

    // Soft delete filter
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>().HasQueryFilter(u => !u.IsDeleted);
    }
}
```

## Entity Configuration

```csharp
public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("Users");

        builder.HasKey(u => u.Id);

        builder.Property(u => u.Email)
            .IsRequired()
            .HasMaxLength(256);

        builder.HasIndex(u => u.Email)
            .IsUnique();

        // Value object
        builder.OwnsOne(u => u.Address, address =>
        {
            address.Property(a => a.Street).HasColumnName("Street");
            address.Property(a => a.City).HasColumnName("City");
        });

        // Relationships
        builder.HasMany(u => u.Orders)
            .WithOne(o => o.User)
            .HasForeignKey(o => o.UserId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
```

## Query Patterns

### Projection

```csharp
// Avoid: loads entire entity
var users = await _context.Users.ToListAsync();

// Better: project to DTO
var userDtos = await _context.Users
    .Select(u => new UserDto
    {
        Id = u.Id,
        Name = u.Name,
        OrderCount = u.Orders.Count
    })
    .ToListAsync();

// With AutoMapper
var userDtos = await _context.Users
    .ProjectTo<UserDto>(_mapper.ConfigurationProvider)
    .ToListAsync();
```

### Eager Loading

```csharp
// Include related data
var users = await _context.Users
    .Include(u => u.Orders)
        .ThenInclude(o => o.Items)
    .Include(u => u.Profile)
    .ToListAsync();

// Filtered include
var users = await _context.Users
    .Include(u => u.Orders.Where(o => o.Status == OrderStatus.Active))
    .ToListAsync();

// AsSplitQuery for large datasets
var users = await _context.Users
    .Include(u => u.Orders)
    .Include(u => u.Addresses)
    .AsSplitQuery()
    .ToListAsync();
```

### Tracking

```csharp
// Read-only queries - no tracking
var user = await _context.Users
    .AsNoTracking()
    .FirstOrDefaultAsync(u => u.Id == id);

// Default to no tracking for read-heavy apps
services.AddDbContext<AppDbContext>(options =>
    options.UseQueryTrackingBehavior(QueryTrackingBehavior.NoTracking));

// Explicit tracking when needed
var user = await _context.Users
    .AsTracking()
    .FirstOrDefaultAsync(u => u.Id == id);
```

## Write Patterns

### Create

```csharp
public async Task<User> CreateAsync(CreateUserRequest request)
{
    var user = new User(request.Name, request.Email);

    _context.Users.Add(user);
    await _context.SaveChangesAsync();

    return user;
}

// Bulk insert
public async Task CreateManyAsync(IEnumerable<User> users)
{
    _context.Users.AddRange(users);
    await _context.SaveChangesAsync();

    // For large datasets, use EF Core Bulk Extensions
    await _context.BulkInsertAsync(users);
}
```

### Update

```csharp
// Update tracked entity
public async Task UpdateAsync(int id, UpdateUserRequest request)
{
    var user = await _context.Users.FindAsync(id);
    if (user is null) throw new NotFoundException();

    user.UpdateProfile(request.Name, request.Email);
    await _context.SaveChangesAsync();
}

// ExecuteUpdate (EF Core 7+) - no loading
public async Task DeactivateInactiveUsersAsync(DateTime cutoff)
{
    await _context.Users
        .Where(u => u.LastLogin < cutoff)
        .ExecuteUpdateAsync(u => u.SetProperty(x => x.IsActive, false));
}
```

### Delete

```csharp
// Soft delete pattern
public async Task DeleteAsync(int id)
{
    var user = await _context.Users.FindAsync(id);
    if (user is null) return;

    user.IsDeleted = true;
    user.DeletedAt = DateTime.UtcNow;
    await _context.SaveChangesAsync();
}

// ExecuteDelete (EF Core 7+)
public async Task PurgeOldLogsAsync(DateTime cutoff)
{
    await _context.AuditLogs
        .Where(l => l.CreatedAt < cutoff)
        .ExecuteDeleteAsync();
}
```

## Transaction Patterns

```csharp
// Explicit transaction
public async Task TransferAsync(int fromId, int toId, decimal amount)
{
    await using var transaction = await _context.Database.BeginTransactionAsync();

    try
    {
        var from = await _context.Accounts.FindAsync(fromId);
        var to = await _context.Accounts.FindAsync(toId);

        from.Withdraw(amount);
        to.Deposit(amount);

        await _context.SaveChangesAsync();
        await transaction.CommitAsync();
    }
    catch
    {
        await transaction.RollbackAsync();
        throw;
    }
}

// Execution strategy for retries
services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString, sqlOptions =>
        sqlOptions.EnableRetryOnFailure(
            maxRetryCount: 3,
            maxRetryDelay: TimeSpan.FromSeconds(5),
            errorNumbersToAdd: null)));
```

## Performance Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| N+1 queries | Loading related data in loops | Use Include() or projection |
| Select * | Loading unused columns | Use Select() projection |
| Large result sets | Memory pressure | Use pagination, streaming |
| Missing indexes | Slow queries | Add indexes on filter/sort columns |
| Tracking read-only | Unnecessary overhead | Use AsNoTracking() |
| SaveChanges in loops | Multiple round trips | Batch operations |

## Repository Pattern (Optional)

```csharp
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<IReadOnlyList<T>> GetAllAsync();
    Task AddAsync(T entity);
    void Update(T entity);
    void Remove(T entity);
}

public class Repository<T> : IRepository<T> where T : class
{
    protected readonly AppDbContext _context;
    protected readonly DbSet<T> _dbSet;

    public Repository(AppDbContext context)
    {
        _context = context;
        _dbSet = context.Set<T>();
    }

    public virtual async Task<T?> GetByIdAsync(int id)
        => await _dbSet.FindAsync(id);

    public virtual async Task<IReadOnlyList<T>> GetAllAsync()
        => await _dbSet.AsNoTracking().ToListAsync();

    public virtual async Task AddAsync(T entity)
        => await _dbSet.AddAsync(entity);

    public virtual void Update(T entity)
        => _dbSet.Update(entity);

    public virtual void Remove(T entity)
        => _dbSet.Remove(entity);
}

// Unit of Work
public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(CancellationToken ct = default);
}
```

## Migrations

```bash
# Add migration
dotnet ef migrations add InitialCreate

# Update database
dotnet ef database update

# Generate script
dotnet ef migrations script --idempotent -o migration.sql

# Remove last migration (if not applied)
dotnet ef migrations remove
```
