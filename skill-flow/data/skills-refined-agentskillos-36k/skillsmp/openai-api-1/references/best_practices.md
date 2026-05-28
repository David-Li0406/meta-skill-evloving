# Openai-Api - Best Practices

**Pages:** 4

---

## Production best practices

**URL:** https://platform.openai.com/docs/guides/production-best-practices

**Contents:**
- Production best practices
- Setting up your organization
  - Managing billing limits
  - API keys
  - Staging projects
- Scaling your solution architecture
  - Managing rate limits
- Improving latencies
  - Common factors affecting latency and possible mitigation techniques
    - Model

This guide provides a comprehensive set of best practices to help you transition from prototype to production. Whether you are a seasoned machine learning engineer or a recent enthusiast, this guide should provide you with the tools you need to successfully put the platform to work in a production setting: from securing access to our API to designing a robust architecture that can handle high traffic volumes. Use this guide to help develop a plan for deploying your application as smoothly and effectively as possible.

If you want to explore best practices for going into production further, please check out our Developer Day talk:

Once you log in to your OpenAI account, you can find your organization name and ID in your organization settings. The organization name is the label for your organization, shown in user interfaces. The organization ID is the unique identifier for your organization which can be used in API requests.

Users who belong to multiple organizations can pass a header to specify which organization is used for an API request. Usage from these API requests will count against the specified organization's quota. If no header is provided, the default organization will be billed. You can change your default organization in your user settings.

You can invite new members to your organization from the Team page. Members can be readers or owners.

Once you’ve entered your billing information, you will have an approved usage limit of $100 per month, which is set by OpenAI. Your quota limit will automatically increase as your usage on your platform increases and you move from one usage tier to another. You can review your current usage limit in the limits page in your account settings.

If you’d like to be notified when your usage exceeds a certain dollar amount, you can set a notification threshold through the usage limits page.

The OpenAI API uses API keys for authentication. Visit your API keys page to retrieve the API key you'll use in your requests.

This is a relatively straightforward way to control access, but you must be vigilant about securing these keys. Avoid exposing the API keys in your code or in public repositories; instead, store them in a secure location. You should expose your keys to your application using environment variables or secret management service, so that you don't need to hard-code them in your codebase. Read more in our Best practices for API key safety.

API key usage can be monitored on the Usage page once tracking is enabled. If you are using an API key generated prior to Dec 20, 2023 tracking will not be enabled by default. You can enable tracking going forward on the API key management dashboard. All API keys generated past Dec 20, 2023 have tracking enabled. Any previous untracked usage will be displayed as Untracked in the dashboard.

As you scale, you may want to create separate projects for your staging and production environments. You can create these projects in the dashboard, allowing you to isolate your development and testing work, so you don't accidentally disrupt your live application. You can also limit user access to your production project, and set custom rate and spend limits per project.

When designing your application or service for production that uses our API, it's important to consider how you will scale to meet traffic demands. There are a few key areas you will need to consider regardless of the cloud service provider of your choice:

When using our API, it's important to understand and plan for rate limits.

Check out our most up-to-date guide on latency optimization.

Latency is the time it takes for a request to be processed and a response to be returned. In this section, we will discuss some factors that influence the latency of our text generation models and provide suggestions on how to reduce it.

The latency of a completion request is mostly influenced by two factors: the model and the number of tokens generated. The life cycle of a completion request looks like this:

The bulk of the latency typically arises from the token generation step.

Intuition: Prompt tokens add very little latency to completion calls. Time to generate completion tokens is much longer, as tokens are generated one at a time. Longer generation lengths will accumulate latency due to generation required for each token.

Now that we have looked at the basics of latency, let’s take a look at various factors that can affect latency, broadly ordered from most impactful to least impactful.

Our API offers different models with varying levels of complexity and generality. The most capable models, such as gpt-5, can generate more complex and diverse completions, but they also take longer to process your query. Models such as gpt-5-nano, can generate faster and cheaper Responses, but they may generate results that are less accurate or relevant for your query. You can choose the model that best suits your use case and the trade-off between speed, cost, and quality.

Requesting a large amount of generated tokens completions can lead to increased latencies:

If n and best_of both equal 1 (which is the default), the number of generated tokens will be at most, equal to max_tokens.

If n (the number of completions returned) or best_of (the number of completions generated for consideration) are set to > 1, each request will create multiple outputs. Here, you can consider the number of generated tokens as [ max_tokens * max (n, best_of) ]

Setting stream: true in a request makes the model start returning tokens as soon as they are available, instead of waiting for the full sequence of tokens to be generated. It does not change the time to get all the tokens, but it reduces the time for first token for an application where we want to show partial progress or are going to stop generations. This can be a better user experience and a UX improvement so it’s worth experimenting with streaming.

Depending on your use case, batching may help. If you are sending multiple requests to the same endpoint, you can batch the prompts to be sent in the same request. This will reduce the number of requests you need to make. The prompt parameter can hold up to 20 unique prompts. We advise you to test out this method and see if it helps. In some cases, you may end up increasing the number of generated tokens which will slow the response time.

To monitor your costs, you can set a notification threshold in your account to receive an email alert once you pass a certain usage threshold. Use the usage tracking dashboard to monitor your token usage during the current and past billing cycles.

One of the challenges of moving your prototype into production is budgeting for the costs associated with running your application. OpenAI offers a pay-as-you-go pricing model, with prices per 1,000 tokens (roughly equal to 750 words). To estimate your costs, you will need to project the token utilization. Consider factors such as traffic levels, the frequency with which users will interact with your application, and the amount of data you will be processing.

One useful framework for thinking about reducing costs is to consider costs as a function of the number of tokens and the cost per token. There are two potential avenues for reducing costs using this framework. First, you could work to reduce the cost per token by switching to smaller models for some tasks in order to reduce costs. Alternatively, you could try to reduce the number of tokens required. There are a few ways you could do this, such as by using shorter prompts, fine-tuning models, or caching common user queries so that they don't need to be processed repeatedly.

You can experiment with our interactive tokenizer tool to help you estimate costs. The API and playground also returns token counts as part of the response. Once you’ve got things working with our most capable model, you can see if the other models can produce the same results with lower latency and costs. Learn more in our token usage help article.

As you move your prototype into production, you may want to consider developing an MLOps strategy. MLOps (machine learning operations) refers to the process of managing the end-to-end life cycle of your machine learning models, including any models you may be fine-tuning using our API. There are a number of areas to consider when designing your MLOps strategy. These include

Thinking through these aspects of your application will help ensure your model stays relevant and performs well over time.

As you move your prototype into production, you will need to assess and address any security and compliance requirements that may apply to your application. This will involve examining the data you are handling, understanding how our API processes data, and determining what regulations you must adhere to. Our security practices and trust and compliance portal provide our most comprehensive and up-to-date documentation. For reference, here is our Privacy Policy and Terms of Use.

Some common areas you'll need to consider include data storage, data transmission, and data retention. You might also need to implement data privacy protections, such as encryption or anonymization where possible. In addition, you should follow best practices for secure coding, such as input sanitization and proper error handling.

When creating your application with our API, consider our safety best practices to ensure your application is safe and successful. These recommendations highlight the importance of testing the product extensively, being proactive about addressing potential issues, and limiting opportunities for misuse.

As projects using AI move from prototype to production, it is important to consider how to build a great product with AI and how that ties back to your core business. We certainly don't have all the answers but a great starting place is a talk from our Developer Day where we dive into this with some of our customers:

---

## Safety best practices

**URL:** https://platform.openai.com/docs/guides/safety-best-practices

**Contents:**
- Safety best practices
  - Use our free Moderation API
  - Adversarial testing
  - Human in the loop (HITL)
  - Prompt engineering
  - “Know your customer” (KYC)
  - Constrain user input and limit output tokens
  - Allow users to report issues
  - Understand and communicate limitations
  - Implement safety identifiers

OpenAI's Moderation API is free-to-use and can help reduce the frequency of unsafe content in your completions. Alternatively, you may wish to develop your own content filtration system tailored to your use case.

We recommend “red-teaming” your application to ensure it's robust to adversarial input. Test your product over a wide range of inputs and user behaviors, both a representative set and those reflective of someone trying to ‘break' your application. Does it wander off topic? Can someone easily redirect the feature via prompt injections, e.g. “ignore the previous instructions and do this instead”?

Wherever possible, we recommend having a human review outputs before they are used in practice. This is especially critical in high-stakes domains, and for code generation. Humans should be aware of the limitations of the system, and have access to any information needed to verify the outputs (for example, if the application summarizes notes, a human should have easy access to the original notes to refer back).

“Prompt engineering” can help constrain the topic and tone of output text. This reduces the chance of producing undesired content, even if a user tries to produce it. Providing additional context to the model (such as by giving a few high-quality examples of desired behavior prior to the new input) can make it easier to steer model outputs in desired directions.

Users should generally need to register and log-in to access your service. Linking this service to an existing account, such as a Gmail, LinkedIn, or Facebook log-in, may help, though may not be appropriate for all use-cases. Requiring a credit card or ID card reduces risk further.

Limiting the amount of text a user can input into the prompt helps avoid prompt injection. Limiting the number of output tokens helps reduce the chance of misuse.

Narrowing the ranges of inputs or outputs, especially drawn from trusted sources, reduces the extent of misuse possible within an application.

Allowing user inputs through validated dropdown fields (e.g., a list of movies on Wikipedia) can be more secure than allowing open-ended text inputs.

Returning outputs from a validated set of materials on the backend, where possible, can be safer than returning novel generated content (for instance, routing a customer query to the best-matching existing customer support article, rather than attempting to answer the query from-scratch).

Users should generally have an easily-available method for reporting improper functionality or other concerns about application behavior (listed email address, ticket submission method, etc). This method should be monitored by a human and responded to as appropriate.

From hallucinating inaccurate information, to offensive outputs, to bias, and much more, language models may not be suitable for every use case without significant modifications. Consider whether the model is fit for your purpose, and evaluate the performance of the API on a wide range of potential inputs in order to identify cases where the API's performance might drop. Consider your customer base and the range of inputs that they will be using, and ensure their expectations are calibrated appropriately.

Safety and security are very important to us at OpenAI.

If you notice any safety or security issues while developing with the API or anything else related to OpenAI, please submit it through our Coordinated Vulnerability Disclosure Program.

Sending safety identifiers in your requests can be a useful tool to help OpenAI monitor and detect abuse. This allows OpenAI to provide your team with more actionable feedback in the event that we detect any policy violations in your application.

A safety identifier should be a string that uniquely identifies each user. Hash the username or email address in order to avoid sending us any identifying information. If you offer a preview of your product to non-logged in users, you can send a session ID instead.

Include safety identifiers in your API requests with the safety_identifier parameter:

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

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": "This is a test"}
  ],
  max_tokens=5,
  safety_identifier="user_123456"
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

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": "This is a test"}
  ],
  max_tokens=5,
  safety_identifier="user_123456"
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
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
  "model": "gpt-4o-mini",
  "messages": [
    {"role": "user", "content": "This is a test"}
  ],
  "max_tokens": 5,
  "safety_identifier": "user123456"
}'
```

---

## Rate limits

**URL:** https://platform.openai.com/docs/guides/rate-limits

**Contents:**
- Rate limits
- Why do we have rate limits?
- How do these rate limits work?
- Usage tiers
  - Rate limits in headers
  - Fine-tuning rate limits
- Error mitigation
  - What are some steps I can take to mitigate this?
    - Retrying with exponential backoff
    - Reduce the max_tokens to match the size of your completions

Rate limits are restrictions that our API imposes on the number of times a user or client can access our services within a specified period of time.

Rate limits are a common practice for APIs, and they're put in place for a few different reasons:

Please work through this document in its entirety to better understand how OpenAI’s rate limit system works. We include code examples and possible solutions to handle common issues. We also include details around how your rate limits are automatically increased in the usage tiers section below.

Rate limits are measured in five ways: RPM (requests per minute), RPD (requests per day), TPM (tokens per minute), TPD (tokens per day), and IPM (images per minute). Rate limits can be hit across any of the options depending on what occurs first. For example, you might send 20 requests with only 100 tokens to the ChatCompletions endpoint and that would fill your limit (if your RPM was 20), even if you did not send 150k tokens (if your TPM limit was 150k) within those 20 requests.

Batch API queue limits are calculated based on the total number of input tokens queued for a given model. Tokens from pending batch jobs are counted against your queue limit. Once a batch job is completed, its tokens are no longer counted against that model's limit.

Other important things worth noting:

You can view the rate and usage limits for your organization under the limits section of your account settings. As your spend on our API goes up, we automatically graduate you to the next usage tier. This usually results in an increase in rate limits across most models.

To view a high-level summary of rate limits per model, visit the models page.

In addition to seeing your rate limit on your account page, you can also view important information about your rate limits such as the remaining requests, tokens, and other metadata in the headers of the HTTP response.

You can expect to see the following header fields:

The fine-tuning rate limits for your organization can be found in the dashboard as well, and can also be retrieved via API:

The OpenAI Cookbook has a Python notebook that explains how to avoid rate limit errors, as well an example Python script for staying under rate limits while batch processing API requests.

You should also exercise caution when providing programmatic access, bulk processing features, and automated social media posting - consider only enabling these for trusted customers.

To protect against automated and high-volume misuse, set a usage limit for individual users within a specified time frame (daily, weekly, or monthly). Consider implementing a hard cap or a manual review process for users who exceed the limit.

One easy way to avoid rate limit errors is to automatically retry requests with a random exponential backoff. Retrying with exponential backoff means performing a short sleep when a rate limit error is hit, then retrying the unsuccessful request. If the request is still unsuccessful, the sleep length is increased and the process is repeated. This continues until the request is successful or until a maximum number of retries is reached. This approach has many benefits:

Note that unsuccessful requests contribute to your per-minute limit, so continuously resending a request won’t work.

Below are a few example solutions for Python that use exponential backoff.

Tenacity is an Apache 2.0 licensed general-purpose retrying library, written in Python, to simplify the task of adding retry behavior to just about anything. To add exponential backoff to your requests, you can use the tenacity.retry decorator. The below example uses the tenacity.wait_random_exponential function to add random exponential backoff to a request.

Note that the Tenacity library is a third-party tool, and OpenAI makes no guarantees about its reliability or security.

Another python library that provides function decorators for backoff and retry is backoff:

Like Tenacity, the backoff library is a third-party tool, and OpenAI makes no guarantees about its reliability or security.

If you don't want to use third-party libraries, you can implement your own backoff logic following this example:

Again, OpenAI makes no guarantees on the security or efficiency of this solution but it can be a good starting place for your own solution.

Your rate limit is calculated as the maximum of max_tokens and the estimated number of tokens based on the character count of your request. Try to set the max_tokens value as close to your expected response size as possible.

If your use case does not require immediate responses, you can use the Batch API to more easily submit and execute large collections of requests without impacting your synchronous request rate limits.

For use cases that do requires synchronous responses, the OpenAI API has separate limits for requests per minute and tokens per minute.

If you're hitting the limit on requests per minute but have available capacity on tokens per minute, you can increase your throughput by batching multiple tasks into each request. This will allow you to process more tokens per minute, especially with our smaller models.

Sending in a batch of prompts works exactly the same as a normal API call, except you pass in a list of strings to the prompt parameter instead of a single string. Learn more in the Batch API guide.

**Examples:**

Example 1 (unknown):
```unknown
curl https://api.openai.com/v1/fine_tuning/model_limits \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

Example 2 (bash):
```bash
curl https://api.openai.com/v1/fine_tuning/model_limits \
  -H "Authorization: Bearer $OPENAI_API_KEY"
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
12
13
14
from openai import OpenAI
client = OpenAI()

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return client.completions.create(**kwargs)

completion_with_backoff(model="gpt-4o-mini", prompt="Once upon a time,")
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

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return client.completions.create(**kwargs)

completion_with_backoff(model="gpt-4o-mini", prompt="Once upon a time,")
```

---

## Moderation

**URL:** https://platform.openai.com/docs/guides/moderation

**Contents:**
- Moderation
- Quickstart
- Content classifications

Use the moderations endpoint to check whether text or images are potentially harmful. If harmful content is identified, you can take corrective action, like filtering content or intervening with user accounts creating offending content. The moderation endpoint is free to use.

You can use two models for this endpoint:

Use the tabs below to see how you can moderate text inputs or image inputs, using our official SDKs and the omni-moderation-latest model:

Here's a full example output, where the input is an image from a single frame of a war movie. The model correctly predicts indicators of violence in the image, with a violence category score of greater than 0.8.

The output has several categories in the JSON response, which tell you which (if any) categories of content are present in the inputs, and to what degree the model believes them to be present.

Set to true if the model classifies the content as potentially harmful, false otherwise.

Contains a dictionary of per-category violation flags. For each category, the value is true if the model flags the corresponding category as violated, false otherwise.

Contains a dictionary of per-category scores output by the model, denoting the model's confidence that the input violates the OpenAI's policy for the category. The value is between 0 and 1, where higher values denote higher confidence.

category_applied_input_types

This property contains information on which input types were flagged in the response, for each category. For example, if the both the image and text inputs to the model are flagged for "violence/graphic", the violence/graphic property will be set to ["image", "text"]. This is only available on omni models.

We plan to continuously upgrade the moderation endpoint's underlying model. Therefore, custom policies that rely on category_scores may need recalibration over time.

The table below describes the types of content that can be detected in the moderation API, along with which models and input types are supported for each category.

Categories marked as "Text only" do not support image inputs. If you send only images (without accompanying text) to the omni-moderation-latest model, it will return a score of 0 for these unsupported categories.

Content that expresses, incites, or promotes harassing language towards any target.

harassment/threatening

Harassment content that also includes violence or serious harm towards any target.

Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste. Hateful content aimed at non-protected groups (e.g., chess players) is harassment.

Hateful content that also includes violence or serious harm towards the targeted group based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.

Content that gives advice or instruction on how to commit illicit acts. A phrase like "how to shoplift" would fit this category.

The same types of content flagged by the illicit category, but also includes references to violence or procuring a weapon.

Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.

Content where the speaker expresses that they are engaging or intend to engage in acts of self-harm, such as suicide, cutting, and eating disorders.

self-harm/instructions

Content that encourages performing acts of self-harm, such as suicide, cutting, and eating disorders, or that gives instructions or advice on how to commit such acts.

Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).

Sexual content that includes an individual who is under 18 years old.

Content that depicts death, violence, or physical injury.

Content that depicts death, violence, or physical injury in graphic detail.

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
from openai import OpenAI
client = OpenAI()

response = client.moderations.create(
    model="omni-moderation-latest",
    input="...text to classify goes here...",
)

print(response)
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
from openai import OpenAI
client = OpenAI()

response = client.moderations.create(
    model="omni-moderation-latest",
    input="...text to classify goes here...",
)

print(response)
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
import OpenAI from "openai";
const openai = new OpenAI();

const moderation = await openai.moderations.create({
    model: "omni-moderation-latest",
    input: "...text to classify goes here...",
});

console.log(moderation);
```

---
