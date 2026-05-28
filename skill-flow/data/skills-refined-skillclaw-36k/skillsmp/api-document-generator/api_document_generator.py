"""
Main API Documentation Generator Module
Orchestrates the parsing, generation, and file handling for API documentation.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
import sys
from pathlib import Path

# Import local modules
from api_parser import APIParser
from openapi_generator import OpenAPIGenerator
from file_handler import FileHandler


class APIDocumentGenerator:
    """Main class for generating API documentation."""

    def __init__(self, base_output_dir: str = ".claude/api_doc"):
        """
        Initialize the API document generator.

        Args:
            base_output_dir: Base directory for output files
        """
        self.parser = APIParser()
        self.generator = OpenAPIGenerator()
        self.file_handler = FileHandler(base_output_dir)
        self.results = {}

    def generate_from_file(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate documentation from a single file.

        Args:
            file_path: Path to the file to parse
            options: Generation options

        Returns:
            Dictionary with generation results
        """
        if options is None:
            options = {}

        start_time = datetime.now()

        try:
            # Parse the file
            parsed_data = self.parser.parse_file(file_path)

            # Validate parsed data
            warnings = self.parser.validate_parsed_data(parsed_data)

            # Generate OpenAPI specification
            openapi_spec = self.generator.generate_openapi_spec(parsed_data)

            # Generate markdown documentation
            markdown_content = self.generator.generate_markdown(parsed_data, openapi_spec)

            # Save documentation files
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Save markdown
            md_filename = f"api_documentation_{timestamp}.md"
            md_path = self.file_handler.save_documentation(markdown_content, md_filename)

            # Save OpenAPI spec (optional)
            json_path = None
            if options.get('save_openapi_spec', True):
                json_filename = f"openapi_spec_{timestamp}.json"
                json_path = self.generator.save_openapi_spec(openapi_spec,
                                                           str(self.file_handler.base_output_dir / json_filename))

            # Cleanup old files (optional)
            deleted_files = []
            if options.get('cleanup_old_files', True):
                max_files = options.get('max_files_to_keep', 10)
                deleted_files = self.file_handler.cleanup_old_files(max_files)

            processing_time = (datetime.now() - start_time).total_seconds()

            # Prepare results
            self.results = {
                'status': 'success',
                'message': 'API documentation generated successfully',
                'generated_files': [
                    {
                        'path': md_path,
                        'type': 'markdown',
                        'size_bytes': Path(md_path).stat().st_size if Path(md_path).exists() else 0
                    }
                ],
                'parsed_data': {
                    'total_endpoints': len(parsed_data.get('endpoints', [])),
                    'total_schemas': len(parsed_data.get('schemas', {})),
                    'files_processed': 1,
                    'validation_warnings': warnings
                },
                'statistics': {
                    'processing_time_seconds': processing_time,
                    'file_processed': file_path
                },
                'output_directory': str(self.file_handler.base_output_dir),
                'timestamp': datetime.now().isoformat(),
                'deleted_files': deleted_files
            }

            if json_path:
                self.results['generated_files'].append({
                    'path': json_path,
                    'type': 'json',
                    'size_bytes': Path(json_path).stat().st_size if Path(json_path).exists() else 0
                })

        except Exception as e:
            self.results = {
                'status': 'error',
                'message': f'Error generating documentation: {str(e)}',
                'error_details': str(e),
                'timestamp': datetime.now().isoformat()
            }

        return self.results

    def generate_from_directory(self, directory_path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate documentation from all files in a directory.

        Args:
            directory_path: Path to the directory to parse
            options: Generation options

        Returns:
            Dictionary with generation results
        """
        if options is None:
            options = {}

        start_time = datetime.now()

        try:
            # Parse the directory
            parsed_data = self.parser.parse_directory(directory_path)

            # Validate parsed data
            warnings = self.parser.validate_parsed_data(parsed_data)

            # Generate OpenAPI specification
            openapi_spec = self.generator.generate_openapi_spec(parsed_data)

            # Generate markdown documentation
            markdown_content = self.generator.generate_markdown(parsed_data, openapi_spec)

            # Save documentation files
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Save markdown
            md_filename = f"api_documentation_{timestamp}.md"
            md_path = self.file_handler.save_documentation(markdown_content, md_filename)

            # Save OpenAPI spec (optional)
            json_path = None
            if options.get('save_openapi_spec', True):
                json_filename = f"openapi_spec_{timestamp}.json"
                json_path = self.generator.save_openapi_spec(openapi_spec,
                                                           str(self.file_handler.base_output_dir / json_filename))

            # Cleanup old files (optional)
            deleted_files = []
            if options.get('cleanup_old_files', True):
                max_files = options.get('max_files_to_keep', 10)
                deleted_files = self.file_handler.cleanup_old_files(max_files)

            processing_time = (datetime.now() - start_time).total_seconds()

            # Count endpoints by method
            endpoints_by_method = {}
            for endpoint in parsed_data.get('endpoints', []):
                method = endpoint.get('method', 'UNKNOWN')
                endpoints_by_method[method] = endpoints_by_method.get(method, 0) + 1

            # Get unique file types
            file_types = set()
            for file_info in parsed_data.get('files_processed', []):
                if file_info.get('parsed_successfully'):
                    file_path = Path(file_info['file'])
                    file_types.add(file_path.suffix.lower())

            # Prepare results
            self.results = {
                'status': 'success',
                'message': 'API documentation generated successfully',
                'generated_files': [
                    {
                        'path': md_path,
                        'type': 'markdown',
                        'size_bytes': Path(md_path).stat().st_size if Path(md_path).exists() else 0
                    }
                ],
                'parsed_data': {
                    'total_endpoints': len(parsed_data.get('endpoints', [])),
                    'total_schemas': len(parsed_data.get('schemas', {})),
                    'files_processed': len([f for f in parsed_data.get('files_processed', [])
                                          if f.get('parsed_successfully')]),
                    'files_failed': len([f for f in parsed_data.get('files_processed', [])
                                       if not f.get('parsed_successfully')]),
                    'validation_warnings': warnings
                },
                'statistics': {
                    'processing_time_seconds': processing_time,
                    'endpoints_by_method': endpoints_by_method,
                    'file_types_processed': list(file_types),
                    'directory_processed': directory_path
                },
                'output_directory': str(self.file_handler.base_output_dir),
                'timestamp': datetime.now().isoformat(),
                'deleted_files': deleted_files
            }

            if json_path:
                self.results['generated_files'].append({
                    'path': json_path,
                    'type': 'json',
                    'size_bytes': Path(json_path).stat().st_size if Path(json_path).exists() else 0
                })

        except Exception as e:
            self.results = {
                'status': 'error',
                'message': f'Error generating documentation: {str(e)}',
                'error_details': str(e),
                'timestamp': datetime.now().isoformat()
            }

        return self.results

    def get_recent_documentation(self, limit: int = 5) -> Dict[str, Any]:
        """
        Get information about recent documentation files.

        Args:
            limit: Maximum number of files to return

        Returns:
            Dictionary with recent files information
        """
        try:
            recent_files = self.file_handler.get_recent_documentation_files(limit)

            return {
                'status': 'success',
                'recent_files': recent_files,
                'total_files': len(recent_files),
                'output_directory': str(self.file_handler.base_output_dir),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error getting recent documentation: {str(e)}',
                'error_details': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def validate_output_directory(self) -> Dict[str, Any]:
        """
        Validate the output directory.

        Returns:
            Dictionary with validation results
        """
        try:
            is_valid, issues = self.file_handler.validate_output_directory()

            return {
                'status': 'success',
                'is_valid': is_valid,
                'issues': issues,
                'output_directory': str(self.file_handler.base_output_dir),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error validating directory: {str(e)}',
                'error_details': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def print_results(self, results: Optional[Dict[str, Any]] = None):
        """
        Print generation results in a readable format.

        Args:
            results: Results to print (uses self.results if None)
        """
        if results is None:
            results = self.results

        if results.get('status') == 'success':
            print(f"✅ {results['message']}")
            print(f"📁 Output directory: {results['output_directory']}")
            print(f"⏰ Generated: {results['timestamp']}")

            if 'generated_files' in results:
                print("\n📄 Generated files:")
                for file_info in results['generated_files']:
                    size = file_info.get('size_human',
                                       f"{file_info.get('size_bytes', 0) / 1024:.1f} KB")
                    print(f"  • {file_info['path']} ({size})")

            if 'parsed_data' in results:
                print(f"\n📊 Statistics:")
                print(f"  • Endpoints: {results['parsed_data'].get('total_endpoints', 0)}")
                print(f"  • Schemas: {results['parsed_data'].get('total_schemas', 0)}")
                print(f"  • Files processed: {results['parsed_data'].get('files_processed', 0)}")

            if 'statistics' in results:
                print(f"  • Processing time: {results['statistics'].get('processing_time_seconds', 0):.2f}s")

            if results.get('deleted_files'):
                print(f"\n🗑️  Cleaned up {len(results['deleted_files'])} old files")

        else:
            print(f"❌ {results.get('message', 'Unknown error')}")
            if 'error_details' in results:
                print(f"   Details: {results['error_details']}")


def main():
    """Command-line interface for the API documentation generator."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate API documentation from code files')
    parser.add_argument('path', help='Path to file or directory to parse')
    parser.add_argument('--output-dir', default='.claude/api_doc',
                       help='Output directory for documentation')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown',
                       help='Output format')
    parser.add_argument('--include-examples', action='store_true', default=True,
                       help='Include example requests/responses')
    parser.add_argument('--no-cleanup', action='store_true',
                       help='Do not cleanup old files')
    parser.add_argument('--max-files', type=int, default=10,
                       help='Maximum number of files to keep')
    parser.add_argument('--recent', action='store_true',
                       help='Show recent documentation files')
    parser.add_argument('--validate', action='store_true',
                       help='Validate output directory')

    args = parser.parse_args()

    generator = APIDocumentGenerator(args.output_dir)

    if args.recent:
        results = generator.get_recent_documentation()
        generator.print_results(results)
        return

    if args.validate:
        results = generator.validate_output_directory()
        generator.print_results(results)
        return

    path = Path(args.path)
    options = {
        'save_openapi_spec': args.format == 'json',
        'include_examples': args.include_examples,
        'cleanup_old_files': not args.no_cleanup,
        'max_files_to_keep': args.max_files
    }

    if path.is_file():
        results = generator.generate_from_file(str(path), options)
    elif path.is_dir():
        results = generator.generate_from_directory(str(path), options)
    else:
        print(f"❌ Path not found: {path}")
        return

    generator.print_results(results)


if __name__ == '__main__':
    main()