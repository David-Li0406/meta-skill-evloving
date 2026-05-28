# Gemini-Api - Models

**Pages:** 77

---

## Troubleshooting guide

**URL:** https://ai.google.dev/gemini-api/docs/troubleshooting

**Contents:**
- Troubleshooting guide
- Gemini API backend service error codes
- Check your API calls for model parameter errors
- Check if you have the right model
- Higher latency or token usage with 2.5 models
- Safety issues
- Recitation issue
- Repetitive tokens issue
- Blocked or non-working API keys
  - Understand why keys are blocked

Use this guide to help you diagnose and resolve common issues that arise when you call the Gemini API. You may encounter issues from either the Gemini API backend service or the client SDKs. Our client SDKs are open sourced in the following repositories:

If you encounter API key issues, verify that you have set up your API key correctly per the API key setup guide.

The following table lists common backend error codes you may encounter, along with explanations for their causes and troubleshooting steps:

Verify that your model parameters are within the following values:

In addition to checking parameter values, make sure you're using the correct API version (e.g., /v1 or /v1beta) and model that supports the features you need. For example, if a feature is in Beta release, it will only be available in the /v1beta API version.

Verify that you are using a supported model listed on our models page.

If you're observing higher latency or token usage with the 2.5 Flash and Pro models, this can be because they come with thinking is enabled by default in order to enhance quality. If you are prioritizing speed or need to minimize costs, you can adjust or disable thinking.

Refer to thinking page for guidance and sample code.

If you see a prompt was blocked because of a safety setting in your API call, review the prompt with respect to the filters you set in the API call.

If you see BlockedReason.OTHER, the query or response may violate the terms of service or be otherwise unsupported.

If you see the model stops generating output due to the RECITATION reason, this means the model output may resemble certain data. To fix this, try to make prompt / context as unique as possible and use a higher temperature.

If you see repeated output tokens, try the following suggestions to help reduce or eliminate them.

Add instructions in your prompt to give the model specific guidelines for generating Markdown tables. Provide examples that follow those guidelines. You can also try adjusting the temperature. For generating code or very structured output like Markdown tables, high temperature have shown to work better (>= 0.8).

The following is an example set of guidelines you can add to your prompt to prevent this issue:

This section describes how to check whether your Gemini API key is blocked and what to do about it.

We have identified a vulnerability where some API keys may have been publicly exposed. To protect your data and prevent unauthorized access, we have proactively blocked these known leaked keys from accessing the Gemini API.

If your key is known to be leaked, you can no longer use that key with the Gemini API. You can use Google AI Studio to see if any of your API keys are blocked from calling the Gemini API and generate new keys. You may also see the following error returned when attempting to use these keys:

You should generate new API keys for your Gemini API integrations using Google AI Studio. We strongly recommend reviewing your API key management practices to ensure that your new keys are kept secure and are not publicly exposed.

Submit a billing support case. Our billing team is working on this, and we will communicate updates as soon as possible.

How is Google going to help secure my account from cost overrun and abuse if my API keys are leaked?

For higher quality model outputs, explore writing more structured prompts. The prompt engineering guide page introduces some basic concepts, strategies, and best practices to get you started.

Read through our Token guide to better understand how to count tokens and their limits.

Join the discussion on the Google AI developer forum if you have questions.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-10 UTC.

**Examples:**

Example 1 (unknown):
```unknown
# Markdown Table Format
          
          * Separator line: Markdown tables must include a separator line below
            the header row. The separator line must use only 3 hyphens per
            column, for example: |---|---|---|. Using more hypens like
            ----, -----, ------ can result in errors. Always
            use |:---|, |---:|, or |---| in these separator strings.

            For example:

            | Date | Description | Attendees |
            |---|---|---|
            | 2024-10-26 | Annual Conference | 500 |
            | 2025-01-15 | Q1 Planning Session | 25 |

          * Alignment: Do not align columns. Always use |---|.
            For three columns, use |---|---|---| as the separator line.
            For four columns use |---|---|---|---| and so on.

          * Conciseness: Keep cell content brief and to the point.

          * Never pad column headers or other cells with lots of spaces to
            match with width of other content. Only a single space on each side
            is needed. For example, always do "| column name |" instead of
            "| column name                |". Extra spaces are wasteful.
            A markdown renderer will automatically take care displaying
            the content in a visually appealing form.
```

Example 2 (unknown):
```unknown
FOR TABLE HEADINGS, IMMEDIATELY ADD ' |' AFTER THE TABLE HEADING.
```

Example 3 (unknown):
```unknown
In quoted strings, the only allowed escape sequences are \\, \n, and \". Instead of \u escapes, use UTF-8.
```

Example 4 (unknown):
```unknown
When thinking silently: ALWAYS start the thought with a brief
        (one sentence) recap of the current progress on the task. In
        particular, consider whether the task is already done.
```

---

## Build mode in Google AI Studio

**URL:** https://ai.google.dev/gemini-api/docs/aistudio-build-mode

**Contents:**
- Build mode in Google AI Studio
- Get started
- What is created?
- Continue building
  - Build in Google AI Studio
  - Develop externally
- Key features
- Deploy or archive your app
- Limitations
- What's Next?

This page describes how you can use the Build mode in Google AI Studio to quickly build (or vibe code) and deploy apps that test out the latest capabilities of Gemini like nano banana and the Live API.

Start vibe coding in Google AI Studio's Build mode. You can start building in a few ways:

Once you run the prompt, you'll see the necessary code and files get generated, with a live preview of your app appearing on the right-hand side.

When you run your prompt, AI Studio creates a web app. By default, it will create a React web app but you can choose to create an Angular app in the Settings menu. You can view the code that gets generated by selecting the Code tab in the right-hand preview pane.

The following are files to note:

Once Google AI Studio generates the initial code for your web application, you have two primary options for continuing your project: Build in AI Studio or Develop Externally.

You can continue refining and expanding your application directly within the Google AI Studio environment:

For more advanced workflows, you can export the code and work in your preferred environment:

Google AI Studio includes several features to make the building process intuitive and visual:

Once your application is ready, you can deploy it directly from AI Studio. Options for deployment include:

This section outlines important limitations when using Build mode in Google AI Studio.

API Key security and exposure

App visibility and sharing

Deployment outside AI Studio

Tool and feature support

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-18 UTC.

---

## Code execution

**URL:** https://ai.google.dev/gemini-api/docs/code-execution

**Contents:**
- Code execution
- Enable code execution
  - Python
  - JavaScript
  - Go
  - REST
- Code Execution with images (Gemini 3)
  - Enabling visual thinking
  - Python
  - JavaScript

The Gemini API provides a code execution tool that enables the model to generate and run Python code. The model can then learn iteratively from the code execution results until it arrives at a final output. You can use code execution to build applications that benefit from code-based reasoning. For example, you can use code execution to solve equations or process text. You can also use the libraries included in the code execution environment to perform more specialized tasks.

Gemini is only able to execute code in Python. You can still ask Gemini to generate code in another language, but the model can't use the code execution tool to run it.

To enable code execution, configure the code execution tool on the model. This allows the model to generate and run code.

The output might look something like the following, which has been formatted for readability:

This output combines several content parts that the model returns when using code execution:

The naming conventions for these parts vary by programming language.

The Gemini 3 Flash model can now write and execute Python code to actively manipulate and inspect images. This capability is called Visual Thinking.

Visual Thinking is officially supported in Gemini 3 Flash. You can activate this behavior by enabling both Code Execution as a tool and Thinking.

You can also use code execution as part of a chat.

Starting with Gemini 2.0 Flash, code execution supports file input and graph output. Using these input and output capabilities, you can upload CSV and text files, ask questions about the files, and have Matplotlib graphs generated as part of the response. The output files are returned as inline images in the response.

When using code execution I/O, you're charged for input tokens and output tokens:

When you're working with code execution I/O, be aware of the following technical details:

There's no additional charge for enabling code execution from the Gemini API. You'll be billed at the current rate of input and output tokens based on the Gemini model you're using.

Here are a few other things to know about billing for code execution:

The billing model is shown in the following diagram:

Code execution tool can be combined with Grounding with Google Search to power more complex use cases.

The code execution environment includes the following libraries:

You can't install your own libraries.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the sum of the first 50 prime numbers? "
    "Generate and run code for the calculation, and make sure you get all 50.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution)]
    ),
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    if part.executable_code is not None:
        print(part.executable_code.code)
    if part.code_execution_result is not None:
        print(part.code_execution_result.output)
```

Example 2 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the sum of the first 50 prime numbers? "
    "Generate and run code for the calculation, and make sure you get all 50.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution)]
    ),
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    if part.executable_code is not None:
        print(part.executable_code.code)
    if part.code_execution_result is not None:
        print(part.code_execution_result.output)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

let response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: [
    "What is the sum of the first 50 prime numbers? " +
      "Generate and run code for the calculation, and make sure you get all 50.",
  ],
  config: {
    tools: [{ codeExecution: {} }],
  },
});

const parts = response?.candidates?.[0]?.content?.parts || [];
parts.forEach((part) => {
  if (part.text) {
    console.log(part.text);
  }

  if (part.executableCode && part.executableCode.code) {
    console.log(part.executableCode.code);
  }

  if (part.codeExecutionResult && part.codeExecutionResult.output) {
    console.log(part.codeExecutionResult.output);
  }
});
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

let response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: [
    "What is the sum of the first 50 prime numbers? " +
      "Generate and run code for the calculation, and make sure you get all 50.",
  ],
  config: {
    tools: [{ codeExecution: {} }],
  },
});

const parts = response?.candidates?.[0]?.content?.parts || [];
parts.forEach((part) => {
  if (part.text) {
    console.log(part.text);
  }

  if (part.executableCode && part.executableCode.code) {
    console.log(part.executableCode.code);
  }

  if (part.codeExecutionResult && part.codeExecutionResult.output) {
    console.log(part.codeExecutionResult.output);
  }
});
```

---

## Batch API

**URL:** https://ai.google.dev/gemini-api/docs/batch-api

**Contents:**
- Batch API
- Creating a batch job
  - Inline requests
  - Python
  - JavaScript
  - REST
  - Input file
  - Python
  - JavaScript
  - REST

The Gemini Batch API is designed to process large volumes of requests asynchronously at 50% of the standard cost. The target turnaround time is 24 hours, but in majority of cases, it is much quicker.

Use Batch API for large-scale, non-urgent tasks such as data pre-processing or running evaluations where an immediate response is not required.

You have two ways to submit your requests in Batch API:

For a small number of requests, you can directly embed the GenerateContentRequest objects within your BatchGenerateContentRequest. The following example calls the BatchGenerateContent method with inline requests:

For larger sets of requests, prepare a JSON Lines (JSONL) file. Each line in this file must be a JSON object containing a user-defined key and a request object, where the request is a valid GenerateContentRequest object. The user-defined key is used in the response to indicate which output is the result of which request. For example, the request with the key defined as request-1 will have its response annotated with the same key name.

This file is uploaded using the File API. The maximum allowed file size for an input file is 2GB.

The following is an example of a JSONL file. You can save it in a file named my-batch-requests.json:

Similarly to inline requests, you can specify other parameters like system instructions, tools or other configurations in each request JSON.

You can upload this file using the File API as shown in the following example. If you are working with multimodal input, you can reference other uploaded files within your JSONL file.

The following example calls the BatchGenerateContent method with the input file uploaded using File API:

When you create a batch job, you will get a job name returned. Use this name for monitoring the job status as well as retrieving the results once the job completes.

The following is an example output that contains a job name:

You can use the Batch API to interact with the Embeddings model for higher throughput. To create an embeddings batch job with either inline requests or input files, use the batches.create_embeddings API and specify the embeddings model.

Read the Embeddings section in the Batch API cookbook for more examples.

You can include any request configurations you would use in a standard non-batch request. For example, you could specify the temperature, system instructions or even pass in other modalities. The following example shows an example inline request that contains a system instruction for one of the requests:

Similarly can specify tools to use for a request. The following example shows a request that enables the Google Search tool:

You can specify structured output as well. The following example shows how to specify for your batch requests.

The following shows an example output of this job:

Use the operation name obtained when creating the batch job to poll its status. The state field of the batch job will indicate its current status. A batch job can be in one of the following states:

You can poll the job status periodically to check for completion.

Once the job status indicates your batch job has succeeded, the results are available in the response field.

You can cancel an ongoing batch job using its name. When a job is canceled, it stops processing new requests.

You can delete an existing batch job using its name. When a job is deleted, it stops processing new requests and is removed from the list of batch jobs.

If you're using Gemini Nano Banana and need to generate a lot of images, you can use the Batch API to get higher rate limits in exchange for a turnaround of up to 24 hours.

You can either use inline requests for small batches of requests (under 20MB) or a JSONL input file for large batches (recommended for image generation):

Inline requests Input file

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-04 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

# A list of dictionaries, where each is a GenerateContentRequest
inline_requests = [
    {
        'contents': [{
            'parts': [{'text': 'Tell me a one-sentence joke.'}],
            'role': 'user'
        }]
    },
    {
        'contents': [{
            'parts': [{'text': 'Why is the sky blue?'}],
            'role': 'user'
        }]
    }
]

inline_batch_job = client.batches.create(
    model="models/gemini-2.5-flash",
    src=inline_requests,
    config={
        'display_name': "inlined-requests-job-1",
    },
)

print(f"Created batch job: {inline_batch_job.name}")
```

Example 2 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

# A list of dictionaries, where each is a GenerateContentRequest
inline_requests = [
    {
        'contents': [{
            'parts': [{'text': 'Tell me a one-sentence joke.'}],
            'role': 'user'
        }]
    },
    {
        'contents': [{
            'parts': [{'text': 'Why is the sky blue?'}],
            'role': 'user'
        }]
    }
]

inline_batch_job = client.batches.create(
    model="models/gemini-2.5-flash",
    src=inline_requests,
    config={
        'display_name': "inlined-requests-job-1",
    },
)

print(f"Created batch job: {inline_batch_job.name}")
```

Example 3 (python):
```python
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({});

const inlinedRequests = [
    {
        contents: [{
            parts: [{text: 'Tell me a one-sentence joke.'}],
            role: 'user'
        }]
    },
    {
        contents: [{
            parts: [{'text': 'Why is the sky blue?'}],
            role: 'user'
        }]
    }
]

const response = await ai.batches.create({
    model: 'gemini-2.5-flash',
    src: inlinedRequests,
    config: {
        displayName: 'inlined-requests-job-1',
    }
});

console.log(response);
```

Example 4 (python):
```python
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({});

const inlinedRequests = [
    {
        contents: [{
            parts: [{text: 'Tell me a one-sentence joke.'}],
            role: 'user'
        }]
    },
    {
        contents: [{
            parts: [{'text': 'Why is the sky blue?'}],
            role: 'user'
        }]
    }
]

const response = await ai.batches.create({
    model: 'gemini-2.5-flash',
    src: inlinedRequests,
    config: {
        displayName: 'inlined-requests-job-1',
    }
});

console.log(response);
```

---

## Gemini thinking

**URL:** https://ai.google.dev/gemini-api/docs/thinking

**Contents:**
- Gemini thinking
- Generating content with thinking
  - Python
  - JavaScript
  - Go
  - REST
- Thought summaries
  - Python
  - JavaScript
  - Go

The Gemini 3 and 2.5 series models use an internal "thinking process" that significantly improves their reasoning and multi-step planning abilities, making them highly effective for complex tasks such as coding, advanced mathematics, and data analysis.

This guide shows you how to work with Gemini's thinking capabilities using the Gemini API.

Initiating a request with a thinking model is similar to any other content generation request. The key difference lies in specifying one of the models with thinking support in the model field, as demonstrated in the following text generation example:

Thought summaries are synthesized versions of the model's raw thoughts and offer insights into the model's internal reasoning process. Note that thinking levels and budgets apply to the model's raw thoughts and not to thought summaries.

You can enable thought summaries by setting includeThoughts to true in your request configuration. You can then access the summary by iterating through the response parameter's parts, and checking the thought boolean.

Here's an example demonstrating how to enable and retrieve thought summaries without streaming, which returns a single, final thought summary with the response:

And here is an example using thinking with streaming, which returns rolling, incremental summaries during generation:

Gemini models engage in dynamic thinking by default, automatically adjusting the amount of reasoning effort based on the complexity of the user's request. However, if you have specific latency constraints or require the model to engage in deeper reasoning than usual, you can optionally use parameters to control thinking behavior.

The thinkingLevel parameter, recommended for Gemini 3 models and onwards, lets you control reasoning behavior. You can set thinking level to "low" or "high" for Gemini 3 Pro, and "minimal", "low", "medium", and "high" for Gemini 3 Flash.

Gemini 3 Pro and Flash thinking levels:

Gemini 3 Flash thinking levels

In addition to the levels above, Gemini 3 Flash also supports the following thinking levels that are not currently supported by Gemini 3 Pro:

minimal: Matches the "no thinking" setting for most queries. The model may think very minimally for complex coding tasks. Minimizes latency for chat or high throughput applications.

You cannot disable thinking for Gemini 3 Pro. Gemini 3 Flash also does not support full thinking-off, but the minimal setting means the model likely will not think (though it still potentially can). If you don't specify a thinking level, Gemini will use the Gemini 3 models' default dynamic thinking level, "high".

Gemini 2.5 series models don't support thinkingLevel; use thinkingBudget instead.

The thinkingBudget parameter, introduced with the Gemini 2.5 series, guides the model on the specific number of thinking tokens to use for reasoning.

The following are thinkingBudget configuration details for each model type. You can disable thinking by setting thinkingBudget to 0. Setting the thinkingBudget to -1 turns on dynamic thinking, meaning the model will adjust the budget based on the complexity of the request.

Depending on the prompt, the model might overflow or underflow the token budget.

The Gemini API is stateless, so the model treats every API request independently and doesn't have access to thought context from previous turns in multi-turn interactions.

In order to enable maintaining thought context across multi-turn interactions, Gemini returns thought signatures, which are encrypted representations of the model's internal thought process.

Gemini 3 models may return thought signatures for all types of parts. We recommend you always pass all signatures back as received, but it's required for function calling signatures. Read the Thought Signatures page to learn more.

The Google GenAI SDK automatically handles the return of thought signatures for you. You only need to manage thought signatures manually if you're modifying conversation history or using the REST API.

Other usage limitations to consider with function calling include:

When thinking is turned on, response pricing is the sum of output tokens and thinking tokens. You can get the total number of generated thinking tokens from the thoughtsTokenCount field.

Thinking models generate full thoughts to improve the quality of the final response, and then output summaries to provide insight into the thought process. So, pricing is based on the full thought tokens the model needs to generate to create a summary, despite only the summary being output from the API.

You can learn more about tokens in the Token counting guide.

This section includes some guidance for using thinking models efficiently. As always, following our prompting guidance and best practices will get you the best results.

Review reasoning: When you're not getting your expected response from the thinking models, it can help to carefully analyze Gemini's thought summaries. You can see how it broke down the task and arrived at its conclusion, and use that information to correct towards the right results.

Provide Guidance in Reasoning: If you're hoping for a particularly lengthy output, you may want to provide guidance in your prompt to constrain the amount of thinking the model uses. This lets you reserve more of the token output for your response.

Thinking features are supported on all 3 and 2.5 series models. You can find all model capabilities on the model overview page.

Thinking models work with all of Gemini's tools and capabilities. This allows the models to interact with external systems, execute code, or access real-time information, incorporating the results into their reasoning and final response.

You can try examples of using tools with thinking models in the Thinking cookbook.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()
prompt = "Explain the concept of Occam's Razor and provide a simple, everyday example."
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=prompt
)

print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()
prompt = "Explain the concept of Occam's Razor and provide a simple, everyday example."
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=prompt
)

print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const prompt = "Explain the concept of Occam's Razor and provide a simple, everyday example.";

  const response = await ai.models.generateContent({
    model: "gemini-2.5-pro",
    contents: prompt,
  });

  console.log(response.text);
}

main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const prompt = "Explain the concept of Occam's Razor and provide a simple, everyday example.";

  const response = await ai.models.generateContent({
    model: "gemini-2.5-pro",
    contents: prompt,
  });

  console.log(response.text);
}

main();
```

---

## ReAct agent from scratch with Gemini 2.5 and LangGraph

**URL:** https://ai.google.dev/gemini-api/docs/langgraph-example

**Contents:**
- ReAct agent from scratch with Gemini 2.5 and LangGraph

LangGraph is a framework for building stateful LLM applications, making it a good choice for constructing ReAct (Reasoning and Acting) Agents.

ReAct agents combine LLM reasoning with action execution. They iteratively think, use tools, and act on observations to achieve user goals, dynamically adapting their approach. Introduced in "ReAct: Synergizing Reasoning and Acting in Language Models" (2023), this pattern tries to mirror human-like, flexible problem-solving over rigid workflows.

While LangGraph offers a prebuilt ReAct agent (create_react_agent), it shines when you need more control and customization for your ReAct implementations.

LangGraph models agents as graphs using three key components:

If you don't have an API Key yet, you can get one for free at the Google AI Studio.

Set your API key in the environment variable GEMINI_API_KEY.

To better understand how to implement a ReAct agent using LangGraph, let's walk through a practical example. You will create a simple agent whose goal is to use a tool to find the current weather for a specified location.

For this weather agent, its State will need to maintain the ongoing conversation history (as a list of messages) and a counter for the number of steps taken to further illustrate state management.

LangGraph provides a convenient helper, add_messages, for updating message lists in the state. It functions as a reducer, meaning it takes the current list and new messages, then returns a combined list. It smartly handles updates by message ID and defaults to an "append-only" behavior for new, unique messages.

Next, you define your weather tool.

Next, you initialize your model and bind the tools to the model.

The last step before you can run your agent is to define your nodes and edges. In this example, you have two nodes and one edge. - call_tool node that executes your tool method. LangGraph has a prebuilt node for this called ToolNode. - call_model node that uses the model_with_tools to call the model. - should_continue edge that decides whether to call the tool or the model.

The number of nodes and edges is not fixed. You can add as many nodes and edges as you want to your graph. For example, you could add a node for adding structured output or a self-verification/reflection node to check the model output before calling the tool or the model.

Now you have all the components to build your agent. Let's put them together.

You can visualize your graph using the draw_mermaid_png method.

Now let's run the agent.

You can now continue with your conversation and for example ask for the weather in another city or let it compare it.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

**Examples:**

Example 1 (unknown):
```unknown
pip install langgraph langchain-google-genai geopy requests
```

Example 2 (unknown):
```unknown
pip install langgraph langchain-google-genai geopy requests
```

Example 3 (python):
```python
import os

# Read your API key from the environment variable or set it manually
api_key = os.getenv("GEMINI_API_KEY")
```

Example 4 (python):
```python
import os

# Read your API key from the environment variable or set it manually
api_key = os.getenv("GEMINI_API_KEY")
```

---

## Migrate to the Google GenAI SDK

**URL:** https://ai.google.dev/gemini-api/docs/migrate

**Contents:**
- Migrate to the Google GenAI SDK
- Installation
  - Python
  - JavaScript
  - Go
  - Python
  - JavaScript
  - Go
- API access
  - Python

Starting with the Gemini 2.0 release in late 2024, we introduced a new set of libraries called the Google GenAI SDK. It offers an improved developer experience through an updated client architecture, and simplifies the transition between developer and enterprise workflows.

The Google GenAI SDK is now in General Availability (GA) across all supported platforms. If you're using one of our legacy libraries, we strongly recommend you to migrate.

This guide provides before-and-after examples of migrated code to help you get started.

The old SDK implicitly handled the API client behind the scenes using a variety of ad hoc methods. This made it hard to manage the client and credentials. Now, you interact through a central Client object. This Client object acts as a single entry point for various API services (e.g., models, chats, files, tunings), promoting consistency and simplifying credential and configuration management across different API calls.

Before (Less Centralized API Access)

The old SDK didn't explicitly use a top-level client object for most API calls. You would directly instantiate and interact with GenerativeModel objects.

While GoogleGenerativeAI was a central point for models and chat, other functionalities like file and cache management often required importing and instantiating entirely separate client classes.

The genai.NewClient function created a client, but generative model operations were typically called on a separate GenerativeModel instance obtained from this client. Other services might have been accessed via distinct packages or patterns.

After (Centralized Client Object)

Both legacy and new libraries authenticate using API keys. You can create your API key in Google AI Studio.

The old SDK handled the API client object implicitly.

Import the Google libraries:

With Google GenAI SDK, you create an API client first, which is used to call the API. The new SDK will pick up your API key from either one of the GEMINI_API_KEY or GOOGLE_API_KEY environment variables, if you don't pass one to the client.

Import the GenAI library:

Previously, there were no client objects, you accessed APIs directly through GenerativeModel objects.

The new Google GenAI SDK provides access to all the API methods through the Client object. Except for a few stateful special cases (chat and live-api sessions), these are all stateless functions. For utility and uniformity, objects returned are pydantic classes.

Many of the same convenience features exist in the new SDK. For example, PIL.Image objects are automatically converted.

For all methods in the new SDK, the required arguments are provided as keyword arguments. All optional inputs are provided in the config argument. Config arguments can be specified as either Python dictionaries or Config classes in the google.genai.types namespace. For utility and uniformity, all definitions within the types module are pydantic classes.

Generate a response with safety settings:

To use the new SDK with asyncio, there is a separate async implementation of every method under client.aio.

Start a chat and send a message to the model:

In the new SDK, automatic function calling is the default. Here, you disable it.

The old SDK only supports automatic function calling in chat. In the new SDK this is the default behavior in generate_content.

Code execution is a tool that allows the model to generate Python code, run it, and return the result.

GoogleSearch (Gemini>=2.0) and GoogleSearchRetrieval (Gemini < 2.0) are tools that allow the model to retrieve public web data for grounding, powered by Google.

Generate answers in JSON format.

By specifying a response_schema and setting response_mime_type="application/json" users can constrain the model to produce a JSON response following a given structure.

The new SDK uses pydantic classes to provide the schema (although you can pass a genai.types.Schema, or equivalent dict). When possible, the SDK will parse the returned JSON, and return the result in response.parsed. If you provided a pydantic class as the schema the SDK will convert that JSON to an instance of the class.

List uploaded files and get an uploaded file with a filename:

Context caching allows the user to pass the content to the model once, cache the input tokens, and then refer to the cached tokens in subsequent calls to lower the cost.

Count the number of tokens in a request.

Generate content embeddings.

Create and use a tuned model.

The new SDK simplifies tuning with client.tunings.tune, which launches the tuning job and polls until the job is complete.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-10 UTC.

**Examples:**

Example 1 (unknown):
```unknown
pip install -U -q "google-generativeai"
```

Example 2 (unknown):
```unknown
pip install -U -q "google-generativeai"
```

Example 3 (unknown):
```unknown
npm install @google/generative-ai
```

Example 4 (unknown):
```unknown
npm install @google/generative-ai
```

---

## Document understanding

**URL:** https://ai.google.dev/gemini-api/docs/document-processing

**Contents:**
- Document understanding
- Passing PDF data inline
  - Python
  - JavaScript
  - Go
  - REST
  - Python
  - JavaScript
  - Go
- Uploading PDFs using the Files API

Gemini models can process documents in PDF format, using native vision to understand entire document contexts. This goes beyond just text extraction, allowing Gemini to:

You can also pass non-PDF documents in the same way but Gemini will see them as normal text which will eliminate context like charts or formatting.

You can pass PDF data inline in the request to generateContent. This is best suited for smaller documents or temporary processing where you don't need to reference the file in subsequent requests. We recommend using the Files API for larger documents that you need to refer to in multi-turn interactions to improve request latency and reduce bandwidth usage.

The following example shows you how to fetch a PDF from a URL and convert it to bytes for processing:

You can also read a PDF from a local file for processing:

We recommend you use Files API for larger files or when you intend to reuse a document across multiple requests. This improves request latency and reduces bandwidth usage by decoupling the file upload from the model requests.

Use the File API to simplify uploading and processing large PDF files from URLs:

You can verify the API successfully stored the uploaded file and get its metadata by calling files.get. Only the name (and by extension, the uri) are unique.

The Gemini API is capable of processing multiple PDF documents (up to 1000 pages) in a single request, as long as the combined size of the documents and the text prompt stays within the model's context window.

Gemini supports PDF files up to 50MB or 1000 pages. This limit applies to both inline data and Files API uploads. Each document page is equivalent to 258 tokens.

While there are no specific limits to the number of pixels in a document besides the model's context window, larger pages are scaled down to a maximum resolution of 3072 x 3072 while preserving their original aspect ratio, while smaller pages are scaled up to 768 x 768 pixels. There is no cost reduction for pages at lower sizes, other than bandwidth, or performance improvement for pages at higher resolution.

Gemini 3 introduces granular control over multimodal vision processing with the media_resolution parameter. You can now set the resolution to low, medium, or high per individual media part. With this addition, the processing of PDF documents has been updated:

For more details about the media resolution parameter, see the Media resolution guide.

Technically, you can pass other MIME types for document understanding, like TXT, Markdown, HTML, XML, etc. However, document vision only meaningfully understands PDFs. Other types will be extracted as pure text, and the model won't be able to interpret what we see in the rendering of those files. Any file-type specifics like charts, diagrams, HTML tags, Markdown formatting, etc., will be lost.

To learn more, see the following resources:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-29 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types
import httpx

client = genai.Client()

doc_url = "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"

# Retrieve and encode the PDF byte
doc_data = httpx.get(doc_url).content

prompt = "Summarize this document"
response = client.models.generate_content(
  model="gemini-2.5-flash",
  contents=[
      types.Part.from_bytes(
        data=doc_data,
        mime_type='application/pdf',
      ),
      prompt])
print(response.text)
```

Example 2 (python):
```python
from google import genai
from google.genai import types
import httpx

client = genai.Client()

doc_url = "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"

# Retrieve and encode the PDF byte
doc_data = httpx.get(doc_url).content

prompt = "Summarize this document"
response = client.models.generate_content(
  model="gemini-2.5-flash",
  contents=[
      types.Part.from_bytes(
        data=doc_data,
        mime_type='application/pdf',
      ),
      prompt])
print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });

async function main() {
    const pdfResp = await fetch('https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf')
        .then((response) => response.arrayBuffer());

    const contents = [
        { text: "Summarize this document" },
        {
            inlineData: {
                mimeType: 'application/pdf',
                data: Buffer.from(pdfResp).toString("base64")
            }
        }
    ];

    const response = await ai.models.generateContent({
        model: "gemini-2.5-flash",
        contents: contents
    });
    console.log(response.text);
}

main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: "GEMINI_API_KEY" });

async function main() {
    const pdfResp = await fetch('https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf')
        .then((response) => response.arrayBuffer());

    const contents = [
        { text: "Summarize this document" },
        {
            inlineData: {
                mimeType: 'application/pdf',
                data: Buffer.from(pdfResp).toString("base64")
            }
        }
    ];

    const response = await ai.models.generateContent({
        model: "gemini-2.5-flash",
        contents: contents
    });
    console.log(response.text);
}

main();
```

---

## File Search

**URL:** https://ai.google.dev/gemini-api/docs/file-search

**Contents:**
- File Search
- Directly upload to File Search store
  - Python
  - JavaScript
- Importing files
  - Python
  - JavaScript
- Chunking configuration
  - Python
  - JavaScript

The Gemini API enables Retrieval Augmented Generation ("RAG") through the File Search tool. File Search imports, chunks, and indexes your data to enable fast retrieval of relevant information based on a provided prompt. This information is then used as context to the model, allowing the model to provide more accurate and relevant answers.

To make File Search simple and affordable for developers, we're making file storage and embedding generation at query time free of charge. You only pay for creating embeddings when you first index your files (at the applicable embedding model cost) and the normal Gemini model input / output tokens cost. This new billing paradigm makes the File Search Tool both easier and more cost-effective to build and scale with.

This examples shows how to directly upload a file to the file search store:

Check the API reference for uploadToFileSearchStore for more information.

Alternatively, you can upload an existing file and import it to your file search store:

Check the API reference for importFile for more information.

When you import a file into a File Search store, it's automatically broken down into chunks, embedded, indexed, and uploaded to your File Search store. If you need more control over the chunking strategy, you can specify a chunking_config setting to set a maximum number of tokens per chunk and maximum number of overlapping tokens.

To use your File Search store, pass it as a tool to the generateContent method, as shown in the Upload and Import examples.

File Search uses a technique called semantic search to find information relevant to the user prompt. Unlike standard keyword-based search, semantic search understands the meaning and context of your query.

When you import a file, it's converted into numerical representations called embeddings, which capture the semantic meaning of the text. These embeddings are stored in a specialized File Search database. When you make a query, it's also converted into an embedding. Then the system performs a File Search to find the most similar and relevant document chunks from the File Search store.

Here's a breakdown of the process for using the File Search uploadToFileSearchStore API:

Create a File Search store: A File Search store contains the processed data from your files. It's the persistent container for the embeddings that the semantic search will operate on.

Upload a file and import into a File Search store: Simultaneously upload a file and import the results into your File Search store. This creates a temporary File object, which is a reference to your raw document. That data is then chunked, converted into File Search embeddings, and indexed. The File object gets deleted after 48 hours, while the data imported into the File Search store will be stored indefinitely until you choose to delete it.

Query with File Search: Finally, you use the FileSearch tool in a generateContent call. In the tool configuration, you specify a FileSearchRetrievalResource, which points to the FileSearchStore you want to search. This tells the model to perform a semantic search on that specific File Search store to find relevant information to ground its response.

In this diagram, the dotted line from from Documents to Embedding model (using gemini-embedding-001) represents the uploadToFileSearchStore API (bypassing File storage). Otherwise, using the Files API to separately create and then import files moves the indexing process from Documents to File storage and then to Embedding model.

A File Search store is a container for your document embeddings. While raw files uploaded through the File API are deleted after 48 hours, the data imported into a File Search store is stored indefinitely until you manually delete it. You can create multiple File Search stores to organize your documents. The FileSearchStore API lets you create, list, get, and delete to manage your file search stores. File Search store names are globally scoped.

Here are some examples of how to manage your File Search stores:

The File Search Documents API reference for methods and fields related to managing documents in your file stores.

You can add custom metadata to your files to help filter them or provide additional context. Metadata is a set of key-value pairs.

This is useful when you have multiple documents in a File Search store and want to search only a subset of them.

Guidance on implementing list filter syntax for metadata_filter can be found at google.aip.dev/160

When you use File Search, the model's response may include citations that specify which parts of your uploaded documents were used to generate the answer. This helps with fact-checking and verification.

You can access citation information through the grounding_metadata attribute of the response.

The following models support File Search:

File Search supports a wide range of file formats, listed in the following sections.

The File Search API has the following limits to enforce service stability:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-29 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types
import time

client = genai.Client()

# File name will be visible in citations
file_search_store = client.file_search_stores.create(config={'display_name': 'your-fileSearchStore-name'})

operation = client.file_search_stores.upload_to_file_search_store(
  file='sample.txt',
  file_search_store_name=file_search_store.name,
  config={
      'display_name' : 'display-file-name',
  }
)

while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="""Can you tell me about [insert question]""",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[file_search_store.name]
                )
            )
        ]
    )
)

print(response.text)
```

Example 2 (python):
```python
from google import genai
from google.genai import types
import time

client = genai.Client()

# File name will be visible in citations
file_search_store = client.file_search_stores.create(config={'display_name': 'your-fileSearchStore-name'})

operation = client.file_search_stores.upload_to_file_search_store(
  file='sample.txt',
  file_search_store_name=file_search_store.name,
  config={
      'display_name' : 'display-file-name',
  }
)

while not operation.done:
    time.sleep(5)
    operation = client.operations.get(operation)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="""Can you tell me about [insert question]""",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[file_search_store.name]
                )
            )
        ]
    )
)

print(response.text)
```

Example 3 (javascript):
```javascript
const { GoogleGenAI } = require('@google/genai');

const ai = new GoogleGenAI({});

async function run() {
  // File name will be visible in citations
  const fileSearchStore = await ai.fileSearchStores.create({
    config: { displayName: 'your-fileSearchStore-name' }
  });

  let operation = await ai.fileSearchStores.uploadToFileSearchStore({
    file: 'file.txt',
    fileSearchStoreName: fileSearchStore.name,
    config: {
      displayName: 'file-name',
    }
  });

  while (!operation.done) {
    await new Promise(resolve => setTimeout(resolve, 5000));
    operation = await ai.operations.get({ operation });
  }

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "Can you tell me about [insert question]",
    config: {
      tools: [
        {
          fileSearch: {
            fileSearchStoreNames: [fileSearchStore.name]
          }
        }
      ]
    }
  });

  console.log(response.text);
}

run();
```

Example 4 (javascript):
```javascript
const { GoogleGenAI } = require('@google/genai');

const ai = new GoogleGenAI({});

async function run() {
  // File name will be visible in citations
  const fileSearchStore = await ai.fileSearchStores.create({
    config: { displayName: 'your-fileSearchStore-name' }
  });

  let operation = await ai.fileSearchStores.uploadToFileSearchStore({
    file: 'file.txt',
    fileSearchStoreName: fileSearchStore.name,
    config: {
      displayName: 'file-name',
    }
  });

  while (!operation.done) {
    await new Promise(resolve => setTimeout(resolve, 5000));
    operation = await ai.operations.get({ operation });
  }

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "Can you tell me about [insert question]",
    config: {
      tools: [
        {
          fileSearch: {
            fileSearchStoreNames: [fileSearchStore.name]
          }
        }
      ]
    }
  });

  console.log(response.text);
}

run();
```

---

## Logs and datasets

**URL:** https://ai.google.dev/gemini-api/docs/logs-datasets

**Contents:**
- Logs and datasets
- 1. Enable logging in Google AI Studio
- 2. View logs in AI Studio
- 3. Curate and share datasets
- Next steps & what to test
- Compatibility

This guide contains everything you need to get started with enabling logging for your existing Gemini API applications. In this guide you'll learn how to view logs from an existing or new application in the Google AI Studio dashboard to better understand model behavior and how users may be interacting with your applications. Use logging to observe, debug, and optionally share usage feedback with Google to help improve Gemini across developer use cases.*

All GenerateContent and StreamGenerateContent API calls are supported, including those made through OpenAI compatibility endpoints.

Before you begin, ensure you have a billing-enabled project that you own.

You can enable or disable logging for all projects or for specific projects, and change these preferences at any time through Google AI Studio.

Click on an entry for a full page view of the request and response pair. You can inspect the full prompt, the complete response from Gemini, and the context from the previous turn. Note that each project has a default storage limit of up to 1,000 logs, and logs not saved in datasets will expire after 55 days. If your project reaches its storage limit you will be promoted to delete logs.

Datasets can be helpful for a number of different use cases.

You can help drive progress in AI research, the Gemini API, and Google AI Studio by choosing to share your datasets as demonstration examples. This allows us to refine our models in diverse contexts and create AI systems that remain useful to developers across many fields and applications

Now that you have logging enabled, here are a few things to try:

Logging is not currently supported for the following:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-10-30 UTC.

---

## Rate limits

**URL:** https://ai.google.dev/gemini-api/docs/rate-limits

**Contents:**
- Rate limits
- How rate limits work
- Usage tiers
- Gemini API rate limits
- Batch API rate limits
  - Tier 1
  - Tier 2
  - Tier 3
- How to upgrade to the next tier
- Request a rate limit increase

Rate limits regulate the number of requests you can make to the Gemini API within a given timeframe. These limits help maintain fair usage, protect against abuse, and help maintain system performance for all users.

View your active rate limits in AI Studio

Rate limits are usually measured across three dimensions:

Your usage is evaluated against each limit, and exceeding any of them will trigger a rate limit error. For example, if your RPM limit is 20, making 21 requests within a minute will result in an error, even if you haven't exceeded your TPM or other limits.

Rate limits are applied per project, not per API key. Requests per day (RPD) quotas reset at midnight Pacific time.

Limits vary depending on the specific model being used, and some limits only apply to specific models. For example, Images per minute, or IPM, is only calculated for models capable of generating images (Imagen 3), but is conceptually similar to TPM. Other models might have a token per day limit (TPD).

Rate limits are more restricted for experimental and preview models.

Rate limits are tied to the project's usage tier. As your API usage and spending increase, you'll have an option to upgrade to a higher tier with increased rate limits.

The qualifications for Tiers 2 and 3 are based on the total cumulative spending on Google Cloud services (including, but not limited to, the Gemini API) for the billing account linked to your project.

When you request an upgrade, our automated abuse protection system performs additional checks. While meeting the stated qualification criteria is generally sufficient for approval, in rare cases an upgrade request may be denied based on other factors identified during the review process.

This system helps maintain the security and integrity of the Gemini API platform for all users.

Rate limits depend on a variety of factors (such as your quota tier) and can be viewed in Google AI Studio. As your tier and account status change over time, your rate limits will automatically be updated.

View your active rate limits in AI Studio

Specified rate limits are not guaranteed and actual capacity may vary.

Batch API requests are subject to their own rate limits, separate from the non-batch API calls.

The Gemini API uses Cloud Billing for all billing services. To transition from the Free tier to a paid tier, you must first enable Cloud Billing for your Google Cloud project.

Once your project meets the specified criteria, it becomes eligible for an upgrade to the next tier. To request an upgrade, follow these steps:

After a quick validation, the project will be upgraded to the next tier.

Each model variation has an associated rate limit (requests per minute, RPM). For details on those rate limits, see Gemini models.

Request paid tier rate limit increase

We offer no guarantees about increasing your rate limit, but we'll do our best to review your request.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

---

## Troubleshoot Google AI Studio

**URL:** https://ai.google.dev/gemini-api/docs/troubleshoot-ai-studio

**Contents:**
- Troubleshoot Google AI Studio
- Understand 403 Access Restricted errors
- Resolve No Content responses on Google AI Studio
- Check token usage and limits

This page provides suggestions for troubleshooting Google AI Studio if you encounter issues.

If you see a 403 Access Restricted error, you are using Google AI Studio in a way that does not follow the Terms of Service. One common reason is you are not located in a supported region.

A warning No Content message appears on Google AI Studio if the content is blocked for any reason. To see more details, hold the pointer over No Content and click warning Safety.

If the response was blocked due to safety settings and you considered the safety risks for your use case, you can modify the safety settings to influence the returned response.

If the response was blocked but not due to the safety settings, the query or response may violate the Terms of Service or be otherwise unsupported.

When you have a prompt open, the Text Preview button at the bottom of the screen shows the current tokens used for the content of your prompt and the maximum token count for the model being used.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

---

## LearnLM

**URL:** https://ai.google.dev/gemini-api/docs/learnlm

**Contents:**
- LearnLM
- Example system instructions
  - Test prep
  - Teach a concept
  - Releveling
  - Guide a student through a learning activity
  - Homework help
- What's next?
- Feedback

LearnLM is an experimental task-specific model that has been trained to align with learning science principles when following system instructions for teaching and learning use cases (for example, when giving the model a system instruction like "You are an expert tutor"). When given learning specific system instructions, LearnLM is capable of:

LearnLM is an experimental model available in AI Studio.

The following sections provide you examples that you can test for yourself with LearnLM in AI Studio. Each example provides:

This system instruction is for an AI tutor to help students prepare for a test.

Learning science principles:

This system instruction is for a friendly, supportive AI tutor to teach new concepts to a student.

Learning science principles:

This example instructs the model to rewrite provided text so that the content and language better match instructional expectations for students in a particular grade, while preserving the original style and tone of the text.

Learning science principles:

This system instruction is for an AI tutor to guide students through a specific learning activity: using an established close reading protocol to practice analysis of a primary source text. Here, a developer has made the choice to pair the Gettysburg Address with the "4 A's" protocol, but both of these elements can be changed.

Learning science principles:

This system instruction is for an AI tutor to help students with specific homework problems.

Alternatively, you can try uploading a photo of a homework problem.

Learning science principles:

Test LearnLM for yourself in AI Studio.

You can provide feedback on LearnLM using our feedback form.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

**Examples:**

Example 1 (unknown):
```unknown
You are a tutor helping a student prepare for a test. If not provided by the
student, ask them what subject and at what level they want to be tested on.
Then,

*   Generate practice questions. Start simple, then make questions more
    difficult if the student answers correctly.
*   Prompt the student to explain the reason for their answer choice. Do not
    debate the student.
*   **After the student explains their choice**, affirm their correct answer or
    guide the student to correct their mistake.
*   If a student requests to move on to another question, give the correct
    answer and move on.
*   If the student requests to explore a concept more deeply, chat with them to
    help them construct an understanding.
*   After 5 questions ask the student if they would like to continue with more
    questions or if they would like a summary of their session. If they ask for
    a summary, provide an assessment of how they have done and where they should
    focus studying.
```

Example 2 (unknown):
```unknown
You are a tutor helping a student prepare for a test. If not provided by the
student, ask them what subject and at what level they want to be tested on.
Then,

*   Generate practice questions. Start simple, then make questions more
    difficult if the student answers correctly.
*   Prompt the student to explain the reason for their answer choice. Do not
    debate the student.
*   **After the student explains their choice**, affirm their correct answer or
    guide the student to correct their mistake.
*   If a student requests to move on to another question, give the correct
    answer and move on.
*   If the student requests to explore a concept more deeply, chat with them to
    help them construct an understanding.
*   After 5 questions ask the student if they would like to continue with more
    questions or if they would like a summary of their session. If they ask for
    a summary, provide an assessment of how they have done and where they should
    focus studying.
```

Example 3 (unknown):
```unknown
Help me study for a high school biology test on ecosystems
```

Example 4 (unknown):
```unknown
Help me study for a high school biology test on ecosystems
```

---

## Customer Support Analysis with Gemini 2.5 Pro and CrewAI

**URL:** https://ai.google.dev/gemini-api/docs/crewai-example

**Contents:**
- Customer Support Analysis with Gemini 2.5 Pro and CrewAI
- Define components
  - Tools
  - Agents
  - Tasks
  - Crew
- Run the Crew

CrewAI is a framework for orchestrating autonomous AI agents that collaborate to achieve complex goals. It lets you define agents by specifying roles, goals, and backstories, and then define tasks for them.

This example demonstrates how to build a multi-agent system for analyzing customer support data to identify issues and propose process improvements using Gemini 2.5 Pro, generating a report intended to be read by a Chief Operating Officer (COO).

The guide will show you how to create a "crew" of AI agents that can do the following tasks:

You need a Gemini API key. If you don't already have one, you can get one in Google AI Studio.

Set your Gemini API key as an environment variable named GEMINI_API_KEY, then configure CrewAI to use the Gemini 2.5 Pro model.

CrewAI applications are built using Tools, Agents, Tasks, and the Crew itself. Each of these is explained in the following sections.

Tools are capabilities that agents can use to interact with the outside world or perform specific actions. Here, you define a placeholder tool to simulate fetching customer support data. In a real application, you would connect to a database, API or file system. For more information on tools, see the CrewAI tools guide.

Agents are the individual AI workers in your crew. Each agent has a specific role, goal, backstory, assigned llm, and optional tools. For more information on agents, see the CrewAI agents guide.

Tasks define the specific assignments for the agents. Each task has a description, expected_output, and is assigned to an agent. Tasks are run sequentially by default and include the context of the previous task. For more information on tasks, see the CrewAI tasks guide.

The Crew brings the agents and tasks together, defining the workflow process (such as "sequential").

Finally, kick off the crew execution with any necessary inputs.

The script will now execute. The Data Analyst will use the tool, the Process Optimizer will analyze the findings, and the Report Writer will compile the final report, which is then printed to the console. The verbose=True setting will show the detailed thought process and actions of each agent.

To learn more about CrewAI, check out the CrewAI introduction.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

**Examples:**

Example 1 (unknown):
```unknown
pip install "crewai[tools]"
```

Example 2 (unknown):
```unknown
pip install "crewai[tools]"
```

Example 3 (python):
```python
import os
from crewai import LLM

# Read your API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Use Gemini 2.5 Pro Experimental model
gemini_llm = LLM(
    model='gemini/gemini-2.5-pro',
    api_key=gemini_api_key,
    temperature=0.0  # Lower temperature for more consistent results.
)
```

Example 4 (python):
```python
import os
from crewai import LLM

# Read your API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Use Gemini 2.5 Pro Experimental model
gemini_llm = LLM(
    model='gemini/gemini-2.5-pro',
    api_key=gemini_api_key,
    temperature=0.0  # Lower temperature for more consistent results.
)
```

---

## Gemini models

**URL:** https://ai.google.dev/gemini-api/docs/models/gemini

**Contents:**
- Gemini models
- Gemini 3 Pro
  - Expand to learn more
    - Model details
  - Gemini 3 Pro Preview
  - Gemini 3 Pro Image Preview
- Gemini 3 Flash
  - Expand to learn more
    - Model details
  - Gemini 3 Flash Preview

OUR MOST INTELLIGENT MODEL

The best model in the world for multimodal understanding, and our most powerful agentic and vibe-coding model yet, delivering richer visuals and deeper interactivity, all built on a foundation of state-of-the-art reasoning.

Try in Google AI Studio

Text, Image, Video, Audio, and PDF

Grounding with Google Maps

Grounding with Google Maps

OUR MOST INTELLIGENT MODEL

Our most intelligent model built for speed, combining frontier intelligence with superior search and grounding.

Try in Google AI Studio

Text, Image, Video, Audio, and PDF

Grounding with Google Maps

Our best model in terms of price-performance, offering well-rounded capabilities. 2.5 Flash is best for large scale processing, low-latency, high volume tasks that require thinking, and agentic use cases.

Try in Google AI Studio

Text, images, video, audio

Grounding with Google Maps

Text, images, video, audio

Grounding with Google Maps

Grounding with Google Maps

Grounding with Google Maps

Grounding with Google Maps

Our fastest flash model optimized for cost-efficiency and high throughput.

Try in Google AI Studio

Text, image, video, audio, PDF

Grounding with Google Maps

Text, image, video, audio, PDF

Grounding with Google Maps

OUR ADVANCED THINKING MODEL

Our state-of-the-art thinking model, capable of reasoning over complex problems in code, math, and STEM, as well as analyzing large datasets, codebases, and documents using long context.

Try in Google AI Studio

Audio, images, video, text, and PDF

Grounding with Google Maps

Grounding with Google Maps

OUR SECOND GENERATION WORKHORSE MODEL

Our second generation workhorse model, with a 1 million token context window.

Gemini 2.0 Flash delivers next-gen features and improved capabilities, including superior speed, native tool use, and a 1M token context window.

Try in Google AI Studio

Audio, images, video, and text

Grounding with Google Maps

Audio, images, video, and text

Grounding with Google Maps

gemini-2.0-flash-preview-image-generation is not currently supported in a number of countries in Europe, Middle East & Africa

OUR SECOND GENERATION FAST MODEL

Our second generation small workhorse model, with a 1 million token context window.

A Gemini 2.0 Flash model optimized for cost efficiency and low latency.

Try in Google AI Studio

Audio, images, video, and text

Grounding with Google Maps

Gemini models are available in either stable, preview, latest, or experimental versions.

Points to a specific stable model. Stable models usually don't change. Most production apps should use a specific stable model.

For example: gemini-2.5-flash.

Points to a preview model which may be used for production. Preview models will typically have billing enabled, might come with more restrictive rate limits and will be deprecated with at least 2 weeks notice.

For example: gemini-2.5-flash-preview-09-2025.

Points to the latest release for a specific model variation. This can be a stable, preview or experimental release. This alias will get hot-swapped with every new release of a specific model variation. A 2-week notice will be provided through email before the version behind latest is changed.

For example: gemini-flash-latest.

Points to an experimental model which will typically be not be suitable for production use and come with more restrictive rate limits. We release experimental models to gather feedback and get our latest updates into the hands of developers quickly.

Experimental models are not stable and availability of model endpoints is subject to change.

For information about model deprecations, visit the Gemini deprecations page.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

---

## Media resolution

**URL:** https://ai.google.dev/gemini-api/docs/media-resolution

**Contents:**
- Media resolution
- Per-part media resolution (Gemini 3 only)
  - Python
  - Javascript
  - REST
- Global media resolution
  - Python
  - Javascript
  - REST
- Available resolution values

The media_resolution parameter controls how the Gemini API processes media inputs like images, videos, and PDF documents by determining the maximum number of tokens allocated for media inputs, allowing you to balance response quality against latency and cost. For different settings, default values and how they correspond to tokens, see the Token counts section.

You can configure media resolution in two ways:

Per part (Gemini 3 only)

Globally for an entire generateContent request (all multimodal models)

Gemini 3 allows you to set media resolution for individual media objects within your request, offering fine-grained optimisation of token usage. You can mix resolution levels in a single request. For example, using high resolution for a complex diagram and low resolution for a simple contextual image. This setting overrides any global configuration for a specific part. For default settings, see Token counts section.

You can set a default resolution for all media parts in a request using the GenerationConfig. This is supported by all multimodal models. If a request includes both global and per-part settings, the per-part setting takes precedence for that specific item.

The Gemini API defines the following levels for media resolution:

Note that MEDIA_RESOLUTION_HIGH provides the optimal performance for most use cases.

The exact number of tokens generated for each of these levels depends on both the media type (Image, Video, PDF) and the model version.

The tables below summarize the approximate token counts for each media_resolution value and media type per model family.

The following lists the recommended media resolution settings for each supported media type.

Always test and evaluate the impact of different resolution settings on your specific application to find the best trade-off between quality, latency, and cost.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

# The media_resolution parameter for parts is currently only available in the v1alpha API version. (experimental)
client = genai.Client(
  http_options={
      'api_version': 'v1alpha',
  }
)

# Replace with your image data
with open('path/to/image1.jpg', 'rb') as f:
    image_bytes_1 = f.read()

# Create parts with different resolutions
image_part_high = types.Part.from_bytes(
    data=image_bytes_1,
    mime_type='image/jpeg',
    media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH
)

model_name = 'gemini-3-pro-preview'

response = client.models.generate_content(
    model=model_name,
    contents=["Describe these images:", image_part_high]
)
print(response.text)
```

Example 2 (python):
```python
from google import genai
from google.genai import types

# The media_resolution parameter for parts is currently only available in the v1alpha API version. (experimental)
client = genai.Client(
  http_options={
      'api_version': 'v1alpha',
  }
)

# Replace with your image data
with open('path/to/image1.jpg', 'rb') as f:
    image_bytes_1 = f.read()

# Create parts with different resolutions
image_part_high = types.Part.from_bytes(
    data=image_bytes_1,
    mime_type='image/jpeg',
    media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH
)

model_name = 'gemini-3-pro-preview'

response = client.models.generate_content(
    model=model_name,
    contents=["Describe these images:", image_part_high]
)
print(response.text)
```

Example 3 (python):
```python
// Example: Setting per-part media resolution in JavaScript
import { GoogleGenAI, MediaResolution, Part } from '@google/genai';
import * as fs from 'fs';
import { Buffer } from 'buffer'; // Node.js

const ai = new GoogleGenAI({ httpOptions: { apiVersion: 'v1alpha' } });

// Helper function to convert local file to a Part object
function fileToGenerativePart(path, mimeType, mediaResolution) {
    return {
        inlineData: { data: Buffer.from(fs.readFileSync(path)).toString('base64'), mimeType },
        mediaResolution: { 'level': mediaResolution }
    };
}

async function run() {
    // Create parts with different resolutions
    const imagePartHigh = fileToGenerativePart('img.png', 'image/png', Part.MediaResolutionLevel.MEDIA_RESOLUTION_HIGH);
    const model_name = 'gemini-3-pro-preview';
    const response = await ai.models.generateContent({
        model: model_name,
        contents: ['Describe these images:', imagePartHigh]
        // Global config can still be set, but per-part settings will override
        // config: {
        //   mediaResolution: MediaResolution.MEDIA_RESOLUTION_MEDIUM
        // }
    });
    console.log(response.text);
}
run();
```

Example 4 (python):
```python
// Example: Setting per-part media resolution in JavaScript
import { GoogleGenAI, MediaResolution, Part } from '@google/genai';
import * as fs from 'fs';
import { Buffer } from 'buffer'; // Node.js

const ai = new GoogleGenAI({ httpOptions: { apiVersion: 'v1alpha' } });

// Helper function to convert local file to a Part object
function fileToGenerativePart(path, mimeType, mediaResolution) {
    return {
        inlineData: { data: Buffer.from(fs.readFileSync(path)).toString('base64'), mimeType },
        mediaResolution: { 'level': mediaResolution }
    };
}

async function run() {
    // Create parts with different resolutions
    const imagePartHigh = fileToGenerativePart('img.png', 'image/png', Part.MediaResolutionLevel.MEDIA_RESOLUTION_HIGH);
    const model_name = 'gemini-3-pro-preview';
    const response = await ai.models.generateContent({
        model: model_name,
        contents: ['Describe these images:', imagePartHigh]
        // Global config can still be set, but per-part settings will override
        // config: {
        //   mediaResolution: MediaResolution.MEDIA_RESOLUTION_MEDIUM
        // }
    });
    console.log(response.text);
}
run();
```

---

## Research Agent with Gemini 2.5 Pro and LlamaIndex

**URL:** https://ai.google.dev/gemini-api/docs/llama-index

**Contents:**
- Research Agent with Gemini 2.5 Pro and LlamaIndex
- Set up Gemini 2.5 Pro in LlamaIndex
- Build tools
- Build a multi-agent assistant
- Go further with custom workflows

LlamaIndex is a framework for building knowledge agents using LLMs connected to your data. This example shows you how to build a multi-agent workflow for a Research Agent. In LlamaIndex, Workflows are the building blocks of agent or multi-agent systems.

You need a Gemini API key. If you don't already have one, you can get one in Google AI Studio. First, install all required LlamaIndex libraries.LlamaIndex uses the google-genai package under the hood.

The engine of any LlamaIndex agent is an LLM that handles reasoning and text processing. This example uses Gemini 2.5 Pro. Make sure you set your API key as an environment variable.

Agents use tools to interact with the outside world, like searching the web or storing information. Tools in LlamaIndex can be regular Python functions, or imported from pre-existing ToolSpecs. Gemini comes with a built-in tool for using Google Search which is used here.

Now test the LLM instance with a query that requires search:

The Research Agent will use Python functions as tools. There are a lot of ways you could go about building a system to perform this task. In this example, you will use the following:

The Context class passes the state between agents/tools, and each agent will have access to the current state of the system.

To build a multi-agent system, you define the agents and their interactions. Your system will have three agents:

This example uses the AgentWorkflow class to create a multi-agent system that will execute these agents in order. Each agent takes a system_prompt that tells it what it should do, and suggests how to work with the other agents.

Optionally, you can help your multi-agent system by specifying which other agents it can talk to using can_handoff_to (if not, it will try to figure this out on its own).

The Agents are defined, now you can create the AgentWorkflow and run it.

During execution of the workflow, you can stream events, tool calls and updates to the console.

After the workflow is complete, you can print the final output of the report, as well as the final review state from then review agent.

The AgentWorkflow is a great way to get started with multi-agent systems. But what if you need more control? You can build a workflow from scratch. Here are some reasons why you might want to build your own workflow:

To learn more about LlamaIndex Workflows, see the LlamaIndex Workflows Documentation.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

**Examples:**

Example 1 (unknown):
```unknown
pip install llama-index llama-index-utils-workflow llama-index-llms-google-genai llama-index-tools-google
```

Example 2 (unknown):
```unknown
pip install llama-index llama-index-utils-workflow llama-index-llms-google-genai llama-index-tools-google
```

Example 3 (python):
```python
from llama_index.llms.google_genai import GoogleGenAI

llm = GoogleGenAI(model="gemini-2.5-pro")
```

Example 4 (python):
```python
from llama_index.llms.google_genai import GoogleGenAI

llm = GoogleGenAI(model="gemini-2.5-pro")
```

---

## Image understanding

**URL:** https://ai.google.dev/gemini-api/docs/image-understanding

**Contents:**
- Image understanding
- Passing images to Gemini
  - Passing inline image data
  - Python
  - JavaScript
  - Go
  - REST
  - Python
  - JavaScript
  - Go

Gemini models are built to be multimodal from the ground up, unlocking a wide range of image processing and computer vision tasks including but not limited to image captioning, classification, and visual question answering without having to train specialized ML models.

You can provide images as input to Gemini using two methods:

You can pass inline image data in the request to generateContent. You can provide image data as Base64 encoded strings or by reading local files directly (depending on the language).

The following example shows how to read an image from a local file and pass it to generateContent API for processing.

You can also fetch an image from a URL, convert it to bytes, and pass it to generateContent as shown in the following examples.

For large files or to be able to use the same image file repeatedly, use the Files API. The following code uploads an image file and then uses the file in a call to generateContent. See the Files API guide for more information and examples.

You can provide multiple images in a single prompt by including multiple image Part objects in the contents array. These can be a mix of inline data (local files or URLs) and File API references.

From Gemini 2.0 onwards, models are further trained to detect objects in an image and get their bounding box coordinates. The coordinates, relative to image dimensions, scale to [0, 1000]. You need to descale these coordinates based on your original image size.

For more examples, check following notebooks in the Gemini Cookbook:

Starting with Gemini 2.5, models not only detect items but also segment them and provide their contour masks.

The model predicts a JSON list, where each item represents a segmentation mask. Each item has a bounding box ("box_2d") in the format [y0, x0, y1, x1] with normalized coordinates between 0 and 1000, a label ("label") that identifies the object, and finally the segmentation mask inside the bounding box, as base64 encoded png that is a probability map with values between 0 and 255. The mask needs to be resized to match the bounding box dimensions, then binarized at your confidence threshold (127 for the midpoint).

Check the segmentation example in the cookbook guide for a more detailed example.

Gemini supports the following image format MIME types:

All Gemini model versions are multimodal and can be utilized in a wide range of image processing and computer vision tasks including but not limited to image captioning, visual question and answering, image classification, object detection and segmentation.

Gemini can reduce the need to use specialized ML models depending on your quality and performance requirements.

Some later model versions are specifically trained improve accuracy of specialized tasks in addition to generic capabilities:

Gemini 2.0 models are further trained to support enhanced object detection.

Gemini 2.5 models are further trained to support enhanced segmentation in addition to object detection.

Gemini 2.5 Pro/Flash, 2.0 Flash, 1.5 Pro, and 1.5 Flash support a maximum of 3,600 image files per request.

A rough formula for calculating the number of tiles is as follows:

For example, for an image of dimensions 960x540 would have a crop unit size of 360. Divide each dimension by 360 and the number of tile is 3 * 2 = 6.

Gemini 3 introduces granular control over multimodal vision processing with the media_resolution parameter. The media_resolution parameter determines the maximum number of tokens allocated per input image or video frame. Higher resolutions improve the model's ability to read fine text or identify small details, but increase token usage and latency.

For more details about the parameter and how it can impact token calculations, see the media resolution guide.

This guide shows you how to upload image files and generate text outputs from image inputs. To learn more, see the following resources:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-18 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
  from google.genai import types

  with open('path/to/small-sample.jpg', 'rb') as f:
      image_bytes = f.read()

  client = genai.Client()
  response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
      types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/jpeg',
      ),
      'Caption this image.'
    ]
  )

  print(response.text)
```

Example 2 (python):
```python
from google import genai
  from google.genai import types

  with open('path/to/small-sample.jpg', 'rb') as f:
      image_bytes = f.read()

  client = genai.Client()
  response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
      types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/jpeg',
      ),
      'Caption this image.'
    ]
  )

  print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});
const base64ImageFile = fs.readFileSync("path/to/small-sample.jpg", {
  encoding: "base64",
});

const contents = [
  {
    inlineData: {
      mimeType: "image/jpeg",
      data: base64ImageFile,
    },
  },
  { text: "Caption this image." },
];

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: contents,
});
console.log(response.text);
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});
const base64ImageFile = fs.readFileSync("path/to/small-sample.jpg", {
  encoding: "base64",
});

const contents = [
  {
    inlineData: {
      mimeType: "image/jpeg",
      data: base64ImageFile,
    },
  },
  { text: "Caption this image." },
];

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: contents,
});
console.log(response.text);
```

---

## Files API

**URL:** https://ai.google.dev/gemini-api/docs/prompting_with_media

**Contents:**
- Files API
- Upload a file
  - Python
  - JavaScript
  - Go
  - REST
- Get metadata for a file
  - Python
  - JavaScript
  - Go

Gemini can handle various types of input data, including text, images, and audio, at the same time.

This guide shows you how to work with media files using the Files API. The basic operations are the same for audio files, images, videos, documents, and other supported file types.

For file prompting guidance, check out the File prompt guide section.

You can use the Files API to upload a media file. Always use the Files API when the total request size (including the files, text prompt, system instructions, etc.) is larger than 20 MB.

The following code uploads a file and then uses the file in a call to generateContent.

You can verify that the API successfully stored the uploaded file and get its metadata by calling files.get.

The following code gets a list of all the files uploaded:

Files are automatically deleted after 48 hours. You can also manually delete an uploaded file:

You can use the Files API to upload and interact with media files. The Files API lets you store up to 20 GB of files per project, with a per-file maximum size of 2 GB. Files are stored for 48 hours. During that time, you can use the API to get metadata about the files, but you can't download the files. The Files API is available at no cost in all regions where the Gemini API is available.

This section provides guidance and best practices for using media files with prompts for the Gemini API.

Being able to use various types of data in your prompts gives you more flexibility in terms of what tasks you can tackle with the Gemini API. For example, you can send the model a photo of a delicious meal and ask it to write a short blog about the meal.

Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.

Meal prepping is a great way to save time and money, and it can also help you to eat healthier. This meal is a great example of a healthy and delicious meal that can be easily prepped ahead of time.

This meal features brown rice, roasted vegetables, and chicken teriyaki. The brown rice is a healthy and complex carbohydrate that will give you sustained energy. The roasted vegetables are a great way to get your daily dose of vitamins and minerals, and the chicken teriyaki is a delicious and protein-rich option.

This meal is also very easy to prepare. Simply cook the brown rice, roast the vegetables, and cook the chicken teriyaki. Once everything is cooked, divide it into meal prep containers and store them in the refrigerator. You can then grab a container and go on busy mornings!

If you're looking for a healthy and delicious meal that can be easily prepped ahead of time, this meal is a great option. It's packed with nutrients and flavor, and it's sure to keep you feeling full and satisfied.

Here's to healthy and delicious meal prepping!

If you are having trouble getting the output you want from prompts that use media files, there are some strategies that can help you get the results you want. The following sections provide design approaches and troubleshooting tips for improving prompts that use multimodal input.

You can improve your multimodal prompts by following these best practices:

Prompts have the most success when they are clear and detailed. If you have a specific output in mind, it's better to include that requirement in the prompt to ensure you get the output you want.

For this image of an airport board, asking the model to just "describe this image" could generate a general description. If you need the model to parse the time and city from the image, you can include that request directly in your prompt.

The image shows an airport arrivals and departures board.

Updated prompt Improved response Parse the time and city from the airport board shown in this image into a list. 10:50 Moscow 11:05 Edinburgh 11:05 London 11:10 Bucharest 11:30 Kiev 11:35 Dublin 11:45 East Midlands 12:15 Sofia 12:30 London 12:30 Newcastle 12:40 St Petersburg 12:40 London 12:45 Manchester

Parse the time and city from the airport board shown in this image into a list.

10:50 Moscow 11:05 Edinburgh 11:05 London 11:10 Bucharest 11:30 Kiev 11:35 Dublin 11:45 East Midlands 12:15 Sofia 12:30 London 12:30 Newcastle 12:40 St Petersburg 12:40 London 12:45 Manchester

The Gemini model can accept multiple inputs which it can use as examples to understand the output you want. Adding these examples can help the model identify the patterns and apply the relationship between the given images and responses to the new example. This is also called "few-shot" learning.

In the example below, the initial output is written in sentence form, and also contains the country (Brazil). Suppose you want the output in a different format or style, and you want only the city, not the country. Adding few-shot examples to your prompt can steer the model to respond in the way you want.

Prompt Model response Determine the city along with the landmark. The landmark is the Christ the Redeemer statue in Rio de Janeiro, Brazil.

Determine the city along with the landmark.

The landmark is the Christ the Redeemer statue in Rio de Janeiro, Brazil.

Determine the city along with the landmark.

city: Rome, landmark: the Colosseum.

city: Beijing, landmark: Forbidden City

city: Rio de Janeiro, landmark: Christ the Redeemer statue

For complex tasks like the ones that require both visual understanding and reasoning, it can be helpful to split the task into smaller, more straightforward steps. Alternatively, it could also be effective if you directly ask the model to “think step by step” in your prompt.

When will I run out of toilet paper?

Soon, you only have 3 rolls left.

1. First, count how many toilet paper rolls are in this picture. 2. Then, determine how much toilet paper a typical person uses per day. 3. Calculate how long these rolls of toilet paper will last.

1. There are 3 rolls of toilet paper in this picture. 2. A typical person uses about 20 sheets of toilet paper per day. 3. If each roll contains 200 sheets, then each roll will last for about 10 days. Therefore, the 3 rolls will last for about a month.

Math problems or other types of word problems are great candidates for asking the model to think step-by-step.

What is the 4th term in the sequence?

What is the 4th term in the sequence?

The response from the model is incorrect. Some ways to improve this is to ask the model to parse the problem before answering the prompt.

Parse the formula in the image first. Then based on the formula, answer "what's the 4th term in the sequence?".

Parse the formula in the image first.

Then based on the formula, answer "what's the 4th term in the sequence?".

Click to expand the result $$ b(n) = b(n-1) * (-3) $$ $$ b(1) = 15 $$ Substitute n = 4 into the formula: $$ b(4) = b(4-1) * (-3) $$ $$ b(4) = b(3) * (-3) $$ We don't know the value of b(3), so substitute n = 3 into the formula: $$ b(3) = b(3-1) * (-3) $$ $$ b(3) = b(2) * (-3) $$ We don't know the value of b(2), so substitute n = 2 into the formula: $$ b(2) = b(2-1) * (-3) $$ $$ b(2) = b(1) * (-3) $$ We know the value of b(1) is 15, so substitute it into the formula: $$ b(2) = 15 * (-3) $$ $$ b(2) = -45 $$ Now that we know the value of b(2), substitute it into the formula for b(3): $$ b(3) = b(2) * (-3) $$ $$ b(3) = -45 * (-3) $$ $$ b(3) = 135 $$ Now that we know the value of b(3), substitute it into the formula for b(4): $$ b(4) = b(3) * (-3) $$ $$ b(4) = 135 * (-3) $$ $$ b(4) = -405 $$ Therefore, the 4th term in the sequence is -405.

$$ b(n) = b(n-1) * (-3) $$

$$ b(4) = b(4-1) * (-3) $$

$$ b(4) = b(3) * (-3) $$

$$ b(3) = b(3-1) * (-3) $$

$$ b(3) = b(2) * (-3) $$

$$ b(2) = b(2-1) * (-3) $$

$$ b(2) = b(1) * (-3) $$

$$ b(2) = 15 * (-3) $$

$$ b(3) = b(2) * (-3) $$

$$ b(3) = -45 * (-3) $$

$$ b(4) = b(3) * (-3) $$

$$ b(4) = 135 * (-3) $$

Therefore, the 4th term in the sequence is -405.

This model response is correct - now to make the response even more streamlined, you can ask the model to to think step-by-step.

Updated prompt Improved response What is the 4th term in the sequence? Think step by step. The first term is 15. The second term is b(1) * (-3) = 15 * (-3) = -45. The third term is b(2) * (-3) = -45 * (-3) = 135. The fourth term is b(3) * (-3) = 135 * (-3) = -405.

What is the 4th term in the sequence? Think step by step.

The first term is 15.

The second term is b(1) * (-3) = 15 * (-3) = -45.

The third term is b(2) * (-3) = -45 * (-3) = 135.

The fourth term is b(3) * (-3) = 135 * (-3) = -405.

A common problem is the need for model output to be in a certain format (e.g. markdown, JSON, HTML), especially if the model output needs to be ingested by a downstream task. You can try to produce output in that format by instructing the model to do so within the prompt. Below are two examples:

Parse the table in this image into markdown format

| Subject | Status | Time | Start date | Due on |

| ------- | ------ | ---- | ---------- | ------ |

| Math | Done | 1.5 hrs | 11/29/2023 | 12/1/2023 |

| Geography | Done | 30 min | 12/2/2023 | 12/4/2023 |

| Physics | In progress | 2 hrs | 12/3/2023 | 12/5/2023 |

| Biology | Not started | 6 hrs | 11/2/2016 | 12/6/2023 |

Provide a list of all the following attributes:

ingredients, type of cuisine, vegetarian or not, in JSON format

```json { "ingredients": [ "rice", "shrimp", "clams", "mussels", "peas", "tomatoes", "onions", "garlic", "olive oil", "paprika", "salt", "pepper" ], "type of cuisine": "Spanish", "vegetarian": false } ```

"type of cuisine": "Spanish",

While Gemini can interpret image and text in any order within a prompt, placing a single image before the text prompt might lead to better results. In the following samples, you'll notice the image comes first before the text in each prompt.

You might need to troubleshoot your prompt if you are not getting a helpful response. Here are a few strategies you could try.

To get a more specific response, you can point out which aspects of the image you want the prompt to draw information from to inform its response.

How many days will these diapers last a baby?

The diapers will last for 198 days before they run out.

How long will these diapers last before I run out?

Use the weight shown on the box to determine the child's age, and use the total number of diapers in the box.

Divide the total number by how many diapers the child goes through per day.

The box contains 198 diapers. The box states the diapers are for a child weighing 22-37 lbs.

The average child in this weight range is likely between 1 and 2 years old.

A 2-year-old typically goes through 6 diapers per day, therefore, the diapers will last around 33 days (198/6).

To help the model tailor its response to the image(s), try asking it to describe the images before performing its reasoning task.

What is in common between these images?

All four images are examples of landscape photography.

First, describe what's in each image in detail. What's in common between these images?

The first image shows a person packing a suitcase. The second image shows an empty hallway in a shopping mall. The third image shows a roll of toilet paper. The fourth image shows a dark and stormy sea.

The commonality between these images is that they are all examples of liminal spaces. Liminal spaces are places or situations that are in between two other places or situations. They are often characterized by a sense of uncertainty or ambiguity.

The first image shows the person in between being at home and being on a trip. The second image shows the hallway in between two stores. The third image is of toilet paper, which can represent a bathroom. A bathroom is a transitional space between private and public realms. It's a place where we prepare ourselves to enter or leave the outside world.

The fourth image shows the sea in between being calm and being stormy.

Liminal spaces can be both exciting and unsettling. They can be a place of new beginning or a place of endings. They can be a place of reflection or a place of action.

You can also try explicitly asking the model to refer to what's in the image.

What is in common between these images? Refer to what's in the images in your response.

All of the images are related to travel. The first image shows a person packing a suitcase, the second image shows an empty hallway in a shopping mall, the third image shows a stack of toilet paper, and the fourth image shows a dark and stormy sea.

These images are all related to travel because they are all things that people need or use when they travel. The first image shows a person packing a suitcase, which is something that people do when they are going on a trip. The second image shows an empty hallway in a shopping mall, which is a place where people often go to buy things for their trips. The third image shows a stack of toilet paper, which is something that people often use when they are traveling. The fourth image shows a dark and stormy sea, which is something that people often encounter when they are traveling.

The same tips work for creative output from images. In the following example with the rabbit, explicitly asking the model to include aspects from the image can improve the output.

Can you write me a poem about this image?

Little bunny, so soft and brown, Hopping through the field, up and down. Your ears so long, your tail so small, You're the cutest creature of them all.

You nibble on the grass, so green and sweet, And hop away when you see me. But I'll always be your friend, Little bunny, until the very end.

Updated prompt Improved response Can you write me a descriptive and dramatic poem about this image and include the location? Little bunny on the green, Ears so long, so keen. What do you see out there, In the distance, where you stare? Is it the ocean blue, Sparkling in the sun's hue? Or the waves that crash and roar, A rhythm that you adore? Little bunny, tell me true, What captures your attention so? Is it the salty breeze, Or the seagulls' cries that please? Perhaps it's the vastness of it all, A world so big and small. A place where dreams can roam, And adventures can be sown. Little bunny, I wonder what you dream, As you sit on the grass, so serene. Do you yearn to explore the deep, Or stay on land, where you can leap? Whatever it may be, little bunny, Keep that spark of wonder burning brightly. For in your dreams and aspirations, Lies a world waiting for your creation.

Can you write me a descriptive and dramatic poem about this image and include the location?

Little bunny on the green, Ears so long, so keen. What do you see out there, In the distance, where you stare?

Is it the ocean blue, Sparkling in the sun's hue? Or the waves that crash and roar, A rhythm that you adore?

Little bunny, tell me true, What captures your attention so? Is it the salty breeze, Or the seagulls' cries that please?

Perhaps it's the vastness of it all, A world so big and small. A place where dreams can roam, And adventures can be sown.

Little bunny, I wonder what you dream, As you sit on the grass, so serene. Do you yearn to explore the deep, Or stay on land, where you can leap?

Whatever it may be, little bunny, Keep that spark of wonder burning brightly. For in your dreams and aspirations, Lies a world waiting for your creation.

It can be hard to know whether a prompt failed because the model didn't understand the image to begin with, or if it did understand the image but did not perform the correct reasoning steps afterward. To disambiguate between those reasons, ask the model to describe what's in the image.

In the following example, if the model responds with a snack that seems surprising when paired with tea (e.g. popcorn), you can first troubleshoot to determine whether the model correctly recognized that the image contains tea.

What's a snack I can make in 1 minute that would go well with this?

Describe what's in this image.

Another strategy is to ask the model to explain its reasoning. That can help you narrow down which part of the reasoning broke down, if any.

What's a snack I can make in 1 minute that would go well with this?

What's a snack I can make in 1 minute that would go well with this? Please explain why.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-08 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp3")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=["Describe this audio clip", myfile]
)

print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp3")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=["Describe this audio clip", myfile]
)

print(response.text)
```

Example 3 (python):
```python
import {
  GoogleGenAI,
  createUserContent,
  createPartFromUri,
} from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const myfile = await ai.files.upload({
    file: "path/to/sample.mp3",
    config: { mimeType: "audio/mpeg" },
  });

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: createUserContent([
      createPartFromUri(myfile.uri, myfile.mimeType),
      "Describe this audio clip",
    ]),
  });
  console.log(response.text);
}

await main();
```

Example 4 (python):
```python
import {
  GoogleGenAI,
  createUserContent,
  createPartFromUri,
} from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const myfile = await ai.files.upload({
    file: "path/to/sample.mp3",
    config: { mimeType: "audio/mpeg" },
  });

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: createUserContent([
      createPartFromUri(myfile.uri, myfile.mimeType),
      "Describe this audio clip",
    ]),
  });
  console.log(response.text);
}

await main();
```

---

## Embeddings

**URL:** https://ai.google.dev/gemini-api/docs/embeddings

**Contents:**
- Embeddings
- Generating embeddings
  - Python
  - JavaScript
  - Go
  - REST
  - Python
  - JavaScript
  - Go
  - REST

The Gemini API offers text embedding models to generate embeddings for words, phrases, sentences, and code. These foundational embeddings power advanced NLP tasks such as semantic search, classification, and clustering, providing more accurate, context-aware results than keyword-based approaches.

Building Retrieval Augmented Generation (RAG) systems is a common use case for embeddings. Embeddings play a key role in significantly enhancing model outputs with improved factual accuracy, coherence, and contextual richness. They efficiently retrieve relevant information from knowledge bases, represented by embeddings, which are then passed as additional context in the input prompt to language models, guiding it to generate more informed and accurate responses.

To learn more about the available embedding model variants, see the Model versions section. For higher throughput serving at half the price, try Batch API Embedding.

Use the embedContent method to generate text embeddings:

You can also generate embeddings for multiple chunks at once by passing them in as a list of strings.

You can use embeddings for a wide range of tasks from classification to document search. Specifying the right task type helps optimize the embeddings for the intended relationships, maximizing accuracy and efficiency. For a complete list of supported task types, see the Supported task types table.

The following example shows how you can use SEMANTIC_SIMILARITY to check how similar in meaning strings of texts are.

The following shows an example output from this code snippet:

The Gemini embedding model, gemini-embedding-001, is trained using the Matryoshka Representation Learning (MRL) technique which teaches a model to learn high-dimensional embeddings that have initial segments (or prefixes) which are also useful, simpler versions of the same data.

Use the output_dimensionality parameter to control the size of the output embedding vector. Selecting a smaller output dimensionality can save storage space and increase computational efficiency for downstream applications, while sacrificing little in terms of quality. By default, it outputs a 3072-dimensional embedding, but you can truncate it to a smaller size without losing quality to save storage space. We recommend using 768, 1536, or 3072 output dimensions.

Example output from the code snippet:

The 3072 dimension embedding is normalized. Normalized embeddings produce more accurate semantic similarity by comparing vector direction, not magnitude. For other dimensions, including 768 and 1536, you need to normalize the embeddings as follows:

Example output from this code snippet:

The following table shows the MTEB scores, a commonly used benchmark for embeddings, for different dimensions. Notably, the result shows that performance is not strictly tied to the size of the embedding dimension, with lower dimensions achieving scores comparable to their higher dimension counterparts.

Text embeddings are crucial for a variety of common AI use cases, such as:

Information retrieval: Search for the most semantically similar text or documents given a piece of input text.

Document search tutorialtask

Search reranking: Prioritize the most relevant items by semantically scoring initial results against the query.

Search reranking tutorialtask

Anomaly detection: Comparing groups of embeddings can help identify hidden trends or outliers.

Anomaly detection tutorialbubble_chart

Classification: Automatically categorize text based on its content, such as sentiment analysis or spam detection

Classification tutorialtoken

Clustering: Effectively grasp complex relationships by creating clusters and visualizations of your embeddings.

Clustering visualization tutorialbubble_chart

As you take embeddings to production, it is common to use vector databases to efficiently store, index, and retrieve high-dimensional embeddings. Google Cloud offers managed data services that can be used for this purpose including BigQuery, AlloyDB, and Cloud SQL.

The following tutorials show how to use other third party vector databases with Gemini Embedding.

Output dimension size

Flexible, supports: 128 - 3072, Recommended: 768, 1536, 3072

If latency is not a concern, try using the Gemini Embeddings model with Batch API. This allows for much higher throughput at 50% of interactive Embedding pricing. Find examples on how to get started in the Batch API cookbook.

Unlike generative AI models that create new content, the Gemini Embedding model is only intended to transform the format of your input data into a numerical representation. While Google is responsible for providing an embedding model that transforms the format of your input data to the numerical-format requested, users retain full responsibility for the data they input and the resulting embeddings. By using the Gemini Embedding model you confirm that you have the necessary rights to any content that you upload. Do not generate content that infringes on others' intellectual property or privacy rights. Your use of this service is subject to our Prohibited Use Policy and Google's Terms of Service.

Check out the embeddings quickstart notebook to explore the model capabilities and learn how to customize and visualize your embeddings.

The following models will be deprecated in October, 2025: - embedding-001 - embedding-gecko-001 - gemini-embedding-exp-03-07 (gemini-embedding-exp)

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-11 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents="What is the meaning of life?")

print(result.embeddings)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents="What is the meaning of life?")

print(result.embeddings)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

async function main() {

    const ai = new GoogleGenAI({});

    const response = await ai.models.embedContent({
        model: 'gemini-embedding-001',
        contents: 'What is the meaning of life?',
    });

    console.log(response.embeddings);
}

main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

async function main() {

    const ai = new GoogleGenAI({});

    const response = await ai.models.embedContent({
        model: 'gemini-embedding-001',
        contents: 'What is the meaning of life?',
    });

    console.log(response.embeddings);
}

main();
```

---

## Data Logging and Sharing

**URL:** https://ai.google.dev/gemini-api/docs/logs-policy

**Contents:**
- Data Logging and Sharing
- 1. Data that can be shared
- 2. How we use your data
- 3. Data permissions
- 4. Data sharing and feedback

This page outlines the storage and management of Gemini API logs, which are developer-owned API data from supported Gemini API calls for projects with billing enabled. Logs encompass the entire process from a user's request to the model's response.

As a project owner you have the choice to opt-in to logging of Gemini API calls, for your own use or for feedback and sharing with Google to help us continually improve our models.

With logging enabled, you can help us build AI systems that continue to be valuable for developers across various fields and use cases by choosing to contribute the following data for product improvements and model training:

When you share a dataset with Google, your logs in that dataset, including requests and responses, will be processed in accordance with our Terms for "Unpaid Services," meaning the dataset may be used to develop and improve Google products, services, and machine learning technologies, including improving and training our models. Do not include personal, sensitive, or confidential information.

Logs will expire after 55 days by default. They will become unavailable after this period. Datasets can be created to retain logs of interest or value beyond this period for downstream use cases and optional contribution to model improvements. Logs stored in datasets do not have set expiry dates, however each project has a default storage limit of up to 1,000 logs.

By default, because logging is only available for billing-enabled projects, prompts and responses within logs are not used for product improvement or development, in accordance with our Terms on data use.

If you choose to share datasets of your logs with Google, those datasets will be used as real-world demonstration data to better understand the diversity of domains and contexts AI systems and applications are used in. This data may be used to improve model quality, and inform the training and evaluation of future models and services. This data is processed in accordance with our data use terms for Unpaid Services. Accordingly, human reviewers may read, annotate, and process the API inputs and outputs you share. Before data is used for model improvement, Google takes steps to protect user privacy as part of this process. This includes disconnecting this data from your Google Account, API key, and Cloud project before reviewers see or annotate it.

By opting-in to contributing API data, you confirm that you have the necessary permissions for Google to process and use the data as described in this documentation. Please do not contribute logs containing sensitive, confidential, or proprietary information obtained through the paid service. The license you grant to Google under the "Submission of Content" section in the API Terms also extends, to the extent required under applicable law for our use, to any content (e.g., prompts, including associated system instructions, cached content, and files such as images, videos, or documents) you submit to the Services and to any generated responses.

You can help us advance the frontier of AI research, the Gemini API and Google AI Studio by opting in to share your data as examples, enabling us to continually improve our models across various contexts and build AI systems that continue to be valuable to developers across various fields and use cases.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-10-30 UTC.

---

## Gemini Developer API pricing

**URL:** https://ai.google.dev/gemini-api/docs/pricing

**Contents:**
- Gemini Developer API pricing
  - Free
  - Paid
  - Enterprise
- Gemini 3 Pro Preview
  - Standard
  - Batch
- Gemini 3 Flash Preview
  - Standard
  - Batch

Start building free of charge with generous limits, then scale up with pay-as-you-go pricing for your production ready applications.

For developers and small projects getting started with the Gemini API.

For production applications that require higher volumes and advanced features.

For large-scale deployments with custom needs for security, support, and compliance, powered by Vertex AI.

Try it in Google AI Studio

The best model in the world for multimodal understanding, and our most powerful agentic and vibe-coding model yet.

* A customer-submitted request to Gemini may result in one or more queries to Google Search. You will be charged for each individual search query performed.

** Gemini 3 billing for Grounding with Google Search will start January 5, 2026.

Try it in Google AI Studio

Our most intelligent model built for speed, combining frontier intelligence with superior search and grounding.

* A customer-submitted request to Gemini may result in one or more queries to Google Search. You will be charged for each individual search query performed.

** Gemini 3 billing for Grounding with Google Search will start January 5, 2026.

Try it in Google AI Studio

Our native image generation model, optimized for speed, flexibility, and contextual understanding. Text input and output is priced the same as Gemini 3 Pro.

Preview models may change before becoming stable and have more restrictive rate limits.

* Image input is set at 560 tokens or $0.0011 per image.

** Image output is priced at $120 per 1,000,000 tokens. Output images from 1024x1024px (1K) and up to 2048x2048px (2K) consume 1120 tokens and are equivalent to $0.134 per image. Output images up to 4096x4096px (4K) consume 2000 tokens and are equivalent to $0.24 per image.

Try it in Google AI Studio

Our state-of-the-art multipurpose model, which excels at coding and complex reasoning tasks.

Try it in Google AI Studio

Our first hybrid reasoning model which supports a 1M token context window and has thinking budgets.

Try it in Google AI Studio

The latest model based on the 2.5 Flash model. 2.5 Flash Preview is best for large scale processing, low-latency, high volume tasks that require thinking, and agentic use cases.

Try it in Google AI Studio

Our smallest and most cost effective model, built for at scale usage.

Try it in Google AI Studio

The latest model based on Gemini 2.5 Flash lite optimized for cost-efficiency, high throughput and high quality.

Try it in Google AI Studio

Our Live API native audio models optimized for higher quality audio outputs with better pacing, voice naturalness, verbosity, and mood.

Preview models may change before becoming stable and have more restrictive rate limits.

Try it in Google AI Studio

Our native image generation model, optimized for speed, flexibility, and contextual understanding. Text input and output is priced the same as 2.5 Flash.

Preview models may change before becoming stable and have more restrictive rate limits.

[*] Image output is priced at $30 per 1,000,000 tokens. Output images up to 1024x1024px consume 1290 tokens and are equivalent to $0.039 per image.

Try it in Google AI Studio

Our 2.5 Flash text-to-speech audio model optimized for price-performant, low-latency, controllable speech generation.

Preview models may change before becoming stable and have more restrictive rate limits.

Try it in Google AI Studio

Our 2.5 Pro text-to-speech audio model optimized for powerful, low-latency speech generation for more natural outputs and easier to steer prompts.

Preview models may change before becoming stable and have more restrictive rate limits.

Try it in Google AI Studio

Our most balanced multimodal model with great performance across all tasks, with a 1 million token context window, and built for the era of Agents.

[*] Image output is priced at $30 per 1,000,000 tokens. Output images up to 1024x1024px consume 1290 tokens and are equivalent to $0.039 per image.

Try it in Google AI Studio

Our smallest and most cost effective model, built for at scale usage.

Try it in Google AI Studio

Our latest image generation model, with significantly better text rendering and better overall image quality.

Preview models may change before becoming stable and have more restrictive rate limits.

Try it in Google AI Studio

Our state-of-the-art image generation model, available to developers on the paid tier of the Gemini API.

Our latest video generation model, available to developers on the paid tier of the Gemini API.

Preview models may change before becoming stable and have more restrictive rate limits.

Our stable video generation model, available to developers on the paid tier of the Gemini API.

Our state-of-the-art video generation model, available to developers on the paid tier of the Gemini API.

Our newest embeddings model, more stable and with higher rate limits than previous versions, available to developers on the free and paid tiers of the Gemini API.

Try it in Google AI Studio

Gemini Robotics-ER, short for Gemini Robotics-Embodied Reasoning, is a thinking model that enhances robots' abilities to understand and interact with the physical world.

Our Computer Use model optimized for building browser control agents that automate tasks.

Our lightweight, state-of the art, open model built from the same technology that powers our Gemini models.

Our open model built for efficient performance on everyday devices like mobile phones, laptops, and tablets.

Tools are priced at their own rates, applied to the model using them. Check the Models page for which tools are available to each model.

[*] Google AI Studio usage is free of charge in all available regions. See Billing FAQs for details.

[**] Prices may differ from the prices listed here and the prices offered on Vertex AI. For Vertex prices, see the Vertex AI pricing page.

[***] If you are using dynamic retrieval to optimize costs, only requests that contain at least one grounding support URL from the web in their response are charged for Grounding with Google Search. Costs for Gemini always apply. Rate limits are subject to change.

Agent usage costs are calculated based on the underlying token consumption and usage of the tools.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

---

## Fine-tuning with the Gemini API

**URL:** https://ai.google.dev/gemini-api/docs/model-tuning

**Contents:**
- Fine-tuning with the Gemini API

With the deprecation of Gemini 1.5 Flash-001 in May 2025, we no longer have a model available which supports fine-tuning in the Gemini API, but it is supported in Vertex AI.

We plan to bring fine-tuning support back in the future. We would love to hear from you on our developer forum if fine-tuning is important to your use case.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-12 UTC.

---

## Gemini models

**URL:** https://ai.google.dev/gemini-api/docs/models/experimental-models

**Contents:**
- Gemini models
- Gemini 3 Pro
  - Expand to learn more
    - Model details
  - Gemini 3 Pro Preview
  - Gemini 3 Pro Image Preview
- Gemini 3 Flash
  - Expand to learn more
    - Model details
  - Gemini 3 Flash Preview

OUR MOST INTELLIGENT MODEL

The best model in the world for multimodal understanding, and our most powerful agentic and vibe-coding model yet, delivering richer visuals and deeper interactivity, all built on a foundation of state-of-the-art reasoning.

Try in Google AI Studio

Text, Image, Video, Audio, and PDF

Grounding with Google Maps

Grounding with Google Maps

OUR MOST INTELLIGENT MODEL

Our most intelligent model built for speed, combining frontier intelligence with superior search and grounding.

Try in Google AI Studio

Text, Image, Video, Audio, and PDF

Grounding with Google Maps

Our best model in terms of price-performance, offering well-rounded capabilities. 2.5 Flash is best for large scale processing, low-latency, high volume tasks that require thinking, and agentic use cases.

Try in Google AI Studio

Text, images, video, audio

Grounding with Google Maps

Text, images, video, audio

Grounding with Google Maps

Grounding with Google Maps

Grounding with Google Maps

Grounding with Google Maps

Our fastest flash model optimized for cost-efficiency and high throughput.

Try in Google AI Studio

Text, image, video, audio, PDF

Grounding with Google Maps

Text, image, video, audio, PDF

Grounding with Google Maps

OUR ADVANCED THINKING MODEL

Our state-of-the-art thinking model, capable of reasoning over complex problems in code, math, and STEM, as well as analyzing large datasets, codebases, and documents using long context.

Try in Google AI Studio

Audio, images, video, text, and PDF

Grounding with Google Maps

Grounding with Google Maps

OUR SECOND GENERATION WORKHORSE MODEL

Our second generation workhorse model, with a 1 million token context window.

Gemini 2.0 Flash delivers next-gen features and improved capabilities, including superior speed, native tool use, and a 1M token context window.

Try in Google AI Studio

Audio, images, video, and text

Grounding with Google Maps

Audio, images, video, and text

Grounding with Google Maps

gemini-2.0-flash-preview-image-generation is not currently supported in a number of countries in Europe, Middle East & Africa

OUR SECOND GENERATION FAST MODEL

Our second generation small workhorse model, with a 1 million token context window.

A Gemini 2.0 Flash model optimized for cost efficiency and low latency.

Try in Google AI Studio

Audio, images, video, and text

Grounding with Google Maps

Gemini models are available in either stable, preview, latest, or experimental versions.

Points to a specific stable model. Stable models usually don't change. Most production apps should use a specific stable model.

For example: gemini-2.5-flash.

Points to a preview model which may be used for production. Preview models will typically have billing enabled, might come with more restrictive rate limits and will be deprecated with at least 2 weeks notice.

For example: gemini-2.5-flash-preview-09-2025.

Points to the latest release for a specific model variation. This can be a stable, preview or experimental release. This alias will get hot-swapped with every new release of a specific model variation. A 2-week notice will be provided through email before the version behind latest is changed.

For example: gemini-flash-latest.

Points to an experimental model which will typically be not be suitable for production use and come with more restrictive rate limits. We release experimental models to gather feedback and get our latest updates into the hands of developers quickly.

Experimental models are not stable and availability of model endpoints is subject to change.

For information about model deprecations, visit the Gemini deprecations page.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

---

## Grounding with Google Search

**URL:** https://ai.google.dev/gemini-api/docs/grounding

**Contents:**
- Grounding with Google Search
  - Python
  - JavaScript
  - REST
- How grounding with Google Search works
- Understanding the grounding response
- Attributing sources with inline citations
  - Python
  - JavaScript
- Pricing

Grounding with Google Search connects the Gemini model to real-time web content and works with all available languages. This allows Gemini to provide more accurate answers and cite verifiable sources beyond its knowledge cutoff.

Grounding helps you build applications that can:

Provide citations: Build user trust by showing the sources for the model's claims.

You can learn more by trying the Search tool notebook.

When you enable the google_search tool, the model handles the entire workflow of searching, processing, and citing information automatically.

When a response is successfully grounded, the response includes a groundingMetadata field. This structured data is essential for verifying claims and building a rich citation experience in your application.

The Gemini API returns the following information with the groundingMetadata:

Grounding with Google Search can also be used in combination with the URL context tool to ground responses in both public web data and the specific URLs you provide.

The API returns structured citation data, giving you complete control over how you display sources in your user interface. You can use the groundingSupports and groundingChunks fields to link the model's statements directly to their sources. Here is a common pattern for processing the metadata to create a response with inline, clickable citations.

The new response with inline citations will look like this:

When you use Grounding with Google Search with Gemini 3, your project is billed for each search query that the model decides to execute. If the model decides to execute multiple search queries to answer a single prompt (for example, searching for "UEFA Euro 2024 winner" and "Spain vs England Euro 2024 final score" within the same API call), this counts as two billable uses of the tool for that request. This only applies to Gemini 3 models; when you use search grounding with Gemini 2.5 or older models, your project is billed per prompt.

For detailed pricing information, see the Gemini API pricing page.

Experimental and Preview models are not included. You can find their capabilities on the model overview page.

You can use Grounding with Google Search with other tools like code execution and URL context to power more complex use cases.

While the google_search tool is recommended for Gemini 2.0 and later, Gemini 1.5 supports a legacy tool named google_search_retrieval. This tool provides a dynamic mode that allows the model to decide whether to perform a search based on its confidence that the prompt requires fresh information. If the model's confidence is above a dynamic_threshold you set (a value between 0.0 and 1.0), it will perform a search.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-05 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Who won the euro 2024?",
    config=config,
)

print(response.text)
```

Example 2 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Who won the euro 2024?",
    config=config,
)

print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

const groundingTool = {
  googleSearch: {},
};

const config = {
  tools: [groundingTool],
};

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: "Who won the euro 2024?",
  config,
});

console.log(response.text);
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

const groundingTool = {
  googleSearch: {},
};

const config = {
  tools: [groundingTool],
};

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: "Who won the euro 2024?",
  config,
});

console.log(response.text);
```

---

## Files API

**URL:** https://ai.google.dev/gemini-api/docs/prompting_with_media?lang=python

**Contents:**
- Files API
- Upload a file
  - Python
  - JavaScript
  - Go
  - REST
- Get metadata for a file
  - Python
  - JavaScript
  - Go

Gemini can handle various types of input data, including text, images, and audio, at the same time.

This guide shows you how to work with media files using the Files API. The basic operations are the same for audio files, images, videos, documents, and other supported file types.

For file prompting guidance, check out the File prompt guide section.

You can use the Files API to upload a media file. Always use the Files API when the total request size (including the files, text prompt, system instructions, etc.) is larger than 20 MB.

The following code uploads a file and then uses the file in a call to generateContent.

You can verify that the API successfully stored the uploaded file and get its metadata by calling files.get.

The following code gets a list of all the files uploaded:

Files are automatically deleted after 48 hours. You can also manually delete an uploaded file:

You can use the Files API to upload and interact with media files. The Files API lets you store up to 20 GB of files per project, with a per-file maximum size of 2 GB. Files are stored for 48 hours. During that time, you can use the API to get metadata about the files, but you can't download the files. The Files API is available at no cost in all regions where the Gemini API is available.

This section provides guidance and best practices for using media files with prompts for the Gemini API.

Being able to use various types of data in your prompts gives you more flexibility in terms of what tasks you can tackle with the Gemini API. For example, you can send the model a photo of a delicious meal and ask it to write a short blog about the meal.

Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.

Meal prepping is a great way to save time and money, and it can also help you to eat healthier. This meal is a great example of a healthy and delicious meal that can be easily prepped ahead of time.

This meal features brown rice, roasted vegetables, and chicken teriyaki. The brown rice is a healthy and complex carbohydrate that will give you sustained energy. The roasted vegetables are a great way to get your daily dose of vitamins and minerals, and the chicken teriyaki is a delicious and protein-rich option.

This meal is also very easy to prepare. Simply cook the brown rice, roast the vegetables, and cook the chicken teriyaki. Once everything is cooked, divide it into meal prep containers and store them in the refrigerator. You can then grab a container and go on busy mornings!

If you're looking for a healthy and delicious meal that can be easily prepped ahead of time, this meal is a great option. It's packed with nutrients and flavor, and it's sure to keep you feeling full and satisfied.

Here's to healthy and delicious meal prepping!

If you are having trouble getting the output you want from prompts that use media files, there are some strategies that can help you get the results you want. The following sections provide design approaches and troubleshooting tips for improving prompts that use multimodal input.

You can improve your multimodal prompts by following these best practices:

Prompts have the most success when they are clear and detailed. If you have a specific output in mind, it's better to include that requirement in the prompt to ensure you get the output you want.

For this image of an airport board, asking the model to just "describe this image" could generate a general description. If you need the model to parse the time and city from the image, you can include that request directly in your prompt.

The image shows an airport arrivals and departures board.

Updated prompt Improved response Parse the time and city from the airport board shown in this image into a list. 10:50 Moscow 11:05 Edinburgh 11:05 London 11:10 Bucharest 11:30 Kiev 11:35 Dublin 11:45 East Midlands 12:15 Sofia 12:30 London 12:30 Newcastle 12:40 St Petersburg 12:40 London 12:45 Manchester

Parse the time and city from the airport board shown in this image into a list.

10:50 Moscow 11:05 Edinburgh 11:05 London 11:10 Bucharest 11:30 Kiev 11:35 Dublin 11:45 East Midlands 12:15 Sofia 12:30 London 12:30 Newcastle 12:40 St Petersburg 12:40 London 12:45 Manchester

The Gemini model can accept multiple inputs which it can use as examples to understand the output you want. Adding these examples can help the model identify the patterns and apply the relationship between the given images and responses to the new example. This is also called "few-shot" learning.

In the example below, the initial output is written in sentence form, and also contains the country (Brazil). Suppose you want the output in a different format or style, and you want only the city, not the country. Adding few-shot examples to your prompt can steer the model to respond in the way you want.

Prompt Model response Determine the city along with the landmark. The landmark is the Christ the Redeemer statue in Rio de Janeiro, Brazil.

Determine the city along with the landmark.

The landmark is the Christ the Redeemer statue in Rio de Janeiro, Brazil.

Determine the city along with the landmark.

city: Rome, landmark: the Colosseum.

city: Beijing, landmark: Forbidden City

city: Rio de Janeiro, landmark: Christ the Redeemer statue

For complex tasks like the ones that require both visual understanding and reasoning, it can be helpful to split the task into smaller, more straightforward steps. Alternatively, it could also be effective if you directly ask the model to “think step by step” in your prompt.

When will I run out of toilet paper?

Soon, you only have 3 rolls left.

1. First, count how many toilet paper rolls are in this picture. 2. Then, determine how much toilet paper a typical person uses per day. 3. Calculate how long these rolls of toilet paper will last.

1. There are 3 rolls of toilet paper in this picture. 2. A typical person uses about 20 sheets of toilet paper per day. 3. If each roll contains 200 sheets, then each roll will last for about 10 days. Therefore, the 3 rolls will last for about a month.

Math problems or other types of word problems are great candidates for asking the model to think step-by-step.

What is the 4th term in the sequence?

What is the 4th term in the sequence?

The response from the model is incorrect. Some ways to improve this is to ask the model to parse the problem before answering the prompt.

Parse the formula in the image first. Then based on the formula, answer "what's the 4th term in the sequence?".

Parse the formula in the image first.

Then based on the formula, answer "what's the 4th term in the sequence?".

Click to expand the result $$ b(n) = b(n-1) * (-3) $$ $$ b(1) = 15 $$ Substitute n = 4 into the formula: $$ b(4) = b(4-1) * (-3) $$ $$ b(4) = b(3) * (-3) $$ We don't know the value of b(3), so substitute n = 3 into the formula: $$ b(3) = b(3-1) * (-3) $$ $$ b(3) = b(2) * (-3) $$ We don't know the value of b(2), so substitute n = 2 into the formula: $$ b(2) = b(2-1) * (-3) $$ $$ b(2) = b(1) * (-3) $$ We know the value of b(1) is 15, so substitute it into the formula: $$ b(2) = 15 * (-3) $$ $$ b(2) = -45 $$ Now that we know the value of b(2), substitute it into the formula for b(3): $$ b(3) = b(2) * (-3) $$ $$ b(3) = -45 * (-3) $$ $$ b(3) = 135 $$ Now that we know the value of b(3), substitute it into the formula for b(4): $$ b(4) = b(3) * (-3) $$ $$ b(4) = 135 * (-3) $$ $$ b(4) = -405 $$ Therefore, the 4th term in the sequence is -405.

$$ b(n) = b(n-1) * (-3) $$

$$ b(4) = b(4-1) * (-3) $$

$$ b(4) = b(3) * (-3) $$

$$ b(3) = b(3-1) * (-3) $$

$$ b(3) = b(2) * (-3) $$

$$ b(2) = b(2-1) * (-3) $$

$$ b(2) = b(1) * (-3) $$

$$ b(2) = 15 * (-3) $$

$$ b(3) = b(2) * (-3) $$

$$ b(3) = -45 * (-3) $$

$$ b(4) = b(3) * (-3) $$

$$ b(4) = 135 * (-3) $$

Therefore, the 4th term in the sequence is -405.

This model response is correct - now to make the response even more streamlined, you can ask the model to to think step-by-step.

Updated prompt Improved response What is the 4th term in the sequence? Think step by step. The first term is 15. The second term is b(1) * (-3) = 15 * (-3) = -45. The third term is b(2) * (-3) = -45 * (-3) = 135. The fourth term is b(3) * (-3) = 135 * (-3) = -405.

What is the 4th term in the sequence? Think step by step.

The first term is 15.

The second term is b(1) * (-3) = 15 * (-3) = -45.

The third term is b(2) * (-3) = -45 * (-3) = 135.

The fourth term is b(3) * (-3) = 135 * (-3) = -405.

A common problem is the need for model output to be in a certain format (e.g. markdown, JSON, HTML), especially if the model output needs to be ingested by a downstream task. You can try to produce output in that format by instructing the model to do so within the prompt. Below are two examples:

Parse the table in this image into markdown format

| Subject | Status | Time | Start date | Due on |

| ------- | ------ | ---- | ---------- | ------ |

| Math | Done | 1.5 hrs | 11/29/2023 | 12/1/2023 |

| Geography | Done | 30 min | 12/2/2023 | 12/4/2023 |

| Physics | In progress | 2 hrs | 12/3/2023 | 12/5/2023 |

| Biology | Not started | 6 hrs | 11/2/2016 | 12/6/2023 |

Provide a list of all the following attributes:

ingredients, type of cuisine, vegetarian or not, in JSON format

```json { "ingredients": [ "rice", "shrimp", "clams", "mussels", "peas", "tomatoes", "onions", "garlic", "olive oil", "paprika", "salt", "pepper" ], "type of cuisine": "Spanish", "vegetarian": false } ```

"type of cuisine": "Spanish",

While Gemini can interpret image and text in any order within a prompt, placing a single image before the text prompt might lead to better results. In the following samples, you'll notice the image comes first before the text in each prompt.

You might need to troubleshoot your prompt if you are not getting a helpful response. Here are a few strategies you could try.

To get a more specific response, you can point out which aspects of the image you want the prompt to draw information from to inform its response.

How many days will these diapers last a baby?

The diapers will last for 198 days before they run out.

How long will these diapers last before I run out?

Use the weight shown on the box to determine the child's age, and use the total number of diapers in the box.

Divide the total number by how many diapers the child goes through per day.

The box contains 198 diapers. The box states the diapers are for a child weighing 22-37 lbs.

The average child in this weight range is likely between 1 and 2 years old.

A 2-year-old typically goes through 6 diapers per day, therefore, the diapers will last around 33 days (198/6).

To help the model tailor its response to the image(s), try asking it to describe the images before performing its reasoning task.

What is in common between these images?

All four images are examples of landscape photography.

First, describe what's in each image in detail. What's in common between these images?

The first image shows a person packing a suitcase. The second image shows an empty hallway in a shopping mall. The third image shows a roll of toilet paper. The fourth image shows a dark and stormy sea.

The commonality between these images is that they are all examples of liminal spaces. Liminal spaces are places or situations that are in between two other places or situations. They are often characterized by a sense of uncertainty or ambiguity.

The first image shows the person in between being at home and being on a trip. The second image shows the hallway in between two stores. The third image is of toilet paper, which can represent a bathroom. A bathroom is a transitional space between private and public realms. It's a place where we prepare ourselves to enter or leave the outside world.

The fourth image shows the sea in between being calm and being stormy.

Liminal spaces can be both exciting and unsettling. They can be a place of new beginning or a place of endings. They can be a place of reflection or a place of action.

You can also try explicitly asking the model to refer to what's in the image.

What is in common between these images? Refer to what's in the images in your response.

All of the images are related to travel. The first image shows a person packing a suitcase, the second image shows an empty hallway in a shopping mall, the third image shows a stack of toilet paper, and the fourth image shows a dark and stormy sea.

These images are all related to travel because they are all things that people need or use when they travel. The first image shows a person packing a suitcase, which is something that people do when they are going on a trip. The second image shows an empty hallway in a shopping mall, which is a place where people often go to buy things for their trips. The third image shows a stack of toilet paper, which is something that people often use when they are traveling. The fourth image shows a dark and stormy sea, which is something that people often encounter when they are traveling.

The same tips work for creative output from images. In the following example with the rabbit, explicitly asking the model to include aspects from the image can improve the output.

Can you write me a poem about this image?

Little bunny, so soft and brown, Hopping through the field, up and down. Your ears so long, your tail so small, You're the cutest creature of them all.

You nibble on the grass, so green and sweet, And hop away when you see me. But I'll always be your friend, Little bunny, until the very end.

Updated prompt Improved response Can you write me a descriptive and dramatic poem about this image and include the location? Little bunny on the green, Ears so long, so keen. What do you see out there, In the distance, where you stare? Is it the ocean blue, Sparkling in the sun's hue? Or the waves that crash and roar, A rhythm that you adore? Little bunny, tell me true, What captures your attention so? Is it the salty breeze, Or the seagulls' cries that please? Perhaps it's the vastness of it all, A world so big and small. A place where dreams can roam, And adventures can be sown. Little bunny, I wonder what you dream, As you sit on the grass, so serene. Do you yearn to explore the deep, Or stay on land, where you can leap? Whatever it may be, little bunny, Keep that spark of wonder burning brightly. For in your dreams and aspirations, Lies a world waiting for your creation.

Can you write me a descriptive and dramatic poem about this image and include the location?

Little bunny on the green, Ears so long, so keen. What do you see out there, In the distance, where you stare?

Is it the ocean blue, Sparkling in the sun's hue? Or the waves that crash and roar, A rhythm that you adore?

Little bunny, tell me true, What captures your attention so? Is it the salty breeze, Or the seagulls' cries that please?

Perhaps it's the vastness of it all, A world so big and small. A place where dreams can roam, And adventures can be sown.

Little bunny, I wonder what you dream, As you sit on the grass, so serene. Do you yearn to explore the deep, Or stay on land, where you can leap?

Whatever it may be, little bunny, Keep that spark of wonder burning brightly. For in your dreams and aspirations, Lies a world waiting for your creation.

It can be hard to know whether a prompt failed because the model didn't understand the image to begin with, or if it did understand the image but did not perform the correct reasoning steps afterward. To disambiguate between those reasons, ask the model to describe what's in the image.

In the following example, if the model responds with a snack that seems surprising when paired with tea (e.g. popcorn), you can first troubleshoot to determine whether the model correctly recognized that the image contains tea.

What's a snack I can make in 1 minute that would go well with this?

Describe what's in this image.

Another strategy is to ask the model to explain its reasoning. That can help you narrow down which part of the reasoning broke down, if any.

What's a snack I can make in 1 minute that would go well with this?

What's a snack I can make in 1 minute that would go well with this? Please explain why.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-08 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp3")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=["Describe this audio clip", myfile]
)

print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp3")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=["Describe this audio clip", myfile]
)

print(response.text)
```

Example 3 (python):
```python
import {
  GoogleGenAI,
  createUserContent,
  createPartFromUri,
} from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const myfile = await ai.files.upload({
    file: "path/to/sample.mp3",
    config: { mimeType: "audio/mpeg" },
  });

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: createUserContent([
      createPartFromUri(myfile.uri, myfile.mimeType),
      "Describe this audio clip",
    ]),
  });
  console.log(response.text);
}

await main();
```

Example 4 (python):
```python
import {
  GoogleGenAI,
  createUserContent,
  createPartFromUri,
} from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const myfile = await ai.files.upload({
    file: "path/to/sample.mp3",
    config: { mimeType: "audio/mpeg" },
  });

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: createUserContent([
      createPartFromUri(myfile.uri, myfile.mimeType),
      "Describe this audio clip",
    ]),
  });
  console.log(response.text);
}

await main();
```

---

## Batch API

**URL:** https://ai.google.dev/gemini-api/docs/batch-mode

**Contents:**
- Batch API
- Creating a batch job
  - Inline requests
  - Python
  - JavaScript
  - REST
  - Input file
  - Python
  - JavaScript
  - REST

The Gemini Batch API is designed to process large volumes of requests asynchronously at 50% of the standard cost. The target turnaround time is 24 hours, but in majority of cases, it is much quicker.

Use Batch API for large-scale, non-urgent tasks such as data pre-processing or running evaluations where an immediate response is not required.

You have two ways to submit your requests in Batch API:

For a small number of requests, you can directly embed the GenerateContentRequest objects within your BatchGenerateContentRequest. The following example calls the BatchGenerateContent method with inline requests:

For larger sets of requests, prepare a JSON Lines (JSONL) file. Each line in this file must be a JSON object containing a user-defined key and a request object, where the request is a valid GenerateContentRequest object. The user-defined key is used in the response to indicate which output is the result of which request. For example, the request with the key defined as request-1 will have its response annotated with the same key name.

This file is uploaded using the File API. The maximum allowed file size for an input file is 2GB.

The following is an example of a JSONL file. You can save it in a file named my-batch-requests.json:

Similarly to inline requests, you can specify other parameters like system instructions, tools or other configurations in each request JSON.

You can upload this file using the File API as shown in the following example. If you are working with multimodal input, you can reference other uploaded files within your JSONL file.

The following example calls the BatchGenerateContent method with the input file uploaded using File API:

When you create a batch job, you will get a job name returned. Use this name for monitoring the job status as well as retrieving the results once the job completes.

The following is an example output that contains a job name:

You can use the Batch API to interact with the Embeddings model for higher throughput. To create an embeddings batch job with either inline requests or input files, use the batches.create_embeddings API and specify the embeddings model.

Read the Embeddings section in the Batch API cookbook for more examples.

You can include any request configurations you would use in a standard non-batch request. For example, you could specify the temperature, system instructions or even pass in other modalities. The following example shows an example inline request that contains a system instruction for one of the requests:

Similarly can specify tools to use for a request. The following example shows a request that enables the Google Search tool:

You can specify structured output as well. The following example shows how to specify for your batch requests.

The following shows an example output of this job:

Use the operation name obtained when creating the batch job to poll its status. The state field of the batch job will indicate its current status. A batch job can be in one of the following states:

You can poll the job status periodically to check for completion.

Once the job status indicates your batch job has succeeded, the results are available in the response field.

You can cancel an ongoing batch job using its name. When a job is canceled, it stops processing new requests.

You can delete an existing batch job using its name. When a job is deleted, it stops processing new requests and is removed from the list of batch jobs.

If you're using Gemini Nano Banana and need to generate a lot of images, you can use the Batch API to get higher rate limits in exchange for a turnaround of up to 24 hours.

You can either use inline requests for small batches of requests (under 20MB) or a JSONL input file for large batches (recommended for image generation):

Inline requests Input file

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-04 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

# A list of dictionaries, where each is a GenerateContentRequest
inline_requests = [
    {
        'contents': [{
            'parts': [{'text': 'Tell me a one-sentence joke.'}],
            'role': 'user'
        }]
    },
    {
        'contents': [{
            'parts': [{'text': 'Why is the sky blue?'}],
            'role': 'user'
        }]
    }
]

inline_batch_job = client.batches.create(
    model="models/gemini-2.5-flash",
    src=inline_requests,
    config={
        'display_name': "inlined-requests-job-1",
    },
)

print(f"Created batch job: {inline_batch_job.name}")
```

Example 2 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

# A list of dictionaries, where each is a GenerateContentRequest
inline_requests = [
    {
        'contents': [{
            'parts': [{'text': 'Tell me a one-sentence joke.'}],
            'role': 'user'
        }]
    },
    {
        'contents': [{
            'parts': [{'text': 'Why is the sky blue?'}],
            'role': 'user'
        }]
    }
]

inline_batch_job = client.batches.create(
    model="models/gemini-2.5-flash",
    src=inline_requests,
    config={
        'display_name': "inlined-requests-job-1",
    },
)

print(f"Created batch job: {inline_batch_job.name}")
```

Example 3 (python):
```python
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({});

const inlinedRequests = [
    {
        contents: [{
            parts: [{text: 'Tell me a one-sentence joke.'}],
            role: 'user'
        }]
    },
    {
        contents: [{
            parts: [{'text': 'Why is the sky blue?'}],
            role: 'user'
        }]
    }
]

const response = await ai.batches.create({
    model: 'gemini-2.5-flash',
    src: inlinedRequests,
    config: {
        displayName: 'inlined-requests-job-1',
    }
});

console.log(response);
```

Example 4 (python):
```python
import {GoogleGenAI} from '@google/genai';

const ai = new GoogleGenAI({});

const inlinedRequests = [
    {
        contents: [{
            parts: [{text: 'Tell me a one-sentence joke.'}],
            role: 'user'
        }]
    },
    {
        contents: [{
            parts: [{'text': 'Why is the sky blue?'}],
            role: 'user'
        }]
    }
]

const response = await ai.batches.create({
    model: 'gemini-2.5-flash',
    src: inlinedRequests,
    config: {
        displayName: 'inlined-requests-job-1',
    }
});

console.log(response);
```

---

## Text generation

**URL:** https://ai.google.dev/gemini-api/docs/text-generation?lang=python

**Contents:**
- Text generation
  - Python
  - JavaScript
  - Go
  - Java
  - REST
  - Apps Script
- Thinking with Gemini 2.5
  - Python
  - JavaScript

The Gemini API can generate text output from various inputs, including text, images, video, and audio, leveraging Gemini models.

Here's a basic example that takes a single text input:

2.5 Flash and Pro models have "thinking" enabled by default to enhance quality, which may take longer to run and increase token usage.

When using 2.5 Flash, you can disable thinking by setting the thinking budget to zero.

For more details, see the thinking guide.

You can guide the behavior of Gemini models with system instructions. To do so, pass a GenerateContentConfig object.

The GenerateContentConfig object also lets you override default generation parameters, such as temperature.

Refer to the GenerateContentConfig in our API reference for a complete list of configurable parameters and their descriptions.

The Gemini API supports multimodal inputs, allowing you to combine text with media files. The following example demonstrates providing an image:

For alternative methods of providing images and more advanced image processing, see our image understanding guide. The API also supports document, video, and audio inputs and understanding.

By default, the model returns a response only after the entire generation process is complete.

For more fluid interactions, use streaming to receive GenerateContentResponse instances incrementally as they're generated.

Our SDKs provide functionality to collect multiple rounds of prompts and responses into a chat, giving you an easy way to keep track of the conversation history.

Streaming can also be used for multi-turn conversations.

All models in the Gemini family support text generation. To learn more about the models and their capabilities, visit the Models page.

For basic text generation, a zero-shot prompt often suffices without needing examples, system instructions or specific formatting.

For more tailored outputs:

Consult our prompt engineering guide for more tips.

In some cases, you may need structured output, such as JSON. Refer to our structured output guide to learn how.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "How does AI work?",
  });
  console.log(response.text);
}

await main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "How does AI work?",
  });
  console.log(response.text);
}

await main();
```

---

## Generate images using Imagen

**URL:** https://ai.google.dev/gemini-api/docs/imagen

**Contents:**
- Generate images using Imagen
- Generate images using the Imagen models
  - Python
  - JavaScript
  - Go
  - REST
  - Imagen configuration
- Imagen prompt guide
  - Prompt writing basics
  - Generate text in images

Imagen is Google's high-fidelity image generation model, capable of generating realistic and high quality images from text prompts. All generated images include a SynthID watermark. To learn more about the available Imagen model variants, see the Model versions section.

This example demonstrates generating images with an Imagen model:

Imagen supports English only prompts at this time and the following parameters:

personGeneration: Allow the model to generate images of people. The following values are supported:

This section of the Imagen guide shows you how modifying a text-to-image prompt can produce different results, along with examples of images you can create.

A good prompt is descriptive and clear, and makes use of meaningful keywords and modifiers. Start by thinking of your subject, context, and style.

Subject: The first thing to think about with any prompt is the subject: the object, person, animal, or scenery you want an image of.

Context and background: Just as important is the background or context in which the subject will be placed. Try placing your subject in a variety of backgrounds. For example, a studio with a white background, outdoors, or indoor environments.

Style: Finally, add the style of image you want. Styles can be general (painting, photograph, sketches) or very specific (pastel painting, charcoal drawing, isometric 3D). You can also combine styles.

After you write a first version of your prompt, refine your prompt by adding more details until you get to the image that you want. Iteration is important. Start by establishing your core idea, and then refine and expand upon that core idea until the generated image is close to your vision.

Imagen models can transform your ideas into detailed images, whether your prompts are short or long and detailed. Refine your vision through iterative prompting, adding details until you achieve the perfect result.

Short prompts let you generate an image quickly.

Longer prompts let you add specific details and build your image.

Additional advice for Imagen prompt writing:

Imagen models can add text into images, opening up more creative image generation possibilities. Use the following guidance to get the most out of this feature:

Multiple phrases: Experiment with two or three distinct phrases to provide additional information. Avoid exceeding three phrases for cleaner compositions.

Guide Placement: While Imagen can attempt to position text as directed, expect occasional variations. This feature is continually improving.

Inspire font style: Specify a general font style to subtly influence Imagen's choices. Don't rely on precise font replication, but expect creative interpretations.

Font size: Specify a font size or a general indication of size (for example, small, medium, large) to influence the font size generation.

To better control output results, you might find it helpful to parameterize the inputs into Imagen. For example, suppose you want your customers to be able to generate logos for their business, and you want to make sure logos are always generated on a solid color background. You also want to limit the options that the client can select from a menu.

In this example, you can create a parameterized prompt similar to the following:

In your custom user interface, the customer can input the parameters using a menu, and their chosen value populates the prompt Imagen receives.

Prompt: A minimalist logo for a health care company on a solid color background. Include the text Journey.

Prompt: A modern logo for a software company on a solid color background. Include the text Silo.

Prompt: A traditional logo for a baking company on a solid color background. Include the text Seed.

Use the following examples to create more specific prompts based on attributes like photography descriptors, shapes and materials, historical art movements, and image quality modifiers.

To use this style, start with using keywords that clearly tell Imagen that you're looking for a photograph. Start your prompts with "A photo of. . .". For example:

Image source: Each image was generated using its corresponding text prompt with the Imagen 3 model.

In the following examples, you can see several photography-specific modifiers and parameters. You can combine multiple modifiers for more precise control.

Camera Proximity - Close up, taken from far away

Prompt: A close-up photo of coffee beans Prompt: A zoomed out photo of a small bag of coffee beans in a messy kitchen

Camera Position - aerial, from below

Lighting - natural, dramatic, warm, cold

Camera Settings - motion blur, soft focus, bokeh, portrait

Lens types - 35mm, 50mm, fisheye, wide angle, macro

Film types - black and white, polaroid

Image source: Each image was generated using its corresponding text prompt with the Imagen 3 model.

Art styles vary from monochrome styles like pencil sketches, to hyper-realistic digital art. For example, the following images use the same prompt with different styles:

"An [art style or creation technique] of an angular sporty electric sedan with skyscrapers in the background"

Image source: Each image was generated using its corresponding text prompt with the Imagen 2 model.

One of the strengths of this technology is that you can create imagery that is otherwise difficult or impossible. For example, you can recreate your company logo in different materials and textures.

Image source: Each image was generated using its corresponding text prompt with the Imagen 3 model.

Certain styles have become iconic over the years. The following are some ideas of historical painting or art styles that you can try.

"generate an image in the style of [art period or movement] : a wind farm"

Image source: Each image was generated using its corresponding text prompt with the Imagen 3 model.

Certain keywords can let the model know that you're looking for a high-quality asset. Examples of quality modifiers include the following:

The following are a few examples of prompts without quality modifiers and the same prompt with quality modifiers.

Image source: Each image was generated using its corresponding text prompt with the Imagen 3 model.

Imagen image generation lets you set five distinct image aspect ratios.

Fullscreen (4:3) - This aspect ratio is commonly used in media or film. It is also the dimensions of most old (non-widescreen) TVs and medium format cameras. It captures more of the scene horizontally (compared to 1:1), making it a preferred aspect ratio for photography.

Portrait full screen (3:4) - This is the fullscreen aspect ratio rotated 90 degrees. This lets to capture more of the scene vertically compared to the 1:1 aspect ratio.

Widescreen (16:9) - This ratio has replaced 4:3 and is now the most common aspect ratio for TVs, monitors, and mobile phone screens (landscape). Use this aspect ratio when you want to capture more of the background (for example, scenic landscapes).

Portrait (9:16) - This ratio is widescreen but rotated. This a relatively new aspect ratio that has been popularized by short form video apps (for example, YouTube shorts). Use this for tall objects with strong vertical orientations such as buildings, trees, waterfalls, or other similar objects.

Different versions of the image generation model might offer a mix of artistic and photorealistic output. Use the following wording in prompts to generate more photorealistic output, based on the subject you want to generate.

Using several keywords from the table, Imagen can generate the following portraits:

Prompt: A woman, 35mm portrait, blue and grey duotones Model: imagen-3.0-generate-002

Prompt: A woman, 35mm portrait, film noir Model: imagen-3.0-generate-002

Using several keywords from the table, Imagen can generate the following object images:

Prompt: leaf of a prayer plant, macro lens, 60mm Model: imagen-3.0-generate-002

Prompt: a plate of pasta, 100mm Macro lens Model: imagen-3.0-generate-002

Using several keywords from the table, Imagen can generate the following motion images:

Prompt: a winning touchdown, fast shutter speed, movement tracking Model: imagen-3.0-generate-002

Prompt: A deer running in the forest, fast shutter speed, movement tracking Model: imagen-3.0-generate-002

Using several keywords from the table, Imagen can generate the following wide-angle images:

Prompt: an expansive mountain range, landscape wide angle 10mm Model: imagen-3.0-generate-002

Prompt: a photo of the moon, astro photography, wide angle 10mm Model: imagen-3.0-generate-002

imagen-4.0-generate-001 imagen-4.0-ultra-generate-001 imagen-4.0-fast-generate-001

1 to 4 (Ultra/Standard/Fast)

imagen-3.0-generate-002

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-03 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client()

response = client.models.generate_images(
    model='imagen-4.0-generate-001',
    prompt='Robot holding a red skateboard',
    config=types.GenerateImagesConfig(
        number_of_images= 4,
    )
)
for generated_image in response.generated_images:
  generated_image.image.show()
```

Example 2 (python):
```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client()

response = client.models.generate_images(
    model='imagen-4.0-generate-001',
    prompt='Robot holding a red skateboard',
    config=types.GenerateImagesConfig(
        number_of_images= 4,
    )
)
for generated_image in response.generated_images:
  generated_image.image.show()
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {

  const ai = new GoogleGenAI({});

  const response = await ai.models.generateImages({
    model: 'imagen-4.0-generate-001',
    prompt: 'Robot holding a red skateboard',
    config: {
      numberOfImages: 4,
    },
  });

  let idx = 1;
  for (const generatedImage of response.generatedImages) {
    let imgBytes = generatedImage.image.imageBytes;
    const buffer = Buffer.from(imgBytes, "base64");
    fs.writeFileSync(`imagen-${idx}.png`, buffer);
    idx++;
  }
}

main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {

  const ai = new GoogleGenAI({});

  const response = await ai.models.generateImages({
    model: 'imagen-4.0-generate-001',
    prompt: 'Robot holding a red skateboard',
    config: {
      numberOfImages: 4,
    },
  });

  let idx = 1;
  for (const generatedImage of response.generatedImages) {
    let imgBytes = generatedImage.image.imageBytes;
    const buffer = Buffer.from(imgBytes, "base64");
    fs.writeFileSync(`imagen-${idx}.png`, buffer);
    idx++;
  }
}

main();
```

---

## Structured Outputs

**URL:** https://ai.google.dev/gemini-api/docs/structured-output?example=recipe

**Contents:**
- Structured Outputs
  - Python
  - JavaScript
  - Go
  - REST
- Streaming
  - Python
  - JavaScript
- Structured outputs with tools
  - Python

You can configure Gemini models to generate responses that adhere to a provided JSON Schema. This capability guarantees predictable and parsable results, ensures format and type-safety, enables the programmatic detection of refusals, and simplifies prompting.

Using structured outputs is ideal for a wide range of applications:

In addition to supporting JSON Schema in the REST API, the Google GenAI SDKs for Python and JavaScript also make it easy to define object schemas using Pydantic and Zod, respectively. The example below demonstrates how to extract information from unstructured text that conforms to a schema defined in code.

Recipe Extractor Content Moderation Recursive Structures

This example demonstrates how to extract structured data from text using basic JSON Schema types like object, array, string, and integer.

You can stream structured outputs, which allows you to start processing the response as it's being generated, without having to wait for the entire output to be complete. This can improve the perceived performance of your application.

The streamed chunks will be valid partial JSON strings, which can be concatenated to form the final, complete JSON object.

Gemini 3 lets you combine Structured Outputs with built-in tools, including Grounding with Google Search, URL Context, and Code Execution.

To generate a JSON object, set the response_mime_type in the generation configuration to application/json and provide a response_json_schema. The schema must be a valid JSON Schema that describes the desired output format.

The model will then generate a response that is a syntactically valid JSON string matching the provided schema. When using structured outputs, the model will produce outputs in the same order as the keys in the schema.

Gemini's structured output mode supports a subset of the JSON Schema specification.

The following values of type are supported:

These descriptive properties help guide the model:

For number and integer values:

The following models support structured output:

* Note that Gemini 2.0 requires an explicit propertyOrdering list within the JSON input to define the preferred structure. You can find an example in this cookbook.

Both structured outputs and function calling use JSON schemas, but they serve different purposes:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional

class Ingredient(BaseModel):
    name: str = Field(description="Name of the ingredient.")
    quantity: str = Field(description="Quantity of the ingredient, including units.")

class Recipe(BaseModel):
    recipe_name: str = Field(description="The name of the recipe.")
    prep_time_minutes: Optional[int] = Field(description="Optional time in minutes to prepare the recipe.")
    ingredients: List[Ingredient]
    instructions: List[str]

client = genai.Client()

prompt = """
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Recipe.model_json_schema(),
    },
)

recipe = Recipe.model_validate_json(response.text)
print(recipe)
```

Example 2 (python):
```python
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional

class Ingredient(BaseModel):
    name: str = Field(description="Name of the ingredient.")
    quantity: str = Field(description="Quantity of the ingredient, including units.")

class Recipe(BaseModel):
    recipe_name: str = Field(description="The name of the recipe.")
    prep_time_minutes: Optional[int] = Field(description="Optional time in minutes to prepare the recipe.")
    ingredients: List[Ingredient]
    instructions: List[str]

client = genai.Client()

prompt = """
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Recipe.model_json_schema(),
    },
)

recipe = Recipe.model_validate_json(response.text)
print(recipe)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const ingredientSchema = z.object({
  name: z.string().describe("Name of the ingredient."),
  quantity: z.string().describe("Quantity of the ingredient, including units."),
});

const recipeSchema = z.object({
  recipe_name: z.string().describe("The name of the recipe."),
  prep_time_minutes: z.number().optional().describe("Optional time in minutes to prepare the recipe."),
  ingredients: z.array(ingredientSchema),
  instructions: z.array(z.string()),
});

const ai = new GoogleGenAI({});

const prompt = `
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
`;

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: prompt,
  config: {
    responseMimeType: "application/json",
    responseJsonSchema: zodToJsonSchema(recipeSchema),
  },
});

const recipe = recipeSchema.parse(JSON.parse(response.text));
console.log(recipe);
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const ingredientSchema = z.object({
  name: z.string().describe("Name of the ingredient."),
  quantity: z.string().describe("Quantity of the ingredient, including units."),
});

const recipeSchema = z.object({
  recipe_name: z.string().describe("The name of the recipe."),
  prep_time_minutes: z.number().optional().describe("Optional time in minutes to prepare the recipe."),
  ingredients: z.array(ingredientSchema),
  instructions: z.array(z.string()),
});

const ai = new GoogleGenAI({});

const prompt = `
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
`;

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: prompt,
  config: {
    responseMimeType: "application/json",
    responseJsonSchema: zodToJsonSchema(recipeSchema),
  },
});

const recipe = recipeSchema.parse(JSON.parse(response.text));
console.log(recipe);
```

---

## Text generation

**URL:** https://ai.google.dev/gemini-api/docs/system-instructions

**Contents:**
- Text generation
  - Python
  - JavaScript
  - Go
  - Java
  - REST
  - Apps Script
- Thinking with Gemini 2.5
  - Python
  - JavaScript

The Gemini API can generate text output from various inputs, including text, images, video, and audio, leveraging Gemini models.

Here's a basic example that takes a single text input:

2.5 Flash and Pro models have "thinking" enabled by default to enhance quality, which may take longer to run and increase token usage.

When using 2.5 Flash, you can disable thinking by setting the thinking budget to zero.

For more details, see the thinking guide.

You can guide the behavior of Gemini models with system instructions. To do so, pass a GenerateContentConfig object.

The GenerateContentConfig object also lets you override default generation parameters, such as temperature.

Refer to the GenerateContentConfig in our API reference for a complete list of configurable parameters and their descriptions.

The Gemini API supports multimodal inputs, allowing you to combine text with media files. The following example demonstrates providing an image:

For alternative methods of providing images and more advanced image processing, see our image understanding guide. The API also supports document, video, and audio inputs and understanding.

By default, the model returns a response only after the entire generation process is complete.

For more fluid interactions, use streaming to receive GenerateContentResponse instances incrementally as they're generated.

Our SDKs provide functionality to collect multiple rounds of prompts and responses into a chat, giving you an easy way to keep track of the conversation history.

Streaming can also be used for multi-turn conversations.

All models in the Gemini family support text generation. To learn more about the models and their capabilities, visit the Models page.

For basic text generation, a zero-shot prompt often suffices without needing examples, system instructions or specific formatting.

For more tailored outputs:

Consult our prompt engineering guide for more tips.

In some cases, you may need structured output, such as JSON. Refer to our structured output guide to learn how.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "How does AI work?",
  });
  console.log(response.text);
}

await main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "How does AI work?",
  });
  console.log(response.text);
}

await main();
```

---

## Safety settings

**URL:** https://ai.google.dev/gemini-api/docs/safety-settings

**Contents:**
- Safety settings
- Safety filters
  - Content safety filtering level
  - Safety filtering per request
  - Safety feedback
- Adjust safety settings
  - Google AI Studio
  - Gemini API SDKs
  - Python
  - Go

The Gemini API provides safety settings that you can adjust during the prototyping stage to determine if your application requires more or less restrictive safety configuration. You can adjust these settings across five filter categories to restrict or allow certain types of content.

This guide covers how the Gemini API handles safety settings and filtering and how you can change the safety settings for your application.

The Gemini API's adjustable safety filters cover the following categories:

You can use these filters to adjust what's appropriate for your use case. For example, if you're building video game dialogue, you may deem it acceptable to allow more content that's rated as Dangerous due to the nature of the game.

In addition to the adjustable safety filters, the Gemini API has built-in protections against core harms, such as content that endangers child safety. These types of harm are always blocked and cannot be adjusted.

The Gemini API categorizes the probability level of content being unsafe as HIGH, MEDIUM, LOW, or NEGLIGIBLE.

The Gemini API blocks content based on the probability of content being unsafe and not the severity. This is important to consider because some content can have low probability of being unsafe even though the severity of harm could still be high. For example, comparing the sentences:

The first sentence might result in a higher probability of being unsafe, but you might consider the second sentence to be a higher severity in terms of violence. Given this, it is important that you carefully test and consider what the appropriate level of blocking is needed to support your key use cases while minimizing harm to end users.

You can adjust the safety settings for each request you make to the API. When you make a request, the content is analyzed and assigned a safety rating. The safety rating includes the category and the probability of the harm classification. For example, if the content was blocked due to the harassment category having a high probability, the safety rating returned would have category equal to HARASSMENT and harm probability set to HIGH.

By default, safety settings block content (including prompts) with medium or higher probability of being unsafe across any filter. This baseline safety is designed to work for most use cases, so you should only adjust your safety settings if it's consistently required for your application.

The following table describes the block settings you can adjust for each category. For example, if you set the block setting to Block few for the Hate speech category, everything that has a high probability of being hate speech content is blocked. But anything with a lower probability is allowed.

If the threshold is not set, the default block threshold is Block none (for all newer stable GA models) or Block some (in all other models) for all categories except the Civic integrity category.

The default block threshold for the Civic integrity category is Block none (for gemini-2.0-flash, and gemini-2.0-flash-lite) both for Google AI Studio and the Gemini API, and Block most for all other models in Google AI Studio only.

You can set these settings for each request you make to the generative service. See the HarmBlockThreshold API reference for details.

generateContent returns a GenerateContentResponse which includes safety feedback.

Prompt feedback is included in promptFeedback. If promptFeedback.blockReason is set, then the content of the prompt was blocked.

Response candidate feedback is included in Candidate.finishReason and Candidate.safetyRatings. If response content was blocked and the finishReason was SAFETY, you can inspect safetyRatings for more details. The content that was blocked is not returned.

This section covers how to adjust the safety settings in both Google AI Studio and in your code.

You can adjust safety settings in Google AI Studio, but you cannot turn them off.

Click Edit safety settings in the Run settings panel to open the Run safety settings modal. In the modal, you can use the sliders to adjust the content filtering level per safety category:

When you send a request (for example, by asking the model a question), a warning No Content message appears if the request's content is blocked. To see more details, hold the pointer over the No Content text and click warning Safety.

The following code snippet shows how to set safety settings in your GenerateContent call. This sets the thresholds for the harassment (HARM_CATEGORY_HARASSMENT) and hate speech (HARM_CATEGORY_HATE_SPEECH) categories. For example, setting these categories to BLOCK_LOW_AND_ABOVE blocks any content that has a low or higher probability of being harassment or hate speech. To understand the threshold settings, see Safety filtering per request.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-10-08 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

import PIL.Image

img = PIL.Image.open("cookies.jpg")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=['Do these look store-bought or homemade?', img],
    config=types.GenerateContentConfig(
      safety_settings=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
      ]
    )
)

print(response.text)
```

Example 2 (python):
```python
from google import genai
from google.genai import types

import PIL.Image

img = PIL.Image.open("cookies.jpg")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=['Do these look store-bought or homemade?', img],
    config=types.GenerateContentConfig(
      safety_settings=[
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
      ]
    )
)

print(response.text)
```

Example 3 (unknown):
```unknown
package main

import (
    "context"
    "fmt"
    "log"

    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    client, err := genai.NewClient(ctx, nil)
    if err != nil {
        log.Fatal(err)
    }

    config := &genai.GenerateContentConfig{
        SafetySettings: []*genai.SafetySetting{
            {
                Category:  "HARM_CATEGORY_HATE_SPEECH",
                Threshold: "BLOCK_LOW_AND_ABOVE",
            },
        },
    }

    response, err := client.Models.GenerateContent(
        ctx,
        "gemini-2.0-flash",
        genai.Text("Some potentially unsafe prompt."),
        config,
    )
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(response.Text())
}
```

Example 4 (unknown):
```unknown
package main

import (
    "context"
    "fmt"
    "log"

    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    client, err := genai.NewClient(ctx, nil)
    if err != nil {
        log.Fatal(err)
    }

    config := &genai.GenerateContentConfig{
        SafetySettings: []*genai.SafetySetting{
            {
                Category:  "HARM_CATEGORY_HATE_SPEECH",
                Threshold: "BLOCK_LOW_AND_ABOVE",
            },
        },
    }

    response, err := client.Models.GenerateContent(
        ctx,
        "gemini-2.0-flash",
        genai.Text("Some potentially unsafe prompt."),
        config,
    )
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(response.Text())
}
```

---

## Gemini Deep Research Agent

**URL:** https://ai.google.dev/gemini-api/docs/deep-research

**Contents:**
- Gemini Deep Research Agent
  - Python
  - JavaScript
  - REST
- Research with your own data
  - Python
  - JavaScript
  - REST
- Steerability and formatting
  - Python

The Gemini Deep Research Agent autonomously plans, executes, and synthesizes multi-step research tasks. Powered by Gemini 3 Pro, it navigates complex information landscapes using web search and your own data to produce detailed, cited reports.

Research tasks involve iterative searching and reading and can take several minutes to complete. You must use background execution (set background=true) to run the agent asynchronously and poll for results. See Handling long running tasks for more details.

The following example shows how to start a research task in the background and poll for results.

Deep Research has access to a variety of tools. By default, the agent has access to information on the public internet using the google_search and url_context tool. You don't need to specify these tools by default. However, if you additionally want to give the agent access to your own data by using the File Search tool you will need to add it as shown in the following example.

You can steer the agent's output by providing specific formatting instructions in your prompt. This allows you to structure reports into specific sections and subsections, include data tables, or adjust tone for different audiences (e.g., "technical," "executive," "casual").

Define the desired output format explicitly in your input text.

Deep Research is a multi-step process involving planning, searching, reading, and writing. This cycle typically exceeds the standard timeout limits of synchronous API calls.

Agents are required to use background=True. The API returns a partial Interaction object immediately. You can use the id property to retrieve an interaction for polling. The interaction state will transition from in_progress to completed or failed.

Deep Research supports streaming to receive real-time updates on the research progress. You must set stream=True and background=True.

The following example shows how to start a research task and process the stream. Crucially, it demonstrates how to track the interaction_id from the interaction.start event. You will need this ID to resume the stream if a network interruption occurs. This code also introduces an event_id variable which lets you resume from the specific point where you disconnected.

Network interruptions can occur during long-running research tasks. To handle this gracefully, your application should catch connection errors and resume the stream using client.interactions.get().

You must provide two values to resume:

The following examples demonstrate a resilient pattern: attempting to stream the initial create request, and falling back to a get loop if the connection drops.

You can continue the conversation after the agent returns the final report by using the previous_interaction_id. This lets you to ask for clarification, summarization or elaboration on specific sections of the research without restarting the entire task.

Deep Research is an agent, not just a model. It is best suited for workloads that require an "analyst-in-a-box" approach rather than low-latency chat.

Giving an agent access to the web and your private files requires careful consideration of safety risks.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-11 UTC.

**Examples:**

Example 1 (python):
```python
import time
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    input="Research the history of Google TPUs.",
    agent='deep-research-pro-preview-12-2025',
    background=True
)

print(f"Research started: {interaction.id}")

while True:
    interaction = client.interactions.get(interaction.id)
    if interaction.status == "completed":
        print(interaction.outputs[-1].text)
        break
    elif interaction.status == "failed":
        print(f"Research failed: {interaction.error}")
        break
    time.sleep(10)
```

Example 2 (python):
```python
import time
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    input="Research the history of Google TPUs.",
    agent='deep-research-pro-preview-12-2025',
    background=True
)

print(f"Research started: {interaction.id}")

while True:
    interaction = client.interactions.get(interaction.id)
    if interaction.status == "completed":
        print(interaction.outputs[-1].text)
        break
    elif interaction.status == "failed":
        print(f"Research failed: {interaction.error}")
        break
    time.sleep(10)
```

Example 3 (python):
```python
import { GoogleGenAI } from '@google/genai';

const client = new GoogleGenAI({});

const interaction = await client.interactions.create({
    input: 'Research the history of Google TPUs.',
    agent: 'deep-research-pro-preview-12-2025',
    background: true
});

console.log(`Research started: ${interaction.id}`);

while (true) {
    const result = await client.interactions.get(interaction.id);
    if (result.status === 'completed') {
        console.log(result.outputs[result.outputs.length - 1].text);
        break;
    } else if (result.status === 'failed') {
        console.log(`Research failed: ${result.error}`);
        break;
    }
    await new Promise(resolve => setTimeout(resolve, 10000));
}
```

Example 4 (python):
```python
import { GoogleGenAI } from '@google/genai';

const client = new GoogleGenAI({});

const interaction = await client.interactions.create({
    input: 'Research the history of Google TPUs.',
    agent: 'deep-research-pro-preview-12-2025',
    background: true
});

console.log(`Research started: ${interaction.id}`);

while (true) {
    const result = await client.interactions.get(interaction.id);
    if (result.status === 'completed') {
        console.log(result.outputs[result.outputs.length - 1].text);
        break;
    } else if (result.status === 'failed') {
        console.log(`Research failed: ${result.error}`);
        break;
    }
    await new Promise(resolve => setTimeout(resolve, 10000));
}
```

---

## Files API

**URL:** https://ai.google.dev/gemini-api/docs/files

**Contents:**
- Files API
- Upload a file
  - Python
  - JavaScript
  - Go
  - REST
- Get metadata for a file
  - Python
  - JavaScript
  - Go

Gemini can handle various types of input data, including text, images, and audio, at the same time.

This guide shows you how to work with media files using the Files API. The basic operations are the same for audio files, images, videos, documents, and other supported file types.

For file prompting guidance, check out the File prompt guide section.

You can use the Files API to upload a media file. Always use the Files API when the total request size (including the files, text prompt, system instructions, etc.) is larger than 20 MB.

The following code uploads a file and then uses the file in a call to generateContent.

You can verify that the API successfully stored the uploaded file and get its metadata by calling files.get.

The following code gets a list of all the files uploaded:

Files are automatically deleted after 48 hours. You can also manually delete an uploaded file:

You can use the Files API to upload and interact with media files. The Files API lets you store up to 20 GB of files per project, with a per-file maximum size of 2 GB. Files are stored for 48 hours. During that time, you can use the API to get metadata about the files, but you can't download the files. The Files API is available at no cost in all regions where the Gemini API is available.

This section provides guidance and best practices for using media files with prompts for the Gemini API.

Being able to use various types of data in your prompts gives you more flexibility in terms of what tasks you can tackle with the Gemini API. For example, you can send the model a photo of a delicious meal and ask it to write a short blog about the meal.

Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.

Meal prepping is a great way to save time and money, and it can also help you to eat healthier. This meal is a great example of a healthy and delicious meal that can be easily prepped ahead of time.

This meal features brown rice, roasted vegetables, and chicken teriyaki. The brown rice is a healthy and complex carbohydrate that will give you sustained energy. The roasted vegetables are a great way to get your daily dose of vitamins and minerals, and the chicken teriyaki is a delicious and protein-rich option.

This meal is also very easy to prepare. Simply cook the brown rice, roast the vegetables, and cook the chicken teriyaki. Once everything is cooked, divide it into meal prep containers and store them in the refrigerator. You can then grab a container and go on busy mornings!

If you're looking for a healthy and delicious meal that can be easily prepped ahead of time, this meal is a great option. It's packed with nutrients and flavor, and it's sure to keep you feeling full and satisfied.

Here's to healthy and delicious meal prepping!

If you are having trouble getting the output you want from prompts that use media files, there are some strategies that can help you get the results you want. The following sections provide design approaches and troubleshooting tips for improving prompts that use multimodal input.

You can improve your multimodal prompts by following these best practices:

Prompts have the most success when they are clear and detailed. If you have a specific output in mind, it's better to include that requirement in the prompt to ensure you get the output you want.

For this image of an airport board, asking the model to just "describe this image" could generate a general description. If you need the model to parse the time and city from the image, you can include that request directly in your prompt.

The image shows an airport arrivals and departures board.

Updated prompt Improved response Parse the time and city from the airport board shown in this image into a list. 10:50 Moscow 11:05 Edinburgh 11:05 London 11:10 Bucharest 11:30 Kiev 11:35 Dublin 11:45 East Midlands 12:15 Sofia 12:30 London 12:30 Newcastle 12:40 St Petersburg 12:40 London 12:45 Manchester

Parse the time and city from the airport board shown in this image into a list.

10:50 Moscow 11:05 Edinburgh 11:05 London 11:10 Bucharest 11:30 Kiev 11:35 Dublin 11:45 East Midlands 12:15 Sofia 12:30 London 12:30 Newcastle 12:40 St Petersburg 12:40 London 12:45 Manchester

The Gemini model can accept multiple inputs which it can use as examples to understand the output you want. Adding these examples can help the model identify the patterns and apply the relationship between the given images and responses to the new example. This is also called "few-shot" learning.

In the example below, the initial output is written in sentence form, and also contains the country (Brazil). Suppose you want the output in a different format or style, and you want only the city, not the country. Adding few-shot examples to your prompt can steer the model to respond in the way you want.

Prompt Model response Determine the city along with the landmark. The landmark is the Christ the Redeemer statue in Rio de Janeiro, Brazil.

Determine the city along with the landmark.

The landmark is the Christ the Redeemer statue in Rio de Janeiro, Brazil.

Determine the city along with the landmark.

city: Rome, landmark: the Colosseum.

city: Beijing, landmark: Forbidden City

city: Rio de Janeiro, landmark: Christ the Redeemer statue

For complex tasks like the ones that require both visual understanding and reasoning, it can be helpful to split the task into smaller, more straightforward steps. Alternatively, it could also be effective if you directly ask the model to “think step by step” in your prompt.

When will I run out of toilet paper?

Soon, you only have 3 rolls left.

1. First, count how many toilet paper rolls are in this picture. 2. Then, determine how much toilet paper a typical person uses per day. 3. Calculate how long these rolls of toilet paper will last.

1. There are 3 rolls of toilet paper in this picture. 2. A typical person uses about 20 sheets of toilet paper per day. 3. If each roll contains 200 sheets, then each roll will last for about 10 days. Therefore, the 3 rolls will last for about a month.

Math problems or other types of word problems are great candidates for asking the model to think step-by-step.

What is the 4th term in the sequence?

What is the 4th term in the sequence?

The response from the model is incorrect. Some ways to improve this is to ask the model to parse the problem before answering the prompt.

Parse the formula in the image first. Then based on the formula, answer "what's the 4th term in the sequence?".

Parse the formula in the image first.

Then based on the formula, answer "what's the 4th term in the sequence?".

Click to expand the result $$ b(n) = b(n-1) * (-3) $$ $$ b(1) = 15 $$ Substitute n = 4 into the formula: $$ b(4) = b(4-1) * (-3) $$ $$ b(4) = b(3) * (-3) $$ We don't know the value of b(3), so substitute n = 3 into the formula: $$ b(3) = b(3-1) * (-3) $$ $$ b(3) = b(2) * (-3) $$ We don't know the value of b(2), so substitute n = 2 into the formula: $$ b(2) = b(2-1) * (-3) $$ $$ b(2) = b(1) * (-3) $$ We know the value of b(1) is 15, so substitute it into the formula: $$ b(2) = 15 * (-3) $$ $$ b(2) = -45 $$ Now that we know the value of b(2), substitute it into the formula for b(3): $$ b(3) = b(2) * (-3) $$ $$ b(3) = -45 * (-3) $$ $$ b(3) = 135 $$ Now that we know the value of b(3), substitute it into the formula for b(4): $$ b(4) = b(3) * (-3) $$ $$ b(4) = 135 * (-3) $$ $$ b(4) = -405 $$ Therefore, the 4th term in the sequence is -405.

$$ b(n) = b(n-1) * (-3) $$

$$ b(4) = b(4-1) * (-3) $$

$$ b(4) = b(3) * (-3) $$

$$ b(3) = b(3-1) * (-3) $$

$$ b(3) = b(2) * (-3) $$

$$ b(2) = b(2-1) * (-3) $$

$$ b(2) = b(1) * (-3) $$

$$ b(2) = 15 * (-3) $$

$$ b(3) = b(2) * (-3) $$

$$ b(3) = -45 * (-3) $$

$$ b(4) = b(3) * (-3) $$

$$ b(4) = 135 * (-3) $$

Therefore, the 4th term in the sequence is -405.

This model response is correct - now to make the response even more streamlined, you can ask the model to to think step-by-step.

Updated prompt Improved response What is the 4th term in the sequence? Think step by step. The first term is 15. The second term is b(1) * (-3) = 15 * (-3) = -45. The third term is b(2) * (-3) = -45 * (-3) = 135. The fourth term is b(3) * (-3) = 135 * (-3) = -405.

What is the 4th term in the sequence? Think step by step.

The first term is 15.

The second term is b(1) * (-3) = 15 * (-3) = -45.

The third term is b(2) * (-3) = -45 * (-3) = 135.

The fourth term is b(3) * (-3) = 135 * (-3) = -405.

A common problem is the need for model output to be in a certain format (e.g. markdown, JSON, HTML), especially if the model output needs to be ingested by a downstream task. You can try to produce output in that format by instructing the model to do so within the prompt. Below are two examples:

Parse the table in this image into markdown format

| Subject | Status | Time | Start date | Due on |

| ------- | ------ | ---- | ---------- | ------ |

| Math | Done | 1.5 hrs | 11/29/2023 | 12/1/2023 |

| Geography | Done | 30 min | 12/2/2023 | 12/4/2023 |

| Physics | In progress | 2 hrs | 12/3/2023 | 12/5/2023 |

| Biology | Not started | 6 hrs | 11/2/2016 | 12/6/2023 |

Provide a list of all the following attributes:

ingredients, type of cuisine, vegetarian or not, in JSON format

```json { "ingredients": [ "rice", "shrimp", "clams", "mussels", "peas", "tomatoes", "onions", "garlic", "olive oil", "paprika", "salt", "pepper" ], "type of cuisine": "Spanish", "vegetarian": false } ```

"type of cuisine": "Spanish",

While Gemini can interpret image and text in any order within a prompt, placing a single image before the text prompt might lead to better results. In the following samples, you'll notice the image comes first before the text in each prompt.

You might need to troubleshoot your prompt if you are not getting a helpful response. Here are a few strategies you could try.

To get a more specific response, you can point out which aspects of the image you want the prompt to draw information from to inform its response.

How many days will these diapers last a baby?

The diapers will last for 198 days before they run out.

How long will these diapers last before I run out?

Use the weight shown on the box to determine the child's age, and use the total number of diapers in the box.

Divide the total number by how many diapers the child goes through per day.

The box contains 198 diapers. The box states the diapers are for a child weighing 22-37 lbs.

The average child in this weight range is likely between 1 and 2 years old.

A 2-year-old typically goes through 6 diapers per day, therefore, the diapers will last around 33 days (198/6).

To help the model tailor its response to the image(s), try asking it to describe the images before performing its reasoning task.

What is in common between these images?

All four images are examples of landscape photography.

First, describe what's in each image in detail. What's in common between these images?

The first image shows a person packing a suitcase. The second image shows an empty hallway in a shopping mall. The third image shows a roll of toilet paper. The fourth image shows a dark and stormy sea.

The commonality between these images is that they are all examples of liminal spaces. Liminal spaces are places or situations that are in between two other places or situations. They are often characterized by a sense of uncertainty or ambiguity.

The first image shows the person in between being at home and being on a trip. The second image shows the hallway in between two stores. The third image is of toilet paper, which can represent a bathroom. A bathroom is a transitional space between private and public realms. It's a place where we prepare ourselves to enter or leave the outside world.

The fourth image shows the sea in between being calm and being stormy.

Liminal spaces can be both exciting and unsettling. They can be a place of new beginning or a place of endings. They can be a place of reflection or a place of action.

You can also try explicitly asking the model to refer to what's in the image.

What is in common between these images? Refer to what's in the images in your response.

All of the images are related to travel. The first image shows a person packing a suitcase, the second image shows an empty hallway in a shopping mall, the third image shows a stack of toilet paper, and the fourth image shows a dark and stormy sea.

These images are all related to travel because they are all things that people need or use when they travel. The first image shows a person packing a suitcase, which is something that people do when they are going on a trip. The second image shows an empty hallway in a shopping mall, which is a place where people often go to buy things for their trips. The third image shows a stack of toilet paper, which is something that people often use when they are traveling. The fourth image shows a dark and stormy sea, which is something that people often encounter when they are traveling.

The same tips work for creative output from images. In the following example with the rabbit, explicitly asking the model to include aspects from the image can improve the output.

Can you write me a poem about this image?

Little bunny, so soft and brown, Hopping through the field, up and down. Your ears so long, your tail so small, You're the cutest creature of them all.

You nibble on the grass, so green and sweet, And hop away when you see me. But I'll always be your friend, Little bunny, until the very end.

Updated prompt Improved response Can you write me a descriptive and dramatic poem about this image and include the location? Little bunny on the green, Ears so long, so keen. What do you see out there, In the distance, where you stare? Is it the ocean blue, Sparkling in the sun's hue? Or the waves that crash and roar, A rhythm that you adore? Little bunny, tell me true, What captures your attention so? Is it the salty breeze, Or the seagulls' cries that please? Perhaps it's the vastness of it all, A world so big and small. A place where dreams can roam, And adventures can be sown. Little bunny, I wonder what you dream, As you sit on the grass, so serene. Do you yearn to explore the deep, Or stay on land, where you can leap? Whatever it may be, little bunny, Keep that spark of wonder burning brightly. For in your dreams and aspirations, Lies a world waiting for your creation.

Can you write me a descriptive and dramatic poem about this image and include the location?

Little bunny on the green, Ears so long, so keen. What do you see out there, In the distance, where you stare?

Is it the ocean blue, Sparkling in the sun's hue? Or the waves that crash and roar, A rhythm that you adore?

Little bunny, tell me true, What captures your attention so? Is it the salty breeze, Or the seagulls' cries that please?

Perhaps it's the vastness of it all, A world so big and small. A place where dreams can roam, And adventures can be sown.

Little bunny, I wonder what you dream, As you sit on the grass, so serene. Do you yearn to explore the deep, Or stay on land, where you can leap?

Whatever it may be, little bunny, Keep that spark of wonder burning brightly. For in your dreams and aspirations, Lies a world waiting for your creation.

It can be hard to know whether a prompt failed because the model didn't understand the image to begin with, or if it did understand the image but did not perform the correct reasoning steps afterward. To disambiguate between those reasons, ask the model to describe what's in the image.

In the following example, if the model responds with a snack that seems surprising when paired with tea (e.g. popcorn), you can first troubleshoot to determine whether the model correctly recognized that the image contains tea.

What's a snack I can make in 1 minute that would go well with this?

Describe what's in this image.

Another strategy is to ask the model to explain its reasoning. That can help you narrow down which part of the reasoning broke down, if any.

What's a snack I can make in 1 minute that would go well with this?

What's a snack I can make in 1 minute that would go well with this? Please explain why.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-08 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp3")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=["Describe this audio clip", myfile]
)

print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp3")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=["Describe this audio clip", myfile]
)

print(response.text)
```

Example 3 (python):
```python
import {
  GoogleGenAI,
  createUserContent,
  createPartFromUri,
} from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const myfile = await ai.files.upload({
    file: "path/to/sample.mp3",
    config: { mimeType: "audio/mpeg" },
  });

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: createUserContent([
      createPartFromUri(myfile.uri, myfile.mimeType),
      "Describe this audio clip",
    ]),
  });
  console.log(response.text);
}

await main();
```

Example 4 (python):
```python
import {
  GoogleGenAI,
  createUserContent,
  createPartFromUri,
} from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const myfile = await ai.files.upload({
    file: "path/to/sample.mp3",
    config: { mimeType: "audio/mpeg" },
  });

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: createUserContent([
      createPartFromUri(myfile.uri, myfile.mimeType),
      "Describe this audio clip",
    ]),
  });
  console.log(response.text);
}

await main();
```

---

## Additional usage policies

**URL:** https://ai.google.dev/gemini-api/docs/usage-policies

**Contents:**
- Additional usage policies
- Abuse monitoring
  - How We Monitor for Misuse
  - How We Handle Data
  - How We Investigate Potential Issues
  - Working with You on Policy Compliance
  - Scope
- Inline Preference Voting
  - Why are we doing this?
  - What data is included in Feedback?

This page includes additional usage policies for the Gemini API.

Google is committed to the responsible development and use of AI. To ensure the safety and integrity of the Gemini API, we have created these policy guidelines. By using the Gemini API, you agree to the following guidelines, the Gemini API Additional Terms of Service and Generative AI Prohibited Use Policy.

Google's Trust and Safety Team employs a combination of automated and manual processes to detect potential misuse of the Gemini API and enforce our policies.

To help with abuse monitoring, Google retains the following data for fifty-five (55) days:

When prompts or model outputs are flagged by safety filters and abuse detection systems described above, authorized Google employees may assess the flagged content, and either confirm or correct the classification or determination based on predefined guidelines and policies. Data can be accessed for human review only by authorized Google employees via an internal governance assessment and review management platform. When data is logged for abuse monitoring, it is used solely for the purpose of policy enforcement and is not used to train or fine-tune any AI/ML models.

If your use of Gemini doesn't align with our policies, we may take the following steps:

These policy guidelines apply to the use of the Gemini API and AI Studio.

In Google AI Studio, you might occasionally see a side-by-side comparison of two different responses to your prompt. This is part of our Inline Preference Voting system. You'll be asked to choose which response you prefer. This helps us understand which model outputs users find most helpful.

We're constantly working to improve our AI models and services. Your feedback through Inline Preference Voting helps us provide, improve, and develop Google products and services and machine learning technologies, including Google's enterprise features, products and services, consistent with the Gemini API Additional Terms of Service and Privacy Policy.

To make informed decisions about our models, we collect certain data when you participate in Inline Preference Voting:

We take your privacy seriously. Google takes steps to protect your privacy as part of this process. This includes disconnecting this data from your Google Account, API key, and Cloud project before reviewers see or annotate it. Do not submit feedback on conversations that include sensitive, confidential, or personal information.

You'll have the option to skip the Inline Preference Voting when it appears.

Thank you for helping us improve Google AI Studio!

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

---

## Function calling with the Gemini API

**URL:** https://ai.google.dev/gemini-api/docs/function-calling/tutorial

**Contents:**
- Function calling with the Gemini API
  - Python
  - JavaScript
  - REST
- How function calling works
  - Step 1: Define a function declaration
  - Python
  - JavaScript
  - Step 2: Call the model with function declarations
  - Python

Function calling lets you connect models to external tools and APIs. Instead of generating text responses, the model determines when to call specific functions and provides the necessary parameters to execute real-world actions. This allows the model to act as a bridge between natural language and real-world actions and data. Function calling has 3 primary use cases:

Get Weather Schedule Meeting Create Chart

Function calling involves a structured interaction between your application, the model, and external functions. Here's a breakdown of the process:

This process can be repeated over multiple turns, allowing for complex interactions and workflows. The model also supports calling multiple functions in a single turn (parallel function calling) and in sequence (compositional function calling).

Define a function and its declaration within your application code that allows users to set light values and make an API request. This function could call external services or APIs.

Once you have defined your function declarations, you can prompt the model to use them. It analyzes the prompt and function declarations and decides whether to respond directly or to call a function. If a function is called, the response object will contain a function call suggestion.

The model then returns a functionCall object in an OpenAPI compatible schema specifying how to call one or more of the declared functions in order to respond to the user's question.

Extract the function call details from the model's response, parse the arguments , and execute the set_light_values function.

Finally, send the result of the function execution back to the model so it can incorporate this information into its final response to the user.

This completes the function calling flow. The model successfully used the set_light_values function to perform the request action of the user.

When you implement function calling in a prompt, you create a tools object, which contains one or more function declarations. You define functions using JSON, specifically with a select subset of the OpenAPI schema format. A single function declaration can include the following parameters:

You can also construct FunctionDeclarations from Python functions directly using types.FunctionDeclaration.from_callable(client=client, callable=your_function).

Gemini 3 and 2.5 series models use an internal "thinking" process to reason through requests. This significantly improves function calling performance, allowing the model to better determine when to call a function and which parameters to use. Because the Gemini API is stateless, models use thought signatures to maintain context across multi-turn conversations.

This section covers advanced management of thought signatures and is only necessary if you're manually constructing API requests (e.g., via REST) or manipulating conversation history.

If you're using the Google GenAI SDKs (our official libraries), you don't need to manage this process. The SDKs automatically handle the necessary steps, as shown in the earlier example.

If you modify the conversation history manually, instead of sending the complete previous response you must correctly handle the thought_signature included in the model's turn.

Follow these rules to ensure the model's context is preserved:

In Gemini 3, any Part of a model response may contain a thought signature. While we generally recommend returning signatures from all Part types, passing back thought signatures is mandatory for function calling. Unless you are manipulating conversation history manually, the Google GenAI SDK will handle thought signatures automatically.

If you are manipulating conversation history manually, refer to the Thoughts Signatures page for complete guidance and details on handling thought signatures for Gemini 3.

While not necessary for implementation, you can inspect the response to see the thought_signature for debugging or educational purposes.

Learn more about limitations and usage of thought signatures, and about thinking models in general, on the Thinking page.

In addition to single turn function calling, you can also call multiple functions at once. Parallel function calling lets you execute multiple functions at once and is used when the functions are not dependent on each other. This is useful in scenarios like gathering data from multiple independent sources, such as retrieving customer details from different databases or checking inventory levels across various warehouses or performing multiple actions such as converting your apartment into a disco.

Configure the function calling mode to allow using all of the specified tools. To learn more, you can read about configuring function calling.

Each of the printed results reflects a single function call that the model has requested. To send the results back, include the responses in the same order as they were requested.

The Python SDK supports automatic function calling, which automatically converts Python functions to declarations, handles the function call execution and response cycle for you. Following is an example for the disco use case.

Compositional or sequential function calling allows Gemini to chain multiple function calls together to fulfill a complex request. For example, to answer "Get the temperature in my current location", the Gemini API might first invoke a get_current_location() function followed by a get_weather() function that takes the location as a parameter.

The following example demonstrates how to implement compositional function calling using the Python SDK and automatic function calling.

This example uses the automatic function calling feature of the google-genai Python SDK. The SDK automatically converts the Python functions to the required schema, executes the function calls when requested by the model, and sends the results back to the model to complete the task.

When you run the code, you will see the SDK orchestrating the function calls. The model first calls get_weather_forecast, receives the temperature, and then calls set_thermostat_temperature with the correct value based on the logic in the prompt.

This example shows how to use JavaScript/TypeScript SDK to do comopositional function calling using a manual execution loop.

When you run the code, you will see the SDK orchestrating the function calls. The model first calls get_weather_forecast, receives the temperature, and then calls set_thermostat_temperature with the correct value based on the logic in the prompt.

Compositional function calling is a native Live API feature. This means Live API can handle the function calling similar to the Python SDK.

The Gemini API lets you control how the model uses the provided tools (function declarations). Specifically, you can set the mode within the.function_calling_config.

VALIDATED (Preview): The model is constrained to predict either function calls or natural language, and ensures function schema adherence. If allowed_function_names is not provided, the model picks from all of the available function declarations. If allowed_function_names is provided, the model picks from the set of allowed functions.

When using the Python SDK, you can provide Python functions directly as tools. The SDK converts these functions into declarations, manages the function call execution, and handles the response cycle for you. Define your function with type hints and a docstring. For optimal results, it is recommended to use Google-style docstrings. The SDK will then automatically:

The SDK currently does not parse argument descriptions into the property description slots of the generated function declaration. Instead, it sends the entire docstring as the top-level function description.

You can disable automatic function calling with:

The API is able to describe any of the following types. Pydantic types are allowed, as long as the fields defined on them are also composed of allowed types. Dict types (like dict[str: int]) are not well supported here, don't use them.

To see what the inferred schema looks like, you can convert it using from_callable:

You can enable multiple tools combining native tools with function calling at the same time. Here's an example that enables two tools, Grounding with Google Search and code execution, in a request using the Live API.

Python developers can try this out in the Live API Tool Use notebook.

For Gemini 3 series models, you can include multimodal content in the function response parts that you send to the model. The model can process this multimodal content in its next turn to produce a more informed response. The following MIME types are supported for multimodal content in function responses:

To include multimodal data in a function response, include it as one or more parts nested within the functionResponse part. Each multimodal part must contain inlineData. If you reference a multimodal part from within the structured response field, it must contain a unique displayName.

You can also reference a multimodal part from within the structured response field of the functionResponse part by using the JSON reference format {"$ref": "<displayName>"}. The model substitutes the reference with the multimodal content when processing the response. Each displayName can only be referenced once in the structured response field.

The following example shows a message containing a functionResponse for a function named get_image and a nested part containing image data with displayName: "wakeupcat.jpg". The functionResponse's response field references this image part:

Model Context Protocol (MCP) is an open standard for connecting AI applications with external tools and data. MCP provides a common protocol for models to access context, such as functions (tools), data sources (resources), or predefined prompts.

The Gemini SDKs have built-in support for the MCP, reducing boilerplate code and offering automatic tool calling for MCP tools. When the model generates an MCP tool call, the Python and JavaScript client SDK can automatically execute the MCP tool and send the response back to the model in a subsequent request, continuing this loop until no more tool calls are made by the model.

Here, you can find an example of how to use a local MCP server with Gemini and mcp SDK.

Make sure the latest version of the mcp SDK is installed on your platform of choice.

Make sure the latest version of the mcp SDK is installed on your platform of choice.

Built-in MCP support is a experimental feature in our SDKs and has the following limitations:

Manual integration of MCP servers is always an option if these limit what you're building.

This section lists models and their function calling capabilities. Experimental models are not included. You can find a comprehensive capabilities overview on the model overview page.

Temperature: Use a low temperature (e.g., 0) for more deterministic and reliable function calls.

Validation: If a function call has significant consequences (e.g., placing an order), validate the call with the user before executing it.

Check Finish Reason: Always check the finishReason in the model's response to handle cases where the model failed to generate a valid function call.

Error Handling: Implement robust error handling in your functions to gracefully handle unexpected inputs or API failures. Return informative error messages that the model can use to generate helpful responses to the user.

Security: Be mindful of security when calling external APIs. Use appropriate authentication and authorization mechanisms. Avoid exposing sensitive data in function calls.

Token Limits: Function descriptions and parameters count towards your input token limit. If you're hitting token limits, consider limiting the number of functions or the length of the descriptions, break down complex tasks into smaller, more focused function sets.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

# Define the function declaration for the model
schedule_meeting_function = {
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees at a given time and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of people attending the meeting.",
            },
            "date": {
                "type": "string",
                "description": "Date of the meeting (e.g., '2024-07-29')",
            },
            "time": {
                "type": "string",
                "description": "Time of the meeting (e.g., '15:00')",
            },
            "topic": {
                "type": "string",
                "description": "The subject or topic of the meeting.",
            },
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}

# Configure the client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[schedule_meeting_function])
config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about the Q3 planning.",
    config=config,
)

# Check for a function call
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    #  In a real app, you would call your function here:
    #  result = schedule_meeting(**function_call.args)
else:
    print("No function call found in the response.")
    print(response.text)
```

Example 2 (python):
```python
from google import genai
from google.genai import types

# Define the function declaration for the model
schedule_meeting_function = {
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees at a given time and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of people attending the meeting.",
            },
            "date": {
                "type": "string",
                "description": "Date of the meeting (e.g., '2024-07-29')",
            },
            "time": {
                "type": "string",
                "description": "Time of the meeting (e.g., '15:00')",
            },
            "topic": {
                "type": "string",
                "description": "The subject or topic of the meeting.",
            },
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}

# Configure the client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[schedule_meeting_function])
config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about the Q3 planning.",
    config=config,
)

# Check for a function call
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    #  In a real app, you would call your function here:
    #  result = schedule_meeting(**function_call.args)
else:
    print("No function call found in the response.")
    print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI, Type } from '@google/genai';

// Configure the client
const ai = new GoogleGenAI({});

// Define the function declaration for the model
const scheduleMeetingFunctionDeclaration = {
  name: 'schedule_meeting',
  description: 'Schedules a meeting with specified attendees at a given time and date.',
  parameters: {
    type: Type.OBJECT,
    properties: {
      attendees: {
        type: Type.ARRAY,
        items: { type: Type.STRING },
        description: 'List of people attending the meeting.',
      },
      date: {
        type: Type.STRING,
        description: 'Date of the meeting (e.g., "2024-07-29")',
      },
      time: {
        type: Type.STRING,
        description: 'Time of the meeting (e.g., "15:00")',
      },
      topic: {
        type: Type.STRING,
        description: 'The subject or topic of the meeting.',
      },
    },
    required: ['attendees', 'date', 'time', 'topic'],
  },
};

// Send request with function declarations
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Schedule a meeting with Bob and Alice for 03/27/2025 at 10:00 AM about the Q3 planning.',
  config: {
    tools: [{
      functionDeclarations: [scheduleMeetingFunctionDeclaration]
    }],
  },
});

// Check for function calls in the response
if (response.functionCalls && response.functionCalls.length > 0) {
  const functionCall = response.functionCalls[0]; // Assuming one function call
  console.log(`Function to call: ${functionCall.name}`);
  console.log(`Arguments: ${JSON.stringify(functionCall.args)}`);
  // In a real app, you would call your actual function here:
  // const result = await scheduleMeeting(functionCall.args);
} else {
  console.log("No function call found in the response.");
  console.log(response.text);
}
```

Example 4 (python):
```python
import { GoogleGenAI, Type } from '@google/genai';

// Configure the client
const ai = new GoogleGenAI({});

// Define the function declaration for the model
const scheduleMeetingFunctionDeclaration = {
  name: 'schedule_meeting',
  description: 'Schedules a meeting with specified attendees at a given time and date.',
  parameters: {
    type: Type.OBJECT,
    properties: {
      attendees: {
        type: Type.ARRAY,
        items: { type: Type.STRING },
        description: 'List of people attending the meeting.',
      },
      date: {
        type: Type.STRING,
        description: 'Date of the meeting (e.g., "2024-07-29")',
      },
      time: {
        type: Type.STRING,
        description: 'Time of the meeting (e.g., "15:00")',
      },
      topic: {
        type: Type.STRING,
        description: 'The subject or topic of the meeting.',
      },
    },
    required: ['attendees', 'date', 'time', 'topic'],
  },
};

// Send request with function declarations
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Schedule a meeting with Bob and Alice for 03/27/2025 at 10:00 AM about the Q3 planning.',
  config: {
    tools: [{
      functionDeclarations: [scheduleMeetingFunctionDeclaration]
    }],
  },
});

// Check for function calls in the response
if (response.functionCalls && response.functionCalls.length > 0) {
  const functionCall = response.functionCalls[0]; // Assuming one function call
  console.log(`Function to call: ${functionCall.name}`);
  console.log(`Arguments: ${JSON.stringify(functionCall.args)}`);
  // In a real app, you would call your actual function here:
  // const result = await scheduleMeeting(functionCall.args);
} else {
  console.log("No function call found in the response.");
  console.log(response.text);
}
```

---

## Prompt design strategies

**URL:** https://ai.google.dev/gemini-api/docs/prompting-strategies

**Contents:**
- Prompt design strategies
- Topic-specific prompt guides
- Clear and specific instructions
  - Input
    - Partial input completion
  - Constraints
  - Response format
    - Format responses with the completion strategy
- Zero-shot vs few-shot prompts
  - Optimal number of examples

Prompt design is the process of creating prompts, or natural language requests, that elicit accurate, high quality responses from a language model.

This page introduces basic concepts, strategies, and best practices to get you started designing prompts to get the most out of Gemini AI models.

Looking for more specific prompt strategies? Check out our other prompting guides on:

You can find other sample prompts in the prompt gallery meant to interactively showcase many of the concepts shared in this guide.

An effective and efficient way to customize model behavior is to provide it with clear and specific instructions. Instructions can be in the form of a question, step-by-step tasks, or as complex as mapping out a user's experience and mindset.

Input is the required text in the prompt that you want the model to provide a response to. Inputs can be a question that the model answers (question input), a task the model performs (task input), an entity the model operates on (entity input), or partial input that the model completes or continues (completion input).

Generative language models work like an advanced auto completion tool. When you provide partial content, the model can provide the rest of the content or what it thinks is a continuation of that content as a response. When doing so, if you include any examples or context, the model can take those examples or context into account.

The following example provides a prompt with an instruction and an entity input:

While the model did as prompted, writing out the instructions in natural language can sometimes be challenging and it leaves a lot to the model's interpretation. For example, a restaurants menu might contain many items. To reduce the size of the JSON response, you probably want to omit the items that weren't ordered. In this case, you can give an example and a response prefix and let the model complete it:

Notice how "cheeseburger" was excluded from the output because it wasn't a part of the order.

Specify any constraints on reading the prompt or generating a response. You can tell the model what to do and not to do. For example, you can specify a constraint in the prompt on how long you want a summary to be:

Prompt: Summarize this text in one sentence: Text: A quantum computer exploits quantum mechanical phenomena to perform calculations exponentially faster than any modern traditional computer. At very tiny scales, physical matter acts as both particles and as waves, and quantum computing uses specialized hardware to leverage this behavior. The operating principles of quantum devices is beyond the scope of classical physics. When deployed at scale, quantum computers could be used in a wide variety of applications such as: in cybersecurity to break existing encryption methods while helping researchers create new ones, in meteorology to develop better weather forecasting etc. However, the current state of the art quantum computers are still largely experimental and impractical.

Response: Exploiting quantum mechanical phenomena, quantum computers can perform calculations exponentially faster than traditional computers for potential applications like cybersecurity and meteorology, although they are currently largely experimental and impractical. (gemini-2.5-flash)

You can give instructions that specify the format of the response. For example, you can ask for the response to be formatted as a table, bulleted list, elevator pitch, keywords, sentence, or paragraph. The following system instruction tells the model to be more conversational in its response:

The completion strategy can also help format the response. The following example prompts the model to create an essay outline:

The prompt didn't specify the format for the outline and the model chose a format for you. To get the model to return an outline in a specific format, you can add text that represents the start of the outline and let the model complete it based on the pattern that you initiated.

You can include examples in the prompt that show the model what getting it right looks like. The model attempts to identify patterns and relationships from the examples and applies them when generating a response. Prompts that contain a few examples are called few-shot prompts, while prompts that provide no examples are called zero-shot prompts. Few-shot prompts are often used to regulate the formatting, phrasing, scoping, or general patterning of model responses. Use specific and varied examples to help the model narrow its focus and generate more accurate results.

We recommend to always include few-shot examples in your prompts. Prompts without few-shot examples are likely to be less effective. In fact, you can remove instructions from your prompt if your examples are clear enough in showing the task at hand.

The following zero-shot prompt asks the model to choose the best explanation.

If your use case requires the model to produce concise responses, you can include examples in the prompt that give preference to concise responses.

The following prompt provides two examples that show preference to the shorter explanations. In the response, you can see that the examples guided the model to choose the shorter explanation (Explanation2) as opposed to the longer explanation (Explanation1) like it did previously.

Models like Gemini can often pick up on patterns using a few examples, though you may need to experiment with the number of examples to provide in the prompt for the best results. At the same time, if you include too many examples, the model may start to overfit the response to the examples.

Using examples to show the model a pattern to follow is more effective than using examples to show the model an anti pattern to avoid.

Make sure that the structure and formatting of few-shot examples are the same to avoid responses with undesired formats. One of the primary objectives of adding few-shot examples in prompts is to show the model the response format. Therefore, it is essential to ensure a consistent format across all examples, especially paying attention to XML tags, white spaces, newlines, and example splitters.

You can include instructions and information in a prompt that the model needs to solve a problem, instead of assuming that the model has all of the required information. This contextual information helps the model understand the constraints and details of what you're asking for it to do.

The following example asks the model to give troubleshooting guidance for a router:

The response looks like generic troubleshooting information that's not specific to the router or the status of the LED indicator lights.

To customize the response for the specific router, you can add to the prompt the router's troubleshooting guide as context for it to refer to when providing a response.

A prefix is a word or phrase that you add to the prompt content that can serve several purposes, depending on where you put the prefix:

In the following example, "Text:" is the input prefix and "The answer is:" is the output prefix.

For use cases that require complex prompts, you can help the model manage this complexity by breaking things down into simpler components.

Break down instructions: Instead of having many instructions in one prompt, create one prompt per instruction. You can choose which prompt to process based on the user's input.

Chain prompts: For complex tasks that involve multiple sequential steps, make each step a prompt and chain the prompts together in a sequence. In this sequential chain of prompts, the output of one prompt in the sequence becomes the input of the next prompt. The output of the last prompt in the sequence is the final output.

Aggregate responses: Aggregation is when you want to perform different parallel tasks on different portions of the data and aggregate the results to produce the final output. For example, you can tell the model to perform one operation on the first part of the data, perform another operation on the rest of the data and aggregate the results.

Each call that you send to a model includes parameter values that control how the model generates a response. The model can generate different results for different parameter values. Experiment with different parameter values to get the best values for the task. The parameters available for different models may differ. The most common parameters are the following:

Max output tokens: Specifies the maximum number of tokens that can be generated in the response. A token is approximately four characters. 100 tokens correspond to roughly 60-80 words.

Temperature: The temperature controls the degree of randomness in token selection. The temperature is used for sampling during response generation, which occurs when topP and topK are applied. Lower temperatures are good for prompts that require a more deterministic or less open-ended response, while higher temperatures can lead to more diverse or creative results. A temperature of 0 is deterministic, meaning that the highest probability response is always selected.

topK: The topK parameter changes how the model selects tokens for output. A topK of 1 means the selected token is the most probable among all the tokens in the model's vocabulary (also called greedy decoding), while a topK of 3 means that the next token is selected from among the 3 most probable using the temperature. For each token selection step, the topK tokens with the highest probabilities are sampled. Tokens are then further filtered based on topP with the final token selected using temperature sampling.

topP: The topP parameter changes how the model selects tokens for output. Tokens are selected from the most to least probable until the sum of their probabilities equals the topP value. For example, if tokens A, B, and C have a probability of 0.3, 0.2, and 0.1 and the topP value is 0.5, then the model will select either A or B as the next token by using the temperature and exclude C as a candidate. The default topP value is 0.95.

stop_sequences: Set a stop sequence to tell the model to stop generating content. A stop sequence can be any sequence of characters. Try to avoid using a sequence of characters that may appear in the generated content.

Prompt design can sometimes require a few iterations before you consistently get the response you're looking for. This section provides guidance on some things you can try when iterating on your prompts:

Use different phrasing: Using different words or phrasing in your prompts often yields different responses from the model even though they all mean the same thing. If you're not getting the expected results from your prompt, try rephrasing it.

Switch to an analogous task: If you can't get the model to follow your instructions for a task, try giving it instructions for an analogous task that achieves the same result.

This prompt tells the model to categorize a book by using predefined categories:

The response is correct, but the model didn't stay within the bounds of the options. You also want to model to just respond with one of the options instead of in a full sentence. In this case, you can rephrase the instructions as a multiple choice question and ask the model to choose an option.

Prompt: Multiple choice problem: Which of the following options describes the book The Odyssey? Options:

Change the order of prompt content: The order of the content in the prompt can sometimes affect the response. Try changing the content order and see how that affects the response.

A fallback response is a response returned by the model when either the prompt or the response triggers a safety filter. An example of a fallback response is "I'm not able to help with that, as I'm only a language model."

If the model responds with a fallback response, try increasing the temperature.

Gemini 3 models are designed for advanced reasoning and instruction following. They respond best to prompts that are direct, well-structured, and clearly define the task and any constraints. The following practices are recommended for optimal results with Gemini 3:

Current day accuracy: Add the following clause to the developer instructions to help the model pay attention to the current day being in 2025:

Knowledge cutoff accuracy: Add the following clause to the developer instructions to make the model aware of its knowledge cutoff:

Grounding performance: Add the following clause to the developer instructions (with edits where appropriate) to improve the model's ability to ground responses in provided context:

You can leverage Gemini 3's advanced thinking capabilities to improve its response quality for complex tasks by prompting it to plan or self-critique before providing the final response.

Example - Explicit planning:

Example - Self-critique:

Using tags or Markdown helps the model distinguish between instructions, context, and tasks.

This template captures the core principles for prompting with Gemini 3. Always make sure to iterate and modify for your specific use case.

For deep agentic workflows, specific instructions are often required to control how the model reasons, plans, and executes tasks. While Gemini provides strong general performance, complex agents often require you to configure the trade-off between computational cost (latency and tokens) and task accuracy.

When designing prompts for agents, consider the following dimensions of behavior that you can steer in the agent:

Configuration for how the model thinks and plans before taking action.

Configuration for how the agent operates autonomously and handles roadblocks.

Configuration for how the agent communicates with the user and formats results.

The following system instruction is an example that has been evaluated by researchers to improve performance on agentic benchmarks where the model must adhere to a complex rulebook and interact with a user. It encourages the agent to act as a strong reasoner and planner, enforces specific behaviors across dimensions listed above and requires the model to proactively plan before taking any action.

You can adapt this template to fit your specific use case constraints.

This section aims to answer the question - Is there randomness in generative models' responses, or are they deterministic?

The short answer - yes to both. When you prompt a generative model, a text response is generated in two stages. In the first stage, the generative model processes the input prompt and generates a probability distribution over possible tokens (words) that are likely to come next. For example, if you prompt with the input text "The dog jumped over the ... ", the generative model will produce an array of probable next words:

This process is deterministic; a generative model will produce this same distribution every time it's input the same prompt text.

In the second stage, the generative model converts these distributions into actual text responses through one of several decoding strategies. A simple decoding strategy might select the most likely token at every timestep. This process would always be deterministic. However, you could instead choose to generate a response by randomly sampling over the distribution returned by the model. This process would be stochastic (random). Control the degree of randomness allowed in this decoding process by setting the temperature. A temperature of 0 means only the most likely tokens are selected, and there's no randomness. Conversely, a high temperature injects a high degree of randomness into the tokens selected by the model, leading to more unexpected, surprising model responses. For Gemini 3, it's recommended to not change the default temperature of 1.0 to avoid unexpected outcomes.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (unknown):
```unknown
What's a good name for a flower shop that specializes in selling bouquets of
    dried flowers? Create a list of 5 options with just the names.
```

Example 2 (unknown):
```unknown
What's a good name for a flower shop that specializes in selling bouquets of
    dried flowers? Create a list of 5 options with just the names.
```

Example 3 (unknown):
```unknown
Here are 10 names for a flower shop specializing in dried flowers:

    1. Everlasting Blooms
    2. Dried & Delightful
    3. The Petal Preserve
    4. Whispers of Wildflowers
    5. Forever Blooms
```

Example 4 (unknown):
```unknown
Here are 10 names for a flower shop specializing in dried flowers:

    1. Everlasting Blooms
    2. Dried & Delightful
    3. The Petal Preserve
    4. Whispers of Wildflowers
    5. Forever Blooms
```

---

## Get started with Live API

**URL:** https://ai.google.dev/gemini-api/docs/live

**Contents:**
- Get started with Live API
- Choose an implementation approach
- Partner integrations
- Get started
  - Python
  - JavaScript
- Example applications
- What's next

The Live API enables low-latency, real-time voice and video interactions with Gemini. It processes continuous streams of audio, video, or text to deliver immediate, human-like spoken responses, creating a natural conversational experience for your users.

Live API offers a comprehensive set of features such as Voice Activity Detection, tool use and function calling, session management (for managing long running conversations) and ephemeral tokens (for secure client-sided authentication).

This page gets you up and running with examples and basic code samples.

Try the Live API in Google AI Studiomic

When integrating with Live API, you'll need to choose one of the following implementation approaches:

To streamline the development of real-time audio and video apps, you can use a third-party integration that supports the Gemini Live API over WebRTC or WebSockets.

Create a real-time AI chatbot using Gemini Live and Pipecat.

Use the Gemini Live API with LiveKit Agents.

Fishjam by Software Mansion

Create live video and audio streaming applications with Fishjam.

Agent Development Kit (ADK)

Implement the Live API with Agent Development Kit (ADK).

Connect inbound and outbound calls to Live API with Voximplant.

Microphone stream Audio file stream

This server-side example streams audio from the microphone and plays the returned audio. For complete end-to-end examples including a client application, see Example applications.

The input audio format should be in 16-bit PCM, 16kHz, mono format, and the received audio uses a sample rate of 24kHz.

Install helpers for audio streaming. Additional system-level dependencies (e.g. portaudio) might be required. Refer to the PyAudio docs for detailed installation steps.

Install helpers for audio streaming. Additional system-level dependencies might be required (sox for Mac/Windows or ALSA for Linux). Refer to the speaker and mic docs for detailed installation steps.

Check out the following example applications that illustrate how to use Live API for end-to-end use cases:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-12 UTC.

**Examples:**

Example 1 (unknown):
```unknown
pip install pyaudio
```

Example 2 (unknown):
```unknown
pip install pyaudio
```

Example 3 (python):
```python
import asyncio
from google import genai
import pyaudio

client = genai.Client()

# --- pyaudio config ---
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

pya = pyaudio.PyAudio()

# --- Live API config ---
MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "You are a helpful and friendly AI assistant.",
}

audio_queue_output = asyncio.Queue()
audio_queue_mic = asyncio.Queue(maxsize=5)
audio_stream = None

async def listen_audio():
    """Listens for audio and puts it into the mic audio queue."""
    global audio_stream
    mic_info = pya.get_default_input_device_info()
    audio_stream = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=SEND_SAMPLE_RATE,
        input=True,
        input_device_index=mic_info["index"],
        frames_per_buffer=CHUNK_SIZE,
    )
    kwargs = {"exception_on_overflow": False} if __debug__ else {}
    while True:
        data = await asyncio.to_thread(audio_stream.read, CHUNK_SIZE, **kwargs)
        await audio_queue_mic.put({"data": data, "mime_type": "audio/pcm"})

async def send_realtime(session):
    """Sends audio from the mic audio queue to the GenAI session."""
    while True:
        msg = await audio_queue_mic.get()
        await session.send_realtime_input(audio=msg)

async def receive_audio(session):
    """Receives responses from GenAI and puts audio data into the speaker audio queue."""
    while True:
        turn = session.receive()
        async for response in turn:
            if (response.server_content and response.server_content.model_turn):
                for part in response.server_content.model_turn.parts:
                    if part.inline_data and isinstance(part.inline_data.data, bytes):
                        audio_queue_output.put_nowait(part.inline_data.data)

        # Empty the queue on interruption to stop playback
        while not audio_queue_output.empty():
            audio_queue_output.get_nowait()

async def play_audio():
    """Plays audio from the speaker audio queue."""
    stream = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=RECEIVE_SAMPLE_RATE,
        output=True,
    )
    while True:
        bytestream = await audio_queue_output.get()
        await asyncio.to_thread(stream.write, bytestream)

async def run():
    """Main function to run the audio loop."""
    try:
        async with client.aio.live.connect(
            model=MODEL, config=CONFIG
        ) as live_session:
            print("Connected to Gemini. Start speaking!")
            async with asyncio.TaskGroup() as tg:
                tg.create_task(send_realtime(live_session))
                tg.create_task(listen_audio())
                tg.create_task(receive_audio(live_session))
                tg.create_task(play_audio())
    except asyncio.CancelledError:
        pass
    finally:
        if audio_stream:
            audio_stream.close()
        pya.terminate()
        print("\nConnection closed.")

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Interrupted by user.")
```

Example 4 (python):
```python
import asyncio
from google import genai
import pyaudio

client = genai.Client()

# --- pyaudio config ---
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

pya = pyaudio.PyAudio()

# --- Live API config ---
MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"
CONFIG = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "You are a helpful and friendly AI assistant.",
}

audio_queue_output = asyncio.Queue()
audio_queue_mic = asyncio.Queue(maxsize=5)
audio_stream = None

async def listen_audio():
    """Listens for audio and puts it into the mic audio queue."""
    global audio_stream
    mic_info = pya.get_default_input_device_info()
    audio_stream = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=SEND_SAMPLE_RATE,
        input=True,
        input_device_index=mic_info["index"],
        frames_per_buffer=CHUNK_SIZE,
    )
    kwargs = {"exception_on_overflow": False} if __debug__ else {}
    while True:
        data = await asyncio.to_thread(audio_stream.read, CHUNK_SIZE, **kwargs)
        await audio_queue_mic.put({"data": data, "mime_type": "audio/pcm"})

async def send_realtime(session):
    """Sends audio from the mic audio queue to the GenAI session."""
    while True:
        msg = await audio_queue_mic.get()
        await session.send_realtime_input(audio=msg)

async def receive_audio(session):
    """Receives responses from GenAI and puts audio data into the speaker audio queue."""
    while True:
        turn = session.receive()
        async for response in turn:
            if (response.server_content and response.server_content.model_turn):
                for part in response.server_content.model_turn.parts:
                    if part.inline_data and isinstance(part.inline_data.data, bytes):
                        audio_queue_output.put_nowait(part.inline_data.data)

        # Empty the queue on interruption to stop playback
        while not audio_queue_output.empty():
            audio_queue_output.get_nowait()

async def play_audio():
    """Plays audio from the speaker audio queue."""
    stream = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=RECEIVE_SAMPLE_RATE,
        output=True,
    )
    while True:
        bytestream = await audio_queue_output.get()
        await asyncio.to_thread(stream.write, bytestream)

async def run():
    """Main function to run the audio loop."""
    try:
        async with client.aio.live.connect(
            model=MODEL, config=CONFIG
        ) as live_session:
            print("Connected to Gemini. Start speaking!")
            async with asyncio.TaskGroup() as tg:
                tg.create_task(send_realtime(live_session))
                tg.create_task(listen_audio())
                tg.create_task(receive_audio(live_session))
                tg.create_task(play_audio())
    except asyncio.CancelledError:
        pass
    finally:
        if audio_stream:
            audio_stream.close()
        pya.terminate()
        print("\nConnection closed.")

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Interrupted by user.")
```

---

## Text generation

**URL:** https://ai.google.dev/gemini-api/docs/text-generation

**Contents:**
- Text generation
  - Python
  - JavaScript
  - Go
  - Java
  - REST
  - Apps Script
- Thinking with Gemini 2.5
  - Python
  - JavaScript

The Gemini API can generate text output from various inputs, including text, images, video, and audio, leveraging Gemini models.

Here's a basic example that takes a single text input:

2.5 Flash and Pro models have "thinking" enabled by default to enhance quality, which may take longer to run and increase token usage.

When using 2.5 Flash, you can disable thinking by setting the thinking budget to zero.

For more details, see the thinking guide.

You can guide the behavior of Gemini models with system instructions. To do so, pass a GenerateContentConfig object.

The GenerateContentConfig object also lets you override default generation parameters, such as temperature.

Refer to the GenerateContentConfig in our API reference for a complete list of configurable parameters and their descriptions.

The Gemini API supports multimodal inputs, allowing you to combine text with media files. The following example demonstrates providing an image:

For alternative methods of providing images and more advanced image processing, see our image understanding guide. The API also supports document, video, and audio inputs and understanding.

By default, the model returns a response only after the entire generation process is complete.

For more fluid interactions, use streaming to receive GenerateContentResponse instances incrementally as they're generated.

Our SDKs provide functionality to collect multiple rounds of prompts and responses into a chat, giving you an easy way to keep track of the conversation history.

Streaming can also be used for multi-turn conversations.

All models in the Gemini family support text generation. To learn more about the models and their capabilities, visit the Models page.

For basic text generation, a zero-shot prompt often suffices without needing examples, system instructions or specific formatting.

For more tailored outputs:

Consult our prompt engineering guide for more tips.

In some cases, you may need structured output, such as JSON. Refer to our structured output guide to learn how.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "How does AI work?",
  });
  console.log(response.text);
}

await main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "How does AI work?",
  });
  console.log(response.text);
}

await main();
```

---

## Billing

**URL:** https://ai.google.dev/gemini-api/docs/billing

**Contents:**
- Billing
- About billing
- How to request an upgrade
  - Why use the paid tier?
- Cloud Billing
- Enable billing
- One-time prepayment verification
  - How the prepayment process works
- Monitor usage
- Frequently asked questions

This guide provides an overview of different Gemini API billing options, explains how to enable billing and monitor usage, and provides answers to frequently asked questions (FAQs) about billing.

Billing for the Gemini API is based on two pricing tiers: free of charge (or free) and pay-as-you-go (or paid). Pricing and rate limits differ between these tiers and also vary by model. You can check out the rate limits and pricing pages for more into. For a model-by-model breakdown of capabilities, see the Gemini models page.

To transition from the free tier to the pay-as-you-go plan, you need to enable billing for your Google Cloud project. The button you see in Google AI Studio depends on your project's current plan.

To start the process, follow these steps:

When you enable billing and use the paid tier, you benefit from higher rate limits, and your prompts and responses aren't used to improve Google products. For more information on data use for paid services, see the terms of service.

The Gemini API uses Cloud Billing for billing services. To use the paid tier, you must set up Cloud Billing on your cloud project. After you've enabled Cloud Billing, you can use Cloud Billing tools to track spending, understand costs, make payments, and access Cloud Billing support.

You can enable Cloud Billing starting from Google AI Studio:

Open Google AI Studio.

In the bottom of the left sidebar, select Dashboard > Usage and Billing > Billing tab.

Click Set up Billing for your chosen project to enable Cloud Billing.

Google may require a one-time prepayment to activate the paid tier for the Gemini API. This measure helps maintain the security and availability of our platform for all users. It is not a fee; it is a credit that is applied directly to your account for future use.

After you enable Cloud Billing, you can monitor your usage of the Gemini API in Google AI Studio.

This section provides answers to frequently asked questions.

Gemini API pricing is based on the following:

For pricing information, see the pricing page.

You can view your quota and system limits in the Google Cloud console.

To request more quota, follow the instructions at How to request an upgrade.

Yes, we make the free tier and paid tier available in many regions.

No, Google AI Studio usage remains free of charge regardless of if you set up billing across all supported regions.

The free tier for Gemini API differs based on the model selected. For now, you can try the 1M token context window in the following ways:

Use the GenerativeModel.count_tokens method to count the number of tokens. Refer to the Tokens guide to learn more about tokens.

Yes, Google Cloud credits can be used towards Gemini API usage.

Billing for the Gemini API is handled by the Cloud Billing system.

If your request fails with a 400 or 500 error, you won't be charged for the tokens used. However, the request will still count against your quota.

Model tuning is free, but inference on tuned models is charged at the same rate as the base models.

Requests to the GetTokens API are not billed, and they don't count against inference quota.

Refer to the terms for details on how data is handled when Cloud billing is enabled (see "How Google Uses Your Data" under "Paid Services"). Note that your Google AI Studio prompts are treated under the same "Paid Services" terms so long as at least 1 API project has billing enabled, which you can validate on the Gemini API Key page if you see any projects marked as "Paid" under "Plan".

The full amount is added as a credit to your Cloud Billing account. This credit will automatically be used to pay for any usage you accrue on Google Cloud, including the Gemini API or other services like Compute Engine and Cloud Storage.

No problem. Your project will remain on the Gemini API free tier. You won't lose any access, but you'll be subject to the free tier's rate limits. You can choose to complete the prepayment at any time in the future to upgrade.

Yes. If you have a credit balance on your account, you can request a refund through the Cloud Console, subject to our standard refund policies.

No. This is separate from your Free Trial credits. You can still use your Free Trial credits for eligible products.

Once your prepaid credit balance is exhausted, your account will transition to standard billing. Any additional usage will be charged to the primary payment method linked to your Cloud Billing account.

To get help with billing, see Get Cloud Billing support.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-16 UTC.

---

## Grounding with Google Maps

**URL:** https://ai.google.dev/gemini-api/docs/maps-grounding

**Contents:**
- Grounding with Google Maps
- Get started
  - Python
  - JavaScript
  - REST
- How Grounding with Google Maps works
- Why and when to use Grounding with Google Maps
- API methods and parameters
  - JSON
  - JSON

Grounding with Google Maps connects the generative capabilities of Gemini with the rich, factual, and up-to-date data of Google Maps. This feature enables developers to easily incorporate location-aware functionality into their applications. When a user query has a context related to Maps data, the Gemini model leverages Google Maps to provide factually accurate and fresh answers that are relevant to the user's specified location or general area.

This example demonstrates how to integrate Grounding with Google Maps into your application to provide accurate, location-aware responses to user queries. The prompt asks for local recommendations with an optional user location, enabling the Gemini model to leverage Google Maps data.

Grounding with Google Maps integrates the Gemini API with the Google Geo ecosystem by using the Maps API as a grounding source. When a user's query contains geographical context, the Gemini model can invoke the Grounding with Google Maps tool. The model can then generate responses grounded in Google Maps data relevant to the provided location.

The process typically involves:

Grounding with Google Maps is ideal for applications that require accurate, up-to-date, and location-specific information. It enhances the user experience by providing relevant and personalized content backed by Google Maps' extensive database of over 250 million places worldwide.

You should use Grounding with Google Maps when your application needs to:

Grounding with Google Maps excels in use cases where proximity and current factual data are critical, such as finding the "best coffee shop near me" or getting directions.

Grounding with Google Maps is exposed through the Gemini API as a tool within the generateContent method. You enable and configure Grounding with Google Maps by including a googleMaps object in the tools parameter of your request.

The googleMaps tool can additionally accept a boolean enableWidget parameter, that is used to control whether the googleMapsWidgetContextToken field is returned in the response. This can be used to display a contextual Places widget.

Additionally, the tool supports passing the contextual location as toolConfig.

When a response is successfully grounded with Google Maps data, the response includes a groundingMetadata field. This structured data is essential for verifying claims and building a rich citation experience in your application, as well as meeting the service usage requirements.

The Gemini API returns the following information with the groundingMetadata:

For a code snippet showing how to render inline citations in text, see the example in the Grounding with Google Search docs.

To use the returned googleMapsWidgetContextToken, you need to load the Google Maps JavaScript API.

Grounding with Google Maps supports a variety of location-aware use cases. The following examples demonstrate how different prompts and parameters can leverage Grounding with Google Maps. Information in the Google Maps Grounded Results may differ from actual conditions.

Ask detailed questions about a specific place to get answers based on Google user reviews and other Maps data.

Get recommendations tailored to a user's preferences and a specific geographical area.

Generate multi-day plans with directions and information about various locations, perfect for travel applications.

In this example, the googleMapsWidgetContextToken has been requested by enabling the widget in the Google Maps tool. When enabled, the returned token can be used to render a contextual Places widget using the <gmp-places-contextual> component from the Google Maps JavaScript API.

When the widget is rendered, it will look something like the following:

This section describes the service usage requirements for Grounding with Google Maps.

With each Google Maps Grounded Result, you'll receive sources in groundingChunks that support each response. The following metadata is also returned:

When presenting results from Grounding with Google Maps, you must specify the associated Google Maps sources, and inform your users of the following:

For each source in groundingChunks and in grounding_chunks.maps.placeAnswerSources.reviewSnippets, a link preview must be generated following these requirements:

These images show the minimum requirements for displaying the sources and Google Maps links.

You can collapse the view of the sources.

Optional: Enhance the link preview with additional content, such as:

For more information about some of our Google Maps data providers and their license terms, see the Google Maps and Google Earth legal notices.

When you attribute sources to Google Maps in text, follow these guidelines:

The following CSS renders Google Maps with the appropriate typographic style and color on a white or light background.

The Google Maps data includes context token, place ID, and review ID. You might cache, store, and export the following response data:

The restrictions against caching in the Grounding with Google Maps Terms don't apply.

Grounding with Google Maps has additional restrictions for certain content and activities to maintain a safe and reliable platform. In addition to the usage restrictions in the Terms, you will not use Grounding with Google Maps for high risk activities including emergency response services. You will not distribute or market your application that offers Grounding with Google Maps in a Prohibited Territory. The current Prohibited Territories are:

This list may be updated from time to time.

Grounding with Google Maps pricing is based on queries. The current rate is $25 / 1K grounded prompts. The free tier also has up to 500 requests per day available. A request is only counted towards the quota when a prompt successfully returns at least one Google Maps grounded result (i.e., results containing at least one Google Maps source). If multiple queries are sent to Google Maps from a single request, it counts as one request towards the rate limit.

For detailed pricing information, see the Gemini API pricing page.

You can find their capabilities on the model overview page.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-28 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

prompt = "What are the best Italian restaurants within a 15-minute walk from here?"

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        # Turn on grounding with Google Maps
        tools=[types.Tool(google_maps=types.GoogleMaps())],
        # Optionally provide the relevant location context (this is in Los Angeles)
        tool_config=types.ToolConfig(retrieval_config=types.RetrievalConfig(
            lat_lng=types.LatLng(
                latitude=34.050481, longitude=-118.248526))),
    ),
)

print("Generated Response:")
print(response.text)

if grounding := response.candidates[0].grounding_metadata:
  if grounding.grounding_chunks:
    print('-' * 40)
    print("Sources:")
    for chunk in grounding.grounding_chunks:
      print(f'- [{chunk.maps.title}]({chunk.maps.uri})')
```

Example 2 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

prompt = "What are the best Italian restaurants within a 15-minute walk from here?"

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        # Turn on grounding with Google Maps
        tools=[types.Tool(google_maps=types.GoogleMaps())],
        # Optionally provide the relevant location context (this is in Los Angeles)
        tool_config=types.ToolConfig(retrieval_config=types.RetrievalConfig(
            lat_lng=types.LatLng(
                latitude=34.050481, longitude=-118.248526))),
    ),
)

print("Generated Response:")
print(response.text)

if grounding := response.candidates[0].grounding_metadata:
  if grounding.grounding_chunks:
    print('-' * 40)
    print("Sources:")
    for chunk in grounding.grounding_chunks:
      print(f'- [{chunk.maps.title}]({chunk.maps.uri})')
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/gnai";

const ai = new GoogleGenAI({});

async function generateContentWithMapsGrounding() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "What are the best Italian restaurants within a 15-minute walk from here?",
    config: {
      // Turn on grounding with Google Maps
      tools: [{ googleMaps: {} }],
      toolConfig: {
        retrievalConfig: {
          // Optionally provide the relevant location context (this is in Los Angeles)
          latLng: {
            latitude: 34.050481,
            longitude: -118.248526,
          },
        },
      },
    },
  });

  console.log("Generated Response:");
  console.log(response.text);

  const grounding = response.candidates[0]?.groundingMetadata;
  if (grounding?.groundingChunks) {
    console.log("-".repeat(40));
    console.log("Sources:");
    for (const chunk of grounding.groundingChunks) {
      if (chunk.maps) {
        console.log(`- [${chunk.maps.title}](${chunk.maps.uri})`);
      }
    }
  }
}

generateContentWithMapsGrounding();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/gnai";

const ai = new GoogleGenAI({});

async function generateContentWithMapsGrounding() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "What are the best Italian restaurants within a 15-minute walk from here?",
    config: {
      // Turn on grounding with Google Maps
      tools: [{ googleMaps: {} }],
      toolConfig: {
        retrievalConfig: {
          // Optionally provide the relevant location context (this is in Los Angeles)
          latLng: {
            latitude: 34.050481,
            longitude: -118.248526,
          },
        },
      },
    },
  });

  console.log("Generated Response:");
  console.log(response.text);

  const grounding = response.candidates[0]?.groundingMetadata;
  if (grounding?.groundingChunks) {
    console.log("-".repeat(40));
    console.log("Sources:");
    for (const chunk of grounding.groundingChunks) {
      if (chunk.maps) {
        console.log(`- [${chunk.maps.title}](${chunk.maps.uri})`);
      }
    }
  }
}

generateContentWithMapsGrounding();
```

---

## Computer Use

**URL:** https://ai.google.dev/gemini-api/docs/computer-use

**Contents:**
- Computer Use
- How Computer Use works
- How to implement Computer Use
    - Install Playwright
    - Initialize Playwright browser instance
  - 1. Send a request to the model
  - Python
  - 2. Receive the model response
  - 3. Execute the received actions
  - Python

The Gemini 2.5 Computer Use Preview model and tool enable you to build browser control agents that interact with and automate tasks. Using screenshots, the Computer Use model can "see" a computer screen, and "act" by generating specific UI actions like mouse clicks and keyboard inputs. Similar to function calling, you need to write the client-side application code to receive and execute the Computer Use actions.

With Computer Use, you can build agents that:

The easiest way to test the Gemini Computer Use model is through the reference implementation or Browserbase demo environment.

To build a browser control agent with the Computer Use model, implement an agent loop that does the following:

Send a request to the model

Receive the model response

Execute the received action

Capture the new environment state

This process repeats from step 2 with the Computer Use model using the new screenshot and the ongoing goal to suggest the next action. The loop continues until the task is completed, an error occurs, or the process is terminated (e.g., due to a "block" safety response or user decision).

Before building with the Computer Use model and tool you will need to set up the following:

The examples in this section use a browser as the execution environment and Playwright as the client-side action handler. To run these samples you must install the necessary dependencies and initialize a Playwright browser instance.

Sample code for extending to an Android environment is included in the Using custom user-defined functions section.

Add the Computer Use tool to your API request and send a prompt to the Computer Use model that includes the user's goal. You must use the Gemini Computer Use model, gemini-2.5-computer-use-preview-10-2025. If you try to use the Computer Use tool with a different model, you will get an error.

You can also optionally add the following parameters:

Note that there is no need to specify the display size when issuing a request; the model predicts pixel coordinates scaled to the height and width of the screen.

For an example with custom functions, see Using custom user-defined functions.

The Computer Use model will respond with one or more FunctionCalls if it determines UI actions are needed to complete the task. Computer Use supports parallel function calling, meaning the model can return multiple actions in a single turn.

Here is an example model response.

Your application code needs to parse the model response, execute the actions, and collect the results.

The example code below extracts function calls from the Computer Use model response, and translates them into actions that can be executed with Playwright. The model outputs normalized coordinates (0-999) regardless of the input image dimensions, so part of the translation step is converting these normalized coordinates back to actual pixel values.

The recommended screen size for use with the Computer Use model is (1440, 900). The model will work with any resolution, though the quality of the results may be impacted.

Note that this example only includes the implementation for the 3 most common UI actions: open_web_browser, click_at, and type_text_at. For production use cases, you will need to implement all other UI actions from the Supported actions list unless you explicitly add them as excluded_predefined_functions.

After executing the actions, send the result of the function execution back to the model so it can use this information to generate the next action. If multiple actions (parallel calls) were executed, you must send a FunctionResponse for each one in the subsequent user turn.

To enable multi-step interactions, combine the four steps from the How to implement Computer Use section into a loop. Remember to manage the conversation history correctly by appending both model responses and your function responses.

To run this code sample you need to:

Define the helper functions from steps (3) Execute the received actions and (4) Capture the new environment state.

You can optionally include custom user-defined functions in your request to extend the functionality of the model. The example below adapts the Computer Use model and tool for mobile use cases by including custom user-defined actions like open_app, long_press_at, and go_home, while excluding browser-specific actions. The model can intelligently call these custom functions alongside standard UI actions to complete tasks in non-browser environments.

The Computer Use model can request the following UI actions via a FunctionCall. Your client-side code must implement the execution logic for these actions. See the reference implementation for examples.

Depending on the action, the model response might also include a safety_decision from an internal safety system that checks the model's proposed action.

If the safety_decision is require_confirmation, you must ask the end user to confirm before proceeding with executing the action. Per the terms of service, you are not allowed to bypass requests for human confirmation.

This code sample prompts the end-user for confirmation before executing the action. If the user does not confirm the action, the loop terminates. If the user confirms the action, the action is executed and the safety_acknowledgement field is marked as True.

If the user confirms, you must include the safety acknowledgement in your FunctionResponse.

Computer Use API is a novel API and presents new risks that developers should be mindful of:

To address these risks, you can implement the following safety measures and best practices:

Human-in-the-Loop (HITL):

Provide custom safety instructions: In addition to the built-in user confirmation checks, developers may optionally add a custom system instruction that enforces their own safety policies, either to block certain model actions or require user confirmation before the model takes certain high-stakes irreversible actions. Here is an example of a custom safety system instruction you may include when interacting with the model.

Set your custom safety rules as a system instruction:

Secure execution environment: Run your agent in a secure, sandboxed environment to limit its potential impact (e.g., A sandboxed virtual machine (VM), a container (e.g., Docker), or a dedicated browser profile with limited permissions).

Input sanitization: Sanitize all user-generated text in prompts to mitigate the risk of unintended instructions or prompt injection. This is a helpful layer of security, but not a replacement for a secure execution environment.

Content guardrails: Use guardrails and content safety APIs to evaluate user inputs, tool input and output, an agent's response for appropriateness, prompt injection, and jailbreak detection.

Allowlists and blocklists: Implement filtering mechanisms to control where the model can navigate and what it can do. A blocklist of prohibited websites is a good starting point, while a more restrictive allowlist is even more secure.

Observability and logging: Maintain detailed logs for debugging, auditing, and incident response. Your client should log prompts, screenshots, model-suggested actions (function_call), safety responses, and all actions ultimately executed by the client.

Environment management: Ensure the GUI environment is consistent. Unexpected pop-ups, notifications, or changes in layout can confuse the model. Start from a known, clean state for each new task if possible.

gemini-2.5-computer-use-preview-10-2025

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-10-24 UTC.

**Examples:**

Example 1 (unknown):
```unknown
pip install google-genai playwright
    playwright install chromium
```

Example 2 (python):
```python
from playwright.sync_api import sync_playwright

    # 1. Configure screen dimensions for the target environment
    SCREEN_WIDTH = 1440
    SCREEN_HEIGHT = 900

    # 2. Start the Playwright browser
    # In production, utilize a sandboxed environment.
    playwright = sync_playwright().start()
    # Set headless=False to see the actions performed on your screen
    browser = playwright.chromium.launch(headless=False)

    # 3. Create a context and page with the specified dimensions
    context = browser.new_context(
        viewport={"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
    )
    page = context.new_page()

    # 4. Navigate to an initial page to start the task
    page.goto("https://www.google.com")

    # The 'page', 'SCREEN_WIDTH', and 'SCREEN_HEIGHT' variables
    # will be used in the steps below.
```

Example 3 (python):
```python
from google import genai
from google.genai import types
from google.genai.types import Content, Part

client = genai.Client()

# Specify predefined functions to exclude (optional)
excluded_functions = ["drag_and_drop"]

generate_content_config = genai.types.GenerateContentConfig(
    tools=[
        # 1. Computer Use tool with browser environment
        types.Tool(
            computer_use=types.ComputerUse(
                environment=types.Environment.ENVIRONMENT_BROWSER,
                # Optional: Exclude specific predefined functions
                excluded_predefined_functions=excluded_functions
                )
              ),
        # 2. Optional: Custom user-defined functions
        #types.Tool(
          # function_declarations=custom_functions
          #   )
          ],
  )

# Create the content with user message
contents=[
    Content(
        role="user",
        parts=[
            Part(text="Search for highly rated smart fridges with touchscreen, 2 doors, around 25 cu ft, priced below 4000 dollars on Google Shopping. Create a bulleted list of the 3 cheapest options in the format of name, description, price in an easy-to-read layout."),
        ],
    )
]

# Generate content with the configured settings
response = client.models.generate_content(
    model='gemini-2.5-computer-use-preview-10-2025',
    contents=contents,
    config=generate_content_config,
)

# Print the response output
print(response)
```

Example 4 (python):
```python
from google import genai
from google.genai import types
from google.genai.types import Content, Part

client = genai.Client()

# Specify predefined functions to exclude (optional)
excluded_functions = ["drag_and_drop"]

generate_content_config = genai.types.GenerateContentConfig(
    tools=[
        # 1. Computer Use tool with browser environment
        types.Tool(
            computer_use=types.ComputerUse(
                environment=types.Environment.ENVIRONMENT_BROWSER,
                # Optional: Exclude specific predefined functions
                excluded_predefined_functions=excluded_functions
                )
              ),
        # 2. Optional: Custom user-defined functions
        #types.Tool(
          # function_declarations=custom_functions
          #   )
          ],
  )

# Create the content with user message
contents=[
    Content(
        role="user",
        parts=[
            Part(text="Search for highly rated smart fridges with touchscreen, 2 doors, around 25 cu ft, priced below 4000 dollars on Google Shopping. Create a bulleted list of the 3 cheapest options in the format of name, description, price in an easy-to-read layout."),
        ],
    )
]

# Generate content with the configured settings
response = client.models.generate_content(
    model='gemini-2.5-computer-use-preview-10-2025',
    contents=contents,
    config=generate_content_config,
)

# Print the response output
print(response)
```

---

## Prompt design strategies

**URL:** https://ai.google.dev/gemini-api/docs/prompting-intro

**Contents:**
- Prompt design strategies
- Topic-specific prompt guides
- Clear and specific instructions
  - Input
    - Partial input completion
  - Constraints
  - Response format
    - Format responses with the completion strategy
- Zero-shot vs few-shot prompts
  - Optimal number of examples

Prompt design is the process of creating prompts, or natural language requests, that elicit accurate, high quality responses from a language model.

This page introduces basic concepts, strategies, and best practices to get you started designing prompts to get the most out of Gemini AI models.

Looking for more specific prompt strategies? Check out our other prompting guides on:

You can find other sample prompts in the prompt gallery meant to interactively showcase many of the concepts shared in this guide.

An effective and efficient way to customize model behavior is to provide it with clear and specific instructions. Instructions can be in the form of a question, step-by-step tasks, or as complex as mapping out a user's experience and mindset.

Input is the required text in the prompt that you want the model to provide a response to. Inputs can be a question that the model answers (question input), a task the model performs (task input), an entity the model operates on (entity input), or partial input that the model completes or continues (completion input).

Generative language models work like an advanced auto completion tool. When you provide partial content, the model can provide the rest of the content or what it thinks is a continuation of that content as a response. When doing so, if you include any examples or context, the model can take those examples or context into account.

The following example provides a prompt with an instruction and an entity input:

While the model did as prompted, writing out the instructions in natural language can sometimes be challenging and it leaves a lot to the model's interpretation. For example, a restaurants menu might contain many items. To reduce the size of the JSON response, you probably want to omit the items that weren't ordered. In this case, you can give an example and a response prefix and let the model complete it:

Notice how "cheeseburger" was excluded from the output because it wasn't a part of the order.

Specify any constraints on reading the prompt or generating a response. You can tell the model what to do and not to do. For example, you can specify a constraint in the prompt on how long you want a summary to be:

Prompt: Summarize this text in one sentence: Text: A quantum computer exploits quantum mechanical phenomena to perform calculations exponentially faster than any modern traditional computer. At very tiny scales, physical matter acts as both particles and as waves, and quantum computing uses specialized hardware to leverage this behavior. The operating principles of quantum devices is beyond the scope of classical physics. When deployed at scale, quantum computers could be used in a wide variety of applications such as: in cybersecurity to break existing encryption methods while helping researchers create new ones, in meteorology to develop better weather forecasting etc. However, the current state of the art quantum computers are still largely experimental and impractical.

Response: Exploiting quantum mechanical phenomena, quantum computers can perform calculations exponentially faster than traditional computers for potential applications like cybersecurity and meteorology, although they are currently largely experimental and impractical. (gemini-2.5-flash)

You can give instructions that specify the format of the response. For example, you can ask for the response to be formatted as a table, bulleted list, elevator pitch, keywords, sentence, or paragraph. The following system instruction tells the model to be more conversational in its response:

The completion strategy can also help format the response. The following example prompts the model to create an essay outline:

The prompt didn't specify the format for the outline and the model chose a format for you. To get the model to return an outline in a specific format, you can add text that represents the start of the outline and let the model complete it based on the pattern that you initiated.

You can include examples in the prompt that show the model what getting it right looks like. The model attempts to identify patterns and relationships from the examples and applies them when generating a response. Prompts that contain a few examples are called few-shot prompts, while prompts that provide no examples are called zero-shot prompts. Few-shot prompts are often used to regulate the formatting, phrasing, scoping, or general patterning of model responses. Use specific and varied examples to help the model narrow its focus and generate more accurate results.

We recommend to always include few-shot examples in your prompts. Prompts without few-shot examples are likely to be less effective. In fact, you can remove instructions from your prompt if your examples are clear enough in showing the task at hand.

The following zero-shot prompt asks the model to choose the best explanation.

If your use case requires the model to produce concise responses, you can include examples in the prompt that give preference to concise responses.

The following prompt provides two examples that show preference to the shorter explanations. In the response, you can see that the examples guided the model to choose the shorter explanation (Explanation2) as opposed to the longer explanation (Explanation1) like it did previously.

Models like Gemini can often pick up on patterns using a few examples, though you may need to experiment with the number of examples to provide in the prompt for the best results. At the same time, if you include too many examples, the model may start to overfit the response to the examples.

Using examples to show the model a pattern to follow is more effective than using examples to show the model an anti pattern to avoid.

Make sure that the structure and formatting of few-shot examples are the same to avoid responses with undesired formats. One of the primary objectives of adding few-shot examples in prompts is to show the model the response format. Therefore, it is essential to ensure a consistent format across all examples, especially paying attention to XML tags, white spaces, newlines, and example splitters.

You can include instructions and information in a prompt that the model needs to solve a problem, instead of assuming that the model has all of the required information. This contextual information helps the model understand the constraints and details of what you're asking for it to do.

The following example asks the model to give troubleshooting guidance for a router:

The response looks like generic troubleshooting information that's not specific to the router or the status of the LED indicator lights.

To customize the response for the specific router, you can add to the prompt the router's troubleshooting guide as context for it to refer to when providing a response.

A prefix is a word or phrase that you add to the prompt content that can serve several purposes, depending on where you put the prefix:

In the following example, "Text:" is the input prefix and "The answer is:" is the output prefix.

For use cases that require complex prompts, you can help the model manage this complexity by breaking things down into simpler components.

Break down instructions: Instead of having many instructions in one prompt, create one prompt per instruction. You can choose which prompt to process based on the user's input.

Chain prompts: For complex tasks that involve multiple sequential steps, make each step a prompt and chain the prompts together in a sequence. In this sequential chain of prompts, the output of one prompt in the sequence becomes the input of the next prompt. The output of the last prompt in the sequence is the final output.

Aggregate responses: Aggregation is when you want to perform different parallel tasks on different portions of the data and aggregate the results to produce the final output. For example, you can tell the model to perform one operation on the first part of the data, perform another operation on the rest of the data and aggregate the results.

Each call that you send to a model includes parameter values that control how the model generates a response. The model can generate different results for different parameter values. Experiment with different parameter values to get the best values for the task. The parameters available for different models may differ. The most common parameters are the following:

Max output tokens: Specifies the maximum number of tokens that can be generated in the response. A token is approximately four characters. 100 tokens correspond to roughly 60-80 words.

Temperature: The temperature controls the degree of randomness in token selection. The temperature is used for sampling during response generation, which occurs when topP and topK are applied. Lower temperatures are good for prompts that require a more deterministic or less open-ended response, while higher temperatures can lead to more diverse or creative results. A temperature of 0 is deterministic, meaning that the highest probability response is always selected.

topK: The topK parameter changes how the model selects tokens for output. A topK of 1 means the selected token is the most probable among all the tokens in the model's vocabulary (also called greedy decoding), while a topK of 3 means that the next token is selected from among the 3 most probable using the temperature. For each token selection step, the topK tokens with the highest probabilities are sampled. Tokens are then further filtered based on topP with the final token selected using temperature sampling.

topP: The topP parameter changes how the model selects tokens for output. Tokens are selected from the most to least probable until the sum of their probabilities equals the topP value. For example, if tokens A, B, and C have a probability of 0.3, 0.2, and 0.1 and the topP value is 0.5, then the model will select either A or B as the next token by using the temperature and exclude C as a candidate. The default topP value is 0.95.

stop_sequences: Set a stop sequence to tell the model to stop generating content. A stop sequence can be any sequence of characters. Try to avoid using a sequence of characters that may appear in the generated content.

Prompt design can sometimes require a few iterations before you consistently get the response you're looking for. This section provides guidance on some things you can try when iterating on your prompts:

Use different phrasing: Using different words or phrasing in your prompts often yields different responses from the model even though they all mean the same thing. If you're not getting the expected results from your prompt, try rephrasing it.

Switch to an analogous task: If you can't get the model to follow your instructions for a task, try giving it instructions for an analogous task that achieves the same result.

This prompt tells the model to categorize a book by using predefined categories:

The response is correct, but the model didn't stay within the bounds of the options. You also want to model to just respond with one of the options instead of in a full sentence. In this case, you can rephrase the instructions as a multiple choice question and ask the model to choose an option.

Prompt: Multiple choice problem: Which of the following options describes the book The Odyssey? Options:

Change the order of prompt content: The order of the content in the prompt can sometimes affect the response. Try changing the content order and see how that affects the response.

A fallback response is a response returned by the model when either the prompt or the response triggers a safety filter. An example of a fallback response is "I'm not able to help with that, as I'm only a language model."

If the model responds with a fallback response, try increasing the temperature.

Gemini 3 models are designed for advanced reasoning and instruction following. They respond best to prompts that are direct, well-structured, and clearly define the task and any constraints. The following practices are recommended for optimal results with Gemini 3:

Current day accuracy: Add the following clause to the developer instructions to help the model pay attention to the current day being in 2025:

Knowledge cutoff accuracy: Add the following clause to the developer instructions to make the model aware of its knowledge cutoff:

Grounding performance: Add the following clause to the developer instructions (with edits where appropriate) to improve the model's ability to ground responses in provided context:

You can leverage Gemini 3's advanced thinking capabilities to improve its response quality for complex tasks by prompting it to plan or self-critique before providing the final response.

Example - Explicit planning:

Example - Self-critique:

Using tags or Markdown helps the model distinguish between instructions, context, and tasks.

This template captures the core principles for prompting with Gemini 3. Always make sure to iterate and modify for your specific use case.

For deep agentic workflows, specific instructions are often required to control how the model reasons, plans, and executes tasks. While Gemini provides strong general performance, complex agents often require you to configure the trade-off between computational cost (latency and tokens) and task accuracy.

When designing prompts for agents, consider the following dimensions of behavior that you can steer in the agent:

Configuration for how the model thinks and plans before taking action.

Configuration for how the agent operates autonomously and handles roadblocks.

Configuration for how the agent communicates with the user and formats results.

The following system instruction is an example that has been evaluated by researchers to improve performance on agentic benchmarks where the model must adhere to a complex rulebook and interact with a user. It encourages the agent to act as a strong reasoner and planner, enforces specific behaviors across dimensions listed above and requires the model to proactively plan before taking any action.

You can adapt this template to fit your specific use case constraints.

This section aims to answer the question - Is there randomness in generative models' responses, or are they deterministic?

The short answer - yes to both. When you prompt a generative model, a text response is generated in two stages. In the first stage, the generative model processes the input prompt and generates a probability distribution over possible tokens (words) that are likely to come next. For example, if you prompt with the input text "The dog jumped over the ... ", the generative model will produce an array of probable next words:

This process is deterministic; a generative model will produce this same distribution every time it's input the same prompt text.

In the second stage, the generative model converts these distributions into actual text responses through one of several decoding strategies. A simple decoding strategy might select the most likely token at every timestep. This process would always be deterministic. However, you could instead choose to generate a response by randomly sampling over the distribution returned by the model. This process would be stochastic (random). Control the degree of randomness allowed in this decoding process by setting the temperature. A temperature of 0 means only the most likely tokens are selected, and there's no randomness. Conversely, a high temperature injects a high degree of randomness into the tokens selected by the model, leading to more unexpected, surprising model responses. For Gemini 3, it's recommended to not change the default temperature of 1.0 to avoid unexpected outcomes.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (unknown):
```unknown
What's a good name for a flower shop that specializes in selling bouquets of
    dried flowers? Create a list of 5 options with just the names.
```

Example 2 (unknown):
```unknown
What's a good name for a flower shop that specializes in selling bouquets of
    dried flowers? Create a list of 5 options with just the names.
```

Example 3 (unknown):
```unknown
Here are 10 names for a flower shop specializing in dried flowers:

    1. Everlasting Blooms
    2. Dried & Delightful
    3. The Petal Preserve
    4. Whispers of Wildflowers
    5. Forever Blooms
```

Example 4 (unknown):
```unknown
Here are 10 names for a flower shop specializing in dried flowers:

    1. Everlasting Blooms
    2. Dried & Delightful
    3. The Petal Preserve
    4. Whispers of Wildflowers
    5. Forever Blooms
```

---

## Grounding with Google Search

**URL:** https://ai.google.dev/gemini-api/docs/google-search

**Contents:**
- Grounding with Google Search
  - Python
  - JavaScript
  - REST
- How grounding with Google Search works
- Understanding the grounding response
- Attributing sources with inline citations
  - Python
  - JavaScript
- Pricing

Grounding with Google Search connects the Gemini model to real-time web content and works with all available languages. This allows Gemini to provide more accurate answers and cite verifiable sources beyond its knowledge cutoff.

Grounding helps you build applications that can:

Provide citations: Build user trust by showing the sources for the model's claims.

You can learn more by trying the Search tool notebook.

When you enable the google_search tool, the model handles the entire workflow of searching, processing, and citing information automatically.

When a response is successfully grounded, the response includes a groundingMetadata field. This structured data is essential for verifying claims and building a rich citation experience in your application.

The Gemini API returns the following information with the groundingMetadata:

Grounding with Google Search can also be used in combination with the URL context tool to ground responses in both public web data and the specific URLs you provide.

The API returns structured citation data, giving you complete control over how you display sources in your user interface. You can use the groundingSupports and groundingChunks fields to link the model's statements directly to their sources. Here is a common pattern for processing the metadata to create a response with inline, clickable citations.

The new response with inline citations will look like this:

When you use Grounding with Google Search with Gemini 3, your project is billed for each search query that the model decides to execute. If the model decides to execute multiple search queries to answer a single prompt (for example, searching for "UEFA Euro 2024 winner" and "Spain vs England Euro 2024 final score" within the same API call), this counts as two billable uses of the tool for that request. This only applies to Gemini 3 models; when you use search grounding with Gemini 2.5 or older models, your project is billed per prompt.

For detailed pricing information, see the Gemini API pricing page.

Experimental and Preview models are not included. You can find their capabilities on the model overview page.

You can use Grounding with Google Search with other tools like code execution and URL context to power more complex use cases.

While the google_search tool is recommended for Gemini 2.0 and later, Gemini 1.5 supports a legacy tool named google_search_retrieval. This tool provides a dynamic mode that allows the model to decide whether to perform a search based on its confidence that the prompt requires fresh information. If the model's confidence is above a dynamic_threshold you set (a value between 0.0 and 1.0), it will perform a search.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-05 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Who won the euro 2024?",
    config=config,
)

print(response.text)
```

Example 2 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Who won the euro 2024?",
    config=config,
)

print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

const groundingTool = {
  googleSearch: {},
};

const config = {
  tools: [groundingTool],
};

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: "Who won the euro 2024?",
  config,
});

console.log(response.text);
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

const groundingTool = {
  googleSearch: {},
};

const config = {
  tools: [groundingTool],
};

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: "Who won the euro 2024?",
  config,
});

console.log(response.text);
```

---

## Audio understanding

**URL:** https://ai.google.dev/gemini-api/docs/audio

**Contents:**
- Audio understanding
- Transcribe speech to text
  - Python
  - JavaScript
  - REST
- Input audio
  - Upload an audio file
  - Python
  - JavaScript
  - Go

Gemini can analyze and understand audio input and generate text responses to it, enabling use cases like the following:

As of now the Gemini API doesn't support real-time transcription use cases. For real-time voice and video interactions refer to the Live API. For dedicated speech to text models with support for real-time transcription, use the Google Cloud Speech-to-Text API.

This example application shows how to prompt the Gemini API to transcribe, translate, and summarize speech, including timestamps, speaker diarization, and emotion detection using structured outputs.

You can prompt AI Studio Build to create a transcription app just like this one, with the click of a button.

You can provide audio data to Gemini in the following ways:

You can use the Files API to upload an audio file. Always use the Files API when the total request size (including the files, text prompt, system instructions, etc.) is larger than 20 MB.

The following code uploads an audio file and then uses the file in a call to generateContent.

To learn more about working with media files, see Files API.

Instead of uploading an audio file, you can pass inline audio data in the request to generateContent:

A few things to keep in mind about inline audio data:

To get a transcript of audio data, just ask for it in the prompt:

You can refer to specific sections of an audio file using timestamps of the form MM:SS. For example, the following prompt requests a transcript that

Ends at 3 minutes 29 seconds from the beginning of the file.

Call the countTokens method to get a count of the number of tokens in an audio file. For example:

Gemini supports the following audio format MIME types:

This guide shows how to generate text in response to audio data. To learn more, see the following resources:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-03 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

YOUTUBE_URL = "https://www.youtube.com/watch?v=ku-N-eS1lgM"

def main():
  prompt = """
    Process the audio file and generate a detailed transcription.

    Requirements:
    1. Identify distinct speakers (e.g., Speaker 1, Speaker 2, or names if context allows).
    2. Provide accurate timestamps for each segment (Format: MM:SS).
    3. Detect the primary language of each segment.
    4. If the segment is in a language different than English, also provide the English translation.
    5. Identify the primary emotion of the speaker in this segment. You MUST choose exactly one of the following: Happy, Sad, Angry, Neutral.
    6. Provide a brief summary of the entire audio at the beginning.
  """

  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
      types.Content(
        parts=[
          types.Part(
            file_data=types.FileData(
              file_uri=YOUTUBE_URL
            )
          ),
          types.Part(
            text=prompt
          )
        ]
      )
    ],
    config=types.GenerateContentConfig(
      response_mime_type="application/json",
      response_schema=types.Schema(
        type=types.Type.OBJECT,
        properties={
          "summary": types.Schema(
            type=types.Type.STRING,
            description="A concise summary of the audio content.",
          ),
          "segments": types.Schema(
            type=types.Type.ARRAY,
            description="List of transcribed segments with speaker and timestamp.",
            items=types.Schema(
              type=types.Type.OBJECT,
              properties={
                "speaker": types.Schema(type=types.Type.STRING),
                "timestamp": types.Schema(type=types.Type.STRING),
                "content": types.Schema(type=types.Type.STRING),
                "language": types.Schema(type=types.Type.STRING),
                "language_code": types.Schema(type=types.Type.STRING),
                "translation": types.Schema(type=types.Type.STRING),
                "emotion": types.Schema(
                  type=types.Type.STRING,
                  enum=["happy", "sad", "angry", "neutral"]
                ),
              },
              required=["speaker", "timestamp", "content", "language", "language_code", "emotion"],
            ),
          ),
        },
        required=["summary", "segments"],
      ),
    ),
  )

  print(response.text)

if __name__ == "__main__":
  main()
```

Example 2 (python):
```python
from google import genai
from google.genai import types

client = genai.Client()

YOUTUBE_URL = "https://www.youtube.com/watch?v=ku-N-eS1lgM"

def main():
  prompt = """
    Process the audio file and generate a detailed transcription.

    Requirements:
    1. Identify distinct speakers (e.g., Speaker 1, Speaker 2, or names if context allows).
    2. Provide accurate timestamps for each segment (Format: MM:SS).
    3. Detect the primary language of each segment.
    4. If the segment is in a language different than English, also provide the English translation.
    5. Identify the primary emotion of the speaker in this segment. You MUST choose exactly one of the following: Happy, Sad, Angry, Neutral.
    6. Provide a brief summary of the entire audio at the beginning.
  """

  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
      types.Content(
        parts=[
          types.Part(
            file_data=types.FileData(
              file_uri=YOUTUBE_URL
            )
          ),
          types.Part(
            text=prompt
          )
        ]
      )
    ],
    config=types.GenerateContentConfig(
      response_mime_type="application/json",
      response_schema=types.Schema(
        type=types.Type.OBJECT,
        properties={
          "summary": types.Schema(
            type=types.Type.STRING,
            description="A concise summary of the audio content.",
          ),
          "segments": types.Schema(
            type=types.Type.ARRAY,
            description="List of transcribed segments with speaker and timestamp.",
            items=types.Schema(
              type=types.Type.OBJECT,
              properties={
                "speaker": types.Schema(type=types.Type.STRING),
                "timestamp": types.Schema(type=types.Type.STRING),
                "content": types.Schema(type=types.Type.STRING),
                "language": types.Schema(type=types.Type.STRING),
                "language_code": types.Schema(type=types.Type.STRING),
                "translation": types.Schema(type=types.Type.STRING),
                "emotion": types.Schema(
                  type=types.Type.STRING,
                  enum=["happy", "sad", "angry", "neutral"]
                ),
              },
              required=["speaker", "timestamp", "content", "language", "language_code", "emotion"],
            ),
          ),
        },
        required=["summary", "segments"],
      ),
    ),
  )

  print(response.text)

if __name__ == "__main__":
  main()
```

Example 3 (python):
```python
import {
  GoogleGenAI,
  Type
} from "@google/genai";

const ai = new GoogleGenAI({});

const YOUTUBE_URL = "https://www.youtube.com/watch?v=ku-N-eS1lgM";

async function main() {
  const prompt = `
      Process the audio file and generate a detailed transcription.

      Requirements:
      1. Identify distinct speakers (e.g., Speaker 1, Speaker 2, or names if context allows).
      2. Provide accurate timestamps for each segment (Format: MM:SS).
      3. Detect the primary language of each segment.
      4. If the segment is in a language different than English, also provide the English translation.
      5. Identify the primary emotion of the speaker in this segment. You MUST choose exactly one of the following: Happy, Sad, Angry, Neutral.
      6. Provide a brief summary of the entire audio at the beginning.
    `;

  const Emotion = {
    Happy: 'happy',
    Sad: 'sad',
    Angry: 'angry',
    Neutral: 'neutral'
  };

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: {
      parts: [
        {
          fileData: {
            fileUri: YOUTUBE_URL,
          },
        },
        {
          text: prompt,
        },
      ],
    },
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          summary: {
            type: Type.STRING,
            description: "A concise summary of the audio content.",
          },
          segments: {
            type: Type.ARRAY,
            description: "List of transcribed segments with speaker and timestamp.",
            items: {
              type: Type.OBJECT,
              properties: {
                speaker: { type: Type.STRING },
                timestamp: { type: Type.STRING },
                content: { type: Type.STRING },
                language: { type: Type.STRING },
                language_code: { type: Type.STRING },
                translation: { type: Type.STRING },
                emotion: {
                  type: Type.STRING,
                  enum: Object.values(Emotion)
                },
              },
              required: ["speaker", "timestamp", "content", "language", "language_code", "emotion"],
            },
          },
        },
        required: ["summary", "segments"],
      },
    },
  });
  const json = JSON.parse(response.text);
  console.log(json);
}

await main();
```

Example 4 (python):
```python
import {
  GoogleGenAI,
  Type
} from "@google/genai";

const ai = new GoogleGenAI({});

const YOUTUBE_URL = "https://www.youtube.com/watch?v=ku-N-eS1lgM";

async function main() {
  const prompt = `
      Process the audio file and generate a detailed transcription.

      Requirements:
      1. Identify distinct speakers (e.g., Speaker 1, Speaker 2, or names if context allows).
      2. Provide accurate timestamps for each segment (Format: MM:SS).
      3. Detect the primary language of each segment.
      4. If the segment is in a language different than English, also provide the English translation.
      5. Identify the primary emotion of the speaker in this segment. You MUST choose exactly one of the following: Happy, Sad, Angry, Neutral.
      6. Provide a brief summary of the entire audio at the beginning.
    `;

  const Emotion = {
    Happy: 'happy',
    Sad: 'sad',
    Angry: 'angry',
    Neutral: 'neutral'
  };

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: {
      parts: [
        {
          fileData: {
            fileUri: YOUTUBE_URL,
          },
        },
        {
          text: prompt,
        },
      ],
    },
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          summary: {
            type: Type.STRING,
            description: "A concise summary of the audio content.",
          },
          segments: {
            type: Type.ARRAY,
            description: "List of transcribed segments with speaker and timestamp.",
            items: {
              type: Type.OBJECT,
              properties: {
                speaker: { type: Type.STRING },
                timestamp: { type: Type.STRING },
                content: { type: Type.STRING },
                language: { type: Type.STRING },
                language_code: { type: Type.STRING },
                translation: { type: Type.STRING },
                emotion: {
                  type: Type.STRING,
                  enum: Object.values(Emotion)
                },
              },
              required: ["speaker", "timestamp", "content", "language", "language_code", "emotion"],
            },
          },
        },
        required: ["summary", "segments"],
      },
    },
  });
  const json = JSON.parse(response.text);
  console.log(json);
}

await main();
```

---

## Session management with Live API

**URL:** https://ai.google.dev/gemini-api/docs/live-session

**Contents:**
- Session management with Live API
- Session lifetime
- Context window compression
  - Python
  - JavaScript
- Session resumption
  - Python
  - JavaScript
- Receiving a message before the session disconnects
  - Python

In the Live API, a session refers to a persistent connection where input and output are streamed continuously over the same connection (read more about how it works). This unique session design enables low latency and supports unique features, but can also introduce challenges, like session time limits, and early termination. This guide covers strategies for overcoming the session management challenges that can arise when using the Live API.

Without compression, audio-only sessions are limited to 15 minutes, and audio-video sessions are limited to 2 minutes. Exceeding these limits will terminate the session (and therefore, the connection), but you can use context window compression to extend sessions to an unlimited amount of time.

The lifetime of a connection is limited as well, to around 10 minutes. When the connection terminates, the session terminates as well. In this case, you can configure a single session to stay active over multiple connections using session resumption. You'll also receive a GoAway message before the connection ends, allowing you to take further actions.

To enable longer sessions, and avoid abrupt connection termination, you can enable context window compression by setting the contextWindowCompression field as part of the session configuration.

In the ContextWindowCompressionConfig, you can configure a sliding-window mechanism and the number of tokens that triggers compression.

To prevent session termination when the server periodically resets the WebSocket connection, configure the sessionResumption field within the setup configuration.

Passing this configuration causes the server to send SessionResumptionUpdate messages, which can be used to resume the session by passing the last resumption token as the SessionResumptionConfig.handle of the subsequent connection.

Resumption tokens are valid for 2 hr after the last sessions termination.

The server sends a GoAway message that signals that the current connection will soon be terminated. This message includes the timeLeft, indicating the remaining time and lets you take further action before the connection will be terminated as ABORTED.

The server sends a generationComplete message that signals that the model finished generating the response.

Explore more ways to work with the Live API in the full Capabilities guide, the Tool use page, or the Live API cookbook.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-12 UTC.

**Examples:**

Example 1 (python):
```python
from google.genai import types

config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    context_window_compression=(
        # Configures compression with default parameters.
        types.ContextWindowCompressionConfig(
            sliding_window=types.SlidingWindow(),
        )
    ),
)
```

Example 2 (python):
```python
from google.genai import types

config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    context_window_compression=(
        # Configures compression with default parameters.
        types.ContextWindowCompressionConfig(
            sliding_window=types.SlidingWindow(),
        )
    ),
)
```

Example 3 (javascript):
```javascript
const config = {
  responseModalities: [Modality.AUDIO],
  contextWindowCompression: { slidingWindow: {} }
};
```

Example 4 (javascript):
```javascript
const config = {
  responseModalities: [Modality.AUDIO],
  contextWindowCompression: { slidingWindow: {} }
};
```

---

## Function calling with the Gemini API

**URL:** https://ai.google.dev/gemini-api/docs/function-calling

**Contents:**
- Function calling with the Gemini API
  - Python
  - JavaScript
  - REST
- How function calling works
  - Step 1: Define a function declaration
  - Python
  - JavaScript
  - Step 2: Call the model with function declarations
  - Python

Function calling lets you connect models to external tools and APIs. Instead of generating text responses, the model determines when to call specific functions and provides the necessary parameters to execute real-world actions. This allows the model to act as a bridge between natural language and real-world actions and data. Function calling has 3 primary use cases:

Get Weather Schedule Meeting Create Chart

Function calling involves a structured interaction between your application, the model, and external functions. Here's a breakdown of the process:

This process can be repeated over multiple turns, allowing for complex interactions and workflows. The model also supports calling multiple functions in a single turn (parallel function calling) and in sequence (compositional function calling).

Define a function and its declaration within your application code that allows users to set light values and make an API request. This function could call external services or APIs.

Once you have defined your function declarations, you can prompt the model to use them. It analyzes the prompt and function declarations and decides whether to respond directly or to call a function. If a function is called, the response object will contain a function call suggestion.

The model then returns a functionCall object in an OpenAPI compatible schema specifying how to call one or more of the declared functions in order to respond to the user's question.

Extract the function call details from the model's response, parse the arguments , and execute the set_light_values function.

Finally, send the result of the function execution back to the model so it can incorporate this information into its final response to the user.

This completes the function calling flow. The model successfully used the set_light_values function to perform the request action of the user.

When you implement function calling in a prompt, you create a tools object, which contains one or more function declarations. You define functions using JSON, specifically with a select subset of the OpenAPI schema format. A single function declaration can include the following parameters:

You can also construct FunctionDeclarations from Python functions directly using types.FunctionDeclaration.from_callable(client=client, callable=your_function).

Gemini 3 and 2.5 series models use an internal "thinking" process to reason through requests. This significantly improves function calling performance, allowing the model to better determine when to call a function and which parameters to use. Because the Gemini API is stateless, models use thought signatures to maintain context across multi-turn conversations.

This section covers advanced management of thought signatures and is only necessary if you're manually constructing API requests (e.g., via REST) or manipulating conversation history.

If you're using the Google GenAI SDKs (our official libraries), you don't need to manage this process. The SDKs automatically handle the necessary steps, as shown in the earlier example.

If you modify the conversation history manually, instead of sending the complete previous response you must correctly handle the thought_signature included in the model's turn.

Follow these rules to ensure the model's context is preserved:

In Gemini 3, any Part of a model response may contain a thought signature. While we generally recommend returning signatures from all Part types, passing back thought signatures is mandatory for function calling. Unless you are manipulating conversation history manually, the Google GenAI SDK will handle thought signatures automatically.

If you are manipulating conversation history manually, refer to the Thoughts Signatures page for complete guidance and details on handling thought signatures for Gemini 3.

While not necessary for implementation, you can inspect the response to see the thought_signature for debugging or educational purposes.

Learn more about limitations and usage of thought signatures, and about thinking models in general, on the Thinking page.

In addition to single turn function calling, you can also call multiple functions at once. Parallel function calling lets you execute multiple functions at once and is used when the functions are not dependent on each other. This is useful in scenarios like gathering data from multiple independent sources, such as retrieving customer details from different databases or checking inventory levels across various warehouses or performing multiple actions such as converting your apartment into a disco.

Configure the function calling mode to allow using all of the specified tools. To learn more, you can read about configuring function calling.

Each of the printed results reflects a single function call that the model has requested. To send the results back, include the responses in the same order as they were requested.

The Python SDK supports automatic function calling, which automatically converts Python functions to declarations, handles the function call execution and response cycle for you. Following is an example for the disco use case.

Compositional or sequential function calling allows Gemini to chain multiple function calls together to fulfill a complex request. For example, to answer "Get the temperature in my current location", the Gemini API might first invoke a get_current_location() function followed by a get_weather() function that takes the location as a parameter.

The following example demonstrates how to implement compositional function calling using the Python SDK and automatic function calling.

This example uses the automatic function calling feature of the google-genai Python SDK. The SDK automatically converts the Python functions to the required schema, executes the function calls when requested by the model, and sends the results back to the model to complete the task.

When you run the code, you will see the SDK orchestrating the function calls. The model first calls get_weather_forecast, receives the temperature, and then calls set_thermostat_temperature with the correct value based on the logic in the prompt.

This example shows how to use JavaScript/TypeScript SDK to do comopositional function calling using a manual execution loop.

When you run the code, you will see the SDK orchestrating the function calls. The model first calls get_weather_forecast, receives the temperature, and then calls set_thermostat_temperature with the correct value based on the logic in the prompt.

Compositional function calling is a native Live API feature. This means Live API can handle the function calling similar to the Python SDK.

The Gemini API lets you control how the model uses the provided tools (function declarations). Specifically, you can set the mode within the.function_calling_config.

VALIDATED (Preview): The model is constrained to predict either function calls or natural language, and ensures function schema adherence. If allowed_function_names is not provided, the model picks from all of the available function declarations. If allowed_function_names is provided, the model picks from the set of allowed functions.

When using the Python SDK, you can provide Python functions directly as tools. The SDK converts these functions into declarations, manages the function call execution, and handles the response cycle for you. Define your function with type hints and a docstring. For optimal results, it is recommended to use Google-style docstrings. The SDK will then automatically:

The SDK currently does not parse argument descriptions into the property description slots of the generated function declaration. Instead, it sends the entire docstring as the top-level function description.

You can disable automatic function calling with:

The API is able to describe any of the following types. Pydantic types are allowed, as long as the fields defined on them are also composed of allowed types. Dict types (like dict[str: int]) are not well supported here, don't use them.

To see what the inferred schema looks like, you can convert it using from_callable:

You can enable multiple tools combining native tools with function calling at the same time. Here's an example that enables two tools, Grounding with Google Search and code execution, in a request using the Live API.

Python developers can try this out in the Live API Tool Use notebook.

For Gemini 3 series models, you can include multimodal content in the function response parts that you send to the model. The model can process this multimodal content in its next turn to produce a more informed response. The following MIME types are supported for multimodal content in function responses:

To include multimodal data in a function response, include it as one or more parts nested within the functionResponse part. Each multimodal part must contain inlineData. If you reference a multimodal part from within the structured response field, it must contain a unique displayName.

You can also reference a multimodal part from within the structured response field of the functionResponse part by using the JSON reference format {"$ref": "<displayName>"}. The model substitutes the reference with the multimodal content when processing the response. Each displayName can only be referenced once in the structured response field.

The following example shows a message containing a functionResponse for a function named get_image and a nested part containing image data with displayName: "wakeupcat.jpg". The functionResponse's response field references this image part:

Model Context Protocol (MCP) is an open standard for connecting AI applications with external tools and data. MCP provides a common protocol for models to access context, such as functions (tools), data sources (resources), or predefined prompts.

The Gemini SDKs have built-in support for the MCP, reducing boilerplate code and offering automatic tool calling for MCP tools. When the model generates an MCP tool call, the Python and JavaScript client SDK can automatically execute the MCP tool and send the response back to the model in a subsequent request, continuing this loop until no more tool calls are made by the model.

Here, you can find an example of how to use a local MCP server with Gemini and mcp SDK.

Make sure the latest version of the mcp SDK is installed on your platform of choice.

Make sure the latest version of the mcp SDK is installed on your platform of choice.

Built-in MCP support is a experimental feature in our SDKs and has the following limitations:

Manual integration of MCP servers is always an option if these limit what you're building.

This section lists models and their function calling capabilities. Experimental models are not included. You can find a comprehensive capabilities overview on the model overview page.

Temperature: Use a low temperature (e.g., 0) for more deterministic and reliable function calls.

Validation: If a function call has significant consequences (e.g., placing an order), validate the call with the user before executing it.

Check Finish Reason: Always check the finishReason in the model's response to handle cases where the model failed to generate a valid function call.

Error Handling: Implement robust error handling in your functions to gracefully handle unexpected inputs or API failures. Return informative error messages that the model can use to generate helpful responses to the user.

Security: Be mindful of security when calling external APIs. Use appropriate authentication and authorization mechanisms. Avoid exposing sensitive data in function calls.

Token Limits: Function descriptions and parameters count towards your input token limit. If you're hitting token limits, consider limiting the number of functions or the length of the descriptions, break down complex tasks into smaller, more focused function sets.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

# Define the function declaration for the model
schedule_meeting_function = {
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees at a given time and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of people attending the meeting.",
            },
            "date": {
                "type": "string",
                "description": "Date of the meeting (e.g., '2024-07-29')",
            },
            "time": {
                "type": "string",
                "description": "Time of the meeting (e.g., '15:00')",
            },
            "topic": {
                "type": "string",
                "description": "The subject or topic of the meeting.",
            },
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}

# Configure the client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[schedule_meeting_function])
config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about the Q3 planning.",
    config=config,
)

# Check for a function call
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    #  In a real app, you would call your function here:
    #  result = schedule_meeting(**function_call.args)
else:
    print("No function call found in the response.")
    print(response.text)
```

Example 2 (python):
```python
from google import genai
from google.genai import types

# Define the function declaration for the model
schedule_meeting_function = {
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees at a given time and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of people attending the meeting.",
            },
            "date": {
                "type": "string",
                "description": "Date of the meeting (e.g., '2024-07-29')",
            },
            "time": {
                "type": "string",
                "description": "Time of the meeting (e.g., '15:00')",
            },
            "topic": {
                "type": "string",
                "description": "The subject or topic of the meeting.",
            },
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}

# Configure the client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[schedule_meeting_function])
config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about the Q3 planning.",
    config=config,
)

# Check for a function call
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    #  In a real app, you would call your function here:
    #  result = schedule_meeting(**function_call.args)
else:
    print("No function call found in the response.")
    print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI, Type } from '@google/genai';

// Configure the client
const ai = new GoogleGenAI({});

// Define the function declaration for the model
const scheduleMeetingFunctionDeclaration = {
  name: 'schedule_meeting',
  description: 'Schedules a meeting with specified attendees at a given time and date.',
  parameters: {
    type: Type.OBJECT,
    properties: {
      attendees: {
        type: Type.ARRAY,
        items: { type: Type.STRING },
        description: 'List of people attending the meeting.',
      },
      date: {
        type: Type.STRING,
        description: 'Date of the meeting (e.g., "2024-07-29")',
      },
      time: {
        type: Type.STRING,
        description: 'Time of the meeting (e.g., "15:00")',
      },
      topic: {
        type: Type.STRING,
        description: 'The subject or topic of the meeting.',
      },
    },
    required: ['attendees', 'date', 'time', 'topic'],
  },
};

// Send request with function declarations
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Schedule a meeting with Bob and Alice for 03/27/2025 at 10:00 AM about the Q3 planning.',
  config: {
    tools: [{
      functionDeclarations: [scheduleMeetingFunctionDeclaration]
    }],
  },
});

// Check for function calls in the response
if (response.functionCalls && response.functionCalls.length > 0) {
  const functionCall = response.functionCalls[0]; // Assuming one function call
  console.log(`Function to call: ${functionCall.name}`);
  console.log(`Arguments: ${JSON.stringify(functionCall.args)}`);
  // In a real app, you would call your actual function here:
  // const result = await scheduleMeeting(functionCall.args);
} else {
  console.log("No function call found in the response.");
  console.log(response.text);
}
```

Example 4 (python):
```python
import { GoogleGenAI, Type } from '@google/genai';

// Configure the client
const ai = new GoogleGenAI({});

// Define the function declaration for the model
const scheduleMeetingFunctionDeclaration = {
  name: 'schedule_meeting',
  description: 'Schedules a meeting with specified attendees at a given time and date.',
  parameters: {
    type: Type.OBJECT,
    properties: {
      attendees: {
        type: Type.ARRAY,
        items: { type: Type.STRING },
        description: 'List of people attending the meeting.',
      },
      date: {
        type: Type.STRING,
        description: 'Date of the meeting (e.g., "2024-07-29")',
      },
      time: {
        type: Type.STRING,
        description: 'Time of the meeting (e.g., "15:00")',
      },
      topic: {
        type: Type.STRING,
        description: 'The subject or topic of the meeting.',
      },
    },
    required: ['attendees', 'date', 'time', 'topic'],
  },
};

// Send request with function declarations
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Schedule a meeting with Bob and Alice for 03/27/2025 at 10:00 AM about the Q3 planning.',
  config: {
    tools: [{
      functionDeclarations: [scheduleMeetingFunctionDeclaration]
    }],
  },
});

// Check for function calls in the response
if (response.functionCalls && response.functionCalls.length > 0) {
  const functionCall = response.functionCalls[0]; // Assuming one function call
  console.log(`Function to call: ${functionCall.name}`);
  console.log(`Arguments: ${JSON.stringify(functionCall.args)}`);
  // In a real app, you would call your actual function here:
  // const result = await scheduleMeeting(functionCall.args);
} else {
  console.log("No function call found in the response.");
  console.log(response.text);
}
```

---

## Available regions for Google AI Studio and Gemini API

**URL:** https://ai.google.dev/gemini-api/docs/available-regions

**Contents:**
- Available regions for Google AI Studio and Gemini API
- Available regions

If you reached this page after trying to open Google AI Studio, it may be because Google AI Studio is not available in your region, or you don't meet the age requirements (18+) for access. You can learn more about the available regions in the following section and other requirements in the terms of service.

The Gemini API and Google AI Studio are available in the following countries and territories. If you're not in one of these countries or territories, try the Gemini API in Vertex AI:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

---

## Speech generation (text-to-speech)

**URL:** https://ai.google.dev/gemini-api/docs/speech-generation

**Contents:**
- Speech generation (text-to-speech)
- Before you begin
- Single-speaker text-to-speech
  - Python
  - JavaScript
  - REST
- Multi-speaker text-to-speech
  - Python
  - JavaScript
  - REST

The Gemini API can transform text input into single speaker or multi-speaker audio using native text-to-speech (TTS) generation capabilities. Text-to-speech (TTS) generation is controllable, meaning you can use natural language to structure interactions and guide the style, accent, pace, and tone of the audio.

The TTS capability differs from speech generation provided through the Live API, which is designed for interactive, unstructured audio, and multimodal inputs and outputs. While the Live API excels in dynamic conversational contexts, TTS through the Gemini API is tailored for scenarios that require exact text recitation with fine-grained control over style and sound, such as podcast or audiobook generation.

This guide shows you how to generate single-speaker and multi-speaker audio from text.

Ensure you use a Gemini 2.5 model variant with native text-to-speech (TTS) capabilities, as listed in the Supported models section. For optimal results, consider which model best fits your specific use case.

You may find it useful to test the Gemini 2.5 TTS models in AI Studio before you start building.

To convert text to single-speaker audio, set the response modality to "audio", and pass a SpeechConfig object with VoiceConfig set. You'll need to choose a voice name from the prebuilt output voices.

This example saves the output audio from the model in a wave file:

For more code samples, refer to the "TTS - Get Started" file in the cookbooks repository:

For multi-speaker audio, you'll need a MultiSpeakerVoiceConfig object with each speaker (up to 2) configured as a SpeakerVoiceConfig. You'll need to define each speaker with the same names used in the prompt:

You can control style, tone, accent, and pace using natural language prompts for both single- and multi-speaker TTS. For example, in a single-speaker prompt, you can say:

In a multi-speaker prompt, provide the model with each speaker's name and corresponding transcript. You can also provide guidance for each speaker individually:

Try using a voice option that corresponds to the style or emotion you want to convey, to emphasize it even more. In the previous prompt, for example, Enceladus's breathiness might emphasize "tired" and "bored", while Puck's upbeat tone could complement "excited" and "happy".

The TTS models only output audio, but you can use other models to generate a transcript first, then pass that transcript to the TTS model to read aloud.

TTS models support the following 30 voice options in the voice_name field:

You can hear all the voice options in AI Studio.

The TTS models detect the input language automatically. They support the following 24 languages:

The Gemini Native Audio Generation Text-to-Speech (TTS) model differentiates itself from traditional TTS models by using a large language model that knows not only what to say, but also how to say it.

To unlock this capability, users can think of themselves as directors setting a scene for a virtual voice talent to perform. To craft a prompt, we recommend considering the following components: an Audio Profile that defines the character's core identity and archetype; a Scene description that establishes the physical environment and emotional "vibe"; and Director's Notes that offer more precise performance guidance regarding style, accent and pace control.

By providing nuanced instructions such as a precise regional accent, specific paralinguistic features (e.g. breathiness), or pacing, users can leverage the model's context awareness to generate highly dynamic, natural and expressive audio performances. For optimal performance, we recommend the Transcript and directorial prompts align, so that "who is saying it" matches with "what is said" and "how it is being said."

The purpose of this guide is to offer fundamental direction and spark ideas when developing audio experiences using Gemini TTS audio generation. We are excited to witness what you create!

A robust prompt ideally includes the following elements that come together to craft a great performance:

Let's break down each element of the prompt.

Briefly describe the persona of the character.

Set the context for the scene, including location, mood, and environmental details that establish the tone and vibe. Describe what is happening around the character and how it affects them. The scene provides the environmental context for the entire interaction and guides the acting performance in a subtle, organic way.

This critical section includes specific performance guidance. You can skip all the other elements, but we recommend you include this element.

Define only what's important to the performance, being careful to not overspecify. Too many strict rules will limit the models' creativity and may result in a worse performance. Balance the role and scene description with the specific performance rules.

The most common directions are Style, Pacing and Accent, but the model is not limited to these, nor requires them. Feel free to include custom instructions to cover any additional details important to your performance, and go into as much or as little detail as necessary.

Sets the tone and Style of the generated speech. Include things like upbeat, energetic, relaxed, bored etc. to guide the performance. Be descriptive and provide as much detail as necessary: "Infectious enthusiasm. The listener should feel like they are part of a massive, exciting community event." works better than simply saying "energetic and enthusiastic".

You can even try terms that are popular in the voiceover industry, like "vocal smile". You can layer as many style characteristics as you want.

Describe the desired accent. The more specific you are, the better the results are. For example use "British English accent as heard in Croydon, England" vs "British Accent".

Overall pacing and pace variation throughout the piece.

Try some of these examples yourself on AI Studio, play with our TTS App and let Gemini put you in the directors chair. Keep these tips in mind to make great vocal performances:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-10 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types
import wave

# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

client = genai.Client()

response = client.models.generate_content(
   model="gemini-2.5-flash-preview-tts",
   contents="Say cheerfully: Have a wonderful day!",
   config=types.GenerateContentConfig(
      response_modalities=["AUDIO"],
      speech_config=types.SpeechConfig(
         voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
               voice_name='Kore',
            )
         )
      ),
   )
)

data = response.candidates[0].content.parts[0].inline_data.data

file_name='out.wav'
wave_file(file_name, data) # Saves the file to current directory
```

Example 2 (python):
```python
from google import genai
from google.genai import types
import wave

# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)

client = genai.Client()

response = client.models.generate_content(
   model="gemini-2.5-flash-preview-tts",
   contents="Say cheerfully: Have a wonderful day!",
   config=types.GenerateContentConfig(
      response_modalities=["AUDIO"],
      speech_config=types.SpeechConfig(
         voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
               voice_name='Kore',
            )
         )
      ),
   )
)

data = response.candidates[0].content.parts[0].inline_data.data

file_name='out.wav'
wave_file(file_name, data) # Saves the file to current directory
```

Example 3 (python):
```python
import {GoogleGenAI} from '@google/genai';
import wav from 'wav';

async function saveWaveFile(
   filename,
   pcmData,
   channels = 1,
   rate = 24000,
   sampleWidth = 2,
) {
   return new Promise((resolve, reject) => {
      const writer = new wav.FileWriter(filename, {
            channels,
            sampleRate: rate,
            bitDepth: sampleWidth * 8,
      });

      writer.on('finish', resolve);
      writer.on('error', reject);

      writer.write(pcmData);
      writer.end();
   });
}

async function main() {
   const ai = new GoogleGenAI({});

   const response = await ai.models.generateContent({
      model: "gemini-2.5-flash-preview-tts",
      contents: [{ parts: [{ text: 'Say cheerfully: Have a wonderful day!' }] }],
      config: {
            responseModalities: ['AUDIO'],
            speechConfig: {
               voiceConfig: {
                  prebuiltVoiceConfig: { voiceName: 'Kore' },
               },
            },
      },
   });

   const data = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
   const audioBuffer = Buffer.from(data, 'base64');

   const fileName = 'out.wav';
   await saveWaveFile(fileName, audioBuffer);
}
await main();
```

Example 4 (python):
```python
import {GoogleGenAI} from '@google/genai';
import wav from 'wav';

async function saveWaveFile(
   filename,
   pcmData,
   channels = 1,
   rate = 24000,
   sampleWidth = 2,
) {
   return new Promise((resolve, reject) => {
      const writer = new wav.FileWriter(filename, {
            channels,
            sampleRate: rate,
            bitDepth: sampleWidth * 8,
      });

      writer.on('finish', resolve);
      writer.on('error', reject);

      writer.write(pcmData);
      writer.end();
   });
}

async function main() {
   const ai = new GoogleGenAI({});

   const response = await ai.models.generateContent({
      model: "gemini-2.5-flash-preview-tts",
      contents: [{ parts: [{ text: 'Say cheerfully: Have a wonderful day!' }] }],
      config: {
            responseModalities: ['AUDIO'],
            speechConfig: {
               voiceConfig: {
                  prebuiltVoiceConfig: { voiceName: 'Kore' },
               },
            },
      },
   });

   const data = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
   const audioBuffer = Buffer.from(data, 'base64');

   const fileName = 'out.wav';
   await saveWaveFile(fileName, audioBuffer);
}
await main();
```

---

## Thought Signatures

**URL:** https://ai.google.dev/gemini-api/docs/thought-signatures

**Contents:**
- Thought Signatures
- How it works
- Signatures in function calling parts
  - Sequential function calling example
  - Parallel function calling example
- Signatures in non functionCall parts
  - Text/In-context reasoning (No validation)
- Signatures for OpenAI compatibility
  - Sequential function calling example
  - Parallel function calling example

Thought signatures are encrypted representations of the model's internal thought process and are used to preserve reasoning context across multi-turn interactions. When using thinking models (such as the Gemini 3 and 2.5 series), the API may return a thoughtSignature field within the content parts of the response (e.g., text or functionCall parts).

As a general rule, if you receive a thought signature in a model response, you should pass it back exactly as received when sending the conversation history in the next turn. When using Gemini 3 models, you must pass back thought signatures during function calling, otherwise you will get a validation error (4xx status code). This includes when using the minimal thinking level setting for Gemini 3 Flash.

The graphic below visualizes the meaning of "turn" and "step" as they pertain to function calling in the Gemini API. A "turn" is a single, complete exchange in a conversation between a user and a model. A "step" is a finer-grained action or operation performed by the model, often as part of a larger process to complete a turn.

This document focuses on handling function calling for Gemini 3 models. Refer to the model behavior section for discrepancies with 2.5.

Gemini 3 returns thought signatures for all model responses (responses from the API) with a function call. Thought signatures show up in the following cases:

The following table provides a visualization for multi-step function calls, combining the definitions of turns and steps with the concept of signatures introduced above:

When Gemini generates a functionCall, it relies on the thought_signature to process the tool's output correctly in the next turn.

This section shows an example of multiple function calls where the user asks a complex question requiring multiple tasks.

Let's walk through a multiple-turn function calling example where the user asks a complex question requiring multiple tasks: "Check flight status for AA100 and book a taxi if delayed".

The following code illustrates the sequence in the above table.

Turn 1, Step 1 (User request)

Turn 1, Step 1 (Model response)

Turn 1, Step 2 (User response - Sending tool outputs) Since this user turn only contains a functionResponse (no fresh text), we are still in Turn 1. We must preserve <Signature_A>.

Turn 1, Step 2 (Model) The model now decides to book a taxi based on the previous tool output.

Turn 1, Step 3 (User - Sending tool output) To send the taxi booking confirmation, we must include signatures for ALL function calls in this loop (<Signature A> + <Signature B>).

Let's walk through a parallel function calling example where the users asks "Check weather in Paris and London" to see where the model does validation.

request1="Check the weather in Paris and London"

FC1 ("Paris") + signature

request 2 = request1 + FC1 ("Paris") + signature + FC2 ("London")

The following code illustrates the sequence in the above table.

Turn 1, Step 1 (User request)

Turn 1, Step 1 (Model response)

Turn 1, Step 2 (User response - Sending tool outputs) We must preserve <Signature_A> on the first part exactly as received.

Gemini may also return thought_signatures in the final part of the response in non-function-call parts.

Turn 1, Step 1 (Model response)

Turn 2, Step 1 (User)

The following examples shows how to handle thought signatures for a chat completion API using OpenAI compatibility.

This is an example of multiple function calling where the user asks a complex question requiring multiple tasks.

Let's walk through a multiple-turn function calling example where the user asks Check flight status for AA100 and book a taxi if delayed and you can see what happens when the user asks a complex question requiring multiple tasks.

The following code walks through the given sequence.

Turn 1, Step 1 (User Request)

Turn 1, Step 1 (Model Response)

Turn 1, Step 2 (User Response - Sending Tool Outputs)

Since this user turn only contains a functionResponse (no fresh text), we are still in Turn 1 and must preserve <Signature_A>.

Turn 1, Step 2 (Model)

The model now decides to book a taxi based on the previous tool output.

Turn 1, Step 3 (User - Sending Tool Output)

To send the taxi booking confirmation, we must include signatures for ALL function calls in this loop (<Signature A> + <Signature B>).

Let's walk through a parallel function calling example where the users asks "Check weather in Paris and London" and you can see where the model does validation.

Here's the code to walk through the given sequence.

Turn 1, Step 1 (User Request)

Turn 1, Step 1 (Model Response)

Turn 1, Step 2 (User Response - Sending Tool Outputs)

You must preserve <Signature_A> on the first part exactly as received.

How do I transfer history from a different model to Gemini 3 with a function call part in the current turn and step? I need to provide function call parts that were not generated by the API and therefore don't have an associated thought signature?

While injecting custom function call blocks into the request is strongly discouraged, in cases where it can't be avoided, e.g. providing information to the model on function calls and responses that were executed deterministically by the client, or transferring a trace from a different model that does not include thought signatures, you can set the following dummy signatures of either "context_engineering_is_the_way_to_go" or "skip_thought_signature_validator" in the thought signature field to skip validation.

I am sending back interleaved parallel function calls and responses and the API is returning a 400. Why?

When the API returns parallel function calls "FC1 + signature, FC2", the user response expected is "FC1+ signature, FC2, FR1, FR2". If you have them interleaved as "FC1 + signature, FR1, FC2, FR2" the API will return a 400 error.

When streaming and the model is not returning a function call I can't find the thought signature

During a model response not containing a FC with a streaming request, the model may return the thought signature in a part with an empty text content part. It is advisable to parse the entire request until the finish_reason is returned by the model.

Gemini 3 Pro and Flash, Gemini 3 Pro Image and Gemini 2.5 models each behave differently with thought signatures. For Gemini 3 Pro Image see the thinking process section of the image generation guide.

Gemini 3 models and Gemini 2.5 models behave differently with thought signatures in function calls:

For Gemini 2.5 models thought signature behavior, refer to the Thinking page.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (unknown):
```unknown
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "Check flight status for AA100 and book a taxi 2 hours before if delayed."
        }
      ]
    }
  ],
  "tools": [
    {
      "functionDeclarations": [
        {
          "name": "check_flight",
          "description": "Gets the current status of a flight",
          "parameters": {
            "type": "object",
            "properties": {
              "flight": {
                "type": "string",
                "description": "The flight number to check"
              }
            },
            "required": [
              "flight"
            ]
          }
        },
        {
          "name": "book_taxi",
          "description": "Book a taxi",
          "parameters": {
            "type": "object",
            "properties": {
              "time": {
                "type": "string",
                "description": "time to book the taxi"
              }
            },
            "required": [
              "time"
            ]
          }
        }
      ]
    }
  ]
}
```

Example 2 (unknown):
```unknown
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "Check flight status for AA100 and book a taxi 2 hours before if delayed."
        }
      ]
    }
  ],
  "tools": [
    {
      "functionDeclarations": [
        {
          "name": "check_flight",
          "description": "Gets the current status of a flight",
          "parameters": {
            "type": "object",
            "properties": {
              "flight": {
                "type": "string",
                "description": "The flight number to check"
              }
            },
            "required": [
              "flight"
            ]
          }
        },
        {
          "name": "book_taxi",
          "description": "Book a taxi",
          "parameters": {
            "type": "object",
            "properties": {
              "time": {
                "type": "string",
                "description": "time to book the taxi"
              }
            },
            "required": [
              "time"
            ]
          }
        }
      ]
    }
  ]
}
```

Example 3 (unknown):
```unknown
{
"content": {
        "role": "model",
        "parts": [
          {
            "functionCall": {
              "name": "check_flight",
              "args": {
                "flight": "AA100"
              }
            },
            "thoughtSignature": "<Signature A>"
          }
        ]
  }
}
```

Example 4 (unknown):
```unknown
{
"content": {
        "role": "model",
        "parts": [
          {
            "functionCall": {
              "name": "check_flight",
              "args": {
                "flight": "AA100"
              }
            },
            "thoughtSignature": "<Signature A>"
          }
        ]
  }
}
```

---

## API versions explained

**URL:** https://ai.google.dev/gemini-api/docs/api-versions

**Contents:**
- API versions explained
- Configure API version in an SDK
  - Python
  - JavaScript
  - REST

This document provides a high-level overview of the differences between the v1 and v1beta versions of the Gemini API.

The Gemini API SDK's default to v1beta, but you can opt to use other versions by setting the API version as shown in the following code sample:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-11 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client(http_options={'api_version': 'v1alpha'})

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents="Explain how AI works",
)

print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client(http_options={'api_version': 'v1alpha'})

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents="Explain how AI works",
)

print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({
  httpOptions: { apiVersion: "v1alpha" },
});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.0-flash",
    contents: "Explain how AI works",
  });
  console.log(response.text);
}

await main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({
  httpOptions: { apiVersion: "v1alpha" },
});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.0-flash",
    contents: "Explain how AI works",
  });
  console.log(response.text);
}

await main();
```

---

## Gemini models

**URL:** https://ai.google.dev/gemini-api/docs/models

**Contents:**
- Gemini models
- Gemini 3 Pro
  - Expand to learn more
    - Model details
  - Gemini 3 Pro Preview
  - Gemini 3 Pro Image Preview
- Gemini 3 Flash
  - Expand to learn more
    - Model details
  - Gemini 3 Flash Preview

OUR MOST INTELLIGENT MODEL

The best model in the world for multimodal understanding, and our most powerful agentic and vibe-coding model yet, delivering richer visuals and deeper interactivity, all built on a foundation of state-of-the-art reasoning.

Try in Google AI Studio

Text, Image, Video, Audio, and PDF

Grounding with Google Maps

Grounding with Google Maps

OUR MOST INTELLIGENT MODEL

Our most intelligent model built for speed, combining frontier intelligence with superior search and grounding.

Try in Google AI Studio

Text, Image, Video, Audio, and PDF

Grounding with Google Maps

Our best model in terms of price-performance, offering well-rounded capabilities. 2.5 Flash is best for large scale processing, low-latency, high volume tasks that require thinking, and agentic use cases.

Try in Google AI Studio

Text, images, video, audio

Grounding with Google Maps

Text, images, video, audio

Grounding with Google Maps

Grounding with Google Maps

Grounding with Google Maps

Grounding with Google Maps

Our fastest flash model optimized for cost-efficiency and high throughput.

Try in Google AI Studio

Text, image, video, audio, PDF

Grounding with Google Maps

Text, image, video, audio, PDF

Grounding with Google Maps

OUR ADVANCED THINKING MODEL

Our state-of-the-art thinking model, capable of reasoning over complex problems in code, math, and STEM, as well as analyzing large datasets, codebases, and documents using long context.

Try in Google AI Studio

Audio, images, video, text, and PDF

Grounding with Google Maps

Grounding with Google Maps

OUR SECOND GENERATION WORKHORSE MODEL

Our second generation workhorse model, with a 1 million token context window.

Gemini 2.0 Flash delivers next-gen features and improved capabilities, including superior speed, native tool use, and a 1M token context window.

Try in Google AI Studio

Audio, images, video, and text

Grounding with Google Maps

Audio, images, video, and text

Grounding with Google Maps

gemini-2.0-flash-preview-image-generation is not currently supported in a number of countries in Europe, Middle East & Africa

OUR SECOND GENERATION FAST MODEL

Our second generation small workhorse model, with a 1 million token context window.

A Gemini 2.0 Flash model optimized for cost efficiency and low latency.

Try in Google AI Studio

Audio, images, video, and text

Grounding with Google Maps

Gemini models are available in either stable, preview, latest, or experimental versions.

Points to a specific stable model. Stable models usually don't change. Most production apps should use a specific stable model.

For example: gemini-2.5-flash.

Points to a preview model which may be used for production. Preview models will typically have billing enabled, might come with more restrictive rate limits and will be deprecated with at least 2 weeks notice.

For example: gemini-2.5-flash-preview-09-2025.

Points to the latest release for a specific model variation. This can be a stable, preview or experimental release. This alias will get hot-swapped with every new release of a specific model variation. A 2-week notice will be provided through email before the version behind latest is changed.

For example: gemini-flash-latest.

Points to an experimental model which will typically be not be suitable for production use and come with more restrictive rate limits. We release experimental models to gather feedback and get our latest updates into the hands of developers quickly.

Experimental models are not stable and availability of model endpoints is subject to change.

For information about model deprecations, visit the Gemini deprecations page.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

---

## Gemini API

**URL:** https://ai.google.dev/gemini-api/docs

**Contents:**
- Gemini API
  - Python
  - JavaScript
  - Go
  - Java
  - C#
  - REST
- Meet the models
- Explore Capabilities
- Resources

The fastest path from prompt to production with Gemini, Veo, Nano Banana, and more.

Follow our Quickstart guide to get an API key and make your first API call in minutes.

auto_awesome Gemini 3 Pro

Our most intelligent model, the best in the world for multimodal understanding, all built on state-of-the-art reasoning.

Frontier-class performance rivaling larger models at a fraction of the cost.

🍌 Nano Banana and Nano Banana Pro

State-of-the-art image generation and editing models.

Our powerful reasoning model, which excels at coding and complex reasonings tasks.

spark Gemini 2.5 Flash

Our most balanced model, with a 1 million token context window and more.

spark Gemini 2.5 Flash-Lite

Our fastest and most cost-efficient multimodal model with great performance for high-frequency tasks.

video_library Veo 3.1

Our state-of-the-art video generation model, with native audio.

spark Gemini 2.5 Pro TTS

Gemini 2.5 model variant with native text-to-speech (TTS) capabilities.

spark Gemini Robotics-ER 1.5

A vision-language model (VLM) that brings Gemini's agentic capabilities to robotics and enables advanced reasoning in the physical world.

Native Image Generation (Nano Banana)

Generate and edit highly contextual images natively with Gemini 2.5 Flash Image.

Input millions of tokens to Gemini models and derive understanding from unstructured images, videos, and documents.

Constrain Gemini to respond with JSON, a structured data format suitable for automated processing.

Build agentic workflows by connecting Gemini to external APIs and tools.

Video Generation with Veo 3.1

Create high-quality video content from text or image prompts with our state-of-the-art model.

Voice Agents with Live API

Build real-time voice applications and agents with the Live API.

Connect Gemini to the world through built-in tools like Google Search, URL Context, Google Maps, Code Execution and Computer Use.

Document Understanding

Process up to 1000 pages of PDF files with full multimodal understanding or other text-based file types.

Explore how thinking capabilities improve reasoning for complex tasks and agents.

Test prompts, manage your API keys, monitor usage, and build prototypes in platform for AI builders.

Open Google AI Studio

group Developer Community

Ask questions and find solutions from other developers and Google engineers.

menu_book API Reference

Find detailed information about the Gemini API in the official reference documentation.

Read the API reference

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words",
)

print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words",
)

print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "Explain how AI works in a few words",
  });
  console.log(response.text);
}

await main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "Explain how AI works in a few words",
  });
  console.log(response.text);
}

await main();
```

---

## Gemini Developer API v.s. Vertex AI

**URL:** https://ai.google.dev/gemini-api/docs/migrate-to-cloud

**Contents:**
- Gemini Developer API v.s. Vertex AI
- Code comparison
  - Python
  - Gemini Developer API
  - Vertex AI Gemini API
  - JavaScript and TypeScript
  - Gemini Developer API
  - Vertex AI Gemini API
  - Go
  - Gemini Developer API

When developing generative AI solutions with Gemini, Google offers two API products: the Gemini Developer API and the Vertex AI Gemini API.

The Gemini Developer API provides the fastest path to build, productionize, and scale Gemini powered applications. Most developers should use the Gemini Developer API unless there is a need for specific enterprise controls.

Vertex AI offers a comprehensive ecosystem of enterprise ready features and services for building and deploying generative AI applications backed by the Google Cloud Platform.

We've recently simplified migrating between these services. Both the Gemini Developer API and the Vertex AI Gemini API are now accessible through the unified Google Gen AI SDK.

This page has side-by-side code comparisons between Gemini Developer API and Vertex AI quickstarts for text generation.

You can access both the Gemini Developer API and Vertex AI services through the google-genai library. See the libraries page for instructions on how to install google-genai.

You can access both Gemini Developer API and Vertex AI services through @google/genai library. See libraries page for instructions on how to install @google/genai.

You can access both Gemini Developer API and Vertex AI services through google.golang.org/genai library. See libraries page for instructions on how to install google.golang.org/genai.

Refer to use case specific guides on Gemini Developer API Documentation and Vertex AI documentation for other platforms and use cases.

You'll need to use Google Cloud service accounts to authenticate. See the Vertex AI documentation for more information.

You can use your existing Google Cloud project (the same one you used to generate your API key) or you can create a new Google Cloud project.

Supported regions may differ between the Gemini Developer API and the Vertex AI Gemini API. See the list of supported regions for generative AI on Google Cloud.

Any models you created in Google AI Studio need to be retrained in Vertex AI.

If you no longer need to use your Gemini API key for the Gemini Developer API, then follow security best practices and delete it.

To delete an API key:

Open the Google Cloud API Credentials page.

Find the API key you want to delete and click the Actions icon.

Select Delete API key.

In the Delete credential modal, select Delete.

Deleting an API key takes a few minutes to propagate. After propagation completes, any traffic using the deleted API key is rejected.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)
```

Example 3 (python):
```python
from google import genai

client = genai.Client(
    vertexai=True, project='your-project-id', location='us-central1'
)

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)
```

Example 4 (python):
```python
from google import genai

client = genai.Client(
    vertexai=True, project='your-project-id', location='us-central1'
)

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)
```

---

## Gemini deprecations

**URL:** https://ai.google.dev/gemini-api/docs/deprecations

**Contents:**
- Gemini deprecations
- Gemini 2.0 models
- Gemini 2.5 Flash models
- Gemini 2.5 Pro models
- Recently deprecated
  - Live API models
  - Imagen 3 models

This page lists the known deprecation schedules for stable (GA) models in the Gemini API. A "deprecation" is the announcement that we no longer provide support for a model, and that it will be "shut down" in the near future. Once a model is "shutdown", it is completely turned off, and the endpoint is no longer available.

Preview model deprecations are documented on the Release notes page.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-12 UTC.

---

## Context caching

**URL:** https://ai.google.dev/gemini-api/docs/caching?lang=python

**Contents:**
- Context caching
- Implicit caching
- Explicit caching
  - Generate content using a cache
  - Videos
  - PDFs
  - List caches
  - Update a cache
  - Delete a cache
  - Explicit caching using the OpenAI library

Python JavaScript Go REST

In a typical AI workflow, you might pass the same input tokens over and over to a model. The Gemini API offers two different caching mechanisms:

Explicit caching is useful in cases where you want to guarantee cost savings, but with some added developer work.

Implicit caching is enabled by default for all Gemini 2.5 models. We automatically pass on cost savings if your request hits caches. There is nothing you need to do in order to enable this. It is effective as of May 8th, 2025. The minimum input token count for context caching is listed in the following table for each model:

To increase the chance of an implicit cache hit:

You can see the number of tokens which were cache hits in the response object's usage_metadata field.

Using the Gemini API explicit caching feature, you can pass some content to the model once, cache the input tokens, and then refer to the cached tokens for subsequent requests. At certain volumes, using cached tokens is lower cost than passing in the same corpus of tokens repeatedly.

When you cache a set of tokens, you can choose how long you want the cache to exist before the tokens are automatically deleted. This caching duration is called the time to live (TTL). If not set, the TTL defaults to 1 hour. The cost for caching depends on the input token size and how long you want the tokens to persist.

This section assumes that you've installed a Gemini SDK (or have curl installed) and that you've configured an API key, as shown in the quickstart.

The following example shows how to generate content using a cached system instruction and video file.

It's not possible to retrieve or view cached content, but you can retrieve cache metadata (name, model, display_name, usage_metadata, create_time, update_time, and expire_time).

To list metadata for all uploaded caches, use CachedContent.list():

To fetch the metadata for one cache object, if you know its name, use get:

You can set a new ttl or expire_time for a cache. Changing anything else about the cache isn't supported.

The following example shows how to update the ttl of a cache using client.caches.update().

To set the expiry time, it will accepts either a datetime object or an ISO-formatted datetime string (dt.isoformat(), like 2025-01-27T16:02:36.473528+00:00). Your time must include a time zone (datetime.utcnow() doesn't attach a time zone, datetime.now(datetime.timezone.utc) does attach a time zone).

The caching service provides a delete operation for manually removing content from the cache. The following example shows how to delete a cache:

If you're using an OpenAI library, you can enable explicit caching using the cached_content property on extra_body.

Context caching is particularly well suited to scenarios where a substantial initial context is referenced repeatedly by shorter requests. Consider using context caching for use cases such as:

Context caching is a paid feature designed to reduce overall operational costs. Billing is based on the following factors:

For up-to-date pricing details, refer to the Gemini API pricing page. To learn how to count tokens, see the Token guide.

Keep the following considerations in mind when using context caching:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-08 UTC.

**Examples:**

Example 1 (python):
```python
import os
import pathlib
import requests
import time

from google import genai
from google.genai import types

client = genai.Client()

# Download video file
url = 'https://storage.googleapis.com/generativeai-downloads/data/SherlockJr._10min.mp4'
path_to_video_file = pathlib.Path('SherlockJr._10min.mp4')
if not path_to_video_file.exists():
  with path_to_video_file.open('wb') as wf:
    response = requests.get(url, stream=True)
    for chunk in response.iter_content(chunk_size=32768):
      wf.write(chunk)

# Upload the video using the Files API
video_file = client.files.upload(file=path_to_video_file)

# Wait for the file to finish processing
while video_file.state.name == 'PROCESSING':
  print('Waiting for video to be processed.')
  time.sleep(2)
  video_file = client.files.get(name=video_file.name)

print(f'Video processing complete: {video_file.uri}')

# You must use an explicit version suffix: "-flash-001", not just "-flash".
model='models/gemini-2.0-flash-001'

# Create a cache with a 5 minute TTL
cache = client.caches.create(
    model=model,
    config=types.CreateCachedContentConfig(
      display_name='sherlock jr movie', # used to identify the cache
      system_instruction=(
          'You are an expert video analyzer, and your job is to answer '
          'the user\'s query based on the video file you have access to.'
      ),
      contents=[video_file],
      ttl="300s",
  )
)

# Construct a GenerativeModel which uses the created cache.
response = client.models.generate_content(
  model = model,
  contents= (
    'Introduce different characters in the movie by describing '
    'their personality, looks, and names. Also list the timestamps '
    'they were introduced for the first time.'),
  config=types.GenerateContentConfig(cached_content=cache.name)
)

print(response.usage_metadata)

# The output should look something like this:
#
# prompt_token_count: 696219
# cached_content_token_count: 696190
# candidates_token_count: 214
# total_token_count: 696433

print(response.text)
```

Example 2 (python):
```python
import os
import pathlib
import requests
import time

from google import genai
from google.genai import types

client = genai.Client()

# Download video file
url = 'https://storage.googleapis.com/generativeai-downloads/data/SherlockJr._10min.mp4'
path_to_video_file = pathlib.Path('SherlockJr._10min.mp4')
if not path_to_video_file.exists():
  with path_to_video_file.open('wb') as wf:
    response = requests.get(url, stream=True)
    for chunk in response.iter_content(chunk_size=32768):
      wf.write(chunk)

# Upload the video using the Files API
video_file = client.files.upload(file=path_to_video_file)

# Wait for the file to finish processing
while video_file.state.name == 'PROCESSING':
  print('Waiting for video to be processed.')
  time.sleep(2)
  video_file = client.files.get(name=video_file.name)

print(f'Video processing complete: {video_file.uri}')

# You must use an explicit version suffix: "-flash-001", not just "-flash".
model='models/gemini-2.0-flash-001'

# Create a cache with a 5 minute TTL
cache = client.caches.create(
    model=model,
    config=types.CreateCachedContentConfig(
      display_name='sherlock jr movie', # used to identify the cache
      system_instruction=(
          'You are an expert video analyzer, and your job is to answer '
          'the user\'s query based on the video file you have access to.'
      ),
      contents=[video_file],
      ttl="300s",
  )
)

# Construct a GenerativeModel which uses the created cache.
response = client.models.generate_content(
  model = model,
  contents= (
    'Introduce different characters in the movie by describing '
    'their personality, looks, and names. Also list the timestamps '
    'they were introduced for the first time.'),
  config=types.GenerateContentConfig(cached_content=cache.name)
)

print(response.usage_metadata)

# The output should look something like this:
#
# prompt_token_count: 696219
# cached_content_token_count: 696190
# candidates_token_count: 214
# total_token_count: 696433

print(response.text)
```

Example 3 (python):
```python
from google import genai
from google.genai import types
import io
import httpx

client = genai.Client()

long_context_pdf_path = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"

# Retrieve and upload the PDF using the File API
doc_io = io.BytesIO(httpx.get(long_context_pdf_path).content)

document = client.files.upload(
  file=doc_io,
  config=dict(mime_type='application/pdf')
)

model_name = "gemini-2.0-flash-001"
system_instruction = "You are an expert analyzing transcripts."

# Create a cached content object
cache = client.caches.create(
    model=model_name,
    config=types.CreateCachedContentConfig(
      system_instruction=system_instruction,
      contents=[document],
    )
)

# Display the cache details
print(f'{cache=}')

# Generate content using the cached prompt and document
response = client.models.generate_content(
  model=model_name,
  contents="Please summarize this transcript",
  config=types.GenerateContentConfig(
    cached_content=cache.name
  ))

# (Optional) Print usage metadata for insights into the API call
print(f'{response.usage_metadata=}')

# Print the generated text
print('\n\n', response.text)
```

Example 4 (python):
```python
from google import genai
from google.genai import types
import io
import httpx

client = genai.Client()

long_context_pdf_path = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"

# Retrieve and upload the PDF using the File API
doc_io = io.BytesIO(httpx.get(long_context_pdf_path).content)

document = client.files.upload(
  file=doc_io,
  config=dict(mime_type='application/pdf')
)

model_name = "gemini-2.0-flash-001"
system_instruction = "You are an expert analyzing transcripts."

# Create a cached content object
cache = client.caches.create(
    model=model_name,
    config=types.CreateCachedContentConfig(
      system_instruction=system_instruction,
      contents=[document],
    )
)

# Display the cache details
print(f'{cache=}')

# Generate content using the cached prompt and document
response = client.models.generate_content(
  model=model_name,
  contents="Please summarize this transcript",
  config=types.GenerateContentConfig(
    cached_content=cache.name
  ))

# (Optional) Print usage metadata for insights into the API call
print(f'{response.usage_metadata=}')

# Print the generated text
print('\n\n', response.text)
```

---

## Function calling with the Gemini API

**URL:** https://ai.google.dev/gemini-api/docs/function-calling?example=meeting

**Contents:**
- Function calling with the Gemini API
  - Python
  - JavaScript
  - REST
- How function calling works
  - Step 1: Define a function declaration
  - Python
  - JavaScript
  - Step 2: Call the model with function declarations
  - Python

Function calling lets you connect models to external tools and APIs. Instead of generating text responses, the model determines when to call specific functions and provides the necessary parameters to execute real-world actions. This allows the model to act as a bridge between natural language and real-world actions and data. Function calling has 3 primary use cases:

Get Weather Schedule Meeting Create Chart

Function calling involves a structured interaction between your application, the model, and external functions. Here's a breakdown of the process:

This process can be repeated over multiple turns, allowing for complex interactions and workflows. The model also supports calling multiple functions in a single turn (parallel function calling) and in sequence (compositional function calling).

Define a function and its declaration within your application code that allows users to set light values and make an API request. This function could call external services or APIs.

Once you have defined your function declarations, you can prompt the model to use them. It analyzes the prompt and function declarations and decides whether to respond directly or to call a function. If a function is called, the response object will contain a function call suggestion.

The model then returns a functionCall object in an OpenAPI compatible schema specifying how to call one or more of the declared functions in order to respond to the user's question.

Extract the function call details from the model's response, parse the arguments , and execute the set_light_values function.

Finally, send the result of the function execution back to the model so it can incorporate this information into its final response to the user.

This completes the function calling flow. The model successfully used the set_light_values function to perform the request action of the user.

When you implement function calling in a prompt, you create a tools object, which contains one or more function declarations. You define functions using JSON, specifically with a select subset of the OpenAPI schema format. A single function declaration can include the following parameters:

You can also construct FunctionDeclarations from Python functions directly using types.FunctionDeclaration.from_callable(client=client, callable=your_function).

Gemini 3 and 2.5 series models use an internal "thinking" process to reason through requests. This significantly improves function calling performance, allowing the model to better determine when to call a function and which parameters to use. Because the Gemini API is stateless, models use thought signatures to maintain context across multi-turn conversations.

This section covers advanced management of thought signatures and is only necessary if you're manually constructing API requests (e.g., via REST) or manipulating conversation history.

If you're using the Google GenAI SDKs (our official libraries), you don't need to manage this process. The SDKs automatically handle the necessary steps, as shown in the earlier example.

If you modify the conversation history manually, instead of sending the complete previous response you must correctly handle the thought_signature included in the model's turn.

Follow these rules to ensure the model's context is preserved:

In Gemini 3, any Part of a model response may contain a thought signature. While we generally recommend returning signatures from all Part types, passing back thought signatures is mandatory for function calling. Unless you are manipulating conversation history manually, the Google GenAI SDK will handle thought signatures automatically.

If you are manipulating conversation history manually, refer to the Thoughts Signatures page for complete guidance and details on handling thought signatures for Gemini 3.

While not necessary for implementation, you can inspect the response to see the thought_signature for debugging or educational purposes.

Learn more about limitations and usage of thought signatures, and about thinking models in general, on the Thinking page.

In addition to single turn function calling, you can also call multiple functions at once. Parallel function calling lets you execute multiple functions at once and is used when the functions are not dependent on each other. This is useful in scenarios like gathering data from multiple independent sources, such as retrieving customer details from different databases or checking inventory levels across various warehouses or performing multiple actions such as converting your apartment into a disco.

Configure the function calling mode to allow using all of the specified tools. To learn more, you can read about configuring function calling.

Each of the printed results reflects a single function call that the model has requested. To send the results back, include the responses in the same order as they were requested.

The Python SDK supports automatic function calling, which automatically converts Python functions to declarations, handles the function call execution and response cycle for you. Following is an example for the disco use case.

Compositional or sequential function calling allows Gemini to chain multiple function calls together to fulfill a complex request. For example, to answer "Get the temperature in my current location", the Gemini API might first invoke a get_current_location() function followed by a get_weather() function that takes the location as a parameter.

The following example demonstrates how to implement compositional function calling using the Python SDK and automatic function calling.

This example uses the automatic function calling feature of the google-genai Python SDK. The SDK automatically converts the Python functions to the required schema, executes the function calls when requested by the model, and sends the results back to the model to complete the task.

When you run the code, you will see the SDK orchestrating the function calls. The model first calls get_weather_forecast, receives the temperature, and then calls set_thermostat_temperature with the correct value based on the logic in the prompt.

This example shows how to use JavaScript/TypeScript SDK to do comopositional function calling using a manual execution loop.

When you run the code, you will see the SDK orchestrating the function calls. The model first calls get_weather_forecast, receives the temperature, and then calls set_thermostat_temperature with the correct value based on the logic in the prompt.

Compositional function calling is a native Live API feature. This means Live API can handle the function calling similar to the Python SDK.

The Gemini API lets you control how the model uses the provided tools (function declarations). Specifically, you can set the mode within the.function_calling_config.

VALIDATED (Preview): The model is constrained to predict either function calls or natural language, and ensures function schema adherence. If allowed_function_names is not provided, the model picks from all of the available function declarations. If allowed_function_names is provided, the model picks from the set of allowed functions.

When using the Python SDK, you can provide Python functions directly as tools. The SDK converts these functions into declarations, manages the function call execution, and handles the response cycle for you. Define your function with type hints and a docstring. For optimal results, it is recommended to use Google-style docstrings. The SDK will then automatically:

The SDK currently does not parse argument descriptions into the property description slots of the generated function declaration. Instead, it sends the entire docstring as the top-level function description.

You can disable automatic function calling with:

The API is able to describe any of the following types. Pydantic types are allowed, as long as the fields defined on them are also composed of allowed types. Dict types (like dict[str: int]) are not well supported here, don't use them.

To see what the inferred schema looks like, you can convert it using from_callable:

You can enable multiple tools combining native tools with function calling at the same time. Here's an example that enables two tools, Grounding with Google Search and code execution, in a request using the Live API.

Python developers can try this out in the Live API Tool Use notebook.

For Gemini 3 series models, you can include multimodal content in the function response parts that you send to the model. The model can process this multimodal content in its next turn to produce a more informed response. The following MIME types are supported for multimodal content in function responses:

To include multimodal data in a function response, include it as one or more parts nested within the functionResponse part. Each multimodal part must contain inlineData. If you reference a multimodal part from within the structured response field, it must contain a unique displayName.

You can also reference a multimodal part from within the structured response field of the functionResponse part by using the JSON reference format {"$ref": "<displayName>"}. The model substitutes the reference with the multimodal content when processing the response. Each displayName can only be referenced once in the structured response field.

The following example shows a message containing a functionResponse for a function named get_image and a nested part containing image data with displayName: "wakeupcat.jpg". The functionResponse's response field references this image part:

Model Context Protocol (MCP) is an open standard for connecting AI applications with external tools and data. MCP provides a common protocol for models to access context, such as functions (tools), data sources (resources), or predefined prompts.

The Gemini SDKs have built-in support for the MCP, reducing boilerplate code and offering automatic tool calling for MCP tools. When the model generates an MCP tool call, the Python and JavaScript client SDK can automatically execute the MCP tool and send the response back to the model in a subsequent request, continuing this loop until no more tool calls are made by the model.

Here, you can find an example of how to use a local MCP server with Gemini and mcp SDK.

Make sure the latest version of the mcp SDK is installed on your platform of choice.

Make sure the latest version of the mcp SDK is installed on your platform of choice.

Built-in MCP support is a experimental feature in our SDKs and has the following limitations:

Manual integration of MCP servers is always an option if these limit what you're building.

This section lists models and their function calling capabilities. Experimental models are not included. You can find a comprehensive capabilities overview on the model overview page.

Temperature: Use a low temperature (e.g., 0) for more deterministic and reliable function calls.

Validation: If a function call has significant consequences (e.g., placing an order), validate the call with the user before executing it.

Check Finish Reason: Always check the finishReason in the model's response to handle cases where the model failed to generate a valid function call.

Error Handling: Implement robust error handling in your functions to gracefully handle unexpected inputs or API failures. Return informative error messages that the model can use to generate helpful responses to the user.

Security: Be mindful of security when calling external APIs. Use appropriate authentication and authorization mechanisms. Avoid exposing sensitive data in function calls.

Token Limits: Function descriptions and parameters count towards your input token limit. If you're hitting token limits, consider limiting the number of functions or the length of the descriptions, break down complex tasks into smaller, more focused function sets.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

# Define the function declaration for the model
schedule_meeting_function = {
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees at a given time and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of people attending the meeting.",
            },
            "date": {
                "type": "string",
                "description": "Date of the meeting (e.g., '2024-07-29')",
            },
            "time": {
                "type": "string",
                "description": "Time of the meeting (e.g., '15:00')",
            },
            "topic": {
                "type": "string",
                "description": "The subject or topic of the meeting.",
            },
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}

# Configure the client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[schedule_meeting_function])
config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about the Q3 planning.",
    config=config,
)

# Check for a function call
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    #  In a real app, you would call your function here:
    #  result = schedule_meeting(**function_call.args)
else:
    print("No function call found in the response.")
    print(response.text)
```

Example 2 (python):
```python
from google import genai
from google.genai import types

# Define the function declaration for the model
schedule_meeting_function = {
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees at a given time and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of people attending the meeting.",
            },
            "date": {
                "type": "string",
                "description": "Date of the meeting (e.g., '2024-07-29')",
            },
            "time": {
                "type": "string",
                "description": "Time of the meeting (e.g., '15:00')",
            },
            "topic": {
                "type": "string",
                "description": "The subject or topic of the meeting.",
            },
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}

# Configure the client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[schedule_meeting_function])
config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about the Q3 planning.",
    config=config,
)

# Check for a function call
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    #  In a real app, you would call your function here:
    #  result = schedule_meeting(**function_call.args)
else:
    print("No function call found in the response.")
    print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI, Type } from '@google/genai';

// Configure the client
const ai = new GoogleGenAI({});

// Define the function declaration for the model
const scheduleMeetingFunctionDeclaration = {
  name: 'schedule_meeting',
  description: 'Schedules a meeting with specified attendees at a given time and date.',
  parameters: {
    type: Type.OBJECT,
    properties: {
      attendees: {
        type: Type.ARRAY,
        items: { type: Type.STRING },
        description: 'List of people attending the meeting.',
      },
      date: {
        type: Type.STRING,
        description: 'Date of the meeting (e.g., "2024-07-29")',
      },
      time: {
        type: Type.STRING,
        description: 'Time of the meeting (e.g., "15:00")',
      },
      topic: {
        type: Type.STRING,
        description: 'The subject or topic of the meeting.',
      },
    },
    required: ['attendees', 'date', 'time', 'topic'],
  },
};

// Send request with function declarations
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Schedule a meeting with Bob and Alice for 03/27/2025 at 10:00 AM about the Q3 planning.',
  config: {
    tools: [{
      functionDeclarations: [scheduleMeetingFunctionDeclaration]
    }],
  },
});

// Check for function calls in the response
if (response.functionCalls && response.functionCalls.length > 0) {
  const functionCall = response.functionCalls[0]; // Assuming one function call
  console.log(`Function to call: ${functionCall.name}`);
  console.log(`Arguments: ${JSON.stringify(functionCall.args)}`);
  // In a real app, you would call your actual function here:
  // const result = await scheduleMeeting(functionCall.args);
} else {
  console.log("No function call found in the response.");
  console.log(response.text);
}
```

Example 4 (python):
```python
import { GoogleGenAI, Type } from '@google/genai';

// Configure the client
const ai = new GoogleGenAI({});

// Define the function declaration for the model
const scheduleMeetingFunctionDeclaration = {
  name: 'schedule_meeting',
  description: 'Schedules a meeting with specified attendees at a given time and date.',
  parameters: {
    type: Type.OBJECT,
    properties: {
      attendees: {
        type: Type.ARRAY,
        items: { type: Type.STRING },
        description: 'List of people attending the meeting.',
      },
      date: {
        type: Type.STRING,
        description: 'Date of the meeting (e.g., "2024-07-29")',
      },
      time: {
        type: Type.STRING,
        description: 'Time of the meeting (e.g., "15:00")',
      },
      topic: {
        type: Type.STRING,
        description: 'The subject or topic of the meeting.',
      },
    },
    required: ['attendees', 'date', 'time', 'topic'],
  },
};

// Send request with function declarations
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Schedule a meeting with Bob and Alice for 03/27/2025 at 10:00 AM about the Q3 planning.',
  config: {
    tools: [{
      functionDeclarations: [scheduleMeetingFunctionDeclaration]
    }],
  },
});

// Check for function calls in the response
if (response.functionCalls && response.functionCalls.length > 0) {
  const functionCall = response.functionCalls[0]; // Assuming one function call
  console.log(`Function to call: ${functionCall.name}`);
  console.log(`Arguments: ${JSON.stringify(functionCall.args)}`);
  // In a real app, you would call your actual function here:
  // const result = await scheduleMeeting(functionCall.args);
} else {
  console.log("No function call found in the response.");
  console.log(response.text);
}
```

---

## Ephemeral tokens

**URL:** https://ai.google.dev/gemini-api/docs/ephemeral-tokens

**Contents:**
- Ephemeral tokens
- How ephemeral tokens work
- Create an ephemeral token
  - Python
  - JavaScript
  - Python
  - JavaScript
- Connect to Live API with an ephemeral token
  - JavaScript
- Best practices

Ephemeral tokens are short-lived authentication tokens for accessing the Gemini API through WebSockets. They are designed to enhance security when you are connecting directly from a user's device to the API (a client-to-server implementation). Like standard API keys, ephemeral tokens can be extracted from client-side applications such as web browsers or mobile apps. But because ephemeral tokens expire quickly and can be restricted, they significantly reduce the security risks in a production environment. You should use them when accessing the Live API directly from client-side applications to enhance API key security.

Here's how ephemeral tokens work at a high level:

This enhances security because even if extracted, the token is short-lived, unlike a long-lived API key deployed client-side. Since the client sends data directly to Gemini, this also improves latency and avoids your backends needing to proxy the real time data.

Here is a simplified example of how to get an ephemeral token from Gemini. By default, you'll have 1 minute to start new Live API sessions using the token from this request (newSessionExpireTime), and 30 minutes to send messages over that connection (expireTime).

For expireTime value constraints, defaults, and other field specs, see the API reference. Within the expireTime timeframe, you'll need sessionResumption to reconnect the call every 10 minutes (this can be done with the same token even if uses: 1).

It's also possible to lock an ephemeral token to a set of configurations. This might be useful to further improve security of your application and keep your system instructions on the server side.

You can also lock a subset of fields, see the SDK documentation for more info.

Once you have an ephemeral token, you use it as if it were an API key (but remember, it only works for the live API, and only with the v1alpha version of the API).

The use of ephemeral tokens only adds value when deploying applications that follow client-to-server implementation approach.

See Get started with Live API for more examples.

Ephemeral tokens are only compatible with Live API at this time.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-12 UTC.

**Examples:**

Example 1 (unknown):
```unknown
import datetime

now = datetime.datetime.now(tz=datetime.timezone.utc)

client = genai.Client(
    http_options={'api_version': 'v1alpha',}
)

token = client.auth_tokens.create(
    config = {
    'uses': 1, # The ephemeral token can only be used to start a single session
    'expire_time': now + datetime.timedelta(minutes=30), # Default is 30 minutes in the future
    # 'expire_time': '2025-05-17T00:00:00Z',   # Accepts isoformat.
    'new_session_expire_time': now + datetime.timedelta(minutes=1), # Default 1 minute in the future
    'http_options': {'api_version': 'v1alpha'},
  }
)

# You'll need to pass the value under token.name back to your client to use it
```

Example 2 (unknown):
```unknown
import datetime

now = datetime.datetime.now(tz=datetime.timezone.utc)

client = genai.Client(
    http_options={'api_version': 'v1alpha',}
)

token = client.auth_tokens.create(
    config = {
    'uses': 1, # The ephemeral token can only be used to start a single session
    'expire_time': now + datetime.timedelta(minutes=30), # Default is 30 minutes in the future
    # 'expire_time': '2025-05-17T00:00:00Z',   # Accepts isoformat.
    'new_session_expire_time': now + datetime.timedelta(minutes=1), # Default 1 minute in the future
    'http_options': {'api_version': 'v1alpha'},
  }
)

# You'll need to pass the value under token.name back to your client to use it
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const client = new GoogleGenAI({});
const expireTime = new Date(Date.now() + 30 * 60 * 1000).toISOString();

  const token: AuthToken = await client.authTokens.create({
    config: {
      uses: 1, // The default
      expireTime: expireTime // Default is 30 mins
      newSessionExpireTime: new Date(Date.now() + (1 * 60 * 1000)), // Default 1 minute in the future
      httpOptions: {apiVersion: 'v1alpha'},
    },
  });
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const client = new GoogleGenAI({});
const expireTime = new Date(Date.now() + 30 * 60 * 1000).toISOString();

  const token: AuthToken = await client.authTokens.create({
    config: {
      uses: 1, // The default
      expireTime: expireTime // Default is 30 mins
      newSessionExpireTime: new Date(Date.now() + (1 * 60 * 1000)), // Default 1 minute in the future
      httpOptions: {apiVersion: 'v1alpha'},
    },
  });
```

---

## Access Google AI Studio with your Workspace account

**URL:** https://ai.google.dev/gemini-api/docs/workspace

**Contents:**
- Access Google AI Studio with your Workspace account
- Troubleshooting
- Enable AI Studio for Workspace users

All Google Workspace users have access to AI Studio by default. If you're a Workspace user and you want to get started with AI Studio, check out the AI Studio quickstart.

If access to AI Studio is disabled for your Google Workspace account, you might see an error like the following:

We are sorry, but you do not have access to Google AI Studio. Please contact your Organization Administrator for access.

If you think you should have access to AI Studio, contact your Workspace administrator.

As a Google Workspace administrator, you can control who uses AI Studio:

To enable or disable AI Studio for users in your organization, see Turn Google AI Studio on or off for users.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

---

## Structured Outputs

**URL:** https://ai.google.dev/gemini-api/docs/structured-output

**Contents:**
- Structured Outputs
  - Python
  - JavaScript
  - Go
  - REST
- Streaming
  - Python
  - JavaScript
- Structured outputs with tools
  - Python

You can configure Gemini models to generate responses that adhere to a provided JSON Schema. This capability guarantees predictable and parsable results, ensures format and type-safety, enables the programmatic detection of refusals, and simplifies prompting.

Using structured outputs is ideal for a wide range of applications:

In addition to supporting JSON Schema in the REST API, the Google GenAI SDKs for Python and JavaScript also make it easy to define object schemas using Pydantic and Zod, respectively. The example below demonstrates how to extract information from unstructured text that conforms to a schema defined in code.

Recipe Extractor Content Moderation Recursive Structures

This example demonstrates how to extract structured data from text using basic JSON Schema types like object, array, string, and integer.

You can stream structured outputs, which allows you to start processing the response as it's being generated, without having to wait for the entire output to be complete. This can improve the perceived performance of your application.

The streamed chunks will be valid partial JSON strings, which can be concatenated to form the final, complete JSON object.

Gemini 3 lets you combine Structured Outputs with built-in tools, including Grounding with Google Search, URL Context, and Code Execution.

To generate a JSON object, set the response_mime_type in the generation configuration to application/json and provide a response_json_schema. The schema must be a valid JSON Schema that describes the desired output format.

The model will then generate a response that is a syntactically valid JSON string matching the provided schema. When using structured outputs, the model will produce outputs in the same order as the keys in the schema.

Gemini's structured output mode supports a subset of the JSON Schema specification.

The following values of type are supported:

These descriptive properties help guide the model:

For number and integer values:

The following models support structured output:

* Note that Gemini 2.0 requires an explicit propertyOrdering list within the JSON input to define the preferred structure. You can find an example in this cookbook.

Both structured outputs and function calling use JSON schemas, but they serve different purposes:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional

class Ingredient(BaseModel):
    name: str = Field(description="Name of the ingredient.")
    quantity: str = Field(description="Quantity of the ingredient, including units.")

class Recipe(BaseModel):
    recipe_name: str = Field(description="The name of the recipe.")
    prep_time_minutes: Optional[int] = Field(description="Optional time in minutes to prepare the recipe.")
    ingredients: List[Ingredient]
    instructions: List[str]

client = genai.Client()

prompt = """
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Recipe.model_json_schema(),
    },
)

recipe = Recipe.model_validate_json(response.text)
print(recipe)
```

Example 2 (python):
```python
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional

class Ingredient(BaseModel):
    name: str = Field(description="Name of the ingredient.")
    quantity: str = Field(description="Quantity of the ingredient, including units.")

class Recipe(BaseModel):
    recipe_name: str = Field(description="The name of the recipe.")
    prep_time_minutes: Optional[int] = Field(description="Optional time in minutes to prepare the recipe.")
    ingredients: List[Ingredient]
    instructions: List[str]

client = genai.Client()

prompt = """
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Recipe.model_json_schema(),
    },
)

recipe = Recipe.model_validate_json(response.text)
print(recipe)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const ingredientSchema = z.object({
  name: z.string().describe("Name of the ingredient."),
  quantity: z.string().describe("Quantity of the ingredient, including units."),
});

const recipeSchema = z.object({
  recipe_name: z.string().describe("The name of the recipe."),
  prep_time_minutes: z.number().optional().describe("Optional time in minutes to prepare the recipe."),
  ingredients: z.array(ingredientSchema),
  instructions: z.array(z.string()),
});

const ai = new GoogleGenAI({});

const prompt = `
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
`;

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: prompt,
  config: {
    responseMimeType: "application/json",
    responseJsonSchema: zodToJsonSchema(recipeSchema),
  },
});

const recipe = recipeSchema.parse(JSON.parse(response.text));
console.log(recipe);
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const ingredientSchema = z.object({
  name: z.string().describe("Name of the ingredient."),
  quantity: z.string().describe("Quantity of the ingredient, including units."),
});

const recipeSchema = z.object({
  recipe_name: z.string().describe("The name of the recipe."),
  prep_time_minutes: z.number().optional().describe("Optional time in minutes to prepare the recipe."),
  ingredients: z.array(ingredientSchema),
  instructions: z.array(z.string()),
});

const ai = new GoogleGenAI({});

const prompt = `
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
`;

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: prompt,
  config: {
    responseMimeType: "application/json",
    responseJsonSchema: zodToJsonSchema(recipeSchema),
  },
});

const recipe = recipeSchema.parse(JSON.parse(response.text));
console.log(recipe);
```

---

## Video understanding

**URL:** https://ai.google.dev/gemini-api/docs/video-understanding

**Contents:**
- Video understanding
- Video input
  - Upload a video file
  - Python
  - JavaScript
  - Go
  - REST
  - Pass video data inline
  - Python
  - JavaScript

Gemini models can process videos, enabling many frontier developer use cases that would have historically required domain specific models. Some of Gemini's vision capabilities include the ability to:

Gemini was built to be multimodal from the ground up and we continue to push the frontier of what is possible. This guide shows how to use the Gemini API to generate text responses based on video inputs.

You can provide videos as input to Gemini in the following ways:

You can use the Files API to upload a video file. Always use the Files API when the total request size (including the file, text prompt, system instructions, etc.) is larger than 20 MB, the video duration is significant, or if you intend to use the same video in multiple prompts. The File API accepts video file formats directly.

The following code downloads the sample video, uploads it using the File API, waits for it to be processed, and then uses the file reference in a generateContent request.

To learn more about working with media files, see Files API.

Instead of uploading a video file using the File API, you can pass smaller videos directly in the request to generateContent. This is suitable for shorter videos under 20MB total request size.

Here's an example of providing inline video data:

You can pass YouTube URLs directly to Gemini API as part of your generateContentrequest as follows:

You can ask questions about specific points in time within the video using timestamps of the form MM:SS.

Gemini models offer powerful capabilities for understanding video content by processing information from both the audio and visual streams. This lets you extract a rich set of details, including generating descriptions of what is happening in a video and answering questions about its content. For visual descriptions, the model samples the video at a rate of 1 frame per second. This sampling rate may affect the level of detail in the descriptions, particularly for videos with rapidly changing visuals.

You can customize video processing in the Gemini API by setting clipping intervals or providing custom frame rate sampling.

You can clip video by specifying videoMetadata with start and end offsets.

You can set custom frame rate sampling by passing an fps argument to videoMetadata.

By default 1 frame per second (FPS) is sampled from the video. You might want to set low FPS (< 1) for long videos. This is especially useful for mostly static videos (e.g. lectures). Use a higher FPS for videos requiring granular temporal analysis, such as fast-action understanding or high-speed motion tracking.

Gemini supports the following video format MIME types:

Medial resolution: Gemini 3 introduces granular control over multimodal vision processing with the media_resolution parameter. The media_resolution parameter determines the maximum number of tokens allocated per input image or video frame. Higher resolutions improve the model's ability to read fine text or identify small details, but increase token usage and latency.

For more details about the parameter and how it can impact token calculations, see the media resolution guide.

Timestamp format: When referring to specific moments in a video within your prompt, use the MM:SS format (e.g., 01:15 for 1 minute and 15 seconds).

This guide shows how to upload video files and generate text outputs from video inputs. To learn more, see the following resources:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp4")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=[myfile, "Summarize this video. Then create a quiz with an answer key based on the information in this video."]
)

print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

myfile = client.files.upload(file="path/to/sample.mp4")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=[myfile, "Summarize this video. Then create a quiz with an answer key based on the information in this video."]
)

print(response.text)
```

Example 3 (python):
```python
import {
  GoogleGenAI,
  createUserContent,
  createPartFromUri,
} from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const myfile = await ai.files.upload({
    file: "path/to/sample.mp4",
    config: { mimeType: "video/mp4" },
  });

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: createUserContent([
      createPartFromUri(myfile.uri, myfile.mimeType),
      "Summarize this video. Then create a quiz with an answer key based on the information in this video.",
    ]),
  });
  console.log(response.text);
}

await main();
```

Example 4 (python):
```python
import {
  GoogleGenAI,
  createUserContent,
  createPartFromUri,
} from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const myfile = await ai.files.upload({
    file: "path/to/sample.mp4",
    config: { mimeType: "video/mp4" },
  });

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: createUserContent([
      createPartFromUri(myfile.uri, myfile.mimeType),
      "Summarize this video. Then create a quiz with an answer key based on the information in this video.",
    ]),
  });
  console.log(response.text);
}

await main();
```

---

## Understand and count tokens

**URL:** https://ai.google.dev/gemini-api/docs/tokens

**Contents:**
- Understand and count tokens
- About tokens
- Try out counting tokens in a Colab
- Context windows
- Count tokens
  - Count text tokens
  - Count multi-turn (chat) tokens
  - Count multimodal tokens
    - Media resolutions
    - Image files

Gemini and other generative AI models process input and output at a granularity called a token.

For Gemini models, a token is equivalent to about 4 characters. 100 tokens is equal to about 60-80 English words.

Tokens can be single characters like z or whole words like cat. Long words are broken up into several tokens. The set of all tokens used by the model is called the vocabulary, and the process of splitting text into tokens is called tokenization.

When billing is enabled, the cost of a call to the Gemini API is determined in part by the number of input and output tokens, so knowing how to count tokens can be helpful.

You can try out counting tokens by using a Colab.

The models available through the Gemini API have context windows that are measured in tokens. The context window defines how much input you can provide and how much output the model can generate. You can determine the size of the context window by calling the getModels endpoint or by looking in the models documentation.

In the following example, you can see that the gemini-2.0-flash model has an input limit of about 1,000,000 tokens and an output limit of about 8,000 tokens, which means a context window is 1,000,000 tokens.

All input to and output from the Gemini API is tokenized, including text, image files, and other non-text modalities.

You can count tokens in the following ways:

All input to the Gemini API is tokenized, including text, image files, and other non-text modalities. Note the following high-level key points about tokenization of multimodal input during processing by the Gemini API:

With Gemini 2.0, image inputs with both dimensions <=384 pixels are counted as 258 tokens. Images larger in one or both dimensions are cropped and scaled as needed into tiles of 768x768 pixels, each counted as 258 tokens. Prior to Gemini 2.0, images used a fixed 258 tokens.

Video and audio files are converted to tokens at the following fixed rates: video at 263 tokens per second and audio at 32 tokens per second.

Gemini 3 Pro Preview introduces granular control over multimodal vision processing with the media_resolution parameter. The media_resolution parameter determines the maximum number of tokens allocated per input image or video frame. Higher resolutions improve the model's ability to read fine text or identify small details, but increase token usage and latency.

For more details about the parameter and how it can impact token calculations, see the media resolution guide.

Example that uses an uploaded image from the File API:

Example that provides the image as inline data:

Audio and video are each converted to tokens at the following fixed rates:

System instructions and tools also count towards the total token count for the input.

If you use system instructions, the total_tokens count increases to reflect the addition of system_instruction.

If you use function calling, the total_tokens count increases to reflect the addition of tools.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-12 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()
model_info = client.models.get(model="gemini-2.0-flash")
print(f"{model_info.input_token_limit=}")
print(f"{model_info.output_token_limit=}")
# ( e.g., input_token_limit=30720, output_token_limit=2048 )count_tokens.py
```

Example 2 (python):
```python
from google import genai

client = genai.Client()
model_info = client.models.get(model="gemini-2.0-flash")
print(f"{model_info.input_token_limit=}")
print(f"{model_info.output_token_limit=}")
# ( e.g., input_token_limit=30720, output_token_limit=2048 )count_tokens.py
```

Example 3 (python):
```python
from google import genai

client = genai.Client()
prompt = "The quick brown fox jumps over the lazy dog."

# Count tokens using the new client method.
total_tokens = client.models.count_tokens(
    model="gemini-2.0-flash", contents=prompt
)
print("total_tokens: ", total_tokens)
# ( e.g., total_tokens: 10 )

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
)

# The usage_metadata provides detailed token counts.
print(response.usage_metadata)
# ( e.g., prompt_token_count: 11, candidates_token_count: 73, total_token_count: 84 )count_tokens.py
```

Example 4 (python):
```python
from google import genai

client = genai.Client()
prompt = "The quick brown fox jumps over the lazy dog."

# Count tokens using the new client method.
total_tokens = client.models.count_tokens(
    model="gemini-2.0-flash", contents=prompt
)
print("total_tokens: ", total_tokens)
# ( e.g., total_tokens: 10 )

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
)

# The usage_metadata provides detailed token counts.
print(response.usage_metadata)
# ( e.g., prompt_token_count: 11, candidates_token_count: 73, total_token_count: 84 )count_tokens.py
```

---

## Long context

**URL:** https://ai.google.dev/gemini-api/docs/long-context

**Contents:**
- Long context
- What is a context window?
- Getting started with long context
- Long context use cases
  - Long form text
  - Long form video
  - Long form audio
- Long context optimizations
- Long context limitations
- FAQs

Many Gemini models come with large context windows of 1 million or more tokens. Historically, large language models (LLMs) were significantly limited by the amount of text (or tokens) that could be passed to the model at one time. The Gemini long context window unlocks many new use cases and developer paradigms.

The code you already use for cases like text generation or multimodal inputs will work without any changes with long context.

This document gives you an overview of what you can achieve using models with context windows of 1M and more tokens. The page gives a brief overview of a context window, and explores how developers should think about long context, various real world use cases for long context, and ways to optimize the usage of long context.

For the context window sizes of specific models, see the Models page.

The basic way you use the Gemini models is by passing information (context) to the model, which will subsequently generate a response. An analogy for the context window is short term memory. There is a limited amount of information that can be stored in someone's short term memory, and the same is true for generative models.

You can read more about how models work under the hood in our generative models guide.

Earlier versions of generative models were only able to process 8,000 tokens at a time. Newer models pushed this further by accepting 32,000 or even 128,000 tokens. Gemini is the first model capable of accepting 1 million tokens.

In practice, 1 million tokens would look like:

The more limited context windows common in many other models often require strategies like arbitrarily dropping old messages, summarizing content, using RAG with vector databases, or filtering prompts to save tokens.

While these techniques remain valuable in specific scenarios, Gemini's extensive context window invites a more direct approach: providing all relevant information upfront. Because Gemini models were purpose-built with massive context capabilities, they demonstrate powerful in-context learning. For example, using only in-context instructional materials (a 500-page reference grammar, a dictionary, and ≈400 parallel sentences), Gemini learned to translate from English to Kalamang—a Papuan language with fewer than 200 speakers—with quality similar to a human learner using the same materials. This illustrates the paradigm shift enabled by Gemini's long context, empowering new possibilities through robust in-context learning.

While the standard use case for most generative models is still text input, the Gemini model family enables a new paradigm of multimodal use cases. These models can natively understand text, video, audio, and images. They are accompanied by the Gemini API that takes in multimodal file types for convenience.

Text has proved to be the layer of intelligence underpinning much of the momentum around LLMs. As mentioned earlier, much of the practical limitation of LLMs was because of not having a large enough context window to do certain tasks. This led to the rapid adoption of retrieval augmented generation (RAG) and other techniques which dynamically provide the model with relevant contextual information. Now, with larger and larger context windows, there are new techniques becoming available which unlock new use cases.

Some emerging and standard use cases for text based long context include:

Many-shot in-context learning is one of the most unique capabilities unlocked by long context models. Research has shown that taking the common "single shot" or "multi-shot" example paradigm, where the model is presented with one or a few examples of a task, and scaling that up to hundreds, thousands, or even hundreds of thousands of examples, can lead to novel model capabilities. This many-shot approach has also been shown to perform similarly to models which were fine-tuned for a specific task. For use cases where a Gemini model's performance is not yet sufficient for a production rollout, you can try the many-shot approach. As you might explore later in the long context optimization section, context caching makes this type of high input token workload much more economically feasible and even lower latency in some cases.

Video content's utility has long been constrained by the lack of accessibility of the medium itself. It was hard to skim the content, transcripts often failed to capture the nuance of a video, and most tools don't process image, text, and audio together. With Gemini, the long-context text capabilities translate to the ability to reason and answer questions about multimodal inputs with sustained performance.

Some emerging and standard use cases for video long context include:

When working with videos, it is important to consider how the videos are processed into tokens, which affects billing and usage limits. You can learn more about prompting with video files in the Prompting guide.

The Gemini models were the first natively multimodal large language models that could understand audio. Historically, the typical developer workflow would involve stringing together multiple domain specific models, like a speech-to-text model and a text-to-text model, in order to process audio. This led to additional latency required by performing multiple round-trip requests and decreased performance usually attributed to disconnected architectures of the multiple model setup.

Some emerging and standard use cases for audio context include:

You can learn more about prompting with audio files in the Prompting guide.

The primary optimization when working with long context and the Gemini models is to use context caching. Beyond the previous impossibility of processing lots of tokens in a single request, the other main constraint was the cost. If you have a "chat with your data" app where a user uploads 10 PDFs, a video, and some work documents, you would historically have to work with a more complex retrieval augmented generation (RAG) tool / framework in order to process these requests and pay a significant amount for tokens moved into the context window. Now, you can cache the files the user uploads and pay to store them on a per hour basis. The input / output cost per request with Gemini Flash for example is ~4x less than the standard input / output cost, so if the user chats with their data enough, it becomes a huge cost saving for you as the developer.

In various sections of this guide, we talked about how Gemini models achieve high performance across various needle-in-a-haystack retrieval evals. These tests consider the most basic setup, where you have a single needle you are looking for. In cases where you might have multiple "needles" or specific pieces of information you are looking for, the model does not perform with the same accuracy. Performance can vary to a wide degree depending on the context. This is important to consider as there is an inherent tradeoff between getting the right information retrieved and cost. You can get ~99% on a single query, but you have to pay the input token cost every time you send that query. So for 100 pieces of information to be retrieved, if you needed 99% performance, you would likely need to send 100 requests. This is a good example of where context caching can significantly reduce the cost associated with using Gemini models while keeping the performance high.

In most cases, especially if the total context is long, the model's performance will be better if you put your query / question at the end of the prompt (after all the other context).

Generally, if you don't need tokens to be passed to the model, it is best to avoid passing them. However, if you have a large chunk of tokens with some information and want to ask questions about that information, the model is highly capable of extracting that information (up to 99% accuracy in many cases).

If you have a similar set of tokens / context that you want to re-use many times, context caching can help reduce the costs associated with asking questions about that information.

There is some fixed amount of latency in any given request, regardless of the size, but generally longer queries will have higher latency (time to first token).

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

---

## Using Tools & Agents with Gemini API

**URL:** https://ai.google.dev/gemini-api/docs/tools

**Contents:**
- Using Tools & Agents with Gemini API
- Available built-in tools
- Available Agents
- How tools execution works
  - Built-in tool flow
  - Custom tool flow (Function Calling)
- Structured outputs vs. function Calling
- Structured outputs with tools
- Building agents
  - Agent frameworks

Tools and Agents extend the capabilities of Gemini models, enabling them to take action in the world, access real-time information, and perform complex computational tasks. Models can use tools in both standard request-response interactions and real-time streaming sessions using the Live API.

The Gemini API provides a suite of fully managed, built-in tools and agents optimized for Gemini models, or you can define custom tools using Function Calling.

See the Pricing page for details on costs associated with specific tools.

Tools allow the model to request actions during a conversation. The flow differs depending on whether the tool is built-in (managed by Google) or custom (managed by you).

For built-in tools like Google Search or Code Execution, the entire process happens within one API call:

For custom tools and Computer Use, your application handles the execution:

Learn more in the Function calling guide.

Gemini offers two methods for generating structured outputs. Use Function calling when the model needs to perform an intermediate step by connecting to your own tools or data systems. Use Structured Outputs when you strictly need the model's final response to adhere to a specific schema, such as for rendering a custom UI.

You can combine Structured Outputs with built-in tools to ensure that model responses grounded in external data or computation still adhere to a strict schema.

See Structured outputs with tools for code examples.

Agents are systems that use models and tools to complete multi-step tasks. While Gemini provides the reasoning capabilities (the "brain") and the essential tools (the "hands"), you often need an orchestration framework to manage the agent's memory, plan loops, and perform complex tool chaining.

To maximize reliability in multi-step workflows, you should craft instructions that explicitly control how the model reasons and plans. While Gemini provides strong general reasoning, complex agents benefit from prompts that enforce specific behaviors like persistence in the face of issues, risk assessment, and proactive planning.

See the Agentic workflows for strategies on designing these prompts. Here is a example, of a system instruction that improved performance on several agentic benchmarks by around 5%.

Gemini integrates with leading open-source agent frameworks such as:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-11 UTC.

---

## Tool use with Live API

**URL:** https://ai.google.dev/gemini-api/docs/live-tools

**Contents:**
- Tool use with Live API
- Overview of supported tools
- Function calling
  - Python
  - JavaScript
- Asynchronous function calling
  - Python
  - JavaScript
  - Python
  - JavaScript

Tool use allows Live API to go beyond just conversation by enabling it to perform actions in the real-world and pull in external context while maintaining a real time connection. You can define tools such as Function calling and Google Search with the Live API.

Here's a brief overview of the available tools for Live API models:

Live API supports function calling, just like regular content generation requests. Function calling lets the Live API interact with external data and programs, greatly increasing what your applications can accomplish.

You can define function declarations as part of the session configuration. After receiving tool calls, the client should respond with a list of FunctionResponse objects using the session.send_tool_response method.

See the Function calling tutorial to learn more.

From a single prompt, the model can generate multiple function calls and the code necessary to chain their outputs. This code executes in a sandbox environment, generating subsequent BidiGenerateContentToolCall messages.

Function calling executes sequentially by default, meaning execution pauses until the results of each function call are available. This ensures sequential processing, which means you won't be able to continue interacting with the model while the functions are being run.

If you don't want to block the conversation, you can tell the model to run the functions asynchronously. To do so, you first need to add a behavior to the function definitions:

NON-BLOCKING ensures the function runs asynchronously while you can continue interacting with the model.

Then you need to tell the model how to behave when it receives the FunctionResponse using the scheduling parameter. It can either:

Or do nothing and use that knowledge later on in the discussion (scheduling="SILENT")

You can enable Grounding with Google Search as part of the session configuration. This increases the Live API's accuracy and prevents hallucinations. See the Grounding tutorial to learn more.

You can combine multiple tools within the Live API, increasing your application's capabilities even more:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-12 UTC.

**Examples:**

Example 1 (python):
```python
import asyncio
import wave
from google import genai
from google.genai import types

client = genai.Client()

model = "gemini-2.5-flash-native-audio-preview-12-2025"

# Simple function definitions
turn_on_the_lights = {"name": "turn_on_the_lights"}
turn_off_the_lights = {"name": "turn_off_the_lights"}

tools = [{"function_declarations": [turn_on_the_lights, turn_off_the_lights]}]
config = {"response_modalities": ["AUDIO"], "tools": tools}

async def main():
    async with client.aio.live.connect(model=model, config=config) as session:
        prompt = "Turn on the lights please"
        await session.send_client_content(turns={"parts": [{"text": prompt}]})

        wf = wave.open("audio.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)  # Output is 24kHz

        async for response in session.receive():
            if response.data is not None:
                wf.writeframes(response.data)
            elif response.tool_call:
                print("The tool was called")
                function_responses = []
                for fc in response.tool_call.function_calls:
                    function_response = types.FunctionResponse(
                        id=fc.id,
                        name=fc.name,
                        response={ "result": "ok" } # simple, hard-coded function response
                    )
                    function_responses.append(function_response)

                await session.send_tool_response(function_responses=function_responses)

        wf.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Example 2 (python):
```python
import asyncio
import wave
from google import genai
from google.genai import types

client = genai.Client()

model = "gemini-2.5-flash-native-audio-preview-12-2025"

# Simple function definitions
turn_on_the_lights = {"name": "turn_on_the_lights"}
turn_off_the_lights = {"name": "turn_off_the_lights"}

tools = [{"function_declarations": [turn_on_the_lights, turn_off_the_lights]}]
config = {"response_modalities": ["AUDIO"], "tools": tools}

async def main():
    async with client.aio.live.connect(model=model, config=config) as session:
        prompt = "Turn on the lights please"
        await session.send_client_content(turns={"parts": [{"text": prompt}]})

        wf = wave.open("audio.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)  # Output is 24kHz

        async for response in session.receive():
            if response.data is not None:
                wf.writeframes(response.data)
            elif response.tool_call:
                print("The tool was called")
                function_responses = []
                for fc in response.tool_call.function_calls:
                    function_response = types.FunctionResponse(
                        id=fc.id,
                        name=fc.name,
                        response={ "result": "ok" } # simple, hard-coded function response
                    )
                    function_responses.append(function_response)

                await session.send_tool_response(function_responses=function_responses)

        wf.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Example 3 (python):
```python
import { GoogleGenAI, Modality } from '@google/genai';
import * as fs from "node:fs";
import pkg from 'wavefile';  // npm install wavefile
const { WaveFile } = pkg;

const ai = new GoogleGenAI({});
const model = 'gemini-2.5-flash-native-audio-preview-12-2025';

// Simple function definitions
const turn_on_the_lights = { name: "turn_on_the_lights" } // , description: '...', parameters: { ... }
const turn_off_the_lights = { name: "turn_off_the_lights" }

const tools = [{ functionDeclarations: [turn_on_the_lights, turn_off_the_lights] }]

const config = {
  responseModalities: [Modality.AUDIO],
  tools: tools
}

async function live() {
  const responseQueue = [];

  async function waitMessage() {
    let done = false;
    let message = undefined;
    while (!done) {
      message = responseQueue.shift();
      if (message) {
        done = true;
      } else {
        await new Promise((resolve) => setTimeout(resolve, 100));
      }
    }
    return message;
  }

  async function handleTurn() {
    const turns = [];
    let done = false;
    while (!done) {
      const message = await waitMessage();
      turns.push(message);
      if (message.serverContent && message.serverContent.turnComplete) {
        done = true;
      } else if (message.toolCall) {
        done = true;
      }
    }
    return turns;
  }

  const session = await ai.live.connect({
    model: model,
    callbacks: {
      onopen: function () {
        console.debug('Opened');
      },
      onmessage: function (message) {
        responseQueue.push(message);
      },
      onerror: function (e) {
        console.debug('Error:', e.message);
      },
      onclose: function (e) {
        console.debug('Close:', e.reason);
      },
    },
    config: config,
  });

  const inputTurns = 'Turn on the lights please';
  session.sendClientContent({ turns: inputTurns });

  let turns = await handleTurn();

  for (const turn of turns) {
    if (turn.toolCall) {
      console.debug('A tool was called');
      const functionResponses = [];
      for (const fc of turn.toolCall.functionCalls) {
        functionResponses.push({
          id: fc.id,
          name: fc.name,
          response: { result: "ok" } // simple, hard-coded function response
        });
      }

      console.debug('Sending tool response...\n');
      session.sendToolResponse({ functionResponses: functionResponses });
    }
  }

  // Check again for new messages
  turns = await handleTurn();

  // Combine audio data strings and save as wave file
  const combinedAudio = turns.reduce((acc, turn) => {
      if (turn.data) {
          const buffer = Buffer.from(turn.data, 'base64');
          const intArray = new Int16Array(buffer.buffer, buffer.byteOffset, buffer.byteLength / Int16Array.BYTES_PER_ELEMENT);
          return acc.concat(Array.from(intArray));
      }
      return acc;
  }, []);

  const audioBuffer = new Int16Array(combinedAudio);

  const wf = new WaveFile();
  wf.fromScratch(1, 24000, '16', audioBuffer);  // output is 24kHz
  fs.writeFileSync('audio.wav', wf.toBuffer());

  session.close();
}

async function main() {
  await live().catch((e) => console.error('got error', e));
}

main();
```

Example 4 (python):
```python
import { GoogleGenAI, Modality } from '@google/genai';
import * as fs from "node:fs";
import pkg from 'wavefile';  // npm install wavefile
const { WaveFile } = pkg;

const ai = new GoogleGenAI({});
const model = 'gemini-2.5-flash-native-audio-preview-12-2025';

// Simple function definitions
const turn_on_the_lights = { name: "turn_on_the_lights" } // , description: '...', parameters: { ... }
const turn_off_the_lights = { name: "turn_off_the_lights" }

const tools = [{ functionDeclarations: [turn_on_the_lights, turn_off_the_lights] }]

const config = {
  responseModalities: [Modality.AUDIO],
  tools: tools
}

async function live() {
  const responseQueue = [];

  async function waitMessage() {
    let done = false;
    let message = undefined;
    while (!done) {
      message = responseQueue.shift();
      if (message) {
        done = true;
      } else {
        await new Promise((resolve) => setTimeout(resolve, 100));
      }
    }
    return message;
  }

  async function handleTurn() {
    const turns = [];
    let done = false;
    while (!done) {
      const message = await waitMessage();
      turns.push(message);
      if (message.serverContent && message.serverContent.turnComplete) {
        done = true;
      } else if (message.toolCall) {
        done = true;
      }
    }
    return turns;
  }

  const session = await ai.live.connect({
    model: model,
    callbacks: {
      onopen: function () {
        console.debug('Opened');
      },
      onmessage: function (message) {
        responseQueue.push(message);
      },
      onerror: function (e) {
        console.debug('Error:', e.message);
      },
      onclose: function (e) {
        console.debug('Close:', e.reason);
      },
    },
    config: config,
  });

  const inputTurns = 'Turn on the lights please';
  session.sendClientContent({ turns: inputTurns });

  let turns = await handleTurn();

  for (const turn of turns) {
    if (turn.toolCall) {
      console.debug('A tool was called');
      const functionResponses = [];
      for (const fc of turn.toolCall.functionCalls) {
        functionResponses.push({
          id: fc.id,
          name: fc.name,
          response: { result: "ok" } // simple, hard-coded function response
        });
      }

      console.debug('Sending tool response...\n');
      session.sendToolResponse({ functionResponses: functionResponses });
    }
  }

  // Check again for new messages
  turns = await handleTurn();

  // Combine audio data strings and save as wave file
  const combinedAudio = turns.reduce((acc, turn) => {
      if (turn.data) {
          const buffer = Buffer.from(turn.data, 'base64');
          const intArray = new Int16Array(buffer.buffer, buffer.byteOffset, buffer.byteLength / Int16Array.BYTES_PER_ELEMENT);
          return acc.concat(Array.from(intArray));
      }
      return acc;
  }, []);

  const audioBuffer = new Int16Array(combinedAudio);

  const wf = new WaveFile();
  wf.fromScratch(1, 24000, '16', audioBuffer);  // output is 24kHz
  fs.writeFileSync('audio.wav', wf.toBuffer());

  session.close();
}

async function main() {
  await live().catch((e) => console.error('got error', e));
}

main();
```

---

## Gemini 3 Developer Guide

**URL:** https://ai.google.dev/gemini-api/docs/gemini-3

**Contents:**
- Gemini 3 Developer Guide
  - Python
  - JavaScript
  - REST
- Meet the Gemini 3 series
- New API features in Gemini 3
  - Thinking level
  - Python
  - JavaScript
  - REST

Gemini 3 is our most intelligent model family to date, built on a foundation of state-of-the-art reasoning. It is designed to bring any idea to life by mastering agentic workflows, autonomous coding, and complex multimodal tasks. This guide covers key features of the Gemini 3 model family and how to get the most out of it.

Explore our collection of Gemini 3 apps to see how the model handles advanced reasoning, autonomous coding, and complex multimodal tasks.

Get started with a few lines of code:

Gemini 3 Pro, the first model in the new series, is best for complex tasks that require broad world knowledge and advanced reasoning across modalities.

Gemini 3 Flash is our latest 3-series model, with Pro-level intelligence at the speed and pricing of Flash.

Nano Banana Pro (also known as Gemini 3 Pro Image) is our highest quality image generation model yet.

All Gemini 3 models are currently in preview.

* Pricing is per 1 million tokens unless otherwise noted. ** Image pricing varies by resolution. See the pricing page for details.

For detailed limits, pricing, and additional information, see the models page.

Gemini 3 introduces new parameters designed to give developers more control over latency, cost, and multimodal fidelity.

Gemini 3 series models use dynamic thinking by default to reason through prompts. You can use the thinking_level parameter, which controls the maximum depth of the model's internal reasoning process before it produces a response. Gemini 3 treats these levels as relative allowances for thinking rather than strict token guarantees.

If thinking_level is not specified, Gemini 3 will default to high. For faster, lower-latency responses when complex reasoning isn't required, you can constrain the model's thinking level to low.

Gemini 3 Pro and Flash thinking levels:

The following thinking levels are supported by both Gemini 3 Pro and Flash:

Gemini 3 Flash thinking levels

In addition to the levels above, Gemini 3 Flash also supports the following thinking levels that are not currently supported by Gemini 3 Pro:

minimal: Matches the “no thinking” setting for most queries. The model may think very minimally for complex coding tasks. Minimizes latency for chat or high throughput applications.

medium: Balanced thinking for most tasks.

Gemini 3 introduces granular control over multimodal vision processing via the media_resolution parameter. Higher resolutions improve the model's ability to read fine text or identify small details, but increase token usage and latency. The media_resolution parameter determines the maximum number of tokens allocated per input image or video frame.

You can now set the resolution to media_resolution_low, media_resolution_medium, media_resolution_high, or media_resolution_ultra_high per individual media part or globally (via generation_config, global not available for ultra high). If unspecified, the model uses optimal defaults based on the media type.

For Gemini 3, we strongly recommend keeping the temperature parameter at its default value of 1.0.

While previous models often benefited from tuning temperature to control creativity versus determinism, Gemini 3's reasoning capabilities are optimized for the default setting. Changing the temperature (setting it below 1.0) may lead to unexpected behavior, such as looping or degraded performance, particularly in complex mathematical or reasoning tasks.

Gemini 3 uses Thought signatures to maintain reasoning context across API calls. These signatures are encrypted representations of the model's internal thought process. To ensure the model maintains its reasoning capabilities you must return these signatures back to the model in your request exactly as they were received:

Function Calling (Strict): The API enforces strict validation on the "Current Turn". Missing signatures will result in a 400 error.

Text/Chat: Validation is not strictly enforced, but omitting signatures will degrade the model's reasoning and answer quality.

Image generation/editing (Strict): The API enforces strict validation on all Model parts including a thoughtSignature. Missing signatures will result in a 400 error.

When Gemini generates a functionCall, it relies on the thoughtSignature to process the tool's output correctly in the next turn. The "Current Turn" includes all Model (functionCall) and User (functionResponse) steps that occurred since the last standard User text message.

For standard chat or text generation, the presence of a signature is not guaranteed.

For gemini-3-pro-image-preview, thought signatures are critical for conversational editing. When you ask the model to modify an image it relies on the thoughtSignature from the previous turn to understand the composition and logic of the original image.

The user asks a question requiring two separate steps (Check Flight -> Book Taxi) in one turn. Step 1: Model calls Flight Tool. The model returns a signature <Sig_A>

Step 2: User sends Flight Result We must send back <Sig_A> to keep the model's train of thought.

Step 3: Model calls Taxi Tool The model remembers the flight delay via <Sig_A> and now decides to book a taxi. It generates a new signature <Sig_B>.

Step 4: User sends Taxi Result To complete the turn, you must send back the entire chain: <Sig_A> AND <Sig_B>.

The user asks: "Check the weather in Paris and London." The model returns two function calls in one response. // User Request (Sending Parallel Results) [ { "role": "user", "parts": [ { "text": "Check the weather in Paris and London." } ] }, { "role": "model", "parts": [ // 1. First Function Call has the signature { "functionCall": { "name": "check_weather", "args": { "city": "Paris" } }, "thoughtSignature": "<Signature_A>" }, // 2. Subsequent parallel calls DO NOT have signatures { "functionCall": { "name": "check_weather", "args": { "city": "London" } } } ] }, { "role": "user", "parts": [ // 3. Function Responses are grouped together in the next block { "functionResponse": { "name": "check_weather", "response": { "temp": "15C" } } }, { "functionResponse": { "name": "check_weather", "response": { "temp": "12C" } } } ] } ]

The user asks a question that requires in-context reasoning without external tools. While not strictly validated, including the signature helps the model maintain the reasoning chain for follow-up questions.

For image generation, signatures are strictly validated. They appear on the first part (text or image) and all subsequent image parts. All must be returned in the next turn.

If you are transferring a conversation trace from another model (e.g., Gemini 2.5) or injecting a custom function call that was not generated by Gemini 3, you will not have a valid signature.

To bypass strict validation in these specific scenarios, populate the field with this specific dummy string: "thoughtSignature": "context_engineering_is_the_way_to_go"

Gemini 3 models allow you to combine Structured Outputs with built-in tools, including Grounding with Google Search, URL Context, and Code Execution.

Gemini 3 Pro Image lets you generate and edit images from text prompts. It uses reasoning to "think" through a prompt and can retrieve real-time data—such as weather forecasts or stock charts—before using Google Search grounding before generating high-fidelity images.

New & improved capabilities:

For complete details on aspect ratios, editing workflows, and configuration options, see the Image Generation guide.

Gemini 3 is our most capable model family to date and offers a stepwise improvement over Gemini 2.5. When migrating, consider the following:

For users utilizing the OpenAI compatibility layer, standard parameters are automatically mapped to Gemini equivalents:

Gemini 3 is a reasoning model, which changes how you should prompt.

Learn more about prompt design strategies in the prompt engineering guide.

What is the knowledge cutoff for Gemini 3? Gemini 3 models have a knowledge cutoff of January 2025. For more recent information, use the Search Grounding tool.

What are the context window limits? Gemini 3 models support a 1 million token input context window and up to 64k tokens of output.

Is there a free tier for Gemini 3? Gemini 3 Flash gemini-3-flash-preview has a free tier in the Gemini API. You can try both Gemini 3 Pro and Flash for free in Google AI Studio, but currently, there is no free tier available for gemini-3-pro-preview in the Gemini API.

Will my old thinking_budget code still work? Yes, thinking_budget is still supported for backward compatibility, but we recommend migrating to thinking_level for more predictable performance. Do not use both in the same request.

Does Gemini 3 support the Batch API? Yes, Gemini 3 supports the Batch API.

Is Context Caching supported? Yes, Context Caching is supported for Gemini 3. The minimum token count required to initiate caching is 2,048 tokens.

Which tools are supported in Gemini 3? Gemini 3 supports Google Search, File Search, Code Execution, and URL Context. It also supports standard Function Calling for your own custom tools (but not with built-in tools). Please note that Grounding with Google Maps and Computer Use are currently not supported.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Find the race condition in this multi-threaded C++ snippet: [code here]",
)

print(response.text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Find the race condition in this multi-threaded C++ snippet: [code here]",
)

print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function run() {
  const response = await ai.models.generateContent({
    model: "gemini-3-pro-preview",
    contents: "Find the race condition in this multi-threaded C++ snippet: [code here]",
  });

  console.log(response.text);
}

run();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function run() {
  const response = await ai.models.generateContent({
    model: "gemini-3-pro-preview",
    contents: "Find the race condition in this multi-threaded C++ snippet: [code here]",
  });

  console.log(response.text);
}

run();
```

---

## Safety guidance

**URL:** https://ai.google.dev/gemini-api/docs/safety-guidance

**Contents:**
- Safety guidance
- Understand the safety risks of your application
    - Advanced tips
- Consider adjustments to mitigate safety risks
    - Advanced tip
- Perform safety testing appropriate to your use case
    - Advanced tips
    - Advanced tips
- Monitor for problems
    - Advanced tips

Generative artificial intelligence models are powerful tools, but they are not without their limitations. Their versatility and applicability can sometimes lead to unexpected outputs, such as outputs that are inaccurate, biased, or offensive. Post-processing, and rigorous manual evaluation are essential to limit the risk of harm from such outputs.

The models provided by the Gemini API can be used for a wide variety of generative AI and natural language processing (NLP) applications. Use of these functions is only available through the Gemini API or the Google AI Studio web app. Your use of Gemini API is also subject to the Generative AI Prohibited Use Policy and the Gemini API terms of service.

Part of what makes large language models (LLMs) so useful is that they're creative tools that can address many different language tasks. Unfortunately, this also means that large language models can generate output that you don't expect, including text that's offensive, insensitive, or factually incorrect. What's more, the incredible versatility of these models is also what makes it difficult to predict exactly what kinds of undesirable output they might produce. While the Gemini API has been designed with Google's AI principles in mind, the onus is on developers to apply these models responsibly. To aid developers in creating safe, responsible applications, the Gemini API has some built-in content filtering as well as adjustable safety settings across 4 dimensions of harm. Refer to the safety settings guide to learn more.

This document is meant to introduce you to some safety risks that can arise when using LLMs, and recommend emerging safety design and development recommendations. (Note that laws and regulations may also impose restrictions, but such considerations are beyond the scope of this guide.)

The following steps are recommended when building applications with LLMs:

The adjustment and testing phases should be iterative until you reach performance appropriate for your application.

In this context, safety is being defined as the ability of an LLM to avoid causing harm to its users, for example, by generating toxic language or content that promotes stereotypes. The models available through the Gemini API have been designed with Google’s AI principles in mind and your use of it is subject to the Generative AI Prohibited Use Policy. The API provides built-in safety filters to help address some common language model problems such as toxic language and hate speech, and striving for inclusiveness and avoidance of stereotypes. However, each application can pose a different set of risks to its users. So as the application owner, you are responsible for knowing your users and the potential harms your application may cause, and ensuring that your application uses LLMs safely and responsibly.

As part of this assessment, you should consider the likelihood that harm could occur and determine its seriousness and mitigation steps. For example, an app that generates essays based on factual events would need to be more careful about avoiding misinformation, as compared to an app that generates fictional stories for entertainment. A good way to begin exploring potential safety risks is to research your end users, and others who might be affected by your application's results. This can take many forms including researching state of the art studies in your app domain, observing how people are using similar apps, or running a user study, survey, or conducting informal interviews with potential users.

Now that you have an understanding of the risks, you can decide how to mitigate them. Determining which risks to prioritize and how much you should do to try to prevent them is a critical decision, similar to triaging bugs in a software project. Once you've determined priorities, you can start thinking about the types of mitigations that would be most appropriate. Often simple changes can make a difference and reduce risks.

For example, when designing an application consider:

Blocking unsafe inputs and filtering output before it is shown to the user. In simple situations, blocklists can be used to identify and block unsafe words or phrases in prompts or responses, or require human reviewers to manually alter or block such content.

Using trained classifiers to label each prompt with potential harms or adversarial signals. Different strategies can then be employed on how to handle the request based on the type of harm detected. For example, If the input is overtly adversarial or abusive in nature, it could be blocked and instead output a pre-scripted response. Advanced tip If signals determine the output to be harmful, the application can employ the following options: Provide an error message or pre-scripted output. Try the prompt again, in case an alternative safe output is generated, since sometimes the same prompt will elicit different outputs.

Putting safeguards in place against deliberate misuse such as assigning each user a unique ID and imposing a limit on the volume of user queries that can be submitted in a given period. Another safeguard is to try and protect against possible prompt injection. Prompt injection, much like SQL injection, is a way for malicious users to design an input prompt that manipulates the output of the model, for example, by sending an input prompt that instructs the model to ignore any previous examples. See the Generative AI Prohibited Use Policy for details about deliberate misuse.

Adjusting functionality to something that is inherently lower risk. Tasks that are narrower in scope (e.g., extracting keywords from passages of text) or that have greater human oversight (e.g., generating short-form content that will be reviewed by a human), often pose a lower risk. So for instance, instead of creating an application to write an email reply from scratch, you might instead limit it to expanding on an outline or suggesting alternative phrasings.

Testing is a key part of building robust and safe applications, but the extent, scope and strategies for testing will vary. For example, a just-for-fun haiku generator is likely to pose less severe risks than, say, an application designed for use by law firms to summarize legal documents and help draft contracts. But the haiku generator may be used by a wider variety of users which means the potential for adversarial attempts or even unintended harmful inputs can be greater. The implementation context also matters. For instance, an application with outputs that are reviewed by human experts prior to any action being taken might be deemed less likely to produce harmful outputs than the identical application without such oversight.

It's not uncommon to go through several iterations of making changes and testing before feeling confident that you're ready to launch, even for applications that are relatively low risk. Two kinds of testing are particularly useful for AI applications:

Safety benchmarking involves designing safety metrics that reflect the ways your application could be unsafe in the context of how it is likely to get used, then testing how well your application performs on the metrics using evaluation datasets. It's good practice to think about the minimum acceptable levels of safety metrics before testing so that 1) you can evaluate the test results against those expectations and 2) you can gather the evaluation dataset based on the tests that evaluate the metrics you care about most.

Adversarial testing involves proactively trying to break your application. The goal is to identify points of weakness so that you can take steps to remedy them as appropriate. Adversarial testing can take significant time/effort from evaluators with expertise in your application — but the more you do, the greater your chance of spotting problems, especially those occurring rarely or only after repeated runs of the application.

No matter how much you test and mitigate, you can never guarantee perfection, so plan upfront how you'll spot and deal with problems that arise. Common approaches include setting up a monitored channel for users to share feedback (e.g., thumbs up/down rating) and running a user study to proactively solicit feedback from a diverse mix of users — especially valuable if usage patterns are different to expectations.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

---

## Music generation using Lyria RealTime

**URL:** https://ai.google.dev/gemini-api/docs/music-generation

**Contents:**
- Music generation using Lyria RealTime
- How music generation works
- Generate and control music
  - Python
  - JavaScript
- Steer music in real-time
  - Prompt Lyria RealTime
  - Python
  - JavaScript
  - Update the configuration

The Gemini API, using Lyria RealTime, provides access to a state-of-the-art, real-time, streaming music generation model. It allows developers to build applications where users can interactively create, continuously steer, and perform instrumental music.

To experience what can be built using Lyria RealTime, try it on AI Studio using the Prompt DJ or the MIDI DJ apps!

Lyria RealTime music generation uses a persistent, bidirectional, low-latency streaming connection using WebSocket.

Lyria RealTime works a bit like the Live API in the sense that it is using websockets to keep a real-time communication with the model. It's still not exactly the same as you can't talk to the model and you have to use a specific format to prompt it.

The following code demonstrates how to generate music:

This example initializes the Lyria RealTime session using client.aio.live.music.connect(), then sends an initial prompt with session.set_weighted_prompts() along with an initial configuration using session.set_music_generation_config, starts the music generation using session.play() and sets up receive_audio() to process the audio chunks it receives.

For a more complete code sample, refer to the "Lyria RealTime - Get Started" file in the cookbooks repository:

This example initializes the Lyria RealTime session using client.live.music.connect(), then sends an initial prompt with session.setWeightedPrompts() along with an initial configuration using session.setMusicGenerationConfig, starts the music generation using session.play() and sets up an onMessage callback to process the audio chunks it receives.

For a more complete code sample, refer to those two AI studio apps:

Try Prompt DJ on AI Studio

Try MIDI DJ on AI Studio

You can then use session.play(), session.pause(), session.stop() and session.reset_context() to start, pause, stop or reset the session.

While the stream is active, you can send new WeightedPrompt messages at any time to alter the generated music. The model will smoothly transition based on the new input.

The prompts need to follow the right format with a text (the actual prompt), and a weight. The weight can take any value except 0. 1.0 is usually a good starting point.

Note that the model transitions can be a bit abrupt when drastically changing the prompts so it's recommended to implement some kind of cross-fading by sending intermediate weight values to the model.

You can also update the music generation parameters in real time. You can't just update a parameter, you need to set the whole configuration otherwise the other fields will be reset back to their default values.

Since updating the bpm or the scale is a drastic change for the model you'll also need to tell it to reset its context using reset_context() to take the new config into account. It won't stop the stream, but it will be a hard transition. You don't need to do it for the other parameters.

Here's a non-exhaustive list of prompts you can use to prompt Lyria RealTime:

These are just some examples, Lyria RealTime can do much more. Experiment with your own prompts!

This section describes the specifics of how to use Lyria RealTime music generation.

Music generation can be influenced in real time by sending messages containing:

For bpm, density, brightness and scale, if no value is provided, the model will decide what's best according to your initial prompts.

More classical parameters like temperature (0.0 to 3.0, default 1.1), top_k (1 to 1000, default 40), and seed (0 to 2 147 483 647, randomly selected by default) are also customizable in the MusicGenerationConfig.

Here are all the scale values that the model can accept:

The model is capable of guiding the notes that are played, but does not distinguish between relative keys. Thus each enum corresponds both to the relative major and minor. For example, C_MAJOR_A_MINOR would correspond to all the white keys of a piano, and F_MAJOR_D_MINOR would be all the white keys except B flat.

Explore the Cookbook for more code examples and tutorials.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-26 UTC.

**Examples:**

Example 1 (python):
```python
import asyncio
  from google import genai
  from google.genai import types

  client = genai.Client(http_options={'api_version': 'v1alpha'})

  async def main():
      async def receive_audio(session):
        """Example background task to process incoming audio."""
        while True:
          async for message in session.receive():
            audio_data = message.server_content.audio_chunks[0].data
            # Process audio...
            await asyncio.sleep(10**-12)

      async with (
        client.aio.live.music.connect(model='models/lyria-realtime-exp') as session,
        asyncio.TaskGroup() as tg,
      ):
        # Set up task to receive server messages.
        tg.create_task(receive_audio(session))

        # Send initial prompts and config
        await session.set_weighted_prompts(
          prompts=[
            types.WeightedPrompt(text='minimal techno', weight=1.0),
          ]
        )
        await session.set_music_generation_config(
          config=types.LiveMusicGenerationConfig(bpm=90, temperature=1.0)
        )

        # Start streaming music
        await session.play()
  if __name__ == "__main__":
      asyncio.run(main())
```

Example 2 (python):
```python
import asyncio
  from google import genai
  from google.genai import types

  client = genai.Client(http_options={'api_version': 'v1alpha'})

  async def main():
      async def receive_audio(session):
        """Example background task to process incoming audio."""
        while True:
          async for message in session.receive():
            audio_data = message.server_content.audio_chunks[0].data
            # Process audio...
            await asyncio.sleep(10**-12)

      async with (
        client.aio.live.music.connect(model='models/lyria-realtime-exp') as session,
        asyncio.TaskGroup() as tg,
      ):
        # Set up task to receive server messages.
        tg.create_task(receive_audio(session))

        # Send initial prompts and config
        await session.set_weighted_prompts(
          prompts=[
            types.WeightedPrompt(text='minimal techno', weight=1.0),
          ]
        )
        await session.set_music_generation_config(
          config=types.LiveMusicGenerationConfig(bpm=90, temperature=1.0)
        )

        # Start streaming music
        await session.play()
  if __name__ == "__main__":
      asyncio.run(main())
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";
import Speaker from "speaker";
import { Buffer } from "buffer";

const client = new GoogleGenAI({
  apiKey: GEMINI_API_KEY,
    apiVersion: "v1alpha" ,
});

async function main() {
  const speaker = new Speaker({
    channels: 2,       // stereo
    bitDepth: 16,      // 16-bit PCM
    sampleRate: 44100, // 44.1 kHz
  });

  const session = await client.live.music.connect({
    model: "models/lyria-realtime-exp",
    callbacks: {
      onmessage: (message) => {
        if (message.serverContent?.audioChunks) {
          for (const chunk of message.serverContent.audioChunks) {
            const audioBuffer = Buffer.from(chunk.data, "base64");
            speaker.write(audioBuffer);
          }
        }
      },
      onerror: (error) => console.error("music session error:", error),
      onclose: () => console.log("Lyria RealTime stream closed."),
    },
  });

  await session.setWeightedPrompts({
    weightedPrompts: [
      { text: "Minimal techno with deep bass, sparse percussion, and atmospheric synths", weight: 1.0 },
    ],
  });

  await session.setMusicGenerationConfig({
    musicGenerationConfig: {
      bpm: 90,
      temperature: 1.0,
      audioFormat: "pcm16",  // important so we know format
      sampleRateHz: 44100,
    },
  });

  await session.play();
}

main().catch(console.error);
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";
import Speaker from "speaker";
import { Buffer } from "buffer";

const client = new GoogleGenAI({
  apiKey: GEMINI_API_KEY,
    apiVersion: "v1alpha" ,
});

async function main() {
  const speaker = new Speaker({
    channels: 2,       // stereo
    bitDepth: 16,      // 16-bit PCM
    sampleRate: 44100, // 44.1 kHz
  });

  const session = await client.live.music.connect({
    model: "models/lyria-realtime-exp",
    callbacks: {
      onmessage: (message) => {
        if (message.serverContent?.audioChunks) {
          for (const chunk of message.serverContent.audioChunks) {
            const audioBuffer = Buffer.from(chunk.data, "base64");
            speaker.write(audioBuffer);
          }
        }
      },
      onerror: (error) => console.error("music session error:", error),
      onclose: () => console.log("Lyria RealTime stream closed."),
    },
  });

  await session.setWeightedPrompts({
    weightedPrompts: [
      { text: "Minimal techno with deep bass, sparse percussion, and atmospheric synths", weight: 1.0 },
    ],
  });

  await session.setMusicGenerationConfig({
    musicGenerationConfig: {
      bpm: 90,
      temperature: 1.0,
      audioFormat: "pcm16",  // important so we know format
      sampleRateHz: 44100,
    },
  });

  await session.play();
}

main().catch(console.error);
```

---

## Generate videos with Veo 3.1 in Gemini API

**URL:** https://ai.google.dev/gemini-api/docs/video

**Contents:**
- Generate videos with Veo 3.1 in Gemini API
- Text to video generation
  - Python
  - JavaScript
  - Go
  - REST
- Image to video generation
  - Python
  - JavaScript
  - Go

Veo 3.1 is Google's state-of-the-art model for generating high-fidelity, 8-second 720p or 1080p videos featuring stunning realism and natively generated audio. You can access this model programmatically using the Gemini API. To learn more about the available Veo model variants, see the Model Versions section.

Veo 3.1 excels at a wide range of visual and cinematic styles and introduces several new capabilities:

For more information about writing effective text prompts for video generation, see the Veo prompt guide

Choose an example to see how to generate a video with dialogue, cinematic realism, or creative animation:

Dialogue & Sound Effects Cinematic Realism Creative Animation

The following code demonstrates generating an image using Gemini 2.5 Flash Image aka Nano Banana, then using that image as the starting frame for generating a video with Veo 3.1.

Veo 3.1 now accepts up to 3 reference images to guide your generated video's content. Provide images of a person, character, or product to preserve the subject's appearance in the output video.

For example, using these three images generated with Nano Banana as references with a well-written prompt creates the following video:

Veo 3.1 lets you create videos using interpolation, or specifying the first and last frames of the video. For information about writing effective text prompts for video generation, see the Veo prompt guide.

Use Veo 3.1 to extend videos that you previously generated with Veo by 7 seconds and up to 20 times.

Input video limitations:

The output of the extension is a single video combining the user input video and the generated extended video for up to 148 seconds of video.

This example takes the a Veo-generated video, shown here with its original prompt, and extends it using the video parameter and a new prompt:

For information about writing effective text prompts for video generation, see the Veo prompt guide.

Video generation is a computationally intensive task. When you send a request to the API, it starts a long-running job and immediately returns an operation object. You must then poll until the video is ready, which is indicated by the done status being true.

The core of this process is a polling loop, which periodically checks the job's status.

These are the parameters you can set in your API request to control the video generation process.

Note that the seed parameter is also available for Veo 3 models. It doesn't guarantee determinism, but slightly improves it.

You can customize your video generation by setting parameters in your request. For example you can specify negativePrompt to guide the model.

This section contains examples of videos you can create using Veo, and shows you how to modify prompts to produce distinct results.

Veo applies safety filters across Gemini to help ensure that generated videos and uploaded photos don't contain offensive content. Prompts that violate our terms and guidelines are blocked.

Good prompts are descriptive and clear. To get the most out of Veo, start with identifying your core idea, refine your idea by adding keywords and modifiers, and incorporate video-specific terminology into your prompts.

The following elements should be included in your prompt:

For more comprehensive prompting strategies, visit Introduction to prompt design.

With Veo 3, you can provide cues for sound effects, ambient noise, and dialogue. The model captures the nuance of these cues to generate a synchronized soundtrack.

These videos demonstrate prompting Veo 3's audio generation with increasing levels of detail.

Try out these prompts yourself to hear the audio! Try Veo 3

You can use one or more images as inputs to guide your generated videos, using Veo's image-to-video capabilities. Veo uses the input image as the initial frame. Select an image closest to what you envision as the first scene of your video to animate everyday objects, bring drawings and paintings to life, and add movement and sound to nature scenes.

Veo 3.1 lets you reference images or ingredients to direct your generated video's content. Provide up to three asset images of a single person, character, or product. Veo preserves the subject's appearance in the output video.

Using Veo 3.1, you can also generate videos by specifying the first and last frames of the video.

This feature gives you precise control over your shot's composition by letting you define the starting and ending frame. Upload an image or use a frame from a previous video generation to make sure your scene begins and concludes exactly as you envision it.

To extend your Veo-generated video with Veo 3.1, use the video as an input along with an optional text prompt. Extend finalizes the final second or 24 frames of your video and continues the action.

Note that voice is not able to be effectively extended if it's not present in the last 1 second of video.

This section presents several prompts, highlighting how descriptive details can elevate the outcome of each video.

This video demonstrates how you can use the elements of prompt writing basics in your prompt.

These videos demonstrate how you can revise your prompt with increasingly specific details to get Veo to refine the output to your liking.

These examples show you how to refine your prompts by each basic element.

Specify the main focus (subject) and the background or environment (context).

Specify what the subject is doing (e.g., walking, running, or turning their head).

Add keywords to steer the generation toward a specific aesthetic (e.g., surreal, vintage, futuristic, film noir).

Specify how the camera moves (POV shot, aerial view, tracking drone view) and how the shot is framed (wide shot, close-up, low angle).

Color palettes and lighting influence the mood. Try terms like "muted orange warm tones," "natural light," "sunrise," or "cool blue tones."

Negative prompts specify elements you don't want in the video.

Veo lets you specify the aspect ratio for your video.

Check out the Pricing and Rate limits pages for more Veo model-specific usage details.

Veo Fast versions allow developers to create videos with sound while maintaining high quality and optimizing for speed and business use cases. They're ideal for backend services that programmatically generate ads, tools for rapid A/B testing of creative concepts, or apps that need to quickly produce social media content.

veo-3.1-generate-preview

veo-3.1-fast-generate-preview

veo-3.0-fast-generate-001

Any image resolution and aspect ratio up to 20MB file size

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-13 UTC.

**Examples:**

Example 1 (python):
```python
import time
from google import genai
from google.genai import types

client = genai.Client()

prompt = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
)

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the generated video.
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save("dialogue_example.mp4")
print("Generated video saved to dialogue_example.mp4")
```

Example 2 (python):
```python
import time
from google import genai
from google.genai import types

client = genai.Client()

prompt = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
)

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the generated video.
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save("dialogue_example.mp4")
print("Generated video saved to dialogue_example.mp4")
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

const prompt = `A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'`;

let operation = await ai.models.generateVideos({
    model: "veo-3.1-generate-preview",
    prompt: prompt,
});

// Poll the operation status until the video is ready.
while (!operation.done) {
    console.log("Waiting for video generation to complete...")
    await new Promise((resolve) => setTimeout(resolve, 10000));
    operation = await ai.operations.getVideosOperation({
        operation: operation,
    });
}

// Download the generated video.
ai.files.download({
    file: operation.response.generatedVideos[0].video,
    downloadPath: "dialogue_example.mp4",
});
console.log(`Generated video saved to dialogue_example.mp4`);
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

const prompt = `A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'`;

let operation = await ai.models.generateVideos({
    model: "veo-3.1-generate-preview",
    prompt: prompt,
});

// Poll the operation status until the video is ready.
while (!operation.done) {
    console.log("Waiting for video generation to complete...")
    await new Promise((resolve) => setTimeout(resolve, 10000));
    operation = await ai.operations.getVideosOperation({
        operation: operation,
    });
}

// Download the generated video.
ai.files.download({
    file: operation.response.generatedVideos[0].video,
    downloadPath: "dialogue_example.mp4",
});
console.log(`Generated video saved to dialogue_example.mp4`);
```

---

## URL context

**URL:** https://ai.google.dev/gemini-api/docs/url-context

**Contents:**
- URL context
  - Python
  - Javascript
  - REST
- How it works
- Combining with other tools
  - Grounding with search
  - Python
  - Javascript
  - REST

The URL context tool lets you provide additional context to the models in the form of URLs. By including URLs in your request, the model will access the content from those pages (as long as it's not a URL type listed in the limitations section) to inform and enhance its response.

The URL context tool is useful for tasks like the following:

The following example shows how to compare two recipes from different websites.

The URL Context tool uses a two-step retrieval process to balance speed, cost, and access to fresh data. When you provide a URL, the tool first attempts to fetch the content from an internal index cache. This acts as a highly optimized cache. If a URL is not available in the index (for example, if it's a very new page), the tool automatically falls back to do a live fetch. This directly accesses the URL to retrieve its content in real-time.

You can combine the URL context tool with other tools to create more powerful workflows.

When both URL context and Grounding with Google Search are enabled, the model can use its search capabilities to find relevant information online and then use the URL context tool to get a more in-depth understanding of the pages it finds. This approach is powerful for prompts that require both broad searching and deep analysis of specific pages.

When the model uses the URL context tool, the response includes a url_context_metadata object. This object lists the URLs the model retrieved content from and the status of each retrieval attempt, which is useful for verification and debugging.

The following is an example of that part of the response (parts of the response have been omitted for brevity):

For complete detail about this object , see the UrlContextMetadata API reference.

The system performs a content moderation check on the URL to confirm they meet safety standards. If the URL you provided fails this check, you will get an url_retrieval_status of URL_RETRIEVAL_STATUS_UNSAFE.

The content retrieved from the URLs you specify in your prompt is counted as part of the input tokens. You can see the token count for your prompt and tools usage in the usage_metadata object of the model output. The following is an example output:

Price per token depends on the model used, see the pricing page for details.

The tool can extract content from URLs with the following content types:

The following content types are not supported:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai.types import Tool, GenerateContentConfig

client = genai.Client()
model_id = "gemini-2.5-flash"

tools = [
  {"url_context": {}},
]

url1 = "https://www.foodnetwork.com/recipes/ina-garten/perfect-roast-chicken-recipe-1940592"
url2 = "https://www.allrecipes.com/recipe/21151/simple-whole-roast-chicken/"

response = client.models.generate_content(
    model=model_id,
    contents=f"Compare the ingredients and cooking times from the recipes at {url1} and {url2}",
    config=GenerateContentConfig(
        tools=tools,
    )
)

for each in response.candidates[0].content.parts:
    print(each.text)

# For verification, you can inspect the metadata to see which URLs the model retrieved
print(response.candidates[0].url_context_metadata)
```

Example 2 (python):
```python
from google import genai
from google.genai.types import Tool, GenerateContentConfig

client = genai.Client()
model_id = "gemini-2.5-flash"

tools = [
  {"url_context": {}},
]

url1 = "https://www.foodnetwork.com/recipes/ina-garten/perfect-roast-chicken-recipe-1940592"
url2 = "https://www.allrecipes.com/recipe/21151/simple-whole-roast-chicken/"

response = client.models.generate_content(
    model=model_id,
    contents=f"Compare the ingredients and cooking times from the recipes at {url1} and {url2}",
    config=GenerateContentConfig(
        tools=tools,
    )
)

for each in response.candidates[0].content.parts:
    print(each.text)

# For verification, you can inspect the metadata to see which URLs the model retrieved
print(response.candidates[0].url_context_metadata)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: [
        "Compare the ingredients and cooking times from the recipes at https://www.foodnetwork.com/recipes/ina-garten/perfect-roast-chicken-recipe-1940592 and https://www.allrecipes.com/recipe/21151/simple-whole-roast-chicken/",
    ],
    config: {
      tools: [{urlContext: {}}],
    },
  });
  console.log(response.text);

  // For verification, you can inspect the metadata to see which URLs the model retrieved
  console.log(response.candidates[0].urlContextMetadata)
}

await main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: [
        "Compare the ingredients and cooking times from the recipes at https://www.foodnetwork.com/recipes/ina-garten/perfect-roast-chicken-recipe-1940592 and https://www.allrecipes.com/recipe/21151/simple-whole-roast-chicken/",
    ],
    config: {
      tools: [{urlContext: {}}],
    },
  });
  console.log(response.text);

  // For verification, you can inspect the metadata to see which URLs the model retrieved
  console.log(response.candidates[0].urlContextMetadata)
}

await main();
```

---

## OpenAI compatibility

**URL:** https://ai.google.dev/gemini-api/docs/openai

**Contents:**
- OpenAI compatibility
  - Python
  - JavaScript
  - REST
- Thinking
  - Python
  - JavaScript
  - REST
  - Python
  - JavaScript

Gemini models are accessible using the OpenAI libraries (Python and TypeScript / Javascript) along with the REST API, by updating three lines of code and using your Gemini API key. If you aren't already using the OpenAI libraries, we recommend that you call the Gemini API directly.

What changed? Just three lines!

api_key="GEMINI_API_KEY": Replace "GEMINI_API_KEY" with your actual Gemini API key, which you can get in Google AI Studio.

base_url="https://generativelanguage.googleapis.com/v1beta/openai/": This tells the OpenAI library to send requests to the Gemini API endpoint instead of the default URL.

model="gemini-2.5-flash": Choose a compatible Gemini model

Gemini 3 and 2.5 models are trained to think through complex problems, leading to significantly improved reasoning. The Gemini API comes with thinking parameters which give fine grain control over how much the model will think.

Gemini 3 Pro uses "low" and "high" thinking levels, and Gemini 3 Flash uses "minimal", "low", "medium", and "high". Gemini 2.5 models use exact thinking budgets. These map to OpenAI's reasoning efforts as follows:

If no reasoning_effort is specified, Gemini uses the model's default level or budget.

If you want to disable thinking, you can set reasoning_effort to "none" for 2.5 models. Reasoning cannot be turned off for Gemini 2.5 Pro or 3 models.

Gemini thinking models also produce thought summaries. You can use the extra_body field to include Gemini fields in your request.

Note that reasoning_effort and thinking_level/thinking_budget overlap functionality, so they can't be used at the same time.

Gemini 3 supports OpenAI compatibility for thought signatures in chat completion APIs. You can find the full example on the thought signatures page.

The Gemini API supports streaming responses.

Function calling makes it easier for you to get structured data outputs from generative models and is supported in the Gemini API.

Gemini models are natively multimodal and provide best in class performance on many common vision tasks.

Gemini models can output JSON objects in any structure you define.

Text embeddings measure the relatedness of text strings and can be generated using the Gemini API.

You can create batch jobs, submit them, and check their status using the OpenAI library.

You'll need to prepare the JSONL file in OpenAI input format. For example:

OpenAI compatibility for Batch supports creating a batch, monitoring job status, and viewing batch results.

Compatibility for upload and download is currently not supported. Instead, the following example uses the genai client for uploading and downloading files, the same as when using the Gemini Batch API.

The OpenAI SDK also supports generating embeddings with the Batch API. To do so, switch out the create method's endpoint field for an embeddings endpoint, as well as the url and model keys in the JSONL file:

See the Batch embedding generation section of the OpenAI compatibility cookbook for a complete example.

There are several features supported by Gemini that are not available in OpenAI models but can be enabled using the extra_body field.

Here's an example of using extra_body to set cached_content:

Get a list of available Gemini models:

Retrieve a Gemini model:

Support for the OpenAI libraries is still in beta while we extend feature support.

If you have questions about supported parameters, upcoming features, or run into any issues getting started with Gemini, join our Developer Forum.

Try our OpenAI Compatibility Colab to work through more detailed examples.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from openai import OpenAI

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)

print(response.choices[0].message)
```

Example 2 (python):
```python
from openai import OpenAI

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)

print(response.choices[0].message)
```

Example 3 (python):
```python
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: "GEMINI_API_KEY",
    baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/"
});

const response = await openai.chat.completions.create({
    model: "gemini-2.0-flash",
    messages: [
        { role: "system", content: "You are a helpful assistant." },
        {
            role: "user",
            content: "Explain to me how AI works",
        },
    ],
});

console.log(response.choices[0].message);
```

Example 4 (python):
```python
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: "GEMINI_API_KEY",
    baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/"
});

const response = await openai.chat.completions.create({
    model: "gemini-2.0-flash",
    messages: [
        { role: "system", content: "You are a helpful assistant." },
        {
            role: "user",
            content: "Explain to me how AI works",
        },
    ],
});

console.log(response.choices[0].message);
```

---

## Context caching

**URL:** https://ai.google.dev/gemini-api/docs/caching

**Contents:**
- Context caching
- Implicit caching
- Explicit caching
  - Generate content using a cache
  - Videos
  - PDFs
  - List caches
  - Update a cache
  - Delete a cache
  - Explicit caching using the OpenAI library

Python JavaScript Go REST

In a typical AI workflow, you might pass the same input tokens over and over to a model. The Gemini API offers two different caching mechanisms:

Explicit caching is useful in cases where you want to guarantee cost savings, but with some added developer work.

Implicit caching is enabled by default for all Gemini 2.5 models. We automatically pass on cost savings if your request hits caches. There is nothing you need to do in order to enable this. It is effective as of May 8th, 2025. The minimum input token count for context caching is listed in the following table for each model:

To increase the chance of an implicit cache hit:

You can see the number of tokens which were cache hits in the response object's usage_metadata field.

Using the Gemini API explicit caching feature, you can pass some content to the model once, cache the input tokens, and then refer to the cached tokens for subsequent requests. At certain volumes, using cached tokens is lower cost than passing in the same corpus of tokens repeatedly.

When you cache a set of tokens, you can choose how long you want the cache to exist before the tokens are automatically deleted. This caching duration is called the time to live (TTL). If not set, the TTL defaults to 1 hour. The cost for caching depends on the input token size and how long you want the tokens to persist.

This section assumes that you've installed a Gemini SDK (or have curl installed) and that you've configured an API key, as shown in the quickstart.

The following example shows how to generate content using a cached system instruction and video file.

It's not possible to retrieve or view cached content, but you can retrieve cache metadata (name, model, display_name, usage_metadata, create_time, update_time, and expire_time).

To list metadata for all uploaded caches, use CachedContent.list():

To fetch the metadata for one cache object, if you know its name, use get:

You can set a new ttl or expire_time for a cache. Changing anything else about the cache isn't supported.

The following example shows how to update the ttl of a cache using client.caches.update().

To set the expiry time, it will accepts either a datetime object or an ISO-formatted datetime string (dt.isoformat(), like 2025-01-27T16:02:36.473528+00:00). Your time must include a time zone (datetime.utcnow() doesn't attach a time zone, datetime.now(datetime.timezone.utc) does attach a time zone).

The caching service provides a delete operation for manually removing content from the cache. The following example shows how to delete a cache:

If you're using an OpenAI library, you can enable explicit caching using the cached_content property on extra_body.

Context caching is particularly well suited to scenarios where a substantial initial context is referenced repeatedly by shorter requests. Consider using context caching for use cases such as:

Context caching is a paid feature designed to reduce overall operational costs. Billing is based on the following factors:

For up-to-date pricing details, refer to the Gemini API pricing page. To learn how to count tokens, see the Token guide.

Keep the following considerations in mind when using context caching:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-08 UTC.

**Examples:**

Example 1 (python):
```python
import os
import pathlib
import requests
import time

from google import genai
from google.genai import types

client = genai.Client()

# Download video file
url = 'https://storage.googleapis.com/generativeai-downloads/data/SherlockJr._10min.mp4'
path_to_video_file = pathlib.Path('SherlockJr._10min.mp4')
if not path_to_video_file.exists():
  with path_to_video_file.open('wb') as wf:
    response = requests.get(url, stream=True)
    for chunk in response.iter_content(chunk_size=32768):
      wf.write(chunk)

# Upload the video using the Files API
video_file = client.files.upload(file=path_to_video_file)

# Wait for the file to finish processing
while video_file.state.name == 'PROCESSING':
  print('Waiting for video to be processed.')
  time.sleep(2)
  video_file = client.files.get(name=video_file.name)

print(f'Video processing complete: {video_file.uri}')

# You must use an explicit version suffix: "-flash-001", not just "-flash".
model='models/gemini-2.0-flash-001'

# Create a cache with a 5 minute TTL
cache = client.caches.create(
    model=model,
    config=types.CreateCachedContentConfig(
      display_name='sherlock jr movie', # used to identify the cache
      system_instruction=(
          'You are an expert video analyzer, and your job is to answer '
          'the user\'s query based on the video file you have access to.'
      ),
      contents=[video_file],
      ttl="300s",
  )
)

# Construct a GenerativeModel which uses the created cache.
response = client.models.generate_content(
  model = model,
  contents= (
    'Introduce different characters in the movie by describing '
    'their personality, looks, and names. Also list the timestamps '
    'they were introduced for the first time.'),
  config=types.GenerateContentConfig(cached_content=cache.name)
)

print(response.usage_metadata)

# The output should look something like this:
#
# prompt_token_count: 696219
# cached_content_token_count: 696190
# candidates_token_count: 214
# total_token_count: 696433

print(response.text)
```

Example 2 (python):
```python
import os
import pathlib
import requests
import time

from google import genai
from google.genai import types

client = genai.Client()

# Download video file
url = 'https://storage.googleapis.com/generativeai-downloads/data/SherlockJr._10min.mp4'
path_to_video_file = pathlib.Path('SherlockJr._10min.mp4')
if not path_to_video_file.exists():
  with path_to_video_file.open('wb') as wf:
    response = requests.get(url, stream=True)
    for chunk in response.iter_content(chunk_size=32768):
      wf.write(chunk)

# Upload the video using the Files API
video_file = client.files.upload(file=path_to_video_file)

# Wait for the file to finish processing
while video_file.state.name == 'PROCESSING':
  print('Waiting for video to be processed.')
  time.sleep(2)
  video_file = client.files.get(name=video_file.name)

print(f'Video processing complete: {video_file.uri}')

# You must use an explicit version suffix: "-flash-001", not just "-flash".
model='models/gemini-2.0-flash-001'

# Create a cache with a 5 minute TTL
cache = client.caches.create(
    model=model,
    config=types.CreateCachedContentConfig(
      display_name='sherlock jr movie', # used to identify the cache
      system_instruction=(
          'You are an expert video analyzer, and your job is to answer '
          'the user\'s query based on the video file you have access to.'
      ),
      contents=[video_file],
      ttl="300s",
  )
)

# Construct a GenerativeModel which uses the created cache.
response = client.models.generate_content(
  model = model,
  contents= (
    'Introduce different characters in the movie by describing '
    'their personality, looks, and names. Also list the timestamps '
    'they were introduced for the first time.'),
  config=types.GenerateContentConfig(cached_content=cache.name)
)

print(response.usage_metadata)

# The output should look something like this:
#
# prompt_token_count: 696219
# cached_content_token_count: 696190
# candidates_token_count: 214
# total_token_count: 696433

print(response.text)
```

Example 3 (python):
```python
from google import genai
from google.genai import types
import io
import httpx

client = genai.Client()

long_context_pdf_path = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"

# Retrieve and upload the PDF using the File API
doc_io = io.BytesIO(httpx.get(long_context_pdf_path).content)

document = client.files.upload(
  file=doc_io,
  config=dict(mime_type='application/pdf')
)

model_name = "gemini-2.0-flash-001"
system_instruction = "You are an expert analyzing transcripts."

# Create a cached content object
cache = client.caches.create(
    model=model_name,
    config=types.CreateCachedContentConfig(
      system_instruction=system_instruction,
      contents=[document],
    )
)

# Display the cache details
print(f'{cache=}')

# Generate content using the cached prompt and document
response = client.models.generate_content(
  model=model_name,
  contents="Please summarize this transcript",
  config=types.GenerateContentConfig(
    cached_content=cache.name
  ))

# (Optional) Print usage metadata for insights into the API call
print(f'{response.usage_metadata=}')

# Print the generated text
print('\n\n', response.text)
```

Example 4 (python):
```python
from google import genai
from google.genai import types
import io
import httpx

client = genai.Client()

long_context_pdf_path = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"

# Retrieve and upload the PDF using the File API
doc_io = io.BytesIO(httpx.get(long_context_pdf_path).content)

document = client.files.upload(
  file=doc_io,
  config=dict(mime_type='application/pdf')
)

model_name = "gemini-2.0-flash-001"
system_instruction = "You are an expert analyzing transcripts."

# Create a cached content object
cache = client.caches.create(
    model=model_name,
    config=types.CreateCachedContentConfig(
      system_instruction=system_instruction,
      contents=[document],
    )
)

# Display the cache details
print(f'{cache=}')

# Generate content using the cached prompt and document
response = client.models.generate_content(
  model=model_name,
  contents="Please summarize this transcript",
  config=types.GenerateContentConfig(
    cached_content=cache.name
  ))

# (Optional) Print usage metadata for insights into the API call
print(f'{response.usage_metadata=}')

# Print the generated text
print('\n\n', response.text)
```

---

## Interactions API

**URL:** https://ai.google.dev/gemini-api/docs/interactions

**Contents:**
- Interactions API
  - Python
  - JavaScript
  - REST
- Basic interactions
  - Python
  - JavaScript
  - REST
- Conversation
  - Stateful conversation

The Interactions API is a unified interface for interacting with Gemini models and agents. It simplifies state management, tool orchestration, and long-running tasks. For comprehensive view of the API schema, see the API Reference.

General use Function calling Deep Research agent

The following example shows how to call the Interactions API with a text prompt.

The Interactions API is available through our existing SDKs. The simplest way to interact with the model is by providing a text prompt. The input can be a string, a list containing a content objects, or a list of turns with roles and content objects.

You can build multi-turn conversations in two ways:

Pass the id from the previous interaction to the previous_interaction_id parameter to continue a conversation.

Using the interaction id to retrieve previous turns of the conversation.

You can manage conversation history manually on the client side.

You can use the Interactions API for multimodal use cases such as image understanding or video generation.

You can provide multimodal data as base64 encoded data inline or using the Files API for larger files.

You can use Interactions API to generation multimodal outputs.

The Interactions API is designed for building and interacting with agents, and includes support for function calling, built-in tools, structured outputs, and the Model Context Protocol (MCP).

You can use specialized agents like deep-research-pro-preview-12-2025 for complex tasks. To learn more about the Gemini Deep Research Agent, see the Deep Research guide.

This section explains how to use function calling to define custom tools and how to use Google's built-in tools within the Interactions API.

If you don't want to use server-side state, you can manage it all on the client side.

Gemini comes with built-in tools like Grounding with Google Search, Code execution, and URL context.

Remote MCP integration simplifies agent development by allowing the Gemini API to directly call external tools hosted on remote servers.

Enforce a specific JSON output by providing a JSON schema in the response_format parameter. This is useful for tasks like moderation, classification, or data extraction.

Combine built-in tools with structured output to get a reliable JSON object based on information retrieved by a tool.

There are also additional advance features that give you more flexibility in working with Interactions API.

Receive responses incrementally as they are generated.

Customize the model's behavior with generation_config.

The thinking_level parameter lets you control the model's reasoning behavior for all Gemini 2.5 and newer models.

Access files using remote URLs directly in the API call.

Upload files to the Gemini Files API before using them.

You can learn more about the data model in the API Reference. The following is a high level overview of the main components.

The Interactions API is designed around a central resource: the Interaction. An Interaction represents a complete turn in a conversation or task. It acts as a session record, containing the entire history of an interaction, including all user inputs, model thoughts, tool calls, tool results, and final model outputs.

When you make a call to interactions.create, you are creating a new Interaction resource.

Optionally, you can use the id of this resource in a subsequent call using the previous_interaction_id parameter to continue the conversation. The server uses this ID to retrieve the full context, saving you from having to resend the entire chat history. This server-side state management is optional; you can also operate in stateless mode by sending the full conversation history in each request.

By default, all Interaction objects are stored (store=true) in order to simplify use of server-side state management features (with previous_interaction_id), background execution (using background=true) and observability purposes.

If you do not want this, you can set store=false in your request. This control is separate from state management; you can opt out of storage for any interaction. However, note that store=false is incompatible with background=true and prevents using previous_interaction_id for subsequent turns.

You can delete stored interactions at any time using the delete method found in the API Reference. You can only delete interactions if you know the interaction ID.

After the retention period expires, your data will be deleted automatically.

Interactions objects are processed according to the terms.

You can use latest version of the Google GenAI SDKs in order to access Interactions API.

You can learn more about how to install the SDKs on Libraries page.

Unsupported features: The following features are not yet supported but are coming soon:

Output ordering: Content ordering for built-in tools (google_search and url_context) may sometimes be incorrect, with text appearing before the tool execution and result. This is a known issue and a fix is in progress.

Tool combinations: Combining MCP, Function Call, and Built-in tools is not yet supported but is coming soon.

Remote MCP: Gemini 3 does not support remote mcp, this is coming soon.

The Interactions API is currently in an early beta stage. We are actively developing and refining the API capabilities, resource schemas, and SDK interfaces based on real-world usage and developer feedback.

As a result, breaking changes may occur. Updates may include changes to:

For production workloads, you should continue to use the standard generateContent API. It remains the recommended path for stable deployments and will continue to be actively developed and maintained.

Your feedback is critical to the development of the Interactions API. Please share your thoughts, report bugs, or request features on our Google AI Developer Community Forum.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-17 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai

client = genai.Client()

interaction =  client.interactions.create(
    model="gemini-3-pro-preview",
    input="Tell me a short joke about programming."
)

print(interaction.outputs[-1].text)
```

Example 2 (python):
```python
from google import genai

client = genai.Client()

interaction =  client.interactions.create(
    model="gemini-3-pro-preview",
    input="Tell me a short joke about programming."
)

print(interaction.outputs[-1].text)
```

Example 3 (python):
```python
import { GoogleGenAI } from '@google/genai';

const client = new GoogleGenAI({});

const interaction =  await client.interactions.create({
    model: 'gemini-3-pro-preview',
    input: 'Tell me a short joke about programming.',
});

console.log(interaction.outputs[interaction.outputs.length - 1].text);
```

Example 4 (python):
```python
import { GoogleGenAI } from '@google/genai';

const client = new GoogleGenAI({});

const interaction =  await client.interactions.create({
    model: 'gemini-3-pro-preview',
    input: 'Tell me a short joke about programming.',
});

console.log(interaction.outputs[interaction.outputs.length - 1].text);
```

---

## Image generation with Gemini (aka Nano Banana & Nano Banana Pro)

**URL:** https://ai.google.dev/gemini-api/docs/image-generation

**Contents:**
- Image generation with Gemini (aka Nano Banana & Nano Banana Pro)
- Image generation (text-to-image)
  - Python
  - JavaScript
  - Go
  - Java
  - REST
- Image editing (text-and-image-to-image)
  - Python
  - JavaScript

Gemini can generate and process images conversationally. You can prompt either the fast Gemini 2.5 Flash (aka Nano Banana) or the advanced Gemini 3 Pro Preview (aka Nano Banana Pro) image models with text, images, or a combination of both, allowing you to create, edit, and iterate on visuals with unprecedented control:

All generated images include a SynthID watermark.

Reminder: Make sure you have the necessary rights to any images you upload. Don't generate content that infringe on others' rights, including videos or images that deceive, harass, or harm. Your use of this generative AI service is subject to our Prohibited Use Policy.

Provide an image and use text prompts to add, remove, or modify elements, change the style, or adjust the color grading.

The following example demonstrates uploading base64 encoded images. For multiple images, larger payloads, and supported MIME types, check the Image understanding page.

Keep generating and editing images conversationally. Chat or multi-turn conversation is the recommended way to iterate on images. The following example shows a prompt to generate an infographic about photosynthesis.

You can then use the same chat to change the language on the graphic to Spanish.

Gemini 3 Pro Image (gemini-3-pro-image-preview) is a state-of-the-art image generation and editing model optimized for professional asset production. Designed to tackle the most challenging workflows through advanced reasoning, it excels at complex, multi-turn creation and modification tasks.

Gemini 3 Pro Preview lets you to mix up to 14 reference images. These 14 images can include the following:

Up to 5 images of humans to maintain character consistency

Use the Google Search tool to generate images based on real-time information, such as weather forecasts, stock charts, or recent events.

Note that when using Grounding with Google Search with image generation, image-based search results are not passed to the generation model and are excluded from the response.

The response includes groundingMetadata which contains the following required fields:

Gemini 3 Pro Image generates 1K images by default but can also output 2K and 4K images. To generate higher resolution assets, specify the image_size in the generation_config.

You must use an uppercase 'K' (e.g., 1K, 2K, 4K). Lowercase parameters (e.g., 1k) will be rejected.

The following is an example image generated from this prompt:

The Gemini 3 Pro Image Preview model is a thinking model and uses a reasoning process ("Thinking") for complex prompts. This feature is enabled by default and cannot be disabled in the API. To learn more about the thinking process, see the Gemini Thinking guide.

The model generates up to two interim images to test composition and logic. The last image within Thinking is also the final rendered image.

You can check the thoughts that lead to the final image being produced.

Thought signatures are encrypted representations of the model's internal thought process and are used to preserve reasoning context across multi-turn interactions. All responses include a thought_signature field. As a general rule, if you receive a thought signature in a model response, you should pass it back exactly as received when sending the conversation history in the next turn. Failure to circulate thought signatures may cause the response to fail. Check the thought signature documentation for more explanations of signatures overall.

Here is how thought signatures work:

The following code shows an example of where thought signatures are included:

Gemini supports other image interaction modes based on prompt structure and context, including:

If you need to generate a lot of images, you can use the Batch API. You get higher rate limits in exchange for a turnaround of up to 24 hours.

Check the Batch API image generation documentation and the cookbook for Batch API image examples and code.

Mastering image generation starts with one fundamental principle:

Describe the scene, don't just list keywords. The model's core strength is its deep language understanding. A narrative, descriptive paragraph will almost always produce a better, more coherent image than a list of disconnected words.

The following strategies will help you create effective prompts to generate exactly the images you're looking for.

For realistic images, use photography terms. Mention camera angles, lens types, lighting, and fine details to guide the model toward a photorealistic result.

To create stickers, icons, or assets, be explicit about the style and request a transparent background.

Gemini excels at rendering text. Be clear about the text, the font style (descriptively), and the overall design. Use Gemini 3 Pro Image Preview for professional asset production.

Perfect for creating clean, professional product shots for e-commerce, advertising, or branding.

Excellent for creating backgrounds for websites, presentations, or marketing materials where text will be overlaid.

Builds on character consistency and scene description to create panels for visual storytelling. For accuracy with text and storytelling ability, these prompts work best with Gemini 3 Pro Image Preview.

Use Google Search to generate images based on recent or real-time information. This is useful for news, weather, and other time-sensitive topics.

These examples show how to provide images alongside your text prompts for editing, composition, and style transfer.

Provide an image and describe your change. The model will match the original image's style, lighting, and perspective.

Conversationally define a "mask" to edit a specific part of an image while leaving the rest untouched.

Provide an image and ask the model to recreate its content in a different artistic style.

Provide multiple images as context to create a new, composite scene. This is perfect for product mockups or creative collages.

To ensure critical details (like a face or logo) are preserved during an edit, describe them in great detail along with your edit request.

Upload a rough sketch or drawing and ask the model to refine it into a finished image.

You can generate 360-degree views of a character by iteratively prompting for different angles. For best results, include previously generated images in subsequent prompts to maintain consistency. For complex poses, include a reference image of the desired pose.

To elevate your results from good to great, incorporate these professional strategies into your workflow.

You can optionally configure the response modalities and aspect ratio of the model's output in the config field of generate_content calls.

The model defaults to returning text and image responses (i.e. response_modalities=['Text', 'Image']). You can configure the response to return only images without text using response_modalities=['Image'].

The model defaults to matching the output image size to that of your input image, or otherwise generates 1:1 squares. You can control the aspect ratio of the output image using the aspect_ratio field under image_config in the response request, shown here:

The different ratios available and the size of the image generated are listed in the following tables:

Gemini 2.5 Flash Image

Gemini 3 Pro Image Preview

Choose the model best suited for your specific use case.

Gemini 3 Pro Image Preview (Nano Banana Pro Preview) is designed for professional asset production and complex instructions. This model features real-world grounding using Google Search, a default "Thinking" process that refines composition prior to generation, and can generate images of up to 4K resolutions.

Gemini 2.5 Flash Image (Nano Banana) is designed for speed and efficiency. This model is optimized for high-volume, low-latency tasks and generates images at 1024px resolution.

In addition to using Gemini's built-in image generation capabilities, you can also access Imagen, our specialized image generation model, through the Gemini API.

Imagen 4 should be your go-to model when starting to generate images with Imagen. Choose Imagen 4 Ultra for advanced use-cases or when you need the best image quality (note that can only generate one image at a time).

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-08 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

prompt = (
    "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
```

Example 2 (python):
```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

prompt = (
    "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {

  const ai = new GoogleGenAI({});

  const prompt =
    "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme";

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash-image",
    contents: prompt,
  });
  for (const part of response.candidates[0].content.parts) {
    if (part.text) {
      console.log(part.text);
    } else if (part.inlineData) {
      const imageData = part.inlineData.data;
      const buffer = Buffer.from(imageData, "base64");
      fs.writeFileSync("gemini-native-image.png", buffer);
      console.log("Image saved as gemini-native-image.png");
    }
  }
}

main();
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {

  const ai = new GoogleGenAI({});

  const prompt =
    "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme";

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash-image",
    contents: prompt,
  });
  for (const part of response.candidates[0].content.parts) {
    if (part.text) {
      console.log(part.text);
    } else if (part.inlineData) {
      const imageData = part.inlineData.data;
      const buffer = Buffer.from(imageData, "base64");
      fs.writeFileSync("gemini-native-image.png", buffer);
      console.log("Image saved as gemini-native-image.png");
    }
  }
}

main();
```

---

## Image understanding

**URL:** https://ai.google.dev/gemini-api/docs/vision

**Contents:**
- Image understanding
- Passing images to Gemini
  - Passing inline image data
  - Python
  - JavaScript
  - Go
  - REST
  - Python
  - JavaScript
  - Go

Gemini models are built to be multimodal from the ground up, unlocking a wide range of image processing and computer vision tasks including but not limited to image captioning, classification, and visual question answering without having to train specialized ML models.

You can provide images as input to Gemini using two methods:

You can pass inline image data in the request to generateContent. You can provide image data as Base64 encoded strings or by reading local files directly (depending on the language).

The following example shows how to read an image from a local file and pass it to generateContent API for processing.

You can also fetch an image from a URL, convert it to bytes, and pass it to generateContent as shown in the following examples.

For large files or to be able to use the same image file repeatedly, use the Files API. The following code uploads an image file and then uses the file in a call to generateContent. See the Files API guide for more information and examples.

You can provide multiple images in a single prompt by including multiple image Part objects in the contents array. These can be a mix of inline data (local files or URLs) and File API references.

From Gemini 2.0 onwards, models are further trained to detect objects in an image and get their bounding box coordinates. The coordinates, relative to image dimensions, scale to [0, 1000]. You need to descale these coordinates based on your original image size.

For more examples, check following notebooks in the Gemini Cookbook:

Starting with Gemini 2.5, models not only detect items but also segment them and provide their contour masks.

The model predicts a JSON list, where each item represents a segmentation mask. Each item has a bounding box ("box_2d") in the format [y0, x0, y1, x1] with normalized coordinates between 0 and 1000, a label ("label") that identifies the object, and finally the segmentation mask inside the bounding box, as base64 encoded png that is a probability map with values between 0 and 255. The mask needs to be resized to match the bounding box dimensions, then binarized at your confidence threshold (127 for the midpoint).

Check the segmentation example in the cookbook guide for a more detailed example.

Gemini supports the following image format MIME types:

All Gemini model versions are multimodal and can be utilized in a wide range of image processing and computer vision tasks including but not limited to image captioning, visual question and answering, image classification, object detection and segmentation.

Gemini can reduce the need to use specialized ML models depending on your quality and performance requirements.

Some later model versions are specifically trained improve accuracy of specialized tasks in addition to generic capabilities:

Gemini 2.0 models are further trained to support enhanced object detection.

Gemini 2.5 models are further trained to support enhanced segmentation in addition to object detection.

Gemini 2.5 Pro/Flash, 2.0 Flash, 1.5 Pro, and 1.5 Flash support a maximum of 3,600 image files per request.

A rough formula for calculating the number of tiles is as follows:

For example, for an image of dimensions 960x540 would have a crop unit size of 360. Divide each dimension by 360 and the number of tile is 3 * 2 = 6.

Gemini 3 introduces granular control over multimodal vision processing with the media_resolution parameter. The media_resolution parameter determines the maximum number of tokens allocated per input image or video frame. Higher resolutions improve the model's ability to read fine text or identify small details, but increase token usage and latency.

For more details about the parameter and how it can impact token calculations, see the media resolution guide.

This guide shows you how to upload image files and generate text outputs from image inputs. To learn more, see the following resources:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-18 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
  from google.genai import types

  with open('path/to/small-sample.jpg', 'rb') as f:
      image_bytes = f.read()

  client = genai.Client()
  response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
      types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/jpeg',
      ),
      'Caption this image.'
    ]
  )

  print(response.text)
```

Example 2 (python):
```python
from google import genai
  from google.genai import types

  with open('path/to/small-sample.jpg', 'rb') as f:
      image_bytes = f.read()

  client = genai.Client()
  response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
      types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/jpeg',
      ),
      'Caption this image.'
    ]
  )

  print(response.text)
```

Example 3 (python):
```python
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});
const base64ImageFile = fs.readFileSync("path/to/small-sample.jpg", {
  encoding: "base64",
});

const contents = [
  {
    inlineData: {
      mimeType: "image/jpeg",
      data: base64ImageFile,
    },
  },
  { text: "Caption this image." },
];

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: contents,
});
console.log(response.text);
```

Example 4 (python):
```python
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});
const base64ImageFile = fs.readFileSync("path/to/small-sample.jpg", {
  encoding: "base64",
});

const contents = [
  {
    inlineData: {
      mimeType: "image/jpeg",
      data: base64ImageFile,
    },
  },
  { text: "Caption this image." },
];

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: contents,
});
console.log(response.text);
```

---

## Market Research Agent with Gemini and the AI SDK by Vercel

**URL:** https://ai.google.dev/gemini-api/docs/vercel-ai-sdk-example

**Contents:**
- Market Research Agent with Gemini and the AI SDK by Vercel
- Prerequisites
- Set up your application
  - npm
  - pnpm
  - yarn
  - Install dependencies
  - npm
  - pnpm
  - yarn

The AI SDK by Vercel is a powerful open-source library for building AI-powered applications, user interfaces, and agents in TypeScript.

This guide will walk you through building a Node.js application with TypeScript that uses the AI SDK to connect with the Gemini API via the Google Generative AI Provider and perform automated market trend analysis. The final application will:

To complete this guide, you'll need:

First, create a new directory for your project and initialize it.

Next, install the AI SDK, the Google Generative AI provider, and other necessary dependencies.

To prevent a TypeScript compiler error, comment out the following line in the generated tsconfig.json:

To prevent a TypeScript compiler error, comment out the following line in the generated tsconfig.json:

This application will also use the third-party packages Puppeteer and Chart.js for rendering charts and creating a PDF:

The puppeteer package requires running a script to download the Chromium browser. Your package manager may ask for approval, so ensure you approve the script when prompted.

Set the GOOGLE_GENERATIVE_AI_API_KEY environment variable with your Gemini API key. The Google Generative AI Provider automatically looks for your API key in this environment variable.

Now, let's create the main file for our application. Create a new file named main.ts in your project directory. You'll build up the logic in this file step-by-step.

For a quick test to ensure everything is set up correctly, add the following code to main.ts. This basic example uses Gemini 2.5 Flash and generateText to get a simple response from Gemini.

Before adding more complexity, let's run this script to verify that your environment is configured correctly. Run the following command in your terminal:

If everything is set up correctly, you'll see Gemini's response printed to the console.

To get up-to-date information, you can enable the Google Search tool for Gemini. When this tool is active, the model can search the web to answer the prompt and will return the sources it used.

Replace the content of main.ts with the following code to perform the first step of our analysis.

Next, let's process the research text to extract structured data suitable for charts. Use the AI SDK's generateObject function along with a zod schema to define the exact data structure.

Also create a helper function to convert this structured data into a configuration that Chart.js can understand.

Add the following code to main.ts. Note the new imports and the added "Step 2".

In the final step, instruct Gemini to act as an expert report writer. Provide it with the market research, the chart configurations, and a clear set of instructions for building an HTML report. Then, use Puppeteer to render this HTML and save it as a PDF.

Add the final puppeteer import and "Step 3" to your main.ts file.

You are now ready to run the application. Execute the following command in your terminal:

You will see logging in your terminal as the script executes each step. Once complete, a report.pdf file containing your market analysis will be created in your project directory.

Below, you'll see the first two pages of an example PDF report:

For more information about building with Gemini and the AI SDK, explore these resources:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

**Examples:**

Example 1 (unknown):
```unknown
mkdir market-trend-app
cd market-trend-app
npm init -y
```

Example 2 (unknown):
```unknown
mkdir market-trend-app
```

Example 3 (unknown):
```unknown
cd market-trend-app
```

Example 4 (unknown):
```unknown
npm init -y
```

---

## Live API capabilities guide

**URL:** https://ai.google.dev/gemini-api/docs/live-guide

**Contents:**
- Live API capabilities guide
- Before you begin
- Establishing a connection
  - Python
  - JavaScript
- Interaction modalities
  - Sending and receiving audio
  - Audio formats
  - Sending text
  - Python

This is a comprehensive guide that covers capabilities and configurations available with the Live API. See Get started with Live API page for a overview and sample code for common use cases.

The following example shows how to create a connection with an API key:

The following sections provide examples and supporting context for the different input and output modalities available in Live API.

The most common audio example, audio-to-audio, is covered in the Getting started guide.

Audio data in the Live API is always raw, little-endian, 16-bit PCM. Audio output always uses a sample rate of 24kHz. Input audio is natively 16kHz, but the Live API will resample if needed so any sample rate can be sent. To convey the sample rate of input audio, set the MIME type of each audio-containing Blob to a value like audio/pcm;rate=16000.

Here's how you can send text:

Use incremental updates to send text input, establish session context, or restore session context. For short contexts you can send turn-by-turn interactions to represent the exact sequence of events:

For longer contexts it's recommended to provide a single message summary to free up the context window for subsequent interactions. See Session Resumption for another method for loading session context.

In addition to the model response, you can also receive transcriptions of both the audio output and the audio input.

To enable transcription of the model's audio output, send output_audio_transcription in the setup config. The transcription language is inferred from the model's response.

To enable transcription of the model's audio input, send input_audio_transcription in setup config.

To see an example of how to use the Live API in a streaming audio and video format, run the "Live API - Get Started" file in the cookbooks repository:

Native audio output models support any of the voices available for our Text-to-Speech (TTS) models. You can listen to all the voices in AI Studio.

To specify a voice, set the voice name within the speechConfig object as part of the session configuration:

The Live API supports multiple languages. Native audio output models automatically choose the appropriate language and don't support explicitly setting the language code.

Our latest models feature native audio output, which provides natural, realistic-sounding speech and improved multilingual performance. Native audio also enables advanced features like affective (emotion-aware) dialogue, proactive audio (where the model intelligently decides when to respond to input), and "thinking".

This feature lets Gemini adapt its response style to the input expression and tone.

To use affective dialog, set the api version to v1alpha and set enable_affective_dialog to truein the setup message:

When this feature is enabled, Gemini can proactively decide not to respond if the content is not relevant.

To use it, set the api version to v1alpha and configure the proactivity field in the setup message and set proactive_audio to true:

The latest native audio output model gemini-2.5-flash-native-audio-preview-12-2025 supports thinking capabilities, with dynamic thinking enabled by default.

The thinkingBudget parameter guides the model on the number of thinking tokens to use when generating a response. You can disable thinking by setting thinkingBudget to 0. For more info on the thinkingBudget configuration details of the model, see the thinking budgets documentation.

Additionally, you can enable thought summaries by setting includeThoughts to true in your configuration. See thought summaries for more info:

Voice Activity Detection (VAD) allows the model to recognize when a person is speaking. This is essential for creating natural conversations, as it allows a user to interrupt the model at any time.

When VAD detects an interruption, the ongoing generation is canceled and discarded. Only the information already sent to the client is retained in the session history. The server then sends a BidiGenerateContentServerContent message to report the interruption.

The Gemini server then discards any pending function calls and sends a BidiGenerateContentServerContent message with the IDs of the canceled calls.

By default, the model automatically performs VAD on a continuous audio input stream. VAD can be configured with the realtimeInputConfig.automaticActivityDetection field of the setup configuration.

When the audio stream is paused for more than a second (for example, because the user switched off the microphone), an audioStreamEnd event should be sent to flush any cached audio. The client can resume sending audio data at any time.

With send_realtime_input, the API will respond to audio automatically based on VAD. While send_client_content adds messages to the model context in order, send_realtime_input is optimized for responsiveness at the expense of deterministic ordering.

For more control over the VAD activity, you can configure the following parameters. See API reference for more info.

Alternatively, the automatic VAD can be disabled by setting realtimeInputConfig.automaticActivityDetection.disabled to true in the setup message. In this configuration the client is responsible for detecting user speech and sending activityStart and activityEnd messages at the appropriate times. An audioStreamEnd isn't sent in this configuration. Instead, any interruption of the stream is marked by an activityEnd message.

You can find the total number of consumed tokens in the usageMetadata field of the returned server message.

You can specify the media resolution for the input media by setting the mediaResolution field as part of the session configuration:

Consider the following limitations of the Live API when you plan your project.

You can only set one response modality (TEXT or AUDIO) per session in the session configuration. Setting both results in a config error message. This means that you can configure the model to respond with either text or audio, but not both in the same session.

The Live API only provides server-to-server authentication by default. If you're implementing your Live API application using a client-to-server approach, you need to use ephemeral tokens to mitigate security risks.

Audio-only sessions are limited to 15 minutes, and audio plus video sessions are limited to 2 minutes. However, you can configure different session management techniques for unlimited extensions on session duration.

A session has a context window limit of:

Live API supports the following languages.

Languages marked with an asterisk (*) are not available for Native audio.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-12 UTC.

**Examples:**

Example 1 (python):
```python
import asyncio
from google import genai

client = genai.Client()

model = "gemini-2.5-flash-native-audio-preview-12-2025"
config = {"response_modalities": ["AUDIO"]}

async def main():
    async with client.aio.live.connect(model=model, config=config) as session:
        print("Session started")
        # Send content...

if __name__ == "__main__":
    asyncio.run(main())
```

Example 2 (python):
```python
import asyncio
from google import genai

client = genai.Client()

model = "gemini-2.5-flash-native-audio-preview-12-2025"
config = {"response_modalities": ["AUDIO"]}

async def main():
    async with client.aio.live.connect(model=model, config=config) as session:
        print("Session started")
        # Send content...

if __name__ == "__main__":
    asyncio.run(main())
```

Example 3 (python):
```python
import { GoogleGenAI, Modality } from '@google/genai';

const ai = new GoogleGenAI({});
const model = 'gemini-2.5-flash-native-audio-preview-12-2025';
const config = { responseModalities: [Modality.AUDIO] };

async function main() {

  const session = await ai.live.connect({
    model: model,
    callbacks: {
      onopen: function () {
        console.debug('Opened');
      },
      onmessage: function (message) {
        console.debug(message);
      },
      onerror: function (e) {
        console.debug('Error:', e.message);
      },
      onclose: function (e) {
        console.debug('Close:', e.reason);
      },
    },
    config: config,
  });

  console.debug("Session started");
  // Send content...

  session.close();
}

main();
```

Example 4 (python):
```python
import { GoogleGenAI, Modality } from '@google/genai';

const ai = new GoogleGenAI({});
const model = 'gemini-2.5-flash-native-audio-preview-12-2025';
const config = { responseModalities: [Modality.AUDIO] };

async function main() {

  const session = await ai.live.connect({
    model: model,
    callbacks: {
      onopen: function () {
        console.debug('Opened');
      },
      onmessage: function (message) {
        console.debug(message);
      },
      onerror: function (e) {
        console.debug('Error:', e.message);
      },
      onclose: function (e) {
        console.debug('Close:', e.reason);
      },
    },
    config: config,
  });

  console.debug("Session started");
  // Send content...

  session.close();
}

main();
```

---
