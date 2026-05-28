# Vercel - Frameworks

**Pages:** 23

---

## xmcp on Vercel

**URL:** https://vercel.com/docs/frameworks/backend/xmcp

**Contents:**
- xmcp on Vercel
- Get started with xmcp on Vercel
  - Get started with Vercel CLI
- Local development
- Middleware
  - xmcp Middleware
  - Vercel Routing Middleware
- Vercel Functions
- More resources

is a TypeScript-first framework for building MCP-compatible backends. It provides an opinionated project structure, automatic tool discovery, and a streamlined middleware layer for request/response processing. You can deploy an xmcp app to Vercel with zero configuration.

Start with xmcp on Vercel by creating a new xmcp project:

This scaffolds a project with a directory for tools, optional , and an file.

To deploy, connect your Git repository or use Vercel CLI:

Get started by initializing a new Xmcp project using Vercel CLI init command:

This will clone the Xmcp example repository in a directory called .

To run your xmcp application locally, you can use Vercel CLI:

Alternatively, use your project's dev script:

In xmcp, an optional lets you run code before and after tool execution. This is commonly used for logging, auth, or request shaping:

In Vercel, Routing Middleware executes before a request is processed by your application. Use it for rewrites, redirects, headers, or personalization, and combine it with xmcp's own middleware as needed.

When you deploy an xmcp app to Vercel, your server endpoints automatically run as Vercel Functions and use Fluid compute by default.

---

## Remix on Vercel

**URL:** https://vercel.com/docs/frameworks/full-stack/remix

**Contents:**
- Remix on Vercel
- Getting started
- Deploy a new Remix project with a template
- Vercel Vite Preset
- Server-Side Rendering (SSR)
  - Vercel Functions
- Response streaming
- headers
- Analytics
- Using a custom file

Remix is a fullstack, server-rendered React framework. Its built-in features for nested pages, error boundaries, transitions between loading states, and more, enable developers to create modern web apps.

With Vercel, you can deploy server-rendered Remix and Remix V2 applications to Vercel with zero configuration. When using the Remix Vite plugin, static site generation using SPA mode is also supported.

It is highly recommended that your application uses the Remix Vite plugin, in conjunction with the Vercel Preset, when deploying to Vercel.

To get started with Remix on Vercel:

Get started in minutes

Ecommerce Template with Crystallize and Remix

A fully-featured eCommerce boilerplate built using Remix and Crystallize with performance in mind.

A new Remix app — the result of running `npx create-remix`.

Product Roadmap Voting App

Public roadmap app for your product powered by Rowy and Firebase

Vercel deployments can integrate with your git provider to generate preview URLs for each pull request you make to your Remix project.

The package exposes useful types and utilities for Remix apps deployed on Vercel, such as:

To best experience Vercel features such as streaming, Vercel Functions, and more, we recommend importing utilities from rather than from standard Remix packages such as .

should be used anywhere in your code that you normally would import utility functions from the following packages:

To get started, navigate to the root directory of your Remix project with your terminal and install with your preferred package manager:

When using the Remix Vite plugin (highly recommended), you should configure the Vercel Preset to enable the full feature set that Vercel offers.

To configure the Preset, add the following lines to your file:

Using this Preset enables Vercel-specific functionality such as rendering your Remix application with Vercel Functions.

Server-Side Rendering (SSR) allows you to render pages dynamically on the server. This is useful for pages where the rendered data needs to be unique on every request. For example, checking authentication or looking at the location of an incoming request.

Remix routes defined in are deployed with server-side rendering by default.

The following example demonstrates a basic route that renders with SSR:

Vercel Functions execute using Node.js. They enable developers to write functions that use resources that scale up and down based on traffic demands. This prevents them from failing during peak hours, but keeps them from running up high costs during periods of low activity.

Remix API routes in are deployed as Vercel Functions by default.

The following example demonstrates a basic route that renders a page with the heading, "Welcome to Remix with Vercel":

To summarize, Server-Side Rendering (SSR) with Remix on Vercel:

with Remix on Vercel is supported with Vercel Functions. See the Streaming page in the Remix docs for general instructions.

The following example demonstrates a route that simulates a throttled network by delaying a promise's result, and renders a loading state until the promise is resolved:

To summarize, Streaming with Remix on Vercel:

Learn more about Streaming

Vercel's CDN caches your content at the edge in order to serve data to your users as fast as possible. Static caching works with zero configuration.

By adding a header to responses returned by your Remix routes, you can specify a set of caching rules for both client (browser) requests and server responses. A cache must obey the requirements defined in the Cache-Control header.

Remix supports header modifications with the function, which you can export in your routes defined in .

The following example demonstrates a route that adds headers which instruct the route to:

See our docs on cache limits to learn the max size and lifetime of caches stored on Vercel.

To summarize, using headers with Remix on Vercel:

Learn more about caching

Vercel's Analytics features enable you to visualize and monitor your application's performance over time. The Analytics tab in your project's dashboard offers detailed insights into your website's visitors, with metrics like top pages, top referrers, and user demographics.

To use Analytics, navigate to the Analytics tab of your project dashboard on Vercel and select Enable in the modal that appears.

To track visitors and page views, we recommend first installing our package by running the terminal command below in the root directory of your Remix project:

Then, follow the instructions below to add the component to your app. The component is a wrapper around Vercel's tracking script, offering a seamless integration with Remix.

Add the following component to your file:

To summarize, Analytics with Remix on Vercel:

Learn more about Analytics

By default, Vercel supplies an implementation of the file which is configured for streaming to work with Vercel Functions. This version will be used when no file is found in the project, or when the existing file has not been modified from the base Remix template.

However, if your application requires a customized or file (for example, to wrap the component with a React context), you should base it off of this template:

Defining a custom file is not supported when using the Remix Vite plugin on Vercel.

It's usually not necessary to define a custom server.js file within your Remix application when deploying to Vercel. In general, we do not recommend it.

If your project requires a custom file, you will need to install and import from . The following example demonstrates a basic file:

See our Frameworks documentation page to learn about the benefits available to all frameworks when you deploy on Vercel.

Learn more about deploying Remix projects on Vercel with the following resources:

---

## Flask on Vercel

**URL:** https://vercel.com/docs/frameworks/backend/flask

**Contents:**
- Flask on Vercel
- Get started with Flask on Vercel
  - Get started with Vercel CLI
- Exporting the Flask application
  - Build command
  - Local development
  - Deploying the application
- Serving static assets
- Vercel Functions
- Limitations

Flask is a lightweight WSGI web application framework for Python. It's designed with simplicity and flexibility in mind, making it easy to get started while remaining powerful for building web applications. You can deploy a Flask app to Vercel with zero configuration.

You can quickly deploy a Flask application to Vercel by creating a Flask app or using an existing one:

Get started by initializing a new Flask project using Vercel CLI init command:

This will clone the Flask example repository in a directory called .

To run a Flask application on Vercel, define an instance that initializes at any of the following entrypoints:

You can also define an application script in to point to your Flask app in a different module:

This script tells Vercel to look for a instance named in .

The property in defines the Build Command for Flask deployments. It runs after dependencies are installed and before your application is deployed.

Use to run your application locally.

To deploy, connect your Git repository or use Vercel CLI:

To serve static assets, place them in the directory. They will be served as a part of our CDN using default headers unless otherwise specified in .

Flask's should not be used for static files on Vercel. Use the directory instead.

When you deploy a Flask app to Vercel, the application becomes a single Vercel Function and uses Fluid compute by default. This means your Flask app will automatically scale up and down based on traffic.

All Vercel Functions limitations apply to Flask applications, including:

Learn more about deploying Flask projects on Vercel with the following resources:

---

## NestJS on Vercel

**URL:** https://vercel.com/docs/frameworks/backend/nestjs

**Contents:**
- NestJS on Vercel
- Get started with NestJS on Vercel
- NestJS entrypoint detection
  - Local development
  - Deploying the application
- Vercel Functions
- Limitations
- More resources

NestJS is a progressive Node.js framework for building efficient, reliable and scalable server-side applications. You can deploy a NestJS app to Vercel with zero configuration using Vercel Functions.

NestJS applications on Vercel benefit from:

You can quickly deploy a NestJS application to Vercel by creating a NestJS app or using an existing one:

To allow Vercel to deploy your NestJS application and process web requests, your server entrypoint file should be named one of the following:

For example, use the following code as an entrypoint:

Use to run your application locally

To deploy, connect your Git repository or use Vercel CLI:

When you deploy a NestJS app to Vercel, your NestJS application becomes a single Vercel Function and uses Fluid compute by default. This means your NestJS app will automatically scale up and down based on traffic.

All Vercel Functions limitations apply to the NestJS application, including the size of the application being limited to 250MB.

Learn more about deploying NestJS projects on Vercel with the following resources:

---

## TanStack Start on Vercel

**URL:** https://vercel.com/docs/frameworks/full-stack/tanstack-start

**Contents:**
- TanStack Start on Vercel
- Getting started
- Nitro Configuration
  - Vercel Functions
- More resources

TanStack Start is a fullstack framework powered by TanStack Router for React and Solid. It has support for full-document SSR, streaming, server functions, bundling and more. TanStack Start works great on Vercel when paired with Nitro.

You can quickly deploy a TanStack Start application to Vercel by creating a new one below or configuring an existing one with Nitro:

The Nitro Vite plugin allows deploying TanStack Start apps on Vercel, and integrates with Vercel's features.

To set up Nitro in your TanStack app, navigate to the root directory of your TanStack Start project with your terminal and install with your preferred package manager:

To configure Nitro with TanStack Start, add the following lines to your file:

TanStack Start apps on Vercel benefit from the advantages of Vercel Functions and use Fluid Compute by default. This means your TanStack Start app will automatically scale up and down based on traffic.

Learn more about deploying TanStack Start projects on Vercel with the following resources:

---

## Mastra

**URL:** https://vercel.com/docs/ai-gateway/framework-integrations/mastra

**Contents:**
- Mastra
- Getting started
  - Create a new Mastra project
  - Install dependencies
  - Configure environment variables
  - Configure your agent to use AI Gateway
  - Running the application

Mastra is a framework for building and deploying AI-powered features using a modern JavaScript stack powered by the Vercel AI SDK. Integrating with AI Gateway provides unified model management and routing capabilities.

First, create a new Mastra project using the CLI:

During the setup, the system prompts you to name your project, choose a default provider, and more. and more. Feel free to use the default settings.

To use the AI Gateway provider, install the package along with Mastra:

Create or update your file with your Vercel AI Gateway API key:

Now, swap out the package (or your existing model provider) for the package.

Update your agent configuration file, typically to the following code:

Since your agent is now configured to use AI Gateway, run the Mastra development server:

Open the Mastra Playground and Mastra API to test your agents, workflows, and tools.

---

## React Router on Vercel

**URL:** https://vercel.com/docs/frameworks/frontend/react-router

**Contents:**
- React Router on Vercel
- Vercel React Router Preset
- Server-Side Rendering (SSR)
- Response streaming
- headers
- Analytics
- Using a custom server entrypoint
- Using a custom file
- More benefits
- More resources

React Router is a multi-strategy router for React. When used as a framework, React Router enables fullstack, server-rendered React applications. Its built-in features for nested pages, error boundaries, transitions between loading states, and more, enable developers to create modern web apps.

With Vercel, you can deploy React Router applications with server-rendering or static site generation (using SPA mode) to Vercel with zero configuration.

It is highly recommended that your application uses the Vercel Preset when deploying to Vercel.

The optional package contains Vercel specific utilities for use in React Router applications. The package contains various entry points for specific use cases:

To get started, navigate to the root directory of your React Router project with your terminal and install with your preferred package manager:

When using the React Router as a framework, you should configure the Vercel Preset to enable the full feature set that Vercel offers.

To configure the Preset, add the following lines to your file:

When this Preset is configured, your React Router application is enhanced with Vercel-specific functionality:

Server-Side Rendering (SSR) allows you to render pages dynamically on the server. This is useful for pages where the rendered data needs to be unique on every request. For example, checking authentication or looking at the location of an incoming request. Server-Side Rendering is invoked using Vercel Functions.

Routes defined in your application are deployed with server-side rendering by default.

The following example demonstrates a basic route that renders with SSR:

To summarize, Server-Side Rendering (SSR) with React Router on Vercel:

with React Router on Vercel is supported with Vercel Functions. See the Streaming with Suspense page in the React Router docs for general instructions.

Streaming with React Router on Vercel:

Learn more about Streaming

Vercel's CDN caches your content at the edge in order to serve data to your users as fast as possible. Static caching works with zero configuration.

By adding a header to responses returned by your React Router routes, you can specify a set of caching rules for both client (browser) requests and server responses. A cache must obey the requirements defined in the Cache-Control header.

React Router supports defining response headers by exporting a headers function within a route.

The following example demonstrates a route that adds headers which instruct the route to:

See our docs on cache limits to learn the max size and lifetime of caches stored on Vercel.

To summarize, using headers with React Router on Vercel:

Learn more about caching

Vercel's Analytics features enable you to visualize and monitor your application's performance over time. The Analytics tab in your project's dashboard offers detailed insights into your website's visitors, with metrics like top pages, top referrers, and user demographics.

To use Analytics, navigate to the Analytics tab of your project dashboard on Vercel and select Enable in the modal that appears.

To track visitors and page views, we recommend first installing our package by running the terminal command below in the root directory of your React Router project:

Then, follow the instructions below to add the component to your app. The component is a wrapper around Vercel's tracking script, offering a seamless integration with React Router.

Add the following component to your file:

To summarize, Analytics with React Router on Vercel:

Learn more about Analytics

Your React Router application may define a custom server entrypoint, which is useful for supplying a "load context" for use by the application's loaders and actions.

The server entrypoint file is expected to export a Web API-compatible function that matches the following signature:

To implement a server entrypoint using the Hono web framework, follow these steps:

First define the property in your Vite config file:

Then, create the server entrypoint file:

To summarize, using a custom server entrypoint with React Router on Vercel allows you to:

By default, Vercel supplies an implementation of the file which is configured for streaming to work with Vercel Functions. This version will be used when no file is found in the project.

However, your application may define a customized or file if necessary. When doing so, your custom file should use the function exported by .

For example, to supply the option and set the corresponding response header:

See our Frameworks documentation page to learn about the benefits available to all frameworks when you deploy on Vercel.

Learn more about deploying React Router projects on Vercel with the following resources:

---

## Framework Integrations

**URL:** https://vercel.com/docs/ai-gateway/framework-integrations

**Contents:**
- Framework Integrations
  - Integration overview
  - Supported frameworks

The Vercel AI Gateway integrates with popular community AI frameworks and tools, enabling you to build powerful AI applications while leveraging the Gateway's features like cost tracking and unified API access.

You can integrate the AI Gateway with popular frameworks in several ways:

The following below list is a non-exhaustive list of frameworks that currently support AI Gateway integration:

---

## LangFuse

**URL:** https://vercel.com/docs/ai-gateway/framework-integrations/langfuse

**Contents:**
- LangFuse
- Getting started
  - Create a new project
  - Install dependencies
  - Configure environment variables
  - Create your LangFuse application
  - Running the application

LangFuse is an LLM engineering platform that helps teams collaboratively develop, monitor, evaluate, and debug AI applications. This guide demonstrates how to integrate Vercel AI Gateway with LangFuse to access various AI models and providers.

First, create a new directory for your project and initialize it:

Install the required LangFuse packages along with the and packages:

Create a file with your Vercel AI Gateway API key and LangFuse API keys:

If you're using the AI Gateway from within a Vercel deployment, you can also use the environment variable which will be automatically provided.

Create a new file called with the following code:

Run your application using Node.js:

You should see a response from the AI model in your console.

---

## Image Optimization with Vercel

**URL:** https://vercel.com/docs/image-optimization

**Contents:**
- Image Optimization with Vercel
- Get started
- Why should I optimize my images on Vercel?
- How Image Optimization works
- When to use Image Optimization
- Setting up remote or local patterns
  - Local images
    - Setting up local patterns
    - Local images cache key
  - Remote images

Image Optimization is available on all plans

Vercel supports dynamically transforming unoptimized images to reduce the file size while maintaining high quality. These optimized images are cached on the Vercel CDN, meaning they're available close to users whenever they're requested.

Image Optimization works with many frameworks, including Next.js, Astro, and Nuxt, enabling you to optimize images using built-in components.

Optimizing images on Vercel provides several advantages for your application:

The flow of image optimization on Vercel involves several steps, starting from the image request to serving the optimized image.

The optimization process starts with your component choice in your codebase:

When Next.js receives an image request, it checks the prop on the component or the configuration in the file to determine if optimization is disabled.

If optimization is enabled, Vercel validates the loader configuration (whether using the default or a custom loader) and verifies that the image source URL matches the allowed patterns defined in your configuration ( or ).

Vercel then checks the status of the cache to see if an image has been previously cached:

Image Optimization is ideal for:

In some cases, Image Optimization may not be necessary or beneficial, such as:

If your images meet any of the above criteria where Image Optimization is not beneficial, we recommend using the prop on the Next.js component. For guidance on SvelteKit, Astro, or Nuxt, see their documentation.

It's important that you are only optimizing images that need to be optimized otherwise you could end up using your image usage quota unnecessarily. For example, if you have a small icon or thumbnail that is under 10 KB, you should not use Image Optimization as these images are already very small and optimizing them further would not provide any benefits.

An important aspect of using the component is properly setting up remote/local patterns in your file. This configuration determines which images are allowed to be optimized.

You can set up patterns for both local images (stored as static assets in your folder) and remote images (stored externally). In both cases you specify the pathname the images are located at.

A local image is imported from your file system and analyzed at build time. The import is added to the prop:

To set up local patterns, you need to specify the pathname of the images you want to optimize. This is done in the file:

See the Next.js documentation for local patterns for more information.

The cache key for local images is based on the query string parameters, the HTTP header, and the content hash of the image URL.

A remote image requires the property to be a URL string, which can be relative or absolute.

To set up remote patterns, you need to specify the of the images you want to optimize. This is done in the file:

In the case of external images, you should consider adding your account id to the if you don't own the . For example . This helps protect your source images from potential abuse.

See the Next.js documentation for remote patterns for more information.

The cache key for remote images is based on the query string parameters, the HTTP header, and the content hash of the image URL.

Once an image is cached, it remains so even if you update the source image. For remote images, users accessing a URL with a previously cached image will see the old version until the cache expires or the image is invalidated. Each time an image is requested, it counts towards your Fast Data Transfer and Edge Request usage for your billing cycle.

See Pricing for more information, and read more about caching behavior in the Next.js documentation.

When you use the component in common frameworks and deploy your project on Vercel, Image Optimization automatically adjusts your images for different device screen sizes. The prop you provided in your code is dynamically replaced with an optimized image URL. For example:

The Image Optimization API has the following query parameters:

The allowed values of those query parameters are determined by the framework you are using, such as for Next.js.

If you are not using a framework that comes with an component or you are building your own framework, refer to the Build Output API to see how the build output from a framework can configure the Image Optimization API.

To switch to the transformation images-based pricing plan:

For more information on what to do next, we recommend the following articles:

---

## Vite on Vercel

**URL:** https://vercel.com/docs/frameworks/frontend/vite

**Contents:**
- Vite on Vercel
- Getting started
- Deploy a new Vite project with a template
- Using Vite community plugins
- Environment Variables
- Vercel Functions
- Server-Side Rendering (SSR)
- Using Vite to make SPAs
- More benefits
- More resources

Vite is an opinionated build tool that aims to provide a faster and leaner development experience for modern web projects. Vite provides a dev server with rich feature enhancements such as pre-bundling NPM dependencies and hot module replacement, and a build command that bundles your code and outputs optimized static assets for production.

These features make Vite more desirable than out-of-the-box CLIs when building larger projects with frameworks for many developers.

Vite powers popular frameworks like SvelteKit, and is often used in large projects built with Vue, Svelte, React, Preact, and more.

To get started with Vite on Vercel:

Get started in minutes

Vue-powered Static Site Generator

Vite/Vue.js site that can be deployed to Vercel

Vercel deployments can integrate with your git provider to generate preview URLs for each pull request you make to your Vite project.

Although Vite offers modern features like SSR and Vercel functions out of the box, implementing those features can sometimes require complex configuration steps. Because of this, many Vite users prefer to use popular community plugins.

Vite's plugins are based on Rollup's plugin interface, giving Vite users access to many tools from the Rollup ecosystem as well as the Vite-specific ecosystem.

We recommend using Vite plugins to configure your project when possible.

is a popular community Vite plugin that implements the Build Output API spec. It enables your Vite apps to use the following Vercel features:

When using the Vercel CLI, set the port as an environment variable. To allow Vite to access this, include the environment variable in your file:

is another popular community Vite plugin that implements the Build Output API spec. It enables your Vite apps to do the following:

Vercel provides a set of System Environment Variables that our platform automatically populates. For example, the variable exposes the Git provider that triggered your project's deployment on Vercel.

These environment variables will be available to your project automatically, and you can enable or disable them in your project settings on Vercel. See our Environment Variables docs to learn how.

To access Vercel's System Environment Variables in Vite during the build process, prefix the variable name with . For example, will return , , or depending on which environment the app is running in.

The following example demonstrates a Vite config file that sets as a global constant available throughout the app:

If you want to read environment variables from a file, additional configuration is required. See the Vite config docs to learn more.

To summarize, the benefits of using System Environment Variables with Vite on Vercel include:

Learn more about System Environment Variables

Vercel Functions scale up and down their resource consumption based on traffic demands. This scaling prevents them from failing during peak hours, but keeps them from running up high costs during periods of low activity.

If your project uses a Vite community plugin, such as , you should follow that plugin's documentation for using Vercel Functions.

If you're using a framework built on Vite, check that framework's official documentation or our dedicated framework docs. Some frameworks built on Vite, such as SvelteKit, support Functions natively. We recommend using that framework's method for implementing Functions.

If you're not using a framework or plugin that supports Vercel Functions, you can still use them in your project by creating routes in an directory at the root of your project.

The following example demonstrates a basic Vercel Function defined in an directory:

To summarize, Vercel Functions on Vercel:

Learn more about Vercel Functions

Server-Side Rendering (SSR) allows you to render pages dynamically on the server. This is useful for pages where the rendered data needs to be unique on every request. For example, checking authentication or looking at the location of an incoming request.

Vite exposes a low-level API for implementing SSR, but in most cases, we recommend using a Vite community plugin.

See the SSR section of Vite's plugin repo for a more comprehensive list of SSR plugins.

To summarize, SSR with Vite on Vercel:

If your Vite app is configured to deploy as a Single Page Application (SPA), deep linking won't work out of the box.

To enable deep linking in SPA Vite apps, create a file at the root of your project, and add the following code:

If is set to in your project's , do not include the file extension in the source or destination path. For example, would be

Deploying your app in Multi-Page App mode is recommended for production builds.

Learn more about Mutli-Page App mode in the Vite docs.

See our Frameworks documentation page to learn about the benefits available to all frameworks when you deploy on Vercel.

Learn more about deploying Vite projects on Vercel with the following resources:

---

## Next.js on Vercel

**URL:** https://vercel.com/docs/frameworks/full-stack/nextjs

**Contents:**
- Next.js on Vercel
- Getting started
- Deploy a new Next.js project with a template
- Incremental Static Regeneration
- Server-Side Rendering (SSR)
- Streaming
    - Streaming with and
- Partial Prerendering
- Image Optimization
- Font Optimization

Next.js is a fullstack React framework for the web, maintained by Vercel.

While Next.js works when self-hosting, deploying to Vercel is zero-configuration and provides additional enhancements for scalability, availability, and performance globally.

To get started with Next.js on Vercel:

Get started in minutes

Next.js App Router Playground

Examples of many Next.js App Router features.

Image Gallery Starter

An image gallery built on Next.js and Cloudinary.

Get started with Next.js and React in seconds.

Vercel deployments can integrate with your git provider to generate preview URLs for each pull request you make to your Next.js project.

Incremental Static Regeneration (ISR) allows you to create or update content without redeploying your site. ISR has three main benefits for developers: better performance, improved security, and faster build times.

When self-hosting, (ISR) is limited to a single region workload. Statically generated pages are not distributed closer to visitors by default, without additional configuration or vendoring of a CDN. By default, self-hosted ISR does not persist generated pages to durable storage. Instead, these files are located in the Next.js cache (which expires).

To summarize, using ISR with Next.js on Vercel:

Learn more about Incremental Static Regeneration (ISR)

Server-Side Rendering (SSR) allows you to render pages dynamically on the server. This is useful for pages where the rendered data needs to be unique on every request. For example, checking authentication or looking at the location of an incoming request.

On Vercel, you can server-render Next.js applications through Vercel Functions.

To summarize, SSR with Next.js on Vercel:

Vercel supports streaming in Next.js projects with any of the following:

Streaming data allows you to fetch information in chunks rather than all at once, speeding up Function responses. You can use streams to improve your app's user experience and prevent your functions from failing when fetching large files.

In the Next.js App Router, you can use the file convention or a component to show an instant loading state from the server while the content of a route segment loads.

The file provides a way to show a loading state for a whole route or route-segment, instead of just particular sections of a page. This file affects all its child elements, including layouts and pages. It continues to display its contents until the data fetching process in the route segment completes.

The following example demonstrates a basic file:

Learn more about loading in the Next.js docs.

The component, introduced in React 18, enables you to display a fallback until components nested within it have finished loading. Using is more granular than showing a loading state for an entire route, and is useful when only sections of your UI need a loading state.

You can specify a component to show during the loading state with the prop on the component as shown below:

To summarize, using Streaming with Next.js on Vercel:

Learn more about Streaming with Vercel Functions.

Partial Prerendering as an experimental feature. It is currently not suitable for production environments.

Partial Prerendering (PPR) is an experimental feature in Next.js that allows the static portions of a page to be pre-generated and served from the cache, while the dynamic portions are streamed in a single HTTP request.

When a user visits a route:

This approach is useful for pages like dashboards, where unique, per-request data coexists with static elements such as sidebars or layouts. This is different from how your application behaves today, where entire routes are either fully static or dynamic.

See the Partial Prerendering docs to learn more.

Image Optimization helps you achieve faster page loads by reducing the size of images and using modern image formats.

When deploying to Vercel, images are automatically optimized on demand, keeping your build times fast while improving your page load performance and Core Web Vitals.

When self-hosting, Image Optimization uses the default Next.js server for optimization. This server manages the rendering of pages and serving of static files.

To use Image Optimization with Next.js on Vercel, import the component into the component you'd like to add an image to, as shown in the following example:

To summarize, using Image Optimization with Next.js on Vercel:

Learn more about Image Optimization

enables built-in automatic self-hosting for any font file. This means you can optimally load web fonts with zero layout shift, thanks to the underlying CSS property.

This also allows you to use all Google Fonts with performance and privacy in mind. CSS and font files are downloaded at build time and self-hosted with the rest of your static files. No requests are sent to Google by the browser.

To summarize, using Font Optimization with Next.js on Vercel:

Learn more about Font Optimization

Dynamic social card images (using the Open Graph protocol) allow you to create a unique image for every page of your site. This is useful when sharing links on the web through social platforms or through text message.

The Vercel OG image generation library allows you generate fast, dynamic social card images using Next.js API Routes.

The following example demonstrates using OG image generation in both the Next.js Pages and App Router:

To see your generated image, run in your terminal and visit the route in your browser (most likely ).

To summarize, the benefits of using Vercel OG with Next.js include:

Learn more about OG Image Generation

Middleware is code that executes before a request is processed. Because Middleware runs before the cache, it's an effective way of providing personalization to statically generated content.

When deploying middleware with Next.js on Vercel, you get access to built-in helpers that expose each request's geolocation information. You also get access to the and objects, which enable rewrites, continuing the middleware chain, and more.

See the Middleware API docs for more information.

To summarize, Middleware with Next.js on Vercel:

Learn more about Middleware

Draft Mode enables you to view draft content from your Headless CMS immediately, while still statically generating pages in production.

See our Draft Mode docs to learn how to use it with Next.js.

When self-hosting, every request using Draft Mode hits the Next.js server, potentially incurring extra load or cost. Further, by spoofing the cookie, malicious users could attempt to gain access to your underlying Next.js server.

Deployments on Vercel automatically secure Draft Mode behind the same authentication used for Preview Comments. In order to enable or disable Draft Mode, the viewer must be logged in as a member of the Team. Once enabled, Vercel's CDN will bypass the ISR cache automatically and invoke the underlying Vercel Function.

You and your team members can toggle Draft Mode in the Vercel Toolbar in production, localhost, and Preview Deployments. When you do so, the toolbar will become purple to indicate Draft Mode is active.

Users outside your Vercel team cannot toggle Draft Mode.

To summarize, the benefits of using Draft Mode with Next.js on Vercel include:

Learn more about Draft Mode

Vercel's Web Analytics features enable you to visualize and monitor your application's performance over time. The Analytics tab in your project's dashboard offers detailed insights into your website's visitors, with metrics like top pages, top referrers, and user demographics.

To use Web Analytics, navigate to the Analytics tab of your project dashboard on Vercel and select Enable in the modal that appears.

To track visitors and page views, we recommend first installing our package by running the terminal command below in the root directory of your Next.js project:

Then, follow the instructions below to add the component to your app either using the directory or the directory.

To summarize, Web Analytics with Next.js on Vercel:

Learn more about Web Analytics

You can see data about your project's Core Web Vitals performance in your dashboard on Vercel. Doing so will allow you to track your web application's loading speed, responsiveness, and visual stability so you can improve the overall user experience.

On Vercel, you can track your Next.js app's Core Web Vitals in your project's dashboard.

Next.js uses Google's library to measure the Web Vitals metrics available in .

To summarize, tracking Web Vitals with Next.js on Vercel:

Learn more about Speed Insights

Vercel has partnered with popular service providers, such as MongoDB and Sanity, to create integrations that make using those services with Next.js easier. There are many integrations across multiple categories, such as Commerce, Databases, and Logging.

To summarize, Integrations on Vercel:

Learn more about Integrations

See our Frameworks documentation page to learn about the benefits available to all frameworks when you deploy on Vercel.

Learn more about deploying Next.js projects on Vercel with the following resources:

---

## Nuxt on Vercel

**URL:** https://vercel.com/docs/frameworks/full-stack/nuxt

**Contents:**
- Nuxt on Vercel
- Getting started
- Deploy a new Nuxt project with a template
  - Choosing a build command
- Editing your Nuxt config
  - Using
- Vercel Functions
- Reading and writing files
- Middleware
  - Nuxt server middleware on Vercel

Nuxt is an open-source framework that streamlines the process of creating modern Vue apps. It offers server-side rendering, SEO features, automatic code splitting, prerendering, and more out of the box. It also has an extensive catalog of community-built modules, which allow you to integrate popular tools with your projects.

You can deploy Nuxt static and server-side rendered sites on Vercel with no configuration required.

To get started with Nuxt on Vercel:

Get started in minutes

Nuxt.js 3 Boilerplate

A Nuxt.js 3 app, bootstrapped with create-nuxt-app.

An AI chatbot template to build your own chatbot powered by Nuxt MDC and Vercel AI SDK.

A link-in-bio SaaS built with Nuxt.js, where the data lives in the URL – no database required.

Vercel deployments can integrate with your git provider to generate preview URLs for each pull request you make to your Nuxt project.

The following table outlines the differences between and on Vercel:

In general, is likely best for most use cases. Consider using to build fully static sites.

You can configure your Nuxt deployment by creating a Nuxt config file in your project's root directory. It can be a TypeScript, JavaScript, or MJS file, but the Nuxt team recommends using TypeScript. Using TypeScript will allow your editor to suggest the correct names for configuration options, which can help mitigate typos.

Your Nuxt config file should default export by default, which you can add an options object to.

The following is an example of a Nuxt config file with no options defined:

See the Nuxt Configuration Reference docs for a list of available options.

With the config option, you can:

At the moment, there is no way to configure route deployment options within your page components, but development of this feature is in progress.

The following is an example of a Nuxt config that:

To learn more about :

Vercel Functions enable developers to write functions that uses resources that scale up and down based on traffic demands. This prevents them from failing during peak hours, but keeps them from running up high costs during periods of low activity.

Nuxt deploys routes defined in , , and as one server-rendered Function by default. Nuxt Pages, APIs, and Middleware routes get bundled into a single Vercel Function.

The following is an example of a basic API Route in Nuxt:

You can test your API Routes with .

You can read and write server files with Nuxt on Vercel. One way to do this is by using Nitro with Vercel Functions and the Vercel KV driver. Use Nitro's server assets to include files in your project deployment. Assets within get included by default.

To access server assets, you can use Nitro's storage API:

To write files, mount KV storage with the Vercel KV driver:

Update your nuxt.config.ts file.

Use with the storage API.

See an example code repository.

Middleware is code that executes before a request gets processed. Because Middleware runs before the cache, it's an effective way of providing personalization to statically generated content.

Nuxt has two forms of Middleware:

In Nuxt, modules defined in will get deployed as server middleware. Server middleware should not have a return statement or send a response to the request.

Server middleware is best used to read data from or add data to a request's . Doing so allows you to handle authentication or check a request's params, headers, url, and more.

The following example demonstrates Middleware that:

You could then access that data in a page on the frontend with the hook. This hook is only available in routes deployed with SSR. If your page renders in the browser, will return .

The following example demonstrates a page fetching data with :

Nuxt's route middleware runs before navigating to a particular route. While server middleware runs in Nuxt's Nitro engine, route middleware runs in Vue.

Route middleware is best used when you want to do things that server middleware can't, such as redirecting users, or preventing them from navigating to a route.

The following example demonstrates route middleware that redirects users to a secret route:

By default, route middleware code will only run on pages that specify them. To do so, within the tag for a page, you must call the method, passing an object with set as an option.

The following example demonstrates a page that runs the above redirect middleware:

To make a middleware global, add the suffix before the file extension. The following is an example of a basic global middleware file:

See a detailed example of route middleware in Nuxt's Middleware example docs.

Middleware with Nuxt on Vercel enables you to:

Learn more about Middleware

Server-Side Rendering (SSR) allows you to render pages dynamically on the server. This is useful for pages where the rendered data needs to be unique on every request. For example, checking authentication or looking at the location of an incoming request.

Nuxt allows you to deploy your projects with a strategy called Universal Rendering. In concrete terms, this allows you to deploy your routes with SSR by default and opt specific routes out in your Nuxt config.

When you deploy your app with Universal Rendering, it renders on the server once, then your client-side JavaScript code gets interpreted in the browser again once the page loads.

On Vercel, Nuxt apps are server-rendered by default

SSR with Nuxt on Vercel:

If you deploy with , you can opt nuxt routes into client-side rendering using by setting as demonstrated below:

To deploy a fully static site on Vercel, build your project with .

Alternatively, you can statically generate some Nuxt routes at build time using the route rule in your nuxt.config.ts:

To verify that a route is prerendered at build time, check useNuxtApp().payload.prerenderedAt.

Incremental Static Regeneration (ISR) allows you to create or update content without redeploying your site. ISR has two main benefits for developers: better performance and faster build times.

To enable ISR in a Nuxt route, add a option to your nuxt.config.ts, as shown in the example below:

You should use the option rather than to enable ISR in a route. The option enables Nuxt to use Vercel's Cache.

using ISR with Nuxt on Vercel offers:

Learn more about ISR with Nuxt.

You can define redirects and response headers with Nuxt on Vercel in your nuxt.config.ts:

Image Optimization helps you achieve faster page loads by reducing the size of images and using modern image formats.

When deploying to Vercel, images are automatically optimized on demand, keeping your build times fast while improving your page load performance and Core Web Vitals.

To use Image Optimization with Nuxt on Vercel, follow the Image Optimization quickstart by selecting Nuxt from the dropdown.

Using Image Optimization with Nuxt on Vercel:

Learn more about Image Optimization

Dynamic social card images allow you to create a unique image for pages of your site. This is great for sharing links on the web through social platforms or text messages.

To generate dynamic social card images for Nuxt projects, you can use . It uses the main Nuxt/Nitro Server-side rendering(SSR) function.

The following example demonstrates using Open Graph (OG) image generation with :

To see your generated image, run your project and use Nuxt DevTools. Or you can visit the image at its URL .

Learn more about OG Image Generation with Nuxt.

The Nuxt team does not recommend deploying legacy versions of Nuxt (such as Nuxt 2) on Vercel, except as static sites. If your project uses a legacy version of Nuxt, you should either:

If you still want to use legacy Nuxt versions with Vercel, you should only do so by building a static site with . We do not recommend deploying legacy Nuxt projects with server-side rendering.

See our Frameworks documentation page to learn about the benefits available to all frameworks when you deploy on Vercel.

Learn more about deploying Nuxt projects on Vercel with the following resources:

---

## Express on Vercel

**URL:** https://vercel.com/docs/frameworks/backend/express

**Contents:**
- Express on Vercel
- Get started with Express on Vercel
  - Get started with Vercel CLI
- Exporting the Express application
  - Using a default export
  - Using a port listener
  - Local development
  - Deploying the application
- Serving static assets
- Vercel Functions

Express is a fast, unopinionated, minimalist web framework for Node.js. You can deploy an Express app to Vercel with zero configuration.

Express applications on Vercel benefit from:

You can quickly deploy an Express application to Vercel by creating an Express app or using an existing one:

Get started by initializing a new Express project using Vercel CLI init command:

This will clone the Express example repository in a directory called .

To run an Express application on Vercel, create a file that imports the package at any one of the following locations:

The file must also export the application as a default export of the module or use a port listener.

For example, use the following code that exports your Express app:

You may also run your application using the pattern that exposes the server on a port.

Use to run your application locally

To deploy, connect your Git repository or use Vercel CLI:

To serve static assets, place them in the directory. They will be served as a part of our CDN using default headers unless otherwise specified in .

will be ignored and will not serve static assets.

When you deploy an Express app to Vercel, your Express application becomes a single Vercel Function and uses Fluid compute by default. This means your Express app will automatically scale up and down based on traffic.

Additionally, all Vercel Functions limitations apply to the Express application, including:

Learn more about deploying Express projects on Vercel with the following resources:

---

## AI SDK

**URL:** https://vercel.com/docs/ai-sdk

**Contents:**
- AI SDK
- Generating text
- Generating structured data
- Using tools with the AI SDK
- Getting started with the AI SDK
- More resources

The AI SDK is the TypeScript toolkit designed to help developers build AI-powered applications with Next.js, Vue, Svelte, Node.js, and more. Integrating LLMs into applications is complicated and heavily dependent on the specific model provider you use.

The AI SDK abstracts away the differences between model providers, eliminates boilerplate code for building chatbots, and allows you to go beyond text output to generate rich, interactive components.

At the center of the AI SDK is AI SDK Core, which provides a unified API to call any LLM.

The following example shows how to generate text with the AI SDK using OpenAI's GPT-5:

The unified interface means that you can easily switch between providers by changing just two lines of code. For example, to use Anthropic's Claude Sonnet 3.7:

While text generation can be useful, you might want to generate structured JSON data. For example, you might want to extract information from text, classify data, or generate synthetic data. AI SDK Core provides two functions ( and ) to generate structured data, allowing you to constrain model outputs to a specific schema.

The following example shows how to generate a type-safe recipe that conforms to a zod schema:

The AI SDK supports tool calling out of the box, allowing it to interact with external systems and perform discrete tasks. The following example shows how to use tool calling with the AI SDK:

The AI SDK is available as a package. To install it, run the following command:

See the AI SDK Getting Started guide for more information on how to get started with the AI SDK.

---

## Astro on Vercel

**URL:** https://vercel.com/docs/frameworks/frontend/astro

**Contents:**
- Astro on Vercel
- Get Started with Astro on Vercel
- Deploy a new Astro project with a template
- Using Vercel's features with Astro
  - Configuration options
- Server-Side Rendering
  - Static rendering
- Incremental Static Regeneration
- Vercel Functions
- Image Optimization

Astro is an all-in-one web framework that enables you to build performant static websites. People choose Astro when they want to build content-rich experiences with as little JavaScript as possible.

You can deploy a static Astro app to Vercel with zero configuration.

To get started with Astro on Vercel:

Get started in minutes

A minimal, responsive and SEO-friendly Astro blog theme.

Starter template for startups, marketing websites & blogs built with Astro and TailwindCSS.

The official 'Getting Started' template for Astro.

Vercel deployments can integrate with your git provider to generate preview URLs for each pull request you make to your Astro project.

To deploy a server-rendered Astro app, or a static Astro site with Vercel features like Web Analytics and Image Optimization, you must:

Add Astro's Vercel adapter to your project. There are two ways to do so:

Configure your project. In your astro.config.ts file, import either the or plugin, and set the output to or respectively:

Enable Vercel's features using Astro's configuration options. The following example astro.config.ts enables Web Analytics and adds a maximum duration to Vercel Function routes:

The following configuration options enable Vercel's features for Astro deployments.

For more details on the configuration options, see Astro's docs.

Using SSR, or on-demand rendering as Astro calls it, enables you to deploy your routes as Vercel functions on Vercel. This allows you to add dynamic elements to your app, such as user logins and personalized content.

You can enable SSR by adding the Vercel adapter to your project.

If your Astro project is statically rendered, you can opt individual routes. To do so:

Set your option to in your :

Add to your components:

SSR with Astro on Vercel:

Learn more about Astro SSR

Statically rendered, or pre-rendered, Astro apps can be deployed to Vercel with zero configuration. To enable Vercel features like Image Optimization or Web Analytics, see Using Vercel's features with Astro.

You can opt individual routes into static rendering with as shown below:

Statically rendered Astro sites on Vercel:

Learn more about Astro Static Rendering

Incremental Static Regeneration (ISR) allows you to create or update content without redeploying your site. ISR has two main benefits for developers: better performance and faster build times.

To enable ISR in Astro, you need to use the Vercel adapter and set to in your configuration in :

ISR function requests do not include search params, similar to requests in static mode.

Using ISR with Astro on Vercel offers:

Learn more about ISR with Astro.

Vercel Functions use resources that scale up and down based on traffic demands. This makes them reliable during peak hours, but low cost during slow periods.

When you enable SSR with Astro's Vercel adapter, all of your routes will be server-rendered as Vercel functions by default. Astro's Server Endpoints are the best way to define API routes with Astro on Vercel.

When defining an Endpoint, you must name each function after the HTTP method it represents. The following example defines basic HTTP methods in a Server Endpoint:

Astro removes the final file during the build process, so the name of the file should include the extension of the data you want serve (for example example.png.js will become /example.png).

Vercel Functions with Astro on Vercel:

Learn more about Vercel Functions

Image Optimization helps you achieve faster page loads by reducing the size of images and using modern image formats. When deploying to Vercel, images are automatically optimized on demand, keeping your build times fast while improving your page load performance and Core Web Vitals.

Image Optimization with Astro on Vercel is supported out of the box with Astro's component. See the Image Optimization quickstart to learn more.

Image Optimization with Astro on Vercel:

Learn more about Image Optimization

Middleware is a function that execute before a request is processed on a site, enabling you to modify the response. Because it runs before the cache, Middleware is an effective way to personalize statically generated content.

Astro middleware allows you to set and share information across your endpoints and pages with a middleware.ts file in your directory. The following example edits the global object, adding data which will be available in any file:

Astro middleware is not the same as Vercel's Routing Middleware

, which has to be placed at the root directory of your project, outside src.

You can then access the data you added to in any file, like so:

You can deploy Astro's middleware at the Edge, giving you access to data in the and , and enabling you to use Vercel's Routing Middleware helpers, such as or .

To use Astro's middleware at the Edge, set in your astro.config.ts file:

If you're using Vercel's Routing Middleware, you do not need to set in your astro.config.ts file.

See Astro's docs on the limitations and constraints for using middleware at the Edge, as well as their troubleshooting tips.

The object exposes data to your components, allowing you to dynamically modify your content with middleware. To make changes to in Astro's middleware at the edge:

Add a new middleware file next to your src/middleware.ts and name it src/vercel-edge-middleware.ts. This file name is required to make changes to . If you don't want to update , this step is not required

Return an object with the properties you want to add to . :

Astro's middleware, which should be in src/middleware.ts, is distinct from Vercel Routing Middleware, which should be a middleware.ts file at the root of your project.

Vercel recommends using framework-native solutions. You should use Astro's middleware over Vercel's Routing Middleware wherever possible.

If you still want to use Vercel's Routing Middleware, see the Quickstart to learn how.

Rewrites only work for static files with Astro. You must use Vercel's Routing Middleware for rewrites. You should not use to rewrite URL paths with astro projects; doing so produces inconsistent behavior, and is not officially supported.

In general, Vercel recommends using framework-native solutions, and Astro has built-in support for redirects. That said, you can also do redirects with Vercel's Routing Middleware.

You can do redirects on Astro with astro.config.ts the config option as shown below:

You can also return a redirect from a Server Endpoint using the utility:

You can redirect from within Astro components with :

Astro Middleware on Vercel:

Learn more about Routing Middleware

Vercel automatically caches static files at the edge after the first request, and stores them for up to 31 days on Vercel's CDN. Dynamic content can also be cached, and both dynamic and static caching behavior can be configured with Cache-Control headers.

The following Astro component will show a new time every 10 seconds. It does by setting a 10 second max age on the contents of the page, then serving stale content while new content is being rendered on the server when that age is exceeded.

Learn more about Cache Control options.

You can also control how the cache behaves on any CDNs you may be using outside of Vercel's CDN with CDN Cache-Control Headers.

The following example tells downstream CDNs to cache the content for 60 seconds, and Vercel's CDN to cache it for 3600 seconds:

Learn more about CDN Cache-Control headers.

Vercel Speed Insights provides you with a detailed view of your website's performance metrics, facilitating informed decisions for its optimization. By enabling Speed Insights, you gain access to the Speed Insights dashboard, which offers in-depth information about scores and individual metrics without the need for code modifications or leaving the dashboard.

To enable Speed Insights with Astro, see the Speed Insights quickstart.

To summarize, using Speed Insights with Astro on Vercel:

Learn more about Speed Insights

See our Frameworks documentation page to learn about the benefits available to all frameworks when you deploy on Vercel.

Learn more about deploying Astro projects on Vercel with the following resources:

---

## FastAPI on Vercel

**URL:** https://vercel.com/docs/frameworks/backend/fastapi

**Contents:**
- FastAPI on Vercel
- Get started with FastAPI on Vercel
  - Get started with Vercel CLI
- Exporting the FastAPI application
  - Build command
  - Local development
  - Deploying the application
- Serving static assets
- Startup and shutdown
- Vercel Functions

FastAPI is a modern, high-performance, web framework for building APIs with Python based on standard Python type hints. You can deploy a FastAPI app to Vercel with zero configuration.

You can quickly deploy a FastAPI application to Vercel by creating a FastAPI app or using an existing one:

Get started by initializing a new FastAPI project using Vercel CLI init command:

This will clone the FastAPI example repository in a directory called .

To run a FastAPI application on Vercel, define an instance that initializes at any of the following entrypoints:

You can also define an application script in to point to your FastAPI app in a different module:

This script tells Vercel to look for a instance named in .

The property in defines the Build Command for FastAPI deployments. It runs after dependencies are installed and before your application is deployed.

Use to run your application locally.

To deploy, connect your Git repository or use Vercel CLI:

To serve static assets, place them in the directory. They will be served as a part of our CDN using default headers unless otherwise specified in .

You can use FastAPI lifespan events to manage startup and shutdown logic, such as initializing and closing database connections.

Cleanup logic during shutdown is limited to a maximum of 500ms after receiving the SIGTERM signal. Logs printed during the shutdown step will not appear in the Vercel dashboard.

When you deploy a FastAPI app to Vercel, the application becomes a single Vercel Function and uses Fluid compute by default. This means your FastAPI app will automatically scale up and down based on traffic.

All Vercel Functions limitations apply to FastAPI applications, including:

Learn more about deploying FastAPI projects on Vercel with the following resources:

---

## Elysia on Vercel

**URL:** https://vercel.com/docs/frameworks/backend/elysia

**Contents:**
- Elysia on Vercel
- Get started with Elysia on Vercel
- Entrypoint detection
  - Using a default export
  - Using a port listener
- Local development
- Using Node.js
- Using the Bun runtime
- Middleware
  - Elysia Plugins and Lifecycle Hooks

Elysia is an ergonomic web framework for building backend servers with Bun. Designed with simplicity and type-safety in mind, Elysia offers a familiar API with extensive support for TypeScript and is optimized for Bun.

You can deploy an Elysia app to Vercel with zero configuration.

Elysia applications on Vercel benefit from:

Get started by initializing a new Elysia project using Vercel CLI init command:

This will clone the Elysia example repository in a directory called .

To deploy, connect your Git repository or use Vercel CLI:

To run an Elysia application on Vercel, create a file that imports the package at any one of the following locations:

The file must also export the application as a default export of the module or use a port listener.

For example, use the following code that exports your Elysia app:

Running your application using is currently not supported. For now, prefer .

To run your Elysia application locally, you can use Vercel CLI:

Ensure is set to in your file:

To use the Bun runtime on Vercel, configure the runtime in :

For more information, visit the Bun runtime on Vercel documentation.

In Elysia, you can use plugins and lifecycle hooks to run code before and after request handling. This is commonly used for logging, auth, or request processing:

In Vercel, Routing Middleware executes before a request is processed by your application. Use it for rewrites, redirects, headers, or personalization, and combine it with Elysia's own lifecycle hooks as needed.

When you deploy an Elysia app to Vercel, your server endpoints automatically run as Vercel Functions and use Fluid compute by default.

---

## Frontends on Vercel

**URL:** https://vercel.com/docs/frameworks/frontend

**Contents:**
- Frontends on Vercel
  - Angular
  - Astro
  - Brunch
  - React
  - Docusaurus (v1)
  - Docusaurus (v2+)
  - Dojo
  - Eleventy
  - Ember.js

The following frontend frameworks are supported with zero-configuration.

Angular is a TypeScript-based cross-platform framework from Google.

Astro is a new kind of static site builder for the modern web. Powerful developer experience meets lightweight output.

Brunch is a fast and simple webapp build tool with seamless incremental compilation for rapid development.

Create React App allows you to get going with React in no time.

Docusaurus makes it easy to maintain Open Source documentation websites.

Docusaurus makes it easy to maintain Open Source documentation websites.

Dojo is a modern progressive, TypeScript first framework.

11ty is a simpler static site generator written in JavaScript, created to be an alternative to Jekyll.

Ember.js helps webapp developers be more productive out of the box.

The fastest way to create an HTML app

Gatsby helps developers build blazing fast websites and apps with React.

Gridsome is a Vue.js-powered framework for building websites & apps that are fast by default.

Hexo is a fast, simple & powerful blog framework powered by Node.js.

Hugo is the world’s fastest framework for building websites, written in Go.

React framework for headless commerce

Ionic Angular allows you to build mobile PWAs with Angular and the Ionic Framework.

Ionic React allows you to build mobile PWAs with React and the Ionic Framework.

Jekyll makes it super easy to transform your plain text into static websites and blogs.

Middleman is a static site generator that uses all the shortcuts and tools in modern web development.

Parcel is a zero configuration build tool for the web that scales to projects of any size and complexity.

Polymer is an open-source webapps library from Google, for building using Web Components.

Preact is a fast 3kB alternative to React with the same modern API.

Declarative routing for React

Saber is a framework for building static sites in Vue.js that supports data from any source.

The structured content platform.

The structured content platform.

Scully is a static site generator for Angular.

Simple and performant reactivity for building user interfaces.

Simple and performant reactivity for building user interfaces.

Stencil is a powerful toolchain for building Progressive Web Apps and Design Systems.

Frontend workshop for UI development

UmiJS is an extensible enterprise-level React application framework.

Vite is a new breed of frontend build tool that significantly improves the frontend development experience.

VitePress is VuePress' little brother, built on top of Vite.

Vue.js is a versatile JavaScript framework that is as approachable as it is performant.

Vue-powered Static Site Generator

Everything you need to make a static site engine in one binary.

The following table shows which features are supported by each framework on Vercel. The framework list is not exhaustive, but a representation of the most popular frameworks deployed on Vercel.

We're committed to having support for all Vercel features across frameworks, and continue to work with framework authors on adding support. This table is continually updated over time.

---

## Full-stack frameworks on Vercel

**URL:** https://vercel.com/docs/frameworks/full-stack

**Contents:**
- Full-stack frameworks on Vercel
  - Next.js
  - Nuxt
  - RedwoodJS
  - Remix
  - SvelteKit
  - TanStack Start
- Frameworks infrastructure support matrix

The following full-stack frameworks are supported with zero-configuration.

Next.js makes you productive with React instantly — whether you want to build static or dynamic sites.

Nuxt is the open source framework that makes full-stack development with Vue.js intuitive.

RedwoodJS is a full-stack framework for the Jamstack.

Build Better Websites

SvelteKit is a framework for building web applications of all sizes.

Full-stack Framework powered by TanStack Router for React and Solid.

The following table shows which features are supported by each framework on Vercel. The framework list is not exhaustive, but a representation of the most popular frameworks deployed on Vercel.

We're committed to having support for all Vercel features across frameworks, and continue to work with framework authors on adding support. This table is continually updated over time.

---

## Fastify on Vercel

**URL:** https://vercel.com/docs/frameworks/backend/fastify

**Contents:**
- Fastify on Vercel
- Get started with Fastify on Vercel
- Fastify entrypoint detection
  - Local development
  - Deploying the application
- Vercel Functions
- Limitations
- More resources

Fastify is a web framework highly focused on providing the best developer experience with the least overhead and a powerful plugin architecture. You can deploy a Fastify app to Vercel with zero configuration using Vercel Functions.

Fastify applications on Vercel benefit from:

You can quickly deploy a Fastify application to Vercel by creating a Fastify app or using an existing one:

To allow Vercel to deploy your Fastify application and process web requests, your server entrypoint file should be named one of the following:

For example, use the following code as an entrypoint:

Use to run your application locally

To deploy, connect your Git repository or use Vercel CLI:

When you deploy a Fastify app to Vercel, your Fastify application becomes a single Vercel Function and uses Fluid compute by default. This means your Fastify app will automatically scale up and down based on traffic.

All Vercel Functions limitations apply to the Fastify application, including the size of the application being limited to 250MB.

Learn more about deploying Fastify projects on Vercel with the following resources:

---

## Frameworks on Vercel

**URL:** https://vercel.com/docs/frameworks

**Contents:**
- Frameworks on Vercel
- Deploy a Template
- Frameworks infrastructure support matrix
- Build Output API
- More resources

Vercel has first-class support for a wide range of the most popular frameworks. You can build and deploy using frontend, backend, and full-stack frameworks ranging from SvelteKit to Nitro, often without any upfront configuration.

Learn how to get started with Vercel or clone one of our example repos to your favorite git provider and deploy it on Vercel using one of the templates below:

Get started in minutes

Get started with Next.js and React in seconds.

SvelteKit Boilerplate

A SvelteKit app including nested routes, layouts, and page endpoints.

Deploying an API on Vercel with Nitro.

Vercel deployments can integrate with your git provider to generate preview URLs for each pull request you make to your project.

Deploying on Vercel with one of our supported frameworks gives you access to many features, such as:

The following table shows which features are supported by each framework on Vercel. The framework list represents the most popular frameworks deployed on Vercel.

The Build Output API is a file-system-based specification for a directory structure that produces a Vercel deployment. It is primarily targeted at framework authors who want to integrate their frameworks with Vercel's platform features. By implementing this directory structure as the output of their build command, framework authors can utilize all Vercel platform features, such as Vercel Functions, Routing, and Caching.

If you are not using a framework, you can still use these features by manually creating and populating the directory according to this specification. Complete examples of Build Output API directories can be found in vercel/examples, and you can read our blog post on using the Build Output API to build your own framework with Vercel.

Learn more about deploying your preferred framework on Vercel with the following resources:

---

## Supported Frameworks on Vercel

**URL:** https://vercel.com/docs/frameworks/more-frameworks

**Contents:**
- Supported Frameworks on Vercel
- Frameworks infrastructure support matrix
- All frameworks
  - Angular
  - Astro
  - Brunch
  - React
  - Docusaurus (v1)
  - Docusaurus (v2+)
  - Dojo

The following table shows which features are supported by each framework on Vercel. The framework list is not exhaustive, but a representation of the most popular frameworks deployed on Vercel.

We're committed to having support for all Vercel features across frameworks, and continue to work with framework authors on adding support. This table is continually updated over time.

The frameworks listed below can be deployed to Vercel with minimal configuration. See our docs on framework presets to learn more about configuration.

Angular is a TypeScript-based cross-platform framework from Google.

Astro is a new kind of static site builder for the modern web. Powerful developer experience meets lightweight output.

Brunch is a fast and simple webapp build tool with seamless incremental compilation for rapid development.

Create React App allows you to get going with React in no time.

Docusaurus makes it easy to maintain Open Source documentation websites.

Docusaurus makes it easy to maintain Open Source documentation websites.

Dojo is a modern progressive, TypeScript first framework.

11ty is a simpler static site generator written in JavaScript, created to be an alternative to Jekyll.

Ergonomic framework for humans

Ember.js helps webapp developers be more productive out of the box.

Fast, unopinionated, minimalist web framework for Node.js

FastAPI framework, high performance, easy to learn, fast to code, ready for production

The fastest way to create an HTML app

Fast and low overhead web framework, for Node.js

The Python micro web framework

Gatsby helps developers build blazing fast websites and apps with React.

Gridsome is a Vue.js-powered framework for building websites & apps that are fast by default.

Universal, Tiny, and Fast Servers

Hexo is a fast, simple & powerful blog framework powered by Node.js.

Web framework built on Web Standards

Hugo is the world’s fastest framework for building websites, written in Go.

React framework for headless commerce

Ionic Angular allows you to build mobile PWAs with Angular and the Ionic Framework.

Ionic React allows you to build mobile PWAs with React and the Ionic Framework.

Jekyll makes it super easy to transform your plain text into static websites and blogs.

Middleman is a static site generator that uses all the shortcuts and tools in modern web development.

Framework for building efficient, scalable Node.js server-side applications

Next.js makes you productive with React instantly — whether you want to build static or dynamic sites.

Nitro is a next generation server toolkit.

Nuxt is the open source framework that makes full-stack development with Vue.js intuitive.

Parcel is a zero configuration build tool for the web that scales to projects of any size and complexity.

Polymer is an open-source webapps library from Google, for building using Web Components.

Preact is a fast 3kB alternative to React with the same modern API.

Declarative routing for React

RedwoodJS is a full-stack framework for the Jamstack.

Build Better Websites

Saber is a framework for building static sites in Vue.js that supports data from any source.

The structured content platform.

The structured content platform.

Scully is a static site generator for Angular.

Simple and performant reactivity for building user interfaces.

Simple and performant reactivity for building user interfaces.

Stencil is a powerful toolchain for building Progressive Web Apps and Design Systems.

Frontend workshop for UI development

SvelteKit is a framework for building web applications of all sizes.

Full-stack Framework powered by TanStack Router for React and Solid.

UmiJS is an extensible enterprise-level React application framework.

Vite is a new breed of frontend build tool that significantly improves the frontend development experience.

VitePress is VuePress' little brother, built on top of Vite.

Vue.js is a versatile JavaScript framework that is as approachable as it is performant.

Vue-powered Static Site Generator

The MCP framework for building AI-powered tools

Everything you need to make a static site engine in one binary.

Learn more about deploying your preferred framework on Vercel with the following resources:

---
