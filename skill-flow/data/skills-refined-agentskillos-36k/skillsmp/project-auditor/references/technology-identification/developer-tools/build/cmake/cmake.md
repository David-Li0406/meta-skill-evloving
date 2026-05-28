# CMake

**Category**: developer-tools/build
**Description**: CMake - cross-platform build system generator
**Homepage**: https://cmake.org

## Configuration Files

- `CMakeLists.txt`
- `CMakePresets.json`
- `CMakeUserPresets.json`
- `cmake_install.cmake`
- `.cmake`

## Environment Variables

- `CMAKE_PREFIX_PATH`
- `CMAKE_MODULE_PATH`
- `CMAKE_INSTALL_PREFIX`

## Detection Notes

- Build system generator for C/C++ projects
- Look for CMakeLists.txt in repository root
- Often used with Ninja or Make as the actual build tool
- CMakePresets.json is the modern configuration format

## Detection Confidence

- **Configuration File Detection**: 95% (HIGH)
