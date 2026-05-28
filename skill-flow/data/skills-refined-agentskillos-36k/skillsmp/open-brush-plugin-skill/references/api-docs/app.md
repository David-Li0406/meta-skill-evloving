
# App

## Summary
Various properties and methods that effect the entire app

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>time</td><td>number<br>Read-only</td><td>The time in seconds since Open Brush was launched</td></tr>
<tr><td>frames</td><td>number<br>Read-only</td><td>The number of frames that have been rendered since Open Brush was launched</td></tr>
<tr><td>physics</td><td>boolean<br>Read/Write</td><td>Whether physics simulation is active (defaults is off)</td></tr>
<tr><td>currentScale</td><td>number<br>Read-only</td><td>The current scale of the scene</td></tr>
<tr><td>environment</td><td>string<br>Read/Write</td><td>Get or set the current environment by name</td></tr>
<tr><td>clipboardText</td><td>string<br>Read/Write</td><td>Get or set the clipboard text</td></tr>
</tbody></table>




## Class Methods

        
### App:Undo()

Undo the last action

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:Undo()</strong></code></pre>




### App:Redo()

Redo the previously undone action

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:Redo()</strong></code></pre>




### App:AddListener(url)

Adds a url that should be sent the data for each stroke as soon as the user finishes drawing it

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>url</td><td>string</td><td></td><td>The url to send the stroke data to</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:AddListener("http://example.com")</strong></code></pre>




### App:ResetPanels()

Reset all panels

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:ResetPanels()</strong></code></pre>




### App:ShowScriptsFolder()

Opens an Explorer/Finder window outside of VR showing the user's Scripts folder on the desktop (Mac/Windows only)

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:ShowScriptsFolder()</strong></code></pre>




### App:ShowExportFolder()

Opens an Explorer/Finder window outside of VR showing the user's Export folder on the desktop (Mac/Windows only)

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:ShowExportFolder()</strong></code></pre>




### App:ShowSketchesFolder(index)

Opens an Explorer/Finder window outside of VR a folder containing a given sketch (Mac/Windows only)

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>index</td><td>number</td><td></td><td>The index of the sketch (0 being the most recent, then 1 and so on)</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:ShowSketchesFolder(index)</strong></code></pre>




### App:StraightEdge(active)

Activate or deactivate straight edge mode

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>True means activate, false means deactivate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:StraightEdge(true)</strong></code></pre>




### App:AutoOrient(active)

Activate or deactivate auto orientation mode

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>True means activate, false means deactivate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:AutoOrient(true)</strong></code></pre>




### App:ViewOnly(active)

Activate or deactivate view only mode

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>True means activate, false means deactivate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:ViewOnly(true)</strong></code></pre>




### App:AutoSimplify(active)

Activate or deactivate auto simplification mode

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>True means activate, false means deactivate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:AutoSimplify(true)</strong></code></pre>




### App:Disco(active)

Activate or deactivate disco mode

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>True means activate, false means deactivate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:Disco(true)</strong></code></pre>




### App:Profiling(active)

Activate or deactivate profiling mode

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>True means activate, false means deactivate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:Profiling(true)</strong></code></pre>




### App:PostProcessing(active)

Activate or deactivate post-processing

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>True means activate, false means deactivate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:PostProcessing(true)</strong></code></pre>




### App:DraftingVisible()

Set the drafting mode to visible

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:DraftingVisible()</strong></code></pre>




### App:DraftingTransparent()

Set the drafting mode to transparent

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:DraftingTransparent()</strong></code></pre>




### App:DraftingHidden()

Set the drafting mode to hidden

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:DraftingHidden()</strong></code></pre>




### App:Watermark(active)

Activate or deactivate the watermark

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>True means activate, false means deactivate</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:Watermark(true)</strong></code></pre>




### App:ReadFile(path)

Read the contents of a file

**Returns:** string  (The contents of the file as a string)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>path</td><td>string</td><td></td><td>The file path to read from. It must be relative to and contined within the Scripts folder</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:ReadFile("path/to/file.txt")</strong></code></pre>




### App:Error(message)

Displays an error message on the back of the user's brush controller

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>message</td><td>string</td><td></td><td>The error message to display</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:Error("This is an error message.")</strong></code></pre>




### App:SetFont(fontData)

Set the font used for drawing text

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>fontData</td><td>string</td><td></td><td>Font data in .chr format</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:SetFont("fontData")</strong></code></pre>




### App:TakeSnapshot(tr, filename, width, height, superSampling, renderDepth, removeBackground)

Take a snapshot of your scene and save it to your Snapshots folder

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>tr</td><td><a href="transform.md">Transform</a></td><td></td><td>Determines the position and orientation of the camera used to take the snapshot</td></tr>
<tr><td>filename</td><td>string</td><td></td><td>The filename to use for the saved snapshot</td></tr>
<tr><td>width</td><td>number</td><td></td><td>Image width</td></tr>
<tr><td>height</td><td>number</td><td></td><td>Image height</td></tr>
<tr><td>superSampling</td><td>number</td><td>1</td><td>The supersampling strength to apply (between 0.125 and 4.0)</td></tr>
<tr><td>renderDepth</td><td>boolean</td><td>false</td><td>If true then render the depth buffer instead of the image</td></tr>
<tr><td>removeBackground</td><td>boolean</td><td>false</td><td></td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:TakeSnapshop(Transform:New(0, 12, 3), "mysnapshot.png", 1024, 768, true)</strong></code></pre>




### App:Take360Snapshot(tr, filename, width)

Take a 360-degree snapshot of the scene and save it

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>tr</td><td><a href="transform.md">Transform</a></td><td></td><td>Determines the position and orientation of the camera used to take the snapshot</td></tr>
<tr><td>filename</td><td>string</td><td></td><td>The filename to use for the saved snapshot</td></tr>
<tr><td>width</td><td>number</td><td>4096</td><td>The width of the image</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>App:Take360Snapshot(Transform:Position(0, 12, 3), "my360snapshot.png", 4096)</strong></code></pre>



    

