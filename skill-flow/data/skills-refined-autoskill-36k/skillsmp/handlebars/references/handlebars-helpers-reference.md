# Handlebars-Helpers Package Reference

Complete reference for the `handlebars-helpers` package (https://github.com/helpers/handlebars-helpers).

These 189+ helpers are automatically available in all Aurora CLI templates.

---

## String Helpers (36)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `append` | `{{ append str suffix }}` | Append suffix to string |
| `camelcase` | `{{ camelcase str }}` | Convert to camelCase |
| `capitalize` | `{{ capitalize str }}` | Capitalize first word |
| `capitalizeAll` | `{{ capitalizeAll str }}` | Capitalize all words |
| `center` | `{{ center str width }}` | Center string with spaces |
| `chop` | `{{ chop str }}` | Remove whitespace and non-word chars |
| `dashcase` | `{{ dashcase str }}` | Convert to dash-case |
| `dotcase` | `{{ dotcase str }}` | Convert to dot.case |
| `downcase` | `{{ downcase str }}` | Convert to lowercase |
| `ellipsis` | `{{ ellipsis str length }}` | Truncate with ellipsis |
| `hyphenate` | `{{ hyphenate str }}` | Replace spaces with hyphens |
| `isString` | `{{#isString val}}...{{/isString}}` | Test if value is string |
| `lowercase` | `{{ lowercase str }}` | Convert to lowercase |
| `occurrences` | `{{ occurrences str substring }}` | Count substring occurrences |
| `pascalcase` | `{{ pascalcase str }}` | Convert to PascalCase |
| `pathcase` | `{{ pathcase str }}` | Convert to path/case |
| `plusify` | `{{ plusify str }}` | Replace spaces with plus signs |
| `prepend` | `{{ prepend str prefix }}` | Prepend prefix to string |
| `raw` | `{{{{raw}}}}...{{{{/raw}}}}` | Render without processing |
| `remove` | `{{ remove str substr }}` | Remove all occurrences |
| `removeFirst` | `{{ removeFirst str substr }}` | Remove first occurrence |
| `replace` | `{{ replace str old new }}` | Replace all occurrences |
| `replaceFirst` | `{{ replaceFirst str old new }}` | Replace first occurrence |
| `reverse` | `{{ reverse str }}` | Reverse string |
| `sentence` | `{{ sentence str }}` | Convert to sentence case |
| `snakecase` | `{{ snakecase str }}` | Convert to snake_case |
| `split` | `{{ split str delimiter }}` | Split string to array |
| `startsWith` | `{{ startsWith str prefix }}` | Test if starts with prefix |
| `titleize` | `{{ titleize str }}` | Convert to Title Case |
| `trim` | `{{ trim str }}` | Remove whitespace from ends |
| `trimLeft` | `{{ trimLeft str }}` | Remove leading whitespace |
| `trimRight` | `{{ trimRight str }}` | Remove trailing whitespace |
| `truncate` | `{{ truncate str length }}` | Truncate to length |
| `truncateWords` | `{{ truncateWords str count }}` | Truncate to word count |
| `upcase` | `{{ upcase str }}` | Convert to uppercase |
| `uppercase` | `{{ uppercase str }}` | Convert to uppercase |

---

## Array Helpers (28)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `after` | `{{ after array n }}` | Items after index n |
| `arrayify` | `{{ arrayify value }}` | Convert value to array |
| `before` | `{{ before array n }}` | First n items |
| `eachIndex` | `{{#eachIndex arr}}...{{/eachIndex}}` | Iterate with index tracking |
| `filter` | `{{#filter arr}}...{{/filter}}` | Filter array by condition |
| `first` | `{{ first array [n] }}` | Get first n items |
| `forEach` | `{{#forEach arr}}...{{/forEach}}` | Iterate with position info |
| `inArray` | `{{#inArray val arr}}...{{/inArray}}` | Check if in array |
| `isArray` | `{{#isArray val}}...{{/isArray}}` | Test if value is array |
| `itemAt` | `{{ itemAt array index }}` | Get item at index |
| `join` | `{{ join array separator }}` | Join array with separator |
| `equalsLength` | `{{#equalsLength arr n}}...{{/equalsLength}}` | Check if length equals n |
| `last` | `{{ last array [n] }}` | Get last n items |
| `length` | `{{ length array }}` | Get array/string length |
| `lengthEqual` | `{{#lengthEqual arr n}}...{{/lengthEqual}}` | Alias for equalsLength |
| `map` | `{{#map arr}}...{{/map}}` | Apply function to each |
| `pluck` | `{{ pluck array property }}` | Extract property values |
| `reverse` | `{{ reverse array }}` | Reverse array |
| `some` | `{{#some arr}}...{{/some}}` | Test if any matches |
| `sort` | `{{ sort array }}` | Sort array |
| `sortBy` | `{{ sortBy array property }}` | Sort by property |
| `withAfter` | `{{#withAfter arr n}}...{{/withAfter}}` | Context: items after n |
| `withBefore` | `{{#withBefore arr n}}...{{/withBefore}}` | Context: items before n |
| `withFirst` | `{{#withFirst arr [n]}}...{{/withFirst}}` | Context: first n items |
| `withGroup` | `{{#withGroup arr size}}...{{/withGroup}}` | Group by size |
| `withLast` | `{{#withLast arr [n]}}...{{/withLast}}` | Context: last n items |
| `withSort` | `{{#withSort arr prop}}...{{/withSort}}` | Context: sorted array |
| `unique` | `{{ unique array }}` | Remove duplicates |

---

## Comparison Helpers (24)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `and` | `{{#and a b}}...{{/and}}` | Both values truthy |
| `compare` | `{{#compare a op b}}...{{/compare}}` | Compare with operator |
| `contains` | `{{#contains coll val}}...{{/contains}}` | Collection has value |
| `default` | `{{ default value fallback }}` | Return fallback if undefined |
| `eq` | `{{#eq a b}}...{{/eq}}` | Strictly equal |
| `gt` | `{{#gt a b}}...{{/gt}}` | Greater than |
| `gte` | `{{#gte a b}}...{{/gte}}` | Greater than or equal |
| `has` | `{{#has val pattern}}...{{/has}}` | Value has pattern |
| `isFalsey` | `{{#isFalsey val}}...{{/isFalsey}}` | Value is falsey |
| `isTruthy` | `{{#isTruthy val}}...{{/isTruthy}}` | Value is truthy |
| `ifEven` | `{{#ifEven num}}...{{/ifEven}}` | Number is even |
| `ifNth` | `{{#ifNth num n}}...{{/ifNth}}` | Every nth iteration |
| `ifOdd` | `{{#ifOdd num}}...{{/ifOdd}}` | Number is odd |
| `is` | `{{#is a b}}...{{/is}}` | Loosely equal |
| `isnt` | `{{#isnt a b}}...{{/isnt}}` | Not equal |
| `lt` | `{{#lt a b}}...{{/lt}}` | Less than |
| `lte` | `{{#lte a b}}...{{/lte}}` | Less than or equal |
| `neither` | `{{#neither a b}}...{{/neither}}` | Both values falsey |
| `not` | `{{#not val}}...{{/not}}` | Value is falsey |
| `or` | `{{#or a b}}...{{/or}}` | At least one truthy |
| `unlessEq` | `{{#unlessEq a b}}...{{/unlessEq}}` | Unless equal |
| `unlessGt` | `{{#unlessGt a b}}...{{/unlessGt}}` | Unless greater than |
| `unlessLt` | `{{#unlessLt a b}}...{{/unlessLt}}` | Unless less than |
| `unlessGteq` | `{{#unlessGteq a b}}...{{/unlessGteq}}` | Unless greater or equal |
| `unlessLteq` | `{{#unlessLteq a b}}...{{/unlessLteq}}` | Unless less or equal |

---

## Math Helpers (16)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `abs` | `{{ abs num }}` | Absolute value |
| `add` | `{{ add a b }}` | Add two numbers |
| `avg` | `{{ avg array }}` | Average of array |
| `ceil` | `{{ ceil num }}` | Round up |
| `divide` | `{{ divide a b }}` | Divide a by b |
| `floor` | `{{ floor num }}` | Round down |
| `minus` | `{{ minus a b }}` | Subtract (alias) |
| `modulo` | `{{ modulo a b }}` | Remainder |
| `multiply` | `{{ multiply a b }}` | Multiply |
| `plus` | `{{ plus a b }}` | Add (alias) |
| `random` | `{{ random min max }}` | Random in range |
| `remainder` | `{{ remainder a b }}` | Remainder (alias) |
| `round` | `{{ round num }}` | Round |
| `subtract` | `{{ subtract a b }}` | Subtract |
| `sum` | `{{ sum array }}` | Sum of array |
| `times` | `{{ times a b }}` | Multiply (alias) |

---

## Number Helpers (9)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `bytes` | `{{ bytes num }}` | Format as byte size |
| `addCommas` | `{{ addCommas num }}` | Add thousand separators |
| `phoneNumber` | `{{ phoneNumber str }}` | Format as phone number |
| `toAbbr` | `{{ toAbbr num }}` | Abbreviate number |
| `toExponential` | `{{ toExponential num dec }}` | Exponential notation |
| `toFixed` | `{{ toFixed num dec }}` | Fixed decimal places |
| `toFloat` | `{{ toFloat str }}` | Convert to float |
| `toInt` | `{{ toInt str }}` | Convert to integer |
| `toPrecision` | `{{ toPrecision num digits }}` | Set precision |

---

## Object Helpers (14)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `extend` | `{{#extend obj1 obj2}}...{{/extend}}` | Extend context |
| `forIn` | `{{#forIn obj}}...{{/forIn}}` | Iterate all properties |
| `forOwn` | `{{#forOwn obj}}...{{/forOwn}}` | Iterate own properties |
| `toPath` | `{{ toPath args... }}` | Create dot-path |
| `get` | `{{ get obj "path.to.val" }}` | Get nested value |
| `getObject` | `{{ getObject obj "key" }}` | Get key-value pair |
| `hasOwn` | `{{#hasOwn obj "key"}}...{{/hasOwn}}` | Has own property |
| `isObject` | `{{#isObject val}}...{{/isObject}}` | Test if object |
| `JSONparse` | `{{ JSONparse str }}` | Parse JSON string |
| `JSONstringify` | `{{ JSONstringify obj }}` | Stringify to JSON |
| `merge` | `{{#merge obj1 obj2}}...{{/merge}}` | Deep merge objects |
| `parseJSON` | `{{ parseJSON str }}` | Parse JSON (alias) |
| `pick` | `{{#pick ctx keys...}}...{{/pick}}` | Pick properties |
| `stringify` | `{{ stringify val }}` | String representation |

---

## Path Helpers (8)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `absolute` | `{{ absolute path n }}` | Directory segment |
| `dirname` | `{{ dirname path }}` | Get directory |
| `relative` | `{{ relative from to }}` | Relative path |
| `basename` | `{{ basename path }}` | Get filename |
| `stem` | `{{ stem path }}` | Filename without ext |
| `extname` | `{{ extname path }}` | Get extension |
| `resolve` | `{{ resolve paths... }}` | Resolve absolute path |
| `segments` | `{{ segments path start end }}` | Path segments range |

---

## URL Helpers (9)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `encodeURI` | `{{ encodeURI str }}` | Encode URI component |
| `escape` | `{{ escape str }}` | Escape for URL |
| `decodeURI` | `{{ decodeURI str }}` | Decode URI component |
| `url_encode` | `{{ url_encode str }}` | Alias for encodeURI |
| `url_decode` | `{{ url_decode str }}` | Alias for decodeURI |
| `urlResolve` | `{{ urlResolve base path }}` | Resolve URL |
| `urlParse` | `{{ urlParse url }}` | Parse URL to object |
| `stripQuerystring` | `{{ stripQuerystring url }}` | Remove query string |
| `stripProtocol` | `{{ stripProtocol url }}` | Remove protocol |

---

## Date Helpers (3)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `year` | `{{ year }}` | Current year |
| `date` | `{{ date }}` | Current date |
| `moment` | `{{ moment date format }}` | Format with moment.js |

---

## HTML Helpers (7)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `attr` | `{{ attr obj }}` | Stringify HTML attributes |
| `css` | `{{{ css path }}}` | Generate stylesheet link |
| `js` | `{{{ js path }}}` | Generate script tag |
| `sanitize` | `{{ sanitize html }}` | Strip HTML tags |
| `ul` | `{{{ ul array }}}` | Create unordered list |
| `ol` | `{{{ ol array }}}` | Create ordered list |
| `thumbnailImage` | `{{ thumbnailImage img }}` | Create figure with image |

---

## Markdown Helpers (2)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `markdown` | `{{{ markdown str }}}` | Convert inline markdown |
| `md` | `{{{ md filepath }}}` | Render markdown file |

---

## Regex Helpers (2)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `toRegex` | `{{ toRegex pattern flags }}` | Create RegExp |
| `test` | `{{#test str pattern}}...{{/test}}` | Test if matches |

---

## Match Helpers (3)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `match` | `{{ match str glob }}` | Match glob pattern |
| `isMatch` | `{{ isMatch path pattern }}` | Test if matches |
| `mm` | `{{ mm str pattern }}` | Alias for match |

---

## Collection Helpers (2)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `isEmpty` | `{{#isEmpty coll}}...{{/isEmpty}}` | Test if empty |
| `iterate` | `{{#iterate coll}}...{{/iterate}}` | Iterate collection |

---

## Inflection Helpers (2)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `inflect` | `{{ inflect count singular plural }}` | Pluralize |
| `ordinalize` | `{{ ordinalize num }}` | Convert to ordinal |

---

## Misc Helpers (5)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `frame` | `{{ frame }}` | Frame-related helper |
| `option` | `{{ option "key" }}` | Get from options |
| `noop` | `{{#noop}}...{{/noop}}` | Render without processing |
| `typeOf` | `{{ typeOf val }}` | Get native type |
| `withHash` | `{{#withHash k=v}}...{{/withHash}}` | Build context from hash |

---

## Logging Helpers (11)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `log` | `{{ log msg }}` | Console log |
| `ok` | `{{ ok msg }}` | Success logging |
| `success` | `{{ success msg }}` | Success message |
| `info` | `{{ info msg }}` | Info level |
| `warning` | `{{ warning msg }}` | Warning level |
| `warn` | `{{ warn msg }}` | Warning alias |
| `error` | `{{ error msg }}` | Error level |
| `danger` | `{{ danger msg }}` | Danger message |
| `bold` | `{{ bold text }}` | Bold formatting |
| `_debug` | `{{ _debug val }}` | Debug output |
| `_inspect` | `{{ _inspect val }}` | Inspect value |

---

## Code Helpers (3)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `embed` | `{{ embed filepath }}` | Embed file as preformatted |
| `gist` | `{{ gist id }}` | Embed GitHub Gist |
| `jsfiddle` | `{{ jsfiddle id }}` | Embed jsFiddle |

---

## FS Helpers (3)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `fileSize` | `{{ fileSize path }}` | Format file size |
| `read` | `{{ read filepath }}` | Read file contents |
| `readdir` | `{{ readdir path }}` | List directory files |

---

## i18n Helpers (1)

| Helper | Signature | Description |
|--------|-----------|-------------|
| `i18n` | `{{ i18n key }}` | Internationalization lookup |

---

## Usage Examples

### String Manipulation

```handlebars
{{! Convert string case }}
{{ camelcase "hello world" }}     {{! helloWorld }}
{{ pascalcase "hello world" }}    {{! HelloWorld }}
{{ snakecase "helloWorld" }}      {{! hello_world }}
{{ dashcase "helloWorld" }}       {{! hello-world }}

{{! String operations }}
{{ append (prepend name "Mr. ") " Jr." }}
{{ replace description "old" "new" }}
{{ truncate longText 50 }}
{{ split "a,b,c" "," }}
```

### Array Operations

```handlebars
{{! Get subset of array }}
{{ first items 3 }}
{{ last items 2 }}
{{ after items 5 }}
{{ before items 10 }}

{{! Array utilities }}
{{ length items }}
{{ join names ", " }}
{{ unique items }}
{{ sort items }}
{{ sortBy users "lastName" }}
{{ pluck users "email" }}

{{! Iteration with forEach }}
{{#forEach items}}
  {{#if @first}}First: {{/if}}
  {{@index}}: {{this}}
  {{#if @last}} (last){{/if}}
{{/forEach}}
```

### Comparisons

```handlebars
{{! Multiple conditions }}
{{#and isAdmin isActive}}
  Admin is active
{{/and}}

{{#or isAdmin isModerator}}
  Has elevated privileges
{{/or}}

{{! Numeric comparisons }}
{{#gt count 10}}More than 10{{/gt}}
{{#lte price 100}}Affordable{{/lte}}
{{#compare age ">=" 18}}Adult{{/compare}}

{{! Special conditions }}
{{#ifEven index}}Even row{{/ifEven}}
{{#ifOdd index}}Odd row{{/ifOdd}}
{{#isEmpty items}}No items{{/isEmpty}}
```

### Math Operations

```handlebars
{{! Basic math }}
Total: {{ add subtotal tax }}
Discount: {{ subtract price discount }}
Tax: {{ multiply price 0.1 }}
Average: {{ avg scores }}
Sum: {{ sum values }}

{{! Formatting }}
{{ round value }}
{{ ceil value }}
{{ floor value }}
{{ toFixed price 2 }}
```

### Object Access

```handlebars
{{! Access nested properties }}
{{ get user "address.city" }}
{{ get config "database.host" }}

{{! Iterate object }}
{{#forOwn settings}}
  {{@key}}: {{this}}
{{/forOwn}}

{{! JSON operations }}
{{ JSONstringify data }}
{{ JSONparse jsonString }}
```

### URL/Path Handling

```handlebars
{{! URL operations }}
{{ encodeURI query }}
{{ decodeURI encodedQuery }}
{{ stripQuerystring fullUrl }}
{{ stripProtocol url }}

{{! Path operations }}
{{ basename "/path/to/file.txt" }}   {{! file.txt }}
{{ dirname "/path/to/file.txt" }}    {{! /path/to }}
{{ extname "file.txt" }}             {{! .txt }}
{{ stem "file.txt" }}                {{! file }}
```
