
# Wand

## Summary
Represents the user's wand (the controller that isn't the brush controller)

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>position</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>The 3D position of the Wand Controller</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read-only</td><td>The 3D orientation of the Wand</td></tr>
<tr><td>direction</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>The vector representing the forward direction of the wand controller</td></tr>
<tr><td>pressure</td><td>number<br>Read-only</td><td>How far the trigger on the wand contrller is pressed in</td></tr>
<tr><td>speed</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>How fast the wand controller is currently moving</td></tr>
<tr><td>triggerIsPressed</td><td>boolean<br>Read-only</td><td>Check whether the wand trigger is currently pressed</td></tr>
<tr><td>triggerPressedThisFrame</td><td>boolean<br>Read-only</td><td>Check whether the wand trigger was pressed during the current frame</td></tr>
<tr><td>triggerReleasedThisFrame</td><td>boolean<br>Read-only</td><td>Check whether the wand trigger was released during the current frame</td></tr>
<tr><td>timeSincePressed</td><td>number<br>Read-only</td><td>Time in seconds since the wand trigger was last pressed</td></tr>
<tr><td>timeSinceReleased</td><td>number<br>Read-only</td><td>Time in seconds since the wand trigger was last released</td></tr>
<tr><td>distanceMoved</td><td>number<br>Read-only</td><td>The distance moved by the wand</td></tr>
<tr><td>distanceDrawn</td><td>number<br>Read-only</td><td>The distance drawn by the wand (i.e. distance since the trigger was last pressed)</td></tr>
</tbody></table>




## Class Methods

        
### Wand:ResizeHistory(size)

Clears the history and sets it's size

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>size</td><td>number</td><td></td><td>The size of the history buffer</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Wand.ResizeHistory(100)</strong></code></pre>




### Wand:SetHistorySize(size)

Sets the size of the history. Only clears it if the size has changed

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>size</td><td>number</td><td></td><td>The size of the history buffer</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Wand.SetHistorySize(100)</strong></code></pre>




### Wand:PastPosition(back)

Recalls previous positions of the Wand from the history buffer

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>back</td><td>number</td><td></td><td>How far back in the history to get the position from</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPosition = Wand.PastPosition(5)</strong></code></pre>




### Wand:PastRotation(back)

Recalls previous orientations of the Wand from the history buffer

**Returns:** <a href="rotation.md">Rotation</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>back</td><td>number</td><td></td><td>How far back in the history to get the rotation from</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myRotation = Wand.PastRotation(5)</strong></code></pre>



    

