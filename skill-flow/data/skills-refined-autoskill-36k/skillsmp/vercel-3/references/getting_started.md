# Vercel - Getting Started

**Pages:** 33

---

## Vercel CDN overview

**URL:** https://vercel.com/docs/cdn

**Contents:**
- Vercel CDN overview
- Global network architecture
- Features
- Pricing
- Usage
- Supported protocols
- Using Vercel's CDN locally
- Using Vercel's CDN with other CDNs

Vercel's CDN is a globally distributed platform that stores content near your customers and runs compute in regions close to your data, reducing latency and improving end-user performance.

If you're deploying an app on Vercel, you already use our CDN. These docs will teach you how to optimize your apps and deployment configuration to get the best performance for your use case.

Vercel's CDN is built on a robust global infrastructure designed for optimal performance and reliability:

This architecture balances the widespread geographical distribution benefits with the efficiency of concentrated caching and computing resources. By maintaining fewer, dense regions, we increase cache hit probabilities while ensuring low-latency access through our extensive PoP network.

Vercel's CDN pricing is divided into three resources:

All resources are billed based on usage with each plan having an included allotment. Those on the Pro plan are billed according to additional allotments.

The pricing for each resource is based on the region from which requests to your site come. Use the dropdown to select your preferred region and see the pricing for each resource.

The table below shows the metrics for the Networking section of the Usage dashboard.

To view information on managing each resource, select the resource link in the Metric column. To jump straight to guidance on optimization, select the corresponding resource link in the Optimize column.

See the manage and optimize networking usage section for more information on how to optimize your usage.

The CDN supports the following protocols (negotiated with ALPN):

Vercel supports 35 frontend frameworks. These frameworks provide a local development environment used to test your app before deploying to Vercel.

Through framework-defined infrastructure, Vercel then transforms your framework build outputs into globally managed infrastructure for production.

If you are using Vercel Functions or other compute on Vercel without a framework, you can use the Vercel CLI to test your code locally with .

While sometimes necessary, proceed with caution when you place another CDN in front of Vercel:

---

## Import an existing project

**URL:** https://vercel.com/docs/getting-started-with-vercel/import

**Contents:**
- Import an existing project
  - Using CLI?
  - Connect to your Git provider
  - Import your repository
  - Optionally, configure any settings
  - Deploy your project
  - Enjoy the confetti!
- Next Steps

Use the following snippet to deploy your existing project with Vercel CLI:

Use the following snippet to deploy your existing project with Vercel CLI:

Your existing project can be any web project that outputs static HTML content (such as a website that contains HTML, CSS, and JavaScript). When you use any of Vercel's supported frameworks, we'll automatically detect and set the optimal build and deployment configurations for your framework.

On the New Project page, under the Import Git Repository section, select the Git provider that you would like to import your project from.

Follow the prompts to sign in to either your GitHub, GitLab, or BitBucket account.

Find the repository in the list that you would like to import and select Import.

Vercel will automatically detect the framework and any necessary build settings. However, you can also configure the Project settings at this point including the build and output settings and Environment Variables. These can also be set later.

Press the Deploy button. Vercel will create the Project and deploy it based on the chosen configurations.

To view your deployment, select the Project in the dashboard and then select the Domain. This page is now visible to anyone who has the URL.

Next, learn how to assign a domain to your new deployment.

---

## Getting Started

**URL:** https://vercel.com/docs/ai-gateway/getting-started

**Contents:**
- Getting Started
  - Set up your application
  - Install dependencies
  - Set up your API key
  - Create and run your script
  - Next steps
- Using OpenAI SDK
- Using other community frameworks

This quickstart will walk you through making an AI model request with Vercel's AI Gateway. While this guide uses the AI SDK, you can also integrate with the OpenAI SDK or other community frameworks.

Start by creating a new directory using the command. Change into your new directory and then run the command, which will create a .

Install the AI SDK package, , along with other necessary dependencies.

is used to access environment variables (your AI Gateway API key) within your application. The package is a TypeScript runner that allows you to run your TypeScript code. The package is the TypeScript compiler. The package is the TypeScript definitions for the Node.js API.

To create an API key, go to the AI Gateway tab of the dashboard:

Once you have the API key, create a file and save your API key:

Instead of using an API key, you can use OIDC tokens to authenticate your requests.

The AI Gateway provider will default to using the environment variable.

Create an file in the root of your project and add the following code:

Now, run your script:

You should see the AI model's response to your prompt.

Continue with the AI SDK documentation to learn advanced configuration, set up provider and model routing with fallbacks, and explore more integration examples.

The AI Gateway provides OpenAI-compatible API endpoints that allow you to use existing OpenAI client libraries and tools with the AI Gateway.

The OpenAI-compatible API includes:

Learn more about using the OpenAI SDK with the AI Gateway in the OpenAI-Compatible API page.

The AI Gateway is designed to work with any framework that supports the OpenAI API or AI SDK 5.

Read more about using the AI Gateway with other community frameworks in the framework integrations section.

---

## Collaborate on Vercel

**URL:** https://vercel.com/docs/getting-started-with-vercel/collaborate

**Contents:**
- Collaborate on Vercel
- Make Changes
- Create a preview deployment
  - Make your changes
  - Commit your changes
  - Inspect your deployment information
  - View your deployment URL
- Commenting on previews
  - Open your deployment
  - Authenticate with your Vercel account

Collaboration is key in successful development projects, and Vercel offers robust features to enhance collaboration among developers. From seamless code collaboration to real-time previews with Comments, Vercel empowers your team to work together effortlessly.

Now that your project is publicly available on your domain of choice, it’s time to begin making changes to it. With Vercel's automatic deployments, this won't require any extra effort. By default, when your Vercel project is connected to a Git repository, Vercel will deploy every commit that is pushed to the Git repository, regardless of which branch you're pushing it to.

A Production environment is one built from the or development branch of your Git repository. A preview environment is created when you deploy from any other branch.

Vercel provides a URL that reflects the latest pushes to that branch. You can find this either on your dashboard, or in a pull request, which you'll see in the next step

This connection was established for you automatically, so all you have to do is push commits, and you will start receiving links to deployments right on your Git provider.

Create a new branch in your project and make some changes

Commit those changes and create a pull request. After a few seconds, Vercel picks up the changes and starts to build and deploy your project. You can see the status of the build through the bot comment made on your PR:

Select Inspect to explore the build within your dashboard. You can see the build is within the preview environment and additional information about the deployment including: build information, a deployment summary, checks, and domain assignment. These happen for every deployment

Return to your pull request. At this point your build should be deployed and you can select Visit Preview. You can now see your changes and share this preview URL with others.

Comments provide a way for your team or friends to give direct feedback on preview deployments. Share with others by doing the following:

Open the preview deployment that you’d like to share by selecting the Domain from the deployment information as shown in step 3 above. Alternatively, you can find it by selecting your project from the dashboard, and selecting the most recent commit under Active Branches:

From the Comments toolbar at the bottom of the screen, select Log in to comment and sign in with your Vercel account.

Select Share in the Toolbar menu. Add the emails of people you would like to share the preview with. If you are previewing a specific commit, you may have the option to share the preview for your branch instead. This option allows you to share a preview that updates with the latest commit to the branch.

To learn more, including other ways to share, see Sharing Deployments.

The person you are sharing the preview with needs to have a Vercel account. To do so, they'll need to select Log in to comment and then enter their email address.

Once the person you are sharing the preview with goes through the security options, they'll be ready to comment. You'll be notified of new comments through email, or when you visit the deployment.

For more information on using Comments, see Using comments.

---

## Projects overview

**URL:** https://vercel.com/docs/projects

**Contents:**
- Projects overview
- Project limits

Projects on Vercel represent applications that you have deployed to the platform from a single Git repository. Each project can have multiple deployments: a single production deployment and many pre-production deployments. A project groups deployments and custom domains.

While each project is only connected to a single, imported Git repository, you can have multiple projects connected to a single Git repository that includes many directories, which is particularly useful for monorepo setups.

You can view all projects in your team's Vercel dashboard and selecting a project will bring you to the project dashboard, where you can:

To learn more about limits on the number of projects you can have, see Limits.

---

## Getting started with Sign in with Vercel

**URL:** https://vercel.com/docs/sign-in-with-vercel/getting-started

**Contents:**
- Getting started with Sign in with Vercel
  - Prerequisites
  - Add environment variables
  - Create your folder structure for the API routes
  - Create an API route
  - Create a API route
  - Create a profile page
  - Create an error page
  - Create a API route
  - Add Sign in and Sign out buttons

This guide uses Next.js App Router. You'll create a Sign in with Vercel button that redirects to the authorization endpoint, add a callback route to exchange the authorization code for tokens, and set authentication cookies.

View a live version of this tutorial to see the sign in flow in action.

Add the following variables to your at your project's root:

When you are ready to go to production, add your environment variables to your project from the dashboard. If you have Vercel CLI installed, you can run to pull the values from your project settings into your local file.

Create a folder structure for the API routes in your project. Each API route will be in a folder with the name of the route.

Use the route to redirect the user to the authorization endpoint.

Use the route to exchange the authorization code for tokens.

Create a profile page to display the user's information.

Create an error page to display when an error occurs.

Use the route to revoke the token and sign the user out.

Add two components to start the OAuth flow (and sign in) and to sign out:

Run your application locally using the following command:

Open http://localhost:3000 and Sign in with Vercel. You will be redirected to the consent page where you can review the permissions and click Allow. Once you have signed in, you will be redirected to the profile page.

The API route can be used to validate the access token. This is optional, but it can be useful to validate the access token.

The component can be used to validate the access token. This is optional, but it can be useful to validate the access token.

Add this component to your profile page.

---

## Vercel Storage overview

**URL:** https://vercel.com/docs/storage

**Contents:**
- Vercel Storage overview
- Choosing a storage product
- Vercel Blob
  - Explore Vercel Blob
- Edge Config
  - Explore Edge Config
- Best practices
  - Locate your data close to your functions
  - Optimize for high cache hit rates
- Transferring your store

Vercel offers a suite of managed, serverless storage products that integrate with your frontend framework.

You can also find storage solutions in the Vercel Marketplace.

The right storage solution depends on your needs for latency, durability, and consistency. This table summarizes the key differences:

See best practices for optimizing your storage usage.

Vercel Blob is available on all plans

Those with the owner, member, developer role can access this feature

Vercel Blob offers optimized storage for images, videos, and other files.

You should use Vercel Blob if you need to:

Edge Config is available on all plans

An Edge Config is a global data store that enables you to read data at the edge without querying an external database or hitting upstream servers. Most lookups return in less than 1ms, and 99% of reads will return under 10ms.

You should use Edge Config if you need to:

Follow these best practices to get the most from your storage:

Deploy your databases in regions closest to your Functions. This minimizes network roundtrips and keeps response times low.

Vercel's CDN caches content in every region globally. Cache data fetched from your data store at the edge using cache headers to get the fastest response times.

Incremental Static Regeneration sets up caching headers automatically and stores generated assets globally. This gives you high availability and prevents cache-control misconfiguration.

You can also configure cache-control headers manually with Vercel Functions to cache responses in every CDN region. Note that Middleware runs before the CDN cache layer and cannot use cache-control headers.

You can bring your Blob or Edge Config stores along with your account as you upgrade from Hobby to Pro, or downgrade from Pro to Hobby. To do so:

When successful, you'll be taken to the Storage tab of the account or team you transferred the store to.

---

## Buy a domain

**URL:** https://vercel.com/docs/getting-started-with-vercel/buy-domain

**Contents:**
- Buy a domain
  - Using CLI?
  - Find a domain
  - Select your domain(s)
  - Purchase your domain(s)
  - Enter payment details and registrant information
  - Configure your domain
- Next steps

Use this snippet to purchase a new domain from Vercel:

Use Vercel to find and buy a domain that resonates with your brand, establishes credibility, and captures your visitors' attention.

All domains purchased on Vercel have WHOIS privacy enabled by default.

Go to https://vercel.com/domains and search for a domain that matches you or your brand. You could try "SuperDev"!

Depending on the TLD (top-level domain), you’ll see the purchase price. Domains with Premium badges are more expensive. You can sort the results by relevance (default), length, price, or alphabetical order.

For the ICANN registrant information:

If you enter the same email address you use for your Vercel user account (or an email your team owner uses), the information will be confirmed automatically.

If you enter another email address, please follow the instructions you receive in an email to confirm your registrant information.

If you don't confirm your registrant information, your domain could be suspended (clientHold). You can resend the verification email or update the registrant address from your Domains dashboard if needed.

You can also configure your domain from the project's domains dashboard page by following the Add and configure domain instructions.

Next, learn how to take advantage of Vercel's collaboration features as part of your developer workflow:

Use Vercel in your developer workflow

---

## Build image overview

**URL:** https://vercel.com/docs/builds/build-image

**Contents:**
- Build image overview
- Pre-installed packages
- Running the build image locally
- Installing additional packages

When you initiate a deployment, Vercel will build your project within a container using the build image. Vercel supports multiple runtimes.

The build image uses Amazon Linux 2023 as its base image.

The following packages are pre-installed in the build image with , the default package manager for Amazon Linux 2023.

You can install these packages using the dnf package manager with the following command:

Vercel does not provide the build image itself, but you can use the Amazon Linux 2023 base image to test things locally:

When you are done, run to return.

You can install additional packages into the build container by configuring the Install Command within the dashboard or the "installCommand" in your to use any of the following commands.

The build image includes access to repositories with stable versions of popular packages. You can list all packages with the following command:

You can search for a package by name with the following command:

You can install a package by name with the following command:

**Examples:**

Example 1 (bash):
```bash
dnf alsa-lib at-spi2-atk atk autoconf automake brotli bsdtar bzip2 bzip2-devel cups-libs expat-devel gcc gcc-c++ git glib2-devel glibc-devel gtk3 gzip ImageMagick-devel iproute java-11-amazon-corretto-headless libXScrnSaver libXcomposite libXcursor libXi libXrandr libXtst libffi-devel libglvnd-glx libicu libjpeg libjpeg-devel libpng libpng-devel libstdc++ libtool libwebp-tools libzstd-devel make nasm ncurses-libs ncurses-compat-libs openssl openssl-devel openssl-libs pango procps perl readline-devel ruby-devel strace sysstat tar unzip which zlib-devel zstd --yes
```

Example 2 (bash):
```bash
dnf alsa-lib at-spi2-atk atk autoconf automake brotli bsdtar bzip2 bzip2-devel cups-libs expat-devel gcc gcc-c++ git glib2-devel glibc-devel gtk3 gzip ImageMagick-devel iproute java-11-amazon-corretto-headless libXScrnSaver libXcomposite libXcursor libXi libXrandr libXtst libffi-devel libglvnd-glx libicu libjpeg libjpeg-devel libpng libpng-devel libstdc++ libtool libwebp-tools libzstd-devel make nasm ncurses-libs ncurses-compat-libs openssl openssl-devel openssl-libs pango procps perl readline-devel ruby-devel strace sysstat tar unzip which zlib-devel zstd --yes
```

---

## Vercel security overview

**URL:** https://vercel.com/docs/security

**Contents:**
- Vercel security overview
- Governance and policies
  - Compliance measures
  - Shared responsibility model
  - Encryption
- Multi-layered protection
  - Vercel firewall

Cloud-deployed web applications face constant security threats, with attackers launching millions of malicious attacks weekly. Your application, users, and business require robust security measures to stay protected.

A comprehensive security strategy requires both active protection, robust policies, and compliance frameworks:

Learn about the protection and compliance measures Vercel takes to ensure the security of your data, including DDoS mitigation, SOC2 Type 2 compliance, Data encryption, and more.

A shared responsibility model is a framework designed to split tasks and obligations between two groups in cloud computing. The model divides duties to ensure security, maintenance, and service functionality.

Out of the box, every Deployment on Vercel is served over an HTTPS connection. The SSL certificates for these unique URLs are automatically generated free of charge.

Understand how Vercel protects every incoming request with multiple layers of firewall and deployment protection.

The Vercel firewall helps to protect your applications and websites from malicious attacks and unauthorized access through:

---

## Getting started with Vercel

**URL:** https://vercel.com/docs/getting-started-with-vercel

**Contents:**
- Getting started with Vercel
- Before you begin
- Customizing your journey

Vercel is a platform for developers that provides the tools, workflows, and infrastructure you need to build and deploy your web apps faster, without the need for additional configuration.

Vercel supports popular frontend frameworks out-of-the-box, and its scalable, secure infrastructure is globally distributed to serve content from data centers near your users for optimal speeds.

During development, Vercel provides tools for real-time collaboration on your projects such as automatic preview and production environments, and comments on preview deployments.

To get started, create an account with Vercel. You can select the plan that's right for you.

Once you create an account, you can choose to authenticate either with a Git provider or by using an email. When using email authentication, you may need to confirm both your email address and a phone number.

This tutorial is framework agnostic but Vercel supports many frontend frameworks. As you go through the docs, the quickstarts will provide specific instructions for your framework. If you don't find what you need, give us feedback and we'll update them!

While many of our instructions use the dashboard, you can also use Vercel CLI to carry out most tasks on Vercel. In this tutorial, look for the "Using CLI?" section for the CLI steps. To use the CLI, you'll need to install it:

---

## Getting started with Image Optimization

**URL:** https://vercel.com/docs/image-optimization/quickstart

**Contents:**
- Getting started with Image Optimization
- Prerequisites
  - Import images
  - Add the required props
  - Deploy your app to Vercel
- Next steps

This guide will help you get started with using Vercel Image Optimization in your project, showing you how to import images, add the required props, and deploy your app to Vercel. Vercel Image Optimization works out of the box with Next.js, Nuxt, SvelteKit, and Astro.

Now that you've set up Vercel Image Optimization, you can explore the following:

---

## Getting Started with Routing Middleware

**URL:** https://vercel.com/docs/routing-middleware/getting-started

**Contents:**
- Getting Started with Routing Middleware
- What you will learn
- Prerequisites
- Creating a Routing Middleware
  - Create a new file for your Routing Middleware
  - Redirecting users
  - Configure which paths trigger the middleware
  - Debugging Routing Middleware
- More resources

Routing Middleware lets you to run code before your pages load, giving you control over incoming requests. It runs close to your users for fast response times and are perfect for redirects, authentication, and request modification.

Routing Middleware is available on the Node.js, Bun, and Edge runtimes. Edge is the default runtime for Routing Middleware. To use Node.js, configure the in your middleware config. To use Bun, set in your file.

The following steps will guide you through creating your first Routing Middleware.

Create a file called in your project root (same level as your ) and add the following code:

Deploy your project and visit any page. You should see "Logging request URL from Middleware" instead of your normal page content.

To redirect users based on their URL, add a new route to your project called , and modify your to include a redirect condition.

Try visiting - you should be redirected to .

By default, Routing Middleware runs on every request. To limit it to specific paths, you can use the object:

See the API Reference for more details on the object and matcher patterns.

When things don't work as expected:

Learn more about Routing Middleware by exploring the following resources:

---

## Navigating the Dashboard

**URL:** https://vercel.com/docs/dashboard-features/overview

**Contents:**
- Navigating the Dashboard
- Projects and repositories
  - Project Dashboard
- Search
- Create

When you sign in to Vercel through your browser, you'll be presented with the dashboard. Any subsequent visits to vercel.com will automatically direct you to the dashboard.

Your dashboard view shows a list of all projects and repositories that belong to the selected team.

You can click on the button to filter by a specific Repository and to choose whether to sort by Activity (which projects you have most recently viewed in the dashboard or deployed to) or Name (alphabetically).

You can use the toggle to change the view between a grid view and list view. Your viewing preference is saved to your account, so if you access your account on another machine, you'll see the same view each time.

Each project in the view shows:

You can click on the button to:

You can select any project to bring up its Project Dashboard, which allows you to view information about its deployments and configure its settings.

Learn more in our project dashboard docs.

Use the searchbar to search for the name of any deployed project.

For accounts on a Hobby plan, you can either create a new team or a new project.

For members of a team, depending on your permissions, you can use the Add New… button to add a new project, domain, or team Member.

The Add New drop-down to create a new project, domain, or team member.

---

## Monitoring Quickstart

**URL:** https://vercel.com/docs/query/monitoring/quickstart

**Contents:**
- Monitoring Quickstart
- Prerequisites
- Create a new query
  - Go to the dashboard
  - Add Visualize clause
  - Add Where clause
  - Add Group By clause
  - Add Limit clause
  - Save and Run Query

In the following guide you will learn how to view the most requested posts on your website.

The Visualize clause specifies which field in your query will be calculated. Set the Visualize clause to to monitor the most popular posts on your website.

Click the Run Query button, and the Monitoring chart will display the total number of requests made.

To filter the query data, use the Where clause and specify the conditions you want to match against. You can use a combination of variables and operators to fetch the most requested posts. Add the following query statement to the Where clause:

This query retrieves data with a host field of and a field that starts with /posts.

The character can be used as a wildcard to match any sequence of characters after , allowing you to capture all values that start with that substring.

Define a criteria that groups the data based on the selected attributes. The grouping mechanism is supported through the Group By clause.

Set the Group By clause to .

With Visualize, Where, and Group By fields set, the Monitoring chart now shows the sum of that are filtered based on the .

To control the number of results returned by the query, use the Limit clause and specify the desired number of results. You can choose from a few options, such as 5, 10, 25, 50, or 100 query results. For this example, set the limit to 5 query results.

Save your query and click the Run Query button to generate the final results. The Monitoring chart will display a comprehensive view of the top 5 most requested posts on your website.

---

## Vercel CLI Overview

**URL:** https://vercel.com/docs/cli

**Contents:**
- Vercel CLI Overview
- Installing Vercel CLI
- Updating Vercel CLI
- Checking the version
- Using in a CI/CD environment
- Available Commands

Vercel gives you multiple ways to interact with and configure your Vercel Projects. With the command-line interface (CLI) you can interact with the Vercel platform using a terminal, or through an automated system, enabling you to retrieve logs, manage certificates, replicate your deployment environment locally, manage Domain Name System (DNS) records, and more.

If you'd like to interface with the platform programmatically, check out the REST API documentation.

To download and install Vercel CLI, run the following command:

When there is a new release of Vercel CLI, running any command will show you a message letting you know that an update is available.

If you have installed our command-line interface through npm or Yarn, the easiest way to update it is by running the installation command yet again.

If you see permission errors, please read npm's official guide. Yarn depends on the same configuration as npm.

The option can be used to verify the version of Vercel CLI currently being used.

Vercel CLI requires you to log in and authenticate before accessing resources or performing administrative tasks. In a terminal environment, you can use , which requires manual input. In a CI/CD environment where manual input is not possible, you can create a token on your tokens page and then use the option to authenticate.

---

## Getting Started

**URL:** https://vercel.com/docs/redirects/bulk-redirects/getting-started

**Contents:**
- Getting Started
- Get started with bulk redirects
  - Create your redirect file
  - Configure bulkRedirectsPath
  - Deploy
- Available fields

Learn how to use bulk redirects to manage thousands of redirects that do not require wildcard or header matching functionality.

You can create fixed files of redirects, or generate them at build time as long as they end up in the location specified by bulkRedirectsPath before the build completes.

Add the property to your file, pointing to your redirect file. You can also point to a folder containing multiple redirect files if needed.

Deploy your project to Vercel. Your bulk redirects will be processed and applied automatically.

Any errors processing the bulk redirects will appear in the build logs for the deployment.

Each redirect supports the following fields:

In order to improve space efficiency, all boolean values can be the single characters (true) or (false) while using the CSV format.

For complete configuration details and advanced options, see the configuration reference.

---

## Getting started with Flags Explorer

**URL:** https://vercel.com/docs/feature-flags/flags-explorer/getting-started

**Contents:**
- Getting started with Flags Explorer
- Prerequisites
- Quickstart
  - Add the Flags SDK to your project
  - Adding a
  - Creating the Flags Discovery Endpoint
  - Handling overrides
  - Emitting flag values (optional)
  - Review
- More resources

Flags Explorer is available on all plans

This guide walks you through connecting your application to the Flags Explorer, so you can use it to view and override your application's feature flags. This works with any framework, any feature flag provider and even custom setups.

Install the package. This package provides convenience methods, components, and types that allow your application to communicate with the Flags Explorer.

This secret is used to encrypt and sign overrides, and so Flags Explorer can make authenticated requests to the API endpoint we'll create in the next step.

Run your application locally with Vercel Toolbar enabled and open Flags Explorer from the toolbar. Click on "Start setup" to begin the onboarding flow, then click on "Create secret" to automatically generate and add a new environment variable to your project.

Pull your environment variables to make them available to your project locally.

If you prefer to create the secret manually, see the instructions in the Flags Explorer Reference.

Your application needs to expose an API endpoint that Flags Explorer queries to get your feature flags. Flags Explorer will make an authenticated request to this API endpoint to receive your application's feature flag definitions. This endpoint can communicate the name, origin, description, and available options of your feature flags.

Using the Flags SDK for Next.js

Ensure you completed the setup of the Flags SDK for Next.js. You should have installed the package and have a file at the root of your project which exposes your feature flags as shown below.

Create your Flags Discovery Endpoint using the snippet below.

This endpoint uses to prevent unauthorized requests, and the function to automatically generate the feature flag definitions based on the feature flags you have defined in code. See the Flags SDK API Reference for more information.

If you are using the Flags SDK with adapters, use the function exported by your flag provider's adapter to load flag metadata from your flag providers. See the Flags SDK Adapters API Reference for more information, and mergeProviderData to combine the feature flags defined in code with the metadata of providers.

Using the Flags SDK for SvelteKit

If you are using the Flags SDK for SvelteKit then the function will automatically create the API endpoint for you. Learn more about using the Flags SDK for SvelteKit.

Learn how to manually return feature flag definitions in the Flags Explorer Reference.

You can now use the Flags Explorer to create feature flag overrides. When you create an override Flags Explorer will set a cookie containing those overrides. Your application can then read this cookie and respect those overrides. You can optionally check the signature on the overrides cookie to ensure it originated from a trusted source.

Using the Flags SDK for Next.js

Feature flags defined in code using the Flags SDK for Next.js will automatically handle overrides set by the Flags Explorer.

Using the Flags SDK for SvelteKit

Feature flags defined in code using the Flags SDK for SvelteKit will automatically handle overrides set by the Flags Explorer.

If you have a custom feature flag setup, or if you are using the SDKs of feature flag providers directly, you need to manually handle the overrides set by the Flags Explorer.

Learn how to read the overrides cookie in the Flags Explorer Reference.

You can optionally make the Flags Explorer aware of the actual value each feature flag resolved to while rendering the current page by rendering a component. This is useful for debugging. Learn how to emit flag values in the Flags Explorer Reference.

If you emit flag values to the client it's further possible to annotate your Web Analytics events with the feature flags you emitted. Learn how to integrate with Web Analytics.

You should now be able to see your feature flags in Flags Explorer. You should also be able to set overrides that your application can respect by using the Flags SDK or reading the cookie manually. If you added the component, you should be able to see the actual value each flag resolved to while rendering the current page.

---

## Getting started with Speed Insights

**URL:** https://vercel.com/docs/speed-insights/quickstart

**Contents:**
- Getting started with Speed Insights
- Prerequisites
  - Enable Speed Insights in Vercel
  - Add to your project
  - Deploy your app to Vercel
  - View your data in the dashboard
- Next steps

This guide will help you get started with using Vercel Speed Insights on your project, showing you how to enable it, add the package to your project, deploy your app to Vercel, and view your data in the dashboard.

Speed Insights is available on all plans

To view instructions on using the Vercel Speed Insights in your project for your framework, use the Choose a framework dropdown on the right (at the bottom in mobile view).

On the Vercel dashboard, select your Project followed by the Speed Insights tab. You can also select the button below to be taken there. Then, select Enable from the dialog.

Enabling Speed Insights will add new routes (scoped at) after your next deployment.

You can deploy your app to Vercel's global CDN by running the following command from your terminal:

Alternatively, you can connect your project's git repository, which will enable Vercel to deploy your latest pushes and merges to main.

Once your app is deployed, it's ready to begin tracking performance metrics.

If everything is set up correctly, you should be able to find the script inside the body tag of your page.

Once your app is deployed, and users have visited your site, you can view the data in the dashboard.

To do so, go to your dashboard, select your project, and click the Speed Insights tab.

After a few days of visitors, you'll be able to start exploring your metrics. For more information on how to use Speed Insights, see Using Speed Insights.

Learn more about how Vercel supports privacy and data compliance standards with Vercel Speed Insights.

Now that you have Vercel Speed Insights set up, you can explore the following topics to learn more:

---

## Projects and deployments

**URL:** https://vercel.com/docs/getting-started-with-vercel/projects-deployments

**Contents:**
- Projects and deployments
  - More resources

To get started with Vercel, it's helpful to understand projects and deployments:

To get started you'll create a new project by either deploying a template or importing and deploying an existing project:

---

## Getting started with cron jobs

**URL:** https://vercel.com/docs/cron-jobs/quickstart

**Contents:**
- Getting started with cron jobs
- Prerequisites
  - Create a function
  - Create or update your vercel.json file
  - Deploy your project.
- Next steps

This guide will help you get started with using cron jobs on Vercel. Cron jobs are scheduled tasks that run at specific times or intervals. They are useful for automating tasks. You will learn how to create a cron job that runs every day at 5 am UTC by creating a Vercel Function and configuring it in your file.

This function contains the code that will be executed by the cron job. This example uses a simple function that returns the user's region.

Create or go to your file and add the following code:

The property is an array of cron jobs. Each cron job has two properties:

When you deploy your project, Vercel's build process creates the cron job. Vercel invokes cron jobs only for production deployments and not for preview deployments

You can also deploy to your production domain using the CLI:

Your cron job is now active and will call the path every day at 5:00 am UTC.

Now that you have created a cron job, you can learn more about how to manage and configure them:

---

## Getting started with microfrontends

**URL:** https://vercel.com/docs/microfrontends/quickstart

**Contents:**
- Getting started with microfrontends
- Prerequisites
- Key concepts
- Set up microfrontends on Vercel
  - Create a microfrontends group
  - Define
  - Install the package
  - Set up microfrontends with your framework
  - Run through steps 3 and 4 for all microfrontend applications in the group
  - Set up the local development proxy

This quickstart guide will help you set up microfrontends on Vercel. Microfrontends can be used with different frameworks, and separate frameworks can be combined in a single microfrontends group.

Choose a framework to optimize documentation to:

Before diving into implementation, it's helpful to understand these core concepts:

Creating a microfrontends group and adding projects to that group does not change any behavior for those applications until you deploy a file to production.

Once the microfrontends group is created, you can define a file at the root in the default application. This configuration file is only needed in the default application, and it will control the routing for microfrontends. In this example, is the default application.

Production behavior will not be changed until the file is merged and promoted, so you test in the Preview environment before deploying changes to production.

On the Settings page for the new microfrontends group, click the Add Config button to copy the to your code.

You can also create the configuration manually in code:

Application names in should match the Vercel project names, see the microfrontends configuration documentation for more information.

See the path routing documentation for details on how to configure the routing for your microfrontends.

In the directory of the microfrontend application, install the package using the following command:

You need to perform this step for every microfrontend application.

Once the file has been added, Vercel will be able to start routing microfrontend requests to each microfrontend. However, the specifics of each framework, such as JS, CSS, and images, also need to be routed to the correct application.

Any static asset not covered by the framework instructions above, such as images or any file in the directory, will also need to be added to the microfrontends configuration file or be moved to a path prefixed by the application's asset prefix. An asset prefix of (in , or in prior versions) is automatically set up by the Vercel microfrontends support.

Set up the other microfrontends in the group by running through steps 3 and 4 for every application.

To provide a seamless local development experience, provides a microfrontends aware local development proxy to run alongside you development servers. This proxy allows you to only run a single microfrontend locally while making sure that all microfrontend requests still work.

If you are using Turborepo, the proxy will automatically run when you run the development task for your microfrontend.

If you don't use , you can set this up by adding a script to your like this:

Next, use the auto-generated port in your command so that the proxy knows where to route the requests to:

Once you have your application and the local development proxy running (either via or manually), visit the "Microfrontends Proxy" URL in your terminal output. Requests will be routed to your local app or your production fallback app. Learn more in the local development guide.

You can now deploy your code to Vercel. Once live, you can then visit the domain for that deployment and visit any of the paths configured in . These paths will be served by the other microfrontend applications.

In the example above, visiting the page will see the content from the microfrontend while visiting will see the content from the microfrontend.

Microfrontends functionality can be tested in Preview before deploying the code to production.

Microfrontends changes how paths are routed to your projects. If you encounter any issues, look at the Testing & Troubleshooting documentation or learn how to debug routing on Vercel.

---

## Use a template

**URL:** https://vercel.com/docs/getting-started-with-vercel/template

**Contents:**
- Use a template
  - Using CLI?
  - Find a template
  - Deploy the template to Vercel
  - Connect your Git provider
  - Project deployment
  - View your dashboard
  - Clone the project to your machine
- Next Steps

Clone the template to your local machine and use the following snippet to deploy the template with Vercel CLI:

Clone the template to your local machine and use the following snippet to deploy the template with Vercel CLI:

Accelerate your development on Vercel with Templates. This guide will show you how to use templates to fast-track project setup, leverage popular frontend frameworks, and maximize Vercel's features.

From https://vercel.com/templates, select the template you’d like to deploy. You can use the filters to select a template based on use case, framework, and other requirements.

Not sure which one to use? How about exploring Next.js.

Once you've selected a template, Click Deploy on the template page to start the process.

To ensure you can easily update your project after deploying it, Vercel will create a new repository with your chosen Git provider. Every push to that Git repository will be deployed automatically.

First, select the Git provider that you'd like to connect to. Once you’ve signed in, you’ll need to set the scope and repository name. At this point, Vercel will clone a copy of the source code into your Git account.

Once the project has been cloned to your git provider, Vercel will automatically start deploying the project. This starts with building your project, then assigning the domain, and finally celebrating your deployed project with confetti.

At this point, you’ve created a production deployment, with its very own domain assigned. If you continue to your dashboard, you can click on the domain to preview a live, accessible URL that is instantly available on the internet.

Finally, you'll want to clone the source files to your local machine so that you can make some changes later. To do this from your dashboard, select the Git repository button and clone the repository.

Because you used a template, we’ve automatically included any additional environment set up as part of the template. You can customize your project by configuring environment variables and build options.

Environment Variables are key-value pairs that can be defined in your project settings for each Environment. Teams can also use shared environment variables that are linked between multiple projects.

Vercel automatically configures builds settings based on your framework, but you can customize the build in your project settings or within a vercel.json file.

Next, learn how to assign a domain to your new deployment.

---

## Speed Insights Overview

**URL:** https://vercel.com/docs/speed-insights

**Contents:**
- Speed Insights Overview
- Dashboard view
- More resources

Speed Insights is available on all plans

Vercel Speed Insights provides you with a detailed view of your website's performance metrics, based on Core Web Vitals, enabling you to make data-driven decisions for optimizing your site. For granular visitor data, use Web Analytics.

The Speed Insights dashboard offers in-depth information about scores and individual metrics without the need for code modifications or leaving the Vercel dashboard.

To get started, follow the quickstart to enable Speed Insights and learn more about the dashboard view and metrics.

When you enable Speed Insights, data will be tracked on all deployed environments, including preview and production deployments.

Once you enable Speed Insights, you can access the dashboard by selecting your project in the Vercel dashboard, and clicking the Speed Insights tab.

The Speed Insights dashboard displays data that you can sort and inspect based on a variety of parameters:

The data in the Kanban and map views is selectable so that you can filter by country, route, path and HTML element. The red, orange and green colors in the map view indicate the P75 score.

---

## Getting started with Vercel Functions

**URL:** https://vercel.com/docs/functions/quickstart

**Contents:**
- Getting started with Vercel Functions
- Prerequisites
- Create a Vercel Function
- Next steps

In this guide, you'll learn how to get started with Vercel Functions using your favorite frontend framework (or no framework).

Open the code block in v0 for a walk through on creating a Vercel Function with the below code, or copy the code into your project. The function fetches data from the Vercel API and returns it as a JSON response.

While using is the recommended way to create a Vercel Function, you can still use HTTP methods like and .

Now that you have set up a Vercel Function, you can explore the following topics to learn more:

---

## Getting started with ISR

**URL:** https://vercel.com/docs/incremental-static-regeneration/quickstart

**Contents:**
- Getting started with ISR
- Background Revalidation
  - Example
- On-Demand Revalidation
- Templates
- Explore ISR with a project template
- Next steps

This guide will help you get started with using Incremental Static Regeneration (ISR) on your project, showing you how to regenerate your pages without rebuilding and redeploying your site. When a page with ISR enabled is regenerated, the most recent data for that page is fetched, and its cache is updated. There are two ways to trigger regeneration:

Background revalidation allows you to purge the cache for an ISR route automatically on an interval.

The following example renders a list of blog posts from a demo site called , revalidating every 10 seconds or whenever a person visits the page:

To test this code, run the appropriate command for your framework, and navigate to the route.

You should see a bulleted list of blog posts.

On-demand revalidation allows you to purge the cache for an ISR route whenever you want, foregoing the time interval required with background revalidation.

Get started in minutes

Instantly update content without redeploying.

ISR Blog with Next.js and WordPress

An Incremental Static Regeneration Blog Example Using Next.js and WordPress

Nitro - Cached HTTP handler

A Nitro HTTP handler with ISR

Now that you have set up ISR, you can explore the following:

---

## Use an existing domain

**URL:** https://vercel.com/docs/getting-started-with-vercel/use-existing

**Contents:**
- Use an existing domain
  - Using CLI?
  - Go to your project's domains settings
  - Add your existing domain to your project
  - Configure your DNS records
- Next steps

Use this snippet to add a domain that you own to a Vercel project:

Use this snippet to add a domain that you own to a Vercel project:

Already have a domain you love? Seamlessly integrate it with Vercel to leverage the platform's powerful features and infrastructure. Whether you're migrating an existing project or want to maintain your established online presence, you can use the steps below to add your custom domain.

Select your project and select the Settings tab. Then, select the Domains menu item or click on this link and select your project

From the Domains page, enter the domain you wish to add to the project.

If you add an apex domain (e.g. ) to the project, Vercel will prompt you to add the subdomain prefix, the apex domain, and some basic redirection options.

For more information on which redirect option to choose, see Redirecting domains.

Configure the DNS records of your domain with your registrar so it can be used with your Project. The dashboard will automatically display different methods for configuring it:

Both apex domains and subdomains can also be configured using the Nameservers method. Wildcard domains must use the nameservers method for verification. For more information see Add a custom domain.

Next, learn how to take advantage of Vercel's collaboration features as part of your developer workflow:

Use Vercel in your developer workflow

---

## Dashboard Overview

**URL:** https://vercel.com/docs/dashboard-features

**Contents:**
- Dashboard Overview
- Scope selector
- Find
- Overview
- Integrations
- Activity
- Recent Previews
- Domains
- Usage
- Settings

You can use the Vercel dashboard to view and manage all aspects of the Vercel platform, including your Projects and Deployments. What you see in each tab is dependant on the scope that is selected.

What you see in each tab is dependant on the scope that is selected.

The scope selector allows you to switch between your Hobby team and any teams that you may be part of. To switch between accounts and teams, select the arrows next to the name:

To go back to your Team dashboard at any time, click the Vercel logo or the scope selector.

The Find bar allows you to search for:

Access this feature by clicking on the Find search input on the top right of the Vercel dashboard or pressing F on your keyboard.

When you first create an account and log on to Vercel, you'll be greeted by your team overview. This shows information on all projects that you have on the selected Vercel team.

You can click on the button to filter by a specific Repository and to choose whether to sort by Activity (which projects you have most recently viewed in the dashboard or deployed to) or Name (alphabetically). Next to the button is a toggle you can use to switch between card view and list view. You can also filter to a certain repository by clicking the pill for that repository on any of its projects.

Integrations allow you to extend the capabilities of Vercel and connect with third-party platforms or services. Users and Teams on all plans can use or create Integrations.

Through the Integrations section on the dashboard, you can view and manage a list of all integrations on your account, browse the marketplace to install integrations, or go to the Integrations Console to create your own Integration.

The Activity Log provides a list of all events on a Hobby team, chronologically organized since its creation. The events that you will see are dependant on the type of account and role within a Team.

The recent previews panel gives you a quick way to access recently deployed and viewed previews within your teams. It's scoped to the team you are actively viewing.

Each listed preview shows the latest deployment ID and status. Any associated pull request to your git provider is also shown or the relevant git branch.

Selecting a preview from the list will navigate to the live preview.

You can also navigate to related items for a preview deployment:

Each preview deployment item also has a context menu where you can see further details and also remove the listing.

By default, all deployments are assigned a domain with the suffix: . This domain can be replaced with a Custom Domain of your choice.

The Domains section of the dashboard lets you view all domains related to your account or Team, and allows you to Buy, Add, or Transfer In a custom domain.

The Usage tab on the Dashboard provides detailed insight into the actual resource usage of all projects relating to your account or Team.

From the dashboard, you can filter the usage by billing cycle, date, project, or function.

There are two different types of settings pages:

Personal Account / Team Settings - These settings allow you to manage account details, billing, invoicing, membership, security, and tokens. The options you see will depend on the your scope and permissions.

Project Settings - You can view this by selecting a project in the dashboard and then selecting its settings. From there you can manage project details, domains, integrations, Git, functions, environment variables, and security.

My settings dashboard

Vercel provides a Command Menu that enables you to navigate through the dashboard and perform common actions using only the keyboard.

You can access the menu using by pressing ⌘ + K on macOS or Ctrl + K on Windows and Linux. Note that you must be logged in to access the Command Menu.

---

## Getting started with Vercel Web Analytics

**URL:** https://vercel.com/docs/analytics/quickstart

**Contents:**
- Getting started with Vercel Web Analytics
- Prerequisites
  - Enable Web Analytics in Vercel
  - Deploy your app to Vercel
  - View your data in the dashboard
- Next steps

This guide will help you get started with using Vercel Web Analytics on your project, showing you how to enable it, add the package to your project, deploy your app to Vercel, and view your data in the dashboard.

Select your framework to view instructions on using the Vercel Web Analytics in your project.

On the Vercel dashboard, select your Project and then click the Analytics tab and click Enable from the dialog.

Enabling Web Analytics will add new routes (scoped at ) after your next deployment.

Deploy your app using the following command:

If you haven't already, we also recommend connecting your project's Git repository, which will enable Vercel to deploy your latest commits to main without terminal commands.

Once your app is deployed, it will start tracking visitors and page views.

If everything is set up properly, you should be able to see a Fetch/XHR request in your browser's Network tab from when you visit any page.

Once your app is deployed, and users have visited your site, you can view your data in the dashboard.

To do so, go to your dashboard, select your project, and click the Analytics tab.

After a few days of visitors, you'll be able to start exploring your data by viewing and filtering the panels.

Users on Pro and Enterprise plans can also add custom events to their data to track user interactions such as button clicks, form submissions, or purchases.

Learn more about how Vercel supports privacy and data compliance standards with Vercel Web Analytics.

Now that you have Vercel Web Analytics set up, you can explore the following topics to learn more:

---

## Comments Overview

**URL:** https://vercel.com/docs/comments

**Contents:**
- Comments Overview
- More resources

Comments are available on all plans

Comments allow teams and invited participants to give direct feedback on preview deployments or other environments through the Vercel Toolbar. Comments can be added to any part of the UI, opening discussion threads that can be linked to Slack threads. This feature is enabled by default on all preview deployments, for all account plans, free of charge. The only requirement is that all users must have a Vercel account.

Pull request owners receive emails when a new comment is created. Comment creators and participants in comment threads will receive email notifications alerting them to new activity within those threads. Anyone in your Vercel team can leave comments on your previews by default. On Pro and Enterprise plans, you can invite external users to view your deployment and leave comments.

When changes are pushed to a PR, and a new preview deployment has been generated, a popup modal in the bottom-right corner of the deployment will prompt you to refresh your view:

Comments are a feature of the Vercel Toolbar and the toolbar must be active to see comments left on a page. You can activate the toolbar by clicking on it. For users who intend to use comments frequently, we recommend downloading the browser extension and toggling on Always Activate in Preferences from the Toolbar menu. This sets the toolbar to always activate so you will see comments on pages without needing to click to activate it.

---

## Add a domain

**URL:** https://vercel.com/docs/getting-started-with-vercel/domains

**Contents:**
- Add a domain
  - Next steps

Assigning a custom domain to your project guarantees that visitors to your application will have a tailored experience that aligns with your brand.

On Vercel, this domain can have any format of your choosing:

If you already own a domain, you can point it to Vercel, or transfer it over. If you don't own one yet, you can purchase a new one. For this tutorial, feel free to use that one domain you bought 11 months ago and haven’t got around to using yet!

For more information on domains at Vercel, see Domains overview.

Now that your site is deployed, you can to personalize it by setting up a custom domain. With Vercel you can either buy a new domain or use an existing domain.

---

## Next Steps

**URL:** https://vercel.com/docs/getting-started-with-vercel/next-steps

**Contents:**
- Next Steps
- Infrastructure
- Storage
- Observability
- Security

Congratulations on getting started with Vercel!

Now, let's explore what's next on your journey. At this point, you can either continue learning more about Vercel's many features, or you can dive straight in and get to work. The choice is yours!

Dive into my dashboard

Manage your projects, domains, and more.

Alternatively, you can start learning about many of the products and features that Vercel provides:

Learn about Vercel's CDN and implement scalable infrastructure in your app using Functions. Get started today by implementing a Vercel Function in your app:

Vercel offers a suite of managed, serverless storage products that integrate with your frontend framework.

Learn more about which storage option is right for you and get started with implementing them:

Vercel provides a suite of observability tools to allow you to monitor, analyze, and manage your site.

Vercel takes security seriously. It uses HTTPS by default for secure data transmission, regularly updates its platform to mitigate potential vulnerabilities, limits system access for increased safety, and offers built-in DDoS mitigation. This layered approach ensures robust protection for your sites and applications.

---

## Domains Overview

**URL:** https://vercel.com/docs/domains

**Contents:**
- Domains Overview
- More resources

A domain is a user-friendly way of referring to the address access a website on the internet. For example, the domain you're reading this on is . Domains can be analogous to the address where your house is. When someone sends a letter to your house, they don't need to know exactly where it is, they just need the address and the relevant post office handles routing the letter.

The system that manages the details about where a site is located on the internet, is known as DNS or the Domain Name System. At its most basic, DNS maps human-readable domain names to computer-friendly IP addresses. When you request a site in your browser, the first step is converting the domain address to an IP address. That process is handled by DNS and called DNS Resolution. Understanding how DNS works is important to ensure that you are configuring your domain correctly.

You enter in your browser. Your browser will first check its local DNS cache to see if it knows the IP address of . If it does, it will request the site from that address.

Your browser initiates a DNS query through a server known as a recursive resolver, usually provided by your ISP or a third-party. The recursive resolver acts as a middleman between the browser and DNS server and is used to increase the speed and efficiency of the resolution process. The resolver will check its cache first to see if it already has the IP address. If it doesn't, it'll request the IP address from a DNS server.

There is a network of DNS servers, in a hierarchy, located all around the world. The recursive resolver will query in the following pattern:

Once your browser has the IP address, an HTTP request is made by the browser to the web server located at that IP address.

This list is just a general overview and doesn't happen every time. Most of us tend to visit the same sites over and over. Therefore, the request will first check the cache from your browser and then from the recursive resolver, allowing for quicker load times. In addition, this example describes a basic unicast DNS network. In reality, when using Vercel, you're using anycast servers on the Vercel CDN.

This overview shows a point of view of a user visiting your site. But what does this look like when you're the developer creating a site?

When you've created a Project and deployed it on Vercel, your site lives on Vercel's web servers, which we know to be at the IP address . However, your user's browser doesn't know that. For this reason, the browser will perform a DNS Lookup to retrieve the correct IP mapping to from a DNS server.

This is where, as a developer, you may have to configure the DNS settings to tell the authoritative server exactly where your site lives. Vercel guides you through exactly what information you need to set, within your Dashboard. There are a number of different settings that you should be aware of:

---
