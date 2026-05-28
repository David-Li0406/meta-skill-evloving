#!/bin/bash
# macOS Project Structure Analyzer
# Usage: bash scripts/macos-project-analyzer.sh [project_path]
#
# This script analyzes a macOS project and reports:
# - Project type and configuration
# - macOS-specific features detected
# - Window and scene management patterns
# - Menu and commands setup
# - Document-based app patterns
# - Entitlements and sandbox configuration

set -e

PROJECT_PATH="${1:-.}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== macOS Project Analysis ===${NC}"
echo -e "Path: ${PROJECT_PATH}"
echo ""

# MARK: - Project Files

echo -e "${YELLOW}## Project Files${NC}"
XCODEPROJ=$(find "$PROJECT_PATH" -maxdepth 2 -name "*.xcodeproj" -print -quit 2>/dev/null)
XCWORKSPACE=$(find "$PROJECT_PATH" -maxdepth 2 -name "*.xcworkspace" -not -path "*/xcodeproj/*" -print -quit 2>/dev/null)

if [ -n "$XCWORKSPACE" ]; then
    echo -e "  ${GREEN}✓${NC} Workspace: $(basename "$XCWORKSPACE")"
fi

if [ -n "$XCODEPROJ" ]; then
    echo -e "  ${GREEN}✓${NC} Project: $(basename "$XCODEPROJ")"
fi

if [ -z "$XCODEPROJ" ] && [ -z "$XCWORKSPACE" ]; then
    echo -e "  ${RED}✗${NC} No Xcode project found"
fi

echo ""

# MARK: - Swift Files Statistics

echo -e "${YELLOW}## Swift Files Statistics${NC}"
SWIFT_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -not -path "*/.*" -not -path "*/.build/*" -not -path "*/Pods/*" 2>/dev/null | wc -l | xargs)
echo -e "  Total Swift files: ${GREEN}${SWIFT_COUNT}${NC}"

TEST_COUNT=$(find "$PROJECT_PATH" -name "*Tests.swift" -not -path "*/.*" 2>/dev/null | wc -l | xargs)
echo -e "  Test files: ${GREEN}${TEST_COUNT}${NC}"

echo ""

# MARK: - macOS Target Detection

echo -e "${YELLOW}## macOS Target Detection${NC}"

# Check for macOS imports
APPKIT_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -exec grep -l "import AppKit" {} \; 2>/dev/null | wc -l | xargs)
if [ "$APPKIT_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✓${NC} AppKit (${APPKIT_COUNT} files)"
fi

SWIFTUI_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -exec grep -l "import SwiftUI" {} \; 2>/dev/null | wc -l | xargs)
if [ "$SWIFTUI_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✓${NC} SwiftUI (${SWIFTUI_COUNT} files)"
fi

# Check for platform-specific code
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "#if os(macOS)" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Platform-specific code (#if os(macOS)) detected"
fi

echo ""

# MARK: - Scene Types

echo -e "${YELLOW}## Scene Types${NC}"

# WindowGroup
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "WindowGroup" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} WindowGroup detected"
fi

# Window (single instance)
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "Window(" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Window (single instance) detected"
fi

# DocumentGroup
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "DocumentGroup" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} DocumentGroup detected (Document-based app)"
fi

# Settings
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "Settings {" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Settings scene detected"
fi

# MenuBarExtra
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "MenuBarExtra" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} MenuBarExtra detected (Status bar app)"
fi

echo ""

# MARK: - Window Management

echo -e "${YELLOW}## Window Management${NC}"

# openWindow
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "openWindow" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Programmatic window opening (openWindow)"
fi

# NavigationSplitView
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "NavigationSplitView" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} NavigationSplitView detected"
fi

# Inspector
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "\.inspector(" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Inspector panel detected"
fi

# Window size modifiers
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "defaultSize\|windowResizability" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Window size configuration detected"
fi

echo ""

# MARK: - Menu and Commands

echo -e "${YELLOW}## Menu and Commands${NC}"

# Commands
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "Commands" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Commands detected"
fi

# CommandGroup
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "CommandGroup" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} CommandGroup detected"
fi

# CommandMenu
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "CommandMenu" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Custom CommandMenu detected"
fi

# Keyboard shortcuts
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "keyboardShortcut" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Keyboard shortcuts detected"
fi

# FocusedValue/FocusedBinding
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "@FocusedValue\|@FocusedBinding\|FocusedValueKey" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} FocusedValue/FocusedBinding detected"
fi

echo ""

# MARK: - Document Support

echo -e "${YELLOW}## Document Support${NC}"

# FileDocument
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "FileDocument" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} FileDocument protocol detected"
fi

# ReferenceFileDocument
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "ReferenceFileDocument" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} ReferenceFileDocument protocol detected"
fi

# UTType
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "UTType\|UniformTypeIdentifiers" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} UTType (Uniform Type Identifiers) detected"
fi

# UndoManager
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "undoManager\|UndoManager" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} UndoManager detected"
fi

echo ""

# MARK: - State Management

echo -e "${YELLOW}## State Management${NC}"

# @Observable (macOS 14+)
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "@Observable" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} @Observable (macOS 14+) detected"
fi

# @AppStorage
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "@AppStorage" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} @AppStorage detected (User Defaults)"
fi

# @SceneStorage
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "@SceneStorage" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} @SceneStorage detected (Window state)"
fi

# ObservableObject (Legacy)
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "ObservableObject" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${YELLOW}⚠${NC} ObservableObject (Legacy) - consider @Observable"
fi

echo ""

# MARK: - Data Layer

echo -e "${YELLOW}## Data Layer${NC}"

# SwiftData
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "import SwiftData\|@Model" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} SwiftData detected"
fi

# Core Data
COREDATA_COUNT=$(find "$PROJECT_PATH" -name "*.xcdatamodeld" 2>/dev/null | wc -l | xargs)
if [ "$COREDATA_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✓${NC} Core Data (${COREDATA_COUNT} models)"
fi

echo ""

# MARK: - System Integration

echo -e "${YELLOW}## System Integration${NC}"

# UserNotifications
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "UserNotifications\|UNUserNotificationCenter" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} UserNotifications detected"
fi

# NSWorkspace
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "NSWorkspace" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} NSWorkspace integration detected"
fi

# CoreSpotlight
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "CoreSpotlight\|CSSearchableItem" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Core Spotlight integration detected"
fi

# WidgetKit
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "WidgetKit\|TimelineProvider" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} WidgetKit detected"
fi

echo ""

# MARK: - Drag & Drop

echo -e "${YELLOW}## Drag & Drop${NC}"

# Transferable
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "Transferable" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Transferable protocol detected"
fi

# Draggable/DropDestination
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "\.draggable\|\.dropDestination" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Drag and drop modifiers detected"
fi

# NSPasteboard
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "NSPasteboard" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} NSPasteboard (pasteboard operations)"
fi

echo ""

# MARK: - Entitlements

echo -e "${YELLOW}## Entitlements & Sandbox${NC}"

ENTITLEMENTS=$(find "$PROJECT_PATH" -name "*.entitlements" -print -quit 2>/dev/null)
if [ -n "$ENTITLEMENTS" ]; then
    echo -e "  ${GREEN}✓${NC} Entitlements file found: $(basename "$ENTITLEMENTS")"

    # Check for common entitlements
    if grep -q "com.apple.security.app-sandbox" "$ENTITLEMENTS" 2>/dev/null; then
        echo -e "    ${CYAN}→${NC} App Sandbox enabled"
    fi

    if grep -q "com.apple.security.network.client" "$ENTITLEMENTS" 2>/dev/null; then
        echo -e "    ${CYAN}→${NC} Network client access"
    fi

    if grep -q "com.apple.security.files.user-selected" "$ENTITLEMENTS" 2>/dev/null; then
        echo -e "    ${CYAN}→${NC} User-selected file access"
    fi

    if grep -q "com.apple.security.files.bookmarks" "$ENTITLEMENTS" 2>/dev/null; then
        echo -e "    ${CYAN}→${NC} Security-scoped bookmarks"
    fi

    if grep -q "hardened-runtime" "$ENTITLEMENTS" 2>/dev/null; then
        echo -e "    ${CYAN}→${NC} Hardened Runtime"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} No entitlements file found"
fi

echo ""

# MARK: - Package Dependencies

echo -e "${YELLOW}## Package Dependencies${NC}"

# Swift Package Manager
if [ -f "$PROJECT_PATH/Package.swift" ]; then
    echo -e "  ${GREEN}✓${NC} Swift Package Manager (Package.swift)"
    PKG_COUNT=$(grep -c "\.package(" "$PROJECT_PATH/Package.swift" 2>/dev/null || echo 0)
    echo "    Packages: ${PKG_COUNT}"
fi

# Check for resolved packages
if [ -f "$PROJECT_PATH/Package.resolved" ]; then
    RESOLVED_COUNT=$(grep -c '"identity"' "$PROJECT_PATH/Package.resolved" 2>/dev/null || echo 0)
    echo -e "  Resolved packages: ${GREEN}${RESOLVED_COUNT}${NC}"
fi

echo ""

# MARK: - Code Quality

echo -e "${YELLOW}## Code Quality${NC}"

# SwiftLint
if [ -f "$PROJECT_PATH/.swiftlint.yml" ]; then
    echo -e "  ${GREEN}✓${NC} SwiftLint configured"
fi

# SwiftFormat
if [ -f "$PROJECT_PATH/.swiftformat" ]; then
    echo -e "  ${GREEN}✓${NC} SwiftFormat configured"
fi

echo ""
echo -e "${BLUE}=== Analysis Complete ===${NC}"
