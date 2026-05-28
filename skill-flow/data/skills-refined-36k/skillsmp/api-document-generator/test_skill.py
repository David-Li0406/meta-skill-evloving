#!/usr/bin/env python3
"""
Test script for API Documentation Generator skill.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from api_document_generator import APIDocumentGenerator


def test_skill_basic():
    """Test basic skill functionality."""
    print("Testing API Documentation Generator skill...")

    # Create a test directory structure
    test_dir = Path("test_api_files")
    test_dir.mkdir(exist_ok=True)

    # Create a simple API file for testing
    test_file = test_dir / "test_api.py"
    test_file.write_text("""
# Sample API endpoints
class UserAPI:
    def get_user(self, user_id: int):
        '''Get user by ID'''
        pass

    def create_user(self, user_data: dict):
        '''Create new user'''
        pass

class ProductAPI:
    def list_products(self, category: str = None):
        '''List products with optional category filter'''
        pass

    def get_product(self, product_id: int):
        '''Get product details'''
        pass
""")

    # Create a simple JSON API spec
    json_file = test_dir / "api_spec.json"
    json_file.write_text("""
{
  "openapi": "3.0.0",
  "info": {
    "title": "Test API",
    "version": "1.0.0"
  },
  "paths": {
    "/users": {
      "get": {
        "summary": "List users",
        "responses": {
          "200": {
            "description": "List of users"
          }
        }
      }
    }
  }
}
""")

    try:
        # Initialize the generator
        generator = APIDocumentGenerator()

        # Test with a single file
        print("\n1. Testing single file generation...")
        results = generator.generate_from_file(str(test_file))
        generator.print_results(results)

        if results.get('status') == 'success':
            print("✅ Single file test passed")
        else:
            print("❌ Single file test failed")
            print(f"Error: {results.get('message')}")

        # Test with directory
        print("\n2. Testing directory generation...")
        results = generator.generate_from_directory(str(test_dir))
        generator.print_results(results)

        if results.get('status') == 'success':
            print("✅ Directory test passed")
        else:
            print("❌ Directory test failed")
            print(f"Error: {results.get('message')}")

        # Test recent files
        print("\n3. Testing recent files...")
        results = generator.get_recent_documentation(limit=3)
        if results.get('status') == 'success':
            print(f"✅ Found {results.get('total_files', 0)} recent files")
        else:
            print("❌ Recent files test failed")

        # Test directory validation
        print("\n4. Testing directory validation...")
        results = generator.validate_output_directory()
        if results.get('status') == 'success':
            if results.get('is_valid'):
                print("✅ Output directory is valid")
            else:
                print(f"⚠️ Output directory has issues: {results.get('issues')}")
        else:
            print("❌ Directory validation test failed")

        print("\n" + "="*50)
        print("Skill test completed!")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup test files
        if test_file.exists():
            test_file.unlink()
        if json_file.exists():
            json_file.unlink()
        if test_dir.exists():
            test_dir.rmdir()

        # Cleanup output directory
        output_dir = Path(".claude/api_doc")
        if output_dir.exists():
            for file in output_dir.glob("*.md"):
                file.unlink()
            for file in output_dir.glob("*.json"):
                file.unlink()


if __name__ == "__main__":
    test_skill_basic()