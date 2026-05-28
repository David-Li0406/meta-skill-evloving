# Vercel - Configuration

**Pages:** 14

---

## Managing the visibility of the Vercel Toolbar

**URL:** https://vercel.com/docs/vercel-toolbar/managing-toolbar

**Contents:**
- Managing the visibility of the Vercel Toolbar
- Viewing the toolbar
- Enable or disable the toolbar team-wide
- Enable or disable the toolbar project-wide
- Disable toolbar for session
- Disable toolbar for automation
- Enable or disable the toolbar for a specific branch
- Using the toolbar with a custom alias domain
- Using a Content Security Policy

Vercel Toolbar is available on all plans

When the toolbar is enabled, you'll be able to view it on any preview or enabled environment. By default, the toolbar will appear as a circle with a menu icon. Clicking activates it, at which point you will see any comments on the page and notifications for issues detected by tools running in the background. When the toolbar has not been activated it will show a small Vercel icon over the menu icon.

Once a tool is used, the toolbar will show a second icon next to the menu, so you can access your most recently used tool.

To disable the toolbar by default for all projects in your team:

To disable the toolbar project-wide:

To disable the toolbar in the current browser tab:

To show the toolbar again, open a new browser session.

Alternatively, you can also hide the toolbar in any of the following ways:

To show the toolbar when it is hidden you can use that same key command or click the browser extension.

Users with the browser extension can set the toolbar to start hidden by toggling on Start Hidden in Preferences from the Toolbar menu.

You can use the header to prevent interference with automated end-to-end tests:

You can use Vercel's preview environment variables to manage the toolbar for specific branches or environments

To enable the toolbar for an individual branch, add the following to the environment variables for the desired preview branch:

To disable the toolbar for an individual branch, set the above environment variable's value to :

To use the toolbar with preview deployments that have custom alias domains, you must opt into the toolbar explicitly in your project settings on the dashboard.

If you have a Content Security Policy (CSP) configured, you may need to adjust the CSP to enable access to the Vercel Toolbar or Comments.

You can make the following adjustments to the response header:

---

## Configuration Redirects

**URL:** https://vercel.com/docs/redirects/configuration-redirects

**Contents:**
- Configuration Redirects
- Limits

Configuration redirects define routing rules that Vercel evaluates at build time. Use them for permanent redirects (), temporary redirects (), and geolocation-based routing.

Define configuration redirects in your framework's config file or in the file, which is located in the root of your application. The should contain a field, which is an array of redirect rules. For more information on all available properties, see the project configuration docs.

View the full API reference for the property.

Using does not yet work locally while using , but does work when deployed.

When deployed, these redirect rules will be deployed to every region in Vercel's CDN.

The /.well-known path is reserved and cannot be redirected or rewritten. Only Enterprise teams can configure custom SSL. Contact sales to learn more.

If you are exceeding the limits below, we recommend using Middleware and Edge Config to dynamically read redirect values.

---

## Vercel Sandbox examples

**URL:** https://vercel.com/docs/vercel-sandbox/examples

**Contents:**
- Vercel Sandbox examples
- Using a private repository
  - GitHub access token options
    - Fine-grained personal access token
    - Other Github methods
- Install system packages
- Extend the timeout of a running sandbox

Vercel Sandbox is available in Beta on all plans

Learn how to use the Sandbox SDK through real-life examples.

In this example, you create an isolated environment from a private Git repository by authenticating with a GitHub personal access token or GitHub App token, and run a simple command inside the sandbox.

The method initializes the environment with the provided repository and configuration options, including authentication credentials, , and exposed . Once created, you can execute commands inside the sandboxed environment using .

There are several ways to authenticate with private GitHub repositories.

Fine-grained tokens provide repository-specific access and enhanced security:

You can install system packages using the system package manager:

You can find the list of available packages on the Amazon Linux documentation.

In the example, allows the command to run with elevated privileges.

You can extend the timeout of a running sandbox using the method, which takes a duration in milliseconds:

You can extend the timeout as many times as you'd like, until the max timeout for your plan has been reached.

---

## Accessibility Audit Tool

**URL:** https://vercel.com/docs/vercel-toolbar/accessibility-audit-tool

**Contents:**
- Accessibility Audit Tool
- Accessing the accessibility audit tool
- Enabling or disabling the accessibility audit tool
- Inspecting accessibility issues
- Recording accessibility issues
- More resources

Accessibility Audit Tool is available on all plans

The accessibility audit tool automatically checks the Web Content Accessibility Guidelines 2.0 level A and AA rules, grouping them by impact as defined by deque axe, and runs in the background on all environments the toolbar and added to.

To access the accessibility audit tool:

The accessibility audit tool is enabled by default. To disable it:

To inspect an accessibility issue select the filter option you want to inspect. A list of issues will are displayed as dropdowns. You can select each dropdown to view the issue details, including an explanation of the issue and a link to the relevant WCAG guideline. Hovering over the failing elements markup will highlight the element on the page, while clicking on the element will log it to the devtools console.

By default the accessibility audit tool will log issues on page load. To test ephemeral states, such as hover or focus, you can record issues by interacting with the page. To record issues select the Start Recording button in the Accessibility panel. This will start recording issues as you interact with the page. To stop recording, select the Stop Recording button. Recording persists for your session, so you can refresh the page, or navigate to a new page and it will continue to record issues while your tab is active.

---

## Security settings

**URL:** https://vercel.com/docs/project-configuration/security-settings

**Contents:**
- Security settings
- Build logs and source protection
- Customer Success Code Visibility
- Git fork protection
- Secure Backend Access with OIDC Federation
- Deployment Retention Policy

To adjust your project's security settings:

From here you can enable or disable Attack Challenge Mode, Logs and Source Protection, Customer Success Code Visibility and Git Fork Protection.

By default, the following paths mentioned below can only be accessed by you and authenticated members of your Vercel team:

Disabling Build Logs and Source Protection will make your source code and logs publicly accessible. Do not edit this setting if you don't want them to be publicly accessible.

None of your existing deployments will be affected when you toggle this setting. If you’d like to make the source code or logs private on your existing deployments, the only option is to delete these deployments.

This setting is overwritten when a deployment is created using Vercel CLI with the option or the property is used in .

For deployments created before July 9th, 2020 at 7:05 AM (UTC), only the Project Settings is considered for determining whether the deployment's Logs and Source are publicly accessible or not. It doesn't matter if the flag was passed when creating those Deployments.

Customer Success Code Visibility is available on Enterprise and Pro plans

Vercel provides a setting that controls the visibility of your source code to our Customer Success team. By default, this setting is disabled, ensuring that your code remains confidential and accessible only to you and your team. The Customer Success team might request for this setting to be enabled to troubleshoot specific issues related to your code.

If you receive a pull request from a fork of your repository, Vercel will require authorization from you or a Team Member to deploy the pull request.

This behavior protects you from leaking sensitive project information such as environment variables and the OIDC Token.

You can disable this protection in the Security section of your Project Settings.

Do not disable this setting until you review Environment Variables in your project as well as vercel.json in your source code.

This feature allows you to secure access to your backend services by using short-lived, non-persistent tokens that are signed by Vercel's OIDC Identity Provider (IdP).

To learn more, see Secure Backend Access with OIDC Federation.

Deployment Retention Policy allows you to set a limit on how long older deployments are kept for your project. To learn more, see Deployment Retention Policy.

This section also provides information on the recently deleted deployments

---

## Managing Cron Jobs

**URL:** https://vercel.com/docs/cron-jobs/manage-cron-jobs

**Contents:**
- Managing Cron Jobs
- Viewing cron jobs
- Cron jobs maintenance
- Securing cron jobs
- Cron job duration
- Cron job error handling
- Cron jobs with dynamic routes
- Handling nonexistent paths
- Cron jobs and deployments
- Controlling cron job concurrency

Cron Jobs are available on all plans

To view your active cron jobs:

Disabled cron jobs will still be listed and will count towards your cron jobs limits

It is possible to secure your cron job invocations by adding an environment variable called to your Vercel project. We recommend using a random string of at least 16 characters for the value of . A password generator, like 1Password, can be used to create one.

The value of the variable will be automatically sent as an header when Vercel invokes your cron job. Your endpoint can then compare both values, the authorization header and the environment variable, to verify the authenticity of the request.

You can use App Router Route Handlers to secure your cron jobs, even when using the Pages Router.

The header will have the prefix for the value.

The duration limits for Cron jobs are identical to those of Vercel Functions. See the documentation for more information.

In most cases, these limits are sufficient. However, if you need more processing time, it's recommended to split your cron jobs into different units or distribute your workload by combining cron jobs with regular HTTP requests with your API.

Vercel will not retry an invocation if a cron job fails. You can check for error logs through the View Log button in the Cron Jobs tab.

Cron jobs can be created for dynamic routes:

If you create a cron job for a path that doesn't exist, it generates a 404 error. However, Vercel still executes your cron job. You can analyze your logs to check if there are any issues.

Creating a new deployment will not interrupt your running cron jobs; they will continue until they finish.

If your cron job runs longer than the interval between invocations, Vercel can trigger a second instance while the first is still running. This can lead to race conditions, duplicate processing, or data corruption.

To prevent concurrent runs, use a lock mechanism like Redis distributed locks in your cron job. A lock ensures only one instance runs at a time by checking if another instance is already active before starting.

You can also prevent overlapping runs by:

Vercel's event-driven system can occasionally deliver the same cron event more than once. This means your job might run twice for a single scheduled execution.

Design your operations to be idempotent so they produce the same result even when executed multiple times. For example:

To make operations idempotent:

Use both locks (to prevent concurrent runs) and idempotency (to handle duplicate events safely) together for the most reliable cron jobs

Cron jobs are API routes. You can run them locally by making a request to their endpoint. For example, if your cron job is in , you could visit the following endpoint in your browser: . You should be aware that while your browser may follow redirects, cron job invocations in production will not follow redirects.

There is currently no support for , , or other framework-native local development servers.

Cron jobs do not follow redirects. When a cron-triggered endpoint returns a 3xx redirect status code, the job completes without further requests. Redirect responses are treated as final for each invocation.

The view logs button on the cron job overview can be used to verify the response of the invocations and gain further insights.

Cron jobs are logged as function invocations from the Logs tab of your projects dashboard. You can view the logs for a cron job from the list on the Cron jobs settings page of the project:

See how to view runtime logs for more information.

Note that when cron jobs respond with a redirect or a cached response, they will not be shown in the logs.

Hobby users can only create cron jobs with hourly accuracy. Vercel may invoke these cron jobs at any point within the specified hour to help distribute load across all accounts. For example, an expression like could trigger an invocation anytime between and .

For all other teams, cron jobs will be invoked within the minute specified. For instance, the expression would trigger an invocation between and .

If you Instant Rollback to a previous deployment, active cron jobs will not be updated. They will continue to run as scheduled until they are manually disabled or updated.

---

## Shared environment variables

**URL:** https://vercel.com/docs/environment-variables/shared-environment-variables

**Contents:**
- Shared environment variables
- Creating shared environment variables
- Linking to projects
  - Project level linking
  - Team level linking
- Removing shared environment variables
  - Unlinking at the project level
  - Unlinking at the team level
  - Deleting environment variables from a team
- Known limitations

Shared Environment Variables are environment variables that you define at the team-level and can link to multiple projects. When a Shared Environment Variable is updated, the change is applied to all linked projects.

When a project-level and a Shared Environment Variable share the same key and environment, the project-level environment variable always overrides the Shared Environment Variable.

Shared Environment Variables are created on the Team Settings page. To create a new Shared Environment Variable, follow these steps:

A Shared Environment Variable is activated once it is linked to at least one project.

You can link an existing Shared Environment Variable to a project either at the project-level or the team-level.

For project-level linking:

From your dashboard, click the Settings tab and go to Environment Variables.

Scroll down below the Shared Environment Variable creation form.

Find the variable you would like to link. You can use the Search box, the Environments drop-down filter and sort by last updated date, name or type to more easily find the variable.

Open the context menu for the specific Shared Environment Variable using the vertical ellipsis icon on the right hand side of the row, and click Edit:

From the Environment Variable form, you can link additional projects using the Link to Projects field

Click Save when you are done

There are two ways to remove a Shared Environment Variable from a project:

This action will remove the Shared Environment Variable from the Vercel Team. It will also unlink the Environment Variable from ALL previously linked projects.

Branch-specific variables are not currently supported with Shared Environment Variables

---

## Speed Insights Configuration with @vercel/speed-insights

**URL:** https://vercel.com/docs/speed-insights/package

**Contents:**
- Speed Insights Configuration with @vercel/speed-insights
- Getting started
- More resources

Speed Insights is available on all plans

With the npm package, you're able to configure your application to capture and send web performance metrics to Vercel.

To get started with Speed Insights, refer to our Quickstart guide which will walk you through the process of setting up Speed Insights for your project.

In prior versions of Speed Insights this was managed in the UI. This option is now managed through code with the package.

This parameter determines the percentage of events that are sent to the server. By default, all events are sent. Lowering this parameter allows for cost savings but may result in a decrease in the overall accuracy of the data being sent. For example, a of would mean that only 50% of the events will be sent to the server.

To learn more about how to configure the option, see the Sending a sample of events to Speed Insights recipe.

With the function, you can modify or filter out the event data before it's sent to Vercel. You can use this to redact sensitive data or to avoid sending certain events.

For instance, if you wish to ignore events from a specific URL or modify them, you can do so with this option.

With the debug mode, you can view all Speed Insights events in the browser's console. This option is especially useful during development.

This option is automatically enabled if the environment variable is available and either or .

You can manually disable it to prevent debug messages in your browsers console.

The option allows you to specify the current dynamic route (such as ). This is particularly beneficial when you need to aggregate performance metrics for similar routes.

This option is automatically set when using a framework specific import such as for Next.js, Nuxt, SvelteKit and Remix.

The option allows you to report the collected metrics to a different url than the default: .

This is useful when deploying several projects under the same domain, as it allows you to keep each application isolated.

For example, when is managed outside of Vercel:

Both applications are sending their metrics to . To restore the isolation, "bob-app" should use:

The option allows you to load the Speed Insights script from a different URL than the default one.

---

## Project settings

**URL:** https://vercel.com/docs/project-configuration/project-settings

**Contents:**
- Project settings
- Configuring your project with a vercel.json file
- General settings
- Build and deployment settings
- Custom domains
- Environment Variables
- Git
- Integrations
- Deployment Protection
- Functions

From the Vercel dashboard, there are two areas where you can configure settings:

This guide focuses on the project settings. To edit project settings:

While many settings can be set from the dashboard, you can also define a file at the project root that allows you to set and override the default behavior of your project.

To learn more, see Configuring projects with vercel.json.

This provides all the foundational information and settings for your Vercel project, including the name, build and deployment settings, the directory where your code is located, the Node.js version, Project ID, toolbar settings, and more.

To learn more, see General Settings

In your build and deployment settings, adjust configurations such as framework settings, code directory, and Node.js version.

In this section, you can adjust build-related configurations, such as framework settings, code directory, Node.js version, and more.

You can add custom domains for each project.

To learn more, see the Domains documentation

You can configure Environment Variables for each environment directly from your project's settings. This includes linking Shared Environment Variables and creating Sensitive Environment Variables

To learn more, see the Environment Variables documentation.

In your project settings, you can manage the Git connection, enable Git LFS, and manage your build step settings.

To learn more about the settings, see Git Settings. To learn more about working with your Git integration, see Git Integrations.

To manage third-party integrations for your project, you can use the Integrations settings.

To learn more, see Integrations.

Protect your project deployments with Vercel Authentication and Password Protection, and more.

To learn more, see Deployment Protection.

You can configure the default settings for your Vercel Functions, including the Node.js version, memory, timeout, region, and more.

To learn more, see Configuring Functions.

You can enable and disable Cron Jobs for your project from the Project Settings. Configuring cron jobs is done in your codebase.

To learn more, see Cron Jobs.

Team owners can manage who has access to the project by adding or removing members to that specific project from the project settings.

To learn more, see project-level roles.

Webhooks allow your external services to respond to events in your project. You can enable them on a per-project level from the project settings.

To learn more, see the Webhooks documentation.

Drains are a Pro and Enterprise feature that allow you to send observability data (logs, traces, speed insights, and analytics) to external services. Drains are created at the team-level, but you can manage them on a per-project level from the project settings.

To learn more, see the Drains documentation.

From your project's security settings you can enable or disable Attack Challenge Mode, Logs and Source Protection, Customer Success Code Visibility Git Fork Protection, and set a retention policy for your deployments.

To learn more, see Security Settings.

Vercel provides some additional features in order to configure your project in a more advanced way. This includes:

---

## Builds

**URL:** https://vercel.com/docs/builds

**Contents:**
- Builds
- Build infrastructure
- How builds are triggered
- Build customization
- Skipping the build step
- Monorepos
- Concurrency and queues
- Environment variables
- Ignored files and folders
- Build output and deployment

Vercel automatically performs a build every time you deploy your code, whether you're pushing to a Git repository, importing a project via the dashboard, or using the Vercel CLI. This process compiles, bundles, and optimizes your application so it's ready to serve to your users.

When you initiate a build, Vercel creates a secure, isolated virtual environment for your project:

This infrastructure handles millions of builds daily, supporting everything from individual developers to large enterprises, while maintaining strict security and performance standards.

Most frontend frameworks—like Next.js, SvelteKit, and Nuxt—are auto-detected, with defaults applied for Build Command, Output Directory, and other settings. To see if your framework is included, visit the Supported Frameworks page.

Builds can be initiated in the following ways:

Push to Git: When you connect a GitHub, GitLab, or Bitbucket repository, each commit to a tracked branch initiates a new build and deployment. By default, Vercel performs a shallow clone of your repo () to speed up build times.

Vercel CLI: Running locally deploys your project. By default, this creates a preview build unless you add the flag (for production).

Dashboard deploy: Clicking Deploy in the dashboard or creating a new project also triggers a build.

Depending on your framework, Vercel automatically sets the Build Command, Install Command, and Output Directory. If needed, you can customize these in your project's Settings:

Build Command: Override the default (, , etc.) for custom workflows.

Output Directory: Specify the folder containing your final build output (e.g., or ).

Install Command: Control how dependencies are installed (e.g., , ) or skip installing dev dependencies if needed.

To learn more, see Configuring a Build.

For static websites—HTML, CSS, and client-side JavaScript only—no build step is required. In those cases:

When working in a monorepo, you can connect multiple Vercel projects within the same repository. By default, each project will build and deploy whenever you push a commit. Vercel can optimize this by:

Skipping unaffected projects: Vercel automatically detects whether a project's files (or its dependencies) have changed and skips deploying projects that are unaffected. This feature reduces unnecessary builds and doesn't occupy concurrent build slots. Learn more about skipping unaffected projects.

Ignored build step: You can also write a script that cancels the build for a project if no relevant changes are detected. This approach still counts toward your concurrent build limits, but may be useful in certain scenarios. See the Ignored Build Step documentation for details.

For monorepo-specific build tools, see:

When multiple builds are requested, Vercel manages concurrency and queues for you:

Concurrency Slots: Each plan has a limit on how many builds can run at once. If all slots are busy, new builds wait until a slot is free.

Branch-Based Queue: If new commits land on the same branch, Vercel skips older queued builds and prioritizes only the most recent commit. This ensures that the latest changes are always deployed first.

On-Demand Concurrency: If you need more concurrent build slots or want certain production builds to jump the queue, consider enabling On-Demand Concurrent Builds.

Vercel can automatically inject environment variables such as API keys, database connections, or feature flags during the build:

Project-Level Variables: Define variables under Settings for each environment (Preview, Production, or any custom environment).

Pull Locally: Use to download environment variables for local development. This command populates your file.

Security: Environment variables remain private within the build environment and are never exposed in logs.

Some files (e.g., large datasets or personal configuration) might not be needed in your deployment:

Once the build completes successfully:

If the build fails or times out, Vercel provides diagnostic logs in the dashboard to help you troubleshoot. For common solutions, see our build troubleshooting docs.

Behind the scenes, Vercel manages a sophisticated global infrastructure that:

Vercel enforces certain limits to ensure reliable builds for all users:

Build timeout: The maximum build time is 45 minutes. If your build exceeds this limit, it will be terminated, and the deployment fails.

Build cache: Each build cache can be up to 1 GB. The cache is retained for one month. Restoring a build cache can speed up subsequent deployments.

Container resources: Vercel creates a build container with different resources depending on your plan:

For more information, visit Build Container Resources and Cancelled Builds.

To explore more features and best practices for building and deploying with Vercel:

---

## Reference

**URL:** https://vercel.com/docs/feature-flags/flags-explorer/reference

**Contents:**
- Reference
- Definitions
  - Returning definitions through the Flags API Endpoint
  - Embedding definitions through script tags
- Values
  - Emitting values using the FlagValues React component
  - Embedding values through script tags
- environment variable
- API endpoint
  - Verifying a request to the API endpoint

Flags Explorer is available on all plans

The Flags Explorer has five main concepts: the API Endpoint, the FLAGS_SECRET environment variable, the override cookie, flag definitions, and flag values.

The Flags Explorer needs to know about your feature flags before it can display them.

Flag definitions are metadata for your feature flags, which communicate:

A definition can never communicate the value of a flag as they load independently from flag values. See flag definitions for more information.

This is how Vercel Toolbar shows flag definitions:

There are two ways to provide your feature flags to the Flags Explorer:

The Flags API Endpoint is the recommended way to provide your feature flags to the Flags Explorer. The Flags Explorer will request your application's Flags API Endpoint to fetch the feature flag definitions and other settings.

See Definitions properties for a full list of properties you can return from your Flags API Endpoint.

We strongly recommend communicating your feature flag definitions through the Flags API Endpoint. In rare cases, it can be useful to communicate feature flag definitions through the HTML response. Vercel Toolbar will pick up any script tags included in the DOM which have a attribute.

If you are using React or Next.js, use the component. If you are using another framework or no framework at all you can render these script tags manually. The expected shape is:

This example shows how to communicate a feature flag definition through the DOM:

You can also encrypt the definitions before emitting them to prevent leaking your feature flags through the DOM.

Using within script tags leads to XSS vulnerabilities. Use exported by to stringify safely.

Your Flags API Endpoint returns your application's feature flag definitions containing information like their key, description, origin, and available options. However the Flags API Endpoint can not return the value a flag evaluated to, since this value might depend on the request which rendered the page initially.

You can optionally provide the values of your feature flags to Flags Explorer in two ways:

Emitted values will show up in the Flags Explorer, and will be used by Web Analytics to annotate events.

This is how Vercel Toolbar shows flag values:

Any JSON-serializable values are supported. Flags Explorer combines these values with any definitions, if they are present.

The package exposes React components which allow making the Flags Explorer aware of your feature flag's values.

The approaches above will add the names and values of your feature flags to the DOM in plain text. Use the function to keep your feature flags confidential.

The component will emit a script tag with a attribute, which get picked up by the Flags Explorer. Flags Explorer then combines the flag values with the definitions returned by your API endpoint. If you are not using React or Next.js you can render these script tags manually as shown in the next section.

Flags Explorer scans the DOM for script tags with the attribute. Any changes to content get detected by a mutation observer.

You can emit the values of feature flags to the Flags Explorer by rendering script tags with the attribute.

Be careful when creating these script tags. Using within script tags leads to XSS vulnerabilities. Use exported by to stringify safely.

The expected shape is:

To prevent disclosing feature flag names and values to the client, the information can be encrypted. This keeps the feature flags confidential. Use the Flags SDK's function together with the environment variable to encrypt your flag values on the server before rendering them on the client. The Flags Explorer will then read these encrypted values and use the from your project to decrypt them.

This secret gates access to the Flags API endpoint, and optionally enables signing and encrypting feature flag overrides set by Vercel Toolbar. As described below, you can ensure that the request is authenticated in your Flags API endpoint, by using .

You can create this secret by following the instructions in the Flags Explorer Quickstart. Alternatively, you can create the manually by following the instructions below. If using microfrontends, you should use the same as the other projects in the microfrontends group.

Manually creating the

The value must have a specific length (32 random bytes encoded in base64) to work as an encryption key. You can create one using node:

In your local environment, pull your environment variables with to make them available to your project.

The environment variable must be defined in your project settings on the Vercel dashboard. Defining the environment variable locally is not enough as Flags Explorer reads the environment variable from your project settings.

When you have set the environment variable in your project, Flags Explorer will request your application's Flags API endpoint. This endpoint should return a configuration for the Flags Explorer that includes the flag definitions.

Your endpoint should call to ensure the request to load flags originates from Vercel Toolbar. This prevents your feature flag definitions from being exposed publicly thorugh the API endpoint. The header sent by Vercel Toolbar contains proof that whoever made this request has access to . The secret itself is not sent over the network.

If the check fails, you should return status code and no response body. When the check is successful, return the feature flag definitions and other configuration as JSON:

If you are not using the Flags SDK to define feature flags in code, or if you are not using Next.js or SvelteKit, you need to manually return the feature flag definitions from your API endpoint.

The JSON response must have the following shape

These are your application's feature flags. You can return the following data for each definition:

You can optionally tell Vercel Toolbar about the actual value flags resolved to. The Flags API Endpoint cannot return this as the value might differ for each request. See Flag values instead.

In some cases you might need to fetch your feature flag definitions from your feature flag provider before you can return them from the Flags API Endpoint.

In case this request fails you can use . Any hints returned will show up in the UI.

This is useful when you are fetching your feature flags from multiple sources. In case one request fails you might still want to show the remaining flags on a best effort basis, while also displaying a hint that fetching a specific source failed. You can return and simultaneously to do so.

When you create an override, Vercel Toolbar will set a cookie called . You can read this cookie in your applications to make your application respect the overrides set by Vercel Toolbar.

The setting controls the value of the cookie:

We highly recommend using mode as it protects against manipulation.

The Flags Explorer will set a cookie called containing the overrides.

If you use the Flags SDK for Next.js or SvelteKit, the SDK will automatically handle the overrides set by the Flags Explorer.

Read this cookie and use the function to decrypt the overrides and use them in your application. The decrypted value is a JSON object containing the name and override value of each overridden flag.

Vercel Toolbar uses a MutationObserver to find all script tags with and attributes. Any changes to content get detected by the toolbar.

For more information, see the following sections:

---

## Git settings

**URL:** https://vercel.com/docs/project-configuration/git-settings

**Contents:**
- Git settings
- Disconnect your Git repository
- Git Large File Storage (LFS)
- Deploy Hooks
- Ignored Build Step
  - Ignore Build Step on redeploy
- Verified Commits

Once you have connected a Git repository, select the Git menu item from your project settings page to edit your project’s Git settings. These settings include:

To disconnect your Git repository from your Vercel project:

If you have LFS objects in your repository, you can enable or disable support for them from the project settings. When support is enabled, Vercel will pull the LFS objects that are used in your repository.

You must redeploy your project after turning Git LFS on.

Vercel supports deploy hooks, which are unique URLs that accept HTTP POST requests and trigger deployments. Check out our Deploy Hooks documentation to learn more.

By default, Vercel creates a new deployment and build (unless the Build Step is skipped) for every commit pushed to your connected Git repository.

Each commit in Git is assigned a unique hash value commonly referred to as SHA. If the SHA of the commit was already deployed in the past, no new Deployment is created. In that case, the last Deployment matching that SHA is returned instead.

To ignore the build step:

Canceled builds are counted as full deployments as they execute a build command in the build step. This means that any canceled builds initiated using the ignore build step will still count towards your deployment quotas and concurrent build slots.

You may be able to optimize your deployment queue by skipping builds for projects within a monorepo that are unaffected by a change.

To learn about more advanced usage see the "How do I use the Ignored Build Step field on Vercel?" guide.

If you have set an ignore build step command or script, you can also skip the build step when redeploying your app:

Vercel allows you to require verified commits for deployments. This is only available for GitHub projects. Learn more about verified commits on GitHub.

To enable verified commits:

When enabled, Vercel will only create deployments for commits that have been verified by GitHub. For all other commits, the deployment will be automatically canceled.

---

## Rotating environment variables

**URL:** https://vercel.com/docs/environment-variables/rotating-secrets

**Contents:**
- Rotating environment variables
- Rotating secrets safely
  - For project-level environment variables
  - For team-level environment variables
- Rotating credentials for integrations
- Troubleshooting
  - Deployment fails after rotating a secret
  - Old deployments still use the old credential
  - Multiple projects broke after rotation

Find guides for rotating secrets for our Marketplace providers in Vercel's Knowledge Base.

When you need to rotate API keys, tokens, or other credentials stored in your environment variables, you'll need to update both your third-party service and your Vercel projects. This ensures your applications continue to work without downtime.

Secret rotation is a security best practice that limits the exposure window if a credential is compromised. You might rotate secrets when:

The key to safe rotation is updating Vercel before you invalidate the old credential. This prevents your deployments from breaking when the old key stops working.

If your secret is configured at the project level, only that project uses it. You'll only need to redeploy that one project.

If you're using the Preview environment, redeploy your preview deployments as well to avoid errors when you invalidate the old credential.

If your secret is configured at the team level, multiple projects might use it. You'll need to redeploy all projects that depend on this credential.

If you invalidate the old credential before all projects are redeployed, any project still using the old value will fail until you redeploy it.

Find guides for rotating secrets for our Marketplace providers in Vercel's Knowledge Base.

When rotating credentials for integrations (like database providers or third-party services installed from the Vercel Marketplace):

If the integration allows for provisioning resources, you will have to repeat this process for each resource that you've provisioned. These resources are listed on the integration page.

If your deployment fails after updating a credential:

Environment variable changes only apply to new deployments. If you visit an old deployment URL, it will still use the old credential. This is expected behavior.

Once you invalidate the old credential, old deployments that relied on it will fail if they make API calls using that credential. Redeploy the old deployment to fix this, as each new deployment picks up the latest version of the environment variables.

If you rotated a team-level environment variable and multiple projects broke, you may have missed redeploying some projects:

---

## Advanced Web Analytics Config with @vercel/analytics

**URL:** https://vercel.com/docs/analytics/package

**Contents:**
- Advanced Web Analytics Config with @vercel/analytics
- Getting started

To get started with analytics, follow our Quickstart guide which will walk you through the process of setting up analytics for your project.

Override the automatic environment detection.

You can manually disable it to prevent debug messages in your browsers console.

With the option, you can modify the event data before it's sent to Vercel. Below, you will see an example that ignores all events that have a inside the URL.

Returning will ignore the event and no data will be sent. You can also modify the URL and check our docs about redacting sensitive data.

The option allows you to report the collected analytics to a different url than the default: .

This is useful when deploying several projects under the same domain, as it allows you to keep each application isolated.

For example, when is managed outside of Vercel:

Both applications are sending their analytics to . To restore the isolation, "bob-app" should use:

The option allows you to load the Web Analytics script from a different URL than the default one.

---
