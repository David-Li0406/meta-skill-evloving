#!/usr/bin/env python3
"""
Validate Google Play Store API connection.
Tests that service account has proper access to Play Console.

Usage:
    python validate-playstore.py <service-account.json> <package-name>

Example:
    python validate-playstore.py service-account.json com.example.app
"""

import sys
import json
from pathlib import Path


def validate_service_account_json(json_path):
    """Validate service account JSON file format and required fields."""
    print("Validating service account JSON...")
    
    # Check file exists
    if not Path(json_path).exists():
        print(f"❌ File not found: {json_path}")
        return False
    
    # Load and parse JSON
    try:
        with open(json_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False
    
    # Check required fields
    required_fields = {
        "type": "service_account",
        "project_id": str,
        "private_key_id": str,
        "private_key": str,
        "client_email": str,
        "client_id": str
    }
    
    for field, expected_type in required_fields.items():
        if field not in data:
            print(f"❌ Missing required field: {field}")
            return False
        
        if field == "type" and data[field] != expected_type:
            print(f"❌ Invalid type: {data[field]} (expected 'service_account')")
            return False
    
    # Validate email format
    email = data["client_email"]
    if not email.endswith(".iam.gserviceaccount.com"):
        print(f"⚠️  Warning: Unexpected email format: {email}")
        print(f"   Expected format: name@project.iam.gserviceaccount.com")
    
    # Validate private key format
    private_key = data["private_key"]
    if not private_key.startswith("-----BEGIN PRIVATE KEY-----"):
        print(f"❌ Invalid private_key format")
        return False
    
    print(f"✅ Service account JSON is valid")
    print(f"   Email: {email}")
    print(f"   Project: {data['project_id']}")
    
    return True


def test_api_connection(json_path, package_name):
    """Test connection to Google Play Developer API."""
    print(f"\nTesting API connection for package: {package_name}...")
    
    # Check if required packages are installed
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
    except ImportError:
        print("❌ Required packages not installed")
        print("\n   Install with:")
        print("   pip install google-auth google-api-python-client")
        return False
    
    try:
        # Authenticate with service account
        credentials = service_account.Credentials.from_service_account_file(
            json_path,
            scopes=['https://www.googleapis.com/auth/androidpublisher']
        )
        
        print("✅ Service account credentials loaded")
        
        # Build API service
        service = build('androidpublisher', 'v3', credentials=credentials)
        
        print("✅ Play Developer API service created")
        
        # Try to create an edit (validates API access and app existence)
        edit_request = service.edits().insert(body={}, packageName=package_name)
        edit_result = edit_request.execute()
        edit_id = edit_result['id']
        
        print(f"✅ Successfully connected to Play Developer API")
        print(f"   Can access package: {package_name}")
        
        # Try to get tracks info
        try:
            tracks_response = service.edits().tracks().list(
                packageName=package_name,
                editId=edit_id
            ).execute()
            
            tracks = [track['track'] for track in tracks_response.get('tracks', [])]
            if tracks:
                print(f"   Available tracks: {', '.join(tracks)}")
            else:
                print(f"   No releases yet (normal for new apps)")
                
        except Exception as e:
            print(f"   ⚠️  Could not list tracks: {str(e)}")
        
        # Clean up edit
        service.edits().delete(packageName=package_name, editId=edit_id).execute()
        
        return True
        
    except HttpError as e:
        error_details = str(e)
        
        if "404" in error_details:
            print(f"❌ App not found in Play Console")
            print(f"\n   Possible causes:")
            print(f"   → Package name is incorrect: {package_name}")
            print(f"   → App hasn't been created in Play Console yet")
            print(f"   → Service account doesn't have access to this app")
            print(f"\n   Fix:")
            print(f"   → Verify package name matches exactly")
            print(f"   → Create app in Play Console first")
            print(f"   → Check service account permissions")
            
        elif "403" in error_details:
            print(f"❌ Permission denied")
            print(f"\n   Possible causes:")
            print(f"   → Service account not linked in Play Console")
            print(f"   → Service account lacks required permissions")
            print(f"\n   Fix:")
            print(f"   → Go to Play Console → Setup → API access")
            print(f"   → Grant 'Release' permission to service account")
            print(f"   → Wait 5-10 minutes for permissions to propagate")
            
        elif "401" in error_details:
            print(f"❌ Authentication failed")
            print(f"\n   Possible causes:")
            print(f"   → Service account JSON is invalid")
            print(f"   → Service account has been deleted")
            print(f"\n   Fix:")
            print(f"   → Re-download service account JSON from Google Cloud")
            print(f"   → Verify JSON file is complete and valid")
            
        else:
            print(f"❌ API error: {error_details}")
        
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


def main():
    """Main validation function."""
    if len(sys.argv) < 3:
        print("Usage: python validate-playstore.py <service-account.json> <package-name>")
        print("\nExample:")
        print("  python validate-playstore.py service-account.json com.example.app")
        sys.exit(1)
    
    json_path = sys.argv[1]
    package_name = sys.argv[2]
    
    print("=" * 60)
    print("Play Store API Validation")
    print("=" * 60)
    print()
    
    # Step 1: Validate JSON file
    if not validate_service_account_json(json_path):
        print("\n" + "=" * 60)
        print("❌ Validation FAILED - JSON file is invalid")
        print("=" * 60)
        sys.exit(1)
    
    # Step 2: Test API connection
    if not test_api_connection(json_path, package_name):
        print("\n" + "=" * 60)
        print("❌ Validation FAILED - API connection failed")
        print("=" * 60)
        sys.exit(1)
    
    # Success!
    print("\n" + "=" * 60)
    print("✅ All validations passed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Add SERVICE_ACCOUNT_JSON to GitHub Secrets")
    print("   → Repository → Settings → Secrets → Actions")
    print("   → New repository secret")
    print("   → Name: SERVICE_ACCOUNT_JSON")
    print("   → Value: [paste entire JSON file contents]")
    print("\n2. Run android-playstore-publishing skill")
    print("   → Generate GitHub Actions workflow")
    print("\n3. Deploy your app!")
    print("   → Push to repository or trigger workflow manually")


if __name__ == "__main__":
    main()
