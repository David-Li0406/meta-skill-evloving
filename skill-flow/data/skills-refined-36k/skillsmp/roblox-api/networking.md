# Networking Classes

## Contents
- [RemoteEvent](#remoteevent)
- [RemoteFunction](#remotefunction)
- [BindableEvent](#bindableevent)
- [BindableFunction](#bindablefunction)
- [UnreliableRemoteEvent](#unreliableremoteevent)

---

## RemoteEvent

An object which facilitates asynchronous, one-way communication across the
client-server boundary. Scripts firing a `Class.RemoteEvent` do not yield.

**Methods:**
- `RemoteEvent:FireAllClients` - Fires the `Class.RemoteEvent.OnClientEvent|OnClientEvent` event for each
- `RemoteEvent:FireClient` - Fires the `Class.RemoteEvent.OnClientEvent|OnClientEvent` event for a
- `RemoteEvent:FireServer` - Fires the `Class.RemoteEvent.OnServerEvent|OnServerEvent` event on the

**Events:**
- `RemoteEvent.OnClientEvent` - Fires from a `Class.LocalScript` when either
- `RemoteEvent.OnServerEvent` - Fires from a `Class.Script` when

---

## RemoteFunction

An object which facilitates synchronous, two-way communication across the
client-server boundary. Scripts invoking a `Class.RemoteFunction` yield until
they receive a response from the recipient.

**Methods:**
- `RemoteFunction:InvokeClient` - Invokes the `Class.RemoteFunction` which in turn calls the
- `RemoteFunction:InvokeServer` - Invokes the `Class.RemoteFunction` which in turn calls the

---

## BindableEvent

An object which enables custom events through asynchronous one-way
communication between scripts on the same side of the client-server boundary.
Scripts firing a `Class.BindableEvent` do not yield.

**Methods:**
- `BindableEvent:Fire` - Fires the `Class.BindableEvent` which in turn fires the

**Events:**
- `BindableEvent.Event` - Fires when any script calls the `Class.BindableEvent:Fire()|Fire()` method

---

## BindableFunction

An object which allows for synchronous two-way communication between scripts
on the same side of the client-server boundary. Scripts invoking a
`Class.BindableFunction` yield until the corresponding callback is found.

**Methods:**
- `BindableFunction:Invoke` - Invokes the `Class.BindableFunction` which in turn calls the

---

## UnreliableRemoteEvent

An object which facilitates asynchronous, unordered and unreliable, one-way
communication across the client-server boundary. Scripts firing a
`Class.UnreliableRemoteEvent` do not yield.

**Methods:**
- `UnreliableRemoteEvent:FireAllClients` - Fires the `Class.UnreliableRemoteEvent.OnClientEvent|OnClientEvent` event
- `UnreliableRemoteEvent:FireClient` - Fires the `Class.UnreliableRemoteEvent.OnClientEvent|OnClientEvent` event
- `UnreliableRemoteEvent:FireServer` - Fires the `Class.UnreliableRemoteEvent.OnServerEvent|OnServerEvent` event

**Events:**
- `UnreliableRemoteEvent.OnClientEvent` - Fires from a `Class.LocalScript` when either
- `UnreliableRemoteEvent.OnServerEvent` - Fires from a `Class.Script` when

---

