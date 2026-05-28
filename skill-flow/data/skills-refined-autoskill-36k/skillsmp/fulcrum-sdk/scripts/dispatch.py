#!/usr/bin/env python3
"""Validation script for Fulcrum dispatch system.

Emits 2-3 test dispatches to verify the dispatch client is working correctly.
Useful for testing environment setup and dispatch connectivity.

Usage:
    # Set required environment variables first
    export FULCRUM_DISPATCH_URL="http://localhost:8000/dispatch"
    export FULCRUM_DISPATCH_TOKEN="test-token"
    export FULCRUM_TICKET_UUID="test-ticket-uuid"
    export FULCRUM_RUN_UUID="test-run-uuid"

    # Run the script
    uv run skills/fulcrum-sdk/scripts/dispatch.py
"""

from fulcrum_sdk._internal.dispatch import get_dispatch_client


def main() -> None:
    """Run dispatch validation tests."""
    dispatch = get_dispatch_client()

    print("Fulcrum Dispatch Validation")
    print("=" * 40)

    if not dispatch.enabled:
        print("ERROR: Dispatch client is not enabled.")
        print("\nRequired environment variables:")
        print("  - FULCRUM_DISPATCH_URL")
        print("  - FULCRUM_DISPATCH_TOKEN")
        print("  - FULCRUM_TICKET_UUID")
        print("  - FULCRUM_RUN_UUID")
        print("\nSet these variables and try again.")
        return

    print("Client enabled: YES")
    print()

    # Test 1: Simple text dispatch
    print("Test 1: dispatch_text")
    result = dispatch.dispatch_text("Dispatch validation started")
    print(f"  Result: {'SUCCESS' if result else 'FAILED'}")

    # Test 2: API call dispatch
    print("Test 2: dispatch_api_call")
    result = dispatch.dispatch_api_call(
        "Validation API call",
        service="fulcrum-sdk",
        operation="validate",
        test_mode=True,
    )
    print(f"  Result: {'SUCCESS' if result else 'FAILED'}")

    # Test 3: External ref dispatch
    print("Test 3: dispatch_external_ref")
    result = dispatch.dispatch_external_ref(
        "Validation external reference",
        provider="fulcrum-sdk",
        ref_type="validation",
        ref_id="test-ref-001",
    )
    print(f"  Result: {'SUCCESS' if result else 'FAILED'}")

    print()
    print("Validation complete.")


if __name__ == "__main__":
    main()
