# Openai-Api - Other

**Pages:** 37

---

## Realtime API with WebRTC

**URL:** https://platform.openai.com/docs/guides/realtime-webrtc

**Contents:**
- Realtime API with WebRTC
- Overview
  - Connecting using the unified interface
    - Creating a session via the unified interface
    - Connecting to the server
  - Connecting using an ephemeral token
    - Creating an ephemeral token
    - Connecting to the server
- Sending and receiving events

WebRTC is a powerful set of standard interfaces for building real-time applications. The OpenAI Realtime API supports connecting to realtime models through a WebRTC peer connection.

For browser-based speech-to-speech voice applications, we recommend starting with the Agents SDK for TypeScript, which provides higher-level helpers and APIs for managing Realtime sessions. The WebRTC interface is powerful and flexible, but lower level than the Agents SDK.

When connecting to a Realtime model from the client (like a web browser or mobile device), we recommend using WebRTC rather than WebSockets for more consistent performance.

For more guidance on building user interfaces on top of WebRTC, refer to the docs on MDN.

The Realtime API supports two mechanisms for connecting to the Realtime API from the browser, either using ephemeral API keys (generated via the OpenAI REST API), or via the new unified interface. Generally, using the unified interface is simpler, but puts your application server in the critical path for session initialization.

The process for initializing a WebRTC connection using the unified interface is as follows (assuming a web browser client):

To create a realtime API session via the unified interface, you will need to build a small server-side application (or integrate with an existing one) to make an request to /v1/realtime/calls. You will use a standard API key to authenticate this request on your backend server.

Below is an example of a simple Node.js express server which creates a realtime API session:

In the browser, you can use standard WebRTC APIs to connect to the Realtime API via your application server. The client directly POSTs its SDP data to your server.

The process for initializing a WebRTC connection using an ephemeral API key is as follows (assuming a web browser client):

To create an ephemeral token to use on the client-side, you will need to build a small server-side application (or integrate with an existing one) to make an OpenAI REST API request for an ephemeral key. You will use a standard API key to authenticate this request on your backend server.

Below is an example of a simple Node.js express server which mints an ephemeral API key using the REST API:

You can create a server endpoint like this one on any platform that can send and receive HTTP requests. Just ensure that you only use standard OpenAI API keys on the server, not in the browser.

In the browser, you can use standard WebRTC APIs to connect to the Realtime API with an ephemeral token. The client first fetches a token from your server endpoint, and then POSTs its SDP data (with the ephemeral token) to the Realtime API.

Realtime API sessions are managed using a combination of client-sent events emitted by you as the developer, and server-sent events created by the Realtime API to indicate session lifecycle events.

When connecting to a Realtime model via WebRTC, you don't have to handle audio events from the model in the same granular way you must with WebSockets. The WebRTC peer connection object, if configured as above, will do all that work for you.

To send and receive other client and server events, you can use the WebRTC peer connection's data channel.

To learn more about managing Realtime conversations, refer to the Realtime conversations guide.

Check out the WebRTC Realtime API in this light weight example app.

**Examples:**

Example 1 (python):
```python
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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
import express from "express";

const app = express();

// Parse raw SDP payloads posted from the browser
app.use(express.text({ type: ["application/sdp", "text/plain"] }));

const sessionConfig = JSON.stringify({
    type: "realtime",
    model: "gpt-realtime",
    audio: { output: { voice: "marin" } }
});

// An endpoint which creates a Realtime API session.
app.post("/session", async (req, res) => {
    const fd = new FormData();
    fd.set("sdp", req.body);
    fd.set("session", sessionConfig);

    try {
        const r = await fetch("https://api.openai.com/v1/realtime/calls", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
            },
            body: fd,
        });
        // Send back the SDP we received from the OpenAI REST API
        const sdp = await r.text();
        res.send(sdp);
    } catch (error) {
        console.error("Token generation error:", error);
        res.status(500).json({ error: "Failed to generate token" });
    }
});

app.listen(3000);
```

Example 2 (javascript):
```javascript
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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
import express from "express";

const app = express();

// Parse raw SDP payloads posted from the browser
app.use(express.text({ type: ["application/sdp", "text/plain"] }));

const sessionConfig = JSON.stringify({
    type: "realtime",
    model: "gpt-realtime",
    audio: { output: { voice: "marin" } }
});

// An endpoint which creates a Realtime API session.
app.post("/session", async (req, res) => {
    const fd = new FormData();
    fd.set("sdp", req.body);
    fd.set("session", sessionConfig);

    try {
        const r = await fetch("https://api.openai.com/v1/realtime/calls", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
            },
            body: fd,
        });
        // Send back the SDP we received from the OpenAI REST API
        const sdp = await r.text();
        res.send(sdp);
    } catch (error) {
        console.error("Token generation error:", error);
        res.status(500).json({ error: "Failed to generate token" });
    }
});

app.listen(3000);
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
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
```

Example 4 (javascript):
```javascript
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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
// Create a peer connection
const pc = new RTCPeerConnection();

// Set up to play remote audio from the model
audioElement.current = document.createElement("audio");
audioElement.current.autoplay = true;
pc.ontrack = (e) => (audioElement.current.srcObject = e.streams[0]);

// Add local audio track for microphone input in the browser
const ms = await navigator.mediaDevices.getUserMedia({
    audio: true,
});
pc.addTrack(ms.getTracks()[0]);

// Set up data channel for sending and receiving events
const dc = pc.createDataChannel("oai-events");

// Start the session using the Session Description Protocol (SDP)
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

const sdpResponse = await fetch("/session", {
    method: "POST",
    body: offer.sdp,
    headers: {
        "Content-Type": "application/sdp",
    },
});

const answer = {
    type: "answer",
    sdp: await sdpResponse.text(),
};
await pc.setRemoteDescription(answer);
```

---

## Data controls in the OpenAI platform

**URL:** https://platform.openai.com/docs/guides/your-data

**Contents:**
- Data controls in the OpenAI platform
- Types of data stored with the OpenAI API
- Data retention controls for abuse monitoring
  - Modified Abuse Monitoring
  - Zero Data Retention
  - Configuring data retention controls
  - Storage requirements and retention controls per endpoint
    - /v1/chat/completions
    - /v1/responses
    - /v1/assistants, /v1/threads, and /v1/vector_stores

Understand how OpenAI uses your data, and how you can control it.

Your data is your data. As of March 1, 2023, data sent to the OpenAI API is not used to train or improve OpenAI models (unless you explicitly opt in to share data with us).

When using the OpenAI API, data may be stored as:

Abuse monitoring logs may contain certain customer content, such as prompts and responses, as well as metadata derived from that customer content, such as classifier outputs. By default, abuse monitoring logs are generated for all API feature usage and retained for up to 30 days, unless we are legally required to retain the logs for longer.

Eligible customers may have their customer content excluded from these abuse monitoring logs by getting approved for the Zero Data Retention or Modified Abuse Monitoring controls. Currently, these controls are subject to prior approval by OpenAI and acceptance of additional requirements. Approved customers may select between Modified Abuse Monitoring or Zero Data Retention for their API Organization or project.

Customers who enable Modified Abuse Monitoring or Zero Data Retention are responsible for ensuring their users abide by OpenAI's policies for safe and responsible use of AI and complying with any moderation and reporting requirements under applicable law.

Get in touch with our sales team to learn more about these offerings and inquire about eligibility.

Modified Abuse Monitoring excludes customer content (other than image and file inputs in rare cases, as described below) from abuse monitoring logs across all API endpoints, while still allowing the customer to take advantage of the full capabilities of the OpenAI platform.

Zero Data Retention excludes customer content from abuse monitoring logs, in the same way as Modified Abuse Monitoring.

Additionally, Zero Data Retention changes some endpoint behavior: the store parameter for /v1/responses and v1/chat/completions will always be treated as false, even if the request attempts to set the value to true.

Besides those specific behavior changes, the endpoints and capabilities listed as No for Zero Data Retention Eligible in the table below may still store application state, even if Zero Data Retention is enabled.

Once your organization has been approved for data retention controls, you'll see a Data Retention tab within Settings → Organization → Data controls. From that tab, you can configure data retention controls at both the organization and project level.

The table below indicates when application state is stored for each endpoint. Zero Data Retention eligible endpoints will not store any data. Zero Data Retention ineligible endpoints or capabilities may store application state when used, even if you have Zero Data Retention enabled.

Images and files may be uploaded as inputs to /v1/responses (including when using the Computer Use tool), /v1/chat/completions, and /v1/images. Image and file inputs are scanned for CSAM content upon submission. If the classifier detects potential CSAM content, the image will be retained for manual review, even if Zero Data Retention or Modified Abuse Monitoring is enabled.

Web Search is ZDR eligible, but Web Search is not HIPAA eligible and is not covered by a BAA.

Data residency controls are a project configuration option that allow you to configure the location of infrastructure OpenAI uses to provide services.

Contact our sales team to see if you're eligible for using data residency controls.

When data residency is enabled on your account, you can set a region for new projects you create in your account from the available regions listed below. If you use the supported endpoints, models, and snapshots listed below, your customer content (as defined in your services agreement) for that project will be stored at rest in the selected region to the extent the endpoint requires data persistence to function (such as /v1/batches).

If you select a region that supports regional processing, as specifically identified below, the services will perform inference for your Customer Content in the selected region as well.

Data residency does not apply to system data, which may be processed and stored outside the selected region. System data means account data, metadata, and usage data that do not contain Customer Content, which are collected by the services and used to manage and operate the services, such as account information or profiles of end users that directly access the services (e.g., your personnel), analytics, usage statistics, billing information, support requests, and structured output schema.

Data residency does not apply to: (a) any transmission or storage of Customer Content outside of the selected region caused by the location of an End User or Customer's infrastructure when accessing the services; (b) products, services, or content offered by parties other than OpenAI through the Services; or (c) any data other than Customer Content, such as system data.

If your selected Region does not support regional processing, as identified below, OpenAI may also process and temporarily store Customer Content outside of the Region to deliver the services.

To use data residency with any region other than the United States, you must be approved for abuse monitoring controls, and execute a Zero Data Retention amendment.

Selecting the United Arab Emirates region requires additional approval. Contact sales for assistance.

Data residency is configured per-project within your API Organization.

To configure data residency for regional storage, select the appropriate region from the dropdown when creating a new project.

For requests to projects with data residency configured, add the domain prefix as defined in the table below to each request. For regions where the prefix is marked as optional, including the prefix may help improve response latency for your requests.

The following models and API services are eligible for data residency today for the regions specified below.

Table 1: Regional data residency capabilities

* Image support in these regions requires approval for enhanced Zero Data Retention or enhanced Modified Abuse Monitoring.

Table 2: API endpoint and tool support

Tracing is not currently EU data residency compliant for /v1/realtime.

text-moderation-latest is only supported for US/EU.

Enterprise Key Management (EKM) allows you to encrypt your customer content at OpenAI using keys managed by your own external Key Management System (KMS).

Once configured, EKM applies to any application state created during your use of the platform. See the EKM help center article for more information about how EKM works, and how to integrate with your KMS provider.

OpenAI supports Bring Your Own Key (BYOK) encryption with external accounts in AWS KMS, Google Cloud (GCP), and Azure Key Vault. If your organization leverages a different key management services, those keys need to be synced to one of the supported Cloud KMSs for use with OpenAI.

EKM does not support the following products. An attempt to use these endpoints in a project with EKM enabled will return an error.

---

## Graders

**URL:** https://platform.openai.com/docs/guides/graders

**Contents:**
- Graders
- Overview
- Templating
  - Item namespace
  - Sample namespace
- String check grader
- Text similarity grader
- Model graders
  - Score model graders
    - Score model grader outputs

Graders are a way to evaluate your model's performance against reference answers. Our graders API is a way to test your graders, experiment with results, and improve your fine-tuning or evaluation framework to get the results you want.

Graders let you compare reference answers to the corresponding model-generated answer and return a grade in the range from 0 to 1. It's sometimes helpful to give the model partial credit for an answer, rather than a binary 0 or 1.

Graders are specified in JSON format, and there are several types:

In reinforcement fine-tuning, you can nest and combine graders by using multigraders.

Use this guide to learn about each grader type and see starter examples. To build a grader and get started with reinforcement fine-tuning, see the RFT guide. Or to get started with evals, see the Evals guide.

The inputs to certain graders use a templating syntax to grade multiple examples with the same configuration. Any string with {{ }} double curly braces will be substituted with the variable value.

Each input inside the {{}} must include a namespace and a variable with the following format {{ namespace.variable }}. The only supported namespaces are item and sample.

All nested variables can be accessed with JSON path like syntax.

The item namespace will be populated with variables from the input data source for evals, and from each dataset item for fine-tuning. For example, if a row contains the following

This can be used within the grader as {{ item.reference_answer }}.

The sample namespace will be populated with variables from the model sampling step during evals or during the fine-tuning step. The following variables are included

For example, to access the model output content as a string, {{ sample.output_text }} can be used within the grader.

When training a model to improve tool-calling behavior, you will need to write your grader to operate over the sample.output_tools variable. The contents of this variable will be the same as the contents of the response.choices[0].message.tool_calls (see function calling docs).

A common way of grading tool calls is to use two graders, one that checks the name of the tool that is called and another that checks the arguments of the called function. An example of a grader that does this is shown below:

This is a multi grader that combined two simple string_check graders, the first checks the name of the tool called via the sample.output_tools[0].function.name variable, and the second checks the arguments of the called function via the sample.output_tools[0].function.arguments variable. The calculate_output field is used to combine the two scores into a single score.

The arguments grader is prone to under-rewarding the model if the function arguments are subtly incorrect, like if 1 is submitted instead of the floating point 1.0, or if a state name is given as an abbreviation instead of spelling it out. To avoid this, you can use a text_similarity grader instead of a string_check grader, or a score_model grader to have a LLM check for semantic similarity.

Use these simple string operations to return a 0 or 1. String check graders are good for scoring straightforward pass or fail answers—for example, the correct name of a city, a yes or no answer, or an answer containing or starting with the correct information.

Operations supported for string-check-grader are:

Use text similarity graders when to evaluate how close the model-generated output is to the reference, scored with various evaluation frameworks.

This is useful for open-ended text responses. For example, if your dataset contains reference answers from experts in paragraph form, it's helpful to see how close your model-generated answer is to that content, in numerical form.

Operations supported for string-similarity-grader are:

In general, using a model grader means prompting a separate model to grade the outputs of the model you're fine-tuning. Your two models work together to do reinforcement fine-tuning. The grader model evaluates the training model.

A score model grader will take the input and return a numeric score based on the prompt within the given range.

Where each message is of the following form:

To use a score model grader, the input is a list of chat messages, each containing a role and content. The output of the grader will be truncated to the given range, and default to 0 for all non-numeric outputs. Within each message, the same templating can be used as with other common graders to reference the ground truth or model sample.

Here’s a full runnable code sample:

Under the hood, the score_model grader will query the requested model with the provided prompt and sampling parameters and will request a response in a specific response format. The response format that is used is provided below

Where each reasoning step is of the form

This format queries the model not just for the numeric result (the reward value for the query), but also provides the model some space to think through the reasoning behind the score. When you are writing your grader prompt, it may be useful to refer to these two fields by name explicitly (e.g. "include reasoning about the type of chemical bonds present in the molecule in the conclusion of your reasoning step", or "return a value of -1.0 in the result field if the inputs do not satisfy condition X").

Writing grader prompts is an iterative process. The best way to iterate on a model grader prompt is to create a model grader eval. To do this, you need:

Then you can automatically evaluate how effectively the model grader distinguishes answers of different quality levels. Over time, add edge cases into your model grader eval as you discover and patch them with changes to the prompt.

For example, say you know from your human experts which answers are best:

Verify that the model grader's answers match that:

Models being trained sometimes learn to exploit weaknesses in model graders, also known as “grader hacking” or “reward hacking." You can detect this by checking the model's performance across model grader evals and expert human evals. A model that's hacked the grader will score highly on model grader evals but score poorly on expert human evaluations. Over time, we intend to improve observability in the API to make it easier to detect this during training.

This grader allows you to execute arbitrary python code to grade the model output. The grader expects a grade function to be present that takes in two arguments and outputs a float value. Any other result (exception, invalid float value, etc.) will be marked as invalid and return a 0 grade.

The python source code must contain a grade function that takes in exactly two arguments and returns a float value as a grade.

The first argument supplied to the grading function will be a dictionary populated with the model’s output during training for you to grade. output_json will only be populated if the output uses response_format.

The second argument supplied is a dictionary populated with input grading context. For evals, this will include keys from the data source. For fine-tuning this will include keys from each training data row.

Here's a working example:

Tip: If you don't want to manually put your grading function in a string, you can also load it from a Python file using importlib and inspect. For example, if your grader function is in a file named grader.py, you can do:

This will automatically use the entire source code of your grader.py file as the grader which can be helpful for longer graders.

The following third-party packages are available at execution time for the image tag 2025-05-08

Additionally the following nltk corpora are available:

Currently, this grader is only used for Reinforcement fine-tuning

A multigrader object combines the output of multiple graders to produce a single score. Multigraders work by computing grades over the fields of other grader objects and turning those sub-grades into an overall grade. This is useful when a correct answer depends on multiple things being true—for example, that the text is similar and that the answer contains a specific string.

As an example, say you wanted the model to output JSON with the following two fields:

You'd want your grader to compare the two fields and then take the average between them.

You can do this by combining multiple graders into an object grader, and then defining a formula to calculate the output score based on each field:

In this example, it’s important for the model to get the email exactly right (string_check returns either 0 or 1) but we tolerate some misspellings on the name (text_similarity returns range from 0 to 1). Samples that get the email wrong will score between 0-0.5, and samples that get the email right will score between 0.5-1.0.

You cannot create a multigrader with a nested multigrader inside.

The calculate output field will have the keys of the input graders as possible variables and the following features are supported:

Designing and creating graders is an iterative process. Start small, experiment, and continue to make changes to get better results.

To get the most value from your graders, use these design principles:

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
{
    "reference_answer": "..."
}
```

Example 2 (json):
```json
1
2
3
{
    "reference_answer": "..."
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
14
15
16
17
18
19
20
{
    "type": "multi",
    "graders": {
        "function_name": {
            "name": "function_name",
            "type": "string_check",
            "input": "get_acceptors",
            "reference": "{{sample.output_tools[0].function.name}}",
            "operation": "eq",
        },
        "arguments": {
            "name": "arguments",
            "type": "string_check",
            "input": "{\"smiles\": \"{{item.smiles}}\"}",
            "reference": "{{sample.output_tools[0].function.arguments}}",
            "operation": "eq",
        },
    },
    "calculate_output": "0.5 * function_name + 0.5 * arguments",
}
```

Example 4 (json):
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
14
15
16
17
18
19
20
{
    "type": "multi",
    "graders": {
        "function_name": {
            "name": "function_name",
            "type": "string_check",
            "input": "get_acceptors",
            "reference": "{{sample.output_tools[0].function.name}}",
            "operation": "eq",
        },
        "arguments": {
            "name": "arguments",
            "type": "string_check",
            "input": "{\"smiles\": \"{{item.smiles}}\"}",
            "reference": "{{sample.output_tools[0].function.arguments}}",
            "operation": "eq",
        },
    },
    "calculate_output": "0.5 * function_name + 0.5 * arguments",
}
```

---

## Code generation

**URL:** https://platform.openai.com/docs/guides/code-generation

**Contents:**
- Code generation
- Get started
- Use Codex
- Integrate with coding models
- Next steps

Writing, reviewing, editing, and answering questions about code is one of the primary use cases for OpenAI models today. This guide walks through your options for code generation.

Codex is OpenAI's series of AI coding tools that help developers move faster by delegating tasks to powerful cloud and local coding agents. Interact with Codex in a variety of interfaces: in your IDE, through the CLI, on web and mobile sites, or in your CI/CD pipelines with the SDK. Codex is the best way to get agentic software engineering on your projects.

Codex models are LLMs specifically trained at coding tasks. They power Codex, and you can use them to create coding-specific applications. For example, let your end users generate code.

Codex has an interface in the browser, similar to ChatGPT, where you can kick off coding tasks that run in the cloud. Visit chatgpt.com/codex to use it.

Codex also has an IDE extension, CLI, and SDK to help you create coding tasks in whichever environment makes the most sense for you. For example, the SDK is useful for using Codex in CI/CD pipelines. The CLI, on the other hand, runs locally from your terminal and can read, modify, and run code on your machine.

See the Codex docs for quickstarts, reference, pricing, and more information.

OpenAI has several models trained specifically to work with code. GPT-5.1-Codex-Max is our best agentic coding model. That said, many OpenAI models excel at writing and editing code as well as other tasks. Use a Codex model if you only want it for coding-related work.

Here's an example that calls GPT-5.1-Codex-Max, the model that powers Codex:

Learn more about GPT-5.1-Codex-Max in the blog post. Read the GPT-5.1-Codex-Max prompting guide to start building with it.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from "openai";
const openai = new OpenAI();

const result = await openai.responses.create({
  model: "gpt-5.1-codex-max",
  input: "Find the null pointer exception: ...your code here...",
  reasoning: { effort: "high" },
});

console.log(result.output_text);
```

Example 2 (javascript):
```javascript
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
import OpenAI from "openai";
const openai = new OpenAI();

const result = await openai.responses.create({
  model: "gpt-5.1-codex-max",
  input: "Find the null pointer exception: ...your code here...",
  reasoning: { effort: "high" },
});

console.log(result.output_text);
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
```

Example 4 (python):
```python
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
from openai import OpenAI
client = OpenAI()

result = client.responses.create(
    model="gpt-5.1-codex-max",
    input="Find the null pointer exception: ...your code here...",
    reasoning={ "effort": "high" },
)

print(result.output_text)
```

---

## Deprecations

**URL:** https://platform.openai.com/docs/deprecations

**Contents:**
- Deprecations
- Overview
- Deprecation vs. legacy
- Deprecation history
  - 2025-11-18: chatgpt-4o-latest snapshot
  - 2025-11-17: codex-mini-latest model snapshot
  - 2025-11-14: DALL·E model snapshots
  - 2025-09-26: Legacy GPT model snapshots
  - 2025-09-15: Realtime API Beta
  - 2025-08-20: Assistants API

As we launch safer and more capable models, we regularly retire older models. Software relying on OpenAI models may need occasional updates to keep working. Impacted customers will always be notified by email and in our documentation along with blog posts for larger changes.

This page lists all API deprecations, along with recommended replacements.

We use the term "deprecation" to refer to the process of retiring a model or endpoint. When we announce that a model or endpoint is being deprecated, it immediately becomes deprecated. All deprecated models and endpoints will also have a shut down date. At the time of the shut down, the model or endpoint will no longer be accessible.

We use the terms "sunset" and "shut down" interchangeably to mean a model or endpoint is no longer accessible.

We use the term "legacy" to refer to models and endpoints that no longer receive updates. We tag endpoints and models as legacy to signal to developers where we're moving as a platform and that they should likely migrate to newer models or endpoints. You can expect that a legacy model or endpoint will be deprecated at some point in the future.

All deprecations are listed below, with the most recent announcements at the top.

On November 18th, 2025, we notified developers using chatgpt-4o-latest model snapshot of its deprecation and removal from the API on February 17, 2026.

On November 17th, 2025, we notified developers using codex-mini-latest model of its deprecation and removal from the API on January 16, 2026.

On November 14th, 2025, we notified developers using DALL·E model snapshots of their deprecation and removal from the API on May 12, 2026.

To improve reliability and make it easier for developers to choose the right models, we are deprecating a set of older OpenAI models with declining usage over the next six to twelve months. Access to these models will be shut down on the dates below.

*For tasks that are especially latency sensitive and don't require reasoning

The Realtime API Beta will be deprecated and removed from the API on February 27, 2026.

There are a few key differences between the interfaces in the Realtime beta API and the recently released GA API. See the migration guide to learn more about how to migrate your current beta integration.

On August 26th, 2025, we notified developers using the Assistants API of its deprecation and removal from the API one year later, on August 26, 2026.

When we released the Responses API in March 2025, we announced plans to bring all Assistants API features to the easier to use Responses API, with a sunset date in 2026.

See the Assistants to Conversations migration guide to learn more about how to migrate your current integration to the Responses API and Conversations API.

In September, 2025, we notified developers using gpt-4o-realtime-preview models of their deprecation and removal from the API in six months.

On June 10th, 2025, we notified developers using gpt-4o-realtime-preview-2024-10-01 of its deprecation and removal from the API in three months.

On June 10th, 2025, we notified developers using gpt-4o-audio-preview-2024-10-01 of its deprecation and removal from the API in three months.

On April 28th, 2025, we notified developers using text-moderation of its deprecation and removal from the API in six months.

On April 28th, 2025, we notified developers using o1-preview and o1-mini of their deprecations and removal from the API in three months and six months respectively.

On April 14th, 2025, we notified developers that the gpt-4.5-preview model is deprecated and will be removed from the API in the coming months.

In April 2024 when we released the v2 beta version of the Assistants API, we announced that access to the v1 beta would be shut off by the end of 2024. Access to the v1 beta will be discontinued on December 18, 2024.

See the Assistants API v2 beta migration guide to learn more about how to migrate your tool usage to the latest version of the Assistants API.

On August 29th, 2024, we notified developers fine-tuning babbage-002 and davinci-002 that new fine-tuning training runs on these models will no longer be supported starting October 28, 2024.

Fine-tuned models created from these base models are not affected by this deprecation, but you will no longer be able to create new fine-tuned versions with these models.

On June 6th, 2024, we notified developers using gpt-4-32k and gpt-4-vision-preview of their upcoming deprecations in one year and six months respectively. As of June 17, 2024, only existing users of these models will be able to continue using them.

On November 6th, 2023, we announced the release of an updated GPT-3.5-Turbo model (which now comes by default with 16k context) along with deprecation of gpt-3.5-turbo-0613 and gpt-3.5-turbo-16k-0613. As of June 17, 2024, only existing users of these models will be able to continue using them.

Fine-tuned models created from these base models are not affected by this deprecation, but you will no longer be able to create new fine-tuned versions with these models.

On August 22nd, 2023, we announced the new fine-tuning API (/v1/fine_tuning/jobs) and that the original /v1/fine-tunes API along with legacy models (including those fine-tuned with the /v1/fine-tunes API) will be shut down on January 04, 2024. This means that models fine-tuned using the /v1/fine-tunes API will no longer be accessible and you would have to fine-tune new models with the updated endpoint and associated base models.

On July 06, 2023, we announced the upcoming retirements of older GPT-3 and GPT-3.5 models served via the completions endpoint. We also announced the upcoming retirement of our first-generation text embedding models. They will be shut down on January 04, 2024.

Pricing for the replacement gpt-3.5-turbo-instruct model can be found on the pricing page.

Pricing for the replacement babbage-002 and davinci-002 models can be found on the pricing page.

On June 13, 2023, we announced new chat model versions in the Function calling and other API updates blog post. The three original versions will be retired in June 2024 at the earliest. As of January 10, 2024, only existing users of these models will be able to continue using them.

---

## Streaming API responses

**URL:** https://platform.openai.com/docs/guides/streaming-responses

**Contents:**
- Streaming API responses
- Enable streaming
- Read the responses
- Advanced use cases
- Moderation risk

By default, when you make a request to the OpenAI API, we generate the model's entire output before sending it back in a single HTTP response. When generating long outputs, waiting for a response can take time. Streaming responses lets you start printing or processing the beginning of the model's output while it continues generating the full response.

To start streaming responses, set stream=True in your request to the Responses endpoint:

The Responses API uses semantic events for streaming. Each event is typed with a predefined schema, so you can listen for events you care about.

For a full list of event types, see the API reference for streaming. Here are a few examples:

If you're using our SDK, every event is a typed instance. You can also identity individual events using the type property of the event.

Some key lifecycle events are emitted only once, while others are emitted multiple times as the response is generated. Common events to listen for when streaming text are:

For a full list of events you can listen for, see the API reference for streaming.

For more advanced use cases, like streaming tool calls, check out the following dedicated guides:

Note that streaming the model's output in a production application makes it more difficult to moderate the content of the completions, as partial completions may be more difficult to evaluate. This may have implications for approved usage.

**Examples:**

Example 1 (python):
```python
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
import { OpenAI } from "openai";
const client = new OpenAI();

const stream = await client.responses.create({
    model: "gpt-5",
    input: [
        {
            role: "user",
            content: "Say 'double bubble bath' ten times fast.",
        },
    ],
    stream: true,
});

for await (const event of stream) {
    console.log(event);
}
```

Example 2 (javascript):
```javascript
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
import { OpenAI } from "openai";
const client = new OpenAI();

const stream = await client.responses.create({
    model: "gpt-5",
    input: [
        {
            role: "user",
            content: "Say 'double bubble bath' ten times fast.",
        },
    ],
    stream: true,
});

for await (const event of stream) {
    console.log(event);
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
14
15
16
17
```

Example 4 (python):
```python
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
from openai import OpenAI
client = OpenAI()

stream = client.responses.create(
    model="gpt-5",
    input=[
        {
            "role": "user",
            "content": "Say 'double bubble bath' ten times fast.",
        },
    ],
    stream=True,
)

for event in stream:
    print(event)
```

---

## Video generation with Sora

**URL:** https://platform.openai.com/docs/guides/video-generation?gallery=open&galleryItem=fox-walk

**Contents:**
- Video generation with Sora
- Overview
- Models
  - Sora 2
  - Sora 2 Pro
- Generate a video
  - Start a render job
  - Guardrails and restrictions
  - Effective prompting
  - Monitor progress

Sora is OpenAI’s newest frontier in generative media – a state-of-the-art video model capable of creating richly detailed, dynamic clips with audio from natural language or images. Built on years of research into multimodal diffusion and trained on diverse visual data, Sora brings a deep understanding of 3D space, motion, and scene continuity to text-to-video generation.

The Video API (in preview) exposes these capabilities to developers for the first time, enabling programmatic creation, extension, and remixing of videos. It provides five endpoints, each with distinct capabilities:

The second generation Sora model comes in two variants, each tailored for different use cases.

sora-2 is designed for speed and flexibility. It’s ideal for the exploration phase, when you’re experimenting with tone, structure, or visual style and need quick feedback rather than perfect fidelity.

It generates good quality results quickly, making it well suited for rapid iteration, concepting, and rough cuts. sora-2 is often more than sufficient for social media content, prototypes, and scenarios where turnaround time matters more than ultra-high fidelity.

sora-2-pro produces higher quality results. It’s the better choice when you need production-quality output.

sora-2-pro takes longer to render and is more expensive to run, but it produces more polished, stable results. It’s best for high-resolution cinematic footage, marketing assets, and any situation where visual precision is critical.

Generating a video is an asynchronous process:

When you call the POST /videos endpoint, the API returns a job object with a job id and an initial status.

You can either poll the GET /videos/{video_id} endpoint until the status transitions to completed, or – for a more efficient approach – use webhooks (see the webhooks section below) to be notified automatically when the job finishes.

Once the job has reached the completed state you can fetch the final MP4 file with GET /videos/{video_id}/content.

Start by calling POST /videos with a text prompt and the required parameters. The prompt defines the creative look and feel – subjects, camera, lighting, and motion – while parameters like size and seconds control the video's resolution and length.

The response is a JSON object with a unique id and an initial status such as queued or in_progress. This means the render job has started.

The API enforces several content restrictions:

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

For best results, describe shot type, subject, action, setting, and lighting. For example:

This level of specificity helps the model produce consistent results without inventing unwanted details. For more advanced prompting techniques, please refer to our dedicated Sora 2 prompting guide.

Video generation takes time. Depending on model, API load and resolution, a single render may take several minutes.

To manage this efficiently, you can poll the API to request status updates or you can get notified via a webhook.

Call GET /videos/{video_id} with the id returned from the create call. The response shows the job’s current status, progress percentage (if available), and any errors.

Typical states are queued, in_progress, completed, and failed. Poll at a reasonable interval (for example, every 10–20 seconds), use exponential backoff if necessary, and provide feedback to users that the job is still in progress.

Instead of polling job status repeatedly with GET, register a webhook to be notified automatically when a video generation completes or fails.

Webhooks can be configured in your webhook settings page. When a job finishes, the API emits one of two event types: video.completed and video.failed. Each event includes the ID of the job that triggered it.

Example webhook payload:

Once the job reaches status completed, fetch the MP4 with GET /videos/{video_id}/content. This endpoint streams the binary video data and returns standard content headers, so you can either save the file directly to disk or pipe it to cloud storage.

You now have the final video file ready for playback, editing, or distribution. Download URLs are valid for a maximum of 1 hour after generation. If you need long-term storage, copy the file to your own storage system promptly.

For each completed video, you can also download a thumbnail and a spritesheet. These are lightweight assets useful for previews, scrubbers, or catalog displays. Use the variant query parameter to specify what you want to download. The default is variant=video for the MP4.

You can guide a generation with an input image, which acts as the first frame of your video. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment. Include an image file as the input_reference parameter in your POST /videos request. The image must match the target video’s resolution (size).

Supported file formats are image/jpeg, image/png, and image/webp.

Remix lets you take an existing video and make targeted adjustments without regenerating everything from scratch. Provide the remix_video_id of a completed job along with a new prompt that describes the change, and the system reuses the original’s structure, continuity, and composition while applying the modification. This works best when you make a single, well-defined change because smaller, focused edits preserve more of the original fidelity and reduce the risk of introducing artifacts.

Remix is especially valuable for iteration because it lets you refine without discarding what already works. By constraining each remix to one clear adjustment, you keep the visual style, subject consistency, and camera framing stable, while still exploring variations in mood, palette, or staging. This makes it far easier to build polished sequences through small, reliable steps.

Use GET /videos to enumerate your videos. The endpoint supports optional query parameters for pagination and sorting.

Use DELETE /videos/{video_id} to remove videos you no longer need from OpenAI’s storage.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
```

Example 2 (javascript):
```javascript
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
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
```

Example 4 (python):
```python
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
from openai import OpenAI

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

---

## Priority processing

**URL:** https://platform.openai.com/docs/guides/priority-processing

**Contents:**
- Priority processing
- Configuring Priority processing
- Rate limits and ramp rate
- Usage considerations

Priority processing delivers significantly lower and more consistent latency compared to Standard processing while keeping pay-as-you-go flexibility.

Priority processing is ideal for high-value, user-facing applications with regular traffic where latency is paramount. Priority processing should not be used for data processing, evaluations, or other highly erratic traffic.

Requests to the Responses or Completions endpoints can be configured to use Priority processing through either a request parameter, or a Project setting.

To opt-in to Priority processing at the request level, include the service_tier=priority parameter for Completions or Responses.

To opt in at the Project level, navigate to the Settings page, select the General tab under Project, then change the Project Service Tier to Priority. Once configured on the project, requests that don't specify a service_tier will default to Priority. Note that requests for the project will be gradually transitioned to Priority over time.

The service_tier field in the Responses or Completions response objects will contain which service tier was used to process the request.

Priority consumption is treated like Standard for rate‑limit accounting. Use your usual retry and backoff logic. For a given model, the rate limit is shared between Standard and Priority processing.

If your traffic ramps too quickly, some Priority requests may be downgraded to Standard and billed at Standard rates. If the ramp rate limit is exceeded, the response will show service_tier="default". Currently, the ramp rate limit may apply if you’re sending at least 1 million TPM and >50% TPM increase within 15 minutes.

To avoid triggering the ramp rate limit, we recommend:

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
5
curl https://api.openai.com/v1/responses   -H "Authorization: Bearer $OPENAI_API_KEY"   -H "Content-Type: application/json"   -d '{
    "model": "gpt-5",
    "input": "What does 'fit check for my napalm era' mean?",
    "service_tier": "priority"
  }'
```

Example 2 (bash):
```bash
1
2
3
4
5
curl https://api.openai.com/v1/responses   -H "Authorization: Bearer $OPENAI_API_KEY"   -H "Content-Type: application/json"   -d '{
    "model": "gpt-5",
    "input": "What does 'fit check for my napalm era' mean?",
    "service_tier": "priority"
  }'
```

Example 3 (python):
```python
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
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
  model: "gpt-5",
  input: "What does 'fit check for my napalm era' mean?",
  service_tier: "priority"
});

console.log(response);
```

Example 4 (javascript):
```javascript
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
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
  model: "gpt-5",
  input: "What does 'fit check for my napalm era' mean?",
  service_tier: "priority"
});

console.log(response);
```

---

## Trace grading

**URL:** https://platform.openai.com/docs/guides/trace-grading

**Contents:**
- Trace grading
- Get started with traces
- Evaluate traces with runs

Trace grading is the process of assigning structured scores or labels to an agent's trace—the end-to-end log of decisions, tool calls, and reasoning steps—to assess correctness, quality, or adherence to expectations. These annotations help identify where the agent did well or made mistakes, enabling targeted improvements in orchestration or behavior.

Trace evals use those graded traces to systematically evaluate agent performance across many examples, helping to benchmark changes, identify regressions, or validate improvements. Unlike black-box evaluations, trace evals provide more data to better understand why an agent succeeds or fails.

Use both features to track, analyze, and optimize the performance of groups of agents.

Trace grading is a valuable tool for error identification at scale, which is critical for building resilience into your AI applications. Learn more about our recommended process in our cookbook.

Learn more about how you can use evals here.

---

## Agent evals

**URL:** https://platform.openai.com/docs/guides/agent-evals

**Contents:**
- Agent evals
- Next steps

The OpenAI Platform offers a suite of evaluation tools to help you ensure your agents perform consistently and accurately.

For identifying errors at the workflow-level, we recommend our trace grading functionality.

For an easy way to build and iterate on your evals, we recommend exploring Datasets.

If you need advanced features such as evaluation against external models, want to interact with your eval runs via API, or want to run evaluations on a larger scale, consider using Evals instead.

For more inspiration, visit the OpenAI Cookbook, which contains example code and links to third-party resources, or learn more about our tools for evals:

Operate a flywheel of continuous improvement using evaluations.

Evaluate against external models, interact with evals via API, and more.

Use your dataset to automatically improve your prompts.

Operate a flywheel of continuous improvement using evaluations.

---

## Working with evals

**URL:** https://platform.openai.com/docs/guides/evals

**Contents:**
- Working with evals
- Create an eval for a task
- Test a prompt with your eval
  - Uploading test data
  - Creating an eval run
- Analyze the results
- Next steps

Evaluations (often called evals) test model outputs to ensure they meet style and content criteria that you specify. Writing evals to understand how your LLM applications are performing against your expectations, especially when upgrading or trying new models, is an essential component to building reliable applications.

In this guide, we will focus on configuring evals programmatically using the Evals API. If you prefer, you can also configure evals in the OpenAI dashboard.

If you're new to evaluations, or want a more iterative environment to experiment in as you build your eval, consider trying Datasets instead.

Broadly, there are three steps to build and run evals for your LLM application.

This process is somewhat similar to behavior-driven development (BDD), where you begin by specifying how the system should behave before implementing and testing the system. Let's see how we would complete each of the steps above using the Evals API.

Creating an eval begins by describing a task to be done by a model. Let's say that we would like to use a model to classify the contents of IT support tickets into one of three categories: Hardware, Software, or Other.

To implement this use case, you can use either the Chat Completions API or the Responses API. Both examples below combine a developer message with a user message containing the text of a support ticket.

Let's set up an eval to test this behavior via API. An eval needs two key ingredients:

Running this eval will require a test data set that represents the type of data you expect your prompt to work with (more on creating the test data set later in this guide). In our data_source_config parameter, we specify that each item in the data set will conform to a JSON schema with two properties:

Since we will be referencing a sample in our test criteria (the output generated by a model given our prompt), we also set include_sample_schema to true.

In our testing_criteria, we define how we will conclude if the model output satisfies our requirements for each item in the data set. In this case, we just want the model to output one of three category strings based on the input ticket. The string it outputs should exactly match the human-labeled correct_label field in our test data. So in this case, we will want to use a string_check grader to evaluate the output.

In the test configuration, we will introduce template syntax, represented by the {{ and }} brackets below. This is how we will insert dynamic content into the test for this eval.

After creating the eval, it will be assigned a UUID that you will need to address it later when kicking off a run.

Now that we've created an eval that describes the desired behavior of our application, let's test a prompt with a set of test data.

Now that we have defined how we want our app to behave in an eval, let's construct a prompt that reliably generates the correct output for a representative sample of test data.

There are several ways to provide test data for eval runs, but it may be convenient to upload a JSONL file that contains data in the schema we specified when we created our eval. A sample JSONL file that conforms to the schema we set up is below:

This data set contains both test inputs and ground truth labels to compare model outputs against.

Next, let's upload our test data file to the OpenAI platform so we can reference it later. You can upload files in the dashboard here, but it's possible to upload files via API as well. The samples below assume you are running the command in a directory where you saved the sample JSON data above to a file called tickets.jsonl:

When you upload the file, make note of the unique id property in the response payload (also available in the UI if you uploaded via the browser) - we will need to reference that value later:

With our test data in place, let's evaluate a prompt and see how it performs against our test criteria. Via API, we can do this by creating an eval run.

Make sure to replace YOUR_EVAL_ID and YOUR_FILE_ID with the unique IDs of the eval configuration and test data files you created in the steps above.

When we create the run, we set up a prompt using either a Chat Completions messages array or a Responses input. This prompt is used to generate a model response for every line of test data in your data set. We can use the double curly brace syntax to template in the dynamic variable item.ticket_text, which is drawn from the current test data item.

If the eval run is successfully created, you'll receive an API response that looks like this:

Your eval run has now been queued, and it will execute asynchronously as it processes every row in your data set, generating responses for testing with the prompt and model we specified.

To receive updates when a run succeeds, fails, or is canceled, create a webhook endpoint and subscribe to the eval.run.succeeded, eval.run.failed, and eval.run.canceled events. See the webhooks guide for more details.

Depending on the size of your dataset, the eval run may take some time to complete. You can view current status in the dashboard, but you can also fetch the current status of an eval run via API:

You'll need the UUID of both your eval and eval run to fetch its status. When you do, you'll see eval run data that looks like this:

The API response contains granular information about test criteria results, API usage for generating model responses, and a report_url property that takes you to a page in the dashboard where you can explore the results visually.

In our simple test, the model reliably generated the content we wanted for a small test case sample. In reality, you will often have to run your eval with more criteria, different prompts, and different data sets. But the process above gives you all the tools you need to build robust evals for your LLM apps!

Now you know how to create and run evals via API, and using the dashboard! Here are a few other resources that may be useful to you as you continue to improve your model results.

Keep tabs on the performance of your prompts as you iterate on them.

Compare the results of many different prompts and models at once.

Examine stored completions to test for prompt regressions.

Improve a model's ability to generate responses tailored to your use case.

Learn how to distill large model results to smaller, cheaper, and faster models.

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
14
15
16
curl https://api.openai.com/v1/responses \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "gpt-4.1",
        "input": [
            {
                "role": "developer",
                "content": "Categorize the following support ticket into one of Hardware, Software, or Other."
            },
            {
                "role": "user",
                "content": "My monitor wont turn on - help!"
            }
        ]
    }'
```

Example 2 (bash):
```bash
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
curl https://api.openai.com/v1/responses \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "gpt-4.1",
        "input": [
            {
                "role": "developer",
                "content": "Categorize the following support ticket into one of Hardware, Software, or Other."
            },
            {
                "role": "user",
                "content": "My monitor wont turn on - help!"
            }
        ]
    }'
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
14
15
16
```

Example 4 (python):
```python
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
18
19
20
import OpenAI from "openai";
const client = new OpenAI();

const instructions = `
You are an expert in categorizing IT support tickets. Given the support
ticket below, categorize the request into one of "Hardware", "Software",
or "Other". Respond with only one of those words.
`;

const ticket = "My monitor won't turn on - help!";

const response = await client.responses.create({
    model: "gpt-4.1",
    input: [
        { role: "developer", content: instructions },
        { role: "user", content: ticket },
    ],
});

console.log(response.output_text);
```

---

## Video generation with Sora

**URL:** https://platform.openai.com/docs/guides/video-generation?gallery=open&galleryItem=Cozy-Coffee-Shop-Interior

**Contents:**
- Video generation with Sora
- Overview
- Models
  - Sora 2
  - Sora 2 Pro
- Generate a video
  - Start a render job
  - Guardrails and restrictions
  - Effective prompting
  - Monitor progress

Sora is OpenAI’s newest frontier in generative media – a state-of-the-art video model capable of creating richly detailed, dynamic clips with audio from natural language or images. Built on years of research into multimodal diffusion and trained on diverse visual data, Sora brings a deep understanding of 3D space, motion, and scene continuity to text-to-video generation.

The Video API (in preview) exposes these capabilities to developers for the first time, enabling programmatic creation, extension, and remixing of videos. It provides five endpoints, each with distinct capabilities:

The second generation Sora model comes in two variants, each tailored for different use cases.

sora-2 is designed for speed and flexibility. It’s ideal for the exploration phase, when you’re experimenting with tone, structure, or visual style and need quick feedback rather than perfect fidelity.

It generates good quality results quickly, making it well suited for rapid iteration, concepting, and rough cuts. sora-2 is often more than sufficient for social media content, prototypes, and scenarios where turnaround time matters more than ultra-high fidelity.

sora-2-pro produces higher quality results. It’s the better choice when you need production-quality output.

sora-2-pro takes longer to render and is more expensive to run, but it produces more polished, stable results. It’s best for high-resolution cinematic footage, marketing assets, and any situation where visual precision is critical.

Generating a video is an asynchronous process:

When you call the POST /videos endpoint, the API returns a job object with a job id and an initial status.

You can either poll the GET /videos/{video_id} endpoint until the status transitions to completed, or – for a more efficient approach – use webhooks (see the webhooks section below) to be notified automatically when the job finishes.

Once the job has reached the completed state you can fetch the final MP4 file with GET /videos/{video_id}/content.

Start by calling POST /videos with a text prompt and the required parameters. The prompt defines the creative look and feel – subjects, camera, lighting, and motion – while parameters like size and seconds control the video's resolution and length.

The response is a JSON object with a unique id and an initial status such as queued or in_progress. This means the render job has started.

The API enforces several content restrictions:

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

For best results, describe shot type, subject, action, setting, and lighting. For example:

This level of specificity helps the model produce consistent results without inventing unwanted details. For more advanced prompting techniques, please refer to our dedicated Sora 2 prompting guide.

Video generation takes time. Depending on model, API load and resolution, a single render may take several minutes.

To manage this efficiently, you can poll the API to request status updates or you can get notified via a webhook.

Call GET /videos/{video_id} with the id returned from the create call. The response shows the job’s current status, progress percentage (if available), and any errors.

Typical states are queued, in_progress, completed, and failed. Poll at a reasonable interval (for example, every 10–20 seconds), use exponential backoff if necessary, and provide feedback to users that the job is still in progress.

Instead of polling job status repeatedly with GET, register a webhook to be notified automatically when a video generation completes or fails.

Webhooks can be configured in your webhook settings page. When a job finishes, the API emits one of two event types: video.completed and video.failed. Each event includes the ID of the job that triggered it.

Example webhook payload:

Once the job reaches status completed, fetch the MP4 with GET /videos/{video_id}/content. This endpoint streams the binary video data and returns standard content headers, so you can either save the file directly to disk or pipe it to cloud storage.

You now have the final video file ready for playback, editing, or distribution. Download URLs are valid for a maximum of 1 hour after generation. If you need long-term storage, copy the file to your own storage system promptly.

For each completed video, you can also download a thumbnail and a spritesheet. These are lightweight assets useful for previews, scrubbers, or catalog displays. Use the variant query parameter to specify what you want to download. The default is variant=video for the MP4.

You can guide a generation with an input image, which acts as the first frame of your video. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment. Include an image file as the input_reference parameter in your POST /videos request. The image must match the target video’s resolution (size).

Supported file formats are image/jpeg, image/png, and image/webp.

Remix lets you take an existing video and make targeted adjustments without regenerating everything from scratch. Provide the remix_video_id of a completed job along with a new prompt that describes the change, and the system reuses the original’s structure, continuity, and composition while applying the modification. This works best when you make a single, well-defined change because smaller, focused edits preserve more of the original fidelity and reduce the risk of introducing artifacts.

Remix is especially valuable for iteration because it lets you refine without discarding what already works. By constraining each remix to one clear adjustment, you keep the visual style, subject consistency, and camera framing stable, while still exploring variations in mood, palette, or staging. This makes it far easier to build polished sequences through small, reliable steps.

Use GET /videos to enumerate your videos. The endpoint supports optional query parameters for pagination and sorting.

Use DELETE /videos/{video_id} to remove videos you no longer need from OpenAI’s storage.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
```

Example 2 (javascript):
```javascript
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
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
```

Example 4 (python):
```python
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
from openai import OpenAI

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

---

## Agents

**URL:** https://platform.openai.com/docs/guides/agents

**Contents:**
- Agents
- AgentKit
- How to build an agent
- Deploy agents in your product
- Optimize agent performance
- Get started

Agents are systems that intelligently accomplish tasks—from simple goals to complex, open-ended workflows. OpenAI provides models with agentic strengths, a toolkit for agent creation and deploys, and dashboard features for monitoring and optimizing agents.

AgentKit is a modular toolkit for building, deploying, and optimizing agents.

Building an agent is a process of designing workflows and connecting pieces of the OpenAI platform to meet your goals. Agent Builder brings all these primitives into one UI.

To build a voice agent that understands audio and responds in natural language, see the voice agents docs. Voice agents are not supported in Agent Builder.

When you're ready to bring your agent to production, use ChatKit to bring the agent workflow into your product UI, with an embeddable chat connected to your agentic backend.

Use the OpenAI platform to evaluate agent performance and automate improvements.

Design an agent workflow with Agent Builder →

---

## Managing costs

**URL:** https://platform.openai.com/docs/guides/realtime-costs

**Contents:**
- Managing costs
- Per-Response costs
  - Example
- Input transcription costs
- Caching
- Truncation
- Other optimization strategies
  - Using a mini model
  - Editing the Conversation
- Estimating costs

This document describes how Realtime API billing works and offer strategies for optimizing costs. Costs are accrued as input and output tokens of different modalities: text, audio, and image. Token costs vary per model, with prices listed on the model pages (e.g. for gpt-realtime and gpt-realtime-mini).

Conversational Realtime API sessions are a series of turns, where the user adds input that triggers a Response to produce the model output. The server maintains a Conversation, which is a list of Items that form the input for the next turn. When a Response is returned the output is automatically added to the Conversation.

Realtime API costs are accrued when a Response is created, and is charged based on the numbers of input and output tokens (except for input transcription costs, see below). There is no cost currently for network bandwidth or connections. A Response can be created manually or automatically if voice activity detection (VAD) is turned on. VAD will effectively filter out empty input audio, so empty audio does not count as input tokens unless the client manually adds it as conversation input.

The entire conversation is sent to the model for each Response. The output from a turn will be added as Items to the server Conversation and become the input to subsequent turns, thus turns later in the session will be more expensive.

Text token costs can be estimated using our tokenization tools. Audio tokens in user messages are 1 token per 100 ms of audio, while audio tokens in assistant messages are 1 token per 50ms of audio. Note that token counts include special tokens aside from the content of a message which will surface as small variations in these counts, for example a user message with 10 text tokens of content may count as 12 tokens.

Here’s a simple example to illustrate token costs over a multi-turn Realtime API session.

For the first turn in the conversation we’ve added 100 tokens of instructions, a user message of 20 audio tokens (for example added by VAD based on the user speaking), for a total of 120 input tokens. Creating a Response generates an assistant output message (20 audio, 10 text tokens).

Then we create a second turn with another user audio message. What will the tokens for turn 2 look like? The Conversation at this point includes the initial instructions, first user message, the output assistant message from the first turn, plus the second user message (25 audio tokens). This turn will have 110 text and 64 audio tokens for input, plus the output tokens of another assistant output message.

The messages from the first turn are likely to be cached for turn 2, which reduces the input cost. See below for more information on caching.

The tokens used for a Response can be read from the response.done event, which looks like the following.

Aside from conversational Responses, the Realtime API bills for input transcriptions, if enabled. Input transcription uses a different model than the speech2speech model, such as whisper-1 or gpt-4o-transcribe, and thus are billed from a different rate card. Transcription is performed when audio is written to the input audio buffer and then committed, either manually or by VAD.

Input transcription token counts can be read from the conversation.item.input_audio_transcription.completed event, as in the following example.

Realtime API supports prompt caching, which is applied automatically and can dramatically reduce the costs of input tokens during multi-turn sessions. Caching applies when the input tokens of a Response match tokens from a previous Response, though this is best-effort and not guaranteed.

The best strategy for maximizing cache rate is keep a session’s history static. Removing or changing content in the conversation will “bust” the cache up to the point of the change — the input no longer matches as much as before. Note that instructions and tool definitions are at the beginning of a conversation, thus changing these mid-session will reduce the cache rate for subsequent turns.

When the number of tokens in a conversation exceeds the model's input token limit the conversation be truncated, meaning messages (starting from the oldest) will be dropped from the Response input. A 32k context model with 4,096 max output tokens can only include 28,224 tokens in the context before truncation occurs.

Clients can set a smaller token window than the model’s maximum, which is a good way to control token usage and cost. This is controlled with the token_limits.post_instructions configuration (if you configure truncation with a retention_ratio type as shown below). As the name indicates, this controls the maximum number of input tokens for a Response, except for the instruction tokens. Setting post_instructions to 1,000 means that items over the 1,000 input token limit will not be sent to the model for a Response.

Truncation busts the cache near the beginning of the conversation, and if truncation occurs on every turn then cache rate will be very low. To mitigate this issue clients can configure truncation to drop more messages than necessary, which will extend the headroom before another truncation is needed. This can be controlled with the session.truncation.retention_ratio setting. The server defaults to a value of 1.0 , meaning truncation will remove only the items necessary. A value of 0.8 means a truncation would retain 80% of the maximum, dropping an additional 20%.

If you’re attempting to reduce Realtime API cost per session (for a given model), we recommend reducing limiting the number of tokens and setting a retention_ratio less than 1, as in the following example. Remember that there may be a tradeoff here in terms of lower cost but lower model memory for a given turn.

Truncation can also be completely disabled, as shown below. When disabled an error will be returned if the Conversation is too long to create a Response. This may be useful if you intend to manage the Conversation size manually.

The Realtime speech2speech models come in a “normal” size and a mini size, which is significantly cheaper. The tradeoff here tends to be intelligence related to instruction following and function calling, which will not be as effective in the mini model. We recommend first testing applications with the larger model, refining your application and prompt, then attempting to optimize using the mini model.

While truncation will occur automatically on the server, another cost management strategy is to manually edit the Conversation. A principle of the API is to allow full client control of the server-side Conversation, allowing the client to add and remove items at will.

Clearing out old messages is a good way to reduce input token sizes and cost. This might remove important content, but a common strategy is to replace these old messages with a summary. Items can be deleted from the Conversation with a conversation.item.delete message as above, and can be added with a conversation.item.create message.

Given the complexity in Realtime API token usage it can be difficult to estimate your costs ahead of time. A good approach is to use the Realtime Playground with your intended prompts and functions, and measure the token usage over a sample session. The token usage for a session can be found under the Logs tab in the Realtime Playground next to the session id.

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
14
15
16
17
18
19
20
21
22
23
24
25
26
{
  "type": "response.done",
  "response": {
    ...
    "usage": {
      "total_tokens": 253,
      "input_tokens": 132,
      "output_tokens": 121,
      "input_token_details": {
        "text_tokens": 119,
        "audio_tokens": 13,
        "image_tokens": 0,
        "cached_tokens": 64,
        "cached_tokens_details": {
          "text_tokens": 64,
          "audio_tokens": 0,
          "image_tokens": 0
        }
      },
      "output_token_details": {
        "text_tokens": 30,
        "audio_tokens": 91
      }
    }
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
14
15
16
17
18
19
20
21
22
23
24
25
26
{
  "type": "response.done",
  "response": {
    ...
    "usage": {
      "total_tokens": 253,
      "input_tokens": 132,
      "output_tokens": 121,
      "input_token_details": {
        "text_tokens": 119,
        "audio_tokens": 13,
        "image_tokens": 0,
        "cached_tokens": 64,
        "cached_tokens_details": {
          "text_tokens": 64,
          "audio_tokens": 0,
          "image_tokens": 0
        }
      },
      "output_token_details": {
        "text_tokens": 30,
        "audio_tokens": 91
      }
    }
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
14
15
16
17
18
19
20
21
22
23
24
25
26
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
{
  "type": "conversation.item.input_audio_transcription.completed",
  ...
  "transcript": "Hi, can you hear me?",
  "usage": {
    "type": "tokens",
    "total_tokens": 26,
    "input_tokens": 17,
    "input_token_details": {
      "text_tokens": 0,
      "audio_tokens": 17
    },
    "output_tokens": 9
  }
}
```

---

## Video generation with Sora

**URL:** https://platform.openai.com/docs/guides/video-generation?gallery=open&galleryItem=90s-TV-Ad

**Contents:**
- Video generation with Sora
- Overview
- Models
  - Sora 2
  - Sora 2 Pro
- Generate a video
  - Start a render job
  - Guardrails and restrictions
  - Effective prompting
  - Monitor progress

Sora is OpenAI’s newest frontier in generative media – a state-of-the-art video model capable of creating richly detailed, dynamic clips with audio from natural language or images. Built on years of research into multimodal diffusion and trained on diverse visual data, Sora brings a deep understanding of 3D space, motion, and scene continuity to text-to-video generation.

The Video API (in preview) exposes these capabilities to developers for the first time, enabling programmatic creation, extension, and remixing of videos. It provides five endpoints, each with distinct capabilities:

The second generation Sora model comes in two variants, each tailored for different use cases.

sora-2 is designed for speed and flexibility. It’s ideal for the exploration phase, when you’re experimenting with tone, structure, or visual style and need quick feedback rather than perfect fidelity.

It generates good quality results quickly, making it well suited for rapid iteration, concepting, and rough cuts. sora-2 is often more than sufficient for social media content, prototypes, and scenarios where turnaround time matters more than ultra-high fidelity.

sora-2-pro produces higher quality results. It’s the better choice when you need production-quality output.

sora-2-pro takes longer to render and is more expensive to run, but it produces more polished, stable results. It’s best for high-resolution cinematic footage, marketing assets, and any situation where visual precision is critical.

Generating a video is an asynchronous process:

When you call the POST /videos endpoint, the API returns a job object with a job id and an initial status.

You can either poll the GET /videos/{video_id} endpoint until the status transitions to completed, or – for a more efficient approach – use webhooks (see the webhooks section below) to be notified automatically when the job finishes.

Once the job has reached the completed state you can fetch the final MP4 file with GET /videos/{video_id}/content.

Start by calling POST /videos with a text prompt and the required parameters. The prompt defines the creative look and feel – subjects, camera, lighting, and motion – while parameters like size and seconds control the video's resolution and length.

The response is a JSON object with a unique id and an initial status such as queued or in_progress. This means the render job has started.

The API enforces several content restrictions:

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

For best results, describe shot type, subject, action, setting, and lighting. For example:

This level of specificity helps the model produce consistent results without inventing unwanted details. For more advanced prompting techniques, please refer to our dedicated Sora 2 prompting guide.

Video generation takes time. Depending on model, API load and resolution, a single render may take several minutes.

To manage this efficiently, you can poll the API to request status updates or you can get notified via a webhook.

Call GET /videos/{video_id} with the id returned from the create call. The response shows the job’s current status, progress percentage (if available), and any errors.

Typical states are queued, in_progress, completed, and failed. Poll at a reasonable interval (for example, every 10–20 seconds), use exponential backoff if necessary, and provide feedback to users that the job is still in progress.

Instead of polling job status repeatedly with GET, register a webhook to be notified automatically when a video generation completes or fails.

Webhooks can be configured in your webhook settings page. When a job finishes, the API emits one of two event types: video.completed and video.failed. Each event includes the ID of the job that triggered it.

Example webhook payload:

Once the job reaches status completed, fetch the MP4 with GET /videos/{video_id}/content. This endpoint streams the binary video data and returns standard content headers, so you can either save the file directly to disk or pipe it to cloud storage.

You now have the final video file ready for playback, editing, or distribution. Download URLs are valid for a maximum of 1 hour after generation. If you need long-term storage, copy the file to your own storage system promptly.

For each completed video, you can also download a thumbnail and a spritesheet. These are lightweight assets useful for previews, scrubbers, or catalog displays. Use the variant query parameter to specify what you want to download. The default is variant=video for the MP4.

You can guide a generation with an input image, which acts as the first frame of your video. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment. Include an image file as the input_reference parameter in your POST /videos request. The image must match the target video’s resolution (size).

Supported file formats are image/jpeg, image/png, and image/webp.

Remix lets you take an existing video and make targeted adjustments without regenerating everything from scratch. Provide the remix_video_id of a completed job along with a new prompt that describes the change, and the system reuses the original’s structure, continuity, and composition while applying the modification. This works best when you make a single, well-defined change because smaller, focused edits preserve more of the original fidelity and reduce the risk of introducing artifacts.

Remix is especially valuable for iteration because it lets you refine without discarding what already works. By constraining each remix to one clear adjustment, you keep the visual style, subject consistency, and camera framing stable, while still exploring variations in mood, palette, or staging. This makes it far easier to build polished sequences through small, reliable steps.

Use GET /videos to enumerate your videos. The endpoint supports optional query parameters for pagination and sorting.

Use DELETE /videos/{video_id} to remove videos you no longer need from OpenAI’s storage.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
```

Example 2 (javascript):
```javascript
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
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
```

Example 4 (python):
```python
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
from openai import OpenAI

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

---

## Conversation state

**URL:** https://platform.openai.com/docs/guides/conversation-state?api-mode=responses

**Contents:**
- Conversation state
- Manually manage conversation state
- OpenAI APIs for conversation state
  - Using the Conversations API
  - Passing context from the previous response
- Managing the context window
  - Managing context for text generation
  - Compaction (advanced)
- Next steps

OpenAI provides a few ways to manage conversation state, which is important for preserving information across multiple messages or turns in a conversation.

While each text generation request is independent and stateless, you can still implement multi-turn conversations by providing additional messages as parameters to your text generation request. Consider a knock-knock joke:

By using alternating user and assistant messages, you capture the previous state of a conversation in one request to the model.

To manually share context across generated responses, include the model's previous response output as input, and append that input to your next request.

In the following example, we ask the model to tell a joke, followed by a request for another joke. Appending previous responses to new requests in this way helps ensure conversations feel natural and retain the context of previous interactions.

Our APIs make it easier to manage conversation state automatically, so you don't have to do pass inputs manually with each turn of a conversation.

The Conversations API works with the Responses API to persist conversation state as a long-running object with its own durable identifier. After creating a conversation object, you can keep using it across sessions, devices, or jobs.

Conversations store items, which can be messages, tool calls, tool outputs, and other data.

In a multi-turn interaction, you can pass the conversation into subsequent responses to persist state and share context across subsequent responses, rather than having to chain multiple response items together.

Another way to manage conversation state is to share context across generated responses with the previous_response_id parameter. This parameter lets you chain responses and create a threaded conversation.

In the following example, we ask the model to tell a joke. Separately, we ask the model to explain why it's funny, and the model has all necessary context to deliver a good response.

Response objects are saved for 30 days by default. They can be viewed in the dashboard logs page or retrieved via the API. You can disable this behavior by setting store to false when creating a Response.

Conversation objects and items in them are not subject to the 30 day TTL. Any response attached to a conversation will have its items persisted with no 30 day TTL.

OpenAI does not use data sent via API to train our models without your explicit consent—learn more.

Even when using previous_response_id, all previous input tokens for responses in the chain are billed as input tokens in the API.

Understanding context windows will help you successfully create threaded conversations and manage state across model interactions.

The context window is the maximum number of tokens that can be used in a single request. This max tokens number includes input, output, and reasoning tokens. To learn your model's context window, see model details.

As your inputs become more complex, or you include more turns in a conversation, you'll need to consider both output token and context window limits. Model inputs and outputs are metered in tokens, which are parsed from inputs to analyze their content and intent and assembled to render logical outputs. Models have limits on token usage during the lifecycle of a text generation request.

If you create a very large prompt—often by including extra context, data, or examples for the model—you run the risk of exceeding the allocated context window for a model, which might result in truncated outputs.

Use the tokenizer tool, built with the tiktoken library, to see how many tokens are in a particular string of text.

For example, when making an API request to the Responses API with a reasoning enabled model, like the o1 model, the following token counts will apply toward the context window total:

Tokens generated in excess of the context window limit may be truncated in API responses.

You can estimate the number of tokens your messages will use with the tokenizer tool.

For long-running conversations with the Responses API, you can use the /responses/compact endpoint to shrink the context you send with each turn.

Instructions (optional)

The instructions field lets you include a system-style message that applies only to the compaction request. We recommend using this field only if you also supply instructions when creating responses, and ensuring that the same instructions are passed to both the Responses and Compact endpoints.

For more specific examples and use cases, visit the OpenAI Cookbook, or learn more about using the APIs to extend model capabilities:

**Examples:**

Example 1 (python):
```python
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
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4o-mini",
    input: [
        { role: "user", content: "knock knock." },
        { role: "assistant", content: "Who's there?" },
        { role: "user", content: "Orange." },
    ],
});

console.log(response.output_text);
```

Example 2 (javascript):
```javascript
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
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4o-mini",
    input: [
        { role: "user", content: "knock knock." },
        { role: "assistant", content: "Who's there?" },
        { role: "user", content: "Orange." },
    ],
});

console.log(response.output_text);
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
14
```

Example 4 (python):
```python
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
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {"role": "user", "content": "knock knock."},
        {"role": "assistant", "content": "Who's there?"},
        {"role": "user", "content": "Orange."},
    ],
)

print(response.output_text)
```

---

## Video generation with Sora

**URL:** https://platform.openai.com/docs/guides/video-generation?gallery=open&galleryItem=coloring

**Contents:**
- Video generation with Sora
- Overview
- Models
  - Sora 2
  - Sora 2 Pro
- Generate a video
  - Start a render job
  - Guardrails and restrictions
  - Effective prompting
  - Monitor progress

Sora is OpenAI’s newest frontier in generative media – a state-of-the-art video model capable of creating richly detailed, dynamic clips with audio from natural language or images. Built on years of research into multimodal diffusion and trained on diverse visual data, Sora brings a deep understanding of 3D space, motion, and scene continuity to text-to-video generation.

The Video API (in preview) exposes these capabilities to developers for the first time, enabling programmatic creation, extension, and remixing of videos. It provides five endpoints, each with distinct capabilities:

The second generation Sora model comes in two variants, each tailored for different use cases.

sora-2 is designed for speed and flexibility. It’s ideal for the exploration phase, when you’re experimenting with tone, structure, or visual style and need quick feedback rather than perfect fidelity.

It generates good quality results quickly, making it well suited for rapid iteration, concepting, and rough cuts. sora-2 is often more than sufficient for social media content, prototypes, and scenarios where turnaround time matters more than ultra-high fidelity.

sora-2-pro produces higher quality results. It’s the better choice when you need production-quality output.

sora-2-pro takes longer to render and is more expensive to run, but it produces more polished, stable results. It’s best for high-resolution cinematic footage, marketing assets, and any situation where visual precision is critical.

Generating a video is an asynchronous process:

When you call the POST /videos endpoint, the API returns a job object with a job id and an initial status.

You can either poll the GET /videos/{video_id} endpoint until the status transitions to completed, or – for a more efficient approach – use webhooks (see the webhooks section below) to be notified automatically when the job finishes.

Once the job has reached the completed state you can fetch the final MP4 file with GET /videos/{video_id}/content.

Start by calling POST /videos with a text prompt and the required parameters. The prompt defines the creative look and feel – subjects, camera, lighting, and motion – while parameters like size and seconds control the video's resolution and length.

The response is a JSON object with a unique id and an initial status such as queued or in_progress. This means the render job has started.

The API enforces several content restrictions:

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

For best results, describe shot type, subject, action, setting, and lighting. For example:

This level of specificity helps the model produce consistent results without inventing unwanted details. For more advanced prompting techniques, please refer to our dedicated Sora 2 prompting guide.

Video generation takes time. Depending on model, API load and resolution, a single render may take several minutes.

To manage this efficiently, you can poll the API to request status updates or you can get notified via a webhook.

Call GET /videos/{video_id} with the id returned from the create call. The response shows the job’s current status, progress percentage (if available), and any errors.

Typical states are queued, in_progress, completed, and failed. Poll at a reasonable interval (for example, every 10–20 seconds), use exponential backoff if necessary, and provide feedback to users that the job is still in progress.

Instead of polling job status repeatedly with GET, register a webhook to be notified automatically when a video generation completes or fails.

Webhooks can be configured in your webhook settings page. When a job finishes, the API emits one of two event types: video.completed and video.failed. Each event includes the ID of the job that triggered it.

Example webhook payload:

Once the job reaches status completed, fetch the MP4 with GET /videos/{video_id}/content. This endpoint streams the binary video data and returns standard content headers, so you can either save the file directly to disk or pipe it to cloud storage.

You now have the final video file ready for playback, editing, or distribution. Download URLs are valid for a maximum of 1 hour after generation. If you need long-term storage, copy the file to your own storage system promptly.

For each completed video, you can also download a thumbnail and a spritesheet. These are lightweight assets useful for previews, scrubbers, or catalog displays. Use the variant query parameter to specify what you want to download. The default is variant=video for the MP4.

You can guide a generation with an input image, which acts as the first frame of your video. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment. Include an image file as the input_reference parameter in your POST /videos request. The image must match the target video’s resolution (size).

Supported file formats are image/jpeg, image/png, and image/webp.

Remix lets you take an existing video and make targeted adjustments without regenerating everything from scratch. Provide the remix_video_id of a completed job along with a new prompt that describes the change, and the system reuses the original’s structure, continuity, and composition while applying the modification. This works best when you make a single, well-defined change because smaller, focused edits preserve more of the original fidelity and reduce the risk of introducing artifacts.

Remix is especially valuable for iteration because it lets you refine without discarding what already works. By constraining each remix to one clear adjustment, you keep the visual style, subject consistency, and camera framing stable, while still exploring variations in mood, palette, or staging. This makes it far easier to build polished sequences through small, reliable steps.

Use GET /videos to enumerate your videos. The endpoint supports optional query parameters for pagination and sorting.

Use DELETE /videos/{video_id} to remove videos you no longer need from OpenAI’s storage.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
```

Example 2 (javascript):
```javascript
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
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
```

Example 4 (python):
```python
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
from openai import OpenAI

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

---

## Batch API

**URL:** https://platform.openai.com/docs/guides/batch

**Contents:**
- Batch API
- Overview
- Getting started
  - 1. Prepare your batch file
    - Moderations input examples
  - 2. Upload your batch input file
  - 3. Create the batch
  - 4. Check the status of a batch
  - 5. Retrieve the results
  - 6. Cancel a batch

Learn how to use OpenAI's Batch API to send asynchronous groups of requests with 50% lower costs, a separate pool of significantly higher rate limits, and a clear 24-hour turnaround time. The service is ideal for processing jobs that don't require immediate responses. You can also explore the API reference directly here.

While some uses of the OpenAI Platform require you to send synchronous requests, there are many cases where requests do not need an immediate response or rate limits prevent you from executing a large number of queries quickly. Batch processing jobs are often helpful in use cases like:

The Batch API offers a straightforward set of endpoints that allow you to collect a set of requests into a single file, kick off a batch processing job to execute these requests, query for the status of that batch while the underlying requests execute, and eventually retrieve the collected results when the batch is complete.

Compared to using standard endpoints directly, Batch API has:

Batches start with a .jsonl file where each line contains the details of an individual request to the API. For now, the available endpoints are /v1/responses (Responses API), /v1/chat/completions (Chat Completions API), /v1/embeddings (Embeddings API), /v1/completions (Completions API), and /v1/moderations (Moderations guide). For a given input file, the parameters in each line's body field are the same as the parameters for the underlying endpoint. Each request must include a unique custom_id value, which you can use to reference results after completion. Here's an example of an input file with 2 requests. Note that each input file can only include requests to a single model.

When targeting /v1/moderations, include an input field in every request body. Batch accepts both plain-text inputs (for omni-moderation-latest and text-moderation-latest) and multimodal content arrays (for omni-moderation-latest). The Batch worker enforces the same non-streaming requirement as the synchronous Moderations API and rejects requests that set stream=true.

Prefer referencing remote assets with image_url (instead of base64 blobs) to keep your .jsonl files well below the 200 MB Batch upload limit, especially for multimodal Moderations requests.

Similar to our Fine-tuning API, you must first upload your input file so that you can reference it correctly when kicking off batches. Upload your .jsonl file using the Files API.

Once you've successfully uploaded your input file, you can use the input File object's ID to create a batch. In this case, let's assume the file ID is file-abc123. For now, the completion window can only be set to 24h. You can also provide custom metadata via an optional metadata parameter.

This request will return a Batch object with metadata about your batch:

You can check the status of a batch at any time, which will also return a Batch object.

The status of a given Batch object can be any of the following:

Once the batch is complete, you can download the output by making a request against the Files API via the output_file_id field from the Batch object and writing it to a file on your machine, in this case batch_output.jsonl

The output .jsonl file will have one response line for every successful request line in the input file. Any failed requests in the batch will have their error information written to an error file that can be found via the batch's error_file_id.

Note that the output line order may not match the input line order. Instead of relying on order to process your results, use the custom_id field which will be present in each line of your output file and allow you to map requests in your input to results in your output.

The output file will automatically be deleted 30 days after the batch is complete.

If necessary, you can cancel an ongoing batch. The batch's status will change to cancelling until in-flight requests are complete (up to 10 minutes), after which the status will change to cancelled.

At any time, you can see all your batches. For users with many batches, you can use the limit and after parameters to paginate your results.

The Batch API is widely available across most of our models, but not all. Please refer to the model reference docs to ensure the model you're using supports the Batch API.

Batch API rate limits are separate from existing per-model rate limits. The Batch API has two new types of rate limits:

There are no limits for output tokens or number of submitted requests for the Batch API today. Because Batch API rate limits are a new, separate pool, using the Batch API will not consume tokens from your standard per-model rate limits, thereby offering you a convenient way to increase the number of requests and processed tokens you can use when querying our API.

Batches that do not complete in time eventually move to an expired state; unfinished requests within that batch are cancelled, and any responses to completed requests are made available via the batch's output file. You will be charged for tokens consumed from any completed requests.

Expired requests will be written to your error file with the message as shown below. You can use the custom_id to retrieve the request data for expired requests.

**Examples:**

Example 1 (unknown):
```unknown
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are an unhelpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
```

Example 2 (jsonl):
```jsonl
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-3.5-turbo-0125", "messages": [{"role": "system", "content": "You are an unhelpful assistant."},{"role": "user", "content": "Hello world!"}],"max_tokens": 1000}}
```

Example 3 (unknown):
```unknown
{"custom_id": "moderation-text-1", "method": "POST", "url": "/v1/moderations", "body": {"model": "omni-moderation-latest", "input": "This is a harmless test sentence."}}
```

Example 4 (jsonl):
```jsonl
{"custom_id": "moderation-text-1", "method": "POST", "url": "/v1/moderations", "body": {"model": "omni-moderation-latest", "input": "This is a harmless test sentence."}}
```

---

## Video generation with Sora

**URL:** https://platform.openai.com/docs/guides/video-generation?gallery=open&galleryItem=zebra-chase

**Contents:**
- Video generation with Sora
- Overview
- Models
  - Sora 2
  - Sora 2 Pro
- Generate a video
  - Start a render job
  - Guardrails and restrictions
  - Effective prompting
  - Monitor progress

Sora is OpenAI’s newest frontier in generative media – a state-of-the-art video model capable of creating richly detailed, dynamic clips with audio from natural language or images. Built on years of research into multimodal diffusion and trained on diverse visual data, Sora brings a deep understanding of 3D space, motion, and scene continuity to text-to-video generation.

The Video API (in preview) exposes these capabilities to developers for the first time, enabling programmatic creation, extension, and remixing of videos. It provides five endpoints, each with distinct capabilities:

The second generation Sora model comes in two variants, each tailored for different use cases.

sora-2 is designed for speed and flexibility. It’s ideal for the exploration phase, when you’re experimenting with tone, structure, or visual style and need quick feedback rather than perfect fidelity.

It generates good quality results quickly, making it well suited for rapid iteration, concepting, and rough cuts. sora-2 is often more than sufficient for social media content, prototypes, and scenarios where turnaround time matters more than ultra-high fidelity.

sora-2-pro produces higher quality results. It’s the better choice when you need production-quality output.

sora-2-pro takes longer to render and is more expensive to run, but it produces more polished, stable results. It’s best for high-resolution cinematic footage, marketing assets, and any situation where visual precision is critical.

Generating a video is an asynchronous process:

When you call the POST /videos endpoint, the API returns a job object with a job id and an initial status.

You can either poll the GET /videos/{video_id} endpoint until the status transitions to completed, or – for a more efficient approach – use webhooks (see the webhooks section below) to be notified automatically when the job finishes.

Once the job has reached the completed state you can fetch the final MP4 file with GET /videos/{video_id}/content.

Start by calling POST /videos with a text prompt and the required parameters. The prompt defines the creative look and feel – subjects, camera, lighting, and motion – while parameters like size and seconds control the video's resolution and length.

The response is a JSON object with a unique id and an initial status such as queued or in_progress. This means the render job has started.

The API enforces several content restrictions:

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

For best results, describe shot type, subject, action, setting, and lighting. For example:

This level of specificity helps the model produce consistent results without inventing unwanted details. For more advanced prompting techniques, please refer to our dedicated Sora 2 prompting guide.

Video generation takes time. Depending on model, API load and resolution, a single render may take several minutes.

To manage this efficiently, you can poll the API to request status updates or you can get notified via a webhook.

Call GET /videos/{video_id} with the id returned from the create call. The response shows the job’s current status, progress percentage (if available), and any errors.

Typical states are queued, in_progress, completed, and failed. Poll at a reasonable interval (for example, every 10–20 seconds), use exponential backoff if necessary, and provide feedback to users that the job is still in progress.

Instead of polling job status repeatedly with GET, register a webhook to be notified automatically when a video generation completes or fails.

Webhooks can be configured in your webhook settings page. When a job finishes, the API emits one of two event types: video.completed and video.failed. Each event includes the ID of the job that triggered it.

Example webhook payload:

Once the job reaches status completed, fetch the MP4 with GET /videos/{video_id}/content. This endpoint streams the binary video data and returns standard content headers, so you can either save the file directly to disk or pipe it to cloud storage.

You now have the final video file ready for playback, editing, or distribution. Download URLs are valid for a maximum of 1 hour after generation. If you need long-term storage, copy the file to your own storage system promptly.

For each completed video, you can also download a thumbnail and a spritesheet. These are lightweight assets useful for previews, scrubbers, or catalog displays. Use the variant query parameter to specify what you want to download. The default is variant=video for the MP4.

You can guide a generation with an input image, which acts as the first frame of your video. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment. Include an image file as the input_reference parameter in your POST /videos request. The image must match the target video’s resolution (size).

Supported file formats are image/jpeg, image/png, and image/webp.

Remix lets you take an existing video and make targeted adjustments without regenerating everything from scratch. Provide the remix_video_id of a completed job along with a new prompt that describes the change, and the system reuses the original’s structure, continuity, and composition while applying the modification. This works best when you make a single, well-defined change because smaller, focused edits preserve more of the original fidelity and reduce the risk of introducing artifacts.

Remix is especially valuable for iteration because it lets you refine without discarding what already works. By constraining each remix to one clear adjustment, you keep the visual style, subject consistency, and camera framing stable, while still exploring variations in mood, palette, or staging. This makes it far easier to build polished sequences through small, reliable steps.

Use GET /videos to enumerate your videos. The endpoint supports optional query parameters for pagination and sorting.

Use DELETE /videos/{video_id} to remove videos you no longer need from OpenAI’s storage.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
```

Example 2 (javascript):
```javascript
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
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
```

Example 4 (python):
```python
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
from openai import OpenAI

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

---

## Video generation with Sora

**URL:** https://platform.openai.com/docs/guides/video-generation?gallery=open&galleryItem=indie-cafe-rainy-window

**Contents:**
- Video generation with Sora
- Overview
- Models
  - Sora 2
  - Sora 2 Pro
- Generate a video
  - Start a render job
  - Guardrails and restrictions
  - Effective prompting
  - Monitor progress

Sora is OpenAI’s newest frontier in generative media – a state-of-the-art video model capable of creating richly detailed, dynamic clips with audio from natural language or images. Built on years of research into multimodal diffusion and trained on diverse visual data, Sora brings a deep understanding of 3D space, motion, and scene continuity to text-to-video generation.

The Video API (in preview) exposes these capabilities to developers for the first time, enabling programmatic creation, extension, and remixing of videos. It provides five endpoints, each with distinct capabilities:

The second generation Sora model comes in two variants, each tailored for different use cases.

sora-2 is designed for speed and flexibility. It’s ideal for the exploration phase, when you’re experimenting with tone, structure, or visual style and need quick feedback rather than perfect fidelity.

It generates good quality results quickly, making it well suited for rapid iteration, concepting, and rough cuts. sora-2 is often more than sufficient for social media content, prototypes, and scenarios where turnaround time matters more than ultra-high fidelity.

sora-2-pro produces higher quality results. It’s the better choice when you need production-quality output.

sora-2-pro takes longer to render and is more expensive to run, but it produces more polished, stable results. It’s best for high-resolution cinematic footage, marketing assets, and any situation where visual precision is critical.

Generating a video is an asynchronous process:

When you call the POST /videos endpoint, the API returns a job object with a job id and an initial status.

You can either poll the GET /videos/{video_id} endpoint until the status transitions to completed, or – for a more efficient approach – use webhooks (see the webhooks section below) to be notified automatically when the job finishes.

Once the job has reached the completed state you can fetch the final MP4 file with GET /videos/{video_id}/content.

Start by calling POST /videos with a text prompt and the required parameters. The prompt defines the creative look and feel – subjects, camera, lighting, and motion – while parameters like size and seconds control the video's resolution and length.

The response is a JSON object with a unique id and an initial status such as queued or in_progress. This means the render job has started.

The API enforces several content restrictions:

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

For best results, describe shot type, subject, action, setting, and lighting. For example:

This level of specificity helps the model produce consistent results without inventing unwanted details. For more advanced prompting techniques, please refer to our dedicated Sora 2 prompting guide.

Video generation takes time. Depending on model, API load and resolution, a single render may take several minutes.

To manage this efficiently, you can poll the API to request status updates or you can get notified via a webhook.

Call GET /videos/{video_id} with the id returned from the create call. The response shows the job’s current status, progress percentage (if available), and any errors.

Typical states are queued, in_progress, completed, and failed. Poll at a reasonable interval (for example, every 10–20 seconds), use exponential backoff if necessary, and provide feedback to users that the job is still in progress.

Instead of polling job status repeatedly with GET, register a webhook to be notified automatically when a video generation completes or fails.

Webhooks can be configured in your webhook settings page. When a job finishes, the API emits one of two event types: video.completed and video.failed. Each event includes the ID of the job that triggered it.

Example webhook payload:

Once the job reaches status completed, fetch the MP4 with GET /videos/{video_id}/content. This endpoint streams the binary video data and returns standard content headers, so you can either save the file directly to disk or pipe it to cloud storage.

You now have the final video file ready for playback, editing, or distribution. Download URLs are valid for a maximum of 1 hour after generation. If you need long-term storage, copy the file to your own storage system promptly.

For each completed video, you can also download a thumbnail and a spritesheet. These are lightweight assets useful for previews, scrubbers, or catalog displays. Use the variant query parameter to specify what you want to download. The default is variant=video for the MP4.

You can guide a generation with an input image, which acts as the first frame of your video. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment. Include an image file as the input_reference parameter in your POST /videos request. The image must match the target video’s resolution (size).

Supported file formats are image/jpeg, image/png, and image/webp.

Remix lets you take an existing video and make targeted adjustments without regenerating everything from scratch. Provide the remix_video_id of a completed job along with a new prompt that describes the change, and the system reuses the original’s structure, continuity, and composition while applying the modification. This works best when you make a single, well-defined change because smaller, focused edits preserve more of the original fidelity and reduce the risk of introducing artifacts.

Remix is especially valuable for iteration because it lets you refine without discarding what already works. By constraining each remix to one clear adjustment, you keep the visual style, subject consistency, and camera framing stable, while still exploring variations in mood, palette, or staging. This makes it far easier to build polished sequences through small, reliable steps.

Use GET /videos to enumerate your videos. The endpoint supports optional query parameters for pagination and sorting.

Use DELETE /videos/{video_id} to remove videos you no longer need from OpenAI’s storage.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
```

Example 2 (javascript):
```javascript
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
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
```

Example 4 (python):
```python
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
from openai import OpenAI

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

---

## Error codes

**URL:** https://platform.openai.com/docs/guides/error-codes

**Contents:**
- Error codes
- API errors
- Python library error types
  - Persistent errors
  - Handling errors

This guide includes an overview on error codes you might see from both the API and our official Python library. Each error code mentioned in the overview has a dedicated section with further guidance.

This error message indicates that your authentication credentials are invalid. This could happen for several reasons, such as:

To resolve this error, please follow these steps:

This error message indicates that the API key you are using in your request is not correct. This could happen for several reasons, such as:

To resolve this error, please follow these steps:

This error message indicates that your account is not part of an organization. This could happen for several reasons, such as:

To resolve this error, please follow these steps:

This error message indicates that you have hit your assigned rate limit for the API. This means that you have submitted too many tokens or requests in a short period of time and have exceeded the number of requests allowed. This could happen for several reasons, such as:

To resolve this error, please follow these steps:

This error message indicates that you hit your monthly usage limit for the API, or for prepaid credits customers that you've consumed all your credits. You can view your maximum usage limit on the limits page. This could happen for several reasons, such as:

To resolve this error, please follow these steps:

This error message indicates that our servers are experiencing high traffic and are unable to process your request at the moment. This could happen for several reasons, such as:

To resolve this error, please follow these steps:

This error can occur with Pay-As-You-Go models, which are shared across all OpenAI users. It indicates that your traffic has significantly increased, overloading the model and triggering temporary throttling to maintain service stability.

To resolve this error, please follow these steps:

An APIConnectionError indicates that your request could not reach our servers or establish a secure connection. This could be due to a network issue, a proxy configuration, an SSL certificate, or a firewall rule.

If you encounter an APIConnectionError, please try the following steps:

A APITimeoutError error indicates that your request took too long to complete and our server closed the connection. This could be due to a network issue, a heavy load on our services, or a complex request that requires more processing time.

If you encounter a APITimeoutError error, please try the following steps:

An AuthenticationError indicates that your API key or token was invalid, expired, or revoked. This could be due to a typo, a formatting error, or a security breach.

If you encounter an AuthenticationError, please try the following steps:

An BadRequestError (formerly InvalidRequestError) indicates that your request was malformed or missing some required parameters, such as a token or an input. This could be due to a typo, a formatting error, or a logic error in your code.

If you encounter an BadRequestError, please try the following steps:

An InternalServerError indicates that something went wrong on our side when processing your request. This could be due to a temporary error, a bug, or a system outage.

We apologize for any inconvenience and we are working hard to resolve any issues as soon as possible. You can check our system status page for more information.

If you encounter an InternalServerError, please try the following steps:

Our support team will investigate the issue and get back to you as soon as possible. Note that our support queue times may be long due to high demand. You can also post in our Community Forum but be sure to omit any sensitive information.

A RateLimitError indicates that you have hit your assigned rate limit. This means that you have sent too many tokens or requests in a given period of time, and our services have temporarily blocked you from sending more.

We impose rate limits to ensure fair and efficient use of our resources and to prevent abuse or overload of our services.

If you encounter a RateLimitError, please try the following steps:

If the issue persists, contact our support team via chat and provide them with the following information:

Our support team will investigate the issue and get back to you as soon as possible. Note that our support queue times may be long due to high demand. You can also post in our Community Forum but be sure to omit any sensitive information.

We advise you to programmatically handle errors returned by the API. To do so, you may want to use a code snippet like below:

**Examples:**

Example 1 (python):
```python
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
18
19
20
21
22
import openai
from openai import OpenAI
client = OpenAI()

try:
  #Make your OpenAI API request here
  response = client.chat.completions.create(
    prompt="Hello world",
    model="gpt-4o-mini"
  )
except openai.APIError as e:
  #Handle API error here, e.g. retry or log
  print(f"OpenAI API returned an API Error: {e}")
  pass
except openai.APIConnectionError as e:
  #Handle connection error here
  print(f"Failed to connect to OpenAI API: {e}")
  pass
except openai.RateLimitError as e:
  #Handle rate limit error (we recommend using exponential backoff)
  print(f"OpenAI API request exceeded rate limit: {e}")
  pass
```

Example 2 (python):
```python
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
18
19
20
21
22
import openai
from openai import OpenAI
client = OpenAI()

try:
  #Make your OpenAI API request here
  response = client.chat.completions.create(
    prompt="Hello world",
    model="gpt-4o-mini"
  )
except openai.APIError as e:
  #Handle API error here, e.g. retry or log
  print(f"OpenAI API returned an API Error: {e}")
  pass
except openai.APIConnectionError as e:
  #Handle connection error here
  print(f"Failed to connect to OpenAI API: {e}")
  pass
except openai.RateLimitError as e:
  #Handle rate limit error (we recommend using exponential backoff)
  print(f"OpenAI API request exceeded rate limit: {e}")
  pass
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
14
15
16
17
18
19
20
21
22
```

---

## Video generation with Sora

**URL:** https://platform.openai.com/docs/guides/video-generation

**Contents:**
- Video generation with Sora
- Overview
- Models
  - Sora 2
  - Sora 2 Pro
- Generate a video
  - Start a render job
  - Guardrails and restrictions
  - Effective prompting
  - Monitor progress

Sora is OpenAI’s newest frontier in generative media – a state-of-the-art video model capable of creating richly detailed, dynamic clips with audio from natural language or images. Built on years of research into multimodal diffusion and trained on diverse visual data, Sora brings a deep understanding of 3D space, motion, and scene continuity to text-to-video generation.

The Video API (in preview) exposes these capabilities to developers for the first time, enabling programmatic creation, extension, and remixing of videos. It provides five endpoints, each with distinct capabilities:

The second generation Sora model comes in two variants, each tailored for different use cases.

sora-2 is designed for speed and flexibility. It’s ideal for the exploration phase, when you’re experimenting with tone, structure, or visual style and need quick feedback rather than perfect fidelity.

It generates good quality results quickly, making it well suited for rapid iteration, concepting, and rough cuts. sora-2 is often more than sufficient for social media content, prototypes, and scenarios where turnaround time matters more than ultra-high fidelity.

sora-2-pro produces higher quality results. It’s the better choice when you need production-quality output.

sora-2-pro takes longer to render and is more expensive to run, but it produces more polished, stable results. It’s best for high-resolution cinematic footage, marketing assets, and any situation where visual precision is critical.

Generating a video is an asynchronous process:

When you call the POST /videos endpoint, the API returns a job object with a job id and an initial status.

You can either poll the GET /videos/{video_id} endpoint until the status transitions to completed, or – for a more efficient approach – use webhooks (see the webhooks section below) to be notified automatically when the job finishes.

Once the job has reached the completed state you can fetch the final MP4 file with GET /videos/{video_id}/content.

Start by calling POST /videos with a text prompt and the required parameters. The prompt defines the creative look and feel – subjects, camera, lighting, and motion – while parameters like size and seconds control the video's resolution and length.

The response is a JSON object with a unique id and an initial status such as queued or in_progress. This means the render job has started.

The API enforces several content restrictions:

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

For best results, describe shot type, subject, action, setting, and lighting. For example:

This level of specificity helps the model produce consistent results without inventing unwanted details. For more advanced prompting techniques, please refer to our dedicated Sora 2 prompting guide.

Video generation takes time. Depending on model, API load and resolution, a single render may take several minutes.

To manage this efficiently, you can poll the API to request status updates or you can get notified via a webhook.

Call GET /videos/{video_id} with the id returned from the create call. The response shows the job’s current status, progress percentage (if available), and any errors.

Typical states are queued, in_progress, completed, and failed. Poll at a reasonable interval (for example, every 10–20 seconds), use exponential backoff if necessary, and provide feedback to users that the job is still in progress.

Instead of polling job status repeatedly with GET, register a webhook to be notified automatically when a video generation completes or fails.

Webhooks can be configured in your webhook settings page. When a job finishes, the API emits one of two event types: video.completed and video.failed. Each event includes the ID of the job that triggered it.

Example webhook payload:

Once the job reaches status completed, fetch the MP4 with GET /videos/{video_id}/content. This endpoint streams the binary video data and returns standard content headers, so you can either save the file directly to disk or pipe it to cloud storage.

You now have the final video file ready for playback, editing, or distribution. Download URLs are valid for a maximum of 1 hour after generation. If you need long-term storage, copy the file to your own storage system promptly.

For each completed video, you can also download a thumbnail and a spritesheet. These are lightweight assets useful for previews, scrubbers, or catalog displays. Use the variant query parameter to specify what you want to download. The default is variant=video for the MP4.

You can guide a generation with an input image, which acts as the first frame of your video. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment. Include an image file as the input_reference parameter in your POST /videos request. The image must match the target video’s resolution (size).

Supported file formats are image/jpeg, image/png, and image/webp.

Remix lets you take an existing video and make targeted adjustments without regenerating everything from scratch. Provide the remix_video_id of a completed job along with a new prompt that describes the change, and the system reuses the original’s structure, continuity, and composition while applying the modification. This works best when you make a single, well-defined change because smaller, focused edits preserve more of the original fidelity and reduce the risk of introducing artifacts.

Remix is especially valuable for iteration because it lets you refine without discarding what already works. By constraining each remix to one clear adjustment, you keep the visual style, subject consistency, and camera framing stable, while still exploring variations in mood, palette, or staging. This makes it far easier to build polished sequences through small, reliable steps.

Use GET /videos to enumerate your videos. The endpoint supports optional query parameters for pagination and sorting.

Use DELETE /videos/{video_id} to remove videos you no longer need from OpenAI’s storage.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
```

Example 2 (javascript):
```javascript
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
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
```

Example 4 (python):
```python
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
from openai import OpenAI

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

---

## Latency optimization

**URL:** https://platform.openai.com/docs/guides/latency-optimization

**Contents:**
- Latency optimization
  - Seven principles
- Process tokens faster
- Generate fewer tokens
- Use fewer input tokens
- Make fewer requests
- Parallelize
- Make your users wait less
- Don't default to an LLM
- Example

This guide covers the core set of principles you can apply to improve latency across a wide variety of LLM-related use cases. These techniques come from working with a wide range of customers and developers on production applications, so they should apply regardless of what you're building – from a granular workflow to an end-to-end chatbot.

While there's many individual techniques, we'll be grouping them into seven principles meant to represent a high-level taxonomy of approaches for improving latency.

At the end, we'll walk through an example to see how they can be applied.

Inference speed is probably the first thing that comes to mind when addressing latency (but as you'll see soon, it's far from the only one). This refers to the actual rate at which the LLM processes tokens, and is often measured in TPM (tokens per minute) or TPS (tokens per second).

The main factor that influences inference speed is model size – smaller models usually run faster (and cheaper), and when used correctly can even outperform larger models. To maintain high quality performance with smaller models you can explore:

You can also employ inference optimizations like our Predicted outputs feature. Predicted outputs let you significantly reduce latency of a generation when you know most of the output ahead of time, such as code editing tasks. By giving the model a prediction, the LLM can focus more on the actual changes, and less on the content that will remain the same.

Generating tokens is almost always the highest latency step when using an LLM: as a general heuristic, cutting 50% of your output tokens may cut ~50% your latency. The way you reduce your output size will depend on output type:

If you're generating natural language, simply asking the model to be more concise ("under 20 words" or "be very brief") may help. You can also use few shot examples and/or fine-tuning to teach the model shorter responses.

If you're generating structured output, try to minimize your output syntax where possible: shorten function names, omit named arguments, coalesce parameters, etc.

Finally, while not common, you can also use max_tokens or stop_tokens to end your generation early.

Always remember: an output token cut is a (milli)second earned!

While reducing the number of input tokens does result in lower latency, this is not usually a significant factor – cutting 50% of your prompt may only result in a 1-5% latency improvement. Unless you're working with truly massive context sizes (documents, images), you may want to spend your efforts elsewhere.

That being said, if you are working with massive contexts (or you're set on squeezing every last bit of performance and you've exhausted all other options) you can use the following techniques to reduce your input tokens:

Check out our docs to learn more about how prompt caching works.

Each time you make a request you incur some round-trip latency – this can start to add up.

If you have sequential steps for the LLM to perform, instead of firing off one request per step consider putting them in a single prompt and getting them all in a single response. You'll avoid the additional round-trip latency, and potentially also reduce complexity of processing multiple responses.

An approach to doing this is by collecting your steps in an enumerated list in the combined prompt, and then requesting the model to return the results in named fields in a JSON. This way you can easily parse out and reference each result!

Parallelization can be very powerful when performing multiple steps with an LLM.

If the steps are not strictly sequential, you can split them out into parallel calls. Two shirts take just as long to dry as one.

If the steps are strictly sequential, however, you might still be able to leverage speculative execution. This is particularly effective for classification steps where one outcome is more likely than the others (e.g. moderation).

If your guess for step 1 is right, then you essentially got to run it with zero added latency!

There's a huge difference between waiting and watching progress happen – make sure your users experience the latter. Here are a few techniques:

Note that while showing your steps & having loading states have a mostly psychological effect, streaming & chunking genuinely do reduce overall latency once you consider the app + user system: the user will finish reading a response sooner.

LLMs are extremely powerful and versatile, and are therefore sometimes used in cases where a faster classical method would be more appropriate. Identifying such cases may allow you to cut your latency significantly. Consider the following examples:

Let's now look at a sample application, identify potential latency optimizations, and propose some solutions!

We'll be analyzing the architecture and prompts of a hypothetical customer service bot inspired by real production applications. The architecture and prompts section sets the stage, and the analysis and optimizations section will walk through the latency optimization process.

You'll notice this example doesn't cover every single principle, much like real-world use cases don't require applying every technique.

The following is the initial architecture for a hypothetical customer service bot. This is what we'll be making changes to.

At a high level, the diagram flow describes the following process:

Below are the prompts used in each part of the diagram. While they are still only hypothetical and simplified, they are written with the same structure and wording that you would find in a production application.

Places where you see placeholders like "[user input here]" represent dynamic portions, that would be replaced by actual data at runtime.

Re-writes user query to be a self-contained search query.

Determines whether a query requires performing retrieval to respond.

Fills the fields of a JSON to reason through a pre-defined set of steps to produce a final response given a user conversation and relevant retrieved information.

Looking at the architecture, the first thing that stands out is the consecutive GPT-4 calls - these hint at a potential inefficiency, and can often be replaced by a single call or parallel calls.

In this case, since the check for retrieval requires the contextualized query, let's combine them into a single prompt to make fewer requests.

What changed? Before, we had one prompt to re-write the query and one to determine whether this requires doing a retrieval lookup. Now, this combined prompt does both. Specifically, notice the updated instruction in the first line of the prompt, and the updated output JSON:

Actually, adding context and determining whether to retrieve are very straightforward and well defined tasks, so we can likely use a smaller, fine-tuned model instead. Switching to GPT-3.5 will let us process tokens faster.

Let's now direct our attention to the Assistant prompt. There seem to be many distinct steps happening as it fills the JSON fields – this could indicate an opportunity to parallelize.

However, let's pretend we have run some tests and discovered that splitting the reasoning steps in the JSON produces worse responses, so we need to explore different solutions.

Could we use a fine-tuned GPT-3.5 instead of GPT-4? Maybe – but in general, open-ended responses from assistants are best left to GPT-4 so it can better handle a greater range of cases. That being said, looking at the reasoning steps themselves, they may not all require GPT-4 level reasoning to produce. The well defined, limited scope nature makes them and good potential candidates for fine-tuning.

This opens up the possibility of a trade-off. Do we keep this as a single request entirely generated by GPT-4, or split it into two sequential requests and use GPT-3.5 for all but the final response? We have a case of conflicting principles: the first option lets us make fewer requests, but the second may let us process tokens faster.

As with many optimization tradeoffs, the answer will depend on the details. For example:

The conclusion will vary by case, and the best way to make the determiation is by testing this with production examples. In this case let's pretend the tests indicated it's favorable to split the prompt in two to process tokens faster.

Note: We'll be grouping response and enough_information_in_context together in the second prompt to avoid passing the retrieved context to both new prompts.

This prompt will be passed to GPT-3.5 and can be fine-tuned on curated examples.

What changed? The "enough_information_in_context" and "response" fields were removed, and the retrieval results are no longer loaded into this prompt.

This prompt will be processed by GPT-4 and will receive the reasoning steps determined in the prior prompt, as well as the results from retrieval.

What changed? All steps were removed except for "enough_information_in_context" and "response". Additionally, the JSON we were previously filling in as output will be passed in to this prompt.

In fact, now that the reasoning prompt does not depend on the retrieved context we can parallelize and fire it off at the same time as the retrieval prompts.

Let's take another look at the reasoning prompt.

Taking a closer look at the reasoning JSON you may notice the field names themselves are quite long.

By making them shorter and moving explanations to the comments we can generate fewer tokens.

This small change removed 19 output tokens. While with GPT-3.5 this may only result in a few millisecond improvement, with GPT-4 this could shave off up to a second.

You might imagine, however, how this can have quite a significant impact for larger model outputs.

We could go further and use single characters for the JSON fields, or put everything in an array, but this may start to hurt our response quality. The best way to know, once again, is through testing.

Let's review the optimizations we implemented for the customer service bot example:

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
{
  query:"[contextualized query]",
  retrieval:"[true/false - whether retrieval is required]"
}
```

Example 2 (jsx):
```jsx
1
2
3
4
{
  query:"[contextualized query]",
  retrieval:"[true/false - whether retrieval is required]"
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
{
  "message_is_conversation_continuation": "True", // <-
  "number_of_messages_in_conversation_so_far": "1", // <-
  "user_sentiment": "Aggravated", // <-
  "query_type": "Hardware Issue", // <-
  "response_tone": "Validating and solution-oriented", // <-
  "response_requirements": "Propose options for repair or replacement.", // <-
  "user_requesting_to_talk_to_human": "False", // <-
  "enough_information_in_context": "True", // <-
  "response": "..." // X -- benefits from GPT-4
}
```

Example 4 (jsx):
```jsx
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
{
  "message_is_conversation_continuation": "True", // <-
  "number_of_messages_in_conversation_so_far": "1", // <-
  "user_sentiment": "Aggravated", // <-
  "query_type": "Hardware Issue", // <-
  "response_tone": "Validating and solution-oriented", // <-
  "response_requirements": "Propose options for repair or replacement.", // <-
  "user_requesting_to_talk_to_human": "False", // <-
  "enough_information_in_context": "True", // <-
  "response": "..." // X -- benefits from GPT-4
}
```

---

## Retrieval

**URL:** https://platform.openai.com/docs/guides/retrieval

**Contents:**
- Retrieval
- Quickstart
- Semantic search
  - Performing semantic search
  - Query rewriting
  - Attribute filtering
  - Ranking
- Vector stores
  - Pricing
  - Vector store operations

The Retrieval API allows you to perform semantic search over your data, which is a technique that surfaces semantically similar results — even when they match few or no keywords. Retrieval is useful on its own, but is especially powerful when combined with our models to synthesize responses.

The Retrieval API is powered by vector stores, which serve as indices for your data. This guide will cover how to perform semantic search, and go into the details of vector stores.

Create vector store and upload files.

Send search query to get relevant results.

To learn how to use the results with our models, check out the synthesizing responses section.

Semantic search is a technique that leverages vector embeddings to surface semantically relevant results. Importantly, this includes results with few or no shared keywords, which classical search techniques might miss.

For example, let's look at potential results for "When did we go to the moon?":

(Jaccard used for keyword, cosine with text-embedding-3-small used for semantic.)

Notice how the most relevant result contains none of the words in the search query. This flexibility makes semantic search a very powerful technique for querying knowledge bases of any size.

Semantic search is powered by vector stores, which we cover in detail later in the guide. This section will focus on the mechanics of semantic search.

You can query a vector store using the search function and specifying a query in natural language. This will return a list of results, each with the relevant chunks, similarity scores, and file of origin.

A response will contain 10 results maximum by default, but you can set up to 50 using the max_num_results param.

Certain query styles yield better results, so we've provided a setting to automatically rewrite your queries for optimal performance. Enable this feature by setting rewrite_query=true when performing a search.

The rewritten query will be available in the result's search_query field.

Attribute filtering helps narrow down results by applying criteria, such as restricting searches to a specific date range. You can define and combine criteria in attribute_filter to target files based on their attributes before performing semantic search.

Use comparison filters to compare a specific key in a file's attributes with a given value, and compound filters to combine multiple filters using and and or.

Below are some example filters.

If you find that your file search results are not sufficiently relevant, you can adjust the ranking_options to improve the quality of responses. This includes specifying a ranker, such as auto or default-2024-08-21, and setting a score_threshold between 0.0 and 1.0. A higher score_threshold will limit the results to more relevant chunks, though it may exclude some potentially useful ones. When ranking_options.hybrid_search is provided you can also tune hybrid_search.embedding_weight (rrf_embedding_weight) and hybrid_search.text_weight (rrf_text_weight) to control how reciprocal rank fusion balances semantic embedding matches vs. sparse keyword matches. Increase the former to emphasize semantic similarity, increase the latter to emphasize textual overlap, and ensure at least one of the weights is greater than zero.

Vector stores are the containers that power semantic search for the Retrieval API and the file search tool. When you add a file to a vector store it will be automatically chunked, embedded, and indexed.

Vector stores contain vector_store_file objects, which are backed by a file object.

You will be charged based on the total storage used across all your vector stores, determined by the size of parsed chunks and their corresponding embeddings.

See expiration policies for options to minimize costs.

Some operations, like create for vector_store.file, are asynchronous and may take time to complete — use our helper functions, like create_and_poll to block until it is. Otherwise, you may check the status.

When creating a batch you can either provide file_ids with optional attributes and/or chunking_strategy, or use the files array to pass objects that include a file_id plus optional attributes and chunking_strategy for each file. The two options are mutually exclusive so that you can cleanly control whether every file shares the same settings or you need per-file overrides.

Each vector_store.file can have associated attributes, a dictionary of values that can be referenced when performing semantic search with attribute filtering. The dictionary can have at most 16 keys, with a limit of 256 characters each.

You can set an expiration policy on vector_store objects with expires_after. Once a vector store expires, all associated vector_store.file objects will be deleted and you'll no longer be charged for them.

The maximum file size is 512 MB. Each file should contain no more than 5,000,000 tokens per file (computed automatically when you attach a file).

By default, max_chunk_size_tokens is set to 800 and chunk_overlap_tokens is set to 400, meaning every file is indexed by being split up into 800-token chunks, with 400-token overlap between consecutive chunks.

You can adjust this by setting chunking_strategy when adding files to the vector store. There are certain limitations to chunking_strategy:

For text/ MIME types, the encoding must be one of utf-8, utf-16, or ascii.

After performing a query you may want to synthesize a response based on the results. You can leverage our models to do so, by supplying the results and original query, to get back a grounded response.

This uses a sample format_results function, which could be implemented like so:

**Examples:**

Example 1 (python):
```python
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
from openai import OpenAI
client = OpenAI()

vector_store = client.vector_stores.create(        # Create vector store
    name="Support FAQ",
)

client.vector_stores.files.upload_and_poll(        # Upload file
    vector_store_id=vector_store.id,
    file=open("customer_policies.txt", "rb")
)
```

Example 2 (python):
```python
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
from openai import OpenAI
client = OpenAI()

vector_store = client.vector_stores.create(        # Create vector store
    name="Support FAQ",
)

client.vector_stores.files.upload_and_poll(        # Upload file
    vector_store_id=vector_store.id,
    file=open("customer_policies.txt", "rb")
)
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
```

Example 4 (python):
```python
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
import OpenAI from "openai";
const client = new OpenAI();

const vector_store = await client.vectorStores.create({   // Create vector store
    name: "Support FAQ",
});

await client.vector_stores.files.upload_and_poll({         // Upload file
    vector_store_id: vector_store.id,
    file: fs.createReadStream("customer_policies.txt"),
});
```

---

## Video generation with Sora

**URL:** https://platform.openai.com/docs/guides/video-generation?gallery=open&galleryItem=maui

**Contents:**
- Video generation with Sora
- Overview
- Models
  - Sora 2
  - Sora 2 Pro
- Generate a video
  - Start a render job
  - Guardrails and restrictions
  - Effective prompting
  - Monitor progress

Sora is OpenAI’s newest frontier in generative media – a state-of-the-art video model capable of creating richly detailed, dynamic clips with audio from natural language or images. Built on years of research into multimodal diffusion and trained on diverse visual data, Sora brings a deep understanding of 3D space, motion, and scene continuity to text-to-video generation.

The Video API (in preview) exposes these capabilities to developers for the first time, enabling programmatic creation, extension, and remixing of videos. It provides five endpoints, each with distinct capabilities:

The second generation Sora model comes in two variants, each tailored for different use cases.

sora-2 is designed for speed and flexibility. It’s ideal for the exploration phase, when you’re experimenting with tone, structure, or visual style and need quick feedback rather than perfect fidelity.

It generates good quality results quickly, making it well suited for rapid iteration, concepting, and rough cuts. sora-2 is often more than sufficient for social media content, prototypes, and scenarios where turnaround time matters more than ultra-high fidelity.

sora-2-pro produces higher quality results. It’s the better choice when you need production-quality output.

sora-2-pro takes longer to render and is more expensive to run, but it produces more polished, stable results. It’s best for high-resolution cinematic footage, marketing assets, and any situation where visual precision is critical.

Generating a video is an asynchronous process:

When you call the POST /videos endpoint, the API returns a job object with a job id and an initial status.

You can either poll the GET /videos/{video_id} endpoint until the status transitions to completed, or – for a more efficient approach – use webhooks (see the webhooks section below) to be notified automatically when the job finishes.

Once the job has reached the completed state you can fetch the final MP4 file with GET /videos/{video_id}/content.

Start by calling POST /videos with a text prompt and the required parameters. The prompt defines the creative look and feel – subjects, camera, lighting, and motion – while parameters like size and seconds control the video's resolution and length.

The response is a JSON object with a unique id and an initial status such as queued or in_progress. This means the render job has started.

The API enforces several content restrictions:

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

For best results, describe shot type, subject, action, setting, and lighting. For example:

This level of specificity helps the model produce consistent results without inventing unwanted details. For more advanced prompting techniques, please refer to our dedicated Sora 2 prompting guide.

Video generation takes time. Depending on model, API load and resolution, a single render may take several minutes.

To manage this efficiently, you can poll the API to request status updates or you can get notified via a webhook.

Call GET /videos/{video_id} with the id returned from the create call. The response shows the job’s current status, progress percentage (if available), and any errors.

Typical states are queued, in_progress, completed, and failed. Poll at a reasonable interval (for example, every 10–20 seconds), use exponential backoff if necessary, and provide feedback to users that the job is still in progress.

Instead of polling job status repeatedly with GET, register a webhook to be notified automatically when a video generation completes or fails.

Webhooks can be configured in your webhook settings page. When a job finishes, the API emits one of two event types: video.completed and video.failed. Each event includes the ID of the job that triggered it.

Example webhook payload:

Once the job reaches status completed, fetch the MP4 with GET /videos/{video_id}/content. This endpoint streams the binary video data and returns standard content headers, so you can either save the file directly to disk or pipe it to cloud storage.

You now have the final video file ready for playback, editing, or distribution. Download URLs are valid for a maximum of 1 hour after generation. If you need long-term storage, copy the file to your own storage system promptly.

For each completed video, you can also download a thumbnail and a spritesheet. These are lightweight assets useful for previews, scrubbers, or catalog displays. Use the variant query parameter to specify what you want to download. The default is variant=video for the MP4.

You can guide a generation with an input image, which acts as the first frame of your video. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment. Include an image file as the input_reference parameter in your POST /videos request. The image must match the target video’s resolution (size).

Supported file formats are image/jpeg, image/png, and image/webp.

Remix lets you take an existing video and make targeted adjustments without regenerating everything from scratch. Provide the remix_video_id of a completed job along with a new prompt that describes the change, and the system reuses the original’s structure, continuity, and composition while applying the modification. This works best when you make a single, well-defined change because smaller, focused edits preserve more of the original fidelity and reduce the risk of introducing artifacts.

Remix is especially valuable for iteration because it lets you refine without discarding what already works. By constraining each remix to one clear adjustment, you keep the visual style, subject consistency, and camera framing stable, while still exploring variations in mood, palette, or staging. This makes it far easier to build polished sequences through small, reliable steps.

Use GET /videos to enumerate your videos. The endpoint supports optional query parameters for pagination and sorting.

Use DELETE /videos/{video_id} to remove videos you no longer need from OpenAI’s storage.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
```

Example 2 (javascript):
```javascript
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
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
```

Example 4 (python):
```python
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
from openai import OpenAI

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

---

## Prompt optimizer

**URL:** https://platform.openai.com/docs/guides/prompt-optimizer

**Contents:**
- Prompt optimizer
- Prepare your data
- Optimize your prompt
- Next steps

The prompt optimizer is a chat interface in the dashboard, where you enter a prompt, and we optimize it according to current best practices before returning it to you. Pairing the prompt optimizer with datasets is a powerful way to automatically improve prompts.

The prompt optimizer can use the following from your dataset to improve your prompt:

For effective results, add annotations containing a Good/Bad rating and detailed, specific critiques. Create graders that precisely capture the properties that you desire from your prompt.

Once you’ve prepared your dataset, create an optimization.

The effectiveness of prompt optimization depends on the quality of your graders. We recommend building narrowly-defined graders for each of the desired output properties where you see your prompt failing.

Always evaluate and manually review optimized prompts before using them in production. While the prompt optimizer generally provides a strict improvement in your prompt’s effectiveness, it's possible for the optimized prompt to perform worse than your original on specific inputs.

For more inspiration, visit the OpenAI Cookbook, which contains example code and links to third-party resources, or learn more about our tools for evals:

Operate a flywheel of continuous improvement using evaluations.

Evaluate against external models, interact with evals via API, and more.

Build sophisticated graders to improve the effectiveness of your evals.

Improve a model's ability to generate responses tailored to your use case.

---

## Conversation state

**URL:** https://platform.openai.com/docs/guides/conversation-state

**Contents:**
- Conversation state
- Manually manage conversation state
- OpenAI APIs for conversation state
  - Using the Conversations API
  - Passing context from the previous response
- Managing the context window
  - Managing context for text generation
  - Compaction (advanced)
- Next steps

OpenAI provides a few ways to manage conversation state, which is important for preserving information across multiple messages or turns in a conversation.

While each text generation request is independent and stateless, you can still implement multi-turn conversations by providing additional messages as parameters to your text generation request. Consider a knock-knock joke:

By using alternating user and assistant messages, you capture the previous state of a conversation in one request to the model.

To manually share context across generated responses, include the model's previous response output as input, and append that input to your next request.

In the following example, we ask the model to tell a joke, followed by a request for another joke. Appending previous responses to new requests in this way helps ensure conversations feel natural and retain the context of previous interactions.

Our APIs make it easier to manage conversation state automatically, so you don't have to do pass inputs manually with each turn of a conversation.

The Conversations API works with the Responses API to persist conversation state as a long-running object with its own durable identifier. After creating a conversation object, you can keep using it across sessions, devices, or jobs.

Conversations store items, which can be messages, tool calls, tool outputs, and other data.

In a multi-turn interaction, you can pass the conversation into subsequent responses to persist state and share context across subsequent responses, rather than having to chain multiple response items together.

Another way to manage conversation state is to share context across generated responses with the previous_response_id parameter. This parameter lets you chain responses and create a threaded conversation.

In the following example, we ask the model to tell a joke. Separately, we ask the model to explain why it's funny, and the model has all necessary context to deliver a good response.

Response objects are saved for 30 days by default. They can be viewed in the dashboard logs page or retrieved via the API. You can disable this behavior by setting store to false when creating a Response.

Conversation objects and items in them are not subject to the 30 day TTL. Any response attached to a conversation will have its items persisted with no 30 day TTL.

OpenAI does not use data sent via API to train our models without your explicit consent—learn more.

Even when using previous_response_id, all previous input tokens for responses in the chain are billed as input tokens in the API.

Understanding context windows will help you successfully create threaded conversations and manage state across model interactions.

The context window is the maximum number of tokens that can be used in a single request. This max tokens number includes input, output, and reasoning tokens. To learn your model's context window, see model details.

As your inputs become more complex, or you include more turns in a conversation, you'll need to consider both output token and context window limits. Model inputs and outputs are metered in tokens, which are parsed from inputs to analyze their content and intent and assembled to render logical outputs. Models have limits on token usage during the lifecycle of a text generation request.

If you create a very large prompt—often by including extra context, data, or examples for the model—you run the risk of exceeding the allocated context window for a model, which might result in truncated outputs.

Use the tokenizer tool, built with the tiktoken library, to see how many tokens are in a particular string of text.

For example, when making an API request to the Responses API with a reasoning enabled model, like the o1 model, the following token counts will apply toward the context window total:

Tokens generated in excess of the context window limit may be truncated in API responses.

You can estimate the number of tokens your messages will use with the tokenizer tool.

For long-running conversations with the Responses API, you can use the /responses/compact endpoint to shrink the context you send with each turn.

Instructions (optional)

The instructions field lets you include a system-style message that applies only to the compaction request. We recommend using this field only if you also supply instructions when creating responses, and ensuring that the same instructions are passed to both the Responses and Compact endpoints.

For more specific examples and use cases, visit the OpenAI Cookbook, or learn more about using the APIs to extend model capabilities:

**Examples:**

Example 1 (python):
```python
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
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4o-mini",
    input: [
        { role: "user", content: "knock knock." },
        { role: "assistant", content: "Who's there?" },
        { role: "user", content: "Orange." },
    ],
});

console.log(response.output_text);
```

Example 2 (javascript):
```javascript
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
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4o-mini",
    input: [
        { role: "user", content: "knock knock." },
        { role: "assistant", content: "Who's there?" },
        { role: "user", content: "Orange." },
    ],
});

console.log(response.output_text);
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
14
```

Example 4 (python):
```python
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
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {"role": "user", "content": "knock knock."},
        {"role": "assistant", "content": "Who's there?"},
        {"role": "user", "content": "Orange."},
    ],
)

print(response.output_text)
```

---

## Structured model outputs

**URL:** https://platform.openai.com/docs/guides/structured-outputs

**Contents:**
- Structured model outputs
  - Supported models
- When to use Structured Outputs via function calling vs via text.format
  - Structured Outputs vs JSON mode
- Examples
  - Chain of thought
    - Example response
  - Structured data extraction
    - Example response
  - UI Generation

JSON is one of the most widely used formats in the world for applications to exchange data.

Structured Outputs is a feature that ensures the model will always generate responses that adhere to your supplied JSON Schema, so you don't need to worry about the model omitting a required key, or hallucinating an invalid enum value.

Some benefits of Structured Outputs include:

In addition to supporting JSON Schema in the REST API, the OpenAI SDKs for Python and JavaScript also make it easy to define object schemas using Pydantic and Zod respectively. Below, you can see how to extract information from unstructured text that conforms to a schema defined in code.

Structured Outputs is available in our latest large language models, starting with GPT-4o. Older models like gpt-4-turbo and earlier may use JSON mode instead.

When to use Structured Outputs via function calling vs via text.format

Structured Outputs is available in two forms in the OpenAI API:

Function calling is useful when you are building an application that bridges the models and functionality of your application.

For example, you can give the model access to functions that query a database in order to build an AI assistant that can help users with their orders, or functions that can interact with the UI.

Conversely, Structured Outputs via response_format are more suitable when you want to indicate a structured schema for use when the model responds to the user, rather than when the model calls a tool.

For example, if you are building a math tutoring application, you might want the assistant to respond to your user using a specific JSON Schema so that you can generate a UI that displays different parts of the model's output in distinct ways.

The remainder of this guide will focus on non-function calling use cases in the Responses API. To learn more about how to use Structured Outputs with function calling, check out the

Structured Outputs is the evolution of JSON mode. While both ensure valid JSON is produced, only Structured Outputs ensure schema adherence. Both Structured Outputs and JSON mode are supported in the Responses API, Chat Completions API, Assistants API, Fine-tuning API and Batch API.

We recommend always using Structured Outputs instead of JSON mode when possible.

However, Structured Outputs with response_format: {type: "json_schema", ...} is only supported with the gpt-4o-mini, gpt-4o-mini-2024-07-18, and gpt-4o-2024-08-06 model snapshots and later.

You can ask the model to output an answer in a structured, step-by-step way, to guide the user through the solution.

You can define structured fields to extract from unstructured input data, such as research papers.

You can generate valid HTML by representing it as recursive data structures with constraints, like enums.

You can classify inputs on multiple categories, which is a common way of doing moderation.

First you must design the JSON Schema that the model should be constrained to follow. See the examples at the top of this guide for reference.

While Structured Outputs supports much of JSON Schema, some features are unavailable either for performance or technical reasons. See here for more details.

To maximize the quality of model generations, we recommend the following:

To use Structured Outputs, simply specify

Note: the first request you make with any schema will have additional latency as our API processes the schema, but subsequent requests with the same schema will not have additional latency.

In some cases, the model might not generate a valid response that matches the provided JSON schema.

This can happen in the case of a refusal, if the model refuses to answer for safety reasons, or if for example you reach a max tokens limit and the response is incomplete.

Refusals with Structured Outputs

When using Structured Outputs with user-generated input, OpenAI models may occasionally refuse to fulfill the request for safety reasons. Since a refusal does not necessarily follow the schema you have supplied in response_format, the API response will include a new field called refusal to indicate that the model refused to fulfill the request.

When the refusal property appears in your output object, you might present the refusal in your UI, or include conditional logic in code that consumes the response to handle the case of a refused request.

The API response from a refusal will look something like this:

Tips and best practices

If your application is using user-generated input, make sure your prompt includes instructions on how to handle situations where the input cannot result in a valid response.

The model will always try to adhere to the provided schema, which can result in hallucinations if the input is completely unrelated to the schema.

You could include language in your prompt to specify that you want to return empty parameters, or a specific sentence, if the model detects that the input is incompatible with the task.

Structured Outputs can still contain mistakes. If you see mistakes, try adjusting your instructions, providing examples in the system instructions, or splitting tasks into simpler subtasks. Refer to the prompt engineering guide for more guidance on how to tweak your inputs.

To prevent your JSON Schema and corresponding types in your programming language from diverging, we strongly recommend using the native Pydantic/zod sdk support.

If you prefer to specify the JSON schema directly, you could add CI rules that flag when either the JSON schema or underlying data objects are edited, or add a CI step that auto-generates the JSON Schema from type definitions (or vice-versa).

You can use streaming to process model responses or function call arguments as they are being generated, and parse them as structured data.

That way, you don't have to wait for the entire response to complete before handling it. This is particularly useful if you would like to display JSON fields one by one, or handle function call arguments as soon as they are available.

We recommend relying on the SDKs to handle streaming with Structured Outputs.

Structured Outputs supports a subset of the JSON Schema language.

The following types are supported for Structured Outputs:

In addition to specifying the type of a property, you can specify a selection of additional constraints:

Supported string properties:

Supported number properties:

Supported array properties:

Here are some examples on how you can use these type restrictions:

Note these constraints are not yet supported for fine-tuned models.

Note that the root level object of a schema must be an object, and not use anyOf. A pattern that appears in Zod (as one example) is using a discriminated union, which produces an anyOf at the top level. So code such as the following won't work:

To use Structured Outputs, all fields or function parameters must be specified as required.

Although all fields must be required (and the model will return a value for each parameter), it is possible to emulate an optional parameter by using a union type with null.

A schema may have up to 5000 object properties total, with up to 10 levels of nesting.

In a schema, total string length of all property names, definition names, enum values, and const values cannot exceed 120,000 characters.

A schema may have up to 1000 enum values across all enum properties.

For a single enum property with string values, the total string length of all enum values cannot exceed 15,000 characters when there are more than 250 enum values.

additionalProperties controls whether it is allowable for an object to contain additional keys / values that were not defined in the JSON Schema.

Structured Outputs only supports generating specified keys / values, so we require developers to set additionalProperties: false to opt into Structured Outputs.

When using Structured Outputs, outputs will be produced in the same order as the ordering of keys in the schema.

For fine-tuned models, we additionally do not support the following:

If you turn on Structured Outputs by supplying strict: true and call the API with an unsupported JSON Schema, you will receive an error.

Here's an example supported anyOf schema:

You can use definitions to define subschemas which are referenced throughout your schema. The following is a simple example.

Sample recursive schema using # to indicate root recursion.

Sample recursive schema using explicit recursion:

JSON mode is a more basic version of the Structured Outputs feature. While JSON mode ensures that model output is valid JSON, Structured Outputs reliably matches the model's output to the schema you specify. We recommend you use Structured Outputs if it is supported for your use case.

When JSON mode is turned on, the model's output is ensured to be valid JSON, except for in some edge cases that you should detect and handle appropriately.

To turn on JSON mode with the Responses API you can set the text.format to { "type": "json_object" }. If you are using function calling, JSON mode is always turned on.

To learn more about Structured Outputs, we recommend browsing the following resources:

**Examples:**

Example 1 (python):
```python
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
18
19
20
21
22
23
24
25
26
27
import OpenAI from "openai";
import { zodTextFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI();

const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const response = await openai.responses.parse({
  model: "gpt-4o-2024-08-06",
  input: [
    { role: "system", content: "Extract the event information." },
    {
      role: "user",
      content: "Alice and Bob are going to a science fair on Friday.",
    },
  ],
  text: {
    format: zodTextFormat(CalendarEvent, "event"),
  },
});

const event = response.output_parsed;
```

Example 2 (javascript):
```javascript
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
18
19
20
21
22
23
24
25
26
27
import OpenAI from "openai";
import { zodTextFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI();

const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const response = await openai.responses.parse({
  model: "gpt-4o-2024-08-06",
  input: [
    { role: "system", content: "Extract the event information." },
    {
      role: "user",
      content: "Alice and Bob are going to a science fair on Friday.",
    },
  ],
  text: {
    format: zodTextFormat(CalendarEvent, "event"),
  },
});

const event = response.output_parsed;
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
14
15
16
17
18
19
20
21
22
23
24
25
26
27
```

Example 4 (python):
```python
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
18
19
20
21
22
23
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text_format=CalendarEvent,
)

event = response.output_parsed
```

---

## Supported countries and territories

**URL:** https://platform.openai.com/docs/supported-countries

**Contents:**
- Supported countries and territories

Accessing or offering access to our services outside of the countries and territories listed below may result in your account being blocked or suspended.

---

## Libraries

**URL:** https://platform.openai.com/docs/libraries

**Contents:**
- Libraries
- Create and export an API key
- Install an official SDK
- Azure OpenAI libraries
- Community libraries
  - C# / .NET
  - C++
  - Clojure
  - Crystal
  - Dart/Flutter

This page covers setting up your local development environment to use the OpenAI API. You can use one of our officially supported SDKs, a community library, or your own preferred HTTP client.

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

Microsoft's Azure team maintains libraries that are compatible with both the OpenAI API and Azure OpenAI services. Read the library documentation below to learn how you can use them with the OpenAI API.

The libraries below are built and maintained by the broader developer community. You can also watch our OpenAPI specification repository on GitHub to get timely updates on when we make changes to our API.

Please note that OpenAI does not verify the correctness or security of these projects. Use them at your own risk!

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

## Structured model outputs

**URL:** https://platform.openai.com/docs/guides/structured-outputs?context=with_parse

**Contents:**
- Structured model outputs
  - Supported models
- When to use Structured Outputs via function calling vs via text.format
  - Structured Outputs vs JSON mode
- Examples
  - Chain of thought
    - Example response
  - Structured data extraction
    - Example response
  - UI Generation

JSON is one of the most widely used formats in the world for applications to exchange data.

Structured Outputs is a feature that ensures the model will always generate responses that adhere to your supplied JSON Schema, so you don't need to worry about the model omitting a required key, or hallucinating an invalid enum value.

Some benefits of Structured Outputs include:

In addition to supporting JSON Schema in the REST API, the OpenAI SDKs for Python and JavaScript also make it easy to define object schemas using Pydantic and Zod respectively. Below, you can see how to extract information from unstructured text that conforms to a schema defined in code.

Structured Outputs is available in our latest large language models, starting with GPT-4o. Older models like gpt-4-turbo and earlier may use JSON mode instead.

When to use Structured Outputs via function calling vs via text.format

Structured Outputs is available in two forms in the OpenAI API:

Function calling is useful when you are building an application that bridges the models and functionality of your application.

For example, you can give the model access to functions that query a database in order to build an AI assistant that can help users with their orders, or functions that can interact with the UI.

Conversely, Structured Outputs via response_format are more suitable when you want to indicate a structured schema for use when the model responds to the user, rather than when the model calls a tool.

For example, if you are building a math tutoring application, you might want the assistant to respond to your user using a specific JSON Schema so that you can generate a UI that displays different parts of the model's output in distinct ways.

The remainder of this guide will focus on non-function calling use cases in the Responses API. To learn more about how to use Structured Outputs with function calling, check out the

Structured Outputs is the evolution of JSON mode. While both ensure valid JSON is produced, only Structured Outputs ensure schema adherence. Both Structured Outputs and JSON mode are supported in the Responses API, Chat Completions API, Assistants API, Fine-tuning API and Batch API.

We recommend always using Structured Outputs instead of JSON mode when possible.

However, Structured Outputs with response_format: {type: "json_schema", ...} is only supported with the gpt-4o-mini, gpt-4o-mini-2024-07-18, and gpt-4o-2024-08-06 model snapshots and later.

You can ask the model to output an answer in a structured, step-by-step way, to guide the user through the solution.

You can define structured fields to extract from unstructured input data, such as research papers.

You can generate valid HTML by representing it as recursive data structures with constraints, like enums.

You can classify inputs on multiple categories, which is a common way of doing moderation.

First you must design the JSON Schema that the model should be constrained to follow. See the examples at the top of this guide for reference.

While Structured Outputs supports much of JSON Schema, some features are unavailable either for performance or technical reasons. See here for more details.

To maximize the quality of model generations, we recommend the following:

To use Structured Outputs, simply specify

Note: the first request you make with any schema will have additional latency as our API processes the schema, but subsequent requests with the same schema will not have additional latency.

In some cases, the model might not generate a valid response that matches the provided JSON schema.

This can happen in the case of a refusal, if the model refuses to answer for safety reasons, or if for example you reach a max tokens limit and the response is incomplete.

Refusals with Structured Outputs

When using Structured Outputs with user-generated input, OpenAI models may occasionally refuse to fulfill the request for safety reasons. Since a refusal does not necessarily follow the schema you have supplied in response_format, the API response will include a new field called refusal to indicate that the model refused to fulfill the request.

When the refusal property appears in your output object, you might present the refusal in your UI, or include conditional logic in code that consumes the response to handle the case of a refused request.

The API response from a refusal will look something like this:

Tips and best practices

If your application is using user-generated input, make sure your prompt includes instructions on how to handle situations where the input cannot result in a valid response.

The model will always try to adhere to the provided schema, which can result in hallucinations if the input is completely unrelated to the schema.

You could include language in your prompt to specify that you want to return empty parameters, or a specific sentence, if the model detects that the input is incompatible with the task.

Structured Outputs can still contain mistakes. If you see mistakes, try adjusting your instructions, providing examples in the system instructions, or splitting tasks into simpler subtasks. Refer to the prompt engineering guide for more guidance on how to tweak your inputs.

To prevent your JSON Schema and corresponding types in your programming language from diverging, we strongly recommend using the native Pydantic/zod sdk support.

If you prefer to specify the JSON schema directly, you could add CI rules that flag when either the JSON schema or underlying data objects are edited, or add a CI step that auto-generates the JSON Schema from type definitions (or vice-versa).

You can use streaming to process model responses or function call arguments as they are being generated, and parse them as structured data.

That way, you don't have to wait for the entire response to complete before handling it. This is particularly useful if you would like to display JSON fields one by one, or handle function call arguments as soon as they are available.

We recommend relying on the SDKs to handle streaming with Structured Outputs.

Structured Outputs supports a subset of the JSON Schema language.

The following types are supported for Structured Outputs:

In addition to specifying the type of a property, you can specify a selection of additional constraints:

Supported string properties:

Supported number properties:

Supported array properties:

Here are some examples on how you can use these type restrictions:

Note these constraints are not yet supported for fine-tuned models.

Note that the root level object of a schema must be an object, and not use anyOf. A pattern that appears in Zod (as one example) is using a discriminated union, which produces an anyOf at the top level. So code such as the following won't work:

To use Structured Outputs, all fields or function parameters must be specified as required.

Although all fields must be required (and the model will return a value for each parameter), it is possible to emulate an optional parameter by using a union type with null.

A schema may have up to 5000 object properties total, with up to 10 levels of nesting.

In a schema, total string length of all property names, definition names, enum values, and const values cannot exceed 120,000 characters.

A schema may have up to 1000 enum values across all enum properties.

For a single enum property with string values, the total string length of all enum values cannot exceed 15,000 characters when there are more than 250 enum values.

additionalProperties controls whether it is allowable for an object to contain additional keys / values that were not defined in the JSON Schema.

Structured Outputs only supports generating specified keys / values, so we require developers to set additionalProperties: false to opt into Structured Outputs.

When using Structured Outputs, outputs will be produced in the same order as the ordering of keys in the schema.

For fine-tuned models, we additionally do not support the following:

If you turn on Structured Outputs by supplying strict: true and call the API with an unsupported JSON Schema, you will receive an error.

Here's an example supported anyOf schema:

You can use definitions to define subschemas which are referenced throughout your schema. The following is a simple example.

Sample recursive schema using # to indicate root recursion.

Sample recursive schema using explicit recursion:

JSON mode is a more basic version of the Structured Outputs feature. While JSON mode ensures that model output is valid JSON, Structured Outputs reliably matches the model's output to the schema you specify. We recommend you use Structured Outputs if it is supported for your use case.

When JSON mode is turned on, the model's output is ensured to be valid JSON, except for in some edge cases that you should detect and handle appropriately.

To turn on JSON mode with the Responses API you can set the text.format to { "type": "json_object" }. If you are using function calling, JSON mode is always turned on.

To learn more about Structured Outputs, we recommend browsing the following resources:

**Examples:**

Example 1 (python):
```python
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
18
19
20
21
22
23
24
25
26
27
import OpenAI from "openai";
import { zodTextFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI();

const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const response = await openai.responses.parse({
  model: "gpt-4o-2024-08-06",
  input: [
    { role: "system", content: "Extract the event information." },
    {
      role: "user",
      content: "Alice and Bob are going to a science fair on Friday.",
    },
  ],
  text: {
    format: zodTextFormat(CalendarEvent, "event"),
  },
});

const event = response.output_parsed;
```

Example 2 (javascript):
```javascript
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
18
19
20
21
22
23
24
25
26
27
import OpenAI from "openai";
import { zodTextFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI();

const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const response = await openai.responses.parse({
  model: "gpt-4o-2024-08-06",
  input: [
    { role: "system", content: "Extract the event information." },
    {
      role: "user",
      content: "Alice and Bob are going to a science fair on Friday.",
    },
  ],
  text: {
    format: zodTextFormat(CalendarEvent, "event"),
  },
});

const event = response.output_parsed;
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
14
15
16
17
18
19
20
21
22
23
24
25
26
27
```

Example 4 (python):
```python
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
18
19
20
21
22
23
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text_format=CalendarEvent,
)

event = response.output_parsed
```

---

## Video generation with Sora

**URL:** https://platform.openai.com/docs/guides/video-generation?gallery=open&galleryItem=Space-Race

**Contents:**
- Video generation with Sora
- Overview
- Models
  - Sora 2
  - Sora 2 Pro
- Generate a video
  - Start a render job
  - Guardrails and restrictions
  - Effective prompting
  - Monitor progress

Sora is OpenAI’s newest frontier in generative media – a state-of-the-art video model capable of creating richly detailed, dynamic clips with audio from natural language or images. Built on years of research into multimodal diffusion and trained on diverse visual data, Sora brings a deep understanding of 3D space, motion, and scene continuity to text-to-video generation.

The Video API (in preview) exposes these capabilities to developers for the first time, enabling programmatic creation, extension, and remixing of videos. It provides five endpoints, each with distinct capabilities:

The second generation Sora model comes in two variants, each tailored for different use cases.

sora-2 is designed for speed and flexibility. It’s ideal for the exploration phase, when you’re experimenting with tone, structure, or visual style and need quick feedback rather than perfect fidelity.

It generates good quality results quickly, making it well suited for rapid iteration, concepting, and rough cuts. sora-2 is often more than sufficient for social media content, prototypes, and scenarios where turnaround time matters more than ultra-high fidelity.

sora-2-pro produces higher quality results. It’s the better choice when you need production-quality output.

sora-2-pro takes longer to render and is more expensive to run, but it produces more polished, stable results. It’s best for high-resolution cinematic footage, marketing assets, and any situation where visual precision is critical.

Generating a video is an asynchronous process:

When you call the POST /videos endpoint, the API returns a job object with a job id and an initial status.

You can either poll the GET /videos/{video_id} endpoint until the status transitions to completed, or – for a more efficient approach – use webhooks (see the webhooks section below) to be notified automatically when the job finishes.

Once the job has reached the completed state you can fetch the final MP4 file with GET /videos/{video_id}/content.

Start by calling POST /videos with a text prompt and the required parameters. The prompt defines the creative look and feel – subjects, camera, lighting, and motion – while parameters like size and seconds control the video's resolution and length.

The response is a JSON object with a unique id and an initial status such as queued or in_progress. This means the render job has started.

The API enforces several content restrictions:

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

For best results, describe shot type, subject, action, setting, and lighting. For example:

This level of specificity helps the model produce consistent results without inventing unwanted details. For more advanced prompting techniques, please refer to our dedicated Sora 2 prompting guide.

Video generation takes time. Depending on model, API load and resolution, a single render may take several minutes.

To manage this efficiently, you can poll the API to request status updates or you can get notified via a webhook.

Call GET /videos/{video_id} with the id returned from the create call. The response shows the job’s current status, progress percentage (if available), and any errors.

Typical states are queued, in_progress, completed, and failed. Poll at a reasonable interval (for example, every 10–20 seconds), use exponential backoff if necessary, and provide feedback to users that the job is still in progress.

Instead of polling job status repeatedly with GET, register a webhook to be notified automatically when a video generation completes or fails.

Webhooks can be configured in your webhook settings page. When a job finishes, the API emits one of two event types: video.completed and video.failed. Each event includes the ID of the job that triggered it.

Example webhook payload:

Once the job reaches status completed, fetch the MP4 with GET /videos/{video_id}/content. This endpoint streams the binary video data and returns standard content headers, so you can either save the file directly to disk or pipe it to cloud storage.

You now have the final video file ready for playback, editing, or distribution. Download URLs are valid for a maximum of 1 hour after generation. If you need long-term storage, copy the file to your own storage system promptly.

For each completed video, you can also download a thumbnail and a spritesheet. These are lightweight assets useful for previews, scrubbers, or catalog displays. Use the variant query parameter to specify what you want to download. The default is variant=video for the MP4.

You can guide a generation with an input image, which acts as the first frame of your video. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment. Include an image file as the input_reference parameter in your POST /videos request. The image must match the target video’s resolution (size).

Supported file formats are image/jpeg, image/png, and image/webp.

Remix lets you take an existing video and make targeted adjustments without regenerating everything from scratch. Provide the remix_video_id of a completed job along with a new prompt that describes the change, and the system reuses the original’s structure, continuity, and composition while applying the modification. This works best when you make a single, well-defined change because smaller, focused edits preserve more of the original fidelity and reduce the risk of introducing artifacts.

Remix is especially valuable for iteration because it lets you refine without discarding what already works. By constraining each remix to one clear adjustment, you keep the visual style, subject consistency, and camera framing stable, while still exploring variations in mood, palette, or staging. This makes it far easier to build polished sequences through small, reliable steps.

Use GET /videos to enumerate your videos. The endpoint supports optional query parameters for pagination and sorting.

Use DELETE /videos/{video_id} to remove videos you no longer need from OpenAI’s storage.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
```

Example 2 (javascript):
```javascript
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
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
```

Example 4 (python):
```python
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
from openai import OpenAI

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

---

## Prompting

**URL:** https://platform.openai.com/docs/guides/prompting

**Contents:**
- Prompting
- Overview
  - Prompts in the API
  - Prompting tools and techniques
- Create a prompt
- Refine your prompt
- Next steps

Prompting is the process of providing input to a model. The quality of your output often depends on how well you're able to prompt the model.

Prompting is both an art and a science. OpenAI has some strategies and API design decisions to help you construct strong prompts and get consistently good results from a model. We encourage you to experiment.

OpenAI provides a long-lived prompt object, with versioning and templating shared by all users in a project. This design lets you manage, test, and reuse prompts across your team, with one central definition across APIs, SDKs, and dashboard.

Universal prompt IDs give you flexibility to test and build. Variables and prompts share a base prompt, so when you create a new version, you can use that for evals and determine whether a prompt performs better or worse.

Log in and use the OpenAI dashboard to create, save, version, and share your prompts.

In the Playground, fill out the fields to create your desired prompt.

Variables let you inject dynamic values without changing your prompt. Use them in any message role using {{variable}}. For example, when creating a local weather prompt, you might add a city variable with the value San Francisco.

Use the prompt in your Responses API call

Find your prompt ID and version number in the URL, and pass it as prompt_id:

Create a new prompt version

Versions let you iterate on your prompts without overwriting existing details. You can use all versions in the API and evaluate their performance against each other. The prompt ID points to the latest published version unless you specify a version.

To create a new version, edit the prompt and click Update. You'll receive a new prompt ID to copy and use in your Responses API calls.

In the prompts dashboard, select the prompt you want to roll back. On the right, click History. Find the version you want to restore, and click Restore.

When you feel confident in your prompts, you might want to check out the following guides and resources.

Use the Playground to develop and iterate on prompts.

Learn how to prompt a model to generate text.

Learn about OpenAI's prompt engineering tools and techniques.

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
curl -s -X POST "https://api.openai.com/v1/responses" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
-d '{
    "prompt": {
    "prompt_id": "pmpt_123",
    "variables": {
        "city": "San Francisco"
    }
    }
}'
```

Example 2 (bash):
```bash
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
curl -s -X POST "https://api.openai.com/v1/responses" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
-d '{
    "prompt": {
    "prompt_id": "pmpt_123",
    "variables": {
        "city": "San Francisco"
    }
    }
}'
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
```

---

## Realtime API with SIP

**URL:** https://platform.openai.com/docs/guides/realtime-sip

**Contents:**
- Realtime API with SIP
- Overview
- Accept the call
- Reject the call
- Monitor call events
  - WebSocket request
  - Query parameters
  - Headers
- Redirect the call
- Hang up the call

SIP is a protocol used to make phone calls over the internet. With SIP and the Realtime API you can direct incoming phone calls to the API.

If you want to connect a phone number to the Realtime API, use a SIP trunking provider (e.g., Twilio). This is a service that converts your phone call to IP traffic. After you purchase a phone number from your SIP trunking provider, follow the instructions below.

Start by creating a webhook for incoming calls, through your platform.openai.com settings > Project > Webhooks. Then, point your SIP trunk at the OpenAI SIP endpoint, using the project ID for which you configured the webhook, e.g., sip:$PROJECT_ID@sip.api.openai.com;transport=tls. To find your $PROJECT_ID, visit settings > Project > General. That page will display the project ID, which will have a proj_ prefix.

When OpenAI receives SIP traffic associated with your project, your webhook will be fired. The event fired will be a realtime.call.incoming event, like the example below:

From this webhook, you can accept or reject the call, using the call_id value from the webhook. When accepting the call, you'll provide the needed configuration (instructions, voice, etc) for the Realtime API session. Once established, you can set up a WebSocket and monitor the session as usual. The APIs to accept, reject, monitor, refer, and hangup the call are documented below.

Use the Accept call endpoint to approve the inbound call and configure the realtime session that will answer it. Send the same parameters you would send in a create client secret request, i.e., ensure the realtime model, voice, tools, or instructions are set before bridging the call to the model.

The request path must include the call_id from the realtime.call.incoming webhook, and every request requires the Authorization header shown above. The endpoint returns 200 OK once the SIP leg is ringing and the realtime session is being established.

Use the Reject call endpoint to decline an invite when you do not want to handle the incoming call, (e.g., from an unsupported country code.) Supply the call_id path parameter and an optional SIP status_code (e.g., 486 to indicate "busy") in the JSON body to control the response sent back to the carrier.

If no status code is supplied the API uses 603 Decline by default. A successful request responds with 200 OK after OpenAI delivers the SIP response.

After you accept a call, open a WebSocket connection to the same session to stream events and issue realtime commands. Note that when connecting to an existing call using the call_id parameter, the model argument is not used (as it has already been configured via the accept endpoint).

GET wss://api.openai.com/v1/realtime?call_id={call_id}

The WebSocket behaves exactly like any other Realtime API connection. Send response.create, and other client events to control the call, and listen for server events to track progress. See Webhooks and server-side controls for more information.

Transfer an active call using the Refer call endpoint. Provide the call_id as well as the target_uri that should be placed in the SIP Refer-To header (for example tel:+14155550123 or sip:agent@example.com).

OpenAI returns 200 OK once the REFER is relayed to your SIP provider. The downstream system handles the rest of the call flow for the caller.

End the session with the Hang up endpoint when your application should disconnect the caller. This endpoint can be used to terminate both SIP and WebRTC realtime sessions.

The API responds with 200 OK when it starts tearing down the call.

The following is an example of a realtime.call.incoming handler. It accepts the call and then logs all the events from the Realtime API.

Now that you've connected over SIP, use the left navigation or click into these pages to start building your realtime application.

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
14
15
16
17
18
19
20
21
POST https://my_website.com/webhook_endpoint
user-agent: OpenAI/1.0 (+https://platform.openai.com/docs/webhooks)
content-type: application/json
webhook-id: wh_685342e6c53c8190a1be43f081506c52 # unique id for idempotency
webhook-timestamp: 1750287078 # timestamp of delivery attempt
webhook-signature: v1,K5oZfzN95Z9UVu1EsfQmfVNQhnkZ2pj9o9NDN/H/pI4= # signature to verify authenticity from OpenAI

{
  "object": "event",
  "id": "evt_685343a1381c819085d44c354e1b330e",
  "type": "realtime.call.incoming",
  "created_at": 1750287018, // Unix timestamp
  "data": {
    "call_id": "some_unique_id",
    "sip_headers": [
      { "name": "From", "value": "sip:+142555512112@sip.example.com" },
      { "name": "To", "value": "sip:+18005551212@sip.example.com" },
      { "name": "Call-ID", "value": "03782086-4ce9-44bf-8b0d-4e303d2cc590"}
    ]
  }
}
```

Example 2 (text):
```text
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
18
19
20
21
POST https://my_website.com/webhook_endpoint
user-agent: OpenAI/1.0 (+https://platform.openai.com/docs/webhooks)
content-type: application/json
webhook-id: wh_685342e6c53c8190a1be43f081506c52 # unique id for idempotency
webhook-timestamp: 1750287078 # timestamp of delivery attempt
webhook-signature: v1,K5oZfzN95Z9UVu1EsfQmfVNQhnkZ2pj9o9NDN/H/pI4= # signature to verify authenticity from OpenAI

{
  "object": "event",
  "id": "evt_685343a1381c819085d44c354e1b330e",
  "type": "realtime.call.incoming",
  "created_at": 1750287018, // Unix timestamp
  "data": {
    "call_id": "some_unique_id",
    "sip_headers": [
      { "name": "From", "value": "sip:+142555512112@sip.example.com" },
      { "name": "To", "value": "sip:+18005551212@sip.example.com" },
      { "name": "Call-ID", "value": "03782086-4ce9-44bf-8b0d-4e303d2cc590"}
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
14
15
16
17
18
19
20
21
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
curl -X POST "https://api.openai.com/v1/realtime/calls/$CALL_ID/accept" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "type": "realtime",
        "model": "gpt-realtime",
        "instructions": "You are Alex, a friendly concierge for Example Corp."
      }'
```

---

## Video generation with Sora

**URL:** https://platform.openai.com/docs/guides/video-generation?gallery=open&galleryItem=Sleeping-Otters

**Contents:**
- Video generation with Sora
- Overview
- Models
  - Sora 2
  - Sora 2 Pro
- Generate a video
  - Start a render job
  - Guardrails and restrictions
  - Effective prompting
  - Monitor progress

Sora is OpenAI’s newest frontier in generative media – a state-of-the-art video model capable of creating richly detailed, dynamic clips with audio from natural language or images. Built on years of research into multimodal diffusion and trained on diverse visual data, Sora brings a deep understanding of 3D space, motion, and scene continuity to text-to-video generation.

The Video API (in preview) exposes these capabilities to developers for the first time, enabling programmatic creation, extension, and remixing of videos. It provides five endpoints, each with distinct capabilities:

The second generation Sora model comes in two variants, each tailored for different use cases.

sora-2 is designed for speed and flexibility. It’s ideal for the exploration phase, when you’re experimenting with tone, structure, or visual style and need quick feedback rather than perfect fidelity.

It generates good quality results quickly, making it well suited for rapid iteration, concepting, and rough cuts. sora-2 is often more than sufficient for social media content, prototypes, and scenarios where turnaround time matters more than ultra-high fidelity.

sora-2-pro produces higher quality results. It’s the better choice when you need production-quality output.

sora-2-pro takes longer to render and is more expensive to run, but it produces more polished, stable results. It’s best for high-resolution cinematic footage, marketing assets, and any situation where visual precision is critical.

Generating a video is an asynchronous process:

When you call the POST /videos endpoint, the API returns a job object with a job id and an initial status.

You can either poll the GET /videos/{video_id} endpoint until the status transitions to completed, or – for a more efficient approach – use webhooks (see the webhooks section below) to be notified automatically when the job finishes.

Once the job has reached the completed state you can fetch the final MP4 file with GET /videos/{video_id}/content.

Start by calling POST /videos with a text prompt and the required parameters. The prompt defines the creative look and feel – subjects, camera, lighting, and motion – while parameters like size and seconds control the video's resolution and length.

The response is a JSON object with a unique id and an initial status such as queued or in_progress. This means the render job has started.

The API enforces several content restrictions:

Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

For best results, describe shot type, subject, action, setting, and lighting. For example:

This level of specificity helps the model produce consistent results without inventing unwanted details. For more advanced prompting techniques, please refer to our dedicated Sora 2 prompting guide.

Video generation takes time. Depending on model, API load and resolution, a single render may take several minutes.

To manage this efficiently, you can poll the API to request status updates or you can get notified via a webhook.

Call GET /videos/{video_id} with the id returned from the create call. The response shows the job’s current status, progress percentage (if available), and any errors.

Typical states are queued, in_progress, completed, and failed. Poll at a reasonable interval (for example, every 10–20 seconds), use exponential backoff if necessary, and provide feedback to users that the job is still in progress.

Instead of polling job status repeatedly with GET, register a webhook to be notified automatically when a video generation completes or fails.

Webhooks can be configured in your webhook settings page. When a job finishes, the API emits one of two event types: video.completed and video.failed. Each event includes the ID of the job that triggered it.

Example webhook payload:

Once the job reaches status completed, fetch the MP4 with GET /videos/{video_id}/content. This endpoint streams the binary video data and returns standard content headers, so you can either save the file directly to disk or pipe it to cloud storage.

You now have the final video file ready for playback, editing, or distribution. Download URLs are valid for a maximum of 1 hour after generation. If you need long-term storage, copy the file to your own storage system promptly.

For each completed video, you can also download a thumbnail and a spritesheet. These are lightweight assets useful for previews, scrubbers, or catalog displays. Use the variant query parameter to specify what you want to download. The default is variant=video for the MP4.

You can guide a generation with an input image, which acts as the first frame of your video. This is useful if you need the output video to preserve the look of a brand asset, a character, or a specific environment. Include an image file as the input_reference parameter in your POST /videos request. The image must match the target video’s resolution (size).

Supported file formats are image/jpeg, image/png, and image/webp.

Remix lets you take an existing video and make targeted adjustments without regenerating everything from scratch. Provide the remix_video_id of a completed job along with a new prompt that describes the change, and the system reuses the original’s structure, continuity, and composition while applying the modification. This works best when you make a single, well-defined change because smaller, focused edits preserve more of the original fidelity and reduce the risk of introducing artifacts.

Remix is especially valuable for iteration because it lets you refine without discarding what already works. By constraining each remix to one clear adjustment, you keep the visual style, subject consistency, and camera framing stable, while still exploring variations in mood, palette, or staging. This makes it far easier to build polished sequences through small, reliable steps.

Use GET /videos to enumerate your videos. The endpoint supports optional query parameters for pagination and sorting.

Use DELETE /videos/{video_id} to remove videos you no longer need from OpenAI’s storage.

**Examples:**

Example 1 (python):
```python
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
```

Example 2 (javascript):
```javascript
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
import OpenAI from 'openai';

const openai = new OpenAI();

let video = await openai.videos.create({
    model: 'sora-2',
    prompt: "A video of the words 'Thank you' in sparkling letters",
});

console.log('Video generation started: ', video);
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
```

Example 4 (python):
```python
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
from openai import OpenAI

openai = OpenAI()

video = openai.videos.create(
    model="sora-2",
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
```

---

## Webhooks

**URL:** https://platform.openai.com/docs/guides/webhooks

**Contents:**
- Webhooks
- Creating webhook endpoints
- Handling webhook requests on a server
  - Testing webhooks locally
- Verifying webhook signatures

OpenAI webhooks allow you to receive real-time notifications about events in the API, such as when a batch completes, a background response is generated, or a fine-tuning job finishes. Webhooks are delivered to an HTTP endpoint you control, following the Standard Webhooks specification. The full list of webhook events can be found in the API reference.

View the full list of webhook events.

Below are examples of simple servers capable of ingesting webhooks from OpenAI, specifically for the response.completed event.

To see a webhook like this one in action, you can set up a webhook endpoint in the OpenAI dashboard subscribed to response.completed, and then make an API request to generate a response in background mode.

You can also trigger test events with sample data from the webhook settings page.

In this guide, you will learn how to create webook endpoints in the dashboard, set up server-side code to handle them, and verify that inbound requests originated from OpenAI.

To start receiving webhook requests on your server, log in to the dashboard and open the webhook settings page. Webhooks are configured per-project.

Click the "Create" button to create a new webhook endpoint. You will configure three things:

After creating a new webhook, you'll receive a signing secret to use for server-side verification of incoming webhook requests. Save this value for later, since you won't be able to view it again.

With your webhook endpoint created, you'll next set up a server-side endpoint to handle those incoming event payloads.

When an event happens that you're subscribed to, your webhook URL will receive an HTTP POST request like this:

Your endpoint should respond quickly to these incoming HTTP requests with a successful (2xx) status code, indicating successful receipt. To avoid timeouts, we recommend offloading any non-trivial processing to a background worker so that the endpoint can respond immediately. If the endpoint doesn't return a successful (2xx) status code, or doesn't respond within a few seconds, the webhook request will be retried. OpenAI will continue to attempt delivery for up to 72 hours with exponential backoff. Note that 3xx redirects will not be followed; they are treated as failures and your endpoint should be updated to use the final destination URL.

In rare cases, due to internal system issues, OpenAI may deliver duplicate copies of the same webhook event. You can use the webhook-id header as an idempotency key to deduplicate.

Testing webhooks requires a URL that is available on the public Internet. This can make development tricky, since your local development environment likely isn't open to the public. A few options that may help:

While you can receive webhook events from OpenAI and process the results without any verification, you should verify that incoming requests are coming from OpenAI, especially if your webhook will take any kind of action on the backend. The headers sent along with webhook requests contain information that can be used in combination with a webhook secret key to verify that the webhook originated from OpenAI.

When you create a webhook endpoint in the OpenAI dashboard, you'll be given a signing secret that you should make available on your server as an environment variable:

The simplest way to verify webhook signatures is by using the unwrap() method of the official OpenAI SDK helpers:

Signatures can also be verified with the Standard Webhooks libraries:

Alternatively, if needed, you can implement your own signature verification as described in the Standard Webhooks spec

If you misplace or accidentally expose your signing secret, you can generate a new one by rotating the signing secret.

**Examples:**

Example 1 (python):
```python
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
18
19
20
21
22
23
24
25
import os
from openai import OpenAI, InvalidWebhookSignatureError
from flask import Flask, request, Response

app = Flask(__name__)
client = OpenAI(webhook_secret=os.environ["OPENAI_WEBHOOK_SECRET"])

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # with webhook_secret set above, unwrap will raise an error if the signature is invalid
        event = client.webhooks.unwrap(request.data, request.headers)

        if event.type == "response.completed":
            response_id = event.data.id
            response = client.responses.retrieve(response_id)
            print("Response output:", response.output_text)

        return Response(status=200)
    except InvalidWebhookSignatureError as e:
        print("Invalid signature", e)
        return Response("Invalid signature", status=400)

if __name__ == "__main__":
    app.run(port=8000)
```

Example 2 (python):
```python
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
18
19
20
21
22
23
24
25
import os
from openai import OpenAI, InvalidWebhookSignatureError
from flask import Flask, request, Response

app = Flask(__name__)
client = OpenAI(webhook_secret=os.environ["OPENAI_WEBHOOK_SECRET"])

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # with webhook_secret set above, unwrap will raise an error if the signature is invalid
        event = client.webhooks.unwrap(request.data, request.headers)

        if event.type == "response.completed":
            response_id = event.data.id
            response = client.responses.retrieve(response_id)
            print("Response output:", response.output_text)

        return Response(status=200)
    except InvalidWebhookSignatureError as e:
        print("Invalid signature", e)
        return Response("Invalid signature", status=400)

if __name__ == "__main__":
    app.run(port=8000)
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
14
15
16
17
18
19
20
21
22
23
24
25
```

Example 4 (python):
```python
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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
import OpenAI from "openai";
import express from "express";

const app = express();
const client = new OpenAI({ webhookSecret: process.env.OPENAI_WEBHOOK_SECRET });

// Don't use express.json() because signature verification needs the raw text body
app.use(express.text({ type: "application/json" }));

app.post("/webhook", async (req, res) => {
  try {
    const event = await client.webhooks.unwrap(req.body, req.headers);

    if (event.type === "response.completed") {
      const response_id = event.data.id;
      const response = await client.responses.retrieve(response_id);
      const output_text = response.output
        .filter((item) => item.type === "message")
        .flatMap((item) => item.content)
        .filter((contentItem) => contentItem.type === "output_text")
        .map((contentItem) => contentItem.text)
        .join("");

      console.log("Response output:", output_text);
    }
    res.status(200).send();
  } catch (error) {
    if (error instanceof OpenAI.InvalidWebhookSignatureError) {
      console.error("Invalid signature", error);
      res.status(400).send("Invalid signature");
    } else {
      throw error;
    }
  }
});

app.listen(8000, () => {
  console.log("Webhook server is running on port 8000");
});
```

---

## Pricing

**URL:** https://platform.openai.com/docs/pricing

**Contents:**
- Pricing
  - Text tokens
  - Image tokens
  - Audio tokens
  - Video
  - Fine-tuning
  - Built-in tools
  - AgentKit
  - Transcription and speech generation
    - Text tokens

For faster processing of API requests, try the priority processing service tier. For lower prices with higher latency, try the flex processing tier.

Large numbers of API requests which are not time-sensitive can use the Batch API for additional savings as well.

While reasoning tokens are not visible via the API, they still occupy space in the model's context window and are billed as output tokens.

For gpt-image-1.5, Text output tokens include model reasoning tokens.

Tokens used for model grading in reinforcement fine-tuning are billed at that model's per-token rate. Inference discounts are available if you enable data sharing when creating the fine-tune job. Learn more.

The tokens used for built-in tools are billed at the chosen model's per-token rates. GB refers to binary gigabytes of storage (also known as gibibyte), where 1GB is 2^30 bytes.

Web search: There are two components that contribute to the cost of using the web search tool: (1) tool calls and (2) search content tokens. Tool calls are billed per 1000 calls, according to the tool version and model type. The billing dashboard and invoices will report these line items as “web search tool calls.”

Search content tokens are tokens retrieved from the search index and fed to the model alongside your prompt to generate an answer. These are billed at the model’s input token rate, unless otherwise specified.

[1] For gpt-4o-mini and gpt-4.1-mini with the web search non-preview tool, search content tokens are charged as a fixed block of 8,000 input tokens per call.

Build, deploy, and optimize production-grade agents with Agent Builder, ChatKit, and Evals. You pay only for the compute and data you actually use.

Build, deploy, and optimize production-grade agents with Agent Builder, ChatKit, and Evals. You pay only for the compute and data you actually use.

Transcription and speech generation

Our omni-moderation models are made available free of charge ✌️

---
