# Unreal Engine - Sharp Edges

## Uproperty Missing

### **Id**
uproperty-missing
### **Summary**
UObject pointers without UPROPERTY macro cause garbage collection crashes
### **Severity**
critical
### **Situation**
Raw pointers to UObjects in C++ classes without UPROPERTY decoration
### **Why**
  Unreal's garbage collector only tracks objects referenced by UPROPERTY pointers.
  Raw pointers become dangling when GC collects the object. Game crashes randomly.
  Debugging is nightmare because crash timing depends on GC timing.
  
### **Solution**
  // WRONG: Raw pointer - GC doesn't see this
  UStaticMesh* MyMesh;
  AActor* MyTarget;
  
  // RIGHT: UPROPERTY tells GC about this reference
  UPROPERTY()
  UStaticMesh* MyMesh;
  
  UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat")
  AActor* MyTarget;
  
  // For non-owning references that shouldn't prevent GC:
  UPROPERTY()
  TWeakObjectPtr<AActor> WeakTarget;
  
  // Check weak pointer before use:
  if (WeakTarget.IsValid())
  {
      WeakTarget->DoSomething();
  }
  
  // For arrays:
  UPROPERTY()
  TArray<UObject*> MyObjects;  // GC tracks all elements
  
### **Symptoms**
  - Random crashes during gameplay
  - Crashes after level transitions
  - Crashes during PIE sessions
  - Access violation in GC functions
  - IsValid() returns false unexpectedly
### **Detection Pattern**
^\s*(UObject|AActor|UActorComponent|USceneComponent|UPrimitiveComponent|UMeshComponent|UStaticMeshComponent|USkeletalMeshComponent|UTexture|UMaterial|USoundBase|UAnimInstance)\*\s+\w+\s*[;=](?!.*UPROPERTY)

## Tick Abuse

### **Id**
tick-abuse
### **Summary**
Overusing Tick for logic that should be event-driven
### **Severity**
critical
### **Situation**
Checking conditions every frame, polling for state changes in Tick
### **Why**
  Tick runs every frame for every ticking actor. 500 enemies checking distance
  to player = 500 calculations per frame. At 60 FPS that's 30,000 checks/second.
  Performance collapses. CPU bound. Frame rate tanks.
  
### **Solution**
  // WRONG: Checking distance every frame
  void AEnemy::Tick(float DeltaTime)
  {
      Super::Tick(DeltaTime);
      if (FVector::Dist(GetActorLocation(), Player->GetActorLocation()) < 1000.f)
      {
          StartChasing();
      }
  }
  
  // RIGHT: Use timers for periodic checks
  void AEnemy::BeginPlay()
  {
      Super::BeginPlay();
      GetWorld()->GetTimerManager().SetTimer(
          PerceptionTimerHandle,
          this,
          &AEnemy::CheckForPlayer,
          0.5f,  // Every 0.5 seconds, not every frame
          true
      );
  }
  
  // BETTER: Use perception system
  UPROPERTY(VisibleAnywhere)
  UAIPerceptionComponent* PerceptionComponent;
  
  void AEnemy::OnTargetPerceived(AActor* Actor, FAIStimulus Stimulus)
  {
      if (Stimulus.WasSuccessfullySensed())
      {
          StartChasing(Actor);
      }
  }
  
  // BEST: Disable tick entirely when not needed
  AEnemy::AEnemy()
  {
      PrimaryActorTick.bCanEverTick = false;
      // Or dynamically:
      // SetActorTickEnabled(false);
  }
  
### **Symptoms**
  - Frame rate drops with more actors
  - High CPU usage
  - Game hitches during gameplay
  - Profiler shows Tick dominating frame
### **Detection Pattern**
Tick\s*\([^)]*\)\s*\{[^}]*(GetAllActors|FindActor|FVector::Dist|GetActorLocation\(\).*GetActorLocation\(\))

## Hot Reload Corruption

### **Id**
hot-reload-corruption
### **Summary**
Trusting hot reload for testing gameplay changes
### **Severity**
high
### **Situation**
Making C++ changes and testing with hot reload instead of restarting editor
### **Why**
  Hot reload corrupts Blueprint state, breaks serialization, causes random crashes.
  CDO (Class Default Object) gets out of sync. Properties don't update correctly.
  You'll waste hours debugging phantom bugs that don't exist after restart.
  
### **Solution**
  # Development workflow:
  1. Use Live Coding (Ctrl+Alt+F11) for code-only changes - safer than hot reload
  2. ALWAYS restart editor before:
     - Testing gameplay that will be saved
     - Recording videos/screenshots
     - Bug hunting
     - Shipping builds
  
  # In Editor Preferences:
  Editor Preferences > General > Live Coding > Enable Live Coding
  
  # If you must use hot reload:
  1. Save all assets first
  2. Don't trust the results
  3. Restart before any real testing
  
  # Consider:
  - Separate gameplay testing PIE instance
  - Fast iteration with Blueprints for logic
  - C++ for systems, Blueprints for tuning
  
### **Symptoms**
  - Blueprints stop working correctly
  - Property values reset randomly
  - "Blueprint could not be loaded" errors
  - Crashes on PIE after compile
  - Values in editor don't match runtime
### **Detection Pattern**


## Replication Authority Confusion

### **Id**
replication-authority-confusion
### **Summary**
Not checking HasAuthority() before modifying replicated state
### **Severity**
critical
### **Situation**
Modifying replicated properties on clients, expecting it to work
### **Why**
  Only the server has authority over replicated state. Client changes are
  overwritten on next replication. Causes desyncs, rubber-banding, and
  seemingly random behavior. Multiplayer breaks in subtle ways.
  
### **Solution**
  // WRONG: Modifying without authority check
  void AMyActor::TakeDamage(float Damage)
  {
      Health -= Damage;  // Works on server, client changes get overwritten
  }
  
  // RIGHT: Authority checks
  void AMyActor::TakeDamage(float Damage)
  {
      if (HasAuthority())
      {
          Health -= Damage;  // Server modifies, replicates to clients
      }
      else
      {
          // Client - request server to apply damage
          Server_TakeDamage(Damage);
      }
  }
  
  UFUNCTION(Server, Reliable, WithValidation)
  void Server_TakeDamage(float Damage);
  
  bool AMyActor::Server_TakeDamage_Validate(float Damage)
  {
      return Damage >= 0.f && Damage < 10000.f;  // Sanity check
  }
  
  void AMyActor::Server_TakeDamage_Implementation(float Damage)
  {
      TakeDamage(Damage);  // Server applies it
  }
  
  // Common pattern: Role checks
  if (GetLocalRole() == ROLE_Authority)
  {
      // Server code
  }
  else if (GetLocalRole() == ROLE_AutonomousProxy)
  {
      // Owning client
  }
  else if (GetLocalRole() == ROLE_SimulatedProxy)
  {
      // Non-owning client
  }
  
### **Symptoms**
  - Player position rubber-banding
  - State changes don't persist
  - Different behavior on host vs client
  - "Desynced" gameplay feel
### **Detection Pattern**
(Health|Ammo|Score|Lives|Mana)\s*[-+]=(?!.*HasAuthority|.*ROLE_Authority)

## Hard Asset References

### **Id**
hard-asset-references
### **Summary**
Hard references causing massive memory usage and load times
### **Severity**
high
### **Situation**
Direct UPROPERTY references to assets instead of soft references
### **Why**
  Hard references load the asset immediately when the referencing object loads.
  An Actor referencing 100 meshes loads ALL of them even if only 1 is used.
  Memory explodes. Load times increase. Every reference chains to more assets.
  
### **Solution**
  // WRONG: Hard reference - loads immediately
  UPROPERTY(EditAnywhere)
  UStaticMesh* WeaponMesh;
  
  UPROPERTY(EditAnywhere)
  TSubclassOf<AActor> EnemyClass;
  
  // RIGHT: Soft reference - loads on demand
  UPROPERTY(EditAnywhere)
  TSoftObjectPtr<UStaticMesh> WeaponMesh;
  
  UPROPERTY(EditAnywhere)
  TSoftClassPtr<AActor> EnemyClass;
  
  // Check and load when needed
  if (!WeaponMesh.IsNull())
  {
      if (WeaponMesh.IsValid())
      {
          // Already loaded
          UseWeapon(WeaponMesh.Get());
      }
      else
      {
          // Need to load
          UStaticMesh* LoadedMesh = WeaponMesh.LoadSynchronous();
          // Or async - see pattern in skill.yaml
      }
  }
  
  // For class references:
  if (EnemyClass.IsValid())
  {
      UClass* LoadedClass = EnemyClass.Get();
      GetWorld()->SpawnActor(LoadedClass, ...);
  }
  
### **Symptoms**
  - Long level load times
  - High memory usage
  - Editor opens slowly
  - "Reference Viewer" shows everything connected
### **Detection Pattern**
UPROPERTY\([^)]*\)\s*(UStaticMesh|USkeletalMesh|UTexture2D|UMaterialInterface|USoundBase|UAnimMontage)\*

## Constructor Component Access

### **Id**
constructor-component-access
### **Summary**
Accessing components in constructor before they exist
### **Severity**
high
### **Situation**
Trying to use components in the Actor constructor
### **Why**
  Actor constructor runs before CreateDefaultSubobject components are fully initialized.
  The World doesn't exist yet. Many systems aren't ready. Crashes or undefined behavior.
  
### **Solution**
  // WRONG: Accessing World in constructor
  AMyActor::AMyActor()
  {
      MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
  
      // These WILL crash or fail:
      GetWorld()->SpawnActor(...);  // World doesn't exist
      FindActor<APlayerController>();  // Nothing exists yet
      MeshComponent->SetWorldLocation(...);  // No world transform yet
  }
  
  // RIGHT: Lifecycle-aware initialization
  AMyActor::AMyActor()
  {
      // Only create subobjects and set defaults
      MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
      MeshComponent->SetupAttachment(RootComponent);
      // Set default values on components - OK
      MeshComponent->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
  }
  
  void AMyActor::PostInitializeComponents()
  {
      Super::PostInitializeComponents();
      // Components are fully created and initialized
      // Can access component properties safely
      MeshComponent->SetRelativeLocation(FVector(0, 0, 100));
  }
  
  void AMyActor::BeginPlay()
  {
      Super::BeginPlay();
      // World exists, all actors spawned, gameplay can start
      PlayerRef = GetWorld()->GetFirstPlayerController();
      InitializeGameplay();
  }
  
  // Lifecycle order:
  // 1. Constructor - create subobjects, set CDO defaults
  // 2. PostInitializeComponents - components ready
  // 3. BeginPlay - world ready, gameplay starts
  
### **Symptoms**
  - Crash in constructor
  - Null pointer exceptions
  - Components not initialized
  - GetWorld() returns nullptr
### **Detection Pattern**
AMyActor::AMyActor\(\)[^}]*(GetWorld\(\)|FindActor|SpawnActor|GetFirstPlayerController)

## Blueprint Cast Failure

### **Id**
blueprint-cast-failure
### **Summary**
Not handling failed Blueprint casts leading to crashes
### **Severity**
high
### **Situation**
Casting without checking result in Blueprints or C++
### **Why**
  Cast can return nullptr if types don't match. Using the result without checking
  causes access violation. Blueprints show "Accessed None" error. Game crashes.
  
### **Solution**
  // WRONG: Unchecked cast
  void AMyActor::OnOverlap(AActor* OtherActor)
  {
      AMyCharacter* Character = Cast<AMyCharacter>(OtherActor);
      Character->TakeDamage(10);  // Crash if OtherActor isn't AMyCharacter
  }
  
  // RIGHT: Check cast result
  void AMyActor::OnOverlap(AActor* OtherActor)
  {
      if (AMyCharacter* Character = Cast<AMyCharacter>(OtherActor))
      {
          Character->TakeDamage(10);  // Safe
      }
  }
  
  // For interfaces:
  if (OtherActor->Implements<UDamageable>())
  {
      IDamageable::Execute_ApplyDamage(OtherActor, 10);
  }
  
  // CastChecked - crashes intentionally if cast fails (use only when guaranteed)
  AMyCharacter* Character = CastChecked<AMyCharacter>(OtherActor);
  
  // Blueprint: Always use "Cast" node with both exec pins
  // Connect the "Cast Failed" pin to handle the failure case
  
### **Symptoms**
  - "Accessed None" Blueprint errors
  - Random crashes on overlap/hit events
  - Crashes with mixed actor types
  - Works in test, crashes in play
### **Detection Pattern**
Cast<[^>]+>\([^)]+\)->

## Async Load Blocking

### **Id**
async-load-blocking
### **Summary**
Using LoadSynchronous on game thread causing hitches
### **Severity**
high
### **Situation**
Synchronously loading assets during gameplay
### **Why**
  LoadSynchronous blocks the game thread. Loading a large mesh = frame hitch.
  Loading multiple assets = unplayable stuttering. Players notice frame drops.
  
### **Solution**
  // WRONG: Blocking load during gameplay
  void AWeapon::EquipAttachment(TSoftObjectPtr<UStaticMesh> AttachmentMesh)
  {
      UStaticMesh* Mesh = AttachmentMesh.LoadSynchronous();  // Game freezes
      MeshComponent->SetStaticMesh(Mesh);
  }
  
  // RIGHT: Async loading
  void AWeapon::EquipAttachment(TSoftObjectPtr<UStaticMesh> AttachmentMesh)
  {
      if (AttachmentMesh.IsValid())
      {
          // Already loaded
          MeshComponent->SetStaticMesh(AttachmentMesh.Get());
          return;
      }
  
      // Show loading indicator
      ShowLoadingIndicator();
  
      // Async load
      StreamableManager.RequestAsyncLoad(
          AttachmentMesh.ToSoftObjectPath(),
          FStreamableDelegate::CreateUObject(this, &AWeapon::OnAttachmentLoaded)
      );
  }
  
  void AWeapon::OnAttachmentLoaded()
  {
      HideLoadingIndicator();
      if (PendingAttachment.IsValid())
      {
          MeshComponent->SetStaticMesh(PendingAttachment.Get());
      }
  }
  
  // For level streaming:
  FLatentActionInfo LatentInfo;
  UGameplayStatics::LoadStreamLevel(this, LevelName, true, true, LatentInfo);
  
### **Symptoms**
  - Frame hitches when spawning enemies
  - Stuttering when picking up items
  - Freeze when entering new areas
  - Profiler shows loading on game thread
### **Detection Pattern**
LoadSynchronous\s*\(\s*\)(?!.*BeginPlay|.*PreloadAssets)

## Getallactors Spam

### **Id**
getallactors-spam
### **Summary**
Using GetAllActorsOfClass repeatedly instead of caching
### **Severity**
high
### **Situation**
Finding actors every frame or frequently during gameplay
### **Why**
  GetAllActorsOfClass iterates through all actors in the world every call.
  O(n) every frame = O(n * 60) per second. With 1000 actors this kills performance.
  
### **Solution**
  // WRONG: Finding every frame
  void AEnemyManager::Tick(float DeltaTime)
  {
      TArray<AActor*> Players;
      UGameplayStatics::GetAllActorsOfClass(GetWorld(), APlayerCharacter::StaticClass(), Players);
      for (AActor* Player : Players)
      {
          // Process each player
      }
  }
  
  // RIGHT: Cache at BeginPlay
  void AEnemyManager::BeginPlay()
  {
      Super::BeginPlay();
  
      // Cache players
      TArray<AActor*> FoundPlayers;
      UGameplayStatics::GetAllActorsOfClass(GetWorld(), APlayerCharacter::StaticClass(), FoundPlayers);
      for (AActor* Actor : FoundPlayers)
      {
          if (APlayerCharacter* Player = Cast<APlayerCharacter>(Actor))
          {
              CachedPlayers.Add(Player);
          }
      }
  
      // Subscribe to spawn events for new players
      GetWorld()->OnActorSpawned().AddUObject(this, &AEnemyManager::OnActorSpawned);
  }
  
  void AEnemyManager::OnActorSpawned(AActor* SpawnedActor)
  {
      if (APlayerCharacter* Player = Cast<APlayerCharacter>(SpawnedActor))
      {
          CachedPlayers.Add(Player);
      }
  }
  
  // Alternative: Use GameMode to track players
  // GameMode->GetNumPlayers()
  // GameState->PlayerArray
  
### **Symptoms**
  - CPU spike in GetAllActorsOfClass
  - Frame drops with more actors
  - Profiler shows actor iteration
### **Detection Pattern**
GetAllActorsOfClass.*Tick|Tick.*GetAllActorsOfClass

## Cooking Asset Issues

### **Id**
cooking-asset-issues
### **Summary**
Assets work in editor but fail in packaged build
### **Severity**
high
### **Situation**
Loading assets by path string that cooking doesn't include
### **Why**
  Editor loads anything. Packaged builds only include cooked assets.
  If asset isn't referenced by something that's cooked, it's not in the package.
  Path-based loading of unreferenced assets = crash in shipping build.
  
### **Solution**
  // WRONG: Path string loading of unreferenced asset
  UStaticMesh* Mesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Game/Meshes/SomeMesh.SomeMesh"));
  // Works in editor, fails in package if not referenced elsewhere
  
  // RIGHT: Soft reference ensures cooking
  UPROPERTY(EditAnywhere)
  TSoftObjectPtr<UStaticMesh> SomeMesh;
  // Asset is referenced, will be cooked
  
  // For runtime path loading, ensure cooking:
  // 1. Add to Primary Asset list in Project Settings
  // 2. Add directory to "Additional Directories to Cook"
  // 3. Reference from a DataAsset that is referenced
  
  // Verify cooking:
  // Window > Developer Tools > Asset Audit
  // Project Launcher > Cook content before package
  
  // DataAsset for guaranteed cooking:
  UCLASS()
  class UGameAssets : public UPrimaryDataAsset
  {
      UPROPERTY(EditDefaultsOnly)
      TArray<TSoftObjectPtr<UStaticMesh>> AllMeshes;
  };
  // Reference this DataAsset from GameMode = all meshes cook
  
### **Symptoms**
  - Works in editor, crashes in package
  - "Failed to load" errors in packaged game
  - Missing meshes/textures in build
  - LogAssetRegistry warnings
### **Detection Pattern**
LoadObject<[^>]+>\s*\(\s*nullptr\s*,\s*TEXT\s*\(

## Rpc Bandwidth Explosion

### **Id**
rpc-bandwidth-explosion
### **Summary**
Sending RPCs too frequently or with too much data
### **Severity**
high
### **Situation**
Multicast every frame, large structs in RPCs, unreliable spam
### **Why**
  Each RPC = network packet. Multicast to 32 players = 32 packets.
  Every frame at 60 FPS = 1920 packets/second per RPC. Bandwidth explodes.
  Clients lag. Server overloads. Multiplayer becomes unplayable.
  
### **Solution**
  // WRONG: Multicast position every frame
  void AEnemy::Tick(float DeltaTime)
  {
      Multicast_UpdatePosition(GetActorLocation());  // 60+ RPCs per second
  }
  
  // RIGHT: Replicate properties instead
  UPROPERTY(Replicated)
  FVector_NetQuantize ReplicatedLocation;
  
  void AEnemy::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
  {
      DOREPLIFETIME(AEnemy, ReplicatedLocation);
  }
  
  // WRONG: Large struct in RPC
  UFUNCTION(Server, Reliable)
  void Server_SendPlayerData(FCompletePlayerInventory Inventory);  // 100KB struct
  
  // RIGHT: Send minimal data, client fetches rest
  UFUNCTION(Server, Reliable)
  void Server_RequestInventory();
  
  UFUNCTION(Client, Reliable)
  void Client_ReceiveInventoryUpdate(int32 Slot, FItemData Item);
  
  // Use Unreliable for cosmetic/non-critical
  UFUNCTION(NetMulticast, Unreliable)
  void Multicast_PlayImpactEffect(FVector Location);
  
  // Use Reliable for important state
  UFUNCTION(NetMulticast, Reliable)
  void Multicast_PlayerDied(APlayerState* DeadPlayer);
  
  // Quantize vectors to save bandwidth
  FVector_NetQuantize Location;  // 24 bits per component vs 32
  
### **Symptoms**
  - High ping/latency
  - Bandwidth warnings in logs
  - Server hitching
  - Clients desyncing under load
### **Detection Pattern**
Multicast_.*Tick|Tick.*Multicast_

## Beginplay Order Dependency

### **Id**
beginplay-order-dependency
### **Summary**
Depending on other Actors' BeginPlay having run
### **Severity**
medium
### **Situation**
Actor A's BeginPlay expects Actor B to be fully initialized
### **Why**
  BeginPlay order is not guaranteed between actors. Actor A may run before B.
  References to other actors may be null or uninitialized. Intermittent bugs.
  
### **Solution**
  // WRONG: Assuming other actors are ready
  void AEnemySpawner::BeginPlay()
  {
      Super::BeginPlay();
      // GameMode might not have BeginPlay called yet!
      AMyGameMode* GM = Cast<AMyGameMode>(GetWorld()->GetAuthGameMode());
      GM->RegisterSpawner(this);  // Crash if GM not initialized
  }
  
  // RIGHT: Defer or use callbacks
  void AEnemySpawner::BeginPlay()
  {
      Super::BeginPlay();
  
      // Option 1: Timer to defer
      GetWorld()->GetTimerManager().SetTimerForNextTick([this]()
      {
          if (AMyGameMode* GM = Cast<AMyGameMode>(GetWorld()->GetAuthGameMode()))
          {
              GM->RegisterSpawner(this);
          }
      });
  
      // Option 2: GameMode initiates registration
      // Let GameMode find spawners in its BeginPlay
  }
  
  // GameMode approach:
  void AMyGameMode::BeginPlay()
  {
      Super::BeginPlay();
  
      // GameMode always initializes after all actors spawned
      TArray<AActor*> Spawners;
      UGameplayStatics::GetAllActorsOfClass(GetWorld(), AEnemySpawner::StaticClass(), Spawners);
      for (AActor* Actor : Spawners)
      {
          RegisterSpawner(Cast<AEnemySpawner>(Actor));
      }
  }
  
### **Symptoms**
  - Intermittent null pointer on startup
  - Works sometimes, crashes others
  - Different behavior in PIE vs packaged
### **Detection Pattern**
