# Luau Reference

## Contents
- [Booleans](#booleans)
- [Luau comments](#luau-comments)
- [Control structures](#control-structures)
- [Enums](#enums)
- [Functions](#functions)
- [Luau](#luau)
- [Luau and C# comparison](#luau-and-c-comparison)
- [Metatables](#metatables)
- [Native code generation](#native-code-generation)
- [Nil](#nil)
- [Numbers](#numbers)
- [Operators](#operators)
- [Queues](#queues)
- [Scope](#scope)
- [Stacks](#stacks)
- [Strings](#strings)
- [Tables](#tables)
- [Tuples](#tuples)
- [Type checking](#type-checking)
- [Type coercion](#type-coercion)
- [Userdata](#userdata)
- [Variables](#variables)

---

## Booleans

The **boolean** data type, or `bool`, has a value of either `true` or `false`.

## Conditionals

If a value isn't `false` or `nil`, Luau evaluates it as `true` in [conditional statements](./control-structures.md#if-statements). Unlike many other languages, Luau considers both zero and the empty string as `true`.

## Operators

You can formulate complex conditions with [relational](./operators.md#relational) and [logical](./operators.md#logical) operators.

---

## Luau comments

A **comment** is text that the Luau parser ignores at runtime.

<Alert severity="info">
Roblox Studio has a similarly-named [comments](../projects/collaboration.md#studio-comments) feature that is unrelated to code comments in Luau.
</Alert>

## Single-line comments

You can define single-line comments with a double hyphen (`--`) anywhere outside a string. Single-line comments extend to the end of the line.

Use single line comments for in-line notes. If the comment spans multiple lines, use multiple single-line comments.

You can add and remove single-line comments in the Script Editor with the keyboard shortcut <kbd>Ctrl</kbd><kbd>/</kbd> (<kbd>⌘</kbd><kbd>/</kbd>).

```lua
-- This condition is really important because the world would blow up if it
-- were missing.
if not foo then
	stopWorldFromBlowingUp()
end
```

## Block comments

You can define multiline block comments with double hyphens and double brackets (`--[[]]`). Use block comments for documenting items:

- Use a block comment at the top of files to describe their purpose.
- Use a block comment before functions or objects to describe their intent.

```lua
--[[
    Shuts off the cosmic moon ray immediately.

    Should only be called within 15 minutes of midnight Mountain Standard
    Time, or the cosmic moon ray may be damaged.
]]
local function stopCosmicMoonRay()
end
```

If necessary, you can nest multiple brackets inside a block comment using the same number of equal signs in both the beginning and ending bracket:

```lua
--[=[
    In-depth detail about cosmic moon ray: [[[TOP SECRET]]]
]=]
```

## Comment directives

Luau uses comments that start with `!` to control features like [type checking](type-checking.md), [native code generation](native-code-gen.md), and [linting](https://luau.org/lint).

```lua
--!strict
--!nonstrict
--!nocheck
--!native
--!nolint
--!optimize 0|1|2
```

For linting, Roblox Studio enables the following subset of warning codes from the [Luau linter](https://luau.org/lint): 

[Content truncated - see full docs]

---

## Control structures

**Control structures** are statements that manage the flow of Luau code execution. There are four main types of control structures:

- An [if then else](#if-statements) statement executes code only if a specified condition is `true`. The code execution doesn't repeat.
- A [while loop](#while-loops) executes code only if a specified condition is `true`, and repeats execution while the condition remains `true`.
- A [repeat loop](#repeat-loops) executes code, and repeats execution if the condition is `true`.
- A [for loop](#for-loops) executes code a set number of times depending on specified inputs.

The condition for `if` statements, `while` loops, and `repeat` loops can be any Luau expression or value. If a value isn't `false` or `nil`, then Luau evaluates it as `true` in conditional statements. Unlike other scripting languages, Luau considers both zero and the empty string as `true`.

## If statements

The basic `if` statement tests its condition. If the condition is true, then Luau executes the code between `then` and `end`.

You can use an `elseif` statement to test for additional conditions if the `if` condition is false. You can use an `else` statement to execute code if all `if` and `elseif` conditions fail. The `elseif` and `else` parts are both optional, but you can't use either without an initial `if` statement.

In a chain of `if`, `elseif`, and `else` conditions, Luau tests conditions from top to bottom, stops at the first `true` condition, and executes the code that follows it.

```lua
if 2 + 2 == 5 then
	print("Two plus two is five") -- Doesn't print because the condition is false
elseif 2 + 3 == 5 then
	print("Two plus three is five") -- Two plus three is five
else
	print("All conditions failed") -- Doesn't print because the previous condition is true
end
```

## While loops

A `while`—`do` loop evaluates if a specified condition is true or false. If the condition is `false` or `nil`, then the loop ends, and Luau skips the code in the loop. If the cond

[Content truncated - see full docs]

---

## Enums

<Alert severity="info">
Enums are not a [built-in Luau type](https://luau.org/typecheck#builtin-types) and they exist only in Roblox, but they're conceptually similar to other Luau data types and are something you'll work with frequently in Roblox development.
</Alert>

The **enumeration** data type, or `Datatype.Enum`, is a fixed list of items. You can access enums through the global object called `Datatype.Enum`. For a full list and their respective items, see [Enums](/reference/engine/enums).

## Enum items

To get all items of an enum, call the `Datatype.Enum:GetEnumItems()|GetEnumItems()` method on it. The following code sample demonstrates how to call `Datatype.Enum:GetEnumItems()|GetEnumItems()` on the `Enum.PartType` enum.

```lua
local partTypes = Enum.PartType:GetEnumItems()

for index, enumItem in partTypes do
	print(enumItem)
end

--[[
	Enum.PartType.Ball
	Enum.PartType.Block
	Enum.PartType.Cylinder
	Enum.PartType.Wedge
	Enum.PartType.CornerWedge
]]
```

## Data type

The `Datatype.EnumItem` is the data type for items in enums. An `Datatype.EnumItem` has three properties:

- `Name` — The name of the `Datatype.EnumItem`.
- `Value` — The numerical index of the `Datatype.EnumItem`.
- `EnumType` — The parent `Datatype.Enum` of the `Datatype.EnumItem`.

Some properties of objects can only be items of certain enums. For example, the `Class.Part.Shape|Shape` property of a `Class.Part` object is an item of the `Enum.PartType` enum. The following code sample demonstrates how to print the properties of the `Enum.PartType.Cylinder` enum item.

```lua
print(Enum.PartType.Cylinder.Name) --> "Cylinder"
print(Enum.PartType.Cylinder.Value) --> 2
print(Enum.PartType.Cylinder.EnumType) --> PartType
```

To assign an `Datatype.EnumItem` as the value of a property, use the full `Datatype.Enum` declaration. You can also use the item's `Datatype.EnumItem.Name|Name` property as a string.

```lua
local Workspace = game:GetService("Workspace")

local part = Instance.new("Part") 

[Content truncated - see full docs]

---

## Functions

**Functions** are [blocks of code](./scope.md) that you can execute multiple times on command. You can also connect them to [events](#event-handlers) or assign them as [callbacks](#callbacks).

## Basic functions

A function definition includes:

- The [scope](./scope.md) of the function (global or `local`).
- The `function` keyword.
- The name of the function in `camelCase`.
- The parameters of the function in parentheses (`()`).
- The block of code, or "body", of the function.
- The `end` keyword.

The body of the function executes when you call the function. To call a function, type its name followed by parentheses. You can define a variable to accept the return value or use the return value in place of a variable.

```lua
-- This function has no parameters and returns nil
local function addOneAndTwo()
	local result = 1 + 2
	print(result)
end
-- Calling a function without a return
addOneAndTwo() -- 3
```

### Parameters

Parameters are variables that you make available to the function and are only used in the function's [scope](./scope.md). Functions have no parameters by default. If you call a function with more parameters than it expects, Luau ignores the extra parameters. If you call a function with fewer parameters than it expects, Luau passes `nil` for all missing parameters.

```lua
-- This function has two parameters: num1 and num2
local function addNumbers(num1, num2)
	print(num1 + num2)
end

addNumbers(2, 3) -- 5
addNumbers(5, 6, 7) -- 11
addNumbers(9) -- attempt to perform arithmetic (add) on number and nil
```

### Return

In the body of the function, the `return` keyword returns a result from a computation. You can return multiple values from one function. `return` ends function execution, and Luau expects the `end` keyword to follow the `return` statements, so writing code between the `return` command and the `end` command throws an error.

```lua
-- This function returns one return value
local function addNumbers(num1, num2)
	local result = num1 + n

[Content truncated - see full docs]

---

## Luau

[Luau](https://luau.org) is the scripting language creators use in Roblox Studio. It is a fast, small, safe, gradually typed embeddable scripting language derived from [Lua 5.1](https://www.lua.org/manual/5.1/).

<Alert severity="success">
Contributing your Luau scripts for AI training can help enhance Luau-focused AI tools in Studio. For more information, see [Empower Luau creation](https://create.roblox.com/data-collection).
</Alert>

## Support in Studio

The **Script Editor** in Studio supports Luau with autocompletion, syntax highlighting, static linting, type checking, and script analysis. It also shows documentation and function signatures for members of the [Roblox Engine API](/reference/engine).

## Types

Luau includes the following data types:

- [Nil](nil.md) represents non-existence or nothingness. It's different from any other value or data type.
- [Booleans](booleans.md), or `bool`, have a value of either `false` or `true`.
- [Numbers](numbers.md), or `double`, represent double-precision (64-bit) floating-point numbers.
- [Strings](strings.md) are sequences of characters, such as letters, numbers, and symbols.
- [Tables](tables.md) are [arrays](tables.md#arrays) or [dictionaries](tables.md#dictionaries) of any value except `nil`.
- [Enums](enums.md) are fixed lists of items.

Luau is dynamically typed by default. Variables, function parameters, and return values can be any data type. This helps you write code faster because you don't need to provide types for each piece of data. You can still declare explicit types for variables in Luau and enable [strict type checking](type-checking.md) to make type issues obvious and easy to locate.

## Data structures

You can also implement the following data structures using primitive data types:

- [Stacks](stacks.md) are Last-In-First-Out collections of items that you can implement using tables.
- [Queues](queues.md) are First-In-First-Out collections of items that you can implement using tables.
- [Metatables]

[Content truncated - see full docs]

---

## Luau and C# comparison

Roblox uses the Luau programming language. The following code samples and tables indicate some of the differences between syntaxes for C# and Luau.

## Line endings

You don't need semicolons in Luau, but they don't break the syntax.

## Reserved keywords

The following table has Luau's reserved keywords mapped to their C# equivalent. Note it doesn't show all C# keywords.

<table>
    <thead>
        <tr>
            <th>Luau</th>
            <th>C#</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>`and`</td>
            <td></td>
        </tr>
        <tr>
            <td>`break`</td>
            <td>`break`</td>
        </tr>
        <tr>
            <td>`do`</td>
            <td>`do`</td>
        </tr>
        <tr>
            <td>`if`</td>
            <td>`if`</td>
        </tr>
        <tr>
            <td>`else`</td>
            <td>`else`</td>
        </tr>
        <tr>
            <td>`elseif`</td>
            <td>`else if`</td>
        </tr>
        <tr>
            <td>`then`</td>
            <td></td>
        </tr>
        <tr>
            <td>`end`</td>
            <td></td>
        </tr>
        <tr>
            <td>`true`</td>
            <td>`true`</td>
        </tr>
        <tr>
            <td>`false`</td>
            <td>`false`</td>
        </tr>
        <tr>
            <td>`for`</td>
            <td>`for` or `foreach`</td>
        </tr>
        <tr>
            <td>`function`</td>
            <td></td>
        </tr>
        <tr>
            <td>`in`</td>
            <td>`in`</td>
        </tr>
        <tr>
            <td>`local`</td>
            <td></td>
        </tr>
        <tr>
            <td>`nil`</td>
            <td>`null`</td>
        </tr>
        <tr>
            <td>`not`</td>
            <td></td>
        </tr>
        <tr>
            <td>`or`</td>
            <td></td>
        </tr>
        <tr>
            <td>`repeat`</td>
            <td></td>
        </tr>
        <tr>
            <td>`return`</td>
    

[Content truncated - see full docs]

---

## Metatables

Metatables allow tables to become more powerful than before. They are attached to data and contain values called metamethods. Metamethods are fired when a certain action is used with the datum that it is attached to.

## Manipulate metatables

The two primary functions for adding and finding a table's metatable are `Global.LuaGlobals.setmetatable()` and `Global.LuaGlobals.getmetatable()`.

```lua
local x = {}
local metaTable = {} -- metaTables are tables, too!
setmetatable(x, metaTable) -- Give x a metatable called metaTable!
print(getmetatable(x)) --> table: [hexadecimal memory address]
```

The `Global.LuaGlobals.setmetatable()` function also returns the table that you're setting the metatable of, so these two scripts do the same thing:

```lua
local x = {}
setmetatable(x, {})
```

```lua
local x = setmetatable({}, {})
```

### Metamethods

Metamethods are the functions that are stored inside a metatable. They can go
from calling a table, to adding a table, to even dividing tables as well.
Here's the list of available metamethods:

<table>
  <thead>
	  <tr>
		  <th>Method</th>
		  <th>Description</th>
		</tr>
	</thead>
	<tbody>
	  <tr>
		  <td>`__index(table, index)`</td>
		  <td>Fires when `table[index]` is indexed, if `table[index]` is `nil`. Can also be set to a table, in which case that table will be indexed.</td>
		</tr>
	  <tr>
		  <td>`__newindex(table, index, value)`</td>
		  <td>Fires when `table[index]` tries to be set `(table[index] = value)`, if `table[index]` is `nil`. Can also be set to a table, in which case that table will be indexed.</td>
		</tr>
	  <tr>
		  <td>`__call(table, ...)`</td>
		  <td>Fires when the table is called like a function, `...` is the arguments that were passed.</td>
		</tr>
	  <tr>
		  <td>`__concat(table, value)`</td>
		  <td>Fires when the `..` concatenation operator is used on the table.</td>
		</tr>
	  <tr>
		  <td>`__unm(table)`</td>
		  <td>Fires when the unary `–` operator is used on the table.</td>
		</tr>
	  <tr>
		 

[Content truncated - see full docs]

---

## Native code generation

With Luau support for native code generation, server-side scripts in your experience can be compiled directly into the machine code instructions that CPUs execute, rather than regular bytecode that the Luau VM operates on. This feature can be used to improve execution speed for some scripts on the server, in particular those that have a lot of numerical computation without using too many heavy Luau library or Roblox API calls.

<iframe width="880" height="495" src="https://www.youtube-nocookie.com/embed/llR_pNlJDQw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Enable native code generation

To enable native code generation for a `Class.Script`, add the <Typography noWrap>`--!native`</Typography> comment at the top:&sup1;

```lua highlight="1"
--!native

print("Hello from native code!")
```

This enables native code generation for all functions in the script, and the top-level scope, if deemed profitable. No additional changes are required; behavior of the natively executing scripts is exactly the same as before and only the performance is different. All features of the Luau language and all Roblox APIs remain supported.

Alternatively, you can enable native code generation for an individual function by adding the `@native` attribute:

```lua highlight="1"
@native
local function f(x)
  return (x + 1)
end
```

<figcaption><sup>1</sup> In the future, some scripts might automatically start running natively if it is determined to be profitable, but manually placed `--!native` comments are currently required.</figcaption>

## Best practices

The following tips will help you benefit most from native code generation:

- It's best to enable this feature inside scripts that perform a lot of computation directly inside Luau. If you have a lot of mathematical operations on tables and especially `Library.buffer` types, the script may be a good

[Content truncated - see full docs]

---

## Nil

In Luau, `nil` represents non-existence or nothingness. It's different from any other value or data type. You can use it to destroy a variable or remove a value in a table. It's the only value other than `false` which doesn't evaluate to [`true`](./booleans.md).

Luau has a **garbage collector** that removes data that is no longer accessible by any script. For best performance, redefine large variables as `nil` in long-running scripts when you don't need them anymore so the garbage collector removes them.

```lua
local variableToDelete = 5
print(variableToDelete) -- 5
variableToDelete = nil
print(variableToDelete) -- nil

local dictionaryTable = {
	Monday = 1,
	Tuesday = 2,
	Wednesday = 3
}
-- Output value of 'Tuesday' key
print(dictionaryTable.Tuesday) -- 2
-- Clear 'Tuesday' key
dictionaryTable.Tuesday = nil
-- Output value of key again
print(dictionaryTable.Tuesday) -- nil
```

You can use `nil` to clear some properties of objects. For example, you can set the `Parent` of an object to `nil` to effectively remove the object from the experience. To return the object to the experience after you remove it, reassign the `Parent`. The following example demonstrates how to use `nil` to remove a `Class.Part`:

```lua
local Workspace = game:GetService("Workspace")

-- Create a new brick
local part = Instance.new("Part")
-- Parent new part to the workspace, making it viewable
part.Parent = Workspace
task.wait(1)
-- Remove the part from view but not from memory
part.Parent = nil
task.wait(1)
-- Part still exists because it's referenced by the variable "part", so it can be returned to view
part.Parent = Workspace
task.wait(1)
-- Remove the part from view again
part.Parent = nil
-- Clear part reference so it gets picked up by the garbage collector
part = nil
```

---

## Numbers

The **number** data type, or `double`, represents a [double-precision (64-bit) floating-point](https://wikipedia.org/wiki/Double-precision_floating-point_format) number. Numbers can range from -1.7 \* 10<sup>308</sup> to 1.7 \* 10<sup>308</sup> (around 15 digits of precision, positive or negative).

## Signed and unsigned

The sign of the number indicates whether it's positive or negative. For example, `1` is positive and `-1` is negative. In Luau, the number `-0` is equivalent to `0`.

```lua
print(0 == -0)  --> true
print(-0 > 1)  --> false
print(-0 < 1)  --> true
print(-0 > -1)  --> true
print(-0 < -1)  --> false
```

## Number classifications

Luau doesn't distinguish between integers and numbers, but the API reference sometimes distinguishes between them to be more specific about how to use each API.

### float

The `float` number type refers to a real number with a decimal place. In computer science terms, they are [single-precision (32-bit) floating-point number](https://wikipedia.org/wiki/Single-precision_floating-point_format), which isn't as precise as double-precision floating-point numbers, but is sufficiently precise for most use cases and requires less memory and storage.

### int

The `integer` number type, or `int`, refers to a 32-bit whole number, which ranges from -2<sup>31</sup> to 2<sup>31</sup> - 1. Properties and functions that expect integers may automatically round or raise errors when you assign or pass non-integers to them.

### int64

The `int64` number type refers to a signed 64-bit integer, which ranges from -2<sup>63</sup> to 2<sup>63</sup> - 1. This type of integer is common for methods that use ID numbers from the Roblox website. For example, `Class.Player.UserId` is an `int64`, and `Class.MarketplaceService:PromptPurchase()` and `Class.TeleportService:Teleport()` each expect `int64` for the ID arguments.

## Notation

Numbers are notated with the most significant digits first (big-endian). There are multiple ways to notate number lit

[Content truncated - see full docs]

---

## Operators

An **operator** is a symbol for performing an operation or conditional evaluation.

## Logical

Logical operators return values depending on the boolean values of the given arguments. If an argument isn't `false` or `nil`, then the operator evaluates it as `true`. Unlike many other languages, Luau considers both zero and the empty string as `true`. The following table summarizes how logical operators behave in [conditionals](./control-structures.md#if-statements).

<table>
  <thead>
    <tr>
      <th>Operator</th>
      <th>Descriptions</th>
    </tr>
  </thead>
  <tr>
    <td>`and`</td>
    <td>Evaluates as `true` only if both conditions are true</td>
  </tr>
  <tr>
    <td>`or`</td>
    <td>Evaluates as `true` if either condition is true</td>
  </tr>
  <tr>
    <td>`not`</td>
    <td>Evaluates as the opposite of the condition</td>
  </tr>
</table>

### and

The binary operator `and` returns one of the two arguments. If the first argument evaluates to `true`, then it returns the second argument. Otherwise, it returns the first argument.

```lua
print(4 and 5) -- 5
print(nil and 12) -- nil
print(false and 12) -- false
print(false and true) -- false
print(false and false) -- false
print(true and false) -- false
print(true and true) -- true
```

You can use `and` to test multiple conditions in [control structures](./control-structures.md) such as [`if` statements](./control-structures.md#if-statements) and [`while` loops](./control-structures.md#while-loops). For example, the following `if`‑`then` statement tests that two conditions are both true:

```lua
local pasta = true
local tomatoSauce = true

if pasta == true and tomatoSauce == true then
	print("We have spaghetti dinner")
else
	print("Something is missing...")
end
-- Output: We have spaghetti dinner
```

### or

The binary operator `or` returns one of the two arguments. If the first argument evaluates to `true`, then it returns the first argument. Otherwise, it returns the second argument.

```lua
local y = x 

[Content truncated - see full docs]

---

## Queues

A queue is a linear data structure with a collection of items. There are two types of queues on Roblox: [regular queues](#regular-queues), which follow the first-in-first-out (FIFO) principle, and [priority queues](#priority-queues), which have priorities for items in the queue that determine the data accessing order. Items in both types of queues can be any Luau [data type](../luau/index.md#types).

Queue is a built-in data structure of the [non-persistent data storage](../cloud-services/memory-stores/queue.md) service named `Class.MemoryStoreService`, for which you can directly call the built-in functions to get a queue and add, read, or remove data from the queue. For any other usage, such as scheduling tasks and handling requests in your experience, you can use tables to implement queues on your own.

## Regular queues

Regular queues are maintained in the FIFO sequence, in which all items are added to the back of the queue and read or removed in the same order as they are added, from the front to the end.

<figure>
  <img src="../assets/data/memory-store/Regular-Queue-Diagram.png" width="80%" />
  <figcaption>The order of how a regular queue adds, reads, and removes items</figcaption>
</figure>

## Priority queues

Priority queues are not following the FIFO rule, in which each item can be added with a priority number that indicates its order being read or removed. The item at the back of a priority queue has the default priority of 0, and the item at the front of the queue has the highest set priority, which is 5 in the following example.

<figure>
  <img src="../assets/data/memory-store/Priority-Queue-Diagram.png" width="80%" />
  <figcaption>An item's set priority changes the order in which a queue reads items</figcaption>
</figure>

For this example, an item with a set priority of 3 is being added to a queue. The queue places the new item behind all existing items with the set priority of 3 or more. To place an item at the front of the queue, you need to set

[Content truncated - see full docs]

---

## Scope

In scripting, a block of code is the body of a [control structure](./control-structures.md) or [function](./functions.md). The **scope** of a variable or function is the block of code that can access it, and it can be **global** or **local**. All blocks can access global variables and functions. A block can access local variables and functions in its parent block, but not in any of its child blocks.

Variables and functions have global scope by default, but it's almost always better to declare them with local scope because Luau accesses local variables and functions faster than global ones. To give a variable or function local scope, put the keyword `local` before its name when you declare it.

Scripts cannot access global and local variables or functions in other scripts. If you want to share values and functions between scripts, use `Class.ModuleScript|ModuleScripts`.

```lua
local helloWorld = 'Hello World!'
local function printHelloWorld()
	print(helloWorld)
end
printHelloWorld() -- Hello World!
```

<img src="../assets/scripting/scripts/Scope-Diagram.png" width="500" />

- Block B **can** access the local variable in block A.
- Block C **can** access the local variables and functions in blocks A and B.
- Block A **cannot** access the local variables and functions in blocks B or C.
- Block B **cannot** access the local variable in block C.

## Global scope

After you declare a global variable or function, any block of code in the same [script](../scripting/index.md) can access it. Variables and functions have global scope unless you declare them with the `local` keyword.

In the following code, `testVar` has global scope within the local `testFunc()` function. When Luau calls the `testFunc()`, it assigns `testVar` the value `64`. The `testVar` has global scope, so the `print()` function outside `testFunc()` can access it and print `64`.

```lua title = 'Example of global functions and variables'
local function testFunc()  -- local scope
	testVar = 64  -- global 

[Content truncated - see full docs]

---

## Stacks

A stack is a linear data structure with a collection of items that follows the Last-In-First-Out (LIFO) principle. The top of the stack is the item most recently added to the stack, and the bottom of the stack is the item that was least recently added.

You can think of the stack data structure as a stack of dinner plates: you start with one, and then you put another above it. When you take plates from the stack, the **first** one you remove from the stack is the **last** one you put on the top.

Stacks have two main operations: **push** for adding an element to the top of the stack and **pop** for removing the element from the top of the stack. A Stack can either have a fixed size or be dynamically resized. Stacks are helpful for design usage such as backtracking algorithms.

## Implement stacks

Though Luau doesn't have stacks as a built-in data structure, you can use [tables](../luau/tables.md) to implement stacks. The following code sample shows how to create a stack, `push` an object to a stack, and `pop` an object from the stack. To use this implementation for your experience, you should save it as a `Class.ModuleScript` and store it in `Class.ReplicatedStorage`, so your stack is accessible for both client and server.

```lua Implement a Stack Using Table
local Stack = {}
Stack.__index = Stack

function Stack.new()
	local self = setmetatable({}, Stack)

	self._stack = {}

	return self
end

-- Check if the stack is empty
function Stack:isEmpty()
	return #self._stack == 0
end

-- Put a new value onto the stack
function Stack:push(value)
	table.insert(self._stack, value)
end

-- Take a value off the stack
function Stack:pop()
	if self:isEmpty() then
		return nil
	end

	return table.remove(self._stack, #self._stack)
end

return Stack
```

The following code sample is a usage example as a `Class.Script` under `Class.Workspace`. You can modify the code, type, and storage location to fit your own usage, as long as you have the previous implementation code sample prop

[Content truncated - see full docs]

---

## Strings

The **string** data type is a sequence of characters, such as letters, numbers, and symbols. It's the data type for storing most text-based information.

## Declare strings

To declare a string variable, put quotes around the characters. It's more common to use double quotes (`"`), but single quotes (`'`) also work. If you want to include a single or double quote in your string, wrap your string around the other type of quote, or use an [escaped quote](#escape-strings).

```lua
local string1 = "Hello world!"
print(string1)  --> Hello world!

local string2 = 'Hello "world"!'
print(string2)  --> Hello "world"!
```

To include both single and double quotes in a string, or to create multi-line strings, declare them using double brackets:

```lua
local string1 = [[Hello
world!
Hello "world"!
Hello 'world'!]]

print(string1)
--> Hello
--> world!
--> Hello "world"!
--> Hello 'world'!
```

If necessary, you can nest multiple brackets inside a string using the same number of equal signs in both the beginning and ending bracket:

```lua
local string1 = [=[Hello
[[world!]]
]=]

print(string1)
--> Hello
--> [[world!]]
```

## Combine strings

To combine strings, **concatenate** them with two dots (`..`). Concatenating strings doesn't insert a space between them, so you'll need to include space(s) at the end/beginning of a preceding/subsequent string, or concatenate a space between the two strings.

```lua
local hello = "Hello"
local helloWithSpace = "Hello "
local world = "world!"

local string1 = hello .. world
local string2 = helloWithSpace .. world
local string3 = hello .. " " .. world

print(string1)  --> Helloworld!
print(string2)  --> Hello world!
print(string3)  --> Hello world!
```

Note that the `print()` command takes multiple arguments and combines them **with** spaces, so you can use `,` instead of `..` to yield spaces in `print()` outputs.

```lua
local hello = "Hello"
local world = "world"
local exclamationMark = "!"

print(hello .. world .. exclamationMark)  --> 

[Content truncated - see full docs]

---

## Tables

The **table** data type can store multiple values of any type that isn't `nil`, including [booleans](./booleans.md), [numbers](./numbers.md), [strings](./strings.md), [functions](./functions.md), and other tables. Construct tables with curly braces (`{}`):

```lua
-- Construct an empty table assigned to variable "t"
local t = {}
print(t) -- {}
```

You can use a table as an [array](#arrays) or [dictionary](#dictionaries). Arrays use an ordered list of numbers as indices, but dictionaries can have numbers, strings, and objects as indices.

For more information on built-in functions for working with tables, see the `Library.table` library.

## Arrays

An **array** is an ordered list of values. Arrays are useful for storing collections of data, such as a group of players with special permissions.

### Create arrays

To create an array using a Luau table, declare the values in sequential order, separated by commas.

```lua
-- Construct an array with three items
local testArray = {"A string", 3.14159, true}
print(testArray)
```

### Read from arrays

To read from an array, add a pair of square brackets after its reference and specify the index number of the element inside (`[pos]`):

```lua
-- Construct an array with three items
local testArray = {"A string", 3.14159, true}

print(testArray[1]) -- A string
print(testArray[2]) -- 3.14159
print(testArray[3]) -- true
```

<Alert severity="warning">
Unlike some languages, Luau uses 1-based indexing for arrays, so the first item in the array is `[1]`, not `[0]`.
</Alert>

### Write to arrays

To define or rewrite the value of an array at an index, declare the index number in square brackets (`[index]`) followed by `=` and the value:

```lua
local testArray = {"A string", 3.14159, true}

testArray[2] = 12345
testArray[4] = "New string"

print(testArray[2]) --12345
print(testArray[4]) -- New string
```

### Iterate over arrays

To iterate over an array, you can use a `for` loop. Because the arrays have numerical indices, you ca

[Content truncated - see full docs]

---

## Tuples

A **tuple** is a list of values. Many [methods](./functions.md#methods) and [callbacks](./functions.md#callbacks) in the [Roblox Engine API](/reference/engine) accept and return multiple values, but the API Reference says "Tuple" instead of those values.

## Parameters

If a [method](./functions.md#methods) or [callback](./functions.md#callbacks) accepts a tuple as a parameter, then it accepts multiple values. For example, the API Reference shows that the `Class.BindableFunction:Invoke()` method accepts a "Tuple" as a parameter, so it accepts multiple arguments.

```lua
BindableFunction:Invoke(1, true, "string", Vector3.new(0, 0, 0))
```

## Returns

If a [method](./functions.md#methods) or [callback](./functions.md#callbacks) returns a tuple, then it returns multiple values. For example, the API Reference shows that the `Class.Players:GetUserThumbnailAsync()` method returns a "Tuple", so it returns multiple values. The first return value is a Content URL, and the second is a [boolean](./booleans.md).

```lua
local Players = game:GetService("Players")

local userId = 156 -- builderman
local thumbType = Enum.ThumbnailType.HeadShot
local thumbSize = Enum.ThumbnailSize.Size420x420
local content, isReady = Players:GetUserThumbnailAsync(userId, thumbType, thumbSize)
print(content, isReady) -- rbxthumb://type=AvatarHeadShot&id=156&w=420&h=420 true
```

---

## Type checking

<Alert severity="info">
For the latest and most complete type checking documentation, see [here](https://luau.org/typecheck).
</Alert>

Luau supports a gradual type system through the use of type annotations and type inference. These types are used to provide better warnings, errors, and suggestions in the [Script Editor](../studio/script-editor.md).

## Define a type

Use the `type` keyword to define your own types:

```lua
type Vector2 = {x: number, y: number}
```

## Inference modes

There are three Luau type inference modes that can be set on the first line of a `Class.Script`:

- `--!nocheck` — Don't check types.
- `--!nonstrict` — Only asserts variable types if they are explicitly annotated.
- `--!strict` — Asserts all types based off the inferred or explicitly annotated type.

The `--!nonstrict` and `--!strict` modes control how strict the type checker is with inferring and checking types for variables and functions. Any type mismatches in scripts are highlighted in the [Script Editor](../studio/script-editor.md) and surfaced as warnings in the [Script Analysis](../studio/script-editor.md#script-analysis) window.

To set a default mode for all scripts that you can override as needed, see `Class.Workspace.LuauTypeCheckMode`.

## Types

A type annotation can be defined using the `:` operator after a local variable, followed by a type definition. By default, in `nonstrict` mode, all variables are assigned the type `any`.

```lua
local foo: string = "bar"
local x: number = 5
```

There are four primitive types that can be used in an annotation:

- `nil` - no value
- `boolean` - `true` or `false`
- `number` - a numeric value
- `string` - text

Within Roblox, all classes, data types, and enums have their own types that you can check against:

```lua
local somePart: Part = Instance.new("Part")
local brickColor: BrickColor = somePart.BrickColor
local material: Enum.Material = somePart.Material
```

To make a type optional, use a `?` at the end of the annotation:

```

[Content truncated - see full docs]

---

## Type coercion

If Luau tries to use a value or [variable](./variables.md) in an operation, such as [arithmetic](#arithmetic), [concatenation](#concatenation), or [assignment](#assignment), but the value isn't the type that the operation expects, then Luau converts (**coerces**) the value to change its data type. Coercion happens at run time for that operation and doesn't change the value of a variable.

## Arithmetic

Luau coerces strings to numbers in [arithmetic operations](./operators.md#arithmetic). This behavior is built into Luau. If the types are incompatible for arithmetic, Luau throws an error and doesn't run the rest of the script. For example, you can't add a string to a number if the string does not represent a number.

```lua
print(100 + "7") -- 107
print(100 - "7") -- 93
print("1000" + 234) -- 1234
print("1000" - 234) -- 766
print("hello" + 234) -- error: attempt to perform arithmetic (add) string and number
```

## Concatenation

In concatenation, Luau coerces numbers to strings. To convert a number to a string without using coercion, use the `Library.string.format()` function.

```lua
print("Pi is " .. math.pi) --> Pi is 3.1415926535898
print("Pi is " .. 3.1415927) --> Pi is 3.1415927

-- Rounds to three decimal places
print("Pi is " .. string.format("%.3f", 3.1415927)) -- Pi is 3.142
```

## Assignment

Some properties expect certain data types, such as an [Enum](#enums) or string, but you can assign a value of a different type to it and Luau converts the value to the type the property expects.

### Enums

Luau coerces numbers and strings of enum values into the full enum name. For example, you can name the value of the `Class.Part.Material` property using a number, string, or full enum name, and the `print()` function always prints the full enum name. It's best practice to be explicit and use the full enum name. For more information on Enums, see [Enums](./enums.md).

```lua
local Workspace = game:GetService("Workspace")

local part1 = Instance.new("Part")
part1.

[Content truncated - see full docs]

---

## Userdata

Userdata is one of the basic types in Luau. Userdata represents arbitrary C/C++ data that exists in Luau. See [Userdata](https://www.lua.org/pil/28.1.html) for more information.

---

## Variables

A **variable** is a name that holds a value. Variable values can be [numbers](./numbers.md), [strings](./strings.md), [booleans](./booleans.md), [data types](/reference/engine/datatypes), and more.

## Name variables

Variable names can be any non-reserved string of letters, digits, and underscores that don't start with a digit.

```lua
LETTERS   -- valid
a1        -- valid
var_name  -- valid
_test     -- valid

if        -- NOT valid
25th      -- NOT valid
```

Variable names are **case-sensitive**, so `TestVar` and `TESTVAR` are different names. Avoid naming variables with an underscore and all uppercase letters, such as `_VERSION`, because Luau may reserve them for internal global variables.

### Best practices

It's best practice to spell out words fully. Abbreviations generally make code easier to write, but harder to read. Following common naming practices when naming your variables can help you and others understand their meaning or purpose:

- Use `PascalCase` names for class and enum-like objects.
- Use `PascalCase` names for all Roblox APIs. `camelCase` APIs are mostly deprecated.
- Use `camelCase` names for local variables, member values, and [functions](./functions.md).
- Use `LOUD_SNAKE_CASE` names for local constants (variables with values that you don't expect to [change](#change-values)).
- Don't capitalize entire acronyms within names. For example, write `aJsonVariable` or `MakeHttpCall`.

### Reserved names

Luau reserves the following keywords, so you can't use them to name variables or [functions](./functions.md):

- `and`
- `for`
- `or`
- `break`
- `function`
- `repeat`
- `do`
- `if`
- `return`
- `else`
- `in`
- `then`
- `elseif`
- `local`
- `true`
- `end`
- `nil`
- `until`
- `false`
- `not`
- `while`

## Assign values

To create a variable and assign a value to it, use the `=` operator. Put the variable on the left of the `=` and the value on the right. If you don't put a value, the value is `nil`.

Variables can have **global** or **local** [s

[Content truncated - see full docs]

---

