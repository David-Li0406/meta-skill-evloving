# Openai-Api - Assistants

**Pages:** 5

---

## Assistants migration guide

**URL:** https://platform.openai.com/docs/assistants

**Contents:**
- Assistants migration guide
  - What's changed?
- From assistants to prompts
  - Why this is helpful
  - Practical migration steps
- From threads to conversations
  - Request example
  - Response example
- From runs to responses
  - Request example

We're moving from the Assistants API to the new Responses API for a simpler and more flexible mental model.

Responses are simpler—send input items and get output items back. With the Responses API, you also get better performance and new features like deep research, MCP, and computer use. This change also lets you manage conversations instead of passing back previous_response_id.

Assistants were persistent API objects that bundled model choice, instructions, and tool declarations—created and managed entirely through the API. Their replacement, prompts, can only be created in the dashboard, where you can version them as you develop your product.

Think of a prompt as a versioned behavioral profile to plug into either Responses or Realtime API.

A thread was a collection of messages stored server-side. Threads could only store messages. Conversations store items, which can include messages, tool calls, tool outputs, and other data.

Runs were asynchronous processes that executed against threads. See the example below. Responses are simpler: provide a set of input items to execute, and get a list of output items back.

Responses are designed to be used alone, but you can also use them with prompt and conversation objects for storing context and configuration.

Follow the migration steps below to move from the Assistants API to the Responses API, without losing any feature support.

This will create a prompt object out of each existing assistant object.

We will not provide an automated tool for migrating Threads to Conversations. Instead, we recommend migrating new user threads onto conversations and backfilling old ones as necessary.

Here's an example for how you might backfill a thread:

Here’s a few simple examples of integrations using both the Assistants API and the Responses API so you can see how they compare.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
thread = openai.beta.threads.create(
  messages=[{"role": "user", "content": "what are the 5 Ds of dodgeball?"}],
  metadata={"user_id": "peter_le_fleur"},
)
```

Example 2 (python):
```python
1
2
3
4
thread = openai.beta.threads.create(
  messages=[{"role": "user", "content": "what are the 5 Ds of dodgeball?"}],
  metadata={"user_id": "peter_le_fleur"},
)
```

Example 3 (unknown):
```unknown
1
2
3
4
conversation = openai.conversations.create(
  items=[{"role": "user", "content": "what are the 5 Ds of dodgeball?"}],
  metadata={"user_id": "peter_le_fleur"},
)
```

Example 4 (python):
```python
1
2
3
4
conversation = openai.conversations.create(
  items=[{"role": "user", "content": "what are the 5 Ds of dodgeball?"}],
  metadata={"user_id": "peter_le_fleur"},
)
```

---

## Assistants API toolsDeprecated

**URL:** https://platform.openai.com/docs/assistants/tools

**Contents:**
- Assistants API toolsDeprecated
- Overview
- Next steps

Assistants created using the Assistants API can be equipped with tools that allow them to perform more complex tasks or interact with your application. We provide built-in tools for assistants, but you can also define your own tools to extend their capabilities using Function Calling.

The Assistants API currently supports the following tools:

Built-in RAG tool to process and search through files

Write and run python code, process files and diverse data

Use your own custom functions to interact with your application

---

## Assistants API deep diveDeprecated

**URL:** https://platform.openai.com/docs/assistants/deep-dive

**Contents:**
- Assistants API deep diveDeprecated
- Overview
- Creating assistants
- Managing Threads and Messages
  - Creating image input content
    - Low or high fidelity image understanding
  - Context window management
    - Max Completion and Max Prompt Tokens
    - Truncation Strategy
  - Message annotations

Don't start a new integration on the Assistants API. We've announced plans to deprecate it soon, as the Responses API now provides the same features and a more elegant integration.

There are several concepts involved in building an app with the Assistants API, covered below in case it helps with your migration to Responses.

We recommend using OpenAI's latest models with the Assistants API for best results and maximum compatibility with tools.

To get started, creating an Assistant only requires specifying the model to use. But you can further customize the behavior of the Assistant:

For example, to create an Assistant that can create data visualization based on a .csv file, first upload a file.

Then, create the Assistant with the code_interpreter tool enabled and provide the file as a resource to the tool.

You can attach a maximum of 20 files to code_interpreter and 10,000 files to file_search (using vector_store objects).

Each file can be at most 512 MB in size and have a maximum of 5,000,000 tokens. By default, the size of all the files uploaded in your project cannot exceed 100 GB, but you can reach out to our support team to increase this limit.

Threads and Messages represent a conversation session between an Assistant and a user. There is a limit of 100,000 Messages per Thread. Once the size of the Messages exceeds the context window of the model, the Thread will attempt to smartly truncate messages, before fully dropping the ones it considers the least important.

You can create a Thread with an initial list of Messages like this:

Messages can contain text, images, or file attachment. Message attachments are helper methods that add files to a thread's tool_resources. You can also choose to add files to the thread.tool_resources directly.

Message content can contain either external image URLs or File IDs uploaded via the File API. Only models with Vision support can accept image input. Supported image content types include png, jpg, gif, and webp. When creating image files, pass purpose="vision" to allow you to later download and display the input content. Currently, there is a 100GB limit per project. Please contact us to request a limit increase.

Tools cannot access image content unless specified. To pass image files to Code Interpreter, add the file ID in the message attachments list to allow the tool to read and analyze the input. Image URLs cannot be downloaded in Code Interpreter today.

By controlling the detail parameter, which has three options, low, high, or auto, you have control over how the model processes the image and generates its textual understanding.

The Assistants API automatically manages the truncation to ensure it stays within the model's maximum context length. You can customize this behavior by specifying the maximum tokens you'd like a run to utilize and/or the maximum number of recent messages you'd like to include in a run.

To control the token usage in a single Run, set max_prompt_tokens and max_completion_tokens when creating the Run. These limits apply to the total number of tokens used in all completions throughout the Run's lifecycle.

For example, initiating a Run with max_prompt_tokens set to 500 and max_completion_tokens set to 1000 means the first completion will truncate the thread to 500 tokens and cap the output at 1000 tokens. If only 200 prompt tokens and 300 completion tokens are used in the first completion, the second completion will have available limits of 300 prompt tokens and 700 completion tokens.

If a completion reaches the max_completion_tokens limit, the Run will terminate with a status of incomplete, and details will be provided in the incomplete_details field of the Run object.

When using the File Search tool, we recommend setting the max_prompt_tokens to no less than 20,000. For longer conversations or multiple interactions with File Search, consider increasing this limit to 50,000, or ideally, removing the max_prompt_tokens limits altogether to get the highest quality results.

You may also specify a truncation strategy to control how your thread should be rendered into the model's context window. Using a truncation strategy of type auto will use OpenAI's default truncation strategy. Using a truncation strategy of type last_messages will allow you to specify the number of the most recent messages to include in the context window.

Messages created by Assistants may contain annotations within the content array of the object. Annotations provide information around how you should annotate the text in the Message.

There are two types of Annotations:

When annotations are present in the Message object, you'll see illegible model-generated substrings in the text that you should replace with the annotations. These strings may look something like 【13†source】 or sandbox:/mnt/data/file.csv. Here’s an example python code snippet that replaces these strings with the annotations.

When you have all the context you need from your user in the Thread, you can run the Thread with an Assistant of your choice.

By default, a Run will use the model and tools configuration specified in Assistant object, but you can override most of these when creating the Run for added flexibility:

Note: tool_resources associated with the Assistant cannot be overridden during Run creation. You must use the modify Assistant endpoint to do this.

Run objects can have multiple statuses.

If you are not using streaming, in order to keep the status of your run up to date, you will have to periodically retrieve the Run object. You can check the status of the run each time you retrieve the object to determine what your application should do next.

You can optionally use Polling Helpers in our Node and Python SDKs to help you with this. These helpers will automatically poll the Run object for you and return the Run object when it's in a terminal state.

When a Run is in_progress and not in a terminal state, the Thread is locked. This means that:

Run step statuses have the same meaning as Run statuses.

Most of the interesting detail in the Run Step object lives in the step_details field. There can be two types of step details:

Currently, Assistants, Threads, Messages, and Vector Stores created via the API are scoped to the Project they're created in. As such, any person with API key access to that Project is able to read or write Assistants, Threads, Messages, and Runs in the Project.

We strongly recommend the following data access controls:

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
file = client.files.create(
  file=open("revenue-forecast.csv", "rb"),
  purpose='assistants'
)
```

Example 2 (python):
```python
1
2
3
4
file = client.files.create(
  file=open("revenue-forecast.csv", "rb"),
  purpose='assistants'
)
```

Example 3 (javascript):
```javascript
1
2
3
4
const file = await openai.files.create({
  file: fs.createReadStream("revenue-forecast.csv"),
  purpose: "assistants",
});
```

Example 4 (javascript):
```javascript
1
2
3
4
const file = await openai.files.create({
  file: fs.createReadStream("revenue-forecast.csv"),
  purpose: "assistants",
});
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/assistants-streaming

**Contents:**
- StreamingBeta
- The message delta objectBeta
- The run step delta objectBeta
- Assistant stream eventsBeta

Stream the result of executing a Run or resuming a Run after submitting tool outputs. You can stream events from the Create Thread and Run, Create Run, and Submit Tool Outputs endpoints by passing "stream": true. The response will be a Server-Sent events stream. Our Node and Python SDKs provide helpful utilities to make streaming easy. Reference the Assistants API quickstart to learn more.

Represents a message delta i.e. any changed fields on a message during streaming.

The delta containing the fields that have changed on the Message.

The identifier of the message, which can be referenced in API endpoints.

The object type, which is always thread.message.delta.

Represents a run step delta i.e. any changed fields on a run step during streaming.

The delta containing the fields that have changed on the run step.

The identifier of the run step, which can be referenced in API endpoints.

The object type, which is always thread.run.step.delta.

Represents an event emitted when streaming a Run.

Each event in a server-sent events stream has an event and data property:

We emit events whenever a new object is created, transitions to a new state, or is being streamed in parts (deltas). For example, we emit thread.run.created when a new run is created, thread.run.completed when a run completes, and so on. When an Assistant chooses to create a message during a run, we emit a thread.message.created event, a thread.message.in_progress event, many thread.message.delta events, and finally a thread.message.completed event.

We may add additional events over time, so we recommend handling unknown events gracefully in your code. See the Assistants API quickstart to learn how to integrate the Assistants API with streaming.

Occurs when a stream ends.

Occurs when an error occurs. This can happen due to an internal server error or a timeout.

Occurs when a new thread is created.

Occurs when a message is completed.

Occurs when a message is created.

data is a message delta

Occurs when parts of a Message are being streamed.

Occurs when a message moves to an in_progress state.

Occurs when a message ends before it is completed.

Occurs when a run is cancelled.

Occurs when a run moves to a cancelling status.

Occurs when a run is completed.

Occurs when a new run is created.

Occurs when a run expires.

Occurs when a run fails.

Occurs when a run moves to an in_progress status.

Occurs when a run ends with status incomplete.

Occurs when a run moves to a queued status.

Occurs when a run moves to a requires_action status.

Occurs when a run step is cancelled.

Occurs when a run step is completed.

Occurs when a run step is created.

data is a run step delta

Occurs when parts of a run step are being streamed.

Occurs when a run step expires.

Occurs when a run step fails.

Occurs when a run step moves to an in_progress state.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
{
  "id": "msg_123",
  "object": "thread.message.delta",
  "delta": {
    "content": [
      {
        "index": 0,
        "type": "text",
        "text": { "value": "Hello", "annotations": [] }
      }
    ]
  }
}
```

Example 2 (json):
```json
1
2
3
4
5
6
7
8
9
10
11
12
13
{
  "id": "msg_123",
  "object": "thread.message.delta",
  "delta": {
    "content": [
      {
        "index": 0,
        "type": "text",
        "text": { "value": "Hello", "annotations": [] }
      }
    ]
  }
}
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
```

Example 4 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
{
  "id": "step_123",
  "object": "thread.run.step.delta",
  "delta": {
    "step_details": {
      "type": "tool_calls",
      "tool_calls": [
        {
          "index": 0,
          "id": "call_123",
          "type": "code_interpreter",
          "code_interpreter": { "input": "", "outputs": [] }
        }
      ]
    }
  }
}
```

---

## Assistants migration guide

**URL:** https://platform.openai.com/docs/assistants/whats-new

**Contents:**
- Assistants migration guide
  - What's changed?
- From assistants to prompts
  - Why this is helpful
  - Practical migration steps
- From threads to conversations
  - Request example
  - Response example
- From runs to responses
  - Request example

We're moving from the Assistants API to the new Responses API for a simpler and more flexible mental model.

Responses are simpler—send input items and get output items back. With the Responses API, you also get better performance and new features like deep research, MCP, and computer use. This change also lets you manage conversations instead of passing back previous_response_id.

Assistants were persistent API objects that bundled model choice, instructions, and tool declarations—created and managed entirely through the API. Their replacement, prompts, can only be created in the dashboard, where you can version them as you develop your product.

Think of a prompt as a versioned behavioral profile to plug into either Responses or Realtime API.

A thread was a collection of messages stored server-side. Threads could only store messages. Conversations store items, which can include messages, tool calls, tool outputs, and other data.

Runs were asynchronous processes that executed against threads. See the example below. Responses are simpler: provide a set of input items to execute, and get a list of output items back.

Responses are designed to be used alone, but you can also use them with prompt and conversation objects for storing context and configuration.

Follow the migration steps below to move from the Assistants API to the Responses API, without losing any feature support.

This will create a prompt object out of each existing assistant object.

We will not provide an automated tool for migrating Threads to Conversations. Instead, we recommend migrating new user threads onto conversations and backfilling old ones as necessary.

Here's an example for how you might backfill a thread:

Here’s a few simple examples of integrations using both the Assistants API and the Responses API so you can see how they compare.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
thread = openai.beta.threads.create(
  messages=[{"role": "user", "content": "what are the 5 Ds of dodgeball?"}],
  metadata={"user_id": "peter_le_fleur"},
)
```

Example 2 (python):
```python
1
2
3
4
thread = openai.beta.threads.create(
  messages=[{"role": "user", "content": "what are the 5 Ds of dodgeball?"}],
  metadata={"user_id": "peter_le_fleur"},
)
```

Example 3 (unknown):
```unknown
1
2
3
4
conversation = openai.conversations.create(
  items=[{"role": "user", "content": "what are the 5 Ds of dodgeball?"}],
  metadata={"user_id": "peter_le_fleur"},
)
```

Example 4 (python):
```python
1
2
3
4
conversation = openai.conversations.create(
  items=[{"role": "user", "content": "what are the 5 Ds of dodgeball?"}],
  metadata={"user_id": "peter_le_fleur"},
)
```

---
