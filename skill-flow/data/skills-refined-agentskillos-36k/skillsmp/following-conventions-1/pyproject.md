# pyproject.toml Configuration

Standard project metadata for Tenzir Python projects.

```toml
[project]
name = "tenzir-<project>"
version = "0.1.0"
description = "Short description of the project."
readme = "README.md"
requires-python = ">=3.12"
authors = [{ name = "Tenzir", email = "engineering@tenzir.com" }]
maintainers = [{ name = "Tenzir Engineering", email = "engineering@tenzir.com" }]
license = { text = "Apache-2.0" }
keywords = ["tenzir", ...]
classifiers = [
  "Development Status :: 3 - Alpha",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: Apache Software License",
  "Operating System :: OS Independent",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
  "Typing :: Typed",
]
dependencies = [
  "click>=8.1",
]

[project.urls]
Homepage = "https://github.com/tenzir/<project>"
Repository = "https://github.com/tenzir/<project>"
"Bug Tracker" = "https://github.com/tenzir/<project>/issues"
Documentation = "https://docs.tenzir.com"

[project.scripts]
tenzir-<project> = "tenzir_<project>.cli:main"

[build-system]
requires = ["hatchling>=1.25.0"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/tenzir_<project>"]
```

## Key Points

- **Naming**: Use `tenzir-` prefix for package names, `tenzir_` for module names
- **Authors**: Always use `Tenzir` with `engineering@tenzir.com`
- **License**: Apache-2.0
- **Python**: Require 3.12+, list 3.12 and 3.13 in classifiers
- **Typed**: Include `Typing :: Typed` classifier
- **Build**: Use Hatchling as build backend
- **URLs**: Point to GitHub repo and docs.tenzir.com
