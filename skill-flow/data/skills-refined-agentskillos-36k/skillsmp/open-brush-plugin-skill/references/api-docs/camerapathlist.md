
# CameraPathList

## Summary
The list of Camera Paths in the scene. (You don't instantiate this yourself. Access this via Sketch.cameraPaths)


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>last</td><td><a href="camerapath.md">CameraPath</a><br>Read-only</td><td>Returns the last Camera Path</td></tr>
<tr><td>this[index]</td><td><a href="camerapath.md">CameraPath</a><br>Read/Write</td><td>Gets a Camera Path by it's index</td></tr>
<tr><td>count</td><td>number<br>Read-only</td><td>The number of Camera Paths</td></tr>
<tr><td>active</td><td><a href="camerapath.md">CameraPath</a><br>Read/Write</td><td>The active Camera Path</td></tr>
</tbody></table>




## Instance Methods

        
### cameraPathList:ShowAll()

Makes all Camera Paths visible

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Sketch.cameraPaths:ShowAll()</strong></code></pre>




### cameraPathList:HideAll()

Hides all Camera Paths

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Sketch:cameraPaths:HideAll()</strong></code></pre>




### cameraPathList:PreviewActivePath(active)

Sets whether to preview the active path or not

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>active</td><td>boolean</td><td></td><td>A boolean value indicating whether to preview the active path or not</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Sketch.cameraPaths:PreviewActivePath(true)</strong></code></pre>



    
