# Release Build Validation Report

**Build Date:** {BUILD_DATE}  
**Version:** {VERSION_NAME} ({VERSION_CODE})  
**Package:** {PACKAGE_NAME}  
**Validated By:** {VALIDATOR}

---

## Executive Summary

**Overall Status:** {OVERALL_STATUS}

{SUMMARY_PARAGRAPH}

---

## Build Status

### APK Build
- **Status:** {APK_STATUS}
- **Size:** {APK_SIZE_MB} MB
- **Location:** `app/build/outputs/apk/release/app-release.apk`
- **Build Time:** {APK_BUILD_TIME} seconds
- **MD5 Hash:** {APK_MD5}

### AAB Build (Android App Bundle)
- **Status:** {AAB_STATUS}
- **Size:** {AAB_SIZE_MB} MB
- **Location:** `app/build/outputs/bundle/release/app-release.aab`
- **Build Time:** {AAB_BUILD_TIME} seconds
- **MD5 Hash:** {AAB_MD5}

---

## Configuration

### SDK Versions
- **Minimum SDK:** {MIN_SDK} (Android {MIN_SDK_VERSION})
- **Target SDK:** {TARGET_SDK} (Android {TARGET_SDK_VERSION})
- **Compile SDK:** {COMPILE_SDK}

{TARGET_SDK_WARNING}

### ProGuard/R8
- **Minification Enabled:** {MINIFY_ENABLED}
- **Resource Shrinking:** {SHRINK_RESOURCES}
- **Mapping File:** {MAPPING_STATUS}
  - Location: `app/build/outputs/mapping/release/mapping.txt`
  - Size: {MAPPING_SIZE_KB} KB

### Signing Configuration
- **Signed:** {SIGNED_STATUS}
- **Algorithm:** {SIGNATURE_ALGORITHM}
- **Certificate Info:**
  - Subject: {CERT_SUBJECT}
  - Issuer: {CERT_ISSUER}
  - Valid From: {CERT_VALID_FROM}
  - Valid Until: {CERT_VALID_UNTIL}
  - Serial: {CERT_SERIAL}

{SIGNING_WARNINGS}

---

## Test Results

### E2E Tests on Release Build

**Execution:** {TEST_EXECUTION_STATUS}

| Metric | Count |
|--------|-------|
| Total Tests | {TOTAL_TESTS} |
| Passed | {PASSED_TESTS} |
| Failed | {FAILED_TESTS} |
| Skipped | {SKIPPED_TESTS} |
| **Success Rate** | **{SUCCESS_RATE}%** |

**Test Execution Time:** {TEST_EXECUTION_TIME} seconds

{TEST_DETAILS}

{FAILED_TEST_DETAILS}

---

## APK Analysis

### Size Breakdown

| Component | Size (MB) | Percentage |
|-----------|-----------|------------|
| DEX Files | {DEX_SIZE_MB} | {DEX_PERCENT}% |
| Resources | {RES_SIZE_MB} | {RES_PERCENT}% |
| Native Libs | {LIB_SIZE_MB} | {LIB_PERCENT}% |
| Assets | {ASSET_SIZE_MB} | {ASSET_PERCENT}% |
| Other | {OTHER_SIZE_MB} | {OTHER_PERCENT}% |
| **Total** | **{TOTAL_SIZE_MB}** | **100%** |

### Size Assessment

{SIZE_ASSESSMENT}

### Method Count
- **Total Methods:** {METHOD_COUNT}
- **DEX Files:** {DEX_FILE_COUNT}

{METHOD_COUNT_WARNING}

### Permissions

**Total Permissions:** {PERMISSION_COUNT}

{PERMISSIONS_LIST}

{PERMISSION_WARNINGS}

### Native Libraries

{NATIVE_LIBS_LIST}

### Large Files (Top 10)

| File | Size | Percentage |
|------|------|------------|
{LARGE_FILES_TABLE}

---

## Issues Found

### Critical Issues

{CRITICAL_ISSUES}

### Warnings

{WARNINGS}

### Recommendations

{RECOMMENDATIONS}

---

## Validation Checklist

| Check | Status | Notes |
|-------|--------|-------|
| APK builds successfully | {CHECK_APK_BUILD} | {CHECK_APK_BUILD_NOTES} |
| AAB builds successfully | {CHECK_AAB_BUILD} | {CHECK_AAB_BUILD_NOTES} |
| ProGuard enabled | {CHECK_PROGUARD} | {CHECK_PROGUARD_NOTES} |
| Mapping file generated | {CHECK_MAPPING} | {CHECK_MAPPING_NOTES} |
| Release signed correctly | {CHECK_SIGNING} | {CHECK_SIGNING_NOTES} |
| E2E tests pass on release | {CHECK_TESTS} | {CHECK_TESTS_NOTES} |
| APK size reasonable | {CHECK_SIZE} | {CHECK_SIZE_NOTES} |
| Target SDK meets requirements | {CHECK_TARGET_SDK} | {CHECK_TARGET_SDK_NOTES} |
| No debug symbols in release | {CHECK_DEBUG_SYMBOLS} | {CHECK_DEBUG_SYMBOLS_NOTES} |
| Permissions appropriate | {CHECK_PERMISSIONS} | {CHECK_PERMISSIONS_NOTES} |

---

## Next Steps

{NEXT_STEPS}

---

## Appendix

### Build Configuration

```kotlin
{BUILD_CONFIG}
```

### ProGuard Configuration

```
{PROGUARD_CONFIG}
```

### Build Logs

{BUILD_LOGS_SUMMARY}

---

**Report Generated:** {REPORT_TIMESTAMP}  
**Validation Tool:** android-release-validation v1.0.0  
**Report Format Version:** 1.0
