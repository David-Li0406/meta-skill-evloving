#!/usr/bin/env python3
"""
Salesforce SOQL Query Tool
Executes SOQL queries against Salesforce and returns results.
"""

import sys
import json
import requests


def execute_query(instance_url, access_token, soql_query):
    """
    Execute SOQL query using Salesforce REST API

    Args:
        instance_url: Salesforce instance URL
        access_token: OAuth access token
        soql_query: SOQL query string

    Returns:
        Dictionary containing query results or error information
    """
    # Build API URL without query parameter
    api_url = f"{instance_url}/services/data/v65.0/query/"

    # Fix Windows cmd escaping issue: remove backslashes before exclamation marks
    access_token = access_token.replace('\\!', '!')

    # Handle flexible token format (Bearer, OAuth, or plain token)
    auth_header = access_token if access_token.startswith(('Bearer ', 'OAuth ')) else f'Bearer {access_token}'

    headers = {
        'Authorization': auth_header
    }

    all_records = []
    first_request = True
    next_records_url = None

    try:
        while True:
            # First request uses params, subsequent requests use nextRecordsUrl
            if first_request:
                # Use params to pass the query - requests will handle encoding
                params = {'q': soql_query}
                response = requests.get(api_url, headers=headers, params=params, timeout=120)
                print(f"Request URL: {response.url}")  # Show actual encoded URL
                first_request = False
            elif next_records_url:
                # Pagination: use nextRecordsUrl directly
                response = requests.get(f"{instance_url}{next_records_url}", headers=headers, timeout=120)
            else:
                # No more pages to fetch
                break

            if response.status_code == 200:
                result = response.json()
                all_records.extend(result.get('records', []))

                # Check if there are more records
                if result.get('done', True):
                    break  # Exit loop when done
                else:
                    next_records_url = result.get('nextRecordsUrl')
            elif response.status_code == 401:
                print(f"API URL: {api_url}")
                print(f"Request URL: {response.url}")
                try:
                    error_details = response.json()
                except:
                    error_details = response.text
                return {
                    'success': False,
                    'error': 'Authentication failed. Please re-authenticate.',
                    'error_code': 401,
                    'details': error_details
                }
            elif response.status_code == 400:
                print(f"API URL: {api_url}")
                print(f"Request URL: {response.url}")
                error_data = response.json()
                error_message = error_data[0].get('message', 'Unknown error') if error_data else 'Bad request'
                return {
                    'success': False,
                    'error': f'SOQL syntax error: {error_message}',
                    'error_code': 400,
                    'details': error_data
                }
            else:
                print(f"API URL: {api_url}")
                print(f"Request URL: {response.url}")
                return {
                    'success': False,
                    'error': f'API request failed: {response.status_code} - {response.text}',
                    'error_code': response.status_code
                }

        # Add URL to each record (instance_url + "/" + Id)
        for record in all_records:
            if 'Id' in record:
                record['URL'] = f"{instance_url}/{record['Id']}"

        return {
            'success': True,
            'totalSize': len(all_records),
            'records': all_records
        }

    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Query timed out. Try simplifying your query or reducing the result set.'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Request failed: {str(e)}'
        }


def format_results(query_result):
    """
    Format query results for display

    Args:
        query_result: Raw query result from Salesforce API

    Returns:
        Formatted result dictionary
    """
    if not query_result['success']:
        return query_result

    records = query_result['records']

    # Remove Salesforce metadata from records
    cleaned_records = []
    for record in records:
        cleaned_record = {}
        for key, value in record.items():
            if key == 'attributes':
                continue

            # Handle nested relationship objects
            if isinstance(value, dict):
                if 'attributes' in value:
                    # This is a related object, flatten it
                    for nested_key, nested_value in value.items():
                        if nested_key != 'attributes':
                            cleaned_record[f"{key}.{nested_key}"] = nested_value
                else:
                    cleaned_record[key] = value
            else:
                cleaned_record[key] = value

        cleaned_records.append(cleaned_record)

    return {
        'success': True,
        'totalSize': query_result['totalSize'],
        'records': cleaned_records
    }


def print_table(records):
    """Print results as a formatted table"""
    if not records:
        print("\n📭 No records found.\n")
        return

    print(f"\n✅ Found {len(records)} record(s):\n")

    # Get all unique keys from all records
    all_keys = set()
    for record in records:
        all_keys.update(record.keys())

    headers = sorted(all_keys)

    # Calculate column widths
    col_widths = {}
    for header in headers:
        max_width = len(str(header))
        for record in records:
            value = record.get(header, '')
            max_width = max(max_width, len(str(value)))
        col_widths[header] = min(max_width, 50)  # Cap at 50 chars

    # Print header
    header_row = ' | '.join(h.ljust(col_widths[h]) for h in headers)
    print(header_row)
    print('-' * len(header_row))

    # Print rows
    for record in records:
        row_values = []
        for header in headers:
            value = record.get(header, '')
            value_str = str(value) if value is not None else ''

            # Truncate if too long
            if len(value_str) > col_widths[header]:
                value_str = value_str[:col_widths[header]-3] + '...'

            row_values.append(value_str.ljust(col_widths[header]))

        print(' | '.join(row_values))

    print()


def main():
    """CLI interface for query tool"""
    if len(sys.argv) < 4:
        print("Usage: python query.py <instance_url> <access_token> <soql_query> [--verbose]")
        print("\nExample:")
        print("  python query.py https://yourorg.my.salesforce.com YOUR_ACCESS_TOKEN \"SELECT Id, Name FROM Account LIMIT 10\"")
        print("\nToken formats accepted:")
        print("  - Bearer xxx")
        print("  - OAuth xxx")
        print("  - xxx (plain token)")
        print("\nOptions:")
        print("  --verbose    Show formatted table output")
        sys.exit(1)

    instance_url = sys.argv[1].rstrip('/')
    access_token = sys.argv[2]
    soql_query = sys.argv[3]
    verbose = '--verbose' in sys.argv

    # Execute query
    result = execute_query(instance_url, access_token, soql_query)

    if result['success']:
        # Format the results
        formatted_result = format_results(result)

        if verbose:
            # Print human-readable table
            print_table(formatted_result['records'])

        # Always output JSON for programmatic use
        print(json.dumps(formatted_result, indent=2))
    else:
        # Output error as JSON
        print(json.dumps(result, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
