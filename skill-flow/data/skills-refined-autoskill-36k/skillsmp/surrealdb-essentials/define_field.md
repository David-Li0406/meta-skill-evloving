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

-- Define nested object property types
DEFINE FIELD emails.address ON TABLE user TYPE string;
DEFINE FIELD emails.primary ON TABLE user TYPE bool;

-- Define individual fields on an array
DEFINE FIELD metadata[0] ON person TYPE datetime;
DEFINE FIELD metadata[1] ON person TYPE int;
```

The DEFINE FIELD statement allows you to set the data type of a field. For a full list of supported data types, see Data types. When defining nested fields, where both the parent and the nested fields have types defined, it is no longer possible to have mismatching types, to prevent any impossible type issues once the schema is defined.

```
-- Set a field to have the string data type
DEFINE FIELD email ON TABLE user TYPE string;

-- Set a field to have the array data type
DEFINE FIELD roles ON TABLE user TYPE array<string>;

-- Set a field to have the array data type, equivalent to `array<any>`
DEFINE FIELD posts ON TABLE user TYPE array;

-- Set a field to have the array object data type
DEFINE FIELD emails ON TABLE user TYPE array<object>;

-- Field for a block in a game showing the possible directions a character can move next.
-- The array can contain no more than four directions
DEFINE FIELD next_paths ON TABLE block TYPE array<"north" | "east" | "south" | "west", 4>;

-- A user may enter a biography, but it is not required.
-- By using the option type you also allow for NONE values.
DEFINE FIELD biography ON TABLE user TYPE option<string>;
DEFINE FIELD user ON TABLE post TYPE option<record<user>>;
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

With the above definition, the primary field will be set to 123.456 when a new product is created without a value for the primary field or with a value of NONE, and when an existing product is updated if the value is specified the result will be the new value.

In the case of NULL or a mismatching type, an error will be returned.

On the other hand, if a valid number is provided during creation or update, that number will be used instead of the default value. In this case, 123.456.

The VALUE clause differs from DEFAULT in that a default value is calculated if no other is indicated, otherwise accepting the value given in a query.

```
DEFINE FIELD updated ON TABLE user DEFAULT time::now();

-- Set `updated` to the year 1900
CREATE user SET updated = d"1900-01-01";
-- Then set to the year 1910
UPDATE user SET updated = d"1910-01-01";
```

A VALUE clause, on the other hand, will ignore attempts to set the field to any other value.

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

To create a field that is calculated each time it is accessed, a computed field can be used.

```
DEFINE FIELD accessed_at ON TABLE user COMPUTED time::now();

CREATE user:one;
SELECT * FROM ONLY user:one;
-- Sleep for one second
SLEEP 1s;
-- `accessed_at` is a different value now
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

You can use the ASSERT clause to apply a regular expression to a field to ensure that it matches a specific pattern. In the example below, the ASSERT clause is used to ensure that the countrycode field is always a valid ISO-3166 country code.

```
-- Specify a field on the user table
DEFINE FIELD countrycode ON user TYPE string
	-- Ensure country code is ISO-3166
	ASSERT $value = /[A-Z]{3}/
	-- Set a default value if empty
	VALUE $value OR $before OR 'GBR'
;
```

While a DEFINE TABLE statement represents a template for any subsequent records to be created, a DEFINE FIELD statement pertains to concrete field data of a record. As such, a DEFINE FIELD statement gives access to the record’s other fields through their names, as well as the current field through the $value parameter.

```
DEFINE TABLE person SCHEMAFULL;

DEFINE FIELD first_name ON TABLE person TYPE string VALUE string::lowercase($value);
DEFINE FIELD last_name  ON TABLE person TYPE string VALUE string::lowercase($value);
DEFINE FIELD name       ON TABLE person             VALUE first_name + ' ' + last_name;

// Creates a `person` with the name "bob bobson"
CREATE person SET first_name = "BOB", last_name = "BOBSON";
```

The $this parameter gives access to the entire record on which a field is defined.

```
DEFINE FIELD extra_self ON TABLE person VALUE $this;
CREATE person:one SET name = "Little person", age = 6;
```

Output:
```
[
	{
		age: 6,
		extra_self: {
			age: 6,
			id: person:one,
			name: 'Little person'
		},
		id: person:one,
		name: 'Little person'
	}
]
```

As DEFINE FIELD statements are computed in alphabetical order, be sure to keep this in mind when using fields that rely on the values of others.

The following example is identical to the above except that full_name has been chosen for the previous field name. The full_name field will be calculated after first_name, but before last_name.

```
DEFINE TABLE person SCHEMAFULL;

DEFINE FIELD first_name ON TABLE person TYPE string VALUE string::lowercase($value);
DEFINE FIELD last_name  ON TABLE person TYPE string VALUE string::lowercase($value);
DEFINE FIELD full_name  ON TABLE person             VALUE first_name + ' ' + last_name;

// Creates a `person` with `full_name` of "bob BOBSON", not "bob bobson"
CREATE person SET first_name = "Bob", last_name = "BOBSON";
```

A field can also be defined as a literal type, by specifying one or more possible values and/or permitted types.

```
DEFINE FIELD coffee ON TABLE order TYPE "regular" | "large" | { special_order: string };

CREATE order:good SET coffee = { special_order: "Venti Quadruple Ristretto Half-Decaf Soy Latte with 4 pumps of sugar-free vanilla syrup" };
CREATE order:bad SET coffee = "small";
```
Response:
```
-------- Query --------

[
	{
		coffee: {
			special_order: 'Venti Quadruple Ristretto Half-Decaf Soy Latte with 4 pumps of sugar-free vanilla syrup'
		},
		id: order:good
	}
]

-------- Query --------
"Found 'small' for field `coffee`, with record `order:bad`, but expected a 'regular' | 'large' | { special_order: string }"
```

A field that is a record link (type record, option<record>, array<record<person>>, and so on) can be defined as a REFERENCE. If this clause is used, any linked to record will be able to define a field of its own of type references which will be aware of the incoming links.


