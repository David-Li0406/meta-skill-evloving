# Unreal Engine LLM Integration

## Patterns


---
  #### **Name**
Async HTTP LLM Request
  #### **Description**
Non-blocking HTTP request to LLM API in Unreal
  #### **When**
Basic LLM integration using cloud API
  #### **Example**
    // C++ - AsyncLLMRequest.h
    UCLASS(BlueprintType)
    class UAsyncLLMRequest : public UBlueprintAsyncActionBase
    {
        GENERATED_BODY()
    
    public:
        UPROPERTY(BlueprintAssignable)
        FOnLLMResponseReceived OnSuccess;
    
        UPROPERTY(BlueprintAssignable)
        FOnLLMRequestFailed OnFailed;
    
        UFUNCTION(BlueprintCallable, meta = (BlueprintInternalUseOnly = "true"))
        static UAsyncLLMRequest* SendLLMRequest(
            const FString& Prompt,
            const FString& SystemPrompt);
    
        virtual void Activate() override;
    
    private:
        void HandleResponse(FHttpRequestPtr Request,
                            FHttpResponsePtr Response,
                            bool bSuccess);
    
        FString Prompt;
        FString SystemPrompt;
    };
    
    // Usage in Blueprint:
    // - Drag out from "Send LLM Request"
    // - Connect to OnSuccess and OnFailed events
    // - Non-blocking, game continues while request processes
    

---
  #### **Name**
Dialogue Queue System
  #### **Description**
Queue multiple dialogue requests to prevent overlapping
  #### **When**
Multiple NPCs or rapid player input
  #### **Example**
    // Dialogue Queue Manager
    UCLASS()
    class UDialogueQueueManager : public UActorComponent
    {
        GENERATED_BODY()
    
    private:
        TQueue<FDialogueRequest> RequestQueue;
        bool bIsProcessing = false;
    
    public:
        void QueueDialogue(AActor* NPC, const FString& PlayerInput);
    
    private:
        void ProcessNextRequest();
        void OnRequestComplete(const FString& Response);
    };
    
    // Prevents multiple simultaneous requests
    // Ensures responses arrive in order
    // Shows thinking indicator while queued
    

## Anti-Patterns


---
  #### **Name**
Blocking HTTP Requests
  #### **Description**
Using synchronous HTTP in Blueprint or C++
  #### **Why**
Freezes game, causes hitching, fails console certification
  #### **Instead**
Use FHttpModule async, UAsyncActionBase, or delegates

---
  #### **Name**
Blueprint JSON Parsing
  #### **Description**
Complex JSON manipulation in Blueprint nodes
  #### **Why**
Verbose, error-prone, hard to maintain
  #### **Instead**
Parse JSON in C++, expose clean structs to Blueprint

---
  #### **Name**
Ignoring Console Requirements
  #### **Description**
Not considering offline/certification scenarios
  #### **Why**
Console builds fail cert, game doesn't work offline
  #### **Instead**
Plan for offline fallbacks from the start