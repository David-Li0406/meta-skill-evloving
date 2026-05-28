# Implement Repository Pattern

## Goal

Build a data access layer using the Repository pattern to separate database logic from business logic in your application.

> **What you'll learn:**
>
> - How to implement the Repository pattern in ASP.NET Core
> - When to use abstraction for data access
> - Best practices for testable and maintainable code

## Prerequisites

> **Before starting, ensure you have:**
>
> - ✓ Development environment with .NET 8.0 or later
> - ✓ Basic understanding of interfaces and dependency injection
> - ✓ Entity Framework Core installed in your project

## Exercise Steps

### Overview

1. **Create the Repository Interface**
2. **Implement the Repository**
3. **Register with Dependency Injection**
4. **Refactor Controller to Use Repository**
5. **Test Your Implementation**

### **Step 1:** Create the Repository Interface

Define a contract for data access operations to keep your code flexible and testable. This abstraction allows you to change the data access implementation without modifying the code that depends on it, following the Dependency Inversion Principle.

1. **Navigate to** the `Repositories` directory (create it if it doesn't exist)

2. **Create a new file** named `IProductRepository.cs`

3. **Add the following code:**

   > `src/Repositories/IProductRepository.cs`

   ```csharp
   namespace TodoApp.Repositories;

   public interface IProductRepository
   {
       // Retrieves a product by its unique identifier
       Task<Product?> GetByIdAsync(int id);

       // Retrieves all products from the database
       Task<List<Product>> GetAllAsync();

       // Adds a new product to the database
       Task<Product> AddAsync(Product product);

       // Updates an existing product
       Task UpdateAsync(Product product);

       // Removes a product by its identifier
       Task DeleteAsync(int id);
   }
   ```

> ℹ **Concept Deep Dive**
>
> Interfaces define contracts without implementation details. This follows the Dependency Inversion Principle - high-level modules should depend on abstractions, not concrete implementations. In production, this enables unit testing with mock repositories and easy swapping of data stores (SQL Server to MongoDB, for example).
>
> ⚠ **Common Mistakes**
>
> - Forgetting the `async` keyword will cause compilation errors
> - Using `void` instead of `Task` for async methods breaks the async chain
> - Not making the return type nullable (`Product?`) for methods that might return nothing
>
> ✓ **Quick check:** File created at `src/Repositories/IProductRepository.cs` with no compilation errors

### **Step 2:** Implement the Repository

Create the concrete implementation that handles actual database operations using Entity Framework Core. This implementation encapsulates all data access logic, making it reusable and testable.

1. **Create a new file** named `ProductRepository.cs` in the same directory

2. **Add the following implementation:**

   > `src/Repositories/ProductRepository.cs`

   ```csharp
   using Microsoft.EntityFrameworkCore;

   namespace TodoApp.Repositories;

   public class ProductRepository : IProductRepository
   {
       private readonly ApplicationDbContext _context;

       public ProductRepository(ApplicationDbContext context)
       {
           _context = context;
       }

       public async Task<Product?> GetByIdAsync(int id)
       {
           return await _context.Products
               .FirstOrDefaultAsync(p => p.Id == id);
       }

       public async Task<List<Product>> GetAllAsync()
       {
           return await _context.Products
               .OrderBy(p => p.Name)
               .ToListAsync();
       }

       public async Task<Product> AddAsync(Product product)
       {
           _context.Products.Add(product);
           await _context.SaveChangesAsync();
           return product;
       }

       public async Task UpdateAsync(Product product)
       {
           _context.Entry(product).State = EntityState.Modified;
           await _context.SaveChangesAsync();
       }

       public async Task DeleteAsync(int id)
       {
           var product = await _context.Products.FindAsync(id);
           if (product != null)
           {
               _context.Products.Remove(product);
               await _context.SaveChangesAsync();
           }
       }
   }
   ```

> ℹ **Concept Deep Dive**
>
> The repository receives the DbContext through dependency injection, maintaining loose coupling. Each method encapsulates a specific database operation, and `SaveChangesAsync()` ensures changes are persisted. The repository pattern creates a consistent interface for data access across your application.
>
> ⚠ **Common Mistakes**
>
> - Forgetting to call `SaveChangesAsync()` means changes won't persist to the database
> - Not checking for null before deleting can cause NullReferenceException
> - Using `.Result` or `.Wait()` instead of `await` can cause deadlocks
>
> ✓ **Quick check:** Both repository files compile without errors

### **Step 3:** Register with Dependency Injection

Configure the dependency injection container to provide repository instances when needed. This registration tells ASP.NET Core how to create and manage the repository's lifecycle.

1. **Open** `Program.cs` in the project root

2. **Locate** the service registration section (after `builder.Services.AddDbContext`)

3. **Add** the repository registration:

   > `src/Program.cs`

   ```csharp
   // Add this line after your DbContext registration
   builder.Services.AddScoped<IProductRepository, ProductRepository>();

   // Your existing code continues...
   var app = builder.Build();
   ```

> ℹ **Concept Deep Dive**
>
> We use `Scoped` lifetime because the repository depends on DbContext, which is also scoped. This means a new instance is created for each HTTP request but shared within that request. Using `Singleton` would cause errors because DbContext isn't thread-safe. Using `Transient` would create unnecessary instances.
>
> ⚠ **Common Mistakes**
>
> - Using `Singleton` lifetime causes "captive dependency" errors with DbContext
> - Forgetting this registration results in "Unable to resolve service" exceptions
> - Registering after `builder.Build()` means the service won't be available
>
> ✓ **Quick check:** Application starts without dependency injection errors

### **Step 4:** Refactor Controller to Use Repository

Update your controller to use the repository instead of directly accessing the database. This separation of concerns makes your controller thinner and more focused on handling HTTP requests.

1. **Open** the existing `ProductsController.cs` file

2. **Replace** the DbContext dependency with the repository:

   > `src/Controllers/ProductsController.cs`

   ```csharp
   using TodoApp.Repositories;

   namespace TodoApp.Controllers;

   public class ProductsController : Controller
   {
       private readonly IProductRepository _repository;
       private readonly ILogger<ProductsController> _logger;

       public ProductsController(
           IProductRepository repository,
           ILogger<ProductsController> logger)
       {
           _repository = repository;
           _logger = logger;
       }

       public async Task<IActionResult> Index()
       {
           var products = await _repository.GetAllAsync();
           return View(products);
       }

       public async Task<IActionResult> Details(int id)
       {
           var product = await _repository.GetByIdAsync(id);
           if (product == null)
           {
               return NotFound();
           }
           return View(product);
       }

       [HttpPost]
       [ValidateAntiForgeryToken]
       public async Task<IActionResult> Create(Product product)
       {
           if (ModelState.IsValid)
           {
               await _repository.AddAsync(product);
               _logger.LogInformation("Product {Name} created", product.Name);
               return RedirectToAction(nameof(Index));
           }
           return View(product);
       }

       [HttpPost]
       [ValidateAntiForgeryToken]
       public async Task<IActionResult> Delete(int id)
       {
           await _repository.DeleteAsync(id);
           _logger.LogInformation("Product {Id} deleted", id);
           return RedirectToAction(nameof(Index));
       }
   }
   ```

> ℹ **Concept Deep Dive**
>
> The controller now depends on the repository abstraction, not the concrete implementation. This makes the controller easier to test (you can mock the repository) and allows you to change data access strategies without modifying controller code. The controller focuses on HTTP concerns while the repository handles data access.
>
> ⚠ **Common Mistakes**
>
> - Forgetting `[ValidateAntiForgeryToken]` on POST actions creates security vulnerabilities
> - Not checking if the product exists before operations can cause null reference errors
> - Missing `ModelState.IsValid` check allows invalid data to be saved
>
> ✓ **Quick check:** Controller compiles and IntelliSense recognizes all repository methods

### **Step 5:** Test Your Implementation

Verify that the repository pattern is working correctly by testing all CRUD operations through your application's user interface.

1. **Run the application:**

   ```bash
   dotnet run
   ```

2. **Navigate to:** `http://localhost:5000/Products`

3. **Test the Read operations:**
   - Verify the product list displays correctly
   - Click on a product to view details
   - Confirm data is retrieved from the database

4. **Test Create operation:**
   - Click "Create New"
   - Enter product details: "Sample Product", Price: 29.99
   - Submit the form
   - Verify the product appears in the list

5. **Test Update and Delete:**
   - Edit an existing product
   - Change the name or price
   - Save and verify changes persist
   - Delete a product and confirm removal

> ✓ **Success indicators:**
>
> - Product list displays all items from database
> - Creating a product adds it to the list
> - Editing a product updates the database
> - Deleting removes the product permanently
> - No errors in browser console or application logs
>
> ✓ **Final verification checklist:**
>
> - ☐ Repository interface and implementation created
> - ☐ Repository registered in Program.cs
> - ☐ Controller uses repository instead of DbContext
> - ☐ All CRUD operations work through the UI
> - ☐ No direct database access in controller

## Common Issues

> **If you encounter problems:**
>
> **"Unable to resolve service for type IProductRepository":** Check that you registered the repository in Program.cs
>
> **"DbContext has been disposed":** Ensure you're using `Scoped` lifetime for the repository
>
> **Changes not saving:** Verify you're calling `SaveChangesAsync()` in repository methods
>
> **NullReferenceException:** Check that you're handling null returns from `GetByIdAsync`
>
> **Still stuck?** Verify all namespaces match and the repository is in the correct folder

## Summary

You've successfully implemented the Repository pattern which:

- ✓ Separates data access logic from business logic
- ✓ Makes your code more testable through abstraction
- ✓ Enables easy swapping of data access implementations

> **Key takeaway:** The Repository pattern is essential for maintainable applications because it centralizes data access logic and makes your code testable. You'll use this pattern whenever you need to abstract database operations from your business logic.

## Going Deeper (Optional)

> **Want to explore more?**
>
> - Try implementing a generic repository base class for common operations
> - Research the Unit of Work pattern to manage transactions
> - Add caching to your repository methods for performance
> - Implement specification pattern for complex queries

## Done! 🎉

Excellent work! You've learned how to implement the Repository pattern and can now build more maintainable and testable applications. This foundation will help you create clean architecture in your projects.
