# Plugins

{% embed url="https://www.youtube.com/playlist?list=PL94EgLgEIJyIou6-PzO2vBTvcZQav2Ibq" %}

You can open the Scripts Panel from a button on the [Labs Panel](../using-the-open-brush-tools-quick-tools-and-menu-panels/the-admin-panel/labs-panel.md)

![](<../../.gitbook/assets/image (1) (3).png>)

We won't be using the buttons on the bottom row at the moment. These are related to the older [HTTP API Scripts](../open-brush-api/) which are are useful for controlling Open Brush remotely. However the new plugin scripts are much more powerful and can add new features and modify how Open Brush works interactively.

The other four rows of buttons each relates to a different type of plugin. From the top down they are [Tool Plugins](./#tool-plugins), [Symmetry Plugins](./#symmetry-plugins), [Pointer Plugins](./#pointer-plugin) and [Background Plugins](./#background-plugins).

## Understanding the different plugin types

### Pointer Plugin

These are the simplest type of plugin. They can change how your brush works while you are painting brush strokes. They can't (currently) create new types of brush but they can change the motion, size, color of the stroke. And they can start and end strokes (for example to create dashed lines). They can even add extra strokes as you paint (for example to create a web of lines back to your starting point). Here are some of the included [example Pointer Plugins](example-plugins/example-pointer-plugins.md).

### Symmetry Plugins

Symmetry plugins supercharge the Mirror tool. Instead of simply adding a single extra stroke mirrored horizontally, Symmetry Plugins can create multiple copies of your brush stroke in any arrangement. The strokes can be mirrored, rotated, reflected or even scaled. They can be oriented around the mirror widget - or they can follow your brush like a flock of birds. Each stroke can have a different color, size or even use a different brush type. Here are some of the included [example Symmetry Plugins](example-plugins/example-symmetry-plugins.md).

### Tool Plugins

The previous two types of plugin work in conjunction with the regular Brush Tool and simply change or add to the brush strokes you draw. Tool Plugins are are more powerful and can implement entirely new tools. They might create new objects in one go - or modify existing ones. Each plugin can behave in different ways so check each script's instructions to understand what it does. Here are some of the included [example Tool Plugins](example-plugins/example-tool-plugins.md).

### Background Plugins

The final type of plugin takes the flexibility one step further. Background plugins can do almost anything. They are more complicated to write but they have less restrictions. For a start they run all the time and can listen in to button presses, track controller movement and react accordingly. They can create repeating animations by moving layers around, they can perform actions based on timers or external signals. And you can have multiple Background Plugins active at once (You can only activate one of each of the other plugin types at any one time). Here are some of the included [example Background Plugins](example-plugins/example-background-plugins.md).

## Selecting and Activating a Plugin

For Pointer, Symmetry and Tool plugins, you can only have one of each type active at any one time. The large button on the left of each row activates and deactivates that plugin type.

The left and right arrow buttons cycle through each installed plugin.

The cog button opens up a panel with controls specific to the currently active plugin. These usually have sliders to change various parameters.

The final button will copy the currently selected plugin into your Plugins folder. You can then view the code, modify it or use it as a starting point for writing your own plugin.

Background Plugins have an extra button and work slightly differently in terms of activating and deactivating. The reason for this is that you can have multiple Background Plugins active at once. The large button on the left will enable or disable _all_ currently active Background Plugins. To turn individual plugins on or off you can click the button with the eye icon when that plugin has been selected with the arrow buttons.

## Plugin Parameters

![](<../../.gitbook/assets/image (5) (1).png>)

Plugins can define various parameters so you can easily change how they work without needing to edit the script. Each slider will show a tooltip when you hover over it.

Drag the slider to change it's value. If you need more precision you can:

While hovering you can

* Move the thumbstick on your brush controller left and right to change the value
* Click the small arrows at either end to apply a set increment to the value

When you've finished you can click the tick button at the bottom or simply move your hand away from the panel to close it.

## Discovering New Plugins

Eventually we hope to have an "App Store" for plugins so you can browse and install ones that the community have created. In the meantime you can check our [Plugins Discord channel](https://discord.com/channels/783806589991780412/1054686775504797816) for info on any plugins.

## Installing Plugins

Place plugins inside your Open Brush/Plugins folder. Some plugins might use extra libraries. These should be placed in Plugins/LuaModules
