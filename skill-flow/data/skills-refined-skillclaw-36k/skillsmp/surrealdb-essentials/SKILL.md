---
name: surrealdb-essentials
description: Essential SurrealDB knowledge. Always load this skill when writing or simply understanding SurrealQL queries, using the SDKs, designing schemas, or troubleshooting - this database has lots of quirks to be aware of.
---

# SurrealDB Essentials

## Overview

SurrealDB is a multi-model database that combines the functionality of traditional SQL databases with document, graph, vector, and key-value capabilities. It uses SurrealQL, a query language somewhat similar to SQL but with extensions for graph traversal, nested data structures, and real-time subscriptions.

## Structure

After connecting to send queries several things need to be specified:

- user - there are system users defined for global/namespace/database scope. Each scope has completely separate user pool, so user names can be the same across them
- namespace - SurrealDB can maintain multiple completely isolated namespaces
- database - each namespace can contain many databases - the databases are the ones that contain the schema and data

## SurrealQL overview

Files with Surreal Query Language should use the `.surql` extension.

## Key data types

SurrealDB uses two types called `NONE` and `NULL` to represent two different ways in which data may not exist:

- `NONE` - denotes that something doesn't exist - in JS it maps to `undefined`. Optional values can return `NONE`. Setting a record field to `NONE` is analogous to using `UNSET` to remove field entirely (schemaless).
- `NULL` - denotes that something exists, but has no value. JS equivalent is `null`.

`NONE` can be used as a datatype of it's own:

```
DEFINE FUNCTION fn::do_stuff() -> NONE {
  // Code that should return nothing
};

DEFINE FIELD middle_name ON TABLE user TYPE string | NONE; // Equivalent to option<string>

DEFINE FIELD value ON temperature TYPE float | decimal | NONE; // Equivalent to option<float|decimal>
```

- `any` - Use this when you explicitly don’t want to specify the field’s data type. The field will allow any data type supported by SurrealDB
- `array` - `array`/`array<string>`/`array<string, 10>` (capacity)
- `bool` - `true`/`false`
- `bytes` - Byte array, ie: `CREATE foo SET value = <bytes>"bar";`
- `datetime` - RFC 3339 - `d"2023-07-03T07:18:52Z"` `d"2023-07-03T07:18:52.841147+02:00"` `<datetime>"2024-04-03"` `d"2023-07-03T07:18:52Z" + 2w` `CREATE event SET time = d"2023-07-03T07:18:52.841147Z" + 1h30m20s1350ms;`
- `decimal` - `99.99dec`
- `duration`
- `float` - `41.5`
- `geometry`
- `int` - 64-bit
- `number` - can hold int/float/decimal
- `object` - Store formatted objects containing values of any supported type including nested objects or arrays
- `regex` - compiled regular expression
- `literal` - similar to an enum or a union type: `'a' | 'b'`, `[number, 'abc']`, `123 | 456 | string | 1y1m1d`
- `option<T>` - guarantees the field to be either empty (`NONE`), or type T, ie. `option<number>`
- `range` - `0..10`, `0..=10`, `..10`, `'a'..'z'`
- `record` - reference to another record (row): `record`, `record<user>`, `record<pallet | package>`
- `set` - `set`, `set<string>`, `set<string, 10>` (capacity)
- `string`

In the SurrealDB type system, values can be converted to other values efficiently - simply use the desired type in `<>`:

```
RETURN <array> 1..=3; -- cast range into array -- [1,2,3]
RETURN <array<int>> ["42", "314", "271", "137", "141"];
RETURN <array<string>> [42, 314, 271, 137, 141];
RETURN <bool> "true"; -- true
RETURN <datetime> "2025-06-07"; -- d'2025-06-07T00:00:00Z'
RETURN <decimal> "13.5729484672938472938410938456";
RETURN <duration> "1h30m"; -- 1h30m
RETURN <int> 53;
SELECT id FROM <record> (s"person:hrebrffwm4sr2yifglta");
SELECT id FROM <record> (s"person:hrebrffwm4sr2yifglta");
RETURN [
  <set<datetime|string>>["2020-09-09", "21 Jan 2020"],
  <set<string|datetime>>["2020-09-09", "21 Jan 2020"]
];
RETURN <string> 1.3463; -- '1.3463f'
RETURN <regex> "a|b" = "a"; -- true
SELECT id FROM <uuid> "a8f30d8b-db67-47ec-8b38-ef703e05ad1b"; -- [ u'a8f30d8b-db67-47ec-8b38-ef703e05ad1b' ]

-- All return a record person:one
RETURN r"person:one";
RETURN <record>"person:one";
RETURN <record<person>>"person:one";
-- Returns a string 'person:one'
RETURN "person:one";

-- Both return a decimal 98dec
RETURN 98dec;
RETURN <decimal>98;
-- Returns an int 98
RETURN 98;


```

## RecordID

SurrealDB record IDs are composed of a table name and a record identifier separated by a : in between, allowing for a simple and consistent way to reference records across the database. Record IDs are used to uniquely identify records within a table, to query, update, and delete records, and serve as links from one record to another.

Record IDs can be constructed from a number of ways, including alphanumeric text, complex Unicode text and symbols, numbers, arrays, objects, built-in ID generation functions, and a function to generate an ID from values.

All of the following are examples of valid record IDs in SurrealQL.

```
company:surrealdb
company:w6xb3izpgvz4n0gow6q7
reaction:`🤪`
weather:['London', d'2025-02-14T01:52:50.375Z']
```

In JS/TS the record IDs need to be explicitly defined to by type `RecordId`:

```
const settingId = new RecordId("setting", "log.retention_days");
const result = await this.surrealFactory.withSystemConnection({}, async (db) => {
  return await db.query<[Setting | undefined]>(
    `RETURN $settingId.*`,
    { settingId: settingId }
  );
});
```

## Key operators

```
RETURN 10 AND 20 AND 30; -- 30
RETURN 0 OR false OR 10; -- 10
RETURN !(TRUE OR FALSE); -- false
RETURN !"Has a value"; -- false
RETURN !!"Has a value"; -- true - Determines the truthiness of a value (simply an application of the ! operator twice)
RETURN NULL ?? 0 ?? false ?? 10; -- 0 Check whether either of two values are truthy and not NONE or NULL
RETURN NULL ?: 0 ?: false ?: 10; -- 10 Check whether either of two values are truthy

-- `=` is the same as `IS`
RETURN true = "true"; -- false
RETURN 10 = "10"; -- false
RETURN 10 = 10.00; -- true
RETURN 10 = "10.3"; -- false
RETURN [1, 2, 3] = [1, 2, 3]; -- true
RETURN [1, 2, 3] = [1, 2, 3, 4]; -- false
RETURN { this: "object" } = { this: "object" }; -- true
RETURN { this: "object" } = { another: "object" }; -- false

-- `!=` is the same as `IS NOT`
RETURN 10 != "15"; -- true

-- `<` `<=` `>` `>=` `+` `-` `*` `/` `**` are available as well
-- `CONTAINS` `CONTAINSNOT` `CONTAINSALL` `CONTAINSANY`
RETURN [10, 20, 30] CONTAINSALL [10, 20, 10]; -- true
RETUR- N "text" INSIDE "this is some text"; -- true
RETURN "name" IN { name: "Riga", country: "Latvia" }; -- true
```

## Helpful snippets

```
[1,3,5].filter(|$val| $val > 2); -- [3,5]
[1,3,5][WHERE $this > 2]; -- [3,5]
[1,2,3].map(|$item| $item + 1); -- [2,3,4]
[1,2,3].map(|$v, $i| "At index " + <string>$i + " we got a " + <string>$v + "!"); -- [ 'At index 0 we got a 1!', 'At index 1 we got a 2!', 'At index 2 we got a 3!' ]

rand::uuid::v4();
rand::uuid::v7();
<uuid> "a8f30d8b-db67-47ec-8b38-ef703e05ad1b";
u"a8f30d8b-db67-47ec-8b38-ef703e05ad1b";
```

## Key statements

### DEFINE USER

Use the DEFINE USER statement to create system users on SurrealDB
Syntax:

```
DEFINE USER [ OVERWRITE | IF NOT EXISTS ] @name
 ON [ ROOT | NAMESPACE | DATABASE ]
 [ PASSWORD @pass | PASSHASH @hash ]
 [ ROLES @roles ]
 [ DURATION ( FOR TOKEN @duration [ , ] [ FOR SESSION @duration ] | FOR SESSION @duration [ , ] [ FOR TOKEN @duration ] ) ]
  [ COMMENT @string ]
```

Examples:

```
-- Create the user with an owner role and some example durations
DEFINE USER username ON ROOT PASSWORD '123456' ROLES OWNER DURATION FOR SESSION 15m, FOR TOKEN 5s;

-- Specify the namespace
USE NS abcum;
-- Create the user with an editor role and some example durations
DEFINE USER username ON NAMESPACE PASSWORD '123456' ROLES EDITOR DURATION FOR SESSION 12h, FOR TOKEN 1m;

-- Specify the namespace and database for the user
USE NS abcum DB app_vitalsense;
-- Create the user with a viewer role and some example durations
DEFINE USER username ON DATABASE PASSWORD '123456' ROLES VIEWER DURATION FOR SESSION 5d, FOR TOKEN 2h;

-- Create a USER if it does not already exist
DEFINE USER IF NOT EXISTS example ON ROOT PASSWORD "example" ROLES OWNER;

-- Create an USER and overwrite if it already exists
DEFINE USER OVERWRITE example ON ROOT PASSWORD "example" ROLES OWNER;
```

Currently, only the built-in roles OWNER, EDITOR and VIEWER are available.

### DEFINE TABLE

The DEFINE TABLE statement allows you to declare your table by name, enabling you to apply strict controls to a table’s schema by making it SCHEMAFULL, create a foreign table view, and set permissions specifying what operations can be performed on the table.

Syntax:

```
DEFINE TABLE [ OVERWRITE | IF NOT EXISTS ] @name
 [ DROP ]
 [ SCHEMAFULL | SCHEMALESS ]
 [ TYPE [ ANY | NORMAL | RELATION [ IN | FROM ] @table [ OUT | TO ] @table [ ENFORCED ]]]
 [ AS SELECT @projections
  FROM @tables
  [ WHERE @condition ]
  [ GROUP [ BY @groups | ALL ] ]
 ]
 [ CHANGEFEED @duration [ INCLUDE ORIGINAL ] ]
 [ PERMISSIONS [ NONE | FULL
  | FOR select @expression
  | FOR create @expression
  | FOR update @expression
  | FOR delete @expression
 ] ]
    [ COMMENT @string ]
```

The following example demonstrates the SCHEMAFULL portion of the DEFINE TABLE statement. When a table is defined as schemafull, the database strictly enforces any schema definitions that are specified using the DEFINE TABLE statement. New fields can not be added to a SCHEMAFULL table unless they are defined via the DEFINE FIELD statement.

```
-- Create schemafull user table.
DEFINE TABLE user SCHEMAFULL;

-- Define some fields.
DEFINE FIELD firstName ON TABLE user TYPE string;
DEFINE FIELD lastName ON TABLE user TYPE string;
DEFINE FIELD email ON TABLE user TYPE string
  ASSERT string::is_email($value);
DEFINE INDEX userEmailIndex ON TABLE user COLUMNS email UNIQUE;
```

The following example demonstrates the SCHEMALESS portion of the DEFINE TABLE statement. This allows you to explicitly state that the specified table has no schema.

```
-- Create schemaless user table.
DEFINE TABLE user SCHEMALESS;

-- Define some fields.
DEFINE FIELD firstName ON TABLE user TYPE string;
DEFINE FIELD lastName ON TABLE user TYPE string;
DEFINE FIELD email ON TABLE user TYPE string
  ASSERT string::is_email($value);
DEFINE INDEX userEmailIndex ON TABLE user COLUMNS email UNIQUE;
```

Using ENFORCED to ensure that related records exist
[More about DEFINE TABLE, table types and views](define_table.md)

### Defining fields

The DEFINE FIELD statement allows you to instantiate a named field on a table, enabling you to set the field’s data type, set a default value, apply assertions to protect data consistency, and set permissions specifying what operations can be performed on the field

Syntax (regular):

```
DEFINE FIELD [ OVERWRITE | IF NOT EXISTS ] @name ON [ TABLE ] @table
 [ TYPE @type | object [ FLEXIBLE ] ]
 [ REFERENCE 
  [ ON DELETE REJECT | 
   ON DELETE CASCADE | 
   ON DELETE IGNORE |
   ON DELETE UNSET | 
   ON DELETE THEN @expression ]
 ]
 [ DEFAULT [ALWAYS] @expression ]
  [ READONLY ]
 [ VALUE @expression ]
 [ ASSERT @expression ]
 [ PERMISSIONS [ NONE | FULL
  | FOR select @expression
  | FOR create @expression
  | FOR update @expression
 ] ]
  [ COMMENT @string ]
```

Examples:

```
-- Declare the name of a field.
DEFINE FIELD email ON TABLE user;
```

The DEFINE FIELD statement allows you to set the data type of a field. For a full list of supported data types, see Data types. When defining nested fields, where both the parent and the nested fields have types defined, it is no longer possible to have mismatching types, to prevent any impossible type issues once the schema is defined.

```
-- Set a field to have the string data type
DEFINE FIELD email ON TABLE user TYPE string;

-- Set a field to have the array data type
DEFINE FIELD roles ON TABLE user TYPE array<string>;

-- Field for a block in a game showing the possible directions a character can move next.
-- The array can contain no more than four directions
DEFINE FIELD next_paths ON TABLE block TYPE array<"north" | "east" | "south" | "west", 4>;
```

Flexible types allow you to have SCHEMALESS functionality on a SCHEMAFULL table. This is necessary for working with nested object types that need to be able to accept fields that have not yet been defined

You can set a default value for a field using the DEFAULT clause. The default value will be used if no value is provided for the field.

```
-- A user is not locked by default.
DEFINE FIELD locked ON TABLE user TYPE bool
-- Set a default value if empty
  DEFAULT false;
```

In addition to the DEFAULT clause, you can use the DEFAULT ALWAYS clause to set a default value for a field. The ALWAYS keyword indicates that the DEFAULT clause is used not only on CREATE, but also on UPDATE if the value is empty (NONE).

```
DEFINE TABLE product SCHEMAFULL;
-- Set a default value of 123.456 for the primary field
DEFINE FIELD primary ON product TYPE number DEFAULT ALWAYS 123.456;
```

The VALUE clause differs from DEFAULT in that a default value is calculated if no other is indicated, otherwise accepting the value given in a query. A VALUE clause, on the other hand, will ignore attempts to set the field to any other value.

```
DEFINE FIELD updated ON TABLE user VALUE time::now();

-- Ignores 1900 date, sets `updated` to current time
CREATE user SET updated = d"1900-01-01";
-- Ignores again, updates to current time
UPDATE user SET updated = d"1900-01-01";
```

As the example above shows, a VALUE clause sets the value every time a record is modified (created or updated). However, the value will not be recalculated in a SELECT statement, which simply accesses the current set value.

```
DEFINE FIELD updated ON TABLE user VALUE time::now();

CREATE user:one;
SELECT * FROM ONLY user:one;
-- Sleep for one second
SLEEP 1s;
-- `updated` is still the same
SELECT * FROM ONLY user:one;
```

You can alter a passed value using the VALUE clause. This is useful for altering the value of a field before it is stored in the database.

In the example below, the VALUE clause is used to ensure that the email address is always stored in lowercase characters by using the string::lowercase function.

```
-- Ensure that an email address is always stored in lowercase characters
DEFINE FIELD email ON TABLE user TYPE string
  VALUE string::lowercase($value);
```

You can take your field definitions even further by using asserts. Assert can be used to ensure that your data remains consistent. For example you can use asserts to ensure that a field is always a valid email address, or that a number is always positive

```
-- Give the user table an email field. Store it in a string
DEFINE FIELD email ON TABLE user TYPE string
  -- Check if the value is a properly formatted email address
  ASSERT string::is_email($value);
```

As the ASSERT clause expects an expression that returns a boolean, an assertion with a custom message can be manually created by returning true in one case and using a THROW clause otherwise.

```
DEFINE FIELD num ON data TYPE int ASSERT {
    IF $input % 2 = 0 {
        RETURN true
    } ELSE {
        THROW "Tried to make a " + <string>$this + " but `num` field requires an even number"
    }
};

CREATE data:one SET num = 11;
```

Error output:

```
'An error occurred: Tried to make a { id: data:one, num: 11 } but `num` field requires an even number'
```

The READONLY clause can be used to prevent any updates to a field. This is useful for fields that are automatically updated by the system. To make a field READONLY, add the READONLY clause to the DEFINE FIELD statement. As seen in the example below, the created field is set to READONLY.

```
DEFINE FIELD created ON resource VALUE time::now() READONLY;
```

[More about DEFINE FIELD](define_field.md)

### Defining events (triggers)

Events allow you to define custom logic that is executed when a record is created, updated, or deleted. These events are triggered automatically within the current transaction after data modifications in the record, giving you access to the state of the record before $before and after $after the change

- Events: Triggered after changes (create, update, delete) to records in a table.
- $event: A preset parameter containing the type of event as a string, will always be one of “CREATE”, “UPDATE”, or “DELETE”.
- $before / $after: Refer to the record state before and after the modification.
- $value: The record in question. For a CREATE or UPDATE event, this will be the record after the changes were made. For a DELETE statement, this will be the record before it was deleted.
- WHEN condition: Determines when the event should be triggered

Syntax:

```
DEFINE EVENT [ OVERWRITE | IF NOT EXISTS ] @name ON [ TABLE ] @table [ WHEN @expression ] THEN @expression [ COMMENT @string ]
```

- OVERWRITE: Replaces the existing event if it already exists
- IF NOT EXISTS: Only creates the event if it doesn’t already exist.
- WHEN: Conditional logic that controls whether the event is triggered
- THEN: Specifies the action(s) to execute when the event is triggered.
- COMMENT: Optional comment for describing the event

Email Change Detection: Create an event that logs whenever a user’s email is updated:

```
-- Create a new event whenever a user changes their email address
-- One-statement event
DEFINE EVENT OVERWRITE test ON TABLE user WHEN $before.email != $after.email THEN (
    CREATE log SET 
        user       = $value.id,
        // Turn events like "CREATE" into string "email created"
        action     = 'email' + ' ' + $event.lowercase() + 'd',
        // `email` field may be NONE, log as '' if so
        old_email  = $before.email ?? '',
        new_email  = $after.email  ?? '',
        at         = time::now()
);
UPSERT user:test SET email = 'old_email@test.com';
UPSERT user:test SET email = 'new_email@test.com';
DELETE user:test;
SELECT * FROM log ORDER BY at ASC;
```

Purchase Event with Multiple Actions: Log a purchase and establish relationships between the customer and product

```
DEFINE EVENT purchase_made ON TABLE purchase
    WHEN $before == NONE
    THEN {
        LET $customer = (SELECT * FROM customer WHERE id = $after.customer);
        LET $product = (SELECT * FROM product WHERE id = $after.product);

        RELATE $customer->bought->$product CONTENT {
            quantity: $after.quantity,
            total: $after.total,
            status: 'Pending',
        };

        CREATE log SET
            customer_id = $after.customer,
            product_id = $after.product,
            action = 'purchase_created',
            timestamp = time::now();
    };
```

You can trigger events based on specific events. You can use the variable $event to detect what type of event is triggered on the table

```
-- CREATE event is triggered when a new record is inserted into the table.
-- Here we are updating the status of the post to PUBLISHED
-- when a new record is inserted into the publish_post table.
DEFINE EVENT publish_post ON TABLE publish_post
    WHEN $event = "CREATE"
    THEN (
        UPDATE post SET status = "PUBLISHED" WHERE id = $after.post_id
    );

-- UPDATE event
-- Here we are creating a notification when a user is updated.
DEFINE EVENT user_updated ON TABLE user
    WHEN $event = "UPDATE"
    THEN (
        CREATE notification SET message = "User updated", user_id = $after.id, created_at = time::now()
    );

-- DELETE event is triggered when a record is deleted from the table.
-- Here we are creating a notification when a user is deleted.
DEFINE EVENT user_deleted ON TABLE user
    WHEN $event = "DELETE"
    THEN (
        CREATE notification SET message = "User deleted", user_id = $before.id, created_at = time::now()
    );

-- You can combine multiple events based on your use cases.
-- Here we are creating a log when a user is created, updated or deleted.
DEFINE EVENT user_event ON TABLE user
    WHEN $event = "CREATE" OR $event = "UPDATE" OR $event = "DELETE"
    THEN (
        CREATE log SET
            table = "user",
            event = $event,
            happened_at = time::now()
    );
```

The behaviour of events can be further refined via the $input parameter, which represents the record in question for the event

```
-- Set CREATE in event to only trigger when record has `true` for `log_event`
DEFINE EVENT something ON person WHEN $input.log_event = true THEN {
    CREATE log SET at = time::now(), of = $input;
};

-- Set to `false`, does not trigger CREATE
CREATE person:debug SET name = "Billy", log_event = false;
-- Triggers CREATE
CREATE person:real SET name = "Bobby", log_event = true;

SELECT * FROM log;
```

### Defining functions

The DEFINE FUNCTION statement allows you to define custom functions that can be reused throughout a database. When using the DEFINE FUNCTION statement, you can define a function that takes one or more arguments and returns a value. You can then call this function in other SurrealQL statements.

Functions can be used to encapsulate logic that you want to reuse in multiple queries. They can also be used to simplify complex queries by breaking them down into smaller, more manageable pieces. The are particularly useful when you have a complex query that you need to run multiple times with different arguments

Syntax:

```
DEFINE FUNCTION [ OVERWRITE | IF NOT EXISTS ] fn::@name( [ @argument: @type ... ] ) [ -> @value ] {
 [ @query ... ]
 [ RETURN @returned ]
} [ COMMENT @string ] [ PERMISSIONS [ NONE | FULL | WHERE @condition]]
```

Below shows how you can define a custom function using the DEFINE FUNCTION statement, and how to call it

```
-- It is necessary to prefix the name of your function with "fn::"
-- This indicates that it's a custom function
DEFINE FUNCTION fn::greet($name: string) {
 "Hello, " + $name + "!"
};

-- Returns: "Hello, Tobie!"
RETURN fn::greet("Tobie");
```

To showcase a slightly more complex custom function, this will check if a relation between two nodes exists

```
-- Define a function that checks if a relation exists between two nodes
DEFINE FUNCTION fn::relation_exists(
 $in: record,
 $tb: string,
 $out: record
) {
 -- Check if a relation exists between the two nodes.
 LET $results = SELECT VALUE id FROM type::table($tb) WHERE in = $in AND out = $out;
 -- Return true if a relation exists, false otherwise
    RETURN array::len($results) > 0;
};
```

If one or more ending arguments have the option<T> type, they can be omitted when you run the invoke the function

```
DEFINE FUNCTION fn::last_option($required: number, $optional: option<number>) {
 RETURN {
  required_present: type::is_number($required),
  optional_present: type::is_number($optional),
 }
};

RETURN fn::last_option(1, 2);
-- { required_present: true, optional_present: true }

RETURN fn::last_option(1);
-- { required_present: true, optional_present: false };
```

Optionally, the return value of a function can be specified.

For a function that is infallible, a return value is mostly for the sake of readability

```
DEFINE FUNCTION fn::greet($name: string) -> string {
 "Hello, " + $name + "!"
};
```

For a function that is not infallible, specifying a return value can be used to customise error output

```
// Arguments must be of type 'number'
DEFINE FUNCTION fn::combine($one: number, $two: number) -> number {
  $one + $two
};

// Accepts any value but expects the return type 'number'
DEFINE FUNCTION fn::combine_any($one: any, $two: any) -> number {
  $one + $two
};

fn::combine("one", "two");
fn::combine_any("one", "two");
```

The return value of a function can even be a literal type. The following function returns such a type by either returning an object of a certain structure, or a string. In this case this output is used in case an application prefers to return an error as a simple string instead of throwing an error or returning a NONE value

```
DEFINE FUNCTION fn::age_and_name($user_num: int) -> { age: int, name: string } | string {
    LET $user = type::record("user", $user_num);
    IF $user.exists() {
        $user.{ name, age }
    } ELSE {
        { "Couldn't find user number " + <string>$user_num + "!" }        
    }
};

CREATE user:1 SET name = "Billy", age = 15;

fn::age_and_name(1);
fn::age_and_name(2);
```

A function is able to call itself, making it a recursive function. One example of a recursive function is the one below which creates a relation between each and every record passed in.

Consider a situation in which seven person records exist. First, person:1 will need to be related to the rest of the person records, after which there are no more relations to create for it. Following this, the relations for person:2 and all the other records except for person:1 will need to be created, and so on.

This can be done in a recursive function by creating all the relations between the first record and the remaining records, after which the function calls itself by passing in all the records except the first. This continues until the function receives less than two records, in which case it ceases calling itself by doing nothing, thereby ending the recursion.

```
DEFINE FUNCTION fn::relate_all($records: array<record>) {
  IF $records.len() < 2 {
      -- Don't do anything, ending the recursion
  }  ELSE {
      LET $first = $records[0];
      LET $remainder = $records[1..];
      FOR $counterpart IN $remainder {
          RELATE $first->to->$counterpart;
      };
      fn::relate_all($remainder);
  }
};

CREATE |person:1..8|;

fn::relate_all(SELECT VALUE id FROM person);

SELECT id, ->to->? FROM person;
```

### Defining indexes

Just like in other databases, SurrealDB uses indexes to help optimize query performance. An index can consist of one or more fields in a table and can enforce a uniqueness constraint. If you don’t intend for your index to have a uniqueness constraint, then the fields you select for your index should have a high degree of cardinality, meaning that there is a high amount of diversity between the data in the indexed table records

Syntax:

```
DEFINE INDEX [ OVERWRITE | IF NOT EXISTS ] @name
    ON [ TABLE ] @table 
    [ FIELDS | COLUMNS ] @fields
    [ @special_clause ]
    [ COMMENT @string ]
    [ CONCURRENTLY ]
    [ DEFER ]
```

The @special_clause part of the statement is an optional part in which an index can be declared for special usage such as guaranteeing unique values, full-text search, and so on. The available clauses are:

```
UNIQUE
| COUNT
| FULLTEXT ANALYZER @analyzer [ BM25 [(@k1, @b)] ] [ HIGHLIGHTS ]
| HNSW DIMENSION @dimension [ TYPE @type ] [DIST @distance] [ EFC @efc ] [ M @m ]
```

SurrealDB offers a range of indexing capabilities designed to optimize data retrieval and search efficiency

An index without any special clauses allows for the indexing of attributes that may have non-unique values, facilitating efficient data retrieval. Non-unique indexes help index frequently appearing data in queries that do not require uniqueness, such as categorization tags or status indicators.

```
-- optimise queries looking for users of a given age
DEFINE INDEX userAgeIndex ON TABLE user COLUMNS age;
```

Unique index - Ensures each value in the index is unique. A unique index helps enforce uniqueness across records by preventing duplicate entries in fields such as user IDs, email addresses, and other unique identifiers

```
DEFINE INDEX userEmailIndex ON TABLE user COLUMNS email UNIQUE;
DEFINE INDEX test ON user FIELDS account, email UNIQUE;
```

An index using the COUNT clause is used to maintain a count of the number of records in a table. This is used together with the count() function and GROUP ALL inside a query. Without a count index, the count() function will iterate through the records of a table when it is called

DEFINE INDEX idx ON indexed_reading COUNT;

FOR $_ IN 0..100000 {
    CREATE reading SET temperature = rand::int(0, 10);
};

FOR $_IN 0..100000 {
    CREATE indexed_reading SET temperature = rand::int(0, 10);
};

-- Wait a moment before running these two
-- queries to ensure the index is built
SELECT count() FROM reading GROUP ALL;
SELECT count() FROM indexed_reading GROUP ALL;

As a count index is declared on a table as a whole, it cannot use the FIELDS / COLUMNS clause

```
-- Other clauses like `COMMENT` are fine
DEFINE INDEX idx ON users COUNT
    COMMENT "Users are expected to grow substantially so index the count"
    CONCURRENTLY;

-- But not `FIELD`
DEFINE INDEX idx2 ON person FIELD name;
```

### Defining params

The DEFINE PARAM statement allows you to define global (database-wide) parameters that are available to every client

Syntax:

```
DEFINE PARAM [ OVERWRITE | IF NOT EXISTS ] $@name 
    VALUE @value
    [ COMMENT @string ]
    [ PERMISSIONS [ NONE | FULL | WHERE @condition ] ]
```

Below shows how you can create a parameter using the DEFINE PARAM statement

```
DEFINE PARAM $endpointBase VALUE "https://dummyjson.com";
```

Then, simply use the global parameter like you would with any variable

```
RETURN http::get($endpointBase + "/products");
```

### SELECT

The SELECT statement can be used for selecting and querying data in a database. Each SELECT statement supports selecting from multiple targets, which can include tables, records, edges, subqueries, parameters, arrays, objects, and other values

Syntax:

```
SELECT 
    VALUE @field | @fields [ AS @alias ] [ OMIT @fields ... ]
    FROM [ ONLY ] @targets
    [ WITH [ NOINDEX | INDEX @indexes ... ]]
    [ WHERE @conditions ]
    [ SPLIT [ ON ] @field, ... ]
    [ GROUP [ ALL | [ BY ] @field, ... ]]
    [ ORDER [ BY ] 
        @field [ COLLATE ] [ NUMERIC ] [ ASC | DESC ], ...
        | RAND() ]
    [ LIMIT [ BY ] @limit ]
    [ START [ AT ] @start 0 ]
    [ FETCH @fields ... ]
    [ TIMEOUT @duration ]
    [ TEMPFILES ]
    [ EXPLAIN [ FULL ]]
;
```

By default, SurrealDB returns an array of JSON-like objects called records instead of a tabular structure of rows and columns

```
CREATE person:tobie SET
 name.first = "Tobie",
 address = "1 Bagshot Row",
 email = "tobie@surrealdb.com";

-- Select all fields from a table
SELECT * FROM person;

-- Select specific fields from a table
SELECT name, address, email FROM person;

-- Select all fields from a specific record
SELECT * FROM person:tobie;

-- Select specific fields from a specific record
SELECT name, address, email FROM person:tobie;

-- Select just a single record
-- Using the ONLY keyword, just an object
-- for the record in question will be returned.
-- This, instead of an array with a single object.
SELECT * FROM ONLY person:tobie;
```

An alias can be used to rename fields or change the structure of an object

```
SELECT * FROM person;

-- Field `address` now shows up as "string::uppercase"
-- name.first structure now flattened into a simple field
SELECT
 name.first AS user_name,
 string::uppercase(address)
FROM person;

-- "Morgan Hitchcock" added to `name` field structure,
-- `angry_address` for field name instead of automatically
-- generated "string::uppercase(address) + '!!!'"
SELECT
 name.first,
 "Morgan Hitchcock" AS name.last,
 string::uppercase(address) + "!!!" AS angry_address
FROM person;
```

Output:

```
-------- Query --------

[
 {
  address: '1 Bagshot Row',
  email: 'tobie@surrealdb.com',
  id: person:tobie,
  name: {
   first: 'Tobie'
  }
 }
]

-------- Query --------

[
 {
  "string::uppercase": '1 BAGSHOT ROW',
  user_name: 'Tobie'
 }
]

-------- Query --------

[
 {
  angry_address: '1 BAGSHOT ROW!!!',
  name: {
   first: 'Tobie',
   last: 'Morgan Hitchcock'
  }
 }
]
```

SurrealDB can also return specific fields as an array of values instead of the default array of objects. This only works if you select a single un-nested field from a table or a record.

```
-- Select the values of a single field from a table
SELECT VALUE name FROM person;

-- Select the values of a single field from a specific record
SELECT VALUE name FROM person:00e1nc508h9f7v63x72O;
```

SELECT queries support advanced expression in the field projections

```
-- Select nested objects/values
SELECT address.city FROM person;

-- Select all nested array values
-- note the .* syntax works to select everything from an array or object-like values
SELECT address.*.coordinates AS coordinates FROM person;
-- Equivalent to
SELECT address.coordinates AS coordinates FROM person;

-- Select one item from an array
SELECT address.coordinates[0] AS latitude FROM person;

-- Select unique values from an array
SELECT array::distinct(tags) FROM article;

-- Select unique values from a nested array across an entire table
SELECT array::group(tags) AS tags FROM article GROUP ALL;

-- Use mathematical calculations in a select expression
SELECT
 (( celsius * 1.8 ) + 32) AS fahrenheit
 FROM temperature;

-- Return boolean expressions with an alias
SELECT rating >= 4 as positive FROM review;

-- Select manually generated object structure
SELECT
 { weekly: false, monthly: true } AS `marketing settings`
FROM user;

-- Select filtered nested array values
SELECT address[WHERE active = true] FROM person;

-- Select a person who has reacted to a post using a celebration
-- Path can be conceptualized as:
-- person->(reacted_to WHERE type='celebrate')->post
SELECT * FROM person WHERE ->(reacted_to WHERE type='celebrate')->post;

-- Select a remote field from connected out graph edges
SELECT ->likes->friend.name AS friends FROM person:tobie;

-- Use the result of a subquery as a returned field
SELECT *, (SELECT * FROM events WHERE type = 'activity' LIMIT 5) AS history FROM user;

-- Restructure objects in a select expression after `.` operator
SELECT address.{city, country} FROM person;
```

Parameters can be used like variables to store a value which can then be used in a subsequent query

```
-- Store the subquery result in a variable and query that result.
LET $avg_price = (
 SELECT math::mean(price) AS avg_price FROM product GROUP ALL
).avg_price;

-- Find the name of the product where the price is higher than the avg price
SELECT name FROM product
WHERE [price] > $avg_price;

-- Use the parent instance's field in a subquery (predefined variable)
SELECT *, (SELECT * FROM events WHERE host == $parent.id) AS hosted_events FROM user;
```

Sometimes, especially with tables containing numerous columns, it is desirable to select all columns except a few specific ones. The OMIT clause can be used in this case

```
CREATE person:tobie SET
 name = 'Tobie',
 password = '123456',
 opts.security = 'secure',
 opts.enabled = true;
CREATE person:jaime SET
 name = 'Jaime',
 password = 'asdfgh',
 opts.security = 'secure',
 opts.enabled = false;

SELECT * FROM person;
-- Omit the password field and security field in the options object
SELECT * OMIT password, opts.security FROM person;

-- Using destructuring syntax
SELECT * OMIT password, opts.{ security, enabled } FROM person;
```

The FROM clause can be used on targets beyond just a single table or record name

```
-- Selects all records from both 'user' and 'admin' tables.
SELECT * FROM user, admin;

-- Selects all records from the table named in the variable '$table',
-- but only if the 'admin' field of those records is true.
-- Equivalent to 'SELECT * FROM user WHERE admin = true'.
LET $table = "user";
SELECT * FROM type::table($table) WHERE admin = true;

-- Selects a single record from:
-- * the table named in the variable '$table',
-- * and the identifier named in the variable '$id'.
-- This query is equivalent to 'SELECT * FROM user:admin'.
LET $table = "user";
LET $id = "admin";
SELECT * FROM type::record($table, $id);

-- Selects all records for specific users 'tobie' and 'jaime',
-- as well as all records for the company 'surrealdb'.
SELECT * FROM user:tobie, user:jaime, company:surrealdb;

-- Selects records from a list of identifiers. The identifiers can be numerical,
-- string, or specific records such as 'person:lrym5gur8hzws72ux5fa'.
SELECT * FROM [3648937, "test", person:lrym5gur8hzws72ux5fa, person:4luro9170uwcv1xrfvby];

-- Selects data from an object that includes a 'person' key,
-- which is associated with a specific person record, and an 'embedded' key set to true.
SELECT * FROM { person: person:lrym5gur8hzws72ux5fa, embedded: true };

-- This command first performs a subquery, which selects all 'user' records and adds a
-- computed 'adult' field that is true if the user's 'age' is 18 or older.
-- The main query then selects all records from this subquery where 'adult' is true.
SELECT * FROM (SELECT age >= 18 AS adult FROM user) WHERE adult = true;
```

As with traditional SQL queries, a SurrealDB SELECT query supports conditional filtering using a WHERE clause. If the expression in the WHERE clause is truthy (is present and not an empty value), then the respective record will be returned

```
-- Simple conditional filtering
SELECT * FROM article WHERE published = true;

-- Conditional filtering based on graph edges
SELECT * FROM profile WHERE count(->experience->organisation) > 3;

-- Conditional filtering based on graph edge properties
SELECT * FROM person WHERE ->(reaction WHERE type='celebrate')->post;

-- Conditional filtering with boolean logic
SELECT * FROM user WHERE (admin AND active) OR owner = true;

-- Select filtered nested array values
SELECT address[WHERE active = true] FROM person;

-- Select names for 'person' records as long as 'name' is present
-- and not an empty string ""
SELECT name FROM person WHERE name;
```

SurrealDB supports data aggregation and grouping, with support for multiple fields, nested fields, and aggregate functions. In SurrealDB, every field which appears in the field projections of the select statement (and which is not an aggregate function), must also be present in the GROUP BY clause

```
-- Group records by a single field
SELECT country FROM user GROUP BY country;

-- Group results by a nested field
SELECT settings.published FROM article GROUP BY settings.published;

-- Group results by multiple fields
SELECT gender, country, city FROM person GROUP BY gender, country, city;

-- Use an aggregate function to select unique values from a nested array across an entire table
SELECT array::group(tags) AS tags FROM article GROUP ALL;
```

A longer example of grouping using aggregate functions

```
INSERT INTO person [
    { gender: "M", age: 20, country: "Japan" },
    { gender: "M", age: 25, country: "Japan" },
    { gender: "F", age: 23, country: "US" },
    { gender: "F", age: 30, country: "US" },
    { gender: "F", age: 25, country: "Korea" },
    { gender: "F", age: 45, country: "UK" },
];

SELECT
 count() AS total,
 math::mean(age) AS average_age,
 gender,
 country
FROM person
GROUP BY gender, country;

-- Get the total number of records in a table
SELECT count() AS number_of_records FROM person GROUP ALL;
```

Output:

```
-------- Query --------

[
 {
  average_age: 25,
  country: 'Korea',
  gender: 'F',
  total: 1
 },
 {
  average_age: 45,
  country: 'UK',
  gender: 'F',
  total: 1
 },
 {
  average_age: 26,
  country: 'US',
  gender: 'F',
  total: 2
 },
 {
  average_age: 22,
  country: 'Japan',
  gender: 'M',
  total: 2
 }
]

-------- Query --------

[
 {
  number_of_records: 6
 }
]
```

To sort records, SurrealDB allows ordering on multiple fields and nested fields. Use the ORDER BY clause to specify a comma-separated list of field names that should be used to order the resulting records. The ASC and DESC keywords can be used to specify whether results should be sorted in an ascending or descending manner. The COLLATE keyword can be used to use Unicode collation when ordering text in string values, ensuring that different cases, and different languages are sorted in a consistent manner. Finally, the NUMERIC can be used to correctly sort text which contains numeric values.

```
-- Order records randomly
SELECT * FROM user ORDER BY rand();

-- Order records descending by a single field
SELECT * FROM song ORDER BY rating DESC;

-- Order records by multiple fields independently
SELECT * FROM song ORDER BY artist ASC, rating DESC;

-- Order text fields with Unicode collation
SELECT * FROM article ORDER BY title COLLATE ASC;

-- Order text fields with which include numeric values
SELECT * FROM article ORDER BY title NUMERIC ASC;
```

To limit the number of records returned, use the LIMIT clause

```
-- Select only the top 50 records from the person table
SELECT * FROM person LIMIT 50;
```

When using the LIMIT clause, it is possible to paginate results by using the START clause to start from a specific record from the result set. It is important to note that the START count starts from 0.

```
-- Start at record 50 and select the following 50 records
SELECT * FROM user LIMIT 50 START 50;
```

The LIMIT clause followed by 1 is often used along with the ONLY clause to satisfy the requirement that only up to a single record can be returned

```
-- Record IDs are unique so guaranteed to be no more than 1
SELECT * FROM ONLY person:jamie;

-- Error because no guarantee that this will return a single record
SELECT * FROM ONLY person WHERE name = "Jaime";

-- Add `LIMIT 1` to ensure that only up to one record will be returned
SELECT * FROM ONLY person WHERE name = "Jaime" LIMIT 1;
```

```
-- Select the first 5 records from the array
SELECT * FROM [1,2,3,4,5,6,7,8,9,10] LIMIT 5 START 4;
-- returns [5, 6, 7, 8, 9]
```

Two of the most powerful features in SurrealDB are record links and graph connections.

Instead of pulling data from multiple tables and merging that data together, SurrealDB allows you to traverse related records efficiently without needing to use JOINs.

To fetch and replace records with the remote record data, use the FETCH clause to specify the fields and nested fields which should be fetched in-place, and returned in the final statement response output

```
-- Select all the review information
-- and the artist's email from the artist table
SELECT *, artist.email FROM review FETCH artist;

-- Select all the article information
-- only if the author's age (from the author table) is under 30.
SELECT * FROM article WHERE author.age < 30 FETCH author;
```

If you are selecting just one single resource, it’s possible to use the ONLY clause to filter that result from an array

```
SELECT * FROM ONLY person:john;
```

If you are selecting from a resource where it is possible that multiple resources are returned, it is required to LIMIT the result to just one. This is needed, because the query would otherwise not be deterministic

```
-- Fails
SELECT * FROM ONLY table_name;
-- Succeeds
SELECT * FROM ONLY table_name LIMIT 1;
```

A SELECT statement and/or its clauses can be used inside graph queries as well at the graph edge portion of the query

```
-- Note: 1..4 used to be inclusive until SurrealDB 3.0.0
-- Now creates 1 up to but not including 4
CREATE |person:1..4|;

RELATE person:1->likes->person:2 SET like_strength = 20, know_in_person = true;
RELATE person:1->likes->person:3 SET like_strength = 5,  know_in_person = false;
RELATE person:2->likes->person:1 SET like_strength = 10, know_in_person = true;
RELATE person:2->likes->person:3 SET like_strength = 12, know_in_person = false;
RELATE person:3->likes->person:1 SET like_strength = 2,  know_in_person = false;
RELATE person:3->likes->person:2 SET like_strength = 9,  know_in_person = false;

SELECT ->likes AS likes FROM person;
SELECT ->(SELECT like_strength FROM likes) AS likes FROM person;
SELECT ->(SELECT like_strength FROM likes WHERE like_strength > 10) AS likes FROM person;
SELECT ->(likes WHERE like_strength > 10) AS likes FROM person;
SELECT ->(SELECT like_strength, know_in_person FROM likes ORDER BY like_strength DESC) AS likes FROM person;
SELECT ->(SELECT count() as count, know_in_person FROM likes GROUP BY know_in_person) AS likes FROM person;
SELECT ->(likes LIMIT 1) AS likes FROM person;
SELECT ->(likes START 1) AS likes FROM person;
```

[More about SELECT](select.md)

There's even more:

- CREATE
- DELETE
- INSERT
- RETURN
- LET
- FOR
- IF ELSE
- RELATE
- THROW
- UPDATE
- UPSERT
- USE

<https://surrealdb.com/docs/surrealql/statements>
