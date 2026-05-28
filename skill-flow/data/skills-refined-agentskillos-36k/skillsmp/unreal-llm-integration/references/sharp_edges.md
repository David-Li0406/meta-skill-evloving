# Unreal Llm Integration - Sharp Edges

## Gamethread Blocking

### **Id**
gamethread-blocking
### **Summary**
HTTP requests or JSON parsing blocking the game thread
### **Severity**
critical
### **Situation**
Game hitches or freezes when NPC dialogue triggers
### **Why**
  Unreal is strict about game thread blocking. Any stall over 33ms causes
  visible hitching. Synchronous HTTP blocks for 100-3000ms.
  
### **Solution**
  # WRONG: Synchronous request
  FString Response = FHttpModule::Get().BlockingRequest(URL);
  
  # RIGHT: Async with delegate
  TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
  Request->OnProcessRequestComplete().BindUObject(
      this, &UMyClass::OnRequestComplete);
  Request->ProcessRequest();
  
  void OnRequestComplete(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess)
  {
      // Handle on game thread via AsyncTask
      AsyncTask(ENamedThreads::GameThread, [this, Response]()
      {
          ProcessLLMResponse(Response->GetContentAsString());
      });
  }
  
### **Symptoms**
  - Frame time spikes in profiler
  - Visible game hitching
  - Console certification failure
### **Detection Pattern**
BlockingRequest|WaitFor|GetContentAsString.*return

## Blueprint Json Hell

### **Id**
blueprint-json-hell
### **Summary**
Complex JSON parsing done entirely in Blueprint
### **Severity**
high
### **Situation**
Massive Blueprint spaghetti for parsing LLM responses
### **Why**
  Blueprint JSON nodes are verbose. Error handling is difficult.
  Nested structures become unmaintainable. Any API change breaks everything.
  
### **Solution**
  // Create C++ wrapper that exposes clean struct
  USTRUCT(BlueprintType)
  struct FNPCDialogueResponse
  {
      UPROPERTY(BlueprintReadOnly)
      FString Speech;
  
      UPROPERTY(BlueprintReadOnly)
      ENPCAction Action;
  
      UPROPERTY(BlueprintReadOnly)
      float Emotion;
  };
  
  // Parse JSON in C++, return struct
  FNPCDialogueResponse ULLMParser::ParseResponse(const FString& JsonString)
  {
      TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);
      // ... parsing logic
      return Response;
  }
  
  // Blueprint just uses the clean struct
  
### **Symptoms**
  - Massive Blueprint graphs
  - JSON parse errors at runtime
  - Hard to modify response format
### **Detection Pattern**
JsonObject|GetField|TryGetField

## Console Offline Failure

### **Id**
console-offline-failure
### **Summary**
Game crashes or breaks when console is offline
### **Severity**
high
### **Situation**
Cloud API fails, game has no fallback
### **Why**
  Consoles may be offline. Cloud APIs fail. Certification requires graceful
  handling. Players in rural areas have poor connectivity.
  
### **Solution**
  # Always implement fallback
  void UDialogueSystem::GetResponse(const FString& Input)
  {
      if (IsNetworkAvailable())
      {
          SendLLMRequest(Input);
      }
      else
      {
          // Use cached/scripted responses
          FString Fallback = GetFallbackResponse(Input);
          OnResponseReceived.Broadcast(Fallback);
      }
  }
  
  // Cache responses for common inputs
  // Pre-generate key dialogues at development time
  
### **Symptoms**
  - Crash when offline
  - Infinite loading on poor connection
  - Failed console certification
### **Detection Pattern**
PLATFORM_XBOX|PLATFORM_PS5|IsNetworkAvailable

## Metahuman Lip Sync Mismatch

### **Id**
metahuman-lip-sync-mismatch
### **Summary**
LLM response doesn't match MetaHuman lip sync
### **Severity**
medium
### **Situation**
MetaHuman mouths words that don't match dialogue text
### **Why**
  LLM generates text, but audio/lip sync needs to match.
  TTS latency adds to total response time.
  Streaming text + audio is complex.
  
### **Solution**
  # Option 1: Generate audio first, then play
  async void ProcessDialogue(FString Text)
  {
      // Generate audio from text
      FAudioData Audio = await TTSService->Generate(Text);
  
      // Play audio with lip sync
      MetaHuman->PlayAudioWithLipSync(Audio);
  
      // Show text in sync with audio
      SubtitleWidget->ShowText(Text);
  }
  
  # Option 2: Pre-generate common dialogues
  # Build time: Generate audio for scripted responses
  # Runtime: Only use LLM for unexpected inputs
  
### **Symptoms**
  - Lip sync doesn't match audio
  - Long delay before speech starts
  - Audio/text timing mismatch
### **Detection Pattern**
MetaHuman|LipSync|TTS