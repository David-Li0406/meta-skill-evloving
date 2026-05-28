# Organizations Implementation Guide

Complete guide for implementing multi-tenant features with Clerk Organizations.

## What are Organizations?

Organizations allow you to group users together and manage shared resources. They're perfect for:
- B2B SaaS applications
- Team collaboration tools  
- Multi-tenant applications
- Project management systems

## Installation

Organizations are included in the Clerk SDK:

```bash
# Backend
pip install clerk-backend-api

# Frontend
npm install @clerk/clerk-react
```

## Backend Organization Management

### Initialize Clerk

```python
import os
from clerk_backend_api import Clerk
from dotenv import load_dotenv

load_dotenv()
clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))
```

### Create Organization

```python
def create_organization(name: str, created_by: str, slug: str = None):
    """
    Create a new organization.
    
    Args:
        name: Organization name
        created_by: User ID of the creator
        slug: Optional URL-friendly identifier
        
    Returns:
        Created organization object
        
    Example:
        org = create_organization("Acme Corp", user_id, "acme-corp")
    """
    try:
        organization = clerk.organizations.create(
            name=name,
            created_by=created_by,
            slug=slug
        )
        
        print(f"Organization created: {organization.id}")
        print(f"Name: {organization.name}")
        print(f"Slug: {organization.slug}")
        
        return organization
    except Exception as e:
        print(f"Error creating organization: {e}")
        return None
```

### Get Organization

```python
def get_organization(organization_id: str):
    """
    Get organization by ID.
    
    Args:
        organization_id: The organization ID
        
    Returns:
        Organization object
    """
    try:
        org = clerk.organizations.get(organization_id=organization_id)
        return org
    except Exception as e:
        print(f"Error fetching organization: {e}")
        return None
```

### List Organizations

```python
def list_organizations(limit=10, offset=0):
    """
    List all organizations.
    
    Args:
        limit: Number of organizations to return
        offset: Number of organizations to skip
        
    Returns:
        List of organization objects
    """
    try:
        response = clerk.organizations.list(
            limit=limit,
            offset=offset
        )
        
        for org in response.data:
            print(f"ID: {org.id}, Name: {org.name}, Members: {org.members_count}")
        
        return response.data
    except Exception as e:
        print(f"Error listing organizations: {e}")
        return []
```

### Update Organization

```python
def update_organization(organization_id: str, name: str = None, slug: str = None):
    """
    Update organization details.
    
    Args:
        organization_id: The organization ID
        name: New organization name
        slug: New organization slug
        
    Returns:
        Updated organization object
    """
    try:
        update_data = {}
        if name:
            update_data['name'] = name
        if slug:
            update_data['slug'] = slug
        
        org = clerk.organizations.update(
            organization_id=organization_id,
            **update_data
        )
        
        print(f"Organization updated: {org.id}")
        return org
    except Exception as e:
        print(f"Error updating organization: {e}")
        return None
```

### Delete Organization

```python
def delete_organization(organization_id: str):
    """
    Delete an organization.
    
    Args:
        organization_id: The organization ID
        
    Returns:
        Deleted organization object
    """
    try:
        result = clerk.organizations.delete(organization_id=organization_id)
        print(f"Organization deleted: {organization_id}")
        return result
    except Exception as e:
        print(f"Error deleting organization: {e}")
        return None
```

## Organization Memberships

### Add Member to Organization

```python
def add_organization_member(organization_id: str, user_id: str, role: str = "basic_member"):
    """
    Add a user to an organization.
    
    Args:
        organization_id: The organization ID
        user_id: The user ID to add
        role: Member role (e.g., 'admin', 'basic_member')
        
    Returns:
        Organization membership object
        
    Example:
        membership = add_organization_member(org_id, user_id, "admin")
    """
    try:
        membership = clerk.organization_memberships.create(
            organization_id=organization_id,
            user_id=user_id,
            role=role
        )
        
        print(f"User {user_id} added to organization {organization_id} as {role}")
        return membership
    except Exception as e:
        print(f"Error adding member: {e}")
        return None
```

### List Organization Members

```python
def list_organization_members(organization_id: str):
    """
    List all members of an organization.
    
    Args:
        organization_id: The organization ID
        
    Returns:
        List of organization membership objects
    """
    try:
        response = clerk.organization_memberships.list(
            organization_id=organization_id
        )
        
        for membership in response.data:
            user = membership.public_user_data
            print(f"User: {user.first_name} {user.last_name}, Role: {membership.role}")
        
        return response.data
    except Exception as e:
        print(f"Error listing members: {e}")
        return []
```

### Update Member Role

```python
def update_member_role(organization_id: str, user_id: str, new_role: str):
    """
    Update a member's role in an organization.
    
    Args:
        organization_id: The organization ID
        user_id: The user ID
        new_role: New role to assign
        
    Returns:
        Updated membership object
    """
    try:
        membership = clerk.organization_memberships.update(
            organization_id=organization_id,
            user_id=user_id,
            role=new_role
        )
        
        print(f"User {user_id} role updated to {new_role}")
        return membership
    except Exception as e:
        print(f"Error updating role: {e}")
        return None
```

### Remove Member from Organization

```python
def remove_organization_member(organization_id: str, user_id: str):
    """
    Remove a user from an organization.
    
    Args:
        organization_id: The organization ID
        user_id: The user ID to remove
        
    Returns:
        Deleted membership object
    """
    try:
        result = clerk.organization_memberships.delete(
            organization_id=organization_id,
            user_id=user_id
        )
        
        print(f"User {user_id} removed from organization {organization_id}")
        return result
    except Exception as e:
        print(f"Error removing member: {e}")
        return None
```

## Organization Invitations

### Create Invitation

```python
def invite_to_organization(organization_id: str, email: str, role: str = "basic_member"):
    """
    Invite a user to an organization via email.
    
    Args:
        organization_id: The organization ID
        email: Email address to invite
        role: Role to assign when user accepts
        
    Returns:
        Organization invitation object
    """
    try:
        invitation = clerk.organization_invitations.create(
            organization_id=organization_id,
            email_address=email,
            role=role
        )
        
        print(f"Invitation sent to {email}")
        return invitation
    except Exception as e:
        print(f"Error sending invitation: {e}")
        return None
```

### List Pending Invitations

```python
def list_pending_invitations(organization_id: str):
    """
    List all pending invitations for an organization.
    
    Args:
        organization_id: The organization ID
        
    Returns:
        List of invitation objects
    """
    try:
        response = clerk.organization_invitations.list_pending(
            organization_id=organization_id
        )
        
        for invitation in response.data:
            print(f"Email: {invitation.email_address}, Role: {invitation.role}, Status: {invitation.status}")
        
        return response.data
    except Exception as e:
        print(f"Error listing invitations: {e}")
        return []
```

### Revoke Invitation

```python
def revoke_invitation(organization_id: str, invitation_id: str):
    """
    Revoke a pending organization invitation.
    
    Args:
        organization_id: The organization ID
        invitation_id: The invitation ID
        
    Returns:
        Revoked invitation object
    """
    try:
        result = clerk.organization_invitations.revoke(
            organization_id=organization_id,
            invitation_id=invitation_id
        )
        
        print(f"Invitation revoked: {invitation_id}")
        return result
    except Exception as e:
        print(f"Error revoking invitation: {e}")
        return None
```

## Frontend Organization Components

### Organization Switcher

```javascript
// src/components/OrganizationSwitcher.jsx
import { OrganizationSwitcher } from '@clerk/clerk-react'

export default function OrgSwitcher() {
  return (
    <OrganizationSwitcher
      hidePersonal={false}
      afterCreateOrganizationUrl="/dashboard"
      afterSelectOrganizationUrl="/dashboard"
      appearance={{
        elements: {
          rootBox: 'flex items-center',
          organizationSwitcherTrigger: 'px-4 py-2 rounded-md'
        }
      }}
    />
  )
}
```

### Organization Profile

```javascript
// src/pages/OrganizationProfilePage.jsx
import { OrganizationProfile } from '@clerk/clerk-react'

export default function OrganizationProfilePage() {
  return (
    <div className="flex justify-center p-8">
      <OrganizationProfile
        routing="path"
        path="/organization-profile"
      />
    </div>
  )
}
```

### Create Organization

```javascript
// src/pages/CreateOrganizationPage.jsx
import { CreateOrganization } from '@clerk/clerk-react'

export default function CreateOrganizationPage() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <CreateOrganization
        routing="path"
        path="/create-organization"
        afterCreateOrganizationUrl="/dashboard"
      />
    </div>
  )
}
```

### Using Organization Hooks

```javascript
// src/components/OrganizationInfo.jsx
import { useOrganization, useOrganizationList } from '@clerk/clerk-react'

export default function OrganizationInfo() {
  const { organization, membership } = useOrganization()
  const { organizationList } = useOrganizationList()

  if (!organization) {
    return <div>No organization selected</div>
  }

  return (
    <div className="p-4">
      <h2>Current Organization</h2>
      <p>Name: {organization.name}</p>
      <p>Slug: {organization.slug}</p>
      <p>Your Role: {membership?.role}</p>
      <p>Members: {organization.membersCount}</p>
      
      <h3>Your Organizations</h3>
      <ul>
        {organizationList?.map(org => (
          <li key={org.organization.id}>
            {org.organization.name} - {org.membership.role}
          </li>
        ))}
      </ul>
    </div>
  )
}
```

## FastAPI Integration with Organizations

```python
from fastapi import FastAPI, Depends, HTTPException
from auth import verify_clerk_token

app = FastAPI()

@app.get("/organizations")
async def list_user_organizations(auth_data = Depends(verify_clerk_token)):
    """
    List all organizations the current user belongs to.
    """
    user_id = auth_data["user_id"]
    
    try:
        memberships = clerk.users.get_organization_memberships(user_id=user_id)
        
        organizations = []
        for membership in memberships.data:
            organizations.append({
                "id": membership.organization.id,
                "name": membership.organization.name,
                "slug": membership.organization.slug,
                "role": membership.role
            })
        
        return {"organizations": organizations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/organizations")
async def create_new_organization(
    name: str,
    slug: str = None,
    auth_data = Depends(verify_clerk_token)
):
    """
    Create a new organization.
    """
    user_id = auth_data["user_id"]
    
    try:
        org = clerk.organizations.create(
            name=name,
            created_by=user_id,
            slug=slug
        )
        
        return {
            "id": org.id,
            "name": org.name,
            "slug": org.slug
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/organizations/{org_id}/members")
async def get_organization_members(
    org_id: str,
    auth_data = Depends(verify_clerk_token)
):
    """
    Get all members of an organization.
    Requires user to be a member of the organization.
    """
    # Verify user is member of the organization
    user_orgs = clerk.users.get_organization_memberships(
        user_id=auth_data["user_id"]
    )
    
    is_member = any(m.organization.id == org_id for m in user_orgs.data)
    if not is_member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    
    try:
        memberships = clerk.organization_memberships.list(
            organization_id=org_id
        )
        
        members = []
        for membership in memberships.data:
            user_data = membership.public_user_data
            members.append({
                "user_id": membership.public_user_data.user_id,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "email": user_data.identifier,
                "role": membership.role
            })
        
        return {"members": members}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/organizations/{org_id}/members")
async def add_member_to_organization(
    org_id: str,
    user_id: str,
    role: str = "basic_member",
    auth_data = Depends(verify_clerk_token)
):
    """
    Add a member to an organization.
    Requires admin role in the organization.
    """
    # Check if user is admin
    user_orgs = clerk.users.get_organization_memberships(
        user_id=auth_data["user_id"]
    )
    
    user_org = next((m for m in user_orgs.data if m.organization.id == org_id), None)
    if not user_org or user_org.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    
    try:
        membership = clerk.organization_memberships.create(
            organization_id=org_id,
            user_id=user_id,
            role=role
        )
        
        return {"message": "Member added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Organization Metadata

```python
def update_organization_metadata(organization_id: str, metadata: dict):
    """
    Update organization metadata.
    
    Args:
        organization_id: The organization ID
        metadata: Metadata dictionary
        
    Returns:
        Updated organization object
    """
    try:
        org = clerk.organizations.update_metadata(
            organization_id=organization_id,
            public_metadata=metadata
        )
        
        print(f"Organization metadata updated: {org.id}")
        return org
    except Exception as e:
        print(f"Error updating metadata: {e}")
        return None

# Example usage
metadata = {
    "plan": "enterprise",
    "max_users": 100,
    "features": ["sso", "custom_domain", "advanced_analytics"]
}
update_organization_metadata(org_id, metadata)
```

## Complete Organization Manager Class

```python
class OrganizationManager:
    """Complete organization management wrapper."""
    
    def __init__(self, secret_key: str):
        self.clerk = Clerk(bearer_auth=secret_key)
    
    def create(self, name: str, created_by: str, slug: str = None):
        """Create organization."""
        return self.clerk.organizations.create(
            name=name,
            created_by=created_by,
            slug=slug
        )
    
    def get(self, organization_id: str):
        """Get organization."""
        return self.clerk.organizations.get(organization_id=organization_id)
    
    def list(self, **kwargs):
        """List organizations."""
        return self.clerk.organizations.list(**kwargs)
    
    def update(self, organization_id: str, **kwargs):
        """Update organization."""
        return self.clerk.organizations.update(
            organization_id=organization_id,
            **kwargs
        )
    
    def delete(self, organization_id: str):
        """Delete organization."""
        return self.clerk.organizations.delete(organization_id=organization_id)
    
    def add_member(self, organization_id: str, user_id: str, role: str = "basic_member"):
        """Add member."""
        return self.clerk.organization_memberships.create(
            organization_id=organization_id,
            user_id=user_id,
            role=role
        )
    
    def list_members(self, organization_id: str):
        """List members."""
        return self.clerk.organization_memberships.list(
            organization_id=organization_id
        )
    
    def update_member_role(self, organization_id: str, user_id: str, role: str):
        """Update member role."""
        return self.clerk.organization_memberships.update(
            organization_id=organization_id,
            user_id=user_id,
            role=role
        )
    
    def remove_member(self, organization_id: str, user_id: str):
        """Remove member."""
        return self.clerk.organization_memberships.delete(
            organization_id=organization_id,
            user_id=user_id
        )
    
    def invite(self, organization_id: str, email: str, role: str = "basic_member"):
        """Invite member."""
        return self.clerk.organization_invitations.create(
            organization_id=organization_id,
            email_address=email,
            role=role
        )
    
    def list_invitations(self, organization_id: str):
        """List pending invitations."""
        return self.clerk.organization_invitations.list_pending(
            organization_id=organization_id
        )

# Usage
org_manager = OrganizationManager(os.getenv("CLERK_SECRET_KEY"))
org = org_manager.create("My Company", user_id, "my-company")
```

## Next Steps

- See [fastapi-backend.md](fastapi-backend.md) for authentication
- See [user-management.md](user-management.md) for user operations
- See [examples.md](examples.md) for complete examples
