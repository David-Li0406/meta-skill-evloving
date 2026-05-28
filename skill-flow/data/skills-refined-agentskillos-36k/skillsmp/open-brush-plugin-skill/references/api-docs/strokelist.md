
# StrokeList

## Summary
The list of Strokes in the scene. (You don't instantiate this yourself. Access this via Sketch.strokes)


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>lastSelected</td><td><a href="stroke.md">Stroke</a><br>Read-only</td><td>Returns the last stroke that was selected</td></tr>
<tr><td>last</td><td><a href="stroke.md">Stroke</a><br>Read-only</td><td>Returns the last Stroke</td></tr>
<tr><td>this[index]</td><td><a href="stroke.md">Stroke</a><br>Read-only</td><td>Returns the Stroke at the given index</td></tr>
<tr><td>count</td><td>number<br>Read-only</td><td>The number of strokes</td></tr>
</tbody></table>




## Instance Methods

        
### strokeList:Select()

Adds these strokes to the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStrokes:Select()</strong></code></pre>




### strokeList:Deselect()

Removes these strokes from the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStrokes:Deselect()</strong></code></pre>




### strokeList:Delete()

Deletes all the strokes in the list

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStrokes:Delete()</strong></code></pre>




### strokeList:SetShaderClipping(clipStart, clipEnd)

Hides the section of the stroke that is outside the specified range

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>clipStart</td><td>number</td><td></td><td>The amount of the stroke to hide from the start (0-1)</td></tr>
<tr><td>clipEnd</td><td>number</td><td></td><td>The amount of the stroke to hide from the end (0-1)</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStroke:SetShaderClipping(0.1, 0.9)</strong></code></pre>




### strokeList:SetShaderFloat(parameter, value)

Changes a shader float parameter.

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>parameter</td><td>string</td><td></td><td>The shader parameter name</td></tr>
<tr><td>value</td><td>number</td><td></td><td>The new value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStrokes:SetShaderFloat("_EmissionGain", 0.5)</strong></code></pre>




### strokeList:SetShaderColor(parameter, color)

Changes a shader color parameter

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>parameter</td><td>string</td><td></td><td>The shader parameter name</td></tr>
<tr><td>color</td><td><a href="color.md">Color</a></td><td></td><td>The new color</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStrokes:SetShaderColor("_TintColor", Color.red)</strong></code></pre>




### strokeList:SetShaderTexture(parameter, image)

Changes a shader texture parameter

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>parameter</td><td>string</td><td></td><td>The shader parameter name</td></tr>
<tr><td>image</td><td><a href="image.md">Image</a></td><td></td><td>The new image to use as a texture</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStrokes:SetShaderTexture("_MainTex", myImage)</strong></code></pre>




### strokeList:SetShaderVector(parameter, x, y, z, w)

Changes a shader vector parameter

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>parameter</td><td>string</td><td></td><td>The shader parameter name</td></tr>
<tr><td>x</td><td>number</td><td></td><td>The new x value</td></tr>
<tr><td>y</td><td>number</td><td>0</td><td>The new y value</td></tr>
<tr><td>z</td><td>number</td><td>0</td><td>The new z value</td></tr>
<tr><td>w</td><td>number</td><td>0</td><td>The new w value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStrokes:SetShaderVector("_TimeOverrideValue", 0.5, 0, 0, 0)</strong></code></pre>



    
