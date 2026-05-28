---
name: dev-debug-cpp
description: C++ debugging for segfaults, memory corruption, threading issues, and linker/ABI problems. Use when encountering crashes (exit code 139/SIGSEGV), memory leaks, data races, undefined behavior, or when debugging native Node.js addons, FFmpeg integrations, or any C++ code that crashes mysteriously.
allowed-tools: Read, Bash, Glob, Grep, LSP
---

# C++ Debugging Skill

## Critical: Triage Before Editing

When encountering segfaults or crashes, **do not edit source code** until completing this triage.

### Step 1: Analyze Build Output

Search build logs for these patterns:

```
# ABI/SDK mismatch (COMMON in native addons)
"built for macOS-X" ... "linking with" ... "built for newer version Y"
"undefined symbol"
"multiple definition"
"incompatible library version"

# Mixed C++ standard libraries (fatal)
"libc++" vs "libstdc++"
```

**If any mismatch found → STOP. Fix build configuration, not source code.**

### Step 2: Classify the Crash Location

| Crash Pattern | Likely Cause | Action |
|--------------|--------------|--------|
| Crash in trivial constructor (empty class, single int) | ABI mismatch or heap already corrupted | Check build config |
| Crash in std::vector/string/function internals | ABI mismatch (different memory layouts) | Check build config |
| Crash location moves when changing unrelated code | Memory corruption earlier in execution | Run ASan from start |
| Crash is stable and reproducible at same line | Actual code bug | Proceed to instrumentation |

### Step 3: Environment Diagnostics

```bash
# macOS: Check linked library versions
otool -L ./build/Release/*.node 2>/dev/null || otool -L ./program

# Linux: Check linked libraries
ldd ./build/Release/*.node 2>/dev/null || ldd ./program

# Check compiler used for each library
nm -gU ./program | grep -E "__(ZN|cxa)" | head -20

# Verify deployment target matches
grep -r "macosx-version-min\|mmacosx-version-min\|MACOSX_DEPLOYMENT_TARGET" binding.gyp CMakeLists.txt 2>/dev/null
```

## Instrumentation (Only After Triage)

### Address Sanitizer (Memory Bugs)

Detects: use-after-free, buffer overflow, stack overflow, memory leaks

```bash
# Compile
clang++ -fsanitize=address -fno-omit-frame-pointer -g -O1 -o program_asan main.cpp

# Run (ASan output is precise—trust it)
ASAN_OPTIONS=detect_leaks=1:halt_on_error=0 ./program_asan
```

ASan output anatomy:
```
==PID==ERROR: AddressSanitizer: heap-use-after-free on address 0x...
READ of size 4 at 0x... thread T0
    #0 0x... in function_name file.cpp:42      ← THIS IS THE BUG
...
freed by thread T0 here:
    #0 0x... in operator delete
    #1 0x... in some_function file.cpp:38      ← FREED HERE
...
previously allocated by thread T0 here:
    #0 0x... in operator new
    #1 0x... in another_function file.cpp:20   ← ALLOCATED HERE
```

### Thread Sanitizer (Data Races)

Detects: data races, deadlocks, lock order inversions

```bash
clang++ -fsanitize=thread -g -O1 -o program_tsan main.cpp
./program_tsan
```

TSan output shows exact conflicting accesses:
```
WARNING: ThreadSanitizer: data race
  Write of size 4 at 0x... by thread T1:
    #0 function_a file.cpp:50
  Previous read of size 4 at 0x... by thread T2:
    #0 function_b file.cpp:75
```

### Undefined Behavior Sanitizer

Detects: null deref, signed overflow, invalid shifts, misaligned access

```bash
clang++ -fsanitize=undefined -g -o program_ubsan main.cpp
./program_ubsan
```

### Valgrind (Deeper Memory Analysis)

```bash
valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./program
```

### GDB Backtrace

```bash
# On crash
gdb -batch -ex "run" -ex "bt full" -ex "info registers" ./program

# With core dump
ulimit -c unlimited
./program  # crashes, generates core
gdb -batch -ex "bt full" ./program core
```

## Node.js Native Addon Specifics

### Common Issues

1. **SDK version mismatch**: `binding.gyp` targets old macOS but links modern FFmpeg
2. **N-API version mismatch**: Addon built for different Node.js version
3. **libuv threading**: Calling JS from wrong thread

### binding.gyp Fixes

```python
# Match your system SDK
"xcode_settings": {
    "MACOSX_DEPLOYMENT_TARGET": "14.0",  # Match: sw_vers -productVersion
}

# Or for CMake
set(CMAKE_OSX_DEPLOYMENT_TARGET "14.0")
```

### Rebuild Everything

```bash
# Nuclear option: rebuild all native deps
rm -rf node_modules build
npm cache clean --force
npm install --build-from-source
```

## Loop Detection

**You are stuck if:**
- Same file edited 3+ times with identical crash
- Crash persists after removing all logic from a class
- Making code "simpler" doesn't help

**When stuck:**
1. STOP editing source code
2. Create minimal standalone test outside your build system:

```cpp
// test_standalone.cpp
#include <vector>
#include <iostream>
int main() {
    std::vector<int> v{1,2,3};
    std::cout << v.size() << std::endl;
    return 0;
}
```

```bash
# Compile with EXACT same flags as your project
clang++ -mmacosx-version-min=11.0 -std=c++17 test_standalone.cpp -o test
./test
```

If standalone crashes → toolchain is broken, not your code.

## Common C++ Bug Patterns (Only Check After Ruling Out Build Issues)

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Use-after-free | ASan: "heap-use-after-free" | Check object lifetimes, use smart pointers |
| Iterator invalidation | Crash in loop modifying container | Copy container or use indices |
| Dangling reference in lambda | Crash when callback fires | Capture by value or ensure lifetime |
| Double-free | ASan: "double-free" | Use unique_ptr, check delete logic |
| Missing virtual destructor | Leak or crash on polymorphic delete | Add `virtual ~Base() = default;` |
| Data race | TSan warning | Add mutex or use atomics |
