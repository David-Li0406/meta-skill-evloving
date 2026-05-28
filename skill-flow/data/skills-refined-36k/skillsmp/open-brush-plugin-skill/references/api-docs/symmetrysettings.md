
# SymmetrySettings

## Summary
A collection of settings for the symmetry mode


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>matrices</td><td><a href="matrixlist.md">MatrixList</a><br>Read-only</td><td>The list of transform matrices for this symmetry mode</td></tr>
<tr><td>mode</td><td><a href="symmetrymode.md">SymmetryMode</a><br>Read/Write</td><td>The symmetry mode</td></tr>
<tr><td>transform</td><td><a href="transform.md">Transform</a><br>Read/Write</td><td>The transform of the symmetry widget</td></tr>
<tr><td>position</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>The position of the symmetry widget</td></tr>
<tr><td>rotation</td><td><a href="rotation.md">Rotation</a><br>Read/Write</td><td>The rotation of the symmetry widget</td></tr>
<tr><td>spin</td><td><a href="vector3.md">Vector3</a><br>Read/Write</td><td>How fast the symmetry widget is spinning in each axis</td></tr>
<tr><td>pointType</td><td><a href="symmetrypointtype.md">SymmetryPointType</a><br>Read/Write</td><td>The type of point symmetry</td></tr>
<tr><td>pointOrder</td><td>number<br>Read/Write</td><td>The order of point symmetry (how many times it repeats around it's axis)</td></tr>
<tr><td>wallpaperType</td><td><a href="symmetrywallpapertype.md">SymmetryWallpaperType</a><br>Read/Write</td><td>The type of wallpaper symmetry</td></tr>
<tr><td>wallpaperRepeatX</td><td>number<br>Read/Write</td><td>How many times the wallpaper symmetry repeats in the X axis</td></tr>
<tr><td>wallpaperRepeatY</td><td>number<br>Read/Write</td><td>How many times the wallpaper symmetry repeats in the Y axis</td></tr>
<tr><td>wallpaperScale</td><td>number<br>Read/Write</td><td>The overall scale of the wallpaper symmetry</td></tr>
<tr><td>wallpaperScaleX</td><td>number<br>Read/Write</td><td>The scale of the wallpaper symmetry in the X axis</td></tr>
<tr><td>wallpaperScaleY</td><td>number<br>Read/Write</td><td>The scale of the wallpaper symmetry in the Y axis</td></tr>
<tr><td>wallpaperSkewX</td><td>number<br>Read/Write</td><td>The skew of the wallpaper symmetry in the X axis</td></tr>
<tr><td>wallpaperSkewY</td><td>number<br>Read/Write</td><td>The skew of the wallpaper symmetry in the Y axis</td></tr>
</tbody></table>



## Class Methods

        
### SymmetrySettings:NewPointSymmetry(type, order)

Creates a new set of symmetry settings based on point symmetry

**Returns:** <a href="symmetrysettings.md">SymmetrySettings</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>type</td><td><a href="symmetrypointtype.md">SymmetryPointType</a></td><td></td><td>The type of point symmetry</td></tr>
<tr><td>order</td><td>number</td><td></td><td>The number of repeats around the axis</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>mySymSettings = Symmetry:NewPoint()</strong></code></pre>




### SymmetrySettings:NewWallpaperSymmetry(type, repeatX, repeatY, scale, scaleX, scaleY, skewX, skewY)

Creates a new set of symmetry settings based on wallpaper symmetry

**Returns:** <a href="symmetrysettings.md">SymmetrySettings</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>type</td><td><a href="symmetrywallpapertype.md">SymmetryWallpaperType</a></td><td></td><td>The type of point symmetry</td></tr>
<tr><td>repeatX</td><td>number</td><td></td><td></td></tr>
<tr><td>repeatY</td><td>number</td><td></td><td></td></tr>
<tr><td>scale</td><td>number</td><td>1</td><td></td></tr>
<tr><td>scaleX</td><td>number</td><td>1</td><td></td></tr>
<tr><td>scaleY</td><td>number</td><td>1</td><td></td></tr>
<tr><td>skewX</td><td>number</td><td>0</td><td></td></tr>
<tr><td>skewY</td><td>number</td><td>0</td><td></td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>mySymSettings = Symmetry:NewPoint()</strong></code></pre>



    

## Instance Methods

        
### symmetrySettings:Duplicate()

Creates a copy of these symmetry settings

**Returns:** <a href="symmetrysettings.md">SymmetrySettings</a> 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>newSettings = Symmetry.current:Duplicate()</strong></code></pre>



    
