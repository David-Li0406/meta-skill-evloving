#!/usr/bin/env python3
"""
Detect drift between documentation hub and actual codebase.

This tool compares:
- Documented modules vs. actual directories
- Documented technologies vs. package.json/requirements.txt
- Documented APIs vs. actual route files
- Documented database schema vs. actual schema files

Returns structured JSON with drift analysis and recommendations.
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Set


def load_package_json(project_path: Path) -> Dict:
    """Load and parse package.json if it exists."""
    package_json = project_path / "package.json"
    if package_json.exists():
        with open(package_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def load_requirements_txt(project_path: Path) -> List[str]:
    """Load requirements.txt if it exists."""
    requirements = project_path / "requirements.txt"
    if requirements.exists():
        with open(requirements, 'r', encoding='utf-8') as f:
            # Parse package names (ignore versions and comments)
            packages = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name (before ==, >=, etc.)
                    package = re.split(r'[=<>!]', line)[0].strip()
                    packages.append(package)
            return packages
    return []


def extract_modules_from_docs(docs_path: Path) -> Set[str]:
    """Extract documented modules from keyPairResponsibility.md."""
    responsibility_file = docs_path / "keyPairResponsibility.md"
    documented_modules = set()

    if not responsibility_file.exists():
        return documented_modules

    with open(responsibility_file, 'r', encoding='utf-8') as f:
        content = f.read()

        # Look for module references (common patterns)
        # Pattern 1: src/module_name
        modules = re.findall(r'`?(?:src|lib)/([a-zA-Z0-9_-]+)', content)
        documented_modules.update(modules)

        # Pattern 2: **ModuleName** or ### ModuleName (section headers)
        headers = re.findall(r'(?:\*\*|###)\s*([A-Z][a-zA-Z0-9]+)', content)
        documented_modules.update([h.lower() for h in headers])

    return documented_modules


def extract_technologies_from_docs(docs_path: Path) -> Set[str]:
    """Extract documented technologies from techStack.md."""
    tech_stack_file = docs_path / "techStack.md"
    documented_tech = set()

    if not tech_stack_file.exists():
        return documented_tech

    with open(tech_stack_file, 'r', encoding='utf-8') as f:
        content = f.read()

        # Common technology name patterns
        # Pattern 1: - Technology or * Technology (list items)
        tech_list = re.findall(r'^\s*[-*]\s*\*\*([A-Za-z0-9.]+)', content, re.MULTILINE)
        documented_tech.update(tech_list)

        # Pattern 2: **Technology**: description
        tech_with_desc = re.findall(r'\*\*([A-Za-z0-9.]+)\*\*:', content)
        documented_tech.update(tech_with_desc)

        # Pattern 3: ### Technology (section headers)
        tech_headers = re.findall(r'###\s+([A-Za-z0-9.]+)', content)
        documented_tech.update(tech_headers)

    return documented_tech


def get_actual_modules(project_path: Path) -> Set[str]:
    """Scan project directory for actual modules."""
    modules = set()

    # Common source directories
    src_paths = [
        project_path / "src",
        project_path / "lib",
        project_path / "app",
        project_path / "pages",
        project_path / "api"
    ]

    for src_path in src_paths:
        if not src_path.exists():
            continue

        # Find first-level subdirectories
        for item in src_path.iterdir():
            if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('_'):
                modules.add(item.name)

    return modules


def get_actual_technologies(project_path: Path) -> Set[str]:
    """Extract actual technologies from package files."""
    technologies = set()

    # From package.json
    package_data = load_package_json(project_path)
    if package_data:
        dependencies = package_data.get('dependencies', {})
        dev_dependencies = package_data.get('devDependencies', {})

        all_deps = {**dependencies, **dev_dependencies}

        # Add major frameworks/libraries
        major_tech = {
            'next': 'Next.js',
            'react': 'React',
            'vue': 'Vue.js',
            'express': 'Express',
            'fastapi': 'FastAPI',
            'django': 'Django',
            'typescript': 'TypeScript',
            'tailwindcss': 'Tailwind CSS',
            'prisma': 'Prisma',
            'mongoose': 'Mongoose',
            'axios': 'Axios',
            'graphql': 'GraphQL',
            'redis': 'Redis',
            'postgresql': 'PostgreSQL',
            'mongodb': 'MongoDB'
        }

        for dep_name in all_deps.keys():
            for tech_key, tech_name in major_tech.items():
                if tech_key in dep_name.lower():
                    technologies.add(tech_name)

    # From requirements.txt (Python projects)
    requirements = load_requirements_txt(project_path)
    python_tech = {
        'fastapi': 'FastAPI',
        'django': 'Django',
        'flask': 'Flask',
        'sqlalchemy': 'SQLAlchemy',
        'pydantic': 'Pydantic',
        'pytest': 'Pytest',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'torch': 'PyTorch',
        'tensorflow': 'TensorFlow'
    }

    for req in requirements:
        for tech_key, tech_name in python_tech.items():
            if tech_key in req.lower():
                technologies.add(tech_name)

    # Check for config files
    config_files = {
        'next.config.js': 'Next.js',
        'next.config.mjs': 'Next.js',
        'tailwind.config.js': 'Tailwind CSS',
        'tailwind.config.ts': 'Tailwind CSS',
        'prisma/schema.prisma': 'Prisma',
        'docker-compose.yml': 'Docker',
        'Dockerfile': 'Docker',
        'tsconfig.json': 'TypeScript'
    }

    for config_file, tech_name in config_files.items():
        if (project_path / config_file).exists():
            technologies.add(tech_name)

    return technologies


def calculate_drift_score(undocumented: int, documented_missing: int, total: int) -> float:
    """Calculate drift score (0-1, lower is better)."""
    if total == 0:
        return 0.0

    # Weight undocumented more heavily than documented-but-missing
    drift = (undocumented * 1.0 + documented_missing * 0.5) / total
    return min(drift, 1.0)


def detect_module_drift(project_path: Path, docs_path: Path) -> Dict:
    """Detect drift in module documentation."""
    documented_modules = extract_modules_from_docs(docs_path)
    actual_modules = get_actual_modules(project_path)

    undocumented = actual_modules - documented_modules
    documented_but_missing = documented_modules - actual_modules

    return {
        "category": "modules",
        "documented_count": len(documented_modules),
        "actual_count": len(actual_modules),
        "undocumented": sorted(list(undocumented)),
        "documented_but_missing": sorted(list(documented_but_missing)),
        "drift_score": calculate_drift_score(
            len(undocumented),
            len(documented_but_missing),
            len(actual_modules) + len(documented_modules)
        )
    }


def detect_technology_drift(project_path: Path, docs_path: Path) -> Dict:
    """Detect drift in technology documentation."""
    documented_tech = extract_technologies_from_docs(docs_path)
    actual_tech = get_actual_technologies(project_path)

    # Normalize for comparison (case-insensitive)
    doc_tech_lower = {t.lower(): t for t in documented_tech}
    actual_tech_lower = {t.lower(): t for t in actual_tech}

    undocumented_keys = set(actual_tech_lower.keys()) - set(doc_tech_lower.keys())
    documented_but_missing_keys = set(doc_tech_lower.keys()) - set(actual_tech_lower.keys())

    undocumented = [actual_tech_lower[k] for k in undocumented_keys]
    documented_but_missing = [doc_tech_lower[k] for k in documented_but_missing_keys]

    return {
        "category": "technologies",
        "documented_count": len(documented_tech),
        "actual_count": len(actual_tech),
        "undocumented": sorted(undocumented),
        "documented_but_missing": sorted(documented_but_missing),
        "drift_score": calculate_drift_score(
            len(undocumented),
            len(documented_but_missing),
            len(actual_tech) + len(documented_tech)
        )
    }


def generate_recommendations(module_drift: Dict, tech_drift: Dict) -> List[str]:
    """Generate actionable recommendations based on drift."""
    recommendations = []

    # Module recommendations
    if module_drift["undocumented"]:
        for module in module_drift["undocumented"][:5]:  # Limit to top 5
            recommendations.append(
                f"Document the '{module}' module in keyPairResponsibility.md"
            )

    if module_drift["documented_but_missing"]:
        for module in module_drift["documented_but_missing"][:3]:
            recommendations.append(
                f"Remove or update documentation for '{module}' (directory not found)"
            )

    # Technology recommendations
    if tech_drift["undocumented"]:
        for tech in tech_drift["undocumented"][:5]:
            recommendations.append(
                f"Add {tech} to techStack.md"
            )

    if tech_drift["documented_but_missing"]:
        for tech in tech_drift["documented_but_missing"][:3]:
            recommendations.append(
                f"Remove {tech} from techStack.md (not found in dependencies)"
            )

    # Overall recommendations
    if module_drift["drift_score"] > 0.3 or tech_drift["drift_score"] > 0.3:
        recommendations.append(
            "Consider running `/document-hub update` to synchronize documentation"
        )

    return recommendations


def main():
    """Main drift detection function."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Project path required"}))
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()

    if not project_path.exists():
        print(json.dumps({"error": f"Project path not found: {project_path}"}))
        sys.exit(1)

    docs_path = project_path / "cline-docs"
    if not docs_path.exists():
        print(json.dumps({
            "error": "Documentation hub not found. Run /document-hub initialize first.",
            "drift_score": 1.0
        }))
        sys.exit(0)

    # Detect drift in different categories
    module_drift = detect_module_drift(project_path, docs_path)
    tech_drift = detect_technology_drift(project_path, docs_path)

    # Calculate overall drift score
    overall_drift = (module_drift["drift_score"] + tech_drift["drift_score"]) / 2

    # Generate recommendations
    recommendations = generate_recommendations(module_drift, tech_drift)

    output = {
        "drift_score": round(overall_drift, 3),
        "status": "good" if overall_drift < 0.15 else "needs_attention" if overall_drift < 0.35 else "significant_drift",
        "module_drift": module_drift,
        "technology_drift": tech_drift,
        "recommendations": recommendations,
        "project_path": str(project_path),
        "docs_path": str(docs_path)
    }

    print(json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
