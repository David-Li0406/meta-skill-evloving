# Godot LLM Integration

## Patterns


---
  #### **Name**
Basic NobodyWho Setup
  #### **Description**
Standard NobodyWho configuration for dialogue
  #### **When**
Starting a new Godot project with LLM features
  #### **Example**
    # Scene structure:
    # Root
    #   ├── NobodyWhoModel (shared)
    #   └── NPCs
    #       ├── Blacksmith (NobodyWhoChat -> Model)
    #       └── Innkeeper (NobodyWhoChat -> Model)
    
    # In your autoload (Global.gd)
    extends Node
    
    var model: NobodyWhoModel
    
    func _ready():
        # Load model once at game start
        model = preload("res://ai/model_node.tscn").instantiate()
        add_child(model)
        # Model file set in inspector: "res://ai/models/qwen-3b-q4.gguf"
    
    # In NPC script
    extends CharacterBody2D
    
    @onready var chat: NobodyWhoChat = $NobodyWhoChat
    
    func _ready():
        # Point to shared model
        chat.model_node = Global.model
    
        # Set character prompt
        chat.system_prompt = """You are Grimjaw, a gruff blacksmith.
        You speak in short, direct sentences.
        You love your craft and hate idle chatter.
        Never break character or mention being an AI."""
    
    func on_player_speak(text: String):
        # Non-blocking - emits signal when done
        chat.say(text)
    
    func _on_chat_message_received(response: String):
        # Connected via signal
        show_dialogue(response)
    

---
  #### **Name**
Signal-Based Dialogue Flow
  #### **Description**
Proper async dialogue using Godot signals
  #### **When**
Implementing NPC conversations without blocking
  #### **Example**
    extends Node
    class_name DialogueManager
    
    signal dialogue_started(npc_name: String)
    signal dialogue_response(npc_name: String, text: String)
    signal dialogue_ended(npc_name: String)
    
    var active_chat: NobodyWhoChat = null
    var is_generating: bool = false
    
    func start_dialogue(npc: Node, player_input: String):
        if is_generating:
            return  # Don't interrupt ongoing generation
    
        var chat = npc.get_node("NobodyWhoChat")
        active_chat = chat
        is_generating = true
    
        # Connect to response signal
        if not chat.message_received.is_connected(_on_response):
            chat.message_received.connect(_on_response)
    
        dialogue_started.emit(npc.name)
    
        # Show thinking indicator
        show_thinking_bubble(npc)
    
        # Non-blocking call
        chat.say(player_input)
    
    func _on_response(response: String):
        is_generating = false
        hide_thinking_bubble()
    
        # Emit for UI to handle
        dialogue_response.emit(active_chat.get_parent().name, response)
    
    func end_dialogue():
        active_chat = null
        dialogue_ended.emit("")
    

---
  #### **Name**
Grammar-Constrained Responses
  #### **Description**
Use NobodyWho's grammar feature for structured output
  #### **When**
NPCs need to trigger game actions, not just speak
  #### **Example**
    # NobodyWho can constrain output to match a grammar
    # This guarantees valid JSON, specific formats, etc.
    
    extends NobodyWhoChat
    
    # Define response format
    const RESPONSE_GRAMMAR = """
    root ::= action
    action ::= '{"speech": "' speech '", "action": "' action_type '"}'
    speech ::= [^"]+
    action_type ::= "none" | "give_item" | "open_shop" | "attack"
    """
    
    func _ready():
        # Set grammar constraint
        grammar = RESPONSE_GRAMMAR
    
    func _on_message_received(response: String):
        # Response is guaranteed valid JSON matching grammar
        var data = JSON.parse_string(response)
    
        if data:
            # Show the speech
            show_dialogue(data.speech)
    
            # Execute the action
            match data.action:
                "give_item":
                    give_item_to_player()
                "open_shop":
                    open_shop_interface()
                "attack":
                    become_hostile()
    

---
  #### **Name**
Conversation Persistence Across Scenes
  #### **Description**
Save and restore NPC conversations when changing scenes
  #### **When**
Player leaves area and returns, expecting NPC to remember
  #### **Example**
    # Autoload: ConversationManager.gd
    extends Node
    
    # Store conversation state per NPC
    var conversations: Dictionary = {}
    
    func save_conversation(npc_id: String, chat: NobodyWhoChat):
        conversations[npc_id] = {
            "messages": chat.get_messages(),
            "key_facts": extract_key_facts(chat)
        }
    
    func restore_conversation(npc_id: String, chat: NobodyWhoChat):
        if npc_id in conversations:
            var data = conversations[npc_id]
            chat.set_messages(data.messages)
    
    func extract_key_facts(chat: NobodyWhoChat) -> Dictionary:
        # Parse conversation for important facts
        var facts = {}
        for msg in chat.get_messages():
            if "my name is" in msg.content.to_lower():
                var name = extract_name(msg.content)
                if name:
                    facts["player_name"] = name
        return facts
    
    # Save on scene exit
    func _on_area_exit(npc: Node):
        var chat = npc.get_node("NobodyWhoChat")
        save_conversation(npc.get_meta("npc_id"), chat)
    
    # Restore on scene enter
    func _on_npc_ready(npc: Node):
        var chat = npc.get_node("NobodyWhoChat")
        restore_conversation(npc.get_meta("npc_id"), chat)
    

---
  #### **Name**
Model Preloading During Loading Screen
  #### **Description**
Load LLM model during loading screen to avoid in-game freeze
  #### **When**
Game has loading screens between major transitions
  #### **Example**
    # LoadingScreen.gd
    extends Control
    
    @onready var progress_bar: ProgressBar = $ProgressBar
    @onready var status_label: Label = $StatusLabel
    
    var model_loaded: bool = false
    
    func _ready():
        # Start loading sequence
        load_game_assets()
    
    func load_game_assets():
        status_label.text = "Loading assets..."
        progress_bar.value = 0
    
        # Load regular assets
        await load_textures()
        progress_bar.value = 30
    
        await load_audio()
        progress_bar.value = 50
    
        # Load LLM model (takes longest)
        status_label.text = "Loading AI..."
        await load_llm_model()
        progress_bar.value = 90
    
        status_label.text = "Initializing..."
        await get_tree().create_timer(0.5).timeout
        progress_bar.value = 100
    
        # Transition to game
        get_tree().change_scene_to_file("res://scenes/main.tscn")
    
    func load_llm_model():
        var model = NobodyWhoModel.new()
        model.model_file = "res://ai/models/qwen-3b-q4.gguf"
        add_child(model)
    
        # NobodyWho loads async, wait for ready
        while not model.is_ready():
            await get_tree().process_frame
    
        # Move to Global autoload
        remove_child(model)
        Global.model = model
        Global.add_child(model)
    

## Anti-Patterns


---
  #### **Name**
Separate Model Per NPC
  #### **Description**
Creating a new NobodyWhoModel for each NPC
  #### **Why**
Each Model loads the full model into RAM. 5 NPCs = 5x memory = crash.
  #### **Instead**
Create one NobodyWhoModel in autoload, point multiple NobodyWhoChat nodes to it.

---
  #### **Name**
Blocking on Response
  #### **Description**
Using await directly on say() in gameplay code
  #### **Why**
Even with await, blocking during active gameplay feels laggy. Use signals for UI update.
  #### **Instead**
Connect to message_received signal, show thinking indicator, handle response in callback.

---
  #### **Name**
Ignoring Grammar Constraints
  #### **Description**
Hoping LLM outputs valid JSON or specific formats
  #### **Why**
LLMs can and will output invalid JSON. One parse error breaks your game logic.
  #### **Instead**
Use NobodyWho's grammar feature to guarantee output format.

---
  #### **Name**
Model Loading in _ready()
  #### **Description**
Loading LLM model when scene loads without feedback
  #### **Why**
Model loading takes 2-10 seconds. Scene appears frozen with no explanation.
  #### **Instead**
Load during dedicated loading screen with progress indication.

---
  #### **Name**
Forgetting Conversations
  #### **Description**
Not persisting NPC conversation state between scenes
  #### **Why**
Player leaves and returns, NPC has amnesia. Breaks immersion immediately.
  #### **Instead**
Save conversation in autoload, restore when NPC scene loads.

---
  #### **Name**
Testing Only on Linux
  #### **Description**
Developing on Linux without testing Windows/macOS exports
  #### **Why**
NobodyWho has platform-specific native libraries. Export issues only appear in exports.
  #### **Instead**
Test exports on all target platforms early in development.