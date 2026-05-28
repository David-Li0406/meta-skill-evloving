// =============================================================================
// .NET 10 BaseController Template
// =============================================================================
// Base controller with common functionality for all controllers.
// Replaces Laravel's app/Http/Controllers/Controller.php
// =============================================================================

using Microsoft.AspNetCore.Mvc;

namespace ProjectName.Controllers;

/// <summary>
/// Base controller providing common functionality for all controllers.
/// Inherit from this class instead of Controller directly.
/// </summary>
public abstract class BaseController : Controller
{
    // ==========================================================================
    // Success/Error Messaging (replaces Laravel's with() flash messages)
    // ==========================================================================

    /// <summary>
    /// Sets a success message to be displayed after redirect.
    /// Replaces: return redirect()->with('success', 'Message');
    /// </summary>
    protected void SetSuccessMessage(string message)
    {
        TempData["Success"] = message;
    }

    /// <summary>
    /// Sets an error message to be displayed after redirect.
    /// Replaces: return redirect()->with('error', 'Message');
    /// </summary>
    protected void SetErrorMessage(string message)
    {
        TempData["Error"] = message;
    }

    /// <summary>
    /// Sets a warning message to be displayed after redirect.
    /// </summary>
    protected void SetWarningMessage(string message)
    {
        TempData["Warning"] = message;
    }

    /// <summary>
    /// Sets an info message to be displayed after redirect.
    /// </summary>
    protected void SetInfoMessage(string message)
    {
        TempData["Info"] = message;
    }

    // ==========================================================================
    // JSON Responses (replaces Laravel's response()->json())
    // ==========================================================================

    /// <summary>
    /// Returns a JSON success response.
    /// Replaces: return response()->json(['success' => true, 'data' => $data]);
    /// </summary>
    protected IActionResult JsonSuccess<T>(T data, string? message = null)
    {
        return Ok(new
        {
            success = true,
            message,
            data
        });
    }

    /// <summary>
    /// Returns a JSON error response.
    /// Replaces: return response()->json(['success' => false, 'message' => $msg], 400);
    /// </summary>
    protected IActionResult JsonError(string message, int statusCode = 400)
    {
        return StatusCode(statusCode, new
        {
            success = false,
            message
        });
    }

    // ==========================================================================
    // Current User Helpers (replaces Laravel's Auth facade)
    // ==========================================================================

    /// <summary>
    /// Gets the current authenticated user's ID.
    /// Replaces: Auth::id() or auth()->id()
    /// </summary>
    protected int? CurrentUserId
    {
        get
        {
            var claim = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier);
            return claim != null ? int.Parse(claim.Value) : null;
        }
    }

    /// <summary>
    /// Checks if a user is authenticated.
    /// Replaces: Auth::check() or auth()->check()
    /// </summary>
    protected bool IsAuthenticated => User.Identity?.IsAuthenticated ?? false;

    /// <summary>
    /// Gets the current user's email.
    /// Replaces: Auth::user()->email
    /// </summary>
    protected string? CurrentUserEmail => User.FindFirst(System.Security.Claims.ClaimTypes.Email)?.Value;

    // ==========================================================================
    // Redirect Helpers
    // ==========================================================================

    /// <summary>
    /// Redirects back to the previous page.
    /// Replaces: return back();
    /// </summary>
    protected IActionResult RedirectBack()
    {
        var referer = Request.Headers.Referer.ToString();
        if (!string.IsNullOrEmpty(referer))
        {
            return Redirect(referer);
        }
        return RedirectToAction("Index", "Home");
    }

    /// <summary>
    /// Redirects back with an error message.
    /// Replaces: return back()->withErrors(['message']);
    /// </summary>
    protected IActionResult RedirectBackWithError(string error)
    {
        SetErrorMessage(error);
        return RedirectBack();
    }
}

// =============================================================================
// API Base Controller (for API-only controllers)
// =============================================================================

/// <summary>
/// Base controller for API endpoints.
/// Replaces Laravel API controller conventions.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public abstract class ApiBaseController : ControllerBase
{
    /// <summary>
    /// Returns a standardized success response.
    /// </summary>
    protected IActionResult ApiSuccess<T>(T data, string? message = null)
    {
        return Ok(new ApiResponse<T>
        {
            Success = true,
            Message = message,
            Data = data
        });
    }

    /// <summary>
    /// Returns a standardized error response.
    /// </summary>
    protected IActionResult ApiError(string message, int statusCode = 400)
    {
        return StatusCode(statusCode, new ApiResponse<object>
        {
            Success = false,
            Message = message,
            Data = null
        });
    }

    /// <summary>
    /// Returns a standardized not found response.
    /// Replaces: abort(404);
    /// </summary>
    protected IActionResult ApiNotFound(string message = "Resource not found")
    {
        return NotFound(new ApiResponse<object>
        {
            Success = false,
            Message = message,
            Data = null
        });
    }
}

/// <summary>
/// Standardized API response wrapper.
/// </summary>
public class ApiResponse<T>
{
    public bool Success { get; set; }
    public string? Message { get; set; }
    public T? Data { get; set; }
}
