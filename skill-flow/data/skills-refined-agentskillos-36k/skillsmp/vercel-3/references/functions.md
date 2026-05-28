# Vercel - Functions

**Pages:** 33

---

## Advanced Configuration

**URL:** https://vercel.com/docs/functions/configuring-functions/advanced-configuration

**Contents:**
- Advanced Configuration
- Adding utility files to the directory
- Bundling Vercel Functions

For an advanced configuration, you can create a file to use Runtimes and other customizations. To view more about the properties you can customize, see the Configuring Functions and Project config with vercel.json.

If your use case requires that you work asynchronously with the results of a function invocation, you may need to consider a queuing, pooling, or streaming approach because of how functions are created on Vercel.

Sometimes, you need to place extra code files, such as or , inside the folder. To avoid turning these files into functions, Vercel ignores files with the following characters:

If your file uses any of the above, it will not be turned into a function.

In order to optimize resources, Vercel uses a process to bundle as many routes as possible into a single Vercel Function.

To provide more control over the bundling process, you can use the property in your file to define the configuration for a route. If a configuration is present, Vercel will bundle functions based on the configuration first. Vercel will then bundle together the remaining routes, optimizing for how many functions are created.

This bundling process is currently only enabled for Next.js, but it will be enabled in other scenarios in the future.

---

## Configuring Maximum Duration for Vercel Functions

**URL:** https://vercel.com/docs/functions/configuring-functions/duration

**Contents:**
- Configuring Maximum Duration for Vercel Functions
- Consequences of changing the maximum duration
- Maximum duration for different runtimes
    - Node.js, Next.js (>= 13.5 or higher), SvelteKit, Astro, Nuxt, and Remix
    - Other Frameworks and runtimes, Next.js versions older than 13.5, Go, Python, or Ruby
- Setting a default maximum duration
  - Dashboard
  - file
- Duration limits

The maximum duration configuration determines the longest time that a function can run. This guide will walk you through configuring the maximum duration for your Vercel Functions.

You are charged based on the amount of time your function has run, also known as its duration. It specifically refers to the actual time elapsed during the entire invocation, regardless of whether that time was actively used for processing or spent waiting for a streamed response. To learn more see Managing function duration.

For this reason, Vercel has set a default maximum duration for functions, which can be useful for preventing runaway functions from consuming resources indefinitely.

If a function runs for longer than its set maximum duration, Vercel will terminate it. Therefore, when setting this duration, it's crucial to strike a balance:

The method of configuring the maximum duration depends on your framework and runtime:

For these runtimes / frameworks, you can configure the number of seconds directly in your function:

For these runtimes and frameworks, configure the property of the object in your file:

If your Next.js project is configured to use src directory, you will need to prefix your function routes with for them to be detected.

The order in which you specify file patterns is important. For more information, see Glob pattern.

While Vercel specifies defaults for the maximum duration of a function, you can also override it in the following ways:

This glob pattern will match everything in the specified path, so you may wish to be more specific by adding a file type, such as instead.

Vercel Functions have the following defaults and maximum limits for the duration of a function with fluid compute (enabled by default):

If you have disabled fluid compute, the following defaults and maximum limits apply:

---

## Runtimes

**URL:** https://vercel.com/docs/functions/runtimes

**Contents:**
- Runtimes
- Official runtimes
- Community runtimes
- Features
  - Location
  - Failover mode
  - Isolation boundary
  - File system support
  - Archiving
  - Functions created per deployment

Vercel supports multiple runtimes for your functions. Each runtime has its own set of libraries, APIs, and functionality that provides different trade-offs and benefits.

Runtimes transform your source code into Functions, which are served by our CDN.

Vercel Functions support the following official runtimes:

If you would like to use a language that Vercel does not support by default, you can use a community runtime by setting the property in . For more information on configuring other runtimes, see Configuring your function runtime.

The following community runtimes are recommended by Vercel:

You can create a community runtime by using the Runtime API. Alternatively, you can use the Build Output API.

Location refers to where your functions are executed. Vercel Functions are region-first, and can be deployed to up to 3 regions on Pro or 18 on Enterprise. Deploying to more regions than your plan allows for will cause your deployment to fail before entering the build step.

Vercel's failover mode refers to the system's behavior when a function fails to execute because of data center downtime.

Vercel provides redundancy and automatic failover for Vercel Functions using the Edge runtime. For Vercel Functions on the Node.js runtime, you can use the configuration in your file to specify which regions the function should automatically failover to.

In Vercel, the isolation boundary refers to the separation of individual instances of a function to ensure they don't interfere with each other. This provides a secure execution environment for each function.

With traditional serverless infrastructure, each function uses a microVM for isolation, which provides strong security but also makes them slower to start and more resource intensive.

Filesystem support refers to a function's ability to read and write to the filesystem. Vercel functions have a read-only filesystem with writable scratch space up to 500 MB.

Vercel Functions are archived when they are not invoked:

Archived functions will be unarchived when they're invoked, which can make the initial cold start time at least 1 second longer than usual.

When using Next.js or SvelteKit on Vercel, dynamic code (APIs, server-rendered pages, or dynamic requests) will be bundled into the fewest number of Vercel Functions possible, to help reduce cold starts. Because of this, it's unlikely that you'll hit the limit of 12 bundled Vercel Functions per deployment.

When using other frameworks, or Vercel Functions directly without a framework, every API maps directly to one Vercel Function. For example, having five files inside would create five Vercel Functions. For Hobby, this approach is limited to 12 Vercel Functions per deployment.

A runtime can retain an archive of up to 100 MB of the filesystem at build time. The cache key is generated as a combination of:

The cache will be invalidated if any of those items changes. You can bypass the cache by running .

You can use environment variables to manage dynamic values and sensitive information affecting the operation of your functions. Vercel allows developers to define these variables either at deployment or during runtime.

You can use a total of 64 KB in environments variables per-deployment on Vercel. This limit is for all variables combined, and so no single variable can be larger than 64 KB.

The following features are supported by Vercel Functions:

Vercel's Secure Compute feature offers enhanced security for your Vercel Functions, including dedicated IP addresses and VPN options. This can be particularly important for functions that handle sensitive data.

Streaming refers to the ability to send or receive data in a continuous flow.

The Node.js runtime supports streaming by default. Streaming is also supported when using the Python runtime.

Vercel Functions have a maximum duration, meaning that it isn't possible to stream indefinitely.

Node.js and Edge runtime streaming functions support the method, which allows for an asynchronous task to be performed during the lifecycle of the request. This means that while your function will likely run for the same amount of time, your end-users can have a better, more interactive experience.

Cron jobs are time-based scheduling tools used to automate repetitive tasks. When a cron job is triggered through the cron expression, it calls a Vercel Function.

From your function, you can communicate with a choice of data stores. To ensure low-latency responses, it's crucial to have compute close to your databases. Always deploy your databases in regions closest to your functions to avoid long network roundtrips. For more information, see our best practices documentation.

An Edge Config is a global data store that enables experimentation with feature flags, A/B testing, critical redirects, and IP blocking. It enables you to read data at the edge without querying an external database or hitting upstream servers.

Vercel supports Tracing that allows you to send OpenTelemetry traces from your Vercel Functions to any application performance monitoring (APM) vendors.

---

## Routing Middleware API

**URL:** https://vercel.com/docs/routing-middleware/api

**Contents:**
- Routing Middleware API
- Routing Middleware file location and name
- object
  - Match paths based on custom matcher config
    - Match a single path
    - Match multiple paths
    - Match using regex
    - Match based on a negative lookahead
    - Match based on character matching
  - Match paths based on conditional statements

The Routing Middleware file should be named middleware.ts and placed at the root of your project, at the same level as your file. This is where Vercel will look for the Routing Middleware when processing requests.

The Routing Middleware must be a default export, with the function being named anything you like. For example, you can name it , , or any other name that makes sense for your application.

Routing Middleware will be invoked for every route in your project. If you only want it to be run on specific paths, you can define those either with a custom matcher config or with conditional statements.

You can also use the option to specify which runtime you would like to use. The default is .

While the option is the preferred method, as it does not get invoked on every request, you can also use conditional statements to only run the Routing Middleware when it matches specific paths.

To decide which route the Routing Middleware should be run on, you can use a custom matcher config to filter on specific paths. The matcher property can be used to define either a single path, or using an array syntax for multiple paths.

The matcher config has full regex support for cases such as negative lookaheads or character matching.

To match all request paths except for the ones starting with:

For help on writing your own regex path matcher, see Path to regexp.

See the helper methods below for more information on using the package.

To change the runtime from the default, update the option as follows:

To use the Bun runtime with Routing Middleware, set the property in your file as well as using the config shown above to :

The Routing Middleware signature is made up of two parameters: and . The parameter is an instance of the Request object, and the parameter is an object containing the method. Both parameters are optional.

Routing Middleware comes with built in helpers that are based on the native , , and objects.

See the section on Routing Middleware helpers for more information.

If you're not using a framework, you must either add "type": "module" to your package.json or change your JavaScript Functions' file extensions from .js to .mjs

The object represents an HTTP request. It is a wrapper around the Fetch API object. When using TypeScript, you do not need to import the object, as it is already available in the global scope.

The method is from the interface. It accepts a as an argument, which will keep the function running until the resolves.

It can be used to keep the function running after a response has been sent. This is useful when you have an async task that you want to keep running after returning a response.

The example below will:

If you're not using a framework, you must either add "type": "module" to your package.json or change your JavaScript Functions' file extensions from .js to .mjs

You can use Vercel-specific helper methods to access a request's geolocation, IP Address, and more when deploying Middleware on Vercel.

These helpers are exclusive to Vercel, and will not work on other providers, even if your app is built with Next.js.

Each property returns a , or .

The is an extension of the standard object, which contains the function. The following example works in middleware for all frameworks:

The following example adds a custom header, then continues the Routing Middleware chain:

This no-op example will return a response with no further action:

---

## Concurrency scaling

**URL:** https://vercel.com/docs/functions/concurrency-scaling

**Contents:**
- Concurrency scaling
- Automatic concurrency scaling
- Burst concurrency limits

Vercel automatically scales your functions to handle traffic surges, ensuring optimal performance during increased loads.

The concurrency model on Vercel refers to how many instances of your functions can run simultaneously. All functions on Vercel scale automatically based on demand to manage increased traffic loads.

With automatic concurrency scaling, your Vercel Functions can scale to a maximum of 30,000 on Pro or 100,000 on Enterprise, maintaining optimal performance during traffic surges. The scaling is based on the burst concurrency limit of 1000 concurrent executions per 10 seconds, per region. Additionally, Enterprise customers can purchase extended concurrency.

Vercel's infrastructure monitors your usage and preemptively adjusts the concurrency limit to cater to growing traffic, allowing your applications to scale without your intervention.

Automatic concurrency scaling is available on all plans.

Burst concurrency refers to Vercel's ability to temporarily handle a sudden influx of traffic by allowing a higher concurrency limit.

Upon detecting a traffic spike, Vercel temporarily increases the concurrency limit to accommodate the additional load. The initial increase allows for a maximum of 1000 concurrent executions per 10 seconds. After the traffic burst subsides, the concurrency limit gradually returns to its previous state, ensuring a smooth scaling experience.

The scaling process may take several minutes during traffic surges, especially substantial ones. While this delay aligns with natural traffic curves to minimize potential impact on your application's performance, it's advisable to monitor the scaling process for optimal operation.

You can monitor burst concurrency events using Log Drains, or Runtime Logs to help you understand and optimize your application's performance.

If you exceed the limit, a error will trigger.

---

## @vercel/functions API Reference (Node.js)

**URL:** https://vercel.com/docs/functions/functions-api-reference/vercel-functions-package

**Contents:**
- @vercel/functions API Reference (Node.js)
- Install and use the package
- Usage with Next.js
- Helper methods (non-Next.js usage or older Next.js versions)
    - Limits
    - Specification
    - Limits and usage
  - Database Connection Pool Management
  - OIDC methods

For OIDC methods, import

If you’re using Next.js 15.1 or above, we recommend using the built-in function from instead of .

allows you to schedule work that runs after the response has been sent or the prerender has completed. This is especially useful to avoid blocking rendering for side effects such as logging, analytics, or other background tasks.

If you're not using Next.js 15.1 or above (or you are using other frameworks), you can use the methods from below.

Description: Extends the lifetime of the request handler for the lifetime of the given Promise. The method enqueues an asynchronous task to be performed during the lifecycle of the request. You can use it for anything that can be done after the response is sent, such as logging, sending analytics, or updating a cache, without blocking the response. is available in Node.js and in the Edge Runtime.

Promises passed to will have the same timeout as the function itself. If the function times out, the promises will be cancelled.

If you're using Next.js 15.1 or above, use from instead. Otherwise, see below.

Description: Gets the System Environment Variables exposed by Vercel.

Description: Returns the location information for the incoming request, in the following way:

Description: Returns the IP address of the request from the headers.

Description: Marks a cache tag as stale, causing cache entries associated with that tag to be revalidated in the background on the next request.

Description: Marks a cache tag as deleted, causing cache entries associated with that tag to be revalidated in the foreground on the next request. Use this method with caution because one tag can be associated with many paths and deleting the cache can cause many concurrent requests to the origin leading to cache stampede problem. A good use case for deleting the cache is when the origin has also been deleted, for example it returns a or status code.

Description: Marks all cached content associated with a source image as stale, causing those cache entries to be revalidated in the background on the next request. This invalidates all cached transformations of the source image.

Learn more about purging Vercel CDN cache.

Description: Marks all cached content associated with a source image as deleted, causing those cache entries to be revalidated in the foreground on the next request. Use this method with caution because deleting the cache can cause many concurrent requests to the origin leading to cache stampede problem. A good use case for deleting the cache is when the origin has also been deleted, for example it returns a or status code.

Learn more about purging Vercel CDN cache.

Description: Adds one or more tags to a cached response, so that you can later invalidate the cache associated with these tag(s) using .

Description: Returns a object that allows you to interact with the Vercel Runtime Cache in any Vercel region. Use this for storing and retrieving data across function, routing middleware, and build execution within a Vercel region.

provides the following methods:

After assigning tags to your cached data, use the method to invalidate all cache entries associated with that tag. This operation is propagated globally across all Vercel regions within 300ms.

The Runtime Cache is isolated per Vercel project and deployment environment ( and ). Cached data is persisted across deployments and can be invalidated either through time-based expiration or by calling . However, TTL (time-to-live) and tag updates aren't reconciled between deployments. In those cases, we recommend either purging the runtime cache or modifying the cache key.

The Runtime Cache API does not have first class integration with Incremental Static Regeneration. This means that:

The following Runtime Cache limits apply:

Usage of the Vercel Runtime Cache is charged, learn more about pricing in the regional pricing docs.

Call this function right after creating a database pool to ensure proper connection management in Fluid Compute. This function ensures that idle pool clients are properly released before functions suspend.

Supports PostgreSQL (pg), MySQL2, MariaDB, MongoDB, Redis (ioredis), Cassandra (cassandra-driver), and other compatible pool types.

This function has moved from @vercel/functions/oidc to @vercel/oidc-aws-credentials-provider. It is now deprecated from @vercel/functions and will be removed in a future release.

Description: Obtains the Vercel OIDC token and creates an AWS credential provider function that gets AWS credentials by calling the STS API.

This function has moved from @vercel/functions/oidc to @vercel/oidc. It is now deprecated from @vercel/functions and will be removed in a future release.

Description: Returns the OIDC token from the request context or the environment variable. This function first checks if the OIDC token is available in the environment variable . If it is not found there, it retrieves the token from the request context headers.

---

## Using the Go Runtime with Vercel functions

**URL:** https://vercel.com/docs/functions/runtimes/go

**Contents:**
- Using the Go Runtime with Vercel functions
- Go Version
- Go Dependencies
- Go Build Configuration
- Advanced Go Usage
  - Private Packages for Go

The Go runtime is available in Beta on all plans

The Go runtime is used by Vercel to compile Go Vercel functions that expose a single HTTP handler, from a file within an directory at your project's root.

For example, define an file inside an directory as follows:

An example index.go file inside an /api directory.

For advanced usage, such as using private packages with your Go projects, see the Advanced Go Usage section.

The exported function needs to include the HandlerFunc signature type, but can use any valid Go exported function declaration as the function name.

The Go runtime will automatically detect the file at the root of your Project to determine the version of Go to use.

If is missing or the version is not defined, the default version 1.20 will be used.

The first time the Go version is detected, it will be automatically downloaded and cached. Subsequent deployments using the same Go version will use the cached Go version instead of downloading it again.

The Go runtime will automatically detect the file at the root of your Project to install dependencies.

You can provide custom build flags by using the Environment Variable.

An example -ldflags flag with -s -w. This will remove debug information from the output file. This is the default value when no GO_BUILD_FLAGS are provided.

In order to use this runtime, no configuration is needed. You only need to create a file inside the directory.

The entry point of this runtime is a global matching files that export a function that implements the signature.

To install private packages with , add an Environment Variable named .

The value should be the URL to the Git repo including credentials, such as .

All major Git providers are supported including GitHub, GitLab, Bitbucket, as well as a self-hosted Git server.

With GitHub, you will need to create a personal token with permission to access your private repository.

---

## vercel.functions API Reference (Python)

**URL:** https://vercel.com/docs/functions/functions-api-reference/vercel-sdk-python

**Contents:**
- vercel.functions API Reference (Python)
- Install and use the package
- Helper methods
    - Specification
    - Limits and usage

Description: Gets the System Environment Variables exposed by Vercel.

Description: Returns the location information for the incoming request, in the following way:

Description: Returns the IP address of the request from the headers.

Description: Allows you to interact with the Vercel Runtime Cache in any Vercel region. Use this for storing and retrieving data across function, routing middleware, and build execution within a Vercel region.

provide the following methods:

Use in async code. It has the same API and uses the same underlying cache as , and exposes awaitable methods.

After assigning tags to your cached data, use the method to invalidate all cache entries associated with that tag. This operation is propagated globally across all Vercel regions within 300ms.

The Runtime Cache is isolated per Vercel project and deployment environment ( and ). Cached data is persisted across deployments and can be invalidated either through time-based expiration or by calling . However, TTL (time-to-live) and tag updates aren't reconciled between deployments. In those cases, we recommend either purging the runtime cache or modifying the cache key.

The Runtime Cache API does not have first class integration with Incremental Static Regeneration. This means that:

The following Runtime Cache limits apply:

Usage of the Vercel Runtime Cache is charged, learn more about pricing in the regional pricing docs.

---

## Routing Middleware

**URL:** https://vercel.com/docs/routing-middleware

**Contents:**
- Routing Middleware
- Creating a Routing Middleware
- Logging
- Using a database with Routing Middleware
- Limits on requests
- Runtime options
- Pricing
- Observability
- More resources

Routing Middleware is available on all plans

Routing Middleware executes code before a request is processed on a site, and are built on top of fluid compute. Based on the request, you can modify the response.

Because it runs globally before the cache, Routing Middleware is an effective way of providing personalization to statically generated content. Depending on the incoming request, you can execute custom logic, rewrite, redirect, add headers and more, before returning a response.

The default runtime for Routing Middlewares is Edge. See runtime options for information on how to change the runtime of your Routing Middleware.

You can use Routing Middleware with any framework. To add a Routing Middleware to your app, you need to create a middleware.ts file at your project's root directory.

Routing Middleware has full support for the API, including , , . Logs will appear inside your Vercel project by clicking View Functions Logs next to the deployment.

If your Routing Middleware depends on a database far away from one of our supported regions, the overall latency of API requests could be slower than expected, due to network latency while connecting to the database from an edge region. To avoid this issue, use a global database. Vercel has multiple global storage products, including Edge Config and Vercel Blob. You can also explore the storage category of the Vercel Marketplace to learn which option is best for you.

The following limits apply to requests processed by Routing Middleware:

Routing Middleware is available on the Node.js, Bun, and Edge runtimes. The default runtime for Routing Middleware is Edge. You can change the runtime to Node.js by exporting a object with a property in your middleware.ts file.

To use the Bun runtime, set in your file and your runtime config to .

Routing Middleware is priced using the fluid compute model, which means you are charged by the amount of compute resources used by your Routing Middleware. See the fluid compute pricing documentation for more information.

The Vercel Observability dashboard provides visibility into your routing middleware usage, including invocation counts and performance metrics. You can get more insights with Observability Plus:

Learn more about Routing Middleware by exploring the following resources:

---

## Legacy Usage & Pricing for Functions

**URL:** https://vercel.com/docs/functions/usage-and-pricing/legacy-pricing

**Contents:**
- Legacy Usage & Pricing for Functions
- Pricing
  - Hobby
  - Pro
  - Enterprise
- Viewing Function Usage
- Managing function invocations
  - Optimizing function invocations
- Managing function duration
  - Optimizing function duration

Legacy Billing Model: This page describes the legacy billing model and relates to functions which do not use Fluid Compute. All new projects use Fluid Compute by default, which bills separately for active CPU time and provisioned memory time for more cost-effective and transparent pricing.

Functions using the Node.js runtime are measured in GB-hours, which is the memory allocated for each Function in GB, multiplied by the time in hours they were running. For example, a function configured to use 3GB of memory that executes for 1 second, would be billed at 3 GB-s, requiring 1,200 executions to reach a full GB-Hr.

A function can use up to 50 ms of CPU time per execution unit. If a function uses more than 50 ms, it will be divided into multiple 50 ms units for billing purposes.

See viewing function usage for more information on how to track your usage.

This information relates to functions which do not use Fluid Compute. Fluid Compute is the default for all new functions. To learn about pricing for functions that use Fluid Compute, see Pricing.

The following table outlines the price for functions which do not use Fluid Compute.

Vercel Functions are available for free with the included usage limits:

Vercel will send you emails as you are nearing your usage limits. On the Hobby plan you will not pay for any additional usage. However, your account may be paused if you do exceed the limits.

When your Hobby team is set to paused, it remains in this state indefinitely unless you take action. This means all new and existing deployments will be paused.

If you have reached this state, your application is likely a good candidate for a Pro account.

To unpause your account, you have two main options:

Once set up, a transfer modal will appear, prompting you to transfer your previous Hobby projects to this new team. After transferring, you can continue with your projects as usual.

For teams on a Pro trial, the trial will end when your team reaches the trial limits.

Once your team exceeds the included usage, you will continue to be charged the on-demand costs going forward.

Pro teams can set up Spend Management to get notified or to automatically take action, such as using a webhook or pausing your projects when your usage hits a set spend amount.

Enterprise agreements provide custom usage and pricing for Vercel Functions, including:

See Vercel Enterprise plans for more information.

Usage metrics can be found in the Usage tab on your dashboard. Functions are invoked for every request that is served.

You can see the usage for functions using the Node.js runtime on the Serverless Functions section of the Usage tab.

You are charged based on the number of times your functions are invoked, including both successful and errored invocations, excluding cache hits. The number of invocations is calculated by the number of times your function is called, regardless of the response status code.

When using Incremental Static Regeneration with Next.js, both the option for and for will result in a Function invocation on revalidation, not for every user request.

When viewing your Functions Invocations graph, you can group by Ratio to see a total of all invocations across your team's projects that finished successfully, errored, or timed out.

Executing a Vercel Function will increase Edge Request usage as well. Caching your Vercel Function reduces the GB-hours of your functions but does not reduce the Edge Request usage that comes with executing it.

Legacy Billing Model: This describes the legacy Function duration billing model based on wall-clock time. For new projects, we recommend Fluid Compute which bills separately for active CPU time and provisioned memory time for more cost-effective and transparent pricing.

You are charged based on the duration your Vercel functions have run. This is sometimes called "wall-clock time", which refers to the actual time elapsed during a process, similar to how you would measure time passing on a wall clock. It includes all time spent from start to finish of the process, regardless of whether that time was actively used for processing or spent waiting for a streamed response. Function Duration is calculated in GB-Hours, which is the memory allocated for each Function in GB x the time in hours they were running.

For example, if a function has 1.7 GB (1769 MB) of memory and is executed 1 million times at a 1-second duration:

To see your current usage, navigate to the Usage tab on your team's Dashboard and go to Serverless Functions > Duration. You can use the Ratio option to see the total amount of execution time across all projects within your team, including the completions, errors, and timeouts.

Recommended: Upgrade to Fluid compute

Legacy optimization strategies:

This counts the number of times that a request to your Functions could not be served because the concurrency limit was hit.

While this is not a chargeable metric, it will cause a error. To learn more, see What should I do if I receive a 503 error on Vercel?.

---

## Using WebAssembly (Wasm)

**URL:** https://vercel.com/docs/functions/runtimes/wasm

**Contents:**
- Using WebAssembly (Wasm)
- Using a Wasm file
  - Get your Wasm file ready
  - Create an API route for calling the Wasm file
  - Call the Wasm endpoint

WebAssembly, or Wasm, is a portable, low-level, assembly-like language that can be used as a compilation target for languages like C, Go, and Rust. Wasm was built to run more efficiently on the web and alongside JavaScript, so that it runs in most JavaScript virtual machines.

With Vercel, you can use Wasm in Vercel Functions or Routing Middleware when the runtime is set to , , or .

Pre-compiled WebAssembly can be imported with the suffix. This will provide an array of the Wasm data that can be instantiated using .

While is supported in Edge Runtime, it requires the Wasm source code to be provided using the import statement. This means you cannot use a buffer or byte array to dynamically compile the module at runtime.

You can use Wasm in your production deployment or locally, using .

With runtime that uses Fluid compute by default:

---

## Fluid compute pricing

**URL:** https://vercel.com/docs/functions/usage-and-pricing

**Contents:**
- Fluid compute pricing
  - Resource Details
    - Active CPU
    - Provisioned Memory
    - Invocations
- Regional pricing
- How pricing works
  - Example

Vercel Functions on fluid compute are priced based on your plan and resource usage. Each plan includes a set amount of resources per month:

Enterprise plans have custom terms. Speak to your Customer Success Manager (CSM) or Account Executive (AE) for details.

For example: If your function takes 100ms to process data but spends 400ms waiting for a database query, you're only billed for the 100ms of active CPU time. This means computationally intensive tasks (like image processing) will use more CPU time than I/O-heavy tasks (like making API calls).

For example: If you have a 1GB function instance running for 1 hour handling multiple requests, you're billed for 1 GB-hour of provisioned memory, regardless of how many requests it processed or how much of that hour was spent waiting for I/O.

For example: If your function receives 1.5 million requests on a Pro plan, you'll be billed for the 500,000 requests beyond your included million at $0.60 per million (approximately $0.30).

The following table shows the regional pricing for fluid compute resources on Vercel. The prices are per hour for CPU and per GB-hr for memory:

A function instance runs in a region, and its pricing is based on the resources it uses in that region. The cost for each invocation is calculated based on the Active CPU and Provisioned memory resources it uses in that region.

When the first request arrives, Vercel starts an instance with your configured memory. Provisioned memory is billed continuously until the last in-flight request finishes. Active CPU is billed only while your code is actually running. If the request is waiting on I/O, CPU billing pauses but memory billing continues.

After all requests complete, the instance is paused, and no CPU or memory charges apply until the next invocation. This means, you pay for memory whenever work is in progress, never for idle CPU, and nothing at all between requests.

Suppose you deploy a function with 4 GB of memory in the São Paulo, Brazil region, where the rates are $0.221/hour for CPU and $0.0183/GB-hour for memory. If one request takes 4 seconds of active CPU time and the instance is alive for 10 seconds (including I/O), the cost will be:

---

## Configuring Memory and CPU for Vercel Functions

**URL:** https://vercel.com/docs/functions/configuring-functions/memory

**Contents:**
- Configuring Memory and CPU for Vercel Functions
- Memory configuration considerations
- Setting your default function memory / CPU size
  - Memory / CPU type
- Viewing your function memory size
- Memory limits
- Pricing

The memory configuration of a function determines how much memory and CPU a function can use while executing. By default, on Pro and Enterprise, functions execute with 2 GB (1 vCPU) of memory. On Hobby, they will always execute with 2 GB (1 vCPU). You can change the default memory size for all functions in a project.

You should consider the following points when changing the memory size of your functions:

Those on the Pro or Enterprise plans can configure the default memory size for all functions in a project.

To change the default function memory size:

You cannot set your memory size using . If you try to do so, you will receive a warning at build time. Only Pro and Enterprise users can set the default memory size in the dashboard. Hobby users will always use the default memory size of 2 GB (1 vCPU).

The memory size you select will also determine the CPU allocated to your Vercel Functions. The following table shows the memory and CPU allocation for each type.

With fluid compute enabled on Pro and Enterprise plans, the default memory size is 2 GB (1 vCPU) and can be upgraded to 4 GB / 2 vCPUs, for Hobby users, Vercel manages the CPU with a minimum of 1 vCPU.

Users on the Hobby plan can only use the default memory size of 2 GB (1 vCPU). Hobby users cannot configure this size. If you are on the Hobby plan, and have enabled fluid compute, the memory size will be managed by Vercel with a minimum of 1 vCPU.

Project created before 2019-11-08 have the default function memory size set to 1024 MB/0.6 vCPU for Hobby plan, and 3008 MB/1.67 vCPU for Pro and Enterprise plan. Although the dashboard may not have any memory size option selected by default for those projects, you can start using the new memory size options by selecting your preferred memory size in the dashboard.

To check the memory size of your functions in the dashboard, follow these steps:

To learn more about the maximum size of your function's memory, see Max memory size.

While memory / CPU size is not an explicitly billed metric, it is fundamental in how the billed metric of Function Duration is calculated.

Legacy Billing Model: This describes the legacy Function duration billing model based on wall-clock time. For new projects, we recommend Fluid Compute which bills separately for active CPU time and provisioned memory time for more cost-effective and transparent pricing.

You are charged based on the duration your Vercel functions have run. This is sometimes called "wall-clock time", which refers to the actual time elapsed during a process, similar to how you would measure time passing on a wall clock. It includes all time spent from start to finish of the process, regardless of whether that time was actively used for processing or spent waiting for a streamed response. Function Duration is calculated in GB-Hours, which is the memory allocated for each Function in GB x the time in hours they were running.

For example, if a function has 1.7 GB (1769 MB) of memory and is executed 1 million times at a 1-second duration:

To see your current usage, navigate to the Usage tab on your team's Dashboard and go to Serverless Functions > Duration. You can use the Ratio option to see the total amount of execution time across all projects within your team, including the completions, errors, and timeouts.

You can also view Invocations to see the number of times your Functions have been invoked. To learn more about the cost of Vercel Functions, see Vercel Function Pricing.

---

## Vercel Function Logs

**URL:** https://vercel.com/docs/functions/logs

**Contents:**
- Vercel Function Logs
- Runtime Logs
  - Number of logs per request
  - Next.js logs

Vercel Functions allow you to debug and monitor your functions using runtime logs. Users on the Pro and Enterprise plans can use Vercel's support for Log Drains to collect and analyze your logs using third-party providers. Functions have full support for the API, including , , , and more.

You can view runtime logs for all Vercel Functions in real-time from the Logs tab of your project's dashboard. You can use the various filters and options to find specific log information. These logs are held for an amount of time based on your plan.

When your function is streaming, you'll get the following:

For more information, see Runtime Logs.

These changes in the frequency and format of logs will affect Log Drains. If you are using Log Drains we recommend ensuring that your ingestion can handle both the new format and frequency.

When a Function on a specific path receives a user request, you may see more than one log when the application renders or regenerates the page.

This can occur in the following situations:

In the case of ISR, multiple logs are the result of:

In Next.js projects, logged functions include API Routes (those defined in pages/api/**/*.ts or app/**/route.ts).

Pages that use SSR, such as those that call or export , will also be available both in the filter dropdown and the real time logs.

---

## Configuring Functions

**URL:** https://vercel.com/docs/functions/configuring-functions

**Contents:**
- Configuring Functions
- Runtime
- Region
- Maximum duration
- Memory

You can configure Vercel functions in many ways, including the runtime, region, maximum duration, and memory.

With different configurations, particularly the runtime configuration, there are a number of trade-offs and limits that you should be aware of. For more information, see the runtimes comparison.

The runtime you select for your function determines the infrastructure, APIs, and other abilities of your function.

With Vercel, you can configure the runtime of a function in any of the following ways:

See choosing a runtime for more information.

Your function should execute in a location close to your data source. This minimizes latency, or delay, thereby enhancing your app's performance. How you configure your function's region, depends on the runtime used.

See configuring a function's region for more information.

The maximum duration for your function defines how long a function can run for, allowing for more predictable billing.

Vercel Functions have a default duration that's dependent on your plan, but you can configure this as needed, up to your plan's limit.

See configuring a function's duration for more information.

Vercel Functions use an infrastructure that allows you to adjust the memory size.

See configuring a function's memory for more information.

---

## Streaming

**URL:** https://vercel.com/docs/functions/streaming-functions

**Contents:**
- Streaming
- Getting started
  - Prerequisites
- Function duration
- Streaming Python functions
- More resources

AI providers can be slow when producing responses, but many make their responses available in chunks as they're processed. Streaming enables you to show users those chunks of data as they arrive rather than waiting for the full response, improving the perceived speed of AI-powered apps.

Vercel recommends using Vercel's AI SDK to stream responses from LLMs and AI APIs. It reduces the boilerplate necessary for streaming responses from AI providers and allows you to change AI providers with a few lines of code, rather than rewriting your entire application.

The following example shows how to send a message to one of OpenAI's models and streams:

If your workload requires longer durations, you should consider enabling fluid compute, which has higher default max durations and limits across plans.

Maximum durations can be configured for Node.js functions to enable streaming responses for longer periods. See max durations for more information.

You can stream responses from Vercel Functions that use the Python runtime.

When your function is streaming, it will be able to take advantage of the extended runtime logs, which will show you the real-time output of your function, in addition to larger and more frequent log entries. Because of this potential increase in frequency and format, your Log Drains may be affected. We recommend ensuring that your ingestion can handle both the new format and frequency.

---

## Using the Python Runtime with Vercel Functions

**URL:** https://vercel.com/docs/functions/runtimes/python

**Contents:**
- Using the Python Runtime with Vercel Functions
- Python version
- Dependencies
- Streaming Python functions
- Controlling what gets bundled
- Using FastAPI with Vercel
- Using Flask with Vercel
- Other Python Frameworks
  - Reading Relative Files in Python
  - Web Server Gateway Interface

The Python runtime is available in Beta on all plans

The Python runtime enables you to write Python code, including using FastAPI, Django, and Flask, with Vercel Functions.

You can create your first function, available at the route, as follows:

The current available version is Python 3.12. This cannot be changed.

You can install dependencies for your Python projects by defining them in a with or without a corresponding , , or a with corresponding .

An example requirements.txt file that defines FastAPI as a dependency.

An example pyproject.toml file that defines FastAPI as a dependency.

Vercel Functions support streaming responses when using the Python runtime. This allows you to render parts of the UI as they become ready, letting users interact with your app before the entire page finishes loading.

By default, Python Vercel Functions include all files from your project that are reachable at build time. Unlike the Node.js runtime, there is no automatic tree-shaking to remove dead code or unused dependencies.

You should make sure your or only lists packages necessary for runtime and you should also explicitly exclude files you don't need in your functions to keep bundles small and avoid hitting size limits.

Python functions have a maximum uncompressed bundle size of 250 MB. See the bundle size limits.

To exclude unnecessary files (for example: tests, static assets, and test data), configure in under the key. The pattern is a glob relative to your project root.

Exclude common development and static folders from all Python functions to stay under the 250 MB bundle limit.

FastAPI is a modern, high-performance, web framework for building APIs with Python. For information on how to use FastAPI with Vercel, review this guide.

Flask is a lightweight WSGI web application framework. For information on how to use Flask with Vercel, review this guide.

For FastAPI, Flask, or basic usage of the Python runtime, no configuration is required. Usage of the Python runtime with other frameworks, including Django, requires some configuration.

The entry point of this runtime is a glob matching source files with one of the following variables defined:

Python uses the current working directory when a relative file is passed to open().

The current working directory is the base of your project, not the directory.

For example, the following directory structure:

With the above directory structure, your function in can read the contents of in a couple different ways.

You can use the path relative to the project's base directory.

Or you can use the path relative to the current file's directory.

The Web Server Gateway Interface (WSGI) is a calling convention for web servers to forward requests to web applications written in Python. You can use WSGI with frameworks such as Flask or Django.

The Asynchronous Server Gateway Interface (ASGI) is a calling convention for web servers to forward requests to asynchronous web applications written in Python. You can use ASGI with frameworks such as Sanic.

Instead of defining a , define an variable in your Python file.

For example, define a file as follows:

An example api/index.py file, using Sanic for a ASGI application.

An example requirements.txt file, listing sanic as a dependency.

---

## Query Reference

**URL:** https://vercel.com/docs/query/reference

**Contents:**
- Query Reference
- Metric
  - Aggregations
- Filter
- Group by
- Group by and where fields

The metric selects what query data is displayed. You can choose one field at a time, and the same metric can be applied to different event types. For instance, Function Wall Time can be selected for edge, serverless, or middleware functions, aggregating each field in various ways.

Metrics can be aggregated in the following ways:

Aggregations are calculated within each point on the chart (hourly, daily, etc) and also across the entire query window.

The filter bar defines the conditions to filter your query data. It only fetches data that meets a specified condition based on several fields and operators:

The clause calculates statistics for each combination of field values. Each group is displayed as a separate color in the chart view, and has a separate row in the table view.

For example, grouping by and will display data broken down by each combination of and .

There are several fields available for use within the Filter and group by:

---

## Using the Bun Runtime with Vercel Functions

**URL:** https://vercel.com/docs/functions/runtimes/bun

**Contents:**
- Using the Bun Runtime with Vercel Functions
- Configuring the runtime
- Framework-specific considerations
  - Next.js
  - Routing Middleware
- Feature support
- Supported APIs
- Using TypeScript with Bun
- Performance considerations
- When to use Bun

The Bun runtime is available in Beta on all plans

Bun is a fast, all-in-one JavaScript runtime that serves as an alternative to Node.js.

Bun provides Node.js API compatibility and is generally faster than Node.js for CPU-bound tasks. It includes a bundler, test runner, and package manager.

For all frameworks, including Next.js, you can configure the runtime in your file using the property.

Once you configure the runtime version, Vercel manages the Bun minor and patch versions automatically, meaning you only need to set the major version. Currently, is the only valid value.

Vercel manages the Bun minor and patch versions automatically. is the only valid value currently.

When using Next.js, and ISR, you must change your and commands in your package.json file to use the Bun runtime:

The Bun runtime works with Routing Middleware the same way as the Node.js runtime once you set the in your file. Note that you'll also have to set the runtime config to in your middleware.ts file.

The Bun runtime on Vercel supports most Node.js features. The main differences relate to automatic source maps, bytecode caching, and request metrics on the and modules. Request metrics using work with both runtimes.

See the table below for a detailed comparison:

Vercel Functions using the Bun runtime support most Node.js APIs, including standard Web APIs such as the Request and Response Objects.

Bun has built-in TypeScript support with zero configuration required. The runtime supports files ending with inside of the directory as TypeScript files to compile and serve when deploying.

Bun is generally faster than Node.js, especially for CPU-bound tasks. Performance varies by workload, and in some cases Node.js may be faster depending on the specific operations your function performs.

Bun is best suited for new workloads where you want a fast, all-in-one toolkit with built-in support for TypeScript, JSX, and modern JavaScript features. Consider using Bun when:

Consider using Node.js instead if:

Both runtimes run on Fluid compute and support the same core Vercel Functions features.

---

## Tracing

**URL:** https://vercel.com/docs/tracing

**Contents:**
- Tracing
- Automatic instrumentation
- Session tracing
- Using OpenTelemetry
- Viewing traces in the dashboard
  - Anatomy of a trace
- Exporting traces to a third party
  - Using custom OpenTelemetry setup with Sentry
- More resources

In observability, tracing is the process of collecting and analyzing how a request or operation flows through your application and through Vercel's infrastructure. Traces are used to explain how your application works, debug errors, and identify performance bottlenecks.

You can think of a trace as the story of a single request:

Request arrives at Vercel CDN -> Middleware executes -> Function handler processes request -> Database query runs -> Response returns to client

Each step in this process is a span. A span is a single unit of work in a trace. Spans are used to measure the performance of each step in the request and include a name, a start time, an end time, and a duration.

Vercel automatically instruments your application without needing any additional code changes. When you have set up Trace Drains or enabled Session Tracing for your Vercel Functions, you'll be able to visualize traces for:

For additional tracing, such as framework spans, you can install the @vercel/otel package to use the OpenTelemetry SDK. In addition, you can add custom spans to your traces to capture spans and gain more visibility into your application.

To visualize traces in your dashboard, you need to enable session tracing using the Vercel toolbar. Session tracing captures infrastructure, framework, and fetch spans for requests made during your individual session, making them available in the logs dashboard for debugging and performance monitoring.

You can initiate a session trace in two ways:

For detailed instructions on starting traces, managing active sessions, and viewing previous traces, see the Session Tracing documentation.

Vercel uses OpenTelemetry, an open standard for collecting traces from your application. In order to capture framework and custom spans, install the package. This package provides helper methods to make it easier to instrument your application with OpenTelemetry.

See the Instrumentation guide to set up OpenTelemetry for your project.

Once you have enabled session tracing, you can visualize traces in your dashboard:

Select your team from the scope selector and select your project.

Use the tracing icon in the filter bar to filter to traces. You can filter traces using all the same filters available in the Logs tab of the dashboard. To view traces for requests to your browser, press the user icon next to the Traces icon.

Find the request you want to view traces for and click the Trace button at the bottom of the request details panel. This will open the traces for that request:

When you view a trace in the dashboard, you see a timeline visualization of how a request flows through your application and Vercel's infrastructure. Each horizontal bar in the visualization is a span, which represents a single unit of work with a start time, end time, and duration.

When session tracing is enabled, your traces display the following types of spans:

To view details of a span, click on the span in the trace. The sidebar will display the span's details. For infrastructure spans, a "what is this?" explanation will be provided.

To view trace spans in more detail, click and drag to zoom in on a specific area of the trace. You can also use the zoom controls in the bottom right corner of the trace.

You can export traces to a third party observability provider using Vercel Drains. This can be done either by sending traces to a custom HTTP endpoint, or by using a native integration from the Vercel Marketplace.

See the Vercel Drains page to learn how to set up a Drain to export traces to a third party observability provider.

If you want to trace your Vercel application using while also using Sentry SDK v8+, you need to configure them to work together. The Sentry SDK automatically sets up OpenTelemetry by default, which can conflict with Vercel's OpenTelemetry setup and break trace propagation.

To use both together, configure Sentry to work with your custom OpenTelemetry setup by following the Sentry custom setup documentation.

Using Vercel OTel instead of Sentry: If you prefer to use Vercel's OpenTelemetry setup instead of Sentry's OTel instrumentation, add to your Sentry initialization in your file. This resolves conflicts between Vercel's OTel and Sentry v8+ that can prevent traces from reaching downstream providers.

---

## Open Graph (OG) Image Generation

**URL:** https://vercel.com/docs/og-image-generation

**Contents:**
- Open Graph (OG) Image Generation
- Benefits
- Supported features
- Runtime support
  - Runtime caveats
- Usage
  - Requirements
  - Getting started
  - Consume the OG route
- Examples

To assist with generating dynamic Open Graph (OG) images, you can use the Vercel library to compute and generate social card images using Vercel Functions.

Vercel OG image generation is supported on the Node.js runtime.

Local resources can be loaded directly using . Alternatively, can be used to load remote resources.

There are limitations when using with the Next.js Pages Router and the Node.js runtime. Specifically, this combination does not support the syntax. The table below provides a breakdown of the supported syntaxes for different configurations.

Get started with an example that generates an image from static text using Next.js by setting up a new app with the following command:

Then paste the following code:

If you're not using a framework, you must either add "type": "module" to your package.json or change your JavaScript Functions' file extensions from .js to .mjs

Run the following command:

Then, browse to . You will see the following image:

Deploy your project to obtain a publicly accessible path to the OG image API endpoint. You can find an example deployment at https://og-examples.vercel.sh/api/static.

Then, based on the Open Graph Protocol, create the web content for your social media post as follows:

With the example deployment at https://og-examples.vercel.sh/api/static, use the following code:

Every time you create a new social media post, you need to update the API endpoint with the new content. However, if you identify which parts of your will change for each post, you can then pass those values as parameters of the endpoint so that you can use the same endpoint for all your posts.

In the examples below, we explore using parameters and including other types of content with .

---

## Configuring the Runtime for Vercel Functions

**URL:** https://vercel.com/docs/functions/configuring-functions/runtime

**Contents:**
- Configuring the Runtime for Vercel Functions
- Node.js
- Go
- Python
- Ruby
- Other runtimes

The runtime of your function determines the environment in which your function will execute. Vercel supports various runtimes including Node.js, Python, Ruby, and Go. You can also configure other runtimes using the file. Here's how to set up each:

By default, a function with no additional configuration will be deployed as a Vercel Function on the Node.js runtime.

If you're not using a framework, you must either add "type": "module" to your package.json or change your JavaScript Functions' file extensions from .js to .mjs

For Go, expose a single HTTP handler from a file within an directory at your project's root. For example:

For Python, create a function by adding the following code to :

For Ruby, define an HTTP handler from files within an directory at your project's root. Ruby files must have one of the following variables defined:

Don't forget to define your dependencies inside a :

You can configure other runtimes by using the property in your file. For example:

In this case, the function at would use the custom runtime specified.

For more information, see Community runtimes

---

## Fluid compute

**URL:** https://vercel.com/docs/fluid-compute

**Contents:**
- Fluid compute
- Enabling fluid compute
  - Enable for entire project
  - Enable for specific environments and deployments
- Available runtime support
- Optimized concurrency
- Bytecode caching
- Isolation boundaries and global state
- Default settings by plan
- Order of settings precedence

Fluid compute offers a blend of serverless flexibility and server-like capabilities. Unlike traditional serverless architectures, which can face issues such as cold starts and limited functionalities, fluid compute provides a hybrid solution. It overcomes the limitations of both serverless and server-based approaches, delivering the advantages of both worlds, including:

See What is compute? to learn more about fluid compute and how it compares to traditional serverless models.

As of April 23, 2025, fluid compute is enabled by default for new projects.

You can enable fluid compute through the Vercel dashboard or by configuring your file for specific environments or deployments.

To enable fluid compute through the dashboard:

When you enable it through the dashboard, fluid compute applies to all deployments for that project by default.

You can programmatically enable fluid compute using the property in your file. This approach is particularly useful for:

Fluid compute is available for the following runtimes:

Fluid compute allows multiple invocations to share a single function instance, this is especially valuable for AI applications, where tasks like fetching embeddings, querying vector databases, or calling external APIs can be I/O-bound. By allowing concurrent execution within the same instance, you can reduce cold starts, minimize latency, and lower compute costs.

Vercel Functions prioritize existing idle resources before allocating new ones, reducing unnecessary compute usage. This in-function-concurrency is especially effective when multiple requests target the same function, leading to fewer total resources needed for the same workload.

Optimized concurrency in fluid compute is available when using Node.js or Python runtimes. See the efficient serverless Node.js with in-function concurrency blog post to learn more.

When using Node.js version 20+, Vercel Functions use bytecode caching to reduce cold start times. This stores the compiled bytecode of JavaScript files after their first execution, eliminating the need for recompilation during subsequent cold starts.

As a result, the first request isn't cached yet. However, subsequent requests benefit from the cached bytecode, enabling faster initialization. This optimization is especially beneficial for functions that are not invoked that often, as they will see faster cold starts and reduced latency for end users.

Bytecode caching is only applied to production environments, and is not available in development or preview deployments.

For frameworks that output ESM, all CommonJS dependencies (for example, , ) will be opted into bytecode caching.

On traditional serverless compute, the isolation boundary refers to the separation of individual instances of a function to ensure they don't interfere with each other. This provides a secure execution environment for each function.

However, because each function uses a microVM for isolation, which can lead to slower start-up times, you can see an increase in resource usage due to idle periods when the microVM remains inactive.

Fluid compute uses a different approach to isolation. Instead of using a microVM for each function invocation, multiple invocations can share the same physical instance (a global state/process) concurrently. This allows functions to share resources and execute in the same environment, which can improve performance and reduce costs.

When uncaught exceptions or unhandled rejections happen in Node.js, Fluid compute logs the error and lets current requests finish before stopping the process. This means one broken request won't crash other requests running on the same instance and you get the reliability of traditional serverless with the performance benefits of shared resources.

Fluid Compute includes default settings that vary by plan:

The settings you configure in your function code, dashboard, or file will override the default fluid compute settings.

The following order of precedence determines which settings take effect. Settings you define later in the sequence will always override those defined earlier:

See the fluid compute pricing documentation for details on how fluid compute is priced, including active CPU, provisioned memory, and invocations.

---

## Reserved environment variables

**URL:** https://vercel.com/docs/environment-variables/reserved-environment-variables

**Contents:**
- Reserved environment variables
- Allowed environment variables

The following environment variable names are reserved and therefore unavailable for use:

The following environment variable names are allowed by Vercel Vercel Function runtimes:

These variables may appear in your Vercel Functions even if you don't set them in your project explicitly. These values do not grant any AWS permissions and are not usable as AWS credentials. Configure your own AWS credentials using environment variables or set up OIDC.

---

## Integrate flags with Runtime Logs

**URL:** https://vercel.com/docs/feature-flags/integrate-with-runtime-logs

**Contents:**
- Integrate flags with Runtime Logs
- Limits

Runtime Logs integration is available in Beta on all plans

On your dashboard, the Logs tab displays your runtime logs. It can also display any feature flags your application evaluated while handling requests.

To make the runtime logs aware of your feature flag call with the flag name and value to be reported. Each call to will show up as a distinct entry, even when the same key is used:

If you are using an implementation of the Feature Flags pattern you don't need to call . The respective implementation will automatically call for you.

The following limits apply to reported values:

---

## Using the Node.js Runtime with Vercel Functions

**URL:** https://vercel.com/docs/functions/runtimes/node-js

**Contents:**
- Using the Node.js Runtime with Vercel Functions
- Creating a Node.js function
- Supported APIs
- Node.js version
- Node.js dependencies
- Using TypeScript with the Node.js runtime
- Node.js request and response objects
  - Node.js helpers
  - Request body
  - Cancelled Requests

You can create Vercel Function in JavaScript or TypeScript by using the Node.js runtime. By default, the runtime builds and serves any function created within the directory of a project to Vercel.

Node.js-powered functions are suited to computationally intense or large functions and provide benefits like:

In order to use the Node.js runtime, create a file inside the directory with a function using the Web Standard export. No additional configuration is needed:

Alternatively, you can export each HTTP method as a separate export instead of using the Web Standard export:

To learn more about creating Vercel Functions, see the Functions API Reference. If you need more advanced behavior, such as a custom build step or private npm modules, see the advanced Node.js usage page.

The entry point for must be a glob matching , , or files** that export a default function.

Vercel Functions using the Node.js runtime support all Node.js APIs, including standard Web APIs such as the Request and Response Objects.

To learn more about the supported Node.js versions on Vercel, see Supported Node.js Versions.

For dependencies listed in a file at the root of a project, the following behavior is used:

If you need to select a specific version of a package manager, see corepack.

The Node.js runtime supports files ending with inside of the directory as TypeScript files to compile and serve when deploying.

An example TypeScript file that exports a Web signature handler is as follows:

You can use a file at the root of your project to configure the TypeScript compiler. Most options are supported aside from "Path Mappings" and "Project References".

Each request to a Node.js Vercel Function gives access to Request and Response objects. These objects are the standard HTTP Request and Response objects from Node.js.

Vercel additionally provides helper methods inside of the Request and Response objects passed to Node.js Vercel Functions. These methods are:

The following Node.js Vercel Function example showcases the use of , and helpers:

Example Node.js Vercel Function using the , , and helpers. It returns greetings for the user specified using .

If needed, you can opt-out of Vercel providing using advanced configuration.

We populate the property with a parsed version of the content sent with the request when possible.

We follow a set of rules on the header sent by the request to do so:

With the helper, you can build applications without extra dependencies or having to parse the content of the request manually.

The helper is set using a JavaScript getter. In turn, it is only computed when it is accessed.

When the request body contains malformed JSON, accessing will throw an error. You can catch that error by wrapping with :

Catching the error thrown by with .

Request cancellation must be enabled on a per-route basis. See Functions API Reference for more information.

You can listen for the event on the request object to detect request cancellation:

Express.js is a popular framework used with Node.js. For information on how to use Express with Vercel, see the guide: Using Express.js with Vercel.

The Node.js runtime can be used as an experimental feature to run middleware. To enable, add the flag to your file:

Then in your middleware file, set the runtime to in the object:

Running middleware on the Node.js runtime incurs charges under Vercel Functions pricing. These functions only run using Fluid compute.

---

## Vercel Functions

**URL:** https://vercel.com/docs/functions

**Contents:**
- Vercel Functions
- Getting started
- Functions lifecycle
  - Functions and your data source
- Viewing Vercel Function metrics
- Pricing
- Related

Vercel Functions lets you run server-side code without managing servers. They adapt automatically to user demand, handle connections to APIs and databases, and offer enhanced concurrency through fluid compute, which is useful for AI workloads or any I/O-bound tasks that require efficient scaling

When you deploy your application, Vercel automatically sets up the tools and optimizations for your chosen framework. It ensures low latency by routing traffic through Vercel's CDN, and placing your functions in a specific region when you need more control over data locality.

To get started with creating your first function, copy the code below:

While using is the recommended way to create a Vercel Function, you can still use HTTP methods like and .

To learn more, see the quickstart or deploy a template.

Vercel Functions run in a single region by default, although you can configure them to run in multiple regions if you have globally replicated data. These functions let you add extra capabilities to your application, such as handling authentication, streaming data, or querying databases.

When a user sends a request to your site, Vercel can automatically run a function based on your application code. You do not need to manage servers, or handle scaling.

Vercel creates a new function invocation for each incoming request. If another request arrives soon after the previous one, Vercel reuses the same function instance to optimize performance and cost efficiency. Over time, Vercel only keeps as many active functions as needed to handle your traffic. Vercel scales your functions down to zero when there are no incoming requests.

By allowing concurrent execution within the same instance (and so using idle time for compute), fluid compute reduces cold starts, lowers latency, and saves on compute costs. It also prevents the need to spin up multiple isolated instances when tasks spend most of their time waiting for external operations.

Functions should always execute close to where your data source is to reduce latency. By default, functions using the Node.js runtime execute in Washington, D.C., USA (), a common location for external data sources. You can set a new region through your project's settings on Vercel.

You can view various performance and cost efficiency metrics using Vercel Observability:

From here, you'll be able to see total consumed and saved GB-Hours, and the ratio of the saved usage. When you have fluid enabled, you will also see the amount of cost savings from the optimized concurrency model.

Vercel Functions are priced based on active CPU, provisioned memory, and invocations. See the fluid compute pricing documentation for more information.

If your project is not using fluid compute, see the legacy pricing documentation for Vercel Functions.

---

## Incremental Static Regeneration usage and pricing

**URL:** https://vercel.com/docs/incremental-static-regeneration/limits-and-pricing

**Contents:**
- Incremental Static Regeneration usage and pricing
- Pricing
- Usage
  - Storage
  - Written data
  - Read data
- ISR reads and writes price
  - ISR cache region
- Optimizing ISR reads and writes
- ISR reads chart

Vercel offers several methods for caching data within Vercel’s managed infrastructure. Incremental Static Regeneration (ISR) caches your data at the edge and persists it to durable storage – data reads and writes from durable storage will incur costs.

ISR Reads and Writes are priced regionally based on the Vercel function region(s) set at your project level. See the regional pricing documentation and ISR cache region for more information.

The table below shows the metrics for the ISR section of the Usage dashboard.

To view information on managing each resource, select the resource link in the Metric column. To jump straight to guidance on optimization, select the corresponding resource link in the Optimize column. The cost for each metric is based on the request location, see the pricing section and choose the region from the dropdown for specific information.

There is no limit on storage for ISR, all the data you write remains cached for the duration you specify. Only you or your team can invalidate this cache—unless it goes unaccessed for 31 days.

The total amount of Write Units used to durably store new ISR data, measured in 8KB units.

The total amount of Read Units used to access the ISR data, measured in 8KB units.

ISR reads and writes are measured in 8 KB units:

ISR Reads and Writes are priced regionally based on the Vercel function region(s) set at your project level. See the regional pricing documentation and ISR cache region for more information.

The ISR cache region for your deployment is set at build time and is based on the default Function region set at your project level. If you have multiple regions set, the region that will give you the best cost optimization is selected. For example, if (Washington, D.C., USA) is one of your regions, it is always selected.

For best performance, set your default Function region (and hence your ISR cache region) to be close to where your users are. Although this may affect your ISR costs, automatic compression of ISR writes will keep your costs down.

You are charged based on the volume of data read from and written to the ISR cache, and the regions where reads and writes occur. To optimize ISR usage, consider the following strategies.

When attempting to perform a revalidation, if the content has no changes from the previous version, no ISR write units will be incurred. This applies to be time-based ISR as well as on-demand revalidation.

If you are seeing writes, this is because the content has changed. Here's how you can debug unexpected writes:

You get charged based on the amount of data read from your ISR cache and the region(s) in which the reads happen.

When viewing your ISR read units chart, you can group by:

You get charged based on the amount of ISR write units written to your ISR cache and the region(s) in which the writes happen.

When viewing your ISR writes chart, you can group by sum of units to see a total of all writes across your team's projects.

---

## vercel project

**URL:** https://vercel.com/docs/cli/project

**Contents:**
- vercel project
- Usage
- Global Options

The command is used to manage your Vercel Projects, providing functionality to list, add, and remove.

Using the vercel project command to list all Vercel Project.

Using the vercel project command to list all Vercel Project that are affected by an upcoming Node.js runtime deprecation.

Using the vercel project command to create a new Vercel Project.

Using the vercel project command to remove a Vercel Project.

The following global options can be passed when using the vercel project command:

For more information on global options and their usage, refer to the options section.

---

## Configuring regions for Vercel Functions

**URL:** https://vercel.com/docs/functions/configuring-functions/region

**Contents:**
- Configuring regions for Vercel Functions
- Setting your default region
  - Dashboard
  - Project configuration
  - Vercel CLI
- Available regions
- Automatic failover
  - Node.js runtime failover

The Vercel platform caches all static content at the edge by default. This means your users will always get static files like HTML, CSS, and JavaScript served from servers that are closest to them. See the regions page for a full list of our regions.

In a globally distributed application, the physical distance between your function and its data source can impact latency and response times. Therefore, Vercel allows you to specify the region in which your functions execute, ideally close to your data source (such as your database).

The default Function region is Washington, D.C., USA () for all new projects.

To change the default regions in the dashboard:

Choose the appropriate project from your dashboard on Vercel

Navigate to the Settings tab

From the left side, select Functions

Use the Function Regions accordion to select your project's default regions:

To change the default region in your configuration file, add the region code(s) to the key:

Additionally, Pro and Enterprise users can deploy Vercel Functions to multiple regions: Pro users can deploy to up to three regions, and Enterprise users can deploy to unlimited regions. To learn more, see location limits.

Enterprise users can also use to specify regions that a Vercel Function should failover to if the default region is out of service.

Use the command in your project's root directory to set a region. Learn more about setting regions with the command in the CLI docs.

To learn more about the regions that you can set for your Functions, see the region list.

Vercel Functions have multiple availability zone redundancy by default. Multi-region redundancy is available depending on your runtime.

Setting failover regions are available on Enterprise plans

Enterprise teams can enable multi-region redundancy for Vercel Functions using Node.js.

To automatically failover to closest region in the event of an outage:

Select your project from your team's dashboard

Navigate to the Settings tab and select Functions

Enable the Function Failover toggle:

To manually specify the fallback region, you can pass one or more regions to the property in your file:

The region(s) set in the property must be different from the default region(s) specified in the property.

During an automatic failover, Vercel will reroute application traffic to the next closest region, meaning the order of the regions in does not matter. For more information on how failover routing works, see .

You can view your default and failover regions through the deployment summary:

Region failover is supported with Secure Compute. See Region Failover to learn more.

---

## Advanced Node.js Usage

**URL:** https://vercel.com/docs/functions/runtimes/node-js/advanced-node-configuration

**Contents:**
- Advanced Node.js Usage
  - Disabling helpers for Node.js
  - Private npm modules for Node.js
  - Custom build step for Node.js
  - Experimental Node.js require() of ES Module

To use Node.js, create a file inside your project's directory. No additional configuration is needed.

The entry point for must be a glob matching , , or files that export a default function.

For more information, see Environment Variables.

To install private npm modules:

For more information, see Environment Variables.

In some cases, you may wish to include build outputs inside your Vercel Function. To do this:

By default, we disable experimental support for requiring ES Modules. You can enable it by setting the following Environment Variable in your project settings:

---

## Edge Runtime

**URL:** https://vercel.com/docs/functions/runtimes/edge

**Contents:**
- Edge Runtime
- Region
  - Setting regions in your function
- Failover mode
- Maximum duration
- Concurrency
- Edge Runtime supported APIs
  - Supported APIs
  - Network APIs
  - Encoding APIs

We recommend migrating from edge to Node.js for improved performance and reliability. Both runtimes run on Fluid compute with Active CPU pricing.

To convert your Vercel Function to use the Edge runtime, add the following code to your function:

If you're not using a framework, you must either add "type": "module" to your package.json or change your JavaScript Functions' file extensions from .js to .mjs

By default, Vercel Functions using the Edge runtime execute in the region closest to the incoming request. You can set one or more preferred regions using the route segment config or specify a key within a config object to set one or more regions for your functions to execute in.

If your function depends on a data source, you may want it to be close to that source for fast responses.

To configure which region (or multiple regions) you want your function to execute in, pass the ID of your preferred region(s) in the following way:

If you're not using a framework, you must either add "type": "module" to your package.json or change your JavaScript Functions' file extensions from .js to .mjs

In the event of regional downtime, Vercel will automatically reroute traffic to the next closest CDN region on all plans. For more information on which regions Vercel routes traffic to, see Outage Resiliency.

Vercel Functions using the Edge runtime must begin sending a response within 25 seconds to maintain streaming capabilities beyond this period, and can continue streaming data for up to 300 seconds.

Vercel automatically scales your functions to handle traffic surges, ensuring optimal performance during increased loads. For more information, see Concurrency scaling.

The Edge runtime is built on top of the V8 engine, allowing it to run in isolated execution environments that don't require a container or virtual machine.

The Edge runtime provides a subset of Web APIs such as , , and .

The following tables list the APIs that are available in the Edge runtime.

You can check if your function is running on the Edge runtime by checking the global property. This can be helpful if you need to validate that your function is running on the Edge runtime in tests, or if you need to use a different API depending on the runtime.

The following modules can be imported with and without the prefix when using the statement:

Also, is globally exposed to maximize compatibility with existing Node.js modules.

The Edge runtime has some restrictions including:

The following JavaScript language features are disabled, and will not work:

While is supported in Edge Runtime, it requires the Wasm source code to be provided using the import statement. This means you cannot use a buffer or byte array to dynamically compile the module at runtime.

You can use to access Environment Variables.

Middleware with the runtime configured is neither a Node.js nor browser application, which means it doesn't have access to all browser and Node.js APIs. Currently, our runtime offers a subset of browser APIs and some Node.js APIs and we plan to implement more functionality in the future.

Dynamic code execution is not available in Middleware with the runtime configured for security reasons. For example, the following APIs cannot be used:

You need to make sure libraries used in your Middleware with the runtime configured don't rely on dynamic code execution because it leads to a runtime error.

Middleware with the runtime configured must begin sending a response within 25 seconds.

You may continue streaming a response beyond that time and you can continue with asynchronous workloads in the background, after returning the response.

The maximum size for an Vercel Function using the Edge runtime includes your JavaScript code, imported libraries and files (such as fonts), and all files bundled in the function.

If you reach the limit, make sure the code you are importing in your function is used and is not too heavy. You can use a package size checker tool like bundle to check the size of a package and search for a smaller alternative.

Environment Variables can be accessed through the object. Since JavaScript objects have methods to allow some operations on them, there are limitations on the names of Environment Variables to avoid having ambiguous code.

The following names will be ignored as Environment Variables to avoid overriding the object prototype:

Therefore, your code will always be able to use them with their expected behavior:

---

## Functions API Reference

**URL:** https://vercel.com/docs/functions/functions-api-reference

**Contents:**
- Functions API Reference
- Function signature
  - Cancel requests
- signal
- The package
  - Helper methods
- The package
  - OIDC Helper methods
- The package
  - AWS Helper methods

Vercel Functions use a Web Handler, which consists of the parameter that is an instance of the web standard API. Next.js extends the standard object with additional properties and methods.

Cancelling requests is useful for cleaning up resources or stopping long-running tasks when the client aborts the request — for example, when a user hits stop on an AI chat or they close a browser tab.

To cancel requests in Vercel Functions

In your file, add to the specific paths you want to opt-in to cancellation for your functions. For example, to enable everything, use as the glob or for app router:

When you have enabled cancellation, anything that must be completed in the event of request cancellation should be put in a or promise. If you don't, there is no guarantee that code will be executed after the request is cancelled.

Use the API in your function to cancel the request. This will allow you to clean up resources or stop long-running tasks when the client aborts the request:

A signal is sent to a function when it is about to be terminated, such as during scale-down events. This allows you to perform any necessary cleanup operations before the function instance is terminated.

Your code can run for up to 500 milliseconds after receiving a signal. After this period, the function instance will be terminated immediately.

The package provides a set of helper methods and utilities for working with Vercel Functions.

See the documentation for more information.

The package was previously provided by .

The package provides helper methods and utilities for working with OpenID Connect (OIDC) tokens.

See the documentation for more information.

The package was previously provided by .

The package provides helper methods and utilities for working with OpenID Connect (OIDC) tokens and AWS credentials.

See the documentation for more information.

---
