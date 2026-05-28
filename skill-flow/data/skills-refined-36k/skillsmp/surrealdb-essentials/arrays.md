# Everything about arrays

An array is a collection of values contained inside `[]`, each of which is stored at a certain index. Individual indexes and slices of indexes can be accesses using the same square bracket syntax.

```
-- Return a full array
RETURN [1,2,3,4,5]; -- [1,2,3,4,5]
-- Return the first ("zeroeth") item
RETURN [1,2,3,4,5][0]; -- 1
-- Return indexes 0 up to and including 2 of an array
RETURN [1,2,3,4,5][0..=2]; -- [1,2,3]
-- Even this returns an array
SELECT * FROM 9; -- [ 9 ]
-- Use the `ONLY` clause to return a single item
SELECT * FROM ONLY 9; -- 9
-- Error: array has more than one item
SELECT * FROM ONLY [1,9]; -- error: Expected a single result output when using the ONLY keyword
CREATE person SET results = [
	{ score: 76, date: "2017-06-18T08:00:00Z", name: "Algorithmics" },
	{ score: 83, date: "2018-03-21T08:00:00Z", name: "Concurrent Programming" },
	{ score: 69, date: "2018-09-17T08:00:00Z", name: "Advanced Computer Science 101" },
	{ score: 73, date: "2019-04-20T08:00:00Z", name: "Distributed Databases" },
];
-- A max num of items can be specified for an array:
DEFINE FIELD employees ON TABLE team TYPE array<record<employee>, 5>;
```

The `[]` operator after an array can also be used to filter the items inside an array. The parameter `$this` is used to refer to each individual item, while `WHERE` (or its alias `?`, a question mark) is used to set the condition for the item to pass the filter.

```
[true, false, true][WHERE $this = true]; -- [true, true]
[1,2,NONE][? $this]; -- [1,2]

-- can be repeated
[
    {
        name: "Boston",
        population: NONE,
        first_mayor: "John Phillips"
    },
    {
        name: "Smurfville",
        population: 55,
        first_mayor: "Papa Smurf"
    },
    {
        name: "Harrisburg",
        population: 50183,
        first_mayor: NONE
    }
][WHERE $this.population]
 [WHERE $this.first_mayor];
-- output: [ { first_mayor: 'Papa Smurf', name: 'Smurfville', population: 55 } ]

[1,3,5].filter(|$val| $val > 2); -- [3,5]
[1,3,5][WHERE $this > 2]; -- [3,5]
[1,2,3].map(|$item| $item + 1); -- [2,3,4]
[1,2,3].map(|$v, $i| "At index " + <string>$i + " we got a " + <string>$v + "!"); -- [ 'At index 0 we got a 1!', 'At index 1 we got a 2!', 'At index 2 we got a 3!' ]

[1,2] + [3,4]; -- [1,2,3,4]
[1,2].concat([3,4]); -- [1,2,3,4]
```
