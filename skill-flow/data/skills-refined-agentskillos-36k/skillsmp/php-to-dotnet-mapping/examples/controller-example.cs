// =============================================================================
// PHP to .NET Controller Conversion Example
// =============================================================================

// -----------------------------------------------------------------------------
// BEFORE: PHP Laravel Controller (app/Http/Controllers/ProductController.php)
// -----------------------------------------------------------------------------
/*
<?php

namespace App\Http\Controllers;

use App\Models\Product;
use App\Services\ProductService;
use Illuminate\Http\Request;

class ProductController extends Controller
{
    protected $productService;

    public function __construct(ProductService $productService)
    {
        $this->productService = $productService;
    }

    public function index()
    {
        $products = $this->productService->getAllProducts();
        return view('products.index', compact('products'));
    }

    public function show($id)
    {
        $product = $this->productService->getProductById($id);
        
        if (!$product) {
            abort(404);
        }
        
        return view('products.show', compact('product'));
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|max:255',
            'price' => 'required|numeric|min:0',
            'description' => 'nullable|string',
        ]);

        $product = $this->productService->createProduct($validated);
        
        return redirect()->route('products.show', $product->id)
            ->with('success', 'Product created successfully.');
    }

    public function update(Request $request, $id)
    {
        $validated = $request->validate([
            'name' => 'required|max:255',
            'price' => 'required|numeric|min:0',
            'description' => 'nullable|string',
        ]);

        $product = $this->productService->updateProduct($id, $validated);
        
        return redirect()->route('products.show', $id)
            ->with('success', 'Product updated successfully.');
    }

    public function destroy($id)
    {
        $this->productService->deleteProduct($id);
        
        return redirect()->route('products.index')
            ->with('success', 'Product deleted successfully.');
    }
}
*/

// -----------------------------------------------------------------------------
// AFTER: .NET 10 Controller (Controllers/ProductController.cs)
// -----------------------------------------------------------------------------

using Microsoft.AspNetCore.Mvc;
using ProjectName.Models.DTOs;
using ProjectName.Models.ViewModels;
using ProjectName.Services.Interfaces;

namespace ProjectName.Controllers;

public class ProductController : Controller
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductController> _logger;

    public ProductController(
        IProductService productService,
        ILogger<ProductController> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    // GET: /products
    public async Task<IActionResult> Index()
    {
        var products = await _productService.GetAllProductsAsync();
        return View(products);
    }

    // GET: /products/{id}
    public async Task<IActionResult> Show(int id)
    {
        var product = await _productService.GetProductByIdAsync(id);
        
        if (product is null)
        {
            return NotFound();
        }
        
        return View(product);
    }

    // POST: /products
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Store([FromForm] CreateProductDto dto)
    {
        if (!ModelState.IsValid)
        {
            return View("Create", dto);
        }

        var product = await _productService.CreateProductAsync(dto);
        
        TempData["Success"] = "Product created successfully.";
        return RedirectToAction(nameof(Show), new { id = product.Id });
    }

    // PUT: /products/{id}
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Update(int id, [FromForm] UpdateProductDto dto)
    {
        if (!ModelState.IsValid)
        {
            return View("Edit", dto);
        }

        await _productService.UpdateProductAsync(id, dto);
        
        TempData["Success"] = "Product updated successfully.";
        return RedirectToAction(nameof(Show), new { id });
    }

    // DELETE: /products/{id}
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Destroy(int id)
    {
        await _productService.DeleteProductAsync(id);
        
        TempData["Success"] = "Product deleted successfully.";
        return RedirectToAction(nameof(Index));
    }
}

// -----------------------------------------------------------------------------
// DTO for Create (Models/DTOs/CreateProductDto.cs)
// -----------------------------------------------------------------------------

namespace ProjectName.Models.DTOs;

public class CreateProductDto
{
    [Required]
    [MaxLength(255)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [Range(0, double.MaxValue)]
    public decimal Price { get; set; }

    public string? Description { get; set; }
}

// -----------------------------------------------------------------------------
// KEY CONVERSION NOTES:
// -----------------------------------------------------------------------------
// 1. Constructor injection pattern is the same
// 2. Add ILogger for logging (replaces Log facade)
// 3. All methods become async with Task<IActionResult>
// 4. $request->validate() → Data annotations on DTO + ModelState.IsValid
// 5. abort(404) → return NotFound()
// 6. view('name', compact('var')) → View(model)
// 7. redirect()->route('name') → RedirectToAction(nameof(Action))
// 8. ->with('key', 'value') → TempData["Key"] = "value"
// 9. Add [ValidateAntiForgeryToken] for POST/PUT/DELETE
// 10. Use [FromForm] for form data binding
