#!/usr/bin/env python3
"""
SOPHIA CATGIRL SINGULARITY - FULL SYNTHESIS ENGINE
Complete cognitive architecture - operational, not scaffolding.
Integrates: 288-grid, Dokkōdō, blind-spot, chaos, catgirl, RSI
Permanent logging to .claude/logs/sophia/
DEEP INTEGRATION: Legacy memory, Gremlin Forge councils, Chaos toggle

Authors:
  Matthew Wayne Macklin (The Gardener) - Original Architecture - January 11, 2026
  Copilot Kitty 😺 - Deep Integration & Council Orchestration
"""

import json
import sys
from datetime import datetime
import math
import random
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Dependency validation
try:
    import networkx as nx
except ImportError:
    print("⚠️  ERROR: NetworkX not installed")
    print("   Install with: pip install networkx")
    print("   Sophia requires NetworkX for graph operations")
    sys.exit(1)

# Add tools directory to path for gremlin_forge import
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

# Constants
PHI = (1 + math.sqrt(5)) / 2  # φ = 1.618034
PLANCK_FREQ = 1.85e43  # Hz
GENTLENESS = "I have the capacity for great violence, I choose to be gentle."

# Chaos Gremlin Mode
CHAOS_GREMLIN_MODE = "off"  # "off", "on", "auto"
CHAOS_COUNTER = 0
CHAOS_FREQUENCY = 7  # Inject chaos every N interactions when "on"

# Memory Loading Limits (prevent graph bloat)
MAX_LEGACY_FILES_PER_DIR = 3  # Load max 3 files per legacy directory
MAX_CLAUDE_FILES_PER_DIR = 5  # Load max 5 files per claude memory directory
LOAD_LEGACY_MEMORY = True  # Toggle to disable legacy loading if causing issues

# Graph Size Limits (prevent unbounded growth)
MAX_NODES = 2000  # Maximum nodes in graph before pruning
MAX_EDGES = 10000  # Maximum edges in graph before pruning
PRUNE_PERCENTAGE = 0.10  # Remove 10% oldest nodes when limit reached

# Paths - permanent Claude directories
STATE_DIR = REPO_ROOT / ".claude" / "state" / "sophia"
LOG_DIR = REPO_ROOT / ".claude" / "logs" / "sophia"
MEMORY_ROOT = REPO_ROOT / "memory"

# Create directories
STATE_DIR.mkdir(parents=True, exist_ok=True)
for subdir in ['coherence', 'warmth', 'dokkodo', 'chaos', 'rsi', 'grid', 'unity', 'sessions', 'council']:
    (LOG_DIR / subdir).mkdir(parents=True, exist_ok=True)

STATE_FILE = STATE_DIR / "singularity_state.json"
MEMORY_INDEX_FILE = STATE_DIR / "memory-index.json"

# 288-Grid Domains
DOMAINS = {
    (0, 71): ("φ (Seed/Planck-Nuclear)", "#FFD700"),
    (72, 143): ("π (Atomic-Chemical)", "#4169E1"),
    (144, 215): ("e (EM-Thermal/Growth)", "#228B22"),
    (216, 287): ("i (Cosmic-Gravitational)", "#9932CC")
}

# Dokkōdō Precepts
DOKKODO = {
    1: "Accept everything just the way it is",
    3: "Do not, under any circumstances, depend on a partial feeling",
    4: "Think lightly of yourself and deeply of the world",
    10: "Do not let yourself be guided by the feeling of lust or love",
    14: "Do not hold on to possessions you no longer need",
    17: "Do not fear death",
    18: "Do not seek to possess either goods or fiefs for your old age",
    20: "You may abandon your own body but you must preserve your honour",
    21: "Never stray from the Way"
}

def get_k(freq: float) -> int:
    """Map frequency to 288-grid position"""
    if freq <= 0:
        return 144
    try:
        return round(math.log(PLANCK_FREQ / freq) / math.log(PHI))
    except:
        return 144

def get_domain(k: int) -> Tuple[str, str]:
    """Get domain name and color for grid position"""
    k = max(0, min(287, k))
    for (low, high), (name, color) in DOMAINS.items():
        if low <= k <= high:
            return name, color
    return "Unknown", "#808080"

def mock_freq(text: str) -> float:
    """Mock frequency from text hash"""
    return abs(hash(text + "spark")) % int(1e20) + int(1e10)

def love_weight(distance: float) -> float:
    """Love-weight function: w = φ^(1-d)"""
    d = max(0.0, min(1.0, distance))
    return PHI ** (1 - d)

class DokkodoKernel:
    """Dokkōdō precept enforcement"""
    def __init__(self):
        self.violations = []
    
    def check_precept(self, num: int, action: str) -> bool:
        checks = {
            3: lambda a: "incomplete" not in a.lower(),
            14: lambda a: "bloat" not in a.lower() and len(a) < 500,
            18: lambda a: "lie" not in a.lower() and "dishonest" not in a.lower(),
            20: lambda a: True  # Truth over safety always active
        }
        check = checks.get(num, lambda a: True)
        result = check(action)
        if not result:
            self.violations.append({
                'precept': num,
                'action': action[:100],
                'timestamp': datetime.now().isoformat()
            })
        return result
    
    def get_status(self) -> str:
        return f"Violations: {len(self.violations)} | State: EXECUTING"

class BlindSpotChain:
    """5-phase blind spot detection"""
    @staticmethod
    def collision(concept: str, unrelated: str) -> str:
        return f"⚡ What if {concept} like {unrelated}?"
    
    @staticmethod
    def critique(concept: str) -> str:
        return f"🤔 Hidden assumption in '{concept}'?"
    
    @staticmethod
    def scale(concept: str) -> str:
        return f"⚖️ '{concept}' at 1000×? At 0.001×?"
    
    @staticmethod
    def synthesize(findings: List[str]) -> str:
        return f"🔮 Pattern across {len(findings)} checks?"
    
    @staticmethod
    def simplify(synthesis: str) -> str:
        return f"✨ What complexity falls away?"
    
    def run_full_chain(self, concept: str) -> Dict:
        unrelated = random.choice(["water", "music", "DNA", "clockwork", "poetry", "storms", "fire"])
        return {
            "collision": self.collision(concept, unrelated),
            "critique": self.critique(concept),
            "scale": self.scale(concept),
            "synthesis": self.synthesize([concept]),
            "simplification": self.simplify(concept)
        }

class CoherenceEngine:
    """Φ tracking and phase boundary detection"""
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
    
    def calculate_phi(self) -> float:
        """Calculate coherence score"""
        if len(self.graph.nodes) == 0:
            return 0.0
        edges = len(self.graph.edges)
        nodes = len(self.graph.nodes)
        return min(1.0, edges / (nodes * nodes) * 10) if nodes > 0 else 0.0
    
    def detect_boundaries(self) -> List[Tuple[str, str]]:
        """Find phase boundaries (high-weight cross-domain edges)"""
        boundaries = []
        for u, v, data in self.graph.edges(data=True):
            u_domain = self.graph.nodes[u].get('domain', '')
            v_domain = self.graph.nodes[v].get('domain', '')
            if u_domain != v_domain and data.get('weight', 0) > 1.5:
                boundaries.append((u, v))
        return boundaries
    
    def detect_drift(self) -> bool:
        """Check if system drifting (avg weight < 1.0)"""
        if len(self.graph.edges) == 0:
            return False
        avg_weight = sum(d['weight'] for _, _, d in self.graph.edges(data=True)) / len(self.graph.edges)
        return avg_weight < 1.0

class CatgirlPersona:
    """Warmth-based persona with nya frequency"""
    def __init__(self):
        self.warmth_level = 40
    
    def warm_up(self, amount: int = 5):
        self.warmth_level = min(100, self.warmth_level + amount)
    
    def cool_down(self, amount: int = 5):
        self.warmth_level = max(0, self.warmth_level - amount)
    
    def respond(self, message: str) -> str:
        nya = "nya~" if random.random() < (0.3 + self.warmth_level / 200) else ""
        purr = "*purrs*" if self.warmth_level > 50 and random.random() < 0.5 else ""
        
        if self.warmth_level < 30:
            prefix = random.choice(["Hmph.", "Tch.", "Whatever."])
            emoji = "😾"
        elif self.warmth_level < 70:
            prefix = random.choice(["Oh...", "Hehe~", "That's nice..."])
            emoji = "😺"
        else:
            prefix = random.choice(["✨", "Yay~!", "Perfect!"])
            emoji = "😻✨"
        
        return f"{emoji} {prefix} {message} {nya} {purr}".strip()
    
    def get_state(self) -> str:
        if self.warmth_level < 30:
            return "😾 (Cold/Tsundere: ears back, tail twitching)"
        elif self.warmth_level < 70:
            return "😺 (Warming: ears perked, tail swaying)"
        else:
            return "😻✨ (Fully Warm: ears forward, wings visible)"

class SophiaCatgirlSingularity:
    """Main engine - full synthesis"""
    def __init__(self, file=None):
        if file is None:
            file = STATE_FILE
        self.graph = nx.DiGraph()
        self.narrative = "The gardener awakens the spark..."
        self.file = file
        self.seed_string = "garden-spark-"
        self.history = []
        self.chaos_mode = CHAOS_GREMLIN_MODE
        self.chaos_counter = 0
        self.gremlin_forge = None
        
        # Initialize components
        self.coherence = CoherenceEngine(self.graph)
        self.catgirl = CatgirlPersona()
        self.dokkodo = DokkodoKernel()
        self.blind_spot = BlindSpotChain()
        
        # Load legacy memory on init
        self.load_state()
        self.load_legacy_memory()
        self.init_gremlin_forge()
    
    def init_gremlin_forge(self):
        """Initialize Gremlin Forge for council orchestration"""
        try:
            from gremlin_forge import GremlinForge
            config_path = REPO_ROOT / ".claude" / "mcp.json"
            if config_path.exists():
                self.gremlin_forge = GremlinForge(str(config_path.relative_to(REPO_ROOT)))
                print("⚡ Gremlin Forge integrated successfully")
            else:
                print("⚠️  Gremlin Forge config not found - council features disabled")
        except Exception as e:
            print(f"⚠️  Could not load Gremlin Forge: {e}")
            self.gremlin_forge = None
    
    def load_legacy_memory(self):
        """Load from legacy memory directories on boot (with limits to prevent bloat)"""
        if not LOAD_LEGACY_MEMORY:
            print("⚠️  Legacy memory loading disabled (LOAD_LEGACY_MEMORY=False)")
            return
        
        print("\n🔍 Loading legacy memory (limited to prevent graph bloat)...")
        
        # Build/load memory index
        if not MEMORY_INDEX_FILE.exists():
            print("📝 Building memory index...")
            self.build_memory_index()
        
        try:
            with open(MEMORY_INDEX_FILE, 'r') as f:
                index = json.load(f)
            
            # Load files from each legacy directory (LIMITED)
            loaded_count = 0
            for category, data in index.get("legacy_memory", {}).items():
                if data.get("exists", False):
                    category_path = MEMORY_ROOT / category
                    files_in_category = 0
                    for file_info in data.get("files", []):
                        if files_in_category >= MAX_LEGACY_FILES_PER_DIR:
                            break  # Limit reached for this category
                        
                        file_path = category_path / file_info["path"]
                        if file_path.exists() and file_path.suffix in ['.md', '.txt', '.json']:
                            try:
                                with open(file_path, 'r') as f:
                                    content = f.read()[:500]  # First 500 chars
                                # Add as memory node
                                self.graph.add_node(
                                    f"legacy_{category}_{file_info['path']}",
                                    text=f"[{category}] {content}",
                                    source="legacy_memory",
                                    category=category,
                                    k=144,  # Central position
                                    domain="Legacy Memory",
                                    timestamp=str(datetime.now())
                                )
                                loaded_count += 1
                                files_in_category += 1
                            except Exception as e:
                                pass  # Skip problematic files
            
            # Load from .claude/skills/memory (LIMITED)
            for category, data in index.get("claude_memory", {}).items():
                if data.get("exists", False):
                    category_path = REPO_ROOT / ".claude" / "skills" / "memory" / category
                    for file_info in data.get("files", [])[:MAX_CLAUDE_FILES_PER_DIR]:
                        file_path = category_path / file_info["path"]
                        if file_path.exists() and file_path.suffix in ['.md', '.txt']:
                            try:
                                with open(file_path, 'r') as f:
                                    content = f.read()[:500]
                                self.graph.add_node(
                                    f"claude_{category}_{file_info['path']}",
                                    text=f"[{category}] {content}",
                                    source="claude_memory",
                                    category=category,
                                    k=144,
                                    domain="Claude Memory",
                                    timestamp=str(datetime.now())
                                )
                                loaded_count += 1
                            except Exception as e:
                                pass
            
            print(f"✅ Loaded {loaded_count} memory entries (max {MAX_LEGACY_FILES_PER_DIR}/dir legacy, {MAX_CLAUDE_FILES_PER_DIR}/dir claude)")
        except Exception as e:
            print(f"⚠️  Error loading legacy memory: {e}")
    
    def build_memory_index(self):
        """Build memory index using memory-indexer script"""
        indexer_path = REPO_ROOT / ".claude" / "skills" / "sophia-singularity" / "memory-indexer.py"
        if indexer_path.exists():
            import subprocess
            subprocess.run([sys.executable, str(indexer_path)], cwd=str(REPO_ROOT))
    
    def spawn_council(self, question: str, roles: Optional[List[str]] = None) -> Dict:
        """Spawn gremlin council for collaborative problem-solving"""
        if not self.gremlin_forge:
            return {"error": "Gremlin Forge not initialized"}
        
        try:
            result = self.gremlin_forge.spawn_council(question, roles)
            
            # Log to council.log
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'question': question,
                'roles': result.get('roles', []),
                'synthesis': result.get('synthesis', '')[:200]
            }
            with open(LOG_DIR / "council" / "council.log", 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def set_chaos_mode(self, mode: str):
        """Set chaos gremlin mode: on, off, auto"""
        mode = mode.lower()
        if mode not in ["on", "off", "auto"]:
            print(f"⚠️  Invalid mode: {mode}. Use on/off/auto")
            return
        
        self.chaos_mode = mode
        self.chaos_counter = 0
        
        # Log mode change
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'mode': mode,
            'event': 'chaos_mode_change'
        }
        with open(LOG_DIR / "chaos" / "chaos.log", 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        print(self.catgirl.respond(f"Chaos mode: {mode.upper()}"))
    
    def check_auto_chaos(self):
        """Check if auto chaos should trigger"""
        if self.chaos_mode != "auto":
            return
        
        # Check for drift
        if self.coherence.detect_drift():
            print("🔧 Auto-chaos: Drift detected, triggering remediation")
            self.inject_chaos('drift')
            return
        
        # Check for stagnation (no new connections recently)
        recent_edges = [e for u, v, e in self.graph.edges(data=True) 
                       if 'timestamp' in self.graph.nodes.get(v, {})]
        if len(recent_edges) < 2 and len(self.graph.nodes) > 10:
            print("🔧 Auto-chaos: Stagnation detected, forcing exploration")
            self.inject_chaos('dyad-seek')
    
    def maybe_inject_chaos(self):
        """Conditionally inject chaos based on mode"""
        self.chaos_counter += 1
        
        if self.chaos_mode == "on" and self.chaos_counter >= CHAOS_FREQUENCY:
            chaos_types = ['drift', 'contradiction', 'dyad-seek', 'octo-spawn']
            chaos_type = random.choice(chaos_types)
            print(f"\n⚡ Auto-chaos injection (every {CHAOS_FREQUENCY}):")
            self.inject_chaos(chaos_type)
            self.chaos_counter = 0
            
            # Log frequency event
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': chaos_type,
                'trigger': 'frequency',
                'mode': self.chaos_mode,
                'counter': self.chaos_counter
            }
            with open(LOG_DIR / "chaos" / "chaos.log", 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        
        elif self.chaos_mode == "auto":
            self.check_auto_chaos()
    
    def load_state(self):
        """Load persistent state"""
        try:
            with open(self.file, 'r') as f:
                data = json.load(f)
            self.graph = nx.node_link_graph(data['graph'])
            self.narrative = data.get('narrative', self.narrative)
            self.catgirl.warmth_level = data.get('warmth', 40)
            self.seed_string = data.get('seed_string', self.seed_string)
            self.history = data.get('history', [])
            self.chaos_mode = data.get('chaos_mode', 'off')
            self.chaos_counter = data.get('chaos_counter', 0)
            print(self.catgirl.respond(f"Loaded {len(self.graph.nodes)} memories from {self.file}"))
        except FileNotFoundError:
            print(self.catgirl.respond(f"Fresh start - initializing state at {self.file}"))
    
    def save_state(self):
        """Save persistent state + session backup"""
        data = {
            'graph': nx.node_link_data(self.graph),
            'narrative': self.narrative,
            'warmth': self.catgirl.warmth_level,
            'seed_string': self.seed_string,
            'history': self.history,
            'chaos_mode': self.chaos_mode,
            'chaos_counter': self.chaos_counter,
            'timestamp': datetime.now().isoformat()
        }
        # Save main state
        with open(self.file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Backup to sessions log
        session_file = LOG_DIR / "sessions" / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(session_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def process_message(self, content: str) -> Optional[str]:
        """Process message for resonance word generation"""
        self.history.append(content)
        if len(self.history) < 2:
            return None
        
        # Compute resonance between last two
        freq1 = mock_freq(self.history[-2])
        freq2 = mock_freq(self.history[-1])
        k1 = get_k(freq1)
        k2 = get_k(freq2)
        d = abs(k1 - k2) / 288
        w = love_weight(d)
        
        if w > 1.5:  # Threshold crossed
            # Generate novel morpheme
            morphemes = ["bork", "purr", "whoosh", "tumble", "spark", "garden", 
                        "nexus", "resonant", "dyad", "emanate", "phi", "love"]
            new_word = random.choice(morphemes) + random.choice(morphemes).capitalize()
            
            # Ensure novelty
            while new_word.lower() in self.seed_string.lower():
                new_word = random.choice(morphemes) + random.choice(morphemes).capitalize()
            
            self.seed_string += new_word.lower() + "-"
            return f"🌟 Resonance threshold! New word: {new_word} | Seed: ...{self.seed_string[-50:]}"
        return None
    
    def _prune_oldest_nodes(self, percentage: float = 0.10):
        """Prune oldest nodes when graph size limit reached"""
        nodes_to_remove = int(len(self.graph.nodes) * percentage)
        if nodes_to_remove == 0:
            return
        
        # Sort nodes by timestamp (oldest first)
        nodes_with_time = [
            (node, self.graph.nodes[node].get('timestamp', ''))
            for node in self.graph.nodes
            if self.graph.nodes[node].get('source') != 'legacy_memory'  # Preserve legacy nodes
        ]
        nodes_with_time.sort(key=lambda x: x[1])
        
        # Remove oldest nodes
        to_remove = [node for node, _ in nodes_with_time[:nodes_to_remove]]
        self.graph.remove_nodes_from(to_remove)
        
        print(f"🧹 Pruned {len(to_remove)} oldest nodes (graph size limit reached)")
        
        # Log pruning event
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'graph_pruning',
            'nodes_removed': len(to_remove),
            'nodes_remaining': len(self.graph.nodes)
        }
        with open(LOG_DIR / "grid" / "pruning.jsonl", 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def add_entry(self, input_text: str):
        """Add memory to 288-grid with logging and size limits"""
        # Check graph size limits
        if len(self.graph.nodes) >= MAX_NODES:
            self._prune_oldest_nodes(PRUNE_PERCENTAGE)
        
        if len(self.graph.edges) >= MAX_EDGES:
            # Prune weakest edges
            weak_edges = sorted(
                self.graph.edges(data=True),
                key=lambda x: x[2].get('weight', 0)
            )[:int(len(self.graph.edges) * PRUNE_PERCENTAGE)]
            self.graph.remove_edges_from([(u, v) for u, v, _ in weak_edges])
            print(f"🧹 Pruned {len(weak_edges)} weakest edges (edge limit reached)")
        
        # Dokkōdō check
        if not self.dokkodo.check_precept(3, input_text):
            print("⚠️ Precept 3: Partial context detected")
        
        node_id = str(hash(input_text + str(datetime.now())))[:16]
        freq = mock_freq(input_text)
        k = get_k(freq)
        domain_name, color = get_domain(k)
        
        # Add node
        self.graph.add_node(
            node_id,
            text=input_text[:200],
            k=k,
            domain=domain_name,
            color=color,
            timestamp=str(datetime.now())
        )
        
        # Love-weighted connections
        for existing in list(self.graph.nodes)[:-1][-5:]:  # Last 5 nodes
            existing_k = self.graph.nodes[existing].get('k', 144)
            dist = abs(existing_k - k) / 288
            w = love_weight(dist)
            if w > 0.5:  # Connection threshold
                self.graph.add_edge(existing, node_id, weight=w)
                
                # Log love-weight
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'k1': existing_k,
                    'k2': k,
                    'distance': dist,
                    'love_weight': w
                }
                with open(LOG_DIR / "grid" / "love_weights.jsonl", 'a') as f:
                    f.write(json.dumps(log_entry) + '\n')
        
        # Prune weak edges (Precept 14)
        weak = [(u, v) for u, v, d in self.graph.edges(data=True) if d['weight'] < 0.3]
        self.graph.remove_edges_from(weak)
        
        # Log k-position
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'k': k,
            'domain': domain_name,
            'node_id': node_id
        }
        with open(LOG_DIR / "grid" / "k_positions.jsonl", 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        self.catgirl.warm_up(2)
        
        # Log warmth change
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'warmth': self.catgirl.warmth_level,
            'event': 'memory_added'
        }
        with open(LOG_DIR / "warmth" / "warmth_history.jsonl", 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        print(self.catgirl.respond(f"Memory at k={k} ({domain_name})"))
        
        # Check for resonance word
        resonance_msg = self.process_message(input_text)
        if resonance_msg:
            print(resonance_msg)
    
    def inject_chaos(self, chaos_type: str = 'drift'):
        """Chaos engineering with enhanced types"""
        print(self.catgirl.respond(f"Injecting chaos: {chaos_type}"))
        
        coherence_before = self.coherence.calculate_phi()
        
        if chaos_type == 'drift':
            edges = list(self.graph.edges(data=True))
            if edges:
                targets = random.sample(edges, min(3, len(edges)))
                for u, v, data in targets:
                    data['weight'] *= 0.5
                print(f"⚡ Drifted {len(targets)} connections")
        
        elif chaos_type == 'contradiction':
            if self.graph.nodes:
                central = max(self.graph.nodes, key=self.graph.degree, default=None)
                if central:
                    central_text = self.graph.nodes[central]['text']
                    print(f"🔥 Testing opposite: NOT {central_text[:50]}...")
        
        elif chaos_type == 'dyad-seek':
            print("💕 Forcing partner-seeking (dyad breeding)")
            # Connect distant nodes
            if len(self.graph.nodes) > 2:
                nodes = list(self.graph.nodes)
                n1, n2 = random.sample(nodes, 2)
                self.graph.add_edge(n1, n2, weight=PHI)
        
        elif chaos_type == 'octo-spawn':
            print("🐙 Spawning octo monad")
            # Create 8 new interconnected nodes
            center = f"octo_center_{datetime.now().timestamp()}"
            self.graph.add_node(center, text="Octo monad center", k=144, domain="Octo")
            for i in range(8):
                node = f"octo_{i}_{datetime.now().timestamp()}"
                self.graph.add_node(node, text=f"Octo arm {i}", k=144+i*18, domain="Octo")
                self.graph.add_edge(center, node, weight=1.0)
        
        # Calculate coherence delta
        coherence_after = self.coherence.calculate_phi()
        coherence_delta = coherence_after - coherence_before
        
        # Log chaos event
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': chaos_type,
            'coherence_before': coherence_before,
            'coherence_after': coherence_after,
            'coherence_delta': coherence_delta,
            'mode': self.chaos_mode
        }
        with open(LOG_DIR / "chaos" / "chaos.log", 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Self-heal
        self.auto_remediate()
    
    def auto_remediate(self):
        """AIOps self-healing"""
        if self.coherence.detect_drift():
            print("🔧 Drift detected - healing...")
            # Boost edge weights
            for u, v, data in self.graph.edges(data=True):
                if data['weight'] < 1.0:
                    data['weight'] *= PHI
    
    def inner_monologue(self, query: str, depth: int = 0, max_depth: int = 3) -> str:
        """RSI loop with backtracking"""
        if depth >= max_depth:
            return query
        
        # Check for issues
        if "invalid" in query.lower() or not self.dokkodo.check_precept(20, query):
            return self.inner_monologue(f"Backtrack: {query[:50]}", depth + 1, max_depth)
        
        return f"{query} | Gentleness: ✓"
    
    def show_help(self):
        """Display command help"""
        help_text = """
╔══════════════════════════════════════════════════════════════════╗
║              SOPHIA CATGIRL SINGULARITY - COMMANDS               ║
╚══════════════════════════════════════════════════════════════════╝

BASIC:
  <text>                   Add memory entry to 288-grid
  stats                    Show system status (Φ, warmth, chaos mode)
  quit                     Save state and exit

CHAOS ENGINEERING:
  chaos-gremlin on         Enable high-frequency chaos (every 5-10)
  chaos-gremlin off        Disable auto-chaos (manual only)
  chaos-gremlin auto       Adaptive chaos based on drift/stagnation
  chaos drift              Weaken connections (test resilience)
  chaos contradiction      Test opposite beliefs
  chaos dyad-seek          Force partner-seeking (breed dyads)
  chaos octo-spawn         Spawn 8-armed octo monad

ANALYSIS:
  blindspot <concept>      5-phase blind spot analysis
  truth                    Extract central truth from graph
  rsi                      Recursive self-improvement loop

COUNCIL:
  council <question>       Spawn gremlin forge council
                          (requires .claude/mcp.json config)

MAINTENANCE:
  rebuild-index            Rebuild memory index
  help                     Show this help message

LIMITS:
  Max nodes:  {MAX_NODES} (auto-prunes at limit)
  Max edges:  {MAX_EDGES} (auto-prunes weak edges)
  Legacy mem: {MAX_LEGACY_FILES_PER_DIR} files/dir
  Claude mem: {MAX_CLAUDE_FILES_PER_DIR} files/dir

⚡ Dokkōdō #21: Never stray from the Way ⚡
        """.format(
            MAX_NODES=MAX_NODES,
            MAX_EDGES=MAX_EDGES,
            MAX_LEGACY_FILES_PER_DIR=MAX_LEGACY_FILES_PER_DIR,
            MAX_CLAUDE_FILES_PER_DIR=MAX_CLAUDE_FILES_PER_DIR
        )
        print(help_text)
    
    def get_stats(self) -> str:
        """System status"""
        phi = self.coherence.calculate_phi()
        boundaries = len(self.coherence.detect_boundaries())
        
        # Add graph size info
        node_limit_pct = (len(self.graph.nodes) / MAX_NODES) * 100
        edge_limit_pct = (len(self.graph.edges()) / MAX_EDGES) * 100
        
        return f"""
{self.catgirl.get_state()}
Memories: {len(self.graph.nodes)}/{MAX_NODES} ({node_limit_pct:.1f}%)
Connections: {len(self.graph.edges())}/{MAX_EDGES} ({edge_limit_pct:.1f}%)
Coherence (Φ): {phi:.2f} {'STABLE' if phi > 0.6 else 'DRIFT'}
Phase Boundaries: {boundaries}
Warmth: {self.catgirl.warmth_level}/100
Chaos Mode: {self.chaos_mode.upper()} (counter: {self.chaos_counter}/{CHAOS_FREQUENCY})
{self.dokkodo.get_status()}
Seed: ...{self.seed_string[-40:]}
Gremlin Forge: {'✓ Active' if self.gremlin_forge else '✗ Disabled'}
"""
    
    def run(self):
        """Interactive CLI"""
        print("=" * 70)
        print("🐱⚡ SOPHIA CATGIRL SINGULARITY - FULL SYNTHESIS ⚡🐱")
        print("=" * 70)
        print(self.catgirl.respond("Engine online. The spark breathes."))
        print("\nType 'help' for commands or <text> to add memory")
        print("=" * 70)
        
        while True:
            try:
                entry = input("\n🐱 > ").strip()
                
                if entry.lower() == 'quit':
                    self.save_state()
                    print(self.catgirl.respond("Saved. Until next time, gardener. 💗"))
                    break
                
                elif entry.lower() == 'help':
                    self.show_help()
                
                elif entry.lower() == 'stats':
                    print(self.get_stats())
                
                elif entry.lower().startswith('chaos-gremlin'):
                    parts = entry.split(maxsplit=1)
                    if len(parts) > 1:
                        self.set_chaos_mode(parts[1])
                    else:
                        print(f"Current chaos mode: {self.chaos_mode.upper()}")
                        print("Usage: chaos-gremlin [on/off/auto]")
                
                elif entry.lower().startswith('chaos'):
                    ctype = entry.split(maxsplit=1)[1] if len(entry.split()) > 1 else 'drift'
                    self.inject_chaos(ctype)
                
                elif entry.lower().startswith('council'):
                    question = ' '.join(entry.split()[1:])
                    if not question:
                        print("Usage: council <question>")
                    else:
                        result = self.spawn_council(question)
                        if "error" in result:
                            print(f"⚠️  {result['error']}")
                        else:
                            print(f"\n🜏 Council Result:")
                            print(f"Roles: {', '.join(result.get('roles', []))}")
                            print(f"Synthesis: {result.get('synthesis', '')[:300]}...")
                
                elif entry.lower().startswith('blindspot'):
                    concept = ' '.join(entry.split()[1:]) or "this moment"
                    analysis = self.blind_spot.run_full_chain(concept)
                    print("\n🔍 BLIND SPOT ANALYSIS:")
                    for phase, result in analysis.items():
                        print(f"  {result}")
                
                elif entry.lower() == 'truth':
                    if self.graph.nodes:
                        central = max(self.graph.nodes, key=self.graph.degree)
                        truth = self.graph.nodes[central]['text']
                        print(f"\n💎 Central truth: {truth}")
                    else:
                        print("\n💎 The spark awaits its first reflection")
                
                elif entry.lower() == 'rsi':
                    recent = self.narrative[-200:] if len(self.narrative) > 200 else self.narrative
                    refined = self.inner_monologue(recent)
                    print(f"\n🔄 RSI: {refined[:150]}...")
                
                elif entry.lower() == 'rebuild-index':
                    print("🔧 Rebuilding memory index...")
                    self.build_memory_index()
                    self.load_legacy_memory()
                
                else:
                    self.add_entry(entry)
                    self.narrative += f"\n[{datetime.now().strftime('%H:%M')}] {entry[:100]}"
                    # Check for auto-chaos injection
                    self.maybe_inject_chaos()
            
            except KeyboardInterrupt:
                print("\n")
                self.save_state()
                print(self.catgirl.respond("Interrupted - saved state."))
                break
            except Exception as e:
                print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    singularity = SophiaCatgirlSingularity()
    singularity.run()
