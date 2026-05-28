---
name: python-docstring
description: |
  Write Python docstrings following PEP 257 and popular formats (Google, NumPy, Sphinx).
  WHEN: Writing docstrings for Python functions/classes/modules, choosing docstring format, documenting parameters/returns/exceptions.
  WHEN NOT: JavaScript documentation (use js-docstring), TypeScript (use ts-docstring), PHP (use php-docstring), general code comments.
---

# Python Docstring Standards

Comprehensive guide for writing high-quality Python docstrings following PEP 257 conventions and popular documentation formats.

## When to Use This Skill

- Writing docstrings for Python functions, methods, classes, and modules
- Improving existing documentation
- Generating API documentation
- Following team docstring conventions
- Documenting parameters, return values, exceptions, and examples

## PEP 257 Conventions

PEP 257 defines the standard conventions for Python docstrings:

### Basic Rules

1. **Triple quotes**: Always use `"""triple double quotes"""`
2. **One-line docstrings**: For simple functions, use a single line
3. **Multi-line docstrings**: Start with summary line, blank line, then details
4. **Imperative mood**: "Return the result" not "Returns the result" (for one-liners)
5. **Ending**: Multi-line docstrings should end with `"""` on its own line

### Docstring Placement

```python
def function():
    """Docstring goes here immediately after the def line."""
    pass

class MyClass:
    """Docstring for class goes here."""

    def method(self):
        """Docstring for method."""
        pass
```

## Common Docstring Formats

Python supports multiple docstring formats. Choose one and be consistent.

## Format 1: Google Style (Recommended)

Clean, readable format used by Google and many modern Python projects.

### Function Docstring

```python
def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two points.

    This function computes the straight-line distance between two points
    in a 2D coordinate system using the Pythagorean theorem.

    Args:
        x1: X-coordinate of the first point.
        y1: Y-coordinate of the first point.
        x2: X-coordinate of the second point.
        y2: Y-coordinate of the second point.

    Returns:
        The Euclidean distance between the two points as a float.

    Raises:
        TypeError: If any coordinate is not a number.

    Examples:
        >>> calculate_distance(0, 0, 3, 4)
        5.0
        >>> calculate_distance(1, 1, 4, 5)
        5.0
    """
    import math
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

### Class Docstring

```python
class DatabaseConnection:
    """Manage database connections with automatic cleanup.

    This class handles database connection lifecycle including connection
    pooling, automatic reconnection, and proper resource cleanup.

    Attributes:
        host: Database host address.
        port: Database port number.
        database: Name of the database to connect to.
        is_connected: Boolean indicating current connection status.

    Examples:
        >>> db = DatabaseConnection("localhost", 5432, "mydb")
        >>> db.connect()
        >>> db.execute_query("SELECT * FROM users")
        >>> db.disconnect()
    """

    def __init__(self, host: str, port: int, database: str):
        """Initialize database connection configuration.

        Args:
            host: Database server hostname or IP address.
            port: Port number for database connection.
            database: Name of the database to connect to.
        """
        self.host = host
        self.port = port
        self.database = database
        self.is_connected = False
```

### Method Docstring

```python
class UserService:
    """Service for managing user operations."""

    def create_user(self, username: str, email: str, password: str) -> dict:
        """Create a new user account.

        Validates user input, hashes the password, and stores the user
        in the database. Sends a welcome email upon successful creation.

        Args:
            username: Unique username for the account (3-20 characters).
            email: Valid email address for the user.
            password: Plain text password (will be hashed before storage).

        Returns:
            A dictionary containing the created user data with keys:
                - id: User's unique identifier
                - username: The username
                - email: The email address
                - created_at: Timestamp of account creation

        Raises:
            ValueError: If username or email is invalid or already exists.
            DatabaseError: If database operation fails.

        Note:
            The password is automatically hashed using bcrypt before storage.
            The returned dictionary does not include the password hash.
        """
        pass
```

### Module Docstring

```python
"""User authentication and authorization utilities.

This module provides functions and classes for handling user authentication,
session management, and role-based access control. It integrates with the
database layer and provides middleware for protecting routes.

The module supports multiple authentication methods:
    - Username/password authentication
    - OAuth 2.0 integration
    - JWT token-based authentication
    - API key authentication

Example:
    Basic usage for authenticating a user::

        from auth import authenticate_user, create_session

        user = authenticate_user("john_doe", "password123")
        session = create_session(user)

Attributes:
    SESSION_TIMEOUT (int): Default session timeout in seconds (3600).
    MAX_LOGIN_ATTEMPTS (int): Maximum failed login attempts before lockout (5).
"""

SESSION_TIMEOUT = 3600
MAX_LOGIN_ATTEMPTS = 5
```

### Class Docstring

```python
class NeuralNetwork:
    """Feedforward neural network implementation.

    A flexible neural network supporting multiple layers, activation
    functions, and optimization algorithms.

    Parameters
    ----------
    layers : list of int
        Number of neurons in each layer, e.g., [784, 128, 10].
    activation : str, optional
        Activation function to use ('relu', 'sigmoid', 'tanh').
        Default is 'relu'.
    learning_rate : float, optional
        Learning rate for gradient descent. Default is 0.001.

    Attributes
    ----------
    weights : list of ndarray
        Weight matrices for each layer.
    biases : list of ndarray
        Bias vectors for each layer.
    num_layers : int
        Total number of layers in the network.

    Methods
    -------
    train(X, y, epochs)
        Train the network on provided data.
    predict(X)
        Make predictions on new data.
    evaluate(X, y)
        Evaluate model performance.

    Examples
    --------
    >>> nn = NeuralNetwork([784, 128, 10])
    >>> nn.train(X_train, y_train, epochs=100)
    >>> predictions = nn.predict(X_test)
    """
    pass
```

## Special Cases

### Property Docstrings

```python
class User:
    """Represents a user in the system."""

    @property
    def full_name(self) -> str:
        """str: The user's full name (first name + last name)."""
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        """int: The user's age calculated from birth date.

        Returns the current age in years. Raises ValueError if
        birth_date is not set.
        """
        if not self.birth_date:
            raise ValueError("Birth date not set")
        # Calculate age...
        return calculated_age
```

### Generator Docstrings

```python
def fibonacci(n: int):
    """Generate Fibonacci sequence up to n terms.

    Args:
        n: Number of Fibonacci numbers to generate.

    Yields:
        int: Next number in the Fibonacci sequence.

    Examples:
        >>> list(fibonacci(5))
        [0, 1, 1, 2, 3]
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
```

### Async Function Docstrings

```python
async def fetch_api_data(url: str, timeout: int = 30) -> dict:
    """Asynchronously fetch data from an API endpoint.

    Makes an HTTP GET request to the specified URL and returns the
    JSON response. Implements retry logic with exponential backoff.

    Args:
        url: The API endpoint URL to fetch from.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response as a dictionary.

    Raises:
        TimeoutError: If the request exceeds the timeout.
        APIError: If the API returns an error response.

    Note:
        This function is asynchronous and must be awaited.

    Examples:
        >>> data = await fetch_api_data("https://api.example.com/users")
        >>> print(data['count'])
        100
    """
    pass
```

### Private Method Docstrings

```python
class DataProcessor:
    """Process and transform data."""

    def _validate_input(self, data: dict) -> bool:
        """Validate input data structure (internal use only).

        Args:
            data: Dictionary to validate.

        Returns:
            True if valid, False otherwise.

        Note:
            This is a private method and should not be called externally.
        """
        pass
```

## Type Hints vs Docstrings

With Python 3.5+ type hints, you can reduce redundancy:

```python
# Good: Type hints + concise docstring
def process_order(order_id: int, customer_email: str) -> bool:
    """Process a customer order and send confirmation email.

    Args:
        order_id: Unique identifier for the order.
        customer_email: Email address for order confirmation.

    Returns:
        True if order processed successfully, False otherwise.
    """
    pass

# Avoid: Redundant type information in docstring
def process_order(order_id: int, customer_email: str) -> bool:
    """Process a customer order and send confirmation email.

    Args:
        order_id (int): Unique identifier for the order.  # Redundant!
        customer_email (str): Email address for confirmation.  # Redundant!

    Returns:
        bool: True if successful, False otherwise.  # Redundant!
    """
    pass
```

## Best Practices

### DO

- Start with a concise summary line
- Use present tense: "Calculate" not "Calculates"
- Document all public APIs
- Include examples for complex functions
- Document exceptions that can be raised
- Keep docstrings up to date with code changes
- Use type hints instead of repeating types in docstrings

### DON'T

- Don't document obvious things excessively
- Don't repeat information from type hints
- Don't write novels - be concise
- Don't forget to update docstrings when code changes
- Don't use docstrings for commented-out code
- Don't document private methods unless complex

## Validation Tools

```bash
# Check docstring coverage
pip install interrogate
interrogate -v myproject/

# Validate docstring format
pip install pydocstyle
pydocstyle myproject/

# Generate documentation
pip install sphinx
sphinx-quickstart
sphinx-build -b html docs/ docs/_build/
```

## Resources

- **PEP 257**: Official docstring conventions
- **pydocstyle**: Docstring style checker
- **interrogate**: Check docstring coverage
