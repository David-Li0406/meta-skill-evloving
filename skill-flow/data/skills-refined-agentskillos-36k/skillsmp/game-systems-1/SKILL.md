---
name: game-systems
description: Implements common game systems including inventory, dialogue, quests, shops, crafting, and progression. Use when building game features and mechanics.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Game Systems

When implementing game systems, use these patterns for robust and extensible features.

## Inventory System

### Item Data Resource
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

### Inventory Container
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

            if slot.amount == 0:
                slot.item = null

            if remaining == 0:
                break

    if remaining < amount:
        item_removed.emit(item, amount - remaining)
        inventory_changed.emit()
        return true

    return false

func has_item(item: ItemData, amount: int = 1) -> bool:
    var total := 0
    for slot in slots:
        if slot.item == item:
            total += slot.amount
            if total >= amount:
                return true
    return false

func find_empty_slot() -> int:
    for i in range(slots.size()):
        if slots[i].item == null:
            return i
    return -1

func get_item_count(item: ItemData) -> int:
    var total := 0
    for slot in slots:
        if slot.item == item:
            total += slot.amount
    return total
```

### Equipment System
```gdscript
class_name EquipmentManager
extends Node

signal equipment_changed(slot: EquipmentSlot, item: ItemData)

enum EquipmentSlot { WEAPON, HEAD, BODY, LEGS, ACCESSORY_1, ACCESSORY_2 }

var equipped: Dictionary = {}  # EquipmentSlot -> ItemData
var stats_modifier: Dictionary = {}

func equip(slot: EquipmentSlot, item: ItemData) -> ItemData:
    var previous := equipped.get(slot)

    equipped[slot] = item
    recalculate_stats()
    equipment_changed.emit(slot, item)

    return previous  # Return unequipped item

func unequip(slot: EquipmentSlot) -> ItemData:
    var item: ItemData = equipped.get(slot)
    equipped.erase(slot)
    recalculate_stats()
    equipment_changed.emit(slot, null)
    return item

func recalculate_stats() -> void:
    stats_modifier.clear()

    for item in equipped.values():
        if item and item.has_method("get_stats"):
            var stats: Dictionary = item.get_stats()
            for stat in stats:
                stats_modifier[stat] = stats_modifier.get(stat, 0) + stats[stat]

func get_stat_bonus(stat: String) -> int:
    return stats_modifier.get(stat, 0)
```

## Dialogue System

### Dialogue Data
```gdscript
# dialogue_data.gd
class_name DialogueData
extends Resource

@export var id: String
@export var lines: Array[DialogueLine]

# dialogue_line.gd
class_name DialogueLine
extends Resource

@export var speaker: String
@export var text: String
@export var portrait: Texture2D
@export var choices: Array[DialogueChoice]
@export var conditions: Array[String]  # Condition checks
@export var effects: Array[String]  # Effects to trigger

# dialogue_choice.gd
class_name DialogueChoice
extends Resource

@export var text: String
@export var next_dialogue_id: String
@export var conditions: Array[String]
@export var effects: Array[String]
```

### Dialogue Manager
```gdscript
class_name DialogueManager
extends Node

signal dialogue_started(dialogue: DialogueData)
signal dialogue_ended
signal line_displayed(line: DialogueLine)
signal choices_presented(choices: Array[DialogueChoice])

var current_dialogue: DialogueData
var current_line_index := 0
var dialogue_database: Dictionary = {}  # id -> DialogueData
var variables: Dictionary = {}  # For conditions/effects

func start_dialogue(dialogue_id: String) -> void:
    current_dialogue = dialogue_database.get(dialogue_id)
    if not current_dialogue:
        push_error("Dialogue not found: " + dialogue_id)
        return

    current_line_index = 0
    dialogue_started.emit(current_dialogue)
    display_current_line()

func display_current_line() -> void:
    if current_line_index >= current_dialogue.lines.size():
        end_dialogue()
        return

    var line := current_dialogue.lines[current_line_index]

    # Check conditions
    if not check_conditions(line.conditions):
        current_line_index += 1
        display_current_line()
        return

    # Apply effects
    apply_effects(line.effects)

    line_displayed.emit(line)

    if line.choices.size() > 0:
        var valid_choices: Array[DialogueChoice] = []
        for choice in line.choices:
            if check_conditions(choice.conditions):
                valid_choices.append(choice)
        choices_presented.emit(valid_choices)

func advance() -> void:
    current_line_index += 1
    display_current_line()

func select_choice(choice: DialogueChoice) -> void:
    apply_effects(choice.effects)

    if choice.next_dialogue_id:
        start_dialogue(choice.next_dialogue_id)
    else:
        advance()

func end_dialogue() -> void:
    current_dialogue = null
    dialogue_ended.emit()

func check_conditions(conditions: Array[String]) -> bool:
    for condition in conditions:
        if not evaluate_condition(condition):
            return false
    return true

func evaluate_condition(condition: String) -> bool:
    # Parse and evaluate condition string
    # Example: "has_item:key", "reputation>=10"
    var parts := condition.split(":")
    match parts[0]:
        "has_item":
            return PlayerInventory.has_item(parts[1])
        "flag":
            return variables.get(parts[1], false)
        _:
            return true

func apply_effects(effects: Array[String]) -> void:
    for effect in effects:
        var parts := effect.split(":")
        match parts[0]:
            "set_flag":
                variables[parts[1]] = true
            "give_item":
                PlayerInventory.add_item(parts[1], int(parts[2]))
            "give_exp":
                PlayerStats.add_exp(int(parts[1]))
```

## Quest System

### Quest Data
```gdscript
class_name QuestData
extends Resource

@export var id: String
@export var title: String
@export var description: String
@export var objectives: Array[QuestObjective]
@export var rewards: Array[QuestReward]
@export var prerequisites: Array[String]  # Quest IDs

enum QuestState { LOCKED, AVAILABLE, ACTIVE, COMPLETED, FAILED }

# quest_objective.gd
class_name QuestObjective
extends Resource

@export var id: String
@export var description: String
@export var type: ObjectiveType
@export var target: String  # Enemy ID, Item ID, Location, etc.
@export var required_amount: int = 1
@export var optional: bool = false

enum ObjectiveType { KILL, COLLECT, TALK, REACH, INTERACT }

# quest_reward.gd
class_name QuestReward
extends Resource

@export var type: RewardType
@export var id: String
@export var amount: int

enum RewardType { ITEM, GOLD, EXP, UNLOCK }
```

### Quest Manager
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

    # Check prerequisites
    for prereq in quest.prerequisites:
        if prereq not in completed_quests:
            return false

    active_quests.append(quest_id)

    # Initialize progress
    for objective in quest.objectives:
        objective_progress[quest_id + ":" + objective.id] = 0

    quest_started.emit(quest)
    return true

func update_objective(type: QuestObjective.ObjectiveType, target: String, amount: int = 1) -> void:
    for quest_id in active_quests:
        var quest := quests[quest_id] as QuestData

        for objective in quest.objectives:
            if objective.type == type and objective.target == target:
                var key := quest_id + ":" + objective.id
                objective_progress[key] = min(
                    objective_progress.get(key, 0) + amount,
                    objective.required_amount
                )
                objective_updated.emit(quest, objective)

                check_quest_completion(quest_id)

func check_quest_completion(quest_id: String) -> void:
    var quest := quests[quest_id] as QuestData
    var all_complete := true

    for objective in quest.objectives:
        if objective.optional:
            continue

        var key := quest_id + ":" + objective.id
        if objective_progress.get(key, 0) < objective.required_amount:
            all_complete = false
            break

    if all_complete:
        complete_quest(quest_id)

func complete_quest(quest_id: String) -> void:
    var quest := quests[quest_id] as QuestData

    active_quests.erase(quest_id)
    completed_quests.append(quest_id)

    # Give rewards
    for reward in quest.rewards:
        apply_reward(reward)

    quest_completed.emit(quest)

func apply_reward(reward: QuestReward) -> void:
    match reward.type:
        QuestReward.RewardType.ITEM:
            PlayerInventory.add_item(reward.id, reward.amount)
        QuestReward.RewardType.GOLD:
            PlayerStats.gold += reward.amount
        QuestReward.RewardType.EXP:
            PlayerStats.add_exp(reward.amount)

func get_objective_progress(quest_id: String, objective_id: String) -> int:
    return objective_progress.get(quest_id + ":" + objective_id, 0)
```

## Shop System

### Shop
```gdscript
class_name Shop
extends Node

signal purchase_made(item: ItemData, amount: int)
signal sale_made(item: ItemData, amount: int)

@export var shop_inventory: Array[ShopItem]
@export var buy_multiplier: float = 1.0  # Price modifier for buying
@export var sell_multiplier: float = 0.5  # Price modifier for selling

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

    # Check player has enough money
    if PlayerStats.gold < price:
        return false

    # Check stock
    for shop_item in shop_inventory:
        if shop_item.item == item:
            if shop_item.stock >= 0 and shop_item.stock < amount:
                return false

    # Check inventory space
    # (simplified - would need proper inventory check)
    return true

func buy(item: ItemData, amount: int = 1) -> bool:
    if not can_buy(item, amount):
        return false

    var price := get_buy_price(item) * amount
    PlayerStats.gold -= price

    PlayerInventory.add_item(item, amount)

    # Reduce stock
    for shop_item in shop_inventory:
        if shop_item.item == item and shop_item.stock >= 0:
            shop_item.stock -= amount

    purchase_made.emit(item, amount)
    return true

func sell(item: ItemData, amount: int = 1) -> bool:
    if not PlayerInventory.has_item(item, amount):
        return false

    var price := get_sell_price(item) * amount
    PlayerStats.gold += price

    PlayerInventory.remove_item(item, amount)

    sale_made.emit(item, amount)
    return true
```

## Crafting System

### Recipe Data
```gdscript
class_name CraftingRecipe
extends Resource

@export var id: String
@export var result_item: ItemData
@export var result_amount: int = 1
@export var ingredients: Array[CraftingIngredient]
@export var required_station: String  # Empty for anywhere
@export var required_skill_level: int = 0

class CraftingIngredient:
    var item: ItemData
    var amount: int
```

### Crafting Manager
```gdscript
class_name CraftingManager
extends Node

signal item_crafted(recipe: CraftingRecipe)

var recipes: Array[CraftingRecipe] = []
var discovered_recipes: Array[String] = []

func can_craft(recipe: CraftingRecipe, station: String = "") -> bool:
    # Check station
    if recipe.required_station and recipe.required_station != station:
        return false

    # Check skill level
    if PlayerStats.crafting_level < recipe.required_skill_level:
        return false

    # Check ingredients
    for ingredient in recipe.ingredients:
        if not PlayerInventory.has_item(ingredient.item, ingredient.amount):
            return false

    return true

func craft(recipe: CraftingRecipe) -> bool:
    if not can_craft(recipe):
        return false

    # Remove ingredients
    for ingredient in recipe.ingredients:
        PlayerInventory.remove_item(ingredient.item, ingredient.amount)

    # Add result
    var leftover := PlayerInventory.add_item(recipe.result_item, recipe.result_amount)

    if leftover > 0:
        # Drop excess items or handle differently
        pass

    item_crafted.emit(recipe)
    return true

func get_craftable_recipes(station: String = "") -> Array[CraftingRecipe]:
    var craftable: Array[CraftingRecipe] = []

    for recipe in recipes:
        if can_craft(recipe, station):
            craftable.append(recipe)

    return craftable

func discover_recipe(recipe_id: String) -> void:
    if recipe_id not in discovered_recipes:
        discovered_recipes.append(recipe_id)
```

## Leveling System

### Experience and Levels
```gdscript
class_name LevelingSystem
extends Node

signal level_up(new_level: int)
signal exp_gained(amount: int)

var level := 1
var experience := 0
var skill_points := 0

# Experience curve: exp_needed = base * (level ^ exponent)
var base_exp := 100
var exp_exponent := 1.5

func get_exp_for_level(target_level: int) -> int:
    return int(base_exp * pow(target_level, exp_exponent))

func get_exp_to_next_level() -> int:
    return get_exp_for_level(level + 1) - experience

func add_experience(amount: int) -> void:
    experience += amount
    exp_gained.emit(amount)

    # Check for level ups
    while experience >= get_exp_for_level(level + 1):
        level += 1
        skill_points += 1
        level_up.emit(level)

func get_level_progress() -> float:
    var current_level_exp := get_exp_for_level(level)
    var next_level_exp := get_exp_for_level(level + 1)
    return float(experience - current_level_exp) / (next_level_exp - current_level_exp)
```

### Skill Tree
```gdscript
class_name SkillTree
extends Node

signal skill_unlocked(skill: SkillData)

var skills: Dictionary = {}  # id -> SkillData
var unlocked_skills: Array[String] = []

class SkillData:
    var id: String
    var name: String
    var description: String
    var icon: Texture2D
    var cost: int
    var prerequisites: Array[String]
    var effects: Dictionary  # stat -> bonus

func can_unlock(skill_id: String) -> bool:
    var skill: SkillData = skills.get(skill_id)
    if not skill:
        return false

    if skill_id in unlocked_skills:
        return false

    if PlayerStats.skill_points < skill.cost:
        return false

    for prereq in skill.prerequisites:
        if prereq not in unlocked_skills:
            return false

    return true

func unlock_skill(skill_id: String) -> bool:
    if not can_unlock(skill_id):
        return false

    var skill: SkillData = skills[skill_id]
    PlayerStats.skill_points -= skill.cost
    unlocked_skills.append(skill_id)

    # Apply effects
    for stat in skill.effects:
        PlayerStats.add_permanent_bonus(stat, skill.effects[stat])

    skill_unlocked.emit(skill)
    return true

func get_available_skills() -> Array[SkillData]:
    var available: Array[SkillData] = []
    for id in skills:
        if can_unlock(id):
            available.append(skills[id])
    return available
```
