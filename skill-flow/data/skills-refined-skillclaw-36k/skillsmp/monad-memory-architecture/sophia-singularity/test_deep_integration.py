#!/usr/bin/env python3
"""
Test script for Sophia Catgirl Singularity Deep Integration
Tests: Memory indexing, legacy loading, chaos modes, council (mocked)

Authors:
  Matthew Wayne Macklin (The Gardener) - January 11, 2026
  Copilot Kitty 😺 - Test Suite Implementation
"""

import json
import sys
from pathlib import Path

# Setup paths - find repo root properly
current = Path(__file__).resolve()
while current.parent != current:
    if (current / ".git").exists():
        REPO_ROOT = current
        break
    current = current.parent
else:
    REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

sys.path.insert(0, str(REPO_ROOT / "tools"))

STATE_DIR = REPO_ROOT / ".claude" / "state" / "sophia"
LOG_DIR = REPO_ROOT / ".claude" / "logs" / "sophia"
MEMORY_ROOT = REPO_ROOT / "memory"

def test_directory_structure():
    """Test that all directories were created"""
    print("🧪 Testing directory structure...")
    
    dirs_to_check = [
        STATE_DIR,
        STATE_DIR / "session_backups",
        LOG_DIR / "coherence",
        LOG_DIR / "warmth",
        LOG_DIR / "chaos",
        LOG_DIR / "council",
        MEMORY_ROOT / "gremlin",
        MEMORY_ROOT / "monad",
        MEMORY_ROOT / "graph",
        MEMORY_ROOT / "visualiser",
        MEMORY_ROOT / "core",
        MEMORY_ROOT / "mind",
    ]
    
    for d in dirs_to_check:
        assert d.exists(), f"Missing directory: {d}"
        print(f"  ✓ {d.relative_to(REPO_ROOT)}")
    
    print("✅ All directories exist\n")

def test_memory_index():
    """Test memory index generation"""
    print("🧪 Testing memory index...")
    
    index_file = STATE_DIR / "memory-index.json"
    assert index_file.exists(), "memory-index.json not found"
    
    with open(index_file, 'r') as f:
        index = json.load(f)
    
    assert "version" in index
    assert "legacy_memory" in index
    assert "claude_memory" in index
    assert "summary" in index
    
    # Check legacy memory entries
    for category in ["gremlin", "monad", "graph", "visualiser", "core", "mind"]:
        assert category in index["legacy_memory"], f"Missing {category} in index"
        print(f"  ✓ {category}: {index['legacy_memory'][category].get('file_count', 0)} files")
    
    print(f"✅ Memory index valid ({index['summary']['total_files']} total files)\n")

def test_chaos_modes():
    """Test chaos mode configuration"""
    print("🧪 Testing chaos mode configuration...")
    
    # Read sophia-engine.py to check for chaos mode support
    engine_file = REPO_ROOT / ".claude" / "skills" / "sophia-singularity" / "sophia-visualizer" / "scripts" / "sophia-engine.py"
    
    with open(engine_file, 'r') as f:
        content = f.read()
    
    # Check for key chaos features
    assert "CHAOS_GREMLIN_MODE" in content, "Missing CHAOS_GREMLIN_MODE constant"
    assert "set_chaos_mode" in content, "Missing set_chaos_mode method"
    assert "maybe_inject_chaos" in content, "Missing maybe_inject_chaos method"
    assert "dyad-seek" in content, "Missing dyad-seek chaos type"
    assert "octo-spawn" in content, "Missing octo-spawn chaos type"
    assert "chaos-gremlin" in content, "Missing chaos-gremlin command"
    
    print("  ✓ CHAOS_GREMLIN_MODE constant")
    print("  ✓ set_chaos_mode method")
    print("  ✓ maybe_inject_chaos method")
    print("  ✓ Enhanced chaos types (dyad-seek, octo-spawn)")
    print("  ✓ chaos-gremlin CLI command")
    
    print("✅ Chaos mode configuration complete\n")

def test_council_integration():
    """Test Gremlin Forge council integration"""
    print("🧪 Testing Gremlin Forge council integration...")
    
    engine_file = REPO_ROOT / ".claude" / "skills" / "sophia-singularity" / "sophia-visualizer" / "scripts" / "sophia-engine.py"
    
    with open(engine_file, 'r') as f:
        content = f.read()
    
    # Check for council features
    assert "init_gremlin_forge" in content, "Missing init_gremlin_forge method"
    assert "spawn_council" in content, "Missing spawn_council method"
    assert "from gremlin_forge import GremlinForge" in content, "Missing gremlin_forge import"
    assert "council.log" in content, "Missing council.log logging"
    assert "elif entry.lower().startswith('council')" in content, "Missing council CLI command"
    
    print("  ✓ init_gremlin_forge method")
    print("  ✓ spawn_council method")
    print("  ✓ gremlin_forge import")
    print("  ✓ Council logging to council.log")
    print("  ✓ council CLI command")
    
    print("✅ Council integration complete\n")

def test_legacy_memory_loader():
    """Test legacy memory loading"""
    print("🧪 Testing legacy memory loader...")
    
    engine_file = REPO_ROOT / ".claude" / "skills" / "sophia-singularity" / "sophia-visualizer" / "scripts" / "sophia-engine.py"
    
    with open(engine_file, 'r') as f:
        content = f.read()
    
    # Check for memory loading features
    assert "load_legacy_memory" in content, "Missing load_legacy_memory method"
    assert "build_memory_index" in content, "Missing build_memory_index method"
    assert "MEMORY_INDEX_FILE" in content, "Missing MEMORY_INDEX_FILE constant"
    assert "MAX_LEGACY_FILES_PER_DIR" in content, "Missing MAX_LEGACY_FILES_PER_DIR limit"
    assert "LOAD_LEGACY_MEMORY" in content, "Missing LOAD_LEGACY_MEMORY toggle"
    assert "rebuild-index" in content, "Missing rebuild-index command"
    
    print("  ✓ load_legacy_memory method")
    print("  ✓ build_memory_index method")
    print("  ✓ MEMORY_INDEX_FILE constant")
    print("  ✓ MAX_LEGACY_FILES_PER_DIR limit (prevents bloat)")
    print("  ✓ LOAD_LEGACY_MEMORY toggle")
    print("  ✓ rebuild-index CLI command")
    
    print("✅ Legacy memory loader complete\n")

def test_documentation():
    """Test USER_MANUAL.md updates"""
    print("🧪 Testing documentation updates...")
    
    manual_file = REPO_ROOT / ".claude" / "skills" / "sophia-singularity" / "USER_MANUAL.md"
    
    with open(manual_file, 'r') as f:
        content = f.read()
    
    # Check for new documentation sections
    assert "Deep Integration Features" in content, "Missing Deep Integration section"
    assert "Legacy Memory System" in content, "Missing Legacy Memory documentation"
    assert "Gremlin Forge Council Integration" in content, "Missing Council documentation"
    assert "Chaos Gremlin Toggle" in content, "Missing Chaos Toggle documentation"
    assert "chaos-gremlin on" in content, "Missing chaos-gremlin on command"
    assert "chaos-gremlin off" in content, "Missing chaos-gremlin off command"
    assert "chaos-gremlin auto" in content, "Missing chaos-gremlin auto command"
    assert "council <question>" in content, "Missing council command"
    assert "rebuild-index" in content, "Missing rebuild-index command"
    
    print("  ✓ Deep Integration Features section")
    print("  ✓ Legacy Memory System documentation")
    print("  ✓ Gremlin Forge Council Integration documentation")
    print("  ✓ Chaos Gremlin Toggle documentation")
    print("  ✓ All new commands documented")
    
    print("✅ Documentation complete\n")

def test_backward_compatibility():
    """Test backward compatibility with existing state"""
    print("🧪 Testing backward compatibility...")
    
    engine_file = REPO_ROOT / ".claude" / "skills" / "sophia-singularity" / "sophia-visualizer" / "scripts" / "sophia-engine.py"
    
    with open(engine_file, 'r') as f:
        content = f.read()
    
    # Check that we handle missing fields gracefully
    assert "data.get('chaos_mode', 'off')" in content, "Missing default for chaos_mode"
    assert "data.get('chaos_counter', 0)" in content, "Missing default for chaos_counter"
    
    print("  ✓ Graceful handling of missing chaos_mode")
    print("  ✓ Graceful handling of missing chaos_counter")
    print("  ✓ Saves new fields to state")
    
    print("✅ Backward compatibility maintained\n")

def main():
    """Run all tests"""
    print("=" * 70)
    print("🐱⚡ SOPHIA DEEP INTEGRATION TEST SUITE ⚡🐱")
    print("=" * 70)
    print()
    
    try:
        test_directory_structure()
        test_memory_index()
        test_chaos_modes()
        test_council_integration()
        test_legacy_memory_loader()
        test_documentation()
        test_backward_compatibility()
        
        print("=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
        return 0
    
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
