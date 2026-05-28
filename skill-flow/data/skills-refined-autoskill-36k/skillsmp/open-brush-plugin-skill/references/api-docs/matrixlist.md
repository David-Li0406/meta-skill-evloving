
# MatrixList

## Summary
A list of transformation matrices


## Instance Properties

<table data-full-width="false">
<thead><tr><th>Name</th><th>Return Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>this[index]</td><td><a href="matrix.md">Matrix</a><br>Read/Write</td><td>Returns the matrix at the specified index</td></tr>
<tr><td>count</td><td>number<br>Read-only</td><td>The number of matrices</td></tr>
</tbody></table>



## Class Methods

        
### MatrixList:New(count)

Creates a new MatrixList with the specified number of matrices

**Returns:** <a href="matrixlist.md">MatrixList</a> 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>count</td><td>number</td><td></td><td>The number of matrices to create</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>matrixList = MatrixListApiWrapper.New(5)</strong></code></pre>



    

