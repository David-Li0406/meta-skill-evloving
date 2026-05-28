
# Brush

## Summary
The user's brush

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>timeSincePressed</td><td>number<br>Read-only</td><td>Time in seconds since the brush trigger was last pressed</td></tr>
<tr><td>timeSinceReleased</td><td>number<br>Read-only</td><td>Time in seconds since the brush trigger was last released</td></tr>
<tr><td>triggerIsPressed</td><td>boolean<br>Read-only</td><td>Check whether the brush trigger is currently pressed</td></tr>
<tr><td>triggerPressedThisFrame</td><td>boolean<br>Read-only</td><td>Check whether the brush trigger was pressed during the current frame</td></tr>
<tr><td>triggerReleasedThisFrame</td><td>boolean<br>Read-only</td><td>Check whether the brush trigger was released during the current frame</td></tr>
<tr><td>button1IsPressed</td><td>boolean<br>Read-only</td><td>Check whether the brush button 1 is currently pressed</td></tr>
<tr><td>button1PressedThisFrame</td><td>boolean<br>Read-only</td><td>Check whether the brush button 1 was pressed during the current frame</td></tr>
<tr><td>button2IsPressed</td><td>boolean<br>Read-only</td><td>Check whether the brush button 2 is currently pressed</td></tr>
<tr><td>button2PressedThisFrame</td><td>boolean<br>Read-only</td><td>Check whether the brush button 2 was pressed during the current frame</td></tr>
<tr><td>distanceMoved</td><td>number<br>Read-only</td><td>The distance moved by the brush</td></tr>
<tr><td>distanceDrawn</td><td>number<br>Read-only</td><td>The distance drawn by the brush (i.e. distance since the trigger was last pressed)</td></tr>
<tr><td>position</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>The 3D position of the Brush Controller's tip</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>The 3D orientation of the Brush Controller's tip</td></tr>
<tr><td>direction</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>The vector representing the forward direction of the brush</td></tr>
<tr><td>size</td><td>number<br>Read/Write</td><td>The current brush size</td></tr>
<tr><td>pressure</td><td>number<br>Read/Write</td><td>Brush pressure is determined by how far the trigger is pressed in</td></tr>
<tr><td>type</td><td>string<br>Read/Write</td><td>The current brush type</td></tr>
<tr><td>types</td><td>string[]<br>Read-only</td><td>All brush types available via the UI</td></tr>
<tr><td>speed</td><td>number<br>Read-only</td><td>How fast the brush is currently moving</td></tr>
<tr><td>colorRgb</td><td><a href="color.md">Color</a><br>Read/Write</td><td>Gets or set brush color</td></tr>
<tr><td>colorHsv</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>Gets or set brush color using a Vector3 representing hue, saturation and brightness</td></tr>
<tr><td>colorHtml</td><td>string<br>Read/Write</td><td>The color of the brush as a valid HTML color string (either hex values or a color name)</td></tr>
<tr><td>lastColorPicked</td><td><a href="color.md">Color</a><br>Read-only</td><td>The last color picked by the brush.</td></tr>
<tr><td>LastColorPickedHsv</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>The last color picked by the brush in HSV.</td></tr>
<tr><td>currentPath</td><td><a href="path.md">Path</a><br>Read/Write</td><td>The current path of the brush. Assumes a stroke is in progress.</td></tr>
</tbody></table>




## Class Methods

        
### Brush:GetTypes(includeTags, excludeTags)

Brush types filtered by chosen tags

**Returns:** string[]  (A filtered list of brush types)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>includeTags</td><td>string[]</td><td></td><td>Include brushes that have any of these tags</td></tr>
<tr><td>excludeTags</td><td>string[]</td><td></td><td>Exclude brushes that have any of these tags</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>brushList = Brush:GetTypes({"audioreactive"}, {"particle"})</strong></code></pre>




### Brush:JitterColor()

Applies the current jitter settings to the brush color

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:JitterColor()</strong></code></pre>




### Brush:SetColorOverride(color)

Sets the brush override color

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>color</td><td><a href="color.md">Color</a></td><td></td><td>The color to set</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:SetColorOverride(Color.red)</strong></code></pre>




### Brush:SetColorOverrideMode(mode)

Sets the brush override color mode

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>mode</td><td><a href="coloroverridemode.md">ColorOverrideMode</a></td><td></td><td>The mode to set</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:SetColorOverrideMode(ColorOverrideMode.Blend)</strong></code></pre>




### Brush:ResizeHistory(size)

Clears the history and sets it's size

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>size</td><td>number</td><td></td><td>How many frames of position/rotation to remember</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:ResizeHistory(10)</strong></code></pre>




### Brush:SetHistorySize(size)

Sets the size of the history. Only clears it if the size has changed

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>size</td><td>number</td><td></td><td>How many frames of position/rotation to remember</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:SetHistorySize(10)</strong></code></pre>




### Brush:GetPastPosition(back)

Recalls previous positions of the Brush from the history buffer

**Returns:** <a href="vector3.md">Vector3</a>  (The position of the brush during the specified frame)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>back</td><td>number</td><td></td><td>How many frames back in the history to look</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:GetPastPosition(3)</strong></code></pre>




### Brush:GetPastRotation(back)

Recalls previous orientations of the Brush from the history buffer

**Returns:** <a href="rotation.md">Rotation</a>  (The rotation of the brush during the specified frame)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>back</td><td>number</td><td></td><td>How many frames back in the history to look</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:GetPastRotation(3)</strong></code></pre>




### Brush:ForcePaintingOn(active)

If set to true then the brush will draw strokes even if the trigger isn't being pressed.

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>True means forced painting, false is normal behaviour</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:ForcePaintingOn(true)</strong></code></pre>




### Brush:ForcePaintingOff(active)

If set to true then the brush will stop drawing strokes even if the trigger is still pressed.

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>True means painting is forced off, false is normal behaviour</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:ForcePaintingOff(true)</strong></code></pre>




### Brush:ForceNewStroke()

Forces the start of a new stroke - will stop painting this frame and start again the next.

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:ForceNewStroke()</strong></code></pre>




### Brush:GetShaderFloatParameters(type)

Gets a list of float property names for a brush

**Returns:** string[]  (A list of float property names usable with Stroke:SetShaderFloat)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>type</td><td>string</td><td></td><td>The brush name</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:GetShaderFloatParameters("Ink")</strong></code></pre>




### Brush:GetShaderColorParameters(type)

Gets a list of color property names for a brush

**Returns:** string[]  (A list of color property names usable with Stroke:SetShaderColor)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>type</td><td>string</td><td></td><td>The brush name</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:GetShaderColorParameters("Ink")</strong></code></pre>




### Brush:GetShaderTextureParameters(type)

Gets a list of texture property names for a brush

**Returns:** string[]  (A list of texture property names usable with Stroke:SetShaderTexture)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>type</td><td>string</td><td></td><td>The brush name</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:GetShaderTextureParameters("Ink")</strong></code></pre>




### Brush:GetShaderVectorParameters(type)

Gets a list of vector property names for a brush

**Returns:** string[]  (A list of vector property names usable with Stroke:SetShaderVector)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>type</td><td>string</td><td></td><td>The brush name</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Brush:GetShaderVectorParameters("Ink")</strong></code></pre>



    

