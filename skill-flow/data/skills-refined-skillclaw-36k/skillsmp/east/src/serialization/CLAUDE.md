# Serialization

East supports three serialization formats out of the box:

 - JSON: a canonical representation of an East value as JSON
 - East: a human-readable data format, intended as a subset of a future concrete syntax for the East programming language (like how JSON is a syntactical subset of JavaScript)
 - Beast: "binary east", a streaming binary data format similar to Avro

## Features

All formats support:

 - Unambiguous encoding and decoding any value of any East type
 - Circular references
 - Preservation of aliasing shared between mutable containers

Functions and closures cannot be serialized (but the IR defining them can).

## JSON

JSON is provided for interoperability with other systems unaware of East and lightweight debuggability.
For the JSON format it is supposed the East type is known in advance.

 - Float encoding supports `NaN`, `Infinity`, `-Infinity` and `-0.0` as strings
 - Integer encoding uses strings to support large integers outside the "safe" range
 - Collections (array/set/map) are represented as arrays of values
 - Variants and structs are represented as objects
 - Circular references and mutable aliases use relative JSON pointers and are encoded similarly as in JSON Schema
 
## East

The East format is how values are printed in East - for example automatically in string interpolation expressions.
It is a JSON-like encoding with distinct syntax for arrays, sets, dictionaries, structs, variants and all of East's primitive types.
A value is unambiguous with or without knowing the type in advance (though the tooling here supposes the type is given).

Circular references and mutable aliases use relative keypaths with a syntax like `3#.foo[0]` meaning "go up three levels, then get the `foo` field, then get the 0th element of that array.

User-friendly summaries of function signatures are printed for debugging purposes, but functions cannot be deserialized.

## Beast

### Version 1

Beast version 1 is deprecated, but we support the reading (and writing) of legacy data.

### Version 2

Beast version 2 is a self-describing format with a header consisting of magic bytes and a type definition.
Following this is the value itself, encoded with a compact, Avro-like format.

Circular references and mutable aliases use byte offsets to refer to values already written to the stream.