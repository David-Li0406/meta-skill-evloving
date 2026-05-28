# Vercel - Deployments

**Pages:** 127

---

## Create React App on Vercel

**URL:** https://vercel.com/docs/frameworks/frontend/create-react-app

**Contents:**
- Create React App on Vercel
- Get Started with CRA on Vercel
- Deploy a new CRA project with a template
- Static file caching
- Preview Deployments
  - Comments
- Web Analytics
- Speed Insights
- Observability
- More benefits

Create React App (CRA) is a development environment for building single-page applications with the React framework. It sets up and configures a new React project with the latest JavaScript features, and optimizes your app for production.

To get started with CRA on Vercel:

Get started in minutes

A client-side React app created with create-react-app.

React application that implements user login, logout and sign-up features using Auth0.

Vercel deployments can integrate with your git provider to generate preview URLs for each pull request you make to your CRA project.

On Vercel, static files are replicated and deployed to every region in our global CDN after the first request. This ensures that static files are served from the closest location to the visitor, improving performance and reducing latency.

Static files are cached for up to 31 days. If a file is unchanged, it can persist across deployments, as their hash caches static files. However, the cache is effectively invalidated when you redeploy, so we always serve the latest version.

To summarize, using Static Files with CRA on Vercel:

Learn more about static files caching

When you deploy your CRA app to Vercel and connect your git repo, every pull request will generate a Preview Deployment.

Preview Deployments allow you to preview changes to your app in a live deployment. They are available by default for all projects, and are generated when you commit changes to a Git branch with an open pull request, or you create a deployment using Vercel CLI.

You can use the comments feature to receive feedback on your Preview Deployments from Vercel Team members and people you share the Preview URL with.

Comments allow you to start discussion threads, share screenshots, send notifications, and more.

To summarize, Preview Deployments with CRA on Vercel:

Learn more about Preview Deployments

Vercel's Web Analytics features enable you to visualize and monitor your application's performance over time. The Analytics tab in your project's dashboard offers detailed insights into your website's visitors, with metrics like top pages, top referrers, and user demographics.

To use Web Analytics, navigate to the Analytics tab of your project dashboard on Vercel and select Enable in the modal that appears.

To track visitors and page views, we recommend first installing our package.

You can then import the function from the package, which will add the tracking script to your app. This should only be called once in your app.

Add the following code to your main app file:

Then, ensure you've enabled Web Analytics in your dashboard on Vercel. You should start seeing usage data in your Vercel dashboard.

To summarize, using Web Analytics with CRA on Vercel:

Learn more about Web Analytics

You can see data about your CRA project's Core Web Vitals performance in your dashboard on Vercel. Doing so will allow you to track your web application's loading speed, responsiveness, and visual stability so you can improve the overall user experience.

On Vercel, you can track your app's Core Web Vitals in your project's dashboard by enabling Speed Insights.

To summarize, using Speed Insights with CRA on Vercel:

Learn more about Speed Insights

Vercel's observability features help you monitor, analyze, and manage your projects. From your project's dashboard on Vercel, you can track website usage and performance, record team members' activities, and visualize real-time data from logs.

Activity Logs, which you can see in the Activity tab of your project dashboard, are available on all account plans. The following observability products are available for Enterprise teams:

For Pro (and Enterprise) accounts:

To summarize, using Vercel's observability features with CRA enable you to:

Learn more about Observability

See our Frameworks documentation page to learn about the benefits available to all frameworks when you deploy on Vercel.

Learn more about deploying CRA projects on Vercel with the following resources:

---

## System environment variables

**URL:** https://vercel.com/docs/environment-variables/system-environment-variables

**Contents:**
- System environment variables
- Automatically expose system environment variables
- System environment variables
  - VERCEL
  - CI
  - VERCEL_ENV
  - VERCEL_TARGET_ENV
  - VERCEL_URL
  - VERCEL_BRANCH_URL
  - VERCEL_PROJECT_PRODUCTION_URL

Vercel provides a set of environment variables that are automatically populated by the system, such as the URL of the deployment or the name of the Git branch deployed.

To expose these environment variables to your deployments:

If you disable this setting, no deployment ID will be made available for supported frameworks (like Next.js) to use, which means Skew Protection will also be disabled.

If you are using a framework for your project, Vercel provides the following prefixed environment variables:

When you choose to automatically expose system environment variables, some React warnings, such as those in a will display as build errors. For more information on this error, see How do I resolve a error?

Available at:Both build and runtime

An indicator to show that system environment variables have been exposed to your project's Deployments.

Available at:Build time

An indicator that the code is running in a Continuous Integration environment.

Available at:Both build and runtime

The environment that the app is deployed and running on. The value can be either production, preview, or development.

Available at:Both build and runtime

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

Available at:Both build and runtime

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

Available at:Both build and runtime

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

Available at:Both build and runtime

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The ID of the Region where the app is running.

Available at:Both build and runtime

The unique identifier for the deployment, which can be used to implement Skew Protection.

Available at:Both build and runtime

The unique identifier for the project.

Available at:Both build and runtime

When Skew Protection is enabled in Project Settings, this value is set to 1.

Available at:Both build and runtime

The Protection Bypass for Automation value, if the secret has been generated in the project's Deployment Protection settings.

Available at:Build time

When Secure Backend Access with OpenID Connect (OIDC) Federation is enabled in Project Settings, this value is set to a Vercel-issued OIDC token. At runtime, the token is set to thex-vercel-oidc-token header on your functions' Request object. In local development, you can download the token using the CLI commandvercel env pull.

Available at:Both build and runtime

The Git Provider the deployment is triggered from.

Available at:Both build and runtime

The origin repository the deployment is triggered from.

Available at:Both build and runtime

The account that owns the repository the deployment is triggered from.

Available at:Both build and runtime

The ID of the repository the deployment is triggered from.

Available at:Both build and runtime

The git branch of the commit the deployment was triggered by.

Available at:Both build and runtime

The git SHA of the commit the deployment was triggered by.

Available at:Both build and runtime

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

Available at:Both build and runtime

The username attached to the author of the commit that the project was deployed by.

Available at:Both build and runtime

The name attached to the author of the commit that the project was deployed by.

Available at:Build time

The git SHA of the last successful deployment for the project and branch.

Available at:Both build and runtime

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

**Examples:**

Example 1 (bash):
```bash
VERCEL_ENV=production
```

Example 2 (bash):
```bash
VERCEL_ENV=production
```

Example 3 (bash):
```bash
VERCEL_TARGET_ENV=production
```

Example 4 (bash):
```bash
VERCEL_TARGET_ENV=production
```

---

## Managing Comments on Preview Deployments

**URL:** https://vercel.com/docs/comments/managing-comments

**Contents:**
- Managing Comments on Preview Deployments
- Resolve comments
- Notifications
  - Customizing notifications for deployments
  - Customizing thread notifications
  - Dashboard notifications
  - Email
  - Slack
- Troubleshooting comments

You can resolve comments by selecting the ☐ Resolve checkbox that appears under each thread or comment. You can access this checkbox by selecting a comment wherever it appears on the page, or by selecting the thread associated with the comment in the Inbox.

Participants in a thread will receive a notification when that thread is resolved.

By default, the activity within a comment thread triggers a notification for all participants in the thread. PR owners will also receive notifications for all newly-created comment threads.

Activities that trigger a notification include:

Whenever there's new activity within a comment thread, you'll receive a new notification. Notifications can be sent to:

To customize notifications for a deployment:

You can manage notifications for threads in the Inbox:

While logged into Vercel, select the notification bell icon and select the Comments tab to see new Comments notifications. To view specific comments, you can:

Comments left on pages with query params in the URL may not appear on the page when you visit the base URL. Filter by page and search with a wildcard to see all pages with similar URLs. For example, you might search for .

You can also resolve comments from your notifications.

To reply to a comment, or view the deployment it was made on, select it and select the link to the deployment.

Email notifications will be sent to the email address associated with your Vercel account. Multiple notifications within a short period will be batched into a single email.

When you configure Vercel's Slack integration, comment threads on linked branches will create Slack threads. New activity on Slack or in the comment thread will be reflected on both platforms. See our Slack integration docs to learn more.

Sometimes, issues appear on a webpage for certain browsers and devices, but not for others. It's also possible for users to leave comments on a preview while viewing an outdated deployment.

To get around this issue, you can select the screen icon beside a commenter's name to copy their session info to your clipboard. Doing so will yield a JSON object similar to the following:

On desktop, you can hover your cursor over a comment's timestamp to view less detailed session information at a glance, including:

---

## Trace Drains Reference

**URL:** https://vercel.com/docs/drains/reference/traces

**Contents:**
- Trace Drains Reference
- Traces Schema
- Format
  - JSON
  - Protobuf
- Sampling Rate
- Limitations
- More resources

Trace Drains forward distributed tracing data from your deployments to external endpoints for storage and analysis. You can configure Trace Drains in two ways:

Vercel sends traces to endpoints over HTTPS following the OpenTelemetry Protocol (OTLP) specification.

Trace Drains follow the OpenTelemetry traces specification. Vercel automatically adds these specific resource attributes to all traces:

Vercel supports the following formats for Trace Drains. You can configure the format when configuring the Drain destination:

Vercel sends traces as JSON objects following the OpenTelemetry specification:

Vercel sends traces in binary protobuf format following the OTLP/HTTP specification. This format is more efficient for high-volume trace data transmission.

Sampling rules control how much trace data each drain forwards so you can manage observability depth and spend. Add sampling rules to define how much data reaches your destination:

Rules run from top to bottom. Requests that match a rule use that rule’s sampling rate, and any other requests are dropped. If you do not add rules, the drain forwards 100% of data to the destination.

Custom spans from functions using the Edge runtime are not forwarded via the Trace Drain.

For more information on Trace Drains and how to use them, check out the following resources:

---

## Troubleshooting Build Errors

**URL:** https://vercel.com/docs/deployments/troubleshoot-a-build

**Contents:**
- Troubleshooting Build Errors
- Troubleshooting views
- Troubleshoot Build failures
  - Investigating Build logs
  - Build Logs not available
- Cancelled Builds due to limits
  - Build container resources
  - Build duration
  - Caching
- Other Build errors

You can troubleshoot build errors that occur during the Build step of your deployment to Vercel. This guide will help you understand how to investigate build failures and long build times.

You can use the following views on your dashboard to troubleshoot a build:

You can navigate to these views from the Deployment page by clicking on the Source tab, the Resources tab or the Build Logs accordion as shown below.

If your build fails, Vercel will report the error message on the Deployments page so that you can investigate and fix the underlying issue.

In the following we show you how to look up the error message of your failed build.

Build logs provide you with an insight into what happened during the build of a deployment and can be accessed by:

On the errored deployment's page, you will see a summary of the error in the preview section. In the Deployment Details section, expand the Building accordion to expand the logs. There are situations where build logs are not available, in this scenario the error will be presented in the UI instead.

Scroll down in the build logs until you find a red section where the keyword "Error" is mentioned. It can be mentioned once or multiple times. In many cases, the last mention is not indicative like in the example below where it says . If you look a few lines above, you will see an additional error which in this case indicates where the problem is with a link for more details. Sometimes, an error may not be mentioned in the lines above but the output will often help you identify where the problem is.

It is recommended to build your project on your local machine first (the build command varies per project) before deploying on Vercel. This will catch issues specific to your code or to your project's dependencies. In the example above, when the command (that runs ) is run in the local console for a Next.js project, the error happens after building locally.

Builds can fail without providing any build logs when Vercel detects a missing precondition that prevents a build from starting. For example:

In this case, you cannot access the Building accordion described above, and instead, Vercel will present an overlay that contains the error message.

Sometimes, your Deployment Build can hit platform limits so that the build will be cancelled and throw a corresponding error that will be shown in the Build logs. Review the limits below in case you run into them.

Every Build is provided with the following resources:

For Hobby customers, these limits are fixed. Pro and Enterprise customers can purchase Enhanced or Turbo build machines with extra CPUs, larger memory, and storage. Exceeding the memory or disk space allocations limits cancels the build and triggers a system report in your Build logs, identifying memory and disk space issues.

By default, the system generates this report only when it detects a problem. To receive a report for every deployment, set as an environment variable.

This report helps you detect hidden Out of Memory (OOM) events, and provides insights into disk usage by breaking down the sizes of your source code, , and output, and flagging files over 100 MB. The input size in the report corresponds to the size of your checked-out repository or files uploaded by CLI. The size represents the total size of all folders on disk.

Review the below steps to help navigate this situation:

The total build duration is shown on the Vercel Dashboard and includes all three steps: building, checking, and assigning domains. Each step also shows the individual duration.

A Build can last for a maximum of 45 minutes. If the build exceeds this time, the deployment will be canceled and the error will be shown on the Deployment's Build logs. If you run into this limit, review this guide that explains how to reduce the Build time with a Next.js Project.

The maximum size of the Build's cache is 1 GB. It is retained for one month and it applies at the level of each Build cache key.

It is not possible to manually configure which files are cached at this time.

You may come across the following Build-specific errors when deploying your Project. The link for each error provides possible causes of the error that can help you troubleshoot.

A 'module not found' error is a syntax error that will appear at build time. This error appears when the static import statement cannot find the file at the declared path. For more information, see How do I resolve a 'module not found' error?

The first Build in a Project will take longer as the Build cache is initially empty. Subsequent builds that have the same Build cache key will take less time because elements from your build, such as framework files and node modules, will be reused from the available cache. The next sections will describe the factors that affect the Build cache to help you decrease the Build time

Vercel caches files based on the Framework Preset selected in your Project settings. The following files are cached in addition to :

Note that the framework detection is dependent on the preset selection made in the Build settings. You should make sure that the correct framework is set for your project for optimum build caching.

At the beginning of each build, the previous Build's cache is restored prior to the Install Command or Build command executing. Each deployment is associated with a unique Build cache key that is derived from the combination of the following data:

Let's say that under your account , you have a project that is connected to your Git repository on the branch for the production environment. When you make a commit to the branch for the first time, you trigger a build that creates a production deployment with a new unique cache key. For any new commits to the branch of , the existing Build cache is used as long as is under .

If you create a new Git branch in and make a commit to it, there is no cache for that specific branch. In this case, the last production Deployment cache is used to create a preview deployment and a new branch cache is created for subsequent commits to the new branch.

If you use Vercel functions to process HTTP requests in your project, each Vercel Function is built separately in the Build step and has its own cache, based on the Runtime used. Therefore, the number and size of Vercel functions will affect your Build time. For Next.js projects, Vercel functions are bundled to optimize Build resources as described here.

At the end of each Build step, successful builds will update the cache and failed builds will not modify the existing cache.

Since development dependencies (for example, packages such as or ) are not needed in production, you may want to prevent them from being installed when deploying to Vercel to reduce the Build time. To skip development dependencies, customize the Install Command to be or .

Sometimes, you may not want to use the Build cache for a specific deployment. You can invalidate or delete the existing Build cache in the following ways:

When redeploying without the existing Build Cache, the Remote Cache from Turborepo and Nx are automatically excluded.

---

## Response headers

**URL:** https://vercel.com/docs/headers/response-headers

**Contents:**
- Response headers

The following headers are included in Vercel deployment responses and indicate certain factors of the environment. These headers can be viewed from the Browser's Dev Tools or using an HTTP client such as .

Used to specify directives for caching mechanisms in both the Network layer cache and the browser cache. See the Cache Control Headers section for more detail.

If you use this header to instruct the CDN to cache data, such as with the directive, Vercel returns the following header to the client:

An integer that indicates the number of bytes in the response.

The media type that describes the nature and format of the response.

A timestamp indicating when the response was generated.

Shows where the request came from. This header can be overridden by other proxies (e.g., Cloudflare).

A header often abbreviated as HSTS that tells browsers that the resource should only be requested over HTTPS. The default value is (2 years)

We add this header automatically with a value of to prevent search engines from crawling your Preview Deployments and outdated Production Deployments, which could cause them to penalize your site for duplicate content.

You can prevent this header from being added to your Preview Deployment by:

The header is primarily used to indicate the cache status of static assets and responses from Vercel's CDN. For dynamic routes and fetch requests that utilize the Vercel Data Cache, this header will often show even if the data is being served from the Data Cache. Use custom headers or runtime logs to determine if a fetch response was served from the Data Cache.

The following values are possible when the content being served is static or uses a Cache-Control header:

The response was not found in the cache and was fetched from the origin server.

The response was served from the cache.

The response was served from the cache but the content is no longer fresh, so a background request to the origin server was made to update the content.

Cached content can go stale for several different reasons such as:

See purging the cache for more information.

The response was served from static storage. An example of prerender is in , when setting in . However, will not return prerender.

The response was served from the origin server after the cache was deleted so it must be revalidated in the foreground.

The cached content can be deleted in several ways such as:

See purging the cache for more information.

This header contains a list of Vercel regions your request hit, as well as the region the function was executed in (for both Edge and Serverless).

It also allows Vercel to automatically prevent infinite loops.

---

## vercel remove

**URL:** https://vercel.com/docs/cli/remove

**Contents:**
- vercel remove
- Usage
- Extended Usage
- Unique Options
  - Safe
  - Yes
- Global Options

The command, which can be shortened to , is used to remove deployments either by ID or for a specific Vercel Project.

You can also remove deployments from the Project Overview page on the Vercel Dashboard.

Using the vercel remove command to remove a deployment from the Vercel platform.

Using the vercel remove command to remove multiple deployments from the Vercel platform.

Using the vercel remove command to remove all deployments for a Vercel Project from the Vercel platform.

By using the project name, the entire Vercel Project will be removed from the current scope unless the --safe is used.

These are options that only apply to the command.

The option, shorthand , can be used to skip the removal of deployments with an active preview URL or production domain when a Vercel Project is provided as the parameter.

Using the vercel remove command with the --safe option.

The option, shorthand , can be used to skip the confirmation step for a deployment or Vercel Project removal.

Using the vercel remove command with the --yes option.

The following global options can be passed when using the vercel remove command:

For more information on global options and their usage, refer to the options section.

---

## Pydantic AI

**URL:** https://vercel.com/docs/ai-gateway/framework-integrations/pydantic-ai

**Contents:**
- Pydantic AI
- Getting started
  - Create a new project
  - Install dependencies
  - Configure environment variables
  - Create your Pydantic AI application
  - Running the application

Pydantic AI is a Python agent framework designed to make it easy to build production grade applications with AI. This guide demonstrates how to integrate Vercel AI Gateway with Pydantic AI to access various AI models and providers.

First, create a new directory for your project and initialize it:

Install the required Pydantic AI packages along with the package:

Create a file with your Vercel AI Gateway API key:

If you're using the AI Gateway from within a Vercel deployment, you can also use the environment variable which will be automatically provided.

Create a new file called with the following code:

Run your application using Python:

You should see structured city information for Tokyo, Paris, and New York displayed in your console.

---

## Environments

**URL:** https://vercel.com/docs/deployments/environments

**Contents:**
- Environments
- Local Development Environment
- Preview Environment (Pre-production)
- Production Environment
- Custom Environments
  - Creating a custom environment
  - Using custom environments via the CLI
  - Pricing and limits
- More resources

Vercel provides three default environments—Local, Preview, and Production:

Pro and Enterprise teams can create Custom Environments for more specialized workflows (e.g., , ). Every environment can define it’s own unique environment variables, like database connection information or API keys.

This environment is where you develop new features and fix bugs on your local machine. When building with frameworks, use the Vercel CLI to pull the environment variables for your project.

Link your Vercel project with your local directory:

Pull environment variables locally for use with application development:

This will populate the file in your application directory.

Preview environments allow you to deploy and test changes in a live setting, without affecting your production site. By default, Vercel creates a preview deployment when you:

Each deployment gets an automatically generated URL, and you'll typically see links appear in your Git provider’s PR comments or in the Vercel Dashboard.

There are two types of preview URLs:

Learn more about generated URLs.

The Production environment is the live, user-facing version of your site or application.

By default, pushing or merging changes into your production branch (commonly ) triggers a production deployment. You can also explicitly deploy to production via the CLI:

When a production deployment succeeds, Vercel updates your production domains to point to the new deployment, ensuring your users see the latest changes immediately. For advanced workflows, you can disable the auto-promotion of deployments and manually control promotion.

Custom environments are available on Enterprise and Pro plans

Custom environments are useful for longer-running pre-production environments like , , or any other specialized workflow you require.

Team owners and project admins can create, update, or remove custom environments.

To create an Authorization Bearer token, see the access token section of the API documentation.

To create an Authorization Bearer token, see the access token section of the API documentation.

You can deploy, pull, and manage environment variables to your custom environment with the CLI:

Custom environments are available at no additional cost on the Pro and Enterprise plans. The number of custom environments you can create is based on your plan:

---

## Deploying to Vercel

**URL:** https://vercel.com/docs/deployments

**Contents:**
- Deploying to Vercel
- Deployment Methods
  - Git
  - Vercel CLI
  - Deploy Hooks
  - Vercel REST API
- Accessing Deployments
- Using the Dashboard
  - Resources Tab and Deployment Summary
  - Project Overview

A deployment on Vercel is the result of a successful build of your project. Each time you deploy, Vercel generates a unique URL so you and your team can preview changes in a live environment.

Vercel supports multiple ways to create a deployment:

The most common way to create a deployment is by pushing code to a connected Git repository. When you import a Git repository to Vercel, each commit or pull request (on supported Git providers) automatically triggers a new deployment.

Vercel supports the following providers:

You can also create deployments from a Git reference using the Vercel Dashboard if you need to deploy specific commits or branches manually.

You can deploy your Projects directly from the command line using Vercel CLI. This method works whether your project is connected to Git or not.

In your project's root directory, run:

This links your local directory to your Vercel Project and creates a Production Deployment. A directory is added to store Project and Organization IDs.

Vercel CLI can also integrate with custom CI/CD workflows or third-party pipelines. Learn more about the different environments on Vercel.

Deploy Hooks let you trigger deployments with a unique URL. You must have a connected Git repository to use this feature, but the deployment does not require a new commit.

Refer to the Deploy Hooks documentation for more information.

The Vercel REST API lets you create deployments by making an HTTP request to the deployment endpoint. In this workflow:

This method is especially useful for custom workflows, multi-tenant applications, or integrating with third-party services not officially supported by Vercel. For more details, see the API reference and How do I generate an SHA for uploading a file.

Vercel provides three default environments—Local, Preview, and Production:

Learn more about environments.

Vercel’s dashboard provides a centralized way to view, manage, and gain insights into your deployments.

When you select a deployment from your Project → Deployments page, you can select the Resources tab to view and search:

You can use the three dot (…) menu for a given function to jump to that function in Logs, Analytics, Speed Insights, or the Observability tab.

You can also see a summary of these resources by expanding the Deployment Summary section on a Deployment Details page. To visit the Deployment Details page for a deployment, select it from your Project → Deployments page.

You’ll also see your build time, detected framework, and any relevant logs or errors.

On your Project Overview page, you can see the latest production deployment, including the generated URL and commit details, and deployment logs for debugging.

From the Deployments tab, you can:

For more information on interacting with your deployments, see Managing Deployments.

---

## Claim Deployments

**URL:** https://vercel.com/docs/deployments/claim-deployments

**Contents:**
- Claim Deployments
- Get started
- Associated resources
- Important endpoints
- Example use case: automated AI-generated deployment
- Team restructuring
- Migrating personal projects to a company account

The Claim Deployments feature enables users to take control of deployments by transferring them to their Vercel accounts. Users can generate and share a claim URL, which allows others to assume ownership of these deployments. This feature is particularly helpful for AI-generated deployments and facilitates the transfer of projects between different accounts with different owners.

However, when transferring a project between two teams owned by the same user, it is recommended to use the Project Transfer flow instead of the Claim Deployments flow.

When a user claims a deployment, Vercel also transfers any associated resources (limited to specific providers) to the new owner's account. These resources maintain their connections to the project, ensuring a seamless transition of both the deployment and its dependencies.

The resource provider that currently supports resource transfer is Prisma.

For more details on the transfer process, see Resources with Claim Deployments flows.

Claim Deployments URL:

Initiate a project transfer request: POST /projects/:idOrName/transfer-request

Complete a project transfer: PUT /projects/transfer-request/:code

File upload: The AI agent uploads the deployment files using the Vercel API: POST /files.

Project transfer request:

User claims the deployment:

Project transfer completion:

Get started with this template of claiming deployments (demo).

When reorganizing teams, you can easily transfer ownership of projects to another team using the Claim Deployments feature.

Freelancers or employees can move deployments from their personal accounts to a company’s Vercel account by generating and sharing a claim URL.

---

## Vercel Functions Limits

**URL:** https://vercel.com/docs/functions/limitations

**Contents:**
- Vercel Functions Limits
- Functions name
- Bundle size limits
- Max duration
  - Node.js and python runtimes
  - Edge runtime
- Memory size limits
- Request body size
- File descriptors
- API support

The table below outlines the limits and restrictions of using Vercel Functions with the Node.js runtime:

The following limits apply to the function's name when using Node.js runtime:

Vercel places restrictions on the maximum size of the deployment bundle for functions to ensure that they execute in a timely manner.

For Vercel Functions, the maximum uncompressed size is 250 MB including layers which are automatically used depending on runtimes. These limits are enforced by AWS.

You can use and to specify items which may affect the function size, however the limits cannot be configured. These configurations are not supported in Next.js, instead use .

This refers to the longest time a function can process an HTTP request before responding.

While Vercel Functions have a default duration, this duration can be extended using the maxDuration config. If a Vercel Function doesn't respond within the duration, a 504 error code () is returned.

With fluid compute enabled, Vercel Functions have the following defaults and maximum limits (applies to the Node.js and Python runtimes):

Vercel Functions have the following defaults and maximum limits for the duration of a function:

Vercel Functions using the Edge runtime must begin sending a response within 25 seconds to maintain streaming capabilities beyond this period, and can continue streaming data for up to 300 seconds.

Vercel Functions have the following defaults and maximum limits:

Users on Pro and Enterprise plans can configure the default memory size for all functions in the dashboard.

The maximum size for a Function includes your JavaScript code, imported libraries and files (such as fonts), and all files bundled in the function.

If you reach the limit, make sure the code you are importing in your function is used and is not too heavy. You can use a package size checker tool like bundle to check the size of a package and search for a smaller alternative.

In Vercel, the request body size is the maximum amount of data that can be included in the body of a request to a function.

The maximum payload size for the request body or the response body of a Vercel Function is 4.5 MB. If a Vercel Function receives a payload in excess of the limit it will return an error 413: . See How do I bypass the 4.5MB body size limit of Vercel Functions for more information.

File descriptors are unique identifiers that the operating system uses to track and manage open resources like files, network connections, and I/O streams. Think of them as handles or references that your application uses to interact with these resources. Each time your code opens a file, establishes a network connection, or creates a socket, the system assigns a file descriptor to track that resource.

Vercel Functions have a limit of 1,024 file descriptors shared across all concurrent executions. This limit includes file descriptors used by the runtime itself, so the actual number available to your application code will be strictly less than 1,024.

File descriptors are used for:

If your function exceeds this limit, you might encounter errors related to "too many open files" or similar resource exhaustion issues.

To manage file descriptors effectively, consider the following:

The Hobby plan offers functions for free, within limits. The Pro plan extends these limits, and charges usage based on active CPU time and provisioned memory time for Vercel Functions.

Active CPU time is based on the amount of CPU time your code actively consumes, measured in milliseconds. Waiting for I/O (e.g. calling AI models, database queries) does not count towards active CPU time. Provisioned memory time is based on the memory allocated to your function instances multiplied by the time they are running.

It is important to make sure you've set a reasonable maximum duration for your function. See "Managing usage and pricing for Vercel Functions" for more information.

If you have fluid compute enabled, the following environment variables are not accessible and you cannot log them:

---

## Skew Protection

**URL:** https://vercel.com/docs/skew-protection

**Contents:**
- Skew Protection
- Enable Skew Protection
- Custom Skew Protection Threshold
- Monitor Skew Protection
- Supported frameworks
- Skew Protection with Next.js
- Skew Protection with SvelteKit
- Skew Protection with Qwik
- Skew Protection with Astro
- Limitations

Skew Protection is available on Enterprise and Pro plans

Those with the owner, admin, member role can access this feature

Version skew occurs when different versions of your application run on client and server, causing application errors and other unexpected behavior. For example, imagine your newest deployment modifies the data structure by adding a required field to a user's profile. Older clients wouldn't expect this new field, leading to errors when they submit it.

Vercel's Skew Protection resolves this problem at the platform and framework layer by using version locking, which ensures client and server use the exact same version. In our example, outdated clients continue to communicate with servers that understand the old data structure, while updated clients use the most recent deployment.

By implementing Skew Protection, you can reduce user-facing errors during new rollouts and boost developer productivity, minimizing concerns about API compatibility across versions.

Projects created after November 19th 2024 using one of the supported frameworks already have Skew Protection enabled by default.

For older projects, you can enable Skew Protection in your project's settings.

In some cases, you may have problematic deployments you want to ensure no longer resolves requests from any other active clients.

Once you deploy a fix, you can set a Skew Protection threshold with the following:

This ensure that deployments created before the fixed deployment will no longer resolve requests from outdated clients.

You can observe how many requests are protected from version skew by visiting the Monitoring page in the Vercel dashboard.

For example, on the event, filter where .

You can view Edge Requests that are successfully fulfilled without the need for skew protection by using .

Skew Protection is available with zero configuration when using the following frameworks:

Other frameworks can implement Skew Protection by checking if has value and then appending the value of to each request using one of the following options.

If you're building outside of Vercel and then deploying using the command, Skew Protection will not be enabled because the Deployment ID was not known at build time. For more information, see When not to use --prebuilt.

If you are using Next.js 14.1.4 or newer, there is no additional configuration needed to enable Skew Protection.

Older versions of Next.js require additional configuration.

The configuration enables Skew Protection for all framework-managed static file requests from your Next.js app such as for JavaScript and CSS files. You can also opt-into Skew Protection for Next.js Server Actions with .

If you are using SvelteKit, you will need to install version 5.2.0 or newer in order to enable Skew Protection.

Older versions can be upgraded by running .

If you are using Qwik 1.5.3 or newer, there is no additional configuration needed to enable Skew Protection.

Older versions can be upgraded by running .

If you are using Astro, you will need to install version 9.0.0 or newer in order to enable Skew Protection.

Older versions can be upgraded by running .

Skew Protection is only available for Pro and Enterprise, not for Hobby teams. You can configure a custom maximum age up to, but not exceeding, your project's retention policy.

Vercel automatically adjusts the maximum age to 60 days for requests from Googlebot and Bingbot in order to handle any delay between document crawl and render.

Deployments that have been deleted either manually or automatically using a retention policy will not be accessible through Skew Protection.

---

## Methods to bypass Deployment Protection

**URL:** https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection

**Contents:**
- Methods to bypass Deployment Protection
- Sharable Links
- Protection bypass for Automation
- Deployment Protection Exceptions
- OPTIONS Allowlist
- More resources

To test, share, or exclude specific domains from Deployment Protection, you can use the following methods to allow specific access while maintaining overall security:

Shareable Links are available on all plans

Sharable Links allow external access to specific branch deployments through a secure query parameter. Users with this link can see the latest deployment and leave comments (if enabled and logged in with their Vercel account).

For example, if you generate a Sharable Link for the branch. Users with this link can view the latest deployment and comment.

Learn more about Sharable Links, and how to generate and revoke them.

Protection Bypass for Automation is available on all plans

For automated tasks like end-to-end (E2E) testing, you can use Protection bypass for Automation. When enabled, it generates a secret that can be used as a System Environment Variable () to bypass protection features for all deployments in a project.

For example, you set up E2E tests that run on deployments. By using this feature and the generated secret, your tests can bypass the protection mechanisms.

Learn more about Protection bypass for Automation, and how to enable and disable it.

Deployment Protection Exceptions are available on Enterprise plansor with the Advanced Deployment Protection add-on for Pro plans

With Deployment Protection Exceptions you can specify preview domains that should be exempt from deployment protection. Adding a domain to Deployment Protection Exceptions makes it publicly accessible, bypassing features like Vercel Authentication, Password Protection, and Trusted IPs.

For example, if you add to Deployment Protection Exceptions, this domain becomes publicly accessible, bypassing the project's deployment protection settings. When removed, it reverts to the default protection settings.

Learn more about Deployment Protection Exceptions, and how to add and remove domains.

OPTIONS Allowlist is available on all plans

With OPTIONS Allowlist you can specify paths to be unprotected for preflight OPTIONS requests. This can be used to enable CORS preflight requests to your project's protected deployments, as browsers do not send authentication on preflight requests.

Incoming request paths will be compared with the paths in the allowlist, if a request path starts with one of the specified paths, and has the method , it will bypass Deployment Protection.

For example, if you specify , all requests to paths that start with (such as and ) will be unprotected for any request.

Learn more about OPTIONS Allowlist.

---

## Vercel Toolbar

**URL:** https://vercel.com/docs/vercel-toolbar

**Contents:**
- Vercel Toolbar
- Activating the Toolbar
- Enabling or Disabling the toolbar
- Using the Toolbar Menu
- Setting Custom Keyboard Shortcuts
- Sharing deployments
- Reposition toolbar
- Toolbar Menu preferences
- More resources

Vercel Toolbar is available on all plans

The Vercel Toolbar is a tool that assists in the iteration and development process. Through the toolbar, you can:

By default, when the toolbar first shows up on your deployments it is sleeping. This means it will not run any tools in the background or show comments on pages. You can activate it by clicking it or using ctrl. It will start activated if a tool is needed to show you the link you’re visiting, like a link to a comment thread or a link with flags overrides.

Users who have installed the browser extension can toggle on Always Activate in Preferences from the Toolbar menu.

The Vercel Toolbar is enabled by default for all preview deployments. You can disable the toolbar at the team, project, or session level.

You can also manage its visibility for automation with HTTP headers and through environment variables. To learn more, see Managing the toolbar.

To enable the toolbar for your local or production environments, see Adding the toolbar to your environment.

You can access the Toolbar Menu by pressing ctrl on your keyboard.

Alternatively, you can also access the Toolbar Menu through the Vercel Toolbar by clicking the menu icon. If you haven't activated the toolbar yet, log in first to display the menu.

You can set your own keyboard shortcuts to quickly access specific tools. Additionally, you can change the default keyboard shortcuts for the Toolbar Menu ctrl and for showing/hiding the toolbar . by following these steps:

You can use the Share button in deployments with the Vercel Toolbar enabled, as well as in all preview deployments, to share your deployment's generated URL. When you use the Share button from the toolbar, the URL will contain any relevant query parameters.

To share a deployment:

If you're on an Enterprise team, you will be able to see who shared deployment URLs in your audit logs.

You can reposition the toolbar by dragging it to either side of your screen. It will snap into place and appear there across deployments until you move it again. Repositioning only affects where you see the toolbar, it does not change the toolbar position for your collaborators.

When logged into the Vercel Toolbar, you'll find a Preferences button in the Toolbar Menu. In this menu, you can update the following settings:

---

## Configuring projects with vercel.json

**URL:** https://vercel.com/docs/project-configuration

**Contents:**
- Configuring projects with vercel.json
- Schema autocomplete
- buildCommand
- bunVersion
- cleanUrls
- crons
  - Cron object definition
- devCommand
- fluid
- framework

The file lets you configure, and override the default behavior of Vercel from within your project.

This file should be created in your project's root directory and allows you to set:

To add autocompletion, type checking, and schema validation to your file, add the following to the top of your file:

The property can be used to override the Build Command in the Project Settings dashboard, and the script from the file for a given deployment. For more information on the default behavior of the Build Command, visit the Configure a Build - Build Command section.

This value overrides the Build Command in Project Settings.

The Bun runtime is available in Beta on all plans

The property configures your project to use the Bun runtime instead of Node.js. When set, all Vercel Functions and Routing Middleware not using the Edge runtime will run using the specified Bun version.

Vercel manages the Bun minor and patch versions automatically. is the only valid value currently.

When using Next.js with ISR (Incremental Static Regeneration), you must also update your and commands in :

To learn more about using Bun with Vercel Functions, see the Bun runtime documentation.

When set to , all HTML files and Vercel functions will have their extension removed. When visiting a path that ends with the extension, a 308 response will redirect the client to the extensionless path.

For example, a static file named will be served when visiting the path. Visiting will redirect to .

Similarly, a Vercel Function named will be served when visiting . Visiting will redirect to .

If you are using Next.js and running , you will get a 404 error when visiting a route configured with locally. It does however work fine when deployed to Vercel. In the example above, visiting locally will give you a 404 with but will render correctly on Vercel.

Used to configure cron jobs for the production deployment of a project.

This value overrides the Development Command in Project Settings.

The property can be used to override the Development Command in the Project Settings dashboard. For more information on the default behavior of the Development Command, visit the Configure a Build - Development Command section.

This value allows you to enable Fluid compute programmatically.

The property allows you to test Fluid compute on a per-deployment or per custom environment basis when using branch tracking, without needing to enable Fluid in production.

As of April 23, 2025, Fluid compute is enabled by default for new projects.

This value overrides the Framework in Project Settings.

Available framework slugs:

The property can be used to override the Framework Preset in the Project Settings dashboard. The value must be a valid framework slug. For more information on the default behavior of the Framework Preset, visit the Configure a Build - Framework Preset section.

To select "Other" as the Framework Preset, use null.

Type: of key and value .

A glob pattern that matches the paths of the Vercel functions you would like to customize:

By default, no configuration is needed to deploy Vercel functions to Vercel.

For all officially supported runtimes, the only requirement is to create an directory at the root of your project directory, placing your Vercel functions inside.

The property cannot be used in combination with . Since the latter is a legacy configuration property, we recommend dropping it in favor of the new one.

Because Incremental Static Regeneration (ISR) uses Vercel functions, the same configurations apply. The ISR route can be defined using a glob pattern, and accepts the same properties as when using Vercel functions.

When deployed, each Vercel Function receives the following properties:

To configure them, you can add the property.

In order to use a runtime that is not officially supported, you can add a property to the definition:

In the example above, the Vercel Function does not use one of the officially supported runtimes. In turn, a property was added in order to invoke the vercel-php community runtime.

For more information on Runtimes, see the Runtimes documentation:

Valid values: a list of header definitions.

This example configures custom response headers for static files, Vercel functions, and a wildcard that matches all routes.

If is an object, it has one or more of the following fields:

This example demonstrates using the expressive object to append the header if the request header's value is prefixed by and ends with .

Learn more about rewrites on Vercel and see limitations.

This value overrides the Ignored Build Step in Project Settings.

This property will override the Command for Ignoring the Build Step for a given deployment. When the command exits with code 1, the build will continue. When the command exits with 0, the build is ignored. For more information on the default behavior of the Ignore Command, visit the Ignored Build Step section.

This value overrides the Install Command in Project Settings.

The property can be used to override the Install Command in the Project Settings dashboard for a given deployment. This setting is useful for trying out a new package manager for the project. An empty string value will cause the Install Command to be skipped. For more information on the default behavior of the install command visit the Configure a Build - Install Command section.

The property defines the behavior of Vercel's native Image Optimization API, which allows on-demand optimization of images at runtime.

This value overrides the Output Directory in Project Settings.

The property can be used to override the Output Directory in the Project Settings dashboard for a given deployment.

In the following example, the deployment will look for the directory rather than the default or root directory. For more information on the default behavior of the Output Directory see the Configure a Build - Output Directory section. The following example is a file that overrides the to :

When set to , both the source view and logs view will be publicly accessible.

Valid values: a list of redirect definitions.

This example redirects requests to the path from your site's root to the file relative to your site's root with a 307 Temporary Redirect:

This example redirects requests to the path from your site's root to the file relative to your site's root with a 308 Permanent Redirect:

This example redirects requests to the path from your site's root to the api route relative to your site's root with a 301 Moved Permanently:

This example redirects requests to the path from your site's root to the absolute path of an external site with a redirect status of 308:

This example redirects requests to all the paths (including all sub-directories and pages) from your site's root to the absolute path of an external site with a redirect status of 308:

This example uses wildcard path matching to redirect requests to any path (including subdirectories) under from your site's root to a corresponding path under relative to your site's root with a redirect status of 308:

This example uses regex path matching to redirect requests to any path under that only contain numerical digits from your site's root to a corresponding path under relative to your site's root with a redirect status of 308:

This example redirects requests to any path from your site's root that does not start with and has header value of to a corresponding path under relative to your site's root with a redirect status of 307:

Using has does not yet work locally while using vercel dev, but does work when deployed.

If is an object, it has one or more of the following fields:

This example uses the expressive object to define a route that redirects users with a redirect status of 308 to only if the header's value is prefixed by and ends with .

Learn more about redirects on Vercel and see limitations.

Learn more about bulk redirects on Vercel and see limits and pricing.

Type: path to a file or folder.

The property can be used to import many thousands of redirects per project. These redirects do not support wildcard or header matching.

CSV, JSON, and JSONL file formats are supported, and the redirect files can be generated at build time as long as they end up in the location specified by . This can point to either a single file or a folder containing multiple redirect files.

CSV headers must match the field names below, can be specific in any order, and optional fields can be ommitted.

Bulk redirects do not work locally while using vercel dev

In order to improve space efficiency, all boolean values can be the single characters (true) or (false) while using the CSV format.

This value overrides the Vercel Function Region in Project Settings.

Type: of region identifier .

Valid values: List of regions, defaults to .

You can define the regions where your Vercel functions are executed. Users on Pro and Enterprise can deploy to multiple regions. Hobby plans can select any single region. To learn more, see Configuring Regions.

Function responses can be cached in the requested regions. Selecting a Vercel Function region does not impact static files, which are deployed to every region by default.

Setting failover regions for Vercel functions are available on Enterprise plans

Set this property to specify the region to which a Vercel Function should fallback when the default region(s) are unavailable.

Type: of region identifier .

Valid values: List of regions.

These regions serve as a fallback to any regions specified in the configuration. The region Vercel selects to invoke your function depends on availability and ingress. For instance:

To learn more about automatic failover for Vercel Functions, see Automatic failover. Vercel Functions using the Edge runtime will automatically failover with no configuration required.

Region failover is supported with Secure Compute, see Region Failover to learn more.

Valid values: a list of rewrite definitions.

If is set to in your project's , do not include the file extension in the source or destination path. For example, would be

This example rewrites requests to the path from your site's root to the file relative to your site's root:

This example rewrites all requests to the root path which is often used for a Single Page Application (SPA).

This example rewrites requests to the paths under that with 2 paths levels (defined as variables and that can be used in the destination value) to the api route relative to your site's root:

This example uses wildcard path matching to rewrite requests to any path (including subdirectories) under from your site's root to a corresponding path under the root of an external site :

This example rewrites requests to any path from your site's root that does not start with /uk/ and has x-vercel-ip-country header value of GB to a corresponding path under /uk/ relative to your site's root:

This example rewrites requests to the path from your site's root that does not have a cookie with key to the path relative to your site's root:

If is an object, it has one or more of the following fields:

This example demonstrates using the expressive object to define a route that rewrites users to only if the header's value is prefixed by and ends with .

The property should NOT be a file because precedence is given to the filesystem prior to rewrites being applied. Instead, you should rename your static file or Vercel Function.

Using has does not yet work locally while using vercel dev, but does work when deployed.

Learn more about rewrites on Vercel.

When , visiting a path that ends with a forward slash will respond with a 308 status code and redirect to the path without the trailing slash.

For example, the path will redirect to .

When , visiting a path that does not end with a forward slash will respond with a 308 status code and redirect to the path with a trailing slash.

For example, the path will redirect to .

However, paths with a file extension will not redirect to a trailing slash.

For example, the path will not redirect, but the path will redirect to .

When , visiting a path with or without a trailing slash will not redirect.

For example, both and will serve the same content without redirecting.

This is not recommended because it could lead to search engines indexing two different pages with duplicate content.

Legacy properties are still supported for backwards compatibility, but are deprecated.

The property has been deprecated in favor of Project Linking, which allows you to link a Vercel project to your local codebase when you run .

Valid values: string name for the deployment.

The prefix for all new deployment instances. Vercel CLI usually generates this field automatically based on the name of the directory. But if you'd like to define it explicitly, this is the way to go.

The defined name is also used to organize the deployment into a project.

The property should not be used anymore.

Specifies the Vercel Platform version the deployment should use.

The property should not be used anymore. To assign a custom Domain to your project, please define it in the Project Settings instead. Once your domains are, they will take precedence over the configuration property.

Valid values: domain names (optionally including subdomains) added to the account, or a string for a suffixed URL using or a Custom Deployment Suffix (available on the Enterprise plan).

Limit: A maximum of 64 aliases in the array.

The alias or aliases are applied automatically using Vercel for GitHub, Vercel for GitLab, or Vercel for Bitbucket when merging or pushing to the Production Branch.

You can deploy to the defined aliases using Vercel CLI by setting the production deployment environment target.

The property has been deprecated in favor of Project Linking, which allows you to link a Vercel project to your local codebase when you run .

Valid values: For teams, either an ID or slug. For users, either a email address, username, or ID.

This property determines the scope (Hobby team or team) under which the project will be deployed by Vercel CLI.

It also affects any other actions that the user takes within the directory that contains this configuration (e.g. listing environment variables using ).

Deployments made through Git will ignore the property because the repository is already connected to project.

We recommend against using this property. To add custom environment variables to your project define them in the Project Settings.

Type: of keys and values.

Valid values: environment keys and values.

Environment variables passed to the invoked Vercel functions.

This example will pass the static env to all Vercel functions and the resolved from the secret dynamically.

We recommend against using this property. To add custom environment variables to your project define them in the Project Settings.

Type: of keys and values inside the .

Valid values: environment keys and values.

Environment variables passed to the Build processes.

The following example will pass the environment variable to all Builds and the resolved from the secret dynamically.

We recommend against using this property. To customize Vercel functions, please use the functions property instead. If you'd like to deploy a monorepo, see the Monorepo docs.

Valid values: a list of build descriptions whose references valid source files.

The following will include all HTML files as-is (to be served statically), and build all Python files and JS files into Vercel functions:

When at least one item is specified, only the outputs of the build processes will be included in the resulting deployment as a security precaution. This is why we need to allowlist static files explicitly with .

We recommend using cleanUrls, trailingSlash, redirects, rewrites, and/or headers instead.

The property is only meant to be used for advanced integration purposes, such as the Build Output API, and cannot be used in conjunction with any of the properties mentioned above.

See the upgrading routes section to learn how to migrate away from this property.

Valid values: a list of route definitions.

Routes are processed in the order they are defined in the array, so wildcard/catch-all patterns should usually be last.

If is an object, it has one or more of the following fields:

This example uses the expressive object to define a route that will only rewrite users to if the header's value is prefixed by and ends with :

This example configures custom routes that map to static files and Vercel functions:

Target is an object with a property. For the operation, the property is used as the header or query key. For other operations, it is used as a matching condition to determine if the transform should be applied.

When the property is an object, it can contain one or more of the following conditional matching properties:

These examples demonstrate practical use-cases for route transforms.

In this example, you remove the incoming request header from all requests and responses to the route:

In this example, you override the incoming query parameter to for all requests to the route, and set if it doesn't already exist:

In this example, you append multiple values to the incoming request header for all requests to the route:

In this example, you delete any header that begins with for all requests to the route:

You can integrate transforms with existing matching capabilities through the and properties for routes, along with using expressive matching conditions through the Transform key object definition.

In most cases, you can upgrade legacy usage to the newer , , , or properties.

Here are some examples that show how to upgrade legacy to the equivalent new property.

With , you use a PCRE Regex named group to match the ID and then pass that parameter in the query string. The following example matches a URL like and proxies to :

With , named parameters are automatically passed in the query string. The following example is equivalent to the legacy usage above, but uses instead:

With , you specify the status code to use a 307 Temporary Redirect. Also, this redirect needs to be defined before other routes. The following example redirects all paths in the directory to the directory, but keeps the path in the new location:

With , you disable the property to use a 307 Temporary Redirect. Also, are always processed before . The following example is equivalent to the legacy usage above, but uses instead:

With , you use to give precedence to the filesystem and exit early if the requested path matched a file. The following example will serve the file for all paths that do not match a file in the filesystem:

With , the filesystem check is the default behavior. If you want to change the name of files at the filesystem level, file renames can be performed during the Build Step, but not with . The following example is equivalent to the legacy usage above, but uses instead:

With , you use to prevent stopping at the first match. The following example adds headers to the favicon and other static assets:

With , this is no longer necessary since that is the default behavior. The following example is equivalent to the legacy usage above, but uses instead:

With , you need to escape a dot with two backslashes, otherwise it would match any character PCRE Regex. The following example matches the literal and proxies to to dynamically generate RSS:

With , the is not a special character so it does not need to be escaped. The following example is equivalent to the legacy usage above, but instead uses :

With , you use PCRE Regex negative lookahead. The following example proxies all requests to the page except for itself to avoid infinite loop:

With , the Regex needs to be wrapped. The following example is equivalent to the legacy usage above, but instead uses :

With , the property is case-insensitive leading to duplicate content, where multiple request paths with difference cases serve the same page.

With / / , the property is case-sensitive so you don't accidentally create duplicate content.

---

## Adding & Configuring a Custom Domain

**URL:** https://vercel.com/docs/domains/working-with-domains/add-a-domain

**Contents:**
- Adding & Configuring a Custom Domain
- Add and configure domain
  - Navigate to Domain Settings
  - Add your domain
  - Using wildcard domain
  - Configure the domain
    - Apex domains
    - Subdomains
    - Vercel Nameservers
  - Verify domain access

Vercel provides all deployments with a URL, which enables you to share Deployments with your Team for collaboration. However, to provide greater personalization and flexibility to your project, you can instead add a custom domain. If you don't own a domain yet, you can purchase it with Vercel.

You can manage all domain settings related to a project in the Domains section of the Settings tab of the project, regardless of whether you are using apex domains or subdomains in your project. This document will guide you through both options.

Hobby teams have a limit of 50 custom domains per project.

The following steps provide an overview of how to add and configure a custom domain in Vercel:

On the dashboard, pick the project to which you would like to assign your domain.

Once you have selected your project, click on the Settings tab and then select the Domains menu item:

From the Domains page, click the Add Domain button:

Input the domain you wish to include in the project:

If you add an apex domain (e.g. ) to the project, Vercel will prompt you to add the subdomain prefix. For more information about why we recommend using a domain, see "Redirecting domains".

You can also use your custom domain as a wildcard domain by prefixing it with .

If using your custom domain as a wildcard domain, you must use the nameservers method for verification.

To add a wildcard domain, use the prefix , for example .

Once you have added your custom domain, you will need to configure the DNS records of your domain with your registrar so it can be used with your Project. The dashboard will automatically display different methods for configuring it:

Both apex domains and subdomains can also be configured using the Nameservers method.

If you are verifying your domain by changing nameservers, you will need to add any DNS records to Vercel that you wish to keep from your previous DNS provider.

You can configure apex domains with an A record.

You can configure subdomains with a CNAME record. Each project has a unique CNAME record e.g. .

If you choose to use a wildcard domain Vercel's nameservers will be automatically enabled for you on saving the domain settings. You will then be provided with the Vercel nameservers to copy and use with your registrar.

If the domain is in use by another Vercel account, you may be prompted to verify access to the domain. Note that this will not move the domain into your account, but will allow you to use it in your project. If you have multiple domains to verify, be aware that you can only set up one TXT record at a time, but you can modify it after the domain is transferred.

Once the domain has been configured and Vercel has verified it, the status of the domain will be updated within the UI to confirm that it is ready for use.

If a someone visits your domain with or without the "www" subdomain prefix, Vercel will attempt to redirect them to your domain. For more robust protection, you should explicitly add this domain and redirect it.

---

## Sharing a Preview Deployment

**URL:** https://vercel.com/docs/deployments/sharing-deployments

**Contents:**
- Sharing a Preview Deployment
- Sharing with members of your team
- Sharing a preview deployment with external collaborators
  - Invite users
  - Sharing with sharable links and managing permissions
  - Request access
- Sharing with deployment protection enabled

By default, members of your Vercel team that have access to your project will also have access to your deployment. This allows them to comment, see who else is viewing the preview, and use the toolbar. Users who don't have access to the project will not have access to your deployment.

To share a preview deployment with a member of your team you can do any of the following:

They will also be able to find it by using the generated URL from any deployment in the Vercel dashboard.

To share a deployment with anyone, you can do any of the following:

When you share a preview deployment with an external user, they will not be added to your Vercel team. The collaborator does not need to have a Vercel account, but will need to create one if they wish to view a deployment that is protected, use the toolbar, or leave comments.

Note that you can share two types of links: branch links, which reflect the latest commit, and commit links, which reflect changes up to a specific commit.

When sharing from the Share button next to the deployment in the Vercel dashboard, the share modal defaults to the branch link. You can switch to the commit link by selecting the dropdown arrow.

When sharing from Share in the toolbar menu, you'll share the current link. If it's a commit-specific link, you can switch to the branch link to share an always up-to-date preview.

Users on Pro and Enterprise teams can use this method to add one or more collaborators. Hobby users are limited to one collaborator at any one time. To invite users to view your deployment:

This is the recommended method for sharing a deployment with external collaborators, as it allows you to control who has access to your deployment on an individual basis.

To learn more, see sharable links in Deployment Protection.

If someone without access to comment attempts to log into the toolbar on a deployment, they will see a screen with the option to Request Access. You will be notified by email and the Vercel notifications widget when a request is made to a deployment you own.

To respond to the request:

It is important to ensure the security of your preview deployments, which you can enable through deployment protection. We recommend that you scope access to the fewest number of people possible.

Deployment protection allows you to secure your preview deployments, with Authentication and/or Password Protection to ensure that only authorized users can view your preview deployment.

---

## vercel open

**URL:** https://vercel.com/docs/cli/open

**Contents:**
- vercel open
- Usage
- How it works
- Examples
  - Open the current project
- Troubleshooting
  - Project not linked
- Global Options
- Related

The command opens your current project in the Vercel Dashboard. It automatically opens your default browser to the project's dashboard page, making it easy to access project settings, deployments, and other configuration options.

This command is available in Vercel CLI v48.10.0 and later. If you're using an older version, see Updating Vercel CLI.

This command requires your directory to be linked to a Vercel project. If you haven't linked your project yet, run first.

Using the vercel open command to open the current project in the Vercel Dashboard.

The command opens the project's main dashboard page at , where you can view deployments, configure settings, and manage your project.

From a linked project directory:

Opening the current project in the Vercel Dashboard.

This opens your browser to the project's dashboard page.

If you see an error that the command requires a linked project:

Linking your project before opening it in the dashboard.

Make sure you're in the correct directory where your project files are located.

The following global options can be passed when using the vercel open command:

For more information on global options and their usage, refer to the options section.

---

## Managing projects

**URL:** https://vercel.com/docs/projects/managing-projects

**Contents:**
- Managing projects
- Creating a project
- Pausing a project
  - Pausing a project when you reach your spend amount
  - Pause a project using the REST API
  - Resuming a project
- Deleting a project

You can manage your project on Vercel in your project's dashboard. See our project dashboard docs to learn more.

To create a new project:

To create an Authorization Bearer token, see the access token section of the API documentation.

To create an Authorization Bearer token, see the access token section of the API documentation.

You can choose to temporarily pause a project to ensure that you do not incur usage from metered resources on your production deployment.

To automatically pause your projects when you reach your spend amount:

To learn more, see the Spend Management documentation.

To pause a project manually or with a webhook you can use the REST API:

When you pause your project, any users accessing your production deployment will see a 503 DEPLOYMENT_PAUSED error.

You can also manually make a POST request to the pause project endpoint without using webhook.

Resuming a project can either be done through the REST API or your project settings:

Your production deployment will resume service within a few minutes. You do not need to redeploy it.

Deleting your project will also delete the deployments, domains, environment variables, and settings within it. If you have any deployments that are assigned to a custom domain and do not want them to be removed, make sure to deploy and assign them to the custom domain under a different project first.

---

## Monitoring

**URL:** https://vercel.com/docs/query/monitoring

**Contents:**
- Monitoring
- Monitoring chart
- Example queries
- Save new queries
  - Manage saved queries
- Error messages
- Enable Monitoring
- Disable Monitoring
- Manage IP Address visibility for Monitoring
- Monitoring sunset

Monitoring allows you to visualize and quantify the performance and traffic of your projects on Vercel. You can use example queries or create custom queries to debug and optimize bandwidth, errors, performance, and bot traffic issues in a production or preview deployment.

Monitoring is available on Enterprise plans

Charts allow you to explore your query results in detail. Use filters to adjust the date, data granularity, and chart type (line or bar).

Hover and move your mouse across the chart to view your data at a specific point in time. For example, if the data granularity is set to 1 hour, each point in time will provide a one-hour summary.

To get started with the most common scenarios, use our Example Queries. You cannot edit or add new example queries. For a list of the available options, view our example queries docs.

You can no longer save new Monitoring queries as the feature has now been sunset.

Instead, use observability queries, which can be saved into Notebooks.

You can manage your saved personal and team queries from the query console. Select a query from the left navigation bar and click on the vertical ellipsis (⋮) in the upper right-hand corner. You can choose to Duplicate, Rename, or Delete the selected query from the dropdown menu.

Duplicating a query creates a copy of the query in the same folder. You cannot copy queries to another folder. To rename a saved query, use the ellipses (⋮) drop-down menu or directly click its title to edit.

Deleting a saved personal or team query is permanent and irreversible. To delete a saved query, click the Delete button in the confirmation modal.

You may encounter errors such as invalid queries when using Monitoring. For example, defining an incorrect location parameter generates an invalid query. In such cases, no data appears.

You can no longer enable Monitoring on Pro plans as the feature has now been sunset.

Get the most comprehensive suite of tools, including queries, by enabling Observability Plus.

Managing IP Address visibility is available on Enterprise and Pro plans

Those with the owner, admin role can access this feature

Vercel creates events each time a request is made to your website. These events include unique parameters such as execution time and bandwidth used.

Certain events such as may be considered personal information under certain data protection laws. To hide IP addresses from your Monitoring queries:

For business purposes, such as DDoS mitigation, Vercel will still collect IP addresses.

For a complete list of fields, see the visualize clause docs.

From the end of billing cycle in Nov 2025, Vercel will sunset Monitoring for pro plans. Pro users will no longer see the Monitoring tab. Current enterprise users with monitoring access will keep the deprecated version of monitoring. If you want to continue using the full Monitoring capabilities or purchase a product similar to Monitoring, consider moving to Query.

For more information on what to do next, we recommend the following articles:

---

## vercel promote

**URL:** https://vercel.com/docs/cli/promote

**Contents:**
- vercel promote
- Usage
- Unique Options
  - Timeout
- Global Options

The command is used to promote an existing deployment to be the current deployment.

Deployments built for the Production environment are the typical promote target. You can promote Deployments built for the Preview environment, but you will be asked to confirm that action and will result in a new production deployment. You can bypass this prompt by using the option.

Using vercel promote will promote an existing deployment to be current.

These are options that only apply to the command.

The option is the time that the command will wait for the promotion to complete. When a timeout occurs, it does not affect the actual promotion which will continue to proceed.

When promoting a deployment, a timeout of will immediately exit after requesting the promotion. The default timeout is .

Using the vercel promote command with the --timeout option.

The following global options can be passed when using the vercel promote command:

For more information on global options and their usage, refer to the options section.

---

## vercel dev

**URL:** https://vercel.com/docs/cli/dev

**Contents:**
- vercel dev
- When to Use This Command
- Usage
- Unique Options
  - Listen
  - Yes
- Global Options

The command is used to replicate the Vercel deployment environment locally, allowing you to test your Vercel Functions and Middleware without requiring you to deploy each time a change is made.

If the Development Command is configured in your Project Settings, it will affect the behavior of for everyone on that team.

Before running vercel dev, make sure to install your dependencies by running npm install.

If you're using a framework and your framework's Development Command already provides all the features you need, we do not recommend using .

For example, Next.js's Development Command () provides native support for Functions, redirects, rewrites, headers and more.

Using the vercel dev command from the root of a Vercel Project directory.

These are options that only apply to the command.

The option, shorthand , can be used to specify which port runs on.

Using the vercel dev command with the --listen option.

The option can be used to skip questions you are asked when setting up a new Vercel Project. The questions will be answered with the default scope and current directory for the Vercel Project name and location.

Using the vercel dev command with the --yes option.

The following global options can be passed when using the vercel dev command:

For more information on global options and their usage, refer to the options section.

---

## General settings

**URL:** https://vercel.com/docs/project-configuration/general-settings

**Contents:**
- General settings
- Project name
- Build and development settings
- Nodejs version
- Project ID
- Vercel Toolbar settings

Project names can be up to 100 characters long and must be lowercase. They can include letters, digits, and the following characters: , , . However, they cannot contain the sequence .

You can edit settings regarding the build and development settings, root directory, and the install command. See the Configure a build documentation to learn more.

The changes you make to these settings will only be applied starting from your next deployment.

Learn more about how to customize the Node.js version of your project in the Node.js runtime documentation.

You can also learn more about all supported versions of Node.js.

Your project ID can be used by the REST API to carry out tasks relating to your project. To locate your Project ID:

The Vercel Toolbar is a tool that assists you in iterating and developing your project and is enabled by default on preview deployments. You can enable or disable the toolbar in your project settings.

---

## vercel rolling-release

**URL:** https://vercel.com/docs/cli/rolling-release

**Contents:**
- vercel rolling-release
- Usage
- Commands
  - configure
  - start
  - approve
  - abort
  - complete
  - fetch
- Unique Options

The command (also available as ) is used to manage your project's rolling releases. Rolling releases allow you to gradually roll out new deployments to a small fraction of your users before promoting them to everyone.

Using vercel rolling-release with a specific command to manage rolling releases.

Configure rolling release settings for a project.

Using the vercel rolling-release configure command to set up a rolling release with manual approval stages.

Start a rolling release for a specific deployment.

Using the vercel rolling-release start command to begin a rolling release for a deployment.

Approve the current stage of an active rolling release.

Using the vercel rolling-release approve command to approve the current stage and advance to the next stage.

Abort an active rolling release.

Using the vercel rolling-release abort command to stop an active rolling release.

Complete an active rolling release, promoting the deployment to 100% of traffic.

Using the vercel rolling-release complete command to finish a rolling release and fully promote the deployment.

Fetch details about a rolling release.

Using the vercel rolling-release fetch command to get information about the current rolling release.

These are options that only apply to the command.

The option is used to configure rolling release settings. It accepts a JSON string or the value to turn off rolling releases.

Using the vercel rolling-release configure command with automatic advancement.

The option specifies the deployment ID or URL for rolling release operations.

Using the vercel rolling-release start command with a deployment URL.

The option specifies the current stage index when approving a rolling release stage.

Using the vercel rolling-release approve command with a specific stage index.

This configures a rolling release that starts at 10% traffic, automatically advances after 5 minutes, and then goes to 100%.

This configures a rolling release that starts at 10% traffic and requires manual approval to advance to 100%.

This configures a rolling release with three stages: 10%, 50%, and 100% traffic, each requiring manual approval.

This disables rolling releases for the project.

The following global options can be passed when using the vercel rolling-release command:

For more information on global options and their usage, refer to the options section.

---

## SvelteKit on Vercel

**URL:** https://vercel.com/docs/frameworks/full-stack/sveltekit

**Contents:**
- SvelteKit on Vercel
- Get started with SvelteKit on Vercel
- Deploy a new SvelteKit project with a template
- Use Vercel features with Svelte
  - Install SvelteKit's Vercel adapter plugin
  - Add the Vercel adapter to your Svelte config
- Configure your SvelteKit deployment
  - Configuration options
- Streaming
- Server-Side Rendering

SvelteKit is a frontend framework that enables you to build Svelte applications with modern techniques, such as Server-Side Rendering, automatic code splitting, and advanced routing.

You can deploy your SvelteKit projects to Vercel with zero configuration, enabling you to use Preview Deployments, Web Analytics, Vercel functions, and more.

To get started with SvelteKit on Vercel:

Get started in minutes

SvelteKit Boilerplate

A SvelteKit app including nested routes, layouts, and page endpoints.

SvelteKit Authentication

A SvelteKit app with authentication.

An all-in-one starter kit for high-performance e-commerce sites built with SvelteKit.

Vercel deployments can integrate with your git provider to generate preview URLs for each pull request you make to your SvelteKit project.

When you create a new SvelteKit project with , it installs by default. This adapter detects that you're deploying on Vercel and installs the plugin for you at build time.

We recommend installing the package yourself. Doing so will ensure version stability, slightly speed up your CI process, and allows you to configure default deployment options for all routes in your project.

The following instructions will guide you through adding the Vercel adapter to your SvelteKit project.

You can add the Vercel adapter to your SvelteKit project by running the following command:

Add the Vercel adapter to your file, which should be at the root of your project directory.

You cannot use TypeScript for your SvelteKit config file.

In your file, import from , and add your preferred options. The following example shows the default configuration, which uses the Node.js runtime (which run on Vercel functions).

Learn more about configuring your Vercel deployment in our configuration section below.

You can configure how your SvelteKit project gets deployed to Vercel at the project-level and at the route-level.

Changes to the object you define in will affect the default settings for routes across your whole project. To override this, you can export a object in any route file.

The following is an example of a file that will deploy using server-side rendering in Vercel's Node.js serverless runtime:

You can also configure how individual routes deploy by exporting a object. The following is an example of a route that will deploy on Vercel's Edge runtime:

Learn about all the config options available in the SvelteKit docs. You can also see the type definitions for config object properties in the SvelteKit source code.

SvelteKit's docs have a comprehensive list of all config options available to you. This section will cover a select few options which may be easier to use with more context.

By default, your SvelteKit routes get bundled into one Function when you deploy your project to Vercel. This configuration typically reduces how often your users encounter cold starts.

In most cases, there is no need to modify this option.

Setting in your Svelte config will cause your SvelteKit project's routes to get split into separate Vercel Functions.

Splitting your Functions is not typically better than bundling them. You may want to consider setting if you're experiencing either of the following issues:

Choosing a region allows you to reduce latency for requests to functions. If you choose a Function region geographically near dependencies, or nearest to your visitor, you can reduce your Functions' latency.

By default, your Vercel Functions will be deployed in Washington, D.C., USA, or . Adding a region ID to the array will deploy your Vercel functions there. See our Vercel Function regions docs to learn how to override this settings.

Vercel supports streaming API responses over time with SvelteKit, allowing you to render parts of the UI early, then render the rest as data becomes available. Doing so lets users interact with your app before the full page loads, improving their perception of your app's speed. Here's how it works:

The following example demonstrates a function that will stream its response to the client. To simulate delayed data returned from a promise, it uses a method.

You could then display this data by creating the following file in the same directory:

To summarize, Streaming with SvelteKit on Vercel:

Learn more about Streaming on Vercel.

Server-Side Rendering (SSR) allows you to render pages dynamically on the server. This is useful for pages where the rendered data needs to be unique on every request. For example, verifying authentication or checking the geolocation of an incoming request.

Vercel offers SSR that scales down resource consumption when traffic is low, and scales up with traffic surges. This protects your site from accruing costs during periods of no traffic or losing business during high-traffic periods.

SvelteKit projects are server-side rendered by default. You can configure individual routes to prerender with the page option, or use the same option in your app's root or file to make all your routes prerendered by default.

While server-side rendered SvelteKit apps do support middleware, SvelteKit does not support URL rewrites from middleware.

See the SvelteKit docs on prerendering to learn more.

To summarize, SSR with SvelteKit on Vercel:

Vercel provides a set of System Environment Variables that our platform automatically populates. For example, the variable exposes the Git provider that triggered your project's deployment on Vercel.

These environment variables will be available to your project automatically, and you can enable or disable them in your project settings on Vercel. See our Environment Variables docs to learn how.

SvelteKit allows you to import environment variables, but separates them into different modules based on whether they're dynamic or static, and whether they're private or public. For example, the module exposes environment variables that don't change, and that you should not share publicly.

System Environment Variables are private and you should never expose them to the frontend client. This means you can only import them from or .

The example below exposes , a variable that exposes the name of the branch associated with your project's deployment, to a function for a Svelte layout:

You could reference that variable in a corresponding layout as shown below:

To summarize, the benefits of using Environment Variables with SvelteKit on Vercel include:

Learn more about Environment Variables

Incremental Static Regeneration allows you to create or update content without redeploying your site. When you deploy a route with ISR, Vercel caches the page to serve it to visitors statically, and rebuilds it on a time interval of your choice. ISR has three main benefits for developers: better performance, improved security, and faster build times.

See our ISR docs to learn more.

To deploy a SvelteKit route with ISR:

The following example demonstrates a SvelteKit route that Vercel will deploy with ISR, revalidating the page every 60 seconds, with on-demand revalidation enabled:

Learn more about ISR with SvelteKit.

To summarize, the benefits of using ISR with SvelteKit on Vercel include:

New project deployments can lead to version skew. This can happen when your users are using your app and a new version gets deployed. Their deployment version requests assets from an older version. And those assets from the previous version got replaced. This can cause errors when those active users navigate or interact with your project.

SvelteKit has a skew protection solution. When it detects version skew, it triggers a hard reload of a page to sync to the latest version. This does mean the client-side state gets lost. With Vercel skew protection, client requests get routed to their original deployment. No client-side state gets lost. To enable it, visit the Advanced section of your project settings on Vercel.

Learn more about skew protection with SvelteKit.

To summarize, the benefits of using ISR with SvelteKit on Vercel include:

Learn more about skew protection on Vercel.

Image Optimization helps you achieve faster page loads by reducing the size of images and using modern image formats.

When deploying to Vercel, you can optimize your images on demand, keeping your build times fast while improving your page load performance and Core Web Vitals.

To use Image Optimization with SvelteKit on Vercel, use the within your svelte.config.ts file.

This allows you to specify configuration options for Vercel's native image optimization API.

To use image optimization with SvelteKit, you have to construct your own URLs. You can create a library function that will optimize URLs in production for you like this:

Use an or any other image component with an optimized generated by the function:

To summarize, using Image Optimization with SvelteKit on Vercel:

Learn more about Image Optimization

Vercel's Web Analytics features enable you to visualize and monitor your application's performance over time. The Analytics tab in your project's dashboard offers detailed insights into your website's visitors, with metrics like top pages, top referrers, and user demographics.

To use Web Analytics, navigate to the Analytics tab of your project dashboard on Vercel and select Enable in the modal that appears.

To track visitors and page views, we recommend first installing our package by running the terminal command below in the root directory of your SvelteKit project:

In your SvelteKit project's main file, add the following :

With the above script added to your project, you'll be able to view detailed user insights in your dashboard on Vercel under the Analytics tab. See our docs to learn more about the user metrics you can track with Vercel's Web Analytics.

Your project must be deployed on Vercel to take advantage of the Web Analytics feature. Work on making this feature more broadly available is in progress.

To summarize, using Web Analytics with SvelteKit on Vercel:

Learn more about Web Analytics

You can see data about your project's Core Web Vitals performance in your dashboard on Vercel. Doing so will allow you to track your web application's loading speed, responsiveness, and visual stability so you can improve the user experience.

See our Speed Insights docs to learn more.

To summarize, using Speed Insights with SvelteKit on Vercel:

Learn more about Speed Insights

Draft Mode enables you to view draft content from your Headless CMS immediately, while still statically generating pages in production.

To use a SvelteKit route in Draft Mode, you must:

To render the draft content, SvelteKit will check for . If its value matches the value of , it will render content fetched at request time rather than prebuilt content.

We recommend using a cryptographically secure random number generator at build time as your value. If a malicious actor guesses your , they can view your pages in Draft Mode.

Deployments on Vercel automatically secure Draft Mode behind the same authentication used for Preview Comments. In order to enable or disable Draft Mode, the viewer must be logged in as a member of the Team. Once enabled, Vercel's CDN will bypass the ISR cache automatically and invoke the underlying Vercel Function.

You and your team members can toggle Draft Mode in the Vercel Toolbar in production, localhost, and Preview Deployments. When you do so, the toolbar will become purple to indicate Draft Mode is active.

Users outside your Vercel team cannot toggle Draft Mode.

To summarize, the benefits of using Draft Mode with SvelteKit on Vercel include:

Learn more about Draft Mode

Routing Middleware is useful for modifying responses before they're sent to a user. We recommend using SvelteKit's server hooks to modify responses. Due to SvelteKit's client-side rendering, you cannot use Vercel's Routing Middleware with SvelteKit.

Adding a file to the root directory of your project enables you to rewrite your app's routes.

We do not recommend using rewrites with SvelteKit.

Rewrites from only apply to the Vercel proxy. At runtime, SvelteKit doesn't have access to the rewritten URL, which means it has no way of rendering the intended rewritten route.

See our Frameworks documentation page to learn about the benefits available to all frameworks when you deploy on Vercel.

Learn more about deploying SvelteKit projects on Vercel with the following resources:

---

## vercel curl

**URL:** https://vercel.com/docs/cli/curl

**Contents:**
- vercel curl
- Usage
- Examples
  - Basic request
  - POST request with data
  - Request specific deployment
  - Verbose output
- How it works
- Unique options
  - Deployment

The command is currently in beta. Features and behavior may change.

The command works like , but automatically handles deployment protection bypass tokens for you. When your project has Deployment Protection enabled, this command lets you test protected deployments without manually managing bypass secrets.

The command runs the system command with the same arguments you provide, but adds an header with a valid token. This makes it simple to test API endpoints, check responses, or debug issues on protected deployments.

This command is available in Vercel CLI v48.8.0 and later. If you're using an older version, see Updating Vercel CLI.

Using the vercel curl command to make an HTTP request to a deployment.

Make a GET request to your production deployment:

Making a GET request to the /api/hello endpoint on your production deployment.

Send a POST request with JSON data:

Making a POST request with JSON data to create a new user.

Test a specific deployment by its URL:

Making a request to a specific deployment instead of the production deployment.

See detailed request information:

Using curl's -v flag for verbose output, which shows headers and connection details.

The command requires to be installed on your system.

These are options that only apply to the command.

The option, shorthand , lets you specify a deployment URL to request instead of using the production deployment.

Using the --deployment option to target a specific deployment.

The option, shorthand , lets you provide your own deployment protection bypass secret instead of automatically generating one. This is useful when you already have a bypass secret configured.

Using the --protection-bypass option with a manual secret.

You can also use the environment variable:

Setting the bypass secret as an environment variable.

Make sure is installed on your system:

Installing curl on different operating systems.

Make sure you're in a directory with a linked Vercel project and that the project has at least one deployment:

Linking your project and creating a deployment.

If automatic token creation fails, you can create a bypass secret manually in the Vercel Dashboard:

When using , verify that:

The following global options can be passed when using the vercel curl command:

For more information on global options and their usage, refer to the options section.

---

## Draft Mode

**URL:** https://vercel.com/docs/draft-mode

**Contents:**
- Draft Mode
- How Draft Mode works
- Getting started
- Sharing drafts

Draft Mode lets you view your unpublished headless CMS content on your website rendered with all the normal styling and layout that you would see once published.

Both Next.js and SvelteKit support Draft Mode. Any framework that uses the Build Output API can support Draft Mode by adding the option to prerender configuration.

Draft Mode was called Preview Mode before the release of Next.js 13.4. The name was changed to avoid confusion with preview deployments, which is a different product.

You can use Draft Mode if you:

Draft Mode allows you to bypass ISR caching to fetch the latest CMS content at request time. This is useful for seeing your draft content on your website without waiting for the cache to refresh, or manually revalidating the page.

The process works like this:

Once implemented, team members can access Draft Mode from the Vercel Toolbar by selecting the eye icon . Once selected, the toolbar will turn purple to indicate that Draft Mode is enabled.

To share a draft URL, it must have the query parameter. For example:

Viewers outside your Vercel team cannot enable Draft Mode or see your draft content, even with a draft URL.

---

## vercel git

**URL:** https://vercel.com/docs/cli/git

**Contents:**
- vercel git
- Usage
- Unique Options
  - Yes
- Global Options

The command is used to manage a Git provider repository for a Vercel Project, enabling deployments to Vercel through Git.

When run, Vercel CLI searches for a local config file containing at least one remote URL. If found, you can connect it to the Vercel Project linked to your directory.

Learn more about using Git with Vercel.

Using the vercel git command to connect a Git provider repository from your local Git config to a Vercel Project.

Using the vercel git command to disconnect a connected Git provider repository from a Vercel Project.

These are options that only apply to the command.

The option can be used to skip connect confirmation.

Using the vercel git connect command with the --yes option.

The following global options can be passed when using the vercel git command:

For more information on global options and their usage, refer to the options section.

---

## Using Comments with Preview Deployments

**URL:** https://vercel.com/docs/comments/using-comments

**Contents:**
- Using Comments with Preview Deployments
- Add comments
  - Mention users
  - Add emojis to a comment
  - Add screenshots to a comment
  - Use Markdown in a comment
  - Supported markdown formatting options
- Comment threads
  - Thread filtering
  - Copy comment links

You must be logged in to create a comment. You can press to enable the comment placement cursor.

Alternatively, select the Comment option in the toolbar menu. You can then select a location to place your comment with your cursor.

You can use to mention team members and alert them to your comment. For example, you might want to request Jennifer's input by writing "Hey @Jennifer, how do you feel about this?"

You can add emojis by entering (the colon symbol) into your comment input box, then entering the name of the emoji. For example, add a smile by entering . As you enter the name of the emoji you want, suggestions will be offered in a popup modal above the input box. You can select one of the suggestions with your cursor.

To add a reaction, select the emoji icon to the right of the name of the commenter whose comment you want to react to. You can then search for the emoji you want to react with.

Custom emoji from your Slack organization are supported when you integrate the Vercel Slack app.

You can add screenshots to a comment in any of the following ways:

The latter two options are only available to users with the browser extension installed.

Markdown is a markup language that allows you to format text, and you can use it to make your comments more readable and visually pleasing.

Supported formatting includes:

Every new comment placed on a page begins a thread. The comment author, PR owner, and anyone participating in the conversation will see the thread listed in their Inbox.

The Inbox can be opened by selecting the Inbox option in the toolbar menu. A small badge will indicate if any comments have been added since you last checked. You can navigate between threads using the up and down arrows near the top of the inbox.

You can move the Inbox to the left or right side of the screen by selecting the top of the Inbox modal and dragging it.

You can filter threads by selecting the branch name at the top of the Inbox. A modal will appear, with the following filter options:

You can copy a link to a comment in two ways:

---

## Managing microfrontends

**URL:** https://vercel.com/docs/microfrontends/managing-microfrontends

**Contents:**
- Managing microfrontends
- Adding microfrontends
- Removing microfrontends
- Fallback environment
  - Project domains for git branches
- Sharing settings between microfrontends
  - Sharing environment variables
- Optimizing navigation's between microfrontends
- Observability data routing

With a project's Microfrontends settings of the Vercel dashboard, you can:

You can also use the Vercel Toolbar to manage microfrontends.

To add projects to a microfrontends group:

These changes will take effect on the next deployment.

To remove projects from a microfrontends group:

Make sure that no other microfrontend is referring to this project. These changes will take effect on the next deployment.

Projects that are the default application for the microfrontends group can only be removed after all other projects in the group have been removed. A microfrontends group can be deleted once all projects have been removed.

This setting only applies to preview and custom environments. Requests for the production environment are always routed to the production deployment for each microfrontend project.

When microfrontend projects are not built for a commit in preview or custom environments, Vercel will route those requests to a specified fallback so that requests in the entire microfrontends group will continue to work. This allows developers to build and test a single microfrontend without having to build other microfrontends.

There are three options for the fallback environment setting:

This table illustrates the different fallback scenarios that could arise:

If the current environment is , requests will always be routed to the environment of the other project.

If using the or options, you may need to make sure that those environments have a deployment to fall back to. For example, if using the option, each project in the microfrontends group will need to have a Custom Environment with the specified name. If environments are not configured correctly, you may see a MICROFRONTENDS_MISSING_FALLBACK_ERROR on the request.

To configure this setting, visit the Settings tab for the microfrontends group and configure the Fallback Environment setting.

If your project has a project domain assigned to a Git branch, and the fallback environment is set to , deployments on that branch will use the branch's project domain as the fallback environment instead of the production branch (e.g. ).

To use that branch across the microfrontends group, add a project domain for the branch to every project in the group.

To share settings between Vercel microfrontend projects, you can use the Vercel Terraform Provider to synchronize across projects.

Shared Environment Variables allow you to manage a single secret and share it across multiple projects seamlessly.

To use environment variables with the same name but different values for different project groups, you can create a shared environment variable with a unique identifier (e.g., ). Then, map it to the desired variable (e.g., ) in your file or build command.

Navigations between different top level microfrontends will introduce a hard navigation for users. Vercel optimizes these navigations by automatically prefetching and prerendering these links to minimize any user-visible latency.

Then in all microfrontends, use the component from anywhere you would use a normal link to automatically use the prefetching and prerendering optimizations.

When using this feature, all paths from the file will be visible on the client side. This information is used to know which microfrontend each link comes from in order to apply prefetching and prerendering.

By default, observability data from Speed Insights and Analytics is routed to the default application. You can view this data in the Speed Insights and Analytics tabs of the Vercel project for the microfrontends group's default application.

Microfrontends also provides an option to route a project's own observability data directly to that Vercel project's page.

Enabling or disabling this feature will not move existing data between the default application and the individual project. Historical data will remain in place.

If you are using Turborepo with , you need to either add and to the allowed env variables or set to . See documentation for more information.

---

## Framework environment variables

**URL:** https://vercel.com/docs/environment-variables/framework-environment-variables

**Contents:**
- Framework environment variables
- Using prefixed framework environment variables locally
- Framework environment variables
  - NEXT_PUBLIC_VERCEL_ENV
  - NEXT_PUBLIC_VERCEL_TARGET_ENV
  - NEXT_PUBLIC_VERCEL_URL
  - NEXT_PUBLIC_VERCEL_BRANCH_URL
  - NEXT_PUBLIC_VERCEL_PROJECT_PRODUCTION_URL
  - NEXT_PUBLIC_VERCEL_GIT_PROVIDER
  - NEXT_PUBLIC_VERCEL_GIT_REPO_SLUG

Frameworks typically use a prefix in order to expose environment variables to the browser.

The following prefixed environment variables will be available during the build step, based on the project's selected framework preset.

Many frontend frameworks require prefixes on environment variable names to make them available to the client, such as for Next.js or for SvelteKit. Vercel adds these prefixes automatically for your production and preview deployments, but not for your local development environment.

Framework environment variables are not prefixed when pulled into your local development environment with . For example, will not be prefixed to .

To use framework-prefixed environment variables locally:

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

The environment that the app is deployed and running on. The value can be either production, preview, or development.

The system or custom environment that the app is deployed and running on. The value can be either production, preview, development, or the name of a custom environment.

The domain name of the generated deployment URL. Example: *.vercel.app. The value does not include the protocol scheme https://.

The domain name of the generated Git branch URL. Example: *-git-*.vercel.app. The value does not include the protocol scheme https://.

A production domain name of the project. We select the shortest production custom domain, or vercel.app domain if no custom domain is available. Note, that this is always set, even in preview deployments. This is useful to reliably generate links that point to production such as OG-image URLs. The value does not include the protocol scheme https://.

The Git Provider the deployment is triggered from.

The origin repository the deployment is triggered from.

The account that owns the repository the deployment is triggered from.

The ID of the repository the deployment is triggered from.

The git branch of the commit the deployment was triggered by.

The git SHA of the commit the deployment was triggered by.

The message attached to the commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username attached to the author of the commit that the project was deployed by.

The name attached to the author of the commit that the project was deployed by.

The pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

**Examples:**

Example 1 (bash):
```bash
NEXT_PUBLIC_VERCEL_ENV=production
```

Example 2 (bash):
```bash
NEXT_PUBLIC_VERCEL_ENV=production
```

Example 3 (bash):
```bash
NEXT_PUBLIC_VERCEL_TARGET_ENV=production
```

Example 4 (bash):
```bash
NEXT_PUBLIC_VERCEL_TARGET_ENV=production
```

---

## Cache-Control headers

**URL:** https://vercel.com/docs/headers/cache-control-headers

**Contents:**
- Cache-Control headers
- Default value
- Recommended settings
  - example
  - SWR example
- Using
- CDN-Cache-Control Header
- Behavior
- Cache-Control comparison tables
  - Functions have priority over config files

You can control how Vercel's CDN caches your Function responses by setting a Cache-Control headers header.

The default value is which instructs both the CDN and the browser not to cache.

We recommend that you set your cache to, adjusting 86400 to the number of seconds you want the response cached. This configuration tells browsers not to cache, allowing Vercel's CDN to cache responses and invalidate them when deployments update.

This directive sets the number of seconds a response is considered "fresh" by the CDN. After this period ends, Vercel's CDN will serve the "stale" response from the edge until the response is asynchronously revalidated with a "fresh" response to your Vercel Function.

is consumed by Vercel's proxy and not included as part the final HTTP response to the client.

The following example instructs the CDN to cache the response for 60 seconds. A response can be cached a minimum of second and maximum of seconds (1 year).

This directive allows you to serve content from the Vercel CDN cache while simultaneously updating the cache in the background with the response from your function. It is useful when:

is consumed by Vercel's proxy and not included as part the final HTTP response to the client. This allows you to deliver the latest content to your visitors right after creating a new deployment (as opposed to waiting for browser cache to expire). It also prevents content-flash.

The following example instructs the CDN to:

The first request is served synchronously. Subsequent requests are served from the cache and revalidated asynchronously if the cache is "stale".

If you need to do a synchronous revalidation you can set the header along with the header. This can be used to understand how long the background revalidation took. It sets the header to .

Many browser developer tools set by default, which reveals the true load time of the page with the synchronous update to the cache.

This directive is currently not supported. is consumed by Vercel's proxy, and will not be included in the HTTP response sent to the client.

This directive is currently not supported.

Using the directive specifies that the response can only be cached by the client and not by Vercel's CDN. Use this directive when you want to cache content on the user's browser, but prevent caching on Vercel's CDN.

When Vercel's CDN receives a request with (such as when the browser devtools are open), it will revalidate any stale resource synchronously, instead of in the background.

Sometimes the directives you set in a header can be interpreted differently by the different CDNs and proxies your content passes through between the origin server and a visitor's browser. To explicitly control caching you can use targeted cache control headers.

The and headers are response headers that can be used to specify caching behavior on the CDN.

You can use the same directives as , but is only used by the CDN.

Origins can set the following headers:

When multiple of the above headers are set, Vercel's CDN will use the following priority to determine the caching behavior:

is exclusive to Vercel and has top priority, whether it's defined in a Vercel Function response or a file. It controls caching behavior only within Vercel's Cache. It is removed from the response and not sent to the client or any CDNs.

is second in priority after , and always overrides headers, whether defined in a Vercel Function response or a file.

By default, configures Vercel's Cache and is used by other CDNs, allowing you to configure intermediary caches. If is also set, only influences other CDN caches.

is a web standard header and last in priority. If neither nor are set, this header will be used by Vercel's Cache before being forwarded to the client.

You can still set while using the other two, and it will be forwarded to the client as is.

If only is used, Vercel strips the directive from the header before it's sent to the client.

The following tables demonstrate how Vercel's Cache behaves in different scenarios:

headers returned from Vercel Functions take priority over headers from or files.

has priority over , even if defined in or .

has priority over both and . It only applies to Vercel, so it is not returned with the other headers, which will control cache behavior on the browser and other CDNs.

The following example demonstrates headers that instruct:

Using configuration, you can assign custom headers to each response.

Custom headers can be configured with the property in for Next.js projects, or it can be configured in for all other projects.

Alternatively, a Vercel Function can assign headers to the Response object.

Response headers , , and are reserved and cannot be modified.

---

## vercel list

**URL:** https://vercel.com/docs/cli/list

**Contents:**
- vercel list
- Usage
- Extended Usage
- Unique Options
  - Meta
  - Policy
  - Yes
  - Status
  - environment
- Global Options

The command, which can be shortened to , provides a list of recent deployments for the currently-linked Vercel Project.

Using the vercel list command to retrieve information about multiple deployments for the currently-linked Vercel Project.

Using the vercel list command to retrieve information about deployments for a specific Vercel Project.

Using the vercel list command to retrieve information about deployments filtered by status.

Using the vercel list command to retrieve information about deployments filtered by metadata.

Using the vercel list command to retrieve information about deployments including retention policy.

These are options that only apply to the command.

The option, shorthand , can be used to filter results based on Vercel deployment metadata.

Using the vercel list command with the --meta option.

To see the meta values for a deployment, use GET /deployments/{idOrUrl} .

The option, shorthand , can be used to display expiration based on Vercel project deployment retention policy.

Using the vercel list command with the --policy option.

The option can be used to skip questions you are asked when setting up a new Vercel Project. The questions will be answered with the default scope and current directory for the Vercel Project name and location.

Using the vercel list command with the --yes option.

The option, shorthand , can be used to filter deployments by their status.

Using the vercel list command with the --status option to filter by a single status.

You can filter by multiple status values using comma-separated values:

Using the vercel list command to filter by multiple status values.

The supported status values are:

Use the option to list the deployments for a specific environment. This could be production, preview, or a custom environment.

The following global options can be passed when using the vercel list command:

For more information on global options and their usage, refer to the options section.

---

## Domain management for multi-tenant

**URL:** https://vercel.com/docs/multi-tenant/domain-management

**Contents:**
- Domain management for multi-tenant
- Using wildcard domains
- Offering custom domains
- Adding a domain programmatically
- Verifying domain ownership
- Handling redirects and apex domains
  - Redirecting between apex and "www"
  - Avoiding duplicate content across subdomains
- Deleting or removing domains
- Troubleshooting common issues

Learn how to programmatically manage domains for your multi-tenant application using Vercel for Platforms.

If you plan on offering subdomains like , add a wildcard domain to your Vercel project. This requires using Vercel's nameservers so that Vercel can manage the DNS challenges necessary for generating wildcard SSL certificates.

Now, any you create—whether it's or —automatically resolves to your Vercel deployment. Vercel issues individual certificates for each subdomain on the fly.

You can also give tenants the option to bring their own domain. In that case, you'll want your code to:

You can add a new domain through the Vercel SDK. For example:

Once the domain is added, Vercel attempts to issue an SSL certificate automatically.

If the domain is already in use on Vercel, the user needs to set a TXT record to prove ownership of it.

You can check the verification status and trigger manual verification:

Some tenants might want to redirect automatically to their apex domain , or the other way around.

This ensures a consistent user experience and prevents issues with duplicate content.

If you offer both and for the same tenant, you may want to redirect the subdomain to the custom domain (or vice versa) to avoid search engine duplicate content. Alternatively, set a canonical URL in your HTML to indicate which domain is the "official" one.

If a tenant cancels or no longer needs their custom domain, you can remove it from your Vercel account using the SDK:

The first call disassociates the domain from your project, and the second removes it from your account entirely.

Here are a few common issues you might run into and how to solve them:

DNS propagation delays

After pointing your nameservers to Vercel or adding CNAME records, changes can take 24–48 hours to propagate. Use WhatsMyDNS to confirm updates worldwide.

Forgetting to verify domain ownership

If you add a tenant's domain but never verify it (e.g., by adding a record or using Vercel nameservers), SSL certificates won't be issued. Always check the domain's status in your Vercel project or with the SDK.

Wildcard domain requires Vercel nameservers

If you try to add without pointing to and , wildcard SSL won't work. Make sure the apex domain's nameservers are correctly set.

Exceeding subdomain length for preview URLs

Each DNS label has a 63-character limit. If you have a very long branch name plus a tenant subdomain, the fully generated preview URL might fail to resolve. Keep branch names concise.

Duplicate content SEO issues

If the same site is served from both subdomain and custom domain, consider using canonical tags or auto-redirecting to the primary domain.

A small typo can block domain verification or routing, so double-check your domain spelling.

---

## Working with domains

**URL:** https://vercel.com/docs/domains/working-with-domains

**Contents:**
- Working with domains
- Buying a domain name
  - Buying a domain through Vercel
  - Buying a domain through a third-party
- Domain ownership and Project assignment
- Subdomains, wildcard domains, and apex domains
  - Apex Domain
  - Subdomain
  - Wildcard domain
- Using email with domains

You can buy a domain through Vercel by going to the Vercel.com domains page and using our fast search to find one or more domains that fit your brand and needs. The price of available domains is the same as the registrar's pricing and Vercel does not keep a log of your search history for marketing purposes.

When you create a deployment on Vercel, we automatically assign it a domain based on your project name and ending in . Your site will be available to anyone that you share the domain with. Deployment URLs with the domain are allocated on a first-come, first-served basis and cannot be reserved.

More often than not, you will want to assign a domain to a project that reflects its nature better. You can buy a domain name either through Vercel or through a third-party. Depending on which option you choose, will dictate how and when you'll need to make configurations:

When you buy a domain through Vercel, we configure and set the nameservers, which means you do not need to set any DNS records or make any configurations. It just works. In addition, if you choose to make configurations, such as setting up email, it's all maintained from the Domains tab of your team's dashboard. Finally, all renewals, including domain and SSL certificate renewals are automatically handled by Vercel.

For the ICANN registrant information:

If you enter the same email address you use for your Vercel user account (or an email your team owner uses), the information will be confirmed automatically.

If you enter another email address, please follow the instructions you receive in an email to confirm your registrant information.

If you don't confirm your registrant information, your domain could be suspended (clientHold). You can resend the verification email or update the registrant address from your Domains dashboard if needed.

When you buy a custom domain through a third-party, you can use the add a custom domain workflow to configure the DNS records. If you are using Vercel's nameservers, you can manage certain settings, such as records for email providers or additional DNS records through the Domains tab of your team's dashboard. Otherwise, you must configure nameservers and DNS records through your domain registrar.

When you are using domains with Vercel, there are two areas of the dashboard that you may need to go to in order to configure them correctly. The first relates to your ownership and the second relates to configuring the domain for your Project:

Domain ownership: Domains are owned by a specific team and can be accessed from the Domains tab on your team's dashboard. All your domains, regardless of where they are registered, are listed here and are owned by the owner of the team. If you are using Vercel's nameservers, which is the case by default if you buy your domain through Vercel, you can manage DNS records, custom nameservers, and SSL certificates here. Domains that are registered by a third-party should manage DNS records and nameservers with the third-party.

Project assignment: This is accessed by selecting the project that you wish to assign the domain to and navigating to Settings > Domains. From here you can add an apex domain or subdomain to the Project. When a user visits your domain, they will see the most recent production deployment of your site, unless you assign the domain to a Git branch or add redirection.

When you add a domain to Vercel for the first time, it will appear as an apex domain in your team's Domains tab. If you add that domain (for example, yourdomain.com, or docs.yourdomain.com) to a project on a different Vercel team, that domain will require a TXT Verification step and will only show up at the project level. The apex domain will still appear in the original account's Domains tab.

The apex domain is the root-level domain, such as . When you add an apex domain, Vercel will recommend that you add a redirect to a subdomain. This is because records allow for better control over your domain. Anything configured on the apex domain (for example, cookies or CAA records), will usually apply to all subdomains, rather than setting it on the subdomain, which will only apply to your record. In addition, because Vercel's servers use anycast networking, it can handle CNAME records differently, allowing for quicker DNS resolution and therefore a faster website experience for the end user.

A subdomain is a more specific part of that domain that can be assigned to a particular part of your site, for example, , . This helps to blend both your brand, with the specificity of where the user may need to go. To add a subdomain to your Project, follow the instructions in the Add a custom domain doc. If you have bought the domain through Vercel, you can also point a subdomain to an external service through the Domains section of the dashboard. Subdomains are set through a CNAME DNS record.

You can also configure wildcard domains. Using a wildcard domain, such as , is a way to scale and customize your project on Vercel. Rather than specifying a particular subdomain, you can add a wildcard domain to your project, and then you need to set the nameservers to the intended nameservers, allowing the domain to be resolved. See our multi-tenant SaaS template for an example of using wildcard domains on Vercel.

To add a wildcard domain, follow the steps in Adding a domain.

Wildcard domains must be configured with the nameservers method. This is because in order to generate the wildcard certificates, Vercel needs to be able to set DNS records, since the service that Vercel uses to generate those requires us to solve a challenge to verify ownership.

When you create a domain, you may want to also set up a way for users to contact you through an email address that is pointed at that domain. Vercel does not provide a mail service for domains purchased with or transferred into it.

Because many domain providers do not offer a mail service, several third-party services specifically offer this type of functionality and are enabled by adding MX records. Examples of this type of service include ImproxMX and Forward Email, however there are many more options available. For each provider, different DNS records are required to be added. For information on how to set up email, see How do I send and receive emails with my Vercel purchased domain?

Invalid domain configurations are one of the most common types of domain issues on Vercel. To learn more about other common domain issues, see the troubleshooting doc.

---

## Deployment Protection Exception

**URL:** https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection/deployment-protection-exceptions

**Contents:**
- Deployment Protection Exception
- Adding a Deployment Protection Exception
  - Go to Project Deployment Protection Settings
  - Select Add Domain
  - Specify domain
  - Confirm domain
- Removing a Deployment Protection Exception
  - Go to Project Deployment Protection Settings
  - Select the Domain to Remove
  - Confirm the Domain to Remove

Deployment Protection Exceptions are available on Enterprise plansor with the Advanced Deployment Protection add-on for Pro plans

You can use Deployment Protection Exceptions to disable Deployment Protection (including Vercel Authentication, Password Protection, and Trusted IPs) for a list of preview domains.

When you add a domain to Deployment Protection Exceptions, it will automatically become publicly accessible and will no longer be covered by Deployment Protection features. When you remove a domain from Deployment Protection Exceptions, the domain becomes protected again with the project's Deployment Protection settings.

Deployment Protection Exceptions is designed for Preview Deployment domains, if you wish to make a Production Deployment domain public, see Configuring Deployment Protection.

From your Vercel dashboard:

From the Deployment Protection Exceptions section, select Add Domain:

From the Unprotect Domain modal:

From the Unprotect Domain modal:

All your existing and future deployments for that domain will be unprotected.

From your Vercel dashboard:

From the Deployment Protection Exceptions section:

From the Reprotect Domain modal:

All your existing and future deployments for that domain will be protected.

You can view and manage all the existing Deployment Protection Exceptions for your team in the following way

---

## Managing environment variables

**URL:** https://vercel.com/docs/environment-variables/managing-environment-variables

**Contents:**
- Managing environment variables
- Declare an Environment Variable
- Viewing, editing, or deleting an Environment Variable

Environment variables are key-value pairs configured outside your source code so that each value can change depending on the Environment.

Changes to environment variables are not applied to previous deployments, they only apply to new deployments. You must redeploy your project to update the value of any variables you change in the deployment.

To declare an Environment Variable for your deployment:

From your dashboard, select your project. If necessary, you can also set environment variables team-wide so that they will be available for all projects.

Select the Settings tab.

Go to the Environment Variables section of your Project Settings.

Enter the desired Name for your Environment Variable. For example, if you are using Node.js and you create an Environment Variable named , it will be available under in your code.

Then, enter the Value for your Environment Variable. The value is encrypted at rest so it is safe to add sensitive data like authentication tokens or private keys.

Configure which deployment environment(s) this variable should apply to.

To ensure that the new Environment Variable is applied to your deployment, you must redeploy your project.

To find and view all environment variables.

---

## Logs

**URL:** https://vercel.com/docs/logs

**Contents:**
- Logs
- Build Logs
- Runtime Logs
- Activity Logs
- Audit Logs
- Log Drains

Build Logs are available on all plans

Those with the owner, member, developer role can access this feature

When you deploy your website to Vercel, the platform generates build logs that show the deployment progress. The build logs contain information about:

Learn more about Build Logs.

Runtime Logs are available on all plans

Runtime logs allow you to search, inspect, and share your team's runtime logs at a project level. You can search runtime logs from the deployments section inside the Vercel dashboard. Your log data is retained for 3 days. For longer log storage, you can use Log Drains.

Learn more about Runtime Logs.

Activity Logs provide chronologically organized events on your personal or team account. You get an overview of changes to your environment variables, deployments, and more.

Learn more about Activity Logs.

Audit Logs are available on Enterprise plans

Those with the owner role can access this feature

Audit Logs allow owners to track events performed by other team members. The feature helps you verify who accessed what, for what reason, and at what time. You can export up to 90 days of audit logs to a CSV file.

Learn more about Audit Logs.

Drains are available on Enterprise and Pro plans

Log Drains allow you to export your log data, making it easier to debug and analyze. You can configure Log Drains through the Vercel dashboard or through one of our Log Drains integrations.

Learn more about Log Drains.

---

## Configuring a Build

**URL:** https://vercel.com/docs/builds/configure-a-build

**Contents:**
- Configuring a Build
- Framework Settings
  - Framework Preset
  - Build Command
  - Output Directory
  - Install Command
    - Corepack
    - Custom Install Command for your API
  - Development Command
  - Skip Build Step

When you make a deployment, Vercel builds your project. During this time, Vercel performs a "shallow clone" on your Git repository using the command and fetches ten levels of git commit history. This means that only the latest ten commits are pulled and not the entire repository history.

Vercel automatically configures the build settings for many front-end frameworks, but you can also customize the build according to your requirements.

To configure your Vercel build with customized settings, choose a project from the dashboard and go to its Settings tab.

The Build and Deployment section of the Settings tab offers the following options to customize your build settings:

If you'd like to override the settings or specify a different framework, you can do so from the Build & Development Settings section.

You have a wide range of frameworks to choose from, including Next.js, Svelte, and Nuxt. In several use cases, Vercel automatically detects your project's framework and sets the best settings for you.

Inside the Framework Preset settings, use the drop-down menu to select the framework of your choice. This selection will be used for all deployments within your Project. The available frameworks are listed below:

However, if no framework is detected, "Other" will be selected. In this case, the Override toggle for the Build Command will be enabled by default so that you can enter the build command manually. The remaining deployment process is that for default frameworks.

If you would like to override Framework Preset for a specific deployment, add to your configuration.

Vercel automatically configures the Build Command based on the framework. Depending on the framework, the Build Command can refer to the project’s file.

For example, if Next.js is your framework:

If you'd like to override the Build Command for all deployments in your Project, you can turn on the Override toggle and specify the custom command.

If you would like to override the Build Command for a specific deployment, add to your configuration.

If you update the Override setting, it will be applied on your next deployment.

After building a project, most frameworks output the resulting build in a directory. Only the contents of this Output Directory will be served statically by Vercel.

If Vercel detects a framework, the output directory will automatically be configured.

If you update the Override setting, it will be applied on your next deployment.

For projects that do not require building, you might want to serve the files in the root directory. In this case, do the following:

If you would like to override the Output Directory for a specific deployment, add to your configuration.

Vercel auto-detects the install command during the build step. It installs dependencies from , including (which can be excluded). The install path is set by the root directory.

The install command can be managed in two ways: through a project override, or per-deployment. See manually specifying a package manager for more details.

To learn what package managers are supported on Vercel, see the package manager support documentation.

Corepack is considered experimental and therefore, breaking changes or removal may occur in any future release of Node.js.

Corepack is an experimental tool that allows a Node.js project to pin a specific version of a package manager.

You can enable Corepack by adding an environment variable with name and value to your Project.

Then, set the property in the file in the root of your repository. For example:

A package.json file with pnpm version 7.5.1

The Install Command defined in the Project Settings will be used for front-end frameworks that support Vercel functions for APIs.

If you're using Vercel functions defined in the natively supported directory, a different Install Command will be used depending on the language of the Vercel Function. You cannot customize this Install Command.

This setting is relevant only if you’re using locally to develop your project. Use only if you need to use Vercel platform features like Vercel functions. Otherwise, it's recommended to use the development command your framework provides (such as for Next.js).

The Development Command settings allow you to customize the behavior of . If Vercel detects a framework, the development command will automatically be configured.

If you’d like to use a custom command for vercel dev, you can turn on the Override toggle. Please note the following:

If you would like to override the Development Command, add to your configuration.

Some static projects do not require building. For example, a website with only HTML/CSS/JS source files can be served as-is.

In such cases, you should:

This prevents running the build, and your content is served directly.

In some projects, the top-level directory of the repository may not be the root directory of the app you’d like to build. For example, your repository might have a front-end directory containing a stand-alone Next.js app.

For such cases, you can specify the project Root Directory. If you do so, please note the following:

To configure the Root Directory:

If you update the root directory setting, it will be applied on your next deployment.

In a monorepo, you can skip deployments for projects that were not affected by a commit. To configure:

---

## Preview Deployment Suffix

**URL:** https://vercel.com/docs/deployments/preview-deployment-suffix

**Contents:**
- Preview Deployment Suffix
  - Enabling the Preview Deployment Suffix
  - Disabling the Preview Deployment Suffix
  - Broken Preview Deployment Suffix error

Preview Deployment Suffix is available on Enterprise and Pro plans

Preview Deployment Suffixes allow you to customize the URL of a preview deployment by replacing the default suffix with a custom domain of your choice.

The entered custom domain must be:

Preview Deployment Suffix is included and enabled by default in Enterprise plans

To enable Preview Deployment Suffix, and customize the appearance of any of your generated URLs:

If you are not able to use Vercel's Nameservers, see our guide on how to use a custom domain without Vercel's Nameservers.

See the plans add-ons documentation for information on pricing.

To disable Preview Deployment Suffix:

The next preview deployment generated will revert back to the default suffix.

You may encounter this error if you are using the Preview Deployment Suffix in your team. Make sure that the custom domain you configured is:

The best way to satisfy all of these constraints is to ensure the domain is also added to a project located in the same team. In this project, you can include a single that displays when someone visits the root of the domain.

---

## Log Drains Reference

**URL:** https://vercel.com/docs/drains/reference/logs

**Contents:**
- Log Drains Reference
- Logs Schema
- Format
  - JSON
  - NDJSON
- Log Sources
- Log Environments
- Sampling Rate
- More resources

Log Drains forward logs from your deployments to external endpoints for storage and analysis. You can configure Log Drains in two ways:

Vercel sends logs to endpoints over HTTPS every time your deployments generate logs. Multiple logs may be batched into a single request when possible to optimize delivery performance. In the dashboard, use Additional configuration for logs to control the sources, environments, and sampling rules described below.

The following table describes the possible fields that are sent via Log Drains:

*Required when object is present

Vercel supports the following formats for Log Drains. You can configure the format when configuring the Drain destination:

Vercel sends logs as JSON arrays containing log objects:

Vercel sends logs as newline-delimited JSON objects:

When you configure a Log Drain, select which sources to collect in Additional configuration for logs:

Use the same panel to choose which environments send logs to your drain:

Sampling rules let you control how much log data each drain receives. Use them to send the right volume of data for observability and cost targets. To add sampling rules:

Rules run from top to bottom. Requests that match a rule use that rule’s sampling rate, and any other requests are dropped. If you do not add rules, the drain forwards 100% of data to the destination.

For more information on Log Drains and how to use them, check out the following resources:

---

## Build Output Configuration

**URL:** https://vercel.com/docs/build-output-api/configuration

**Contents:**
- Build Output Configuration
- supported properties
  - version
    - example
  - routes
    - route
        - Source route:
        - Source route:
        - Source route:
        - Source route:

.vercel/output/config.json

Schema (as TypeScript):

The file contains configuration information and metadata for a Deployment. The individual properties are described in greater detail in the sub-sections below.

At a minimum, a file with a property is required.

.vercel/output/config.json

The property indicates which version of the Build Output API has been implemented. The version described in this document is version .

.vercel/output/config.json

vercel/examples/build-output-api/routes

The property describes the routing rules that will be applied to the Deployment. It uses the same syntax as the property of the file.

Routes may be used to point certain URL paths to others on your Deployment, attach response headers to paths, and various other routing-related use-cases.

The routing system has multiple phases. The value indicates the start of a phase. All following routes are only checked in that phase.

The following example shows a routing rule that will cause the path to perform an HTTP redirect to an external URL:

.vercel/output/config.json

vercel/examples/build-output-api/image-optimization

The property defines the behavior of Vercel's native Image Optimization API, which allows on-demand optimization of images at runtime.

The following example shows an image optimization configuration that specifies allowed image size dimensions, external domains, caching lifetime and file formats:

When the property is defined, the Image Optimization API will be available by visiting the path. When the property is undefined, visiting the path will respond with 404 Not Found.

The API accepts the following query string parameters:

.vercel/output/config.json

vercel/examples/build-output-api/wildcard

The property relates to Vercel's Internationalization feature. The way it works is the domain names listed in this array are mapped to the routing variable, which can be referenced by the configuration.

Each of the domain names specified in the configuration will need to be assigned as Production Domains in the Project Settings.

Objects contained within the configuration support the following properties:

The following example shows a wildcard configuration where the matching domain name will be served the localized version of the blog post HTML file:

.vercel/output/config.json

vercel/examples/build-output-api/overrides

The property allows for overriding the output of one or more static files contained within the directory.

The main use-cases are to override the header that will be served for a static file, and/or to serve a static file in the Vercel Deployment from a different URL path than how it is stored on the file system.

Objects contained within the configuration support the following properties:

The following example shows an override configuration where an HTML file can be accessed without the file extension:

.vercel/output/config.json

The property is an array of file paths and/or glob patterns that should be re-populated within the build sandbox upon subsequent Deployments.

Note that this property is only relevant when Vercel is building a Project from source code, meaning it is not relevant when building locally or when creating a Deployment from "prebuilt" build artifacts.

.vercel/output/config.json

The optional property is an object describing the framework of the built outputs.

This value is used for display purposes only.

.vercel/output/config.json

The optional property is an object describing the cron jobs for the production deployment of a project.

---

## Deploying Azure DevOps Pipelines with Vercel

**URL:** https://vercel.com/docs/git/vercel-for-azure-pipelines

**Contents:**
- Deploying Azure DevOps Pipelines with Vercel
- Quickstart
  - Prerequisites
  - Extension and Pipeline set up
  - Create a Vercel Personal Access Token
  - Create secret variables
  - Set up the Vercel Deployment Extension
  - Set up a basic Azure Pipeline
    - Value of
    - Value of

The Vercel Deployment Extension allows you to automatically deploy to Vercel from Azure DevOps Pipelines. You can add the extension to your Azure DevOps Projects through the Visual Studio marketplace.

Once the Vercel extension is set up, your Azure DevOps project is connected to your Vercel Project. You can then use your Azure Pipeline(s) inside your Azure DevOps project to trigger a Vercel Deployment.

This page will help you use the extension in your own use case. You can:

At the end of this quickstart, your Azure DevOps Pipeline will trigger a Vercel production deployment whenever you commit a change to the branch of your code. To get this done, we will follow these steps:

Once you have the Vercel Deployment extension set up, you only need to modify your Azure DevOps Pipeline (Steps 4 and 5) to change the deployment workflow to fit your use case.

An empty Vercel Project with no Git integration

An Azure DevOps project that contains the code that you would like to deploy on Vercel

To create an empty Vercel project:

For security purposes, you should use the above created token in your Azure Pipeline through secret variables.

This step assumes that your code exists as a repository in your Azure Project's Repos and that your Vercel Project is named .

Look for Project ID located on the Vercel Project's Settings page at Project Settings > General.

Your Azure DevOps project is now connected to your Vercel project with automatic production deployments on the branch. You can update or create pipelines in the Azure DevOps project to customize the Vercel deployment behavior by using the options of the Vercel Deployment Extension.

In a production environment, you will often want the following to happen:

Before you update your pipeline file to enable preview deployments, you need to configure Azure DevOps with pull requests.

In order to allow pull requests in your Azure repository to create a deployment and report back with a comment, you need the following:

Create a pull request to the branch. This will trigger the pipeline, run the deployment and comment back on the pull request with the deployment URL.

The creates an output variable called . By setting the of the step to , you can access it using which you can then assign to the input option of the task step.

Here, you can find a list of available properties for each of the available tasks in the Vercel Deployment Extension.

---

## Webhooks API Reference

**URL:** https://vercel.com/docs/webhooks/webhooks-api

**Contents:**
- Webhooks API Reference
- Payload
- Supported Event Types
  - deployment.canceled
  - deployment.check-rerequested
  - deployment.cleanup
  - deployment.created
  - deployment.error
  - deployment.integration.action.cancel
  - deployment.integration.action.cleanup

Vercel Integrations allow you to subscribe to certain trigger-based events through webhooks. An example use-cases for webhooks might be cleaning up resources after someone removes your Integration.

The webhook payload is a JSON object with the following keys.

Occurs whenever a deployment is canceled.

Occurs when a user has requested for a check to be rerun after it failed.

Occurs whenever a deployment is cleaned up after it has been fully removed either due to explicit removal or retention rules.

Occurs whenever a deployment is created.

Occurs whenever a deployment has failed.

Occurs when an integration deployment action or the deployment itself is canceled.

Occurs when a deployment that executed an integration deployment action is cleaned up, such as due to the deployment retention policy.

Occurs when a deployment starts an integration deployment action.

Occurs whenever a deployment is promoted.

This event gets fired after a production deployment is promoted to start serving production traffic. This can happen automatically after a successful build, or after running the promote command.

Occurs whenever a deployment is successfully built and your integration has registered at least one check.

Occurs whenever a deployment is ready.

This event gets fired after all blocking Checks have passed. See deployment-prepared if you registered Checks.

Occurs whenever a domain has been created.

Occurs whenever a domain's auto-renewal setting is changed.

Occurs whenever a new SSL certificate is added for a domain.

Occurs whenever adding a new SSL certificate for a domain fails.

Occurs whenever an SSL certificate is deleted for a domain.

Occurs whenever an SSL certificate is renewed for a domain.

Occurs whenever renewing an SSL certificate for a domain fails.

Occurs whenever DNS records for a domain are modified.

Occurs whenever a domain is renewed.

Occurs whenever a domain renewal fails.

Occurs whenever a domain transfer into Vercel is completed.

Occurs whenever a domain transfer into Vercel fails.

Occurs whenever a domain transfer into Vercel is initiated.

Occurs whenever a domain is added to a project.

Occurs whenever a domain is removed from a project.

Occurs whenever a domain is moved from one project to another.

Occurs whenever a project domain becomes unverified.

Occurs whenever a project domain is updated.

Occurs whenever a project domain is verified.

Occurs whenever the user changes the project permission for an integration.

Occurs whenever an integration has been removed.

Occurs whenever the user confirms pending scope changes.

Occurs whenever the integration installation has been transferred to another team.

Occurs whenever the user connects the integration resource to a project.

Occurs whenever the user disconnects the integration resource to a project.

Occurs when an invoice was created and sent to the customer.

Occurs when an invoice was not paid after a grace period.

Occurs when an invoice was paid.

Occurs when an invoice is refunded.

Occurs whenever a member is added, removed, or their role changed for an installation.

Occurs whenever your project's usage exceeds a dynamic threshold.

See the Alerts documentation for more details and examples.

Occurs whenever your project's error rate (5xx) exceeds a dynamic threshold.

See the Alerts documentation for more details and examples.

Occurs whenever a project has been created.

This event is sent only when the Integration has access to all projects in a Vercel scope.

Occurs whenever a project has been removed.

This event is sent only when the integration has access to all projects in a Vercel scope.

Occurs whenever a rolling release stage is approved and progresses to the next stage.

Occurs whenever a rolling release is completed successfully.

Occurs whenever a rolling release is aborted.

Occurs whenever a rolling release is started.

The legacy webhook payload is a JSON object with the following keys.

The following event types have been deprecated and webhooks that listen for them can no longer be created. Vercel will continue to deliver the deprecated events to existing webhooks.

This event is replaced by deployment.created.

Occurs whenever a deployment is created.

This event is replaced by deployment.succeeded.

Occurs whenever a deployment is ready.

This event gets fired after all blocking checks have passed. See deployment-prepared if you registered Checks.

This event is replaced by deployment.ready.

Occurs whenever a deployment is successfully built and your integration has registered at least one check.

This event is replaced by deployment.canceled.

Occurs whenever a deployment is canceled.

This event is replaced by deployment.error.

Occurs whenever a deployment has failed.

This event is replaced by deployment.check-rerequested.

Occurs when a user has requested for a check to be rerun after it failed.

This event has been removed. deployment.succeeded can be used for the same purpose.

Occurs when all checks for a deployment have completed. This does not indicate that they have all passed, only that they are no longer running. It is possible for webhook to occur multiple times for a single deployment if any checks are re-requested.

Each item in has the following properties:

This event is replaced by project.created.

Occurs whenever a project has been created.

This event is sent only when the Integration has access to all projects in a Vercel scope.

This event is replaced by project.removed.

Occurs whenever a Project has been removed.

This event is sent only when the Integration has access to all Projects in a Vercel scope.

This event is replaced by integration-configuration.removed.

Occurs whenever an integration has been removed.

This event is replaced by integration-configuration.permission-upgraded .

Occurs whenever the user changes the project permission for an integration.

This event is replaced by integration-configuration.scope-change-confirmed .

Occurs whenever the user confirms pending scope changes.

This event is replaced by domain.created.

Occurs whenever a domain has been created.

Once your server is configured to receive payloads, it will listen for any payload sent to the endpoint you configured. By knowing the URL of your webhook, anybody can send you requests. Therefore, it is recommended to check whether the requests are coming from Vercel or not.

The recommended method to check is to use the security header you receive with each request. The value of this header corresponds to the of the request body using your secret key.

For example, you can validate a webhook request as follows:

For enhanced security against timing attacks, use constant-time comparison when verifying the header. See x-vercel-signature in Request Headers.

You can compute the signature using an HMAC hexdigest from the secret token of OAuth2 and request body, then compare it with the value of the header to validate the payload.

You should consider this HTTP request to be an event. Once you receive the request, you should schedule a task for your action.

This request has a timeout of 30 seconds. That means if a HTTP response is not received within 30 seconds, the request will be aborted.

If your HTTP endpoint does not respond with a HTTP status code, we attempt to deliver the webhook event up to 24 hours with an exponential backoff. Events that could not be delivered within 24 hours will not be retried and will be discarded.

---

## Accessing Deployments through Generated URLs

**URL:** https://vercel.com/docs/deployments/generated-urls

**Contents:**
- Accessing Deployments through Generated URLs
- Viewing generated URLs
- URL Components
  - Generated from Git
  - Generated with Vercel CLI
  - Truncation
  - Anti-phishing protection
- Preview Deployment Suffix

When you create a new deployment in either a preview or production environment, Vercel will automatically generate a unique URL in order for you to access that deployment. You can use this URL to access a particular deployment for as long as your set deployment retention policy allows.

This URL is publicly accessible by default, but you can configure it to be private using deployment protection.

The make up of the URL depends on how it was created and if it relates to a branch of a specific commit. To learn more, see URL Components.

You can access these automatically generated URLs in the following ways:

Generated URLs are comprised of several different pieces of data associated with the underlying deployment. Varying combinations of the following information may be used to generate a URL:

When are working with Git, Vercel will automatically generate a URL for the following:

To access the commit URL, click the View deployment button from your pull request. To access the branch URL, click the Visit Preview button from the pull request comment.

To access the URL for a successful deployment from Vercel CLI, you can save the standard output of the deploy command. The generated URL will have the following structure:

Once you deploy to the production environment, the above URL will point to the production deployment.

If the deployment is created on a Team, you can also use the URL specific to the deployment's author. It will have the following structure:

This allows you to stay on top of the latest change deployed by a particular member of a team within a specific project.

If more than 63 characters are present before the suffix (or the respective Preview Deployment Suffix) for a generated URL, they will be truncated.

If your resembles a regular web domain, it may be shortened to avoid that resemblance. For example, would be changed to just . This is done to prevent an accidental trigger of anti-phishing protection built into web browsers that protect the user from visiting domains that look roughly like other domains they visit.

Preview Deployment Suffix is available on Enterprise and Pro plans

Preview Deployment Suffixes allow you to customize the URL of a preview deployment by replacing the default suffix with a custom domain of your choice.

To learn more, see the Preview Deployment Suffix documentation.

---

## Checks API Reference

**URL:** https://vercel.com/docs/checks/checks-api

**Contents:**
- Checks API Reference
  - Create a new check
  - Update a check
  - Get all checks
  - Get one check
  - Rerequest a failed check

API endpoints allow integrations to interact with the Vercel platform. Integrations can run checks every time you create a deployment.

The post and patch endpoints must be called with an OAuth2, or it will produce a 400 error.

Allows the integration to create and register checks. When the "deployment" event triggers, the endpoint registers new checks. It runs until the "deployment.succeeded" event. The endpoint will then set the check "status" to "running".

/v1/deployments/{deploymentId}/checks

Allows the integration to update existing checks with a new status or conclusion. This endpoint sets the status to “completed”. The value for the conclusion can be "canceled", "failed", "neutral", "succeeded", or "skipped".

/v1/deployments/{deploymentId}/checks/{checkId}

Allows integration to fetch all existing checks with all their attributes. For comparison purposes, you can use it to get information from a previous deployment.

/v1/deployments/{deploymentId}/checks

Allows integration to fetch only a single check with all the attributes. For comparison purposes, you can use it to get information from a previous deployment.

/v1/deployments/{deploymentId}/checks/{checkId}

Allows integration to return a new outcome or rewrite an existing check result. This endpoint is used for check reruns.

/v1/deployments/{deploymentId}/checks/{checkId}/rerequest

---

## vercel httpstat

**URL:** https://vercel.com/docs/cli/httpstat

**Contents:**
- vercel httpstat
- Usage
- Examples
  - Basic timing analysis
  - POST request timing
  - Specific deployment timing
  - Multiple requests
- How it works
- Unique options
  - Deployment

The command is currently in beta. Features and behavior may change.

The command works like , but automatically handles deployment protection bypass tokens for you. It provides visualization of HTTP timing statistics, showing how long each phase of an HTTP request takes. When your project has Deployment Protection enabled, this command lets you test protected deployments without manually managing bypass secrets.

The command runs the tool with the same arguments you provide, but adds an header with a valid token. This makes it simple to measure response times, analyze performance bottlenecks, or debug latency issues on protected deployments.

This command is available in Vercel CLI v48.9.0 and later. If you're using an older version, see Updating Vercel CLI.

Using the vercel httpstat command to visualize HTTP timing statistics for a deployment.

Get timing statistics for your production deployment:

Getting timing statistics for the /api/hello endpoint on your production deployment.

Analyze timing for a POST request with JSON data:

Measuring timing statistics for a POST request that creates a new user.

Test timing for a specific deployment by its URL:

Analyzing timing for a specific deployment instead of the production deployment.

Run multiple requests to get average timing statistics:

Running 10 requests to get more reliable timing data.

The command requires to be installed on your system.

These are options that only apply to the command.

The option, shorthand , lets you specify a deployment URL to request instead of using the production deployment.

Using the --deployment option to target a specific deployment.

The option, shorthand , lets you provide your own deployment protection bypass secret instead of automatically generating one. This is useful when you already have a bypass secret configured.

Using the --protection-bypass option with a manual secret.

You can also use the environment variable:

Setting the bypass secret as an environment variable.

The tool displays timing information in a visual format:

Each phase is color-coded and displayed with its duration in milliseconds, helping you identify which part of the request is taking the most time.

Make sure is installed on your system:

Installing httpstat on different systems.

Make sure you're in a directory with a linked Vercel project and that the project has at least one deployment:

Linking your project and creating a deployment.

If automatic token creation fails, you can create a bypass secret manually in the Vercel Dashboard:

When using , verify that:

The following global options can be passed when using the vercel httpstat command:

For more information on global options and their usage, refer to the options section.

---

## Accessing Build Logs

**URL:** https://vercel.com/docs/deployments/logs

**Contents:**
- Accessing Build Logs
- How build logs work?
  - Link to build logs
- Save logs

When you deploy your website to Vercel, the platform generates build logs that show the deployment progress. The build logs contain information about:

Build logs are particularly useful for debugging issues that may arise during deployment. If a deployment fails, these can help you identify the root cause of the issue.

To access build logs, click the Build Logs button from the production deployment tile in the projects overview page.

Build logs are generated at build time for all Deployments. The logs are similar to your framework's Build Command output, with a few minor additions from the Vercel build system. Once a build is complete, no new logs will be recorded.

In addition to the list of build actions, you can also find errors or warnings. These are highlighted with different colors, such as yellow for warnings and red for errors. This color coding makes it flexible to investigate why your build failed and which part of your website is affected. Build logs are stored indefinitely for each deployment.

Build logs will automatically be truncated, if the total size reaches over 4MB.

If you click on the timestamp to the left of the log entry, you get a link to that log entry. This will highlight the selected log and append the line number to the URL as an anchor (). You can then share this link with other team members to point them to a specific line in the log.

You can select multiple lines by holding the key and clicking the timestamps. This will create a link for the content between the first and last lines ().

The log link is only accessible to team members. Anyone who is not a member or has a valid Vercel account cannot access this link.

The link to build logs feature works for logs that are up to 2000 lines long.

You can use Drains to export, store, and analyze your build logs. Log Drains configuration can be accessed through the Vercel dashboard or through one of our Logging integrations.

---

## SAML Single Sign-On

**URL:** https://vercel.com/docs/saml

**Contents:**
- SAML Single Sign-On
- Configuring SAML SSO
- Enforcing SAML
- Authenticating with SAML SSO
  - Customizing the login page
- Managing team members
- SAML providers

SAML is available on Enterprise and Pro plans

Those with the owner role can access this feature

To manage the members of your team through a third-party identity provider like Okta or Auth0, you can set up the Security Assertion Markup Language (SAML) feature from your team's settings.

Once enabled, all team members will be able to log in or access Preview and Production Deployments using your selected identity provider. Any new users signing up with SAML will automatically be added to your team.

For Enterprise customers, you can also automatically manage team member roles and provisioning by setting up Directory Sync.

Pro teams will first need to purchase the SAML SSO add-on from their Billing settings before it can be configured.

For additional security, SAML SSO can be enforced for a team so that all team members cannot access any team information unless their current session was authenticated with SAML SSO.

When modifying your SAML configuration, the option for enforcing will automatically be turned off. Please verify your new configuration is working correctly by re-authenticating with SAML SSO before re-enabling the option.

Once you have configured SAML, your team members can use SAML SSO to log in or sign up to Vercel. To login:

SAML SSO sessions last for 24 hours before users must re-authenticate with the third-party SAML provider.

You can choose to share a Vercel login page that only shows the option to log in with SAML SSO. This prevents your team members from logging in with an account that's not managed by your identity provider.

To use this page, you can set the query param to your team URL. For example:

When using SAML SSO, team members can authenticate through your identity provider, but team membership must be managed manually through the Vercel dashboard.

For automatic provisioning and de-provisioning of team members based on your identity provider, consider upgrading to Directory Sync, which is available on Enterprise plans.

Vercel supports the following third-party SAML providers:

---

## Build Features for Customizing Deployments

**URL:** https://vercel.com/docs/builds/build-features

**Contents:**
- Build Features for Customizing Deployments
- Private npm packages
- Ignored files and folders
- Special paths
  - Source View
  - Logs View
  - Security considerations
- Git submodules

Vercel provides the following features to customize your deployments:

When your project's code is using private modules that require authentication, you need to perform an additional step to install private modules.

To install private modules, define as an Environment Variable in your project. Alternatively, define as an Environment Variable in the contents of the project's npmrc config file that resides at the root of the project folder and is named . This file defines the config settings of at the level of the project.

To learn more, check out the guide here if you need help configuring private dependencies.

Vercel ignores certain files and folders by default and prevents them from being uploaded during the deployment process for security and performance reasons. Please note that these ignored files are only relevant when using Vercel CLI.

A complete list of files and folders ignored by Vercel during the Deployment process.

The directory is not ignored when is used to deploy a prebuilt Vercel Project, according to the Build Output API specification.

You do not need to add any of the above files and folders to your .vercelignore file because it is done automatically by Vercel.

Vercel allows you to access the source code and build logs for your deployment using special pathnames for Build Logs and Source Protection. You can access this option from your project's Security settings.

All deployment URLs have two special pathnames to access the source code and the build logs:

By default, these routes are protected so that they can only be accessed by you and the members of your Vercel Team.

By appending to a Deployment URL or Custom Domain in your web browser, you will be redirected to the Deployment inspector and be able to browse the sources and build outputs.

By appending to a Deployment URL or Custom Domain in your web browser, you can see a real-time stream of logs from your deployment build processes by clicking on the Build Logs accordion.

The pathnames and redirect to and require logging into your Vercel account to access any sensitive information. By default, a third-party can never access your source or logs by crafting a deployment URL with one of these paths.

You can configure these paths to make them publicly accessible under the Security tab on the Project Settings page. You can learn more about making paths publicly accessible in the Build Logs and Source Protection section.

On Vercel, you can deploy Git submodules with a Git provider as long as the submodule is publicly accessible through the HTTP protocol. Git submodules that are private or requested over SSH will fail during the Build step. However, you can reference private repositories formatted as npm packages in your file dependencies. Private repository modules require a special link syntax that varies according to the Git provider. For more information on this syntax, see "How do I use private dependencies with Vercel?".

---

## LangChain

**URL:** https://vercel.com/docs/ai-gateway/framework-integrations/langchain

**Contents:**
- LangChain
- Getting started
  - Create a new project
  - Install dependencies
  - Configure environment variables
  - Create your LangChain application
  - Running the application

LangChain gives you tools for every step of the agent development lifecycle. This guide demonstrates how to integrate Vercel AI Gateway with LangChain to access various AI models and providers.

First, create a new directory for your project and initialize it:

Install the required LangChain packages along with the and packages:

Create a file with your Vercel AI Gateway API key:

If you're using the AI Gateway from within a Vercel deployment, you can also use the environment variable which will be automatically provided.

Create a new file called with the following code:

Run your application using Node.js:

You should see a response from the AI model in your console.

---

## Vercel Authentication

**URL:** https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication

**Contents:**
- Vercel Authentication
- Who can access protected deployments?
- Access requests
- Vercel Authentication security considerations
- Managing Vercel Authentication
  - Manage using the dashboard
  - Go to Project Deployment Protection Settings
  - Manage Vercel Authentication
  - Manage using the API
  - Manage using Terraform

Vercel Authentication is available on all plans

Those with the owner, member and admin roles can manage Vercel Authentication

Vercel Authentication lets you restrict access to your public and non-public deployments. It is the recommended approach to protecting your deployments, and available on all plans. When enabled, it allows only users with deployment access to view and comment on your site.

Users attempting to access the deployment will encounter a Vercel login redirect. If already logged into Vercel, Vercel will authenticate them automatically.

After login, users are redirected and a cookie is set in the browser if they have view access. If the user does not have access to view the deployment, they will be redirected to request access.

Access requests are available on all plans

Those with the owner, member, admin and developer roles can accept or reject access requests

When a Vercel user visits your protected deployment, but they do not have permission to access it, they have the option to request access for their Vercel account. This request triggers an email and Vercel notification to the branch authors.

The access request can be approved or declined. Additionally, granted access can be revoked for a user at any time.

Users granted access can view the latest deployment from a specific branch when logged in with their Vercel account. They can also leave preview Comments if these are enabled on your team.

Those on the Hobby plan can only have one external user per account. If you need more, you can upgrade to a Pro plan.

You can manage access requests in the following way

Access requests can also be managed using the share modal on the deployment page

You can configure Vercel Authentication for different environments, as outlined in Understanding Deployment Protection by environment. This feature works alongside other security measures like Password Protection and Trusted IPs. For specific use-cases, you can bypass Vercel Authentication with methods like Shareable Links or Protection bypass for Automation.

Disabling Vercel Authentication renders all existing deployments unprotected. However, re-enabling it allows previously authenticated users to maintain access without a new login provided they have already authenticated to the specific deployment and have a cookie set in their browser. The authentication token sent as a cookie is restricted to one URL and isn't transferable, even between URLs pointing to the same deployment.

Admins and members can enable or disable Vercel Authentication for their team. Hobby teams can also enable or disable for their own projects. Vercel Authentication is managed on a per-project basis.

You can manage Vercel Authentication through the dashboard, API, or Terraform:

From your Vercel dashboard:

From the Vercel Authentication section:

All your existing and future deployments will be protected with Vercel Authentication for the project. Next time when you access a deployment, you will be asked to log in with Vercel if you aren't already logged in, you will be redirected to the deployment URL and a cookie will be set in your browser for that deployment URL.

You can manage Vercel Authentication using the Vercel API endpoint to update an existing project with the following body

You can configure Vercel Authentication using in the data source in the Vercel Terraform Provider.

---

## Enabling and Disabling Comments

**URL:** https://vercel.com/docs/comments/how-comments-work

**Contents:**
- Enabling and Disabling Comments
  - At the account level
  - At the project level
  - At the session or interface level
  - With environment variables
  - In production and localhost
- Sharing

Comments are enabled by default for all preview deployments on all new projects. By default, only members of your Vercel team can contribute comments.

The comments toolbar will only render on sites with HTML set as the . Additionally, on Next.js sites, the comments toolbar will only render on Next.js pages and not on API routes or static files.

You can enable or disable comments at the account level with certain permissions:

To disable comments for the current browser session, you must disable the toolbar.

You can enable or disable comments for specific branches or environments with preview environment variables.

See Managing the toolbar for more information.

To use comments in a production deployment, or link comments in your local development environment to a preview deployment, see our docs on using comments in production and localhost.

See Managing the toolbar for more information.

To learn how to share deployments with comments enabled, see the Sharing Deployments docs.

---

## Rolling Releases

**URL:** https://vercel.com/docs/rolling-releases

**Contents:**
- Rolling Releases
- Configuring Rolling Releases
- Managing Rolling Releases
  - Starting a rolling release
  - Observability
    - Metrics stored outside of Vercel
  - Advancing a rolling release
  - Aborting a rolling release
- Understanding Rolling Releases
  - Why Rolling Releases needs Skew Protection

Rolling Releases are available on Enterprise and Pro plans

Rolling Releases allow you to roll out new deployments to a small fraction of your users before promoting them to everyone.

Once Rolling Releases is enabled, new deployments won't be immediately served to 100% of traffic. Instead, Vercel will direct a configurable fraction of your visitors, for example, 5%, to the new deployment. The rest of your traffic will be routed to your previous production deployment.

You can leave your rollout in this state for as long as you want, and Vercel will show you a breakdown of key metrics, such as Speed Insights, between the canary and current deployment. You can also compare these deployments with other metrics you gather with your own observability dashboards. When you're ready, or when a configurable period of time has passed, you can promote the prospective deployment to 100% of traffic. At any point, you can use Instant Rollback to revert from the current release candidate.

We highly recommend enabling Skew Protection with Rolling Releases. This ensures that every user, whether they get the prior deployment or the release candidate, communicates with the backend code from the matching deployment. Without Skew Protection, users may experience inconsistencies between client and server versions during rollouts.

Once you've enabled Rolling Releases, you need to configure two or more stages for your release. Stages are the distinct traffic ratios you want to serve as your release candidate rolls out. Each stage must send a larger fraction of traffic to the release candidate. The last stage must always be 100%, representing the full promotion of the release candidate. Many projects only need two stages, with a single fractional stage before final promotion, but you can configure more stages as needed.

A stage configured for 0% of traffic is a special case. Vercel will not automatically direct any visitors to the release candidate in this case, but it can be accessed by forcing a value for the rolling release cookie. See setting the rolling release cookie for more information.

Once Rolling Releases are configured for the project, any subsequent rollout will use the project's current rolling release configuration. Each new rollout clones the rolling release configuration. Therefore, editing the configuration will not impact any rollouts that are currently in progress.

You can manage Rolling releases on the project's settings page or via the API or CLI.

When you enable Rolling Releases in your project's settings, any action that promotes a deployment to production will initiate a new rolling release. This includes:

The rolling release will proceed to its first stage, sending a portion of traffic to the release candidate.

If a rolling release is in progress when one of the promote actions triggers, the project's state won't change. The active rolling release must be resolved (either completed or aborted) before starting a new one.

While a rolling release is in progress, it will be prominently indicated in several locations:

Furthermore, the Observability tab for your project has a Rolling Releases section. This lets you examine Vercel-gathered metrics about the actual traffic mix between your deployments and comparative performance differences between them. You can use these metrics to help you decide whether you want to advance or abort a rolling release.

You may have observability metrics gathered by platforms other than Vercel. To leverage these metrics to help make decisions about rolling releases, you will need to ensure that these metrics can distinguish between behaviors observed on the base deployment and ones on the canary. The easiest way to do this is to propagate Vercel's deployment ID to your other observability systems.

Both the Deployments page and the Rolling Releases Observability tab have controls to change the state of the current release with a button to advance the release to its next stage. If the next stage is the final stage, the release candidate will be fully promoted to be your current production deployment, and the project exits the rolling release state.

If the metrics on the release candidate are unacceptable to you, there are several ways to abort the rolling release:

This will leave your project in a rolled-back state, as with Instant Rollback. When you're ready, you can select any deployment to promote to initiate a new rolling release. The project will exit rollback status once that rolling release completes.

Rolling Releases should work out-of-the-box for most projects, but the implementation details may be significant for some users.

When a user requests a page from a project's production deployment with an active rolling release, Vercel assigns this user to a random bucket that is stored in a cookie on the client. We use client-identifying information such as the client's IP address to perform this bucket assignment. This allows the same device to see the same deployment even when in incognito mode. It also ensures that in race conditions such as multiple simultaneous requests from the same client, all requests resolve to the same target deployment.

Buckets are divided among the two releases at the fraction requested in the current rolling release stage. When the rolling release advances to a later stage, clients assigned to some buckets will now be assigned to a different deployment, and will receive the new deployment at that time.

Note that while we attempt to divide user sessions among the two deployments at the configured fraction, not all users behave the same. If a particularly high-traffic user is placed into one bucket, the observed fraction of total requests between the two deployments may not match the requested fraction. Likewise, note that randomized assignment based on hashing may not achieve precisely the desired diversion rate, especially when the number of sessions is small.

Rolling Releases impact which deployment a user gets when they make a page load. Skew Protection ensures that backend API requests made from a particular deployment are served by a backend implementation from the same deployment.

When a new user loads a page from a project with an active rolling release, they might receive a page from either deployment. Skew Protection ensures that, whichever deployment they are served, their backend calls are consistent with the page that they loaded.

If the rolling release stage is advanced, the user may be eligible for a new deployment. On their next page load or refresh, they will fetch that page from the new deployment. Until they refresh, Skew Protection will continue to ensure that they use backends consistent with the page they are currently on.

You can modify the Rolling Release cookie on a client by issuing a request that includes a special query parameter. Requests that include in the URL will always get the base release for the current rolling release. Likewise, will force the cookie to target the current canary, including for a rolling release stage configured for 0% of traffic.

This forced cookie is good only for the duration of a single rolling release. When that rolling release is completed or aborted and a new rolling release starts, the cookie will get re-processed to a random value.

Be aware that anybody is capable of setting on a URL. 0% canaries are not served by default, but they are not securely hidden from users.

The Rolling Releases REST API allows you to programmatically manage rolling release configurations and monitor active releases. Common use cases include:

For detailed API specifications, request/response schemas, and code examples:

---

## Sharable Links

**URL:** https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection/sharable-links

**Contents:**
- Sharable Links
- Who can create Shareable Links?
- Creating Sharable Links
  - Select your project
  - Select the deployment
  - Click Share button
  - Revoking a Sharable Link
- Managing Shareable Links

Shareable Links are available on all plans

Shareable links allow external users to securely access your deployments through a query string parameter. Shareable links include the ability to leave Comments on deployments which have them enabled.

Users with the Admin, Member, and Developer roles can create or revoke sharable links for their project's deployments. Personal accounts can also manage sharable links for their Hobby deployments.

Developers on the hobby plan can only create one shareable link in total per account.

To manage Sharable Links, do the following:

From your Vercel dashboard:

From the list of Preview Deployments, select the deployment you wish to share.

From the Deployment page, click Share to display the Share popover. From the popover, select Anyone with the link from the dropdown.

To revoke access for users, switch the dropdown option to Only people with access.

If you have also shared the deployment with individual users, you will need to remove them from the Share popover.

You can view and manage all the existing Shareable Links for your team in the following way

---

## Deploying Turborepo to Vercel

**URL:** https://vercel.com/docs/monorepos/turborepo

**Contents:**
- Deploying Turborepo to Vercel
- Deploy Turborepo to Vercel
  - Handling environment variables
  - Import your Turborepo to Vercel
- Using global
- Ignoring unchanged builds
- Setup Remote Caching for Turborepo on Vercel
  - Link your project to the Vercel Remote Cache
  - Test the caching
- Troubleshooting

Turborepo is a high-performance build system for JavaScript and TypeScript codebases with:

And more. Read the Why Turborepo docs to learn about the benefits of using Turborepo to manage your monorepos. To get started with Turborepo in your monorepo, follow Turborepo's Quickstart docs.

Follow the steps below to deploy your Turborepo to Vercel:

It's important to ensure you are managing environment variables (and files outside of packages and apps) correctly.

If your project has environment variables, you'll need to create a list of them in your so Turborepo knows to use different caches for different environments. For example, you can accidentally ship your staging environment to production if you don't tell Turborepo about your environment variables.

Frameworks like Next.js inline build-time environment variables (e.g. ) in bundled outputs as strings. Turborepo will automatically try to infer these based on the framework, but if your build inlines other environment variables or they otherwise affect the build output, you must declare them in your Turborepo configuration.

You can control Turborepo's cache behavior (hashing) based on the values of both environment variables and the contents of files in a few ways. Read the Caching docs on Turborepo for more information.

and key support is available in Turborepo version 1.5 or later. You should update your Turborepo version if you're using an older version.

The following example shows a Turborepo configuration, that handles these suggestions:

In most monorepos, environment variables are usually used in applications rather than in shared packages. To get higher cache hit rates, you should only include environment variables in the app-specific tasks where they are used or inlined.

Once you've declared your environment variables, commit and push any changes you've made. When you update or add new inlined build-time environment variables, be sure to declare them in your Turborepo configuration.

If you haven't already connected your monorepo to Turborepo, you can follow the quickstart on the Turborepo docs to do so.

Create a new Project on the Vercel dashboard and import your Turborepo project.

Vercel handles all aspects of configuring your monorepo, including setting build commands, the Output Directory, the Root Directory, the correct directory for workspaces, and the Ignored Build Step.

The table below reflects the values that Vercel will set if you'd like to set them manually in your Dashboard or in the of your application's directory:

Turborepo is also available globally when you deploy on Vercel, which means that you do not have to add as a dependency in your application.

Thanks to automatic workspace scoping and globally installed turbo, your build command can be as straightforward as:

The appropriate filter will be automatically inferred based on the configured root directory.

To override this behavior and use a specific version of Turborepo, install the desired version of in your project. Learn more

You likely don't need to build a preview for every application in your monorepo on every commit. To ensure that only applications that have changed are built, ensure your project is configured to automatically skip unaffected projects.

You can optionally choose to connect your Turborepo to the Vercel Remote Cache from your local machine, allowing you to share artifacts and completed computations with your team and CI/CD pipelines.

You do not need to host your project on Vercel to use Vercel Remote Caching. For more information, see the Remote Caching doc. You can also use a custom remote cache. For more information, see the Turborepo documentation.

First, authenticate with the Turborepo CLI from the root of your monorepo:

Then, use to link your Turborepo to your remote cache. This command should be run from the root of your monorepo:

Next, into each project in your Turborepo and run to link each directory within the monorepo to your Vercel Project.

As a Team owner, you can also enable caching within the Vercel Dashboard.

Your project now has the Remote Cache linked. Run to see the caching in action. Turborepo caches the filesystem output both locally and remote (cloud). To see the cached artifacts open .

Now try making a change in a file and running again. The builds speed will have dramatically improved. This is because Turborepo will only rebuild the changed files.

To see information about the Remote Cache usage, go to the Artifacts section of the Usage tab.

For Vercel to deploy your application, the outputs need to be present for your Framework Preset after your application builds. If you're getting an error that the outputs from your build don't exist after a cache hit:

Visit the Turborepo documentation to learn more about the key.

When using Turborepo on Vercel, all information used by during the build process is automatically collected to help debug cache misses.

Turborepo Run Summary is only available in Turborepo version or later. To upgrade, use .

To view the Turborepo Run Summary for a deployment, use the following steps:

This opens a view containing a review of the build, including:

If a previous deployment from the same branch is available, the difference between the cache inputs for the current and previous build will be automatically displayed, highlighting the specific changes that caused the cache miss.

This information can be helpful in identifiying exactly why a cache miss occurred, and can be used to determine if a cache miss is due to a change in the project, or a change in the environment.

To change the comparison, select a different deployment from the dropdown, or search for a deployment ID. The summary data can also be downloaded for comparison with a local build.

Environment variable values are encrypted when displayed in Turborepo Run Summary, and can only be compared with summary files generated locally when viewed by a team member with access to the projects environment variables. Learn more

Building a Next.js application that is using Skew Protection always results in a Turborepo cache miss. This occurs because Skew Protection for Next.js uses an environment variable that changes with each deployment, resulting in Turborepo cache misses. There can still be cache hits for the Vercel CDN Cache.

If you are using a version of Turborepo below 2.4.1, you may encounter issues with Skew Protection related to missing assets in production. We strongly recommend upgrading to Turborepo 2.4.1+ to restore desired behavior.

---

## Working with Checks

**URL:** https://vercel.com/docs/checks

**Contents:**
- Working with Checks
- Types of flows enabled by Checks API
- Checks lifecycle
- Checks integrations
  - Install integrations
  - Build your Checks integration

Checks are tests and assertions created and run after every successful deployment. Checks API defines your application's quality metrics, runs end-to-end tests, investigates APIs' reliability, and checks your deployment.

Most testing and CI/CD flows occur in synthetic environments. This leads to false results, overlooked performance degradation, and missed broken connections.

The diagram shows the complete lifecycle of how a check works:

Learn more about this process in the Anatomy of Checks API

You can create a native or connectable account integration that works with the checks API to facilitate testing of deployments for Vercel users.

Vercel users can find and install your integration from the Marketplace under testing, monitoring or observability.

Once you have created your integration, publish it to the marketplace by following these guidelines:

---

## vercel rollback

**URL:** https://vercel.com/docs/cli/rollback

**Contents:**
- vercel rollback
- Usage
- Unique Options
  - Timeout
- Global Options

The command is used to roll back production deployments to previous deployments.

Using vercel rollback fetches the status of any rollbacks in progress.

Using vercel rollback rolls back to previous deployment.

On the hobby plan, you can only roll back to the previous production deployment. If you attempt to pass in a deployment id or url from an earlier deployment, you will be given an error:

To roll back further than the previous production deployment, upgrade to pro

These are options that only apply to the command.

The option is the time that the command will wait for the rollback to complete. It does not affect the actual rollback which will continue to proceed.

When rolling back a deployment, a timeout of will immediately exit after requesting the rollback.

Using the vercel rollback command to the https://example-app-6vd6bhoqt.vercel.app deployment.

The following global options can be passed when using the vercel rollback command:

For more information on global options and their usage, refer to the options section.

---

## Vercel Primitives

**URL:** https://vercel.com/docs/build-output-api/primitives

**Contents:**
- Vercel Primitives
- Static files
  - Configuration
  - Directory structure for static files
- Serverless Functions
  - Serverless function configuration
    - Base config
    - Node.js config
    - Node.js config example
  - Directory structure for Serverless Functions

The following directories, code files, and configuration files represent all Vercel platform primitives. These primitives are the "building blocks" that make up a Vercel Deployment.

Files outside of these directories are ignored and will not be served to visitors.

.vercel/output/static

vercel/examples/build-output-api/static-files

Static files that are publicly accessible from the Deployment URL should be placed in the directory.

These files are served with the Vercel Edge CDN.

Files placed within this directory will be made available at the root () of the Deployment URL and neither their contents, nor their file name or extension will be modified in any way. Sub directories within are also retained in the URL, and are appended before the file name.

There is no standalone configuration file that relates to static files.

However, certain properties of static files (such as the response header) can be modified by utilizing the property of the file.

The following example shows static files placed into the directory:

.vercel/output/functions

vercel/examples/build-output-api/serverless-functions

A Vercel Function is represented on the file system as a directory with a suffix on the name, contained within the directory.

Conceptually, you can think of this directory as a filesystem mount for a Vercel Function: the files below the directory are included (recursively) and files above the directory are not included. Private files may safely be placed within this directory because they will not be directly accessible to end-users. However, they can be referenced by code that will be executed by the Vercel Function.

A directory may be a symlink to another directory in cases where you want to have more than one path point to the same underlying Vercel Function.

A configuration file named must be included within the directory, which contains information about how Vercel should construct the Vercel Function.

The suffix on the directory name is not included as part of the URL path of Vercel Function on the Deployment. For example, a directory located at will be accessible at the URL path of the Deployment.

.vercel/output/functions/<name>.func/.vc-config.json

The configuration file contains information related to how the Vercel Function will be created by Vercel.

This extends the Base Config for Node.js Serverless Functions.

This is what the configuration file could look like in a real scenario:

The following example shows a directory structure where the Vercel Function will be accessible at the URL path of the Deployment:

.vercel/output/functions

vercel/examples/build-output-api/edge-functions

An Edge Function is represented on the file system as a directory with a suffix on the name, contained within the directory.

The directory requires at least one JavaScript or TypeScript source file which will serve as the of the function. Additional source files may also be included in the directory. All imported source files will be bundled at build time.

WebAssembly (Wasm) files may also be placed in this directory for an Edge Function to import. See Using a WebAssembly file for more information.

A configuration file named must be included within the directory, which contains information about how Vercel should configure the Edge Function.

The suffix is not included in the URL path. For example, a directory located at will be accessible at the URL path of the Deployment.

Edge Functions will bundle an and all supported source files that are imported by that . The following list includes all supported content types by their common file extensions.

.vercel/output/functions/<name>.func/.vc-config.json

The configuration file contains information related to how the Edge Function will be created by Vercel.

This is what the configuration file could look like in a real scenario:

The following example shows a directory structure where the Edge Function will be accessible at the URL path of the Deployment:

.vercel/output/functions

vercel/examples/build-output-api/prerender-functions

A Prerender asset is a Vercel Function that will be cached by the Vercel CDN in the same way as a static file. This concept is also known as Incremental Static Regeneration.

On the file system, a Prerender is represented in the same way as a Vercel Function, with an additional configuration file that describes the cache invalidation rules for the Prerender asset.

An optional "fallback" static file can also be specified, which will be served when there is no cached version available.

.vercel/output/functions/<name>.prerender-config.json

The configuration file contains information related to how the Prerender Function will be created by Vercel.

.vercel/output/functions/<name>.prerender-fallback.<ext>

A Prerender asset may also include a static "fallback" version that is generated at build-time. The fallback file will be served by Vercel while there is not yet a cached version that was generated during runtime.

When the fallback file is served, the Vercel Function will also be invoked "out-of-band" to re-generate a new version of the asset that will be cached and served for future HTTP requests.

This is what an file could look like in a real scenario:

The following example shows a directory structure where the Prerender will be accessible at the URL path of the Deployment:

---

## vercel inspect

**URL:** https://vercel.com/docs/cli/inspect

**Contents:**
- vercel inspect
- Usage
- Unique Options
  - Timeout
  - Wait
  - Logs
- Global Options

The command is used to retrieve information about a deployment referenced either by its deployment URL or ID.

You can use this command to view either a deployment's information or its build logs.

Using the vercel inspect command to retrieve information about a specific deployment.

These are options that only apply to the command.

The option sets the time to wait for deployment completion. It defaults to 3 minutes.

Any valid time string for the ms package can be used.

Using the vercel inspect command with the --timeout option.

The option will block the CLI until the specified deployment has completed.

Using the vercel inspect command with the --wait option.

The option, shorthand , prints the build logs instead of the deployment information.

Using the vercel inspect command with the --logs option, to view available build logs.

If the deployment is queued or canceled, there will be no logs to display.

If the deployment is building, you may want to specify option. The command will wait for build completion, and will display build logs as they are emitted.

Using the vercel inspect command with the --logs and --wait options, to view all build logs until the deployement is ready.

The following global options can be passed when using the vercel inspect command:

For more information on global options and their usage, refer to the options section.

---

## Deploying Nx to Vercel

**URL:** https://vercel.com/docs/monorepos/nx

**Contents:**
- Deploying Nx to Vercel
- Deploy Nx to Vercel
  - Ensure your Nx project is configured correctly
  - Import your project
  - Next steps
- Using
- Setup Remote Caching for Nx on Vercel
  - Install the plugin
  - Configure the runner
  - Clear cache and run

Nx is an extensible build system with support for monorepos, integrations, and Remote Caching on Vercel.

Read the Intro to Nx docs to learn about the benefits of using Nx to manage your monorepos.

If you haven't already connected your monorepo to Nx, you can follow the Getting Started on the Nx docs to do so.

To ensure the best experience using Nx with Vercel, the following versions and settings are recommended:

There are also additional settings if you are using Remote Caching

Create a new Project on the Vercel dashboard and import your monorepo project.

Vercel handles all aspects of configuring your monorepo, including setting build commands, the Root Directory, the correct directory for npm workspaces, and the ignored build step.

Your Nx monorepo is now configured and ready to be used with Vercel!

You can now setup Remote Caching for Nx on Vercel or configure additional deployment options, such as environment variables.

provides a way for you to tell Vercel if a build should continue or not. For more details and information on how to use , see the documentation.

Before using remote caching with Nx, do one of the following:

To configure Remote Caching for your Nx project on Vercel, use the plugin.

In your file you will find a field. Update this field so that it's using the installed :

You can specify your and in your nx.json or set them as environment variables.

When deploying on Vercel, these variables will be automatically set for you.

Clear your local cache and rebuild your project.

---

## Notifications

**URL:** https://vercel.com/docs/notifications

**Contents:**
- Notifications
- Receiving notifications
- Basic capabilities
- Managing notifications
  - Notifications for Comments
  - On-demand usage notifications
- Types of notifications
  - Critical notifications
  - Notification details

Notifications are available on all plans

Vercel sends configurable notifications to you through the dashboard and email. These notifications enable you to view and manage important alerts about your deployments, domains, integrations, account, and usage.

There are a number of places where you can receive notifications:

By default, you will receive both web and email notifications for all types of alerts. Push notifications are opt-in per device and are available on desktop and mobile web. You can manage these notifications from the Settings tab, but any changes you make will only affect your notifications.

There are two main ways to interact with web notifications:

You can manage your own notifications by using the following steps:

Any changes you make will only be reflected for your notifications and not for any other members of the team. You cannot configure notifications for other users.

You can receive feedback on your deployments with the Comments feature. When someone leaves a comment, you'll receive a notification on Vercel. You can see all new comments in the Comments tab of your notifications.

Learn more in the Comments docs.

Customizing on-demand usage notifications is available on Pro plans

Those with the owner role can access this feature

You'll receive notifications as you accrue usage past the included amounts for products like Vercel Functions, Image Optimization, and more.

Team owners on the Pro plan can customize which usage categories they want to receive notifications for based on percentage thresholds or absolute dollar values.

Emails are sent out at specific usage thresholds which vary based on the feature and plan you are on.

If you choose to disable notifications, you won't receive alerts for any excessive charges within that category. This may result in unexpected additional costs on your bill. It is recommended that you carefully consider the implications of turning off notifications for any usage thresholds before making changes to your notification settings.

The types of notifications available for you to manage depend on the role you are assigned within your team. For example, someone with a Developer role will only be able to be notified of Deployment failures and Integration updates.

It is not possible to disable all notifications for alerts that are critical to your Vercel workflow. You can opt-out of one specific channel, like email, but not both email and web notifications. This is because of the importance of these notifications for using the Vercel platform. The list below provides information on which alerts are critical.

---

## Project Dashboard

**URL:** https://vercel.com/docs/projects/project-dashboard

**Contents:**
- Project Dashboard
- Project overview
  - Active branches
- Deployments
- Web Analytics and Speed Insights
- Runtime logs
- Storage
- Settings

Each Vercel project has a separate dashboard to configure settings, view deployments, and more.

To get started with a project on Vercel, see Creating a Project or create a new project with one of our templates.

The Project Overview tab provides an overview of your production deployment, including its active Git branches, build logs, runtime logs, associated domains, and more.

The Project Overview's Active Branches gives you a quick view of your project's branches that are being actively committed to. The metadata we surface on these active branches further enables you to determine whether there's feedback to resolve or a deployment that needs your immediate attention.

If your project isn't connected to a Git provider, you'll see a Preview Deployments section where Active Branches should be.

You can filter the list of active branches by a search term, and see the status of each branch's deployment at a glance with the colored circle icon to the left of the branch name.

From the Active Branches section, you can:

The project dashboard lets you manage all your current and previous deployments associated with your project. To manage a deployment, select the project in the dashboard and click the Deployments tab from the top navigation.

You can sort your deployments by branch, or by status. You can also interact with your deployment by redeploying it, inspecting it, assigning it a domain, and more.

See our docs on managing deployments to learn more.

You can learn about your site's performance metrics with Speed Insights. When enabled, this dashboard displays in-depth information about scores and individual metrics without the need for code modifications or leaving the Vercel dashboard.

Through Web Analytics, Vercel exposes data about your audience, such as the top pages, top referrers, and visitor demographics.

The Logs tab inside your project dashboard allows you to view, search, inspect, and share your runtime logs without any third-party integration. You can filter and group your runtime logs based on the relevant fields.

Learn more in the runtime logs docs.

The Storage tab lets you manage storage products connected to your project, including:

Learn more in our storage docs.

The Settings tab lets you configure your project. You can change the project's name, specify its root directory, configure environment variables and more directly in the dashboard.

Learn more in our project settings docs.

---

## Methods to Protect Deployments

**URL:** https://vercel.com/docs/deployment-protection/methods-to-protect-deployments

**Contents:**
- Methods to Protect Deployments
  - Vercel Authentication
  - Password Protection
  - Trusted IPs
- More resources

Vercel offers three methods for protecting your deployments. Depending on your use case, you can choose to protect a single environment, or multiple environments. See Understanding Deployment Protection by environment for more information.

You can see an overview of your projects' protections in the following way

Vercel Authentication is available on all plans

With Vercel Authentication you can restrict access to all deployments (including non-public deployments), meaning only those with a Vercel account on your team, or those you share a Sharable Link with, can access non-public urls, such as .

When a Vercel user visits your protected deployment, but they do not have permission to access it, they have the option to request access for their Vercel account. This request triggers an email and Vercel notification to the branch authors.

Learn more about Vercel Authentication and how to enable it.

Password Protection is available on Enterprise plansor with the Advanced Deployment Protection add-on for Pro plans

Password Protection on Vercel lets you restrict access to both non-public, and public deployments depending on the type of environment protection you choose.

Learn more about Password Protection and how to enable it.

Trusted IPs are available on Enterprise plans

Trusted IPs restrict deployment access to specified IPv4 addresses and CIDR ranges, returning a 404 for unauthorized IPs. This protection feature is suitable for limiting access through specific paths like VPNs or external proxies.

Learn more about Trusted IPs and how to enable it.

---

## Deploying Bitbucket Projects with Vercel

**URL:** https://vercel.com/docs/git/vercel-for-bitbucket

**Contents:**
- Deploying Bitbucket Projects with Vercel
- Supported Bitbucket Products
- Deploying a Bitbucket Repository
- Changing the Bitbucket Repository of a Project
  - A Deployment for Each Push
  - Updating the Production Domain
  - Preview URLs for Each Pull Request
  - System environment variables
  - VERCEL_GIT_PROVIDER
  - VERCEL_GIT_REPO_SLUG

Vercel for Bitbucket automatically deploys your Bitbucket projects with Vercel, providing Preview Deployment URLs, and automatic Custom Domain updates.

The Deploying a Git repository guide outlines how to create a new Vercel Project from a Bitbucket repository, and enable automatic deployments on every branch push.

If you'd like to connect your Vercel Project to a different Bitbucket repository or disconnect it, you can do so from the Git section in the Project Settings.

Vercel for Bitbucket will deploy each push by default. This includes pushes and pull requests made to branches. This allows those working within the project to preview the changes made before they are pushed to production.

With each new push, if Vercel is already building a previous commit on the same branch, the current build will complete and any commit pushed during this time will be queued. Once the first build completes, the most recent commit will begin deployment and the other queued builds will be cancelled. This ensures that you always have the latest changes deployed as quickly as possible.

If Custom Domains are set from a project domains dashboard, pushes and merges to the Production Branch (commonly "main") will be made live to those domains with the latest deployment made with a push.

If you decide to revert a commit that has already been deployed to production, the previous Production Deployment from a commit will automatically be made available at the Custom Domain instantly; providing you with instant rollbacks.

The latest push to any pull request will automatically be made available at a unique preview URL based on the project name, branch, and team or username. These URLs will be given through a comment on each pull request.

You may want to use different workflows and APIs based on Git information. To support this, the following System Environment Variables are exposed to your Deployments:

The Git Provider the deployment is triggered from. In the case of Bitbucket, the value is always bitbucket.

The slug of the Bitbucket repository that was deployed.

The Bitbucket user or team that the project belongs to.

The ID of the Bitbucket repository the deployment is triggered from.

The Bitbucket branch that the deployment was triggered by.

The Bitbucket sha of the commit the deployment was triggered by.

The message accompanying the Bitbucket commit that was deployed. The message is truncated if it exceeds 2048 bytes.

The name of the commit author on Bitbucket.

Bitbucket profile URL of the commit author.

The Bitbucket pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

We require some permissions through our Vercel for Bitbucket integration. Below are listed the permissions required and a description for what they are used for.

Repository permissions allow us to interact with repositories belonging to or associated with (if permitted) the connected account.

Organization permissions allow us to offer an enhanced experience through information about the connected organization.

User permissions allow us to offer an enhanced experience through information about the connected user.

We use the permissions above in order to provide you with the best possible deployment experience. If you have any questions or concerns about any of the permission scopes, please contact Vercel Support.

To sign up on Vercel with a different Bitbucket account, sign out of your current Bitbucket account. Then, restart the Vercel signup process.

When importing or connecting a Bitbucket repository, we require that you have Admin access to the corresponding repository, so that we can configure a webhook and automatically deploy pushed commits.

If a repository is missing when you try to import or connect it, make sure that you have Admin access configured for the repository.

By default, comments from the Vercel bot will appear on your pull requests and commits. You can silence these comments in your project's settings:

It is currently not possible to prevent comments for specific branches.

You can use Bitbucket Pipelines to build and deploy your Vercel Application.

allows you to build your project inside Bitbucket Pipelines, without exposing your source code to Vercel. Then, skips the build step on Vercel and uploads the previously generated folder to Vercel from the Bitbucket Pipeline.

Learn more about how to configure Bitbucket Pipelines and Vercel for custom CI/CD workflows.

**Examples:**

Example 1 (bash):
```bash
VERCEL_GIT_REPO_SLUG=my-site
```

Example 2 (bash):
```bash
VERCEL_GIT_REPO_SLUG=my-site
```

Example 3 (bash):
```bash
VERCEL_GIT_REPO_OWNER=acme
```

Example 4 (bash):
```bash
VERCEL_GIT_REPO_OWNER=acme
```

---

## Bulk redirects

**URL:** https://vercel.com/docs/redirects/bulk-redirects

**Contents:**
- Bulk redirects
- Using bulk redirects
- Limits and pricing

Bulk Redirects are available on Enterprise and Pro plans

With bulk redirects, you can handle thousands of simple path-to-path or path-to-URL redirects efficiently. Store your redirects in CSV, JSON, or JSONL files and import them using the field in . They are framework agnostic and Vercel processes them before any other route specified in your deployment.

Use bulk redirects when you have thousands of redirects that do not require wildcard or header matching functionality.

can point to either a single file or a folder with up to 100 files. Vercel supports any combination of CSV, JSON, and JSONL files containing redirects, and they can be generated at build time.

Learn more about bulk redirects fields and file formats in the project configuration documentation.

We recommend using status code or to avoid the ambiguity of non methods, which is necessary when your application needs to redirect a public API.

Each project has a free configurable capacity of bulk redirects, and additional bulk redirect capacity can be purchased in groups of 25,000 redirects by going to the Advanced section of your project's settings. At runtime, requests served by bulk redirects are treated like any other request for billing purposes. For more information, see the pricing page.

---

## Runtime Logs

**URL:** https://vercel.com/docs/logs/runtime

**Contents:**
- Runtime Logs
- What are runtime logs?
- Available Log Types
- View runtime logs
- Log filters
  - Timeline
  - Level
  - Function
  - Host
  - Deployment

Runtime Logs are available on all plans

The Logs tab allows you to view, search, inspect, and share your runtime logs without any third-party integration. You can also filter and group your runtime logs based on the relevant fields.

You can only view runtime logs from the Logs tab. Build logs can be accessed from the production deployment tile.

Runtime logs include all logs generated by Vercel Functions invocations in both preview and production deployments. These log results provide information about the output for your functions as well as the output.

You can view the following log types in the Logs tab:

To view runtime logs:

You can use the following filters from the left sidebar to get a refined search experience.

You can filter runtime logs based on a specific timeline. It can vary from the past hour, last 3 days, or a custom timespan depending on your account type. You can use the Live mode option to follow the logs in real-time.

You can filter requests that contain Warning, and Error logs. A request can contain both types of logs at the same time. Streaming functions will always preserve the original intent:

You can filter and analyze logs for one or more functions defined in your project. The log output is generated for the Vercel Functions, and Routing Middleware.

You can view logs for one or more domains and subdomains attached to your team’s project. Alternatively, you can use the Search hosts... field to navigate to the desired host.

Like host and functions, you can filter your logs based on deployments URLs.

Using the resource filter, you can search for requests containing logs generated as a result of:

You can filter your logs based on framework-defined mechanism or rendering strategy used such as API routes, Incremental Static Regeneration (ISR), and cron jobs.

You can filter your logs based on the request method used by a function such as or .

You can filter your logs based on the request path used by a function such as .

You can filter your logs based on the cache behavior such as or . See for the possible values.

You can filter logs to only show requests made from your current browser by clicking the user button. This is helpful for debugging your own requests, especially when there's high traffic volume. The filter works by matching your IP address and User Agent against incoming requests.

The matching is based on your IP address and User Agent. In some cases, this data may not be accurate, especially if you're using a VPN or proxy, or if other people in your network are using the same IP address and browser.

You can use the main search field to filter logs by their messages. In the current search state, filtered log results are sorted chronologically, with the most recent first. Filtered values can also be searched from the main search bar.

This free text search feature is limited to the message and requestPath field. Other fields can be filtered using the left sidebar or the filters in the search bar.

You can view details for each request to analyze and improve your debugging experience. When you click a log from the list, the following details appear in the right sidebar:

Towards the end of the log results window is a button called Show New Logs. By default, it is set to display log results for the past 30 minutes.

Click this button, and it loads new log rows. The latest entries are added based on the selected filters.

You can share a log entry with other team members to view the particular log and context you are looking at. Click on the log you want to share, copy the current URL of your browser, and send it to team members through the medium of your choice.

Logs are streamed. Each output can be up to 256KB, and each request can log up to 1MB of data in total, with a limit of 256 individual log lines per request. If you exceed the log entry limits, you can only query the most recent logs.

Runtime logs are stored with the following observability limits:

Users who have purchased the Observability Plus add-on can view up to 14 consecutive days of runtime logs over the 30 days, providing extended access to historical runtime data for enhanced debugging capabilities.

The above limits are applied immediately when upgrading plans. For example, if you upgrade from Hobby to Pro, you will have access to the Pro plan limits, and access historical logs for up to 1 day.

---

## Vercel CDN Cache

**URL:** https://vercel.com/docs/cdn-cache

**Contents:**
- Vercel CDN Cache
- How to cache responses
  - Using Vercel Functions
  - Using and
  - Static Files Caching
    - Browser
- Cache control options
  - CDN-Cache-Control
  - Vary header
    - Use cases

Vercel's CDN caches your content (including pages, API responses, and static assets) in data centers around the world, closer to your users than your origin server. When someone requests cached content, Vercel serves it from the nearest region, cutting latency, reducing load on your origin, and making your site feel faster everywhere.

CDN caching is available for all deployments and domains on your account, regardless of the pricing plan.

There are two ways to cache content:

To learn about cache keys, manually purging the cache, and the differences between invalidate and delete methods, see Purging Vercel CDN cache

You can cache responses on Vercel with headers defined in:

You can use any combination of the above options, but if you return headers in a Vercel Function, it will override the headers defined for the same route in or .

To cache the response of Functions on Vercel's CDN, you must include headers with any of the following directives:

and are not currently supported.

The following example demonstrates a function that caches its response and revalidates it every 1 second:

For direct control over caching on Vercel and downstream CDNs, you can use CDN-Cache-Control headers.

You can define route headers in or files. These headers will be overridden by headers defined in Function responses.

The following example demonstrates a file that adds headers to a route:

If you're building your app with Next.js, you should use rather than . The following example demonstrates a file that adds headers to a route:

See the Next docs to learn more about .

Static files are automatically cached at the edge on Vercel's CDN for the lifetime of the deployment after the first request.

Where is the number of seconds the response should be cached. The response must also meet the caching criteria.

You can cache dynamic content through Vercel Functions, including SSR, by adding headers to your response. When you specify headers in a function, responses will be cached in the region the function was requested from.

See our docs on Cache-Control headers to learn how to best use directives on Vercel's CDN.

Vercel supports two Targeted Cache-Control headers:

By default, the headers returned to the browser are as follows:

headers are not returned to the browser or forwarded to other CDNs.

To learn how these headers work in detail, see our dedicated headers docs.

The following example demonstrates headers that instruct:

If you set without a , the Vercel CDN strips and from the response before sending it to the browser. To determine if the response was served from the cache, check the header in the response.

The response header instructs caches to use specific request headers as part of the cache key. This allows you to serve different cached responses to different users based on their request headers.

The header only has an effect when used in combination with headers that enable caching (such as ). Without a caching directive, the header has no behavior.

When Vercel's CDN receives a request, it combines the cache key (described in the Cache Invalidation section) with the values of any request headers specified in the header to create a unique cache entry for each distinct combination.

Vercel's CDN already includes the and headers as part of the cache key by default. You do not need to explicitly include these headers in your header.

The most common use case for the header is content negotiation, serving different content based on:

Example: Country-specific content

You can use the header with Vercel's request header to cache different responses for users from different countries:

You can set the header in the same ways you set other response headers:

If you're building your app with Next.js, use :

You can specify multiple headers in a single value by separating them with commas:

This will create separate cache entries for each unique combination of country and language preference.

The field is an HTTP header specifying caching rules for client (browser) requests and server responses. A cache must obey the requirements defined in the header.

For server responses to be successfully cached with Vercel's CDN, the following criteria must be met:

Vercel does not allow bypassing the cache for static files by design.

To learn about cache keys, manually purging the cache, and the differences between invalidate and delete methods, see Purging Vercel CDN Cache.

The header is included in HTTP responses to the client, and describes the state of the cache.

See our headers docs to learn more.

Vercel's Edge Cache is segmented by region. The following caching limits apply to Vercel Function responses:

While you can put the maximum time for server-side caching, cache times are best-effort and not guaranteed. If an asset is requested often, it is more likely to live the entire duration. If your asset is rarely requested (e.g. once a day), it may be evicted from the regional cache.

Vercel does not currently support using and for server-side caching.

---

## Protection Bypass for Automation

**URL:** https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection/protection-bypass-automation

**Contents:**
- Protection Bypass for Automation
- Who can manage protection bypass for automation?
- Using Protection Bypass for Automation
  - Advanced Configuration
  - Examples
    - Playwright

Protection Bypass for Automation is available on all plans

The Protection Bypass for Automation feature lets you bypass Vercel Deployment Protection (Password Protection, Vercel Authentication, and Trusted IPs) for automated tooling (e.g. E2E testing).

The generated secret can be used to bypass deployment protection on all deployments in a project until it is revoked. This value will also be automatically added to your deployments as a system environment variable .

The environment variable value is set when a deployment is built, so regenerating the secret in the project settings will invalidate previous deployments. You will need to redeploy your app if you update the secret in order to use the new value.

To use Protection Bypass for Automation, set an HTTP header (or query parameter) named with the value of the generated secret for the project.

Using a header is strongly recommended, however in cases where your automation tool is unable to specify a header, it is also possible to set the same name and value as a query parameter.

To bypass authorization on follow-up requests (e.g. for in-browser testing) you can set an additional header or query parameter named with the value .

This will set the authorization bypass as a cookie using a redirect with a header.

If you are accessing the deployment through a non-direct way (e.g. in an ) then you may need to further configure by setting the value to .

This will set to on the header, by default is set to .

**Examples:**

Example 1 (unknown):
```unknown
x-vercel-protection-bypass: your-generated-secret (required)
```

Example 2 (unknown):
```unknown
x-vercel-set-bypass-cookie: true (optional)
```

Example 3 (unknown):
```unknown
x-vercel-set-bypass-cookie: samesitenone (optional)
```

Example 4 (typescript):
```typescript
1const config: PlaywrightTestConfig = {2  use: {3    extraHTTPHeaders: {4      'x-vercel-protection-bypass': process.env.VERCEL_AUTOMATION_BYPASS_SECRET,5      'x-vercel-set-bypass-cookie': true | 'samesitenone' (optional)6    }7  }8}
```

---

## Build Output API

**URL:** https://vercel.com/docs/build-output-api

**Contents:**
- Build Output API
- Overview
- Known limitations
- More resources

The Build Output API is a file-system-based specification for a directory structure that can produce a Vercel deployment.

Framework authors can take advantage of framework-defined infrastructure by implementing this directory structure as the output of their build command. This allows the framework to define and use all of the Vercel platform features.

The Build Output API closely maps to the Vercel product features in a logical and understandable format.

It is primarily targeted toward authors of web frameworks who would like to utilize all of the Vercel platform features, such as Vercel Functions, Routing, Caching, etc.

If you are a framework author looking to integrate with Vercel, you can use this reference as a way to understand which files the framework should emit to the directory.

If you are not using a framework and would like to still take advantage of any of the features that those frameworks provide, you can create the directory and populate it according to this specification yourself.

You can find complete examples of Build Output API directories in vercel/examples.

Check out our blog post on using the Build Output API to build your own framework with Vercel.

Native Dependencies: Please keep in mind that when building locally, your build tools will compile native dependencies targeting your machine’s architecture. This will not necessarily match what runs in production on Vercel.

For projects that depend on native binaries, you should build on a host machine running Linux with a CPU architecture, ideally the same as the platform Build Image.

---

## Build Queues

**URL:** https://vercel.com/docs/builds/build-queues

**Contents:**
- Build Queues
- With On-Demand Concurrent Builds
- Without On-Demand Concurrent Builds
- Concurrency queue
  - How concurrent build slots work
- Git branch queue

Build queueing is when a build must wait for resources to become available before starting. This creates more time between when the code is committed and the deployment being ready.

On-Demand Concurrent Builds prevent build queueing so your team can build faster. Vercel dynamically scales the amount of builds that can run simultaneously.

You can choose between two modes:

To configure on-demand concurrent builds, see Project-level on-demand concurrent builds.

If you're experiencing build queues, we strongly recommend enabling On-Demand Concurrent Builds. For billing information, visit the usage and limits section for builds.

When multiple deployments are started concurrently from code changes, Vercel's build system places deployments into one of the following queues:

This queue manages how many builds can run in parallel based on the number of concurrent build slots available to the team. If all concurrent build slots are in use, new builds are queued until a slot becomes available unless you have On-Demand Concurrent Builds enabled at the project level.

Concurrent build slots are the key factor in concurrent build queuing. They control how many builds can run at the same time and ensure efficient use of resources while prioritizing the latest changes.

Each account plan comes with a predefined number of build slots:

Builds are handled sequentially. If new commits are pushed while a build is in progress:

This means that commits in between the current build and most recent commit will not produce builds.

Enterprise users can use Urgent On-Demand Concurrency to skip the Git branch queue for specific builds.

---

## Build with AI on Vercel

**URL:** https://vercel.com/docs/ai

**Contents:**
- Build with AI on Vercel
- Integrating with AI providers
- Using AI integrations
- Featured AI integrations
  - xAIMarketplace native integration
  - GroqMarketplace native integration
  - falMarketplace native integration
  - DeepInfraMarketplace native integration
  - PerplexityMarketplace connectable account
  - ReplicateMarketplace connectable account

AI services and models help enhance and automate the building and deployment of applications for various use cases:

With Vercel AI integrations, you can build and deploy these AI-powered applications efficiently. Through the Vercel Marketplace, you can research which AI service fits your needs with example use cases. Then, you can install and manage two types of AI integrations:

You can view your installed AI integrations by navigating to the AI tab of your Vercel dashboard. If you don't have installed integrations, you can browse and connect to the AI models and services that best fit your project's needs. Otherwise, you will see a list of your installed native and connectable account integrations, with an indication of which project(s) they are connected to. You will be able to browse available services, models and templates below the list of installed integrations.

See the adding a provider guide to learn how to add a provider to your Vercel project, or the adding a model guide to learn how to add a model to your Vercel project.

An AI service with an efficient text model and a wide context image understanding model.

A high-performance AI inference service with an ultra-fast Language Processing Unit (LPU) architecture.

A serverless AI inferencing platform for creative processes.

A platform with access to a vast library of open-source models.

Learn how to integrate Perplexity with Vercel.

Learn how to integrate Replicate with Vercel.

Learn how to integrate ElevenLabs with Vercel.

Learn how to integrate LMNT with Vercel.

Learn how to integrate Together AI with Vercel.

Connect powerful AI models like GPT-4

---

## Setting Up Webhooks

**URL:** https://vercel.com/docs/webhooks

**Contents:**
- Setting Up Webhooks
- Account Webhooks
  - Configure a webhook
  - Go to your team settings
  - Select the events to listen to
    - Deployment Events
    - Project Events
    - Firewall events
  - Choose your target projects
  - Enter your endpoint URL

A webhook is a trigger-based HTTP endpoint configured to receive HTTP POST requests through events. When an event happens, a webhook is sent to another third-party app, which can then take appropriate action.

Webhooks configured with Vercel can trigger a deployment when a specific event occurs. Vercel integrations receive platform events through webhooks.

Account Webhooks are available on Enterprise and Pro plans

Vercel allows you to add a generic endpoint for events from your dashboard. Pro and Enterprise teams will be able to configure these webhooks at the account level.

Choose your team scope on the dashboard, and go to Settings ➞ Webhooks.

The configured webhook listens to one or more events before it triggers the function request. Vercel supports event selections from the following categories:

Configurable webhooks listen to the following deployment-based events:

Project events are only available when "All Team Projects" is selected as the project scope.

Configurable webhooks listen to the following project-based events:

Configurable webhooks listen to the following firewall-based events:

The events you select should depend on your use case and the workflow you want to implement.

After selecting the event types, choose the scope of team projects for which webhooks will listen for events.

The endpoint URL is the destination that triggers the events. All events are forwarded to this URL as a POST request. In case of an event, your webhook initiates an HTTP callback to this endpoint that you must configure to receive data. In order to be accessible, make sure these endpoint URLs are public.

Once you have configured your webhook, click the Create Webhook button.

The Webhook Created dialog will display a secret key, which won't be shown again. You should secure your webhooks by comparing the header of an incoming request with this secret. For integration webhooks, use your Integration Secret (also called Client Secret) from the Integration Console instead. See Securing webhooks to learn how to do this.

Once complete, click Done.

To view all your new and existing webhooks, go to the Webhooks section of your team's dashboard. To remove any webhook, click the cross icon next to the webhook. You can create and use up to 20 custom webhooks per team.

Webhooks can also be created through Integrations. When creating a new integration, you can add webhooks using the Integration Console. Inside your Integration's settings page locate the text field for setting the webhook URL. This is where you should add the HTTP endpoint to listen for events. Next, you can select one or more of these checkboxes to specify which events to listen to.

For native integrations, you can also receive billing-related webhook events such as invoice creation, payment, and refunds. Learn more about working with billing events through webhooks.

The webhook URL receives an HTTP POST request with a JSON payload for each event. All the events have the following format:

Here's a list of supported event types and their .

---

## Add the Vercel Toolbar to your local environment

**URL:** https://vercel.com/docs/vercel-toolbar/in-production-and-localhost/add-to-localhost

**Contents:**
- Add the Vercel Toolbar to your local environment
  - Install the package and link your project
  - Add the toolbar to your project

To enable the toolbar in your local environment, add it to your project using the package, or with an injection script.

Install the package using the following command:

Then link your local project to your Vercel project with the command using Vercel CLI.

---

## Global Vercel CLI Configuration

**URL:** https://vercel.com/docs/project-configuration/global-configuration

**Contents:**
- Global Vercel CLI Configuration
- config.json
  - currentTeam
  - collectMetrics
- auth.json

Using the following files and configuration options, you can configure Vercel CLI under your system user.

The two global configuration files are: and . These files are stored in the directory inside , which defaults to:

These files are automatically generated by Vercel CLI, and shouldn't need to be altered.

This file is used for global configuration of Vercel deployments. Vercel CLI uses this file as a way to co-ordinate how deployments should be treated, consistently.

The first option is a single that gives a description to the file, if a user should find themselves looking through it without context.

You can use the following options to configure all Vercel deployments on your system's user profile:

Valid values: A team ID.

This option tells Vercel CLI which context is currently active. If this property exists and contains a team ID, that team is used as the scope for deployments, otherwise if this property does not exist, the user's Hobby team is used.

Valid values: (default), .

This option defines whether Vercel CLI should collect anonymous metrics about which commands are invoked the most, how long they take to run, and which errors customers are running into.

This file should not be edited manually. It exists to contain the authentication information for the Vercel clients.

In the case that you are uploading your global configuration setup to a potentially insecure destination, we highly recommend ensuring that this file will not be uploaded, as it allows an attacker to gain access to your provider accounts.

---

## vercel deploy

**URL:** https://vercel.com/docs/cli/deploy

**Contents:**
- vercel deploy
- Usage
- Extended usage
- Standard output usage
  - Deploying to a custom domain
- Standard error usage
- Unique options
  - Prebuilt
    - When not to use --prebuilt
  - Build env

The command deploys Vercel projects, executable from the project's root directory or by specifying a path. You can omit 'deploy' in , as is the only command that operates without a subcommand. This document will use 'vercel' to refer to .

Using the vercel command from the root of a Vercel project directory.

Using the vercel command and supplying a path to the root directory of the Vercel project.

Using the vercel command to deploy a prebuilt Vercel project, typically with vercel build. See vercel build and Build Output API for more details.

When deploying, is always the Deployment URL.

Using the vercel command to deploy and write stdout to a text file. When deploying, stdout is always the Deployment URL.

In the following example, you create a bash script that you include in your CI/CD workflow. The goal is to have all preview deployments be aliased to a custom domain so that developers can bookmark the preview deployment URL. Note that you may need to define the scope when using

The script deploys your project and assigns the deployment URL saved in stdout to the custom domain using vercel alias.

If you need to check for errors when the command is executed such as in a CI/CD workflow, use . If the exit code is anything other than , an error has occurred. The following example demonstrates a script that checks if the exit code is not equal to 0:

These are options that only apply to the command.

The option can be used to upload and deploy the results of a previous execution located in the .vercel/output directory. See vercel build and Build Output API for more details.

When using the flag, no deployment ID will be made available for supported frameworks (like Next.js) to use, which means Skew Protection will not be enabled. Additionally, System Environment Variables will be missing at build time, so frameworks that rely on them at build time may not function correctly. If you need Skew Protection or System Environment Variables, do not use the flag or use Git-based deployments.

You should also consider using the archive option to minimize the number of files uploaded and avoid hitting upload limits:

This example uses the command to build your project locally. It then uses the and options on the command to compress the build output and then deploy it.

The option, shorthand , can be used to provide environment variables to the build step.

Using the vercel command with the --build-env option.

The option can be used to skip questions you are asked when setting up a new Vercel project. The questions will be answered with the provided defaults, inferred from and the folder name.

Using the vercel command with the --yes option.

The option, shorthand , can be used to provide environment variables at runtime.

Using the vercel command with the --env option.

The --name option has been deprecated in favor of Vercel project linking, which allows you to link a Vercel project to your local codebase when you run vercel.

The option, shorthand , can be used to provide a Vercel project name for a deployment.

Using the vercel command with the --name option.

The option can be used to create a deployment for a production domain specified in the Vercel project dashboard.

Using the vercel command with the --prod option.

This CLI option will override the Auto-assign Custom Production Domains project setting.

Must be used with . The option will disable the automatic promotion (aliasing) of the relevant domains to a new production deployment. You can use to complete the domain-assignment process later.

Using the vercel command with the --skip-domain option.

The option can be used to ensures the source code is publicly available at the path.

Using the vercel command with the --public option.

The option can be used to specify which regions the deployments Vercel functions should run in.

Using the vercel command with the --regions option.

The option does not wait for a deployment to finish before exiting from the command.

The option, shorthand , is used to force a new deployment without the build cache.

The option is used to retain the build cache when using .

The option compresses the deployment code into one or more files before uploading it. This option should be used when deployments include thousands of files to avoid rate limits such as the files limit.

In some cases, makes deployments slower. This happens because the caching of source files to optimize file uploads in future deployments is negated when source files are archived.

The option, shorthand , also prints the build logs.

Using the vercel deploy command with the --logs option, to view logs from the build process.

The option, shorthand , is used to add metadata to the deployment.

Deployments can be filtered using this data with .

Use the option to define the environment you want to deploy to. This could be production, preview, or a custom environment.

The following global options can be passed when using the vercel deploy command:

For more information on global options and their usage, refer to the options section.

---

## vercel build

**URL:** https://vercel.com/docs/cli/build

**Contents:**
- vercel build
- Usage
- Unique Options
  - Production
  - Yes
  - target
- Global Options
- Related guides

The command can be used to build a Vercel Project locally or in your own CI environment. Build artifacts are placed into the directory according to the Build Output API.

When used in conjunction with the command, this allows a Vercel Deployment to be created without sharing the Vercel Project's source code with Vercel.

This command can also be helpful in debugging a Vercel Project by receiving error messages for a failed build locally, or by inspecting the resulting build artifacts to get a better understanding of how Vercel will create the Deployment.

It is recommended to run the command before invoking to ensure that you have the most recent Project Settings and Environment Variables stored locally.

Using the vercel build command to build a Vercel Project.

These are options that only apply to the command.

The option can be specified when you want to build the Vercel Project using Production Environment Variables. By default, the Preview Environment Variables will be used.

Using the vercel build command with the --prod option.

The option can be used to bypass the confirmation prompt and automatically pull environment variables and Project Settings if not found locally.

Using the vercel build command with the --yes option.

Use the option to define the environment you want to build against. This could be production, preview, or a custom environment.

The following global options can be passed when using the vercel build command:

For more information on global options and their usage, refer to the options section.

---

## Creating & Triggering Deploy Hooks

**URL:** https://vercel.com/docs/deploy-hooks

**Contents:**
- Creating & Triggering Deploy Hooks
- Creating a Deploy Hook
- Triggering a Deploy Hook
    - Example Request
    - Example Response
- Security
- Build Cache
- Other Optimizations
- Limits
- Troubleshooting

Deploy Hooks allow you to create URLs that accept HTTP requests in order to trigger deployments and re-run the Build Step. These URLs are uniquely linked to your project, repository, and branch, so there is no need to use any authentication mechanism or provide any payload to the request.

This feature allows you to integrate Vercel deployments with other systems. For example, you can set up:

To create a Deploy Hook for your project, make sure your project is connected to a Git repository.

Once your project is connected, navigate to its Settings page and then select the Git menu item.

In the "Deploy Hooks" section, choose a name for your Deploy Hook and select the branch that will be deployed when the generated URL is requested.

We suggest you use a name that easily identifies the Deploy Hook so you will be able to understand when it triggers a deployment. We also suggest creating only one Deploy Hook per branch unless you’re using multiple data sources.

After submitting the form, you will see a URL that you can copy and use.

To trigger a Deploy Hook, send a GET or POST request to the provided URL.

Deploy Hooks will not be triggered if you have the configuration present in your file.

Here's an example request and response you can use for testing:

You do not need to add an authorization header. See Security to learn more.

After sending a request, you can see that it triggered a deployment on your project dashboard.

Deployments triggered by a Deploy Hook are marked in the list.

When you create a Deploy Hook, a unique identifier is generated in the URL. This allows anyone with the URL to deploy your project, so treat it with the same security as you would any other token or password.

If you believe your Deploy Hook URL has been compromised, you can revoke it and create a new one.

Builds triggered by a Deploy Hook are automatically provided with an appropriate Build Cache by default, if it exists.

Caching helps speed up the Build Step, so we encourage you to keep the default behavior. However, if you explicitly want to opt out of using a Build Cache, you can disable it by appending to the Deploy Hook URL.

Here is an example request that explicitly disables the Build Cache:

Deploy Hooks created before May 11th, 2021 do not have the Build Cache enabled by default. To change it, you can either explicitly append to the Deploy Hook URL, or replace your existing Deploy Hook with a newly created one.

If you send multiple requests to deploy the same version of your project, previous deployments for the same Deploy Hook will be canceled to reduce build times.

If your deploy hook fails to create a deployment, check the status check on the commit associated with the deploy hook to identify any failures. See Troubleshooting project collaboration for more information.

---

## Troubleshoot project collaboration

**URL:** https://vercel.com/docs/deployments/troubleshoot-project-collaboration

**Contents:**
- Troubleshoot project collaboration
- Team configuration
  - Hobby teams
  - Pro teams
  - Bot access
- Account configuration
  - Connecting Git provider accounts
  - Managing multiple email addresses

This guide will help you understand how to troubleshoot deployment failures related to project collaboration.

For private repositories, if we cannot identify the Vercel user associated with a commit, any deployment associated with that commit will fail. You can use the following checklist to make sure your Vercel team is properly configured:

Ensure all contributors pushing code are members of your Vercel team.

For each team member, verify their Vercel account is connected to their git provider.

Confirm bot commits are properly configured by the git provider.

The Hobby Plan does not support collaboration for private repositories. If you need collaboration, upgrade to the Pro Plan.

To deploy commits under a Hobby team, the commit author must be the owner of the Hobby team containing the Vercel project connected to the Git repository. This is verified by comparing the Login Connections Hobby team's owner with the commit author.

To make sure we can verify your commits:

If your account is not connected to your git provider, make sure you've properly configured your Vercel email address so that it matches the email associated with the commit.

For the most reliable experience, ensure both your project and account are properly connected to your git provider.

For more information, see Using Hobby teams

The Pro Plan allows for collaboration through team membership. Each person committing to your codebase should be added as a team member.

To deploy commits under a Vercel Pro team, the commit author must be a member of the team containing the Vercel project connected to the Git repository.

To make sure we can verify commits associated with your team:

For more information, see Using Pro teams

Ensure your bots are properly configured and that their commits are clearly identified as automated.

Each team member must connect their git provider account to their Vercel account:

If you use multiple email addresses for git commits, you will need to configure a secondary email address with either your git provider or Vercel depending on if your git repository is linked to your project.

To add secondary email addresses to your Vercel account:

---

## Using the Ruby Runtime with Vercel Functions

**URL:** https://vercel.com/docs/functions/runtimes/ruby

**Contents:**
- Using the Ruby Runtime with Vercel Functions
- Ruby Version
- Ruby Dependencies

The Ruby runtime is available in Beta on all plans

The Ruby runtime is used by Vercel to compile Ruby Vercel functions that define a singular HTTP handler from files within an directory at your project's root.

Ruby files must have one of the following variables defined:

For example, define a file inside a directory as follows:

An example index.rb file inside an /api directory.

An example Gemfile file that defines cowsay as a dependency.

New deployments use Ruby 3.3.x as the default version.

You can specify the version of Ruby by defining in a , like so:

If the patch part of the version is defined, like 3.3.1 it will be ignored and assume the latest 3.3.x.

This runtime supports installing dependencies defined in the . Alternatively, dependencies can be vendored with the command (useful for gems that require native extensions). In this case, dependencies are not built on deployment.

---

## OPTIONS Allowlist

**URL:** https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection/options-allowlist

**Contents:**
- OPTIONS Allowlist
- Enabling OPTIONS Allowlist
  - Go to Project Deployment Protection Settings
  - Enable OPTIONS Allowlist
  - Specify a path
  - Add more paths
  - Save changes
- Disabling OPTIONS Allowlist
  - Go to Project Deployment Protection Settings
  - Disable OPTIONS Allowlist

OPTIONS Allowlist is available on all plans

You can use OPTIONS Allowlist to disable Deployment Protection (including Vercel Authentication, Password Protection, and Trusted IPs) on any incoming CORS preflight request for a list of paths.

When you add a path to OPTIONS Allowlist, any incoming request with the method that starts with the path will no longer be covered by Deployment Protection. When you remove a path from OPTIONS Allowlist, the path becomes protected again with the project's Deployment Protection settings.

For example, if you specify , all requests to paths that start with (such as and ) will be unprotected for any request.

From your Vercel dashboard:

From the OPTIONS Allowlist section, enable the toggle labelled Disabled:

Specify a path to add to the OPTIONS Allowlist:

To add more paths, select Add path:

Once all the paths are added, select Save

From your Vercel dashboard:

From the OPTIONS Allowlist section, select the toggle labelled Enabled:

Once all the paths are added, select Save

---

## Using the Rust Runtime with Vercel functions

**URL:** https://vercel.com/docs/functions/runtimes/rust

**Contents:**
- Using the Rust Runtime with Vercel functions
- Getting Started
- Project setup
  - Cargo.toml configuration
  - Creating API handlers
- Deployment
  - Git deployment
  - CLI deployment
  - Build optimization
- Feature support

The Rust runtime is available in Beta on all plans

Use Rust to build high-performance, memory-safe serverless functions. The Rust runtime runs on Fluid compute for optimal performance and lower latency.

Create a file in your project root:

Create Rust files in your directory. Each file becomes a serverless function:

For more code examples, please refer to our templates:

Push your code to a connected GitHub repository for automatic deployments.

Deploy directly using the Vercel CLI:

For prebuilt deployments, optimize your :

---

## Deploying GitHub Projects with Vercel

**URL:** https://vercel.com/docs/git/vercel-for-github

**Contents:**
- Deploying GitHub Projects with Vercel
- Supported GitHub Products
- Deploying a GitHub Repository
- Changing the GitHub Repository of a Project
  - A Deployment for Each Push
  - Updating the Production Domain
  - Preview URLs for the Latest Changes for Each Pull Request
  - Deployment Authorizations for Forks
  - Configuring for GitHub
  - System environment variables

Vercel for GitHub automatically deploys your GitHub projects with Vercel, providing Preview Deployment URLs, and automatic Custom Domain updates.

When using Data Residency with a unique subdomain on GitHub Enterprise Cloud you'll need to use GitHub Actions

The Deploying a Git repository guide outlines how to create a new Vercel Project from a GitHub repository, and enable automatic deployments on every branch push.

If you'd like to connect your Vercel Project to a different GitHub repository or disconnect it, you can do so from the Git section in the Project Settings.

Vercel for GitHub will deploy every push by default. This includes pushes and pull requests made to branches. This allows those working within the repository to preview changes made before they are pushed to production.

With each new push, if Vercel is already building a previous commit on the same branch, the current build will complete and any commit pushed during this time will be queued. Once the first build completes, the most recent commit will begin deployment and the other queued builds will be cancelled. This ensures that you always have the latest changes deployed as quickly as possible.

You can disable this feature for GitHub by configuring the github.autoJobCancellation option in your file.

If Custom Domains are set from a project domains dashboard, pushes and merges to the Production Branch (commonly "main") will be made live to those domains with the latest deployment made with a push.

If you decide to revert a commit that has already been deployed to production, the previous Production Deployment from a commit will automatically be made available at the Custom Domain instantly; providing you with instant rollbacks.

The latest push to any pull request will automatically be made available at a unique preview URL based on the project name, branch, and team or username. These URLs will be provided through a comment on each pull request. Vercel also supports Comments on preview deployments made from PRs on GitHub. Learn more about Comments on preview deployments in GitHub here.

If you receive a pull request from a fork of your repository, Vercel will require authorization from you or a team member to deploy the pull request.

This behavior protects you from leaking sensitive project information such as environment variables and the OIDC Token.

You can disable Git Fork Protection in the Security section of your Project Settings.

Vercel for GitHub uses the deployment API to bring you an extended user interface both in GitHub, when showing deployments, and Slack, if you have notifications setup using the Slack GitHub app.

You will see all of your deployments, production or preview, from within GitHub on its own page.

Due to using GitHub's Deployments API, you will also be able to integrate with other services through GitHub's checks. Vercel will provide the deployment URL to the checks that require it, for example; to a testing suite such as Checkly.

To configure the Vercel for GitHub integration, see the configuration reference for Git.

You may want to use different workflows and APIs based on Git information. To support this, the following System Environment Variables are exposed to your Deployments:

The Git Provider the deployment is triggered from. In the case of GitHub, the value is always github.

The origin repository of the app on GitHub.

The GitHub organization that owns the repository the deployment is triggered from.

The ID of the GitHub repository the deployment is triggered from.

The GitHub branch that the deployment was made from.

The GitHub SHA of the commit the deployment was triggered by.

The message attached to the GitHub commit the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The GitHub username belonging to the author of the commit that the project was deployed by.

The GitHub name belonging to the author of the commit that the project was deployed by.

The GitHub pull request id the deployment was triggered by. If a deployment is created on a branch before a pull request is made, this value will be an empty string.

We require some permissions through our Vercel for GitHub integration. Below are listed the permissions required and a description for what they are used for.

Repository permissions allow us to interact with repositories belonging to or associated with (if permitted) the connected account.

Organization permissions allow us to offer an enhanced experience through information about the connected organization.

User permissions allow us to offer an enhanced experience through information about the connected user.

We use the permissions above in order to provide you with the best possible deployment experience. If you have any questions or concerns about any of the permission scopes, please contact Vercel Support.

To sign up on Vercel with a different GitHub account, sign out of your current GitHub account.

Then, restart the Vercel signup process.

When importing or connecting a GitHub repository, we require that you have Collaborator access to the corresponding repository, so that we can configure a webhook and automatically deploy pushed commits.

If a repository is missing when you try to import or connect it, make sure that you have Collaborator access configured for the repository. For an organization or a team, this page explains how to view the permissions of the members. For personal GitHub accounts, this page explains how to manage access.

By default, comments from the Vercel GitHub bot will appear on your pull requests and commits. You can silence these comments in your project's settings:

If you had previously used the, now deprecated, property in your project configuration, we'll automatically adjust the setting for you.

It is currently not possible to prevent comments for specific branches.

By default, Vercel notifies GitHub of deployments using the webhook event. This creates an entry in the activity log of GitHub's pull request UI.

Because Vercel also adds a comment to the pull request with a link to the deployment, unwanted noise can accumulate from the list of deployment notifications added to a pull request.

You can disable events by:

Before doing this, ensure that you aren't depending on events in your GitHub Actions workflows. If you are, we encourage migrating to events.

You can use GitHub Actions to build and deploy your Vercel Application. This approach is necessary to enable Vercel with GitHub Enterprise Server (GHES) with Vercel, as GHES cannot use Vercel’s built-in Git integration.

You'll need to make GitHub Actions for preview (non- pushes) and production ( pushes) deployments. Learn more about how to configure GitHub Actions and Vercel for custom CI/CD workflows.

This event will only trigger a workflow run if the workflow file exists on the default branch (e.g. ). If you'd like to test the workflow prior to merging to , we recommend adding a trigger.

Vercel sends events to GitHub when the status of your deployment changes. These events can trigger GitHub Actions, enabling continuous integration tasks dependent on Vercel deployments.

GitHub Actions can trigger on the following events:

events contain a JSON payload with information about the deployment, such as deployment and deployment . GitHub Actions can access this payload through . For example, accessing the URL of your triggering deployment through .

Read more and see the full schema in our package, and see the how can I run end-to-end tests after my Vercel preview deployment? guide for a practical example.

With , the dispatch event contains details about your deployment allowing you to reduce GitHub Actions costs and complexity in your workflows.

For example, to migrate the GitHub Actions trigger for preview deployments for end-to-end tests:

Previously, we needed to check if the status of a deployment was successful. Now, with we can trigger our workflow only on a successful deployment by specifying the dispatch type.

Since we're no longer using the event, we need to get the from the event's .

**Examples:**

Example 1 (bash):
```bash
VERCEL_GIT_REPO_SLUG=my-site
```

Example 2 (bash):
```bash
VERCEL_GIT_REPO_SLUG=my-site
```

Example 3 (bash):
```bash
VERCEL_GIT_REPO_OWNER=acme
```

Example 4 (bash):
```bash
VERCEL_GIT_REPO_OWNER=acme
```

---

## Password Protection

**URL:** https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/password-protection

**Contents:**
- Password Protection
- Password Protection security considerations
- Managing Password Protection
  - Go to Project Deployment Protection Settings
  - Manage Password Protection
  - Manage using the API
  - Manage using Terraform

Password Protection is available on Enterprise plansor with the Advanced Deployment Protection add-on for Pro plans

Those with the owner, member and admin roles can manage Password Protection

With Password Protection enabled, visitors to your deployment must enter the pre-defined password to gain access. You can set the desired password from your project settings when enabling the feature, and update it any time

The table below outlines key considerations and security implications when using Password Protection for your deployments on Vercel.

You can manage Password Protection through the dashboard, API, or Terraform:

From your Vercel dashboard:

From the Password Protection section:

All your existing and future deployments will be protected with a password for the project. Next time when you access a deployment, you will be asked to log in by entering the password, which takes you to the deployment. A cookie will then be set in your browser for the deployment URL so you don't need to enter the password every time.

You can manage Password Protection using the Vercel API endpoint to update an existing project with the following body

You can configure Password Protection using in the data source in the Vercel Terraform Provider.

---

## Purging Vercel CDN Cache

**URL:** https://vercel.com/docs/cdn-cache/purge

**Contents:**
- Purging Vercel CDN Cache
- Cache keys
- Understanding cache purging
  - Invalidating the cache
  - Deleting the cache
  - Cache tags
    - Cache tag case sensitivity
    - Cache tag scope
- Programmatically purging CDN Cache
- Manually purging Vercel CDN Cache

Cache purging is available on all plans

Those with the owner and member roles can access this feature

Learn how to invalidate and purge cached content on Vercel's CDN, including cache keys and manual purging options.

Each request to Vercel's CDN has a cache key derived from the following:

Since each deployment has a different cache key, you can promote a new deployment to production without affecting the cache of the previous deployment.

The cache key for Image Optimization behaves differently for static images and remote images.

When you invalidate a cache tag, all cached content associated with that tag is marked as stale. The next request serves the stale content instantly while revalidation happens in the background. This approach has no latency impact for users while ensuring content gets updated.

When you delete a cache tag, the cached entries are marked for deletion. The next request fetches content from your origin before responding to the user. This can slow down the first request after deletion. If many users request the same deleted content simultaneously, it can create a cache stampede where multiple requests hit your origin at once.

Cache tags are user-defined strings that can be assigned to cached responses. These tags can later be used to purge the the CDN cache.

For example, you may have a product with id that is displayed on multiple pages such as , , etc. If you add a unique cache tag to those pages, such as , you can invalidate that tag when the content of the product changes.

You can add a cache tag by importing addCacheTag from the npm package and passing your tag.

Cache tags are case-sensitive, meaning and are treated as different tags.

Cache tags are scoped to your project. When you purge a tag, you can target production deployments, preview deployments, or both. By default, purging affects all cached responses across all deployments in that project that use that tag.

You can purge Vercel CDN cache in the following ways:

In some circumstances, you may need to delete all cached data and force revalidation. For example, you might have set a to cache the response for a month but the content changes more frequently than once a month. You can do this by purging the cache:

The purge event itself is not billed but it can temporarily increase Function Duration, Functions Invocations, Edge Function Executions, Fast Origin Transfer, Image Optimization Transformations, Image Optimization Cache Writes, and ISR Writes.

Purge is not the same as creating a new deployment because it will also purge Image Optimization content, which is usually preserved between deployments, as well as ISR content, which is often generated at build time for new deployments.

---

## LlamaIndex

**URL:** https://vercel.com/docs/ai-gateway/framework-integrations/llamaindex

**Contents:**
- LlamaIndex
- Getting started
  - Create a new project
  - Install dependencies
  - Configure environment variables
  - Create your LlamaIndex application
  - Running the application

LlamaIndex makes it simple to build knowledge assistants using LLMs connected to your enterprise data. This guide demonstrates how to integrate Vercel AI Gateway with LlamaIndex to access various AI models and providers.

First, create a new directory for your project and initialize it:

Install the required LlamaIndex packages along with the package:

Create a file with your Vercel AI Gateway API key:

If you're using the AI Gateway from within a Vercel deployment, you can also use the environment variable which will be automatically provided.

Create a new file called with the following code:

Run your application using Python:

You should see a streaming response from the AI model.

---

## Deploying Git Repositories with Vercel

**URL:** https://vercel.com/docs/git

**Contents:**
- Deploying Git Repositories with Vercel
- Supported Git Providers
  - Self-Hosted examples
- Deploying a Git repository
  - Creating a deployment from a Git reference
- Deploying private Git repositories
  - Using Pro teams
  - Using Hobby teams
- Deploying forks of public Git repositories
- Production branch

Vercel allows for automatic deployments on every branch push and merges onto the production branch of your GitHub, GitLab, Bitbucket and Azure DevOps Pipelines projects.

Using Git with Vercel provides the following benefits:

When working with Git, have a branch that works as your production branch, often called . After you create a pull request (PR) to that branch, Vercel creates a unique deployment you can use to preview any changes. Once you are happy with the changes, you can merge your PR into the branch, and Vercel will create a production deployment.

You can choose to use a different branch as the production branch.

If your provider is not listed here, you can also use the Vercel CLI to deploy with any git provider.

Setting up your GitHub, GitLab, or Bitbucket repository on Vercel is only a matter of clicking the "New Project" button on the top right of your dashboard and following the steps.

For Azure DevOps repositories, use the Vercel Deployment Extension

After clicking it, you'll be presented with a list of Git repositories that the Git account you've signed up with has write access to.

To select a different Git namespace or provider, you can use the dropdown list on the top left of the section.

After you've selected the Git repository or template you want to use for your new project, you'll be taken to a page where you can configure your project before it's deployed.

When your settings are correct, you can select the Deploy button to initiate a deployment.

You can initiate new deployments directly from the Vercel Dashboard using a Git reference. This approach is ideal when automatic deployments are interrupted or unavailable.

To create a deployment from a Git reference:

From your dashboard, select the project you'd like to create a deployment for

Select the Deployments tab. Once on the Deployments page, select the Create Deployment button

Depending on how you would like to deploy, enter the following:

Select Create Deployment. Vercel will build and deploy your commit or branch as usual

When the same commit appears in multiple branches, Vercel will prompt you to choose the appropriate branch configuration. This choice is crucial as it affects settings like environment variables linked to each branch.

As an additional security measure, commits on private Git repositories (and commits of forks that are targeting those Git repositories) will only be deployed if the commit author also has access to the respective project on Vercel.

Depending on whether the owner of the connected Vercel project is a Hobby or a Pro team, the behavior changes as mentioned in the sections below.

This only applies to commit authors on GitHub organizations, GitLab groups and non-personal Bitbucket workspaces. It does not apply to collaborators on personal Git accounts.

For public Git repositories, a different behavior applies.

To deploy commits under a Vercel Pro team, the commit author must be a member of the team containing the Vercel project connected to the Git repository.

Membership is verified by finding the Vercel user associated with the commit author through Login Connections. If a Vercel user is found, it checks if the account is a member of the Pro team.

If the commit author is not a member, the deployment will be prevented, and the commit author can request to join the team. The team owners will be notified and can accept or decline the membership request on the Members page in the team Settings.

If the request is declined, the commit will remain undeployed. If the commit author is accepted as a member of the Pro team, their most recent commit will automatically resume deployment to Vercel.

Commit authors are automatically considered part of the Pro team on Vercel if one of the existing members has connected their account on Vercel with the Git account that created the commit.

You cannot deploy to a Hobby team from a private repository in a GitHub organization, GitLab group, or Bitbucket workspace. Consider making the repository public or upgrading to Pro.

To deploy commits under a Hobby team, the commit author must be the owner of the Hobby team containing the Vercel project connected to the Git repository. This is verified by comparing the Login Connections Hobby team's owner with the commit author.

If the commit author is not the owner of the destination Hobby team, the deployment will be prevented, and a recommendation to transfer the project to a Pro team will be displayed on the Git provider.

After transferring the project to a Pro team, commit authors can be added as members of that team. The behavior mentioned in the section above will then apply to them whenever they commit.

When a public repository is forked, commits from it will usually deploy automatically. However, when you receive a pull request from a fork of your repository, Vercel will require authorization from you or a team member to deploy the pull request. This is a security measure that protects you from leaking sensitive project information. A link to authorize the deployment will be posted as a comment on the pull request.

The authorization step will be skipped if the commit author is already a team member on Vercel.

A Production deployment will be created each time you merge to the production branch.

When you create a new Project from a Git repository on Vercel, the Production Branch will be selected in the following order:

On the Environments page in the Project Settings, you can change your production branch:

Whenever a new commit is then pushed to the branch you configured here, a production deployment will be created for you.

While the production branch is a single Git branch that contains the code that is served to your visitors, all other branches are deployed as pre-production branches (either preview branches, or if you have configured them, custom environments branches).

For example, if your production branch is , then by default all the Git branches that are not are considered preview branches. That means there can be many preview branches, but only a single production branch.

To learn more about previews, see the Preview Deployments page.

By default, every preview branch automatically receives its own domain similar to the one shown below, whenever a commit is pushed to it. To learn more about generated URLs, see the Accessing Deployments through Generated URLs page.

For most use cases, the default preview behavior mentioned above is enough. If you'd like your changes to pass through multiple phases of preview branches instead of just one, you can accomplish it by assigning Domains and Environment Variables to specific Preview Branches.

For example, you could create a phase called "Staging" where you can accumulate Preview changes before merging them onto production by following these steps:

Alternatively, teams on the Pro plan can use custom environments.

Custom environments allow you to create and define a pre-production environment. As part of creating a custom environment, you can match specific branches or branch names, including , to automatically deploy to that environment. You can also attach a domain to the environment.

---

## Speed Insights Metrics

**URL:** https://vercel.com/docs/speed-insights/metrics

**Contents:**
- Speed Insights Metrics
- Real Experience Score (RES)
  - Real user monitoring
- Core Web Vitals explained
  - Largest Contentful Paint (LCP)
  - Cumulative Layout Shift (CLS)
  - Interaction to Next Paint (INP)
  - First Contentful Paint (FCP)
- Other metrics
  - Time to First Byte (TTFB)

While many performance measurement tools, like Lighthouse, estimate user experience based on lab simulations, Vercel's Real Experience Score (RES) uses real data points collected from your users' devices.

As a result, RES shows how real users experience your application. This real-time data helps you understand your application's performance and track changes as they happen.

You can use these insights to see how new deployments affect performance, helping you improve your application's user experience.

The timestamps in the Speed Insights view are in local time (not UTC).

The Core Web Vitals, as defined by Google and the Web Performance Working Group, are key metrics that assess your web application's loading speed, responsiveness, and visual stability.

Speed Insights now uses Lighthouse 10 scoring criteria instead of Lighthouse 6 criteria as explained in Updated Scoring Criteria

Largest Contentful Paint (LCP) is a performance metric that measures the time from when the page starts loading to when the largest content element in the viewable screen is fully displayed. This could be an image, a video, or a block of text. LCP is important as it gives a measure of when the main content of the page is visible to the user.

A good LCP time is considered to be 2.5 seconds or less.

Cumulative Layout Shift (CLS) is a performance metric that quantifies the fraction of layout shift experienced by the user. A layout shift occurs any time a visible element changes its position from one rendered frame to the next.

The score is calculated from the product of two measures:

A good CLS score is considered to be 0.1 or less.

Interaction to Next Paint (INP) is a metric that measures the time from when a user interacts with your site to the time the browser renders the next frame in response to that interaction.

This metric is used to gauge the responsiveness of a page to user interactions. The quicker the page responds to user input, the better the INP.

Lower INP times are better, with an INP time of 200 milliseconds or less being considered good.

First Contentful Paint (FCP) is a performance metric that measures the time from the moment the page starts loading to the moment the first piece of content from the Document Object Model (DOM) is rendered on the screen. This could be any content from the webpage such as an image, a block of text, or a canvas render. The FCP is important because it indicates when the user first sees something useful on the screen, providing an insight into your webpage's loading speed.

Lower FCP times are better, with an FCP time of 1.8 seconds or less being considered good.

Time to First Byte (TTFB) measures the time between the request for a resource and when the first byte of a response begins to arrive.

Lower TTFB times are better, with a good TTFB time being considered as under 800 milliseconds.

First Input Delay (FID) measures the time from when a user first interacts with your site (by selecting a link for example) to the time when the browser is able to respond to that interaction. This metric is important on pages where the user needs to do something, because it captures some of the delay that users feel when trying to interact with the page.

A good FID score is 100 milliseconds or less.

As stated by Google, simulating an environment to measure Web Vitals necessitates a different approach since no real user request is involved.

Total Blocking Time (TBT) quantifies how non-interactive a page is. It measures the total time between the First Contentful Paint (FCP) and Time to Interactive (TTI) where the main thread was blocked for long enough to prevent user input. Long tasks (over 50 ms) block the main thread, preventing the user from interacting with the page. The sum of the time portions exceeding 50 ms constitutes the TBT.

Lower TBT times are better, with a good TBT time being considered as under 800 milliseconds.

For more in-depth information related to performance metrics, visit the PageSpeed Insights documentation.

Vercel calculates performance scores using real-world data obtained from the HTTP Archive. This process involves assigning each collected metric (e.g., First Contentful Paint (FCP)) a score ranging from 0 to 100. The score is determined based on where the raw metric value falls within a log-normal distribution derived from actual website performance data.

For instance, if HTTP Archive data shows that the top-performing sites render the Largest Contentful Paint (LCP) in approximately 1220 milliseconds, this value is mapped to a score of 99. Vercel then uses this correlation, along with your project's specific LCP metric value, to compute your LCP score.

The Real Experience Score is a weighted average of all individual metric scores. Vercel has assigned each metric a specific weighting, which best represents user's perceived performance on mobile and desktop devices.

In the context of Vercel's Speed Insights, a data point is a single unit of information that represents a measurement of a specific Web Vital metric during a user's visit to your website.

Data points are collected on hard navigations, which in the case of Next.js apps, are only the first-page view in a session. During a user's visit, data points are gathered during the initial page load, user interaction, and upon leaving the page.

As of now, up to 6 data points can be potentially tracked per visit:

The collection of metrics may vary depending on how users interact with or exit the page. On average, you can expect to collect between 3 and 6 metrics per visit.

These data points provide insights into various performance aspects of your website, such as the time it takes to display the first content (FCP) and the delay between user input and response (FID). By analyzing these data points, you can gain valuable information to optimize and enhance the performance of your website.

By default, the user experience percentile is set to P75, which offers a balanced overview of the majority of user experiences. You can view the data for the other percentiles by selecting them in the time-based line graph.

The chosen percentile corresponds to the proportion of users who experience a load time faster than a specific value. Here's how each percentile is defined:

For instance, a P75 score of 1 second for First Contentful Paint (FCP) means that 75% of your users experience an FCP faster than 1 second. Similarly, a P99 score of 8 seconds means 99% of your users experience an FCP faster than 8 seconds.

Performance metrics, including the Real Experience Score, the Virtual Experience Score, and the individual Core Web Vitals (along with Other Web Vitals) are color-coded as follows:

Aim for 'Good' scores (90 to 100) for both Real and Virtual Experience Scores. Keep in mind that reaching a score of 100 is extremely challenging due to diminishing returns. For example, improving from 99 to 100 is much harder than moving from 90 to 94, as the effort needed increases dramatically at higher scores.

Higher Real Experience and Virtual Experience Scores generally translate to better end-user experiences, making it worthwhile to strive for improved Web Vital Scores. Performance scores are color-coded and improvements within the same color range will enhance user experience but don't significantly impact search engine rankings.

If you aim to boost your site's search ranking, aim to move your scores into a higher color-coded category, for instance, from 'Needs Improvement' (orange) to 'Good' (green). This change reflects substantial improvements in performance and is more likely to be rewarded with higher search engine rankings.

The Real Experience Score (RES) displayed in the Speed Insights tab is derived from actual data points collected from your visitors' devices. As such, it can only offer insight into your app's performance post-deployment. While it's critical to gather these real-world data points, they only reflect user experiences after the fact, limiting their predictive power.

In contrast, the Virtual Experience Score (VES) is a predictive performance metric that allows you to anticipate the impact of changes on your app's performance, ensuring there's no regression in user experience. This metric is provided by integrations like Checkly that employ Deployment Checks.

Setting up an integration supporting performance checks enables these checks to run for each deployment. These checks assess whether the user experience is likely to improve or deteriorate with the proposed changes, helping guide your decision-making process.

Like RES, the VES draws from four separate Speed Insights, albeit with some variations:

Speed Insights offers a variety of views to help you analyze your application's performance data. This allows you to identify areas that need improvement and make informed decisions about how to optimize your site. To learn more, see Using Speed Insights.

---

## vercel alias

**URL:** https://vercel.com/docs/cli/alias

**Contents:**
- vercel alias
- Preferred production commands
- Usage
- Unique options
  - Yes
  - Limit
- Global Options
- Related guides

The command allows you to apply custom domains to your deployments.

When a new deployment is created (with our Git Integration, Vercel CLI, or the REST API), the platform will automatically apply any custom domains configured in the project settings.

Any custom domain that doesn't have a custom preview branch configured (there can only be one Production Branch and it's configured separately in the project settings) will be applied to production deployments created through any of the available sources.

Custom domains that do have a custom preview branch configured, however, only get applied when using the Git Integration.

If you're not using the Git Integration, is a great solution if you still need to apply custom domains based on Git branches, or other heuristics.

The command is not the recommended way to promote production deployments to specific domains. Instead, you can use the following commands:

In general, the command allows for assigning custom domains to any deployment.

Make sure to not include the HTTP protocol (e.g. ) for the parameter.

Using the vercel alias command to assign a custom domain to a deployment.

Using the vercel alias command to remove a custom domain from a deployment.

Using the vercel alias command to list custom domains that were assigned to deployments.

These are options that only apply to the command.

The option can be used to bypass the confirmation prompt when removing an alias.

Using the vercel alias rm command with the --yes option.

The option can be used to specify the maximum number of aliases returned when using . The default value is and the maximum is .

Using the vercel alias ls command with the --limit option.

The following global options can be passed when using the vercel alias command:

For more information on global options and their usage, refer to the options section.

---

## Nitro on Vercel

**URL:** https://vercel.com/docs/frameworks/backend/nitro

**Contents:**
- Nitro on Vercel
- Get started with Nitro on Vercel
  - Get started with Vercel CLI
- Using Vercel's features with Nitro
- Incremental Static Regeneration (ISR)
  - On-demand revalidation
  - Create an Environment Variable
  - Update your configuration
  - Trigger revalidation
  - Fine-grained ISR configuration

Nitro is a full-stack framework with TypeScript-first support. It includes filesystem routing, code-splitting for fast startup, built-in caching, and multi-driver storage. It enables deployments from the same codebase to any platform with output sizes under 1MB.

You can deploy a Nitro app to Vercel with zero configuration.

To get started with Nitro on Vercel, use the following Nitro template to deploy to Vercel with zero configuration:

Vercel deployments can integrate with your git provider to generate preview URLs for each pull request you make to your Nitro project.

Get started by initializing a new Nitro project using Vercel CLI init command:

This will clone the Nitro example repository in a directory called .

When you deploy a Nitro app to Vercel, you can use Vercel specific features such as Incremental Static Regeneration (ISR), preview deployments, Fluid compute, Observability, and Vercel firewall with zero or minimum configuration.

ISR allows you to create or update content without redeploying your site. ISR has three main benefits for developers: better performance, improved security, and faster build times.

With on-demand revalidation, you can purge the cache for an ISR route whenever you want, foregoing the time interval required with background revalidation.

To revalidate a path to a prerendered function:

Create an Environment Variable to store a revalidation secret by:

Update your configuration to use the revalidation secret as follows:

You can revalidate a path to a prerendered function by making a or request to that path with a header of

When the prerendered function endpoint is accessed with this header set, the cache will be revalidated. The next request to that function will return a fresh response.

To have more control over ISR caching, you can pass an options object to the route rule as shown below:

By default, query parameters are ignored by cache unless you specify them in the array.

The following options are available:

With Vercel Observability, you can view detailed performance insights broken down by route and monitor function execution performance. This can help you identify bottlenecks and optimization opportunities.

Nitro (>=2.12) generates routing hints for functions observability insights, providing a detailed view of performance broken down by route.

To enable this feature, ensure you are using a compatibility date of or later.

Framework integrations can use the configuration to declare SSR routes. For more information, see #3475.

When you deploy a Nitro app to Vercel, your server routes automatically become Vercel Functions and use Fluid compute by default.

Learn more about deploying Nitro projects on Vercel with the following resources:

---

## Inspecting your Open Graph metadata

**URL:** https://vercel.com/docs/deployments/og-preview

**Contents:**
- Inspecting your Open Graph metadata
- Filter by pathname
- Metadata
  - Twitter-specific metadata

You can use the Open Graph tab on every deployment on Vercel to validate and view your Open Graph (OG) data across a range of social media sites before you share it out. Routes using Deployment Protection can also be inspected.

You can use the Path dropdown to view the OG card for any page on that particular deployment.

These properties set by the Open Graph protocol.

---

## Deploying GitLab Projects with Vercel

**URL:** https://vercel.com/docs/git/vercel-for-gitlab

**Contents:**
- Deploying GitLab Projects with Vercel
- Supported GitLab Products
- Deploying a GitLab Repository
- Changing the GitLab Repository of a Project
  - A Deployment for Each Push
  - Updating the Production Domain
  - Preview URLs for Each Merge Request
  - System environment variables
  - VERCEL_GIT_PROVIDER
  - VERCEL_GIT_REPO_SLUG

Vercel for GitLab automatically deploys your GitLab projects with Vercel, providing Preview Deployment URLs, and automatic Custom Domain updates.

The Deploying a Git repository guide outlines how to create a new Vercel Project from a GitLab repository, and enable automatic deployments on every branch push.

If you'd like to connect your Vercel Project to a different GitLab repository or disconnect it, you can do so from the Git section in the Project Settings.

Vercel for GitLab will deploy each push by default. This includes pushes and pull requests made to branches. This allows those working within the project to preview the changes made before they are pushed to production.

With each new push, if Vercel is already building a previous commit on the same branch, the current build will complete and any commit pushed during this time will be queued. Once the first build completes, the most recent commit will begin deployment and the other queued builds will be cancelled. This ensures that you always have the latest changes deployed as quickly as possible.

If Custom Domains are set from a project domains dashboard, pushes and merges to the Production Branch (commonly "main") will be made live to those domains with the latest deployment made with a push.

If you decide to revert a commit that has already been deployed to production, the previous Production Deployment from a commit will automatically be made available at the Custom Domain instantly; providing you with instant rollbacks.

The latest push to any merge request will automatically be made available at a unique preview URL based on the project name, branch, and team or username. These URLs will be provided through a comment on each merge request.

You may want to use different workflows and APIs based on Git information. To support this, the following System Environment Variables are exposed to your Deployments:

The Git Provider the deployment is triggered from. In the case of GitLab, the value is always gitlab.

The GitLab name of the deployed project.

The GitLab user, group, or sub-group that the project belongs to.

The GitLab ID of the deployed project.

The GitLab branch that the deployment was triggered by.

The GitLab sha of the commit the deployment was triggered by.

The message accompanying the GitLab commit that the deployment was triggered by. The message is truncated if it exceeds 2048 bytes.

The username belonging to the author of the commit that was deployed on GitLab.

The name belonging to the author of the commit that was deployed on GitLab.

The GitLab merge request id the deployment was triggered by. If a deployment is created on a branch before a merge request is made, this value will be an empty string.

We require some permissions through our Vercel for GitLab integration. Below are listed the permissions required and a description for what they are used for.

We use the permissions above in order to provide you with the best possible deployment experience. If you have any questions or concerns about any of the permission scopes, please contact Vercel Support.

To sign up on Vercel with a different GitLab account, sign out of your current GitLab account.

Then, restart the Vercel signup process.

When importing or connecting a GitLab repository, we require that you have Maintainer access to the corresponding repository, so that we can configure a webhook and automatically deploy pushed commits. If your repository belongs to a Gitlab group, you need to have Maintainer access to the group as well. You can use the Group and project access requests API to find the access levels for a group.

If a repository is missing when you try to import or connect it, make sure that you have Maintainer access configured for the repository.

By default, comments from the Vercel bot will appear on your pull requests and commits. You can silence these comments in your project's settings:

It is currently not possible to prevent comments for specific branches.

You can use GitLab Pipelines to build and deploy your Vercel Application.

allows you to build your project inside GitLab Pipelines, without exposing your source code to Vercel. Then, skips the build step on Vercel and uploads the previously generated folder to Vercel from the GitLab Pipeline.

Learn more about how to configure GitLab Pipelines and Vercel for custom CI/CD workflows.

In some cases, your GitLab merge pipeline can fail while your branch pipeline succeeds, allowing your merge requests to merge with failing tests. This is a GitLab issue. To avoid it, we recommend using Vercel CLI to deploy your projects.

**Examples:**

Example 1 (bash):
```bash
VERCEL_GIT_REPO_SLUG=my-site
```

Example 2 (bash):
```bash
VERCEL_GIT_REPO_SLUG=my-site
```

Example 3 (bash):
```bash
VERCEL_GIT_REPO_OWNER=acme
```

Example 4 (bash):
```bash
VERCEL_GIT_REPO_OWNER=acme
```

---

## vercel redeploy

**URL:** https://vercel.com/docs/cli/redeploy

**Contents:**
- vercel redeploy
- Usage
- Standard output usage
- Standard error usage
- Unique Options
  - No Wait
  - target
- Global Options

The command is used to rebuild and redeploy an existing deployment.

Using vercel redeploy will rebuild and deploys an existing deployment.

When redeploying, is always the Deployment URL.

Using the vercel redeploy command to redeploy and write stdout to a text file. When redeploying, stdout is always the Deployment URL.

If you need to check for errors when the command is executed such as in a CI/CD workflow, use . If the exit code is anything other than , an error has occurred. The following example demonstrates a script that checks if the exit code is not equal to 0:

These are options that only apply to the command.

The option does not wait for a deployment to finish before exiting from the command.

Using the vercel redeploy command with the --no-wait option.

Use the option to define the environment you want to redeploy to. This could be production, preview, or a custom environment.

The following global options can be passed when using the vercel redeploy command:

For more information on global options and their usage, refer to the options section.

---

## Deployment Checks

**URL:** https://vercel.com/docs/deployment-checks

**Contents:**
- Deployment Checks
- Understanding Deployment Checks
- Enabling Deployment Checks
  - Ensure prerequisites are enabled
  - Select your Deployment Checks
  - Update workflows (if necessary)
  - Create a new production deployment
  - Run GitHub Actions to fulfill all Deployment Checks
  - Promote to production once all Deployment Checks are met
- Bypassing Deployment Checks

Deployment Checks are conditions that must be met before promoting a production build to your production environment.

When a project is connected to GitHub using Vercel for GitHub, Vercel can automatically read the statuses of your commits and selected GitHub Action results. Using these statuses, Vercel can prevent production deployments from promoting to production until your checks have passed.

Decoupling production builds and releases allows teams to move faster with higher confidence at scale.

By default, Vercel automatically promotes your most recent, successful production build to your custom production domains. This creates the following release workflow:

At scale, this can mean the set of code that is tested before merging is not the same as the code that would be released to end users. We want to maintain the safety of releases, while allowing developers and agents to continue authoring and merging code at high velocity.

With Deployment Checks, you introduce a new step that ensures the safety of the production deployment before it's released, with the following workflow:

Visit your project's settings, and select Add Checks to select required Deployment Checks.

If using GitHub Actions with a trigger, update your workflows to set a status for Vercel using the action. This will ensure the commit that triggered the deployment is the one that is used to determine if the Deployment Checks are met.

If you are not using , you can still use the , however it is not required and you can depend on the check directly.

Deployment Checks appear as part of a production deployment's lifecycle. Production deployments will still be created, but will not be automatically assigned to your custom domains until all Deployment Checks are met.

To meet Deployment Checks, run their corresponding GitHub Actions.

If you're using to trigger a workflow in response to Vercel deployments, you must use the event. This event triggers after the deployment is created, and before checks are run.

Once all of the Deployment Checks have passed, the deployment is aliased to your production domain(s) automatically.

For additional release protection, enable Rolling Releases to ensure your deployment is fractionally released before promoting to everyone.

You can bypass Deployment Checks by selecting Force Promote from the deployment details page.

GitHub and GitHub Actions have edge cases with status reporting. These behaviors are matched in GitHub-backed Deployment Checks.

---

## Vercel for Platforms

**URL:** https://vercel.com/docs/multi-tenant

**Contents:**
- Vercel for Platforms
- Why build multi-tenant apps?
- Getting started
- Multi-tenant features on Vercel
- Next steps

A multi-tenant application serves multiple customers (tenants) from a single codebase.

Each tenant gets its own domain or subdomain, but you only have one Next.js (or similar) deployment running on Vercel. This approach simplifies your infrastructure, scales well, and keeps your branding consistent across all tenant sites.

Get started with our detailed docs, multi-tenant Next.js example, or learn more about customizing domains.

Some popular multi-tenant apps on Vercel include:

For example, you might have:

Vercel's platform automatically issues SSL certificates, handles DNS routing via its Anycast network, and ensures each of your tenants gets low-latency responses from the closest CDN region.

The fastest way to get started is with our multi-tenant Next.js starter kit. This template includes:

---

## Performing an Instant Rollback on a Deployment

**URL:** https://vercel.com/docs/instant-rollback

**Contents:**
- Performing an Instant Rollback on a Deployment
- How to roll back deployments
  - Select your project
  - Select the deployment to roll back to
  - Verify the information
  - Confirm the rollback
  - Successful rollback
  - Accessing Instant Rollback from Deployments tab
- Who can roll back deployments?
- Eligible deployments

Vercel provides Instant Rollback as a way to quickly revert to a previous production deployment. This can be useful in situations that require a swift recovery from production incidents, like breaking changes or bugs. It's important to keep in mind that during a rollback:

For teams on a Pro or Enterprise plan, all deployments previously aliased to a production domain are eligible to roll back. Hobby users can roll back to the immediately previous deployment.

To initiate an Instant Rollback from the Vercel dashboard:

On the project's overview page, you will see the Production Deployment tile. From there, click Instant Rollback.

After selecting Instant Rollback, you'll see an dialog that displays your current production deployment and the eligible deployments that you can roll back to.

If you're on the Pro or Enterprise plans, you can also click the Choose another deployment button to display a list of all eligible deployments.

Select the deployment that you'd like to roll back to and click Continue.

Once you've selected the deployment to roll back to, verify the roll back information:

Once you have verified the details, click the Confirm Rollback button. At this point, you'll get confirmation details about the successful rollback.

If you have custom aliases, ensure the domains listed above are correct. The rolled-back deployment does not include custom aliases since these are not a part of your project’s domain settings. Custom aliases will only be included if they were present on the previous production deployment.

The rollback happens instantaneously and Vercel will point your domain and sub-domain back to the selected deployment. The production deployment tile for your project will highlight the canceled and rolled back commits.

When using Instant Rollback, Vercel will turn off auto-assignment of production domains. This means that when you or your team push changes to production, the roll backed deployment won't be replaced.

To replace the rolled back deployment, either turn on the Auto-assign Custom Production Domains toggle from the Production Environment settings of your project settings and push a new change, or perform a manual promote to a newer deployment which will automatically turn the setting on.

Only one deployment can be rolled back at a time for every project. However, a rolled back deployment stays disabled in your deployment list and can be accessed and re-reverted whenever you want

You can also roll back from the main Deployments tab in your dashboard. Filtering the deployments list by is recommended to view a list of eligible roll back deployments as this list all your current and previous deployments promoted to production.

Click the vertical ellipses (⋮) next to the deployment row and select the Instant Rollback option from the context menu.

Deployments previously aliased to a production domain are eligible for Instant Rollback. Deployments that have never been aliased to production a domain, e.g., most preview deployments, are not eligible.

To compare the manual promotion options, see Manually promoting to Production.

---

## Deploying Projects from Vercel CLI

**URL:** https://vercel.com/docs/cli/deploying-from-cli

**Contents:**
- Deploying Projects from Vercel CLI
- Deploying from source
  - Relevant commands
- Deploying a staged production build
  - Relevant commands
- Deploying from local build (prebuilt)
  - Relevant commands

The command is used to deploy Vercel Projects and can be used from either the root of the Vercel Project directory or by providing a path.

Deploys the current Vercel project, when run from the Vercel Project root.

You can alternatively use the command for the same effect, if you want to be more explicit.

Deploys the Vercel project found at the provided path, when it's a Vercel Project root.

When deploying, stdout is always the Deployment URL.

Writes the Deployment URL output from the deploy command to a text file.

By default, when you promote a deployment to production, your domain will point to that deployment. If you want to create a production deployment without assigning it to your domain, for example to avoid sending all of your traffic to it, you can:

You can build Vercel projects locally to inspect the build outputs before they are deployed. This is a great option for producing builds for Vercel that do not share your source code with the platform.

It's also useful for debugging build outputs.

Using the vercel command to deploy and write stdout to a text file.

This produces in the Build Output API format. You can review the output, then deploy with:

Deploy the build outputs in .vercel/output produced by vercel build.

Review the When not to use --prebuilt section to understand when you should not use the flag.

See more details at Build Output API.

---

## Add the Vercel Toolbar to local and production environments

**URL:** https://vercel.com/docs/vercel-toolbar/in-production-and-localhost

**Contents:**
- Add the Vercel Toolbar to local and production environments

The Vercel Toolbar is available by default on all preview environments. In production environments the toolbar supports ongoing team collaboration and project iteration. When used in development environments, you can see and resolve preview comments during development, streamlining the process of iterating on your project.

All toolbar features such as Comments, Feature Flags, Draft Mode, and Edit Mode, are available in both production and development environments.

---

## vercel logs

**URL:** https://vercel.com/docs/cli/logs

**Contents:**
- vercel logs
- Usage
- Unique options
  - Json
  - Follow
  - Limit
  - Output
  - Since
  - Until
- Global Options

The command displays and follows runtime logs data for a specific deployment. Runtime logs are produced by Middleware and Vercel Functions. You can find more detailed runtime logs on the Logs page from the Vercel Dashboard.

From the moment you run this command, all newly emitted logs will display in your terminal, for up to 5 minutes, unless you interrupt it.

Logs are pretty-printed by default, but you can use the option to display them in JSON format, which makes the output easier to parse programmatically.

Using the vercel logs command to retrieve runtime logs for a specific deployment.

These are options that only apply to the command.

The option, shorthand , changes the format of the logs output from pretty print to JSON objects. This makes it possible to pipe the output to other command-line tools, such as jq, to perform your own filtering and formatting.

Using the vercel logs command with the --json option, together with jq, to display only warning logs.

The --follow option has been deprecated since it's now the default behavior.

The option, shorthand , can be used to watch for additional logs output.

The --limit option has been deprecated as the command displays all newly emitted logs by default.

The option, shorthand , can be used to specify the number of log lines to output.

The --output option has been deprecated in favor of the --json option.

The option, shorthand , can be used to specify the format of the logs output, this can be either (default) or .

The --since option has been deprecated. Logs are displayed from when you started the command.

The option can be used to return logs only after a specific date, using the ISO 8601 format.

The --since option has been deprecated. Logs are displayed until the command is interrupted, either by you or after 5 minutes.

The option can be used to return logs only up until a specific date, using the ISO 8601 format.

The following global options can be passed when using the vercel logs command:

For more information on global options and their usage, refer to the options section.

---

## Trusted IPs

**URL:** https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/trusted-ips

**Contents:**
- Trusted IPs
- Trusted IPs security considerations
- Managing Trusted IPs
  - Manage using the dashboard
  - Go to Project Deployment Protection Settings
  - Manage Vercel Authentication
  - Manage Trusted IPs
  - Manage using the API
  - Manage using Terraform

Trusted IPs are available on Enterprise plans

Those with the owner, member and admin roles can manage Trusted IPs

With Trusted IPs enabled at the level of your project, only visitors from an allowed IP address can access your deployment. The deployment URL will return No Deployment Found for all other requests. Trusted IPs is configured by specifying a list of IPv4 addresses and IPv4 CIDR ranges.

Trusted IPs is suitable for customers who access Vercel deployments through a specific IP address. For example, limiting preview deployment access to your VPN. Trusted IPs can also be enabled in production, for example, to restrict incoming access to only requests through your external proxy.

The table below outlines key considerations and security implications when using Trusted IPs for your deployments on Vercel.

You can manage Trusted IPs through the dashboard, API, or Terraform:

From your Vercel dashboard:

Ensure Vercel Authentication is enabled. See Managing Vercel Authentication.

From the Trusted IPs section:

All your existing and future deployments will be protected with Trusted IPs for that project. Visitors to your project deployments from IP addresses not included in your list will see a No Deployment Found error page.

You can manage Trusted IPs using the Vercel API endpoint to update an existing project with the following body

You can configure Trusted IPs using in the data source in the Vercel Terraform Provider.

---

## Deploying & Redirecting Domains

**URL:** https://vercel.com/docs/domains/working-with-domains/deploying-and-redirecting

**Contents:**
- Deploying & Redirecting Domains
- Deploying your Domain
- Redirecting domains
- Redirecting domains
- Additional technical information about Domain redirects
- Programmatic redirects

Once the domain has been added to your project and configured, it is automatically applied to your latest production deployment.

The first deployment of a new project will be marked as production and subsequently assigned with your custom domain automatically.

When you assign a custom domain to a project that's using Git, each push (including merges) that you make to the production branch (commonly ) will trigger a deployment to the domain.

When you assign a domain to a different branch, you'll need to make a new deployment to the desired branch for the domain to resolve correctly.

Reverts take effect immediately, assigning the Custom Domain to the deployment made prior to the point the revert is effective from.

You can add domain redirects from the Domains tab when more than one domain is present in the project. This provides a way to, for example, redirect a subdomain to an apex domain, but can be used in a variety of ways.

If a user visits your domain with or without the "www" subdomain prefix, we will attempt to redirect automatically. You might still want to add this redirect explicitly.

To add a redirect, navigate to the Domains tab within Project Settings, then select Edit on the domain you want to redirect from. Use the Redirect to dropdown to select the domain you want to redirect to:

A domain redirect that redirects requests made to to .

Adding an apex domain to a Project on Vercel will automatically suggest adding its counterpart. Using both of these domains ensures that visitors can always access your site, regardless of whether or not they use when entering the URL.

We recommend using the subdomain as your primary domain, with a redirect from the non- domain to it. This allows the Vercel CDN more control over incoming traffic for improved reliability, speed, and security. The redirect is also cached on visitor's browsers for faster subsequent visits.

Some browsers like Google Chrome automatically hide the subdomain from the address bar, so this redirect may not affect your URL appearance.

Choosing to redirect the domain to the non- also works but provides Vercel less control over incoming traffic. Alternatively, you can choose to add only the domain you typed.

The DNS spec forbids using CNAME records on apex domains like . They are, however, allowed for subdomains like . This is why Vercel recommends primarily using a domain with a CNAME record, and adding a redirect from the non- domain to it.

Using CNAME instead of A records ensures that domains on Vercel are fast, reliable, and fault-tolerant. Unlike A records, CNAME records avoid hard-coding a specific IP address in favor of an additional lookup at the DNS level. This means that Vercel can quickly steer traffic in the case of DDoS attacks or for performance optimizations.

While we recommend using as described above, Vercel maximizes the reliability and performance of your apex domain if you choose to use it as your primary domain by leveraging the Anycast methodology. This means Vercel still supports geographically routed traffic at infinite scale if you use an A record.

You can also add redirects programmatically using frameworks and Vercel Functions. Learn more.

---

## Environment variables

**URL:** https://vercel.com/docs/environment-variables

**Contents:**
- Environment variables
- Creating environment variables
- Environment Variable size
- Environments
  - Preview environment variables
  - Development environment variables
- Integration environment variables

Environment variables are key-value pairs configured outside your source code so that each value can change depending on the Environment. These values are encrypted at rest and visible to any user that has access to the project. It is safe to use both non-sensitive and sensitive data, such as tokens.

Your source code can read these values to change behavior during the Build Step or during Function execution.

Any change you make to environment variables are not applied to previous deployments, they only apply to new deployments.

Environment variables can either be declared at the team or project level. When declared at the team level, they are available to all projects within the team. When declared at the project level, they are only available to that project.

To learn how to create and manage environment variables, see Managing environment variables.

Developers on all plans using the runtimes stated below can use a total of 64 KB in Environments Variables per-Deployment on Vercel. This limit is for all variables combined, and so no single variable can be larger than 64 KB. The total size includes any variables configured through the dashboard or the CLI.

With support for 64 KB of environment variables, you can add large values for authentication tokens, JWTs, or certificates.

Deployments using the following runtimes can support environment variables up to 64 KB:

Vercel also provides support for custom runtimes, through the Build Output API. For information on creating custom runtime support, see the following guides:

While Vercel allows environment variables up to a total of 64KB in size, Edge Functions and Middleware using the runtime are limited to 5KB per Environment Variable.

For each Environment Variable, you can select one or more Environments to apply the Variable to:

You need Vercel CLI version 22.0.0 or higher to use the features described in this section.

Preview environment variables are applied to deployments from any Git branch that does not match the Production Branch. When you add a preview environment variable, you can choose to apply to all non-production branches or you can select a specific branch.

Any branch-specific variables will override other preview environment variables with the same name. This means you don't need to replicate all your existing preview environment variables for each branch – you only need to add the values you wish to override.

You need Vercel CLI version 21.0.1 or higher to use the features described in this section.

Environment variables for local development are defined in the file. This is a plain text file that contains pairs of environment variables, that you can manually create in your project's root directory to define specific variables.

You can use the command to automatically create and populate the file (which serves the same purpose as ) with the environment variables from your Vercel project:

This command creates a file in your project's current directory with the environment variables from your Vercel project's Development environment.

If you're using , there's no need to run , as automatically downloads the Development Environment Variables into memory. For more information on the command, see the CLI docs.

For more information, see Environment variables for local development.

Integrations can automatically add environment variables to your Project Settings. In that case, the Integration that added the Variable will be displayed in your project settings:

**Examples:**

Example 1 (unknown):
```unknown
vercel env pull
Downloading Development Environment Variables for Project my-lovely-project
✅ Created .env file [510ms]
```

---

## Encryption

**URL:** https://vercel.com/docs/encryption

**Contents:**
- Encryption
- Supported TLS versions
- TLS resumption
- OCSP stapling
- Supported ciphers
- Post-quantum cryptography
- Support for HSTS
- How certificates are handled
- Full specification

Out of the box, every deployment on Vercel is served over an HTTPS connection. The SSL certificates for these unique URLs are automatically generated free of charge.

Any HTTP requests to your deployment are automatically forwarded to HTTPS using the status code:

An example showing how all requests are forwarded to .

Enabling HTTPS redirection for deployments is considered an industry standard, and therefore it is not possible to disable it. This ensures that web content is always served over a secure connection, which helps protect users' data and privacy.

If the client that is issuing requests to your deployment wants to establish a WebSocket connection, please ensure it is connecting using HTTPS. directly, as the WSS protocol does not support redirections.

​Vercel supports TLS version 1.2 and TLS version 1.3.

​Vercel supports both Session Identifiers and Session Tickets as methods for resuming a TLS connection. This can significantly improve Time To First Byte for second time visitors.

To ensure clients can validate TLS certificates as quickly as possible, we staple an OCSP response allowing them to skip a network request to check for revocation, which improves TTFB for first-time visitors.

In order to ensure the integrity of the data received and sent by any deployment running on the Vercel platform, we only support strong ciphers with forward secrecy.

The following cipher algorithms are supported:

This is the recommended configuration from Mozilla.

Vercel offers the key exchange mechanism during TLS handshakes, which protects your deployments against future quantum computing attacks. This key exchange mechanism will be negotiated automatically by your browser if you use:

The domain (and therefore all of its sub domains, which are the unique URLs set when creating a deployment) support HSTS automatically and are preloaded.

The default header for *.vercel.app

Custom domains use HSTS, but only for the particular subdomain.

The default header for custom domains

You can modify the header by configuring custom response headers in your project.

Theoretically, you could set the parameter to a different value (it indicates how long the client should remember that your site is only accessible over HTTPS), but since we do not allow connections made over HTTP, there is no point in setting it to a shorter value, as the client can just remember it forever.

You can test whether your site qualifies for HSTS Preloading here. It also allows submitting the domain to Google Chrome's hardcoded HSTS list. Making it onto that list means your site will become even faster, as it is always accessed over HTTPS right away, instead of the browser following the redirection issued by our Network layer.

The unique URLs generated when creating a deployment are handled using a wildcard certificate issued for the domain. The Vercel platform generates wildcard certificates using LetsEncrypt and keeps them updated automatically.

When custom certificates are generated using , however, their keys are placed in our database and encrypted at rest within the Network layer.

Then, once a hostname is requested, the certificate and key are read from the database and used for establishing the secure connection. In addition, both are cached in memory for optimal SSL termination performance.

Any features of the encryption mechanism that were left uncovered are documented on SSL Labs. You only need to make sure to select any IP address of your choice (it does not matter which one you pick – the results are the same for all).

---

## Request headers

**URL:** https://vercel.com/docs/headers/request-headers

**Contents:**
- Request headers
  - Custom IP
  - 1. Reading the header value
  - 2. Verifying the signature
  - 3. Getting your signature secret

The following headers are sent to each Vercel deployment and can be used to process the request before sending back a response. These headers can be read from the Request object in your Vercel Function.

This header represents the domain name as it was accessed by the client. If the deployment has been assigned to a preview URL or production domain and the client visits the domain URL, it contains the custom domain instead of the underlying deployment URL.

This header contains a list of Vercel regions your request hit, as well as the region the function was executed in (for both Edge and Serverless).

It also allows Vercel to automatically prevent infinite loops.

This header is identical to the header.

This header represents the protocol of the forwarded server, typically in production and in development.

The public IP address of the client that made the request.

If you are trying to use Vercel behind a proxy, we currently overwrite the header and do not forward external IPs. This restriction is in place to prevent IP spoofing.

Trusted Proxy is available on Enterprise plans

Enterprise customers can purchase and enable a trusted proxy to allow your custom IP. Contact us for more information.

This header is identical to the header. However, could be overwritten if you're using a proxy on top of Vercel.

This header is identical to the header.

This header represents the unique deployment, not the preview URL or production domain. For example, .

A two-character ISO 3166-1 code representing the continent associated with the location of the requester's public IP address. Codes used to identify continents are as follows:

A two-character ISO 3166-1 country code for the country associated with the location of the requester's public IP address.

A string of up to three characters containing the region-portion of the ISO 3166-2 code for the first level region associated with the requester's public IP address. Some countries have two levels of subdivisions, in which case this is the least specific one. For example, in the United Kingdom this will be a country like "England", not a county like "Devon".

The city name for the location of the requester's public IP address. Non-ASCII characters are encoded according to RFC3986.

The latitude for the location of the requester's public IP address. For example, .

The longitude for the location of the requester's public IP address. For example, .

The name of the time zone for the location of the requester's public IP address in ICANN Time Zone Database name format such as .

The postal code close to the user's location.

Vercel sends an header with requests from Webhooks, Log Drains, and other services. The header contains an HMAC-SHA1 signature that you can use to verify the request came from Vercel.

First, let's see how to read the header value from incoming requests:

When your server has a public endpoint, anyone who knows the URL can send requests to it. Verify the signature to confirm the request came from Vercel and wasn't tampered with.

Vercel creates the signature as an HMAC-SHA1 hash of the raw request body using a secret key. To verify it, generate the same hash with your secret (See Getting your signature secret) and compare the values:

The secret key you need depends on what type of request you're receiving:

For complete examples with additional error handling, see Securing webhooks and Drain security.

---

## Package Managers

**URL:** https://vercel.com/docs/package-managers

**Contents:**
- Package Managers
- Supported package managers
- Manually specifying a package manager
  - Project override
  - Deployment override

Vercel will automatically detect the package manager used in your project and install the dependencies when you create a deployment. It does this by looking at the lock file in your project and inferring the correct package manager to use.

If you are using Corepack, Vercel will use the package manager specified in the file's field instead.

The following table lists the package managers supported by Vercel, with their install commands and versions:

While Vercel automatically selects the package manager based on the lock file present in your project, the specific version of that package manager is determined by the version information in the lock file or associated configuration files.

The npm and pnpm package managers create a property when they generate a lock file. This property specifies the lock file's format version, ensuring proper processing and compatibility. For example, a file with will be interpreted by pnpm 9, while a file with will be interpreted by pnpm 7.

version 9.0 can be generated by pnpm 9 or 10. Newer projects will prefer 10, while older prefer 9. Check build logs to see which version is used for your project.

When no lock file exists, Vercel uses npm by default. Npm's default version aligns with the Node.js version as described in the table above. Defaults can be overridden using or Corepack for specific package manager versions.

You can manually specify a package manager to use on a per-project, or per-deployment basis.

To specify a package manager for all deployments in your project, use the Override setting in your project's Build & Development Settings:

When using an override install command like pnpm install, Vercel will use the oldest version of the specified package manager available in the build container. For example, if you specify pnpm install as your override install command, Vercel will use pnpm 6.

To specify a package manager for a deployment, use the property in your projects .

---

## Managing microfrontends security

**URL:** https://vercel.com/docs/microfrontends/managing-microfrontends/security

**Contents:**
- Managing microfrontends security
- Deployment Protection and microfrontends
  - Managing Deployment Protection for your microfrontend
- Vercel Firewall and microfrontends
  - Vercel WAF and microfrontends
  - Managing the Vercel WAF for your microfrontend

Understand how and where you manage Deployment Protection and Vercel Firewall for each microfrontend application.

For requests to a microfrontend host (a domain belonging to the microfrontend default application):

For requests directly to a child application (a domain belonging to a child microfrontend):

This applies to all protection methods and bypass methods, including:

Use the Deployment Protection settings for the project of the default application for the group.

For requests to a microfrontend host (a domain belonging to the microfrontend default application):

For requests directly to a child application (a domain belonging to a child microfrontend):

This applies for the entire Vercel WAF, including Custom Rules, IP Blocking, Managed Rulesets, and Attack Challenge Mode.

To set a WAF rule that applies to all requests to a microfrontend, use the Vercel WAF for your default application.

To set a WAF rule that applies only to requests to paths of a child application, use the Vercel WAF for the child project.

---

## Managing Deployments

**URL:** https://vercel.com/docs/deployments/managing-deployments

**Contents:**
- Managing Deployments
- Filter deployment
- Delete a deployment
  - Set the deployment retention policy
- Deployment protection
- Redeploy a project
  - When to Redeploy

You can manage all current and previous deployments regardless of environment, status, or branch from the dashboard. To manage a deployment from the dashboard:

Vercel CLI and Vercel REST API also provide alternative ways to manage your deployments. You can find a full list of the commands available in the Vercel CLI Reference, along with the deployments section of the Vercel REST API Reference.

You can filter your deployments based on branch, status, and deployment environment:

If you no longer need a specific deployment of your app, you can delete it from your project with the following steps:

To create an Authorization Bearer token, see the access token section of the API documentation.

To create an Authorization Bearer token, see the access token section of the API documentation.

Deleting a deployment prevents you from using instant rollback on it and might break the links used in integrations, such as the ones in the pull requests of your Git provider.

You can also set a deployment retention policy to automatically delete deployments after a certain period.

You can set the retention policy for your deployments to automatically delete them after a certain period. To learn more, see Deployment Retention.

Vercel provides a way to protect your deployments from being accessed by unauthorized users. You can use Vercel Authentication to restrict access to your deployments to only Vercel users with suitable access rights. You can also configure which environments are protected.

In addition, Enterprise teams can use Trusted IPs and Password Protection to further secure their deployments. Password protection is also available as a paid add-on for Pro teams.

To learn more, see Deployment Protection.

Vercel automatically redeploys your application when you make any commits. However, there can be situations such as bad cached data where you need to Redeploy your application to fix issues manually. To do so:

Other than your custom needs to redeploy, it's always recommended to redeploy your application to Vercel for the following use cases:

---

## Monorepos FAQ

**URL:** https://vercel.com/docs/monorepos/monorepo-faq

**Contents:**
- Monorepos FAQ
- How can I speed up builds?
- How can I make my projects available on different paths under the same domain?
- How are projects built after I push?
- Can I share source files between projects? Are shared packages supported?
- How can I use Vercel CLI without Project Linking?
- Can I use Turborepo on the Hobby plan?
- Can I use Nx with environment variables on Vercel?

Whether or not your deployments are queued depends on the amount of Concurrent Builds you have available. Hobby plans are limited to 1 Concurrent Build, while Pro or Enterprise plans can customize the amount on the "Billing" page in the team settings.

Learn more about Concurrent Builds.

After having set up your monorepo as described above, each of the directories will be a separate Vercel project, and therefore be available on a separate domain.

If you'd like to host multiple projects under a single domain, you can create a new project, assign the domain in the project settings, and proxy requests to the other upstream projects. The proxy can be implemented using a file with the rewrites property, where each is the path under the main domain and each is the upstream project domain.

Pushing a commit to a Git repository that is connected with multiple Vercel projects will result in multiple deployments being created and built in parallel for each.

To access source files outside the Root Directory, enable the Include source files outside of the Root Directory in the Build Step option in the Root Directory section within the project settings.

For information on using Yarn workspaces, see Deploying a Monorepo Using Yarn Workspaces to Vercel.

Vercel projects created after August 27th 2020 23:50 UTC have this option enabled by default. If you're using Vercel CLI, at least version 20.1.0 is required.

Vercel CLI will accept Environment Variables instead of Project Linking, which can be useful for deployments from CI providers. For example:

Learn more about Vercel CLI for custom workflows.

Yes. Turborepo is available on all plans.

When using Nx on Vercel with environment variables, you may encounter an issue where some of your environment variables are not being assigned the correct value in a specific deployment.

This can happen if the environment variable is not initialized or defined in that deployment. If that's the case, the system will look for a value in an existing cache which may or may not be the value you would like to use. It is a recommended practice to define all environment variables in each deployment for all monorepos.

With Nx, you also have the ability to prevent the environment variable from using a cached value. You can do that by using Runtime Hash Inputs. For example, if you have an environment variable in your project, you will add the following line to your configuration file:

---

## Sensitive environment variables

**URL:** https://vercel.com/docs/environment-variables/sensitive-environment-variables

**Contents:**
- Sensitive environment variables
- Creating sensitive environment variables
- Edit sensitive environment variables
- Environment variables policy

Sensitive environment variables are environment variables whose values are non-readable once created. They help protect sensitive information stored in environment variables, such as API keys.

To mark an existing environment variable as sensitive, remove and re-add it with the Sensitive option enabled. Once you mark it as sensitive, Vercel stores the variable in an unreadable format. This is only possible for environment variables in the production and preview environments.

Both project environment variables and shared environment variables can be marked as sensitive.

You can only create sensitive environment variables in the preview and production environments.

Sensitive environment variables can be created at the project or team level:

To create an Authorization Bearer token, see the access token section of the API documentation.

To create an Authorization Bearer token, see the access token section of the API documentation.

You can edit the value and environment for a sensitive environment variable. You cannot edit the key of a sensitive environment variable.

Users with the owner role can set a team-wide environment variable policy for creating environment variables. Once enabled, all newly created environment variables in the Production and/or Preview environments will be sensitive environment variables.

---

## Add the Vercel Toolbar to your production environment

**URL:** https://vercel.com/docs/vercel-toolbar/in-production-and-localhost/add-to-production

**Contents:**
- Add the Vercel Toolbar to your production environment
- Adding the toolbar using the browser extension
- Adding the toolbar using the package
  - Install the package and link your project
  - Add the toolbar to your project
  - Managing notifications and integrations for Comments on production
- Enabling the Vercel Toolbar
  - Disabling the toolbar
- Acessing the toolbar using the Vercel dashboard
- Accessing the toolbar using the Browser extension

As a team owner or member, you can enable the toolbar in your production environment for sites that your team(s) own, either through the dashboard or by adding the package to your project.

For team members that use supported browsers and want the most straightforward experience, we recommend using the Vercel Browser Extension to get access to the toolbar on your team's production sites.

For team members that use browsers for which a Vercel extension is not available, to allow toolbar access for everyone that accesses your site, or if you have more complex rules for when it shows in production, you'll need to add the package to your project.

For team members that do not use the browser extension or if you have more complex rules for when the toolbar shows in production, you can add the package to your project:

Install the package in your project using the following command:

Then link your local project to your Vercel project with the command using Vercel CLI.

Before using the Vercel Toolbar in a production deployment Vercel recommends conditionally injecting the toolbar. Otherwise, all visitors will be prompted to log in when visiting your site.

The following example demonstrates code that will show the Vercel Toolbar to a team member on a production deployment.

Unlike comments on preview deployments, alerts for new comments won't be sent to a specific user by default. Vercel recommends linking your project to Slack with the integration, or directly mentioning someone when starting a new comment thread in production to ensure new comments are seen.

Alternatively to using the package, you can enable access to the Vercel Toolbar for your production environment at the team or project level. Once enabled, team members can access the toolbar using the Vercel Browser Extension or by enabling it in the toolbar menu.

If you have noticed that the toolbar is showing up for team members on your production sites, you can disable it at either the team or project level:

You can send team members and users a production deployment with the Vercel Toolbar included from the dashboard. To do so:

This will not show for users who have the browser extension installed, as the extension will already show the toolbar whenever you visit your production deployment unless it is disabled in team or project settings.

Provided the Vercel toolbar is enabled for your project, any team member can use the Vercel Toolbar in your production environment by installing the Vercel Browser Extension. The extension allows you to access the toolbar on any website hosted on Vercel that your team(s) own:

Provided the Vercel toolbar is enabled for your project, you can enable the toolbar on production environments from the toolbar menu:

---

## Production checklist for launch

**URL:** https://vercel.com/docs/production-checklist

**Contents:**
- Production checklist for launch
- Operational excellence
- Security
- Reliability
- Performance
- Cost optimization
- Enterprise support

When launching your application on Vercel, it is important to ensure that it's ready for production. This checklist is prepared by the Vercel engineering team and designed to help you prepare your application for launch by running through a series of questions to ensure:

Define an incident response plan for your team, including escalation paths, communication channels, and rollback strategies for deployments

Familiarize yourself with how to stage, promote and rollback deployments

Ensure caching is configured if deploying using a monorepo to prevent unnecessary builds

Perform a zero downtime migration to Vercel DNS

Implement a Content Security Policy (CSP) and proper security headers

Enable Deployment Protection to prevent unauthorized access to your deployments

Configure the Vercel Web Application Firewall (WAF) to monitor, block, and challenge incoming traffic. This includes setting up custom rules, IP blocking, and enabling managed rulesets for enhanced security

Enable Log Drains to persist logs from your deployments

Review common SSL certificate issues

Enable a Preview Deployment Suffix to use a custom domain for Preview Deployments

Commit your lockfiles to pin dependencies and speed up builds through caching

Consider implementing rate limiting to prevent abuse

Review and implement access roles to ensure the correct permissions are set for your team members

Enable SAML SSO and SCIM (Enterprise plans with Owner role only)

Enable Audit Logs to track and analyze team member activity (Enterprise plans with Owner role only)

Ensure that cookies comply with the allowed cookie policy to enhance security. (Enterprise plans with Owner role only)

Setup a firewall rule to block requests from unwanted bots to your project deployment

Enable Observability Plus to debug and optimize performance, investigate errors, monitor traffic, and more (Available on Pro and Enterprise plans)

Enable automatic Function failover to add multi-region redundancy and protect against regional outages (Enterprise plans only)

If using Secure Compute, enable a passive failover region to ensure continued operation during regional outages (Enterprise plans only)

Implement caching headers for static assets or Function responses to reduce usage or origin requests

Understand the differences between caching headers and Incremental Static Regeneration

Consider adding Tracing to instrument your application for distributed tracing

Consider running a load test on your application to stress your upstream services (Enterprise plans only)

Enable Speed Insights for instant access to field performance data and Core Web Vitals

Review your Time To First Byte (TTFB) to ensure your application is responding quickly

Ensure you are using Image Optimization to reduce the size of your images

Ensure you are using Script Optimization to optimize script loading performance

Ensure you are using Font Optimization to remove external network requests for improved privacy and performance

Ensure your Vercel Function region is the same as your origin API or database

Consider the limitations of placing a third-party proxy in front of Vercel, and notify your Customer Success Manager (CSM) or Account Executive (AE) (Enterprise customers) for guidance

Enable Fluid compute to reduce cold starts, optimize concurrency, and enhance function scalability

Follow our manage and optimize usage guides to understand how to optimize your usage, and manage your costs

Configure Spend Management to manage your usage and trigger alerts on usage changes

Review or adjust the maximum duration, and memory for your Vercel Functions

Ensure Incremental Static Regeneration (ISR) revalidation times are set appropriately to match content changes or move to on-demand revalidation

For teams created before February 18th, 2025, opt in to the new image optimization pricing to ensure the lowest cost, and review best practices.

Move large media files such as GIFs and videos to blob storage

Need help with your production rollout?

---

## Deployment Protection on Vercel

**URL:** https://vercel.com/docs/deployment-protection

**Contents:**
- Deployment Protection on Vercel
- Configuring Deployment Protection
- Understanding Deployment Protection by environment
  - Standard Protection
    - Migrating to Standard Protection
  - All deployments
  - Only production deployments
  - (Legacy) Standard Protection
  - (Legacy) Only Preview Deployments
- Advanced Deployment Protection

Deployment Protection safeguards both your preview and production URLs across various environments. Configured at the project level through your settings, Deployment Protection provides detailed access control for different deployment types.

Vercel offers the following Deployment Protection features:

Deployment protection requires authentication for all requests, including those to Middleware.

Deployment Protection is managed through your project settings. To configure Deployment Protection:

You can configure the type of Deployment Protection for each environment in your project depending on your projects security needs. When choosing your protection method, you can select from three options:

To protect only production URLs, you can use Trusted IPs. Note that this option is only available on the Enterprise plan.

Standard Protection is available on all plans

Standard Protection is the recommended way to secure your deployments, as it protects all domains except Production Custom Domains.

Standard Protection can be configured with the following Deployment Protection features:

Enabling Standard Protection restricts public access to the production generated deployment URL. This affects and from System Environment Variables, making them unsuitable for fetch requests.

If you are using or to make fetch requests, you will need to update your requests to target the same domain the user has requested.

The Framework Environment Variable is prefixed with the name of the framework. For example, for Next.js is , and for Nuxt is . See the Framework Environment Variables documentation for more information.

For client-side requests, use relative paths in the fetch call to target the current domain, automatically including the user's authentication cookie for protected URLs.

For server-side requests, use the origin from the incoming request and manually add request cookies to pass the user's authentication cookie.

Bypassing protection using Protection Bypass for Automation is an option but not required for requests targeting the same domain.

Protecting all deployments is available on Enterprise plansor with the Advanced Deployment Protection add-on for Pro plans

Selecting All Deployments secures all deployments, both preview and production, restricting public access entirely.

With this configuration, all URLs, including your production domain and generated URLs like , are protected.

Protecting all deployments can be configured with the following Deployment Protection features:

Protecting production deployments is available on Enterprise plans

Restrict access to protected deployments to a list of Trusted IPs.

Preview deployment URLs remain publicly accessible. This feature is only available on the Enterprise plan.

(Legacy) Standard Protection is a legacy feature that protects all preview URLs and deployment URLs. All up to date production URLs are unprotected.

Selecting (Legacy) Only Preview Deployments protects preview URLs, while the production environment remains publicly accessible.

For example, Vercel generates a preview URL such as , which will be protected. In contrast, all production URLs, including any past or current generated production branch URLs like , remain accessible.

Advanced Deployment Protection features are available to Enterprise customers by default. Customers on the Pro plan can access these features for an additional $150 per month, including:

To opt-into Advanced Deployment Protection while on a Pro plan:

When you enable Advanced Deployment Protection, you will be charged $150 per month for the add-on, and will have access to all Advanced Deployment Protection features.

To opt out of Advanced Deployment Protection:

In order to disable Advanced Deployment Protection, you must have been using the feature for a minimum of thirty days. After this time, once cancelled, all Advanced Deployment Protection features will be disabled.

---

## Anatomy of the Checks API

**URL:** https://vercel.com/docs/checks/creating-checks

**Contents:**
- Anatomy of the Checks API
  - Types of Checks
  - Associations
  - Body attributes
  - Response
  - Response codes
- Rich results
  - Output
  - Metrics
  - Rerunning checks

Checks API extends the build and deploy process once your deployment is ready. Each check behaves like a webhook that triggers specific events, such as , , and . The test are verified before domains are assigned.

To learn more, see the Supported Webhooks Events docs.

The workflow for registering and running a check is as follows:

If a check is "rerequestable", your integration users get an option to rerequest and rerun the failing checks.

Depending on the type, checks can block the domain assignment stage of deployments.

A blocking check with a state is configured by the developer (and not the integration).

Checks are always associated with a specific deployment that is tested and validated.

The check gets a status if there is no status update for more than one hour (). The same applies if the check is running () for more than five minutes.

The property can store any data like Web Vitals and Virtual Experience Score. It is defined under a field:

Each of these keys has the following properties:

makes Web Vitals visible on checks. It is defined inside as follows:

All fields are required except previousValue. If previousValue is present, the delta will be shown.

A check can be "rerequested" using the webhook. Add the attribute, and you can rerequest failed checks.

A rerequested check triggers the webhook. It updates the check to and resets the , , , and fields.

You can "Skip" to stop and ignore check results without affecting the alias assignment. You cannot skip active checks. They continue running until built successfully, and assign domains as the last step.

For "Running Checks", only the Automatic Deployment URL is available. Automatic Branch URL and Custom Domains will apply once the checks finish.

Checks may take different times to run. Each integrator determines the running order of the checks. While Vercel REST API determines the order of check results.

When Checks API begins running on your deployment, the is set to . Once it gets a , the updates to . This results in a successful deployment.

However, your deployment will fail if the updates to one of the following values:

---

## Promoting Deployments

**URL:** https://vercel.com/docs/deployments/promoting-a-deployment

**Contents:**
- Promoting Deployments
- Instant Rollback
- Promote a deployment from preview to production
- Staging and promoting a production deployment
  - CLI
  - Dashboard
- Production deployment state

By default, when you merge to or make commits to your production branch (often ), Vercel will automatically promote the changes to Production. However, there are a number of ways to manually change which deployment is served to people who visit your production domain:

Use this when you want to replace the current production deployment with another deployment that has already been serving as current in the past. Instant Rollback is a faster process since it involves assigning domains to an existing deployment rather than a complete rebuild and is ideal to quickly recover from an incident in production to roll back. However, because it does not do a complete rebuild, items such as environment variables will not be rebuilt.

For more information on how and when to use it, see the Instant Rollback docs.

There may be times when you need to promote an existing preview deployment to production, such as when you need to temporarily use a branch that isn't set as the production branch.

To promote an existing preview deployment to production on Vercel, do the following:

If you have different Environment Variables set for preview and production deployments then the variables used will change from preview to those you have linked to the production environment. You cannot use your preview environment variables in a production deployment

In some cases you may want to create a production-like deployment to use as a staging environment before promoting it to production.

In this scenario, you can turn off the auto-assignment of domains for your production build, as described below. Turning off the auto-assignment of domains means the deployment won't automatically be served to your production traffic, but also means you must manually promote it to production.

For steps on using this workflow in the CLI, see Deploying a staged production build.

Vercel will instantly promote the deployment; it doesn't require a rebuild. Once promoted, the deployment is marked as Current.

Your production deployments could be in one of three states:

---

## Supported Node.js versions

**URL:** https://vercel.com/docs/functions/runtimes/node-js/node-js-versions

**Contents:**
- Supported Node.js versions
- Default and available versions
- Setting the Node.js version in project settings
- Version overrides in
- Checking your deployment's Node.js version

By default, a new project uses the latest Node.js LTS version available on Vercel.

Current available versions are:

Only major versions are available. Vercel automatically rolls out minor and patch updates when needed, such as to fix a security issue.

To override the default version and set a different Node.js version for new deployments:

You can define the major Node.js version in the section of the to override the one you have selected in the Project Settings:

For instance, when you set the Node.js version to 20.x in the Project Settings and you specify a valid semver range for Node.js 24 (e.g. ) in , your project will be deployed with the latest 24.x version of Node.js.

The following table lists some example version ranges and the available Node.js version they map to:

To verify the Node.js version your Deployment is using, either run in the Build Command or log .

---

## Microfrontends Configuration

**URL:** https://vercel.com/docs/microfrontends/configuration

**Contents:**
- Microfrontends Configuration
- Schema
- Example
- Application Naming
- File Naming

The file is used to configure your microfrontends. If this file is not deployed with your default application, the deployment will not be a microfrontend.

If the application name differs from the field in for the application, you should either rename the name field in to match or add the field to the microfrontends configuration.

The microfrontends configuration file can be named either or .

You can also define a custom configuration file by setting the environment variable — for example, . The file name must end with either or , and it may include a path, such as . The filename / path specified is relative to the root directory for the default application.

Be sure to add the environment variable to all projects within the microfrontends group.

Using a custom file name allows the same repository to support multiple microfrontends groups, since each group can have its own configuration file.

If you're using Turborepo, define the environment variable outside of the Turbo invocation when running , so the local proxy can detect and use the correct configuration file.

---

## Backends on Vercel

**URL:** https://vercel.com/docs/frameworks/backend

**Contents:**
- Backends on Vercel
- Zero-configuration backends
  - Elysia
  - Express
  - FastAPI
  - Fastify
  - Flask
  - H3
  - Hono
  - NestJS

Backends deployed to Vercel receive the benefits of Vercel's infrastructure, including:

Deploy the following backends to Vercel with zero-configuration.

Ergonomic framework for humans

Fast, unopinionated, minimalist web framework for Node.js

FastAPI framework, high performance, easy to learn, fast to code, ready for production

Fast and low overhead web framework, for Node.js

The Python micro web framework

Universal, Tiny, and Fast Servers

Web framework built on Web Standards

Framework for building efficient, scalable Node.js server-side applications

Nitro is a next generation server toolkit.

The MCP framework for building AI-powered tools

If you are transitioning from a fully managed server or containerized environment to Vercel’s serverless architecture, you may need to rethink a few concepts in your application since there is no longer a server always running in the background.

The following are generally applicable to serverless, and therefore Vercel Functions (running with or without Fluid compute).

Serverless functions have maximum execution limits and should respond as quickly as possible. They should not subscribe to data events. Instead, we need a client that subscribes to data events and a serverless functions that publishes new data. Consider using a serverless friendly realtime data provider.

To manage database connections efficiently, use the function from .

---

## Deploy MCP servers to Vercel

**URL:** https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel

**Contents:**
- Deploy MCP servers to Vercel
- Deploy a Template
- Deploy MCP servers efficiently
- Deploy an MCP server on Vercel
  - Test the MCP server locally
  - Configure an MCP host
- Enabling authorization
  - Secure your server with OAuth
  - Expose OAuth metadata endpoint
    - How to add OAuth metadata endpoint

Deploy your Model Context Protocol (MCP) servers on Vercel to take advantage of features like Vercel Functions, OAuth, and efficient scaling for AI applications.

Get started in minutes

ChatGPT app with Next.js

Ship a ChatGPT app on Vercel with Next.js and Model Context Protocol (MCP).

A fullstack template for using x402 with MCP and AI SDK.

Run an Model Context Protocol (MCP) server on Vercel with Next.js.

Vercel provides the following features for production MCP deployments:

Use the package and create the following API route to host an MCP server that provides a single tool that rolls a dice.

This assumes that your MCP server application, with the above-mentioned API route, runs locally at .

When you deploy your application on Vercel, you will get a URL such as .

Using Cursor, add the URL of your MCP server to the configuration file in Streamable HTTP transport format.

You can now use your MCP roll dice tool in Cursor's AI chat or any other MCP client.

The provides built-in OAuth support to secure your MCP server. This ensures that only authorized clients with valid tokens can access your tools.

To add OAuth authorization to the MCP server you created in the previous section:

To comply with the MCP specification, your server must expose a metadata endpoint that provides OAuth configuration details. Among other things, this endpoint allows MCP clients to discover, how to authorize with your server, which authorization servers can issue valid tokens, and what scopes are supported.

To view the full list of values available to be returned in the OAuth Protected Resource Metadata JSON, see the protected resource metadata RFC.

MCP clients that are compliant with the latest version of the MCP spec can now securely connect and invoke tools defined in your MCP server, when provided with a valid OAuth token.

Learn how to deploy MCP servers on Vercel, connect to them using the AI SDK, and explore curated lists of public MCP servers.

---

## LiteLLM

**URL:** https://vercel.com/docs/ai-gateway/framework-integrations/litellm

**Contents:**
- LiteLLM
- Getting started
  - Create a new project
  - Install dependencies
  - Configure environment variables
  - Create your LiteLLM application
  - Running the application

LiteLLM is an open-source library that provides a unified interface to call LLMs. This guide demonstrates how to integrate Vercel AI Gateway with LiteLLM to access various AI models and providers.

First, create a new directory for your project:

Install the required LiteLLM Python package:

Create a file with your Vercel AI Gateway API key:

If you're using the AI Gateway from within a Vercel deployment, you can also use the environment variable which will be automatically provided.

Create a new file called with the following code:

Run your Python application:

You should see a response from the AI model in your console.

---

## vercel bisect

**URL:** https://vercel.com/docs/cli/bisect

**Contents:**
- vercel bisect
- Usage
- Unique Options
  - Good
  - Bad
  - Path
  - Open
  - Run
- Global Options
- Related guides

The command can be used to perform a binary search upon a set of deployments in a Vercel Project for the purpose of determining when a bug was introduced.

This is similar to git bisect but faster because you don't need to wait to rebuild each commit, as long as there is a corresponding Deployment. The command works by specifing both a bad Deployment and a good Deployment. Then, will retrieve all the deployments in between, and step by them one by one. At each step, you will perform your check and specify whether or not the issue you are investigating is present in the Deployment for that step.

Note that if an alias URL is used for either the good or bad deployment, then the URL will be resolved to the current target of the alias URL. So if your Project is currently in promote/rollback state, then the alias URL may not be the newest chronological Deployment.

The good and bad deployments provided to must be production deployments.

Using the vercel bisect command will initiate an interactive prompt where you specify a good deployment, followed by a bad deployment and step through the deployments in between to find the first bad deployment.

These are options that only apply to the command.

The option, shorthand , can be used to specify the initial "good" deployment from the command line. When this option is present, the prompt will be skipped at the beginning of the bisect session. A production alias URL may be specified for convenience.

Using the vercel bisect command with the --good option.

The option, shorthand , can be used to specify the "bad" deployment from the command line. When this option is present, the prompt will be skipped at the beginning of the bisect session. A production alias URL may be specified for convenience.

Using the vercel bisect command with the --bad option.

The option, shorthand , can be used to specify a subpath of the deployment where the issue occurs. The subpath will be appended to each URL during the bisect session.

Using the vercel bisect command with the --path option.

The option, shorthand , will attempt to automatically open each deployment URL in your browser window for convenience.

Using the vercel bisect command with the --open option.

The option, shorthand , provides the ability for the bisect session to be automated using a shell script or command that will be invoked for each deployment URL. The shell script can run an automated test (for example, using the curl command to check the exit code) which the bisect command will use to determine whether each URL is good (exit code 0), bad (exit code non-0), or should be skipped (exit code 125).

Using the vercel bisect command with the --run option.

The following global options can be passed when using the vercel bisect command:

For more information on global options and their usage, refer to the options section.

---

## Microfrontends path routing

**URL:** https://vercel.com/docs/microfrontends/path-routing

**Contents:**
- Microfrontends path routing
- Add a new path to a microfrontend
  - Supported path expressions
- Asset Prefix
  - Next.js
- Setting a default route
- Routing to externally hosted applications
- Routing changes safely with flags
  - Specify a flag name
  - Add microfrontends middleware

Vercel handles routing to microfrontends directly in Vercel's network infrastructure, simplifying the setup and improving latency. When Vercel receives a request to a domain that uses microfrontends, we read the file in the live deployment to decide where to route it.

You can also route paths to a different microfrontend based on custom application logic using middleware.

To route paths to a new microfrontend, modify your file. In the section for the project, add the new path:

The routing for this new path will take effect when the code is merged and the deployment is live. You can test the routing changes in Preview or pre-Production to make sure it works as expected before rolling out the change to end users.

Additionally, if you need to revert, you can use Instant Rollback to rollback the project to a deployment before the routing change to restore the old routing rules.

Changes to separate microfrontends are not rolled out in lockstep. If you need to modify , make sure that the new application can handle the requests before merging the change. Otherwise use flags to control whether the path is routed to the microfrontend.

You can use following path expressions in :

The following are not supported:

Test your path expression

To assert whether the path expressions will work for your path, use the test utility to add unit tests that ensure paths get routed to the correct microfrontend.

An asset prefix is a unique prefix prepended to paths in URLs of static assets, like JavaScript, CSS, or images. This is needed so that URLs are unique across microfrontends and can be correctly routed to the appropriate project. Without this, these static assets may collide with each other and not work correctly.

When using , a default auto-generated asset prefix is automatically added. The default value is an obfuscated hash of the project name, like , in order to not leak the project name to users.

If you would like to use a human readable asset prefix, you can also set the asset prefix that is used in .

Changing the asset prefix is not guaranteed to be backwards compatible. Make sure that the asset prefix that you choose is routed to the correct project in production before changing the field.

JavaScript and CSS URLs are automatically prefixed with the asset prefix, but content in the directory needs to be manually moved to a subdirectory with the name of the asset prefix.

Some functionality in the Vercel Dashboard, such as screenshots and links to the deployment domain, automatically links to the path. Microfrontends deployments may not serve any content on the path so that functionality may appear broken. You can set a default route in the dashboard so that the Vercel Dashboard instead always links to a valid route in the microfrontends deployment.

To update the default route, visit the Microfrontends Settings page.

Deployments created after this change will now use the provided path as the default route.

If a microfrontend is not yet hosted on Vercel, you can create a new Vercel project to rewrite requests to the external application. You will then use this Vercel project in your microfrontends configuration on Vercel.

If you want to dynamically control the routing for a path, you can use flags to make sure that the change is safe before enabling the routing change permanently. Instead of automatically routing the path to the microfrontend, the request will be sent to the default application which then decides whether the request should be routed to the microfrontend.

This is compatible with the Flags SDK or it can be used with custom feature flag implementations.

If using this with the Flags SDK, make sure to share the same value of the environment between all microfrontends in the same group.

In your file, add a name in the field for the group of paths:

Instead of being automatically routed to the microfrontend, requests to will now be routed to the default application to make the decision about routing.

The package uses middleware to route requests to the correct location for flagged paths and based on what microfrontends were deployed for your commit. Only the default application needs microfrontends middleware.

You can add it to your Next.js application with the following code:

Your middleware matcher should include . This endpoint is used by the client to know which application the path is being routed to for prefetch optimizations. The client will make a request to this well known endpoint to fetch the result of the path routing decision for this session.

Make sure that any flagged paths are also configured in the middleware matcher so that middleware runs for these paths.

Any function that returns can be used as the implementation of the flag. This also works directly with feature flags on Vercel.

If the flag returns true, the microfrontends middleware will route the path to the microfrontend specified in . If it returns false, the request will continue to be handled by the default application.

We recommend setting up and tests to prevent many common middleware misconfigurations.

Vercel automatically determines which deployment to route a request to for the microfrontends projects in the same group. This allows developers to build and test any combination of microfrontends without worrying have to build them all on the same commit.

Domains that use this microfrontends routing will have an M icon next to the name on the deployment page.

Microfrontends routing for a domain is set when a domain is created or updated, for example when a deployment is built, promoted, or rolled back. The rules for routing are as follows:

Domains assigned to the production environment will always route to each project's current production deployment. This is the same deployment that would be reached by accessing the project's production domain. If a microfrontends project is rolled back for example, then the microfrontends routing will route to the rolled back deployment.

Domains assigned to a custom environment will route requests to other microfrontends to custom environments with the same name, or fallback based on the fallback environment configuration.

Automatically generated branch URLs will route to the latest built deployment for the project on the branch. If no deployment exists for the project on the branch, routing will fallback based on the fallback environment configuration.

Automatically generated deployment URLs are fixed to the point in time they were created. Vercel will route requests to other microfrontends to deployments created for the same commit, or a previous commit from the branch if not built at that commit.

If there is no deployment for the commit or branch for the project at that point in time, routing will fallback to the deployment at that point in time for the fallback environment.

To identify which microfrontend is responsible for serving a specific path, you can use the Deployment Summary or the Vercel Toolbar.

---

## Git Configuration

**URL:** https://vercel.com/docs/project-configuration/git-configuration

**Contents:**
- Git Configuration
- git.deploymentEnabled
  - Matching multiple branches
  - Branches matching multiple rules
  - Turning off all automatic deployments
- github.autoAlias
- github.autoJobCancelation
- Legacy
  - github.silent
  - github.enabled

The following configuration options can be used through a file like the Project Configuration.

Type: of key branch identifier and value , or .

Specify branches that should not trigger a deployment upon commits. By default, any unspecified branch is set to .

Use minimatch syntax to define behavior for multiple branches.

The example below prevents automated deployments for any branch that starts with .

If a branch matches multiple rules and at least one rule is , a deployment will occur.

A branch named will create a deployment.

To turn off automatic deployments for all branches, set the property value to .

When set to , Vercel for GitHub will create preview deployments upon merge.

Follow the deploying a staged production build workflow instead of this setting.

When set to false, Vercel for GitHub will always build pushes in sequence without cancelling a build for the most recent commit.

The property has been deprecated in favor of the new settings in the dashboard, which allow for more fine-grained control over which comments appear on your connected Git repositories. These settings can be found in the Git section of your project's settings.

When set to , Vercel for GitHub will stop commenting on pull requests and commits.

The property has been deprecated in favor of git.deploymentEnabled, which allows you to disable auto-deployments for your project.

When set to , Vercel for GitHub will not deploy the given project regardless of the GitHub app being installed.

---

## Hono on Vercel

**URL:** https://vercel.com/docs/frameworks/backend/hono

**Contents:**
- Hono on Vercel
- Get started with Hono on Vercel
  - Get started with Vercel CLI
- Exporting the Hono application
  - Local development
- Middleware
  - Hono Middleware
  - Vercel Routing Middleware
- Serving static assets
- Vercel Functions

Hono is a fast and lightweight web application framework built on Web Standards. You can deploy a Hono app to Vercel with zero configuration.

Start with Hono on Vercel by using the following Hono template to deploy to Vercel with zero configuration:

Vercel deployments can integrate with your git provider to generate preview URLs for each pull request you make to your Hono project.

Get started by initializing a new Hono project using Vercel CLI init command:

This will clone the Hono example repository in a directory called .

To run a Hono application on Vercel, create a file that imports the package at any one of the following locations:

To run your Hono application locally, use Vercel CLI:

This ensures that the application will use the default export to run the same as when deployed to Vercel. The application will be available on your .

Hono has the concept of "Middleware" as a part of the framework. This is different from Vercel Routing Middleware, though they can be used together.

In Hono, Middleware runs before a request handler in the framework's router. This is commonly used for loggers, CORS handling, or authentication. The code in the Hono application might look like this:

More examples of Hono Middleware can be found in the Hono documentation.

In Vercel, Routing Middleware executes code before a request is processed by the application. This gives you a way to handle rewrites, redirects, headers, and more, before returning a response. See the Routing Middleware documentation for examples.

To serve static assets, place them in the directory. They will be served as a part of our CDN using default headers unless otherwise specified in .

Hono's will be ignored and will not serve static assets.

When you deploy a Hono app to Vercel, your server routes automatically become Vercel Functions and use Fluid compute by default.

Vercel Functions support streaming which can be used with Hono's function.

Learn more about deploying Hono projects on Vercel with the following resources:

---

## Vercel Agent

**URL:** https://vercel.com/docs/agent

**Contents:**
- Vercel Agent
- Features
  - Code Review
  - Investigation
- Getting started
- Pricing
- Privacy

Vercel Agent is available in Beta on Enterprise and Pro plans

Vercel Agent is a suite of AI-powered development tools built to speed up your workflow. Instead of spending hours debugging production issues or waiting for code reviews, Agent helps you catch problems faster and resolve incidents quickly.

Agent works because it already understands your application. Vercel builds your code, deploys your functions, and serves your traffic. Agent uses this deep context about your codebase, deployment history, and runtime behavior to provide intelligent assistance right where you need it.

Everything runs on Vercel's AI Cloud, infrastructure designed specifically for AI workloads. This means Agent can use secure sandboxes to reproduce issues, access the latest models, and provide reliable results you can trust.

Get automatic code reviews on every pull request. Code Review analyzes your changes, identifies potential issues, and suggests fixes you can apply directly.

Learn more in the Code Review docs.

When error alerts fire, Vercel Agent Investigations can analyze what's happening to help you debug faster. Instead of manually digging through logs and metrics, AI does the analysis and shows you what might be causing the issue.

Learn more in the Agent Investigation docs.

You can enable Vercel Agent in the Agent tab of your dashboard. Setup varies by feature:

Vercel Agent uses a credit-based system. Each review or investigation costs a fixed $0.30 USD plus token costs billed at the Agent's underlying AI provider's rate, with no additional markup. Pro teams can redeem a $100 USD promotional credit when enabling Agent.

You can purchase credits and enable auto-reload in the Agent tab of your dashboard. For complete pricing details, credit management, and cost tracking information, see Vercel Agent Pricing.

Vercel Agent doesn't store or train on your data. It only uses LLMs from providers on our subprocessor list, and we have agreements in place that don't allow them to train on your data.

---

## Using Monorepos

**URL:** https://vercel.com/docs/monorepos

**Contents:**
- Using Monorepos
- Deploy a template monorepo
  - Turborepo
  - Nx
- Add a monorepo through the Vercel Dashboard
- Add a monorepo through Vercel CLI
- When does a monorepo build occur?
  - Skipping unaffected projects
    - Requirements
    - Disable the skipping unaffected projects feature

Monorepos allow you to manage multiple projects in a single directory. They are a great way to organize your projects and make them easier to work with.

Get started with monorepos on Vercel in a few minutes by using one of our monorepo quickstart templates.

Once you've created a separate project for each of the directories within your Git repository, every commit will issue a deployment for all connected projects and display the resulting URLs on your pull requests and commits:

The number of Vercel Projects connected with the same Git repository is limited depending on your plan.

You should use Vercel CLI 20.1.0 or newer.

Alternatively, you can use git clone to create multiple copies of your monorepo in different directories and link each one to a different Vercel Project.

See this example of a monorepo with Yarn Workspaces.

By default, pushing a commit to your monorepo will create a deployment for each of the connected Vercel projects. However, you can choose to:

A project in a monorepo is considered to be changed if any of the following conditions are true:

Vercel automatically skips builds for projects in a monorepo that are unchanged by the commit.

This setting does not occupy concurrent build slots, unlike the Ignored Build Step feature, reducing build queue times.

To disable this behavior, visit the project's Root Directory settings.

If you want to cancel the Build Step for projects if their files didn't change, you can do so with the Ignored Build Step project setting. Canceled builds initiated using the ignore build step do count towards your deployment and concurrent build limits and so skipping unaffected projects may be a better option for monorepos with many projects.

If you have created a script to ignore the build step, you can skip the the script when redeploying or promoting your app to production. This can be done through the dashboard when you click on the Redeploy button, and unchecking the Use project's Ignore Build Step checkbox.

When working in a monorepo with multiple applications—such as a frontend and a backend—it can be challenging to manage the connection strings between environments to ensure a seamless experience. Traditionally, referencing one project from another requires manually setting URLs or environment variables for each deployment, in every environment.

With Related Projects, this process is streamlined, enabling teams to:

For example, if your monorepo contains:

Related Projects can ensure that each preview deployment of the frontend automatically references the corresponding preview deployment of the backend, avoiding the need for hardcoded environment variables when testing changes that span both projects.

Specify the projects your app needs to reference in a configuration file at the root of the app. While every app in your monorepo can list related projects in their own , you can only specify up to three related projects per app.

This will make the preview, and production hosts of available as an environment variable in the deployment of the project.

You can find your project ID in the project Settings page in the Vercel dashboard.

The next deployment will have the environment variable set containing the urls of the related projects for use.

View the data provided for each project in the package.

For easy access to this information, you can use the npm package:

---

## Deployment Retention

**URL:** https://vercel.com/docs/deployment-retention

**Contents:**
- Deployment Retention
- Setting a deployment retention policy
  - Viewing deployment retention policy
- Restoring a deleted deployment
- More resources

Deployment Retention is available on all plans

Deployment retention refers to the configured policies that determine how long different types of deployments are kept before they are automatically deleted.

These configured retention policies allow you to control how long your deployment data is stored, providing:

Vercel provides unlimited deployment retention for all deployments, regardless of the plan that you are on.

You can configure retention durations for the following deployment states:

The latest production deployment will always be retained, regardless of the retention policy.

For example, imagine you created a production deployment with a 60-day retention period on 01/01/2024 and later replaced it with a newer deployment. The origin deployment would expire on 03/01/2024, entering the recovery period, and users accessing it would see a 410 status code. If required, you could still restore it until 03/31/2024, when all associated resources are permanently removed and restoring the deployment is no longer possible.

Once a policy is enabled on a project, deployments within the retention period will start to be automatically marked for deletion, within a few days of enabling the policy.

To configure a retention policy, navigate to the Settings tab of your project and follow these steps:

You can view your deployments retention policy using Vercel CLI and running the following command from your terminal:

When a deployment is marked for deletion either accidentally or as part of the retention policy, you can restore it within the recovery period. This period is 30 days for successfully built deployments, but unsuccessful deployments may be garbage collected sooner.

To restore a deleted deployment, navigate to the Settings tab of your project:

---
