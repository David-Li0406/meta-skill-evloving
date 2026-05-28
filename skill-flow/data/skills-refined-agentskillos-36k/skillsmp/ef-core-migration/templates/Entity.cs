// =============================================================================
// EF Core Entity Template
// =============================================================================
// This template shows how to structure an EF Core entity migrated from Eloquent.
// Copy and customize for each entity in your application.
// =============================================================================

using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ProjectName.Models.Entities;

/// <summary>
/// Product entity - migrated from App\Models\Product (Eloquent)
/// </summary>
public class Product : IHasTimestamps, ISoftDelete
{
    // ==========================================================================
    // Primary Key
    // Eloquent: protected $primaryKey = 'id'; (default)
    // ==========================================================================
    
    public int Id { get; set; }

    // ==========================================================================
    // Properties
    // Eloquent: protected $fillable = ['name', 'slug', 'description', ...]
    // ==========================================================================

    [Required]
    [MaxLength(255)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [MaxLength(255)]
    public string Slug { get; set; } = string.Empty;

    [MaxLength(2000)]
    public string? Description { get; set; }

    /// <summary>
    /// Price with 2 decimal places.
    /// Eloquent: 'price' => 'decimal:2'
    /// </summary>
    [Column(TypeName = "decimal(18,2)")]
    public decimal Price { get; set; }

    /// <summary>
    /// Stock quantity.
    /// </summary>
    public int StockQuantity { get; set; }

    /// <summary>
    /// Active status.
    /// Eloquent: 'is_active' => 'boolean'
    /// </summary>
    public bool IsActive { get; set; } = true;

    /// <summary>
    /// JSON metadata stored as string.
    /// Eloquent: 'metadata' => 'array'
    /// Use a value converter for automatic JSON serialization.
    /// </summary>
    public string? MetadataJson { get; set; }

    // ==========================================================================
    // Foreign Keys
    // ==========================================================================

    /// <summary>
    /// Category foreign key.
    /// Eloquent: public function category() { return $this->belongsTo(Category::class); }
    /// </summary>
    public int CategoryId { get; set; }

    /// <summary>
    /// Optional user who created this product.
    /// </summary>
    public int? CreatedByUserId { get; set; }

    // ==========================================================================
    // Timestamps (IHasTimestamps)
    // Eloquent: use Illuminate\Database\Eloquent\Model; (has $timestamps = true by default)
    // ==========================================================================

    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }

    // ==========================================================================
    // Soft Delete (ISoftDelete)
    // Eloquent: use SoftDeletes;
    // ==========================================================================

    public DateTime? DeletedAt { get; set; }

    // ==========================================================================
    // Navigation Properties (Relationships)
    // ==========================================================================

    /// <summary>
    /// Category this product belongs to.
    /// Eloquent: return $this->belongsTo(Category::class);
    /// </summary>
    public Category Category { get; set; } = null!;

    /// <summary>
    /// User who created this product (optional).
    /// Eloquent: return $this->belongsTo(User::class, 'created_by_user_id');
    /// </summary>
    public User? CreatedByUser { get; set; }

    /// <summary>
    /// Reviews for this product.
    /// Eloquent: return $this->hasMany(Review::class);
    /// </summary>
    public ICollection<Review> Reviews { get; set; } = new List<Review>();

    /// <summary>
    /// Order items containing this product.
    /// Eloquent: return $this->hasMany(OrderItem::class);
    /// </summary>
    public ICollection<OrderItem> OrderItems { get; set; } = new List<OrderItem>();

    /// <summary>
    /// Tags for this product (many-to-many via join entity).
    /// Eloquent: return $this->belongsToMany(Tag::class);
    /// </summary>
    public ICollection<ProductTag> ProductTags { get; set; } = new List<ProductTag>();

    /// <summary>
    /// Images for this product (polymorphic).
    /// Eloquent: return $this->morphMany(Image::class, 'imageable');
    /// </summary>
    public ICollection<Image> Images { get; set; } = new List<Image>();

    // ==========================================================================
    // Computed Properties (Accessors)
    // Eloquent: public function getFormattedPriceAttribute()
    // ==========================================================================

    /// <summary>
    /// Formatted price for display.
    /// Eloquent: $product->formatted_price
    /// </summary>
    [NotMapped]
    public string FormattedPrice => $"${Price:N2}";

    /// <summary>
    /// Check if product is in stock.
    /// </summary>
    [NotMapped]
    public bool IsInStock => StockQuantity > 0;

    /// <summary>
    /// Check if product is available for purchase.
    /// Eloquent: public function isAvailable()
    /// </summary>
    [NotMapped]
    public bool IsAvailable => IsActive && IsInStock;

    // ==========================================================================
    // Business Logic Methods
    // Eloquent: public function applyDiscount($percentage)
    // ==========================================================================

    /// <summary>
    /// Calculate price after discount.
    /// </summary>
    public decimal ApplyDiscount(decimal percentage)
    {
        if (percentage < 0 || percentage > 100)
            throw new ArgumentOutOfRangeException(nameof(percentage));
        
        return Price * (1 - percentage / 100);
    }

    /// <summary>
    /// Check if product can fulfill the requested quantity.
    /// </summary>
    public bool CanFulfill(int quantity)
    {
        return IsActive && StockQuantity >= quantity;
    }

    /// <summary>
    /// Reduce stock by quantity.
    /// </summary>
    public void ReduceStock(int quantity)
    {
        if (quantity > StockQuantity)
            throw new InvalidOperationException("Insufficient stock");
        
        StockQuantity -= quantity;
    }
}

// =============================================================================
// Join Entity for Many-to-Many (ProductTag)
// =============================================================================

/// <summary>
/// Join entity for Product-Tag many-to-many relationship.
/// Eloquent: handled automatically by belongsToMany
/// EF Core: requires explicit join entity
/// </summary>
public class ProductTag
{
    public int ProductId { get; set; }
    public Product Product { get; set; } = null!;

    public int TagId { get; set; }
    public Tag Tag { get; set; } = null!;

    /// <summary>
    /// Optional: track when the tag was added.
    /// Eloquent: ->withTimestamps() on the pivot
    /// </summary>
    public DateTime CreatedAt { get; set; }
}

// =============================================================================
// Interfaces for Common Patterns
// =============================================================================

/// <summary>
/// Interface for entities with created/updated timestamps.
/// </summary>
public interface IHasTimestamps
{
    DateTime CreatedAt { get; set; }
    DateTime? UpdatedAt { get; set; }
}

/// <summary>
/// Interface for soft-deletable entities.
/// </summary>
public interface ISoftDelete
{
    DateTime? DeletedAt { get; set; }
}
