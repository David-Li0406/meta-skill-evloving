
# Selection

## Summary
Various actions related to selections of strokes and widgets



## Class Methods

        
### Selection:Deselect()



**Returns:** nil 






### Selection:Duplicate()

Duplicates the currently selected items

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Selection:Duplicate()</strong></code></pre>




### Selection:Group()

Groups or ungroups the currently selected strokes and widgets

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Selection:Group()</strong></code></pre>




### Selection:Invert()

Inverts the current selection

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Selection:Invert()</strong></code></pre>




### Selection:Flip()

Flips (mirrors) the current selected items horizontally

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Selection:Flip()</strong></code></pre>




### Selection:Recolor()

Changes the color of all currently selected brush strokes

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Selection:Recolor()</strong></code></pre>




### Selection:Rebrush()

Changes the brush type for all currently selected brush strokes

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Selection:Rebrush()</strong></code></pre>




### Selection:Resize()

Changes the size of all currently selected brush strokes

**Returns:** nil 




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Selection:Resize()</strong></code></pre>




### Selection:Trim(count)

Trims control points from all selected brush strokes. Resulting empty strokes are deleted.

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>count</td><td>number</td><td></td><td>The number of points to trim from each stroke</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>Selection:Trim(5)</strong></code></pre>



    

