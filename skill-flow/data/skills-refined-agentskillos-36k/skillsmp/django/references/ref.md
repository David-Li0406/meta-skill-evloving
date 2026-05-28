# Django - Ref

**Pages:** 20

---

## Built-in Views¶

**URL:** https://docs.djangoproject.com/en/stable/ref/views/

**Contents:**
- Built-in Views¶
- Serving files in development¶
- Error views¶
  - The 404 (page not found) view¶
  - The 500 (server error) view¶
  - The 403 (HTTP Forbidden) view¶
  - The 400 (bad request) view¶

Several of Django’s built-in views are documented in Writing views as well as elsewhere in the documentation.

There may be files other than your project’s static assets that, for convenience, you’d like to have Django serve for you in local development. The serve() view can be used to serve any directory you give it. (This view is not hardened for production use and should be used only as a development aid; you should serve these files in production using a real front-end web server).

The most likely example is user-uploaded content in MEDIA_ROOT. django.contrib.staticfiles is intended for static assets and has no built-in handling for user-uploaded files, but you can have Django serve your MEDIA_ROOT by appending something like this to your URLconf:

Note, the snippet assumes your MEDIA_URL has a value of 'media/'. This will call the serve() view, passing in the path from the URLconf and the (required) document_root parameter.

Since it can become a bit cumbersome to define this URL pattern, Django ships with a small URL helper function static() that takes as parameters the prefix such as MEDIA_URL and a dotted path to a view, such as 'django.views.static.serve'. Any other function parameter will be transparently passed to the view.

Django comes with a few views by default for handling HTTP errors. To override these with your own custom views, see Customizing error views.

When you raise Http404 from within a view, Django loads a special view devoted to handling 404 errors. By default, it’s the view django.views.defaults.page_not_found(), which either produces a “Not Found” message or loads and renders the template 404.html if you created it in your root template directory.

The default 404 view will pass two variables to the template: request_path, which is the URL that resulted in the error, and exception, which is a useful representation of the exception that triggered the view (e.g. containing any message passed to a specific Http404 instance).

Three things to note about 404 views:

The 404 view is also called if Django doesn’t find a match after checking every regular expression in the URLconf.

The 404 view is passed a RequestContext and will have access to variables supplied by your template context processors (e.g. MEDIA_URL).

If DEBUG is set to True (in your settings module), then your 404 view will never be used, and your URLconf will be displayed instead, with some debug information.

Similarly, Django executes special-case behavior in the case of runtime errors in view code. If a view results in an exception, Django will, by default, call the view django.views.defaults.server_error, which either produces a “Server Error” message or loads and renders the template 500.html if you created it in your root template directory.

The default 500 view passes no variables to the 500.html template and is rendered with an empty Context to lessen the chance of additional errors.

If DEBUG is set to True (in your settings module), then your 500 view will never be used, and the traceback will be displayed instead, with some debug information.

In the same vein as the 404 and 500 views, Django has a view to handle 403 Forbidden errors. If a view results in a 403 exception then Django will, by default, call the view django.views.defaults.permission_denied.

This view loads and renders the template 403.html in your root template directory, or if this file does not exist, instead serves the text “403 Forbidden”, as per RFC 9110 Section 15.5.4 (the HTTP 1.1 Specification). The template context contains exception, which is the string representation of the exception that triggered the view.

django.views.defaults.permission_denied is triggered by a PermissionDenied exception. To deny access in a view you can use code like this:

When a SuspiciousOperation is raised in Django, it may be handled by a component of Django (for example resetting the session data). If not specifically handled, Django will consider the current request a ‘bad request’ instead of a server error.

django.views.defaults.bad_request, is otherwise very similar to the server_error view, but returns with the status code 400 indicating that the error condition was the result of a client operation. By default, nothing related to the exception that triggered the view is passed to the template context, as the exception message might contain sensitive information like filesystem paths.

bad_request views are also only used when DEBUG is False.

---

## Conditional Expressions¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/conditional-expressions/

**Contents:**
- Conditional Expressions¶
- The conditional expression classes¶
  - When¶
  - Case¶
- Advanced queries¶
  - Conditional update¶
  - Conditional aggregation¶
  - Conditional filter¶

Conditional expressions let you use if … elif … else logic within filters, annotations, aggregations, and updates. A conditional expression evaluates a series of conditions for each row of a table and returns the matching result expression. Conditional expressions can also be combined and nested like other expressions.

We’ll be using the following model in the subsequent examples:

A When() object is used to encapsulate a condition and its result for use in the conditional expression. Using a When() object is similar to using the filter() method. The condition can be specified using field lookups, Q objects, or Expression objects that have an output_field that is a BooleanField. The result is provided using the then keyword.

Keep in mind that each of these values can be an expression.

Since the then keyword argument is reserved for the result of the When(), there is a potential conflict if a Model has a field named then. This can be resolved in two ways:

A Case() expression is like the if … elif … else statement in Python. Each condition in the provided When() objects is evaluated in order, until one evaluates to a truthful value. The result expression from the matching When() object is returned.

Case() accepts any number of When() objects as individual arguments. Other options are provided using keyword arguments. If none of the conditions evaluate to TRUE, then the expression given with the default keyword argument is returned. If a default argument isn’t provided, None is used.

If we wanted to change our previous query to get the discount based on how long the Client has been with us, we could do so using lookups:

Remember that the conditions are evaluated in order, so in the above example we get the correct result even though the second condition matches both Jane Doe and Jack Black. This works just like an if … elif … else statement in Python.

Case() also works in a filter() clause. For example, to find gold clients that registered more than a month ago and platinum clients that registered more than a year ago:

Conditional expressions can be used in annotations, aggregations, filters, lookups, and updates. They can also be combined and nested with other expressions. This allows you to make powerful conditional queries.

Let’s say we want to change the account_type for our clients to match their registration dates. We can do this using a conditional expression and the update() method:

What if we want to find out how many clients there are for each account_type? We can use the filter argument of aggregate functions to achieve this:

This aggregate produces a query with the SQL 2003 FILTER WHERE syntax on databases that support it:

On other databases, this is emulated using a CASE statement:

The two SQL statements are functionally equivalent but the more explicit FILTER may perform better.

When a conditional expression returns a boolean value, it is possible to use it directly in filters. This means that it will not be added to the SELECT columns, but you can still use it to filter results:

In SQL terms, that evaluates to:

---

## Databases¶

**URL:** https://docs.djangoproject.com/en/stable/ref/databases/

**Contents:**
- Databases¶
- General notes¶
  - Persistent connections¶
    - Connection management¶
    - Caveats¶
  - Encoding¶
- PostgreSQL notes¶
  - PostgreSQL connection settings¶
  - Optimizing PostgreSQL’s configuration¶
  - Isolation level¶

Django officially supports the following databases:

There are also a number of database backends provided by third parties.

Django attempts to support as many features as possible on all database backends. However, not all database backends are alike, and we’ve had to make design decisions on which features to support and which assumptions we can make safely.

This file describes some of the features that might be relevant to Django usage. It is not intended as a replacement for server-specific documentation or reference manuals.

Persistent connections avoid the overhead of reestablishing a connection to the database in each HTTP request. They’re controlled by the CONN_MAX_AGE parameter which defines the maximum lifetime of a connection. It can be set independently for each database.

The default value is 0, preserving the historical behavior of closing the database connection at the end of each request. To enable persistent connections, set CONN_MAX_AGE to a positive integer of seconds. For unlimited persistent connections, set it to None.

When using ASGI, persistent connections should be disabled. Instead, use your database backend’s built-in connection pooling if available, or investigate a third-party connection pooling option if required.

Django opens a connection to the database when it first makes a database query. It keeps this connection open and reuses it in subsequent requests. Django closes the connection once it exceeds the maximum age defined by CONN_MAX_AGE or when it isn’t usable any longer.

In detail, Django automatically opens a connection to the database whenever it needs one and doesn’t have one already — either because this is the first connection, or because the previous connection was closed.

At the beginning of each request, Django closes the connection if it has reached its maximum age. If your database terminates idle connections after some time, you should set CONN_MAX_AGE to a lower value, so that Django doesn’t attempt to use a connection that has been terminated by the database server. (This problem may only affect very low traffic sites.)

At the end of each request, Django closes the connection if it has reached its maximum age or if it is in an unrecoverable error state. If any database errors have occurred while processing the requests, Django checks whether the connection still works, and closes it if it doesn’t. Thus, database errors affect at most one request per each application’s worker thread; if the connection becomes unusable, the next request gets a fresh connection.

Setting CONN_HEALTH_CHECKS to True can be used to improve the robustness of connection reuse and prevent errors when a connection has been closed by the database server which is now ready to accept and serve new connections, e.g. after database server restart. The health check is performed only once per request and only if the database is being accessed during the handling of the request.

Since each thread maintains its own connection, your database must support at least as many simultaneous connections as you have worker threads.

Sometimes a database won’t be accessed by the majority of your views, for example because it’s the database of an external system, or thanks to caching. In such cases, you should set CONN_MAX_AGE to a low value or even 0, because it doesn’t make sense to maintain a connection that’s unlikely to be reused. This will help keep the number of simultaneous connections to this database small.

The development server creates a new thread for each request it handles, negating the effect of persistent connections. Don’t enable them during development.

When Django establishes a connection to the database, it sets up appropriate parameters, depending on the backend being used. If you enable persistent connections, this setup is no longer repeated every request. If you modify parameters such as the connection’s isolation level or time zone, you should either restore Django’s defaults at the end of each request, force an appropriate value at the beginning of each request, or disable persistent connections.

If a connection is created in a long-running process, outside of Django’s request-response cycle, the connection will remain open until explicitly closed, or timeout occurs. You can use django.db.close_old_connections() to close all old or unusable connections.

Django assumes that all databases use UTF-8 encoding. Using other encodings may result in unexpected behavior such as “value too long” errors from your database for data that is valid in Django. See the database specific notes below for information on how to set up your database correctly.

Django supports PostgreSQL 14 and higher. psycopg 3.1.12+ or psycopg2 2.9.9+ is required, though the latest psycopg 3.1.12+ is recommended.

Support for psycopg2 is likely to be deprecated and removed at some point in the future.

See HOST for details.

To connect using a service name from the connection service file and a password from the password file, you must specify them in the OPTIONS part of your database configuration in DATABASES:

The PostgreSQL backend passes the content of OPTIONS as keyword arguments to the connection constructor, allowing for more advanced control of driver behavior. All available parameters are described in detail in the PostgreSQL documentation.

Using a service name for testing purposes is not supported. This may be implemented later.

Django needs the following parameters for its database connections:

client_encoding: 'UTF8',

default_transaction_isolation: 'read committed' by default, or the value set in the connection options (see below),

when USE_TZ is True, 'UTC' by default, or the TIME_ZONE value set for the connection,

when USE_TZ is False, the value of the global TIME_ZONE setting.

If these parameters already have the correct values, Django won’t set them for every new connection, which improves performance slightly. You can configure them directly in postgresql.conf or more conveniently per database user with ALTER ROLE.

Django will work just fine without this optimization, but each new connection will do some additional queries to set these parameters.

Like PostgreSQL itself, Django defaults to the READ COMMITTED isolation level. If you need a higher isolation level such as REPEATABLE READ or SERIALIZABLE, set it in the OPTIONS part of your database configuration in DATABASES:

Under higher isolation levels, your application should be prepared to handle exceptions raised on serialization failures. This option is designed for advanced uses.

If you need to use a different role for database connections than the role used to establish the connection, set it in the OPTIONS part of your database configuration in DATABASES:

To use a connection pool with psycopg, you can either set "pool" in the OPTIONS part of your database configuration in DATABASES to be a dict to be passed to ConnectionPool, or to True to use the ConnectionPool defaults:

This option requires psycopg[pool] or psycopg-pool to be installed and is ignored with psycopg2.

With psycopg 3.1.8+, Django defaults to the client-side binding cursors. If you want to use the server-side binding set it in the OPTIONS part of your database configuration in DATABASES:

This option is ignored with psycopg2.

When specifying db_index=True on your model fields, Django typically outputs a single CREATE INDEX statement. However, if the database type for the field is either varchar or text (e.g., used by CharField, FileField, and TextField), then Django will create an additional index that uses an appropriate PostgreSQL operator class for the column. The extra index is necessary to correctly perform lookups that use the LIKE operator in their SQL, as is done with the contains and startswith lookup types.

If you need to add a PostgreSQL extension (like hstore, postgis, etc.) using a migration, use the CreateExtension operation.

When using QuerySet.iterator(), Django opens a server-side cursor. By default, PostgreSQL assumes that only the first 10% of the results of cursor queries will be fetched. The query planner spends less time planning the query and starts returning results faster, but this could diminish performance if more than 10% of the results are retrieved. PostgreSQL’s assumptions on the number of rows retrieved for a cursor query is controlled with the cursor_tuple_fraction option.

Using a connection pooler in transaction pooling mode (e.g. PgBouncer) requires disabling server-side cursors for that connection.

Server-side cursors are local to a connection and remain open at the end of a transaction when AUTOCOMMIT is True. A subsequent transaction may attempt to fetch more results from a server-side cursor. In transaction pooling mode, there’s no guarantee that subsequent transactions will use the same connection. If a different connection is used, an error is raised when the transaction references the server-side cursor, because server-side cursors are only accessible in the connection in which they were created.

One solution is to disable server-side cursors for a connection in DATABASES by setting DISABLE_SERVER_SIDE_CURSORS to True.

To benefit from server-side cursors in transaction pooling mode, you could set up another connection to the database in order to perform queries that use server-side cursors. This connection needs to either be directly to the database or to a connection pooler in session pooling mode.

Another option is to wrap each QuerySet using server-side cursors in an atomic() block, because it disables autocommit for the duration of the transaction. This way, the server-side cursor will only live for the duration of the transaction.

Django uses PostgreSQL’s identity columns to store auto-incrementing primary keys. An identity column is populated with values from a sequence that keeps track of the next available value. Manually assigning a value to an auto-incrementing field doesn’t update the field’s sequence, which might later cause a conflict. For example:

If you need to specify such values, reset the sequence afterward to avoid reusing a value that’s already in the table. The sqlsequencereset management command generates the SQL statements to do that.

You can use the TEST['TEMPLATE'] setting to specify a template (e.g. 'template0') from which to create a test database.

You can speed up test execution times by configuring PostgreSQL to be non-durable.

This is dangerous: it will make your database more susceptible to data loss or corruption in the case of a server crash or power loss. Only use this on a development machine where you can easily restore the entire contents of all databases in the cluster.

Django supports MariaDB 10.6 and higher.

To use MariaDB, use the MySQL backend, which is shared between the two. See the MySQL notes for more details.

Django supports MySQL 8.0.11 and higher.

Django’s inspectdb feature uses the information_schema database, which contains detailed data on all database schemas.

Django expects the database to support Unicode (UTF-8 encoding) and delegates to it the task of enforcing transactions and referential integrity. It is important to be aware of the fact that the two latter ones aren’t actually enforced by MySQL when using the MyISAM storage engine, see the next section.

MySQL has several storage engines. You can change the default storage engine in the server configuration.

MySQL’s default storage engine is InnoDB. This engine is fully transactional and supports foreign key references. It’s the recommended choice. However, the InnoDB autoincrement counter is lost on a MySQL restart because it does not remember the AUTO_INCREMENT value, instead recreating it as “max(id)+1”. This may result in an inadvertent reuse of AutoField values.

The main drawbacks of MyISAM are that it doesn’t support transactions or enforce foreign-key constraints.

MySQL has a couple drivers that implement the Python Database API described in PEP 249:

mysqlclient is a native driver. It’s the recommended choice.

MySQL Connector/Python is a pure Python driver from Oracle that does not require the MySQL client library or any Python modules outside the standard library.

In addition to a DB API driver, Django needs an adapter to access the database drivers from its ORM. Django provides an adapter for mysqlclient while MySQL Connector/Python includes its own.

Django requires mysqlclient 2.2.1 or later.

MySQL Connector/Python is available from the download page. The Django adapter is available in versions 1.1.X and later. It may not support the most recent releases of Django.

If you plan on using Django’s timezone support, use mysql_tzinfo_to_sql to load time zone tables into the MySQL database. This needs to be done just once for your MySQL server, not per database.

You can create your database using the command-line tools and this SQL:

This ensures all tables and columns will use UTF-8 by default.

The collation setting for a column controls the order in which data is sorted as well as what strings compare as equal. You can specify the db_collation parameter to set the collation name of the column for CharField and TextField.

The collation can also be set on a database-wide level and per-table. This is documented thoroughly in the MySQL documentation. In such cases, you must set the collation by directly manipulating the database settings or tables. Django doesn’t provide an API to change them.

By default, with a UTF-8 database, MySQL will use the utf8mb4_0900_ai_ci collation. This results in all string equality comparisons being done in a case-insensitive manner. That is, "Fred" and "freD" are considered equal at the database level. If you have a unique constraint on a field, it would be illegal to try to insert both "aa" and "AA" into the same column, since they compare as equal (and, hence, non-unique) with the default collation. If you want case-sensitive comparisons on a particular column or table, change the column or table to use the utf8mb4_0900_as_cs collation.

Please note that according to MySQL Unicode Character Sets, comparisons for the utf8mb4_general_ci collation are faster, but slightly less correct, than comparisons for utf8mb4_unicode_ci. If this is acceptable for your application, you should use utf8mb4_general_ci because it is faster. If this is not acceptable (for example, if you require German dictionary order), use utf8mb4_unicode_ci because it is more accurate.

Model formsets validate unique fields in a case-sensitive manner. Thus when using a case-insensitive collation, a formset with unique field values that differ only by case will pass validation, but upon calling save(), an IntegrityError will be raised.

Refer to the settings documentation.

Connection settings are used in this order:

NAME, USER, PASSWORD, HOST, PORT

In other words, if you set the name of the database in OPTIONS, this will take precedence over NAME, which would override anything in a MySQL option file.

Here’s a sample configuration which uses a MySQL option file:

Several other MySQLdb connection options may be useful, such as ssl, init_command, and sql_mode.

The default value of the sql_mode option contains STRICT_TRANS_TABLES. That option escalates warnings into errors when data are truncated upon insertion, so Django highly recommends activating a strict mode for MySQL to prevent data loss (either STRICT_TRANS_TABLES or STRICT_ALL_TABLES).

If you need to customize the SQL mode, you can set the sql_mode variable like other MySQL options: either in a config file or with the entry 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'" in the OPTIONS part of your database configuration in DATABASES.

When running concurrent loads, database transactions from different sessions (say, separate threads handling different requests) may interact with each other. These interactions are affected by each session’s transaction isolation level. You can set a connection’s isolation level with an 'isolation_level' entry in the OPTIONS part of your database configuration in DATABASES. Valid values for this entry are the four standard isolation levels:

or None to use the server’s configured isolation level. However, Django works best with and defaults to read committed rather than MySQL’s default, repeatable read. Data loss is possible with repeatable read. In particular, you may see cases where get_or_create() will raise an IntegrityError but the object won’t appear in a subsequent get() call.

When Django generates the schema, it doesn’t specify a storage engine, so tables will be created with whatever default storage engine your database server is configured for. The easiest solution is to set your database server’s default storage engine to the desired engine.

If you’re using a hosting service and can’t change your server’s default storage engine, you have a couple of options.

After the tables are created, execute an ALTER TABLE statement to convert a table to a new storage engine (such as InnoDB):

This can be tedious if you have a lot of tables.

Another option is to use the init_command option for MySQLdb prior to creating your tables:

This sets the default storage engine upon connecting to the database. After your tables have been created, you should remove this option as it adds a query that is only needed during table creation to each database connection.

There are known issues in even the latest versions of MySQL that can cause the case of a table name to be altered when certain SQL statements are executed under certain conditions. It is recommended that you use lowercase table names, if possible, to avoid any problems that might arise from this behavior. Django uses lowercase table names when it auto-generates table names from models, so this is mainly a consideration if you are overriding the table name via the db_table parameter.

Both the Django ORM and MySQL (when using the InnoDB storage engine) support database savepoints.

If you use the MyISAM storage engine please be aware of the fact that you will receive database-generated errors if you try to use the savepoint-related methods of the transactions API. The reason for this is that detecting the storage engine of a MySQL database/table is an expensive operation so it was decided it isn’t worth to dynamically convert these methods in no-op’s based in the results of such detection.

Any fields that are stored with VARCHAR column types may have their max_length restricted to 255 characters if you are using unique=True for the field. This affects CharField, SlugField. See the MySQL documentation for more details.

MySQL can index only the first N chars of a BLOB or TEXT column. Since TextField doesn’t have a defined length, you can’t mark it as unique=True. MySQL will report: “BLOB/TEXT column ‘<db_column>’ used in key specification without a key length”.

MySQL can store fractional seconds, provided that the column definition includes a fractional indication (e.g. DATETIME(6)).

Django will not upgrade existing columns to include fractional seconds if the database server supports it. If you want to enable them on an existing database, it’s up to you to either manually update the column on the target database, by executing a command like:

or using a RunSQL operation in a data migration.

If you are using a legacy database that contains TIMESTAMP columns, you must set USE_TZ = False to avoid data corruption. inspectdb maps these columns to DateTimeField and if you enable timezone support, both MySQL and Django will attempt to convert the values from UTC to local time.

MySQL and MariaDB do not support some options to the SELECT ... FOR UPDATE statement. If select_for_update() is used with an unsupported option, then a NotSupportedError is raised.

When using select_for_update() on MySQL, make sure you filter a queryset against at least a set of fields contained in unique constraints or only against fields covered by indexes. Otherwise, an exclusive write lock will be acquired over the full table for the duration of the transaction.

When performing a query on a string type, but with an integer value, MySQL will coerce the types of all values in the table to an integer before performing the comparison. If your table contains the values 'abc', 'def' and you query for WHERE mycolumn=0, both rows will match. Similarly, WHERE mycolumn=1 will match the value 'abc1'. Therefore, string type fields included in Django will always cast the value to a string before using it in a query.

If you implement custom model fields that inherit from Field directly, are overriding get_prep_value(), or use RawSQL, extra(), or raw(), you should ensure that you perform appropriate typecasting.

Django supports SQLite 3.31.0 and later.

SQLite provides an excellent development alternative for applications that are predominantly read-only or require a smaller installation footprint. As with all database servers, though, there are some differences that are specific to SQLite that you should be aware of.

For all SQLite versions, there is some slightly counterintuitive behavior when attempting to match some types of strings. These are triggered when using the iexact or contains filters in querysets. The behavior splits into two cases:

1. For substring matching, all matches are done case-insensitively. That is a filter such as filter(name__contains="aa") will match a name of "Aabb".

2. For strings containing characters outside the ASCII range, all exact string matches are performed case-sensitively, even when the case-insensitive options are passed into the query. So the iexact filter will behave exactly the same as the exact filter in these cases.

Some possible workarounds for this are documented at sqlite.org, but they aren’t utilized by the default SQLite backend in Django, as incorporating them would be fairly difficult to do robustly. Thus, Django exposes the default SQLite behavior and you should be aware of this when doing case-insensitive or substring filtering.

SQLite has no real decimal internal type. Decimal values are internally converted to the REAL data type (8-byte IEEE floating point number), as explained in the SQLite datatypes documentation, so they don’t support correctly-rounded decimal floating point arithmetic.

SQLite is meant to be a lightweight database, and thus can’t support a high level of concurrency. OperationalError: database is locked errors indicate that your application is experiencing more concurrency than sqlite can handle in default configuration. This error means that one thread or process has an exclusive lock on the database connection and another thread timed out waiting for the lock the be released.

Python’s SQLite wrapper has a default timeout value that determines how long the second thread is allowed to wait on the lock before it times out and raises the OperationalError: database is locked error.

If you’re getting this error, you can solve it by:

Switching to another database backend. At a certain point SQLite becomes too “lite” for real-world applications, and these sorts of concurrency errors indicate you’ve reached that point.

Rewriting your code to reduce concurrency and ensure that database transactions are short-lived.

Increase the default timeout value by setting the timeout database option:

This will make SQLite wait a bit longer before throwing “database is locked” errors; it won’t really do anything to solve them.

SQLite supports three transaction modes: DEFERRED, IMMEDIATE, and EXCLUSIVE.

The default is DEFERRED. If you need to use a different mode, set it in the OPTIONS part of your database configuration in DATABASES, for example:

To make sure your transactions wait until timeout before raising “Database is Locked”, change the transaction mode to IMMEDIATE.

For the best performance with IMMEDIATE and EXCLUSIVE, transactions should be as short as possible. This might be hard to guarantee for all of your views so the usage of ATOMIC_REQUESTS is discouraged in this case.

For more information see Transactions in SQLite.

SQLite does not support the SELECT ... FOR UPDATE syntax. Calling it will have no effect.

There are special considerations described in Isolation In SQLite when modifying a table while iterating over it using QuerySet.iterator(). If a row is added, changed, or deleted within the loop, then that row may or may not appear, or may appear twice, in subsequent results fetched from the iterator. Your code must handle this.

To use JSONField on SQLite, you need to enable the JSON1 extension on Python’s sqlite3 library. If the extension is not enabled on your installation, a system error (fields.E180) will be raised.

To enable the JSON1 extension you can follow the instruction on the wiki page.

The JSON1 extension is enabled by default on SQLite 3.38+.

Pragma options can be set upon connection by using the init_command in the OPTIONS part of your database configuration in DATABASES. The example below shows how to enable extra durability of synchronous writes and change the cache_size:

Django supports Oracle Database Server versions 19c and higher. Version 2.3.0 or higher of the oracledb Python driver is required.

In order for the python manage.py migrate command to work, your Oracle database user must have privileges to run the following commands:

To run a project’s test suite, the user usually needs these additional privileges:

CREATE SESSION WITH ADMIN OPTION

CREATE TABLE WITH ADMIN OPTION

CREATE SEQUENCE WITH ADMIN OPTION

CREATE PROCEDURE WITH ADMIN OPTION

CREATE TRIGGER WITH ADMIN OPTION

While the RESOURCE role has the required CREATE TABLE, CREATE SEQUENCE, CREATE PROCEDURE, and CREATE TRIGGER privileges, and a user granted RESOURCE WITH ADMIN OPTION can grant RESOURCE, such a user cannot grant the individual privileges (e.g. CREATE TABLE), and thus RESOURCE WITH ADMIN OPTION is not usually sufficient for running tests.

Some test suites also create views or materialized views; to run these, the user also needs CREATE VIEW WITH ADMIN OPTION and CREATE MATERIALIZED VIEW WITH ADMIN OPTION privileges. In particular, this is needed for Django’s own test suite.

All of these privileges are included in the DBA role, which is appropriate for use on a private developer’s database.

The Oracle database backend uses the SYS.DBMS_LOB and SYS.DBMS_RANDOM packages, so your user will require execute permissions on it. It’s normally accessible to all users by default, but in case it is not, you’ll need to grant permissions like so:

To connect using the service name of your Oracle database, your settings.py file should look something like this:

In this case, you should leave both HOST and PORT empty. However, if you don’t use a tnsnames.ora file or a similar naming method and want to connect using the SID (“xe” in this example), then fill in both HOST and PORT like so:

You should either supply both HOST and PORT, or leave both as empty strings. Django will use a different connect descriptor depending on that choice.

A Full DSN or Easy Connect string can be used in NAME if both HOST and PORT are empty. This format is required when using RAC or pluggable databases without tnsnames.ora, for example.

Example of an Easy Connect string:

Example of a full DSN string:

To use a connection pool with oracledb, set "pool" to True in the OPTIONS part of your database configuration. This uses the driver’s create_pool() default values:

To pass custom parameters to the driver’s create_pool() function, you can alternatively set "pool" to be a dict:

By default, the Oracle backend uses a RETURNING INTO clause to efficiently retrieve the value of an AutoField when inserting new rows. This behavior may result in a DatabaseError in certain unusual setups, such as when inserting into a remote table, or into a view with an INSTEAD OF trigger. The RETURNING INTO clause can be disabled by setting the use_returning_into option of the database configuration to False:

In this case, the Oracle backend will use a separate SELECT query to retrieve AutoField values.

Oracle imposes a name length limit of 30 characters. To accommodate this, the backend truncates database identifiers to fit, replacing the final four characters of the truncated name with a repeatable MD5 hash value. Additionally, the backend turns database identifiers to all-uppercase.

To prevent these transformations (this is usually required only when dealing with legacy databases or accessing tables which belong to other users), use a quoted name as the value for db_table:

Quoted names can also be used with Django’s other supported database backends; except for Oracle, however, the quotes have no effect.

When running migrate, an ORA-06552 error may be encountered if certain Oracle keywords are used as the name of a model field or the value of a db_column option. Django quotes all identifiers used in queries to prevent most such problems, but this error can still occur when an Oracle datatype is used as a column name. In particular, take care to avoid using the names date, timestamp, number or float as a field name.

Django generally prefers to use the empty string ('') rather than NULL, but Oracle treats both identically. To get around this, the Oracle backend ignores an explicit null option on fields that have the empty string as a possible value and generates DDL as if null=True. When fetching from the database, it is assumed that a NULL value in one of these fields really means the empty string, and the data is silently converted to reflect this assumption.

The Oracle backend stores each TextField as an NCLOB column. Oracle imposes some limitations on the usage of such LOB columns in general:

LOB columns may not be used as primary keys.

LOB columns may not be used in indexes.

LOB columns may not be used in a SELECT DISTINCT list. This means that attempting to use the QuerySet.distinct method on a model that includes TextField columns will result in an ORA-00932 error when run against Oracle. As a workaround, use the QuerySet.defer method in conjunction with distinct() to prevent TextField columns from being included in the SELECT DISTINCT list.

Django comes with built-in database backends. You may subclass an existing database backend to modify its behavior, features, or configuration.

Consider, for example, that you need to change a single database feature. First, you have to create a new directory with a base module in it. For example:

The base.py module must contain a class named DatabaseWrapper that subclasses an existing engine from the django.db.backends module. Here’s an example of subclassing the PostgreSQL engine to change a feature class allows_group_by_selected_pks_on_model:

Finally, you must specify a DATABASE-ENGINE in your settings.py file:

You can see the current list of database engines by looking in django/db/backends.

In addition to the officially supported databases, there are backends provided by 3rd parties that allow you to use other databases with Django:

The Django versions and ORM features supported by these unofficial backends vary considerably. Queries regarding the specific capabilities of these unofficial backends, along with any support queries, should be directed to the support channels provided by each 3rd party project.

---

## Database Functions¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/database-functions/

**Contents:**
- Database Functions¶
- Comparison and conversion functions¶
  - Cast¶
  - Coalesce¶
  - Collate¶
  - Greatest¶
  - Least¶
  - NullIf¶
- Date functions¶
  - Extract¶

The classes documented below provide a way for users to use functions provided by the underlying database as annotations, aggregations, or filters in Django. Functions are also expressions, so they can be used and combined with other expressions like aggregate functions. See the Func documentation for security considerations.

We’ll be using the following model in examples of each function:

We don’t usually recommend allowing null=True for CharField since this allows the field to have two “empty values”, but it’s important for the Coalesce example below.

Forces the result type of expression to be the one from output_field.

Accepts a list of at least two field names or expressions and returns the first non-null value (note that an empty string is not considered a null value). Each argument must be of a similar type, so mixing text and numbers will result in a database error.

A Python value passed to Coalesce on MySQL may be converted to an incorrect type unless explicitly cast to the correct database type:

Takes an expression and a collation name to query against.

For example, to filter case-insensitively in SQLite:

It can also be used when ordering, for example with PostgreSQL:

Accepts a list of at least two field names or expressions and returns the greatest value. Each argument must be of a similar type, so mixing text and numbers will result in a database error.

annotated_comment.last_updated will be the most recent of blog.modified and comment.modified.

The behavior of Greatest when one or more expression may be null varies between databases:

PostgreSQL: Greatest will return the largest non-null expression, or null if all expressions are null.

SQLite, Oracle, and MySQL: If any expression is null, Greatest will return null.

The PostgreSQL behavior can be emulated using Coalesce if you know a sensible minimum value to provide as a default.

Accepts a list of at least two field names or expressions and returns the least value. Each argument must be of a similar type, so mixing text and numbers will result in a database error.

The behavior of Least when one or more expression may be null varies between databases:

PostgreSQL: Least will return the smallest non-null expression, or null if all expressions are null.

SQLite, Oracle, and MySQL: If any expression is null, Least will return null.

The PostgreSQL behavior can be emulated using Coalesce if you know a sensible maximum value to provide as a default.

Accepts two expressions and returns None if they are equal, otherwise returns expression1.

Due to an Oracle convention, this function returns the empty string instead of None when the expressions are of type CharField.

Passing Value(None) to expression1 is prohibited on Oracle since Oracle doesn’t accept NULL as the first argument.

We’ll be using the following model in examples of each function:

Extracts a component of a date as a number.

Takes an expression representing a DateField, DateTimeField, TimeField, or DurationField and a lookup_name, and returns the part of the date referenced by lookup_name as an IntegerField. Django usually uses the databases’ extract function, so you may use any lookup_name that your database supports. A tzinfo subclass, usually provided by zoneinfo, can be passed to extract a value in a specific timezone.

Given the datetime 2015-06-15 23:30:01.000321+00:00, the built-in lookup_names return:

If a different timezone like Australia/Melbourne is active in Django, then the datetime is converted to the timezone before the value is extracted. The timezone offset for Melbourne in the example date above is +10:00. The values returned when this timezone is active will be the same as above except for:

The week_day lookup_type is calculated differently from most databases and from Python’s standard functions. This function will return 1 for Sunday, 2 for Monday, through 7 for Saturday.

The equivalent calculation in Python is:

The week lookup_type is calculated based on ISO-8601, i.e., a week starts on a Monday. The first week of a year is the one that contains the year’s first Thursday, i.e. the first week has the majority (four or more) of its days in the year. The value returned is in the range 1 to 52 or 53.

Each lookup_name above has a corresponding Extract subclass (listed below) that should typically be used instead of the more verbose equivalent, e.g. use ExtractYear(...) rather than Extract(..., lookup_name='year').

Returns the ISO-8601 week-numbering year.

Returns the ISO-8601 week day with day 1 being Monday and day 7 being Sunday.

These are logically equivalent to Extract('date_field', lookup_name). Each class is also a Transform registered on DateField and DateTimeField as __(lookup_name), e.g. __year.

Since DateFields don’t have a time component, only Extract subclasses that deal with date-parts can be used with DateField:

In addition to the following, all extracts for DateField listed above may also be used on DateTimeFields .

These are logically equivalent to Extract('datetime_field', lookup_name). Each class is also a Transform registered on DateTimeField as __(lookup_name), e.g. __minute.

DateTimeField examples:

When USE_TZ is True then datetimes are stored in the database in UTC. If a different timezone is active in Django, the datetime is converted to that timezone before the value is extracted. The example below converts to the Melbourne timezone (UTC +10:00), which changes the day, weekday, and hour values that are returned:

Explicitly passing the timezone to the Extract function behaves in the same way, and takes priority over an active timezone:

Returns the database server’s current date and time when the query is executed, typically using the SQL CURRENT_TIMESTAMP.

PostgreSQL considerations

On PostgreSQL, the SQL CURRENT_TIMESTAMP returns the time that the current transaction started. Therefore for cross-database compatibility, Now() uses STATEMENT_TIMESTAMP instead. If you need the transaction timestamp, use django.contrib.postgres.functions.TransactionNow.

On Oracle, the SQL LOCALTIMESTAMP is used to avoid issues with casting CURRENT_TIMESTAMP to DateTimeField.

Truncates a date up to a significant component.

When you only care if something happened in a particular year, hour, or day, but not the exact second, then Trunc (and its subclasses) can be useful to filter or aggregate your data. For example, you can use Trunc to calculate the number of sales per day.

Trunc takes a single expression, representing a DateField, TimeField, or DateTimeField, a kind representing a date or time part, and an output_field that’s either DateTimeField(), TimeField(), or DateField(). It returns a datetime, date, or time depending on output_field, with fields up to kind set to their minimum value. If output_field is omitted, it will default to the output_field of expression. A tzinfo subclass, usually provided by zoneinfo, can be passed to truncate a value in a specific timezone.

Given the datetime 2015-06-15 14:30:50.000321+00:00, the built-in kinds return:

“year”: 2015-01-01 00:00:00+00:00

“quarter”: 2015-04-01 00:00:00+00:00

“month”: 2015-06-01 00:00:00+00:00

“week”: 2015-06-15 00:00:00+00:00

“day”: 2015-06-15 00:00:00+00:00

“hour”: 2015-06-15 14:00:00+00:00

“minute”: 2015-06-15 14:30:00+00:00

“second”: 2015-06-15 14:30:50+00:00

If a different timezone like Australia/Melbourne is active in Django, then the datetime is converted to the new timezone before the value is truncated. The timezone offset for Melbourne in the example date above is +10:00. The values returned when this timezone is active will be:

“year”: 2015-01-01 00:00:00+11:00

“quarter”: 2015-04-01 00:00:00+10:00

“month”: 2015-06-01 00:00:00+10:00

“week”: 2015-06-16 00:00:00+10:00

“day”: 2015-06-16 00:00:00+10:00

“hour”: 2015-06-16 00:00:00+10:00

“minute”: 2015-06-16 00:30:00+10:00

“second”: 2015-06-16 00:30:50+10:00

The year has an offset of +11:00 because the result transitioned into daylight saving time.

Each kind above has a corresponding Trunc subclass (listed below) that should typically be used instead of the more verbose equivalent, e.g. use TruncYear(...) rather than Trunc(..., kind='year').

The subclasses are all defined as transforms, but they aren’t registered with any fields, because the lookup names are already reserved by the Extract subclasses.

Truncates to midnight on the Monday of the week.

These are logically equivalent to Trunc('date_field', kind). They truncate all parts of the date up to kind which allows grouping or filtering dates with less precision. expression can have an output_field of either DateField or DateTimeField.

Since DateFields don’t have a time component, only Trunc subclasses that deal with date-parts can be used with DateField:

TruncDate casts expression to a date rather than using the built-in SQL truncate function. It’s also registered as a transform on DateTimeField as __date.

TruncTime casts expression to a time rather than using the built-in SQL truncate function. It’s also registered as a transform on DateTimeField as __time.

These are logically equivalent to Trunc('datetime_field', kind). They truncate all parts of the date up to kind and allow grouping or filtering datetimes with less precision. expression must have an output_field of DateTimeField.

These are logically equivalent to Trunc('time_field', kind). They truncate all parts of the time up to kind which allows grouping or filtering times with less precision. expression can have an output_field of either TimeField or DateTimeField.

Since TimeFields don’t have a date component, only Trunc subclasses that deal with time-parts can be used with TimeField:

Accepts a list of field names or expressions and returns a JSON array containing those values.

Takes a list of key-value pairs and returns a JSON object containing those pairs.

We’ll be using the following model in math function examples:

Returns the absolute value of a numeric field or expression.

It can also be registered as a transform. For example:

Returns the arccosine of a numeric field or expression. The expression value must be within the range -1 to 1.

It can also be registered as a transform. For example:

Returns the arcsine of a numeric field or expression. The expression value must be in the range -1 to 1.

It can also be registered as a transform. For example:

Returns the arctangent of a numeric field or expression.

It can also be registered as a transform. For example:

Returns the arctangent of expression1 / expression2.

Returns the smallest integer greater than or equal to a numeric field or expression.

It can also be registered as a transform. For example:

Returns the cosine of a numeric field or expression.

It can also be registered as a transform. For example:

Returns the cotangent of a numeric field or expression.

It can also be registered as a transform. For example:

Converts a numeric field or expression from radians to degrees.

It can also be registered as a transform. For example:

Returns the value of e (the natural logarithm base) raised to the power of a numeric field or expression.

It can also be registered as a transform. For example:

Returns the largest integer value not greater than a numeric field or expression.

It can also be registered as a transform. For example:

Returns the natural logarithm a numeric field or expression.

It can also be registered as a transform. For example:

Accepts two numeric fields or expressions and returns the logarithm of the second to base of the first.

Accepts two numeric fields or expressions and returns the remainder of the first divided by the second (modulo operation).

Returns the value of the mathematical constant π.

Accepts two numeric fields or expressions and returns the value of the first raised to the power of the second.

Converts a numeric field or expression from degrees to radians.

It can also be registered as a transform. For example:

Returns a random value in the range 0.0 ≤ x < 1.0.

Rounds a numeric field or expression to precision (must be an integer) decimal places. By default, it rounds to the nearest integer. Whether half values are rounded up or down depends on the database.

It can also be registered as a transform. For example:

Returns the sign (-1, 0, 1) of a numeric field or expression.

It can also be registered as a transform. For example:

Returns the sine of a numeric field or expression.

It can also be registered as a transform. For example:

Returns the square root of a nonnegative numeric field or expression.

It can also be registered as a transform. For example:

Returns the tangent of a numeric field or expression.

It can also be registered as a transform. For example:

Accepts a numeric field or expression and returns the text representation of the expression as a single character. It works the same as Python’s chr() function.

Like Length, it can be registered as a transform on IntegerField. The default lookup name is chr.

Accepts a list of at least two text fields or expressions and returns the concatenated text. Each argument must be of a text or char type. If you want to concatenate a TextField() with a CharField(), then be sure to tell Django that the output_field should be a TextField(). Specifying an output_field is also required when concatenating a Value as in the example below.

This function will never have a null result. On backends where a null argument results in the entire expression being null, Django will ensure that each null part is converted to an empty string first.

Returns the first length characters of the given text field or expression.

Accepts a single text field or expression and returns the number of characters the value has. If the expression is null, then the length will also be null.

It can also be registered as a transform. For example:

Accepts a single text field or expression and returns the lowercase representation.

It can also be registered as a transform as described in Length.

Returns the value of the given text field or expression padded on the left side with fill_text so that the resulting value is length characters long. The default fill_text is a space.

Similar to Trim, but removes only leading spaces.

Accepts a single text field or expression and returns the MD5 hash of the string.

It can also be registered as a transform as described in Length.

Accepts a single text field or expression and returns the Unicode code point value for the first character of that expression. It works similar to Python’s ord() function, but an exception isn’t raised if the expression is more than one character long.

It can also be registered as a transform as described in Length. The default lookup name is ord.

Returns the value of the given text field or expression repeated number times.

Replaces all occurrences of text with replacement in expression. The default replacement text is the empty string. The arguments to the function are case-sensitive.

Accepts a single text field or expression and returns the characters of that expression in reverse order.

It can also be registered as a transform as described in Length. The default lookup name is reverse.

Returns the last length characters of the given text field or expression.

Similar to LPad, but pads on the right side.

Similar to Trim, but removes only trailing spaces.

Accepts a single text field or expression and returns the particular hash of the string.

They can also be registered as transforms as described in Length.

The pgcrypto extension must be installed. You can use the CryptoExtension migration operation to install it.

Oracle doesn’t support the SHA224 function.

Returns a positive integer corresponding to the 1-indexed position of the first occurrence of substring inside expression, or 0 if substring is not found.

In MySQL, a database table’s collation determines whether string comparisons (such as the expression and substring of this function) are case-sensitive. Comparisons are case-insensitive by default.

Returns a substring of length length from the field or expression starting at position pos. The position is 1-indexed, so the position must be greater than 0. If length is None, then the rest of the string will be returned.

Returns the value of the given text field or expression with leading and trailing spaces removed.

Accepts a single text field or expression and returns the uppercase representation.

It can also be registered as a transform as described in Length.

There are a number of functions to use in a Window expression for computing the rank of elements or the Ntile of some rows.

Calculates the cumulative distribution of a value within a window or partition. The cumulative distribution is defined as the number of rows preceding or peered with the current row divided by the total number of rows in the frame.

Equivalent to Rank but does not have gaps.

Returns the value evaluated at the row that’s the first row of the window frame, or None if no such value exists.

Calculates the value offset by offset, and if no row exists there, returns default.

default must have the same type as the expression, however, this is only validated by the database and not in Python.

MariaDB doesn’t support the default parameter.

Comparable to FirstValue, it calculates the last value in a given frame clause.

Calculates the leading value in a given frame. Both offset and default are evaluated with respect to the current row.

default must have the same type as the expression, however, this is only validated by the database and not in Python.

MariaDB doesn’t support the default parameter.

Computes the row relative to the offset nth (must be a positive value) within the window. Returns None if no row exists.

Some databases may handle a nonexistent nth-value differently. For example, Oracle returns an empty string rather than None for character-based expressions. Django doesn’t do any conversions in these cases.

Calculates a partition for each of the rows in the frame clause, distributing numbers as evenly as possible between 1 and num_buckets. If the rows don’t divide evenly into a number of buckets, one or more buckets will be represented more frequently.

Computes the relative rank of the rows in the frame clause. This computation is equivalent to evaluating:

The following table explains the calculation for the relative rank of a row:

Comparable to RowNumber, this function ranks rows in the window. The computed rank contains gaps. Use DenseRank to compute rank without gaps.

Computes the row number according to the ordering of either the frame clause or the ordering of the whole query if there is no partitioning of the window frame.

---

## django.contrib.postgres¶

**URL:** https://docs.djangoproject.com/en/stable/ref/contrib/postgres/

**Contents:**
- django.contrib.postgres¶

PostgreSQL has a number of features which are not shared by the other databases Django supports. This optional module contains model fields and form fields for a number of PostgreSQL specific data types.

Django is, and will continue to be, a database-agnostic web framework. We would encourage those writing reusable applications for the Django community to write database-agnostic code where practical. However, we recognize that real world projects written using Django need not be database-agnostic. In fact, once a project reaches a given size changing the underlying data store is already a significant challenge and is likely to require changing the code base in some ways to handle differences between the data stores.

Django provides support for a number of data types which will only work with PostgreSQL. There is no fundamental reason why (for example) a contrib.mysql module does not exist, except that PostgreSQL has the richest feature set of the supported databases so its users have the most to gain.

---

## File storage API¶

**URL:** https://docs.djangoproject.com/en/stable/ref/files/storage/

**Contents:**
- File storage API¶
- Getting the default storage class¶
- The FileSystemStorage class¶
- The InMemoryStorage class¶
- The Storage class¶

Django provides convenient ways to access the default storage class:

A dictionary-like object that allows retrieving a storage instance using its alias as defined by STORAGES.

storages has an attribute backends, which defaults to the raw value provided in STORAGES.

Additionally, storages provides a create_storage() method that accepts the dictionary used in STORAGES for a backend, and returns a storage instance based on that backend definition. This may be useful for third-party packages needing to instantiate storages in tests:

DefaultStorage provides lazy access to the default storage system as defined by default key in STORAGES. DefaultStorage uses storages internally.

default_storage is an instance of the DefaultStorage.

The FileSystemStorage class implements basic file storage on a local filesystem. It inherits from Storage and provides implementations for all the public methods thereof.

The FileSystemStorage.delete() method will not raise an exception if the given file name does not exist.

Absolute path to the directory that will hold the files. Defaults to the value of your MEDIA_ROOT setting.

URL that serves the files stored at this location. Defaults to the value of your MEDIA_URL setting.

The file system permissions that the file will receive when it is saved. Defaults to FILE_UPLOAD_PERMISSIONS.

The file system permissions that the directory will receive when it is saved. Defaults to FILE_UPLOAD_DIRECTORY_PERMISSIONS.

Flag to control allowing saving a new file over an existing one. Defaults to False.

Returns a datetime of the system’s ctime, i.e. os.path.getctime(). On some systems (like Unix), this is the time of the last metadata change, and on others (like Windows), it’s the creation time of the file.

The InMemoryStorage class implements a memory-based file storage. It has no persistence, but can be useful for speeding up tests by avoiding disk access.

Absolute path to the directory name assigned to files. Defaults to the value of your MEDIA_ROOT setting.

URL that serves the files stored at this location. Defaults to the value of your MEDIA_URL setting.

The file system permissions assigned to files, provided for compatibility with FileSystemStorage. Defaults to FILE_UPLOAD_PERMISSIONS.

The file system permissions assigned to directories, provided for compatibility with FileSystemStorage. Defaults to FILE_UPLOAD_DIRECTORY_PERMISSIONS.

The Storage class provides a standardized API for storing files, along with a set of default behaviors that all other storage systems can inherit or override as necessary.

When methods return naive datetime objects, the effective timezone used will be the current value of os.environ['TZ']; note that this is usually set from Django’s TIME_ZONE.

Deletes the file referenced by name. If deletion is not supported on the target storage system this will raise NotImplementedError instead.

Returns True if a file referenced by the given name already exists in the storage system.

Returns a datetime of the last accessed time of the file. For storage systems unable to return the last accessed time this will raise NotImplementedError.

If USE_TZ is True, returns an aware datetime, otherwise returns a naive datetime in the local timezone.

Returns an alternative filename based on the file_root and file_ext parameters, an underscore plus a random 7 character alphanumeric string is appended to the filename before the extension.

Returns a filename based on the name parameter that’s free and available for new content to be written to on the target storage system.

The length of the filename will not exceed max_length, if provided. If a free unique filename cannot be found, a SuspiciousFileOperation exception will be raised.

If a file with name already exists, get_alternative_name() is called to obtain an alternative name.

Returns a datetime of the creation time of the file. For storage systems unable to return the creation time this will raise NotImplementedError.

If USE_TZ is True, returns an aware datetime, otherwise returns a naive datetime in the local timezone.

Returns a datetime of the last modified time of the file. For storage systems unable to return the last modified time this will raise NotImplementedError.

If USE_TZ is True, returns an aware datetime, otherwise returns a naive datetime in the local timezone.

Returns a filename based on the name parameter that’s suitable for use on the target storage system.

Validates the filename by calling get_valid_name and returns a filename to be passed to the save() method.

The filename argument may include a path as returned by FileField.upload_to. In that case, the path won’t be passed to get_valid_name but will be prepended back to the resulting name.

The default implementation uses os.path operations. Override this method if that’s not appropriate for your storage.

Lists the contents of the specified path, returning a 2-tuple of lists; the first item being directories, the second item being files. For storage systems that aren’t able to provide such a listing, this will raise a NotImplementedError instead.

Opens the file given by name. Note that although the returned file is guaranteed to be a File object, it might actually be some subclass. In the case of remote file storage this means that reading/writing could be quite slow, so be warned.

The local filesystem path where the file can be opened using Python’s standard open(). For storage systems that aren’t accessible from the local filesystem, this will raise NotImplementedError instead.

Saves a new file using the storage system, preferably with the name specified. If there already exists a file with this name name, the storage system may modify the filename as necessary to get a unique name. The actual name of the stored file will be returned.

The max_length argument is passed along to get_available_name().

The content argument must be an instance of django.core.files.File or a file-like object that can be wrapped in File.

Returns the total size, in bytes, of the file referenced by name. For storage systems that aren’t able to return the file size this will raise NotImplementedError instead.

Returns the URL where the contents of the file referenced by name can be accessed. For storage systems that don’t support access by URL this will raise NotImplementedError instead.

There are community-maintained solutions too!

Django has a vibrant ecosystem. There are storage backends highlighted on the Community Ecosystem page. The Django Packages Storage Backends grid has even more options for you!

---

## Lookup API reference¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/lookups/

**Contents:**
- Lookup API reference¶
- Registration API¶
- The Query Expression API¶
- Transform reference¶
- Lookup reference¶

This document has the API references of lookups, the Django API for building the WHERE clause of a database query. To learn how to use lookups, see Making queries; to learn how to create new lookups, see How to write custom lookups.

The lookup API has two components: a RegisterLookupMixin class that registers lookups, and the Query Expression API, a set of methods that a class has to implement to be registrable as a lookup.

Django has two base classes that follow the query expression API and from where all Django builtin lookups are derived:

Lookup: to lookup a field (e.g. the exact of field_name__exact)

Transform: to transform a field

A lookup expression consists of three parts:

Fields part (e.g. Book.objects.filter(author__best_friends__first_name...);

Transforms part (may be omitted) (e.g. __lower__first3chars__reversed);

A lookup (e.g. __icontains) that, if omitted, defaults to __exact.

Django uses RegisterLookupMixin to give a class the interface to register lookups on itself or its instances. The two prominent examples are Field, the base class of all model fields, and Transform, the base class of all Django transforms.

A mixin that implements the lookup API on a class.

Registers a new lookup in the class or class instance. For example:

will register YearExact lookup on DateField and MonthExact lookup on the User.date_joined (you can use Field Access API to retrieve a single field instance). It overrides a lookup that already exists with the same name. Lookups registered on field instances take precedence over the lookups registered on classes. lookup_name will be used for this lookup if provided, otherwise lookup.lookup_name will be used.

Returns the Lookup named lookup_name registered in the class or class instance depending on what calls it. The default implementation looks recursively on all parent classes and checks if any has a registered lookup named lookup_name, returning the first match. Instance lookups would override any class lookups with the same lookup_name.

Returns a dictionary of each lookup name registered in the class or class instance mapped to the Lookup class.

Returns a Transform named transform_name registered in the class or class instance. The default implementation looks recursively on all parent classes to check if any has the registered transform named transform_name, returning the first match.

For a class to be a lookup, it must follow the Query Expression API. Lookup and Transform naturally follow this API.

The query expression API is a common set of methods that classes define to be usable in query expressions to translate themselves into SQL expressions. Direct field references, aggregates, and Transform are examples that follow this API. A class is said to follow the query expression API when it implements the following methods:

Generates the SQL fragment for the expression. Returns a tuple (sql, params), where sql is the SQL string, and params is the list or tuple of query parameters. The compiler is an SQLCompiler object, which has a compile() method that can be used to compile other expressions. The connection is the connection used to execute the query.

Calling expression.as_sql() is usually incorrect - instead compiler.compile(expression) should be used. The compiler.compile() method will take care of calling vendor-specific methods of the expression.

Custom keyword arguments may be defined on this method if it’s likely that as_vendorname() methods or subclasses will need to supply data to override the generation of the SQL string. See Func.as_sql() for example usage.

Works like as_sql() method. When an expression is compiled by compiler.compile(), Django will first try to call as_vendorname(), where vendorname is the vendor name of the backend used for executing the query. The vendorname is one of postgresql, oracle, sqlite, or mysql for Django’s built-in backends.

Must return the lookup named lookup_name. For instance, by returning self.output_field.get_lookup(lookup_name).

Must return the lookup named transform_name. For instance, by returning self.output_field.get_transform(transform_name).

Defines the type of class returned by the get_lookup() method. It must be a Field instance.

A Transform is a generic class to implement field transformations. A prominent example is __year that transforms a DateField into a IntegerField.

The notation to use a Transform in a lookup expression is <expression>__<transformation> (e.g. date__year).

This class follows the Query Expression API, which implies that you can use <expression>__<transform1>__<transform2>. It’s a specialized Func() expression that only accepts one argument. It can also be used on the right hand side of a filter or directly as an annotation.

A boolean indicating whether this transformation should apply to both lhs and rhs. Bilateral transformations will be applied to rhs in the same order as they appear in the lookup expression. By default it is set to False. For example usage, see How to write custom lookups.

The left-hand side - what is being transformed. It must follow the Query Expression API.

The name of the lookup, used for identifying it on parsing query expressions. It cannot contain the string "__".

Defines the class this transformation outputs. It must be a Field instance. By default is the same as its lhs.output_field.

A Lookup is a generic class to implement lookups. A lookup is a query expression with a left-hand side, lhs; a right-hand side, rhs; and a lookup_name that is used to produce a boolean comparison between lhs and rhs such as lhs in rhs or lhs > rhs.

The primary notation to use a lookup in an expression is <lhs>__<lookup_name>=<rhs>. Lookups can also be used directly in QuerySet filters:

The left-hand side - what is being looked up. The object typically follows the Query Expression API. It may also be a plain value.

The right-hand side - what lhs is being compared against. It can be a plain value, or something that compiles into SQL, typically an F() object or a QuerySet.

The name of this lookup, used to identify it on parsing query expressions. It cannot contain the string "__".

Defaults to True. When rhs is a plain value, prepare_rhs determines whether it should be prepared for use as a parameter in a query. In order to do so, lhs.output_field.get_prep_value() is called if defined, or rhs is wrapped in Value() otherwise.

Returns a tuple (lhs_string, lhs_params), as returned by compiler.compile(lhs). This method can be overridden to tune how the lhs is processed.

compiler is an SQLCompiler object, to be used like compiler.compile(lhs) for compiling lhs. The connection can be used for compiling vendor specific SQL. If lhs is not None, use it as the processed lhs instead of self.lhs.

Behaves the same way as process_lhs(), for the right-hand side.

---

## Migration Operations¶

**URL:** https://docs.djangoproject.com/en/stable/ref/migration-operations/

**Contents:**
- Migration Operations¶
- Schema Operations¶
  - CreateModel¶
  - DeleteModel¶
  - RenameModel¶
  - AlterModelTable¶
  - AlterModelTableComment¶
  - AlterUniqueTogether¶
  - AlterIndexTogether¶
  - AlterOrderWithRespectTo¶

Migration files are composed of one or more Operations, objects that declaratively record what the migration should do to your database.

Django also uses these Operation objects to work out what your models looked like historically, and to calculate what changes you’ve made to your models since the last migration so it can automatically write your migrations; that’s why they’re declarative, as it means Django can easily load them all into memory and run through them without touching the database to work out what your project should look like.

There are also more specialized Operation objects which are for things like data migrations and for advanced manual database manipulation. You can also write your own Operation classes if you want to encapsulate a custom change you commonly make.

If you need an empty migration file to write your own Operation objects into, use python manage.py makemigrations --empty yourappname, but be aware that manually adding schema-altering operations can confuse the migration autodetector and make resulting runs of makemigrations output incorrect code.

All of the core Django operations are available from the django.db.migrations.operations module.

For introductory material, see the migrations topic guide.

Creates a new model in the project history and a corresponding table in the database to match it.

name is the model name, as would be written in the models.py file.

fields is a list of 2-tuples of (field_name, field_instance). The field instance should be an unbound field (so just models.CharField(...), rather than a field taken from another model).

options is an optional dictionary of values from the model’s Meta class.

bases is an optional list of other classes to have this model inherit from; it can contain both class objects as well as strings in the format "appname.ModelName" if you want to depend on another model (so you inherit from the historical version). If it’s not supplied, it defaults to inheriting from the standard models.Model.

managers takes a list of 2-tuples of (manager_name, manager_instance). The first manager in the list will be the default manager for this model during migrations.

Deletes the model from the project history and its table from the database.

Renames the model from an old name to a new one.

You may have to manually add this if you change the model’s name and quite a few of its fields at once; to the autodetector, this will look like you deleted a model with the old name and added a new one with a different name, and the migration it creates will lose any data in the old table.

Changes the model’s table name (the db_table option on the Meta subclass).

Changes the model’s table comment (the db_table_comment option on the Meta subclass).

Changes the model’s set of unique constraints (the unique_together option on the Meta subclass).

Changes the model’s set of custom indexes (the index_together option on the Meta subclass).

AlterIndexTogether is officially supported only for pre-Django 4.2 migration files. For backward compatibility reasons, it’s still part of the public API, and there’s no plan to deprecate or remove it, but it should not be used for new migrations. Use AddIndex and RemoveIndex operations instead.

Makes or deletes the _order column needed for the order_with_respect_to option on the Meta subclass.

Stores changes to miscellaneous model options (settings on a model’s Meta) like permissions and verbose_name. Does not affect the database, but persists these changes for RunPython instances to use. options should be a dictionary mapping option names to values.

Alters the managers that are available during migrations.

Adds a field to a model. model_name is the model’s name, name is the field’s name, and field is an unbound Field instance (the thing you would put in the field declaration in models.py - for example, models.IntegerField(null=True).

The preserve_default argument indicates whether the field’s default value is permanent and should be baked into the project state (True), or if it is temporary and just for this migration (False) - usually because the migration is adding a non-nullable field to a table and needs a default value to put into existing rows. It does not affect the behavior of setting defaults in the database directly - Django never sets database defaults and always applies them in the Django ORM code.

On older databases, adding a field with a default value may cause a full rewrite of the table. This happens even for nullable fields and may have a negative performance impact. To avoid that, the following steps should be taken.

Add the nullable field without the default value and run the makemigrations command. This should generate a migration with an AddField operation.

Add the default value to your field and run the makemigrations command. This should generate a migration with an AlterField operation.

Removes a field from a model.

Bear in mind that when reversed, this is actually adding a field to a model. The operation is reversible (apart from any data loss, which is irreversible) if the field is nullable or if it has a default value that can be used to populate the recreated column. If the field is not nullable and does not have a default value, the operation is irreversible.

BaseDatabaseSchemaEditor and PostgreSQL backends no longer use CASCADE to delete dependent related database objects, such as views. Any dependent objects that are not managed by Django may need to be removed manually before running RemoveField.

Alters a field’s definition, including changes to its type, null, unique, db_column and other field attributes.

The preserve_default argument indicates whether the field’s default value is permanent and should be baked into the project state (True), or if it is temporary and just for this migration (False) - usually because the migration is altering a nullable field to a non-nullable one and needs a default value to put into existing rows. It does not affect the behavior of setting defaults in the database directly - Django never sets database defaults and always applies them in the Django ORM code.

Note that not all changes are possible on all databases - for example, you cannot change a text-type field like models.TextField() into a number-type field like models.IntegerField() on most databases.

Changes a field’s name (and, unless db_column is set, its column name).

Creates an index in the database table for the model with model_name. index is an instance of the Index class.

Removes the index named name from the model with model_name.

Renames an index in the database table for the model with model_name. Exactly one of old_name and old_fields can be provided. old_fields is an iterable of the strings, often corresponding to fields of index_together (pre-Django 5.1 option).

On databases that don’t support an index renaming statement (SQLite), the operation will drop and recreate the index, which can be expensive.

Creates a constraint in the database table for the model with model_name.

Removes the constraint named name from the model with model_name.

Alters the constraint named name of the model with model_name with the new constraint without affecting the database.

Allows running of arbitrary SQL on the database - useful for more advanced features of database backends that Django doesn’t support directly.

sql, and reverse_sql if provided, should be strings of SQL to run on the database. On most database backends (all but PostgreSQL), Django will split the SQL into individual statements prior to executing them.

On PostgreSQL and SQLite, only use BEGIN or COMMIT in your SQL in non-atomic migrations, to avoid breaking Django’s transaction state.

You can also pass a list of strings or 2-tuples. The latter is used for passing queries and parameters in the same way as cursor.execute(). These three operations are equivalent:

If you want to include literal percent signs in the query, you have to double them if you are passing parameters.

The reverse_sql queries are executed when the migration is unapplied. They should undo what is done by the sql queries. For example, to undo the above insertion with a deletion:

If reverse_sql is None (the default), the RunSQL operation is irreversible.

The state_operations argument allows you to supply operations that are equivalent to the SQL in terms of project state. For example, if you are manually creating a column, you should pass in a list containing an AddField operation here so that the autodetector still has an up-to-date state of the model. If you don’t, when you next run makemigrations, it won’t see any operation that adds that field and so will try to run it again. For example:

The optional hints argument will be passed as **hints to the allow_migrate() method of database routers to assist them in making routing decisions. See Hints for more details on database hints.

The optional elidable argument determines whether or not the operation will be removed (elided) when squashing migrations.

Pass the RunSQL.noop attribute to sql or reverse_sql when you want the operation not to do anything in the given direction. This is especially useful in making the operation reversible.

Runs custom Python code in a historical context. code (and reverse_code if supplied) should be callable objects that accept two arguments; the first is an instance of django.apps.registry.Apps containing historical models that match the operation’s place in the project history, and the second is an instance of SchemaEditor.

The reverse_code argument is called when unapplying migrations. This callable should undo what is done in the code callable so that the migration is reversible. If reverse_code is None (the default), the RunPython operation is irreversible.

The optional hints argument will be passed as **hints to the allow_migrate() method of database routers to assist them in making a routing decision. See Hints for more details on database hints.

The optional elidable argument determines whether or not the operation will be removed (elided) when squashing migrations.

You are advised to write the code as a separate function above the Migration class in the migration file, and pass it to RunPython. Here’s an example of using RunPython to create some initial objects on a Country model:

This is generally the operation you would use to create data migrations, run custom data updates and alterations, and anything else you need access to an ORM and/or Python code for.

Much like RunSQL, ensure that if you change schema inside here you’re either doing it outside the scope of the Django model system (e.g. triggers) or that you use SeparateDatabaseAndState to add in operations that will reflect your changes to the model state - otherwise, the versioned ORM and the autodetector will stop working correctly.

By default, RunPython will run its contents inside a transaction on databases that do not support DDL transactions (for example, MySQL and Oracle). This should be safe, but may cause a crash if you attempt to use the schema_editor provided on these backends; in this case, pass atomic=False to the RunPython operation.

On databases that do support DDL transactions (SQLite and PostgreSQL), RunPython operations do not have any transactions automatically added besides the transactions created for each migration. Thus, on PostgreSQL, for example, you should avoid combining schema changes and RunPython operations in the same migration or you may hit errors like OperationalError: cannot ALTER TABLE "mytable" because it has pending trigger events.

If you have a different database and aren’t sure if it supports DDL transactions, check the django.db.connection.features.can_rollback_ddl attribute.

If the RunPython operation is part of a non-atomic migration, the operation will only be executed in a transaction if atomic=True is passed to the RunPython operation.

RunPython does not magically alter the connection of the models for you; any model methods you call will go to the default database unless you give them the current database alias (available from schema_editor.connection.alias, where schema_editor is the second argument to your function).

Pass the RunPython.noop method to code or reverse_code when you want the operation not to do anything in the given direction. This is especially useful in making the operation reversible.

A highly specialized operation that lets you mix and match the database (schema-changing) and state (autodetector-powering) aspects of operations.

It accepts two lists of operations. When asked to apply state, it will use the state_operations list (this is a generalized version of RunSQL’s state_operations argument). When asked to apply changes to the database, it will use the database_operations list.

If the actual state of the database and Django’s view of the state get out of sync, this can break the migration framework, even leading to data loss. It’s worth exercising caution and checking your database and state operations carefully. You can use sqlmigrate and dbshell to check your database operations. You can use makemigrations, especially with --dry-run, to check your state operations.

For an example using SeparateDatabaseAndState, see Changing a ManyToManyField to use a through model.

Categories of migration operation used by the makemigrations command to display meaningful symbols.

Operations have a relatively simple API, and they’re designed so that you can easily write your own to supplement the built-in Django ones. The basic structure of an Operation looks like this:

You can take this template and work from it, though we suggest looking at the built-in Django operations in django.db.migrations.operations - they cover a lot of the example usage of semi-internal aspects of the migration framework like ProjectState and the patterns used to get historical models, as well as ModelState and the patterns used to mutate historical models in state_forwards().

You don’t need to learn too much about ProjectState to write migrations; just know that it has an apps property that gives access to an app registry (which you can then call get_model on).

database_forwards and database_backwards both get two states passed to them; these represent the difference the state_forwards method would have applied, but are given to you for convenience and speed reasons.

If you want to work with model classes or model instances from the from_state argument in database_forwards() or database_backwards(), you must render model states using the clear_delayed_apps_cache() method to make related models available:

to_state in the database_backwards method is the older state; that is, the one that will be the current state once the migration has finished reversing.

You might see implementations of references_model on the built-in operations; this is part of the autodetection code and does not matter for custom operations.

For performance reasons, the Field instances in ModelState.fields are reused across migrations. You must never change the attributes on these instances. If you need to mutate a field in state_forwards(), you must remove the old instance from ModelState.fields and add a new instance in its place. The same is true for the Manager instances in ModelState.managers.

As an example, let’s make an operation that loads PostgreSQL extensions (which contain some of PostgreSQL’s more exciting features). Since there’s no model state changes, all it does is run one command:

---

## Model class reference¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/class/

**Contents:**
- Model class reference¶
- Attributes¶
  - DoesNotExist¶
  - MultipleObjectsReturned¶
  - NotUpdated¶
  - objects¶

This document covers features of the Model class. For more information about models, see the complete list of Model reference guides.

This exception is raised by the ORM when an expected object is not found. For example, QuerySet.get() will raise it when no object is found for the given lookups.

Django provides a DoesNotExist exception as an attribute of each model class to identify the class of object that could not be found, allowing you to catch exceptions for a particular model class. The exception is a subclass of django.core.exceptions.ObjectDoesNotExist.

This exception is raised by QuerySet.get() when multiple objects are found for the given lookups.

Django provides a MultipleObjectsReturned exception as an attribute of each model class to identify the class of object for which multiple objects were found, allowing you to catch exceptions for a particular model class. The exception is a subclass of django.core.exceptions.MultipleObjectsReturned.

This exception is raised when a forced update of a Model instance does not affect any rows.

Django provides a NotUpdated exception as an attribute of each model class to identify the class of object that could not be updated, allowing you to catch exceptions for a particular model class. The exception is a subclass of django.core.exceptions.ObjectNotUpdated and inherits from django.db.DatabaseError for backward compatibility reasons.

Each non-abstract Model class must have a Manager instance added to it. Django ensures that in your model class you have at least a default Manager specified. If you don’t add your own Manager, Django will add an attribute objects containing default Manager instance. If you add your own Manager instance attribute, the default one does not appear. Consider the following example:

For more details on model managers see Managers and Retrieving objects.

---

## Model field reference¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/fields/

**Contents:**
- Model field reference¶
- Field options¶
  - null¶
  - blank¶
  - choices¶
    - Enumeration types¶
  - db_column¶
  - db_comment¶
  - db_default¶
  - db_index¶

This document contains all the API references of Field including the field options and field types Django offers.

If the built-in fields don’t do the trick, you can try django-localflavor (documentation), which contains assorted pieces of code that are useful for particular countries and cultures.

Also, you can easily write your own custom model fields.

Fields are defined in django.db.models.fields, but for convenience they’re imported into django.db.models. The standard convention is to use from django.db import models and refer to fields as models.<Foo>Field.

The following arguments are available to all field types. All are optional.

If True, Django will store empty values as NULL in the database. Default is False.

Avoid using null on string-based fields such as CharField and TextField. The Django convention is to use an empty string, not NULL, as the “no data” state for string-based fields. If a string-based field has null=False, empty strings can still be saved for “no data”. If a string-based field has null=True, that means it has two possible values for “no data”: NULL, and the empty string. In most cases, it’s redundant to have two possible values for “no data”. One exception is when a CharField has both unique=True and blank=True set. In this situation, null=True is required to avoid unique constraint violations when saving multiple objects with blank values.

For both string-based and non-string-based fields, you will also need to set blank=True if you wish to permit empty values in forms, as the null parameter only affects database storage (see blank).

When using the Oracle database backend, the value NULL will be stored to denote the empty string regardless of this attribute.

If True, the field is allowed to be blank. Default is False.

Note that this is different than null. null is purely database-related, whereas blank is validation-related. If a field has blank=True, form validation will allow entry of an empty value. If a field has blank=False, the field will be required.

Supplying missing values

blank=True can be used with fields having null=False, but this will require implementing clean() on the model in order to programmatically supply any missing values.

A mapping or iterable in the format described below to use as choices for this field. If choices are given, they’re enforced by model validation and the default form widget will be a select box with these choices instead of the standard text field.

If a mapping is given, the key element is the actual value to be set on the model, and the second element is the human readable name. For example:

You can also pass a sequence consisting itself of iterables of exactly two items (e.g. [(A1, B1), (A2, B2), …]). The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name. For example:

choices can also be defined as a callable that expects no arguments and returns any of the formats described above. For example:

Passing a callable for choices can be particularly handy when, for example, the choices are:

the result of I/O-bound operations (which could potentially be cached), such as querying a table in the same or an external database, or accessing the choices from a static file.

a list that is mostly stable but could vary from time to time or from project to project. Examples in this category are using third-party apps that provide a well-known inventory of values, such as currencies, countries, languages, time zones, etc.

Generally, it’s best to define choices inside a model class, and to define a suitably-named constant for each value:

Though you can define a choices list outside of a model class and then refer to it, defining the choices and names for each choice inside the model class keeps all of that information with the class that uses it, and helps reference the choices (e.g, Student.SOPHOMORE will work anywhere that the Student model has been imported).

You can also collect your available choices into named groups that can be used for organizational purposes:

The key of the mapping is the name to apply to the group and the value is the choices inside that group, consisting of the field value and a human-readable name for an option. Grouped options may be combined with ungrouped options within a single mapping (such as the "unknown" option in this example).

You can also use a sequence, e.g. a list of 2-tuples:

Note that choices can be any sequence object – not necessarily a list or tuple. This lets you construct choices dynamically. But if you find yourself hacking choices to be dynamic, you’re probably better off using a proper database table with a ForeignKey. choices is meant for static data that doesn’t change much, if ever.

A new migration is created each time the order of choices changes.

For each model field that has choices set, Django will normalize the choices to a list of 2-tuples and add a method to retrieve the human-readable name for the field’s current value. See get_FOO_display() in the database API documentation.

Unless blank=False is set on the field along with a default then a label containing "---------" will be rendered with the select box. To override this behavior, add a tuple to choices containing None; e.g. (None, 'Your String For Display'). Alternatively, you can use an empty string instead of None where this makes sense - such as on a CharField.

In addition, Django provides enumeration types that you can subclass to define choices in a concise way:

These work similar to enum from Python’s standard library, but with some modifications:

Enum member values are a tuple of arguments to use when constructing the concrete data type. Django supports adding an extra string value to the end of this tuple to be used as the human-readable name, or label. The label can be a lazy translatable string. Thus, in most cases, the member value will be a (value, label) 2-tuple. See below for an example of subclassing choices using a more complex data type. If a tuple is not provided, or the last item is not a (lazy) string, the label is automatically generated from the member name.

A .label property is added on values, to return the human-readable name.

A number of custom properties are added to the enumeration classes – .choices, .labels, .values, and .names – to make it easier to access lists of those separate parts of the enumeration.

These property names cannot be used as member names as they would conflict.

The use of enum.unique() is enforced to ensure that values cannot be defined multiple times. This is unlikely to be expected in choices for a field.

Note that using YearInSchool.SENIOR, YearInSchool['SENIOR'], or YearInSchool('SR') to access or lookup enum members work as expected, as do the .name and .value properties on the members.

If you don’t need to have the human-readable names translated, you can have them inferred from the member name (replacing underscores with spaces and using title-case):

Since the case where the enum values need to be integers is extremely common, Django provides an IntegerChoices class. For example:

It is also possible to make use of the Enum Functional API with the caveat that labels are automatically generated as highlighted above:

If you require support for a concrete data type other than int or str, you can subclass Choices and the required concrete data type, e.g. date for use with DateField:

There are some additional caveats to be aware of:

Enumeration types do not support named groups.

Because an enumeration with a concrete data type requires all values to match the type, overriding the blank label cannot be achieved by creating a member with a value of None. Instead, set the __empty__ attribute on the class:

The name of the database column to use for this field. If this isn’t given, Django will use the field’s name.

If your database column name is an SQL reserved word, or contains characters that aren’t allowed in Python variable names – notably, the hyphen – that’s OK. Django quotes column and table names behind the scenes.

The comment on the database column to use for this field. It is useful for documenting fields for individuals with direct database access who may not be looking at your Django code. For example:

The database-computed default value for this field. This can be a literal value or a database function, such as Now:

More complex expressions can be used, as long as they are made from literals and database functions:

Database defaults cannot reference other fields or models. For example, this is invalid:

If both db_default and Field.default are set, default will take precedence when creating instances in Python code. db_default will still be set at the database level and will be used when inserting rows outside of the ORM or when adding a new field in a migration.

If a field has a db_default without a default set and no value is assigned to the field, a DatabaseDefault object is returned as the field value on unsaved model instances. The actual value for the field is determined by the database when the model instance is saved.

If True, a database index will be created for this field.

Use the indexes option instead.

Where possible, use the Meta.indexes option instead. In nearly all cases, indexes provides more functionality than db_index. db_index may be deprecated in the future.

The name of the database tablespace to use for this field’s index, if this field is indexed. The default is the project’s DEFAULT_INDEX_TABLESPACE setting, if set, or the db_tablespace of the model, if any. If the backend doesn’t support tablespaces for indexes, this option is ignored.

The default value for the field. This can be a value or a callable object. If callable it will be called every time a new object is created.

The default can’t be a mutable object (model instance, list, set, etc.), as a reference to the same instance of that object would be used as the default value in all new model instances. Instead, wrap the desired default in a callable. For example, if you want to specify a default dict for JSONField, use a function:

lambdas can’t be used for field options like default because they can’t be serialized by migrations. See that documentation for other caveats.

For fields like ForeignKey that map to model instances, defaults should be the value of the field they reference (pk unless to_field is set) instead of model instances.

The default value is used when new model instances are created and a value isn’t provided for the field. When the field is a primary key, the default is also used when the field is set to None.

The default value can also be set at the database level with Field.db_default.

If False, the field will not be displayed in the admin or any other ModelForm. It will also be skipped during model validation. Default is True.

The error_messages argument lets you override the default messages that the field will raise. Pass in a dictionary with keys matching the error messages you want to override.

Error message keys include null, blank, invalid, invalid_choice, unique, and unique_for_date. Additional error message keys are specified for each field in the Field types section below.

These error messages often don’t propagate to forms. See Considerations regarding model’s error_messages.

Extra “help” text to be displayed with the form widget. It’s useful for documentation even if your field isn’t used on a form.

Note that this value is not HTML-escaped in automatically-generated forms. This lets you include HTML in help_text if you so desire. For example:

Alternatively you can use plain text and django.utils.html.escape() to escape any HTML special characters. Ensure that you escape any help text that may come from untrusted users to avoid a cross-site scripting attack.

If True, this field is the primary key for the model.

If you don’t specify primary_key=True for any field in your model and have not defined a composite primary key, Django will automatically add a field to hold the primary key. So, you don’t need to set primary_key=True on any of your fields unless you want to override the default primary-key behavior. The type of auto-created primary key fields can be specified per app in AppConfig.default_auto_field or globally in the DEFAULT_AUTO_FIELD setting. For more, see Automatic primary key fields.

primary_key=True implies null=False and unique=True. Only one field per model can set primary_key=True. Composite primary keys must be defined using CompositePrimaryKey instead of setting this flag to True for all fields to maintain this invariant.

The primary key field is read-only. If you change the value of the primary key on an existing object and then save it, a new object will be created alongside the old one.

The primary key field is set to None when deleting an object.

The CompositePrimaryKey field was added.

If True, this field must be unique throughout the table.

This is enforced at the database level and by model validation. If you try to save a model with a duplicate value in a unique field, a django.db.IntegrityError will be raised by the model’s save() method.

This option is valid on all field types except ManyToManyField and OneToOneField.

Note that when unique is True, you don’t need to specify db_index, because unique implies the creation of an index.

Set this to the name of a DateField or DateTimeField to require that this field be unique for the value of the date field.

For example, if you have a field title that has unique_for_date="pub_date", then Django wouldn’t allow the entry of two records with the same title and pub_date.

Note that if you set this to point to a DateTimeField, only the date portion of the field will be considered. Besides, when USE_TZ is True, the check will be performed in the current time zone at the time the object gets saved.

This is enforced by Model.validate_unique() during model validation but not at the database level. If any unique_for_date constraint involves fields that are not part of a ModelForm (for example, if one of the fields is listed in exclude or has editable=False), Model.validate_unique() will skip validation for that particular constraint.

Like unique_for_date, but requires the field to be unique with respect to the month.

Like unique_for_date and unique_for_month.

A human-readable name for the field. If the verbose name isn’t given, Django will automatically create it using the field’s attribute name, converting underscores to spaces. See Verbose field names.

A list of validators to run for this field. See the validators documentation for more information.

An IntegerField that automatically increments according to available IDs. You usually won’t need to use this directly; a primary key field will automatically be added to your model if you don’t specify otherwise. See Automatic primary key fields.

A 64-bit integer, much like an AutoField except that it is guaranteed to fit numbers from 1 to 9223372036854775807.

A 64-bit integer, much like an IntegerField except that it is guaranteed to fit numbers from -9223372036854775808 to 9223372036854775807. The default form widget for this field is a NumberInput.

A field to store raw binary data. It can be assigned bytes, bytearray, or memoryview.

By default, BinaryField sets editable to False, in which case it can’t be included in a ModelForm.

Optional. The maximum length (in bytes) of the field. The maximum length is enforced in Django’s validation using MaxLengthValidator.

Although you might think about storing files in the database, consider that it is bad design in 99% of the cases. This field is not a replacement for proper static files handling.

The default form widget for this field is CheckboxInput, or NullBooleanSelect if null=True.

The default value of BooleanField is None when Field.default isn’t defined.

A virtual field used for defining a composite primary key.

This field must be defined as the model’s pk attribute. If present, Django will create the underlying model table with a composite primary key.

The *field_names argument is a list of positional field names that compose the primary key.

See Composite primary keys for more details.

A string field, for small- to large-sized strings.

For large amounts of text, use TextField.

The default form widget for this field is a TextInput.

CharField has the following extra arguments:

The maximum length (in characters) of the field. The max_length is enforced at the database level and in Django’s validation using MaxLengthValidator. It’s required for all database backends included with Django except PostgreSQL and SQLite, which supports unlimited VARCHAR columns.

If you are writing an application that must be portable to multiple database backends, you should be aware that there are restrictions on max_length for some backends. Refer to the database backend notes for details.

Support for unlimited VARCHAR columns was added on SQLite.

Optional. The database collation name of the field.

Collation names are not standardized. As such, this will not be portable across multiple database backends.

Oracle supports collations only when the MAX_STRING_SIZE database initialization parameter is set to EXTENDED.

A date, represented in Python by a datetime.date instance. Has a few extra, optional arguments:

Automatically set the field to now every time the object is saved. Useful for “last-modified” timestamps. Note that the current date is always used; it’s not just a default value that you can override.

The field is only automatically updated when calling Model.save(). The field isn’t updated when making updates to other fields in other ways such as QuerySet.update(), though you can specify a custom value for the field in an update like that.

Automatically set the field to now when the object is first created. Useful for creation of timestamps. Note that the current date is always used; it’s not just a default value that you can override. So even if you set a value for this field when creating the object, it will be ignored. If you want to be able to modify this field, set the following instead of auto_now_add=True:

For DateField: default=date.today - from datetime.date.today()

For DateTimeField: default=timezone.now - from django.utils.timezone.now()

The default form widget for this field is a DateInput. The admin adds a JavaScript calendar, and a shortcut for “Today”. Includes an additional invalid_date error message key.

The options auto_now_add, auto_now, and default are mutually exclusive. Any combination of these options will result in an error.

As currently implemented, setting auto_now or auto_now_add to True will cause the field to have editable=False and blank=True set.

The auto_now and auto_now_add options will always use the date in the default timezone at the moment of creation or update. If you need something different, you may want to consider using your own callable default or overriding save() instead of using auto_now or auto_now_add; or using a DateTimeField instead of a DateField and deciding how to handle the conversion from datetime to date at display time.

Always use DateField with a datetime.date instance.

If you have a datetime.datetime instance, it’s recommended to convert it to a datetime.date first. If you don’t, DateField will localize the datetime.datetime to the default timezone and convert it to a datetime.date instance, removing its time component. This is true for both storage and comparison.

On PostgreSQL and MySQL, arithmetic operations on a DateField with a timedelta return a datetime instead of a date. This occurs because Python’s timedelta is converted to SQL INTERVAL, and the SQL operation date +/- interval returns a timestamp on these databases.

To ensure a date result, use one of the following approaches. Either explicitly cast the result to a date:

Or on PostgreSQL only, use integer arithmetic to represent days:

A date and time, represented in Python by a datetime.datetime instance. Takes the same extra arguments as DateField.

The default form widget for this field is a single DateTimeInput. The admin uses two separate TextInput widgets with JavaScript shortcuts.

Always use DateTimeField with a datetime.datetime instance.

If you have a datetime.date instance, it’s recommended to convert it to a datetime.datetime first. If you don’t, DateTimeField will use midnight in the default timezone for the time component. This is true for both storage and comparison. To compare the date portion of a DateTimeField with a datetime.date instance, use the date lookup.

A fixed-precision decimal number, represented in Python by a Decimal instance. It validates the input using DecimalValidator.

Has the following required arguments:

The maximum number of digits allowed in the number. Note that this number must be greater than or equal to decimal_places.

The number of decimal places to store with the number.

For example, to store numbers up to 999.99 with a resolution of 2 decimal places, you’d use:

And to store numbers up to approximately one billion with a resolution of 10 decimal places:

The default form widget for this field is a NumberInput when localize is False or TextInput otherwise.

For more information about the differences between the FloatField and DecimalField classes, please see FloatField vs. DecimalField. You should also be aware of SQLite limitations of decimal fields.

A field for storing periods of time - modeled in Python by timedelta. When used on PostgreSQL, the data type used is an interval and on Oracle the data type is INTERVAL DAY(9) TO SECOND(6). Otherwise a bigint of microseconds is used.

Arithmetic with DurationField works in most cases. However on all databases other than PostgreSQL, comparing the value of a DurationField to arithmetic on DateTimeField instances will not work as expected.

A CharField that checks that the value is a valid email address using EmailValidator.

The primary_key argument isn’t supported and will raise an error if used.

Has the following optional arguments:

This attribute provides a way of setting the upload directory and file name, and can be set in two ways. In both cases, the value is passed to the Storage.save() method.

If you specify a string value or a Path, it may contain strftime() formatting, which will be replaced by the date/time of the file upload (so that uploaded files don’t fill up the given directory). For example:

If you are using the default FileSystemStorage, the string value will be appended to your MEDIA_ROOT path to form the location on the local filesystem where uploaded files will be stored. If you are using a different storage, check that storage’s documentation to see how it handles upload_to.

upload_to may also be a callable, such as a function. This will be called to obtain the upload path, including the filename. This callable must accept two arguments and return a Unix-style path (with forward slashes) to be passed along to the storage system. The two arguments are:

An instance of the model where the FileField is defined. More specifically, this is the particular instance where the current file is being attached.

In most cases, this object will not have been saved to the database yet, so if it uses the default AutoField, it might not yet have a value for its primary key field.

The filename that was originally given to the file. This may or may not be taken into account when determining the final destination path.

A storage object, or a callable which returns a storage object. This handles the storage and retrieval of your files. See Managing files for details on how to provide this object.

The default form widget for this field is a ClearableFileInput.

Using a FileField or an ImageField (see below) in a model takes a few steps:

In your settings file, you’ll need to define MEDIA_ROOT as the full path to a directory where you’d like Django to store uploaded files. (For performance, these files are not stored in the database.) Define MEDIA_URL as the base public URL of that directory. Make sure that this directory is writable by the web server’s user account.

Add the FileField or ImageField to your model, defining the upload_to option to specify a subdirectory of MEDIA_ROOT to use for uploaded files.

All that will be stored in your database is a path to the file (relative to MEDIA_ROOT). You’ll most likely want to use the convenience url attribute provided by Django. For example, if your ImageField is called mug_shot, you can get the absolute path to your image in a template with {{ object.mug_shot.url }}.

For example, say your MEDIA_ROOT is set to '/home/media', and upload_to is set to 'photos/%Y/%m/%d'. The '%Y/%m/%d' part of upload_to is strftime() formatting; '%Y' is the four-digit year, '%m' is the two-digit month and '%d' is the two-digit day. If you upload a file on Jan. 15, 2007, it will be saved in the directory /home/media/photos/2007/01/15.

If you wanted to retrieve the uploaded file’s on-disk filename, or the file’s size, you could use the name and size attributes respectively; for more information on the available attributes and methods, see the File class reference and the Managing files topic guide.

The file is saved as part of saving the model in the database, so the actual file name used on disk cannot be relied on until after the model has been saved.

The uploaded file’s relative URL can be obtained using the url attribute. Internally, this calls the url() method of the underlying Storage class.

Note that whenever you deal with uploaded files, you should pay close attention to where you’re uploading them and what type of files they are, to avoid security holes. Validate all uploaded files so that you’re sure the files are what you think they are. For example, if you blindly let somebody upload files, without validation, to a directory that’s within your web server’s document root, then somebody could upload a CGI or PHP script and execute that script by visiting its URL on your site. Don’t allow that.

Also note that even an uploaded HTML file, since it can be executed by the browser (though not by the server), can pose security threats that are equivalent to XSS or CSRF attacks.

FileField instances are created in your database as varchar columns with a default max length of 100 characters. As with other fields, you can change the maximum length using the max_length argument.

When you access a FileField on a model, you are given an instance of FieldFile as a proxy for accessing the underlying file.

The API of FieldFile mirrors that of File, with one key difference: The object wrapped by the class is not necessarily a wrapper around Python’s built-in file object. Instead, it is a wrapper around the result of the Storage.open() method, which may be a File object, or it may be a custom storage’s implementation of the File API.

In addition to the API inherited from File such as read() and write(), FieldFile includes several methods that can be used to interact with the underlying file:

Two methods of this class, save() and delete(), default to saving the model object of the associated FieldFile in the database.

The name of the file including the relative path from the root of the Storage of the associated FileField.

A read-only property to access the file’s local filesystem path by calling the path() method of the underlying Storage class.

The result of the underlying Storage.size() method.

A read-only property to access the file’s relative URL by calling the url() method of the underlying Storage class.

Opens or reopens the file associated with this instance in the specified mode. Unlike the standard Python open() method, it doesn’t return a file descriptor.

Since the underlying file is opened implicitly when accessing it, it may be unnecessary to call this method except to reset the pointer to the underlying file or to change the mode.

Behaves like the standard Python file.close() method and closes the file associated with this instance.

This method takes a filename and file contents and passes them to the storage class for the field, then associates the stored file with the model field. If you want to manually associate file data with FileField instances on your model, the save() method is used to persist that file data.

Takes two required arguments: name which is the name of the file, and content which is an object containing the file’s contents. The optional save argument controls whether or not the model instance is saved after the file associated with this field has been altered. Defaults to True.

Note that the content argument should be an instance of django.core.files.File, not Python’s built-in file object. You can construct a File from an existing Python file object like this:

Or you can construct one from a Python string like this:

For more information, see Managing files.

Deletes the file associated with this instance and clears all attributes on the field. Note: This method will close the file if it happens to be open when delete() is called.

The optional save argument controls whether or not the model instance is saved after the file associated with this field has been deleted. Defaults to True.

Note that when a model is deleted, related files are not deleted. If you need to cleanup orphaned files, you’ll need to handle it yourself (for instance, with a custom management command that can be run manually or scheduled to run periodically via e.g. cron).

A CharField whose choices are limited to the filenames in a certain directory on the filesystem. Has some special arguments, of which the first is required:

Required. The absolute filesystem path to a directory from which this FilePathField should get its choices. Example: "/home/images".

path may also be a callable, such as a function to dynamically set the path at runtime. Example:

Optional. A regular expression, as a string, that FilePathField will use to filter filenames. Note that the regex will be applied to the base filename, not the full path. Example: "foo.*\.txt$", which will match a file called foo23.txt but not bar.txt or foo23.png.

Optional. Either True or False. Default is False. Specifies whether all subdirectories of path should be included

Optional. Either True or False. Default is True. Specifies whether files in the specified location should be included. Either this or allow_folders must be True.

Optional. Either True or False. Default is False. Specifies whether folders in the specified location should be included. Either this or allow_files must be True.

The one potential gotcha is that match applies to the base filename, not the full path. So, this example:

…will match /home/images/foo.png but not /home/images/foo/bar.png because the match applies to the base filename (foo.png and bar.png).

FilePathField instances are created in your database as varchar columns with a default max length of 100 characters. As with other fields, you can change the maximum length using the max_length argument.

A floating-point number represented in Python by a float instance.

The default form widget for this field is a NumberInput when localize is False or TextInput otherwise.

FloatField vs. DecimalField

The FloatField class is sometimes mixed up with the DecimalField class. Although they both represent real numbers, they represent those numbers differently. FloatField uses Python’s float type internally, while DecimalField uses Python’s Decimal type. For information on the difference between the two, see Python’s documentation for the decimal module.

A field that is always computed based on other fields in the model. This field is managed and updated by the database itself. Uses the GENERATED ALWAYS SQL syntax.

There are two kinds of generated columns: stored and virtual. A stored generated column is computed when it is written (inserted or updated) and occupies storage as if it were a regular column. A virtual generated column occupies no storage and is computed when it is read. Thus, a virtual generated column is similar to a view and a stored generated column is similar to a materialized view.

An Expression used by the database to automatically set the field value each time the model is changed.

The expressions should be deterministic and only reference fields within the model (in the same database table). Generated fields cannot reference other generated fields. Database backends can impose further restrictions.

A model field instance to define the field’s data type.

Determines if the database column should occupy storage as if it were a real column. If False, the column acts as a virtual column and does not occupy database storage space.

PostgreSQL only supports persisted columns. Oracle only supports virtual columns.

There are many database-specific restrictions on generated fields that Django doesn’t validate and the database may raise an error e.g. PostgreSQL requires functions and operators referenced in a generated column to be marked as IMMUTABLE.

You should always check that expression is supported on your database. Check out MariaDB, MySQL, Oracle, PostgreSQL, or SQLite docs.

GeneratedFields are now automatically refreshed from the database on backends that support it (SQLite, PostgreSQL, and Oracle) and marked as deferred otherwise.

An IPv4 or IPv6 address, in string format (e.g. 192.0.2.30 or 2a02:42fe::4). The default form widget for this field is a TextInput.

The IPv6 address normalization follows RFC 4291 Section 2.2 section 2.2, including using the IPv4 format suggested in paragraph 3 of that section, like ::ffff:192.0.2.0. For example, 2001:0::0:01 would be normalized to 2001::1, and ::ffff:0a0a:0a0a to ::ffff:10.10.10.10. All characters are converted to lowercase.

Limits valid inputs to the specified protocol. Accepted values are 'both' (default), 'IPv4' or 'IPv6'. Matching is case insensitive.

Unpacks IPv4 mapped addresses like ::ffff:192.0.2.1. If this option is enabled that address would be unpacked to 192.0.2.1. Default is disabled. Can only be used when protocol is set to 'both'.

If you allow for blank values, you have to allow for null values since blank values are stored as null.

Inherits all attributes and methods from FileField, but also validates that the uploaded object is a valid image.

In addition to the special attributes that are available for FileField, an ImageField also has height and width attributes.

To facilitate querying on those attributes, ImageField has the following optional arguments:

Name of a model field which is auto-populated with the height of the image each time an image object is set.

Name of a model field which is auto-populated with the width of the image each time an image object is set.

Requires the pillow library.

ImageField instances are created in your database as varchar columns with a default max length of 100 characters. As with other fields, you can change the maximum length using the max_length argument.

The default form widget for this field is a ClearableFileInput.

An integer. Values are only allowed between certain (database-dependent) points. Values from -2147483648 to 2147483647 are compatible in all databases supported by Django.

It uses MinValueValidator and MaxValueValidator to validate the input based on the values that the default database supports.

The default form widget for this field is a NumberInput when localize is False or TextInput otherwise.

A field for storing JSON encoded data. In Python the data is represented in its Python native format: dictionaries, lists, strings, numbers, booleans and None.

JSONField is supported on MariaDB, MySQL, Oracle, PostgreSQL, and SQLite (with the JSON1 extension enabled).

An optional json.JSONEncoder subclass to serialize data types not supported by the standard JSON serializer (e.g. datetime.datetime or UUID). For example, you can use the DjangoJSONEncoder class.

Defaults to json.JSONEncoder.

An optional json.JSONDecoder subclass to deserialize the value retrieved from the database. The value will be in the format chosen by the custom encoder (most often a string). Your deserialization may need to account for the fact that you can’t be certain of the input type. For example, you run the risk of returning a datetime that was actually a string that just happened to be in the same format chosen for datetimes.

Defaults to json.JSONDecoder.

To query JSONField in the database, see Querying JSONField.

If you give the field a default, ensure it’s a callable such as the dict class or a function that returns a fresh object each time. Incorrectly using a mutable object like default={} or default=[] creates a mutable default that is shared between all instances.

Index and Field.db_index both create a B-tree index, which isn’t particularly helpful when querying JSONField. On PostgreSQL only, you can use GinIndex that is better suited.

PostgreSQL has two native JSON based data types: json and jsonb. The main difference between them is how they are stored and how they can be queried. PostgreSQL’s json field is stored as the original string representation of the JSON and must be decoded on the fly when queried based on keys. The jsonb field is stored based on the actual structure of the JSON which allows indexing. The trade-off is a small additional cost on writing to the jsonb field. JSONField uses jsonb.

Oracle Database does not support storing JSON scalar values. Only JSON objects and arrays (represented in Python using dict and list) are supported.

Like a PositiveIntegerField, but only allows values under a certain (database-dependent) point. Values from 0 to 9223372036854775807 are compatible in all databases supported by Django.

Like an IntegerField, but must be either positive or zero (0). Values are only allowed under a certain (database-dependent) point. Values from 0 to 2147483647 are compatible in all databases supported by Django. The value 0 is accepted for backward compatibility reasons.

Like a PositiveIntegerField, but only allows values under a certain (database-dependent) point. Values from 0 to 32767 are compatible in all databases supported by Django.

Slug is a newspaper term. A slug is a short label for something, containing only letters, numbers, underscores or hyphens. They’re generally used in URLs.

Like a CharField, you can specify max_length (read the note about database portability and max_length in that section, too). If max_length is not specified, Django will use a default length of 50.

Implies setting Field.db_index to True.

It is often useful to automatically prepopulate a SlugField based on the value of some other value. You can do this automatically in the admin using prepopulated_fields.

It uses validate_slug or validate_unicode_slug for validation.

If True, the field accepts Unicode letters in addition to ASCII letters. Defaults to False.

Like an AutoField, but only allows values under a certain (database-dependent) limit. Values from 1 to 32767 are compatible in all databases supported by Django.

Like an IntegerField, but only allows values under a certain (database-dependent) point. Values from -32768 to 32767 are compatible in all databases supported by Django.

A large text field. The default form widget for this field is a Textarea.

If you specify a max_length attribute, it will be reflected in the Textarea widget of the auto-generated form field. However it is not enforced at the model or database level. Use a CharField for that.

Optional. The database collation name of the field.

Collation names are not standardized. As such, this will not be portable across multiple database backends.

Oracle does not support collations for a TextField.

A time, represented in Python by a datetime.time instance. Accepts the same auto-population options as DateField.

The default form widget for this field is a TimeInput. The admin adds some JavaScript shortcuts.

A CharField for a URL, validated by URLValidator.

The default form widget for this field is a URLInput.

Like all CharField subclasses, URLField takes the optional max_length argument. If you don’t specify max_length, a default of 200 is used.

A field for storing universally unique identifiers. Uses Python’s UUID class. When used on PostgreSQL and MariaDB 10.7+, this stores in a uuid datatype, otherwise in a char(32).

Universally unique identifiers are a good alternative to AutoField for primary_key. The database will not generate the UUID for you, so it is recommended to use default:

Note that a callable (with the parentheses omitted) is passed to default, not an instance of UUID.

Lookups on PostgreSQL and MariaDB 10.7+

Using iexact, contains, icontains, startswith, istartswith, endswith, or iendswith lookups on PostgreSQL don’t work for values without hyphens, because PostgreSQL and MariaDB 10.7+ store them in a hyphenated uuid datatype type.

Django also defines a set of fields that represent relations.

A many-to-one relationship. Requires two positional arguments: the class to which the model is related and the on_delete option:

The first positional argument can be either a concrete model class or a lazy reference to a model class. Recursive relationships, where a model has a relationship with itself, are also supported.

See ForeignKey.on_delete for details on the second positional argument.

A database index is automatically created on the ForeignKey. You can disable this by setting db_index to False. You may want to avoid the overhead of an index if you are creating a foreign key for consistency rather than joins, or if you will be creating an alternative index like a partial or multiple column index.

Behind the scenes, Django appends "_id" to the field name to create its database column name. In the above example, the database table for the Car model will have a manufacturer_id column. You can change this explicitly by specifying db_column, however, your code should never have to deal with the database column name (unless you write custom SQL). You’ll always deal with the field names of your model object.

ForeignKey accepts other arguments that define the details of how the relation works.

When an object referenced by a ForeignKey is deleted, Django will emulate the behavior of the SQL constraint specified by the on_delete argument. For example, if you have a nullable ForeignKey and you want it to be set null when the referenced object is deleted:

on_delete doesn’t create an SQL constraint in the database. Support for database-level cascade options may be implemented later.

The possible values for on_delete are found in django.db.models:

Cascade deletes. Django emulates the behavior of the SQL constraint ON DELETE CASCADE and also deletes the object containing the ForeignKey.

Model.delete() isn’t called on related models, but the pre_delete and post_delete signals are sent for all deleted objects.

Prevent deletion of the referenced object by raising ProtectedError, a subclass of django.db.IntegrityError.

Prevent deletion of the referenced object by raising RestrictedError (a subclass of django.db.IntegrityError). Unlike PROTECT, deletion of the referenced object is allowed if it also references a different object that is being deleted in the same operation, but via a CASCADE relationship.

Consider this set of models:

Artist can be deleted even if that implies deleting an Album which is referenced by a Song, because Song also references Artist itself through a cascading relationship. For example:

Set the ForeignKey null; this is only possible if null is True.

Set the ForeignKey to its default value; a default for the ForeignKey must be set.

Set the ForeignKey to the value passed to SET(), or if a callable is passed in, the result of calling it. In most cases, passing a callable will be necessary to avoid executing queries at the time your models.py is imported:

Take no action. If your database backend enforces referential integrity, this will cause an IntegrityError unless you manually add an SQL ON DELETE constraint to the database field.

Sets a limit to the available choices for this field when this field is rendered using a ModelForm or the admin (by default, all objects in the queryset are available to choose). Either a dictionary, a Q object, or a callable returning a dictionary or Q object can be used.

causes the corresponding field on the ModelForm to list only User instances that have is_staff=True. This may be helpful in the Django admin.

The callable form can be helpful, for instance, when used in conjunction with the Python datetime module to limit selections by date range. For example:

If limit_choices_to is or returns a Q object, which is useful for complex queries, then it will only have an effect on the choices available in the admin when the field is not listed in raw_id_fields in the ModelAdmin for the model.

If a callable is used for limit_choices_to, it will be invoked every time a new form is instantiated. It may also be invoked when a model is validated, for example by management commands or the admin. The admin constructs querysets to validate its form inputs in various edge cases multiple times, so there is a possibility your callable may be invoked several times.

The name to use for the relation from the related object back to this one. It’s also the default value for related_query_name (the name to use for the reverse filter name from the target model). See the related objects documentation for a full explanation and example. Note that you must set this value when defining relations on abstract models; and when you do so some special syntax is available.

If you’d prefer Django not to create a backwards relation, set related_name to '+' or end it with '+'. For example, this will ensure that the User model won’t have a backwards relation to this model:

The name to use for the reverse filter name from the target model. It defaults to the value of related_name or default_related_name if set, otherwise it defaults to the name of the model:

Like related_name, related_query_name supports app label and class interpolation via some special syntax.

The field on the related object that the relation is to. By default, Django uses the primary key of the related object. If you reference a different field, that field must have unique=True.

Controls whether or not a constraint should be created in the database for this foreign key. The default is True, and that’s almost certainly what you want; setting this to False can be very bad for data integrity. That said, here are some scenarios where you might want to do this:

You have legacy data that is not valid.

You’re sharding your database.

If this is set to False, accessing a related object that doesn’t exist will raise its DoesNotExist exception.

Controls the migration framework’s reaction if this ForeignKey is pointing at a swappable model. If it is True - the default - then if the ForeignKey is pointing at a model which matches the current value of settings.AUTH_USER_MODEL (or another swappable model setting) the relationship will be stored in the migration using a reference to the setting, not to the model directly.

You only want to override this to be False if you are sure your model should always point toward the swapped-in model - for example, if it is a profile model designed specifically for your custom user model.

Setting it to False does not mean you can reference a swappable model even if it is swapped out - False means that the migrations made with this ForeignKey will always reference the exact model you specify (so it will fail hard if the user tries to run with a User model you don’t support, for example).

If in doubt, leave it to its default of True.

A many-to-many relationship. Requires a positional argument: the class to which the model is related, which works exactly the same as it does for ForeignKey, including recursive and lazy relationships.

Related objects can be added, removed, or created with the field’s RelatedManager.

Behind the scenes, Django creates an intermediary join table to represent the many-to-many relationship. By default, this table name is generated using the name of the many-to-many field and the name of the table for the model that contains it. Since some databases don’t support table names above a certain length, these table names will be automatically truncated and a uniqueness hash will be used, e.g. author_books_9cdf. You can manually provide the name of the join table using the db_table option.

ManyToManyField accepts an extra set of arguments – all optional – that control how the relationship functions.

Same as ForeignKey.related_name.

Same as ForeignKey.related_query_name.

Same as ForeignKey.limit_choices_to.

Only used in the definition of ManyToManyFields on self. Consider the following model:

When Django processes this model, it identifies that it has a ManyToManyField on itself, and as a result, it doesn’t add a person_set attribute to the Person class. Instead, the ManyToManyField is assumed to be symmetrical – that is, if I am your friend, then you are my friend.

If you do not want symmetry in many-to-many relationships with self, set symmetrical to False. This will force Django to add the descriptor for the reverse relationship, allowing ManyToManyField relationships to be non-symmetrical.

Django will automatically generate a table to manage many-to-many relationships. However, if you want to manually specify the intermediary table, you can use the through option to specify the Django model that represents the intermediate table that you want to use.

The through model can be specified using either the model class directly or a lazy reference to the model class.

The most common use for this option is when you want to associate extra data with a many-to-many relationship.

Recursive relationships using an intermediary model can’t determine the reverse accessors names, as they would be the same. You need to set a related_name to at least one of them. If you’d prefer Django not to create a backwards relation, set related_name to '+'.

Foreign key order in intermediary models

When defining an asymmetric many-to-many relationship from a model to itself using an intermediary model without defining through_fields, the first foreign key in the intermediary model will be treated as representing the source side of the ManyToManyField, and the second as the target side. For example:

Here, the Manufacturer model defines the many-to-many relationship with clients in its role as a supplier. Therefore, the supplier foreign key (the source) must come before the client foreign key (the target) in the intermediary Supply model.

Specifying through_fields=("supplier", "client") on the ManyToManyField makes the order of foreign keys on the through model irrelevant.

If you don’t specify an explicit through model, there is still an implicit through model class you can use to directly access the table created to hold the association. It has three fields to link the models, a primary key and two foreign keys. There is a unique constraint on the two foreign keys.

If the source and target models differ, the following fields are generated:

id: the primary key of the relation.

<containing_model>_id: the id of the model that declares the ManyToManyField.

<other_model>_id: the id of the model that the ManyToManyField points to.

If the ManyToManyField points from and to the same model, the following fields are generated:

id: the primary key of the relation.

from_<model>_id: the id of the instance which points at the model (i.e. the source instance).

to_<model>_id: the id of the instance to which the relationship points (i.e. the target model instance).

This class can be used to query associated records for a given model instance like a normal model:

Only used when a custom intermediary model is specified. Django will normally determine which fields of the intermediary model to use in order to establish a many-to-many relationship automatically. However, consider the following models:

Membership has two foreign keys to Person (person and inviter), which makes the relationship ambiguous and Django can’t know which one to use. In this case, you must explicitly specify which foreign keys Django should use using through_fields, as in the example above.

through_fields accepts a 2-tuple ('field1', 'field2'), where field1 is the name of the foreign key to the model the ManyToManyField is defined on (group in this case), and field2 the name of the foreign key to the target model (person in this case).

When you have more than one foreign key on an intermediary model to any (or even both) of the models participating in a many-to-many relationship, you must specify through_fields. This also applies to recursive relationships when an intermediary model is used and there are more than two foreign keys to the model, or you want to explicitly specify which two Django should use.

The name of the table to create for storing the many-to-many data. If this is not provided, Django will assume a default name based upon the names of: the table for the model defining the relationship and the name of the field itself.

Controls whether or not constraints should be created in the database for the foreign keys in the intermediary table. The default is True, and that’s almost certainly what you want; setting this to False can be very bad for data integrity. That said, here are some scenarios where you might want to do this:

You have legacy data that is not valid.

You’re sharding your database.

It is an error to pass both db_constraint and through.

Controls the migration framework’s reaction if this ManyToManyField is pointing at a swappable model. If it is True - the default - then if the ManyToManyField is pointing at a model which matches the current value of settings.AUTH_USER_MODEL (or another swappable model setting) the relationship will be stored in the migration using a reference to the setting, not to the model directly.

You only want to override this to be False if you are sure your model should always point toward the swapped-in model - for example, if it is a profile model designed specifically for your custom user model.

If in doubt, leave it to its default of True.

ManyToManyField does not support validators.

null has no effect since there is no way to require a relationship at the database level.

A one-to-one relationship. Conceptually, this is similar to a ForeignKey with unique=True, but the “reverse” side of the relation will directly return a single object.

This is most useful as the primary key of a model which “extends” another model in some way; Multi-table inheritance is implemented by adding an implicit one-to-one relation from the child model to the parent model, for example.

One positional argument is required: the class to which the model will be related. This works exactly the same as it does for ForeignKey, including all the options regarding recursive and lazy relationships.

If you do not specify the related_name argument for the OneToOneField, Django will use the lowercase name of the current model as default value.

With the following example:

your resulting User model will have the following attributes:

A RelatedObjectDoesNotExist exception is raised when accessing the reverse relationship if an entry in the related table doesn’t exist. This is a subclass of the target model’s Model.DoesNotExist exception and can be accessed as an attribute of the reverse accessor. For example, if a user doesn’t have a supervisor designated by MySpecialUser:

Additionally, OneToOneField accepts all of the extra arguments accepted by ForeignKey, plus one extra argument:

When True and used in a model which inherits from another concrete model, indicates that this field should be used as the link back to the parent class, rather than the extra OneToOneField which would normally be implicitly created by subclassing.

See One-to-one relationships for usage examples of OneToOneField.

Lazy relationships allow referencing models by their names (as strings) or creating recursive relationships. Strings can be used as the first argument in any relationship field to reference models lazily. A lazy reference can be either recursive, relative or absolute.

To define a relationship where a model references itself, use "self" as the first argument of the relationship field:

When used in an abstract model, the recursive relationship resolves such that each concrete subclass references itself.

When a relationship needs to be created with a model that has not been defined yet, it can be referenced by its name rather than the model object itself:

Relationships defined this way on abstract models are resolved when the model is subclassed as a concrete model and are not relative to the abstract model’s app_label:

In this example, the Car.manufacturer relationship will resolve to production.Manufacturer, as it points to the concrete model defined within the production/models.py file.

Reusable models with relative references

Relative references allow the creation of reusable abstract models with relationships that can resolve to different implementations of the referenced models in various subclasses across different applications.

Absolute references specify a model using its app_label and class name, allowing for model references across different applications. This type of lazy relationship can also help resolve circular imports.

For example, if the Manufacturer model is defined in another application called thirdpartyapp, it can be referenced as:

Absolute references always point to the same model, even when used in an abstract model.

Field is an abstract class that represents a database table column. Django uses fields to create the database table (db_type()), to map Python types to database (get_prep_value()) and vice-versa (from_db_value()).

A field is thus a fundamental piece in different Django APIs, notably, models and querysets.

In models, a field is instantiated as a class attribute and represents a particular table column, see Models. It has attributes such as null and unique, and methods that Django uses to map the field value to database-specific values.

A Field is a subclass of RegisterLookupMixin and thus both Transform and Lookup can be registered on it to be used in QuerySets (e.g. field_name__exact="foo"). All built-in lookups are registered by default.

All of Django’s built-in fields, such as CharField, are particular implementations of Field. If you need a custom field, you can either subclass any of the built-in fields or write a Field from scratch. In either case, see How to create custom model fields.

A verbose description of the field, e.g. for the django.contrib.admindocs application.

The description can be of the form:

where the arguments are interpolated from the field’s __dict__.

A class implementing the descriptor protocol that is instantiated and assigned to the model instance attribute. The constructor must accept a single argument, the Field instance. Overriding this class attribute allows for customizing the get and set behavior.

To map a Field to a database-specific type, Django exposes several methods:

Returns a string naming this field for backend specific purposes. By default, it returns the class name.

See Emulating built-in field types for usage in custom fields.

Returns the database column data type for the Field, taking into account the connection.

See Custom database types for usage in custom fields.

Returns the database column data type for fields such as ForeignKey and OneToOneField that point to the Field, taking into account the connection.

See Custom database types for usage in custom fields.

There are three main situations where Django needs to interact with the database backend and fields:

when it queries the database (Python value -> database backend value)

when it loads data from the database (database backend value -> Python value)

when it saves to the database (Python value -> database backend value)

When querying, get_db_prep_value() and get_prep_value() are used:

value is the current value of the model’s attribute, and the method should return data in a format that has been prepared for use as a parameter in a query.

See Converting Python objects to query values for usage.

Converts value to a backend-specific value. By default it returns value if prepared=True, and get_prep_value(value) otherwise.

See Converting query values to database values for usage.

When loading data, from_db_value() is used:

Converts a value as returned by the database to a Python object. It is the reverse of get_prep_value().

This method is not used for most built-in fields as the database backend already returns the correct Python type, or the backend itself does the conversion.

expression is the same as self.

See Converting values to Python objects for usage.

For performance reasons, from_db_value is not implemented as a no-op on fields which do not require it (all Django fields). Consequently you may not call super in your definition.

When saving, pre_save() and get_db_prep_save() are used:

Same as the get_db_prep_value(), but called when the field value must be saved to the database. By default returns get_db_prep_value().

Method called prior to get_db_prep_save() to prepare the value before being saved (e.g. for DateField.auto_now).

model_instance is the instance this field belongs to and add is whether the instance is being saved to the database for the first time.

It should return the value of the appropriate attribute from model_instance for this field. The attribute name is in self.attname (this is set up by Field).

See Preprocessing values before saving for usage.

Fields often receive their values as a different type, either from serialization or from forms.

Converts the value into the correct Python object. It acts as the reverse of value_to_string(), and is also called in clean().

See Converting values to Python objects for usage.

Besides saving to the database, the field also needs to know how to serialize its value:

Returns the field’s value for the given model instance.

This method is often used by value_to_string().

Converts obj to a string. Used to serialize the value of the field.

See Converting field data for serialization for usage.

When using model forms, the Field needs to know which form field it should be represented by:

Returns the default django.forms.Field of this field for ModelForm.

If formfield() is overridden to return None, this field is excluded from the ModelForm.

By default, if both form_class and choices_form_class are None, it uses CharField. If the field has choices and choices_form_class isn’t specified, it uses TypedChoiceField.

See Specifying the form field for a model field for usage.

Returns a 4-tuple with enough information to recreate the field:

The name of the field on the model.

The import path of the field (e.g. "django.db.models.IntegerField"). This should be the most portable version, so less specific may be better.

A list of positional arguments.

A dict of keyword arguments.

This method must be added to fields prior to 1.7 to migrate its data using Migrations.

Field implements the lookup registration API. The API can be used to customize which lookups are available for a field class and its instances, and how lookups are fetched from a field.

Every Field instance contains several attributes that allow introspecting its behavior. Use these attributes instead of isinstance checks when you need to write code that depends on a field’s functionality. These attributes can be used together with the Model._meta API to narrow down a search for specific field types. Custom model fields should implement these flags.

Boolean flag that indicates if the field was automatically created, such as the OneToOneField used by model inheritance.

Boolean flag that indicates if the field has a database column associated with it.

Boolean flag that indicates if a field is hidden and should not be returned by Options.get_fields() by default. An example is the reverse field for a ForeignKey with a related_name that starts with '+'.

Boolean flag that indicates if a field contains references to one or more other models for its functionality (e.g. ForeignKey, ManyToManyField, OneToOneField, etc.).

Returns the model on which the field is defined. If a field is defined on a superclass of a model, model will refer to the superclass, not the class of the instance.

These attributes are used to query for the cardinality and other details of a relation. These attribute are present on all fields; however, they will only have boolean values (rather than None) if the field is a relation type (Field.is_relation=True).

Boolean flag that is True if the field has a many-to-many relation; False otherwise. The only field included with Django where this is True is ManyToManyField.

Boolean flag that is True if the field has a many-to-one relation, such as a ForeignKey; False otherwise.

Boolean flag that is True if the field has a one-to-many relation, such as a GenericRelation or the reverse of a ForeignKey; False otherwise.

Boolean flag that is True if the field has a one-to-one relation, such as a OneToOneField; False otherwise.

Points to the model the field relates to. For example, Author in ForeignKey(Author, on_delete=models.CASCADE). The related_model for a GenericForeignKey is always None.

---

## Model index reference¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/indexes/

**Contents:**
- Model index reference¶
- Index options¶
  - expressions¶
  - fields¶
  - name¶
  - db_tablespace¶
  - opclasses¶
  - condition¶
  - include¶

Index classes ease creating database indexes. They can be added using the Meta.indexes option. This document explains the API references of Index which includes the index options.

Referencing built-in indexes

Indexes are defined in django.db.models.indexes, but for convenience they’re imported into django.db.models. The standard convention is to use from django.db import models and refer to the indexes as models.<IndexClass>.

Creates an index (B-Tree) in the database.

Positional argument *expressions allows creating functional indexes on expressions and database functions.

creates an index on the lowercased value of the title field in descending order and the pub_date field in the default ascending order.

creates an index on the result of multiplying fields height and weight and the weight rounded to the nearest integer.

Index.name is required when using *expressions.

Restrictions on Oracle

Oracle requires functions referenced in an index to be marked as DETERMINISTIC. Django doesn’t validate this but Oracle will error. This means that functions such as Random() aren’t accepted.

Restrictions on PostgreSQL

PostgreSQL requires functions and operators referenced in an index to be marked as IMMUTABLE. Django doesn’t validate this but PostgreSQL will error. This means that functions such as Concat() aren’t accepted.

Functional indexes are ignored with MySQL < 8.0.13 and MariaDB as neither supports them.

A list or tuple of the name of the fields on which the index is desired.

By default, indexes are created with an ascending order for each column. To define an index with a descending order for a column, add a hyphen before the field’s name.

For example Index(fields=['headline', '-pub_date']) would create SQL with (headline, pub_date DESC).

Index ordering isn’t supported on MariaDB < 10.8. In that case, a descending index is created as a normal index.

The name of the index. If name isn’t provided Django will auto-generate a name. For compatibility with different databases, index names cannot be longer than 30 characters and shouldn’t start with a number (0-9) or underscore (_).

Partial indexes in abstract base classes

You must always specify a unique name for an index. As such, you cannot normally specify a partial index on an abstract base class, since the Meta.indexes option is inherited by subclasses, with exactly the same values for the attributes (including name) each time. To work around name collisions, part of the name may contain '%(app_label)s' and '%(class)s', which are replaced, respectively, by the lowercased app label and class name of the concrete model. For example Index(fields=['title'], name='%(app_label)s_%(class)s_title_index').

The name of the database tablespace to use for this index. For single field indexes, if db_tablespace isn’t provided, the index is created in the db_tablespace of the field.

If Field.db_tablespace isn’t specified (or if the index uses multiple fields), the index is created in tablespace specified in the db_tablespace option inside the model’s class Meta. If neither of those tablespaces are set, the index is created in the same tablespace as the table.

For a list of PostgreSQL-specific indexes, see django.contrib.postgres.indexes.

The names of the PostgreSQL operator classes to use for this index. If you require a custom operator class, you must provide one for each field in the index.

For example, GinIndex(name='json_index', fields=['jsonfield'], opclasses=['jsonb_path_ops']) creates a gin index on jsonfield using jsonb_path_ops.

opclasses are ignored for databases besides PostgreSQL.

Index.name is required when using opclasses.

If the table is very large and your queries mostly target a subset of rows, it may be useful to restrict an index to that subset. Specify a condition as a Q. For example, condition=Q(pages__gt=400) indexes records with more than 400 pages.

Index.name is required when using condition.

Restrictions on PostgreSQL

PostgreSQL requires functions referenced in the condition to be marked as IMMUTABLE. Django doesn’t validate this but PostgreSQL will error. This means that functions such as Date functions and Concat aren’t accepted. If you store dates in DateTimeField, comparison to datetime objects may require the tzinfo argument to be provided because otherwise the comparison could result in a mutable function due to the casting Django does for lookups.

Restrictions on SQLite

SQLite imposes restrictions on how a partial index can be constructed.

Oracle does not support partial indexes. Instead, partial indexes can be emulated by using functional indexes together with Case expressions.

The condition argument is ignored with MySQL and MariaDB as neither supports conditional indexes.

A list or tuple of the names of the fields to be included in the covering index as non-key columns. This allows index-only scans to be used for queries that select only included fields (include) and filter only by indexed fields (fields).

will allow filtering on headline, also selecting pub_date, while fetching data only from the index.

Using include will produce a smaller index than using a multiple column index but with the drawback that non-key columns can not be used for sorting or filtering.

include is ignored for databases besides PostgreSQL.

Index.name is required when using include.

See the PostgreSQL documentation for more details about covering indexes.

Restrictions on PostgreSQL

PostgreSQL supports covering B-Tree and GiST indexes. PostgreSQL 14+ also supports covering SP-GiST indexes.

---

## Model instance reference¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/instances/

**Contents:**
- Model instance reference¶
- Creating objects¶
  - Customizing model loading¶
- Refreshing objects from database¶
- Validating objects¶
- Saving objects¶
  - Auto-incrementing primary keys¶
    - The pk property¶
    - Explicitly specifying auto-primary-key values¶
  - What happens when you save?¶

This document describes the details of the Model API. It builds on the material presented in the model and database query guides, so you’ll probably want to read and understand those documents before reading this one.

Throughout this reference we’ll use the example blog models presented in the database query guide.

To create a new instance of a model, instantiate it like any other Python class:

The keyword arguments are the names of the fields you’ve defined on your model. Note that instantiating a model in no way touches your database; for that, you need to save().

You may be tempted to customize the model by overriding the __init__ method. If you do so, however, take care not to change the calling signature as any change may prevent the model instance from being saved. Additionally, referring to model fields within __init__ may potentially result in infinite recursion errors in some circumstances. Rather than overriding __init__, try using one of these approaches:

Add a classmethod on the model class:

Add a method on a custom manager (usually preferred):

The from_db() method can be used to customize model instance creation when loading from the database.

The db argument contains the database alias for the database the model is loaded from, field_names contains the names of all loaded fields, and values contains the loaded values for each field in field_names. The field_names are in the same order as the values. If all of the model’s fields are present, then values are guaranteed to be in the order __init__() expects them. That is, the instance can be created by cls(*values). If any fields are deferred, they won’t appear in field_names. In that case, assign a value of django.db.models.DEFERRED to each of the missing fields.

In addition to creating the new model, the from_db() method must set the adding and db flags in the new instance’s _state attribute.

Below is an example showing how to record the initial values of fields that are loaded from the database:

The example above shows a full from_db() implementation to clarify how that is done. In this case it would be possible to use a super() call in the from_db() method.

If you delete a field from a model instance, accessing it again reloads the value from the database:

Asynchronous version: arefresh_from_db()

If you need to reload a model’s values from the database, you can use the refresh_from_db() method. When this method is called without arguments the following is done:

All non-deferred fields of the model are updated to the values currently present in the database.

Any cached relations are cleared from the reloaded instance.

Only fields of the model are reloaded from the database. Other database-dependent values such as annotations aren’t reloaded. Any @cached_property attributes aren’t cleared either.

The reloading happens from the database the instance was loaded from, or from the default database if the instance wasn’t loaded from the database. The using argument can be used to force the database used for reloading.

It is possible to force the set of fields to be loaded by using the fields argument.

For example, to test that an update() call resulted in the expected update, you could write a test similar to this:

Note that when deferred fields are accessed, the loading of the deferred field’s value happens through this method. Thus it is possible to customize the way deferred loading happens. The example below shows how one can reload all of the instance’s fields when a deferred field is reloaded:

The from_queryset argument allows using a different queryset than the one created from _base_manager. It gives you more control over how the model is reloaded. For example, when your model uses soft deletion you can make refresh_from_db() to take this into account:

You can cache related objects that otherwise would be cleared from the reloaded instance:

You can lock the row until the end of transaction before reloading a model’s values:

A helper method that returns a set containing the attribute names of all those fields that are currently deferred for this model.

There are four steps involved in validating a model:

Validate the model fields - Model.clean_fields()

Validate the model as a whole - Model.clean()

Validate the field uniqueness - Model.validate_unique()

Validate the constraints - Model.validate_constraints()

All four steps are performed when you call a model’s full_clean() method.

When you use a ModelForm, the call to is_valid() will perform these validation steps for all the fields that are included on the form. See the ModelForm documentation for more information. You should only need to call a model’s full_clean() method if you plan to handle validation errors yourself, or if you have excluded fields from the ModelForm that require validation.

This method calls Model.clean_fields(), Model.clean(), Model.validate_unique() (if validate_unique is True), and Model.validate_constraints() (if validate_constraints is True) in that order and raises a ValidationError that has a message_dict attribute containing errors from all four stages.

The optional exclude argument can be used to provide a set of field names that can be excluded from validation and cleaning. ModelForm uses this argument to exclude fields that aren’t present on your form from being validated since any errors raised could not be corrected by the user.

Note that full_clean() will not be called automatically when you call your model’s save() method. You’ll need to call it manually when you want to run one-step model validation for your own manually created models. For example:

The first step full_clean() performs is to clean each individual field.

This method will validate all fields on your model. The optional exclude argument lets you provide a set of field names to exclude from validation. It will raise a ValidationError if any fields fail validation.

The second step full_clean() performs is to call Model.clean(). This method should be overridden to perform custom validation on your model.

This method should be used to provide custom model validation, and to modify attributes on your model if desired. For instance, you could use it to automatically provide a value for a field, or to do validation that requires access to more than a single field:

Note, however, that like Model.full_clean(), a model’s clean() method is not invoked when you call your model’s save() method.

In the above example, the ValidationError exception raised by Model.clean() was instantiated with a string, so it will be stored in a special error dictionary key, NON_FIELD_ERRORS. This key is used for errors that are tied to the entire model instead of to a specific field:

To assign exceptions to a specific field, instantiate the ValidationError with a dictionary, where the keys are the field names. We could update the previous example to assign the error to the pub_date field:

If you detect errors in multiple fields during Model.clean(), you can also pass a dictionary mapping field names to errors:

Then, full_clean() will check unique constraints on your model.

How to raise field-specific validation errors if those fields don’t appear in a ModelForm

You can’t raise validation errors in Model.clean() for fields that don’t appear in a model form (a form may limit its fields using Meta.fields or Meta.exclude). Doing so will raise a ValueError because the validation error won’t be able to be associated with the excluded field.

To work around this dilemma, instead override Model.clean_fields() as it receives the list of fields that are excluded from validation. For example:

This method is similar to clean_fields(), but validates uniqueness constraints defined via Field.unique, Field.unique_for_date, Field.unique_for_month, Field.unique_for_year, or Meta.unique_together on your model instead of individual field values. The optional exclude argument allows you to provide a set of field names to exclude from validation. It will raise a ValidationError if any fields fail validation.

UniqueConstraints defined in the Meta.constraints are validated by Model.validate_constraints().

Note that if you provide an exclude argument to validate_unique(), any unique_together constraint involving one of the fields you provided will not be checked.

Finally, full_clean() will check any other constraints on your model.

This method validates all constraints defined in Meta.constraints. The optional exclude argument allows you to provide a set of field names to exclude from validation. It will raise a ValidationError if any constraints fail validation.

To save an object back to the database, call save():

Asynchronous version: asave()

For details on using the force_insert and force_update arguments, see Forcing an INSERT or UPDATE. Details about the update_fields argument can be found in the Specifying which fields to save section.

If you want customized saving behavior, you can override this save() method. See Overriding predefined model methods for more details.

The model save process also has some subtleties; see the sections below.

If a model has an AutoField — an auto-incrementing primary key — then that auto-incremented value will be calculated and saved as an attribute on your object the first time you call save():

There’s no way to tell what the value of an ID will be before you call save(), because that value is calculated by your database, not by Django.

For convenience, each model has an AutoField named id by default unless you explicitly specify primary_key=True on a field in your model. See the documentation for AutoField for more details.

Regardless of whether you define a primary key field yourself, or let Django supply one for you, each model will have a property called pk. It behaves like a normal attribute on the model, but is actually an alias for whichever field or fields compose the primary key for the model. You can read and set this value, just as you would for any other attribute, and it will update the correct fields in the model.

Support for the primary key to be composed of multiple fields was added via CompositePrimaryKey.

If a model has an AutoField but you want to define a new object’s ID explicitly when saving, define it explicitly before saving, rather than relying on the auto-assignment of the ID:

If you assign auto-primary-key values manually, make sure not to use an already-existing primary-key value! If you create a new object with an explicit primary-key value that already exists in the database, Django will assume you’re changing the existing record rather than creating a new one.

Given the above 'Cheddar Talk' blog example, this example would override the previous record in the database:

See How Django knows to UPDATE vs. INSERT, below, for the reason this happens.

Explicitly specifying auto-primary-key values is mostly useful for bulk-saving objects, when you’re confident you won’t have primary-key collision.

If you’re using PostgreSQL, the sequence associated with the primary key might need to be updated; see Manually-specifying values of auto-incrementing primary keys.

When you save an object, Django performs the following steps:

Emit a pre-save signal. The pre_save signal is sent, allowing any functions listening for that signal to do something.

Preprocess the data. Each field’s pre_save() method is called to perform any automated data modification that’s needed. For example, the date/time fields override pre_save() to implement auto_now_add and auto_now.

Prepare the data for the database. Each field’s get_db_prep_save() method is asked to provide its current value in a data type that can be written to the database.

Most fields don’t require data preparation. Simple data types, such as integers and strings, are ‘ready to write’ as a Python object. However, more complex data types often require some modification.

For example, DateField fields use a Python datetime object to store data. Databases don’t store datetime objects, so the field value must be converted into an ISO-compliant date string for insertion into the database.

Insert the data into the database. The preprocessed, prepared data is composed into an SQL statement for insertion into the database.

Emit a post-save signal. The post_save signal is sent, allowing any functions listening for that signal to do something.

You may have noticed Django database objects use the same save() method for creating and changing objects. Django abstracts the need to use INSERT or UPDATE SQL statements. Specifically, when you call save() and the object’s primary key attribute does not define a default or db_default, Django follows this algorithm:

If the object’s primary key attribute is set to anything except None, Django executes an UPDATE.

If the object’s primary key attribute is not set or if the UPDATE didn’t update anything (e.g. if primary key is set to a value that doesn’t exist in the database), Django executes an INSERT.

If the object’s primary key attribute defines a default or db_default then Django executes an UPDATE if it is an existing model instance and primary key is set to a value that exists in the database. Otherwise, Django executes an INSERT.

The one gotcha here is that you should be careful not to specify a primary-key value explicitly when saving new objects, if you cannot guarantee the primary-key value is unused. For more on this nuance, see Explicitly specifying auto-primary-key values above and Forcing an INSERT or UPDATE below.

In Django 1.5 and earlier, Django did a SELECT when the primary key attribute was set. If the SELECT found a row, then Django did an UPDATE, otherwise it did an INSERT. The old algorithm results in one more query in the UPDATE case. There are some rare cases where the database doesn’t report that a row was updated even if the database contains a row for the object’s primary key value. An example is the PostgreSQL ON UPDATE trigger which returns NULL. In such cases it is possible to revert to the old algorithm by setting the select_on_save option to True.

In some rare circumstances, it’s necessary to be able to force the save() method to perform an SQL INSERT and not fall back to doing an UPDATE. Or vice-versa: update, if possible, but not insert a new row. In these cases you can pass the force_insert=True or force_update=True parameters to the save() method. Passing both parameters is an error: you cannot both insert and update at the same time!

When using multi-table inheritance, it’s also possible to provide a tuple of parent classes to force_insert in order to force INSERT statements for each base. For example:

You can pass force_insert=(models.Model,) to force an INSERT statement for all parents. By default, force_insert=True only forces the insertion of a new row for the current model.

When a forced update does not affect any rows a NotUpdated exception is raised. On previous versions a generic django.db.DatabaseError was raised.

It should be very rare that you’ll need to use these parameters. Django will almost always do the right thing and trying to override that will lead to errors that are difficult to track down. This feature is for advanced use only.

Using update_fields will force an update similarly to force_update.

Sometimes you’ll need to perform a simple arithmetic task on a field, such as incrementing or decrementing the current value. One way of achieving this is doing the arithmetic in Python like:

If the old number_sold value retrieved from the database was 10, then the value of 11 will be written back to the database.

The process can be made robust, avoiding a race condition, as well as slightly faster by expressing the update relative to the original field value, rather than as an explicit assignment of a new value. Django provides F expressions for performing this kind of relative update. Using F expressions, the previous example is expressed as:

For more details, see the documentation on F expressions and their use in update queries.

If save() is passed a list of field names in keyword argument update_fields, only the fields named in that list will be updated. This may be desirable if you want to update just one or a few fields on an object. There will be a slight performance benefit from preventing all of the model fields from being updated in the database. For example:

The update_fields argument can be any iterable containing strings. An empty update_fields iterable will skip the save. A value of None will perform an update on all fields.

Specifying update_fields will force an update.

When saving a model fetched through deferred model loading (only() or defer()) only the fields loaded from the DB will get updated. In effect there is an automatic update_fields in this case. If you assign or change any deferred field value, the field will be added to the updated fields.

Field.pre_save() and update_fields

If update_fields is passed in, only the pre_save() methods of the update_fields are called. For example, this means that date/time fields with auto_now=True will not be updated unless they are included in the update_fields.

Asynchronous version: adelete()

Issues an SQL DELETE for the object. This only deletes the object in the database; the Python instance will still exist and will still have data in its fields, except for the primary key set to None. This method returns the number of objects deleted and a dictionary with the number of deletions per object type.

For more details, including how to delete objects in bulk, see Deleting objects.

If you want customized deletion behavior, you can override the delete() method. See Overriding predefined model methods for more details.

Sometimes with multi-table inheritance you may want to delete only a child model’s data. Specifying keep_parents=True will keep the parent model’s data.

When you pickle a model, its current state is pickled. When you unpickle it, it’ll contain the model instance at the moment it was pickled, rather than the data that’s currently in the database.

You can’t share pickles between versions

Pickles of models are only valid for the version of Django that was used to generate them. If you generate a pickle using Django version N, there is no guarantee that pickle will be readable with Django version N+1. Pickles should not be used as part of a long-term archival strategy.

Since pickle compatibility errors can be difficult to diagnose, such as silently corrupted objects, a RuntimeWarning is raised when you try to unpickle a model in a Django version that is different than the one in which it was pickled.

A few object methods have special purposes.

The __str__() method is called whenever you call str() on an object. Django uses str(obj) in a number of places. Most notably, to display an object in the Django admin site and as the value inserted into a template when it displays an object. Thus, you should always return a nice, human-readable representation of the model from the __str__() method.

The equality method is defined such that instances with the same primary key value and the same concrete class are considered equal, except that instances with a primary key value of None aren’t equal to anything except themselves. For proxy models, concrete class is defined as the model’s first non-proxy parent; for all other models it’s simply the model’s class.

The __hash__() method is based on the instance’s primary key value. It is effectively hash(obj.pk). If the instance doesn’t have a primary key value then a TypeError will be raised (otherwise the __hash__() method would return different values before and after the instance is saved, but changing the __hash__() value of an instance is forbidden in Python.

Define a get_absolute_url() method to tell Django how to calculate the canonical URL for an object. To callers, this method should appear to return a string that can be used to refer to the object over HTTP.

While this code is correct and simple, it may not be the most portable way to to write this kind of method. The reverse() function is usually the best approach.

One place Django uses get_absolute_url() is in the admin app. If an object defines this method, the object-editing page will have a “View on site” link that will jump you directly to the object’s public view, as given by get_absolute_url().

Similarly, a couple of other bits of Django, such as the syndication feed framework, use get_absolute_url() when it is defined. If it makes sense for your model’s instances to each have a unique URL, you should define get_absolute_url().

You should avoid building the URL from unvalidated user input, in order to reduce possibilities of link or redirect poisoning:

If self.name is '/example.com' this returns '//example.com/' which, in turn, is a valid schema relative URL but not the expected '/%2Fexample.com/'.

It’s good practice to use get_absolute_url() in templates, instead of hardcoding your objects’ URLs. For example, this template code is bad:

This template code is much better:

The logic here is that if you change the URL structure of your objects, even for something small like correcting a spelling error, you don’t want to have to track down every place that the URL might be created. Specify it once, in get_absolute_url() and have all your other code call that one place.

The string you return from get_absolute_url() must contain only ASCII characters (required by the URI specification, RFC 3986 Section 2) and be URL-encoded, if necessary.

Code and templates calling get_absolute_url() should be able to use the result directly without any further processing. You may wish to use the django.utils.encoding.iri_to_uri() function to help with this if you are using strings containing characters outside the ASCII range.

In addition to save(), delete(), a model object might have some of the following methods:

For every field that has choices set, the object will have a get_FOO_display() method, where FOO is the name of the field. This method returns the “human-readable” value of the field.

For every DateField and DateTimeField that does not have null=True, the object will have get_next_by_FOO() and get_previous_by_FOO() methods, where FOO is the name of the field. This returns the next and previous object with respect to the date field, raising a DoesNotExist exception when appropriate.

Both of these methods will perform their queries using the default manager for the model. If you need to emulate filtering used by a custom manager, or want to perform one-off custom filtering, both methods also accept optional keyword arguments, which should be in the format described in Field lookups.

Note that in the case of identical date values, these methods will use the primary key as a tie-breaker. This guarantees that no records are skipped or duplicated. That also means you cannot use those methods on unsaved objects.

Overriding extra instance methods

In most cases overriding or inheriting get_FOO_display(), get_next_by_FOO(), and get_previous_by_FOO() should work as expected. Since they are added by the metaclass however, it is not practical to account for all possible inheritance structures. In more complex cases you should override Field.contribute_to_class() to set the methods you need.

The _state attribute refers to a ModelState object that tracks the lifecycle of the model instance.

The ModelState object has two attributes: adding, a flag which is True if the model has not been saved to the database yet, and db, a string referring to the database alias the instance was loaded from or saved to.

Newly instantiated instances have adding=True and db=None, since they are yet to be saved. Instances fetched from a QuerySet will have adding=False and db set to the alias of the associated database.

The _is_pk_set() method returns whether the model instance’s pk is set. It abstracts the model’s primary key definition, ensuring consistent behavior regardless of the specific pk configuration.

---

## Model Meta options¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/options/

**Contents:**
- Model Meta options¶
- Available Meta options¶
  - abstract¶
  - app_label¶
  - base_manager_name¶
  - db_table¶
    - Table names¶
  - db_table_comment¶
  - db_tablespace¶
  - default_manager_name¶

This document explains all the possible metadata options that you can give your model in its internal class Meta.

If abstract = True, this model will be an abstract base class.

If a model is defined outside of an application in INSTALLED_APPS, it must declare which app it belongs to:

If you want to represent a model with the format app_label.object_name or app_label.model_name you can use model._meta.label or model._meta.label_lower respectively.

The attribute name of the manager, for example, 'objects', to use for the model’s _base_manager.

The name of the database table to use for the model:

To save you time, Django automatically derives the name of the database table from the name of your model class and the app that contains it. A model’s database table name is constructed by joining the model’s “app label” – the name you used in manage.py startapp – to the model’s class name, with an underscore between them.

For example, if you have an app bookstore (as created by manage.py startapp bookstore), a model defined as class Book will have a database table named bookstore_book.

To override the database table name, use the db_table parameter in class Meta.

If your database table name is an SQL reserved word, or contains characters that aren’t allowed in Python variable names – notably, the hyphen – that’s OK. Django quotes column and table names behind the scenes.

Use lowercase table names for MariaDB and MySQL

It is strongly advised that you use lowercase table names when you override the table name via db_table, particularly if you are using the MySQL backend. See the MySQL notes for more details.

Table name quoting for Oracle

In order to meet the 30-char limitation Oracle has on table names, and match the usual conventions for Oracle databases, Django may shorten table names and turn them all-uppercase. To prevent such transformations, use a quoted name as the value for db_table:

Such quoted names can also be used with Django’s other supported database backends; except for Oracle, however, the quotes have no effect. See the Oracle notes for more details.

The comment on the database table to use for this model. It is useful for documenting database tables for individuals with direct database access who may not be looking at your Django code. For example:

The name of the database tablespace to use for this model. The default is the project’s DEFAULT_TABLESPACE setting, if set. If the backend doesn’t support tablespaces, this option is ignored.

The name of the manager to use for the model’s _default_manager.

The name that will be used by default for the relation from a related object back to this one. The default is <model_name>_set.

This option also sets related_query_name.

As the reverse name for a field should be unique, be careful if you intend to subclass your model. To work around name collisions, part of the name should contain '%(app_label)s' and '%(model_name)s', which are replaced respectively by the name of the application the model is in, and the name of the model, both lowercased. See the paragraph on related names for abstract models.

The name of a field or a list of field names in the model, typically DateField, DateTimeField, or IntegerField. This specifies the default field(s) to use in your model Manager’s latest() and earliest() methods.

See the latest() docs for more.

Defaults to True, meaning Django will create the appropriate database tables in migrate or as part of migrations and remove them as part of a flush management command. That is, Django manages the database tables’ lifecycles.

If False, no database table creation, modification, or deletion operations will be performed for this model. This is useful if the model represents an existing table or a database view that has been created by some other means. This is the only difference when managed=False. All other aspects of model handling are exactly the same as normal. This includes

Adding an automatic primary key field to the model if you don’t declare it. To avoid confusion for later code readers, it’s recommended to specify all the columns from the database table you are modeling when using unmanaged models.

If a model with managed=False contains a ManyToManyField that points to another unmanaged model, then the intermediate table for the many-to-many join will also not be created. However, the intermediary table between one managed and one unmanaged model will be created.

If you need to change this default behavior, create the intermediary table as an explicit model (with managed set as needed) and use the ManyToManyField.through attribute to make the relation use your custom model.

For tests involving models with managed=False, it’s up to you to ensure the correct tables are created as part of the test setup.

If you’re interested in changing the Python-level behavior of a model class, you could use managed=False and create a copy of an existing model. However, there’s a better approach for that situation: Proxy models.

Makes this object orderable with respect to the given field, usually a ForeignKey. This can be used to make related objects orderable with respect to a parent object. For example, if an Answer relates to a Question object, and a question has more than one answer, and the order of answers matters, you’d do this:

When order_with_respect_to is set, two additional methods are provided to retrieve and to set the order of the related objects: get_RELATED_order() and set_RELATED_order(), where RELATED is the lowercased model name. For example, assuming that a Question object has multiple related Answer objects, the list returned contains the primary keys of the related Answer objects:

The order of a Question object’s related Answer objects can be set by passing in a list of Answer primary keys:

The related objects also get two methods, get_next_in_order() and get_previous_in_order(), which can be used to access those objects in their proper order. Assuming the Answer objects are ordered by id:

order_with_respect_to implicitly sets the ordering option

Internally, order_with_respect_to adds an additional field/database column named _order and sets the model’s ordering option to this field. Consequently, order_with_respect_to and ordering cannot be used together, and the ordering added by order_with_respect_to will apply whenever you obtain a list of objects of this model.

Changing order_with_respect_to

Because order_with_respect_to adds a new database column, be sure to make and apply the appropriate migrations if you add or change order_with_respect_to after your initial migrate.

The default ordering for the object, for use when obtaining lists of objects:

This is a tuple or list of strings and/or query expressions. Each string is a field name with an optional “-” prefix, which indicates descending order. Fields without a leading “-” will be ordered ascending. Use the string “?” to order randomly.

For example, to order by a pub_date field ascending, use this:

To order by pub_date descending, use this:

To order by pub_date descending, then by author ascending, use this:

You can also use query expressions. To order by author ascending and make null values sort last, use this:

Default ordering and GROUP BY

In GROUP BY queries (for example, those using values() and annotate()), the default ordering is not applied.

Ordering is not a free operation. Each field you add to the ordering incurs a cost to your database. Each foreign key you add will implicitly include all of its default orderings as well.

If a query doesn’t have an ordering specified, results are returned from the database in an unspecified order. A particular ordering is guaranteed only when ordering by a set of fields that uniquely identify each object in the results. For example, if a name field isn’t unique, ordering by it won’t guarantee objects with the same name always appear in the same order.

Extra permissions to enter into the permissions table when creating this object. Add, change, delete, and view permissions are automatically created for each model. This example specifies an extra permission, can_deliver_pizzas:

This is a list or tuple of 2-tuples in the format (permission_code, human_readable_permission_name).

Defaults to ('add', 'change', 'delete', 'view'). You may customize this list, for example, by setting this to an empty list if your app doesn’t require any of the default permissions. It must be specified on the model before the model is created by migrate in order to prevent any omitted permissions from being created.

If proxy = True, a model which subclasses another model will be treated as a proxy model.

List of database features that the current connection should have so that the model is considered during the migration phase. For example, if you set this list to ['gis_enabled'], the model will only be synchronized on GIS-enabled databases. It’s also useful to skip some models when testing with several database backends. Avoid relations between models that may or may not be created as the ORM doesn’t handle this.

Name of a supported database vendor that this model is specific to. Current built-in vendor names are: sqlite, postgresql, mysql, oracle. If this attribute is not empty and the current connection vendor doesn’t match it, the model will not be synchronized.

Determines if Django will use the pre-1.6 django.db.models.Model.save() algorithm. The old algorithm uses SELECT to determine if there is an existing row to be updated. The new algorithm tries an UPDATE directly. In some rare cases the UPDATE of an existing row isn’t visible to Django. An example is the PostgreSQL ON UPDATE trigger which returns NULL. In such cases the new algorithm will end up doing an INSERT even when a row exists in the database.

Usually there is no need to set this attribute. The default is False.

See django.db.models.Model.save() for more about the old and new saving algorithm.

A list of indexes that you want to define on the model:

Use UniqueConstraint with the constraints option instead.

UniqueConstraint provides more functionality than unique_together. unique_together may be deprecated in the future.

Sets of field names that, taken together, must be unique:

This is a list of lists that must be unique when considered together. It’s used in the Django admin and is enforced at the database level (i.e., the appropriate UNIQUE statements are included in the CREATE TABLE statement).

For convenience, unique_together can be a single list when dealing with a single set of fields:

A ManyToManyField cannot be included in unique_together. (It’s not clear what that would even mean!) If you need to validate uniqueness related to a ManyToManyField, try using a signal or an explicit through model.

The ValidationError raised during model validation when the constraint is violated has the unique_together error code.

A list of constraints that you want to define on the model:

A human-readable name for the object, singular:

If this isn’t given, Django will use a munged version of the class name: CamelCase becomes camel case.

The plural name for the object:

If this isn’t given, Django will use verbose_name + "s".

Representation of the object, returns app_label.object_name, e.g. 'polls.Question'.

Representation of the model, returns app_label.model_name, e.g. 'polls.question'.

---

## QuerySet API reference¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/querysets/

**Contents:**
- QuerySet API reference¶
- When QuerySets are evaluated¶
  - Pickling QuerySets¶
- QuerySet API¶
  - Methods that return new QuerySets¶
    - filter()¶
    - exclude()¶
    - annotate()¶
    - alias()¶
    - order_by()¶

This document describes the details of the QuerySet API. It builds on the material presented in the model and database query guides, so you’ll probably want to read and understand those documents before reading this one.

Throughout this reference we’ll use the example blog models presented in the database query guide.

Internally, a QuerySet can be constructed, filtered, sliced, and generally passed around without actually hitting the database. No database activity actually occurs until you do something to evaluate the queryset.

You can evaluate a QuerySet in the following ways:

Iteration. A QuerySet is iterable, and it executes its database query the first time you iterate over it. For example, this will print the headline of all entries in the database:

Note: Don’t use this if all you want to do is determine if at least one result exists. It’s more efficient to use exists().

Asynchronous iteration. A QuerySet can also be iterated over using async for:

Both synchronous and asynchronous iterators of QuerySets share the same underlying cache.

Slicing. As explained in Limiting QuerySets, a QuerySet can be sliced, using Python’s array-slicing syntax. Slicing an unevaluated QuerySet usually returns another unevaluated QuerySet, but Django will execute the database query if you use the “step” parameter of slice syntax, and will return a list. Slicing a QuerySet that has been evaluated also returns a list.

Also note that even though slicing an unevaluated QuerySet returns another unevaluated QuerySet, modifying it further (e.g., adding more filters, or modifying ordering) is not allowed, since that does not translate well into SQL and it would not have a clear meaning either.

Pickling/Caching. See the following section for details of what is involved when pickling QuerySets. The important thing for the purposes of this section is that the results are read from the database.

repr(). A QuerySet is evaluated when you call repr() on it. This is for convenience in the Python interactive interpreter, so you can immediately see your results when using the API interactively.

len(). A QuerySet is evaluated when you call len() on it. This, as you might expect, returns the length of the result list.

Note: If you only need to determine the number of records in the set (and don’t need the actual objects), it’s much more efficient to handle a count at the database level using SQL’s SELECT COUNT(*). Django provides a count() method for precisely this reason.

list(). Force evaluation of a QuerySet by calling list() on it. For example:

bool(). Testing a QuerySet in a boolean context, such as using bool(), or, and or an if statement, will cause the query to be executed. If there is at least one result, the QuerySet is True, otherwise False. For example:

Note: If you only want to determine if at least one result exists (and don’t need the actual objects), it’s more efficient to use exists().

If you pickle a QuerySet, this will force all the results to be loaded into memory prior to pickling. Pickling is usually used as a precursor to caching and when the cached queryset is reloaded, you want the results to already be present and ready for use (reading from the database can take some time, defeating the purpose of caching). This means that when you unpickle a QuerySet, it contains the results at the moment it was pickled, rather than the results that are currently in the database.

If you only want to pickle the necessary information to recreate the QuerySet from the database at a later time, pickle the query attribute of the QuerySet. You can then recreate the original QuerySet (without any results loaded) using some code like this:

The query attribute is an opaque object. It represents the internals of the query construction and is not part of the public API. However, it is safe (and fully supported) to pickle and unpickle the attribute’s contents as described here.

Restrictions on QuerySet.values_list()

If you recreate QuerySet.values_list() using the pickled query attribute, it will be converted to QuerySet.values():

You can’t share pickles between versions

Pickles of QuerySet objects are only valid for the version of Django that was used to generate them. If you generate a pickle using Django version N, there is no guarantee that pickle will be readable with Django version N+1. Pickles should not be used as part of a long-term archival strategy.

Since pickle compatibility errors can be difficult to diagnose, such as silently corrupted objects, a RuntimeWarning is raised when you try to unpickle a queryset in a Django version that is different than the one in which it was pickled.

Here’s the formal declaration of a QuerySet:

Usually when you’ll interact with a QuerySet you’ll use it by chaining filters. To make this work, most QuerySet methods return new querysets. These methods are covered in detail later in this section.

The QuerySet class has the following public attributes you can use for introspection:

True if the QuerySet is ordered — i.e. has an order_by() clause or a default ordering on the model. False otherwise.

The database that will be used if this query is executed now.

The query parameter to QuerySet exists so that specialized query subclasses can reconstruct internal query state. The value of the parameter is an opaque representation of that query state and is not part of a public API.

Django provides a range of QuerySet refinement methods that modify either the types of results returned by the QuerySet or the way its SQL query is executed.

These methods do not run database queries, therefore they are safe to run in asynchronous code, and do not have separate asynchronous versions.

Returns a new QuerySet containing objects that match the given lookup parameters.

The lookup parameters (**kwargs) should be in the format described in Field lookups below. Multiple parameters are joined via AND in the underlying SQL statement.

If you need to execute more complex queries (for example, queries with OR statements), you can use Q objects (*args).

Returns a new QuerySet containing objects that do not match the given lookup parameters.

The lookup parameters (**kwargs) should be in the format described in Field lookups below. Multiple parameters are joined via AND in the underlying SQL statement, and the whole thing is enclosed in a NOT().

This example excludes all entries whose pub_date is later than 2005-1-3 AND whose headline is “Hello”:

In SQL terms, that evaluates to:

This example excludes all entries whose pub_date is later than 2005-1-3 OR whose headline is “Hello”:

In SQL terms, that evaluates to:

Note the second example is more restrictive.

If you need to execute more complex queries (for example, queries with OR statements), you can use Q objects (*args).

Annotates each object in the QuerySet with the provided list of query expressions or Q objects. Each object can be annotated with:

a simple value, via Value();

a reference to a field on the model (or any related models), via F();

a boolean, via Q(); or

a result from an aggregate expression (averages, sums, etc.) computed over the objects that are related to the objects in the QuerySet.

Each argument to annotate() is an annotation that will be added to each object in the QuerySet that is returned.

The aggregation functions that are provided by Django are described in Aggregation Functions below.

Annotations specified using keyword arguments will use the keyword as the alias for the annotation. Anonymous arguments will have an alias generated for them based upon the name of the aggregate function and the model field that is being aggregated. Only aggregate expressions that reference a single field can be anonymous arguments. Everything else must be a keyword argument.

For example, if you were manipulating a list of blogs, you may want to determine how many entries have been made in each blog:

The Blog model doesn’t define an entry__count attribute by itself, but by using a keyword argument to specify the aggregate function, you can control the name of the annotation:

For an in-depth discussion of aggregation, see the topic guide on Aggregation.

Same as annotate(), but instead of annotating objects in the QuerySet, saves the expression for later reuse with other QuerySet methods. This is useful when the result of the expression itself is not needed but it is used for filtering, ordering, or as a part of a complex expression. Not selecting the unused value removes redundant work from the database which should result in better performance.

For example, if you want to find blogs with more than 5 entries, but are not interested in the exact number of entries, you could do this:

alias() can be used in conjunction with annotate(), exclude(), filter(), order_by(), and update(). To use aliased expression with other methods (e.g. aggregate()), you must promote it to an annotation:

filter() and order_by() can take expressions directly, but expression construction and usage often does not happen in the same place (for example, QuerySet method creates expressions, for later use in views). alias() allows building complex expressions incrementally, possibly spanning multiple methods and modules, refer to the expression parts by their aliases and only use annotate() for the final result.

By default, results returned by a QuerySet are ordered by the ordering tuple given by the ordering option in the model’s Meta. You can override this on a per-QuerySet basis by using the order_by method.

The result above will be ordered by pub_date descending, then by headline ascending. The negative sign in front of "-pub_date" indicates descending order. Ascending order is implied. To order randomly, use "?", like so:

Note: order_by('?') queries may be expensive and slow, depending on the database backend you’re using.

To order by a field in a different model, use the same syntax as when you are querying across model relations. That is, the name of the field, followed by a double underscore (__), followed by the name of the field in the new model, and so on for as many models as you want to join. For example:

If you try to order by a field that is a relation to another model, Django will use the default ordering on the related model, or order by the related model’s primary key if there is no Meta.ordering specified. For example, since the Blog model has no default ordering specified:

If Blog had ordering = ['name'], then the first queryset would be identical to:

You can also order by query expressions by calling asc() or desc() on the expression:

asc() and desc() have arguments (nulls_first and nulls_last) that control how null values are sorted.

Be cautious when ordering by fields in related models if you are also using distinct(). See the note in distinct() for an explanation of how related model ordering can change the expected results.

It is permissible to specify a multi-valued field to order the results by (for example, a ManyToManyField field, or the reverse relation of a ForeignKey field).

Here, there could potentially be multiple ordering data for each Event; each Event with multiple children will be returned multiple times into the new QuerySet that order_by() creates. In other words, using order_by() on the QuerySet could return more items than you were working on to begin with - which is probably neither expected nor useful.

Thus, take care when using multi-valued field to order the results. If you can be sure that there will only be one ordering piece of data for each of the items you’re ordering, this approach should not present problems. If not, make sure the results are what you expect.

There’s no way to specify whether ordering should be case sensitive. With respect to case-sensitivity, Django will order results however your database backend normally orders them.

You can order by a field converted to lowercase with Lower which will achieve case-consistent ordering:

If you don’t want any ordering to be applied to a query, not even the default ordering, call order_by() with no parameters.

You can tell if a query is ordered or not by checking the QuerySet.ordered attribute, which will be True if the QuerySet has been ordered in any way.

Each order_by() call will clear any previous ordering. For example, this query will be ordered by pub_date and not headline:

Ordering is not a free operation. Each field you add to the ordering incurs a cost to your database. Each foreign key you add will implicitly include all of its default orderings as well.

If a query doesn’t have an ordering specified, results are returned from the database in an unspecified order. A particular ordering is guaranteed only when ordering by a set of fields that uniquely identify each object in the results. For example, if a name field isn’t unique, ordering by it won’t guarantee objects with the same name always appear in the same order.

Use the reverse() method to reverse the order in which a queryset’s elements are returned. Calling reverse() a second time restores the ordering back to the normal direction.

To retrieve the “last” five items in a queryset, you could do this:

Note that this is not quite the same as slicing from the end of a sequence in Python. The above example will return the last item first, then the penultimate item and so on. If we had a Python sequence and looked at seq[-5:], we would see the fifth-last item first. Django doesn’t support that mode of access (slicing from the end), because it’s not possible to do it efficiently in SQL.

Also, note that reverse() should generally only be called on a QuerySet which has a defined ordering (e.g., when querying against a model which defines a default ordering, or when using order_by()). If no such ordering is defined for a given QuerySet, calling reverse() on it has no real effect (the ordering was undefined prior to calling reverse(), and will remain undefined afterward).

Returns a new QuerySet that uses SELECT DISTINCT in its SQL query. This eliminates duplicate rows from the query results.

By default, a QuerySet will not eliminate duplicate rows. In practice, this is rarely a problem, because simple queries such as Blog.objects.all() don’t introduce the possibility of duplicate result rows. However, if your query spans multiple tables, it’s possible to get duplicate results when a QuerySet is evaluated. That’s when you’d use distinct().

Any fields used in an order_by() call are included in the SQL SELECT columns. This can sometimes lead to unexpected results when used in conjunction with distinct(). If you order by fields from a related model, those fields will be added to the selected columns and they may make otherwise duplicate rows appear to be distinct. Since the extra columns don’t appear in the returned results (they are only there to support ordering), it sometimes looks like non-distinct results are being returned.

Similarly, if you use a values() query to restrict the columns selected, the columns used in any order_by() (or default model ordering) will still be involved and may affect uniqueness of the results.

The moral here is that if you are using distinct() be careful about ordering by related models. Similarly, when using distinct() and values() together, be careful when ordering by fields not in the values() call.

On PostgreSQL only, you can pass positional arguments (*fields) in order to specify the names of fields to which the DISTINCT should apply. This translates to a SELECT DISTINCT ON SQL query. Here’s the difference. For a normal distinct() call, the database compares each field in each row when determining which rows are distinct. For a distinct() call with specified field names, the database will only compare the specified field names.

When you specify field names, you must provide an order_by() in the QuerySet, and the fields in order_by() must start with the fields in distinct(), in the same order.

For example, SELECT DISTINCT ON (a) gives you the first row for each value in column a. If you don’t specify an order, you’ll get some arbitrary row.

Examples (those after the first will only work on PostgreSQL):

Keep in mind that order_by() uses any default related model ordering that has been defined. You might have to explicitly order by the relation _id or referenced field to make sure the DISTINCT ON expressions match those at the beginning of the ORDER BY clause. For example, if the Blog model defined an ordering by name:

…wouldn’t work because the query would be ordered by blog__name thus mismatching the DISTINCT ON expression. You’d have to explicitly order by the relation _id field (blog_id in this case) or the referenced one (blog__pk) to make sure both expressions match.

Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable.

Each of those dictionaries represents an object, with the keys corresponding to the attribute names of model objects.

This example compares the dictionaries of values() with the normal model objects:

The values() method takes optional positional arguments, *fields, which specify field names to which the SELECT should be limited. If you specify the fields, each dictionary will contain only the field keys/values for the fields you specify. If you don’t specify the fields, each dictionary will contain a key and value for every field in the database table.

The values() method also takes optional keyword arguments, **expressions, which are passed through to annotate():

You can use built-in and custom lookups in ordering. For example:

An aggregate within a values() clause is applied before other arguments within the same values() clause. If you need to group by another value, add it to an earlier values() clause instead. For example:

A few subtleties that are worth mentioning:

If you have a field called foo that is a ForeignKey, the default values() call will return a dictionary key called foo_id, since this is the name of the hidden model attribute that stores the actual value (the foo attribute refers to the related model). When you are calling values() and passing in field names, you can pass in either foo or foo_id and you will get back the same thing (the dictionary key will match the field name you passed in).

When using values() together with distinct(), be aware that ordering can affect the results. See the note in distinct() for details.

If you use a values() clause after an extra() call, any fields defined by a select argument in the extra() must be explicitly included in the values() call. Any extra() call made after a values() call will have its extra selected fields ignored.

Calling only() and defer() after values() doesn’t make sense, so doing so will raise a TypeError.

Combining transforms and aggregates requires the use of two annotate() calls, either explicitly or as keyword arguments to values(). As above, if the transform has been registered on the relevant field type the first annotate() can be omitted, thus the following examples are equivalent:

It is useful when you know you’re only going to need values from a small number of the available fields and you won’t need the functionality of a model instance object. It’s more efficient to select only the fields you need to use.

Finally, note that you can call filter(), order_by(), etc. after the values() call, that means that these two calls are identical:

The people who made Django prefer to put all the SQL-affecting methods first, followed (optionally) by any output-affecting methods (such as values()), but it doesn’t really matter. This is your chance to really flaunt your individualism.

You can also refer to fields on related models with reverse relations through OneToOneField, ForeignKey and ManyToManyField attributes:

Because ManyToManyField attributes and reverse relations can have multiple related rows, including these can have a multiplier effect on the size of your result set. This will be especially pronounced if you include multiple such fields in your values() query, in which case all possible combinations will be returned.

Special values for JSONField on SQLite

Due to the way the JSON_EXTRACT and JSON_TYPE SQL functions are implemented on SQLite, and lack of the BOOLEAN data type, values() will return True, False, and None instead of "true", "false", and "null" strings for JSONField key transforms.

The SELECT clause generated when using values() was updated to respect the order of the specified *fields and **expressions.

This is similar to values() except that instead of returning dictionaries, it returns tuples when iterated over. Each tuple contains the value from the respective field or expression passed into the values_list() call — so the first item is the first field, etc. For example:

If you only pass in a single field, you can also pass in the flat parameter. If True, this will mean the returned results are single values, rather than 1-tuples. An example should make the difference clearer:

It is an error to pass in flat when there is more than one field.

You can pass named=True to get results as a namedtuple():

Using a named tuple may make use of the results more readable, at the expense of a small performance penalty for transforming the results into a named tuple.

If you don’t pass any values to values_list(), it will return all the fields in the model, in the order they were declared.

A common need is to get a specific field value of a certain model instance. To achieve that, use values_list() followed by a get() call:

values() and values_list() are both intended as optimizations for a specific use case: retrieving a subset of data without the overhead of creating a model instance. This metaphor falls apart when dealing with many-to-many and other multivalued relations (such as the one-to-many relation of a reverse foreign key) because the “one row, one object” assumption doesn’t hold.

For example, notice the behavior when querying across a ManyToManyField:

Authors with multiple entries appear multiple times and authors without any entries have None for the entry headline.

Similarly, when querying a reverse foreign key, None appears for entries not having any author:

Special values for JSONField on SQLite

Due to the way the JSON_EXTRACT and JSON_TYPE SQL functions are implemented on SQLite, and lack of the BOOLEAN data type, values_list() will return True, False, and None instead of "true", "false", and "null" strings for JSONField key transforms.

The SELECT clause generated when using values_list() was updated to respect the order of the specified *fields.

Returns a QuerySet that evaluates to a list of datetime.date objects representing all available dates of a particular kind within the contents of the QuerySet.

field should be the name of a DateField of your model. kind should be either "year", "month", "week", or "day". Each datetime.date object in the result list is “truncated” to the given type.

"year" returns a list of all distinct year values for the field.

"month" returns a list of all distinct year/month values for the field.

"week" returns a list of all distinct year/week values for the field. All dates will be a Monday.

"day" returns a list of all distinct year/month/day values for the field.

order, which defaults to 'ASC', should be either 'ASC' or 'DESC'. This specifies how to order the results.

Returns a QuerySet that evaluates to a list of datetime.datetime objects representing all available dates of a particular kind within the contents of the QuerySet.

field_name should be the name of a DateTimeField of your model.

kind should be either "year", "month", "week", "day", "hour", "minute", or "second". Each datetime.datetime object in the result list is “truncated” to the given type.

order, which defaults to 'ASC', should be either 'ASC' or 'DESC'. This specifies how to order the results.

tzinfo defines the time zone to which datetimes are converted prior to truncation. Indeed, a given datetime has different representations depending on the time zone in use. This parameter must be a datetime.tzinfo object. If it’s None, Django uses the current time zone. It has no effect when USE_TZ is False.

This function performs time zone conversions directly in the database. As a consequence, your database must be able to interpret the value of tzinfo.tzname(None). This translates into the following requirements:

SQLite: no requirements. Conversions are performed in Python.

PostgreSQL: no requirements (see Time Zones).

Oracle: no requirements (see Choosing a Time Zone File).

MySQL: load the time zone tables with mysql_tzinfo_to_sql.

Calling none() will create a queryset that never returns any objects and no query will be executed when accessing the results. A qs.none() queryset is an instance of EmptyQuerySet.

Returns a copy of the current QuerySet (or QuerySet subclass). This can be useful in situations where you might want to pass in either a model manager or a QuerySet and do further filtering on the result. After calling all() on either object, you’ll definitely have a QuerySet to work with.

When a QuerySet is evaluated, it typically caches its results. If the data in the database might have changed since a QuerySet was evaluated, you can get updated results for the same query by calling all() on a previously evaluated QuerySet.

Uses SQL’s UNION operator to combine the results of two or more QuerySets. For example:

The UNION operator selects only distinct values by default. To allow duplicate values, use the all=True argument.

union(), intersection(), and difference() return model instances of the type of the first QuerySet even if the arguments are QuerySets of other models. Passing different models works as long as the SELECT list is the same in all QuerySets (at least the types, the names don’t matter as long as the types are in the same order). In such cases, you must use the column names from the first QuerySet in QuerySet methods applied to the resulting QuerySet. For example:

In addition, only LIMIT, OFFSET, COUNT(*), ORDER BY, and specifying columns (i.e. slicing, count(), exists(), order_by(), and values()/values_list()) are allowed on the resulting QuerySet. Further, databases place restrictions on what operations are allowed in the combined queries. For example, most databases don’t allow LIMIT or OFFSET in the combined queries.

Uses SQL’s INTERSECT operator to return the shared elements of two or more QuerySets. For example:

See union() for some restrictions.

Uses SQL’s EXCEPT operator to keep only elements present in the QuerySet but not in some other QuerySets. For example:

See union() for some restrictions.

Returns a QuerySet that will “follow” foreign-key relationships, selecting additional related-object data when it executes its query. This is a performance booster which results in a single more complex query but means later use of foreign-key relationships won’t require database queries.

The following examples illustrate the difference between plain lookups and select_related() lookups. Here’s standard lookup:

And here’s select_related lookup:

You can use select_related() with any queryset of objects:

The order of filter() and select_related() chaining isn’t important. These querysets are equivalent:

You can follow foreign keys in a similar way to querying them. If you have the following models:

Then a call to Book.objects.select_related('author__hometown').get(id=4) will cache the related Person and the related City:

You can refer to any ForeignKey or OneToOneField relation in the list of fields passed to select_related().

You can also refer to the reverse direction of a OneToOneField in the list of fields passed to select_related — that is, you can traverse a OneToOneField back to the object on which the field is defined. Instead of specifying the field name, use the related_name for the field on the related object.

There may be some situations where you wish to call select_related() with a lot of related objects, or where you don’t know all of the relations. In these cases it is possible to call select_related() with no arguments. This will follow all non-null foreign keys it can find - nullable foreign keys must be specified. This is not recommended in most cases as it is likely to make the underlying query more complex, and return more data, than is actually needed.

If you need to clear the list of related fields added by past calls of select_related on a QuerySet, you can pass None as a parameter:

Chaining select_related calls works in a similar way to other methods - that is that select_related('foo', 'bar') is equivalent to select_related('foo').select_related('bar').

Returns a QuerySet that will automatically retrieve, in a single batch, related objects for each of the specified lookups.

This has a similar purpose to select_related, in that both are designed to stop the deluge of database queries that is caused by accessing related objects, but the strategy is quite different.

select_related works by creating an SQL join and including the fields of the related object in the SELECT statement. For this reason, select_related gets the related objects in the same database query. However, to avoid the much larger result set that would result from joining across a ‘many’ relationship, select_related is limited to single-valued relationships - foreign key and one-to-one.

prefetch_related, on the other hand, does a separate lookup for each relationship, and does the ‘joining’ in Python. This allows it to prefetch many-to-many, many-to-one, and GenericRelation objects which cannot be done using select_related, in addition to the foreign key and one-to-one relationships that are supported by select_related. It also supports prefetching of GenericForeignKey, however, the queryset for each ContentType must be provided in the querysets parameter of GenericPrefetch.

For example, suppose you have these models:

The problem with this is that every time Pizza.__str__() asks for self.toppings.all() it has to query the database, so Pizza.objects.all() will run a query on the Toppings table for every item in the Pizza QuerySet.

We can reduce to just two queries using prefetch_related:

This implies a self.toppings.all() for each Pizza; now each time self.toppings.all() is called, instead of having to go to the database for the items, it will find them in a prefetched QuerySet cache that was populated in a single query.

That is, all the relevant toppings will have been fetched in a single query, and used to make QuerySet instances that have a pre-filled cache of the relevant results; these are then used in the self.toppings.all() calls.

The additional queries in prefetch_related() are executed after the QuerySet has begun to be evaluated and the primary query has been executed.

Note that there is no mechanism to prevent another database query from altering the items in between the execution of the primary query and the additional queries, which could produce an inconsistent result. For example, if a Pizza is deleted after the primary query has executed, its toppings will not be returned in the additional query, and it will seem like the pizza has no toppings:

If you have an iterable of model instances, you can prefetch related attributes on those instances using the prefetch_related_objects() function.

Note that the result cache of the primary QuerySet and all specified related objects will then be fully loaded into memory. This changes the typical behavior of a QuerySet, which normally tries to avoid loading all objects into memory before they are needed, even after a query has been executed in the database.

Remember that, as always with QuerySet objects, any subsequent chained methods which imply a different database query will ignore previously cached results, and retrieve data using a fresh database query. So, if you write the following:

…then the fact that pizza.toppings.all() has been prefetched will not help you. The prefetch_related('toppings') implied pizza.toppings.all(), but pizza.toppings.filter() is a new and different query. The prefetched cache can’t help here; in fact it hurts performance, since you have done a database query that you haven’t used. So use this feature with caution!

Also, if you call the database-altering methods add(), create(), remove(), clear() or set(), on related managers, any prefetched cache for the relation will be cleared.

You can also use the normal join syntax to do related fields of related fields. Suppose we have an additional model to the example above:

The following are all legal:

This will prefetch all pizzas belonging to restaurants, and all toppings belonging to those pizzas. This will result in a total of 3 database queries - one for the restaurants, one for the pizzas, and one for the toppings.

This will fetch the best pizza and all the toppings for the best pizza for each restaurant. This will be done in 3 database queries - one for the restaurants, one for the ‘best pizzas’, and one for the toppings.

The best_pizza relationship could also be fetched using select_related to reduce the query count to 2:

Since the prefetch is executed after the main query (which includes the joins needed by select_related), it is able to detect that the best_pizza objects have already been fetched, and it will skip fetching them again.

Chaining prefetch_related calls will accumulate the lookups that are prefetched. To clear any prefetch_related behavior, pass None as a parameter:

One difference to note when using prefetch_related is that objects created by a query can be shared between the different objects that they are related to i.e. a single Python model instance can appear at more than one point in the tree of objects that are returned. This will normally happen with foreign key relationships. Typically this behavior will not be a problem, and will in fact save both memory and CPU time.

While prefetch_related supports prefetching GenericForeignKey relationships, the number of queries will depend on the data. Since a GenericForeignKey can reference data in multiple tables, one query per table referenced is needed, rather than one query for all the items. There could be additional queries on the ContentType table if the relevant rows have not already been fetched.

prefetch_related in most cases will be implemented using an SQL query that uses the ‘IN’ operator. This means that for a large QuerySet a large ‘IN’ clause could be generated, which, depending on the database, might have performance problems of its own when it comes to parsing or executing the SQL query. Always profile for your use case!

If you use iterator() to run the query, prefetch_related() calls will only be observed if a value for chunk_size is provided.

You can use the Prefetch object to further control the prefetch operation.

In its simplest form Prefetch is equivalent to the traditional string based lookups:

You can provide a custom queryset with the optional queryset argument. This can be used to change the default ordering of the queryset:

Or to call select_related() when applicable to reduce the number of queries even further:

You can also assign the prefetched result to a custom attribute with the optional to_attr argument. The result will be stored directly in a list.

This allows prefetching the same relation multiple times with a different QuerySet; for instance:

Lookups created with custom to_attr can still be traversed as usual by other lookups:

Using to_attr is recommended when filtering down the prefetch result as it is less ambiguous than storing a filtered result in the related manager’s cache:

Custom prefetching also works with single related relations like forward ForeignKey or OneToOneField. Generally you’ll want to use select_related() for these relations, but there are a number of cases where prefetching with a custom QuerySet is useful:

You want to use a QuerySet that performs further prefetching on related models.

You want to prefetch only a subset of the related objects.

You want to use performance optimization techniques like deferred fields:

When using multiple databases, Prefetch will respect your choice of database. If the inner query does not specify a database, it will use the database selected by the outer query. All of the following are valid:

The ordering of lookups matters.

Take the following examples:

This works even though it’s unordered because 'pizzas__toppings' already contains all the needed information, therefore the second argument 'pizzas' is actually redundant.

This will raise a ValueError because of the attempt to redefine the queryset of a previously seen lookup. Note that an implicit queryset was created to traverse 'pizzas' as part of the 'pizzas__toppings' lookup.

This will trigger an AttributeError because 'pizza_list' doesn’t exist yet when 'pizza_list__toppings' is being processed.

This consideration is not limited to the use of Prefetch objects. Some advanced techniques may require that the lookups be performed in a specific order to avoid creating extra queries; therefore it’s recommended to always carefully order prefetch_related arguments.

Sometimes, the Django query syntax by itself can’t easily express a complex WHERE clause. For these edge cases, Django provides the extra() QuerySet modifier — a hook for injecting specific clauses into the SQL generated by a QuerySet.

Use this method as a last resort

This is an old API that we aim to deprecate at some point in the future. Use it only if you cannot express your query using other queryset methods. If you do need to use it, please file a ticket using the QuerySet.extra keyword with your use case (please check the list of existing tickets first) so that we can enhance the QuerySet API to allow removing extra(). We are no longer improving or fixing bugs for this method.

For example, this use of extra():

The main benefit of using RawSQL is that you can set output_field if needed. The main downside is that if you refer to some table alias of the queryset in the raw SQL, then it is possible that Django might change that alias (for example, when the queryset is used as a subquery in yet another query).

You should be very careful whenever you use extra(). Every time you use it, you should escape any parameters that the user can control by using params in order to protect against SQL injection attacks.

You also must not quote placeholders in the SQL string. This example is vulnerable to SQL injection because of the quotes around %s:

You can read more about how Django’s SQL injection protection works.

By definition, these extra lookups may not be portable to different database engines (because you’re explicitly writing SQL code) and violate the DRY principle, so you should avoid them if possible.

Specify one or more of params, select, where or tables. None of the arguments is required, but you should use at least one of them.

The select argument lets you put extra fields in the SELECT clause. It should be a dictionary mapping attribute names to SQL clauses to use to calculate that attribute.

As a result, each Entry object will have an extra attribute, is_recent, a boolean representing whether the entry’s pub_date is greater than Jan. 1, 2006.

Django inserts the given SQL snippet directly into the SELECT statement, so the resulting SQL of the above example would be something like:

The next example is more advanced; it does a subquery to give each resulting Blog object an entry_count attribute, an integer count of associated Entry objects:

In this particular case, we’re exploiting the fact that the query will already contain the blog_blog table in its FROM clause.

The resulting SQL of the above example would be:

Note that the parentheses required by most database engines around subqueries are not required in Django’s select clauses.

In some rare cases, you might wish to pass parameters to the SQL fragments in extra(select=...). For this purpose, use the select_params parameter.

This will work, for example:

If you need to use a literal %s inside your select string, use the sequence %%s.

You can define explicit SQL WHERE clauses — perhaps to perform non-explicit joins — by using where. You can manually add tables to the SQL FROM clause by using tables.

where and tables both take a list of strings. All where parameters are “AND”ed to any other search criteria.

…translates (roughly) into the following SQL:

Be careful when using the tables parameter if you’re specifying tables that are already used in the query. When you add extra tables via the tables parameter, Django assumes you want that table included an extra time, if it is already included. That creates a problem, since the table name will then be given an alias. If a table appears multiple times in an SQL statement, the second and subsequent occurrences must use aliases so the database can tell them apart. If you’re referring to the extra table you added in the extra where parameter this is going to cause errors.

Normally you’ll only be adding extra tables that don’t already appear in the query. However, if the case outlined above does occur, there are a few solutions. First, see if you can get by without including the extra table and use the one already in the query. If that isn’t possible, put your extra() call at the front of the queryset construction so that your table is the first use of that table. Finally, if all else fails, look at the query produced and rewrite your where addition to use the alias given to your extra table. The alias will be the same each time you construct the queryset in the same way, so you can rely upon the alias name to not change.

If you need to order the resulting queryset using some of the new fields or tables you have included via extra() use the order_by parameter to extra() and pass in a sequence of strings. These strings should either be model fields (as in the normal order_by() method on querysets), of the form table_name.column_name or an alias for a column that you specified in the select parameter to extra().

This would sort all the items for which is_recent is true to the front of the result set (True sorts before False in a descending ordering).

This shows, by the way, that you can make multiple calls to extra() and it will behave as you expect (adding new constraints each time).

The where parameter described above may use standard Python database string placeholders — '%s' to indicate parameters the database engine should automatically quote. The params argument is a list of any extra parameters to be substituted.

Always use params instead of embedding values directly into where because params will ensure values are quoted correctly according to your particular backend. For example, quotes will be escaped correctly.

If you are performing queries on MySQL, note that MySQL’s silent type coercion may cause unexpected results when mixing types. If you query on a string type column, but with an integer value, MySQL will coerce the types of all values in the table to an integer before performing the comparison. For example, if your table contains the values 'abc', 'def' and you query for WHERE mycolumn=0, both rows will match. To prevent this, perform the correct typecasting before using the value in a query.

In some complex data-modeling situations, your models might contain a lot of fields, some of which could contain a lot of data (for example, text fields), or require expensive processing to convert them to Python objects. If you are using the results of a queryset in some situation where you don’t know if you need those particular fields when you initially fetch the data, you can tell Django not to retrieve them from the database.

This is done by passing the names of the fields to not load to defer():

A queryset that has deferred fields will still return model instances. Each deferred field will be retrieved from the database if you access that field (one at a time, not all the deferred fields at once).

Deferred fields will not lazy-load like this from asynchronous code. Instead, you will get a SynchronousOnlyOperation exception. If you are writing asynchronous code, you should not try to access any fields that you defer().

You can make multiple calls to defer(). Each call adds new fields to the deferred set:

The order in which fields are added to the deferred set does not matter. Calling defer() with a field name that has already been deferred is harmless (the field will still be deferred).

You can defer loading of fields in related models (if the related models are loading via select_related()) by using the standard double-underscore notation to separate related fields:

If you want to clear the set of deferred fields, pass None as a parameter to defer():

Some fields in a model won’t be deferred, even if you ask for them. You can never defer the loading of the primary key. If you are using select_related() to retrieve related models, you shouldn’t defer the loading of the field that connects from the primary model to the related one, doing so will result in an error.

Similarly, calling defer() (or its counterpart only()) including an argument from an aggregation (e.g. using the result of annotate()) doesn’t make sense: doing so will raise an exception. The aggregated values will always be fetched into the resulting queryset.

The defer() method (and its cousin, only(), below) are only for advanced use-cases. They provide an optimization for when you have analyzed your queries closely and understand exactly what information you need and have measured that the difference between returning the fields you need and the full set of fields for the model will be significant.

Even if you think you are in the advanced use-case situation, only use defer() when you cannot, at queryset load time, determine if you will need the extra fields or not. If you are frequently loading and using a particular subset of your data, the best choice you can make is to normalize your models and put the non-loaded data into a separate model (and database table). If the columns must stay in the one table for some reason, create a model with Meta.managed = False (see the managed attribute documentation) containing just the fields you normally need to load and use that where you might otherwise call defer(). This makes your code more explicit to the reader, is slightly faster and consumes a little less memory in the Python process.

For example, both of these models use the same underlying database table:

If many fields need to be duplicated in the unmanaged model, it may be best to create an abstract model with the shared fields and then have the unmanaged and managed models inherit from the abstract model.

When calling save() for instances with deferred fields, only the loaded fields will be saved. See save() for more details.

The only() method is essentially the opposite of defer(). Only the fields passed into this method and that are not already specified as deferred are loaded immediately when the queryset is evaluated.

If you have a model where almost all the fields need to be deferred, using only() to specify the complementary set of fields can result in simpler code.

Suppose you have a model with fields name, age and biography. The following two querysets are the same, in terms of deferred fields:

Whenever you call only() it replaces the set of fields to load immediately. The method’s name is mnemonic: only those fields are loaded immediately; the remainder are deferred. Thus, successive calls to only() result in only the final fields being considered:

Since defer() acts incrementally (adding fields to the deferred list), you can combine calls to only() and defer() and things will behave logically:

All of the cautions in the note for the defer() documentation apply to only() as well. Use it cautiously and only after exhausting your other options.

Using only() and omitting a field requested using select_related() is an error as well. On the other hand, invoking only() without any arguments, will return every field (including annotations) fetched by the queryset.

As with defer(), you cannot access the non-loaded fields from asynchronous code and expect them to load. Instead, you will get a SynchronousOnlyOperation exception. Ensure that all fields you might access are in your only() call.

When calling save() for instances with deferred fields, only the loaded fields will be saved. See save() for more details.

When using defer() after only() the fields in defer() will override only() for fields that are listed in both.

This method is for controlling which database the QuerySet will be evaluated against if you are using more than one database. The only argument this method takes is the alias of a database, as defined in DATABASES.

Returns a queryset that will lock rows until the end of the transaction, generating a SELECT ... FOR UPDATE SQL statement on supported databases.

When the queryset is evaluated (for entry in entries in this case), all matched entries will be locked until the end of the transaction block, meaning that other transactions will be prevented from changing or acquiring locks on them.

Usually, if another transaction has already acquired a lock on one of the selected rows, the query will block until the lock is released. If this is not the behavior you want, call select_for_update(nowait=True). This will make the call non-blocking. If a conflicting lock is already acquired by another transaction, DatabaseError will be raised when the queryset is evaluated. You can also ignore locked rows by using select_for_update(skip_locked=True) instead. The nowait and skip_locked are mutually exclusive and attempts to call select_for_update() with both options enabled will result in a ValueError.

By default, select_for_update() locks all rows that are selected by the query. For example, rows of related objects specified in select_related() are locked in addition to rows of the queryset’s model. If this isn’t desired, specify the related objects you want to lock in select_for_update(of=(...)) using the same fields syntax as select_related(). Use the value 'self' to refer to the queryset’s model.

Lock parents models in select_for_update(of=(...))

If you want to lock parents models when using multi-table inheritance, you must specify parent link fields (by default <parent_model_name>_ptr) in the of argument. For example:

Using select_for_update(of=(...)) with specified fields

If you want to lock models and specify selected fields, e.g. using values(), you must select at least one field from each model in the of argument. Models without selected fields will not be locked.

On PostgreSQL only, you can pass no_key=True in order to acquire a weaker lock, that still allows creating rows that merely reference locked rows (through a foreign key, for example) while the lock is in place. The PostgreSQL documentation has more details about row-level lock modes.

You can’t use select_for_update() on nullable relations:

To avoid that restriction, you can exclude null objects if you don’t care about them:

The postgresql, oracle, and mysql database backends support select_for_update(). However, MariaDB only supports the nowait argument, MariaDB 10.6+ also supports the skip_locked argument, and MySQL supports the nowait, skip_locked, and of arguments. The no_key argument is only supported on PostgreSQL.

Passing nowait=True, skip_locked=True, no_key=True, or of to select_for_update() using database backends that do not support these options, such as MySQL, raises a NotSupportedError. This prevents code from unexpectedly blocking.

Evaluating a queryset with select_for_update() in autocommit mode on backends which support SELECT ... FOR UPDATE is a TransactionManagementError error because the rows are not locked in that case. If allowed, this would facilitate data corruption and could easily be caused by calling code that expects to be run in a transaction outside of one.

Using select_for_update() on backends which do not support SELECT ... FOR UPDATE (such as SQLite) will have no effect. SELECT ... FOR UPDATE will not be added to the query, and an error isn’t raised if select_for_update() is used in autocommit mode.

Although select_for_update() normally fails in autocommit mode, since TestCase automatically wraps each test in a transaction, calling select_for_update() in a TestCase even outside an atomic() block will (perhaps unexpectedly) pass without raising a TransactionManagementError. To properly test select_for_update() you should use TransactionTestCase.

Certain expressions may not be supported

PostgreSQL doesn’t support select_for_update() with Window expressions.

Takes a raw SQL query, executes it, and returns a django.db.models.query.RawQuerySet instance. This RawQuerySet instance can be iterated over just like a normal QuerySet to provide object instances.

See the Performing raw SQL queries for more information.

raw() always triggers a new query and doesn’t account for previous filtering. As such, it should generally be called from the Manager or from a fresh QuerySet instance.

Combined querysets must use the same model.

Combines two QuerySets using the SQL AND operator in a manner similar to chaining filters.

The following are equivalent:

Combines two QuerySets using the SQL OR operator.

The following are equivalent:

| is not a commutative operation, as different (though equivalent) queries may be generated.

Combines two QuerySets using the SQL XOR operator. A XOR expression matches rows that are matched by an odd number of operands.

The following are equivalent:

XOR is natively supported on MariaDB and MySQL. On other databases, x ^ y ^ ... ^ z is converted to an equivalent:

The following QuerySet methods evaluate the QuerySet and return something other than a QuerySet.

These methods do not use a cache (see Caching and QuerySets). Rather, they query the database each time they’re called.

Because these methods evaluate the QuerySet, they are blocking calls, and so their main (synchronous) versions cannot be called from asynchronous code. For this reason, each has a corresponding asynchronous version with an a prefix - for example, rather than get(…) you can await aget(…).

There is usually no difference in behavior apart from their asynchronous nature, but any differences are noted below next to each method.

Asynchronous version: aget()

Returns the object matching the given lookup parameters, which should be in the format described in Field lookups. You should use lookups that are guaranteed unique, such as the primary key or fields in a unique constraint. For example:

If you expect a queryset to already return one row, you can use get() without any arguments to return the object for that row:

If get() doesn’t find any object, it raises a Model.DoesNotExist exception:

If get() finds more than one object, it raises a Model.MultipleObjectsReturned exception:

Both these exception classes are attributes of the model class, and specific to that model. If you want to handle such exceptions from several get() calls for different models, you can use their generic base classes. For example, you can use django.core.exceptions.ObjectDoesNotExist to handle DoesNotExist exceptions from multiple models:

Asynchronous version: acreate()

A convenience method for creating an object and saving it all in one step. Thus:

The force_insert parameter is documented elsewhere, but all it means is that a new object will always be created. Normally you won’t need to worry about this. However, if your model contains a manual primary key value that you set and if that value already exists in the database, a call to create() will fail with an IntegrityError since primary keys must be unique. Be prepared to handle the exception if you are using manual primary keys.

Asynchronous version: aget_or_create()

A convenience method for looking up an object with the given kwargs (may be empty if your model has defaults for all fields), creating one if necessary.

Returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean specifying whether a new object was created.

This is meant to prevent duplicate objects from being created when requests are made in parallel, and as a shortcut to boilerplatish code. For example:

Here, with concurrent requests, multiple attempts to save a Person with the same parameters may be made. To avoid this race condition, the above example can be rewritten using get_or_create() like so:

Any keyword arguments passed to get_or_create() — except an optional one called defaults — will be used in a get() call. If an object is found, get_or_create() returns a tuple of that object and False.

This method is atomic assuming that the database enforces uniqueness of the keyword arguments (see unique or unique_together). If the fields used in the keyword arguments do not have a uniqueness constraint, concurrent calls to this method may result in multiple rows with the same parameters being inserted.

You can specify more complex conditions for the retrieved object by chaining get_or_create() with filter() and using Q objects. For example, to retrieve Robert or Bob Marley if either exists, and create the latter otherwise:

If multiple objects are found, get_or_create() raises MultipleObjectsReturned. If an object is not found, get_or_create() will instantiate and save a new object, returning a tuple of the new object and True. The new object will be created roughly according to this algorithm:

In English, that means start with any non-'defaults' keyword argument that doesn’t contain a double underscore (which would indicate a non-exact lookup). Then add the contents of defaults, overriding any keys if necessary, and use the result as the keyword arguments to the model class. If there are any callables in defaults, evaluate them. As hinted at above, this is a simplification of the algorithm that is used, but it contains all the pertinent details. The internal implementation has some more error-checking than this and handles some extra edge-conditions; if you’re interested, read the code.

If you have a field named defaults and want to use it as an exact lookup in get_or_create(), use 'defaults__exact', like so:

The get_or_create() method has similar error behavior to create() when you’re using manually specified primary keys. If an object needs to be created and the key already exists in the database, an IntegrityError will be raised.

Finally, a word on using get_or_create() in Django views. Please make sure to use it only in POST requests unless you have a good reason not to. GET requests shouldn’t have any effect on data. Instead, use POST whenever a request to a page has a side effect on your data. For more, see Safe methods in the HTTP spec.

You can use get_or_create() through ManyToManyField attributes and reverse relations. In that case you will restrict the queries inside the context of that relation. That could lead you to some integrity problems if you don’t use it consistently.

Being the following models:

You can use get_or_create() through Book’s chapters field, but it only fetches inside the context of that book:

This is happening because it’s trying to get or create “Chapter 1” through the book “Ulysses”, but it can’t do either: the relation can’t fetch that chapter because it isn’t related to that book, but it can’t create it either because title field should be unique.

Asynchronous version: aupdate_or_create()

A convenience method for updating an object with the given kwargs, creating a new one if necessary. Both create_defaults and defaults are dictionaries of (field, value) pairs. The values in both create_defaults and defaults can be callables. defaults is used to update the object while create_defaults are used for the create operation. If create_defaults is not supplied, defaults will be used for the create operation.

Returns a tuple of (object, created), where object is the created or updated object and created is a boolean specifying whether a new object was created.

The update_or_create method tries to fetch an object from database based on the given kwargs. If a match is found, it updates the fields passed in the defaults dictionary.

This is meant as a shortcut to boilerplatish code. For example:

This pattern gets quite unwieldy as the number of fields in a model goes up. The above example can be rewritten using update_or_create() like so:

For a detailed description of how names passed in kwargs are resolved, see get_or_create().

As described above in get_or_create(), this method is prone to a race-condition which can result in multiple rows being inserted simultaneously if uniqueness is not enforced at the database level.

Like get_or_create() and create(), if you’re using manually specified primary keys and an object needs to be created but the key already exists in the database, an IntegrityError is raised.

Asynchronous version: abulk_create()

This method inserts the provided list of objects into the database in an efficient manner (generally only 1 query, no matter how many objects there are), and returns created objects as a list, in the same order as provided:

This has a number of caveats though:

The model’s save() method will not be called, and the pre_save and post_save signals will not be sent.

It does not work with child models in a multi-table inheritance scenario.

If the model’s primary key is an AutoField or has a db_default value, and ignore_conflicts is False, the primary key attribute can only be retrieved on certain databases (currently PostgreSQL, MariaDB, and SQLite 3.35+). On other databases, it will not be set.

It does not work with many-to-many relationships.

It casts objs to a list, which fully evaluates objs if it’s a generator. The cast allows inspecting all objects so that any objects with a manually set primary key can be inserted first. If you want to insert objects in batches without evaluating the entire generator at once, you can use this technique as long as the objects don’t have any manually set primary keys:

The batch_size parameter controls how many objects are created in a single query. The default is to create as many objects in one batch as the database will allow. (SQLite and Oracle limit the number of parameters in a query.)

On databases that support it (all but Oracle), setting the ignore_conflicts parameter to True tells the database to ignore failure to insert any rows that fail constraints such as duplicate unique values.

On databases that support it (all except Oracle), setting the update_conflicts parameter to True, tells the database to update update_fields when a row insertion fails on conflicts. On PostgreSQL and SQLite, in addition to update_fields, a list of unique_fields that may be in conflict must be provided.

Enabling the ignore_conflicts parameter disables setting the primary key on each model instance (if the database normally supports it).

On MySQL and MariaDB, setting the ignore_conflicts parameter to True turns certain types of errors, other than duplicate key, into warnings. Even with Strict Mode. For example: invalid values or non-nullable violations. See the MySQL documentation and MariaDB documentation for more details.

Asynchronous version: abulk_update()

This method efficiently updates the given fields on the provided model instances, generally with one query, and returns the number of objects updated:

QuerySet.update() is used to save the changes, so this is more efficient than iterating through the list of models and calling save() on each of them, but it has a few caveats:

You cannot update the model’s primary key.

Each model’s save() method isn’t called, and the pre_save and post_save signals aren’t sent.

If updating a large number of columns in a large number of rows, the SQL generated can be very large. Avoid this by specifying a suitable batch_size.

When updating a large number of objects, be aware that bulk_update() prepares all of the WHEN clauses for every object across all batches before executing any queries. This can require more memory than expected. To reduce memory usage, you can use an approach like this:

Updating fields defined on multi-table inheritance ancestors will incur an extra query per ancestor.

When an individual batch contains duplicates, only the first instance in that batch will result in an update.

The number of objects updated returned by the function may be fewer than the number of objects passed in. This can be due to duplicate objects passed in which are updated in the same batch or race conditions such that objects are no longer present in the database.

The batch_size parameter controls how many objects are saved in a single query. The default is to update all objects in one batch, except for SQLite and Oracle which have restrictions on the number of variables used in a query.

Asynchronous version: acount()

Returns an integer representing the number of objects in the database matching the QuerySet.

A count() call performs a SELECT COUNT(*) behind the scenes, so you should always use count() rather than loading all of the record into Python objects and calling len() on the result (unless you need to load the objects into memory anyway, in which case len() will be faster).

Note that if you want the number of items in a QuerySet and are also retrieving model instances from it (for example, by iterating over it), it’s probably more efficient to use len(queryset) which won’t cause an extra database query like count() would.

If the queryset has already been fully retrieved, count() will use that length rather than perform an extra database query.

Asynchronous version: ain_bulk()

Takes a list of field values (id_list) and the field_name for those values, and returns a dictionary mapping each value to an instance of the object with the given field value. No django.core.exceptions.ObjectDoesNotExist exceptions will ever be raised by in_bulk; that is, any id_list value not matching any instance will simply be ignored. If id_list isn’t provided, all objects in the queryset are returned. field_name must be a unique field or a distinct field (if there’s only one field specified in distinct()). field_name defaults to the primary key.

If you pass in_bulk() an empty list, you’ll get an empty dictionary.

Asynchronous version: aiterator()

Evaluates the QuerySet (by performing the query) and returns an iterator (see PEP 234) over the results, or an asynchronous iterator (see PEP 492) if you call its asynchronous version aiterator.

A QuerySet typically caches its results internally so that repeated evaluations do not result in additional queries. In contrast, iterator() will read results directly, without doing any caching at the QuerySet level (internally, the default iterator calls iterator() and caches the return value). For a QuerySet which returns a large number of objects that you only need to access once, this can result in better performance and a significant reduction in memory.

Note that using iterator() on a QuerySet which has already been evaluated will force it to evaluate again, repeating the query.

iterator() is compatible with previous calls to prefetch_related() as long as chunk_size is given. Larger values will necessitate fewer queries to accomplish the prefetching at the cost of greater memory usage.

On some databases (e.g. Oracle, SQLite), the maximum number of terms in an SQL IN clause might be limited. Hence values below this limit should be used. (In particular, when prefetching across two or more relations, a chunk_size should be small enough that the anticipated number of results for each prefetched relation still falls below the limit.)

So long as the QuerySet does not prefetch any related objects, providing no value for chunk_size will result in Django using an implicit default of 2000.

Depending on the database backend, query results will either be loaded all at once or streamed from the database using server-side cursors.

Oracle and PostgreSQL use server-side cursors to stream results from the database without loading the entire result set into memory.

The Oracle database driver always uses server-side cursors.

With server-side cursors, the chunk_size parameter specifies the number of results to cache at the database driver level. Fetching bigger chunks diminishes the number of round trips between the database driver and the database, at the expense of memory.

On PostgreSQL, server-side cursors will only be used when the DISABLE_SERVER_SIDE_CURSORS setting is False. Read Transaction pooling and server-side cursors if you’re using a connection pooler configured in transaction pooling mode. When server-side cursors are disabled, the behavior is the same as databases that don’t support server-side cursors.

MySQL doesn’t support streaming results, hence the Python database driver loads the entire result set into memory. The result set is then transformed into Python row objects by the database adapter using the fetchmany() method defined in PEP 249.

SQLite can fetch results in batches using fetchmany(), but since SQLite doesn’t provide isolation between queries within a connection, be careful when writing to the table being iterated over. See Isolation when using QuerySet.iterator() for more information.

The chunk_size parameter controls the size of batches Django retrieves from the database driver. Larger batches decrease the overhead of communicating with the database driver at the expense of a slight increase in memory consumption.

So long as the QuerySet does not prefetch any related objects, providing no value for chunk_size will result in Django using an implicit default of 2000, a value derived from a calculation on the psycopg mailing list:

Assuming rows of 10-20 columns with a mix of textual and numeric data, 2000 is going to fetch less than 100KB of data, which seems a good compromise between the number of rows transferred and the data discarded if the loop is exited early.

Asynchronous version: alatest()

Returns the latest object in the table based on the given field(s).

This example returns the latest Entry in the table, according to the pub_date field:

You can also choose the latest based on several fields. For example, to select the Entry with the earliest expire_date when two entries have the same pub_date:

The negative sign in '-expire_date' means to sort expire_date in descending order. Since latest() gets the last result, the Entry with the earliest expire_date is selected.

If your model’s Meta specifies get_latest_by, you can omit any arguments to earliest() or latest(). The fields specified in get_latest_by will be used by default.

Like get(), earliest() and latest() raise DoesNotExist if there is no object with the given parameters.

Note that earliest() and latest() exist purely for convenience and readability.

earliest() and latest() may return instances with null dates.

Since ordering is delegated to the database, results on fields that allow null values may be ordered differently if you use different databases. For example, PostgreSQL and MySQL sort null values as if they are higher than non-null values, while SQLite does the opposite.

You may want to filter out null values:

Asynchronous version: aearliest()

Works otherwise like latest() except the direction is changed.

Asynchronous version: afirst()

Returns the first object matched by the queryset, or None if there is no matching object. If the QuerySet has no ordering defined, then the queryset is automatically ordered by the primary key. This can affect aggregation results as described in Interaction with order_by().

Note that first() is a convenience method, the following code sample is equivalent to the above example:

Asynchronous version: alast()

Works like first(), but returns the last object in the queryset.

Asynchronous version: aaggregate()

Returns a dictionary of aggregate values (averages, sums, etc.) calculated over the QuerySet. Each argument to aggregate() specifies a value that will be included in the dictionary that is returned.

The aggregation functions that are provided by Django are described in Aggregation Functions below. Since aggregates are also query expressions, you may combine aggregates with other aggregates or values to create complex aggregates.

Aggregates specified using keyword arguments will use the keyword as the name for the annotation. Anonymous arguments will have a name generated for them based upon the name of the aggregate function and the model field that is being aggregated. Complex aggregates cannot use anonymous arguments and must specify a keyword argument as an alias.

For example, when you are working with blog entries, you may want to know the number of authors that have contributed blog entries:

By using a keyword argument to specify the aggregate function, you can control the name of the aggregation value that is returned:

For an in-depth discussion of aggregation, see the topic guide on Aggregation.

Asynchronous version: aexists()

Returns True if the QuerySet contains any results, and False if not. This tries to perform the query in the simplest and fastest way possible, but it does execute nearly the same query as a normal QuerySet query.

exists() is useful for searches relating to the existence of any objects in a QuerySet, particularly in the context of a large QuerySet.

To find whether a queryset contains any items:

Which will be faster than:

… but not by a large degree (hence needing a large queryset for efficiency gains).

Additionally, if a some_queryset has not yet been evaluated, but you know that it will be at some point, then using some_queryset.exists() will do more overall work (one query for the existence check plus an extra one to later retrieve the results) than using bool(some_queryset), which retrieves the results and then checks if any were returned.

Asynchronous version: acontains()

Returns True if the QuerySet contains obj, and False if not. This tries to perform the query in the simplest and fastest way possible.

contains() is useful for checking an object membership in a QuerySet, particularly in the context of a large QuerySet.

To check whether a queryset contains a specific item:

This will be faster than the following which requires evaluating and iterating through the entire queryset:

Like exists(), if some_queryset has not yet been evaluated, but you know that it will be at some point, then using some_queryset.contains(obj) will make an additional database query, generally resulting in slower overall performance.

Asynchronous version: aupdate()

Performs an SQL update query for the specified fields, and returns the number of rows matched (which may not be equal to the number of rows updated if some rows already have the new value).

For example, to turn comments off for all blog entries published in 2010, you could do this:

(This assumes your Entry model has fields pub_date and comments_on.)

You can update multiple fields — there’s no limit on how many. For example, here we update the comments_on and headline fields:

The update() method is applied instantly, and the only restriction on the QuerySet that is updated is that it can only update columns in the model’s main table, not on related models. You can’t do this, for example:

Filtering based on related fields is still possible, though:

You cannot call update() on a QuerySet that has had a slice taken or can otherwise no longer be filtered.

The update() method returns the number of affected rows:

If you’re just updating a record and don’t need to do anything with the model object, the most efficient approach is to call update(), rather than loading the model object into memory. For example, instead of doing this:

Using update() also prevents a race condition wherein something might change in your database in the short period of time between loading the object and calling save().

MySQL does not support self-select updates

On MySQL, QuerySet.update() may execute a SELECT followed by an UPDATE instead of a single UPDATE when filtering on related tables, which can introduce a race condition if concurrent changes occur between the queries. To ensure atomicity, consider using transactions or avoiding such filter conditions on MySQL.

Finally, realize that update() does an update at the SQL level and, thus, does not call any save() methods on your models, nor does it emit the pre_save or post_save signals (which are a consequence of calling Model.save()). If you want to update a bunch of records for a model that has a custom save() method, loop over them and call save(), like this:

Chaining order_by() with update() is supported only on MariaDB and MySQL, and is ignored for different databases. This is useful for updating a unique field in the order that is specified without conflicts. For example:

order_by() clause will be ignored if it contains annotations, inherited fields, or lookups spanning relations.

Asynchronous version: adelete()

Performs an SQL delete query on all rows in the QuerySet and returns the number of objects deleted and a dictionary with the number of deletions per object type.

The delete() is applied instantly. You cannot call delete() on a QuerySet that has had a slice taken or can otherwise no longer be filtered.

For example, to delete all the entries in a particular blog:

By default, Django’s ForeignKey emulates the SQL constraint ON DELETE CASCADE — in other words, any objects with foreign keys pointing at the objects to be deleted will be deleted along with them. For example:

This cascade behavior is customizable via the on_delete argument to the ForeignKey.

The delete() method does a bulk delete and does not call any delete() methods on your models. It does, however, emit the pre_delete and post_delete signals for all deleted objects (including cascaded deletions).

Django needs to fetch objects into memory to send signals and handle cascades. However, if there are no cascades and no signals, then Django may take a fast-path and delete objects without fetching into memory. For large deletes this can result in significantly reduced memory usage. The amount of executed queries can be reduced, too.

ForeignKeys which are set to on_delete DO_NOTHING do not prevent taking the fast-path in deletion.

Note that the queries generated in object deletion is an implementation detail subject to change.

Class method that returns an instance of Manager with a copy of the QuerySet’s methods. See Creating a manager with QuerySet methods for more details.

Note that unlike the other entries in this section, this does not have an asynchronous variant as it does not execute a query.

Asynchronous version: aexplain()

Returns a string of the QuerySet’s execution plan, which details how the database would execute the query, including any indexes or joins that would be used. Knowing these details may help you improve the performance of slow queries.

For example, when using PostgreSQL:

The output differs significantly between databases.

explain() is supported by all built-in database backends except Oracle because an implementation there isn’t straightforward.

The format parameter changes the output format from the databases’s default, which is usually text-based. PostgreSQL supports 'TEXT', 'JSON', 'YAML', and 'XML' formats. MariaDB and MySQL support 'TEXT' (also called 'TRADITIONAL') and 'JSON' formats. MySQL 8.0.16+ also supports an improved 'TREE' format, which is similar to PostgreSQL’s 'TEXT' output and is used by default, if supported.

Some databases accept flags that can return more information about the query. Pass these flags as keyword arguments. For example, when using PostgreSQL:

On some databases, flags may cause the query to be executed which could have adverse effects on your database. For example, the ANALYZE flag supported by MariaDB, MySQL 8.0.18+, and PostgreSQL could result in changes to data if there are triggers or if a function is called, even for a SELECT query.

Support for the memory and serialize options on PostgreSQL 17+ was added.

Field lookups are how you specify the meat of an SQL WHERE clause. They’re specified as keyword arguments to the QuerySet methods filter(), exclude() and get().

For an introduction, see models and database queries documentation.

Django’s built-in lookups are listed below. It is also possible to write custom lookups for model fields.

As a convenience when no lookup type is provided (like in Entry.objects.get(id=14)) the lookup type is assumed to be exact.

Exact match. If the value provided for comparison is None, it will be interpreted as an SQL NULL (see isnull for more details).

In MySQL, a database table’s “collation” setting determines whether exact comparisons are case-sensitive. This is a database setting, not a Django setting. It’s possible to configure your MySQL tables to use case-sensitive comparisons, but some trade-offs are involved. For more information about this, see the collation section in the databases documentation.

Case-insensitive exact match. If the value provided for comparison is None, it will be interpreted as an SQL NULL (see isnull for more details).

Note the first query will match 'Beatles Blog', 'beatles blog', 'BeAtLes BLoG', etc.

When using the SQLite backend and non-ASCII strings, bear in mind the database note about string comparisons. SQLite does not do case-insensitive matching for non-ASCII strings.

Case-sensitive containment test.

Note this will match the headline 'Lennon honored today' but not 'lennon honored today'.

SQLite doesn’t support case-sensitive LIKE statements; contains acts like icontains for SQLite. See the database note for more information.

Case-insensitive containment test.

When using the SQLite backend and non-ASCII strings, bear in mind the database note about string comparisons.

In a given iterable; often a list, tuple, or queryset. It’s not a common use case, but strings (being iterables) are accepted.

You can also use a queryset to dynamically evaluate the list of values instead of providing a list of literal values:

This queryset will be evaluated as subselect statement:

If you pass in a QuerySet resulting from values() or values_list() as the value to an __in lookup, you need to ensure you are only extracting one field in the result. For example, this will work (filtering on the blog names):

This example will raise an exception, since the inner query is trying to extract two field values, where only one is expected:

Performance considerations

Be cautious about using nested queries and understand your database server’s performance characteristics (if in doubt, benchmark!). Some database backends, most notably MySQL, don’t optimize nested queries very well. It is more efficient, in those cases, to extract a list of values and then pass that into the second query. That is, execute two queries instead of one:

Note the list() call around the Blog QuerySet to force execution of the first query. Without it, a nested query would be executed, because QuerySets are lazy.

Greater than or equal to.

Less than or equal to.

Case-sensitive starts-with.

SQLite doesn’t support case-sensitive LIKE statements; startswith acts like istartswith for SQLite.

Case-insensitive starts-with.

When using the SQLite backend and non-ASCII strings, bear in mind the database note about string comparisons.

Case-sensitive ends-with.

SQLite doesn’t support case-sensitive LIKE statements; endswith acts like iendswith for SQLite. Refer to the database note documentation for more.

Case-insensitive ends-with.

When using the SQLite backend and non-ASCII strings, bear in mind the database note about string comparisons.

Range test (inclusive).

You can use range anywhere you can use BETWEEN in SQL — for dates, numbers and even characters.

Filtering a DateTimeField with dates won’t include items on the last day, because the bounds are interpreted as “0am on the given date”. If pub_date was a DateTimeField, the above expression would be turned into this SQL:

Generally speaking, you can’t mix dates and datetimes.

For datetime fields, casts the value as date. Allows chaining additional field lookups. Takes a date value.

(No equivalent SQL code fragment is included for this lookup because implementation of the relevant query varies among different database engines.)

When USE_TZ is True, fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For date and datetime fields, an exact year match. Allows chaining additional field lookups. Takes an integer year.

(The exact SQL syntax varies for each database engine.)

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For date and datetime fields, an exact ISO 8601 week-numbering year match. Allows chaining additional field lookups. Takes an integer year.

(The exact SQL syntax varies for each database engine.)

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For date and datetime fields, an exact month match. Allows chaining additional field lookups. Takes an integer 1 (January) through 12 (December).

(The exact SQL syntax varies for each database engine.)

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For date and datetime fields, an exact day match. Allows chaining additional field lookups. Takes an integer day.

(The exact SQL syntax varies for each database engine.)

Note this will match any record with a pub_date on the third day of the month, such as January 3, July 3, etc.

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For date and datetime fields, return the week number (1-52 or 53) according to ISO-8601, i.e., weeks start on a Monday and the first week contains the year’s first Thursday.

(No equivalent SQL code fragment is included for this lookup because implementation of the relevant query varies among different database engines.)

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For date and datetime fields, a ‘day of the week’ match. Allows chaining additional field lookups.

Takes an integer value representing the day of week from 1 (Sunday) to 7 (Saturday).

(No equivalent SQL code fragment is included for this lookup because implementation of the relevant query varies among different database engines.)

Note this will match any record with a pub_date that falls on a Monday (day 2 of the week), regardless of the month or year in which it occurs. Week days are indexed with day 1 being Sunday and day 7 being Saturday.

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For date and datetime fields, an exact ISO 8601 day of the week match. Allows chaining additional field lookups.

Takes an integer value representing the day of the week from 1 (Monday) to 7 (Sunday).

(No equivalent SQL code fragment is included for this lookup because implementation of the relevant query varies among different database engines.)

Note this will match any record with a pub_date that falls on a Monday (day 1 of the week), regardless of the month or year in which it occurs. Week days are indexed with day 1 being Monday and day 7 being Sunday.

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For date and datetime fields, a ‘quarter of the year’ match. Allows chaining additional field lookups. Takes an integer value between 1 and 4 representing the quarter of the year.

Example to retrieve entries in the second quarter (April 1 to June 30):

(No equivalent SQL code fragment is included for this lookup because implementation of the relevant query varies among different database engines.)

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For datetime fields, casts the value as time. Allows chaining additional field lookups. Takes a datetime.time value.

(No equivalent SQL code fragment is included for this lookup because implementation of the relevant query varies among different database engines.)

When USE_TZ is True, fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For datetime and time fields, an exact hour match. Allows chaining additional field lookups. Takes an integer between 0 and 23.

(The exact SQL syntax varies for each database engine.)

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For datetime and time fields, an exact minute match. Allows chaining additional field lookups. Takes an integer between 0 and 59.

(The exact SQL syntax varies for each database engine.)

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

For datetime and time fields, an exact second match. Allows chaining additional field lookups. Takes an integer between 0 and 59.

(The exact SQL syntax varies for each database engine.)

When USE_TZ is True, datetime fields are converted to the current time zone before filtering. This requires time zone definitions in the database.

Takes either True or False, which correspond to SQL queries of IS NULL and IS NOT NULL, respectively.

Case-sensitive regular expression match.

The regular expression syntax is that of the database backend in use. In the case of SQLite, which has no built in regular expression support, this feature is provided by a (Python) user-defined REGEXP function, and the regular expression syntax is therefore that of Python’s re module.

Using raw strings (e.g., r'foo' instead of 'foo') for passing in the regular expression syntax is recommended.

Case-insensitive regular expression match.

Django provides the following aggregation functions in the django.db.models module. For details on how to use these aggregate functions, see the topic guide on aggregation. See the Aggregate documentation to learn how to create your aggregates.

SQLite can’t handle aggregation on date/time fields out of the box. This is because there are no native date/time fields in SQLite and Django currently emulates these features using a text field. Attempts to use aggregation on date/time fields in SQLite will raise NotSupportedError.

Empty querysets or groups

Aggregation functions return None when used with an empty QuerySet or group. For example, the Sum aggregation function returns None instead of 0 if the QuerySet contains no entries or for any empty group in a non-empty QuerySet. To return another value instead, define the default argument. Count is an exception to this behavior; it returns 0 if the QuerySet is empty since Count does not support the default argument.

All aggregates have the following parameters in common:

Strings that reference fields on the model, transforms of the field, or query expressions.

An optional argument that represents the model field of the return value

When combining multiple field types, Django can only determine the output_field if all fields are of the same type. Otherwise, you must provide the output_field yourself.

An optional Q object that’s used to filter the rows that are aggregated.

See Conditional aggregation and Filtering on annotations for example usage.

An optional argument that allows specifying a value to use as a default value when the queryset (or grouping) contains no entries.

Keyword arguments that can provide extra context for the SQL generated by the aggregate.

Returns an arbitrary value from the non-null input values.

Default alias: <field>__anyvalue

Return type: same as input field, or output_field if supplied. If the queryset or grouping is empty, default is returned.

Supported on SQLite, MySQL, Oracle, and PostgreSQL 16+.

MySQL with ONLY_FULL_GROUP_BY enabled

When the ONLY_FULL_GROUP_BY SQL mode is enabled on MySQL it may be necessary to use AnyValue if an aggregation includes a mix of aggregate and non-aggregate functions. Using AnyValue allows the non-aggregate function to be referenced in the select list when database cannot determine that it is functionally dependent on the columns in the group by clause. See the aggregation documentation for more details.

Returns the mean value of the given expression, which must be numeric unless you specify a different output_field.

Default alias: <field>__avg

Return type: float if input is int, otherwise same as input field, or output_field if supplied. If the queryset or grouping is empty, default is returned.

Optional. If distinct=True, Avg returns the mean value of unique values. This is the SQL equivalent of AVG(DISTINCT <field>). The default value is False.

Returns the number of objects that are related through the provided expression. Count('*') is equivalent to the SQL COUNT(*) expression.

Default alias: <field>__count

Optional. If distinct=True, the count will only include unique instances. This is the SQL equivalent of COUNT(DISTINCT <field>). The default value is False.

The default argument is not supported.

Returns the maximum value of the given expression.

Default alias: <field>__max

Return type: same as input field, or output_field if supplied. If the queryset or grouping is empty, default is returned.

Returns the minimum value of the given expression.

Default alias: <field>__min

Return type: same as input field, or output_field if supplied. If the queryset or grouping is empty, default is returned.

Returns the standard deviation of the data in the provided expression.

Default alias: <field>__stddev

Return type: float if input is int, otherwise same as input field, or output_field if supplied. If the queryset or grouping is empty, default is returned.

Optional. By default, StdDev returns the population standard deviation. However, if sample=True, the return value will be the sample standard deviation.

Computes the sum of all values of the given expression.

Default alias: <field>__sum

Return type: same as input field, or output_field if supplied. If the queryset or grouping is empty, default is returned.

Optional. If distinct=True, Sum returns the sum of unique values. This is the SQL equivalent of SUM(DISTINCT <field>). The default value is False.

Returns the variance of the data in the provided expression.

Default alias: <field>__variance

Return type: float if input is int, otherwise same as input field, or output_field if supplied. If the queryset or grouping is empty, default is returned.

Optional. By default, Variance returns the population variance. However, if sample=True, the return value will be the sample variance.

Returns the input values concatenated into a string, separated by the delimiter string, or default if there are no values.

Default alias: <field>__stringagg

Return type: string or output_field if supplied. If the queryset or grouping is empty, default is returned.

A Value or expression representing the string that should separate each of the values. For example, Value(",").

This section provides reference material for query-related tools not documented elsewhere.

A Q() object represents an SQL condition that can be used in database-related operations. It’s similar to how an F() object represents the value of a model field or annotation. They make it possible to define and reuse conditions. These can be negated using the ~ (NOT) operator, and combined using operators such as | (OR), & (AND), and ^ (XOR). See Complex lookups with Q objects.

The Prefetch() object can be used to control the operation of prefetch_related().

The lookup argument describes the relations to follow and works the same as the string based lookups passed to prefetch_related(). For example:

The queryset argument supplies a base QuerySet for the given lookup. This is useful to further filter down the prefetch operation, or to call select_related() from the prefetched relation, hence reducing the number of queries even further:

The to_attr argument sets the result of the prefetch operation to a custom attribute:

When using to_attr the prefetched result is stored in a list. This can provide a significant speed improvement over traditional prefetch_related calls which store the cached result within a QuerySet instance.

Asynchronous version: aprefetch_related_objects()

Prefetches the given lookups on an iterable of model instances. This is useful in code that receives a list of model instances as opposed to a QuerySet; for example, when fetching models from a cache or instantiating them manually.

Pass an iterable of model instances (must all be of the same class and able to be iterated multiple times) and the lookups or Prefetch objects you want to prefetch for. For example:

When using multiple databases with prefetch_related_objects, the prefetch query will use the database associated with the model instance. This can be overridden by using a custom queryset in a related lookup.

The name of the field on which you’d like to filter the relation.

A Q object to control the filtering.

FilteredRelation is used with annotate() to create an ON clause when a JOIN is performed. It doesn’t act on the default relationship but on the annotation name (pizzas_vegetarian in example below).

For example, to find restaurants that have vegetarian pizzas with 'mozzarella' in the name:

If there are a large number of pizzas, this queryset performs better than:

because the filtering in the WHERE clause of the first queryset will only operate on vegetarian pizzas.

FilteredRelation doesn’t support:

QuerySet.only() and prefetch_related().

A GenericForeignKey inherited from a parent model.

---

## Query Expressions¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/expressions/

**Contents:**
- Query Expressions¶
- Supported arithmetic¶
- Output field¶
- Some examples¶
- Built-in Expressions¶
  - F() expressions¶
    - Slicing F() expressions¶
    - Avoiding race conditions using F()¶
    - F() assignments are refreshed after Model.save()¶
    - Using F() in filters¶

Query expressions describe a value or a computation that can be used as part of an update, create, filter, order by, annotation, or aggregate. When an expression outputs a boolean value, it may be used directly in filters. There are a number of built-in expressions (documented below) that can be used to help you write queries. Expressions can be combined, or in some cases nested, to form more complex computations.

Django supports negation, addition, subtraction, multiplication, division, modulo arithmetic, and the power operator on query expressions, using Python constants, variables, and even other expressions.

Many of the expressions documented in this section support an optional output_field parameter. If given, Django will load the value into that field after retrieving it from the database.

output_field takes a model field instance, like IntegerField() or BooleanField(). Usually, the field doesn’t need any arguments, like max_length, since field arguments relate to data validation which will not be performed on the expression’s output value.

output_field is only required when Django is unable to automatically determine the result’s field type, such as complex expressions that mix field types. For example, adding a DecimalField() and a FloatField() requires an output field, like output_field=FloatField().

output_field also allows using custom fields that perform type conversions outside a specific model field context. For example, if you frequently need to perform date arithmetic with timedelta, you can create a custom field that handles the conversion, ensuring consistent results across databases. See How to create custom model fields.

These expressions are defined in django.db.models.expressions and django.db.models.aggregates, but for convenience they’re available and usually imported from django.db.models.

An F() object represents the value of a model field, transformed value of a model field, or annotated column. It makes it possible to refer to model field values and perform database operations using them without actually having to pull them out of the database into Python memory.

Instead, Django uses the F() object to generate an SQL expression that describes the required operation at the database level.

Let’s try this with an example. Normally, one might do something like this:

Here, we have pulled the value of reporter.stories_filed from the database into memory and manipulated it using familiar Python operators, and then saved the object back to the database. But instead we could also have done:

Although reporter.stories_filed = F('stories_filed') + 1 looks like a normal Python assignment of value to an instance attribute, in fact it’s an SQL construct describing an operation on the database.

When Django encounters an instance of F(), it overrides the standard Python operators to create an encapsulated SQL expression; in this case, one which instructs the database to increment the database field represented by reporter.stories_filed.

Whatever value is or was on reporter.stories_filed, Python never gets to know about it - it is dealt with entirely by the database. All Python does, through Django’s F() class, is create the SQL syntax to refer to the field and describe the operation.

As well as being used in operations on single instances as above, F() can be used with update() to perform bulk updates on a QuerySet. This reduces the two queries we were using above - the get() and the save() - to just one:

We can also use update() to increment the field value on multiple objects - which could be very much faster than pulling them all into Python from the database, looping over them, incrementing the field value of each one, and saving each one back to the database:

F() therefore can offer performance advantages by:

getting the database, rather than Python, to do work

reducing the number of queries some operations require

For string-based fields, text-based fields, and ArrayField, you can use Python’s array-slicing syntax. The indices are 0-based. The step argument to slice and negative indexing are not supported. For example:

Another useful benefit of F() is that having the database - rather than Python - update a field’s value avoids a race condition.

If two Python threads execute the code in the first example above, one thread could retrieve, increment, and save a field’s value after the other has retrieved it from the database. The value that the second thread saves will be based on the original value; the work of the first thread will be lost.

If the database is responsible for updating the field, the process is more robust: it will only ever update the field based on the value of the field in the database when the save() or update() is executed, rather than based on its value when the instance was retrieved.

F() objects assigned to model fields are refreshed from the database on save() on backends that support it without incurring a subsequent query (SQLite, PostgreSQL, and Oracle) and deferred otherwise (MySQL or MariaDB). For example:

In previous versions of Django, F() objects were not refreshed from the database on save() which resulted in them being evaluated and persisted every time the instance was saved.

F() is also very useful in QuerySet filters, where they make it possible to filter a set of objects against criteria based on their field values, rather than on Python values.

This is documented in using F() expressions in queries.

F() can be used to create dynamic fields on your models by combining different fields with arithmetic:

If the fields that you’re combining are of different types you’ll need to tell Django what kind of field will be returned. Most expressions support output_field for this case, but since F() does not, you will need to wrap the expression with ExpressionWrapper:

When referencing relational fields such as ForeignKey, F() returns the primary key value rather than a model instance:

Use F() and the nulls_first or nulls_last keyword argument to Expression.asc() or desc() to control the ordering of a field’s null values. By default, the ordering depends on your database.

For example, to sort companies that haven’t been contacted (last_contacted is null) after companies that have been contacted:

F() expressions that output BooleanField can be logically negated with the inversion operator ~F(). For example, to swap the activation status of companies:

Func() expressions are the base type of all expressions that involve database functions like COALESCE and LOWER, or aggregates like SUM. They can be used directly:

or they can be used to build a library of database functions:

But both cases will result in a queryset where each model is annotated with an extra attribute field_lower produced, roughly, from the following SQL:

See Database Functions for a list of built-in database functions.

The Func API is as follows:

A class attribute describing the function that will be generated. Specifically, the function will be interpolated as the function placeholder within template. Defaults to None.

A class attribute, as a format string, that describes the SQL that is generated for this function. Defaults to '%(function)s(%(expressions)s)'.

If you’re constructing SQL like strftime('%W', 'date') and need a literal % character in the query, quadruple it (%%%%) in the template attribute because the string is interpolated twice: once during the template interpolation in as_sql() and once in the SQL interpolation with the query parameters in the database cursor.

A class attribute that denotes the character used to join the list of expressions together. Defaults to ', '.

A class attribute that denotes the number of arguments the function accepts. If this attribute is set and the function is called with a different number of expressions, TypeError will be raised. Defaults to None.

Generates the SQL fragment for the database function. Returns a tuple (sql, params), where sql is the SQL string, and params is the list or tuple of query parameters.

The as_vendor() methods should use the function, template, arg_joiner, and any other **extra_context parameters to customize the SQL as needed. For example:

To avoid an SQL injection vulnerability, extra_context must not contain untrusted user input as these values are interpolated into the SQL string rather than passed as query parameters, where the database driver would escape them.

The *expressions argument is a list of positional expressions that the function will be applied to. The expressions will be converted to strings, joined together with arg_joiner, and then interpolated into the template as the expressions placeholder.

Positional arguments can be expressions or Python values. Strings are assumed to be column references and will be wrapped in F() expressions while other values will be wrapped in Value() expressions.

The **extra kwargs are key=value pairs that can be interpolated into the template attribute. To avoid an SQL injection vulnerability, extra must not contain untrusted user input as these values are interpolated into the SQL string rather than passed as query parameters, where the database driver would escape them.

The function, template, and arg_joiner keywords can be used to replace the attributes of the same name without having to define your own class. output_field can be used to define the expected return type.

Sanitize input used to configure a query expression

Built-in database functions (such as Cast) vary in whether arguments such as output_field can be supplied positionally or only by keyword. For output_field and several other cases, the input ultimately reaches Func() as a keyword argument, so the advice to avoid constructing keyword arguments from untrusted user input applies as equally to these arguments as it does to **extra.

An aggregate expression is a special case of a Func() expression that informs the query that a GROUP BY clause is required. All of the aggregate functions, like Sum() and Count(), inherit from Aggregate().

Since Aggregates are expressions and wrap expressions, you can represent some complex computations:

The Aggregate API is as follows:

A class attribute, as a format string, that describes the SQL that is generated for this aggregate. Defaults to '%(function)s(%(distinct)s%(expressions)s)'.

A class attribute describing the aggregate function that will be generated. Specifically, the function will be interpolated as the function placeholder within template. Defaults to None.

Defaults to True since most aggregate functions can be used as the source expression in Window.

A class attribute determining whether or not this aggregate function allows passing a distinct keyword argument. If set to False (default), TypeError is raised if distinct=True is passed.

A class attribute determining whether or not this aggregate function allows passing a order_by keyword argument. If set to False (default), TypeError is raised if order_by is passed as a value other than None.

Defaults to None since most aggregate functions result in NULL when applied to an empty result set.

The expressions positional arguments can include expressions, transforms of the model field, or the names of model fields. They will be converted to a string and used as the expressions placeholder within the template.

The distinct argument determines whether or not the aggregate function should be invoked for each distinct value of expressions (or set of values, for multiple expressions). The argument is only supported on aggregates that have allow_distinct set to True.

The filter argument takes a Q object that’s used to filter the rows that are aggregated. See Conditional aggregation and Filtering on annotations for example usage.

The order_by argument behaves similarly to the field_names input of the order_by() function, accepting a field name (with an optional "-" prefix which indicates descending order) or an expression (or a tuple or list of strings and/or expressions) that specifies the ordering of the elements in the result.

The default argument takes a value that will be passed along with the aggregate to Coalesce. This is useful for specifying a value to be returned other than None when the queryset (or grouping) contains no entries.

The **extra kwargs are key=value pairs that can be interpolated into the template attribute.

The order_by argument was added.

You can create your own aggregate functions, too. At a minimum, you need to define function, but you can also completely customize the SQL that is generated. Here’s a brief example:

A Value() object represents the smallest possible component of an expression: a simple value. When you need to represent the value of an integer, boolean, or string within an expression, you can wrap that value within a Value().

You will rarely need to use Value() directly. When you write the expression F('field') + 1, Django implicitly wraps the 1 in a Value(), allowing simple values to be used in more complex expressions. You will need to use Value() when you want to pass a string to an expression. Most expressions interpret a string argument as the name of a field, like Lower('name').

The value argument describes the value to be included in the expression, such as 1, True, or None. Django knows how to convert these Python values into their corresponding database type.

If no output_field is specified, it will be inferred from the type of the provided value for many common types. For example, passing an instance of datetime.datetime as value defaults output_field to DateTimeField.

ExpressionWrapper surrounds another expression and provides access to properties, such as output_field, that may not be available on other expressions. ExpressionWrapper is necessary when using arithmetic on F() expressions with different types as described in Using F() with annotations.

Database casting not performed

ExpressionWrapper only sets the output field for the ORM and does not perform any database-level casting. To ensure a specific type is returned from the database, use Cast instead.

Conditional expressions allow you to use if … elif … else logic in queries. Django natively supports SQL CASE expressions. For more details see Conditional Expressions.

You can add an explicit subquery to a QuerySet using the Subquery expression.

For example, to annotate each post with the email address of the author of the newest comment on that post:

On PostgreSQL, the SQL looks like:

The examples in this section are designed to show how to force Django to execute a subquery. In some cases it may be possible to write an equivalent queryset that performs the same task more clearly or efficiently.

Use OuterRef when a queryset in a Subquery needs to refer to a field from the outer query or its transform. It acts like an F expression except that the check to see if it refers to a valid field isn’t made until the outer queryset is resolved.

Instances of OuterRef may be used in conjunction with nested instances of Subquery to refer to a containing queryset that isn’t the immediate parent. For example, this queryset would need to be within a nested pair of Subquery instances to resolve correctly:

There are times when a single column must be returned from a Subquery, for instance, to use a Subquery as the target of an __in lookup. To return all comments for posts published within the last day:

In this case, the subquery must use values() to return only a single column: the primary key of the post.

To prevent a subquery from returning multiple rows, a slice ([:1]) of the queryset is used:

In this case, the subquery must only return a single column and a single row: the email address of the most recently created comment.

(Using get() instead of a slice would fail because the OuterRef cannot be resolved until the queryset is used within a Subquery.)

Exists is a Subquery subclass that uses an SQL EXISTS statement. In many cases it will perform better than a subquery since the database is able to stop evaluation of the subquery when a first matching row is found.

For example, to annotate each post with whether or not it has a comment from within the last day:

On PostgreSQL, the SQL looks like:

It’s unnecessary to force Exists to refer to a single column, since the columns are discarded and a boolean result is returned. Similarly, since ordering is unimportant within an SQL EXISTS subquery and would only degrade performance, it’s automatically removed.

You can query using NOT EXISTS with ~Exists().

Subquery() that returns a boolean value and Exists() may be used as a condition in When expressions, or to directly filter a queryset:

This will ensure that the subquery will not be added to the SELECT columns, which may result in a better performance.

Aggregates may be used within a Subquery, but they require a specific combination of filter(), values(), and annotate() to get the subquery grouping correct.

Assuming both models have a length field, to find posts where the post length is greater than the total length of all combined comments:

The initial filter(...) limits the subquery to the relevant parameters. order_by() removes the default ordering (if any) on the Comment model. values('post') aggregates comments by Post. Finally, annotate(...) performs the aggregation. The order in which these queryset methods are applied is important. In this case, since the subquery must be limited to a single column, values('total') is required.

This is the only way to perform an aggregation within a Subquery, as using aggregate() attempts to evaluate the queryset (and if there is an OuterRef, this will not be possible to resolve).

Sometimes database expressions can’t easily express a complex WHERE clause. In these edge cases, use the RawSQL expression. For example:

These extra lookups may not be portable to different database engines (because you’re explicitly writing SQL code) and violate the DRY principle, so you should avoid them if possible.

RawSQL expressions can also be used as the target of __in filters:

To protect against SQL injection attacks, you must escape any parameters that the user can control by using params. params is a required argument to force you to acknowledge that you’re not interpolating your SQL with user-provided data.

You also must not quote placeholders in the SQL string. This example is vulnerable to SQL injection because of the quotes around %s:

You can read more about how Django’s SQL injection protection works.

Window functions provide a way to apply functions on partitions. Unlike a normal aggregation function which computes a final result for each set defined by the group by, window functions operate on frames and partitions, and compute the result for each row.

You can specify multiple windows in the same query which in Django ORM would be equivalent to including multiple expressions in a QuerySet.annotate() call. The ORM doesn’t make use of named windows, instead they are part of the selected columns.

Defaults to %(expression)s OVER (%(window)s). If only the expression argument is provided, the window clause will be blank.

The Window class is the main expression for an OVER clause.

The expression argument is either a window function, an aggregate function, or an expression that’s compatible in a window clause.

The partition_by argument accepts an expression or a sequence of expressions (column names should be wrapped in an F-object) that control the partitioning of the rows. Partitioning narrows which rows are used to compute the result set.

The output_field is specified either as an argument or by the expression.

The order_by argument accepts an expression on which you can call asc() and desc(), a string of a field name (with an optional "-" prefix which indicates descending order), or a tuple or list of strings and/or expressions. The ordering controls the order in which the expression is applied. For example, if you sum over the rows in a partition, the first result is the value of the first row, the second is the sum of first and second row.

The frame parameter specifies which other rows that should be used in the computation. See Frames for details.

For example, to annotate each movie with the average rating for the movies by the same studio in the same genre and release year:

This allows you to check if a movie is rated better or worse than its peers.

You may want to apply multiple expressions over the same window, i.e., the same partition and frame. For example, you could modify the previous example to also include the best and worst rating in each movie’s group (same studio, genre, and release year) by using three window functions in the same query. The partition and ordering from the previous example is extracted into a dictionary to reduce repetition:

Filtering against window functions is supported as long as lookups are not disjunctive (not using OR or XOR as a connector) and against a queryset performing aggregation.

For example, a query that relies on aggregation and has an OR-ed filter against a window function and a field is not supported. Applying combined predicates post-aggregation could cause rows that would normally be excluded from groups to be included:

Among Django’s built-in database backends, MySQL, PostgreSQL, and Oracle support window expressions. Support for different window expression features varies among the different databases. For example, the options in asc() and desc() may not be supported. Consult the documentation for your database as needed.

For a window frame, you can choose either a range-based sequence of rows or an ordinary sequence of rows.

This attribute is set to 'RANGE'.

PostgreSQL has limited support for ValueRange and only supports use of the standard start and end points, such as CURRENT ROW and UNBOUNDED FOLLOWING.

This attribute is set to 'ROWS'.

Both classes return SQL with the template:

The exclusion argument allows excluding rows (CURRENT_ROW), groups (GROUP), and ties (TIES) from the window frames on supported databases:

Frames narrow the rows that are used for computing the result. They shift from some start point to some specified end point. Frames can be used with and without partitions, but it’s often a good idea to specify an ordering of the window to ensure a deterministic result. In a frame, a peer in a frame is a row with an equivalent value, or all rows if an ordering clause isn’t present.

The default starting point for a frame is UNBOUNDED PRECEDING which is the first row of the partition. The end point is always explicitly included in the SQL generated by the ORM and is by default UNBOUNDED FOLLOWING. The default frame includes all rows from the partition to the last row in the set.

The accepted values for the start and end arguments are None, an integer, or zero. A negative integer for start results in N PRECEDING, while None yields UNBOUNDED PRECEDING. In ROWS mode, a positive integer can be used for start resulting in N FOLLOWING. Positive integers are accepted for end and results in N FOLLOWING. In ROWS mode, a negative integer can be used for end resulting in N PRECEDING. For both start and end, zero will return CURRENT ROW.

There’s a difference in what CURRENT ROW includes. When specified in ROWS mode, the frame starts or ends with the current row. When specified in RANGE mode, the frame starts or ends at the first or last peer according to the ordering clause. Thus, RANGE CURRENT ROW evaluates the expression for rows which have the same value specified by the ordering. Because the template includes both the start and end points, this may be expressed with:

If a movie’s “peers” are described as movies released by the same studio in the same genre in the same year, this RowRange example annotates each movie with the average rating of a movie’s two prior and two following peers:

If the database supports it, you can specify the start and end points based on values of an expression in the partition. If the released field of the Movie model stores the release month of each movie, this ValueRange example annotates each movie with the average rating of a movie’s peers released between twelve months before and twelve months after each movie:

Below you’ll find technical implementation details that may be useful to library authors. The technical API and examples below will help with creating generic query expressions that can extend the built-in functionality that Django provides.

Query expressions implement the query expression API, but also expose a number of extra methods and attributes listed below. All query expressions must inherit from Expression() or a relevant subclass.

When a query expression wraps another expression, it is responsible for calling the appropriate methods on the wrapped expression.

Tells Django that this expression can be used in Field.db_default. Defaults to False.

Tells Django that this expression can be used during a constraint validation. Expressions with constraint_validation_compatible set to False must have only one source expression. Defaults to True.

Tells Django that this expression contains an aggregate and that a GROUP BY clause needs to be added to the query.

Tells Django that this expression contains a Window expression. It’s used, for example, to disallow window function expressions in queries that modify data.

Tells Django that this expression can be referenced in QuerySet.filter(). Defaults to True.

Tells Django that this expression can be used as the source expression in Window. Defaults to False.

Tells Django which value should be returned when the expression is used to apply a function over an empty result set. Defaults to NotImplemented which forces the expression to be computed on the database.

Tells Django that this expression contains a set-returning function, enforcing subquery evaluation. It’s used, for example, to allow some Postgres set-returning functions (e.g. JSONB_PATH_QUERY, UNNEST, etc.) to skip optimization and be properly evaluated when annotations spawn rows themselves. Defaults to False.

Tells Django that this expression allows composite expressions, for example, to support composite primary keys. Defaults to False.

Provides the chance to do any preprocessing or validation of the expression before it’s added to the query. resolve_expression() must also be called on any nested expressions. A copy() of self should be returned with any necessary transformations.

query is the backend query implementation.

allow_joins is a boolean that allows or denies the use of joins in the query.

reuse is a set of reusable joins for multi-join scenarios.

summarize is a boolean that, when True, signals that the query being computed is a terminal aggregate query.

for_save is a boolean that, when True, signals that the query being executed is performing a create or update.

Returns an ordered list of inner expressions. For example:

Takes a list of expressions and stores them such that get_source_expressions() can return them.

Returns a clone (copy) of self, with any column aliases relabeled. Column aliases are renamed when subqueries are created. relabeled_clone() should also be called on any nested expressions and assigned to the clone.

change_map is a dictionary mapping old aliases to new aliases.

A hook allowing the expression to coerce value into a more appropriate type.

expression is the same as self.

Responsible for returning the list of columns references by this expression. get_group_by_cols() should be called on any nested expressions. F() objects, in particular, hold a reference to a column.

Returns the expression ready to be sorted in ascending order.

nulls_first and nulls_last define how null values are sorted. See Using F() to sort null values for example usage.

Returns the expression ready to be sorted in descending order.

nulls_first and nulls_last define how null values are sorted. See Using F() to sort null values for example usage.

Returns self with any modifications required to reverse the sort order within an order_by call. As an example, an expression implementing NULLS LAST would change its value to be NULLS FIRST. Modifications are only required for expressions that implement sort order like OrderBy. This method is called when reverse() is called on a queryset.

You can write your own query expression classes that use, and can integrate with, other query expressions. Let’s step through an example by writing an implementation of the COALESCE SQL function, without using the built-in Func() expressions.

The COALESCE SQL function is defined as taking a list of columns or values. It will return the first column or value that isn’t NULL.

We’ll start by defining the template to be used for SQL generation and an __init__() method to set some attributes:

We do some basic validation on the parameters, including requiring at least 2 columns or values, and ensuring they are expressions. We are requiring output_field here so that Django knows what kind of model field to assign the eventual result to.

Now we implement the preprocessing and validation. Since we do not have any of our own validation at this point, we delegate to the nested expressions:

Next, we write the method responsible for generating the SQL:

as_sql() methods can support custom keyword arguments, allowing as_vendorname() methods to override data used to generate the SQL string. Using as_sql() keyword arguments for customization is preferable to mutating self within as_vendorname() methods as the latter can lead to errors when running on different database backends. If your class relies on class attributes to define data, consider allowing overrides in your as_sql() method.

We generate the SQL for each of the expressions by using the compiler.compile() method, and join the result together with commas. Then the template is filled out with our data and the SQL and parameters are returned.

We’ve also defined a custom implementation that is specific to the Oracle backend. The as_oracle() function will be called instead of as_sql() if the Oracle backend is in use.

Finally, we implement the rest of the methods that allow our query expression to play nice with other query expressions:

Let’s see how it works:

Since a Func’s keyword arguments for __init__() (**extra) and as_sql() (**extra_context) are interpolated into the SQL string rather than passed as query parameters (where the database driver would escape them), they must not contain untrusted user input.

For example, if substring is user-provided, this function is vulnerable to SQL injection:

This function generates an SQL string without any parameters. Since substring is passed to super().__init__() as a keyword argument, it’s interpolated into the SQL string before the query is sent to the database.

Here’s a corrected rewrite:

With substring instead passed as a positional argument, it’ll be passed as a parameter in the database query.

If you’re using a database backend that uses a different SQL syntax for a certain function, you can add support for it by monkey patching a new method onto the function’s class.

Let’s say we’re writing a backend for Microsoft’s SQL Server which uses the SQL LEN instead of LENGTH for the Length function. We’ll monkey patch a new method called as_sqlserver() onto the Length class:

You can also customize the SQL using the template parameter of as_sql().

We use as_sqlserver() because django.db.connection.vendor returns sqlserver for the backend.

Third-party backends can register their functions in the top level __init__.py file of the backend package or in a top level expressions.py file (or package) that is imported from the top level __init__.py.

For user projects wishing to patch the backend that they’re using, this code should live in an AppConfig.ready() method.

---

## Related objects reference¶

**URL:** https://docs.djangoproject.com/en/stable/ref/models/relations/

**Contents:**
- Related objects reference¶

A “related manager” is a manager used in a one-to-many or many-to-many related context. This happens in two cases:

The “other side” of a ForeignKey relation. That is:

In the above example, the methods below will be available on the manager blog.entry_set.

Both sides of a ManyToManyField relation

In this example, the methods below will be available both on topping.pizza_set and on pizza.toppings.

Asynchronous version: aadd

Adds the specified model objects to the related object set.

In the example above, in the case of a ForeignKey relationship, QuerySet.update() is used to perform the update. This requires the objects to already be saved.

You can use the bulk=False argument to instead have the related manager perform the update by calling e.save().

Using add() with a many-to-many relationship, however, will not call any save() methods (the bulk argument doesn’t exist), but rather create the relationships using QuerySet.bulk_create(). If you need to execute some custom logic when a relationship is created, listen to the m2m_changed signal, which will trigger pre_add and post_add actions.

Using add() on a relation that already exists won’t duplicate the relation, but it will still trigger signals.

For many-to-many relationships add() accepts either model instances or field values, normally primary keys, as the *objs argument.

Use the through_defaults argument to specify values for the new intermediate model instance(s), if needed. You can use callables as values in the through_defaults dictionary and they will be evaluated once before creating any intermediate instance(s).

Asynchronous version: acreate

Creates a new object, saves it and puts it in the related object set. Returns the newly created object:

This is equivalent to (but simpler than):

Note that there’s no need to specify the keyword argument of the model that defines the relationship. In the above example, we don’t pass the parameter blog to create(). Django figures out that the new Entry object’s blog field should be set to b.

Use the through_defaults argument to specify values for the new intermediate model instance, if needed. You can use callables as values in the through_defaults dictionary.

Asynchronous version: aremove

Removes the specified model objects from the related object set:

Similar to add(), e.save() is called in the example above to perform the update. Using remove() with a many-to-many relationship, however, will delete the relationships using QuerySet.delete() which means no model save() methods are called; listen to the m2m_changed signal if you wish to execute custom code when a relationship is deleted.

For many-to-many relationships remove() accepts either model instances or field values, normally primary keys, as the *objs argument.

For ForeignKey objects, this method only exists if null=True. If the related field can’t be set to None (NULL), then an object can’t be removed from a relation without being added to another. In the above example, removing e from b.entry_set() is equivalent to doing e.blog = None, and because the blog ForeignKey doesn’t have null=True, this is invalid.

For ForeignKey objects, this method accepts a bulk argument to control how to perform the operation. If True (the default), QuerySet.update() is used. If bulk=False, the save() method of each individual model instance is called instead. This triggers the pre_save and post_save signals and comes at the expense of performance.

For many-to-many relationships, the bulk keyword argument doesn’t exist.

Asynchronous version: aclear

Removes all objects from the related object set:

Note this doesn’t delete the related objects – it just disassociates them.

Just like remove(), clear() is only available on ForeignKeys where null=True and it also accepts the bulk keyword argument.

For many-to-many relationships, the bulk keyword argument doesn’t exist.

Asynchronous version: aset

Replace the set of related objects:

This method accepts a clear argument to control how to perform the operation. If False (the default), the elements missing from the new set are removed using remove() and only the new ones are added. If clear=True, the clear() method is called instead and the whole set is added at once.

For ForeignKey objects, the bulk argument is passed on to add() and remove().

For many-to-many relationships, the bulk keyword argument doesn’t exist.

Note that since set() is a compound operation, it is subject to race conditions. For instance, new objects may be added to the database in between the call to clear() and the call to add().

For many-to-many relationships set() accepts a list of either model instances or field values, normally primary keys, as the objs argument.

Use the through_defaults argument to specify values for the new intermediate model instance(s), if needed. You can use callables as values in the through_defaults dictionary and they will be evaluated once before creating any intermediate instance(s).

Note that add(), aadd(), create(), acreate(), remove(), aremove(), clear(), aclear(), set(), and aset() all apply database changes immediately for all types of related fields. In other words, there is no need to call save()/asave() on either end of the relationship.

If you use prefetch_related(), the add(), aadd(), remove(), aremove(), clear(), aclear(), set(), and aset() methods clear the prefetched cache.

---

## Request and response objects¶

**URL:** https://docs.djangoproject.com/en/stable/ref/request-response/

**Contents:**
- Request and response objects¶
- Quick overview¶
- HttpRequest objects¶
  - Attributes¶
  - Attributes set by application code¶
  - Attributes set by middleware¶
  - Methods¶
- QueryDict objects¶
  - Methods¶
- HttpResponse objects¶

Django uses request and response objects to pass state through the system.

When a page is requested, Django creates an HttpRequest object that contains metadata about the request. Then Django loads the appropriate view, passing the HttpRequest as the first argument to the view function. Each view is responsible for returning an HttpResponse object.

This document explains the APIs for HttpRequest and HttpResponse objects, which are defined in the django.http module.

All attributes should be considered read-only, unless stated otherwise.

A string representing the scheme of the request (http or https usually).

The raw HTTP request body as a bytestring. This is useful for processing data in different ways than conventional HTML forms: binary images, XML payload etc. For processing conventional form data, use HttpRequest.POST.

You can also read from an HttpRequest using a file-like interface with HttpRequest.read() or HttpRequest.readline(). Accessing the body attribute after reading the request with either of these I/O stream methods will produce a RawPostDataException.

A string representing the full path to the requested page, not including the scheme, domain, or query string.

Example: "/music/bands/the_beatles/"

Under some web server configurations, the portion of the URL after the host name is split up into a script prefix portion and a path info portion. The path_info attribute always contains the path info portion of the path, no matter what web server is being used. Using this instead of path can make your code easier to move between test and deployment servers.

For example, if the WSGIScriptAlias for your application is set to "/minfo", then path might be "/minfo/music/bands/the_beatles/" and path_info would be "/music/bands/the_beatles/".

A string representing the HTTP method used in the request. This is guaranteed to be uppercase. For example:

A string representing the current encoding used to decode form submission data (or None, which means the DEFAULT_CHARSET setting is used). You can write to this attribute to change the encoding used when accessing the form data. Any subsequent attribute accesses (such as reading from GET or POST) will use the new encoding value. Useful if you know the form data is not in the DEFAULT_CHARSET encoding.

A string representing the MIME type of the request, parsed from the CONTENT_TYPE header.

A dictionary of key/value parameters included in the CONTENT_TYPE header.

A dictionary-like object containing all given HTTP GET parameters. See the QueryDict documentation below.

A dictionary-like object containing all given HTTP POST parameters, providing that the request contains form data. See the QueryDict documentation below. If you need to access raw or non-form data posted in the request, access this through the HttpRequest.body attribute instead.

It’s possible that a request can come in via POST with an empty POST dictionary – if, say, a form is requested via the POST HTTP method but does not include form data. Therefore, you shouldn’t use if request.POST to check for use of the POST method; instead, use if request.method == "POST" (see HttpRequest.method).

POST does not include file-upload information. See FILES.

A dictionary containing all cookies. Keys and values are strings.

A dictionary-like object containing all uploaded files. Each key in FILES is the name from the <input type="file" name="">. Each value in FILES is an UploadedFile.

See Managing files for more information.

FILES will only contain data if the request method was POST and the <form> that posted to the request had enctype="multipart/form-data". Otherwise, FILES will be a blank dictionary-like object.

A dictionary containing all available HTTP headers. Available headers depend on the client and server, but here are some examples:

CONTENT_LENGTH – The length of the request body (as a string).

CONTENT_TYPE – The MIME type of the request body.

HTTP_ACCEPT – Acceptable content types for the response.

HTTP_ACCEPT_ENCODING – Acceptable encodings for the response.

HTTP_ACCEPT_LANGUAGE – Acceptable languages for the response.

HTTP_HOST – The HTTP Host header sent by the client.

HTTP_REFERER – The referring page, if any.

HTTP_USER_AGENT – The client’s user-agent string.

QUERY_STRING – The query string, as a single (unparsed) string.

REMOTE_ADDR – The IP address of the client.

REMOTE_HOST – The hostname of the client.

REMOTE_USER – The user authenticated by the web server, if any.

REQUEST_METHOD – A string such as "GET" or "POST".

SERVER_NAME – The hostname of the server.

SERVER_PORT – The port of the server (as a string).

With the exception of CONTENT_LENGTH and CONTENT_TYPE, as given above, any HTTP headers in the request are converted to META keys by converting all characters to uppercase, replacing any hyphens with underscores and adding an HTTP_ prefix to the name. So, for example, a header called X-Bender would be mapped to the META key HTTP_X_BENDER.

Note that runserver strips all headers with underscores in the name, so you won’t see them in META. This prevents header-spoofing based on ambiguity between underscores and dashes both being normalizing to underscores in WSGI environment variables. It matches the behavior of web servers like Nginx and Apache 2.4+.

HttpRequest.headers is a simpler way to access all HTTP-prefixed headers, plus CONTENT_LENGTH and CONTENT_TYPE.

A case insensitive, dict-like object that provides access to all HTTP-prefixed headers (plus Content-Length and Content-Type) from the request.

The name of each header is stylized with title-casing (e.g. User-Agent) when it’s displayed. You can access headers case-insensitively:

For use in, for example, Django templates, headers can also be looked up using underscores in place of hyphens:

An instance of ResolverMatch representing the resolved URL. This attribute is only set after URL resolving took place, which means it’s available in all views but not in middleware which are executed before URL resolving takes place (you can use it in process_view() though).

Django doesn’t set these attributes itself but makes use of them if set by your application.

The url template tag will use its value as the current_app argument to reverse().

This will be used as the root URLconf for the current request, overriding the ROOT_URLCONF setting. See How Django processes a request for details.

urlconf can be set to None to revert any changes made by previous middleware and return to using the ROOT_URLCONF.

This will be used instead of DEFAULT_EXCEPTION_REPORTER_FILTER for the current request. See Custom error reports for details.

This will be used instead of DEFAULT_EXCEPTION_REPORTER for the current request. See Custom error reports for details.

Some of the middleware included in Django’s contrib apps set attributes on the request. If you don’t see the attribute on a request, be sure the appropriate middleware class is listed in MIDDLEWARE.

From the SessionMiddleware: A readable and writable, dictionary-like object that represents the current session.

From the CurrentSiteMiddleware: An instance of Site or RequestSite as returned by get_current_site() representing the current site.

From the AuthenticationMiddleware: An instance of AUTH_USER_MODEL representing the currently logged-in user. If the user isn’t currently logged in, user will be set to an instance of AnonymousUser. You can tell them apart with is_authenticated, like so:

The auser() method does the same thing but can be used from async contexts.

From the AuthenticationMiddleware: Coroutine. Returns an instance of AUTH_USER_MODEL representing the currently logged-in user. If the user isn’t currently logged in, auser will return an instance of AnonymousUser. This is similar to the user attribute but it works in async contexts.

Returns the originating host of the request using information from the HTTP_X_FORWARDED_HOST (if USE_X_FORWARDED_HOST is enabled) and HTTP_HOST headers, in that order. If they don’t provide a value, the method uses a combination of SERVER_NAME and SERVER_PORT as detailed in PEP 3333.

Example: "127.0.0.1:8000"

Raises django.core.exceptions.DisallowedHost if the host is not in ALLOWED_HOSTS or the domain name is invalid according to RFC 1034/1035.

The get_host() method fails when the host is behind multiple proxies. One solution is to use middleware to rewrite the proxy headers, as in the following example:

This middleware should be positioned before any other middleware that relies on the value of get_host() – for instance, CommonMiddleware or CsrfViewMiddleware.

Returns the originating port of the request using information from the HTTP_X_FORWARDED_PORT (if USE_X_FORWARDED_PORT is enabled) and SERVER_PORT META variables, in that order.

Returns the path, plus an appended query string, if applicable.

Example: "/minfo/music/bands/the_beatles/?print=true"

Like get_full_path(), but uses path_info instead of path.

Example: "/music/bands/the_beatles/?print=true"

Returns the absolute URI form of location. If no location is provided, the location will be set to request.get_full_path().

If the location is already an absolute URI, it will not be altered. Otherwise the absolute URI is built using the server variables available in this request. For example:

Mixing HTTP and HTTPS on the same site is discouraged, therefore build_absolute_uri() will always generate an absolute URI with the same scheme the current request has. If you need to redirect users to HTTPS, it’s best to let your web server redirect all HTTP traffic to HTTPS.

Returns a cookie value for a signed cookie, or raises a django.core.signing.BadSignature exception if the signature is no longer valid. If you provide the default argument the exception will be suppressed and that default value will be returned instead.

The optional salt argument can be used to provide extra protection against brute force attacks on your secret key. If supplied, the max_age argument will be checked against the signed timestamp attached to the cookie value to ensure the cookie is not older than max_age seconds.

See cryptographic signing for more information.

Returns True if the request is secure; that is, if it was made with HTTPS.

Returns the preferred mime type from media_types, based on the Accept header, or None if the client does not accept any of the provided types.

Assuming the client sends an Accept header of text/html,application/json;q=0.8:

If the mime type includes parameters, these are also considered when determining the preferred media type. For example, with an Accept header of text/vcard;version=3.0,text/html;q=0.5, the return value of request.get_preferred_type() depends on the available media types:

(For further details on how content negotiation is performed, see RFC 9110 Section 12.5.1.)

Most browsers send Accept: */* by default, meaning they don’t have a preference, in which case the first item in media_types would be returned.

Setting an explicit Accept header in API requests can be useful for returning a different content type for those consumers only. See Content negotiation example for an example of returning different content based on the Accept header.

If a response varies depending on the content of the Accept header and you are using some form of caching like Django’s cache middleware, you should decorate the view with vary_on_headers('Accept') so that the responses are properly cached.

Returns True if the request’s Accept header matches the mime_type argument:

Most browsers send Accept: */* by default, so this would return True for all content types.

See Content negotiation example for an example of using accepts() to return different content based on the Accept header.

Methods implementing a file-like interface for reading from an HttpRequest instance. This makes it possible to consume an incoming request in a streaming fashion. A common use-case would be to process a big XML payload with an iterative parser without constructing a whole XML tree in memory.

Given this standard interface, an HttpRequest instance can be passed directly to an XML parser such as ElementTree:

In an HttpRequest object, the GET and POST attributes are instances of django.http.QueryDict, a dictionary-like class customized to deal with multiple values for the same key. This is necessary because some HTML form elements, notably <select multiple>, pass multiple values for the same key.

The QueryDicts at request.POST and request.GET will be immutable when accessed in a normal request/response cycle. To get a mutable version you need to use QueryDict.copy().

QueryDict implements all the standard dictionary methods because it’s a subclass of dictionary. Exceptions are outlined here:

Instantiates a QueryDict object based on query_string.

If query_string is not passed in, the resulting QueryDict will be empty (it will have no keys or values).

Most QueryDicts you encounter, and in particular those at request.POST and request.GET, will be immutable. If you are instantiating one yourself, you can make it mutable by passing mutable=True to its __init__().

Strings for setting both keys and values will be converted from encoding to str. If encoding is not set, it defaults to DEFAULT_CHARSET.

Creates a new QueryDict with keys from iterable and each value equal to value. For example:

Returns the last value for the given key; or an empty list ([]) if the key exists but has no values. Raises django.utils.datastructures.MultiValueDictKeyError if the key does not exist. (This is a subclass of Python’s standard KeyError, so you can stick to catching KeyError.)

Sets the given key to [value] (a list whose single element is value). Note that this, as other dictionary functions that have side effects, can only be called on a mutable QueryDict (such as one that was created via QueryDict.copy()).

Returns True if the given key is set. This lets you do, e.g., if "foo" in request.GET.

Uses the same logic as __getitem__(), with a hook for returning a default value if the key doesn’t exist.

Like dict.setdefault(), except it uses __setitem__() internally.

Takes either a QueryDict or a dictionary. Like dict.update(), except it appends to the current dictionary items rather than replacing them. For example:

Like dict.items(), except this uses the same last-value logic as __getitem__() and returns an iterator object instead of a view object. For example:

Like dict.values(), except this uses the same last-value logic as __getitem__() and returns an iterator instead of a view object. For example:

In addition, QueryDict has the following methods:

Returns a copy of the object using copy.deepcopy(). This copy will be mutable even if the original was not.

Returns a list of the data with the requested key. Returns an empty list if the key doesn’t exist and default is None. It’s guaranteed to return a list unless the default value provided isn’t a list.

Sets the given key to list_ (unlike __setitem__()).

Appends an item to the internal list associated with key.

Like setdefault(), except it takes a list of values instead of a single value.

Like items(), except it includes all values, as a list, for each member of the dictionary. For example:

Returns a list of values for the given key and removes them from the dictionary. Raises KeyError if the key does not exist. For example:

Removes an arbitrary member of the dictionary (since there’s no concept of ordering), and returns a two value tuple containing the key and a list of all values for the key. Raises KeyError when called on an empty dictionary. For example:

Returns a dict representation of QueryDict. For every (key, list) pair in QueryDict, dict will have (key, item), where item is one element of the list, using the same logic as QueryDict.__getitem__():

Returns a string of the data in query string format. For example:

Use the safe parameter to pass characters which don’t require encoding. For example:

In contrast to HttpRequest objects, which are created automatically by Django, HttpResponse objects are your responsibility. Each view you write is responsible for instantiating, populating, and returning an HttpResponse.

The HttpResponse class lives in the django.http module.

Typical usage is to pass the contents of the page, as a string, bytestring, or memoryview, to the HttpResponse constructor:

But if you want to add content incrementally, you can use response as a file-like object:

Finally, you can pass HttpResponse an iterator rather than strings. HttpResponse will consume the iterator immediately, store its content as a string, and discard it. Objects with a close() method such as files and generators are immediately closed.

If you need the response to be streamed from the iterator to the client, you must use the StreamingHttpResponse class instead.

To set or remove a header field in your response, use HttpResponse.headers:

You can also manipulate headers by treating your response like a dictionary:

This proxies to HttpResponse.headers, and is the original interface offered by HttpResponse.

When using this interface, unlike a dictionary, del doesn’t raise KeyError if the header field doesn’t exist.

You can also set headers on instantiation:

For setting the Cache-Control and Vary header fields, it is recommended to use the patch_cache_control() and patch_vary_headers() methods from django.utils.cache, since these fields can have multiple, comma-separated values. The “patch” methods ensure that other values, e.g. added by a middleware, are not removed.

HTTP header fields cannot contain newlines. An attempt to set a header field containing a newline character (CR or LF) will raise BadHeaderError

To tell the browser to treat the response as a file attachment, set the Content-Type and Content-Disposition headers. For example, this is how you might return a Microsoft Excel spreadsheet:

There’s nothing Django-specific about the Content-Disposition header, but it’s easy to forget the syntax, so we’ve included it here.

A bytestring representing the content, encoded from a string if necessary.

A string representation of HttpResponse.content, decoded using the response’s HttpResponse.charset (defaulting to UTF-8 if empty).

A http.cookies.SimpleCookie object holding the cookies included in the response.

A case insensitive, dict-like object that provides an interface to all HTTP headers on the response, except a Set-Cookie header. See Setting header fields and HttpResponse.cookies.

A string denoting the charset in which the response will be encoded. If not given at HttpResponse instantiation time, it will be extracted from content_type and if that is unsuccessful, the DEFAULT_CHARSET setting will be used.

The HTTP status code for the response.

Unless reason_phrase is explicitly set, modifying the value of status_code outside the constructor will also modify the value of reason_phrase.

The HTTP reason phrase for the response. It uses the HTTP standard’s default reason phrases.

Unless explicitly set, reason_phrase is determined by the value of status_code.

This is always False.

This attribute exists so middleware can treat streaming responses differently from regular responses.

True if the response has been closed.

Instantiates an HttpResponse object with the given page content, content type, and headers.

content is most commonly an iterator, bytestring, memoryview, or string. Other types will be converted to a bytestring by encoding their string representation. Iterators should return strings or bytestrings and those will be joined together to form the content of the response.

content_type is the MIME type optionally completed by a character set encoding and is used to fill the HTTP Content-Type header. If not specified, it is formed by 'text/html' and the DEFAULT_CHARSET settings, by default: "text/html; charset=utf-8".

status is the HTTP status code for the response. You can use Python’s http.HTTPStatus for meaningful aliases, such as HTTPStatus.NO_CONTENT.

reason is the HTTP response phrase. If not provided, a default phrase will be used.

charset is the charset in which the response will be encoded. If not given it will be extracted from content_type, and if that is unsuccessful, the DEFAULT_CHARSET setting will be used.

headers is a dict of HTTP headers for the response.

Sets the given header name to the given value. Both header and value should be strings.

Deletes the header with the given name. Fails silently if the header doesn’t exist. Case-insensitive.

Returns the value for the given header name. Case-insensitive.

Returns the value for the given header, or an alternate if the header doesn’t exist.

Returns True or False based on a case-insensitive check for a header with the given name.

Acts like dict.items() for HTTP headers on the response.

Sets a header unless it has already been set.

Sets a cookie. The parameters are the same as in the Morsel cookie object in the Python standard library.

max_age should be a timedelta object, an integer number of seconds, or None (default) if the cookie should last only as long as the client’s browser session. If expires is not specified, it will be calculated.

expires should either be a string in the format "Wdy, DD-Mon-YY HH:MM:SS GMT" or a datetime.datetime object in UTC. If expires is a datetime object, the max_age will be calculated.

Use domain if you want to set a cross-domain cookie. For example, domain="example.com" will set a cookie that is readable by the domains www.example.com, blog.example.com, etc. Otherwise, a cookie will only be readable by the domain that set it.

Use secure=True if you want the cookie to be only sent to the server when a request is made with the https scheme.

Use httponly=True if you want to prevent client-side JavaScript from having access to the cookie.

HttpOnly is a flag included in a Set-Cookie HTTP response header. It’s part of the RFC 6265 standard for cookies and can be a useful way to mitigate the risk of a client-side script accessing the protected cookie data.

Use samesite='Strict' or samesite='Lax' to tell the browser not to send this cookie when performing a cross-origin request. SameSite isn’t supported by all browsers, so it’s not a replacement for Django’s CSRF protection, but rather a defense in depth measure.

Use samesite='None' (string) to explicitly state that this cookie is sent with all same-site and cross-site requests.

RFC 6265 states that user agents should support cookies of at least 4096 bytes. For many browsers this is also the maximum size. Django will not raise an exception if there’s an attempt to store a cookie of more than 4096 bytes, but many browsers will not set the cookie correctly.

Like set_cookie(), but cryptographic signing the cookie before setting it. Use in conjunction with HttpRequest.get_signed_cookie(). You can use the optional salt argument for added key strength, but you will need to remember to pass it to the corresponding HttpRequest.get_signed_cookie() call.

Deletes the cookie with the given key. Fails silently if the key doesn’t exist.

Due to the way cookies work, path and domain should be the same values you used in set_cookie() – otherwise the cookie may not be deleted.

This method is called at the end of the request directly by the WSGI or ASGI server.

This method makes an HttpResponse instance a file-like object.

This method makes an HttpResponse instance a file-like object.

This method makes an HttpResponse instance a file-like object.

Returns the value of HttpResponse.content. This method makes an HttpResponse instance a stream-like object.

Always False. This method makes an HttpResponse instance a stream-like object.

Always False. This method makes an HttpResponse instance a stream-like object.

Always True. This method makes an HttpResponse instance a stream-like object.

Writes a list of lines to the response. Line separators are not added. This method makes an HttpResponse instance a stream-like object.

Django includes a number of HttpResponse subclasses that handle different types of HTTP responses. Like HttpResponse, these subclasses live in django.http.

The first argument to the constructor is required – the path to redirect to. This can be a fully qualified URL (e.g. 'https://www.yahoo.com/search/'), an absolute path with no domain (e.g. '/search/'), or even a relative path (e.g. 'search/'). In that last case, the client browser will reconstruct the full URL itself according to the current path.

The constructor accepts an optional preserve_request keyword argument that defaults to False, producing a response with a 302 status code. If preserve_request is True, the status code will be 307 instead.

See HttpResponse for other optional constructor arguments.

This read-only attribute represents the URL the response will redirect to (equivalent to the Location response header).

The preserve_request argument was added.

Like HttpResponseRedirect, but it returns a permanent redirect (HTTP status code 301) instead of a “found” redirect (status code 302). When preserve_request=True, the response’s status code is 308.

The preserve_request argument was added.

The constructor doesn’t take any arguments and no content should be added to this response. Use this to designate that a page hasn’t been modified since the user’s last request (status code 304).

Acts just like HttpResponse but uses a 400 status code.

Acts just like HttpResponse but uses a 404 status code.

Acts just like HttpResponse but uses a 403 status code.

Like HttpResponse, but uses a 405 status code. The first argument to the constructor is required: a list of permitted methods (e.g. ['GET', 'POST']).

Acts just like HttpResponse but uses a 410 status code.

Acts just like HttpResponse but uses a 500 status code.

If a custom subclass of HttpResponse implements a render method, Django will treat it as emulating a SimpleTemplateResponse, and the render method must itself return a valid response object.

If you find yourself needing a response class that Django doesn’t provide, you can create it with the help of http.HTTPStatus. For example:

An HttpResponse subclass that helps to create a JSON-encoded response. It inherits most behavior from its superclass with a couple differences:

Its default Content-Type header is set to application/json.

The first parameter, data, should be a dict instance. If the safe parameter is set to False (see below) it can be any JSON-serializable object.

The encoder, which defaults to django.core.serializers.json.DjangoJSONEncoder, will be used to serialize the data. See JSON serialization for more details about this serializer.

The safe boolean parameter defaults to True. If it’s set to False, any object can be passed for serialization (otherwise only dict instances are allowed). If safe is True and a non-dict object is passed as the first argument, a TypeError will be raised.

The json_dumps_params parameter is a dictionary of keyword arguments to pass to the json.dumps() call used to generate the response.

Typical usage could look like:

In order to serialize objects other than dict you must set the safe parameter to False:

Without passing safe=False, a TypeError will be raised.

Note that an API based on dict objects is more extensible, flexible, and makes it easier to maintain forwards compatibility. Therefore, you should avoid using non-dict objects in JSON-encoded response.

Before the 5th edition of ECMAScript it was possible to poison the JavaScript Array constructor. For this reason, Django does not allow passing non-dict objects to the JsonResponse constructor by default. However, most modern browsers implement ECMAScript 5 which removes this attack vector. Therefore it is possible to disable this security precaution.

If you need to use a different JSON encoder class you can pass the encoder parameter to the constructor method:

The StreamingHttpResponse class is used to stream a response from Django to the browser.

StreamingHttpResponse is somewhat advanced, in that it is important to know whether you’ll be serving your application synchronously under WSGI or asynchronously under ASGI, and adjust your usage appropriately.

Please read these notes with care.

An example usage of StreamingHttpResponse under WSGI is streaming content when generating the response would take too long or uses too much memory. For instance, it’s useful for generating large CSV files.

There are performance considerations when doing this, though. Django, under WSGI, is designed for short-lived requests. Streaming responses will tie a worker process for the entire duration of the response. This may result in poor performance.

Generally speaking, you would perform expensive tasks outside of the request-response cycle, rather than resorting to a streamed response.

When serving under ASGI, however, a StreamingHttpResponse need not stop other requests from being served whilst waiting for I/O. This opens up the possibility of long-lived requests for streaming content and implementing patterns such as long-polling, and server-sent events.

Even under ASGI note, StreamingHttpResponse should only be used in situations where it is absolutely required that the whole content isn’t iterated before transferring the data to the client. Because the content can’t be accessed, many middleware can’t function normally. For example the ETag and Content-Length headers can’t be generated for streaming responses.

The StreamingHttpResponse is not a subclass of HttpResponse, because it features a slightly different API. However, it is almost identical, with the following notable differences:

It should be given an iterator that yields bytestrings, memoryview, or strings as content. When serving under WSGI, this should be a sync iterator. When serving under ASGI, then it should be an async iterator.

You cannot access its content, except by iterating the response object itself. This should only occur when the response is returned to the client: you should not iterate the response yourself.

Under WSGI the response will be iterated synchronously. Under ASGI the response will be iterated asynchronously. (This is why the iterator type must match the protocol you’re using.)

To avoid a crash, an incorrect iterator type will be mapped to the correct type during iteration, and a warning will be raised, but in order to do this the iterator must be fully-consumed, which defeats the purpose of using a StreamingHttpResponse at all.

It has no content attribute. Instead, it has a streaming_content attribute. This can be used in middleware to wrap the response iterable, but should not be consumed.

It has no text attribute, as it would require iterating the response object.

You cannot use the file-like object tell() or write() methods. Doing so will raise an exception.

The HttpResponseBase base class is common between HttpResponse and StreamingHttpResponse.

An iterator of the response content, bytestring encoded according to HttpResponse.charset.

The HTTP status code for the response.

Unless reason_phrase is explicitly set, modifying the value of status_code outside the constructor will also modify the value of reason_phrase.

The HTTP reason phrase for the response. It uses the HTTP standard’s default reason phrases.

Unless explicitly set, reason_phrase is determined by the value of status_code.

Boolean indicating whether StreamingHttpResponse.streaming_content is an asynchronous iterator or not.

This is useful for middleware needing to wrap StreamingHttpResponse.streaming_content.

If the client disconnects during a streaming response, Django will cancel the coroutine that is handling the response. If you want to clean up resources manually, you can do so by catching the asyncio.CancelledError:

This example only shows how to handle client disconnection while the response is streaming. If you perform long-running operations in your view before returning the StreamingHttpResponse object, then you may also want to handle disconnections in the view itself.

FileResponse is a subclass of StreamingHttpResponse optimized for binary files. It uses wsgi.file_wrapper if provided by the wsgi server, otherwise it streams the file out in small chunks.

If as_attachment=True, the Content-Disposition header is set to attachment, which asks the browser to offer the file to the user as a download. Otherwise, a Content-Disposition header with a value of inline (the browser default) will be set only if a filename is available.

If open_file doesn’t have a name or if the name of open_file isn’t appropriate, provide a custom file name using the filename parameter. Note that if you pass a file-like object like io.BytesIO, it’s your task to seek() it before passing it to FileResponse.

The Content-Length header is automatically set when it can be guessed from the content of open_file.

The Content-Type header is automatically set when it can be guessed from the filename, or the name of open_file.

FileResponse accepts any file-like object with binary content, for example a file open in binary mode like so:

The file will be closed automatically, so don’t open it with a context manager.

Python’s file API is synchronous. This means that the file must be fully consumed in order to be served under ASGI.

In order to stream a file asynchronously you need to use a third-party package that provides an asynchronous file API, such as aiofiles.

This method is automatically called during the response initialization and set various headers (Content-Length, Content-Type, and Content-Disposition) depending on open_file.

The HttpResponseBase class is common to all Django responses. It should not be used to create responses directly, but it can be useful for type-checking.

---

## SchemaEditor¶

**URL:** https://docs.djangoproject.com/en/stable/ref/schema-editor/

**Contents:**
- SchemaEditor¶
- Methods¶
  - execute()¶
  - create_model()¶
  - delete_model()¶
  - add_index()¶
  - remove_index()¶
  - rename_index()¶
  - add_constraint()¶
  - remove_constraint()¶

Django’s migration system is split into two parts; the logic for calculating and storing what operations should be run (django.db.migrations), and the database abstraction layer that turns things like “create a model” or “delete a field” into SQL - which is the job of the SchemaEditor.

It’s unlikely that you will want to interact directly with SchemaEditor as a normal developer using Django, but if you want to write your own migration system, or have more advanced needs, it’s a lot nicer than writing SQL.

Each database backend in Django supplies its own version of SchemaEditor, and it’s always accessible via the connection.schema_editor() context manager:

It must be used via the context manager as this allows it to manage things like transactions and deferred SQL (like creating ForeignKey constraints).

It exposes all possible operations as methods, that should be called in the order you wish changes to be applied. Some possible operations or types of change are not possible on all databases - for example, MyISAM does not support foreign key constraints.

If you are writing or maintaining a third-party database backend for Django, you will need to provide a SchemaEditor implementation in order to work with Django’s migration functionality - however, as long as your database is relatively standard in its use of SQL and relational design, you should be able to subclass one of the built-in Django SchemaEditor classes and tweak the syntax a little.

Executes the SQL statement passed in, with parameters if supplied. This is a wrapper around the normal database cursors that allows capture of the SQL to a .sql file if the user wishes.

Creates a new table in the database for the provided model, along with any unique constraints or indexes it requires.

Drops the model’s table in the database along with any unique constraints or indexes it has.

Adds index to model’s table.

Removes index from model’s table.

Renames old_index from model’s table to new_index.

Adds constraint to model’s table.

Removes constraint from model’s table.

Changes a model’s unique_together value; this will add or remove unique constraints from the model’s table until they match the new value.

Changes a model’s index_together value; this will add or remove indexes from the model’s table until they match the new value.

Renames the model’s table from old_db_table to new_db_table.

Change the model’s table comment to new_db_table_comment.

Moves the model’s table from one tablespace to another.

Adds a column (or sometimes multiple) to the model’s table to represent the field. This will also add indexes or a unique constraint if the field has db_index=True or unique=True.

If the field is a ManyToManyField without a value for through, instead of creating a column, it will make a table to represent the relationship. If through is provided, it is a no-op.

If the field is a ForeignKey, this will also add the foreign key constraint to the column.

Removes the column(s) representing the field from the model’s table, along with any unique constraints, foreign key constraints, or indexes caused by that field.

If the field is a ManyToManyField without a value for through, it will remove the table created to track the relationship. If through is provided, it is a no-op.

This transforms the field on the model from the old field to the new one. This includes changing the name of the column (the db_column attribute), changing the type of the field (if the field class changes), changing the NULL status of the field, adding or removing field-only unique constraints and indexes, changing primary key, and changing the destination of ForeignKey constraints.

The most common transformation this cannot do is transforming a ManyToManyField into a normal Field or vice-versa; Django cannot do this without losing data, and so it will refuse to do it. Instead, remove_field() and add_field() should be called separately.

If the database has the supports_combined_alters, Django will try and do as many of these in a single database call as possible; otherwise, it will issue a separate ALTER statement for each change, but will not issue ALTERs where no change is required.

All attributes should be considered read-only unless stated otherwise.

A connection object to the database. A useful attribute of the connection is alias which can be used to determine the name of the database being accessed.

This is useful when doing data migrations for migrations with multiple databases.

---

## TemplateResponse and SimpleTemplateResponse¶

**URL:** https://docs.djangoproject.com/en/stable/ref/template-response/

**Contents:**
- TemplateResponse and SimpleTemplateResponse¶
- SimpleTemplateResponse objects¶
  - Attributes¶
  - Methods¶
- TemplateResponse objects¶
  - Methods¶
- The rendering process¶
  - Post-render callbacks¶
- Using TemplateResponse and SimpleTemplateResponse¶

Standard HttpResponse objects are static structures. They are provided with a block of pre-rendered content at time of construction, and while that content can be modified, it isn’t in a form that makes it easy to perform modifications.

However, it can sometimes be beneficial to allow decorators or middleware to modify a response after it has been constructed by the view. For example, you may want to change the template that is used, or put additional data into the context.

TemplateResponse provides a way to do just that. Unlike basic HttpResponse objects, TemplateResponse objects retain the details of the template and context that was provided by the view to compute the response. The final output of the response is not computed until it is needed, later in the response process.

The name of the template to be rendered. Accepts a backend-dependent template object (such as those returned by get_template()), the name of a template, or a list of template names.

Example: ['foo.html', 'path/to/bar.html']

The context data to be used when rendering the template. It must be a dict.

Example: {'foo': 123}

The current rendered value of the response content, using the current template and context data.

A boolean indicating whether the response content has been rendered.

Instantiates a SimpleTemplateResponse object with the given template, context, content type, HTTP status, and charset.

A backend-dependent template object (such as those returned by get_template()), the name of a template, or a list of template names.

A dict of values to add to the template context. By default, this is an empty dictionary.

The value included in the HTTP Content-Type header, including the MIME type specification and the character set encoding. If content_type is specified, then its value is used. Otherwise, 'text/html' is used.

The HTTP status code for the response.

The charset in which the response will be encoded. If not given it will be extracted from content_type, and if that is unsuccessful, the DEFAULT_CHARSET setting will be used.

The NAME of a template engine to use for loading the template.

A dict of HTTP headers to add to the response.

Preprocesses context data that will be used for rendering a template. Accepts a dict of context data. By default, returns the same dict.

Override this method in order to customize the context.

Resolves the template instance to use for rendering. Accepts a backend-dependent template object (such as those returned by get_template()), the name of a template, or a list of template names.

Returns the backend-dependent template object instance to be rendered.

Override this method in order to customize template loading.

Add a callback that will be invoked after rendering has taken place. This hook can be used to defer certain processing operations (such as caching) until after rendering has occurred.

If the SimpleTemplateResponse has already been rendered, the callback will be invoked immediately.

When called, callbacks will be passed a single argument – the rendered SimpleTemplateResponse instance.

If the callback returns a value that is not None, this will be used as the response instead of the original response object (and will be passed to the next post rendering callback etc.)

Sets response.content to the result obtained by SimpleTemplateResponse.rendered_content, runs all post-rendering callbacks, and returns the resulting response object.

render() will only have an effect the first time it is called. On subsequent calls, it will return the result obtained from the first call.

TemplateResponse is a subclass of SimpleTemplateResponse that knows about the current HttpRequest.

Instantiates a TemplateResponse object with the given request, template, context, content type, HTTP status, and charset.

An HttpRequest instance.

A backend-dependent template object (such as those returned by get_template()), the name of a template, or a list of template names.

A dict of values to add to the template context. By default, this is an empty dictionary.

The value included in the HTTP Content-Type header, including the MIME type specification and the character set encoding. If content_type is specified, then its value is used. Otherwise, 'text/html' is used.

The HTTP status code for the response.

The charset in which the response will be encoded. If not given it will be extracted from content_type, and if that is unsuccessful, the DEFAULT_CHARSET setting will be used.

The NAME of a template engine to use for loading the template.

A dict of HTTP headers to add to the response.

Before a TemplateResponse instance can be returned to the client, it must be rendered. The rendering process takes the intermediate representation of template and context, and turns it into the final byte stream that can be served to the client.

There are three circumstances under which a TemplateResponse will be rendered:

When the TemplateResponse instance is explicitly rendered, using the SimpleTemplateResponse.render() method.

When the content of the response is explicitly set by assigning response.content.

After passing through template response middleware, but before passing through response middleware.

A TemplateResponse can only be rendered once. The first call to SimpleTemplateResponse.render() sets the content of the response; subsequent rendering calls do not change the response content.

However, when response.content is explicitly assigned, the change is always applied. If you want to force the content to be re-rendered, you can reevaluate the rendered content, and assign the content of the response manually:

Some operations – such as caching – cannot be performed on an unrendered template. They must be performed on a fully complete and rendered response.

If you’re using middleware, you can do that. Middleware provides multiple opportunities to process a response on exit from a view. If you put behavior in the response middleware, it’s guaranteed to execute after template rendering has taken place.

However, if you’re using a decorator, the same opportunities do not exist. Any behavior defined in a decorator is handled immediately.

To compensate for this (and any other analogous use cases), TemplateResponse allows you to register callbacks that will be invoked when rendering has completed. Using this callback, you can defer critical processing until a point where you can guarantee that rendered content will be available.

To define a post-render callback, define a function that takes a single argument – response – and register that function with the template response:

my_render_callback() will be invoked after the mytemplate.html has been rendered, and will be provided the fully rendered TemplateResponse instance as an argument.

If the template has already been rendered, the callback will be invoked immediately.

A TemplateResponse object can be used anywhere that a normal django.http.HttpResponse can be used. It can also be used as an alternative to calling render().

For example, the following view returns a TemplateResponse with a template and a context containing a queryset:

---

## The File object¶

**URL:** https://docs.djangoproject.com/en/stable/ref/files/file/

**Contents:**
- The File object¶
- The File class¶
- The ContentFile class¶
- The ImageFile class¶
- Additional methods on files attached to objects¶

The django.core.files module and its submodules contain built-in classes for basic file handling in Django.

The File class is a thin wrapper around a Python file object with some Django-specific additions. Internally, Django uses this class when it needs to represent a file.

File objects have the following attributes and methods:

The name of the file including the relative path from MEDIA_ROOT.

The size of the file in bytes.

The underlying file object that this class wraps.

Be careful with this attribute in subclasses.

Some subclasses of File, including ContentFile and FieldFile, may replace this attribute with an object other than a Python file object. In these cases, this attribute may itself be a File subclass (and not necessarily the same subclass). Whenever possible, use the attributes and methods of the subclass itself rather than the those of the subclass’s file attribute.

The read/write mode for the file.

Open or reopen the file (which also does File.seek(0)). The mode argument allows the same values as Python’s built-in open(). *args and **kwargs are passed after mode to Python’s built-in open().

When reopening a file, mode will override whatever mode the file was originally opened with; None means to reopen with the original mode.

It can be used as a context manager, e.g. with file.open() as f:.

Iterate over the file yielding one line at a time.

Iterate over the file yielding “chunks” of a given size. chunk_size defaults to 64 KB.

This is especially useful with very large files since it allows them to be streamed off disk and avoids storing the whole file in memory.

Returns True if the file is large enough to require multiple chunks to access all of its content give some chunk_size.

In addition to the listed methods, File exposes the following attributes and methods of its file object: encoding, fileno, flush, isatty, newlines, read, readinto, readline, readlines, seek, tell, truncate, write, writelines, readable(), writable(), and seekable().

The ContentFile class inherits from File, but unlike File it operates on string content (bytes also supported), rather than an actual file. For example:

Django provides a built-in class specifically for images. django.core.files.images.ImageFile inherits all the attributes and methods of File, and additionally provides the following:

Width of the image in pixels.

Height of the image in pixels.

Any File that is associated with an object (as with Car.photo, below) will also have a couple of extra methods:

Saves a new file with the file name and contents provided. This will not replace the existing file, but will create a new file and update the object to point to it. If save is True, the model’s save() method will be called once the file is saved. That is, these two lines:

Note that the content argument must be an instance of either File or of a subclass of File, such as ContentFile.

Removes the file from the model instance and deletes the underlying file. If save is True, the model’s save() method will be called once the file is deleted.

---
