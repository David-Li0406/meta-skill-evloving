# Django - Howto

**Pages:** 6

---

## How to create custom model fields¶

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-model-fields/

**Contents:**
- How to create custom model fields¶
- Introduction¶
  - Our example object¶
- Background theory¶
  - Database storage¶
  - What does a field class do?¶
- Writing a field subclass¶
  - Field deconstruction¶
  - Field attributes not affecting database column definition¶
  - Changing a custom field’s base class¶

The model reference documentation explains how to use Django’s standard field classes – CharField, DateField, etc. For many purposes, those classes are all you’ll need. Sometimes, though, the Django version won’t meet your precise requirements, or you’ll want to use a field that is entirely different from those shipped with Django.

Django’s built-in field types don’t cover every possible database column type – only the common types, such as VARCHAR and INTEGER. For more obscure column types, such as geographic polygons or even user-created types such as PostgreSQL custom types, you can define your own Django Field subclasses.

Alternatively, you may have a complex Python object that can somehow be serialized to fit into a standard database column type. This is another case where a Field subclass will help you use your object with your models.

Creating custom fields requires a bit of attention to detail. To make things easier to follow, we’ll use a consistent example throughout this document: wrapping a Python object representing the deal of cards in a hand of Bridge. Don’t worry, you don’t have to know how to play Bridge to follow this example. You only need to know that 52 cards are dealt out equally to four players, who are traditionally called north, east, south and west. Our class looks something like this:

This is an ordinary Python class, with nothing Django-specific about it. We’d like to be able to do things like this in our models (we assume the hand attribute on the model is an instance of Hand):

We assign to and retrieve from the hand attribute in our model just like any other Python class. The trick is to tell Django how to handle saving and loading such an object.

In order to use the Hand class in our models, we do not have to change this class at all. This is ideal, because it means you can easily write model support for existing classes where you cannot change the source code.

You might only be wanting to take advantage of custom database column types and deal with the data as standard Python types in your models; strings, or floats, for example. This case is similar to our Hand example and we’ll note any differences as we go along.

Let’s start with model fields. If you break it down, a model field provides a way to take a normal Python object – string, boolean, datetime, or something more complex like Hand – and convert it to and from a format that is useful when dealing with the database. (Such a format is also useful for serialization, but as we’ll see later, that is easier once you have the database side under control).

Fields in a model must somehow be converted to fit into an existing database column type. Different databases provide different sets of valid column types, but the rule is still the same: those are the only types you have to work with. Anything you want to store in the database must fit into one of those types.

Normally, you’re either writing a Django field to match a particular database column type, or you will need a way to convert your data to, say, a string.

For our Hand example, we could convert the card data to a string of 104 characters by concatenating all the cards together in a predetermined order – say, all the north cards first, then the east, south and west cards. So Hand objects can be saved to text or character columns in the database.

All of Django’s fields (and when we say fields in this document, we always mean model fields and not form fields) are subclasses of django.db.models.Field. Most of the information that Django records about a field is common to all fields – name, help text, uniqueness and so forth. Storing all that information is handled by Field. We’ll get into the precise details of what Field can do later on; for now, suffice it to say that everything descends from Field and then customizes key pieces of the class behavior.

It’s important to realize that a Django field class is not what is stored in your model attributes. The model attributes contain normal Python objects. The field classes you define in a model are actually stored in the Meta class when the model class is created (the precise details of how this is done are unimportant here). This is because the field classes aren’t necessary when you’re just creating and modifying attributes. Instead, they provide the machinery for converting between the attribute value and what is stored in the database or sent to the serializer.

Keep this in mind when creating your own custom fields. The Django Field subclass you write provides the machinery for converting between your Python instances and the database/serializer values in various ways (there are differences between storing a value and using a value for lookups, for example). If this sounds a bit tricky, don’t worry – it will become clearer in the examples below. Just remember that you will often end up creating two classes when you want a custom field:

The first class is the Python object that your users will manipulate. They will assign it to the model attribute, they will read from it for displaying purposes, things like that. This is the Hand class in our example.

The second class is the Field subclass. This is the class that knows how to convert your first class back and forth between its permanent storage form and the Python form.

When planning your Field subclass, first give some thought to which existing Field class your new field is most similar to. Can you subclass an existing Django field and save yourself some work? If not, you should subclass the Field class, from which everything is descended.

Initializing your new field is a matter of separating out any arguments that are specific to your case from the common arguments and passing the latter to the __init__() method of Field (or your parent class).

In our example, we’ll call our field HandField. (It’s a good idea to call your Field subclass <Something>Field, so it’s easily identifiable as a Field subclass.) It doesn’t behave like any existing field, so we’ll subclass directly from Field:

Our HandField accepts most of the standard field options (see the list below), but we ensure it has a fixed length, since it only needs to hold 52 card values plus their suits; 104 characters in total.

Many of Django’s model fields accept options that they don’t do anything with. For example, you can pass both editable and auto_now to a django.db.models.DateField and it will ignore the editable parameter (auto_now being set implies editable=False). No error is raised in this case.

This behavior simplifies the field classes, because they don’t need to check for options that aren’t necessary. They pass all the options to the parent class and then don’t use them later on. It’s up to you whether you want your fields to be more strict about the options they select, or to use the more permissive behavior of the current fields.

The Field.__init__() method takes the following parameters:

rel: Used for related fields (like ForeignKey). For advanced use only.

serialize: If False, the field will not be serialized when the model is passed to Django’s serializers. Defaults to True.

db_tablespace: Only for index creation, if the backend supports tablespaces. You can usually ignore this option.

auto_created: True if the field was automatically created, as for the OneToOneField used by model inheritance. For advanced use only.

All of the options without an explanation in the above list have the same meaning they do for normal Django fields. See the field documentation for examples and details.

The counterpoint to writing your __init__() method is writing the deconstruct() method. It’s used during model migrations to tell Django how to take an instance of your new field and reduce it to a serialized form - in particular, what arguments to pass to __init__() to recreate it.

If you haven’t added any extra options on top of the field you inherited from, then there’s no need to write a new deconstruct() method. If, however, you’re changing the arguments passed in __init__() (like we are in HandField), you’ll need to supplement the values being passed.

deconstruct() returns a tuple of four items: the field’s attribute name, the full import path of the field class, the positional arguments (as a list), and the keyword arguments (as a dict). Note this is different from the deconstruct() method for custom classes which returns a tuple of three things.

As a custom field author, you don’t need to care about the first two values; the base Field class has all the code to work out the field’s attribute name and import path. You do, however, have to care about the positional and keyword arguments, as these are likely the things you are changing.

For example, in our HandField class we’re always forcibly setting max_length in __init__(). The deconstruct() method on the base Field class will see this and try to return it in the keyword arguments; thus, we can drop it from the keyword arguments for readability:

If you add a new keyword argument, you need to write code in deconstruct() that puts its value into kwargs yourself. You should also omit the value from kwargs when it isn’t necessary to reconstruct the state of the field, such as when the default value is being used:

More complex examples are beyond the scope of this document, but remember - for any configuration of your Field instance, deconstruct() must return arguments that you can pass to __init__ to reconstruct that state.

Pay extra attention if you set new default values for arguments in the Field superclass; you want to make sure they’re always included, rather than disappearing if they take on the old default value.

In addition, try to avoid returning values as positional arguments; where possible, return values as keyword arguments for maximum future compatibility. If you change the names of things more often than their position in the constructor’s argument list, you might prefer positional, but bear in mind that people will be reconstructing your field from the serialized version for quite a while (possibly years), depending how long your migrations live for.

You can see the results of deconstruction by looking in migrations that include the field, and you can test deconstruction in unit tests by deconstructing and reconstructing the field:

You can override Field.non_db_attrs to customize attributes of a field that don’t affect a column definition. It’s used during model migrations to detect no-op AlterField operations.

You can’t change the base class of a custom field because Django won’t detect the change and make a migration for it. For example, if you start with:

and then decide that you want to use TextField instead, you can’t change the subclass like this:

Instead, you must create a new custom field class and update your models to reference it:

As discussed in removing fields, you must retain the original CustomCharField class as long as you have migrations that reference it.

As always, you should document your field type, so users will know what it is. In addition to providing a docstring for it, which is useful for developers, you can also allow users of the admin app to see a short description of the field type via the django.contrib.admindocs application. To do this provide descriptive text in a description class attribute of your custom field. In the above example, the description displayed by the admindocs application for a HandField will be ‘A hand of cards (bridge style)’.

In the django.contrib.admindocs display, the field description is interpolated with field.__dict__ which allows the description to incorporate arguments of the field. For example, the description for CharField is:

Once you’ve created your Field subclass, you might consider overriding a few standard methods, depending on your field’s behavior. The list of methods below is in approximately decreasing order of importance, so start from the top.

Say you’ve created a PostgreSQL custom type called mytype. You can subclass Field and implement the db_type() method, like so:

Once you have MytypeField, you can use it in any model, just like any other Field type:

If you aim to build a database-agnostic application, you should account for differences in database column types. For example, the date/time column type in PostgreSQL is called timestamp, while the same column in MySQL is called datetime. You can handle this in a db_type() method by checking the connection.vendor attribute. Current built-in vendor names are: sqlite, postgresql, mysql, and oracle.

The db_type() and rel_db_type() methods are called by Django when the framework constructs the CREATE TABLE statements for your application – that is, when you first create your tables. The methods are also called when constructing a WHERE clause that includes the model field – that is, when you retrieve data using QuerySet methods like get(), filter(), and exclude() and have the model field as an argument.

Some database column types accept parameters, such as CHAR(25), where the parameter 25 represents the maximum column length. In cases like these, it’s more flexible if the parameter is specified in the model rather than being hardcoded in the db_type() method. For example, it wouldn’t make much sense to have a CharMaxlength25Field, shown here:

The better way of doing this would be to make the parameter specifiable at run time – i.e., when the class is instantiated. To do that, implement Field.__init__(), like so:

Finally, if your column requires truly complex SQL setup, return None from db_type(). This will cause Django’s SQL creation code to skip over this field. You are then responsible for creating the column in the right table in some other way, but this gives you a way to tell Django to get out of the way.

The rel_db_type() method is called by fields such as ForeignKey and OneToOneField that point to another field to determine their database column data types. For example, if you have an UnsignedAutoField, you also need the foreign keys that point to that field to use the same data type:

If your custom Field class deals with data structures that are more complex than strings, dates, integers, or floats, then you may need to override from_db_value() and to_python().

If present for the field subclass, from_db_value() will be called in all circumstances when the data is loaded from the database, including in aggregates and values() calls.

to_python() is called by deserialization and during the clean() method used from forms.

As a general rule, to_python() should deal gracefully with any of the following arguments:

An instance of the correct type (e.g., Hand in our ongoing example).

None (if the field allows null=True)

In our HandField class, we’re storing the data as a VARCHAR field in the database, so we need to be able to process strings and None in the from_db_value(). In to_python(), we need to also handle Hand instances:

Notice that we always return a Hand instance from these methods. That’s the Python object type we want to store in the model’s attribute.

For to_python(), if anything goes wrong during value conversion, you should raise a ValidationError exception.

Since using a database requires conversion in both ways, if you override from_db_value() you also have to override get_prep_value() to convert Python objects back to query values.

If your custom field uses the CHAR, VARCHAR or TEXT types for MySQL, you must make sure that get_prep_value() always returns a string type. MySQL performs flexible and unexpected matching when a query is performed on these types and the provided value is an integer, which can cause queries to include unexpected objects in their results. This problem cannot occur if you always return a string type from get_prep_value().

Some data types (for example, dates) need to be in a specific format before they can be used by a database backend. get_db_prep_value() is the method where those conversions should be made. The specific connection that will be used for the query is passed as the connection parameter. This allows you to use backend-specific conversion logic if it is required.

For example, Django uses the following method for its BinaryField:

In case your custom field needs a special conversion when being saved that is not the same as the conversion used for normal query parameters, you can override get_db_prep_save().

If you want to preprocess the value just before saving, you can use pre_save(). For example, Django’s DateTimeField uses this method to set the attribute correctly in the case of auto_now or auto_now_add.

If you do override this method, you must return the value of the attribute at the end. You should also update the model’s attribute if you make any changes to the value so that code holding references to the model will always see the correct value.

To customize the form field used by ModelForm, you can override formfield().

The form field class can be specified via the form_class and choices_form_class arguments; the latter is used if the field has choices specified, the former otherwise. If these arguments are not provided, CharField or TypedChoiceField will be used.

All of the kwargs dictionary is passed directly to the form field’s __init__() method. Normally, all you need to do is set up a good default for the form_class (and maybe choices_form_class) argument and then delegate further handling to the parent class. This might require you to write a custom form field (and even a form widget). See the forms documentation for information about this.

If you wish to exclude the field from the ModelForm, you can override the formfield() method to return None.

Continuing our ongoing example, we can write the formfield() method as:

This assumes we’ve imported a MyFormField field class (which has its own default widget). This document doesn’t cover the details of writing custom form fields.

If you have created a db_type() method, you don’t need to worry about get_internal_type() – it won’t be used much. Sometimes, though, your database storage is similar in type to some other field, so you can use that other field’s logic to create the right column.

No matter which database backend we are using, this will mean that migrate and other SQL commands create the right column type for storing a string.

If get_internal_type() returns a string that is not known to Django for the database backend you are using – that is, it doesn’t appear in django.db.backends.<db_name>.base.DatabaseWrapper.data_types – the string will still be used by the serializer, but the default db_type() method will return None. See the documentation of db_type() for reasons why this might be useful. Putting a descriptive string in as the type of the field for the serializer is a useful idea if you’re ever going to be using the serializer output in some other place, outside of Django.

To customize how the values are serialized by a serializer, you can override value_to_string(). Using value_from_object() is the best way to get the field’s value prior to serialization. For example, since HandField uses strings for its data storage anyway, we can reuse some existing conversion code:

Writing a custom field can be a tricky process, particularly if you’re doing complex conversions between your Python types and your database and serialization formats. Here are a couple of tips to make things go more smoothly:

Look at the existing Django fields (in django/db/models/fields/__init__.py) for inspiration. Try to find a field that’s similar to what you want and extend it a little bit, instead of creating an entirely new field from scratch.

Put a __str__() method on the class you’re wrapping up as a field. There are a lot of places where the default behavior of the field code is to call str() on the value. (In our examples in this document, value would be a Hand instance, not a HandField). So if your __str__() method automatically converts to the string form of your Python object, you can save yourself a lot of work.

In addition to the above methods, fields that deal with files have a few other special requirements which must be taken into account. The majority of the mechanics provided by FileField, such as controlling database storage and retrieval, can remain unchanged, leaving subclasses to deal with the challenge of supporting a particular type of file.

Django provides a File class, which is used as a proxy to the file’s contents and operations. This can be subclassed to customize how the file is accessed, and what methods are available. It lives at django.db.models.fields.files, and its default behavior is explained in the file documentation.

Once a subclass of File is created, the new FileField subclass must be told to use it. To do so, assign the new File subclass to the special attr_class attribute of the FileField subclass.

In addition to the above details, there are a few guidelines which can greatly improve the efficiency and readability of the field’s code.

The source for Django’s own ImageField (in django/db/models/fields/files.py) is a great example of how to subclass FileField to support a particular type of file, as it incorporates all of the techniques described above.

Cache file attributes wherever possible. Since files may be stored in remote storage systems, retrieving them may cost extra time, or even money, that isn’t always necessary. Once a file is retrieved to obtain some data about its content, cache as much of that data as possible to reduce the number of times the file must be retrieved on subsequent calls for that information.

---

## How to create database migrations¶

**URL:** https://docs.djangoproject.com/en/stable/howto/writing-migrations/

**Contents:**
- How to create database migrations¶
- Data migrations and multiple databases¶
- Migrations that add unique fields¶
  - Non-atomic migrations¶
- Controlling the order of migrations¶
- Migrating data between third-party apps¶
- Changing a ManyToManyField to use a through model¶
- Changing an unmanaged model to managed¶

This document explains how to structure and write database migrations for different scenarios you might encounter. For introductory material on migrations, see the topic guide.

When using multiple databases, you may need to figure out whether or not to run a migration against a particular database. For example, you may want to only run a migration on a particular database.

In order to do that you can check the database connection’s alias inside a RunPython operation by looking at the schema_editor.connection.alias attribute:

You can also provide hints that will be passed to the allow_migrate() method of database routers as **hints:

Then, to leverage this in your migrations, do the following:

If your RunPython or RunSQL operation only affects one model, it’s good practice to pass model_name as a hint to make it as transparent as possible to the router. This is especially important for reusable and third-party apps.

Applying a “plain” migration that adds a unique non-nullable field to a table with existing rows will raise an error because the value used to populate existing rows is generated only once, thus breaking the unique constraint.

Therefore, the following steps should be taken. In this example, we’ll add a non-nullable UUIDField with a default value. Modify the respective field according to your needs.

Add the field on your model with default=uuid.uuid4 and unique=True arguments (choose an appropriate default for the type of the field you’re adding).

Run the makemigrations command. This should generate a migration with an AddField operation.

Generate two empty migration files for the same app by running makemigrations myapp --empty twice. We’ve renamed the migration files to give them meaningful names in the examples below.

Copy the AddField operation from the auto-generated migration (the first of the three new files) to the last migration, change AddField to AlterField, and add imports of uuid and models. For example:

Edit the first migration file. The generated migration class should look similar to this:

Change unique=True to null=True – this will create the intermediary null field and defer creating the unique constraint until we’ve populated unique values on all the rows.

In the first empty migration file, add a RunPython or RunSQL operation to generate a unique value (UUID in the example) for each existing row. Also add an import of uuid. For example:

Now you can apply the migrations as usual with the migrate command.

Note there is a race condition if you allow objects to be created while this migration is running. Objects created after the AddField and before RunPython will have their original uuid’s overwritten.

On databases that support DDL transactions (SQLite and PostgreSQL), migrations will run inside a transaction by default. For use cases such as performing data migrations on large tables, you may want to prevent a migration from running in a transaction by setting the atomic attribute to False:

Within such a migration, all operations are run without a transaction. It’s possible to execute parts of the migration inside a transaction using atomic() or by passing atomic=True to RunPython.

Here’s an example of a non-atomic data migration that updates a large table in smaller batches:

The atomic attribute doesn’t have an effect on databases that don’t support DDL transactions (e.g. MySQL, Oracle). (MySQL’s atomic DDL statement support refers to individual statements rather than multiple statements wrapped in a transaction that can be rolled back.)

Django determines the order in which migrations should be applied not by the filename of each migration, but by building a graph using two properties on the Migration class: dependencies and run_before.

If you’ve used the makemigrations command you’ve probably already seen dependencies in action because auto-created migrations have this defined as part of their creation process.

The dependencies property is declared like this:

Usually this will be enough, but from time to time you may need to ensure that your migration runs before other migrations. This is useful, for example, to make third-party apps’ migrations run after your AUTH_USER_MODEL replacement.

To achieve this, place all migrations that should depend on yours in the run_before attribute on your Migration class:

Prefer using dependencies over run_before when possible. You should only use run_before if it is undesirable or impractical to specify dependencies in the migration which you want to run after the one you are writing.

You can use a data migration to move data from one third-party application to another.

If you plan to remove the old app later, you’ll need to set the dependencies property based on whether or not the old app is installed. Otherwise, you’ll have missing dependencies once you uninstall the old app. Similarly, you’ll need to catch LookupError in the apps.get_model() call that retrieves models from the old app. This approach allows you to deploy your project anywhere without first installing and then uninstalling the old app.

Here’s a sample migration:

Also consider what you want to happen when the migration is unapplied. You could either do nothing (as in the example above) or remove some or all of the data from the new application. Adjust the second argument of the RunPython operation accordingly.

If you change a ManyToManyField to use a through model, the default migration will delete the existing table and create a new one, losing the existing relations. To avoid this, you can use SeparateDatabaseAndState to rename the existing table to the new table name while telling the migration autodetector that the new model has been created. You can check the existing table name and constraint name through sqlmigrate or dbshell. You can check the new table name with the through model’s _meta.db_table property. Your new through model should use the same names for the ForeignKeys as Django did. Also if it needs any extra fields, they should be added in operations after SeparateDatabaseAndState.

For example, if we had a Book model with a ManyToManyField linking to Author, we could add a through model AuthorBook with a new field is_primary, like so:

If you want to change an unmanaged model (managed=False) to managed, you must remove managed=False and generate a migration before making other schema-related changes to the model, since schema changes that appear in the migration that contains the operation to change Meta.managed may not be applied.

---

## How-to guides¶

**URL:** https://docs.djangoproject.com/en/stable/howto/

**Contents:**
- How-to guides¶
- Models, data and databases¶
- Templates and output¶
- Project configuration and management¶
- Installing, deploying and upgrading¶
- Other guides¶

Practical guides covering common tasks and problems.

The Django community aggregator, where we aggregate content from the global Django community. Many writers in the aggregator write this sort of how-to material.

---

## How to integrate Django with a legacy database¶

**URL:** https://docs.djangoproject.com/en/stable/howto/legacy-databases/

**Contents:**
- How to integrate Django with a legacy database¶
- Give Django your database parameters¶
- Auto-generate the models¶
- Install the core Django tables¶
- Test and tweak¶

While Django is best suited for developing new applications, it’s quite possible to integrate it into legacy databases. Django includes a couple of utilities to automate as much of this process as possible.

This document assumes you know the Django basics, as covered in the tutorial.

Once you’ve got Django set up, you’ll follow this general process to integrate with an existing database.

You’ll need to tell Django what your database connection parameters are, and what the name of the database is. Do that by editing the DATABASES setting and assigning values to the following keys for the 'default' connection:

Django comes with a utility called inspectdb that can create models by introspecting an existing database. You can view the output by running this command:

Save this as a file by using standard Unix output redirection:

This feature is meant as a shortcut, not as definitive model generation. See the documentation of inspectdb for more information.

Once you’ve cleaned up your models, name the file models.py and put it in the Python package that holds your app. Then add the app to your INSTALLED_APPS setting.

By default, inspectdb creates unmanaged models. That is, managed = False in the model’s Meta class tells Django not to manage each table’s creation, modification, and deletion:

If you do want to allow Django to manage the table’s lifecycle, you’ll need to change the managed option above to True (or remove it because True is its default value).

Next, run the migrate command to install any extra needed database records such as admin permissions and content types:

Those are the basic steps – from here you’ll want to tweak the models Django generated until they work the way you’d like. Try accessing your data via the Django database API, and try editing objects via Django’s admin site, and edit the models file accordingly.

---

## How to write a custom storage class¶

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-file-storage/

**Contents:**
- How to write a custom storage class¶
- Use your custom storage engine¶

If you need to provide custom file storage – a common example is storing files on some remote system – you can do so by defining a custom storage class. You’ll need to follow these steps:

Your custom storage system must be a subclass of django.core.files.storage.Storage:

Django must be able to instantiate your storage system without any arguments. This means that any settings should be taken from django.conf.settings:

Your storage class must implement the _open() and _save() methods, along with any other methods appropriate to your storage class. See below for more on these methods.

In addition, if your class provides local file storage, it must override the path() method.

Your storage class must be deconstructible so it can be serialized when it’s used on a field in a migration. As long as your field has arguments that are themselves serializable, you can use the django.utils.deconstruct.deconstructible class decorator for this (that’s what Django uses on FileSystemStorage).

By default, the following methods raise NotImplementedError and will typically have to be overridden:

Note however that not all these methods are required and may be deliberately omitted. As it happens, it is possible to leave each method unimplemented and still have a working Storage.

By way of example, if listing the contents of certain storage backends turns out to be expensive, you might decide not to implement Storage.listdir().

Another example would be a backend that only handles writing to files. In this case, you would not need to implement any of the above methods.

Ultimately, which of these methods are implemented is up to you. Leaving some methods unimplemented will result in a partial (possibly broken) interface.

You’ll also usually want to use hooks specifically designed for custom storage objects. These are:

Called by Storage.open(), this is the actual mechanism the storage class uses to open the file. This must return a File object, though in most cases, you’ll want to return some subclass here that implements logic specific to the backend storage system. The FileNotFoundError exception should be raised when a file doesn’t exist.

Called by Storage.save(). The name will already have gone through get_valid_name() and get_available_name(), and the content will be a File object itself.

Should return the actual name of the file saved (usually the name passed in, but if the storage needs to change the file name return the new name instead).

Returns a filename suitable for use with the underlying storage system. The name argument passed to this method is either the original filename sent to the server or, if upload_to is a callable, the filename returned by that method after any path information is removed. Override this to customize how non-standard characters are converted to safe filenames.

The code provided on Storage retains only alpha-numeric characters, periods and underscores from the original filename, removing everything else.

Returns an alternative filename based on the file_root and file_ext parameters. By default, an underscore plus a random 7 character alphanumeric string is appended to the filename before the extension.

Returns a filename that is available in the storage mechanism, possibly taking the provided filename into account. The name argument passed to this method will have already cleaned to a filename valid for the storage system, according to the get_valid_name() method described above.

The length of the filename will not exceed max_length, if provided. If a free unique filename cannot be found, a SuspiciousFileOperation exception is raised.

If a file with name already exists, get_alternative_name() is called to obtain an alternative name.

The first step to using your custom storage with Django is to tell Django about the file storage backend you’ll be using. This is done using the STORAGES setting. This setting maps storage aliases, which are a way to refer to a specific storage throughout Django, to a dictionary of settings for that specific storage backend. The settings in the inner dictionaries are described fully in the STORAGES documentation.

Storages are then accessed by alias from the django.core.files.storage.storages dictionary:

---

## How to write custom lookups¶

**URL:** https://docs.djangoproject.com/en/stable/howto/custom-lookups/

**Contents:**
- How to write custom lookups¶
- A lookup example¶
- A transformer example¶
- Writing an efficient abs__lt lookup¶
- A bilateral transformer example¶
- Writing alternative implementations for existing lookups¶
- How Django determines the lookups and transforms which are used¶

Django offers a wide variety of built-in lookups for filtering (for example, exact and icontains). This documentation explains how to write custom lookups and how to alter the working of existing lookups. For the API references of lookups, see the Lookup API reference.

Let’s start with a small custom lookup. We will write a custom lookup ne which works opposite to exact. Author.objects.filter(name__ne='Jack') will translate to the SQL:

This SQL is backend independent, so we don’t need to worry about different databases.

There are two steps to making this work. Firstly we need to implement the lookup, then we need to tell Django about it:

To register the NotEqual lookup we will need to call register_lookup on the field class we want the lookup to be available for. In this case, the lookup makes sense on all Field subclasses, so we register it with Field directly:

Lookup registration can also be done using a decorator pattern:

We can now use foo__ne for any field foo. You will need to ensure that this registration happens before you try to create any querysets using it. You could place the implementation in a models.py file, or register the lookup in the ready() method of an AppConfig.

Taking a closer look at the implementation, the first required attribute is lookup_name. This allows the ORM to understand how to interpret name__ne and use NotEqual to generate the SQL. By convention, these names are always lowercase strings containing only letters, but the only hard requirement is that it must not contain the string __.

We then need to define the as_sql method. This takes a SQLCompiler object, called compiler, and the active database connection. SQLCompiler objects are not documented, but the only thing we need to know about them is that they have a compile() method which returns a tuple containing an SQL string, and the parameters to be interpolated into that string. In most cases, you don’t need to use it directly and can pass it on to process_lhs() and process_rhs().

A Lookup works against two values, lhs and rhs, standing for left-hand side and right-hand side. The left-hand side is usually a field reference, but it can be anything implementing the query expression API. The right-hand is the value given by the user. In the example Author.objects.filter(name__ne='Jack'), the left-hand side is a reference to the name field of the Author model, and 'Jack' is the right-hand side.

We call process_lhs and process_rhs to convert them into the values we need for SQL using the compiler object described before. These methods return tuples containing some SQL and the parameters to be interpolated into that SQL, just as we need to return from our as_sql method. In the above example, process_lhs returns ('"author"."name"', []) and process_rhs returns ('"%s"', ['Jack']). In this example there were no parameters for the left hand side, but this would depend on the object we have, so we still need to include them in the parameters we return.

Finally we combine the parts into an SQL expression with <>, and supply all the parameters for the query. We then return a tuple containing the generated SQL string and the parameters.

The custom lookup above is great, but in some cases you may want to be able to chain lookups together. For example, let’s suppose we are building an application where we want to make use of the abs() operator. We have an Experiment model which records a start value, end value, and the change (start - end). We would like to find all experiments where the change was equal to a certain amount (Experiment.objects.filter(change__abs=27)), or where it did not exceed a certain amount (Experiment.objects.filter(change__abs__lt=27)).

This example is somewhat contrived, but it nicely demonstrates the range of functionality which is possible in a database backend independent manner, and without duplicating functionality already in Django.

We will start by writing an AbsoluteValue transformer. This will use the SQL function ABS() to transform the value before comparison:

Next, let’s register it for IntegerField:

We can now run the queries we had before. Experiment.objects.filter(change__abs=27) will generate the following SQL:

By using Transform instead of Lookup it means we are able to chain further lookups afterward. So Experiment.objects.filter(change__abs__lt=27) will generate the following SQL:

Note that in case there is no other lookup specified, Django interprets change__abs=27 as change__abs__exact=27.

This also allows the result to be used in ORDER BY and DISTINCT ON clauses. For example Experiment.objects.order_by('change__abs') generates:

And on databases that support distinct on fields (such as PostgreSQL), Experiment.objects.distinct('change__abs') generates:

When looking for which lookups are allowable after the Transform has been applied, Django uses the output_field attribute. We didn’t need to specify this here as it didn’t change, but supposing we were applying AbsoluteValue to some field which represents a more complex type (for example a point relative to an origin, or a complex number) then we may have wanted to specify that the transform returns a FloatField type for further lookups. This can be done by adding an output_field attribute to the transform:

This ensures that further lookups like abs__lte behave as they would for a FloatField.

When using the above written abs lookup, the SQL produced will not use indexes efficiently in some cases. In particular, when we use change__abs__lt=27, this is equivalent to change__gt=-27 AND change__lt=27. (For the lte case we could use the SQL BETWEEN).

So we would like Experiment.objects.filter(change__abs__lt=27) to generate the following SQL:

The implementation is:

There are a couple of notable things going on. First, AbsoluteValueLessThan isn’t calling process_lhs(). Instead it skips the transformation of the lhs done by AbsoluteValue and uses the original lhs. That is, we want to get "experiments"."change" not ABS("experiments"."change"). Referring directly to self.lhs.lhs is safe as AbsoluteValueLessThan can be accessed only from the AbsoluteValue lookup, that is the lhs is always an instance of AbsoluteValue.

Notice also that as both sides are used multiple times in the query the params need to contain lhs_params and rhs_params multiple times.

The final query does the inversion (27 to -27) directly in the database. The reason for doing this is that if the self.rhs is something else than a plain integer value (for example an F() reference) we can’t do the transformations in Python.

In fact, most lookups with __abs could be implemented as range queries like this, and on most database backends it is likely to be more sensible to do so as you can make use of the indexes. However with PostgreSQL you may want to add an index on abs(change) which would allow these queries to be very efficient.

The AbsoluteValue example we discussed previously is a transformation which applies to the left-hand side of the lookup. There may be some cases where you want the transformation to be applied to both the left-hand side and the right-hand side. For instance, if you want to filter a queryset based on the equality of the left and right-hand side insensitively to some SQL function.

Let’s examine case-insensitive transformations here. This transformation isn’t very useful in practice as Django already comes with a bunch of built-in case-insensitive lookups, but it will be a nice demonstration of bilateral transformations in a database-agnostic way.

We define an UpperCase transformer which uses the SQL function UPPER() to transform the values before comparison. We define bilateral = True to indicate that this transformation should apply to both lhs and rhs:

Next, let’s register it:

Now, the queryset Author.objects.filter(name__upper="doe") will generate a case insensitive query like this:

Sometimes different database vendors require different SQL for the same operation. For this example we will rewrite a custom implementation for MySQL for the NotEqual operator. Instead of <> we will be using != operator. (Note that in reality almost all databases support both, including all the official databases supported by Django).

We can change the behavior on a specific backend by creating a subclass of NotEqual with an as_mysql method:

We can then register it with Field. It takes the place of the original NotEqual class as it has the same lookup_name.

When compiling a query, Django first looks for as_%s % connection.vendor methods, and then falls back to as_sql. The vendor names for the in-built backends are sqlite, postgresql, oracle and mysql.

In some cases you may wish to dynamically change which Transform or Lookup is returned based on the name passed in, rather than fixing it. As an example, you could have a field which stores coordinates or an arbitrary dimension, and wish to allow a syntax like .filter(coords__x7=4) to return the objects where the 7th coordinate has value 4. In order to do this, you would override get_lookup with something like:

You would then define get_coordinate_lookup appropriately to return a Lookup subclass which handles the relevant value of dimension.

There is a similarly named method called get_transform(). get_lookup() should always return a Lookup subclass, and get_transform() a Transform subclass. It is important to remember that Transform objects can be further filtered on, and Lookup objects cannot.

When filtering, if there is only one lookup name remaining to be resolved, we will look for a Lookup. If there are multiple names, it will look for a Transform. In the situation where there is only one name and a Lookup is not found, we look for a Transform and then the exact lookup on that Transform. All call sequences always end with a Lookup. To clarify:

.filter(myfield__mylookup) will call myfield.get_lookup('mylookup').

.filter(myfield__mytransform__mylookup) will call myfield.get_transform('mytransform'), and then mytransform.get_lookup('mylookup').

.filter(myfield__mytransform) will first call myfield.get_lookup('mytransform'), which will fail, so it will fall back to calling myfield.get_transform('mytransform') and then mytransform.get_lookup('exact').

---
