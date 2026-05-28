# Dependency Analysis

Techniques for analyzing file relationships and dependencies across codebases.

## Overview

Dependency analysis identifies how files relate to each other through imports, references, and shared dependencies. This information enables intelligent chunking, impact analysis, and refactoring guidance.

## Import Extraction

Extract import statements from source files.

### Python

**Import patterns:**
```python
import module
import module as alias
from module import name
from module import name as alias
from module import name1, name2
from . import relative
from .. import parent_relative
```

**Extraction script:**
```python
import ast
import re

def extract_python_imports(file_path):
    imports = []

    try:
        with open(file_path) as f:
            tree = ast.parse(f.read(), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "alias": alias.asname,
                        "type": "import"
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                level = node.level
                for alias in node.names:
                    imports.append({
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "level": level,
                        "type": "from_import"
                    })
    except SyntaxError:
        # Fallback to regex for syntax errors
        imports = extract_python_imports_regex(file_path)

    return imports

def extract_python_imports_regex(file_path):
    imports = []

    with open(file_path) as f:
        for line in f:
            line = line.strip()

            # import module
            if match := re.match(r'^import\s+([a-zA-Z0-9_.]+)', line):
                imports.append({"module": match.group(1), "type": "import"})

            # from module import name
            elif match := re.match(r'^from\s+([a-zA-Z0-9_.]+)\s+import', line):
                imports.append({"module": match.group(1), "type": "from_import"})

    return imports
```

**Resolve to files:**
```python
def resolve_python_import(import_spec, source_file, project_root):
    module = import_spec["module"]

    # Handle relative imports
    if import_spec.get("level", 0) > 0:
        source_dir = Path(source_file).parent
        for _ in range(import_spec["level"]):
            source_dir = source_dir.parent
        module = str(source_dir / module)

    # Convert module path to file path
    # e.g., "package.module" -> "package/module.py"
    file_path = Path(project_root) / module.replace(".", "/")

    # Try .py file
    if file_path.with_suffix(".py").exists():
        return str(file_path.with_suffix(".py"))

    # Try __init__.py in package
    init_path = file_path / "__init__.py"
    if init_path.exists():
        return str(init_path)

    return None
```

### Rust

**Use patterns:**
```rust
use std::collections::HashMap;
use crate::module::function;
use super::sibling;
use self::child;
mod submodule;
```

**Extraction script:**
```python
import re

def extract_rust_uses(file_path):
    uses = []

    with open(file_path) as f:
        for line in f:
            line = line.strip()

            # use statements
            if match := re.match(r'^use\s+([a-zA-Z0-9_:]+)', line):
                path = match.group(1)
                uses.append({
                    "path": path,
                    "type": "use"
                })

            # mod declarations
            elif match := re.match(r'^mod\s+([a-zA-Z0-9_]+)', line):
                module = match.group(1)
                uses.append({
                    "module": module,
                    "type": "mod"
                })

    return uses

def resolve_rust_use(use_spec, source_file, project_root):
    path = use_spec["path"]

    # crate:: refers to project root
    if path.startswith("crate::"):
        module_path = path.replace("crate::", "").replace("::", "/")
        file_path = Path(project_root) / "src" / module_path

    # super:: refers to parent module
    elif path.startswith("super::"):
        source_dir = Path(source_file).parent
        module_path = path.replace("super::", "").replace("::", "/")
        file_path = source_dir.parent / module_path

    # self:: refers to current module
    elif path.startswith("self::"):
        source_dir = Path(source_file).parent
        module_path = path.replace("self::", "").replace("::", "/")
        file_path = source_dir / module_path

    else:
        # External crate, skip
        return None

    # Try .rs file
    if file_path.with_suffix(".rs").exists():
        return str(file_path.with_suffix(".rs"))

    # Try mod.rs in directory
    mod_rs = file_path / "mod.rs"
    if mod_rs.exists():
        return str(mod_rs)

    return None
```

### Go

**Import patterns:**
```go
import "fmt"
import "github.com/user/project/pkg/module"
import (
    "context"
    "github.com/user/project/internal/auth"
)
```

**Extraction script:**
```python
import re

def extract_go_imports(file_path):
    imports = []

    with open(file_path) as f:
        content = f.read()

    # Single import
    for match in re.finditer(r'^import\s+"([^"]+)"', content, re.MULTILINE):
        imports.append({"package": match.group(1), "type": "import"})

    # Import block
    import_block = re.search(r'import\s*\((.*?)\)', content, re.DOTALL)
    if import_block:
        for line in import_block.group(1).split('\n'):
            if match := re.match(r'^\s*"([^"]+)"', line):
                imports.append({"package": match.group(1), "type": "import"})

    return imports

def resolve_go_import(import_spec, source_file, project_root):
    package = import_spec["package"]

    # Standard library, skip
    if not "/" in package:
        return None

    # Find go.mod to get module name
    go_mod = Path(project_root) / "go.mod"
    if not go_mod.exists():
        return None

    with open(go_mod) as f:
        module_line = f.readline()
        module_name = module_line.split()[1]

    # Internal package
    if package.startswith(module_name):
        relative_path = package.replace(module_name, "").lstrip("/")
        package_dir = Path(project_root) / relative_path

        # Find .go files in package
        go_files = list(package_dir.glob("*.go"))
        if go_files:
            return [str(f) for f in go_files]

    return None
```

### JavaScript/TypeScript

**Import patterns:**
```javascript
import { function } from 'module';
import * as name from 'module';
import defaultExport from 'module';
const module = require('module');
```

**Extraction script:**
```python
import re

def extract_js_imports(file_path):
    imports = []

    with open(file_path) as f:
        for line in f:
            line = line.strip()

            # import from
            if match := re.match(r'^import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]', line):
                imports.append({
                    "module": match.group(1),
                    "type": "import"
                })

            # require
            elif match := re.match(r'require\([\'"]([^\'"]+)[\'"]\)', line):
                imports.append({
                    "module": match.group(1),
                    "type": "require"
                })

    return imports

def resolve_js_import(import_spec, source_file, project_root):
    module = import_spec["module"]

    # Relative import
    if module.startswith("."):
        source_dir = Path(source_file).parent
        resolved = (source_dir / module).resolve()

        # Try with extensions
        for ext in [".js", ".jsx", ".ts", ".tsx"]:
            if resolved.with_suffix(ext).exists():
                return str(resolved.with_suffix(ext))

        # Try index file
        for ext in [".js", ".jsx", ".ts", ".tsx"]:
            index = resolved / f"index{ext}"
            if index.exists():
                return str(index)

    # Package import, skip (external)
    return None
```

## Dependency Graph Construction

Build complete project dependency graph.

### Graph Representation

```python
from collections import defaultdict
from typing import Dict, Set, List

class DependencyGraph:
    def __init__(self):
        # file -> [files it imports]
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)

        # file -> [files that import it]
        self.dependents: Dict[str, Set[str]] = defaultdict(set)

    def add_dependency(self, source: str, target: str):
        self.dependencies[source].add(target)
        self.dependents[target].add(source)

    def get_dependencies(self, file: str) -> Set[str]:
        return self.dependencies.get(file, set())

    def get_dependents(self, file: str) -> Set[str]:
        return self.dependents.get(file, set())

    def get_all_files(self) -> Set[str]:
        files = set(self.dependencies.keys())
        for deps in self.dependencies.values():
            files.update(deps)
        return files
```

### Building the Graph

```python
def build_dependency_graph(project_root):
    graph = DependencyGraph()

    # Find all source files
    source_files = find_source_files(project_root)

    for source_file in source_files:
        language = detect_language(source_file)

        # Extract imports based on language
        if language == "Python":
            imports = extract_python_imports(source_file)
            for imp in imports:
                target = resolve_python_import(imp, source_file, project_root)
                if target:
                    graph.add_dependency(source_file, target)

        elif language == "Rust":
            uses = extract_rust_uses(source_file)
            for use in uses:
                target = resolve_rust_use(use, source_file, project_root)
                if target:
                    graph.add_dependency(source_file, target)

        elif language == "Go":
            imports = extract_go_imports(source_file)
            for imp in imports:
                targets = resolve_go_import(imp, source_file, project_root)
                if targets:
                    for target in targets:
                        graph.add_dependency(source_file, target)

        elif language == "JavaScript":
            imports = extract_js_imports(source_file)
            for imp in imports:
                target = resolve_js_import(imp, source_file, project_root)
                if target:
                    graph.add_dependency(source_file, target)

    return graph
```

## Dependency Metrics

Calculate coupling and cohesion metrics.

### Afferent Coupling (Ca)

Number of files that depend on this file:

```python
def calculate_afferent_coupling(graph, file):
    return len(graph.get_dependents(file))
```

### Efferent Coupling (Ce)

Number of files this file depends on:

```python
def calculate_efferent_coupling(graph, file):
    return len(graph.get_dependencies(file))
```

### Instability (I)

Ratio of efferent to total coupling:

```python
def calculate_instability(graph, file):
    ca = calculate_afferent_coupling(graph, file)
    ce = calculate_efferent_coupling(graph, file)

    if ca + ce == 0:
        return 0

    return ce / (ca + ce)
```

**Interpretation:**
- I = 0: Maximally stable (many dependents, no dependencies)
- I = 1: Maximally unstable (many dependencies, no dependents)

### Distance from Main Sequence

Balance between abstractness and stability:

```python
def calculate_distance_from_main_sequence(graph, file, abstractness):
    instability = calculate_instability(graph, file)
    distance = abs(abstractness + instability - 1)
    return distance
```

**Ideal:** Distance close to 0 (file is on "main sequence")

### Shared Dependencies

Files that depend on same modules:

```python
def calculate_shared_dependencies(graph, file_a, file_b):
    deps_a = graph.get_dependencies(file_a)
    deps_b = graph.get_dependencies(file_b)
    return len(deps_a & deps_b)
```

## Transitive Dependencies

Find all transitive dependencies.

### Depth-First Search

```python
def get_transitive_dependencies(graph, file, visited=None):
    if visited is None:
        visited = set()

    if file in visited:
        return set()

    visited.add(file)
    transitive = set()

    for dep in graph.get_dependencies(file):
        transitive.add(dep)
        transitive.update(get_transitive_dependencies(graph, dep, visited))

    return transitive
```

### Breadth-First Search

```python
from collections import deque

def get_transitive_dependencies_bfs(graph, file):
    visited = set()
    queue = deque([file])
    transitive = set()

    while queue:
        current = queue.popleft()
        if current in visited:
            continue

        visited.add(current)

        for dep in graph.get_dependencies(current):
            transitive.add(dep)
            queue.append(dep)

    return transitive
```

### Dependency Depth

Maximum depth of dependency chain:

```python
def calculate_dependency_depth(graph, file, visited=None):
    if visited is None:
        visited = set()

    if file in visited:
        return 0

    visited.add(file)

    deps = graph.get_dependencies(file)
    if not deps:
        return 0

    max_depth = 0
    for dep in deps:
        depth = calculate_dependency_depth(graph, dep, visited)
        max_depth = max(max_depth, depth + 1)

    return max_depth
```

## Circular Dependency Detection

Identify circular dependencies in codebase.

### Tarjan's Algorithm

Find strongly connected components:

```python
def find_circular_dependencies(graph):
    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    on_stack = defaultdict(bool)
    sccs = []

    def strongconnect(file):
        index[file] = index_counter[0]
        lowlinks[file] = index_counter[0]
        index_counter[0] += 1
        stack.append(file)
        on_stack[file] = True

        for dep in graph.get_dependencies(file):
            if dep not in index:
                strongconnect(dep)
                lowlinks[file] = min(lowlinks[file], lowlinks[dep])
            elif on_stack[dep]:
                lowlinks[file] = min(lowlinks[file], index[dep])

        if lowlinks[file] == index[file]:
            scc = []
            while True:
                node = stack.pop()
                on_stack[node] = False
                scc.append(node)
                if node == file:
                    break
            sccs.append(scc)

    for file in graph.get_all_files():
        if file not in index:
            strongconnect(file)

    # Filter to only circular dependencies (SCC size > 1)
    circular = [scc for scc in sccs if len(scc) > 1]
    return circular
```

### Simple Cycle Detection

Check if adding dependency would create cycle:

```python
def would_create_cycle(graph, source, target):
    # Check if target has path to source
    visited = set()
    stack = [target]

    while stack:
        current = stack.pop()
        if current == source:
            return True

        if current in visited:
            continue

        visited.add(current)
        stack.extend(graph.get_dependencies(current))

    return False
```

## Impact Analysis

Analyze impact of changes to files.

### Direct Impact

Files directly importing changed file:

```python
def get_direct_impact(graph, changed_file):
    return graph.get_dependents(changed_file)
```

### Transitive Impact

All files transitively affected:

```python
def get_transitive_impact(graph, changed_file):
    visited = set()
    queue = deque([changed_file])
    impacted = set()

    while queue:
        current = queue.popleft()
        if current in visited:
            continue

        visited.add(current)

        for dependent in graph.get_dependents(current):
            impacted.add(dependent)
            queue.append(dependent)

    return impacted
```

### Impact Score

Weighted impact considering dependency depth:

```python
def calculate_impact_score(graph, changed_file):
    score = 0
    visited = set()

    def score_dependents(file, depth):
        nonlocal score
        if file in visited:
            return

        visited.add(file)

        for dependent in graph.get_dependents(file):
            # Weight decreases with depth
            weight = 1.0 / (depth + 1)
            score += weight
            score_dependents(dependent, depth + 1)

    score_dependents(changed_file, 0)
    return score
```

## Visualization

Generate dependency visualizations.

### DOT Format (Graphviz)

```python
def export_to_dot(graph, output_file):
    with open(output_file, 'w') as f:
        f.write("digraph dependencies {\n")
        f.write("  rankdir=LR;\n")
        f.write("  node [shape=box];\n\n")

        # Nodes
        for file in graph.get_all_files():
            label = Path(file).name
            f.write(f'  "{file}" [label="{label}"];\n')

        f.write("\n")

        # Edges
        for source in graph.get_all_files():
            for target in graph.get_dependencies(source):
                f.write(f'  "{source}" -> "{target}";\n')

        f.write("}\n")
```

Generate image:
```bash
dot -Tpng dependencies.dot -o dependencies.png
```

### JSON Format

```python
def export_to_json(graph, output_file):
    data = {
        "nodes": [],
        "links": []
    }

    file_to_id = {}
    for i, file in enumerate(graph.get_all_files()):
        file_to_id[file] = i
        data["nodes"].append({
            "id": i,
            "file": file,
            "name": Path(file).name
        })

    for source in graph.get_all_files():
        for target in graph.get_dependencies(source):
            data["links"].append({
                "source": file_to_id[source],
                "target": file_to_id[target]
            })

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
```

### Dependency Matrix

```python
def generate_dependency_matrix(graph):
    files = sorted(graph.get_all_files())
    n = len(files)

    matrix = [[0] * n for _ in range(n)]

    for i, source in enumerate(files):
        for j, target in enumerate(files):
            if target in graph.get_dependencies(source):
                matrix[i][j] = 1

    return matrix, files
```

## Caching Strategies

Cache dependency graphs for performance.

### File-Based Cache

```python
import pickle
import hashlib

def cache_dependency_graph(graph, project_root):
    cache_file = Path(project_root) / ".claude" / ".dependency-graph.cache"
    cache_file.parent.mkdir(exist_ok=True)

    # Calculate cache key from file mtimes
    cache_key = calculate_cache_key(project_root)

    cache_data = {
        "key": cache_key,
        "graph": graph
    }

    with open(cache_file, 'wb') as f:
        pickle.dump(cache_data, f)

def load_cached_graph(project_root):
    cache_file = Path(project_root) / ".claude" / ".dependency-graph.cache"

    if not cache_file.exists():
        return None

    with open(cache_file, 'rb') as f:
        cache_data = pickle.load(f)

    # Validate cache key
    current_key = calculate_cache_key(project_root)
    if cache_data["key"] != current_key:
        return None

    return cache_data["graph"]

def calculate_cache_key(project_root):
    hasher = hashlib.sha256()

    for source_file in sorted(find_source_files(project_root)):
        mtime = Path(source_file).stat().st_mtime
        hasher.update(f"{source_file}:{mtime}".encode())

    return hasher.hexdigest()
```

### Incremental Updates

```python
def update_graph_incremental(graph, changed_files, project_root):
    for file in changed_files:
        # Remove old dependencies
        old_deps = graph.get_dependencies(file)
        for dep in old_deps:
            graph.dependencies[file].discard(dep)
            graph.dependents[dep].discard(file)

        # Add new dependencies
        language = detect_language(file)
        imports = extract_imports(file, language)

        for imp in imports:
            target = resolve_import(imp, file, project_root, language)
            if target:
                graph.add_dependency(file, target)

    return graph
```

## Performance Optimization

Optimize dependency analysis for large projects.

### Parallel Processing

```python
from multiprocessing import Pool
from functools import partial

def build_dependency_graph_parallel(project_root, num_workers=4):
    source_files = find_source_files(project_root)

    # Process files in parallel
    with Pool(num_workers) as pool:
        extract_func = partial(extract_file_dependencies, project_root=project_root)
        results = pool.map(extract_func, source_files)

    # Merge results
    graph = DependencyGraph()
    for source_file, dependencies in results:
        for dep in dependencies:
            graph.add_dependency(source_file, dep)

    return graph

def extract_file_dependencies(file, project_root):
    language = detect_language(file)
    imports = extract_imports(file, language)

    dependencies = []
    for imp in imports:
        target = resolve_import(imp, file, project_root, language)
        if target:
            dependencies.append(target)

    return (file, dependencies)
```

### Sampling for Large Projects

```python
def build_sampled_graph(project_root, sample_size=1000):
    all_files = find_source_files(project_root)

    if len(all_files) <= sample_size:
        return build_dependency_graph(project_root)

    # Stratified sampling by language
    files_by_lang = defaultdict(list)
    for file in all_files:
        lang = detect_language(file)
        files_by_lang[lang].append(file)

    sampled_files = []
    for lang, files in files_by_lang.items():
        proportion = len(files) / len(all_files)
        lang_sample_size = int(sample_size * proportion)
        sampled_files.extend(random.sample(files, min(lang_sample_size, len(files))))

    # Build graph for sampled files
    graph = DependencyGraph()
    for file in sampled_files:
        # ... extract dependencies ...
        pass

    return graph
```

## Additional Resources

For implementation examples:
- `../scripts/create-phases.py` - Uses dependency inference
- See chunking-algorithms.md for clustering based on dependencies
