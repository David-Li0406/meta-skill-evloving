# User Management with Clerk Backend SDK

Complete guide for managing users programmatically using the Clerk Backend SDK.

## Installation

```bash
pip install clerk-backend-api
```

## Setup

```python
import os
from clerk_backend_api import Clerk
from dotenv import load_dotenv

load_dotenv()

# Initialize Clerk SDK
clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))
```

## User Operations

### Get User by ID

```python
def get_user(user_id: str):
    """
    Retrieve a user by their Clerk ID.
    
    Args:
        user_id: The Clerk user ID
        
    Returns:
        User object with all user information
    """
    try:
        user = clerk.users.get(user_id=user_id)
        
        print(f"User ID: {user.id}")
        print(f"Email: {user.email_addresses[0].email_address if user.email_addresses else 'None'}")
        print(f"Name: {user.first_name} {user.last_name}")
        print(f"Created: {user.created_at}")
        
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
```

### List All Users

```python
def list_users(limit=10, offset=0):
    """
    List users with pagination.
    
    Args:
        limit: Number of users to return
        offset: Number of users to skip
        
    Returns:
        List of user objects
    """
    try:
        response = clerk.users.list(
            limit=limit,
            offset=offset
        )
        
        for user in response.data:
            print(f"ID: {user.id}, Email: {user.email_addresses[0].email_address if user.email_addresses else 'None'}")
        
        print(f"\nTotal users: {response.total_count}")
        return response.data
    except Exception as e:
        print(f"Error listing users: {e}")
        return []
```

### Search Users

```python
def search_users(email=None, phone=None, username=None):
    """
    Search users by email, phone, or username.
    
    Args:
        email: Email address to search for
        phone: Phone number to search for
        username: Username to search for
        
    Returns:
        List of matching users
    """
    try:
        params = {}
        if email:
            params['email_address'] = [email]
        if phone:
            params['phone_number'] = [phone]
        if username:
            params['username'] = [username]
        
        response = clerk.users.list(**params)
        return response.data
    except Exception as e:
        print(f"Error searching users: {e}")
        return []
```

### Create User

```python
def create_user(email: str, password: str, first_name: str = None, last_name: str = None):
    """
    Create a new user programmatically.
    
    Args:
        email: User's email address
        password: User's password
        first_name: User's first name (optional)
        last_name: User's last name (optional)
        
    Returns:
        Created user object
    """
    try:
        user = clerk.users.create(
            email_address=[email],
            password=password,
            first_name=first_name,
            last_name=last_name,
            skip_password_checks=False,  # Enforce password requirements
            skip_password_requirement=False
        )
        
        print(f"User created successfully: {user.id}")
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None
```

### Update User

```python
def update_user(user_id: str, **kwargs):
    """
    Update user information.
    
    Args:
        user_id: The Clerk user ID
        **kwargs: Fields to update (first_name, last_name, etc.)
        
    Returns:
        Updated user object
        
    Example:
        update_user(user_id, first_name="John", last_name="Doe")
    """
    try:
        user = clerk.users.update(
            user_id=user_id,
            **kwargs
        )
        
        print(f"User updated successfully: {user.id}")
        return user
    except Exception as e:
        print(f"Error updating user: {e}")
        return None
```

### Delete User

```python
def delete_user(user_id: str):
    """
    Delete a user permanently.
    
    Args:
        user_id: The Clerk user ID
        
    Returns:
        Deleted user object
    """
    try:
        result = clerk.users.delete(user_id=user_id)
        print(f"User deleted successfully: {user_id}")
        return result
    except Exception as e:
        print(f"Error deleting user: {e}")
        return None
```

### Ban/Unban User

```python
def ban_user(user_id: str):
    """
    Ban a user from accessing the application.
    
    Args:
        user_id: The Clerk user ID
        
    Returns:
        Updated user object
    """
    try:
        user = clerk.users.ban(user_id=user_id)
        print(f"User banned: {user_id}")
        return user
    except Exception as e:
        print(f"Error banning user: {e}")
        return None

def unban_user(user_id: str):
    """
    Unban a previously banned user.
    
    Args:
        user_id: The Clerk user ID
        
    Returns:
        Updated user object
    """
    try:
        user = clerk.users.unban(user_id=user_id)
        print(f"User unbanned: {user_id}")
        return user
    except Exception as e:
        print(f"Error unbanning user: {e}")
        return None
```

### Lock/Unlock User

```python
def lock_user(user_id: str):
    """
    Lock a user account temporarily.
    
    Args:
        user_id: The Clerk user ID
        
    Returns:
        Updated user object
    """
    try:
        user = clerk.users.lock(user_id=user_id)
        print(f"User locked: {user_id}")
        return user
    except Exception as e:
        print(f"Error locking user: {e}")
        return None

def unlock_user(user_id: str):
    """
    Unlock a previously locked user account.
    
    Args:
        user_id: The Clerk user ID
        
    Returns:
        Updated user object
    """
    try:
        user = clerk.users.unlock(user_id=user_id)
        print(f"User unlocked: {user_id}")
        return user
    except Exception as e:
        print(f"Error unlocking user: {e}")
        return None
```

## User Metadata

### Update User Metadata

```python
def update_user_metadata(user_id: str, public_metadata=None, private_metadata=None, unsafe_metadata=None):
    """
    Update user metadata.
    
    Metadata types:
    - public_metadata: Accessible by frontend, stored in JWT
    - private_metadata: Only accessible by backend
    - unsafe_metadata: Accessible by frontend, updatable by user
    
    Args:
        user_id: The Clerk user ID
        public_metadata: Public metadata dictionary
        private_metadata: Private metadata dictionary
        unsafe_metadata: Unsafe metadata dictionary
        
    Returns:
        Updated user object
        
    Example:
        update_user_metadata(
            user_id,
            public_metadata={"role": "admin", "department": "IT"},
            private_metadata={"internal_id": "EMP123"}
        )
    """
    try:
        update_data = {}
        if public_metadata is not None:
            update_data['public_metadata'] = public_metadata
        if private_metadata is not None:
            update_data['private_metadata'] = private_metadata
        if unsafe_metadata is not None:
            update_data['unsafe_metadata'] = unsafe_metadata
        
        user = clerk.users.update_metadata(
            user_id=user_id,
            **update_data
        )
        
        print(f"User metadata updated: {user_id}")
        return user
    except Exception as e:
        print(f"Error updating metadata: {e}")
        return None
```

### Get User Metadata

```python
def get_user_with_metadata(user_id: str):
    """
    Get user with all metadata fields.
    
    Args:
        user_id: The Clerk user ID
        
    Returns:
        User object with metadata
    """
    try:
        user = clerk.users.get(user_id=user_id)
        
        print(f"Public Metadata: {user.public_metadata}")
        print(f"Private Metadata: {user.private_metadata}")
        print(f"Unsafe Metadata: {user.unsafe_metadata}")
        
        return user
    except Exception as e:
        print(f"Error fetching user metadata: {e}")
        return None
```

## Email Operations

### Get User by Email

```python
def get_user_by_email(email: str):
    """
    Find a user by their email address.
    
    Args:
        email: Email address to search for
        
    Returns:
        User object if found, None otherwise
    """
    try:
        response = clerk.users.list(email_address=[email])
        
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error finding user by email: {e}")
        return None
```

### Verify Email

```python
def verify_email(email_address_id: str):
    """
    Mark an email address as verified.
    
    Args:
        email_address_id: The email address ID (not the user ID)
        
    Returns:
        Updated email address object
    """
    try:
        email = clerk.email_addresses.update(
            email_address_id=email_address_id,
            verified=True
        )
        print(f"Email verified: {email_address_id}")
        return email
    except Exception as e:
        print(f"Error verifying email: {e}")
        return None
```

## OAuth Tokens

### Get OAuth Access Token

```python
def get_oauth_access_token(user_id: str, provider: str):
    """
    Get OAuth access token for a user's connected account.
    
    Args:
        user_id: The Clerk user ID
        provider: OAuth provider (e.g., 'oauth_google', 'oauth_github')
        
    Returns:
        OAuth token information
        
    Example:
        token = get_oauth_access_token(user_id, "oauth_google")
        print(token.token)  # Use this to make API calls to Google
    """
    try:
        token = clerk.users.get_o_auth_access_token(
            user_id=user_id,
            provider=provider
        )
        return token
    except Exception as e:
        print(f"Error getting OAuth token: {e}")
        return None
```

## Organization Memberships

### Get User's Organizations

```python
def get_user_organizations(user_id: str):
    """
    Get all organizations a user is a member of.
    
    Args:
        user_id: The Clerk user ID
        
    Returns:
        List of organization memberships
    """
    try:
        memberships = clerk.users.get_organization_memberships(
            user_id=user_id
        )
        
        for membership in memberships.data:
            print(f"Organization: {membership.organization.name}")
            print(f"Role: {membership.role}")
        
        return memberships.data
    except Exception as e:
        print(f"Error fetching user organizations: {e}")
        return []
```

## Session Management

### Get User Sessions

```python
def get_user_sessions(user_id: str):
    """
    Get all active sessions for a user.
    
    Args:
        user_id: The Clerk user ID
        
    Returns:
        List of session objects
    """
    try:
        response = clerk.sessions.list(
            user_id=user_id,
            status='active'
        )
        
        for session in response.data:
            print(f"Session ID: {session.id}")
            print(f"Created: {session.created_at}")
            print(f"Expires: {session.expire_at}")
        
        return response.data
    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return []
```

### Revoke Session

```python
def revoke_session(session_id: str):
    """
    Revoke a specific session, logging the user out.
    
    Args:
        session_id: The session ID to revoke
        
    Returns:
        Revoked session object
    """
    try:
        session = clerk.sessions.revoke(session_id=session_id)
        print(f"Session revoked: {session_id}")
        return session
    except Exception as e:
        print(f"Error revoking session: {e}")
        return None
```

## Password Management

### Verify User Password

```python
def verify_password(user_id: str, password: str):
    """
    Verify a user's password.
    
    Args:
        user_id: The Clerk user ID
        password: Password to verify
        
    Returns:
        Boolean indicating if password is correct
    """
    try:
        result = clerk.users.verify_password(
            user_id=user_id,
            password=password
        )
        return result.verified
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False
```

## Complete User Management Class

```python
class UserManager:
    """
    Complete user management wrapper for Clerk operations.
    """
    
    def __init__(self, secret_key: str):
        self.clerk = Clerk(bearer_auth=secret_key)
    
    def get(self, user_id: str):
        """Get user by ID."""
        return self.clerk.users.get(user_id=user_id)
    
    def list(self, **kwargs):
        """List users with filters."""
        return self.clerk.users.list(**kwargs)
    
    def create(self, **kwargs):
        """Create new user."""
        return self.clerk.users.create(**kwargs)
    
    def update(self, user_id: str, **kwargs):
        """Update user."""
        return self.clerk.users.update(user_id=user_id, **kwargs)
    
    def delete(self, user_id: str):
        """Delete user."""
        return self.clerk.users.delete(user_id=user_id)
    
    def ban(self, user_id: str):
        """Ban user."""
        return self.clerk.users.ban(user_id=user_id)
    
    def unban(self, user_id: str):
        """Unban user."""
        return self.clerk.users.unban(user_id=user_id)
    
    def lock(self, user_id: str):
        """Lock user account."""
        return self.clerk.users.lock(user_id=user_id)
    
    def unlock(self, user_id: str):
        """Unlock user account."""
        return self.clerk.users.unlock(user_id=user_id)
    
    def update_metadata(self, user_id: str, **metadata):
        """Update user metadata."""
        return self.clerk.users.update_metadata(user_id=user_id, **metadata)
    
    def find_by_email(self, email: str):
        """Find user by email."""
        response = self.clerk.users.list(email_address=[email])
        return response.data[0] if response.data else None
    
    def get_organizations(self, user_id: str):
        """Get user's organizations."""
        return self.clerk.users.get_organization_memberships(user_id=user_id)
    
    def get_sessions(self, user_id: str):
        """Get user's active sessions."""
        return self.clerk.sessions.list(user_id=user_id, status='active')

# Usage
user_manager = UserManager(os.getenv("CLERK_SECRET_KEY"))
user = user_manager.get("user_123")
```

## Integration with FastAPI

```python
from fastapi import FastAPI, Depends, HTTPException
from auth import verify_clerk_token
from typing import Optional

app = FastAPI()

# Initialize user manager
user_manager = UserManager(os.getenv("CLERK_SECRET_KEY"))

@app.get("/admin/users")
async def list_users(
    limit: int = 10,
    offset: int = 0,
    auth_data = Depends(verify_clerk_token)
):
    """Admin endpoint to list users."""
    # Verify admin role
    if "admin" not in auth_data["payload"].get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    response = user_manager.list(limit=limit, offset=offset)
    return {
        "users": response.data,
        "total": response.total_count
    }

@app.get("/admin/users/{user_id}")
async def get_user(
    user_id: str,
    auth_data = Depends(verify_clerk_token)
):
    """Admin endpoint to get specific user."""
    if "admin" not in auth_data["payload"].get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = user_manager.get(user_id)
    return user

@app.patch("/admin/users/{user_id}")
async def update_user(
    user_id: str,
    updates: dict,
    auth_data = Depends(verify_clerk_token)
):
    """Admin endpoint to update user."""
    if "admin" not in auth_data["payload"].get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = user_manager.update(user_id, **updates)
    return user

@app.post("/admin/users/{user_id}/ban")
async def ban_user(
    user_id: str,
    auth_data = Depends(verify_clerk_token)
):
    """Admin endpoint to ban user."""
    if "admin" not in auth_data["payload"].get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = user_manager.ban(user_id)
    return {"message": "User banned successfully", "user_id": user_id}
```

## Next Steps

- See [fastapi-backend.md](fastapi-backend.md) for authentication implementation
- See [organizations.md](organizations.md) for organization management
- See [examples.md](examples.md) for complete working examples
