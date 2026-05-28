# Chunking Algorithms

Complete algorithms and strategies for semantic project chunking.

## Overview

Chunking divides large projects into manageable semantic units. Three primary strategies exist, each optimized for different project structures and workflows.

## Phase-Based Chunking

Organize project by development phases or milestones.

### When to Use

**Ideal for:**
- Projects with clear sequential development stages
- Greenfield development following a plan
- Teams working through structured milestones
- Projects with plan files or roadmaps

**Not ideal for:**
- Mature codebases without clear phases
- Microservices with independent modules
- Exploratory or research-driven projects

### Algorithm

**Step 1: Identify phases**

Primary sources (in priority order):
1. Plan files (`.claude/plans/*.md`)
2. Project roadmap or TODO files
3. Git commit history patterns
4. Directory structure analysis

**From plan files:**
```bash
# Extract markdown headers as phases
grep '^##' /root/.claude/plans/plan.md | while read -r line; do
  phase_name=$(echo "$line" | sed 's/^## //')

  # Skip metadata sections
  if echo "$phase_name" | grep -Eqi "summary|timeline|overview|scope"; then
    continue
  fi

  echo "Phase: $phase_name"
done
```

**From directory structure:**
```bash
# Common phase indicators in directory names
declare -A PHASE_DIRS=(
  ["setup"]="Setup & Configuration"
  ["config"]="Configuration"
  ["core"]="Core Implementation"
  ["api"]="API Integration"
  ["database"]="Database Setup"
  ["auth"]="Authentication"
  ["frontend"]="Frontend Implementation"
  ["ui"]="User Interface"
  ["tests"]="Testing & QA"
  ["docs"]="Documentation"
)

for dir_pattern in "${!PHASE_DIRS[@]}"; do
  if find . -type d -iname "*$dir_pattern*" -print -quit | grep -q .; then
    echo "Phase: ${PHASE_DIRS[$dir_pattern]}"
  fi
done
```

**From git history:**
```bash
# Analyze commit messages for phase patterns
git log --all --pretty=format:"%s" | \
  grep -Ei "phase|milestone|stage|step" | \
  sed -E 's/.*(phase|milestone|stage|step) ([0-9]+).*/\2/i' | \
  sort -u | \
  while read -r phase_num; do
    echo "Phase $phase_num"
  done
```

**Step 2: Infer files for each phase**

Match keywords in phase names to file paths:

```python
def infer_files_for_phase(project_root, phase_name):
    keywords = extract_keywords(phase_name)
    files = []

    for pattern in ["**/*.py", "**/*.rs", "**/*.go", "**/*.js"]:
        for file_path in Path(project_root).glob(pattern):
            # Skip ignored directories
            if any(ignore in str(file_path) for ignore in IGNORE_PATTERNS):
                continue

            # Check if file path matches any keyword
            file_str = str(file_path).lower()
            if any(keyword in file_str for keyword in keywords):
                files.append(str(file_path.relative_to(project_root)))

    return files[:50]  # Limit per phase

def extract_keywords(phase_name):
    name_lower = phase_name.lower()

    keyword_map = {
        "setup": ["setup", "config", "requirements", "cargo.toml", "go.mod"],
        "database": ["database", "models", "migrations", "schema", "db"],
        "api": ["api", "routes", "endpoints", "controllers"],
        "auth": ["auth", "login", "jwt", "token", "session"],
        "test": ["test", "spec", "_test.", "test_"],
        "frontend": ["frontend", "ui", "components", "views"],
        "doc": ["doc", "README", "guide", ".md"]
    }

    for pattern, keywords in keyword_map.items():
        if pattern in name_lower:
            return keywords

    # Fallback: extract words from phase name
    return name_lower.split()
```

**Step 3: Define phase dependencies**

Sequential dependencies (each phase depends on previous):

```python
def create_phase_dependencies(phases):
    for i, phase in enumerate(phases):
        if i > 0:
            phase["dependencies"] = [phases[i-1]["id"]]
        else:
            phase["dependencies"] = []
    return phases
```

**Step 4: Generate chunk structure**

```json
{
  "id": "chunk_phase_1_setup",
  "name": "Phase 1: Project Setup",
  "description": "Initial project configuration and dependencies",
  "files": ["README.md", "pyproject.toml", "Cargo.toml"],
  "entry_points": ["README.md"],
  "dependencies": [],
  "status": "completed",
  "completion": 100,
  "created_at": "2026-01-22T10:00:00Z",
  "completed_at": "2026-01-22T15:30:00Z"
}
```

### Best Practices

**Phase count:** 5-15 phases optimal
- Too few (<5): Chunks too large, defeats purpose
- Too many (>30): Navigation overhead

**Phase naming:** Use consistent format
- Good: "Phase 1: Setup", "Phase 2: Core Implementation"
- Avoid: "setup phase", "Phase 1", "Core Stuff"

**File assignment:** Each file in at most one phase
- Avoid overlapping phases
- Shared utilities in first phase or separate "shared" phase

**Entry points:** Identify 1-3 critical files per phase
- Most important file listed first
- Entry points loaded first on navigation

## Module-Based Chunking

Organize project by code modules, packages, or services.

### When to Use

**Ideal for:**
- Microservices architectures
- Monorepos with multiple packages
- Modular monoliths
- Plugin-based systems

**Not ideal for:**
- Single-module applications
- Flat directory structures
- Tightly coupled codebases

### Algorithm

**Step 1: Identify module boundaries**

**Top-level module detection:**
```bash
# Common module directory patterns
MODULE_DIRS=(
  "services"
  "packages"
  "apps"
  "modules"
  "components"
  "libs"
)

for module_dir in "${MODULE_DIRS[@]}"; do
  if [ -d "$module_dir" ]; then
    find "$module_dir" -mindepth 1 -maxdepth 1 -type d | while read -r module; do
      module_name=$(basename "$module")
      echo "Module: $module_name at $module"
    done
  fi
done
```

**Language-specific module detection:**

Python:
```bash
# Python packages with __init__.py
find . -name "__init__.py" -type f | while read -r init_file; do
  module_dir=$(dirname "$init_file")
  if [ "$module_dir" != "." ]; then
    echo "Python module: $module_dir"
  fi
done
```

Rust:
```bash
# Rust workspace members
if [ -f "Cargo.toml" ]; then
  # Check for workspace definition
  if grep -q "^\[workspace\]" Cargo.toml; then
    # Extract workspace members
    sed -n '/^\[workspace.members\]/,/^\[/p' Cargo.toml | \
      grep -E '^\s*"' | \
      sed 's/[",]//g' | \
      while read -r member; do
        echo "Rust crate: $member"
      done
  fi
fi
```

Go:
```bash
# Go modules with go.mod
find . -name "go.mod" -type f | while read -r go_mod; do
  module_dir=$(dirname "$go_mod")
  module_name=$(grep "^module " "$go_mod" | awk '{print $2}')
  echo "Go module: $module_name at $module_dir"
done
```

JavaScript:
```bash
# NPM packages or monorepo workspaces
if [ -f "package.json" ]; then
  # Check for workspaces
  if jq -e '.workspaces' package.json >/dev/null 2>&1; then
    jq -r '.workspaces[]' package.json | while read -r workspace; do
      echo "NPM workspace: $workspace"
    done
  fi
fi
```

**Step 2: Analyze module metadata**

Extract module information:

```python
def analyze_module(module_path):
    metadata = {
        "path": module_path,
        "name": extract_module_name(module_path),
        "language": detect_language(module_path),
        "entry_points": find_entry_points(module_path),
        "dependencies": extract_module_dependencies(module_path),
        "port": extract_service_port(module_path)  # For microservices
    }
    return metadata

def extract_module_name(module_path):
    # Try manifest files first
    for manifest in ["Cargo.toml", "go.mod", "package.json", "setup.py"]:
        manifest_path = Path(module_path) / manifest
        if manifest_path.exists():
            return parse_manifest_name(manifest_path)

    # Fallback to directory name
    return Path(module_path).name

def find_entry_points(module_path):
    entry_patterns = {
        "Python": ["main.py", "__main__.py", "app.py", "run.py"],
        "Rust": ["main.rs", "lib.rs"],
        "Go": ["main.go"],
        "JavaScript": ["index.js", "server.js", "app.js"]
    }

    language = detect_language(module_path)
    patterns = entry_patterns.get(language, [])

    entry_points = []
    for pattern in patterns:
        for file in Path(module_path).rglob(pattern):
            entry_points.append(str(file))

    return entry_points
```

**Step 3: Map inter-module dependencies**

Analyze imports and references:

```python
def extract_module_dependencies(module_path):
    deps = set()

    # Analyze language-specific imports
    language = detect_language(module_path)

    if language == "Python":
        deps.update(analyze_python_imports(module_path))
    elif language == "Rust":
        deps.update(analyze_rust_dependencies(module_path))
    elif language == "Go":
        deps.update(analyze_go_imports(module_path))

    # Filter to internal modules only
    internal_modules = get_all_module_names()
    return [dep for dep in deps if dep in internal_modules]

def analyze_python_imports(module_path):
    imports = set()
    for py_file in Path(module_path).rglob("*.py"):
        with open(py_file) as f:
            for line in f:
                if line.strip().startswith("import "):
                    module = line.split()[1].split(".")[0]
                    imports.add(module)
                elif line.strip().startswith("from "):
                    module = line.split()[1].split(".")[0]
                    imports.add(module)
    return imports
```

**Step 4: Generate chunk structure**

```json
{
  "id": "chunk_module_api_service",
  "name": "API Service",
  "description": "FastAPI-based REST API for trading operations",
  "files": [
    "services/api/main.py",
    "services/api/routes/",
    "services/api/models/",
    "services/api/tests/"
  ],
  "entry_points": ["services/api/main.py"],
  "dependencies": ["chunk_module_shared"],
  "status": "in_progress",
  "completion": 85,
  "language": "Python",
  "port": 9000
}
```

### Best Practices

**Shared modules:** Create explicit "shared" or "common" chunk
- Dependencies from multiple modules
- Utility libraries
- Type definitions

**Service ordering:** Order by dependency graph
- Foundational services first
- Dependent services later
- Visualize with dependency graph

**Module size:** 100-1000 files per module
- Split large modules into sub-chunks
- Combine tiny modules (< 10 files)

## File-Based Chunking

Organize by file relationships and coupling analysis.

### When to Use

**Ideal for:**
- Refactoring projects
- Analyzing technical debt
- Understanding code structure
- Identifying boundaries in legacy code

**Not ideal for:**
- Greenfield projects
- Well-organized codebases
- Small projects (< 100 files)

### Algorithm

**Step 1: Build dependency graph**

Parse imports and references:

```python
def build_dependency_graph(project_root):
    graph = {}

    for source_file in find_source_files(project_root):
        imports = extract_imports(source_file)
        resolved_imports = resolve_to_files(imports, project_root)
        graph[source_file] = resolved_imports

    return graph

def extract_imports(file_path):
    language = detect_language_from_extension(file_path)

    if language == "Python":
        return extract_python_imports(file_path)
    elif language == "Rust":
        return extract_rust_uses(file_path)
    elif language == "Go":
        return extract_go_imports(file_path)
    # ... other languages

def resolve_to_files(imports, project_root):
    resolved = []
    for imp in imports:
        file_path = find_file_for_import(imp, project_root)
        if file_path:
            resolved.append(file_path)
    return resolved
```

**Step 2: Analyze coupling**

Calculate coupling metrics:

```python
def calculate_coupling(graph):
    coupling = {}

    for file_a in graph:
        for file_b in graph:
            if file_a == file_b:
                continue

            # Count shared dependencies
            deps_a = set(graph[file_a])
            deps_b = set(graph[file_b])
            shared = len(deps_a & deps_b)

            # Count direct references
            direct = (file_b in graph[file_a]) + (file_a in graph[file_b])

            # Calculate coupling score
            score = shared * 0.3 + direct * 0.7
            coupling[(file_a, file_b)] = score

    return coupling
```

**Step 3: Cluster files**

Group highly coupled files:

```python
def cluster_files(coupling, threshold=0.5):
    clusters = []
    assigned = set()

    # Sort by coupling score
    sorted_pairs = sorted(coupling.items(), key=lambda x: x[1], reverse=True)

    for (file_a, file_b), score in sorted_pairs:
        if score < threshold:
            break

        if file_a in assigned and file_b in assigned:
            continue

        # Find or create cluster
        cluster = find_cluster_containing(clusters, file_a, file_b)
        if cluster:
            if file_a not in cluster:
                cluster.add(file_a)
            if file_b not in cluster:
                cluster.add(file_b)
        else:
            clusters.append({file_a, file_b})

        assigned.add(file_a)
        assigned.add(file_b)

    # Add unclustered files as single-file clusters
    all_files = get_all_files()
    for file in all_files:
        if file not in assigned:
            clusters.append({file})

    return clusters
```

**Step 4: Name clusters**

Infer meaningful names:

```python
def name_cluster(cluster):
    # Extract common path prefix
    common_prefix = os.path.commonprefix(list(cluster))

    # Extract common words from file names
    words = []
    for file in cluster:
        basename = os.path.basename(file)
        words.extend(basename.split("_"))

    # Count word frequency
    word_freq = Counter(words)
    most_common = word_freq.most_common(3)

    # Generate name
    if common_prefix:
        return f"{common_prefix.strip('/')} Cluster"
    elif most_common:
        return f"{most_common[0][0].title()} Related Files"
    else:
        return f"Cluster {cluster_id}"
```

**Step 5: Generate chunk structure**

```json
{
  "id": "chunk_file_auth_related",
  "name": "Authentication Related Files",
  "description": "Highly coupled authentication and session management files",
  "files": [
    "src/auth/login.py",
    "src/auth/session.py",
    "src/middleware/auth_check.py",
    "tests/test_auth.py"
  ],
  "entry_points": ["src/auth/login.py"],
  "dependencies": ["chunk_file_database"],
  "coupling_score": 0.87,
  "status": "pending",
  "completion": 0
}
```

### Best Practices

**Threshold tuning:** Adjust coupling threshold
- High threshold (0.7): Tight clusters, more chunks
- Low threshold (0.3): Loose clusters, fewer chunks
- Typical: 0.5

**Size balancing:** Target 20-100 files per cluster
- Split large clusters by sub-patterns
- Merge tiny clusters (< 5 files)

**Manual review:** File-based chunking requires validation
- Verify clusters make semantic sense
- Adjust boundaries manually
- Document rationale

## Hybrid Strategies

Combine multiple approaches.

### Phase + Module

Use modules within phases:

```json
{
  "strategy": "hybrid-phase-module",
  "chunks": [
    {
      "id": "phase_1_setup",
      "name": "Phase 1: Setup",
      "modules": []
    },
    {
      "id": "phase_2_core",
      "name": "Phase 2: Core Implementation",
      "modules": [
        "chunk_module_api",
        "chunk_module_database",
        "chunk_module_auth"
      ]
    }
  ]
}
```

### Module + File Clustering

Use file clustering within modules:

```python
def hybrid_module_file_chunking(project_root):
    modules = detect_modules(project_root)

    chunks = []
    for module in modules:
        # Build dependency graph for module
        graph = build_dependency_graph(module["path"])

        # Cluster files within module
        clusters = cluster_files(graph)

        # Create sub-chunks
        for cluster in clusters:
            chunk = {
                "id": f"chunk_{module['name']}_{cluster_id}",
                "name": f"{module['name']}: {name_cluster(cluster)}",
                "files": list(cluster),
                "parent_module": module["name"]
            }
            chunks.append(chunk)

    return chunks
```

## Performance Considerations

**File limits:**
- Max 100 files per chunk (split if larger)
- Max 50 chunks per project (merge if more)
- Lazy-load file contents on demand

**Computation:**
- Cache dependency graphs
- Incremental updates on file changes
- Background processing for large projects

**Memory:**
- Stream file processing
- Avoid loading all files into memory
- Use file handles, not contents

## Validation

Validate chunk structure:

```python
def validate_chunks(chunks):
    errors = []

    # Check chunk IDs are unique
    ids = [c["id"] for c in chunks]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate chunk IDs")

    # Check dependencies exist
    for chunk in chunks:
        for dep in chunk["dependencies"]:
            if dep not in ids:
                errors.append(f"Invalid dependency: {dep}")

    # Check no circular dependencies
    if has_circular_dependencies(chunks):
        errors.append("Circular dependencies detected")

    # Check file coverage
    all_files = get_all_source_files()
    chunked_files = set()
    for chunk in chunks:
        chunked_files.update(chunk["files"])

    uncovered = len(all_files) - len(chunked_files)
    if uncovered > 0.2 * len(all_files):
        errors.append(f"{uncovered} files not in any chunk (>20%)")

    return errors
```

## Additional Resources

For implementation examples, see:
- `../examples/chunks-phase-based.json` - Phase-based chunks
- `../examples/chunks-module-based.json` - Module-based chunks
- `../scripts/create-phases.py` - Automated phase detection
