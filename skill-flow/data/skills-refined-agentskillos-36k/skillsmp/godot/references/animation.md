# Godot - Animation

**Pages:** 12

---

## Animation — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/animation/index.html

**Contents:**
- Animation

This section of the tutorial covers using the two animation nodes in Godot and the animation editor.

See Importing 3D scenes for information on importing animations from a 3D model.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Animation Track types — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/animation/animation_track_types.html

**Contents:**
- Animation Track types
- Property Track
- Position 3D / Rotation 3D / Scale 3D Track
- Blend Shape Track
- Call Method Track
- Bezier Curve Track
- Audio Playback Track
- Animation Playback Track
- User-contributed notes

This page gives an overview of the track types available for Godot's animation player node on top of the default property tracks.

We assume you already read Introduction to the animation features, which covers the basics, including property tracks.

The most basic track type. See Introduction to the animation features.

These 3D transform tracks control the location, rotation, and scale of a 3D object. They make it easier to animate a 3D object's transform compared to using regular property tracks.

It is designed for animations imported from external 3D models and can reduce resource capacity through compression.

A blend shape track is optimized for animating blend shape in MeshInstance3D.

It is designed for animations imported from external 3D models and can reduce resource capacity through compression.

A call method track allow you to call a function at a precise time from within an animation. For example, you can call queue_free() to delete a node at the end of a death animation.

The events placed on the call method track are not executed when the animation is previewed in the editor for safety.

To create such a track in the editor, click "Add Track -> Call Method Track." Then, a window opens and lets you select the node to associate with the track. To call one of the node's methods, right-click the timeline and select "Insert Key". A window opens with a list of available methods. Double-click one to finish creating the keyframe.

To change the method call or its arguments, click on the key and head to the inspector dock. There, you can change the method to call. If you expand the "Args" section, you will see a list of arguments you can edit.

To create such a track through code, pass a dictionary that contains the target method's name and parameters as the Variant for key in Animation.track_insert_key(). The keys and their expected values are as follows:

The name of the method as a String

The arguments to pass to the function as an Array

A bezier curve track is similar to a property track, except it allows you to animate a property's value using a bezier curve.

Bezier curve track and property track cannot be blended in AnimationPlayer and AnimationTree.

To create one, click "Add Track -> Bezier Curve Track". As with property tracks, you need to select a node and a property to animate. To open the bezier curve editor, click the curve icon to the right of the animation track.

In the editor, keys are represented by filled diamonds and the outlined diamonds connected to them by a line control curve's shape.

For better precision while manually working with curves, you might want to alter the zoom levels of the editor. The slider on the bottom right of the editor can be used to zoom in and out on the time axis, you can also do that with Ctrl + Shift + Mouse wheel. Using Ctrl + Alt + Mouse wheel will zoom in and out on the Y axis

While a keyframe is selected (not the handle), in the right click panel of the editor, you can select the handle mode:

Free: Allows you to orient a manipulator in any direction without affecting the other's position.

Linear: Does not allow rotation of the manipulator and draws a linear graph.

Balanced: Makes it so manipulators rotate together, but the distance between the key and a manipulator is not mirrored.

Mirrored: Makes the position of one manipulator perfectly mirror the other, including their distance to the key.

If you want to create an animation with audio, you need to create an audio playback track. To create one, your scene must have either an AudioStreamPlayer, AudioStreamPlayer2D, or AudioStreamPlayer3D node. When creating the track, you must select one of those nodes.

To play a sound in your animation, drag and drop an audio file from the file system dock onto the animation track. You should see the waveform of your audio file in the track.

To remove a sound from the animation, you can right-click it and select "Delete Key(s)" or click on it and press the Del key.

The blend mode allows you to choose whether or not to adjust the audio volume when blending in the AnimationTree.

Animation playback tracks allow you to sequence the animations of other animation player nodes in a scene. For example, you can use it to animate several characters in a cut-scene.

To create an animation playback track, select "New Track -> Animation Playback Track."

Then, select the animation player you want to associate with the track.

To add an animation to the track, right-click on it and insert a key. Select the key you just created to select an animation in the inspector dock.

If an animation is already playing and you want to stop it early, you can create a key and have it set to [STOP] in the inspector.

If you instanced a scene that contains an animation player into your scene, you need to enable "Editable Children" in the scene tree to access its animation player. Also, an animation player cannot reference itself.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
# Create a call method track.
func create_method_animation_track():
    # Get or create the animation the target method will be called from.
    var animation = $AnimationPlayer.get_animation("idle")
    # Get or create the target method's animation track.
    var track_index = animation.add_track(Animation.TYPE_METHOD)
    # Make the arguments for the target method jump().
    var jump_velocity = -400.0
    var multiplier = randf_range(.8, 1.2)
    # Get or create a dictionary with the target method's name and arguments.
    var method_dictionary = {
        "method": "jump",
        "args": [jump_velocity, multiplier],
    }

    # Set scene-tree path to node with target method.
    animation.track_set_path(track_index, ".")
    # Add the dictionary as the animation method track's key.
    animation.track_insert_key(track_index, 0.6, method_dictionary, 0)


# The target method that will be called from the animation.
func jump(jump_velocity, multiplier):
    velocity.y = jump_velocity * multiplier
```

Example 2 (csharp):
```csharp
// Create a call method track.
public void CreateAnimationTrack()
{
    // Get reference to the AnimationPlayer.
    var animationPlayer = GetNode<AnimationPlayer>("AnimationPlayer");
    // Get or create the animation the target method will be called from.
    var animation = animationPlayer.GetAnimation("idle");
    // Get or create the target method's animation track.
    var trackIndex = animation.AddTrack(Animation.TrackType.Method);
    // Make the arguments for the target method Jump().
    var jumpVelocity = -400.0;
    var multiplier = GD.RandRange(.8, 1.2);
    // Get or create a dictionary with the target method's name and arguments.
    var methodDictionary = new Godot.Collections.Dictionary
    {
        { "method", MethodName.Jump },
        { "args", new Godot.Collections.Array { jumpVelocity, multiplier } }
    };

    // Set scene-tree path to node with target method.
    animation.TrackSetPath(trackIndex, ".");
    // Add the dictionary as the animation method track's key.
    animation.TrackInsertKey(trackIndex, 0.6, methodDictionary, 0);
}


// The target method that will be called from the animation.
private void Jump(float jumpVelocity, float multiplier)
{
    Velocity = new Vector2(Velocity.X, jumpVelocity * multiplier);
}
```

---

## 2D skeletons — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html

**Contents:**
- 2D skeletons
- Introduction
- Setup
- Creating the polygons
- Creating the skeleton
- Deforming the polygons
- Internal vertices
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

When working with 3D, skeletal deforms are common for characters and creatures and most 3D modeling applications support it. For 2D, as this function is not used as often, it's difficult to find mainstream software aimed for this.

One option is to create animations in third-party software such as Spine or Dragonbones. This functionality is also supported built-in.

Why would you want to do skeletal animations directly in Godot? The answer is that there are many advantages to it:

Better integration with the engine, so less hassle importing and editing from an external tool.

Ability to control particle systems, shaders, sounds, call scripts, colors, transparency, etc. in animations.

The built-in skeletal system in Godot is very efficient and designed for performance.

The following tutorial will, then, explain 2D skeletal deformations.

Before starting, we recommend you to go through the Cutout animation tutorial to gain a general understanding of animating within Godot.

For this tutorial, we will be using a single image to construct our character. Download it from gBot_pieces.png or save the image below.

It is also advised to download the final character image gBot_complete.png to have a good reference for putting the different pieces together.

Create a new scene for your model (if it's going to be an animated character, you may want to use a CharacterBody2D). For ease of use, an empty 2D node is created as a root for the polygons.

Begin with a Polygon2D node. There is no need to place it anywhere in the scene for now, so simply create it like this:

Select it and assign the texture with the character pieces you have downloaded before:

Drawing a polygon directly is not advised. Instead, open the "UV" dialog for the polygon:

Head over to the Points mode, select the pencil and draw a polygon around the desired piece:

Duplicate the polygon node and give it a proper name. Then, enter the "UV" dialog again and replace the old polygon with another one in the new desired piece.

When you duplicate nodes and the next piece has a similar shape, you can edit the previous polygon instead of drawing a new one.

After moving the polygon, remember to update the UV by selecting Edit > Copy Polygon to UV in the Polygon 2D UV Editor.

Keep doing this until you mapped all pieces.

You will notice that pieces for nodes appear in the same layout as they do in the original texture. This is because by default, when you draw a polygon, the UV and points are the same.

Rearrange the pieces and build the character. This should be pretty quick. There is no need to change pivots, so don't bother making sure rotation pivots for each piece are right; you can leave them be for now.

Ah, the visual order of the pieces is not correct yet, as some are covering wrong pieces. Rearrange the order of the nodes to fix this:

And there you go! It was definitely much easier than in the cutout tutorial.

Create a Skeleton2D node as a child of the root node. This will be the base of our skeleton:

Create a Bone2D node as a child of the skeleton. Put it on the hip (usually skeletons start here). The bone will be pointing to the right, but you can ignore this for now.

Keep creating bones in hierarchy and naming them accordingly.

At the end of this chain, there will be a jaw node. It is, again, very short and pointing to the right. This is normal for bones without children. The length of tip bones can be changed with a property in the inspector:

In this case, we don't need to rotate the bone (coincidentally the jaw points right in the sprite), but in case you need to, feel free to do it. Again, this is only really needed for tip bones as nodes with children don't usually need a length or a specific rotation.

Keep going and build the whole skeleton:

You will notice that all bones raise a warning about a missing rest pose. A rest pose is the default pose for a skeleton, you can come back to it anytime you want (which is very handy for animating). To set one click on the skeleton node in the scene tree, then click on the Skeleton2D button in the toolbar, and select Overwrite Rest Pose from the dropdown menu.

The warnings will go away. If you modify the skeleton (add/remove bones) you will need to set the rest pose again.

Select the previously created polygons and assign the skeleton node to their Skeleton property. This will ensure that they can eventually be deformed by it.

Click the property highlighted above and select the skeleton node:

Again, open the UV editor for the polygon and go to the Bones section.

You will not be able to paint weights yet. For this you need to synchronize the list of bones from the skeleton with the polygon. This step is done only once and manually (unless you modify the skeleton by adding/removing/renaming bones). It ensures that your rigging information is kept in the polygon, even if a skeleton node is accidentally lost or the skeleton modified. Push the "Sync Bones to Polygon" button to sync the list.

The list of bones will automatically appear. By default, your polygon has no weight assigned to any of them. Select the bones you want to assign weight to and paint them:

Points in white have a full weight assigned, while points in black are not influenced by the bone. If the same point is painted white for multiple bones, the influence will be distributed amongst them (so usually there is not that much need to use shades in-between unless you want to polish the bending effect).

After painting the weights, animating the bones (NOT the polygons!) will have the desired effect of modifying and bending the polygons accordingly. As you only need to animate bones in this approach, work becomes much easier!

But it's not all roses. Trying to animate bones that bend the polygon will often yield unexpected results:

This happens because Godot generates internal triangles that connect the points when drawing the polygon. They don't always bend the way you would expect. To solve this, you need to set hints in the geometry to clarify how you expect it to deform.

Open the UV menu for each bone again and go to the Points section. Add some internal vertices in the regions where you expect the geometry to bend:

Now, go to the Polygon section and redraw your own polygons with more detail. Imagine that, as your polygons bend, you need to make sure they deform the least possible, so experiment a bit to find the right setup.

Once you start drawing, the original polygon will disappear and you will be free to create your own:

This amount of detail is usually fine, though you may want to have more fine-grained control over where triangles go. Experiment by yourself until you get the results you like.

Note: Don't forget that your newly added internal vertices also need weight painting! Go to the Bones section again to assign them to the right bones.

Once you are all set, you will get much better results:

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Cutout animation — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/animation/cutout_animation.html

**Contents:**
- Cutout animation
- What is it?
- Cutout animation in Godot
- Making of GBot
- Setting up the rig
- Adjusting the pivot
- RemoteTransform2D node
- Completing the skeleton
- Skeletons
- IK chains

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

Traditionally, cutout animation is a type of stop motion animation in which pieces of paper (or other thin material) are cut into special shapes and arranged in two-dimensional representations of characters and objects. Characters' bodies are usually made out of several pieces. The pieces are arranged and photographed once for each frame of the film. The animator moves and rotates the parts in small increments between each shot to create the illusion of movement when the images are played back quickly in sequence.

Simulations of cutout animation can now be created using software as seen in South Park and Jake and the Never Land Pirates.

In video games, this technique has also become popular. Examples of this are Paper Mario or Rayman Origins .

Godot provides tools for working with cutout rigs, and is ideal for the workflow:

The animation system is fully integrated with the engine: This means animations can control much more than just motion of objects. Textures, sprite sizes, pivots, opacity, color modulation, and more, can all be animated and blended.

Combine animation styles: AnimatedSprite2D allows traditional cel animation to be used alongside cutout animation. In cel animation different animation frames use entirely different drawings rather than the same pieces positioned differently. In an otherwise cutout-based animation, cel animation can be used selectively for complex parts such as hands, feet, changing facial expressions, etc.

Custom Shaped Elements: Custom shapes can be created with Polygon2D allowing UV animation, deformations, etc.

Particle Systems: A cutout animation rig can be combined with particle systems. This can be useful for magic effects, jetpacks, etc.

Custom Colliders: Set colliders and influence areas in different parts of the skeletons, great for bosses and fighting games.

Animation Tree: Allows complex combinations and blending between several animations, the same way it works in 3D.

For this tutorial, we will use as demo content the pieces of the GBot character, created by Andreas Esau.

Get your assets: cutout_animation_assets.zip.

Create an empty Node2D as root of the scene, we will work under it:

The first node of the model is the hip. Generally, both in 2D and 3D, the hip is the root of the skeleton. This makes it easier to animate:

Next will be the torso. The torso needs to be a child of the hip, so create a child sprite and load the torso texture, later accommodate it properly:

This looks good. Let's see if our hierarchy works as a skeleton by rotating the torso. We can do this be pressing E to enter rotate mode, and dragging with the left mouse button. To exit rotate mode hit ESC.

The rotation pivot is wrong and needs to be adjusted.

This small cross in the middle of the Sprite2D is the rotation pivot:

The pivot can be adjusted by changing the offset property in the Sprite2D:

The pivot can also be adjusted visually. While hovering over the desired pivot point, press V to move the pivot there for the selected Sprite2D. There is also a tool in the tool bar that has a similar function.

Continue adding body pieces, starting with the right arm. Make sure to put each sprite in its correct place in the hierarchy, so its rotations and translations are relative to its parent:

With the left arm there's a problem. In 2D, child nodes appear in front of their parents:

We want the left arm to appear behind the hip and the torso. We could move the left arm nodes behind the hip (above the hip node in the scene hierarchy), but then the left arm is no longer in its proper place in the hierarchy. This means it wouldn't be affected by the movement of the torso. We'll fix this problem with RemoteTransform2D nodes.

You can also fix depth ordering problems by adjusting the Z property of any node inheriting from Node2D.

The RemoteTransform2D node transforms nodes somewhere else in the hierarchy. This node applies its own transform (including any transformation it inherits from its parents) to the remote node it targets.

This allows us to correct the visibility order of our elements, independently of the locations of those parts in the cutout hierarchy.

Create a RemoteTransform2D node as a child of the torso. Call it remote_arm_l. Create another RemoteTransform2D node inside the first and call it remote_hand_l. Use the Remote Path property of the two new nodes to target the arm_l and hand_l sprites respectively:

Moving the RemoteTransform2D nodes now moves the sprites. So we can create animations by adjusting the RemoteTransform2D transforms:

Complete the skeleton by following the same steps for the rest of the parts. The resulting scene should look similar to this:

The resulting rig will be easy to animate. By selecting the nodes and rotating them you can animate forward kinematics (FK) efficiently.

For simple objects and rigs this is fine, but there are limitations:

Selecting sprites in the main viewport can become difficult in complex rigs. The scene tree ends up being used to select parts instead, which can be slower.

Inverse Kinematics (IK) is useful for animating extremities like hands and feet, and can't be used with our rig in its current state.

To solve these problems we'll use Godot's skeletons.

In Godot there is a helper to create "bones" between nodes. The bone-linked nodes are called skeletons.

As an example, let's turn the right arm into a skeleton. To create a skeleton, a chain of nodes must be selected from top to bottom:

Then, click on the Skeleton menu and select Make Bones.

This will add bones covering the arm, but the result may be surprising.

Why does the hand lack a bone? In Godot, a bone connects a node with its parent. And there's currently no child of the hand node. With this knowledge let's try again.

The first step is creating an endpoint node. Any kind of node will do, but Marker2D is preferred because it's visible in the editor. The endpoint node will ensure that the last bone has orientation.

Now select the whole chain, from the endpoint to the arm and create bones:

The result resembles a skeleton a lot more, and now the arm and forearm can be selected and animated.

Create endpoints for all important extremities. Generate bones for all articulable parts of the cutout, with the hip as the ultimate connection between all of them.

You may notice that an extra bone is created when connecting the hip and torso. Godot has connected the hip node to the scene root with a bone, and we don't want that. To fix this, select the root and hip node, open the Skeleton menu, click clear bones.

Your final skeleton should look something like this:

You might have noticed a second set of endpoints in the hands. This will make sense soon.

Now that the whole figure is rigged, the next step is setting up the IK chains. IK chains allow for more natural control of extremities.

IK stands for inverse kinematics. It's a convenient technique for animating the position of hands, feet and other extremities of rigs like the one we've made. Imagine you want to pose a character's foot in a specific position on the ground. Without IK chains, each motion of the foot would require rotating and positioning several other bones (the shin and the thigh at least). This would be quite complex and lead to imprecise results. IK allows us to move the foot directly while the shin and thigh self-adjust.

IK chains in Godot currently work in the editor only, not at runtime. They are intended to ease the process of setting keyframes, and are not currently useful for techniques like procedural animation.

To create an IK chain, select a chain of bones from endpoint to the base for the chain. For example, to create an IK chain for the right leg, select the following:

Then enable this chain for IK. Go to Edit > Make IK Chain.

As a result, the base of the chain will turn Yellow.

Once the IK chain is set up, grab any child or grand-child of the base of the chain (e.g. a foot), and move it. You'll see the rest of the chain adjust as you adjust its position.

The following section will be a collection of tips for creating animation for your cutout rigs. For more information on how the animation system in Godot works, see Introduction to the animation features.

Special contextual elements appear in the top toolbar when the animation editor window is open:

The key button inserts location, rotation, and scale keyframes for the selected objects or bones at the current playhead position.

The "loc", "rot", and "scl" toggle buttons to the left of the key button modify its function, allowing you to specify which of the three properties keyframes will be created for.

Here's an illustration of how this can be useful: Imagine you have a node which already has two keyframes animating its scale only. You want to add an overlapping rotation movement to the same node. The rotation movement should begin and end at different times from the scale change that's already set up. You can use the toggle buttons to have only rotation information added when you add a new keyframe. This way, you can avoid adding unwanted scale keyframes which would disrupt the existing scale animation.

Think of a rest pose as a default pose that your cutout rig should be set to when no other pose is active in your game. Create a rest pose as follows:

1. Make sure the rig parts are positioned in what looks like a "resting" arrangement.

Create a new animation, rename it "rest".

Select all nodes in your rig (box selection should work fine).

4. Make sure the "loc", "rot", and "scl" toggle buttons are all active in the toolbar.

5. Press the key button. Keys will be inserted for all selected parts storing their current arrangement. This pose can now be recalled when necessary in your game by playing the "rest" animation you've created.

When animating a cutout rig, often it's only the rotation of the nodes that needs to change. Location and scale are rarely used.

So when inserting keys, you might find it convenient to have only the "rot" toggle active most of the time:

This will avoid the creation of unwanted animation tracks for position and scale.

When editing IK chains, it's not necessary to select the whole chain to add keyframes. Selecting the endpoint of the chain and inserting a keyframe will automatically insert keyframes for all other parts of the chain too.

Sometimes it is necessary to have a node change its visual depth relative to its parent node during an animation. Think of a character facing the camera, who pulls something out from behind his back and holds it out in front of him. During this animation the whole arm and the object in his hand would need to change their visual depth relative to the body of the character.

To help with this there's a keyframable "Behind Parent" property on all Node2D-inheriting nodes. When planning your rig, think about the movements it will need to perform and give some thought to how you'll use "Behind Parent" and/or RemoteTransform2D nodes. They provide overlapping functionality.

To apply the same easing curve to multiple keyframes at once:

Select the relevant keys.

Click on the pencil icon in the bottom right of the animation panel. This will open the transition editor.

In the transition editor, click on the desired curve to apply it.

Skeletal deform can be used to augment a cutout rig, allowing single pieces to deform organically (e.g. antennae that wobble as an insect character walks).

This process is described in a separate tutorial.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Creating movies — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html

**Contents:**
- Creating movies
- Enabling Movie Maker mode
  - Command line usage
- Choosing an output format
  - OGV (recommended)
  - AVI
  - PNG
  - Custom
- Configuration
- Quitting Movie Maker mode

Godot can record non-real-time video and audio from any 2D or 3D project. This kind of recording is also called offline rendering. There are many scenarios where this is useful:

Recording game trailers for promotional use.

Recording cutscenes that will be displayed as pre-recorded videos in the final game. This allows for using higher quality settings (at the cost of file size), regardless of the player's hardware.

Recording procedurally generated animations or motion design. User interaction remains possible during video recording, and audio can be included as well (although you won't be able to hear it while the video is recording).

Comparing the visual output of graphics settings, shaders, or rendering techniques in an animated scene.

With Godot's animation features such as the AnimationPlayer node, Tweeners, particles and shaders, it can effectively be used to create any kind of 2D and 3D animations (and still images).

If you are already used to Godot's workflow, you may find yourself more productive by using Godot for video rendering compared to Blender. That said, renderers designed for non-real-time usage such as Cycles and Eevee can result in better visuals (at the cost of longer rendering times).

Compared to real-time video recording, some advantages of non-real-time recording include:

Use any graphics settings (including extremely demanding settings) regardless of your hardware's capabilities. The output video will always have perfect frame pacing; it will never exhibit dropped frames or stuttering. Faster hardware will allow you to render a given animation in less time, but the visual output remains identical.

Render at a higher resolution than the screen resolution, without having to rely on driver-specific tools such as NVIDIA's Dynamic Super Resolution or AMD's Virtual Super Resolution.

Render at a higher framerate than the video's target framerate, then post-process to generate high-quality motion blur. This also makes effects that converge over several frames (such as temporal antialiasing, SDFGI and volumetric fog) look better.

This feature is not designed for capturing real-time footage during gameplay.

Players should use something like OBS Studio or SimpleScreenRecorder to record gameplay videos, as they do a much better job at intercepting the compositor than Godot can do using Vulkan or OpenGL natively.

That said, if your game runs at near-real-time speeds when capturing, you can still use this feature (but it will lack audible sound playback, as sound is saved directly to the video file).

To enable Movie Maker mode, click the "movie reel" button in the top-right corner of the editor before running the project:

Movie Maker mode is disabled, click the "movie reel" icon to enable

A menu will be displayed with options to enable Movie Maker mode and to go to the settings. The icon gets a background matching the accent color when Movie Maker mode is enabled:

Movie Maker mode is enabled, click the "movie reel" icon again to disable

Movie Maker status is not persisted when the editor quits, so you must re-enable Movie Maker mode again after restarting the editor if needed.

Toggling Movie Maker mode while running the project will not have any effect until the project is restarted.

Before you can record video by running the project, you still need to configure the output file path. This path can be set for all scenes in the Project Settings:

Movie Maker project settings (with Advanced toggle enabled)

Alternatively, you can set the output file path on a per-scene basis by adding a String metadata with the name movie_file to the scene's root node. This is only used when the main scene is set to the scene in question, or when running the scene directly by pressing F6 (Cmd + R on macOS).

Inspector view after creating a movie_file metadata of type String

The path specified in the project settings or metadata can be either absolute, or relative to the project root.

Once you've configured and enabled Movie Maker mode, it will be automatically used when running the project from the editor.

Movie Maker can also be enabled from the command line:

If the output path is relative, then it is relative to the project folder, not the current working directory. In the above example, the file will be written to /path/to/your_project/output.avi. This behavior is similar to the --export-release command line argument.

Since Movie Maker's output resolution is set by the viewport size, you can adjust the window size on startup to override it if the project uses the disabled or canvas_items stretch mode:

Note that the window size is clamped by your display's resolution. See Rendering at a higher resolution than the screen resolution if you need to record a video at a higher resolution than the screen resolution.

The recording FPS can also be overridden on the command line, without having to edit the Project Settings:

The --write-movie and --fixed-fps command line arguments are both available in exported projects. Movie Maker mode cannot be toggled while the project is running, but you can use the OS.execute() method to run a second instance of the exported project that will record a video file.

Output formats are provided by the MovieWriter class. Godot has 3 built-in MovieWriters, and more can be implemented by extensions:

OGV container with Theora for video and Vorbis for audio. Features lossy video and audio compression with a good balance of file size and encoding speed, with a better image quality than MJPEG. It has 4 speed levels that can be adjusted by changing Editor > Movie Writer > Encoding Speed with the fastest one being around as fast as AVI with better compression. At slower speed levels, it can compress even better while keeping the same image quality. The lossy compression quality can be adjusted by changing Editor > Movie Writer > Video Quality for video and Editor > Movie Writer > Audio Quality for audio.

The Keyframe Interval can be adjusted by changing Editor > Movie Writer > Keyframe Interval. In some cases, increasing this setting can improve compression efficiency without downsides.

The resulting file can be viewed in Godot with VideoStreamPlayer and most video players but not web browsers. OGV does not support transparency.

To use OGV, specify a path to a .ogv file to be created in the Editor > Movie Writer > Movie File project setting.

OGV can only be recorded in editor builds. On the other hand, OGV playback is possible in both editor and export template builds.

AVI container with MJPEG for video and uncompressed audio. Features lossy video compression, resulting in medium file sizes and fast encoding. The lossy compression quality can be adjusted by changing Editor > Movie Writer > Video Quality.

The resulting file can be viewed in most video players, but it must be converted to another format for viewing on the web or by Godot with the VideoStreamPlayer node. MJPEG does not support transparency. AVI output is currently limited to a file of 4 GB in size at most.

To use AVI, specify a path to a .avi file to be created in the Editor > Movie Writer > Movie File project setting.

PNG image sequence for video and WAV for audio. Features lossless video compression, at the cost of large file sizes and slow encoding. This is designed to be encoded to a video file with an external tool after recording.

Transparency is supported, but the root viewport must have its transparent_bg property set to true for transparency to be visible on the output image. This can be achieved by enabling the Rendering > Transparent Background advanced project setting. Display > Window > Size > Transparent and Display > Window > Per Pixel Transparency > Enabled can optionally be enabled to allow transparency to be previewed while recording the video, but they do not have to be enabled for the output image to contain transparency.

To use PNG, specify a .png file to be created in the Editor > Movie Writer > Movie File project setting. The generated .wav file will have the same name as the .png file (minus the extension).

If you need to encode directly to a different format or pipe a stream through third-party software, you can extend the MovieWriter class to create your own movie writers. This should typically be done using GDExtension for performance reasons.

In the Editor > Movie Writer section of the Project Settings, there are several options you can configure. Some of them are only visible after enabling the Advanced toggle in the top-right corner of the Project Settings dialog.

Mix Rate Hz: The audio mix rate to use in the recorded audio when writing a movie. This can be different from the project's mix rate, but this value must be divisible by the recorded FPS to prevent audio from desynchronizing over time.

Speaker Mode: The speaker mode to use in the recorded audio when writing a movie (stereo, 5.1 surround or 7.1 surround).

Video Quality: The image quality to use when writing a video to an OGV or AVI file, between 0.01 and 1.0 (inclusive). Higher quality values result in better-looking output at the cost of larger file sizes. Recommended quality values are between 0.75 and 0.9. Even at quality 1.0, compression remains lossy. This setting does not affect audio quality and is ignored when writing to a PNG image sequence.

Movie File: The output path for the movie. This can be absolute or relative to the project root.

Disable V-Sync: If enabled, requests V-Sync to be disabled when writing a movie. This can speed up video writing if the hardware is fast enough to render, encode and save the video at a framerate higher than the monitor's refresh rate. This setting has no effect if the operating system or graphics driver forces V-Sync with no way for applications to disable it.

FPS: The rendered frames per second in the output movie. Higher values result in smoother animation, at the cost of longer rendering times and larger output file sizes. Most video hosting platforms do not support FPS values higher than 60, but you can use a higher value and use that to generate motion blur.

Audio Quality: The audio quality to use when writing a video to an OGV file, between -0.1 and 1.0 (inclusive). Higher quality values result in better audio quality at the cost of very slightly larger file sizes. Recommended quality values are between 0.3 and 0.5. Even at quality 1.0, compression remains lossy.

Encoding Speed: The speed level to use when writing a video to an OGV file. Faster speed levels have less compression efficiency. The image quality stays barely the same.

Keyframe Interval: Also known as GOP (Group Of Pictures), the maximum number of inter-frames to use when writing to an OGV file. Higher values can improve compression efficiency without quality loss but at the cost of slower video seeks.

When using the disabled or 2d stretch modes, the output file's resolution is set by the window size. Make sure to resize the window before the splash screen has ended. For this purpose, it's recommended to adjust the Display > Window > Size > Window Width Override and Window Height Override advanced project settings.

See also Rendering at a higher resolution than the screen resolution.

To safely quit a project that is using Movie Maker mode, use the X button at the top of the window, or call get_tree().quit() in a script. You can also use the --quit-after N command line argument where N is the number of frames to render before quitting.

Pressing F8 (Cmd + . on macOS) or pressing Ctrl + C on the terminal running Godot is not recommended, as it will result in an improperly formatted AVI file with no duration information. For PNG image sequences, PNG images will not be negatively altered, but the associated WAV file will still lack duration information. OGV files might end up with slightly different duration video and audio tracks but still valid.

Some video players may still be able to play the AVI or WAV file with working video and audio. However, software that makes use of the AVI or WAV file such as video editors may not be able to open the file. Using a video converter program can help in those cases.

If you're using an AnimationPlayer to control a "main action" in the scene (such as camera movement), you can enable the Movie Quit On Finish property on the AnimationPlayer node in question. When enabled, this property will make Godot quit on its own when an animation is done playing and the engine is running in Movie Maker mode. Note that this property has no effect on looping animations. Therefore, you need to make sure that the animation is set as non-looping.

The movie feature tag can be used to override specific project settings. This is useful to enable high-quality graphics settings that wouldn't be fast enough to run in real-time speeds on your hardware. Remember that putting every setting to its maximum value can still slow down movie saving speed, especially when recording at higher resolutions. Therefore, it's still recommended to only increase graphics settings if they make a meaningful difference in the output image.

This feature tag can also be queried in a script to increase quality settings that are set in the Environment resource. For example, to further improve SDFGI detail and reduce light leaking:

The overall rendering quality can be improved significantly by rendering at high resolutions such as 4K or 8K.

For 3D rendering, Godot provides a Rendering > Scaling 3D > Scale advanced project setting, which can be set above 1.0 to obtain supersample antialiasing. The 3D rendering is then downsampled when it's drawn on the viewport. This provides an expensive but high-quality form of antialiasing, without increasing the final output resolution.

Consider using this project setting first, as it avoids slowing down movie writing speeds and increasing output file size compared to actually increasing the output resolution.

If you wish to render 2D at a higher resolution, or if you actually need the higher raw pixel output for 3D rendering, you can increase the resolution above what the screen allows.

By default, Godot uses the disabled stretch modes in projects. If using disabled or canvas_items stretch mode, the window size dictates the output video resolution.

On the other hand, if the project is configured to use the viewport stretch mode, the viewport resolution dictates the output video resolution. The viewport resolution is set using the Display > Window > Size > Viewport Width and Viewport Height project settings. This can be used to render a video at a higher resolution than the screen resolution.

To make the window smaller during recording without affecting the output video resolution, you can set the Display > Window > Size > Window Width Override and Window Height Override advanced project settings to values greater than 0.

To apply a resolution override only when recording a movie, you can override those settings with the movie feature tag.

Some common post-processing steps are listed below.

When using several post-processing steps, try to perform all of them in a single FFmpeg command. This will save encoding time and improve quality by avoiding multiple lossy encoding steps.

While some platforms such as YouTube support uploading the AVI file directly, many others will require a conversion step beforehand. HandBrake (GUI) and FFmpeg (CLI) are popular open source tools for this purpose. FFmpeg has a steeper learning curve, but it's more powerful.

The command below converts an OGV/AVI video to an MP4 (H.264) video with a Constant Rate Factor (CRF) of 15. This results in a relatively large file, but is well-suited for platforms that will re-encode your videos to reduce their size (such as most video sharing websites):

To get a smaller file at the cost of quality, increase the CRF value in the above command.

To get a file with a better size/quality ratio (at the cost of slower encoding times), add -preset veryslow before -crf 15 in the above command. On the contrary, -preset veryfast can be used to achieve faster encoding at the cost of a worse size/quality ratio.

If you chose to record a PNG image sequence with a WAV file beside it, you need to convert it to a video before you can use it elsewhere.

The filename for the PNG image sequence generated by Godot always contains 8 digits, starting at 0 with zero-padded numbers. If you specify an output path folder/example.png, Godot will write folder/example00000000.png, folder/example00000001.png, and so on in that folder. The audio will be saved at folder/example.wav.

The FPS is specified using the -r argument. It should match the FPS specified during recording. Otherwise, the video will appear to be slowed down or sped up, and audio will be out of sync with the video.

If you recorded a PNG image sequence with transparency enabled, you need to use a video format that supports storing transparency. MP4/H.264 doesn't support storing transparency, so you can use WebM/VP9 as an alternative:

You can trim parts of the video you don't want to keep after the video is recorded. For example, to discard everything before 12.1 seconds and keep only 5.2 seconds of video after that point:

Cutting videos can also be done with the GUI tool LosslessCut.

The following command resizes a video to be 1080 pixels tall (1080p), while preserving its existing aspect ratio:

The following command changes a video's framerate to 30 FPS, dropping some of the original frames if there are more in the input video:

Godot does not have built-in support for motion blur, but it can still be created in recorded videos.

If you record the video at a multiple of the original framerate, you can blend the frames together then reduce the frameate to produce a video with accumulation motion blur. This motion blur can look very good, but it can take a long time to generate since you have to render many more frames per second (on top of the time spent on post-processing).

Example with a 240 FPS source video, generating 4× motion blur and decreasing its output framerate to 60 FPS:

This also makes effects that converge over several frames (such as temporal antialiasing, SDFGI and volumetric fog) converge faster and therefore look better, since they'll be able to work with more data at a given time. See Reducing framerate if you want to get this benefit without adding motion blur.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
godot --path /path/to/your_project --write-movie output.avi
```

Example 2 (unknown):
```unknown
godot --path /path/to/your_project --write-movie output.avi --resolution 1280x720
```

Example 3 (unknown):
```unknown
godot --path /path/to/your_project --write-movie output.avi --fixed-fps 30
```

Example 4 (gdscript):
```gdscript
extends Node3D

func _ready():
    if OS.has_feature("movie"):
        # When recording a movie, improve SDFGI cell density
        # without decreasing its maximum distance.
        get_viewport().world_3d.environment.sdfgi_min_cell_size *= 0.25
        get_viewport().world_3d.environment.sdfgi_cascades = 8
```

---

## Using AnimationTree — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html

**Contents:**
- Using AnimationTree
- Introduction
- AnimationTree and AnimationPlayer
- Creating a tree
- Blend tree
  - Blend2 / Blend3
  - OneShot
  - TimeSeek
  - TimeScale
  - Transition

With AnimationPlayer, Godot has one of the most flexible animation systems that you can find in any game engine. It is pretty much unique in its ability to animate almost any property in any node or resource, and its dedicated transform, bezier, function calling, audio, and sub-animation tracks.

However, the support for blending those animations via AnimationPlayer is limited, as you can only set a fixed cross-fade transition time.

AnimationTree is a new node introduced in Godot 3.1 to deal with advanced transitions. It replaces the ancient AnimationTreePlayer, while adding a huge amount of features and flexibility.

Before starting, know that an AnimationTree node does not contain its own animations. Instead, it uses animations contained in an AnimationPlayer node. You create, edit, or import your animations in an AnimationPlayer and then use an AnimationTree to control the playback.

AnimationPlayer and AnimationTree can be used in both 2D and 3D scenes. When importing 3D scenes and their animations, you can use name suffixes to simplify the process and import with the correct properties. At the end, the imported Godot scene will contain the animations in an AnimationPlayer node. Since you rarely use imported scenes directly in Godot (they are either instantiated or inherited from), you can place the AnimationTree node in your new scene which contains the imported one. Afterwards, point the AnimationTree node to the AnimationPlayer that was created in the imported scene.

This is how it's done in the Third Person Shooter demo, for reference:

A new scene was created for the player with a CharacterBody3D as root. Inside this scene, the original .dae (Collada) file was instantiated and an AnimationTree node was created.

To use an AnimationTree, you have to set a root node. An animation root node is a class that contains and evaluates sub-nodes and outputs an animation. There are 3 types of sub-nodes:

Animation nodes, which reference an animation from the linked AnimationPlayer.

Animation Root nodes, which are used to blend sub-nodes and can be nested.

Animation Blend nodes, which are used in an AnimationNodeBlendTree, a 2D graph of nodes. Blend nodes take multiple input ports and give one output port.

A few types of root nodes are available:

AnimationNodeAnimation: Selects an animation from the list and plays it. This is the simplest root node, and generally not used as a root.

AnimationNodeBlendTree: Contains multiple nodes as children in a graph. Many blend nodes are available, such as mix, blend2, blend3, one shot, etc.

AnimationNodeBlendSpace1D: Allows linear blending between two animation nodes. Control the blend position in a 1D blend space to mix between animations.

AnimationNodeBlendSpace2D: Allows linear blending between three animation nodes. Control the blend position in a 2D blend space to mix between animations.

AnimationNodeStateMachine: Contains multiple nodes as children in a graph. Each node is used as a state, with multiple functions used to alternate between states.

When you make an AnimationNodeBlendTree, you get an empty 2d graph in the bottom panel, under the AnimationTree tab. It contains only an Output node by default.

In order for animations to play, a node has to be connected to the output. You can add nodes from the Add Node.. menu or by right clicking an empty space:

The simplest connection to make is to connect an Animation node to the output directly, which will just play back the animation.

Following is a description of the other available nodes:

These nodes will blend between two or three inputs by a user-specified blend value:

Blending can use filters to control individually which tracks get blended and which do not. This can be useful for layering animations on top of each other.

For more complex blending, it is recommended to use blend spaces instead.

This node will execute an animation once and return when it finishes. You can customize blend times for fading in and out, as well as filters.

This node allows you to seek to a time in the animation connected to its in input. Use this node to play an Animation starting from a certain playback position. Note that the seek request value is measured in seconds, so if you would like to play an animation from the beginning, set the value to 0.0, or if you would like to play an animation from 3 seconds in, set the value to 3.0.

This node allows you to scale the speed of the animation connected to its in input. The speed of the animation will be multiplied by the number in the scale parameter. Setting the scale to 0 will pause the animation. Setting the scale to a negative number will play the animation backwards.

This node is a simplified version of a StateMachine. You connect animations to the inputs, and the current state index determines which animation to play. You may specify a crossfade transition time. In the Inspector, you may change the number of input ports, rearrange inputs, or delete inputs.

When you make an AnimationNodeStateMachine, you get an empty 2d graph in the bottom panel, under the AnimationTree tab. It contains a Start and End state by default.

To add states, right click or use the create new nodes button, whose icon is a plus in a box. You can add animations, blendspaces, blendtrees, or even another StateMachine. To edit one of these more complex sub-nodes, click on the pencil icon on the right of the state. To return to the original StateMachine, click Root on the top left of the panel.

Before the StateMachine can do anything useful, the states must be connected with transitions. To add a transition, click the connect nodes button, which is a line with a right-facing arrow, and drag between two states. You can create 2 transitions between states, one going in each direction.

There are 3 types of transitions:

Immediate: Will switch to the next state immediately.

Sync: Will switch to the next state immediately, but will seek the new state to the playback position of the old state.

At End: Will wait for the current state playback to end, then switch to the beginning of the next state animation.

Transitions also have a few properties. Click a transition and it will be displayed in the inspector:

Xfade Time is the time to cross-fade between this state and the next.

Xfade Curve is a cross-fade following a curve rather than a linear blend.

Reset determines whether the state you are switching into plays from the beginning (true) or not (false).

Priority is used together with the travel() function from code (more on this later). Lower priority transitions are preferred when travelling through the tree.

Switch Mode is the transition type (see above). It can be changed after creation here.

Advance Mode determines the advance mode. If Disabled, the transition will not be used. If Enabled, the transition will only be used during travel(). If Auto, the transition will be used if the advance condition and expression are true, or if there are no advance conditions/expressions.

The last 2 properties in a StateMachine transition are Advance Condition and Advance Expression. When the Advance Mode is set to Auto, these determine if the transition will advance or not.

Advance Condition is a true/false check. You may put a custom variable name in the text field, and when the StateMachine reaches this transition, it will check if your variable is true. If so, the transition continues. Note that the advance condition only checks if a variable is true, and it cannot check for falseness.

This gives the Advance Condition a very limited capability. If you wanted to make a transition back and forth based on one property, you would need to make 2 variables that have opposite values, and check if either of them are true. This is why, in Godot 4, the Advance Expression was added.

The Advance Expression works similar to the Advance Condition, but instead of checking if one variable is true, it evaluates any expression. An expression is anything you could put in an if statement. These are all examples of expressions that would work in the Advance Expression:

is_walking && !is_idle

Here is an example of an improperly-set-up StateMachine transition using Advance Condition:

This is not working because there is a ! variable in the Advance Condition, which cannot be checked.

Here is the same example, set up properly, using two opposite variables:

Here is the same example, but using Advance Expression rather than Advance Condition, which eliminates the need for two variables:

In order to use Advance Expressions, the Advance Expression Base Node has to be set from the Inspector of the AnimationTree node. By default, it is set to the AnimationTree node itself, but it needs to point to whatever node contains the script with your animation variables.

One of the nice features in Godot's StateMachine implementation is the ability to travel. You can instruct the graph to go from the current state to another one, while visiting all the intermediate ones. This is done via the A* algorithm. If there is no path of transitions starting at the current state and finishing at the destination state, the graph teleports to the destination state.

To use the travel ability, you should first retrieve the AnimationNodeStateMachinePlayback object from the AnimationTree node (it is exported as a property), and then call one of its many functions:

The StateMachine must be running before you can travel. Make sure to either call start() or connect a node to Start.

BlendSpace2D is a node to do advanced blending in two dimensions. Points representing animations are added to a 2D space and then a position between them is controlled to determine the blending:

You may place these points anywhere on the graph by right clicking or using the add point button, whose icon is a pen and point. Wherever you place the points, the triangle between them will be generated automatically using Delaunay. You may also control and label the ranges in X and Y.

Finally, you may also change the blend mode. By default, blending happens by interpolating points inside the closest triangle. When dealing with 2D animations (frame by frame), you may want to switch to Discrete mode. Alternatively, if you want to keep the current play position when switching between discrete animations, there is a Carry mode. This mode can be changed in the Blend menu:

BlendSpace1D works just like BlendSpace2D, but in one dimension (a line). Triangles are not used.

In Godot 4.0+, in order for the blending results to be deterministic (reproducible and always consistent), the blended property values must have a specific initial value. For example, in the case of two animations to be blended, if one animation has a property track and the other does not, the blended animation is calculated as if the latter animation had a property track with the initial value.

When using Position/Rotation/Scale 3D tracks for Skeleton3D bones, the initial value is Bone Rest. For other properties, the initial value is 0 and if the track is present in the RESET animation, the value of its first keyframe is used instead.

For example, the following AnimationPlayer has two animations, but one of them lacks a Property track for Position.

This means that the animation lacking that will treat those Positions as Vector2(0, 0).

This problem can be solved by adding a Property track for Position as an initial value to the RESET animation.

Be aware that the RESET animation exists to define the default pose when loading an object originally. It is assumed to have only one frame and is not expected to be played back using the timeline.

Also keep in mind that the Rotation 3D tracks and the Property tracks for 2D rotation with Interpolation Type set to Linear Angle or Cubic Angle will prevent rotations greater than 180 degrees from the initial value as blended animation.

This can be useful for Skeleton3Ds to prevent the bones penetrating the body when blending animations. Therefore, Skeleton3D's Bone Rest values should be as close to the midpoint of the movable range as possible. This means that for humanoid models, it is preferable to import them in a T-pose.

You can see that the shortest rotation path from Bone Rests is prioritized rather than the shortest rotation path between animations.

If you need to rotate Skeleton3D itself more than 180 degrees by blend animations for movement, you can use Root Motion.

When working with 3D animations, a popular technique is for animators to use the root skeleton bone to give motion to the rest of the skeleton. This allows animating characters in a way where steps actually match the floor below. It also allows precise interaction with objects during cinematics.

When playing back the animation in Godot, it is possible to select this bone as the root motion track. Doing so will cancel the bone transformation visually (the animation will stay in place).

Afterwards, the actual motion can be retrieved via the AnimationTree API as a transform:

This can be fed to functions such as CharacterBody3D.move_and_slide to control the character movement.

There is also a tool node, RootMotionView, you can place a scene that will act as a custom floor for your character and animations (this node is disabled by default during the game).

After building the tree and previewing it, the only question remaining is "How is all this controlled from code?".

Keep in mind that the animation nodes are just resources, so they are shared between all instances using them. Setting values in the nodes directly will affect all instances of the scene that uses this AnimationTree. This is generally undesirable, but does have some cool use cases, e.g. you can copy and paste parts of your animation tree, or reuse nodes with a complex layout (such as a StateMachine or blend space) in different animation trees.

The actual animation data is contained in the AnimationTree node and is accessed via properties. Check the "Parameters" section of the AnimationTree node to see all the parameters that can be modified in real-time:

This is handy because it makes it possible to animate them from an AnimationPlayer, or even the AnimationTree itself, allowing very complex animation logic.

To modify these values from code, you must obtain the property path. You can find them by hovering your mouse over any of the parameters:

Then you can set or read them:

Advance Expressions from a StateMachine will not be found under the parameters. This is because they are held in another script rather than the AnimationTree itself. Advance Conditions will be found under parameters.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (markdown):
```markdown
# Play child animation connected to "shot" port.
animation_tree.set("parameters/OneShot/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)
# Alternative syntax (same result).
animation_tree["parameters/OneShot/request"] = AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE

# Abort child animation connected to "shot" port.
animation_tree.set("parameters/OneShot/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_ABORT)
# Alternative syntax (same result).
animation_tree["parameters/OneShot/request"] = AnimationNodeOneShot.ONE_SHOT_REQUEST_ABORT

# Get current state (read-only).
animation_tree.get("parameters/OneShot/active"))
# Alternative syntax (same result).
animation_tree["parameters/OneShot/active"]
```

Example 2 (unknown):
```unknown
// Play child animation connected to "shot" port.
animationTree.Set("parameters/OneShot/request", (int)AnimationNodeOneShot.OneShotRequest.Fire);

// Abort child animation connected to "shot" port.
animationTree.Set("parameters/OneShot/request", (int)AnimationNodeOneShot.OneShotRequest.Abort);

// Get current state (read-only).
animationTree.Get("parameters/OneShot/active");
```

Example 3 (sql):
```sql
# Play child animation from the start.
animation_tree.set("parameters/TimeSeek/seek_request", 0.0)
# Alternative syntax (same result).
animation_tree["parameters/TimeSeek/seek_request"] = 0.0

# Play child animation from 12 second timestamp.
animation_tree.set("parameters/TimeSeek/seek_request", 12.0)
# Alternative syntax (same result).
animation_tree["parameters/TimeSeek/seek_request"] = 12.0
```

Example 4 (sql):
```sql
// Play child animation from the start.
animationTree.Set("parameters/TimeSeek/seek_request", 0.0);

// Play child animation from 12 second timestamp.
animationTree.Set("parameters/TimeSeek/seek_request", 12.0);
```

---

## Playing videos — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/animation/playing_videos.html

**Contents:**
- Playing videos
- Supported playback formats
- Setting up VideoStreamPlayer
  - Handling resizing and different aspect ratios
  - Displaying a video on a 3D surface
  - Looping a video
- Video decoding conditions and recommended resolutions
- Playback limitations
- Recommended Theora encoding settings
  - Balancing quality and file size

Godot supports video playback with the VideoStreamPlayer node.

The only supported format in core is Ogg Theora (not to be confused with Ogg Vorbis audio) with optional Ogg Vorbis audio tracks. It's possible for extensions to bring support for additional formats.

H.264 and H.265 cannot be supported in core Godot, as they are both encumbered by software patents. AV1 is royalty-free, but it remains slow to decode on the CPU and hardware decoding support isn't readily available on all GPUs in use yet.

WebM was supported in core in Godot 3.x, but support for it was removed in 4.0 as it was too buggy and difficult to maintain.

You may find videos with a .ogg or .ogx extensions, which are generic extensions for data within an Ogg container.

Renaming these file extensions to .ogv may allow the videos to be imported in Godot. However, not all files with .ogg or .ogx extensions are videos - some of them may only contain audio.

Create a VideoStreamPlayer node using the Create New Node dialog.

Select the VideoStreamPlayer node in the scene tree dock, go to the inspector and load a .ogv file in the Stream property.

If you don't have your video in Ogg Theora format yet, jump to Recommended Theora encoding settings.

If you want the video to play as soon as the scene is loaded, check Autoplay in the inspector. If not, leave Autoplay disabled and call play() on the VideoStreamPlayer node in a script to start playback when desired.

By default in Godot 4.0, the VideoStreamPlayer will automatically be resized to match the video's resolution. You can make it follow usual Control sizing by enabling Expand on the VideoStreamPlayer node.

To adjust how the VideoStreamPlayer node resizes depending on window size, adjust the anchors using the Layout menu at the top of the 2D editor viewport. However, this setup may not be powerful enough to handle all use cases, such as playing fullscreen videos without distorting the video (but with empty space on the edges instead). For more control, you can use an AspectRatioContainer node, which is designed to handle this kind of use case:

Add an AspectRatioContainer node. Make sure it is not a child of any other container node. Select the AspectRatioContainer node, then set its Layout at the top of the 2D editor to Full Rect. Set Ratio in the AspectRatioContainer node to match your video's aspect ratio. You can use math formulas in the inspector to help yourself. Remember to make one of the operands a float. Otherwise, the division's result will always be an integer.

This will evaluate to (approximately) 1.777778

Once you've configured the AspectRatioContainer, reparent your VideoStreamPlayer node to be a child of the AspectRatioContainer node. Make sure Expand is enabled on the VideoStreamPlayer. Your video should now scale automatically to fit the whole screen while avoiding distortion.

See Multiple resolutions for more tips on supporting multiple aspect ratios in your project.

Using a VideoStreamPlayer node as a child of a SubViewport node, it's possible to display any 2D node on a 3D surface. For example, this can be used to display animated billboards when frame-by-frame animation would require too much memory.

This can be done with the following steps:

Create a SubViewport node. Set its size to match your video's size in pixels.

Create a VideoStreamPlayer node as a child of the SubViewport node and specify a video path in it. Make sure Expand is disabled, and enable Autoplay if needed.

Create a MeshInstance3D node with a PlaneMesh or QuadMesh resource in its Mesh property. Resize the mesh to match the video's aspect ratio (otherwise, it will appear distorted).

Create a new StandardMaterial3D resource in the Material Override property in the GeometryInstance3D section.

Enable Local To Scene in the StandardMaterial3D's Resource section (at the bottom). This is required before you can use a ViewportTexture in its Albedo Texture property.

In the StandardMaterial3D, set the Albedo > Texture property to New ViewportTexture. Edit the new resource by clicking it, then specify the path to the SubViewport node in the Viewport Path property.

Enable Albedo Texture Force sRGB in the StandardMaterial3D to prevent colors from being washed out.

If the billboard is supposed to emit its own light, set Shading Mode to Unshaded to improve rendering performance.

See Using Viewports and the GUI in 3D demo for more information on setting this up.

For looping a video, the Loop property can be enabled. This will seamlessly restart the video when it reaches its end.

Note that setting the project setting Video Delay Compensation to a non-zero value might cause your loop to not be seamless, because the synchronization of audio and video takes place at the start of each loop causing occasional missed frames. Set Video Delay Compensation in your project settings to 0 to avoid frame drop issues.

Video decoding is performed on the CPU, as GPUs don't have hardware acceleration for decoding Theora videos. Modern desktop CPUs can decode Ogg Theora videos at 1440p @ 60 FPS or more, but low-end mobile CPUs will likely struggle with high-resolution videos.

To ensure your videos decode smoothly on varied hardware:

When developing games for desktop platforms, it's recommended to encode in 1080p at most (preferably at 30 FPS). Most people are still using 1080p or lower resolution displays, so encoding higher-resolution videos may not be worth the increased file size and CPU requirements.

When developing games for mobile or web platforms, it's recommended to encode in 720p at most (preferably at 30 FPS or even lower). The visual difference between 720p and 1080p videos on a mobile device is usually not that noticeable.

There are some limitations with the current implementation of video playback in Godot:

Streaming a video from a URL is not supported.

Only mono and stereo audio output is supported. Videos with 4, 5.1 and 7.1 audio channels are supported but down-mixed to stereo.

A word of advice is to avoid relying on built-in Ogg Theora exporters (most of the time). There are 2 reasons you may want to favor using an external program to encode your video:

Some programs such as Blender can render to Ogg Theora. However, the default quality presets are usually very low by today's standards. You may be able to increase the quality options in the software you're using, but you may find the output quality to remain less than ideal (given the increased file size). This usually means that the software only supports encoding to constant bit rate (CBR), instead of variable bit rate (VBR). VBR encoding should be preferred in most scenarios as it provides a better quality to file size ratio.

Some other programs can't render to Ogg Theora at all.

In this case, you can render the video to an intermediate high-quality format (such as a high-bitrate H.264 video) then re-encode it to Ogg Theora. Ideally, you should use a lossless or uncompressed format as an intermediate format to maximize the quality of the output Ogg Theora video, but this can require a lot of disk space.

FFmpeg (CLI) is a popular open source tool for this purpose. FFmpeg has a steep learning curve, but it's a powerful tool.

Here are example FFmpeg commands to convert an MP4 video to Ogg Theora. Since FFmpeg supports a lot of input formats, you should be able to use the commands below with almost any input video format (AVI, MOV, WebM, …).

Make sure your copy of FFmpeg is compiled with libtheora and libvorbis support. You can check this by running ffmpeg without any arguments, then looking at the configuration: line in the command output.

Current official FFmpeg releases have some bugs in their Ogg/Theora multiplexer. It's highly recommended to use one of the latest static daily builds, or build from their master branch to get the latest fixes.

The video quality level (-q:v) must be between 1 and 10. Quality 6 is a good compromise between quality and file size. If encoding at a high resolution (such as 1440p or 4K), you will probably want to decrease -q:v to 5 to keep file sizes reasonable. Since pixel density is higher on a 1440p or 4K video, lower quality presets at higher resolutions will look as good or better compared to low-resolution videos.

The audio quality level (-q:a) must be between -1 and 10. Quality 6 provides a good compromise between quality and file size. In contrast to video quality, increasing audio quality doesn't increase the output file size nearly as much. Therefore, if you want the cleanest audio possible, you can increase this to 9 to get perceptually lossless audio. This is especially valuable if your input file already uses lossy audio compression. Higher quality audio does increase the CPU usage of the decoder, so it might lead to audio dropouts in case of high system load. See this page for a table listing Ogg Vorbis audio quality presets and their respective variable bitrates.

The GOP (Group of Pictures) size (-g:v) is the max interval between keyframes. Increasing this value can improve compression with almost no impact on quality. The default size (12) is too low for most types of content, it's therefore recommended using higher GOP values before reducing video quality. Compression benefits will fade away as the GOP size increases though. Values between 64 and 512 usually give the best compression.

Higher GOP sizes will increase max seek times with a sudden increase when going beyond powers of two starting at 64. Max seek times with GOP size 65 can be almost twice as long as with GOP size 64, depending on decoding speed.

The following command converts the video while keeping its original resolution. The video and audio's bitrate will be variable to maximize quality while saving space in parts of the video/audio that don't require a high bitrate (such as static scenes).

The following command resizes a video to be 720 pixels tall (720p), while preserving its existing aspect ratio. This helps decrease the file size significantly if the source is recorded at a higher resolution than 720p:

Chroma key, commonly known as the "green screen" or "blue screen" effect, allows you to remove a specific color from an image or video and replace it with another background. This effect is widely used in video production to composite different elements together seamlessly.

We will achieve the chroma key effect by writing a custom shader in GDScript and using a VideoStreamPlayer node to display the video content.

Ensure that the scene contains a VideoStreamPlayer node to play the video and a Control node to hold the UI elements for controlling the chroma key effect.

To implement the chroma key effect, follow these steps:

Select the VideoStreamPlayer node in the scene and go to its properties. Under CanvasItem > Material, create a new shader named "ChromaKeyShader.gdshader."

In the "ChromaKeyShader.gdshader" file, write the custom shader code as shown below:

The shader uses the distance calculation to identify pixels close to the chroma key color and discards them, effectively removing the selected color. Pixels that are slightly further away from the chroma key color are faded based on the fade_factor, blending them smoothly with the surrounding colors. This process creates the desired chroma key effect, making it appear as if the background has been replaced with another image or video.

The code above represents a simple demonstration of the Chroma Key shader, and users can customize it according to their specific requirements.

To allow users to manipulate the chroma key effect in real-time, we created sliders in the Control node. The Control node's script contains the following functions:

also make sure that the range of the sliders are appropriate, our settings are :

Connect the appropriate signal from the UI elements to the Control node's script. you created in the Control node's script to control the chroma key effect. These signal handlers will update the shader's uniform variables in response to user input.

Save and run the scene to see the chroma key effect in action! With the provided UI controls, you can now adjust the chroma key color, pickup range, and fade amount in real-time, achieving the desired chroma key functionality for your video content.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
ffmpeg -i input.mp4 -q:v 6 -q:a 6 -g:v 64 output.ogv
```

Example 2 (json):
```json
ffmpeg -i input.mp4 -vf "scale=-1:720" -q:v 6 -q:a 6 -g:v 64 output.ogv
```

Example 3 (typescript):
```typescript
shader_type canvas_item;

// Uniform variables for chroma key effect
uniform vec3 chroma_key_color : source_color = vec3(0.0, 1.0, 0.0);
uniform float pickup_range : hint_range(0.0, 1.0) = 0.1;
uniform float fade_amount : hint_range(0.0, 1.0) = 0.1;

void fragment() {
    // Get the color from the texture at the given UV coordinates
    vec4 color = texture(TEXTURE, UV);

    // Calculate the distance between the current color and the chroma key color
    float distance = length(color.rgb - chroma_key_color);

    // If the distance is within the pickup range, discard the pixel
    // the lesser the distance more likely the colors are
    if (distance <= pickup_range) {
        discard;
    }

    // Calculate the fade factor based on the pickup range and fade amount
    float fade_factor = smoothstep(pickup_range, pickup_range + fade_amount, distance);

    // Set the output color with the original RGB values and the calculated fade factor
    COLOR = vec4(color.rgb, fade_factor);
}
```

Example 4 (gdscript):
```gdscript
extends Control

 func _on_color_picker_button_color_changed(color):
     # Update the "chroma_key_color" shader parameter of the VideoStreamPlayer's material.
     $VideoStreamPlayer.material.set("shader_parameter/chroma_key_color", color)

 func _on_h_slider_value_changed(value):
     # Update the "pickup_range" shader parameter of the VideoStreamPlayer's material.
     $VideoStreamPlayer.material.set("shader_parameter/pickup_range", value)

 func _on_h_slider_2_value_changed(value):
     # Update the "fade_amount" shader parameter of the VideoStreamPlayer's material.
     $VideoStreamPlayer.material.set("shader_parameter/fade_amount", value)

func _on_video_stream_player_finished():
     # Restart the video playback when it's finished.
     $VideoStreamPlayer.play()
```

---

## Animating thousands of objects — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/performance/vertex_animation/index.html

**Contents:**
- Animating thousands of objects

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Controlling thousands of fish with Particles — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/performance/vertex_animation/controlling_thousands_of_fish.html

**Contents:**
- Controlling thousands of fish with Particles
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

The problem with MeshInstance3D is that it is expensive to update their transform array. It is great for placing many static objects around the scene. But it is still difficult to move the objects around the scene.

To make each instance move in an interesting way, we will use a GPUParticles3D node. Particles take advantage of GPU acceleration by computing and setting the per-instance information in a Shader.

First create a Particles node. Then, under "Draw Passes" set the Particle's "Draw Pass 1" to your Mesh. Then under "Process Material" create a new ShaderMaterial.

Set the shader_type to particles.

Then add the following two functions:

These functions come from the default ParticleProcessMaterial. They are used to generate a random number from each particle's RANDOM_SEED.

A unique thing about particle shaders is that some built-in variables are saved across frames. TRANSFORM, COLOR, and CUSTOM can all be accessed in the shader of the mesh, and also in the particle shader the next time it is run.

Next, setup your start() function. Particles shaders contain a start() function and a process() function.

The code in the start() function only runs when the particle system starts. The code in the process() function will always run.

We need to generate 4 random numbers: 3 to create a random position and one for the random offset of the swim cycle.

First, generate 4 seeds inside the start() function using the hash() function provided above:

Then, use those seeds to generate random numbers using rand_from_seed:

Finally, assign position to TRANSFORM[3].xyz, which is the part of the transform that holds the position information.

Remember, all this code so far goes inside the start() function.

The vertex shader for your mesh can stay the exact same as it was in the previous tutorial.

Now you can move each fish individually each frame, either by adding to the TRANSFORM directly or by writing to VELOCITY.

Let's transform the fish by setting their VELOCITY in the start() function.

This is the most basic way to set VELOCITY every particle (or fish) will have the same velocity.

Just by setting VELOCITY you can make the fish swim however you want. For example, try the code below.

This will give each fish a unique speed between 2 and 10.

You can also let each fish change its velocity over time if you set the velocity in the process() function.

If you used CUSTOM.y in the last tutorial, you can also set the speed of the swim animation based on the VELOCITY. Just use CUSTOM.y.

This code gives you the following behavior:

Using a ParticleProcessMaterial you can make the fish behavior as simple or complex as you like. In this tutorial we only set Velocity, but in your own Shaders you can also set COLOR, rotation, scale (through TRANSFORM). Please refer to the Particles Shader Reference for more information on particle shaders.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
shader_type particles
```

Example 2 (unknown):
```unknown
float rand_from_seed(in uint seed) {
  int k;
  int s = int(seed);
  if (s == 0)
    s = 305420679;
  k = s / 127773;
  s = 16807 * (s - k * 127773) - 2836 * k;
  if (s < 0)
    s += 2147483647;
  seed = uint(s);
  return float(seed % uint(65536)) / 65535.0;
}

uint hash(uint x) {
  x = ((x >> uint(16)) ^ x) * uint(73244475);
  x = ((x >> uint(16)) ^ x) * uint(73244475);
  x = (x >> uint(16)) ^ x;
  return x;
}
```

Example 3 (unknown):
```unknown
uint alt_seed1 = hash(NUMBER + uint(1) + RANDOM_SEED);
uint alt_seed2 = hash(NUMBER + uint(27) + RANDOM_SEED);
uint alt_seed3 = hash(NUMBER + uint(43) + RANDOM_SEED);
uint alt_seed4 = hash(NUMBER + uint(111) + RANDOM_SEED);
```

Example 4 (unknown):
```unknown
CUSTOM.x = rand_from_seed(alt_seed1);
vec3 position = vec3(rand_from_seed(alt_seed2) * 2.0 - 1.0,
                     rand_from_seed(alt_seed3) * 2.0 - 1.0,
                     rand_from_seed(alt_seed4) * 2.0 - 1.0);
```

---

## AnimationPlayer — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_animationplayer.html

**Contents:**
- AnimationPlayer
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: AnimationMixer < Node < Object

A node used for animation playback.

An animation player is used for general-purpose playback of animations. It contains a dictionary of AnimationLibrary resources and custom blend times between animation transitions.

Some methods and properties use a single key to reference an animation directly. These keys are formatted as the key for the library, followed by a forward slash, then the key for the animation within the library, for example "movement/run". If the library's key is an empty string (known as the default library), the forward slash is omitted, being the same key used by the library.

AnimationPlayer is better-suited than Tween for more complex animations, for example ones with non-trivial timings. It can also be used over Tween if the animation track editor is more convenient than doing it in code.

Updating the target properties of animations occurs at the process frame.

Animation documentation index

Third Person Shooter (TPS) Demo

current_animation_length

current_animation_position

playback_auto_capture

playback_auto_capture_duration

playback_auto_capture_ease_type

playback_auto_capture_transition_type

playback_default_blend_time

animation_get_next(animation_from: StringName) const

animation_set_next(animation_from: StringName, animation_to: StringName)

get_blend_time(animation_from: StringName, animation_to: StringName) const

AnimationMethodCallMode

get_method_call_mode() const

get_playing_speed() const

AnimationProcessCallback

get_process_callback() const

get_section_end_time() const

get_section_start_time() const

play(name: StringName = &"", custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false)

play_backwards(name: StringName = &"", custom_blend: float = -1)

play_section(name: StringName = &"", start_time: float = -1, end_time: float = -1, custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false)

play_section_backwards(name: StringName = &"", start_time: float = -1, end_time: float = -1, custom_blend: float = -1)

play_section_with_markers(name: StringName = &"", start_marker: StringName = &"", end_marker: StringName = &"", custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false)

play_section_with_markers_backwards(name: StringName = &"", start_marker: StringName = &"", end_marker: StringName = &"", custom_blend: float = -1)

play_with_capture(name: StringName = &"", duration: float = -1.0, custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false, trans_type: TransitionType = 0, ease_type: EaseType = 0)

queue(name: StringName)

seek(seconds: float, update: bool = false, update_only: bool = false)

set_blend_time(animation_from: StringName, animation_to: StringName, sec: float)

set_method_call_mode(mode: AnimationMethodCallMode)

set_process_callback(mode: AnimationProcessCallback)

set_root(path: NodePath)

set_section(start_time: float = -1, end_time: float = -1)

set_section_with_markers(start_marker: StringName = &"", end_marker: StringName = &"")

stop(keep_state: bool = false)

animation_changed(old_name: StringName, new_name: StringName) 🔗

Emitted when a queued animation plays after the previous animation finished. See also queue().

Note: The signal is not emitted when the animation is changed via play() or by an AnimationTree.

current_animation_changed(name: String) 🔗

Emitted when current_animation changes.

enum AnimationProcessCallback: 🔗

AnimationProcessCallback ANIMATION_PROCESS_PHYSICS = 0

Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS.

AnimationProcessCallback ANIMATION_PROCESS_IDLE = 1

Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE.

AnimationProcessCallback ANIMATION_PROCESS_MANUAL = 2

Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL.

enum AnimationMethodCallMode: 🔗

AnimationMethodCallMode ANIMATION_METHOD_CALL_DEFERRED = 0

Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_METHOD_DEFERRED.

AnimationMethodCallMode ANIMATION_METHOD_CALL_IMMEDIATE = 1

Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_METHOD_IMMEDIATE.

String assigned_animation 🔗

void set_assigned_animation(value: String)

String get_assigned_animation()

If playing, the current animation's key, otherwise, the animation last played. When set, this changes the animation, but will not play it unless already playing. See also current_animation.

String autoplay = "" 🔗

void set_autoplay(value: String)

String get_autoplay()

The key of the animation to play when the scene loads.

String current_animation = "" 🔗

void set_current_animation(value: String)

String get_current_animation()

The key of the currently playing animation. If no animation is playing, the property's value is an empty string. Changing this value does not restart the animation. See play() for more information on playing animations.

Note: While this property appears in the Inspector, it's not meant to be edited, and it's not saved in the scene. This property is mainly used to get the currently playing animation, and internally for animation playback tracks. For more information, see Animation.

float current_animation_length 🔗

float get_current_animation_length()

The length (in seconds) of the currently playing animation.

float current_animation_position 🔗

float get_current_animation_position()

The position (in seconds) of the currently playing animation.

bool movie_quit_on_finish = false 🔗

void set_movie_quit_on_finish_enabled(value: bool)

bool is_movie_quit_on_finish_enabled()

If true and the engine is running in Movie Maker mode (see MovieWriter), exits the engine with SceneTree.quit() as soon as an animation is done playing in this AnimationPlayer. A message is printed when the engine quits for this reason.

Note: This obeys the same logic as the AnimationMixer.animation_finished signal, so it will not quit the engine if the animation is set to be looping.

bool playback_auto_capture = true 🔗

void set_auto_capture(value: bool)

bool is_auto_capture()

If true, performs AnimationMixer.capture() before playback automatically. This means just play_with_capture() is executed with default arguments instead of play().

Note: Capture interpolation is only performed if the animation contains a capture track. See also Animation.UPDATE_CAPTURE.

float playback_auto_capture_duration = -1.0 🔗

void set_auto_capture_duration(value: float)

float get_auto_capture_duration()

See also play_with_capture() and AnimationMixer.capture().

If playback_auto_capture_duration is negative value, the duration is set to the interval between the current position and the first key.

EaseType playback_auto_capture_ease_type = 0 🔗

void set_auto_capture_ease_type(value: EaseType)

EaseType get_auto_capture_ease_type()

The ease type of the capture interpolation. See also EaseType.

TransitionType playback_auto_capture_transition_type = 0 🔗

void set_auto_capture_transition_type(value: TransitionType)

TransitionType get_auto_capture_transition_type()

The transition type of the capture interpolation. See also TransitionType.

float playback_default_blend_time = 0.0 🔗

void set_default_blend_time(value: float)

float get_default_blend_time()

The default time in which to blend animations. Ranges from 0 to 4096 with 0.01 precision.

float speed_scale = 1.0 🔗

void set_speed_scale(value: float)

float get_speed_scale()

The speed scaling ratio. For example, if this value is 1, then the animation plays at normal speed. If it's 0.5, then it plays at half speed. If it's 2, then it plays at double speed.

If set to a negative value, the animation is played in reverse. If set to 0, the animation will not advance.

StringName animation_get_next(animation_from: StringName) const 🔗

Returns the key of the animation which is queued to play after the animation_from animation.

void animation_set_next(animation_from: StringName, animation_to: StringName) 🔗

Triggers the animation_to animation when the animation_from animation completes.

Clears all queued, unplayed animations.

float get_blend_time(animation_from: StringName, animation_to: StringName) const 🔗

Returns the blend time (in seconds) between two animations, referenced by their keys.

AnimationMethodCallMode get_method_call_mode() const 🔗

Deprecated: Use AnimationMixer.callback_mode_method instead.

Returns the call mode used for "Call Method" tracks.

float get_playing_speed() const 🔗

Returns the actual playing speed of current animation or 0 if not playing. This speed is the speed_scale property multiplied by custom_speed argument specified when calling the play() method.

Returns a negative value if the current animation is playing backwards.

AnimationProcessCallback get_process_callback() const 🔗

Deprecated: Use AnimationMixer.callback_mode_process instead.

Returns the process notification in which to update animations.

PackedStringArray get_queue() 🔗

Returns a list of the animation keys that are currently queued to play.

NodePath get_root() const 🔗

Deprecated: Use AnimationMixer.root_node instead.

Returns the node which node path references will travel from.

float get_section_end_time() const 🔗

Returns the end time of the section currently being played.

float get_section_start_time() const 🔗

Returns the start time of the section currently being played.

bool has_section() const 🔗

Returns true if an animation is currently playing with a section.

bool is_playing() const 🔗

Returns true if an animation is currently playing (even if speed_scale and/or custom_speed are 0).

Pauses the currently playing animation. The current_animation_position will be kept and calling play() or play_backwards() without arguments or with the same animation name as assigned_animation will resume the animation.

void play(name: StringName = &"", custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false) 🔗

Plays the animation with key name. Custom blend times and speed can be set.

The from_end option only affects when switching to a new animation track, or if the same track but at the start or end. It does not affect resuming playback that was paused in the middle of an animation. If custom_speed is negative and from_end is true, the animation will play backwards (which is equivalent to calling play_backwards()).

The AnimationPlayer keeps track of its current or last played animation with assigned_animation. If this method is called with that same animation name, or with no name parameter, the assigned animation will resume playing if it was paused.

Note: The animation will be updated the next time the AnimationPlayer is processed. If other variables are updated at the same time this is called, they may be updated too early. To perform the update immediately, call advance(0).

void play_backwards(name: StringName = &"", custom_blend: float = -1) 🔗

Plays the animation with key name in reverse.

This method is a shorthand for play() with custom_speed = -1.0 and from_end = true, so see its description for more information.

void play_section(name: StringName = &"", start_time: float = -1, end_time: float = -1, custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false) 🔗

Plays the animation with key name and the section starting from start_time and ending on end_time. See also play().

Setting start_time to a value outside the range of the animation means the start of the animation will be used instead, and setting end_time to a value outside the range of the animation means the end of the animation will be used instead. start_time cannot be equal to end_time.

void play_section_backwards(name: StringName = &"", start_time: float = -1, end_time: float = -1, custom_blend: float = -1) 🔗

Plays the animation with key name and the section starting from start_time and ending on end_time in reverse.

This method is a shorthand for play_section() with custom_speed = -1.0 and from_end = true, see its description for more information.

void play_section_with_markers(name: StringName = &"", start_marker: StringName = &"", end_marker: StringName = &"", custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false) 🔗

Plays the animation with key name and the section starting from start_marker and ending on end_marker.

If the start marker is empty, the section starts from the beginning of the animation. If the end marker is empty, the section ends on the end of the animation. See also play().

void play_section_with_markers_backwards(name: StringName = &"", start_marker: StringName = &"", end_marker: StringName = &"", custom_blend: float = -1) 🔗

Plays the animation with key name and the section starting from start_marker and ending on end_marker in reverse.

This method is a shorthand for play_section_with_markers() with custom_speed = -1.0 and from_end = true, see its description for more information.

void play_with_capture(name: StringName = &"", duration: float = -1.0, custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false, trans_type: TransitionType = 0, ease_type: EaseType = 0) 🔗

See also AnimationMixer.capture().

You can use this method to use more detailed options for capture than those performed by playback_auto_capture. When playback_auto_capture is false, this method is almost the same as the following:

If name is blank, it specifies assigned_animation.

If duration is a negative value, the duration is set to the interval between the current position and the first key, when from_end is true, uses the interval between the current position and the last key instead.

Note: The duration takes speed_scale into account, but custom_speed does not, because the capture cache is interpolated with the blend result and the result may contain multiple animations.

void queue(name: StringName) 🔗

Queues an animation for playback once the current animation and all previously queued animations are done.

Note: If a looped animation is currently playing, the queued animation will never play unless the looped animation is stopped somehow.

void reset_section() 🔗

Resets the current section. Does nothing if a section has not been set.

void seek(seconds: float, update: bool = false, update_only: bool = false) 🔗

Seeks the animation to the seconds point in time (in seconds). If update is true, the animation updates too, otherwise it updates at process time. Events between the current frame and seconds are skipped.

If update_only is true, the method / audio / animation playback tracks will not be processed.

Note: Seeking to the end of the animation doesn't emit AnimationMixer.animation_finished. If you want to skip animation and emit the signal, use AnimationMixer.advance().

void set_blend_time(animation_from: StringName, animation_to: StringName, sec: float) 🔗

Specifies a blend time (in seconds) between two animations, referenced by their keys.

void set_method_call_mode(mode: AnimationMethodCallMode) 🔗

Deprecated: Use AnimationMixer.callback_mode_method instead.

Sets the call mode used for "Call Method" tracks.

void set_process_callback(mode: AnimationProcessCallback) 🔗

Deprecated: Use AnimationMixer.callback_mode_process instead.

Sets the process notification in which to update animations.

void set_root(path: NodePath) 🔗

Deprecated: Use AnimationMixer.root_node instead.

Sets the node which node path references will travel from.

void set_section(start_time: float = -1, end_time: float = -1) 🔗

Changes the start and end times of the section being played. The current playback position will be clamped within the new section. See also play_section().

void set_section_with_markers(start_marker: StringName = &"", end_marker: StringName = &"") 🔗

Changes the start and end markers of the section being played. The current playback position will be clamped within the new section. See also play_section_with_markers().

If the argument is empty, the section uses the beginning or end of the animation. If both are empty, it means that the section is not set.

void stop(keep_state: bool = false) 🔗

Stops the currently playing animation. The animation position is reset to 0 and the custom_speed is reset to 1.0. See also pause().

If keep_state is true, the animation state is not updated visually.

Note: The method / audio / animation playback tracks will not be processed by this method.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (unknown):
```unknown
capture(name, duration, trans_type, ease_type)
play(name, custom_blend, custom_speed, from_end)
```

---

## AnimationMixer — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_animationmixer.html

**Contents:**
- AnimationMixer
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: Node < Object

Inherited By: AnimationPlayer, AnimationTree

Base class for AnimationPlayer and AnimationTree.

Base class for AnimationPlayer and AnimationTree to manage animation lists. It also has general properties and methods for playback and blending.

After instantiating the playback information data within the extended class, the blending is processed by the AnimationMixer.

Migrating Animations from Godot 4.0 to 4.3

AnimationCallbackModeDiscrete

callback_mode_discrete

AnimationCallbackModeMethod

AnimationCallbackModeProcess

callback_mode_process

_post_process_key_value(animation: Animation, track: int, value: Variant, object_id: int, object_sub_idx: int) virtual const

add_animation_library(name: StringName, library: AnimationLibrary)

advance(delta: float)

capture(name: StringName, duration: float, trans_type: TransitionType = 0, ease_type: EaseType = 0)

find_animation(animation: Animation) const

find_animation_library(animation: Animation) const

get_animation(name: StringName) const

get_animation_library(name: StringName) const

get_animation_library_list() const

get_animation_list() const

get_root_motion_position() const

get_root_motion_position_accumulator() const

get_root_motion_rotation() const

get_root_motion_rotation_accumulator() const

get_root_motion_scale() const

get_root_motion_scale_accumulator() const

has_animation(name: StringName) const

has_animation_library(name: StringName) const

remove_animation_library(name: StringName)

rename_animation_library(name: StringName, newname: StringName)

animation_finished(anim_name: StringName) 🔗

Notifies when an animation finished playing.

Note: This signal is not emitted if an animation is looping.

animation_libraries_updated() 🔗

Notifies when the animation libraries have changed.

animation_list_changed() 🔗

Notifies when an animation list is changed.

animation_started(anim_name: StringName) 🔗

Notifies when an animation starts playing.

Note: This signal is not emitted if an animation is looping.

Notifies when the caches have been cleared, either automatically, or manually via clear_caches().

Notifies when the blending result related have been applied to the target objects.

Notifies when the property related process have been updated.

enum AnimationCallbackModeProcess: 🔗

AnimationCallbackModeProcess ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS = 0

Process animation during physics frames (see Node.NOTIFICATION_INTERNAL_PHYSICS_PROCESS). This is especially useful when animating physics bodies.

AnimationCallbackModeProcess ANIMATION_CALLBACK_MODE_PROCESS_IDLE = 1

Process animation during process frames (see Node.NOTIFICATION_INTERNAL_PROCESS).

AnimationCallbackModeProcess ANIMATION_CALLBACK_MODE_PROCESS_MANUAL = 2

Do not process animation. Use advance() to process the animation manually.

enum AnimationCallbackModeMethod: 🔗

AnimationCallbackModeMethod ANIMATION_CALLBACK_MODE_METHOD_DEFERRED = 0

Batch method calls during the animation process, then do the calls after events are processed. This avoids bugs involving deleting nodes or modifying the AnimationPlayer while playing.

AnimationCallbackModeMethod ANIMATION_CALLBACK_MODE_METHOD_IMMEDIATE = 1

Make method calls immediately when reached in the animation.

enum AnimationCallbackModeDiscrete: 🔗

AnimationCallbackModeDiscrete ANIMATION_CALLBACK_MODE_DISCRETE_DOMINANT = 0

An Animation.UPDATE_DISCRETE track value takes precedence when blending Animation.UPDATE_CONTINUOUS or Animation.UPDATE_CAPTURE track values and Animation.UPDATE_DISCRETE track values.

AnimationCallbackModeDiscrete ANIMATION_CALLBACK_MODE_DISCRETE_RECESSIVE = 1

An Animation.UPDATE_CONTINUOUS or Animation.UPDATE_CAPTURE track value takes precedence when blending the Animation.UPDATE_CONTINUOUS or Animation.UPDATE_CAPTURE track values and the Animation.UPDATE_DISCRETE track values. This is the default behavior for AnimationPlayer.

AnimationCallbackModeDiscrete ANIMATION_CALLBACK_MODE_DISCRETE_FORCE_CONTINUOUS = 2

Always treat the Animation.UPDATE_DISCRETE track value as Animation.UPDATE_CONTINUOUS with Animation.INTERPOLATION_NEAREST. This is the default behavior for AnimationTree.

If a value track has un-interpolatable type key values, it is internally converted to use ANIMATION_CALLBACK_MODE_DISCRETE_RECESSIVE with Animation.UPDATE_DISCRETE.

Un-interpolatable type list:

@GlobalScope.TYPE_NIL

@GlobalScope.TYPE_NODE_PATH

@GlobalScope.TYPE_RID

@GlobalScope.TYPE_OBJECT

@GlobalScope.TYPE_CALLABLE

@GlobalScope.TYPE_SIGNAL

@GlobalScope.TYPE_DICTIONARY

@GlobalScope.TYPE_PACKED_BYTE_ARRAY

@GlobalScope.TYPE_BOOL and @GlobalScope.TYPE_INT are treated as @GlobalScope.TYPE_FLOAT during blending and rounded when the result is retrieved.

It is same for arrays and vectors with them such as @GlobalScope.TYPE_PACKED_INT32_ARRAY or @GlobalScope.TYPE_VECTOR2I, they are treated as @GlobalScope.TYPE_PACKED_FLOAT32_ARRAY or @GlobalScope.TYPE_VECTOR2. Also note that for arrays, the size is also interpolated.

@GlobalScope.TYPE_STRING and @GlobalScope.TYPE_STRING_NAME are interpolated between character codes and lengths, but note that there is a difference in algorithm between interpolation between keys and interpolation by blending.

void set_active(value: bool)

If true, the AnimationMixer will be processing.

int audio_max_polyphony = 32 🔗

void set_audio_max_polyphony(value: int)

int get_audio_max_polyphony()

The number of possible simultaneous sounds for each of the assigned AudioStreamPlayers.

For example, if this value is 32 and the animation has two audio tracks, the two AudioStreamPlayers assigned can play simultaneously up to 32 voices each.

AnimationCallbackModeDiscrete callback_mode_discrete = 1 🔗

void set_callback_mode_discrete(value: AnimationCallbackModeDiscrete)

AnimationCallbackModeDiscrete get_callback_mode_discrete()

Ordinarily, tracks can be set to Animation.UPDATE_DISCRETE to update infrequently, usually when using nearest interpolation.

However, when blending with Animation.UPDATE_CONTINUOUS several results are considered. The callback_mode_discrete specify it explicitly. See also AnimationCallbackModeDiscrete.

To make the blended results look good, it is recommended to set this to ANIMATION_CALLBACK_MODE_DISCRETE_FORCE_CONTINUOUS to update every frame during blending. Other values exist for compatibility and they are fine if there is no blending, but not so, may produce artifacts.

AnimationCallbackModeMethod callback_mode_method = 0 🔗

void set_callback_mode_method(value: AnimationCallbackModeMethod)

AnimationCallbackModeMethod get_callback_mode_method()

The call mode used for "Call Method" tracks.

AnimationCallbackModeProcess callback_mode_process = 1 🔗

void set_callback_mode_process(value: AnimationCallbackModeProcess)

AnimationCallbackModeProcess get_callback_mode_process()

The process notification in which to update animations.

bool deterministic = false 🔗

void set_deterministic(value: bool)

bool is_deterministic()

If true, the blending uses the deterministic algorithm. The total weight is not normalized and the result is accumulated with an initial value (0 or a "RESET" animation if present).

This means that if the total amount of blending is 0.0, the result is equal to the "RESET" animation.

If the number of tracks between the blended animations is different, the animation with the missing track is treated as if it had the initial value.

If false, The blend does not use the deterministic algorithm. The total weight is normalized and always 1.0. If the number of tracks between the blended animations is different, nothing is done about the animation that is missing a track.

Note: In AnimationTree, the blending with AnimationNodeAdd2, AnimationNodeAdd3, AnimationNodeSub2 or the weight greater than 1.0 may produce unexpected results.

For example, if AnimationNodeAdd2 blends two nodes with the amount 1.0, then total weight is 2.0 but it will be normalized to make the total amount 1.0 and the result will be equal to AnimationNodeBlend2 with the amount 0.5.

bool reset_on_save = true 🔗

void set_reset_on_save_enabled(value: bool)

bool is_reset_on_save_enabled()

This is used by the editor. If set to true, the scene will be saved with the effects of the reset animation (the animation with the key "RESET") applied as if it had been seeked to time 0, with the editor keeping the values that the scene had before saving.

This makes it more convenient to preview and edit animations in the editor, as changes to the scene will not be saved as long as they are set in the reset animation.

bool root_motion_local = false 🔗

void set_root_motion_local(value: bool)

bool is_root_motion_local()

If true, get_root_motion_position() value is extracted as a local translation value before blending. In other words, it is treated like the translation is done after the rotation.

NodePath root_motion_track = NodePath("") 🔗

void set_root_motion_track(value: NodePath)

NodePath get_root_motion_track()

The path to the Animation track used for root motion. Paths must be valid scene-tree paths to a node, and must be specified starting from the parent node of the node that will reproduce the animation. The root_motion_track uses the same format as Animation.track_set_path(), but note that a bone must be specified.

If the track has type Animation.TYPE_POSITION_3D, Animation.TYPE_ROTATION_3D, or Animation.TYPE_SCALE_3D the transformation will be canceled visually, and the animation will appear to stay in place. See also get_root_motion_position(), get_root_motion_rotation(), get_root_motion_scale(), and RootMotionView.

NodePath root_node = NodePath("..") 🔗

void set_root_node(value: NodePath)

NodePath get_root_node()

The node which node path references will travel from.

Variant _post_process_key_value(animation: Animation, track: int, value: Variant, object_id: int, object_sub_idx: int) virtual const 🔗

A virtual function for processing after getting a key during playback.

Error add_animation_library(name: StringName, library: AnimationLibrary) 🔗

Adds library to the animation player, under the key name.

AnimationMixer has a global library by default with an empty string as key. For adding an animation to the global library:

void advance(delta: float) 🔗

Manually advance the animations by the specified time (in seconds).

void capture(name: StringName, duration: float, trans_type: TransitionType = 0, ease_type: EaseType = 0) 🔗

If the animation track specified by name has an option Animation.UPDATE_CAPTURE, stores current values of the objects indicated by the track path as a cache. If there is already a captured cache, the old cache is discarded.

After this it will interpolate with current animation blending result during the playback process for the time specified by duration, working like a crossfade.

You can specify trans_type as the curve for the interpolation. For better results, it may be appropriate to specify Tween.TRANS_LINEAR for cases where the first key of the track begins with a non-zero value or where the key value does not change, and Tween.TRANS_QUAD for cases where the key value changes linearly.

void clear_caches() 🔗

AnimationMixer caches animated nodes. It may not notice if a node disappears; clear_caches() forces it to update the cache again.

StringName find_animation(animation: Animation) const 🔗

Returns the key of animation or an empty StringName if not found.

StringName find_animation_library(animation: Animation) const 🔗

Returns the key for the AnimationLibrary that contains animation or an empty StringName if not found.

Animation get_animation(name: StringName) const 🔗

Returns the Animation with the key name. If the animation does not exist, null is returned and an error is logged.

AnimationLibrary get_animation_library(name: StringName) const 🔗

Returns the first AnimationLibrary with key name or null if not found.

To get the AnimationMixer's global animation library, use get_animation_library("").

Array[StringName] get_animation_library_list() const 🔗

Returns the list of stored library keys.

PackedStringArray get_animation_list() const 🔗

Returns the list of stored animation keys.

Vector3 get_root_motion_position() const 🔗

Retrieve the motion delta of position with the root_motion_track as a Vector3 that can be used elsewhere.

If root_motion_track is not a path to a track of type Animation.TYPE_POSITION_3D, returns Vector3(0, 0, 0).

See also root_motion_track and RootMotionView.

The most basic example is applying position to CharacterBody3D:

By using this in combination with get_root_motion_rotation_accumulator(), you can apply the root motion position more correctly to account for the rotation of the node.

If root_motion_local is true, returns the pre-multiplied translation value with the inverted rotation.

In this case, the code can be written as follows:

Vector3 get_root_motion_position_accumulator() const 🔗

Retrieve the blended value of the position tracks with the root_motion_track as a Vector3 that can be used elsewhere.

This is useful in cases where you want to respect the initial key values of the animation.

For example, if an animation with only one key Vector3(0, 0, 0) is played in the previous frame and then an animation with only one key Vector3(1, 0, 1) is played in the next frame, the difference can be calculated as follows:

However, if the animation loops, an unintended discrete change may occur, so this is only useful for some simple use cases.

Quaternion get_root_motion_rotation() const 🔗

Retrieve the motion delta of rotation with the root_motion_track as a Quaternion that can be used elsewhere.

If root_motion_track is not a path to a track of type Animation.TYPE_ROTATION_3D, returns Quaternion(0, 0, 0, 1).

See also root_motion_track and RootMotionView.

The most basic example is applying rotation to CharacterBody3D:

Quaternion get_root_motion_rotation_accumulator() const 🔗

Retrieve the blended value of the rotation tracks with the root_motion_track as a Quaternion that can be used elsewhere.

This is necessary to apply the root motion position correctly, taking rotation into account. See also get_root_motion_position().

Also, this is useful in cases where you want to respect the initial key values of the animation.

For example, if an animation with only one key Quaternion(0, 0, 0, 1) is played in the previous frame and then an animation with only one key Quaternion(0, 0.707, 0, 0.707) is played in the next frame, the difference can be calculated as follows:

However, if the animation loops, an unintended discrete change may occur, so this is only useful for some simple use cases.

Vector3 get_root_motion_scale() const 🔗

Retrieve the motion delta of scale with the root_motion_track as a Vector3 that can be used elsewhere.

If root_motion_track is not a path to a track of type Animation.TYPE_SCALE_3D, returns Vector3(0, 0, 0).

See also root_motion_track and RootMotionView.

The most basic example is applying scale to CharacterBody3D:

Vector3 get_root_motion_scale_accumulator() const 🔗

Retrieve the blended value of the scale tracks with the root_motion_track as a Vector3 that can be used elsewhere.

For example, if an animation with only one key Vector3(1, 1, 1) is played in the previous frame and then an animation with only one key Vector3(2, 2, 2) is played in the next frame, the difference can be calculated as follows:

However, if the animation loops, an unintended discrete change may occur, so this is only useful for some simple use cases.

bool has_animation(name: StringName) const 🔗

Returns true if the AnimationMixer stores an Animation with key name.

bool has_animation_library(name: StringName) const 🔗

Returns true if the AnimationMixer stores an AnimationLibrary with key name.

void remove_animation_library(name: StringName) 🔗

Removes the AnimationLibrary associated with the key name.

void rename_animation_library(name: StringName, newname: StringName) 🔗

Moves the AnimationLibrary associated with the key name to the key newname.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
var global_library = mixer.get_animation_library("")
global_library.add_animation("animation_name", animation_resource)
```

Example 2 (gdscript):
```gdscript
var current_rotation

func _process(delta):
    if Input.is_action_just_pressed("animate"):
        current_rotation = get_quaternion()
        state_machine.travel("Animate")
    var velocity = current_rotation * animation_tree.get_root_motion_position() / delta
    set_velocity(velocity)
    move_and_slide()
```

Example 3 (gdscript):
```gdscript
func _process(delta):
    if Input.is_action_just_pressed("animate"):
        state_machine.travel("Animate")
    set_quaternion(get_quaternion() * animation_tree.get_root_motion_rotation())
    var velocity = (animation_tree.get_root_motion_rotation_accumulator().inverse() * get_quaternion()) * animation_tree.get_root_motion_position() / delta
    set_velocity(velocity)
    move_and_slide()
```

Example 4 (gdscript):
```gdscript
func _process(delta):
    if Input.is_action_just_pressed("animate"):
        state_machine.travel("Animate")
    set_quaternion(get_quaternion() * animation_tree.get_root_motion_rotation())
    var velocity = get_quaternion() * animation_tree.get_root_motion_position() / delta
    set_velocity(velocity)
    move_and_slide()
```

---

## AnimationTree — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/classes/class_animationtree.html

**Contents:**
- AnimationTree
- Description
- Tutorials
- Properties
- Methods
- Signals
- Enumerations
- Property Descriptions
- Method Descriptions
- User-contributed notes

Inherits: AnimationMixer < Node < Object

A node used for advanced animation transitions in an AnimationPlayer.

A node used for advanced animation transitions in an AnimationPlayer.

Note: When linked with an AnimationPlayer, several properties and methods of the corresponding AnimationPlayer will not function as expected. Playback and transitions should be handled using only the AnimationTree and its constituent AnimationNode(s). The AnimationPlayer node should be used solely for adding, deleting, and editing animations.

Third Person Shooter (TPS) Demo

advance_expression_base_node

AnimationCallbackModeDiscrete

callback_mode_discrete

2 (overrides AnimationMixer)

true (overrides AnimationMixer)

AnimationProcessCallback

get_process_callback() const

set_process_callback(mode: AnimationProcessCallback)

animation_player_changed() 🔗

Emitted when the anim_player is changed.

enum AnimationProcessCallback: 🔗

AnimationProcessCallback ANIMATION_PROCESS_PHYSICS = 0

Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS.

AnimationProcessCallback ANIMATION_PROCESS_IDLE = 1

Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE.

AnimationProcessCallback ANIMATION_PROCESS_MANUAL = 2

Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL.

NodePath advance_expression_base_node = NodePath(".") 🔗

void set_advance_expression_base_node(value: NodePath)

NodePath get_advance_expression_base_node()

The path to the Node used to evaluate the AnimationNode Expression if one is not explicitly specified internally.

NodePath anim_player = NodePath("") 🔗

void set_animation_player(value: NodePath)

NodePath get_animation_player()

The path to the AnimationPlayer used for animating.

AnimationRootNode tree_root 🔗

void set_tree_root(value: AnimationRootNode)

AnimationRootNode get_tree_root()

The root animation node of this AnimationTree. See AnimationRootNode.

AnimationProcessCallback get_process_callback() const 🔗

Deprecated: Use AnimationMixer.callback_mode_process instead.

Returns the process notification in which to update animations.

void set_process_callback(mode: AnimationProcessCallback) 🔗

Deprecated: Use AnimationMixer.callback_mode_process instead.

Sets the process notification in which to update animations.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---
