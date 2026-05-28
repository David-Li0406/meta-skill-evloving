import os
import json
import sys
import httpx
from pathlib import Path
from typing import Optional, Dict, Any, Generator

# ============================================================================
# Configuration
# ============================================================================

def load_env_file():
    """Load environment variables from .env file if it exists."""
    # Look for .env in current directory and parent directories
    current = Path(__file__).parent.parent  # Start from tools/../ (project root)
    env_file = current / ".env"

    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:  # Don't override existing env vars
                        os.environ[key] = value

# Load .env file on import
load_env_file()

ROBYNN_API_BASE_URL = os.environ.get("ROBYNN_API_BASE_URL", "https://robynn.ai")

# ============================================================================
# Remote CMO Execution
# ============================================================================

class RemoteCMO:
    """Handles remote execution of CMO agent tasks via Robynn API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ROBYNN_API_KEY")
        self.base_url = ROBYNN_API_BASE_URL

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def stream_query(self, message: str) -> Generator[Dict[str, Any], None, None]:
        """Execute a query and stream the results/progress."""
        url = f"{self.base_url}/api/agents/cmo/stream"
        payload = {"message": message}
        
        try:
            with httpx.stream(
                "POST", 
                url, 
                json=payload, 
                headers=self._get_headers(),
                timeout=600.0
            ) as response:
                if response.status_code == 401:
                    yield {
                        "type": "error", 
                        "message": "Not connected to Robynn.\n\n"
                                   "Quick fix: Run 'rory init' to set up your account.\n"
                                   "Or if you already have a key: 'rory config <your_key>'"
                    }
                    return
                elif response.status_code != 200:
                    yield {"type": "error", "message": f"Server error: {response.status_code}"}
                    return

                buffer = ""
                for chunk in response.iter_text():
                    buffer += chunk
                    while "\n\n" in buffer:
                        event_block, buffer = buffer.split("\n\n", 1)
                        event_data = self._parse_event(event_block)
                        if event_data:
                            yield event_data
        except Exception as e:
            yield {"type": "error", "message": f"Connection error: {str(e)}"}

    def _parse_event(self, block: str) -> Optional[Dict[str, Any]]:
        """Parse an SSE event block."""
        lines = block.strip().split("\n")
        event_type = "message"
        data_str = ""
        
        for line in lines:
            if line.startswith("event:"):
                event_type = line[6:].strip()
            elif line.startswith("data:"):
                data_str += line[5:].strip()
        
        if not data_str:
            return None
            
        try:
            return json.loads(data_str)
        except json.JSONDecodeError:
            # Fallback for non-JSON data
            return {"type": event_type, "message": data_str}

def main():
    """CLI entry point for remote execution."""
    if len(sys.argv) < 2:
        print("Usage: rory \"your query\"")
        sys.exit(1)
        
    query = sys.argv[1]
    cmo = RemoteCMO()
    
    print(f"\n⠋ Rory is thinking about: {query[:50]}...")
    
    for event in cmo.stream_query(query):
        etype = event.get("type")
        msg = event.get("message")
        
        if etype == "status":
            print(f"  → {msg}")
        elif etype == "progress":
            print(f"  ⚙️  {msg}")
        elif etype == "complete":
            print("\n" + "="*80)
            data = event.get("data", {})
            print(data.get("response", "Done."))
            print("="*80)

            # Display usage if available (can be in data.usage or data.metadata.usage)
            metadata = data.get("metadata", {})
            usage = metadata.get("usage") or data.get("usage")
            if usage:
                remaining = usage.get("remaining")
                limit = usage.get("limit")
                tier = usage.get("tier", "")
                unit = usage.get("unit", "month")
                if remaining is not None and limit is not None:
                    print(f"✓ {remaining} of {limit} tasks remaining this {unit}. (Tier: {tier})")

            print("✓ Task complete. Sounds like you.")
            print()
        elif etype == "error":
            print(f"\n❌ Error: {msg}")

if __name__ == "__main__":
    main()
