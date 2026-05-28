# go-dota2 Library Reference

DOTA 2 Game Coordinator client plugin for go-steam. Repository: `github.com/paralin/go-dota2`

## Setup and Initialization

```go
import (
    "github.com/paralin/go-steam"
    "github.com/paralin/go-dota2"
    "github.com/paralin/go-dota2/protocol"
    "github.com/paralin/go-dota2/cso"
    "github.com/paralin/go-dota2/events"
    "github.com/sirupsen/logrus"
)

// After steam client connected and logged in
client := steam.NewClient()
logger := logrus.New()

d := dota2.New(client, logger)
d.SetPlaying(true)   // Tell Steam we're playing Dota 2
d.SayHello()         // Initiate GC connection
```

## Client Type

```go
type Dota2 struct {
    client  *steam.Client
    cache   *socache.SOCache
    state   state.Dota2State
}
```

**Key Methods:**
- `New(client, logger) *Dota2` - Create client
- `SetPlaying(bool)` - Toggle Dota 2 playing status
- `SayHello(versions...)` - Initiate GC hello
- `GetCache() *SOCache` - Get shared object cache

## Connection Events

```go
// Listen for GC connection
client.On(func(e *events.GCConnectionStatusChanged) {
    if e.NewState == protocol.GCConnectionStatus_GCConnectionStatus_HAVE_SESSION {
        // GC session established
    }
})

// Welcome event with account data
client.On(func(e *events.ClientWelcomed) {
    // e.Msg contains welcome data
})
```

## Lobby Operations

```go
// Create lobby
details := &protocol.CMsgPracticeLobbySetDetails{
    GameName:   proto.String("My Lobby"),
    GameMode:   proto.Uint32(uint32(protocol.DOTA_GameMode_DOTA_GAMEMODE_AP)),
    ServerRegion: proto.Uint32(1), // US West
    // ... other settings
}
d.CreateLobby(details)

// Create with context (leaves current lobby first)
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
err := d.LeaveCreateLobby(ctx, details, true)

// Other lobby operations
d.LeaveLobby()
d.DestroyLobby(ctx)
d.KickLobbyMember(memberId, team)
d.ApplyTeamToLobby(teamID)
d.ClearTeamFromLobby()
d.RespondLobbyInvite(inviteId, accept)
```

## Party Operations

```go
d.LeaveParty()
d.RespondPartyInvite(partyId, accept)
d.SendPartyReadyCheck()
d.AckPartyReadyCheck(status)
```

## Chat Operations

```go
d.SendChannelMessage(channelID, "message")
```

## State Access

```go
state := d.GetState()
state.ConnectionStatus  // GCConnectionStatus
state.Lobby            // *CSODOTALobby
state.Party            // *CSODOTAParty
state.PartyInvite      // *CSODOTAPartyInvite
```

## SOCache (Shared Object Cache)

Real-time tracking of lobbies, parties, items. Subscribe to object type events:

```go
cache := d.GetCache()

// Subscribe to lobby events
eventCh, cancel, err := cache.SubscribeType(cso.Lobby)
if err != nil {
    return err
}
defer cancel()

for event := range eventCh {
    lobby := event.Object.(*protocol.CSODOTALobby)
    switch event.EventType {
    case socache.EventTypeCreate:
        // Lobby created
    case socache.EventTypeUpdate:
        // Lobby updated
    case socache.EventTypeDestroy:
        // Lobby destroyed
    }
}
```

**CSO Types (cso package):**
- `cso.Lobby` - Lobby state
- `cso.Party` - Party state
- `cso.PartyInvite` - Party invitations
- `cso.LobbyInvite` - Lobby invitations
- `cso.EconItem` - Inventory items

## Events Reference

**Connection:**
- `GCConnectionStatusChanged` - GC connection state change
- `ClientWelcomed` - GC welcome with account data
- `UnhandledGCPacket` - Unknown message received

**Chat:**
- `ChatMessage` - Chat message received
- `JoinedChatChannel` - Joined channel

**Invitations:**
- `InvitationCreated` - New invite received

**Ready Check:**
- `PartyReadyCheckRequest` - Ready check initiated

## Generated API Methods

The library auto-generates 200+ methods in `client_generated.go`. Common patterns:

**Fire-and-forget (no response):**
```go
d.SomeAction(param1, param2)
```

**Request/Response (with context):**
```go
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
response, err := d.SomeQuery(ctx, param1)
```

### Lobby Methods
- `CreateLobby`, `LeaveLobby`, `DestroyLobby`
- `SetLobbyTeamSlot`, `KickLobbyMember`, `AbandonLobby`
- `ApplyTeamToLobby`, `ClearTeamFromLobby`
- `RespondLobbyInvite`, `InviteToLobby`

### Party Methods
- `LeaveParty`, `RespondPartyInvite`
- `SendPartyReadyCheck`, `AckPartyReadyCheck`
- `SetPartyLeader`, `SetPartyOpen`, `CancelPartyInvites`

### Match/Profile Methods
- `GetMatchDetails`, `GetPlayerMatches`
- `GetProfile`, `GetBattleReportInfo`

### Spectator Methods
- `FindTopSourceTVGames`, `WatchGame`, `CancelWatchGame`

### Guild Methods
- `CreateGuild`, `EditGuildDetails`
- `InviteToGuild`, `RespondGuildInvite`

### Battle Pass/Events
- `ClaimEventAction`, `GetEventPoints`
- `ClaimBingoRow`, `GetBingoUserData`

### Fantasy/Tournaments
- `SubmitFantasyTeamSelection`, `GetFantasyPlayerStats`
- `JoinWeekendTourney`

## Protocol Types

Key protobuf types in `protocol` package:

```go
// Lobby
*protocol.CSODOTALobby
*protocol.CMsgPracticeLobbySetDetails

// Party
*protocol.CSODOTAParty
*protocol.CSODOTAPartyInvite

// Connection
protocol.GCConnectionStatus_GCConnectionStatus_HAVE_SESSION
*protocol.CMsgConnectionStatus

// Game Modes
protocol.DOTA_GameMode_DOTA_GAMEMODE_AP  // All Pick
protocol.DOTA_GameMode_DOTA_GAMEMODE_CM  // Captains Mode
// ... etc
```

## MakeRequest Pattern

For custom request/response calls:

```go
response := &protocol.CMsgSomeResponse{}
err := d.MakeRequest(
    ctx,
    uint32(protocol.EDOTAGCMsg_k_EMsgSomeRequest),
    &protocol.CMsgSomeRequest{/* ... */},
    uint32(protocol.EDOTAGCMsg_k_EMsgSomeResponse),
    response,
)
```
