
# Sketch

## Summary
Represents the current sketch

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>cameraPaths</td><td><a href="camerapathlist.md">CameraPathList</a><br>Read-only</td><td>Returns a list of active camera paths in the sketch</td></tr>
<tr><td>strokes</td><td><a href="strokelist.md">StrokeList</a><br>Read-only</td><td>Returns a list of all active strokes in the sketch</td></tr>
<tr><td>layers</td><td><a href="layerlist.md">LayerList</a><br>Read-only</td><td>Returns a list of all layers in the sketch</td></tr>
<tr><td>mainLayer</td><td><a href="layer.md">Layer</a><br>Read-only</td><td>Returns a list of all layers in the sketch</td></tr>
<tr><td>groups</td><td><a href="grouplist.md">GroupList</a><br>Read-only</td><td>All the groups in this sketch</td></tr>
<tr><td>images</td><td><a href="imagelist.md">ImageList</a><br>Read-only</td><td>Returns a list of active image widgets in the sketch</td></tr>
<tr><td>videos</td><td><a href="videolist.md">VideoList</a><br>Read-only</td><td>Returns a list of active video widgets in the sketch</td></tr>
<tr><td>models</td><td><a href="modellist.md">ModelList</a><br>Read-only</td><td>Returns a list of active model widgets in the sketch</td></tr>
<tr><td>guides</td><td><a href="guidelist.md">GuideList</a><br>Read-only</td><td>Returns a list of active stencil widgets in the sketch</td></tr>
<tr><td>environments</td><td><a href="environmentlist.md">EnvironmentList</a><br>Read-only</td><td>Returns a list of all the available environments</td></tr>
<tr><td>ambientLightColor</td><td><a href="color.md">Color</a><br>Read/Write</td><td>The ambient light color</td></tr>
<tr><td>mainLightColor</td><td><a href="color.md">Color</a><br>Read/Write</td><td>The main light's color</td></tr>
<tr><td>secondaryLightColor</td><td><a href="color.md">Color</a><br>Read/Write</td><td>The secondary light's color</td></tr>
<tr><td>mainLightRotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>The main light's rotation</td></tr>
<tr><td>secondaryLightRotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>The secondary light's rotation</td></tr>
</tbody></table>




## Class Methods

        
### Sketch:Open(name)

Opens a sketch with the specified name in the User's Sketches folder

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>name</td><td>string</td><td></td><td>The filename of the sketch</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Sketch:Open("MySketch.tilt")</strong></code></pre>




### Sketch:Save(overwrite)

Saves the current sketch, possibly overwriting an existing one

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>overwrite</td><td>boolean</td><td></td><td>If set to true, overwrite the existing file. If false, the method will not overwrite the file</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Sketch:Save(overwrite)</strong></code></pre>




### Sketch:SaveAs(name)

Saves the current sketch with a new name

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>name</td><td>string</td><td></td><td>The new name for the sketch</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Sketch:SaveAs("NewName.tilt")</strong></code></pre>




### Sketch:Export()

Exports the sketch in all supported export formats

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Sketch:Export()</strong></code></pre>




### Sketch:NewSketch()

Creates a new sketch

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Sketch:NewSketch()</strong></code></pre>




### Sketch:ImportSkybox(filename)

Imports a image with the specified name from the MediaLibrary/BackgroundImages folder and assigns it as a custom skybox

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>filename</td><td>string</td><td></td><td>The filename of the image</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:ImportSkybox("landscape.hdr")</strong></code></pre>



    

