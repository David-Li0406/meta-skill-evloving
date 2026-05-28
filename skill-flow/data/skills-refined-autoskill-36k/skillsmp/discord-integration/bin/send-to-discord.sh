#!/bin/bash

# Send a message to the Discord channel via the Runner Agent
# Usage: send-to-discord.sh [options] "Message content"
# Options:
#   --title "Embed Title"
#   --color "hex_color" (e.g., "0x00FF00" or "green")
#   --description "Embed Description" (overrides content if used in embed)

CONTENT=""
TITLE=""
COLOR=""
DESCRIPTION=""
FILE_PATH=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --title) TITLE="$2"; shift ;;
        --color) COLOR="$2"; shift ;;
        --description) DESCRIPTION="$2"; shift ;;
        --file|-f) FILE_PATH="$2"; shift ;;
        *) CONTENT="$1" ;;
    esac
    shift
done

if [ -z "$CONTENT" ] && [ -z "$TITLE" ] && [ -z "$DESCRIPTION" ] && [ -z "$FILE_PATH" ]; then
    echo "Usage: $0 [--title \"Title\"] [--color \"Red\"] \"Message content\""
    exit 1
fi

# Use environment variables injected by the runner
if [ -z "$DISCODE_HTTP_PORT" ] || [ -z "$DISCODE_SESSION_ID" ]; then
    echo "Error: DISCODE_HTTP_PORT or DISCODE_SESSION_ID not set."
    exit 1
fi

# Map common color names to hex
case "${COLOR,,}" in
    red) COLOR_HEX="0xFF0000" ;;
    green) COLOR_HEX="0x00FF00" ;;
    blue) COLOR_HEX="0x0000FF" ;;
    yellow) COLOR_HEX="0xFFFF00" ;;
    orange) COLOR_HEX="0xFFA500" ;;
    purple) COLOR_HEX="0x800080" ;;
    white) COLOR_HEX="0xFFFFFF" ;;
    black) COLOR_HEX="0x000000" ;;
    *) COLOR_HEX="$COLOR" ;;
esac

# Construct JSON payload
# Note: In a real environment we should use jq, but we fallback to manual construction
# assuming simple inputs if jq isn't present, or use python/node if available.
# Here we'll try to use a simple node script if possible, otherwise crude bash string building.

PAYLOAD_SCRIPT="
const http = require('http');
const fs = require('fs');
const path = require('path');

const content = process.argv[2] ? process.argv[2].trim() : undefined;
const title = process.argv[3] ? process.argv[3].trim() : undefined;
const colorStr = process.argv[4] ? process.argv[4].trim() : undefined;
const description = process.argv[5] ? process.argv[5].trim() : undefined;
const filePath = process.argv[6] ? process.argv[6].trim() : undefined;

const data = {
    type: 'discord_action',
    action: 'send_message',
    sessionId: '$DISCODE_SESSION_ID',
    content: content,
    embeds: [],
    files: []
};


// Build embed if any embed fields are present
if (title || description || colorStr) {
    const embed = {};
    if (title) embed.title = title;
    if (description) embed.description = description;
    
    if (colorStr) {
        // Parse hex color if needed
        const hex = colorStr.replace(/^0x/, '').replace(/^#/, '');
        embed.color = parseInt(hex, 16) || 0;
    }
    
    // Valid embed must have at least one field
    if (Object.keys(embed).length > 0) {
        data.embeds.push(embed);
    }
}

// Process file if provided
if (filePath) {
    try {
        if (fs.existsSync(filePath)) {
            const fileBuffer = fs.readFileSync(filePath);
            const fileName = path.basename(filePath);
            data.files.push({
                name: fileName,
                content: fileBuffer.toString('base64')
            });
        } else {
            console.error('File not found:', filePath);
            process.exit(1);
        }
    } catch (err) {
        console.error('Error reading file:', err);
        process.exit(1);
    }
}

// Validation: Discord requires either content, embeds, or files
if (!data.content && data.embeds.length === 0 && data.files.length === 0) {
    console.error('Error: Cannot send an empty message. Provide content or embed details (--title, --description).');
    process.exit(1);
}

const postData = JSON.stringify(data);

const options = {
    hostname: '127.0.0.1',
    port: $DISCODE_HTTP_PORT,
    path: '/session-event',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
    }
};

const req = http.request(options, (res) => {
    // Consume response to free memory
    res.on('data', () => {});
    res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
            process.exit(0);
        } else {
            console.error('Request failed with status code:', res.statusCode);
            process.exit(1);
        }
    });
});

req.on('error', (e) => {
    console.error('Problem with request:', e.message);
    process.exit(1);
});

req.write(postData);
req.end();
"

# Try to run with node (most likely available in this env)
if command -v node &> /dev/null; then
    node -e "$PAYLOAD_SCRIPT" "$CONTENT" "$TITLE" "$COLOR_HEX" "$DESCRIPTION" "$FILE_PATH"
else
    # Fallback to curl with simplistic escaping if node is not present
    # This is risky for complex strings but a necessary fallback
    # TODO: Implement better fallback
    echo "Error: 'node' is required to run this script safely."
    exit 1
fi

