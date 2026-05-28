
# Symmetry

## Summary
Functions for controlling the mirror symmetry mode

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>current</td><td><a href="symmetrysettings.md">SymmetrySettings</a><br>Read/Write</td><td>The current symmetry settings</td></tr>
<tr><td>brushOffset</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>Gets the offset between the current brush position and the symmetry widget</td></tr>
<tr><td>wandOffset</td><td><a href="vector3.md">Vector3</a><br>Read-only</td><td>Gets the offset between the current wand position and the symmetry widget</td></tr>
</tbody></table>




## Class Methods

        
### Symmetry:SummonWidget()

Moves the Symmetry Widget close to user

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:SummonWidget()</strong></code></pre>




### Symmetry:Ellipse(angle, minorRadius)

Returns the radius of an ellipse at a given angle

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>angle</td><td>number</td><td></td><td>The angle in degrees to sample the radius at</td></tr>
<tr><td>minorRadius</td><td>number</td><td></td><td>The minor radius of the ellipse (The major radius is always 1)</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>for i = 0, 90 do
  radius = Symmetry:Ellipse(i * 4, 0.5)
  pointer = Transform:New(Symmetry.brushOffset:ScaleBy(radius, 1, radius))
  pointers:Insert(pointer)
end</strong></code></pre>




### Symmetry:Square(angle)

Returns the radius of an square at a given angle

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>angle</td><td>number</td><td></td><td>The angle in degrees to sample the radius at</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>for i = 0, 90 do
  radius = Symmetry:Square(i * 4)
  pointer = Transform:New(Symmetry.brushOffset:ScaleBy(radius, 1, radius))
  pointers:Insert(pointer)
end</strong></code></pre>




### Symmetry:Superellipse(angle, n, a, b)

Returns the radius of a superellipse at a given angle

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>angle</td><td>number</td><td></td><td>The angle in degrees to sample the radius at</td></tr>
<tr><td>n</td><td>number</td><td></td><td>The exponent of the superellipse. This determines the roundness vs sharpness of the corners of the superellipse. For n = 2, you get an ellipse. As n increases, the shape becomes more rectangular with sharper corners. As n approaches infinity, the superellipse becomes a rectangle. If n is less than 1, the shape becomes a star with pointed tips.</td></tr>
<tr><td>a</td><td>number</td><td>1</td><td>The horizontal radius of the superellipse</td></tr>
<tr><td>b</td><td>number</td><td>1</td><td>The vertical radius of the superellipse</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>for i = 0, 90 do
  radius = Symmetry:Superellipse(i * 4, 2, 0.5, 0.5)
  pointer = Transform:New(Symmetry.brushOffset:ScaleBy(radius, 1, radius))
  pointers:Insert(pointer)
end</strong></code></pre>




### Symmetry:Rsquare(angle, size, cornerRadius)

Returns the radius of a rounded square at a given angle

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>angle</td><td>number</td><td></td><td>The angle in degrees to sample the radius at</td></tr>
<tr><td>size</td><td>number</td><td></td><td>Half the length of a side or the distance from the center to any edge midpoint</td></tr>
<tr><td>cornerRadius</td><td>number</td><td></td><td>The radius of the rounded corners</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>for i = 0, 90 do
  radius = Symmetry:Rsquare(i * 4, 0.5, 0.1)
  pointer = Transform:New(Symmetry.brushOffset:ScaleBy(radius, 1, radius))
  pointers:Insert(pointer)
end</strong></code></pre>




### Symmetry:Polygon(angle, numSides, radius)

Returns the radius of a polygon at a given angle

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>angle</td><td>number</td><td></td><td>The angle in degrees to sample the radius at</td></tr>
<tr><td>numSides</td><td>number</td><td></td><td>The number of sides of the polygon</td></tr>
<tr><td>radius</td><td>number</td><td>1</td><td>The distance from the center to any vertex</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>for i = 0, 90 do
  radius = Symmetry:Polygon(i * 4, 5, 0.5)
  pointer = Transform:New(Symmetry.brushOffset:ScaleBy(radius, 1, radius))
  pointers:Insert(pointer)
end</strong></code></pre>




### Symmetry:ClearColors()

Clears the list of symmetry pointer colors

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:ClearColors()</strong></code></pre>




### Symmetry:AddColor(color)

Adds a color to the list of symmetry pointer colors

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>color</td><td><a href="color.md">Color</a></td><td></td><td>The color to add</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:AddColor(Color.red)</strong></code></pre>




### Symmetry:SetColors(color)

Sets all symmetry pointer colors to a single color

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>color</td><td><a href="color.md">Color</a></td><td></td><td>The color to set</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:SetColors(Color.red)</strong></code></pre>




### Symmetry:SetColors(colors)

Sets the list of symmetry pointer colors

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>colors</td><td>Color[]</td><td></td><td>The list of colors to set</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:SetColors({Color.red, Color.green, Color.blue})</strong></code></pre>




### Symmetry:GetColors()

Gets the list of symmetry pointer colors

**Returns:** Color[] 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myColors = Symmetry:GetColors()</strong></code></pre>




### Symmetry:AddBrush(brush)

Adds a brush to the list of symmetry pointer brushes

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>brush</td><td>string</td><td></td><td>The brush to add. Either the name or the GUID of the brush</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:AddBrush("Ink")</strong></code></pre>




### Symmetry:ClearBrushes()

Clears the list of symmetry pointer brushes

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:ClearBrushes()</strong></code></pre>




### Symmetry:SetBrushes(brushes)

Sets the list of symmetry pointer brushes

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>brushes</td><td>string[]</td><td></td><td>The list of brushes to set. Either the names or the GUIDs of the brushes</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:SetBrushes({"Ink", "Marker"})</strong></code></pre>




### Symmetry:SetColorOverrides(color)

Sets the override color for all symmetry pointer brushes

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>color</td><td><a href="color.md">Color</a></td><td></td><td>The color to set</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:SetColorOverrides(Color.red)</strong></code></pre>




### Symmetry:SetColorOverrideModes(mode)

Sets the override color mode for all symmetry pointer brushes

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>mode</td><td><a href="coloroverridemode.md">ColorOverrideMode</a></td><td></td><td>The mode to set</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:SetColorOverrideModes(ColorOverrideMode.Blend)</strong></code></pre>




### Symmetry:ClearColorOverrides()

Clears the list of symmetry pointer override colors

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:ClearColorOverride()</strong></code></pre>




### Symmetry:GetBrushNames()

Gets the list of symmetry pointer brushes as brush names

**Returns:** string[] 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>brushNames = Symmetry:GetBrushNames()</strong></code></pre>




### Symmetry:GetBrushGuids()

Gets the list of symmetry pointer brushes as brush GUIDs

**Returns:** string[] 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>brushGuids = Symmetry:GetBrushGuids()</strong></code></pre>




### Symmetry:PathToPolar(path)

Converts a path to a format suitable for using as a symmetry path in polar mode

**Returns:** <a href="path.md">Path</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>path</td><td><a href="path.md">Path</a></td><td></td><td>The path to convert</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>pointers = Symmetry:PathToPolar(myPath):OnY()</strong></code></pre>




### Symmetry:SetPointerPaintMode(pointerIndex, mode)

Sets the painting override for a scripted pointer.

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>pointerIndex</td><td>number</td><td></td><td>Zero-based pointer index matching the transform order returned by the symmetry script.</td></tr>
<tr><td>mode</td><td><a href="symmetrypointerpaintmode.md">SymmetryPointerPaintMode</a></td><td></td><td>The override to apply to the pointer.</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:SetPointerPaintMode(0, SymmetryPointerPaintMode.ForcedOn)</strong></code></pre>




### Symmetry:GetPointerPaintMode(pointerIndex)

Gets the current painting override for a scripted pointer.

**Returns:** <a href="symmetrypointerpaintmode.md">SymmetryPointerPaintMode</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>pointerIndex</td><td>number</td><td></td><td>Zero-based pointer index matching the transform order returned by the symmetry script.</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>local mode = Symmetry:GetPointerPaintMode(0)</strong></code></pre>




### Symmetry:GetPointerPaintModes()

Returns the painting overrides for all active scripted pointers.

**Returns:** <a href="system.collections.generic.list`1[symmetrypointerpaintmode].md">System.Collections.Generic.List`1[SymmetryPointerPaintMode]</a> 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>for i, mode in ipairs(Symmetry:GetPointerPaintModes()) do
  print(i, mode)
end</strong></code></pre>




### Symmetry:StartPointer(pointerIndex)

Convenience helper that forces a scripted pointer to start painting.

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>pointerIndex</td><td>number</td><td></td><td>Zero-based pointer index matching the transform order returned by the symmetry script.</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:StartPointer(1)</strong></code></pre>




### Symmetry:StopPointer(pointerIndex)

Convenience helper that forces a scripted pointer to stop painting.

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>pointerIndex</td><td>number</td><td></td><td>Zero-based pointer index matching the transform order returned by the symmetry script.</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:StopPointer(1)</strong></code></pre>




### Symmetry:ForcePointerNewStroke(pointerIndex)

Detaches the current stroke for a scripted pointer and immediately begins a new one if the pointer remains enabled.

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>pointerIndex</td><td>number</td><td></td><td>Zero-based pointer index matching the transform order returned by the symmetry script.</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Symmetry:ForcePointerNewStroke(0)</strong></code></pre>




### Symmetry:ApplyToPath(path)

Creates multiple copies of a path based on the current symmetry settings

**Returns:** <a href="pathlist.md">PathList</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>path</td><td><a href="path.md">Path</a></td><td></td><td>The path to duplicate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>pathList = Symmetry:ApplyToPath(myPath)</strong></code></pre>



    

