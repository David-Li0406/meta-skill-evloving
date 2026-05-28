# Openai-Api - Getting Started

**Pages:** 4

---

## Getting started with datasets

**URL:** https://platform.openai.com/docs/guides/evaluation-getting-started

**Contents:**
- Getting started with datasets
- Create a dataset
  - Uploading a CSV
  - Using the visual data interface
- Build a prompt
- Generate and annotate outputs
  - What annotation does
  - Annotation starting points
  - Incorporate expert annotations
- Add graders

Evaluations (often called evals) test model outputs to ensure they meet your specified style and content criteria. Writing evals is an essential part of building reliable applications. Datasets, a feature of the OpenAI platform, provide a quick way to get started with evals and test prompts.

If you need advanced features such as evaluation against external models, want to interact with your eval runs via API, or want to run evaluations on a larger scale, consider using Evals instead.

First, create a dataset in the dashboard.

Your browser does not support the video tag.

We recommend using your dataset as a dynamic space, expanding your set of evaluation data over time. As you identify edge cases or blind spots that need monitoring, add them using the dashboard interface.

We have a simple CSV containing company names and actual values for their revenue from past quarters.

Your browser does not support the video tag.

The columns in your CSV are accessible to both your prompt and graders. For example, our CSV contains input columns (company) and ground truth columns (correct_revenue, correct_income) for our graders to use as reference.

After opening your dataset, you can manipulate your data in the Data tab. Click a cell to edit its contents. Add a row to add more data. You can also delete or duplicate rows in the overflow menu at the right edge of each row.

To save your changes, click Save button in the top right.

The tabs in the datasets dashboard let multiple prompts interact with the same data.

To add a new prompt, click Add prompt.

Datasets are designed to be used with your OpenAI prompts. If you’ve saved a prompt on the OpenAI platform, you’ll be able to select it from the dropdown and make changes in this interface. To save your prompt changes, click Save.

Our prompts use a versioning system so you can safely make updates. Clicking Save creates a new version of your prompt, which you can refer to or use anywhere in the OpenAI platform.

In the prompt panel, use the provided fields and settings to control the inference call:

In our example, we'll add the web search tool so our model call can pull financial data from the internet. In our variables list, we'll add company so our prompt can reference the company column in our dataset. And for the prompt, we’ll generate one by telling the model to “generate a financial report."

With your data and prompt set up, you’re ready to generate outputs. The model's output gives you a sense of how the model performs your task with the prompt and tools you provided. You'll then annotate the outputs so the model can improve its performance over time.

Your browser does not support the video tag.

In the top right, click Generate output.

You’ll see a new special output column in the dataset begin to populate with results. This column contains the results from running your prompt on each row in your dataset.

Once your generated outputs are ready, annotate them. Open the annotation view by clicking the output, rating, or output_feedback column.

Annotate as little or as much as you want. Datasets are designed to work with any degree and type of annotation, but the higher quality of information you can provide, the better your results will be.

Annotations are a key part of evaluating and improving model output. A good annotation:

You can choose to annotate as little or as much as you want. Datasets are designed to work with any degree and type of annotation, but the higher quality of information you can provide, the better your results will be. Additionally, if you’re not an expert on the contents of your dataset, we recommend that a subject matter expert performs the annotation — this is the most valuable way for their expertise to be incorporated into your optimization process. Explore our cookbook to learn more about what we have found to be most effective in using evals to improve our prompt resilience.

Here are a few types of annotations you can use to get started:

If you’re not an expert on the contents of your dataset, have a subject matter expert perform the annotation. This is the best way to incorporate expertise into the optimization process. Explore our cookbook to learn more.

While annotations are the most effective way to incorporate human feedback into your evaluation process, graders let you run evaluations at scale. Graders are automated assessments that can produce a variety of inputs depending on their type.

Your browser does not support the video tag.

After saving your dataset, graders persist as you make changes to your dataset and prompt, making them a great way to quickly assess whether a prompt or model parameter change leads to improvements, or whether adding edge cases reveals shortcomings in your prompt. The datasets dashboard supports multiple tabs for simultaneously tracking results from automated graders across multiple variants of a prompt.

Learn more about our graders.

Datasets are great for rapid iteration. When you're ready to track performance over time or run at scale, export your dataset to an Eval. Evals run asynchronously, support larger data volumes, and let you monitor performance across versions.

For more inspiration, visit the OpenAI Cookbook, which contains example code and links to third-party resources, or learn more about our evaluation tools:

Operate a flywheel of continuous improvement using evaluations.

Evaluate against external models, interact with evals via API, and more.

Use your dataset to automatically improve your prompts.

Build sophisticated graders to improve the effectiveness of your evals.

---

## Developer quickstart

**URL:** https://platform.openai.com/docs/quickstart

**Contents:**
- Developer quickstart
- Create and export an API key
- Install the OpenAI SDK and Run an API Call
- Add credits to keep building
- Analyze images and files
- Extend the model with tools
- Stream responses and build realtime apps
- Build agents

The OpenAI API provides a simple interface to state-of-the-art AI models for text generation, natural language processing, computer vision, and more. Get started by creating an API Key and running your first API call. Discover how to generate text, analyze images, build agents, and more.

Before you begin, create an API key in the dashboard, which you'll use to securely access the API. Store the key in a safe location, like a .zshrc file or another text file on your computer. Once you've generated an API key, export it as an environment variable in your terminal.

OpenAI SDKs are configured to automatically read your API key from the system environment.

To use the OpenAI API in server-side JavaScript environments like Node.js, Deno, or Bun, you can use the official OpenAI SDK for TypeScript and JavaScript. Get started by installing the SDK using npm or your preferred package manager:

With the OpenAI SDK installed, create a file called example.mjs and copy the example code into it:

Execute the code with node example.mjs (or the equivalent command for Deno or Bun). In a few moments, you should see the output of your API request.

Discover more SDK capabilities and options on the library's GitHub README.

To use the OpenAI API in Python, you can use the official OpenAI SDK for Python. Get started by installing the SDK using pip:

With the OpenAI SDK installed, create a file called example.py and copy the example code into it:

Execute the code with python example.py. In a few moments, you should see the output of your API request.

Discover more SDK capabilities and options on the library's GitHub README.

In collaboration with Microsoft, OpenAI provides an officially supported API client for C#. You can install it with the .NET CLI from NuGet.

A simple API request to the Responses API would look like this:

To learn more about using the OpenAI API in .NET, check out the GitHub repo linked below!

Discover more SDK capabilities and options on the library's GitHub README.

OpenAI provides an API helper for the Java programming language, currently in beta. You can include the Maven dependency using the following configuration:

A simple API request to Responses API would look like this:

To learn more about using the OpenAI API in Java, check out the GitHub repo linked below!

Discover more SDK capabilities and options on the library's GitHub README.

OpenAI provides an API helper for the Go programming language, currently in beta. You can import the library using the code below:

A simple API request to the Responses API would look like this:

To learn more about using the OpenAI API in Go, check out the GitHub repo linked below!

Discover more SDK capabilities and options on the library's GitHub README.

Start building with the Responses API.

Learn more about prompting, message roles, and building conversational apps.

Congrats on running a free test API request! Start building real applications with higher limits and use our models to generate text, audio, images, videos and more.

Build & test conversational prompts and embed them in your app.

Build, deploy, and optimize agent workflows.

Send image URLs, uploaded files, or PDF documents directly to the model to extract text, classify content, or detect visual elements.

Learn to use image inputs to the model and extract meaning from images.

Learn to use file inputs to the model and extract meaning from documents.

Give the model access to external data and functions by attaching tools. Use built-in tools like web search or file search, or define your own for calling APIs, running code, or integrating with third-party systems.

Learn about powerful built-in tools like web search and file search.

Learn to enable the model to call your own custom code.

Use server‑sent streaming events to show results as they’re generated, or the Realtime API for interactive voice and multimodal apps.

Use server-sent events to stream model responses to users fast.

Use WebRTC or WebSockets for super fast speech-to-speech AI apps.

Use the OpenAI platform to build agents capable of taking action—like controlling computers—on behalf of your users. Use the Agents SDK for Python or TypeScript to create orchestration logic on the backend.

Learn how to use the OpenAI platform to build powerful, capable AI agents.

**Examples:**

Example 1 (unknown):
```unknown
1
export OPENAI_API_KEY="your_api_key_here"
```

Example 2 (bash):
```bash
1
export OPENAI_API_KEY="your_api_key_here"
```

Example 3 (unknown):
```unknown
1
setx OPENAI_API_KEY "your_api_key_here"
```

Example 4 (bash):
```bash
1
setx OPENAI_API_KEY "your_api_key_here"
```

---

## Developer quickstart

**URL:** https://platform.openai.com/docs/quickstart?api-mode=responses

**Contents:**
- Developer quickstart
- Create and export an API key
- Install the OpenAI SDK and Run an API Call
- Add credits to keep building
- Analyze images and files
- Extend the model with tools
- Stream responses and build realtime apps
- Build agents

The OpenAI API provides a simple interface to state-of-the-art AI models for text generation, natural language processing, computer vision, and more. Get started by creating an API Key and running your first API call. Discover how to generate text, analyze images, build agents, and more.

Before you begin, create an API key in the dashboard, which you'll use to securely access the API. Store the key in a safe location, like a .zshrc file or another text file on your computer. Once you've generated an API key, export it as an environment variable in your terminal.

OpenAI SDKs are configured to automatically read your API key from the system environment.

To use the OpenAI API in server-side JavaScript environments like Node.js, Deno, or Bun, you can use the official OpenAI SDK for TypeScript and JavaScript. Get started by installing the SDK using npm or your preferred package manager:

With the OpenAI SDK installed, create a file called example.mjs and copy the example code into it:

Execute the code with node example.mjs (or the equivalent command for Deno or Bun). In a few moments, you should see the output of your API request.

Discover more SDK capabilities and options on the library's GitHub README.

To use the OpenAI API in Python, you can use the official OpenAI SDK for Python. Get started by installing the SDK using pip:

With the OpenAI SDK installed, create a file called example.py and copy the example code into it:

Execute the code with python example.py. In a few moments, you should see the output of your API request.

Discover more SDK capabilities and options on the library's GitHub README.

In collaboration with Microsoft, OpenAI provides an officially supported API client for C#. You can install it with the .NET CLI from NuGet.

A simple API request to the Responses API would look like this:

To learn more about using the OpenAI API in .NET, check out the GitHub repo linked below!

Discover more SDK capabilities and options on the library's GitHub README.

OpenAI provides an API helper for the Java programming language, currently in beta. You can include the Maven dependency using the following configuration:

A simple API request to Responses API would look like this:

To learn more about using the OpenAI API in Java, check out the GitHub repo linked below!

Discover more SDK capabilities and options on the library's GitHub README.

OpenAI provides an API helper for the Go programming language, currently in beta. You can import the library using the code below:

A simple API request to the Responses API would look like this:

To learn more about using the OpenAI API in Go, check out the GitHub repo linked below!

Discover more SDK capabilities and options on the library's GitHub README.

Start building with the Responses API.

Learn more about prompting, message roles, and building conversational apps.

Congrats on running a free test API request! Start building real applications with higher limits and use our models to generate text, audio, images, videos and more.

Build & test conversational prompts and embed them in your app.

Build, deploy, and optimize agent workflows.

Send image URLs, uploaded files, or PDF documents directly to the model to extract text, classify content, or detect visual elements.

Learn to use image inputs to the model and extract meaning from images.

Learn to use file inputs to the model and extract meaning from documents.

Give the model access to external data and functions by attaching tools. Use built-in tools like web search or file search, or define your own for calling APIs, running code, or integrating with third-party systems.

Learn about powerful built-in tools like web search and file search.

Learn to enable the model to call your own custom code.

Use server‑sent streaming events to show results as they’re generated, or the Realtime API for interactive voice and multimodal apps.

Use server-sent events to stream model responses to users fast.

Use WebRTC or WebSockets for super fast speech-to-speech AI apps.

Use the OpenAI platform to build agents capable of taking action—like controlling computers—on behalf of your users. Use the Agents SDK for Python or TypeScript to create orchestration logic on the backend.

Learn how to use the OpenAI platform to build powerful, capable AI agents.

**Examples:**

Example 1 (unknown):
```unknown
1
export OPENAI_API_KEY="your_api_key_here"
```

Example 2 (bash):
```bash
1
export OPENAI_API_KEY="your_api_key_here"
```

Example 3 (unknown):
```unknown
1
setx OPENAI_API_KEY "your_api_key_here"
```

Example 4 (bash):
```bash
1
setx OPENAI_API_KEY "your_api_key_here"
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/introduction

**Contents:**
- Introduction
- Authentication
- Debugging requests
  - Supplying your own request ID with X-Client-Request-Id
- Backward compatibility

This API reference describes the RESTful, streaming, and realtime APIs you can use to interact with the OpenAI platform. REST APIs are usable via HTTP in any environment that supports HTTP requests. Language-specific SDKs are listed on the libraries page.

The OpenAI API uses API keys for authentication. Create, manage, and learn more about API keys in your organization settings.

Remember that your API key is a secret! Do not share it with others or expose it in any client-side code (browsers, apps). API keys should be securely loaded from an environment variable or key management service on the server.

API keys should be provided via HTTP Bearer authentication.

If you belong to multiple organizations or access projects through a legacy user API key, pass a header to specify which organization and project to use for an API request:

Usage from these API requests counts as usage for the specified organization and project.Organization IDs can be found on your organization settings page. Project IDs can be found on your general settings page by selecting the specific project.

In addition to error codes returned from API responses, you can inspect HTTP response headers containing the unique ID of a particular API request or information about rate limiting applied to your requests. Below is an incomplete list of HTTP headers returned with API responses:

Rate limiting information

OpenAI recommends logging request IDs in production deployments for more efficient troubleshooting with our support team, should the need arise. Our official SDKs provide a property on top-level response objects containing the value of the x-request-id header.

In addition to the server-generated x-request-id, you can supply your own unique identifier for each request via the X-Client-Request-Id request header. This header is not added automatically; you must explicitly set it on the request.

When you include X-Client-Request-Id:

You control the ID format (for example, a UUID or your internal trace ID), but it must contain only ASCII characters and be no more than 512 characters long; otherwise, the request will fail with a 400 error. We strongly recommend making this value unique per request.

OpenAI will log this value in our internal logs for supported endpoints, including chat/completions, embeddings, responses, and more.

In cases like timeouts or network issues when you can’t get the X-Request-Id response header, you can share the X-Client-Request-Id value with our support team, and we can look up whether we received the request and when.

OpenAI is committed to providing stability to API users by avoiding breaking changes in major API versions whenever reasonably possible. This includes:

Model prompting behavior between snapshots is subject to change. Model outputs are by their nature variable, so expect changes in prompting and model behavior between snapshots. For example, if you moved from gpt-4o-2024-05-13 to gpt-4o-2024-08-06, the same system or user messages could function differently between versions. The best way to ensure consistent prompting behavior and model output is to use pinned model versions, and to implement evals for your applications.

Backwards-compatible API changes:

See the changelog for a list of backwards-compatible changes and rare breaking changes.

**Examples:**

Example 1 (unknown):
```unknown
Authorization: Bearer OPENAI_API_KEY
```

Example 2 (bash):
```bash
Authorization: Bearer OPENAI_API_KEY
```

Example 3 (unknown):
```unknown
1
2
3
4
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Organization: $ORGANIZATION_ID" \
  -H "OpenAI-Project: $PROJECT_ID"
```

Example 4 (bash):
```bash
1
2
3
4
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Organization: $ORGANIZATION_ID" \
  -H "OpenAI-Project: $PROJECT_ID"
```

---
