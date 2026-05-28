# go-steam Library Reference

Go library implementing Valve's Steam network protocol. Enables Steam bot automation without running the official client. Repository: `github.com/paralin/go-steam`

## Core Architecture

```go
import "github.com/paralin/go-steam"

client := steam.NewClient()
go func() {
    for event := range client.Events() {
        switch e := event.(type) {
        case *steam.LoggedOnEvent:
            // Handle login success
        case *steam.DisconnectedEvent:
            // Handle disconnect
        case error:
            // Handle error
        }
    }
}()
client.Connect()  // Random server
// OR: client.ConnectTo(&netutil.PortAddr{Host: "ip", Port: 27015})
```

## Client Type

```go
type Client struct {
    Auth          *Auth           // Authentication module
    Social        *Social         // Friends/groups/chat
    Web           *Web            // Web session
    Notifications *Notifications  // User notifications
    Trading       *Trading        // Trade requests
    GC            *GameCoordinator// Game coordinator bridge
}
```

**Key Methods:**
- `NewClient() *Client` - Create client
- `Connect() error` - Connect to random Steam server
- `ConnectTo(addr *PortAddr) error` - Connect to specific server
- `Disconnect()` - Graceful disconnect
- `Events() <-chan interface{}` - Event channel
- `RegisterPacketHandler(handler PacketHandler)` - Custom handler

## Authentication

```go
// Username + Password
client.Auth.LogOn(&steam.LogOnDetails{
    Username: "user",
    Password: "pass",
})

// With 2FA
client.Auth.LogOn(&steam.LogOnDetails{
    Username: "user",
    Password: "pass",
    AuthCode: "123456",  // From authenticator
})

// With Login Key (persistent, no password)
client.Auth.LogOn(&steam.LogOnDetails{
    Username: "user",
    LoginKey: "saved_key",
})

// With Machine Auth (device whitelist)
client.Auth.LogOn(&steam.LogOnDetails{
    Username:      "user",
    Password:      "pass",
    SentryFileHash: machineAuthHash,  // SHA1 of sentry file
})
```

## Social Module

```go
s := client.Social

// Friends
s.AddFriend(steamId)           // Send/accept friend request
s.RemoveFriend(steamId)        // Remove friend
s.IgnoreFriend(steamId)        // Block user
s.RequestFriendInfo([]SteamId) // Get persona details
s.RequestProfileInfo(steamId)  // Get profile

// Messaging
s.SendMessage(steamId, steam.EChatEntryType_ChatMsg, "Hello")

// Chat Rooms
s.JoinChat(chatId)
s.LeaveChat(chatId)
s.KickChatMember(chatId, userId)
s.BanChatMember(chatId, userId)
s.UnbanChatMember(chatId, userId)

// Cached data
s.Friends  // *socialcache.FriendsList
s.Groups   // *socialcache.GroupsList
s.Chats    // *socialcache.ChatsList
```

## Trading Module

```go
t := client.Trading

t.RequestTrade(otherSteamId)              // Initiate trade
t.RespondRequest(requestId, true/false)   // Accept/decline
t.CancelRequest(otherSteamId)             // Cancel request
```

## Web Session

```go
// After WebSessionIdEvent
client.Web.LogOn()

// After WebLoggedOnEvent - cookies available:
client.Web.SessionId       // Web session cookie
client.Web.SteamLogin      // HTTP auth cookie
client.Web.SteamLoginSecure // HTTPS auth cookie
```

## Game Coordinator

```go
gc := client.GC

gc.SetGamesPlayed(570)  // 570 = Dota 2 AppID
gc.RegisterPacketHandler(handler)
gc.Write(protoMessage)
```

## SteamID Utilities

```go
import "github.com/paralin/go-steam/steamid"

// Parse various formats
id := steamid.NewId("[U:1:12345]")      // Steam3
id := steamid.NewId("STEAM_0:1:6172")   // Steam2
id := steamid.NewId("76561198012345")   // Decimal

// Convert
id.ToUint64()    // uint64
id.ToString()    // Decimal string
id.ToSteam2()    // STEAM_X:Y:Z
id.ToSteam3()    // [U:1:...]

// Clan/Chat conversion
id.ClanToChat()
id.ChatToClan()
```

## Events Reference

**Authentication:**
- `LoggedOnEvent` - Login success (contains SteamId, Result)
- `LogOnFailedEvent` - Login failed (contains Result code)
- `LoginKeyEvent` - New persistent login key
- `LoggedOffEvent` - Disconnected by server
- `MachineAuthUpdateEvent` - Machine auth hash needed
- `AccountInfoEvent` - Account details received

**Social:**
- `FriendsListEvent` - Friends list updated
- `FriendStateEvent` - Friend status changed
- `FriendAddedEvent` - Friend added
- `PersonaStateEvent` - Friend persona changed
- `ChatMsgEvent` - Message received
- `ChatEnterEvent` - Joined chat
- `ChatInviteEvent` - Chat invite received
- `ProfileInfoEvent` - Profile info received

**Trading:**
- `TradeProposedEvent` - Trade proposal received
- `TradeResultEvent` - Trade result
- `TradeSessionStartEvent` - Trade session started

**Web:**
- `WebSessionIdEvent` - Web session ready (call Web.LogOn())
- `WebLoggedOnEvent` - Web login success
- `WebLogOnErrorEvent` - Web login failed

**Connection:**
- `ConnectedEvent` - Connected to Steam
- `DisconnectedEvent` - Disconnected
- `FatalErrorEvent` - Fatal error
- `ClientCMListEvent` - Server list (cache for reconnection)

## TF2 Module

```go
import "github.com/paralin/go-steam/tf2"

tf2Client := tf2.New(client)
tf2Client.SetPlaying(true)

// Wait for GCReadyEvent, then:
tf2Client.SetItemPosition(assetId, position)
tf2Client.DeleteItem(assetId)
tf2Client.NameItem(assetId, "New Name")
tf2Client.CraftItems(recipe, item1, item2, ...)
```

## Inventory Access

```go
import "github.com/paralin/go-steam/economy/inventory"

// Fetch inventory (requires web session)
inv, err := inventory.GetFullInventory(apiGetFunc, steamId, appId, contextId)

inv.Items        // map[uint64]Item
inv.Descriptions // map[string]ItemDescription
inv.Items.Get(assetId)
inv.Descriptions.Get(classId, instanceId)
```
