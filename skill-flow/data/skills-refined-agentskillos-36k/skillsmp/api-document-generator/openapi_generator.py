"""
OpenAPI Generator Module
Generates OpenAPI-compliant documentation from parsed API information.
"""

import json
import yaml
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class OpenAPIGenerator:
    """Generates OpenAPI-compliant documentation."""

    def __init__(self):
        """Initialize the OpenAPI generator."""
        self.openapi_version = "3.0.3"
        self.default_info = {
            "title": "Generated API Documentation",
            "description": "Automatically generated from code files",
            "version": "1.0.0",
            "contact": {
                "name": "API Documentation Generator",
                "url": "https://github.com/anthropics/skills"
            }
        }

    def generate_openapi_spec(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate OpenAPI specification from parsed data.

        Args:
            parsed_data: Parsed API information

        Returns:
            OpenAPI specification as dictionary
        """
        openapi_spec = {
            "openapi": self.openapi_version,
            "info": self._get_info(parsed_data),
            "paths": self._generate_paths(parsed_data),
            "components": self._generate_components(parsed_data),
            "tags": self._generate_tags(parsed_data),
            "externalDocs": {
                "description": "OpenAPI Specification",
                "url": "https://swagger.io/specification/"
            }
        }

        return openapi_spec

    def generate_markdown(self, parsed_data: Dict[str, Any],
                         openapi_spec: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate markdown documentation from parsed data.

        Args:
            parsed_data: Parsed API information
            openapi_spec: Optional OpenAPI specification (generated if not provided)

        Returns:
            Markdown documentation string
        """
        if openapi_spec is None:
            openapi_spec = self.generate_openapi_spec(parsed_data)

        markdown = []

        # Header
        markdown.append(f"# {openapi_spec['info']['title']}")
        markdown.append("")
        markdown.append(f"**Version**: {openapi_spec['info']['version']}")
        markdown.append("")
        markdown.append(f"**Description**: {openapi_spec['info']['description']}")
        markdown.append("")
        markdown.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        markdown.append("")
        markdown.append("---")
        markdown.append("")

        # Table of Contents
        markdown.append("## Table of Contents")
        markdown.append("")
        markdown.append("- [Overview](#overview)")
        markdown.append("- [Endpoints](#endpoints)")
        if openapi_spec.get('components', {}).get('schemas'):
            markdown.append("- [Schemas](#schemas)")
        markdown.append("- [Authentication](#authentication)")
        markdown.append("- [Examples](#examples)")
        markdown.append("- [Error Codes](#error-codes)")
        markdown.append("")
        markdown.append("---")
        markdown.append("")

        # Overview
        markdown.append("## Overview")
        markdown.append("")
        markdown.append("This API documentation was automatically generated from source code.")
        markdown.append("")
        markdown.append(f"**OpenAPI Version**: {openapi_spec['openapi']}")
        markdown.append(f"**Base URL**: `https://api.example.com`")
        markdown.append("")
        markdown.append("### Authentication")
        markdown.append("")
        markdown.append("This API uses the following authentication methods:")
        markdown.append("- **API Key**: Include `X-API-Key` header")
        markdown.append("- **Bearer Token**: Include `Authorization: Bearer <token>` header")
        markdown.append("")
        markdown.append("---")
        markdown.append("")

        # Endpoints
        markdown.append("## Endpoints")
        markdown.append("")

        paths = openapi_spec.get('paths', {})
        for path, methods in sorted(paths.items()):
            markdown.append(f"### `{path}`")
            markdown.append("")

            for method, details in methods.items():
                markdown.append(f"#### {method.upper()}")
                markdown.append("")

                if 'summary' in details:
                    markdown.append(f"**Summary**: {details['summary']}")
                    markdown.append("")

                if 'description' in details:
                    markdown.append(f"**Description**: {details['description']}")
                    markdown.append("")

                # Parameters
                if 'parameters' in details and details['parameters']:
                    markdown.append("**Parameters**:")
                    markdown.append("")
                    markdown.append("| Name | In | Type | Required | Description |")
                    markdown.append("|------|----|------|----------|-------------|")
                    for param in details['parameters']:
                        markdown.append(f"| {param.get('name', '')} | {param.get('in', '')} | {param.get('schema', {}).get('type', '')} | {param.get('required', False)} | {param.get('description', '')} |")
                    markdown.append("")

                # Request Body
                if 'requestBody' in details:
                    markdown.append("**Request Body**:")
                    markdown.append("")
                    content = details['requestBody'].get('content', {})
                    for content_type, schema_info in content.items():
                        markdown.append(f"**Content-Type**: `{content_type}`")
                        if 'schema' in schema_info:
                            schema_ref = schema_info['schema'].get('$ref', '')
                            if schema_ref:
                                schema_name = schema_ref.split('/')[-1]
                                markdown.append(f"**Schema**: [{schema_name}](#{schema_name.lower()})")
                    markdown.append("")

                # Responses
                if 'responses' in details:
                    markdown.append("**Responses**:")
                    markdown.append("")
                    markdown.append("| Code | Description |")
                    markdown.append("|------|-------------|")
                    for code, response in details['responses'].items():
                        description = response.get('description', '')
                        markdown.append(f"| {code} | {description} |")
                    markdown.append("")

                markdown.append("---")
                markdown.append("")

        # Schemas
        components = openapi_spec.get('components', {})
        if 'schemas' in components and components['schemas']:
            markdown.append("## Schemas")
            markdown.append("")

            for schema_name, schema_def in sorted(components['schemas'].items()):
                markdown.append(f"### {schema_name}")
                markdown.append("")

                if 'type' in schema_def:
                    markdown.append(f"**Type**: `{schema_def['type']}`")
                    markdown.append("")

                if 'properties' in schema_def:
                    markdown.append("**Properties**:")
                    markdown.append("")
                    markdown.append("| Property | Type | Description |")
                    markdown.append("|----------|------|-------------|")
                    for prop_name, prop_def in schema_def['properties'].items():
                        prop_type = prop_def.get('type', '')
                        description = prop_def.get('description', '')
                        markdown.append(f"| {prop_name} | {prop_type} | {description} |")
                    markdown.append("")

                if 'required' in schema_def and schema_def['required']:
                    markdown.append(f"**Required**: {', '.join(schema_def['required'])}")
                    markdown.append("")

                markdown.append("---")
                markdown.append("")

        # Examples
        markdown.append("## Examples")
        markdown.append("")

        # Example requests
        markdown.append("### Example Requests")
        markdown.append("")

        example_endpoints = list(paths.items())[:3]  # Show first 3 endpoints as examples
        for path, methods in example_endpoints:
            for method in methods:
                if method.upper() in ['GET', 'POST']:
                    markdown.append(f"#### {method.upper()} {path}")
                    markdown.append("")
                    markdown.append("```bash")
                    if method.upper() == 'GET':
                        markdown.append(f"curl -X GET https://api.example.com{path} \\")
                        markdown.append("  -H 'X-API-Key: your-api-key'")
                    else:  # POST
                        markdown.append(f"curl -X POST https://api.example.com{path} \\")
                        markdown.append("  -H 'Content-Type: application/json' \\")
                        markdown.append("  -H 'X-API-Key: your-api-key' \\")
                        markdown.append("  -d '{\"example\": \"data\"}'")
                    markdown.append("```")
                    markdown.append("")

        # Error Codes
        markdown.append("## Error Codes")
        markdown.append("")

        error_codes = {
            "400": "Bad Request - The request was malformed or invalid",
            "401": "Unauthorized - Authentication failed or not provided",
            "403": "Forbidden - Authenticated but not authorized",
            "404": "Not Found - Resource not found",
            "429": "Too Many Requests - Rate limit exceeded",
            "500": "Internal Server Error - Server error",
            "502": "Bad Gateway - Upstream server error",
            "503": "Service Unavailable - Service temporarily unavailable"
        }

        markdown.append("| Code | Description |")
        markdown.append("|------|-------------|")
        for code, description in error_codes.items():
            markdown.append(f"| {code} | {description} |")
        markdown.append("")

        # Footer
        markdown.append("---")
        markdown.append("")
        markdown.append("*This documentation was automatically generated by the API Documentation Generator skill.*")
        markdown.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return "\n".join(markdown)

    def _get_info(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get OpenAPI info section."""
        info = self.default_info.copy()

        if 'metadata' in parsed_data:
            metadata = parsed_data['metadata']
            if 'title' in metadata:
                info['title'] = metadata['title']
            if 'description' in metadata:
                info['description'] = metadata['description']
            if 'version' in metadata:
                info['version'] = metadata['version']

        return info

    def _generate_paths(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate OpenAPI paths section."""
        paths = {}

        if 'endpoints' in parsed_data:
            for endpoint in parsed_data['endpoints']:
                path = endpoint.get('path', '')
                method = endpoint.get('method', 'get').lower()

                if path not in paths:
                    paths[path] = {}

                paths[path][method] = {
                    "summary": endpoint.get('summary', f"{method.upper()} {path}"),
                    "description": endpoint.get('description', ''),
                    "operationId": endpoint.get('operationId', f"{method}_{path.replace('/', '_').strip('_')}"),
                    "tags": self._get_tags_for_endpoint(endpoint),
                    "responses": {
                        "200": {
                            "description": "Successful operation"
                        },
                        "400": {
                            "description": "Bad request"
                        },
                        "401": {
                            "description": "Unauthorized"
                        },
                        "500": {
                            "description": "Internal server error"
                        }
                    }
                }

                # Add parameters for path variables
                path_params = self._extract_path_parameters(path)
                if path_params:
                    paths[path][method]["parameters"] = [
                        {
                            "name": param,
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": f"{param} parameter"
                        }
                        for param in path_params
                    ]

        return paths

    def _generate_components(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate OpenAPI components section."""
        components = {
            "schemas": {},
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key"
                },
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }

        if 'schemas' in parsed_data:
            for schema_name, schema_info in parsed_data['schemas'].items():
                components["schemas"][schema_name] = {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "Unique identifier"},
                        "created_at": {"type": "string", "format": "date-time", "description": "Creation timestamp"},
                        "updated_at": {"type": "string", "format": "date-time", "description": "Last update timestamp"}
                    }
                }

        return components

    def _generate_tags(self, parsed_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate OpenAPI tags section."""
        tags = [
            {"name": "authentication", "description": "Authentication endpoints"},
            {"name": "users", "description": "User management endpoints"},
            {"name": "data", "description": "Data operations endpoints"}
        ]

        # Extract unique frameworks from endpoints
        if 'endpoints' in parsed_data:
            frameworks = set()
            for endpoint in parsed_data['endpoints']:
                if 'framework' in endpoint:
                    frameworks.add(endpoint['framework'])

            for framework in frameworks:
                tags.append({
                    "name": framework,
                    "description": f"{framework.capitalize()} framework endpoints"
                })

        return tags

    def _get_tags_for_endpoint(self, endpoint: Dict[str, Any]) -> List[str]:
        """Get tags for a specific endpoint."""
        tags = []

        if 'framework' in endpoint:
            tags.append(endpoint['framework'])

        # Categorize by path
        path = endpoint.get('path', '')
        if '/auth' in path or '/login' in path or '/token' in path:
            tags.append('authentication')
        elif '/users' in path or '/user' in path:
            tags.append('users')
        elif '/data' in path or '/items' in path or '/resources' in path:
            tags.append('data')

        return tags

    def _extract_path_parameters(self, path: str) -> List[str]:
        """Extract path parameters from route pattern."""
        import re
        pattern = r'{([^}]+)}'
        return re.findall(pattern, path)

    def save_openapi_spec(self, openapi_spec: Dict[str, Any], output_path: str,
                         format: str = 'json') -> str:
        """
        Save OpenAPI specification to file.

        Args:
            openapi_spec: OpenAPI specification
            output_path: Path to save the file
            format: Output format ('json' or 'yaml')

        Returns:
            Path to saved file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(openapi_spec, f, indent=2)
        elif format == 'yaml':
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(openapi_spec, f, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

        return str(output_path)

    def save_markdown(self, markdown_content: str, output_path: str) -> str:
        """
        Save markdown documentation to file.

        Args:
            markdown_content: Markdown content
            output_path: Path to save the file

        Returns:
            Path to saved file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        return str(output_path)