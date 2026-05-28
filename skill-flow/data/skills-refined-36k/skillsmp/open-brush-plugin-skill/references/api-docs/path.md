
# Path

## Summary
A list of transforms that usually represents a path in 3D space. These form the basis for brush strokes and camera paths


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>count</td><td>number<br>Read-only</td><td>Returns the number of points in this path</td></tr>
<tr><td>this[index]</td><td><a href="transform.md">Transform</a><br>Read/Write</td><td>Returns the point at the specified index</td></tr>
<tr><td>last</td><td><a href="transform.md">Transform</a><br>Read-only</td><td>Returns the last point in this path</td></tr>
</tbody></table>



## Class Methods

        
### Path:New()

Creates a new empty Path

**Returns:** <a href="path.md">Path</a> 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath = Path:New()</strong></code></pre>




### Path:New(transformList)

Creates a path from a list of Transforms

**Returns:** <a href="path.md">Path</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transformList</td><td>Transform[]</td><td></td><td>The list of transforms</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath = Path:New({transform1, transform2, transform3})</strong></code></pre>




### Path:New(positionList)

Creates a path from a list of Vector3 positions

**Returns:** <a href="path.md">Path</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>positionList</td><td>Vector3[]</td><td></td><td>The list of positions</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath = Path:New({position1, position2, position3})</strong></code></pre>




### Path:Hermite(startTransform, endTransform, startTangent, endTangent, resolution, tangentStrength)

Generates a hermite spline

**Returns:** <a href="path.md">Path</a>  (A new Path)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>startTransform</td><td><a href="transform.md">Transform</a></td><td></td><td>Starting transformation</td></tr>
<tr><td>endTransform</td><td><a href="transform.md">Transform</a></td><td></td><td>End transformation</td></tr>
<tr><td>startTangent</td><td><a href="vector3.md">Vector3</a></td><td></td><td>Starting tangent</td></tr>
<tr><td>endTangent</td><td><a href="vector3.md">Vector3</a></td><td></td><td>End tangent</td></tr>
<tr><td>resolution</td><td>number</td><td></td><td>Resolution of the spline</td></tr>
<tr><td>tangentStrength</td><td>number</td><td>1</td><td>Strength of the tangent</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Hermite(startTransform, endTransform, startTangent, endTangent, resolution, tangentStrength)</strong></code></pre>



    

## Instance Methods

        
### path:GetDirection(index)

Returns a vector representing the direction of the path at the given point

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>index</td><td>number</td><td></td><td>Index of control point to use</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:GetDirection(3)</strong></code></pre>




### path:GetNormal(index)

Returns a vector representing the normal of the path at the given point

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>index</td><td>number</td><td></td><td>Index of control point to use</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:GetNormal(3)</strong></code></pre>




### path:GetTangent(index)

Returns a vector representing the tangent of the path at the given point

**Returns:** <a href="vector3.md">Vector3</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>index</td><td>number</td><td></td><td>Index of control point to use</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:GetTangent(3)</strong></code></pre>




### path:Draw()

Draws this path as a brush stroke using current settings

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Draw()</strong></code></pre>




### path:Insert(transform)

Inserts a new point at the end of the path

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform to be inserted at the end of the path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Insert(myTransform</strong></code></pre>




### path:Insert(transform, index)

Inserts a new point at the specified index

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform to be inserted</td></tr>
<tr><td>index</td><td>number</td><td></td><td>The index at which to insert the transform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Insert(transform, index)</strong></code></pre>




### path:TransformBy(transform)

Transforms all points in the path by the specific amount

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform to be applied to all points in the path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:TransformBy(transform)</strong></code></pre>




### path:TranslateBy(amount)

Changes the position of all points in the path by a given amount

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>amount</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The distance to move the points</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:TranslateBy(Vector3:up)</strong></code></pre>




### path:RotateBy(amount)

Rotates all points in the path around the origin by a given amount

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>amount</td><td><a href="rotation.md">Rotation</a></td><td></td><td>The amount by which to rotate the path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:RotateBy(Rotation.New(45, 0, 0)</strong></code></pre>




### path:ScaleBy(scale)

Scales the path

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>scale</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The scaling factor to apply to the path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:ScaleBy(Vector3:New(2, 1, 1)</strong></code></pre>




### path:Center()

Moves all points on the path so that their common center is the origin

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Center()</strong></code></pre>




### path:StartingFrom(index)

Reorders the points so that point at the given index is shifted to be the first point

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>index</td><td>number</td><td></td><td>The index of the point to make the new first point</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:StartingFrom(3)</strong></code></pre>




### path:FindClosest(point)

Returns the index of the point closest to the given position

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>point</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The 3D position that we are seeking the closest to</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindClosest(Vector3:New(10, 2, 4)</strong></code></pre>




### path:FindMinimumX()

Returns the index of the point with the smallest X value

**Returns:** number 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindMinimumX()</strong></code></pre>




### path:FindMinimumY()

Returns the index of the point with the smallest Y value

**Returns:** number 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindMinimumY()</strong></code></pre>




### path:FindMinimumZ()

Returns the index of the point with the smallest Z value

**Returns:** number 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindMinimumZ()</strong></code></pre>




### path:FindMaximumX()

Returns the index of the point with the biggest X value

**Returns:** number 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindMaximumX()</strong></code></pre>




### path:FindMaximumY()

Returns the index of the point with the biggest Y value

**Returns:** number 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindMaximumY()</strong></code></pre>




### path:FindMaximumZ()

Returns the index of the point with the biggest Z value

**Returns:** number 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindMaximumZ()</strong></code></pre>




### path:Normalize(size)

Scales and shifts all points so that they fit in a cube of the given size at the origin

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>size</td><td>number</td><td>1</td><td>The size of the cube to fit the path into</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Normalize(size)</strong></code></pre>




### path:SampleByDistance(spacing)

Resamples the path evenly by distance

**Returns:** nil  (The new path)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>spacing</td><td>number</td><td></td><td>The space between points in the new path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:SampleByDistance(spacing)</strong></code></pre>




### path:SampleByCount(count)

Resamples the path evenly into the specified number of points

**Returns:** nil  (The new path)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>count</td><td>number</td><td></td><td>The number of points in the new path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:SampleByCount(count)</strong></code></pre>




### path:SubdivideSegments(parts)

Subdivides each path segment into the specified number of parts

**Returns:** nil  (The new path)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>parts</td><td>number</td><td></td><td>Number of parts to subdivide into</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:SubdivideSegments(parts)</strong></code></pre>



    
