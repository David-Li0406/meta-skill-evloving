# Godot - About

**Pages:** 7

---

## Complying with licenses — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/complying_with_licenses.html

**Contents:**
- Complying with licenses
- What are licenses?
- Requirements
- Inclusion
  - Credits screen
  - Licenses screen
  - Output log
  - Accompanying file
  - Printed manual
  - Link to the license

The recommendations in this page are not legal advice. They are provided in good faith to help users navigate license attribution requirements.

Godot is created and distributed under the MIT License. It doesn't have a sole owner, as every contributor that submits code to the project does it under this same license and keeps ownership of their contribution.

The license is the legal requirement for you (or your company) to use and distribute the software (and derivative projects, including games made with it). Your game or project can have a different license, but it still needs to comply with the original one.

This section covers compliance with licenses from a user perspective. If you are interested in licence compliance as a contributor, you can find guidelines here.

Alongside the Godot license text, remember to also list third-party notices for assets you're using, such as textures, models, sounds, music and fonts. This includes free assets, which often come with licenses that require attribution.

In the case of the MIT license, the only requirement is to include the license text somewhere in your game or derivative project.

This text reads as follows:

Beside its own MIT license, Godot includes code from a number of third-party libraries. See Third-party licenses for details.

Your games do not need to be under the same license. You are free to release your Godot projects under any license and to create commercial games with the engine.

The license text must be made available to the user. The license doesn't specify how the text has to be included, but here are the most common approaches (you only need to implement one of them, not all).

Include the above license text somewhere in the credits screen. It can be at the bottom after showing the rest of the credits. Most large studios use this approach with open source licenses.

Some games have a special menu (often in the settings) to display licenses. This menu is typically accessed with a button called Third-party Licenses or Open Source Licenses.

Printing the license text using the print() function may be enough on platforms where a global output log is readable. This is the case on desktop platforms, Android and HTML5 (but not iOS).

If the game is distributed on desktop platforms, a file containing the license text can be added to the software that is installed to the user PC.

If the game includes a printed manual, the license text can be included there.

The Godot Engine developers consider that a link to godotengine.org/license in your game documentation or credits would be an acceptable way to satisfy the license terms.

Godot provides several methods to get license information in the Engine singleton. This allows you to source the license information directly from the engine binary, which prevents the information from becoming outdated if you update engine versions.

For the engine itself:

Engine.get_license_text

For third-party components used by the engine:

Engine.get_license_info

Engine.get_copyright_info

Godot itself contains software written by third parties, which is compatible with, but not covered by Godot's MIT license.

Many of these dependencies are distributed under permissive open source licenses which require attribution by explicitly citing their copyright statement and license text in the final product's documentation.

Given the scope of the Godot project, this is fairly difficult to do thoroughly. For the Godot editor, the full documentation of third-party copyrights and licenses is provided in the COPYRIGHT.txt file.

A good option for end users to document third-party licenses is to include this file in your project's distribution, which you can e.g. rename to GODOT_COPYRIGHT.txt to prevent any confusion with your own code and assets.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Documentation changelog — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/docs_changelog.html

**Contents:**
- Documentation changelog
- New pages since version 4.3
  - 2D
  - 3D
  - Debug
  - Editor
  - Performance
  - Physics
  - Rendering
  - Shaders

The documentation is continually being improved. New releases include new pages, fixes and updates to existing pages, and many updates to the class reference. Below is a list of new pages added since version 3.0.

This document only contains new pages so not all changes are reflected, many pages have been substantially updated but are not reflected in this document.

Third-person camera with spring arm

Reducing stutter from shader (pipeline) compilations

Physics Interpolation

Using physics interpolation

Advanced physics interpolation

2D and 3D physics interpolation

Overview of renderers

Handling compatibility breakages

The .gdextension file

Upgrading from Godot 4.2 to Godot 4.3

A better XR start script

Where to go from here

OpenXR composition layers

2D coordinate systems and 2D transforms

Upgrading from Godot 4.1 to Godot 4.2

Runtime file loading and saving

Godot Android library

Internal rendering architecture

Upgrading from Godot 4.0 to Godot 4.1

Troubleshooting physics issues

Faking global illumination

Introduction to global illumination

Mesh level of detail (LOD)

Signed distance field global illumination (SDFGI)

Visibility ranges (HLOD)

Volumetric fog and fog volumes

Variable rate shading

Physical light and camera units

Retargeting 3D Skeletons

Custom platform ports

Upgrading from Godot 3 to Godot 4

Large world coordinates

Custom performance monitors

Using compute shaders

Managing editor features

GDScript documentation comments

3D rendering limitations

Version control systems

Configuring an IDE: Code::Blocks

Default editor shortcuts

Exporting for dedicated servers

Controllers, gamepads, and joysticks

Random number generation

HTML5 shell class reference

Collision shapes (2D)

Collision shapes (3D)

Creating script templates

Evaluating expressions

GDScript warning system (split from Static typing in GDScript)

Gradle builds for Android

Recording with microphone

Sync the gameplay with audio and music

Beziers, curves and paths

Localization using gettext (PO files)

Introduction to shaders

Your second 3D shader

Godot Android plugins

Visual Shader plugins

Using multiple threads

Using the SurfaceTool

Using the MeshDataTool

Optimization using MultiMeshes

Optimization using Servers

Complying with licenses

Static typing in GDScript

Applying object-oriented principles in Godot

When to use scenes versus scripts

Autoloads versus regular nodes

When and how to avoid using nodes for everything

2D lights and shadows

Prototyping levels with CSG

Animating thousands of fish with MultiMeshInstance3D

Controlling thousands of fish with Particles

Using a SubViewport as a texture

Custom post-processing

Converting GLSL to Godot shaders

Advanced post-processing

Introduction to shaders

Making main screen plugins

Custom HTML page for Web export

Fixing jitter, stutter and input lag

Running code in the editor

Change scenes manually

Optimizing a build for size

Compiling with PCK encryption key

Binding to external libraries

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Frequently asked questions — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/faq.html

**Contents:**
- Frequently asked questions
- What can I do with Godot? How much does it cost? What are the license terms?
- Which platforms are supported by Godot?
- Which programming languages are supported in Godot?
- What is GDScript and why should I use it?
- What were the motivations behind creating GDScript?
- Which programming language is fastest?
- What 3D model formats does Godot support?
- Will [insert closed SDK such as FMOD, GameWorks, etc.] be supported in Godot?
- How can I extend Godot?

Godot is Free and open source Software available under the OSI-approved MIT license. This means it is free as in "free speech" as well as in "free beer."

You are free to download and use Godot for any purpose: personal, non-profit, commercial, or otherwise.

You are free to modify, distribute, redistribute, and remix Godot to your heart's content, for any reason, both non-commercially and commercially.

All the contents of this accompanying documentation are published under the permissive Creative Commons Attribution 3.0 (CC BY 3.0) license, with attribution to "Juan Linietsky, Ariel Manzur and the Godot Engine community."

Logos and icons are generally under the same Creative Commons license. Note that some third-party libraries included with Godot's source code may have different licenses.

For full details, look at the COPYRIGHT.txt as well as the LICENSE.txt and LOGO_LICENSE.txt files in the Godot repository.

Also, see the license page on the Godot website.

Android (experimental)

For exporting your games:

Both 32- and 64-bit binaries are supported where it makes sense, with 64 being the default. Official macOS builds support Apple Silicon natively as well as x86_64.

Some users also report building and using Godot successfully on ARM-based systems with Linux, like the Raspberry Pi.

The Godot team can't provide an open source console export due to the licensing terms imposed by console manufacturers. Regardless of the engine you use, though, releasing games on consoles is always a lot of work. You can read more about Console support in Godot.

For more on this, see the sections on exporting and compiling Godot yourself.

Godot 3 also had support for Universal Windows Platform (UWP). This platform port was removed in Godot 4 due to lack of maintenance, and it being deprecated by Microsoft. It is still available in the current stable release of Godot 3 for interested users.

The officially supported languages for Godot are GDScript, C#, and C++. See the subcategories for each language in the scripting section.

If you are just starting out with either Godot or game development in general, GDScript is the recommended language to learn and use since it is native to Godot. While scripting languages tend to be less performant than lower-level languages in the long run, for prototyping, developing Minimum Viable Products (MVPs), and focusing on Time-To-Market (TTM), GDScript will provide a fast, friendly, and capable way of developing your games.

Note that C# support is still relatively new, and as such, you may encounter some issues along the way. C# support is also currently missing on the web platform. Our friendly and hard-working development community is always ready to tackle new problems as they arise, but since this is an open source project, we recommend that you first do some due diligence yourself. Searching through discussions on open issues is a great way to start your troubleshooting.

As for new languages, support is possible via third parties with GDExtensions. (See the question about plugins below). Work is currently underway, for example, on unofficial bindings for Godot to Python and Nim.

GDScript is Godot's integrated scripting language. It was built from the ground up to maximize Godot's potential in the least amount of code, affording both novice and expert developers alike to capitalize on Godot's strengths as fast as possible. If you've ever written anything in a language like Python before, then you'll feel right at home. For examples and a complete overview of the power GDScript offers you, check out the GDScript scripting guide.

There are several reasons to use GDScript, but the most salient reason is the overall reduction of complexity.

The original intent of creating a tightly integrated, custom scripting language for Godot was two-fold: first, it reduces the amount of time necessary to get up and running with Godot, giving developers a rapid way of exposing themselves to the engine with a focus on productivity; second, it reduces the overall burden of maintenance, attenuates the dimensionality of issues, and allows the developers of the engine to focus on squashing bugs and improving features related to the engine core, rather than spending a lot of time trying to get a small set of incremental features working across a large set of languages.

Since Godot is an open source project, it was imperative from the start to prioritize a more integrated and seamless experience over attracting additional users by supporting more familiar programming languages, especially when supporting those more familiar languages would result in a worse experience. We understand if you would rather use another language in Godot (see the list of supported options above). That being said, if you haven't given GDScript a try, try it for three days. Just like Godot, once you see how powerful it is and how rapid your development becomes, we think GDScript will grow on you.

More information about getting comfortable with GDScript or dynamically typed languages can be found in the GDScript: An introduction to dynamic languages tutorial.

In the early days, the engine used the Lua scripting language. Lua can be fast thanks to LuaJIT, but creating bindings to an object-oriented system (by using fallbacks) was complex and slow and took an enormous amount of code. After some experiments with Python, that also proved difficult to embed.

The main reasons for creating a custom scripting language for Godot were:

Poor threading support in most script VMs, and Godot uses threads (Lua, Python, Squirrel, JavaScript, ActionScript, etc.).

Poor class-extending support in most script VMs, and adapting to the way Godot works is highly inefficient (Lua, Python, JavaScript).

Many existing languages have horrible interfaces for binding to C++, resulting in a large amount of code, bugs, bottlenecks, and general inefficiency (Lua, Python, Squirrel, JavaScript, etc.). We wanted to focus on a great engine, not a great number of integrations.

No native vector types (Vector3, Transform3D, etc.), resulting in highly reduced performance when using custom types (Lua, Python, Squirrel, JavaScript, ActionScript, etc.).

Garbage collector results in stalls or unnecessarily large memory usage (Lua, Python, JavaScript, ActionScript, etc.).

Difficulty integrating with the code editor for providing code completion, live editing, etc. (all of them).

GDScript was designed to curtail the issues above, and more.

In most games, the scripting language itself is not the cause of performance problems. Instead, performance is slowed by inefficient algorithms (which are slow in all languages), by GPU performance, or by the common C++ engine code like physics or navigation. All languages supported by Godot are fast enough for general-purpose scripting. You should choose a language based on other factors, like ease-of-use, familiarity, platform support, or language features.

In general, the performance of C# and GDScript is within the same order of magnitude, and C++ is faster than both.

Comparing GDScript performance to C# is tricky, since C# can be faster in some specific cases. The C# language itself tends to be faster than GDScript, which means that C# can be faster in situations with few calls to Godot engine code. However, C# can be slower than GDScript when making many Godot API calls, due to the cost of marshalling. C#'s performance can also be brought down by garbage collection which occurs at random and unpredictable moments. This can result in stuttering issues in complex projects, and is not exclusive to Godot.

C++, using GDExtension, will almost always be faster than either C# or GDScript. However, C++ is less easy to use than C# or GDScript, and is slower to develop with.

You can also use multiple languages within a single project, with cross-language scripting, or by using GDExtension and scripting languages together. Be aware that doing so comes with its own complications.

You can find detailed information on supported formats, how to export them from your 3D modeling software, and how to import them for Godot in the Importing 3D scenes documentation.

The aim of Godot is to create a free and open source MIT-licensed engine that is modular and extendable. There are no plans for the core engine development community to support any third-party, closed-source/proprietary SDKs, as integrating with these would go against Godot's ethos.

That said, because Godot is open source and modular, nothing prevents you or anyone else interested in adding those libraries as a module and shipping your game with them, as either open- or closed-source.

To see how support for your SDK of choice could still be provided, look at the Plugins question below.

If you know of a third-party SDK that is not supported by Godot but that offers free and open source integration, consider starting the integration work yourself. Godot is not owned by one person; it belongs to the community, and it grows along with ambitious community contributors like you.

For extending Godot, like creating Godot Editor plugins or adding support for additional languages, take a look at EditorPlugins and tool scripts.

Also, see the official blog post on GDExtension, a way to develop native extensions for Godot:

Introducing GDNative's successor, GDExtension

You can also take a look at the GDScript implementation, the Godot modules, as well as the Jolt physics engine integration for Godot. This would be a good starting point to see how another third-party library integrates with Godot.

Since you don't need to actually install Godot on your system to run it, this means desktop integration is not performed automatically. There are two ways to overcome this. You can install Godot from Steam (all platforms), Scoop (Windows), Homebrew (macOS) or Flathub (Linux). This will automatically perform the required steps for desktop integration.

Alternatively, you can manually perform the steps that an installer would do for you:

Move the Godot executable to a stable location (i.e. outside of your Downloads folder), so you don't accidentally move it and break the shortcut in the future.

Right-click the Godot executable and choose Create Shortcut.

Move the created shortcut to %APPDATA%\Microsoft\Windows\Start Menu\Programs. This is the user-wide location for shortcuts that will appear in the Start menu. You can also pin Godot in the task bar by right-clicking the executable and choosing Pin to Task Bar.

Drag the extracted Godot application to /Applications/Godot.app, then drag it to the Dock if desired. Spotlight will be able to find Godot as long as it's in /Applications or ~/Applications.

Move the Godot binary to a stable location (i.e. outside of your Downloads folder), so you don't accidentally move it and break the shortcut in the future.

Rename and move the Godot binary to a location present in your PATH environment variable. This is typically /usr/local/bin/godot or /usr/bin/godot. Doing this requires administrator privileges, but this also allows you to run the Godot editor from a terminal by entering godot.

If you cannot move the Godot editor binary to a protected location, you can keep the binary somewhere in your home directory, and modify the Path= line in the .desktop file linked below to contain the full absolute path to the Godot binary.

Save this .desktop file to $HOME/.local/share/applications/. If you have administrator privileges, you can also save the .desktop file to /usr/local/share/applications to make the shortcut available for all users.

In its default configuration, Godot is semi-portable. Its executable can run from any location (including non-writable locations) and never requires administrator privileges.

However, configuration files will be written to the user-wide configuration or data directory. This is usually a good approach, but this means configuration files will not carry across machines if you copy the folder containing the Godot executable. See File paths in Godot projects for more information.

If true portable operation is desired (e.g. for use on a USB stick), follow the steps in Self-contained mode.

Godot aims for cross-platform compatibility and open standards first and foremost. OpenGL and Vulkan are the technologies that are both open and available on (nearly) all platforms. Thanks to this design decision, a project developed with Godot on Windows will run out of the box on Linux, macOS, and more.

While Vulkan and OpenGL remain our primary focus for their open standard and cross-platform benefits, Godot 4.3 introduced experimental support for Direct3D 12. This addition aims to enhance performance and compatibility on platforms where Direct3D 12 is prevalent, such as Windows and Xbox. However, Vulkan and OpenGL will continue as the default rendering drivers on all platforms, including Windows.

Godot intentionally does not include features that can be implemented by add-ons unless they are used very often. One example of something not used often is advanced artificial intelligence functionality.

There are several reasons for this:

Code maintenance and surface for bugs. Every time we accept new code in the Godot repository, existing contributors often take the responsibility of maintaining it. Some contributors don't always stick around after getting their code merged, which can make it difficult for us to maintain the code in question. This can lead to poorly maintained features with bugs that are never fixed. On top of that, the "API surface" that needs to be tested and checked for regressions keeps increasing over time.

Ease of contribution. By keeping the codebase small and tidy, it can remain fast and easy to compile from source. This makes it easier for new contributors to get started with Godot, without requiring them to purchase high-end hardware.

Keeping the binary size small for the editor. Not everyone has a fast Internet connection. Ensuring that everyone can download the Godot editor, extract it and run it in less than 5 minutes makes Godot more accessible to developers in all countries.

Keeping the binary size small for export templates. This directly impacts the size of projects exported with Godot. On mobile and web platforms, keeping file sizes low is important to ensure fast installation and loading on underpowered devices. Again, there are many countries where high-speed Internet is not readily available. To add to this, strict data usage caps are often in effect in those countries.

For all the reasons above, we have to be selective of what we can accept as core functionality in Godot. This is why we are aiming to move some core functionality to officially supported add-ons in future versions of Godot. In terms of binary size, this also has the advantage of making you pay only for what you actually use in your project. (In the meantime, you can compile custom export templates with unused features disabled to optimize the distribution size of your project.)

This question pops up often and it's probably thanks to the misunderstanding created by Apple when they originally doubled the resolution of their devices. It made people think that having the same assets in different resolutions was a good idea, so many continued towards that path. That originally worked to a point and only for Apple devices, but then several Android and Apple devices with different resolutions and aspect ratios were created, with a very wide range of sizes and DPIs.

The most common and proper way to achieve this is to, instead, use a single base resolution for the game and only handle different screen aspect ratios. This is mostly needed for 2D, as in 3D, it's just a matter of camera vertical or horizontal FOV.

Choose a single base resolution for your game. Even if there are devices that go up to 1440p and devices that go down to 400p, regular hardware scaling in your device will take care of this at little or no performance cost. The most common choices are either near 1080p (1920x1080) or 720p (1280x720). Keep in mind the higher the resolution, the larger your assets, the more memory they will take and the longer the time it will take for loading.

Use the stretch options in Godot; canvas items stretching while keeping aspect ratios works best. Check the Multiple resolutions tutorial on how to achieve this.

Determine a minimum resolution and then decide if you want your game to stretch vertically or horizontally for different aspect ratios, or if there is one aspect ratio and you want black bars to appear instead. This is also explained in Multiple resolutions.

For user interfaces, use the anchoring to determine where controls should stay and move. If UIs are more complex, consider learning about Containers.

And that's it! Your game should work in multiple resolutions.

When it's ready! See When is the next release out? for more information.

We recommend using Godot 4.x for new projects, but depending on the feature set you need, it may be better to use 3.x instead. See Which version should I use for a new project? for more information.

Some new versions are safer to upgrade to than others. In general, whether you should upgrade depends on your project's circumstances. See Should I upgrade my project to use new engine versions? for more information.

You can find a detailed comparison of the renderers in Overview of renderers.

Awesome! As an open source project, Godot thrives off of the innovation and the ambition of developers like you.

The best way to start contributing to Godot is by using it and reporting any issues that you might experience. A good bug report with clear reproduction steps helps your fellow contributors fix bugs quickly and efficiently. You can also report issues you find in the online documentation.

If you feel ready to submit your first PR, pick any issue that resonates with you from one of the links above and try your hand at fixing it. You will need to learn how to compile the engine from sources, or how to build the documentation. You also need to get familiar with Git, a version control system that Godot developers use.

We explain how to work with the engine source, how to edit the documentation, and what other ways to contribute are there in our documentation for contributors.

We are always looking for suggestions about how to improve the engine. User feedback is the main driving force behind our decision-making process, and limitations that you might face while working on your project are a great data point for us when considering engine enhancements.

If you experience a usability problem or are missing a feature in the current version of Godot, start by discussing it with our community. There may be other, perhaps better, ways to achieve the desired result that community members could suggest. And you can learn if other users experience the same issue, and figure out a good solution together.

If you come up with a well-defined idea for the engine, feel free to open a proposal issue. Try to be specific and concrete while describing your problem and your proposed solution — only actionable proposals can be considered. It is not required, but if you want to implement it yourself, that's always appreciated!

If you only have a general idea without specific details, you can open a proposal discussion. These can be anything you want, and allow for a free-form discussion in search of a solution. Once you find one, a proposal issue can be opened.

Please, read the readme document before creating a proposal to learn more about the process.

Yes! Godot features an extensive built-in UI system, and its small distribution size can make it a suitable alternative to frameworks like Electron or Qt.

When creating a non-game application, make sure to enable low-processor mode in the Project Settings to decrease CPU and GPU usage.

Check out Material Maker and Pixelorama for examples of open source applications made with Godot.

Godot is meant to be used with its editor. We recommend you give it a try, as it will most likely save you time in the long term. There are no plans to make Godot usable as a library, as it would make the rest of the engine more convoluted and difficult to use for casual users.

If you want to use a rendering library, look into using an established rendering engine instead. Keep in mind rendering engines usually have smaller communities compared to Godot. This will make it more difficult to find answers to your questions.

Godot does not use a standard GUI toolkit like GTK, Qt or wxWidgets. Instead, Godot uses its own user interface toolkit, rendered using OpenGL ES or Vulkan. This toolkit is exposed in the form of Control nodes, which are used to render the editor (which is written in C++). These Control nodes can also be used in projects from any scripting language supported by Godot.

This custom toolkit makes it possible to benefit from hardware acceleration and have a consistent appearance across all platforms. On top of that, it doesn't have to deal with the LGPL licensing caveats that come with GTK or Qt. Lastly, this means Godot is "eating its own dog food" since the editor itself is one of the most complex users of Godot's UI system.

This custom UI toolkit can't be used as a library, but you can still use Godot to create non-game applications by using the editor.

Godot uses the SCons build system. There are no plans to switch to a different build system in the near future. There are many reasons why we have chosen SCons over other alternatives. For example:

Godot can be compiled for a dozen different platforms: all PC platforms, all mobile platforms, many consoles, and WebAssembly.

Developers often need to compile for several of the platforms at the same time, or even different targets of the same platform. They can't afford reconfiguring and rebuilding the project each time. SCons can do this with no sweat, without breaking the builds.

SCons will never break a build no matter how many changes, configurations, additions, removals etc.

Godot's build process is not simple. Several files are generated by code (binders), others are parsed (shaders), and others need to offer customization (modules). This requires complex logic which is easier to write in an actual programming language (like Python) rather than using a mostly macro-based language only meant for building.

Godot's build process makes heavy use of cross-compiling tools. Each platform has a specific detection process, and all these must be handled as specific cases with special code written for each.

Please try to keep an open mind and get at least a little familiar with SCons if you are planning to build Godot yourself.

Like many other libraries (Qt as an example), Godot does not make use of STL (with a few exceptions such as threading primitives). We believe STL is a great general-purpose library, but we had special requirements for Godot.

STL templates create very large symbols, which results in huge debug binaries. We use few templates with very short names instead.

Most of our containers cater to special needs, like Vector, which uses copy on write and we use to pass data around, or the RID system, which requires O(1) access time for performance. Likewise, our hash map implementations are designed to integrate seamlessly with internal engine types.

Our containers have memory tracking built-in, which helps better track memory usage.

For large arrays, we use pooled memory, which can be mapped to either a preallocated buffer or virtual memory.

We use our custom String type, as the one provided by STL is too basic and lacks proper internationalization support.

Check out Godot's container types for alternatives.

We believe games should not crash, no matter what. If an unexpected situation happens, Godot will print an error (which can be traced even to script), but then it will try to recover as gracefully as possible and keep going.

Additionally, exceptions significantly increase the binary size for the executable and result in increased compile times.

Godot does not use an ECS and relies on inheritance instead. While there is no universally better approach, we found that using an inheritance-based approach resulted in better usability while still being fast enough for most use cases.

That said, nothing prevents you from making use of composition in your project by creating child Nodes with individual scripts. These nodes can then be added and removed at runtime to dynamically add and remove behaviors.

More information about Godot's design choices can be found in this article.

While Godot internally attempts to use cache coherency as much as possible, we believe users don't need to be forced to use DOD practices.

DOD is mostly a cache coherency optimization that can only provide significant performance improvements when dealing with dozens of thousands of objects which are processed every frame with little modification. That is, if you are moving a few hundred sprites or enemies per frame, DOD won't result in a meaningful improvement in performance. In such a case, you should consider a different approach to optimization.

The vast majority of games do not need this and Godot provides handy helpers to do the job for most cases when you do.

If a game needs to process such a large amount of objects, our recommendation is to use C++ and GDExtensions for performance-heavy tasks and GDScript (or C#) for the rest of the game.

See How to contribute.

See the corresponding page on the Godot website.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Godot release policy — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/release_policy.html

**Contents:**
- Godot release policy
- Godot versioning
- Release support timeline
- Which version should I use for a new project?
- Should I upgrade my project to use new engine versions?
- When is the next release out?
- What are the criteria for compatibility across engine versions?

Godot's release policy is in constant evolution. The description below provides a general idea of what to expect, but what will actually happen depends on the choices of core contributors and the needs of the community at a given time.

Godot loosely follows Semantic Versioning with a major.minor.patch versioning system, albeit with an interpretation of each term adapted to the complexity of a game engine:

The major version is incremented when major compatibility breakages happen which imply significant porting work to move projects from one major version to another.

For example, porting Godot projects from Godot 3.x to Godot 4.x requires running the project through a conversion tool, and then performing a number of further adjustments manually for what the tool could not do automatically.

The minor version is incremented for feature releases that do not break compatibility in a major way. Minor compatibility breakage in very specific areas may happen in minor versions, but the vast majority of projects should not be affected or require significant porting work.

This is because Godot, as a game engine, covers many areas like rendering, physics, and scripting. Fixing bugs or implementing new features in one area might sometimes require changing a feature's behavior or modifying a class's interface, even if the rest of the engine API remains backwards compatible.

Upgrading to a new minor version is recommended for all users, but some testing is necessary to ensure that your project still behaves as expected.

The patch version is incremented for maintenance releases which focus on fixing bugs and security issues, implementing new requirements for platform support, and backporting safe usability enhancements. Patch releases are backwards compatible.

Patch versions may include minor new features which do not impact the existing API, and thus have no risk of impacting existing projects.

Updating to new patch versions is therefore considered safe and strongly recommended to all users of a given stable branch.

We call major.minor combinations stable branches. Each stable branch starts with a major.minor release (without the 0 for patch) and is further developed for maintenance releases in a Git branch of the same name (for example patch updates for the 4.0 stable branch are developed in the 4.0 Git branch).

Stable branches are supported at least until the next stable branch is released and has received its first patch update. In practice, we support stable branches on a best effort basis for as long as they have active users who need maintenance updates.

Whenever a new major version is released, we make the previous stable branch a long-term supported release, and do our best to provide fixes for issues encountered by users of that branch who cannot port complex projects to the new major version. This was the case for the 2.1 branch, and is the case for the 3.x branch.

In a given minor release series, only the latest patch release receives support. If you experience an issue using an older patch release, please upgrade to the latest patch release of that series and test again before reporting an issue on GitHub.

Development. Receives new features, usability and performance improvements, as well as bug fixes, while under development.

Receives fixes for bugs and security issues, as well as patches that enable platform support.

Receives fixes for bugs and security issues, as well as patches that enable platform support.

Receives fixes for security and platform support issues only.

No longer supported (last update: 4.1.4).

No longer supported (last update: 4.0.4).

Beta. Receives new features, usability and performance improvements, as well as bug fixes, while under development.

Receives fixes for bugs and security issues, as well as patches that enable platform support.

Receives fixes for security and platform support issues only.

No longer supported (last update: 3.4.5).

No longer supported (last update: 3.3.4).

No longer supported (last update: 3.2.3).

No longer supported (last update: 3.1.2).

No longer supported (last update: 3.0.6).

No longer supported (last update: 2.1.6).

No longer supported (last update: 2.0.4.1).

Legend: Full support – Partial support – No support (end of life) – Development version

Pre-release Godot versions aren't intended to be used in production and are provided for testing purposes only.

See Upgrading from Godot 3 to Godot 4 for instructions on migrating a project from Godot 3.x to 4.x.

We recommend using Godot 4.x for new projects, as the Godot 4.x series will be supported long after 3.x stops receiving updates in the future. One caveat is that a lot of third-party documentation hasn't been updated for Godot 4.x yet. If you have to follow a tutorial designed for Godot 3.x, we recommend keeping Upgrading from Godot 3 to Godot 4 open in a separate tab to check which methods have been renamed (if you get a script error while trying to use a specific node or method that was renamed in Godot 4.x).

If your project requires a feature that is missing in 4.x (such as GLES2/WebGL 1.0), you should use Godot 3.x for a new project instead.

Upgrading software while working on a project is inherently risky, so consider whether it's a good idea for your project before attempting an upgrade. Also, make backups of your project or use version control to prevent losing data in case the upgrade goes wrong.

That said, we do our best to keep minor and especially patch releases compatible with existing projects.

The general recommendation is to upgrade your project to follow new patch releases, such as upgrading from 4.0.2 to 4.0.3. This ensures you get bug fixes, security updates and platform support updates (which is especially important for mobile platforms). You also get continued support, as only the last patch release receives support on official community platforms.

For minor releases, you should determine whether it's a good idea to upgrade on a case-by-case basis. We've made a lot of effort in making the upgrade process as seamless as possible, but some breaking changes may be present in minor releases, along with a greater risk of regressions. Some fixes included in minor releases may also change a class' expected behavior as required to fix some bugs. This is especially the case in classes marked as experimental in the documentation.

Major releases bring a lot of new functionality, but they also remove previously existing functionality and may raise hardware requirements. They also require much more work to upgrade to compared to minor releases. As a result, we recommend sticking with the major release you've started your project with if you are happy with how your project currently works. For example, if your project was started with 3.5, we recommend upgrading to 3.5.2 and possibly 3.6 in the future, but not to 4.0+, unless your project really needs the new features that come with 4.0+.

While Godot contributors aren't working under any deadlines, we strive to publish minor releases relatively frequently.

In particular, after the very long release cycle for 4.0, we are pivoting to a faster-paced development workflow, 4.1 released 4 months after 4.0, and 4.2 released 4 months after 4.1.

Frequent minor releases will enable us to ship new features faster (possibly as experimental), get user feedback quickly, and iterate to improve those features and their usability. Likewise, the general user experience will be improved more steadily with a faster path to the end users.

Maintenance (patch) releases are released as needed with potentially very short development cycles, to provide users of the current stable branch with the latest bug fixes for their production needs.

There is currently no planned release date for the next 3.x minor version, 3.7. The current stable release, 3.6, may be the last stable branch of Godot 3.x. Godot 3.x is supported on a best-effort basis, as long as contributors continue to maintain it.

This section is intended to be used by contributors to determine which changes are safe for a given release. The list is not exhaustive; it only outlines the most common situations encountered during Godot's development.

The following changes are acceptable in patch releases:

Fixing a bug in a way that has no major negative impact on most projects, such as a visual or physics bug. Godot's physics engine is not deterministic, so physics bug fixes are not considered to break compatibility. If fixing a bug has a negative impact that could impact a lot of projects, it should be made optional (e.g. using a project setting or separate method).

Adding a new optional parameter to a method.

Small-scale editor usability tweaks.

Note that we tend to be more conservative with the fixes we allow in each subsequent patch release. For instance, 4.0.1 may receive more impactful fixes than 4.0.4 would.

The following changes are acceptable in minor releases, but not patch releases:

Significant new features.

Renaming a method parameter. In C#, method parameters can be passed by name (but not in GDScript). As a result, this can break some projects that use C#.

Deprecating a method, member variable, or class. This is done by adding a deprecated flag to its class reference, which will show up in the editor. When a method is marked as deprecated, it's slated to be removed in the next major release.

Changes that affect the default project theme's visuals.

Bug fixes which significantly change the behavior or the output, with the aim to meet user expectations better. In comparison, in patch releases, we may favor keeping a buggy behavior so we don't break existing projects which likely already rely on the bug or use a workaround.

Performance optimizations that result in visual changes.

The following changes are considered compatibility-breaking and can only be performed in a new major release:

Renaming or removing a method, member variable, or class.

Modifying a node's inheritance tree by making it inherit from a different class.

Changing the default value of a project setting value in a way that affects existing projects. To only affect new projects, the project manager should write a modified project.godot instead.

Since Godot 5.0 hasn't been branched off yet, we currently discourage making compatibility-breaking changes of this kind.

When modifying a method's signature in any fashion (including adding an optional parameter), a GDExtension compatibility method must be created. This ensures that existing GDExtensions continue to work across patch and minor releases, so that users don't have to recompile them. See Handling compatibility breakages for more information.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Introduction — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/introduction.html

**Contents:**
- Introduction
- Before you start
- About Godot Engine
- Organization of the documentation
- About this documentation

Welcome to the official documentation of Godot Engine, the free and open source community-driven 2D and 3D game engine! Behind this mouthful, you will find a powerful yet user-friendly tool that you can use to develop any kind of game, for any platform and with no usage restriction whatsoever.

This page gives a broad overview of the engine and of this documentation, so that you know where to start if you are a beginner or where to look if you need information on a specific feature.

The Tutorials and resources page lists video tutorials contributed by the community. If you prefer video to text, consider checking them out. Otherwise, Getting Started is a great starting point.

In case you have trouble with one of the tutorials or your project, you can find help on the various Community channels, especially the Godot Discord community and Forum.

A game engine is a complex tool and difficult to present in a few words. Here's a quick synopsis, which you are free to reuse if you need a quick write-up about Godot Engine:

Godot Engine is a feature-packed, cross-platform game engine to create 2D and 3D games from a unified interface. It provides a comprehensive set of common tools, so that users can focus on making games without having to reinvent the wheel. Games can be exported with one click to a number of platforms, including the major desktop platforms (Linux, macOS, Windows), mobile platforms (Android, iOS), as well as Web-based platforms and consoles.

Godot is completely free and open source under the permissive MIT license. No strings attached, no royalties, nothing. Users' games are theirs, down to the last line of engine code. Godot's development is fully independent and community-driven, empowering users to help shape their engine to match their expectations. It is supported by the Godot Foundation not-for-profit.

This documentation is organized into several sections:

About contains this introduction as well as information about the engine, its history, its licensing, authors, etc. It also contains the Frequently asked questions.

Getting Started contains all necessary information on using the engine to make games. It starts with the Introduction section which should be the entry point for all new users. This is the best place to start if you're new!

The Manual can be read or referenced as needed, in any order. It contains feature-specific tutorials and documentation.

Engine details contains sections intended for advanced users and contributors, with information on compiling the engine, working on the editor, or developing C++ modules.

Community is dedicated to the life of Godot's community and contains a list of recommended third-party tutorials and materials outside of this documentation. It also provides details on the Asset Library. It also used to list Godot communities, which are now listed on the Godot website.

Finally, the Class reference documents the full Godot API, also available directly within the engine's script editor. You can find information on all classes, functions, signals and so on here.

In addition to this documentation, you may also want to take a look at the various Godot demo projects.

Members of the Godot Engine community continuously write, correct, edit, and improve this documentation. We are always looking for more help. You can also contribute by opening Github issues or translating the documentation into your language. If you are interested in helping, see How to contribute and Writing documentation, or get in touch with the Documentation team on Godot Contributors Chat.

All documentation content is licensed under the permissive Creative Commons Attribution 3.0 (CC BY 3.0) license, with attribution to "Juan Linietsky, Ariel Manzur, and the Godot Engine community" unless otherwise noted.

Have fun reading and making games with Godot Engine!

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## List of features — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/list_of_features.html

**Contents:**
- List of features
- Platforms
- Editor
- Rendering
- 2D graphics
- 2D tools
- 2D physics
- 3D graphics
- 3D tools
- 3D physics

This page aims to list all features currently supported by Godot.

This page lists features supported by the current stable version of Godot. Some of these features are not available in the 3.x release series.

See System requirements for hardware and software version requirements.

Can run both the editor and exported projects:

Windows (x86 and ARM, 64-bit and 32-bit).

macOS (x86 and ARM, 64-bit only).

Linux (x86 and ARM, 64-bit and 32-bit).

Binaries are statically linked and can run on any distribution if compiled on an old enough base distribution.

Official binaries are compiled using the Godot Engine buildroot, allowing for binaries that work across common Linux distributions.

Android (editor support is experimental).

Web browsers. Experimental in 4.0, using Godot 3.x is recommended instead when targeting HTML5.

Linux supports rv64 (RISC-V), ppc64 & ppc32 (PowerPC), and loongarch64. However you must compile the editor for that platform (as well as export templates) yourself, no official downloads are currently provided. RISC-V compiling instructions can be found on the Compiling for Linux, *BSD page.

Runs exported projects:

Godot aims to be as platform-independent as possible and can be ported to new platforms with relative ease.

Projects written in C# using Godot 4 currently cannot be exported to the web platform. To use C# on that platform, consider Godot 3 instead. Android and iOS platform support is available as of Godot 4.2, but is experimental and some limitations apply.

Built-in script editor.

Support for external script editors such as Visual Studio Code or Vim.

Support for debugging in threads is available since 4.2.

Visual profiler with CPU and GPU time indications for each step of the rendering pipeline.

Performance monitoring tools, including custom performance monitors.

Live script reloading.

Changes will reflect in the editor and will be kept after closing the running project.

Changes won't reflect in the editor and won't be kept after closing the running project.

Live camera replication.

Move the in-editor camera and see the result in the running project.

Built-in offline class reference documentation.

Use the editor in dozens of languages contributed by the community.

Editor plugins can be downloaded from the asset library to extend editor functionality.

Create your own plugins using GDScript to add new features or speed up your workflow.

Download projects from the asset library in the Project Manager and import them directly.

Godot 4 includes three renderers:

Forward+. The most advanced renderer, suited for desktop platforms only. Used by default on desktop platforms. This renderer uses Vulkan, Direct3D 12, or Metal as the rendering driver, and it uses the RenderingDevice backend.

Mobile. Fewer features, but renders simple scenes faster. Suited for mobile and desktop platforms. Used by default on mobile platforms. This renderer uses Vulkan, Direct3D 12, or Metal as the rendering driver, and it uses the RenderingDevice backend.

Compatibility, sometimes called GL Compatibility. The least advanced renderer, suited for low-end desktop and mobile platforms. Used by default on the web platform. This renderer uses OpenGL as the rendering driver.

See Overview of renderers for a detailed comparison of the rendering methods.

Sprite, polygon and line rendering.

High-level tools to draw lines and polygons such as Polygon2D and Line2D, with support for texturing.

AnimatedSprite2D as a helper for creating animated sprites.

Pseudo-3D support including preview in the editor.

2D lighting with normal maps and specular maps.

Point (omni/spot) and directional 2D lights.

Hard or soft shadows (adjustable on a per-light basis).

Custom shaders can access a real-time SDF representation of the 2D scene based on LightOccluder2D nodes, which can be used for improved 2D lighting effects including 2D global illumination.

Font rendering using bitmaps, rasterization using FreeType or multi-channel signed distance fields (MSDF).

Bitmap fonts can be exported using tools like BMFont, or imported from images (for fixed-width fonts only).

Dynamic fonts support monochrome fonts as well as colored fonts (e.g. for emoji). Supported formats are TTF, OTF, WOFF1 and WOFF2.

Dynamic fonts support optional font outlines with adjustable width and color.

Dynamic fonts support variable fonts and OpenType features including ligatures.

Dynamic fonts support simulated bold and italic when the font file lacks those styles.

Dynamic fonts support oversampling to keep fonts sharp at higher resolutions.

Dynamic fonts support subpixel positioning to make fonts crisper at low sizes.

Dynamic fonts support LCD subpixel optimizations to make fonts even crisper at low sizes.

Signed distance field fonts can be scaled at any resolution without requiring re-rasterization. Multi-channel usage makes SDF fonts scale down to lower sizes better compared to monochrome SDF fonts.

GPU-based particles with support for custom particle shaders.

Optional 2D HDR rendering for better glow capabilities.

TileMaps for 2D tile-based level design.

2D camera with built-in smoothing and drag margins.

Path2D node to represent a path in 2D space.

Can be drawn in the editor or generated procedurally.

PathFollow2D node to make nodes follow a Path2D.

2D geometry helper class.

Animatable bodies (for objects moving only by script or animation, such as doors and platforms).

Areas to detect bodies entering or leaving it.

Built-in shapes: line, box, circle, capsule, world boundary (infinite plane).

Collision polygons (can be drawn manually or generated from a sprite in the editor).

HDR rendering with sRGB.

Perspective, orthographic and frustum-offset cameras.

When using the Forward+ renderer, a depth prepass is used to improve performance in complex scenes by reducing the cost of overdraw.

Variable rate shading on supported GPUs in Forward+ and Mobile.

Physically-based rendering (built-in material features):

Follows the Disney PBR model.

Supports Burley, Lambert, Lambert Wrap (half-Lambert) and Toon diffuse shading modes.

Supports Schlick-GGX, Toon and Disabled specular shading modes.

Uses a roughness-metallic workflow with support for ORM textures.

Uses horizon specular occlusion (Filament model) to improve material appearance.

Parallax/relief mapping with automatic level of detail based on distance.

Detail mapping for the albedo and normal maps.

Sub-surface scattering and transmittance.

Screen-space refraction with support for material roughness (resulting in blurry refraction).

Proximity fade (soft particles) and distance fade.

Distance fade can use alpha blending or dithering to avoid going through the transparent pipeline.

Dithering can be determined on a per-pixel or per-object basis.

Directional lights (sun/moon). Up to 4 per scene.

Omnidirectional lights.

Spot lights with adjustable cone angle and attenuation.

Specular, indirect light, and volumetric fog energy can be adjusted on a per-light basis.

Adjustable light "size" for fake area lights (will also make shadows blurrier).

Optional distance fade system to fade distant lights and their shadows, improving performance.

When using the Forward+ renderer (default on desktop), lights are rendered with clustered forward optimizations to decrease their individual cost. Clustered rendering also lifts any limits on the number of lights that can be used on a mesh.

When using the Mobile renderer, up to 8 omni lights and 8 spot lights can be displayed per mesh resource. Baked lighting can be used to overcome this limit if needed.

DirectionalLight: Orthogonal (fastest), PSSM 2-split and 4-split. Supports blending between splits.

OmniLight: Dual paraboloid (fast) or cubemap (slower but more accurate). Supports colored projector textures in the form of panoramas.

SpotLight: Single texture. Supports colored projector textures.

Shadow normal offset bias and shadow pancaking to decrease the amount of visible shadow acne and peter-panning.

PCSS-like shadow blur based on the light size and distance from the surface the shadow is cast on.

Adjustable shadow blur on a per-light basis.

Global illumination with indirect lighting:

Baked lightmaps (fast, but can't be updated at runtime).

Supports baking indirect light only or baking both direct and indirect lighting. The bake mode can be adjusted on a per-light basis to allow for hybrid light baking setups.

Supports lighting dynamic objects using automatic and manually placed probes.

Optionally supports directional lighting and rough reflections based on spherical harmonics.

Lightmaps are baked on the GPU using compute shaders (much faster compared to CPU lightmapping). Baking can only be performed from the editor, not in exported projects.

Supports GPU-based denoising with JNLM, or CPU/GPU-based denoising with OIDN.

Voxel-based GI probes. Supports dynamic lights and dynamic occluders, while also supporting reflections. Requires a fast baking step which can be performed in the editor or at runtime (including from an exported project).

Signed-distance field GI designed for large open worlds. Supports dynamic lights, but not dynamic occluders. Supports reflections. No baking required.

Screen-space indirect lighting (SSIL) at half or full resolution. Fully real-time and supports any kind of emissive light source (including decals).

VoxelGI and SDFGI use a deferred pass to allow for rendering GI at half resolution to improve performance (while still having functional MSAA support).

Voxel-based reflections (when using GI probes) and SDF-based reflections (when using signed distance field GI). Voxel-based reflections are visible on transparent surfaces, while rough SDF-based reflections are visible on transparent surfaces.

Fast baked reflections or slow real-time reflections using ReflectionProbe. Parallax box correction can optionally be enabled.

Screen-space reflections with support for material roughness.

Reflection techniques can be mixed together for greater accuracy or scalability.

When using the Forward+ renderer (default on desktop), reflection probes are rendered with clustered forward optimizations to decrease their individual cost. Clustered rendering also lifts any limits on the number of reflection probes that can be used on a mesh.

When using the Mobile renderer, up to 8 reflection probes can be displayed per mesh resource. When using the Compatibility renderer, up to 2 reflection probes can be displayed per mesh resource.

Supports albedo, emissive, ORM, and normal mapping.

Texture channels are smoothly overlaid on top of the underlying material, with support for normal/ORM-only decals.

Support for normal fade to fade the decal depending on its incidence angle.

Does not rely on runtime mesh generation. This means decals can be used on complex skinned meshes with no performance penalty, even if the decal moves every frame.

Support for nearest, bilinear, trilinear or anisotropic texture filtering (configured globally).

Optional distance fade system to fade distant decals, improving performance.

When using the Forward+ renderer (default on desktop), decals are rendered with clustered forward optimizations to decrease their individual cost. Clustered rendering also lifts any limits on the number of decals that can be used on a mesh.

When using the Mobile renderer, up to 8 decals can be displayed per mesh resource.

Panorama sky (using an HDRI).

Procedural sky and Physically-based sky that respond to the DirectionalLights in the scene.

Support for custom sky shaders, which can be animated.

The radiance map used for ambient and specular light can be updated in real-time depending on the quality settings chosen.

Exponential depth fog.

Exponential height fog.

Support for automatic fog color depending on the sky color (aerial perspective).

Support for sun scattering in the fog.

Support for controlling how much fog rendering should affect the sky, with separate controls for traditional and volumetric fog.

Support for making specific materials ignore fog.

Global volumetric fog that reacts to lights and shadows.

Volumetric fog can take indirect light into account when using VoxelGI or SDFGI.

Fog volume nodes that can be placed to add fog to specific areas (or remove fog from specific areas). Supported shapes include box, ellipse, cone, cylinder, and 3D texture-based density maps.

Each fog volume can have its own custom shader.

Can be used together with traditional fog.

GPU-based particles with support for subemitters (2D + 3D), trails (2D + 3D), attractors (3D only) and collision (2D + 3D).

3D particle attractor shapes supported: box, sphere and 3D vector fields.

3D particle collision shapes supported: box, sphere, baked signed distance field and real-time heightmap (suited for open world weather effects).

2D particle collision is handled using a signed distance field generated in real-time based on LightOccluder2D nodes in the scene.

Trails can use the built-in ribbon trail and tube trail meshes, or custom meshes with skeletons.

Support for custom particle shaders with manual emission.

Tonemapping (Linear, Reinhard, Filmic, ACES, AgX).

Automatic exposure adjustments based on viewport brightness (and manual exposure override).

Near and far depth of field with adjustable bokeh simulation (box, hexagon, circle).

Screen-space ambient occlusion (SSAO) at half or full resolution.

Glow/bloom with optional bicubic upscaling and several blend modes available: Screen, Soft Light, Add, Replace, Mix.

Glow can have a colored dirt map texture, acting as a lens dirt effect.

Glow can be used as a screen-space blur effect.

Color correction using a one-dimensional ramp or a 3D LUT texture.

Roughness limiter to reduce the impact of specular aliasing.

Brightness, contrast and saturation adjustments.

Nearest, bilinear, trilinear or anisotropic filtering.

Filtering options are defined on a per-use basis, not a per-texture basis.

Basis Universal (slow, but results in smaller files).

BPTC for high-quality compression (not supported on macOS).

ETC2 (not supported on macOS).

S3TC (not supported on mobile/Web platforms).

Temporal antialiasing (TAA).

AMD FidelityFX Super Resolution 2.2 antialiasing (FSR2), which can be used at native resolution as a form of high-quality temporal antialiasing.

Multi-sample antialiasing (MSAA), for both 2D antialiasing and 3D antialiasing.

Fast approximate antialiasing (FXAA).

Super-sample antialiasing (SSAA) using bilinear 3D scaling and a 3D resolution scale above 1.0.

Alpha antialiasing, MSAA alpha to coverage and alpha hashing on a per-material basis.

Support for rendering 3D at a lower resolution while keeping 2D rendering at the original scale. This can be used to improve performance on low-end systems or improve visuals on high-end systems.

Resolution scaling uses bilinear filtering, AMD FidelityFX Super Resolution 1.0 (FSR1) or AMD FidelityFX Super Resolution 2.2 (FSR2).

Texture mipmap LOD bias is adjusted automatically to improve quality at lower resolution scales. It can also be modified with a manual offset.

Most effects listed above can be adjusted for better performance or to further improve quality. This can be helpful when using Godot for offline rendering.

Built-in meshes: cube, cylinder/cone, (hemi)sphere, prism, plane, quad, torus, ribbon, tube.

GridMaps for 3D tile-based level design.

Constructive solid geometry (intended for prototyping).

Tools for procedural geometry generation.

Path3D node to represent a path in 3D space.

Can be drawn in the editor or generated procedurally.

PathFollow3D node to make nodes follow a Path3D.

3D geometry helper class.

Support for exporting the current scene as a glTF 2.0 file, both from the editor and at runtime from an exported project.

Animatable bodies (for objects moving only by script or animation, such as doors and platforms).

Vehicle bodies (intended for arcade physics, not simulation).

Areas to detect bodies entering or leaving it.

Built-in shapes: cuboid, sphere, capsule, cylinder, world boundary (infinite plane).

Generate triangle collision shapes for any mesh from the editor.

Generate one or several convex collision shapes for any mesh from the editor.

2D: Custom vertex, fragment, and light shaders.

3D: Custom vertex, fragment, light, and sky shaders.

Text-based shaders using a shader language inspired by GLSL.

Visual shader editor.

Support for visual shader plugins.

Object-oriented design pattern with scripts extending nodes.

Signals and groups for communicating between scripts.

Support for cross-language scripting.

Many 2D, 3D and 4D linear algebra data types such as vectors and transforms.

High-level interpreted language with optional static typing.

Syntax inspired by Python. However, GDScript is not based on Python.

Syntax highlighting is provided on GitHub.

Use threads to perform asynchronous actions or make use of multiple processor cores.

Packaged in a separate binary to keep file sizes and dependencies down.

Supports .NET 8 and higher.

Full support for the C# 12.0 syntax and features.

Supports Windows, Linux, and macOS. Since Godot 4.2, experimental support for Android and iOS is also available.

On the iOS platform only some architectures are supported: arm64.

The web platform is currently unsupported. To use C# on that platform, consider Godot 3 instead.

Using an external editor is recommended to benefit from IDE functionality.

GDExtension (C, C++, Rust, D, ...):

When you need it, link to native libraries for higher performance and third-party integrations.

For scripting game logic, GDScript or C# are recommended if their performance is suitable.

Official GDExtension bindings for C and C++.

Use any build system and language features you wish.

Actively developed GDExtension bindings for D, Swift, and Rust bindings provided by the community. (Some of these bindings may be experimental and not production-ready).

Mono, stereo, 5.1 and 7.1 output.

Non-positional and positional playback in 2D and 3D.

Optional Doppler effect in 2D and 3D.

Support for re-routable audio buses and effects with dozens of effects included.

Support for polyphony (playing several sounds from a single AudioStreamPlayer node).

Support for random volume and pitch.

Support for real-time pitch scaling.

Support for sequential/random sample selection, including repetition prevention when using random sample selection.

Listener2D and Listener3D nodes to listen from a position different than the camera.

Support for procedural audio generation.

Audio input to record microphones.

No support for MIDI output yet.

Linux: PulseAudio or ALSA.

Support for custom import plugins.

Images: See Importing images.

WAV with optional IMA-ADPCM compression.

3D scenes: See Importing 3D scenes.

glTF 2.0 (recommended).

.blend (by calling Blender's glTF export functionality transparently).

FBX (by calling FBX2glTF transparently).

Wavefront OBJ (static scenes only, can be loaded directly as a mesh or imported as a 3D scene).

Support for loading glTF 2.0 scenes at runtime, including from an exported project.

3D meshes use Mikktspace to generate tangents on import, which ensures consistency with other 3D applications such as Blender.

Input mapping system using hardcoded input events or remappable input actions.

Axis values can be mapped to two different actions with a configurable deadzone.

Use the same code to support both keyboards and gamepads.

Keys can be mapped in "physical" mode to be independent of the keyboard layout.

The mouse cursor can be visible, hidden, captured or confined within the window.

When captured, raw input will be used on Windows and Linux to sidestep the OS' mouse acceleration settings.

Gamepad input (up to 8 simultaneous controllers).

Pen/tablet input with pressure support.

A* algorithm in 2D and 3D.

Navigation meshes with dynamic obstacle avoidance in 2D and 3D.

Generate navigation meshes from the editor or at runtime (including from an exported project).

Low-level TCP networking using StreamPeer and TCPServer.

Low-level UDP networking using PacketPeer and UDPServer.

Low-level HTTP requests using HTTPClient.

High-level HTTP requests using HTTPRequest.

Supports HTTPS out of the box using bundled certificates.

High-level multiplayer API using UDP and ENet.

Automatic replication using remote procedure calls (RPCs).

Supports unreliable, reliable and ordered transfers.

WebSocket client and server, available on all platforms.

WebRTC client and server, available on all platforms.

Support for UPnP to sidestep the requirement to forward ports when hosting a server behind a NAT.

Full support for Unicode including emoji.

Store localization strings using CSV or gettext.

Support for generating gettext POT and PO files from the editor.

Use localized strings in your project automatically in GUI elements or by using the tr() function.

Support for pluralization and translation contexts when using gettext translations.

Support for bidirectional typesetting, text shaping and OpenType localized forms.

Automatic UI mirroring for right-to-left locales.

Support for pseudolocalization to test your project for i18n-friendliness.

Spawn multiple independent windows within a single process.

Move, resize, minimize, and maximize windows spawned by the project.

Change the window title and icon.

Request attention (will cause the title bar to blink on most platforms).

Uses borderless fullscreen by default on Windows for fast alt-tabbing, but can optionally use exclusive fullscreen to reduce input lag.

Borderless windows (fullscreen or non-fullscreen).

Ability to keep a window always on top.

Global menu integration on macOS.

Execute commands in a blocking or non-blocking manner (including running multiple instances of the same project).

Open file paths and URLs using default or custom protocol handlers (if registered on the system).

Parse custom command line arguments.

Any Godot binary (editor or exported project) can be used as a headless server by starting it with the --headless command line argument. This allows running the engine without a GPU or display server.

In-app purchases on Android and iOS.

Support for advertisements using third-party modules.

Out of the box support for OpenXR.

Including support for popular desktop headsets like the Valve Index, WMR headsets, and Quest over Link.

Support for Android-based headsets using OpenXR through a plugin.

Including support for popular stand alone headsets like the Meta Quest 1/2/3 and Pro, Pico 4, Magic Leap 2, and Lynx R1.

Out of the box limited support for visionOS Apple headsets.

Currently only exporting an application for use on a flat plane within the headset is supported. Immersive experiences are not supported.

Other devices supported through an XR plugin structure.

Various advanced toolkits are available that implement common features required by XR applications.

Godot's GUI is built using the same Control nodes used to make games in Godot. The editor UI can easily be extended in many ways using add-ons.

Checkboxes, check buttons, radio buttons.

Text entry using LineEdit (single line) and TextEdit (multiple lines). TextEdit also supports code editing features such as displaying line numbers and syntax highlighting.

Dropdown menus using PopupMenu and OptionButton.

RichTextLabel for text formatted using BBCode, with support for animated custom effects.

Trees (can also be used to represent tables).

Color picker with RGB and HSV modes.

Controls can be rotated and scaled.

Anchors to keep GUI elements in a specific corner, edge or centered.

Containers to place GUI elements automatically following certain rules.

Flow layouts (similar to autowrapping text).

Margin, centered and aspect ratio layouts.

Draggable splitter layouts.

Scale to multiple resolutions using the canvas_items or viewport stretch modes.

Support any aspect ratio using anchors and the expand stretch aspect.

Built-in theme editor.

Generate a theme based on the current editor theme settings.

Procedural vector-based theming using StyleBoxFlat.

Supports rounded/beveled corners, drop shadows, per-border widths and antialiasing.

Texture-based theming using StyleBoxTexture.

Godot's small distribution size can make it a suitable alternative to frameworks like Electron or Qt.

Direct kinematics and inverse kinematics.

Support for animating any property with customizable interpolation.

Support for calling methods in animation tracks.

Support for playing sounds in animation tracks.

Support for Bézier curves in animation.

Scenes and resources can be saved in text-based or binary formats.

Text-based formats are human-readable and more friendly to version control.

Binary formats are faster to save/load for large scenes/resources.

Read and write text or binary files using FileAccess.

Can optionally be compressed or encrypted.

Read and write JSON files.

Read and write INI-style configuration files using ConfigFile.

Can (de)serialize any Godot datatype, including Vector2/3, Color, ...

Read XML files using XMLParser.

Load and save images, audio/video, fonts and ZIP archives in an exported project without having to go through Godot's import system.

Pack game data into a PCK file (custom format optimized for fast seeking), into a ZIP archive, or directly into the executable for single-file distribution.

Export additional PCK files that can be read by the engine to support mods and DLCs.

Video playback with built-in support for Ogg Theora.

Movie Maker mode to record videos from a running project with synchronized audio and perfect frame pacing.

Low-level access to servers which allows bypassing the scene tree's overhead when needed.

Command line interface for automation.

Export and deploy projects using continuous integration platforms.

Shell completion scripts are available for Bash, zsh and fish.

Print colored text to standard output on all platforms using print_rich.

The editor can detect features used in a project and create a compilation profile, which can be used to create smaller export template binaries with unneeded features disabled.

Support for C++ modules statically linked into the engine binary.

Most built-in modules can be disabled at compile-time to reduce binary size in custom builds. See Optimizing a build for size for details.

Engine and editor written in C++17.

Can be compiled using GCC, Clang and MSVC. MinGW is also supported.

Friendly towards packagers. In most cases, system libraries can be used instead of the ones provided by Godot. The build system doesn't download anything. Builds can be fully reproducible.

Licensed under the permissive MIT license.

Open development process with contributions welcome.

The Godot proposals repository lists features that have been requested by the community and may be implemented in future Godot releases.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## System requirements — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/about/system_requirements.html

**Contents:**
- System requirements
- Godot editor
  - Desktop or laptop PC - Minimum
  - Mobile device (smartphone/tablet) - Minimum
  - Desktop or laptop PC - Recommended
  - Mobile device (smartphone/tablet) - Recommended
- Exported Godot project
  - Desktop or laptop PC - Minimum
  - Mobile device (smartphone/tablet) - Minimum
  - Desktop or laptop PC - Recommended

This page contains system requirements for the editor and exported projects. These specifications are given for informative purposes only, but they can be referred to if you're looking to build or upgrade a system to use Godot on.

These are the minimum specifications required to run the Godot editor and work on a simple 2D or 3D project:

Windows: x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support, ARMv8 CPU

Example: Intel Core 2 Duo E8200, AMD FX-4100, Snapdragon X Elite

macOS: x86_64 or ARM CPU (Apple Silicon)

Example: Intel Core 2 Duo SU9400, Apple M1

Linux: x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support, ARMv7 or ARMv8 CPU

Example: Intel Core 2 Duo E8200, AMD FX-4100, Raspberry Pi 4

Forward+ renderer: Integrated graphics with full Vulkan 1.0 support

Example: Intel HD Graphics 510 (Skylake), AMD Radeon R5 Graphics (Kaveri)

Mobile renderer: Integrated graphics with full Vulkan 1.0 support

Example: Intel HD Graphics 510 (Skylake), AMD Radeon R5 Graphics (Kaveri)

Compatibility renderer: Integrated graphics with full OpenGL 3.3 support

Example: Intel HD Graphics 2500 (Ivy Bridge), AMD Radeon R5 Graphics (Kaveri)

200 MB (used for the executable, project files and cache). Exporting projects requires downloading export templates separately (1.3 GB after installation).

Native editor: Windows 10, macOS 10.13 (Compatibility) or macOS 10.15 (Forward+/Mobile), Linux distribution released after 2018

Web editor: Recent versions of mainstream browsers: Firefox and derivatives (including ESR), Chrome and Chromium derivatives, Safari and WebKit derivatives.

If your x86_64 CPU does not support SSE4.2, you can still run the 32-bit Godot executable which only has a SSE2 requirement (all x86_64 CPUs support SSE2).

While supported on Linux, we have no official minimum requirements for running on rv64 (RISC-V), ppc64 & ppc32 (PowerPC), and loongarch64. In addition you must compile the editor for that platform (as well as export templates) yourself, no official downloads are currently provided. RISC-V compiling instructions can be found on the Compiling for Linux, *BSD page.

Android: SoC with any 32-bit or 64-bit ARM or x86 CPU

Example: Qualcomm Snapdragon 430, Samsung Exynos 5 Octa 5430

iOS: Cannot run the editor

Forward+ renderer: SoC featuring GPU with full Vulkan 1.0 support

Example: Qualcomm Adreno 505, Mali-G71 MP2

Mobile renderer: SoC featuring GPU with full Vulkan 1.0 support

Example: Qualcomm Adreno 505, Mali-G71 MP2

Compatibility renderer: SoC featuring GPU with full OpenGL ES 3.0 support

Example: Qualcomm Adreno 306, Mali-T628 MP6

200 MB (used for the executable, project files and cache) Exporting projects requires downloading export templates separately (1.3 GB after installation)

Native editor: Android 6.0 (Compatibility) or Android 9.0 (Forward+/Mobile)

Web editor: Recent versions of mainstream browsers: Firefox and derivatives (including ESR), Chrome and Chromium derivatives, Safari and WebKit derivatives.

These are the recommended specifications to get a smooth experience with the Godot editor on a simple 2D or 3D project:

Windows: x86_64 CPU with SSE4.2 support, with 4 physical cores or more, ARMv8 CPU

Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Snapdragon X Elite

macOS: x86_64 or ARM CPU (Apple Silicon)

Example: Intel Core i5-8500, Apple M1

Linux: x86_64 CPU with SSE4.2 support, ARMv7 or ARMv8 CPU

Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Raspberry Pi 5 with overclocking

Forward+ renderer: Dedicated graphics with full Vulkan 1.2 support

Example: NVIDIA GeForce GTX 1050 (Pascal), AMD Radeon RX 460 (GCN 4.0)

Mobile renderer: Dedicated graphics with full Vulkan 1.2 support

Example: NVIDIA GeForce GTX 1050 (Pascal), AMD Radeon RX 460 (GCN 4.0)

Compatibility renderer: Dedicated graphics with full OpenGL 4.6 support

Example: NVIDIA GeForce GTX 650 (Kepler), AMD Radeon HD 7750 (GCN 1.0)

1.5 GB (used for the executable, project files, all export templates and cache)

Native editor: Windows 10, macOS 10.15, Linux distribution released after 2020

Web editor: Latest version of Firefox, Chrome, Edge, Safari, Opera

Android: SoC with 64-bit ARM or x86 CPU, with 3 "performance" cores or more

Example: Qualcomm Snapdragon 845, Samsung Exynos 9810

iOS: Cannot run the editor

Forward+ renderer: SoC featuring GPU with full Vulkan 1.2 support

Example: Qualcomm Adreno 630, Mali-G72 MP18

Mobile renderer: SoC featuring GPU with full Vulkan 1.2 support

Example: Qualcomm Adreno 630, Mali-G72 MP18

Compatibility renderer: SoC featuring GPU with full OpenGL ES 3.2 support

Example: Qualcomm Adreno 630, Mali-G72 MP18

1.5 GB (used for the executable, project files, all export templates and cache)

Native editor: Android 9.0

Web editor: Latest version of Firefox, Chrome, Edge, Safari, Opera, Samsung Internet

The requirements below are a baseline for a simple 2D or 3D project, with basic scripting and few visual flourishes. CPU, GPU, RAM and storage requirements will heavily vary depending on your project's scope, its renderer, viewport resolution and graphics settings chosen. Other programs running on the system while the project is running will also compete for resources, including RAM and video RAM.

It is strongly recommended to do your own testing on low-end hardware to make sure your project runs at the desired speed. To provide scalability for low-end hardware, you will also need to introduce a graphics options menu to your project.

These are the minimum specifications required to run a simple 2D or 3D project exported with Godot:

Windows: x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support, ARMv8 CPU

Example: Intel Core 2 Duo E8200, AMD FX-4100, Snapdragon X Elite

macOS: x86_64 or ARM CPU (Apple Silicon)

Example: Intel Core 2 Duo SU9400, Apple M1

Linux: x86_32 CPU with SSE2 support, x86_64 CPU with SSE4.2 support, ARMv7 or ARMv8 CPU

Example: Intel Core 2 Duo E8200, AMD FX-4100, Raspberry Pi 4

Forward+ renderer: Integrated graphics with full Vulkan 1.0 support, Metal 3 support (macOS) or Direct3D 12 (12_0 feature level) support (Windows)

Example: Intel HD Graphics 510 (Skylake), AMD Radeon R5 Graphics (Kaveri)

Mobile renderer: Integrated graphics with full Vulkan 1.0 support, Metal 3 support (macOS) or Direct3D 12 (12_0 feature level) support (Windows)

Example: Intel HD Graphics 510 (Skylake), AMD Radeon R5 Graphics (Kaveri)

Compatibility renderer: Integrated graphics with full OpenGL 3.3 support or Direct3D 11 support (Windows).

Example: Intel HD Graphics 2500 (Ivy Bridge), AMD Radeon R5 Graphics (Kaveri)

For native exports: 2 GB

For web exports: 4 GB

150 MB (used for the executable, project files and cache)

For native exports: Windows 10, macOS 10.13 (Compatibility), macOS 10.15 (Forward+/Mobile, Vulkan), macOS 13.0 (Forward+/Mobile, Metal), Linux distribution released after 2018

Web editor: Recent versions of mainstream browsers: Firefox and derivatives (including ESR), Chrome and Chromium derivatives, Safari and WebKit derivatives.

Android: SoC with any 32-bit or 64-bit ARM or x86 CPU

Example: Qualcomm Snapdragon 430, Samsung Exynos 5 Octa 5430

iOS: SoC with any 64-bit ARM CPU

Example: Apple A7 (iPhone 5S)

Forward+ renderer: SoC featuring GPU with full Vulkan 1.0 support, or Metal 3 support (iOS/iPadOS)

Example (Vulkan): Qualcomm Adreno 505, Mali-G71 MP2, Apple A12 (iPhone XR/XS)

Example (Metal): Apple A11 (iPhone 8/X)

Mobile renderer: SoC featuring GPU with full Vulkan 1.0 support, or Metal 3 support (iOS/iPadOS)

Example (Vulkan): Qualcomm Adreno 505, Mali-G71 MP2, Apple A12 (iPhone XR/XS)

Example (Metal): Apple A11 (iPhone 8/X)

Compatibility renderer: SoC featuring GPU with full OpenGL ES 3.0 support

Example: Qualcomm Adreno 306, Mali-T628 MP6, Apple A7 (iPhone 5S)

For native exports: 1 GB

For web exports: 2 GB

150 MB (used for the executable, project files and cache)

For native exports: Android 6.0 (Compatibility), Android 9.0 (Forward+/Mobile), iOS 12.0 (Forward+/Mobile, Vulkan), iOS 16.0 (Forward+/Mobile, Metal)

Web editor: Recent versions of mainstream browsers: Firefox and derivatives (including ESR), Chrome and Chromium derivatives, Safari and WebKit derivatives.

These are the recommended specifications to get a smooth experience with a simple 2D or 3D project exported with Godot:

Windows: x86_64 CPU with SSE4.2 support, with 4 physical cores or more, ARMv8 CPU

Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Snapdragon X Elite

macOS: x86_64 or ARM CPU (Apple Silicon)

Example: Intel Core i5-8500, Apple M1

Linux: x86_64 CPU with SSE4.2 support, with 4 physical cores or more, ARMv7 or ARMv8 CPU

Example: Intel Core i5-6600K, AMD Ryzen 5 1600, Raspberry Pi 5 with overclocking

Forward+ renderer: Dedicated graphics with full Vulkan 1.2 support, Metal 3 support (macOS), or Direct3D 12 (12_0 feature level) support (Windows)

Example: NVIDIA GeForce GTX 1050 (Pascal), AMD Radeon RX 460 (GCN 4.0)

Mobile renderer: Dedicated graphics with full Vulkan 1.2 support, Metal 3 support (macOS), or Direct3D 12 (12_0 feature level) support (Windows)

Example: NVIDIA GeForce GTX 1050 (Pascal), AMD Radeon RX 460 (GCN 4.0)

Compatibility renderer: Dedicated graphics with full OpenGL 4.6 support

Example: NVIDIA GeForce GTX 650 (Kepler), AMD Radeon HD 7750 (GCN 1.0)

For native exports: 4 GB

For web exports: 8 GB

150 MB (used for the executable, project files and cache)

For native exports: Windows 10, macOS 10.15 (Forward+/Mobile, Vulkan), macOS 13.0 (Forward+/Mobile, Metal), Linux distribution released after 2020

For web exports: Latest version of Firefox, Chrome, Edge, Safari, Opera

Android: SoC with 64-bit ARM or x86 CPU, with 3 "performance" cores or more

Example: Qualcomm Snapdragon 845, Samsung Exynos 9810

iOS: SoC with 64-bit ARM CPU

Example: Apple A14 (iPhone 12)

Forward+ renderer: SoC featuring GPU with full Vulkan 1.2 support, or Metal 3 support (iOS/iPadOS)

Example: Qualcomm Adreno 630, Mali-G72 MP18, Apple A14 (iPhone 12)

Mobile renderer: SoC featuring GPU with full Vulkan 1.2 support, or Metal 3 support (iOS/iPadOS)

Example: Qualcomm Adreno 630, Mali-G72 MP18, Apple A14 (iPhone 12)

Compatibility renderer: SoC featuring GPU with full OpenGL ES 3.2 support

Example: Qualcomm Adreno 630, Mali-G72 MP18, Apple A14 (iPhone 12)

For native exports: 2 GB

For web exports: 4 GB

150 MB (used for the executable, project files and cache)

For native exports: Android 9.0, iOS 14.1 (Forward+/Mobile, Vulkan), iOS 16.0 (Forward+/Mobile, Metal)

For web exports: Latest version of Firefox, Chrome, Edge, Safari, Opera, Samsung Internet

Godot doesn't use OpenGL/OpenGL ES extensions introduced after OpenGL 3.3/OpenGL ES 3.0, but GPUs supporting newer OpenGL/OpenGL ES versions generally have fewer driver issues.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---
