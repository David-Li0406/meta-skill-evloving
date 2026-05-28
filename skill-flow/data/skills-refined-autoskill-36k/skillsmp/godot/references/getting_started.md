# Godot - Getting Started

**Pages:** 50

---

## Introduction — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/getting_started/introduction/index.html

**Contents:**
- Introduction

This series will introduce you to Godot and give you an overview of its features.

In the following pages, you will get answers to questions such as "Is Godot for me?" or "What can I do with Godot?". We will then introduce the engine's most essential concepts, run you through the editor's interface, and give you tips to make the most of your time learning it.

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

## Introduction to 2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/2d/introduction_to_2d.html

**Contents:**
- Introduction to 2D
- 2D workspace
  - Main toolbar
  - Coordinate system
  - 2D Viewport
- Node2D and Control node
- 3D in 2D
- User-contributed notes

Godot's 2D game development tools include a dedicated 2D rendering engine, physics system, and features tailored specifically for creating 2D experiences. You can efficiently design levels with the TileMap system, animate characters with 2D sprite or Cutout animation, and leverage 2D lighting for dynamic scene illumination. The built-in 2D particle system allows you to create complex visual effects, and Godot also supports custom shaders to enhance your graphics. These features, combined with Godot's accessibility and flexibility, provide a solid foundation for creating engaging 2D games.

2D Platformer Demo available on the Asset Library.

This page will show you the 2D workspace and how you can get to know it.

If you would like to get an introduction to 3D, see Introduction to 3D.

You will use the 2D workspace to work with 2D scenes, design levels, or create user interfaces. To switch to the 2D workspace, you can either select a 2D node from the scene tree, or use the workspace selector located at the top edge of the editor:

Similar to 3D, you can use the tabs below the workspace selector to change between currently opened scenes or create a new one using the plus (+) button. The left and right docks should be familiar from editor introduction.

Below the scene selector is the main toolbar, and beneath the main toolbar is the 2D viewport.

You can drag and drop compatible nodes from the FileSystem dock to add them to the viewport as nodes. Dragging and dropping adds the dragged node as a sibling of the selected node (if the root node is selected, adds as a child). Keeping Shift pressed when dropping adds the node as a child of the selected node. Holding Alt when dropping adds the node as a child of the root node. If Alt + Shift is held when dropping, the node type can be selected if applicable.

Some buttons in the main toolbar are the same as those in the 3D workspace. A brief explanation is given with the shortcut if the mouse cursor is hovered over a button for one second. Some buttons may have additional functionality if another keypress is performed. A recap of main functionality of each button with its default shortcut is provided below from left to right:

Select Mode (Q): Allows selection of nodes in the viewport. Left clicking on a node in the viewport selects it. Left clicking and dragging a rectangle selects all nodes within the rectangle's boundaries, once released. Holding Shift while selecting adds more nodes to the selection. Clicking on a selected node while holding Shift deselects the node. In this mode, you can drag the selected node(s) to move, press Ctrl to switch to the rotation mode temporarily, or use the red circles to scale it. If multiple nodes are selected, only movement and rotation are possible. In this mode, rotation and scaling will not use the snapping options if snapping is enabled.

Move Mode (W): Enables move (or translate) mode for the selected nodes. See 2D Viewport for more details.

Rotate Mode (E): Enables rotation mode for the selected nodes. See 2D Viewport for more details.

Scale Mode (S): Enables scaling and displays scaling gizmos in both axes for the selected node(s). See 2D Viewport for more details.

Show list of selectable nodes at position clicked: As the description suggests, this provides a list of selectable nodes at the clicked position as a context menu, if there is more than one node in the clicked area.

Rotation pivot: Sets the rotation pivot to rotate node(s) around. An added node has its rotation pivot at x: 0, y: 0, by default, with exceptions. For example, the default pivot for a Sprite2D is its center if the centered property is set to true. If you would like to change the rotation pivot of a node, click this button and choose a new location by left clicking. The node rotates considering this point. If you have multiple nodes selected, this icon will add a temporary pivot to be used commonly by all selected nodes. Pressing Shift and clicking this button will create the pivot at the center of selected nodes. If any of the snap options are enabled, the pivot will also snap to them when dragged.

Pan Mode (G): Allows you to navigate in the viewport without accidentally selecting any nodes. In other modes, you can also hold Space and drag with the left mouse button to do the same.

Ruler Mode: After enabling, click on the viewport to display the current global x and y coordinates. Dragging from a position to another one measures the distance in pixels. If you drag diagonally, it will draw a triangle and show the separate distances in terms of x, y, and total distance to the target, including the angles to the axes in degrees. The R key activates the ruler. If snapping is enabled, it also displays the measurements in terms of grid count:

Using ruler with snapping enabled.

Use Smart Snap: Toggles smart snapping for move, rotate, and scale modes; and the rotation pivot. Customize it using the three-dot menu next to the snap tools.

Use Grid Snap: Toggles snapping to grid for move and scale mode, rotation pivot, and the ruler. Customize it using the three-dot menu next to the snap tools.

You can customize the grid settings so that move mode, rotate mode, scale mode, ruler, and rotation pivot uses snapping. Use the three-dot menu for this:

Use Rotation Snap: Toggles snapping using the configured rotation setting.

Use Scale Snap: Toggles snapping using the configured scaling step setting.

Snap Relative: Toggles the usage of snapping based on the selected node's current transform values. For example, if the grids are set to 32x32 pixels and if the selected node is located at x: 1, y: 1, then, enabling this option will temporarily shift the grids by x: 1, y: 1.

Use Pixel Snap: Toggles the use of subpixels for snapping. If enabled, the position values will be integers, disabling will enable subpixel movement as decimal values. For the runtime property, consider checking Project Settings > Rendering > 2D > Snapping property for Node2D nodes, and Project Settings > GUI > General > Snap Controls to Pixels for Control nodes.

Smart Snapping: Provides a set of options to snap to specific positions if they are enabled:

Snap to Parent: Snaps to parent's edges. For example, scaling a child control node while this is enabled will snap to the boundaries of the parent.

Snap to Node Anchor: Snaps to the node's anchor. For example, if anchors of a control node is positioned at different positions, enabling this will snap to the sides and corners of the anchor.

Snap to Node Sides: Snaps to the node's sides, such as for the rotation pivot or anchor positioning.

Snap to Node Center: Snaps to the node's center, such as for the rotation pivot or anchor positioning.

Snap to Other Nodes: Snaps to other nodes while moving or scaling. Useful to align nodes in the editor.

Snap to Guides: Snaps to custom guides drawn using the horizontal or vertical ruler. More on the ruler and guides below.

Configure Snap: Opens the window shown above, offering a set of snapping parameters.

Grid Offset: Allows you to shift grids with respect to the origin. x and y can be adjusted separately.

Grid Step: The distance between each grid in pixels. x and y can be adjusted separately.

Primary Line Every: The number of grids in-between to draw infinite lines as indication of main lines.

Rotation Offset: Sets the offset to shift rotational snapping.

Rotation Step: Defines the snapping degree. E.g., 15 means the node will rotate and snap at multiples of 15 degrees if rotation snap is enabled and the rotate mode is used.

Scale Step: Determines the scaling increment factor. For example, if it is 0.1, it will change the scaling at 0.1 steps if scaling snap is enabled and the scaling mode is used.

Lock selected nodes (Ctrl + L). Locks the selected nodes, preventing selection and movement in the viewport. Clicking the button again (or using Ctrl + Shift + L) unlocks the selected nodes. Locked nodes can only be selected in the scene tree. They can easily be identified by a padlock next to their node names in the scene tree. Clicking on this padlock also unlocks the nodes.

Group selected nodes (Ctrl + G). This allows selection of the root node if any of the children are selected. Using Ctrl + G ungroups them. Additionally, clicking the ungroup button in the scene tree performs the same action.

Skeleton Options: Provides options to work with Skeleton2D and Bone2D.

Show Bones: Toggles the visibility of bones for the selected node.

Make Bone2D Node(s) from Node(s): Converts selected node(s) into Bone2D.

To learn more about Skeletons, see Cutout animation.

View menu: Provides options to control the viewport view. Since its options depend heavily on the viewport, it is covered in the 2D Viewport section.

Next to the View menu, additional buttons may be visible. In the toolbar image at the beginning of this chapter, an additional Sprite2D button appears because a Sprite2D is selected. This menu provides some quick actions and tools to work on a specific node or selection. For example, while drawing a polygon, it provides buttons to add, modify, or remove points.

In the 2D editor, unlike 3D, there are only two axes: x and y. Also, the viewing angle is fixed.

In the viewport, you will see two lines in two colors going across the screen infinitely: red for the x-axis, and green for the y-axis. In Godot, going right and down are positive directions. Where these two lines intersect is the origin: x: 0, y: 0.

A root node will have its origin at this position once added. Switching to the move or scale modes after selecting a node will display the gizmos at the node's offset position. The gizmos will point to the positive directions of the x and y axes. In the move mode, you can drag the green line to move only in the y axis. Similarly, you can hold the red line to move only in the x axis.

In the scale mode, the gizmos will have a square shape. You can hold and drag the green and red squares to scale the nodes in the y or x axes. Dragging in a negative direction flips the node horizontally or vertically.

The viewport will be the area you spend the most time if you plan to design levels or user interfaces visually:

Middle-clicking and dragging the mouse will pan the view. The scrollbars on the right or bottom of the viewport also move the view. Alternatively, the G or Space keys can be used. If you enable Editor Settings > Editors > Panning > Simple Panning, you can activate panning directly with Space only, without requiring dragging.

The viewport has buttons on the top-left. Center View centers the selected node(s) in the screen. Useful if you have a large scene with many nodes, and want to see the node selected in the scene tree. Next to it are the zoom controls. - zooms out, + zooms in, and clicking on the number with percentage defaults to 100%. Alternatively, you can use middle-mouse scrolling to zoom in (scroll up) and out (scroll down).

The black bars at the viewport's left and top edges are the rulers. You can use them to orient yourself in the viewport. By default, the rulers will display the pixel coordinates of the viewport, numbered at 100 pixel steps. Changing the zoom factor will change the shown values. Enabling Grid Snap or changing the snapping options will update the ruler's scaling and the shown values.

You can also create multiple custom guides to help you make measurements or align nodes with them:

If you have at least one node in the scene, you can create guides by dragging from the horizontal or vertical ruler towards the viewport. A purple guide will appear, showing its position, and will remain there when you release the mouse. You can create both horizontal and vertical guides simultaneously by dragging from the gray square at the rulers' intersection. Guides can be repositioned by dragging them back to their respective rulers, and they can be removed by dragging them all the way back to the ruler.

You can also enable snapping to the created guides using the Smart Snap menu.

If you cannot create a line, or do not see previously created guides, make sure that they are visible by checking the View menu of the viewport. Y toggles their visibility, by default. Also, make sure you have at least one node in the scene.

Depending on the tool chosen in the toolbar, left-clicking will have a primary action in the viewport. For example, the Select Mode will select the left-clicked node in the viewport. Sometimes, left-clicking can be combined with a modifier (e.g., Ctrl, or Shift) to perform secondary actions. For example, keeping Shift pressed while dragging a node in the Select or Move modes will try to snap the node in a single axis while moving.

Right clicking in the viewport provides two options to create a node or instantiate a scene at the chosen position. If at least one node is selected, right clicking also provides the option to move the selected node(s) to this position.

Viewport has a View menu which provides several options to change the look of the viewport:

Grid: Allows you to show grids all the time, only when using snapping, or not at all. You can also toggle them with the provided option.

Show Helpers: Toggles the temporary display of an outline of the node, with the previous transform properties (position, scaling, or rotation) if a transform operation has been initiated. For Control nodes, it also shows the sizing parameters. Useful to see the deltas.

Show Rulers: Toggles the visibility of horizontal and vertical rulers. See 2D Viewport more on rulers.

Show Guides: Toggles the visibility of created guides. See 2D Viewport for on how to create them.

Show Origin: Toggles the display of the green and red origin lines drawn at x: 0, y: 0.

Show Viewport: Toggles the visibility of the game's default viewport, indicated by an indigo-colored rectangle. It is also the default window size on desktop platforms, which can be changed by going to Project Settings > Display > Window > Size and setting Viewport Width and Viewport Height.

Gizmos: Toggles the visibility of Position (shown with cross icon), Lock (shown with padlock), Groups (shown with two squares), and Transformation (shown with green and red lines) indicators.

Center Selection: The same as the Center View button inside the viewport. Centers the selected node(s) in the view. F is the default shortcut.

Frame to Selection: Similar to Center Selection, but also changes the zoom factor to fit the contents in the screen. Shift + F is the default shortcut.

Clear Guides: Deletes all guides from the screen. You will need to recreate them if you plan to use them later.

Preview Canvas Scale: Toggles the preview for scaling of canvas in the editor when the zoom factor or view of the viewport changes. Useful to see how the controls will look like after scaling and moving, without running the game.

Preview Theme: Allows to choose from the available themes to change the look of control items in the editor, without requiring to run the game.

CanvasItem is the base node for 2D. Node2D is the base node for 2D game objects, and Control is the base node for everything GUI. For 3D, Godot uses the Node3D node.

It is possible to display 3D scenes in 2D screen, You can see this in the demo 3D in 2D Viewport.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Introduction to 3D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html

**Contents:**
- Introduction to 3D
- 3D workspace
  - Main toolbar
  - View menu of viewport
  - Coordinate system
  - Space and manipulation gizmos
  - Navigating the 3D environment
  - Using Blender-style transform shortcuts
- Node3D node
- 3D content

Creating a 3D game can be challenging. That extra Z coordinate makes many of the common techniques that helped to make 2D games simpler no longer work. To aid in this transition, it is worth mentioning that Godot uses similar APIs for 2D and 3D. Most nodes are the same and are present in both 2D and 3D versions. In fact, it is worth checking the 3D platformer tutorial, or the 3D kinematic character tutorials, which are almost identical to their 2D counterparts.

Godot Third Person Shooter (TPS) Demo, available on the Github repository or the Asset Library.

In 3D, math is a little more complex than in 2D. For an introduction to the relevant math written for game developers, not mathemeticians or engineers, check out Vector math and Using 3D transforms.

Editing 3D scenes is done in the 3D workspace. This workspace can be selected manually, but it will be automatically selected when a Node3D node is selected.

Similar to 2D, the tabs below the workspace selector are used to change between currently opened scenes or create a new one using the plus (+) button. The left and right docks should be familiar from editor introduction.

Below the scene selector, the main toolbar is visible, and beneath the main toolbar is the 3D viewport.

Some buttons in the main toolbar are the same as those in the 2D workspace. A brief explanation is given with the shortcut if the mouse cursor is hovered over a button for one second. Some buttons may have additional functionality if another keypress is performed. A recap of main functionality of each button with its default shortcut is provided below from left to right:

Select Mode (Q): Allows selection of nodes in the viewport. Left clicking on a node to select one. Left clicking and dragging a rectangle selects all nodes within the rectangle's boundaries, once released. Holding Shift while selecting adds more nodes to the selection. Clicking on a selected node while holding Shift deselects the node. In this mode, you can use the gizmos to perform movement or rotation.

Move Mode (W): Enables move (or translate) mode for the selected nodes. See Space and manipulation gizmos for more details.

Rotate Mode (E): Enables rotation mode for the selected nodes. See Space and manipulation gizmos for more details.

Scale Mode (R): Enables scaling and displays scaling gizmos in different axes for the selected nodes. See Space and manipulation gizmos for more details.

Show the list of selectable nodes at the clicked position: As the description suggests, this provides a list of selectable nodes at the clicked position as a context menu, if there is more than one node in the clicked area.

Lock (Ctrl + L) the selected nodes, preventing selection and movement in the viewport. Clicking the button again (or using Ctrl + Shift + L) unlocks the selected nodes. Locked nodes can only be selected in the scene tree. They can easily be identified with a padlock next to their node names in the scene tree. Clicking on this padlock also unlocks the nodes.

Group selected nodes (Ctrl + G). This allows selection of the root node if any of the children are selected. Using Ctrl + G ungroups them. Additionally, clicking the ungroup button in the scene tree performs the same action.

Ruler Mode (M): When enabled you can click and drag to measure distance in the scene in meters.

Use Local Space (T): If enabled, gizmos of a node are drawn using the current node's rotation angle instead of the global viewport axes.

Use Snap (Y): If enabled, movement, and rotation snap to grid. Snapping can also temporarily be activated using Ctrl while performing the action. The settings for changing snap options are explained below.

Toggle preview sunlight: If no DirectionalLight3D exist in the scene, a preview of sunlight can be used as a light source. See Preview environment and light for more details.

Toggle preview environment: If no WorldEnvironment exists in the scene, a preview of the environment can be used as a placeholder. See Preview environment and light for more details.

Edit Sun and Environment Settings (three dots): Opens the menu to configure preview sunlight and environment settings. See Preview environment and light for more details.

Transform menu: It has three options:

Snap Object to Floor: Snaps an object to a solid floor.

Transform Dialog: Opens a dialog to adjust transform parameters (translate, rotate, scale, and transform) manually.

Snap Settings: Allows you to change transform, rotate snap (in degrees), and scale snap (in percent) settings.

View menu: Controls the view options and enables additional viewports:

In this menu, you can also show/hide grids, which are set to 1x1 meter by default, and the origin, where the blue, green, and red axis lines intersect. Moreover, specific types of gizmos can be toggled in this menu.

An open eye means that the gizmo is visible, a closed eye means it is hidden. A half-open eye means that it is also visible through opaque surfaces.

Clicking on Settings in this view menu opens a window to change the Vertical Field of View (VFOV) parameter (in degrees), Z-Near, and Z-Far values.

Next to the View menu, additional buttons may be visible. In the toolbar image at the beginning of this chapter, an additional Mesh button appears because a MeshInstance3D is selected. This menu provides some quick actions or tools to work on a specific node or selection.

Below the Select tool, in the 3D viewport, clicking on the three dots opens the View menu for the viewport. Hiding all shown gizmos in the editor's 3D view can also be performed through this menu:

This menu also displays the current view type and enables quick adjustment of the viewport's viewing angle. Additionally, it offers options to modify the appearance of nodes within the viewport.

Godot uses the metric system for everything in 3D, with 1 unit being equal to 1 meter. Physics and other areas are tuned for this scale. Therefore, attempting to use a different scale is usually a bad idea (unless you know what you are doing).

When working with 3D assets, it's always best to work in the correct scale (set the unit to metric in your 3D modeling software). Godot allows scaling post-import and, while this works in most cases, in rare situations it may introduce floating-point precision issues (and thus, glitches or artifacts) in delicate areas such as rendering or physics. Make sure your artists always work in the right scale!

The Y coordinate is used for "up". As for the horizontal X/Z axes, Godot uses a right-handed coordinate system. This means that for most objects that need alignment (such as lights or cameras), the Z axis is used as a "pointing towards" direction. This convention roughly means that:

See this chart for comparison with other 3D software:

Image by Freya Holmér

Moving, rotating, and scaling objects in the 3D view is done through the manipulator gizmos. Each axis is represented by a color: Red, Green, Blue represent X, Y, Z respectively. This convention applies to the grid and other gizmos too (and also to the shader language, ordering of components for Vector3, Color, etc.).

Some useful keybindings:

To snap placement or rotation, press Ctrl while moving, scaling, or rotating.

To center the view on the selected object, press F.

In the viewport, the arrows can be clicked and held to move the object on an axis. The arcs can be clicked and held to rotate the object. To lock one axis and move the object freely in the other two axes, the colored rectangles can be clicked, held, and dragged.

If the transform mode is changed from Select Mode to Scale Mode, the arrows will be replaced by cubes, which can be dragged to scale an object as if the object is being moved.

In 3D environments, it is often important to adjust the viewpoint or angle from which you are viewing the scene. In Godot, navigating the 3D environment in the viewport (or spatial editor) can be done in multiple ways.

The default 3D scene navigation controls are similar to Blender (aiming to have some sort of consistency in the free software pipeline), but options are included to customize mouse buttons and behavior to be similar to other tools in the Editor Settings. To change the controls to Maya or Modo controls, you can navigate to Editor Settings > Editors > 3D. Then, under Navigation, search for Navigation Scheme.

Using the default settings, the following shortcuts control how one can navigate in the viewport:

Pressing the middle mouse button and dragging the mouse allows you to orbit around the center of what is on the screen.

It is also possible to left-click and hold the manipulator gizmo located on the top right of the viewport to orbit around the center:

Left-clicking on one of the colored circles will set the view to the chosen orthogonal and the viewport's view menu will be updated accordingly.

If the Perspective view is enabled on the viewport (can be seen on the viewport's View menu, not the View menu on the main toolbar), holding down the right mouse button on the viewport or pressing Shift + F switches to "free-look" mode. In this mode you can move the mouse to look around, use the W A S D keys to fly around the view, E to go up, and Q to go down. To disable this mode, release the right mouse button or press Shift + F again.

In the free-look mode, you can temporarily increase the flying speed using Shift or decrease it using Alt. To change and keep the speed modifier use mouse wheel up or mouse wheel down, to increase or decrease it, respectively.

In orthogonal mode, holding the right mouse button will pan the view instead. Use Keypad 5 to toggle between perspective and orthogonal view.

Since Godot 4.2, you can enable Blender-style shortcuts for translating, rotating and scaling nodes. In Blender, these shortcuts are:

After pressing a shortcut key while focusing on the 3D editor viewport, move the mouse or enter a number to move the selected node(s) by the specified amount in 3D units. You can constrain movement to a specific axis by specifying the axis as a letter, then the distance (if entering a value with the keyboard).

For instance, to move the selection upwards by 2.5 units, enter the following sequence in order (Y+ is upwards in Godot):

To use Blender-style transform shortcuts in Godot, go to the Editor Settings' Shortcuts tab, then in the Spatial Editor section:

Bind Begin Translate Transformation to G.

Bind Begin Rotate Transformation to R.

Bind Begin Scale Transformation to S.

Finally, unbind Scale Mode so that its shortcut won't conflict with Begin Rotate Transformation.

More shortcuts can be found on the 3D / Spatial editor page.

Node2D is the base node for 2D. Control is the base node for everything GUI. Following this reasoning, the 3D engine uses the Node3D node for everything 3D.

Node3Ds have a local transform, which is relative to the parent node (as long as the parent node is also of or inherits from the type Node3D). This transform can be accessed as a 3×4 Transform3D, or as 3 Vector3 members representing location, Euler rotation (X, Y and Z angles) and scale.

Unlike 2D, where loading image content and drawing is straightforward, 3D is a little more difficult. The content needs to be created with special 3D tools (also called Digital Content Creation tools, or DCCs) and exported to an exchange file format to be imported in Godot. This is required since 3D formats are not as standardized as images.

It is possible to import 3D models in Godot created in external tools. Depending on the format, you can import entire scenes (exactly as they look in the 3D modeling software), including animation, skeletal rigs, blend shapes, or as simple resources.

See Importing 3D scenes for more on importing.

It is possible to create custom geometry by using the ArrayMesh resource directly. Simply create your arrays and use the ArrayMesh.add_surface_from_arrays() function. A helper class is also available, SurfaceTool, which provides a more straightforward API and helpers for indexing, generating normals, tangents, etc.

In any case, this method is meant for generating static geometry (models that will not be updated often), as creating vertex arrays and submitting them to the 3D API has a significant performance cost.

To learn about prototyping inside Godot or using external tools, see Prototyping levels with CSG.

If, instead, you need to generate simple geometry that will be updated often, Godot provides a special ImmediateMesh resource that can be used in a MeshInstance3D node. This provides an OpenGL 1.x-style immediate-mode API to create points, lines, triangles, etc.

While Godot packs a powerful 2D engine, many types of games use 2D in a 3D environment. By using a fixed camera (either orthogonal or perspective) that does not rotate, nodes such as Sprite3D and AnimatedSprite3D can be used to create 2D games that take advantage of mixing with 3D backgrounds, more realistic parallax, lighting/shadow effects, etc.

The disadvantage is, of course, that added complexity and reduced performance in comparison to plain 2D, as well as the lack of reference of working in pixels.

Besides editing a scene, it is often common to edit the environment. Godot provides a WorldEnvironment node that allows changing the background color, mode (as in, put a skybox), and applying several types of built-in post-processing effects. Environments can also be overridden in the Camera.

By default, any 3D scene that doesn't have a WorldEnvironment node, or a DirectionalLight3D, will have a preview turned on for what it's missing to light the scene.

The preview light and environment will only be visible in the scene while in the editor. If you run the scene or export the project they will not affect the scene.

The preview light and environment can be turned on or off from the top menu by clicking on their respective icon.

The three dots dropdown menu next to those icons can be used to adjust the properties of the preview environment and light if they are enabled.

The same preview sun and environment is used for every scene in the same project, So only make adjustments that would apply to all of the scenes you will need a preview light and environment for.

No matter how many objects are placed in the 3D space, nothing will be displayed unless a Camera3D is also added to the scene. Cameras can work in either orthogonal or perspective projections:

Cameras are associated with (and only display to) a parent or grandparent viewport. Since the root of the scene tree is a viewport, cameras will display on it by default, but if sub-viewports (either as render target or picture-in-picture) are desired, they need their own children cameras to display.

When dealing with multiple cameras, the following rules are enforced for each viewport:

If no cameras are present in the scene tree, the first one that enters it will become the active camera. Further cameras entering the scene will be ignored (unless they are set as current).

If a camera has the "current" property set, it will be used regardless of any other camera in the scene. If the property is set, it will become active, replacing the previous camera.

If an active camera leaves the scene tree, the first camera in tree-order will take its place.

The background environment emits some ambient light which appears on surfaces. Still, without any light sources placed in the scene, the scene will appear quite dark unless the background environment is very bright.

Most outdoor scenes have a directional light (the sun or moon), while indoor scenes typically have several positional lights (lamps, torches, …). See 3D lights and shadows for more information on setting up lights in Godot.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Introduction to global illumination — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/introduction_to_global_illumination.html

**Contents:**
- Introduction to global illumination
- What is global illumination?
  - Indirect diffuse lighting
  - Specular lighting
- Which global illumination technique should I use?
  - Performance
  - Visuals
  - Real-time ability
  - User work needed
  - Summary

Global illumination is a catch-all term used to describe a system of lighting that uses both direct light (light that comes directly from a light source) and indirect light (light that bounces from a surface). In a 3D rendering engine, global illumination is one of the most important elements to achieving realistic lighting. Global illumination aims to mimic how light behaves in real life, such as light bouncing on surfaces and light being emitted from emissive materials.

In the example below, the entire scene is illuminated by an emissive material (the white square at the top). The white wall and ceiling on the back is tinted red and green close to the walls, as the light bouncing on the colored walls is being reflected back onto the rest of the scene.

Global illumination is composed of several key concepts:

This is the lighting that does not change depending on the camera's angle. There are two main sources of indirect diffuse lighting:

Light bouncing on surfaces. This bounced lighting is multiplied with the material's albedo color. The bounced lighting can then be reflected by other surfaces, with decreasing impact due to light attenuation. In real life, light bounces an infinite number of times. However, for performance reasons, this can't be simulated in a game engine. Instead, the number of bounces is typically limited to 1 or 2 (or up to 16 when baking lightmaps). A greater number of bounces will lead to more realistic light falloff in shaded areas, at the cost of lower performance or greater bake times.

Emissive materials can also emit light that can be bounced on surfaces. This acts as a form of area lighting. Instead of having an infinitely small point emit light using an OmniLight3D or SpotLight3D node, an area of a determined size will emit light using its own surface.

Direct diffuse lighting is already handled by the light nodes themselves, which means that global illumination algorithms only try to represent indirect lighting.

Different global illumination techniques offer varying levels of accuracy to represent indirect diffuse lighting. See the comparison table at the bottom of this page for more information.

To provide more accurate ambient occlusion for small objects, screen-space ambient occlusion (SSAO) can be enabled in the environment settings. SSAO has a significant performance cost, so make sure to disable it when targeting low-end hardware.

Indirect diffuse lighting may be a source of color banding in scenes with no detailed textures. This results in light gradients not being smooth, but having a visible "stepping" effect instead. See the Color banding section in the 3D rendering limitations documentation for ways to reduce this effect.

Specular lighting is also referred to as reflections. This is the lighting that changes in intensity depending on the camera's angle. This specular lighting can be direct or indirect.

Most global illumination techniques offer a way to render specular lighting. However, the degree of accuracy at which specular lighting is rendered varies greatly from technique to technique. See the comparison table at the bottom of this page for more information.

To provide more accurate reflections for small objects, screen-space reflections (SSR) can be enabled in the environment settings. SSR has a significant performance cost (even more so than SSAO), so make sure to disable it when targeting low-end hardware.

When determining a global illumination (GI) technique to use, there are several criteria to keep in mind:

Performance. Real-time GI techniques are usually more expensive compared to semi-real-time or baked techniques. Note that most of the cost in GI rendering is spent on the GPU, rather than the CPU.

Visuals. On top of not performing the best, real-time GI techniques generally don't provide the best visual output. This is especially the case in a mostly static scene where the dynamic nature of real-time GI is not easily noticeable. If maximizing visual quality is your goal, baked techniques will often look better and will result in fewer light leaks.

Real-time ability. Some GI techniques are fully real-time, whereas others are only semi-real-time or aren't real-time at all. Semi-real-time techniques have restrictions that fully real-time techniques don't. For instance, dynamic objects may not contribute emissive lighting to the scene. Non-real-time techniques do not support any form of dynamic GI, so it must be faked using other techniques if needed (such as placing positional lights near emissive surfaces). Real-time ability also affects the GI technique's viability in procedurally generated levels.

User work needed. Some GI techniques are fully automatic, whereas others require careful planning and manual work on the user's side. Depending on your time budget, some GI techniques may be preferable to others.

Here's a comparison of all the global illumination techniques available in Godot:

In order of performance from fastest to slowest:

ReflectionProbes with their update mode set to Always are much more expensive than probes with their update mode set to Once (the default). Suited for integrated graphics when using the Once update mode. Available in all renderers.

Lights can be baked with indirect lighting only, or fully baked on a per-light basis to further improve performance. Hybrid setups can be used (such as having a real-time directional light and fully baked positional lights). Directional information can be enabled before baking to improve visuals at a small performance cost (and at the cost of larger file sizes). Suited for integrated graphics. Available in all renderers. However, baking lightmaps requires hardware with RenderingDevice support.

The bake's number of subdivisions can be adjusted to balance between performance and quality. The VoxelGI rendering quality can be adjusted in the Project Settings. The rendering can optionally be performed at half resolution (and then linearly scaled) to improve performance significantly. Not available when using the Mobile or Compatibility renderers.

Screen-space indirect lighting (SSIL):

The SSIL quality and number of blur passes can be adjusted in the Project Settings. By default, SSIL rendering is performed at half resolution (and then linearly scaled) to ensure a reasonable performance level. Not available when using the Mobile or Compatibility renderers.

The number of cascades can be adjusted to balance performance and quality. The number of rays thrown per frame can be adjusted in the Project Settings. The rendering can optionally be performed at half resolution (and then linearly scaled) to improve performance significantly. Not available when using the Mobile or Compatibility renderers.

For comparison, here's a 3D scene with no global illumination options used:

A 3D scene without any form of global illumination (only constant environment lighting). The box and sphere near the camera are both dynamic objects.

Here's how Godot's various global illumination techniques compare:

VoxelGI: Good reflections and indirect lighting, but beware of leaks.

Due to its voxel-based nature, VoxelGI will exhibit light leaks if walls and floors are too thin. It's recommended to make sure all solid surfaces are at least as thick as one voxel.

Streaking artifacts may also be visible on sloped surfaces. In this case, tweaking the bias properties or rotating the VoxelGI node can help combat this.

SDFGI: Good reflections and indirect lighting, but beware of leaks and visible cascade shifts.

GI level of detail varies depending on the distance between the camera and surface.

Leaks can be reduced significantly by enabling the Use Occlusion property. This has a small performance cost, but it often results in fewer leaks compared to VoxelGI.

Cascade shifts may be visible when the camera moves fast. This can be made less noticeable by adjusting the cascade sizes or using fog.

Screen-space indirect lighting (SSIL): Good secondary source of indirect lighting, but no reflections.

SSIL is designed to be used as a complement to another GI technique such as VoxelGI, SDFGI or LightmapGI. SSIL works best for small-scale details, as it cannot provide accurate indirect lighting for large structures on its own. SSIL can provide real-time indirect lighting in situations where other GI techniques fail to capture small-scale details or dynamic objects. Its screen-space nature will result in some artifacts, especially when objects enter and leave the screen. SSIL works using the last frame's color (before post-processing) which means that emissive decals and custom shaders are included (as long as they're present on screen).

SSIL in action (without any other GI technique). Notice the emissive lighting around the yellow box.

LightmapGI: Excellent indirect lighting, decent reflections (optional).

This is the only technique where the number of light bounces can be pushed above 2 (up to 16). When directional information is enabled, spherical harmonics (SH) are used to provide blurry reflections.

LightmapGI in action. Only indirect lighting is baked here, but direct light can also be baked.

ReflectionProbe: Good reflections, but poor indirect lighting.

Indirect lighting can be disabled, set to a constant color spread throughout the probe, or automatically read from the probe's environment (and applied as a cubemap). This essentially acts as local ambient lighting. Reflections and indirect lighting are blended with other nearby probes.

ReflectionProbe in action (without any other GI technique). Notice the reflective sphere.

VoxelGI: Fully real-time.

Indirect lighting and reflections are fully real-time. Dynamic objects can receive GI and contribute to it with their emissive surfaces. Custom shaders can also emit their own light, which will be emitted accurately.

Viable for procedurally generated levels if they are generated in advance (and not during gameplay). Baking requires several seconds or more to complete, but it can be done from both the editor and an exported project.

SDFGI: Semi-real-time.

Cascades are generated in real-time, making SDFGI viable for procedurally generated levels (including when structures are generated during gameplay).

Dynamic objects can receive GI, but not contribute to it. Emissive lighting will only update when an object enters a cascade, so it may still work for slow-moving objects.

Screen-space indirect lighting (SSIL): Fully real-time.

SSIL works with both static and dynamic lights. It also works with both static and dynamic occluders (including emissive materials).

LightmapGI: Baked, and therefore not real-time.

Both indirect lighting and SH reflections are baked and can't be changed at runtime. Real-time GI must be simulated via other means, such as real-time positional lights. Dynamic objects receive indirect lighting via light probes, which can be placed automatically or manually by the user (LightmapProbe node). Not viable for procedurally generated levels, as baking lightmaps is only possible from the editor.

ReflectionProbe: Optionally real-time.

By default, reflections update when the probe is moved. They update as often as possible if the update mode is set to Always (which is expensive).

Indirect lighting must be configured manually by the user, but can be changed at runtime without causing an expensive computation to happen behind the scenes. This makes ReflectionProbes viable for procedurally generated levels.

VoxelGI: One or more VoxelGI nodes need to be created and baked.

Adjusting extents correctly is required to get good results. Additionally rotating the node and baking again can help combat leaks or streaking artifacts in certain situations. Bake times are fast – usually below 10 seconds for a scene of medium complexity.

SDFGI is fully automatic; it only needs to be enabled in the Environment resource. The only manual work required is to set MeshInstances' bake mode property correctly. No node needs to be created, and no baking is required.

Screen-space indirect lighting (SSIL): Very little.

SSIL is fully automatic; it only needs to be enabled in the Environment resource. No node needs to be created, and no baking is required.

LightmapGI: Requires UV2 setup and baking.

Static meshes must be reimported with UV2 and lightmap generation enabled. On a dedicated GPU, bake times are relatively fast thanks to the GPU-based lightmap baking – usually below 1 minute for a scene of medium complexity.

ReflectionProbe: Placed manually by the user.

If you are unsure about which GI technique to use:

For desktop games, it's a good idea to start with SDFGI first as it requires the least amount of setup. Move to other GI techniques later if needed. To improve performance on low-end GPUs and integrated graphics, consider adding an option to disable SDFGI or VoxelGI in your game's settings. SDFGI can be disabled in the Environment resource, and VoxelGI can be disabled by hiding the VoxelGI node(s). To further improve visuals on high-end setups, add an option to enable SSIL in your game's settings.

For mobile games, LightmapGI and ReflectionProbes are the only supported options. See also Alternatives to GI techniques.

You can compare global illumination techniques in action using the Global Illumination demo project.

Regardless of which global illumination technique you use, there is no universally "better" global illumination mode. Still, here are some recommendations for meshes:

For static level geometry, use the Static global illumination mode (default).

For small dynamic geometry and players/enemies, use the Disabled global illumination mode. Small dynamic geometry will not be able to contribute a significant amount of indirect lighting, due to the geometry being smaller than a voxel. If you need indirect lighting for small dynamic objects, it can be simulated using an OmniLight3D or SpotLight3D node parented to the object.

For large dynamic level geometry (such as a moving train), use the Dynamic global illumination mode. Note that this only has an effect with VoxelGI, as SDFGI and LightmapGI do not support global illumination with dynamic objects.

Here are some recommendations for light bake modes:

For static level lighting, use the Static bake mode. The Static mode is also suitable for dynamic lights that don't change much during gameplay, such as a flickering torch.

For short-lived dynamic effects (such as a weapon), use the Disabled bake mode to improve performance.

For long-lived dynamic effects (such as a rotating alarm light), use the Dynamic bake mode to improve quality (default). Note that this only has an effect with VoxelGI and SDFGI, as LightmapGI does not support global illumination with dynamic lights.

If none of the GI techniques mentioned above fits, it's still possible to simulate GI by placing additional lights manually. This requires more manual work, but it can offer good performance and good visuals if done right. This approach is still used in many modern games to this day.

When targeting low-end hardware in situations where using LightmapGI is not viable (such as procedurally generated levels), relying on environment lighting alone or a constant ambient light factor may be a necessity. This may result in flatter visuals, but adjusting the ambient light color and sky contribution still makes it possible to achieve acceptable results in most cases.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Introduction to the animation features — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/animation/introduction.html

**Contents:**
- Introduction to the animation features
- Create an AnimationPlayer node
- Computer animation relies on keyframes
- Tutorial: Creating a simple animation
  - Scene setup
  - Adding an animation
  - Managing animation libraries
  - Adding a track
  - The second keyframe
  - Run the animation

The AnimationPlayer node allows you to create anything from simple to complex animations.

In this guide you learn to:

Work with the Animation Panel

Animate any property of any node

Create a simple animation

In Godot, you can animate anything available in the Inspector, such as Node transforms, sprites, UI elements, particles, visibility and color of materials, and so on. You can also modify values of script variables and even call functions.

To use the animation tools we first have to create an AnimationPlayer node.

The AnimationPlayer node type is the data container for your animations. One AnimationPlayer node can hold multiple animations, which can automatically transition to one another.

The AnimationPlayer node

After you create an AnimationPlayer node, click on it to open the Animation Panel at the bottom of the viewport.

The animation panel position

The animation panel consists of four parts:

Animation controls (i.e. add, load, save, and delete animations)

The timeline with keyframes

The timeline and track controls, where you can zoom the timeline and edit tracks, for example.

A keyframe defines the value of a property at a point in time.

Diamond shapes represent keyframes in the timeline. A line between two keyframes indicates that the value doesn't change between them.

You set values of a node's properties and create animation keyframes for them. When the animation runs, the engine will interpolate the values between the keyframes, resulting in them gradually changing over time.

Two keyframes are all it takes to obtain a smooth motion

The timeline defines how long the animation will take. You can insert keyframes at various points, and change their timing.

The timeline in the animation panel

Each line in the Animation Panel is an animation track that references a Normal or Transform property of a node. Each track stores a path to a node and its affected property. For example, the position track in the illustration refers to the position property of the Sprite2D node.

Example of Normal animation tracks

If you animate the wrong property, you can edit a track's path at any time by double-clicking on it and typing the new path. Play the animation using the "Play from beginning" button (or pressing Shift + D on keyboard) to see the changes instantly.

For this tutorial, we'll create a Sprite node with an AnimationPlayer as its child. We will animate the sprite to move between two points on the screen.

AnimationPlayer inherits from Node instead of Node2D or Node3D, which means that the child nodes will not inherit the transform from the parent nodes due to a bare Node being present in the hierarchy.

Therefore, it is not recommended to add nodes that have a 2D/3D transform as a child of an AnimationPlayer node.

The sprite holds an image texture. For this tutorial, select the Sprite2D node, click Texture in the Inspector, and then click Load. Select the default Godot icon for the sprite's texture.

Select the AnimationPlayer node and click the "Animation" button in the animation editor. From the list, select "New" () to add a new animation. Enter a name for the animation in the dialog box.

For reusability, the animation is registered in a list in the animation library resource. If you add an animation to AnimationPlayer without specifying any particular settings, the animation will be registered in the [Global] animation library that AnimationPlayer has by default.

If there are multiple animation libraries and you try to add an animation, a dialog box will appear with options.

Add a new animation with library option

To add a new track for our sprite, select it and take a look at the toolbar:

These switches and buttons allow you to add keyframes for the selected node's location, rotation, and scale. Since we are only animating the sprite's position, make sure that only the location switch is selected. The selected switches are blue.

Click on the key button to create the first keyframe. Since we don't have a track set up for the Position property yet, Godot will offer to create it for us. Click Create.

Godot will create a new track and insert our first keyframe at the beginning of the timeline:

We need to set our sprite's end location and how long it will take for it to get there.

Let's say we want it to take two seconds to move between the points. By default, the animation is set to last only one second, so change the animation length to 2 in the controls on the right side of the animation panel's timeline header.

Now, move the sprite right, to its final position. You can use the Move tool in the toolbar or set the Position's X value in the Inspector.

Click on the timeline header near the two-second mark in the animation panel and then click the key button in the toolbar to create the second keyframe.

Click on the "Play from beginning" () button.

Yay! Our animation runs:

You can make it so an animation plays automatically when the AnimationPlayer nodes scene starts, or joins another scene. To do this click the "Autoplay on load" button in the animation editor, it's right next to the edit button.

The icon for it will also appear in front of the name of the animation, so you can easily identify which one is the autoplay animation.

Godot has an interesting feature that we can use in animations. When Animation Looping is set but there's no keyframe specified at the end of the animation, the first keyframe is also the last.

This means we can extend the animation length to four seconds now, and Godot will also calculate the frames from the last keyframe to the first, moving our sprite back and forth.

You can change this behavior by changing the track's loop mode. This is covered in the next chapter.

Each property track has a settings panel at the end, where you can set its update mode, track interpolation, and loop mode.

The update mode of a track tells Godot when to update the property values. This can be:

Continuous: Update the property on each frame

Discrete: Only update the property on keyframes

Capture: if the first keyframe's time is greater than 0.0, the current value of the property will be remembered and will be blended with the first animation key. For example, you could use the Capture mode to move a node that's located anywhere to a specific location.

You will usually use "Continuous" mode. The other types are used to script complex animations.

Track interpolation tells Godot how to calculate the frame values between keyframes. These interpolation modes are supported:

Nearest: Set the nearest keyframe value

Linear: Set the value based on a linear function calculation between the two keyframes

Cubic: Set the value based on a cubic function calculation between the two keyframes

Linear Angle (Only appears in rotation property): Linear mode with shortest path rotation

Cubic Angle (Only appears in rotation property): Cubic mode with shortest path rotation

With Cubic interpolation, animation is slower at keyframes and faster between them, which leads to more natural movement. Cubic interpolation is commonly used for character animation. Linear interpolation animates changes at a fixed pace, resulting in a more robotic effect.

Godot supports two loop modes, which affect the animation when it's set to loop:

Clamp loop interpolation: When this is selected, the animation stops after the last keyframe for this track. When the first keyframe is reached again, the animation will reset to its values.

Wrap loop interpolation: When this is selected, Godot calculates the animation after the last keyframe to reach the values of the first keyframe again.

Godot's animation system isn't restricted to position, rotation, and scale. You can animate any property.

If you select your sprite while the animation panel is visible, Godot will display a small keyframe button in the Inspector for each of the sprite's properties. Click on one of these buttons to add a track and keyframe to the current animation.

Keyframes for other properties

You can click on a keyframe in the animation timeline to display and edit its value in the Inspector.

Keyframe editor editing a key

You can also edit the easing value for a keyframe here by clicking and dragging its easing curve. This tells Godot how to interpolate the animated property when it reaches this keyframe.

You can tweak your animations this way until the movement "looks right."

You can set up a special RESET animation to contain the "default pose". This is used to ensure that the default pose is restored when you save the scene and open it again in the editor.

For existing tracks, you can add an animation called "RESET" (case-sensitive), then add tracks for each property that you want to reset. The only keyframe should be at time 0, and give it the desired default value for each track.

If AnimationPlayer's Reset On Save property is set to true, the scene will be saved with the effects of the reset animation applied (as if it had been seeked to time 0.0). This only affects the saved file – the property tracks in the editor stay where they were.

If you want to reset the tracks in the editor, select the AnimationPlayer node, open the Animation bottom panel then choose Apply Reset in the animation editor's Edit dropdown menu.

When using the keyframe icon next to a property in the inspector the editor will ask you to automatically create a RESET track.

RESET tracks are also used as reference values for blending. See also For better blending.

Godot's animation editor allows you use onion skinning while creating an animation. To turn this feature on click on the onion icon in the top right of the animation editor. Now there will be transparent red copies of what is being animated in its previous positions in the animation.

The three dots button next to the onion skinning button opens a dropdown menu that lets you adjust how it works, including the ability to use onion skinning for future frames.

Animation markers can be used to play a specific part of an animation rather than the whole thing. Here is a use case example, there's an animation file that has a character doing two distinct actions, and the project requires the whole animation, as well as both actions individually. Instead of making two additional animations, markers can be placed on the timeline, and both actions can now be played individually.

To add a marker to an animation right click the space above the timeline and select Insert Marker....

All markers require a unique name within the animation. You can also set the color of the markers for improved organization.

To play the part of the animation between two markers use the play_section_with_markers() and play_section_with_markers_backwards() methods. If no start marker is specified then the beginning of the animation is used, and if no end marker is specified, then the end of the animation is used.

If the end marker is after the end of the animation then the AnimationPlayer will clamp the end of the section so it does not go past the end of the animation.

To preview the animation between two markers use Shift + Click to select the markers. When two are selected the space between them should be highlighted in red.

Now all of the play animation buttons will act as if the selected area is the whole animation. Play Animation from Start will treat the first marker as the start of the animation, Play Animation Backwards from End will treat the second marker as the end, and so on.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## 2D navigation overview — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_introduction_2d.html

**Contents:**
- 2D navigation overview
- Setup for 2D scene
- User-contributed notes

Godot provides multiple objects, classes and servers to facilitate grid-based or mesh-based navigation and pathfinding for 2D and 3D games. The following section provides a quick overview over all available navigation related objects in Godot for 2D scenes and their primary use.

Godot provides the following objects and classes for 2D navigation:

Astar2D objects provide an option to find the shortest path in a graph of weighted points.

The AStar2D class is best suited for cell-based 2D gameplay that does not require actors to reach any possible position within an area but only predefined, distinct positions.

AstarGrid2D is a variant of AStar2D that is specialized for partial 2D grids.

AstarGrid2D is simpler to use when applicable because it doesn't require you to manually create points and connect them together.

NavigationServer2D provides a powerful server API to find the shortest path between two positions on an area defined by a navigation mesh.

The NavigationServer is best suited for 2D realtime gameplay that does require actors to reach any possible position within a navigation mesh defined area. Mesh-based navigation scales well with large game worlds as a large area can often be defined with a single polygon when it would require many, many grid cells.

The NavigationServer holds different navigation maps that each consist of regions that hold navigation mesh data. Agents can be placed on a map for avoidance calculation. RIDs are used to reference internal maps, regions, and agents when communicating with the server.

Reference to a specific navigation map that holds regions and agents. The map will attempt to join the navigation meshes of the regions by proximity. The map will synchronize regions and agents each physics frame.

Reference to a specific navigation region that can hold navigation mesh data. The region can be enabled / disabled or the use restricted with a navigation layer bitmask.

Reference to a specific navigation link that connects two navigation mesh positions over arbitrary distances.

Reference to a specific avoidance agent. The avoidance is specified by a radius value.

Reference to a specific avoidance obstacle used to affect and constrain the avoidance velocity of agents.

The following scene tree nodes are available as helpers to work with the NavigationServer2D API.

A Node that holds a NavigationPolygon resource that defines a navigation mesh for the NavigationServer2D.

The region can be enabled / disabled.

The use in pathfinding can be further restricted through the navigation_layers bitmask.

The NavigationServer2D will join the navigation meshes of regions by proximity for a combined navigation mesh.

A Node that connects two positions on navigation meshes over arbitrary distances for pathfinding.

The link can be enabled / disabled.

The link can be made one-way or bidirectional.

The use in pathfinding can be further restricted through the navigation_layers bitmask.

Links tell the pathfinding that a connection exists and at what cost. The actual agent handling and movement needs to happen in custom scripts.

A helper Node used to facilitate common NavigationServer2D API calls for pathfinding and avoidance. Use this Node with a Node2D inheriting parent Node.

A Node that can be used to affect and constrain the avoidance velocity of avoidance enabled agents. This Node does NOT affect the pathfinding of agents. You need to change the navigation meshes for that instead.

The 2D navigation meshes are defined with the following resources:

A resource that holds 2D navigation mesh data. It provides polygon drawing tools to allow defining navigation areas inside the Editor as well as at runtime.

The NavigationRegion2D Node uses this resource to define its navigation area.

The NavigationServer2D uses this resource to update the navigation mesh of individual regions.

The TileSet Editor creates and uses this resource internally when defining tile navigation areas.

You can see how 2D navigation works in action using the 2D Navigation Polygon and Grid-based Navigation with AStarGrid2D demo projects.

The following steps show the basic setup for minimal viable navigation in 2D. It uses the NavigationServer2D and a NavigationAgent2D for path movement.

Add a NavigationRegion2D Node to the scene.

Click on the region node and add a new NavigationPolygon Resource to the region node.

Define the movable navigation area with the NavigationPolygon draw tool. Then click the Bake NavigationPolygon button on the toolbar.

The navigation mesh defines the area where an actor can stand and move with its center. Leave enough margin between the navigation polygon edges and collision objects to not get path following actors repeatedly stuck on collision.

Add a CharacterBody2D node in the scene with a basic collision shape and a sprite or mesh for visuals.

Add a NavigationAgent2D node below the character node.

Add the following script to the CharacterBody2D node. We make sure to set a movement target after the scene has fully loaded and the NavigationServer had time to sync.

On the first frame the NavigationServer map has not synchronized region data and any path query will return empty. Wait for the NavigationServer synchronization by awaiting one frame in the script.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends CharacterBody2D

var movement_speed: float = 200.0
var movement_target_position: Vector2 = Vector2(60.0,180.0)

@onready var navigation_agent: NavigationAgent2D = $NavigationAgent2D

func _ready():
    # These values need to be adjusted for the actor's speed
    # and the navigation layout.
    navigation_agent.path_desired_distance = 4.0
    navigation_agent.target_desired_distance = 4.0

    # Make sure to not await during _ready.
    actor_setup.call_deferred()

func actor_setup():
    # Wait for the first physics frame so the NavigationServer can sync.
    await get_tree().physics_frame

    # Now that the navigation map is no longer empty, set the movement target.
    set_movement_target(movement_target_position)

func set_movement_target(movement_target: Vector2):
    navigation_agent.target_position = movement_target

func _physics_process(delta):
    if navigation_agent.is_navigation_finished():
        return

    var current_agent_position: Vector2 = global_position
    var next_path_position: Vector2 = navigation_agent.get_next_path_position()

    velocity = current_agent_position.direction_to(next_path_position) * movement_speed
    move_and_slide()
```

Example 2 (csharp):
```csharp
using Godot;

public partial class MyCharacterBody2D : CharacterBody2D
{
    private NavigationAgent2D _navigationAgent;

    private float _movementSpeed = 200.0f;
    private Vector2 _movementTargetPosition = new Vector2(70.0f, 226.0f);

    public Vector2 MovementTarget
    {
        get { return _navigationAgent.TargetPosition; }
        set { _navigationAgent.TargetPosition = value; }
    }

    public override void _Ready()
    {
        base._Ready();

        _navigationAgent = GetNode<NavigationAgent2D>("NavigationAgent2D");

        // These values need to be adjusted for the actor's speed
        // and the navigation layout.
        _navigationAgent.PathDesiredDistance = 4.0f;
        _navigationAgent.TargetDesiredDistance = 4.0f;

        // Make sure to not await during _Ready.
        Callable.From(ActorSetup).CallDeferred();
    }

    public override void _PhysicsProcess(double delta)
    {
        base._PhysicsProcess(delta);

        if (_navigationAgent.IsNavigationFinished())
        {
            return;
        }

        Vector2 currentAgentPosition = GlobalTransform.Origin;
        Vector2 nextPathPosition = _navigationAgent.GetNextPathPosition();

        Velocity = currentAgentPosition.DirectionTo(nextPathPosition) * _movementSpeed;
        MoveAndSlide();
    }

    private async void ActorSetup()
    {
        // Wait for the first physics frame so the NavigationServer can sync.
        await ToSignal(GetTree(), SceneTree.SignalName.PhysicsFrame);

        // Now that the navigation map is no longer empty, set the movement target.
        MovementTarget = _movementTargetPosition;
    }
}
```

---

## Physics introduction — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html

**Contents:**
- Physics introduction
- Collision objects
  - Physics material
  - Collision shapes
  - Physics process callback
  - Collision layers and masks
    - GUI example
    - Code example
- Area2D
- StaticBody2D

In game development, you often need to know when two objects in the game intersect or come into contact. This is known as collision detection. When a collision is detected, you typically want something to happen. This is known as collision response.

Godot offers a number of collision objects in 2D and 3D to provide both collision detection and response. Trying to decide which one to use for your project can be confusing. You can avoid problems and simplify development if you understand how each works and what their pros and cons are.

In this guide, you will learn:

Godot's four collision object types

How each collision object works

When and why to choose one type over another

This document's examples will use 2D objects. Every 2D physics object and collision shape has a direct equivalent in 3D and in most cases they work in much the same way.

Godot offers four kinds of collision objects which all extend CollisionObject2D. The last three listed below are physics bodies and additionally extend PhysicsBody2D.

Area2D nodes provide detection and influence. They can detect when objects overlap and can emit signals when bodies enter or exit. An Area2D can also be used to override physics properties, such as gravity or damping, in a defined area.

A static body is one that is not moved by the physics engine. It participates in collision detection, but does not move in response to the collision. They are most often used for objects that are part of the environment or that do not need to have any dynamic behavior.

This is the node that implements simulated 2D physics. You do not control a RigidBody2D directly, but instead you apply forces to it (gravity, impulses, etc.) and the physics engine calculates the resulting movement. Read more about using rigid bodies.

A body that provides collision detection, but no physics. All movement and collision response must be implemented in code.

Static bodies and rigid bodies can be configured to use a PhysicsMaterial. This allows adjusting the friction and bounce of an object, and set if it's absorbent and/or rough.

A physics body can hold any number of Shape2D objects as children. These shapes are used to define the object's collision bounds and to detect contact with other objects.

In order to detect collisions, at least one Shape2D must be assigned to the object.

The most common way to assign a shape is by adding a CollisionShape2D or CollisionPolygon2D as a child of the object. These nodes allow you to draw the shape directly in the editor workspace.

Be careful to never scale your collision shapes in the editor. The "Scale" property in the Inspector should remain (1, 1). When changing the size of the collision shape, you should always use the size handles, not the Node2D scale handles. Scaling a shape can result in unexpected collision behavior.

The physics engine runs at a fixed rate (a default of 60 iterations per second). This rate is typically different from the frame rate which fluctuates based on what is rendered and available resources.

It is important that all physics related code runs at this fixed rate. Therefore Godot differentiates between physics and idle processing. Code that runs each frame is called idle processing and code that runs on each physics tick is called physics processing. Godot provides two different callbacks, one for each of those processing rates.

The physics callback, Node._physics_process(), is called before each physics step. Any code that needs to access a body's properties should be run in here. This method will be passed a delta parameter, which is a floating-point number equal to the time passed in seconds since the last step. When using the default 60 Hz physics update rate, it will typically be equal to 0.01666... (but not always, see below).

It's recommended to always use the delta parameter when relevant in your physics calculations, so that the game behaves correctly if you change the physics update rate or if the player's device can't keep up.

One of the most powerful, but frequently misunderstood, collision features is the collision layer system. This system allows you to build up complex interactions between a variety of objects. The key concepts are layers and masks. Each CollisionObject2D has 32 different physics layers it can interact with.

Let's look at each of the properties in turn:

This describes the layers that the object appears in. By default, all bodies are on layer 1.

This describes what layers the body will scan for collisions. If an object isn't in one of the mask layers, the body will ignore it. By default, all bodies scan layer 1.

These properties can be configured via code, or by editing them in the Inspector.

Keeping track of what you're using each layer for can be difficult, so you may find it useful to assign names to the layers you're using. Names can be assigned in Project Settings > Layer Names > 2D Physics.

You have four node types in your game: Walls, Player, Enemy, and Coin. Both Player and Enemy should collide with Walls. The Player node should detect collisions with both Enemy and Coin, but Enemy and Coin should ignore each other.

Start by naming layers 1-4 "walls", "player", "enemies", and "coins" and place each node type in its respective layer using the "Layer" property. Then set each node's "Mask" property by selecting the layers it should interact with. For example, the Player's settings would look like this:

In function calls, layers are specified as a bitmask. Where a function enables all layers by default, the layer mask will be given as 0xffffffff. Your code can use binary, hexadecimal, or decimal notation for layer masks, depending on your preference.

The code equivalent of the above example where layers 1, 3 and 4 were enabled would be as follows:

You can also set bits independently by calling set_collision_layer_value(layer_number, value) or set_collision_mask_value(layer_number, value) on any given CollisionObject2D as follows:

Export annotations can be used to export bitmasks in the editor with a user-friendly GUI:

Additional export annotations are available for render and navigation layers, in both 2D and 3D. See Exporting bit flags.

Area nodes provide detection and influence. They can detect when objects overlap and emit signals when bodies enter or exit. Areas can also be used to override physics properties, such as gravity or damping, in a defined area.

There are three main uses for Area2D:

Overriding physics parameters (such as gravity) in a given region.

Detecting when other bodies enter or exit a region or what bodies are currently in a region.

Checking other areas for overlap.

By default, areas also receive mouse and touchscreen input.

A static body is one that is not moved by the physics engine. It participates in collision detection, but does not move in response to the collision. However, it can impart motion or rotation to a colliding body as if it were moving, using its constant_linear_velocity and constant_angular_velocity properties.

StaticBody2D nodes are most often used for objects that are part of the environment or that do not need to have any dynamic behavior.

Example uses for StaticBody2D:

Platforms (including moving platforms)

Walls and other obstacles

This is the node that implements simulated 2D physics. You do not control a RigidBody2D directly. Instead, you apply forces to it and the physics engine calculates the resulting movement, including collisions with other bodies, and collision responses, such as bouncing, rotating, etc.

You can modify a rigid body's behavior via properties such as "Mass", "Friction", or "Bounce", which can be set in the Inspector.

The body's behavior is also affected by the world's properties, as set in Project Settings > Physics, or by entering an Area2D that is overriding the global physics properties.

When a rigid body is at rest and hasn't moved for a while, it goes to sleep. A sleeping body acts like a static body, and its forces are not calculated by the physics engine. The body will wake up when forces are applied, either by a collision or via code.

One of the benefits of using a rigid body is that a lot of behavior can be had "for free" without writing any code. For example, if you were making an "Angry Birds"-style game with falling blocks, you would only need to create RigidBody2Ds and adjust their properties. Stacking, falling, and bouncing would automatically be calculated by the physics engine.

However, if you do wish to have some control over the body, you should take care - altering the position, linear_velocity, or other physics properties of a rigid body can result in unexpected behavior. If you need to alter any of the physics-related properties, you should use the _integrate_forces() callback instead of _physics_process(). In this callback, you have access to the body's PhysicsDirectBodyState2D, which allows for safely changing properties and synchronizing them with the physics engine.

For example, here is the code for an "Asteroids" style spaceship:

Note that we are not setting the linear_velocity or angular_velocity properties directly, but rather applying forces (thrust and torque) to the body and letting the physics engine calculate the resulting movement.

When a rigid body goes to sleep, the _integrate_forces() function will not be called. To override this behavior, you will need to keep the body awake by creating a collision, applying a force to it, or by disabling the can_sleep property. Be aware that this can have a negative effect on performance.

By default, rigid bodies do not keep track of contacts, because this can require a huge amount of memory if many bodies are in the scene. To enable contact reporting, set the max_contacts_reported property to a non-zero value. The contacts can then be obtained via PhysicsDirectBodyState2D.get_contact_count() and related functions.

Contact monitoring via signals can be enabled via the contact_monitor property. See RigidBody2D for the list of available signals.

CharacterBody2D bodies detect collisions with other bodies, but are not affected by physics properties like gravity or friction. Instead, they must be controlled by the user via code. The physics engine will not move a character body.

When moving a character body, you should not set its position directly. Instead, you use the move_and_collide() or move_and_slide() methods. These methods move the body along a given vector, and it will instantly stop if a collision is detected with another body. After the body has collided, any collision response must be coded manually.

After a collision, you may want the body to bounce, to slide along a wall, or to alter the properties of the object it hit. The way you handle collision response depends on which method you used to move the CharacterBody2D.

When using move_and_collide(), the function returns a KinematicCollision2D object, which contains information about the collision and the colliding body. You can use this information to determine the response.

For example, if you want to find the point in space where the collision occurred:

Or to bounce off of the colliding object:

Sliding is a common collision response; imagine a player moving along walls in a top-down game or running up and down slopes in a platformer. While it's possible to code this response yourself after using move_and_collide(), move_and_slide() provides a convenient way to implement sliding movement without writing much code.

move_and_slide() automatically includes the timestep in its calculation, so you should not multiply the velocity vector by delta. This does not apply to gravity as it is an acceleration and is time dependent, and needs to be scaled by delta.

For example, use the following code to make a character that can walk along the ground (including slopes) and jump when standing on the ground:

See Kinematic character (2D) for more details on using move_and_slide(), including a demo project with detailed code.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (markdown):
```markdown
# Example: Setting mask value for enabling layers 1, 3 and 4

# Binary - set the bit corresponding to the layers you want to enable (1, 3, and 4) to 1, set all other bits to 0.
# Note: Layer 32 is the first bit, layer 1 is the last. The mask for layers 4, 3 and 1 is therefore:
0b00000000_00000000_00000000_00001101
# (This can be shortened to 0b1101)

# Hexadecimal equivalent (1101 binary converted to hexadecimal).
0x000d
# (This value can be shortened to 0xd.)

# Decimal - Add the results of 2 to the power of (layer to be enabled - 1).
# (2^(1-1)) + (2^(3-1)) + (2^(4-1)) = 1 + 4 + 8 = 13
#
# We can use the `<<` operator to shift the bit to the left by the layer number we want to enable.
# This is a faster way to multiply by powers of 2 than `pow()`.
# Additionally, we use the `|` (binary OR) operator to combine the results of each layer.
# This ensures we don't add the same layer multiple times, which would behave incorrectly.
(1 << 1 - 1) | (1 << 3 - 1) | (1 << 4 - 1)

# The above can alternatively be written as:
# pow(2, 1 - 1) + pow(2, 3 - 1) + pow(2, 4 - 1)
```

Example 2 (csharp):
```csharp
# Example: Setting mask value to enable layers 1, 3, and 4.

var collider: CollisionObject2D = $CollisionObject2D  # Any given collider.
collider.set_collision_mask_value(1, true)
collider.set_collision_mask_value(3, true)
collider.set_collision_mask_value(4, true)
```

Example 3 (swift):
```swift
@export_flags_2d_physics var layers_2d_physics
```

Example 4 (gdscript):
```gdscript
extends RigidBody2D

var thrust = Vector2(0, -250)
var torque = 20000

func _integrate_forces(state):
    if Input.is_action_pressed("ui_up"):
        state.apply_force(thrust.rotated(rotation))
    else:
        state.apply_force(Vector2())
    var rotation_direction = 0
    if Input.is_action_pressed("ui_right"):
        rotation_direction += 1
    if Input.is_action_pressed("ui_left"):
        rotation_direction -= 1
    state.apply_torque(rotation_direction * torque)
```

---

## Using Area2D — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/using_area_2d.html

**Contents:**
- Using Area2D
- Introduction
- What is an area?
- Area properties
- Overlap detection
- Area influence
  - Point gravity
  - Examples
- User-contributed notes

Godot offers a number of collision objects to provide both collision detection and response. Trying to decide which one to use for your project can be confusing. You can avoid problems and simplify development if you understand how each of them works and what their pros and cons are. In this tutorial, we'll look at the Area2D node and show some examples of how it can be used.

This document assumes you're familiar with Godot's various physics bodies. Please read Physics introduction first.

An Area2D defines a region of 2D space. In this space you can detect other CollisionObject2D nodes overlapping, entering, and exiting. Areas also allow for overriding local physics properties. We'll explore each of these functions below.

Areas have many properties you can use to customize their behavior.

The Gravity, Linear Damp, and Angular Damp sections are used to configure the area's physics override behavior. We'll look at how to use those in the Area influence section below.

Monitoring and Monitorable are used to enable and disable the area.

The Audio Bus section allows you to override audio in the area, for example to apply an audio effect when the player moves through.

Note that Area2D extends CollisionObject2D, so it also provides properties inherited from that class. The Collision section of CollisionObject2D is where you configure the area's collision layer(s) and mask(s).

Perhaps the most common use of Area2D nodes is for contact and overlap detection. When you need to know that two objects have touched, but don't need physical collision, you can use an area to notify you of the contact.

For example, let's say we're making a coin for the player to pick up. The coin is not a solid object - the player can't stand on it or push it - we just want it to disappear when the player touches it.

Here's the node setup for the coin:

To detect the overlap, we'll connect the appropriate signal on the Area2D. Which signal to use depends on the player's node type. If the player is another area, use area_entered. However, let's assume our player is a CharacterBody2D (and therefore a CollisionObject2D type), so we'll connect the body_entered signal.

If you're not familiar with using signals, see Using signals for an introduction.

Now our player can collect the coins!

Some other usage examples:

Areas are great for bullets and other projectiles that hit and deal damage, but don't need any other physics such as bouncing.

Use a large circular area around an enemy to define its "detect" radius. When the player is outside the area, the enemy can't "see" it.

"Security cameras" - In a large level with multiple cameras, attach areas to each camera and activate them when the player enters.

See the Your first 2D game for an example of using Area2D in a game.

The second major use for area nodes is to alter physics. By default, the area won't do this, but you can enable this with the Space Override property. When areas overlap, they are processed in Priority order (higher priority areas are processed first). There are four options for override:

Combine - The area adds its values to what has been calculated so far.

Replace - The area replaces physics properties, and lower priority areas are ignored.

Combine-Replace - The area adds its gravity/damping values to whatever has been calculated so far (in priority order), ignoring any lower priority areas.

Replace-Combine - The area replaces any gravity/damping calculated so far, but keeps calculating the rest of the areas.

Using these properties, you can create very complex behavior with multiple overlapping areas.

The physics properties that can be overridden are:

Gravity - Gravity's strength inside the area.

Gravity Direction - This vector does not need to be normalized.

Linear Damp - How quickly objects stop moving - linear velocity lost per second.

Angular Damp - How quickly objects stop spinning - angular velocity lost per second.

The Gravity Point property allows you to create an "attractor". Gravity in the area will be calculated towards a point, given by the Point Center property. Values are relative to the Area2D, so for example using (0, 0) will attract objects to the center of the area.

The example project attached below has three areas demonstrating physics override.

You can download this project here: area_2d_starter.zip

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Area2D

func _on_coin_body_entered(body):
    queue_free()
```

Example 2 (swift):
```swift
using Godot;

public partial class Coin : Area2D
{
    private void OnCoinBodyEntered(PhysicsBody2D body)
    {
        QueueFree();
    }
}
```

---

## Introduction — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/physics_interpolation_introduction.html

**Contents:**
- Introduction
- Physics ticks and rendered frames
- What can we do about frames and ticks being out of sync?
  - Lock the tick / frame rate together?
  - Adapt the tick rate?
  - Lock the tick rate, but use interpolation to smooth frames in between physics ticks
  - Linear interpolation
  - The physics interpolation fraction
  - Calculating the interpolated position
  - Smoothed transformations between physics ticks?

One key concept to understand in Godot is the distinction between physics ticks (sometimes referred to as iterations or physics frames), and rendered frames. The physics proceeds at a fixed tick rate (set in Project Settings > Physics > Common > Physics Tick per Second), which defaults to 60 ticks per second.

However, the engine does not necessarily render at the same rate. Although many monitors refresh at 60 Hz (cycles per second), many refresh at completely different frequencies (e.g. 75 Hz, 144 Hz, 240 Hz or more). Even though a monitor may be able to show a new frame e.g. 60 times a second, there is no guarantee that the CPU and GPU will be able to supply frames at this rate. For instance, when running with V-Sync, the computer may be too slow for 60 and only reach the deadlines for 30 FPS, in which case the frames you see will change at 30 FPS (resulting in stuttering).

But there is a problem here. What happens if the physics ticks do not coincide with frames? What happens if the physics tick rate is out of phase with the frame rate? Or worse, what happens if the physics tick rate is lower than the rendered frame rate?

This problem is easier to understand if we consider an extreme scenario. If you set the physics tick rate to 10 ticks per second, in a simple game with a rendered frame rate of 60 FPS. If we plot a graph of the positions of an object against the rendered frames, you can see that the positions will appear to "jump" every 1/10th of a second, rather than giving a smooth motion. When the physics calculates a new position for a new object, it is not rendered in this position for just one frame, but for 6 frames.

This jump can be seen in other combinations of tick / frame rate as glitches, or jitter, caused by this staircasing effect due to the discrepancy between physics tick time and rendered frame time.

The most obvious solution is to get rid of the problem, by ensuring there is a physics tick that coincides with every frame. This used to be the approach on old consoles and fixed hardware computers. If you know that every player will be using the same hardware, you can ensure it is fast enough to calculate ticks and frames at e.g. 50 FPS, and you will be sure it will work great for everybody.

However, modern games are often no longer made for fixed hardware. You will often be planning to release on desktop computers, mobiles, and more. All of which have huge variations in performance, as well as different monitor refresh rates. We need to come up with a better way of dealing with the problem.

Instead of designing the game at a fixed physics tick rate, we could allow the tick rate to scale according to the end user's hardware. We could for example use a fixed tick rate that works for that hardware, or even vary the duration of each physics tick to match a particular frame duration.

This works, but there is a problem. Physics (and game logic, which is often also run in the _physics_process) work best and most consistently when run at a fixed, predetermined tick rate. If you attempt to run a racing game physics that has been designed for 60 TPS (ticks per second) at e.g. 10 TPS, the physics will behave completely differently. Controls may be less responsive, collisions / trajectories can be completely different. You may test your game thoroughly at 60 TPS, then find it breaks on end users' machines when it runs at a different tick rate.

This can make quality assurance difficult with hard to reproduce bugs, especially in AAA games where problems of this sort can be very costly. This can also be problematic for multiplayer games for competitive integrity, as running the game at certain tick rates may be more advantageous than others.

This has become one of the most popular approaches to deal with the problem, although it is optional and disabled by default.

We have established that the most desirable physics/game logic arrangement for consistency and predictability is a physics tick rate that is fixed at design-time. The problem is the discrepancy between the physics position recorded, and where we "want" a physics object to be shown on a frame to give smooth motion.

The answer turns out to be simple, but can be a little hard to get your head around at first.

Instead of keeping track of just the current position of a physics object in the engine, we keep track of both the current position of the object, and the previous position on the previous physics tick.

Why do we need the previous position (in fact the entire transform, including rotation and scaling)? By using a little math magic, we can use interpolation to calculate what the transform of the object would be between those two points, in our ideal world of smooth continuous movement.

The simplest way to achieve this is linear interpolation, or lerping, which you may have used before.

Let us consider only the position, and a situation where we know that the previous physics tick X coordinate was 10 units, and the current physics tick X coordinate is 30 units.

Although the maths is explained here, you do not have to worry about the details, as this step will be performed for you. Under the hood, Godot may use more complex forms of interpolation, but linear interpolation is the easiest in terms of explanation.

If our physics ticks are happening 10 times per second (for this example), what happens if our rendered frame takes place at time 0.12 seconds? We can do some math to figure out where the object would be to obtain a smooth motion between the two ticks.

First of all, we have to calculate how far through the physics tick we want the object to be. If the last physics tick took place at 0.1 seconds, we are 0.02 seconds (0.12 - 0.1) through a tick that we know will take 0.1 seconds (10 ticks per second). The fraction through the tick is thus:

This is called the physics interpolation fraction, and is handily calculated for you by Godot. It can be retrieved on any frame by calling Engine.get_physics_interpolation_fraction.

Once we have the interpolation fraction, we can insert it into a standard linear interpolation equation. The X coordinate would thus be:

So substituting our x_prev as 10, and x_curr as 30:

Let's break that down:

We know the X starts from the coordinate on the previous tick (x_prev) which is 10 units.

We know that after the full tick, the difference between the current tick and the previous tick will have been added (x_curr - x_prev) (which is 20 units).

The only thing we need to vary is the proportion of this difference we add, according to how far we are through the physics tick.

Although this example interpolates the position, the same thing can be done with the rotation and scale of objects. It is not necessary to know the details as Godot will do all this for you.

Putting all this together shows that it should be possible to have a nice smooth estimation of the transform of objects between the current and previous physics tick.

But wait, you may have noticed something. If we are interpolating between the current and previous ticks, we are not estimating the position of the object now, we are estimating the position of the object in the past. To be exact, we are estimating the position of the object between 1 and 2 ticks into the past.

What does this mean? This scheme does work, but it does mean we are effectively introducing a delay between what we see on the screen, and where the objects should be.

In practice, most people won't notice this delay, or rather, it is typically not objectionable. There are already significant delays involved in games, we just don't typically notice them. The most significant effect is there can be a slight delay to input, which can be a factor in fast twitch games. In some of these fast input situations, you may wish to turn off physics interpolation and use a different scheme, or use a high tick rate, which mitigates these delays.

There is an alternative to this scheme, which is: instead of interpolating between the previous and current tick, we use maths to extrapolate into the future. We try to predict where the object will be, rather than show it where it was. This can be done and may be offered as an option in future, but there are some significant downsides:

The prediction may not be correct, especially when an object collides with another object during the physics tick.

Where a prediction was incorrect, the object may extrapolate into an "impossible" position, like inside a wall.

Providing the movement speed is slow, these incorrect predictions may not be too much of a problem.

When a prediction was incorrect, the object may have to jump or snap back onto the corrected path. This can be visually jarring.

In Godot this whole system is referred to as physics interpolation, but you may also hear it referred to as "fixed timestep interpolation", as it is interpolating between objects moved with a fixed timestep (physics ticks per second). In some ways the second term is more accurate, because it can also be used to interpolate objects that are not driven by physics.

Although physics interpolation is usually a good choice, there are exceptions where you may choose not to use Godot's built-in physics interpolation (or use it in a limited fashion). An example category is internet multiplayer games. Multiplayer games often receive tick or timing based information from other players or a server and these may not coincide with local physics ticks, so a custom interpolation technique can often be a better fit.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
fraction = 0.02 / 0.10
fraction = 0.2
```

Example 2 (unknown):
```unknown
x_interpolated = x_prev + ((x_curr - x_prev) * 0.2)
```

Example 3 (unknown):
```unknown
x_interpolated = 10 + ((30 - 10) * 0.2)
x_interpolated = 10 + 4
x_interpolated = 14
```

---

## Introduction to shaders — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html

**Contents:**
- Introduction to shaders
- Shaders in Godot
- Shader types
- Render modes
  - Vertex processor
  - Fragment processor
  - Light processor
- User-contributed notes

This page explains what shaders are and will give you an overview of how they work in Godot. For a detailed reference of the engine's shading language, see Shading language.

Shaders are a special kind of program that runs on Graphics Processing Units (GPUs). They were initially used to shade 3D scenes but can nowadays do much more. You can use them to control how the engine draws geometry and pixels on the screen, allowing you to achieve all sorts of effects.

Modern rendering engines like Godot draw everything with shaders: graphics cards can run thousands of instructions in parallel, leading to incredible rendering speed.

Because of their parallel nature, though, shaders don't process information the way a typical program does. Shader code runs on each vertex or pixel in isolation. You cannot store data between frames either. As a result, when working with shaders, you need to code and think differently from other programming languages.

Suppose you want to update all the pixels in a texture to a given color. In GDScript, your code would use for loops:

Your code is already part of a loop in a shader, so the corresponding code would look like this.

The graphics card calls the fragment() function once or more for each pixel it has to draw. More on that below.

Godot provides a shading language based on the popular OpenGL Shading Language (GLSL) but simplified. The engine handles some of the lower-level initialization work for you, making it easier to write complex shaders.

In Godot, shaders are made up of main functions called "processor functions". Processor functions are the entry point for your shader into the program. There are seven different processor functions.

The vertex() function runs over all the vertices in the mesh and sets their positions and some other per-vertex variables. Used in canvas_item shaders and spatial shaders.

The fragment() function runs for every pixel covered by the mesh. It uses values output by the vertex() function, interpolated between the vertices. Used in canvas_item shaders and spatial shaders.

The light() function runs for every pixel and for every light. It takes variables from the fragment() function and from its previous runs. Used in canvas_item shaders and spatial shaders.

The start() function runs for every particle in a particle system once when the particle is first spawned. Used in particles shaders.

The process() function runs for every particle in a particle system for each frame. Used in particles shaders.

The sky() function runs for every pixel in the radiance cubemap when the radiance cubemap needs to be updated, and for every pixel on the current screen. Used in sky shaders.

The fog() function runs for every froxel in the volumetric fog froxel buffer that intersects with the FogVolume. Used by fog shaders.

The light() function won't run if the vertex_lighting render mode is enabled, or if Rendering > Quality > Shading > Force Vertex Shading is enabled in the Project Settings. It's enabled by default on mobile platforms.

Godot also exposes an API for users to write totally custom GLSL shaders. For more information see Using compute shaders.

Instead of supplying a general-purpose configuration for all uses (2D, 3D, particles, sky, fog), you must specify the type of shader you're writing. Different types support different render modes, built-in variables, and processing functions.

In Godot, all shaders need to specify their type in the first line, like so:

Here are the available types:

spatial for 3D rendering.

canvas_item for 2D rendering.

particles for particle systems.

fog to render FogVolumes

Shaders have optional render modes you can specify on the second line, after the shader type, like so:

Render modes alter the way Godot applies the shader. For example, the unshaded mode makes the engine skip the built-in light processor function.

Each shader type has different render modes. See the reference for each shader type for a complete list of render modes.

The vertex() processing function is called once for every vertex in spatial and canvas_item shaders.

Each vertex in your world's geometry has properties like a position and color. The function modifies those values and passes them to the fragment function. You can also use it to send extra data to the fragment function using varyings.

By default, Godot transforms your vertex information for you, which is necessary to project geometry onto the screen. You can use render modes to transform the data yourself; see the Spatial shader doc for an example.

The fragment() processing function is used to set up the Godot material parameters per pixel. This code runs on every visible pixel the object or primitive draws. It is only available in spatial and canvas_item shaders.

The standard use of the fragment function is to set up material properties used to calculate lighting. For example, you would set values for ROUGHNESS, RIM, or TRANSMISSION, which would tell the light function how the lights respond to that fragment. This makes it possible to control a complex shading pipeline without the user having to write much code. If you don't need this built-in functionality, you can ignore it and write your own light processing function, and Godot will optimize it away. For example, if you do not write a value to RIM, Godot will not calculate rim lighting. During compilation, Godot checks to see if RIM is used; if not, it cuts all the corresponding code out. Therefore, you will not waste calculations on the effects that you do not use.

The light() processor runs per pixel too, and it runs once for every light that affects the object. It does not run if no lights affect the object. It exists as a function called inside the fragment() processor and typically operates on the material properties setup inside the fragment() function.

The light() processor works differently in 2D than it does in 3D; for a description of how it works in each, see their documentation, CanvasItem shaders and Spatial shaders, respectively.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (bash):
```bash
for x in range(width):
    for y in range(height):
        set_color(x, y, some_color)
```

Example 2 (cpp):
```cpp
void fragment() {
    COLOR = some_color;
}
```

Example 3 (unknown):
```unknown
shader_type spatial;
```

Example 4 (unknown):
```unknown
shader_type spatial;
render_mode unshaded, cull_disabled;
```

---

## Your first shader — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/index.html

**Contents:**
- Your first shader

This tutorial series will walk you through writing your first shader. It is intended for people who have very little prior experience with shaders and want to get started with the basics. This tutorial will not cover advanced topics and it is not comprehensive. For a comprehensive and detailed overview of shaders in Godot see the Shading Reference Page.

The "your first shader" tutorials walk you through the process of writing a shader step-by-step.

For a more general introduction into shaders and the OpenGL Shading Language, use The Book of Shaders.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Your second 3D shader — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_second_3d_shader.html

**Contents:**
- Your second 3D shader
- Your first spatial fragment function
- Animating with TIME
- Advanced effects: waves
- User-contributed notes

From a high-level, what Godot does is give the user a bunch of parameters that can be optionally set (AO, SSS_Strength, RIM, etc.). These parameters correspond to different complex effects (Ambient Occlusion, SubSurface Scattering, Rim Lighting, etc.). When not written to, the code is thrown out before it is compiled and so the shader does not incur the cost of the extra feature. This makes it easy for users to have complex PBR-correct shading, without writing complex shaders. Of course, Godot also allows you to ignore all these parameters and write a fully customized shader.

For a full list of these parameters see the spatial shader reference doc.

A difference between the vertex function and a fragment function is that the vertex function runs per vertex and sets properties such as VERTEX (position) and NORMAL, while the fragment shader runs per pixel and, most importantly, sets the ALBEDO color of the MeshInstance3D.

As mentioned in the previous part of this tutorial. The standard use of the fragment function in Godot is to set up different material properties and let Godot handle the rest. In order to provide even more flexibility, Godot also provides things called render modes. Render modes are set at the top of the shader, directly below shader_type, and they specify what sort of functionality you want the built-in aspects of the shader to have.

For example, if you do not want to have lights affect an object, set the render mode to unshaded:

You can also stack multiple render modes together. For example, if you want to use toon shading instead of more-realistic PBR shading, set the diffuse mode and specular mode to toon:

This model of built-in functionality allows you to write complex custom shaders by changing only a few parameters.

For a full list of render modes see the Spatial shader reference.

In this part of the tutorial, we will walk through how to take the bumpy terrain from the previous part and turn it into an ocean.

First let's set the color of the water. We do that by setting ALBEDO.

ALBEDO is a vec3 that contains the color of the object.

Let's set it to a nice shade of blue.

We set it to a very dark shade of blue because most of the blueness of the water will come from reflections from the sky.

The PBR model that Godot uses relies on two main parameters: METALLIC and ROUGHNESS.

ROUGHNESS specifies how smooth/rough the surface of a material is. A low ROUGHNESS will make a material appear like a shiny plastic, while a high roughness makes the material appear more solid in color.

METALLIC specifies how much like a metal the object is. It is better set close to 0 or 1. Think of METALLIC as changing the balance between the reflection and the ALBEDO color. A high METALLIC almost ignores ALBEDO altogether, and looks like a mirror of the sky. While a low METALLIC has a more equal representation of sky color and ALBEDO color.

ROUGHNESS increases from 0 to 1 from left to right while METALLIC increase from 0 to 1 from top to bottom.

METALLIC should be close to 0 or 1 for proper PBR shading. Only set it between them for blending between materials.

Water is not a metal, so we will set its METALLIC property to 0.0. Water is also highly reflective, so we will set its ROUGHNESS property to be quite low as well.

Now we have a smooth plastic looking surface. It is time to think about some particular properties of water that we want to emulate. There are two main ones that will take this from a weird plastic surface to nice stylized water. The first is specular reflections. Specular reflections are those bright spots you see from where the sun reflects directly into your eye. The second is fresnel reflectance. Fresnel reflectance is the property of objects to become more reflective at shallow angles. It is the reason why you can see into water below you, but farther away it reflects the sky.

In order to increase the specular reflections, we will do two things. First, we will change the render mode for specular to toon because the toon render mode has larger specular highlights.

Second we will add rim lighting. Rim lighting increases the effect of light at glancing angles. Usually it is used to emulate the way light passes through fabric on the edges of an object, but we will use it here to help achieve a nice watery effect.

In order to add fresnel reflectance, we will compute a fresnel term in our fragment shader. Here, we aren't going to use a real fresnel term for performance reasons. Instead, we'll approximate it using the dot product of the NORMAL and VIEW vectors. The NORMAL vector points away from the mesh's surface, while the VIEW vector is the direction between your eye and that point on the surface. The dot product between them is a handy way to tell when you are looking at the surface head-on or at a glancing angle.

And mix it into both ROUGHNESS and ALBEDO. This is the benefit of ShaderMaterials over StandardMaterial3Ds. With StandardMaterial3D, we could set these properties with a texture, or to a flat number. But with shaders we can set them based on any mathematical function that we can dream up.

And now, with only 5 lines of code, you can have complex looking water. Now that we have lighting, this water is looking too bright. Let's darken it. This is done easily by decreasing the values of the vec3 we pass into ALBEDO. Let's set them to vec3(0.01, 0.03, 0.05).

Going back to the vertex function, we can animate the waves using the built-in variable TIME.

TIME is a built-in variable that is accessible from the vertex and fragment functions.

In the last tutorial we calculated height by reading from a heightmap. For this tutorial, we will do the same. Put the heightmap code in a function called height().

In order to use TIME in the height() function, we need to pass it in.

And make sure to correctly pass it in inside the vertex function.

Instead of using a normalmap to calculate normals. We are going to compute them manually in the vertex() function. To do so use the following line of code.

We need to compute NORMAL manually because in the next section we will be using math to create complex-looking waves.

Now, we are going to make the height() function a little more complicated by offsetting position by the cosine of TIME.

This results in waves that move slowly, but not in a very natural way. The next section will dig deeper into using shaders to create more complex effects, in this case realistic waves, by adding a few more mathematical functions.

What makes shaders so powerful is that you can achieve complex effects by using math. To illustrate this, we are going to take our waves to the next level by modifying the height() function and by introducing a new function called wave().

wave() has one parameter, position, which is the same as it is in height().

We are going to call wave() multiple times in height() in order to fake the way waves look.

At first this looks complicated. So let's go through it line-by-line.

Offset the position by the noise texture. This will make the waves curve, so they won't be straight lines completely aligned with the grid.

Define a wave-like function using sin() and position. Normally sin() waves are very round. We use abs() to absolute to give them a sharp ridge and constrain them to the 0-1 range. And then we subtract it from 1.0 to put the peak on top.

Multiply the x-directional wave by the y-directional wave and raise it to a power to sharpen the peaks. Then subtract that from 1.0 so that the ridges become peaks and raise that to a power to sharpen the ridges.

We can now replace the contents of our height() function with wave().

The shape of the sin wave is too obvious. So let's spread the waves out a bit. We do this by scaling position.

Now it looks much better.

We can do even better if we layer multiple waves on top of each other at varying frequencies and amplitudes. What this means is that we are going to scale position for each one to make the waves thinner or wider (frequency). And we are going to multiply the output of the wave to make them shorter or taller (amplitude).

Here is an example for how you could layer the four waves to achieve nicer looking waves.

Note that we add time to two and subtract it from the other two. This makes the waves move in different directions creating a complex effect. Also note that the amplitudes (the number the result is multiplied by) all add up to 1.0. This keeps the wave in the 0-1 range.

With this code you should end up with more complex looking waves and all you had to do was add a bit of math!

For more information about Spatial shaders read the Shading Language doc and the Spatial Shaders doc. Also look at more advanced tutorials in the Shading section and the 3D sections.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
render_mode unshaded;
```

Example 2 (unknown):
```unknown
render_mode diffuse_toon, specular_toon;
```

Example 3 (cpp):
```cpp
void fragment() {
  ALBEDO = vec3(0.1, 0.3, 0.5);
}
```

Example 4 (cpp):
```cpp
void fragment() {
  METALLIC = 0.0;
  ROUGHNESS = 0.01;
  ALBEDO = vec3(0.1, 0.3, 0.5);
}
```

---

## Using compute shaders — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html

**Contents:**
- Using compute shaders
- Create a local RenderingDevice
- Provide input data
- Defining a compute pipeline
- Execute a compute shader
- Retrieving results
- Freeing memory
- User-contributed notes

This tutorial will walk you through the process of creating a minimal compute shader. But first, a bit of background on compute shaders and how they work with Godot.

This tutorial assumes you are familiar with shaders generally. If you are new to shaders please read Introduction to shaders and your first shader before proceeding with this tutorial.

A compute shader is a special type of shader program that is orientated towards general purpose programming. In other words, they are more flexible than vertex shaders and fragment shaders as they don't have a fixed purpose (i.e. transforming vertices or writing colors to an image). Unlike fragment shaders and vertex shaders, compute shaders have very little going on behind the scenes. The code you write is what the GPU runs and very little else. This can make them a very useful tool to offload heavy calculations to the GPU.

Now let's get started by creating a short compute shader.

First, in the external text editor of your choice, create a new file called compute_example.glsl in your project folder. When you write compute shaders in Godot, you write them in GLSL directly. The Godot shader language is based on GLSL. If you are familiar with normal shaders in Godot, the syntax below will look somewhat familiar.

Compute shaders can only be used from RenderingDevice-based renderers (the Forward+ or Mobile renderer). To follow along with this tutorial, ensure that you are using the Forward+ or Mobile renderer. The setting for which is located in the top right-hand corner of the editor.

Note that compute shader support is generally poor on mobile devices (due to driver bugs), even if they are technically supported.

Let's take a look at this compute shader code:

This code takes an array of floats, multiplies each element by 2 and store the results back in the buffer array. Now let's look at it line-by-line.

These two lines communicate two things:

The following code is a compute shader. This is a Godot-specific hint that is needed for the editor to properly import the shader file.

The code is using GLSL version 450.

You should never have to change these two lines for your custom compute shaders.

Next, we communicate the number of invocations to be used in each workgroup. Invocations are instances of the shader that are running within the same workgroup. When we launch a compute shader from the CPU, we tell it how many workgroups to run. Workgroups run in parallel to each other. While running one workgroup, you cannot access information in another workgroup. However, invocations in the same workgroup can have some limited access to other invocations.

Think about workgroups and invocations as a giant nested for loop.

Workgroups and invocations are an advanced topic. For now, remember that we will be running two invocations per workgroup.

Here we provide information about the memory that the compute shader will have access to. The layout property allows us to tell the shader where to look for the buffer, we will need to match these set and binding positions from the CPU side later.

The restrict keyword tells the shader that this buffer is only going to be accessed from one place in this shader. In other words, we won't bind this buffer in another set or binding index. This is important as it allows the shader compiler to optimize the shader code. Always use restrict when you can.

This is an unsized buffer, which means it can be any size. So we need to be careful not to read from an index larger than the size of the buffer.

Finally, we write the main function which is where all the logic happens. We access a position in the storage buffer using the gl_GlobalInvocationID built-in variables. gl_GlobalInvocationID gives you the global unique ID for the current invocation.

To continue, write the code above into your newly created compute_example.glsl file.

To interact with and execute a compute shader, we need a script. Create a new script in the language of your choice and attach it to any Node in your scene.

Now to execute our shader we need a local RenderingDevice which can be created using the RenderingServer:

After that, we can load the newly created shader file compute_example.glsl and create a precompiled version of it using this:

Local RenderingDevices cannot be debugged using tools such as RenderDoc.

As you might remember, we want to pass an input array to our shader, multiply each element by 2 and get the results.

We need to create a buffer to pass values to a compute shader. We are dealing with an array of floats, so we will use a storage buffer for this example. A storage buffer takes an array of bytes and allows the CPU to transfer data to and from the GPU.

So let's initialize an array of floats and create a storage buffer:

With the buffer in place we need to tell the rendering device to use this buffer. To do that we will need to create a uniform (like in normal shaders) and assign it to a uniform set which we can pass to our shader later.

The next step is to create a set of instructions our GPU can execute. We need a pipeline and a compute list for that.

The steps we need to do to compute our result are:

Create a new pipeline.

Begin a list of instructions for our GPU to execute.

Bind our compute list to our pipeline

Bind our buffer uniform to our pipeline

Specify how many workgroups to use

End the list of instructions

Note that we are dispatching the compute shader with 5 work groups in the X axis, and one in the others. Since we have 2 local invocations in the X axis (specified in our shader), 10 compute shader invocations will be launched in total. If you read or write to indices outside of the range of your buffer, you may access memory outside of your shaders control or parts of other variables which may cause issues on some hardware.

After all of this we are almost done, but we still need to execute our pipeline. So far we have only recorded what we would like the GPU to do; we have not actually run the shader program.

To execute our compute shader we need to submit the pipeline to the GPU and wait for the execution to finish:

Ideally, you would not call sync() to synchronize the RenderingDevice right away as it will cause the CPU to wait for the GPU to finish working. In our example, we synchronize right away because we want our data available for reading right away. In general, you will want to wait at least 2 or 3 frames before synchronizing so that the GPU is able to run in parallel with the CPU.

Long computations can cause Windows graphics drivers to "crash" due to TDR being triggered by Windows. This is a mechanism that reinitializes the graphics driver after a certain amount of time has passed without any activity from the graphics driver (usually 5 to 10 seconds).

Depending on the duration your compute shader takes to execute, you may need to split it into multiple dispatches to reduce the time each dispatch takes and reduce the chances of triggering a TDR. Given TDR is time-dependent, slower GPUs may be more prone to TDRs when running a given compute shader compared to a faster GPU.

You may have noticed that, in the example shader, we modified the contents of the storage buffer. In other words, the shader read from our array and stored the data in the same array again so our results are already there. Let's retrieve the data and print the results to our console.

The buffer, pipeline, and uniform_set variables we've been using are each an RID. Because RenderingDevice is meant to be a lower-level API, RIDs aren't freed automatically. This means that once you're done using buffer or any other RID, you are responsible for freeing its memory manually using the RenderingDevice's free_rid() method.

With that, you have everything you need to get started working with compute shaders.

The demo projects repository contains a Compute Shader Heightmap demo This project performs heightmap image generation on the CPU and GPU separately, which lets you compare how a similar algorithm can be implemented in two different ways (with the GPU implementation being faster in most cases).

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (cpp):
```cpp
#[compute]
#version 450

// Invocations in the (x, y, z) dimension
layout(local_size_x = 2, local_size_y = 1, local_size_z = 1) in;

// A binding to the buffer we create in our script
layout(set = 0, binding = 0, std430) restrict buffer MyDataBuffer {
    float data[];
}
my_data_buffer;

// The code we want to execute in each invocation
void main() {
    // gl_GlobalInvocationID.x uniquely identifies this invocation across all work groups
    my_data_buffer.data[gl_GlobalInvocationID.x] *= 2.0;
}
```

Example 2 (unknown):
```unknown
#[compute]
#version 450
```

Example 3 (unknown):
```unknown
// Invocations in the (x, y, z) dimension
layout(local_size_x = 2, local_size_y = 1, local_size_z = 1) in;
```

Example 4 (unknown):
```unknown
for (int x = 0; x < workgroup_size_x; x++) {
  for (int y = 0; y < workgroup_size_y; y++) {
     for (int z = 0; z < workgroup_size_z; z++) {
        // Each workgroup runs independently and in parallel.
        for (int local_x = 0; local_x < invocation_size_x; local_x++) {
           for (int local_y = 0; local_y < invocation_size_y; local_y++) {
              for (int local_z = 0; local_z < invocation_size_z; local_z++) {
                 // Compute shader runs here.
              }
           }
        }
     }
  }
}
```

---

## Your first 2D shader — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_first_2d_shader.html

**Contents:**
- Your first 2D shader
- Introduction
- Setup
- Your first CanvasItem shader
- Your first fragment function
  - Using TEXTURE built-in
  - Uniform input
  - Interacting with shaders from code
- Your first vertex function
- Conclusion

Shaders are special programs that execute on the GPU and are used for rendering graphics. All modern rendering is done with shaders. For a more detailed description of what shaders are please see What are shaders.

This tutorial will focus on the practical aspects of writing shader programs by walking you through the process of writing a shader with both vertex and fragment functions. This tutorial targets absolute beginners to shaders.

If you have experience writing shaders and are just looking for an overview of how shaders work in Godot, see the Shading Reference.

CanvasItem shaders are used to draw all 2D objects in Godot, while Spatial shaders are used to draw all 3D objects.

In order to use a shader it must be attached inside a Material which must be attached to an object. Materials are a type of Resource. To draw multiple objects with the same material, the material must be attached to each object.

All objects derived from a CanvasItem have a material property. This includes all GUI elements, Sprite2Ds, TileMapLayers, MeshInstance2Ds etc. They also have an option to inherit their parent's material. This can be useful if you have a large number of nodes that you want to use the same material.

To begin, create a Sprite2D node. You can use any CanvasItem, so long as it is drawing to the canvas, so for this tutorial we will use a Sprite2D, as it is the easiest CanvasItem to start drawing with.

In the Inspector, click beside "Texture" where it says "[empty]" and select "Load", then select "icon.svg". For new projects, this is the Godot icon. You should now see the icon in the viewport.

Next, look down in the Inspector, under the CanvasItem section, click beside "Material" and select "New ShaderMaterial". This creates a new Material resource. Click on the sphere that appears. Godot currently doesn't know whether you are writing a CanvasItem Shader or a Spatial Shader and it previews the output of spatial shaders. So what you are seeing is the output of the default Spatial Shader.

Materials that inherit from the Material resource, such as StandardMaterial3D and ParticleProcessMaterial, can be converted to a ShaderMaterial and their existing properties will be converted to an accompanying text shader. To do so, right-click on the material in the FileSystem dock and choose Convert to ShaderMaterial. You can also do so by right-clicking on any property holding a reference to the material in the inspector.

Click beside "Shader" and select "New Shader". Finally, click on the shader you just created and the shader editor will open. You are now ready to begin writing your first shader.

In Godot, all shaders start with a line specifying what type of shader they are. It uses the following format:

Because we are writing a CanvasItem shader, we specify canvas_item in the first line. All our code will go beneath this declaration.

This line tells the engine which built-in variables and functionality to supply you with.

In Godot you can override three functions to control how the shader operates; vertex, fragment, and light. This tutorial will walk you through writing a shader with both vertex and fragment functions. Light functions are significantly more complex than vertex and fragment functions and so will not be covered here.

The fragment function runs for every pixel in a Sprite2D and determines what color that pixel should be.

They are restricted to the pixels covered by the Sprite2D, that means you cannot use one to, for example, create an outline around a Sprite2D.

The most basic fragment function does nothing except assign a single color to every pixel.

We do so by writing a vec4 to the built-in variable COLOR. vec4 is shorthand for constructing a vector with 4 numbers. For more information about vectors see the Vector math tutorial. COLOR is both an input variable to the fragment function and the final output from it.

Congratulations! You're done. You have successfully written your first shader in Godot.

Now let's make things more complex.

There are many inputs to the fragment function that you can use for calculating COLOR. UV is one of them. UV coordinates are specified in your Sprite2D (without you knowing it!) and they tell the shader where to read from textures for each part of the mesh.

In the fragment function you can only read from UV, but you can use it in other functions or to assign values to COLOR directly.

UV varies between 0-1 from left-right and from top-bottom.

The default fragment function reads from the set Sprite2D texture and displays it.

When you want to adjust a color in a Sprite2D you can adjust the color from the texture manually like in the code below.

Certain nodes, like Sprite2Ds, have a dedicated texture variable that can be accessed in the shader using TEXTURE. If you want to use the Sprite2D texture to combine with other colors, you can use the UV with the texture function to access this variable. Use them to redraw the Sprite2D with the texture.

Uniform input is used to pass data into a shader that will be the same across the entire shader.

You can use uniforms by defining them at the top of your shader like so:

For more information about usage see the Shading Language doc.

Add a uniform to change the amount of blue in our Sprite2D.

Now you can change the amount of blue in the Sprite2D from the editor. Look back at the Inspector under where you created your shader. You should see a section called "Shader Param". Unfold that section and you will see the uniform you just declared. If you change the value in the editor, it will overwrite the default value you provided in the shader.

You can change uniforms from code using the function set_shader_parameter() which is called on the node's material resource. With a Sprite2D node, the following code can be used to set the blue uniform.

Note that the name of the uniform is a string. The string must match exactly with how it is written in the shader, including spelling and case.

Now that we have a fragment function, let's write a vertex function.

Use the vertex function to calculate where on the screen each vertex should end up.

The most important variable in the vertex function is VERTEX. Initially, it specifies the vertex coordinates in your model, but you also write to it to determine where to actually draw those vertices. VERTEX is a vec2 that is initially presented in local-space (i.e. not relative to the camera, viewport, or parent nodes).

You can offset the vertices by directly adding to VERTEX.

Combined with the TIME built-in variable, this can be used for basic animation.

At their core, shaders do what you have seen so far, they compute VERTEX and COLOR. It is up to you to dream up more complex mathematical strategies for assigning values to those variables.

For inspiration, take a look at some of the more advanced shader tutorials, and look at other sites like Shadertoy and The Book of Shaders.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
shader_type canvas_item;
```

Example 2 (cpp):
```cpp
void fragment(){
  COLOR = vec4(0.4, 0.6, 0.9, 1.0);
}
```

Example 3 (cpp):
```cpp
void fragment() {
  COLOR = vec4(UV, 0.5, 1.0);
}
```

Example 4 (cpp):
```cpp
void fragment(){
  // This shader will result in a blue-tinted icon
  COLOR.b = 1.0;
}
```

---

## Your first 3D shader — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/shaders/your_first_shader/your_first_3d_shader.html

**Contents:**
- Your first 3D shader
- Where to assign my material
- Setting up
- Shader magic
- Noise heightmap
- Uniforms
- Interacting with light
- Full code
- User-contributed notes

You have decided to start writing your own custom Spatial shader. Maybe you saw a cool trick online that was done with shaders, or you have found that the StandardMaterial3D isn't quite meeting your needs. Either way, you have decided to write your own and now you need to figure out where to start.

This tutorial will explain how to write a Spatial shader and will cover more topics than the CanvasItem tutorial.

Spatial shaders have more built-in functionality than CanvasItem shaders. The expectation with spatial shaders is that Godot has already provided the functionality for common use cases and all the user needs to do in the shader is set the proper parameters. This is especially true for a PBR (physically based rendering) workflow.

This is a two-part tutorial. In this first part we will create terrain using vertex displacement from a heightmap in the vertex function. In the second part we will take the concepts from this tutorial and set up custom materials in a fragment shader by writing an ocean water shader.

This tutorial assumes some basic shader knowledge such as types (vec2, float, sampler2D), and functions. If you are uncomfortable with these concepts it is best to get a gentle introduction from The Book of Shaders before completing this tutorial.

In 3D, objects are drawn using Meshes. Meshes are a resource type that store geometry (the shape of your object) and materials (the color and how the object reacts to light) in units called "surfaces". A Mesh can have multiple surfaces, or just one. Typically, you would import a mesh from another program (e.g. Blender). But Godot also has a few PrimitiveMeshes that allow you to add basic geometry to a scene without importing Meshes.

There are multiple node types that you can use to draw a mesh. The main one is MeshInstance3D, but you can also use GPUParticles3D, MultiMeshes (with a MultiMeshInstance3D), or others.

Typically, a material is associated with a given surface in a mesh, but some nodes, like MeshInstance3D, allow you to override the material for a specific surface, or for all surfaces.

If you set a material on the surface or mesh itself, then all MeshInstance3Ds that share that mesh will share that material. However, if you want to reuse the same mesh across multiple mesh instances, but have different materials for each instance then you should set the material on the MeshInstance3D.

For this tutorial we will set our material on the mesh itself rather than taking advantage of the MeshInstance3D's ability to override materials.

Add a new MeshInstance3D node to your scene.

In the inspector tab, set the MeshInstance3D's Mesh property to a new PlaneMesh resource, by clicking on <empty> and choosing New PlaneMesh. Then expand the resource by clicking on the image of a plane that appears.

This adds a plane to our scene.

Then, in the viewport, click in the upper left corner on the Perspective button. In the menu that appears, select Display Wireframe.

This will allow you to see the triangles making up the plane.

Now set Subdivide Width and Subdivide Depth of the PlaneMesh to 32.

You can see that there are now many more triangles in the MeshInstance3D. This will give us more vertices to work with and thus allow us to add more detail.

PrimitiveMeshes, like PlaneMesh, only have one surface, so instead of an array of materials there is only one. Set the Material to a new ShaderMaterial, then expand the material by clicking on the sphere that appears.

Materials that inherit from the Material resource, such as StandardMaterial3D and ParticleProcessMaterial, can be converted to a ShaderMaterial and their existing properties will be converted to an accompanying text shader. To do so, right-click on the material in the FileSystem dock and choose Convert to ShaderMaterial. You can also do so by right-clicking on any property holding a reference to the material in the inspector.

Now set the material's Shader to a new Shader by clicking <empty> and select New Shader.... Leave the default settings, give your shader a name, and click Create.

Click on the shader in the inspector, and the shader editor should now pop up. You are ready to begin writing your first Spatial shader!

The new shader is already generated with a shader_type variable, the vertex() function, and the fragment() function. The first thing Godot shaders need is a declaration of what type of shader they are. In this case the shader_type is set to spatial because this is a spatial shader.

The vertex() function determines where the vertices of your MeshInstance3D appear in the final scene. We will be using it to offset the height of each vertex and make our flat plane appear like a little terrain.

With nothing in the vertex() function, Godot will use its default vertex shader. We can start to make changes by adding a single line:

Adding this line, you should get an image like the one below.

Okay, let's unpack this. The y value of the VERTEX is being increased. And we are passing the x and z components of the VERTEX as arguments to cos() and sin(); that gives us a wave-like appearance across the x and z axes.

What we want to achieve is the look of little hills; after all. cos() and sin() already look kind of like hills. We do so by scaling the inputs to the cos() and sin() functions.

This looks better, but it is still too spiky and repetitive, let's make it a little more interesting.

Noise is a very popular tool for faking the look of terrain. Think of it as similar to the cosine function where you have repeating hills except, with noise, each hill has a different height.

Godot provides the NoiseTexture2D resource for generating a noise texture that can be accessed from a shader.

To access a texture in a shader add the following code near the top of your shader, outside the vertex() function.

This will allow you to send a noise texture to the shader. Now look in the inspector under your material. You should see a section called Shader Parameters. If you open it up, you'll see a parameter called "Noise".

Set this Noise parameter to a new NoiseTexture2D. Then in your NoiseTexture2D, set its Noise property to a new FastNoiseLite. The FastNoiseLite class is used by the NoiseTexture2D to generate a heightmap.

Once you set it up and should look like this.

Now, access the noise texture using the texture() function:

texture() takes a texture as the first argument and a vec2 for the position on the texture as the second argument. We use the x and z channels of VERTEX to determine where on the texture to look up.

Since the PlaneMesh coordinates are within the [-1.0, 1.0] range (for a size of 2.0), while the texture coordinates are within [0.0, 1.0], to remap the coordinates we divide by the size of the PlaneMesh by 2.0 and add 0.5 .

texture() returns a vec4 of the r, g, b, a channels at the position. Since the noise texture is grayscale, all of the values are the same, so we can use any one of the channels as the height. In this case we'll use the r, or x channel.

xyzw is the same as rgba in GLSL, so instead of texture().x above, we could use texture().r. See the OpenGL documentation for more details.

Using this code you can see the texture creates random looking hills.

Right now it is too spiky, we want to soften the hills a bit. To do that, we will use a uniform. You already used a uniform above to pass in the noise texture, now let's learn how they work.

Uniform variables allow you to pass data from the game into the shader. They are very useful for controlling shader effects. Uniforms can be almost any datatype that can be used in the shader. To use a uniform, you declare it in your Shader using the keyword uniform.

Let's make a uniform that changes the height of the terrain.

Godot lets you initialize a uniform with a value; here, height_scale is set to 0.5. You can set uniforms from GDScript by calling the function set_shader_parameter() on the material corresponding to the shader. The value passed from GDScript takes precedence over the value used to initialize it in the shader.

Changing uniforms in Spatial-based nodes is different from CanvasItem-based nodes. Here, we set the material inside the PlaneMesh resource. In other mesh resources you may need to first access the material by calling surface_get_material(). While in the MeshInstance3D you would access the material using get_surface_material() or material_override.

Remember that the string passed into set_shader_parameter() must match the name of the uniform variable in the shader. You can use the uniform variable anywhere inside your shader. Here, we will use it to set the height value instead of arbitrarily multiplying by 0.5.

Now it looks much better.

Using uniforms, we can even change the value every frame to animate the height of the terrain. Combined with Tweens, this can be especially useful for animations.

First, turn wireframe off. To do so, open the Perspective menu in the upper-left of the viewport again, and select Display Normal. Additionally in the 3D scene toolbar, turn off preview sunlight.

Note how the mesh color goes flat. This is because the lighting on it is flat. Let's add a light!

First, we will add an OmniLight3D to the scene, and drag it up so it is above the terrain.

You can see the light affecting the terrain, but it looks odd. The problem is the light is affecting the terrain as if it were a flat plane. This is because the light shader uses the normals from the Mesh to calculate light.

The normals are stored in the Mesh, but we are changing the shape of the Mesh in the shader, so the normals are no longer correct. To fix this, we can recalculate the normals in the shader or use a normal texture that corresponds to our noise. Godot makes both easy for us.

You can calculate the new normal manually in the vertex function and then just set NORMAL. With NORMAL set, Godot will do all the difficult lighting calculations for us. We will cover this method in the next part of this tutorial, for now we will read normals from a texture.

Instead we will rely on the NoiseTexture again to calculate normals for us. We do that by passing in a second noise texture.

Set this second uniform texture to another NoiseTexture2D with another FastNoiseLite. But this time, check As Normal Map.

When we have normals that correspond to a specific vertex we set NORMAL, but if you have a normalmap that comes from a texture, set the normal using NORMAL_MAP in the fragment() function. This way Godot will handle wrapping the texture around the mesh automatically.

Lastly, in order to ensure that we are reading from the same places on the noise texture and the normalmap texture, we are going to pass the VERTEX.xz position from the vertex() function to the fragment() function. We do that using a varying.

Above the vertex() define a varying vec2 called tex_position. And inside the vertex() function assign VERTEX.xz to tex_position.

And now we can access tex_position from the fragment() function.

With the normals in place the light now reacts to the height of the mesh dynamically.

We can even drag the light around and the lighting will update automatically.

Here is the full code for this tutorial. You can see it is not very long as Godot handles most of the difficult stuff for you.

That is everything for this part. Hopefully, you now understand the basics of vertex shaders in Godot. In the next part of this tutorial we will write a fragment function to accompany this vertex function and we will cover a more advanced technique to turn this terrain into an ocean of moving waves.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
shader_type spatial;
```

Example 2 (cpp):
```cpp
void vertex() {
  VERTEX.y += cos(VERTEX.x) * sin(VERTEX.z);
}
```

Example 3 (cpp):
```cpp
void vertex() {
  VERTEX.y += cos(VERTEX.x * 4.0) * sin(VERTEX.z * 4.0);
}
```

Example 4 (unknown):
```unknown
uniform sampler2D noise;
```

---

## Introduction to GUI skinning — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/ui/gui_skinning.html

**Contents:**
- Introduction to GUI skinning
- Basics of themes
  - Theme items
  - Theme types
- Customizing a control
- Customizing a project
- Beyond controls
- User-contributed notes

It is essential for a game to provide clear, informative, and yet visually pleasing user interface to its players. While Control nodes come with a decently functional look out of the box, there is always room for uniqueness and case-specific tuning. For this purpose Godot engine includes a system for GUI skinning (or theming), which allows you to customize the look of every control in your user interface, including your custom controls.

Here is an example of this system in action — a game with the GUI that is radically different from the default UI theme of the engine:

A "Gear Up!" screen in Tank Kings, courtesy of Winterpixel Games

Beyond achieving a unique look for your game, this system also enables developers to provide customization options to the end users, including accessibility settings. UI themes are applied in a cascading manner (i.e. they propagate from parent controls to their children), which means that font settings or adjustments for colorblind users can be applied in a single place and affect the entire UI tree. Of course this system can also be used for gameplay purposes: your hero-based game can change its style for the selected player character, or you can give different flavors to the sides in your team-based project.

The skinning system is driven by the Theme resource. Every Godot project has an inherent default theme that contains the settings used by the built-in control nodes. This is what gives the controls their distinct look out of the box. A theme only describes the configuration, however, and it is still the job of each individual control to use that configuration in the way it requires to display itself. This is important to remember when implementing your own custom controls.

Even the Godot editor itself relies on the default theme. But it doesn't look the same as a Godot project, because it applies its own heavily customized theme on top of the default one. In principle, this works exactly like it would in your game as explained below.

The configuration that is stored in a theme consists of theme items. Each item has a unique name and must be one of the following data types:

A color value, which is often used for fonts and backgrounds. Colors can also be used for modulation of controls and icons.

An integer value, which can be used either for numeric properties of controls (such as the item separation in a BoxContainer), or for boolean flags (such as the drawing of relationship lines in a Tree).

A font resource, which is used by controls that display text. Fonts contain most text rendering settings, except for its size and color. On top of that, alignment and text direction are controlled by individual controls.

An integer value, which is used alongside a font to determine the size at which the text should be displayed.

A texture resource, which is normally used to display an icon (on a Button, for example).

A StyleBox resource, a collection of configuration options which define the way a UI panel should be displayed. This is not limited to the Panel control, as styleboxes are used by many controls for their backgrounds and overlays.

Different controls will apply StyleBoxes in a different manner. Most notably, focus styleboxes are drawn as an overlay to other styleboxes (such as normal or pressed) to allow the base stylebox to remain visible. This means the focus stylebox should be designed as an outline or translucent box, so that its background can remain visible.

To help with the organization of its items each theme is separated into types, and each item must belong to a single type. In other words, each theme item is defined by its name, its data type and its theme type. This combination must be unique within the theme. For example, there cannot be two color items named font_color in a type called Label, but there can be another font_color item in a type LineEdit.

The default Godot theme comes with multiple theme types already defined, one for every built-in control node that uses UI skinning. The example above contains actual theme items present in the default theme. You can refer to the Theme Properties section in the class reference for each control to see which items are available to it and its child classes.

Child classes can use theme items defined for their parent class (Button and its derivatives being a good example of that). In fact, every control can use every theme item of any theme type, if it needs to (but for the clarity and predictability we try to avoid that in the engine).

It is important to remember that for child classes that process is automated. Whenever a built-in control requests a theme item from the theme it can omit the theme type, and its class name will be used instead. On top of that, the class names of its parent classes will also be used in turn. This allows changes to the parent class, such as Button, to affect all derived classes without the need to customize every one of them.

You can also define your own theme types, and additionally customize both built-in controls and your own controls. Because built-in controls have no knowledge of your custom theme types, you must utilize scripts to access those items. All control nodes have several methods that allow you to fetch theme items from the theme that is applied to them. Those methods accept the theme type as one of the arguments.

To give more customization opportunities types can also be linked together as type variations. This is another use-case for custom theme types. For example, a theme can contain a type Header which can be marked as a variation of the base Label type. An individual Label control can then be set to use the Header variation for its type, and every time a theme item is requested from a theme this variation will be used before any other type. This allows to store various presets of theme items for the same class of the control node in the single Theme resource.

Only variations available from the default theme or defined in the custom project theme are shown in the Inspector dock as options. You can still input manually the name of a variation that is defined outside of those two places, but it is recommended to keep all variations to the project theme.

You can learn more about creating and using theme type variations in a dedicated article.

Each control node can be customized directly without the use of themes. This is called local overrides. Every theme property from the control's class reference can be overridden directly on the control itself, using either the Inspector dock, or scripts. This allows to make granular changes to a particular part of the UI, while not affecting anything else in the project, including this control's children.

Local overrides are less useful for the visual flair of your user interface, especially if you aim for consistency. However, for layout nodes these are essential. Nodes such as BoxContainer and GridContainer use theme constants for defining separation between their children, and MarginContainer stores its customizable margins in its theme items.

Whenever a control has a local theme item override, this is the value that it uses. Values provided by the theme are ignored.

Out of the box each project adopts the default project theme provided by Godot. The default theme itself is constant and cannot be changed, but its items can be overridden with a custom theme. Custom themes can be applied in two ways: as a project setting, and as a node property throughout the tree of control nodes.

There are two project settings that can be adjusted to affect your entire project: GUI > Theme > Custom allows you to set a custom project-wide theme, and GUI > Theme > Custom Font does the same to the default fallback font. When a theme item is requested by a control node the custom project theme, if present, is checked first. Only if it doesn't have the item the default theme is checked.

This allows you to configure the default look of every Godot control with a single theme resource, but you can go more granular than that. Every control node also has a theme property, which allows you to set a custom theme for the branch of nodes starting with that control. This means that the control and all of its children, and their children in turn, would first check that custom theme resource before falling back on the project and the default themes.

Instead of changing the project setting you can set the custom theme resource to the root-most control node of your entire UI branch to almost the same effect. While in the running project it will behave as expected, individual scenes will still display using the default theme when previewing or running them directly. To fix that you can set the same theme resource to the root control of each individual scene.

For example, you can have a certain style for buttons in your project theme, but want a different look for buttons inside of a popup dialog. You can set a custom theme resource to the root control of your popup and define a different style for buttons within that resource. As long as the chain of control nodes between the root of the popup and the buttons is uninterrupted, those buttons will use the styles defined in the theme resource that is closest to them. All other controls will still be styled using the project-wide theme and the default theme styles.

To sum it up, for an arbitrary control its theme item lookup would look something like this:

Check for local overrides of the same data type and name.

Using control's type variation, class name and parent class names:

Check every control starting from itself and see if it has a theme property set;

If it does, check that theme for the matching item of the same name, data and theme type;

If there is no custom theme or it doesn't have the item, move to the parent control;

Repeat steps a-c. until the root of the tree is reached, or a non-control node is reached.

Using control's type variation, class name and parent class names check the project-wide theme, if it's present.

Using control's type variation, class name and parent class names check the default theme.

Even if the item doesn't exist in any theme, a corresponding default value for that data type will be returned.

Naturally, themes are an ideal type of resource for storing configuration for something visual. While the support for theming is built into control nodes, other nodes can use them as well, just like any other resource.

An example of using themes for something beyond controls can be a modulation of sprites for the same units on different teams in a strategy game. A theme resource can define a collection of colors, and sprites (with a help from scripts) can use those colors to draw the texture. The main benefit being that you could make different themes using the same theme items for red, blue, and green teams, and swap them with a single resource change.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var accent_color = get_theme_color("accent_color", "MyType")
label.add_theme_color_override("font_color", accent_color)
```

Example 2 (unknown):
```unknown
Color accentColor = GetThemeColor("accent_color", "MyType");
label.AddThemeColorOverride("font_color", accentColor);
```

---
