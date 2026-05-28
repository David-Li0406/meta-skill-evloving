
# Matrix

## Summary
A 4x4 matrix representing a 3D transformation

## Class Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>identity</td><td><a href="matrix.md">Matrix</a><br>Read-only</td><td>Returns the identity matrix</td></tr>
<tr><td>zero</td><td><a href="matrix.md">Matrix</a><br>Read-only</td><td>Returns a matrix with all elements set to zero</td></tr>
</tbody></table>



## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>this[index]</td><td>number<br>Read/Write</td><td>The component at the specified index</td></tr>
<tr><td>this[index]</td><td>number<br>Read/Write</td><td>The component at the specified row and column</td></tr>
<tr><td>determinant</td><td>number<br>Read-only</td><td>The determinant of the matrix</td></tr>
<tr><td>inverse</td><td><a href="matrix.md">Matrix</a><br>Read-only</td><td>The inverse of this matrix</td></tr>
<tr><td>isIdentity</td><td>boolean<br>Read-only</td><td>Checks whether this is an identity matrix</td></tr>
<tr><td>scale</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>Attempts to get a scale value from the matrix</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>Attempts to get a rotation from this matrix</td></tr>
<tr><td>transpose</td><td><a href="matrix.md">Matrix</a><br>Read-only</td><td>Returns the transpose of this matrix</td></tr>
<tr><td>position</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>The position vector of this matrix</td></tr>
<tr><td>isValidTRS</td><td>boolean<br>Read-only</td><td>Checks if this matrix is a valid transform matrix</td></tr>
</tbody></table>



## Class Methods

        
### Matrix:New(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33)

Creates a new 4x4 matrix

**Returns:** <a href="matrix.md">Matrix</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>m00</td><td>number</td><td></td><td></td></tr>
<tr><td>m01</td><td>number</td><td></td><td></td></tr>
<tr><td>m02</td><td>number</td><td></td><td></td></tr>
<tr><td>m03</td><td>number</td><td></td><td></td></tr>
<tr><td>m10</td><td>number</td><td></td><td></td></tr>
<tr><td>m11</td><td>number</td><td></td><td></td></tr>
<tr><td>m12</td><td>number</td><td></td><td></td></tr>
<tr><td>m13</td><td>number</td><td></td><td></td></tr>
<tr><td>m20</td><td>number</td><td></td><td></td></tr>
<tr><td>m21</td><td>number</td><td></td><td></td></tr>
<tr><td>m22</td><td>number</td><td></td><td></td></tr>
<tr><td>m23</td><td>number</td><td></td><td></td></tr>
<tr><td>m30</td><td>number</td><td></td><td></td></tr>
<tr><td>m31</td><td>number</td><td></td><td></td></tr>
<tr><td>m32</td><td>number</td><td></td><td></td></tr>
<tr><td>m33</td><td>number</td><td></td><td></td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newVector = Matrix:New(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1 ,0, 0, 0, 0, 1)</strong></code></pre>




### Matrix:NewRotation(rotation)

Creates a rotation matrix

**Returns:** <a href="matrix.md">Matrix</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>rotation</td><td><a href="rotation.md">Rotation</a></td><td></td><td></td></tr></tbody></table>






### Matrix:NewScaling(scale)

Creates a scaling matrix

**Returns:** <a href="matrix.md">Matrix</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>scale</td><td><a href="vector3.md">Vector3</a></td><td></td><td></td></tr></tbody></table>






### Matrix:NewTranslation(translation)

Creates a translation matrix

**Returns:** <a href="matrix.md">Matrix</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>translation</td><td><a href="vector3.md">Vector3</a></td><td></td><td></td></tr></tbody></table>






### Matrix:NewTRS(translation, rotation, scale)

Creates a translation, rotation and scaling matrix

**Returns:** <a href="matrix.md">Matrix</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>translation</td><td><a href="vector3.md">Vector3</a></td><td></td><td></td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a></td><td></td><td></td></tr>
<tr><td>scale</td><td><a href="vector3.md">Vector3</a></td><td></td><td></td></tr></tbody></table>





    

## Instance Methods

        
### matrix:MultiplyPoint(point)

Transforms a position by this matrix

**Returns:** <a href="vector3.md">Vector3</a>  (The transformed position)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>point</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The position to transform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVector = myMatrix:MultiplyPoint(myVector)</strong></code></pre>




### matrix:MultiplyPoint3x4(point)

Transforms a position by this matrix (Faster than MultiplyPoint but only supports TRS matrices)

**Returns:** <a href="vector3.md">Vector3</a>  (The transformed position)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>point</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The position to transform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVector = myMatrix:MultiplyPoint3x4(myVector)</strong></code></pre>




### matrix:MultiplyVector(vector)

Transforms a direction by this matrix

**Returns:** <a href="vector3.md">Vector3</a>  (The transformed direction vector)


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>vector</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The direction vector to transform</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVector = myMatrix:MultiplyVector(myVector)</strong></code></pre>




### matrix:GetColumn(index)

Get a column from the matrix

**Returns:** <a href="vector4.md">Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>index</td><td>number</td><td></td><td>The index of the column to return (0 is the first column)</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVector = myMatrix:GetColumn(0)</strong></code></pre>




### matrix:SetColumn(index, value)

Sets a column of the matrix

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>index</td><td>number</td><td></td><td>The index of the column to set (0 is the first column)</td></tr>
<tr><td>value</td><td><a href="vector4.md">Vector4</a></td><td></td><td>The value to set</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myMatrix:SetColumn(0, myVector)</strong></code></pre>




### matrix:GetRow(index)

Returns a row from the matrix

**Returns:** <a href="vector4.md">Vector4</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>index</td><td>number</td><td></td><td>The index of the row to return (0 is the first row)</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myVector = myMatrix:GetRow(0)</strong></code></pre>




### matrix:SetRow(index, value)

Sets a row of the matrix

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>index</td><td>number</td><td></td><td>The index of the row to set (0 is the first row)</td></tr>
<tr><td>value</td><td><a href="vector4.md">Vector4</a></td><td></td><td>The value to set</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myMatrix:SetRow(0, myVector)</strong></code></pre>




### matrix:SetTRS(pos, rot, scale)

Sets this matrix to a translation, rotation and scaling matrix

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>pos</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The position</td></tr>
<tr><td>rot</td><td><a href="rotation.md">Rotation</a></td><td></td><td>The rotation</td></tr>
<tr><td>scale</td><td><a href="vector3.md">Vector3</a></td><td></td><td>The scale</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>myMatrix:SetTRS(myPosition, myRotation, myScale)</strong></code></pre>




### matrix:LookAt(from, to, up)

Creates a  "Look At" matrix

**Returns:** <a href="matrix.md">Matrix</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>from</td><td><a href="vector3.md">Vector3</a></td><td></td><td></td></tr>
<tr><td>to</td><td><a href="vector3.md">Vector3</a></td><td></td><td></td></tr>
<tr><td>up</td><td><a href="vector3.md">Vector3</a></td><td></td><td></td></tr></tbody></table>





    
