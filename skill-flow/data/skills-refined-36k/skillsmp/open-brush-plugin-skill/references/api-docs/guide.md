
# Guide

## Summary
A guide widget


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>index</td><td>number<br>Read-only</td><td>The index of the active widget</td></tr>
<tr><td>layer</td><td><a href="layer.md">Layer</a><br>Read/Write</td><td>The layer the guide is on</td></tr>
<tr><td>group</td><td><a href="group.md">Group</a><br>Read/Write</td><td>The group this guide is part of</td></tr>
<tr><td>transform</td><td><a href="transform.md">Transform</a><br>Read/Write</td><td>The transform of the Guide Widget</td></tr>
<tr><td>position</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>The 3D position of the Guide Widget</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>The 3D orientation of the Guide Widget</td></tr>
<tr><td>scale</td><td>number<br>Read/Write</td><td>The scale of the Guide Widget</td></tr>
</tbody></table>



## Class Methods

        
### Guide:NewCube(transform)

Creates a new cube guide with a default size using the transform for position and orientation

**Returns:** <a href="guide.md">Guide</a>  (A new cube guide)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform of the Guide Widget</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myGuide = Guide:NewCube(Transform:New(0, 5, 2)</strong></code></pre>




### Guide:NewSphere(transform)

Creates a new sphere guide with a default size using the transform for position and orientation

**Returns:** <a href="guide.md">Guide</a>  (A new sphere guide)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform of the Guide Widget</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myGuide = Guide:NewSphere(Transform:New(0, 5, 2)</strong></code></pre>




### Guide:NewCapsule(transform)

Creates a new capsule guide with a default size using the transform for position and orientation

**Returns:** <a href="guide.md">Guide</a>  (A new capsule guide)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform of the Guide Widget</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myGuide = Guide:NewCapsule(Transform:New(0, 5, 2)</strong></code></pre>




### Guide:NewCone(transform)

Creates a new cone guide with a default size using the transform for position and orientation

**Returns:** <a href="guide.md">Guide</a>  (A new cone guide)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform of the Guide Widget</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myGuide = Guide:NewCone(Transform:New(0, 5, 2)</strong></code></pre>




### Guide:NewEllipsoid(transform)

Creates a new ellipsoid guide with a default size using the transform for position and orientation

**Returns:** <a href="guide.md">Guide</a>  (A new ellipsoid guide)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform of the Guide Widget</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myGuide = Guide:NewEllipsoid(Transform:New(0, 5, 2)</strong></code></pre>




### Guide:NewCustom(transform, model)

Creates a new custom guide from a 3d model. Note that custom guides have to be convex so your model will be "wrapped" as a convex hull

**Returns:** <a href="guide.md">Guide</a>  (A new custom guide based on the convex hull of the model)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform of the Guide Widget</td></tr>
<tr><td>model</td><td><a href="model.md">Model</a></td><td></td><td>The Model to use for the custom guide</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myGuide = Guide:NewCustom(Transform:New(0, 5, 2), myModel</strong></code></pre>



    

## Instance Methods

        
### guide:Select()

Adds the guide to the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myGuide:Select()</strong></code></pre>




### guide:Deselect()

Removes the guide from the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myGuide:Deselect()</strong></code></pre>




### guide:Delete()

Deletes the guide

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myGuide:Delete()</strong></code></pre>




### guide:Scale(scale)

Scales the guide (scale can be non-uniform as some guide types can be stretched)

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>scale</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The scale vector for scaling the Guide Widget</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myGuide:Scale(Vector3:New(2, 0, 0)</strong></code></pre>



    
