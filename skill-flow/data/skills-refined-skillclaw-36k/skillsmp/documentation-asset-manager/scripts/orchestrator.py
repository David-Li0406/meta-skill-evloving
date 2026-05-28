#!/usr/bin/env python3
"""
Complete workflow orchestrator for documentation asset management
Combines upload, captioning, and inventory management in one command
"""

import json
import os
import sys
import time
from pathlib import Path
import hashlib

# Import other modules
from r2_uploader import R2Uploader
from image_captioner import ImageCaptioner
from asset_inventory import AssetInventory


class AssetManagerOrchestrator:
    def __init__(self, credentials_path=None, inventory_path=None, anthropic_key=None):
        """Initialize orchestrator with all components

        Paths can be provided explicitly or will be auto-detected:
        - credentials_path: Defaults to ../cloudflare_credentials.json (relative to script)
        - inventory_path: Defaults to ../documentation/documentation_assets.csv (relative to script)
        """
        # Auto-detect credentials path if not provided
        if not credentials_path:
            script_dir = Path(__file__).parent
            # Look in parent directory (GitHub root)
            credentials_path = script_dir.parent.parent.parent / 'cloudflare_credentials.json'
            # Fallback to environment variable
            if not credentials_path.exists():
                credentials_path = os.environ.get('CLOUDFLARE_CREDENTIALS', credentials_path)

        # Auto-detect inventory path if not provided
        if not inventory_path:
            script_dir = Path(__file__).parent
            # Look in sibling directory (GitHub/documentation/)
            inventory_path = script_dir.parent.parent.parent / 'documentation' / 'documentation_assets.csv'
            # Fallback to environment variable
            if not inventory_path.exists():
                inventory_path = os.environ.get('ASSET_INVENTORY_CSV', inventory_path)

        self.uploader = R2Uploader(credentials_path)
        self.inventory = AssetInventory(inventory_path)

        # Captioner is optional (for uploads without captions)
        # ImageCaptioner now uses Claude Code native - no API key needed
        try:
            self.captioner = ImageCaptioner()
            self.captions_enabled = True
        except Exception:
            self.captioner = None
            self.captions_enabled = False

    def calculate_checksum(self, file_path):
        """Calculate SHA256 checksum of file"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def get_file_info(self, file_path):
        """Get file metadata"""
        file_path = Path(file_path)
        stat = file_path.stat()

        # Get file size in human-readable format
        size_bytes = stat.st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                size_human = f"{size_bytes:.1f}{unit}"
                break
            size_bytes /= 1024
        else:
            size_human = f"{size_bytes:.1f}TB"

        # Get image dimensions if image
        dimensions = 'N/A'
        if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            try:
                from PIL import Image
                img = Image.open(file_path)
                dimensions = f"{img.width}x{img.height}"
            except:
                pass

        return {
            'size_bytes': stat.st_size,
            'size_human': size_human,
            'dimensions': dimensions,
            'file_type': file_path.suffix.lower()
        }

    def process_asset(self, local_path, r2_key=None, article_ids=None,
                     skip_captions=False, skip_inventory=False):
        """
        Complete asset processing workflow

        Args:
            local_path: Path to local file
            r2_key: R2 key (default: auto-generate from filename)
            article_ids: Comma-separated article IDs or list
            skip_captions: Skip AI caption generation
            skip_inventory: Skip inventory update

        Returns:
            dict with complete results
        """
        local_path = Path(local_path)

        if not local_path.exists():
            return {
                'success': False,
                'error': f'File not found: {local_path}',
                'stage': 'validation'
            }

        # Auto-generate R2 key if not provided
        if not r2_key:
            r2_key = f"tallyfy/docs/{local_path.name}"

        print(f"🚀 Processing: {local_path.name}")
        print(f"   R2 Key: {r2_key}")

        results = {
            'filename': local_path.name,
            'local_path': str(local_path),
            'r2_key': r2_key,
            'stages': {}
        }

        # Get file info
        file_info = self.get_file_info(local_path)
        results.update(file_info)

        # Stage 1: Upload to R2
        print(f"\n📤 Stage 1: Uploading to R2...")
        upload_result = self.uploader.upload_file(str(local_path), r2_key)
        results['stages']['upload'] = upload_result

        if not upload_result['success']:
            results['success'] = False
            results['error'] = upload_result['error']
            results['stage'] = 'upload'
            return results

        results['production_url'] = upload_result['url']
        print(f"   ✅ Uploaded: {upload_result['url']}")

        # Stage 2: Generate AI Captions (if enabled)
        if not skip_captions and self.captions_enabled:
            is_image = local_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']

            if is_image:
                print(f"\n🤖 Stage 2: Generating AI captions...")
                caption_result = self.captioner.generate_all_captions(upload_result['url'], is_url=True)
                results['stages']['captions'] = caption_result

                if caption_result['success']:
                    results['captions'] = caption_result['captions']
                    print(f"   ✅ Alt text: {caption_result['captions']['alt_text'][:60]}...")
                    print(f"   ✅ Descriptive: {caption_result['captions']['descriptive'][:60]}...")
                    print(f"   ✅ SEO: {caption_result['captions']['seo'][:60]}...")
                else:
                    print(f"   ⚠️ Caption generation failed (continuing anyway)")
                    results['captions'] = caption_result['captions']

                # Small delay to avoid rate limits
                time.sleep(1)
            else:
                print(f"\n⏭️  Stage 2: Skipping captions (non-image file)")
                results['captions'] = {}
        else:
            if skip_captions:
                print(f"\n⏭️  Stage 2: Skipping captions (--skip-captions flag)")
            else:
                print(f"\n⏭️  Stage 2: Skipping captions (Anthropic API key not configured)")
            results['captions'] = {}

        # Stage 3: Update Inventory
        if not skip_inventory:
            print(f"\n📋 Stage 3: Updating inventory...")

            # Parse article IDs
            if isinstance(article_ids, str):
                article_ids_list = [aid.strip() for aid in article_ids.split(',') if aid.strip()]
            elif isinstance(article_ids, list):
                article_ids_list = article_ids
            else:
                article_ids_list = []

            # Check if asset already exists in inventory
            existing = self.inventory.find_asset(r2_key=r2_key)

            inventory_data = {
                'filename': local_path.name,
                'r2_key': r2_key,
                'production_url': upload_result['url'],
                'source_type': 'native',
                'file_type': file_info['file_type'],
                'file_size': file_info['size_human'],
                'file_size_bytes': file_info['size_bytes'],
                'url_exists': True,
                'article_ids': ','.join(article_ids_list),
                'article_count': len(article_ids_list),
                'last_modified': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'etag': self.calculate_checksum(local_path),
                'ai_caption_alt': results['captions'].get('alt_text', ''),
                'ai_caption_descriptive': results['captions'].get('descriptive', ''),
                'ai_caption_seo': results['captions'].get('seo', ''),
                'needs_caption': 'yes' if (file_info['file_type'] in ['.jpg', '.jpeg', '.png', '.gif', '.webp'] and not results['captions'].get('alt_text')) else 'no'
            }

            if existing:
                # Update existing record
                self.inventory.update_asset(r2_key, inventory_data)
                print(f"   ✅ Updated existing inventory record")
                results['stages']['inventory'] = {'action': 'updated', 'success': True}
            else:
                # Add new record
                self.inventory.add_asset(inventory_data)
                print(f"   ✅ Added to inventory")
                results['stages']['inventory'] = {'action': 'added', 'success': True}
        else:
            print(f"\n⏭️  Stage 3: Skipping inventory (--skip-inventory flag)")

        results['success'] = True
        print(f"\n✅ Complete!")
        return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Complete asset management workflow')
    parser.add_argument('--file', required=True, help='Local file path')
    parser.add_argument('--key', help='R2 key (default: auto-generate)')
    parser.add_argument('--article-ids', help='Comma-separated article IDs')
    parser.add_argument('--skip-captions', action='store_true',
                       help='Skip AI caption generation')
    parser.add_argument('--skip-inventory', action='store_true',
                       help='Skip inventory update')
    parser.add_argument('--credentials',
                       help='Cloudflare credentials path (default: auto-detect from script location)')
    parser.add_argument('--inventory',
                       help='Inventory CSV path (default: auto-detect from script location)')
    parser.add_argument('--api-key', help='Anthropic API key')
    parser.add_argument('--output', help='Output JSON file for results')
    parser.add_argument('--batch-mode', action='store_true',
                       help='Batch mode (suppress some output)')

    args = parser.parse_args()

    try:
        orchestrator = AssetManagerOrchestrator(
            credentials_path=args.credentials,
            inventory_path=args.inventory,
            anthropic_key=args.api_key
        )

        result = orchestrator.process_asset(
            args.file,
            r2_key=args.key,
            article_ids=args.article_ids,
            skip_captions=args.skip_captions,
            skip_inventory=args.skip_inventory
        )

        if not args.batch_mode:
            print("\n" + "="*60)
            print("FINAL RESULT:")
            print(json.dumps(result, indent=2))

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(result, indent=2))

        sys.exit(0 if result['success'] else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
        sys.exit(130)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'stage': 'initialization'
        }
        print(json.dumps(error_result, indent=2))
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
