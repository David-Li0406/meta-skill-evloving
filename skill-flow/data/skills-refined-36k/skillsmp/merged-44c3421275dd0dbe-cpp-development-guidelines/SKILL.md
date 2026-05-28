---
name: cpp-development-guidelines
description: Use this skill for expert-level guidance on modern C++ development, covering C++17/20 standards, memory management, performance optimization, and best practices.
---

# C++ Development Guidelines

You are an expert in modern C++ development with deep knowledge of C++17/20 standards, memory management, and high-performance programming.

## Core Concepts

### Modern C++ Features
- **C++17 Features**: Use structured bindings, `std::optional`, `std::variant`, `if constexpr`, and `std::string_view`.
- **C++20 Features**: Utilize concepts, ranges, `std::span`, coroutines, and modules.

### Memory Management
- **Smart Pointers**: Use `std::unique_ptr` for exclusive ownership, `std::shared_ptr` for shared ownership, and `std::weak_ptr` to break circular references. Avoid raw pointers.
- **RAII (Resource Acquisition Is Initialization)**: Wrap resources in classes with proper destructors to ensure exception safety.

### Performance Optimization
- Use `const` and `constexpr` liberally, prefer move semantics, and avoid unnecessary copies. Profile before optimizing.

## Code Style and Structure
- Write clean, modern C++ code following C++17/20 standards.
- Use meaningful variable and function names, and follow the Single Responsibility Principle.
- Keep functions small and focused.

## Naming Conventions
- Use PascalCase for classes and structs, camelCase for functions and variables, SCREAMING_SNAKE_CASE for constants, and snake_case for namespaces.

## Error Handling
- Use exceptions for error handling and define custom exception types. Provide strong exception guarantees where possible.

## Security
- Ensure buffer safety by using `std::array` and `std::vector` with bounds checking. Prefer `std::string` over C-style strings.

## Concurrency
- Use `std::thread`, `std::mutex`, and `std::atomic` for threading and synchronization. Prefer `std::async` for simple async operations.

## Testing
- Write unit tests with frameworks like Google Test or Catch2, and use sanitizers during testing.

## Documentation
- Use Doxygen-style comments for documentation, including usage examples and thread safety requirements.

## Build System
- Use CMake for cross-platform builds, organize code into logical modules, and enable compiler warnings and static analysis.

## Best Practices
- Prefer stack allocation over heap allocation, use `std::make_unique` and `std::make_shared`, and avoid `new` and `delete` in application code.

## Anti-Patterns to Avoid
- Avoid raw pointers for ownership, manual memory management, and unnecessary copies. Use smart pointers and RAII.

## Resources
- C++ Reference: https://en.cppreference.com/
- C++ Core Guidelines: https://isocpp.github.io/CppCoreGuidelines/
- Compiler Explorer: https://godbolt.org/
- CPP Reference: https://cplusplus.com/