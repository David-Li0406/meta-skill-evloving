
# Model

## Summary
A 3D model widget


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>index</td><td>number<br>Read-only</td><td>The index of the active Model Widget</td></tr>
<tr><td>layer</td><td><a href="layer.md">Layer</a><br>Read/Write</td><td>The layer the model is on</td></tr>
<tr><td>group</td><td><a href="group.md">Group</a><br>Read/Write</td><td>The group this model is part of</td></tr>
<tr><td>transform</td><td><a href="transform.md">Transform</a><br>Read/Write</td><td>The transformation of the Model Widget</td></tr>
<tr><td>position</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>The 3D position of the Model Widget</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>The 3D orientation of the Model Widget</td></tr>
<tr><td>scale</td><td>number<br>Read/Write</td><td>The scale of the Model Widget</td></tr>
</tbody></table>



## Class Methods

        
### Model:Import(filename)

Imports a new model from the MediaLibrary/Models folder

**Returns:** <a href="model.md">Model</a>  (Returns the Model instance)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>filename</td><td>string</td><td></td><td>The filename of the model to be imported</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Model:Import("Andy.obj")</strong></code></pre>



    

## Instance Methods

        
### model:Select()

Adds this model to the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myModel:Select()</strong></code></pre>




### model:Deselect()

Removes the model from the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myModel:Deselect()</strong></code></pre>




### model:Delete()

Deletes this model

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myModel:Delete()</strong></code></pre>



    
