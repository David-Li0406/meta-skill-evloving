---
title: FFI and C Interoperability
description: Complete guide to foreign function interface patterns including C strings, libc, binary data, type safety, vendor libraries, dynamic loading, and GPU integration
impact: CRITICAL
category: ffi
tags: ffi, c-interop, strings, binary, gpu, blas, vendor-libraries, dynamic-loading
error_patterns:
  - "undefined symbol"
  - "linker error"
  - "CString"
  - "DLHandle"
  - "library not found"
  - "symbol not found"
  - "Accelerate"
scenarios:
  - "Call C library from Mojo"
  - "Use Apple BLAS for matrix multiply"
  - "Load dynamic library at runtime"
  - "Handle C strings safely"
  - "Fix linker error"
consolidates:
  - ffi-cstring-safety.md
  - ffi-libc-functions.md
  - ffi-binary-data-patterns.md
  - ffi-int-size-mismatch.md
  - ffi-prefer-vendor-libraries.md
  - ffi-apple-amx-blas.md
  - ffi-missing-math-functions.md
  - ffi-dynamic-library-loading.md
  - ffi-gpu-libraries.md
  - ffi-gpu-program-caching.md
  - ffi-string-handling.md
  - ffi-python-gil.md
  - ffi-apple-bf16-to-f16.md
  - ffi-mps-bf16-limitations.md
---

# FFI and C Interoperability

**Category:** ffi | **Impact:** CRITICAL

Comprehensive patterns for interfacing Mojo with C libraries, system APIs, and GPU frameworks. Covers string handling, binary data, type safety, vendor library integration, and platform-specific considerations. Proper FFI usage enables 10-100x performance gains through vendor-optimized libraries like Apple BLAS.

---

## Core Concepts

### Type Aliases for FFI

Define standard type aliases for consistent FFI code.

**Pattern:**

```mojo
from sys.ffi import external_call, OwnedDLHandle, RTLD
from memory import UnsafePointer, memcpy
from builtin.type_aliases import MutAnyOrigin

# Standard pointer types
comptime UInt8Ptr = UnsafePointer[mut=True, type=UInt8, origin=MutAnyOrigin]
comptime Float32Ptr = UnsafePointer[mut=True, type=Float32, origin=MutAnyOrigin]
comptime Float64Ptr = UnsafePointer[mut=True, type=Float64, origin=MutAnyOrigin]
comptime Int32Ptr = UnsafePointer[mut=True, type=Int32, origin=MutAnyOrigin]
comptime NonePtr = UnsafePointer[mut=True, type=NoneType, origin=MutAnyOrigin]

# Opaque pointer for FILE*
comptime FILE = UnsafePointer[mut=True, type=UInt8, origin=MutAnyOrigin]
```

### Integer Type Sizes

Mojo's `Int` is 64-bit on most platforms, but C's `int` is 32-bit. This mismatch causes silent data corruption.

**Pattern:**

```mojo
# Type size reference
# | Mojo Type | Size on Apple Silicon | C Equivalent |
# |-----------|----------------------|--------------|
# | Int       | 64-bit               | long/int64_t |
# | Int32     | 32-bit               | int/int32_t  |
# | Int64     | 64-bit               | int64_t      |
# | Int16     | 16-bit               | short        |
# | Int8      | 8-bit                | char         |
```

---

## CString Safety Patterns

### String to C String (for calling C functions)

```mojo
fn call_c_function(s: String):
    # Get null-terminated pointer (valid while s is alive)
    var c_str = s.unsafe_cstr_ptr()

    # Call C function
    external_call["puts", NoneType](c_str)

    # WARNING: c_str is only valid while s exists
    # Do NOT store or return c_str
```

### Correct Lifetime Management

```mojo
fn safe_c_call(s: String):
    # Explicitly manage lifetime
    var c_str: UnsafePointer[C_char] = s.unsafe_cstr_ptr()

    # Call is safe - s still in scope
    var result = external_call["strlen", Int](c_str)

    # s goes out of scope after this function
    # c_str becomes dangling - do not use after return
```

### C String to Mojo String (taking ownership)

```mojo
fn receive_c_string() -> String:
    # C function returns allocated string
    var c_str = external_call["get_message", UnsafePointer[C_char]]()

    # Option 1: Copy to String (C still owns memory)
    var s = String(StringRef(c_str))

    # Must free C memory if we own it
    external_call["free", NoneType](c_str)

    return s
```

### StringSlice for Borrowed C Data

```mojo
fn process_c_buffer(ptr: UnsafePointer[UInt8], length: Int):
    # Create view without copying (ptr must remain valid)
    var slice = StringSlice[ImmutableAnyOrigin](
        ptr=ptr.bitcast[Byte](),
        length=length,
    )

    # Use slice (zero-copy)
    print("Length:", len(slice))

    # slice becomes invalid when ptr is freed
```

### Buffer Allocation for C Output

```mojo
from memory.unsafe_pointer import alloc

fn get_cwd() raises -> String:
    # Allocate buffer for C function to write into
    comptime BUFFER_SIZE = 4096
    var buffer = alloc[C_char](BUFFER_SIZE)

    # C function writes into buffer
    var result = external_call["getcwd", UnsafePointer[C_char]](
        buffer, BUFFER_SIZE
    )

    if not result:
        buffer.free()
        raise Error("getcwd failed")

    # Convert to String (copies data)
    var path = String(StringRef(buffer))

    # Free our buffer
    buffer.free()

    return path
```

### StaticString for Compile-Time C Strings

```mojo
fn use_static_string():
    # Compile-time string - guaranteed null-terminated, static lifetime
    comptime MSG: StaticString = "Hello, World!"

    # Safe to pass to C - lives forever
    var c_str = MSG.unsafe_cstr_ptr()
    external_call["puts", NoneType](c_str)
```

### Common CString Mistakes

```mojo
# BAD: Using pointer after String is freed
fn bad_lifetime() -> UnsafePointer[C_char]:
    var s = String("hello")
    return s.unsafe_cstr_ptr()  # s is freed, pointer dangles!

# BAD: Double-free
fn bad_ownership():
    var c_str = external_call["strdup", UnsafePointer[C_char]]("hello")
    var s1 = String(c_str, transfer_ownership=True)  # s1 will free
    var s2 = String(c_str, transfer_ownership=True)  # Double free!

# BAD: Assuming null termination
fn bad_assumption(ptr: UnsafePointer[UInt8], len: Int):
    # ptr might not be null-terminated!
    external_call["puts", NoneType](ptr.bitcast[C_char]())
```

---

## libc Function Usage

### Basic File I/O with libc

```mojo
from sys.ffi import external_call
from memory import UnsafePointer
from builtin.type_aliases import MutAnyOrigin

# Define opaque pointer type for FILE*
comptime FILE = UnsafePointer[mut=True, type=UInt8, origin=MutAnyOrigin]

fn fopen(path: String, mode: String) -> FILE:
    """Open file using libc."""
    return external_call["fopen", FILE](path.unsafe_ptr(), mode.unsafe_ptr())

fn fclose(f: FILE) -> Int32:
    """Close file using libc."""
    return external_call["fclose", Int32](f)

fn fread(ptr: UnsafePointer[UInt8], size: Int, count: Int, f: FILE) -> Int:
    """Read from file using libc."""
    return Int(external_call["fread", Int64](ptr, size, count, f))

fn fwrite(ptr: UnsafePointer[UInt8], size: Int, count: Int, f: FILE) -> Int:
    """Write to file using libc."""
    return Int(external_call["fwrite", Int64](ptr, size, count, f))

fn fseek(f: FILE, offset: Int64, whence: Int32) -> Int32:
    """Seek in file using libc."""
    return external_call["fseek", Int32](f, offset, whence)

fn ftell(f: FILE) -> Int64:
    """Get file position using libc."""
    return external_call["ftell", Int64](f)
```

### Reading a File

```mojo
fn read_file_contents(path: String) raises -> List[UInt8]:
    """Read entire file into byte buffer."""
    var f = fopen(path, "rb")
    if not f:
        raise "Failed to open file: " + path

    # Get file size
    _ = fseek(f, 0, 2)  # SEEK_END
    var size = Int(ftell(f))
    _ = fseek(f, 0, 0)  # SEEK_SET

    # Read contents
    var buffer = List[UInt8](capacity=size)
    buffer.resize(size, 0)
    var bytes_read = fread(buffer.unsafe_ptr(), 1, size, f)
    _ = fclose(f)

    if bytes_read != size:
        raise "Failed to read complete file"

    return buffer
```

---

## Binary Data Patterns

### Byte-Order Functions (Little-Endian)

```mojo
fn read_le16(data: UInt8Ptr) -> UInt16:
    """Read little-endian 16-bit value."""
    return UInt16(data[0]) | (UInt16(data[1]) << 8)

fn read_le32(data: UInt8Ptr) -> UInt32:
    """Read little-endian 32-bit value."""
    return UInt32(data[0]) | (UInt32(data[1]) << 8) | \
           (UInt32(data[2]) << 16) | (UInt32(data[3]) << 24)

fn read_le64(data: UInt8Ptr) -> UInt64:
    """Read little-endian 64-bit value."""
    return UInt64(read_le32(data)) | (UInt64(read_le32(data + 4)) << 32)

fn write_le32(data: UInt8Ptr, val: UInt32):
    """Write little-endian 32-bit value."""
    data[0] = UInt8(val & 0xFF)
    data[1] = UInt8((val >> 8) & 0xFF)
    data[2] = UInt8((val >> 16) & 0xFF)
    data[3] = UInt8((val >> 24) & 0xFF)
```

### Byte-Order Functions (Big-Endian)

```mojo
fn read_be16(data: UInt8Ptr) -> UInt16:
    """Read big-endian 16-bit value."""
    return (UInt16(data[0]) << 8) | UInt16(data[1])

fn read_be32(data: UInt8Ptr) -> UInt32:
    """Read big-endian 32-bit value."""
    return (UInt32(data[0]) << 24) | (UInt32(data[1]) << 16) | \
           (UInt32(data[2]) << 8) | UInt32(data[3])

fn write_be32(data: UInt8Ptr, val: UInt32):
    """Write big-endian 32-bit value."""
    data[0] = UInt8((val >> 24) & 0xFF)
    data[1] = UInt8((val >> 16) & 0xFF)
    data[2] = UInt8((val >> 8) & 0xFF)
    data[3] = UInt8(val & 0xFF)
```

### Memory Copy (CRITICAL: Use Keyword Arguments)

```mojo
# WRONG: Positional arguments (deprecated, may break)
fn copy_wrong(dest: UInt8Ptr, src: UInt8Ptr, count: Int):
    memcpy(dest, src, count)  # WARNING: deprecated

# CORRECT: Keyword arguments (required in Mojo 0.26+)
fn copy_correct(dest: UInt8Ptr, src: UInt8Ptr, count: Int):
    memcpy(dest=dest, src=src, count=count)
```

### Bitcasting Between Types

```mojo
fn float32_to_bytes(val: Float32) -> UInt32:
    """Reinterpret float bits as integer."""
    var ptr = UnsafePointer.address_of(val)
    return ptr.bitcast[UInt32]()[]

fn bytes_to_float32(val: UInt32) -> Float32:
    """Reinterpret integer bits as float."""
    var ptr = UnsafePointer.address_of(val)
    return ptr.bitcast[Float32]()[]

fn read_float32_le(data: UInt8Ptr) -> Float32:
    """Read little-endian float32."""
    return bytes_to_float32(read_le32(data))
```

### Common Binary Formats

| Format | Byte Order | Header |
|--------|------------|--------|
| Safetensors | Little-endian | 8-byte size + JSON |
| PNG | Big-endian | 8-byte signature |
| PPM | ASCII | "P6\n" or "P3\n" |
| BMP | Little-endian | "BM" + sizes |
| GGUF | Little-endian | Magic + version |

---

## Integer Size Mismatch (CRITICAL)

### The Problem

Mojo's `Int` is 64-bit, but C's `int` is 32-bit. Direct bitcast causes data corruption.

```mojo
# WRONG: Direct bitcast of 64-bit Int array to 32-bit pointer
var mojo_ints: UnsafePointer[Int] = ...  # 64-bit values
var c_ints = mojo_ints.bitcast[Int32]()  # Reinterprets bytes, doesn't convert!

# Memory layout of [1, 1, 1, 1] as 64-bit:
# 0x01 0x00 0x00 0x00 0x00 0x00 0x00 0x00  (first Int = 1)
# 0x01 0x00 0x00 0x00 0x00 0x00 0x00 0x00  (second Int = 1)

# After bitcast, C sees these as 32-bit ints:
# int[0] = 1, int[1] = 0, int[2] = 1, int[3] = 0  <- WRONG!
```

### The Fix

```mojo
from memory.unsafe_pointer import alloc

fn pass_int_array_to_c(mojo_ints: UnsafePointer[Int], count: Int) -> Int32Ptr:
    """Convert Mojo Int array to C-compatible Int32 array."""
    # Allocate new buffer with correct element size
    var c_ints = alloc[Int32](count)

    # Explicit element-by-element conversion
    for i in range(count):
        c_ints[i] = Int32(mojo_ints[i])

    return c_ints

# Usage:
var mask32 = pass_int_array_to_c(attention_mask, seq_len)
defer mask32.free()  # Don't forget to free!

# Now safe to pass to C/Metal FFI
var success = mps_gpu_flash_attention(output, q, k, v, mask32, ...)
```

### Debugging This Issue

Symptoms:
- GPU kernel produces wrong results but compiles without errors
- Every other element in the array appears to be zero
- Results look "randomly wrong" but are deterministically incorrect
- CPU version works fine, GPU version doesn't

```mojo
# Debug print to catch this issue
print("  [DEBUG MASK] attention_mask[0..3]:", attention_mask[0], attention_mask[1], attention_mask[2], attention_mask[3])
print("  [DEBUG MASK32] mask32[0..3]:", mask32[0], mask32[1], mask32[2], mask32[3])
```

---

## Vendor Library Integration

### Why Vendor Libraries

Vendor libraries use undocumented hardware features and years of optimization. Custom implementations rarely beat them for standard operations.

| Operation | Custom | Vendor Library | Winner |
|-----------|--------|----------------|--------|
| Dense Matmul | 1.0x | 2-10x | Library |
| FFT | 1.0x | 5-20x | Library |
| Convolution | 1.0x | 3-10x | Library |
| Fused Ops | 1.2-2x | 1.0x | Custom |

### When Custom Kernels Help

```mojo
# GOOD: Fuse operations that libraries can't combine
fn fused_layernorm_linear(x: Ptr, weight: Ptr, scale: Ptr, bias: Ptr, out: Ptr):
    # LayerNorm + Linear in one kernel = fewer memory round-trips
    pass

# GOOD: Custom operations not in vendor libraries
fn rotary_position_embedding(...):
    # Libraries don't provide this
    pass
```

---

## Apple Accelerate BLAS (AMX)

### Benchmark Results

| Matrix Size | Custom Mojo | BLAS (AMX) | Speedup |
|-------------|-------------|------------|---------|
| 512x512 | 5.5 ms | 0.45 ms | **12x** |
| 1024x1024 | 48 ms | 0.85 ms | **56x** |
| 2048x2048 | 390 ms | 6.5 ms | **60x** |
| 4096x4096 | 3200 ms | 51 ms | **63x** |

### Basic BLAS Integration

```mojo
from sys.ffi import external_call
from memory import UnsafePointer
from builtin.type_aliases import MutAnyOrigin

comptime Float64Ptr = UnsafePointer[mut=True, type=Float64, origin=MutAnyOrigin]
comptime Float32Ptr = UnsafePointer[mut=True, type=Float32, origin=MutAnyOrigin]

# BLAS constants
comptime CblasRowMajor: Int32 = 101
comptime CblasColMajor: Int32 = 102
comptime CblasNoTrans: Int32 = 111
comptime CblasTrans: Int32 = 112


fn blas_dgemm(M: Int, N: Int, K: Int, alpha: Float64,
    A: Float64Ptr, B: Float64Ptr, beta: Float64, C: Float64Ptr):
    """
    Double-precision matrix multiply: C = alpha*A*B + beta*C
    A: MxK, B: KxN, C: MxN (row-major)
    """
    external_call["cblas_dgemm", NoneType](
        CblasRowMajor, CblasNoTrans, CblasNoTrans,
        Int32(M), Int32(N), Int32(K),
        alpha, A, Int32(K),  # A is MxK, lda=K
        B, Int32(N),         # B is KxN, ldb=N
        beta, C, Int32(N)    # C is MxN, ldc=N
    )


fn blas_sgemm(M: Int, N: Int, K: Int, alpha: Float32,
    A: Float32Ptr, B: Float32Ptr, beta: Float32, C: Float32Ptr):
    """Single-precision matrix multiply."""
    external_call["cblas_sgemm", NoneType](
        CblasRowMajor, CblasNoTrans, CblasNoTrans,
        Int32(M), Int32(N), Int32(K),
        alpha, A, Int32(K),
        B, Int32(N),
        beta, C, Int32(N)
    )
```

### Building with Accelerate Framework

```bash
# Link against Accelerate framework for BLAS
mojo build main.mojo -o app -Xlinker "-framework" -Xlinker "Accelerate"
```

### Common BLAS Operations

```mojo
fn blas_dgemv(M: Int, N: Int, alpha: Float64,
    A: Float64Ptr, x: Float64Ptr, beta: Float64, y: Float64Ptr):
    """y = alpha*A*x + beta*y, where A is MxN."""
    external_call["cblas_dgemv", NoneType](
        CblasRowMajor, CblasNoTrans,
        Int32(M), Int32(N),
        alpha, A, Int32(N),
        x, Int32(1),  # incX
        beta, y, Int32(1)  # incY
    )

fn blas_ddot(n: Int, x: Float64Ptr, y: Float64Ptr) -> Float64:
    """Dot product of two vectors."""
    return external_call["cblas_ddot", Float64](
        Int32(n), x, Int32(1), y, Int32(1)
    )

fn blas_dscal(n: Int, alpha: Float64, x: Float64Ptr):
    """Scale vector: x = alpha * x."""
    external_call["cblas_dscal", NoneType](
        Int32(n), alpha, x, Int32(1)
    )

fn blas_daxpy(n: Int, alpha: Float64, x: Float64Ptr, y: Float64Ptr):
    """y = alpha*x + y."""
    external_call["cblas_daxpy", NoneType](
        Int32(n), alpha, x, Int32(1), y, Int32(1)
    )
```

### Neural Network Layer Example

```mojo
fn linear_layer_blas(
    weights: Float32Ptr,  # out_features x in_features
    bias: Float32Ptr,     # out_features
    input: Float32Ptr,    # batch x in_features
    output: Float32Ptr,   # batch x out_features
    batch: Int, in_features: Int, out_features: Int
):
    """Linear layer: output = input @ weights.T + bias using BLAS."""

    # Matrix multiply: output = input @ weights.T
    external_call["cblas_sgemm", NoneType](
        CblasRowMajor, CblasNoTrans, CblasTrans,  # Transpose B
        Int32(batch), Int32(out_features), Int32(in_features),
        Float32(1.0),
        input, Int32(in_features),
        weights, Int32(in_features),  # Stored as outxin, accessed as inxout
        Float32(0.0),
        output, Int32(out_features)
    )

    # Add bias to each row
    for b in range(batch):
        for o in range(out_features):
            output[b * out_features + o] += bias[o]
```

### Cross-Platform BLAS

```bash
# macOS - Apple Accelerate
mojo build main.mojo -o app -Xlinker "-framework" -Xlinker "Accelerate"

# Linux - OpenBLAS
mojo build main.mojo -o app -Xlinker "-lopenblas"

# Linux - Intel MKL
mojo build main.mojo -o app -Xlinker "-lmkl_rt"
```

---

## Dynamic Library Loading

### Load Library and Get Functions

```mojo
from sys.ffi import OwnedDLHandle, RTLD

# Function type aliases
comptime CreateCtxFn = fn() -> NonePtr
comptime DestroyCtxFn = fn(NonePtr) -> None
comptime MatmulFn = fn(NonePtr, Int32, Int32, Int32, Float32Ptr, Float32Ptr, Float32Ptr) -> Int32

fn main() raises:
    # Load the dynamic library
    var lib = OwnedDLHandle("./libcustom.so", RTLD.NOW)  # .dylib on macOS

    # Get function pointers
    var create_ctx = lib.get_function[CreateCtxFn]("create_context")
    var destroy_ctx = lib.get_function[DestroyCtxFn]("destroy_context")
    var matmul = lib.get_function[MatmulFn]("matmul_f32")

    # Create context and use
    var ctx = create_ctx()
    _ = matmul(ctx, 1024, 1024, 1024, A, B, C)
    destroy_ctx(ctx)
```

### Platform-Specific Loading

```mojo
fn load_platform_library() raises -> OwnedDLHandle:
    """Load appropriate library for current platform."""
    @parameter
    if os_is_macos():
        return OwnedDLHandle("./libcustom.dylib", RTLD.NOW)
    elif os_is_linux():
        return OwnedDLHandle("./libcustom.so", RTLD.NOW)
    else:
        return OwnedDLHandle("./custom.dll", RTLD.NOW)
```

### Building Shared Libraries

```bash
# Linux
gcc -shared -fPIC -o libcustom.so custom.c

# macOS
clang -dynamiclib -o libcustom.dylib custom.c

# macOS with frameworks (e.g., Metal)
clang -dynamiclib -o libgpu_wrapper.dylib gpu_wrapper.m \
    -framework Metal -fobjc-arc
```

---

## GPU Library Integration

### cuBLAS Integration Pattern

```mojo
from sys.ffi import external_call, DLHandle
from memory import UnsafePointer

# Load cuBLAS library
var cublas = DLHandle("libcublas.so")

# cuBLAS handle type
struct cublasHandle_t:
    var handle: UnsafePointer[NoneType]

# Initialize cuBLAS
fn cublas_create() -> cublasHandle_t:
    var handle = cublasHandle_t(UnsafePointer[NoneType]())
    var status = external_call["cublasCreate", Int32](
        UnsafePointer(to=handle.handle)
    )
    debug_assert(status == 0, "cuBLAS create failed")
    return handle

# SGEMM: C = alpha * A * B + beta * C
fn cublas_sgemm(
    handle: cublasHandle_t,
    m: Int, n: Int, k: Int,
    alpha: Float32,
    A: UnsafePointer[Float32], lda: Int,
    B: UnsafePointer[Float32], ldb: Int,
    beta: Float32,
    C: UnsafePointer[Float32], ldc: Int,
):
    # cuBLAS uses column-major, so we compute C^T = B^T * A^T
    # which gives row-major C = A * B
    var status = external_call["cublasSgemm", Int32](
        handle.handle,
        0,  # CUBLAS_OP_N (no transpose)
        0,  # CUBLAS_OP_N
        Int32(n), Int32(m), Int32(k),  # Note: n, m swapped for row-major
        UnsafePointer(to=alpha),
        B, Int32(ldb),
        A, Int32(lda),
        UnsafePointer(to=beta),
        C, Int32(ldc),
    )
    debug_assert(status == 0, "cuBLAS SGEMM failed")
```

### Platform Abstraction Pattern

```mojo
struct GPUBlas:
    var _handle: UnsafePointer[NoneType]
    var _is_nvidia: Bool

    fn __init__(out self, ctx: DeviceContext):
        @parameter
        if is_nvidia_gpu():
            self._handle = _cublas_create()
            self._is_nvidia = True
        elif is_amd_gpu():
            self._handle = _rocblas_create()
            self._is_nvidia = False
        else:
            abort("No GPU BLAS available")

    fn gemm(
        self,
        A: DeviceBuffer[DType.float32],
        B: DeviceBuffer[DType.float32],
        C: DeviceBuffer[DType.float32],
        m: Int, n: Int, k: Int,
    ):
        if self._is_nvidia:
            _cublas_sgemm(self._handle, m, n, k, ...)
        else:
            _rocblas_sgemm(self._handle, m, n, k, ...)

    fn __del__(deinit self):
        if self._is_nvidia:
            _cublas_destroy(self._handle)
        else:
            _rocblas_destroy(self._handle)
```

### Library vs Custom Kernel Decision

| Operation | Library | Custom Kernel |
|-----------|---------|---------------|
| Dense GEMM | cuBLAS/rocBLAS | Only for small matrices |
| Batched GEMM | Library | Fused with other ops |
| Convolution | cuDNN/MIOpen | Non-standard strides |
| FFT | cuFFT/rocFFT | Always use library |
| Sparse ops | cuSPARSE/rocSPARSE | Custom sparsity patterns |
| Element-wise | Custom kernel | Simpler, can fuse |
| Reductions | Custom kernel | Better for fused ops |

---

## GPU Program Caching

Cache compiled GPU programs for 10-50x speedup.

### Caching Pattern

```c
#define MAX_CACHE_SIZE 64

typedef struct {
    int param1, param2, param3;  // Parameters that define the program
    GPUProgram *program;         // Cached compiled program
} cache_entry_t;

static cache_entry_t g_cache[MAX_CACHE_SIZE];
static int g_cache_count = 0;

GPUProgram* get_cached_program(int param1, int param2, int param3) {
    // Search for existing program with same parameters
    for (int i = 0; i < g_cache_count; i++) {
        if (g_cache[i].param1 == param1 &&
            g_cache[i].param2 == param2 &&
            g_cache[i].param3 == param3) {
            return g_cache[i].program;  // Reuse!
        }
    }
    // Create new program only if not found
    GPUProgram *program = create_gpu_program(param1, param2, param3);
    // Add to cache and return...
    return program;
}
```

### What to Cache by Platform

| Platform | Cacheable Object | Typical Speedup |
|----------|------------------|-----------------|
| Apple/MPS | MPSGraph, MPSCommandBuffer | 10-50x |
| CUDA | CUDA Graphs, Compiled PTX | 5-20x |
| Vulkan | VkPipeline objects | 10-30x |
| OpenCL | cl_program, cl_kernel | 5-15x |

---

## String Handling for C Interop

### String Indexing

```mojo
# WRONG: Direct string indexing
fn get_char_wrong(s: String, i: Int) -> UInt8:
    return s[i]  # ERROR: no matching method '__getitem__'

# CORRECT: Use as_bytes() for byte access
fn get_char(s: String, i: Int) -> UInt8:
    return s.as_bytes()[i]

# Iterating over string bytes
fn process_bytes(s: String):
    var bytes = s.as_bytes()
    for i in range(len(bytes)):
        var byte = bytes[i]
        # process byte...
```

### String Conversion

```mojo
# WRONG: Using str() for conversion
fn int_to_string_wrong(val: Int) -> String:
    return str(val)  # ERROR: 'str' not found

# CORRECT: Use String() constructor
fn int_to_string(val: Int) -> String:
    return String(val)

fn float_to_string(val: Float64) -> String:
    return String(val)

fn build_message(count: Int, name: String) -> String:
    return "Found " + String(count) + " items for " + name
```

### Writing Strings to Files

```mojo
fn write_string_to_file(f: FILE, s: String):
    """Write string to file using libc fwrite."""
    # String.unsafe_ptr() returns pointer to internal char data
    # bitcast to UInt8 for fwrite
    _ = fwrite(s.unsafe_ptr().bitcast[UInt8](), 1, len(s), f)

# Example: Writing PPM header
fn write_ppm_header(f: FILE, width: Int, height: Int):
    write_string_to_file(f, "P6\n")
    write_string_to_file(f, String(width) + " " + String(height) + "\n")
    write_string_to_file(f, "255\n")
```

---

## Python GIL Management

### GIL States

```mojo
@register_passable("trivial")
struct GILAcquired:
    """Marker type indicating the GIL is held by this thread."""
    pass

@register_passable("trivial")
struct GILReleased:
    """Marker type indicating the GIL is NOT held by this thread."""
    pass
```

### Release GIL During Mojo Computation

```mojo
fn long_computation() raises -> PythonObject:
    var result: MyResult

    # Release GIL while doing pure Mojo work
    Python.release_gil()
    result = expensive_mojo_function()  # GIL released - Python threads can run
    Python.acquire_gil()

    # Re-acquire GIL for Python interop
    return Python.import_module("json").dumps(result)
```

### Context Manager Pattern (Preferred)

```mojo
fn process_batch(data: PythonObject) raises -> PythonObject:
    # Convert Python input to Mojo (GIL needed)
    var mojo_data = convert_to_mojo(data)

    var result: MojoResult
    with Python.GILReleased():
        # Pure Mojo computation - GIL automatically released/re-acquired
        result = heavy_processing(mojo_data)

    # Convert back to Python (GIL re-acquired)
    return convert_to_python(result)
```

### GIL Rules

| Situation | GIL Status | Action |
|-----------|------------|--------|
| Calling from Python | Held | Keep it for Python calls |
| Long Mojo computation | Held | Release it |
| Calling Python API | Required | Acquire if not held |
| Parallel Mojo threads | Don't need | Release for parallelism |
| Python callbacks | Not held | Acquire before calling |

### Common GIL Mistakes

```mojo
# BAD: Deadlock - releasing when already released
Python.release_gil()
Python.release_gil()  # Double release - undefined behavior!

# BAD: Deadlock - Python call without GIL
Python.release_gil()
var x = Python.import_module("os")  # CRASH - no GIL!
Python.acquire_gil()

# BAD: Blocking Python threads unnecessarily
fn handle_request(request: PythonObject) raises -> PythonObject:
    # Should release GIL during file I/O
    var data = read_large_file("data.bin")  # Blocks Python threads
    return process(data)
```

---

## MPS/Metal GPU Performance Optimization

Critical learnings from optimizing transformer inference on Apple Silicon with MPSGraph and Metal.

### Counter-Intuitive Finding: GPU Beats CPU Even for Tiny Matrices

**Hypothesis:** CPU BLAS (Apple Accelerate) would be faster for small resolutions due to avoiding GPU dispatch overhead.

**Reality:** CPU BLAS is **6.6x SLOWER** than GPU path even at 64×64 resolution.

| Path | Time (64×64, 4 steps) | Relative |
|------|----------------------|----------|
| GPU (MPS) | 1839ms | 1x |
| CPU (Accelerate) | 12133ms | **6.6x slower** |

**Why:**
- Apple's MPS is highly optimized even for small matrices
- CPU BLAS has function call overhead and cache misses
- BF16→F32 weight conversion adds CPU latency
- Modern Apple GPUs have very low dispatch latency (~1.5ms)

**Lesson:** Don't assume CPU is faster for small workloads—benchmark first.

### MPSGraph Overhead Analysis

At small resolutions, dispatch overhead dominates compute time.

**Key Numbers (FLUX.2 transformer):**
- 310 GPU operations per denoising step
- ~1.5ms overhead per operation = 465ms fixed overhead
- At 64×64: actual compute ~75ms, overhead ~465ms
- At 512×512: compute dominates, overhead negligible

**Per-operation overhead sources:**
1. MPSGraphTensorData wrapper creation (3 per linear op)
2. NSDictionary creation for feeds/results (2 per linear op)
3. `encodeToCommandBuffer` call
4. Objective-C message dispatch

**Total:** ~550 Obj-C allocations per step, inherent to MPSGraph API.

### Kernel Fusion Effectiveness

**What Works:**

| Fusion | Ops Saved | Impact |
|--------|-----------|--------|
| Triple linear (QKV) | 3→1 | Good |
| Fused QKNorm + RoPE | 3→1 | Good |
| Flash attention threadgroups 128→256 | N/A | 10-15% |

**What Doesn't Work:**

| Fusion | Result | Why |
|--------|--------|-----|
| MLP gate+up with split kernel | Neutral/negative | Split kernel overhead offsets fusion |
| BF16 weight caching | No improvement | Small weights (512 bytes), mutex overhead |
| Custom fused AdaLN+QKV | 2x slower | MPSGraph's matmul is more optimized |

**Lesson:** Fusion only helps if the fused kernel is more efficient than the dispatch overhead saved. MPSGraph is often more optimized than custom Metal kernels for standard ops.

### Command Encoder Batching

**Problem:** Each custom Metal kernel created its own command encoder (67 create/end cycles per step).

**Solution:** Persistent encoder mode—share encoder across consecutive custom kernels.

**Result:** Reduced to ~15 encoder cycles per step.

**Caveat:** MPSGraph operations use different API and interrupt encoder sharing.

### Flash Attention Threadgroup Optimization

**Discovery:** M3 Max supports 1024 threads per threadgroup, but flash attention was using only 128 (12.5% utilization).

**Fix:** Increase to 256 threads.

**Impact:** 10-15% attention speedup.

### MPSGraph Pre-compilation

**Problem:** JIT compilation adds ~100-150ms on first use per resolution.

**Solution:** Pre-compile graphs for target resolution only (not all possible resolutions).

**Trade-off:**
- Pre-compile everything: +3s startup, faster first inference
- JIT on demand: Fast startup, slower first inference

**Best approach:** Pre-compile when weights are preloaded with known target resolution.

### Graph Cache Sizing

MPSGraph caches compiled graphs by input shapes. At small sizes, cache eviction causes re-compilation.

**Recommended cache sizes:**
- SDPA graphs: 16 (up from 8)
- Linear graphs: 64 (up from 32)
- Threshold for MPSGraph vs custom: seq_len ≥ 8

### MLP Fusion is Resolution-Dependent

**Critical Discovery:** MLP gate+up fusion behaves differently at different resolutions.

| Resolution | Fusion Impact | Why |
|------------|---------------|-----|
| Small (64-128) | Neutral/positive | Fewer dispatches helps |
| Large (512+) | **Negative** | Split kernel overhead exceeds dispatch savings |

**Pattern:**
```mojo
# Fused (faster at small resolutions, slower at large)
_ = gpu_linear(input, fused_out, fused_weight, seq, hidden, mlp*2)
split_gate_up(fused_out, gate, up, seq, mlp)  # Extra kernel!

# Separate (slower at small, faster at large resolutions)
_ = gpu_linear(input, gate, gate_weight, seq, hidden, mlp)
_ = gpu_linear(input, up, up_weight, seq, hidden, mlp)
```

**Recommendation:** Profile at your target resolution before committing to fusion. MPSGraph may already optimize consecutive matmuls internally.

### Mega-Kernel Fusion Pattern

For significant overhead reduction, fuse multiple operations into single Metal kernels:

**Post-Attention Mega-Kernel Example:**
```metal
kernel void fused_post_attention_bf16(
    device const ushort *attn_out,    // From attention
    device const ushort *mlp_gate,    // From MLP split
    device const ushort *mlp_up,
    device ushort *hidden_state,      // In-place residual update
    device const ushort *proj_weight,
    device const float *gate_mod,
    // ... dimensions
) {
    // Fuses: SwiGLU + Concat + Projection + Gated Add
    // All in one kernel - no intermediate memory writes
}
```

**Impact:** Reduced 60 kernel dispatches per forward pass, ~14% speedup.

### Direct MPS vs MPSGraph Threshold

MPSGraph has ~1.0-1.6ms overhead per operation. Direct MPS has ~0.3-0.5ms.

**Optimal threshold (FLOPS-based):**
```c
static int use_mpsgraph(int seq, int in_dim, int out_dim) {
    long long flops = (long long)seq * in_dim * out_dim;
    if (flops < 50000000) return 0;  // Direct MPS for <50M FLOPS
    if (seq < 64) return 0;          // Small sequences
    if (in_dim < 512 && out_dim < 512) return 0;  // Small matrices
    return 1;  // MPSGraph only for large operations
}
```

### Performance Results Summary

| Resolution | Optimization Impact | vs PyTorch |
|------------|---------------------|------------|
| 64×64 | 45% faster (2905→1595ms) | 2.0x slower |
| 128×128 | 38% faster (2716→1695ms) | 1.4x slower |
| 256×256 | 27% faster (3062→2230ms) | **11% faster** |
| 512×512 | 17% faster (4838→4040ms) | **16% faster** |

**Bottom line:** Now beating PyTorch at 256×256 and 512×512 through mega-kernel fusion and optimized dispatch thresholds. Small resolutions still limited by per-operation overhead.

### Resolution Execution Plans (Buffer Pre-allocation)

**Problem:** At small workloads, per-operation overhead dominates. Each GPU operation incurs:
1. Mutex lock on buffer pool allocation
2. Cache lookup in tensor pool
3. MPSGraphTensorData wrapper creation
4. NSDictionary creation for feeds/results

**Solution:** Pre-allocate all intermediate buffers during warmup, then replay with fixed buffer addresses.

**Pattern:**
```c
typedef struct {
    int width, height;          // Configuration key
    int is_recording;           // Recording vs replay mode
    id<MTLBuffer> buffers[512]; // Pre-allocated buffers
    size_t buffer_sizes[512];   // Buffer sizes for validation
    int num_buffers;
    int next_buffer;            // Replay index
} resolution_plan_t;

// Fast path: No mutex, no cache lookup
static id<MTLBuffer> tensor_pool_get(Context* ctx, size_t size) {
    if (res_plan_active()) {
        id<MTLBuffer> buf = res_plan_get_buffer(ctx, size);
        if (buf) return buf;  // Hit! No allocation overhead
    }
    // ... normal pool path with mutex
}
```

**Implementation strategy:**
1. First inference: Record all buffer allocations
2. Subsequent inferences: Replay with pre-allocated buffers
3. Skip buffer release during replay (reuse same addresses)

**Impact:** 10-11% speedup at small workloads (64-256 resolution).

**Caveats:**
- Memory pressure at large workloads (512+ buffers)
- Only effective when workload is fixed (same shapes)
- Requires validation that replay sizes match recorded sizes

### CPU Encoding vs GPU Compute Bottleneck

**Critical discovery:** At large workloads, CPU command encoding time exceeds GPU execution time.

**Example profiling (512×512 inference):**
```
GPU linear encoding: 508ms (CPU time building commands)
GPU execution: 345ms (actual GPU work)
```

**Implication:** Further GPU kernel optimization has diminishing returns when CPU encoding is the bottleneck.

**Diagnostic approach:**
```mojo
var encode_start = perf_counter_ns()
# ... queue GPU operations ...
var encode_time = (perf_counter_ns() - encode_start) / 1_000_000.0

mps.gpu_batch_wait()
var total_time = (perf_counter_ns() - encode_start) / 1_000_000.0

var gpu_time = total_time - encode_time
print("Encode:", encode_time, "ms, GPU:", gpu_time, "ms")
```

**Solutions when CPU-bound:**
1. Reduce operation count through fusion
2. Batch more operations per command buffer
3. Use resolution execution plans to skip allocation overhead
4. Consider parallelizing command encoding (complex)

### CUDA Graphs vs Metal Limitations

**Why PyTorch with CUDA Graphs beats Metal at small workloads:**

| Feature | CUDA Graphs | Metal |
|---------|-------------|-------|
| Record entire command stream | Yes | No |
| Replay with near-zero CPU cost | Yes | No |
| Works with vendor libs (cuBLAS) | Yes | N/A |
| MTLIndirectCommandBuffer | N/A | Custom kernels only |

**Metal's constraints:**
- MTLIndirectCommandBuffer doesn't support MPSGraph operations
- MPSGraph requires per-call encoding (NSDictionary, TensorData creation)
- Achieving CUDA Graph-like replay requires rewriting ALL operations as custom Metal kernels

**Practical implications:**
1. Accept higher overhead at small workloads on Metal
2. Focus optimization on large workloads where GPU compute dominates
3. Use resolution execution plans for partial mitigation
4. Consider custom Metal kernels for critical hot paths

### GPU State Degradation

**Symptom:** Performance degrades significantly after many benchmark runs.

**Example:** 64×64 inference: 1600ms → 2300ms (44% regression)

**Possible causes:**
1. Metal driver memory fragmentation
2. MPSGraph cache corruption or eviction thrashing
3. Thermal throttling on sustained load
4. Buffer pool fragmentation

**Solutions:**
1. Periodic process restart in production
2. Monitor GPU memory and temperature
3. Use fixed buffer sizes to reduce fragmentation
4. Reset MPSGraph caches between long sessions

---

## BF16/F16 Data Type Considerations

### Float Format Comparison

- **BF16 (Brain Float 16):** sign(1) + exp(8) + mant(7) - Same dynamic range as F32
- **F16 (IEEE Half):** sign(1) + exp(5) + mant(10) - Lower dynamic range, higher precision

### BF16 to F16 Conversion (Lossy)

```c
static inline uint16_t bf16_to_f16(uint16_t bf16) {
    uint32_t sign = (bf16 >> 15) & 0x1;
    int32_t exp = (bf16 >> 7) & 0xFF;  // bf16 exponent (bias 127)
    uint32_t mant = bf16 & 0x7F;       // bf16 mantissa (7 bits)

    if (exp == 0) return (uint16_t)(sign << 15);  // Zero/denormal
    if (exp == 0xFF) return (uint16_t)((sign << 15) | 0x7C00 | (mant << 3));  // Inf/NaN

    int32_t new_exp = exp - 127 + 15;  // Rebias from 127 to 15
    if (new_exp <= 0) return (uint16_t)(sign << 15);  // Underflow
    if (new_exp >= 31) return (uint16_t)((sign << 15) | 0x7C00);  // Overflow

    return (uint16_t)((sign << 15) | (new_exp << 10) | (mant << 3));
}
```

### MPS Data Type Constraints

| Input A | Weights B | Output C | Supported |
|---------|-----------|----------|-----------|
| F32 | F32 | F32 | Yes |
| F32 | F16 | F32 | Yes |
| BF16 | BF16 | BF16 | Yes |
| F32 | BF16 | F32 | **NO** |

### Workarounds

```mojo
# Option 1: Convert BF16 to F16 (lossy but compatible)
var f16_weights = convert_bf16_to_f16(bf16_weights)
vendor_matmul(f32_input, f16_weights, f32_output)

# Option 2: Use consistent precision pipeline
var bf16_input = convert_f32_to_bf16(f32_input)
vendor_matmul_bf16(bf16_input, bf16_weights, bf16_output)
var f32_result = convert_bf16_to_f32(bf16_output)

# Option 3: Use F32 throughout (simple but uses more memory)
var f32_weights = convert_bf16_to_f32(bf16_weights)  # Lossless
vendor_matmul(f32_input, f32_weights, f32_output)
```

---

## Missing Math Functions

Some math functions are not in Mojo's math module. Implement them using primitives.

### Power Function

```mojo
from math import exp, log, sqrt

fn pow(base: Float64, exponent: Float64) -> Float64:
    """Power function - not available in math module."""
    if base <= 0:
        if base == 0 and exponent > 0:
            return 0.0
        return 0.0  # Handle edge cases
    return exp(exponent * log(base))

fn ipow(base: Int, exponent: Int) -> Int:
    """Integer power using repeated squaring - O(log n)."""
    if exponent < 0:
        return 0
    if exponent == 0:
        return 1

    var result = 1
    var b = base
    var e = exponent

    while e > 0:
        if e & 1:
            result *= b
        b *= b
        e >>= 1

    return result
```

### Available vs Missing Functions

**Available in `from math import`:**
- `sqrt`, `exp`, `log`, `log2`, `log10`
- `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`
- `floor`, `ceil`, `abs`

**Not available (implement yourself):**
| Function | Implementation |
|----------|----------------|
| `pow(a, b)` | `exp(b * log(a))` |
| `hypot(a, b)` | `sqrt(a*a + b*b)` |
| `cbrt(x)` | `exp(log(x)/3.0)` |
| `round(x)` | `floor(x + 0.5)` |

---

## Decision Guide

| Scenario | Approach | See Also |
|----------|----------|----------|
| Matrix multiply | Use vendor BLAS (10-100x faster) | Apple Accelerate, cuBLAS |
| Need C string | Use `unsafe_cstr_ptr()`, mind lifetime | CString Safety |
| Passing int arrays to C | Convert Int to Int32 explicitly | Integer Size Mismatch |
| Loading optional library | Use `OwnedDLHandle` with RTLD.NOW | Dynamic Loading |
| BF16 data on MPS | Convert to F16 or F32 | Data Type Limitations |
| Long Mojo computation from Python | Release GIL | GIL Management |
| Binary file format | Use byte-order functions | Binary Data Patterns |

---

## Quick Reference

- **CString lifetime**: `unsafe_cstr_ptr()` only valid while String lives
- **Int to C**: Always convert `Int` to `Int32` for C's `int`
- **memcpy**: Use keyword arguments: `memcpy(dest=d, src=s, count=n)`
- **BLAS build**: `mojo build -Xlinker "-framework" -Xlinker "Accelerate"`
- **GPU caching**: Cache compiled programs by parameters for 10-50x speedup
- **GIL**: Release during long Mojo computation, acquire for Python calls
- **BF16 on MPS**: Convert to F16 (lossy) or F32 (lossless)

---

## Related Patterns

- [`python-interop.md`](python-interop.md) - Python-specific interop patterns
- [`memory-ownership.md`](memory-ownership.md) - Memory safety for FFI buffers
- [`gpu-fundamentals.md`](gpu-fundamentals.md) - GPU programming patterns

---

## References

- [Mojo FFI Documentation](https://docs.modular.com/mojo/std/sys/ffi/)
- [Apple Accelerate Documentation](https://developer.apple.com/documentation/accelerate)
- [BLAS Reference](https://developer.apple.com/documentation/accelerate/blas)
