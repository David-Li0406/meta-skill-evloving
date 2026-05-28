# Openai-Api - Vision

**Pages:** 6

---

## Images and vision

**URL:** https://platform.openai.com/docs/guides/images

**Contents:**
- Images and vision
- Overview
  - A tour of image-related use cases
- Generate or edit images
  - Using world knowledge for image generation
- Analyze images
  - Giving a model images as input
  - Image input requirements
  - Specify image input detail level
- Limitations

In this guide, you will learn about building applications involving images with the OpenAI API. If you know what you want to build, find your use case below to get started. If you're not sure where to start, continue reading to get an overview.

Recent language models can process image inputs and analyze them — a capability known as vision. With gpt-image-1, they can both analyze visual inputs and create images.

The OpenAI API offers several endpoints to process images as input or generate them as output, enabling you to build powerful multimodal applications.

To learn more about the input and output modalities supported by our models, refer to our models page.

You can generate or edit images using the Image API or the Responses API.

Our latest image generation model, gpt-image-1, is a natively multimodal large language model. It can understand text and images and leverage its broad world knowledge to generate images with better instruction following and contextual awareness.

In contrast, we also offer specialized image generation models - DALL·E 2 and 3 - which don't have the same inherent understanding of the world as GPT Image.

You can learn more about image generation in our Image generation guide.

The difference between DALL·E models and GPT Image is that a natively multimodal language model can use its visual understanding of the world to generate lifelike images including real-life details without a reference.

For example, if you prompt GPT Image to generate an image of a glass cabinet with the most popular semi-precious stones, the model knows enough to select gemstones like amethyst, rose quartz, jade, etc, and depict them in a realistic way.

Vision is the ability for a model to "see" and understand images. If there is text in an image, the model can also understand the text. It can understand most visual elements, including objects, shapes, colors, and textures, even if there are some limitations.

You can provide images as input to generation requests in multiple ways:

You can provide multiple images as input in a single request by including multiple images in the content array, but keep in mind that images count as tokens and will be billed accordingly.

Input images must meet the following requirements to be used in the API.

The detail parameter tells the model what level of detail to use when processing and understanding the image (low, high, or auto to let the model decide). If you skip the parameter, the model will use auto.

You can save tokens and speed up responses by using "detail": "low". This lets the model process the image with a budget of 85 tokens. The model receives a low-resolution 512px x 512px version of the image. This is fine if your use case doesn't require the model to see with high-resolution detail (for example, if you're asking about the dominant shape or color in the image).

On the other hand, you can use "detail": "high" if you want the model to have a better understanding of the image.

Read more about calculating image processing costs in the Calculating costs section below.

While models with vision capabilities are powerful and can be used in many situations, it's important to understand the limitations of these models. Here are some known limitations:

Image inputs are metered and charged in tokens, just as text inputs are. How images are converted to text token inputs varies based on the model. You can find a vision pricing calculator in the FAQ section of the pricing page.

Image inputs are metered and charged in tokens based on their dimensions. The token cost of an image is determined as follows:

A. Calculate the number of 32px x 32px patches that are needed to fully cover the image (a patch may extend beyond the image boundaries; out-of-bounds pixels are treated as black.)

B. If the number of patches exceeds 1536, we scale down the image so that it can be covered by no more than 1536 patches

C. The token cost is the number of patches, capped at a maximum of 1536 tokens

D. Apply a multiplier based on the model to get the total tokens.

Cost calculation examples

The token cost of an image is determined by two factors: size and detail.

Any image with "detail": "low" costs a set, base number of tokens. This amount varies by model (see chart below). To calculate the cost of an image with "detail": "high", we do the following:

Cost calculation examples (for gpt-4o)

For GPT Image 1, we calculate the cost of an image input the same way as described above, except that we scale down the image so that the shortest side is 512px instead of 768px. The price depends on the dimensions of the image and the input fidelity.

When input fidelity is set to low, the base cost is 65 image tokens, and each tile costs 129 image tokens. When using high input fidelity, we add a set number of tokens based on the image's aspect ratio in addition to the image tokens described above.

To see pricing for image input tokens, refer to our pricing page.

We process images at the token level, so each image we process counts towards your tokens per minute (TPM) limit.

For the most precise and up-to-date estimates for image processing, please use our image pricing calculator available here.

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
import OpenAI from "openai";
const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1-mini",
    input: "Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools: [{type: "image_generation"}],
});

// Save the image to a file
const imageData = response.output
  .filter((output) => output.type === "image_generation_call")
  .map((output) => output.result);

if (imageData.length > 0) {
  const imageBase64 = imageData[0];
  const fs = await import("fs");
  fs.writeFileSync("cat_and_otter.png", Buffer.from(imageBase64, "base64"));
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
18
19
import OpenAI from "openai";
const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1-mini",
    input: "Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools: [{type: "image_generation"}],
});

// Save the image to a file
const imageData = response.output
  .filter((output) => output.type === "image_generation_call")
  .map((output) => output.result);

if (imageData.length > 0) {
  const imageBase64 = imageData[0];
  const fs = await import("fs");
  fs.writeFileSync("cat_and_otter.png", Buffer.from(imageBase64, "base64"));
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
from openai import OpenAI
import base64

client = OpenAI() 

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools=[{"type": "image_generation"}],
)

// Save the image to a file
image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]
    with open("cat_and_otter.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
```

---

## Vision fine-tuning

**URL:** https://platform.openai.com/docs/guides/vision-fine-tuning

**Contents:**
- Vision fine-tuning
- Data format
- Image data requirements
    - Size
    - Format
    - Content moderation policy
    - What to do if your images get skipped
- Best practices
    - Reducing training cost
    - Control image quality

Vision fine-tuning uses image inputs for supervised fine-tuning to improve the model's understanding of image inputs. This guide will take you through this subset of SFT, and outline some of the important considerations for fine-tuning with image inputs.

Provide image inputs for supervised fine-tuning to improve the model's understanding of image inputs.

Just as you can send one or many image inputs and create model responses based on them, you can include those same message types within your JSONL training data files. Images can be provided either as HTTP URLs or data URLs containing Base64-encoded images.

Here's an example of an image message on a line of your JSONL file. Below, the JSON object is expanded for readability, but typically this JSON would appear on a single line in your data file:

Uploading training data for vision fine-tuning follows the same process described here.

We scan your images before training to ensure that they comply with our usage policy. This may introduce latency in file validation before fine-tuning begins.

Images containing the following will be excluded from your dataset and not used for training:

Your images can get skipped during training for the following reasons:

If you set the detail parameter for an image to low, the image is resized to 512 by 512 pixels and is only represented by 85 tokens regardless of its size. This will reduce the cost of training. See here for more information.

To control the fidelity of image understanding, set the detail parameter of image_url to low, high, or auto for each image. This will also affect the number of tokens per image that the model sees during training time, and will affect the cost of training. See here for more information.

Before launching in production, review and follow the following safety information.

Once a fine-tuning job is completed, we assess the resulting model’s behavior across 13 distinct safety categories. Each category represents a critical area where AI outputs could potentially cause harm if not properly controlled.

Each category has a predefined pass threshold; if too many evaluated examples in a given category fail, OpenAI blocks the fine-tuned model from deployment. If your fine-tuned model does not pass the safety checks, OpenAI sends a message in the fine-tuning job explaining which categories don't meet the required thresholds. You can view the results in the moderation checks section of the fine-tuning job.

In addition to reviewing any failed safety checks in the fine-tuning job object, you can retrieve details about which categories failed by querying the fine-tuning API events endpoint. Look for events of type moderation_checks for details about category results and enforcement. This information can help you narrow down which categories to target for retraining and improvement. The model spec has rules and examples that can help identify areas for additional training data.

While these evaluations cover a broad range of safety categories, conduct your own evaluations of the fine-tuned model to ensure it's appropriate for your use case.

Now that you know the basics of vision fine-tuning, explore these other methods as well.

Fine-tune a model by providing correct outputs for sample inputs.

Fine-tune a model using direct preference optimization (DPO).

Fine-tune a reasoning model by grading its outputs.

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
27
{
  "messages": [
    {
      "role": "system",
      "content": "You are an assistant that identifies uncommon cheeses."
    },
    {
      "role": "user",
      "content": "What is this cheese?"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/3/36/Danbo_Cheese.jpg"
          }
        }
      ]
    },
    {
      "role": "assistant",
      "content": "Danbo"
    }
  ]
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
27
{
  "messages": [
    {
      "role": "system",
      "content": "You are an assistant that identifies uncommon cheeses."
    },
    {
      "role": "user",
      "content": "What is this cheese?"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/3/36/Danbo_Cheese.jpg"
          }
        }
      ]
    },
    {
      "role": "assistant",
      "content": "Danbo"
    }
  ]
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
27
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
{
  "type": "image_url",
  "image_url": {
    "url": "https://upload.wikimedia.org/wikipedia/commons/3/36/Danbo_Cheese.jpg",
    "detail": "low"
  }
}
```

---

## Images and vision

**URL:** https://platform.openai.com/docs/guides/images-vision

**Contents:**
- Images and vision
- Overview
  - A tour of image-related use cases
- Generate or edit images
  - Using world knowledge for image generation
- Analyze images
  - Giving a model images as input
  - Image input requirements
  - Specify image input detail level
- Limitations

In this guide, you will learn about building applications involving images with the OpenAI API. If you know what you want to build, find your use case below to get started. If you're not sure where to start, continue reading to get an overview.

Recent language models can process image inputs and analyze them — a capability known as vision. With gpt-image-1, they can both analyze visual inputs and create images.

The OpenAI API offers several endpoints to process images as input or generate them as output, enabling you to build powerful multimodal applications.

To learn more about the input and output modalities supported by our models, refer to our models page.

You can generate or edit images using the Image API or the Responses API.

Our latest image generation model, gpt-image-1, is a natively multimodal large language model. It can understand text and images and leverage its broad world knowledge to generate images with better instruction following and contextual awareness.

In contrast, we also offer specialized image generation models - DALL·E 2 and 3 - which don't have the same inherent understanding of the world as GPT Image.

You can learn more about image generation in our Image generation guide.

The difference between DALL·E models and GPT Image is that a natively multimodal language model can use its visual understanding of the world to generate lifelike images including real-life details without a reference.

For example, if you prompt GPT Image to generate an image of a glass cabinet with the most popular semi-precious stones, the model knows enough to select gemstones like amethyst, rose quartz, jade, etc, and depict them in a realistic way.

Vision is the ability for a model to "see" and understand images. If there is text in an image, the model can also understand the text. It can understand most visual elements, including objects, shapes, colors, and textures, even if there are some limitations.

You can provide images as input to generation requests in multiple ways:

You can provide multiple images as input in a single request by including multiple images in the content array, but keep in mind that images count as tokens and will be billed accordingly.

Input images must meet the following requirements to be used in the API.

The detail parameter tells the model what level of detail to use when processing and understanding the image (low, high, or auto to let the model decide). If you skip the parameter, the model will use auto.

You can save tokens and speed up responses by using "detail": "low". This lets the model process the image with a budget of 85 tokens. The model receives a low-resolution 512px x 512px version of the image. This is fine if your use case doesn't require the model to see with high-resolution detail (for example, if you're asking about the dominant shape or color in the image).

On the other hand, you can use "detail": "high" if you want the model to have a better understanding of the image.

Read more about calculating image processing costs in the Calculating costs section below.

While models with vision capabilities are powerful and can be used in many situations, it's important to understand the limitations of these models. Here are some known limitations:

Image inputs are metered and charged in tokens, just as text inputs are. How images are converted to text token inputs varies based on the model. You can find a vision pricing calculator in the FAQ section of the pricing page.

Image inputs are metered and charged in tokens based on their dimensions. The token cost of an image is determined as follows:

A. Calculate the number of 32px x 32px patches that are needed to fully cover the image (a patch may extend beyond the image boundaries; out-of-bounds pixels are treated as black.)

B. If the number of patches exceeds 1536, we scale down the image so that it can be covered by no more than 1536 patches

C. The token cost is the number of patches, capped at a maximum of 1536 tokens

D. Apply a multiplier based on the model to get the total tokens.

Cost calculation examples

The token cost of an image is determined by two factors: size and detail.

Any image with "detail": "low" costs a set, base number of tokens. This amount varies by model (see chart below). To calculate the cost of an image with "detail": "high", we do the following:

Cost calculation examples (for gpt-4o)

For GPT Image 1, we calculate the cost of an image input the same way as described above, except that we scale down the image so that the shortest side is 512px instead of 768px. The price depends on the dimensions of the image and the input fidelity.

When input fidelity is set to low, the base cost is 65 image tokens, and each tile costs 129 image tokens. When using high input fidelity, we add a set number of tokens based on the image's aspect ratio in addition to the image tokens described above.

To see pricing for image input tokens, refer to our pricing page.

We process images at the token level, so each image we process counts towards your tokens per minute (TPM) limit.

For the most precise and up-to-date estimates for image processing, please use our image pricing calculator available here.

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
import OpenAI from "openai";
const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1-mini",
    input: "Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools: [{type: "image_generation"}],
});

// Save the image to a file
const imageData = response.output
  .filter((output) => output.type === "image_generation_call")
  .map((output) => output.result);

if (imageData.length > 0) {
  const imageBase64 = imageData[0];
  const fs = await import("fs");
  fs.writeFileSync("cat_and_otter.png", Buffer.from(imageBase64, "base64"));
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
18
19
import OpenAI from "openai";
const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1-mini",
    input: "Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools: [{type: "image_generation"}],
});

// Save the image to a file
const imageData = response.output
  .filter((output) => output.type === "image_generation_call")
  .map((output) => output.result);

if (imageData.length > 0) {
  const imageBase64 = imageData[0];
  const fs = await import("fs");
  fs.writeFileSync("cat_and_otter.png", Buffer.from(imageBase64, "base64"));
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
from openai import OpenAI
import base64

client = OpenAI() 

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools=[{"type": "image_generation"}],
)

// Save the image to a file
image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]
    with open("cat_and_otter.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/images-streaming

**Contents:**
- Image Streaming
- image_generation.partial_image
- image_generation.completed
- image_edit.partial_image
- image_edit.completed

Stream image generation and editing in real time with server-sent events. Learn more about image streaming.

Emitted when a partial image is available during image generation streaming.

Base64-encoded partial image data, suitable for rendering as an image.

The background setting for the requested image.

The Unix timestamp when the event was created.

The output format for the requested image.

0-based index for the partial image (streaming).

The quality setting for the requested image.

The size of the requested image.

The type of the event. Always image_generation.partial_image.

Emitted when image generation has completed and the final image is available.

Base64-encoded image data, suitable for rendering as an image.

The background setting for the generated image.

The Unix timestamp when the event was created.

The output format for the generated image.

The quality setting for the generated image.

The size of the generated image.

The type of the event. Always image_generation.completed.

For the GPT image models only, the token usage information for the image generation.

Emitted when a partial image is available during image editing streaming.

Base64-encoded partial image data, suitable for rendering as an image.

The background setting for the requested edited image.

The Unix timestamp when the event was created.

The output format for the requested edited image.

0-based index for the partial image (streaming).

The quality setting for the requested edited image.

The size of the requested edited image.

The type of the event. Always image_edit.partial_image.

Emitted when image editing has completed and the final image is available.

Base64-encoded final edited image data, suitable for rendering as an image.

The background setting for the edited image.

The Unix timestamp when the event was created.

The output format for the edited image.

The quality setting for the edited image.

The size of the edited image.

The type of the event. Always image_edit.completed.

For the GPT image models only, the token usage information for the image generation.

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
{
  "type": "image_generation.partial_image",
  "b64_json": "...",
  "created_at": 1620000000,
  "size": "1024x1024",
  "quality": "high",
  "background": "transparent",
  "output_format": "png",
  "partial_image_index": 0
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
{
  "type": "image_generation.partial_image",
  "b64_json": "...",
  "created_at": 1620000000,
  "size": "1024x1024",
  "quality": "high",
  "background": "transparent",
  "output_format": "png",
  "partial_image_index": 0
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
18
{
  "type": "image_generation.completed",
  "b64_json": "...",
  "created_at": 1620000000,
  "size": "1024x1024",
  "quality": "high",
  "background": "transparent",
  "output_format": "png",
  "usage": {
    "total_tokens": 100,
    "input_tokens": 50,
    "output_tokens": 50,
    "input_tokens_details": {
      "text_tokens": 10,
      "image_tokens": 40
    }
  }
}
```

---

## Image generation

**URL:** https://platform.openai.com/docs/guides/tools-image-generation

**Contents:**
- Image generation
- Usage
  - Tool options
  - Revised prompt
  - Prompting tips
- Multi-turn editing
- Streaming
- Supported models

The image generation tool allows you to generate images using a text prompt, and optionally image inputs. It leverages GPT Image models (gpt-image-1 and gpt-image-1-mini, and we're working on support for gpt-image-1.5), and automatically optimizes text inputs for improved performance.

To learn more about image generation, refer to our dedicated image generation guide.

When you include the image_generation tool in your request, the model can decide when and how to generate images as part of the conversation, using your prompt and any provided image inputs.

The image_generation_call tool call result will include a base64-encoded image.

You can provide input images using file IDs or base64 data.

To force the image generation tool call, you can set the parameter tool_choice to {"type": "image_generation"}.

You can configure the following output options as parameters for the image generation tool:

size, quality, and background support the auto option, where the model will automatically select the best option based on the prompt.

For more details on available options, refer to the image generation guide.

When using the image generation tool, the mainline model (e.g. gpt-4.1) will automatically revise your prompt for improved performance.

You can access the revised prompt in the revised_prompt field of the image generation call:

Image generation works best when you use terms like "draw" or "edit" in your prompt.

For example, if you want to combine images, instead of saying "combine" or "merge", you can say something like "edit the first image by adding this element from the second image".

You can iteratively edit images by referencing previous response or image IDs. This allows you to refine images across multiple turns in a conversation.

The image generation tool supports streaming partial images as the final result is being generated. This provides faster visual feedback for users and improves perceived latency.

You can set the number of partial images (1-3) with the partial_images parameter.

The image generation tool is supported for the following models:

The model used for the image generation process is always a GPT Image model (gpt-image-1.5, gpt-image-1, or gpt-image-1-mini), but these models can be used as the mainline model in the Responses API as they can reliably call the image generation tool when needed.

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
import OpenAI from "openai";
const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-5",
    input: "Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools: [{type: "image_generation"}],
});

// Save the image to a file
const imageData = response.output
  .filter((output) => output.type === "image_generation_call")
  .map((output) => output.result);

if (imageData.length > 0) {
  const imageBase64 = imageData[0];
  const fs = await import("fs");
  fs.writeFileSync("otter.png", Buffer.from(imageBase64, "base64"));
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
18
19
import OpenAI from "openai";
const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-5",
    input: "Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools: [{type: "image_generation"}],
});

// Save the image to a file
const imageData = response.output
  .filter((output) => output.type === "image_generation_call")
  .map((output) => output.result);

if (imageData.length > 0) {
  const imageBase64 = imageData[0];
  const fs = await import("fs");
  fs.writeFileSync("otter.png", Buffer.from(imageBase64, "base64"));
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
from openai import OpenAI
import base64

client = OpenAI() 

response = client.responses.create(
    model="gpt-5",
    input="Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools=[{"type": "image_generation"}],
)

# Save the image to a file
image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]
    
if image_data:
    image_base64 = image_data[0]
    with open("otter.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
```

---

## File inputs

**URL:** https://platform.openai.com/docs/guides/pdf-files

**Contents:**
- File inputs
- How it works
- File URLs
- Uploading files
- Base64-encoded files
- Usage considerations
- Next steps

OpenAI models with vision capabilities can also accept PDF files as input. Provide PDFs either as Base64-encoded data or as file IDs obtained after uploading files to the /v1/files endpoint through the API or dashboard.

To help models understand PDF content, we put into the model's context both the extracted text and an image of each page. The model can then use both the text and the images to generate a response. This is useful, for example, if diagrams contain key information that isn't in the text.

You can upload PDF file inputs by linking external URLs.

In the example below, we first upload a PDF using the Files API, then reference its file ID in an API request to the model.

You can also send PDF file inputs as Base64-encoded inputs.

Below are a few considerations to keep in mind while using PDF inputs.

To help models understand PDF content, we put into the model's context both extracted text and an image of each page—regardless of whether the page includes images. Before deploying your solution at scale, ensure you understand the pricing and token usage implications of using PDFs as input. More on pricing.

File size limitations

You can upload multiple files, each less than 50 MB. The total content limit across all files in a single API request is 50 MB.

Only models that support both text and image inputs, such as gpt-4o, gpt-4o-mini, or o1, can accept PDF files as input. Check model features here.

You can upload these files to the Files API with any purpose, but we recommend using the user_data purpose for files you plan to use as model inputs.

Now that you known the basics of text inputs and outputs, you might want to check out one of these resources next.

Use the Playground to develop and iterate on prompts with PDF inputs.

Check out the API reference for more options.

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
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-5",
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Analyze the letter and provide a summary of the key points."
                    },
                    {
                        "type": "input_file",
                        "file_url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf"
                    }
                ]
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
17
18
19
20
21
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-5",
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Analyze the letter and provide a summary of the key points."
                    },
                    {
                        "type": "input_file",
                        "file_url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf"
                    }
                ]
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
17
18
19
20
21
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
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-5",
    input: [
        {
            role: "user",
            content: [
                {
                    type: "input_text",
                    text: "Analyze the letter and provide a summary of the key points.",
                },
                {
                    type: "input_file",
                    file_url: "https://www.berkshirehathaway.com/letters/2024ltr.pdf",
                },
            ],
        },
    ],
});

console.log(response.output_text);
```

---
