
# PathList

## Summary
Multiple disconnected path segments


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>count</td><td>number<br>Read-only</td><td>Gets the number of paths in the PathList</td></tr>
<tr><td>pointCount</td><td>number<br>Read-only</td><td>Gets the number of points in all paths in the PathList</td></tr>
</tbody></table>



## Class Methods

        
### PathList:New()

Creates a new empty PathList

**Returns:** <a href="pathlist.md">PathList</a> 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>PathList:New()</strong></code></pre>




### PathList:New(pathList)

Creates a new PathList from a list of Paths

**Returns:** <a href="pathlist.md">PathList</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>pathList</td><td>Path[]</td><td></td><td>A list of Paths .</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>PathList:New(pathList)</strong></code></pre>




### PathList:FromText(text)

Creates a new PathList from a text

**Returns:** <a href="pathlist.md">PathList</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>text</td><td>string</td><td></td><td>Input text to generate a path.</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>PathList.FromText('example')</strong></code></pre>



    

## Instance Methods

        
### pathList:Draw()

Draws this PathList using current settings

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:Draw()</strong></code></pre>




### pathList:Insert(path)

Inserts a path at the end of the PathList

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>path</td><td><a href="path.md">Path</a></td><td></td><td>The path to be inserted.</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:Insert(myPath)</strong></code></pre>




### pathList:Insert(path, index)

Inserts a path at the specified index of the PathList

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>path</td><td><a href="path.md">Path</a></td><td></td><td>The path to be inserted</td></tr>
<tr><td>index</td><td>number</td><td></td><td>Inserts the new path at this position in the list of paths</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:Insert(myPath, 3)</strong></code></pre>




### pathList:InsertPoint(transform)

Inserts a point at the end of the last path in the PathList

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The point to be inserted</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:InsertPoint(myTransform)</strong></code></pre>




### pathList:InsertPoint(transform, pathIndex, pointIndex)

Inserts a point at the specified index of the specified path

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The point to be inserted</td></tr>
<tr><td>pathIndex</td><td>number</td><td></td><td>Index of the path to add the point to</td></tr>
<tr><td>pointIndex</td><td>number</td><td></td><td>Inserts the point at this index in the list of points</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:InsertPoint(myTransform, 3, 0)</strong></code></pre>




### pathList:TransformBy(transform)

Transforms the whole set of paths

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>A Transform specifying the translation, rotation and scale to apply</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:TransformBy(myTransform)</strong></code></pre>




### pathList:TranslateBy(amount)

Translates the whole set of paths by a given amount

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>amount</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The amount to move the paths by</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:TranslateBy(Vector3.up:Multiply(4))</strong></code></pre>




### pathList:RotateBy(rotation)

Rotates the whole set of paths by a specified amount

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>rotation</td><td><a href="rotation.md">Rotation</a></td><td></td><td>The amount to rotate the paths by</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:RotateBy(Rotation.anticlockwise)</strong></code></pre>




### pathList:ScaleBy(scale)

Scales the whole set of paths by a specified factor

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>scale</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The amount to scale the paths by</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:ScaleBy(vector3)</strong></code></pre>




### pathList:ScaleBy(scale)

Scales the whole set of paths by a specified factor

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>scale</td><td>number</td><td></td><td>The amount to scale the paths by</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:ScaleBy(float)</strong></code></pre>




### pathList:Center()

Offsets all points on the path so that their common center is at the origin

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:Center()</strong></code></pre>




### pathList:Normalize(size)

Scales the whole PathList to fit inside a cube of given size at the origin

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>size</td><td>number</td><td>1</td><td>The size of the cube to fit inside</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:Normalize(1.5)</strong></code></pre>




### pathList:SampleByDistance(spacing)

Resamples all paths with a specified spacing between points

**Returns:** nil  (The new PathList)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>spacing</td><td>number</td><td></td><td>The distance between each new point</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:SampleByDistance(0.2)</strong></code></pre>




### pathList:SampleByCount(count)

Resamples each path evenly into a specified number of points

**Returns:** nil  (The new PathList)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>count</td><td>number</td><td></td><td>Number of points in the new path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:SampleByCount(4)</strong></code></pre>




### pathList:SubdivideSegments(parts)

For each path in the list subdivide it's path segment into the specified number of parts

**Returns:** nil  (The new PathList)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>parts</td><td>number</td><td></td><td>Number of parts to subdivide each path segment into</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:SubdivideSegments(4)</strong></code></pre>




### pathList:Join()

Joins all the paths in order connecting each end to the following start

**Returns:** <a href="path.md">Path</a>  (A single path)




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPaths:Join()</strong></code></pre>




### pathList:Longest()

Returns the longest path in the PathList

**Returns:** <a href="path.md">Path</a>  (The path with the most control points)




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>path = myPaths:Longest()</strong></code></pre>



    
