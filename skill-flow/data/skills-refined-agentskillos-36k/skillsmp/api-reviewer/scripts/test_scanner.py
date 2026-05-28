#!/usr/bin/env python3
"""
Simple test for the scan_api_endpoints.py script

Tests that the script can:
1. Find API endpoints with @frappe.whitelist decorator
2. Detect security patterns
3. Generate valid YAML output
"""

import sys
import subprocess
import yaml
from pathlib import Path

def run_test():
    """Run basic tests on the scanner script"""
    script_dir = Path(__file__).parent
    scanner = script_dir / "scan_api_endpoints.py"
    test_output = "/tmp/test-scan-output.yaml"
    
    # Test 1: Run scanner on tweaks directory
    print("Test 1: Scanning tweaks directory...")
    result = subprocess.run(
        [sys.executable, str(scanner), "--path", "tweaks", "--output", test_output],
        cwd=script_dir.parent.parent.parent.parent,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Test 1 FAILED: Scanner returned error code {result.returncode}")
        print(result.stderr)
        return False
    
    print("✓ Scanner ran successfully")
    
    # Test 2: Validate YAML output exists and is valid
    print("\nTest 2: Validating YAML output...")
    output_path = Path(test_output)
    if not output_path.exists():
        print("❌ Test 2 FAILED: Output file not created")
        return False
    
    print("✓ Output file created")
    
    # Test 3: Parse YAML and check structure
    print("\nTest 3: Checking YAML structure...")
    with open(output_path) as f:
        data = yaml.safe_load(f)
    
    if "scan_info" not in data:
        print("❌ Test 3 FAILED: Missing scan_info")
        return False
    
    if "endpoints" not in data:
        print("❌ Test 3 FAILED: Missing endpoints")
        return False
    
    print(f"✓ Found {data['scan_info']['total_endpoints']} endpoints")
    
    # Test 4: Check that at least some endpoints were found
    print("\nTest 4: Checking endpoint count...")
    if data['scan_info']['total_endpoints'] == 0:
        print("❌ Test 4 FAILED: No endpoints found")
        return False
    
    if len(data['endpoints']) != data['scan_info']['total_endpoints']:
        print("❌ Test 4 FAILED: Endpoint count mismatch")
        return False
    
    print(f"✓ Endpoint count matches: {len(data['endpoints'])}")
    
    # Test 5: Check endpoint structure
    print("\nTest 5: Checking endpoint structure...")
    required_fields = ['function', 'file', 'line', 'arguments', 'security_checks', 'reviewed']
    
    first_endpoint = data['endpoints'][0]
    for field in required_fields:
        if field not in first_endpoint:
            print(f"❌ Test 5 FAILED: Missing field '{field}' in endpoint")
            return False
    
    print("✓ Endpoint structure is valid")
    
    # Test 6: Check security checks structure
    print("\nTest 6: Checking security checks...")
    security_checks = first_endpoint['security_checks']
    required_checks = [
        'has_frappe_only_for',
        'has_frappe_get_list',
        'has_frappe_has_permission',
        'has_permission_check'
    ]
    
    for check in required_checks:
        if check not in security_checks:
            print(f"❌ Test 6 FAILED: Missing security check '{check}'")
            return False
    
    print("✓ Security checks structure is valid")
    
    # Test 7: Verify at least one endpoint has a security check
    print("\nTest 7: Verifying security detection...")
    found_security = False
    for endpoint in data['endpoints']:
        checks = endpoint['security_checks']
        if any(checks.values()):
            found_security = True
            print(f"✓ Found security pattern in {endpoint['function']}")
            break
    
    if not found_security:
        print("⚠ Warning: No security patterns detected (might be normal)")
    
    print("\n" + "="*50)
    print("✅ All tests passed!")
    print("="*50)
    return True

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
