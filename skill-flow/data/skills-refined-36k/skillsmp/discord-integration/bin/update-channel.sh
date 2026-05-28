#!/bin/bash

# Update the Discord channel name and description via the Runner Agent

NAME="$1"
DESC="$2"

if [ -z "$NAME" ]; then
    echo "Usage: $0 <channel_name> [description]"
    exit 1
fi

# Use environment variables injected by the runner
if [ -z "$DISCODE_HTTP_PORT" ] || [ -z "$DISCODE_SESSION_ID" ]; then
    echo "Error: DISCODE_HTTP_PORT or DISCODE_SESSION_ID not set."
    exit 1
fi

if ! curl -f -s -X POST "http://127.0.0.1:$DISCODE_HTTP_PORT/session-event" \
     -H "Content-Type: application/json" \
     -d "{
           \"type\": \"discord_action\",
           \"action\": \"update_channel\",
           \"sessionId\": \"$DISCODE_SESSION_ID\",
           \"name\": $(jq -n --arg name "$NAME" '$name'),
           \"description\": $(jq -n --arg desc "$DESC" '$desc')
         }"; then
    echo "Error: Failed to update channel. Runner agent may be unreachable or disconnected."
    exit 1
fi

echo "Channel updated."
