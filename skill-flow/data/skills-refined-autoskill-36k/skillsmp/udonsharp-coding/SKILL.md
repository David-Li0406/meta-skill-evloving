---
name: udonsharp-coding
description: A guide for coding with UdonSharp. Use this when you are asked to create or edit UdonSharp programs. Code that inherits from UdonSharpBehavior falls under UdonSharp code.
---

UdonSharp generally follows C# syntax, but its features are limited.

# Supported C# Features

- Flow control: `if`, `else`, `while`, `for`, `do`, `foreach`, `switch`, `return`, `break`, `continue`, `ternary operator (condition ? true : false)`, `??`
- Implicit and explicit type conversions
- Arrays and array indexers
- All built-in arithmetic operators
- Conditional short circuiting `(true || CheckIfTrue())` will not execute `CheckIfTrue()`
- `typeof()`
- Extern methods with `out` or `ref` parameters, such as many variants of `Physics.Raycast()`
- User defined methods with parameters and return values, supports out/ref, extension methods, and `params`
- User defined properties
- Static user methods
- UdonSharpBehaviour inheritence, virtual methods, etc
- Unity/Udon event callbacks with arguments. For instance, registering an `OnPlayerJoined` event with a `VRCPlayerApi` argument is valid.
- String interpolation
- Field initializers
- Jagged arrays
- Referencing other custom UdonSharpBehaviour classes, accessing fields, and calling methods on them
- Recursive method calls are supported via the `[RecursiveMethod]` attribute

# Differences from Unity C#

- Udon currently only supports array `[]` collections and by extension UdonSharp only supports arrays at the moment.
- Field initilizers are evaluated at compile time, if you have any init logic that depends on other objects in the scene you should use Start for this.
- Use the UdonSynced attribute on fields that you want to sync.
- Numeric casts are checked for overflow due to UdonVM limitations
- The internal type of variables returned by `.GetType()` will not always match what you may expect since U# abstracts some types in order to make them work in Udon. For instance, any jagged array type will return a type of `object[]` instead of something like `int[][]` for a 2D int jagged array.

## Instantiate

You cannot create a new GameObject using `new GameObject()` and similar APIs. In UdonSharp, you create new objects by cloning an existing `GameObject` in the scene using `Instantiate()`. Additionally, only `GameObject` can be instantiated via `Instantiate()`.

# Best Practices

## Use `Utilities.IsValid` for null checks

`bool IsValid(object obj)` returns true when `obj` is not null (or is otherwise valid). In UdonSharp, this is faster than doing null checks with `==`.

# Basic Template

```cs
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class UdonSharpScript : UdonSharpBehaviour
{

}
```

# Networking

If the problem you are addressing involves network synchronization, read the document `references/en/udon_network/README.md`. These documents describe the concepts and methods required to implement network logic in Udon.

# Class Design

If you need shared logic, encapsulation, or inheritance, be aware that UdonSharp has important limitations. See `references/en/udon_class.md`.

# Player Tracking

If you are implementing things like gaze-following objects or objects that follow avatar bones, see `references/en/udon_playerTracking.md`. It includes important notes and pitfalls for implementation.

# Persistence

If you need to save player-specific data (like high scores, inventory, or settings) across sessions or instances, refer to `references/en/udon_persistence.md`. This document explains how to use PlayerData and PlayerObjects for persistent storage.