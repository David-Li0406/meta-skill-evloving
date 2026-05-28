
# Pointer

## Summary
An independently controllable brush that can paint independently of user actions


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>isDrawing</td><td>boolean<br>Read/Write</td><td>True if the pointer is currently drawing a stroke, otherwise false</td></tr>
<tr><td>layer</td><td><a href="layer.md">Layer</a><br>Read/Write</td><td>Sets the layer that the pointer will draw on. Must be set before starting a new stroke</td></tr>
<tr><td>color</td><td><a href="color.md">Color</a><br>Read/Write</td><td>Sets the color of the strokes created by this pointer. Must be set before starting a new stroke</td></tr>
<tr><td>brush</td><td>string<br>Read/Write</td><td>Sets the brush type the pointer will draw. Must be set before starting a new stroke</td></tr>
<tr><td>size</td><td>number<br>Read/Write</td><td>Sets the size of the brush strokes this pointer will draw. Must be set before starting a new stroke</td></tr>
<tr><td>pressure</td><td>number<br>Read/Write</td><td>Sets the pressure of the stroke being drawn</td></tr>
<tr><td>transform</td><td><a href="transform.md">Transform</a><br>Read/Write</td><td>The position and orientation of the pointer</td></tr>
<tr><td>position</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>The 3D position of this pointer</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>The 3D orientation of the Pointer</td></tr>
</tbody></table>



## Class Methods

        
### Pointer:New()

Creates a new pointer for drawing

**Returns:** <a href="pointer.md">Pointer</a>  (The new pointer)




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Pointer:New()</strong></code></pre>



    

