#!/usr/bin/env python3
"""
Common utilities for HelixDB memory hooks.
Enhanced with real embeddings, time-windows, and reasoning chains.
"""

import json
import os
import requests
import configparser
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import sys

# ============================================================================
# CONFIGURATION LOADING
# ============================================================================

def _load_config() -> configparser.ConfigParser:
    """Load configuration from ~/.helix-memory.conf if it exists."""
    config = configparser.ConfigParser()
    config_path = Path.home() / ".helix-memory.conf"
    if config_path.exists():
        config.read(config_path)
    return config

_CONFIG = _load_config()

def _get_config(section: str, key: str, default: str = "") -> str:
    """Get config value with fallback to default."""
    try:
        value = _CONFIG.get(section, key)
        # Expand ~ in paths
        if value.startswith("~"):
            value = str(Path(value).expanduser())
        return value
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default

# HelixDB configuration
HELIX_URL = _get_config("helix", "url", "http://localhost:6969")
HELIX_DATA_DIR = _get_config("helix", "data_dir", str(Path.home() / ".claude/skills/helix-memory"))
HELIX_BIN = _get_config("paths", "helix_bin", str(Path.home() / ".local/bin/helix"))
CACHE_DIR = Path(_get_config("paths", "cache_dir", str(Path.home() / ".cache/helix-memory")))
P_TOOL = _get_config("tools", "p_tool", "")
H_TOOL = _get_config("tools", "h_tool", "")

# Embedding configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_EMBEDDING_MODEL = "text-embedding-004"  # 768 dims, free tier
GEMINI_LLM_MODEL = "gemma-3-4b-it"  # 30 RPM, 14.4K RPD - instruction-tuned, high free limits
EMBEDDING_DIM = 1536  # HelixDB was initialized with 1536 (OpenAI standard) - must match

# Ollama config - detect remote GPU vs local at startup
OLLAMA_REMOTE = "http://100.101.59.25:11434"  # RTX4070 PC via Tailscale
OLLAMA_LOCAL = "http://localhost:11434"
OLLAMA_MODEL = "nomic-embed-text"  # For embeddings

# Detect best Ollama server once at import
def _detect_ollama():
    try:
        requests.get(f"{OLLAMA_REMOTE}/api/tags", timeout=2)
        return OLLAMA_REMOTE, "llama3.1:8b", "remote-gpu"
    except:
        return OLLAMA_LOCAL, "llama3.2:3b", "local"

OLLAMA_URL, OLLAMA_LLM_MODEL, OLLAMA_SOURCE = _detect_ollama()

# LLM provider preference: "ollama" (free, local) or "haiku" (Claude API)
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "ollama")  # Default to Ollama when available

# Time windows (in hours)
TIME_WINDOWS = {
    "recent": 4,       # Last 4 hours - immediate context
    "contextual": 720, # Last 30 days - balanced
    "deep": 2160,      # Last 90 days - thorough
    "full": None       # All time
}

# Valid memory categories (per schema + problem)
VALID_CATEGORIES = {"preference", "fact", "context", "decision", "task", "solution", "problem"}

# Category normalization mappings (invalid -> valid)
CATEGORY_MAPPINGS = {
    # Preference variants
    "user preference": "preference",

    # Fact variants
    "insight": "fact",
    "benefit": "fact",
    "inconsistency": "fact",
    "credential": "fact",
    "path": "fact",
    "url": "fact",

    # Solution variants
    "feature": "solution",
    "problem solved": "solution",
    "solution proposal": "solution",

    # Problem variants
    "bug": "problem",
    "problem identification": "problem",

    # Task variants
    "user request": "task",

    # Decision variants
    "workflow choice": "decision",
}

def normalize_category(category: str) -> str:
    """
    Normalize arbitrary category to valid schema category.

    Args:
        category: Raw category string from LLM or user

    Returns:
        Valid category from VALID_CATEGORIES
    """
    if not category:
        return "fact"

    cat = category.strip().lower()

    # Already valid
    if cat in VALID_CATEGORIES:
        return cat

    # Map known invalid categories
    if cat in CATEGORY_MAPPINGS:
        return CATEGORY_MAPPINGS[cat]

    # Default fallback
    return "fact"

# Embedding cache (LRU-style, persisted per-process)
_embedding_cache: Dict[str, Tuple[List[float], str]] = {}
_CACHE_MAX_SIZE = 500  # Max cached embeddings

# ============================================================================
# BASIC I/O
# ============================================================================

def read_hook_input() -> Dict[str, Any]:
    """Read hook input JSON from stdin."""
    try:
        return json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse hook input: {e}", file=sys.stderr)
        sys.exit(1)

def parse_transcript(transcript_path: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Parse conversation transcript from JSONL file."""
    transcript = []
    try:
        with open(transcript_path, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    if entry.get("type") in ["user", "assistant"]:
                        transcript.append(entry)
    except FileNotFoundError:
        print(f"WARNING: Transcript file not found: {transcript_path}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"ERROR: Failed to parse transcript: {e}", file=sys.stderr)
        return []

    if limit and len(transcript) > limit:
        return transcript[-limit:]
    return transcript

def extract_message_content(message: Dict[str, Any]) -> str:
    """Extract text content from a message."""
    content = message.get("message", {}).get("content", "")
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))
            elif isinstance(block, str):
                texts.append(block)
        return "\n".join(texts)
    return str(content)

# ============================================================================
# PROJECT DETECTION
# ============================================================================

_known_projects_cache = None

def get_known_projects() -> Dict[str, str]:
    """Get known projects from p tool (cached)."""
    global _known_projects_cache
    if _known_projects_cache is not None:
        return _known_projects_cache

    import subprocess
    projects = {}

    # Use p_tool from config, or skip if not configured
    p_tool_path = P_TOOL or str(Path.home() / 'Tools' / 'p')
    if not Path(p_tool_path).exists():
        _known_projects_cache = projects
        return projects

    try:
        result = subprocess.run(
            [p_tool_path, '--list'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    name, path = line.split(':', 1)
                    name = name.strip()
                    path = path.strip()
                    if name and path:
                        projects[path] = name
    except Exception as e:
        print(f"WARNING: Could not get projects from p tool: {e}", file=sys.stderr)

    _known_projects_cache = projects
    return projects


def detect_project(cwd: str) -> str:
    """
    Detect project name from working directory.
    Priority:
    1. Exact match in p tool registry
    2. Directory name-based detection (most reliable)
    3. Prefix match in registry (least specific)
    """
    if not cwd:
        return ""

    cwd = cwd.rstrip('/')
    projects = get_known_projects()

    # Priority 1: Exact match or DIRECT child in registry
    # Only use registry if cwd IS the project or is immediately inside it
    for path, name in projects.items():
        path = path.rstrip('/')
        if cwd == path:
            return name.lower().replace(' ', '-')
        # Check if cwd is direct child or very close (max 2 levels deep)
        if cwd.startswith(path + '/'):
            relative = cwd[len(path)+1:]
            depth = len(relative.split('/'))
            if depth <= 2 and len(path.split('/')) > 4:  # Deep project, close match
                return name.lower().replace(' ', '-')

    # Priority 2: Extract from path (most reliable for unregistered projects)
    SKIP_DIRS = {'wordpress', 'wp-content', 'plugins', 'themes', 'Sites',
                 'Tools', 'Projects', 'PycharmProjects', 'Documents', 'Praca',
                 'Users', 'cminds', 'hooks', 'src', 'lib', 'node_modules',
                 '.wp-test', 'sites', 'Fiverr', '_WLASNE_'}

    parts = cwd.split('/')
    for part in reversed(parts):
        if part and len(part) > 2 and part not in SKIP_DIRS:
            # Clean up common suffixes
            result = part.lower().replace(' ', '-')
            result = result.replace('.local', '').replace('.loc', '')
            # Normalize known project aliases
            if result in ('marriagemarketal', 'marriagemarket'):
                return 'marriagemarket'
            return result

    # Priority 3: Fallback to longest prefix match
    best_match = ""
    best_name = ""
    for path, name in projects.items():
        path = path.rstrip('/')
        if cwd.startswith(path):
            if len(path) > len(best_match):
                best_match = path
                best_name = name

    if best_name:
        return best_name.lower().replace(' ', '-')

    return ""

# ============================================================================
# HELIX CONNECTION
# ============================================================================

def check_helix_running() -> bool:
    """Check if HelixDB is accessible."""
    try:
        response = requests.post(
            f"{HELIX_URL}/GetAllMemories",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=2
        )
        return response.status_code == 200
    except:
        return False

def try_restart_helix() -> bool:
    """Attempt to restart HelixDB if it's not running."""
    import subprocess
    print("INFO: Attempting to restart HelixDB...", file=sys.stderr)
    try:
        result = subprocess.run(
            [HELIX_BIN, "start", "dev"],
            cwd=HELIX_DATA_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            import time
            time.sleep(3)
            if check_helix_running():
                print("SUCCESS: HelixDB restarted successfully", file=sys.stderr)
                return True
        return False
    except Exception as e:
        print(f"WARNING: Error restarting HelixDB: {e}", file=sys.stderr)
        return False

def ensure_helix_running() -> bool:
    """Ensure HelixDB is running, attempting restart if needed."""
    if check_helix_running():
        return True
    if try_restart_helix():
        return True
    print("⚠️  ALERT: HelixDB not running and auto-restart failed", file=sys.stderr)
    return False

# ============================================================================
# EMBEDDINGS (Real vectors!)
# ============================================================================

def pad_embedding(embedding: List[float], target_dim: int = EMBEDDING_DIM) -> List[float]:
    """Pad embedding to target dimension with zeros."""
    if len(embedding) >= target_dim:
        return embedding[:target_dim]
    return embedding + [0.0] * (target_dim - len(embedding))


def generate_embedding_gemini(text: str) -> Optional[List[float]]:
    """Generate embedding using Google Gemini API (free tier)."""
    if not GEMINI_API_KEY:
        return None
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_EMBEDDING_MODEL}:embedContent",
            params={"key": GEMINI_API_KEY},
            json={
                "model": f"models/{GEMINI_EMBEDDING_MODEL}",
                "content": {"parts": [{"text": text[:8000]}]}
            },
            timeout=15
        )
        if response.status_code == 200:
            embedding = response.json().get("embedding", {}).get("values", [])
            if embedding:
                return pad_embedding(embedding)  # Pad 768 → 1536 for HelixDB
        else:
            print(f"WARNING: Gemini API error {response.status_code}: {response.text[:100]}", file=sys.stderr)
    except Exception as e:
        print(f"WARNING: Gemini embedding failed: {e}", file=sys.stderr)
    return None

def check_ollama_running() -> bool:
    """Check if Ollama is accessible (legacy fallback)."""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

def generate_embedding_ollama(text: str) -> Optional[List[float]]:
    """Generate embedding using Ollama (fallback). Note: nomic-embed-text is 768 dims."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": OLLAMA_MODEL, "prompt": text[:8000]},
            timeout=30
        )
        if response.status_code == 200:
            embedding = response.json().get("embedding")
            if embedding:
                return pad_embedding(embedding)  # Pad 768 → 1536 for HelixDB
    except Exception as e:
        print(f"WARNING: Ollama embedding failed: {e}", file=sys.stderr)
    return None

def generate_embedding_hash(text: str, dim: int = EMBEDDING_DIM) -> List[float]:
    """Fallback: Generate deterministic pseudo-embedding from text hash."""
    import hashlib
    normalized = ' '.join(text.lower().split())[:2000]
    text_hash = hashlib.sha256(normalized.encode()).hexdigest()
    vector = []
    for i in range(dim):
        byte_val = int(text_hash[(i * 2) % len(text_hash)], 16)
        vector.append((byte_val - 7.5) / 7.5)
    return vector

def generate_embedding(text: str) -> Tuple[List[float], str]:
    """
    Generate embedding with best available method + caching.
    Priority: Cache > Ollama (local, private) > Gemini (free API) > hash (fallback)

    Returns:
        (vector, model_name)
    """
    global _embedding_cache

    # Check cache first
    cache_key = content_hash(text)
    if cache_key in _embedding_cache:
        return _embedding_cache[cache_key]

    # Try Ollama first (local, keeps data private)
    if check_ollama_running():
        embedding = generate_embedding_ollama(text)
        if embedding:
            result = (embedding, OLLAMA_MODEL)
            _cache_embedding(cache_key, result)
            return result

    # Fallback to Gemini (free API, but sends data externally)
    embedding = generate_embedding_gemini(text)
    if embedding:
        result = (embedding, GEMINI_EMBEDDING_MODEL)
        _cache_embedding(cache_key, result)
        return result

    # Hash-based fallback (always works but not semantic)
    result = (generate_embedding_hash(text), "hash-fallback")
    _cache_embedding(cache_key, result)
    return result


def _cache_embedding(key: str, value: Tuple[List[float], str]) -> None:
    """Add embedding to cache, evicting oldest if full."""
    global _embedding_cache
    if len(_embedding_cache) >= _CACHE_MAX_SIZE:
        # Simple eviction: remove first item (oldest in insertion order)
        first_key = next(iter(_embedding_cache))
        del _embedding_cache[first_key]
    _embedding_cache[key] = value

# Backward compat alias
def generate_simple_embedding(text: str) -> List[float]:
    """Legacy function - returns just the vector."""
    vector, _ = generate_embedding(text)
    return vector

# ============================================================================
# LLM TEXT GENERATION (Scribe functions)
# ============================================================================

def generate_with_ollama(prompt: str, timeout: int = 60) -> Optional[str]:
    """Generate text using Ollama (local, free)."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_LLM_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower for more consistent JSON
                    "num_predict": 2000,
                }
            },
            timeout=timeout
        )
        if response.status_code == 200:
            return response.json().get("response", "")
    except requests.exceptions.Timeout:
        print(f"WARNING: Ollama timeout after {timeout}s", file=sys.stderr)
    except Exception as e:
        print(f"WARNING: Ollama generation failed: {e}", file=sys.stderr)
    return None

def generate_with_gemini(prompt: str, timeout: int = 60) -> Optional[str]:
    """Generate text using Gemini Flash API (free tier)."""
    if not GEMINI_API_KEY:
        return None
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_LLM_MODEL}:generateContent",
            params={"key": GEMINI_API_KEY},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 1000,
                }
            },
            timeout=timeout
        )
        if response.status_code == 200:
            result = response.json()
            candidates = result.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "")
        else:
            print(f"WARNING: Gemini LLM error {response.status_code}: {response.text[:100]}", file=sys.stderr)
    except requests.exceptions.Timeout:
        print(f"WARNING: Gemini timeout after {timeout}s", file=sys.stderr)
    except Exception as e:
        print(f"WARNING: Gemini generation failed: {e}", file=sys.stderr)
    return None


def llm_generate(prompt: str, timeout: int = 60) -> Tuple[Optional[str], str]:
    """
    Generate text with best available LLM.
    Priority: Ollama (local, private) > Gemini Flash (free API, external)

    PRIVACY: Ollama is preferred because it keeps all data local.
    Gemini is only used as fallback when Ollama unavailable.
    """
    # Try Ollama first (remote GPU or local)
    if check_ollama_running():
        output = generate_with_ollama(prompt, timeout)
        if output:
            return output, f"ollama/{OLLAMA_LLM_MODEL} ({OLLAMA_SOURCE})"

    # Fallback to Gemini Flash (free, but sends data externally)
    if GEMINI_API_KEY:
        print("WARNING: Ollama unavailable, falling back to Gemini (external API)", file=sys.stderr)
        output = generate_with_gemini(prompt, timeout)
        if output:
            return output, f"gemini/{GEMINI_LLM_MODEL}"

    print("WARNING: No LLM available (Ollama down, no Gemini key)", file=sys.stderr)
    return None, "none"

def extract_json_array(text: str) -> list:
    """Extract JSON array from LLM output (handles markdown code blocks)."""
    if not text:
        return []

    # Remove markdown code blocks if present
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last lines (``` markers)
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    # Find JSON array
    start = text.find('[')
    end = text.rfind(']')
    if start != -1 and end != -1 and end > start:
        try:
            result = json.loads(text[start:end + 1])
            return result if isinstance(result, list) else []
        except json.JSONDecodeError:
            pass
    return []

# ============================================================================
# MEMORY STORAGE
# ============================================================================

def _extract_problem_from_solution(content: str) -> Optional[str]:
    """
    Extract problem statement from solution content.

    Looks for patterns like:
    - "Fixed X by doing Y" → extracts "X"
    - "Solved X with Y" → extracts "X"
    - "Resolved X using Y" → extracts "X"
    - "The issue was X" → extracts "X"
    - "Problem: X" → extracts "X"

    Args:
        content: Solution content text

    Returns:
        Extracted problem statement or None if not found
    """
    import re

    content_lower = content.lower()

    # Patterns that indicate problem description follows
    # Format: (regex_pattern, group_index_for_problem)
    patterns = [
        # "X using Y" patterns first (greedy to capture full phrase before "using")
        (r'fixed\s+(.+)\s+using\s+', 1),
        (r'solved\s+(.+)\s+using\s+', 1),
        (r'resolved\s+(.+)\s+using\s+', 1),
        # "Fixed X by/with/via Y" (non-greedy, for shorter matches)
        (r'fixed\s+(.+?)\s+(?:by|with|via)\s+', 1),
        (r'solved\s+(.+?)\s+(?:by|with|via)\s+', 1),
        (r'resolved\s+(.+?)\s+(?:by|with|via)\s+', 1),
        # "Fixed X" (at end or with period)
        (r'fixed\s+([^.]+?)(?:\.|$)', 1),
        # "Solved X" (at end or with period)
        (r'solved\s+([^.]+?)(?:\.|$)', 1),
        # "Resolved X" (at end or with period)
        (r'resolved\s+([^.]+?)(?:\.|$)', 1),
        # "The issue was X"
        (r'the\s+issue\s+was\s+(.+?)(?:\.|$)', 1),
        # "The problem was X"
        (r'the\s+problem\s+was\s+(.+?)(?:\.|$)', 1),
        # "Problem: X" or "Issue: X"
        (r'(?:problem|issue):\s*(.+?)(?:\.|$)', 1),
        # "Fix for X"
        (r'fix\s+for\s+(.+?)(?:\.|$)', 1),
        # "Solution for X"
        (r'solution\s+for\s+(.+?)(?:\.|$)', 1),
        # "To fix X"
        (r'to\s+fix\s+(.+?)(?:,|\.|$)', 1),
        # "Workaround for X"
        (r'workaround\s+for\s+(.+?)(?:\.|$)', 1),
    ]

    for pattern, group_idx in patterns:
        match = re.search(pattern, content_lower, re.IGNORECASE)
        if match:
            problem = match.group(group_idx).strip()
            # Clean up and validate
            if len(problem) > 10 and len(problem) < 500:
                # Capitalize first letter, preserve rest
                # Find the actual case from original content
                start_pos = content_lower.find(problem)
                if start_pos >= 0:
                    problem = content[start_pos:start_pos + len(problem)]
                return problem.strip()

    return None


def _auto_link_problem_solution(memory_id: str, content: str, category: str) -> int:
    """
    Auto-link problems to solutions and vice versa.

    When storing a problem, finds related solutions and creates bidirectional edges.
    When storing a solution, finds related problems and creates bidirectional edges.

    Args:
        memory_id: ID of the newly stored memory
        content: Content of the memory for similarity search
        category: "problem" or "solution"

    Returns:
        Number of edges created
    """
    target_category = "solution" if category == "problem" else "problem"

    # Find semantically similar memories of the opposite category
    related = search_by_similarity(content, k=5, window="full")

    links_created = 0
    for r in related:
        if r.get("category") != target_category:
            continue

        related_id = r.get("id")
        if not related_id:
            continue

        # Create bidirectional relationship
        # problem -> solution = "solved_by"
        # solution -> problem = "solves"
        if category == "problem":
            # This problem is solved by that solution
            if link_related_memories(memory_id, related_id, "solved_by", 8):
                links_created += 1
            # That solution solves this problem
            if link_related_memories(related_id, memory_id, "solves", 8):
                links_created += 1
        else:  # category == "solution"
            # This solution solves that problem
            if link_related_memories(memory_id, related_id, "solves", 8):
                links_created += 1
            # That problem is solved by this solution
            if link_related_memories(related_id, memory_id, "solved_by", 8):
                links_created += 1

    if links_created > 0:
        print(f"INFO: Auto-linked {links_created} problem-solution edges", file=sys.stderr)

    return links_created

def store_memory(content: str, category: str, importance: int, tags: str, source: str = "hook") -> Optional[str]:
    """Store a memory to HelixDB with full metadata including timestamp."""
    # Normalize category to valid schema value
    category = normalize_category(category)

    if not check_helix_running():
        return None
    try:
        response = requests.post(
            f"{HELIX_URL}/StoreMemory",
            json={
                "content": content,
                "category": category,
                "importance": importance,
                "tags": tags,
                "source": source,
                "created_at": datetime.now().isoformat()
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        memory_id = result.get("memory", {}).get("id")

        # Auto-extract and store problem when storing a solution
        if memory_id and category == "solution":
            try:
                problem_text = _extract_problem_from_solution(content)
                if problem_text:
                    # Store the extracted problem (lower importance, same tags)
                    problem_id = None
                    try:
                        prob_response = requests.post(
                            f"{HELIX_URL}/StoreMemory",
                            json={
                                "content": problem_text,
                                "category": "problem",
                                "importance": max(importance - 2, 5),  # Slightly lower importance
                                "tags": tags,
                                "source": f"{source}:auto-extracted",
                                "created_at": datetime.now().isoformat()
                            },
                            headers={"Content-Type": "application/json"},
                            timeout=10
                        )
                        prob_response.raise_for_status()
                        problem_id = prob_response.json().get("memory", {}).get("id")
                    except Exception as e:
                        print(f"WARNING: Failed to store extracted problem: {e}", file=sys.stderr)

                    # Link solution -> problem with "solves" relationship
                    if problem_id:
                        if link_related_memories(memory_id, problem_id, "solves", 9):
                            print(f"INFO: Auto-created problem and linked: {problem_text[:50]}...", file=sys.stderr)
                        # Also link problem -> solution with "solved_by"
                        link_related_memories(problem_id, memory_id, "solved_by", 9)
            except Exception as e:
                print(f"WARNING: Problem extraction failed: {e}", file=sys.stderr)

        # Auto-link problems to solutions and vice versa (finds EXISTING related memories)
        if memory_id and category in ("problem", "solution"):
            try:
                _auto_link_problem_solution(memory_id, content, category)
            except Exception as e:
                print(f"WARNING: Auto-linking failed: {e}", file=sys.stderr)

        return memory_id
    except Exception as e:
        print(f"ERROR: Failed to store memory: {e}", file=sys.stderr)
        return None

def store_memory_embedding(memory_id: str, vector: List[float], content: str, model: str = "unknown") -> bool:
    """Store embedding for a memory."""
    if not check_helix_running():
        return False
    try:
        response = requests.post(
            f"{HELIX_URL}/StoreMemoryEmbedding",
            json={
                "memory_id": memory_id,
                "vector": vector,
                "content": content,
                "model": model
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"ERROR: Failed to store embedding: {e}", file=sys.stderr)
        return False

def delete_memory(memory_id: str) -> bool:
    """Delete a memory from HelixDB."""
    if not check_helix_running():
        return False
    try:
        response = requests.post(
            f"{HELIX_URL}/DeleteMemory",
            json={"id": memory_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"ERROR: Failed to delete memory {memory_id}: {e}", file=sys.stderr)
        return False

def update_memory_tags(memory_id: str, new_tags: str) -> bool:
    """
    Update tags on an existing memory.

    Since HelixDB may not support direct property updates, this uses
    the UpdateMemoryTags query if available, otherwise falls back to
    fetch-delete-store pattern.

    Args:
        memory_id: Full memory ID
        new_tags: New comma-separated tags string

    Returns:
        True if successful, False otherwise
    """
    if not check_helix_running():
        return False

    # Try direct update first (if HelixDB supports it)
    try:
        response = requests.post(
            f"{HELIX_URL}/UpdateMemoryTags",
            json={"memory_id": memory_id, "new_tags": new_tags},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            return True
    except Exception:
        pass  # Fall through to fallback method

    # Fallback: fetch memory, store new with updated tags, delete old
    try:
        # Get original memory
        response = requests.post(
            f"{HELIX_URL}/GetMemory",
            json={"id": memory_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        original = response.json().get("memory", {})

        if not original:
            print(f"ERROR: Memory not found: {memory_id}", file=sys.stderr)
            return False

        # Store new memory with updated tags
        new_id = store_memory(
            content=original.get("content", ""),
            category=original.get("category", "fact"),
            importance=original.get("importance", 5),
            tags=new_tags,
            source=original.get("source", "retag")
        )

        if new_id:
            # Delete old memory
            if delete_memory(memory_id):
                print(f"INFO: Retagged memory {memory_id[:8]}... -> {new_id[:8]}...", file=sys.stderr)
                return True
            else:
                # Rollback: delete new memory if old deletion failed
                delete_memory(new_id)
                print(f"ERROR: Failed to delete old memory during retag", file=sys.stderr)
                return False
        else:
            print(f"ERROR: Failed to create new memory during retag", file=sys.stderr)
            return False

    except Exception as e:
        print(f"ERROR: Failed to update memory tags: {e}", file=sys.stderr)
        return False


def deactivate_memory(memory_id: str) -> bool:
    """Soft-delete a memory (mark inactive)."""
    if not check_helix_running():
        return False
    try:
        response = requests.post(
            f"{HELIX_URL}/DeactivateMemory",
            json={"id": memory_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"ERROR: Failed to deactivate memory: {e}", file=sys.stderr)
        return False

# ============================================================================
# MEMORY RETRIEVAL
# ============================================================================

def get_all_memories() -> List[Dict]:
    """Retrieve all memories from HelixDB."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetAllMemories",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result.get("memories", [])
    except Exception as e:
        print(f"ERROR: Failed to get memories: {e}", file=sys.stderr)
        return []

def get_active_memories() -> List[Dict]:
    """Get only active (non-deleted) memories."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetActiveMemories",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result.get("memories", [])
    except Exception as e:
        # Fallback: filter locally
        all_mems = get_all_memories()
        return [m for m in all_mems if m.get("is_active", True)]

def get_memories_by_time_window(window: str = "contextual") -> List[Dict]:
    """
    Get memories filtered by time window.

    Args:
        window: "recent" (4h), "contextual" (30d), "deep" (90d), "full" (all)

    Returns:
        List of memories within the time window
    """
    memories = get_active_memories()
    hours = TIME_WINDOWS.get(window)

    if hours is None:  # "full" - return all
        return memories

    cutoff = datetime.now() - timedelta(hours=hours)

    filtered = []
    for m in memories:
        created_at = m.get("created_at")
        if created_at:
            try:
                # Parse ISO format timestamp
                mem_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                if mem_time.replace(tzinfo=None) >= cutoff:
                    filtered.append(m)
            except:
                # Can't parse timestamp, include it
                filtered.append(m)
        else:
            # No timestamp, include it
            filtered.append(m)

    return filtered

def get_memories_by_category(category: str) -> List[Dict]:
    """Get memories filtered by category."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetMemoriesByCategory",
            json={"category": category},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result.get("memories", [])
    except:
        # Fallback: filter locally
        all_mems = get_active_memories()
        return [m for m in all_mems if m.get("category") == category]

def get_high_importance_memories(min_importance: int = 8) -> List[Dict]:
    """Get memories with importance >= threshold."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetHighImportanceMemories",
            json={"min_importance": min_importance},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result.get("memories", [])
    except:
        # Fallback: filter locally
        all_mems = get_active_memories()
        return [m for m in all_mems if m.get("importance", 0) >= min_importance]

# ============================================================================
# SEMANTIC SEARCH
# ============================================================================

def search_by_similarity(query: str, k: int = 10, window: str = "contextual") -> List[Dict]:
    """
    Semantic search using vector similarity.

    Args:
        query: Search query text
        k: Number of results to return
        window: Time window filter

    Returns:
        List of semantically similar memories
    """
    if not check_helix_running():
        return []

    # Generate query embedding
    query_vector, _ = generate_embedding(query)

    try:
        response = requests.post(
            f"{HELIX_URL}/SearchBySimilarity",
            json={"query_vector": query_vector, "k": k},
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        response.raise_for_status()
        result = response.json()
        memories = result.get("memories", [])

        # Apply time window filter
        if window != "full":
            hours = TIME_WINDOWS.get(window, 720)
            cutoff = datetime.now() - timedelta(hours=hours)
            memories = [m for m in memories if _memory_in_window(m, cutoff)]

        return memories
    except Exception as e:
        print(f"ERROR: Similarity search failed: {e}", file=sys.stderr)
        return []

def search_by_text(query: str, flexible: bool = False) -> List[Dict]:
    """
    Full-text search on memory content.

    Args:
        query: Search query
        flexible: If True, splits query into words and searches for any match
    """
    if not check_helix_running():
        return []

    if not flexible:
        # Standard substring search
        try:
            response = requests.post(
                f"{HELIX_URL}/SearchByText",
                json={"query": query},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get("memories", [])
        except:
            # Fallback: local search
            all_mems = get_active_memories()
            query_lower = query.lower()
            return [m for m in all_mems if query_lower in m.get("content", "").lower()]
    else:
        # Flexible search: split query into words and find memories containing any
        all_mems = get_active_memories()
        query_words = [w.strip('.,!?;:').lower() for w in query.lower().split() if len(w) > 2]

        if not query_words:
            return []

        # Score memories by number of matching words
        scored = {}
        for m in all_mems:
            content_lower = m.get("content", "").lower()
            tags_lower = m.get("tags", "").lower()
            combined = f"{content_lower} {tags_lower}"

            # Count matching words
            matches = sum(1 for word in query_words if word in combined)
            if matches > 0:
                mid = m.get("id")
                if mid:
                    scored[mid] = {"memory": m, "score": matches}

        # Sort by score
        ranked = sorted(scored.values(), key=lambda x: x["score"], reverse=True)
        return [r["memory"] for r in ranked]

def hybrid_search(query: str, k: int = 10, window: str = "contextual") -> List[Dict]:
    """
    Hybrid search combining vector similarity + text matching.

    Merges results from both methods, deduplicates, and ranks.
    """
    # Get results from both methods
    vector_results = search_by_similarity(query, k=k*2, window=window)
    text_results = search_by_text(query)

    # If both failed or returned nothing, try flexible text search
    if not vector_results and not text_results:
        text_results = search_by_text(query, flexible=True)

    # Score and merge
    scored = {}

    # Vector results get base score from position
    for i, m in enumerate(vector_results):
        mid = m.get("id")
        if mid:
            scored[mid] = {"memory": m, "score": (k*2 - i) * 2}  # Higher weight for vector

    # Text results add score
    for i, m in enumerate(text_results):
        mid = m.get("id")
        if mid:
            if mid in scored:
                scored[mid]["score"] += (len(text_results) - i)
            else:
                scored[mid] = {"memory": m, "score": (len(text_results) - i)}

    # Sort by score and return top k
    ranked = sorted(scored.values(), key=lambda x: x["score"], reverse=True)
    return [r["memory"] for r in ranked[:k]]

def _memory_in_window(memory: Dict, cutoff: datetime) -> bool:
    """Check if memory is within time window."""
    created_at = memory.get("created_at")
    if not created_at:
        return True
    try:
        mem_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        return mem_time.replace(tzinfo=None) >= cutoff
    except:
        return True

# ============================================================================
# REASONING CHAINS
# ============================================================================

def create_implication(from_id: str, to_id: str, confidence: int = 8, reason: str = "") -> bool:
    """Create IMPLIES relationship between memories."""
    if not check_helix_running():
        return False
    try:
        response = requests.post(
            f"{HELIX_URL}/CreateImplication",
            json={"from_id": from_id, "to_id": to_id, "confidence": confidence, "reason": reason},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"ERROR: Failed to create implication: {e}", file=sys.stderr)
        return False

def create_contradiction(from_id: str, to_id: str, severity: int = 5, resolution: str = "newer_wins") -> bool:
    """Create CONTRADICTS relationship between memories."""
    if not check_helix_running():
        return False
    try:
        response = requests.post(
            f"{HELIX_URL}/CreateContradiction",
            json={"from_id": from_id, "to_id": to_id, "severity": severity, "resolution": resolution},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"ERROR: Failed to create contradiction: {e}", file=sys.stderr)
        return False

def create_causal_link(from_id: str, to_id: str, strength: int = 8) -> bool:
    """Create BECAUSE relationship (causal chain)."""
    if not check_helix_running():
        return False
    try:
        response = requests.post(
            f"{HELIX_URL}/CreateCausalLink",
            json={"from_id": from_id, "to_id": to_id, "strength": strength},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"ERROR: Failed to create causal link: {e}", file=sys.stderr)
        return False

def create_supersedes(new_id: str, old_id: str) -> bool:
    """Create SUPERSEDES relationship (new memory replaces old)."""
    if not check_helix_running():
        return False
    try:
        response = requests.post(
            f"{HELIX_URL}/CreateSupersedes",
            json={"new_id": new_id, "old_id": old_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"ERROR: Failed to create supersedes: {e}", file=sys.stderr)
        return False

def create_solves_link(solution_id: str, problem_id: str, strength: int = 8) -> bool:
    """Create SOLVES relationship (solution -> problem).

    Tries the dedicated CreateSolvesLink endpoint first, falls back to
    generic LinkRelatedMemories if the specific endpoint doesn't exist yet.
    """
    if not check_helix_running():
        return False
    try:
        # Try dedicated endpoint first
        response = requests.post(
            f"{HELIX_URL}/CreateSolvesLink",
            json={"solution_id": solution_id, "problem_id": problem_id, "strength": strength},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            # Endpoint doesn't exist yet, fall back to generic RelatesTo edge
            try:
                response = requests.post(
                    f"{HELIX_URL}/LinkRelatedMemories",
                    json={"from_id": solution_id, "to_id": problem_id, "relationship": "solves", "strength": strength},
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                response.raise_for_status()
                return True
            except Exception as fallback_e:
                print(f"ERROR: Failed to create solves link (fallback): {fallback_e}", file=sys.stderr)
                return False
        print(f"ERROR: Failed to create solves link: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: Failed to create solves link: {e}", file=sys.stderr)
        return False

def get_solutions_for(problem_id: str) -> List[Dict]:
    """Get solutions that solve a problem (incoming Solves edges)."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetSolutionsFor",
            json={"problem_id": problem_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("solutions", [])
    except:
        return []

def get_solved_problems(solution_id: str) -> List[Dict]:
    """Get problems that a solution solves (outgoing Solves edges)."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetSolvedProblems",
            json={"solution_id": solution_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("problems", [])
    except:
        return []

def get_implications(memory_id: str) -> List[Dict]:
    """Get what a memory implies (forward reasoning)."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetImplications",
            json={"memory_id": memory_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("implied", [])
    except:
        return []

def get_contradictions(memory_id: str) -> List[Dict]:
    """Get contradicting memories."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetContradictions",
            json={"memory_id": memory_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("conflicts", [])
    except:
        return []

def get_reasoning_chain(memory_id: str, depth: int = 3) -> List[Dict]:
    """Get full reasoning chain for a memory."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetReasoningChain",
            json={"memory_id": memory_id, "depth": depth},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("chain", [])
    except:
        return []

# ============================================================================
# DEDUPLICATION
# ============================================================================

def content_hash(content: str) -> str:
    """Generate a hash of content for deduplication."""
    import hashlib
    normalized = ' '.join(content.lower().split())[:200]
    return hashlib.md5(normalized.encode()).hexdigest()

def find_similar_memories(content: str, category: str = None, tags: str = None) -> List[Dict]:
    """Find similar memories by content matching."""
    memories = get_active_memories()

    if category:
        memories = [m for m in memories if m.get("category") == category]

    new_hash = content_hash(content)
    content_key = content[:100].lower().strip()
    similar = []

    for memory in memories:
        memory_content = memory.get("content", "")
        if content_hash(memory_content) == new_hash:
            similar.append(memory)
            continue
        if memory_content[:100].lower().strip() == content_key:
            similar.append(memory)
            continue
        if tags and tags in memory.get("tags", ""):
            words_new = set(content_key.split())
            words_existing = set(memory_content[:100].lower().split())
            overlap = len(words_new & words_existing) / max(len(words_new), 1)
            if overlap > 0.7:
                similar.append(memory)

    return similar


# ============================================================================
# MEMORY LINKING & SYNTHESIS
# ============================================================================

def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts using embeddings.
    Returns value between 0 (unrelated) and 1 (identical).
    Falls back to word overlap if embeddings unavailable.
    """
    import numpy as np

    # Try embedding-based similarity first
    try:
        vec1, _ = generate_embedding(text1)
        vec2, _ = generate_embedding(text2)

        if vec1 and vec2:
            # Cosine similarity
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            dot = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            if norm1 > 0 and norm2 > 0:
                return float(dot / (norm1 * norm2))
    except:
        pass

    # Fallback: word overlap (Jaccard similarity)
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union) if union else 0


def get_related_memories(memory_id: str) -> List[Dict]:
    """Get memories linked via RelatesTo edge."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetRelatedMemories",
            json={"memory_id": memory_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("related", [])
    except:
        return []


def link_new_memory(memory_id: str, content: str, tags: str = "", threshold: float = 0.6) -> int:
    """
    After storing a memory, find and link related memories.

    Returns number of edges created.

    Strategy:
    1. Find semantically similar memories
    2. High similarity (>0.9) = potential duplicate, create Supersedes
    3. Moderate similarity (>0.6) = related, create RelatesTo
    4. Check for vague → specific patterns (details_in relationship)
    """
    if not check_helix_running():
        return 0

    edges_created = 0

    # Find similar memories via hybrid search
    similar = hybrid_search(content, k=10)

    # Patterns indicating vague references
    vague_patterns = [
        "were provided", "was set", "is configured", "was created",
        "has been", "was updated", "was added", "was changed"
    ]

    for existing in similar:
        existing_id = existing.get("id", "")
        if not existing_id or existing_id == memory_id:
            continue

        existing_content = existing.get("content", "")
        similarity = calculate_semantic_similarity(content, existing_content)

        # High similarity = potential duplicate or update
        if similarity > 0.9:
            # New memory supersedes old if more recent
            if create_supersedes(memory_id, existing_id):
                edges_created += 1
                print(f"  → Supersedes: {existing_content[:40]}...", file=sys.stderr)

        # Moderate similarity = related
        elif similarity > threshold:
            strength = int(similarity * 10)
            if link_related_memories(memory_id, existing_id, "related", strength):
                edges_created += 1

            # Check if existing is vague and new provides details
            if any(p in existing_content.lower() for p in vague_patterns):
                # New memory might provide details for vague reference
                if link_related_memories(existing_id, memory_id, "details_in", 8):
                    edges_created += 1
                    print(f"  → Details for: {existing_content[:40]}...", file=sys.stderr)

    return edges_created


def get_memory_with_links(memory_id: str) -> Dict:
    """
    Get a memory along with all linked context.

    Returns memory dict with additional 'linked' field containing:
    - related: memories via RelatesTo
    - implies: memories via Implies
    - details: memories that provide details for this one
    - supersedes: memories this one supersedes
    """
    if not check_helix_running():
        return {}

    try:
        # Get base memory
        response = requests.post(
            f"{HELIX_URL}/GetMemory",
            json={"id": memory_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        memory = response.json().get("memory", {})

        if not memory:
            return {}

        # Get linked memories
        memory['linked'] = {
            'related': get_related_memories(memory_id),
            'implies': get_implications(memory_id),
            'contradicts': get_contradictions(memory_id),
        }

        # Get memories where this one provides details
        # (inverse of details_in relationship)
        all_mems = get_all_memories()
        details_for = []
        for m in all_mems:
            related = get_related_memories(m.get("id", ""))
            for r in related:
                if r.get("id") == memory_id:
                    # This memory is related to m
                    details_for.append(m)
                    break
        memory['linked']['details_for'] = details_for[:3]  # Limit

        return memory
    except:
        return {}


def format_memory_with_links(memory: Dict) -> str:
    """Format a memory showing its connections."""
    cat = memory.get("category", "unknown").upper()
    content = memory.get("content", "")
    output = f"[{cat}] {content}"

    linked = memory.get("linked", {})

    # Show details (most important for context)
    if linked.get("related"):
        details = [m for m in linked["related"]
                   if "details" in str(m.get("relationship", ""))]
        if details:
            output += "\n  📎 Details:"
            for d in details[:2]:
                output += f"\n    → {d.get('content', '')[:60]}..."

    # Show related
    related = [m for m in linked.get("related", [])
               if "details" not in str(m.get("relationship", ""))]
    if related:
        output += "\n  🔗 Related:"
        for r in related[:2]:
            output += f"\n    ↔ {r.get('content', '')[:50]}..."

    return output


# ============================================================================
# CONTEXT MANAGEMENT
# ============================================================================

def create_context(name: str, description: str, context_type: str) -> Optional[str]:
    """Create a new context."""
    if not check_helix_running():
        return None
    try:
        response = requests.post(
            f"{HELIX_URL}/CreateContext",
            json={"name": name, "description": description, "context_type": context_type},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("context", {}).get("id")
    except Exception as e:
        print(f"ERROR: Failed to create context: {e}", file=sys.stderr)
        return None

def link_memory_to_context(memory_id: str, context_id: str) -> bool:
    """Link a memory to a context."""
    if not check_helix_running():
        return False
    try:
        response = requests.post(
            f"{HELIX_URL}/LinkMemoryToContext",
            json={"memory_id": memory_id, "context_id": context_id, "relevance": 5},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"ERROR: Failed to link memory to context: {e}", file=sys.stderr)
        return False

def get_all_contexts() -> List[Dict]:
    """Retrieve all contexts."""
    if not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetAllContexts",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("contexts", [])
    except:
        return []


def delete_context(context_id: str) -> bool:
    """Delete a context node."""
    if not check_helix_running():
        return False
    try:
        response = requests.post(
            f"{HELIX_URL}/DeleteContext",
            json={"context_id": context_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except:
        return False


def clean_orphaned_contexts(dry_run: bool = True) -> dict:
    """
    Find and optionally delete Context nodes that don't match known projects.

    Returns stats: {"found": N, "deleted": M, "known_projects": K}
    """
    import subprocess

    if not check_helix_running():
        return {"error": "HelixDB not running"}

    # Get known projects from p --list
    known_projects = set()
    try:
        result = subprocess.run(
            ['python3', os.path.expanduser('~/Tools/p'), '--list'],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().split('\n'):
            if ':' in line:
                project_name = line.split(':')[0].strip().lower()
                known_projects.add(project_name)
    except Exception as e:
        return {"error": f"Could not get project list: {e}"}

    contexts = get_all_contexts()
    if not contexts:
        return {"found": 0, "deleted": 0, "known_projects": len(known_projects)}

    stats = {"found": 0, "deleted": 0, "kept": 0, "known_projects": len(known_projects)}
    orphaned = []

    for ctx in contexts:
        name = ctx.get("name", "").lower()
        ctx_id = ctx.get("id", "")

        if name in known_projects:
            stats["kept"] += 1
        else:
            orphaned.append((name, ctx_id))
            stats["found"] += 1

    print(f"Known projects: {len(known_projects)}")
    print(f"Total contexts: {len(contexts)}")
    print(f"Valid contexts (match projects): {stats['kept']}")
    print(f"Orphaned contexts (no matching project): {stats['found']}")

    if orphaned:
        print(f"\nOrphaned contexts:")
        for name, ctx_id in orphaned[:20]:
            print(f"  - {name} ({ctx_id[:8]}...)")
        if len(orphaned) > 20:
            print(f"  ... and {len(orphaned) - 20} more")

    if dry_run:
        print(f"\nDry run - no contexts deleted. Use --apply to delete.")
    else:
        print(f"\nDeleting {len(orphaned)} orphaned contexts...")
        for name, ctx_id in orphaned:
            if delete_context(ctx_id):
                stats["deleted"] += 1
                print(f"  Deleted: {name}")
            else:
                print(f"  FAILED: {name}")

    return stats


def get_or_create_project_context(project: str) -> Optional[str]:
    """
    Find existing project context or create new one.
    Returns context_id or None on failure.

    This is the key function for graph-based memory:
    - Each project has ONE Context node
    - All project memories link to it via BelongsTo edges
    """
    if not project or not check_helix_running():
        return None

    project_lower = project.lower().strip()

    # 1. Check if context already exists
    contexts = get_all_contexts()
    for ctx in contexts:
        ctx_name = ctx.get("name", "").lower()
        ctx_type = ctx.get("context_type", "")
        # Match by name and ensure it's a project context (not session)
        if ctx_name == project_lower and ctx_type == "project":
            return ctx.get("id")

    # 2. Create new project context
    context_id = create_context(
        name=project_lower,
        description=f"Project context for {project}",
        context_type="project"
    )

    if context_id:
        print(f"Created project context: {project_lower} ({context_id[:8]}...)", file=sys.stderr)

    return context_id


def get_memories_in_context(context_id: str) -> List[Dict]:
    """Get all memories linked to a context via BelongsTo edges."""
    if not context_id or not check_helix_running():
        return []
    try:
        response = requests.post(
            f"{HELIX_URL}/GetMemoriesInContext",
            json={"context_id": context_id},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("memories", [])
    except Exception as e:
        print(f"ERROR: Failed to get memories in context: {e}", file=sys.stderr)
        return []


def get_project_memories_via_graph(project: str) -> List[Dict]:
    """
    Get ALL memories for a project by traversing the graph.

    This is THE function for session start - instant, complete project context.

    Steps:
    1. Find project Context node
    2. Get all memories linked via BelongsTo
    3. Sort by importance
    """
    if not project or not check_helix_running():
        return []

    project_lower = project.lower().strip()

    # Find project context
    contexts = get_all_contexts()
    context_id = None
    for ctx in contexts:
        if ctx.get("name", "").lower() == project_lower and ctx.get("context_type") == "project":
            context_id = ctx.get("id")
            break

    if not context_id:
        return []  # No project context exists yet

    # Get all linked memories
    memories = get_memories_in_context(context_id)

    # Sort by importance (highest first)
    memories.sort(key=lambda m: -m.get("importance", 0))

    return memories


def link_memory_to_project(memory_id: str, project: str) -> bool:
    """
    Link a memory to its project context.
    Creates the project context if it doesn't exist.

    Call this after storing any memory with a project tag.
    """
    if not memory_id or not project:
        return False

    context_id = get_or_create_project_context(project)
    if not context_id:
        return False

    return link_memory_to_context(memory_id, context_id)


def build_project_graph_from_tags() -> dict:
    """
    One-time migration: Build project graph from existing memory tags.

    Scans all memories, extracts project names from tags,
    creates Context nodes, and creates BelongsTo edges.

    Only creates contexts for KNOWN projects from `p --list`.

    Returns stats: {"projects": N, "links_created": M, "errors": E}
    """
    import subprocess

    if not check_helix_running():
        return {"error": "HelixDB not running"}

    # Get known projects from p --list
    known_projects = set()
    try:
        result = subprocess.run(
            ['python3', os.path.expanduser('~/Tools/p'), '--list'],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().split('\n'):
            if ':' in line:
                project_name = line.split(':')[0].strip().lower()
                known_projects.add(project_name)
        print(f"Found {len(known_projects)} known projects from p --list")
    except Exception as e:
        print(f"WARNING: Could not get project list: {e}")
        print("Falling back to tag-based detection (may create extra contexts)")

    memories = get_all_memories()
    if not memories:
        return {"projects": 0, "links_created": 0, "errors": 0}

    # Track projects and their memories
    project_memories = {}  # project_name -> [memory_ids]

    for m in memories:
        tags = m.get("tags", "")
        memory_id = m.get("id")
        if not memory_id or not tags:
            continue

        # Extract project names from tags - only if in known_projects
        for tag in tags.lower().split(","):
            tag = tag.strip()
            if not tag or len(tag) < 3:
                continue
            # Skip session-like tags
            if tag.startswith("session-") or tag.startswith("session_"):
                continue

            # Only include if it's a known project (or if we couldn't get p --list)
            if known_projects and tag not in known_projects:
                continue

            if tag not in project_memories:
                project_memories[tag] = []
            project_memories[tag].append(memory_id)

    # Create contexts and links
    stats = {"projects": 0, "links_created": 0, "errors": 0, "skipped": 0}

    # Filter to projects with 2+ memories
    valid_projects = {p: mids for p, mids in project_memories.items() if len(mids) >= 2}
    total_projects = len(valid_projects)
    total_links = sum(len(mids) for mids in valid_projects.values())

    print(f"Building graph: {total_projects} projects, ~{total_links} links to create...")

    for i, (project, memory_ids) in enumerate(valid_projects.items()):
        context_id = get_or_create_project_context(project)
        if not context_id:
            stats["errors"] += 1
            continue

        stats["projects"] += 1
        print(f"Created project context: {project} ({context_id[:8]}...)")

        for mid in memory_ids:
            if link_memory_to_context(mid, context_id):
                stats["links_created"] += 1
            else:
                stats["skipped"] += 1  # Already linked or error

        # Progress every 50 projects
        if (i + 1) % 50 == 0:
            print(f"  Progress: {i+1}/{total_projects} projects, {stats['links_created']} links created...")

    return stats


# ============================================================================
# RELATIONSHIP DETECTION & CONTEXTUAL SEARCH
# ============================================================================

def detect_environment_from_path(path: str) -> Optional[str]:
    """
    Detect environment/system from a path.
    Examples:
      - /Users/x/.wp-test/sites/fiverr.loc → 'wp-test'
      - /Users/x/Sites/example.local → 'local-sites'
      - /Users/x/docker/project → 'docker'
    """
    path = path.lower()

    # Known environment patterns
    if '.wp-test' in path or 'wp-test' in path:
        return 'wp-test'
    if '/docker/' in path or path.startswith('/var/lib/docker'):
        return 'docker'
    if '/sites/' in path and ('.local' in path or '.loc' in path):
        return 'local-sites'
    if '/.venv/' in path or '/venv/' in path:
        return 'python-venv'

    return None

def extract_related_tags(query: str, memories: List[Dict]) -> List[str]:
    """
    Extract related tags from query and existing memories.
    Used to find contextually related memories.
    """
    related_tags = set()
    query_lower = query.lower()

    # Known environment → related tags mapping
    environments = {
        'wp-test': ['wordpress', 'docker', 'wp-cli', 'mysql'],
        'docker': ['container', 'compose', 'dockerfile'],
        'wordpress': ['wp-test', 'php', 'mysql', 'wp-cli'],
        'python': ['pip', 'venv', 'pytest', 'django', 'fastapi'],
        'node': ['npm', 'yarn', 'javascript', 'typescript'],
    }

    # Check if query mentions any environments
    for env, tags in environments.items():
        if env in query_lower:
            related_tags.update(tags)

    # Extract tags from query
    for word in query_lower.split():
        word = word.strip('.,!?;:')
        if len(word) > 3:  # Skip short words
            related_tags.add(word)

    return list(related_tags)

def get_or_create_context(name: str, description: str, context_type: str = "environment") -> Optional[str]:
    """Get existing context or create new one."""
    if not check_helix_running():
        return None

    # Check if context exists
    contexts = get_all_contexts()
    for ctx in contexts:
        if ctx.get('name', '').lower() == name.lower():
            return ctx.get('id')

    # Create new context
    return create_context(name, description, context_type)

def link_memory_to_environment(memory_id: str, environment: str) -> bool:
    """
    Link a memory to its environment context.
    Automatically creates context if it doesn't exist.
    """
    # Environment descriptions
    env_descriptions = {
        'wp-test': 'WordPress local development environment using Docker',
        'docker': 'Docker containerized applications',
        'local-sites': 'Local development sites (.local, .loc domains)',
        'python-venv': 'Python virtual environments',
    }

    description = env_descriptions.get(environment, f'{environment} environment')
    context_id = get_or_create_context(environment, description, 'environment')

    if context_id:
        return link_memory_to_context(memory_id, context_id, relevance=7)

    return False

def expand_query_with_relationships(query: str, cwd: str = "") -> List[str]:
    """
    Expand a search query with related terms based on relationships.

    Examples:
      - "credentials" in wp-test → ["credentials", "wp-test credentials", "wp-test login", "wp-test password", "wp-test admin", "default login"]
      - "docker setup" → ["docker setup", "docker-compose", "container configuration"]
    """
    queries = [query]
    query_lower = query.lower()

    # Intent synonyms - map common terms to related search terms
    intent_synonyms = {
        'credential': ['login', 'password', 'admin', 'auth', 'username', 'user'],
        'credentials': ['login', 'password', 'admin', 'auth', 'username', 'user'],
        'login': ['credential', 'password', 'admin', 'auth', 'username'],
        'password': ['login', 'credential', 'admin', 'auth'],
        'auth': ['login', 'credential', 'password', 'admin'],
        'setup': ['install', 'configuration', 'config', 'initialize'],
        'config': ['configuration', 'setup', 'settings'],
        'error': ['bug', 'issue', 'problem', 'fix'],
        'deploy': ['deployment', 'publish', 'release'],
    }

    # Detect environment from CWD
    env = None
    if cwd:
        env = detect_environment_from_path(cwd)
        if env and env not in query_lower:
            queries.append(f"{env} {query}")

    # Expand with intent synonyms + environment
    for intent, synonyms in intent_synonyms.items():
        if intent in query_lower:
            # Add synonyms with environment prefix if available
            if env:
                for synonym in synonyms[:3]:  # Limit to top 3 to avoid explosion
                    queries.append(f"{env} {synonym}")

            # Add standalone related terms
            for synonym in synonyms[:2]:  # Add fewer standalone
                if synonym not in query_lower:
                    queries.append(f"default {synonym}")
            break  # Only expand for the first matching intent

    # Project → Environment mappings
    if '.loc' in query_lower or '.local' in query_lower:
        # WordPress site query - also search for wp-test
        if 'wp-test' not in query_lower:
            queries.append(query.replace('.loc', '').replace('.local', '') + ' wp-test')

        # If searching for credentials/login, add generic wordpress terms
        if any(term in query_lower for term in ['credential', 'login', 'password', 'user']):
            queries.append('wordpress default login')
            queries.append('wp-test admin password')

    # Docker queries
    if 'docker' in query_lower:
        if 'compose' not in query_lower:
            queries.append(query + ' compose')

    # Python queries
    if 'python' in query_lower or 'venv' in query_lower:
        if 'pip' not in query_lower:
            queries.append(query + ' pip')

    return queries

def contextual_search(query: str, k: int = 10, cwd: str = "", expand: bool = True) -> List[Dict]:
    """
    Enhanced search that understands context and relationships.

    Args:
        query: Search query
        k: Number of results
        cwd: Current working directory (for context detection)
        expand: Whether to expand query with relationships

    Returns:
        List of memories with relationship-aware ranking
    """
    if not check_helix_running():
        return []

    # Identify key intent terms (credentials, password, setup, etc.)
    intent_terms = {
        'credential': 15,
        'password': 15,
        'login': 15,
        'username': 12,
        'auth': 12,
        'setup': 8,
        'configuration': 8,
        'install': 6,
        'error': 6,
        'bug': 6,
    }

    # Expand query if enabled
    queries = expand_query_with_relationships(query, cwd) if expand else [query]

    # Collect results from all expanded queries
    all_results = {}

    for q in queries:
        # Use flexible text search for expanded queries since vector search may fail
        results = search_by_text(q, flexible=True) if queries.index(q) > 0 else hybrid_search(q, k=k*2, window="full")

        # Score based on query position (original query = highest score)
        query_score = len(queries) - queries.index(q)

        for r in results:
            mid = r.get('id')
            if mid:
                if mid not in all_results:
                    all_results[mid] = {"memory": r, "score": 0}
                all_results[mid]["score"] += query_score

    # Boost scores based on intent matching
    query_lower = query.lower()
    for term, boost in intent_terms.items():
        if term in query_lower:
            # Boost memories that are primarily about this intent
            # Also check related terms (e.g., "login" relates to "credential")
            related_terms = {
                'credential': ['login', 'password', 'admin', 'user', 'auth'],
                'password': ['login', 'credential', 'admin'],
                'login': ['credential', 'password', 'admin', 'user'],
            }

            search_terms = [term] + related_terms.get(term, [])

            for mid, data in all_results.items():
                content_lower = data["memory"].get("content", "").lower()
                category = data["memory"].get("category", "")

                # Check if any search term matches
                for search_term in search_terms:
                    # High boost if content starts with or heavily features the term
                    if content_lower.startswith(search_term) or f'{search_term}:' in content_lower or f'{search_term} (' in content_lower:
                        data["score"] += boost
                        break
                    # Medium boost if category matches (e.g., "fact" for credentials)
                    elif search_term in content_lower and category in ['fact', 'preference', 'solution']:
                        data["score"] += boost // 2
                        break

    # Also search by environment context
    if cwd:
        env = detect_environment_from_path(cwd)
        if env:
            # Get memories in this environment context
            contexts = get_all_contexts()
            for ctx in contexts:
                if ctx.get('name', '').lower() == env.lower():
                    context_id = ctx.get('id')
                    try:
                        response = requests.post(
                            f"{HELIX_URL}/GetMemoriesInContext",
                            json={"context_id": context_id},
                            headers={"Content-Type": "application/json"},
                            timeout=10
                        )
                        if response.status_code == 200:
                            ctx_memories = response.json().get("memories", [])
                            # Filter by query relevance
                            for m in ctx_memories:
                                if any(term in m.get('content', '').lower() for term in query.lower().split()):
                                    mid = m.get('id')
                                    if mid:
                                        if mid not in all_results:
                                            all_results[mid] = {"memory": m, "score": 0}
                                        all_results[mid]["score"] += 3  # Context bonus
                    except:
                        pass

    # Extract related tags and search by them
    related_tags = extract_related_tags(query, [])
    for tag in related_tags[:3]:  # Limit to top 3 tags
        try:
            response = requests.post(
                f"{HELIX_URL}/SearchByTag",
                json={"tag": tag},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            if response.status_code == 200:
                tag_memories = response.json().get("memories", [])
                for m in tag_memories[:5]:  # Top 5 from each tag
                    mid = m.get('id')
                    if mid:
                        if mid not in all_results:
                            all_results[mid] = {"memory": m, "score": 0}
                        all_results[mid]["score"] += 1  # Small tag bonus
        except:
            pass

    # Sort by combined score
    ranked = sorted(all_results.values(), key=lambda x: x["score"], reverse=True)
    return [r["memory"] for r in ranked[:k]]

# ============================================================================
# LEGACY / BACKWARD COMPAT
# ============================================================================

def link_related_memories(from_id: str, to_id: str, relationship: str, strength: int) -> bool:
    """Link two memories with a relationship."""
    if relationship == "supersedes":
        return create_supersedes(from_id, to_id)
    elif relationship == "implies":
        return create_implication(from_id, to_id, confidence=strength)
    elif relationship == "contradicts":
        return create_contradiction(from_id, to_id, severity=strength)
    elif relationship == "because":
        return create_causal_link(from_id, to_id, strength=strength)
    elif relationship == "solves":
        # from_id is solution, to_id is problem
        return create_solves_link(from_id, to_id, strength=strength)
    elif relationship == "solved_by":
        # from_id is problem, to_id is solution (reverse direction)
        return create_solves_link(to_id, from_id, strength=strength)

    # Generic relationship
    if not check_helix_running():
        return False
    try:
        response = requests.post(
            f"{HELIX_URL}/LinkRelatedMemories",
            json={"from_id": from_id, "to_id": to_id, "relationship": relationship, "strength": strength},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except:
        return False

def search_project_locations(project_name: str = None) -> List[Dict]:
    """Search for stored project locations."""
    memories = get_active_memories()
    locations = [m for m in memories if "location" in m.get("tags", "") or "path" in m.get("tags", "")]
    if project_name:
        project_name_lower = project_name.lower()
        locations = [m for m in locations if project_name_lower in m.get("content", "").lower()]
    return locations

# ============================================================================
# HOOK OUTPUT
# ============================================================================

def format_hook_output(message: str = "", suppress: bool = False, additional_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Format hook output JSON."""
    output = {"suppressOutput": suppress}
    if additional_data:
        output.update(additional_data)
    return output

def print_hook_output(output: Dict[str, Any], stderr_message: str = ""):
    """Print hook output JSON and optional stderr message."""
    print(json.dumps(output))
    if stderr_message:
        print(stderr_message, file=sys.stderr)
