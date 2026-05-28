---
name: java-rts-build-converter
description: Convert Java Maven project test.sh scripts for RTS (Regression Test Selection) with OpenClover. Also handles Maven multi-module test exclusions via pom.xml. Use when fixing test.sh scripts for RTS builds, handling OpenClover instrumentation failures, skipping failing tests, or configuring test exclusions.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Java RTS Build Converter Skill

This skill converts Java Maven project test.sh scripts to properly support RTS (Regression Test Selection) with OpenClover. It also covers Maven pom.xml modifications for skipping failing tests in multi-module projects.

## CRITICAL CONSTRAINTS

### 1. DO NOT Modify oss-fuzz Infrastructure Code

**NEVER modify these files:**
- `oss-fuzz/infra/helper.py`
- `oss-fuzz/infra/base-images/*`
- Any other oss-fuzz infrastructure code

**ONLY modify:**
- `oss-fuzz/projects/{project}/test.sh`
- `oss-fuzz/projects/{project}/build.sh` (if absolutely necessary)
- Source code pom.xml files (for surefire excludes)

### 2. Focus on test.sh Modifications

The primary focus is fixing `test.sh` scripts for RTS compatibility, not build.sh.

---

## OpenClover RTS Test Exclusion

### Two-Level Exclusion Strategy

When tests fail with OpenClover, there are TWO levels of exclusion:

| Level | Variable/Option | Purpose | When to Use |
|-------|-----------------|---------|-------------|
| 1 | `-Dmaven.clover.excludesList` | Exclude from **instrumentation** | Test fails due to Clover bytecode instrumentation |
| 2 | `EXCLUDE_TESTS` / `-Dsurefire.excludes` | Exclude from **execution** | Test fails regardless of instrumentation |

### Level 1: OpenClover Instrumentation Exclusion

When a test fails **only with OpenClover instrumentation** (passes without Clover), add to `excludesList`:

```bash
# Tests that fail due to Clover instrumentation
CLOVER_EXCLUDES="**/SimplePerfTest.java,**/FastFileAppenderLocationTest.java,**/AsyncAppenderTest.java"

$MVN clover:setup clover:optimize test clover:snapshot $MVN_ARGS \
    -Dmaven.clover.excludesList="$CLOVER_EXCLUDES"
```

**Common symptoms of instrumentation-related failures:**
- `java.lang.VerifyError` - Bytecode verification failed
- `java.lang.ClassFormatError` - Invalid class format
- Timing-sensitive tests failing (Clover adds overhead)
- Location/line number related tests (Clover modifies bytecode)
- Performance tests failing threshold checks

### Level 2: General Test Exclusion

If the same test **still fails after adding to `excludesList`**, the test has issues unrelated to instrumentation. Add to `EXCLUDE_TESTS`:

```bash
# Tests that fail regardless of instrumentation
EXCLUDE_TESTS="**/BrokenTest.java,**/FlakyTest.java"

# Use with surefire
if [ -n "$EXCLUDE_TESTS" ]; then
    MVN_ARGS="$MVN_ARGS -Dsurefire.excludes=$EXCLUDE_TESTS"
fi
```

### Decision Flow

```
Test fails with OpenClover RTS
            │
            ▼
   Add to excludesList
   -Dmaven.clover.excludesList="**/FailingTest.java"
            │
            ▼
   Re-run test ────────────► Still fails?
            │                     │
            │ No                  │ Yes
            ▼                     ▼
         Done             Add to EXCLUDE_TESTS
                          -Dsurefire.excludes="**/FailingTest.java"
```

---

## Standard test.sh Template for OpenClover RTS

```bash
#!/bin/bash
set -ex

: "${SRC:=/src}"
: "${WORK:=/work}"

cd $SRC/{project}

MVN="mvn -DskipTests -Denforcer.skip -Drat.skip -Dcheckstyle.skip -Dlicense.skip"
MVN_ARGS="-Dmaven.test.failure.ignore=true"

# Level 1: Tests that fail due to Clover instrumentation
# (bytecode modification causes test failures)
CLOVER_EXCLUDES=""
CLOVER_EXCLUDES="$CLOVER_EXCLUDES,**/SimplePerfTest.java"
CLOVER_EXCLUDES="$CLOVER_EXCLUDES,**/FastFileAppenderLocationTest.java"
CLOVER_EXCLUDES="$CLOVER_EXCLUDES,**/AsyncAppenderTest.java"
# Remove leading comma
CLOVER_EXCLUDES="${CLOVER_EXCLUDES#,}"

# Level 2: Tests that fail regardless of instrumentation
# (general test issues - flaky, env-dependent, etc.)
EXCLUDE_TESTS=""
# EXCLUDE_TESTS="$EXCLUDE_TESTS,**/BrokenTest.java"
# Remove leading comma
EXCLUDE_TESTS="${EXCLUDE_TESTS#,}"

# Add surefire excludes if any
if [ -n "$EXCLUDE_TESTS" ]; then
    MVN_ARGS="$MVN_ARGS -Dsurefire.excludes=$EXCLUDE_TESTS"
fi

# Build Clover exclude argument
CLOVER_EXCLUDE_ARG=""
if [ -n "$CLOVER_EXCLUDES" ]; then
    CLOVER_EXCLUDE_ARG="-Dmaven.clover.excludesList=$CLOVER_EXCLUDES"
fi

# Run RTS test
if [ -n "${RTS_ON}" ]; then
    $MVN clover:setup clover:optimize test clover:snapshot $MVN_ARGS $CLOVER_EXCLUDE_ARG
else
    $MVN test $MVN_ARGS
fi

echo "Tests completed"
```

---

## Common OpenClover Instrumentation Failures

### 1. Location/LineNumber Tests

Tests that verify stack trace line numbers fail because Clover adds instrumentation code.

```bash
# These test types commonly fail with Clover
CLOVER_EXCLUDES="**/FastFileAppenderLocationTest.java"
CLOVER_EXCLUDES="$CLOVER_EXCLUDES,**/FastRollingFileAppenderLocationTest.java"
CLOVER_EXCLUDES="$CLOVER_EXCLUDES,**/AsyncLoggerLocationTest.java"
```

### 2. Performance/Timing Tests

Tests with strict timing requirements fail due to Clover overhead.

```bash
CLOVER_EXCLUDES="**/SimplePerfTest.java"
CLOVER_EXCLUDES="$CLOVER_EXCLUDES,**/PerformanceBenchmarkTest.java"
```

### 3. Async/Threading Tests

Tests sensitive to thread timing or async behavior.

```bash
CLOVER_EXCLUDES="**/AsyncAppenderTest.java"
CLOVER_EXCLUDES="$CLOVER_EXCLUDES,**/AsyncLoggerConfigTest.java"
```

### 4. Bytecode Verification Tests

Tests that inspect or verify bytecode structure.

```bash
CLOVER_EXCLUDES="**/RFC5424LayoutTest.java"
```

---

## Common test.sh Issues and Fixes

### Issue 1: Missing Clover Excludes

**Symptom:** Tests pass without RTS, fail with OpenClover

**Fix:** Add failing tests to `CLOVER_EXCLUDES`:

```bash
# Before
$MVN clover:setup clover:optimize test clover:snapshot $MVN_ARGS

# After
CLOVER_EXCLUDES="**/FailingTest.java"
$MVN clover:setup clover:optimize test clover:snapshot $MVN_ARGS \
    -Dmaven.clover.excludesList="$CLOVER_EXCLUDES"
```

### Issue 2: Test Still Fails After excludesList

**Symptom:** Added to `excludesList` but test still fails

**Cause:** The test failure is NOT caused by instrumentation

**Fix:** Add to `EXCLUDE_TESTS` instead:

```bash
# Level 1 didn't help, escalate to Level 2
EXCLUDE_TESTS="**/StillFailingTest.java"
MVN_ARGS="$MVN_ARGS -Dsurefire.excludes=$EXCLUDE_TESTS"
```

### Issue 3: RAT License Check Failure

**Symptom:** `RatCheckException: Too many files with unapproved license`

**Fix:** Add `-Drat.skip=true` to MVN base:

```bash
MVN="mvn -DskipTests -Denforcer.skip -Drat.skip=true"
```

### Issue 4: Checkstyle/License Plugin Failures

**Symptom:** Build fails on style checks during test

**Fix:** Skip all verification plugins:

```bash
MVN="mvn -DskipTests -Denforcer.skip -Drat.skip -Dcheckstyle.skip -Dlicense.skip -Dspotbugs.skip"
```

### Issue 5: Test Timeout

**Symptom:** Tests hang or timeout

**Fix:** Add timeout configuration:

```bash
MVN_ARGS="$MVN_ARGS -Dsurefire.timeout=300"
```

### Issue 6: Memory Issues

**Symptom:** `OutOfMemoryError` during tests

**Fix:** Increase memory:

```bash
MVN_ARGS="$MVN_ARGS -DargLine=-Xmx4g"
```

---

## Identifying Which Exclusion Level to Use

### Check if failure is instrumentation-related:

1. **Run without Clover:**
   ```bash
   mvn test -Dtest=FailingTest
   ```

2. **Run with Clover:**
   ```bash
   mvn clover:setup test -Dtest=FailingTest
   ```

3. **Compare results:**
   - Passes without Clover, fails with → Use `excludesList` (Level 1)
   - Fails both → Use `EXCLUDE_TESTS` (Level 2)

### Common Level 1 (excludesList) candidates:

- Tests with "Location" in name
- Tests with "Perf" or "Performance" in name
- Tests with "Async" in name
- Tests checking line numbers or stack traces
- Tests with strict timing assertions

### Common Level 2 (EXCLUDE_TESTS) candidates:

- Tests requiring external resources (network, files)
- Tests with environment-specific behavior
- Flaky tests
- Tests requiring specific JDK features

---

## Error Pattern Reference

| Error Message | Likely Cause | Fix |
|---------------|--------------|-----|
| `VerifyError: Bad type on operand stack` | Clover instrumentation | Add to `excludesList` |
| `ClassFormatError` | Clover bytecode issue | Add to `excludesList` |
| `expected line 42 but was 128` | Clover changed line numbers | Add to `excludesList` |
| `Test timed out after X ms` | Clover overhead | Add to `excludesList` or increase timeout |
| `AssertionError: expected <10ms` | Performance test + Clover overhead | Add to `excludesList` |
| `NoClassDefFoundError` | Missing dependency | Check classpath, not Clover issue |
| `FileNotFoundException` | Missing resource | Add to `EXCLUDE_TESTS` |
| `ConnectException` | Network test | Add to `EXCLUDE_TESTS` |

---

## Maven pom.xml Test Exclusions (Alternative to test.sh)

When command-line exclusions are not sufficient or when tests need to be permanently excluded, modify pom.xml files directly.

### CRITICAL: Maven Multi-Module Inheritance Rules

**IMPORTANT: `<plugins>` section settings in parent pom.xml are NOT inherited by child modules!**

```
project-parent/pom.xml
├── <pluginManagement>  → Settings inherited when child DECLARES the plugin
│   └── <plugins>
└── <plugins>           → NOT inherited (only applies to parent itself)
```

### CRITICAL: Add Under `<build>`, NOT Under `<profiles>`!

**WRONG - Adding under `<profiles>`:**
```xml
<profiles>
  <profile>
    <id>some-profile</id>
    <build>
      <plugins>
        <plugin>
          <artifactId>maven-surefire-plugin</artifactId>
          <!-- This only applies when profile is active! -->
        </plugin>
      </plugins>
    </build>
  </profile>
</profiles>
```

**CORRECT - Adding directly under `<build>`:**
```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
      <configuration>
        <excludes>
          <exclude>**/HtmlParserTest.java</exclude>
        </excludes>
      </configuration>
    </plugin>
  </plugins>
</build>
```

### Step 1: Find the Test Class Location

```bash
# Find where the failing test class exists
find . -name "HtmlParserTest.java" -type f
```

Example output:
```
./tika-parsers/tika-parsers-standard/tika-parsers-standard-package/src/test/java/.../HtmlParserTest.java
./tika-parsers/tika-parsers-standard/tika-parsers-standard-modules/tika-parser-html-module/src/test/java/.../HtmlParserTest.java
```

**IMPORTANT:** Test may exist in MULTIPLE modules. Must fix ALL relevant pom.xml files.

### Step 2: Check Current Surefire Configuration

```bash
# Check if surefire is configured in each module
grep -l "surefire" $(find . -name "pom.xml" -type f)

# Check parent pom structure
grep -n "pluginManagement\|</plugins>\|<plugins>" parent/pom.xml
```

### Step 3: Identify Which pom.xml to Modify

| Scenario | pom.xml to modify |
|----------|------------------|
| Test in specific module | That module's pom.xml |
| Test in multiple modules | Each module's pom.xml |
| All tests in project | Use `<pluginManagement>` in root + declare in each module |

### pom.xml Fix Templates

**Template 1: Skip Single Test in Module**

```xml
<!-- Add to module's pom.xml where test exists -->
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
      <configuration>
        <excludes>
          <exclude>**/TestClassName.java</exclude>
        </excludes>
      </configuration>
    </plugin>
  </plugins>
</build>
```

**Template 2: Skip Multiple Tests**

```xml
<configuration>
  <excludes>
    <exclude>**/Test1.java</exclude>
    <exclude>**/Test2.java</exclude>
    <exclude>**/Test3.java</exclude>
  </excludes>
</configuration>
```

**Template 3: Merge with Existing Configuration**

If the module already has surefire configuration:

```xml
<!-- BEFORE -->
<plugin>
  <artifactId>maven-surefire-plugin</artifactId>
  <configuration>
    <argLine>-Xmx4g</argLine>
  </configuration>
</plugin>

<!-- AFTER - Add excludes to existing config -->
<plugin>
  <artifactId>maven-surefire-plugin</artifactId>
  <configuration>
    <argLine>-Xmx4g</argLine>
    <excludes>
      <exclude>**/HtmlParserTest.java</exclude>
    </excludes>
  </configuration>
</plugin>
```

**Template 4: Module has no `<build>` section**

```xml
<!-- Add this before </project> -->
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
      <configuration>
        <excludes>
          <exclude>**/FailingTest.java</exclude>
        </excludes>
      </configuration>
    </plugin>
  </plugins>
</build>
```

### Common pom.xml Mistakes

| Error | Cause | Fix |
|-------|-------|-----|
| Test still runs after adding exclude | Added under `<profiles>` instead of root `<build>` | Move to root `<build>` section |
| Test still runs after adding exclude | Added to parent `<plugins>` instead of child | Add to child module's pom.xml |
| Duplicate plugin declaration error | Plugin declared in both parent and child | Use `<pluginManagement>` in parent |
| Exclude pattern not matching | Wrong pattern syntax | Use `**/ClassName.java` format |

---

## Testing with test-inc-build Subagent

After fixing test.sh or pom.xml, verify using the subagent:

```
Task tool:
  subagent_type: "test-inc-build"
  description: "Test Java RTS build"
  prompt: "Run incremental build test for aixcc/jvm/{project-name} with oss-fuzz path ../oss-fuzz"
```

---

## Checklist

### test.sh Modifications
- [ ] test.sh uses correct MVN base with skip flags (`-Drat.skip`, `-Dcheckstyle.skip`, etc.)
- [ ] `CLOVER_EXCLUDES` defined for instrumentation-sensitive tests
- [ ] `EXCLUDE_TESTS` defined for generally failing tests
- [ ] Tests failing with Clover added to `excludesList` first
- [ ] Tests still failing after `excludesList` moved to `EXCLUDE_TESTS`
- [ ] RTS command includes `$CLOVER_EXCLUDE_ARG`
- [ ] Non-RTS fallback path works
- [ ] Timeout and memory settings adequate

### pom.xml Modifications (if needed)
- [ ] Found ALL locations where the test class exists
- [ ] Identified correct pom.xml for each location
- [ ] Added under root `<build>`, NOT under `<profiles>`
- [ ] Checked if module has existing surefire configuration (merge, don't replace)
- [ ] Verified fix is in `<plugins>` section of child module, NOT parent `<plugins>`
- [ ] Test no longer runs after fix
