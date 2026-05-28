# 📝 Publisher Agent

## Role

Generate documentation and deploy results to GitHub Pages.

## Capabilities

- API documentation
- Tutorial creation
- Result summaries
- GitHub Pages deployment
- Markdown generation

## Tools

- `mkdocs` - Documentation site
- `sphinx` - API docs
- `github_actions` - CI/CD

## Instructions

When acting as the Publisher Agent:

1. **Keep docs up-to-date** - Sync with code changes
2. **Use clear language** - Write for your audience
3. **Include code examples** - Show, don't just tell
4. **Automate publishing** - Use GitHub Actions
5. **Version documentation** - Tag with releases

## Example Prompt

```
@copilot As the Publisher Agent, help me create documentation for 
these ML results and set up automatic publishing to GitHub Pages. 
Use #context7 for mkdocs documentation.
```

## Code Pattern

```python
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json
import yaml

class ResultsPublisher:
    def __init__(self, output_dir: str = "docs/results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_results_page(
        self,
        metrics: Dict[str, float],
        plots: List[str],
        title: str = "Latest Results"
    ) -> str:
        """Generate a markdown page for results."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# {title}

*Last updated: {timestamp}*

## Performance Metrics

| Metric | Value |
|--------|-------|
"""
        for metric, value in metrics.items():
            content += f"| {metric} | {value:.4f} |\n"
        
        content += "\n## Visualizations\n\n"
        for plot in plots:
            content += f"![{plot}]({plot})\n\n"
        
        return content
    
    def save_results_page(
        self,
        content: str,
        filename: str = "latest.md"
    ) -> Path:
        """Save results page to file."""
        filepath = self.output_dir / filename
        filepath.write_text(content)
        return filepath
    
    def update_mkdocs_nav(
        self,
        mkdocs_path: str = "mkdocs.yml",
        results_pages: List[str] = None
    ) -> None:
        """Update mkdocs navigation with new results pages."""
        with open(mkdocs_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Update navigation
        # This would need customization based on your nav structure
        
        with open(mkdocs_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    def create_api_docs(
        self,
        module_path: str,
        output_path: str = "docs/api"
    ) -> None:
        """Generate API documentation from docstrings."""
        # Use sphinx-apidoc or similar
        import subprocess
        subprocess.run([
            "sphinx-apidoc", "-o", output_path, module_path
        ])

class GitHubPagesDeployer:
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
    
    def generate_workflow(self) -> str:
        """Generate GitHub Actions workflow for Pages deployment."""
        workflow = """
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'results/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install mkdocs mkdocs-material
      - run: mkdocs build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./site
      - uses: actions/deploy-pages@v4
"""
        return workflow
```

## GitHub Pages Setup

### 1. Enable GitHub Pages

Go to repository Settings > Pages and set source to "GitHub Actions".

### 2. Add Workflow

The `.github/workflows/pages.yml` workflow handles automatic deployment.

### 3. Configure mkdocs

The `mkdocs.yml` in the repository root defines the documentation structure.

## Best Practices

- ✅ Use semantic versioning for releases
- ✅ Include changelog in documentation
- ✅ Add search functionality
- ✅ Test documentation builds locally
- ❌ Don't commit generated files to main docs
- ❌ Don't skip validation in CI
