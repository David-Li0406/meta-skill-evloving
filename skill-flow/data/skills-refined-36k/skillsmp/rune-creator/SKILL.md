---
name: rune-creator
description: Procedural guide for adding or modifying rune resources (.tres) in this Godot rune project. Use when creating new runes, wiring effects (conditions/targets/payloads), updating icons, or adjusting descriptions/elements/rarity.
---

# Rune Creator

How to author a new rune using existing reusable pieces.

## Quick workflow
- Pick tier/rarity/elements. Default tier 1; rarity follows element count (1=common, 2=uncommon, etc.).
- Copy a similar rune in `resources/runes/<rarity>/` and edit in-place.
- Prefer existing building blocks: `rune_effect.gd`, conditions in `resources/effects/conditions/`, targets in `resources/effects/targets/`, payloads in `resources/effects/payloads/`.
- Add a base score effect if needed (e.g., `effect_score_30.tres`) before modular effects.
- Choose an icon from `sprites/icons/runes/` and set `textures = [ExtResource("<icon>")]` (one texture per tier unless variant art exists).
- Write a concise description; include element icon cues by relying on payload/condition descriptions (they pull from `ElementIcons`).

## Reusable payloads/targets to favor
- Score per element adjacency: `payload_score_per_element.gd` with `target_elements = [FIRE|WATER|EARTH|AIR|SPIRIT]`, `score_per_match = +/-N`. Target with `target_adjacent.tres` and set `include_diagonals = true` when diagonals count.
- Score per remaining activations: `payload_score_per_remaining_activations.gd` with `score_per_activation`, `activation_source` (SELF, TARGETS, TARGETS_SUM), optional `allowed_elements` to filter (e.g., `[FIRE]`). Pair with `target_adjacent` (diagonals optional).
- Flat score: `effect_score_30.tres` (or variants) targets self.
- Conditions: usually `condition_always.tres`; use more specific only if required.
- Targets: `target_adjacent.tres`, `target_below.tres`, `target_next.tres`, etc. Set `include_diagonals`/`include_self` on sub-resources when needed.

## Minimal rune template (edit values)
```gdresource
[gd_resource type="Resource" script_class="RuneData" format=3]

[ext_resource type="Script" path="res://scripts/data/rune_data.gd" id="1_data"]
[ext_resource type="Script" path="res://scripts/data/rune_effect.gd" id="1_effect"]
[ext_resource type="Resource" path="res://resources/effects/conditions/condition_always.tres" id="2_cond"]
[ext_resource type="Resource" path="res://resources/effects/targets/target_adjacent.tres" id="3_target_adjacent"]
[ext_resource type="Script" path="res://scripts/data/effects/payloads/payload_score_per_element.gd" id="4_payload_elem"]
[ext_resource type="Texture2D" path="res://sprites/icons/runes/IconNN.png" id="5_icon"]

[sub_resource type="Resource" id="TargetAdj"]
script = ExtResource("3_target_adjacent")
include_diagonals = false

[sub_resource type="Resource" id="PayloadElem"]
script = ExtResource("4_payload_elem")
target_elements = Array[int]([0]) # FIRE=0, WATER=1, EARTH=2, AIR=3, SPIRIT=4
score_per_match = 20

[sub_resource type="Resource" id="Effect1"]
script = ExtResource("1_effect")
condition = ExtResource("2_cond")
target = SubResource("TargetAdj")
payload = SubResource("PayloadElem")

[resource]
script = ExtResource("1_data")
id = "new_id"
rune_name = "Novo Nome"
description = "Descreva o efeito principal"
tier = 1
rarity = 0 # 0=COMMON,1=UNCOMMON,2=RARE,3=EPIC,4=LEGENDARY
base_max_activations = 1
is_indestructible = true
elements = Array[int]([0])
textures = Array[Texture2D]([ExtResource("5_icon")])
effects = Array[ExtResource("1_effect")]([SubResource("Effect1")])
```

## Notes from recent runes
- Diagonal adjacency: set `include_diagonals = true` on the `TargetAdjacent` sub-resource (Óleo uses this).
- Counting remaining activations only for certain elements: set `allowed_elements = [FIRE]` in `payload_score_per_remaining_activations` and choose `activation_source = TARGETS` (counting runes) or `TARGETS_SUM` (summing charges).
- Element-linked descriptions auto-render icons when payload/condition specifies elements; keep descriptions short and factual.

## Checklist before shipping
- [ ] Correct folder by rarity and `elements` matches gameplay intent.
- [ ] Description matches implemented effects (order: flat bonuses first, then conditional parts).
- [ ] Textures array not empty and UID/path valid.
- [ ] Effects array references only existing sub-resources/ext_resources.
- [ ] If new parameters added to payloads, ensure tooltips render (e.g., `allowed_elements` for remaining-activations).
- [ ] Load in Godot and verify tooltip and scoring in a test grid.
