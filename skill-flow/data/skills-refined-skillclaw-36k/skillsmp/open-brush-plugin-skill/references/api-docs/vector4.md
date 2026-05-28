
# Vector4

## Summary
A position or offset in 3D space. See https://docs.unity3d.com/ScriptReference/Vector4.html for more detail on many of these methods or properties

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>negativeInfinity</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a><br>Read-only</td><td>A vector of -infinity in all axes</td></tr>
<tr><td>one</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a><br>Read-only</td><td>A vector of 1 in all axes</td></tr>
<tr><td>positiveInfinity</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a><br>Read-only</td><td>A vector of infinity in all axes</td></tr>
<tr><td>zero</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a><br>Read-only</td><td>A vector of 0 in all axes</td></tr>
</tbody></table>



## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>this[index]</td><td>number<br>Read/Write</td><td>The component at the specified index</td></tr>
<tr><td>x</td><td>number<br>Read/Write</td><td>The x coordinate</td></tr>
<tr><td>y</td><td>number<br>Read/Write</td><td>The y coordinate</td></tr>
<tr><td>z</td><td>number<br>Read/Write</td><td>The z coordinate</td></tr>
<tr><td>w</td><td>number<br>Read/Write</td><td>The w coordinate</td></tr>
<tr><td>magnitude</td><td>number<br>Read/Write</td><td>Returns the length of this vector</td></tr>
<tr><td>sqrMagnitude</td><td>number<br>Read/Write</td><td>Returns the squared length of this vector</td></tr>
<tr><td>normalized</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a><br>Read-only</td><td>Returns a vector with the same direction but with a length of 1</td></tr>
</tbody></table>



## Class Methods

        
### Vector4:New(x, y, z, w)

Creates a new vector based on x, y, z and w position

**Returns:** <a href="vector4.md">Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x coordinate</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y coordinate</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The w coordinate</td></tr>
<tr><td>w</td><td>number</td><td></td><td></td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = Vector4:New(1, 2, 3, 4)</strong></code></pre>




### Vector4:Lerp(a, b, t)

Linearly interpolates between two points

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value between 0 and 1 that controls how far between a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector4:Lerp(pointA, PointB, 0.25)</strong></code></pre>




### Vector4:LerpUnclamped(a, b, t)

Linearly interpolates (or extrapolates) between two points

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value that controls how far between (or beyond) a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector4:Lerp(pointA, PointB, 0.25)</strong></code></pre>




### Vector4:Max(a, b)

Creates a vector made from the largest components of the inputs

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The first vector</td></tr>
<tr><td>b</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The second vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = Vector4:Max(firstVector, secondVector</strong></code></pre>




### Vector4:Min(a, b)

Creates a vector made from the smallest components of the inputs

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The first vector</td></tr>
<tr><td>b</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The second vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = Vector4:Min(firstVector, secondVector</strong></code></pre>




### Vector4:Slerp(a, b, t)

Spherically interpolates between two vectors

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value that controls how far between (or beyond) a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector4:Lerp(pointA, PointB, 0.25)</strong></code></pre>




### Vector4:SlerpUnclamped(a, b, t)

Spherically interpolates (or extrapolates) between two vectors

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a>  (A point somewhere between a and b based on the value of t)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>a</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The first point</td></tr>
<tr><td>b</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The second point</td></tr>
<tr><td>t</td><td>number</td><td></td><td>The value that controls how far between (or beyond) a and b the new point is</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newPoint = Vector4:Lerp(pointA, PointB, 0.25)</strong></code></pre>



    

## Instance Methods

        
### vector4:Distance(other)

Returns the distance between two points

**Returns:** number 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>distance = Vector4:Distance(firstPoint, secondPoint)</strong></code></pre>




### vector4:MoveTowards(target, maxDistanceDelta)

Moves a point towards a target point

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>target</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The target point</td></tr>
<tr><td>maxDistanceDelta</td><td>number</td><td></td><td>The maximum distance to move towards the target point</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>position = position:MoveTowards(PointB, 0.25)</strong></code></pre>




### vector4:Project(other)

Projects this vector onto another

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = myVector:Project(otherVector)</strong></code></pre>




### vector4:ScaleBy(other)

Multiplies two vectors component-wise

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Scale(secondVector</strong></code></pre>




### vector4:Add(other)

Adds two vectors

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Add(secondVector)</strong></code></pre>




### vector4:Add(x, y, z)

Adds x, y and z values to this vector

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Add(1, 2, 3)</strong></code></pre>




### vector4:Subtract(other)

Subtracts a Vector4 from this vector

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="unityengine.vector4.md">UnityEngine.Vector4</a></td><td></td><td>The vector to subtract</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Subtract(otherVector)</strong></code></pre>




### vector4:Subtract(x, y, z)

Subtracts x, y and z values from this vector

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Subtract(1, 2, 3)</strong></code></pre>




### vector4:Multiply(value)

Multiplies this vector by a scalar value

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>value</td><td>number</td><td></td><td>The scalar value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Multiply(2)</strong></code></pre>




### vector4:ScaleBy(x, y, z)

Multiplies this vector by x, y and z values component-wise

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Multiply(2, 3, 4)</strong></code></pre>




### vector4:Divide(value)

Divides this vector by a scalar value

**Returns:** <a href="unityengine.vector4.md">UnityEngine.Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>value</td><td>number</td><td></td><td>The scalar value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>result = myVector:Divide(2)</strong></code></pre>




### vector4:NotEquals(other)

Is this vector not equal to another?

**Returns:** boolean 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>other</td><td><a href="vector4.md">Vector4</a></td><td></td><td>The other vector</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>if myVector:NotEquals(Vector4.zero) then print("Vector is not zero") end</strong></code></pre>




### vector4:NotEquals(x, y, z)

Is this vector not equal to these x, y and z values?

**Returns:** boolean 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>x</td><td>number</td><td></td><td>The x value</td></tr>
<tr><td>y</td><td>number</td><td></td><td>The y value</td></tr>
<tr><td>z</td><td>number</td><td></td><td>The z value</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>if myVector:NotEquals(1, 2, 3) then print("Vector is not 1,2,3") end</strong></code></pre>



    
