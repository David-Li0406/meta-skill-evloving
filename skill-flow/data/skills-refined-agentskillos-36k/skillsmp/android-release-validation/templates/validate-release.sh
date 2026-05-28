#!/bin/bash
# Android Release Build Validation Script
# This script validates release builds before deployment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_MODULE="app"
BUILD_TYPE="release"
VALIDATION_REPORT="validation-report.md"

# Counters
ERRORS=0
WARNINGS=0
CHECKS_PASSED=0
CHECKS_TOTAL=0

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
    ((CHECKS_TOTAL++))
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
    ((CHECKS_TOTAL++))
}

log_error() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
    ((CHECKS_TOTAL++))
}

check_command() {
    if command -v $1 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

echo "======================================"
echo "Android Release Build Validation"
echo "======================================"
echo ""

# Step 1: Check prerequisites
log_info "Checking prerequisites..."

if ! check_command "java"; then
    log_error "Java not found. Install JDK."
    exit 1
fi

if ! check_command "aapt"; then
    log_warning "aapt not found. Some checks will be skipped."
fi

if ! check_command "jarsigner"; then
    log_warning "jarsigner not found. Signature validation will be skipped."
fi

log_success "Prerequisites check complete"
echo ""

# Step 2: Clean build
log_info "Cleaning previous build outputs..."
./gradlew clean
log_success "Build cleaned"
echo ""

# Step 3: Build release APK
log_info "Building release APK..."
BUILD_START=$(date +%s)

if ./gradlew assembleRelease; then
    BUILD_END=$(date +%s)
    BUILD_TIME=$((BUILD_END - BUILD_START))
    log_success "APK built successfully in ${BUILD_TIME}s"
    
    APK_PATH="${APP_MODULE}/build/outputs/apk/release/${APP_MODULE}-release.apk"
    
    if [ -f "$APK_PATH" ]; then
        APK_SIZE=$(du -h "$APK_PATH" | cut -f1)
        log_info "APK size: $APK_SIZE"
        
        # Check APK size
        APK_SIZE_MB=$(du -m "$APK_PATH" | cut -f1)
        if [ $APK_SIZE_MB -gt 100 ]; then
            log_warning "APK size > 100MB. Consider optimization."
        elif [ $APK_SIZE_MB -gt 50 ]; then
            log_warning "APK size > 50MB. May want to optimize."
        else
            log_success "APK size is reasonable"
        fi
    else
        log_error "APK file not found at $APK_PATH"
    fi
else
    log_error "APK build failed"
fi
echo ""

# Step 4: Build release AAB
log_info "Building release AAB..."
BUILD_START=$(date +%s)

if ./gradlew bundleRelease; then
    BUILD_END=$(date +%s)
    BUILD_TIME=$((BUILD_END - BUILD_START))
    log_success "AAB built successfully in ${BUILD_TIME}s"
    
    AAB_PATH="${APP_MODULE}/build/outputs/bundle/release/${APP_MODULE}-release.aab"
    
    if [ -f "$AAB_PATH" ]; then
        AAB_SIZE=$(du -h "$AAB_PATH" | cut -f1)
        log_info "AAB size: $AAB_SIZE"
        log_success "AAB generated"
    else
        log_error "AAB file not found at $AAB_PATH"
    fi
else
    log_error "AAB build failed"
fi
echo ""

# Step 5: Validate ProGuard mapping
log_info "Checking ProGuard mapping file..."
MAPPING_PATH="${APP_MODULE}/build/outputs/mapping/release/mapping.txt"

if [ -f "$MAPPING_PATH" ]; then
    if [ -s "$MAPPING_PATH" ]; then
        MAPPING_SIZE=$(du -h "$MAPPING_PATH" | cut -f1)
        log_success "Mapping file exists and is not empty ($MAPPING_SIZE)"
    else
        log_error "Mapping file is empty"
    fi
else
    log_error "Mapping file not found. ProGuard/R8 may not be enabled."
fi
echo ""

# Step 6: Validate signing
log_info "Validating APK signature..."

if check_command "jarsigner" && [ -f "$APK_PATH" ]; then
    if jarsigner -verify -verbose "$APK_PATH" > /dev/null 2>&1; then
        log_success "APK is properly signed"
        
        # Check certificate details
        CERT_INFO=$(jarsigner -verify -verbose -certs "$APK_PATH" 2>&1 | grep "X.509" | head -1)
        log_info "Certificate: $CERT_INFO"
    else
        log_error "APK signature verification failed"
    fi
else
    log_warning "Skipping signature validation (jarsigner not available)"
fi
echo ""

# Step 7: Analyze APK with aapt
if check_command "aapt" && [ -f "$APK_PATH" ]; then
    log_info "Analyzing APK contents..."
    
    # Get package info
    PACKAGE_INFO=$(aapt dump badging "$APK_PATH" 2>&1)
    
    PACKAGE_NAME=$(echo "$PACKAGE_INFO" | grep "package: name=" | sed -n "s/.*name='\([^']*\)'.*/\1/p")
    VERSION_NAME=$(echo "$PACKAGE_INFO" | grep "versionName=" | sed -n "s/.*versionName='\([^']*\)'.*/\1/p")
    VERSION_CODE=$(echo "$PACKAGE_INFO" | grep "versionCode=" | sed -n "s/.*versionCode='\([^']*\)'.*/\1/p")
    
    log_info "Package: $PACKAGE_NAME"
    log_info "Version: $VERSION_NAME ($VERSION_CODE)"
    
    # Check target SDK
    TARGET_SDK=$(echo "$PACKAGE_INFO" | grep "targetSdkVersion:" | sed -n "s/.*targetSdkVersion:'\([^']*\)'.*/\1/p")
    log_info "Target SDK: $TARGET_SDK"
    
    if [ "$TARGET_SDK" -lt 33 ]; then
        log_warning "Target SDK < 33. Play Store requires 33+ for new apps."
    else
        log_success "Target SDK meets Play Store requirements"
    fi
    
    # Check for debug symbols
    if aapt list -v "$APK_PATH" | grep -i "debug" > /dev/null; then
        log_warning "Debug symbols found in release APK"
    else
        log_success "No debug symbols in release (as expected)"
    fi
    
    log_success "APK analysis complete"
else
    log_warning "Skipping APK analysis (aapt not available)"
fi
echo ""

# Step 8: Run tests on release build
log_info "Running E2E tests on release build..."

if adb devices | grep -q "device$"; then
    log_info "Device/emulator detected"
    
    # Install release APK
    if [ -f "$APK_PATH" ]; then
        log_info "Installing release APK..."
        if adb install -r "$APK_PATH"; then
            log_success "APK installed"
            
            # Run tests
            log_info "Running tests..."
            if ./gradlew connectedReleaseAndroidTest; then
                log_success "All E2E tests passed on release build"
            else
                log_error "E2E tests failed on release build"
                log_error "This usually means ProGuard broke something!"
            fi
        else
            log_error "Failed to install APK"
        fi
    fi
else
    log_warning "No device/emulator connected. Skipping E2E tests."
    log_warning "Connect device and run: ./gradlew connectedReleaseAndroidTest"
fi
echo ""

# Summary
echo "======================================"
echo "Validation Summary"
echo "======================================"
echo ""
echo -e "Checks Passed: ${GREEN}$CHECKS_PASSED${NC}/$CHECKS_TOTAL"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo -e "Errors: ${RED}$ERRORS${NC}"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}✗ VALIDATION FAILED${NC}"
    echo "Fix errors before deploying to Play Store."
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠ VALIDATION PASSED WITH WARNINGS${NC}"
    echo "Review warnings before deploying."
    exit 0
else
    echo -e "${GREEN}✓ VALIDATION PASSED${NC}"
    echo "Release build is ready for deployment!"
    exit 0
fi
