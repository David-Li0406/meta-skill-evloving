---
name: terraform-functions
description: 'Quick reference for Terraform built-in functions organized by category. Use when asked about "terraform functions", common functions (merge, concat, lookup, coalesce, length) or function categories (numeric, string, collection, encoding, filesystem, date/time, IP network, type conversion, crypto).'
---

# Terraform Functions Quick Reference

Comprehensive reference of all Terraform built-in functions organized by category. Use this skill to quickly identify which function to use for a specific task and where to find detailed documentation.

## When to Use This Skill

- User asks "what terraform functions are available"
- Questions about function categories or groups
- "How to manipulate strings/lists/maps in terraform"
- Looking for the right function for a specific task
- Need to know function signature or basic usage
- Want to explore available functions by category

## Function Overview

Terraform includes **100+ built-in functions** that you can use in expressions. Functions transform and combine values.

**General syntax:**
```hcl
function_name(arg1, arg2, ...)
```

**Example:**
```hcl
locals {
  uppercase_name = upper(var.name)
  combined_list  = concat(var.list1, var.list2)
  json_data      = jsondecode(file("config.json"))
}
```

**Testing functions:**
Use `terraform console` to experiment:
```bash
$ terraform console
> upper("hello")
"HELLO"
> length([1, 2, 3])
3
```

## Function Categories

Functions are organized into these categories:

1. **Numeric Functions** - Mathematical operations
2. **String Functions** - String manipulation
3. **Collection Functions** - List, map, and set operations
4. **Encoding Functions** - Encode/decode data formats
5. **Filesystem Functions** - Read files and paths
6. **Date and Time Functions** - Date/time manipulation
7. **Hash and Crypto Functions** - Hashing and encryption
8. **IP Network Functions** - CIDR and IP calculations
9. **Type Conversion Functions** - Convert between types
10. **Validation Functions** - Validate and test values
11. **Provider Functions** - Provider-specific functions (Terraform provider)

---

## Numeric Functions

Mathematical operations on numbers.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `abs(number)` | Absolute value | `abs(-5) → 5` | [abs](https://developer.hashicorp.com/terraform/language/functions/abs) |
| `ceil(number)` | Round up to nearest integer | `ceil(4.2) → 5` | [ceil](https://developer.hashicorp.com/terraform/language/functions/ceil) |
| `floor(number)` | Round down to nearest integer | `floor(4.8) → 4` | [floor](https://developer.hashicorp.com/terraform/language/functions/floor) |
| `log(number, base)` | Logarithm | `log(16, 2) → 4` | [log](https://developer.hashicorp.com/terraform/language/functions/log) |
| `max(number, ...)` | Maximum value | `max(5, 12, 9) → 12` | [max](https://developer.hashicorp.com/terraform/language/functions/max) |
| `min(number, ...)` | Minimum value | `min(5, 12, 9) → 5` | [min](https://developer.hashicorp.com/terraform/language/functions/min) |
| `parseint(string, base)` | Parse string to integer | `parseint("100", 10) → 100` | [parseint](https://developer.hashicorp.com/terraform/language/functions/parseint) |
| `pow(base, exponent)` | Exponentiation | `pow(2, 3) → 8` | [pow](https://developer.hashicorp.com/terraform/language/functions/pow) |
| `signum(number)` | Sign of number (-1, 0, 1) | `signum(-5) → -1` | [signum](https://developer.hashicorp.com/terraform/language/functions/signum) |
| `sum(list)` | Sum of list elements | `sum([1, 2, 3]) → 6` | [sum](https://developer.hashicorp.com/terraform/language/functions/sum) |

---

## String Functions

String manipulation and formatting.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `chomp(string)` | Remove trailing newlines | `chomp("hello\n") → "hello"` | [chomp](https://developer.hashicorp.com/terraform/language/functions/chomp) |
| `endswith(string, suffix)` | Check if string ends with suffix | `endswith("hello", "lo") → true` | [endswith](https://developer.hashicorp.com/terraform/language/functions/endswith) |
| `format(spec, values...)` | Format string (printf-style) | `format("Hello, %s", "World")` | [format](https://developer.hashicorp.com/terraform/language/functions/format) |
| `formatlist(spec, values...)` | Format each element in lists | `formatlist("ip-%s", ["a", "b"])` | [formatlist](https://developer.hashicorp.com/terraform/language/functions/formatlist) |
| `indent(spaces, string)` | Indent lines | `indent(4, "hello\nworld")` | [indent](https://developer.hashicorp.com/terraform/language/functions/indent) |
| `join(separator, list)` | Join list into string | `join(",", ["a", "b"]) → "a,b"` | [join](https://developer.hashicorp.com/terraform/language/functions/join) |
| `lower(string)` | Convert to lowercase | `lower("HELLO") → "hello"` | [lower](https://developer.hashicorp.com/terraform/language/functions/lower) |
| `regex(pattern, string)` | Match regex pattern | `regex("[0-9]+", "abc123")` | [regex](https://developer.hashicorp.com/terraform/language/functions/regex) |
| `regexall(pattern, string)` | Find all regex matches | `regexall("[0-9]+", "a1b2c3")` | [regexall](https://developer.hashicorp.com/terraform/language/functions/regexall) |
| `replace(string, search, replace)` | Replace substring | `replace("hello", "ll", "y")` | [replace](https://developer.hashicorp.com/terraform/language/functions/replace) |
| `split(separator, string)` | Split string into list | `split(",", "a,b,c") → ["a","b","c"]` | [split](https://developer.hashicorp.com/terraform/language/functions/split) |
| `startswith(string, prefix)` | Check if string starts with prefix | `startswith("hello", "he") → true` | [startswith](https://developer.hashicorp.com/terraform/language/functions/startswith) |
| `strcontains(string, substr)` | Check if string contains substring | `strcontains("hello", "ll") → true` | [strcontains](https://developer.hashicorp.com/terraform/language/functions/strcontains) |
| `strrev(string)` | Reverse string | `strrev("hello") → "olleh"` | [strrev](https://developer.hashicorp.com/terraform/language/functions/strrev) |
| `substr(string, offset, length)` | Extract substring | `substr("hello", 1, 3) → "ell"` | [substr](https://developer.hashicorp.com/terraform/language/functions/substr) |
| `templatestring(template, vars)` | Render template string | `templatestring("Hi ${name}", {name="World"})` | [templatestring](https://developer.hashicorp.com/terraform/language/functions/templatestring) |
| `title(string)` | Title case | `title("hello world") → "Hello World"` | [title](https://developer.hashicorp.com/terraform/language/functions/title) |
| `trim(string, chars)` | Trim characters from both ends | `trim("!!hello!!", "!")` | [trim](https://developer.hashicorp.com/terraform/language/functions/trim) |
| `trimprefix(string, prefix)` | Remove prefix | `trimprefix("helloworld", "hello")` | [trimprefix](https://developer.hashicorp.com/terraform/language/functions/trimprefix) |
| `trimspace(string)` | Trim whitespace | `trimspace(" hello ") → "hello"` | [trimspace](https://developer.hashicorp.com/terraform/language/functions/trimspace) |
| `trimsuffix(string, suffix)` | Remove suffix | `trimsuffix("helloworld", "world")` | [trimsuffix](https://developer.hashicorp.com/terraform/language/functions/trimsuffix) |
| `upper(string)` | Convert to uppercase | `upper("hello") → "HELLO"` | [upper](https://developer.hashicorp.com/terraform/language/functions/upper) |
| `urlencode(string)` | URL encode | `urlencode("hello world")` | [urlencode](https://developer.hashicorp.com/terraform/language/functions/urlencode) |

---

## Collection Functions

Operations on lists, maps, and sets.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `alltrue(list)` | Check if all elements are true | `alltrue([true, true]) → true` | [alltrue](https://developer.hashicorp.com/terraform/language/functions/alltrue) |
| `anytrue(list)` | Check if any element is true | `anytrue([true, false]) → true` | [anytrue](https://developer.hashicorp.com/terraform/language/functions/anytrue) |
| `chunklist(list, size)` | Split list into chunks | `chunklist([1,2,3,4], 2)` | [chunklist](https://developer.hashicorp.com/terraform/language/functions/chunklist) |
| `coalesce(values...)` | First non-null value | `coalesce(null, "a", "b") → "a"` | [coalesce](https://developer.hashicorp.com/terraform/language/functions/coalesce) |
| `coalescelist(lists...)` | First non-empty list | `coalescelist([], ["a"], ["b"])` | [coalescelist](https://developer.hashicorp.com/terraform/language/functions/coalescelist) |
| `compact(list)` | Remove empty strings from list | `compact(["a", "", "b"]) → ["a","b"]` | [compact](https://developer.hashicorp.com/terraform/language/functions/compact) |
| `concat(lists...)` | Concatenate lists | `concat([1,2], [3,4]) → [1,2,3,4]` | [concat](https://developer.hashicorp.com/terraform/language/functions/concat) |
| `contains(list, value)` | Check if list contains value | `contains(["a","b"], "a") → true` | [contains](https://developer.hashicorp.com/terraform/language/functions/contains) |
| `distinct(list)` | Remove duplicates | `distinct([1,2,2,3]) → [1,2,3]` | [distinct](https://developer.hashicorp.com/terraform/language/functions/distinct) |
| `element(list, index)` | Get element at index (wraps) | `element([1,2,3], 5) → 3` | [element](https://developer.hashicorp.com/terraform/language/functions/element) |
| `flatten(list)` | Flatten nested lists | `flatten([[1,2],[3,4]]) → [1,2,3,4]` | [flatten](https://developer.hashicorp.com/terraform/language/functions/flatten) |
| `index(list, value)` | Find index of value | `index(["a","b","c"], "b") → 1` | [index](https://developer.hashicorp.com/terraform/language/functions/index_function) |
| `keys(map)` | Get map keys | `keys({a=1, b=2}) → ["a","b"]` | [keys](https://developer.hashicorp.com/terraform/language/functions/keys) |
| `length(collection)` | Get length | `length([1,2,3]) → 3` | [length](https://developer.hashicorp.com/terraform/language/functions/length) |
| `list(values...)` | Create list (deprecated) | `list("a", "b")` | [list](https://developer.hashicorp.com/terraform/language/functions/list) |
| `lookup(map, key, default)` | Get value from map | `lookup({a=1}, "a", 0) → 1` | [lookup](https://developer.hashicorp.com/terraform/language/functions/lookup) |
| `map(key, value, ...)` | Create map (deprecated) | `map("a", 1, "b", 2)` | [map](https://developer.hashicorp.com/terraform/language/functions/map) |
| `matchkeys(values, keys, searchset)` | Filter values by key matches | `matchkeys(values, keys, ["a"])` | [matchkeys](https://developer.hashicorp.com/terraform/language/functions/matchkeys) |
| `merge(maps...)` | Merge maps | `merge({a=1}, {b=2})` | [merge](https://developer.hashicorp.com/terraform/language/functions/merge) |
| `one(list)` | Extract single element from list | `one([aws_instance.web])` | [one](https://developer.hashicorp.com/terraform/language/functions/one) |
| `range(start?, limit, step?)` | Generate number sequence | `range(3) → [0,1,2]` | [range](https://developer.hashicorp.com/terraform/language/functions/range) |
| `reverse(list)` | Reverse list | `reverse([1,2,3]) → [3,2,1]` | [reverse](https://developer.hashicorp.com/terraform/language/functions/reverse) |
| `setintersection(sets...)` | Set intersection | `setintersection([1,2], [2,3])` | [setintersection](https://developer.hashicorp.com/terraform/language/functions/setintersection) |
| `setproduct(sets...)` | Cartesian product | `setproduct([1,2], ["a","b"])` | [setproduct](https://developer.hashicorp.com/terraform/language/functions/setproduct) |
| `setsubtract(a, b)` | Set difference | `setsubtract([1,2,3], [2])` | [setsubtract](https://developer.hashicorp.com/terraform/language/functions/setsubtract) |
| `setunion(sets...)` | Set union | `setunion([1,2], [2,3])` | [setunion](https://developer.hashicorp.com/terraform/language/functions/setunion) |
| `slice(list, start, end)` | Extract slice | `slice([1,2,3,4], 1, 3) → [2,3]` | [slice](https://developer.hashicorp.com/terraform/language/functions/slice) |
| `sort(list)` | Sort list | `sort(["c","a","b"]) → ["a","b","c"]` | [sort](https://developer.hashicorp.com/terraform/language/functions/sort) |
| `transpose(map)` | Transpose map of lists | `transpose({a=["1","2"]})` | [transpose](https://developer.hashicorp.com/terraform/language/functions/transpose) |
| `values(map)` | Get map values | `values({a=1, b=2}) → [1,2]` | [values](https://developer.hashicorp.com/terraform/language/functions/values) |
| `zipmap(keys, values)` | Create map from lists | `zipmap(["a","b"], [1,2])` | [zipmap](https://developer.hashicorp.com/terraform/language/functions/zipmap) |

---

## Encoding Functions

Encode and decode various data formats.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `base64decode(string)` | Decode base64 | `base64decode("aGVsbG8=")` | [base64decode](https://developer.hashicorp.com/terraform/language/functions/base64decode) |
| `base64encode(string)` | Encode to base64 | `base64encode("hello")` | [base64encode](https://developer.hashicorp.com/terraform/language/functions/base64encode) |
| `base64gzip(string)` | Gzip compress and base64 encode | `base64gzip("hello")` | [base64gzip](https://developer.hashicorp.com/terraform/language/functions/base64gzip) |
| `csvdecode(string)` | Parse CSV to list of maps | `csvdecode("a,b\n1,2")` | [csvdecode](https://developer.hashicorp.com/terraform/language/functions/csvdecode) |
| `jsondecode(string)` | Parse JSON | `jsondecode("{\"a\":1}")` | [jsondecode](https://developer.hashicorp.com/terraform/language/functions/jsondecode) |
| `jsonencode(value)` | Encode to JSON | `jsonencode({a = 1})` | [jsonencode](https://developer.hashicorp.com/terraform/language/functions/jsonencode) |
| `textdecodebase64(string, encoding)` | Decode base64 with encoding | `textdecodebase64(str, "UTF-8")` | [textdecodebase64](https://developer.hashicorp.com/terraform/language/functions/textdecodebase64) |
| `textencodebase64(string, encoding)` | Encode to base64 with encoding | `textencodebase64(str, "UTF-8")` | [textencodebase64](https://developer.hashicorp.com/terraform/language/functions/textencodebase64) |
| `urlencode(string)` | URL encode | `urlencode("hello world")` | [urlencode](https://developer.hashicorp.com/terraform/language/functions/urlencode) |
| `yamldecode(string)` | Parse YAML | `yamldecode("a: 1\nb: 2")` | [yamldecode](https://developer.hashicorp.com/terraform/language/functions/yamldecode) |
| `yamlencode(value)` | Encode to YAML | `yamlencode({a = 1})` | [yamlencode](https://developer.hashicorp.com/terraform/language/functions/yamlencode) |

---

## Filesystem Functions

Read files and manipulate paths.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `abspath(path)` | Convert to absolute path | `abspath("./file.txt")` | [abspath](https://developer.hashicorp.com/terraform/language/functions/abspath) |
| `basename(path)` | Get filename from path | `basename("foo/bar.txt") → "bar.txt"` | [basename](https://developer.hashicorp.com/terraform/language/functions/basename) |
| `dirname(path)` | Get directory from path | `dirname("foo/bar.txt") → "foo"` | [dirname](https://developer.hashicorp.com/terraform/language/functions/dirname) |
| `file(path)` | Read file as string | `file("config.txt")` | [file](https://developer.hashicorp.com/terraform/language/functions/file) |
| `filebase64(path)` | Read file as base64 | `filebase64("image.png")` | [filebase64](https://developer.hashicorp.com/terraform/language/functions/filebase64) |
| `filebase64sha256(path)` | SHA256 hash of file (base64) | `filebase64sha256("file.txt")` | [filebase64sha256](https://developer.hashicorp.com/terraform/language/functions/filebase64sha256) |
| `filebase64sha512(path)` | SHA512 hash of file (base64) | `filebase64sha512("file.txt")` | [filebase64sha512](https://developer.hashicorp.com/terraform/language/functions/filebase64sha512) |
| `fileexists(path)` | Check if file exists | `fileexists("config.txt")` | [fileexists](https://developer.hashicorp.com/terraform/language/functions/fileexists) |
| `filemd5(path)` | MD5 hash of file | `filemd5("file.txt")` | [filemd5](https://developer.hashicorp.com/terraform/language/functions/filemd5) |
| `fileset(path, pattern)` | Find files matching pattern | `fileset(".", "*.txt")` | [fileset](https://developer.hashicorp.com/terraform/language/functions/fileset) |
| `filesha1(path)` | SHA1 hash of file | `filesha1("file.txt")` | [filesha1](https://developer.hashicorp.com/terraform/language/functions/filesha1) |
| `filesha256(path)` | SHA256 hash of file | `filesha256("file.txt")` | [filesha256](https://developer.hashicorp.com/terraform/language/functions/filesha256) |
| `filesha512(path)` | SHA512 hash of file | `filesha512("file.txt")` | [filesha512](https://developer.hashicorp.com/terraform/language/functions/filesha512) |
| `pathexpand(path)` | Expand ~ in path | `pathexpand("~/file.txt")` | [pathexpand](https://developer.hashicorp.com/terraform/language/functions/pathexpand) |
| `templatefile(path, vars)` | Render template file | `templatefile("tpl.txt", {name="x"})` | [templatefile](https://developer.hashicorp.com/terraform/language/functions/templatefile) |

---

## Date and Time Functions

Date and time manipulation.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `formatdate(format, timestamp)` | Format timestamp | `formatdate("YYYY-MM-DD", timestamp())` | [formatdate](https://developer.hashicorp.com/terraform/language/functions/formatdate) |
| `plantimestamp()` | Current timestamp (plan time) | `plantimestamp()` | [plantimestamp](https://developer.hashicorp.com/terraform/language/functions/plantimestamp) |
| `timeadd(timestamp, duration)` | Add duration to timestamp | `timeadd(timestamp(), "1h")` | [timeadd](https://developer.hashicorp.com/terraform/language/functions/timeadd) |
| `timecmp(a, b)` | Compare timestamps | `timecmp(t1, t2) → -1/0/1` | [timecmp](https://developer.hashicorp.com/terraform/language/functions/timecmp) |
| `timestamp()` | Current timestamp (UTC) | `timestamp() → "2024-01-20T10:30:00Z"` | [timestamp](https://developer.hashicorp.com/terraform/language/functions/timestamp) |

⚠️ **Note:** `timestamp()` is evaluated every time Terraform runs, causing perpetual differences. Use `plantimestamp()` for consistent plan-time timestamps.

---

## Hash and Crypto Functions

Hashing and cryptographic operations.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `base64sha256(string)` | SHA256 hash (base64) | `base64sha256("hello")` | [base64sha256](https://developer.hashicorp.com/terraform/language/functions/base64sha256) |
| `base64sha512(string)` | SHA512 hash (base64) | `base64sha512("hello")` | [base64sha512](https://developer.hashicorp.com/terraform/language/functions/base64sha512) |
| `bcrypt(string, cost?)` | Generate bcrypt hash | `bcrypt("password", 10)` | [bcrypt](https://developer.hashicorp.com/terraform/language/functions/bcrypt) |
| `md5(string)` | MD5 hash | `md5("hello")` | [md5](https://developer.hashicorp.com/terraform/language/functions/md5) |
| `rsadecrypt(ciphertext, key)` | RSA decrypt | `rsadecrypt(encrypted, private_key)` | [rsadecrypt](https://developer.hashicorp.com/terraform/language/functions/rsadecrypt) |
| `sha1(string)` | SHA1 hash | `sha1("hello")` | [sha1](https://developer.hashicorp.com/terraform/language/functions/sha1) |
| `sha256(string)` | SHA256 hash | `sha256("hello")` | [sha256](https://developer.hashicorp.com/terraform/language/functions/sha256) |
| `sha512(string)` | SHA512 hash | `sha512("hello")` | [sha512](https://developer.hashicorp.com/terraform/language/functions/sha512) |
| `uuid()` | Generate UUID | `uuid() → "b5ee72a3-..."` | [uuid](https://developer.hashicorp.com/terraform/language/functions/uuid) |
| `uuidv5(namespace, name)` | Generate UUID v5 | `uuidv5("dns", "example.com")` | [uuidv5](https://developer.hashicorp.com/terraform/language/functions/uuidv5) |

⚠️ **Note:** `uuid()` generates a new value each run, causing perpetual differences. Use only when necessary (e.g., with lifecycle `ignore_changes`).

---

## IP Network Functions

CIDR and IP address calculations.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `cidrhost(prefix, hostnum)` | Calculate IP address | `cidrhost("10.0.0.0/24", 5)` | [cidrhost](https://developer.hashicorp.com/terraform/language/functions/cidrhost) |
| `cidrnetmask(prefix)` | Get netmask from CIDR | `cidrnetmask("10.0.0.0/24")` | [cidrnetmask](https://developer.hashicorp.com/terraform/language/functions/cidrnetmask) |
| `cidrsubnet(prefix, newbits, netnum)` | Calculate subnet | `cidrsubnet("10.0.0.0/16", 8, 1)` | [cidrsubnet](https://developer.hashicorp.com/terraform/language/functions/cidrsubnet) |
| `cidrsubnets(prefix, newbits...)` | Calculate multiple subnets | `cidrsubnets("10.0.0.0/16", 8, 8)` | [cidrsubnets](https://developer.hashicorp.com/terraform/language/functions/cidrsubnets) |

---

## Type Conversion Functions

Convert values between types.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `can(expression)` | Test if expression succeeds | `can(regex("^[0-9]+$", var.input))` | [can](https://developer.hashicorp.com/terraform/language/functions/can) |
| `tobool(value)` | Convert to boolean | `tobool("true") → true` | [tobool](https://developer.hashicorp.com/terraform/language/functions/tobool) |
| `tolist(value)` | Convert to list | `tolist(toset([1,2,3]))` | [tolist](https://developer.hashicorp.com/terraform/language/functions/tolist) |
| `tomap(value)` | Convert to map | `tomap({a = 1, b = 2})` | [tomap](https://developer.hashicorp.com/terraform/language/functions/tomap) |
| `tonumber(value)` | Convert to number | `tonumber("42") → 42` | [tonumber](https://developer.hashicorp.com/terraform/language/functions/tonumber) |
| `toset(value)` | Convert to set | `toset([1, 2, 2, 3])` | [toset](https://developer.hashicorp.com/terraform/language/functions/toset) |
| `tostring(value)` | Convert to string | `tostring(42) → "42"` | [tostring](https://developer.hashicorp.com/terraform/language/functions/tostring) |
| `try(expressions...)` | Return first successful expression | `try(var.x, "default")` | [try](https://developer.hashicorp.com/terraform/language/functions/try) |
| `type(value)` | Get type of value | `type([1,2]) → "list"` | [type](https://developer.hashicorp.com/terraform/language/functions/type) |

---

## Validation and Testing Functions

Validate values and test conditions.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `can(expression)` | Test if expression succeeds | `can(regex("^ami-", var.ami_id))` | [can](https://developer.hashicorp.com/terraform/language/functions/can) |
| `ephemeralasnull(value)` | Convert ephemeral to null | `ephemeralasnull(ephemeral.value)` | [ephemeralasnull](https://developer.hashicorp.com/terraform/language/functions/ephemeralasnull) |
| `issensitive(value)` | Check if value is sensitive | `issensitive(var.password)` | [issensitive](https://developer.hashicorp.com/terraform/language/functions/issensitive) |
| `nonsensitive(value)` | Remove sensitive marking | `nonsensitive(sensitive_value)` | [nonsensitive](https://developer.hashicorp.com/terraform/language/functions/nonsensitive) |
| `sensitive(value)` | Mark value as sensitive | `sensitive(var.api_key)` | [sensitive](https://developer.hashicorp.com/terraform/language/functions/sensitive) |
| `try(expressions...)` | Return first successful expression | `try(var.x, var.y, "default")` | [try](https://developer.hashicorp.com/terraform/language/functions/try) |

---

## Provider-Defined Functions (Terraform Provider)

Built-in provider-specific functions from the `terraform` provider.

| Function | Purpose | Example | Documentation |
|----------|---------|---------|---------------|
| `provider::terraform::applying()` | Check if currently applying | `provider::terraform::applying()` | [applying](https://developer.hashicorp.com/terraform/language/functions/terraform-applying) |
| `provider::terraform::decode_tfvars(string)` | Parse tfvars format | `provider::terraform::decode_tfvars(file("vars.tfvars"))` | [decode_tfvars](https://developer.hashicorp.com/terraform/language/functions/terraform-decode_tfvars) |
| `provider::terraform::encode_expr(value)` | Encode to Terraform expression | `provider::terraform::encode_expr({a = 1})` | [encode_expr](https://developer.hashicorp.com/terraform/language/functions/terraform-encode_expr) |
| `provider::terraform::encode_tfvars(value)` | Encode to tfvars format | `provider::terraform::encode_tfvars({a = 1})` | [encode_tfvars](https://developer.hashicorp.com/terraform/language/functions/terraform-encode_tfvars) |

**Note:** Provider-specific functions use the `provider::<name>::<function>` syntax and require the provider to be declared in `required_providers`.

---

## Common Usage Patterns

### String Manipulation

```hcl
# Normalize naming
locals {
  normalized_name = lower(replace(var.name, "_", "-"))
  env_upper       = upper(var.environment)
}

# Template rendering
locals {
  user_data = templatefile("${path.module}/user-data.sh", {
    region      = var.region
    environment = var.environment
  })
}
```

### Collection Operations

```hcl
# Merge configurations
locals {
  default_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  all_tags = merge(local.default_tags, var.additional_tags)
}

# Filter and transform
locals {
  public_subnets = [
    for subnet in var.subnets : subnet.id
    if subnet.public == true
  ]
}

# Safely access with one()
locals {
  bucket = try(one(aws_s3_bucket.logs), null)
}
```

### File and Path Operations

```hcl
# Read configuration files
locals {
  config = jsondecode(file("${path.module}/config.json"))

  ssl_cert = fileexists("${path.module}/cert.pem") ?
    file("${path.module}/cert.pem") : null
}

# Hash for change detection
resource "aws_s3_object" "config" {
  bucket = aws_s3_bucket.config.id
  key    = "config.json"
  source = "${path.module}/config.json"
  etag   = filemd5("${path.module}/config.json")
}
```

### Type Conversion and Validation

```hcl
# Safe type conversion
locals {
  port = can(tonumber(var.port)) ? tonumber(var.port) : 8080
}

# Validation with can()
variable "ami_id" {
  type = string

  validation {
    condition     = can(regex("^ami-[a-f0-9]{8,}$", var.ami_id))
    error_message = "AMI ID must be valid format (ami-xxxxxxxx)."
  }
}

# Try with fallbacks
locals {
  db_endpoint = try(
    aws_db_instance.primary.endpoint,
    aws_db_instance.replica.endpoint,
    "localhost:5432"
  )
}
```

### Network Calculations

```hcl
# Calculate subnets
locals {
  vpc_cidr = "10.0.0.0/16"

  # Create /24 subnets
  subnet_cidrs = cidrsubnets(local.vpc_cidr, 8, 8, 8, 8)

  # Calculate specific IPs
  nat_gateway_ip = cidrhost(local.subnet_cidrs[0], 5)
}
```

---

## Finding More Information

**Official Documentation:**
- [Function Calls Overview](https://developer.hashicorp.com/terraform/language/expressions/function-calls)
- [All Functions Index](https://developer.hashicorp.com/terraform/language/functions)

**Testing Functions:**
```bash
# Interactive console
terraform console

# Example session
> upper("hello")
"HELLO"

> cidrsubnet("10.0.0.0/16", 8, 1)
"10.0.1.0/24"

> merge({a = 1}, {b = 2})
{
  "a" = 1
  "b" = 2
}
```

**Getting Function Signatures:**
```bash
# List all functions with signatures (Terraform v1.4+)
terraform metadata functions -json
```

---

## Best Practices

### Do's

✅ **Use descriptive variable names** when using complex function chains
```hcl
# Good
locals {
  normalized_bucket_name = lower(replace(var.bucket_name, "_", "-"))
}

# Avoid
locals {
  bn = lower(replace(var.bn, "_", "-"))
}
```

✅ **Use `try()` for safe access to potentially null values**
```hcl
# Good
locals {
  container_memory = try(var.container_definitions[0].memory, 512)
}
```

✅ **Use `can()` for validation**
```hcl
# Good validation
validation {
  condition     = can(regex("^[a-z0-9-]+$", var.name))
  error_message = "Name must contain only lowercase letters, numbers, and hyphens."
}
```

✅ **Use `one()` for count-based resources**
```hcl
# Good
output "bucket_id" {
  value = try(one(aws_s3_bucket.optional).id, null)
}
```

✅ **Test functions in terraform console before using**

### Don'ts

❌ **Don't use `uuid()` or `timestamp()` without lifecycle ignore_changes**
```hcl
# Bad - causes perpetual diff
resource "random_id" "example" {
  keepers = {
    timestamp = timestamp()  # Changes every run!
  }
}

# Good - use plantimestamp() or ignore_changes
resource "random_id" "example" {
  keepers = {
    timestamp = plantimestamp()  # Consistent during plan
  }
}
```

❌ **Don't over-nest function calls** - use locals for clarity
```hcl
# Bad - hard to read
resource "aws_s3_bucket" "example" {
  bucket = lower(replace(trimspace(var.name), "_", "-"))
}

# Good - clear steps
locals {
  cleaned_name     = trimspace(var.name)
  normalized_name  = replace(local.cleaned_name, "_", "-")
  bucket_name      = lower(local.normalized_name)
}

resource "aws_s3_bucket" "example" {
  bucket = local.bucket_name
}
```

❌ **Don't use file() for large files** - consider alternatives
```hcl
# Bad for large files
locals {
  large_config = jsondecode(file("large-config.json"))
}

# Consider: use data sources or external systems for large configs
```

❌ **Don't use deprecated functions** (`list()`, `map()`)
```hcl
# Bad - deprecated
locals {
  items = list("a", "b", "c")
  config = map("key", "value")
}

# Good - use literal syntax
locals {
  items = ["a", "b", "c"]
  config = { key = "value" }
}
```

---

## Quick Reference Summary

**Total Functions:** 100+ built-in functions

**Categories:**
- Numeric (10) - Math operations
- String (23) - Text manipulation
- Collection (30) - Lists, maps, sets
- Encoding (11) - JSON, YAML, CSV, Base64
- Filesystem (15) - Files and paths
- Date/Time (5) - Timestamps and formatting
- Hash/Crypto (10) - Hashing and encryption
- IP Network (4) - CIDR calculations
- Type Conversion (9) - Type conversions
- Validation (6) - Testing and validation
- Provider (4) - Terraform provider functions

**Most Commonly Used:**
- `try()` - Safe value access
- `merge()` - Merge maps
- `concat()` - Combine lists
- `length()` - Get collection size
- `lookup()` - Map value with default
- `jsondecode()` / `jsonencode()` - JSON handling
- `file()` - Read files
- `templatefile()` - Template rendering
- `cidrsubnet()` - Subnet calculations
- `one()` - Extract single element

**Documentation:** [https://developer.hashicorp.com/terraform/language/functions](https://developer.hashicorp.com/terraform/language/functions)
