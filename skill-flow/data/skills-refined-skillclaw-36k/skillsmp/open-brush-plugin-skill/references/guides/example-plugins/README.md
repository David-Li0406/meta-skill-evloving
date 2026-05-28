# Example Plugins

Open Brush (or at least currently the experimental build that supports plugins) ships with a selection of plugins that are both useful in their own right, great examples of what is possible and hopefully good starting points for people that want to write their own plugins.&#x20;

This page will list the included plugins along with a brief explanation of what each one does. It is aimed mainly at users. If you're interested in understanding how each plugin was written, then the source code is hopefully clearly written and contains enough comments to make it easy to follow.

## General Tips

* Try different brushes. Plugins can have wildly different results for some brush types. Try the hull brushes in particular with some of the Tool Plugins. Also try various animated brushes such as Neon Pulse or Keijiro Brush
* You can have more than one plugin type active at once and the combinations can be wild. Try combining a Symmetry Plugin with a Pointer Plugin. Or use a Background Plugin that animates a layer whilst drawing on it with an animated Pointer Plugin. Or maybe all three at once!
* Try spinning the Symmetry Widget with a flick of your hand while drawing. A slow spin gives very different results to a fast spin.
* [Lazy Input](../../../user-guide/lazy-input.md) (the rabbit/tortoise switch on your brush) is especially effective with some plugins. The smooth strokes you can with tortoise mode can combine beautifly with animated Pointer or Symmetry plugins.
* Many of the Symmetry Plugins have additional parameters for color shift. These allow you to create anything from a wild rainbow of different colored strokes, down to subtle shifts of your base color that gives a more natural effect.
* Don't forget to try different parameter values. The same plugin can look massively different based on the settings you choose.
* Use the Copy button to copy the script to your Open Brush folder and then open it up in a text editor (ideally something like VS Code). Try changing some of the values or modifying a line of lua code here or there.
