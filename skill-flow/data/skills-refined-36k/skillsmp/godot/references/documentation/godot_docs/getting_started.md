# Godot_Docs - Getting Started

**Pages:** 36

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

**Examples:**

Example 1 (gdscript):
```gdscript
func _ready():
    print("Hello world!")
```

Example 2 (gdscript):
```gdscript
public override void _Ready()
{
    GD.Print("Hello world!");
}
```

---

## Introduction — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/introduction/index.html

**Contents:**
- Introduction

This series will introduce you to Godot and give you an overview of its features.

In the following pages, you will get answers to questions such as "Is Godot for me?" or "What can I do with Godot?". We will then introduce the engine's most essential concepts, run you through the editor's interface, and give you tips to make the most of your time learning it.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Introduction to Godot — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/introduction/introduction_to_godot.html

**Contents:**
- Introduction to Godot
- What is Godot?
- What can the engine do?
- How does it work and look?
- Programming languages
- What do I need to know to use Godot?
- User-contributed notes

This article is here to help you figure out whether Godot might be a good fit for you. We will introduce some broad features of the engine to give you a feel for what you can achieve with it and answer questions such as "what do I need to know to get started?".

This is by no means an exhaustive overview. We will introduce many more features in this getting started series.

Godot is a general-purpose 2D and 3D game engine designed to support all sorts of projects. You can use it to create games or applications you can then release on desktop or mobile, as well as on the web.

You can also create console games with it, although you either need strong programming skills or a developer to port the game for you.

The Godot team can't provide an open source console export due to the licensing terms imposed by console manufacturers. Regardless of the engine you use, though, releasing games on consoles is always a lot of work. You can read more on that here: Console support in Godot.

Godot was initially developed in-house by an Argentinian game studio. Its development started in 2001, and the engine was rewritten and improved tremendously since its open source release in 2014.

Some examples of games created with Godot include Cassette Beasts, PVKK, and Usagi Shima. As for applications, the open source pixel art drawing program Pixelorama is powered by Godot, and so is the voxel RPG creator RPG in a Box. You can find many more examples in the Official Showcase.

PVKK: Planetenverteidigungskanonenkommandant

Godot comes with a fully-fledged game editor with integrated tools to answer the most common needs. It includes a code editor, an animation editor, a tilemap editor, a shader editor, a debugger, a profiler, and more.

The team strives to offer a feature-rich game editor with a consistent user experience. While there is always room for improvement, the user interface keeps getting refined.

Of course, if you prefer, you can work with external programs. We officially support importing 3D scenes designed in Blender and maintain plugins to code in VSCode and Emacs for GDScript and C#. We also support Visual Studio for C# on Windows.

Let's talk about the available programming languages.

You can code your games using GDScript, a Godot-specific and tightly integrated language with a lightweight syntax, or C#, which is popular in the games industry. These are the two main scripting languages we support.

With the GDExtension technology, you can also write gameplay or high-performance algorithms in C++ or other languages without recompiling the engine. You can use this technology to integrate third-party libraries and other Software Development Kits (SDK) in the engine.

Of course, you can also directly add modules and features to the engine, as it's completely free and open source.

Godot is a feature-packed game engine. With its thousands of features, there is a lot to learn. To make the most of it, you need good programming foundations. While we try to make the engine accessible, you will benefit a lot from knowing how to think like a programmer first.

Godot relies on the object-oriented programming paradigm. Being comfortable with concepts such as classes and objects will help you code efficiently in it.

If you are entirely new to programming, we recommend following the CS50 open courseware from Harvard University. It's a great free course that will teach you everything you need to know to be off to a good start. It will save you countless hours and hurdles learning any game engine afterward.

In CS50, you will learn multiple programming languages. Don't be afraid of that: programming languages have many similarities. The skills you learn with one language transfer well to others.

We will provide you with more Godot-specific learning resources in Learning new features.

In the next part, you will get an overview of the engine's essential concepts.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Learn to code with GDScript — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/introduction/learn_to_code_with_gdscript.html

**Contents:**
- Learn to code with GDScript
- Learn in your browser with the GDScript app
- User-contributed notes

In Godot, you can write code using the GDScript and C# programming languages.

If you are new to programming, we recommend starting with GDScript because we designed it to be simpler than all-purpose languages like C#. It will be both faster and easier to learn.

While GDScript is a language specific to Godot, the techniques you will learn with it will apply to other programming languages.

Note that it is completely normal for a programmer to learn and use multiple languages. Programming languages have more similarities than differences, so once you know one, you can learn another much faster.

To learn GDScript, you can use the app Learn GDScript From Zero. It is a complete beginner course with interactive practices you can do right in your browser.

Click here to access the app: Learn GDScript From Zero app

This app is an open-source project. To report bugs or contribute, head to the app's source code repository: GitHub repository.

In the next part, you will get an overview of the engine's essential concepts.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Overview of Godot's key concepts — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html

**Contents:**
- Overview of Godot's key concepts
- Scenes
- Nodes
- The scene tree
- Signals
- Summary
- User-contributed notes

Every game engine revolves around abstractions you use to build your applications. In Godot, a game is a tree of nodes that you group together into scenes. You can then wire these nodes so they can communicate using signals.

These are the four concepts you will learn here. We're going to look at them briefly to give you a sense of how the engine works. In the getting started series, you will get to use them in practice.

In Godot, you break down your game in reusable scenes. A scene can be a character, a weapon, a menu in the user interface, a single house, an entire level, or anything you can think of. Godot's scenes are flexible; they fill the role of both prefabs and scenes in some other game engines.

You can also nest scenes. For example, you can put your character in a level, and drag and drop a scene as a child of it.

A scene is composed of one or more nodes. Nodes are your game's smallest building blocks that you arrange into trees. Here's an example of a character's nodes.

It is made of a CharacterBody2D node named "Player", a Camera2D, a Sprite2D, and a CollisionShape2D.

The node names end with "2D" because this is a 2D scene. Their 3D counterparts have names that end with "3D". Be aware that "Spatial" Nodes are now called "Node3D" starting with Godot 4.

Notice how nodes and scenes look the same in the editor. When you save a tree of nodes as a scene, it then shows as a single node, with its internal structure hidden in the editor.

Godot provides an extensive library of base node types you can combine and extend to build more powerful ones. 2D, 3D, or user interface, you will do most things with these nodes.

All your game's scenes come together in the scene tree, literally a tree of scenes. And as scenes are trees of nodes, the scene tree also is a tree of nodes. But it's easier to think of your game in terms of scenes as they can represent characters, weapons, doors, or your user interface.

Nodes emit signals when some event occurs. This feature allows you to make nodes communicate without hard-wiring them in code. It gives you a lot of flexibility in how you structure your scenes.

Signals are Godot's version of the observer pattern. You can read more about it here: https://gameprogrammingpatterns.com/observer.html

For example, buttons emit a signal when pressed. You can connect a piece of code to this signal which will run in reaction to this event, like starting the game or opening a menu.

Other built-in signals can tell you when two objects collided, when a character or monster entered a given area, and much more. You can also define new signals tailored to your game.

Nodes, scenes, the scene tree, and signals are four core concepts in Godot that you will manipulate all the time.

Nodes are your game's smallest building blocks. You combine them to create scenes that you then combine and nest into the scene tree. You can then use signals to make nodes react to events in other nodes or different scene tree branches.

After this short breakdown, you probably have many questions. Bear with us as you will get many answers throughout the getting started series.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## First look at Godot's interface — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/introduction/first_look_at_the_editor.html

**Contents:**
- First look at Godot's interface
- The Project Manager
- First look at Godot's editor
- The five main screens
- Integrated class reference
- User-contributed notes

This page will give you a brief overview of Godot's interface. We're going to look at the different main screens and docks to help you situate yourself.

For a comprehensive breakdown of the editor's interface and how to use it, see the Editor manual.

When you launch Godot, the first window you see is the Project Manager. In the default tab Projects, you can manage existing projects, import or create new ones, and more.

At the top of the window, there is another tab named Asset Library. The first time you go to this tab you'll see a "Go Online" button. For privacy reasons, the Godot project manager does not access the internet by default. To change this click the "Go Online" button. You can change this option later in the settings.

Once your network mode is set to "online", you can search for demo projects in the open source asset library, which includes many projects developed by the community:

The Project Manager's settings can be opened using the Settings menu:

From here, you can change the editor's language (default is the system language), interface theme, display scale, network mode, and also the directory naming convention.

To learn the Project Manager's ins and outs, read Using the Project Manager.

When you open a new or an existing project, the editor's interface appears. Let's look at its main areas:

By default, along the window's top edge, it features main menu on the left, workspace switching buttons in the center (active workspace is highlighted), and playtest buttons and the Movie Maker Mode toggle on the right:

Just below the workspace buttons, the opened scenes as tabs are seen. The plus (+) button right next to the tabs will add a new scene to the project. With the button on the far right, distraction-free mode can be toggled, which maximizes or restores the viewport's size by hiding docks in the interface:

In the center, below the scene selector is the viewport with its toolbar at the top, where you'll find different tools to move, scale, or lock the scene's nodes (currently the 3D workspace is active):

This toolbar changes based on the context and selected node. Here is the 2D toolbar:

To learn more on workspaces, read The five main screens.

To learn more on the 3D viewport and 3D in general, read Introduction to 3D.

On either side of the viewport sit the docks. And at the bottom of the window lies the bottom panel.

Let's look at the docks. The FileSystem dock lists your project files, including scripts, images, audio samples, and more:

The Scene dock lists the active scene's nodes:

The Inspector allows you to edit the properties of a selected node:

To read more on inspector, see Inspector Dock.

Docks can be customized. Read more on Moving and resizing docks.

The bottom panel, situated below the viewport, is the host for the debug console, the animation editor, the audio mixer, and more. They can take precious space, that's why they're folded by default:

When you click on one, it expands vertically. Below, you can see the animation editor opened:

Bottom panels can also be shown or hidden using the shortcuts defined in Editor Settings > Shortcuts, under the Bottom Panels category.

There are five main screen buttons centered at the top of the editor: 2D, 3D, Script, Game and Asset Library.

You'll use the 2D screen for all types of games. In addition to 2D games, the 2D screen is where you'll build your interfaces.

In the 3D screen, you can work with meshes, lights, and design levels for 3D games.

Read Introduction to 3D for more detail about the 3D main screen.

The Game screen is where your project will appear when running it from the editor. You can go through your project to test it, and pause it and adjust it in real time. Note that this is for testing how adjustments would work, any changes made here are not saved when the game stops running.

The Script screen is a complete code editor with a debugger, rich auto-completion, and built-in code reference.

Finally, the Asset Library is a library of free and open source add-ons, scripts, and assets to use in your projects.

You can learn more about the asset library in About the Asset Library.

Godot comes with a built-in class reference.

You can search for information about a class, method, property, constant, or signal by any one of the following methods:

Pressing F1 (or Opt + Space on macOS, or Fn + F1 for laptops with a Fn key) anywhere in the editor.

Clicking the "Search Help" button in the top-right of the Script main screen.

Clicking on the Help menu and Search Help.

Ctrl + Click (Cmd + Click on macOS) on a class name, function name, or built-in variable in the script editor.

When you do any of these, a window pops up. Type to search for any item. You can also use it to browse available objects and methods.

Double-click on an item to open the corresponding page in the script main screen.

Clicking while pressing the Ctrl key on a class name, function name, or built-in variable in the script editor.

Right-clicking on nodes and choosing Open Documentation or choosing Lookup Symbol for elements in script editor will directly open their documentation.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Learning new features — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/introduction/learning_new_features.html

**Contents:**
- Learning new features
- Making the most of this manual
- Learning to think like a programmer
- Learning with the community
- Community tutorials
- User-contributed notes

Godot is a feature-rich game engine. There is a lot to learn about it. This page explains how you can use the online manual, built-in code reference, and join online communities to learn new features and techniques.

What you are reading now is the user manual. It documents each of the engine's concepts and available features. When learning a new topic, you can start by browsing the corresponding section of this website. The left menu allows you to explore broad topics while the search bar will help you find more specific pages. If a page exists for a given theme, it will often link to more related content.

The manual has a companion class reference that explains each Godot class's available functions and properties when programming. While the manual covers general features, concepts, and how to use the editor, the reference is all about using Godot's scripting API (Application Programming Interface). You can access it both online and offline. We recommend browsing the reference offline, from within the Godot editor. To do so, go to Help -> Search Help or press F1.

To browse it online, head to the manual's Class Reference section.

A class reference's page tells you:

Where the class exists in the inheritance hierarchy. You can click the top links to jump to parent classes and see the properties and methods a type inherits.

A summary of the class's role and use cases.

An explanation of the class's properties, methods, signals, enums, and constants.

Links to manual pages further detailing the class.

If the manual or class reference is missing or has insufficient information, please open an Issue in the official godot-docs GitHub repository to report it.

You can hold Ctrl (macOS Cmd) and then mouseover text like the name of a class, property, method, signal, or constant to underline it, then Ctrl + Click (macOS Cmd + Click) it to jump to it.

Teaching programming foundations and how to think like a game developer is beyond the scope of Godot's documentation. If you're new to programming, we recommend two excellent free resources to get you started:

Harvard university offers a free courseware to learn to program, CS50. It will teach you programming fundamentals, how code works, and how to think like a programmer. These skills are essential to become a game developer and learn any game engine efficiently. You can see this course as an investment that will save you time and trouble when you learn to create games.

If you prefer books, check out the free ebook Automate The Boring Stuff With Python by Al Sweigart.

Godot has a growing community of users. If you're stuck on a problem or need help to better understand how to achieve something, you can ask other users for help on one of the many active communities.

The best place to ask questions and find already answered ones is the official Godot Forum. These responses show up in search engine results and get saved, allowing other users to benefit from discussions on the platform. Once you have asked a question there, you can share its link on other social platforms. Before asking a question, be sure to look for existing answers that might solve your problem on this website or using your preferred search engine.

Asking questions well and providing details will help others answer you faster and better. When asking questions, we recommend including the following information:

Describe your goal. You want to explain what you are trying to achieve design-wise. If you are having trouble figuring out how to make a solution work, there may be a different, easier solution that accomplishes the same goal.

If there is an error involved, share the exact error message. You can copy the exact error message in the editor's Debugger bottom panel by clicking the Copy Error icon. Knowing what it says can help community members better identify how you triggered the error.

If there is code involved, share a code sample. Other users won't be able to help you fix a problem without seeing your code. Share the code as text directly. To do so, you can copy and paste a short code snippet in a chat box, or use a website like Pastebin to share long files.

Share a screenshot of your Scene dock along with your written code. Most of the code you write affects nodes in your scenes. As a result, you should think of those scenes as part of your source code.

Also, please don't take a picture with your phone, the low quality and screen reflections can make it hard to understand the image. Your operating system should have a built-in tool to take screenshots with the PrtSc (Print Screen) key (macOS: use Cmd + Shift + 3 for a full screen shot, more information here).

Alternatively, you can use a program like ShareX on Windows, or Flameshot on Windows/macOS/Linux.

Sharing a video of your running game can also be really useful to troubleshoot your game. You can use programs like OBS Studio and Screen to GIF to capture your screen.

You can then use a service like streamable or a cloud provider to upload and share your videos for free.

If you're not using the stable version of Godot, please mention the version you're using. The answer can be different as available features and the interface evolve rapidly.

Following these guidelines will maximize your chances of getting the answer you're looking for. They will save time both for you and the persons helping you.

This manual aims to provide a comprehensive reference of Godot's features. Aside from the 2D and 3D getting started series, it does not contain tutorials to implement specific game genres. If you're looking for a tutorial about creating a role-playing game, a platformer, or other, please see Tutorials and resources, which lists content made by the Godot community.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Godot's design philosophy — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/introduction/godot_design_philosophy.html

**Contents:**
- Godot's design philosophy
- Object-oriented design and composition
- All-inclusive package
- Open source
- Community-driven
- The Godot editor is a Godot game
- Separate 2D and 3D engines
- User-contributed notes

Now that you've gotten your feet wet, let's talk about Godot's design.

Every game engine is different and fits different needs. Not only do they offer a range of features, but the design of each engine is unique. This leads to different workflows and different ways to form your games' structures. This all stems from their respective design philosophies.

This page is here to help you understand how Godot works, starting with some of its core pillars. It is not a list of available features, nor is it an engine comparison. To know if any engine can be a good fit for your project, you need to try it out for yourself and understand its design and limitations.

Please watch Godot explained in 7 minutes if you're looking for an overview of the engine's features.

Godot embraces object-oriented design at its core with its flexible scene system and Node hierarchy. It tries to stay away from strict programming patterns to offer an intuitive way to structure your game.

For one, Godot lets you compose or aggregate scenes. It's like nested prefabs: you can create a BlinkingLight scene and a BrokenLantern scene that uses the BlinkingLight. Then, create a city filled with BrokenLanterns. Change the BlinkingLight's color, save, and all the BrokenLanterns in the city will update instantly.

On top of that, you can inherit from any scene.

A Godot scene could be a Weapon, a Character, an Item, a Door, a Level, part of a level… anything you'd like. It works like a class in pure code, except you're free to design it by using the editor, using only the code, or mixing and matching the two.

It's different from prefabs you find in several 3D engines, as you can then inherit from and extend those scenes. You may create a Magician that extends your Character. Modify the Character in the editor and the Magician will update as well. It helps you build your projects so that their structure matches the game's design.

Also note that Godot offers many different types of objects called nodes, each with a specific purpose. Nodes are part of a tree and always inherit from their parents up to the Node class. Although the engine does feature some nodes like collision shapes that a parent physics body will use, most nodes work independently from one another.

In other words, Godot's nodes do not work like components in some other game engines.

Sprite2D is a Node2D, a CanvasItem and a Node. It has all the properties and features of its three parent classes, like transforms or the ability to draw custom shapes and render with a custom shader.

Godot tries to provide its own tools to answer most common needs. It has a dedicated scripting workspace, an animation editor, a tilemap editor, a shader editor, a debugger, a profiler, the ability to hot-reload locally and on remote devices, etc.

The goal is to offer a full package to create games and a continuous user experience. You can still work with external programs as long as there is an import plugin available in Godot for it.

That is also partly why Godot offers its own programming language GDScript along with C#. GDScript is designed for the needs of game developers and game designers, and is tightly integrated in the engine and the editor.

GDScript lets you write code using an indentation-based syntax, yet it detects types and offers a static language's quality of auto-completion. It is also optimized for gameplay code with built-in types like Vectors and Colors.

Note that with GDExtension, you can write high-performance code using compiled languages like C, C++, Rust, D, Haxe, or Swift without recompiling the engine.

Note that the 3D workspace doesn't feature as many tools as the 2D workspace. You'll need external programs or add-ons to edit terrains, animate complex characters, and so on. Godot provides a complete API to extend the editor's functionality using game code. See The Godot editor is a Godot game below.

Godot offers a fully open source codebase under the MIT license. This means that the codebase is free for anyone to download, use, modify, or share, as long as its license file is kept intact.

All technologies that ship with Godot, including third-party libraries, must be legally compatible with this open source license. Therefore, most parts of Godot are developed from the ground up by community contributors.

Anyone can plug in proprietary tools for the needs of their projects — they just won't ship with the engine. This may include Google AdMob, or FMOD. Any of these can come as third-party plugins instead.

On the other hand, an open codebase means you can learn from and extend the engine to your heart's content. You can also debug games easily, as Godot will print errors with a stack trace, even if they come from the engine itself.

This does not affect the work you do with Godot in any way: there's no strings attached to the engine or anything you make with it.

Godot is made by its community, for the community, and for all game creators out there. It's the needs of the users and open discussions that drive the core updates. New features from the core developers often focus on what will benefit the most users first.

That said, although a handful of core developers work on it full-time, the project has thousands of contributors at the time of writing. Benevolent programmers work on features they may need themselves, so you'll see improvements in all corners of the engine at the same time in every major release.

The Godot editor runs on the game engine. It uses the engine's own UI system, it can hot-reload code and scenes when you test your projects, or run game code in the editor. This means you can use the same code and scenes for your games, or build plugins and extend the editor.

This leads to a reliable and flexible UI system, as it powers the editor itself. With the @tool annotation, you can run any game code in the editor.

RPG in a Box is a voxel RPG editor made with Godot. It uses Godot's UI tools for its node-based programming system and for the rest of the interface.

Put the @tool annotation at the top of any GDScript file and it will run in the editor. This lets you import and export plugins, create plugins like custom level editors, or create scripts with the same nodes and API you use in your projects.

The editor is fully written in C++ and is statically compiled into the binary. This means you can't import it as a typical project that would have a project.godot file.

Godot offers dedicated 2D and 3D rendering engines. As a result, the base unit for 2D scenes is pixels. Even though the engines are separate, you can render 2D in 3D, 3D in 2D, and overlay 2D sprites and interfaces over your 3D world.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Step by step — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/step_by_step/index.html

**Contents:**
- Step by step

This series builds upon the Introduction to Godot and will get you started with the editor and the engine. You will learn more about nodes and scenes, code your first classes with GDScript, use signals to make nodes communicate with one another, and more.

The following lessons are here to prepare you for Your first 2D game, a step-by-step tutorial where you will code a game from scratch. By the end of it, you will have the necessary foundations to explore more features in other sections. We also included links to pages that cover a given topic in-depth where appropriate.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Nodes and Scenes — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/step_by_step/nodes_and_scenes.html

**Contents:**
- Nodes and Scenes
- Nodes
- Scenes
- Creating your first scene
- Changing a node's properties
- Running the scene
- Setting the main scene
- User-contributed notes

In Overview of Godot's key concepts, we saw that a Godot game is a tree of scenes and that each scene is a tree of nodes. In this lesson, we explain a bit more about them. You will also create your first scene.

Nodes are the fundamental building blocks of your game. They are like the ingredients in a recipe. There are dozens of kinds that can display an image, play a sound, represent a camera, and much more.

All nodes have the following characteristics:

They receive callbacks to update every frame.

You can extend them with new properties and functions.

You can add them to another node as a child.

The last characteristic is important. Together, nodes form a tree, which is a powerful feature to organize projects. Since different nodes have different functions, combining them produces more complex behavior. As we saw before, you can build a playable character the camera follows using a CharacterBody2D node, a Sprite2D node, a Camera2D node, and a CollisionShape2D node.

When you organize nodes in a tree, like our character, we call this construct a scene. Once saved, scenes work like new node types in the editor, where you can add them as a child of an existing node. In that case, the instance of the scene appears as a single node with its internals hidden.

Scenes allow you to structure your game's code however you want. You can compose nodes to create custom and complex node types, like a game character that runs and jumps, a life bar, a chest with which you can interact, and more.

The Godot editor essentially is a scene editor. It has plenty of tools for editing 2D and 3D scenes, as well as user interfaces. A Godot project can contain as many of these scenes as you need. The engine only requires one as your application's main scene. This is the scene Godot will first load when you or a player runs the game.

On top of acting like nodes, scenes have the following characteristics:

They always have one root node, like the "Player" in our example.

You can save them to your local drive and load them later.

You can create as many instances of a scene as you'd like. You could have five or ten characters in your game, created from your Character scene.

Let's create our first scene with a single node. To do so, you will need to create a new project first. After opening the project, you should see an empty editor.

In an empty scene, the Scene dock on the left shows several options to add a root node quickly. 2D Scene adds a Node2D node, 3D Scene adds a Node3D node, and User Interface adds a Control node. These presets are here for convenience; they are not mandatory. Other Node lets you select any node to be the root node. In an empty scene, Other Node is equivalent to pressing the Add Child Node button at the top-left of the Scene dock, which usually adds a new node as a child of the currently selected node.

We're going to add a single Label node to our scene. Its function is to draw text on the screen.

Press the Add Child Node button or Other Node to create a root node.

The Create New Node dialog opens, showing the long list of available nodes.

Select the Label node. You can type its name to filter down the list.

Click on the Label node to select it and click the Create button at the bottom of the window.

A lot happens when you add a scene's first node. The scene changes to the 2D workspace because Label is a 2D node type. The Label appears, selected, in the top-left corner of the viewport. The node appears in the Scene dock on the left, and the node's properties appear in the Inspector dock on the right.

The next step is to change the Label's Text property. Let's change it to "Hello World".

Head to the Inspector dock on the right of the viewport. Click inside the field below the Text property and type "Hello World".

You will see the text draw in the viewport as you type.

You can edit any property listed in the Inspector as we did with the Text. For a complete reference of the Inspector dock, see Inspector Dock.

You can move your Label node in the viewport by selecting the move tool in the toolbar.

With the Label selected, click and drag anywhere in the viewport to move it to the center of the view delimited by the rectangle.

Everything's ready to run the scene! Press the Run Current Scene button in the top-right of the screen or press F6 (Cmd + R on macOS).

A popup invites you to save the scene, which is required to run it. Click the Save button in the file browser to save it as label.tscn.

The Save Scene As dialog, like other file dialogs in the editor, only allows you to save files inside the project. The res:// path at the top of the window represents the project's root directory and stands for "resource path". For more information about file paths in Godot, see File system.

The application should open in a new window and display the text "Hello World".

Close the window or press F8 (Cmd + . on macOS) to quit the running scene.

To run our test scene, we used the Run Current Scene button. Another button next to it, Run Project, allows you to set and run the project's main scene. You can also press F5 (Cmd + B on macOS) to do so.

Running the project's main scene is distinct from running the current scene. If you encounter unexpected behavior, check to ensure you are running the correct scene.

A popup window appears and invites you to select the main scene.

Click the Select button, and in the file dialog that appears, double click on label.tscn.

The demo should run again. Moving forward, every time you run the project, Godot will use this scene as a starting point.

The editor saves the main scene's path in a project.godot file in your project's directory. While you can edit this text file directly to change project settings, you can also use the Project > Project Settings window to do so. For more information, see Project Settings.

In the next part, we will discuss another key concept in games and in Godot: creating instances of a scene.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Creating instances — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/step_by_step/instancing.html

**Contents:**
- Creating instances
- In practice
- Editing scenes and instances
- Scene instances as a design language
- Summary
- User-contributed notes

This tutorial refers to instancing scenes in the editor. To learn how to instance scenes from code, see Nodes and scene instances.

Godot's approach to instancing described below should not be confused with hardware instancing that can be used to render large amounts of similar objects quickly. See Optimization using MultiMeshes instead.

In the previous part, we saw that a scene is a collection of nodes organized in a tree structure, with a single node as its root. You can split your project into any number of scenes. This feature helps you break down and organize your game's different components.

You can create as many scenes as you'd like and save them as files with the .tscn extension, which stands for "text scene". The label.tscn file from the previous lesson was an example. We call those files "Packed Scenes" as they pack information about your scene's content.

Here's an example of a ball. It's composed of a RigidBody2D node as its root named Ball, which allows the ball to fall and bounce on walls, a Sprite2D node, and a CollisionShape2D.

Once you have saved a scene, it works as a blueprint: you can reproduce it in other scenes as many times as you'd like. Replicating an object from a template like this is called instancing.

As we mentioned in the previous part, instanced scenes behave like a node: the editor hides their content by default. When you instance the Ball, you only see the Ball node. Notice also how each duplicate has a unique name.

Every instance of the Ball scene starts with the same structure and properties as ball.tscn. However, you can modify each independently, such as changing how they bounce, how heavy they are, or any property exposed by the source scene.

Let's use instancing in practice to see how it works in Godot. We invite you to download the ball's sample project we prepared for you: instancing_starter.zip.

Extract the archive on your computer. To import it, you need the Project Manager. The Project Manager is accessed by opening Godot, or if you already have Godot opened, click on Project > Quit to Project List (Ctrl + Shift + Q, Ctrl + Option + Cmd + Q on macOS)

In the Project Manager, click the Import button to import the project.

In the pop-up that appears navigate to the folder you extracted. Double-click the project.godot file to open it.

Finally, click the Import button.

A window notifying you that the project was last opened in an older Godot version may appear, that's not an issue. Click Ok to open the project.

The project contains two packed scenes: main.tscn, containing walls against which the ball collides, and ball.tscn. The Main scene should open automatically. If you're seeing an empty 3D scene instead of the main scene, click the 2D button at the top of the screen.

Let's add a ball as a child of the Main node. In the Scene dock, select the Main node. Then, click the link icon at the top of the scene dock. This button allows you to add an instance of a scene as a child of the currently selected node.

Double-click the ball scene to instance it.

The ball appears in the top-left corner of the viewport.

Click on it and drag it towards the center of the view.

Play the game by pressing F5 (Cmd + B on macOS). You should see it fall.

Now, we want to create more instances of the Ball node. With the ball still selected, press Ctrl + D (Cmd + D on macOS) to call the duplicate command. Click and drag to move the new ball to a different location.

You can repeat this process until you have several in the scene.

Play the game again. You should now see every ball fall independently from one another. This is what instances do. Each is an independent reproduction of a template scene.

There is more to instances. With this feature, you can:

Change the properties of one ball without affecting the others using the Inspector.

Change the default properties of every Ball by opening the ball.tscn scene and making a change to the Ball node there. Upon saving, all instances of the Ball in the project will see their values update.

Changing a property on an instance always overrides values from the corresponding packed scene.

Let's try this. Double-click ball.tscn in the FileSystem to open it.

In the Scene dock on the left, select the Ball node. Then, in the Inspector on the right, click on the PhysicsMaterial property to expand it.

Set its Bounce property to 0.5 by clicking on the number field, typing 0.5, and pressing Enter.

Play the game by pressing F5 (Cmd + B on macOS) and notice how all balls now bounce a lot more. As the Ball scene is a template for all instances, modifying it and saving causes all instances to update accordingly.

Let's now adjust an individual instance. Head back to the Main scene by clicking on the corresponding tab above the viewport.

Select one of the instanced Ball nodes and, in the Inspector, set its Gravity Scale value to 10.

A grey "revert" button appears next to the adjusted property.

This icon indicates you are overriding a value from the source packed scene. Even if you modify the property in the original scene, the value override will be preserved in the instance. Clicking the revert icon will restore the property to the value in the saved scene.

Rerun the game and notice how this ball now falls much faster than the others.

You may notice you are unable to change the values of the PhysicsMaterial of the ball. This is because PhysicsMaterial is a resource, and needs to be made unique before you can edit it in a scene that is linking to its original scene. To make a resource unique for one instance, right-click on the Physics Material property in the Inspector and click Make Unique in the context menu.

Resources are another essential building block of Godot games we will cover in a later lesson.

Instances and scenes in Godot offer an excellent design language, setting the engine apart from others out there. We designed Godot around this concept from the ground up.

We recommend dismissing architectural code patterns when making games with Godot, such as Model-View-Controller (MVC) or Entity-Relationship diagrams. Instead, you can start by imagining the elements players will see in your game and structure your code around them.

For example, you could break down a shooter game like so:

You can come up with a diagram like this for almost any type of game. Each rectangle represents an entity that's visible in the game from the player's perspective. The arrows point towards the instantiator of each scene.

Once you have a diagram, we recommend creating a scene for each element listed in it to develop your game. You'll use instancing, either by code or directly in the editor, to build your tree of scenes.

Programmers tend to spend a lot of time designing abstract architectures and trying to fit components into it. Designing based on scenes makes development faster and more straightforward, allowing you to focus on the game logic itself. Because most game components map directly to a scene, using a design based on scene instantiation means you need little other architectural code.

Here's the example of a scene diagram for an open-world game with tons of assets and nested elements:

Imagine we started by creating the room. We could make a couple of different room scenes, with unique arrangements of furniture in them. Later, we could make a house scene that uses multiple room instances for the interior. We would create a citadel out of many instanced houses and a large terrain on which we would place the citadel. Each of these would be a scene instancing one or more sub-scenes.

Later, we could create scenes representing guards and add them to the citadel. They would be indirectly added to the overall game world.

With Godot, it's easy to iterate on your game like this, as all you need to do is create and instantiate more scenes. We designed the editor to be accessible to programmers, designers, and artists alike. A typical team development process can involve 2D or 3D artists, level designers, game designers, and animators, all working with the Godot editor.

Instancing, the process of producing an object from a blueprint, has many handy uses. With scenes, it gives you:

The ability to divide your game into reusable components.

A tool to structure and encapsulate complex systems.

A language to think about your game project's structure in a natural way.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Scripting languages — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/step_by_step/scripting_languages.html

**Contents:**
- Scripting languages
- Available scripting languages
- Which language should I use?
  - GDScript
  - .NET / C#
  - C++ via GDExtension
- Summary
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

This lesson will give you an overview of the available scripting languages in Godot. You will learn the pros and cons of each option. In the next part, you will write your first script using GDScript.

Scripts attach to a node and extend its behavior. This means that scripts inherit all functions and properties of the node they attach to.

For example, take a game where a Camera2D node follows a ship. The Camera2D node follows its parent by default. Imagine you want the camera to shake when the player takes damage. As this feature is not built into Godot, you would attach a script to the Camera2D node and code the shake.

Godot offers four gameplay programming languages: GDScript, C#, and, via its GDExtension technology, C and C++. There are more community-supported languages, but these are the official ones.

You can use multiple languages in a single project. For instance, in a team, you could code gameplay logic in GDScript as it's fast to write, and use C# or C++ to implement complex algorithms and maximize their performance. Or you can write everything in GDScript or C#. It's your call.

We provide this flexibility to answer the needs of different game projects and developers.

If you're a beginner, we recommend to start with GDScript. We made this language specifically for Godot and the needs of game developers. It has a lightweight and straightforward syntax and provides the tightest integration with Godot.

For C#, you will need an external code editor like VSCode or Visual Studio. While C# support is now mature, you will find fewer learning resources for it compared to GDScript. That's why we recommend C# mainly to users who already have experience with the language.

Let's look at each language's features, as well as its pros and cons.

GDScript is an object-oriented and imperative programming language built for Godot. It's made by and for game developers to save you time coding games. Its features include:

A simple syntax that leads to short files.

Blazing fast compilation and loading times.

Tight editor integration, with code completion for nodes, signals, and more information from the scene it's attached to.

Built-in vector and transform types, making it efficient for heavy use of linear algebra, a must for games.

Supports multiple threads as efficiently as statically typed languages.

No garbage collection, as this feature eventually gets in the way when creating games. The engine counts references and manages the memory for you in most cases by default, but you can also control memory if you need to.

Gradual typing. Variables have dynamic types by default, but you also can use type hints for strong type checks.

GDScript looks like Python as you structure your code blocks using indentations, but it doesn't work the same way in practice. It's inspired by multiple languages, including Squirrel, Lua, and Python.

Why don't we use Python or Lua directly?

Years ago, Godot used Python, then Lua. Both languages' integration took a lot of work and had severe limitations. For example, threading support was a big challenge with Python.

Developing a dedicated language doesn't take us more work and we can tailor it to game developers' needs. We're now working on performance optimizations and features that would've been difficult to offer with third-party languages.

As Microsoft's C# is a favorite amongst game developers, we officially support it. C# is a mature and flexible language with tons of libraries written for it. We were able to add support for it thanks to a generous donation from Microsoft.

C# offers a good tradeoff between performance and ease of use, although you should be aware of its garbage collector.

You must use the .NET edition of the Godot editor to script in C#. You can download it on the Godot website's download page.

Since Godot uses .NET 8, in theory, you can use any third-party .NET library or framework in Godot, as well as any Common Language Infrastructure-compliant programming language, such as F#, Boo, or ClojureCLR. However, C# is the only officially supported .NET option.

GDScript code itself doesn't execute as fast as compiled C# or C++. However, most script code calls functions written with fast algorithms in C++ code inside the engine. In many cases, writing gameplay logic in GDScript, C#, or C++ won't have a significant impact on performance.

Projects written in C# using Godot 4 currently cannot be exported to the web platform. To use C# on that platform, consider Godot 3 instead. Android and iOS platform support is available as of Godot 4.2, but is experimental and some limitations apply.

To learn more about C#, head to the C#/.NET section.

GDExtension allows you to write game code in C++ without needing to recompile Godot.

You can use any version of the language or mix compiler brands and versions for the generated shared libraries, thanks to our use of an internal C API Bridge.

GDExtension is the best choice for performance. You don't need to use it throughout an entire game, as you can write other parts in GDScript or C#.

When working with GDExtension, the available types, functions, and properties closely resemble Godot's actual C++ API.

Scripts are files containing code that you attach to a node to extend its functionality.

Godot supports four official scripting languages, offering you flexibility between performance and ease of use.

You can mix languages, for instance, to implement demanding algorithms with C or C++ and write most of the game logic with GDScript or C#.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Creating your first script — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/step_by_step/scripting_first_script.html

**Contents:**
- Creating your first script
- Project setup
- Creating a new script
- Hello, world!
- Turning around
  - Moving forward
- Complete script
- User-contributed notes

In this lesson, you will code your first script to make the Godot icon turn in circles. As we mentioned in the introduction, we assume you have programming foundations.

This tutorial is written for GDScript, and the equivalent C# code is included in another tab of each codeblock for convenience.

To learn more about GDScript, its keywords, and its syntax, head to the GDScript section. To learn more about C#, head to the C#/.NET section.

Please create a new project to start with a clean slate. Your project should contain one picture: the Godot icon, which we often use for prototyping in the community.

We need to create a Sprite2D node to display it in the game. In the Scene dock, click the Other Node button.

Type "Sprite2D" in the search bar to filter nodes and double-click on Sprite2D to create the node.

Your Scene tab should now only have a Sprite2D node.

A Sprite2D node needs a texture to display. In the Inspector on the right, you can see that the Texture property says <empty>. To display the Godot icon, click and drag the file icon.svg from the FileSystem dock onto the Texture slot.

You can create Sprite2D nodes automatically by dragging and dropping images on the viewport.

Then, click and drag the icon in the viewport to center it in the game view.

To create and attach a new script to our node, right-click on Sprite2D in the Scene dock and select Attach Script.

The Attach Node Script window appears. It allows you to select the script's language and file path, among other options.

Change the Template field from Node: Default to Object: Empty to start with a clean file. Leave the other options set to their default values and click the Create button to create the script.

C# script names need to match their class name. In this case, you should name the file MySprite2D.cs.

The Script workspace should appear with your new sprite_2d.gd file open and the following line of code:

Every GDScript file is implicitly a class. The extends keyword defines the class this script inherits or extends. In this case, it's Sprite2D, meaning our script will get access to all the properties and functions of the Sprite2D node, including classes it extends, like Node2D, CanvasItem, and Node.

In GDScript, if you omit the line with the extends keyword, your class will implicitly extend RefCounted, which Godot uses to manage your application's memory.

Inherited properties include the ones you can see in the Inspector dock, like our node's texture.

By default, the Inspector displays a node's properties in "Title Case", with capitalized words separated by a space. In GDScript code, these properties are in "snake_case", which is lowercase with words separated by an underscore.

You can hover over any property's name in the Inspector to see a description and its identifier in code.

Our script currently doesn't do anything. Let's make it print the text "Hello, world!" to the Output bottom panel to get started.

Add the following code to your script:

Let's break it down. The func keyword defines a new function named _init. This is a special name for our class's constructor. The engine calls _init() on every object or node upon creating it in memory, if you define this function.

GDScript is an indent-based language. The tab at the start of the line that says print() is necessary for the code to work. If you omit it or don't indent a line correctly, the editor will highlight it in red and display the following error message: "Indented block expected".

Save the scene as sprite_2d.tscn if you haven't already, then press F6 (Cmd + R on macOS) to run it. Look at the Output bottom panel that expands. It should display "Hello, world!".

Delete the _init() function, so you're only left with the line extends Sprite2D.

It's time to make our node move and rotate. To do so, we're going to add two member variables to our script: the movement speed in pixels per second and the angular speed in radians per second. Add the following after the extends Sprite2D line.

Member variables sit near the top of the script, after any "extends" lines, but before functions. Every node instance with this script attached to it will have its own copy of the speed and angular_speed properties.

Angles in Godot work in radians by default, but you have built-in functions and properties available if you prefer to calculate angles in degrees instead.

To move our icon, we need to update its position and rotation every frame in the game loop. We can use the _process() virtual function of the Node class. If you define it in any class that extends the Node class, like Sprite2D, Godot will call the function every frame and pass it an argument named delta, the time elapsed since the last frame.

Games work by rendering many images per second, each called a frame, and they do so in a loop. We measure the rate at which a game produces images in Frames Per Second (FPS). Most games aim for 60 FPS, although you might find figures like 30 FPS on slower mobile devices or 90 to 240 for virtual reality games.

The engine and game developers do their best to update the game world and render images at a constant time interval, but there are always small variations in frame render times. That's why the engine provides us with this delta time value, making our motion independent of our framerate.

At the bottom of the script, define the function:

The func keyword defines a new function. After it, we have to write the function's name and arguments it takes in parentheses. A colon ends the definition, and the indented blocks that follow are the function's content or instructions.

Notice how _process(), like _init(), starts with a leading underscore. By convention, Godot's virtual functions, that is to say, built-in functions you can override to communicate with the engine, start with an underscore.

The line inside the function, rotation += angular_speed * delta, increments our sprite's rotation every frame. Here, rotation is a property inherited from the class Node2D, which Sprite2D extends. It controls the rotation of our node and works with radians.

In the code editor, you can Ctrl + Click (Cmd + Click on macOS) on any built-in property or function like position, rotation, or _process to open the corresponding documentation in a new tab.

Run the scene to see the Godot icon turn in-place.

In C#, notice how the delta argument taken by _Process() is a double. We therefore need to convert it to float when we apply it to the rotation.

Let's now make the node move. Add the following two lines inside of the _process() function, ensuring the new lines are indented the same way as the rotation += angular_speed * delta line before them.

As we already saw, the var keyword defines a new variable. If you put it at the top of the script, it defines a property of the class. Inside a function, it defines a local variable: it only exists within the function's scope.

We define a local variable named velocity, a 2D vector representing both a direction and a speed. To make the node move forward, we start from the Vector2 class's constant Vector2.UP, a vector pointing up, and rotate it by calling the Vector2 method rotated(). This expression, Vector2.UP.rotated(rotation), is a vector pointing forward relative to our icon. Multiplied by our speed property, it gives us a velocity we can use to move the node forward.

We add velocity * delta to the node's position to move it. The position itself is of type Vector2, a built-in type in Godot representing a 2D vector.

Run the scene to see the Godot head run in circles.

Moving a node like that does not take into account colliding with walls or the floor. In Your first 2D game, you will learn another approach to moving objects while detecting collisions.

Our node currently moves by itself. In the next part, Listening to player input, we'll use player input to control it.

Here is the complete sprite_2d.gd file for reference.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Sprite2D
```

Example 2 (swift):
```swift
using Godot;
using System;

public partial class MySprite2D : Sprite2D
{
}
```

Example 3 (go):
```go
func _init():
    print("Hello, world!")
```

Example 4 (json):
```json
public MySprite2D()
{
    GD.Print("Hello, world!");
}
```

---

## Listening to player input — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/step_by_step/scripting_player_input.html

**Contents:**
- Listening to player input
- Moving when pressing "up"
- Complete script
- Summary
- User-contributed notes

Building upon the previous lesson, Creating your first script, let's look at another important feature of any game: giving control to the player. To add this, we need to modify our sprite_2d.gd code.

You have two main tools to process the player's input in Godot:

The built-in input callbacks, mainly _unhandled_input(). Like _process(), it's a built-in virtual function that Godot calls every time the player presses a key. It's the tool you want to use to react to events that don't happen every frame, like pressing Space to jump. To learn more about input callbacks, see Using InputEvent.

The Input singleton. A singleton is a globally accessible object. Godot provides access to several in scripts. It's the right tool to check for input every frame.

We're going to use the Input singleton here as we need to know if the player wants to turn or move every frame.

For turning, we should use a new variable: direction. In our _process() function, replace the rotation += angular_speed * delta line with the code below.

Our direction local variable is a multiplier representing the direction in which the player wants to turn. A value of 0 means the player isn't pressing the left or the right arrow key. A value of 1 means the player wants to turn right, and -1 means they want to turn left.

To produce these values, we introduce conditional statements and the use of Input. A conditional statement starts with the if keyword in GDScript and ends with a colon. The condition is specifically the expression between the keyword and the colon at the end of the line.

To check if a key was pressed this frame, we call Input.is_action_pressed(). The method takes a text string representing an input action and returns true if the action is pressed, false otherwise.

The two actions we use above, "ui_left" and "ui_right", are predefined in every Godot project. They respectively trigger when the player presses the left and right arrows on the keyboard or left and right on a gamepad's D-pad.

You can see and edit input actions in your project by going to Project > Project Settings and clicking on the Input Map tab.

Finally, we use the direction as a multiplier when we update the node's rotation: rotation += angular_speed * direction * delta.

Comment out the lines var velocity = Vector2.UP.rotated(rotation) * speed and position += velocity * delta like this:

This will ignore the code that moved the icon's position in a circle without user input from the previous exercise.

If you run the scene with this code, the icon should rotate when you press Left and Right.

To only move when pressing a key, we need to modify the code that calculates the velocity. Uncomment the code and replace the line starting with var velocity with the code below.

We initialize the velocity with a value of Vector2.ZERO, another constant of the built-in Vector type representing a 2D vector of length 0.

If the player presses the "ui_up" action, we then update the velocity's value, causing the sprite to move forward.

Here is the complete sprite_2d.gd file for reference.

If you run the scene, you should now be able to rotate with the left and right arrow keys and move forward by pressing Up.

In summary, every script in Godot represents a class and extends one of the engine's built-in classes. The node types your classes inherit from give you access to properties, such as rotation and position in our sprite's case. You also inherit many functions, which we didn't get to use in this example.

In GDScript, the variables you put at the top of the file are your class's properties, also called member variables. Besides variables, you can define functions, which, for the most part, will be your classes' methods.

Godot provides several virtual functions you can define to connect your class with the engine. These include _process(), to apply changes to the node every frame, and _unhandled_input(), to receive input events like key and button presses from the users. There are quite a few more.

The Input singleton allows you to react to the player's input anywhere in your code. In particular, you'll get to use it in the _process() loop.

In the next lesson, Using signals, we'll build upon the relationship between scripts and nodes by having our nodes trigger code in scripts.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (typescript):
```typescript
var direction = 0
if Input.is_action_pressed("ui_left"):
    direction = -1
if Input.is_action_pressed("ui_right"):
    direction = 1

rotation += angular_speed * direction * delta
```

Example 2 (gdscript):
```gdscript
var direction = 0;
if (Input.IsActionPressed("ui_left"))
{
    direction = -1;
}
if (Input.IsActionPressed("ui_right"))
{
    direction = 1;
}

Rotation += _angularSpeed * direction * (float)delta;
```

Example 3 (csharp):
```csharp
#var velocity = Vector2.UP.rotated(rotation) * speed

#position += velocity * delta
```

Example 4 (csharp):
```csharp
//var velocity = Vector2.Up.Rotated(Rotation) * _speed;

//Position += velocity * (float)delta;
```

---

## Using signals — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html

**Contents:**
- Using signals
- Scene setup
- Connecting a signal in the editor
- Connecting a signal via code
- Complete script
- Custom signals
- Summary
- User-contributed notes

In this lesson, we will look at signals. They are messages that nodes emit when something specific happens to them, like a button being pressed. Other nodes can connect to that signal and call a function when the event occurs.

Signals are a delegation mechanism built into Godot that allows one game object to react to a change in another without them referencing one another. Using signals limits coupling and keeps your code flexible.

For example, you might have a life bar on the screen that represents the player's health. When the player takes damage or uses a healing potion, you want the bar to reflect the change. To do so, in Godot, you would use signals.

Like methods (Callable), signals are a first-class type since Godot 4.0. This means you can pass them around as method arguments directly without having to pass them as strings, which allows for better autocompletion and is less error-prone. See the Signal class reference for a list of what you can do with the Signal type directly.

As mentioned in the introduction, signals are Godot's version of the observer pattern. You can learn more about it in Game Programming Patterns.

We will now use a signal to make our Godot icon from the previous lesson (Listening to player input) move and stop by pressing a button.

For this project, we will be following the Godot naming conventions.

GDScript: Classes (nodes) use PascalCase, variables and functions use snake_case, and constants use ALL_CAPS (See GDScript style guide).

C#: Classes, export variables and methods use PascalCase, private fields use _camelCase, local variables and parameters use camelCase (See C# style guide). Be careful to type the method names precisely when connecting signals.

To add a button to our game, we will create a new scene which will include both a Button and the sprite_2d.tscn scene we created in the Creating your first script lesson.

Create a new scene by going to the menu Scene > New Scene.

In the Scene dock, click the 2D Scene button. This will add a Node2D as our root.

In the FileSystem dock, click and drag the sprite_2d.tscn file you saved previously onto the Node2D to instantiate it.

We want to add another node as a sibling of the Sprite2D. To do so, right-click on Node2D and select Add Child Node.

Search for the Button node and add it.

The node is small by default. Click and drag on the bottom-right handle of the Button in the viewport to resize it.

If you don't see the handles, ensure the select tool is active in the toolbar.

Click and drag on the button itself to move it closer to the sprite.

You can also write a label on the Button by editing its Text property in the Inspector. Enter Toggle motion.

Your scene tree and viewport should look like this.

Save your newly created scene as node_2d.tscn, if you haven't already. You can then run it with F6 (Cmd + R on macOS). At the moment, the button will be visible, but nothing will happen if you press it.

Here, we want to connect the Button's "pressed" signal to our Sprite2D, and we want to call a new function that will toggle its motion on and off. We need to have a script attached to the Sprite2D node, which we do from the previous lesson.

You can connect signals in the Node dock. Select the Button node and, on the right side of the editor, click on the tab named Node next to the Inspector.

The dock displays a list of signals available on the selected node.

Double-click the "pressed" signal to open the node connection window.

There, you can connect the signal to the Sprite2D node. The node needs a receiver method, a function that Godot will call when the Button emits the signal. The editor generates one for you. By convention, we name these callback methods "_on_node_name_signal_name". Here, it'll be "_on_button_pressed".

When connecting signals via the editor's Node dock, you can use two modes. The simple one only allows you to connect to nodes that have a script attached to them and creates a new callback function on them.

The advanced view lets you connect to any node and any built-in function, add arguments to the callback, and set options. You can toggle the mode in the window's bottom-right by clicking the Advanced button.

If you are using an external editor (such as VS Code), this automatic code generation might not work. In this case, you need to connect the signal via code as explained in the next section.

Click the Connect button to complete the signal connection and jump to the Script workspace. You should see the new method with a connection icon in the left margin.

If you click the icon, a window pops up and displays information about the connection. This feature is only available when connecting nodes in the editor.

Let's replace the line with the pass keyword with code that'll toggle the node's motion.

Our Sprite2D moves thanks to code in the _process() function. Godot provides a method to toggle processing on and off: Node.set_process(). Another method of the Node class, is_processing(), returns true if idle processing is active. We can use the not keyword to invert the value.

This function will toggle processing and, in turn, the icon's motion on and off upon pressing the button.

Before trying the game, we need to simplify our _process() function to move the node automatically and not wait for user input. Replace it with the following code, which we saw two lessons ago:

Your complete sprite_2d.gd code should look like the following.

Run the current scene by pressing F6 (Cmd + R on macOS), and click the button to see the sprite start and stop.

You can connect signals via code instead of using the editor. This is necessary when you create nodes or instantiate scenes inside of a script.

Let's use a different node here. Godot has a Timer node that's useful to implement skill cooldown times, weapon reloading, and more.

Head back to the 2D workspace. You can either click the "2D" text at the top of the window or press Ctrl + F1 (Ctrl + Cmd + 1 on macOS).

In the Scene dock, right-click on the Sprite2D node and add a new child node. Search for Timer and add the corresponding node. Your scene should now look like this.

With the Timer node selected, go to the Inspector and enable the Autostart property.

Click the script icon next to Sprite2D to jump back to the scripting workspace.

We need to do two operations to connect the nodes via code:

Get a reference to the Timer from the Sprite2D.

Call the connect() method on the Timer's "timeout" signal.

To connect to a signal via code, you need to call the connect() method of the signal you want to listen to. In this case, we want to listen to the Timer's "timeout" signal.

We want to connect the signal when the scene is instantiated, and we can do that using the Node._ready() built-in function, which is called automatically by the engine when a node is fully instantiated.

To get a reference to a node relative to the current one, we use the method Node.get_node(). We can store the reference in a variable.

The function get_node() looks at the Sprite2D's children and gets nodes by their name. For example, if you renamed the Timer node to "BlinkingTimer" in the editor, you would have to change the call to get_node("BlinkingTimer").

We can now connect the Timer to the Sprite2D in the _ready() function.

The line reads like so: we connect the Timer's "timeout" signal to the node to which the script is attached. When the Timer emits timeout, we want to call the function _on_timer_timeout(), that we need to define. Let's add it at the bottom of our script and use it to toggle our sprite's visibility.

By convention, we name these callback methods in GDScript as "_on_node_name_signal_name" and in C# as "OnNodeNameSignalName". Here, it'll be "_on_timer_timeout" for GDScript and OnTimerTimeout() for C#.

The visible property is a boolean that controls the visibility of our node. The line visible = not visible toggles the value. If visible is true, it becomes false, and vice-versa.

If you run the Node2D scene now, you will see that the sprite blinks on and off, at one second intervals.

That's it for our little moving and blinking Godot icon demo! Here is the complete sprite_2d.gd file for reference.

This section is a reference on how to define and use your own signals, and does not build upon the project created in previous lessons.

You can define custom signals in a script. Say, for example, that you want to show a game over screen when the player's health reaches zero. To do so, you could define a signal named "died" or "health_depleted" when their health reaches 0.

As signals represent events that just occurred, we generally use an action verb in the past tense in their names.

Your signals work the same way as built-in ones: they appear in the Node tab and you can connect to them like any other.

To emit a signal in your scripts, call emit() on the signal.

A signal can optionally declare one or more arguments. Specify the argument names between parentheses:

The signal arguments show up in the editor's node dock, and Godot can use them to generate callback functions for you. However, you can still emit any number of arguments when you emit signals. So it's up to you to emit the correct values.

To emit values along with the signal, add them as extra arguments to the emit() function:

Any node in Godot emits signals when something specific happens to them, like a button being pressed. Other nodes can connect to individual signals and react to selected events.

Signals have many uses. With them, you can react to a node entering or exiting the game world, to a collision, to a character entering or leaving an area, to an element of the interface changing size, and much more.

For example, an Area2D representing a coin emits a body_entered signal whenever the player's physics body enters its collision shape, allowing you to know when the player collected it.

In the next section, Your first 2D game, you'll create a complete 2D game and put everything you learned so far into practice.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (go):
```go
func _on_button_pressed():
    set_process(not is_processing())
```

Example 2 (json):
```json
// We also specified this function name in PascalCase in the editor's connection window.
private void OnButtonPressed()
{
    SetProcess(!IsProcessing());
}
```

Example 3 (gdscript):
```gdscript
func _process(delta):
    rotation += angular_speed * delta
    var velocity = Vector2.UP.rotated(rotation) * speed
    position += velocity * delta
```

Example 4 (gdscript):
```gdscript
public override void _Process(double delta)
{
    Rotation += _angularSpeed * (float)delta;
    var velocity = Vector2.Up.Rotated(Rotation) * _speed;
    Position += velocity * (float)delta;
}
```

---

## Your first 2D game — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_2d_game/index.html

**Contents:**
- Your first 2D game
- Prerequisites
- Contents

In this step-by-step tutorial series, you will create your first complete 2D game with Godot. By the end of the series, you will have a simple yet complete game of your own, like the image below.

You will learn how the Godot editor works, how to structure a project, and build a 2D game.

This project is an introduction to the Godot engine. It assumes that you have some programming experience already. If you're new to programming entirely, you should start here: Scripting languages.

The game is called "Dodge the Creeps!". Your character must move and avoid the enemies for as long as possible.

Create a complete 2D game with the Godot editor.

Structure a simple game project.

Move the player character and change its sprite.

Spawn random enemies.

You'll find another series where you'll create a similar game but in 3D. We recommend you to start with this one, though.

If you are new to game development or unfamiliar with Godot, we recommend starting with 2D games. This will allow you to become comfortable with both before tackling 3D games, which tend to be more complicated.

You can find a completed version of this project at this location:

https://github.com/godotengine/godot-demo-projects/tree/master/2d/dodge_the_creeps

This step-by-step tutorial is intended for beginners who followed the complete Step by step.

If you're an experienced programmer, you can find the complete demo's source code here: Dodge the Creeps source code.

We prepared some game assets you'll need to download so we can jump straight to the code.

You can download them by clicking the link below.

dodge_the_creeps_2d_assets.zip.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Setting up the project — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_2d_game/01.project_setup.html

**Contents:**
- Setting up the project
- Organizing the project
- User-contributed notes

In this short first part, we'll set up and organize the project.

Launch Godot and create a new project.

When creating the new project, you only need to choose a valid Project Path. You can leave the other default settings alone.

Download dodge_the_creeps_2d_assets.zip. The archive contains the images and sounds you'll be using to make the game. Extract the archive and move the art/ and fonts/ directories to your project's directory.

Download dodge_the_creeps_2d_assets.zip. The archive contains the images and sounds you'll be using to make the game. Extract the archive and move the art/ and fonts/ directories to your project's directory.

Ensure that you have the required dependencies to use C# in Godot. You need the latest stable .NET SDK, and an editor such as VS Code. See Prerequisites.

The C++ part of this tutorial wasn't rewritten for the new GDExtension system yet.

Your project folder should look like this.

This game is designed for portrait mode, so we need to adjust the size of the game window. Click on Project -> Project Settings to open the project settings window, in the left column open the Display -> Window tab. There, set "Viewport Width" to 480 and "Viewport Height" to 720. You can see the "Project" menu on the upper left corner.

Also, under the Stretch options, set Mode to canvas_items and Aspect to keep. This ensures that the game scales consistently on different sized screens.

In this project, we will make 3 independent scenes: Player, Mob, and HUD, which we will combine into the game's Main scene.

In a larger project, it might be useful to create folders to hold the various scenes and their scripts, but for this relatively small game, you can save your scenes and scripts in the project's root folder, identified by res://. You can see your project folders in the FileSystem dock in the lower left corner:

With the project in place, we're ready to design the player scene in the next lesson.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Creating the player scene — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_2d_game/02.player_scene.html

**Contents:**
- Creating the player scene
- Node structure
- Sprite animation
- User-contributed notes

With the project settings in place, we can start working on the player-controlled character.

The first scene will define the Player object. One of the benefits of creating a separate Player scene is that we can test it separately, even before we've created other parts of the game.

To begin, we need to choose a root node for the player object. As a general rule, a scene's root node should reflect the object's desired functionality - what the object is. In the upper-left corner, in the "Scene" tab, click the "Other Node" button and add an Area2D node to the scene.

When you add the Area2D node, Godot will display the following warning icon next to it in the scene tree:

This warning tells us that the Area2D node requires a shape to detect collisions or overlaps. We can ignore the warning temporarily because we will first set up the player's visuals (using an animated sprite). Once the visuals are ready, we will add a collision shape as a child node. This will allow us to accurately size and position the shape based on the sprite's appearance.

With Area2D we can detect objects that overlap or run into the player. Change the node's name to Player by double-clicking on it. Now that we've set the scene's root node, we can add additional nodes to give it more functionality.

Before we add any children to the Player node, we want to make sure we don't accidentally move or resize them by clicking on them. Select the node and click the icon to the right of the lock. Its tooltip says "Groups the selected node with its children. This causes the parent to be selected when any child node is clicked in 2D and 3D view."

Save the scene as player.tscn. Click Scene > Save, or press Ctrl + S on Windows/Linux or Cmd + S on macOS.

For this project, we will be following the Godot naming conventions.

GDScript: Classes (nodes) use PascalCase, variables and functions use snake_case, and constants use ALL_CAPS (See GDScript style guide).

C#: Classes, export variables and methods use PascalCase, private fields use _camelCase, local variables and parameters use camelCase (See C# style guide). Be careful to type the method names precisely when connecting signals.

Click on the Player node and add (Ctrl + A on Windows/Linux or Cmd + A on macOS) a child node AnimatedSprite2D. The AnimatedSprite2D will handle the appearance and animations for our player. Notice that there is a warning symbol next to the node. An AnimatedSprite2D requires a SpriteFrames resource, which is a list of the animations it can display. Make sure AnimatedSprite2D is selected and then find the Sprite Frames property under the Animation section in the Inspector and click "[empty]" -> "New SpriteFrames":

Click on the SpriteFrames you just created to open the "SpriteFrames" panel:

On the left is a list of animations. Click the default one and rename it to walk. Then click the Add Animation button to create a second animation named up.

Find the player images in the FileSystem dock - they're in the art folder you unzipped earlier. Drag the two images for each animation, into the Animation Frames side of the panel for the corresponding animation:

playerGrey_walk1 and playerGrey_walk2 for the walk animation

playerGrey_up1 and playerGrey_up2 for the up animation

The player images are a bit too large for the game window, so we need to scale them down. Click on the AnimatedSprite2D node and set the Scale property to (0.5, 0.5). You can find it in the Inspector under the Node2D heading.

Finally, add a CollisionShape2D as a child of Player. This will determine the player's "hitbox", or the bounds of its collision area. For this character, a CapsuleShape2D node gives the best fit, so next to "Shape" in the Inspector, click "[empty]" -> "New CapsuleShape2D". Using the two size handles, resize the shape to cover the sprite:

When you're finished, your Player scene should look like this:

Once this is done, the warning on the Area2D node will disappear, as it now has a shape assigned and can interact with other objects.

Make sure to save the scene again after these changes.

In the next part, we'll add a script to the player node to move and animate it. Then, we'll set up collision detection to know when the player got hit by something.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Coding the player — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_2d_game/03.coding_the_player.html

**Contents:**
- Coding the player
- Choosing animations
- Preparing for collisions
- User-contributed notes

In this lesson, we'll add player movement, animation, and set it up to detect collisions.

To do so, we need to add some functionality that we can't get from a built-in node, so we'll add a script. Click the Player node and click the "Attach Script" button:

In the script settings window, you can leave the default settings alone. Just click "Create":

If you're creating a C# script or other languages, select the language from the language drop down menu before hitting create.

If this is your first time encountering GDScript, please read Scripting languages before continuing.

Start by declaring the member variables this object will need:

Using the export keyword on the first variable speed allows us to set its value in the Inspector. This can be handy for values that you want to be able to adjust just like a node's built-in properties. Click on the Player node and you'll see the property now appears in the Inspector in a new section with the name of the script. Remember, if you change the value here, it will override the value written in the script.

If you're using C#, you need to (re)build the project assemblies whenever you want to see new export variables or signals. This build can be manually triggered by clicking the Build button at the top right of the editor.

Your player.gd script should already contain a _ready() and a _process() function. If you didn't select the default template shown above, create these functions while following the lesson.

The _ready() function is called when a node enters the scene tree, which is a good time to find the size of the game window:

Now we can use the _process() function to define what the player will do. _process() is called every frame, so we'll use it to update elements of our game, which we expect will change often. For the player, we need to do the following:

Move in the given direction.

Play the appropriate animation.

First, we need to check for input - is the player pressing a key? For this game, we have 4 direction inputs to check. Input actions are defined in the Project Settings under "Input Map". Here, you can define custom events and assign different keys, mouse events, or other inputs to them. For this game, we will map the arrow keys to the four directions.

Click on Project -> Project Settings to open the project settings window and click on the Input Map tab at the top. Type "move_right" in the top bar and click the "Add" button to add the move_right action.

We need to assign a key to this action. Click the "+" icon on the right, to open the event manager window.

The "Listening for Input..." field should automatically be selected. Press the "right" key on your keyboard, and the menu should look like this now.

Select the "ok" button. The "right" key is now associated with the move_right action.

Repeat these steps to add three more mappings:

move_left mapped to the left arrow key.

move_up mapped to the up arrow key.

And move_down mapped to the down arrow key.

Your input map tab should look like this:

Click the "Close" button to close the project settings.

We only mapped one key to each input action, but you can map multiple keys, joystick buttons, or mouse buttons to the same input action.

You can detect whether a key is pressed using Input.is_action_pressed(), which returns true if it's pressed or false if it isn't.

We start by setting the velocity to (0, 0) - by default, the player should not be moving. Then we check each input and add/subtract from the velocity to obtain a total direction. For example, if you hold right and down at the same time, the resulting velocity vector will be (1, 1). In this case, since we're adding a horizontal and a vertical movement, the player would move faster diagonally than if it just moved horizontally.

We can prevent that if we normalize the velocity, which means we set its length to 1, then multiply by the desired speed. This means no more fast diagonal movement.

If you've never used vector math before, or need a refresher, you can see an explanation of vector usage in Godot at Vector math. It's good to know but won't be necessary for the rest of this tutorial.

We also check whether the player is moving so we can call play() or stop() on the AnimatedSprite2D.

$ is shorthand for get_node(). So in the code above, $AnimatedSprite2D.play() is the same as get_node("AnimatedSprite2D").play().

In GDScript, $ returns the node at the relative path from the current node, or returns null if the node is not found. Since AnimatedSprite2D is a child of the current node, we can use $AnimatedSprite2D.

Now that we have a movement direction, we can update the player's position. We can also use clamp() to prevent it from leaving the screen. Clamping a value means restricting it to a given range. Add the following to the bottom of the _process function (make sure it's not indented under the else):

The delta parameter in the _process() function refers to the frame length - the amount of time that the previous frame took to complete. Using this value ensures that your movement will remain consistent even if the frame rate changes.

Click "Run Current Scene" (F6, Cmd + R on macOS) and confirm you can move the player around the screen in all directions.

If you get an error in the "Debugger" panel that says

Attempt to call function 'play' in base 'null instance' on a null instance

this likely means you spelled the name of the AnimatedSprite2D node wrong. Node names are case-sensitive and $NodeName must match the name you see in the scene tree.

Now that the player can move, we need to change which animation the AnimatedSprite2D is playing based on its direction. We have the "walk" animation, which shows the player walking to the right. This animation should be flipped horizontally using the flip_h property for left movement. We also have the "up" animation, which should be flipped vertically with flip_v for downward movement. Let's place this code at the end of the _process() function:

The boolean assignments in the code above are a common shorthand for programmers. Since we're doing a comparison test (boolean) and also assigning a boolean value, we can do both at the same time. Consider this code versus the one-line boolean assignment above:

Play the scene again and check that the animations are correct in each of the directions.

A common mistake here is to type the names of the animations wrong. The animation names in the SpriteFrames panel must match what you type in the code. If you named the animation "Walk", you must also use a capital "W" in the code.

When you're sure the movement is working correctly, add this line to _ready(), so the player will be hidden when the game starts:

We want Player to detect when it's hit by an enemy, but we haven't made any enemies yet! That's OK, because we're going to use Godot's signal functionality to make it work.

Add the following at the top of the script. If you're using GDScript, add it after extends Area2D. If you're using C#, add it after public partial class Player : Area2D:

This defines a custom signal called "hit" that we will have our player emit (send out) when it collides with an enemy. We will use Area2D to detect the collision. Select the Player node and click the "Node" tab next to the Inspector tab to see the list of signals the player can emit:

Notice our custom "hit" signal is there as well! Since our enemies are going to be RigidBody2D nodes, we want the body_entered(body: Node2D) signal. This signal will be emitted when a body contacts the player. Click "Connect.." and the "Connect a Signal" window appears.

Godot will create a function with that exact name directly in script for you. You don't need to change the default settings right now.

If you're using an external text editor (for example, Visual Studio Code), a bug currently prevents Godot from doing so. You'll be sent to your external editor, but the new function won't be there.

In this case, you'll need to write the function yourself into the Player's script file.

Note the green icon indicating that a signal is connected to this function; this does not mean the function exists, only that the signal will attempt to connect to a function with that name, so double-check that the spelling of the function matches exactly!

Next, add this code to the function:

Each time an enemy hits the player, the signal is going to be emitted. We need to disable the player's collision so that we don't trigger the hit signal more than once.

Disabling the area's collision shape can cause an error if it happens in the middle of the engine's collision processing. Using set_deferred() tells Godot to wait to disable the shape until it's safe to do so.

The last piece is to add a function we can call to reset the player when starting a new game.

With the player working, we'll work on the enemy in the next lesson.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Area2D

@export var speed = 400 # How fast the player will move (pixels/sec).
var screen_size # Size of the game window.
```

Example 2 (csharp):
```csharp
using Godot;

public partial class Player : Area2D
{
    [Export]
    public int Speed { get; set; } = 400; // How fast the player will move (pixels/sec).

    public Vector2 ScreenSize; // Size of the game window.
}
```

Example 3 (gdscript):
```gdscript
func _ready():
    screen_size = get_viewport_rect().size
```

Example 4 (gdscript):
```gdscript
public override void _Ready()
{
    ScreenSize = GetViewportRect().Size;
}
```

---

## Creating the enemy — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_2d_game/04.creating_the_enemy.html

**Contents:**
- Creating the enemy
- Node setup
- Enemy script
- User-contributed notes

Now it's time to make the enemies our player will have to dodge. Their behavior will not be very complex: mobs will spawn randomly at the edges of the screen, choose a random direction, and move in a straight line.

We'll create a Mob scene, which we can then instance to create any number of independent mobs in the game.

Click Scene -> New Scene from the top menu and add the following nodes:

RigidBody2D (named Mob)

VisibleOnScreenNotifier2D

Don't forget to set the children so they can't be selected, like you did with the Player scene. This is done by selecting the parent node (RigidBody2D) in the Scene tree dock, then using the Group button at the top of the 2D editor (or pressing Ctrl + G).

Select the Mob node and set its Gravity Scale property in the RigidBody2D section of the inspector to 0. This will prevent the mob from falling downwards.

In addition, under the CollisionObject2D section just beneath the RigidBody2D section, expand the Collision group and uncheck the 1 inside the Mask property. This will ensure the mobs do not collide with each other.

Set up the AnimatedSprite2D like you did for the player. This time, we have 3 animations: fly, swim, and walk. There are two images for each animation in the art folder.

The Animation Speed property has to be set for each individual animation. Adjust it to 3 for all 3 animations.

You can use the "Play Animation" buttons on the right of the Animation Speed input field to preview your animations.

We'll select one of these animations randomly so that the mobs will have some variety.

Like the player images, these mob images need to be scaled down. Set the AnimatedSprite2D's Scale property to (0.75, 0.75).

As in the Player scene, add a CapsuleShape2D for the collision. To align the shape with the image, you'll need to set the Rotation property to 90 (under "Transform" in the Inspector).

Add a script to the Mob like this:

Now let's look at the rest of the script. In _ready() we play the animation and randomly choose one of the three animation types:

First, we get the list of animation names from the AnimatedSprite2D's sprite_frames property. This returns an Array containing all three animation names: ["walk", "swim", "fly"].

In the GDScript code, we use the Array.pick_random method to select one of these animation names at random. Meanwhile, in the C# code, we pick a random number between 0 and 2 to select one of these names from the list (array indices start at 0). The expression GD.Randi() % n selects a random integer between 0 and n-1.

Finally, we call play() to start playing the chosen animation.

The last piece is to make the mobs delete themselves when they leave the screen. Connect the screen_exited() signal of the VisibleOnScreenNotifier2D node to the Mob and add this code:

queue_free() is a function that essentially 'frees', or deletes, the node at the end of the frame.

This completes the Mob scene.

With the player and enemies ready, in the next part, we'll bring them together in a new scene. We'll make enemies spawn randomly around the game board and move forward, turning our project into a playable game.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends RigidBody2D
```

Example 2 (swift):
```swift
using Godot;

public partial class Mob : RigidBody2D
{
    // Don't forget to rebuild the project.
}
```

Example 3 (gdscript):
```gdscript
func _ready():
    var mob_types = Array($AnimatedSprite2D.sprite_frames.get_animation_names())
    $AnimatedSprite2D.animation = mob_types.pick_random()
    $AnimatedSprite2D.play()
```

Example 4 (gdscript):
```gdscript
public override void _Ready()
{
    var animatedSprite2D = GetNode<AnimatedSprite2D>("AnimatedSprite2D");
    string[] mobTypes = animatedSprite2D.SpriteFrames.GetAnimationNames();
    animatedSprite2D.Play(mobTypes[GD.Randi() % mobTypes.Length]);
}
```

---

## The main game scene — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_2d_game/05.the_main_game_scene.html

**Contents:**
- The main game scene
- Spawning mobs
- Main script
- Testing the scene
- User-contributed notes

Now it's time to bring everything we did together into a playable game scene.

Create a new scene and add a Node named Main. (The reason we are using Node instead of Node2D is because this node will be a container for handling game logic. It does not require 2D functionality itself.)

Click the Instance button (represented by a chain link icon) and select your saved player.tscn.

Now, add the following nodes as children of Main, and name them as shown:

Timer (named MobTimer) - to control how often mobs spawn

Timer (named ScoreTimer) - to increment the score every second

Timer (named StartTimer) - to give a delay before starting

Marker2D (named StartPosition) - to indicate the player's start position

Set the Wait Time property of each of the Timer nodes as follows (values are in seconds):

In addition, set the One Shot property of StartTimer to "On" and set Position of the StartPosition node to (240, 450).

The Main node will be spawning new mobs, and we want them to appear at a random location on the edge of the screen. Click the Main node in the Scene dock, then add a child Path2D node named MobPath. When you select Path2D, you will see some new buttons at the top of the editor:

Select the middle one ("Add Point") and draw the path by clicking to add the points at the corners shown. To have the points snap to the grid, make sure "Use Grid Snap" and "Use Smart Snap" are both selected. These options can be found to the left of the "Lock" button, appearing as a magnet next to some dots and intersecting lines, respectively.

Draw the path in clockwise order, or your mobs will spawn pointing outwards instead of inwards!

After placing point 4 in the image, click the "Close Curve" button and your curve will be complete.

Now that the path is defined, add a PathFollow2D node as a child of MobPath and name it MobSpawnLocation. This node will automatically rotate and follow the path as it moves, so we can use it to select a random position and direction along the path.

Your scene should look like this:

Add a script to Main. At the top of the script, we use @export var mob_scene: PackedScene to allow us to choose the Mob scene we want to instance.

Click the Main node and you will see the Mob Scene property in the Inspector under "Main.gd".

You can assign this property's value in two ways:

Drag mob.tscn from the "FileSystem" dock and drop it in the Mob Scene property.

Click the down arrow next to "[empty]" and choose "Load". Select mob.tscn.

Next, select the instance of the Player scene under Main node in the Scene dock, and access the Node dock on the sidebar. Make sure to have the Signals tab selected in the Node dock.

You should see a list of the signals for the Player node. Find and double-click the hit signal in the list (or right-click it and select "Connect..."). This will open the signal connection dialog. We want to make a new function named game_over, which will handle what needs to happen when a game ends. Type "game_over" in the "Receiver Method" box at the bottom of the signal connection dialog and click "Connect". You are aiming to have the hit signal emitted from Player and handled in the Main script. Add the following code to the new function, as well as a new_game function that will set everything up for a new game:

Now we'll connect the timeout() signal of each Timer node (StartTimer, ScoreTimer, and MobTimer) to the main script. For each of the three timers, select the timer in the Scene dock, open the Signals tab of the Node dock, then double-click the timeout() signal in the list. This will open a new signal connection dialog. The default settings in this dialog should be fine, so select Connect to create a new signal connection.

Once all three timers have this set up, you should be able to see each timer have a Signal connection for their respective timeout() signal, showing in green, within their respective Signals tabs:

(For MobTimer): _on_mob_timer_timeout()

(For ScoreTimer): _on_score_timer_timeout()

(For StartTimer): _on_start_timer_timeout()

Now we define how each of these timers operate by adding the code below. Notice that StartTimer will start the other two timers, and that ScoreTimer will increment the score by 1.

In _on_mob_timer_timeout(), we will create a mob instance, pick a random starting location along the Path2D, and set the mob in motion. The PathFollow2D node will automatically rotate as it follows the path, so we will use that to select the mob's direction as well as its position. When we spawn a mob, we'll pick a random value between 150.0 and 250.0 for how fast each mob will move (it would be boring if they were all moving at the same speed).

Note that a new instance must be added to the scene using add_child().

Why PI? In functions requiring angles, Godot uses radians, not degrees. Pi represents a half turn in radians, about 3.1415 (there is also TAU which is equal to 2 * PI). If you're more comfortable working with degrees, you'll need to use the deg_to_rad() and rad_to_deg() functions to convert between the two.

Let's test the scene to make sure everything is working. Add this new_game call to _ready():

Let's also assign Main as our "Main Scene" - the one that runs automatically when the game launches. Press the "Play" button and select main.tscn when prompted.

If you had already set another scene as the "Main Scene", you can right click main.tscn in the FileSystem dock and select "Set As Main Scene".

You should be able to move the player around, see mobs spawning, and see the player disappear when hit by a mob.

When you're sure everything is working, remove the call to new_game() from _ready() and replace it with pass.

What's our game lacking? Some user interface. In the next lesson, we'll add a title screen and display the player's score.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
extends Node

@export var mob_scene: PackedScene
var score
```

Example 2 (json):
```json
using Godot;

public partial class Main : Node
{
    // Don't forget to rebuild the project so the editor knows about the new export variable.

    [Export]
    public PackedScene MobScene { get; set; }

    private int _score;
}
```

Example 3 (typescript):
```typescript
func game_over():
    $ScoreTimer.stop()
    $MobTimer.stop()

func new_game():
    score = 0
    $Player.start($StartPosition.position)
    $StartTimer.start()
```

Example 4 (gdscript):
```gdscript
public void GameOver()
{
    GetNode<Timer>("MobTimer").Stop();
    GetNode<Timer>("ScoreTimer").Stop();
}

public void NewGame()
{
    _score = 0;

    var player = GetNode<Player>("Player");
    var startPosition = GetNode<Marker2D>("StartPosition");
    player.Start(startPosition.Position);

    GetNode<Timer>("StartTimer").Start();
}
```

---

## Heads up display — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_2d_game/06.heads_up_display.html

**Contents:**
- Heads up display
- ScoreLabel
- Message
- StartButton
- Connecting HUD to Main
- Removing old creeps
- User-contributed notes

The final piece our game needs is a User Interface (UI) to display things like score, a "game over" message, and a restart button.

Create a new scene, click the "Other Node" button and add a CanvasLayer node named HUD. "HUD" stands for "heads-up display", an informational display that appears as an overlay on top of the game view.

The CanvasLayer node lets us draw our UI elements on a layer above the rest of the game, so that the information it displays isn't covered up by any game elements like the player or mobs.

The HUD needs to display the following information:

Score, changed by ScoreTimer.

A message, such as "Game Over" or "Get Ready!"

A "Start" button to begin the game.

The basic node for UI elements is Control. To create our UI, we'll use two types of Control nodes: Label and Button.

Create the following as children of the HUD node:

Label named ScoreLabel.

Button named StartButton.

Timer named MessageTimer.

Click on the ScoreLabel and type a number into the Text field in the Inspector. The default font for Control nodes is small and doesn't scale well. There is a font file included in the game assets called "Xolonium-Regular.ttf". To use this font, do the following:

Under "Theme Overrides > Fonts", choose "Load" and select the "Xolonium-Regular.ttf" file.

The font size is still too small, increase it to 64 under "Theme Overrides > Font Sizes". Once you've done this with the ScoreLabel, repeat the changes for the Message and StartButton nodes.

Anchors: Control nodes have a position and size, but they also have anchors. Anchors define the origin - the reference point for the edges of the node.

Arrange the nodes as shown below. You can drag the nodes to place them manually, or for more precise placement, use "Anchor Presets".

Set the "Horizontal Alignment" and "Vertical Alignment" to Center.

Choose the "Anchor Preset" Center Top.

Add the text Dodge the Creeps!.

Set the "Horizontal Alignment" and "Vertical Alignment" to Center.

Set the "Autowrap Mode" to Word, otherwise the label will stay on one line.

Under "Control - Layout/Transform" set "Size X" to 480 to use the entire width of the screen.

Choose the "Anchor Preset" Center.

Under "Control - Layout/Transform", set "Size X" to 200 and "Size Y" to 100 to add a little bit more padding between the border and text.

Choose the "Anchor Preset" Center Bottom.

Under "Control - Layout/Transform", set "Position Y" to 580.

On the MessageTimer, set the Wait Time to 2 and set the One Shot property to "On".

Now add this script to HUD:

We now want to display a message temporarily, such as "Get Ready", so we add the following code

We also need to process what happens when the player loses. The code below will show "Game Over" for 2 seconds, then return to the title screen and, after a brief pause, show the "Start" button.

When you need to pause for a brief time, an alternative to using a Timer node is to use the SceneTree's create_timer() function. This can be very useful to add delays such as in the above code, where we want to wait some time before showing the "Start" button.

Add the code below to HUD to update the score

Connect the pressed() signal of StartButton and the timeout() signal of MessageTimer to the HUD node, and add the following code to the new functions:

Now that we're done creating the HUD scene, go back to Main. Instance the HUD scene in Main like you did the Player scene. The scene tree should look like this, so make sure you didn't miss anything:

Now we need to connect the HUD functionality to our Main script. This requires a few additions to the Main scene:

In the Node tab, connect the HUD's start_game signal to the new_game() function of the Main node by clicking the "Pick" button in the "Connect a Signal" window and selecting the new_game() method or type "new_game" below "Receiver Method" in the window. Verify that the green connection icon now appears next to func new_game() in the script.

In new_game(), update the score display and show the "Get Ready" message:

In game_over() we need to call the corresponding HUD function:

Finally, add this to _on_score_timer_timeout() to keep the display in sync with the changing score:

Remember to remove the call to new_game() from _ready() if you haven't already, otherwise your game will start automatically.

Now you're ready to play! Click the "Play the Project" button.

If you play until "Game Over" and then start a new game right away, the creeps from the previous game may still be on the screen. It would be better if they all disappeared at the start of a new game. We just need a way to tell all the mobs to remove themselves. We can do this with the "group" feature.

In the Mob scene, select the root node and click the "Node" tab next to the Inspector (the same place where you find the node's signals). Next to "Signals", click "Groups" to open the group overview and the "+" button to open the "Create New Group" dialog.

Name the group mobs and click "ok" to add a new scene group.

Now all mobs will be in the "mobs" group.

We can then add the following line to the new_game() function in Main:

The call_group() function calls the named function on every node in a group - in this case we are telling every mob to delete itself.

The game's mostly done at this point. In the next and last part, we'll polish it a bit by adding a background, looping music, and some keyboard shortcuts.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends CanvasLayer

# Notifies `Main` node that the button has been pressed
signal start_game
```

Example 2 (json):
```json
using Godot;

public partial class HUD : CanvasLayer
{
    // Don't forget to rebuild the project so the editor knows about the new signal.

    [Signal]
    public delegate void StartGameEventHandler();
}
```

Example 3 (go):
```go
func show_message(text):
    $Message.text = text
    $Message.show()
    $MessageTimer.start()
```

Example 4 (gdscript):
```gdscript
public void ShowMessage(string text)
{
    var message = GetNode<Label>("Message");
    message.Text = text;
    message.Show();

    GetNode<Timer>("MessageTimer").Start();
}
```

---

## Finishing up — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_2d_game/07.finishing-up.html

**Contents:**
- Finishing up
- Background
- Sound effects
- Keyboard shortcut
- Sharing the finished game with others
- User-contributed notes

We have now completed all the functionality for our game. Below are some remaining steps to add a bit more "juice" to improve the game experience.

Feel free to expand the gameplay with your own ideas.

The default gray background is not very appealing, so let's change its color. One way to do this is to use a ColorRect node. Make it the first node under Main so that it will be drawn behind the other nodes. ColorRect only has one property: Color. Choose a color you like and select "Layout" -> "Anchors Preset" -> "Full Rect" either in the toolbar at the top of the viewport or in the inspector so that it covers the screen.

You could also add a background image, if you have one, by using a TextureRect node instead.

Sound and music can be the single most effective way to add appeal to the game experience. In your game's art folder, you have two sound files: "House In a Forest Loop.ogg" for background music, and "gameover.wav" for when the player loses.

Add two AudioStreamPlayer nodes as children of Main. Name one of them Music and the other DeathSound. On each one, click on the Stream property, select "Load", and choose the corresponding audio file.

All audio is automatically imported with the Loop setting disabled. If you want the music to loop seamlessly, click on the Stream file arrow, select Make Unique, then click on the Stream file and check the Loop box.

To play the music, add $Music.play() in the new_game() function and $Music.stop() in the game_over() function.

Finally, add $DeathSound.play() in the game_over() function.

Since the game is played with keyboard controls, it would be convenient if we could also start the game by pressing a key on the keyboard. We can do this with the "Shortcut" property of the Button node.

In a previous lesson, we created four input actions to move the character. We will create a similar input action to map to the start button.

Select "Project" -> "Project Settings" and then click on the "Input Map" tab. In the same way you created the movement input actions, create a new input action called start_game and add a key mapping for the Enter key.

Now would be a good time to add controller support if you have one available. Attach or pair your controller and then under each input action that you wish to add controller support for, click on the "+" button and press the corresponding button, d-pad, or stick direction that you want to map to the respective input action.

In the HUD scene, select the StartButton and find its Shortcut property in the Inspector. Create a new Shortcut resource by clicking within the box, open the Events array and add a new array element to it by clicking on Array[InputEvent] (size 0).

Create a new InputEventAction and name it start_game.

Now when the start button appears, you can either click it or press Enter to start the game.

And with that, you completed your first 2D game in Godot.

You got to make a player-controlled character, enemies that spawn randomly around the game board, count the score, implement a game over and replay, user interface, sounds, and more. Congratulations!

There's still much to learn, but you can take a moment to appreciate what you achieved.

And when you're ready, you can move on to Your first 3D game to learn to create a complete 3D game from scratch, in Godot.

If you want people to try out your game without having to install Godot, you'll need to export the project for each operating system you want the game to be playable on. See Exporting projects for instructions.

After exporting the project, compress the exported executable and PCK file (not the raw project files) to a ZIP file, then upload this ZIP file to a file sharing website.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (go):
```go
func game_over():
    ...
    $Music.stop()
    $DeathSound.play()

func new_game():
    ...
    $Music.play()
```

Example 2 (json):
```json
public void GameOver()
{
    ...
    GetNode<AudioStreamPlayer>("Music").Stop();
    GetNode<AudioStreamPlayer>("DeathSound").Play();
}

public void NewGame()
{
    ...
    GetNode<AudioStreamPlayer>("Music").Play();
}
```

---

## Your first 3D game — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/index.html

**Contents:**
- Your first 3D game
- Contents

In this step-by-step tutorial series, you will create your first complete 3D game with Godot. By the end of the series, you will have a simple yet finished project of your own like the animated gif below.

The game we'll code here is similar to Your first 2D game, with a twist: you can now jump and your goal is to squash the creeps. This way, you will both recognize patterns you learned in the previous tutorial and build upon them with new code and features.

Work with 3D coordinates with a jumping mechanic.

Use kinematic bodies to move 3D characters and detect when and how they collide.

Use physics layers and a group to detect interactions with specific entities.

Code basic procedural gameplay by instancing monsters at regular time intervals.

Design a movement animation and change its speed at runtime.

Draw a user interface on a 3D game.

This tutorial is for beginners who followed the complete getting started series. We'll start slow with detailed instructions and shorten them as we do similar steps. If you're an experienced programmer, you can browse the complete demo's source code here: Squash the Creep source code.

You can follow this series without having done the 2D one. However, if you're new to game development, we recommend you to start with 2D. 3D game code is always more complex and the 2D series will give you foundations to follow along more comfortably.

We prepared some game assets so we can jump straight to the code. You can download them here: Squash the Creeps assets.

We will first work on a basic prototype for the player's movement. We will then add the monsters that we'll spawn randomly around the screen. After that, we'll implement the jump and squashing mechanic before refining the game with some nice animation. We'll wrap up with the score and the retry screen.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Setting up the game area — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/01.game_setup.html

**Contents:**
- Setting up the game area
- Setting up the playable area
- User-contributed notes

In this first part, we're going to set up the game area. Let's get started by importing the start assets and setting up the game scene.

We've prepared a Godot project with the 3D models and sounds we'll use for this tutorial, linked in the index page. If you haven't done so yet, you can download the archive here: Squash the Creeps assets.

Once you downloaded it, extract the .zip archive on your computer. Open the Godot Project Manager and click the Import button.

In the import popup, enter the full path to the freshly created directory 3d_squash_the_creeps_starter/. You can click the Browse button on the right to open a file browser and navigate to the project.godot file the folder contains.

Click Import to open the project in the editor.

A window notifying you that the project was generated by an older Godot version may appear. Click OK to convert the project to your current Godot version.

If it doesn't open immediately open the project from your project list.

The start project contains an icon and two folders: art/ and fonts/. There, you will find the art assets and music we'll use in the game.

There are two 3D models, player.glb and mob.glb, some materials that belong to these models, and a music track.

We're going to create our main scene with a plain Node as its root. In the Scene dock, click the Add Child Node button represented by a "+" icon in the top-left and double-click on Node. Name the node Main. An alternate method to rename the node is to right-click on Node and choose Rename (or F2). Alternatively, to add a node to the scene, you can press Ctrl + A (Cmd + A on macOS).

Save the scene as main.tscn by pressing Ctrl + S (Cmd + S on macOS).

We'll start by adding a floor that'll prevent the characters from falling. To create static colliders like the floor, walls, or ceilings, you can use StaticBody3D nodes. They require CollisionShape3D child nodes to define the collision area. With the Main node selected, add a StaticBody3D node, then a CollisionShape3D. Rename the StaticBody3D to Ground.

Your scene tree should look like this

A warning sign next to the CollisionShape3D appears because we haven't defined its shape. If you click the icon, a popup appears to give you more information.

To create a shape, select the CollisionShape3D node, head to the Inspector and click the <empty> field next to the Shape property. Create a new BoxShape3D.

The box shape is perfect for flat ground and walls. Its thickness makes it reliable to block even fast-moving objects.

A box's wireframe appears in the viewport with three orange dots. You can click and drag these to edit the shape's extents interactively. We can also precisely set the size in the inspector. Click on the BoxShape3D to expand the resource. Set its Size to 60 on the X-axis, 2 for the Y-axis, and 60 for the Z-axis.

Collision shapes are invisible. We need to add a visual floor that goes along with it. Select the Ground node and add a MeshInstance3D as its child.

In the Inspector, click on the field next to Mesh and create a BoxMesh resource to create a visible box.

Once again, it's too small by default. Click the box icon to expand the resource and set its Size to 60, 2, and 60.

You should see a wide grey slab that covers the grid and blue and red axes in the viewport.

We're going to move the ground down so we can see the floor grid. To do this, the grid snapping feature can be used. Grid snapping can be activated 2 ways in the 3D editor. The first is by pressing the Use Snap button (or pressing the Y key). The second is by selecting a node, dragging a handle on the gizmo then holding Ctrl while still clicking to enable snapping as long as Ctrl is held.

Start by setting snapping with your preferred method. Then move the Ground node using the Y-axis (the green arrow on the gizmo).

If you can't see the 3D object manipulator like on the image above, ensure the Select Mode is active in the toolbar above the view.

Move the ground down 1 meter, in order to have a visible editor grid. A label in the bottom-left corner of the viewport tells you how much you're translating the node.

Moving the Ground node down moves both children along with it. Ensure you move the Ground node, not the MeshInstance3D or the CollisionShape3D.

Ultimately, Ground's transform.position.y should be -1

Let's add a directional light so our scene isn't all grey. Select the Main node and add a child node DirectionalLight3D.

We need to move and rotate the DirectionalLight3D node. Move it up by clicking and dragging on the manipulator's green arrow and click and drag on the red arc to rotate it around the X-axis, until the ground is lit.

In the Inspector, turn on Shadow by clicking the checkbox.

At this point, your project should look like this.

That's our starting point. In the next part, we will work on the player scene and base movement.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Player scene and input actions — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/02.player_input.html

**Contents:**
- Player scene and input actions
- Creating input actions
- User-contributed notes

In the next two lessons, we will design the player scene, register custom input actions, and code player movement. By the end, you'll have a playable character that moves in eight directions.

Create a new scene by going to the Scene menu in the top-left and clicking New Scene.

Click the Other Node button and select the CharacterBody3D node type to create a CharacterBody3D as the root node.

Rename the CharacterBody3D to Player. Character bodies are complementary to the area and rigid bodies used in the 2D game tutorial. Like rigid bodies, they can move and collide with the environment, but instead of being controlled by the physics engine, you dictate their movement. You will see how we use the node's unique features when we code the jump and squash mechanics.

To learn more about the different physics node types, see the Physics introduction.

For now, we're going to create a basic rig for our character's 3D model. This will allow us to rotate the model later via code while it plays an animation.

Add a Node3D node as a child of Player. Select the Player node in the Scene tree and click the "+" button to add a child node. Rename it to Pivot.

Then, in the FileSystem dock, expand the art/ folder by double-clicking it and drag and drop player.glb onto Pivot.

This should instantiate the model as a child of Pivot. You can rename it to Character.

The .glb files contain 3D scene data based on the open source glTF 2.0 specification. They're a modern and powerful alternative to a proprietary format like FBX, which Godot also supports. To produce these files, we designed the model in Blender 3D and exported it to glTF.

As with all kinds of physics nodes, we need a collision shape for our character to collide with the environment. Select the Player node again and add a child node CollisionShape3D. In the Inspector, on the Shape property, add a new SphereShape3D.

The sphere's wireframe appears below the character.

It will be the shape the physics engine uses to collide with the environment, so we want it to better fit the 3D model. Make it a bit larger by dragging the orange dot in the viewport. My sphere has a radius of about 0.8 meters.

Then, move the collision shape up so its bottom roughly aligns with the grid's plane.

To make moving the shape easier, you can toggle the model's visibility by clicking the eye icon next to the Character or the Pivot nodes.

Save the scene as player.tscn.

With the nodes ready, we can almost get coding. But first, we need to define some input actions.

To move the character, we will listen to the player's input, like pressing the arrow keys. In Godot, while we could write all the key bindings in code, there's a powerful system that allows you to assign a label to a set of keys and buttons. This simplifies our scripts and makes them more readable.

This system is the Input Map. To access its editor, head to the Project menu and select Project Settings....

At the top, there are multiple tabs. Click on Input Map. This window allows you to add new actions at the top; they are your labels. In the bottom part, you can bind keys to these actions.

Godot projects come with some predefined actions designed for user interface design (see above screenshot). These will become visible if you enable the Show Built-in Actions toggle. We could use these here, but instead we're defining our own to support gamepads. Leave Show Built-in Actions disabled.

We're going to name our actions move_left, move_right, move_forward, move_back, and jump.

To add an action, write its name in the bar at the top and press Enter or click the Add button.

Create the following five actions:

To bind a key or button to an action, click the "+" button to its right. Do this for move_left. Press the left arrow key and click OK.

Bind also the A key, onto the action move_left.

Let's now add support for a gamepad's left joystick. Click the "+" button again but this time, select the input within the input tree yourself. Select the negative X axis of the left joystick under Joypad Axes.

Leave the other values as default and press OK.

If you want controllers to have different input actions, you should use the Devices option in Additional Options. Device 0 corresponds to the first plugged gamepad, Device 1 corresponds to the second plugged gamepad, and so on.

Do the same for the other input actions. For example, bind the right arrow, D, and the left joystick's positive axis to move_right. After binding all keys, your interface should look like this.

The final action to set up is the jump action. Bind the Space key and the gamepad's A button located under Joypad Buttons.

Your jump input action should look like this.

That's all the actions we need for this game. You can use this menu to label any groups of keys and buttons in your projects.

In the next part, we'll code and test the player's movement.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Moving the player with code — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/03.player_movement_code.html

**Contents:**
- Moving the player with code
- Testing our player's movement
  - Adding a camera
- User-contributed notes

It's time to code! We're going to use the input actions we created in the last part to move the character.

For this project, we will be following the Godot naming conventions.

GDScript: Classes (nodes) use PascalCase, variables and functions use snake_case, and constants use ALL_CAPS (See GDScript style guide).

C#: Classes, export variables and methods use PascalCase, private fields use _camelCase, local variables and parameters use camelCase (See C# style guide). Be careful to type the method names precisely when connecting signals.

Right-click the Player node and select Attach Script to add a new script to it. In the popup, set the Template to Empty before pressing the Create button. We set it to Empty because we want to write our own code for player movement.

Let's start with the class's properties. We're going to define a movement speed, a fall acceleration representing gravity, and a velocity we'll use to move the character.

These are common properties for a moving body. The target_velocity is a 3D vector combining a speed with a direction. Here, we define it as a property because we want to update and reuse its value across frames.

The values are quite different from 2D code because distances are in meters. While in 2D, a thousand units (pixels) may only correspond to half of your screen's width, in 3D, it's a kilometer.

Let's code the movement. We start by calculating the input direction vector using the global Input object, in _physics_process().

Here, instead of _process(), we're going to make all calculations using the _physics_process() virtual function. It's designed specifically for physics-related code like moving a kinematic or rigid body. It updates the node using fixed time intervals.

To learn more about the difference between _process() and _physics_process(), see Idle and Physics Processing.

We start by initializing a direction variable to Vector3.ZERO. Then, we check if the player is pressing one or more of the move_* inputs and update the vector's x and z components accordingly. These correspond to the ground plane's axes.

These four conditions give us eight possibilities and eight possible directions.

In case the player presses, say, both W and D simultaneously, the vector will have a length of about 1.4. But if they press a single key, it will have a length of 1. We want the vector's length to be consistent, and not move faster diagonally. To do so, we can call its normalized() method.

Here, we only normalize the vector if the direction has a length greater than zero, which means the player is pressing a direction key.

We compute the direction the $Pivot is looking by creating a Basis that looks in the direction direction.

Then, we update the velocity. We have to calculate the ground velocity and the fall speed separately. Be sure to go back one tab so the lines are inside the _physics_process() function but outside the condition we just wrote above.

The CharacterBody3D.is_on_floor() function returns true if the body collided with the floor in this frame. That's why we apply gravity to the Player only while it is in the air.

For the vertical velocity, we subtract the fall acceleration multiplied by the delta time every frame. This line of code will cause our character to fall in every frame, as long as it is not on or colliding with the floor.

The physics engine can only detect interactions with walls, the floor, or other bodies during a given frame if movement and collisions happen. We will use this property later to code the jump.

On the last line, we call CharacterBody3D.move_and_slide() which is a powerful method of the CharacterBody3D class that allows you to move a character smoothly. If it hits a wall midway through a motion, the engine will try to smooth it out for you. It uses the velocity value native to the CharacterBody3D

And that's all the code you need to move the character on the floor.

Here is the complete player.gd code for reference.

We're going to put our player in the Main scene to test it. To do so, we need to instantiate the player and then add a camera. Unlike in 2D, in 3D, you won't see anything if your viewport doesn't have a camera pointing at something.

Save your Player scene and open the Main scene. You can click on the Main tab at the top of the editor to do so.

If you closed the scene before, head to the FileSystem dock and double-click main.tscn to re-open it.

To instantiate the Player, right-click on the Main node and select Instantiate Child Scene.

In the popup, double-click player.tscn. The character should appear in the center of the viewport.

Let's add the camera next. Like we did with our Player's Pivot, we're going to create a basic rig. Right-click on the Main node again and select Add Child Node. Create a new Marker3D, and name it CameraPivot. Select CameraPivot and add a child node Camera3D to it. Your scene tree should look similar to this.

Notice the Preview checkbox that appears in the top-left of the 3D view when you have the Camera selected. You can click it to preview the in-game camera projection.

We're going to use the Pivot to rotate the camera as if it was on a crane. Let's first split the 3D view to be able to freely navigate the scene and see what the camera sees.

In the toolbar right above the viewport, click on View, then 2 Viewports. You can also press Ctrl + 2 (Cmd + 2 on macOS).

On the bottom view, select your Camera3D and turn on camera Preview by clicking the checkbox.

In the top view, make sure your Camera3D is selected and move the camera about 19 units on the Z axis (drag the blue arrow).

Here's where the magic happens. Select the CameraPivot and rotate it -45 degrees around the X axis (using the red circle). You'll see the camera move as if it was attached to a crane.

You can run the scene by pressing F6 and press the arrow keys to move the character.

We can see some empty space around the character due to the perspective projection. In this game, we're going to use an orthographic projection instead to better frame the gameplay area and make it easier for the player to read distances.

Select the Camera again and in the Inspector, set the Projection to Orthogonal and the Size to 19. The character should now look flatter and the ground should fill the background.

When using an orthogonal camera in Godot 4, directional shadow quality is dependent on the camera's Far value. The higher the Far value, the further away the camera will be able to see. However, higher Far values also decrease shadow quality as the shadow rendering has to cover a greater distance.

If directional shadows look too blurry after switching to an orthogonal camera, decrease the camera's Far property to a lower value such as 100. Don't decrease this Far property too much, or objects in the distance will start disappearing.

Test your scene and you should be able to move in all 8 directions and not glitch through the floor!

Ultimately, we have both player movement and the view in place. Next, we will work on the monsters.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends CharacterBody3D

# How fast the player moves in meters per second.
@export var speed = 14
# The downward acceleration when in the air, in meters per second squared.
@export var fall_acceleration = 75

var target_velocity = Vector3.ZERO
```

Example 2 (csharp):
```csharp
using Godot;

public partial class Player : CharacterBody3D
{
    // Don't forget to rebuild the project so the editor knows about the new export variable.

    // How fast the player moves in meters per second.
    [Export]
    public int Speed { get; set; } = 14;
    // The downward acceleration when in the air, in meters per second squared.
    [Export]
    public int FallAcceleration { get; set; } = 75;

    private Vector3 _targetVelocity = Vector3.Zero;
}
```

Example 3 (gdscript):
```gdscript
func _physics_process(delta):
    # We create a local variable to store the input direction.
    var direction = Vector3.ZERO

    # We check for each move input and update the direction accordingly.
    if Input.is_action_pressed("move_right"):
        direction.x += 1
    if Input.is_action_pressed("move_left"):
        direction.x -= 1
    if Input.is_action_pressed("move_back"):
        # Notice how we are working with the vector's x and z axes.
        # In 3D, the XZ plane is the ground plane.
        direction.z += 1
    if Input.is_action_pressed("move_forward"):
        direction.z -= 1
```

Example 4 (csharp):
```csharp
public override void _PhysicsProcess(double delta)
{
    // We create a local variable to store the input direction.
    var direction = Vector3.Zero;

    // We check for each move input and update the direction accordingly.
    if (Input.IsActionPressed("move_right"))
    {
        direction.X += 1.0f;
    }
    if (Input.IsActionPressed("move_left"))
    {
        direction.X -= 1.0f;
    }
    if (Input.IsActionPressed("move_back"))
    {
        // Notice how we are working with the vector's X and Z axes.
        // In 3D, the XZ plane is the ground plane.
        direction.Z += 1.0f;
    }
    if (Input.IsActionPressed("move_forward"))
    {
        direction.Z -= 1.0f;
    }
}
```

---

## Designing the mob scene — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/04.mob_scene.html

**Contents:**
- Designing the mob scene
- Removing monsters off-screen
  - Coding the mob's movement
  - Leaving the screen
- User-contributed notes

In this part, you're going to code the monsters, which we'll call mobs. In the next lesson, we'll spawn them randomly around the playable area.

Let's design the monsters themselves in a new scene. The node structure is going to be similar to the player.tscn scene.

Create a scene with, once again, a CharacterBody3D node as its root. Name it Mob. Add a child node Node3D, name it Pivot. And drag and drop the file mob.glb from the FileSystem dock onto the Pivot to add the monster's 3D model to the scene.

You can rename the newly created mob node into Character.

We need a collision shape for our body to work. Right-click on the Mob node, the scene's root, and click Add Child Node.

Add a CollisionShape3D.

In the Inspector, assign a BoxShape3D to the Shape property.

We should change its size to fit the 3D model better. You can do so interactively by clicking and dragging on the orange dots.

The box should touch the floor and be a little thinner than the model. Physics engines work in such a way that if the player's sphere touches even the box's corner, a collision will occur. If the box is a little too big compared to the 3D model, you may die at a distance from the monster, and the game will feel unfair to the players.

Notice that my box is taller than the monster. It is okay in this game because we're looking at the scene from above and using a fixed perspective. Collision shapes don't have to match the model exactly. It's the way the game feels when you test it that should dictate their form and size.

We're going to spawn monsters at regular time intervals in the game level. If we're not careful, their count could increase to infinity, and we don't want that. Each mob instance has both a memory and a processing cost, and we don't want to pay for it when the mob is outside the screen.

Once a monster leaves the screen, we don't need it anymore, so we should delete it. Godot has a node that detects when objects leave the screen, VisibleOnScreenNotifier3D, and we're going to use it to destroy our mobs.

When you keep instancing an object, there's a technique you can use to avoid the cost of creating and destroying instances all the time called pooling. It consists of pre-creating an array of objects and reusing them over and over.

When working with GDScript, you don't need to worry about this. The main reason to use pools is to avoid freezes with garbage-collected languages like C# or Lua. GDScript uses a different technique to manage memory, reference counting, which doesn't have that caveat. You can learn more about that here: Memory management.

Select the Mob node and add a child node VisibleOnScreenNotifier3D. Another box, pink this time, appears. When this box completely leaves the screen, the node will emit a signal.

Resize it using the orange dots until it covers the entire 3D model.

Let's implement the monster's motion. We're going to do this in two steps. First, we'll write a script on the Mob that defines a function to initialize the monster. We'll then code the randomized spawn mechanism in the main.tscn scene and call the function from there.

Attach a script to the Mob.

Here's the movement code to start with. We define two properties, min_speed and max_speed, to define a random speed range, which we will later use to define CharacterBody3D.velocity.

Similarly to the player, we move the mob every frame by calling the function CharacterBody3D.move_and_slide(). This time, we don't update the velocity every frame; we want the monster to move at a constant speed and leave the screen, even if it were to hit an obstacle.

We need to define another function to calculate the CharacterBody3D.velocity. This function will turn the monster towards the player and randomize both its angle of motion and its velocity.

The function will take a start_position,the mob's spawn position, and the player_position as its arguments.

We position the mob at start_position and turn it towards the player using the look_at_from_position() method, and randomize the angle by rotating a random amount around the Y axis. Below, randf_range() outputs a random value between -PI / 4 radians and PI / 4 radians.

We got a random position, now we need a random_speed. randi_range() will be useful as it gives random int values, and we will use min_speed and max_speed. random_speed is just an integer, and we just use it to multiply our CharacterBody3D.velocity. After random_speed is applied, we rotate CharacterBody3D.velocity Vector3 towards the player.

We still have to destroy the mobs when they leave the screen. To do so, we'll connect our VisibleOnScreenNotifier3D node's screen_exited signal to the Mob.

Head back to the 3D viewport by clicking on the 3D label at the top of the editor. You can also press Ctrl + F2 (Opt + 2 on macOS).

Select the VisibleOnScreenNotifier3D node and on the right side of the interface, navigate to the Node dock. Double-click the screen_exited() signal.

Connect the signal to the Mob

This will add a new function for you in your mob script, _on_visible_on_screen_notifier_3d_screen_exited(). From it, call the queue_free() method. This function destroys the instance it's called on.

Our monster is ready to enter the game! In the next part, you will spawn monsters in the game level.

Here is the complete mob.gd script for reference.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends CharacterBody3D

# Minimum speed of the mob in meters per second.
@export var min_speed = 10
# Maximum speed of the mob in meters per second.
@export var max_speed = 18


func _physics_process(_delta):
    move_and_slide()
```

Example 2 (json):
```json
using Godot;

public partial class Mob : CharacterBody3D
{
    // Don't forget to rebuild the project so the editor knows about the new export variable.

    // Minimum speed of the mob in meters per second
    [Export]
    public int MinSpeed { get; set; } = 10;
    // Maximum speed of the mob in meters per second
    [Export]
    public int MaxSpeed { get; set; } = 18;

    public override void _PhysicsProcess(double delta)
    {
        MoveAndSlide();
    }
}
```

Example 3 (csharp):
```csharp
# This function will be called from the Main scene.
func initialize(start_position, player_position):
    # We position the mob by placing it at start_position
    # and rotate it towards player_position, so it looks at the player.
    look_at_from_position(start_position, player_position, Vector3.UP)
    # Rotate this mob randomly within range of -45 and +45 degrees,
    # so that it doesn't move directly towards the player.
    rotate_y(randf_range(-PI / 4, PI / 4))
```

Example 4 (csharp):
```csharp
// This function will be called from the Main scene.
public void Initialize(Vector3 startPosition, Vector3 playerPosition)
{
    // We position the mob by placing it at startPosition
    // and rotate it towards playerPosition, so it looks at the player.
    LookAtFromPosition(startPosition, playerPosition, Vector3.Up);
    // Rotate this mob randomly within range of -45 and +45 degrees,
    // so that it doesn't move directly towards the player.
    RotateY((float)GD.RandRange(-Mathf.Pi / 4.0, Mathf.Pi / 4.0));
}
```

---

## Spawning monsters — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/05.spawning_mobs.html

**Contents:**
- Spawning monsters
- Creating the spawn path
  - Adding placeholder cylinders
- Spawning monsters randomly
- User-contributed notes

In this part, we're going to spawn monsters along a path randomly. By the end, you will have monsters roaming the game board.

Double-click on main.tscn in the FileSystem dock to open the Main scene.

Before drawing the path, we're going to change the game resolution. Our game has a default window size of 1152x648. We're going to set it to 720x540, a nice little box.

Go to Project -> Project Settings.

If you still have Input Map open, switch to the General tab.

In the left menu, navigate down to Display -> Window. On the right, set the Viewport Width to 720 and the Viewport Height to 540.

Like you did in the 2D game tutorial, you're going to design a path and use a PathFollow3D node to sample random locations on it.

In 3D though, it's a bit more complicated to draw the path. We want it to be around the game view so monsters appear right outside the screen. But if we draw a path, we won't see it from the camera preview.

To find the view's limits, we can use some placeholder meshes. Your viewport should still be split into two parts, with the camera preview at the bottom. If that isn't the case, press Ctrl + 2 (Cmd + 2 on macOS) to split the view into two. Select the Camera3D node and click the Preview checkbox in the bottom viewport.

Let's add the placeholder meshes. Add a new Node3D as a child of the Main node and name it Cylinders. We'll use it to group the cylinders. Select Cylinders and add a child node MeshInstance3D

In the Inspector, assign a CylinderMesh to the Mesh property.

Set the top viewport to the top orthogonal view using the menu in the viewport's top-left corner. Alternatively, you can press the keypad's 7 key.

The grid may be distracting. You can toggle it by going to the View menu in the toolbar and clicking View Grid.

You now want to move the cylinder along the ground plane, looking at the camera preview in the bottom viewport. I recommend using grid snap to do so. You can toggle it by clicking the magnet icon in the toolbar or pressing Y.

Move the cylinder so it's right outside the camera's view in the top-left corner.

We're going to create copies of the mesh and place them around the game area. Press Ctrl + D (Cmd + D on macOS) to duplicate the node. You can also right-click the node in the Scene dock and select Duplicate. Move the copy down along the blue Z axis until it's right outside the camera's preview.

Select both cylinders by pressing the Shift key and clicking on the unselected one and duplicate them.

Move them to the right by dragging the red X axis.

They're a bit hard to see in white, aren't they? Let's make them stand out by giving them a new material.

In 3D, materials define a surface's visual properties like its color, how it reflects light, and more. We can use them to change the color of a mesh.

We can update all four cylinders at once. Select all the mesh instances in the Scene dock. To do so, you can click on the first one and Shift click on the last one.

In the Inspector, expand the Material section and assign a StandardMaterial3D to slot 0.

Click the sphere icon to open the material resource. You get a preview of the material and a long list of sections filled with properties. You can use these to create all sorts of surfaces, from metal to rock or water.

Expand the Albedo section.

Set the color to something that contrasts with the background, like a bright orange.

We can now use the cylinders as guides. Fold them in the Scene dock by clicking the grey arrow next to them. Moving forward, you can also toggle their visibility by clicking the eye icon next to Cylinders.

Add a child node Path3D to Main node. In the toolbar, four icons appear. Click the Add Point tool, the icon with the green "+" sign.

You can hover any icon to see a tooltip describing the tool.

Click in the center of each cylinder to create a point. Then, click the Close Curve icon in the toolbar to close the path. If any point is a bit off, you can click and drag on it to reposition it.

Your path should look like this.

To sample random positions on it, we need a PathFollow3D node. Add a PathFollow3D as a child of the Path3D. Rename the two nodes to SpawnLocation and SpawnPath, respectively. It's more descriptive of what we'll use them for.

With that, we're ready to code the spawn mechanism.

Right-click on the Main node and attach a new script to it.

We first export a variable to the Inspector so that we can assign mob.tscn or any other monster to it.

We want to spawn mobs at regular time intervals. To do this, we need to go back to the scene and add a timer. Before that, though, we need to assign the mob.tscn file to the mob_scene property above (otherwise it's null!)

Head back to the 3D screen and select the Main node. Drag mob.tscn from the FileSystem dock to the Mob Scene slot in the Inspector.

Add a new Timer node as a child of Main. Name it MobTimer.

In the Inspector, set its Wait Time to 0.5 seconds and turn on Autostart so it automatically starts when we run the game.

Timers emit a timeout signal every time they reach the end of their Wait Time. By default, they restart automatically, emitting the signal in a cycle. We can connect to this signal from the Main node to spawn monsters every 0.5 seconds.

With the MobTimer still selected, head to the Node dock on the right, and double-click the timeout signal.

Connect it to the Main node.

This will take you back to the script, with a new empty _on_mob_timer_timeout() function.

Let's code the mob spawning logic. We're going to:

Instantiate the mob scene.

Sample a random position on the spawn path.

Get the player's position.

Call the mob's initialize() method, passing it the random position and the player's position.

Add the mob as a child of the Main node.

Above, randf() produces a random value between 0 and 1, which is what the PathFollow node's progress_ratio expects: 0 is the start of the path, 1 is the end of the path. The path we have set is around the camera's viewport, so any random value between 0 and 1 is a random position alongside the edges of the viewport!

Note that if you remove the Player from the main scene, the following line

gives an error because there is no $Player!

Here is the complete main.gd script so far, for reference.

You can test the scene by pressing F6. You should see the monsters spawn and move in a straight line.

For now, they bump and slide against one another when their paths cross. We'll address this in the next part.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
extends Node

@export var mob_scene: PackedScene
```

Example 2 (json):
```json
using Godot;

public partial class Main : Node
{
    // Don't forget to rebuild the project so the editor knows about the new export variable.

    [Export]
    public PackedScene MobScene { get; set; }
}
```

Example 3 (gdscript):
```gdscript
func _on_mob_timer_timeout():
    # Create a new instance of the Mob scene.
    var mob = mob_scene.instantiate()

    # Choose a random location on the SpawnPath.
    # We store the reference to the SpawnLocation node.
    var mob_spawn_location = get_node("SpawnPath/SpawnLocation")
    # And give it a random offset.
    mob_spawn_location.progress_ratio = randf()

    var player_position = $Player.position
    mob.initialize(mob_spawn_location.position, player_position)

    # Spawn the mob by adding it to the Main scene.
    add_child(mob)
```

Example 4 (csharp):
```csharp
// We also specified this function name in PascalCase in the editor's connection window.
private void OnMobTimerTimeout()
{
    // Create a new instance of the Mob scene.
    Mob mob = MobScene.Instantiate<Mob>();

    // Choose a random location on the SpawnPath.
    // We store the reference to the SpawnLocation node.
    var mobSpawnLocation = GetNode<PathFollow3D>("SpawnPath/SpawnLocation");
    // And give it a random offset.
    mobSpawnLocation.ProgressRatio = GD.Randf();

    Vector3 playerPosition = GetNode<Player>("Player").Position;
    mob.Initialize(mobSpawnLocation.Position, playerPosition);

    // Spawn the mob by adding it to the Main scene.
    AddChild(mob);
}
```

---

## Jumping and squashing monsters — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/06.jump_and_squash.html

**Contents:**
- Jumping and squashing monsters
- Controlling physics interactions
  - Setting layer names
  - Assigning layers and masks
- Jumping
- Squashing monsters
  - Coding the squash mechanic
- User-contributed notes

In this part, we'll add the ability to jump and squash the monsters. In the next lesson, we'll make the player die when a monster hits them on the ground.

First, we have to change a few settings related to physics interactions. Enter the world of physics layers.

Physics bodies have access to two complementary properties: layers and masks. Layers define on which physics layer(s) an object is.

Masks control the layers that a body will listen to and detect. This affects collision detection. When you want two bodies to interact, you need at least one to have a mask corresponding to the other.

If that's confusing, don't worry, we'll see three examples in a second.

The important point is that you can use layers and masks to filter physics interactions, control performance, and remove the need for extra conditions in your code.

By default, all physics bodies and areas are set to both layer and mask 1. This means they all collide with each other.

Physics layers are represented by numbers, but we can give them names to keep track of what's what.

Let's give our physics layers a name. Go to Project -> Project Settings.

In the left menu, navigate down to Layer Names -> 3D Physics. You can see a list of layers with a field next to each of them on the right. You can set their names there. Name the first three layers player, enemies, and world, respectively.

Now, we can assign them to our physics nodes.

In the Main scene, select the Ground node. In the Inspector, expand the Collision section. There, you can see the node's layers and masks as a grid of buttons.

The ground is part of the world, so we want it to be part of the third layer. Click the lit button to toggle off the first Layer and toggle on the third one. Then, toggle off the Mask by clicking on it.

As mentioned before, the Mask property allows a node to listen to interaction with other physics objects, but we don't need it to have collisions. Ground doesn't need to listen to anything; it's just there to prevent creatures from falling.

Note that you can click the "..." button on the right side of the properties to see a list of named checkboxes.

Next up are the Player and the Mob. Open player.tscn by double-clicking the file in the FileSystem dock.

Select the Player node and set its Collision -> Mask to both "enemies" and "world". You can leave the default Layer property as it is, because the first layer is the "player" layer.

Then, open the Mob scene by double-clicking on mob.tscn and select the Mob node.

Set its Collision -> Layer to "enemies" and unset its Collision -> Mask, leaving the mask empty.

These settings mean the monsters will move through one another. If you want the monsters to collide with and slide against each other, turn on the "enemies" mask.

The mobs don't need to mask the "world" layer because they only move on the XZ plane. We don't apply any gravity to them by design.

The jumping mechanic itself requires only two lines of code. Open the Player script. We need a value to control the jump's strength and update _physics_process() to code the jump.

After the line that defines fall_acceleration, at the top of the script, add the jump_impulse.

Inside _physics_process(), add the following code before the move_and_slide() codeblock.

That's all you need to jump!

The is_on_floor() method is a tool from the CharacterBody3D class. It returns true if the body collided with the floor in this frame. That's why we apply gravity to the Player: so we collide with the floor instead of floating over it like the monsters.

If the character is on the floor and the player presses "jump", we instantly give them a lot of vertical speed. In games, you really want controls to be responsive and giving instant speed boosts like these, while unrealistic, feels great.

Notice that the Y axis is positive upwards. That's unlike 2D, where the Y axis is positive downwards.

Let's add the squash mechanic next. We're going to make the character bounce over monsters and kill them at the same time.

We need to detect collisions with a monster and to differentiate them from collisions with the floor. To do so, we can use Godot's group tagging feature.

Open the scene mob.tscn again and select the Mob node. Go to the Node dock on the right to see a list of signals. The Node dock has two tabs: Signals, which you've already used, and Groups, which allows you to assign tags to nodes. Click on the + button to open the Create new Group dialog.

Enter "mob" in the Name field and click the Ok button.

The "mob" group is now shown under the Scene Groups section.

An icon appears in the Scene dock to indicate the node is part of at least one group.

We can now use the group from the code to distinguish collisions with monsters from collisions with the floor.

Head back to the Player script to code the squash and bounce.

At the top of the script, we need another property, bounce_impulse. When squashing an enemy, we don't necessarily want the character to go as high up as when jumping.

Then, after the Jumping codeblock we added above in _physics_process(), add the following loop. With move_and_slide(), Godot makes the body move sometimes multiple times in a row to smooth out the character's motion. So we have to loop over all collisions that may have happened.

In every iteration of the loop, we check if we landed on a mob. If so, we kill it and bounce.

With this code, if no collisions occurred on a given frame, the loop won't run.

That's a lot of new functions. Here's some more information about them.

The functions get_slide_collision_count() and get_slide_collision() both come from the CharacterBody3D class and are related to move_and_slide().

get_slide_collision() returns a KinematicCollision3D object that holds information about where and how the collision occurred. For example, we use its get_collider property to check if we collided with a "mob" by calling is_in_group() on it: collision.get_collider().is_in_group("mob").

The method is_in_group() is available on every Node.

To check that we are landing on the monster, we use the vector dot product: Vector3.UP.dot(collision.get_normal()) > 0.1. The collision normal is a 3D vector that is perpendicular to the plane where the collision occurred. The dot product allows us to compare it to the up direction.

With dot products, when the result is greater than 0, the two vectors are at an angle of fewer than 90 degrees. A value higher than 0.1 tells us that we are roughly above the monster.

After handling the squash and bounce logic, we terminate the loop early via the break statement to prevent further duplicate calls to mob.squash(), which may otherwise result in unintended bugs such as counting the score multiple times for one kill.

We are calling one undefined function, mob.squash(), so we have to add it to the Mob class.

Open the script mob.gd by double-clicking on it in the FileSystem dock. At the top of the script, we want to define a new signal named squashed. And at the bottom, you can add the squash function, where we emit the signal and destroy the mob.

When using C#, Godot will create the appropriate events automatically for all Signals ending with EventHandler, see C# Signals.

We will use the signal to add points to the score in the next lesson.

With that, you should be able to kill monsters by jumping on them. You can press F5 to try the game and set main.tscn as your project's main scene.

However, the player won't die yet. We'll work on that in the next part.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (swift):
```swift
#...
# Vertical impulse applied to the character upon jumping in meters per second.
@export var jump_impulse = 20
```

Example 2 (csharp):
```csharp
// Don't forget to rebuild the project so the editor knows about the new export variable.

// ...
// Vertical impulse applied to the character upon jumping in meters per second.
[Export]
public int JumpImpulse { get; set; } = 20;
```

Example 3 (go):
```go
func _physics_process(delta):
    #...

    # Jumping.
    if is_on_floor() and Input.is_action_just_pressed("jump"):
        target_velocity.y = jump_impulse

    #...
```

Example 4 (json):
```json
public override void _PhysicsProcess(double delta)
{
    // ...

    // Jumping.
    if (IsOnFloor() && Input.IsActionJustPressed("jump"))
    {
        _targetVelocity.Y = JumpImpulse;
    }

    // ...
}
```

---

## Killing the player — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/07.killing_player.html

**Contents:**
- Killing the player
- Hitbox with the Area node
- Ending the game
- Code checkpoint
- User-contributed notes

We can kill enemies by jumping on them, but the player still can't die. Let's fix this.

We want to detect being hit by an enemy differently from squashing them. We want the player to die when they're moving on the floor, but not if they're in the air. We could use vector math to distinguish the two kinds of collisions. Instead, though, we will use an Area3D node, which works well for hitboxes.

Head back to the player.tscn scene and add a new child node Area3D. Name it MobDetector Add a CollisionShape3D node as a child of it.

In the Inspector, assign a cylinder shape to it.

Here is a trick you can use to make the collisions only happen when the player is on the ground or close to it. You can reduce the cylinder's height and move it up to the top of the character. This way, when the player jumps, the shape will be too high up for the enemies to collide with it.

You also want the cylinder to be wider than the sphere. This way, the player gets hit before colliding and being pushed on top of the monster's collision box.

The wider the cylinder, the more easily the player will get killed.

Next, select the MobDetector node again, and in the Inspector, turn off its Monitorable property. This makes it so other physics nodes cannot detect the area. The complementary Monitoring property allows it to detect collisions. Then, remove the Collision -> Layer and set the mask to the "enemies" layer.

When areas detect a collision, they emit signals. We're going to connect one to the Player node. Select MobDetector and go to Inspector's Node tab, double-click the body_entered signal and connect it to the Player

The MobDetector will emit body_entered when a CharacterBody3D or a RigidBody3D node enters it. As it only masks the "enemies" physics layers, it will only detect the Mob nodes.

Code-wise, we're going to do two things: emit a signal we'll later use to end the game and destroy the player. We can wrap these operations in a die() function that helps us put a descriptive label on the code.

We can use the Player's hit signal to end the game. All we need to do is connect it to the Main node and stop the MobTimer in reaction.

Open main.tscn, select the Player node, and in the Node dock, connect its hit signal to the Main node.

Get the timer, and stop it, in the _on_player_hit() function.

If you try the game now, the monsters will stop spawning when you die, and the remaining ones will leave the screen.

Notice also that the game no longer crashes or displays an error when the player dies. Because we are stopping the MobTimer, it no longer triggers the _on_mob_timer_timeout() function.

Also note that the enemy colliding with the player and dying depends on the size and position of the Player and the Mob's collision shapes. You may need to move them and resize them to achieve a tight game feel.

You can pat yourself on the back: you prototyped a complete 3D game, even if it's still a bit rough.

From there, we'll add a score, the option to retry the game, and you'll see how you can make the game feel much more alive with minimalistic animations.

Here are the complete scripts for the Main, Mob, and Player nodes, for reference. You can use them to compare and check your code.

Starting with main.gd.

Finally, the longest script, player.gd:

See you in the next lesson to add the score and the retry option.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (go):
```go
# Emitted when the player was hit by a mob.
# Put this at the top of the script.
signal hit


# And this function at the bottom.
func die():
    hit.emit()
    queue_free()


func _on_mob_detector_body_entered(body):
    die()
```

Example 2 (json):
```json
// Don't forget to rebuild the project so the editor knows about the new signal.

// Emitted when the player was hit by a mob.
[Signal]
public delegate void HitEventHandler();

// ...

private void Die()
{
    EmitSignal(SignalName.Hit);
    QueueFree();
}

// We also specified this function name in PascalCase in the editor's connection window.
private void OnMobDetectorBodyEntered(Node3D body)
{
    Die();
}
```

Example 3 (go):
```go
func _on_player_hit():
    $MobTimer.stop()
```

Example 4 (json):
```json
// We also specified this function name in PascalCase in the editor's connection window.
private void OnPlayerHit()
{
    GetNode<Timer>("MobTimer").Stop();
}
```

---

## Score and replay — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/08.score_and_replay.html

**Contents:**
- Score and replay
- Creating a UI theme
- Keeping track of the score
- Retrying the game
  - Coding the retry option
- Adding music
- User-contributed notes

In this part, we'll add the score, music playback, and the ability to restart the game.

We have to keep track of the current score in a variable and display it on screen using a minimal interface. We will use a text label to do that.

In the main scene, add a new child node Control to Main and name it UserInterface. Ensure you are on the 2D screen, where you can edit your User Interface (UI).

Add a Label node and name it ScoreLabel

In the Inspector, set the Label's Text to a placeholder like "Score: 0".

Also, the text is white by default, like our game's background. We need to change its color to see it at runtime.

Scroll down to Theme Overrides, and expand Colors and enable Font Color in order to tint the text to black (which contrasts well with the white 3D scene)

Finally, click and drag on the text in the viewport to move it away from the top-left corner.

The UserInterface node allows us to group our UI in a branch of the scene tree and use a theme resource that will propagate to all its children. We'll use it to set our game's font.

Once again, select the UserInterface node. In the Inspector, create a new theme resource in Theme -> Theme.

Click on it to open the theme editor In the bottom panel. It gives you a preview of how all the built-in UI widgets will look with your theme resource.

By default, a theme only has a few properties: Default Base Scale, Default Font and Default Font Size.

You can add more properties to the theme resource to design complex user interfaces, but that is beyond the scope of this series. To learn more about creating and editing themes, see Introduction to GUI skinning.

The Default Font expects a font file like the ones you have on your computer. Two common font file formats are TrueType Font (TTF) and OpenType Font (OTF).

In the FileSystem dock, expand the fonts directory and click and drag the Montserrat-Medium.ttf file we included in the project onto the Default Font. The text will reappear in the theme preview.

The text is a bit small. Set the Default Font Size to 22 pixels to increase the text's size.

Let's work on the score next. Attach a new script to the ScoreLabel and define the score variable.

The score should increase by 1 every time we squash a monster. We can use their squashed signal to know when that happens. However, because we instantiate monsters from the code, we cannot connect the mob signal to the ScoreLabel via the editor.

Instead, we have to make the connection from the code every time we spawn a monster.

Open the script main.gd. If it's still open, you can click on its name in the script editor's left column.

Alternatively, you can double-click the main.gd file in the FileSystem dock.

At the bottom of the _on_mob_timer_timeout() function, add the following line:

This line means that when the mob emits the squashed signal, the ScoreLabel node will receive it and call the function _on_mob_squashed().

Head back to the score_label.gd script to define the _on_mob_squashed() callback function.

There, we increment the score and update the displayed text.

The second line uses the value of the score variable to replace the placeholder %s. When using this feature, Godot automatically converts values to string text, which is convenient when outputting text in labels or when using the print() function.

You can learn more about string formatting here: GDScript format strings. In C#, consider using string interpolation with "$".

You can now play the game and squash a few enemies to see the score increase.

In a complex game, you may want to completely separate your user interface from the game world. In that case, you would not keep track of the score on the label. Instead, you may want to store it in a separate, dedicated object. But when prototyping or when your project is simple, it is fine to keep your code simple. Programming is always a balancing act.

We'll now add the ability to play again after dying. When the player dies, we'll display a message on the screen and wait for input.

Head back to the main.tscn scene, select the UserInterface node, add a child node ColorRect, and name it Retry. This node fills a rectangle with a uniform color and will serve as an overlay to darken the screen.

To make it span over the whole viewport, you can use the Anchor Preset menu in the toolbar.

Open it and apply the Full Rect command.

Nothing happens. Well, almost nothing; only the four green pins move to the corners of the selection box.

This is because UI nodes (all the ones with a green icon) work with anchors and margins relative to their parent's bounding box. Here, the UserInterface node has a small size and the Retry one is limited by it.

Select the UserInterface and apply Anchor Preset -> Full Rect to it as well. The Retry node should now span the whole viewport.

Let's change its color so it darkens the game area. Select Retry and in the Inspector, set its Color to something both dark and transparent. To do so, in the color picker, drag the A slider to the left. It controls the color's Alpha channel, that is to say, its opacity/transparency.

Next, add a Label as a child of Retry and give it the Text "Press Enter to retry." To move it and anchor it in the center of the screen, apply Anchor Preset -> Center to it.

We can now head to the code to show and hide the Retry node when the player dies and plays again.

Open the script main.gd. First, we want to hide the overlay at the start of the game. Add this line to the _ready() function.

Then, when the player gets hit, we show the overlay.

Finally, when the Retry node is visible, we need to listen to the player's input and restart the game if they press enter. To do this, we use the built-in _unhandled_input() callback, which is triggered on any input.

If the player pressed the predefined ui_accept input action and Retry is visible, we reload the current scene.

The function get_tree() gives us access to the global SceneTree object, which allows us to reload and restart the current scene.

To add music that plays continuously in the background, we're going to use another feature in Godot: autoloads.

To play audio, all you need to do is add an AudioStreamPlayer node to your scene and attach an audio file to it. When you start the scene, it can play automatically. However, when you reload the scene, like we do to play again, the audio nodes are also reset, and the music starts back from the beginning.

You can use the autoload feature to have Godot load a node or a scene automatically at the start of the game, outside the current scene. You can also use it to create globally accessible objects.

Create a new scene by going to the Scene menu and clicking New Scene or by using the + icon next to your currently opened scene.

Click the Other Node button to create an AudioStreamPlayer and rename it to MusicPlayer.

We included a music soundtrack in the art/ directory, House In a Forest Loop.ogg. Click and drag it onto the Stream property in the Inspector. Also, turn on Autoplay so the music plays automatically at the start of the game.

Save the scene as music_player.tscn.

We have to register it as an autoload. Head to the Project -> Project Settings… menu and click on the Globals -> Autoload tab.

In the Path field, you want to enter the path to your scene. Click the folder icon to open the file browser and double-click on music_player.tscn. Then, click the Add button on the right to register the node.

music_player.tscn now loads into any scene you open or play. So if you run the game now, the music will play automatically in any scene.

Before we wrap up this lesson, here's a quick look at how it works under the hood. When you run the game, your Scene dock changes to give you two tabs: Remote and Local.

The Remote tab allows you to visualize the node tree of your running game. There, you will see the Main node and everything the scene contains and the instantiated mobs at the bottom.

At the top are the autoloaded MusicPlayer and a root node, which is your game's viewport.

And that does it for this lesson. In the next part, we'll add an animation to make the game both look and feel much nicer.

Here is the complete main.gd script for reference.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Label

var score = 0
```

Example 2 (swift):
```swift
using Godot;

public partial class ScoreLabel : Label
{
    private int _score = 0;
}
```

Example 3 (go):
```go
func _on_mob_timer_timeout():
    #...
    # We connect the mob to the score label to update the score upon squashing one.
    mob.squashed.connect($UserInterface/ScoreLabel._on_mob_squashed.bind())
```

Example 4 (sql):
```sql
private void OnMobTimerTimeout()
{
    // ...
    // We connect the mob to the score label to update the score upon squashing one.
    mob.Squashed += GetNode<ScoreLabel>("UserInterface/ScoreLabel").OnMobSquashed;
}
```

---

## Character animation — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/09.adding_animations.html

**Contents:**
- Character animation
- Using the animation editor
- The float animation
  - Controlling the animation in code
- Animating the mobs
- User-contributed notes

In this final lesson, we'll use Godot's built-in animation tools to make our characters float and flap. You'll learn to design animations in the editor and use code to make your game feel alive.

We'll start with an introduction to using the animation editor.

The engine comes with tools to author animations in the editor. You can then use the code to play and control them at runtime.

Open the player scene, select the Player node, and add an AnimationPlayer node.

The Animation dock appears in the bottom panel.

It features a toolbar and the animation drop-down menu at the top, a track editor in the middle that's currently empty, and filter, snap, and zoom options at the bottom.

Let's create an animation. Click on Animation -> New.

Name the animation "float".

Once you've created the animation, the timeline appears with numbers representing time in seconds.

We want the animation to start playback automatically at the start of the game. Also, it should loop.

To do so, you can click the autoplay button () in the animation toolbar and the looping arrows, respectively.

You can also pin the animation editor by clicking the pin icon in the top-right. This prevents it from folding when you click on the viewport and deselect the nodes.

Set the animation duration to 1.2 seconds in the top-right of the dock.

You should see the gray ribbon widen a bit. It shows you the start and end of your animation and the vertical blue line is your time cursor.

You can click and drag the slider in the bottom-right to zoom in and out of the timeline.

With the animation player node, you can animate most properties on as many nodes as you need. Notice the key icon next to properties in the Inspector. You can click any of them to create a keyframe, a time and value pair for the corresponding property. The keyframe gets inserted where your time cursor is in the timeline.

Let's insert our first keys. Here, we will animate both the position and the rotation of the Character node.

Select the Character and in the Inspector expand the Transform section. Click the key icon next to Position, and Rotation.

For this tutorial, just create RESET Track(s) which is the default choice

Two tracks appear in the editor with a diamond icon representing each keyframe.

You can click and drag on the diamonds to move them in time. Move the position key to 0.3 seconds and the rotation key to 0.1 seconds.

Move the time cursor to 0.5 seconds by clicking and dragging on the gray timeline, or by entering it into the input field.

In the Inspector, set the Position's Y axis to 0.65 meters and the Rotation' X axis to 8.

If you don't see the properties in the Inspector panel, first click on the Character node again in the Scene dock.

Create a keyframe for both properties

Now, move the position keyframe to 0.7 seconds by dragging it on the timeline.

A lecture on the principles of animation is beyond the scope of this tutorial. Just note that you don't want to time and space everything evenly. Instead, animators play with timing and spacing, two core animation principles. You want to offset and contrast in your character's motion to make them feel alive.

Move the time cursor to the end of the animation, at 1.2 seconds. Set the Y position to about 0.35 and the X rotation to -9 degrees. Once again, create a key for both properties.

You can preview the result by clicking the play button or pressing Shift + D. Click the stop button or press S to stop playback.

You can see that the engine interpolates between your keyframes to produce a continuous animation. At the moment, though, the motion feels very robotic. This is because the default interpolation is linear, causing constant transitions, unlike how living things move in the real world.

We can control the transition between keyframes using easing curves.

Click and drag around the first two keys in the timeline to box select them.

You can edit the properties of both keys simultaneously in the Inspector, where you can see an Easing property.

Click and drag on the curve, pulling it towards the left. This will make it ease-out, that is to say, transition fast initially and slow down as the time cursor reaches the next keyframe.

Play the animation again to see the difference. The first half should already feel a bit bouncier.

Apply an ease-out to the second keyframe in the rotation track.

Do the opposite for the second position keyframe, dragging it to the right.

Your animation should look something like this.

Animations update the properties of the animated nodes every frame, overriding initial values. If we directly animated the Player node, it would prevent us from moving it in code. This is where the Pivot node comes in handy: even though we animated the Character, we can still move and rotate the Pivot and layer changes on top of the animation in a script.

If you play the game, the player's creature will now float!

If the creature is a little too close to the floor, you can move the Pivot up to offset it.

We can use code to control the animation playback based on the player's input. Let's change the animation speed when the character is moving.

Open the Player's script by clicking the script icon next to it.

In _physics_process(), after the line where we check the direction vector, add the following code.

This code makes it so when the player moves, we multiply the playback speed by 4. When they stop, we reset it to normal.

We mentioned that the Pivot could layer transforms on top of the animation. We can make the character arc when jumping using the following line of code. Add it at the end of _physics_process().

Here's another nice trick with animations in Godot: as long as you use a similar node structure, you can copy them to different scenes.

For example, both the Mob and the Player scenes have a Pivot and a Character node, so we can reuse animations between them.

Open the Player scene, select the AnimationPlayer node and then click on Animation > Manage Animations.... Click the Copy animation to clipboard button (two small squares) alongside the float animation. Click OK to close the window.

Then open mob.tscn, create an AnimationPlayer child node and select it. Click Animation > Manage Animations, then New Library. You should see the message "Global library will be created." Leave the text field blank and click OK. Click the Paste icon (clipboard) and it should appear in the window. Click OK to close the window.

Next, make sure that the autoplay button () and the looping arrows (Animation looping) are also turned on in the animation editor in the bottom panel. That's it; all monsters will now play the float animation.

We can change the playback speed based on the creature's random_speed. Open the Mob's script and at the end of the initialize() function, add the following line.

And with that, you finished coding your first complete 3D game.

In the next part, we'll quickly recap what you learned and give you some links to keep learning more. But for now, here are the complete player.gd and mob.gd so you can check your code against them.

Here's the Player script.

And the Mob's script.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (csharp):
```csharp
func _physics_process(delta):
    #...
    if direction != Vector3.ZERO:
        #...
        $AnimationPlayer.speed_scale = 4
    else:
        $AnimationPlayer.speed_scale = 1
```

Example 2 (csharp):
```csharp
public override void _PhysicsProcess(double delta)
{
    // ...
    if (direction != Vector3.Zero)
    {
        // ...
        GetNode<AnimationPlayer>("AnimationPlayer").SpeedScale = 4;
    }
    else
    {
        GetNode<AnimationPlayer>("AnimationPlayer").SpeedScale = 1;
    }
}
```

Example 3 (go):
```go
func _physics_process(delta):
    #...
    $Pivot.rotation.x = PI / 6 * velocity.y / jump_impulse
```

Example 4 (csharp):
```csharp
public override void _PhysicsProcess(double delta)
{
    // ...
    var pivot = GetNode<Node3D>("Pivot");
    pivot.Rotation = new Vector3(Mathf.Pi / 6.0f * Velocity.Y / JumpImpulse, pivot.Rotation.Y, pivot.Rotation.Z);
}
```

---

## Going further — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/first_3d_game/going_further.html

**Contents:**
- Going further
- Exploring the manual
- User-contributed notes

You can pat yourself on the back for having completed your first 3D game with Godot.

In this series, we went over a wide range of techniques and editor features. Hopefully, you've witnessed how intuitive Godot's scene system can be and learned a few tricks you can apply in your projects.

But we just scratched the surface: Godot has a lot more in store for you to save time creating games. And you can learn all that by browsing the documentation.

Where should you begin? Below, you'll find a few pages to start exploring and build upon what you've learned so far.

But before that, here's a link to download a completed version of the project: https://github.com/godotengine/godot-demo-projects/releases.

The manual is your ally whenever you have a doubt or you're curious about a feature. It does not contain tutorials about specific game genres or mechanics. Instead, it explains how Godot works in general. In it, you will find information about 2D, 3D, physics, rendering and performance, and much more.

Here are the sections we recommend you to explore next:

Read the Scripting section to learn essential programming features you'll use in every project.

The 3D and Physics sections will teach you more about 3D game creation in the engine.

Inputs is another important one for any game project.

You can start with these or, if you prefer, look at the sidebar menu on the left and pick your options.

We hope you enjoyed this tutorial series, and we're looking forward to seeing what you achieve using Godot.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Introduction — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/best_practices/introduction_best_practices.html

**Contents:**
- Introduction
- User-contributed notes

This series is a collection of best practices to help you work efficiently with Godot.

Godot allows for a great amount of flexibility in how you structure a project's codebase and break it down into scenes. Each approach has its pros and cons, and they can be hard to weigh until you've worked with the engine for long enough.

There are always many ways to structure your code and solve specific programming problems. It would be impossible to cover them all here.

That is why each article starts from a real-world problem. We will break down each problem in fundamental questions, suggest solutions, analyze the pros and cons of each option, and highlight the best course of action for the problem at hand.

You should start by reading Applying object-oriented principles in Godot. It explains how Godot's nodes and scenes relate to classes and objects in other Object-Oriented programming languages. It will help you make sense of the rest of the series.

The best practices in Godot rely on Object-Oriented design principles. We use tools like the single responsibility principle and encapsulation.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Editor introduction — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/editor/index.html

**Contents:**
- Editor introduction
- Editor's interface
- XR editor
- Android editor
- Web editor
- Advanced features
- Managing editor features

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

In this section, we cover the Godot editor in general, from its interface to using it with the command line.

The following pages explain how to use the various windows, workspaces, and docks that make up the Godot editor. We cover some specific editors' interfaces in other sections where appropriate. For example, the animation editor.

Godot offers a port of the editor designed to run natively on Meta Quest devices. The port can be downloaded from the Meta Horizon Store, or from the Godot download page.

Godot offers a native port of the editor running entirely on Android devices. The Android port can be downloaded from the Android Downloads page. While we strive for feature parity with the Desktop version of the editor, the Android port has a certain amount of caveats you should be aware of.

Godot offers an HTML5 version of the editor running entirely in your browser. No download is required to use it, but it has a certain amount of caveats you should be aware of.

The articles below focus on advanced features useful for experienced developers, such as calling Godot from the command line and using an external text editor like Visual Studio Code or Emacs.

Godot allows you to remove features from the editor. This may be useful if you're an educator trying to ease students into the editor slowly, or if you're working on a project that's only 2D or only 3D and don't want to see what you don't need.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---
