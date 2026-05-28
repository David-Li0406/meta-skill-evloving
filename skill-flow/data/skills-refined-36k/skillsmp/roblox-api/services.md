# Services Classes

## Contents
- [Players](#players)
- [Workspace](#workspace)
- [ReplicatedStorage](#replicatedstorage)
- [ServerStorage](#serverstorage)
- [RunService](#runservice)
- [TweenService](#tweenservice)
- [UserInputService](#userinputservice)
- [DataStoreService](#datastoreservice)
- [HttpService](#httpservice)
- [SoundService](#soundservice)
- [Lighting](#lighting)
- [StarterGui](#startergui)
- [StarterPlayer](#starterplayer)
- [Teams](#teams)
- [Chat](#chat)
- [MarketplaceService](#marketplaceservice)
- [GamePassService](#gamepassservice)
- [BadgeService](#badgeservice)
- [MemoryStoreService](#memorystoreservice)
- [MessagingService](#messagingservice)
- [PolicyService](#policyservice)
- [LocalizationService](#localizationservice)

---

## Players

A service that contains presently connected `Class.Player` objects.

**Properties:**
- `Players.BanningEnabled`: boolean - Enables or disables the three `Class.Players` methods
- `Players.BubbleChat`: boolean - Indicates whether or not bubble chat is enabled. It is set with the
- `Players.CharacterAutoLoads`: boolean - Indicates whether `Class.Player.Character|characters` will respawn
- `Players.ClassicChat`: boolean - Indicates whether or not classic chat is enabled; set by the
- `Players.LocalPlayer`: Player - The `Class.Player` that the `Class.LocalScript` is running for.
- `Players.localPlayer`: Player
- `Players.MaxPlayers`: int - The maximum number of players that can be in a server.
- `Players.NumPlayers`: int - Returns the number of people in the server at the current time.
- `Players.numPlayers`: int - Returns the number of people in the server at the current time.
- `Players.PreferredPlayers`: int - The preferred number of players for a server.
- ...and 2 more

**Methods:**
- `Players:BanAsync` - Bans users from your experience, with options to specify duration, reason,
- `Players:Chat` - Makes the local player chat the given message.
- `Players:CreateHumanoidModelFromDescriptionAsync` - Returns a character `Class.Model` equipped with everything specified in
- `Players:CreateHumanoidModelFromDescription` - Returns a character `Class.Model` equipped with everything specified in
- `Players:CreateHumanoidModelFromUserIdAsync` - Returns a character Model set-up with everything equipped to match the
- `Players:CreateHumanoidModelFromUserId` - Returns a character Model set-up with everything equipped to match the
- `Players:GetBanHistoryAsync` - Retrieves the ban and unban history of any user within the experience's
- `Players:GetCharacterAppearanceAsync` - Returns a `Class.Model` containing the assets which the player is wearing,
- `Players:GetCharacterAppearanceInfoAsync` - Returns information about the character appearance of a given user.
- `Players:GetFriendsAsync` - Returns a `Class.FriendPages` object which contains information for all of
- ...and 16 more

**Events:**
- `Players.PlayerAdded` - Fires when a player enters the game.
- `Players.PlayerMembershipChanged` - Fires when the game server recognizes that a player's membership has
- `Players.PlayerRemoving` - Fires when a player is about to leave the game.
- `Players.UserSubscriptionStatusChanged` - Fires when the game server recognizes that the user's status for a certain

---

## Workspace

**Workspace** houses 3D objects which are rendered to the 3D world. Objects
not descending from it will not be rendered or physically interact with the
world.

**Properties:**
- `Workspace.AirDensity`: float - The air density at ground level, used in the aerodynamic force model.
- `Workspace.AirTurbulenceIntensity`: float - Controls the strength of turbulence present in the wind velocity field,
- `Workspace.AllowThirdPartySales`: boolean - Determines whether assets created by other users can be sold in the game.
- `Workspace.AuthorityMode`: AuthorityMode - Sets the server authority mode.
- `Workspace.AvatarUnificationMode`: AvatarUnificationMode
- `Workspace.ClientAnimatorThrottling`: ClientAnimatorThrottlingMode - Specifies the animation throttling mode for the local client.
- `Workspace.CurrentCamera`: Camera - The `Class.Camera` object being used by the local player.
- `Workspace.DistributedGameTime`: double - The amount of time, in seconds, that the game has been running.
- `Workspace.FallenPartsDestroyHeight`: float - Determines the height at which falling `Class.BasePart|BaseParts` and
- `Workspace.FallHeightEnabled`: boolean
- ...and 34 more

**Methods:**
- `Workspace:BreakJoints` - Goes through all `Class.BasePart|BaseParts` given, breaking any joints
- `Workspace:GetNumAwakeParts` - Returns the number of `Class.BasePart|BaseParts` that are deemed
- `Workspace:GetPhysicsThrottling` - Returns an integer, between 0 and 100, representing the percentage of real
- `Workspace:GetRealPhysicsFPS` - Returns the number of frames per second that physics is currently being
- `Workspace:GetServerTimeNow` - Returns the server's Unix time in seconds.
- `Workspace:JoinToOutsiders` - Creates joints between the specified `Class.BasePart|Parts` and any
- `Workspace:MakeJoints` - Goes through all `Class.BasePart|BaseParts` given. If any part's side has
- `Workspace:PGSIsEnabled` - Returns `true` if the game has the PGS Physics solver enabled.
- `Workspace:UnjoinFromOutsiders` - Breaks all joints between the specified `Class.BasePart|BaseParts` and
- `Workspace:ZoomToExtents` - Positions and zooms the `Class.Workspace.CurrentCamera` to show the extent

**Events:**
- `Workspace.PersistentLoaded` - Fires when persistent models have been sent to the specified player.

---

## ReplicatedStorage

A container service for objects that are replicated to all clients.

---

## ServerStorage

A container whose contents are only accessible on the server. Objects
descending from ServerStorage will not replicate to the client and will not be
accessible from `Class.LocalScript|LocalScripts`.

---

## RunService

Service responsible for all runtime activity and progression of time.

**Properties:**
- `RunService.ClientGitHash`: string
- `RunService.RunState`: RunState

**Methods:**
- `RunService:BindToRenderStep` - Given a string name of a function and a priority, this method binds the
- `RunService:BindToSimulation` - Binds a custom function to be called at a fixed frequency which is
- `RunService:GetPredictionStatus` - Checks the `Enum.PredictionStatus` of a specific context instance, useful
- `RunService:IsClient` - Returns whether the current environment is running on the client.
- `RunService:IsEdit` - Returns whether the current environment is in `Edit` mode.
- `RunService:IsRunMode` - Returns whether a **Run** playtest has been initiated in Studio.
- `RunService:IsRunning` - Returns whether the experience is currently running.
- `RunService:IsServer` - Returns whether the current environment is running on the server.
- `RunService:IsStudio` - Returns whether the current environment is running in Studio.
- `RunService:Pause` - Pauses the experience's simulation if it is running, suspending physics
- ...and 5 more

**Events:**
- `RunService.Heartbeat` - Fires every frame, after the physics simulation has completed.
- `RunService.PostSimulation` - Fires every frame, after the physics simulation has completed.
- `RunService.PreAnimation` - Fires every frame, prior to the physics simulation but after rendering.
- `RunService.PreRender` - Fires every frame, prior to the frame being rendered.
- `RunService.PreSimulation` - Fires every frame, prior to the physics simulation.

---

## TweenService

Used to create `Class.Tween|Tweens` which interpolate, or tween, the
properties of instances.

**Methods:**
- `TweenService:Create` - Creates a new `Class.Tween` given the object whose properties are to be
- `TweenService:GetValue` - Calculates a new alpha given an `Enum.EasingStyle` and
- `TweenService:SmoothDamp` - Smoothly interpolates a value towards a target, simulating a critically

---

## UserInputService

`UserInputService` is primarily used to detect the input types available on a
user's device, as well as detect input events.

**Properties:**
- `UserInputService.AccelerometerEnabled`: boolean - Describes whether the user's device has an accelerometer.
- `UserInputService.GamepadEnabled`: boolean - Describes whether the user's device has an available gamepad.
- `UserInputService.GyroscopeEnabled`: boolean - Describes whether the user's device has a gyroscope.
- `UserInputService.KeyboardEnabled`: boolean - Describes whether the user's device has a keyboard available.
- `UserInputService.ModalEnabled`: boolean - Toggles whether Roblox's mobile controls are hidden on mobile devices.
- `UserInputService.MouseBehavior`: MouseBehavior - Determines whether the user's mouse can be moved freely or is locked.
- `UserInputService.MouseDeltaSensitivity`: float - Scales the delta (change) output of the user's `Class.Mouse`.
- `UserInputService.MouseEnabled`: boolean - Describes whether the user's device has a mouse available.
- `UserInputService.MouseIcon`: ContentId - The content ID of the image for the user's mouse icon.
- `UserInputService.MouseIconContent`: Content - The content ID of the image for the user's mouse icon. Only supports asset
- ...and 9 more

**Methods:**
- `UserInputService:GamepadSupports` - Returns whether the given `Enum.UserInputType` gamepad supports a button
- `UserInputService:GetConnectedGamepads` - Returns an array of `Enum.UserInputType` gamepads currently connected.
- `UserInputService:GetDeviceAcceleration` - Returns an `Class.InputObject` that describes the device's current
- `UserInputService:GetDeviceGravity` - Returns an `Class.InputObject` describing the device's current gravity
- `UserInputService:GetDeviceRotation` - Returns an `Class.InputObject` and a `Datatype.CFrame` describing the
- `UserInputService:GetFocusedTextBox` - Returns the currently `Class.TextBox` the client is currently focused on.
- `UserInputService:GetGamepadConnected` - Returns whether a gamepad with the given `Enum.UserInputType` is
- `UserInputService:GetGamepadState` - Returns an array of `Class.InputObject|InputObjects` for all available
- `UserInputService:GetImageForKeyCode` - Returns an image for the requested `Enum.KeyCode`.
- `UserInputService:GetKeysPressed` - Returns an array of `Class.InputObject|InputObjects` associated with the
- ...and 14 more

**Events:**
- `UserInputService.DeviceAccelerationChanged` - Fires when a user moves a device that has an accelerometer.
- `UserInputService.DeviceGravityChanged` - Fires when the force of gravity changes on a device that has an enabled
- `UserInputService.DeviceRotationChanged` - Fires when a user rotates a device that has a gyroscope.
- `UserInputService.GamepadConnected` - Fires when a gamepad is connected to the client.
- `UserInputService.GamepadDisconnected` - Fires when a gamepad is disconnected from the client.

---

## DataStoreService

A game service that gives access to persistent data storage across places in a
game.

**Methods:**
- `DataStoreService:GetDataStore` - Creates a `Class.DataStore` instance with the provided name and scope.
- `DataStoreService:GetGlobalDataStore` - Returns the default data store.
- `DataStoreService:GetOrderedDataStore` - Get an `Class.OrderedDataStore` given a name and optional scope.
- `DataStoreService:GetRequestBudgetForRequestType` - Returns the number of requests that can be made by the given request type.
- `DataStoreService:ListDataStoresAsync` - Returns a `Class.DataStoreListingPages` object for enumerating through all

---

## HttpService

Allows sending HTTP requests and provides various web-related and JSON
methods.

**Properties:**
- `HttpService.HttpEnabled`: boolean - Indicates whether HTTP requests can be sent to external websites.

**Methods:**
- `HttpService:CreateWebStreamClient` - Creates a client that opens a persistent connection to stream data.
- `HttpService:GenerateGUID` - Generates a UUID/GUID random string, optionally with curly braces.
- `HttpService:GetAsync` - Sends an HTTP `GET` request.
- `HttpService:GetSecret` - Returns a `Datatype.Secret` from the secrets store.
- `HttpService:JSONDecode` - Decodes a JSON string into a Luau table.
- `HttpService:JSONEncode` - Generate a JSON string from a Luau table.
- `HttpService:PostAsync` - Sends an HTTP `POST` request.
- `HttpService:RequestAsync` - Sends an HTTP request using any HTTP method given a dictionary of
- `HttpService:UrlEncode` - Replaces URL-unsafe characters with '%' and two hexadecimal characters.

---

## SoundService

A service that determines various aspects of how the audio engine works. Most
of its properties affect how `Class.Sound|Sounds` play in the experience.

**Properties:**
- `SoundService.AcousticSimulationEnabled`: boolean - Determines whether acoustic simulation is enabled globally in the advanced
- `SoundService.AmbientReverb`: ReverbType - The ambient sound environment preset applied to all `Class.Sound|Sounds`.
- `SoundService.CharacterSoundsUseNewApi`: RolloutState - Determines whether the default character sounds will use instances in the
- `SoundService.DefaultListenerLocation`: ListenerLocation - Determines where (if anywhere) to place an `Class.AudioListener` by
- `SoundService.DistanceFactor`: float - The number of studs to be considered a meter by `Class.SoundService` when
- `SoundService.DopplerScale`: float - Degree to which the pitch of a `Class.Sound` varies due to the Doppler
- `SoundService.RespectFilteringEnabled`: boolean - Sets whether `Class.Sound` playback from a client will replicate to the
- `SoundService.RolloffScale`: float - Determines how fast the volume of a `Class.Sound` attenuates beyond its
- `SoundService.VolumetricAudio`: VolumetricAudio - Determines whether certain spatialized `Class.Sound|Sounds` emit

**Methods:**
- `SoundService:GetListener` - Returns the current listener type used by `Class.Sound|Sounds`, as well as
- `SoundService:OpenAttenuationCurveEditor` - Opens the attenuation curve editor in Studio for the provided
- `SoundService:OpenDirectionalCurveEditor` - Opens the directional curve editor in Studio for the provided
- `SoundService:PlayLocalSound` - Plays a copy of a `Class.Sound` locally, such that it will only be heard
- `SoundService:SetListener` - Sets the listener used by `Class.Sound|Sounds`.

---

## Lighting

The `Lighting` service controls global lighting in an experience. It includes
a range of adjustable properties that you can use to change how lighting
appears and interacts with other objects.

**Properties:**
- `Lighting.Ambient`: Color3 - The lighting hue applied to areas that are occluded from the sky, such as
- `Lighting.Brightness`: float - The intensity of illumination in the place.
- `Lighting.ClockTime`: float - A numerical representation (in hours) of the current time of day used by
- `Lighting.ColorShift_Bottom`: Color3 - The hue represented in light reflected in the opposite surfaces to those
- `Lighting.ColorShift_Top`: Color3 - The hue represented in light reflected from surfaces facing the sun or
- `Lighting.EnvironmentDiffuseScale`: float - Ambient light that is derived from the environment.
- `Lighting.EnvironmentSpecularScale`: float - Specular light derived from environment.
- `Lighting.ExposureCompensation`: float - The exposure compensation value.
- `Lighting.ExtendLightRangeTo120`: RolloutState
- `Lighting.FogColor`: Color3 - A `Datatype.Color3` value giving the hue of `Lighting` fog.
- ...and 12 more

**Methods:**
- `Lighting:GetMinutesAfterMidnight` - Returns the number of minutes that have passed after midnight for the
- `Lighting:getMinutesAfterMidnight`
- `Lighting:GetMoonDirection` - Returns a `Datatype.Vector3` representing the direction of the moon.
- `Lighting:GetMoonPhase` - Returns the moon's current phase.
- `Lighting:GetSunDirection` - Returns a `Datatype.Vector3` representing the direction of the sun.
- `Lighting:SetMinutesAfterMidnight` - Sets `Class.Lighting.TimeOfDay|TimeOfDay` and
- `Lighting:setMinutesAfterMidnight`

**Events:**
- `Lighting.LightingChanged` - This event fires when a `Lighting` property is changed or a `Class.Sky` is

---

## StarterGui

A container for `Class.LayerCollector` objects to be copied into the
`Class.PlayerGui` of `Class.Player|Players`. Also provides a range of
functions for interacting with the `Class.CoreGui`.

**Properties:**
- `StarterGui.ProcessUserInput`: boolean - Allows this service to process input like `Class.PlayerGui` and
- `StarterGui.ResetPlayerGuiOnSpawn`: boolean - Determines whether each child parented to the StarterGui will be cloned
- `StarterGui.RtlTextSupport`: RtlTextSupport
- `StarterGui.ScreenOrientation`: ScreenOrientation - Sets the default screen orientation mode for users with mobile devices.
- `StarterGui.ShowDevelopmentGui`: boolean - Determines whether the contents of `Class.StarterGui` is visible in
- `StarterGui.VirtualCursorMode`: VirtualCursorMode

**Methods:**
- `StarterGui:GetCore` - Returns a variable that has been specified by a Roblox core script.
- `StarterGui:GetCoreGuiEnabled` - Returns whether the given `Enum.CoreGuiType`is enabled, or if it has been
- `StarterGui:SetCore` - Allows you to perform certain interactions with Roblox's core scripts.
- `StarterGui:SetCoreGuiEnabled` - Sets whether the `Class.CoreGui` element associated with the given

---

## StarterPlayer

A service which allows the defaults of properties in the `Class.Player` object
to be set.

**Properties:**
- `StarterPlayer.AllowCustomAnimations`: boolean - Describes the current game's permission levels regarding custom avatar
- `StarterPlayer.AutoJumpEnabled`: boolean - Sets whether the character will automatically jump when hitting an
- `StarterPlayer.AvatarJointUpgrade`: RolloutState - Controls whether avatars spawn with AnimationConstraint joints for
- `StarterPlayer.CameraMaxZoomDistance`: float - The maximum distance the player's default camera is allowed to zoom out in
- `StarterPlayer.CameraMinZoomDistance`: float - The minimum distance in studs the player's default camera is allowed to
- `StarterPlayer.CameraMode`: CameraMode - Changes the default camera's mode to either first or third person.
- `StarterPlayer.CharacterBreakJointsOnDeath`: boolean - Determines the starting value of `Class.Humanoid.BreakJointsOnDeath` for
- `StarterPlayer.CharacterJumpHeight`: float - Determines the starting value of `Class.Humanoid.JumpHeight` for
- `StarterPlayer.CharacterJumpPower`: float - Determines the starting value of `Class.Humanoid.JumpPower` for
- `StarterPlayer.CharacterMaxSlopeAngle`: float - Determines the starting value of `Class.Humanoid.MaxSlopeAngle` for
- ...and 17 more

---

## Teams

The Teams service holds a game's `Class.Team` objects. `Class.Team` objects
must be parented to the Teams service.

**Methods:**
- `Teams:GetTeams` - Returns a table containing the game's `Class.Team` objects. Will only
- `Teams:RebalanceTeams` - Evens the number of people on each team. This function does not work

---

## Chat

Houses the Luau code responsible for running the legacy chat system.

**Properties:**
- `Chat.BubbleChatEnabled`: boolean - Determines whether player's chat messages will appear above their in-game
- `Chat.LoadDefaultChat`: boolean - Toggles whether the default chat framework should be automatically loaded

**Methods:**
- `Chat:CanUserChatAsync` - Will return false if the player with the specified `Class.Player.UserId`
- `Chat:CanUsersChatAsync` - Will return false if the two users cannot communicate because their
- `Chat:Chat` - Fires the `Class.Chat.Chatted` event with the parameters specified in this
- `Chat:FilterStringAsync` - Filters a string sent from a player to another player using filtering that
- `Chat:FilterStringForBroadcast` - Filters a string sent from a player meant for broadcast to no particular
- `Chat:FilterStringForPlayerAsync` - Filters a string appropriate to the given player's age settings, so they
- `Chat:InvokeChatCallback` - Invoke a chat callback function registered by
- `Chat:RegisterChatCallback` - Register a function to be called upon the invocation of some chat system
- `Chat:SetBubbleChatSettings` - Customizes various settings of the in-game bubble chat.

**Events:**
- `Chat.Chatted` - Fires when `Class.Chat:Chat()` is called.

---

## MarketplaceService

The service responsible for in-experience transactions.

**Methods:**
- `MarketplaceService:GetDeveloperProductsAsync` - Returns a `Class.Pages` object which contains information for all of the
- `MarketplaceService:GetProductInfo` - Returns the product information of an asset using its asset ID.
- `MarketplaceService:GetSubscriptionProductInfoAsync` - Returns the product information of a subscription for the given
- `MarketplaceService:GetUsersPriceLevelsAsync` - Returns the regionalized price level of a user, representing the
- `MarketplaceService:GetUserSubscriptionDetailsAsync` - Returns a table that contains the details of the user's subscription for a
- `MarketplaceService:GetUserSubscriptionPaymentHistoryAsync` - Returns an `Library.table|Array` that contains up to one year of the
- `MarketplaceService:GetUserSubscriptionStatusAsync` - Returns a `Library.table` that contains the subscription status of the
- `MarketplaceService:PlayerOwnsAsset` - Returns whether the given user has the given asset.
- `MarketplaceService:PlayerOwnsAssetAsync` - Returns whether the given user has the given asset.
- `MarketplaceService:PlayerOwnsBundle` - Returns whether the given player owns the given bundle.
- ...and 12 more

**Events:**
- `MarketplaceService.PromptBulkPurchaseFinished` - Fires when a purchase prompt for bulk avatar items is closed.
- `MarketplaceService.PromptBundlePurchaseFinished`
- `MarketplaceService.PromptGamePassPurchaseFinished` - Fires when a purchase prompt for a pass is closed.
- `MarketplaceService.PromptPremiumPurchaseFinished` - Fires when a purchase prompt for Roblox Premium is closed.
- `MarketplaceService.PromptProductPurchaseFinished` - Fires when a purchase prompt for a developer product is closed. Do not use

---

## GamePassService

A service associated with the legacy game pass system. Use
`Class.MarketplaceService` for all new work.

**Methods:**
- `GamePassService:PlayerHasPass` - Returns `true` if the `Class.Player` has the specified **legacy** game

---

## BadgeService

Provides information on badges and awards them.

**Methods:**
- `BadgeService:AwardBadgeAsync` - Award a badge to a player given the ID of each.
- `BadgeService:AwardBadge` - Award a badge to a player given the ID of each.
- `BadgeService:CheckUserBadgesAsync` - Checks a list of badge IDs against a `Class.Player.UserId|UserId` and
- `BadgeService:GetBadgeInfoAsync` - Fetch information about a badge given its ID.
- `BadgeService:IsDisabled` - Returns whether a given badge is disabled.
- `BadgeService:IsLegal` - Determines if a given badge is associated with the current game.
- `BadgeService:UserHasBadge` - Checks whether a user has the badge given the `Class.Player.UserId` and
- `BadgeService:UserHasBadgeAsync` - Checks whether a player has the badge given the `Class.Player.UserId` and

---

## MemoryStoreService

Exposes methods to access specific primitives within MemoryStore.

**Methods:**
- `MemoryStoreService:GetHashMap` - Returns a `Class.MemoryStoreHashMap` instance for the provided name.
- `MemoryStoreService:GetQueue` - Returns a `Class.MemoryStoreQueue` instance for the provided name.
- `MemoryStoreService:GetSortedMap` - Returns a `Class.MemoryStoreSortedMap` instance for the provided name.

---

## MessagingService

Allows servers of the same experience to communicate with each other.

**Methods:**
- `MessagingService:PublishAsync` - Invokes the supplied callback whenever a message is pushed to the topic.
- `MessagingService:SubscribeAsync` - Begins listening to the given topic.

---

## PolicyService

Helps you query information regarding policy compliance for players around the
world based on age range, location, and platform type.

**Methods:**
- `PolicyService:CanViewBrandProjectAsync` - Determines if a user can see brand project assets inside your experience.
- `PolicyService:GetPolicyInfoForPlayerAsync` - Returns policy information about a player based on geolocation, age group,

---

## LocalizationService

Handles automated translation.

**Properties:**
- `LocalizationService.RobloxLocaleId`: string - The locale ID used for localizing core and internal features.
- `LocalizationService.SystemLocaleId`: string - The locale ID that the local player has set for their operating system.

**Methods:**
- `LocalizationService:GetCorescriptLocalizations` - Returns a list of `Class.LocalizationTable` objects used for localizing
- `LocalizationService:GetCountryRegionForPlayerAsync` - Returns country/region code string according to player's client IP
- `LocalizationService:GetTableEntries` - Gets all entries used for automated localization.
- `LocalizationService:GetTranslatorForLocaleAsync` - Yields until the cloud `Class.LocalizationTable` for the argument locale
- `LocalizationService:GetTranslatorForPlayer` - Returns a `Class.Translator` to be used for translations using the locale
- `LocalizationService:GetTranslatorForPlayerAsync` - Yields until the cloud `Class.LocalizationTable` for the player's locale

---

