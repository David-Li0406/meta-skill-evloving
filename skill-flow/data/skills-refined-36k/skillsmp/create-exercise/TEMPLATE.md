# [Exercise Title]

## Goal

Build [specific feature] to enable [business capability] in your application.

> **What you'll learn:**
>
> - How to implement [concept/pattern]
> - When to use [technique] in real applications
> - Best practices for [specific area]

## Prerequisites

> **Before starting, ensure you have:**
>
> - ✓ Development environment with [tools/frameworks]
> - ✓ Basic understanding of [concept]
> - ✓ [Any specific setup requirement]

## Exercise Steps

### Overview

1. **[Action Title for Step 1]**
2. **[Action Title for Step 2]**
3. **[Action Title for Step 3]**
4. **[Action Title for Step 4]**
5. **Test Your Implementation**

### **Step 1:** [Clear Action Title]

[Explain what this step accomplishes and why it's important. This paragraph provides context about what you're about to build, how it fits into the larger picture, and what problem it solves. Be explanatory here - this helps students understand not just what to do, but why they're doing it.]

1. **Navigate to** the `[folder]` directory

2. **Create a new file** named `[filename.ext]`

3. **Add the following code:**

   > `src/Models/ExampleClass.cs`

   ```csharp
   namespace YourApp.Models;

   public class ExampleClass
   {
       // This property stores [purpose]
       public string Name { get; set; }

       // This method handles [responsibility]
       public void Process()
       {
           // Implementation here
       }
   }
   ```

> ℹ **Concept Deep Dive**
>
> This class serves as [explanation of purpose and design decision]. We use [pattern] here because [benefit]. In production applications, this pattern is commonly used for [real-world scenario].
>
> ⚠ **Common Mistakes**
>
> - Forgetting to [important step] will result in `[specific error message]`
> - Make sure the namespace matches your project structure
> - Don't confuse [concept A] with [concept B]
>
> ✓ **Quick check:** File created at the correct location with proper namespace

### **Step 2:** [Clear Action Title]

[This step connects the component you just created to the rest of your application. Explain how this integration works, what dependencies are involved, and why this connection pattern is important for maintainable code.]

1. **Open** the existing file at `[path/to/file.cs]`

2. **Locate** the [specific section/method] (usually around line [X])

3. **Replace/Add** the following code:

   > `src/Controllers/ExampleController.cs`

   ```csharp
   using YourApp.Models;
   using YourApp.Services;

   namespace YourApp.Controllers;

   public class ExampleController : Controller
   {
       private readonly IService _service;

       public ExampleController(IService service)
       {
           _service = service;  // Dependency injection
       }

       public async Task<IActionResult> Index()
       {
           // Key: This calls our new service
           var result = await _service.ProcessAsync();
           return View(result);
       }
   }
   ```

> ℹ **Concept Deep Dive**
>
> This demonstrates dependency injection - instead of creating objects directly, we receive them through the constructor. This makes our code more testable and follows the Dependency Inversion Principle. The service is injected by the DI container at runtime.
>
> ✓ **Quick check:** No compilation errors, IntelliSense recognizes the new service

### **Step 3:** [Clear Action Title]

[Now we need to register our service with the application's dependency injection container. This step is crucial for making your service available throughout the application. We'll also configure any necessary middleware or options.]

1. **Open** `Program.cs` in the project root

2. **Add** the service registration after the existing service registrations:

   > `src/Program.cs`

   ```csharp
   // Add this with other service registrations
   builder.Services.AddScoped<IExampleService, ExampleService>();

   // If you need configuration
   builder.Services.Configure<ExampleOptions>(
       builder.Configuration.GetSection("ExampleSettings"));

   var app = builder.Build();
   ```

3. **Configure** the middleware pipeline (if needed):

   > `src/Program.cs`

   ```csharp
   // Add after app.UseAuthentication() if present
   app.UseMiddleware<ExampleMiddleware>();
   ```

> ℹ **Concept Deep Dive**
>
> We use `Scoped` lifetime because this service uses DbContext (also scoped). Using Singleton would cause a captive dependency error. Transient would work but creates unnecessary overhead since we don't need a new instance for every injection.
>
> ⚠ **Common Mistakes**
>
> - Wrong service lifetime can cause runtime errors
> - Middleware order matters - authentication should come before authorization
> - Forgetting to add configuration section in appsettings.json
>
> ✓ **Quick check:** Application starts without dependency injection errors

### **Step 4:** [Clear Action Title]

[Create the user interface to interact with your new feature. This step brings together the backend logic with a frontend that users can interact with. We'll create a view that properly binds to our model and handles user input.]

1. **Create** a new folder `Views/[ControllerName]` if it doesn't exist

2. **Add** a new view file:

   > `src/Views/Example/Index.cshtml`

   ```html
   @model YourApp.ViewModels.ExampleViewModel

   <div class="container">
       <h2>@ViewData["Title"]</h2>

       <form asp-action="Create" method="post">
           <div asp-validation-summary="ModelOnly" class="text-danger"></div>

           <div class="form-group">
               <label asp-for="Name"></label>
               <input asp-for="Name" class="form-control" />
               <span asp-validation-for="Name" class="text-danger"></span>
           </div>

           <button type="submit" class="btn btn-primary">Submit</button>
       </form>
   </div>

   @section Scripts {
       @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}
   }
   ```

> ℹ **Concept Deep Dive**
>
> Tag Helpers (asp-for, asp-action) provide IntelliSense support and compile-time checking. They generate proper HTML with correct names and ids for model binding. The validation summary and field validation work together to provide client and server-side validation.
>
> ✓ **Quick check:** View renders without errors when navigating to the route

### **Step 5:** Test Your Implementation

[Time to verify that everything works correctly. We'll test the happy path, edge cases, and ensure proper error handling. This systematic testing approach helps catch issues before they reach production.]

1. **Run the application:**

   ```bash
   dotnet run
   ```

2. **Navigate to:** `http://localhost:5000/[controller]`

3. **Test the happy path:**
   - Enter valid data: [example data]
   - Submit the form
   - Verify the data is processed correctly
   - Check the database/storage to confirm persistence

4. **Test validation:**
   - Submit with empty required fields
   - Enter invalid data formats
   - Verify validation messages appear

5. **Test edge cases:**
   - Try [specific edge case]
   - Test with [boundary values]
   - Verify proper error handling

> ✓ **Success indicators:**
>
> - Page loads without errors
> - Form submission works with valid data
> - Validation prevents invalid submissions
> - Data persists correctly
> - No errors in browser console or application logs
>
> ✓ **Final verification checklist:**
>
> - ☐ All files created in correct locations
> - ☐ Application compiles without errors
> - ☐ Feature works with test data
> - ☐ Validation works properly
> - ☐ [Specific verification for this exercise]

## Common Issues

> **If you encounter problems:**
>
> **Build errors:** Ensure all namespaces match your project structure
>
> **Service not found error:** Check service registration in Program.cs
>
> **404 Not Found:** Verify controller name matches route and view folder
>
> **Validation not working:** Ensure validation scripts are included
>
> **Still stuck?** Review the file paths and ensure exact naming

## Summary

You've successfully implemented [feature/pattern] which:

- ✓ Enables [business capability]
- ✓ Follows [design pattern] for better [quality attribute]
- ✓ Prepares your app for [future enhancement]

> **Key takeaway:** [Most important concept] is essential because [real-world application]. You'll use this pattern whenever [common scenario].

## Going Deeper (Optional)

> **Want to explore more?**
>
> - Try adding [enhancement A] to handle [edge case]
> - Research how [concept] works under the hood
> - Implement [related pattern] for comparison
> - Add unit tests for your new components

## Done! 🎉

Great job! You've learned how to [core skill] and can now [capability gained]. This foundation will help you build more [quality attribute] applications.
