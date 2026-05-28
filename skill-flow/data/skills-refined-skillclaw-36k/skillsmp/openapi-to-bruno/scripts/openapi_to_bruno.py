#!/usr/bin/env python3
"""
OpenAPI to Bruno Collection Converter

Converts OpenAPI specifications to Bruno .bru collection files with:
- Proper directory structure
- Generated test blocks
- Auth configuration
- Request chaining support
"""

import json
import yaml
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


class OpenAPIToBrunoConverter:
    """Convert OpenAPI specs to Bruno collections"""

    def __init__(self, openapi_file: str, output_dir: str, collection_name: Optional[str] = None):
        self.openapi_file = openapi_file
        self.output_dir = Path(output_dir)
        self.spec = self._load_spec()
        self.collection_name = collection_name or self.spec.get('info', {}).get('title', 'API Collection')
        self.base_url_var = "baseUrl"
        self.auth_var = "accessToken"

    def _load_spec(self) -> Dict:
        """Load OpenAPI specification from YAML or JSON"""
        with open(self.openapi_file, 'r') as f:
            content = f.read()
            try:
                # Try YAML first
                return yaml.safe_load(content)
            except yaml.YAMLError:
                # Fallback to JSON
                return json.loads(content)

    def convert(self):
        """Main conversion process"""
        print(f"Converting {self.openapi_file} to Bruno collection...")

        # Create collection structure
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate bruno.json
        self._generate_bruno_json()

        # Generate environments
        self._generate_environments()

        # Process paths and generate .bru files
        self._process_paths()

        print(f"✅ Conversion complete! Collection created at: {self.output_dir}")

    def _generate_bruno_json(self):
        """Generate bruno.json configuration"""
        config = {
            "version": "1",
            "name": self.collection_name,
            "type": "collection"
        }

        bruno_json_path = self.output_dir / "bruno.json"
        with open(bruno_json_path, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"✅ Created bruno.json")

    def _generate_environments(self):
        """Generate environment files from servers"""
        env_dir = self.output_dir / "environments"
        env_dir.mkdir(exist_ok=True)

        servers = self.spec.get('servers', [])

        if not servers:
            # Create default environment
            self._create_env_file(env_dir / "default.bru", "https://api.example.com", {})
            return

        # Create environment for each server
        for idx, server in enumerate(servers):
            url = server.get('url', '')
            description = server.get('description', '')

            # Determine environment name
            env_name = self._infer_env_name(description, url, idx)

            # Get variables
            variables = server.get('variables', {})

            self._create_env_file(env_dir / f"{env_name}.bru", url, variables)

        print(f"✅ Created {len(servers) or 1} environment file(s)")

    def _infer_env_name(self, description: str, url: str, index: int) -> str:
        """Infer environment name from description or URL"""
        desc_lower = description.lower()
        url_lower = url.lower()

        if 'prod' in desc_lower or 'production' in desc_lower or 'prod' in url_lower:
            return 'production'
        elif 'stag' in desc_lower or 'staging' in desc_lower or 'stag' in url_lower:
            return 'staging'
        elif 'dev' in desc_lower or 'development' in desc_lower or 'dev' in url_lower:
            return 'development'
        elif 'test' in desc_lower or 'test' in url_lower:
            return 'test'
        elif 'local' in desc_lower or 'localhost' in url_lower:
            return 'local'
        else:
            return f'env{index + 1}' if index > 0 else 'default'

    def _create_env_file(self, path: Path, base_url: str, variables: Dict):
        """Create a Bruno environment file"""
        content = f"vars {{\n  {self.base_url_var}: {base_url}\n"

        # Add server variables
        for var_name, var_info in variables.items():
            default_value = var_info.get('default', '')
            content += f"  {var_name}: {default_value}\n"

        content += "}\n"

        with open(path, 'w') as f:
            f.write(content)

    def _process_paths(self):
        """Process all paths and generate .bru files"""
        paths = self.spec.get('paths', {})

        if not paths:
            print("⚠️  No paths found in OpenAPI spec")
            return

        for path, path_item in paths.items():
            self._process_path(path, path_item)

        print(f"✅ Generated {len(paths)} endpoint(s)")

    def _process_path(self, path: str, path_item: Dict):
        """Process a single path and create .bru files for each operation"""
        # HTTP methods to process
        methods = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

        for method in methods:
            if method in path_item:
                operation = path_item[method]
                self._generate_bru_file(path, method, operation, path_item)

    def _generate_bru_file(self, path: str, method: str, operation: Dict, path_item: Dict):
        """Generate a .bru file for a single operation"""
        # Determine directory structure and filename
        dir_path, filename = self._get_file_location(path, method, operation)

        # Create directory
        full_dir = self.output_dir / dir_path
        full_dir.mkdir(parents=True, exist_ok=True)

        # Generate .bru content
        content = self._generate_bru_content(path, method, operation, path_item)

        # Write file
        bru_file = full_dir / f"{filename}.bru"
        with open(bru_file, 'w') as f:
            f.write(content)

    def _get_file_location(self, path: str, method: str, operation: Dict) -> Tuple[str, str]:
        """Determine directory structure and filename for .bru file"""
        # Get operation ID or generate one
        operation_id = operation.get('operationId', '')

        # Clean path for directory structure
        path_parts = [p for p in path.split('/') if p and not p.startswith('{')]

        # Get tags for organization
        tags = operation.get('tags', [])

        # Determine directory
        if tags:
            dir_path = tags[0].lower().replace(' ', '-')
        elif path_parts:
            dir_path = path_parts[0].lower()
        else:
            dir_path = 'endpoints'

        # Determine filename
        if operation_id:
            filename = self._slugify(operation_id)
        else:
            # Generate from method and path
            if path_parts:
                filename = f"{method}-{'-'.join(path_parts)}"
            else:
                filename = method
            filename = self._slugify(filename)

        return dir_path, filename

    def _slugify(self, text: str) -> str:
        """Convert text to slug format"""
        # Convert to lowercase
        text = text.lower()
        # Replace spaces and underscores with hyphens
        text = re.sub(r'[\s_]+', '-', text)
        # Remove non-alphanumeric characters except hyphens
        text = re.sub(r'[^a-z0-9\-]', '', text)
        # Remove consecutive hyphens
        text = re.sub(r'-+', '-', text)
        # Strip hyphens from ends
        text = text.strip('-')
        return text

    def _generate_bru_content(self, path: str, method: str, operation: Dict, path_item: Dict) -> str:
        """Generate complete .bru file content"""
        content = []

        # Meta block
        content.append(self._generate_meta_block(operation))
        content.append("")

        # HTTP method block
        content.append(self._generate_method_block(path, method, operation))
        content.append("")

        # Parameters
        query_params = self._get_query_parameters(operation, path_item)
        if query_params:
            content.append(self._generate_params_block(query_params))
            content.append("")

        # Headers
        headers = self._generate_headers(operation)
        if headers:
            content.append(self._generate_headers_block(headers))
            content.append("")

        # Auth
        auth_block = self._generate_auth_block(operation)
        if auth_block:
            content.append(auth_block)
            content.append("")

        # Body
        body_block = self._generate_body_block(method, operation)
        if body_block:
            content.append(body_block)
            content.append("")

        # Pre-request script
        pre_request = self._generate_pre_request_script(operation)
        if pre_request:
            content.append(pre_request)
            content.append("")

        # Tests
        tests = self._generate_tests_block(method, operation)
        content.append(tests)

        return "\n".join(content)

    def _generate_meta_block(self, operation: Dict) -> str:
        """Generate meta block"""
        name = operation.get('summary', operation.get('operationId', 'API Request'))
        return f"meta {{\n  name: {name}\n  type: http\n  seq: 1\n}}"

    def _generate_method_block(self, path: str, method: str, operation: Dict) -> str:
        """Generate HTTP method block"""
        # Convert path parameters to Bruno format
        url = path.replace('{', '{{').replace('}', '}}')
        url = f"{{{{{self.base_url_var}}}}}{url}"

        body_type = "none"
        if method in ['post', 'put', 'patch']:
            request_body = operation.get('requestBody', {})
            content = request_body.get('content', {})
            if 'application/json' in content:
                body_type = "json"
            elif 'multipart/form-data' in content:
                body_type = "multipartForm"
            elif 'application/x-www-form-urlencoded' in content:
                body_type = "formUrlEncoded"

        return f"{method} {{\n  url: {url}\n  body: {body_type}\n  auth: none\n}}"

    def _get_query_parameters(self, operation: Dict, path_item: Dict) -> List[Dict]:
        """Extract query parameters from operation"""
        params = []

        # Combine path-level and operation-level parameters
        all_params = path_item.get('parameters', []) + operation.get('parameters', [])

        for param in all_params:
            # Resolve $ref if present
            if '$ref' in param:
                param = self._resolve_ref(param['$ref'])

            if param.get('in') == 'query':
                params.append(param)

        return params

    def _generate_params_block(self, params: List[Dict]) -> str:
        """Generate query parameters block"""
        lines = ["params:query {"]

        for param in params:
            name = param.get('name', '')
            schema = param.get('schema', {})
            example = schema.get('example', schema.get('default', ''))

            # Use example or default value
            if example:
                lines.append(f"  {name}: {example}")
            else:
                # Use placeholder based on type
                param_type = schema.get('type', 'string')
                if param_type == 'integer':
                    lines.append(f"  {name}: 10")
                elif param_type == 'boolean':
                    lines.append(f"  {name}: true")
                else:
                    lines.append(f"  {name}: value")

        lines.append("}")
        return "\n".join(lines)

    def _generate_headers(self, operation: Dict) -> Dict[str, str]:
        """Generate headers for request"""
        headers = {}

        # Content-Type from requestBody
        request_body = operation.get('requestBody', {})
        content = request_body.get('content', {})

        if 'application/json' in content:
            headers['Content-Type'] = 'application/json'
        elif 'application/xml' in content:
            headers['Content-Type'] = 'application/xml'

        # Accept header from responses
        responses = operation.get('responses', {})
        for response in responses.values():
            if isinstance(response, dict):
                response_content = response.get('content', {})
                if 'application/json' in response_content:
                    headers['Accept'] = 'application/json'
                    break

        return headers

    def _generate_headers_block(self, headers: Dict[str, str]) -> str:
        """Generate headers block"""
        lines = ["headers {"]
        for key, value in headers.items():
            lines.append(f"  {key}: {value}")
        lines.append("}")
        return "\n".join(lines)

    def _generate_auth_block(self, operation: Dict) -> Optional[str]:
        """Generate auth block based on security requirements"""
        # Check operation-level security
        security = operation.get('security', self.spec.get('security', []))

        if not security:
            return None

        # Get first security scheme
        if security and len(security) > 0:
            scheme_name = list(security[0].keys())[0]
            scheme = self._get_security_scheme(scheme_name)

            if not scheme:
                return None

            scheme_type = scheme.get('type', '')

            if scheme_type == 'http':
                http_scheme = scheme.get('scheme', '').lower()
                if http_scheme == 'bearer':
                    return f"auth:bearer {{\n  token: {{{{{self.auth_var}}}}}\n}}"
                elif http_scheme == 'basic':
                    return f"auth:basic {{\n  username: {{{{username}}}}\n  password: {{{{password}}}}\n}}"

            elif scheme_type == 'apiKey':
                # API key in header (handled in headers block)
                return None

            elif scheme_type == 'oauth2':
                flows = scheme.get('flows', {})
                if 'authorizationCode' in flows:
                    return "auth:oauth2 {\n  grant_type: authorization_code\n  // Configure OAuth2 settings\n}"

        return None

    def _get_security_scheme(self, name: str) -> Optional[Dict]:
        """Get security scheme definition"""
        components = self.spec.get('components', {})
        security_schemes = components.get('securitySchemes', {})
        return security_schemes.get(name)

    def _generate_body_block(self, method: str, operation: Dict) -> Optional[str]:
        """Generate request body block"""
        if method not in ['post', 'put', 'patch']:
            return None

        request_body = operation.get('requestBody', {})
        content = request_body.get('content', {})

        if 'application/json' in content:
            schema = content['application/json'].get('schema', {})
            example = self._generate_example_from_schema(schema)

            return f"body:json {{\n  {json.dumps(example, indent=2)}\n}}"

        elif 'application/x-www-form-urlencoded' in content:
            schema = content['application/x-www-form-urlencoded'].get('schema', {})
            properties = schema.get('properties', {})

            lines = ["body:form-urlencoded {"]
            for prop_name, prop_schema in properties.items():
                example = prop_schema.get('example', prop_schema.get('default', 'value'))
                lines.append(f"  {prop_name}: {example}")
            lines.append("}")
            return "\n".join(lines)

        elif 'multipart/form-data' in content:
            return "body:multipart-form {\n  // Add form fields here\n}"

        return None

    def _generate_example_from_schema(self, schema: Dict) -> Any:
        """Generate example data from JSON schema"""
        # Check for example
        if 'example' in schema:
            return schema['example']

        # Resolve $ref
        if '$ref' in schema:
            schema = self._resolve_ref(schema['$ref'])
            return self._generate_example_from_schema(schema)

        schema_type = schema.get('type', 'object')

        if schema_type == 'object':
            properties = schema.get('properties', {})
            obj = {}
            for prop_name, prop_schema in properties.items():
                obj[prop_name] = self._generate_example_from_schema(prop_schema)
            return obj

        elif schema_type == 'array':
            items = schema.get('items', {})
            return [self._generate_example_from_schema(items)]

        elif schema_type == 'string':
            return schema.get('default', 'string')

        elif schema_type == 'integer':
            return schema.get('default', 0)

        elif schema_type == 'number':
            return schema.get('default', 0.0)

        elif schema_type == 'boolean':
            return schema.get('default', True)

        return None

    def _resolve_ref(self, ref: str) -> Dict:
        """Resolve $ref to actual schema"""
        # Parse ref like #/components/schemas/User
        parts = ref.split('/')
        current = self.spec

        for part in parts:
            if part == '#':
                continue
            current = current.get(part, {})

        return current

    def _generate_pre_request_script(self, operation: Dict) -> Optional[str]:
        """Generate pre-request script if needed"""
        # Check if we need to generate test data
        request_body = operation.get('requestBody', {})

        if request_body:
            return """script:pre-request {
  // Generate test data if needed
  const timestamp = Date.now();
  // bru.setVar("testValue", `value_${timestamp}`);
}"""

        return None

    def _generate_tests_block(self, method: str, operation: Dict) -> str:
        """Generate comprehensive tests block"""
        lines = ["tests {"]

        # Get expected response
        responses = operation.get('responses', {})
        success_code = self._get_success_code(method, responses)

        # Status code test
        lines.append(f'  test("Status code is {success_code}", function() {{')
        lines.append(f'    expect(res.getStatus()).to.equal({success_code});')
        lines.append('  });')
        lines.append('')

        # Response body tests
        if success_code != '204':
            response_schema = self._get_response_schema(responses, success_code)

            if response_schema:
                schema_tests = self._generate_schema_tests(response_schema)
                lines.extend(schema_tests)

        # Response time test
        lines.append('  test("Response time acceptable", function() {')
        lines.append('    expect(res.getResponseTime()).to.be.below(2000);')
        lines.append('  });')

        # Save data for chaining (POST/PUT)
        if method in ['post', 'put']:
            lines.append('')
            lines.append('  test("Save resource ID", function() {')
            lines.append('    const data = res.getBody();')
            lines.append('    if (data && data.id) {')
            lines.append('      bru.setVar("resourceId", data.id);')
            lines.append('    }')
            lines.append('  });')

        lines.append("}")
        return "\n".join(lines)

    def _get_success_code(self, method: str, responses: Dict) -> str:
        """Determine expected success status code"""
        if method == 'post':
            if '201' in responses:
                return '201'
        if method == 'delete':
            if '204' in responses:
                return '204'

        # Default to 200
        if '200' in responses:
            return '200'

        # Return first 2xx code
        for code in responses.keys():
            if code.startswith('2'):
                return code

        return '200'

    def _get_response_schema(self, responses: Dict, status_code: str) -> Optional[Dict]:
        """Get response schema for status code"""
        response = responses.get(status_code, {})

        # Resolve $ref if present
        if '$ref' in response:
            response = self._resolve_ref(response['$ref'])

        content = response.get('content', {})

        # Check for JSON content
        if 'application/json' in content:
            schema = content['application/json'].get('schema', {})

            # Resolve $ref in schema
            if '$ref' in schema:
                schema = self._resolve_ref(schema['$ref'])

            return schema

        return None

    def _generate_schema_tests(self, schema: Dict) -> List[str]:
        """Generate tests for response schema validation"""
        lines = []

        schema_type = schema.get('type', 'object')

        if schema_type == 'array':
            lines.append('  test("Response is array", function() {')
            lines.append('    const data = res.getBody();')
            lines.append('    expect(data).to.be.an(\'array\');')
            lines.append('  });')
            lines.append('')

            # Validate array items
            items_schema = schema.get('items', {})
            if '$ref' in items_schema:
                items_schema = self._resolve_ref(items_schema['$ref'])

            if items_schema.get('type') == 'object':
                properties = items_schema.get('properties', {})
                if properties:
                    lines.append('  test("Array items have correct structure", function() {')
                    lines.append('    const data = res.getBody();')
                    lines.append('    if (data.length > 0) {')
                    for prop_name in properties.keys():
                        lines.append(f'      expect(data[0]).to.have.property(\'{prop_name}\');')
                    lines.append('    }')
                    lines.append('  });')
                    lines.append('')

        elif schema_type == 'object':
            properties = schema.get('properties', {})
            required = schema.get('required', [])

            if properties:
                lines.append('  test("Response has required fields", function() {')
                lines.append('    const data = res.getBody();')

                # Test required fields
                for prop_name in required:
                    lines.append(f'    expect(data).to.have.property(\'{prop_name}\');')

                lines.append('  });')
                lines.append('')

                # Type validation for key fields
                type_checks = []
                for prop_name, prop_schema in properties.items():
                    if '$ref' in prop_schema:
                        prop_schema = self._resolve_ref(prop_schema['$ref'])

                    prop_type = prop_schema.get('type', '')

                    if prop_type in ['string', 'number', 'boolean', 'array', 'object']:
                        js_type = prop_type
                        if prop_type == 'number':
                            js_type = 'number'
                        elif prop_type == 'integer':
                            js_type = 'number'

                        type_checks.append((prop_name, js_type))

                if type_checks:
                    lines.append('  test("Field types are correct", function() {')
                    lines.append('    const data = res.getBody();')
                    for prop_name, js_type in type_checks[:5]:  # Limit to first 5
                        lines.append(f'    if (data.{prop_name} !== undefined) {{')
                        lines.append(f'      expect(data.{prop_name}).to.be.a(\'{js_type}\');')
                        lines.append('    }')
                    lines.append('  });')
                    lines.append('')

        return lines


def main():
    """CLI entry point"""
    if len(sys.argv) < 3:
        print("Usage: python openapi_to_bruno.py <openapi-file> <output-directory> [collection-name]")
        sys.exit(1)

    openapi_file = sys.argv[1]
    output_dir = sys.argv[2]
    collection_name = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(openapi_file):
        print(f"❌ Error: OpenAPI file not found: {openapi_file}")
        sys.exit(1)

    converter = OpenAPIToBrunoConverter(openapi_file, output_dir, collection_name)
    converter.convert()


if __name__ == '__main__':
    main()
