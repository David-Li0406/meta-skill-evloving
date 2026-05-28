#!/bin/bash
# iOS Project Structure Analyzer
# Usage: bash scripts/project-analyzer.sh [project_path]
#
# This script analyzes an iOS project and reports:
# - Project type and configuration
# - Architecture patterns detected
# - UI framework usage
# - Data layer setup
# - Test coverage
# - Dependencies

set -e

PROJECT_PATH="${1:-.}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== iOS Project Analysis ===${NC}"
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

UITEST_COUNT=$(find "$PROJECT_PATH" -name "*UITests.swift" -not -path "*/.*" 2>/dev/null | wc -l | xargs)
echo -e "  UI Test files: ${GREEN}${UITEST_COUNT}${NC}"

echo ""

# MARK: - Architecture Detection

echo -e "${YELLOW}## Architecture Patterns${NC}"

# TCA Detection
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "ComposableArchitecture\|@Reducer" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} TCA (The Composable Architecture) detected"
fi

# MVVM Detection
VIEWMODEL_COUNT=$(find "$PROJECT_PATH" -name "*ViewModel.swift" 2>/dev/null | wc -l | xargs)
if [ "$VIEWMODEL_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✓${NC} MVVM pattern detected (${VIEWMODEL_COUNT} ViewModels)"
fi

# Clean Architecture Detection
USECASE_COUNT=$(find "$PROJECT_PATH" -name "*UseCase.swift" 2>/dev/null | wc -l | xargs)
REPOSITORY_COUNT=$(find "$PROJECT_PATH" -name "*Repository.swift" 2>/dev/null | wc -l | xargs)
if [ "$USECASE_COUNT" -gt 0 ] || [ "$REPOSITORY_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✓${NC} Clean Architecture detected (${USECASE_COUNT} UseCases, ${REPOSITORY_COUNT} Repositories)"
fi

# Observable Detection (iOS 17+)
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "@Observable" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} @Observable (iOS 17+) detected"
fi

# ObservableObject Detection (Legacy)
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "ObservableObject\|@StateObject\|@ObservedObject" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${YELLOW}⚠${NC} ObservableObject (Legacy) detected - consider migrating to @Observable"
fi

echo ""

# MARK: - UI Framework

echo -e "${YELLOW}## UI Framework${NC}"

SWIFTUI_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -exec grep -l "import SwiftUI" {} \; 2>/dev/null | wc -l | xargs)
UIKIT_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -exec grep -l "import UIKit" {} \; 2>/dev/null | wc -l | xargs)

if [ "$SWIFTUI_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✓${NC} SwiftUI (${SWIFTUI_COUNT} files)"
fi

if [ "$UIKIT_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✓${NC} UIKit (${UIKIT_COUNT} files)"
fi

# Storyboard Detection
STORYBOARD_COUNT=$(find "$PROJECT_PATH" -name "*.storyboard" 2>/dev/null | wc -l | xargs)
if [ "$STORYBOARD_COUNT" -gt 0 ]; then
    echo -e "  ${YELLOW}⚠${NC} Storyboards (${STORYBOARD_COUNT} files)"
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

# Realm
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "import RealmSwift\|import Realm" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Realm detected"
fi

echo ""

# MARK: - Networking

echo -e "${YELLOW}## Networking${NC}"

# Alamofire
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "import Alamofire" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Alamofire detected"
fi

# Moya
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "import Moya" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} Moya detected"
fi

# URLSession with async/await
if find "$PROJECT_PATH" -name "*.swift" -exec grep -l "URLSession.*async\|await.*data(for:" {} \; 2>/dev/null | head -1 | grep -q .; then
    echo -e "  ${GREEN}✓${NC} URLSession with async/await detected"
fi

echo ""

# MARK: - Dependencies

echo -e "${YELLOW}## Package Dependencies${NC}"

# Swift Package Manager
if [ -f "$PROJECT_PATH/Package.swift" ]; then
    echo -e "  ${GREEN}✓${NC} Swift Package Manager (Package.swift)"
    echo "  Dependencies:"
    grep -E "\.package\(" "$PROJECT_PATH/Package.swift" 2>/dev/null | head -10 | while read -r line; do
        echo "    - $(echo "$line" | sed 's/.*url: "\([^"]*\)".*/\1/' | sed 's/.*path: "\([^"]*\)".*/\1/')"
    done
fi

# Check for resolved packages
if [ -f "$PROJECT_PATH/Package.resolved" ]; then
    PKG_COUNT=$(grep -c '"identity"' "$PROJECT_PATH/Package.resolved" 2>/dev/null || echo 0)
    echo -e "  Resolved packages: ${GREEN}${PKG_COUNT}${NC}"
fi

# CocoaPods
if [ -f "$PROJECT_PATH/Podfile" ]; then
    echo -e "  ${GREEN}✓${NC} CocoaPods (Podfile)"
    POD_COUNT=$(grep -c "pod '" "$PROJECT_PATH/Podfile" 2>/dev/null || echo 0)
    echo "    Pods: ${POD_COUNT}"
fi

# Carthage
if [ -f "$PROJECT_PATH/Cartfile" ]; then
    echo -e "  ${GREEN}✓${NC} Carthage (Cartfile)"
fi

echo ""

# MARK: - CI/CD

echo -e "${YELLOW}## CI/CD Configuration${NC}"

# Xcode Cloud
if [ -d "$PROJECT_PATH/ci_scripts" ]; then
    echo -e "  ${GREEN}✓${NC} Xcode Cloud (ci_scripts/)"
fi

# fastlane
if [ -d "$PROJECT_PATH/fastlane" ]; then
    echo -e "  ${GREEN}✓${NC} fastlane"
fi

# GitHub Actions
if [ -d "$PROJECT_PATH/.github/workflows" ]; then
    WORKFLOW_COUNT=$(find "$PROJECT_PATH/.github/workflows" -name "*.yml" -o -name "*.yaml" 2>/dev/null | wc -l | xargs)
    echo -e "  ${GREEN}✓${NC} GitHub Actions (${WORKFLOW_COUNT} workflows)"
fi

# GitLab CI
if [ -f "$PROJECT_PATH/.gitlab-ci.yml" ]; then
    echo -e "  ${GREEN}✓${NC} GitLab CI"
fi

# Bitrise
if [ -f "$PROJECT_PATH/bitrise.yml" ]; then
    echo -e "  ${GREEN}✓${NC} Bitrise"
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
