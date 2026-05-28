# Data Types

All Convex documents are defined as JavaScript objects. These objects can have field values of any of the types below.

You can codify the shape of documents within your tables by [defining a schema](/database/schemas.md).

## Convex values[​](#convex-values "Direct link to Convex values")

Convex supports the following types of values:

| Convex Type | TS/JS Type                                                                                                                      | Example Usage          | Validator for [Argument Validation](/functions/validation.md) and [Schemas](/database/schemas.md) | `json` Format for [Export](/database/import-export/.md) | Notes                                                                                                                                                                                                                                                                                                                                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Id          | [Id](/database/document-ids.md) ([string](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)) | `doc._id`              | `v.id(tableName)`                                                                                 | string                                                  | See [Document IDs](/database/document-ids.md).                                                                                                                                                                                                                                                                                                         |
| Null        | [null](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#null_type)                                       | `null`                 | `v.null()`                                                                                        | null                                                    | JavaScript's `undefined` is not a valid Convex value. Functions the return `undefined` or do not return will return `null` when called from a client. Use `null` instead.                                                                                                                                                                              |
| Int64       | [bigint](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#bigint_type)                                   | `3n`                   | `v.int64()`                                                                                       | string (base10)                                         | Int64s only support BigInts between -2^63 and 2^63-1. Convex supports `bigint`s in [most modern browsers](https://caniuse.com/bigint).                                                                                                                                                                                                                 |
| Float64     | [number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#number_type)                                   | `3.1`                  | `v.number()`                                                                                      | number / string                                         | Convex supports all IEEE-754 double-precision floating point numbers (such as NaNs). Inf and NaN are JSON serialized as strings.                                                                                                                                                                                                                       |
| Boolean     | [boolean](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#boolean_type)                                 | `true`                 | `v.boolean()`                                                                                     | bool                                                    |                                                                                                                                                                                                                                                                                                                                                        |
| String      | [string](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#string_type)                                   | `"abc"`                | `v.string()`                                                                                      | string                                                  | Strings are stored as UTF-8 and must be valid Unicode sequences. Strings must be smaller than the 1MB total size limit when encoded as UTF-8.                                                                                                                                                                                                          |
| Bytes       | [ArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer)                     | `new ArrayBuffer(8)`   | `v.bytes()`                                                                                       | string (base64)                                         | Convex supports first class bytestrings, passed in as `ArrayBuffer`s. Bytestrings must be smaller than the 1MB total size limit for Convex types.                                                                                                                                                                                                      |
| Array       | [Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)                                 | `[1, 3.2, "abc"]`      | `v.array(values)`                                                                                 | array                                                   | Arrays can have at most 8192 values.                                                                                                                                                                                                                                                                                                                   |
| Object      | [Object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#objects)                                       | `{a: "abc"}`           | `v.object({property: value})`                                                                     | object                                                  | Convex only supports "plain old JavaScript objects" (objects that do not have a custom prototype). Convex includes all [enumerable properties](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Enumerability_and_ownership_of_properties). Objects can have at most 1024 entries. Field names must be nonempty and not start with "$" or "\_". |
| Record      | [Record](https://www.typescriptlang.org/docs/handbook/utility-types.html#recordkeys-type)                                       | `{"a": "1", "b": "2"}` | `v.record(keys, values)`                                                                          | object                                                  | Records are objects at runtime, but can have dynamic keys. Keys must be only ASCII characters, nonempty, and not start with "$" or "\_".                                                                                                                                                                                                               |

## System fields[​](#system-fields "Direct link to System fields")

Every document in Convex has two automatically-generated system fields:

* `_id`: The [document ID](/database/document-ids.md) of the document.
* `_creationTime`: The time this document was created, in milliseconds since the Unix epoch.

## Limits[​](#limits "Direct link to Limits")

Convex values must be less than 1MB in total size. This is an approximate limit for now, but if you're running into these limits and would like a more precise method to calculate a document's size, [reach out to us](https://convex.dev/community). Documents can have nested values, either objects or arrays that contain other Convex types. Convex types can have at most 16 levels of nesting, and the cumulative size of a nested tree of values must be under the 1MB limit.

Table names may contain alphanumeric characters ("a" to "z", "A" to "Z", and "0" to "9") and underscores ("\_"), and they cannot start with an underscore.

For information on other limits, see [here](/production/state/limits.md).

If any of these limits don't work for you, [let us know](https://convex.dev/community)!

## Working with `undefined`[​](#working-with-undefined "Direct link to working-with-undefined")

The TypeScript value `undefined` is not a valid Convex value, so it cannot be used in Convex function arguments or return values, or in stored documents.

1. Objects/records with `undefined` values are the same as if the field were missing: `{a: undefined}` is transformed into `{}` when passed to a function or stored in the database. You can think of Convex function calls and the Convex database as serializing the data with `JSON.stringify`, which similarly removes `undefined` values.

2. Validators for object fields can use `v.optional(...)` to indicate that the field might not be present.
   <!-- -->
   * If an object's field "a" is missing, i.e. `const obj = {};`, then `obj.a === undefined`. This is a property of TypeScript/JavaScript, not specific to Convex.

3. You can use `undefined` in filters and index queries, and it will match documents that do not have the field. i.e. `.withIndex("by_a", q=>q.eq("a", undefined))` matches document `{}` and `{b: 1}`, but not `{a: 1}` or `{a: null, b: 1}`.
   <!-- -->
   * In Convex's ordering scheme, `undefined < null < all other values`, so you can match documents that *have* a field via `q.gte("a", null as any)` or `q.gt("a", undefined)`.

4. There is exactly one case where `{a: undefined}` is different from `{}`: when passed to `ctx.db.patch`. Passing `{a: undefined}` removes the field "a" from the document, while passing `{}` does not change the field "a". See [Updating existing documents](/database/writing-data.md#updating-existing-documents).

5. Since `undefined` gets stripped from function arguments but has meaning in `ctx.db.patch`, there are some tricks to pass patch's argument from the client.

   <!-- -->

   * If the client passing `args={}` (or `args={a: undefined}` which is equivalent) should leave the field "a" unchanged, use `ctx.db.patch(id, args)`.
   * If the client passing `args={}` should remove the field "a", use `ctx.db.patch(id, {a: undefined, ...args})`.
   * If the client passing `args={}` should leave the field "a" unchanged and `args={a: null}` should remove it, you could do
     <!-- -->
     ```
     if (args.a === null) {
       args.a = undefined;
     }
     await ctx.db.patch(tableName, id, args);
     ```

6. Functions that return a plain `undefined`/`void` are treated as if they returned `null`.

7. Arrays containing `undefined` values, like `[undefined]`, throw an error when used as Convex values.

If you would prefer to avoid the special behaviors of `undefined`, you can use `null` instead, which *is* a valid Convex value.

## Working with dates and times[​](#working-with-dates-and-times "Direct link to Working with dates and times")

Convex does not have a special data type for working with dates and times. How you store dates depends on the needs of your application:

1. If you only care about a point in time, you can store a [UTC timestamp](https://en.wikipedia.org/wiki/Unix_time). We recommend following the `_creationTime` field example, which stores the timestamp as a `number` in milliseconds. In your functions and on the client you can create a JavaScript `Date` by passing the timestamp to its constructor: `new Date(timeInMsSinceEpoch)`. You can then print the date and time in the desired time zone (such as your user's machine's configured time zone).
   <!-- -->
   * To get the current UTC timestamp in your function and store it in the database, use `Date.now()`
2. If you care about a calendar date or a specific clock time, such as when implementing a booking app, you should store the actual date and/or time as a string. If your app supports multiple timezones you should store the timezone as well. [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) is a common format for storing dates and times together in a single string like `"2024-03-21T14:37:15Z"`. If your users can choose a specific time zone you should probably store it in a separate `string` field, usually using the [IANA time zone name](https://en.wikipedia.org/wiki/Tz_database#Names_of_time_zones) (although you could concatenate the two fields with unique character like `"|"`).

For more sophisticated printing (formatting) and manipulation of dates and times use one of the popular JavaScript libraries: [date-fns](https://date-fns.org/), [Day.js](https://day.js.org/), [Luxon](https://moment.github.io/luxon/) or [Moment.js](https://momentjs.com/).
