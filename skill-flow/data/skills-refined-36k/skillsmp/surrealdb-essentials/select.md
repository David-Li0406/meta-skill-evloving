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

As SurrealDB supports arrays and nested fields within arrays, it is possible to use the SPLIT clause to split the result on a specific field name, returning each value in an array as a separate value, along with the record content itself. This is useful in data analysis contexts

```
CREATE user SET
    name = "Name",
    emails = ["me@me.com", "longer_email@other_service.com"];

-- Split the results by each value in an array
SELECT * FROM user SPLIT emails;
```

Output:
```
[
	{
		emails: 'me@me.com',
		id: user:tr5sxe8iygdco05faoh0,
		name: 'Name'
	},
	{
		emails: 'longer_email@other_service.com',
		id: user:tr5sxe8iygdco05faoh0,
		name: 'Name'
	}
]
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
