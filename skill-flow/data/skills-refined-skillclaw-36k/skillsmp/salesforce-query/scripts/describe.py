#!/usr/bin/env python3
"""
Salesforce Object Describe Tool
Fetches metadata and field information for Salesforce objects.
"""

import sys
import json
import requests


def describe_object(instance_url, access_token, object_name):
    """
    Fetch object metadata using Salesforce REST API

    Args:
        instance_url: Salesforce instance URL
        access_token: OAuth access token
        object_name: Name of the Salesforce object (e.g., 'Account', 'Opportunity')

    Returns:
        Dictionary containing object metadata and field information
    """
    # Build API endpoint
    api_url = f"{instance_url}/services/data/v60.0/sobjects/{object_name}/describe"

    # Handle flexible token format (Bearer, OAuth, or plain token)
    auth_header = access_token if access_token.startswith(('Bearer ', 'OAuth ')) else f'Bearer {access_token}'

    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=30)

        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json()
            }
        elif response.status_code == 401:
            return {
                'success': False,
                'error': 'Authentication failed. Please re-authenticate.',
                'error_code': 401
            }
        elif response.status_code == 404:
            return {
                'success': False,
                'error': f"Object '{object_name}' not found. Check the object name.",
                'error_code': 404
            }
        else:
            return {
                'success': False,
                'error': f"API request failed: {response.status_code} - {response.text}",
                'error_code': response.status_code
            }

    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timed out. Please try again.'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Request failed: {str(e)}'
        }


def format_field_info(describe_data):
    """
    Extract and format useful field information from describe response

    Args:
        describe_data: Raw describe response from Salesforce API

    Returns:
        Formatted field information
    """
    fields_info = []

    for field in describe_data.get('fields', []):
        field_info = {
            'name': field.get('name'),
            'label': field.get('label'),
            'type': field.get('type'),
            'length': field.get('length'),
            'required': not field.get('nillable', True),
            'updateable': field.get('updateable', False),
            'createable': field.get('createable', False),
            'filterable': field.get('filterable', False),
            'sortable': field.get('sortable', False)
        }

        # Add relationship info if this is a reference field
        if field.get('type') == 'reference' and field.get('referenceTo'):
            field_info['referenceTo'] = field.get('referenceTo')
            field_info['relationshipName'] = field.get('relationshipName')

        # Add picklist values if applicable
        if field.get('type') in ['picklist', 'multipicklist']:
            field_info['picklistValues'] = [
                {'label': val.get('label'), 'value': val.get('value')}
                for val in field.get('picklistValues', [])
                if val.get('active', False)
            ]

        fields_info.append(field_info)

    return {
        'objectName': describe_data.get('name'),
        'label': describe_data.get('label'),
        'labelPlural': describe_data.get('labelPlural'),
        'queryable': describe_data.get('queryable', False),
        'searchable': describe_data.get('searchable', False),
        'totalFields': len(fields_info),
        'fields': fields_info
    }


def print_field_summary(formatted_info):
    """Print a human-readable summary of fields"""
    print(f"\n📋 Object: {formatted_info['label']} ({formatted_info['objectName']})")
    print(f"📊 Total Fields: {formatted_info['totalFields']}")
    print(f"🔍 Queryable: {'Yes' if formatted_info['queryable'] else 'No'}")
    print(f"\n{'='*80}\n")

    print(f"{'Field Name':<30} {'Type':<15} {'Label':<30}")
    print(f"{'-'*30} {'-'*15} {'-'*30}")

    for field in formatted_info['fields'][:50]:  # Show first 50 fields
        field_name = field['name']
        field_type = field['type']
        field_label = field['label']

        print(f"{field_name:<30} {field_type:<15} {field_label:<30}")

    if formatted_info['totalFields'] > 50:
        print(f"\n... and {formatted_info['totalFields'] - 50} more fields")

    print(f"\n{'='*80}\n")


def main():
    """CLI interface for describe tool"""
    if len(sys.argv) < 4:
        print("Usage: python describe.py <instance_url> <access_token> <object_name> [--verbose]")
        print("\nExample:")
        print("  python describe.py https://yourorg.my.salesforce.com YOUR_ACCESS_TOKEN Account")
        print("\nToken formats accepted:")
        print("  - Bearer xxx")
        print("  - OAuth xxx")
        print("  - xxx (plain token)")
        print("\nOptions:")
        print("  --verbose    Show detailed field information")
        sys.exit(1)

    instance_url = sys.argv[1].rstrip('/')
    access_token = sys.argv[2]
    object_name = sys.argv[3]
    verbose = '--verbose' in sys.argv

    # Fetch object metadata
    result = describe_object(instance_url, access_token, object_name)

    if result['success']:
        # Format the data
        formatted_info = format_field_info(result['data'])

        if verbose:
            # Print human-readable summary
            print_field_summary(formatted_info)

        # Always output JSON for programmatic use
        print(json.dumps(formatted_info, indent=2))
    else:
        # Output error as JSON
        print(json.dumps(result, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
