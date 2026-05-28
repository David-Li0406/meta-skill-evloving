#!/usr/bin/env python3
"""
Repo Analyzer - Code repository analysis and technical documentation generation tool.

This tool performs comprehensive analysis of code repositories and generates
detailed technical documentation reports following an 8-step analysis framework.
"""

import os
import sys
import json
import yaml
import toml
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Any
import chardet
from datetime import datetime

class RepoAnalyzer:
    """Main repository analyzer class."""

    def __init__(self, repo_path: str, depth: int = 2, verbose: bool = False):
        self.repo_path = Path(repo_path).resolve()
        self.depth = depth
        self.verbose = verbose
        self.report_data = {
            'overview': {},
            'structure': {},
            'tech_stack': {},
            'modules': {},
            'workflows': {},
            'architecture': {},
            'onboarding': {},
            'risks': {}
        }

    def log(self, message: str):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")

    def step1_global_scan(self):
        """Step 1: Repository global scan."""
        self.log("Starting global repository scan...")

        # Get repository stats
        total_files = 0
        total_dirs = 0
        max_depth = 0
        file_types = {}

        for root, dirs, files in os.walk(self.repo_path):
            depth = root[len(str(self.repo_path)):].count(os.sep)
            max_depth = max(max_depth, depth)

            if depth <= self.depth:
                total_dirs += len(dirs)
                total_files += len(files)

                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    file_types[ext] = file_types.get(ext, 0) + 1

        # Identify main languages based on file extensions
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.cs': 'C#',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.html': 'HTML',
            '.css': 'CSS',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.toml': 'TOML',
            '.xml': 'XML',
            '.sql': 'SQL'
        }

        languages = {}
        for ext, count in file_types.items():
            if ext in lang_map:
                lang = lang_map[ext]
                languages[lang] = languages.get(lang, 0) + count

        # Find key documentation files
        doc_files = []
        for doc_name in ['README.md', 'README', 'readme.md', 'CONTRIBUTING.md',
                        'CODE_OF_CONDUCT.md', 'LICENSE', 'CHANGELOG.md', 'CHANGELOG']:
            doc_path = self.repo_path / doc_name
            if doc_path.exists():
                doc_files.append(doc_name)

        # Find configuration files
        config_files = []
        for config_name in ['package.json', 'requirements.txt', 'pyproject.toml',
                          'pom.xml', 'build.gradle', 'build.gradle.kts',
                          'Cargo.toml', 'go.mod', 'composer.json',
                          'Gemfile', 'Podfile', 'docker-compose.yml',
                          'docker-compose.yaml', 'Dockerfile', '.gitignore']:
            config_path = self.repo_path / config_name
            if config_path.exists():
                config_files.append(config_name)

        self.report_data['overview'] = {
            'total_files': total_files,
            'total_dirs': total_dirs,
            'max_depth': max_depth,
            'languages': languages,
            'doc_files': doc_files,
            'config_files': config_files,
            'scan_depth': self.depth
        }

        self.log(f"Global scan complete: {total_files} files, {total_dirs} directories")

    def step2_project_positioning(self):
        """Step 2: Project positioning and purpose inference."""
        self.log("Analyzing project positioning...")

        # Read README if exists
        readme_content = ""
        readme_path = None
        for readme_name in ['README.md', 'README', 'readme.md']:
            test_path = self.repo_path / readme_name
            if test_path.exists():
                readme_path = test_path
                try:
                    with open(test_path, 'r', encoding='utf-8') as f:
                        readme_content = f.read()[:2000]  # First 2000 chars
                except:
                    try:
                        with open(test_path, 'rb') as f:
                            raw_data = f.read(2000)
                            result = chardet.detect(raw_data)
                            encoding = result['encoding']
                            readme_content = raw_data.decode(encoding, errors='ignore')
                    except:
                        readme_content = ""
                break

        # Analyze directory naming patterns
        dir_patterns = []
        top_level_dirs = []
        for item in os.listdir(self.repo_path):
            item_path = self.repo_path / item
            if item_path.is_dir():
                top_level_dirs.append(item)

                # Common patterns
                if item in ['src', 'source', 'lib', 'library']:
                    dir_patterns.append('source_code')
                elif item in ['test', 'tests', 'spec', 'specs']:
                    dir_patterns.append('testing')
                elif item in ['docs', 'documentation']:
                    dir_patterns.append('documentation')
                elif item in ['config', 'configuration', 'conf']:
                    dir_patterns.append('configuration')
                elif item in ['scripts', 'bin']:
                    dir_patterns.append('scripts')
                elif item in ['data', 'database', 'db']:
                    dir_patterns.append('data')
                elif item in ['public', 'static', 'assets']:
                    dir_patterns.append('assets')
                elif item in ['dist', 'build', 'target']:
                    dir_patterns.append('build_output')
                elif item in ['examples', 'demos', 'samples']:
                    dir_patterns.append('examples')

        # Infer project type based on patterns
        project_type = "unknown"
        if 'source_code' in dir_patterns and 'testing' in dir_patterns:
            project_type = "application"
        elif len(dir_patterns) == 1 and dir_patterns[0] == 'source_code':
            project_type = "library"
        elif 'documentation' in dir_patterns and 'source_code' not in dir_patterns:
            project_type = "documentation_project"

        # Infer from README keywords
        purpose_keywords = {
            'web': ['web', 'http', 'api', 'rest', 'graphql', 'server', 'client'],
            'mobile': ['mobile', 'ios', 'android', 'react native', 'flutter'],
            'desktop': ['desktop', 'gui', 'electron', 'qt', 'javafx'],
            'cli': ['cli', 'command line', 'terminal', 'console'],
            'library': ['library', 'sdk', 'framework', 'package', 'module'],
            'data': ['data', 'database', 'analytics', 'processing', 'etl'],
            'ai': ['ai', 'machine learning', 'ml', 'deep learning', 'neural'],
            'devops': ['devops', 'deploy', 'infrastructure', 'kubernetes', 'docker']
        }

        inferred_purposes = []
        readme_lower = readme_content.lower()
        for purpose, keywords in purpose_keywords.items():
            for keyword in keywords:
                if keyword in readme_lower:
                    if purpose not in inferred_purposes:
                        inferred_purposes.append(purpose)
                    break

        self.report_data['overview'].update({
            'readme_exists': readme_path is not None,
            'top_level_dirs': top_level_dirs,
            'dir_patterns': list(set(dir_patterns)),
            'project_type': project_type,
            'inferred_purposes': inferred_purposes,
            'readme_preview': readme_content[:500] if readme_content else ""
        })

        self.log(f"Project positioning complete: type={project_type}, purposes={inferred_purposes}")

    def step3_directory_structure(self):
        """Step 3: Directory structure and responsibility mapping."""
        self.log("Analyzing directory structure...")

        structure_analysis = {}

        # Analyze top-level directories
        for item in os.listdir(self.repo_path):
            item_path = self.repo_path / item
            if item_path.is_dir():
                analysis = {
                    'path': str(item_path.relative_to(self.repo_path)),
                    'type': 'directory',
                    'responsibility': self._infer_directory_responsibility(item),
                    'contents': [],
                    'relationships': []
                }

                # Scan immediate contents
                try:
                    for subitem in os.listdir(item_path):
                        subitem_path = item_path / subitem
                        if subitem_path.is_dir():
                            analysis['contents'].append(f"📁 {subitem}/")
                        else:
                            ext = os.path.splitext(subitem)[1]
                            if ext in ['.py', '.js', '.ts', '.java', '.go', '.rs']:
                                analysis['contents'].append(f"📄 {subitem} (code)")
                            elif ext in ['.md', '.txt', '.rst']:
                                analysis['contents'].append(f"📝 {subitem} (doc)")
                            elif ext in ['.json', '.yaml', '.yml', '.toml', '.xml']:
                                analysis['contents'].append(f"⚙️ {subitem} (config)")
                            else:
                                analysis['contents'].append(f"📄 {subitem}")
                except:
                    analysis['contents'] = ["[Access denied or error reading directory]"]

                # Limit contents display
                if len(analysis['contents']) > 10:
                    analysis['contents'] = analysis['contents'][:10] + [f"... and {len(analysis['contents']) - 10} more items"]

                structure_analysis[item] = analysis

        # Identify key directories (based on common patterns)
        key_dirs = []
        focus_dirs = []

        for dir_name, analysis in structure_analysis.items():
            resp = analysis['responsibility']
            if resp in ['source_code', 'core_logic', 'business_logic']:
                key_dirs.append(dir_name)
                focus_dirs.append(dir_name)
            elif resp in ['configuration', 'build_output', 'testing']:
                key_dirs.append(dir_name)

        self.report_data['structure'] = {
            'analysis': structure_analysis,
            'key_directories': key_dirs,
            'focus_directories': focus_dirs,
            'total_directories_analyzed': len(structure_analysis)
        }

        self.log(f"Directory analysis complete: {len(structure_analysis)} directories analyzed")

    def _infer_directory_responsibility(self, dir_name: str) -> str:
        """Infer directory responsibility from name."""
        dir_lower = dir_name.lower()

        responsibility_map = {
            'source_code': ['src', 'source', 'lib', 'library', 'app', 'application'],
            'core_logic': ['core', 'main', 'kernel', 'engine'],
            'business_logic': ['business', 'domain', 'model', 'service', 'logic'],
            'testing': ['test', 'tests', 'spec', 'specs', '__tests__'],
            'documentation': ['docs', 'documentation', 'doc'],
            'configuration': ['config', 'configuration', 'conf', 'settings'],
            'scripts': ['scripts', 'bin', 'tools', 'utilities'],
            'data': ['data', 'database', 'db', 'storage'],
            'assets': ['public', 'static', 'assets', 'media', 'images'],
            'build_output': ['dist', 'build', 'target', 'out', 'bin'],
            'examples': ['examples', 'demos', 'samples', 'examples'],
            'third_party': ['vendor', 'third_party', 'external', 'libs']
        }

        for resp, patterns in responsibility_map.items():
            for pattern in patterns:
                if pattern in dir_lower:
                    return resp

        return 'unknown'

    def step4_tech_stack_analysis(self):
        """Step 4: Technology stack and dependency analysis."""
        self.log("Analyzing technology stack...")

        dependencies = {}
        frameworks = {}
        infrastructure = {}

        # Check for various dependency files
        dep_files = {
            'package.json': self._parse_package_json,
            'requirements.txt': self._parse_requirements_txt,
            'pyproject.toml': self._parse_pyproject_toml,
            'pom.xml': self._parse_pom_xml,
            'build.gradle': self._parse_gradle,
            'build.gradle.kts': self._parse_gradle_kts,
            'Cargo.toml': self._parse_cargo_toml,
            'go.mod': self._parse_go_mod,
            'composer.json': self._parse_composer_json,
            'Gemfile': self._parse_gemfile
        }

        for dep_file, parser in dep_files.items():
            file_path = self.repo_path / dep_file
            if file_path.exists():
                try:
                    deps = parser(file_path)
                    if deps:
                        dependencies[dep_file] = deps
                except Exception as e:
                    self.log(f"Error parsing {dep_file}: {e}")

        # Infer frameworks from dependencies
        framework_patterns = {
            'web': ['express', 'koa', 'fastapi', 'flask', 'django', 'spring', 'laravel', 'rails'],
            'frontend': ['react', 'vue', 'angular', 'svelte', 'next', 'nuxt'],
            'database': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'elasticsearch'],
            'testing': ['jest', 'mocha', 'pytest', 'junit', 'rspec', 'cypress'],
            'devops': ['docker', 'kubernetes', 'terraform', 'ansible', 'jenkins'],
            'ai_ml': ['tensorflow', 'pytorch', 'scikit-learn', 'opencv', 'numpy', 'pandas']
        }

        for dep_file, deps in dependencies.items():
            for dep_name in deps:
                dep_lower = dep_name.lower()
                for category, patterns in framework_patterns.items():
                    for pattern in patterns:
                        if pattern in dep_lower:
                            if category not in frameworks:
                                frameworks[category] = []
                            if dep_name not in frameworks[category]:
                                frameworks[category].append(dep_name)

        # Check for infrastructure files
        infra_files = ['docker-compose.yml', 'docker-compose.yaml', 'Dockerfile',
                      'dockerfile', '.dockerignore', 'docker-compose.override.yml']

        for infra_file in infra_files:
            file_path = self.repo_path / infra_file
            if file_path.exists():
                infrastructure[infra_file] = 'found'

        self.report_data['tech_stack'] = {
            'dependencies': dependencies,
            'frameworks': frameworks,
            'infrastructure': infrastructure,
            'dependency_files_found': list(dependencies.keys())
        }

        self.log(f"Tech stack analysis complete: {len(dependencies)} dependency files found")

    def _parse_package_json(self, file_path: Path) -> List[str]:
        """Parse package.json file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        deps = []
        if 'dependencies' in data:
            deps.extend(list(data['dependencies'].keys()))
        if 'devDependencies' in data:
            deps.extend(list(data['devDependencies'].keys()))

        return deps

    def _parse_requirements_txt(self, file_path: Path) -> List[str]:
        """Parse requirements.txt file."""
        deps = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('-'):
                        # Extract package name (before version specifiers)
                        pkg = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0]
                        pkg = pkg.strip()
                        if pkg:
                            deps.append(pkg)
        except:
            pass

        return deps

    def _parse_pyproject_toml(self, file_path: Path) -> List[str]:
        """Parse pyproject.toml file."""
        try:
            data = toml.load(file_path)
            deps = []

            # Check for dependencies in various sections
            if 'project' in data and 'dependencies' in data['project']:
                deps.extend(data['project']['dependencies'])

            if 'tool' in data and 'poetry' in data['tool']:
                if 'dependencies' in data['tool']['poetry']:
                    deps.extend(list(data['tool']['poetry']['dependencies'].keys()))

            return deps
        except:
            return []

    def _parse_pom_xml(self, file_path: Path) -> List[str]:
        """Parse pom.xml file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Simple XML parsing for dependencies
            deps = []
            import re
            dependency_pattern = r'<artifactId>([^<]+)</artifactId>'
            matches = re.findall(dependency_pattern, content)
            deps.extend(matches)

            return deps
        except:
            return []

    def _parse_gradle(self, file_path: Path) -> List[str]:
        """Parse build.gradle file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Simple pattern matching for dependencies
            deps = []
            import re
            dep_pattern = r"implementation\s+['\"]([^:'\"]+)"
            matches = re.findall(dep_pattern, content)
            deps.extend(matches)

            return deps
        except:
            return []

    def _parse_gradle_kts(self, file_path: Path) -> List[str]:
        """Parse build.gradle.kts file."""
        return self._parse_gradle(file_path)

    def _parse_cargo_toml(self, file_path: Path) -> List[str]:
        """Parse Cargo.toml file."""
        try:
            data = toml.load(file_path)
            deps = []

            if 'dependencies' in data:
                deps.extend(list(data['dependencies'].keys()))

            return deps
        except:
            return []

    def _parse_go_mod(self, file_path: Path) -> List[str]:
        """Parse go.mod file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            deps = []
            import re
            require_pattern = r'require\s+([^\s]+)'
            matches = re.findall(require_pattern, content)
            deps.extend(matches)

            return deps
        except:
            return []

    def _parse_composer_json(self, file_path: Path) -> List[str]:
        """Parse composer.json file."""
        return self._parse_package_json(file_path)

    def _parse_gemfile(self, file_path: Path) -> List[str]:
        """Parse Gemfile."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            deps = []
            import re
            gem_pattern = r"gem\s+['\"]([^'\"]+)"
            matches = re.findall(gem_pattern, content)
            deps.extend(matches)

            return deps
        except:
            return []

    def step5_core_modules(self):
        """Step 5: Core module and business domain abstraction."""
        self.log("Analyzing core modules...")

        modules = {}

        # Look for common module patterns
        module_patterns = {
            'api': ['api', 'rest', 'graphql', 'endpoint', 'controller'],
            'service': ['service', 'business', 'logic', 'manager', 'handler'],
            'model': ['model', 'entity', 'domain', 'schema', 'dto'],
            'repository': ['repository', 'dao', 'store', 'persistence'],
            'utility': ['util', 'utility', 'helper', 'tool', 'common'],
            'config': ['config', 'configuration', 'setting', 'constant'],
            'middleware': ['middleware', 'interceptor', 'filter', 'guard'],
            'component': ['component', 'widget', 'view', 'page', 'screen']
        }

        # Scan source directories
        source_dirs = []
        for dir_name, analysis in self.report_data['structure']['analysis'].items():
            if analysis['responsibility'] in ['source_code', 'core_logic', 'business_logic']:
                source_dirs.append(dir_name)

        for source_dir in source_dirs:
            source_path = self.repo_path / source_dir
            if source_path.exists():
                # Look for module indicators
                for root, dirs, files in os.walk(source_path):
                    for dir_name in dirs:
                        dir_lower = dir_name.lower()
                        for module_type, patterns in module_patterns.items():
                            for pattern in patterns:
                                if pattern in dir_lower:
                                    if module_type not in modules:
                                        modules[module_type] = []
                                    if dir_name not in modules[module_type]:
                                        modules[module_type].append(dir_name)

                    for file_name in files:
                        file_lower = file_name.lower()
                        for module_type, patterns in module_patterns.items():
                            for pattern in patterns:
                                if pattern in file_lower and file_name.endswith(('.py', '.js', '.ts', '.java')):
                                    if module_type not in modules:
                                        modules[module_type] = []
                                    module_name = os.path.splitext(file_name)[0]
                                    if module_name not in modules[module_type]:
                                        modules[module_type].append(module_name)

        # Infer business domains from directory names
        business_domains = []
        domain_keywords = ['user', 'auth', 'product', 'order', 'payment', 'inventory',
                          'customer', 'account', 'report', 'analytics', 'notification',
                          'message', 'file', 'image', 'video', 'document', 'task']

        for dir_name in self.report_data['overview']['top_level_dirs']:
            dir_lower = dir_name.lower()
            for keyword in domain_keywords:
                if keyword in dir_lower:
                    business_domains.append(dir_name)
                    break

        self.report_data['modules'] = {
            'module_types': modules,
            'business_domains': business_domains,
            'source_directories': source_dirs
        }

        self.log(f"Core module analysis complete: {len(modules)} module types identified")

    def step6_execution_workflows(self):
        """Step 6: Key execution workflow analysis."""
        self.log("Analyzing execution workflows...")

        entry_points = []
        workflow_patterns = []

        # Look for common entry points
        entry_patterns = [
            'main.py', 'app.py', 'index.js', 'server.js', 'app.js',
            'Main.java', 'Application.java', 'main.go', 'main.rs',
            'package.json', 'pom.xml', 'build.gradle', 'Cargo.toml'
        ]

        for pattern in entry_patterns:
            for root, dirs, files in os.walk(self.repo_path):
                for file in files:
                    if file.lower() == pattern.lower():
                        rel_path = os.path.relpath(os.path.join(root, file), self.repo_path)
                        entry_points.append(rel_path)

        # Look for startup scripts
        script_patterns = ['start.sh', 'start.bat', 'run.sh', 'run.bat',
                          'docker-compose.yml', 'docker-compose.yaml']

        for pattern in script_patterns:
            file_path = self.repo_path / pattern
            if file_path.exists():
                entry_points.append(pattern)

        # Infer workflow from project type
        project_type = self.report_data['overview']['project_type']
        if project_type == 'application':
            workflow_patterns.append('Request → Controller → Service → Repository → Database')
            workflow_patterns.append('CLI command → Parser → Handler → Output')
        elif project_type == 'library':
            workflow_patterns.append('Import → Initialization → Method calls')
            workflow_patterns.append('Configuration → Factory → Instance creation')

        # Check for common workflow files
        workflow_files = ['docker-compose.yml', 'docker-compose.yaml', 'Makefile',
                         'package.json', 'Procfile', 'dockerfile']

        found_workflow_files = []
        for wf_file in workflow_files:
            file_path = self.repo_path / wf_file
            if file_path.exists():
                found_workflow_files.append(wf_file)

        self.report_data['workflows'] = {
            'entry_points': entry_points,
            'workflow_patterns': workflow_patterns,
            'workflow_files': found_workflow_files,
            'project_type': project_type
        }

        self.log(f"Execution workflow analysis complete: {len(entry_points)} entry points found")

    def step7_onboarding_guide(self):
        """Step 7: Onboarding path generation."""
        self.log("Generating onboarding guide...")

        reading_order = []
        safe_modification_points = []
        first_week_goals = []

        # Determine reading order based on project structure
        reading_order.append("1. README.md - Project overview and setup instructions")

        if self.report_data['overview']['config_files']:
            config_preview = ', '.join(self.report_data['overview']['config_files'][:3])
            reading_order.append(f"2. Configuration files: {config_preview}")

        source_dirs = self.report_data['modules']['source_directories']
        if source_dirs:
            reading_order.append(f"3. Source directories: {', '.join(source_dirs[:3])}")

        if self.report_data['structure']['key_directories']:
            key_dirs = self.report_data['structure']['key_directories'][:3]
            reading_order.append(f"4. Key directories: {', '.join(key_dirs)}")

        reading_order.append("5. Test directories and examples")
        reading_order.append("6. Build and deployment configuration")

        # Identify safe modification points
        safe_patterns = [
            ('test files', 'Add new test cases in existing test directories'),
            ('configuration', 'Modify configuration values in config files'),
            ('documentation', 'Update README or documentation files'),
            ('utility functions', 'Add helper functions in utility modules'),
            ('examples', 'Add new example files in examples directory')
        ]

        for pattern, description in safe_patterns:
            safe_modification_points.append(f"• {description}")

        # First week goals
        first_week_goals.append("• Set up development environment")
        first_week_goals.append("• Run the test suite")
        first_week_goals.append("• Make a small, safe change (e.g., update documentation)")
        first_week_goals.append("• Understand the basic project structure")
        first_week_goals.append("• Identify key entry points and workflows")

        self.report_data['onboarding'] = {
            'reading_order': reading_order,
            'safe_modification_points': safe_modification_points,
            'first_week_goals': first_week_goals,
            'key_directories': self.report_data['structure']['key_directories'][:5] if self.report_data['structure']['key_directories'] else []
        }

        self.log("Onboarding guide generation complete")

    def step8_risk_assessment(self):
        """Step 8: Risk assessment and technical debt analysis."""
        self.log("Performing risk assessment...")

        risks = []
        complex_points = []
        pitfalls = []

        # Check for potential risks
        if self.report_data['overview']['max_depth'] > 4:
            risks.append("Deep directory nesting may indicate complex module dependencies")

        if len(self.report_data['tech_stack']['dependency_files_found']) > 3:
            risks.append("Multiple dependency management systems may cause version conflicts")

        if not self.report_data['overview']['readme_exists']:
            risks.append("Missing README file makes onboarding difficult")

        # Check for complex points
        module_types = len(self.report_data['modules']['module_types'])
        if module_types > 5:
            complex_points.append(f"Multiple module types ({module_types}) may indicate complex architecture")

        if len(self.report_data['workflows']['entry_points']) > 3:
            complex_points.append("Multiple entry points may require understanding different startup scenarios")

        # Identify potential pitfalls
        if 'build_output' in [a['responsibility'] for a in self.report_data['structure']['analysis'].values()]:
            pitfalls.append("Build output directories should be excluded from version control (.gitignore)")

        if self.report_data['overview']['project_type'] == 'unknown':
            pitfalls.append("Unclear project structure may make navigation challenging")

        self.report_data['risks'] = {
            'potential_risks': risks,
            'complex_points': complex_points,
            'potential_pitfalls': pitfalls,
            'has_risks': len(risks) > 0 or len(complex_points) > 0 or len(pitfalls) > 0
        }

        self.log(f"Risk assessment complete: {len(risks)} risks, {len(complex_points)} complex points")

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate the final Markdown report."""
        self.log("Generating final report...")

        report = []
        report.append(f"# Repository Analysis Report")
        report.append(f"")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Repository**: {self.repo_path}")
        report.append(f"**Analysis Depth**: {self.depth}")
        report.append(f"")

        # 1. Repository Overview
        report.append(f"## 1. Repository Overview")
        report.append(f"")

        overview = self.report_data['overview']
        report.append(f"- **Project Type**: {overview.get('project_type', 'unknown')}")
        report.append(f"- **Inferred Purposes**: {', '.join(overview.get('inferred_purposes', ['unknown']))}")
        report.append(f"- **Total Files**: {overview.get('total_files', 0)}")
        report.append(f"- **Total Directories**: {overview.get('total_dirs', 0)}")
        report.append(f"- **Maximum Depth**: {overview.get('max_depth', 0)}")
        report.append(f"- **Main Languages**: {', '.join([f'{k} ({v} files)' for k, v in overview.get('languages', {}).items()][:5])}")

        if overview.get('readme_exists'):
            report.append(f"- **README**: Found")
            preview = overview.get('readme_preview', '')
            if preview:
                report.append(f"  Preview: {preview[:200]}...")
        else:
            report.append(f"- **README**: Not found")

        report.append(f"- **Configuration Files**: {', '.join(overview.get('config_files', [])[:5])}")
        report.append(f"")

        # 2. Project Structure
        report.append(f"## 2. Project Structure")
        report.append(f"")

        structure = self.report_data['structure']
        report.append(f"- **Total Directories Analyzed**: {structure.get('total_directories_analyzed', 0)}")
        report.append(f"- **Key Directories**: {', '.join(structure.get('key_directories', [])[:5])}")
        report.append(f"- **Focus Directories**: {', '.join(structure.get('focus_directories', [])[:3])}")
        report.append(f"")

        report.append(f"### Directory Analysis")
        report.append(f"")
        for dir_name, analysis in list(structure.get('analysis', {}).items())[:10]:  # Limit to 10
            report.append(f"#### 📁 {dir_name}")
            report.append(f"- **Responsibility**: {analysis.get('responsibility', 'unknown')}")
            if analysis.get('contents'):
                report.append(f"- **Contents Preview**:")
                for item in analysis.get('contents', [])[:5]:
                    report.append(f"  - {item}")
                if len(analysis.get('contents', [])) > 5:
                    report.append(f"  - ... and {len(analysis.get('contents', [])) - 5} more items")
            report.append(f"")

        # 3. Technology Stack
        report.append(f"## 3. Technology Stack")
        report.append(f"")

        tech_stack = self.report_data['tech_stack']
        report.append(f"- **Dependency Files Found**: {', '.join(tech_stack.get('dependency_files_found', []))}")
        report.append(f"")

        if tech_stack.get('frameworks'):
            report.append(f"### Framework Categories")
            report.append(f"")
            for category, frameworks in tech_stack.get('frameworks', {}).items():
                report.append(f"- **{category.title()}**: {', '.join(frameworks[:5])}")
                if len(frameworks) > 5:
                    report.append(f"  (and {len(frameworks) - 5} more)")
            report.append(f"")

        if tech_stack.get('infrastructure'):
            report.append(f"### Infrastructure")
            report.append(f"")
            for infra_file, status in tech_stack.get('infrastructure', {}).items():
                report.append(f"- **{infra_file}**: {status}")
            report.append(f"")

        # 4. Core Modules
        report.append(f"## 4. Core Modules & Business Domains")
        report.append(f"")

        modules = self.report_data['modules']
        report.append(f"- **Source Directories**: {', '.join(modules.get('source_directories', []))}")
        report.append(f"- **Business Domains**: {', '.join(modules.get('business_domains', []))}")
        report.append(f"")

        if modules.get('module_types'):
            report.append(f"### Module Types Identified")
            report.append(f"")
            for module_type, module_list in modules.get('module_types', {}).items():
                report.append(f"- **{module_type.title()}**: {', '.join(module_list[:5])}")
                if len(module_list) > 5:
                    report.append(f"  (and {len(module_list) - 5} more)")
            report.append(f"")

        # 5. Execution Workflows
        report.append(f"## 5. Key Execution Workflows")
        report.append(f"")

        workflows = self.report_data['workflows']
        report.append(f"- **Project Type**: {workflows.get('project_type', 'unknown')}")

        if workflows.get('entry_points'):
            report.append(f"- **Entry Points**:")
            for entry in workflows.get('entry_points', [])[:5]:
                report.append(f"  - {entry}")
            if len(workflows.get('entry_points', [])) > 5:
                report.append(f"  - ... and {len(workflows.get('entry_points', [])) - 5} more")
            report.append(f"")

        if workflows.get('workflow_patterns'):
            report.append(f"- **Inferred Workflow Patterns**:")
            for pattern in workflows.get('workflow_patterns', []):
                report.append(f"  - {pattern}")
            report.append(f"")

        if workflows.get('workflow_files'):
            report.append(f"- **Workflow Configuration Files**: {', '.join(workflows.get('workflow_files', []))}")
            report.append(f"")

        # 6. Architecture Design
        report.append(f"## 6. Architecture Design & Extension Patterns")
        report.append(f"")

        # Infer architecture from patterns
        arch_inferences = []
        if 'api' in modules.get('module_types', {}):
            arch_inferences.append("API-driven architecture with separate endpoint definitions")
        if 'service' in modules.get('module_types', {}):
            arch_inferences.append("Service layer separating business logic from presentation")
        if 'repository' in modules.get('module_types', {}):
            arch_inferences.append("Repository pattern for data access abstraction")

        if arch_inferences:
            report.append(f"### Inferred Architectural Patterns")
            report.append(f"")
            for inference in arch_inferences:
                report.append(f"- {inference}")
            report.append(f"")

        report.append(f"### Recommended Extension Paths")
        report.append(f"")
        report.append(f"1. **Add new features** in appropriate service/module directories")
        report.append(f"2. **Extend APIs** by adding new endpoints in API directories")
        report.append(f"3. **Add tests** in corresponding test directories")
        report.append(f"4. **Update configuration** in config files for new features")
        report.append(f"")

        # 7. Quick Start Guide
        report.append(f"## 7. Quick Start Guide")
        report.append(f"")

        onboarding = self.report_data['onboarding']
        report.append(f"### Recommended Reading Order")
        report.append(f"")
        for item in onboarding.get('reading_order', []):
            report.append(item)
        report.append(f"")

        report.append(f"### Safe Modification Points")
        report.append(f"")
        for point in onboarding.get('safe_modification_points', []):
            report.append(point)
        report.append(f"")

        report.append(f"### First Week Goals")
        report.append(f"")
        for goal in onboarding.get('first_week_goals', []):
            report.append(goal)
        report.append(f"")

        # 8. Risk Assessment (if any)
        risks = self.report_data['risks']
        if risks.get('has_risks'):
            report.append(f"## 8. Risk Points & Considerations")
            report.append(f"")

            if risks.get('potential_risks'):
                report.append(f"### Potential Risks")
                report.append(f"")
                for risk in risks.get('potential_risks', []):
                    report.append(f"- ⚠️ {risk}")
                report.append(f"")

            if risks.get('complex_points'):
                report.append(f"### Architectural Complexities")
                report.append(f"")
                for point in risks.get('complex_points', []):
                    report.append(f"- 🔄 {point}")
                report.append(f"")

            if risks.get('potential_pitfalls'):
                report.append(f"### Potential Pitfalls")
                report.append(f"")
                for pitfall in risks.get('potential_pitfalls', []):
                    report.append(f"- 💡 {pitfall}")
                report.append(f"")

        # Footer
        report.append(f"---")
        report.append(f"")
        report.append(f"*Report generated by Repo Analyzer Skill v1.0.0*")
        report.append(f"")

        report_text = "\n".join(report)

        # Write to file if output path specified
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            self.log(f"Report written to: {output_file}")

        return report_text

    def run_analysis(self):
        """Run the complete 8-step analysis."""
        self.log(f"Starting repository analysis for: {self.repo_path}")

        steps = [
            self.step1_global_scan,
            self.step2_project_positioning,
            self.step3_directory_structure,
            self.step4_tech_stack_analysis,
            self.step5_core_modules,
            self.step6_execution_workflows,
            self.step7_onboarding_guide,
            self.step8_risk_assessment
        ]

        for i, step in enumerate(steps, 1):
            try:
                self.log(f"Running Step {i}/8...")
                step()
            except Exception as e:
                self.log(f"Error in step {i}: {e}")

        self.log("Analysis complete!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Code repository analysis and technical documentation generation tool'
    )
    parser.add_argument(
        'repository_path',
        help='Path to the repository to analyze'
    )
    parser.add_argument(
        '--output',
        default='repo_analysis_report.md',
        help='Output file path for the report (default: repo_analysis_report.md)'
    )
    parser.add_argument(
        '--depth',
        type=int,
        default=2,
        help='Directory scanning depth (default: 2)'
    )
    parser.add_argument(
        '--include-risks',
        type=lambda x: x.lower() == 'true',
        default=True,
        help='Include risk assessment section (default: true)'
    )
    parser.add_argument(
        '--verbose',
        type=lambda x: x.lower() == 'true',
        default=False,
        help='Enable verbose logging (default: false)'
    )

    args = parser.parse_args()

    # Validate repository path
    repo_path = Path(args.repository_path)
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)

    if not repo_path.is_dir():
        print(f"Error: Path is not a directory: {repo_path}")
        sys.exit(1)

    # Create analyzer and run analysis
    analyzer = RepoAnalyzer(
        repo_path=args.repository_path,
        depth=args.depth,
        verbose=args.verbose
    )

    analyzer.run_analysis()

    # Generate report
    report = analyzer.generate_report(output_path=args.output)

    print(f"\n[SUCCESS] Analysis complete!")
    print(f"[INFO] Repository: {repo_path}")
    print(f"[INFO] Report saved to: {args.output}")
    print(f"\nSummary:")
    print(f"  - Files: {analyzer.report_data['overview'].get('total_files', 0)}")
    print(f"  - Directories: {analyzer.report_data['overview'].get('total_dirs', 0)}")
    print(f"  - Languages: {len(analyzer.report_data['overview'].get('languages', {}))}")
    print(f"  - Dependency files: {len(analyzer.report_data['tech_stack'].get('dependency_files_found', []))}")

    if analyzer.report_data['risks'].get('has_risks'):
        print(f"  [WARNING] Risks identified: {len(analyzer.report_data['risks'].get('potential_risks', []))}")


if __name__ == '__main__':
    main()