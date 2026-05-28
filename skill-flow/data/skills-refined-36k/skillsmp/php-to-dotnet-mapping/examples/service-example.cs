// =============================================================================
// PHP to .NET Service Conversion Example
// =============================================================================

// -----------------------------------------------------------------------------
// BEFORE: PHP Laravel Service (app/Services/ProductService.php)
// -----------------------------------------------------------------------------
/*
<?php

namespace App\Services;

use App\Models\Product;
use App\Repositories\ProductRepository;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

class ProductService
{
    protected $productRepository;

    public function __construct(ProductRepository $productRepository)
    {
        $this->productRepository = $productRepository;
    }

    public function getAllProducts()
    {
        return Cache::remember('products.all', 3600, function () {
            Log::info('Fetching all products from database');
            return $this->productRepository->all();
        });
    }

    public function getProductById($id)
    {
        $cacheKey = "products.{$id}";
        
        return Cache::remember($cacheKey, 3600, function () use ($id) {
            return $this->productRepository->find($id);
        });
    }

    public function createProduct(array $data)
    {
        $product = $this->productRepository->create($data);
        
        Cache::forget('products.all');
        Log::info('Product created', ['id' => $product->id]);
        
        return $product;
    }

    public function updateProduct($id, array $data)
    {
        $product = $this->productRepository->update($id, $data);
        
        Cache::forget('products.all');
        Cache::forget("products.{$id}");
        Log::info('Product updated', ['id' => $id]);
        
        return $product;
    }

    public function deleteProduct($id)
    {
        $this->productRepository->delete($id);
        
        Cache::forget('products.all');
        Cache::forget("products.{$id}");
        Log::info('Product deleted', ['id' => $id]);
    }

    public function searchProducts($query, $filters = [])
    {
        return $this->productRepository
            ->where('name', 'like', "%{$query}%")
            ->when($filters['category'] ?? null, function ($q, $category) {
                return $q->where('category_id', $category);
            })
            ->when($filters['min_price'] ?? null, function ($q, $minPrice) {
                return $q->where('price', '>=', $minPrice);
            })
            ->when($filters['max_price'] ?? null, function ($q, $maxPrice) {
                return $q->where('price', '<=', $maxPrice);
            })
            ->get();
    }
}
*/

// -----------------------------------------------------------------------------
// AFTER: .NET 10 Service Interface (Services/Interfaces/IProductService.cs)
// -----------------------------------------------------------------------------

using ProjectName.Models.DTOs;
using ProjectName.Models.Entities;

namespace ProjectName.Services.Interfaces;

public interface IProductService
{
    Task<IEnumerable<Product>> GetAllProductsAsync();
    Task<Product?> GetProductByIdAsync(int id);
    Task<Product> CreateProductAsync(CreateProductDto dto);
    Task<Product> UpdateProductAsync(int id, UpdateProductDto dto);
    Task DeleteProductAsync(int id);
    Task<IEnumerable<Product>> SearchProductsAsync(string query, ProductSearchFilters? filters = null);
}

// -----------------------------------------------------------------------------
// AFTER: .NET 10 Service Implementation (Services/ProductService.cs)
// -----------------------------------------------------------------------------

using Microsoft.Extensions.Caching.Memory;
using ProjectName.Data;
using ProjectName.Models.DTOs;
using ProjectName.Models.Entities;
using ProjectName.Services.Interfaces;

namespace ProjectName.Services;

public class ProductService : IProductService
{
    private readonly ApplicationDbContext _context;
    private readonly IMemoryCache _cache;
    private readonly ILogger<ProductService> _logger;
    
    private const string AllProductsCacheKey = "products.all";
    private static readonly TimeSpan CacheDuration = TimeSpan.FromHours(1);

    public ProductService(
        ApplicationDbContext context,
        IMemoryCache cache,
        ILogger<ProductService> logger)
    {
        _context = context;
        _cache = cache;
        _logger = logger;
    }

    public async Task<IEnumerable<Product>> GetAllProductsAsync()
    {
        return await _cache.GetOrCreateAsync(AllProductsCacheKey, async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = CacheDuration;
            
            _logger.LogInformation("Fetching all products from database");
            return await _context.Products.ToListAsync();
        }) ?? Enumerable.Empty<Product>();
    }

    public async Task<Product?> GetProductByIdAsync(int id)
    {
        var cacheKey = $"products.{id}";
        
        return await _cache.GetOrCreateAsync(cacheKey, async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = CacheDuration;
            return await _context.Products.FindAsync(id);
        });
    }

    public async Task<Product> CreateProductAsync(CreateProductDto dto)
    {
        var product = new Product
        {
            Name = dto.Name,
            Price = dto.Price,
            Description = dto.Description,
            CreatedAt = DateTime.UtcNow
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();
        
        _cache.Remove(AllProductsCacheKey);
        _logger.LogInformation("Product created: {ProductId}", product.Id);
        
        return product;
    }

    public async Task<Product> UpdateProductAsync(int id, UpdateProductDto dto)
    {
        var product = await _context.Products.FindAsync(id)
            ?? throw new NotFoundException($"Product {id} not found");

        product.Name = dto.Name;
        product.Price = dto.Price;
        product.Description = dto.Description;
        product.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();
        
        _cache.Remove(AllProductsCacheKey);
        _cache.Remove($"products.{id}");
        _logger.LogInformation("Product updated: {ProductId}", id);
        
        return product;
    }

    public async Task DeleteProductAsync(int id)
    {
        var product = await _context.Products.FindAsync(id)
            ?? throw new NotFoundException($"Product {id} not found");

        _context.Products.Remove(product);
        await _context.SaveChangesAsync();
        
        _cache.Remove(AllProductsCacheKey);
        _cache.Remove($"products.{id}");
        _logger.LogInformation("Product deleted: {ProductId}", id);
    }

    public async Task<IEnumerable<Product>> SearchProductsAsync(
        string query, 
        ProductSearchFilters? filters = null)
    {
        var queryable = _context.Products.AsQueryable();

        // Name search (like "%query%")
        queryable = queryable.Where(p => p.Name.Contains(query));

        // Apply filters using LINQ (replaces Laravel's ->when())
        if (filters?.CategoryId.HasValue == true)
        {
            queryable = queryable.Where(p => p.CategoryId == filters.CategoryId);
        }

        if (filters?.MinPrice.HasValue == true)
        {
            queryable = queryable.Where(p => p.Price >= filters.MinPrice);
        }

        if (filters?.MaxPrice.HasValue == true)
        {
            queryable = queryable.Where(p => p.Price <= filters.MaxPrice);
        }

        return await queryable.ToListAsync();
    }
}

// -----------------------------------------------------------------------------
// Search Filters DTO (Models/DTOs/ProductSearchFilters.cs)
// -----------------------------------------------------------------------------

namespace ProjectName.Models.DTOs;

public class ProductSearchFilters
{
    public int? CategoryId { get; set; }
    public decimal? MinPrice { get; set; }
    public decimal? MaxPrice { get; set; }
}

// -----------------------------------------------------------------------------
// Register in DI (Program.cs)
// -----------------------------------------------------------------------------
/*
builder.Services.AddMemoryCache();
builder.Services.AddScoped<IProductService, ProductService>();
*/

// -----------------------------------------------------------------------------
// KEY CONVERSION NOTES:
// -----------------------------------------------------------------------------
// 1. Always create an interface (IProductService) for DI
// 2. Cache::remember() → IMemoryCache.GetOrCreateAsync()
// 3. Log::info() → ILogger.LogInformation() with structured logging
// 4. All methods become async with Task<T>
// 5. Repository pattern can be replaced with direct DbContext access
// 6. ->when() conditional queries → if statements with IQueryable
// 7. Register service in DI container in Program.cs
// 8. Use structured logging with template strings, not string interpolation
// 9. Throw custom exceptions for not found scenarios
// 10. Always use async versions: FindAsync, ToListAsync, SaveChangesAsync
