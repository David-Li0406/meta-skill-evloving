"""
API Parser Module
Parses interface/API information from code files to extract endpoint definitions,
parameters, responses, and other metadata for documentation generation.
"""

import os
import re
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import json
import yaml


class APIParser:
    """Main class for parsing API information from code files."""

    def __init__(self):
        """Initialize the API parser with default configurations."""
        self.supported_extensions = {'.py', '.js', '.ts', '.json', '.yaml', '.yml'}
        self.endpoints = []
        self.schemas = {}
        self.metadata = {
            'title': 'API Documentation',
            'description': 'Automatically generated API documentation',
            'version': '1.0.0'
        }

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a single file for API information.

        Args:
            file_path: Path to the file to parse

        Returns:
            Dictionary containing parsed API information
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = file_path.suffix.lower()

        if file_ext == '.py':
            return self._parse_python_file(file_path)
        elif file_ext in ['.js', '.ts']:
            return self._parse_javascript_file(file_path)
        elif file_ext == '.json':
            return self._parse_json_file(file_path)
        elif file_ext in ['.yaml', '.yml']:
            return self._parse_yaml_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    def parse_directory(self, directory_path: str) -> Dict[str, Any]:
        """
        Parse all supported files in a directory.

        Args:
            directory_path: Path to the directory to parse

        Returns:
            Dictionary containing aggregated API information from all files
        """
        directory_path = Path(directory_path)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        all_endpoints = []
        all_schemas = {}
        file_metadata = []

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.supported_extensions:
                    try:
                        parsed_data = self.parse_file(str(file_path))
                        if 'endpoints' in parsed_data:
                            all_endpoints.extend(parsed_data['endpoints'])
                        if 'schemas' in parsed_data:
                            all_schemas.update(parsed_data['schemas'])
                        file_metadata.append({
                            'file': str(file_path),
                            'parsed_successfully': True
                        })
                    except Exception as e:
                        file_metadata.append({
                            'file': str(file_path),
                            'parsed_successfully': False,
                            'error': str(e)
                        })

        return {
            'endpoints': all_endpoints,
            'schemas': all_schemas,
            'metadata': self.metadata,
            'files_processed': file_metadata,
            'total_endpoints': len(all_endpoints),
            'total_schemas': len(all_schemas)
        }

    def _parse_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse Python file for API definitions."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        endpoints = []
        schemas = {}

        # Look for FastAPI/Flask/Django patterns
        # FastAPI: @app.get("/endpoint")
        fastapi_pattern = r'@app\.(get|post|put|delete|patch|head|options|trace)\s*\(\s*["\']([^"\']+)["\']'
        for match in re.finditer(fastapi_pattern, content):
            method = match.group(1).upper()
            path = match.group(2)
            endpoints.append({
                'method': method,
                'path': path,
                'framework': 'fastapi',
                'file': str(file_path)
            })

        # Flask: @app.route("/endpoint", methods=["GET"])
        flask_pattern = r'@app\.route\s*\(\s*["\']([^"\']+)["\'][^)]*methods\s*=\s*\[([^\]]+)\]'
        for match in re.finditer(flask_pattern, content):
            path = match.group(1)
            methods = [m.strip().strip('"\'') for m in match.group(2).split(',')]
            for method in methods:
                endpoints.append({
                    'method': method.upper(),
                    'path': path,
                    'framework': 'flask',
                    'file': str(file_path)
                })

        # Django: path("endpoint/", view_function)
        django_pattern = r'path\s*\(\s*["\']([^"\']+)["\']'
        for match in re.finditer(django_pattern, content):
            path = match.group(1)
            endpoints.append({
                'method': 'GET',  # Default for Django
                'path': path,
                'framework': 'django',
                'file': str(file_path)
            })

        # Look for Pydantic models (schemas)
        pydantic_pattern = r'class\s+(\w+)\s*\(\s*BaseModel\s*\)'
        for match in re.finditer(pydantic_pattern, content):
            schema_name = match.group(1)
            schemas[schema_name] = {
                'name': schema_name,
                'type': 'pydantic',
                'file': str(file_path)
            }

        return {
            'endpoints': endpoints,
            'schemas': schemas,
            'metadata': {
                'language': 'python',
                'file': str(file_path)
            }
        }

    def _parse_javascript_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse JavaScript/TypeScript file for API definitions."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        endpoints = []
        schemas = {}

        # Express.js patterns
        # app.get("/endpoint", handler)
        express_pattern = r'(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
        for match in re.finditer(express_pattern, content):
            method = match.group(1).upper()
            path = match.group(2)
            endpoints.append({
                'method': method,
                'path': path,
                'framework': 'express',
                'file': str(file_path)
            })

        # TypeScript interfaces
        ts_interface_pattern = r'interface\s+(\w+)\s*{'
        for match in re.finditer(ts_interface_pattern, content):
            interface_name = match.group(1)
            schemas[interface_name] = {
                'name': interface_name,
                'type': 'typescript_interface',
                'file': str(file_path)
            }

        return {
            'endpoints': endpoints,
            'schemas': schemas,
            'metadata': {
                'language': 'javascript/typescript',
                'file': str(file_path)
            }
        }

    def _parse_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse JSON file (could be OpenAPI spec or similar)."""
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON file: {e}")

        endpoints = []
        schemas = {}

        # Check if it's an OpenAPI spec
        if 'openapi' in data or 'swagger' in data:
            # Parse OpenAPI specification
            if 'paths' in data:
                for path, methods in data['paths'].items():
                    for method, details in methods.items():
                        endpoints.append({
                            'method': method.upper(),
                            'path': path,
                            'description': details.get('description', ''),
                            'summary': details.get('summary', ''),
                            'operationId': details.get('operationId', ''),
                            'framework': 'openapi',
                            'file': str(file_path)
                        })

            if 'components' in data and 'schemas' in data['components']:
                for schema_name, schema_def in data['components']['schemas'].items():
                    schemas[schema_name] = {
                        'name': schema_name,
                        'definition': schema_def,
                        'type': 'openapi_schema',
                        'file': str(file_path)
                    }

        return {
            'endpoints': endpoints,
            'schemas': schemas,
            'metadata': {
                'format': 'json',
                'file': str(file_path),
                'is_openapi': 'openapi' in data or 'swagger' in data
            }
        }

    def _parse_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse YAML file (could be OpenAPI spec or similar)."""
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML file: {e}")

        endpoints = []
        schemas = {}

        # Check if it's an OpenAPI spec
        if data and ('openapi' in data or 'swagger' in data):
            # Parse OpenAPI specification
            if 'paths' in data:
                for path, methods in data['paths'].items():
                    for method, details in methods.items():
                        endpoints.append({
                            'method': method.upper(),
                            'path': path,
                            'description': details.get('description', ''),
                            'summary': details.get('summary', ''),
                            'operationId': details.get('operationId', ''),
                            'framework': 'openapi',
                            'file': str(file_path)
                        })

            if 'components' in data and 'schemas' in data['components']:
                for schema_name, schema_def in data['components']['schemas'].items():
                    schemas[schema_name] = {
                        'name': schema_name,
                        'definition': schema_def,
                        'type': 'openapi_schema',
                        'file': str(file_path)
                    }

        return {
            'endpoints': endpoints,
            'schemas': schemas,
            'metadata': {
                'format': 'yaml',
                'file': str(file_path),
                'is_openapi': data and ('openapi' in data or 'swagger' in data)
            }
        }

    def validate_parsed_data(self, parsed_data: Dict[str, Any]) -> List[str]:
        """
        Validate parsed API data for completeness and consistency.

        Args:
            parsed_data: Parsed API data to validate

        Returns:
            List of validation warnings/messages
        """
        warnings = []

        if 'endpoints' not in parsed_data:
            warnings.append("No endpoints found in parsed data")
        else:
            for endpoint in parsed_data['endpoints']:
                if 'method' not in endpoint:
                    warnings.append(f"Endpoint missing method: {endpoint.get('path', 'unknown')}")
                if 'path' not in endpoint:
                    warnings.append(f"Endpoint missing path: {endpoint.get('method', 'unknown')}")

        if 'schemas' not in parsed_data:
            warnings.append("No schemas found in parsed data")

        return warnings