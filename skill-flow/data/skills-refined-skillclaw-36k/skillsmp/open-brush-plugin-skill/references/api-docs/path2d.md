
# Path2d

## Summary
A set of Vector2 points forming a 2D path


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>count</td><td>number<br>Read-only</td><td>Returns the number of points in this path</td></tr>
<tr><td>this[index]</td><td><a href="transform.md">Transform</a><br>Read-only</td><td>Returns the point at the specified index</td></tr>
<tr><td>last</td><td><a href="transform.md">Transform</a><br>Read-only</td><td>Returns the last point in this path</td></tr>
</tbody></table>



## Class Methods

        
### Path2d:New()

Creates a new empty 2d Path

**Returns:** <a href="path2d.md">Path2d</a> 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath = Path2d:New()</strong></code></pre>




### Path2d:New(positionList)

Creates a 2d path from a list of Vector2 points

**Returns:** <a href="path2d.md">Path2d</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>positionList</td><td>Vector2[]</td><td></td><td>The list of points</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath = Path2d:New({point1, point2, point3})</strong></code></pre>




### Path2d:New(positionList)

Creates a path from a list of Vector3 points

**Returns:** <a href="path2d.md">Path2d</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>positionList</td><td>Vector3[]</td><td></td><td>The list of points</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath = Path:New({point1, point2, point3})</strong></code></pre>




### Path2d:Polygon(sides)

Generates a regular polygon path

**Returns:** <a href="path2d.md">Path2d</a>  (The new path)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>sides</td><td>number</td><td></td><td>The number of sides for the polygon</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath = Path2d:Polygon(6)</strong></code></pre>



    

## Instance Methods

        
### path2d:Insert(point)

Inserts a new point at the end of the path

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>point</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The point to be inserted at the end of the path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Insert(Transform:New(pos, rot)</strong></code></pre>




### path2d:Insert(point, index)

Inserts a new point at the specified index

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>point</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The point to be inserted</td></tr>
<tr><td>index</td><td>number</td><td></td><td>The index at which to insert the point</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Insert(transform, index)</strong></code></pre>




### path2d:OnX()

Converts the 2D path to a 3D path on the YZ plane (i.e. with all x values set to 0)

**Returns:** <a href="path.md">Path</a>  (A 3D Path based on the input but with all x as 0: (0, inX, inY))




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>my3dPath = my2dPath:OnX()</strong></code></pre>




### path2d:OnY()

Converts the 2D path to a 3D path on the XZ plane (i.e. with all y values set to 0)

**Returns:** <a href="path.md">Path</a>  (A 3D Path based on the input but with all y as 0: (inX, 0, inY))




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>my3dPath = my2dPath:OnY()</strong></code></pre>




### path2d:OnZ()

Converts the 2D path to a 3D path on the XY plane (i.e. with all z values set to 0)

**Returns:** <a href="path.md">Path</a>  (A 3D Path based on the input but with all z as 0: (inX, inY, 0))




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>my3dPath = my2dPath:OnZ()</strong></code></pre>




### path2d:TransformBy(transform)

Transforms all points in the path by the specific amount

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>transform</td><td><a href="transform.md">Transform</a></td><td></td><td>The transform to be applied to all points in the path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:TransformBy(transform)</strong></code></pre>




### path2d:TranslateBy(amount)

Changes the position of all points in the path by a given amount

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>amount</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The distance to move the points</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:TranslateBy(Vector3:up)</strong></code></pre>




### path2d:RotateBy(amount)

Rotates all points in the path around the origin by a given amount

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>amount</td><td><a href="rotation.md">Rotation</a></td><td></td><td>The amount by which to rotate the path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:RotateBy(Rotation.New(45, 0, 0)</strong></code></pre>




### path2d:ScaleBy(scale)

Scales the path

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>scale</td><td>number</td><td></td><td>The scaling factor to apply to the path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:ScaleBy(2)</strong></code></pre>




### path2d:ScaleBy(x, y)

Scales the path

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x scaling factor to apply to the path</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y scaling factor to apply to the path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:ScaleBy(2, 1)</strong></code></pre>




### path2d:ScaleBy(scale)

Scales the path

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>scale</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The scaling factor to apply to the path</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:ScaleBy(myVector2</strong></code></pre>




### path2d:Center()

Moves all points on the path so that their common center is the origin

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Center()</strong></code></pre>




### path2d:StartingFrom(index)

Reorders the points so that point at the given index is shifted to be the first point

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>index</td><td>number</td><td></td><td>The index of the point to make the new first point</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:StartingFrom(3)</strong></code></pre>




### path2d:FindClosest(point)

Returns the index of the point closest to the given position

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>point</td><td><a href="vector2.md">Vector2</a></td><td></td><td>The 3D position that we are seeking the closest to</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindClosest(Vector3:New(10, 2, 4)</strong></code></pre>




### path2d:FindMinimumX()

Returns the index of the point with the smallest X value

**Returns:** number 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindMinimumX()</strong></code></pre>




### path2d:FindMinimumY()

Returns the index of the point with the smallest Y value

**Returns:** number 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindMinimumY()</strong></code></pre>




### path2d:FindMaximumX()

Returns the index of the point with the biggest X value

**Returns:** number 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindMaximumX()</strong></code></pre>




### path2d:FindMaximumY()

Returns the index of the point with the biggest Y value

**Returns:** number 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:FindMaximumY()</strong></code></pre>




### path2d:Normalize(size)

Scales and shifts all points so that they fit in a 1 unit square at the origin

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>size</td><td>number</td><td>1</td><td>The size of the square to fit the path into</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Normalize(size)</strong></code></pre>




### path2d:Resample(spacing)

Resamples the path at a specified spacing

**Returns:** nil  (The resampled path)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>spacing</td><td>number</td><td></td><td>The space between points in the new pat</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myPath:Resample(spacing)</strong></code></pre>



    
