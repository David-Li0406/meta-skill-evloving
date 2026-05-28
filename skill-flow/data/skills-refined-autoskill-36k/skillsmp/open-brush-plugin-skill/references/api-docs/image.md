
# Image

## Summary
An image widget


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>index</td><td>number<br>Read-only</td><td>The index of the active widget</td></tr>
<tr><td>layer</td><td><a href="layer.md">Layer</a><br>Read/Write</td><td>The layer the image is on</td></tr>
<tr><td>group</td><td><a href="group.md">Group</a><br>Read/Write</td><td>The group this image is part of</td></tr>
<tr><td>transform</td><td><a href="transform.md">Transform</a><br>Read/Write</td><td>The transform of the image widget</td></tr>
<tr><td>position</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>The 3D position of the Image Widget</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>The 3D orientation of the Image Widget</td></tr>
<tr><td>scale</td><td>number<br>Read/Write</td><td>The scale of the image widget</td></tr>
<tr><td>visible</td><td>boolean<br>Read/Write</td><td>Whether the widget is visible or not</td></tr>
<tr><td>aspect</td><td>number<br>Read-only</td><td>The aspect ration of the image</td></tr>
<tr><td>filename</td><td>string<br>Read-only</td><td>The filename of the image</td></tr>
</tbody></table>



## Class Methods

        
### Image:Import(filename)

Imports an image widget based on the specified filename

**Returns:** <a href="image.md">Image</a>  (The imported image widget)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>filename</td><td>string</td><td></td><td>The filename of the image</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Image:Import("test.png")</strong></code></pre>



    

## Instance Methods

        
### image:GetPixel(x, y)

Get a pixel color from the image

**Returns:** <a href="color.md">Color</a>  (The pixel color)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The y coordinate of the pixel</td></tr>
<tr><td>y</td><td>number</td><td></td><td></td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myColor = myImage:GetPixel(10, 20)</strong></code></pre>




### image:Select()

Selects the image widget

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myImage:Select()</strong></code></pre>




### image:Deselect()

Removes the image from the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myImage:Deselect()</strong></code></pre>




### image:Delete()

Deletes the image widget

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myImage:Delete()</strong></code></pre>




### image:Extrude(depth, color)

Extrudes the image widget with the specified depth and color

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>depth</td><td>number</td><td></td><td>The depth of the extrusion</td></tr>
<tr><td>color</td><td><a href="color.md">Color</a></td><td></td><td>The color of the extrusion</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Image:Extrude(5, Color.green)</strong></code></pre>




### image:FormEncode()

Encodes the image as a form

**Returns:** string  (The encoded image so it can be submitted as a response to a HTML form)




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>formdata = myImage:FormEncode()</strong></code></pre>




### image:SaveBase64(base64, filename)

Saves an image as a png based on base64 data

**Returns:** string 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>base64</td><td>string</td><td></td><td>The base64 data for the image</td></tr>
<tr><td>filename</td><td>string</td><td></td><td>The filename to save as</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Image:SaveBase64(someData, "image.png")</strong></code></pre>



    
