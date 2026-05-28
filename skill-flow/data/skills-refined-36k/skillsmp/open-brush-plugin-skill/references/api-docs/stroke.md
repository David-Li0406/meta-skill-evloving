
# Stroke

## Summary
A specific brush stroke


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>path</td><td><a href="path.md">Path</a><br>Read/Write</td><td>The control points of this stroke from a Path</td></tr>
<tr><td>brushType</td><td>string<br>Read/Write</td><td>The stroke's brush type</td></tr>
<tr><td>brushSize</td><td>number<br>Read/Write</td><td>The stroke's size</td></tr>
<tr><td>brushColor</td><td><a href="color.md">Color</a><br>Read/Write</td><td>The stroke's Color</td></tr>
<tr><td>layer</td><td><a href="layer.md">Layer</a><br>Read/Write</td><td>The layer the stroke is on</td></tr>
<tr><td>group</td><td><a href="group.md">Group</a><br>Read/Write</td><td>The group this stroke is part of</td></tr>
<tr><td>this[index]</td><td><a href="transform.md">Transform</a><br>Read/Write</td><td>Gets or sets a control point by index</td></tr>
<tr><td>count</td><td>number<br>Read-only</td><td>The number of control points in this stroke</td></tr>
</tbody></table>



## Class Methods

        
### Stroke:SelectRange(from, to)

Adds multiple strokes to the current selection

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>from</td><td>number</td><td></td><td>Start stroke index (0 is the first stroke that was drawn</td></tr>
<tr><td>to</td><td>number</td><td></td><td>End stroke index</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Stroke:SelectMultiple(0, 4) --Adds the first 5 strokes on the sketch</strong></code></pre>



    

## Instance Methods

        
### stroke:ChangeMaterial(brushName)

Assigns the material from another brush type to this stroke (Experimental. Results are unpredictable and are not saved with the scene)

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>brushName</td><td>string</td><td></td><td>The name (or guid) of the brush to get the material from</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStroke.ChangeMaterial("Light")</strong></code></pre>




### stroke:Delete()

Deletes the current stroke

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStroke:Delete()</strong></code></pre>




### stroke:Select()

Adds this stroke to the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStroke:Select()</strong></code></pre>




### stroke:Deselect()

Removes this stroke from the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStroke:Deselect()</strong></code></pre>




### stroke:JoinRange(from, to)

Joins joins multiple strokes into one stroke

**Returns:** <a href="stroke.md">Stroke</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>from</td><td>number</td><td></td><td>Start stroke index (0 is the first stroke that was drawn</td></tr>
<tr><td>to</td><td>number</td><td></td><td>End stroke index</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newStroke = Stroke:Join(0, 10)</strong></code></pre>




### stroke:JoinToPrevious()

Joins a stroke with the previous stroke

**Returns:** <a href="stroke.md">Stroke</a> 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newStroke = myStroke:JoinPrevious()</strong></code></pre>




### stroke:Join(stroke2)

Joins a stroke with the previous stroke

**Returns:** <a href="stroke.md">Stroke</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>stroke2</td><td><a href="stroke.md">Stroke</a></td><td></td><td>The stroke to join to this one</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newStroke = myStroke:JoinPrevious()</strong></code></pre>




### stroke:MergeFrom(name)

Imports the file with the specified name from the user's Sketches folder and merges it's strokes into the current sketch

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>name</td><td>string</td><td></td><td>Name of the file to be merged</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Stroke:MergeFrom(string name)</strong></code></pre>




### stroke:SetShaderClipping(clipStart, clipEnd)

Hides the section of the stroke that is outside the specified range

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>clipStart</td><td>number</td><td></td><td>The amount of the stroke to hide from the start (0-1)</td></tr>
<tr><td>clipEnd</td><td>number</td><td></td><td>The amount of the stroke to hide from the end (0-1)</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStroke:SetShaderClipping(0.1, 0.9)</strong></code></pre>




### stroke:SetShaderFloat(parameter, value)

Changes a shader float parameter

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>parameter</td><td>string</td><td></td><td>The shader parameter name</td></tr>
<tr><td>value</td><td>number</td><td></td><td>The new value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStroke:SetShaderFloat("_EmissionGain", 0.5)</strong></code></pre>




### stroke:SetShaderColor(parameter, color)

Changes a shader color parameter

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>parameter</td><td>string</td><td></td><td>The shader parameter name</td></tr>
<tr><td>color</td><td><a href="color.md">Color</a></td><td></td><td>The new color</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStroke:SetShaderColor("_TintColor", Color.red)</strong></code></pre>




### stroke:SetShaderTexture(parameter, image)

Changes a shader texture parameter

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>parameter</td><td>string</td><td></td><td>The shader parameter name</td></tr>
<tr><td>image</td><td><a href="image.md">Image</a></td><td></td><td>The new image to use as a texture</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myStroke:SetShaderTexture("_MainTex", myImage)</strong></code></pre>




### stroke:SetShaderVector(parameter, x, y, z, w)

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

<pre class="language-lua"><code class="lang-lua"><strong>myStroke:SetShaderVector("_TimeOverrideValue", 0.5, 0, 0, 0)</strong></code></pre>



    
