# Scripting Reference

## Contents
- [Properties and attributes](#properties-and-attributes)
- [Script capabilities](#script-capabilities)
- [Debounce patterns](#debounce-patterns)
- [Bindable events and callbacks](#bindable-events-and-callbacks)
- [Deferred engine events](#deferred-engine-events)
- [Events](#events)
- [Remote events and callbacks](#remote-events-and-callbacks)
- [Scripting](#scripting)
- [Script types and locations](#script-types-and-locations)
- [Reuse code](#reuse-code)
- [Parallel Luau](#parallel-luau)
- [Schedule code](#schedule-code)
- [Scripts](#scripts)
- [Security and cheat mitigation tactics](#security-and-cheat-mitigation-tactics)
- [Services](#services)

---

## Properties and attributes

Making experiences interactive often means manipulating object properties and attributes:

- Properties are part of the object class. For example, the `Class.BasePart.Anchored` property controls physics for the part. In a track and field experience, you might want to anchor a discus or javelin the instant it lands so that players have a visual indicator of how far it traveled.

- Attributes are essentially custom properties that you define. For example, the [Plant](../resources/plant-reference-project.md) reference project uses attributes to set the purchase price for seeds and the maximum plant size that a pot can hold.

## Replication order

Before you begin retrieving and manipulating objects, you must have an understanding of replication order.

The Roblox Engine doesn't guarantee the order in which objects are replicated from the server to the client, which makes the `Class.Instance:WaitForChild()` method essential for accessing objects in client scripts, particularly objects in the `Class.Workspace`. Still, some aspects of the process are predictable:

1. The client loads the contents of `Class.ReplicatedFirst`, such as a loading screen, assets, and scripts.
1. `Class.LocalScript|LocalScripts` (and `Class.Script|Scripts` with a `Class.Script.RunContext|RunContext` of `Enum.RunContext.Client|Client`) in `ReplicatedFirst` run. These scripts can safely get objects from `ReplicatedFirst` without using `WaitForChild()`:

   ```lua
   -- Safe
   local ReplicatedFirst = game:GetService("ReplicatedFirst")
   local LoadingScreen = require(ReplicatedFirst.LoadingScreen)
   ```

   These scripts **can't** safely get objects from other [services](services.md), because they might not have loaded yet:

   ```lua
   -- Not safe
   local ReplicatedStorage = game:GetService("ReplicatedStorage")
   local PickupManager = require(ReplicatedStorage.PickupManager)
   ```

   You **can** use `WaitForChild()` in these scripts to get objects from other services, but doing so negates t

[Content truncated - see full docs]

---

## Script capabilities

<Alert severity="success">
This page describes a feature that is still experimental and is available as a client beta. Features described here might undergo additional changes based on developer feedback and/or bug fixes.
</Alert>

**Script capabilities** is a system that offers control over actions that scripts can perform inside the `Class.DataModel` subtree. It provides better control over experience scripts rather than being an "all or nothing" system where any script can do anything that other scripts can.

- This system lets you limit what models taken from the toolbox can do and makes it easier to include user-generated content inside the experience, even those that contain scripts.
- It can also help ensure better security of experiences that allow players to run their own code, which is often executed in a restricted or emulated environment.
- It can also be used to share libraries that restrict what they can do themselves. For example, a library providing additional math methods can be restricted to the smallest set of capabilities it needs so that other developers using that library don't have to validate the entire codebase to make sure it doesn't include malicious code.

## Enable script capabilities

To enable this feature, change the `Class.Workspace.SandboxedInstanceMode|SandboxedInstanceMode` setting from `Default` to `Experimental` in the **Explorer**.

When the client beta test is completed, this step will no longer be required.

## Sandboxed container

This system introduces a concept of a **sandboxed container**.
An instance of type `Class.Model`, `Class.Folder`, `Class.Script`, or descendants of any of those classes have a `Class.Instance.Sandboxed|Sandboxed` property available in the Studio **Properties** window, under the **Permissions** section.

<img src="../assets/studio/properties/Folder-Sandboxed.png" width="320" alt="Sandboxed property of a Folder in the Properties window." />

Enabling the `Class.Instance.Sandboxed|Sandboxed` property 

[Content truncated - see full docs]

---

## Debounce patterns

A **debounce** pattern is a coding technique that prevents a function from running too many times or an input from triggering multiple times. The following scripting scenarios illustrate debounce as a best practice.

## Detect collisions

Suppose you want to create a hazardous trap part that inflicts 10 damage when touched. An initial implementation might use a basic `Class.BasePart.Touched` connection and a `damagePlayer` function like this:

```lua title="Script - Damage Player"
local part = script.Parent

local function damagePlayer(otherPart)
	print(part.Name .. " collided with " .. otherPart.Name)

	local humanoid = otherPart.Parent:FindFirstChildWhichIsA("Humanoid")
	if humanoid then
		humanoid.Health -= 10  -- Reduce player health
	end
end

part.Touched:Connect(damagePlayer)
```

While logical at first glance, testing will show that the `Class.BasePart.Touched|Touched` event fires multiple times in quick succession based on subtle physical collisions.

<img src="../assets/scripting/scripts/Touched-Event-No-Debounce.png" width="780" />

To avoid causing excessive damage on initial contact, you can add a debounce system which enforces a cooldown period on damage through an [instance attribute](../studio/properties.md#instance-attributes).

```lua title="Script - Damage Player Using Debounce" highlight="10, 11, 13, 14"
local part = script.Parent

local RESET_TIME = 1

local function damagePlayer(otherPart)
	print(part.Name .. " collided with " .. otherPart.Name)

	local humanoid = otherPart.Parent:FindFirstChildWhichIsA("Humanoid")
	if humanoid then
		if not part:GetAttribute("Touched") then
			part:SetAttribute("Touched", true)  -- Set attribute to true
			humanoid.Health -= 10  -- Reduce player health
			task.wait(RESET_TIME)  -- Wait for reset duration
			part:SetAttribute("Touched", false)  -- Reset attribute
		end
	end
end

part.Touched:Connect(damagePlayer)
```

## Trigger sounds

Debounce is also useful when working with sound effects, such as playing a s

[Content truncated - see full docs]

---

## Bindable events and callbacks

`Class.BindableEvent` and `Class.BindableFunction` objects let you bind behaviors between scripts **on the same side** of the [client-server](../../projects/client-server.md) boundary and communicate a specific desired outcome for in-experience actions.

The most common use case for bindable events is for experiences that have a round-based structure. For example, you might have a "match started" event that lets other scripts start a timer and display a leaderboard, with a corresponding "match ended" event that lets other scripts know when to move players back into a lobby and display the winners.

Because they coordinate activities between scripts, bindable events are typically used on the server, but you can use them on the client, too.

Depending on how your experience works, bindable events can help make your code more modular, but [module scripts](../module.md) are often a better alternative for situations in which you need to share data between scripts. You can also use bindable events in conjunction with module scripts for a cleaner syntax, as noted in [Custom events](../module.md#custom-events).

<Alert severity="info">
To communicate between scripts **across** the client-server boundary, see [Remote events](remote.md).
</Alert>

## Bindable events

The `Class.BindableEvent` object enables custom events through asynchronous, one-way communication between scripts.

When you fire a `Class.BindableEvent` through the `Class.BindableEvent:Fire()|Fire()` method, the firing script does **not** yield, and the target function receives the passed arguments with certain [limitations](#argument-limitations). Like all events, `Class.BindableEvent|BindableEvents` create threads of each connected function, so even if one errors, others continue.

To create a new `Class.BindableEvent` using the [Explorer](../../studio/explorer.md) window in Studio:

1. Hover over the container into which you want to insert the `Class.BindableEvent`. We recommend using `Class.ServerScriptSer

[Content truncated - see full docs]

---

## Deferred engine events

The `Class.Workspace.SignalBehavior` property controls whether event handlers are fired immediately or deferred. The `Enum.SignalBehavior.Deferred` option is recommended which helps improve the performance and correctness of the engine. The event handlers for **deferred events** are resumed at the next [resumption point](#resumption-points), along with any newly triggered event handlers.

<Alert severity="info">
The `Enum.SignalBehavior.Default` value of `Class.Workspace.SignalBehavior` is currently equivalent to `Enum.SignalBehavior.Immediate`, but will eventually switch to being equivalent to `Enum.SignalBehavior.Deferred`. Template places are directly set to `Enum.SignalBehavior.Deferred` by default.
</Alert>

The following diagram compares the `Enum.SignalBehavior.Immediate|Immediate` event behavior and the `Enum.SignalBehavior.Deferred|Deferred` event behavior.

- With the `Immediate` behavior, if an event triggers another event, the second event handler fires immediately.
- With the `Deferred` behavior, the second event is added to the back of a queue and run later.

The total time taken does not change, but the ordering is different.

<img alt="A comparison of three event handlers firing with Immediate and Deferred behavior" src="../../assets/scripting/scripts/ImmediateVsDeferredEvents.png" width="100%" />

"Re-entrancy" prevents events from continuously firing one another when they reach a certain depth. The current limit for this is 10.

## Deferred event benefits

The `Immediate` behavior has some disadvantages. For every instance added to your game, property that changes, or some other trigger that is invoked, the engine needs to run Luau code before anything else happens.

- To change 1,000 properties, 1,000 snippets of code potentially need to run after each change.
- Strange, hard-to-diagnose bugs can occur, such as a removing event firing before something was even added.
- Performance-critical systems can fire events requiring them to yield back and f

[Content truncated - see full docs]

---

## Events

Events are occurrences within your experience that you can listen for and respond to. Many Roblox services and objects have built-in events that automatically **fire** in response to specific actions or changes.

For example, a player's `Class.Player.Character|Character` touching a `Class.BasePart` automatically fires a `Class.BasePart.Touched|Touched` event. Each time a player joins your experience, the `Class.Players.PlayerAdded` event fires.

Due to the sheer number of events and client-server architecture, Roblox scripting is often referred to as **event-driven**. This approach is different from many other game engines, which emphasize running code on a frame-by-frame basis.

You don't have to listen for events or take any action in response to them, but the events are firing and available nevertheless. When you do want to respond to an event, you connect a function to it.

<Alert severity="info">
Deferred events can help you ensure more performant and consistent event handling. See [here](deferred.md) for more information.
</Alert>

## Connect functions to events

You connect a function to an event using `Datatype.RBXScriptSignal.Connect()|Connect()` to execute code each time the event fires. Most events pass arguments to their connected functions. For example, the `Class.BasePart.Touched` event passes the object that touched the part (such as a left hand or car wheel), and the `Class.Players.PlayerAdded` event passes the `Class.Player` that joined your experience.

The following code sample demonstrates how to connect a function named `onPartTouched()` to the `Class.BasePart.Touched|Touched` event of a part:

```lua
-- Assumes the script is parented to the part
local part = script.Parent

-- The function you want to run
local function onPartTouched(object)
	print("Part was touched by", object:GetFullName())
end

-- Connect the function to the part's Touched event
part.Touched:Connect(onPartTouched)
```

<Alert severity="success">
As a best practice and for opt

[Content truncated - see full docs]

---

## Remote events and callbacks

Roblox experiences are multiplayer by default, so all experiences inherently communicate between the server and the players' connected clients. In the simplest case, as players move their characters, certain `Class.Humanoid` properties, such as states, are communicated to the server, which passes this information to other connected clients.

Remote events and callbacks let you communicate **across** the client-server boundary:

- `Class.RemoteEvent|RemoteEvents` enable one-way communication (sending a request and **not** yielding for a response).
- `Class.UnreliableRemoteEvent|UnreliableRemoteEvents` enable one-way communication for data that changes continuously or isn't critical to game state. These events trade ordering and reliability for improved network performance.
- `Class.RemoteFunction|RemoteFunctions` enable two-way communication (sending a request and yielding until a response is received from the recipient).

Unlike [bindable events](bindable.md), which have more limited utility, the use cases for remote events and functions are too numerous to list:

- **Gameplay** - Basic gameplay, such as a player reaching the end of a level, can require a remote event. A client script notifies the server, and server scripts reset the player's position.
- **Server verification** - If a player tries to drink a potion, do they actually _have_ that potion? To ensure fairness, the server has to be the source of truth for an experience. A client script can use a remote event to notify the server that the player is drinking a potion, and then server scripts can decide whether the player actually has that potion and whether to confer any benefits.
- **User interface updates** - As the game state changes, server scripts can use remote events to notify clients of changes to scores, objectives, etc.
- **In-experience Marketplace purchases** - For an example implementation that uses remote functions, see [Prompt subscription purchases](../../production/monetization/subscription

[Content truncated - see full docs]

---

## Scripting

Scripts are plain text files that let you add custom, dynamic behavior to your experiences. You can use scripts to trigger in-game events, respond to player input, save player data, create leaderboards, spawn enemies, control NPC behavior, and much, much more.

<Alert severity="success">
This section is for creators with some coding experience who want to know the specifics of scripting in Roblox.

If you've never written code before and want an introduction to programming, see [Coding fundamentals](../tutorials/fundamentals/coding-1/coding-fundamentals.md), which covers concepts like variables, functions, conditionals, loops, and arrays. For a more guided, step-by-step approach, see the [Basic gameplay](../tutorials/use-case-tutorials/scripting/basic-scripting/intro-to-scripting.md) tutorial.
</Alert>

## Luau

Roblox scripts use the [Luau](https://luau.org) programming language, which is derived from [Lua 5.1](https://www.lua.org/manual/5.1/).

- Compared to Lua 5.1, Luau adds performance enhancements and many useful features, including an optional typing system, string interpolation, and generalized iteration for tables.
- All valid Lua 5.1 code is valid Luau code, but the opposite is not true.

Most books and online resources for Lua are still broadly applicable to Luau. For a detailed summary of differences, see [Compatibility](https://luau.org/compatibility) in the Luau documentation. For language syntax, see the [Luau reference](../luau/index.md).

### Luau basics

Luau is gradually typed, so you don't need to specify a type when you create a variable. You can use `Global.LuaGlobals.type()` to check object type:

```lua
logMessage = "User has more than 10 items!"
print(logMessage) --> User has more than 10 items!
print(type(logMessage)) --> string
```

Luau has global and local [scopes](../luau/scope.md), but it's almost always better to declare variables and functions locally with the `local` keyword:

```lua
local logMessage = "User has more than 10 items!"

[Content truncated - see full docs]

---

## Script types and locations

import ScriptLocations from '../includes/engine-comparisons/script-locations.md'

For many developers, the fundamental challenge of adapting to Roblox scripting is the importance of file location and the `Class.Script.RunContext` property. Depending on script type, location in the **Explorer**, and run context, scripts can behave very differently. Certain method calls might fail, objects in your experience might be inaccessible, or scripts might not run at all.

The reason for this complexity is that Roblox experiences are multiplayer by default. Scripts need the ability to only run on the server, only run on the client, or be shared across both. The evolution of the Roblox platform over time has further complicated the situation.

## Script types

Roblox has three types of scripts:

- `Class.Script` - Code that runs on either the server or the client, depending on its location and `Class.Script.RunContext` property.
- `Class.LocalScript` - Code that runs only on the client. Does not have a run context.
- `Class.ModuleScript` - Code that you can reuse in other scripts. Does not have a run context.

When you create a `Class.Script`, its default run context is `Legacy`, meaning that it a) is a server-side script and b) only runs if it is in a server container, such as `Class.Workspace` or `Class.ServerScriptService`.

- If you change the script's run context to `Server`, it can now also run in `Class.ReplicatedStorage`, but that's not recommended. The contents of that location are replicated to clients, so it's a poor location for server-side scripts.
- If you change the script's run context to `Client`, it can run in `ReplicatedStorage`. It can also run in `Class.StarterCharacterScripts` and `Class.StarterPlayerScripts`. Starter containers are copied to clients, though, so the original script **and** the copy run, which isn't desirable.

To change a script run context, select it in the [Explorer](../studio/explorer.md) and change the value in the [Properties](../stud

[Content truncated - see full docs]

---

## Reuse code

After creating a few scripts, it's never long before you want to reuse some code between them. Depending on [location](./locations.md), `Class.ModuleScript|ModuleScripts` let you reuse code between scripts on different sides of the client-server boundary or the same side of the boundary.

You can put module scripts anywhere that you put scripts, but `Class.ReplicatedStorage` is a popular location; storing module scripts here lets you reuse code between the server and clients.

## Anatomy of a module script

In Roblox Studio, add a module script to **ReplicatedStorage** and rename it to `PickupManager`. Each `Class.ModuleScript` starts with the following code:

```lua
local module = {}

return module
```

This code creates an empty Luau [table](../luau/tables.md) and returns it to any script that requires the module script.

The return value can be any [data type](/reference/engine/datatypes) except for `nil`, but most module scripts return a function, a table, or a table of functions. To generate its return value, module scripts can of course run arbitrary code, which includes requiring other module scripts.

<Alert severity="info">
Be careful not to have module scripts require each other in a circular manner, which results in a `Requested module was required recursively` error.
</Alert>

The following example returns a table with a single function called `getPickupBonus`. Paste it into the new module script:

```lua
-- ModuleScript in ReplicatedStorage
local PickupManager = {}

local defaultMultiplier = 1.25
local rarityMultipliers = {
	common = 10,
	uncommon = 20,
	rare = 50,
	legendary = 100
}

-- Add the getPickupBonus function to the PickupManager table
PickupManager.getPickupBonus = function(rarity)
	local bonus = rarityMultipliers[rarity] * defaultMultiplier
	return bonus
end

return PickupManager
```

Adding the function to a table isn't strictly necessary—you could just return the function itself—but it's a good pattern to follow; it gives you an easy-to-un

[Content truncated - see full docs]

---

## Parallel Luau

With the **Parallel Luau** programming model, you can run code on multiple threads simultaneously, which can improve the performance of your experience. As you expand your experience with more content, you can adopt this model to help maintain the performance and safety of your Luau scripts.

<video controls width="100%" src="../assets/scripting/scripts/Parallel-Luau.mp4"></video>

## Parallel programming model

By default, scripts execute sequentially. If your experience has complex logic or content, such as non-player characters (NPCs), raycasting validation, and procedural generation, then sequential execution might cause lag for your users. With the parallel programming model, you can [split tasks into multiple scripts](#split-code-into-multiple-threads) and run them in parallel. This makes your experience code run faster, which improves the user experience.

The parallel programming model also adds safety benefits to your code. By splitting code into multiple threads, when you edit code in one thread, it doesn't affect other code running in parallel. This reduces the risk of having one bug in your code corrupting the entire experience, and minimizes the delay for users in live servers when you push an update.

Adopting the parallel programming model doesn't mean to put everything in multiple threads. For example, the [server-side raycasting validation](#server-side-raycasting-validation) sets each individual user a remote event in parallel but still requires the initial code to run serially to change global properties, which is a common pattern for parallel execution.

Most times you need to combine serial and parallel phases to achieve your desired output, since currently there are some operations not supported in parallel that can prevent scripts from running, such as modifying instances in parallel phases. For more information on the level of usage of APIs in parallel, see [thread safety](#thread-safety).

## Split code into multiple threads

To run your exp

[Content truncated - see full docs]

---

## Schedule code

Scheduling code is useful in many situations, such as ensuring code executes after a specific action or cycle has completed, or delaying code for a specific duration of time. You can use the `Library.task` library to optimize Roblox's [task scheduler](../performance-optimization/microprofiler/task-scheduler.md) to manage and schedule code. You can also use a similar library called `Library.coroutine` to schedule code which has some additional functionality.

### Common methods

The following are the most common `Library.task` methods used to schedule code. You should use the task methods over legacy scheduling methods, such as `Global.RobloxGlobals.wait()`, to ensure that your code runs optimally.

<Alert severity="warning">
Certain legacy global methods, such as (`Global.RobloxGlobals.spawn()`, `Global.RobloxGlobals.delay()`, and `Global.RobloxGlobals.wait()`) can provide similar code scheduling results but are less optimized and configurable as their `Library.task` alternatives. If your experience uses these legacy methods, you should use `Library.task` instead to ensure your experience's code remains efficient and up-to-date.
</Alert>

The following table lists the relevant legacy global methods and their preferred, more optimized counterparts:

| Legacy global methods                   | Task methods                                       | Additional alternatives                            |
| :-------------------------------------- | :------------------------------------------------- | :------------------------------------------------- |
| `wait()`                                | `Library.task.wait()`                              | `Class.RunService.Heartbeat`                       |
| `wait(n)`                               | `Library.task.wait()\|task.wait(n)`                |                                                    |
| `spawn(f)`                              | `Library.task.defer()\|task.defer(f)`              | `Library.task.delay()\|task.delay(

[Content truncated - see full docs]

---

## Scripts

`Class.Script` objects are pieces of Luau code that can modify object behaviors and implement the overall logic of your experience. They can run on the client or server, depending on the functionality you're building. For example, a script that detects and acts on user input must run on the client, and a script that validates an in-experience consumable must run on the server.

Both server-side and client-side scripts can require `Class.ModuleScript` objects, which are [reusable modules](#module-scripts) for organizing and sharing code.

There are two things to consider when writing scripts:

Scripts have a `Class.Script.RunContext` property that sets whether the script runs on the client or server. There are three types of run context:

- **Legacy** - lets the script run based on its parent container. Legacy is the default run context.
- **Server** - lets the script run only on the server, regardless of its parent container.
- **Client** - lets the script run only on the client, regardless of its parent container.

Scripts need to reside in **script containers** in the data model. Based on the run context, you need to place the script in the right container. For more information, see the [server](../projects/data-model.md#server), [client](../projects/data-model.md#client), and [replication](../projects/data-model.md#replication) sections of the data model documentation.

<Alert severity="info">
You can also use `Class.LocalScript` objects for client-side scripts, but we recommend using regular scripts with the run context setting to specify whether the script runs on the client or server.
</Alert>

## Module scripts

`Class.ModuleScript` objects are reusable modules that script objects
load by calling the `Global.LuaGlobals.require()` function. Module scripts must return exactly one
value and run once and only once
per Luau environment. As a result, subsequent calls to `Global.LuaGlobals.require()` return a
cached value. You can execute arbitrary code in a `Class.

[Content truncated - see full docs]

---

## Security and cheat mitigation tactics

The following document covers various concepts and tactics to improve security and mitigate cheating in your Roblox experiences. It's highly recommended that all developers read through these to ensure that your experiences are secure and fair for all users.

## 1. General Principles

Before diving into specific tactics, it's essential to understand the foundational principles of Roblox security. A secure experience is built on a mindset that anticipates adversarial actions. Before writing a single line of code, you must internalize these foundational principles. They should inform every architectural and design decision you make.

### 1.1 Never trust the client

This is the foundational principle. A determined exploiter has complete control over their local state and network traffic. Because exploiters have this level of control, any security measure that relies on client-side enforcement will eventually be bypassed. This is not a limitation of Roblox: it's a fundamental reality of client-server architectures. Assume every piece of data sent from the client has been manipulated, fabricated, or sent with malicious intent. This includes the power to:

- Decompile any replicated LocalScript or any ModuleScript, even if they never run on the client
- Take network ownership of their character and any unanchored parts
- Trigger client-initiated events such as Touched events or ProximityPrompt activations at any range or frequency
- Modify their player's position, physics, or interactions with the world
- Fire or invoke RemoteEvents and RemoteFunctions at any frequency with arbitrary arguments (besides the first Player argument)
- Change anything in their local DataModel without firing any expected events
- Arbitrarily alter the behavior of any locally running code

Because of this, all critical game logic must be validated server-side or run exclusively on the server. The consequences of this control are detailed in [Section 4 (Network Ownership, Movement Validation, and

[Content truncated - see full docs]

---

## Services

In [Reuse code](module.md), you might have noticed frequent use of the `game:GetService()` method. Roblox services let you access the built-in features of the engine, like selling in-experience items, enabling chat, playing sounds, animating objects, and managing instances.

In fact, services are the first step in **the most fundamental, common pattern of Roblox development**:

1. Get services.
1. Require module scripts.
1. Add local functions.
1. Add the [events](events/index.md) that trigger those functions.

For example, you might want to save players' positions in the world when they exit your experience:

```lua
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local SaveManager = require(ReplicatedStorage:WaitForChild("SaveManager"))

-- Local function that calls a reusable function in the module script.
local function saveProgress(character)
	-- Get the position of the player's character.
	local position = character:FindFirstChild("HumanoidRootPart").Position
	-- Use the saveData function in the module script, which writes to the
	-- DataStoreService.
	SaveManager.saveData(character, position)
end

-- Another local function that calls saveProgress() when a character is removed
-- from the experience (in this case, when the player leaves).
local function onPlayerAdded(player)
	player.CharacterRemoving:Connect(saveProgress)
end

-- Calls onPlayerAdded when a player first connects to the experience.
Players.PlayerAdded:Connect(onPlayerAdded)
```

Some key details include:

- Because you should only retrieve a service once per script, the convention is to give the variable the same name as the service. This convention applies to module scripts, as well.
- You retrieve services with the global variable `Class.DataModel|game`, a reference to the root of the data model.
- Roblox doesn't make guarantees around loading order (and [instance streaming](../workspace/streaming.md) further complicates what is and isn

[Content truncated - see full docs]

---

