# Openai-Api - Fine Tuning

**Pages:** 5

---

## Reinforcement fine-tuning

**URL:** https://platform.openai.com/docs/guides/reinforcement-fine-tuning

**Contents:**
- Reinforcement fine-tuning
- Example: LLM-powered security review
- Define a grader
- Prepare your dataset
  - Upload your files
- Create a fine-tune job
  - Structured Outputs JSON schema
  - Create a job with the API
  - Monitoring your fine-tune job
    - Reward metrics

Reinforcement fine-tuning (RFT) adapts an OpenAI reasoning model with a feedback signal you define. Like supervised fine-tuning, it tailors the model to your task. The difference is that instead of training on fixed “correct” answers, it relies on a programmable grader that scores every candidate response. The training algorithm then shifts the model’s weights, so high-scoring outputs become more likely and low-scoring ones fade.

Generate a response for a prompt, provide an expert grade for the result, and reinforce the model's chain-of-thought for higher-scored responses.

Requires expert graders to agree on the ideal output from the model.

Reasoning models only.

This optimization lets you align the model with nuanced objectives like style, safety, or domain accuracy—with many practical use cases emerging. Run RFT in five steps:

During training, the platform cycles through the dataset, samples several responses per prompt, scores them with the grader, and applies policy-gradient updates based on those rewards. The loop continues until we hit the end of your training data or you stop the job at a chosen checkpoint, producing a model optimized for the metric that matters to you.

It's useful to understand the strengths and weaknesses of reinforcement fine-tuning to identify opportunities and to avoid wasted effort.

See common use cases, specific implementations, and grader examples in the reinforcement fine-tuning use case guide.

Reinforcement learning is a branch of machine learning in which a model learns by acting, receiving feedback, and readjusting itself to maximise future feedback. Instead of memorising one “right” answer per example, the model explores many possible answers, observes a numeric reward for each, and gradually shifts its behaviour so the high-reward answers become more likely and the low-reward ones disappear. Over repeated rounds, the model converges on a policy—a rule for choosing outputs—that best satisfies the reward signal you define.

In reinforcement fine-tuning (RFT), that reward signal comes from a custom grader that you define for your task. For every prompt in your dataset, the platform samples multiple candidate answers, runs your grader to score them, and applies a policy-gradient update that nudges the model toward answers with higher scores. This cycle—sample, grade, update—continues across the dataset (and successive epochs) until the model reliably optimizes for your grader’s understanding of quality. The grader encodes whatever you care about—accuracy, style, safety, or any metric—so the resulting fine-tuned model reflects those priorities and you don't have to manage reinforcement learning infrastructure.

Reinforcement fine-tuning is supported on o-series reasoning models only, and currently only for o4-mini.

To demonstrate reinforcement fine-tuning below, we'll fine-tune an o4-mini model to provide expert answers about a fictional company's security posture, based on an internal company policy document. We want the model to return a JSON object that conforms to a specific schema with Structured Outputs.

Example input question:

Using the internal policy document, we want the model to respond with JSON that has two keys:

Example desired output from the model:

Let's fine-tune a model with RFT to perform well at this task.

To perform RFT, define a grader to score the model's output during training, indicating the quality of its response. RFT uses the same set of graders as evals, which you may already be familiar with.

In this example, we define multiple graders to examine the properties of the JSON returned by our fine-tuned model:

We weight the output of each property equally in the calculate_output expression.

Below is the JSON payload data we'll use for this grader in API requests. In both graders, we use {{ }} template syntax to refer to the relevant properties of both the item (the row of test data being used for evaluation) and sample (the model output generated during the training run).

To create an RFT fine-tune, you'll need both a training and test dataset. Both the training and test datasets will share the same JSONL format. Each line in the JSONL data file will contain a messages array, along with any additional fields required to grade the output from the model. The full specification for RFT dataset can be found here.

In our case, in addition to the messages array, each line in our JSONL file also needs compliant and explanation properties, which we can use as reference values to test the fine-tuned model's Structured Output.

A single line in our training and test datasets looks like this as indented JSON:

Below, find some JSONL data you can use for both training and testing when you create your fine-tune job. Note that these datasets are for illustration purposes only—in your real test data, strive for diverse and representative inputs for your application.

Start small—between several dozen and a few hundred examples—to determine the usefulness of RFT before investing in a large dataset. For product safety reasons, the training set must first pass through an automated screening process. Large datasets take longer to process. This screening process begins when you start a fine-tuning job with a file, not upon initial file upload. Once a file has successfully completed screening, you can use it repeatedly without delay.

Dozens of examples can be meaningful as long as they're high quality. After screening, more data is better, as long as it remains high quality. With larger datasets, you can use a higher batch size, which tends to improve training stability.

Your training file can contain a maximum of 50,000 examples. Test datasets can contain a maximum of 1,000 examples. Test datasets also go through automated screening.

The process for uploading RFT training and test data files is the same as supervised fine-tuning. Upload your training data to OpenAI either through the API or using our UI. Files must be uploaded with a purpose of fine-tune in order to be used with fine-tuning.

You need file IDs for both your test and training data files to create a fine-tune job.

Create a fine-tune job using either the API or fine-tuning dashboard. To do this, you need:

If you're fine-tuning a model to return Structured Outputs, provide the JSON schema being used to format the output. See a valid JSON schema for our security interview use case:

To simplify JSON schema generation, start from a Pydantic BaseModel class:

Configuring a job with the API has a lot of moving parts, so many users prefer to configure them in the fine-tuning dashboard UI. However, here's a complete API request to kick off a fine-tune job with all the configuration we've set up in this guide so far:

This request returns a fine-tuning job object, which includes a job id. Use this ID to monitor the progress of your job and retrieve the fine-tuned model when the job is complete.

To qualify for data sharing inference pricing, make sure to share evaluation and fine-tuning data with OpenAI before creating the job. You can verify the job was marked as shared by confirming shared_with_openai is set to true.

Fine-tuning jobs take some time to complete, and RFT jobs tend to take longer than SFT or DPO jobs. To monitor the progress of your fine-tune job, use the fine-tuning dashboard or the API.

For reinforcement fine-tuning jobs, the primary metrics are the per-step reward metrics. These metrics indicate how well your model is performing on the training data. They're calculated by the graders you defined in your job configuration. These are two separate top-level reward metrics:

Find a full description of all training metrics in the training metrics section.

To evaluate the current state of the model when your job is only partially finished, pause the job to stop the training process and produce a checkpoint at the current step. You can use this checkpoint to evaluate the model on a held-out test set. If the results look good, resume the job to continue training from that checkpoint. Learn more in pausing and resuming jobs.

Reinforcement fine-tuning jobs are integrated with our evals product. When you make a reinforcement fine-tuning job, a new eval is automatically created and associated with the job. As validation steps are performed, we combine the input prompts, model samples, and grader outputs to make a new eval run for that step.

Learn more about the evals integration in the appendix section below.

By the time your fine-tuning job finishes, you should have a decent idea of how well the model is performing based on the mean reward value on the validation set. However, it's possible that the model has either overfit to the training data or has learned to reward hack your grader, which allows it to produce high scores without actually being correct. Before deploying your model, inspect its behavior on a representative set of prompts to ensure it behaves how you expect.

Understanding the model's behavior can be done quickly by inspecting the evals associated with the fine-tuning job. Specifically, pay close attention to the run made for the final training step to see the end model's behavior. You can also use the evals product to compare the final run to earlier runs and see how the model's behavior has changed over the course of training.

Evaluate your newly optimized model by using it! When the fine-tuned model finishes training, use its ID in either the Responses or Chat Completions API, just as you would an OpenAI base model.

Checkpoints are models you can use that are created before the final step of the training process. For RFT, OpenAI creates a full model checkpoint at each validation step and keeps the three with the highest valid_reward_mean scores. Checkpoints are useful for evaluating the model at different points in the training process and comparing performance at different steps.

The checkpoint object contains metrics data to help you determine the usefulness of this model. As an example, the response looks like this:

Each checkpoint specifies:

Before launching in production, review and follow the following safety information.

Once a fine-tuning job is completed, we assess the resulting model’s behavior across 13 distinct safety categories. Each category represents a critical area where AI outputs could potentially cause harm if not properly controlled.

Each category has a predefined pass threshold; if too many evaluated examples in a given category fail, OpenAI blocks the fine-tuned model from deployment. If your fine-tuned model does not pass the safety checks, OpenAI sends a message in the fine-tuning job explaining which categories don't meet the required thresholds. You can view the results in the moderation checks section of the fine-tuning job.

In addition to reviewing any failed safety checks in the fine-tuning job object, you can retrieve details about which categories failed by querying the fine-tuning API events endpoint. Look for events of type moderation_checks for details about category results and enforcement. This information can help you narrow down which categories to target for retraining and improvement. The model spec has rules and examples that can help identify areas for additional training data.

While these evaluations cover a broad range of safety categories, conduct your own evaluations of the fine-tuned model to ensure it's appropriate for your use case.

Now that you know the basics of reinforcement fine-tuning, explore other fine-tuning methods.

Fine-tune a model by providing correct outputs for sample inputs.

Learn to fine-tune for computer vision with image inputs.

Fine-tune a model using direct preference optimization (DPO).

Reinforcement fine-tuning jobs publish per-step training metrics as fine-tuning events. Pull these metrics through the API or view them as graphs and charts in the fine-tuning dashboard.

Learn more about training metrics below.

Below is an example metric event from a real reinforcement fine-tuning job. The various fields in this payload will be discussed in the following sections.

The top-level metrics to watch are train_reward_mean and valid_reward_mean, which indicate the average reward assigned by your graders across all samples in the training and validation datasets, respectively.

Additionally, if you use a multi-grader configuration, per-grader train and validation reward metrics will be published as well. These metrics are included under the event.data.scores object in the fine-tuning events object, with one entry per grader. The per-grader metrics are useful for understanding how the model is performing on each individual grader, and can help you identify if the model is overfitting to one grader or another.

From the fine-tuning dashboard, the individual grader metrics will be displayed in their own graph below the overall train_reward_mean and valid_reward_mean metrics.

An important characteristic of a reasoning model is the number of reasoning tokens it uses before responding to a prompt. Often, during training, the model will drastically change the average number of reasoning tokens it uses to respond to a prompt. This is a sign that the model is changing its behavior in response to the reward signal. The model may learn to use fewer reasoning tokens to achieve the same reward, or it may learn to use more reasoning tokens to achieve a higher reward.

You can monitor the train_reasoning_tokens_mean and valid_reasoning_tokens_mean metrics to see how the model is changing its behavior over time. These metrics are the average number of reasoning tokens used by the model to respond to a prompt in the training and validation datasets, respectively. You can also view the mean reasoning token count in the fine-tuning dashboard under the "Reasoning Tokens" chart.

If you are using model graders, you will likely want to monitor the token usage of these graders. Per-grader token usage statistics are available under the event.data.usage.graders object, and are broken down into:

The _mean metrics represent the average number of tokens used by the grader to process all prompts in the current step, while the _count metrics represent the total number of tokens used by the grader across all samples in the current step. The per-step token usage is also displayed on the fine-tuning dashboard under the "Grading Token Usage" chart.

We include various metrics that help you understand how long each step of the training process is taking and how different parts of the training process are contributing to the per-step timing.

These metrics are available under the event.data.timing object, and are broken down into step and graders fields.

The step field contains the following metrics:

The step timing metrics are also displayed on the fine-tuning dashboard under the "Per Step Duration" chart.

The graders field contains timing information that details the time taken to execute each grader for the current step. Each grader will have its own timing under the train_execution_latency_mean and valid_execution_latency_mean metrics, which represent the average time taken to execute the grader on the training and validation datasets, respectively.

Graders are executed in parallel with a concurrency limit, so it is not always clear how individual grader latency adds up to the total time taken for grading. However, it is generally true that graders which take longer to execute individually will cause a job to execute more slowly. This means that slower model graders will cause the job to take longer to complete, and more expensive python code will do the same. The fastest graders generally are string_check and text_similarity as those are executed local to the training loop.

Reinforcement fine-tuning jobs are directly integrated with our evals product. When you make a reinforcement fine-tuning job, a new eval is automatically created and associated with the job.

As validation steps are performed, the input prompts, model samples, grader outputs, and more metadata will be combined to make a new eval run for that step. At the end of the job, you will have one run for each validation step. This allows you to compare the performance of the model at different steps, and to see how the model's behavior has changed over the course of training.

You can find the eval associated with your fine-tuning job by viewing your job on the fine-tuning dashboard, or by finding the eval_id field on the fine-tuning job object.

The evals product is useful for inspecting the outputs of the model on specific datapoints, to get an understanding for how the model is behaving in different scenarios. It can help you figure out which slice of your dataset the model is performing poorly on which can help you identify areas for improvement in your training data.

The evals product can also help you find areas of improvement for your graders by finding areas where the grader is either overly lenient or overly harsh on the model outputs.

You can pause a fine-tuning job at any time by using the fine-tuning jobs API. Calling the pause API will tell the training process to create a new model snapshot, stop training, and put the job into a "Paused" state. The model snapshot will go through a normal safety screening process after which it will be available for you to use throughout the OpenAI platform as a normal fine-tuned model.

If you wish to continue the training process for a paused job, you can do so by using the fine-tuning jobs API. This will resume the training process from the last checkpoint created when the job was paused and will continue training until the job is either completed or paused again.

If you are training your model to perform tool calls, you will need to:

Reinforcement fine-tuning jobs are billed based on the amount of time spent training, as well as the number of tokens used by the model during training. We only bill for time spent in the core training loop, not for time spent preparing the training data, validating datasets, waiting in queues, running safety evals, or other overhead.

Details on exactly how we bill for reinforcement fine-tuning jobs can be found in this help center article.

Reinforcement fine-tuning is a complex process with many moving parts, and there are many places where things can go wrong. We publish various error metrics to help you understand what is going wrong in your job, and how to fix it. In general, we try to avoid failing a job entirely unless a very serious error occurs. When errors do occur, they often happen during the grading step. Errors during grading often happen either to the model outputting a sample that the grader doesn't know how to handle, the grader failing to execute properly due to some sort of system error, or due to a bug in the grading logic itself.

The error metrics are available under the event.data.errors object, and are aggregated into counts and rates rolled up per-grader. We also display rates and counts of errors on the fine-tuning dashboard.

The grader errors are broken down into the following categories, and they exist in both train_ (for training data) and valid_ (for validation data) versions:

**Examples:**

Example 1 (unknown):
```unknown
Do you have a dedicated security team?
```

Example 2 (text):
```text
Do you have a dedicated security team?
```

Example 3 (unknown):
```unknown
1
2
3
4
{
    "compliant": "yes",
    "explanation": "A dedicated security team follows strict protocols for handling incidents."
}
```

Example 4 (json):
```json
1
2
3
4
{
    "compliant": "yes",
    "explanation": "A dedicated security team follows strict protocols for handling incidents."
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/fine-tuning

**Contents:**
- Fine-tuning
- Create fine-tuning job
    - Request body
    - Returns
- List fine-tuning jobs
    - Query parameters
    - Returns
- List fine-tuning events
    - Path parameters
    - Query parameters

Manage fine-tuning jobs to tailor a model to your specific training data. Related guide: Fine-tune models

Creates a fine-tuning job which begins the process of creating a new model from a given dataset.

Response includes details of the enqueued job including job status and the name of the fine-tuned models once complete.

Learn more about fine-tuning

The name of the model to fine-tune. You can select one of the supported models.

The ID of an uploaded file that contains training data.

See upload file for how to upload a file.

Your dataset must be formatted as a JSONL file. Additionally, you must upload your file with the purpose fine-tune.

The contents of the file should differ depending on if the model uses the chat, completions format, or if the fine-tuning method uses the preference format.

See the fine-tuning guide for more details.

The hyperparameters used for the fine-tuning job. This value is now deprecated in favor of method, and should be passed in under the method parameter.

A list of integrations to enable for your fine-tuning job.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The method used for fine-tuning.

The seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases. If a seed is not specified, one will be generated for you.

A string of up to 64 characters that will be added to your fine-tuned model name.

For example, a suffix of "custom-model-name" would produce a model name like ft:gpt-4o-mini:openai:custom-model-name:7p4lURel.

The ID of an uploaded file that contains validation data.

If you provide this file, the data is used to generate validation metrics periodically during fine-tuning. These metrics can be viewed in the fine-tuning results file. The same data should not be present in both train and validation files.

Your dataset must be formatted as a JSONL file. You must upload your file with the purpose fine-tune.

See the fine-tuning guide for more details.

A fine-tuning.job object.

List your organization's fine-tuning jobs

Identifier for the last job from the previous pagination request.

Number of fine-tuning jobs to retrieve.

Optional metadata filter. To filter, use the syntax metadata[k]=v. Alternatively, set metadata=null to indicate no metadata.

A list of paginated fine-tuning job objects.

Get status updates for a fine-tuning job.

The ID of the fine-tuning job to get events for.

Identifier for the last event from the previous pagination request.

Number of events to retrieve.

A list of fine-tuning event objects.

List checkpoints for a fine-tuning job.

The ID of the fine-tuning job to get checkpoints for.

Identifier for the last checkpoint ID from the previous pagination request.

Number of checkpoints to retrieve.

A list of fine-tuning checkpoint objects for a fine-tuning job.

NOTE: This endpoint requires an admin API key.

Organization owners can use this endpoint to view all permissions for a fine-tuned model checkpoint.

The ID of the fine-tuned model checkpoint to get permissions for.

Identifier for the last permission ID from the previous pagination request.

Number of permissions to retrieve.

The order in which to retrieve permissions.

The ID of the project to get permissions for.

A list of fine-tuned model checkpoint permission objects for a fine-tuned model checkpoint.

NOTE: Calling this endpoint requires an admin API key.

This enables organization owners to share fine-tuned models with other projects in their organization.

The ID of the fine-tuned model checkpoint to create a permission for.

The project identifiers to grant access to.

A list of fine-tuned model checkpoint permission objects for a fine-tuned model checkpoint.

NOTE: This endpoint requires an admin API key.

Organization owners can use this endpoint to delete a permission for a fine-tuned model checkpoint.

The ID of the fine-tuned model checkpoint to delete a permission for.

The ID of the fine-tuned model checkpoint permission to delete.

The deletion status of the fine-tuned model checkpoint permission object.

Get info about a fine-tuning job.

Learn more about fine-tuning

The ID of the fine-tuning job.

The fine-tuning object with the given ID.

Immediately cancel a fine-tune job.

The ID of the fine-tuning job to cancel.

The cancelled fine-tuning object.

Resume a fine-tune job.

The ID of the fine-tuning job to resume.

The resumed fine-tuning object.

Pause a fine-tune job.

The ID of the fine-tuning job to pause.

The paused fine-tuning object.

The per-line training example of a fine-tuning input file for chat models using the supervised method. Input messages may contain text or image content only. Audio and file input messages are not currently supported for fine-tuning.

A list of functions the model may generate JSON inputs for.

Whether to enable parallel function calling during tool use.

A list of tools the model may generate JSON inputs for.

The per-line training example of a fine-tuning input file for chat models using the dpo method. Input messages may contain text or image content only. Audio and file input messages are not currently supported for fine-tuning.

The non-preferred completion message for the output.

The preferred completion message for the output.

Per-line training example for reinforcement fine-tuning. Note that messages and tools are the only reserved keywords. Any other arbitrary key-value data can be included on training datapoints and will be available to reference during grading under the {{ item.XXX }} template variable. Input messages may contain text or image content only. Audio and file input messages are not currently supported for fine-tuning.

A list of tools the model may generate JSON inputs for.

The fine_tuning.job object represents a fine-tuning job that has been created through the API.

The Unix timestamp (in seconds) for when the fine-tuning job was created.

For fine-tuning jobs that have failed, this will contain more information on the cause of the failure.

The Unix timestamp (in seconds) for when the fine-tuning job is estimated to finish. The value will be null if the fine-tuning job is not running.

The name of the fine-tuned model that is being created. The value will be null if the fine-tuning job is still running.

The Unix timestamp (in seconds) for when the fine-tuning job was finished. The value will be null if the fine-tuning job is still running.

The hyperparameters used for the fine-tuning job. This value will only be returned when running supervised jobs.

The object identifier, which can be referenced in the API endpoints.

A list of integrations to enable for this fine-tuning job.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The method used for fine-tuning.

The base model that is being fine-tuned.

The object type, which is always "fine_tuning.job".

The organization that owns the fine-tuning job.

The compiled results file ID(s) for the fine-tuning job. You can retrieve the results with the Files API.

The seed used for the fine-tuning job.

The current status of the fine-tuning job, which can be either validating_files, queued, running, succeeded, failed, or cancelled.

The total number of billable tokens processed by this fine-tuning job. The value will be null if the fine-tuning job is still running.

The file ID used for training. You can retrieve the training data with the Files API.

The file ID used for validation. You can retrieve the validation results with the Files API.

Fine-tuning job event object

The Unix timestamp (in seconds) for when the fine-tuning job was created.

The data associated with the event.

The object identifier.

The log level of the event.

The message of the event.

The object type, which is always "fine_tuning.job.event".

The fine_tuning.job.checkpoint object represents a model checkpoint for a fine-tuning job that is ready to use.

The Unix timestamp (in seconds) for when the checkpoint was created.

The name of the fine-tuned checkpoint model that is created.

The name of the fine-tuning job that this checkpoint was created from.

The checkpoint identifier, which can be referenced in the API endpoints.

Metrics at the step number during the fine-tuning job.

The object type, which is always "fine_tuning.job.checkpoint".

The step number that the checkpoint was created at.

The checkpoint.permission object represents a permission for a fine-tuned model checkpoint.

The Unix timestamp (in seconds) for when the permission was created.

The permission identifier, which can be referenced in the API endpoints.

The object type, which is always "checkpoint.permission".

The project identifier that the permission is for.

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
curl https://api.openai.com/v1/fine_tuning/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "training_file": "file-BK7bzQj3FfZFXr7DbL6xJwfo",
    "model": "gpt-4o-mini"
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
curl https://api.openai.com/v1/fine_tuning/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "training_file": "file-BK7bzQj3FfZFXr7DbL6xJwfo",
    "model": "gpt-4o-mini"
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
from openai import OpenAI
client = OpenAI()

client.fine_tuning.jobs.create(
  training_file="file-abc123",
  model="gpt-4o-mini"
)
```

---

## Supervised fine-tuning

**URL:** https://platform.openai.com/docs/guides/supervised-fine-tuning

**Contents:**
- Supervised fine-tuning
- Overview
- Build your dataset
  - Right number of examples
  - What makes a good example
  - Formatting your data
  - Distilling from a larger model
- Upload training data
- Create a fine-tuning job
- Evaluate the result

Supervised fine-tuning (SFT) lets you train an OpenAI model with examples for your specific use case. The result is a customized model that more reliably produces your desired style and content.

Provide examples of correct responses to prompts to guide the model's behavior.

Often uses human-generated "ground truth" responses to show the model how it should respond.

gpt-4.1-2025-04-14 gpt-4.1-mini-2025-04-14 gpt-4.1-nano-2025-04-14

Supervised fine-tuning has four major parts:

Good evals first! Only invest in fine-tuning after setting up evals. You need a reliable way to determine whether your fine-tuned model is performing better than a base model.

Build a robust, representative dataset to get useful results from a fine-tuned model. Use the following techniques and considerations.

If performance improves with 50 good examples, try adding examples to see further results. If 50 examples have no impact, rethink your task or prompt before adding training data.

An example of JSONL training data, where the model calls a get_weather function:

Each line of the training data file contains a JSON structure like the following, containing both an example user prompt and a correct response from the model as an assistant message.

One way to build a training data set for a smaller model is to distill the results of a large model to create training data for supervised fine tuning. The general flow of this technique is:

This technique can enable you to train a small model to perform similarly on a specific task to a larger, more costly model.

Upload your dataset of examples to OpenAI. We use it to update the model's weights and produce outputs like the ones included in your data.

In addition to text completions, you can train the model to more effectively generate structured JSON output or function calls.

Assuming the data above is saved to a file called mydata.jsonl, you can upload it to the OpenAI platform using the code below. Note that the purpose of the uploaded file is set to fine-tune:

Note the id of the file that is uploaded in the data returned from the API - you'll need that file identifier in subsequent API requests.

With your test data uploaded, create a fine-tuning job to customize a base model using the training data you provide. When creating a fine-tuning job, you must specify:

Create a supervised fine-tuning job by calling the fine-tuning API:

The API responds with information about the fine-tuning job in progress. Depending on the size of your training data, the training process may take several minutes or hours. You can poll the API for updates on a specific job.

When the fine-tuning job finishes, your fine-tuned model is ready to use. A completed fine-tune job returns data like this:

Note the fine_tuned_model property. This is the model ID to use in Responses or Chat Completions to make API requests using your fine-tuned model.

Here's an example of calling the Responses API with your fine-tuned model ID:

Use the approaches below to check how your fine-tuned model performs. Adjust your prompts, data, and fine-tuning job as needed until you get the results you want. The best way to fine-tune is to continue iterating.

To see if your fine-tuned model performs better than the original base model, use evals. Before running your fine-tuning job, carve out data from the same training dataset you collected in step 1. This holdout data acts as a control group when you use it for evals. Make sure the training and holdout data have roughly the same diversity of user input types and model responses.

Learn more about running evals.

Check the status of a fine-tuning job in the dashboard or by polling the job ID in the API.

Use this curl command to get information about your fine-tuning job:

The job contains a fine_tuned_model property, which is your new fine-tuned model's unique ID.

Evaluate your newly optimized model by using it! When the fine-tuned model finishes training, use its ID in either the Responses or Chat Completions API, just as you would an OpenAI base model.

Checkpoints are models you can use. We create a full model checkpoint for you at the end of each training epoch. They're useful in cases where your fine-tuned model improves early on but then memorizes the dataset instead of learning generalizable knowledge—called _overfitting. Checkpoints provide versions of your customized model from various moments in the process.

The checkpoint object contains metrics data to help you determine the usefulness of this model. As an example, the response looks like this:

Each checkpoint specifies:

Currently, only the checkpoints for the last three epochs of the job are saved and available for use.

Before launching in production, review and follow the following safety information.

Once a fine-tuning job is completed, we assess the resulting model’s behavior across 13 distinct safety categories. Each category represents a critical area where AI outputs could potentially cause harm if not properly controlled.

Each category has a predefined pass threshold; if too many evaluated examples in a given category fail, OpenAI blocks the fine-tuned model from deployment. If your fine-tuned model does not pass the safety checks, OpenAI sends a message in the fine-tuning job explaining which categories don't meet the required thresholds. You can view the results in the moderation checks section of the fine-tuning job.

In addition to reviewing any failed safety checks in the fine-tuning job object, you can retrieve details about which categories failed by querying the fine-tuning API events endpoint. Look for events of type moderation_checks for details about category results and enforcement. This information can help you narrow down which categories to target for retraining and improvement. The model spec has rules and examples that can help identify areas for additional training data.

While these evaluations cover a broad range of safety categories, conduct your own evaluations of the fine-tuned model to ensure it's appropriate for your use case.

Now that you know the basics of supervised fine-tuning, explore these other methods as well.

Learn to fine-tune for computer vision with image inputs.

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
{"messages":[{"role":"user","content":"What is the weather in San Francisco?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Francisco, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Minneapolis?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Minneapolis, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Minneapolis, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in San Diego?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Diego, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Diego, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Memphis?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Memphis, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Memphis, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Atlanta?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Atlanta, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Atlanta, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Sunnyvale?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Sunnyvale, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Sunnyvale, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Chicago?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Chicago, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Chicago, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Boston?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Boston, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Boston, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Honolulu?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Honolulu, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Honolulu, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in San Antonio?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Antonio, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Antonio, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
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
{"messages":[{"role":"user","content":"What is the weather in San Francisco?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Francisco, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Minneapolis?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Minneapolis, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Minneapolis, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in San Diego?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Diego, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Diego, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Memphis?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Memphis, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Memphis, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Atlanta?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Atlanta, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Atlanta, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Sunnyvale?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Sunnyvale, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Sunnyvale, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Chicago?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Chicago, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Chicago, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Boston?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Boston, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Boston, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Honolulu?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Honolulu, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Honolulu, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in San Antonio?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Antonio, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Antonio, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
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
{
  "messages": [
    { "role": "user", "content": "What is the weather in San Francisco?" },
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "call_id",
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "arguments": "{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"
          }
        }
      ]
    }
  ],
  "parallel_tool_calls": false,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "Get the current weather",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
                "type": "string",
                "description": "The city and country, eg. San Francisco, USA"
            },
            "format": { "type": "string", "enum": ["celsius", "fahrenheit"] }
          },
          "required": ["location", "format"]
        }
      }
    }
  ]
}
```

---

## Model optimization

**URL:** https://platform.openai.com/docs/guides/fine-tuning

**Contents:**
- Model optimization
- Model optimization workflow
- Build evals
- Write effective prompts
- Fine-tune a model
  - Fine-tuning methods
  - How fine-tuning works
- Learn from experts

LLM output is non-deterministic, and model behavior changes between model snapshots and families. Developers must constantly measure and tune the performance of LLM applications to ensure they're getting the best results. In this guide, we explore the techniques and OpenAI platform tools you can use to ensure high quality outputs from the model.

Optimizing model output requires a combination of evals, prompt engineering, and fine-tuning, creating a flywheel of feedback that leads to better prompts and better training data for fine-tuning. The optimization process usually goes something like this.

Here's an overview of the major steps, and how to do them using the OpenAI platform.

In the OpenAI platform, you can build and run evals either via API or in the dashboard. You might even consider writing evals before you start writing prompts, taking an approach akin to behavior-driven development (BDD).

Run your evals against test inputs like you expect to see in production. Using one of several available graders, measure the results of a prompt against your test data set.

Run tests on your model outputs to ensure you're getting the right results.

With evals in place, you can effectively iterate on prompts. The prompt engineering process may be all you need in order to get great results for your use case. Different models may require different prompting techniques, but there are several best practices you can apply across the board to get better results.

Learn the basics of writing good prompts for the model.

OpenAI models are already pre-trained to perform across a broad range of subjects and tasks. Fine-tuning lets you take an OpenAI base model, provide the kinds of inputs and outputs you expect in your application, and get a model that excels in the tasks you'll use it for.

Fine-tuning can be a time-consuming process, but it can also enable a model to consistently format responses in a certain way or handle novel inputs. You can use fine-tuning with prompt engineering to realize a few more benefits over prompting alone:

Visit our pricing page to learn more about how fine-tuned model training and usage are billed.

These are the fine-tuning methods supported in the OpenAI platform today.

Supervised fine-tuning (SFT)

Provide examples of correct responses to prompts to guide the model's behavior.

Often uses human-generated "ground truth" responses to show the model how it should respond.

gpt-4.1-2025-04-14 gpt-4.1-mini-2025-04-14 gpt-4.1-nano-2025-04-14

Provide image inputs for supervised fine-tuning to improve the model's understanding of image inputs.

Direct preference optimization (DPO)

Provide both a correct and incorrect example response for a prompt. Indicate the correct response to help the model perform better.

gpt-4.1-2025-04-14 gpt-4.1-mini-2025-04-14 gpt-4.1-nano-2025-04-14

Reinforcement fine-tuning (RFT)

Generate a response for a prompt, provide an expert grade for the result, and reinforce the model's chain-of-thought for higher-scored responses.

Requires expert graders to agree on the ideal output from the model.

Reasoning models only.

In the OpenAI platform, you can create fine-tuned models either in the dashboard or with the API. This is the general shape of the fine-tuning process:

Get started with supervised fine-tuning, vision fine-tuning, direct preference optimization, or reinforcement fine-tuning.

Model optimization is a complex topic, and sometimes more art than science. Check out the videos below from members of the OpenAI team on model optimization techniques.

---

## Supervised fine-tuning

**URL:** https://platform.openai.com/docs/guides/distillation

**Contents:**
- Supervised fine-tuning
- Overview
- Build your dataset
  - Right number of examples
  - What makes a good example
  - Formatting your data
  - Distilling from a larger model
- Upload training data
- Create a fine-tuning job
- Evaluate the result

Supervised fine-tuning (SFT) lets you train an OpenAI model with examples for your specific use case. The result is a customized model that more reliably produces your desired style and content.

Provide examples of correct responses to prompts to guide the model's behavior.

Often uses human-generated "ground truth" responses to show the model how it should respond.

gpt-4.1-2025-04-14 gpt-4.1-mini-2025-04-14 gpt-4.1-nano-2025-04-14

Supervised fine-tuning has four major parts:

Good evals first! Only invest in fine-tuning after setting up evals. You need a reliable way to determine whether your fine-tuned model is performing better than a base model.

Build a robust, representative dataset to get useful results from a fine-tuned model. Use the following techniques and considerations.

If performance improves with 50 good examples, try adding examples to see further results. If 50 examples have no impact, rethink your task or prompt before adding training data.

An example of JSONL training data, where the model calls a get_weather function:

Each line of the training data file contains a JSON structure like the following, containing both an example user prompt and a correct response from the model as an assistant message.

One way to build a training data set for a smaller model is to distill the results of a large model to create training data for supervised fine tuning. The general flow of this technique is:

This technique can enable you to train a small model to perform similarly on a specific task to a larger, more costly model.

Upload your dataset of examples to OpenAI. We use it to update the model's weights and produce outputs like the ones included in your data.

In addition to text completions, you can train the model to more effectively generate structured JSON output or function calls.

Assuming the data above is saved to a file called mydata.jsonl, you can upload it to the OpenAI platform using the code below. Note that the purpose of the uploaded file is set to fine-tune:

Note the id of the file that is uploaded in the data returned from the API - you'll need that file identifier in subsequent API requests.

With your test data uploaded, create a fine-tuning job to customize a base model using the training data you provide. When creating a fine-tuning job, you must specify:

Create a supervised fine-tuning job by calling the fine-tuning API:

The API responds with information about the fine-tuning job in progress. Depending on the size of your training data, the training process may take several minutes or hours. You can poll the API for updates on a specific job.

When the fine-tuning job finishes, your fine-tuned model is ready to use. A completed fine-tune job returns data like this:

Note the fine_tuned_model property. This is the model ID to use in Responses or Chat Completions to make API requests using your fine-tuned model.

Here's an example of calling the Responses API with your fine-tuned model ID:

Use the approaches below to check how your fine-tuned model performs. Adjust your prompts, data, and fine-tuning job as needed until you get the results you want. The best way to fine-tune is to continue iterating.

To see if your fine-tuned model performs better than the original base model, use evals. Before running your fine-tuning job, carve out data from the same training dataset you collected in step 1. This holdout data acts as a control group when you use it for evals. Make sure the training and holdout data have roughly the same diversity of user input types and model responses.

Learn more about running evals.

Check the status of a fine-tuning job in the dashboard or by polling the job ID in the API.

Use this curl command to get information about your fine-tuning job:

The job contains a fine_tuned_model property, which is your new fine-tuned model's unique ID.

Evaluate your newly optimized model by using it! When the fine-tuned model finishes training, use its ID in either the Responses or Chat Completions API, just as you would an OpenAI base model.

Checkpoints are models you can use. We create a full model checkpoint for you at the end of each training epoch. They're useful in cases where your fine-tuned model improves early on but then memorizes the dataset instead of learning generalizable knowledge—called _overfitting. Checkpoints provide versions of your customized model from various moments in the process.

The checkpoint object contains metrics data to help you determine the usefulness of this model. As an example, the response looks like this:

Each checkpoint specifies:

Currently, only the checkpoints for the last three epochs of the job are saved and available for use.

Before launching in production, review and follow the following safety information.

Once a fine-tuning job is completed, we assess the resulting model’s behavior across 13 distinct safety categories. Each category represents a critical area where AI outputs could potentially cause harm if not properly controlled.

Each category has a predefined pass threshold; if too many evaluated examples in a given category fail, OpenAI blocks the fine-tuned model from deployment. If your fine-tuned model does not pass the safety checks, OpenAI sends a message in the fine-tuning job explaining which categories don't meet the required thresholds. You can view the results in the moderation checks section of the fine-tuning job.

In addition to reviewing any failed safety checks in the fine-tuning job object, you can retrieve details about which categories failed by querying the fine-tuning API events endpoint. Look for events of type moderation_checks for details about category results and enforcement. This information can help you narrow down which categories to target for retraining and improvement. The model spec has rules and examples that can help identify areas for additional training data.

While these evaluations cover a broad range of safety categories, conduct your own evaluations of the fine-tuned model to ensure it's appropriate for your use case.

Now that you know the basics of supervised fine-tuning, explore these other methods as well.

Learn to fine-tune for computer vision with image inputs.

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
{"messages":[{"role":"user","content":"What is the weather in San Francisco?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Francisco, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Minneapolis?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Minneapolis, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Minneapolis, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in San Diego?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Diego, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Diego, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Memphis?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Memphis, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Memphis, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Atlanta?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Atlanta, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Atlanta, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Sunnyvale?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Sunnyvale, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Sunnyvale, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Chicago?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Chicago, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Chicago, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Boston?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Boston, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Boston, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Honolulu?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Honolulu, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Honolulu, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in San Antonio?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Antonio, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Antonio, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
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
{"messages":[{"role":"user","content":"What is the weather in San Francisco?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Francisco, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Minneapolis?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Minneapolis, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Minneapolis, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in San Diego?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Diego, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Diego, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Memphis?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Memphis, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Memphis, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Atlanta?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Atlanta, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Atlanta, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Sunnyvale?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Sunnyvale, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Sunnyvale, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Chicago?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Chicago, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Chicago, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Boston?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Boston, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Boston, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in Honolulu?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"Honolulu, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. Honolulu, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
{"messages":[{"role":"user","content":"What is the weather in San Antonio?"},{"role":"assistant","tool_calls":[{"id":"call_id","type":"function","function":{"name":"get_current_weather","arguments":"{\"location\": \"San Antonio, USA\", \"format\": \"celsius\"}"}}]}],"parallel_tool_calls":false,"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and country, eg. San Antonio, USA"},"format":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
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
{
  "messages": [
    { "role": "user", "content": "What is the weather in San Francisco?" },
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "call_id",
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "arguments": "{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"
          }
        }
      ]
    }
  ],
  "parallel_tool_calls": false,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "Get the current weather",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
                "type": "string",
                "description": "The city and country, eg. San Francisco, USA"
            },
            "format": { "type": "string", "enum": ["celsius", "fahrenheit"] }
          },
          "required": ["location", "format"]
        }
      }
    }
  ]
}
```

---
