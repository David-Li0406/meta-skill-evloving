
# Video

## Summary
A video widget


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>index</td><td>number<br>Read-only</td><td>Gets the index of this Video</td></tr>
<tr><td>layer</td><td><a href="layer.md">Layer</a><br>Read/Write</td><td>The layer the video is on</td></tr>
<tr><td>group</td><td><a href="group.md">Group</a><br>Read/Write</td><td>The group this video is part of</td></tr>
<tr><td>transform</td><td><a href="transform.md">Transform</a><br>Read/Write</td><td>The Transform (position, rotation, scale) of the Video Widget</td></tr>
<tr><td>position</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>The 3D position of the Video Widget</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>The 3D orientation of the Video Widget</td></tr>
<tr><td>scale</td><td>number<br>Read/Write</td><td>The scale of the Video Widget</td></tr>
</tbody></table>



## Class Methods

        
### Video:Import(location)

Imports a video file from the user's MediaLibrary/Videos folder

**Returns:** <a href="video.md">Video</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>location</td><td>string</td><td></td><td>The filename of the video file to import from the user's MediaLibrary/Videos folder</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVideo = Video.Import("myVideo.mp4")</strong></code></pre>



    

## Instance Methods

        
### video:Select()

Adds this Video Widget to the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVideo:Select()</strong></code></pre>




### video:Deselect()

Removes this Video Widget from the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVideo:Deselect()</strong></code></pre>




### video:Delete()

Deletes this Video Widget

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVideo:Delete()</strong></code></pre>



    
