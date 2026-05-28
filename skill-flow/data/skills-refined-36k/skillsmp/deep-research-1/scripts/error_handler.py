#!/usr/bin/env python3
"""
Error Handler - User-friendly error processing and guidance

This module provides comprehensive error handling with user-friendly messages,
resolution guides, and automatic fallback capabilities.
"""

import logging
import traceback
from typing import Dict, List, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Categories of errors for targeted handling."""
    API_KEY_MISSING = "api_key_missing"
    API_KEY_INVALID = "api_key_invalid"
    DEPENDENCY_MISSING = "dependency_missing"
    NETWORK_ERROR = "network_error"
    API_QUOTA_EXCEEDED = "api_quota_exceeded"
    API_RATE_LIMIT = "api_rate_limit"
    PERMISSION_ERROR = "permission_error"
    VALIDATION_ERROR = "validation_error"
    UNKNOWN_ERROR = "unknown_error"


class ErrorHandler:
    """Handles errors with user-friendly messages and resolution guides."""
    
    def __init__(self):
        """Initialize the error handler."""
        self.error_templates = self._load_error_templates()
        self.resolution_guides = self._load_resolution_guides()
        
    def _load_error_templates(self) -> Dict[ErrorType, str]:
        """Load user-friendly error message templates."""
        return {
            ErrorType.API_KEY_MISSING: """
🔑 API Key Missing

No API keys were found for any LLM provider. The skill will run in mock mode.

{resolution_guide}
            """.strip(),
            
            ErrorType.API_KEY_INVALID: """
🚫 Invalid API Key

The API key for {provider} appears to be invalid or malformed.

Key preview: {key_preview}
{resolution_guide}
            """.strip(),
            
            ErrorType.DEPENDENCY_MISSING: """
📦 Missing Dependencies

Required Python packages are missing: {missing_packages}

{resolution_guide}
            """.strip(),
            
            ErrorType.NETWORK_ERROR: """
🌐 Network Connection Failed

Unable to connect to required services. Please check your internet connection.

{resolution_guide}
            """.strip(),
            
            ErrorType.API_QUOTA_EXCEEDED: """
💳 API Quota Exceeded

The API quota for {provider} has been exceeded. Please check your billing status.

{resolution_guide}
            """.strip(),
            
            ErrorType.API_RATE_LIMIT: """
⏱️ API Rate Limit Exceeded

Too many requests to {provider}. Please wait a moment before trying again.

{resolution_guide}
            """.strip(),
            
            ErrorType.PERMISSION_ERROR: """
🔒 Permission Denied

Unable to access required files or directories.

{resolution_guide}
            """.strip(),
            
            ErrorType.VALIDATION_ERROR: """
⚠️ Input Validation Error

The provided input is invalid: {validation_details}

{resolution_guide}
            """.strip(),
            
            ErrorType.UNKNOWN_ERROR: """
❓ Unexpected Error

An unexpected error occurred: {error_message}

{resolution_guide}
            """.strip(),
        }
    
    def _load_resolution_guides(self) -> Dict[ErrorType, str]:
        """Load resolution guides for each error type."""
        return {
            ErrorType.API_KEY_MISSING: """
## Resolution Steps:

1. **Set up Gemini API (Recommended):**
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```

2. **Or set up OpenAI API:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

3. **Get API keys:**
   - Gemini: https://makersuite.google.com/app/apikey
   - OpenAI: https://platform.openai.com/api-keys

4. **For persistent setup:**
   Add the export command to ~/.bashrc or ~/.config/opencode/.env
            """.strip(),
            
            ErrorType.API_KEY_INVALID: """
## Resolution Steps:

1. **Verify the API key:**
   - Check for typos or extra characters
   - Ensure the key is complete (not truncated)

2. **Regenerate the key:**
   - Visit the provider's dashboard
   - Create a new API key
   - Update your environment variable

3. **Common format issues:**
   - Gemini keys should start with "AIza" or "GOYA"
   - OpenAI keys should start with "sk-"
            """.strip(),
            
            ErrorType.DEPENDENCY_MISSING: """
## Resolution Steps:

1. **Install missing packages:**
   ```bash
   pip install {install_command}
   ```

2. **Install all dependencies at once:**
   ```bash
   pip install duckduckgo-search beautifulsoup4 requests google-generativeai openai
   ```

3. **If you use conda:**
   ```bash
   conda install -c conda-forge beautifulsoup4 requests
   pip install duckduckgo-search google-generativeai openai
   ```
            """.strip(),
            
            ErrorType.NETWORK_ERROR: """
## Resolution Steps:

1. **Check internet connection:**
   ```bash
   ping google.com
   ```

2. **Check firewall/proxy settings:**
   - Ensure Python can access external sites
   - Configure proxy if needed

3. **Try alternative DNS:**
   ```bash
   # Temporarily use Google DNS
   echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
   ```
            """.strip(),
            
            ErrorType.API_QUOTA_EXCEEDED: """
## Resolution Steps:

1. **Check billing status:**
   - Visit the provider's dashboard
   - Verify payment method is valid

2. **Monitor usage:**
   - Check API usage statistics
   - Set up usage alerts

3. **Upgrade plan if needed:**
   - Consider higher tier plans
   - Set usage limits to avoid overages
            """.strip(),
            
            ErrorType.API_RATE_LIMIT: """
## Resolution Steps:

1. **Wait and retry:**
   - Most rate limits reset within 1-60 seconds
   - Try again after a short delay

2. **Reduce request frequency:**
   - Add delays between API calls
   - Batch requests when possible

3. **Upgrade if needed:**
   - Higher tier plans often have better rate limits
            """.strip(),
            
            ErrorType.PERMISSION_ERROR: """
## Resolution Steps:

1. **Check directory permissions:**
   ```bash
   ls -la ~/.cache/opencode/
   ```

2. **Fix permissions if needed:**
   ```bash
   mkdir -p ~/.cache/opencode/research
   chmod 755 ~/.cache/opencode/research
   ```

3. **Run with appropriate user:**
   - Avoid running as root when possible
   - Ensure user has write permissions
            """.strip(),
            
            ErrorType.VALIDATION_ERROR: """
## Resolution Steps:

1. **Check input format:**
   - Ensure all required fields are provided
   - Verify input meets expected format

2. **Review examples:**
   - Check documentation for correct usage
   - Try with sample inputs first

3. **Common issues:**
   - Empty research topics
   - Invalid characters in filenames
   - Malformed JSON responses
            """.strip(),
            
            ErrorType.UNKNOWN_ERROR: """
## Resolution Steps:

1. **Check the logs:**
   - Review the full error traceback
   - Look for specific error messages

2. **Try these common fixes:**
   - Restart the script
   - Update dependencies: pip install --upgrade
   - Check for conflicting packages

3. **Report the issue:**
   - Include the full error message
   - Describe what you were trying to do
   - Mention your OS and Python version
            """.strip(),
        }
    
    def classify_error(self, error: Exception) -> ErrorType:
        """
        Classify an error into a specific category.
        
        Args:
            error: The exception to classify
            
        Returns:
            ErrorType category
        """
        error_message = str(error).lower()
        error_type = type(error).__name__.lower()
        
        # API Key errors
        if any(keyword in error_message for keyword in ["api key", "unauthorized", "authentication", "401"]):
            if "not found" in error_message or "missing" in error_message:
                return ErrorType.API_KEY_MISSING
            return ErrorType.API_KEY_INVALID
            
        # Dependency errors
        if any(keyword in error_message for keyword in ["module not found", "no module named", "import error"]):
            return ErrorType.DEPENDENCY_MISSING
            
        # Network errors
        if any(keyword in error_message for keyword in ["connection", "network", "timeout", "dns", "unreachable"]):
            return ErrorType.NETWORK_ERROR
            
        # Quota errors
        if any(keyword in error_message for keyword in ["quota", "billing", "payment", "credit"]):
            return ErrorType.API_QUOTA_EXCEEDED
            
        # Rate limit errors
        if any(keyword in error_message for keyword in ["rate limit", "too many requests", "429"]):
            return ErrorType.API_RATE_LIMIT
            
        # Permission errors
        if any(keyword in error_message for keyword in ["permission", "access denied", "forbidden", "403"]):
            return ErrorType.PERMISSION_ERROR
            
        # Validation errors
        if any(keyword in error_type for keyword in ["valueerror", "validation", "invalid"]):
            return ErrorType.VALIDATION_ERROR
            
        return ErrorType.UNKNOWN_ERROR
    
    def format_user_message(
        self, 
        error: Exception, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Format a user-friendly error message.
        
        Args:
            error: The exception that occurred
            context: Additional context information
            
        Returns:
            Formatted user-friendly error message
        """
        error_type = self.classify_error(error)
        template = self.error_templates[error_type]
        resolution_guide = self.resolution_guides[error_type]
        
        # Prepare context variables
        context_vars = {
            "error_message": str(error),
            "error_type": error_type.value,
            "resolution_guide": resolution_guide,
        }
        
        # Add error-specific context
        if context:
            context_vars.update(context)
            
        # Format the message
        try:
            message = template.format(**context_vars)
        except KeyError as e:
            # Fallback if template variable is missing
            logger.warning(f"Missing template variable: {e}")
            message = template.format(
                error_message=str(error),
                resolution_guide=resolution_guide,
                **{k: "N/A" for k in context_vars if k not in ["error_message", "resolution_guide"]}
            )
            
        return message
    
    def provide_resolution_guide(self, error_type: ErrorType) -> str:
        """
        Get the resolution guide for a specific error type.
        
        Args:
            error_type: The type of error
            
        Returns:
            Resolution guide text
        """
        return self.resolution_guides.get(error_type, "No specific resolution guide available.")
    
    def should_fallback(self, error: Exception) -> bool:
        """
        Determine if the system should fall back to mock mode.
        
        Args:
            error: The exception that occurred
            
        Returns:
            True if fallback is appropriate
        """
        error_type = self.classify_error(error)
        
        # Always fallback for these errors
        fallback_errors = {
            ErrorType.API_KEY_MISSING,
            ErrorType.API_KEY_INVALID,
            ErrorType.DEPENDENCY_MISSING,
            ErrorType.NETWORK_ERROR,
            ErrorType.API_QUOTA_EXCEEDED,
        }
        
        return error_type in fallback_errors
    
    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """
        Log the error with full technical details.
        
        Args:
            error: The exception to log
            context: Additional context information
        """
        error_type = self.classify_error(error)
        
        logger.error(f"Error Type: {error_type.value}")
        logger.error(f"Error: {error}")
        
        if context:
            logger.error(f"Context: {context}")
            
        logger.debug(f"Full traceback:\n{traceback.format_exc()}")
    
    def handle_error(
        self, 
        error: Exception, 
        context: Optional[Dict[str, Any]] = None,
        fallback_callback: Optional[callable] = None
    ) -> str:
        """
        Handle an error comprehensively.
        
        Args:
            error: The exception that occurred
            context: Additional context information
            fallback_callback: Optional callback to execute if fallback is needed
            
        Returns:
            User-friendly error message
        """
        # Log the technical details
        self.log_error(error, context)
        
        # Format user-friendly message
        user_message = self.format_user_message(error, context)
        
        # Execute fallback if appropriate
        if self.should_fallback(error) and fallback_callback:
            logger.info("Executing fallback due to error")
            try:
                fallback_result = fallback_callback()
                user_message += f"\n\n✅ Fallback executed successfully:\n{fallback_result}"
            except Exception as fallback_error:
                logger.error(f"Fallback failed: {fallback_error}")
                user_message += f"\n\n❌ Fallback also failed: {fallback_error}"
                
        return user_message


# Global instance
_error_handler = None


def get_error_handler() -> ErrorHandler:
    """Get or create the global error handler instance."""
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler()
    return _error_handler