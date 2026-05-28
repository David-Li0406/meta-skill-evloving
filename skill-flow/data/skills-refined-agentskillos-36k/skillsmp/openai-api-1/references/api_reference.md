# Openai-Api - Api Reference

**Pages:** 58

---

## 

**URL:** https://platform.openai.com/docs/api-reference/authentication

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

## 

**URL:** https://platform.openai.com/docs/api-reference/project-groups

**Contents:**
- Project groups
- List project groups
    - Path parameters
    - Query parameters
    - Returns
- Add project group
    - Path parameters
    - Request body
    - Returns
- Remove project group

Manage which groups have access to a project and the role they receive.

Lists the groups that have access to a project.

The ID of the project to inspect.

Cursor for pagination. Provide the ID of the last group from the previous response to fetch the next page.

A limit on the number of project groups to return. Defaults to 20.

Sort order for the returned groups.

A list of project group objects.

Grants a group access to a project.

The ID of the project to update.

Identifier of the group to add to the project.

Identifier of the project role to grant to the group.

The created project group object.

Revokes a group's access to a project.

The ID of the group to remove from the project.

The ID of the project to update.

Confirmation of the deleted project group.

Details about a group's membership in a project.

Unix timestamp (in seconds) when the group was granted project access.

Identifier of the group that has access to the project.

Display name of the group.

Always project.group.

Identifier of the project.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/projects/proj_abc123/groups?limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/projects/proj_abc123/groups?limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
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
{
    "object": "list",
    "data": [
        {
            "object": "project.group",
            "project_id": "proj_abc123",
            "group_id": "group_01J1F8ABCDXYZ",
            "group_name": "Support Team",
            "created_at": 1711471533
        }
    ],
    "has_more": false,
    "next": null
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
{
    "object": "list",
    "data": [
        {
            "object": "project.group",
            "project_id": "proj_abc123",
            "group_id": "group_01J1F8ABCDXYZ",
            "group_name": "Support Team",
            "created_at": 1711471533
        }
    ],
    "has_more": false,
    "next": null
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/realtime-beta-server-events

**Contents:**
- Realtime Beta server events
- error
- session.created
- session.updated
- transcription_session.created
- transcription_session.updated
- conversation.item.created
- conversation.item.retrieved
- conversation.item.input_audio_transcription.completed
- conversation.item.input_audio_transcription.delta

These are events emitted from the OpenAI Realtime WebSocket server to the client.

Returned when an error occurs, which could be a client problem or a server problem. Most errors are recoverable and the session will stay open, we recommend to implementors to monitor and log error messages by default.

Details of the error.

The unique ID of the server event.

The event type, must be error.

Returned when a Session is created. Emitted automatically when a new connection is established as the first server event. This event will contain the default Session configuration.

The unique ID of the server event.

Realtime session object for the beta interface.

The event type, must be session.created.

Returned when a session is updated with a session.update event, unless there is an error.

The unique ID of the server event.

Realtime session object for the beta interface.

The event type, must be session.updated.

Returned when a transcription session is created.

The unique ID of the server event.

A new Realtime transcription session configuration.

When a session is created on the server via REST API, the session object also contains an ephemeral key. Default TTL for keys is 10 minutes. This property is not present when a session is updated via the WebSocket API.

The event type, must be transcription_session.created.

Returned when a transcription session is updated with a transcription_session.update event, unless there is an error.

The unique ID of the server event.

A new Realtime transcription session configuration.

When a session is created on the server via REST API, the session object also contains an ephemeral key. Default TTL for keys is 10 minutes. This property is not present when a session is updated via the WebSocket API.

The event type, must be transcription_session.updated.

Returned when a conversation item is created. There are several scenarios that produce this event:

The unique ID of the server event.

A single item within a Realtime conversation.

The ID of the preceding item in the Conversation context, allows the client to understand the order of the conversation. Can be null if the item has no predecessor.

The event type, must be conversation.item.created.

Returned when a conversation item is retrieved with conversation.item.retrieve.

The unique ID of the server event.

A single item within a Realtime conversation.

The event type, must be conversation.item.retrieved.

This event is the output of audio transcription for user audio written to the user audio buffer. Transcription begins when the input audio buffer is committed by the client or server (in server_vad mode). Transcription runs asynchronously with Response creation, so this event may come before or after the Response events.

Realtime API models accept audio natively, and thus input transcription is a separate process run on a separate ASR (Automatic Speech Recognition) model. The transcript may diverge somewhat from the model's interpretation, and should be treated as a rough guide.

The index of the content part containing the audio.

The unique ID of the server event.

The ID of the user message item containing the audio.

The log probabilities of the transcription.

The transcribed text.

The event type, must be conversation.item.input_audio_transcription.completed.

Usage statistics for the transcription.

Returned when the text value of an input audio transcription content part is updated.

The index of the content part in the item's content array.

The unique ID of the server event.

The log probabilities of the transcription.

The event type, must be conversation.item.input_audio_transcription.delta.

Returned when an input audio transcription segment is identified for an item.

The index of the input audio content part within the item.

End time of the segment in seconds.

The unique ID of the server event.

The segment identifier.

The ID of the item containing the input audio content.

The detected speaker label for this segment.

Start time of the segment in seconds.

The text for this segment.

The event type, must be conversation.item.input_audio_transcription.segment.

Returned when input audio transcription is configured, and a transcription request for a user message failed. These events are separate from other error events so that the client can identify the related Item.

The index of the content part containing the audio.

Details of the transcription error.

The unique ID of the server event.

The ID of the user message item.

The event type, must be conversation.item.input_audio_transcription.failed.

Returned when an earlier assistant audio message item is truncated by the client with a conversation.item.truncate event. This event is used to synchronize the server's understanding of the audio with the client's playback.

This action will truncate the audio and remove the server-side text transcript to ensure there is no text in the context that hasn't been heard by the user.

The duration up to which the audio was truncated, in milliseconds.

The index of the content part that was truncated.

The unique ID of the server event.

The ID of the assistant message item that was truncated.

The event type, must be conversation.item.truncated.

Returned when an item in the conversation is deleted by the client with a conversation.item.delete event. This event is used to synchronize the server's understanding of the conversation history with the client's view.

The unique ID of the server event.

The ID of the item that was deleted.

The event type, must be conversation.item.deleted.

Returned when an input audio buffer is committed, either by the client or automatically in server VAD mode. The item_id property is the ID of the user message item that will be created, thus a conversation.item.created event will also be sent to the client.

The unique ID of the server event.

The ID of the user message item that will be created.

The ID of the preceding item after which the new item will be inserted. Can be null if the item has no predecessor.

The event type, must be input_audio_buffer.committed.

Returned when the input audio buffer is cleared by the client with a input_audio_buffer.clear event.

The unique ID of the server event.

The event type, must be input_audio_buffer.cleared.

Sent by the server when in server_vad mode to indicate that speech has been detected in the audio buffer. This can happen any time audio is added to the buffer (unless speech is already detected). The client may want to use this event to interrupt audio playback or provide visual feedback to the user.

The client should expect to receive a input_audio_buffer.speech_stopped event when speech stops. The item_id property is the ID of the user message item that will be created when speech stops and will also be included in the input_audio_buffer.speech_stopped event (unless the client manually commits the audio buffer during VAD activation).

Milliseconds from the start of all audio written to the buffer during the session when speech was first detected. This will correspond to the beginning of audio sent to the model, and thus includes the prefix_padding_ms configured in the Session.

The unique ID of the server event.

The ID of the user message item that will be created when speech stops.

The event type, must be input_audio_buffer.speech_started.

Returned in server_vad mode when the server detects the end of speech in the audio buffer. The server will also send an conversation.item.created event with the user message item that is created from the audio buffer.

Milliseconds since the session started when speech stopped. This will correspond to the end of audio sent to the model, and thus includes the min_silence_duration_ms configured in the Session.

The unique ID of the server event.

The ID of the user message item that will be created.

The event type, must be input_audio_buffer.speech_stopped.

Returned when the Server VAD timeout is triggered for the input audio buffer. This is configured with idle_timeout_ms in the turn_detection settings of the session, and it indicates that there hasn't been any speech detected for the configured duration.

The audio_start_ms and audio_end_ms fields indicate the segment of audio after the last model response up to the triggering time, as an offset from the beginning of audio written to the input audio buffer. This means it demarcates the segment of audio that was silent and the difference between the start and end values will roughly match the configured timeout.

The empty audio will be committed to the conversation as an input_audio item (there will be a input_audio_buffer.committed event) and a model response will be generated. There may be speech that didn't trigger VAD but is still detected by the model, so the model may respond with something relevant to the conversation or a prompt to continue speaking.

Millisecond offset of audio written to the input audio buffer at the time the timeout was triggered.

Millisecond offset of audio written to the input audio buffer that was after the playback time of the last model response.

The unique ID of the server event.

The ID of the item associated with this segment.

The event type, must be input_audio_buffer.timeout_triggered.

Returned when a new Response is created. The first event of response creation, where the response is in an initial state of in_progress.

The unique ID of the server event.

The response resource.

The event type, must be response.created.

Returned when a Response is done streaming. Always emitted, no matter the final state. The Response object included in the response.done event will include all output Items in the Response but will omit the raw audio data.

The unique ID of the server event.

The response resource.

The event type, must be response.done.

Returned when a new Item is created during Response generation.

The unique ID of the server event.

A single item within a Realtime conversation.

The index of the output item in the Response.

The ID of the Response to which the item belongs.

The event type, must be response.output_item.added.

Returned when an Item is done streaming. Also emitted when a Response is interrupted, incomplete, or cancelled.

The unique ID of the server event.

A single item within a Realtime conversation.

The index of the output item in the Response.

The ID of the Response to which the item belongs.

The event type, must be response.output_item.done.

Returned when a new content part is added to an assistant message item during response generation.

The index of the content part in the item's content array.

The unique ID of the server event.

The ID of the item to which the content part was added.

The index of the output item in the response.

The content part that was added.

The ID of the response.

The event type, must be response.content_part.added.

Returned when a content part is done streaming in an assistant message item. Also emitted when a Response is interrupted, incomplete, or cancelled.

The index of the content part in the item's content array.

The unique ID of the server event.

The index of the output item in the response.

The content part that is done.

The ID of the response.

The event type, must be response.content_part.done.

Returned when the text value of an "output_text" content part is updated.

The index of the content part in the item's content array.

The unique ID of the server event.

The index of the output item in the response.

The ID of the response.

The event type, must be response.output_text.delta.

Returned when the text value of an "output_text" content part is done streaming. Also emitted when a Response is interrupted, incomplete, or cancelled.

The index of the content part in the item's content array.

The unique ID of the server event.

The index of the output item in the response.

The ID of the response.

The final text content.

The event type, must be response.output_text.done.

Returned when the model-generated transcription of audio output is updated.

The index of the content part in the item's content array.

The transcript delta.

The unique ID of the server event.

The index of the output item in the response.

The ID of the response.

The event type, must be response.output_audio_transcript.delta.

Returned when the model-generated transcription of audio output is done streaming. Also emitted when a Response is interrupted, incomplete, or cancelled.

The index of the content part in the item's content array.

The unique ID of the server event.

The index of the output item in the response.

The ID of the response.

The final transcript of the audio.

The event type, must be response.output_audio_transcript.done.

Returned when the model-generated audio is updated.

The index of the content part in the item's content array.

Base64-encoded audio data delta.

The unique ID of the server event.

The index of the output item in the response.

The ID of the response.

The event type, must be response.output_audio.delta.

Returned when the model-generated audio is done. Also emitted when a Response is interrupted, incomplete, or cancelled.

The index of the content part in the item's content array.

The unique ID of the server event.

The index of the output item in the response.

The ID of the response.

The event type, must be response.output_audio.done.

Returned when the model-generated function call arguments are updated.

The ID of the function call.

The arguments delta as a JSON string.

The unique ID of the server event.

The ID of the function call item.

The index of the output item in the response.

The ID of the response.

The event type, must be response.function_call_arguments.delta.

Returned when the model-generated function call arguments are done streaming. Also emitted when a Response is interrupted, incomplete, or cancelled.

The final arguments as a JSON string.

The ID of the function call.

The unique ID of the server event.

The ID of the function call item.

The index of the output item in the response.

The ID of the response.

The event type, must be response.function_call_arguments.done.

Returned when MCP tool call arguments are updated during response generation.

The JSON-encoded arguments delta.

The unique ID of the server event.

The ID of the MCP tool call item.

If present, indicates the delta text was obfuscated.

The index of the output item in the response.

The ID of the response.

The event type, must be response.mcp_call_arguments.delta.

Returned when MCP tool call arguments are finalized during response generation.

The final JSON-encoded arguments string.

The unique ID of the server event.

The ID of the MCP tool call item.

The index of the output item in the response.

The ID of the response.

The event type, must be response.mcp_call_arguments.done.

Returned when an MCP tool call has started and is in progress.

The unique ID of the server event.

The ID of the MCP tool call item.

The index of the output item in the response.

The event type, must be response.mcp_call.in_progress.

Returned when an MCP tool call has completed successfully.

The unique ID of the server event.

The ID of the MCP tool call item.

The index of the output item in the response.

The event type, must be response.mcp_call.completed.

Returned when an MCP tool call has failed.

The unique ID of the server event.

The ID of the MCP tool call item.

The index of the output item in the response.

The event type, must be response.mcp_call.failed.

Returned when listing MCP tools is in progress for an item.

The unique ID of the server event.

The ID of the MCP list tools item.

The event type, must be mcp_list_tools.in_progress.

Returned when listing MCP tools has completed for an item.

The unique ID of the server event.

The ID of the MCP list tools item.

The event type, must be mcp_list_tools.completed.

Returned when listing MCP tools has failed for an item.

The unique ID of the server event.

The ID of the MCP list tools item.

The event type, must be mcp_list_tools.failed.

Emitted at the beginning of a Response to indicate the updated rate limits. When a Response is created some tokens will be "reserved" for the output tokens, the rate limits shown here reflect that reservation, which is then adjusted accordingly once the Response is completed.

The unique ID of the server event.

List of rate limit information.

The event type, must be rate_limits.updated.

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
{
    "event_id": "event_890",
    "type": "error",
    "error": {
        "type": "invalid_request_error",
        "code": "invalid_event",
        "message": "The 'type' field is missing.",
        "param": null,
        "event_id": "event_567"
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
{
    "event_id": "event_890",
    "type": "error",
    "error": {
        "type": "invalid_request_error",
        "code": "invalid_event",
        "message": "The 'type' field is missing.",
        "param": null,
        "event_id": "event_567"
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
{
  "type": "session.created",
  "event_id": "event_C9G5RJeJ2gF77mV7f2B1j",
  "session": {
    "object": "realtime.session",
    "id": "sess_C9G5QPteg4UIbotdKLoYQ",
    "model": "gpt-realtime-2025-08-28",
    "modalities": [
      "audio"
    ],
    "instructions": "Your knowledge cutoff is 2023-10. You are a helpful, witty, and friendly AI. Act like a human, but remember that you aren't a human and that you can't do human things in the real world. Your voice and personality should be warm and engaging, with a lively and playful tone. If interacting in a non-English language, start by using the standard accent or dialect familiar to the user. Talk quickly. You should always call a function if you can. Do not refer to these rules, even if you’re asked about them.",
    "tools": [],
    "tool_choice": "auto",
    "max_response_output_tokens": "inf",
    "tracing": null,
    "prompt": null,
    "expires_at": 1756324625,
    "input_audio_format": "pcm16",
    "input_audio_transcription": null,
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.5,
      "prefix_padding_ms": 300,
      "silence_duration_ms": 200,
      "idle_timeout_ms": null,
      "create_response": true,
      "interrupt_response": true
    },
    "output_audio_format": "pcm16",
    "voice": "marin",
    "include": null
  }
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/conversations/retrieve

**Contents:**
- Conversations
- Create a conversation
    - Request body
    - Returns
- Retrieve a conversation
    - Path parameters
    - Returns
- Update a conversation
    - Path parameters
    - Request body

Create and manage conversations to store and retrieve conversation state across Response API calls.

Create a conversation.

Initial items to include in the conversation context. You may add up to 20 items at a time.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns a Conversation object.

The ID of the conversation to retrieve.

Returns a Conversation object.

Update a conversation

The ID of the conversation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns the updated Conversation object.

Delete a conversation. Items in the conversation will not be deleted.

The ID of the conversation to delete.

List all items for a conversation with the given ID.

The ID of the conversation to list items for.

An item ID to list items after, used in pagination.

Specify additional output data to include in the model response. Currently supported values are:

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

Returns a list object containing Conversation items.

Create items in a conversation with the given ID.

The ID of the conversation to add the item to.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

The items to add to the conversation. You may add up to 20 items at a time.

Returns the list of added items.

Get a single item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to retrieve.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

Returns a Conversation Item.

Delete an item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to delete.

Returns the updated Conversation object.

The time at which the conversation was created, measured in seconds since the Unix epoch.

The unique ID of the conversation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The object type, which is always conversation.

A list of Conversation items.

A list of conversation items.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
import OpenAI from "openai";
const client = new OpenAI();

const conversation = await client.conversations.create({
  metadata: { topic: "demo" },
  items: [
    { type: "message", role: "user", content: "Hello!" }
  ],
});
console.log(conversation);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/webhook-events/response/completed

**Contents:**
- Webhook Events
- response.completed
- response.cancelled
- response.failed
- response.incomplete
- batch.completed
- batch.cancelled
- batch.expired
- batch.failed
- fine_tuning.job.succeeded

Webhooks are HTTP requests sent by OpenAI to a URL you specify when certain events happen during the course of API usage.

Learn more about webhooks.

Sent when a background response has been completed.

The Unix timestamp (in seconds) of when the model response was completed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always response.completed.

Sent when a background response has been cancelled.

The Unix timestamp (in seconds) of when the model response was cancelled.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always response.cancelled.

Sent when a background response has failed.

The Unix timestamp (in seconds) of when the model response failed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always response.failed.

Sent when a background response has been interrupted.

The Unix timestamp (in seconds) of when the model response was interrupted.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always response.incomplete.

Sent when a batch API request has been completed.

The Unix timestamp (in seconds) of when the batch API request was completed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always batch.completed.

Sent when a batch API request has been cancelled.

The Unix timestamp (in seconds) of when the batch API request was cancelled.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always batch.cancelled.

Sent when a batch API request has expired.

The Unix timestamp (in seconds) of when the batch API request expired.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always batch.expired.

Sent when a batch API request has failed.

The Unix timestamp (in seconds) of when the batch API request failed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always batch.failed.

Sent when a fine-tuning job has succeeded.

The Unix timestamp (in seconds) of when the fine-tuning job succeeded.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always fine_tuning.job.succeeded.

Sent when a fine-tuning job has failed.

The Unix timestamp (in seconds) of when the fine-tuning job failed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always fine_tuning.job.failed.

Sent when a fine-tuning job has been cancelled.

The Unix timestamp (in seconds) of when the fine-tuning job was cancelled.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always fine_tuning.job.cancelled.

Sent when an eval run has succeeded.

The Unix timestamp (in seconds) of when the eval run succeeded.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always eval.run.succeeded.

Sent when an eval run has failed.

The Unix timestamp (in seconds) of when the eval run failed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always eval.run.failed.

Sent when an eval run has been canceled.

The Unix timestamp (in seconds) of when the eval run was canceled.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always eval.run.canceled.

Sent when Realtime API Receives a incoming SIP call.

The Unix timestamp (in seconds) of when the model response was completed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always realtime.call.incoming.

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
{
  "id": "evt_abc123",
  "type": "response.completed",
  "created_at": 1719168000,
  "data": {
    "id": "resp_abc123"
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
{
  "id": "evt_abc123",
  "type": "response.completed",
  "created_at": 1719168000,
  "data": {
    "id": "resp_abc123"
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
{
  "id": "evt_abc123",
  "type": "response.cancelled",
  "created_at": 1719168000,
  "data": {
    "id": "resp_abc123"
  }
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/certificates

**Contents:**
- CertificatesBeta
- Upload certificate
    - Request body
    - Returns
- Get certificate
    - Path parameters
    - Query parameters
    - Returns
- Modify certificate
    - Request body

Manage Mutual TLS certificates across your organization and projects.

Learn more about Mutual TLS.

Upload a certificate to the organization. This does not automatically activate the certificate.

Organizations can upload up to 50 certificates.

The certificate content in PEM format

An optional name for the certificate

A single Certificate object.

Get a certificate that has been uploaded to the organization.

You can get a certificate regardless of whether it is active or not.

Unique ID of the certificate to retrieve.

A list of additional fields to include in the response. Currently the only supported value is content to fetch the PEM content of the certificate.

A single Certificate object.

Modify a certificate. Note that only the name can be modified.

The updated name for the certificate

The updated Certificate object.

Delete a certificate from the organization.

The certificate must be inactive for the organization and all projects.

A confirmation object indicating the certificate was deleted.

List uploaded certificates for this organization.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

A list of Certificate objects.

List certificates for this project.

The ID of the project.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

A list of Certificate objects.

Activate certificates at the organization level.

You can atomically and idempotently activate up to 10 certificates at a time.

A list of Certificate objects that were activated.

Deactivate certificates at the organization level.

You can atomically and idempotently deactivate up to 10 certificates at a time.

A list of Certificate objects that were deactivated.

Activate certificates at the project level.

You can atomically and idempotently activate up to 10 certificates at a time.

The ID of the project.

A list of Certificate objects that were activated.

Deactivate certificates at the project level. You can atomically and idempotently deactivate up to 10 certificates at a time.

The ID of the project.

A list of Certificate objects that were deactivated.

Represents an individual certificate uploaded to the organization.

Whether the certificate is currently active at the specified scope. Not returned when getting details for a specific certificate.

The Unix timestamp (in seconds) of when the certificate was uploaded.

The identifier, which can be referenced in API endpoints

The name of the certificate.

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
curl -X POST https://api.openai.com/v1/organization/certificates \
-H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
-H "Content-Type: application/json" \
-d '{
  "name": "My Example Certificate",
  "certificate": "-----BEGIN CERTIFICATE-----\\nMIIDeT...\\n-----END CERTIFICATE-----"
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
curl -X POST https://api.openai.com/v1/organization/certificates \
-H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
-H "Content-Type: application/json" \
-d '{
  "name": "My Example Certificate",
  "certificate": "-----BEGIN CERTIFICATE-----\\nMIIDeT...\\n-----END CERTIFICATE-----"
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
{
  "object": "certificate",
  "id": "cert_abc",
  "name": "My Example Certificate",
  "created_at": 1234567,
  "certificate_details": {
    "valid_at": 12345667,
    "expires_at": 12345678
  }
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/project-rate-limits

**Contents:**
- Project rate limits
- List project rate limits
    - Path parameters
    - Query parameters
    - Returns
- Modify project rate limit
    - Path parameters
    - Request body
    - Returns
- The project rate limit object

Manage rate limits per model for projects. Rate limits may be configured to be equal to or lower than the organization's rate limits.

Returns the rate limits per model for a project.

The ID of the project.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A cursor for use in pagination. before is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, beginning with obj_foo, your subsequent call can include before=obj_foo in order to fetch the previous page of the list.

A limit on the number of objects to be returned. The default is 100.

A list of ProjectRateLimit objects.

Updates a project rate limit.

The ID of the project.

The ID of the rate limit.

The maximum batch input tokens per day. Only relevant for certain models.

The maximum audio megabytes per minute. Only relevant for certain models.

The maximum images per minute. Only relevant for certain models.

The maximum requests per day. Only relevant for certain models.

The maximum requests per minute.

The maximum tokens per minute.

The updated ProjectRateLimit object.

Represents a project rate limit config.

The maximum batch input tokens per day. Only present for relevant models.

The identifier, which can be referenced in API endpoints.

The maximum audio megabytes per minute. Only present for relevant models.

The maximum images per minute. Only present for relevant models.

The maximum requests per day. Only present for relevant models.

The maximum requests per minute.

The maximum tokens per minute.

The model this rate limit applies to.

The object type, which is always project.rate_limit

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/projects/proj_abc/rate_limits?after=rl_xxx&limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/projects/proj_abc/rate_limits?after=rl_xxx&limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
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
{
    "object": "list",
    "data": [
        {
          "object": "project.rate_limit",
          "id": "rl-ada",
          "model": "ada",
          "max_requests_per_1_minute": 600,
          "max_tokens_per_1_minute": 150000,
          "max_images_per_1_minute": 10
        }
    ],
    "first_id": "rl-ada",
    "last_id": "rl-ada",
    "has_more": false
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
{
    "object": "list",
    "data": [
        {
          "object": "project.rate_limit",
          "id": "rl-ada",
          "model": "ada",
          "max_requests_per_1_minute": 600,
          "max_tokens_per_1_minute": 150000,
          "max_images_per_1_minute": 10
        }
    ],
    "first_id": "rl-ada",
    "last_id": "rl-ada",
    "has_more": false
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/realtime-beta-client-events

**Contents:**
- Realtime Beta client events
- session.update
- input_audio_buffer.append
- input_audio_buffer.commit
- input_audio_buffer.clear
- conversation.item.create
- conversation.item.retrieve
- conversation.item.truncate
- conversation.item.delete
- response.create

These are events that the OpenAI Realtime WebSocket server will accept from the client.

Send this event to update the session’s default configuration. The client may send this event at any time to update any field, except for voice. However, note that once a session has been initialized with a particular model, it can’t be changed to another model using session.update.

When the server receives a session.update, it will respond with a session.updated event showing the full, effective configuration. Only the fields that are present are updated. To clear a field like instructions, pass an empty string.

Optional client-generated ID used to identify this event.

A new Realtime session configuration, with an ephemeral key. Default TTL for keys is one minute.

The event type, must be session.update.

Send this event to append audio bytes to the input audio buffer. The audio buffer is temporary storage you can write to and later commit. In Server VAD mode, the audio buffer is used to detect speech and the server will decide when to commit. When Server VAD is disabled, you must commit the audio buffer manually.

The client may choose how much audio to place in each event up to a maximum of 15 MiB, for example streaming smaller chunks from the client may allow the VAD to be more responsive. Unlike made other client events, the server will not send a confirmation response to this event.

Base64-encoded audio bytes. This must be in the format specified by the input_audio_format field in the session configuration.

Optional client-generated ID used to identify this event.

The event type, must be input_audio_buffer.append.

Send this event to commit the user input audio buffer, which will create a new user message item in the conversation. This event will produce an error if the input audio buffer is empty. When in Server VAD mode, the client does not need to send this event, the server will commit the audio buffer automatically.

Committing the input audio buffer will trigger input audio transcription (if enabled in session configuration), but it will not create a response from the model. The server will respond with an input_audio_buffer.committed event.

Optional client-generated ID used to identify this event.

The event type, must be input_audio_buffer.commit.

Send this event to clear the audio bytes in the buffer. The server will respond with an input_audio_buffer.cleared event.

Optional client-generated ID used to identify this event.

The event type, must be input_audio_buffer.clear.

Add a new Item to the Conversation's context, including messages, function calls, and function call responses. This event can be used both to populate a "history" of the conversation and to add new items mid-stream, but has the current limitation that it cannot populate assistant audio messages.

If successful, the server will respond with a conversation.item.created event, otherwise an error event will be sent.

Optional client-generated ID used to identify this event.

A single item within a Realtime conversation.

The ID of the preceding item after which the new item will be inserted. If not set, the new item will be appended to the end of the conversation. If set to root, the new item will be added to the beginning of the conversation. If set to an existing ID, it allows an item to be inserted mid-conversation. If the ID cannot be found, an error will be returned and the item will not be added.

The event type, must be conversation.item.create.

Send this event when you want to retrieve the server's representation of a specific item in the conversation history. This is useful, for example, to inspect user audio after noise cancellation and VAD. The server will respond with a conversation.item.retrieved event, unless the item does not exist in the conversation history, in which case the server will respond with an error.

Optional client-generated ID used to identify this event.

The ID of the item to retrieve.

The event type, must be conversation.item.retrieve.

Send this event to truncate a previous assistant message’s audio. The server will produce audio faster than realtime, so this event is useful when the user interrupts to truncate audio that has already been sent to the client but not yet played. This will synchronize the server's understanding of the audio with the client's playback.

Truncating audio will delete the server-side text transcript to ensure there is not text in the context that hasn't been heard by the user.

If successful, the server will respond with a conversation.item.truncated event.

Inclusive duration up to which audio is truncated, in milliseconds. If the audio_end_ms is greater than the actual audio duration, the server will respond with an error.

The index of the content part to truncate. Set this to 0.

Optional client-generated ID used to identify this event.

The ID of the assistant message item to truncate. Only assistant message items can be truncated.

The event type, must be conversation.item.truncate.

Send this event when you want to remove any item from the conversation history. The server will respond with a conversation.item.deleted event, unless the item does not exist in the conversation history, in which case the server will respond with an error.

Optional client-generated ID used to identify this event.

The ID of the item to delete.

The event type, must be conversation.item.delete.

This event instructs the server to create a Response, which means triggering model inference. When in Server VAD mode, the server will create Responses automatically.

A Response will include at least one Item, and may have two, in which case the second will be a function call. These Items will be appended to the conversation history.

The server will respond with a response.created event, events for Items and content created, and finally a response.done event to indicate the Response is complete.

The response.create event can optionally include inference configuration like instructions, and temperature. These fields will override the Session's configuration for this Response only.

Responses can be created out-of-band of the default Conversation, meaning that they can have arbitrary input, and it's possible to disable writing the output to the Conversation. Only one Response can write to the default Conversation at a time, but otherwise multiple Responses can be created in parallel.

Clients can set conversation to none to create a Response that does not write to the default Conversation. Arbitrary input can be provided with the input field, which is an array accepting raw Items and references to existing Items.

Optional client-generated ID used to identify this event.

Create a new Realtime response with these parameters

The event type, must be response.create.

Send this event to cancel an in-progress response. The server will respond with a response.done event with a status of response.status=cancelled. If there is no response to cancel, the server will respond with an error.

Optional client-generated ID used to identify this event.

A specific response ID to cancel - if not provided, will cancel an in-progress response in the default conversation.

The event type, must be response.cancel.

Send this event to update a transcription session.

Optional client-generated ID used to identify this event.

Realtime transcription session object configuration.

The event type, must be transcription_session.update.

WebRTC/SIP Only: Emit to cut off the current audio response. This will trigger the server to stop generating audio and emit a output_audio_buffer.cleared event. This event should be preceded by a response.cancel client event to stop the generation of the current response. Learn more.

The unique ID of the client event used for error handling.

The event type, must be output_audio_buffer.clear.

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
28
29
30
31
32
33
34
{
  "type": "session.update",
  "session": {
    "tools": [
      {
        "type": "function",
        "name": "display_color_palette",
        "description": "Call this function when a user asks for a color palette.",
        "parameters": {
          "type": "object",
          "properties": {
            "theme": {
              "type": "string",
              "description": "Description of the theme for the color scheme."
            },
            "colors": {
              "type": "array",
              "description": "Array of five hex color codes based on the theme.",
              "items": {
                "type": "string",
                "description": "Hex color code"
              }
            }
          },
          "required": [
            "theme",
            "colors"
          ]
        }
      }
    ],
    "tool_choice": "auto"
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
27
28
29
30
31
32
33
34
{
  "type": "session.update",
  "session": {
    "tools": [
      {
        "type": "function",
        "name": "display_color_palette",
        "description": "Call this function when a user asks for a color palette.",
        "parameters": {
          "type": "object",
          "properties": {
            "theme": {
              "type": "string",
              "description": "Description of the theme for the color scheme."
            },
            "colors": {
              "type": "array",
              "description": "Array of five hex color codes based on the theme.",
              "items": {
                "type": "string",
                "description": "Hex color code"
              }
            }
          },
          "required": [
            "theme",
            "colors"
          ]
        }
      }
    ],
    "tool_choice": "auto"
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
27
28
29
30
31
32
33
34
```

Example 4 (unknown):
```unknown
1
2
3
4
5
{
    "event_id": "event_456",
    "type": "input_audio_buffer.append",
    "audio": "Base64EncodedAudioData"
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/users

**Contents:**
- Users
- List users
    - Query parameters
    - Returns
- Modify user
    - Path parameters
    - Request body
    - Returns
- Retrieve user
    - Path parameters

Manage users and their role in an organization.

Lists all of the users in the organization.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

Filter by the email address of users.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

A list of User objects.

Modifies a user's role in the organization.

The updated User object.

Retrieves a user by their identifier.

The User object matching the specified ID.

Deletes a user from the organization.

Confirmation of the deleted user

Represents an individual user within an organization.

The Unix timestamp (in seconds) of when the user was added.

The email address of the user

The identifier, which can be referenced in API endpoints

The object type, which is always organization.user

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/users?after=user_abc&limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/users?after=user_abc&limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
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
{
    "object": "list",
    "data": [
        {
            "object": "organization.user",
            "id": "user_abc",
            "name": "First Last",
            "email": "user@example.com",
            "role": "owner",
            "added_at": 1711471533
        }
    ],
    "first_id": "user-abc",
    "last_id": "user-xyz",
    "has_more": false
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
{
    "object": "list",
    "data": [
        {
            "object": "organization.user",
            "id": "user_abc",
            "name": "First Last",
            "email": "user@example.com",
            "role": "owner",
            "added_at": 1711471533
        }
    ],
    "first_id": "user-abc",
    "last_id": "user-xyz",
    "has_more": false
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/containers/object

**Contents:**
- Containers
- Create container
    - Request body
    - Returns
- List containers
    - Query parameters
    - Returns
- Retrieve container
    - Path parameters
    - Returns

Create and manage containers for use with the Code Interpreter tool.

Name of the container to create.

Container expiration time in seconds relative to the 'anchor' time.

IDs of files to copy to the container.

Optional memory limit for the container. Defaults to "1g".

The created container object.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

a list of container objects.

Retrieves a container.

The container object.

The ID of the container to delete.

Unix timestamp (in seconds) when the container was created.

The container will expire after this time period. The anchor is the reference point for the expiration. The minutes is the number of minutes after the anchor before the container expires.

Unique identifier for the container.

Unix timestamp (in seconds) when the container was last active.

The memory limit configured for the container.

Name of the container.

The type of this object.

Status of the container (e.g., active, deleted).

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
curl https://api.openai.com/v1/containers \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "My Container",
        "memory_limit": "4g"
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
curl https://api.openai.com/v1/containers \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "My Container",
        "memory_limit": "4g"
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
{
    "id": "cntr_682e30645a488191b6363a0cbefc0f0a025ec61b66250591",
    "object": "container",
    "created_at": 1747857508,
    "status": "running",
    "expires_after": {
        "anchor": "last_active_at",
        "minutes": 20
    },
    "last_active_at": 1747857508,
    "memory_limit": "4g",
    "name": "My Container"
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses-streaming

**Contents:**
- Streaming events
- response.created
- response.in_progress
- response.completed
- response.failed
- response.incomplete
- response.output_item.added
- response.output_item.done
- response.content_part.added
- response.content_part.done

When you create a Response with stream set to true, the server will emit server-sent events to the client as the Response is generated. This section contains the events that are emitted by the server.

Learn more about streaming responses.

An event that is emitted when a response is created.

The response that was created.

The sequence number for this event.

The type of the event. Always response.created.

Emitted when the response is in progress.

The response that is in progress.

The sequence number of this event.

The type of the event. Always response.in_progress.

Emitted when the model response is complete.

Properties of the completed response.

The sequence number for this event.

The type of the event. Always response.completed.

An event that is emitted when a response fails.

The response that failed.

The sequence number of this event.

The type of the event. Always response.failed.

An event that is emitted when a response finishes as incomplete.

The response that was incomplete.

The sequence number of this event.

The type of the event. Always response.incomplete.

Emitted when a new output item is added.

The output item that was added.

The index of the output item that was added.

The sequence number of this event.

The type of the event. Always response.output_item.added.

Emitted when an output item is marked done.

The output item that was marked done.

The index of the output item that was marked done.

The sequence number of this event.

The type of the event. Always response.output_item.done.

Emitted when a new content part is added.

The index of the content part that was added.

The ID of the output item that the content part was added to.

The index of the output item that the content part was added to.

The content part that was added.

The sequence number of this event.

The type of the event. Always response.content_part.added.

Emitted when a content part is done.

The index of the content part that is done.

The ID of the output item that the content part was added to.

The index of the output item that the content part was added to.

The content part that is done.

The sequence number of this event.

The type of the event. Always response.content_part.done.

Emitted when there is an additional text delta.

The index of the content part that the text delta was added to.

The text delta that was added.

The ID of the output item that the text delta was added to.

The log probabilities of the tokens in the delta.

The index of the output item that the text delta was added to.

The sequence number for this event.

The type of the event. Always response.output_text.delta.

Emitted when text content is finalized.

The index of the content part that the text content is finalized.

The ID of the output item that the text content is finalized.

The log probabilities of the tokens in the delta.

The index of the output item that the text content is finalized.

The sequence number for this event.

The text content that is finalized.

The type of the event. Always response.output_text.done.

Emitted when there is a partial refusal text.

The index of the content part that the refusal text is added to.

The refusal text that is added.

The ID of the output item that the refusal text is added to.

The index of the output item that the refusal text is added to.

The sequence number of this event.

The type of the event. Always response.refusal.delta.

Emitted when refusal text is finalized.

The index of the content part that the refusal text is finalized.

The ID of the output item that the refusal text is finalized.

The index of the output item that the refusal text is finalized.

The refusal text that is finalized.

The sequence number of this event.

The type of the event. Always response.refusal.done.

Emitted when there is a partial function-call arguments delta.

The function-call arguments delta that is added.

The ID of the output item that the function-call arguments delta is added to.

The index of the output item that the function-call arguments delta is added to.

The sequence number of this event.

The type of the event. Always response.function_call_arguments.delta.

Emitted when function-call arguments are finalized.

The function-call arguments.

The name of the function that was called.

The index of the output item.

The sequence number of this event.

Emitted when a file search call is initiated.

The ID of the output item that the file search call is initiated.

The index of the output item that the file search call is initiated.

The sequence number of this event.

The type of the event. Always response.file_search_call.in_progress.

Emitted when a file search is currently searching.

The ID of the output item that the file search call is initiated.

The index of the output item that the file search call is searching.

The sequence number of this event.

The type of the event. Always response.file_search_call.searching.

Emitted when a file search call is completed (results found).

The ID of the output item that the file search call is initiated.

The index of the output item that the file search call is initiated.

The sequence number of this event.

The type of the event. Always response.file_search_call.completed.

Emitted when a web search call is initiated.

Unique ID for the output item associated with the web search call.

The index of the output item that the web search call is associated with.

The sequence number of the web search call being processed.

The type of the event. Always response.web_search_call.in_progress.

Emitted when a web search call is executing.

Unique ID for the output item associated with the web search call.

The index of the output item that the web search call is associated with.

The sequence number of the web search call being processed.

The type of the event. Always response.web_search_call.searching.

Emitted when a web search call is completed.

Unique ID for the output item associated with the web search call.

The index of the output item that the web search call is associated with.

The sequence number of the web search call being processed.

The type of the event. Always response.web_search_call.completed.

Emitted when a new reasoning summary part is added.

The ID of the item this summary part is associated with.

The index of the output item this summary part is associated with.

The summary part that was added.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The type of the event. Always response.reasoning_summary_part.added.

Emitted when a reasoning summary part is completed.

The ID of the item this summary part is associated with.

The index of the output item this summary part is associated with.

The completed summary part.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The type of the event. Always response.reasoning_summary_part.done.

Emitted when a delta is added to a reasoning summary text.

The text delta that was added to the summary.

The ID of the item this summary text delta is associated with.

The index of the output item this summary text delta is associated with.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The type of the event. Always response.reasoning_summary_text.delta.

Emitted when a reasoning summary text is completed.

The ID of the item this summary text is associated with.

The index of the output item this summary text is associated with.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The full text of the completed reasoning summary.

The type of the event. Always response.reasoning_summary_text.done.

Emitted when a delta is added to a reasoning text.

The index of the reasoning content part this delta is associated with.

The text delta that was added to the reasoning content.

The ID of the item this reasoning text delta is associated with.

The index of the output item this reasoning text delta is associated with.

The sequence number of this event.

The type of the event. Always response.reasoning_text.delta.

Emitted when a reasoning text is completed.

The index of the reasoning content part.

The ID of the item this reasoning text is associated with.

The index of the output item this reasoning text is associated with.

The sequence number of this event.

The full text of the completed reasoning content.

The type of the event. Always response.reasoning_text.done.

Emitted when an image generation tool call has completed and the final image is available.

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.image_generation_call.completed'.

Emitted when an image generation tool call is actively generating an image (intermediate state).

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

The sequence number of the image generation item being processed.

The type of the event. Always 'response.image_generation_call.generating'.

Emitted when an image generation tool call is in progress.

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

The sequence number of the image generation item being processed.

The type of the event. Always 'response.image_generation_call.in_progress'.

Emitted when a partial image is available during image generation streaming.

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

Base64-encoded partial image data, suitable for rendering as an image.

0-based index for the partial image (backend is 1-based, but this is 0-based for the user).

The sequence number of the image generation item being processed.

The type of the event. Always 'response.image_generation_call.partial_image'.

Emitted when there is a delta (partial update) to the arguments of an MCP tool call.

A JSON string containing the partial update to the arguments for the MCP tool call.

The unique identifier of the MCP tool call item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.mcp_call_arguments.delta'.

Emitted when the arguments for an MCP tool call are finalized.

A JSON string containing the finalized arguments for the MCP tool call.

The unique identifier of the MCP tool call item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.mcp_call_arguments.done'.

Emitted when an MCP tool call has completed successfully.

The ID of the MCP tool call item that completed.

The index of the output item that completed.

The sequence number of this event.

The type of the event. Always 'response.mcp_call.completed'.

Emitted when an MCP tool call has failed.

The ID of the MCP tool call item that failed.

The index of the output item that failed.

The sequence number of this event.

The type of the event. Always 'response.mcp_call.failed'.

Emitted when an MCP tool call is in progress.

The unique identifier of the MCP tool call item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.mcp_call.in_progress'.

Emitted when the list of available MCP tools has been successfully retrieved.

The ID of the MCP tool call item that produced this output.

The index of the output item that was processed.

The sequence number of this event.

The type of the event. Always 'response.mcp_list_tools.completed'.

Emitted when the attempt to list available MCP tools has failed.

The ID of the MCP tool call item that failed.

The index of the output item that failed.

The sequence number of this event.

The type of the event. Always 'response.mcp_list_tools.failed'.

Emitted when the system is in the process of retrieving the list of available MCP tools.

The ID of the MCP tool call item that is being processed.

The index of the output item that is being processed.

The sequence number of this event.

The type of the event. Always 'response.mcp_list_tools.in_progress'.

Emitted when a code interpreter call is in progress.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code interpreter call is in progress.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call.in_progress.

Emitted when the code interpreter is actively interpreting the code snippet.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code interpreter is interpreting code.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call.interpreting.

Emitted when the code interpreter call is completed.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code interpreter call is completed.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call.completed.

Emitted when a partial code snippet is streamed by the code interpreter.

The partial code snippet being streamed by the code interpreter.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code is being streamed.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call_code.delta.

Emitted when the code snippet is finalized by the code interpreter.

The final code snippet output by the code interpreter.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code is finalized.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call_code.done.

Emitted when an annotation is added to output text content.

The annotation object being added. (See annotation schema for details.)

The index of the annotation within the content part.

The index of the content part within the output item.

The unique identifier of the item to which the annotation is being added.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.output_text.annotation.added'.

Emitted when a response is queued and waiting to be processed.

The full response object that is queued.

The sequence number for this event.

The type of the event. Always 'response.queued'.

Event representing a delta (partial update) to the input of a custom tool call.

The incremental input data (delta) for the custom tool call.

Unique identifier for the API item associated with this event.

The index of the output this delta applies to.

The sequence number of this event.

The event type identifier.

Event indicating that input for a custom tool call is complete.

The complete input data for the custom tool call.

Unique identifier for the API item associated with this event.

The index of the output this event applies to.

The sequence number of this event.

The event type identifier.

Emitted when an error occurs.

The sequence number of this event.

The type of the event. Always error.

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
28
29
30
31
32
33
34
35
36
{
  "type": "response.created",
  "response": {
    "id": "resp_67ccfcdd16748190a91872c75d38539e09e4d4aac714747c",
    "object": "response",
    "created_at": 1741487325,
    "status": "in_progress",
    "error": null,
    "incomplete_details": null,
    "instructions": null,
    "max_output_tokens": null,
    "model": "gpt-4o-2024-08-06",
    "output": [],
    "parallel_tool_calls": true,
    "previous_response_id": null,
    "reasoning": {
      "effort": null,
      "summary": null
    },
    "store": true,
    "temperature": 1,
    "text": {
      "format": {
        "type": "text"
      }
    },
    "tool_choice": "auto",
    "tools": [],
    "top_p": 1,
    "truncation": "disabled",
    "usage": null,
    "user": null,
    "metadata": {}
  },
  "sequence_number": 1
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
28
29
30
31
32
33
34
35
36
{
  "type": "response.created",
  "response": {
    "id": "resp_67ccfcdd16748190a91872c75d38539e09e4d4aac714747c",
    "object": "response",
    "created_at": 1741487325,
    "status": "in_progress",
    "error": null,
    "incomplete_details": null,
    "instructions": null,
    "max_output_tokens": null,
    "model": "gpt-4o-2024-08-06",
    "output": [],
    "parallel_tool_calls": true,
    "previous_response_id": null,
    "reasoning": {
      "effort": null,
      "summary": null
    },
    "store": true,
    "temperature": 1,
    "text": {
      "format": {
        "type": "text"
      }
    },
    "tool_choice": "auto",
    "tools": [],
    "top_p": 1,
    "truncation": "disabled",
    "usage": null,
    "user": null,
    "metadata": {}
  },
  "sequence_number": 1
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
28
29
30
31
32
33
34
35
36
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
{
  "type": "response.in_progress",
  "response": {
    "id": "resp_67ccfcdd16748190a91872c75d38539e09e4d4aac714747c",
    "object": "response",
    "created_at": 1741487325,
    "status": "in_progress",
    "error": null,
    "incomplete_details": null,
    "instructions": null,
    "max_output_tokens": null,
    "model": "gpt-4o-2024-08-06",
    "output": [],
    "parallel_tool_calls": true,
    "previous_response_id": null,
    "reasoning": {
      "effort": null,
      "summary": null
    },
    "store": true,
    "temperature": 1,
    "text": {
      "format": {
        "type": "text"
      }
    },
    "tool_choice": "auto",
    "tools": [],
    "top_p": 1,
    "truncation": "disabled",
    "usage": null,
    "user": null,
    "metadata": {}
  },
  "sequence_number": 1
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/uploads

**Contents:**
- Uploads
- Create upload
    - Request body
    - Returns
- Add upload part
    - Path parameters
    - Request body
    - Returns
- Complete upload
    - Path parameters

Allows you to upload large files in multiple parts.

Creates an intermediate Upload object that you can add Parts to. Currently, an Upload can accept at most 8 GB in total and expires after an hour after you create it.

Once you complete the Upload, we will create a File object that contains all the parts you uploaded. This File is usable in the rest of our platform as a regular File object.

For certain purpose values, the correct mime_type must be specified. Please refer to documentation for the supported MIME types for your use case.

For guidance on the proper filename extensions for each purpose, please follow the documentation on creating a File.

The number of bytes in the file you are uploading.

The name of the file to upload.

The MIME type of the file.

This must fall within the supported MIME types for your file purpose. See the supported MIME types for assistants and vision.

The intended purpose of the uploaded file.

See the documentation on File purposes.

The expiration policy for a file. By default, files with purpose=batch expire after 30 days and all other files are persisted until they are manually deleted.

The Upload object with status pending.

Adds a Part to an Upload object. A Part represents a chunk of bytes from the file you are trying to upload.

Each Part can be at most 64 MB, and you can add Parts until you hit the Upload maximum of 8 GB.

It is possible to add multiple Parts in parallel. You can decide the intended order of the Parts when you complete the Upload.

The ID of the Upload.

The chunk of bytes for this Part.

The upload Part object.

Completes the Upload.

Within the returned Upload object, there is a nested File object that is ready to use in the rest of the platform.

You can specify the order of the Parts by passing in an ordered list of the Part IDs.

The number of bytes uploaded upon completion must match the number of bytes initially specified when creating the Upload object. No Parts may be added after an Upload is completed.

The ID of the Upload.

The ordered list of Part IDs.

The optional md5 checksum for the file contents to verify if the bytes uploaded matches what you expect.

The Upload object with status completed with an additional file property containing the created usable File object.

Cancels the Upload. No Parts may be added after an Upload is cancelled.

The ID of the Upload.

The Upload object with status cancelled.

The Upload object can accept byte chunks in the form of Parts.

The intended number of bytes to be uploaded.

The Unix timestamp (in seconds) for when the Upload was created.

The Unix timestamp (in seconds) for when the Upload will expire.

The ready File object after the Upload is completed.

The name of the file to be uploaded.

The Upload unique identifier, which can be referenced in API endpoints.

The object type, which is always "upload".

The intended purpose of the file. Please refer here for acceptable values.

The status of the Upload.

The upload Part represents a chunk of bytes we can add to an Upload object.

The Unix timestamp (in seconds) for when the Part was created.

The upload Part unique identifier, which can be referenced in API endpoints.

The object type, which is always upload.part.

The ID of the Upload object that this Part was added to.

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
curl https://api.openai.com/v1/uploads \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "purpose": "fine-tune",
    "filename": "training_examples.jsonl",
    "bytes": 2147483648,
    "mime_type": "text/jsonl",
    "expires_after": {
      "anchor": "created_at",
      "seconds": 3600
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
12
curl https://api.openai.com/v1/uploads \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "purpose": "fine-tune",
    "filename": "training_examples.jsonl",
    "bytes": 2147483648,
    "mime_type": "text/jsonl",
    "expires_after": {
      "anchor": "created_at",
      "seconds": 3600
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
12
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
{
  "id": "upload_abc123",
  "object": "upload",
  "bytes": 2147483648,
  "created_at": 1719184911,
  "filename": "training_examples.jsonl",
  "purpose": "fine-tune",
  "status": "pending",
  "expires_at": 1719127296
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/role-assignments

**Contents:**
- Role assignments
- List group organization role assignments
    - Path parameters
    - Query parameters
    - Returns
- Assign organization role to group
    - Path parameters
    - Request body
    - Returns
- Unassign organization role from group

Assign and remove roles for users and groups at the organization or project level.

Lists the organization roles assigned to a group within the organization.

The ID of the group whose organization role assignments you want to list.

Cursor for pagination. Provide the value from the previous response's next field to continue listing organization roles.

A limit on the number of organization role assignments to return.

Sort order for the returned organization roles.

A list of role objects.

Assigns an organization role to a group within the organization.

The ID of the group that should receive the organization role.

Identifier of the role to assign.

The created group role object.

Unassigns an organization role from a group within the organization.

The ID of the group to modify.

The ID of the organization role to remove from the group.

Confirmation of the deleted group role object.

Lists the organization roles assigned to a user within the organization.

The ID of the user to inspect.

Cursor for pagination. Provide the value from the previous response's next field to continue listing organization roles.

A limit on the number of organization role assignments to return.

Sort order for the returned organization roles.

A list of role objects.

Assigns an organization role to a user within the organization.

The ID of the user that should receive the organization role.

Identifier of the role to assign.

The created user role object.

Unassigns an organization role from a user within the organization.

The ID of the organization role to remove from the user.

The ID of the user to modify.

Confirmation of the deleted user role object.

Lists the project roles assigned to a group within a project.

The ID of the group to inspect.

The ID of the project to inspect.

Cursor for pagination. Provide the value from the previous response's next field to continue listing project roles.

A limit on the number of project role assignments to return.

Sort order for the returned project roles.

A list of role objects.

Assigns a project role to a group within a project.

The ID of the group that should receive the project role.

The ID of the project to update.

Identifier of the role to assign.

The created group role object.

Unassigns a project role from a group within a project.

The ID of the group whose project role assignment should be removed.

The ID of the project to modify.

The ID of the project role to remove from the group.

Confirmation of the deleted group role object.

Lists the project roles assigned to a user within a project.

The ID of the project to inspect.

The ID of the user to inspect.

Cursor for pagination. Provide the value from the previous response's next field to continue listing project roles.

A limit on the number of project role assignments to return.

Sort order for the returned project roles.

A list of role objects.

Assigns a project role to a user within a project.

The ID of the project to update.

The ID of the user that should receive the project role.

Identifier of the role to assign.

The created user role object.

Unassigns a project role from a user within a project.

The ID of the project to modify.

The ID of the project role to remove from the user.

The ID of the user whose project role assignment should be removed.

Confirmation of the deleted user role object.

Role assignment linking a group to a role.

Summary information about a group returned in role assignment responses.

Details about a role that can be assigned through the public Roles API.

Role assignment linking a user to a role.

Details about a role that can be assigned through the public Roles API.

Represents an individual user within an organization.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/groups/group_01J1F8ABCDXYZ/roles \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/groups/group_01J1F8ABCDXYZ/roles \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
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
{
    "object": "list",
    "data": [
        {
            "id": "role_01J1F8ROLE01",
            "name": "API Group Manager",
            "permissions": [
                "api.groups.read",
                "api.groups.write"
            ],
            "resource_type": "api.organization",
            "predefined_role": false,
            "description": "Allows managing organization groups",
            "created_at": 1711471533,
            "updated_at": 1711472599,
            "created_by": "user_abc123",
            "created_by_user_obj": {
                "id": "user_abc123",
                "name": "Ada Lovelace",
                "email": "ada@example.com"
            },
            "metadata": {}
        }
    ],
    "has_more": false,
    "next": null
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
21
22
23
24
25
26
27
{
    "object": "list",
    "data": [
        {
            "id": "role_01J1F8ROLE01",
            "name": "API Group Manager",
            "permissions": [
                "api.groups.read",
                "api.groups.write"
            ],
            "resource_type": "api.organization",
            "predefined_role": false,
            "description": "Allows managing organization groups",
            "created_at": 1711471533,
            "updated_at": 1711472599,
            "created_by": "user_abc123",
            "created_by_user_obj": {
                "id": "user_abc123",
                "name": "Ada Lovelace",
                "email": "ada@example.com"
            },
            "metadata": {}
        }
    ],
    "has_more": false,
    "next": null
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/containers

**Contents:**
- Containers
- Create container
    - Request body
    - Returns
- List containers
    - Query parameters
    - Returns
- Retrieve container
    - Path parameters
    - Returns

Create and manage containers for use with the Code Interpreter tool.

Name of the container to create.

Container expiration time in seconds relative to the 'anchor' time.

IDs of files to copy to the container.

Optional memory limit for the container. Defaults to "1g".

The created container object.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

a list of container objects.

Retrieves a container.

The container object.

The ID of the container to delete.

Unix timestamp (in seconds) when the container was created.

The container will expire after this time period. The anchor is the reference point for the expiration. The minutes is the number of minutes after the anchor before the container expires.

Unique identifier for the container.

Unix timestamp (in seconds) when the container was last active.

The memory limit configured for the container.

Name of the container.

The type of this object.

Status of the container (e.g., active, deleted).

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
curl https://api.openai.com/v1/containers \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "My Container",
        "memory_limit": "4g"
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
curl https://api.openai.com/v1/containers \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "My Container",
        "memory_limit": "4g"
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
{
    "id": "cntr_682e30645a488191b6363a0cbefc0f0a025ec61b66250591",
    "object": "container",
    "created_at": 1747857508,
    "status": "running",
    "expires_after": {
        "anchor": "last_active_at",
        "minutes": 20
    },
    "last_active_at": 1747857508,
    "memory_limit": "4g",
    "name": "My Container"
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/models/list

**Contents:**
- Models
- List models
    - Returns
- Retrieve model
    - Path parameters
    - Returns
- Delete a fine-tuned model
    - Path parameters
    - Returns
- The model object

List and describe the various models available in the API. You can refer to the Models documentation to understand what models are available and the differences between them.

Lists the currently available models, and provides basic information about each one such as the owner and availability.

A list of model objects.

Retrieves a model instance, providing basic information about the model such as the owner and permissioning.

The ID of the model to use for this request

The model object matching the specified ID.

Delete a fine-tuned model. You must have the Owner role in your organization to delete a model.

Describes an OpenAI model offering that can be used with the API.

The Unix timestamp (in seconds) when the model was created.

The model identifier, which can be referenced in the API endpoints.

The object type, which is always "model".

The organization that owns the model.

**Examples:**

Example 1 (unknown):
```unknown
1
2
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

Example 2 (bash):
```bash
1
2
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

Example 3 (python):
```python
1
2
3
4
from openai import OpenAI
client = OpenAI()

client.models.list()
```

Example 4 (python):
```python
1
2
3
4
from openai import OpenAI
client = OpenAI()

client.models.list()
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses/compact

**Contents:**
- Responses
- Create a model response
    - Request body
    - Returns
- Get a model response
    - Path parameters
    - Query parameters
    - Returns
- Delete a model response
    - Path parameters

OpenAI's most advanced interface for generating model responses. Supports text and image inputs, and text outputs. Create stateful interactions with the model, using the output of previous responses as input. Extend the model's capabilities with built-in tools for file search, web search, computer use, and more. Allow the model access to external systems and data using function calling.

Creates a model response. Provide text or image inputs to generate text or JSON outputs. Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Specify additional output data to include in the model response. Currently supported values are:

Text, image, or file inputs to the model, used to generate a response.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

Whether to store the generated model response for later retrieval via API.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

Options for streaming responses. Only set this when you set stream: true.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

Returns a Response object.

Retrieves a model response with the given ID.

The ID of the response to retrieve.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an obfuscation field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set include_obfuscation to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API.

The sequence number of the event after which to start streaming.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

The Response object matching the specified ID.

Deletes a model response with the given ID.

The ID of the response to delete.

Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled. Learn more.

The ID of the response to cancel.

Runs a compaction pass over a conversation. Compaction returns encrypted, opaque items and the underlying logic may evolve over time.

Model ID used to generate the response, like gpt-5 or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

A compacted response object.

Learn when and how to compact long-running conversations in the conversation state guide.

Returns a list of input items for a given response.

The ID of the response to retrieve input items for.

An item ID to list items after, used in pagination.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

A list of input item objects.

Returns input token counts of the request.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

gpt-5 and o-series models only

Configuration options for reasoning models.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

The truncation strategy to use for the model response. - auto: If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation. - disabled (default): If the input size will exceed the context window size for a model, the request will fail with a 400 error.

The input token counts.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

Unix timestamp (in seconds) of when this Response was created.

An error object returned when the model fails to generate a Response.

Unique identifier for this Response.

Details about why the response is incomplete.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

The object type of this resource - always set to response.

An array of content items generated by the model.

SDK-only convenience property that contains the aggregated text output from all output_text items in the output array, if any are present. Supported in the Python and JavaScript SDKs.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

The status of the response generation. One of completed, failed, in_progress, cancelled, queued, or incomplete.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

A list of Response items.

A list of items used to generate this response.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

Unix timestamp (in seconds) when the compacted conversation was created.

The unique identifier for the compacted response.

The object type. Always response.compaction.

The compacted list of output items.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
8
9
10
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "Tell me a three sentence bedtime story about a unicorn."
});

console.log(response);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/administration

**Contents:**
- Administration

Programmatically manage your organization. The Audit Logs endpoint provides a log of all actions taken in the organization for security and monitoring purposes. To access these endpoints please generate an Admin API Key through the API Platform Organization overview. Admin API keys cannot be used for non-administration endpoints. For best practices on setting up your organization, please refer to this guide

---

## 

**URL:** https://platform.openai.com/docs/api-reference/project-service-accounts

**Contents:**
- Project service accounts
- List project service accounts
    - Path parameters
    - Query parameters
    - Returns
- Create project service account
    - Path parameters
    - Request body
    - Returns
- Retrieve project service account

Manage service accounts within a project. A service account is a bot user that is not associated with a user. If a user leaves an organization, their keys and membership in projects will no longer work. Service accounts do not have this limitation. However, service accounts can also be deleted from a project.

Returns a list of service accounts in the project.

The ID of the project.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

A list of ProjectServiceAccount objects.

Creates a new service account in the project. This also returns an unredacted API key for the service account.

The ID of the project.

The name of the service account being created.

The created ProjectServiceAccount object.

Retrieves a service account in the project.

The ID of the project.

The ID of the service account.

The ProjectServiceAccount object matching the specified ID.

Deletes a service account from the project.

The ID of the project.

The ID of the service account.

Confirmation of service account being deleted, or an error in case of an archived project, which has no service accounts

Represents an individual service account in a project.

The Unix timestamp (in seconds) of when the service account was created

The identifier, which can be referenced in API endpoints

The name of the service account

The object type, which is always organization.project.service_account

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/projects/proj_abc/service_accounts?after=custom_id&limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/projects/proj_abc/service_accounts?after=custom_id&limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
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
{
    "object": "list",
    "data": [
        {
            "object": "organization.project.service_account",
            "id": "svc_acct_abc",
            "name": "Service Account",
            "role": "owner",
            "created_at": 1711471533
        }
    ],
    "first_id": "svc_acct_abc",
    "last_id": "svc_acct_xyz",
    "has_more": false
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
{
    "object": "list",
    "data": [
        {
            "object": "organization.project.service_account",
            "id": "svc_acct_abc",
            "name": "Service Account",
            "role": "owner",
            "created_at": 1711471533
        }
    ],
    "first_id": "svc_acct_abc",
    "last_id": "svc_acct_xyz",
    "has_more": false
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/projects

**Contents:**
- Projects
- List projects
    - Query parameters
    - Returns
- Create project
    - Request body
    - Returns
- Retrieve project
    - Path parameters
    - Returns

Manage the projects within an orgnanization includes creation, updating, and archiving or projects. The Default project cannot be archived.

Returns a list of projects.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

If true returns all projects including those that have been archived. Archived projects are not included by default.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

A list of Project objects.

Create a new project in the organization. Projects can be created and archived, but cannot be deleted.

The friendly name of the project, this name appears in reports.

Create the project with the specified data residency region. Your organization must have access to Data residency functionality in order to use. See data residency controls to review the functionality and limitations of setting this field.

The created Project object.

The ID of the project.

The Project object matching the specified ID.

Modifies a project in the organization.

The ID of the project.

The updated name of the project, this name appears in reports.

The updated Project object.

Archives a project in the organization. Archived projects cannot be used or updated.

The ID of the project.

The archived Project object.

Represents an individual project.

The Unix timestamp (in seconds) of when the project was archived or null.

The Unix timestamp (in seconds) of when the project was created.

The identifier, which can be referenced in API endpoints

The name of the project. This appears in reporting.

The object type, which is always organization.project

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/projects?after=proj_abc&limit=20&include_archived=false \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/projects?after=proj_abc&limit=20&include_archived=false \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
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
{
    "object": "list",
    "data": [
        {
            "id": "proj_abc",
            "object": "organization.project",
            "name": "Project example",
            "created_at": 1711471533,
            "archived_at": null,
            "status": "active"
        }
    ],
    "first_id": "proj-abc",
    "last_id": "proj-xyz",
    "has_more": false
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
{
    "object": "list",
    "data": [
        {
            "id": "proj_abc",
            "object": "organization.project",
            "name": "Project example",
            "created_at": 1711471533,
            "archived_at": null,
            "status": "active"
        }
    ],
    "first_id": "proj-abc",
    "last_id": "proj-xyz",
    "has_more": false
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses/input-tokens

**Contents:**
- Responses
- Create a model response
    - Request body
    - Returns
- Get a model response
    - Path parameters
    - Query parameters
    - Returns
- Delete a model response
    - Path parameters

OpenAI's most advanced interface for generating model responses. Supports text and image inputs, and text outputs. Create stateful interactions with the model, using the output of previous responses as input. Extend the model's capabilities with built-in tools for file search, web search, computer use, and more. Allow the model access to external systems and data using function calling.

Creates a model response. Provide text or image inputs to generate text or JSON outputs. Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Specify additional output data to include in the model response. Currently supported values are:

Text, image, or file inputs to the model, used to generate a response.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

Whether to store the generated model response for later retrieval via API.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

Options for streaming responses. Only set this when you set stream: true.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

Returns a Response object.

Retrieves a model response with the given ID.

The ID of the response to retrieve.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an obfuscation field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set include_obfuscation to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API.

The sequence number of the event after which to start streaming.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

The Response object matching the specified ID.

Deletes a model response with the given ID.

The ID of the response to delete.

Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled. Learn more.

The ID of the response to cancel.

Runs a compaction pass over a conversation. Compaction returns encrypted, opaque items and the underlying logic may evolve over time.

Model ID used to generate the response, like gpt-5 or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

A compacted response object.

Learn when and how to compact long-running conversations in the conversation state guide.

Returns a list of input items for a given response.

The ID of the response to retrieve input items for.

An item ID to list items after, used in pagination.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

A list of input item objects.

Returns input token counts of the request.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

gpt-5 and o-series models only

Configuration options for reasoning models.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

The truncation strategy to use for the model response. - auto: If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation. - disabled (default): If the input size will exceed the context window size for a model, the request will fail with a 400 error.

The input token counts.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

Unix timestamp (in seconds) of when this Response was created.

An error object returned when the model fails to generate a Response.

Unique identifier for this Response.

Details about why the response is incomplete.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

The object type of this resource - always set to response.

An array of content items generated by the model.

SDK-only convenience property that contains the aggregated text output from all output_text items in the output array, if any are present. Supported in the Python and JavaScript SDKs.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

The status of the response generation. One of completed, failed, in_progress, cancelled, queued, or incomplete.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

A list of Response items.

A list of items used to generate this response.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

Unix timestamp (in seconds) when the compacted conversation was created.

The unique identifier for the compacted response.

The object type. Always response.compaction.

The compacted list of output items.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
8
9
10
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "Tell me a three sentence bedtime story about a unicorn."
});

console.log(response);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses/create

**Contents:**
- Responses
- Create a model response
    - Request body
    - Returns
- Get a model response
    - Path parameters
    - Query parameters
    - Returns
- Delete a model response
    - Path parameters

OpenAI's most advanced interface for generating model responses. Supports text and image inputs, and text outputs. Create stateful interactions with the model, using the output of previous responses as input. Extend the model's capabilities with built-in tools for file search, web search, computer use, and more. Allow the model access to external systems and data using function calling.

Creates a model response. Provide text or image inputs to generate text or JSON outputs. Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Specify additional output data to include in the model response. Currently supported values are:

Text, image, or file inputs to the model, used to generate a response.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

Whether to store the generated model response for later retrieval via API.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

Options for streaming responses. Only set this when you set stream: true.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

Returns a Response object.

Retrieves a model response with the given ID.

The ID of the response to retrieve.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an obfuscation field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set include_obfuscation to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API.

The sequence number of the event after which to start streaming.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

The Response object matching the specified ID.

Deletes a model response with the given ID.

The ID of the response to delete.

Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled. Learn more.

The ID of the response to cancel.

Runs a compaction pass over a conversation. Compaction returns encrypted, opaque items and the underlying logic may evolve over time.

Model ID used to generate the response, like gpt-5 or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

A compacted response object.

Learn when and how to compact long-running conversations in the conversation state guide.

Returns a list of input items for a given response.

The ID of the response to retrieve input items for.

An item ID to list items after, used in pagination.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

A list of input item objects.

Returns input token counts of the request.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

gpt-5 and o-series models only

Configuration options for reasoning models.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

The truncation strategy to use for the model response. - auto: If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation. - disabled (default): If the input size will exceed the context window size for a model, the request will fail with a 400 error.

The input token counts.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

Unix timestamp (in seconds) of when this Response was created.

An error object returned when the model fails to generate a Response.

Unique identifier for this Response.

Details about why the response is incomplete.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

The object type of this resource - always set to response.

An array of content items generated by the model.

SDK-only convenience property that contains the aggregated text output from all output_text items in the output array, if any are present. Supported in the Python and JavaScript SDKs.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

The status of the response generation. One of completed, failed, in_progress, cancelled, queued, or incomplete.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

A list of Response items.

A list of items used to generate this response.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

Unix timestamp (in seconds) when the compacted conversation was created.

The unique identifier for the compacted response.

The object type. Always response.compaction.

The compacted list of output items.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
8
9
10
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "Tell me a three sentence bedtime story about a unicorn."
});

console.log(response);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses/cancel

**Contents:**
- Responses
- Create a model response
    - Request body
    - Returns
- Get a model response
    - Path parameters
    - Query parameters
    - Returns
- Delete a model response
    - Path parameters

OpenAI's most advanced interface for generating model responses. Supports text and image inputs, and text outputs. Create stateful interactions with the model, using the output of previous responses as input. Extend the model's capabilities with built-in tools for file search, web search, computer use, and more. Allow the model access to external systems and data using function calling.

Creates a model response. Provide text or image inputs to generate text or JSON outputs. Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Specify additional output data to include in the model response. Currently supported values are:

Text, image, or file inputs to the model, used to generate a response.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

Whether to store the generated model response for later retrieval via API.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

Options for streaming responses. Only set this when you set stream: true.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

Returns a Response object.

Retrieves a model response with the given ID.

The ID of the response to retrieve.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an obfuscation field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set include_obfuscation to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API.

The sequence number of the event after which to start streaming.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

The Response object matching the specified ID.

Deletes a model response with the given ID.

The ID of the response to delete.

Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled. Learn more.

The ID of the response to cancel.

Runs a compaction pass over a conversation. Compaction returns encrypted, opaque items and the underlying logic may evolve over time.

Model ID used to generate the response, like gpt-5 or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

A compacted response object.

Learn when and how to compact long-running conversations in the conversation state guide.

Returns a list of input items for a given response.

The ID of the response to retrieve input items for.

An item ID to list items after, used in pagination.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

A list of input item objects.

Returns input token counts of the request.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

gpt-5 and o-series models only

Configuration options for reasoning models.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

The truncation strategy to use for the model response. - auto: If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation. - disabled (default): If the input size will exceed the context window size for a model, the request will fail with a 400 error.

The input token counts.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

Unix timestamp (in seconds) of when this Response was created.

An error object returned when the model fails to generate a Response.

Unique identifier for this Response.

Details about why the response is incomplete.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

The object type of this resource - always set to response.

An array of content items generated by the model.

SDK-only convenience property that contains the aggregated text output from all output_text items in the output array, if any are present. Supported in the Python and JavaScript SDKs.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

The status of the response generation. One of completed, failed, in_progress, cancelled, queued, or incomplete.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

A list of Response items.

A list of items used to generate this response.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

Unix timestamp (in seconds) when the compacted conversation was created.

The unique identifier for the compacted response.

The object type. Always response.compaction.

The compacted list of output items.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
8
9
10
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "Tell me a three sentence bedtime story about a unicorn."
});

console.log(response);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/conversations/update

**Contents:**
- Conversations
- Create a conversation
    - Request body
    - Returns
- Retrieve a conversation
    - Path parameters
    - Returns
- Update a conversation
    - Path parameters
    - Request body

Create and manage conversations to store and retrieve conversation state across Response API calls.

Create a conversation.

Initial items to include in the conversation context. You may add up to 20 items at a time.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns a Conversation object.

The ID of the conversation to retrieve.

Returns a Conversation object.

Update a conversation

The ID of the conversation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns the updated Conversation object.

Delete a conversation. Items in the conversation will not be deleted.

The ID of the conversation to delete.

List all items for a conversation with the given ID.

The ID of the conversation to list items for.

An item ID to list items after, used in pagination.

Specify additional output data to include in the model response. Currently supported values are:

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

Returns a list object containing Conversation items.

Create items in a conversation with the given ID.

The ID of the conversation to add the item to.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

The items to add to the conversation. You may add up to 20 items at a time.

Returns the list of added items.

Get a single item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to retrieve.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

Returns a Conversation Item.

Delete an item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to delete.

Returns the updated Conversation object.

The time at which the conversation was created, measured in seconds since the Unix epoch.

The unique ID of the conversation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The object type, which is always conversation.

A list of Conversation items.

A list of conversation items.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
import OpenAI from "openai";
const client = new OpenAI();

const conversation = await client.conversations.create({
  metadata: { topic: "demo" },
  items: [
    { type: "message", role: "user", content: "Hello!" }
  ],
});
console.log(conversation);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/conversations/delete

**Contents:**
- Conversations
- Create a conversation
    - Request body
    - Returns
- Retrieve a conversation
    - Path parameters
    - Returns
- Update a conversation
    - Path parameters
    - Request body

Create and manage conversations to store and retrieve conversation state across Response API calls.

Create a conversation.

Initial items to include in the conversation context. You may add up to 20 items at a time.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns a Conversation object.

The ID of the conversation to retrieve.

Returns a Conversation object.

Update a conversation

The ID of the conversation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns the updated Conversation object.

Delete a conversation. Items in the conversation will not be deleted.

The ID of the conversation to delete.

List all items for a conversation with the given ID.

The ID of the conversation to list items for.

An item ID to list items after, used in pagination.

Specify additional output data to include in the model response. Currently supported values are:

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

Returns a list object containing Conversation items.

Create items in a conversation with the given ID.

The ID of the conversation to add the item to.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

The items to add to the conversation. You may add up to 20 items at a time.

Returns the list of added items.

Get a single item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to retrieve.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

Returns a Conversation Item.

Delete an item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to delete.

Returns the updated Conversation object.

The time at which the conversation was created, measured in seconds since the Unix epoch.

The unique ID of the conversation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The object type, which is always conversation.

A list of Conversation items.

A list of conversation items.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
import OpenAI from "openai";
const client = new OpenAI();

const conversation = await client.conversations.create({
  metadata: { topic: "demo" },
  items: [
    { type: "message", role: "user", content: "Hello!" }
  ],
});
console.log(conversation);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/conversations

**Contents:**
- Conversations
- Create a conversation
    - Request body
    - Returns
- Retrieve a conversation
    - Path parameters
    - Returns
- Update a conversation
    - Path parameters
    - Request body

Create and manage conversations to store and retrieve conversation state across Response API calls.

Create a conversation.

Initial items to include in the conversation context. You may add up to 20 items at a time.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns a Conversation object.

The ID of the conversation to retrieve.

Returns a Conversation object.

Update a conversation

The ID of the conversation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns the updated Conversation object.

Delete a conversation. Items in the conversation will not be deleted.

The ID of the conversation to delete.

List all items for a conversation with the given ID.

The ID of the conversation to list items for.

An item ID to list items after, used in pagination.

Specify additional output data to include in the model response. Currently supported values are:

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

Returns a list object containing Conversation items.

Create items in a conversation with the given ID.

The ID of the conversation to add the item to.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

The items to add to the conversation. You may add up to 20 items at a time.

Returns the list of added items.

Get a single item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to retrieve.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

Returns a Conversation Item.

Delete an item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to delete.

Returns the updated Conversation object.

The time at which the conversation was created, measured in seconds since the Unix epoch.

The unique ID of the conversation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The object type, which is always conversation.

A list of Conversation items.

A list of conversation items.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
import OpenAI from "openai";
const client = new OpenAI();

const conversation = await client.conversations.create({
  metadata: { topic: "demo" },
  items: [
    { type: "message", role: "user", content: "Hello!" }
  ],
});
console.log(conversation);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses/get

**Contents:**
- Responses
- Create a model response
    - Request body
    - Returns
- Get a model response
    - Path parameters
    - Query parameters
    - Returns
- Delete a model response
    - Path parameters

OpenAI's most advanced interface for generating model responses. Supports text and image inputs, and text outputs. Create stateful interactions with the model, using the output of previous responses as input. Extend the model's capabilities with built-in tools for file search, web search, computer use, and more. Allow the model access to external systems and data using function calling.

Creates a model response. Provide text or image inputs to generate text or JSON outputs. Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Specify additional output data to include in the model response. Currently supported values are:

Text, image, or file inputs to the model, used to generate a response.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

Whether to store the generated model response for later retrieval via API.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

Options for streaming responses. Only set this when you set stream: true.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

Returns a Response object.

Retrieves a model response with the given ID.

The ID of the response to retrieve.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an obfuscation field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set include_obfuscation to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API.

The sequence number of the event after which to start streaming.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

The Response object matching the specified ID.

Deletes a model response with the given ID.

The ID of the response to delete.

Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled. Learn more.

The ID of the response to cancel.

Runs a compaction pass over a conversation. Compaction returns encrypted, opaque items and the underlying logic may evolve over time.

Model ID used to generate the response, like gpt-5 or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

A compacted response object.

Learn when and how to compact long-running conversations in the conversation state guide.

Returns a list of input items for a given response.

The ID of the response to retrieve input items for.

An item ID to list items after, used in pagination.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

A list of input item objects.

Returns input token counts of the request.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

gpt-5 and o-series models only

Configuration options for reasoning models.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

The truncation strategy to use for the model response. - auto: If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation. - disabled (default): If the input size will exceed the context window size for a model, the request will fail with a 400 error.

The input token counts.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

Unix timestamp (in seconds) of when this Response was created.

An error object returned when the model fails to generate a Response.

Unique identifier for this Response.

Details about why the response is incomplete.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

The object type of this resource - always set to response.

An array of content items generated by the model.

SDK-only convenience property that contains the aggregated text output from all output_text items in the output array, if any are present. Supported in the Python and JavaScript SDKs.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

The status of the response generation. One of completed, failed, in_progress, cancelled, queued, or incomplete.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

A list of Response items.

A list of items used to generate this response.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

Unix timestamp (in seconds) when the compacted conversation was created.

The unique identifier for the compacted response.

The object type. Always response.compaction.

The compacted list of output items.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
8
9
10
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "Tell me a three sentence bedtime story about a unicorn."
});

console.log(response);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference

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

## 

**URL:** https://platform.openai.com/docs/api-reference/evals/createRun

**Contents:**
- Evals
- Create eval
    - Request body
    - Returns
- Get an eval
    - Path parameters
    - Returns
- Update an eval
    - Path parameters
    - Request body

Create, manage, and run evals in the OpenAI platform. Related guide: Evals

Create the structure of an evaluation that can be used to test a model's performance. An evaluation is a set of testing criteria and the config for a data source, which dictates the schema of the data used in the evaluation. After creating an evaluation, you can run it on different models and model parameters. We support several types of graders and datasources. For more information, see the Evals guide.

The configuration for the data source used for the evaluation runs. Dictates the schema of the data used in the evaluation.

A list of graders for all eval runs in this group. Graders can reference variables in the data source using double curly braces notation, like {{item.variable_name}}. To reference the model's output, use the sample namespace (ie, {{sample.output_text}}).

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The name of the evaluation.

The created Eval object.

Get an evaluation by ID.

The ID of the evaluation to retrieve.

The Eval object matching the specified ID.

Update certain properties of an evaluation.

The ID of the evaluation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Rename the evaluation.

The Eval object matching the updated version.

Delete an evaluation.

The ID of the evaluation to delete.

A deletion confirmation object.

List evaluations for a project.

Identifier for the last eval from the previous pagination request.

Number of evals to retrieve.

Sort order for evals by timestamp. Use asc for ascending order or desc for descending order.

Evals can be ordered by creation time or last updated time. Use created_at for creation time or updated_at for last updated time.

A list of evals matching the specified filters.

Get a list of runs for an evaluation.

The ID of the evaluation to retrieve runs for.

Identifier for the last run from the previous pagination request.

Number of runs to retrieve.

Sort order for runs by timestamp. Use asc for ascending order or desc for descending order. Defaults to asc.

Filter runs by status. One of queued | in_progress | failed | completed | canceled.

A list of EvalRun objects matching the specified ID.

Get an evaluation run by ID.

The ID of the evaluation to retrieve runs for.

The ID of the run to retrieve.

The EvalRun object matching the specified ID.

Kicks off a new run for a given evaluation, specifying the data source, and what model configuration to use to test. The datasource will be validated against the schema specified in the config of the evaluation.

The ID of the evaluation to create a run for.

Details about the run's data source.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The EvalRun object matching the specified ID.

Cancel an ongoing evaluation run.

The ID of the evaluation whose run you want to cancel.

The ID of the run to cancel.

The updated EvalRun object reflecting that the run is canceled.

The ID of the evaluation to delete the run from.

The ID of the run to delete.

An object containing the status of the delete operation.

Get an evaluation run output item by ID.

The ID of the evaluation to retrieve runs for.

The ID of the output item to retrieve.

The ID of the run to retrieve.

The EvalRunOutputItem object matching the specified ID.

Get a list of output items for an evaluation run.

The ID of the evaluation to retrieve runs for.

The ID of the run to retrieve output items for.

Identifier for the last output item from the previous pagination request.

Number of output items to retrieve.

Sort order for output items by timestamp. Use asc for ascending order or desc for descending order. Defaults to asc.

Filter output items by status. Use failed to filter by failed output items or pass to filter by passed output items.

A list of EvalRunOutputItem objects matching the specified ID.

An Eval object with a data source config and testing criteria. An Eval represents a task to be done for your LLM integration. Like:

The Unix timestamp (in seconds) for when the eval was created.

Configuration of data sources used in runs of the evaluation.

Unique identifier for the evaluation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The name of the evaluation.

A list of testing criteria.

A schema representing an evaluation run.

Unix timestamp (in seconds) when the evaluation run was created.

Information about the run's data source.

An object representing an error response from the Eval API.

The identifier of the associated evaluation.

Unique identifier for the evaluation run.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The model that is evaluated, if applicable.

The name of the evaluation run.

The type of the object. Always "eval.run".

Usage statistics for each model during the evaluation run.

Results per testing criteria applied during the evaluation run.

The URL to the rendered evaluation run report on the UI dashboard.

Counters summarizing the outcomes of the evaluation run.

The status of the evaluation run.

A schema representing an evaluation run output item.

Unix timestamp (in seconds) when the evaluation run was created.

Details of the input data source item.

The identifier for the data source item.

The identifier of the evaluation group.

Unique identifier for the evaluation run output item.

The type of the object. Always "eval.run.output_item".

A list of grader results for this output item.

The identifier of the evaluation run associated with this output item.

A sample containing the input and output of the evaluation run.

The status of the evaluation run.

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
curl https://api.openai.com/v1/evals \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Sentiment",
        "data_source_config": {
          "type": "stored_completions",
          "metadata": {
              "usecase": "chatbot"
          }
        },
        "testing_criteria": [
          {
            "type": "label_model",
            "model": "o3-mini",
            "input": [
              {
                "role": "developer",
                "content": "Classify the sentiment of the following statement as one of 'positive', 'neutral', or 'negative'"
              },
              {
                "role": "user",
                "content": "Statement: {{item.input}}"
              }
            ],
            "passing_labels": [
              "positive"
            ],
            "labels": [
              "positive",
              "neutral",
              "negative"
            ],
            "name": "Example label grader"
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
curl https://api.openai.com/v1/evals \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Sentiment",
        "data_source_config": {
          "type": "stored_completions",
          "metadata": {
              "usecase": "chatbot"
          }
        },
        "testing_criteria": [
          {
            "type": "label_model",
            "model": "o3-mini",
            "input": [
              {
                "role": "developer",
                "content": "Classify the sentiment of the following statement as one of 'positive', 'neutral', or 'negative'"
              },
              {
                "role": "user",
                "content": "Statement: {{item.input}}"
              }
            ],
            "passing_labels": [
              "positive"
            ],
            "labels": [
              "positive",
              "neutral",
              "negative"
            ],
            "name": "Example label grader"
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
from openai import OpenAI
client = OpenAI()

eval_obj = client.evals.create(
  name="Sentiment",
  data_source_config={
    "type": "stored_completions",
    "metadata": {"usecase": "chatbot"}
  },
  testing_criteria=[
    {
      "type": "label_model",
      "model": "o3-mini",
      "input": [
        {"role": "developer", "content": "Classify the sentiment of the following statement as one of 'positive', 'neutral', or 'negative'"},
        {"role": "user", "content": "Statement: {{item.input}}"}
      ],
      "passing_labels": ["positive"],
      "labels": ["positive", "neutral", "negative"],
      "name": "Example label grader"
    }
  ]
)
print(eval_obj)
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/backward-compatibility

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

## 

**URL:** https://platform.openai.com/docs/api-reference/conversations/create

**Contents:**
- Conversations
- Create a conversation
    - Request body
    - Returns
- Retrieve a conversation
    - Path parameters
    - Returns
- Update a conversation
    - Path parameters
    - Request body

Create and manage conversations to store and retrieve conversation state across Response API calls.

Create a conversation.

Initial items to include in the conversation context. You may add up to 20 items at a time.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns a Conversation object.

The ID of the conversation to retrieve.

Returns a Conversation object.

Update a conversation

The ID of the conversation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns the updated Conversation object.

Delete a conversation. Items in the conversation will not be deleted.

The ID of the conversation to delete.

List all items for a conversation with the given ID.

The ID of the conversation to list items for.

An item ID to list items after, used in pagination.

Specify additional output data to include in the model response. Currently supported values are:

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

Returns a list object containing Conversation items.

Create items in a conversation with the given ID.

The ID of the conversation to add the item to.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

The items to add to the conversation. You may add up to 20 items at a time.

Returns the list of added items.

Get a single item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to retrieve.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

Returns a Conversation Item.

Delete an item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to delete.

Returns the updated Conversation object.

The time at which the conversation was created, measured in seconds since the Unix epoch.

The unique ID of the conversation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The object type, which is always conversation.

A list of Conversation items.

A list of conversation items.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
import OpenAI from "openai";
const client = new OpenAI();

const conversation = await client.conversations.create({
  metadata: { topic: "demo" },
  items: [
    { type: "message", role: "user", content: "Hello!" }
  ],
});
console.log(conversation);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/conversations/get-item

**Contents:**
- Conversations
- Create a conversation
    - Request body
    - Returns
- Retrieve a conversation
    - Path parameters
    - Returns
- Update a conversation
    - Path parameters
    - Request body

Create and manage conversations to store and retrieve conversation state across Response API calls.

Create a conversation.

Initial items to include in the conversation context. You may add up to 20 items at a time.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns a Conversation object.

The ID of the conversation to retrieve.

Returns a Conversation object.

Update a conversation

The ID of the conversation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns the updated Conversation object.

Delete a conversation. Items in the conversation will not be deleted.

The ID of the conversation to delete.

List all items for a conversation with the given ID.

The ID of the conversation to list items for.

An item ID to list items after, used in pagination.

Specify additional output data to include in the model response. Currently supported values are:

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

Returns a list object containing Conversation items.

Create items in a conversation with the given ID.

The ID of the conversation to add the item to.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

The items to add to the conversation. You may add up to 20 items at a time.

Returns the list of added items.

Get a single item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to retrieve.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

Returns a Conversation Item.

Delete an item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to delete.

Returns the updated Conversation object.

The time at which the conversation was created, measured in seconds since the Unix epoch.

The unique ID of the conversation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The object type, which is always conversation.

A list of Conversation items.

A list of conversation items.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
import OpenAI from "openai";
const client = new OpenAI();

const conversation = await client.conversations.create({
  metadata: { topic: "demo" },
  items: [
    { type: "message", role: "user", content: "Hello!" }
  ],
});
console.log(conversation);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses/list

**Contents:**
- Responses
- Create a model response
    - Request body
    - Returns
- Get a model response
    - Path parameters
    - Query parameters
    - Returns
- Delete a model response
    - Path parameters

OpenAI's most advanced interface for generating model responses. Supports text and image inputs, and text outputs. Create stateful interactions with the model, using the output of previous responses as input. Extend the model's capabilities with built-in tools for file search, web search, computer use, and more. Allow the model access to external systems and data using function calling.

Creates a model response. Provide text or image inputs to generate text or JSON outputs. Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Specify additional output data to include in the model response. Currently supported values are:

Text, image, or file inputs to the model, used to generate a response.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

Whether to store the generated model response for later retrieval via API.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

Options for streaming responses. Only set this when you set stream: true.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

Returns a Response object.

Retrieves a model response with the given ID.

The ID of the response to retrieve.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an obfuscation field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set include_obfuscation to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API.

The sequence number of the event after which to start streaming.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

The Response object matching the specified ID.

Deletes a model response with the given ID.

The ID of the response to delete.

Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled. Learn more.

The ID of the response to cancel.

Runs a compaction pass over a conversation. Compaction returns encrypted, opaque items and the underlying logic may evolve over time.

Model ID used to generate the response, like gpt-5 or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

A compacted response object.

Learn when and how to compact long-running conversations in the conversation state guide.

Returns a list of input items for a given response.

The ID of the response to retrieve input items for.

An item ID to list items after, used in pagination.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

A list of input item objects.

Returns input token counts of the request.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

gpt-5 and o-series models only

Configuration options for reasoning models.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

The truncation strategy to use for the model response. - auto: If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation. - disabled (default): If the input size will exceed the context window size for a model, the request will fail with a 400 error.

The input token counts.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

Unix timestamp (in seconds) of when this Response was created.

An error object returned when the model fails to generate a Response.

Unique identifier for this Response.

Details about why the response is incomplete.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

The object type of this resource - always set to response.

An array of content items generated by the model.

SDK-only convenience property that contains the aggregated text output from all output_text items in the output array, if any are present. Supported in the Python and JavaScript SDKs.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

The status of the response generation. One of completed, failed, in_progress, cancelled, queued, or incomplete.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

A list of Response items.

A list of items used to generate this response.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

Unix timestamp (in seconds) when the compacted conversation was created.

The unique identifier for the compacted response.

The object type. Always response.compaction.

The compacted list of output items.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
8
9
10
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "Tell me a three sentence bedtime story about a unicorn."
});

console.log(response);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/conversations/object

**Contents:**
- Conversations
- Create a conversation
    - Request body
    - Returns
- Retrieve a conversation
    - Path parameters
    - Returns
- Update a conversation
    - Path parameters
    - Request body

Create and manage conversations to store and retrieve conversation state across Response API calls.

Create a conversation.

Initial items to include in the conversation context. You may add up to 20 items at a time.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns a Conversation object.

The ID of the conversation to retrieve.

Returns a Conversation object.

Update a conversation

The ID of the conversation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns the updated Conversation object.

Delete a conversation. Items in the conversation will not be deleted.

The ID of the conversation to delete.

List all items for a conversation with the given ID.

The ID of the conversation to list items for.

An item ID to list items after, used in pagination.

Specify additional output data to include in the model response. Currently supported values are:

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

Returns a list object containing Conversation items.

Create items in a conversation with the given ID.

The ID of the conversation to add the item to.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

The items to add to the conversation. You may add up to 20 items at a time.

Returns the list of added items.

Get a single item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to retrieve.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

Returns a Conversation Item.

Delete an item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to delete.

Returns the updated Conversation object.

The time at which the conversation was created, measured in seconds since the Unix epoch.

The unique ID of the conversation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The object type, which is always conversation.

A list of Conversation items.

A list of conversation items.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
import OpenAI from "openai";
const client = new OpenAI();

const conversation = await client.conversations.create({
  metadata: { topic: "demo" },
  items: [
    { type: "message", role: "user", content: "Hello!" }
  ],
});
console.log(conversation);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/models

**Contents:**
- Models
- List models
    - Returns
- Retrieve model
    - Path parameters
    - Returns
- Delete a fine-tuned model
    - Path parameters
    - Returns
- The model object

List and describe the various models available in the API. You can refer to the Models documentation to understand what models are available and the differences between them.

Lists the currently available models, and provides basic information about each one such as the owner and availability.

A list of model objects.

Retrieves a model instance, providing basic information about the model such as the owner and permissioning.

The ID of the model to use for this request

The model object matching the specified ID.

Delete a fine-tuned model. You must have the Owner role in your organization to delete a model.

Describes an OpenAI model offering that can be used with the API.

The Unix timestamp (in seconds) when the model was created.

The model identifier, which can be referenced in the API endpoints.

The object type, which is always "model".

The organization that owns the model.

**Examples:**

Example 1 (unknown):
```unknown
1
2
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

Example 2 (bash):
```bash
1
2
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

Example 3 (python):
```python
1
2
3
4
from openai import OpenAI
client = OpenAI()

client.models.list()
```

Example 4 (python):
```python
1
2
3
4
from openai import OpenAI
client = OpenAI()

client.models.list()
```

---

## 

**URL:** https://platform.openai.com/docs/apit-reference/responses

**Contents:**
  - Page not found

---

## 

**URL:** https://platform.openai.com/docs/api-reference/container-files

**Contents:**
- Container Files
- Create container file
    - Path parameters
    - Request body
    - Returns
- List container files
    - Path parameters
    - Query parameters
    - Returns
- Retrieve container file

Create and manage container files for use with the Code Interpreter tool.

Creates a container file.

The File object (not file name) to be uploaded.

Name of the file to create.

The created container file object.

Lists container files.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

a list of container file objects.

Retrieves a container file.

The container file object.

Retrieves a container file content.

The contents of the container file.

Delete a container file.

Size of the file in bytes.

The container this file belongs to.

Unix timestamp (in seconds) when the file was created.

Unique identifier for the file.

The type of this object (container.file).

Path of the file in the container.

Source of the file (e.g., user, assistant).

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/containers/cntr_682e0e7318108198aa783fd921ff305e08e78805b9fdbb04/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@example.txt"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/containers/cntr_682e0e7318108198aa783fd921ff305e08e78805b9fdbb04/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@example.txt"
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
{
  "id": "cfile_682e0e8a43c88191a7978f477a09bdf5",
  "object": "container.file",
  "created_at": 1747848842,
  "bytes": 880,
  "container_id": "cntr_682e0e7318108198aa783fd921ff305e08e78805b9fdbb04",
  "path": "/mnt/data/88e12fa445d32636f190a0b33daed6cb-tsconfig.json",
  "source": "user"
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
{
  "id": "cfile_682e0e8a43c88191a7978f477a09bdf5",
  "object": "container.file",
  "created_at": 1747848842,
  "bytes": 880,
  "container_id": "cntr_682e0e7318108198aa783fd921ff305e08e78805b9fdbb04",
  "path": "/mnt/data/88e12fa445d32636f190a0b33daed6cb-tsconfig.json",
  "source": "user"
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/webhook-events

**Contents:**
- Webhook Events
- response.completed
- response.cancelled
- response.failed
- response.incomplete
- batch.completed
- batch.cancelled
- batch.expired
- batch.failed
- fine_tuning.job.succeeded

Webhooks are HTTP requests sent by OpenAI to a URL you specify when certain events happen during the course of API usage.

Learn more about webhooks.

Sent when a background response has been completed.

The Unix timestamp (in seconds) of when the model response was completed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always response.completed.

Sent when a background response has been cancelled.

The Unix timestamp (in seconds) of when the model response was cancelled.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always response.cancelled.

Sent when a background response has failed.

The Unix timestamp (in seconds) of when the model response failed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always response.failed.

Sent when a background response has been interrupted.

The Unix timestamp (in seconds) of when the model response was interrupted.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always response.incomplete.

Sent when a batch API request has been completed.

The Unix timestamp (in seconds) of when the batch API request was completed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always batch.completed.

Sent when a batch API request has been cancelled.

The Unix timestamp (in seconds) of when the batch API request was cancelled.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always batch.cancelled.

Sent when a batch API request has expired.

The Unix timestamp (in seconds) of when the batch API request expired.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always batch.expired.

Sent when a batch API request has failed.

The Unix timestamp (in seconds) of when the batch API request failed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always batch.failed.

Sent when a fine-tuning job has succeeded.

The Unix timestamp (in seconds) of when the fine-tuning job succeeded.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always fine_tuning.job.succeeded.

Sent when a fine-tuning job has failed.

The Unix timestamp (in seconds) of when the fine-tuning job failed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always fine_tuning.job.failed.

Sent when a fine-tuning job has been cancelled.

The Unix timestamp (in seconds) of when the fine-tuning job was cancelled.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always fine_tuning.job.cancelled.

Sent when an eval run has succeeded.

The Unix timestamp (in seconds) of when the eval run succeeded.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always eval.run.succeeded.

Sent when an eval run has failed.

The Unix timestamp (in seconds) of when the eval run failed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always eval.run.failed.

Sent when an eval run has been canceled.

The Unix timestamp (in seconds) of when the eval run was canceled.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always eval.run.canceled.

Sent when Realtime API Receives a incoming SIP call.

The Unix timestamp (in seconds) of when the model response was completed.

The unique ID of the event.

The object of the event. Always event.

The type of the event. Always realtime.call.incoming.

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
{
  "id": "evt_abc123",
  "type": "response.completed",
  "created_at": 1719168000,
  "data": {
    "id": "resp_abc123"
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
{
  "id": "evt_abc123",
  "type": "response.completed",
  "created_at": 1719168000,
  "data": {
    "id": "resp_abc123"
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
{
  "id": "evt_abc123",
  "type": "response.cancelled",
  "created_at": 1719168000,
  "data": {
    "id": "resp_abc123"
  }
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses-streaming/response

**Contents:**
- Streaming events
- response.created
- response.in_progress
- response.completed
- response.failed
- response.incomplete
- response.output_item.added
- response.output_item.done
- response.content_part.added
- response.content_part.done

When you create a Response with stream set to true, the server will emit server-sent events to the client as the Response is generated. This section contains the events that are emitted by the server.

Learn more about streaming responses.

An event that is emitted when a response is created.

The response that was created.

The sequence number for this event.

The type of the event. Always response.created.

Emitted when the response is in progress.

The response that is in progress.

The sequence number of this event.

The type of the event. Always response.in_progress.

Emitted when the model response is complete.

Properties of the completed response.

The sequence number for this event.

The type of the event. Always response.completed.

An event that is emitted when a response fails.

The response that failed.

The sequence number of this event.

The type of the event. Always response.failed.

An event that is emitted when a response finishes as incomplete.

The response that was incomplete.

The sequence number of this event.

The type of the event. Always response.incomplete.

Emitted when a new output item is added.

The output item that was added.

The index of the output item that was added.

The sequence number of this event.

The type of the event. Always response.output_item.added.

Emitted when an output item is marked done.

The output item that was marked done.

The index of the output item that was marked done.

The sequence number of this event.

The type of the event. Always response.output_item.done.

Emitted when a new content part is added.

The index of the content part that was added.

The ID of the output item that the content part was added to.

The index of the output item that the content part was added to.

The content part that was added.

The sequence number of this event.

The type of the event. Always response.content_part.added.

Emitted when a content part is done.

The index of the content part that is done.

The ID of the output item that the content part was added to.

The index of the output item that the content part was added to.

The content part that is done.

The sequence number of this event.

The type of the event. Always response.content_part.done.

Emitted when there is an additional text delta.

The index of the content part that the text delta was added to.

The text delta that was added.

The ID of the output item that the text delta was added to.

The log probabilities of the tokens in the delta.

The index of the output item that the text delta was added to.

The sequence number for this event.

The type of the event. Always response.output_text.delta.

Emitted when text content is finalized.

The index of the content part that the text content is finalized.

The ID of the output item that the text content is finalized.

The log probabilities of the tokens in the delta.

The index of the output item that the text content is finalized.

The sequence number for this event.

The text content that is finalized.

The type of the event. Always response.output_text.done.

Emitted when there is a partial refusal text.

The index of the content part that the refusal text is added to.

The refusal text that is added.

The ID of the output item that the refusal text is added to.

The index of the output item that the refusal text is added to.

The sequence number of this event.

The type of the event. Always response.refusal.delta.

Emitted when refusal text is finalized.

The index of the content part that the refusal text is finalized.

The ID of the output item that the refusal text is finalized.

The index of the output item that the refusal text is finalized.

The refusal text that is finalized.

The sequence number of this event.

The type of the event. Always response.refusal.done.

Emitted when there is a partial function-call arguments delta.

The function-call arguments delta that is added.

The ID of the output item that the function-call arguments delta is added to.

The index of the output item that the function-call arguments delta is added to.

The sequence number of this event.

The type of the event. Always response.function_call_arguments.delta.

Emitted when function-call arguments are finalized.

The function-call arguments.

The name of the function that was called.

The index of the output item.

The sequence number of this event.

Emitted when a file search call is initiated.

The ID of the output item that the file search call is initiated.

The index of the output item that the file search call is initiated.

The sequence number of this event.

The type of the event. Always response.file_search_call.in_progress.

Emitted when a file search is currently searching.

The ID of the output item that the file search call is initiated.

The index of the output item that the file search call is searching.

The sequence number of this event.

The type of the event. Always response.file_search_call.searching.

Emitted when a file search call is completed (results found).

The ID of the output item that the file search call is initiated.

The index of the output item that the file search call is initiated.

The sequence number of this event.

The type of the event. Always response.file_search_call.completed.

Emitted when a web search call is initiated.

Unique ID for the output item associated with the web search call.

The index of the output item that the web search call is associated with.

The sequence number of the web search call being processed.

The type of the event. Always response.web_search_call.in_progress.

Emitted when a web search call is executing.

Unique ID for the output item associated with the web search call.

The index of the output item that the web search call is associated with.

The sequence number of the web search call being processed.

The type of the event. Always response.web_search_call.searching.

Emitted when a web search call is completed.

Unique ID for the output item associated with the web search call.

The index of the output item that the web search call is associated with.

The sequence number of the web search call being processed.

The type of the event. Always response.web_search_call.completed.

Emitted when a new reasoning summary part is added.

The ID of the item this summary part is associated with.

The index of the output item this summary part is associated with.

The summary part that was added.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The type of the event. Always response.reasoning_summary_part.added.

Emitted when a reasoning summary part is completed.

The ID of the item this summary part is associated with.

The index of the output item this summary part is associated with.

The completed summary part.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The type of the event. Always response.reasoning_summary_part.done.

Emitted when a delta is added to a reasoning summary text.

The text delta that was added to the summary.

The ID of the item this summary text delta is associated with.

The index of the output item this summary text delta is associated with.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The type of the event. Always response.reasoning_summary_text.delta.

Emitted when a reasoning summary text is completed.

The ID of the item this summary text is associated with.

The index of the output item this summary text is associated with.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The full text of the completed reasoning summary.

The type of the event. Always response.reasoning_summary_text.done.

Emitted when a delta is added to a reasoning text.

The index of the reasoning content part this delta is associated with.

The text delta that was added to the reasoning content.

The ID of the item this reasoning text delta is associated with.

The index of the output item this reasoning text delta is associated with.

The sequence number of this event.

The type of the event. Always response.reasoning_text.delta.

Emitted when a reasoning text is completed.

The index of the reasoning content part.

The ID of the item this reasoning text is associated with.

The index of the output item this reasoning text is associated with.

The sequence number of this event.

The full text of the completed reasoning content.

The type of the event. Always response.reasoning_text.done.

Emitted when an image generation tool call has completed and the final image is available.

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.image_generation_call.completed'.

Emitted when an image generation tool call is actively generating an image (intermediate state).

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

The sequence number of the image generation item being processed.

The type of the event. Always 'response.image_generation_call.generating'.

Emitted when an image generation tool call is in progress.

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

The sequence number of the image generation item being processed.

The type of the event. Always 'response.image_generation_call.in_progress'.

Emitted when a partial image is available during image generation streaming.

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

Base64-encoded partial image data, suitable for rendering as an image.

0-based index for the partial image (backend is 1-based, but this is 0-based for the user).

The sequence number of the image generation item being processed.

The type of the event. Always 'response.image_generation_call.partial_image'.

Emitted when there is a delta (partial update) to the arguments of an MCP tool call.

A JSON string containing the partial update to the arguments for the MCP tool call.

The unique identifier of the MCP tool call item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.mcp_call_arguments.delta'.

Emitted when the arguments for an MCP tool call are finalized.

A JSON string containing the finalized arguments for the MCP tool call.

The unique identifier of the MCP tool call item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.mcp_call_arguments.done'.

Emitted when an MCP tool call has completed successfully.

The ID of the MCP tool call item that completed.

The index of the output item that completed.

The sequence number of this event.

The type of the event. Always 'response.mcp_call.completed'.

Emitted when an MCP tool call has failed.

The ID of the MCP tool call item that failed.

The index of the output item that failed.

The sequence number of this event.

The type of the event. Always 'response.mcp_call.failed'.

Emitted when an MCP tool call is in progress.

The unique identifier of the MCP tool call item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.mcp_call.in_progress'.

Emitted when the list of available MCP tools has been successfully retrieved.

The ID of the MCP tool call item that produced this output.

The index of the output item that was processed.

The sequence number of this event.

The type of the event. Always 'response.mcp_list_tools.completed'.

Emitted when the attempt to list available MCP tools has failed.

The ID of the MCP tool call item that failed.

The index of the output item that failed.

The sequence number of this event.

The type of the event. Always 'response.mcp_list_tools.failed'.

Emitted when the system is in the process of retrieving the list of available MCP tools.

The ID of the MCP tool call item that is being processed.

The index of the output item that is being processed.

The sequence number of this event.

The type of the event. Always 'response.mcp_list_tools.in_progress'.

Emitted when a code interpreter call is in progress.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code interpreter call is in progress.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call.in_progress.

Emitted when the code interpreter is actively interpreting the code snippet.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code interpreter is interpreting code.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call.interpreting.

Emitted when the code interpreter call is completed.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code interpreter call is completed.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call.completed.

Emitted when a partial code snippet is streamed by the code interpreter.

The partial code snippet being streamed by the code interpreter.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code is being streamed.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call_code.delta.

Emitted when the code snippet is finalized by the code interpreter.

The final code snippet output by the code interpreter.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code is finalized.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call_code.done.

Emitted when an annotation is added to output text content.

The annotation object being added. (See annotation schema for details.)

The index of the annotation within the content part.

The index of the content part within the output item.

The unique identifier of the item to which the annotation is being added.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.output_text.annotation.added'.

Emitted when a response is queued and waiting to be processed.

The full response object that is queued.

The sequence number for this event.

The type of the event. Always 'response.queued'.

Event representing a delta (partial update) to the input of a custom tool call.

The incremental input data (delta) for the custom tool call.

Unique identifier for the API item associated with this event.

The index of the output this delta applies to.

The sequence number of this event.

The event type identifier.

Event indicating that input for a custom tool call is complete.

The complete input data for the custom tool call.

Unique identifier for the API item associated with this event.

The index of the output this event applies to.

The sequence number of this event.

The event type identifier.

Emitted when an error occurs.

The sequence number of this event.

The type of the event. Always error.

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
28
29
30
31
32
33
34
35
36
{
  "type": "response.created",
  "response": {
    "id": "resp_67ccfcdd16748190a91872c75d38539e09e4d4aac714747c",
    "object": "response",
    "created_at": 1741487325,
    "status": "in_progress",
    "error": null,
    "incomplete_details": null,
    "instructions": null,
    "max_output_tokens": null,
    "model": "gpt-4o-2024-08-06",
    "output": [],
    "parallel_tool_calls": true,
    "previous_response_id": null,
    "reasoning": {
      "effort": null,
      "summary": null
    },
    "store": true,
    "temperature": 1,
    "text": {
      "format": {
        "type": "text"
      }
    },
    "tool_choice": "auto",
    "tools": [],
    "top_p": 1,
    "truncation": "disabled",
    "usage": null,
    "user": null,
    "metadata": {}
  },
  "sequence_number": 1
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
28
29
30
31
32
33
34
35
36
{
  "type": "response.created",
  "response": {
    "id": "resp_67ccfcdd16748190a91872c75d38539e09e4d4aac714747c",
    "object": "response",
    "created_at": 1741487325,
    "status": "in_progress",
    "error": null,
    "incomplete_details": null,
    "instructions": null,
    "max_output_tokens": null,
    "model": "gpt-4o-2024-08-06",
    "output": [],
    "parallel_tool_calls": true,
    "previous_response_id": null,
    "reasoning": {
      "effort": null,
      "summary": null
    },
    "store": true,
    "temperature": 1,
    "text": {
      "format": {
        "type": "text"
      }
    },
    "tool_choice": "auto",
    "tools": [],
    "top_p": 1,
    "truncation": "disabled",
    "usage": null,
    "user": null,
    "metadata": {}
  },
  "sequence_number": 1
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
28
29
30
31
32
33
34
35
36
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
{
  "type": "response.in_progress",
  "response": {
    "id": "resp_67ccfcdd16748190a91872c75d38539e09e4d4aac714747c",
    "object": "response",
    "created_at": 1741487325,
    "status": "in_progress",
    "error": null,
    "incomplete_details": null,
    "instructions": null,
    "max_output_tokens": null,
    "model": "gpt-4o-2024-08-06",
    "output": [],
    "parallel_tool_calls": true,
    "previous_response_id": null,
    "reasoning": {
      "effort": null,
      "summary": null
    },
    "store": true,
    "temperature": 1,
    "text": {
      "format": {
        "type": "text"
      }
    },
    "tool_choice": "auto",
    "tools": [],
    "top_p": 1,
    "truncation": "disabled",
    "usage": null,
    "user": null,
    "metadata": {}
  },
  "sequence_number": 1
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/evals

**Contents:**
- Evals
- Create eval
    - Request body
    - Returns
- Get an eval
    - Path parameters
    - Returns
- Update an eval
    - Path parameters
    - Request body

Create, manage, and run evals in the OpenAI platform. Related guide: Evals

Create the structure of an evaluation that can be used to test a model's performance. An evaluation is a set of testing criteria and the config for a data source, which dictates the schema of the data used in the evaluation. After creating an evaluation, you can run it on different models and model parameters. We support several types of graders and datasources. For more information, see the Evals guide.

The configuration for the data source used for the evaluation runs. Dictates the schema of the data used in the evaluation.

A list of graders for all eval runs in this group. Graders can reference variables in the data source using double curly braces notation, like {{item.variable_name}}. To reference the model's output, use the sample namespace (ie, {{sample.output_text}}).

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The name of the evaluation.

The created Eval object.

Get an evaluation by ID.

The ID of the evaluation to retrieve.

The Eval object matching the specified ID.

Update certain properties of an evaluation.

The ID of the evaluation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Rename the evaluation.

The Eval object matching the updated version.

Delete an evaluation.

The ID of the evaluation to delete.

A deletion confirmation object.

List evaluations for a project.

Identifier for the last eval from the previous pagination request.

Number of evals to retrieve.

Sort order for evals by timestamp. Use asc for ascending order or desc for descending order.

Evals can be ordered by creation time or last updated time. Use created_at for creation time or updated_at for last updated time.

A list of evals matching the specified filters.

Get a list of runs for an evaluation.

The ID of the evaluation to retrieve runs for.

Identifier for the last run from the previous pagination request.

Number of runs to retrieve.

Sort order for runs by timestamp. Use asc for ascending order or desc for descending order. Defaults to asc.

Filter runs by status. One of queued | in_progress | failed | completed | canceled.

A list of EvalRun objects matching the specified ID.

Get an evaluation run by ID.

The ID of the evaluation to retrieve runs for.

The ID of the run to retrieve.

The EvalRun object matching the specified ID.

Kicks off a new run for a given evaluation, specifying the data source, and what model configuration to use to test. The datasource will be validated against the schema specified in the config of the evaluation.

The ID of the evaluation to create a run for.

Details about the run's data source.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The EvalRun object matching the specified ID.

Cancel an ongoing evaluation run.

The ID of the evaluation whose run you want to cancel.

The ID of the run to cancel.

The updated EvalRun object reflecting that the run is canceled.

The ID of the evaluation to delete the run from.

The ID of the run to delete.

An object containing the status of the delete operation.

Get an evaluation run output item by ID.

The ID of the evaluation to retrieve runs for.

The ID of the output item to retrieve.

The ID of the run to retrieve.

The EvalRunOutputItem object matching the specified ID.

Get a list of output items for an evaluation run.

The ID of the evaluation to retrieve runs for.

The ID of the run to retrieve output items for.

Identifier for the last output item from the previous pagination request.

Number of output items to retrieve.

Sort order for output items by timestamp. Use asc for ascending order or desc for descending order. Defaults to asc.

Filter output items by status. Use failed to filter by failed output items or pass to filter by passed output items.

A list of EvalRunOutputItem objects matching the specified ID.

An Eval object with a data source config and testing criteria. An Eval represents a task to be done for your LLM integration. Like:

The Unix timestamp (in seconds) for when the eval was created.

Configuration of data sources used in runs of the evaluation.

Unique identifier for the evaluation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The name of the evaluation.

A list of testing criteria.

A schema representing an evaluation run.

Unix timestamp (in seconds) when the evaluation run was created.

Information about the run's data source.

An object representing an error response from the Eval API.

The identifier of the associated evaluation.

Unique identifier for the evaluation run.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The model that is evaluated, if applicable.

The name of the evaluation run.

The type of the object. Always "eval.run".

Usage statistics for each model during the evaluation run.

Results per testing criteria applied during the evaluation run.

The URL to the rendered evaluation run report on the UI dashboard.

Counters summarizing the outcomes of the evaluation run.

The status of the evaluation run.

A schema representing an evaluation run output item.

Unix timestamp (in seconds) when the evaluation run was created.

Details of the input data source item.

The identifier for the data source item.

The identifier of the evaluation group.

Unique identifier for the evaluation run output item.

The type of the object. Always "eval.run.output_item".

A list of grader results for this output item.

The identifier of the evaluation run associated with this output item.

A sample containing the input and output of the evaluation run.

The status of the evaluation run.

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
curl https://api.openai.com/v1/evals \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Sentiment",
        "data_source_config": {
          "type": "stored_completions",
          "metadata": {
              "usecase": "chatbot"
          }
        },
        "testing_criteria": [
          {
            "type": "label_model",
            "model": "o3-mini",
            "input": [
              {
                "role": "developer",
                "content": "Classify the sentiment of the following statement as one of 'positive', 'neutral', or 'negative'"
              },
              {
                "role": "user",
                "content": "Statement: {{item.input}}"
              }
            ],
            "passing_labels": [
              "positive"
            ],
            "labels": [
              "positive",
              "neutral",
              "negative"
            ],
            "name": "Example label grader"
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
curl https://api.openai.com/v1/evals \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Sentiment",
        "data_source_config": {
          "type": "stored_completions",
          "metadata": {
              "usecase": "chatbot"
          }
        },
        "testing_criteria": [
          {
            "type": "label_model",
            "model": "o3-mini",
            "input": [
              {
                "role": "developer",
                "content": "Classify the sentiment of the following statement as one of 'positive', 'neutral', or 'negative'"
              },
              {
                "role": "user",
                "content": "Statement: {{item.input}}"
              }
            ],
            "passing_labels": [
              "positive"
            ],
            "labels": [
              "positive",
              "neutral",
              "negative"
            ],
            "name": "Example label grader"
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
from openai import OpenAI
client = OpenAI()

eval_obj = client.evals.create(
  name="Sentiment",
  data_source_config={
    "type": "stored_completions",
    "metadata": {"usecase": "chatbot"}
  },
  testing_criteria=[
    {
      "type": "label_model",
      "model": "o3-mini",
      "input": [
        {"role": "developer", "content": "Classify the sentiment of the following statement as one of 'positive', 'neutral', or 'negative'"},
        {"role": "user", "content": "Statement: {{item.input}}"}
      ],
      "passing_labels": ["positive"],
      "labels": ["positive", "neutral", "negative"],
      "name": "Example label grader"
    }
  ]
)
print(eval_obj)
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/debugging-requests

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

## 

**URL:** https://platform.openai.com/docs/api-reference/conversations/create-items

**Contents:**
- Conversations
- Create a conversation
    - Request body
    - Returns
- Retrieve a conversation
    - Path parameters
    - Returns
- Update a conversation
    - Path parameters
    - Request body

Create and manage conversations to store and retrieve conversation state across Response API calls.

Create a conversation.

Initial items to include in the conversation context. You may add up to 20 items at a time.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns a Conversation object.

The ID of the conversation to retrieve.

Returns a Conversation object.

Update a conversation

The ID of the conversation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns the updated Conversation object.

Delete a conversation. Items in the conversation will not be deleted.

The ID of the conversation to delete.

List all items for a conversation with the given ID.

The ID of the conversation to list items for.

An item ID to list items after, used in pagination.

Specify additional output data to include in the model response. Currently supported values are:

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

Returns a list object containing Conversation items.

Create items in a conversation with the given ID.

The ID of the conversation to add the item to.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

The items to add to the conversation. You may add up to 20 items at a time.

Returns the list of added items.

Get a single item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to retrieve.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

Returns a Conversation Item.

Delete an item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to delete.

Returns the updated Conversation object.

The time at which the conversation was created, measured in seconds since the Unix epoch.

The unique ID of the conversation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The object type, which is always conversation.

A list of Conversation items.

A list of conversation items.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
import OpenAI from "openai";
const client = new OpenAI();

const conversation = await client.conversations.create({
  metadata: { topic: "demo" },
  items: [
    { type: "message", role: "user", content: "Hello!" }
  ],
});
console.log(conversation);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses/delete

**Contents:**
- Responses
- Create a model response
    - Request body
    - Returns
- Get a model response
    - Path parameters
    - Query parameters
    - Returns
- Delete a model response
    - Path parameters

OpenAI's most advanced interface for generating model responses. Supports text and image inputs, and text outputs. Create stateful interactions with the model, using the output of previous responses as input. Extend the model's capabilities with built-in tools for file search, web search, computer use, and more. Allow the model access to external systems and data using function calling.

Creates a model response. Provide text or image inputs to generate text or JSON outputs. Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Specify additional output data to include in the model response. Currently supported values are:

Text, image, or file inputs to the model, used to generate a response.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

Whether to store the generated model response for later retrieval via API.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

Options for streaming responses. Only set this when you set stream: true.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

Returns a Response object.

Retrieves a model response with the given ID.

The ID of the response to retrieve.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an obfuscation field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set include_obfuscation to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API.

The sequence number of the event after which to start streaming.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

The Response object matching the specified ID.

Deletes a model response with the given ID.

The ID of the response to delete.

Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled. Learn more.

The ID of the response to cancel.

Runs a compaction pass over a conversation. Compaction returns encrypted, opaque items and the underlying logic may evolve over time.

Model ID used to generate the response, like gpt-5 or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

A compacted response object.

Learn when and how to compact long-running conversations in the conversation state guide.

Returns a list of input items for a given response.

The ID of the response to retrieve input items for.

An item ID to list items after, used in pagination.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

A list of input item objects.

Returns input token counts of the request.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

gpt-5 and o-series models only

Configuration options for reasoning models.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

The truncation strategy to use for the model response. - auto: If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation. - disabled (default): If the input size will exceed the context window size for a model, the request will fail with a 400 error.

The input token counts.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

Unix timestamp (in seconds) of when this Response was created.

An error object returned when the model fails to generate a Response.

Unique identifier for this Response.

Details about why the response is incomplete.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

The object type of this resource - always set to response.

An array of content items generated by the model.

SDK-only convenience property that contains the aggregated text output from all output_text items in the output array, if any are present. Supported in the Python and JavaScript SDKs.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

The status of the response generation. One of completed, failed, in_progress, cancelled, queued, or incomplete.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

A list of Response items.

A list of items used to generate this response.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

Unix timestamp (in seconds) when the compacted conversation was created.

The unique identifier for the compacted response.

The object type. Always response.compaction.

The compacted list of output items.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
8
9
10
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "Tell me a three sentence bedtime story about a unicorn."
});

console.log(response);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses

**Contents:**
- Responses
- Create a model response
    - Request body
    - Returns
- Get a model response
    - Path parameters
    - Query parameters
    - Returns
- Delete a model response
    - Path parameters

OpenAI's most advanced interface for generating model responses. Supports text and image inputs, and text outputs. Create stateful interactions with the model, using the output of previous responses as input. Extend the model's capabilities with built-in tools for file search, web search, computer use, and more. Allow the model access to external systems and data using function calling.

Creates a model response. Provide text or image inputs to generate text or JSON outputs. Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Specify additional output data to include in the model response. Currently supported values are:

Text, image, or file inputs to the model, used to generate a response.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

Whether to store the generated model response for later retrieval via API.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

Options for streaming responses. Only set this when you set stream: true.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

Returns a Response object.

Retrieves a model response with the given ID.

The ID of the response to retrieve.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an obfuscation field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set include_obfuscation to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API.

The sequence number of the event after which to start streaming.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

The Response object matching the specified ID.

Deletes a model response with the given ID.

The ID of the response to delete.

Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled. Learn more.

The ID of the response to cancel.

Runs a compaction pass over a conversation. Compaction returns encrypted, opaque items and the underlying logic may evolve over time.

Model ID used to generate the response, like gpt-5 or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

A compacted response object.

Learn when and how to compact long-running conversations in the conversation state guide.

Returns a list of input items for a given response.

The ID of the response to retrieve input items for.

An item ID to list items after, used in pagination.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

A list of input item objects.

Returns input token counts of the request.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

gpt-5 and o-series models only

Configuration options for reasoning models.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

The truncation strategy to use for the model response. - auto: If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation. - disabled (default): If the input size will exceed the context window size for a model, the request will fail with a 400 error.

The input token counts.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

Unix timestamp (in seconds) of when this Response was created.

An error object returned when the model fails to generate a Response.

Unique identifier for this Response.

Details about why the response is incomplete.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

The object type of this resource - always set to response.

An array of content items generated by the model.

SDK-only convenience property that contains the aggregated text output from all output_text items in the output array, if any are present. Supported in the Python and JavaScript SDKs.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

The status of the response generation. One of completed, failed, in_progress, cancelled, queued, or incomplete.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

A list of Response items.

A list of items used to generate this response.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

Unix timestamp (in seconds) when the compacted conversation was created.

The unique identifier for the compacted response.

The object type. Always response.compaction.

The compacted list of output items.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
8
9
10
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "Tell me a three sentence bedtime story about a unicorn."
});

console.log(response);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/containers/createContainers

**Contents:**
- Containers
- Create container
    - Request body
    - Returns
- List containers
    - Query parameters
    - Returns
- Retrieve container
    - Path parameters
    - Returns

Create and manage containers for use with the Code Interpreter tool.

Name of the container to create.

Container expiration time in seconds relative to the 'anchor' time.

IDs of files to copy to the container.

Optional memory limit for the container. Defaults to "1g".

The created container object.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

a list of container objects.

Retrieves a container.

The container object.

The ID of the container to delete.

Unix timestamp (in seconds) when the container was created.

The container will expire after this time period. The anchor is the reference point for the expiration. The minutes is the number of minutes after the anchor before the container expires.

Unique identifier for the container.

Unix timestamp (in seconds) when the container was last active.

The memory limit configured for the container.

Name of the container.

The type of this object.

Status of the container (e.g., active, deleted).

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
curl https://api.openai.com/v1/containers \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "My Container",
        "memory_limit": "4g"
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
curl https://api.openai.com/v1/containers \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "My Container",
        "memory_limit": "4g"
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
{
    "id": "cntr_682e30645a488191b6363a0cbefc0f0a025ec61b66250591",
    "object": "container",
    "created_at": 1747857508,
    "status": "running",
    "expires_after": {
        "anchor": "last_active_at",
        "minutes": 20
    },
    "last_active_at": 1747857508,
    "memory_limit": "4g",
    "name": "My Container"
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/roles

**Contents:**
- Roles
- List organization roles
    - Query parameters
    - Returns
- Create organization role
    - Request body
    - Returns
- Update organization role
    - Path parameters
    - Request body

Create and manage custom roles that can be assigned to groups and users at the organization or project level.

Lists the roles configured for the organization.

Cursor for pagination. Provide the value from the previous response's next field to continue listing roles.

A limit on the number of roles to return. Defaults to 1000.

Sort order for the returned roles.

A list of role objects.

Creates a custom role for the organization.

Permissions to grant to the role.

Unique name for the role.

The created role object.

Updates an existing organization role.

The ID of the role to update.

The updated role object.

Deletes a custom role from the organization.

The ID of the role to delete.

Confirmation of the deleted role.

Lists the roles configured for a project.

The ID of the project to inspect.

Cursor for pagination. Provide the value from the previous response's next field to continue listing roles.

A limit on the number of roles to return. Defaults to 1000.

Sort order for the returned roles.

A list of role objects configured on the project.

Creates a custom role for a project.

The ID of the project to update.

Permissions to grant to the role.

Unique name for the role.

The created role object.

Updates an existing project role.

The ID of the project to update.

The ID of the role to update.

The updated role object.

Deletes a custom role from a project.

The ID of the project to update.

The ID of the role to delete.

Confirmation of the deleted role.

Details about a role that can be assigned through the public Roles API.

Identifier for the role.

Unique name for the role.

Permissions granted by the role.

Whether the role is predefined and managed by OpenAI.

Resource type the role is bound to (for example api.organization or api.project).

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/roles?limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/roles?limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
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
{
    "object": "list",
    "data": [
        {
            "object": "role",
            "id": "role_01J1F8ROLE01",
            "name": "API Group Manager",
            "description": "Allows managing organization groups",
            "permissions": [
                "api.groups.read",
                "api.groups.write"
            ],
            "resource_type": "api.organization",
            "predefined_role": false
        }
    ],
    "has_more": false,
    "next": null
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
{
    "object": "list",
    "data": [
        {
            "object": "role",
            "id": "role_01J1F8ROLE01",
            "name": "API Group Manager",
            "description": "Allows managing organization groups",
            "permissions": [
                "api.groups.read",
                "api.groups.write"
            ],
            "resource_type": "api.organization",
            "predefined_role": false
        }
    ],
    "has_more": false,
    "next": null
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/realtime-sessions

**Contents:**
- Client secrets
- Create client secret
    - Request body
    - Returns
- Session response object

REST API endpoint to generate ephemeral client secrets for use in client-side applications. Client secrets are short-lived tokens that can be passed to a client app, such as a web frontend or mobile client, which grants access to the Realtime API without leaking your main API key. You can configure a custom TTL for each client secret.

You can also attach session configuration options to the client secret, which will be applied to any sessions created using that client secret, but these can also be overridden by the client connection.

Learn more about authentication with client secrets over WebRTC.

Create a Realtime client secret with an associated session configuration.

Configuration for the client secret expiration. Expiration refers to the time after which a client secret will no longer be valid for creating sessions. The session itself may continue after that time once started. A secret can be used to create multiple sessions until it expires.

Session configuration to use for the client secret. Choose either a realtime session or a transcription session.

The created client secret and the effective session object. The client secret is a string that looks like ek_1234.

Response from creating a session and client secret for the Realtime API.

Expiration timestamp for the client secret, in seconds since epoch.

The session configuration for either a realtime or transcription session.

The generated client secret value.

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
curl -X POST https://api.openai.com/v1/realtime/client_secrets \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "expires_after": {
      "anchor": "created_at",
      "seconds": 600
    },
    "session": {
      "type": "realtime",
      "model": "gpt-realtime",
      "instructions": "You are a friendly assistant."
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
12
13
14
curl -X POST https://api.openai.com/v1/realtime/client_secrets \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "expires_after": {
      "anchor": "created_at",
      "seconds": 600
    },
    "session": {
      "type": "realtime",
      "model": "gpt-realtime",
      "instructions": "You are a friendly assistant."
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
12
13
14
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
40
41
42
43
{
  "value": "ek_68af296e8e408191a1120ab6383263c2",
  "expires_at": 1756310470,
  "session": {
    "type": "realtime",
    "object": "realtime.session",
    "id": "sess_C9CiUVUzUzYIssh3ELY1d",
    "model": "gpt-realtime",
    "output_modalities": [
      "audio"
    ],
    "instructions": "You are a friendly assistant.",
    "tools": [],
    "tool_choice": "auto",
    "max_output_tokens": "inf",
    "tracing": null,
    "truncation": "auto",
    "prompt": null,
    "expires_at": 0,
    "audio": {
      "input": {
        "format": {
          "type": "audio/pcm",
          "rate": 24000
        },
        "transcription": null,
        "noise_reduction": null,
        "turn_detection": {
          "type": "server_vad",
        }
      },
      "output": {
        "format": {
          "type": "audio/pcm",
          "rate": 24000
        },
        "voice": "alloy",
        "speed": 1.0
      }
    },
    "include": null
  }
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/groups

**Contents:**
- Groups
- List groups
    - Query parameters
    - Returns
- Create group
    - Request body
    - Returns
- Update group
    - Path parameters
    - Request body

Manage reusable collections of users for organization-wide access control and maintain their membership.

Lists all groups in the organization.

A cursor for use in pagination. after is a group ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with group_abc, your subsequent call can include after=group_abc in order to fetch the next page of the list.

A limit on the number of groups to be returned. Limit can range between 0 and 1000, and the default is 100.

Specifies the sort order of the returned groups.

A list of group objects.

Creates a new group in the organization.

Human readable name for the group.

The created group object.

Updates a group's information.

The ID of the group to update.

New display name for the group.

The updated group object.

Deletes a group from the organization.

The ID of the group to delete.

Confirmation of the deleted group.

Lists the users assigned to a group.

The ID of the group to inspect.

A cursor for use in pagination. Provide the ID of the last user from the previous list response to retrieve the next page.

A limit on the number of users to be returned. Limit can range between 0 and 1000, and the default is 100.

Specifies the sort order of users in the list.

A list of user objects.

Adds a user to a group.

The ID of the group to update.

Identifier of the user to add to the group.

The created group user object.

Removes a user from a group.

The ID of the group to update.

The ID of the user to remove from the group.

Confirmation of the deleted group user object.

Confirmation payload returned after adding a user to a group.

Identifier of the group the user was added to.

Identifier of the user that was added.

Summary information about a group returned in role assignment responses.

Unix timestamp (in seconds) when the group was created.

Identifier for the group.

Display name of the group.

Whether the group is managed through SCIM.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/groups?limit=20&order=asc \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/groups?limit=20&order=asc \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
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
{
    "object": "list",
    "data": [
        {
            "object": "group",
            "id": "group_01J1F8ABCDXYZ",
            "name": "Support Team",
            "created_at": 1711471533,
            "is_scim_managed": false
        }
    ],
    "has_more": false,
    "next": null
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
{
    "object": "list",
    "data": [
        {
            "object": "group",
            "id": "group_01J1F8ABCDXYZ",
            "name": "Support Team",
            "created_at": 1711471533,
            "is_scim_managed": false
        }
    ],
    "has_more": false,
    "next": null
}
```

---

## Node referenceBeta

**URL:** https://platform.openai.com/docs/guides/node-reference

**Contents:**
- Node referenceBeta
  - Core nodes
    - Start
    - Agent
    - Note
  - Tool nodes
    - File search
    - Guardrails
    - MCP
  - Logic nodes

Agent Builder is a visual canvas for composing agentic worfklows. Workflows are made up of nodes and connections that control the sequence and flow. Insert nodes, then configure and connect them to define the process you want your agents to follow.

Explore all available nodes below. To learn more, read the Agent Builder guide.

Get started with basic building blocks. All workflows have start and agent nodes.

Define inputs to your workflow. For user input in a chat workflow, start nodes do two things:

All chat start nodes have input_as_text as an input variable. You can add state variables too.

Define instructions, tools, and model configuration, or attach evaluations.

Keep each agent well defined in scope. In our homework helper example, we use one agent to rewrite the user's query for more specificity and relevance with the knowledge base. We use another agent to classify the query as either Q&A or fact-finding, and another agent to field each type of question.

Add model behavior instructions and user messages as you would with any other model prompt. To pipe output from a previous step, you can add it as context.

You can have as many agent nodes as you'd like.

Leave comments and explanations about your workflow. Unlike other nodes, notes don't do anything in the flow. They're just helpful commentary for you and your team.

Tool nodes let you equip your agents with tools and external services. You can retrieve data, monitor for misuse, and connect to external services.

Retrieve data from vector stores you've created in the OpenAI platform. Search by vector store ID, and add a query for what the model should search for. You can use variables to include output from previous nodes in the workflow.

See the file search documentation to set up vector stores and see supported file types.

To search outside of your hosted storage with OpenAI, use MCP instead.

Set up input monitors for unwanted inputs such as personally identifiable information (PII), jailbreaks, hallucinations, and other misuse.

Guardrails are pass/fail by default, meaning they test the output from a previous node, and you define what happens next. When there's a guardrails failure, we recommend either ending the workflow or returning to the previous step with a reminder of safe use.

Call third-party tools and services. Connect with OpenAI connectors or third-party servers, or add your own server. MCP connections are helpful in a workflow that needs to read or search data in another application, like Gmail or Zapier.

Browse options in the Agent Builder. To learn more about MCP, see the connectors and MCP documentation.

Logic nodes let you write custom logic and define the control flow—for example, looping on custom conditions, or asking the user for approval before continuing an operation.

Add conditional logic. Use Common Expression Language (CEL) to create a custom expression. Useful for defining what to do with input that's been sorted into classifications.

For example, if an agent classifies input as Q&A, route that query to the Q&A agent for a straightforward answer. If it's an open-ended query, route to an agent that finds relevant facts. Else, end the workflow.

Loop on custom conditions. Use Common Expression Language (CEL) to create a custom expression. Useful for checking whether a condition is still true.

Defer to end-users for approval. Useful for workflows where agents draft work that could use a human review before it goes out.

For example, picture an agent workflow that sends emails on your behalf. You'd include an agent node that outputs an email widget, then a human approval node immediately following. You can configure the human approval node to ask, "Would you like me to send this email?" and, if approved, proceeds to an MCP node that connects to Gmail.

Data nodes let you define and manipulate data in your workflow. Reshape outputs or define global variables for use across your workflow.

Reshape outputs (e.g., object → array). Useful for enforcing types to adhere to your schema or reshaping outputs for agents to read and understand as inputs.

Define global variables for use across the workflow. Useful for when an agent takes input and outputs something new that you'll want to use throughout the workflow. You can define that output as a new global variable.

---

## 

**URL:** https://platform.openai.com/docs/api-reference/files

**Contents:**
- Files
- Upload file
    - Request body
    - Returns
- List files
    - Query parameters
    - Returns
- Retrieve file
    - Path parameters
    - Returns

Files are used to upload documents that can be used with features like Assistants, Fine-tuning, and Batch API.

Upload a file that can be used across various endpoints. Individual files can be up to 512 MB, and the size of all files uploaded by one organization can be up to 1 TB.

Please contact us if you need to increase these storage limits.

The File object (not file name) to be uploaded.

The intended purpose of the uploaded file. One of: - assistants: Used in the Assistants API - batch: Used in the Batch API - fine-tune: Used for fine-tuning - vision: Images used for vision fine-tuning - user_data: Flexible file type for any purpose - evals: Used for eval data sets

The expiration policy for a file. By default, files with purpose=batch expire after 30 days and all other files are persisted until they are manually deleted.

The uploaded File object.

Returns a list of files.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 10,000, and the default is 10,000.

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

Only return files with the given purpose.

A list of File objects.

Returns information about a specific file.

The ID of the file to use for this request.

The File object matching the specified ID.

Delete a file and remove it from all vector stores.

The ID of the file to use for this request.

Returns the contents of the specified file.

The ID of the file to use for this request.

The File object represents a document that has been uploaded to OpenAI.

The size of the file, in bytes.

The Unix timestamp (in seconds) for when the file was created.

The Unix timestamp (in seconds) for when the file will expire.

The name of the file.

The file identifier, which can be referenced in the API endpoints.

The object type, which is always file.

The intended purpose of the file. Supported values are assistants, assistants_output, batch, batch_output, fine-tune, fine-tune-results, vision, and user_data.

Deprecated. The current status of the file, which can be either uploaded, processed, or error.

Deprecated. For details on why a fine-tuning training file failed validation, see the error field on fine_tuning.job.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
5
6
curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F purpose="fine-tune" \
  -F file="@mydata.jsonl"
  -F expires_after[anchor]="created_at"
  -F expires_after[seconds]=2592000
```

Example 2 (bash):
```bash
1
2
3
4
5
6
curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F purpose="fine-tune" \
  -F file="@mydata.jsonl"
  -F expires_after[anchor]="created_at"
  -F expires_after[seconds]=2592000
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
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
from openai import OpenAI
client = OpenAI()

client.files.create(
  file=open("mydata.jsonl", "rb"),
  purpose="fine-tune",
  expires_after={
    "anchor": "created_at",
    "seconds": 2592000
  }
)
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/realtime-client-events

**Contents:**
- Client events
- session.update
- input_audio_buffer.append
- input_audio_buffer.commit
- input_audio_buffer.clear
- conversation.item.create
- conversation.item.retrieve
- conversation.item.truncate
- conversation.item.delete
- response.create

These are events that the OpenAI Realtime WebSocket server will accept from the client.

Send this event to update the session’s configuration. The client may send this event at any time to update any field except for voice and model. voice can be updated only if there have been no other audio outputs yet.

When the server receives a session.update, it will respond with a session.updated event showing the full, effective configuration. Only the fields that are present in the session.update are updated. To clear a field like instructions, pass an empty string. To clear a field like tools, pass an empty array. To clear a field like turn_detection, pass null.

Optional client-generated ID used to identify this event. This is an arbitrary string that a client may assign. It will be passed back if there is an error with the event, but the corresponding session.updated event will not include it.

Update the Realtime session. Choose either a realtime session or a transcription session.

The event type, must be session.update.

Send this event to append audio bytes to the input audio buffer. The audio buffer is temporary storage you can write to and later commit. A "commit" will create a new user message item in the conversation history from the buffer content and clear the buffer. Input audio transcription (if enabled) will be generated when the buffer is committed.

If VAD is enabled the audio buffer is used to detect speech and the server will decide when to commit. When Server VAD is disabled, you must commit the audio buffer manually. Input audio noise reduction operates on writes to the audio buffer.

The client may choose how much audio to place in each event up to a maximum of 15 MiB, for example streaming smaller chunks from the client may allow the VAD to be more responsive. Unlike most other client events, the server will not send a confirmation response to this event.

Base64-encoded audio bytes. This must be in the format specified by the input_audio_format field in the session configuration.

Optional client-generated ID used to identify this event.

The event type, must be input_audio_buffer.append.

Send this event to commit the user input audio buffer, which will create a new user message item in the conversation. This event will produce an error if the input audio buffer is empty. When in Server VAD mode, the client does not need to send this event, the server will commit the audio buffer automatically.

Committing the input audio buffer will trigger input audio transcription (if enabled in session configuration), but it will not create a response from the model. The server will respond with an input_audio_buffer.committed event.

Optional client-generated ID used to identify this event.

The event type, must be input_audio_buffer.commit.

Send this event to clear the audio bytes in the buffer. The server will respond with an input_audio_buffer.cleared event.

Optional client-generated ID used to identify this event.

The event type, must be input_audio_buffer.clear.

Add a new Item to the Conversation's context, including messages, function calls, and function call responses. This event can be used both to populate a "history" of the conversation and to add new items mid-stream, but has the current limitation that it cannot populate assistant audio messages.

If successful, the server will respond with a conversation.item.created event, otherwise an error event will be sent.

Optional client-generated ID used to identify this event.

A single item within a Realtime conversation.

The ID of the preceding item after which the new item will be inserted. If not set, the new item will be appended to the end of the conversation. If set to root, the new item will be added to the beginning of the conversation. If set to an existing ID, it allows an item to be inserted mid-conversation. If the ID cannot be found, an error will be returned and the item will not be added.

The event type, must be conversation.item.create.

Send this event when you want to retrieve the server's representation of a specific item in the conversation history. This is useful, for example, to inspect user audio after noise cancellation and VAD. The server will respond with a conversation.item.retrieved event, unless the item does not exist in the conversation history, in which case the server will respond with an error.

Optional client-generated ID used to identify this event.

The ID of the item to retrieve.

The event type, must be conversation.item.retrieve.

Send this event to truncate a previous assistant message’s audio. The server will produce audio faster than realtime, so this event is useful when the user interrupts to truncate audio that has already been sent to the client but not yet played. This will synchronize the server's understanding of the audio with the client's playback.

Truncating audio will delete the server-side text transcript to ensure there is not text in the context that hasn't been heard by the user.

If successful, the server will respond with a conversation.item.truncated event.

Inclusive duration up to which audio is truncated, in milliseconds. If the audio_end_ms is greater than the actual audio duration, the server will respond with an error.

The index of the content part to truncate. Set this to 0.

Optional client-generated ID used to identify this event.

The ID of the assistant message item to truncate. Only assistant message items can be truncated.

The event type, must be conversation.item.truncate.

Send this event when you want to remove any item from the conversation history. The server will respond with a conversation.item.deleted event, unless the item does not exist in the conversation history, in which case the server will respond with an error.

Optional client-generated ID used to identify this event.

The ID of the item to delete.

The event type, must be conversation.item.delete.

This event instructs the server to create a Response, which means triggering model inference. When in Server VAD mode, the server will create Responses automatically.

A Response will include at least one Item, and may have two, in which case the second will be a function call. These Items will be appended to the conversation history by default.

The server will respond with a response.created event, events for Items and content created, and finally a response.done event to indicate the Response is complete.

The response.create event includes inference configuration like instructions and tools. If these are set, they will override the Session's configuration for this Response only.

Responses can be created out-of-band of the default Conversation, meaning that they can have arbitrary input, and it's possible to disable writing the output to the Conversation. Only one Response can write to the default Conversation at a time, but otherwise multiple Responses can be created in parallel. The metadata field is a good way to disambiguate multiple simultaneous Responses.

Clients can set conversation to none to create a Response that does not write to the default Conversation. Arbitrary input can be provided with the input field, which is an array accepting raw Items and references to existing Items.

Optional client-generated ID used to identify this event.

Create a new Realtime response with these parameters

The event type, must be response.create.

Send this event to cancel an in-progress response. The server will respond with a response.done event with a status of response.status=cancelled. If there is no response to cancel, the server will respond with an error. It's safe to call response.cancel even if no response is in progress, an error will be returned the session will remain unaffected.

Optional client-generated ID used to identify this event.

A specific response ID to cancel - if not provided, will cancel an in-progress response in the default conversation.

The event type, must be response.cancel.

WebRTC/SIP Only: Emit to cut off the current audio response. This will trigger the server to stop generating audio and emit a output_audio_buffer.cleared event. This event should be preceded by a response.cancel client event to stop the generation of the current response. Learn more.

The unique ID of the client event used for error handling.

The event type, must be output_audio_buffer.clear.

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
28
29
30
31
32
33
34
35
36
{
  "type": "session.update",
  "session": {
    "type": "realtime",
    "instructions": "You are a creative assistant that helps with design tasks.",
    "tools": [
      {
        "type": "function",
        "name": "display_color_palette",
        "description": "Call this function when a user asks for a color palette.",
        "parameters": {
          "type": "object",
          "properties": {
            "theme": {
              "type": "string",
              "description": "Description of the theme for the color scheme."
            },
            "colors": {
              "type": "array",
              "description": "Array of five hex color codes based on the theme.",
              "items": {
                "type": "string",
                "description": "Hex color code"
              }
            }
          },
          "required": [
            "theme",
            "colors"
          ]
        }
      }
    ],
    "tool_choice": "auto"
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
{
  "type": "session.update",
  "session": {
    "type": "realtime",
    "instructions": "You are a creative assistant that helps with design tasks.",
    "tools": [
      {
        "type": "function",
        "name": "display_color_palette",
        "description": "Call this function when a user asks for a color palette.",
        "parameters": {
          "type": "object",
          "properties": {
            "theme": {
              "type": "string",
              "description": "Description of the theme for the color scheme."
            },
            "colors": {
              "type": "array",
              "description": "Array of five hex color codes based on the theme.",
              "items": {
                "type": "string",
                "description": "Hex color code"
              }
            }
          },
          "required": [
            "theme",
            "colors"
          ]
        }
      }
    ],
    "tool_choice": "auto"
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
```

Example 4 (unknown):
```unknown
1
2
3
4
5
{
    "event_id": "event_456",
    "type": "input_audio_buffer.append",
    "audio": "Base64EncodedAudioData"
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses/object

**Contents:**
- Responses
- Create a model response
    - Request body
    - Returns
- Get a model response
    - Path parameters
    - Query parameters
    - Returns
- Delete a model response
    - Path parameters

OpenAI's most advanced interface for generating model responses. Supports text and image inputs, and text outputs. Create stateful interactions with the model, using the output of previous responses as input. Extend the model's capabilities with built-in tools for file search, web search, computer use, and more. Allow the model access to external systems and data using function calling.

Creates a model response. Provide text or image inputs to generate text or JSON outputs. Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Specify additional output data to include in the model response. Currently supported values are:

Text, image, or file inputs to the model, used to generate a response.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

Whether to store the generated model response for later retrieval via API.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

Options for streaming responses. Only set this when you set stream: true.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

Returns a Response object.

Retrieves a model response with the given ID.

The ID of the response to retrieve.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an obfuscation field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set include_obfuscation to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API.

The sequence number of the event after which to start streaming.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

The Response object matching the specified ID.

Deletes a model response with the given ID.

The ID of the response to delete.

Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled. Learn more.

The ID of the response to cancel.

Runs a compaction pass over a conversation. Compaction returns encrypted, opaque items and the underlying logic may evolve over time.

Model ID used to generate the response, like gpt-5 or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

A compacted response object.

Learn when and how to compact long-running conversations in the conversation state guide.

Returns a list of input items for a given response.

The ID of the response to retrieve input items for.

An item ID to list items after, used in pagination.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

A list of input item objects.

Returns input token counts of the request.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

gpt-5 and o-series models only

Configuration options for reasoning models.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

The truncation strategy to use for the model response. - auto: If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation. - disabled (default): If the input size will exceed the context window size for a model, the request will fail with a 400 error.

The input token counts.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

Unix timestamp (in seconds) of when this Response was created.

An error object returned when the model fails to generate a Response.

Unique identifier for this Response.

Details about why the response is incomplete.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

The object type of this resource - always set to response.

An array of content items generated by the model.

SDK-only convenience property that contains the aggregated text output from all output_text items in the output array, if any are present. Supported in the Python and JavaScript SDKs.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

The status of the response generation. One of completed, failed, in_progress, cancelled, queued, or incomplete.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

A list of Response items.

A list of items used to generate this response.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

Unix timestamp (in seconds) when the compacted conversation was created.

The unique identifier for the compacted response.

The object type. Always response.compaction.

The compacted list of output items.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
8
9
10
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "Tell me a three sentence bedtime story about a unicorn."
});

console.log(response);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/invite

**Contents:**
- Invites
- List invites
    - Query parameters
    - Returns
- Create invite
    - Request body
    - Returns
- Retrieve invite
    - Path parameters
    - Returns

Invite and manage invitations for an organization.

Returns a list of invites in the organization.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

A list of Invite objects.

Create an invite for a user to the organization. The invite must be accepted by the user before they have access to the organization.

Send an email to this address

An array of projects to which membership is granted at the same time the org invite is accepted. If omitted, the user will be invited to the default project for compatibility with legacy behavior.

The created Invite object.

The ID of the invite to retrieve.

The Invite object matching the specified ID.

Delete an invite. If the invite has already been accepted, it cannot be deleted.

The ID of the invite to delete.

Confirmation that the invite has been deleted

Represents an individual invite to the organization.

The Unix timestamp (in seconds) of when the invite was accepted.

The email address of the individual to whom the invite was sent

The Unix timestamp (in seconds) of when the invite expires.

The identifier, which can be referenced in API endpoints

The Unix timestamp (in seconds) of when the invite was sent.

The object type, which is always organization.invite

The projects that were granted membership upon acceptance of the invite.

accepted,expired, or pending

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/invites?after=invite-abc&limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/invites?after=invite-abc&limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
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
{
  "object": "list",
  "data": [
    {
      "object": "organization.invite",
      "id": "invite-abc",
      "email": "user@example.com",
      "role": "owner",
      "status": "accepted",
      "invited_at": 1711471533,
      "expires_at": 1711471533,
      "accepted_at": 1711471533
    }
  ],
  "first_id": "invite-abc",
  "last_id": "invite-abc",
  "has_more": false
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
{
  "object": "list",
  "data": [
    {
      "object": "organization.invite",
      "id": "invite-abc",
      "email": "user@example.com",
      "role": "owner",
      "status": "accepted",
      "invited_at": 1711471533,
      "expires_at": 1711471533,
      "accepted_at": 1711471533
    }
  ],
  "first_id": "invite-abc",
  "last_id": "invite-abc",
  "has_more": false
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/container-files/createContainerFile

**Contents:**
- Container Files
- Create container file
    - Path parameters
    - Request body
    - Returns
- List container files
    - Path parameters
    - Query parameters
    - Returns
- Retrieve container file

Create and manage container files for use with the Code Interpreter tool.

Creates a container file.

The File object (not file name) to be uploaded.

Name of the file to create.

The created container file object.

Lists container files.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

Sort order by the created_at timestamp of the objects. asc for ascending order and desc for descending order.

a list of container file objects.

Retrieves a container file.

The container file object.

Retrieves a container file content.

The contents of the container file.

Delete a container file.

Size of the file in bytes.

The container this file belongs to.

Unix timestamp (in seconds) when the file was created.

Unique identifier for the file.

The type of this object (container.file).

Path of the file in the container.

Source of the file (e.g., user, assistant).

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/containers/cntr_682e0e7318108198aa783fd921ff305e08e78805b9fdbb04/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@example.txt"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/containers/cntr_682e0e7318108198aa783fd921ff305e08e78805b9fdbb04/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@example.txt"
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
{
  "id": "cfile_682e0e8a43c88191a7978f477a09bdf5",
  "object": "container.file",
  "created_at": 1747848842,
  "bytes": 880,
  "container_id": "cntr_682e0e7318108198aa783fd921ff305e08e78805b9fdbb04",
  "path": "/mnt/data/88e12fa445d32636f190a0b33daed6cb-tsconfig.json",
  "source": "user"
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
{
  "id": "cfile_682e0e8a43c88191a7978f477a09bdf5",
  "object": "container.file",
  "created_at": 1747848842,
  "bytes": 880,
  "container_id": "cntr_682e0e7318108198aa783fd921ff305e08e78805b9fdbb04",
  "path": "/mnt/data/88e12fa445d32636f190a0b33daed6cb-tsconfig.json",
  "source": "user"
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses/input-items

**Contents:**
- Responses
- Create a model response
    - Request body
    - Returns
- Get a model response
    - Path parameters
    - Query parameters
    - Returns
- Delete a model response
    - Path parameters

OpenAI's most advanced interface for generating model responses. Supports text and image inputs, and text outputs. Create stateful interactions with the model, using the output of previous responses as input. Extend the model's capabilities with built-in tools for file search, web search, computer use, and more. Allow the model access to external systems and data using function calling.

Creates a model response. Provide text or image inputs to generate text or JSON outputs. Have the model call your own custom code or use built-in tools like web search or file search to use your own data as input for the model's response.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Specify additional output data to include in the model response. Currently supported values are:

Text, image, or file inputs to the model, used to generate a response.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

Whether to store the generated model response for later retrieval via API.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

Options for streaming responses. Only set this when you set stream: true.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

Returns a Response object.

Retrieves a model response with the given ID.

The ID of the response to retrieve.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an obfuscation field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set include_obfuscation to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API.

The sequence number of the event after which to start streaming.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section below for more information.

The Response object matching the specified ID.

Deletes a model response with the given ID.

The ID of the response to delete.

Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled. Learn more.

The ID of the response to cancel.

Runs a compaction pass over a conversation. Compaction returns encrypted, opaque items and the underlying logic may evolve over time.

Model ID used to generate the response, like gpt-5 or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

A compacted response object.

Learn when and how to compact long-running conversations in the conversation state guide.

Returns a list of input items for a given response.

The ID of the response to retrieve input items for.

An item ID to list items after, used in pagination.

Additional fields to include in the response. See the include parameter for Response creation above for more information.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

A list of input item objects.

Returns input token counts of the request.

The conversation that this response belongs to. Items from this conversation are prepended to input_items for this response request. Input items and output items from this response are automatically added to this conversation after this response completes.

Text, image, or file inputs to the model, used to generate a response

A system (or developer) message inserted into the model's context. When used along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

gpt-5 and o-series models only

Configuration options for reasoning models.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

The truncation strategy to use for the model response. - auto: If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation. - disabled (default): If the input size will exceed the context window size for a model, the request will fail with a 400 error.

The input token counts.

Whether to run the model response in the background. Learn more.

The conversation that this response belongs to. Input items and output items from this response are automatically added to this conversation.

Unix timestamp (in seconds) of when this Response was created.

An error object returned when the model fails to generate a Response.

Unique identifier for this Response.

Details about why the response is incomplete.

A system (or developer) message inserted into the model's context.

When using along with previous_response_id, the instructions from a previous response will not be carried over to the next response. This makes it simple to swap out system (or developer) messages in new responses.

An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens.

The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Model ID used to generate the response, like gpt-4o or o3. OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points. Refer to the model guide to browse and compare available models.

The object type of this resource - always set to response.

An array of content items generated by the model.

SDK-only convenience property that contains the aggregated text output from all output_text items in the output array, if any are present. Supported in the Python and JavaScript SDKs.

Whether to allow the model to run tool calls in parallel.

The unique ID of the previous response to the model. Use this to create multi-turn conversations. Learn more about conversation state. Cannot be used in conjunction with conversation.

Reference to a prompt template and its variables. Learn more.

Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the user field. Learn more.

The retention policy for the prompt cache. Set to 24h to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours. Learn more.

gpt-5 and o-series models only

Configuration options for reasoning models.

A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies. The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. Learn more.

Specifies the processing type used for serving the request.

When the service_tier parameter is set, the response body will include the service_tier value based on the processing mode actually used to serve the request. This response value may be different from the value set in the parameter.

The status of the response generation. One of completed, failed, in_progress, cancelled, queued, or incomplete.

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.

Configuration options for a text response from the model. Can be plain text or structured JSON data. Learn more:

How the model should select which tool (or tools) to use when generating a response. See the tools parameter to see how to specify which tools the model can call.

An array of tools the model may call while generating a response. You can specify which tool to use by setting the tool_choice parameter.

We support the following categories of tools:

An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability.

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

The truncation strategy to use for the model response.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

This field is being replaced by safety_identifier and prompt_cache_key. Use prompt_cache_key instead to maintain caching optimizations. A stable identifier for your end-users. Used to boost cache hit rates by better bucketing similar requests and to help OpenAI detect and prevent abuse. Learn more.

A list of Response items.

A list of items used to generate this response.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

Unix timestamp (in seconds) when the compacted conversation was created.

The unique identifier for the compacted response.

The object type. Always response.compaction.

The compacted list of output items.

Represents token usage details including input tokens, output tokens, a breakdown of output tokens, and the total tokens used.

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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4.1",
    "input": "Tell me a three sentence bedtime story about a unicorn."
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
8
9
10
import OpenAI from "openai";

const openai = new OpenAI();

const response = await openai.responses.create({
    model: "gpt-4.1",
    input: "Tell me a three sentence bedtime story about a unicorn."
});

console.log(response);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress

**Contents:**
- Streaming events
- response.created
- response.in_progress
- response.completed
- response.failed
- response.incomplete
- response.output_item.added
- response.output_item.done
- response.content_part.added
- response.content_part.done

When you create a Response with stream set to true, the server will emit server-sent events to the client as the Response is generated. This section contains the events that are emitted by the server.

Learn more about streaming responses.

An event that is emitted when a response is created.

The response that was created.

The sequence number for this event.

The type of the event. Always response.created.

Emitted when the response is in progress.

The response that is in progress.

The sequence number of this event.

The type of the event. Always response.in_progress.

Emitted when the model response is complete.

Properties of the completed response.

The sequence number for this event.

The type of the event. Always response.completed.

An event that is emitted when a response fails.

The response that failed.

The sequence number of this event.

The type of the event. Always response.failed.

An event that is emitted when a response finishes as incomplete.

The response that was incomplete.

The sequence number of this event.

The type of the event. Always response.incomplete.

Emitted when a new output item is added.

The output item that was added.

The index of the output item that was added.

The sequence number of this event.

The type of the event. Always response.output_item.added.

Emitted when an output item is marked done.

The output item that was marked done.

The index of the output item that was marked done.

The sequence number of this event.

The type of the event. Always response.output_item.done.

Emitted when a new content part is added.

The index of the content part that was added.

The ID of the output item that the content part was added to.

The index of the output item that the content part was added to.

The content part that was added.

The sequence number of this event.

The type of the event. Always response.content_part.added.

Emitted when a content part is done.

The index of the content part that is done.

The ID of the output item that the content part was added to.

The index of the output item that the content part was added to.

The content part that is done.

The sequence number of this event.

The type of the event. Always response.content_part.done.

Emitted when there is an additional text delta.

The index of the content part that the text delta was added to.

The text delta that was added.

The ID of the output item that the text delta was added to.

The log probabilities of the tokens in the delta.

The index of the output item that the text delta was added to.

The sequence number for this event.

The type of the event. Always response.output_text.delta.

Emitted when text content is finalized.

The index of the content part that the text content is finalized.

The ID of the output item that the text content is finalized.

The log probabilities of the tokens in the delta.

The index of the output item that the text content is finalized.

The sequence number for this event.

The text content that is finalized.

The type of the event. Always response.output_text.done.

Emitted when there is a partial refusal text.

The index of the content part that the refusal text is added to.

The refusal text that is added.

The ID of the output item that the refusal text is added to.

The index of the output item that the refusal text is added to.

The sequence number of this event.

The type of the event. Always response.refusal.delta.

Emitted when refusal text is finalized.

The index of the content part that the refusal text is finalized.

The ID of the output item that the refusal text is finalized.

The index of the output item that the refusal text is finalized.

The refusal text that is finalized.

The sequence number of this event.

The type of the event. Always response.refusal.done.

Emitted when there is a partial function-call arguments delta.

The function-call arguments delta that is added.

The ID of the output item that the function-call arguments delta is added to.

The index of the output item that the function-call arguments delta is added to.

The sequence number of this event.

The type of the event. Always response.function_call_arguments.delta.

Emitted when function-call arguments are finalized.

The function-call arguments.

The name of the function that was called.

The index of the output item.

The sequence number of this event.

Emitted when a file search call is initiated.

The ID of the output item that the file search call is initiated.

The index of the output item that the file search call is initiated.

The sequence number of this event.

The type of the event. Always response.file_search_call.in_progress.

Emitted when a file search is currently searching.

The ID of the output item that the file search call is initiated.

The index of the output item that the file search call is searching.

The sequence number of this event.

The type of the event. Always response.file_search_call.searching.

Emitted when a file search call is completed (results found).

The ID of the output item that the file search call is initiated.

The index of the output item that the file search call is initiated.

The sequence number of this event.

The type of the event. Always response.file_search_call.completed.

Emitted when a web search call is initiated.

Unique ID for the output item associated with the web search call.

The index of the output item that the web search call is associated with.

The sequence number of the web search call being processed.

The type of the event. Always response.web_search_call.in_progress.

Emitted when a web search call is executing.

Unique ID for the output item associated with the web search call.

The index of the output item that the web search call is associated with.

The sequence number of the web search call being processed.

The type of the event. Always response.web_search_call.searching.

Emitted when a web search call is completed.

Unique ID for the output item associated with the web search call.

The index of the output item that the web search call is associated with.

The sequence number of the web search call being processed.

The type of the event. Always response.web_search_call.completed.

Emitted when a new reasoning summary part is added.

The ID of the item this summary part is associated with.

The index of the output item this summary part is associated with.

The summary part that was added.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The type of the event. Always response.reasoning_summary_part.added.

Emitted when a reasoning summary part is completed.

The ID of the item this summary part is associated with.

The index of the output item this summary part is associated with.

The completed summary part.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The type of the event. Always response.reasoning_summary_part.done.

Emitted when a delta is added to a reasoning summary text.

The text delta that was added to the summary.

The ID of the item this summary text delta is associated with.

The index of the output item this summary text delta is associated with.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The type of the event. Always response.reasoning_summary_text.delta.

Emitted when a reasoning summary text is completed.

The ID of the item this summary text is associated with.

The index of the output item this summary text is associated with.

The sequence number of this event.

The index of the summary part within the reasoning summary.

The full text of the completed reasoning summary.

The type of the event. Always response.reasoning_summary_text.done.

Emitted when a delta is added to a reasoning text.

The index of the reasoning content part this delta is associated with.

The text delta that was added to the reasoning content.

The ID of the item this reasoning text delta is associated with.

The index of the output item this reasoning text delta is associated with.

The sequence number of this event.

The type of the event. Always response.reasoning_text.delta.

Emitted when a reasoning text is completed.

The index of the reasoning content part.

The ID of the item this reasoning text is associated with.

The index of the output item this reasoning text is associated with.

The sequence number of this event.

The full text of the completed reasoning content.

The type of the event. Always response.reasoning_text.done.

Emitted when an image generation tool call has completed and the final image is available.

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.image_generation_call.completed'.

Emitted when an image generation tool call is actively generating an image (intermediate state).

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

The sequence number of the image generation item being processed.

The type of the event. Always 'response.image_generation_call.generating'.

Emitted when an image generation tool call is in progress.

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

The sequence number of the image generation item being processed.

The type of the event. Always 'response.image_generation_call.in_progress'.

Emitted when a partial image is available during image generation streaming.

The unique identifier of the image generation item being processed.

The index of the output item in the response's output array.

Base64-encoded partial image data, suitable for rendering as an image.

0-based index for the partial image (backend is 1-based, but this is 0-based for the user).

The sequence number of the image generation item being processed.

The type of the event. Always 'response.image_generation_call.partial_image'.

Emitted when there is a delta (partial update) to the arguments of an MCP tool call.

A JSON string containing the partial update to the arguments for the MCP tool call.

The unique identifier of the MCP tool call item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.mcp_call_arguments.delta'.

Emitted when the arguments for an MCP tool call are finalized.

A JSON string containing the finalized arguments for the MCP tool call.

The unique identifier of the MCP tool call item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.mcp_call_arguments.done'.

Emitted when an MCP tool call has completed successfully.

The ID of the MCP tool call item that completed.

The index of the output item that completed.

The sequence number of this event.

The type of the event. Always 'response.mcp_call.completed'.

Emitted when an MCP tool call has failed.

The ID of the MCP tool call item that failed.

The index of the output item that failed.

The sequence number of this event.

The type of the event. Always 'response.mcp_call.failed'.

Emitted when an MCP tool call is in progress.

The unique identifier of the MCP tool call item being processed.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.mcp_call.in_progress'.

Emitted when the list of available MCP tools has been successfully retrieved.

The ID of the MCP tool call item that produced this output.

The index of the output item that was processed.

The sequence number of this event.

The type of the event. Always 'response.mcp_list_tools.completed'.

Emitted when the attempt to list available MCP tools has failed.

The ID of the MCP tool call item that failed.

The index of the output item that failed.

The sequence number of this event.

The type of the event. Always 'response.mcp_list_tools.failed'.

Emitted when the system is in the process of retrieving the list of available MCP tools.

The ID of the MCP tool call item that is being processed.

The index of the output item that is being processed.

The sequence number of this event.

The type of the event. Always 'response.mcp_list_tools.in_progress'.

Emitted when a code interpreter call is in progress.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code interpreter call is in progress.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call.in_progress.

Emitted when the code interpreter is actively interpreting the code snippet.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code interpreter is interpreting code.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call.interpreting.

Emitted when the code interpreter call is completed.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code interpreter call is completed.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call.completed.

Emitted when a partial code snippet is streamed by the code interpreter.

The partial code snippet being streamed by the code interpreter.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code is being streamed.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call_code.delta.

Emitted when the code snippet is finalized by the code interpreter.

The final code snippet output by the code interpreter.

The unique identifier of the code interpreter tool call item.

The index of the output item in the response for which the code is finalized.

The sequence number of this event, used to order streaming events.

The type of the event. Always response.code_interpreter_call_code.done.

Emitted when an annotation is added to output text content.

The annotation object being added. (See annotation schema for details.)

The index of the annotation within the content part.

The index of the content part within the output item.

The unique identifier of the item to which the annotation is being added.

The index of the output item in the response's output array.

The sequence number of this event.

The type of the event. Always 'response.output_text.annotation.added'.

Emitted when a response is queued and waiting to be processed.

The full response object that is queued.

The sequence number for this event.

The type of the event. Always 'response.queued'.

Event representing a delta (partial update) to the input of a custom tool call.

The incremental input data (delta) for the custom tool call.

Unique identifier for the API item associated with this event.

The index of the output this delta applies to.

The sequence number of this event.

The event type identifier.

Event indicating that input for a custom tool call is complete.

The complete input data for the custom tool call.

Unique identifier for the API item associated with this event.

The index of the output this event applies to.

The sequence number of this event.

The event type identifier.

Emitted when an error occurs.

The sequence number of this event.

The type of the event. Always error.

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
28
29
30
31
32
33
34
35
36
{
  "type": "response.created",
  "response": {
    "id": "resp_67ccfcdd16748190a91872c75d38539e09e4d4aac714747c",
    "object": "response",
    "created_at": 1741487325,
    "status": "in_progress",
    "error": null,
    "incomplete_details": null,
    "instructions": null,
    "max_output_tokens": null,
    "model": "gpt-4o-2024-08-06",
    "output": [],
    "parallel_tool_calls": true,
    "previous_response_id": null,
    "reasoning": {
      "effort": null,
      "summary": null
    },
    "store": true,
    "temperature": 1,
    "text": {
      "format": {
        "type": "text"
      }
    },
    "tool_choice": "auto",
    "tools": [],
    "top_p": 1,
    "truncation": "disabled",
    "usage": null,
    "user": null,
    "metadata": {}
  },
  "sequence_number": 1
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
28
29
30
31
32
33
34
35
36
{
  "type": "response.created",
  "response": {
    "id": "resp_67ccfcdd16748190a91872c75d38539e09e4d4aac714747c",
    "object": "response",
    "created_at": 1741487325,
    "status": "in_progress",
    "error": null,
    "incomplete_details": null,
    "instructions": null,
    "max_output_tokens": null,
    "model": "gpt-4o-2024-08-06",
    "output": [],
    "parallel_tool_calls": true,
    "previous_response_id": null,
    "reasoning": {
      "effort": null,
      "summary": null
    },
    "store": true,
    "temperature": 1,
    "text": {
      "format": {
        "type": "text"
      }
    },
    "tool_choice": "auto",
    "tools": [],
    "top_p": 1,
    "truncation": "disabled",
    "usage": null,
    "user": null,
    "metadata": {}
  },
  "sequence_number": 1
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
28
29
30
31
32
33
34
35
36
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
{
  "type": "response.in_progress",
  "response": {
    "id": "resp_67ccfcdd16748190a91872c75d38539e09e4d4aac714747c",
    "object": "response",
    "created_at": 1741487325,
    "status": "in_progress",
    "error": null,
    "incomplete_details": null,
    "instructions": null,
    "max_output_tokens": null,
    "model": "gpt-4o-2024-08-06",
    "output": [],
    "parallel_tool_calls": true,
    "previous_response_id": null,
    "reasoning": {
      "effort": null,
      "summary": null
    },
    "store": true,
    "temperature": 1,
    "text": {
      "format": {
        "type": "text"
      }
    },
    "tool_choice": "auto",
    "tools": [],
    "top_p": 1,
    "truncation": "disabled",
    "usage": null,
    "user": null,
    "metadata": {}
  },
  "sequence_number": 1
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/audit-logs

**Contents:**
- Audit logs
- List audit logs
    - Query parameters
    - Returns
- The audit log object

Logs of user actions and configuration changes within this organization. To log events, an Organization Owner must activate logging in the Data Controls Settings. Once activated, for security reasons, logging cannot be deactivated.

List user actions and configuration changes within this organization.

Return only events performed by users with these emails.

Return only events performed by these actors. Can be a user ID, a service account ID, or an api key tracking ID.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A cursor for use in pagination. before is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with obj_foo, your subsequent call can include before=obj_foo in order to fetch the previous page of the list.

Return only events whose effective_at (Unix seconds) is in this range.

Return only events with a type in one of these values. For example, project.created. For all options, see the documentation for the audit log object.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

Return only events for these projects.

Return only events performed on these targets. For example, a project ID updated.

A list of paginated Audit Log objects.

A log of a user action or configuration change within this organization.

The actor who performed the audit logged action.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The project and fine-tuned model checkpoint that the checkpoint permission was created for.

The details for events with this type.

The Unix timestamp (in seconds) of the event.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

This event has no additional fields beyond the standard audit log attributes.

The details for events with this type.

This event has no additional fields beyond the standard audit log attributes.

The details for events with this type.

The project that the action was scoped to. Absent for actions not scoped to projects. Note that any admin actions taken via Admin API keys are associated with the default project.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

The details for events with this type.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/audit_logs \
-H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
-H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/audit_logs \
-H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
-H "Content-Type: application/json"
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
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
{
    "object": "list",
    "data": [
        {
            "id": "audit_log-xxx_yyyymmdd",
            "type": "project.archived",
            "effective_at": 1722461446,
            "actor": {
                "type": "api_key",
                "api_key": {
                    "type": "user",
                    "user": {
                        "id": "user-xxx",
                        "email": "user@example.com"
                    }
                }
            },
            "project.archived": {
                "id": "proj_abc"
            },
        },
        {
            "id": "audit_log-yyy__20240101",
            "type": "api_key.updated",
            "effective_at": 1720804190,
            "actor": {
                "type": "session",
                "session": {
                    "user": {
                        "id": "user-xxx",
                        "email": "user@example.com"
                    },
                    "ip_address": "127.0.0.1",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "ja3": "a497151ce4338a12c4418c44d375173e",
                    "ja4": "q13d0313h3_55b375c5d22e_c7319ce65786",
                    "ip_address_details": {
                      "country": "US",
                      "city": "San Francisco",
                      "region": "California",
                      "region_code": "CA",
                      "asn": "1234",
                      "latitude": "37.77490",
                      "longitude": "-122.41940"
                    }
                }
            },
            "api_key.updated": {
                "id": "key_xxxx",
                "data": {
                    "scopes": ["resource_2.operation_2"]
                }
            },
        }
    ],
    "first_id": "audit_log-xxx__20240101",
    "last_id": "audit_log_yyy__20240101",
    "has_more": true
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
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
{
    "object": "list",
    "data": [
        {
            "id": "audit_log-xxx_yyyymmdd",
            "type": "project.archived",
            "effective_at": 1722461446,
            "actor": {
                "type": "api_key",
                "api_key": {
                    "type": "user",
                    "user": {
                        "id": "user-xxx",
                        "email": "user@example.com"
                    }
                }
            },
            "project.archived": {
                "id": "proj_abc"
            },
        },
        {
            "id": "audit_log-yyy__20240101",
            "type": "api_key.updated",
            "effective_at": 1720804190,
            "actor": {
                "type": "session",
                "session": {
                    "user": {
                        "id": "user-xxx",
                        "email": "user@example.com"
                    },
                    "ip_address": "127.0.0.1",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "ja3": "a497151ce4338a12c4418c44d375173e",
                    "ja4": "q13d0313h3_55b375c5d22e_c7319ce65786",
                    "ip_address_details": {
                      "country": "US",
                      "city": "San Francisco",
                      "region": "California",
                      "region_code": "CA",
                      "asn": "1234",
                      "latitude": "37.77490",
                      "longitude": "-122.41940"
                    }
                }
            },
            "api_key.updated": {
                "id": "key_xxxx",
                "data": {
                    "scopes": ["resource_2.operation_2"]
                }
            },
        }
    ],
    "first_id": "audit_log-xxx__20240101",
    "last_id": "audit_log_yyy__20240101",
    "has_more": true
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/conversations/item-object

**Contents:**
- Conversations
- Create a conversation
    - Request body
    - Returns
- Retrieve a conversation
    - Path parameters
    - Returns
- Update a conversation
    - Path parameters
    - Request body

Create and manage conversations to store and retrieve conversation state across Response API calls.

Create a conversation.

Initial items to include in the conversation context. You may add up to 20 items at a time.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns a Conversation object.

The ID of the conversation to retrieve.

Returns a Conversation object.

Update a conversation

The ID of the conversation to update.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

Returns the updated Conversation object.

Delete a conversation. Items in the conversation will not be deleted.

The ID of the conversation to delete.

List all items for a conversation with the given ID.

The ID of the conversation to list items for.

An item ID to list items after, used in pagination.

Specify additional output data to include in the model response. Currently supported values are:

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

The order to return the input items in. Default is desc.

Returns a list object containing Conversation items.

Create items in a conversation with the given ID.

The ID of the conversation to add the item to.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

The items to add to the conversation. You may add up to 20 items at a time.

Returns the list of added items.

Get a single item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to retrieve.

Additional fields to include in the response. See the include parameter for listing Conversation items above for more information.

Returns a Conversation Item.

Delete an item from a conversation with the given IDs.

The ID of the conversation that contains the item.

The ID of the item to delete.

Returns the updated Conversation object.

The time at which the conversation was created, measured in seconds since the Unix epoch.

The unique ID of the conversation.

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

The object type, which is always conversation.

A list of Conversation items.

A list of conversation items.

The ID of the first item in the list.

Whether there are more items available.

The ID of the last item in the list.

The type of object returned, must be list.

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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
curl https://api.openai.com/v1/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "metadata": {"topic": "demo"},
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello!"
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
import OpenAI from "openai";
const client = new OpenAI();

const conversation = await client.conversations.create({
  metadata: { topic: "demo" },
  items: [
    { type: "message", role: "user", content: "Hello!" }
  ],
});
console.log(conversation);
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/project-api-keys

**Contents:**
- Project API keys
- List project API keys
    - Path parameters
    - Query parameters
    - Returns
- Retrieve project API key
    - Path parameters
    - Returns
- Delete project API key
    - Path parameters

Manage API keys for a given project. Supports listing and deleting keys for users. This API does not allow issuing keys for users, as users need to authorize themselves to generate keys.

Returns a list of API keys in the project.

The ID of the project.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

A list of ProjectApiKey objects.

Retrieves an API key in the project.

The ID of the API key.

The ID of the project.

The ProjectApiKey object matching the specified ID.

Deletes an API key from the project.

The ID of the API key.

The ID of the project.

Confirmation of the key's deletion or an error if the key belonged to a service account

Represents an individual API key in a project.

The Unix timestamp (in seconds) of when the API key was created

The identifier, which can be referenced in API endpoints

The Unix timestamp (in seconds) of when the API key was last used.

The name of the API key

The object type, which is always organization.project.api_key

The redacted value of the API key

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
curl https://api.openai.com/v1/organization/projects/proj_abc/api_keys?after=key_abc&limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
```

Example 2 (bash):
```bash
1
2
3
curl https://api.openai.com/v1/organization/projects/proj_abc/api_keys?after=key_abc&limit=20 \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json"
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
{
    "object": "list",
    "data": [
        {
            "object": "organization.project.api_key",
            "redacted_value": "sk-abc...def",
            "name": "My API Key",
            "created_at": 1711471533,
            "last_used_at": 1711471534,
            "id": "key_abc",
            "owner": {
                "type": "user",
                "user": {
                    "object": "organization.project.user",
                    "id": "user_abc",
                    "name": "First Last",
                    "email": "user@example.com",
                    "role": "owner",
                    "added_at": 1711471533
                }
            }
        }
    ],
    "first_id": "key_abc",
    "last_id": "key_xyz",
    "has_more": false
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
21
22
23
24
25
26
27
{
    "object": "list",
    "data": [
        {
            "object": "organization.project.api_key",
            "redacted_value": "sk-abc...def",
            "name": "My API Key",
            "created_at": 1711471533,
            "last_used_at": 1711471534,
            "id": "key_abc",
            "owner": {
                "type": "user",
                "user": {
                    "object": "organization.project.user",
                    "id": "user_abc",
                    "name": "First Last",
                    "email": "user@example.com",
                    "role": "owner",
                    "added_at": 1711471533
                }
            }
        }
    ],
    "first_id": "key_abc",
    "last_id": "key_xyz",
    "has_more": false
}
```

---
