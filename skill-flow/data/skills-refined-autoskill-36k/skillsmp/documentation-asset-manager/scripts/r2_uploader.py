#!/usr/bin/env python3
"""
Upload files to Cloudflare R2 storage using Cloudflare API
Auto-detects credentials from parent directory or environment variable
"""

import json
import os
import requests
import sys
from pathlib import Path

class R2Uploader:
    def __init__(self, credentials_path=None):
        """Initialize R2 uploader with Cloudflare credentials

        Args:
            credentials_path: Path to credentials JSON. If None, auto-detects from:
                1. Script parent directory (../cloudflare_credentials.json)
                2. Environment variable CLOUDFLARE_CREDENTIALS
        """
        # Auto-detect credentials path if not provided
        if not credentials_path:
            script_dir = Path(__file__).parent
            credentials_path = script_dir.parent.parent.parent / 'cloudflare_credentials.json'
            # Fallback to environment variable
            if not credentials_path.exists():
                credentials_path = os.environ.get('CLOUDFLARE_CREDENTIALS', credentials_path)

        creds_path = Path(credentials_path)

        if not creds_path.exists():
            raise FileNotFoundError(f"Credentials not found: {creds_path}")

        with open(creds_path) as f:
            creds = json.load(f)

        self.account_id = creds['account_id']
        # Use R2-specific token if available, otherwise fall back to general API token
        self.api_token = creds.get('r2_api_token') or creds['api_token']
        self.bucket_name = 'screenshots'
        self.base_url = f'https://api.cloudflare.com/client/v4/accounts/{self.account_id}/r2/buckets/{self.bucket_name}/objects'

    def upload_file(self, local_path, r2_key):
        """
        Upload file to R2

        Args:
            local_path: Path to local file
            r2_key: Key (path) in R2 bucket

        Returns:
            dict with success status and public URL
        """
        local_path = Path(local_path)

        if not local_path.exists():
            return {
                'success': False,
                'error': f'File not found: {local_path}'
            }

        try:
            # Read file
            with open(local_path, 'rb') as f:
                file_data = f.read()

            # Determine content type
            content_type = self._get_content_type(local_path.suffix)

            # Upload to R2 via Cloudflare API
            url = f'{self.base_url}/{r2_key}'

            headers = {
                'Authorization': f'Bearer {self.api_token}',
                'Content-Type': content_type
            }

            response = requests.put(url, data=file_data, headers=headers, timeout=60)

            if response.status_code in [200, 201]:
                public_url = f'https://screenshots.tallyfy.com/{r2_key}'
                size_kb = len(file_data) / 1024

                return {
                    'success': True,
                    'url': public_url,
                    'key': r2_key,
                    'size': f'{size_kb:.1f}KB',
                    'size_bytes': len(file_data),
                    'content_type': content_type,
                    'message': f'Uploaded {local_path.name} to {r2_key}'
                }
            else:
                return {
                    'success': False,
                    'error': f'Upload failed: {response.status_code} - {response.text}',
                    'status_code': response.status_code
                }

        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Upload error: {str(e)}'
            }

    def delete_file(self, r2_key):
        """Delete file from R2"""
        try:
            url = f'{self.base_url}/{r2_key}'

            headers = {
                'Authorization': f'Bearer {self.api_token}'
            }

            response = requests.delete(url, headers=headers, timeout=30)

            if response.status_code in [200, 204]:
                return {
                    'success': True,
                    'message': f'Deleted {r2_key} from R2'
                }
            else:
                return {
                    'success': False,
                    'error': f'Delete failed: {response.status_code} - {response.text}'
                }

        except Exception as e:
            return {
                'success': False,
                'error': f'Delete error: {str(e)}'
            }

    def file_exists(self, r2_key):
        """Check if file exists in R2"""
        try:
            url = f'{self.base_url}/{r2_key}'

            headers = {
                'Authorization': f'Bearer {self.api_token}'
            }

            response = requests.head(url, headers=headers, timeout=10)
            return response.status_code == 200

        except:
            return False

    def _get_content_type(self, extension):
        """Get content type from file extension"""
        ext = extension.lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml',
            '.pdf': 'application/pdf',
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.json': 'application/json',
            '.txt': 'text/plain',
            '.md': 'text/markdown'
        }
        return content_types.get(ext, 'application/octet-stream')


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Upload files to Cloudflare R2')
    parser.add_argument('--file', required=True, help='Local file path')
    parser.add_argument('--key', required=True, help='R2 key (path in bucket)')
    parser.add_argument('--credentials',
                       help='Path to Cloudflare credentials JSON (default: auto-detect)')
    parser.add_argument('--output', help='Output JSON file for result')
    parser.add_argument('--delete', action='store_true', help='Delete file instead of upload')

    args = parser.parse_args()

    try:
        uploader = R2Uploader(args.credentials)

        if args.delete:
            result = uploader.delete_file(args.key)
        else:
            result = uploader.upload_file(args.file, args.key)

        print(json.dumps(result, indent=2))

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(result, indent=2))

        sys.exit(0 if result['success'] else 1)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e)
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
