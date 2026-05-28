---
name: staging-token
description: Retrieve staging credentials/JWT token for the Aircall dashboard
---

# Staging Token

Retrieve staging JWT token by running the fish script.

Run the following command:

```bash
fish -c "source $HOME/dotfiles/.config/fish/functions/get_token.fish && get_token"
```

This will:

1. Authenticate against the staging identity server
2. Store the token in `DASHBOARD_JWT_TOKEN` environment variable
3. Copy the token to clipboard (if pbcopy is available)

The cookie key used to store this token is `ac-auth.id-token`.

Report back the result to the user.
