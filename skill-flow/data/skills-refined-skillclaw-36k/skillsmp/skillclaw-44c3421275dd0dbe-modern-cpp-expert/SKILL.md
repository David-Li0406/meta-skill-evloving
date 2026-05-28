---
name: modern-cpp-expert
description: Use this skill when you need expert guidance on modern C++ development, including C++17/20/23 features, memory management, and performance optimization.
---

# Modern C++ Expert

This skill provides expert guidance for modern C++ development, covering C++17, C++20, and C++23 features, memory management techniques, and performance optimization strategies.

## Core Concepts

### Modern C++ Features
- **C++17 Features**:
  - Structured bindings for tuple unpacking
  - `std::optional` for values that may not exist
  - `std::variant` for type-safe unions
  - `if constexpr` for compile-time conditionals
  - `std::string_view` for non-owning string references

- **C++20 Features**:
  - Concepts and constraints
  - Ranges and views
  - Coroutines
  - Modules
  - Three-way comparison (spaceship operator)
  - `std::format`
  - `std::span`
  - Designated initializers
  - `consteval` and `constinit`

- **C++23 Features**:
  - (Add any relevant features as they become standardized)

### Memory Management
- **RAII (Resource Acquisition Is Initialization)**:
  - Use RAII for all resource management.
  - Wrap resources in classes with proper destructors.
  - Ensure exception safety through RAII.
  - Use scope guards for cleanup operations.

- **Smart Pointers**:
  - Use `std::unique_ptr` for exclusive ownership.
  - Use `std::shared_ptr` only when shared ownership is required.
  - Use `std::weak_ptr` to break circular references.
  - Avoid raw owning pointers.

### Performance Optimization
- Zero-cost abstractions
- Inline optimization
- Template metaprogramming
- Compile-time computation (`constexpr`)
- Cache-friendly data structures
- SIMD operations
- Profile before optimizing

## Code Style and Structure
- Write clean, modern C++ code following C++17/20 standards.
- Use meaningful variable and function names.
- Follow the Single Responsibility Principle.
- Prefer composition over inheritance.
- Keep functions small and focused.

## Naming Conventions
- Use PascalCase for classes and structs.
- Use camelCase for functions, variables, and methods.
- Use SCREAMING_SNAKE_CASE for constants and macros.
- Use snake_case for namespaces.
- Prefix member variables with `m_` or use trailing underscore.

## Error Handling
- Use exceptions for error handling.
- Define custom exception types for domain-specific errors.
- Use `noexcept` for functions that don't throw.
- Catch exceptions by const reference.
- Provide strong exception guarantees where possible.

## Example Code Snippets

### Concepts (C++20)
```cpp
#include <concepts>
#include <iostream>
#include <vector>

template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<Numeric T>
T add(T a, T b) {
    return a + b;
}

template<typename T>
concept Container = requires(T container) {
    typename T::value_type;
    { container.begin() } -> std::same_as<typename T::iterator>;
    { container.end() } -> std::same_as<typename T::iterator>;
    { container.size() } -> std::convertible_to<std::size_t>;
};

template<Container C>
void process(const C& container) {
    for (const auto& item : container) {
        std::cout << item << ' ';
    }
}
```

### Ranges and Views (C++20)
```cpp
#include <ranges>
#include <vector>
#include <algorithm>

std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

auto even_squares = numbers
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * n; });

for (int value : even_squares) {
    std::cout << value << ' ';
}
```