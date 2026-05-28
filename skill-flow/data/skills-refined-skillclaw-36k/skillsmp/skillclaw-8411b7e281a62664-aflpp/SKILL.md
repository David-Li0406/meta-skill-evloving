---
name: aflpp
description: Use this skill when you need to perform multi-core fuzzing on C/C++ projects with advanced features and better performance than traditional fuzzers.
---

# AFL++

AFL++ is a fork of the original AFL fuzzer that offers improved fuzzing performance and advanced features while maintaining stability. A major benefit over libFuzzer is its stable support for running fuzzing campaigns on multiple cores, making it ideal for large-scale fuzzing efforts.

## When to Use

| Fuzzer | Best For | Complexity |
|--------|----------|------------|
| AFL++ | Multi-core fuzzing, diverse mutations, mature projects | Medium |
| libFuzzer | Quick setup, single-threaded, simple harnesses | Low |
| LibAFL | Custom fuzzers, research, advanced use cases | High |

**Choose AFL++ when:**
- You need multi-core fuzzing to maximize throughput.
- Your project can be compiled with Clang or GCC.
- You want diverse mutation strategies and mature tooling.
- libFuzzer has plateaued and you need more coverage.
- You're fuzzing production codebases that benefit from parallel execution.

## Quick Start

```c++
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Call your code with fuzzer-provided data
    check_buf((char*)data, size);
    return 0;
}
```

Compile and run:
```bash
# Setup AFL++ wrapper script first (see Installation)
./afl++ docker afl-clang-fast++ -DNO_MAIN=1 -O2 -fsanitize=fuzzer harness.cc main.cc -o fuzz
mkdir seeds && echo "aaaa" > seeds/minimal_seed
./afl++ docker afl-fuzz -i seeds -o out -- ./fuzz
```

## Installation

AFL++ has many dependencies including LLVM, Python, and Rust. We recommend using a current Debian or Ubuntu distribution for fuzzing with AFL++.

| Method | When to Use | Supported Compilers |
|--------|-------------|---------------------|
| Ubuntu/Debian repos | Recent Ubuntu, basic features only | Ubuntu 23.10: Clang 14 & GCC 13<br>Debian 12: Clang 14 & GCC 12 |
| Docker (from Docker Hub) | Specific AFL++ version, Apple Silicon support | As of 4.35c: Clang 19 & GCC 11 |
| Docker (from source) | Test unreleased features, apply patches | Configurable in Dockerfile |
| From source | Avoid Docker, need specific patches | Adjustable via `LLVM_CONFIG` env var |

### Ubuntu/Debian

Prior to installing AFL++, check the clang version dependency of the package with `apt-cache show afl++`, and install the matching `lld` version (e.g., `lld-17`).

```bash
apt install afl++ lld-17
```