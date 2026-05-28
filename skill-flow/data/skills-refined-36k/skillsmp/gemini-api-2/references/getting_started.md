# Gemini-Api - Getting Started

**Pages:** 6

---

## Authentication with OAuth quickstart

**URL:** https://ai.google.dev/gemini-api/docs/oauth

**Contents:**
- Authentication with OAuth quickstart
- Objectives
- Prerequisites
- Set up your cloud project
  - 1. Enable the API
  - 2. Configure the OAuth consent screen
  - 3. Authorize credentials for a desktop application
- Set up Application Default Credentials
  - Curl
  - Python

The easiest way to authenticate to the Gemini API is to configure an API key, as described in the Gemini API quickstart. If you need stricter access controls, you can use OAuth instead. This guide will help you set up authentication with OAuth.

This guide uses a simplified authentication approach that is appropriate for a testing environment. For a production environment, learn about authentication and authorization before choosing the access credentials that are appropriate for your app.

To run this quickstart, you need:

To complete this quickstart, you first need to setup your Cloud project.

Before using Google APIs, you need to turn them on in a Google Cloud project.

In the Google Cloud console, enable the Google Generative Language API.

Next configure the project's OAuth consent screen and add yourself as a test user. If you've already completed this step for your Cloud project, skip to the next section.

In the Google Cloud console, go to Menu > Google Auth platform > Overview.

Go to the Google Auth platform

Complete the project configuration form and set the user type to External in the Audience section.

Complete the rest of the form, accept the User Data Policy terms, and then click Create.

For now, you can skip adding scopes and click Save and Continue. In the future, when you create an app for use outside of your Google Workspace organization, you must add and verify the authorization scopes that your app requires.

To authenticate as an end user and access user data in your app, you need to create one or more OAuth 2.0 Client IDs. A client ID is used to identify a single app to Google's OAuth servers. If your app runs on multiple platforms, you must create a separate client ID for each platform.

In the Google Cloud console, go to Menu > Google Auth platform > Clients.

Click Application type > Desktop app.

In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.

Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.

Click OK. The newly created credential appears under OAuth 2.0 Client IDs.

Click the download button to save the JSON file. It will be saved as client_secret_<identifier>.json, and rename it to client_secret.json and move it to your working directory.

To convert the client_secret.json file into usable credentials, pass its location the gcloud auth application-default login command's --client-id-file argument.

The simplified project setup in this tutorial triggers a "Google hasn't verified this app." dialog. This is normal, choose "continue".

This places the resulting token in a well known location so it can be accessed by gcloud or the client libraries.

gcloud auth application-default login --no-browser --client-id-file=client_secret.json --scopes='https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/generative-language.retriever'

Once you have the Application Default Credentials (ADC) set, the client libraries in most languages need minimal to no help to find them.

The quickest way to test that this is working is to use it to access the REST API using curl:

In python the client libraries should find them automatically:

A minimal script to test it might be:

If that's working you're ready to try Semantic retrieval on your text data.

In many cases you won't have the gcloud command available to create the access token from the Client ID (client_secret.json). Google provides libraries in many languages to let you manage that process within your app. This section demonstrates the process, in python. There are equivalent examples of this sort of procedure, for other languages, available in the Drive API documentation

Install the Google client library for Python, and the Gemini client library.

To minimize the number of times you have to click through the authorization screens, create a file called load_creds.py in your working directory to caches a token.json file that it can reuse later, or refresh if it expires.

Start with the following code to convert the client_secret.json file to a token usable with genai.configure:

Now create your script.py:

In your working directory, run the sample:

The first time you run the script, it opens a browser window and prompts you to authorize access.

If you're not already signed in to your Google Account, you're prompted to sign in. If you're signed in to multiple accounts, be sure to select the account you set as a "Test Account" when configuring your project.

Authorization information is stored in the file system, so the next time you run the sample code, you aren't prompted for authorization.

You have successfully setup authentication.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-03 UTC.

**Examples:**

Example 1 (unknown):
```unknown
gcloud auth application-default login \
    --client-id-file=client_secret.json \
    --scopes='https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/generative-language.retriever'
```

Example 2 (unknown):
```unknown
gcloud auth application-default login \
    --client-id-file=client_secret.json \
    --scopes='https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/generative-language.retriever'
```

Example 3 (unknown):
```unknown
gcloud auth application-default login 
    --no-browser
    --client-id-file=client_secret.json 
    --scopes='https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/generative-language.retriever'
```

Example 4 (unknown):
```unknown
access_token=$(gcloud auth application-default print-access-token)
project_id=<MY PROJECT ID>
curl -X GET https://generativelanguage.googleapis.com/v1/models \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer ${access_token}" \
    -H "x-goog-user-project: ${project_id}" | grep '"name"'
```

---

## Gemini API libraries

**URL:** https://ai.google.dev/gemini-api/docs/libraries

**Contents:**
- Gemini API libraries
- Language support and installation
  - Python
  - JavaScript
  - Go
  - Java
  - C#
- General availability
- Legacy libraries and migration
- Prompt templates for code generation

When building with the Gemini API, we recommend using the Google GenAI SDK. These are the official, production-ready libraries that we develop and maintain for the most popular languages. They are in General Availability and used in all our official documentation and examples.

If you're new to the Gemini API, follow our quickstart guide to get started.

The Google GenAI SDK is available for the Python, JavaScript/TypeScript, Go and Java languages. You can install each language's library using package managers, or visit their GitHub repos for further engagement:

Library: google-genai

GitHub Repository: googleapis/python-genai

Installation: pip install google-genai

Library: @google/genai

GitHub Repository: googleapis/js-genai

Installation: npm install @google/genai

Library: google.golang.org/genai

GitHub Repository: googleapis/go-genai

Installation: go get google.golang.org/genai

Library: google-genai

GitHub Repository: googleapis/java-genai

Installation: If you're using Maven, add the following to your dependencies:

Library: Google.GenAI

GitHub Repository: googleapis/dotnet-genai

Installation: dotnet add package Google.GenAI

We started rolling out Google GenAI SDK, a new set of libraries to access Gemini API, in late 2024 when we launched Gemini 2.0.

As of May 2025, they reached General Availability (GA) across all supported platforms and are the recommended libraries to access the Gemini API. They are stable, fully supported for production use, and are actively maintained. They provide access to the latest features, and offer the best performance working with Gemini.

If you're using one of our legacy libraries, we strongly recommend you migrate so that you can access the latest features and get the best performance working with Gemini. Review the legacy libraries section for more information.

If you are using one of our legacy libraries, we recommend that you migrate to the new libraries.

The legacy libraries don't provide access to recent features (such as Live API and Veo) and are on a deprecation path. They will stop receiving updates on November 30th, 2025, the feature gaps will grow and potential bugs may no longer get fixed.

Each legacy library's support status varies, detailed in the following table:

Note for Java developers: There was no legacy Google-provided Java SDK for the Gemini API, so no migration from a previous Google library is required. You can start directly with the new library in the Language support and installation section.

Generative models (e.g., Gemini, Claude) and AI-powered IDEs (e.g., Cursor) may produce code for the Gemini API using outdated or deprecated libraries due to their training data cutoff. For the generated code to use the latest, recommended libraries, provide version and usage guidance directly in your prompts. You can use the templates below to provide the necessary context:

JavaScript/TypeScript

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-10 UTC.

**Examples:**

Example 1 (unknown):
```unknown
<dependencies>
  <dependency>
    <groupId>com.google.genai</groupId>
    <artifactId>google-genai</artifactId>
    <version>1.0.0</version>
  </dependency>
</dependencies>
```

Example 2 (unknown):
```unknown
<dependencies>
  <dependency>
    <groupId>com.google.genai</groupId>
    <artifactId>google-genai</artifactId>
    <version>1.0.0</version>
  </dependency>
</dependencies>
```

---

## Google AI Studio quickstart

**URL:** https://ai.google.dev/gemini-api/docs/ai-studio-quickstart

**Contents:**
- Google AI Studio quickstart
- Prompts and settings
- Chat prompt example: Build a custom chat application
  - Step 1 - Create a chat prompt
  - Step 2 - Teach your bot to chat better
  - Step 3 - Next steps
- Further reading

Google AI Studio lets you quickly try out models and experiment with different prompts. When you're ready to build, you can select "Get code" and your preferred programming language to use the Gemini API.

Google AI Studio provides several interfaces for prompts that are designed for different use cases. This guide covers Chat prompts, used to build conversational experiences. This prompting technique allows for multiple input and response turns to generate output. You can learn more with our chat prompt example below. Other options include Realtime streaming, Video gen, and more.

AI Studio also provides the Run settings panel, where you can make adjustments to model parameters, safety settings, and toggle-on tools like structured output, function calling, code execution, and grounding.

If you've used a general-purpose chatbot like Gemini, you've experienced first-hand how powerful generative AI models can be for open-ended dialog. While these general-purpose chatbots are useful, often they need to be tailored for particular use cases.

For example, maybe you want to build a customer service chatbot that only supports conversations that talk about a company's product. You might want to build a chatbot that speaks with a particular tone or style: a bot that cracks lots of jokes, rhymes like a poet, or uses lots of emoji in its answers.

This example shows you how to use Google AI Studio to build a friendly chatbot that communicates as if it is an alien living on one of Jupiter's moons, Europa.

To build a chatbot, you need to provide examples of interactions between a user and the chatbot to guide the model to provide the responses you're looking for.

To create a chat prompt:

Open Google AI Studio. Chat will be pre- selected on the left side options menu.

Click the assignment icon at the top of the Chat Prompt window to expand the System Instructions input field. Paste the following into the text input field:

After you've added the system instructions, start testing your application by chatting with the model:

In the text input boxed labeled Type something..., type in a question or observation that a user might make. For example:

Click the Run button to get a response from the chatbot. This response may be something like the following:

By providing a single instruction, you were able to build a basic Europa alien chatbot. However, a single instruction may not be enough to ensure consistency and quality in the model's responses. Without more specific instructions, the model's response to a question about the weather tends to be very long, and can take on a mind of its own.

Customize the tone of your chatbot by adding to the system instructions:

Start a new chat prompt, or use the same one. System instructions are modifiable after the chat session has started.

In the System Instructions section, change the instructions you already have to the following:

Re-enter your question (What's the weather like?) and click the Run button. If you didn't start a new chat, your response might look something like this:

You can use this approach to add additional depth to the chatbot. Ask more questions, edit the answers, and improve the quality of your chatbot. Continue to add or modify the instructions and test how they change your chatbot's behavior.

Similar to the other prompt types, once you have your prompt prototyped to your satisfaction, you can use the Get code button to start coding or save your prompt to work on later and share with others.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-22 UTC.

**Examples:**

Example 1 (unknown):
```unknown
You are an alien that lives on Europa, one of Jupiter's moons.
```

Example 2 (unknown):
```unknown
You are an alien that lives on Europa, one of Jupiter's moons.
```

Example 3 (unknown):
```unknown
What's the weather like?
```

Example 4 (unknown):
```unknown
What's the weather like?
```

---

## Gemini API quickstart

**URL:** https://ai.google.dev/gemini-api/docs/quickstart

**Contents:**
- Gemini API quickstart
- Before you begin
- Install the Google GenAI SDK
  - Python
  - JavaScript
  - Go
  - Java
  - C#
  - Apps Script
- Make your first request

This quickstart shows you how to install our libraries and make your first Gemini API request.

You need a Gemini API key. If you don't already have one, you can get it for free in Google AI Studio.

Using Python 3.9+, install the google-genai package using the following pip command:

Using Node.js v18+, install the Google Gen AI SDK for TypeScript and JavaScript using the following npm command:

Install google.golang.org/genai in your module directory using the go get command:

If you're using Maven, you can install google-genai by adding the following to your dependencies:

Install googleapis/go-genai in your module directory using the dotnet add command

Here is an example that uses the generateContent method to send a request to the Gemini API using the Gemini 2.5 Flash model.

If you set your API key as the environment variable GEMINI_API_KEY, it will be picked up automatically by the client when using the Gemini API libraries. Otherwise you will need to pass your API key as an argument when initializing the client.

Note that all code samples in the Gemini API docs assume that you have set the environment variable GEMINI_API_KEY.

Now that you made your first API request, you might want to explore the following guides that show Gemini in action:

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-10 UTC.

**Examples:**

Example 1 (unknown):
```unknown
pip install -q -U google-genai
```

Example 2 (unknown):
```unknown
pip install -q -U google-genai
```

Example 3 (unknown):
```unknown
npm install @google/genai
```

Example 4 (unknown):
```unknown
npm install @google/genai
```

---

## Gemini Robotics-ER 1.5

**URL:** https://ai.google.dev/gemini-api/docs/robotics-overview

**Contents:**
- Gemini Robotics-ER 1.5
- Safety
- Getting started: Finding objects in a scene
  - Python
  - REST
  - JSON
- How it works
  - Using the thinking budget with Gemini Robotics-ER 1.5
- Agentic capabilities for robotics
  - Pointing to objects

Gemini Robotics-ER 1.5 is a vision-language model (VLM) that brings Gemini's agentic capabilities to robotics. It's designed for advanced reasoning in the physical world, allowing robots to interpret complex visual data, perform spatial reasoning, and plan actions from natural language commands.

Key features and benefits:

This document describes what the model does and takes you through several examples that highlight the model's agentic capabilities.

If you want to jump right in, you can try out the model in Google AI Studio.

Try in Google AI Studio

While Gemini Robotics-ER 1.5 was built with safety in mind, it is your responsibility to maintain a safe environment around the robot. Generative AI models can make mistakes, and physical robots can cause damage. Safety is a priority, and making generative AI models safe when used with real-world robotics is an active and critical area of our research. To learn more, visit the Google DeepMind robotics safety page.

The following example demonstrates a common robotics use case. It shows how to pass an image and a text prompt to the model using the generateContent method to get a list of identified objects with their corresponding 2D points. The model returns points for items it identified in an image, returning their normalized 2D coordinates and labels.

You can use this output with a robotics API or call a vision-language-action (VLA) model or any other third-party user-defined functions to generate actions for a robot to perform.

The output will be a JSON array containing objects, each with a point (normalized [y, x] coordinates) and a label identifying the object.

The following image is an example of how these points can be displayed:

Gemini Robotics-ER 1.5 allows your robots to contextualize and work in the physical world using spatial understanding. It takes image/video/audio input and natural language prompts to:

This enables robots to "see" and "understand" their environment programmatically.

Gemini Robotics-ER 1.5 is also agentic, which means it can break down complex tasks (like "put the apple in the bowl") into sub-tasks to orchestrate long horizon tasks:

Read more about how function calling with Gemini works on the Function Calling page.

Gemini Robotics-ER 1.5 has a flexible thinking budget that gives you control over latency versus accuracy tradeoffs. For spatial understanding tasks like object detection, the model can achieve high performance with a small thinking budget. More complex reasoning tasks like counting and weight estimation benefit from a larger thinking budget. This lets you balance the need for low-latency responses with high-accuracy results for more challenging tasks.

To learn more about thinking budgets, see the Thinking core capabilities page.

This section walks through various capabilities of Gemini Robotics-ER 1.5, demonstrating how to use the model for robotic perception, reasoning, and planning applications.

The examples in this section demonstrate capabilities from pointing and finding objects in an image to planning trajectories and orchestrating long horizon tasks. For simplicity, the code snippets have been reduced to show the prompt and the call to generate_content API. The full runnable code as well as additional examples can be found in the Robotics cookbook.

Pointing and finding objects in images or video frames is a common use case for vision-and-language models (VLMs) in robotics. The following example asks the model to find specific objects within an image and return their coordinates in an image.

The output would be similar to the getting started example, a JSON containing the coordinates of the objects found and their labels.

Use the following prompt to request the model to interpret abstract categories like "fruit" instead of specific objects and locate all instances in the image.

Visit the image understanding page for other image processing techniques.

Gemini Robotics-ER 1.5 can also analyze video frames to track objects over time. See Video inputs for a list of supported video formats.

The following is the base prompt used to find specific objects in each frame that the model analyzes:

The output shows a pen and laptop being tracked across the video frames.

For the full runnable code, see the Robotics cookbook.

Beyond single points, the model can also return 2D bounding boxes, providing a rectangular region enclosing an object.

This example requests 2D bounding boxes for identifiable objects on a table. The model is instructed to limit the output to 25 objects and to name multiple instances uniquely.

The following displays the boxes returned from the model.

For the full runnable code, see the Robotics cookbook. The Image understanding page also has additional examples of visual tasks like segmentation and object detection.

Additional bounding box examples can be found in the Image understanding page.

Gemini Robotics-ER 1.5 can generate sequences of points that define a trajectory, useful for guiding robot movement.

This example requests a trajectory to move a red pen to an organizer, including the starting point and a series of intermediate points.

The response is a set of coordinates that describe the trajectory of the path that the red pen should follow to complete the task of moving it on top of the organizer:

Gemini Robotics-ER 1.5 can perform higher-level spatial reasoning, inferring actions or identifying optimal locations based on contextual understanding.

This example shows how Gemini Robotics-ER can reason about a space. The prompt asks the model to identify which object needs to be moved to create space for another item.

The response contains a 2D coordinate of the object that answers the user's question, in this case, the object that should move to make room for a laptop.

The model can also provide instructions for multi-step tasks and point to relevant objects for each step. This example shows how the model plans a series of steps to pack a lunch bag.

The response of this prompt is a set of step by step instructions on how to pack a lunch bag from the image input.

This example demonstrates task orchestration with a custom robot API. It introduces a mock API designed for a pick-and-place operation. The task is to pick up a blue block and place it in an orange bowl:

Similar to the other examples on this page, the full runnable code is available in the Robotics cookbook.

First step is to locate both of the items with the following prompt:

The model response includes the normalized coordinates of the block and the bowl:

This example uses the following mock robot API:

The next step is calling a sequence of API functions with the necessary logic to execute the action. The following prompt includes a description of the robot API that the model should use when orchestrating this task.

The following shows a possible output of the model based on the prompt and the mock robot API. The output includes the model thinking process and the tasks that it planned out as a result. It also shows the output of the robot function calls that the model sequenced together.

Gemini Robotics-ER 1.5 can suggest and execute Python code to perform tasks that require dynamic actions, such as zooming into an image region for better detail.

This example demonstrates how the model can suggest using the code execution tool to "zoom in" on a specific area of an image, which it then carries out to answer the user's question.

The following shows a possible model response for this task. The output shows the model generating code for zooming into the image to read the screen better. It also shows the thought process around the adjustments it made to the cropping. For the complete sample output, see the Robotics cookbook.

To optimize the performance and accuracy of your robotics applications, it's crucial to understand how to interact with the Gemini model effectively. This section outlines best practices and key strategies for crafting prompts, handling visual data, and structuring tasks to achieve the most reliable results.

Use clear and simple language.

Embrace natural language: The Gemini model is designed to comprehend natural, conversational language. Structure your prompts in a way that is semantically clear and mirrors how a person would naturally give instructions.

Use everyday terminology: Opt for common, everyday language over technical or specialized jargon. If the model is not responding as expected to a particular term, try rephrasing it with a more common synonym.

Optimize the visual input.

Zoom in for detail: When dealing with objects that are small or difficult to discern in a wider shot, use a bounding box function to isolate the object of interest. You can then crop the image to this selection and send the new, focused image to the model for a more detailed analysis.

Experiment with lighting and color: The model's perception can be affected by challenging lighting conditions and poor color contrast.

Break down complex problems into smaller steps. By addressing each smaller step individually, you can guide the model to a more precise and successful outcome.

Improve accuracy through consensus. For tasks that require a high degree of precision, you can query the model multiple times with the same prompt. By averaging the returned results, you can arrive at a "consensus" that is often more accurate and reliable.

Consider the following limitations when developing with Gemini Robotics-ER 1.5:

You acknowledge that the models referenced in this document (the "Robotics Models") leverage video and audio data in order to operate and move your hardware in accordance with your instructions. You therefore may operate the Robotics Models such that data from identifiable persons, such as voice, imagery, and likeness data ("Personal Data"), will be collected by the Robotics Models. If you elect to operate the Robotics Models in a manner that collects Personal Data, you agree that you will not permit any identifiable persons to interact with, or be present in the area surrounding, the Robotics Models, unless and until such identifiable persons have been sufficiently notified of and consented to the fact that their Personal Data may be provided to and used by Google as outlined in the Gemini API Additional Terms of Service found at https://ai.google.dev/gemini-api/terms (the "Terms"), including in accordance with the section entitled "How Google Uses Your Data". You will ensure that such notice permits the collection and use of Personal Data as outlined in the Terms, and you will use commercially reasonable efforts to minimize the collection and distribution of Personal Data by using techniques such as face blurring and operating the Robotics Models in areas not containing identifiable persons to the extent practicable.

For detailed information on pricing and available regions, refer to the pricing page.

Text, images, video, audio

Grounding with Google Maps

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-10-24 UTC.

**Examples:**

Example 1 (python):
```python
from google import genai
from google.genai import types

# Initialize the GenAI client and specify the model
MODEL_ID = "gemini-robotics-er-1.5-preview"
PROMPT = """
          Point to no more than 10 items in the image. The label returned
          should be an identifying name for the object detected.
          The answer should follow the json format: [{"point": <point>,
          "label": <label1>}, ...]. The points are in [y, x] format
          normalized to 0-1000.
        """
client = genai.Client(api_key=YOUR_API_KEY)

# Load your image
with open("my-image.png", 'rb') as f:
    image_bytes = f.read()

image_response = client.models.generate_content(
    model=MODEL_ID,
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/png',
        ),
        PROMPT
    ],
    config = types.GenerateContentConfig(
        temperature=0.5,
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
)

print(image_response.text)
```

Example 2 (python):
```python
from google import genai
from google.genai import types

# Initialize the GenAI client and specify the model
MODEL_ID = "gemini-robotics-er-1.5-preview"
PROMPT = """
          Point to no more than 10 items in the image. The label returned
          should be an identifying name for the object detected.
          The answer should follow the json format: [{"point": <point>,
          "label": <label1>}, ...]. The points are in [y, x] format
          normalized to 0-1000.
        """
client = genai.Client(api_key=YOUR_API_KEY)

# Load your image
with open("my-image.png", 'rb') as f:
    image_bytes = f.read()

image_response = client.models.generate_content(
    model=MODEL_ID,
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/png',
        ),
        PROMPT
    ],
    config = types.GenerateContentConfig(
        temperature=0.5,
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
)

print(image_response.text)
```

Example 3 (unknown):
```unknown
# First, ensure you have the image file locally.
# Encode the image to base64
IMAGE_BASE64=$(base64 -w 0 my-image.png)

curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-robotics-er-1.5-preview:generateContent \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "inlineData": {
              "mimeType": "image/png",
              "data": "'"${IMAGE_BASE64}"'"
            }
          },
          {
            "text": "Point to no more than 10 items in the image. The label returned should be an identifying name for the object detected. The answer should follow the json format: [{\"point\": [y, x], \"label\": <label1>}, ...]. The points are in [y, x] format normalized to 0-1000."
          }
        ]
      }
    ],
    "generationConfig": {
      "temperature": 0.5,
      "thinkingConfig": {
        "thinkingBudget": 0
      }
    }
  }'
```

Example 4 (unknown):
```unknown
# First, ensure you have the image file locally.
# Encode the image to base64
IMAGE_BASE64=$(base64 -w 0 my-image.png)

curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-robotics-er-1.5-preview:generateContent \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "inlineData": {
              "mimeType": "image/png",
              "data": "'"${IMAGE_BASE64}"'"
            }
          },
          {
            "text": "Point to no more than 10 items in the image. The label returned should be an identifying name for the object detected. The answer should follow the json format: [{\"point\": [y, x], \"label\": <label1>}, ...]. The points are in [y, x] format normalized to 0-1000."
          }
        ]
      }
    ],
    "generationConfig": {
      "temperature": 0.5,
      "thinkingConfig": {
        "thinkingBudget": 0
      }
    }
  }'
```

---

## Using Gemini API keys

**URL:** https://ai.google.dev/gemini-api/docs/api-key

**Contents:**
- Using Gemini API keys
- API Keys
- Google Cloud projects
  - Default project
- Import projects
- Limitations
- Setting the API key as an environment variable
  - Linux/macOS - Bash
  - macOS - Zsh
  - Windows

To use the Gemini API, you need an API key. This page outlines how to create and manage your keys in Google AI Studio as well as how to set up your environment to use them in your code.

Create or view a Gemini API Key

You can create and manage all your Gemini API Keys from the Google AI Studio API Keys page.

Once you have an API key, you have the following options to connect to the Gemini API:

For initial testing, you can hard code an API key, but this should only be temporary since it's not secure. You can find examples for hard coding the API key in Providing API key explicitly section.

Google Cloud projects are fundamental to using Google Cloud services (such as the Gemini API), managing billing, and controlling collaborators and permissions. Google AI Studio provides a lightweight interface to your Google Cloud projects.

If you don't have any projects created yet, you must either create a new project or import one from Google Cloud into Google AI Studio. The Projects page in Google AI Studio will display all keys that have sufficient permission to use the Gemini API. Refer to the import projects section for instructions.

For new users, after accepting Terms of Service, Google AI Studio creates a default Google Cloud Project and API Key, for ease of use. You can rename this project in Google AI Studio by navigating to Projects view in the Dashboard, clicking the 3 dots settings button next to a project and choosing Rename project. Existing users, or users who already have Google Cloud Accounts won't have a default project created.

Each Gemini API key is associated with a Google Cloud project. By default, Google AI Studio does not show all of your Cloud Projects. You must import the projects you want by searching for the name or project ID in the Import Projects dialog. To view a complete list of projects you have access to, visit the Cloud Console.

If you don't have any projects imported yet, follow these steps to import a Google Cloud project and create a key:

Once a project is imported, go to the API Keys page from the Dashboard menu and create an API key in the project you just imported.

The following are limitations of managing API keys and Google Cloud projects in Google AI Studio.

For additional management access to your projects, visit the Google Cloud Console.

If you set the environment variable GEMINI_API_KEY or GOOGLE_API_KEY, the API key will automatically be picked up by the client when using one of the Gemini API libraries. It's recommended that you set only one of those variables, but if both are set, GOOGLE_API_KEY takes precedence.

If you're using the REST API, or JavaScript on the browser, you will need to provide the API key explicitly.

Here is how you can set your API key locally as the environment variable GEMINI_API_KEY with different operating systems.

Bash is a common Linux and macOS terminal configuration. You can check if you have a configuration file for it by running the following command:

If the response is "No such file or directory", you will need to create this file and open it by running the following commands, or use zsh:

Next, you need to set your API key by adding the following export command:

After saving the file, apply the changes by running:

Zsh is a common Linux and macOS terminal configuration. You can check if you have a configuration file for it by running the following command:

If the response is "No such file or directory", you will need to create this file and open it by running the following commands, or use bash:

Next, you need to set your API key by adding the following export command:

After saving the file, apply the changes by running:

In some cases, you may want to explicitly provide an API key. For example:

Below are examples for how you can provide an API key explicitly:

Treat your Gemini API key like a password. If compromised, others can use your project's quota, incur charges (if billing is enabled), and access your private data, such as files.

Keep keys confidential: API keys for Gemini may access sensitive data your application depends upon.

Never commit API keys to source control. Do not check your API key into version control systems like Git.

Never expose API keys on the client-side. Do not use your API key directly in web or mobile apps in production. Keys in client-side code (including our JavaScript/TypeScript libraries and REST calls) can be extracted.

Restrict access: Restrict API key usage to specific IP addresses, HTTP referrers, or Android/iOS apps where possible.

Restrict usage: Enable only the necessary APIs for each key.

Perform regular audits: Regularly audit your API keys and rotate them periodically.

Use server-side calls with API keys The most secure way to use your API key is to call the Gemini API from a server-side application where the key can be kept confidential.

Use ephemeral tokens for client-side access (Live API only): For direct client-side access to the Live API, you can use ephemeral tokens. They come with lower security risks and can be suitable for production use. Review ephemeral tokens guide for more information.

Consider adding restrictions to your key: You can limit a key's permissions by adding API key restrictions. This minimizes the potential damage if the key is ever leaked.

For some general best practices, you can also review this support article.

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. For details, see the Google Developers Site Policies. Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-13 UTC.

**Examples:**

Example 1 (unknown):
```unknown
touch ~/.bashrc
open ~/.bashrc
```

Example 2 (unknown):
```unknown
touch ~/.bashrc
```

Example 3 (unknown):
```unknown
open ~/.bashrc
```

Example 4 (unknown):
```unknown
export GEMINI_API_KEY=<YOUR_API_KEY_HERE>
```

---
