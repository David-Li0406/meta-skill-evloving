# Unreal Engine Development

## Patterns


---
  #### **Name**
Actor Component Architecture
  #### **Description**
Use Actor Components for reusable, composable functionality
  #### **When**
Adding behavior or data to Actors without deep inheritance hierarchies
  #### **Example**
    // Health component - reusable across any Actor
    UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
    class MYGAME_API UHealthComponent : public UActorComponent
    {
        GENERATED_BODY()
    
    public:
        UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Health")
        float MaxHealth = 100.f;
    
        UPROPERTY(ReplicatedUsing = OnRep_CurrentHealth, BlueprintReadOnly, Category = "Health")
        float CurrentHealth;
    
        UFUNCTION()
        void OnRep_CurrentHealth();
    
        UFUNCTION(BlueprintCallable, Category = "Health")
        void TakeDamage(float DamageAmount, AActor* DamageCauser);
    
        UPROPERTY(BlueprintAssignable, Category = "Health")
        FOnHealthChanged OnHealthChanged;
    
        UPROPERTY(BlueprintAssignable, Category = "Health")
        FOnDeath OnDeath;
    
        virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;
    };
    
    // Usage in any Actor:
    // Just add the component - no inheritance needed
    HealthComponent = CreateDefaultSubobject<UHealthComponent>(TEXT("HealthComponent"));
    

---
  #### **Name**
Gameplay Framework Separation
  #### **Description**
Respect the role of GameMode, GameState, PlayerState, PlayerController, Pawn
  #### **When**
Designing multiplayer-ready game architecture
  #### **Example**
    // GameMode - Server-only authority, game rules
    // Only exists on server, controls match flow
    class AMyGameMode : public AGameModeBase
    {
        void HandleMatchStart();
        void HandlePlayerDeath(AController* DeadPlayer, AController* Killer);
        bool CanRespawn(AController* Player);
    };
    
    // GameState - Replicated to all, game-wide state
    class AMyGameState : public AGameStateBase
    {
        UPROPERTY(Replicated)
        int32 TeamAScore;
    
        UPROPERTY(Replicated)
        float MatchTimeRemaining;
    };
    
    // PlayerState - Per-player, replicated to all
    class AMyPlayerState : public APlayerState
    {
        UPROPERTY(Replicated)
        int32 Kills;
    
        UPROPERTY(Replicated)
        int32 Deaths;
    
        UPROPERTY(Replicated)
        ETeam Team;
    };
    
    // PlayerController - Per-player, partially replicated
    // Handles input, UI, camera
    class AMyPlayerController : public APlayerController
    {
        void SetupInputComponent();
        void ShowGameOverUI();
    };
    
    // Pawn/Character - The physical representation
    class AMyCharacter : public ACharacter
    {
        void Move(const FInputActionValue& Value);
        void Attack();
    };
    

---
  #### **Name**
Subsystem Pattern
  #### **Description**
Use Subsystems for global game systems without singletons
  #### **When**
Needing game-wide managers that respect Engine lifecycles
  #### **Example**
    // Game Instance Subsystem - Lives for entire game session
    UCLASS()
    class MYGAME_API USaveGameSubsystem : public UGameInstanceSubsystem
    {
        GENERATED_BODY()
    
    public:
        virtual void Initialize(FSubsystemCollectionBase& Collection) override;
        virtual void Deinitialize() override;
    
        UFUNCTION(BlueprintCallable)
        void SaveGame();
    
        UFUNCTION(BlueprintCallable)
        void LoadGame();
    
    private:
        UPROPERTY()
        USaveGame* CurrentSaveGame;
    };
    
    // World Subsystem - Per-world, respects level changes
    UCLASS()
    class MYGAME_API UQuestSubsystem : public UWorldSubsystem
    {
        GENERATED_BODY()
    
    public:
        virtual void OnWorldBeginPlay(UWorld& InWorld) override;
    
        UFUNCTION(BlueprintCallable)
        void StartQuest(FName QuestId);
    
        UFUNCTION(BlueprintCallable)
        bool IsQuestComplete(FName QuestId) const;
    };
    
    // Access from anywhere:
    UGameInstance* GI = GetGameInstance();
    USaveGameSubsystem* SaveSystem = GI->GetSubsystem<USaveGameSubsystem>();
    SaveSystem->SaveGame();
    
    // Or from World:
    UQuestSubsystem* QuestSystem = GetWorld()->GetSubsystem<UQuestSubsystem>();
    

---
  #### **Name**
Gameplay Ability System Setup
  #### **Description**
GAS for complex ability/skill systems with prediction and replication
  #### **When**
Building action games with abilities, cooldowns, effects, and multiplayer support
  #### **Example**
    // 1. AbilitySystemComponent on your character
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Abilities")
    UAbilitySystemComponent* AbilitySystemComponent;
    
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Abilities")
    UMyAttributeSet* AttributeSet;
    
    // 2. Attribute Set for stats
    UCLASS()
    class MYGAME_API UMyAttributeSet : public UAttributeSet
    {
        GENERATED_BODY()
    
    public:
        UPROPERTY(BlueprintReadOnly, Category = "Attributes", ReplicatedUsing = OnRep_Health)
        FGameplayAttributeData Health;
        ATTRIBUTE_ACCESSORS(UMyAttributeSet, Health)
    
        UPROPERTY(BlueprintReadOnly, Category = "Attributes", ReplicatedUsing = OnRep_MaxHealth)
        FGameplayAttributeData MaxHealth;
        ATTRIBUTE_ACCESSORS(UMyAttributeSet, MaxHealth)
    
        UPROPERTY(BlueprintReadOnly, Category = "Attributes", ReplicatedUsing = OnRep_Mana)
        FGameplayAttributeData Mana;
        ATTRIBUTE_ACCESSORS(UMyAttributeSet, Mana)
    
        virtual void PreAttributeChange(const FGameplayAttribute& Attribute, float& NewValue) override;
        virtual void PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data) override;
    };
    
    // 3. Gameplay Ability
    UCLASS()
    class MYGAME_API UGA_Fireball : public UGameplayAbility
    {
        GENERATED_BODY()
    
    public:
        UGA_Fireball();
    
        virtual void ActivateAbility(...) override;
        virtual void EndAbility(...) override;
        virtual bool CanActivateAbility(...) const override;
    
        UPROPERTY(EditDefaultsOnly, Category = "Damage")
        TSubclassOf<UGameplayEffect> DamageEffect;
    
        UPROPERTY(EditDefaultsOnly, Category = "Damage")
        float BaseDamage = 50.f;
    };
    

---
  #### **Name**
Enhanced Input System
  #### **Description**
Data-driven input with contexts and modifiers
  #### **When**
Any player input handling in UE5+
  #### **Example**
    // Input Action asset (create in editor)
    // IA_Move, IA_Look, IA_Jump, IA_Attack
    
    // Input Mapping Context (create in editor)
    // IMC_Default - maps keys to actions
    
    // In PlayerController or Character
    void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
    {
        Super::SetupPlayerInputComponent(PlayerInputComponent);
    
        if (UEnhancedInputComponent* EnhancedInput = Cast<UEnhancedInputComponent>(PlayerInputComponent))
        {
            // Bind actions
            EnhancedInput->BindAction(IA_Move, ETriggerEvent::Triggered, this, &AMyCharacter::Move);
            EnhancedInput->BindAction(IA_Look, ETriggerEvent::Triggered, this, &AMyCharacter::Look);
            EnhancedInput->BindAction(IA_Jump, ETriggerEvent::Started, this, &AMyCharacter::StartJump);
            EnhancedInput->BindAction(IA_Jump, ETriggerEvent::Completed, this, &AMyCharacter::StopJump);
        }
    
        // Add mapping context
        if (APlayerController* PC = Cast<APlayerController>(GetController()))
        {
            if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PC->GetLocalPlayer()))
            {
                Subsystem->AddMappingContext(DefaultMappingContext, 0);
            }
        }
    }
    
    void AMyCharacter::Move(const FInputActionValue& Value)
    {
        FVector2D MovementVector = Value.Get<FVector2D>();
        // Apply movement
    }
    

---
  #### **Name**
Proper Replication Setup
  #### **Description**
Network replication with authority checks and RPCs
  #### **When**
Building multiplayer games
  #### **Example**
    // Header
    UCLASS()
    class MYGAME_API AMyWeapon : public AActor
    {
        GENERATED_BODY()
    
    public:
        // Replicated property with RepNotify
        UPROPERTY(ReplicatedUsing = OnRep_AmmoCount)
        int32 AmmoCount;
    
        UFUNCTION()
        void OnRep_AmmoCount();
    
        // Server RPC - client requests, server executes
        UFUNCTION(Server, Reliable, WithValidation)
        void Server_Fire(FVector_NetQuantize TargetLocation);
    
        // Client RPC - server tells specific client
        UFUNCTION(Client, Reliable)
        void Client_PlayHitMarker();
    
        // Multicast RPC - server tells all clients
        UFUNCTION(NetMulticast, Unreliable)
        void Multicast_PlayFireEffect();
    
        virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;
    };
    
    // Implementation
    void AMyWeapon::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
    {
        Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    
        DOREPLIFETIME(AMyWeapon, AmmoCount);
        // Or with conditions:
        DOREPLIFETIME_CONDITION(AMyWeapon, AmmoCount, COND_OwnerOnly);
    }
    
    void AMyWeapon::Fire()
    {
        if (!HasAuthority())
        {
            // Client - request server to fire
            Server_Fire(GetTargetLocation());
            // Local prediction for responsiveness
            PlayLocalFireEffects();
            return;
        }
    
        // Server - actually fire
        AmmoCount--;
        SpawnProjectile();
        Multicast_PlayFireEffect();
    }
    
    bool AMyWeapon::Server_Fire_Validate(FVector_NetQuantize TargetLocation)
    {
        // Cheat detection
        return AmmoCount > 0;
    }
    
    void AMyWeapon::Server_Fire_Implementation(FVector_NetQuantize TargetLocation)
    {
        Fire();
    }
    

---
  #### **Name**
Async Asset Loading
  #### **Description**
Load assets without blocking the game thread
  #### **When**
Loading assets at runtime, level streaming, reducing memory footprint
  #### **Example**
    // Soft object pointers for on-demand loading
    UPROPERTY(EditAnywhere, Category = "Assets")
    TSoftObjectPtr<UStaticMesh> WeaponMesh;
    
    UPROPERTY(EditAnywhere, Category = "Assets")
    TSoftClassPtr<AActor> EnemyClass;
    
    // Async loading
    void AMyActor::LoadWeaponAsync()
    {
        if (WeaponMesh.IsNull())
        {
            UE_LOG(LogTemp, Warning, TEXT("WeaponMesh is null!"));
            return;
        }
    
        // Check if already loaded
        if (WeaponMesh.IsValid())
        {
            OnWeaponMeshLoaded();
            return;
        }
    
        // Async load
        FStreamableManager& StreamableManager = UAssetManager::GetStreamableManager();
        StreamableManager.RequestAsyncLoad(
            WeaponMesh.ToSoftObjectPath(),
            FStreamableDelegate::CreateUObject(this, &AMyActor::OnWeaponMeshLoaded)
        );
    }
    
    void AMyActor::OnWeaponMeshLoaded()
    {
        UStaticMesh* LoadedMesh = WeaponMesh.Get();
        if (LoadedMesh)
        {
            MeshComponent->SetStaticMesh(LoadedMesh);
        }
    }
    
    // Bulk async loading
    TArray<FSoftObjectPath> AssetsToLoad;
    AssetsToLoad.Add(WeaponMesh.ToSoftObjectPath());
    AssetsToLoad.Add(EnemyClass.ToSoftObjectPath());
    
    StreamableManager.RequestAsyncLoad(AssetsToLoad,
        FStreamableDelegate::CreateLambda([this]()
        {
            UE_LOG(LogTemp, Log, TEXT("All assets loaded!"));
        })
    );
    

## Anti-Patterns


---
  #### **Name**
Tick Abuse
  #### **Description**
Putting everything in Tick when events or timers would work
  #### **Why**
Tick runs every frame. 1000 actors ticking = 1000 function calls per frame. Performance dies.
  #### **Instead**
Use timers, events, delegates. Only Tick what truly needs per-frame updates.

---
  #### **Name**
Blueprint Spaghetti
  #### **Description**
Complex logic in a single massive Blueprint graph
  #### **Why**
Impossible to debug, can't diff/merge, execution flow unclear, performance tanks.
  #### **Instead**
Break into Blueprint functions, use C++ for complex logic, Blueprint Interfaces for communication.

---
  #### **Name**
Inheritance Over Composition
  #### **Description**
Deep Actor inheritance hierarchies instead of components
  #### **Why**
Inflexible, code duplication, diamond problem, harder to reuse functionality.
  #### **Instead**
Use Actor Components. A "HealthComponent" beats "DamageableActor" base class.

---
  #### **Name**
Ignoring UPROPERTY
  #### **Description**
Raw pointers to UObjects without UPROPERTY macro
  #### **Why**
Garbage collector doesn't know about them. Dangling pointers. Crashes. Memory leaks.
  #### **Instead**
Always UPROPERTY() for UObject pointers. TWeakObjectPtr for non-owning references.

---
  #### **Name**
Hard Asset References
  #### **Description**
Direct references to assets causing everything to load at once
  #### **Why**
Massive memory usage. Long load times. Everything loads even if unused.
  #### **Instead**
Use TSoftObjectPtr/TSoftClassPtr. Load assets on demand. Asset Manager for bundles.

---
  #### **Name**
Fighting the Gameplay Framework
  #### **Description**
Ignoring GameMode/GameState/PlayerState/PlayerController architecture
  #### **Why**
Replication breaks. Authority confusion. Reinventing what Engine provides.
  #### **Instead**
Learn and use the framework. It exists for good reasons, especially multiplayer.

---
  #### **Name**
Hot Reload Trust
  #### **Description**
Testing gameplay with hot reload instead of proper restarts
  #### **Why**
Hot reload is unstable. State corrupts. Blueprints break. Real bugs hide.
  #### **Instead**
Restart editor for real testing. Hot reload only for quick iteration.

---
  #### **Name**
Multicast RPC Spam
  #### **Description**
Sending multicast RPCs every frame instead of replicating state
  #### **Why**
Bandwidth explosion. Late-joiners miss state. Server overload.
  #### **Instead**
Replicate state with RepNotify. Multicast only for transient effects.

---
  #### **Name**
GetAllActorsOfClass in Tick
  #### **Description**
Finding actors dynamically every frame
  #### **Why**
O(n) scan every frame. Performance killer at scale.
  #### **Instead**
Cache references at BeginPlay. Use events to track spawns/destroys.

---
  #### **Name**
Ignoring Actor Lifecycle
  #### **Description**
Accessing components in constructor that don't exist yet
  #### **Why**
Constructor runs before components are created. Crashes. Undefined behavior.
  #### **Instead**
Use PostInitializeComponents for component access, BeginPlay for gameplay logic.