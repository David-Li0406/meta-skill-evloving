#!/usr/bin/env python3
"""
Simple test script for API Documentation Generator skill (Windows compatible).
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from api_document_generator import APIDocumentGenerator


def test_skill_simple():
    """Test basic skill functionality without Unicode."""
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

    try:
        # Initialize the generator
        generator = APIDocumentGenerator()

        # Test with a single file
        print("\n1. Testing single file generation...")
        results = generator.generate_from_file(str(test_file))

        if results.get('status') == 'success':
            print("[OK] Single file test passed")
            print(f"Generated file: {results.get('generated_files', [{}])[0].get('path', 'unknown')}")
        else:
            print("[ERROR] Single file test failed")
            print(f"Error: {results.get('message')}")

        # Test with directory
        print("\n2. Testing directory generation...")
        results = generator.generate_from_directory(str(test_dir))

        if results.get('status') == 'success':
            print("[OK] Directory test passed")
            print(f"Endpoints found: {results.get('parsed_data', {}).get('total_endpoints', 0)}")
        else:
            print("[ERROR] Directory test failed")
            print(f"Error: {results.get('message')}")

        # Test recent files
        print("\n3. Testing recent files...")
        results = generator.get_recent_documentation(limit=3)
        if results.get('status') == 'success':
            print(f"[OK] Found {results.get('total_files', 0)} recent files")
        else:
            print("[ERROR] Recent files test failed")

        # Test directory validation
        print("\n4. Testing directory validation...")
        results = generator.validate_output_directory()
        if results.get('status') == 'success':
            if results.get('is_valid'):
                print("[OK] Output directory is valid")
            else:
                print(f"[WARNING] Output directory has issues: {results.get('issues')}")
        else:
            print("[ERROR] Directory validation test failed")

        print("\n" + "="*50)
        print("Skill test completed!")

    except Exception as e:
        print(f"[ERROR] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup test files
        if test_file.exists():
            test_file.unlink()
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
    test_skill_simple()