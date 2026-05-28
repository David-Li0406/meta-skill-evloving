---
name: game-systems
description: Use this skill when implementing common game systems such as inventory, quests, shops, crafting, and progression in games.
---

# Skill body

## Inventory System

### Slot-Based Inventory (Lua)
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
            return true
        end
    end

    return false
end
```

### Item Data Resource (GDScript)
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

### Inventory Container (GDScript)
```gdscript
class_name Inventory
extends RefCounted

signal item_added(item: ItemData, amount: int)
signal item_removed(item: ItemData, amount: int)
signal inventory_changed

var slots: Array[Dictionary] = []  # [{item: ItemData, amount: int}]
var max_slots: int

func _init(size: int = 20) -> void:
    max_slots = size
    slots.resize(size)
    for i in range(size):
        slots[i] = {"item": null, "amount": 0}

func add_item(item: ItemData, amount: int = 1) -> int:
    var remaining := amount

    # Try to stack with existing items
    for slot in slots:
        if slot.item == item and slot.amount < item.max_stack:
            var can_add := min(remaining, item.max_stack - slot.amount)
            slot.amount += can_add
            remaining -= can_add
            if remaining == 0:
                break

    # Add to empty slots
    while remaining > 0:
        var empty_slot := find_empty_slot()
        if empty_slot == -1:
            break  # Inventory full

        var add_amount := min(remaining, item.max_stack)
        slots[empty_slot] = {"item": item, "amount": add_amount}
        remaining -= add_amount

    var added := amount - remaining
    if added > 0:
        item_added.emit(item, added)
        inventory_changed.emit()

    return remaining  # Return leftover amount

func remove_item(item: ItemData, amount: int = 1) -> bool:
    var remaining := amount

    for slot in slots:
        if slot.item == item:
            var remove := min(remaining, slot.amount)
            slot.amount -= remove
            remaining -= remove

            if slot.amount <= 0:
                slot.item = null  # Clear the slot if empty

    return remaining == 0  # Return true if all requested items were removed
```