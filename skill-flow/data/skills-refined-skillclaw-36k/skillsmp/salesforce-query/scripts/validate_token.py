#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Salesforce Bearer Token Validator
Simple validation of bearer tokens for Salesforce API access.
"""

import sys
import json
import requests

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def validate_token(instance_url, bearer_token):
    """
    Validate that a bearer token is valid and has API access

    Args:
        instance_url: Salesforce instance URL
        bearer_token: Bearer token (with or without 'Bearer ' prefix)

    Returns:
        Dictionary with validation result
    """
    print("[VALIDATE] Testing bearer token...")

    # Normalize token format
    if bearer_token.startswith(('Bearer ', 'OAuth ')):
        auth_header = bearer_token
    else:
        auth_header = f'Bearer {bearer_token}'

    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }

    try:
        # Test token with a lightweight API call
        response = requests.get(
            f"{instance_url}/services/data/v60.0/limits",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            limits = response.json()
            print("[OK] Token is valid!\n")
            return {
                'success': True,
                'message': 'Token is valid and has API access',
                'api_usage': {
                    'daily_api_requests_used': limits.get('DailyApiRequests', {}).get('Remaining'),
                    'daily_api_requests_limit': limits.get('DailyApiRequests', {}).get('Max')
                }
            }
        elif response.status_code == 401:
            print("[ERROR] Token is invalid or expired\n")
            return {
                'success': False,
                'error': 'Token is invalid or expired. Please provide a valid bearer token.',
                'error_code': 401
            }
        else:
            return {
                'success': False,
                'error': f'Unexpected response: {response.status_code} - {response.text}',
                'error_code': response.status_code
            }

    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timed out. Check your network connection and instance URL.'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Request failed: {str(e)}'
        }


def main():
    """CLI interface for token validation"""
    if len(sys.argv) < 3:
        print("Usage: python validate_token.py <instance_url> <bearer_token>")
        print("\nExample:")
        print("  python validate_token.py https://yourorg.my.salesforce.com 00D...")
        print("\nToken formats accepted:")
        print("  - Bearer xxx")
        print("  - OAuth xxx")
        print("  - xxx (plain token)")
        print("\nHow to get a bearer token:")
        print("  1. Session ID (Quick):")
        print("     - Developer Console → Execute Anonymous")
        print("     - Run: System.debug(UserInfo.getSessionId());")
        print("     - Copy session ID from logs")
        print("  2. OAuth Token (via external OAuth flow)")
        print("  3. Connected App (via Salesforce REST API OAuth)")
        sys.exit(1)

    instance_url = sys.argv[1].rstrip('/')
    bearer_token = sys.argv[2]

    result = validate_token(instance_url, bearer_token)

    # Output result as JSON
    print(json.dumps(result, indent=2))

    if not result['success']:
        sys.exit(1)


if __name__ == '__main__':
    main()
