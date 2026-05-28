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

While a DEFINE TABLE statement represents a template for any subsequent records to be created, a DEFINE FIELD statement pertains to concrete field data of a record. As such, a DEFINE FIELD statement gives access to the record’s other fields through their names, as well as the current field through the $value parameter.

```
DEFINE TABLE person SCHEMAFULL;

DEFINE FIELD first_name ON TABLE person TYPE string ASSERT string::len($value) < 20;
DEFINE FIELD last_name  ON TABLE person TYPE string ASSERT string::len($value) < 20;
DEFINE FIELD name       ON TABLE person             VALUE first_name + ' ' + last_name;

// Creates a `person` with the name "Bob Bobson"
CREATE person SET first_name = "Bob", last_name = "Bobson";
```

In SurrealDB, like in other databases, you can create views. The way you create views is using the DEFINE TABLE statement like you would for any other table, then adding the AS clause at the end with your SELECT query.

```
DEFINE TABLE review DROP;
-- Define a table as a view which aggregates data from the review table
DEFINE TABLE avg_product_review TYPE NORMAL AS
SELECT
 count() AS number_of_reviews,
 math::mean(<float> rating) AS avg_review,
 ->product.id AS product_id,
 ->product.name AS product_name
FROM review
GROUP BY product_id, product_name;

-- Query the projection
SELECT * FROM avg_product_review;
```

When defining a table in SurrealDB, you can specify the type of data that can be stored in the table. This can be done using the TYPE clause, followed by either ANY, NORMAL, or RELATION.

With TYPE ANY, you can specify a table to store any type of data, whether it’s a normal record or a relational record.

With TYPE NORMAL, you can specify a table to only store “normal” records, and not relations. When a table is defined as TYPE NORMAL, it will not be able to store relations this can be useful when you want to restrict the type of data that can be stored in a table in schemafull mode.

Finally, with TYPE RELATION, you can specify a table to only store relational type content. This can be useful when you want to restrict the type of data that can be stored in a table.

Using ENFORCED to ensure that related records exist
