#!/usr/bin/env python3
"""
MCP Server Initializer - Creates a new MCP server from template

Usage:
    init_mcp.py <mcp-name> --path <path> --lang <python|typescript>

Examples:
    init_mcp.py my-mcp-server --path ./servers --lang python
    init_mcp.py weather-api --path ./servers --lang typescript
"""

import sys
from pathlib import Path


# Python MCP Server Template
PYTHON_SERVER_TEMPLATE = """#!/usr/bin/env python3
\"\"\"
{server_title} MCP Server

An MCP server implementation for {server_name}.
\"\"\"

from mcp.server.fastmcp import FastMCP
from typing import Any

# Initialize FastMCP server
mcp = FastMCP("{server_name}")


@mcp.tool()
async def example_tool(param: str) -> str:
    \"\"\"Example tool that demonstrates the basic structure.
    
    Args:
        param: A sample parameter
        
    Returns:
        A formatted response string
    \"\"\"
    return f"Processed: {{param}}"


# Add your tools here using the @mcp.tool() decorator
# See python_mcp_server.md in reference/ for more patterns


if __name__ == "__main__":
    # Run the server
    mcp.run()
"""

PYTHON_REQUIREMENTS = """mcp>=0.9.0
# Add your dependencies here
"""

PYTHON_README = """# {server_title}

MCP server for {server_name}.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run with stdio transport
```bash
python server.py
```

### Run with MCP Inspector
```bash
npx @modelcontextprotocol/inspector python server.py
```

## Configuration

Edit `server.py` to add your tools and resources.

## Development

See [python_mcp_server.md](reference/python_mcp_server.md) for implementation patterns.
"""


# TypeScript MCP Server Template
TS_SERVER_TEMPLATE = """import {{ Server }} from "@modelcontextprotocol/sdk/server/index.js";
import {{ StdioServerTransport }} from "@modelcontextprotocol/sdk/server/stdio.js";
import {{
    CallToolRequestSchema,
    ListToolsRequestSchema,
}} from "@modelcontextprotocol/sdk/types.js";

// Create server instance
const server = new Server(
    {{
        name: "{server_name}",
        version: "0.1.0",
    }},
    {{
        capabilities: {{
            tools: {{}},
        }},
    }}
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({{
    return {{
        tools: [
            {{
                name: "example_tool",
                description: "An example tool that demonstrates the basic structure",
                inputSchema: {{
                    type: "object",
                    properties: {{
                        param: {{
                            type: "string",
                            description: "A sample parameter",
                        }},
                    }},
                    required: ["param"],
                }},
            }},
        ],
    }};
}});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {{
    const {{ name, arguments: args }} = request.params;

    if (name === "example_tool") {{
        const param = args?.param as string;
        return {{
            content: [{{
                type: "text",
                text: `Processed: ${{param}}`,
            }}],
        }};
    }}

    throw new Error(`Unknown tool: ${{name}}`);
}});

// Start the server
async function main() {{
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("{server_title} MCP server running on stdio");
}}

main().catch((error) => {{
    console.error("Fatal error in main():", error);
    process.exit(1);
}});
"""

TS_PACKAGE_JSON = """{{
  "name": "{server_name}",
  "version": "0.1.0",
  "description": "{server_title} MCP Server",
  "type": "module",
  "main": "build/index.js",
  "bin": {{
    "server": "build/index.js"
  }},
  "scripts": {{
    "build": "tsc",
    "watch": "tsc --watch",
    "prepare": "npm run build",
    "server": "node build/index.js"
  }},
  "dependencies": {{
    "@modelcontextprotocol/sdk": "^1.0.4"
  }},
  "devDependencies": {{
    "@types/node": "^20",
    "typescript": "^5.6.3"
  }}
}}
"""

TS_TSCONFIG = """{{
  "compilerOptions": {{
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }},
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}}
"""

TS_README = """# {server_title}

MCP server for {server_name}.

## Installation

```bash
npm install
npm run build
```

## Usage

### Run with stdio transport
```bash
npm run server
```

### Run with MCP Inspector
```bash
npx @modelcontextprotocol/inspector npm run server
```

## Configuration

Edit `src/index.ts` to add your tools and resources.

## Development

```bash
npm run watch  # Watch mode for development
```

See [node_mcp_server.md](reference/node_mcp_server.md) for implementation patterns.
"""


def title_case_mcp_name(mcp_name):
    """Convert hyphenated MCP name to Title Case for display."""
    return ' '.join(word.capitalize() for word in mcp_name.split('-'))


def init_python_mcp(mcp_name, mcp_dir):
    """Initialize a Python MCP server."""
    mcp_title = title_case_mcp_name(mcp_name)
    
    # Create src directory structure
    src_dir = mcp_dir / 'src'
    src_dir.mkdir(exist_ok=True)
    
    # Create server.py
    server_py = src_dir / 'server.py'
    server_py.write_text(PYTHON_SERVER_TEMPLATE.format(
        server_name=mcp_name,
        server_title=mcp_title
    ))
    print("✅ Created src/server.py")
    
    # Create requirements.txt
    requirements = src_dir / 'requirements.txt'
    requirements.write_text(PYTHON_REQUIREMENTS)
    print("✅ Created src/requirements.txt")
    
    # Create README.md
    readme = mcp_dir / 'README.md'
    readme.write_text(PYTHON_README.format(
        server_name=mcp_name,
        server_title=mcp_title
    ))
    print("✅ Created README.md")
    
    return True


def init_typescript_mcp(mcp_name, mcp_dir):
    """Initialize a TypeScript MCP server."""
    mcp_title = title_case_mcp_name(mcp_name)
    
    # Create src directory
    src_dir = mcp_dir / 'src'
    src_dir.mkdir(exist_ok=True)
    
    # Create server file
    server_ts = src_dir / 'index.ts'
    server_ts.write_text(TS_SERVER_TEMPLATE.format(
        server_name=mcp_name,
        server_title=mcp_title
    ))
    print("✅ Created src/index.ts")
    
    # Create package.json
    package_json = mcp_dir / 'package.json'
    package_json.write_text(TS_PACKAGE_JSON.format(
        server_name=mcp_name,
        server_title=mcp_title
    ))
    print("✅ Created package.json")
    
    # Create tsconfig.json
    tsconfig = mcp_dir / 'tsconfig.json'
    tsconfig.write_text(TS_TSCONFIG)
    print("✅ Created tsconfig.json")
    
    # Create README.md
    readme = mcp_dir / 'README.md'
    readme.write_text(TS_README.format(
        server_name=mcp_name,
        server_title=mcp_title
    ))
    print("✅ Created README.md")
    
    return True


def init_mcp(mcp_name, path, lang):
    """
    Initialize a new MCP server directory.

    Args:
        mcp_name: Name of the MCP server
        path: Path where the MCP directory should be created
        lang: Programming language (python or typescript)

    Returns:
        Path to created MCP directory, or None if error
    """
    # Validate language
    lang = lang.lower()
    if lang not in ['python', 'typescript']:
        print(f"❌ Error: Language must be 'python' or 'typescript', got '{lang}'")
        return None
    
    # Determine MCP directory path
    mcp_dir = Path(path).resolve() / mcp_name

    # Check if directory already exists
    if mcp_dir.exists():
        print(f"❌ Error: MCP directory already exists: {mcp_dir}")
        return None

    # Create MCP directory
    try:
        mcp_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created MCP directory: {mcp_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Create reference directory with symlinks or copies
    try:
        ref_dir = mcp_dir / 'reference'
        ref_dir.mkdir(exist_ok=True)
        
        # Get the path to mcp-builder reference files
        script_dir = Path(__file__).parent.parent
        builder_ref_dir = script_dir / 'reference'
        
        if builder_ref_dir.exists():
            # Copy reference files
            for ref_file in builder_ref_dir.glob('*.md'):
                dest = ref_dir / ref_file.name
                dest.write_text(ref_file.read_text())
            print(f"✅ Created reference/ with MCP documentation")
    except Exception as e:
        print(f"⚠️  Warning: Could not copy reference files: {e}")

    # Initialize based on language
    if lang == 'python':
        success = init_python_mcp(mcp_name, mcp_dir)
    else:  # typescript
        success = init_typescript_mcp(mcp_name, mcp_dir)
    
    if not success:
        return None

    # Print next steps
    print(f"\n✅ MCP server '{mcp_name}' initialized successfully at {mcp_dir}")
    print("\nNext steps:")
    if lang == 'python':
        print("1. Edit src/server.py to implement your tools")
        print("2. Add dependencies to src/requirements.txt")
        print("3. Test with: npx @modelcontextprotocol/inspector python src/server.py")
    else:
        print("1. Edit src/index.ts to implement your tools")
        print("2. Run: npm install")
        print("3. Run: npm run build")
        print("4. Test with: npx @modelcontextprotocol/inspector npm run server")
    print("\nSee reference/ for MCP implementation guides and best practices.")

    return mcp_dir


def main():
    if len(sys.argv) < 6 or sys.argv[2] != '--path' or sys.argv[4] != '--lang':
        print("Usage: init_mcp.py <mcp-name> --path <path> --lang <python|typescript>")
        print("\nMCP name requirements:")
        print("  - Hyphen-case identifier (e.g., 'my-mcp-server')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Must match directory name exactly")
        print("\nLanguage options:")
        print("  - python:      Python FastMCP server")
        print("  - typescript:  TypeScript MCP SDK server")
        print("\nExamples:")
        print("  init_mcp.py weather-api --path ./servers --lang python")
        print("  init_mcp.py github-tools --path ./servers --lang typescript")
        sys.exit(1)

    mcp_name = sys.argv[1]
    path = sys.argv[3]
    lang = sys.argv[5]

    print(f"🚀 Initializing MCP server: {mcp_name}")
    print(f"   Location: {path}")
    print(f"   Language: {lang}")
    print()

    result = init_mcp(mcp_name, path, lang)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
