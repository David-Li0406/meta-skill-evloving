#!/usr/bin/env python3
"""
Gemini RLM CLI Orchestrator

This script implements the "Root LLM" logic for the Recursive Language Model architecture.
It uses the `rlm_repl.py` for persistent context state and the Gemini API for processing.

Usage:
  export GEMINI_API_KEY="your_key"
  python gem_rlm.py --context path/to/large_file.txt --query "Your question"
"""

import argparse
import os
import sys
import json
import subprocess
import glob
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any

# --- Configuration ---
REPL_SCRIPT = Path(__file__).parent / "scripts" / "rlm_repl.py"
STATE_DIR = Path(__file__).parent / "state"
STATE_FILE = STATE_DIR / "state.pkl"
CHUNKS_DIR = STATE_DIR / "chunks"

# Models
SUB_MODEL = "gemini-2.0-flash-exp"  # Fast model for chunks
ROOT_MODEL = "gemini-2.0-flash-exp" # Strong model for synthesis (using Flash for speed/cost in this min version)

class GeminiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate_content(self, model: str, prompt: str) -> str:
        url = f"{self.base_url}/{model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                try:
                    return result['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError):
                    return "" # Return empty if blocked or error structure
        except urllib.error.HTTPError as e:
            print(f"Error calling Gemini API: {e}", file=sys.stderr)
            print(e.read().decode('utf-8'), file=sys.stderr)
            return ""

def run_repl(args: List[str]) -> str:
    """Runs the rlm_repl.py script and returns stdout."""
    # Ensure state directory exists
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    
    cmd = [sys.executable, str(REPL_SCRIPT), "--state", str(STATE_FILE)] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"REPL Error: {result.stderr}", file=sys.stderr)
        raise RuntimeError("REPL command failed")
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Gemini RLM CLI")
    parser.add_argument("--context", required=True, help="Path to large context file")
    parser.add_argument("--query", required=True, help="Question to answer")
    parser.add_argument("--chunk-size", type=int, default=50000, help="Chunk size in chars")
    parser.add_argument("--overlap", type=int, default=0, help="Chunk overlap")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    client = GeminiClient(api_key)

    print(f"--- RLM Started ---\nContext: {args.context}\nQuery: {args.query}\n")

    # 1. Initialize REPL
    print("1. Initializing Context Environment...")
    # Clean previous state
    if STATE_DIR.exists():
        import shutil
        shutil.rmtree(STATE_DIR)
    
    run_repl(["init", args.context])
    
    # 2. Create Chunks
    print(f"2. Chunking Document (Size: {args.chunk_size})...")
    # We use the REPL's exec to run the write_chunks helper
    chunk_script = f"""
paths = write_chunks('{CHUNKS_DIR}', size={args.chunk_size}, overlap={args.overlap})
print(len(paths))
"""
    repl_out = run_repl(["exec", "-c", chunk_script])
    try:
        num_chunks = int(repl_out.strip().split('\n')[-1]) # Last line should be the number
        print(f"   Created {num_chunks} chunks.")
    except ValueError:
        print("   Warning: Could not determine number of chunks from REPL output.")
        num_chunks = 0 # Will verify via glob

    chunk_files = sorted(glob.glob(str(CHUNKS_DIR / "chunk_*.txt")))
    if not chunk_files:
        print("Error: No chunks created.")
        sys.exit(1)

    # 3. Sub-LLM Processing Loop
    print("3. Running Sub-LLM on Chunks...")
    observations = []
    
    for i, chunk_path in enumerate(chunk_files):
        print(f"   Processing chunk {i+1}/{len(chunk_files)}...", end="", flush=True)
        chunk_content = Path(chunk_path).read_text()
        
        # Sub-LLM Prompt
        sub_prompt = f"""
You are a sub-process reading a chunk of a larger document.
Your task is to extract information RELEVANT to the user's query.
If the chunk contains no relevant information, output "NO_RELEVANT_INFO".
Be concise.

User Query: {args.query}

--- CHUNK START ---
{chunk_content}
--- CHUNK END ---

Relevant Findings:
"""
        response = client.generate_content(SUB_MODEL, sub_prompt).strip()
        
        if response and "NO_RELEVANT_INFO" not in response:
            observations.append(f"--- Info from Chunk {i} ---\n{response}\n")
            print(" Found info.")
        else:
            print(" No relevant info.")

    # 4. Synthesis
    print("\n4. Synthesizing Final Answer...")
    if not observations:
        print("No relevant information found in the document.")
        sys.exit(0)

    all_findings = "\n".join(observations)
    
    # Root LLM Prompt
    root_prompt = f"""
You are the Root LLM. You have tasked sub-agents to scan a large document for information regarding a user's query.
Below are the aggregated findings from the document chunks.
Synthesize a comprehensive answer to the user's query based ONLY on these findings.

User Query: {args.query}

--- AGGREGATED FINDINGS ---
{all_findings}
--- END FINDINGS ---

Final Answer:
"""
    
    final_answer = client.generate_content(ROOT_MODEL, root_prompt)
    
    print("\n" + "="*40)
    print("FINAL ANSWER")
    print("="*40 + "\n")
    print(final_answer)

if __name__ == "__main__":
    main()
