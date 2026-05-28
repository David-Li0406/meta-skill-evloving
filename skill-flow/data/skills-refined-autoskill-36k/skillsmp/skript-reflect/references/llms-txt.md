# Skript-Reflect - Llms-Txt

**Pages:** 24

---

## Utilities

**URL:** llms-txt#utilities

**Contents:**
- Collect
- Spread
- Array Creation
- Array Value
- Null
- Bits
- Raw Expression
- Members
- Member Names
- Is Instance

Creates an array containing the specified objects. Specifying a type determines the component type of the resulting array.

{% hint style="info" %}
The brackets in this syntax are literal, not representing an optional group.
{% endhint %}

Returns the contents of a single array, iterable, iterator, or stream.

Creates an array of the given type and size. The type may be primitive, which doesn't require an import.

{% hint style="info" %}
The brackets in this syntax are literal, not representing an optional group.
{% endhint %}

Represents the value at a certain index of an array.

This value may be read from and written to.

{% hint style="info" %}
The brackets in this syntax are literal, not representing an optional group.
{% endhint %}

Represents `null` in Java. This is different from Skript's `<none>`.

Represents a subset of bits from a number.

This value may be read from and written to.

Returns the underlying object of an expression.

{% hint style="info" %}
When used with [the expression-expression](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax#expression), you can set it to a value, which will change the input value from that argument. This can be used to store data in variables in the calling trigger.

Returns a list of the fields, methods, or constructors of an object, including their modifiers and parameters.

If you need a list of field or method names without modifier or parameter details, see [Member Names](#member-names).

Returns a list of the fields or methods of an object.

Checks whether objects are instances of the given java types.

Returns a reference to the class from the given java type. Returns an object of type `java.lang.Class`. This expression also supports primitive types, which doesn't require an import.

Returns the instance of the given plugin (either the name as a string, or the plugin class).

**Examples:**

Example 1 (unknown):
```unknown
[%objects%]
[%objects% as %javatype%]
```

Example 2 (unknown):
```unknown
...%object%
```

Example 3 (unknown):
```unknown
new %javatype%[%integer%]
```

Example 4 (unknown):
```unknown
%array%[%integer%]
```

---

## Frequently Asked Questions

**URL:** llms-txt#frequently-asked-questions

**Contents:**
- Why don't you keep documentation on another site?

## Why don't you keep documentation on another site?

Though many Skript-specific documentation sites have popped up and grown in popularity, these sites typically have two issues that make them an unattractive option for skript-reflect.

* Documentation is usually stored solely by the site. If the site ever breaks or shuts down, this means the documentation may be lost as well.
* These sites lack the flexibility of other documentation solutions. Generally, these sites focus on documenting each feature individually. While this might be adequate for many simpler Skript addons, skript-reflect's complexity necessitates the use of manually organized documentation.

That being said, third-party sites may display the contents of skript-reflect's documentation, but they would be responsible for keeping the documentation up-to-date. For the convenience of other scripters, these sites should prominently display [a link to the documentation](https://tpgamesnl.gitbook.io/) on each page. Please avoid documenting features individually or using an automated tool to extract syntax patterns from skript-reflect. Most of skript-reflect's core features are best explained using hand-written documentation.

---

## Running Java code

**URL:** llms-txt#running-java-code

**Contents:**
- Calling methods
  - Calling non-public methods
  - Calling overloaded methods
- Calling fields
  - Calling non-public fields
- Calling constructors

Methods may be used as effects, expressions, and conditions. If used as a condition, the condition will pass as long as the return value of the method is not `false`, `null`, or `0`.

### Calling non-public methods

If the method you're trying to invoke is not public, you may have to prefix the method name with the declaring class in brackets. Since an object may have a non-public method with the same name in multiple superclasses, you must explicitly specify where to find the method.

### Calling overloaded methods

Generally, skript-reflect can infer the correct overloaded method to call from the arguments passed at runtime. If you need to use a certain implementation of a method, you may append a comma separated list to the end of the method name surrounded in brackets.

### Calling non-public fields

If the field you're trying to access is not public, you may have to prefix the field name with the declaring class in brackets. Since an object may have a non-public field with the same name in multiple superclasses, you must explicitly specify where to find the field.

## Calling constructors

**Examples:**

Example 1 (unknown):
```unknown
%object%.<method name>(%objects%)
```

Example 2 (unknown):
```unknown
event-block.breakNaturally()
(last spawned creeper).setPowered(true)
player.giveExpLevels({_levels})
```

Example 3 (unknown):
```unknown
{_arraylist}.[ArrayList]fastRemove(1)
```

Example 4 (unknown):
```unknown
System.out.println[Object]({_something})

Math.max[int, int](0, {_value})
```

---

## Getting Started

**URL:** llms-txt#getting-started

**Contents:**
- Installation

1. Download the latest `skript-reflect.jar` from GitHub
2. Move `skript-reflect.jar` to your `plugins/` folder
3. If you have third-party libraries you would like to use (that are not Bukkit plugins), [follow the steps outlined here.](https://tpgamesnl.gitbook.io/skript-reflect/advanced/loading-external-libraries)

{% hint style="info" %}
Tip: Enable effect commands in Skript's config! Effect commands make it extremely easy to prototype and test Skript code, which can be especially useful when working with skript-reflect.
{% endhint %}

---

## skript-reflect

**URL:** llms-txt#skript-reflect

**Contents:**
- What's been changed in this fork:

This fork of [skript-mirror](https://github.com/btk5h/skript-mirror) aims to fix multiple issues that I believe have been present for too long, and implement some long-wanted features.

Documentation: <https://tpgamesnl.gitbook.io/skript-reflect>

Source code: <https://github.com/TPGamesNL/skript-reflect>

Downloads: [releases](https://github.com/TPGamesNL/skript-reflect/releases) or [actions](https://github.com/TPGamesNL/skript-reflect/actions?query=event%3Apush+is%3Asuccess+actor%3ATPGamesNL) (not stable)

Discord: <https://discord.gg/jDW8UbD>

## What's been changed in this fork:

* Added custom events
* Support for more Java versions (Java 13+, OpenJ9)
* Support for listening to asynchronous events
* Class proxy fixes + documentation
* Fixed multiple issues with local variables
* \+ much more

---

## Custom syntax

**URL:** llms-txt#custom-syntax

**Contents:**
- Shared Syntax
  - Event Classes
  - Expression
  - Matched Pattern
  - Parser Mark
  - Parse Tag
  - Parser Regular Expression
  - Continue

Due to Skript and skript-reflect limitations, it is not easy to create custom syntax through Java calls alone. To help with this, skript-reflect offers utilities that simplify the creation of custom syntax.

{% hint style="info" %}
When used with [the raw expression](https://tpgamesnl.gitbook.io/skript-reflect/basics/utilities#raw-expression), you can set it to a value, which will change the input value from that argument. This can be used to store data in variables in the calling trigger.

Parse tags are like parse tags, but they're a set of strings instead of a single integer.

Parse tags were added in Skript 2.6.1, and are explained in more detail [here](https://github.com/SkriptLang/Skript/pull/4176#issuecomment-882056536)

### Parser Regular Expression

{% content-ref url="custom-syntax/effects" %}
[effects](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/effects)
{% endcontent-ref %}

{% content-ref url="custom-syntax/conditions" %}
[conditions](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/conditions)
{% endcontent-ref %}

{% content-ref url="custom-syntax/expressions" %}
[expressions](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/expressions)
{% endcontent-ref %}

{% content-ref url="custom-syntax/events" %}
[events](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/events)
{% endcontent-ref %}

**Examples:**

Example 1 (unknown):
```unknown
event-classes
```

Example 2 (unknown):
```unknown
[the] expr[ession][s](-| )%number%
```

Example 3 (unknown):
```unknown
import:
	ch.njol.skript.lang.Variable

effect put %objects% in %objects%:
	parse:
		expr-2 is an instance of Variable # to check if the second argument is a variable
		continue
	trigger:
		set raw expr-2 to expr-1
```

Example 4 (unknown):
```unknown
[the] [matched] pattern
```

---

## Conditions

**URL:** llms-txt#conditions

**Contents:**
- Flag `local`
- Section `usable in`
- Section `parse`
- Section `check`

{% tabs %}
{% tab title="With one pattern" %}

{% tab title="With multiple patterns" %}

{% tab title="Property condition" %}

{% endtab %}
{% endtabs %}

Specifying that a condition is `local` makes the condition only usable from within the script that it is defined in. This allows you to create condition that do not interfere with conditions from other addons or scripts.

{% hint style="info" %}
Local conditions are guaranteed to be parsed before other custom conditions, but not necessarily before conditions from other addons.
{% endhint %}

## Section `usable in`

Each entry in this section should be either an imported class or a custom event (syntax: `custom event %string%`).

This condition will error if it is used outside of all the given events.

Code in this section is executed whenever the condition is parsed. This section may be used to emit errors if the condition is used in an improper context.

If this section is included, you must also [`continue`](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/..#continue) if the effect was parsed successfully.

{% hint style="info" %}
Local variables created in this section are copied by-value to other sections.

Code in this section is executed whenever the condition is checked. This section must [`continue`](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/..#continue) if the condition is met. The section may exit without continuing if the condition fails.

**Examples:**

Example 1 (unknown):
```unknown
[local] condition <pattern>:
  usable in:
    # events, optional
  parse:
    # code, optional
  check:
    # code, required
```

Example 2 (unknown):
```unknown
[local] condition:
  usable in:
    # events, optional
  patterns:
    # patterns, one per line
  parse:
    # code, optional
  check:
    # code, required
```

Example 3 (unknown):
```unknown
[local] <skript type> property condition <pattern>:
  usable in:
    # events, optional
  parse:
    # code, optional
  check:
    # code, required
```

Example 4 (unknown):
```unknown
condition example:
  parse:
    set {_test} to 1
    continue
  check:
    # {_test} always starts at 1 here
    add 1 to {_test}
    # 2 is always broadcast
    broadcast "%{_test}%"
```

---

## Error handling

**URL:** llms-txt#error-handling

**Contents:**
- Suppressing errors
- Programmatic access
  - Error object

By default, warnings and errors related to your code are logged to the console. Skript-reflect also offers additional tools that give you more control over how errors are handled.

## Suppressing errors

Adding `try` before a Java call prevents errors from being logged to the console.

{% tabs %}
{% tab title="example.sk" %}

{% endtab %}
{% endtabs %}

If an error occurs, the error object can still be accessed programmatically.

## Programmatic access

In some cases, you may want to handle errors yourself, either to do your own error logging or to perform an alternate task in case of a failure.

{% tabs %}
{% tab title="Syntax" %}

{% endtab %}
{% endtabs %}

Returns the last error object thrown by a java call. If there was an issue resolving the method or converting its output, it may be a `com.btk5h.skriptmirror.JavaCallException`.

**Examples:**

Example 1 (unknown):
```unknown
set {_second item in list} to try {_list}.get(1)
try {_connection}.setUseCaches(true)
```

Example 2 (unknown):
```unknown
[the] [last] [java] (throwable|exception|error)
```

---

## Loading external libraries

**URL:** llms-txt#loading-external-libraries

Normally, you may only access classes loaded in the server's classpath, such as Java standard library classes, Bukkit classes, and plugin classes. If you want to use third-party libraries that are not included on the server classpath, you must load them through skript-reflect first.

To load a jar file, place it in `plugins/skript-reflect/` (create the folder if it doesn't exist).

Once an external library is loaded, its classes may be imported just like any other class.

---

## Reflection

**URL:** llms-txt#reflection

---

## Advanced

**URL:** llms-txt#advanced

---

## Handling events

**URL:** llms-txt#handling-events

**Contents:**
- Listening to events
- Using the `event` expression
- Setting a priority level
- Handling cancelled events

## Listening to events

You may listen to any Bukkit-based event (including events added by other plugins) by referencing the imported class. For example, if you wanted to listen to [org.bukkit.event.entity.EnderDragonChangePhaseEvent](https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/event/entity/EnderDragonChangePhaseEvent.html):

{% tabs %}
{% tab title="example.sk" %}

{% endtab %}
{% endtabs %}

{% hint style="warning" %}
Some plugins use their own event handling system or do not pass their events through Bukkit's event executor (which is the case with some of Skript's internal events).

In order to listen to an event, it must extend [org.bukkit.event.Event](https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/event/Event.html) and be executed by Bukkit's event executor.
{% endhint %}

You may also listen to multiple events with the same handler. The events do not have to be related, but you should take appropriate precautions if you try to access methods that are available in one event but not in the other. For example, if you want to listen to both [org.bukkit.event.entity.ProjectileLaunchEvent](https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/event/entity/ProjectileLaunchEvent.html) and [org.bukkit.event.entity.ProjectileHitEvent](https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/event/entity/ProjectileHitEvent.html)

{% tabs %}
{% tab title="example.sk" %}

{% endtab %}
{% endtabs %}

## Using the `event` expression

skript-reflect exposes an `event` expression, allowing you to access event values using reflection.

{% tabs %}
{% tab title="Syntax" %}

{% tab title="example.sk" %}

{% endtab %}
{% endtabs %}

{% hint style="info" %}
The `event` expression may also be used in normal Skript events.
{% endhint %}

## Setting a priority level

The priority level of an event may be set to control when a particular event handler is run relative to other event handlers.

{% tabs %}
{% tab title="example.sk" %}

{% endtab %}
{% endtabs %}

Any event priorities defined in [org.bukkit.event.EventPriority](https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/event/EventPriority.html) may be used. Lower priority event handlers are run before higher priority event handlers.

{% tabs %}
{% tab title="Event Priorities" %}

{% endtab %}
{% endtabs %}

{% hint style="warning" %}
`highest` is the highest priority event handler you should use if you are modifying the contents of an event. If you only care about the final result of the event, use `monitor`.
{% endhint %}

## Handling cancelled events

By default, event handlers will not be called if an event is cancelled by a lower priority handler. This behavior can be changed by specifying that the handler should handle `all` events.

{% tabs %}
{% tab title="example.sk" %}

{% endtab %}
{% endtabs %}

**Examples:**

Example 1 (unknown):
```unknown
import:
  org.bukkit.event.entity.EnderDragonChangePhaseEvent

on EnderDragonChangePhaseEvent:
  # your code
```

Example 2 (unknown):
```unknown
import:
  org.bukkit.event.entity.ProjectileLaunchEvent
  org.bukkit.event.entity.ProjectileHitEvent

on ProjectileLaunchEvent and ProjectileHitEvent:
  # your code
```

Example 3 (unknown):
```unknown
[the] event
```

Example 4 (unknown):
```unknown
import:
  org.bukkit.event.entity.EnderDragonChangePhaseEvent
  org.bukkit.entity.EnderDragon$Phase as EnderDragonPhase

on EnderDragonChangePhaseEvent:
  if event.getNewPhase() is EnderDragonPhase.CIRCLING:
    event.setNewPhase(EnderDragonPhase.CHARGE_PLAYER)
```

---

## Initial page

**URL:** llms-txt#initial-page

---

## Proxies

**URL:** llms-txt#proxies

{% tabs %}
{% tab title="Syntax" %}

{% endtab %}
{% endtabs %}

The first argument (`%javatypes%`) is a list of imported interfaces (whether a class is an interface can be found on the javadoc).

The second argument is an indexed list variable, with each element in the form `{list::%method name%} = %function/section%`. `%method name%` is the name of one of the methods from one of the interfaces. `%function/section%` is either a function reference or a [section](https://tpgamesnl.gitbook.io/skript-reflect/advanced/reflection/sections).

Function wrappers can be created with the following syntax.

{% tabs %}
{% tab title="Function reference syntax" %}

{% endtab %}
{% endtabs %}

The first argument (`%strings%`) is the name of the function you want to reference. This is enough for the function reference to be completed, but you can also add some argument values.

When a method from the proxy is ran, it is passed on to the function/section corresponding to the method name. The arguments are defined in the following way: 1. The argument values specified in the function reference (if there are any) (only if this method doesn't redirect to a section) 2. The proxy instance object itself. 3. The argument values from the method call.

Here's an example to help you understand it:

{% tabs %}
{% tab title="Function reference example" %}

{% tab title="Section example" %}

{% endtab %}
{% endtabs %}

{% hint style="info" %}
Class proxies are most useful for more interaction with Java code, for example when methods require some implementation of an interface.
{% endhint %}

**Examples:**

Example 1 (unknown):
```unknown
[a] [new] proxy [instance] of %javatypes% (using|from) %objects%
```

Example 2 (unknown):
```unknown
[the] function(s| [reference[s]]) %strings% [called with [[the] [arg[ument][s]]] %-objects%]
```

Example 3 (unknown):
```unknown
import:
    org.bukkit.Bukkit
    ch.njol.skript.Skript
    java.lang.Runnable

function do_something():
    broadcast "It does something!"

command /proxy:
    trigger:
        # As you can see on https://docs.oracle.com/javase/8/docs/api/java/lang/Runnable.html
        # the Runnable interface has one method: run
        set {_functions::run} to function reference "do_something"
        set {_proxy} to new proxy instance of Runnable using {_functions::*}
        {_proxy}.run() # will broadcast 'It does something!'
        Bukkit.getScheduler().runTask(Skript.getInstance(), {_proxy}) # also broadcasts 'It does something!'
```

Example 4 (unknown):
```unknown
import:
    org.bukkit.Bukkit
    ch.njol.skript.Skript
    java.lang.Runnable

command /proxy:
    trigger:
        # As you can see on https://docs.oracle.com/javase/8/docs/api/java/lang/Runnable.html
        # the Runnable interface has one method: run
        create section with {_proxy} stored in {_functions::run}:
            broadcast "It does something!"
        set {_proxy} to new proxy instance of Runnable using {_functions::*}
        {_proxy}.run() # will broadcast 'It does something!'
        Bukkit.getScheduler().runTask(Skript.getInstance(), {_proxy}) # also broadcasts 'It does something!'
```

---

## Importing classes

**URL:** llms-txt#importing-classes

**Contents:**
- Importing classes at parse-time (recommended)
  - Importing NMS classes on Minecraft versions below 1.17
- Importing classes at runtime
  - From a fully qualified name
  - From an object
  - Importing in effect commands
- Dealing with nested classes

Many of skript-reflect's reflection features require a reference to a java class.

## Importing classes at parse-time (recommended)

In most cases, the exact qualified name of the class you need is known without running the script. If this is the case, you should use skript-reflect's import block.

Similar to events, import blocks must be placed at the root of your script (no indentation before `import`). Imports must also be placed before the imported classes are referred to in your code, so we recommend you place your imports as far up in your script as possible.

Once you import a class through an import block, skript-reflect will create an expression allowing you to reference the java class by its simple name.

{% hint style="info" %}
To avoid conflicts, expressions created by import blocks are only available to the script that imported them. You must import java classes in each script that uses them.
{% endhint %}

In most cases, expressions created by import blocks will not conflict with each other or with other Skript expressions. In cases where the class's simple name conflicts with another expression (such as with `Player` and `String`), you must import the class under an alias.

{% hint style="info" %}
Aliases must be valid Java identifiers!
{% endhint %}

### Importing NMS classes on Minecraft versions below 1.17

Since NMS packages from Minecraft versions below 1.17 change with each Minecraft version, you should generate the package prefix dynamically. See [Computed Options](https://tpgamesnl.gitbook.io/skript-reflect/advanced/computed-options#using-computed-options-for-nms-imports) for more details.

## Importing classes at runtime

Sometimes, the class reference you need cannot be determined until the script is executed.

### From a fully qualified name

### Importing in effect commands

Since import blocks aren't available in effect commands, you can use the import effect (only available in effect commands):

This import will only be usable in following effect commands, until you stop the server.

## Dealing with nested classes

Sometimes, a class may be nested inside another class. When referring to the fully qualified name of the class, the nested class is separated from the surrounding class using a `$` rather than a `.`

For example, [`org.bukkit.entity.EnderDragon.Phase`](https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/entity/EnderDragon.Phase.html) would become `org.bukkit.entity.EnderDragon$Phase`

Nested classes usually have more general names than their surrounding classes, so you should import these under an alias.

Another way to import these classes, is to just import their enclosing class:

**Examples:**

Example 1 (unknown):
```unknown
import:
    <fully qualified name> [as <alias>]
    # multiple imports may be placed under the import section
```

Example 2 (unknown):
```unknown
import:
    java.lang.System

command /example:
    trigger:
        message "%System%" # java.lang.System
        System.out.println("test")
```

Example 3 (unknown):
```unknown
import:
    java.lang.String as JavaString

command /example:
    trigger:
        message JavaString.format("Hello %%s", sender)
```

Example 4 (unknown):
```unknown
[the] [java] class %text%
```

---

## Effects

**URL:** llms-txt#effects

**Contents:**
- Flag `local`
- Section `usable in`
- Section `parse`
- Section `trigger`

{% tabs %}
{% tab title="With one pattern" %}

{% tab title="With multiple patterns" %}

{% endtab %}
{% endtabs %}

Specifying that an effect is `local` makes the effect only usable from within the script that it is defined in. This allows you to create effects that do not interfere with effects from other addons or scripts.

{% hint style="info" %}
Local effects are guaranteed to be parsed before other custom effects, but not necessarily before effects from other addons.
{% endhint %}

## Section `usable in`

Each entry in this section should be either an imported class or a custom event (syntax: `custom event %string%`).

This condition will error if it is used outside of all the given events.

Code in this section is executed whenever the effect is parsed. This section may be used to emit errors if the effect is used in an improper context.

If this section is included, you must also [`continue`](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/..#continue) if the effect was parsed successfully.

{% hint style="info" %}
Local variables created in this section are copied by-value to other sections.

The code in this section is executed whenever the effect is run. You can delay the execution of this effect with the following syntax:

After the delay effect has been run, you can use delays in this section. If you're done using delays, you can use [the continue effect](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/..#continue) to continue the execution.

**Examples:**

Example 1 (unknown):
```unknown
[local] effect <pattern>:
  usable in:
    # events, optional
  parse:
    # code, optional
  trigger:
    # code, required
```

Example 2 (unknown):
```unknown
[local] effect:
  usable in:
    # events, optional
  patterns:
    # patterns, one per line
  parse:
    # code, optional
  trigger:
    # code, required
```

Example 3 (unknown):
```unknown
effect example:
  parse:
    set {_test} to 1
    continue
  trigger:
    # {_test} always starts at 1 here
    add 1 to {_test}
    # 2 is always broadcast
    broadcast "%{_test}%"
```

Example 4 (unknown):
```unknown
delay [the] [current] effect
```

---

## Expressions

**URL:** llms-txt#expressions

**Contents:**
- Flag `local`
- Flag `plural`/`non-single`
  - `$` type modifier
- Option `return type`
- Option `loop of`
- Section `usable in`
- Section `parse`
- Section `get`
  - Return
- Section `add`/`set`/`remove`/`remove all`/`delete`/`reset`

{% tabs %}
{% tab title="With one pattern" %}

{% tab title="With multiple patterns" %}

{% tab title="Property expression" %}

Property expressions have two patterns:

When property expressions are used, if multiple inputs are passed, the `get` section is called multiple times with each individual input passed as the first expression.

{% hint style="info" %}
`expression-1` is always the object the property belongs to, even when the`[the] <pattern> of %$<skript types>%` form is used.
{% endhint %}
{% endtab %}
{% endtabs %}

Specifying that an expression is `local` makes the expression only usable from within the script that it is defined in. This allows you to create expression that do not interfere with expressions from other addons or scripts.

{% hint style="info" %}
Local expressions are guaranteed to be parsed before other custom expressions, but not necessarily before expressions from other addons.
{% endhint %}

## Flag `plural`/`non-single`

Specifying that an expression is `plural` or `non-single` indicates that the expression may return more than one value regardless of context.

### `$` type modifier

If the expression is single or non-single depending on whether the input is single or non-single, you may prefix the type with a `$`.

{% tabs %}
{% tab title="example.sk" %}

{% endtab %}
{% endtabs %}

In the above example, `uppercase "test"` would be single and `uppercase ("hello" and "world")` would be non-single.

## Option `return type`

Specifying a return type restricts the possible values that an expression returns, allowing Skript to potentially resolve type conflicts or perform optimizations.

In most cases, explicitly specifying a return type is unnecessary.

If the expression is non-single, this option specifies an alias that may be used if the expression is looped.

{% tabs %}
{% tab title="example.sk" %}

{% endtab %}
{% endtabs %}

## Section `usable in`

Each entry in this section should be either an imported class or a custom event (syntax: `custom event %string%`).

This condition will error if it is used outside of all the given events.

Code in this section is executed whenever the effect is parsed. This section may be used to emit errors if the effect is used in an improper context.

If this section is included, you must also [`continue`](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/..#continue) if the effect was parsed successfully.

{% hint style="info" %}
Local variables created in this section are copied by-value to other sections.

Code in this section is executed whenever the expression's value is read. This section must [return](#return) a value and must not contain delays.

{% tabs %}
{% tab title="Syntax" %}

{% endtab %}
{% endtabs %}

## Section `add`/`set`/`remove`/`remove all`/`delete`/`reset`

Code in these sections is executed whenever the expression is changed using Skript's change effect (or by other means).

{% tabs %}
{% tab title="Syntax" %}

{% endtab %}
{% endtabs %}

Represents the value (or values) that the expression is being changed by.

{% hint style="info" %}
If multiple change values are expected, use the plural form of the expression `change values` instead of the singular `change value`.
{% endhint %}

**Examples:**

Example 1 (unknown):
```unknown
[local] [(plural|non(-|[ ])single))] expression <pattern>:
  return type: <skript type (cannot be a java type)> # optional
  loop of: <text> # optional
  usable in:
    # events, optional
  parse:
    # code, optional
  get:
    # code, optional
  add:
    # code, optional
  set:
    # code, optional
  remove:
    # code, optional
  remove all:
    # code, optional
  delete:
    # code, optional
  reset:
    # code, optional
```

Example 2 (unknown):
```unknown
[local] [(plural|non(-|[ ])single))] expression:
  patterns:
    # patterns, one per line
  return type: <skript type (cannot be a java type)> # optional
  usable in:
    # events, optional
  parse:
    # code, optional
  get:
    # code, optional
  add:
    # code, optional
  set:
    # code, optional
  remove:
    # code, optional
  remove all:
    # code, optional
  delete:
    # code, optional
  reset:
    # code, optional
```

Example 3 (unknown):
```unknown
[local] <skript types> property <pattern>:
  return type: <skript type> # optional
  usable in:
    # events, optional
  parse:
    # code, optional
  get:
    # code, optional
  add:
    # code, optional
  set:
    # code, optional
  remove:
    # code, optional
  remove all:
    # code, optional
  delete:
    # code, optional
  reset:
    # code, optional
```

Example 4 (unknown):
```unknown
[the] <pattern> of %$<skript types>%
%$<skript types>%'[s] <pattern>
```

---

## Sections

**URL:** llms-txt#sections

**Contents:**
- Creating a section
- Running a section
- Example

Sections are very similar to functions: they contain code, they (optionally) have some input variables and (optionally) give some output. One of the key differences being that sections can be created within a trigger.

## Creating a section

{% tabs %}
{% tab title="Syntax" %}

{% endtab %}
{% endtabs %}

The argument variables are a list of variables that represent the input of the section. Example: `with argument variables {_x}, {_y}`.

For section output, you have to use [return](https://tpgamesnl.gitbook.io/skript-reflect/custom-syntax/expressions#return).

The last expression is a variable in which the created section will be stored.

Local variables from before the creation of a section are available in the section itself, but won't modify the local variables from outside the section.

{% tabs %}
{% tab title="Syntax" %}

{% endtab %}
{% endtabs %}

This effect will run the given section. If you run the section (a)sync, you can choose to wait for it to be done or not, by appending `and wait` or not.

{% hint style="info" %}
Note that you can't get output from running an async section without waiting for it to return.
{% endhint %}

You can specify arguments with this effect, for example like this: `with arguments {_a}, {_b}`.

The output of the section is stored in the result part: `and store result in {_result}`.

{% tabs %}
{% tab title="Example" %}

{% endtab %}
{% endtabs %}

{% hint style="info" %}
Sections are very useful to use with [proxies](https://tpgamesnl.gitbook.io/skript-reflect/advanced/reflection/proxies), since you don't have to create functions for the proxy with sections.
{% endhint %}

**Examples:**

Example 1 (unknown):
```unknown
create [new] section [with [arguments variables] %-objects%] (and store it|stored) in %objects%
```

Example 2 (unknown):
```unknown
run section %section% [(1¦sync|2¦async)] [with [arguments] %-objects%] [and store [the] result in %-objects%] [(2¦and wait)]
```

Example 3 (unknown):
```unknown
set {_i} to 2
create new section with {_x} stored in {_section}:
    return {_x} * {_i}
run section {_section} async with 3 and store result in {_result} and wait
broadcast "Result: %{_result}%" # shows 6
```

---

## Events

**URL:** llms-txt#events

**Contents:**
  - Flag `local`
  - Event identifier
  - Option `event-values`
  - Section `parse`
  - Section `check`
  - Calling the event
  - Extra data

{% tabs %}
{% tab title="With one pattern" %}

{% tab title="With multiple patterns" %}

{% endtab %}
{% endtabs %}

Specifying that an event is `local` makes the event only usable from within the script that it is defined in. This allows you to create events that do not interfere with events from other addons or scripts.

{% hint style="info" %}
Local events are guaranteed to be parsed before other custom events, but not necessarily before events from other addons.
{% endhint %}

The string used in the trigger line represents the identifier of this custom event. This identifier should be used for [`calling the event`](#calling-the-event).

### Option `event-values`

The event-values specified here will be available in the event, either as a default expression (`message "Hello"` without the need for `to player`) or as a normal event-value (`event-player` / `player`)

Code in this section is executed whenever the event is parsed. This section may be used to emit errors if the effect is used in an improper context.

If this section is included, you must also [`continue`](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/..#continue) if the event was parsed successfully.

{% hint style="info" %}
Local variables created in this section are copied by-value to other sections.

Code in this section is executed just before the event is called. This section may be used to stop the event from being called if certain conditions are met.

If this section is included, you must also [`continue`](https://tpgamesnl.gitbook.io/skript-reflect/advanced/custom-syntax/..#continue) if you want to event to be called.

### Calling the event

You can get an instance of a custom event using the following expression:

The first argument should contain the name of the event you want to call. The second argument is a list variable, with each element of the following format: `{list::%type%} = %value%`. The third argument is almost the same, the only difference is that `%type%` is replaced with a string, which is just the index. The first list variable is for [the event-values](#option-event-values), while the second is for [the extra data](#extra-data).

You can then call it using the following effect:

If you want to check if an event has been cancelled, after you've called it, you can use the following condition:

If the event-values aren't enough for your desire, you can make use of the extra data feature. The syntax for adding event-values to a custom event is explained in [the event-values option](#option-event-values), and how to call an event with them is explained in [calling the event](#calling-the-event) In the event itself, you can get the extra data with the data expression:

In the syntax above, `%string%` is the index. This doesn't have to be plural, but can be.

{% hint style="info" %}
It may look fancier to create a custom expression instead of using extra data. To do so, you need to call `event.getData(%string%)` to get the data value. See the `usable in` sections in [effects](https://tpgamesnl.gitbook.io/skript-reflect/advanced/effects#section-usable-in), [conditions](https://tpgamesnl.gitbook.io/skript-reflect/advanced/conditions#section-usable-in) and [expressions](https://tpgamesnl.gitbook.io/skript-reflect/advanced/expressions#section-usable-in).
{% endhint %}

**Examples:**

Example 1 (unknown):
```unknown
[local] [custom] event %string%:
  pattern: # pattern, required
  event-values: # list of types, optional
  parse:
    # code, optional
  check:
    # code, optional
```

Example 2 (unknown):
```unknown
[local] [custom] event %string%:
  patterns:
    # patterns, one per line, required
  event-values: # list of types, optional
  parse:
    # code, optional
  check:
    # code, optional
```

Example 3 (unknown):
```unknown
event "example":
  pattern: example
  parse:
    set {_test} to 1
    continue
  check:
    # {_test} always starts at 1 here
    add 1 to {_test}
    # broadcasts 2
    broadcast "%{_test}%"
    continue
```

Example 4 (unknown):
```unknown
[a] [new] custom event %string% [(with|using) [[event-]values] %-objects%] [[and] [(with|using)] data %-objects%]
```

---

## Experiments

**URL:** llms-txt#experiments

**Contents:**
- `deferred-parsing`
- Preloading

{% hint style="danger" %}
These features are experimental and are subject to change in the future!
{% endhint %}

In order to enable experimental features, add the following section to your script:

{% tabs %}
{% tab title="Consent section" %}

{% endtab %}
{% endtabs %}

Individual features may be enabled by adding the codename of the feature on new lines following the consent section.

## `deferred-parsing`

Deferred parsing allows you to prefix any line with `(parse[d] later)` to defer parsing until the first execution of the line. This allows you to circumvent issues where custom syntaxes are used before they are defined.

{% hint style="danger" %}
This should only be used when two custom syntaxes refer to each other. Other issues should be resolved by reordering custom syntax definitions and ensuring that libraries containing custom syntax load before other scripts, or by using the [preloading feature](#preloading).
{% endhint %}

When preloading is enabled in `config.yml`, custom syntax will be available from any scripts, independent of file names. Preloading is only available from Skript 2.5-alpha6+, using skript-reflect 2.2-alpha1 or above.

There is one case for which custom syntax can't be preloaded, that is when it has a `parse` section. `parse` sections can't be used in preloadable syntax, so to still allow for custom syntax to run code when being parsed, there are the `safe parse` sections. These sections have the same purpose as normal `parse` sections, with a few differences:

* In safe parse sections
  * Functions can't be used.
  * Options (including computed options) can't be used.
  * Some imports can't be used (if they contain options for example).

Because of these differences, custom syntax with `safe parse` sections are preloadable.

{% hint style="warning" %}
Be careful when using custom syntax in `on script load` events, as the custom syntax might not have been fully parsed yet.
{% endhint %}

**Examples:**

Example 1 (unknown):
```unknown
skript-reflect, I know what I'm doing:
  I understand that the following features are experimental and may change in the future.
  I have read about this at https://tpgamesnl.gitbook.io/skript-reflect/advanced/experiments
```

---

## Reading Javadocs

**URL:** llms-txt#reading-javadocs

**Contents:**
- Fully qualified names
- Non-public APIs
  - Built-in inspection
  - Source code

Most public APIs and libraries offer documentation in the form of Javadocs. Javadocs outline what features of a library are publicly accessible to developers.

Here are a few links to some commonly referenced Javadocs: [Java SE 8 Javadocs](https://docs.oracle.com/javase/8/docs/api/overview-summary.html), [Spigot Javadocs](https://hub.spigotmc.org/javadocs/spigot/overview-summary.html)

## Fully qualified names

A fully qualified name is composed of a class's package and name. On the Javadoc of a class, this may be found near the top of the page. Fully qualified names are used when [importing classes](https://tpgamesnl.gitbook.io/skript-reflect/basics/importing-classes).

![The fully qualified name of this class is org.bukkit.entity.Player ](https://1452774296-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-M9EtYI-5mJuHFlCVB2t%2Fsync%2Fe9a04fa5f98de95e16d613287a5a5df38df97f02.png?generation=1591552337382871\&alt=media)

![Classes may have an inheritance hierarchy which shows the fully qualified name of the class](https://1452774296-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-M9EtYI-5mJuHFlCVB2t%2Fsync%2F1b494c971cbedd1357c5fbdf1314fc4fc585cbeb.png?generation=1591552344422954\&alt=media)

If the name of the class contains a `.`, that is because the class is nested within another class. When referring to these classes, you must replace the `.` with a `$`.

![The fully qualified name of this class is org.bukkit.Effect$Type](https://1452774296-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/assets%2F-M9EtYI-5mJuHFlCVB2t%2Fsync%2F8299927223bd628d1f44c9e90f3ff14a0f54fa48.png?generation=1591552337311498\&alt=media)

{% hint style="info" %}
Typically, nested classes should be [imported under an alias](https://tpgamesnl.gitbook.io/skript-reflect/importing-classes#dealing-with-nested-classes)!
{% endhint %}

Javadocs do not describe everything available in a library. Most libraries include private classes, methods, fields, and constructors reserved for internal use. Using skript-reflect, these internal APIs are accessible just like any public API.

{% hint style="warning" %}
Usually, private APIs are private for a reason! Make sure you know what you're doing before you start digging around!
{% endhint %}

### Built-in inspection

skript-reflect has built-in tools for dumping all of the available members of an object. If you need a list of these members, including their return types and input parameters, you can use the [Members](https://tpgamesnl.gitbook.io/skript-reflect/utilities#members) expression. If you only need a list of names, you can use the [Member Names](https://tpgamesnl.gitbook.io/skript-reflect/utilities#member-names) expression.

The best way to learn about how a library works is to read the source code! Many libraries will have their source code easily available online, though you may have to resort to decompiling libraries that are not open source.

[Craftbukkit source code](https://hub.spigotmc.org/stash/projects/SPIGOT/repos/craftbukkit/browse) [Online Java decompiler](http://www.javadecompilers.com/)

---

## Code Conventions

**URL:** llms-txt#code-conventions

**Contents:**
- Separate complex Skript expressions from skript-reflect calls
- Keep the target of a skript-reflect call grouped
- Avoid aliasing classes for aesthetic purposes
- Avoid unnecessary uses of Java reflection

## Separate complex Skript expressions from skript-reflect calls

Combining Skript expressions with skript-reflect calls may make your code difficult to read. Use variables to separate these different types of calls.

{% hint style="danger" %}

{% hint style="success" %}

## Keep the target of a skript-reflect call grouped

When calling a method or accessing a field, avoid using spaces when possible.

{% hint style="danger" %}

{% hint style="success" %}

If the expression is simple (i.e. does not contain other expressions) but requires a space, surround the expression in parentheses.

{% hint style="danger" %}

{% hint style="success" %}

If the target of the expression is not simple (i.e. contains other expressions), extract the expression into a local variable. ([rule](#separate-complex-skript-expressions-from-skript-reflect-calls))

Variables are the exception to this rule and may contain spaces and/or other expressions

{% hint style="success" %}

## Avoid aliasing classes for aesthetic purposes

The purpose of import aliases is to avoid conflicts with other imports and expressions. Do not alias imports in order to make them look like Skript events.

{% hint style="danger" %}

{% hint style="success" %}

## Avoid unnecessary uses of Java reflection

Especially when copying Java code and translating it for skript-reflect, you may run into instances where you need to use reflection to access a private method, field, or constructor. In skript-reflect, private members are visible and accessible by default.

{% hint style="danger" %}

{% hint style="success" %}

**Examples:**

Example 1 (unknown):
```unknown
(the player's targeted block).breakNaturally()
```

Example 2 (unknown):
```unknown
set {_target} to the player's targeted block
{_target}.breakNaturally()
```

Example 3 (unknown):
```unknown
the event.getPlayer()
```

Example 4 (unknown):
```unknown
event.getPlayer()
```

---

## Basics

**URL:** llms-txt#basics

---

## Computed Options

**URL:** llms-txt#computed-options

**Contents:**
  - Section `get`
- Using computed options for NMS imports

Skript's options section allows you to create snippets of text that are copied into other sections of your script. This is useful for static text, but does not work well for text that must be derived from dynamic sources, such as variables.

After the computed option is defined, it is accessible as `{@<option name>}` within the same script.

Code in this section is executed as soon as it is parsed. This section must [return](https://tpgamesnl.gitbook.io/skript-reflect/custom-syntax/expressions#return) a value and must not contain delays.

## Using computed options for NMS imports

NMS packages from before Minecraft 1.17 include the Minecraft version, preventing code referencing NMS classes from working across versions. To get around this, computed options may be used to dynamically generate the proper NMS package.

{% hint style="warning" %}
While this code dynamically generates the appropriate NMS package prefix, it does not guarantee your code will work across versions! Be aware that classes, methods, and fields may change in incompatible ways across versions.
{% endhint %}

**Examples:**

Example 1 (unknown):
```unknown
option <option name>:
  get:
    # code, required
```

Example 2 (unknown):
```unknown
import:
  org.bukkit.Bukkit

option nms:
  get:
    set {_nms version} to Bukkit.getServer().getClass().getPackage().getName().split("\.")[3]
    return "net.minecraft.server.%{_nms version}%"

import:
  {@nms}.MinecraftServer
  {@nms}.Item
```

---
