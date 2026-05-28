# GPTScript Template for Model Providers

Level 3 resource for new-provider skill.

## Basic Template

```gpt
Name: {Name} Model Provider
Description: {Name} model provider for Obot - provides access to {Name} LLM models
Credential: github.com/obot-platform/tools/model-provider-credential as credential

#!/usr/bin/env -S go run

package main

import (
    "fmt"
    "os"

    "github.com/obot-platform/tools/openai-model-provider/proxy"
)

func main() {
    apiKey := os.Getenv("OBOT_{NAME}_MODEL_PROVIDER_API_KEY")
    if apiKey == "" {
        fmt.Println("OBOT_{NAME}_MODEL_PROVIDER_API_KEY environment variable not set")
        os.Exit(1)
    }

    proxy.Run(
        "https://api.{provider}.com/v1",
        apiKey,
        "{provider}",
    )
}
```

## OAuth-Based Provider Template

```gpt
Name: {Name} Model Provider
Description: {Name} model provider for Obot with OAuth authentication
Credential: github.com/obot-platform/tools/oauth-credential as oauth with {PROVIDER} as env and "model:read model:write" as scope

#!/usr/bin/env -S go run

package main

import (
    "fmt"
    "os"

    "github.com/obot-platform/tools/openai-model-provider/proxy"
)

func main() {
    accessToken := os.Getenv("{PROVIDER}_OAUTH_TOKEN")
    if accessToken == "" {
        fmt.Println("OAuth token not available")
        os.Exit(1)
    }

    proxy.Run(
        "https://api.{provider}.com/v1",
        accessToken,
        "{provider}",
    )
}
```

## Provider-Specific Templates

### Anthropic

```gpt
Name: Anthropic Model Provider
Description: Anthropic Claude model provider for Obot
Credential: github.com/obot-platform/tools/model-provider-credential as credential

#!/usr/bin/env -S go run

package main

import (
    "fmt"
    "os"

    "github.com/obot-platform/tools/anthropic-model-provider/proxy"
)

func main() {
    apiKey := os.Getenv("OBOT_ANTHROPIC_MODEL_PROVIDER_API_KEY")
    if apiKey == "" {
        fmt.Println("OBOT_ANTHROPIC_MODEL_PROVIDER_API_KEY not set")
        os.Exit(1)
    }

    proxy.Run(
        "https://api.anthropic.com",
        apiKey,
        "anthropic",
    )
}
```

### Mistral (OpenAI-compatible)

```gpt
Name: Mistral Model Provider
Description: Mistral AI model provider for Obot
Credential: github.com/obot-platform/tools/model-provider-credential as credential

#!/usr/bin/env -S go run

package main

import (
    "fmt"
    "os"

    "github.com/obot-platform/tools/openai-model-provider/proxy"
)

func main() {
    apiKey := os.Getenv("OBOT_MISTRAL_MODEL_PROVIDER_API_KEY")
    if apiKey == "" {
        fmt.Println("OBOT_MISTRAL_MODEL_PROVIDER_API_KEY not set")
        os.Exit(1)
    }

    // Mistral uses OpenAI-compatible API
    proxy.Run(
        "https://api.mistral.ai/v1",
        apiKey,
        "mistral",
    )
}
```

## Environment Variables

| Provider | Variable Pattern |
| ---------- | ----------------- |
| OpenAI | `OBOT_OPENAI_MODEL_PROVIDER_API_KEY` |
| Anthropic | `OBOT_ANTHROPIC_MODEL_PROVIDER_API_KEY` |
| Mistral | `OBOT_MISTRAL_MODEL_PROVIDER_API_KEY` |
| Google | `OBOT_GOOGLE_MODEL_PROVIDER_API_KEY` |
| Azure | `OBOT_AZURE_MODEL_PROVIDER_*` |

## Required Files

```text
{name}-model-provider/
├── tool.gpt           # GPTScript definition
├── main.go            # Entry point (if complex)
├── go.mod             # Go module
├── go.sum             # Dependencies
└── proxy/             # Proxy implementation (if custom)
    └── proxy.go
```
