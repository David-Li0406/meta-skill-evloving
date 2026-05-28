
# WebRequest

## Summary
Functions to call remote websites or APIs



## Class Methods

        
### WebRequest:Get(url, onSuccess, onError, headers, context)

Sends a GET request to the given URL

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>url</td><td>string</td><td></td><td>The URL to send the request to</td></tr>
<tr><td>onSuccess</td><td>function</td><td></td><td>A function to call when the request succeeds</td></tr>
<tr><td>onError</td><td>function</td><td></td><td>A function to call when the request fails</td></tr>
<tr><td>headers</td><td>table</td><td></td><td>A table of key-value pairs to send as headers</td></tr>
<tr><td>context</td><td>table</td><td></td><td>A value to pass to the onSuccess and onError functions</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>WebRequest:Get("https://www.example.com/", onSuccess, onError, {["Accept"] = "application/json"}, context)</strong></code></pre>




### WebRequest:Post(url, postData, onSuccess, onError, headers, context)

Sends a POST request to the given URL with the given data

**Returns:** nil 


**Parameters:**

<table data-full-width="false">
<thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody><tr><td>url</td><td>string</td><td></td><td>The URL to send the request to</td></tr>
<tr><td>postData</td><td>table</td><td></td><td>A table of key-value pairs to send as POST data</td></tr>
<tr><td>onSuccess</td><td>function</td><td></td><td>A function to call when the request succeeds</td></tr>
<tr><td>onError</td><td>function</td><td></td><td>A function to call when the request fails</td></tr>
<tr><td>headers</td><td>table</td><td></td><td>A table of key-value pairs to send as headers</td></tr>
<tr><td>context</td><td>table</td><td></td><td>A value to pass to the onSuccess and onError functions</td></tr></tbody></table>




#### Example

<pre class="language-lua"><code class="lang-lua"><strong>WebRequest:Post("https://www.example.com/", {["foo"] = "bar"}, onSuccess, onError, {["Accept"] = "application/json"}, context)</strong></code></pre>



    

