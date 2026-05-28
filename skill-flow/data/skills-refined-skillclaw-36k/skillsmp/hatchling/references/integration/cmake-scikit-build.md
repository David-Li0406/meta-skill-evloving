---
category: integration
topics: [cmake, scikit-build-core, compiled-extensions, build-hooks, c-extensions]
related: [./extension-modules.md]
---

# CMake & scikit-build Integration

Reference guide for helping users build C/C++/Rust extensions and compiled modules with hatchling using scikit-build-core. Use this when assisting with compiled extension development and CMake integration.

## Overview

Hatchling alone handles pure Python packages. For projects with compiled components, use **scikit-build-core**, a modern CMake adaptor that integrates with hatchling as a build hook.

### Key Differences

| Approach                  | Use Case             | Configuration            |
| ------------------------- | -------------------- | ------------------------ |
| Pure hatchling            | Python-only packages | `[build-system]` only    |
| Hatchling + scikit-build  | C/C++ extensions     | `[build-system]` + CMake |
| Old setuptools.Extension  | Legacy projects      | setup.py with distutils  |
| scikit-build (deprecated) | Old projects         | setup.py based           |

---

## Scikit-build-core Architecture

### How It Works

```text
1. User runs: pip install -e .
   ↓
2. pip calls hatchling's build_editable()
   ↓
3. Hatchling executes build hooks
   ↓
4. scikit-build-core hook runs CMake
   ↓
5. CMake compiles C/C++/Rust code
   ↓
6. Hatchling packages compiled .so/.pyd files into wheel
   ↓
7. pip installs wheel (now with compiled binaries)
```

### Why This Design

- **Separation of concerns**: CMake handles compilation, hatchling handles packaging
- **Modern standards**: Uses PEP 517 hooks, not custom setup.py commands
- **Isolation**: Build environment is clean, reproducible
- **Flexibility**: Supports any language CMake can compile (C, C++, Rust, Fortran, etc.)

---

## Basic Setup

### Minimal Configuration

**pyproject.toml**:

```toml
[build-system]
requires = ["hatchling", "scikit-build-core~=0.9"]
build-backend = "hatchling.build"

[project]
name = "myextension"
version = "0.1.0"

[tool.hatch.build.targets.wheel.hooks.scikit-build]
experimental = true
```

**CMakeLists.txt** (in project root):

```cmake
cmake_minimum_required(VERSION 3.15)
project(myextension)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

add_library(myext MODULE src/myext.cpp)
target_link_libraries(myext PRIVATE Python::Module)

set_target_properties(myext PROPERTIES
    PREFIX ""
    SUFFIX ${Python_SOABI_SUFFIX}
)

install(TARGETS myext DESTINATION myextension)
```

### Project Structure

```text
myextension/
├── CMakeLists.txt          # Build configuration
├── pyproject.toml          # Package metadata
├── README.md
├── src/
│   └── myext.cpp           # C++ extension source
└── myextension/
    ├── __init__.py         # Python package
    └── _ext.pyi            # Type hints (optional)
```

---

## CMakeLists.txt Essentials

### Finding Python Development Headers

```cmake
# Required for compiled extensions
find_package(Python COMPONENTS
    Interpreter          # Python executable
    Development.Module   # Headers and libraries
    REQUIRED
)
```

**Important**: Use `Development.Module`, not `Development`, as `Development` includes embedding components not relevant for extensions.

### Creating Extension Modules

```cmake
# Python extension module (compiled shared library)
add_library(myext MODULE src/myext.cpp)

# Link against Python libraries
target_link_libraries(myext PRIVATE Python::Module)

# Configure for proper loading
set_target_properties(myext PROPERTIES
    PREFIX ""                          # Remove lib prefix
    SUFFIX ${Python_SOABI_SUFFIX}     # Use Python ABI suffix
    POSITION_INDEPENDENT_CODE ON
)

# Install to package directory
install(TARGETS myext DESTINATION myextension)
```

### Accessing scikit-build Variables

```cmake
# scikit-build-core provides these useful variables:
# ${SKBUILD}                    - "2" (scikit-build-core version)
# ${SKBUILD_PROJECT_NAME}       - Project name from pyproject.toml
# ${SKBUILD_PROJECT_VERSION}    - Full version string
# ${SKBUILD_STATE}              - "wheel", "sdist", "editable", etc.

if(SKBUILD)
    message(STATUS "Building with scikit-build-core")
    message(STATUS "Project: ${SKBUILD_PROJECT_NAME} v${SKBUILD_PROJECT_VERSION}")
endif()
```

---

## Python/C++ Integration

### Using pybind11

```cmake
# Add pybind11
find_package(pybind11 REQUIRED)

# Create extension
pybind11_add_module(myext src/myext.cpp)

# Install
install(TARGETS myext DESTINATION myextension)
```

**Build configuration**:

```toml
[build-system]
requires = [
    "hatchling",
    "scikit-build-core~=0.9",
    "pybind11>=2.6",
]
```

### Using cffi

```cmake
# cffi generates C code, which we compile
add_library(myext MODULE ${CFFI_C_FILE})
target_link_libraries(myext PRIVATE Python::Module)
```

### Using SWIG

```cmake
find_package(SWIG REQUIRED)
include(UseSWIG)

set_source_files_properties(myext.i PROPERTIES CPLUSPLUS ON)
swig_add_library(myext
    TYPE SHARED
    LANGUAGE python
    SOURCES myext.i myext.cpp
)
```

---

## Dependencies & Build Requirements

### External Dependencies

```toml
[build-system]
requires = [
    "hatchling",
    "scikit-build-core~=0.9",
]

[project]
dependencies = [
    "numpy>=1.20",      # Runtime dependency
]
```

### Build-Time Only Dependencies

```toml
# In build requirements, not runtime
[build-system]
requires = [
    "hatchling",
    "scikit-build-core~=0.9",
    "pybind11>=2.6",    # Build-only
    "numpy>=1.20",      # Needed at build time
]

[project]
dependencies = [
    "numpy>=1.20",      # Also needed at runtime
]
```

---

## Advanced Configuration

### Conditional Compilation

```cmake
# Check platform
if(WIN32)
    add_compile_definitions(PLATFORM_WINDOWS)
elseif(APPLE)
    add_compile_definitions(PLATFORM_MACOS)
else()
    add_compile_definitions(PLATFORM_LINUX)
endif()

# Check Python version
if(Python_VERSION_MINOR GREATER_EQUAL 10)
    add_compile_definitions(PYTHON_310_PLUS)
endif()
```

### Linking External Libraries

```cmake
# System libraries
find_package(OpenSSL REQUIRED)
target_link_libraries(myext PRIVATE OpenSSL::Crypto)

# Bundled libraries
add_subdirectory(extern/zlib)
target_link_libraries(myext PRIVATE zlibstatic)
```

### Configuration Options

```toml
[tool.scikit-build]
cmake.minimum-version = "3.20"
cmake.build-type = "Release"

# Pass options to CMake
cmake.define = {
    "CMAKE_CXX_STANDARD" = "17",
    "MY_CUSTOM_OPTION" = "ON",
}
```

---

## Building & Testing

### Build Wheel

```bash
# Using hatchling (with scikit-build hook)
pip install -e .

# Or using build tool
pip install build
python -m build
```

### Editable Install

```bash
# Install for development (triggers CMake build)
pip install -e .

# Python code changes: work immediately
# C++ code changes: must rebuild
pip install -e .  # Rerun after C++ edits
```

### Testing

```bash
# Test the compiled extension
python -c "import myextension; myextension.myext.my_function()"

# Run test suite
pytest
```

### Incremental Builds

CMake caches build artifacts:

```bash
# Initial build (slow, compiles everything)
pip install -e .

# Second install (fast, reuses compilation)
pip install -e .

# Force rebuild
rm -rf build/
pip install -e .
```

---

## Troubleshooting

### Problem: CMake Not Found

```text
ERROR: Could not find CMake
```

**Solution**:

```bash
# Install cmake
pip install cmake

# Or system package manager
# Ubuntu: apt install cmake
# macOS: brew install cmake
# Windows: choco install cmake
```

### Problem: Python Development Headers Not Found

```text
ERROR: Could not find Python development headers
```

**Solution**:

```bash
# Ubuntu
sudo apt install python3-dev

# macOS (homebrew python)
python-config --includes

# Verify Python has development headers
python -m sysconfig
```

### Problem: ABI/Binary Incompatibility

```text
ImportError: cannot import name 'myext'
```

**Causes**:

- Built with different Python version than running Python
- Using wrong `Python_SOABI_SUFFIX`

**Solution**:

```bash
# Verify Python versions match
python --version

# Rebuild if Python upgraded
pip install -e . --force-reinstall
```

### Problem: Module Not Found After Install

```text
ModuleNotFoundError: No module named 'myextension'
```

**Solution**: Verify installation worked:

```bash
python -c "import myextension; print(myextension.__file__)"
```

---

## Real-World Example: NumPy-Style Extension

### Project Structure

```text
numerics/
├── CMakeLists.txt
├── pyproject.toml
├── src/
│   └── _numerics.cpp
└── numerics/
    ├── __init__.py
    └── _numerics.pyi
```

### pyproject.toml

```toml
[build-system]
requires = [
    "hatchling",
    "scikit-build-core~=0.9",
    "numpy>=1.20",
]
build-backend = "hatchling.build"

[project]
name = "numerics"
version = "1.0.0"
description = "Numerics with C++ acceleration"
dependencies = ["numpy>=1.20"]

[tool.scikit-build]
cmake.version = ">=3.15"
cmake.build-type = "Release"

[tool.hatch.build.targets.wheel.hooks.scikit-build]
experimental = true
```

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.15)
project(numerics)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(NumPy REQUIRED)

add_library(_numerics MODULE src/_numerics.cpp)

target_link_libraries(_numerics PRIVATE Python::Module NumPy::NumPy)

set_target_properties(_numerics PROPERTIES
    PREFIX ""
    SUFFIX ${Python_SOABI_SUFFIX}
)

install(TARGETS _numerics DESTINATION numerics)
```

### Building

```bash
# Install with compiled extension
pip install -e .

# Use in Python
python -c "from numerics import _numerics; print(_numerics.my_function())"
```

---

## Rust Extensions

For Rust, use **maturin** instead:

```toml
[build-system]
requires = ["hatchling", "maturin"]
build-backend = "hatchling.build"
```

Or **PyO3** with scikit-build-core (advanced).

---

## Resources

- [scikit-build-core Documentation](https://scikit-build-core.readthedocs.io/)
- [pybind11 Documentation](https://pybind11.readthedocs.io/)
- [CMake Documentation](https://cmake.org/documentation/)
- [Python Extending Documentation](https://docs.python.org/3/extending/)

**Key Takeaway**: Scikit-build-core provides a clean, modern way to build extensions with hatchling, handling the CMake → Python integration seamlessly.
