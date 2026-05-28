# Django - Topics

**Pages:** 21

---

## Aggregation¶

**URL:** https://docs.djangoproject.com/en/stable/topics/db/aggregation/

**Contents:**
- Aggregation¶
- Cheat sheet¶
- Generating aggregates over a QuerySet¶
- Generating aggregates for each item in a QuerySet¶
  - Combining multiple aggregations¶
- Joins and aggregates¶
  - Following relationships backwards¶
- Aggregations and other QuerySet clauses¶
  - filter() and exclude()¶
    - Filtering on annotations¶

The topic guide on Django’s database-abstraction API described the way that you can use Django queries that create, retrieve, update and delete individual objects. However, sometimes you will need to retrieve values that are derived by summarizing or aggregating a collection of objects. This topic guide describes the ways that aggregate values can be generated and returned using Django queries.

Throughout this guide, we’ll refer to the following models. These models are used to track the inventory for a series of online bookstores:

In a hurry? Here’s how to do common aggregate queries, assuming the models above:

Django provides two ways to generate aggregates. The first way is to generate summary values over an entire QuerySet. For example, say you wanted to calculate the average price of all books available for sale. Django’s query syntax provides a means for describing the set of all books:

What we need is a way to calculate summary values over the objects that belong to this QuerySet. This is done by appending an aggregate() clause onto the QuerySet:

The all() is redundant in this example, so this could be simplified to:

The argument to the aggregate() clause describes the aggregate value that we want to compute - in this case, the average of the price field on the Book model. A list of the aggregate functions that are available can be found in the QuerySet reference.

aggregate() is a terminal clause for a QuerySet that, when invoked, returns a dictionary of name-value pairs. The name is an identifier for the aggregate value; the value is the computed aggregate. The name is automatically generated from the name of the field and the aggregate function. If you want to manually specify a name for the aggregate value, you can do so by providing that name when you specify the aggregate clause:

If you want to generate more than one aggregate, you add another argument to the aggregate() clause. So, if we also wanted to know the maximum and minimum price of all books, we would issue the query:

The second way to generate summary values is to generate an independent summary for each object in a QuerySet. For example, if you are retrieving a list of books, you may want to know how many authors contributed to each book. Each Book has a many-to-many relationship with the Author; we want to summarize this relationship for each book in the QuerySet.

Per-object summaries can be generated using the annotate() clause. When an annotate() clause is specified, each object in the QuerySet will be annotated with the specified values.

The syntax for these annotations is identical to that used for the aggregate() clause. Each argument to annotate() describes an aggregate that is to be calculated. For example, to annotate books with the number of authors:

As with aggregate(), the name for the annotation is automatically derived from the name of the aggregate function and the name of the field being aggregated. You can override this default name by providing an alias when you specify the annotation:

Unlike aggregate(), annotate() is not a terminal clause. The output of the annotate() clause is a QuerySet; this QuerySet can be modified using any other QuerySet operation, including filter(), order_by(), or even additional calls to annotate().

Combining multiple aggregations with annotate() will yield the wrong results because joins are used instead of subqueries:

For most aggregates, there is no way to avoid this problem, however, the Count aggregate has a distinct parameter that may help:

If in doubt, inspect the SQL query!

In order to understand what happens in your query, consider inspecting the query property of your QuerySet.

So far, we have dealt with aggregates over fields that belong to the model being queried. However, sometimes the value you want to aggregate will belong to a model that is related to the model you are querying.

When specifying the field to be aggregated in an aggregate function, Django will allow you to use the same double underscore notation that is used when referring to related fields in filters. Django will then handle any table joins that are required to retrieve and aggregate the related value.

For example, to find the price range of books offered in each store, you could use the annotation:

This tells Django to retrieve the Store model, join (through the many-to-many relationship) with the Book model, and aggregate on the price field of the book model to produce a minimum and maximum value.

The same rules apply to the aggregate() clause. If you wanted to know the lowest and highest price of any book that is available for sale in any of the stores, you could use the aggregate:

Join chains can be as deep as you require. For example, to extract the age of the youngest author of any book available for sale, you could issue the query:

In a way similar to Lookups that span relationships, aggregations and annotations on fields of models or models that are related to the one you are querying can include traversing “reverse” relationships. The lowercase name of related models and double-underscores are used here too.

For example, we can ask for all publishers, annotated with their respective total book stock counters (note how we use 'book' to specify the Publisher -> Book reverse foreign key hop):

(Every Publisher in the resulting QuerySet will have an extra attribute called book__count.)

We can also ask for the oldest book of any of those managed by every publisher:

(The resulting dictionary will have a key called 'oldest_pubdate'. If no such alias were specified, it would be the rather long 'book__pubdate__min'.)

This doesn’t apply just to foreign keys. It also works with many-to-many relations. For example, we can ask for every author, annotated with the total number of pages considering all the books the author has (co-)authored (note how we use 'book' to specify the Author -> Book reverse many-to-many hop):

(Every Author in the resulting QuerySet will have an extra attribute called total_pages. If no such alias were specified, it would be the rather long book__pages__sum.)

Or ask for the average rating of all the books written by author(s) we have on file:

(The resulting dictionary will have a key called 'average_rating'. If no such alias were specified, it would be the rather long 'book__rating__avg'.)

Aggregates can also participate in filters. Any filter() (or exclude()) applied to normal model fields will have the effect of constraining the objects that are considered for aggregation.

When used with an annotate() clause, a filter has the effect of constraining the objects for which an annotation is calculated. For example, you can generate an annotated list of all books that have a title starting with “Django” using the query:

When used with an aggregate() clause, a filter has the effect of constraining the objects over which the aggregate is calculated. For example, you can generate the average price of all books with a title that starts with “Django” using the query:

Annotated values can also be filtered. The alias for the annotation can be used in filter() and exclude() clauses in the same way as any other model field.

For example, to generate a list of books that have more than one author, you can issue the query:

This query generates an annotated result set, and then generates a filter based upon that annotation.

If you need two annotations with two separate filters you can use the filter argument with any aggregate. For example, to generate a list of authors with a count of highly rated books:

Each Author in the result set will have the num_books and highly_rated_books attributes. See also Conditional aggregation.

Choosing between filter and QuerySet.filter()

Avoid using the filter argument with a single annotation or aggregation. It’s more efficient to use QuerySet.filter() to exclude rows. The aggregation filter argument is only useful when using two or more aggregations over the same relations with different conditionals.

When developing a complex query that involves both annotate() and filter() clauses, pay particular attention to the order in which the clauses are applied to the QuerySet.

When an annotate() clause is applied to a query, the annotation is computed over the state of the query up to the point where the annotation is requested. The practical implication of this is that filter() and annotate() are not commutative operations.

Publisher A has two books with ratings 4 and 5.

Publisher B has two books with ratings 1 and 4.

Publisher C has one book with rating 1.

Here’s an example with the Count aggregate:

Both queries return a list of publishers that have at least one book with a rating exceeding 3.0, hence publisher C is excluded.

In the first query, the annotation precedes the filter, so the filter has no effect on the annotation. distinct=True is required to avoid a query bug.

The second query counts the number of books that have a rating exceeding 3.0 for each publisher. The filter precedes the annotation, so the filter constrains the objects considered when calculating the annotation.

Here’s another example with the Avg aggregate:

The first query asks for the average rating of all a publisher’s books for publisher’s that have at least one book with a rating exceeding 3.0. The second query asks for the average of a publisher’s book’s ratings for only those ratings exceeding 3.0.

It’s difficult to intuit how the ORM will translate complex querysets into SQL queries so when in doubt, inspect the SQL with str(queryset.query) and write plenty of tests.

Annotations can be used as a basis for ordering. When you define an order_by() clause, the aggregates you provide can reference any alias defined as part of an annotate() clause in the query.

For example, to order a QuerySet of books by the number of authors that have contributed to the book, you could use the following query:

Ordinarily, annotations are generated on a per-object basis - an annotated QuerySet will return one result for each object in the original QuerySet. However, when a values() clause is used to constrain the columns that are returned in the result set, the method for evaluating annotations is slightly different. Instead of returning an annotated result for each result in the original QuerySet, the original results are grouped according to the unique combinations of the fields specified in the values() clause. An annotation is then provided for each unique group; the annotation is computed over all members of the group.

For example, consider an author query that attempts to find out the average rating of books written by each author:

This will return one result for each author in the database, annotated with their average book rating.

However, the result will be slightly different if you use a values() clause:

In this example, the authors will be grouped by name, so you will only get an annotated result for each unique author name. This means if you have two authors with the same name, their results will be merged into a single result in the output of the query; the average will be computed as the average over the books written by both authors.

As with the filter() clause, the order in which annotate() and values() clauses are applied to a query is significant. If the values() clause precedes the annotate(), the annotation will be computed using the grouping described by the values() clause.

However, if the annotate() clause precedes the values() clause, the annotations will be generated over the entire query set. In this case, the values() clause only constrains the fields that are generated on output.

For example, if we reverse the order of the values() and annotate() clause from our previous example:

This will now yield one unique result for each author; however, only the author’s name and the average_rating annotation will be returned in the output data.

You should also note that average_rating has been explicitly included in the list of values to be returned. This is required because of the ordering of the values() and annotate() clause.

If the values() clause precedes the annotate() clause, any annotations will be automatically added to the result set. However, if the values() clause is applied after the annotate() clause, you need to explicitly include the aggregate column.

Fields that are mentioned in the order_by() part of a queryset are used when selecting the output data, even if they are not otherwise specified in the values() call. These extra fields are used to group “like” results together and they can make otherwise identical result rows appear to be separate. This shows up, particularly, when counting things.

By way of example, suppose you have a model like this:

If you want to count how many times each distinct data value appears in an ordered queryset, you might try this:

…which will group the Item objects by their common data values and then count the number of id values in each group. Except that it won’t quite work. The ordering by name will also play a part in the grouping, so this query will group by distinct (data, name) pairs, which isn’t what you want. Instead, you should construct this queryset:

…clearing any ordering in the query. You could also order by, say, data without any harmful effects, since that is already playing a role in the query.

This behavior is the same as that noted in the queryset documentation for distinct() and the general rule is the same: normally you won’t want extra columns playing a part in the result, so clear out the ordering, or at least make sure it’s restricted only to those fields you also select in a values() call.

You might reasonably ask why Django doesn’t remove the extraneous columns for you. The main reason is consistency with distinct() and other places: Django never removes ordering constraints that you have specified explicitly with order_by() (and we can’t change those other methods’ behavior, as that would violate our API stability policy).

Default ordering not applied to GROUP BY

GROUP BY queries (for example, those using .values() and .annotate()) don’t use the model’s default ordering. Use order_by() explicitly when a given order is needed.

You can also generate an aggregate on the result of an annotation. When you define an aggregate() clause, the aggregates you provide can reference any alias defined as part of an annotate() clause in the query.

For example, if you wanted to calculate the average number of authors per book you first annotate the set of books with the author count, then aggregate that author count, referencing the annotation field:

When an aggregation is applied to an empty queryset or grouping, the result defaults to its default parameter, typically None. This behavior occurs because aggregate functions return NULL when the executed query returns no rows.

You can specify a return value by providing the default argument for most aggregations. However, since Count does not support the default argument, it will always return 0 for empty querysets or groups.

For example, assuming that no book contains web in its name, calculating the total price for this book set would return None since there are no matching rows to compute the Sum aggregation on:

However, the default argument can be set when calling Sum to return a different default value if no books can be found:

Under the hood, the default argument is implemented by wrapping the aggregate function with Coalesce.

When using the values() clause to group query results for annotations in MySQL with the ONLY_FULL_GROUP_BY SQL mode enabled, you may need to apply AnyValue if the annotation includes a mix of aggregate and non-aggregate expressions.

Take the following example:

This creates groups of books based on the SQL column GREATEST(pages, 600). One unique group consists of books with 600 pages or less, and other unique groups will consist of books with the same pages. The pages_per_author annotation is composed of aggregate and non-aggregate expressions, num_authors is an aggregate expression while greatest_page isn’t.

Since the grouping is based on the greatest_pages expression, MySQL may be unable to determine that greatest_pages (used in the pages_per_author expression) is functionally dependent on the grouped column. As a result, it may raise an error like:

To avoid this, you can wrap the non-aggregate expression with AnyValue.

Other supported databases do not encounter the OperationalError in the example above because they can detect the functional dependency. In general, AnyValue is useful when dealing with select list columns that involve non-aggregate functions or complex expressions not recognized by the database as functionally dependent on the columns in the grouping clause.

The AnyValue aggregate was added.

---

## Asynchronous support¶

**URL:** https://docs.djangoproject.com/en/stable/topics/async/

**Contents:**
- Asynchronous support¶
- Async views¶
  - Decorators¶
  - Queries & the ORM¶
  - Performance¶
  - Handling disconnects¶
- Async safety¶
- Async adapter functions¶
  - async_to_sync()¶
  - sync_to_async()¶

Django has support for writing asynchronous (“async”) views, along with an entirely async-enabled request stack if you are running under ASGI. Async views will still work under WSGI, but with performance penalties, and without the ability to have efficient long-running requests.

We’re still working on async support for the ORM and other parts of Django. You can expect to see this in future releases. For now, you can use the sync_to_async() adapter to interact with the sync parts of Django. There is also a whole range of async-native Python libraries that you can integrate with.

Any view can be declared async by making the callable part of it return a coroutine - commonly, this is done using async def. For a function-based view, this means declaring the whole view using async def. For a class-based view, this means declaring the HTTP method handlers, such as get() and post() as async def (not its __init__(), or as_view()).

Django uses asgiref.sync.iscoroutinefunction to test if your view is asynchronous or not. If you implement your own method of returning a coroutine, ensure you use asgiref.sync.markcoroutinefunction so this function returns True.

Under a WSGI server, async views will run in their own, one-off event loop. This means you can use async features, like concurrent async HTTP requests, without any issues, but you will not get the benefits of an async stack.

The main benefits are the ability to service hundreds of connections without using Python threads. This allows you to use slow streaming, long-polling, and other exciting response types.

If you want to use these, you will need to deploy Django using ASGI instead.

You will only get the benefits of a fully-asynchronous request stack if you have no synchronous middleware loaded into your site. If there is a piece of synchronous middleware, then Django must use a thread per request to safely emulate a synchronous environment for it.

Middleware can be built to support both sync and async contexts. Some of Django’s middleware is built like this, but not all. To see what middleware Django has to adapt for, you can turn on debug logging for the django.request logger and look for log messages about “Asynchronous handler adapted for middleware …”.

In both ASGI and WSGI mode, you can still safely use asynchronous support to run code concurrently rather than serially. This is especially handy when dealing with external APIs or data stores.

If you want to call a part of Django that is still synchronous, you will need to wrap it in a sync_to_async() call. For example:

If you accidentally try to call a part of Django that is synchronous-only from an async view, you will trigger Django’s asynchronous safety protection to protect your data from corruption.

The following decorators can be used with both synchronous and asynchronous view functions:

csp_report_only_override()

requires_csrf_token()

sensitive_variables()

sensitive_post_parameters()

require_http_methods()

xframe_options_deny()

xframe_options_sameorigin()

xframe_options_exempt()

With some exceptions, Django can run ORM queries asynchronously as well:

Detailed notes can be found in Asynchronous queries, but in short:

All QuerySet methods that cause an SQL query to occur have an a-prefixed asynchronous variant.

async for is supported on all QuerySets (including the output of values() and values_list().)

Django also supports some asynchronous model methods that use the database:

Transactions do not yet work in async mode. If you have a piece of code that needs transactions behavior, we recommend you write that piece as a single synchronous function and call it using sync_to_async().

Persistent database connections, set via the CONN_MAX_AGE setting, should also be disabled in async mode. Instead, use your database backend’s built-in connection pooling if available, or investigate a third-party connection pooling option if required.

When running in a mode that does not match the view (e.g. an async view under WSGI, or a traditional sync view under ASGI), Django must emulate the other call style to allow your code to run. This context-switch causes a small performance penalty of around a millisecond.

This is also true of middleware. Django will attempt to minimize the number of context-switches between sync and async. If you have an ASGI server, but all your middleware and views are synchronous, it will switch just once, before it enters the middleware stack.

However, if you put synchronous middleware between an ASGI server and an asynchronous view, it will have to switch into sync mode for the middleware and then back to async mode for the view. Django will also hold the sync thread open for middleware exception propagation. This may not be noticeable at first, but adding this penalty of one thread per request can remove any async performance advantage.

You should do your own performance testing to see what effect ASGI versus WSGI has on your code. In some cases, there may be a performance increase even for a purely synchronous codebase under ASGI because the request-handling code is still all running asynchronously. In general you will only want to enable ASGI mode if you have asynchronous code in your project.

For long-lived requests, a client may disconnect before the view returns a response. In this case, an asyncio.CancelledError will be raised in the view. You can catch this error and handle it if you need to perform any cleanup:

You can also handle client disconnects in streaming responses.

Certain key parts of Django are not able to operate safely in an async environment, as they have global state that is not coroutine-aware. These parts of Django are classified as “async-unsafe”, and are protected from execution in an async environment. The ORM is the main example, but there are other parts that are also protected in this way.

If you try to run any of these parts from a thread where there is a running event loop, you will get a SynchronousOnlyOperation error. Note that you don’t have to be inside an async function directly to have this error occur. If you have called a sync function directly from an async function, without using sync_to_async() or similar, then it can also occur. This is because your code is still running in a thread with an active event loop, even though it may not be declared as async code.

If you encounter this error, you should fix your code to not call the offending code from an async context. Instead, write your code that talks to async-unsafe functions in its own, sync function, and call that using asgiref.sync.sync_to_async() (or any other way of running sync code in its own thread).

The async context can be imposed upon you by the environment in which you are running your Django code. For example, Jupyter notebooks and IPython interactive shells both transparently provide an active event loop so that it is easier to interact with asynchronous APIs.

If you’re using an IPython shell, you can disable this event loop by running:

as a command at the IPython prompt. This will allow you to run synchronous code without generating SynchronousOnlyOperation errors; however, you also won’t be able to await asynchronous APIs. To turn the event loop back on, run:

If you’re in an environment other than IPython (or you can’t turn off autoawait in IPython for some reason), you are certain there is no chance of your code being run concurrently, and you absolutely need to run your sync code from an async context, then you can disable the warning by setting the DJANGO_ALLOW_ASYNC_UNSAFE environment variable to any value.

If you enable this option and there is concurrent access to the async-unsafe parts of Django, you may suffer data loss or corruption. Be very careful and do not use this in production environments.

If you need to do this from within Python, do that with os.environ:

It is necessary to adapt the calling style when calling sync code from an async context, or vice-versa. For this there are two adapter functions, from the asgiref.sync module: async_to_sync() and sync_to_async(). They are used to transition between the calling styles while preserving compatibility.

These adapter functions are widely used in Django. The asgiref package itself is part of the Django project, and it is automatically installed as a dependency when you install Django with pip.

Takes an async function and returns a sync function that wraps it. Can be used as either a direct wrapper or a decorator:

The async function is run in the event loop for the current thread, if one is present. If there is no current event loop, a new event loop is spun up specifically for the single async invocation and shut down again once it completes. In either situation, the async function will execute on a different thread to the calling code.

Threadlocals and contextvars values are preserved across the boundary in both directions.

async_to_sync() is essentially a more powerful version of the asyncio.run() function in Python’s standard library. As well as ensuring threadlocals work, it also enables the thread_sensitive mode of sync_to_async() when that wrapper is used below it.

Takes a sync function and returns an async function that wraps it. Can be used as either a direct wrapper or a decorator:

Threadlocals and contextvars values are preserved across the boundary in both directions.

Sync functions tend to be written assuming they all run in the main thread, so sync_to_async() has two threading modes:

thread_sensitive=True (the default): the sync function will run in the same thread as all other thread_sensitive functions. This will be the main thread, if the main thread is synchronous and you are using the async_to_sync() wrapper.

thread_sensitive=False: the sync function will run in a brand new thread which is then closed once the invocation completes.

asgiref version 3.3.0 changed the default value of the thread_sensitive parameter to True. This is a safer default, and in many cases interacting with Django the correct value, but be sure to evaluate uses of sync_to_async() if updating asgiref from a prior version.

Thread-sensitive mode is quite special, and does a lot of work to run all functions in the same thread. Note, though, that it relies on usage of async_to_sync() above it in the stack to correctly run things on the main thread. If you use asyncio.run() or similar, it will fall back to running thread-sensitive functions in a single, shared thread, but this will not be the main thread.

The reason this is needed in Django is that many libraries, specifically database adapters, require that they are accessed in the same thread that they were created in. Also a lot of existing Django code assumes it all runs in the same thread, e.g. middleware adding things to a request for later use in views.

Rather than introduce potential compatibility issues with this code, we instead opted to add this mode so that all existing Django sync code runs in the same thread and thus is fully compatible with async mode. Note that sync code will always be in a different thread to any async code that is calling it, so you should avoid passing raw database handles or other thread-sensitive references around.

In practice this restriction means that you should not pass features of the database connection object when calling sync_to_async(). Doing so will trigger the thread safety checks:

Rather, you should encapsulate all database access within a helper function that can be called with sync_to_async() without relying on the connection object in the calling code.

---

## Built-in class-based generic views¶

**URL:** https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-display/

**Contents:**
- Built-in class-based generic views¶
- Extending generic views¶
- Generic views of objects¶
  - Making “friendly” template contexts¶
  - Adding extra context¶
  - Viewing subsets of objects¶
  - Dynamic filtering¶
  - Performing extra work¶

Writing web applications can be monotonous, because we repeat certain patterns again and again. Django tries to take away some of that monotony at the model and template layers, but web developers also experience this boredom at the view level.

Django’s generic views were developed to ease that pain. They take certain common idioms and patterns found in view development and abstract them so that you can quickly write common views of data without having to write too much code.

We can recognize certain common tasks, like displaying a list of objects, and write code that displays a list of any object. Then the model in question can be passed as an extra argument to the URLconf.

Django ships with generic views to do the following:

Display list and detail pages for a single object. If we were creating an application to manage conferences then a TalkListView and a RegisteredUserListView would be examples of list views. A single talk page is an example of what we call a “detail” view.

Present date-based objects in year/month/day archive pages, associated detail, and “latest” pages.

Allow users to create, update, and delete objects – with or without authorization.

Taken together, these views provide interfaces to perform the most common tasks developers encounter.

There’s no question that using generic views can speed up development substantially. In most projects, however, there comes a moment when the generic views no longer suffice. Indeed, the most common question asked by new Django developers is how to make generic views handle a wider array of situations.

This is one of the reasons generic views were redesigned for the 1.3 release - previously, they were view functions with a bewildering array of options; now, rather than passing in a large amount of configuration in the URLconf, the recommended way to extend generic views is to subclass them, and override their attributes or methods.

That said, generic views will have a limit. If you find you’re struggling to implement your view as a subclass of a generic view, then you may find it more effective to write just the code you need, using your own class-based or functional views.

More examples of generic views are available in some third party applications, or you could write your own as needed.

TemplateView certainly is useful, but Django’s generic views really shine when it comes to presenting views of your database content. Because it’s such a common task, Django comes with a handful of built-in generic views to help generate list and detail views of objects.

Let’s start by looking at some examples of showing a list of objects or an individual object.

We’ll be using these models:

Now we need to define a view:

Finally hook that view into your urls:

That’s all the Python code we need to write. We still need to write a template, however. We could explicitly tell the view which template to use by adding a template_name attribute to the view, but in the absence of an explicit template Django will infer one from the object’s name. In this case, the inferred template will be "books/publisher_list.html" – the “books” part comes from the name of the app that defines the model, while the “publisher” bit is the lowercased version of the model’s name.

Thus, when (for example) the APP_DIRS option of a DjangoTemplates backend is set to True in TEMPLATES, a template location could be: /path/to/project/books/templates/books/publisher_list.html

This template will be rendered against a context containing a variable called object_list that contains all the publisher objects. A template might look like this:

That’s really all there is to it. All the cool features of generic views come from changing the attributes set on the generic view. The generic views reference documents all the generic views and their options in detail; the rest of this document will consider some of the common ways you might customize and extend generic views.

You might have noticed that our sample publisher list template stores all the publishers in a variable named object_list. While this works just fine, it isn’t all that “friendly” to template authors: they have to “just know” that they’re dealing with publishers here.

Well, if you’re dealing with a model object, this is already done for you. When you are dealing with an object or queryset, Django is able to populate the context using the lowercased version of the model class’ name. This is provided in addition to the default object_list entry, but contains exactly the same data, i.e. publisher_list.

If this still isn’t a good match, you can manually set the name of the context variable. The context_object_name attribute on a generic view specifies the context variable to use:

Providing a useful context_object_name is always a good idea. Your coworkers who design templates will thank you.

Often you need to present some extra information beyond that provided by the generic view. For example, think of showing a list of all the books on each publisher detail page. The DetailView generic view provides the publisher to the context, but how do we get additional information in that template?

The answer is to subclass DetailView and provide your own implementation of the get_context_data method. The default implementation adds the object being displayed to the template, but you can override it to send more:

Generally, get_context_data will merge the context data of all parent classes with those of the current class. To preserve this behavior in your own classes where you want to alter the context, you should be sure to call get_context_data on the super class. When no two classes try to define the same key, this will give the expected results. However if any class attempts to override a key after parent classes have set it (after the call to super), any children of that class will also need to explicitly set it after super if they want to be sure to override all parents. If you’re having trouble, review the method resolution order of your view.

Another consideration is that the context data from class-based generic views will override data provided by context processors; see get_context_data() for an example.

Now let’s take a closer look at the model argument we’ve been using all along. The model argument, which specifies the database model that the view will operate upon, is available on all the generic views that operate on a single object or a collection of objects. However, the model argument is not the only way to specify the objects that the view will operate upon – you can also specify the list of objects using the queryset argument:

Specifying model = Publisher is shorthand for saying queryset = Publisher.objects.all(). However, by using queryset to define a filtered list of objects you can be more specific about the objects that will be visible in the view (see Making queries for more information about QuerySet objects, and see the class-based views reference for the complete details).

To pick an example, we might want to order a list of books by publication date, with the most recent first:

That’s a pretty minimal example, but it illustrates the idea nicely. You’ll usually want to do more than just reorder objects. If you want to present a list of books by a particular publisher, you can use the same technique:

Notice that along with a filtered queryset, we’re also using a custom template name. If we didn’t, the generic view would use the same template as the “vanilla” object list, which might not be what we want.

Also notice that this isn’t a very elegant way of doing publisher-specific books. If we want to add another publisher page, we’d need another handful of lines in the URLconf, and more than a few publishers would get unreasonable. We’ll deal with this problem in the next section.

If you get a 404 when requesting /books/acme/, check to ensure you actually have a Publisher with the name ‘ACME Publishing’. Generic views have an allow_empty parameter for this case. See the class-based-views reference for more details.

Another common need is to filter down the objects given in a list page by some key in the URL. Earlier we hardcoded the publisher’s name in the URLconf, but what if we wanted to write a view that displayed all the books by some arbitrary publisher?

Handily, the ListView has a get_queryset() method we can override. By default, it returns the value of the queryset attribute, but we can use it to add more logic.

The key part to making this work is that when class-based views are called, various useful things are stored on self; as well as the request (self.request) this includes the positional (self.args) and name-based (self.kwargs) arguments captured according to the URLconf.

Here, we have a URLconf with a single captured group:

Next, we’ll write the PublisherBookListView view itself:

Using get_queryset to add logic to the queryset selection is as convenient as it is powerful. For instance, if we wanted, we could use self.request.user to filter using the current user, or other more complex logic.

We can also add the publisher into the context at the same time, so we can use it in the template:

The last common pattern we’ll look at involves doing some extra work before or after calling the generic view.

Imagine we had a last_accessed field on our Author model that we were using to keep track of the last time anybody looked at that author:

The generic DetailView class wouldn’t know anything about this field, but once again we could write a custom view to keep that field updated.

First, we’d need to add an author detail bit in the URLconf to point to a custom view:

Then we’d write our new view – get_object is the method that retrieves the object – so we override it and wrap the call:

The URLconf here uses the named group pk - this name is the default name that DetailView uses to find the value of the primary key used to filter the queryset.

If you want to call the group something else, you can set pk_url_kwarg on the view.

---

## Class-based views¶

**URL:** https://docs.djangoproject.com/en/stable/topics/class-based-views/

**Contents:**
- Class-based views¶
- Basic examples¶
- Usage in your URLconf¶
- Subclassing generic views¶
  - Supporting other HTTP methods¶
- Asynchronous class-based views¶

A view is a callable which takes a request and returns a response. This can be more than just a function, and Django provides an example of some classes which can be used as views. These allow you to structure your views and reuse code by harnessing inheritance and mixins. There are also some generic views for tasks which we’ll get to later, but you may want to design your own structure of reusable views which suits your use case. For full details, see the class-based views reference documentation.

Django provides base view classes which will suit a wide range of applications. All views inherit from the View class, which handles linking the view into the URLs, HTTP method dispatching and other common features. RedirectView provides a HTTP redirect, and TemplateView extends the base class to make it also render a template.

The most direct way to use generic views is to create them directly in your URLconf. If you’re only changing a few attributes on a class-based view, you can pass them into the as_view() method call itself:

Any arguments passed to as_view() will override attributes set on the class. In this example, we set template_name on the TemplateView. A similar overriding pattern can be used for the url attribute on RedirectView.

The second, more powerful way to use generic views is to inherit from an existing view and override attributes (such as the template_name) or methods (such as get_context_data) in your subclass to provide new values or methods. Consider, for example, a view that just displays one template, about.html. Django has a generic view to do this - TemplateView - so we can subclass it, and override the template name:

Then we need to add this new view into our URLconf. TemplateView is a class, not a function, so we point the URL to the as_view() class method instead, which provides a function-like entry to class-based views:

For more information on how to use the built in generic views, consult the next topic on generic class-based views.

Suppose somebody wants to access our book library over HTTP using the views as an API. The API client would connect every now and then and download book data for the books published since last visit. But if no new books appeared since then, it is a waste of CPU time and bandwidth to fetch the books from the database, render a full response and send it to the client. It might be preferable to ask the API when the most recent book was published.

We map the URL to book list view in the URLconf:

If the view is accessed from a GET request, an object list is returned in the response (using the book_list.html template). But if the client issues a HEAD request, the response has an empty body and the Last-Modified header indicates when the most recent book was published. Based on this information, the client may or may not download the full object list.

As well as the synchronous (def) method handlers already shown, View subclasses may define asynchronous (async def) method handlers to leverage asynchronous code using await:

Within a single view-class, all user-defined method handlers must be either synchronous, using def, or all asynchronous, using async def. An ImproperlyConfigured exception will be raised in as_view() if def and async def declarations are mixed.

Django will automatically detect asynchronous views and run them in an asynchronous context. You can read more about Django’s asynchronous support, and how to best use async views, in Asynchronous support.

---

## Database access optimization¶

**URL:** https://docs.djangoproject.com/en/stable/topics/db/optimization/

**Contents:**
- Database access optimization¶
- Profile first¶
- Use standard DB optimization techniques¶
- Understand QuerySets¶
  - Understand QuerySet evaluation¶
  - Understand cached attributes¶
  - Use the with template tag¶
  - Use iterator()¶
  - Use explain()¶
- Do database work in the database rather than in Python¶

Django’s database layer provides various ways to help developers get the most out of their databases. This document gathers together links to the relevant documentation, and adds various tips, organized under a number of headings that outline the steps to take when attempting to optimize your database usage.

As general programming practice, this goes without saying. Find out what queries you are doing and what they are costing you. Use QuerySet.explain() to understand how specific QuerySets are executed by your database. You may also want to use an external project like django-debug-toolbar, or a tool that monitors your database directly.

Remember that you may be optimizing for speed or memory or both, depending on your requirements. Sometimes optimizing for one will be detrimental to the other, but sometimes they will help each other. Also, work that is done by the database process might not have the same cost (to you) as the same amount of work done in your Python process. It is up to you to decide what your priorities are, where the balance must lie, and profile all of these as required since this will depend on your application and server.

With everything that follows, remember to profile after every change to ensure that the change is a benefit, and a big enough benefit given the decrease in readability of your code. All of the suggestions below come with the caveat that in your circumstances the general principle might not apply, or might even be reversed.

Indexes. This is a number one priority, after you have determined from profiling what indexes should be added. Use Meta.indexes or Field.db_index to add these from Django. Consider adding indexes to fields that you frequently query using filter(), exclude(), order_by(), etc. as indexes may help to speed up lookups. Note that determining the best indexes is a complex database-dependent topic that will depend on your particular application. The overhead of maintaining an index may outweigh any gains in query speed.

Appropriate use of field types.

We will assume you have done the things listed above. The rest of this document focuses on how to use Django in such a way that you are not doing unnecessary work. This document also does not address other optimization techniques that apply to all expensive operations, such as general purpose caching.

Understanding QuerySets is vital to getting good performance with simple code. In particular:

To avoid performance problems, it is important to understand:

that QuerySets are lazy.

when they are evaluated.

how the data is held in memory.

As well as caching of the whole QuerySet, there is caching of the result of attributes on ORM objects. In general, attributes that are not callable will be cached. For example, assuming the example blog models:

But in general, callable attributes cause DB lookups every time:

Be careful when reading template code - the template system does not allow use of parentheses, but will call callables automatically, hiding the above distinction.

Be careful with your own custom properties - it is up to you to implement caching when required, for example using the cached_property decorator.

To make use of the caching behavior of QuerySet, you may need to use the with template tag.

When you have a lot of objects, the caching behavior of the QuerySet can cause a large amount of memory to be used. In this case, iterator() may help.

QuerySet.explain() gives you detailed information about how the database executes a query, including indexes and joins that are used. These details may help you find queries that could be rewritten more efficiently, or identify indexes that could be added to improve performance.

At the most basic level, use filter and exclude to do filtering in the database.

Use F expressions to filter based on other fields within the same model.

Use annotate to do aggregation in the database.

If these aren’t enough to generate the SQL you need:

A less portable but more powerful method is the RawSQL expression, which allows some SQL to be explicitly added to the query. If that still isn’t powerful enough:

Write your own custom SQL to retrieve data or populate models. Use django.db.connection.queries to find out what Django is writing for you and start from there.

There are two reasons to use a column with unique or db_index when using get() to retrieve individual objects. First, the query will be quicker because of the underlying database index. Also, the query could run much slower if multiple objects match the lookup; having a unique constraint on the column guarantees this will never happen.

So using the example blog models:

will be quicker than:

because id is indexed by the database and is guaranteed to be unique.

Doing the following is potentially quite slow:

First of all, headline is not indexed, which will make the underlying database fetch slower.

Second, the lookup doesn’t guarantee that only one object will be returned. If the query matches more than one object, it will retrieve and transfer all of them from the database. This penalty could be substantial if hundreds or thousands of records are returned. The penalty will be compounded if the database lives on a separate server, where network overhead and latency also play a factor.

Hitting the database multiple times for different parts of a single ‘set’ of data that you will need all parts of is, in general, less efficient than retrieving it all in one query. This is particularly important if you have a query that is executed in a loop, and could therefore end up doing many database queries, when only one was needed. So:

Understand select_related() and prefetch_related() thoroughly, and use them:

in managers and default managers where appropriate. Be aware when your manager is and is not used; sometimes this is tricky so don’t make assumptions.

in view code or other layers, possibly making use of prefetch_related_objects() where needed.

When you only want a dict or list of values, and don’t need ORM model objects, make appropriate usage of values(). These can be useful for replacing model objects in template code - as long as the dicts you supply have the same attributes as those used in the template, you are fine.

Use defer() and only() if there are database columns you know that you won’t need (or won’t need in most cases) to avoid loading them. Note that if you do use them, the ORM will have to go and get them in a separate query, making this a pessimization if you use it inappropriately.

Don’t be too aggressive in deferring fields without profiling as the database has to read most of the non-text, non-VARCHAR data from the disk for a single row in the results, even if it ends up only using a few columns. The defer() and only() methods are most useful when you can avoid loading a lot of text data or for fields that might take a lot of processing to convert back to Python. As always, profile first, then optimize.

…if you only want to find out if obj is in the queryset, rather than if obj in queryset.

…if you only want the count, rather than doing len(queryset).

…if you only want to find out if at least one result exists, rather than if queryset.

If you are going to need other data from the QuerySet, evaluate it immediately.

For example, assuming a Group model that has a many-to-many relation to User, the following code is optimal:

It is optimal because:

Since QuerySets are lazy, this does no database queries if display_group_members is False.

Storing group.members.all() in the members variable allows its result cache to be reused.

The line if members: causes QuerySet.__bool__() to be called, which causes the group.members.all() query to be run on the database. If there aren’t any results, it will return False, otherwise True.

The line if current_user in members: checks if the user is in the result cache, so no additional database queries are issued.

The use of len(members) calls QuerySet.__len__(), reusing the result cache, so again, no database queries are issued.

The for member loop iterates over the result cache.

In total, this code does either one or zero database queries. The only deliberate optimization performed is using the members variable. Using QuerySet.exists() for the if, QuerySet.contains() for the in, or QuerySet.count() for the count would each cause additional queries.

Rather than retrieve a load of objects, set some values, and save them individual, use a bulk SQL UPDATE statement, via QuerySet.update(). Similarly, do bulk deletes where possible.

Note, however, that these bulk update methods cannot call the save() or delete() methods of individual instances, which means that any custom behavior you have added for these methods will not be executed, including anything driven from the normal database object signals.

If you only need a foreign key value, use the foreign key value that is already on the object you’ve got, rather than getting the whole related object and taking its primary key. i.e. do:

Ordering is not free; each field to order by is an operation the database must perform. If a model has a default ordering (Meta.ordering) and you don’t need it, remove it on a QuerySet by calling order_by() with no parameters.

Adding an index to your database may help to improve ordering performance.

Use bulk methods to reduce the number of SQL statements.

When creating objects, where possible, use the bulk_create() method to reduce the number of SQL queries. For example:

Note that there are a number of caveats to this method, so make sure it’s appropriate for your use case.

When updating objects, where possible, use the bulk_update() method to reduce the number of SQL queries. Given a list or queryset of objects:

The following example:

Note that there are a number of caveats to this method, so make sure it’s appropriate for your use case.

When inserting objects into ManyToManyFields, use add() with multiple objects to reduce the number of SQL queries. For example:

…where Band and Artist are models with a many-to-many relationship.

When inserting different pairs of objects into ManyToManyField or when the custom through table is defined, use bulk_create() method to reduce the number of SQL queries. For example:

…where Pizza and Topping have a many-to-many relationship. Note that there are a number of caveats to this method, so make sure it’s appropriate for your use case.

When removing objects from ManyToManyFields, use remove() with multiple objects to reduce the number of SQL queries. For example:

…where Band and Artist are models with a many-to-many relationship.

When removing different pairs of objects from ManyToManyFields, use delete() on a Q expression with multiple through model instances to reduce the number of SQL queries. For example:

…where Pizza and Topping have a many-to-many relationship.

---

## Database transactions¶

**URL:** https://docs.djangoproject.com/en/stable/topics/db/transactions/

**Contents:**
- Database transactions¶
- Managing database transactions¶
  - Django’s default transaction behavior¶
  - Tying transactions to HTTP requests¶
  - Controlling transactions explicitly¶
- Autocommit¶
  - Why Django uses autocommit¶
  - Deactivating transaction management¶
- Performing actions after commit¶
  - Savepoints¶

Django gives you a few ways to control how database transactions are managed.

Django’s default behavior is to run in autocommit mode. Each query is immediately committed to the database, unless a transaction is active. See below for details.

Django uses transactions or savepoints automatically to guarantee the integrity of ORM operations that require multiple queries, especially delete() and update() queries.

Django’s TestCase class also wraps each test in a transaction for performance reasons.

A common way to handle transactions on the web is to wrap each request in a transaction. Set ATOMIC_REQUESTS to True in the configuration of each database for which you want to enable this behavior.

It works like this. Before calling a view function, Django starts a transaction. If the response is produced without problems, Django commits the transaction. If the view produces an exception, Django rolls back the transaction.

You may perform subtransactions using savepoints in your view code, typically with the atomic() context manager. However, at the end of the view, either all or none of the changes will be committed.

While the simplicity of this transaction model is appealing, it also makes it inefficient when traffic increases. Opening a transaction for every view has some overhead. The impact on performance depends on the query patterns of your application and on how well your database handles locking.

Per-request transactions and streaming responses

When a view returns a StreamingHttpResponse, reading the contents of the response will often execute code to generate the content. Since the view has already returned, such code runs outside of the transaction.

Generally speaking, it isn’t advisable to write to the database while generating a streaming response, since there’s no sensible way to handle errors after starting to send the response.

In practice, this feature wraps every view function in the atomic() decorator described below.

Note that only the execution of your view is enclosed in the transactions. Middleware runs outside of the transaction, and so does the rendering of template responses.

When ATOMIC_REQUESTS is enabled, it’s still possible to prevent views from running in a transaction.

This decorator will negate the effect of ATOMIC_REQUESTS for a given view:

It only works if it’s applied to the view itself.

Django provides a single API to control database transactions.

Atomicity is the defining property of database transactions. atomic allows us to create a block of code within which the atomicity on the database is guaranteed. If the block of code is successfully completed, the changes are committed to the database. If there is an exception, the changes are rolled back.

atomic blocks can be nested. In this case, when an inner block completes successfully, its effects can still be rolled back if an exception is raised in the outer block at a later point.

It is sometimes useful to ensure an atomic block is always the outermost atomic block, ensuring that any database changes are committed when the block is exited without errors. This is known as durability and can be achieved by setting durable=True. If the atomic block is nested within another it raises a RuntimeError.

atomic is usable both as a decorator:

and as a context manager:

Wrapping atomic in a try/except block allows for natural handling of integrity errors:

In this example, even if generate_relationships() causes a database error by breaking an integrity constraint, you can execute queries in add_children(), and the changes from create_parent() are still there and bound to the same transaction. Note that any operations attempted in generate_relationships() will already have been rolled back safely when handle_exception() is called, so the exception handler can also operate on the database if necessary.

Avoid catching exceptions inside atomic!

When exiting an atomic block, Django looks at whether it’s exited normally or with an exception to determine whether to commit or roll back. If you catch and handle exceptions inside an atomic block, you may hide from Django the fact that a problem has happened. This can result in unexpected behavior.

This is mostly a concern for DatabaseError and its subclasses such as IntegrityError. After such an error, the transaction is broken and Django will perform a rollback at the end of the atomic block. If you attempt to run database queries before the rollback happens, Django will raise a TransactionManagementError. You may also encounter this behavior when an ORM-related signal handler raises an exception.

The correct way to catch database errors is around an atomic block as shown above. If necessary, add an extra atomic block for this purpose. This pattern has another advantage: it delimits explicitly which operations will be rolled back if an exception occurs.

If you catch exceptions raised by raw SQL queries, Django’s behavior is unspecified and database-dependent.

You may need to manually revert app state when rolling back a transaction.

The values of a model’s fields won’t be reverted when a transaction rollback happens. This could lead to an inconsistent model state unless you manually restore the original field values.

For example, given MyModel with an active field, this snippet ensures that the if obj.active check at the end uses the correct value if updating active to True fails in the transaction:

This also applies to any other mechanism that may hold app state, such as caching or global variables. For example, if the code proactively updates data in the cache after saving an object, it’s recommended to use transaction.on_commit() instead, to defer cache alterations until the transaction is actually committed.

In order to guarantee atomicity, atomic disables some APIs. Attempting to commit, roll back, or change the autocommit state of the database connection within an atomic block will raise an exception.

atomic takes a using argument which should be the name of a database. If this argument isn’t provided, Django uses the "default" database.

Under the hood, Django’s transaction management code:

opens a transaction when entering the outermost atomic block;

creates a savepoint when entering an inner atomic block;

releases or rolls back to the savepoint when exiting an inner block;

commits or rolls back the transaction when exiting the outermost block.

You can disable the creation of savepoints for inner blocks by setting the savepoint argument to False. If an exception occurs, Django will perform the rollback when exiting the first parent block with a savepoint if there is one, and the outermost block otherwise. Atomicity is still guaranteed by the outer transaction. This option should only be used if the overhead of savepoints is noticeable. It has the drawback of breaking the error handling described above.

You may use atomic when autocommit is turned off. It will only use savepoints, even for the outermost block.

Performance considerations

Open transactions have a performance cost for your database server. To minimize this overhead, keep your transactions as short as possible. This is especially important if you’re using atomic() in long-running processes, outside of Django’s request / response cycle.

In the SQL standards, each SQL query starts a transaction, unless one is already active. Such transactions must then be explicitly committed or rolled back.

This isn’t always convenient for application developers. To alleviate this problem, most databases provide an autocommit mode. When autocommit is turned on and no transaction is active, each SQL query gets wrapped in its own transaction. In other words, not only does each such query start a transaction, but the transaction also gets automatically committed or rolled back, depending on whether the query succeeded.

PEP 249, the Python Database API Specification v2.0, requires autocommit to be initially turned off. Django overrides this default and turns autocommit on.

To avoid this, you can deactivate the transaction management, but it isn’t recommended.

You can totally disable Django’s transaction management for a given database by setting AUTOCOMMIT to False in its configuration. If you do this, Django won’t enable autocommit, and won’t perform any commits. You’ll get the regular behavior of the underlying database library.

This requires you to commit explicitly every transaction, even those started by Django or by third-party libraries. Thus, this is best used in situations where you want to run your own transaction-controlling middleware or do something really strange.

Sometimes you need to perform an action related to the current database transaction, but only if the transaction successfully commits. Examples might include a background task, an email notification, or a cache invalidation.

on_commit() allows you to register callbacks that will be executed after the open transaction is successfully committed:

Pass a function, or any callable, to on_commit():

Callbacks will not be passed any arguments, but you can bind them with functools.partial():

Callbacks are called after the open transaction is successfully committed. If the transaction is instead rolled back (typically when an unhandled exception is raised in an atomic() block), the callback will be discarded, and never called.

If you call on_commit() while there isn’t an open transaction, the callback will be executed immediately.

It’s sometimes useful to register callbacks that can fail. Passing robust=True allows the next callbacks to be executed even if the current one throws an exception. All errors derived from Python’s Exception class are caught and logged to the django.db.backends.base logger.

You can use TestCase.captureOnCommitCallbacks() to test callbacks registered with on_commit().

Savepoints (i.e. nested atomic() blocks) are handled correctly. That is, an on_commit() callable registered after a savepoint (in a nested atomic() block) will be called after the outer transaction is committed, but not if a rollback to that savepoint or any previous savepoint occurred during the transaction:

On the other hand, when a savepoint is rolled back (due to an exception being raised), the inner callable will not be called:

On-commit functions for a given transaction are executed in the order they were registered.

If one on-commit function registered with robust=False within a given transaction raises an uncaught exception, no later registered functions in that same transaction will run. This is the same behavior as if you’d executed the functions sequentially yourself without on_commit().

Your callbacks are executed after a successful commit, so a failure in a callback will not cause the transaction to roll back. They are executed conditionally upon the success of the transaction, but they are not part of the transaction. For the intended use cases (mail notifications, background tasks, etc.), this should be fine. If it’s not (if your follow-up action is so critical that its failure should mean the failure of the transaction itself), then you don’t want to use the on_commit() hook. Instead, you may want two-phase commit such as the psycopg Two-Phase Commit protocol support and the optional Two-Phase Commit Extensions in the Python DB-API specification.

Callbacks are not run until autocommit is restored on the connection following the commit (because otherwise any queries done in a callback would open an implicit transaction, preventing the connection from going back into autocommit mode).

When in autocommit mode and outside of an atomic() block, the function will run immediately, not on commit.

On-commit functions only work with autocommit mode and the atomic() (or ATOMIC_REQUESTS) transaction API. Calling on_commit() when autocommit is disabled and you are not within an atomic block will result in an error.

Django’s TestCase class wraps each test in a transaction and rolls back that transaction after each test, in order to provide test isolation. This means that no transaction is ever actually committed, thus your on_commit() callbacks will never be run.

You can overcome this limitation by using TestCase.captureOnCommitCallbacks(). This captures your on_commit() callbacks in a list, allowing you to make assertions on them, or emulate the transaction committing by calling them.

Another way to overcome the limitation is to use TransactionTestCase instead of TestCase. This will mean your transactions are committed, and the callbacks will run. However TransactionTestCase flushes the database between tests, which is significantly slower than TestCase's isolation.

A rollback hook is harder to implement robustly than a commit hook, since a variety of things can cause an implicit rollback.

For instance, if your database connection is dropped because your process was killed without a chance to shut down gracefully, your rollback hook will never run.

But there is a solution: instead of doing something during the atomic block (transaction) and then undoing it if the transaction fails, use on_commit() to delay doing it in the first place until after the transaction succeeds. It’s a lot easier to undo something you never did in the first place!

Always prefer atomic() if possible at all. It accounts for the idiosyncrasies of each database and prevents invalid operations.

The low level APIs are only useful if you’re implementing your own transaction management.

Django provides an API in the django.db.transaction module to manage the autocommit state of each database connection.

These functions take a using argument which should be the name of a database. If it isn’t provided, Django uses the "default" database.

Autocommit is initially turned on. If you turn it off, it’s your responsibility to restore it.

Once you turn autocommit off, you get the default behavior of your database adapter, and Django won’t help you. Although that behavior is specified in PEP 249, implementations of adapters aren’t always consistent with one another. Review the documentation of the adapter you’re using carefully.

You must ensure that no transaction is active, usually by issuing a commit() or a rollback(), before turning autocommit back on.

Django will refuse to turn autocommit off when an atomic() block is active, because that would break atomicity.

A transaction is an atomic set of database queries. Even if your program crashes, the database guarantees that either all the changes will be applied, or none of them.

Django doesn’t provide an API to start a transaction. The expected way to start a transaction is to disable autocommit with set_autocommit().

Once you’re in a transaction, you can choose either to apply the changes you’ve performed until this point with commit(), or to cancel them with rollback(). These functions are defined in django.db.transaction.

These functions take a using argument which should be the name of a database. If it isn’t provided, Django uses the "default" database.

Django will refuse to commit or to rollback when an atomic() block is active, because that would break atomicity.

A savepoint is a marker within a transaction that enables you to roll back part of a transaction, rather than the full transaction. Savepoints are available with the SQLite, PostgreSQL, Oracle, and MySQL (when using the InnoDB storage engine) backends. Other backends provide the savepoint functions, but they’re empty operations – they don’t actually do anything.

Savepoints aren’t especially useful if you are using autocommit, the default behavior of Django. However, once you open a transaction with atomic(), you build up a series of database operations awaiting a commit or rollback. If you issue a rollback, the entire transaction is rolled back. Savepoints provide the ability to perform a fine-grained rollback, rather than the full rollback that would be performed by transaction.rollback().

When the atomic() decorator is nested, it creates a savepoint to allow partial commit or rollback. You’re strongly encouraged to use atomic() rather than the functions described below, but they’re still part of the public API, and there’s no plan to deprecate them.

Each of these functions takes a using argument which should be the name of a database for which the behavior applies. If no using argument is provided then the "default" database is used.

Savepoints are controlled by three functions in django.db.transaction:

Creates a new savepoint. This marks a point in the transaction that is known to be in a “good” state. Returns the savepoint ID (sid).

Releases savepoint sid. The changes performed since the savepoint was created become part of the transaction.

Rolls back the transaction to savepoint sid.

These functions do nothing if savepoints aren’t supported or if the database is in autocommit mode.

In addition, there’s a utility function:

Resets the counter used to generate unique savepoint IDs.

The following example demonstrates the use of savepoints:

Savepoints may be used to recover from a database error by performing a partial rollback. If you’re doing this inside an atomic() block, the entire block will still be rolled back, because it doesn’t know you’ve handled the situation at a lower level! To prevent this, you can control the rollback behavior with the following functions.

Setting the rollback flag to True forces a rollback when exiting the innermost atomic block. This may be useful to trigger a rollback without raising an exception.

Setting it to False prevents such a rollback. Before doing that, make sure you’ve rolled back the transaction to a known-good savepoint within the current atomic block! Otherwise you’re breaking atomicity and data corruption may occur.

While SQLite supports savepoints, a flaw in the design of the sqlite3 module makes them hardly usable.

When autocommit is enabled, savepoints don’t make sense. When it’s disabled, sqlite3 commits implicitly before savepoint statements. (In fact, it commits before any statement other than SELECT, INSERT, UPDATE, DELETE and REPLACE.) This bug has two consequences:

The low level APIs for savepoints are only usable inside a transaction i.e. inside an atomic() block.

It’s impossible to use atomic() when autocommit is turned off.

If you’re using MySQL, your tables may or may not support transactions; it depends on your MySQL version and the table types you’re using. (By “table types,” we mean something like “InnoDB” or “MyISAM”.) MySQL transaction peculiarities are outside the scope of this article, but the MySQL site has information on MySQL transactions.

If your MySQL setup does not support transactions, then Django will always function in autocommit mode: statements will be executed and committed as soon as they’re called. If your MySQL setup does support transactions, Django will handle transactions as explained in this document.

This section is relevant only if you’re implementing your own transaction management. This problem cannot occur in Django’s default mode and atomic() handles it automatically.

Inside a transaction, when a call to a PostgreSQL cursor raises an exception (typically IntegrityError), all subsequent SQL in the same transaction will fail with the error “current transaction is aborted, queries ignored until end of transaction block”. While the basic use of save() is unlikely to raise an exception in PostgreSQL, there are more advanced usage patterns which might, such as saving objects with unique fields, saving using the force_insert/force_update flag, or invoking custom SQL.

There are several ways to recover from this sort of error.

The first option is to roll back the entire transaction. For example:

Calling transaction.rollback() rolls back the entire transaction. Any uncommitted database operations will be lost. In this example, the changes made by a.save() would be lost, even though that operation raised no error itself.

You can use savepoints to control the extent of a rollback. Before performing a database operation that could fail, you can set or update the savepoint; that way, if the operation fails, you can roll back the single offending operation, rather than the entire transaction. For example:

In this example, a.save() will not be undone in the case where b.save() raises an exception.

---

## Django shortcut functions¶

**URL:** https://docs.djangoproject.com/en/stable/topics/http/shortcuts/

**Contents:**
- Django shortcut functions¶
- render()¶
  - Required arguments¶
  - Optional arguments¶
  - Example¶
- redirect()¶
  - Examples¶
- resolve_url()¶
  - Examples¶
- get_object_or_404()¶

The package django.shortcuts collects helper functions and classes that “span” multiple levels of MVC. In other words, these functions/classes introduce controlled coupling for convenience’s sake.

Combines a given template with a given context dictionary and returns an HttpResponse object with that rendered text.

Django does not provide a shortcut function which returns a TemplateResponse because the constructor of TemplateResponse offers the same level of convenience as render().

The request object used to generate this response.

The full name of a template to use or sequence of template names. If a sequence is given, the first template that exists will be used. See the template loading documentation for more information on how templates are found.

A dictionary of values to add to the template context. By default, this is an empty dictionary. If a value in the dictionary is callable, the view will call it just before rendering the template.

The MIME type to use for the resulting document. Defaults to 'text/html'.

The status code for the response. Defaults to 200.

The NAME of a template engine to use for loading the template.

The following example renders the template myapp/index.html with the MIME type application/xhtml+xml:

This example is equivalent to:

Returns an HttpResponseRedirect to the appropriate URL for the arguments passed.

The arguments could be:

A model: the model’s get_absolute_url() function will be called.

A view name, possibly with arguments: reverse() will be used to reverse-resolve the name.

An absolute or relative URL, which will be used as-is for the redirect location.

By default, a temporary redirect is issued with a 302 status code. If permanent=True, a permanent redirect is issued with a 301 status code.

If preserve_request=True, the response instructs the user agent to preserve the method and body of the original request when issuing the redirect. In this case, temporary redirects use a 307 status code, and permanent redirects use a 308 status code. This is better illustrated in the following table:

The argument preserve_request was added.

You can use the redirect() function in a number of ways.

By passing some object; that object’s get_absolute_url() method will be called to figure out the redirect URL:

By passing the name of a view and optionally some positional or keyword arguments; the URL will be reverse resolved using the reverse() method:

By passing a hardcoded URL to redirect to:

This also works with full URLs:

By default, redirect() returns a temporary redirect. All of the above forms accept a permanent argument; if set to True a permanent redirect will be returned:

Additionally, the preserve_request argument can be used to preserve the original HTTP method:

Returns a URL string by resolving and normalizing the given to argument into a concrete URL. The parameter to may be:

An object implementing get_absolute_url(), in which case the method will be called and its result returned.

A view name, view function, or view class, possibly with arguments passed as *args and **kwargs, in which case reverse() will be used to reverse-resolve the view.

A URL string, which will be returned unchanged.

This function is used internally by the redirect() shortcut to determine the target URL for the redirect location.

Resolving a URL for a model that defines get_absolute_url():

Resolving a target URL for use outside of a redirect, such as in an HTTP response header:

Asynchronous version: aget_object_or_404()

Calls get() on a given model manager, but it raises Http404 instead of the model’s DoesNotExist exception.

A Model class, a Manager, or a QuerySet instance from which to get the object.

Lookup parameters, which should be in the format accepted by get() and filter().

The following example gets the object with the primary key of 1 from MyModel:

This example is equivalent to:

The most common use case is to pass a Model, as shown above. However, you can also pass a QuerySet instance:

The above example is a bit contrived since it’s equivalent to doing:

but it can be useful if you are passed the queryset variable from somewhere else.

Finally, you can also use a Manager. This is useful for example if you have a custom manager:

You can also use related managers:

Note: As with get(), a MultipleObjectsReturned exception will be raised if more than one object is found.

Asynchronous version: aget_list_or_404()

Returns the result of filter() on a given model manager cast to a list, raising Http404 if the resulting list is empty.

A Model, Manager or QuerySet instance from which to get the list.

Lookup parameters, which should be in the format accepted by get() and filter().

The following example gets all published objects from MyModel:

This example is equivalent to:

---

## File Uploads¶

**URL:** https://docs.djangoproject.com/en/stable/topics/http/file-uploads/

**Contents:**
- File Uploads¶
- Basic file uploads¶
  - Handling uploaded files with a model¶
  - Uploading multiple files¶
- Upload Handlers¶
  - Where uploaded data is stored¶
  - Changing upload handler behavior¶
  - Modifying upload handlers on the fly¶

When Django handles a file upload, the file data ends up placed in request.FILES (for more on the request object see the documentation for request and response objects). This document explains how files are stored on disk and in memory, and how to customize the default behavior.

There are security risks if you are accepting uploaded content from untrusted users! See the security guide’s topic on User-uploaded content for mitigation details.

Consider a form containing a FileField:

A view handling this form will receive the file data in request.FILES, which is a dictionary containing a key for each FileField (or ImageField, or other FileField subclass) in the form. So the data from the above form would be accessible as request.FILES['file'].

Note that request.FILES will only contain data if the request method was POST, at least one file field was actually posted, and the <form> that posted the request has the attribute enctype="multipart/form-data". Otherwise, request.FILES will be empty.

Most of the time, you’ll pass the file data from request into the form as described in Binding uploaded files to a form. This would look something like:

Notice that we have to pass request.FILES into the form’s constructor; this is how file data gets bound into a form.

Here’s a common way you might handle an uploaded file:

Looping over UploadedFile.chunks() instead of using read() ensures that large files don’t overwhelm your system’s memory.

There are a few other methods and attributes available on UploadedFile objects; see UploadedFile for a complete reference.

If you’re saving a file on a Model with a FileField, using a ModelForm makes this process much easier. The file object will be saved to the location specified by the upload_to argument of the corresponding FileField when calling form.save():

If you are constructing an object manually, you can assign the file object from request.FILES to the file field in the model:

If you are constructing an object manually outside of a request, you can assign a File like object to the FileField:

If you want to upload multiple files using one form field, create a subclass of the field’s widget and set its allow_multiple_selected class attribute to True.

In order for such files to be all validated by your form (and have the value of the field include them all), you will also have to subclass FileField. See below for an example.

Django is likely to have a proper multiple file field support at some point in the future.

Then override the form_valid() method of your FormView subclass to handle multiple file uploads:

This will allow you to handle multiple files at the form level only. Be aware that you cannot use it to put multiple files on a single model instance (in a single field), for example, even if the custom widget is used with a form field related to a model FileField.

When a user uploads a file, Django passes off the file data to an upload handler – a small class that handles file data as it gets uploaded. Upload handlers are initially defined in the FILE_UPLOAD_HANDLERS setting, which defaults to:

Together MemoryFileUploadHandler and TemporaryFileUploadHandler provide Django’s default file upload behavior of reading small files into memory and large ones onto disk.

You can write custom handlers that customize how Django handles files. You could, for example, use custom handlers to enforce user-level quotas, compress data on the fly, render progress bars, and even send data to another storage location directly without storing it locally. See Writing custom upload handlers for details on how you can customize or completely replace upload behavior.

Before you save uploaded files, the data needs to be stored somewhere.

By default, if an uploaded file is smaller than 2.5 megabytes, Django will hold the entire contents of the upload in memory. This means that saving the file involves only a read from memory and a write to disk and thus is very fast.

However, if an uploaded file is too large, Django will write the uploaded file to a temporary file stored in your system’s temporary directory. On a Unix-like platform this means you can expect Django to generate a file called something like /tmp/tmpzfp6I6.upload. If an upload is large enough, you can watch this file grow in size as Django streams the data onto disk.

These specifics – 2.5 megabytes; /tmp; etc. – are “reasonable defaults” which can be customized as described in the next section.

There are a few settings which control Django’s file upload behavior. See File Upload Settings for details.

Sometimes particular views require different upload behavior. In these cases, you can override upload handlers on a per-request basis by modifying request.upload_handlers. By default, this list will contain the upload handlers given by FILE_UPLOAD_HANDLERS, but you can modify the list as you would any other list.

For instance, suppose you’ve written a ProgressBarUploadHandler that provides feedback on upload progress to some sort of AJAX widget. You’d add this handler to your upload handlers like this:

Using list.insert(), as shown above, ensures that the progress bar handler is placed at the beginning of the list. Since upload handlers are executed in order, this placement guarantees that the progress bar handler runs before the default handlers, allowing it to track progress across the entire upload.

If you want to replace the upload handlers completely, you can assign a new list:

You can only modify upload handlers before accessing request.POST or request.FILES – it doesn’t make sense to change upload handlers after upload handling has already started. If you try to modify request.upload_handlers after reading from request.POST or request.FILES Django will throw an error.

Thus, you should always modify uploading handlers as early in your view as possible.

Also, request.POST is accessed by CsrfViewMiddleware which is enabled by default. This means you will need to use csrf_exempt() on your view to allow you to change the upload handlers. You will then need to use csrf_protect() on the function that actually processes the request. Note that this means that the handlers may start receiving the file upload before the CSRF checks have been done. Example code:

If you are using a class-based view, you will need to use csrf_exempt() on its dispatch() method and csrf_protect() on the method that actually processes the request. Example code:

---

## Form handling with class-based views¶

**URL:** https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-editing/

**Contents:**
- Form handling with class-based views¶
- Basic forms¶
- Model forms¶
- Models and request.user¶
- Content negotiation example¶

Form processing generally has 3 paths:

Initial GET (blank or prepopulated form)

POST with invalid data (typically redisplay form with errors)

POST with valid data (process the data and typically redirect)

Implementing this yourself often results in a lot of repeated boilerplate code (see Using a form in a view). To help avoid this, Django provides a collection of generic class-based views for form processing.

Given a contact form:

The view can be constructed using a FormView:

FormView inherits TemplateResponseMixin so template_name can be used here.

The default implementation for form_valid() simply redirects to the success_url.

Generic views really shine when working with models. These generic views will automatically create a ModelForm, so long as they can work out which model class to use:

If the model attribute is given, that model class will be used.

If get_object() returns an object, the class of that object will be used.

If a queryset is given, the model for that queryset will be used.

Model form views provide a form_valid() implementation that saves the model automatically. You can override this if you have any special requirements; see below for examples.

You don’t even need to provide a success_url for CreateView or UpdateView - they will use get_absolute_url() on the model object if available.

If you want to use a custom ModelForm (for instance to add extra validation), set form_class on your view.

When specifying a custom form class, you must still specify the model, even though the form_class may be a ModelForm.

First we need to add get_absolute_url() to our Author class:

Then we can use CreateView and friends to do the actual work. Notice how we’re just configuring the generic class-based views here; we don’t have to write any logic ourselves:

We have to use reverse_lazy() instead of reverse(), as the urls are not loaded when the file is imported.

The fields attribute works the same way as the fields attribute on the inner Meta class on ModelForm. Unless you define the form class in another way, the attribute is required and the view will raise an ImproperlyConfigured exception if it’s not.

If you specify both the fields and form_class attributes, an ImproperlyConfigured exception will be raised.

Finally, we hook these new views into the URLconf:

These views inherit SingleObjectTemplateResponseMixin which uses template_name_suffix to construct the template_name based on the model.

CreateView and UpdateView use myapp/author_form.html

DeleteView uses myapp/author_confirm_delete.html

If you wish to have separate templates for CreateView and UpdateView, you can set either template_name or template_name_suffix on your view class.

To track the user that created an object using a CreateView, you can use a custom ModelForm to do this. First, add the foreign key relation to the model:

In the view, ensure that you don’t include created_by in the list of fields to edit, and override form_valid() to add the user:

LoginRequiredMixin prevents users who aren’t logged in from accessing the form. If you omit that, you’ll need to handle unauthorized users in form_valid().

Here is an example showing how you might go about implementing a form that works with an API-based workflow as well as ‘normal’ form POSTs:

The above example assumes that if the client supports text/html, that they would prefer it. However, this may not always be true. When requesting a .css file, many browsers will send the header Accept: text/css,*/*;q=0.1, indicating that they would prefer CSS, but anything else is fine. This means request.accepts("text/html") will be True.

To determine the correct format, taking into consideration the client’s preference, use django.http.HttpRequest.get_preferred_type():

The HttpRequest.get_preferred_type() method was added.

---

## Making queries¶

**URL:** https://docs.djangoproject.com/en/stable/topics/db/queries/

**Contents:**
- Making queries¶
- Creating objects¶
- Saving changes to objects¶
  - Saving ForeignKey and ManyToManyField fields¶
- Retrieving objects¶
  - Retrieving all objects¶
  - Retrieving specific objects with filters¶
    - Chaining filters¶
    - Filtered QuerySets are unique¶
    - QuerySets are lazy¶

Once you’ve created your data models, Django automatically gives you a database-abstraction API that lets you create, retrieve, update and delete objects. This document explains how to use this API. Refer to the data model reference for full details of all the various model lookup options.

Throughout this guide (and in the reference), we’ll refer to the following models, which comprise a blog application:

To represent database-table data in Python objects, Django uses an intuitive system: A model class represents a database table, and an instance of that class represents a particular record in the database table.

To create an object, instantiate it using keyword arguments to the model class, then call save() to save it to the database.

Assuming models live in a models.py file inside a blog Django app, here is an example:

This performs an INSERT SQL statement behind the scenes. Django doesn’t hit the database until you explicitly call save().

The save() method has no return value.

save() takes a number of advanced options not described here. See the documentation for save() for complete details.

To create and save an object in a single step, use the create() method.

To save changes to an object that’s already in the database, use save().

Given a Blog instance b5 that has already been saved to the database, this example changes its name and updates its record in the database:

This performs an UPDATE SQL statement behind the scenes. Django doesn’t hit the database until you explicitly call save().

Updating a ForeignKey field works exactly the same way as saving a normal field – assign an object of the right type to the field in question. This example updates the blog attribute of an Entry instance entry, assuming appropriate instances of Entry and Blog are already saved to the database (so we can retrieve them below):

Updating a ManyToManyField works a little differently – use the add() method on the field to add a record to the relation. This example adds the Author instance joe to the entry object:

To add multiple records to a ManyToManyField in one go, include multiple arguments in the call to add(), like this:

Django will complain if you try to assign or add an object of the wrong type.

To retrieve objects from your database, construct a QuerySet via a Manager on your model class.

A QuerySet represents a collection of objects from your database. It can have zero, one or many filters. Filters narrow down the query results based on the given parameters. In SQL terms, a QuerySet equates to a SELECT statement, and a filter is a limiting clause such as WHERE or LIMIT.

You get a QuerySet by using your model’s Manager. Each model has at least one Manager, and it’s called objects by default. Access it directly via the model class, like so:

A Manager is accessible only via model classes, rather than from model instances, to enforce a separation between “table-level” operations and “record-level” operations.

The Manager is the main source of querysets for a model. For example, Blog.objects.all() returns a QuerySet that contains all Blog objects in the database.

The simplest way to retrieve objects from a table is to get all of them. To do this, use the all() method on a Manager:

The all() method returns a QuerySet of all the objects in the database.

The QuerySet returned by all() describes all objects in the database table. Usually, though, you’ll need to select only a subset of the complete set of objects.

To create such a subset, you refine the initial QuerySet, adding filter conditions. The two most common ways to refine a QuerySet are:

Returns a new QuerySet containing objects that match the given lookup parameters.

Returns a new QuerySet containing objects that do not match the given lookup parameters.

The lookup parameters (**kwargs in the above function definitions) should be in the format described in Field lookups below.

For example, to get a QuerySet of blog entries from the year 2006, use filter() like so:

With the default manager class, it is the same as:

The result of refining a QuerySet is itself a QuerySet, so it’s possible to chain refinements together. For example:

This takes the initial QuerySet of all entries in the database, adds a filter, then an exclusion, then another filter. The final result is a QuerySet containing all entries with a headline that starts with “What”, that were published between January 30, 2005, and the current day.

Each time you refine a QuerySet, you get a brand-new QuerySet that is in no way bound to the previous QuerySet. Each refinement creates a separate and distinct QuerySet that can be stored, used and reused.

These three querysets are separate. The first is a base QuerySet containing all entries that contain a headline starting with “What”. The second is a subset of the first, with an additional criteria that excludes records whose pub_date is today or in the future. The third is a subset of the first, with an additional criteria that selects only the records whose pub_date is today or in the future. The initial QuerySet (q1) is unaffected by the refinement process.

QuerySet objects are lazy – the act of creating a QuerySet doesn’t involve any database activity. You can stack filters together all day long, and Django won’t actually run the query until the QuerySet is evaluated. Take a look at this example:

Though this looks like three database hits, in fact it hits the database only once, at the last line (print(q)). In general, the results of a QuerySet aren’t fetched from the database until you “ask” for them. When you do, the QuerySet is evaluated by accessing the database. For more details on exactly when evaluation takes place, see When QuerySets are evaluated.

filter() will always give you a QuerySet, even if only a single object matches the query - in this case, it will be a QuerySet containing a single element.

If you know there is only one object that matches your query, you can use the get() method on a Manager which returns the object directly:

You can use any query expression with get(), just like with filter() - again, see Field lookups below.

Note that there is a difference between using get(), and using filter() with a slice of [0]. If there are no results that match the query, get() will raise a DoesNotExist exception. This exception is an attribute of the model class that the query is being performed on - so in the code above, if there is no Entry object with a primary key of 1, Django will raise Entry.DoesNotExist.

Similarly, Django will complain if more than one item matches the get() query. In this case, it will raise MultipleObjectsReturned, which again is an attribute of the model class itself.

Most of the time you’ll use all(), get(), filter() and exclude() when you need to look up objects from the database. However, that’s far from all there is; see the QuerySet API Reference for a complete list of all the various QuerySet methods.

Use a subset of Python’s array-slicing syntax to limit your QuerySet to a certain number of results. This is the equivalent of SQL’s LIMIT and OFFSET clauses.

For example, this returns the first 5 objects (LIMIT 5):

This returns the sixth through tenth objects (OFFSET 5 LIMIT 5):

Negative indexing (i.e. Entry.objects.all()[-1]) is not supported.

Generally, slicing a QuerySet returns a new QuerySet – it doesn’t evaluate the query. An exception is if you use the “step” parameter of Python slice syntax. For example, this would actually execute the query in order to return a list of every second object of the first 10:

Further filtering or ordering of a sliced queryset is prohibited due to the ambiguous nature of how that might work.

To retrieve a single object rather than a list (e.g. SELECT foo FROM bar LIMIT 1), use an index instead of a slice. For example, this returns the first Entry in the database, after ordering entries alphabetically by headline:

This is roughly equivalent to:

Note, however, that the first of these will raise IndexError while the second will raise DoesNotExist if no objects match the given criteria. See get() for more details.

Field lookups are how you specify the meat of an SQL WHERE clause. They’re specified as keyword arguments to the QuerySet methods filter(), exclude() and get().

Basic lookups keyword arguments take the form field__lookuptype=value. (That’s a double-underscore). For example:

translates (roughly) into the following SQL:

Python has the ability to define functions that accept arbitrary name-value arguments whose names and values are evaluated at runtime. For more information, see Keyword Arguments in the official Python tutorial.

The field specified in a lookup has to be the name of a model field. There’s one exception though, in case of a ForeignKey you can specify the field name suffixed with _id. In this case, the value parameter is expected to contain the raw value of the foreign model’s primary key. For example:

If you pass an invalid keyword argument, a lookup function will raise TypeError.

The database API supports about two dozen lookup types; a complete reference can be found in the field lookup reference. To give you a taste of what’s available, here’s some of the more common lookups you’ll probably use:

An “exact” match. For example:

Would generate SQL along these lines:

If you don’t provide a lookup type – that is, if your keyword argument doesn’t contain a double underscore – the lookup type is assumed to be exact.

For example, the following two statements are equivalent:

This is for convenience, because exact lookups are the common case.

A case-insensitive match. So, the query:

Would match a Blog titled "Beatles Blog", "beatles blog", or even "BeAtlES blOG".

Case-sensitive containment test. For example:

Roughly translates to this SQL:

Note this will match the headline 'Today Lennon honored' but not 'today lennon honored'.

There’s also a case-insensitive version, icontains.

Starts-with and ends-with search, respectively. There are also case-insensitive versions called istartswith and iendswith.

Again, this only scratches the surface. A complete reference can be found in the field lookup reference.

Django offers a powerful and intuitive way to “follow” relationships in lookups, taking care of the SQL JOINs for you automatically, behind the scenes. To span a relationship, use the field name of related fields across models, separated by double underscores, until you get to the field you want.

This example retrieves all Entry objects with a Blog whose name is 'Beatles Blog':

This spanning can be as deep as you’d like.

It works backwards, too. While it can be customized, by default you refer to a “reverse” relationship in a lookup using the lowercase name of the model.

This example retrieves all Blog objects which have at least one Entry whose headline contains 'Lennon':

If you are filtering across multiple relationships and one of the intermediate models doesn’t have a value that meets the filter condition, Django will treat it as if there is an empty (all values are NULL), but valid, object there. All this means is that no error will be raised. For example, in this filter:

(if there was a related Author model), if there was no author associated with an entry, it would be treated as if there was also no name attached, rather than raising an error because of the missing author. Usually this is exactly what you want to have happen. The only case where it might be confusing is if you are using isnull. Thus:

will return Blog objects that have an empty name on the author and also those which have an empty author on the entry. If you don’t want those latter objects, you could write:

When spanning a ManyToManyField or a reverse ForeignKey (such as from Blog to Entry), filtering on multiple attributes raises the question of whether to require each attribute to coincide in the same related object. We might seek blogs that have an entry from 2008 with “Lennon” in its headline, or we might seek blogs that merely have any entry from 2008 as well as some newer or older entry with “Lennon” in its headline.

To select all blogs containing at least one entry from 2008 having “Lennon” in its headline (the same entry satisfying both conditions), we would write:

Otherwise, to perform a more permissive query selecting any blogs with merely some entry with “Lennon” in its headline and some entry from 2008, we would write:

Suppose there is only one blog that has both entries containing “Lennon” and entries from 2008, but that none of the entries from 2008 contained “Lennon”. The first query would not return any blogs, but the second query would return that one blog. (This is because the entries selected by the second filter may or may not be the same as the entries in the first filter. We are filtering the Blog items with each filter statement, not the Entry items.) In short, if each condition needs to match the same related object, then each should be contained in a single filter() call.

As the second (more permissive) query chains multiple filters, it performs multiple joins to the primary model, potentially yielding duplicates.

The behavior of filter() for queries that span multi-value relationships, as described above, is not implemented equivalently for exclude(). Instead, the conditions in a single exclude() call will not necessarily refer to the same item.

For example, the following query would exclude blogs that contain both entries with “Lennon” in the headline and entries published in 2008:

However, unlike the behavior when using filter(), this will not limit blogs based on entries that satisfy both conditions. In order to do that, i.e. to select all blogs that do not contain entries published with “Lennon” that were published in 2008, you need to make two queries:

In the examples given so far, we have constructed filters that compare the value of a model field with a constant. But what if you want to compare the value of a model field with another field on the same model?

Django provides F expressions to allow such comparisons. Instances of F() act as a reference to a model field within a query. These references can then be used in query filters to compare the values of two different fields on the same model instance.

For example, to find a list of all blog entries that have had more comments than pingbacks, we construct an F() object to reference the pingback count, and use that F() object in the query:

Django supports the use of addition, subtraction, multiplication, division, modulo, and power arithmetic with F() objects, both with constants and with other F() objects. To find all the blog entries with more than twice as many comments as pingbacks, we modify the query:

To find all the entries where the rating of the entry is less than the sum of the pingback count and comment count, we would issue the query:

You can also use the double underscore notation to span relationships in an F() object. An F() object with a double underscore will introduce any joins needed to access the related object. For example, to retrieve all the entries where the author’s name is the same as the blog name, we could issue the query:

For date and date/time fields, you can add or subtract a timedelta object. The following would return all entries that were modified more than 3 days after they were published:

The F() objects support bitwise operations by .bitand(), .bitor(), .bitxor(), .bitrightshift(), and .bitleftshift(). For example:

Oracle doesn’t support bitwise XOR operation.

Django supports using transforms in expressions.

For example, to find all Entry objects published in the same year as they were last modified:

To find the earliest year an entry was published, we can issue the query:

This example finds the value of the highest rated entry and the total number of comments on all entries for each year:

For convenience, Django provides a pk lookup shortcut, which stands for “primary key”.

In the example Blog model, the primary key is the id field, so these three statements are equivalent:

The use of pk isn’t limited to __exact queries – any query term can be combined with pk to perform a query on the primary key of a model:

pk lookups also work across joins. For example, these three statements are equivalent:

The field lookups that equate to LIKE SQL statements (iexact, contains, icontains, startswith, istartswith, endswith and iendswith) will automatically escape the two special characters used in LIKE statements – the percent sign and the underscore. (In a LIKE statement, the percent sign signifies a multiple-character wildcard and the underscore signifies a single-character wildcard.)

This means things should work intuitively, so the abstraction doesn’t leak. For example, to retrieve all the entries that contain a percent sign, use the percent sign as any other character:

Django takes care of the quoting for you; the resulting SQL will look something like this:

Same goes for underscores. Both percentage signs and underscores are handled for you transparently.

Each QuerySet contains a cache to minimize database access. Understanding how it works will allow you to write the most efficient code.

In a newly created QuerySet, the cache is empty. The first time a QuerySet is evaluated – and, hence, a database query happens – Django saves the query results in the QuerySet’s cache and returns the results that have been explicitly requested (e.g., the next element, if the QuerySet is being iterated over). Subsequent evaluations of the QuerySet reuse the cached results.

Keep this caching behavior in mind, because it may bite you if you don’t use your QuerySets correctly. For example, the following will create two QuerySets, evaluate them, and throw them away:

That means the same database query will be executed twice, effectively doubling your database load. Also, there’s a possibility the two lists may not include the same database records, because an Entry may have been added or deleted in the split second between the two requests.

To avoid this problem, save the QuerySet and reuse it:

Querysets do not always cache their results. When evaluating only part of the queryset, the cache is checked, but if it is not populated then the items returned by the subsequent query are not cached. Specifically, this means that limiting the queryset using an array slice or an index will not populate the cache.

For example, repeatedly getting a certain index in a queryset object will query the database each time:

However, if the entire queryset has already been evaluated, the cache will be checked instead:

Here are some examples of other actions that will result in the entire queryset being evaluated and therefore populate the cache:

Simply printing the queryset will not populate the cache. This is because the call to __repr__() only returns a slice of the entire queryset.

If you are writing asynchronous views or code, you cannot use the ORM for queries in quite the way we have described above, as you cannot call blocking synchronous code from asynchronous code - it will block up the event loop (or, more likely, Django will notice and raise a SynchronousOnlyOperation to stop that from happening).

Fortunately, you can do many queries using Django’s asynchronous query APIs. Every method that might block - such as get() or delete() - has an asynchronous variant (aget() or adelete()), and when you iterate over results, you can use asynchronous iteration (async for) instead.

The default way of iterating over a query - with for - will result in a blocking database query behind the scenes as Django loads the results at iteration time. To fix this, you can swap to async for:

Be aware that you also can’t do other things that might iterate over the queryset, such as wrapping list() around it to force its evaluation (you can use async for in a comprehension, if you want it).

Because QuerySet methods like filter() and exclude() do not actually run the query - they set up the queryset to run when it’s iterated over - you can use those freely in asynchronous code. For a guide to which methods can keep being used like this, and which have asynchronous versions, read the next section.

Some methods on managers and querysets - like get() and first() - force execution of the queryset and are blocking. Some, like filter() and exclude(), don’t force execution and so are safe to run from asynchronous code. But how are you supposed to tell the difference?

While you could poke around and see if there is an a-prefixed version of the method (for example, we have aget() but not afilter()), there is a more logical way - look up what kind of method it is in the QuerySet reference.

In there, you’ll find the methods on QuerySets grouped into two sections:

Methods that return new querysets: These are the non-blocking ones, and don’t have asynchronous versions. You’re free to use these in any situation, though read the notes on defer() and only() before you use them.

Methods that do not return querysets: These are the blocking ones, and have asynchronous versions - the asynchronous name for each is noted in its documentation, though our standard pattern is to add an a prefix.

Using this distinction, you can work out when you need to use asynchronous versions, and when you don’t. For example, here’s a valid asynchronous query:

filter() returns a queryset, and so it’s fine to keep chaining it inside an asynchronous environment, whereas first() evaluates and returns a model instance - thus, we change to afirst(), and use await at the front of the whole expression in order to call it in an asynchronous-friendly way.

If you forget to put the await part in, you may see errors like “coroutine object has no attribute x” or “<coroutine …>” strings in place of your model instances. If you ever see these, you are missing an await somewhere to turn that coroutine into a real value.

Transactions are not currently supported with asynchronous queries and updates. You will find that trying to use one raises SynchronousOnlyOperation.

If you wish to use a transaction, we suggest you write your ORM code inside a separate, synchronous function and then call that using sync_to_async - see Asynchronous support for more.

Lookups implementation is different in JSONField, mainly due to the existence of key transformations. To demonstrate, we will use the following example model:

As with other fields, storing None as the field’s value will store it as SQL NULL. While not recommended, it is possible to store JSON scalar null instead of SQL NULL by using Value(None, JSONField()).

Whichever of the values is stored, when retrieved from the database, the Python representation of the JSON scalar null is the same as SQL NULL, i.e. None. Therefore, it can be hard to distinguish between them.

This only applies to None as the top-level value of the field. If None is inside a list or dict, it will always be interpreted as JSON null.

When querying, None value will always be interpreted as JSON null. To query for SQL NULL, use isnull:

Unless you are sure you wish to work with SQL NULL values, consider setting null=False and providing a suitable default for empty values, such as default=dict.

Storing JSON scalar null does not violate null=False.

To query based on a given dictionary key, use that key as the lookup name:

Multiple keys can be chained together to form a path lookup:

If the key is an integer, it will be interpreted as an index transform in an array:

If the key is a negative integer, it cannot be used in a filter keyword directly, but you can still use dictionary unpacking to use it in a query:

MySQL, MariaDB, and Oracle

Negative JSON array indices are not supported.

SQLite support for negative JSON array indices was added.

If the key you wish to query by clashes with the name of another lookup, use the contains lookup instead.

To query for missing keys, use the isnull lookup:

The lookup examples given above implicitly use the exact lookup. Key, index, and path transforms can also be chained with: icontains, endswith, iendswith, iexact, regex, iregex, startswith, istartswith, lt, lte, gt, and gte, as well as with Containment and key lookups.

Represents the text value of a key, index, or path transform of JSONField. You can use the double underscore notation in lookup to chain dictionary key and index transforms.

Due to the way in which key-path queries work, exclude() and filter() are not guaranteed to produce exhaustive sets. If you want to include objects that do not have the path, add the isnull lookup.

Since any string could be a key in a JSON object, any lookup other than those listed below will be interpreted as a key lookup. No errors are raised. Be extra careful for typing mistakes, and always check your queries work as you intend.

MariaDB and Oracle users

Using order_by() on key, index, or path transforms will sort the objects using the string representation of the values. This is because MariaDB and Oracle Database do not provide a function that converts JSON values into their equivalent SQL values.

On Oracle Database, using None as the lookup value in an exclude() query will return objects that do not have null as the value at the given path, including objects that do not have the path. On other database backends, the query will return objects that have the path and the value is not null.

On PostgreSQL, if only one key or index is used, the SQL operator -> is used. If multiple operators are used then the #> operator is used.

On SQLite, "true", "false", and "null" string values will always be interpreted as True, False, and JSON null respectively.

The contains lookup is overridden on JSONField. The returned objects are those where the given dict of key-value pairs are all contained in the top-level of the field. For example:

contains is not supported on Oracle and SQLite.

This is the inverse of the contains lookup - the objects returned will be those where the key-value pairs on the object are a subset of those in the value passed. For example:

contained_by is not supported on Oracle and SQLite.

Returns objects where the given key is in the top-level of the data. For example:

Returns objects where all of the given keys are in the top-level of the data. For example:

Returns objects where any of the given keys are in the top-level of the data. For example:

Keyword argument queries – in filter(), etc. – are “AND”ed together. If you need to execute more complex queries (for example, queries with OR statements), you can use Q objects.

A Q object (django.db.models.Q) is an object used to encapsulate a collection of keyword arguments. These keyword arguments are specified as in “Field lookups” above.

For example, this Q object encapsulates a single LIKE query:

Q objects can be combined using the &, |, and ^ operators. When an operator is used on two Q objects, it yields a new Q object.

For example, this statement yields a single Q object that represents the “OR” of two "question__startswith" queries:

This is equivalent to the following SQL WHERE clause:

You can compose statements of arbitrary complexity by combining Q objects with the &, |, and ^ operators and use parenthetical grouping. Also, Q objects can be negated using the ~ operator, allowing for combined lookups that combine both a normal query and a negated (NOT) query:

Each lookup function that takes keyword-arguments (e.g. filter(), exclude(), get()) can also be passed one or more Q objects as positional (not-named) arguments. If you provide multiple Q object arguments to a lookup function, the arguments will be “AND”ed together. For example:

… roughly translates into the SQL:

Lookup functions can mix the use of Q objects and keyword arguments. All arguments provided to a lookup function (be they keyword arguments or Q objects) are “AND”ed together. However, if a Q object is provided, it must precede the definition of any keyword arguments. For example:

… would be a valid query, equivalent to the previous example; but:

… would not be valid.

The OR lookups examples in Django’s unit tests show some possible uses of Q.

To compare two model instances, use the standard Python comparison operator, the double equals sign: ==. Behind the scenes, that compares the primary key values of two models.

Using the Entry example above, the following two statements are equivalent:

If a model’s primary key isn’t called id, no problem. Comparisons will always use the primary key, whatever it’s called. For example, if a model’s primary key field is called name, these two statements are equivalent:

The delete method, conveniently, is named delete(). This method immediately deletes the object and returns the number of objects deleted and a dictionary with the number of deletions per object type. Example:

You can also delete objects in bulk. Every QuerySet has a delete() method, which deletes all members of that QuerySet.

For example, this deletes all Entry objects with a pub_date year of 2005:

Keep in mind that this will, whenever possible, be executed purely in SQL, and so the delete() methods of individual object instances will not necessarily be called during the process. If you’ve provided a custom delete() method on a model class and want to ensure that it is called, you will need to “manually” delete instances of that model (e.g., by iterating over a QuerySet and calling delete() on each object individually) rather than using the bulk delete() method of a QuerySet.

When Django deletes an object, by default it emulates the behavior of the SQL constraint ON DELETE CASCADE – in other words, any objects which had foreign keys pointing at the object to be deleted will be deleted along with it. For example:

This cascade behavior is customizable via the on_delete argument to the ForeignKey.

Note that delete() is the only QuerySet method that is not exposed on a Manager itself. This is a safety mechanism to prevent you from accidentally requesting Entry.objects.delete(), and deleting all the entries. If you do want to delete all the objects, then you have to explicitly request a complete query set:

Although there is no built-in method for copying model instances, it is possible to easily create new instance with all fields’ values copied. In the simplest case, you can set pk to None and _state.adding to True. Using our blog example:

Things get more complicated if you use inheritance. Consider a subclass of Blog:

Due to how inheritance works, you have to set both pk and id to None, and _state.adding to True:

This process doesn’t copy relations that aren’t part of the model’s database table. For example, Entry has a ManyToManyField to Author. After duplicating an entry, you must set the many-to-many relations for the new entry:

For a OneToOneField, you must duplicate the related object and assign it to the new object’s field to avoid violating the one-to-one unique constraint. For example, assuming entry is already duplicated as above:

Note that it is not possible to copy instances of models with deferred fields using this pattern unless values are assigned to them:

Sometimes you want to set a field to a particular value for all the objects in a QuerySet. You can do this with the update() method. For example:

You can only set non-relation fields and ForeignKey fields using this method. To update a non-relation field, provide the new value as a constant. To update ForeignKey fields, set the new value to be the new model instance you want to point to. For example:

The update() method is applied instantly and returns the number of rows matched by the query (which may not be equal to the number of rows updated if some rows already have the new value). The only restriction on the QuerySet being updated is that it can only access one database table: the model’s main table. You can filter based on related fields, but you can only update columns in the model’s main table. Example:

Be aware that the update() method is converted directly to an SQL statement. It is a bulk operation for direct updates. It doesn’t run any save() methods on your models, or emit the pre_save or post_save signals (which are a consequence of calling save()), or honor the auto_now field option. If you want to save every item in a QuerySet and make sure that the save() method is called on each instance, you don’t need any special function to handle that. Loop over them and call save():

Calls to update can also use F expressions to update one field based on the value of another field in the model. This is especially useful for incrementing counters based upon their current value. For example, to increment the pingback count for every entry in the blog:

However, unlike F() objects in filter and exclude clauses, you can’t introduce joins when you use F() objects in an update – you can only reference fields local to the model being updated. If you attempt to introduce a join with an F() object, a FieldError will be raised:

When you define a relationship in a model (i.e., a ForeignKey, OneToOneField, or ManyToManyField), instances of that model will have a convenient API to access the related object(s).

Using the models at the top of this page, for example, an Entry object e can get its associated Blog object by accessing the blog attribute: e.blog.

(Behind the scenes, this functionality is implemented by Python descriptors. This shouldn’t really matter to you, but we point it out here for the curious.)

Django also creates API accessors for the “other” side of the relationship – the link from the related model to the model that defines the relationship. For example, a Blog object b has access to a list of all related Entry objects via the entry_set attribute: b.entry_set.all().

All examples in this section use the sample Blog, Author and Entry models defined at the top of this page.

If a model has a ForeignKey, instances of that model will have access to the related (foreign) object via an attribute of the model.

You can get and set via a foreign-key attribute. As you may expect, changes to the foreign key aren’t saved to the database until you call save(). Example:

If a ForeignKey field has null=True set (i.e., it allows NULL values), you can assign None to remove the relation. Example:

Forward access to one-to-many relationships is cached the first time the related object is accessed. Subsequent accesses to the foreign key on the same object instance are cached. Example:

Note that the select_related() QuerySet method recursively prepopulates the cache of all one-to-many relationships ahead of time. Example:

If a model has a ForeignKey, instances of the foreign-key model will have access to a Manager that returns all instances of the first model. By default, this Manager is named FOO_set, where FOO is the source model name, lowercased. This Manager returns QuerySet instances, which can be filtered and manipulated as described in the “Retrieving objects” section above.

You can override the FOO_set name by setting the related_name parameter in the ForeignKey definition. For example, if the Entry model was altered to blog = ForeignKey(Blog, on_delete=models.CASCADE, related_name='entries'), the above example code would look like this:

By default the RelatedManager used for reverse relations is a subclass of the default manager for that model. If you would like to specify a different manager for a given query you can use the following syntax:

If EntryManager performed default filtering in its get_queryset() method, that filtering would apply to the all() call.

Specifying a custom reverse manager also enables you to call its custom methods:

Interaction with prefetching

When calling prefetch_related() with a reverse relation, the default manager will be used. If you want to prefetch related objects using a custom reverse manager, use Prefetch(). For example:

In addition to the QuerySet methods defined in “Retrieving objects” above, the ForeignKey Manager has additional methods used to handle the set of related objects. A synopsis of each is below, and complete details can be found in the related objects reference.

Adds the specified model objects to the related object set.

Creates a new object, saves it and puts it in the related object set. Returns the newly created object.

Removes the specified model objects from the related object set.

Removes all objects from the related object set.

Replace the set of related objects.

To assign the members of a related set, use the set() method with an iterable of object instances. For example, if e1 and e2 are Entry instances:

If the clear() method is available, any preexisting objects will be removed from the entry_set before all objects in the iterable (in this case, a list) are added to the set. If the clear() method is not available, all objects in the iterable will be added without removing any existing elements.

Each “reverse” operation described in this section has an immediate effect on the database. Every addition, creation and deletion is immediately and automatically saved to the database.

Both ends of a many-to-many relationship get automatic API access to the other end. The API works similar to a “backward” one-to-many relationship, above.

One difference is in the attribute naming: The model that defines the ManyToManyField uses the attribute name of that field itself, whereas the “reverse” model uses the lowercased model name of the original model, plus '_set' (just like reverse one-to-many relationships).

An example makes this easier to understand:

Like ForeignKey, ManyToManyField can specify related_name. In the above example, if the ManyToManyField in Entry had specified related_name='entries', then each Author instance would have an entries attribute instead of entry_set.

Another difference from one-to-many relationships is that in addition to model instances, the add(), set(), and remove() methods on many-to-many relationships accept primary key values. For example, if e1 and e2 are Entry instances, then these set() calls work identically:

When calling filter() on a many-to-many relationship, be aware that the join between Entry and the intermediary model to Author is performed only once, resulting in a restrictive, or “sticky”, filter. Consider the following example:

This filtered query is looking for blog entries that are co-authored by anna and gloria. You would expect it to return the entry e. However, the filter condition, which traverses the many-to-many relationship between Entry and Author, yields an empty QuerySet.

Since the join between Entry and the intermediary model to Author happens only once, no single object of the joined models - i.e., a relation between one author and one entry - can fulfill the query condition (entries that are co-authored by anna and gloria). You can circumvent this behavior by chaining two consecutive filter() calls, resulting in two separate joins and thus a more permissive filter:

exclude() is also sticky

Please note that for this example, exclude() behaves similarly to filter() despite being implemented differently. When traversing the many-to-many relationship, it does not exclude the entry e despite being co-authored by Gloria:

When chaining a second exclude() call, an empty QuerySet is returned, as expected:

However, in other cases, exclude() behaves differently from filter(). See the note in the “Spanning multi-valued relationships” section above.

One-to-one relationships are very similar to many-to-one relationships. If you define a OneToOneField on your model, instances of that model will have access to the related object via an attribute of the model.

The difference comes in “reverse” queries. The related model in a one-to-one relationship also has access to a Manager object, but that Manager represents a single object, rather than a collection of objects:

If no object has been assigned to this relationship, Django will raise a DoesNotExist exception.

Instances can be assigned to the reverse relationship in the same way as you would assign the forward relationship:

Other object-relational mappers require you to define relationships on both sides. The Django developers believe this is a violation of the DRY (Don’t Repeat Yourself) principle, so Django only requires you to define the relationship on one end.

But how is this possible, given that a model class doesn’t know which other model classes are related to it until those other model classes are loaded?

The answer lies in the app registry. When Django starts, it imports each application listed in INSTALLED_APPS, and then the models module inside each application. Whenever a new model class is created, Django adds backward-relationships to any related models. If the related models haven’t been imported yet, Django keeps tracks of the relationships and adds them when the related models eventually are imported.

For this reason, it’s particularly important that all the models you’re using be defined in applications listed in INSTALLED_APPS. Otherwise, backwards relations may not work properly.

Queries involving related objects follow the same rules as queries involving normal value fields. When specifying the value for a query to match, you may use either an object instance itself, or the primary key value for the object.

For example, if you have a Blog object b with id=5, the following three queries would be identical:

If you find yourself needing to write an SQL query that is too complex for Django’s database-mapper to handle, you can fall back on writing SQL by hand. Django has a couple of options for writing raw SQL queries; see Performing raw SQL queries.

Finally, it’s important to note that the Django database layer is merely an interface to your database. You can access your database via other tools, programming languages or database frameworks; there’s nothing Django-specific about your database.

---

## Managers¶

**URL:** https://docs.djangoproject.com/en/stable/topics/db/managers/

**Contents:**
- Managers¶
- Manager names¶
- Custom managers¶
  - Adding extra manager methods¶
  - Modifying a manager’s initial QuerySet¶
  - Default managers¶
  - Base managers¶
    - Using managers for related object access¶
    - Don’t filter away any results in this type of manager subclass¶
  - Calling custom QuerySet methods from the manager¶

A Manager is the interface through which database query operations are provided to Django models. At least one Manager exists for every model in a Django application.

The way Manager classes work is documented in Making queries; this document specifically touches on model options that customize Manager behavior.

By default, Django adds a Manager with the name objects to every Django model class. However, if you want to use objects as a field name, or if you want to use a name other than objects for the Manager, you can rename it on a per-model basis. To rename the Manager for a given class, define a class attribute of type models.Manager() on that model. For example:

Using this example model, Person.objects will generate an AttributeError exception, but Person.people.all() will provide a list of all Person objects.

You can use a custom Manager in a particular model by extending the base Manager class and instantiating your custom Manager in your model.

There are two reasons you might want to customize a Manager: to add extra Manager methods, and/or to modify the initial QuerySet the Manager returns.

Adding extra Manager methods is the preferred way to add “table-level” functionality to your models. (For “row-level” functionality – i.e., functions that act on a single instance of a model object – use Model methods, not custom Manager methods.)

For example, this custom Manager adds a method with_counts():

With this example, you’d use OpinionPoll.objects.with_counts() to get a QuerySet of OpinionPoll objects with the extra num_responses attribute attached.

A custom Manager method can return anything you want. It doesn’t have to return a QuerySet.

Another thing to note is that Manager methods can access self.model to get the model class to which they’re attached.

A Manager’s base QuerySet returns all objects in the system. For example, using this model:

…the statement Book.objects.all() will return all books in the database.

You can override a Manager’s base QuerySet by overriding the Manager.get_queryset() method. get_queryset() should return a QuerySet with the properties you require.

For example, the following model has two Managers – one that returns all objects, and one that returns only the books by Roald Dahl:

With this sample model, Book.objects.all() will return all books in the database, but Book.dahl_objects.all() will only return the ones written by Roald Dahl.

Because get_queryset() returns a QuerySet object, you can use filter(), exclude() and all the other QuerySet methods on it. So these statements are all legal:

This example also pointed out another interesting technique: using multiple managers on the same model. You can attach as many Manager() instances to a model as you’d like. This is a non-repetitive way to define common “filters” for your models.

This example allows you to request Person.authors.all(), Person.editors.all(), and Person.people.all(), yielding predictable results.

If you use custom Manager objects, take note that the first Manager Django encounters (in the order in which they’re defined in the model) has a special status. Django interprets the first Manager defined in a class as the “default” Manager, and several parts of Django (including dumpdata) will use that Manager exclusively for that model. As a result, it’s a good idea to be careful in your choice of default manager in order to avoid a situation where overriding get_queryset() results in an inability to retrieve objects you’d like to work with.

You can specify a custom default manager using Meta.default_manager_name.

If you’re writing some code that must handle an unknown model, for example, in a third-party app that implements a generic view, use this manager (or _base_manager) rather than assuming the model has an objects manager.

By default, Django uses an instance of the Model._base_manager manager class when accessing related objects (e.g. choice.question), not the _default_manager on the related object. This is because Django needs to be able to retrieve the related object, even if it would otherwise be filtered out (and hence be inaccessible) by the default manager.

If the normal base manager class (django.db.models.Manager) isn’t appropriate for your circumstances, you can tell Django which class to use by setting Meta.base_manager_name.

Base managers aren’t used when querying on related models, or when accessing a one-to-many or many-to-many relationship. For example, if the Question model from the tutorial had a deleted field and a base manager that filters out instances with deleted=True, a queryset like Choice.objects.filter(question__name__startswith='What') would include choices related to deleted questions.

This manager is used to access objects that are related to from some other model. In those situations, Django has to be able to see all the objects for the model it is fetching, so that anything which is referred to can be retrieved.

Therefore, you should not override get_queryset() to filter out any rows. If you do so, Django will return incomplete results.

While most methods from the standard QuerySet are accessible directly from the Manager, this is only the case for the extra methods defined on a custom QuerySet if you also implement them on the Manager:

This example allows you to call both authors() and editors() directly from the manager Person.people.

In lieu of the above approach which requires duplicating methods on both the QuerySet and the Manager, QuerySet.as_manager() can be used to create an instance of Manager with a copy of a custom QuerySet’s methods:

The Manager instance created by QuerySet.as_manager() will be virtually identical to the PersonManager from the previous example.

Not every QuerySet method makes sense at the Manager level; for instance we intentionally prevent the QuerySet.delete() method from being copied onto the Manager class.

Methods are copied according to the following rules:

Public methods are copied by default.

Private methods (starting with an underscore) are not copied by default.

Methods with a queryset_only attribute set to False are always copied.

Methods with a queryset_only attribute set to True are never copied.

For advanced usage you might want both a custom Manager and a custom QuerySet. You can do that by calling Manager.from_queryset() which returns a subclass of your base Manager with a copy of the custom QuerySet methods:

You may also store the generated class into a variable:

Here’s how Django handles custom managers and model inheritance:

Managers from base classes are always inherited by the child class, using Python’s normal name resolution order (names on the child class override all others; then come names on the first parent class, and so on).

If no managers are declared on a model and/or its parents, Django automatically creates the objects manager.

The default manager on a class is either the one chosen with Meta.default_manager_name, or the first manager declared on the model, or the default manager of the first parent model.

These rules provide the necessary flexibility if you want to install a collection of custom managers on a group of models, via an abstract base class, but still customize the default manager. For example, suppose you have this base class:

If you use this directly in a child class, objects will be the default manager if you declare no managers in the child class:

If you want to inherit from AbstractBase, but provide a different default manager, you can provide the default manager on the child class:

Here, default_manager is the default. The objects manager is still available, since it’s inherited, but isn’t used as the default.

Finally for this example, suppose you want to add extra managers to the child class, but still use the default from AbstractBase. You can’t add the new manager directly in the child class, as that would override the default and you would have to also explicitly include all the managers from the abstract base class. The solution is to put the extra managers in another base class and introduce it into the inheritance hierarchy after the defaults:

Note that while you can define a custom manager on the abstract model, you can’t invoke any methods using the abstract model. That is:

will raise an exception. This is because managers are intended to encapsulate logic for managing collections of objects. Since you can’t have a collection of abstract objects, it doesn’t make sense to be managing them. If you have functionality that applies to the abstract model, you should put that functionality in a staticmethod or classmethod on the abstract model.

Whatever features you add to your custom Manager, it must be possible to make a shallow copy of a Manager instance; i.e., the following code must work:

Django makes shallow copies of manager objects during certain queries; if your Manager cannot be copied, those queries will fail.

This won’t be an issue for most custom managers. If you are just adding simple methods to your Manager, it is unlikely that you will inadvertently make instances of your Manager uncopyable. However, if you’re overriding __getattr__ or some other private method of your Manager object that controls object state, you should ensure that you don’t affect the ability of your Manager to be copied.

---

## Managing files¶

**URL:** https://docs.djangoproject.com/en/stable/topics/files/

**Contents:**
- Managing files¶
- Using files in models¶
- The File object¶
- File storage¶
  - Storage objects¶
  - The built-in filesystem storage class¶
  - Using a callable¶

This document describes Django’s file access APIs for files such as those uploaded by a user. The lower level APIs are general enough that you could use them for other purposes. If you want to handle “static files” (JS, CSS, etc.), see How to manage static files (e.g. images, JavaScript, CSS).

By default, Django stores files locally, using the MEDIA_ROOT and MEDIA_URL settings. The examples below assume that you’re using these defaults.

However, Django provides ways to write custom file storage systems that allow you to completely customize where and how Django stores files. The second half of this document describes how these storage systems work.

When you use a FileField or ImageField, Django provides a set of APIs you can use to deal with that file.

Consider the following model, using an ImageField to store a photo:

Any Car instance will have a photo attribute that you can use to get at the details of the attached photo:

This object – car.photo in the example – is a File object, which means it has all the methods and attributes described below.

The file is saved as part of saving the model in the database, so the actual file name used on disk cannot be relied on until after the model has been saved.

For example, you can change the file name by setting the file’s name to a path relative to the file storage’s location (MEDIA_ROOT if you are using the default FileSystemStorage):

To save an existing file on disk to a FileField:

While ImageField non-image data attributes, such as height, width, and size are available on the instance, the underlying image data cannot be used without reopening the image. For example:

Internally, Django uses a django.core.files.File instance any time it needs to represent a file.

Most of the time you’ll use a File that Django’s given you (i.e. a file attached to a model as above, or perhaps an uploaded file).

If you need to construct a File yourself, the easiest way is to create one using a Python built-in file object:

Now you can use any of the documented attributes and methods of the File class.

Be aware that files created in this way are not automatically closed. The following approach may be used to close files automatically:

Closing files is especially important when accessing file fields in a loop over a large number of objects. If files are not manually closed after accessing them, the risk of running out of file descriptors may arise. This may lead to the following error:

Behind the scenes, Django delegates decisions about how and where to store files to a file storage system. This is the object that actually understands things like file systems, opening and reading files, etc.

Django’s default file storage is 'django.core.files.storage.FileSystemStorage'. If you don’t explicitly provide a storage system in the default key of the STORAGES setting, this is the one that will be used.

See below for details of the built-in default file storage system, and see How to write a custom storage class for information on writing your own file storage system.

Though most of the time you’ll want to use a File object (which delegates to the proper storage for that file), you can use file storage systems directly. You can create an instance of some custom file storage class, or – often more useful – you can use the global default storage system:

See File storage API for the file storage API.

Django ships with a django.core.files.storage.FileSystemStorage class which implements basic local filesystem file storage.

For example, the following code will store uploaded files under /media/photos regardless of what your MEDIA_ROOT setting is:

Custom storage systems work the same way: you can pass them in as the storage argument to a FileField.

You can use a callable as the storage parameter for FileField or ImageField. This allows you to modify the used storage at runtime, selecting different storages for different environments, for example.

Your callable will be evaluated when your models classes are loaded, and must return an instance of Storage.

In order to set a storage defined in the STORAGES setting you can use storages:

Because the callable is evaluated when your models classes are loaded, if you need to override the STORAGES setting in tests, you should use a LazyObject subclass instead:

The LazyObject delays the evaluation of the storage until it’s actually needed, allowing override_settings() to take effect:

---

## Migrations¶

**URL:** https://docs.djangoproject.com/en/stable/topics/migrations/

**Contents:**
- Migrations¶
- The Commands¶
- Backend Support¶
  - PostgreSQL¶
  - MySQL¶
  - SQLite¶
- Workflow¶
  - Version control¶
- Transactions¶
- Dependencies¶

Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They’re designed to be mostly automatic, but you’ll need to know when to make migrations, when to run them, and the common problems you might run into.

There are several commands which you will use to interact with migrations and Django’s handling of database schema:

migrate, which is responsible for applying and unapplying migrations.

makemigrations, which is responsible for creating new migrations based on the changes you have made to your models.

sqlmigrate, which displays the SQL statements for a migration.

showmigrations, which lists a project’s migrations and their status.

You should think of migrations as a version control system for your database schema. makemigrations is responsible for packaging up your model changes into individual migration files - analogous to commits - and migrate is responsible for applying those to your database.

The migration files for each app live in a “migrations” directory inside of that app, and are designed to be committed to, and distributed as part of, its codebase. You should be making them once on your development machine and then running the same migrations on your colleagues’ machines, your staging machines, and eventually your production machines.

It is possible to override the name of the package which contains the migrations on a per-app basis by modifying the MIGRATION_MODULES setting.

Migrations will run the same way on the same dataset and produce consistent results, meaning that what you see in development and staging is, under the same circumstances, exactly what will happen in production.

Django will make migrations for any change to your models or fields - even options that don’t affect the database - as the only way it can reconstruct a field correctly is to have all the changes in the history, and you might need those options in some data migrations later on (for example, if you’ve set custom validators).

Migrations are supported on all backends that Django ships with, as well as any third-party backends if they have programmed in support for schema alteration (done via the SchemaEditor class).

However, some databases are more capable than others when it comes to schema migrations; some of the caveats are covered below.

PostgreSQL is the most capable of all the databases here in terms of schema support.

MySQL lacks support for transactions around schema alteration operations, meaning that if a migration fails to apply you will have to manually unpick the changes in order to try again (it’s impossible to roll back to an earlier point).

MySQL 8.0 introduced significant performance enhancements for DDL operations, making them more efficient and reducing the need for full table rebuilds. However, it cannot guarantee a complete absence of locks or interruptions. In situations where locks are still necessary, the duration of these operations will be proportionate to the number of rows involved.

Finally, MySQL has a relatively small limit on the combined size of all columns an index covers. This means that indexes that are possible on other backends will fail to be created under MySQL.

SQLite has very little built-in schema alteration support, and so Django attempts to emulate it by:

Creating a new table with the new schema

Copying the data across

Dropping the old table

Renaming the new table to match the original name

This process generally works well, but it can be slow and occasionally buggy. It is not recommended that you run and migrate SQLite in a production environment unless you are very aware of the risks and its limitations; the support Django ships with is designed to allow developers to use SQLite on their local machines to develop less complex Django projects without the need for a full database.

Django can create migrations for you. Make changes to your models - say, add a field and remove a model - and then run makemigrations:

Your models will be scanned and compared to the versions currently contained in your migration files, and then a new set of migrations will be written out. Make sure to read the output to see what makemigrations thinks you have changed - it’s not perfect, and for complex changes it might not be detecting what you expect.

Once you have your new migration files, you should apply them to your database to make sure they work as expected:

Once the migration is applied, commit the migration and the models change to your version control system as a single commit - that way, when other developers (or your production servers) check out the code, they’ll get both the changes to your models and the accompanying migration at the same time.

If you want to give the migration(s) a meaningful name instead of a generated one, you can use the makemigrations --name option:

Because migrations are stored in version control, you’ll occasionally come across situations where you and another developer have both committed a migration to the same app at the same time, resulting in two migrations with the same number.

Don’t worry - the numbers are just there for developers’ reference, Django just cares that each migration has a different name. Migrations specify which other migrations they depend on - including earlier migrations in the same app - in the file, so it’s possible to detect when there’s two new migrations for the same app that aren’t ordered.

When this happens, Django will prompt you and give you some options. If it thinks it’s safe enough, it will offer to automatically linearize the two migrations for you. If not, you’ll have to go in and modify the migrations yourself - don’t worry, this isn’t difficult, and is explained more in Migration files below.

On databases that support DDL transactions (SQLite and PostgreSQL), all migration operations will run inside a single transaction by default. In contrast, if a database doesn’t support DDL transactions (e.g. MySQL, Oracle) then all operations will run without a transaction.

You can prevent a migration from running in a transaction by setting the atomic attribute to False. For example:

It’s also possible to execute parts of the migration inside a transaction using atomic() or by passing atomic=True to RunPython. See Non-atomic migrations for more details.

While migrations are per-app, the tables and relationships implied by your models are too complex to be created for one app at a time. When you make a migration that requires something else to run - for example, you add a ForeignKey in your books app to your authors app - the resulting migration will contain a dependency on a migration in authors.

This means that when you run the migrations, the authors migration runs first and creates the table the ForeignKey references, and then the migration that makes the ForeignKey column runs afterward and creates the constraint. If this didn’t happen, the migration would try to create the ForeignKey column without the table it’s referencing existing and your database would throw an error.

This dependency behavior affects most migration operations where you restrict to a single app. Restricting to a single app (either in makemigrations or migrate) is a best-efforts promise, and not a guarantee; any other apps that need to be used to get dependencies correct will be.

Apps without migrations must not have relations (ForeignKey, ManyToManyField, etc.) to apps with migrations. Sometimes it may work, but it’s not supported.

The swappable_dependency() function is used in migrations to declare “swappable” dependencies on migrations in the app of the swapped-in model, currently, on the first migration of this app. As a consequence, the swapped-in model should be created in the initial migration. The argument value is a string "<app label>.<model>" describing an app label and a model name, e.g. "myapp.MyModel".

By using swappable_dependency(), you inform the migration framework that the migration relies on another migration which sets up a swappable model, allowing for the possibility of substituting the model with a different implementation in the future. This is typically used for referencing models that are subject to customization or replacement, such as the custom user model (settings.AUTH_USER_MODEL, which defaults to "auth.User") in Django’s authentication system.

Migrations are stored as an on-disk format, referred to here as “migration files”. These files are actually normal Python files with an agreed-upon object layout, written in a declarative style.

A basic migration file looks like this:

What Django looks for when it loads a migration file (as a Python module) is a subclass of django.db.migrations.Migration called Migration. It then inspects this object for four attributes, only two of which are used most of the time:

dependencies, a list of migrations this one depends on.

operations, a list of Operation classes that define what this migration does.

The operations are the key; they are a set of declarative instructions which tell Django what schema changes need to be made. Django scans them and builds an in-memory representation of all of the schema changes to all apps, and uses this to generate the SQL which makes the schema changes.

That in-memory structure is also used to work out what the differences are between your models and the current state of your migrations; Django runs through all the changes, in order, on an in-memory set of models to come up with the state of your models last time you ran makemigrations. It then uses these models to compare against the ones in your models.py files to work out what you have changed.

You should rarely, if ever, need to edit migration files by hand, but it’s entirely possible to write them manually if you need to. Some of the more complex operations are not autodetectable and are only available via a hand-written migration, so don’t be scared about editing them if you have to.

You can’t modify the number of positional arguments in an already migrated custom field without raising a TypeError. The old migration will call the modified __init__ method with the old signature. So if you need a new argument, please create a keyword argument and add something like assert 'argument_name' in kwargs in the constructor.

You can optionally serialize managers into migrations and have them available in RunPython operations. This is done by defining a use_in_migrations attribute on the manager class:

If you are using the from_queryset() function to dynamically generate a manager class, you need to inherit from the generated class to make it importable:

Please refer to the notes about Historical models in migrations to see the implications that come along.

The “initial migrations” for an app are the migrations that create the first version of that app’s tables. Usually an app will have one initial migration, but in some cases of complex model interdependencies it may have two or more.

Initial migrations are marked with an initial = True class attribute on the migration class. If an initial class attribute isn’t found, a migration will be considered “initial” if it is the first migration in the app (i.e. if it has no dependencies on any other migration in the same app).

When the migrate --fake-initial option is used, these initial migrations are treated specially. For an initial migration that creates one or more tables (CreateModel operation), Django checks that all of those tables already exist in the database and fake-applies the migration if so. Similarly, for an initial migration that adds one or more fields (AddField operation), Django checks that all of the respective columns already exist in the database and fake-applies the migration if so. Without --fake-initial, initial migrations are treated no differently from any other migration.

As previously discussed, you may need to linearize migrations manually when two development branches are joined. While editing migration dependencies, you can inadvertently create an inconsistent history state where a migration has been applied but some of its dependencies haven’t. This is a strong indication that the dependencies are incorrect, so Django will refuse to run migrations or make new migrations until it’s fixed. When using multiple databases, you can use the allow_migrate() method of database routers to control which databases makemigrations checks for consistent history.

New apps come preconfigured to accept migrations, and so you can add migrations by running makemigrations once you’ve made some changes.

If your app already has models and database tables, and doesn’t have migrations yet (for example, you created it against a previous Django version), you’ll need to convert it to use migrations by running:

This will make a new initial migration for your app. Now, run python manage.py migrate --fake-initial, and Django will detect that you have an initial migration and that the tables it wants to create already exist, and will mark the migration as already applied. (Without the migrate --fake-initial flag, the command would error out because the tables it wants to create already exist.)

Note that this only works given two things:

You have not changed your models since you made their tables. For migrations to work, you must make the initial migration first and then make changes, as Django compares changes against migration files, not the database.

You have not manually edited your database - Django won’t be able to detect that your database doesn’t match your models, you’ll just get errors when migrations try to modify those tables.

Migrations can be reversed with migrate by passing the number of the previous migration. For example, to reverse migration books.0003:

If you want to reverse all migrations applied for an app, use the name zero:

A migration is irreversible if it contains any irreversible operations. Attempting to reverse such migrations will raise IrreversibleError:

When you run migrations, Django is working from historical versions of your models stored in the migration files. If you write Python code using the RunPython operation, or if you have allow_migrate methods on your database routers, you need to use these historical model versions rather than importing them directly.

If you import models directly rather than using the historical models, your migrations may work initially but will fail in the future when you try to rerun old migrations (commonly, when you set up a new installation and run through all the migrations to set up the database).

This means that historical model problems may not be immediately obvious. If you run into this kind of failure, it’s OK to edit the migration to use the historical models rather than direct imports and commit those changes.

Because it’s impossible to serialize arbitrary Python code, these historical models will not have any custom methods that you have defined. They will, however, have the same fields, relationships, managers (limited to those with use_in_migrations = True) and Meta options (also versioned, so they may be different from your current ones).

This means that you will NOT have custom save() methods called on objects when you access them in migrations, and you will NOT have any custom constructors or instance methods. Plan appropriately!

References to functions in field options such as upload_to and limit_choices_to and model manager declarations with managers having use_in_migrations = True are serialized in migrations, so the functions and classes will need to be kept around for as long as there is a migration referencing them. Any custom model fields will also need to be kept, since these are imported directly by migrations.

In addition, the concrete base classes of the model are stored as pointers, so you must always keep base classes around for as long as there is a migration that contains a reference to them. On the plus side, methods and managers from these base classes inherit normally, so if you absolutely need access to these you can opt to move them into a superclass.

To remove old references, you can squash migrations or, if there aren’t many references, copy them into the migration files.

Similar to the “references to historical functions” considerations described in the previous section, removing custom model fields from your project or third-party app will cause a problem if they are referenced in old migrations.

To help with this situation, Django provides some model field attributes to assist with model field deprecation using the system checks framework.

Add the system_check_deprecated_details attribute to your model field similar to the following:

After a deprecation period of your choosing (two or three feature releases for fields in Django itself), change the system_check_deprecated_details attribute to system_check_removed_details and update the dictionary similar to:

You should keep the field’s methods that are required for it to operate in database migrations such as __init__(), deconstruct(), and get_internal_type(). Keep this stub field for as long as any migrations which reference the field exist. For example, after squashing migrations and removing the old ones, you should be able to remove the field completely.

As well as changing the database schema, you can also use migrations to change the data in the database itself, in conjunction with the schema if you want.

Migrations that alter data are usually called “data migrations”; they’re best written as separate migrations, sitting alongside your schema migrations.

Django can’t automatically generate data migrations for you, as it does with schema migrations, but it’s not very hard to write them. Migration files in Django are made up of Operations, and the main operation you use for data migrations is RunPython.

To start, make an empty migration file you can work from (Django will put the file in the right place, suggest a name, and add dependencies for you):

Then, open up the file; it should look something like this:

Now, all you need to do is create a new function and have RunPython use it. RunPython expects a callable as its argument which takes two arguments - the first is an app registry that has the historical versions of all your models loaded into it to match where in your history the migration sits, and the second is a SchemaEditor, which you can use to manually effect database schema changes (but beware, doing this can confuse the migration autodetector).

Let’s write a migration that populates our new name field with the combined values of first_name and last_name (we’ve come to our senses and realized that not everyone has first and last names). All we need to do is use the historical model and iterate over the rows:

Once that’s done, we can run python manage.py migrate as normal and the data migration will run in place alongside other migrations.

You can pass a second callable to RunPython to run whatever logic you want executed when migrating backwards. If this callable is omitted, migrating backwards will raise an exception.

When writing a RunPython function that uses models from apps other than the one in which the migration is located, the migration’s dependencies attribute should include the latest migration of each app that is involved, otherwise you may get an error similar to: LookupError: No installed app with label 'myappname' when you try to retrieve the model in the RunPython function using apps.get_model().

In the following example, we have a migration in app1 which needs to use models in app2. We aren’t concerned with the details of move_m1 other than the fact it will need to access models from both apps. Therefore we’ve added a dependency that specifies the last migration of app2:

If you’re interested in the more advanced migration operations, or want to be able to write your own, see the migration operations reference and the “how-to” on writing migrations.

You are encouraged to make migrations freely and not worry about how many you have; the migration code is optimized to deal with hundreds at a time without much slowdown. However, eventually you will want to move back from having several hundred migrations to just a few, and that’s where squashing comes in.

Squashing is the act of reducing an existing set of many migrations down to one (or sometimes a few) migrations which still represent the same changes.

Django does this by taking all of your existing migrations, extracting their Operations and putting them all in sequence, and then running an optimizer over them to try and reduce the length of the list - for example, it knows that CreateModel and DeleteModel cancel each other out, and it knows that AddField can be rolled into CreateModel.

Once the operation sequence has been reduced as much as possible - the amount possible depends on how closely intertwined your models are and if you have any RunSQL or RunPython operations (which can’t be optimized through unless they are marked as elidable) - Django will then write it back out into a new set of migration files.

These files are marked to say they replace the previously-squashed migrations, so they can coexist with the old migration files, and Django will intelligently switch between them depending on where you are in the history. If you’re still part-way through the set of migrations that you squashed, it will keep using them until it hits the end and then switch to the squashed history, while new installs will use the new squashed migration and skip all the old ones.

This enables you to squash and not mess up systems currently in production that aren’t fully up-to-date yet. The recommended process is to squash, keeping the old files, commit and release, wait until all systems are upgraded with the new release (or if you’re a third-party project, ensure your users upgrade releases in order without skipping any), and then remove the old files, commit and do a second release.

The command that backs all this is squashmigrations - pass it the app label and migration name you want to squash up to, and it’ll get to work:

Use the squashmigrations --squashed-name option if you want to set the name of the squashed migration rather than use an autogenerated one.

Note that model interdependencies in Django can get very complex, and squashing may result in migrations that do not run; either mis-optimized (in which case you can try again with --no-optimize, though you should also report an issue), or with a CircularDependencyError, in which case you can manually resolve it.

To manually resolve a CircularDependencyError, break out one of the ForeignKeys in the circular dependency loop into a separate migration, and move the dependency on the other app with it. If you’re unsure, see how makemigrations deals with the problem when asked to create brand new migrations from your models. In a future release of Django, squashmigrations will be updated to attempt to resolve these errors itself.

Once you’ve squashed your migration, you should then commit it alongside the migrations it replaces and distribute this change to all running instances of your application, making sure that they run migrate to store the change in their database.

You can then transition the squashed migration to a normal migration by:

Deleting all the migration files it replaces.

Updating all migrations that depend on the deleted migrations to depend on the squashed migration instead.

Removing the replaces attribute in the Migration class of the squashed migration (this is how Django tells that it is a squashed migration).

You can squash squashed migrations themselves without transitioning to normal migrations, which might be useful for situations where every environment has not yet run the original squashed migration set. But in general it is better to transition squashed migrations to normal migrations to be able to clean up older migration files.

Pruning references to deleted migrations

If it is likely that you may reuse the name of a deleted migration in the future, you should remove references to it from Django’s migrations table with the migrate --prune option.

Support for squashing squashed migrations was added.

Migrations are Python files containing the old definitions of your models - thus, to write them, Django must take the current state of your models and serialize them out into a file.

While Django can serialize most things, there are some things that we just can’t serialize out into a valid Python representation - there’s no Python standard for how a value can be turned back into code (repr() only works for basic values, and doesn’t specify import paths).

Django can serialize the following:

int, float, bool, str, bytes, None, NoneType

list, set, tuple, dict, range

datetime.date, datetime.time, and datetime.datetime instances (include those that are timezone-aware)

zoneinfo.ZoneInfo instances

decimal.Decimal instances

enum.Enum and enum.Flag instances

functools.partial() and functools.partialmethod instances which have serializable func, args, and keywords values

Pure and concrete path objects from pathlib. Concrete paths are converted to their pure path equivalent, e.g. pathlib.PosixPath to pathlib.PurePosixPath

os.PathLike instances, e.g. os.DirEntry, which are converted to str or bytes using os.fspath()

LazyObject instances which wrap a serializable value

Enumeration types (e.g. TextChoices or IntegerChoices) instances

Any function or method reference (e.g. datetime.datetime.today) (must be in module’s top-level scope)

Functions may be decorated if wrapped properly, i.e. using functools.wraps()

The functools.cache() and functools.lru_cache() decorators are explicitly supported

Unbound methods used from within the class body

Any class reference (must be in module’s top-level scope)

Anything with a custom deconstruct() method (see below)

Serialization support for zoneinfo.ZoneInfo instances was added.

Django cannot serialize:

Arbitrary class instances (e.g. MyClass(4.3, 5.7))

You can serialize other types by writing a custom serializer. For example, if Django didn’t serialize Decimal by default, you could do this:

The first argument of MigrationWriter.register_serializer() is a type or iterable of types that should use the serializer.

The serialize() method of your serializer must return a string of how the value should appear in migrations and a set of any imports that are needed in the migration.

You can let Django serialize your own custom class instances by giving the class a deconstruct() method. It takes no arguments, and should return a tuple of three things (path, args, kwargs):

path should be the Python path to the class, with the class name included as the last part (for example, myapp.custom_things.MyClass). If your class is not available at the top level of a module it is not serializable.

args should be a list of positional arguments to pass to your class’ __init__ method. Everything in this list should itself be serializable.

kwargs should be a dict of keyword arguments to pass to your class’ __init__ method. Every value should itself be serializable.

This return value is different from the deconstruct() method for custom fields which returns a tuple of four items.

Django will write out the value as an instantiation of your class with the given arguments, similar to the way it writes out references to Django fields.

To prevent a new migration from being created each time makemigrations is run, you should also add a __eq__() method to the decorated class. This function will be called by Django’s migration framework to detect changes between states.

As long as all of the arguments to your class’ constructor are themselves serializable, you can use the @deconstructible class decorator from django.utils.deconstruct to add the deconstruct() method:

The decorator adds logic to capture and preserve the arguments on their way into your constructor, and then returns those arguments exactly when deconstruct() is called.

If you are the maintainer of a third-party app with models, you may need to ship migrations that support multiple Django versions. In this case, you should always run makemigrations with the lowest Django version you wish to support.

The migrations system will maintain backwards-compatibility according to the same policy as the rest of Django, so migration files generated on Django X.Y should run unchanged on Django X.Y+1. The migrations system does not promise forwards-compatibility, however. New features may be added, and migration files generated with newer versions of Django may not work on older versions.

Covers the schema operations API, special operations, and writing your own operations.

Explains how to structure and write database migrations for different scenarios you might encounter.

---

## Models¶

**URL:** https://docs.djangoproject.com/en/stable/topics/db/models/

**Contents:**
- Models¶
- Quick example¶
- Using models¶
- Fields¶
  - Field types¶
  - Field options¶
  - Automatic primary key fields¶
  - Verbose field names¶
  - Relationships¶
    - Many-to-one relationships¶

A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.

Each model is a Python class that subclasses django.db.models.Model.

Each attribute of the model represents a database field.

With all of this, Django gives you an automatically-generated database-access API; see Making queries.

This example model defines a Person, which has a first_name and last_name:

first_name and last_name are fields of the model. Each field is specified as a class attribute, and each attribute maps to a database column.

The above Person model would create a database table like this:

Some technical notes:

The name of the table, myapp_person, is automatically derived from some model metadata but can be overridden. See Table names for more details.

An id field is added automatically, but this behavior can be overridden. See Automatic primary key fields.

The CREATE TABLE SQL in this example is formatted using PostgreSQL syntax, but it’s worth noting Django uses SQL tailored to the database backend specified in your settings file.

Once you have defined your models, you need to tell Django you’re going to use those models. Do this by editing your settings file and changing the INSTALLED_APPS setting to add the name of the module that contains your models.py.

For example, if the models for your application live in the module myapp.models (the package structure that is created for an application by the manage.py startapp script), INSTALLED_APPS should read, in part:

When you add new apps to INSTALLED_APPS, be sure to run manage.py migrate, optionally making migrations for them first with manage.py makemigrations.

The most important part of a model – and the only required part of a model – is the list of database fields it defines. Fields are specified by class attributes. Be careful not to choose field names that conflict with the models API like clean, save, or delete.

Each field in your model should be an instance of the appropriate Field class. Django uses the field class types to determine a few things:

The column type, which tells the database what kind of data to store (e.g. INTEGER, VARCHAR, TEXT).

The default HTML widget to use when rendering a form field (e.g. <input type="text">, <select>).

The minimal validation requirements, used in Django’s admin and in automatically-generated forms.

Django ships with dozens of built-in field types; you can find the complete list in the model field reference. You can easily write your own fields if Django’s built-in ones don’t do the trick; see How to create custom model fields.

Each field takes a certain set of field-specific arguments (documented in the model field reference). For example, CharField (and its subclasses) require a max_length argument which specifies the size of the VARCHAR database field used to store the data.

There’s also a set of common arguments available to all field types. All are optional. They’re fully explained in the reference, but here’s a quick summary of the most often-used ones:

If True, Django will store empty values as NULL in the database. Default is False.

If True, the field is allowed to be blank. Default is False.

Note that this is different than null. null is purely database-related, whereas blank is validation-related. If a field has blank=True, form validation will allow entry of an empty value. If a field has blank=False, the field will be required.

A sequence of 2-value tuples, a mapping, an enumeration type, or a callable (that expects no arguments and returns any of the previous formats), to use as choices for this field. If this is given, the default form widget will be a select box instead of the standard text field and will limit choices to the choices given.

A choices list looks like this:

A new migration is created each time the order of choices changes.

The first element in each tuple is the value that will be stored in the database. The second element is displayed by the field’s form widget.

Given a model instance, the display value for a field with choices can be accessed using the get_FOO_display() method. For example:

You can also use enumeration classes to define choices in a concise way:

Further examples are available in the model field reference.

The default value for the field. This can be a value or a callable object. If callable it will be called every time a new object is created.

The database-computed default value for the field. This can be a literal value or a database function.

If both db_default and Field.default are set, default will take precedence when creating instances in Python code. db_default will still be set at the database level and will be used when inserting rows outside of the ORM or when adding a new field in a migration.

Extra “help” text to be displayed with the form widget. It’s useful for documentation even if your field isn’t used on a form.

If True, this field is the primary key for the model.

If you don’t specify primary_key=True for any fields in your model, Django will automatically add a field to hold the primary key, so you don’t need to set primary_key=True on any of your fields unless you want to override the default primary-key behavior. For more, see Automatic primary key fields.

The primary key field is read-only. If you change the value of the primary key on an existing object and then save it, a new object will be created alongside the old one. For example:

If True, this field must be unique throughout the table.

Again, these are just short descriptions of the most common field options. Full details can be found in the common model field option reference.

By default, Django gives each model an auto-incrementing primary key with the type specified per app in AppConfig.default_auto_field or globally in the DEFAULT_AUTO_FIELD setting. For example:

If you’d like to specify a custom primary key, specify primary_key=True on one of your fields. If Django sees you’ve explicitly set Field.primary_key, it won’t add the automatic id column.

Each model requires exactly one field to have primary_key=True (either explicitly declared or automatically added).

Each field type, except for ForeignKey, ManyToManyField and OneToOneField, takes an optional first positional argument – a verbose name. If the verbose name isn’t given, Django will automatically create it using the field’s attribute name, converting underscores to spaces.

In this example, the verbose name is "person's first name":

In this example, the verbose name is "first name":

ForeignKey, ManyToManyField and OneToOneField require the first argument to be a model class, so use the verbose_name keyword argument:

The convention is not to capitalize the first letter of the verbose_name. Django will automatically capitalize the first letter where it needs to.

Clearly, the power of relational databases lies in relating tables to each other. Django offers ways to define the three most common types of database relationships: many-to-one, many-to-many and one-to-one.

To define a many-to-one relationship, use django.db.models.ForeignKey. You use it just like any other Field type: by including it as a class attribute of your model.

ForeignKey requires a positional argument: the class to which the model is related.

For example, if a Car model has a Manufacturer – that is, a Manufacturer makes multiple cars but each Car only has one Manufacturer – use the following definitions:

You can also create recursive relationships (an object with a many-to-one relationship to itself) and relationships to models not yet defined; see the model field reference for details.

It’s suggested, but not required, that the name of a ForeignKey field (manufacturer in the example above) be the name of the model, lowercase. You can call the field whatever you want. For example:

ForeignKey fields accept a number of extra arguments which are explained in the model field reference. These options help define how the relationship should work; all are optional.

For details on accessing backwards-related objects, see the Following relationships backward example.

For sample code, see the Many-to-one relationship model example.

To define a many-to-many relationship, use ManyToManyField. You use it just like any other Field type: by including it as a class attribute of your model.

ManyToManyField requires a positional argument: the class to which the model is related.

For example, if a Pizza has multiple Topping objects – that is, a Topping can be on multiple pizzas and each Pizza has multiple toppings – here’s how you’d represent that:

As with ForeignKey, you can also create recursive relationships (an object with a many-to-many relationship to itself) and relationships to models not yet defined.

It’s suggested, but not required, that the name of a ManyToManyField (toppings in the example above) be a plural describing the set of related model objects.

It doesn’t matter which model has the ManyToManyField, but you should only put it in one of the models – not both.

Generally, ManyToManyField instances should go in the object that’s going to be edited on a form. In the above example, toppings is in Pizza (rather than Topping having a pizzas ManyToManyField ) because it’s more natural to think about a pizza having toppings than a topping being on multiple pizzas. The way it’s set up above, the Pizza form would let users select the toppings.

See the Many-to-many relationship model example for a full example.

ManyToManyField fields also accept a number of extra arguments which are explained in the model field reference. These options help define how the relationship should work; all are optional.

When you’re only dealing with many-to-many relationships such as mixing and matching pizzas and toppings, a standard ManyToManyField is all you need. However, sometimes you may need to associate data with the relationship between two models.

For example, consider the case of an application tracking the musical groups which musicians belong to. There is a many-to-many relationship between a person and the groups of which they are a member, so you could use a ManyToManyField to represent this relationship. However, there is a lot of detail about the membership that you might want to collect, such as the date at which the person joined the group.

For these situations, Django allows you to specify the model that will be used to govern the many-to-many relationship. You can then put extra fields on the intermediate model. The intermediate model is associated with the ManyToManyField using the through argument to point to the model that will act as an intermediary. For our musician example, the code would look something like this:

When you set up the intermediary model, you explicitly specify foreign keys to the models that are involved in the many-to-many relationship. This explicit declaration defines how the two models are related.

If you don’t want multiple associations between the same instances, add a UniqueConstraint including the from and to fields. Django’s automatically generated many-to-many tables include such a constraint.

There are a few restrictions on the intermediate model:

Your intermediate model must contain one - and only one - foreign key to the source model (this would be Group in our example), or you must explicitly specify the foreign keys Django should use for the relationship using ManyToManyField.through_fields. If you have more than one foreign key and through_fields is not specified, a validation error will be raised. A similar restriction applies to the foreign key to the target model (this would be Person in our example).

For a model which has a many-to-many relationship to itself through an intermediary model, two foreign keys to the same model are permitted, but they will be treated as the two (different) sides of the many-to-many relationship. If through_fields is not specified, the first foreign key will be taken to represent the source side of the ManyToManyField, while the second will be taken to represent the target side. If there are more than two foreign keys though, you must specify through_fields to explicitly indicate which foreign keys to use, otherwise a validation error will be raised.

Now that you have set up your ManyToManyField to use your intermediary model (Membership, in this case), you’re ready to start creating some many-to-many relationships. You do this by creating instances of the intermediate model:

You can also use add(), create(), or set() to create relationships, as long as you specify through_defaults for any required fields:

You may prefer to create instances of the intermediate model directly.

If the custom through table defined by the intermediate model does not enforce uniqueness on the (model1, model2) pair, allowing multiple values, the remove() call will remove all intermediate model instances:

The clear() method can be used to remove all many-to-many relationships for an instance:

Once you have established the many-to-many relationships, you can issue queries. Just as with normal many-to-many relationships, you can query using the attributes of the many-to-many-related model:

As you are using an intermediate model, you can also query on its attributes:

If you need to access a membership’s information you may do so by directly querying the Membership model:

Another way to access the same information is by querying the many-to-many reverse relationship from a Person object:

To define a one-to-one relationship, use OneToOneField. You use it just like any other Field type: by including it as a class attribute of your model.

This is most useful on the primary key of an object when that object “extends” another object in some way.

OneToOneField requires a positional argument: the class to which the model is related.

For example, if you were building a database of “places”, you would build pretty standard stuff such as address, phone number, etc. in the database. Then, if you wanted to build a database of restaurants on top of the places, instead of repeating yourself and replicating those fields in the Restaurant model, you could make Restaurant have a OneToOneField to Place (because a restaurant “is a” place; in fact, to handle this you’d typically use inheritance, which involves an implicit one-to-one relation).

As with ForeignKey, a recursive relationship can be defined and references to as-yet undefined models can be made.

See the One-to-one relationship model example for a full example.

OneToOneField fields also accept an optional parent_link argument.

OneToOneField classes used to automatically become the primary key on a model. This is no longer true (although you can manually pass in the primary_key argument if you like). Thus, it’s now possible to have multiple fields of type OneToOneField on a single model.

It’s perfectly OK to relate a model to one from another app. To do this, import the related model at the top of the file where your model is defined. Then, refer to the other model class wherever needed. For example:

Alternatively, you can use a lazy reference to the related model, specified as a string in the format "app_label.ModelName". This does not require the related model to be imported. For example:

See lazy relationships for more details.

Django places some restrictions on model field names:

A field name cannot be a Python reserved word, because that would result in a Python syntax error. For example:

A field name cannot contain more than one underscore in a row, due to the way Django’s query lookup syntax works. For example:

A field name cannot end with an underscore, for similar reasons.

A field name cannot be check, as this would override the check framework’s Model.check() method.

These limitations can be worked around, though, because your field name doesn’t necessarily have to match your database column name. See the db_column option.

SQL reserved words, such as join, where or select, are allowed as model field names, because Django escapes all database table names and column names in every underlying SQL query. It uses the quoting syntax of your particular database engine.

If one of the existing model fields cannot be used to fit your purposes, or if you wish to take advantage of some less common database column types, you can create your own field class. Full coverage of creating your own fields is provided in How to create custom model fields.

Give your model metadata by using an inner class Meta, like so:

Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name (db_table), or human-readable singular and plural names (verbose_name and verbose_name_plural). None are required, and adding class Meta to a model is completely optional.

A complete list of all possible Meta options can be found in the model option reference.

The most important attribute of a model is the Manager. It’s the interface through which database query operations are provided to Django models and is used to retrieve the instances from the database. If no custom Manager is defined, the default name is objects. Managers are only accessible via model classes, not the model instances.

Define custom methods on a model to add custom “row-level” functionality to your objects. Whereas Manager methods are intended to do “table-wide” things, model methods should act on a particular model instance.

This is a valuable technique for keeping business logic in one place – the model.

For example, this model has a few custom methods:

The last method in this example is a property.

The model instance reference has a complete list of methods automatically given to each model. You can override most of these – see overriding predefined model methods, below – but there are a couple that you’ll almost always want to define:

A Python “magic method” that returns a string representation of any object. This is what Python and Django will use whenever a model instance needs to be coerced and displayed as a plain string. Most notably, this happens when you display an object in an interactive console or in the admin.

You’ll always want to define this method; the default isn’t very helpful at all.

This tells Django how to calculate the URL for an object. Django uses this in its admin interface, and any time it needs to figure out a URL for an object.

Any object that has a URL that uniquely identifies it should define this method.

There’s another set of model methods that encapsulate a bunch of database behavior that you’ll want to customize. In particular you’ll often want to change the way save() and delete() work.

You’re free to override these methods (and any other model method) to alter behavior.

A classic use-case for overriding the built-in methods is if you want something to happen whenever you save an object. For example (see save() for documentation of the parameters it accepts):

You can also prevent saving:

It’s important to remember to call the superclass method – that’s that super().save(**kwargs) business – to ensure that the object still gets saved into the database. If you forget to call the superclass method, the default behavior won’t happen and the database won’t get touched.

It’s also important that you pass through the arguments that can be passed to the model method – that’s what the **kwargs bit does. Django will, from time to time, extend the capabilities of built-in model methods, adding new keyword arguments. If you use **kwargs in your method definitions, you are guaranteed that your code will automatically support those arguments when they are added.

If you wish to update a field value in the save() method, you may also want to have this field added to the update_fields keyword argument. This will ensure the field is saved when update_fields is specified. For example:

See Specifying which fields to save for more details.

Overridden model methods are not called on bulk operations

Note that the delete() method for an object is not necessarily called when deleting objects in bulk using a QuerySet or as a result of a cascading delete. To ensure customized delete logic gets executed, you can use pre_delete and/or post_delete signals.

Unfortunately, there isn’t a workaround when creating or updating objects in bulk, since none of save(), pre_save, and post_save are called.

Another common pattern is writing custom SQL statements in model methods and module-level methods. For more details on using raw SQL, see the documentation on using raw SQL.

Model inheritance in Django works almost identically to the way normal class inheritance works in Python, but the basics at the beginning of the page should still be followed. That means the base class should subclass django.db.models.Model.

The only decision you have to make is whether you want the parent models to be models in their own right (with their own database tables), or if the parents are just holders of common information that will only be visible through the child models.

There are three styles of inheritance that are possible in Django.

Often, you will just want to use the parent class to hold information that you don’t want to have to type out for each child model. This class isn’t going to ever be used in isolation, so Abstract base classes are what you’re after.

If you’re subclassing an existing model (perhaps something from another application entirely) and want each model to have its own database table, Multi-table inheritance is the way to go.

Finally, if you only want to modify the Python-level behavior of a model, without changing the models fields in any way, you can use Proxy models.

Abstract base classes are useful when you want to put some common information into a number of other models. You write your base class and put abstract=True in the Meta class. This model will then not be used to create any database table. Instead, when it is used as a base class for other models, its fields will be added to those of the child class.

The Student model will have three fields: name, age and home_group. The CommonInfo model cannot be used as a normal Django model, since it is an abstract base class. It does not generate a database table or have a manager, and cannot be instantiated or saved directly.

Fields inherited from abstract base classes can be overridden with another field or value, or be removed with None.

For many uses, this type of model inheritance will be exactly what you want. It provides a way to factor out common information at the Python level, while still only creating one database table per child model at the database level.

When an abstract base class is created, Django makes any Meta inner class you declared in the base class available as an attribute. If a child class does not declare its own Meta class, it will inherit the parent’s Meta. If the child wants to extend the parent’s Meta class, it can subclass it. For example:

Django does make one adjustment to the Meta class of an abstract base class: before installing the Meta attribute, it sets abstract=False. This means that children of abstract base classes don’t automatically become abstract classes themselves. To make an abstract base class that inherits from another abstract base class, you need to explicitly set abstract=True on the child.

Some attributes won’t make sense to include in the Meta class of an abstract base class. For example, including db_table would mean that all the child classes (the ones that don’t specify their own Meta) would use the same database table, which is almost certainly not what you want.

Due to the way Python inheritance works, if a child class inherits from multiple abstract base classes, only the Meta options from the first listed class will be inherited by default. To inherit Meta options from multiple abstract base classes, you must explicitly declare the Meta inheritance. For example:

If you are using related_name or related_query_name on a ForeignKey or ManyToManyField, you must always specify a unique reverse name and query name for the field. This would normally cause a problem in abstract base classes, since the fields on this class are included into each of the child classes, with exactly the same values for the attributes (including related_name and related_query_name) each time.

To work around this problem, when you are using related_name or related_query_name in an abstract base class (only), part of the value should contain '%(app_label)s' and '%(class)s'.

'%(class)s' is replaced by the lowercased name of the child class that the field is used in.

'%(app_label)s' is replaced by the lowercased name of the app the child class is contained within. Each installed application name must be unique and the model class names within each app must also be unique, therefore the resulting name will end up being different.

For example, given an app common/models.py:

Along with another app rare/models.py:

The reverse name of the common.ChildA.m2m field will be common_childa_related and the reverse query name will be common_childas. The reverse name of the common.ChildB.m2m field will be common_childb_related and the reverse query name will be common_childbs. Finally, the reverse name of the rare.ChildB.m2m field will be rare_childb_related and the reverse query name will be rare_childbs. It’s up to you how you use the '%(class)s' and '%(app_label)s' portion to construct your related name or related query name but if you forget to use it, Django will raise errors when you perform system checks (or run migrate).

If you don’t specify a related_name attribute for a field in an abstract base class, the default reverse name will be the name of the child class followed by '_set', just as it normally would be if you’d declared the field directly on the child class. For example, in the above code, if the related_name attribute was omitted, the reverse name for the m2m field would be childa_set in the ChildA case and childb_set for the ChildB field.

The second type of model inheritance supported by Django is when each model in the hierarchy is a model all by itself. Each model corresponds to its own database table and can be queried and created individually. The inheritance relationship introduces links between the child model and each of its parents (via an automatically-created OneToOneField). For example:

All of the fields of Place will also be available in Restaurant, although the data will reside in a different database table. So these are both possible:

If you have a Place that is also a Restaurant, you can get from the Place object to the Restaurant object by using the lowercase version of the model name:

However, if p in the above example was not a Restaurant (it had been created directly as a Place object or was the parent of some other class), referring to p.restaurant would raise a Restaurant.DoesNotExist exception.

The automatically-created OneToOneField on Restaurant that links it to Place looks like this:

You can override that field by declaring your own OneToOneField with parent_link=True on Restaurant.

In the multi-table inheritance situation, it doesn’t make sense for a child class to inherit from its parent’s Meta class. All the Meta options have already been applied to the parent class and applying them again would normally only lead to contradictory behavior (this is in contrast with the abstract base class case, where the base class doesn’t exist in its own right).

So a child model does not have access to its parent’s Meta class. However, there are a few limited cases where the child inherits behavior from the parent: if the child does not specify an ordering attribute or a get_latest_by attribute, it will inherit these from its parent.

If the parent has an ordering and you don’t want the child to have any natural ordering, you can explicitly disable it:

Because multi-table inheritance uses an implicit OneToOneField to link the child and the parent, it’s possible to move from the parent down to the child, as in the above example. However, this uses up the name that is the default related_name value for ForeignKey and ManyToManyField relations. If you are putting those types of relations on a subclass of the parent model, you must specify the related_name attribute on each such field. If you forget, Django will raise a validation error.

For example, using the above Place class again, let’s create another subclass with a ManyToManyField:

This results in the error:

Adding related_name to the customers field as follows would resolve the error: models.ManyToManyField(Place, related_name='provider').

As mentioned, Django will automatically create a OneToOneField linking your child class back to any non-abstract parent models. If you want to control the name of the attribute linking back to the parent, you can create your own OneToOneField and set parent_link=True to indicate that your field is the link back to the parent class.

When using multi-table inheritance, a new database table is created for each subclass of a model. This is usually the desired behavior, since the subclass needs a place to store any additional data fields that are not present on the base class. Sometimes, however, you only want to change the Python behavior of a model – perhaps to change the default manager, or add a new method.

This is what proxy model inheritance is for: creating a proxy for the original model. You can create, delete and update instances of the proxy model and all the data will be saved as if you were using the original (non-proxied) model. The difference is that you can change things like the default model ordering or the default manager in the proxy, without having to alter the original.

Proxy models are declared like normal models. You tell Django that it’s a proxy model by setting the proxy attribute of the Meta class to True.

For example, suppose you want to add a method to the Person model. You can do it like this:

The MyPerson class operates on the same database table as its parent Person class. In particular, any new instances of Person will also be accessible through MyPerson, and vice-versa:

You could also use a proxy model to define a different default ordering on a model. You might not always want to order the Person model, but regularly order by the last_name attribute when you use the proxy:

Now normal Person queries will be unordered and OrderedPerson queries will be ordered by last_name.

Proxy models inherit Meta attributes in the same way as regular models.

There is no way to have Django return, say, a MyPerson object whenever you query for Person objects. A queryset for Person objects will return those types of objects. The whole point of proxy objects is that code relying on the original Person will use those and your own code can use the extensions you included (that no other code is relying on anyway). It is not a way to replace the Person (or any other) model everywhere with something of your own creation.

A proxy model must inherit from exactly one non-abstract model class. You can’t inherit from multiple non-abstract models as the proxy model doesn’t provide any connection between the rows in the different database tables. A proxy model can inherit from any number of abstract model classes, providing they do not define any model fields. A proxy model may also inherit from any number of proxy models that share a common non-abstract parent class.

If you don’t specify any model managers on a proxy model, it inherits the managers from its model parents. If you define a manager on the proxy model, it will become the default, although any managers defined on the parent classes will still be available.

Continuing our example from above, you could change the default manager used when you query the Person model like this:

If you wanted to add a new manager to the Proxy, without replacing the existing default, you can use the techniques described in the custom manager documentation: create a base class containing the new managers and inherit that after the primary base class:

You probably won’t need to do this very often, but, when you do, it’s possible.

Proxy model inheritance might look fairly similar to creating an unmanaged model, using the managed attribute on a model’s Meta class.

With careful setting of Meta.db_table you could create an unmanaged model that shadows an existing model and adds Python methods to it. However, that would be very repetitive and fragile as you need to keep both copies synchronized if you make any changes.

On the other hand, proxy models are intended to behave exactly like the model they are proxying for. They are always in sync with the parent model since they directly inherit its fields and managers.

The general rules are:

If you are mirroring an existing model or database table and don’t want all the original database table columns, use Meta.managed=False. That option is normally useful for modeling database views and tables not under the control of Django.

If you are wanting to change the Python-only behavior of a model, but keep all the same fields as in the original, use Meta.proxy=True. This sets things up so that the proxy model is an exact copy of the storage structure of the original model when data is saved.

Just as with Python’s subclassing, it’s possible for a Django model to inherit from multiple parent models. Keep in mind that normal Python name resolution rules apply. The first base class that a particular name (e.g. Meta) appears in will be the one that is used; for example, this means that if multiple parents contain a Meta class, only the first one is going to be used, and all others will be ignored.

Generally, you won’t need to inherit from multiple parents. The main use-case where this is useful is for “mix-in” classes: adding a particular extra field or method to every class that inherits the mix-in. Try to keep your inheritance hierarchies as simple and straightforward as possible so that you won’t have to struggle to work out where a particular piece of information is coming from.

Note that inheriting from multiple models that have a common id primary key field will raise an error. To properly use multiple inheritance, you can use an explicit AutoField in the base models:

Or use a common ancestor to hold the AutoField. This requires using an explicit OneToOneField from each parent model to the common ancestor to avoid a clash between the fields that are automatically generated and inherited by the child:

In normal Python class inheritance, it is permissible for a child class to override any attribute from the parent class. In Django, this isn’t usually permitted for model fields. If a non-abstract model base class has a field called author, you can’t create another model field or define an attribute called author in any class that inherits from that base class.

This restriction doesn’t apply to model fields inherited from an abstract model. Such fields may be overridden with another field or value, or be removed by setting field_name = None.

Model managers are inherited from abstract base classes. Overriding an inherited field which is referenced by an inherited Manager may cause subtle bugs. See custom managers and model inheritance.

Some fields define extra attributes on the model, e.g. a ForeignKey defines an extra attribute with _id appended to the field name, as well as related_name and related_query_name on the foreign model.

These extra attributes cannot be overridden unless the field that defines it is changed or removed so that it no longer defines the extra attribute.

Overriding fields in a parent model leads to difficulties in areas such as initializing new instances (specifying which field is being initialized in Model.__init__) and serialization. These are features which normal Python class inheritance doesn’t have to deal with in quite the same way, so the difference between Django model inheritance and Python class inheritance isn’t arbitrary.

This restriction only applies to attributes which are Field instances. Normal Python attributes can be overridden if you wish. It also only applies to the name of the attribute as Python sees it: if you are manually specifying the database column name, you can have the same column name appearing in both a child and an ancestor model for multi-table inheritance (they are columns in two different database tables).

Django will raise a FieldError if you override any model field in any ancestor model.

Note that because of the way fields are resolved during class definition, model fields inherited from multiple abstract parent models are resolved in a strict depth-first order. This contrasts with standard Python MRO, which is resolved breadth-first in cases of diamond shaped inheritance. This difference only affects complex model hierarchies, which (as per the advice above) you should try to avoid.

The manage.py startapp command creates an application structure that includes a models.py file. If you have many models, organizing them in separate files may be useful.

To do so, create a models package. Remove models.py and create a myapp/models/ directory with an __init__.py file and the files to store your models. You must import the models in the __init__.py file.

For example, if you had organic.py and synthetic.py in the models directory:

Explicitly importing each model rather than using from .models import * has the advantages of not cluttering the namespace, making code more readable, and keeping code analysis tools useful.

Covers all the model related APIs including model fields, related objects, and QuerySet.

---

## Multiple databases¶

**URL:** https://docs.djangoproject.com/en/stable/topics/db/multi-db/

**Contents:**
- Multiple databases¶
- Defining your databases¶
- Synchronizing your databases¶
  - Using other management commands¶
- Automatic database routing¶
  - Database routers¶
    - Hints¶
  - Using routers¶
  - An example¶
- Manually selecting a database¶

This topic guide describes Django’s support for interacting with multiple databases. Most of the rest of Django’s documentation assumes you are interacting with a single database. If you want to interact with multiple databases, you’ll need to take some additional steps.

See Multi-database support for information about testing with multiple databases.

The first step to using more than one database with Django is to tell Django about the database servers you’ll be using. This is done using the DATABASES setting. This setting maps database aliases, which are a way to refer to a specific database throughout Django, to a dictionary of settings for that specific connection. The settings in the inner dictionaries are described fully in the DATABASES documentation.

Databases can have any alias you choose. However, the alias default has special significance. Django uses the database with the alias of default when no other database has been selected.

The following is an example settings.py snippet defining two databases – a default PostgreSQL database and a MySQL database called users:

If the concept of a default database doesn’t make sense in the context of your project, you need to be careful to always specify the database that you want to use. Django requires that a default database entry be defined, but the parameters dictionary can be left blank if it will not be used. To do this, you must set up DATABASE_ROUTERS for all of your apps’ models, including those in any contrib and third-party apps you’re using, so that no queries are routed to the default database. The following is an example settings.py snippet defining two non-default databases, with the default entry intentionally left empty:

If you attempt to access a database that you haven’t defined in your DATABASES setting, Django will raise a django.utils.connection.ConnectionDoesNotExist exception.

The migrate management command operates on one database at a time. By default, it operates on the default database, but by providing the --database option, you can tell it to synchronize a different database. So, to synchronize all models onto all databases in the first example above, you would need to call:

If you don’t want every application to be synchronized onto a particular database, you can define a database router that implements a policy constraining the availability of particular models.

If, as in the second example above, you’ve left the default database empty, you must provide a database name each time you run migrate. Omitting the database name would raise an error. For the second example:

Most other django-admin commands that interact with the database operate in the same way as migrate – they only ever operate on one database at a time, using --database to control the database used.

An exception to this rule is the makemigrations command. It validates the migration history in the databases to catch problems with the existing migration files (which could be caused by editing them) before creating new migrations. By default, it checks only the default database, but it consults the allow_migrate() method of routers if any are installed.

The easiest way to use multiple databases is to set up a database routing scheme. The default routing scheme ensures that objects remain ‘sticky’ to their original database (i.e., an object retrieved from the foo database will be saved on the same database). The default routing scheme ensures that if a database isn’t specified, all queries fall back to the default database.

You don’t have to do anything to activate the default routing scheme – it is provided ‘out of the box’ on every Django project. However, if you want to implement more interesting database allocation behaviors, you can define and install your own database routers.

A database Router is a class that provides up to four methods:

Suggest the database that should be used for read operations for objects of type model.

If a database operation is able to provide any additional information that might assist in selecting a database, it will be provided in the hints dictionary. Details on valid hints are provided below.

Returns None if there is no suggestion.

Suggest the database that should be used for writes of objects of type Model.

If a database operation is able to provide any additional information that might assist in selecting a database, it will be provided in the hints dictionary. Details on valid hints are provided below.

Returns None if there is no suggestion.

Return True if a relation between obj1 and obj2 should be allowed, False if the relation should be prevented, or None if the router has no opinion. This is purely a validation operation, used by foreign key and many to many operations to determine if a relation should be allowed between two objects.

If no router has an opinion (i.e. all routers return None), only relations within the same database are allowed.

Determine if the migration operation is allowed to run on the database with alias db. Return True if the operation should run, False if it shouldn’t run, or None if the router has no opinion.

The app_label positional argument is the label of the application being migrated.

model_name is set by most migration operations to the value of model._meta.model_name (the lowercased version of the model __name__) of the model being migrated. Its value is None for the RunPython and RunSQL operations unless they provide it using hints.

hints are used by certain operations to communicate additional information to the router.

When model_name is set, hints normally contains the model class under the key 'model'. Note that it may be a historical model, and thus not have any custom attributes, methods, or managers. You should only rely on _meta.

This method can also be used to determine the availability of a model on a given database.

makemigrations always creates migrations for model changes, but if allow_migrate() returns False, any migration operations for the model_name will be silently skipped when running migrate on the db. Changing the behavior of allow_migrate() for models that already have migrations may result in broken foreign keys, extra tables, or missing tables. When makemigrations verifies the migration history, it skips databases where no app is allowed to migrate.

A router doesn’t have to provide all these methods – it may omit one or more of them. If one of the methods is omitted, Django will skip that router when performing the relevant check.

The hints received by the database router can be used to decide which database should receive a given request.

At present, the only hint that will be provided is instance, an object instance that is related to the read or write operation that is underway. This might be the instance that is being saved, or it might be an instance that is being added in a many-to-many relation. In some cases, no instance hint will be provided at all. The router checks for the existence of an instance hint, and determine if that hint should be used to alter routing behavior.

Database routers are installed using the DATABASE_ROUTERS setting. This setting defines a list of class names, each specifying a router that should be used by the base router (django.db.router).

The base router is used by Django’s database operations to allocate database usage. Whenever a query needs to know which database to use, it calls the base router, providing a model and a hint (if available). The base router tries each router class in turn until one returns a database suggestion. If no routers return a suggestion, the base router tries the current instance._state.db of the hint instance. If no hint instance was provided, or instance._state.db is None, the base router will allocate the default database.

Example purposes only!

This example is intended as a demonstration of how the router infrastructure can be used to alter database usage. It intentionally ignores some complex issues in order to demonstrate how routers are used.

This example won’t work if any of the models in myapp contain relationships to models outside of the other database. Cross-database relationships introduce referential integrity problems that Django can’t currently handle.

The primary/replica (referred to as master/slave by some databases) configuration described is also flawed – it doesn’t provide any solution for handling replication lag (i.e., query inconsistencies introduced because of the time taken for a write to propagate to the replicas). It also doesn’t consider the interaction of transactions with the database utilization strategy.

So - what does this mean in practice? Let’s consider another sample configuration. This one will have several databases: one for the auth application, and all other apps using a primary/replica setup with two read replicas. Here are the settings specifying these databases:

Now we’ll need to handle routing. First we want a router that knows to send queries for the auth and contenttypes apps to auth_db (auth models are linked to ContentType, so they must be stored in the same database):

And we also want a router that sends all other apps to the primary/replica configuration, and randomly chooses a replica to read from:

Finally, in the settings file, we add the following (substituting path.to. with the actual Python path to the module(s) where the routers are defined):

The order in which routers are processed is significant. Routers will be queried in the order they are listed in the DATABASE_ROUTERS setting. In this example, the AuthRouter is processed before the PrimaryReplicaRouter, and as a result, decisions concerning the models in auth are processed before any other decision is made. If the DATABASE_ROUTERS setting listed the two routers in the other order, PrimaryReplicaRouter.allow_migrate() would be processed first. The catch-all nature of the PrimaryReplicaRouter implementation would mean that all models would be available on all databases.

With this setup installed, and all databases migrated as per Synchronizing your databases, lets run some Django code:

This example defined a router to handle interaction with models from the auth app, and other routers to handle interaction with all other apps. If you left your default database empty and don’t want to define a catch-all database router to handle all apps not otherwise specified, your routers must handle the names of all apps in INSTALLED_APPS before you migrate. See Behavior of contrib apps for information about contrib apps that must be together in one database.

Django also provides an API that allows you to maintain complete control over database usage in your code. A manually specified database allocation will take priority over a database allocated by a router.

You can select the database for a QuerySet at any point in the QuerySet “chain.” Call using() on the QuerySet to get another QuerySet that uses the specified database.

using() takes a single argument: the alias of the database on which you want to run the query. For example:

Use the using keyword to Model.save() to specify to which database the data should be saved.

For example, to save an object to the legacy_users database, you’d use this:

If you don’t specify using, the save() method will save into the default database allocated by the routers.

If you’ve saved an instance to one database, it might be tempting to use save(using=...) as a way to migrate the instance to a new database. However, if you don’t take appropriate steps, this could have some unexpected consequences.

Consider the following example:

In statement 1, a new Person object is saved to the first database. At this time, p doesn’t have a primary key, so Django issues an SQL INSERT statement. This creates a primary key, and Django assigns that primary key to p.

When the save occurs in statement 2, p already has a primary key value, and Django will attempt to use that primary key on the new database. If the primary key value isn’t in use in the second database, then you won’t have any problems – the object will be copied to the new database.

However, if the primary key of p is already in use on the second database, the existing object in the second database will be overridden when p is saved.

You can avoid this in two ways. First, you can clear the primary key of the instance. If an object has no primary key, Django will treat it as a new object, avoiding any loss of data on the second database:

The second option is to use the force_insert option to save() to ensure that Django does an SQL INSERT:

This will ensure that the person named Fred will have the same primary key on both databases. If that primary key is already in use when you try to save onto the second database, an error will be raised.

By default, a call to delete an existing object will be executed on the same database that was used to retrieve the object in the first place:

To specify the database from which a model will be deleted, pass a using keyword argument to the Model.delete() method. This argument works just like the using keyword argument to save().

For example, if you’re migrating a user from the legacy_users database to the new_users database, you might use these commands:

Use the db_manager() method on managers to give managers access to a non-default database.

For example, say you have a custom manager method that touches the database – User.objects.create_user(). Because create_user() is a manager method, not a QuerySet method, you can’t do User.objects.using('new_users').create_user(). (The create_user() method is only available on User.objects, the manager, not on QuerySet objects derived from the manager.) The solution is to use db_manager(), like this:

db_manager() returns a copy of the manager bound to the database you specify.

If you’re overriding get_queryset() on your manager, be sure to either call the method on the parent (using super()) or do the appropriate handling of the _db attribute on the manager (a string containing the name of the database to use).

For example, if you want to return a custom QuerySet class from the get_queryset method, you could do this:

Django’s admin doesn’t have any explicit support for multiple databases. If you want to provide an admin interface for a model on a database other than that specified by your router chain, you’ll need to write custom ModelAdmin classes that will direct the admin to use a specific database for content.

ModelAdmin objects have the following methods that require customization for multiple-database support:

The implementation provided here implements a multi-database strategy where all objects of a given type are stored on a specific database (e.g., all User objects are in the other database). If your usage of multiple databases is more complex, your ModelAdmin will need to reflect that strategy.

InlineModelAdmin objects can be handled in a similar fashion. They require three customized methods:

Once you’ve written your model admin definitions, they can be registered with any Admin instance:

This example sets up two admin sites. On the first site, the Author and Publisher objects are exposed; Publisher objects have a tabular inline showing books published by that publisher. The second site exposes just publishers, without the inlines.

If you are using more than one database you can use django.db.connections to obtain the connection (and cursor) for a specific database. django.db.connections is a dictionary-like object that allows you to retrieve a specific connection using its alias:

Django doesn’t currently provide any support for foreign key or many-to-many relationships spanning multiple databases. If you have used a router to partition models to different databases, any foreign key and many-to-many relationships defined by those models must be internal to a single database.

This is because of referential integrity. In order to maintain a relationship between two objects, Django needs to know that the primary key of the related object is valid. If the primary key is stored on a separate database, it’s not possible to easily evaluate the validity of a primary key.

If you’re using Postgres, SQLite, Oracle, or MySQL with InnoDB, this is enforced at the database integrity level – database level key constraints prevent the creation of relations that can’t be validated.

However, if you’re using MySQL with MyISAM tables, there is no enforced referential integrity; as a result, you may be able to ‘fake’ cross database foreign keys. However, this configuration is not officially supported by Django.

Several contrib apps include models, and some apps depend on others. Since cross-database relationships are impossible, this creates some restrictions on how you can split these models across databases:

each one of contenttypes.ContentType, sessions.Session and sites.Site can be stored in any database, given a suitable router.

auth models — User, Group and Permission — are linked together and linked to ContentType, so they must be stored in the same database as ContentType.

admin depends on auth, so its models must be in the same database as auth.

flatpages and redirects depend on sites, so their models must be in the same database as sites.

In addition, some objects are automatically created just after migrate creates a table to hold them in a database:

a ContentType for each model (including those not stored in that database),

the Permissions for each model (including those not stored in that database).

For common setups with multiple databases, it isn’t useful to have these objects in more than one database. Common setups include primary/replica and connecting to external databases. Therefore, it’s recommended to write a database router that allows synchronizing these three models to only one database. Use the same approach for contrib and third-party apps that don’t need their tables in multiple databases.

If you’re synchronizing content types to more than one database, be aware that their primary keys may not match across databases. This may result in data corruption or data loss.

---

## Performing raw SQL queries¶

**URL:** https://docs.djangoproject.com/en/stable/topics/db/sql/

**Contents:**
- Performing raw SQL queries¶
- Performing raw queries¶
  - Mapping query fields to model fields¶
  - Index lookups¶
  - Deferring model fields¶
  - Adding annotations¶
  - Passing parameters into raw()¶
- Executing custom SQL directly¶
  - Connections and cursors¶
    - Calling stored procedures¶

Django gives you two ways of performing raw SQL queries: you can use Manager.raw() to perform raw queries and return model instances, or you can avoid the model layer entirely and execute custom SQL directly.

Explore the ORM before using raw SQL!

The Django ORM provides many tools to express queries without writing raw SQL. For example:

The QuerySet API is extensive.

You can annotate and aggregate using many built-in database functions. Beyond those, you can create custom query expressions.

Before using raw SQL, explore the ORM. Ask on one of the support channels to see if the ORM supports your use case.

You should be very careful whenever you write raw SQL. Every time you use it, you should properly escape any parameters that the user can control by using params in order to protect against SQL injection attacks. Please read more about SQL injection protection.

The raw() manager method can be used to perform raw SQL queries that return model instances:

This method takes a raw SQL query, executes it, and returns a django.db.models.query.RawQuerySet instance. This RawQuerySet instance can be iterated over like a normal QuerySet to provide object instances.

This is best illustrated with an example. Suppose you have the following model:

You could then execute custom SQL like so:

This example isn’t very exciting – it’s exactly the same as running Person.objects.all(). However, raw() has a bunch of other options that make it very powerful.

Where did the name of the Person table come from in that example?

By default, Django figures out a database table name by joining the model’s “app label” – the name you used in manage.py startapp – to the model’s class name, with an underscore between them. In the example we’ve assumed that the Person model lives in an app named myapp, so its table would be myapp_person.

For more details check out the documentation for the db_table option, which also lets you manually set the database table name.

No checking is done on the SQL statement that is passed in to .raw(). Django expects that the statement will return a set of rows from the database, but does nothing to enforce that. If the query does not return rows, a (possibly cryptic) error will result.

If you are performing queries on MySQL, note that MySQL’s silent type coercion may cause unexpected results when mixing types. If you query on a string type column, but with an integer value, MySQL will coerce the types of all values in the table to an integer before performing the comparison. For example, if your table contains the values 'abc', 'def' and you query for WHERE mycolumn=0, both rows will match. To prevent this, perform the correct typecasting before using the value in a query.

raw() automatically maps fields in the query to fields on the model.

The order of fields in your query doesn’t matter. In other words, both of the following queries work identically:

Matching is done by name. This means that you can use SQL’s AS clauses to map fields in the query to model fields. So if you had some other table that had Person data in it, you could easily map it into Person instances:

As long as the names match, the model instances will be created correctly.

Alternatively, you can map fields in the query to model fields using the translations argument to raw(). This is a dictionary mapping names of fields in the query to names of fields on the model. For example, the above query could also be written:

raw() supports indexing, so if you need only the first result you can write:

However, the indexing and slicing are not performed at the database level. If you have a large number of Person objects in your database, it is more efficient to limit the query at the SQL level:

Fields may also be left out:

The Person objects returned by this query will be deferred model instances (see defer()). This means that the fields that are omitted from the query will be loaded on demand. For example:

From outward appearances, this looks like the query has retrieved both the first name and last name. However, this example actually issued 3 queries. Only the first names were retrieved by the raw() query – the last names were both retrieved on demand when they were printed.

There is only one field that you can’t leave out - the primary key field. Django uses the primary key to identify model instances, so it must always be included in a raw query. A FieldDoesNotExist exception will be raised if you forget to include the primary key.

You can also execute queries containing fields that aren’t defined on the model. For example, we could use PostgreSQL’s age() function to get a list of people with their ages calculated by the database:

You can often avoid using raw SQL to compute annotations by instead using a Func() expression.

If you need to perform parameterized queries, you can use the params argument to raw():

params is a list or dictionary of parameters. You’ll use %s placeholders in the query string for a list, or %(key)s placeholders for a dictionary (where key is replaced by a dictionary key), regardless of your database engine. Such placeholders will be replaced with parameters from the params argument.

Dictionary params are not supported with the SQLite backend; with this backend, you must pass parameters as a list.

Do not use string formatting on raw queries or quote placeholders in your SQL strings!

It’s tempting to write the above query as:

You might also think you should write your query like this (with quotes around %s):

Don’t make either of these mistakes.

As discussed in SQL injection protection, using the params argument and leaving the placeholders unquoted protects you from SQL injection attacks, a common exploit where attackers inject arbitrary SQL into your database. If you use string interpolation or quote the placeholder, you’re at risk for SQL injection.

Sometimes even Manager.raw() isn’t quite enough: you might need to perform queries that don’t map cleanly to models, or directly execute UPDATE, INSERT, or DELETE queries.

In these cases, you can always access the database directly, routing around the model layer entirely.

The object django.db.connection represents the default database connection. To use the database connection, call connection.cursor() to get a cursor object. Then, call cursor.execute(sql, [params]) to execute the SQL and cursor.fetchone() or cursor.fetchall() to return the resulting rows.

To protect against SQL injection, you must not include quotes around the %s placeholders in the SQL string.

Note that if you want to include literal percent signs in the query, you have to double them in the case you are passing parameters:

If you are using more than one database, you can use django.db.connections to obtain the connection (and cursor) for a specific database. django.db.connections is a dictionary-like object that allows you to retrieve a specific connection using its alias:

By default, the Python DB API will return results without their field names, which means you end up with a list of values, rather than a dict. At a small performance and memory cost, you can return results as a dict by using something like this:

Another option is to use collections.namedtuple() from the Python standard library. A namedtuple is a tuple-like object that has fields accessible by attribute lookup; it’s also indexable and iterable. Results are immutable and accessible by field names or indices, which might be useful:

The dictfetchall() and namedtuplefetchall() examples assume unique column names, since a cursor cannot distinguish columns from different tables.

Here is an example of the difference between the three:

connection and cursor mostly implement the standard Python DB-API described in PEP 249 — except when it comes to transaction handling.

If you’re not familiar with the Python DB-API, note that the SQL statement in cursor.execute() uses placeholders, "%s", rather than adding parameters directly within the SQL. If you use this technique, the underlying database library will automatically escape your parameters as necessary.

Also note that Django expects the "%s" placeholder, not the "?" placeholder, which is used by the SQLite Python bindings. This is for the sake of consistency and sanity.

Using a cursor as a context manager:

Calls a database stored procedure with the given name. A sequence (params) or dictionary (kparams) of input parameters may be provided. Most databases don’t support kparams. Of Django’s built-in backends, only Oracle supports it.

For example, given this stored procedure in an Oracle database:

---

## Search¶

**URL:** https://docs.djangoproject.com/en/stable/topics/db/search/

**Contents:**
- Search¶
- Use Cases¶
  - Standard textual queries¶
  - A database’s more advanced comparison functions¶
  - Document-based search¶
    - PostgreSQL support¶

A common task for web applications is to search some data in the database with user input. In a simple case, this could be filtering a list of objects by a category. A more complex use case might require searching with weighting, categorization, highlighting, multiple languages, and so on. This document explains some of the possible use cases and the tools you can use.

We’ll refer to the same models used in Making queries.

Text-based fields have a selection of matching operations. For example, you may wish to allow lookup up an author like so:

This is a very fragile solution as it requires the user to know an exact substring of the author’s name. A better approach could be a case-insensitive match (icontains), but this is only marginally better.

If you’re using PostgreSQL, Django provides a selection of database specific tools to allow you to leverage more complex querying options. Other databases have different selections of tools, possibly via plugins or user-defined functions. Django doesn’t include any support for them at this time. We’ll use some examples from PostgreSQL to demonstrate the kind of functionality databases may have.

Searching in other databases

All of the searching tools provided by django.contrib.postgres are constructed entirely on public APIs such as custom lookups and database functions. Depending on your database, you should be able to construct queries to allow similar APIs. If there are specific things which cannot be achieved this way, please open a ticket.

In the above example, we determined that a case insensitive lookup would be more useful. When dealing with non-English names, a further improvement is to use unaccented comparison:

This shows another issue, where we are matching against a different spelling of the name. In this case we have an asymmetry though - a search for Helen will pick up Helena or Hélène, but not the reverse. Another option would be to use a trigram_similar comparison, which compares sequences of letters.

Now we have a different problem - the longer name of “Helena Bonham Carter” doesn’t show up as it is much longer. Trigram searches consider all combinations of three letters, and compares how many appear in both search and source strings. For the longer name, there are more combinations that don’t appear in the source string, so it is no longer considered a close match.

The correct choice of comparison functions here depends on your particular data set, for example the language(s) used and the type of text being searched. All of the examples we’ve seen are on short strings where the user is likely to enter something close (by varying definitions) to the source data.

Standard database operations stop being a useful approach when you start considering large blocks of text. Whereas the examples above can be thought of as operations on a string of characters, full text search looks at the actual words. Depending on the system used, it’s likely to use some of the following ideas:

Ignoring “stop words” such as “a”, “the”, “and”.

Stemming words, so that “pony” and “ponies” are considered similar.

Weighting words based on different criteria such as how frequently they appear in the text, or the importance of the fields, such as the title or keywords, that they appear in.

There are many alternatives for using searching software, some of the most prominent are Elastic and Solr. These are full document-based search solutions. To use them with data from Django models, you’ll need a layer which translates your data into a textual document, including back-references to the database ids. When a search using the engine returns a certain document, you can then look it up in the database. There are a variety of third-party libraries which are designed to help with this process.

PostgreSQL has its own full text search implementation built-in. While not as powerful as some other search engines, it has the advantage of being inside your database and so can easily be combined with other relational queries such as categorization.

The django.contrib.postgres module provides some helpers to make these queries. For example, a query might select all the blog entries which mention “cheese”:

You can also filter on a combination of fields and on related models:

See the contrib.postgres Full text search document for complete details.

---

## URL dispatcher¶

**URL:** https://docs.djangoproject.com/en/stable/topics/http/urls/

**Contents:**
- URL dispatcher¶
- Overview¶
- How Django processes a request¶
- Example¶
- Path converters¶
- Registering custom path converters¶
- Using regular expressions¶
  - Using unnamed regular expression groups¶
  - Nested arguments¶
- What the URLconf searches against¶

A clean, elegant URL scheme is an important detail in a high-quality web application. Django lets you design URLs however you want, with no framework limitations.

See Cool URIs don’t change, by World Wide Web creator Tim Berners-Lee, for excellent arguments on why URLs should be clean and usable.

To design URLs for an app, you create a Python module informally called a URLconf (URL configuration). This module is pure Python code and is a mapping between URL path expressions to Python functions (your views).

This mapping can be as short or as long as needed. It can reference other mappings. And, because it’s pure Python code, it can be constructed dynamically.

Django also provides a way to translate URLs according to the active language. See the internationalization documentation for more information.

When a user requests a page from your Django-powered site, this is the algorithm the system follows to determine which Python code to execute:

Django determines the root URLconf module to use. Ordinarily, this is the value of the ROOT_URLCONF setting, but if the incoming HttpRequest object has a urlconf attribute (set by middleware), its value will be used in place of the ROOT_URLCONF setting.

Django loads that Python module and looks for the variable urlpatterns. This should be a sequence of django.urls.path() and/or django.urls.re_path() instances.

Django runs through each URL pattern, in order, and stops at the first one that matches the requested URL, matching against path_info.

Once one of the URL patterns matches, Django imports and calls the given view, which is a Python function (or a class-based view). The view gets passed the following arguments:

An instance of HttpRequest.

If the matched URL pattern contained no named groups, then the matches from the regular expression are provided as positional arguments.

The keyword arguments are made up of any named parts matched by the path expression that are provided, overridden by any arguments specified in the optional kwargs argument to django.urls.path() or django.urls.re_path().

If no URL pattern matches, or if an exception is raised during any point in this process, Django invokes an appropriate error-handling view. See Error handling below.

Here’s a sample URLconf:

To capture a value from the URL, use angle brackets.

Captured values can optionally include a converter type. For example, use <int:name> to capture an integer parameter. If a converter isn’t included, any string, excluding a / character, is matched.

There’s no need to add a leading slash, because every URL has that. For example, it’s articles, not /articles.

A request to /articles/2005/03/ would match the third entry in the list. Django would call the function views.month_archive(request, year=2005, month=3).

/articles/2003/ would match the first pattern in the list, not the second one, because the patterns are tested in order, and the first one is the first test to pass. Feel free to exploit the ordering to insert special cases like this. Here, Django would call the function views.special_case_2003(request)

/articles/2003 would not match any of these patterns, because each pattern requires that the URL end with a slash.

/articles/2003/03/building-a-django-site/ would match the final pattern. Django would call the function views.article_detail(request, year=2003, month=3, slug="building-a-django-site").

The following path converters are available by default:

str - Matches any non-empty string, excluding the path separator, '/'. This is the default if a converter isn’t included in the expression.

int - Matches zero or any positive integer. Returns an int.

slug - Matches any slug string consisting of ASCII letters or numbers, plus the hyphen and underscore characters. For example, building-your-1st-django-site.

uuid - Matches a formatted UUID. To prevent multiple URLs from mapping to the same page, dashes must be included and letters must be lowercase. For example, 075194d3-6885-417e-a8a8-6c931e272f00. Returns a UUID instance.

path - Matches any non-empty string, including the path separator, '/'. This allows you to match against a complete URL path rather than a segment of a URL path as with str.

For more complex matching requirements, you can define your own path converters.

A converter is a class that includes the following:

A regex class attribute, as a string.

A to_python(self, value) method, which handles converting the matched string into the type that should be passed to the view function. It should raise ValueError if it can’t convert the given value. A ValueError is interpreted as no match and as a consequence a 404 response is sent to the user unless another URL pattern matches.

A to_url(self, value) method, which handles converting the Python type into a string to be used in the URL. It should raise ValueError if it can’t convert the given value. A ValueError is interpreted as no match and as a consequence reverse() will raise NoReverseMatch unless another URL pattern matches.

Register custom converter classes in your URLconf using register_converter():

If the paths and converters syntax isn’t sufficient for defining your URL patterns, you can also use regular expressions. To do so, use re_path() instead of path().

In Python regular expressions, the syntax for named regular expression groups is (?P<name>pattern), where name is the name of the group and pattern is some pattern to match.

Here’s the example URLconf from earlier, rewritten using regular expressions:

This accomplishes roughly the same thing as the previous example, except:

The exact URLs that will match are slightly more constrained. For example, the year 10000 will no longer match since the year integers are constrained to be exactly four digits long.

Each captured argument is sent to the view as a string, regardless of what sort of match the regular expression makes.

When switching from using path() to re_path() or vice versa, it’s particularly important to be aware that the type of the view arguments may change, and so you may need to adapt your views.

As well as the named group syntax, e.g. (?P<year>[0-9]{4}), you can also use the shorter unnamed group, e.g. ([0-9]{4}).

This usage isn’t particularly recommended as it makes it easier to accidentally introduce errors between the intended meaning of a match and the arguments of the view.

In either case, using only one style within a given regex is recommended. When both styles are mixed, any unnamed groups are ignored and only named groups are passed to the view function.

Regular expressions allow nested arguments, and Django will resolve them and pass them to the view. When reversing, Django will try to fill in all outer captured arguments, ignoring any nested captured arguments. Consider the following URL patterns which optionally take a page argument:

Both patterns use nested arguments and will resolve: for example, blog/page-2/ will result in a match to blog_articles with two positional arguments: page-2/ and 2. The second pattern for comments will match comments/page-2/ with keyword argument page_number set to 2. The outer argument in this case is a non-capturing argument (?:...).

The blog_articles view needs the outermost captured argument to be reversed, page-2/ or no arguments in this case, while comments can be reversed with either no arguments or a value for page_number.

Nested captured arguments create a strong coupling between the view arguments and the URL as illustrated by blog_articles: the view receives part of the URL (page-2/) instead of only the value the view is interested in. This coupling is even more pronounced when reversing, since to reverse the view we need to pass the piece of URL instead of the page number.

As a rule of thumb, only capture the values the view needs to work with and use non-capturing arguments when the regular expression needs an argument but the view ignores it.

The URLconf searches against the requested URL, as a normal Python string. This does not include GET or POST parameters, or the domain name.

For example, in a request to https://www.example.com/myapp/, the URLconf will look for myapp/.

In a request to https://www.example.com/myapp/?page=3, the URLconf will look for myapp/.

The URLconf doesn’t look at the request method. In other words, all request methods – POST, GET, HEAD, etc. – will be routed to the same function for the same URL.

A convenient trick is to specify default parameters for your views’ arguments. Here’s an example URLconf and view:

In the above example, both URL patterns point to the same view – views.page – but the first pattern doesn’t capture anything from the URL. If the first pattern matches, the page() function will use its default argument for num, 1. If the second pattern matches, page() will use whatever num value was captured.

Django processes regular expressions in the urlpatterns list which is compiled the first time it’s accessed. Subsequent requests use the cached configuration via the URL resolver.

urlpatterns should be a sequence of path() and/or re_path() instances.

When Django can’t find a match for the requested URL, or when an exception is raised, Django invokes an error-handling view.

The views to use for these cases are specified by four variables. Their default values should suffice for most projects, but further customization is possible by overriding their default values.

See the documentation on customizing error views for the full details.

Such values can be set in your root URLconf. Setting these variables in any other URLconf will have no effect.

Values must be callables, or strings representing the full Python import path to the view that should be called to handle the error condition at hand.

handler400 – See django.conf.urls.handler400.

handler403 – See django.conf.urls.handler403.

handler404 – See django.conf.urls.handler404.

handler500 – See django.conf.urls.handler500.

At any point, your urlpatterns can “include” other URLconf modules. This essentially “roots” a set of URLs below other ones.

For example, here’s an excerpt of the URLconf for the Django website itself. It includes a number of other URLconfs:

Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

Another possibility is to include additional URL patterns by using a list of path() instances. For example, consider this URLconf:

In this example, the /credit/reports/ URL will be handled by the credit_views.report() Django view.

This can be used to remove redundancy from URLconfs where a single pattern prefix is used repeatedly. For example, consider this URLconf:

We can improve this by stating the common path prefix only once and grouping the suffixes that differ:

An included URLconf receives any captured parameters from parent URLconfs, so the following example is valid:

In the above example, the captured "username" variable is passed to the included URLconf, as expected.

URLconfs have a hook that lets you pass extra arguments to your view functions, as a Python dictionary.

The path() function can take an optional third argument which should be a dictionary of extra keyword arguments to pass to the view function.

In this example, for a request to /blog/2005/, Django will call views.year_archive(request, year=2005, foo='bar').

This technique is used in the syndication framework to pass metadata and options to views.

Dealing with conflicts

It’s possible to have a URL pattern which captures named keyword arguments, and also passes arguments with the same names in its dictionary of extra arguments. When this happens, the arguments in the dictionary will be used instead of the arguments captured in the URL.

Similarly, you can pass extra options to include() and each line in the included URLconf will be passed the extra options.

For example, these two URLconf sets are functionally identical:

Note that extra options will always be passed to every line in the included URLconf, regardless of whether the line’s view actually accepts those options as valid. For this reason, this technique is only useful if you’re certain that every view in the included URLconf accepts the extra options you’re passing.

A common need when working on a Django project is the possibility to obtain URLs in their final forms either for embedding in generated content (views and assets URLs, URLs shown to the user, etc.) or for handling of the navigation flow on the server side (redirections, etc.)

It is strongly desirable to avoid hardcoding these URLs (a laborious, non-scalable and error-prone strategy). Equally dangerous is devising ad-hoc mechanisms to generate URLs that are parallel to the design described by the URLconf, which can result in the production of URLs that become stale over time.

In other words, what’s needed is a DRY mechanism. Among other advantages it would allow evolution of the URL design without having to go over all the project source code to search and replace outdated URLs.

The primary piece of information we have available to get a URL is an identification (e.g. the name) of the view in charge of handling it. Other pieces of information that necessarily must participate in the lookup of the right URL are the types (positional, keyword) and values of the view arguments.

Django provides a solution such that the URL mapper is the only repository of the URL design. You feed it with your URLconf and then it can be used in both directions:

Starting with a URL requested by the user/browser, it calls the right Django view providing any arguments it might need with their values as extracted from the URL.

Starting with the identification of the corresponding Django view plus the values of arguments that would be passed to it, obtain the associated URL.

The first one is the usage we’ve been discussing in the previous sections. The second one is what is known as reverse resolution of URLs, reverse URL matching, reverse URL lookup, or simply URL reversing.

Django provides tools for performing URL reversing that match the different layers where URLs are needed:

In templates: Using the url template tag.

In Python code: Using the reverse() function.

In higher level code related to handling of URLs of Django model instances: The get_absolute_url() method.

Consider again this URLconf entry:

According to this design, the URL for the archive corresponding to year nnnn is /articles/<nnnn>/.

You can obtain these in template code by using:

If, for some reason, it was decided that the URLs where content for yearly article archives are published at should be changed then you would only need to change the entry in the URLconf.

In some scenarios where views are of a generic nature, a many-to-one relationship might exist between URLs and views. For these cases the view name isn’t a good enough identifier for it when comes the time of reversing URLs. Read the next section to know about the solution Django provides for this.

In order to perform URL reversing, you’ll need to use named URL patterns as done in the examples above. The string used for the URL name can contain any characters you like. You are not restricted to valid Python names.

When naming URL patterns, choose names that are unlikely to clash with other applications’ choice of names. If you call your URL pattern comment and another application does the same thing, the URL that reverse() finds depends on whichever pattern is last in your project’s urlpatterns list.

Putting a prefix on your URL names, perhaps derived from the application name (such as myapp-comment instead of comment), decreases the chance of collision.

You can deliberately choose the same URL name as another application if you want to override a view. For example, a common use case is to override the LoginView. Parts of Django and most third-party apps assume that this view has a URL pattern with the name login. If you have a custom login view and give its URL the name login, reverse() will find your custom view as long as it’s in urlpatterns after django.contrib.auth.urls is included (if that’s included at all).

You may also use the same name for multiple URL patterns if they differ in their arguments. In addition to the URL name, reverse() matches the number of arguments and the names of the keyword arguments. Path converters can also raise ValueError to indicate no match, see Registering custom path converters for details.

URL namespaces allow you to uniquely reverse named URL patterns even if different applications use the same URL names. It’s a good practice for third-party apps to always use namespaced URLs (as we did in the tutorial). Similarly, it also allows you to reverse URLs if multiple instances of an application are deployed. In other words, since multiple instances of a single application will share named URLs, namespaces provide a way to tell these named URLs apart.

Django applications that make proper use of URL namespacing can be deployed more than once for a particular site. For example django.contrib.admin has an AdminSite class which allows you to deploy more than one instance of the admin. In a later example, we’ll discuss the idea of deploying the polls application from the tutorial in two different locations so we can serve the same functionality to two different audiences (authors and publishers).

A URL namespace comes in two parts, both of which are strings:

This describes the name of the application that is being deployed. Every instance of a single application will have the same application namespace. For example, Django’s admin application has the somewhat predictable application namespace of 'admin'.

This identifies a specific instance of an application. Instance namespaces should be unique across your entire project. However, an instance namespace can be the same as the application namespace. This is used to specify a default instance of an application. For example, the default Django admin instance has an instance namespace of 'admin'.

Namespaced URLs are specified using the ':' operator. For example, the main index page of the admin application is referenced using 'admin:index'. This indicates a namespace of 'admin', and a named URL of 'index'.

Namespaces can also be nested. The named URL 'sports:polls:index' would look for a pattern named 'index' in the namespace 'polls' that is itself defined within the top-level namespace 'sports'.

When given a namespaced URL (e.g. 'polls:index') to resolve, Django splits the fully qualified name into parts and then tries the following lookup:

First, Django looks for a matching application namespace (in this example, 'polls'). This will yield a list of instances of that application.

If there is a current application defined, Django finds and returns the URL resolver for that instance. The current application can be specified with the current_app argument to the reverse() function.

The url template tag uses the namespace of the currently resolved view as the current application in a RequestContext. You can override this default by setting the current application on the request.current_app attribute.

If there is no current application, Django looks for a default application instance. The default application instance is the instance that has an instance namespace matching the application namespace (in this example, an instance of polls called 'polls').

If there is no default application instance, Django will pick the last deployed instance of the application, whatever its instance name may be.

If the provided namespace doesn’t match an application namespace in step 1, Django will attempt a direct lookup of the namespace as an instance namespace.

If there are nested namespaces, these steps are repeated for each part of the namespace until only the view name is unresolved. The view name will then be resolved into a URL in the namespace that has been found.

To show this resolution strategy in action, consider an example of two instances of the polls application from the tutorial: one called 'author-polls' and one called 'publisher-polls'. Assume we have enhanced that application so that it takes the instance namespace into consideration when creating and displaying polls.

Using this setup, the following lookups are possible:

If one of the instances is current - say, if we were rendering the detail page in the instance 'author-polls' - 'polls:index' will resolve to the index page of the 'author-polls' instance; i.e. both of the following will result in "/author-polls/".

In the method of a class-based view:

If there is no current instance - say, if we were rendering a page somewhere else on the site - 'polls:index' will resolve to the last registered instance of polls. Since there is no default instance (instance namespace of 'polls'), the last instance of polls that is registered will be used. This would be 'publisher-polls' since it’s declared last in the urlpatterns.

'author-polls:index' will always resolve to the index page of the instance 'author-polls' (and likewise for 'publisher-polls').

If there were also a default instance - i.e., an instance named 'polls' - the only change from above would be in the case where there is no current instance (the second item in the list above). In this case 'polls:index' would resolve to the index page of the default instance instead of the instance declared last in urlpatterns.

Application namespaces of included URLconfs can be specified in two ways.

Firstly, you can set an app_name attribute in the included URLconf module, at the same level as the urlpatterns attribute. You have to pass the actual module, or a string reference to the module, to include(), not the list of urlpatterns itself.

The URLs defined in polls.urls will have an application namespace polls.

Secondly, you can include an object that contains embedded namespace data. If you include() a list of path() or re_path() instances, the URLs contained in that object will be added to the global namespace. However, you can also include() a 2-tuple containing:

This will include the nominated URL patterns into the given application namespace.

The instance namespace can be specified using the namespace argument to include(). If the instance namespace is not specified, it will default to the included URLconf’s application namespace. This means it will also be the default instance for that namespace.

---

## Using Django¶

**URL:** https://docs.djangoproject.com/en/stable/topics/

**Contents:**
- Using Django¶

Introductions to all the key parts of Django you’ll need to know:

---

## View decorators¶

**URL:** https://docs.djangoproject.com/en/stable/topics/http/decorators/

**Contents:**
- View decorators¶
- Allowed HTTP methods¶
- Conditional view processing¶
- GZip compression¶
- Vary headers¶
- Caching¶
- Common¶

Django provides several decorators that can be applied to views to support various HTTP features.

See Decorating the class for how to use these decorators with class-based views.

The decorators in django.views.decorators.http can be used to restrict access to views based on the request method. These decorators will return a django.http.HttpResponseNotAllowed if the conditions are not met.

Decorator to require that a view only accepts particular request methods. Usage:

Note that request methods should be in uppercase.

Decorator to require that a view only accepts the GET method.

Decorator to require that a view only accepts the POST method.

Decorator to require that a view only accepts the GET and HEAD methods. These methods are commonly considered “safe” because they should not have the significance of taking an action other than retrieving the requested resource.

Web servers should automatically strip the content of responses to HEAD requests while leaving the headers unchanged, so you may handle HEAD requests exactly like GET requests in your views. Since some software, such as link checkers, rely on HEAD requests, you might prefer using require_safe instead of require_GET.

The following decorators in django.views.decorators.http can be used to control caching behavior on particular views.

This decorator provides the conditional GET operation handling of ConditionalGetMiddleware to a view.

These decorators can be used to generate ETag and Last-Modified headers; see conditional view processing.

The decorators in django.views.decorators.gzip control content compression on a per-view basis.

This decorator compresses content if the browser allows gzip compression. It sets the Vary header accordingly, so that caches will base their storage on the Accept-Encoding header.

The decorators in django.views.decorators.vary can be used to control caching based on specific request headers.

The Vary header defines which request headers a cache mechanism should take into account when building its cache key.

See using vary headers.

The decorators in django.views.decorators.cache control server and client-side caching.

This decorator patches the response’s Cache-Control header by adding all of the keyword arguments to it. See patch_cache_control() for the details of the transformation.

This decorator adds an Expires header to the current date/time.

This decorator adds a Cache-Control: max-age=0, no-cache, no-store, must-revalidate, private header to a response to indicate that a page should never be cached.

Each header is only added if it isn’t already set.

The decorators in django.views.decorators.common allow per-view customization of CommonMiddleware behavior.

This decorator allows individual views to be excluded from APPEND_SLASH URL normalization.

---

## Writing views¶

**URL:** https://docs.djangoproject.com/en/stable/topics/http/views/

**Contents:**
- Writing views¶
- A simple view¶
- Mapping URLs to views¶
- Returning errors¶
  - The Http404 exception¶
- Customizing error views¶
  - Testing custom error views¶
- Async views¶

A view function, or view for short, is a Python function that takes a web request and returns a web response. This response can be the HTML contents of a web page, or a redirect, or a 404 error, or an XML document, or an image … or anything, really. The view itself contains whatever arbitrary logic is necessary to return that response. This code can live anywhere you want, as long as it’s on your Python path. There’s no other requirement–no “magic,” so to speak. For the sake of putting the code somewhere, the convention is to put views in a file called views.py, placed in your project or application directory.

Here’s a view that returns the current date and time, as an HTML document:

Let’s step through this code one line at a time:

First, we import the class HttpResponse from the django.http module, along with Python’s datetime library.

Next, we define a function called current_datetime. This is the view function. Each view function takes an HttpRequest object as its first parameter, which is typically named request.

Note that the name of the view function doesn’t matter; it doesn’t have to be named in a certain way in order for Django to recognize it. We’re calling it current_datetime here, because that name clearly indicates what it does.

The view returns an HttpResponse object that contains the generated response. Each view function is responsible for returning an HttpResponse object. (There are exceptions, but we’ll get to those later.)

Django includes a TIME_ZONE setting that defaults to America/Chicago. This probably isn’t where you live, so you might want to change it in your settings file.

So, to recap, this view function returns an HTML page that includes the current date and time. To display this view at a particular URL, you’ll need to create a URLconf; see URL dispatcher for instructions.

Django provides help for returning HTTP error codes. There are subclasses of HttpResponse for a number of common HTTP status codes other than 200 (which means “OK”). You can find the full list of available subclasses in the request/response documentation. Return an instance of one of those subclasses instead of a normal HttpResponse in order to signify an error. For example:

There isn’t a specialized subclass for every possible HTTP response code, since many of them aren’t going to be that common. However, as documented in the HttpResponse documentation, you can also pass the HTTP status code into the constructor for HttpResponse to create a return class for any status code you like. For example:

Because 404 errors are by far the most common HTTP error, there’s an easier way to handle those errors.

When you return an error such as HttpResponseNotFound, you’re responsible for defining the HTML of the resulting error page:

For convenience, and because it’s a good idea to have a consistent 404 error page across your site, Django provides an Http404 exception. If you raise Http404 at any point in a view function, Django will catch it and return the standard error page for your application, along with an HTTP error code 404.

In order to show customized HTML when Django returns a 404, you can create an HTML template named 404.html and place it in the top level of your template tree. This template will then be served when DEBUG is set to False.

When DEBUG is True, you can provide a message to Http404 and it will appear in the standard 404 debug template. Use these messages for debugging purposes; they generally aren’t suitable for use in a production 404 template.

The default error views in Django should suffice for most web applications, but can easily be overridden if you need any custom behavior. Specify the handlers as seen below in your URLconf (setting them anywhere else will have no effect).

The page_not_found() view is overridden by handler404:

The server_error() view is overridden by handler500:

The permission_denied() view is overridden by handler403:

The bad_request() view is overridden by handler400:

Use the CSRF_FAILURE_VIEW setting to override the CSRF error view.

To test the response of a custom error handler, raise the appropriate exception in a test view. For example:

As well as being synchronous functions, views can also be asynchronous (“async”) functions, normally defined using Python’s async def syntax. Django will automatically detect these and run them in an async context. However, you will need to use an async server based on ASGI to get their performance benefits.

Here’s an example of an async view:

You can read more about Django’s async support, and how to best use async views, in Asynchronous support.

---
