#!/bin/bash
#
# JUCE VST Plugin Build Script
# Builds VST3, AU, and Standalone targets using CMake and Ninja
#
# Usage:
#   ./scripts/build.sh [plugin_directory] [build_type]
#
# Arguments:
#   plugin_directory - Path to the plugin project (default: current directory)
#   build_type       - Release or Debug (default: Release)
#
# Example:
#   ./scripts/build.sh /path/to/MyPlugin Release
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
PLUGIN_DIR="${1:-.}"
BUILD_TYPE="${2:-Release}"
BUILD_DIR="build"

# Print colored message
print_status() {
    echo -e "${CYAN}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}==>${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}==>${NC} $1"
}

print_error() {
    echo -e "${RED}==>${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."

    # Check CMake
    if ! command -v cmake &> /dev/null; then
        print_error "CMake is not installed. Install with: brew install cmake"
        exit 1
    fi
    echo "  CMake: $(cmake --version | head -n1)"

    # Check Ninja (preferred) or Make
    if command -v ninja &> /dev/null; then
        GENERATOR="Ninja"
        echo "  Generator: Ninja"
    elif command -v make &> /dev/null; then
        GENERATOR="Unix Makefiles"
        echo "  Generator: Make"
    else
        print_error "Neither Ninja nor Make found. Install with: brew install ninja"
        exit 1
    fi

    # Check C++ compiler
    if command -v clang++ &> /dev/null; then
        echo "  Compiler: $(clang++ --version | head -n1)"
    elif command -v g++ &> /dev/null; then
        echo "  Compiler: $(g++ --version | head -n1)"
    else
        print_error "No C++ compiler found"
        exit 1
    fi
}

# Navigate to plugin directory
navigate_to_plugin() {
    if [ ! -d "$PLUGIN_DIR" ]; then
        print_error "Plugin directory not found: $PLUGIN_DIR"
        exit 1
    fi

    cd "$PLUGIN_DIR"
    print_status "Building plugin in: $(pwd)"

    if [ ! -f "CMakeLists.txt" ]; then
        print_error "CMakeLists.txt not found in $PLUGIN_DIR"
        exit 1
    fi
}

# Configure with CMake
configure_build() {
    print_status "Configuring CMake build..."

    cmake -B "$BUILD_DIR" \
        -G "$GENERATOR" \
        -DCMAKE_BUILD_TYPE="$BUILD_TYPE" \
        -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64" \
        -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

    if [ $? -eq 0 ]; then
        print_success "Configuration complete"
    else
        print_error "Configuration failed"
        exit 1
    fi
}

# Build the plugin
build_plugin() {
    print_status "Building plugin ($BUILD_TYPE)..."

    # Determine number of parallel jobs
    if [ "$(uname)" == "Darwin" ]; then
        JOBS=$(sysctl -n hw.ncpu)
    else
        JOBS=$(nproc)
    fi

    cmake --build "$BUILD_DIR" --config "$BUILD_TYPE" -j "$JOBS"

    if [ $? -eq 0 ]; then
        print_success "Build complete"
    else
        print_error "Build failed"
        exit 1
    fi
}

# Find and display plugin outputs
show_outputs() {
    print_status "Plugin outputs:"

    # Find the plugin name from CMakeLists.txt
    PLUGIN_NAME=$(grep -m1 "^project(" CMakeLists.txt | sed 's/project(\([^ ]*\).*/\1/')

    ARTEFACTS_DIR="$BUILD_DIR/${PLUGIN_NAME}_artefacts/$BUILD_TYPE"

    if [ -d "$ARTEFACTS_DIR" ]; then
        echo ""

        # VST3
        VST3_PATH="$ARTEFACTS_DIR/VST3"
        if [ -d "$VST3_PATH" ]; then
            VST3_FILE=$(find "$VST3_PATH" -name "*.vst3" -type d 2>/dev/null | head -n1)
            if [ -n "$VST3_FILE" ]; then
                echo -e "  ${GREEN}VST3:${NC} $VST3_FILE"
            fi
        fi

        # AU
        AU_PATH="$ARTEFACTS_DIR/AU"
        if [ -d "$AU_PATH" ]; then
            AU_FILE=$(find "$AU_PATH" -name "*.component" -type d 2>/dev/null | head -n1)
            if [ -n "$AU_FILE" ]; then
                echo -e "  ${GREEN}AU:${NC} $AU_FILE"
            fi
        fi

        # Standalone
        STANDALONE_PATH="$ARTEFACTS_DIR/Standalone"
        if [ -d "$STANDALONE_PATH" ]; then
            APP_FILE=$(find "$STANDALONE_PATH" -name "*.app" -type d 2>/dev/null | head -n1)
            if [ -n "$APP_FILE" ]; then
                echo -e "  ${GREEN}Standalone:${NC} $APP_FILE"
            fi
        fi

        echo ""
    else
        print_warning "Artefacts directory not found: $ARTEFACTS_DIR"
    fi
}

# Install plugins to system locations
install_plugins() {
    if [ "${3:-}" != "--install" ]; then
        return
    fi

    print_status "Installing plugins to system locations..."

    PLUGIN_NAME=$(grep -m1 "^project(" CMakeLists.txt | sed 's/project(\([^ ]*\).*/\1/')
    ARTEFACTS_DIR="$BUILD_DIR/${PLUGIN_NAME}_artefacts/$BUILD_TYPE"

    # VST3
    VST3_SRC="$ARTEFACTS_DIR/VST3/${PLUGIN_NAME}.vst3"
    VST3_DEST="$HOME/Library/Audio/Plug-Ins/VST3/"
    if [ -d "$VST3_SRC" ]; then
        print_status "Installing VST3..."
        mkdir -p "$VST3_DEST"
        rm -rf "${VST3_DEST}${PLUGIN_NAME}.vst3"
        cp -r "$VST3_SRC" "$VST3_DEST"
        print_success "VST3 installed to $VST3_DEST"
    fi

    # AU
    AU_SRC="$ARTEFACTS_DIR/AU/${PLUGIN_NAME}.component"
    AU_DEST="$HOME/Library/Audio/Plug-Ins/Components/"
    if [ -d "$AU_SRC" ]; then
        print_status "Installing AU..."
        mkdir -p "$AU_DEST"
        rm -rf "${AU_DEST}${PLUGIN_NAME}.component"
        cp -r "$AU_SRC" "$AU_DEST"
        print_success "AU installed to $AU_DEST"

        # Refresh AU cache
        print_status "Refreshing Audio Unit cache..."
        killall -9 AudioComponentRegistrar 2>/dev/null || true
    fi

    echo ""
    print_success "Installation complete! Rescan plugins in your DAW."
}

# Main execution
main() {
    echo ""
    echo "=========================================="
    echo "   JUCE VST Plugin Build Script"
    echo "=========================================="
    echo ""

    check_prerequisites
    navigate_to_plugin
    configure_build
    build_plugin
    show_outputs
    install_plugins "$@"

    echo ""
    print_success "Build finished successfully!"
    echo ""
}

# Run main function
main "$@"
