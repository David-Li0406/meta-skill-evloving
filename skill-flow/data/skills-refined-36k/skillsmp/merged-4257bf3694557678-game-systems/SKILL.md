---
name: game-systems
description: Implements common game systems including inventory, shops, quests, crafting, dialogue, and leveling. Use when building game features and mechanics.
---

# Game Systems

When implementing game systems, follow these patterns for robust and extensible features.

## Inventory System

### Slot-Based Inventory (Roblox)
```lua
local InventoryService = {}

local DEFAULT_SLOTS = 20
local MAX_STACK = 99

function InventoryService.create(maxSlots)
    return {
        slots = {},
        maxSlots = maxSlots or DEFAULT_SLOTS
    }
end

function InventoryService.addItem(inventory, itemId, quantity)
    quantity = quantity or 1

    -- Try to stack with existing
    for slotIndex, slot in pairs(inventory.slots) do
        if slot.itemId == itemId and slot.quantity < MAX_STACK then
            local canAdd = math.min(quantity, MAX_STACK - slot.quantity)
            slot.quantity = slot.quantity + canAdd
            quantity = quantity - canAdd

            if quantity <= 0 then
                return true, slotIndex
            end
        end
    end

    -- Find empty slots for remaining
    while quantity > 0 do
        local emptySlot = InventoryService.findEmptySlot(inventory)
        if not emptySlot then
            return false, "Inventory full"
        end

        local stackSize = math.min(quantity, MAX_STACK)
        inventory.slots[emptySlot] = {
            itemId = itemId,
            quantity = stackSize
        }
        quantity = quantity - stackSize
    end

    return true
end

function InventoryService.removeItem(inventory, itemId, quantity)
    quantity = quantity or 1
    local removed = 0

    -- Remove from slots (prefer partial stacks first)
    local slots = {}
    for slotIndex, slot in pairs(inventory.slots) do
        if slot.itemId == itemId then
            table.insert(slots, {index = slotIndex, quantity = slot.quantity})
        end
    end

    table.sort(slots, function(a, b) return a.quantity < b.quantity end)

    for _, slotInfo in ipairs(slots) do
        local slot = inventory.slots[slotInfo.index]
        local toRemove = math.min(quantity - removed, slot.quantity)

        slot.quantity = slot.quantity - toRemove
        removed = removed + toRemove

        if slot.quantity <= 0 then
            inventory.slots[slotInfo.index] = nil
        end

        if removed >= quantity then
            break
        end
    end

    return removed >= quantity, removed
end

function InventoryService.hasItem(inventory, itemId, quantity)
    quantity = quantity or 1
    local total = 0

    for _, slot in pairs(inventory.slots) do
        if slot.itemId == itemId then
            total = total + slot.quantity
            if total >= quantity then
                return true
            end
        end
    end

    return false
end

function InventoryService.getItemCount(inventory, itemId)
    local total = 0
    for _, slot in pairs(inventory.slots) do
        if slot.itemId == itemId then
            total = total + slot.quantity
        end
    end
    return total
end

function InventoryService.findEmptySlot(inventory)
    for i = 1, inventory.maxSlots do
        if not inventory.slots[i] then
            return i
        end
    end
    return nil
end
```

### Item Data Resource (Godot)
```gdscript
# item_data.gd
class_name ItemData
extends Resource

@export var id: String
@export var name: String
@export var description: String
@export var icon: Texture2D
@export var max_stack: int = 99
@export var item_type: ItemType
@export var rarity: Rarity
@export var value: int

enum ItemType { CONSUMABLE, EQUIPMENT, MATERIAL, KEY_ITEM }
enum Rarity { COMMON, UNCOMMON, RARE, EPIC, LEGENDARY }

func use(user: Node) -> bool:
    # Override in specific item scripts
    return false
```

## Shop System

### Server-Side Shop with Validation (Roblox)
```lua
local ShopService = {}

local ShopItems = {
    sword_basic = {price = 100, currency = "coins", category = "weapons"},
    potion_health = {price = 50, currency = "coins", category = "consumables"},
    vip_pass = {price = 499, currency = "robux", productId = 123456789}
}

function ShopService.canPurchase(player, itemId, quantity)
    quantity = quantity or 1
    local item = ShopItems[itemId]

    if not item then
        return false, "Item not found"
    end

    if item.currency == "robux" then
        return true, "Use promptPurchase"
    end

    local playerCurrency = DataManager.get(player, item.currency) or 0
    local totalCost = item.price * quantity

    if playerCurrency < totalCost then
        return false, "Not enough " .. item.currency
    end

    local inventory = DataManager.get(player, "inventory")
    local emptySlots = InventoryService.countEmptySlots(inventory)

    if emptySlots < math.ceil(quantity / MAX_STACK) then
        return false, "Inventory full"
    end

    return true, totalCost
end

function ShopService.purchase(player, itemId, quantity)
    quantity = quantity or 1

    local canBuy, result = ShopService.canPurchase(player, itemId, quantity)
    if not canBuy then
        return false, result
    end

    local item = ShopItems[itemId]

    if item.currency == "robux" then
        MarketplaceService:PromptProductPurchase(player, item.productId)
        return true, "Purchase prompted"
    end

    local success = DataManager.removeCurrency(player, item.currency, result)
    if not success then
        return false, "Transaction failed"
    end

    local inventory = DataManager.get(player, "inventory")
    local added = InventoryService.addItem(inventory, itemId, quantity)

    if not added then
        DataManager.addCurrency(player, item.currency, result)
        return false, "Failed to add item"
    end

    return true, "Purchase successful"
end
```

### Shop (Godot)
```gdscript
class_name Shop
extends Node

signal purchase_made(item: ItemData, amount: int)
signal sale_made(item: ItemData, amount: int)

@export var shop_inventory: Array[ShopItem]
@export var buy_multiplier: float = 1.0
@export var sell_multiplier: float = 0.5

class ShopItem:
    var item: ItemData
    var stock: int  # -1 for unlimited
    var price_override: int  # -1 to use item's base value

func get_buy_price(item: ItemData) -> int:
    for shop_item in shop_inventory:
        if shop_item.item == item:
            var base := shop_item.price_override if shop_item.price_override >= 0 else item.value
            return int(base * buy_multiplier)
    return int(item.value * buy_multiplier)

func get_sell_price(item: ItemData) -> int:
    return int(item.value * sell_multiplier)

func can_buy(item: ItemData, amount: int = 1) -> bool:
    var price := get_buy_price(item) * amount

    if PlayerStats.gold < price:
        return false

    for shop_item in shop_inventory:
        if shop_item.item == item:
            if shop_item.stock >= 0 and shop_item.stock < amount:
                return false

    return true

func buy(item: ItemData, amount: int = 1) -> bool:
    if not can_buy(item, amount):
        return false

    var price := get_buy_price(item) * amount
    PlayerStats.gold -= price

    PlayerInventory.add_item(item, amount)

    for shop_item in shop_inventory:
        if shop_item.item == item and shop_item.stock >= 0:
            shop_item.stock -= amount

    purchase_made.emit(item, amount)
    return true
```

## Quest System

### Quest Manager (Roblox)
```lua
local QuestService = {}

local QuestDefinitions = {
    kill_enemies_1 = {
        title = "Enemy Slayer",
        description = "Defeat 10 enemies",
        objectives = {
            {type = "kill", target = "enemy", count = 10}
        },
        rewards = {
            {type = "currency", currency = "coins", amount = 100},
            {type = "experience", amount = 50}
        }
    },
    collect_items_1 = {
        title = "Collector",
        description = "Collect 5 gems",
        objectives = {
            {type = "collect", item = "gem", count = 5}
        },
        rewards = {
            {type = "currency", currency = "coins", amount = 200}
        }
    }
}

function QuestService.startQuest(player, questId)
    local quest = QuestDefinitions[questId]
    if not quest then return false end

    local playerQuests = DataManager.get(player, "activeQuests") or {}

    if playerQuests[questId] then
        return false, "Quest already active"
    end

    playerQuests[questId] = {
        startedAt = os.time(),
        progress = {}
    }

    for i, objective in ipairs(quest.objectives) do
        playerQuests[questId].progress[i] = 0
    end

    DataManager.set(player, "activeQuests", playerQuests)
    return true
end
```

### Quest Manager (Godot)
```gdscript
class_name QuestManager
extends Node

signal quest_started(quest: QuestData)
signal quest_completed(quest: QuestData)
signal quest_failed(quest: QuestData)
signal objective_updated(quest: QuestData, objective: QuestObjective)

var quests: Dictionary = {}  # id -> QuestData
var active_quests: Array[String] = []
var completed_quests: Array[String] = []
var objective_progress: Dictionary = {}  # "quest_id:objective_id" -> int

func start_quest(quest_id: String) -> bool:
    var quest := quests.get(quest_id) as QuestData
    if not quest:
        return false

    for prereq in quest.prerequisites:
        if prereq not in completed_quests:
            return false

    active_quests.append(quest_id)

    for objective in quest.objectives:
        objective_progress[quest_id + ":" + objective.id] = 0

    quest_started.emit(quest)
    return true
```

## Crafting System

### Crafting Manager (Godot)
```gdscript
class_name CraftingManager
extends Node

signal item_crafted(recipe: CraftingRecipe)

var recipes: Array[CraftingRecipe] = []
var discovered_recipes: Array[String] = []

func can_craft(recipe: CraftingRecipe, station: String = "") -> bool:
    if recipe.required_station and recipe.required_station != station:
        return false

    if PlayerStats.crafting_level < recipe.required_skill_level:
        return false

    for ingredient in recipe.ingredients:
        if not PlayerInventory.has_item(ingredient.item, ingredient.amount):
            return false

    return true

func craft(recipe: CraftingRecipe) -> bool:
    if not can_craft(recipe):
        return false

    for ingredient in recipe.ingredients:
        PlayerInventory.remove_item(ingredient.item, ingredient.amount)

    PlayerInventory.add_item(recipe.result_item, recipe.result_amount)
    item_crafted.emit(recipe)
    return true
```

## Leveling System

### Experience and Levels (Roblox)
```lua
local LevelingService = {}

local function getRequiredXP(level)
    return level * level * 100
end

function LevelingService.addExperience(player, amount)
    local currentLevel = DataManager.get(player, "level") or 1
    local currentXP = DataManager.get(player, "experience") or 0

    currentXP = currentXP + amount

    local levelsGained = 0
    while currentXP >= getRequiredXP(currentLevel) do
        currentXP = currentXP - getRequiredXP(currentLevel)
        currentLevel = currentLevel + 1
        levelsGained = levelsGained + 1
    end

    DataManager.set(player, "level", currentLevel)
    DataManager.set(player, "experience", currentXP)

    if levelsGained > 0 then
        LevelingService.onLevelUp(player, currentLevel, levelsGained)
    end

    return currentLevel, currentXP, levelsGained
end
```

### Leveling System (Godot)
```gdscript
class_name LevelingSystem
extends Node

signal level_up(new_level: int)
signal exp_gained(amount: int)

var level := 1
var experience := 0
var skill_points := 0

var base_exp := 100
var exp_exponent := 1.5

func get_exp_for_level(target_level: int) -> int:
    return int(base_exp * pow(target_level, exp_exponent))

func add_experience(amount: int) -> void:
    experience += amount
    exp_gained.emit(amount)

    while experience >= get_exp_for_level(level + 1):
        level += 1
        skill_points += 1
        level_up.emit(level)
```

## Dialogue System

### Dialogue Manager (Godot)
```gdscript
class_name DialogueManager
extends Node

signal dialogue_started(dialogue: DialogueData)
signal dialogue_ended
signal line_displayed(line: DialogueLine)
signal choices_presented(choices: Array[DialogueChoice])

var current_dialogue: DialogueData
var current_line_index := 0
var dialogue_database: Dictionary = {}
var variables: Dictionary = {}

func start_dialogue(dialogue_id: String) -> void:
    current_dialogue = dialogue_database.get(dialogue_id)
    if not current_dialogue:
        push_error("Dialogue not found: " + dialogue_id)
        return

    current_line_index = 0
    dialogue_started.emit(current_dialogue)
    display_current_line()
```