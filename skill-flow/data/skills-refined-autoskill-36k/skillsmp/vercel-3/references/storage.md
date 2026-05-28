# Vercel - Storage

**Pages:** 4

---

## Vercel & OpenAI Integration

**URL:** https://vercel.com/docs/ai/openai

**Contents:**
- Vercel & OpenAI Integration
- Getting started
- Getting Your OpenAI API Key
  - Navigate to API Keys
  - Generate API Key
  - Set Environment Variable
- Building chat interfaces with the AI SDK
- Using OpenAI Functions with Vercel

Vercel integrates with OpenAI to enable developers to build fast, scalable, and secure AI applications.

You can integrate with any OpenAI model using the AI SDK, including the following OpenAI models:

To help you get started, we have built a variety of AI templates integrating OpenAI with Vercel.

Vercel Postgres pgvector Starter

A Next.js template that uses Vercel Postgres as the database, pgvector for vector similarity search + OpenAI's text embedding models.

A full-featured, hackable Next.js AI chatbot built by Vercel

Before you begin, ensure you have an OpenAI account. Once registered:

Log into your OpenAI Dashboard and view API keys.

Click on Create new secret key. Copy the generated API key securely.

Always keep your API keys confidential. Do not expose them in client-side code. Use Vercel Environment Variables for safe storage and do not commit these values to git.

Finally, add the environment variable in your project:

Integrating OpenAI into your Vercel project is seamless with the AI SDK.

Install the AI SDK in your project with your favorite package manager:

You can use the SDK to build AI applications with React (Next.js), Vue (Nuxt), Svelte (SvelteKit), and Node.js.

The AI SDK also has full support for OpenAI Functions (tool calling).

Learn more about using tools with the AI SDK.

---

## vercel blob

**URL:** https://vercel.com/docs/cli/blob

**Contents:**
- vercel blob
- Usage
  - list (ls)
  - put
  - del
  - copy (cp)
  - store add
  - store remove (rm)
  - store get
- Unique Options

The command is used to interact with Vercel Blob storage, providing functionality to upload, list, delete, and copy files, as well as manage Blob stores.

For more information about Vercel Blob, see the Vercel Blob documentation and Vercel Blob SDK reference.

The command supports the following operations:

For authentication, the CLI reads the value from your env file or you can use the option.

Using the vercel blob list command to list all files in the Blob store.

Using the vercel blob put command to upload a file to the Blob store.

Using the vercel blob del command to delete a file from the Blob store.

Using the vercel blob copy command to copy a file in the Blob store.

Using the vercel blob store add command to add a new Blob store. The default region is set to when not specified.

Using the vercel blob store remove command to remove a Blob store.

Using the vercel blob store get command to get a Blob store.

These are options that only apply to the command.

You can use the option to specify your Blob read-write token.

Using the vercel blob put command with the --rw-token option.

You can use the option to specify the number of results to return per page when using . The default value is and the maximum is .

Using the vercel blob list command with the --limit option.

You can use the option to specify the cursor from a previous page to start listing from.

Using the vercel blob list command with the --cursor option.

You can use the option to filter Blobs by a specific prefix.

Using the vercel blob list command with the --prefix option.

You can use the option to filter Blobs by either folded or expanded mode. The default is .

Using the vercel blob list command with the --mode option.

You can use the option to add a random suffix to the file name when using or .

Using the vercel blob put command with the --add-random-suffix option.

You can use the option to specify the pathname to upload the file to. The default is the filename.

Using the vercel blob put command with the --pathname option.

You can use the option to overwrite the content-type when using or . It will be inferred from the file extension if not provided.

Using the vercel blob put command with the --content-type option.

You can use the option to set the of the cache-control header directive when using or . The default is (30 days).

Using the vercel blob put command with the --cache-control-max-age option.

You can use the option to overwrite the file if it already exists when uploading. The default is .

Using the vercel blob put command with the --force option.

You can use the option to upload the file in multiple small chunks for performance and reliability. The default is .

Using the vercel blob put command with the --multipart option.

You can use the option to specify the region where your Blob store should be created. The default is . This option is only applicable when using the command.

Using the command with the option.

The following global options can be passed when using the vercel blob command:

For more information on global options and their usage, refer to the options section.

---

## Vercel Pinecone IntegrationConnectable Account

**URL:** https://vercel.com/docs/ai/pinecone

**Contents:**
- Vercel Pinecone IntegrationConnectable Account
  - What is a vector database?
- Use cases
- Getting started
  - Prerequisites
  - Add the provider to your project
    - Using the dashboard
- Deploy a template
- More resources

is a vector database service that handles the storage and search of complex data. With Pinecone, you can use machine-learning models for content recommendation systems, personalized search, image recognition, and more. The Vercel Pinecone integration allows you to deploy your models to Vercel and use them in your applications.

A vector database is a database that stores and searches for vectors. In this context, a vector represents a data point mathematically, often termed as an embedding.

An embedding is data that's converted to an array of numbers (a vector). The combination of the numbers that make up the vector form a multi-dimensional map used in comparison to other vectors to determine similarity.

Take the below example of two vectors, one for an image of a cat and one for an image of a dog. In the cat's vector, the first element is , and in the dog's vector . This similarity and difference in values illustrate how vector comparison works. The closer the values are to each other, the more similar the vectors are.

You can use the Vercel and Pinecone integration to power a variety of AI applications, including:

The Vercel integration can be accessed through the AI tab on your Vercel dashboard.

To follow this guide, you'll need the following:

You can deploy a template to Vercel that includes a pre-trained model and a sample application that uses the model:

Pinecone - Vercel AI SDK Starter

A Next.js starter chatbot using Vercel's AI SDK and implements the Retrieval-Augmented Generation (RAG) pattern with Pinecone

---

## Vercel Documentation

**URL:** https://vercel.com/docs

**Contents:**
- Vercel Documentation
- Get started with Vercel
- Quick references
- Build your applications
- Use Vercel's AI infrastructure
- Collaborate with your team
- Secure your applications
- Deploy and scale

Vercel is the AI Cloud for building and deploying modern web applications, from static sites to AI-powered agents.

You can build and host many different types of applications on Vercel, static sites with your favorite framework, multi-tenant applications, or microfrontends, to AI-powered agents.

You can also use the Vercel Marketplace to find and install integrations such as AI providers, databases, CMSs, analytics, storage, and more.

When you are ready to build, connect your Git repository to deploy on every push, with automatic preview environments for testing changes before production.

See the getting started guide for more information, or the incremental migration guide for a step-by-step guide to migrating your existing application to Vercel.

Use one or more of the following tools to build your application depending on your needs:

Add intelligence to your applications with Vercel's AI-first infrastructure:

Collaborate with your team using the following tools:

Secure your applications with the following tools:

Vercel handles infrastructure automatically based on your framework and code, and provides the following tools to help you deploy and scale your applications:

---
