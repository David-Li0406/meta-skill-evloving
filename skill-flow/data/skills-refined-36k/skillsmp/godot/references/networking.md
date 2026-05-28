# Godot - Networking

**Pages:** 7

---

## Making HTTP requests — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/networking/http_request_class.html

**Contents:**
- Making HTTP requests
- Why use HTTP?
- HTTP requests in Godot
- Preparing the scene
- Scripting the request
- Sending data to the server
- Setting custom HTTP headers
- User-contributed notes

HTTP requests are useful to communicate with web servers and other non-Godot programs.

Compared to Godot's other networking features (like High-level multiplayer), HTTP requests have more overhead and take more time to get going, so they aren't suited for real-time communication, and aren't great to send lots of small updates as is common for multiplayer gameplay.

HTTP, however, offers interoperability with external web resources and is great at sending and receiving large amounts of data, for example to transfer files like game assets. These assets can then be loaded using runtime file loading and saving.

So HTTP may be useful for your game's login system, lobby browser, to retrieve some information from the web or to download game assets.

The HTTPRequest node is the easiest way to make HTTP requests in Godot. It is backed by the more low-level HTTPClient, for which a tutorial is available here.

For this example, we will make an HTTP request to GitHub to retrieve the name of the latest Godot release.

When exporting to Android, make sure to enable the Internet permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by the Android OS.

Create a new empty scene, add a root Node and add a script to it. Then add an HTTPRequest node as a child.

When the project is started (so in _ready()), we're going to send an HTTP request to Github using our HTTPRequest node, and once the request completes, we're going to parse the returned JSON data, look for the name field and print that to console.

Save the script and the scene, and run the project. The name of the most recent Godot release on Github should be printed to the output log. For more information on parsing JSON, see the class references for JSON.

Note that you may want to check whether the result equals RESULT_SUCCESS and whether a JSON parsing error occurred, see the JSON class reference and HTTPRequest for more.

You have to wait for a request to finish before sending another one. Making multiple request at once requires you to have one node per request. A common strategy is to create and delete HTTPRequest nodes at runtime as necessary.

Until now, we have limited ourselves to requesting data from a server. But what if you need to send data to the server? Here is a common way of doing it:

Of course, you can also set custom HTTP headers. These are given as a string array, with each string containing a header in the format "header: value". For example, to set a custom user agent (the HTTP User-Agent header) you could use the following:

Be aware that someone might analyse and decompile your released application and thus may gain access to any embedded authorization information like tokens, usernames or passwords. That means it is usually not a good idea to embed things such as database access credentials inside your game. Avoid providing information useful to an attacker whenever possible.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node

func _ready():
    $HTTPRequest.request_completed.connect(_on_request_completed)
    $HTTPRequest.request("https://api.github.com/repos/godotengine/godot/releases/latest")

func _on_request_completed(result, response_code, headers, body):
    var json = JSON.parse_string(body.get_string_from_utf8())
    print(json["name"])
```

Example 2 (swift):
```swift
using Godot;
using System.Text;

public partial class MyNode : Node
{
    public override void _Ready()
    {
        HttpRequest httpRequest = GetNode<HttpRequest>("HTTPRequest");
        httpRequest.RequestCompleted += OnRequestCompleted;
        httpRequest.Request("https://api.github.com/repos/godotengine/godot/releases/latest");
    }

    private void OnRequestCompleted(long result, long responseCode, string[] headers, byte[] body)
    {
        Godot.Collections.Dictionary json = Json.ParseString(Encoding.UTF8.GetString(body)).AsGodotDictionary();
        GD.Print(json["name"]);
    }
}
```

Example 3 (gdscript):
```gdscript
var json = JSON.stringify(data_to_send)
var headers = ["Content-Type: application/json"]
$HTTPRequest.request(url, headers, HTTPClient.METHOD_POST, json)
```

Example 4 (csharp):
```csharp
string json = Json.Stringify(dataToSend);
string[] headers = ["Content-Type: application/json"];
HttpRequest httpRequest = GetNode<HttpRequest>("HTTPRequest");
httpRequest.Request(url, headers, HttpClient.Method.Post, json);
```

---

## High-level multiplayer — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html

**Contents:**
- High-level multiplayer
- High-level vs low-level API
- Mid-level abstraction
- Hosting considerations
- Initializing the network
- Managing connections
- Remote procedure calls
- Channels
- Example lobby implementation
- Exporting for dedicated servers

The following explains the differences of high- and low-level networking in Godot as well as some fundamentals. If you want to jump in head-first and add networking to your first nodes, skip to Initializing the network below. But make sure to read the rest later on!

Godot always supported standard low-level networking via UDP, TCP and some higher-level protocols such as HTTP and SSL. These protocols are flexible and can be used for almost anything. However, using them to synchronize game state manually can be a large amount of work. Sometimes that work can't be avoided or is worth it, for example when working with a custom server implementation on the backend. But in most cases, it's worthwhile to consider Godot's high-level networking API, which sacrifices some of the fine-grained control of low-level networking for greater ease of use.

This is due to the inherent limitations of the low-level protocols:

TCP ensures packets will always arrive reliably and in order, but latency is generally higher due to error correction. It's also quite a complex protocol because it understands what a "connection" is, and optimizes for goals that often don't suit applications like multiplayer games. Packets are buffered to be sent in larger batches, trading less per-packet overhead for higher latency. This can be useful for things like HTTP, but generally not for games. Some of this can be configured and disabled (e.g. by disabling "Nagle's algorithm" for the TCP connection).

UDP is a simpler protocol, which only sends packets (and has no concept of a "connection"). No error correction makes it pretty quick (low latency), but packets may be lost along the way or received in the wrong order. Added to that, the MTU (maximum packet size) for UDP is generally low (only a few hundred bytes), so transmitting larger packets means splitting them, reorganizing them and retrying if a part fails.

In general, TCP can be thought of as reliable, ordered, and slow; UDP as unreliable, unordered and fast. Because of the large difference in performance, it often makes sense to re-build the parts of TCP wanted for games (optional reliability and packet order), while avoiding the unwanted parts (congestion/traffic control features, Nagle's algorithm, etc). Due to this, most game engines come with such an implementation, and Godot is no exception.

In summary, you can use the low-level networking API for maximum control and implement everything on top of bare network protocols or use the high-level API based on SceneTree that does most of the heavy lifting behind the scenes in a generally optimized way.

Most of Godot's supported platforms offer all or most of the mentioned high- and low-level networking features. As networking is always largely hardware and operating system dependent, however, some features may change or not be available on some target platforms. Most notably, the HTML5 platform currently offers WebSockets and WebRTC support but lacks some of the higher-level features, as well as raw access to low-level protocols like TCP and UDP.

More about TCP/IP, UDP, and networking: https://gafferongames.com/post/udp_vs_tcp/

Gaffer On Games has a lot of useful articles about networking in Games (here), including the comprehensive introduction to networking models in games.

Adding networking to your game comes with some responsibility. It can make your application vulnerable if done wrong and may lead to cheats or exploits. It may even allow an attacker to compromise the machines your application runs on and use your servers to send spam, attack others or steal your users' data if they play your game.

This is always the case when networking is involved and has nothing to do with Godot. You can of course experiment, but when you release a networked application, always take care of any possible security concerns.

Before going into how we would like to synchronize a game across the network, it can be helpful to understand how the base network API for synchronization works.

Godot uses a mid-level object MultiplayerPeer. This object is not meant to be created directly, but is designed so that several C++ implementations can provide it.

This object extends from PacketPeer, so it inherits all the useful methods for serializing, sending and receiving data. On top of that, it adds methods to set a peer, transfer mode, etc. It also includes signals that will let you know when peers connect or disconnect.

This class interface can abstract most types of network layers, topologies and libraries. By default, Godot provides an implementation based on ENet (ENetMultiplayerPeer), one based on WebRTC (WebRTCMultiplayerPeer), and one based on WebSocket (WebSocketPeer), but this could be used to implement mobile APIs (for ad hoc WiFi, Bluetooth) or custom device/console-specific networking APIs.

For most common cases, using this object directly is discouraged, as Godot provides even higher level networking facilities. This object is still made available in case a game has specific needs for a lower-level API.

When hosting a server, clients on your LAN can connect using the internal IP address which is usually of the form 192.168.*.*. This internal IP address is not reachable by non-LAN/Internet clients.

On Windows, you can find your internal IP address by opening a command prompt and entering ipconfig. On macOS, open a Terminal and enter ifconfig. On Linux, open a terminal and enter ip addr.

If you're hosting a server on your own machine and want non-LAN clients to connect to it, you'll probably have to forward the server port on your router. This is required to make your server reachable from the Internet since most residential connections use a NAT. Godot's high-level multiplayer API only uses UDP, so you must forward the port in UDP, not just TCP.

After forwarding a UDP port and making sure your server uses that port, you can use this website to find your public IP address. Then give this public IP address to any Internet clients that wish to connect to your server.

Godot's high-level multiplayer API uses a modified version of ENet which allows for full IPv6 support.

High-level networking in Godot is managed by the SceneTree.

Each node has a multiplayer property, which is a reference to the MultiplayerAPI instance configured for it by the scene tree. Initially, every node is configured with the same default MultiplayerAPI object.

It is possible to create a new MultiplayerAPI object and assign it to a NodePath in the scene tree, which will override multiplayer for the node at that path and all of its descendants. This allows sibling nodes to be configured with different peers, which makes it possible to run a server and a client simultaneously in one instance of Godot.

To initialize networking, a MultiplayerPeer object must be created, initialized as a server or client, and passed to the MultiplayerAPI.

To terminate networking:

When exporting to Android, make sure to enable the INTERNET permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android.

Every peer is assigned a unique ID. The server's ID is always 1, and clients are assigned a random positive integer.

Responding to connections or disconnections is possible by connecting to MultiplayerAPI's signals:

peer_connected(id: int) This signal is emitted with the newly connected peer's ID on each other peer, and on the new peer multiple times, once with each other peer's ID.

peer_disconnected(id: int) This signal is emitted on every remaining peer when one disconnects.

The rest are only emitted on clients:

connected_to_server()

server_disconnected()

To get the unique ID of the associated peer:

To check whether the peer is server or client:

Remote procedure calls, or RPCs, are functions that can be called on other peers. To create one, use the @rpc annotation before a function definition. To call an RPC, use Callable's method rpc() to call in every peer, or rpc_id() to call in a specific peer.

RPCs will not serialize objects or callables.

For a remote call to be successful, the sending and receiving node need to have the same NodePath, which means they must have the same name. When using add_child() for nodes which are expected to use RPCs, set the argument force_readable_name to true.

If a function is annotated with @rpc on the client script (resp. server script), then this function must also be declared on the server script (resp. client script). Both RPCs must have the same signature which is evaluated with a checksum of all RPCs. All RPCs in a script are checked at once, and all RPCs must be declared on both the client scripts and the server scripts, even functions that are currently not in use.

The signature of the RPC includes the @rpc() declaration, the function, return type, and the NodePath. If an RPC resides in a script attached to /root/Main/Node1, then it must reside in precisely the same path and node on both the client script and the server script. Function arguments are not checked for matching between the server and client code (example: func sendstuff(): and func sendstuff(arg1, arg2): will pass signature matching).

If these conditions are not met (if all RPCs do not pass signature matching), the script may print an error or cause unwanted behavior. The error message may be unrelated to the RPC function you are currently building and testing.

See further explanation and troubleshooting on this post.

The annotation can take a number of arguments, which have default values. @rpc is equivalent to:

The parameters and their functions are as follows:

"authority": Only the multiplayer authority can call remotely. The authority is the server by default, but can be changed per-node using Node.set_multiplayer_authority.

"any_peer": Clients are allowed to call remotely. Useful for transferring user input.

"call_remote": The function will not be called on the local peer.

"call_local": The function can be called on the local peer. Useful when the server is also a player.

"unreliable" Packets are not acknowledged, can be lost, and can arrive at any order.

"unreliable_ordered" Packets are received in the order they were sent in. This is achieved by ignoring packets that arrive later if another that was sent after them has already been received. Can cause packet loss if used incorrectly.

"reliable" Resend attempts are sent until packets are acknowledged, and their order is preserved. Has a significant performance penalty.

transfer_channel is the channel index.

The first 3 can be passed in any order, but transfer_channel must always be last.

The function multiplayer.get_remote_sender_id() can be used to get the unique id of an rpc sender, when used within the function called by rpc.

Modern networking protocols support channels, which are separate connections within the connection. This allows for multiple streams of packets that do not interfere with each other.

For example, game chat related messages and some of the core gameplay messages should all be sent reliably, but a gameplay message should not wait for a chat message to be acknowledged. This can be achieved by using different channels.

Channels are also useful when used with the unreliable ordered transfer mode. Sending packets of variable size with this transfer mode can cause packet loss, since packets which are slower to arrive are ignored. Separating them into multiple streams of homogeneous packets by using channels allows ordered transfer with little packet loss, and without the latency penalty caused by reliable mode.

The default channel with index 0 is actually three different channels - one for each transfer mode.

This is an example lobby that can handle peers joining and leaving, notify UI scenes through signals, and start the game after all clients have loaded the game scene.

The game scene's root node should be named Game. In the script attached to it:

Once you've made a multiplayer game, you may want to export it to run it on a dedicated server with no GPU available. See Exporting for dedicated servers for more information.

The code samples on this page aren't designed to run on a dedicated server. You'll have to modify them so the server isn't considered to be a player. You'll also have to modify the game starting mechanism so that the first player who joins can start the game.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (markdown):
```markdown
# By default, these expressions are interchangeable.
multiplayer # Get the MultiplayerAPI object configured for this node.
get_tree().get_multiplayer() # Get the default MultiplayerAPI object.
```

Example 2 (unknown):
```unknown
// By default, these expressions are interchangeable.
Multiplayer; // Get the MultiplayerAPI object configured for this node.
GetTree().GetMultiplayer(); // Get the default MultiplayerAPI object.
```

Example 3 (gdscript):
```gdscript
# Create client.
var peer = ENetMultiplayerPeer.new()
peer.create_client(IP_ADDRESS, PORT)
multiplayer.multiplayer_peer = peer

# Create server.
var peer = ENetMultiplayerPeer.new()
peer.create_server(PORT, MAX_CLIENTS)
multiplayer.multiplayer_peer = peer
```

Example 4 (gdscript):
```gdscript
// Create client.
var peer = new ENetMultiplayerPeer();
peer.CreateClient(IPAddress, Port);
Multiplayer.MultiplayerPeer = peer;

// Create server.
var peer = new ENetMultiplayerPeer();
peer.CreateServer(Port, MaxClients);
Multiplayer.MultiplayerPeer = peer;
```

---

## Networking — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/networking/index.html

**Contents:**
- Networking

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## TLS/SSL certificates — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/networking/ssl_certificates.html

**Contents:**
- TLS/SSL certificates
- Introduction
- Obtain a certificate from a certificate authority
- Generate a self-signed certificate
- User-contributed notes

It is often desired to use TLS connections (also known as SSL connections) for communications to avoid "man in the middle" attacks. Godot has a connection wrapper, StreamPeerTLS, which can take a regular connection and add security around it. The HTTPClient and HTTPRequest classes also support HTTPS using this same wrapper.

Godot will try to use the TLS certificate bundle provided by the operating system, but also includes the TLS certificate bundle from Mozilla as a fallback.

You can alternatively force your own certificate bundle in the Project Settings:

Setting the TLS certificate bundle override project setting

When set, this file overrides the operating system provided bundle by default. This file should contain any number of public certificates in PEM format.

There are two ways to obtain certificates:

The main approach to getting a certificate is to use a certificate authority (CA) such as Let's Encrypt. This is a more cumbersome process than a self-signed certificate, but it's more "official" and ensures your identity is clearly represented. The resulting certificate is also trusted by applications such as web browsers, unlike a self-signed certificate which requires additional configuration on the client side before it's considered trusted.

These certificates do not require any configuration on the client to work, since Godot already bundles the Mozilla certificate bundle in the editor and exported projects.

For most use cases, it's recommended to go through certificate authority as the process is free with certificate authorities such as Let's Encrypt. However, if using a certificate authority is not an option, then you can generate a self-signed certificate and tell the client to consider your self-signed certificate as trusted.

To create a self-signed certificate, generate a private and public key pair and add the public key (in PEM format) to the CRT file specified in the Project Settings.

The private key should only go to your server. The client must not have access to it: otherwise, the security of the certificate will be compromised.

When specifying a self-signed certificate as TLS bundle in the project settings, normal domain name validation is enforced via the certificate CN and alternative names. See TLSOptions to customize domain name validation.

For development purposes Godot can generate self-signed certificates via Crypto.generate_self_signed_certificate.

Alternatively, OpenSSL has some documentation about generating keys and certificates.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

---

## Using WebSockets — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/networking/websocket.html

**Contents:**
- Using WebSockets
- HTML5 and WebSocket
- Using WebSocket in Godot
  - Minimal client example
  - Minimal server example
  - Advanced chat demo
- User-contributed notes

The WebSocket protocol was standardized in 2011 with the original goal of allowing browsers to create stable and bidirectional connections with a server. Before that, browsers used to only support HTTP requests, which aren't well-suited for bidirectional communication.

The protocol is message-based and a very powerful tool to send push notifications to browsers. It has been used to implement chats, turn-based games, and more. It still uses a TCP connection, which is good for reliability but not for latency, so it's not good for real-time applications like VoIP and fast-paced games (see WebRTC for those use cases).

Due to its simplicity, its wide compatibility, and being easier to use than a raw TCP connection, WebSocket started to spread outside the browsers, in native applications as a mean to communicate with network servers.

Godot supports WebSocket in both native and web exports.

WebSocket is implemented in Godot via WebSocketPeer. The WebSocket implementation is compatible with the High-Level Multiplayer. See section on high-level multiplayer for more details.

When exporting to Android, make sure to enable the INTERNET permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android.

This example will show you how to create a WebSocket connection to a remote server, and how to send and receive data.

This will print something similar to:

This example will show you how to create a WebSocket server that listens for remote connections, and how to send and receive data.

When a client connects, this will print something similar to this:

A more advanced chat demo which optionally uses the multiplayer mid-level abstraction and a high-level multiplayer demo are available in the godot demo projects under networking/websocket_chat and networking/websocket_multiplayer.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node

# The URL we will connect to.
# Use "ws://localhost:9080" if testing with the minimal server example below.
# `wss://` is used for secure connections,
# while `ws://` is used for plain text (insecure) connections.
@export var websocket_url = "wss://echo.websocket.org"

# Our WebSocketClient instance.
var socket = WebSocketPeer.new()


func _ready():
    # Initiate connection to the given URL.
    var err = socket.connect_to_url(websocket_url)
    if err == OK:
        print("Connecting to %s..." % websocket_url)
        # Wait for the socket to connect.
        await get_tree().create_timer(2).timeout

        # Send data.
        print("> Sending test packet.")
        socket.send_text("Test packet")
    else:
        push_error("Unable to connect.")
        set_process(false)


func _process(_delta):
    # Call this in `_process()` or `_physics_process()`.
    # Data transfer and state updates will only happen when calling this function.
    socket.poll()

    # get_ready_state() tells you what state the socket is in.
    var state = socket.get_ready_state()

    # `WebSocketPeer.STATE_OPEN` means the socket is connected and ready
    # to send and receive data.
    if state == WebSocketPeer.STATE_OPEN:
        while socket.get_available_packet_count():
            var packet = socket.get_packet()
            if socket.was_string_packet():
                var packet_text = packet.get_string_from_utf8()
                print("< Got text data from server: %s" % packet_text)
            else:
                print("< Got binary data from server: %d bytes" % packet.size())

    # `WebSocketPeer.STATE_CLOSING` means the socket is closing.
    # It is important to keep polling for a clean close.
    elif state == WebSocketPeer.STATE_CLOSING:
        pass

    # `WebSocketPeer.STATE_CLOSED` means the connection has fully closed.
    # It is now safe to stop polling.
    elif state == WebSocketPeer.STATE_CLOSED:
        # The code will be `-1` if the disconnection was not properly notified by the remote peer.
        var code = socket.get_close_code()
        print("WebSocket closed with code: %d. Clean: %s" % [code, code != -1])
        set_process(false) # Stop processing.
```

Example 2 (sql):
```sql
Connecting to wss://echo.websocket.org...
< Got text data from server: Request served by 7811941c69e658
> Sending test packet.
< Got text data from server: Test packet
```

Example 3 (gdscript):
```gdscript
extends Node

# The port we will listen to.
const PORT = 9080

# Our TCP Server instance.
var _tcp_server = TCPServer.new()

# Our connected peers list.
var _peers: Dictionary[int, WebSocketPeer] = {}

var last_peer_id := 1


func _ready():
    # Start listening on the given port.
    var err = _tcp_server.listen(PORT)
    if err == OK:
        print("Server started.")
    else:
        push_error("Unable to start server.")
        set_process(false)


func _process(_delta):
    while _tcp_server.is_connection_available():
        last_peer_id += 1
        print("+ Peer %d connected." % last_peer_id)
        var ws = WebSocketPeer.new()
        ws.accept_stream(_tcp_server.take_connection())
        _peers[last_peer_id] = ws

    # Iterate over all connected peers using "keys()" so we can erase in the loop
    for peer_id in _peers.keys():
        var peer = _peers[peer_id]

        peer.poll()

        var peer_state = peer.get_ready_state()
        if peer_state == WebSocketPeer.STATE_OPEN:
            while peer.get_available_packet_count():
                var packet = peer.get_packet()
                if peer.was_string_packet():
                    var packet_text = packet.get_string_from_utf8()
                    print("< Got text data from peer %d: %s ... echoing" % [peer_id, packet_text])
                    # Echo the packet back.
                    peer.send_text(packet_text)
                else:
                    print("< Got binary data from peer %d: %d ... echoing" % [peer_id, packet.size()])
                    # Echo the packet back.
                    peer.send(packet)
        elif peer_state == WebSocketPeer.STATE_CLOSED:
            # Remove the disconnected peer.
            _peers.erase(peer_id)
            var code = peer.get_close_code()
            var reason = peer.get_close_reason()
            print("- Peer %s closed with code: %d, reason %s. Clean: %s" % [peer_id, code, reason, code != -1])
```

Example 4 (sql):
```sql
Server started.
+ Peer 2 connected.
< Got text data from peer 2: Test packet ... echoing
```

---

## WebRTC — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/networking/webrtc.html

**Contents:**
- WebRTC
- HTML5, WebSocket, WebRTC
  - WebSocket
  - WebRTC
- Using WebRTC in Godot
  - Minimal connection example
  - Local signaling example
  - Remote signaling with WebSocket
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

One of Godot's great features is its ability to export to the HTML5/WebAssembly platform, allowing your game to run directly in the browser when a user visit your webpage.

This is a great opportunity for both demos and full games, but used to come with some limitations. In the area of networking, browsers used to support only HTTPRequests until recently, when first WebSocket and then WebRTC were proposed as standards.

When the WebSocket protocol was standardized in December 2011, it allowed browsers to create stable and bidirectional connections to a WebSocket server. The protocol is a very powerful tool to send push notifications to browsers, and has been used to implement chats, turn-based games, etc.

WebSockets, though, still use a TCP connection, which is good for reliability but not for latency, so not good for real-time applications like VoIP and fast-paced games.

For this reason, since 2010, Google started working on a new technology called WebRTC, which later on, in 2017, became a W3C candidate recommendation. WebRTC is a much more complex set of specifications, and relies on many other technologies behind the scenes (ICE, DTLS, SDP) to provide fast, real-time, and secure communication between two peers.

The idea is to find the fastest route between the two peers and establish whenever possible a direct communication (i.e. try to avoid a relaying server).

However, this comes at a price, which is that some media information must be exchanged between the two peers before the communication can start (in the form of Session Description Protocol - SDP strings). This usually takes the form of a so-called WebRTC Signaling Server.

Peers connect to a signaling server (for example a WebSocket server) and send their media information. The server then relays this information to other peers, allowing them to establish the desired direct communication. Once this step is done, peers can disconnect from the signaling server and keep the direct Peer-to-Peer (P2P) connection open.

WebRTC is implemented in Godot via two main classes WebRTCPeerConnection and WebRTCDataChannel, plus the multiplayer API implementation WebRTCMultiplayerPeer. See section on high-level multiplayer for more details.

These classes are available automatically in HTML5, but require an external GDExtension plugin on native (non-HTML5) platforms. Check out the webrtc-native plugin repository for instructions and to get the latest release.

When exporting to Android, make sure to enable the INTERNET permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android.

This example will show you how to create a WebRTC connection between two peers in the same application. This is not very useful in real life, but will give you a good overview of how a WebRTC connection is set up.

This example expands on the previous one, separating the peers in two different scenes, and using a singleton as a signaling server.

And now for the local signaling server:

This local signaling server is supposed to be used as a singleton to connect two peers in the same scene.

Then you can use it like this:

This will print something similar to this:

A more advanced demo using WebSocket for signaling peers and WebRTCMultiplayerPeer is available in the godot demo projects under networking/webrtc_signaling.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (gdscript):
```gdscript
extends Node

# Create the two peers
var p1 = WebRTCPeerConnection.new()
var p2 = WebRTCPeerConnection.new()
# And a negotiated channel for each each peer
var ch1 = p1.create_data_channel("chat", {"id": 1, "negotiated": true})
var ch2 = p2.create_data_channel("chat", {"id": 1, "negotiated": true})

func _ready():
    # Connect P1 session created to itself to set local description.
    p1.session_description_created.connect(p1.set_local_description)
    # Connect P1 session and ICE created to p2 set remote description and candidates.
    p1.session_description_created.connect(p2.set_remote_description)
    p1.ice_candidate_created.connect(p2.add_ice_candidate)

    # Same for P2
    p2.session_description_created.connect(p2.set_local_description)
    p2.session_description_created.connect(p1.set_remote_description)
    p2.ice_candidate_created.connect(p1.add_ice_candidate)

    # Let P1 create the offer
    p1.create_offer()

    # Wait a second and send message from P1.
    await get_tree().create_timer(1).timeout
    ch1.put_packet("Hi from P1".to_utf8_buffer())

    # Wait a second and send message from P2.
    await get_tree().create_timer(1).timeout
    ch2.put_packet("Hi from P2".to_utf8_buffer())

func _process(_delta):
    # Poll connections
    p1.poll()
    p2.poll()

    # Check for messages
    if ch1.get_ready_state() == ch1.STATE_OPEN and ch1.get_available_packet_count() > 0:
        print("P1 received: ", ch1.get_packet().get_string_from_utf8())
    if ch2.get_ready_state() == ch2.STATE_OPEN and ch2.get_available_packet_count() > 0:
        print("P2 received: ", ch2.get_packet().get_string_from_utf8())
```

Example 2 (sql):
```sql
P1 received: Hi from P1
P2 received: Hi from P2
```

Example 3 (gdscript):
```gdscript
extends Node
# An example p2p chat client.

var peer = WebRTCPeerConnection.new()

# Create negotiated data channel.
var channel = peer.create_data_channel("chat", {"negotiated": true, "id": 1})

func _ready():
    # Connect all functions.
    peer.ice_candidate_created.connect(self._on_ice_candidate)
    peer.session_description_created.connect(self._on_session)

    # Register to the local signaling server (see below for the implementation).
    Signaling.register(String(get_path()))


func _on_ice_candidate(mid, index, sdp):
    # Send the ICE candidate to the other peer via signaling server.
    Signaling.send_candidate(String(get_path()), mid, index, sdp)


func _on_session(type, sdp):
    # Send the session to other peer via signaling server.
    Signaling.send_session(String(get_path()), type, sdp)
    # Set generated description as local.
    peer.set_local_description(type, sdp)


func _process(delta):
    # Always poll the connection frequently.
    peer.poll()
    if channel.get_ready_state() == WebRTCDataChannel.STATE_OPEN:
        while channel.get_available_packet_count() > 0:
            print(String(get_path()), " received: ", channel.get_packet().get_string_from_utf8())


func send_message(message):
    channel.put_packet(message.to_utf8_buffer())
```

Example 4 (gdscript):
```gdscript
# A local signaling server. Add this to autoloads with name "Signaling" (/root/Signaling)
extends Node

# We will store the two peers here
var peers = []

func register(path):
    assert(peers.size() < 2)
    peers.append(path)
    if peers.size() == 2:
        get_node(peers[0]).peer.create_offer()


func _find_other(path):
    # Find the other registered peer.
    for p in peers:
        if p != path:
            return p
    return ""


func send_session(path, type, sdp):
    var other = _find_other(path)
    assert(other != "")
    get_node(other).peer.set_remote_description(type, sdp)


func send_candidate(path, mid, index, sdp):
    var other = _find_other(path)
    assert(other != "")
    get_node(other).peer.add_ice_candidate(mid, index, sdp)
```

---

## HTTP client class — Godot Engine (stable) documentation in English

**URL:** https://docs.godotengine.org/en/stable/tutorials/networking/http_client_class.html

**Contents:**
- HTTP client class
- User-contributed notes

The content of this page was not yet updated for Godot 4.5 and may be outdated. If you know how to improve this page or you can confirm that it's up to date, feel free to open a pull request.

HTTPClient provides low-level access to HTTP communication. For a higher-level interface, you may want to take a look at HTTPRequest first, which has a tutorial available here.

When exporting to Android, make sure to enable the INTERNET permission in the Android export preset before exporting the project or using one-click deploy. Otherwise, network communication of any kind will be blocked by Android.

Here's an example of using the HTTPClient class. It's just a script, so it can be run by executing:

It will connect and fetch a website.

Please read the User-contributed notes policy before submitting a comment.

© Copyright 2014-present Juan Linietsky, Ariel Manzur and the Godot community (CC BY 3.0).

**Examples:**

Example 1 (yaml):
```yaml
c:\godot> godot -s http_test.gd
```

Example 2 (yaml):
```yaml
c:\godot> godot -s HTTPTest.cs
```

Example 3 (gdscript):
```gdscript
extends SceneTree

# HTTPClient demo
# This simple class can do HTTP requests; it will not block, but it needs to be polled.

func _init():
    var err = 0
    var http = HTTPClient.new() # Create the Client.

    err = http.connect_to_host("www.php.net", 80) # Connect to host/port.
    assert(err == OK) # Make sure connection is OK.

    # Wait until resolved and connected.
    while http.get_status() == HTTPClient.STATUS_CONNECTING or http.get_status() == HTTPClient.STATUS_RESOLVING:
        http.poll()
        print("Connecting...")
        await get_tree().process_frame

    assert(http.get_status() == HTTPClient.STATUS_CONNECTED) # Check if the connection was made successfully.

    # Some headers
    var headers = [
        "User-Agent: Pirulo/1.0 (Godot)",
        "Accept: */*"
    ]

    err = http.request(HTTPClient.METHOD_GET, "/ChangeLog-5.php", headers) # Request a page from the site (this one was chunked..)
    assert(err == OK) # Make sure all is OK.

    while http.get_status() == HTTPClient.STATUS_REQUESTING:
        # Keep polling for as long as the request is being processed.
        http.poll()
        print("Requesting...")
        await get_tree().process_frame

    assert(http.get_status() == HTTPClient.STATUS_BODY or http.get_status() == HTTPClient.STATUS_CONNECTED) # Make sure request finished well.

    print("response? ", http.has_response()) # Site might not have a response.

    if http.has_response():
        # If there is a response...

        headers = http.get_response_headers_as_dictionary() # Get response headers.
        print("code: ", http.get_response_code()) # Show response code.
        print("**headers:\\n", headers) # Show headers.

        # Getting the HTTP Body

        if http.is_response_chunked():
            # Does it use chunks?
            print("Response is Chunked!")
        else:
            # Or just plain Content-Length
            var bl = http.get_response_body_length()
            print("Response Length: ", bl)

        # This method works for both anyway

        var rb = PackedByteArray() # Array that will hold the data.

        while http.get_status() == HTTPClient.STATUS_BODY:
            # While there is body left to be read
            http.poll()
            # Get a chunk.
            var chunk = http.read_response_body_chunk()
            if chunk.size() == 0:
                await get_tree().process_frame
            else:
                rb = rb + chunk # Append to read buffer.
        # Done!

        print("bytes got: ", rb.size())
        var text = rb.get_string_from_ascii()
        print("Text: ", text)

    quit()
```

Example 4 (swift):
```swift
using Godot;

public partial class HTTPTest : SceneTree
{
    // HTTPClient demo.
    // This simple class can make HTTP requests; it will not block, but it needs to be polled.
    public override async void _Initialize()
    {
        Error err;
        HTTPClient http = new HTTPClient(); // Create the client.

        err = http.ConnectToHost("www.php.net", 80); // Connect to host/port.
        Debug.Assert(err == Error.Ok); // Make sure the connection is OK.

        // Wait until resolved and connected.
        while (http.GetStatus() == HTTPClient.Status.Connecting || http.GetStatus() == HTTPClient.Status.Resolving)
        {
            http.Poll();
            GD.Print("Connecting...");
            OS.DelayMsec(500);
        }

        Debug.Assert(http.GetStatus() == HTTPClient.Status.Connected); // Check if the connection was made successfully.

        // Some headers.
        string[] headers =
        [
            "User-Agent: Pirulo/1.0 (Godot)",
            "Accept: */*",
        ];

        err = http.Request(HTTPClient.Method.Get, "/ChangeLog-5.php", headers); // Request a page from the site.
        Debug.Assert(err == Error.Ok); // Make sure all is OK.

        // Keep polling for as long as the request is being processed.
        while (http.GetStatus() == HTTPClient.Status.Requesting)
        {
            http.Poll();
            GD.Print("Requesting...");
            if (OS.HasFeature("web"))
            {
                // Synchronous HTTP requests are not supported on the web,
                // so wait for the next main loop iteration.
                await ToSignal(Engine.GetMainLoop(), "idle_frame");
            }
            else
            {
                OS.DelayMsec(500);
            }
        }

        Debug.Assert(http.GetStatus() == HTTPClient.Status.Body || http.GetStatus() == HTTPClient.Status.Connected); // Make sure the request finished well.

        GD.Print("Response? ", http.HasResponse()); // The site might not have a response.

        // If there is a response...
        if (http.HasResponse())
        {
            headers = http.GetResponseHeaders(); // Get response headers.
            GD.Print("Code: ", http.GetResponseCode()); // Show response code.
            GD.Print("Headers:");
            foreach (string header in headers)
            {
                // Show headers.
                GD.Print(header);
            }

            if (http.IsResponseChunked())
            {
                // Does it use chunks?
                GD.Print("Response is Chunked!");
            }
            else
            {
                // Or just Content-Length.
                GD.Print("Response Length: ", http.GetResponseBodyLength());
            }

            // This method works for both anyways.
            List<byte> rb = new List<byte>(); // List that will hold the data.

            // While there is data left to be read...
            while (http.GetStatus() == HTTPClient.Status.Body)
            {
                http.Poll();
                byte[] chunk = http.ReadResponseBodyChunk(); // Read a chunk.
                if (chunk.Length == 0)
                {
                    // If nothing was read, wait for the buffer to fill.
                    OS.DelayMsec(500);
                }
                else
                {
                    // Append the chunk to the read buffer.
                    rb.AddRange(chunk);
                }
            }

            // Done!
            GD.Print("Bytes Downloaded: ", rb.Count);
            string text = Encoding.ASCII.GetString(rb.ToArray());
            GD.Print(text);
        }
        Quit();
    }
}
```

---
