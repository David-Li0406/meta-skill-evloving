---
name: thistle-tea-message-implementation
description: Use this skill when implementing Thistle Tea server and client messages following the architecture patterns.
---

# Body of the merged SKILL.md

Create/modify a module under `lib/game/network/message/` that:

- For server messages, use `ThistleTea.Game.Network.ServerMessage, :SMSG_FOO` and define a `defstruct` matching the fields needed to encode the packet. Implement `to_binary/1` using little-endian bit syntax patterns like `<<x::little-size(32)>>`.
- For client messages, use `ThistleTea.Game.Network.ClientMessage, :CMSG_FOO` and define a `defstruct` matching the fields decoded from the payload. Implement `from_binary/1` using little-endian bit syntax patterns and `handle/2` to update state and send any responses.

## Quick examples

### Server Message Example (`SMSG_PONG`)

```elixir
defmodule ThistleTea.Game.Network.Message.SmsgPong do
  use ThistleTea.Game.Network.ServerMessage, :SMSG_PONG

  defstruct [:sequence_id]

  @impl ServerMessage
  def to_binary(%__MODULE__{sequence_id: sequence_id}) do
    <<sequence_id::little-size(32)>>
  end
end
```

### Client Message Example (`CMSG_PING`)

```elixir
defmodule ThistleTea.Game.Network.Message.CmsgPing do
  use ThistleTea.Game.Network.ClientMessage, :CMSG_PING

  defstruct [:sequence_id, :latency]

  @impl ClientMessage
  def handle(%__MODULE__{sequence_id: sequence_id, latency: latency}, state) do
    Network.send_packet(%Message.SmsgPong{sequence_id: sequence_id})
    Map.put(state, :latency, latency)
  end

  @impl ClientMessage
  def from_binary(payload) do
    <<sequence_id::little-size(32), latency::little-size(32)>> = payload

    %__MODULE__{
      sequence_id: sequence_id,
      latency: latency
    }
  end
end
```

## How to find the packet spec

- Packet formats are cataloged in the `wow_messages` git submodule at `refs/wow_messages/`.
- Look up the `.wowm` spec here: `refs/wow_messages/wow_message_parser/wowm/*/${MESSAGE_NAME}.wowm`.
- Thistle Tea is a Vanilla (patch 1.12.1) server, so ignore future client versions.
- The `refs/mangos/` directory contains the Mangos C++ server codebase and can be used as a reference for expected `handle/2` behavior.

## Workflow

- For server messages, translate the `.wowm` fields into `defstruct` fields and an encoder in `to_binary/1`.
- For client messages, translate the `.wowm` fields into `defstruct` fields and a decoder in `from_binary/1`.
- Use pattern matching in the function head for type safety: `to_binary(%__MODULE__{} = msg)` for server messages and `handle(%__MODULE__{} = msg, state)` for client messages.
- Register the new handler in `lib/game/network/packet.ex` under the `@l` map for correct packet dispatch.