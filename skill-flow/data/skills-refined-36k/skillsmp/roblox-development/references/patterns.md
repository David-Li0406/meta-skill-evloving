# Roblox Development

## Patterns


---
  #### **Name**
Server-Client Architecture
  #### **Description**
Properly separate server and client code for security
  #### **Detection**
script|server|client|remote
  #### **Guidance**
    ## Roblox Server-Client Architecture
    
    NEVER trust the client. The server is law.
    
    ### Folder Structure
    
    ```
    game/
    ├── ServerScriptService/      # Server-only scripts
    │   ├── GameManager.lua
    │   ├── DataManager.lua
    │   └── CombatHandler.lua
    ├── ReplicatedStorage/        # Shared between server/client
    │   ├── Modules/
    │   │   ├── Config.lua
    │   │   └── Utils.lua
    │   └── Remotes/              # RemoteEvents and Functions
    ├── StarterPlayerScripts/     # Client scripts
    │   ├── InputHandler.lua
    │   └── UIController.lua
    └── StarterGui/               # UI elements
    ```
    
    ### RemoteEvent Pattern (Secure)
    
    ```lua
    -- ServerScriptService/CombatHandler.lua
    local ReplicatedStorage = game:GetService("ReplicatedStorage")
    local Players = game:GetService("Players")
    
    local AttackRemote = ReplicatedStorage.Remotes:WaitForChild("Attack")
    
    -- NEVER trust client data without validation
    AttackRemote.OnServerEvent:Connect(function(player, targetId)
        -- Validate player exists and is alive
        local character = player.Character
        if not character or not character:FindFirstChild("Humanoid") then
            return
        end
        if character.Humanoid.Health <= 0 then
            return
        end
    
        -- Validate target exists
        local target = workspace:FindFirstChild(targetId)
        if not target or not target:FindFirstChild("Humanoid") then
            return
        end
    
        -- Validate distance (prevent teleport hacks)
        local distance = (character.HumanoidRootPart.Position - target.HumanoidRootPart.Position).Magnitude
        if distance > 10 then -- Max attack range
            warn("Player " .. player.Name .. " attempted attack from too far")
            return
        end
    
        -- Validate cooldown (prevent spam)
        local lastAttack = player:GetAttribute("LastAttack") or 0
        if tick() - lastAttack < 0.5 then
            return
        end
        player:SetAttribute("LastAttack", tick())
    
        -- NOW we can process the attack (server-side damage calculation)
        local damage = 10 -- Server decides damage, NOT client
        target.Humanoid:TakeDamage(damage)
    end)
    ```
    
    ### What Goes Where
    
    | Logic | Location | Why |
    |-------|----------|-----|
    | Damage calculation | Server | Prevent god mode |
    | Currency changes | Server | Prevent duping |
    | Inventory changes | Server | Prevent item spawning |
    | Player input | Client | Responsiveness |
    | UI updates | Client | Performance |
    | Animations | Client | Smoothness |
    | Sound effects | Client | No latency |
    
  #### **Success Rate**
Proper server authority prevents 95% of exploits

---
  #### **Name**
DataStore Management
  #### **Description**
Reliably save and load player data
  #### **Detection**
datastore|save|load|data|persistence
  #### **Guidance**
    ## DataStore Best Practices
    
    Player data loss = players never return. Get this right.
    
    ### ProfileService Pattern (Recommended)
    
    ```lua
    -- ServerScriptService/DataManager.lua
    local DataStoreService = game:GetService("DataStoreService")
    local Players = game:GetService("Players")
    
    local DataManager = {}
    
    -- Use versioned DataStore names for migrations
    local DATASTORE_NAME = "PlayerData_v3"
    local playerDataStore = DataStoreService:GetDataStore(DATASTORE_NAME)
    
    -- Session locking to prevent duplication
    local activeSessions = {}
    
    -- Default data template (NEVER save nil values)
    local DEFAULT_DATA = {
        Coins = 0,
        Gems = 0,
        Level = 1,
        Experience = 0,
        Inventory = {},
        Settings = {
            MusicVolume = 0.5,
            SFXVolume = 0.5
        },
        Statistics = {
            PlayTime = 0,
            GamesPlayed = 0
        },
        Version = 3 -- For migrations
    }
    
    function DataManager:LoadData(player)
        local key = "Player_" .. player.UserId
        local success, data = pcall(function()
            return playerDataStore:GetAsync(key)
        end)
    
        if not success then
            warn("DataStore load failed for " .. player.Name .. ": " .. tostring(data))
            -- Retry logic
            for i = 1, 3 do
                wait(1)
                success, data = pcall(function()
                    return playerDataStore:GetAsync(key)
                end)
                if success then break end
            end
        end
    
        if not success then
            -- Critical failure - kick player to prevent data corruption
            player:Kick("Failed to load your data. Please rejoin.")
            return nil
        end
    
        -- New player or migration needed
        if not data then
            data = table.clone(DEFAULT_DATA)
        else
            -- Migrate old data
            data = self:MigrateData(data)
        end
    
        -- Session lock
        activeSessions[player.UserId] = data
    
        return data
    end
    
    function DataManager:SaveData(player)
        local data = activeSessions[player.UserId]
        if not data then return false end
    
        local key = "Player_" .. player.UserId
    
        local success, err = pcall(function()
            playerDataStore:SetAsync(key, data)
        end)
    
        if not success then
            warn("DataStore save failed: " .. tostring(err))
            -- Queue for retry
            return false
        end
    
        return true
    end
    
    function DataManager:MigrateData(data)
        -- Handle old data versions
        if not data.Version or data.Version < 3 then
            -- Add new fields with defaults
            data.Settings = data.Settings or DEFAULT_DATA.Settings
            data.Statistics = data.Statistics or DEFAULT_DATA.Statistics
            data.Version = 3
        end
        return data
    end
    
    -- Auto-save every 60 seconds
    spawn(function()
        while true do
            wait(60)
            for userId, data in pairs(activeSessions) do
                local player = Players:GetPlayerByUserId(userId)
                if player then
                    DataManager:SaveData(player)
                end
            end
        end
    end)
    
    -- Save on leave
    Players.PlayerRemoving:Connect(function(player)
        DataManager:SaveData(player)
        activeSessions[player.UserId] = nil
    end)
    
    -- Handle server shutdown
    game:BindToClose(function()
        for userId, data in pairs(activeSessions) do
            local player = Players:GetPlayerByUserId(userId)
            if player then
                DataManager:SaveData(player)
            end
        end
    end)
    
    return DataManager
    ```
    
    ### DataStore Limits
    
    | Limit | Value | Strategy |
    |-------|-------|----------|
    | Request budget | 60 + 10*players/min | Batch saves |
    | Key size | 50 chars | Use UserId |
    | Value size | 4MB | Compress inventory |
    | Throttle | 6 sec between same key | Queue writes |
    
  #### **Success Rate**
Proper DataStore handling has 99.9%+ data retention

---
  #### **Name**
Monetization Design
  #### **Description**
Ethical monetization that respects young players
  #### **Detection**
monetize|robux|gamepass|devproduct|premium
  #### **Guidance**
    ## Roblox Monetization
    
    Remember: Many players are kids. Be ethical.
    
    ### Game Pass vs Developer Product
    
    ```lua
    -- Game Pass: One-time purchase, permanent
    -- Developer Product: Consumable, buy multiple times
    
    local MarketplaceService = game:GetService("MarketplaceService")
    local Players = game:GetService("Players")
    
    -- Game Pass IDs (create in Game Settings > Monetization)
    local GAME_PASSES = {
        VIP = 123456789,
        DoubleCoins = 123456790,
        ExtraInventory = 123456791
    }
    
    -- Developer Product IDs
    local DEV_PRODUCTS = {
        Coins100 = 123456792,
        Coins500 = 123456793,
        SkipLevel = 123456794
    }
    
    -- Check if player owns game pass
    function HasGamePass(player, passName)
        local passId = GAME_PASSES[passName]
        if not passId then return false end
    
        local success, owns = pcall(function()
            return MarketplaceService:UserOwnsGamePassAsync(player.UserId, passId)
        end)
    
        return success and owns
    end
    
    -- Process developer product purchase
    local function ProcessReceipt(receiptInfo)
        local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
        if not player then
            return Enum.ProductPurchaseDecision.NotProcessedYet
        end
    
        local productId = receiptInfo.ProductId
        local data = DataManager:GetData(player)
    
        if productId == DEV_PRODUCTS.Coins100 then
            data.Coins = data.Coins + 100
        elseif productId == DEV_PRODUCTS.Coins500 then
            data.Coins = data.Coins + 500
        elseif productId == DEV_PRODUCTS.SkipLevel then
            data.Level = data.Level + 1
        else
            return Enum.ProductPurchaseDecision.NotProcessedYet
        end
    
        -- Save immediately after purchase
        if DataManager:SaveData(player) then
            return Enum.ProductPurchaseDecision.PurchaseGranted
        else
            return Enum.ProductPurchaseDecision.NotProcessedYet
        end
    end
    
    MarketplaceService.ProcessReceipt = ProcessReceipt
    ```
    
    ### Ethical Monetization Guidelines
    
    | Do | Don't |
    |----|-------|
    | Cosmetics that don't affect gameplay | Pay-to-win mechanics |
    | Time savers (2x coins) | Required purchases to progress |
    | Clear pricing | Hidden costs |
    | Permanent game passes | Temporary boosts that expire |
    | Value bundles | Predatory limited-time pressure |
    
    ### Pricing Strategy
    
    | Item Type | Price Range | Why |
    |-----------|-------------|-----|
    | Small cosmetic | 25-75 Robux | Impulse buy |
    | Game pass | 100-400 Robux | Value perception |
    | Premium feature | 400-1000 Robux | Serious fans |
    | Currency pack | 50-500 Robux | Multiple tiers |
    
  #### **Success Rate**
Games with ethical monetization have 40% higher retention

---
  #### **Name**
Performance Optimization
  #### **Description**
Keep games running smoothly on all devices
  #### **Detection**
performance|lag|optimize|fps|memory
  #### **Guidance**
    ## Roblox Performance Optimization
    
    Many players are on mobile/low-end devices. Optimize for them.
    
    ### Common Performance Killers
    
    ```lua
    -- BAD: Finding parts every frame
    game:GetService("RunService").Heartbeat:Connect(function()
        local coin = workspace:FindFirstChild("Coin") -- BAD!
        if coin then
            -- do something
        end
    end)
    
    -- GOOD: Cache references
    local coin = workspace:WaitForChild("Coin")
    game:GetService("RunService").Heartbeat:Connect(function()
        if coin then
            -- do something
        end
    end)
    
    -- BAD: Creating parts in loops
    for i = 1, 1000 do
        local part = Instance.new("Part")
        part.Parent = workspace
    end
    
    -- GOOD: Use object pooling
    local PartPool = {}
    local poolSize = 100
    
    function GetPart()
        if #PartPool > 0 then
            return table.remove(PartPool)
        end
        return Instance.new("Part")
    end
    
    function ReturnPart(part)
        part.Parent = nil
        part.CFrame = CFrame.new(0, -1000, 0) -- Move out of sight
        table.insert(PartPool, part)
    end
    ```
    
    ### Streaming & LOD
    
    ```lua
    -- Enable StreamingEnabled in Workspace properties
    -- This loads/unloads parts based on player distance
    
    -- For important parts that must always exist:
    part.ModelStreamingMode = Enum.ModelStreamingMode.Persistent
    
    -- For parts that can stream:
    part.ModelStreamingMode = Enum.ModelStreamingMode.Default
    
    -- LOD (Level of Detail) for complex models
    local function SetupLOD(model, lodDistances)
        local RunService = game:GetService("RunService")
        local camera = workspace.CurrentCamera
    
        local highDetail = model:FindFirstChild("HighDetail")
        local lowDetail = model:FindFirstChild("LowDetail")
    
        RunService.Heartbeat:Connect(function()
            local distance = (camera.CFrame.Position - model.PrimaryPart.Position).Magnitude
    
            if distance < lodDistances.high then
                highDetail.Transparency = 0
                lowDetail.Transparency = 1
            else
                highDetail.Transparency = 1
                lowDetail.Transparency = 0
            end
        end)
    end
    ```
    
    ### Memory Management
    
    | Issue | Solution |
    |-------|----------|
    | Connection leaks | Disconnect events when done |
    | Orphaned instances | Use Debris service |
    | Large tables | Clear when not needed |
    | Too many parts | Use MeshParts, merge parts |
    
    ```lua
    -- Connection cleanup
    local connection
    connection = event:Connect(function()
        -- do stuff
        if shouldStop then
            connection:Disconnect()
        end
    end)
    
    -- Debris for temporary objects
    local Debris = game:GetService("Debris")
    local explosion = Instance.new("Explosion")
    explosion.Parent = workspace
    Debris:AddItem(explosion, 2) -- Remove after 2 seconds
    ```
    
  #### **Success Rate**
Optimized games have 60% lower bounce rate on mobile

## Anti-Patterns


---
  #### **Name**
Trusting Client Data
  #### **Description**
Accepting client-sent values without validation
  #### **Detection**
RemoteEvent|RemoteFunction|OnServerEvent
  #### **Why Harmful**
    Exploiters can send any data they want through RemoteEvents.
    If you trust "damage = 999999" from the client, your game is broken.
    Every competitive Roblox game gets exploited if client is trusted.
    
  #### **What To Do**
    Server calculates all important values. Client only sends intent
    ("I want to attack target X"), server validates and executes.
    Validate distance, cooldowns, ownership, and all parameters.
    

---
  #### **Name**
Direct Currency Modification
  #### **Description**
Letting client request specific currency amounts
  #### **Detection**
Coins|Currency|Money|Gems
  #### **Why Harmful**
    RemoteEvent("AddCoins", 999999) = instant economy destruction.
    Players will find it, share it, and your game's economy collapses.
    
  #### **What To Do**
    Server grants currency based on server-verified events.
    Client requests actions ("sell item"), server calculates value.
    Never expose a "give me X currency" remote.
    

---
  #### **Name**
No Auto-Save
  #### **Description**
Only saving on player leave
  #### **Detection**
PlayerRemoving|save|SaveData
  #### **Why Harmful**
    Players crash, disconnect, or leave unexpectedly. If you only
    save on PlayerRemoving, crashes = data loss. Server shutdown
    without BindToClose = everyone loses progress.
    
  #### **What To Do**
    Auto-save every 60-120 seconds. Use BindToClose for shutdown.
    Save immediately after purchases. Consider session locking.
    

---
  #### **Name**
Infinite Loops Without Yields
  #### **Description**
Loops that don't wait/yield
  #### **Detection**
while true|for.*do
  #### **Why Harmful**
    A while loop without wait() freezes the entire game. This is
    the #1 cause of "script timeout" and unresponsive games.
    
  #### **What To Do**
    Always include wait(), task.wait(), or RunService event in loops.
    Use task.spawn for concurrent operations. Avoid busy-waiting.
    

---
  #### **Name**
Hardcoded IDs
  #### **Description**
Putting asset/game pass IDs directly in code
  #### **Detection**
\d{9,}
  #### **Why Harmful**
    When you need to change an asset, you hunt through all scripts.
    Miss one? Bug. Different IDs for testing vs production? Chaos.
    
  #### **What To Do**
    Centralize IDs in a Config module. Use separate configs for
    testing and production. Reference by name, not number.
    