# Godot Llm Integration - Sharp Edges

## Linux Dependency Missing

### **Id**
linux-dependency-missing
### **Summary**
NobodyWho fails to load on Linux with missing library errors
### **Severity**
critical
### **Situation**
Works on Windows/macOS, crashes on Linux with libgomp/vulkan errors
### **Why**
  NobodyWho's binaries from Godot Asset Library are compiled for generic Linux.
  They expect dynamic libraries in FHS locations (/lib, /usr/lib).
  NixOS and some distros don't have libraries in expected paths.
  
### **Solution**
  # SYMPTOMS:
  # - "libgomp.so.1: cannot open shared object file"
  # - "libvulkan.so.1: not found"
  # - Works on Ubuntu but not Fedora/NixOS
  
  # FIX 1: Install missing libraries (Ubuntu/Debian)
  # Terminal:
  # sudo apt install libgomp1 libvulkan1
  
  # FIX 2: Install missing libraries (Fedora)
  # sudo dnf install libgomp vulkan-loader
  
  # FIX 3: NixOS - use nix-ld or steam-run
  # In your shell.nix or flake:
  # { pkgs, ... }: {
  #   environment.systemPackages = [ pkgs.steam-run ];
  # }
  # Run Godot with: steam-run godot
  
  # FIX 4: Set LD_LIBRARY_PATH
  # export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
  # godot
  
  # FIX 5: Build from source with local dependencies
  # git clone https://github.com/nobodywho-ooo/nobodywho
  # cd nobodywho && cargo build --release
  
### **Symptoms**
  - cannot open shared object file
  - libgomp.so.1 not found
  - libvulkan.so.1 not found
  - Works on one Linux distro but not another
### **Detection Pattern**
Linux|linux|\.so|shared object

## Model Node Not Shared

### **Id**
model-node-not-shared
### **Summary**
Memory explodes with multiple NPCs using separate model nodes
### **Severity**
critical
### **Situation**
Adding more NPCs causes out-of-memory or extreme slowdown
### **Why**
  NobodyWhoModel loads the entire model weights into RAM.
  A 3B Q4 model is ~2GB in memory. Each separate NobodyWhoModel
  duplicates this. 5 NPCs = 10GB RAM = crash.
  
### **Solution**
  # WRONG: Separate model per NPC
  # Blacksmith.tscn:
  #   Blacksmith
  #     └── NobodyWhoModel  <- Loads 2GB
  #     └── NobodyWhoChat
  #
  # Innkeeper.tscn:
  #   Innkeeper
  #     └── NobodyWhoModel  <- Another 2GB!
  #     └── NobodyWhoChat
  
  # RIGHT: Shared model in autoload
  # Global.gd (autoload)
  extends Node
  
  var llm_model: NobodyWhoModel
  
  func _ready():
      llm_model = NobodyWhoModel.new()
      llm_model.model_file = "res://ai/qwen-3b-q4.gguf"
      add_child(llm_model)
  
  # NPC scripts reference shared model:
  # npc.gd
  extends CharacterBody2D
  
  @onready var chat: NobodyWhoChat = $NobodyWhoChat
  
  func _ready():
      # Point to shared model (loaded once)
      chat.model_node = Global.llm_model
  
  # Now: 1 model = 2GB regardless of NPC count
  
### **Symptoms**
  - RAM usage grows with each NPC
  - Game slows down with more NPCs active
  - Out of memory crash
  - Model loading time multiplied
### **Detection Pattern**
NobodyWhoModel|model_node

## Export Native Missing

### **Id**
export-native-missing
### **Summary**
Export works but LLM fails with missing native libraries
### **Severity**
critical
### **Situation**
Game runs in editor, exported game crashes on LLM calls
### **Why**
  NobodyWho uses GDExtension native libraries. These must be included in exports.
  Godot's export templates may not automatically include all required .dll/.so/.dylib files.
  Export presets need correct architecture and platform settings.
  
### **Solution**
  # CHECKLIST FOR EXPORTS:
  
  # 1. Verify NobodyWho addon structure:
  # res://addons/nobodywho/
  #   ├── bin/
  #   │   ├── linux/
  #   │   │   └── libnobodywho.so
  #   │   ├── windows/
  #   │   │   └── nobodywho.dll
  #   │   └── macos/
  #   │       └── libnobodywho.dylib
  #   └── nobodywho.gdextension
  
  # 2. Check .gdextension file includes all platforms
  # nobodywho.gdextension should have:
  # [libraries]
  # linux.x86_64 = "res://addons/nobodywho/bin/linux/libnobodywho.so"
  # windows.x86_64 = "res://addons/nobodywho/bin/windows/nobodywho.dll"
  # macos.universal = "res://addons/nobodywho/bin/macos/libnobodywho.dylib"
  
  # 3. In Export Preset:
  # - Resources tab: Ensure addons/** is included
  # - Features: Match target architecture (x86_64, arm64)
  
  # 4. Include model file:
  # Model GGUF file must be in exported resources
  # Place in res:// and verify it's exported
  
  # 5. Test export, not just editor:
  func _ready():
      if OS.has_feature("editor"):
          print("WARNING: Test in export, not just editor!")
  
### **Symptoms**
  - Works in editor, crashes in export
  - GDExtension library not found
  - NobodyWho classes not recognized
  - Crash on first LLM call
### **Detection Pattern**
export|Export|\.pck

## Main Thread Block Gdscript

### **Id**
main-thread-block-gdscript
### **Summary**
Game freezes during LLM response generation
### **Severity**
high
### **Situation**
FPS drops to 0 when NPC is thinking, input unresponsive
### **Why**
  GDScript runs on main thread. Long operations block rendering.
  While NobodyWho is async internally, waiting for it incorrectly blocks.
  Using await in the wrong pattern still freezes the game.
  
### **Solution**
  # WRONG: Synchronous-looking code that blocks
  func talk_to_npc(input: String):
      var response = chat.say_and_wait(input)  # If this exists, blocks!
      show_dialogue(response)
  
  # WRONG: Await in animation/update
  func _process(delta):
      if waiting_for_response:
          var response = await chat.get_response()  # Blocks process!
  
  # RIGHT: Signal-based non-blocking
  func _ready():
      chat.message_received.connect(_on_response)
  
  func talk_to_npc(input: String):
      show_thinking_indicator()
      chat.say(input)  # Returns immediately, emits signal when done
  
  func _on_response(response: String):
      hide_thinking_indicator()
      show_dialogue(response)
  
  # RIGHT: If you must await, use timer-based check
  func talk_to_npc_awaited(input: String) -> String:
      chat.say(input)
      show_thinking_indicator()
  
      var response = ""
      var received = false
      chat.message_received.connect(func(r): response = r; received = true)
  
      while not received:
          await get_tree().process_frame  # Yields to engine
  
      hide_thinking_indicator()
      return response
  
### **Symptoms**
  - FPS drops during dialogue
  - Input unresponsive while NPC responds
  - Animation stutters
  - UI freezes
### **Detection Pattern**
await.*say|_process.*await|while.*await

## Context Window Exceeded

### **Id**
context-window-exceeded
### **Summary**
NPC responses become incoherent after long conversations
### **Severity**
high
### **Situation**
NPC forgets earlier parts of conversation, contradicts itself
### **Why**
  All LLMs have context limits. Without management, old messages get truncated.
  NobodyWho has "preemptive context shifting" but needs proper setup.
  Long system prompts eat into available context.
  
### **Solution**
  # Check your context usage:
  func check_context():
      var used = chat.get_context_length()
      var max_ctx = chat.context_size
      print("Context: %d / %d tokens" % [used, max_ctx])
  
  # Enable context shifting (NobodyWho feature)
  func _ready():
      # In Inspector or code:
      chat.enable_context_shifting = true
      chat.context_shift_threshold = 0.8  # Shift when 80% full
  
  # Keep system prompts concise:
  # WRONG: 500 word backstory in system prompt
  chat.system_prompt = """[Very long backstory about the character's
  childhood, every item in their shop, their opinions on 47 topics...]"""
  
  # RIGHT: Essential personality only
  chat.system_prompt = """You are Grimjaw, a gruff blacksmith.
  Speak in short sentences. Love your craft. Hate small talk.
  Never break character."""
  
  # For backstory, inject relevant parts dynamically:
  func inject_relevant_lore(player_question: String):
      var relevant = search_lore_database(player_question)
      chat.say("Context: %s\n\nPlayer: %s" % [relevant, player_question])
  
### **Symptoms**
  - NPC forgets earlier conversation
  - Responses become generic/confused
  - NPC contradicts what it said earlier
  - "Lost in the middle" behavior
### **Detection Pattern**
context_size|system_prompt|get_context_length

## Mobile Not Ready

### **Id**
mobile-not-ready
### **Summary**
Attempting to deploy LLM game to mobile platforms
### **Severity**
high
### **Situation**
Game works on desktop, fails or performs terribly on mobile
### **Why**
  NobodyWho mobile support is experimental as of 2025. Android has issues
  with native library loading. iOS not yet supported. Mobile devices have
  limited RAM and thermal constraints even when it works.
  
### **Solution**
  # Current mobile status (2025):
  # - Android: Experimental, see GitHub issues #114, #66, #67
  # - iOS: Not yet supported
  # - Web: Not supported (WASM limitations)
  
  # If you MUST target mobile:
  
  # 1. Wait for stable mobile support
  # Check: https://github.com/nobodywho-ooo/nobodywho/issues
  
  # 2. Use cloud API fallback
  func get_response(input: String) -> String:
      if OS.has_feature("mobile"):
          return await cloud_api_request(input)
      else:
          return await local_llm_request(input)
  
  # 3. Use tiny models only
  # Mobile maximum: 1-2B parameters
  # Use qwen-0.5b or phi-2 style models
  
  # 4. Pre-generate common responses
  # Bake common NPC responses at build time
  var pregenerated = preload("res://data/common_responses.json")
  func maybe_use_cached(input: String) -> String:
      var cached = find_similar(input, pregenerated)
      if cached:
          return cached
      return await llm_request(input)
  
  # 5. Desktop-first development
  # Ship desktop version first, add mobile later
  
### **Symptoms**
  - Crash on Android at LLM load
  - iOS build fails with missing symbols
  - Extreme performance issues on mobile
  - App killed by OS for memory usage
### **Detection Pattern**
mobile|Mobile|Android|iOS|android|ios

## Model File Missing Export

### **Id**
model-file-missing-export
### **Summary**
Model GGUF file not included in export
### **Severity**
high
### **Situation**
Export runs but LLM fails with "file not found"
### **Why**
  GGUF files are large (1-5GB). Godot may not export them by default.
  Export filters might exclude .gguf extension. Model path in code
  may differ from where file is actually placed.
  
### **Solution**
  # 1. Place model in res:// (not user://)
  # res://ai/models/qwen-3b-q4.gguf
  
  # 2. Verify export includes it
  # In Export Preset > Resources:
  # - Filters to export: *.gguf
  # OR
  # - Export all resources (larger export)
  
  # 3. Use correct path in code
  var model_path = "res://ai/models/qwen-3b-q4.gguf"
  # NOT "C:/Dev/MyGame/ai/models/..." (absolute path)
  # NOT "ai/models/..." (relative without res://)
  
  # 4. Verify file exists at runtime
  func _ready():
      var model_path = "res://ai/models/qwen-3b-q4.gguf"
      if not FileAccess.file_exists(model_path):
          push_error("Model file not found: " + model_path)
          push_error("Ensure GGUF is exported and path is correct")
  
  # 5. Consider external model (for size)
  # For very large models, load from user data dir
  func get_model_path() -> String:
      var bundled = "res://ai/models/qwen-3b-q4.gguf"
      var external = OS.get_user_data_dir() + "/models/qwen-3b-q4.gguf"
  
      if FileAccess.file_exists(bundled):
          return bundled
      elif FileAccess.file_exists(external):
          return external
      else:
          push_error("No model found!")
          return ""
  
### **Symptoms**
  - "File not found" error in export
  - LLM works in editor but not export
  - Model loading fails silently
  - NobodyWho initialized but no responses
### **Detection Pattern**
\.gguf|model_file|model_path|res://

## Grammar Not Used For Actions

### **Id**
grammar-not-used-for-actions
### **Summary**
Relying on LLM to output valid JSON without constraints
### **Severity**
medium
### **Situation**
Sometimes NPC actions work, sometimes JSON parse fails
### **Why**
  LLMs are not deterministic. They might output "{"action": "attack"}" one time
  and "I'll attack! {action: attack}" the next. Without grammar constraints,
  you're gambling on output format.
  
### **Solution**
  # WRONG: Hope for valid JSON
  func get_action(input: String):
      chat.system_prompt = "Respond with JSON: {\"speech\": \"...\", \"action\": \"...\"}"
      chat.say(input)
  
  func _on_response(response: String):
      var data = JSON.parse_string(response)  # Sometimes fails!
      if data:
          do_action(data.action)
  
  # RIGHT: Grammar-constrained output
  const ACTION_GRAMMAR = """
  root ::= response
  response ::= '{"speech":"' text '","action":"' action '"}'
  text ::= [^"]+
  action ::= "none" | "attack" | "trade" | "flee"
  """
  
  func _ready():
      chat.grammar = ACTION_GRAMMAR
  
  func _on_response(response: String):
      # Guaranteed to be valid JSON matching grammar
      var data = JSON.parse_string(response)
      # data.action is guaranteed to be one of: none, attack, trade, flee
      execute_action(data.action)
      show_dialogue(data.speech)
  
### **Symptoms**
  - JSON parse errors
  - Actions work inconsistently
  - NPC sometimes outputs unexpected format
  - Game logic breaks on malformed response
### **Detection Pattern**
JSON\.parse|json.*parse|grammar