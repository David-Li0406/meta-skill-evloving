# Unreal Engine - Validations

## Raw UObject Pointer

### **Id**
ue-raw-uobject-pointer
### **Severity**
critical
### **Type**
regex
### **Pattern**
^\s*(UObject|AActor|UActorComponent|ACharacter|APawn|AController|USceneComponent|UPrimitiveComponent|UMeshComponent|UStaticMeshComponent|USkeletalMeshComponent|UWidgetComponent)\s*\*\s+\w+\s*[;=](?!.*//.*UPROPERTY)
### **Message**
UObject pointer without UPROPERTY. Garbage collector won't track this - potential crash.
### **Fix Action**
Add UPROPERTY() macro above the declaration
### **Applies To**
  - *.h
  - *.cpp

## World Access in Constructor

### **Id**
ue-constructor-world-access
### **Severity**
critical
### **Type**
regex
### **Pattern**
A\w+::\w+\(\)[^}]*(GetWorld\(\)|GetGameInstance\(\)|GetFirstPlayerController\(\)|SpawnActor|FindActor)
### **Message**
Accessing World/Game systems in constructor. World doesn't exist yet - will crash.
### **Fix Action**
Move to PostInitializeComponents() or BeginPlay()
### **Applies To**
  - *.cpp

## Unchecked Cast Result

### **Id**
ue-unchecked-cast
### **Severity**
error
### **Type**
regex
### **Pattern**
Cast<\w+>\s*\([^)]+\)\s*->
### **Message**
Using Cast result without null check. Will crash if cast fails.
### **Fix Action**
Use if (auto* Var = Cast<Type>(Source)) { ... }
### **Applies To**
  - *.cpp

## Missing GENERATED_BODY

### **Id**
ue-missing-generated-body
### **Severity**
critical
### **Type**
regex
### **Pattern**
class\s+\w+_API\s+\w+\s*:\s*public\s+\w+[^}]*\{(?![^}]*GENERATED_BODY)
### **Message**
UCLASS without GENERATED_BODY() macro. Reflection won't work.
### **Fix Action**
Add GENERATED_BODY() as first line in class body
### **Applies To**
  - *.h

## GetAllActorsOfClass in Tick

### **Id**
ue-tick-getallactors
### **Severity**
error
### **Type**
regex
### **Pattern**
Tick\s*\([^)]*\)\s*\{[^}]*(GetAllActorsOfClass|GetAllActorsWithTag|GetAllActorsWithInterface)
### **Message**
GetAllActorsOfClass in Tick is O(n) every frame. Cache references instead.
### **Fix Action**
Cache actor references in BeginPlay and update on spawn/destroy events
### **Applies To**
  - *.cpp

## Multicast RPC in Tick

### **Id**
ue-tick-multicast
### **Severity**
error
### **Type**
regex
### **Pattern**
Tick\s*\([^)]*\)\s*\{[^}]*Multicast_
### **Message**
Multicast RPC in Tick causes bandwidth explosion. Use replicated properties instead.
### **Fix Action**
Replicate state with UPROPERTY(Replicated) and OnRep
### **Applies To**
  - *.cpp

## Synchronous Asset Load

### **Id**
ue-synchronous-load-gameplay
### **Severity**
warning
### **Type**
regex
### **Pattern**
LoadSynchronous\s*\(\s*\)(?!.*BeginPlay|.*PreloadAssets|.*Init)
### **Message**
Synchronous asset loading during gameplay causes frame hitches.
### **Fix Action**
Use async loading with FStreamableManager::RequestAsyncLoad
### **Applies To**
  - *.cpp

## FString Operations in Tick

### **Id**
ue-fstring-in-tick
### **Severity**
warning
### **Type**
regex
### **Pattern**
Tick\s*\([^)]*\)\s*\{[^}]*(FString::Printf|FString\s+\w+\s*=|\.Append\(|FName\s*\(.*FString)
### **Message**
FString allocation in Tick causes GC pressure. Cache strings or use FName.
### **Fix Action**
Cache FString results or use FName for comparisons
### **Applies To**
  - *.cpp

## Object Allocation in Tick

### **Id**
ue-new-in-tick
### **Severity**
warning
### **Type**
regex
### **Pattern**
Tick\s*\([^)]*\)\s*\{[^}]*new\s+\w+
### **Message**
Memory allocation in Tick causes fragmentation. Use object pooling.
### **Fix Action**
Pre-allocate objects or use TArray with Reserve()
### **Applies To**
  - *.cpp

## Replicated Property Without Authority

### **Id**
ue-replicated-no-authority-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
(Health|Ammo|Score|Mana|Stamina|Lives)\s*[-+]=(?!.*HasAuthority|.*ROLE_Authority|.*GetLocalRole)
### **Message**
Modifying replicated property without authority check. Changes may be overwritten.
### **Fix Action**
Add if (HasAuthority()) check before modifying
### **Applies To**
  - *.cpp

## Replicated Without GetLifetimeReplicatedProps

### **Id**
ue-missing-getlifetimereplicatedprops
### **Severity**
error
### **Type**
regex
### **Pattern**
UPROPERTY\s*\([^)]*Replicated[^)]*\)(?![^;]*GetLifetimeReplicatedProps)
### **Message**
Replicated property requires GetLifetimeReplicatedProps override.
### **Fix Action**
Implement GetLifetimeReplicatedProps and add DOREPLIFETIME macro
### **Applies To**
  - *.h

## Server RPC Without Validation

### **Id**
ue-server-rpc-no-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
UFUNCTION\s*\(\s*Server\s*,\s*Reliable\s*\)
### **Message**
Server RPC without WithValidation. Vulnerable to cheating.
### **Fix Action**
Add WithValidation specifier and implement _Validate function
### **Applies To**
  - *.h

## Hard Asset Reference

### **Id**
ue-hard-asset-reference
### **Severity**
warning
### **Type**
regex
### **Pattern**
UPROPERTY\s*\([^)]*\)\s*(UStaticMesh|USkeletalMesh|UTexture2D|UMaterialInterface|USoundBase|UAnimMontage|UAnimSequence|UParticleSystem)\s*\*
### **Message**
Hard asset reference loads asset immediately. Consider TSoftObjectPtr for on-demand loading.
### **Fix Action**
Use TSoftObjectPtr<Type> for assets that aren't always needed
### **Applies To**
  - *.h

## LoadObject With Path String

### **Id**
ue-loadobject-path
### **Severity**
warning
### **Type**
regex
### **Pattern**
LoadObject<[^>]+>\s*\(\s*nullptr\s*,\s*TEXT\s*\(
### **Message**
LoadObject with path string may fail in packaged build if asset not cooked.
### **Fix Action**
Use TSoftObjectPtr or ensure asset is in Primary Asset list
### **Applies To**
  - *.cpp

## Tick Enabled by Default

### **Id**
ue-tick-enabled-default
### **Severity**
info
### **Type**
regex
### **Pattern**
PrimaryActorTick\.bCanEverTick\s*=\s*true
### **Message**
Actor ticks by default. Only enable if truly needed per-frame.
### **Fix Action**
Set to false if Tick not needed. Use timers for periodic updates.
### **Applies To**
  - *.cpp

## Public Member Without UPROPERTY

### **Id**
ue-public-member-no-uproperty
### **Severity**
warning
### **Type**
regex
### **Pattern**
public:\s*\n\s*(?!UPROPERTY|UFUNCTION|GENERATED|virtual|static|explicit|friend|using|template|class|struct|enum)[A-Z]\w+\s*\*?\s+\w+\s*[;=]
### **Message**
Public member without UPROPERTY won't be visible to Blueprint or serialization.
### **Fix Action**
Add UPROPERTY() or move to private if internal
### **Applies To**
  - *.h

## BeginPlay Without Super

### **Id**
ue-beginplay-no-super
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+\w+::BeginPlay\s*\(\s*\)\s*\{(?![^}]*Super::BeginPlay)
### **Message**
BeginPlay override without Super::BeginPlay() call.
### **Fix Action**
Add Super::BeginPlay() at start of function
### **Applies To**
  - *.cpp

## EndPlay Without Super

### **Id**
ue-endplay-no-super
### **Severity**
error
### **Type**
regex
### **Pattern**
void\s+\w+::EndPlay\s*\([^)]*\)\s*\{(?![^}]*Super::EndPlay)
### **Message**
EndPlay override without Super::EndPlay() call.
### **Fix Action**
Add Super::EndPlay(EndPlayReason) at end of function
### **Applies To**
  - *.cpp

## ensure() in Performance Path

### **Id**
ue-ensure-vs-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
Tick\s*\([^)]*\)\s*\{[^}]*(ensure|ensureMsg|ensureAlways)
### **Message**
ensure() in Tick generates reports in shipping builds. Use check() for fatal or remove.
### **Fix Action**
Use check() for fatal errors, or handle gracefully without assert
### **Applies To**
  - *.cpp

## Magic Numbers

### **Id**
ue-magic-numbers
### **Severity**
info
### **Type**
regex
### **Pattern**
(SetTimer|Delay)\s*\([^)]*,\s*\d+\.\d+f?\s*,
### **Message**
Magic number in timer. Consider using named constant or UPROPERTY.
### **Fix Action**
Define as const or UPROPERTY for easier tuning
### **Applies To**
  - *.cpp

## Hardcoded String

### **Id**
ue-text-macro-missing
### **Severity**
info
### **Type**
regex
### **Pattern**
UE_LOG\s*\([^,]+,\s*\w+\s*,\s*"
### **Message**
Hardcoded string in UE_LOG. Use TEXT() macro for Unicode safety.
### **Fix Action**
Wrap string in TEXT() macro
### **Applies To**
  - *.cpp

## BlueprintCallable Without Category

### **Id**
ue-blueprint-callable-no-category
### **Severity**
info
### **Type**
regex
### **Pattern**
UFUNCTION\s*\(\s*BlueprintCallable\s*\)(?![^;]*Category)
### **Message**
BlueprintCallable without Category makes function hard to find in Blueprint.
### **Fix Action**
Add Category = "MyCategory" to UFUNCTION specifiers
### **Applies To**
  - *.h

## Deprecated API Usage

### **Id**
ue-deprecated-api
### **Severity**
warning
### **Type**
regex
### **Pattern**
(FPaths::GameDir|FPaths::GameContentDir|UProperty|GetPlayerPawn\(0\)|GetPlayerController\(0\))
### **Message**
Using deprecated Unreal API. Check migration guide for replacement.
### **Fix Action**
Update to current API: FPaths::ProjectDir, FProperty, GetPlayerPawn(GetWorld(), 0)
### **Applies To**
  - *.cpp
  - *.h

## Unconnected Cast Failure Pin

### **Id**
ue-blueprint-cast-unconnected
### **Severity**
warning
### **Type**
regex
### **Pattern**
CastFailed.*=.*None
### **Message**
Blueprint Cast node has unconnected failure pin. Handle the failure case.
### **Fix Action**
Connect Cast Failed pin to handle when cast returns nullptr
### **Applies To**
  - *.uasset

## Include Order

### **Id**
ue-include-order
### **Severity**
info
### **Type**
regex
### **Pattern**
#include\s+"[^"]+\.generated\.h"(?!\s*$)
### **Message**
*.generated.h must be the last include in the file.
### **Fix Action**
Move *.generated.h to be the last #include
### **Applies To**
  - *.h

## Missing pragma once

### **Id**
ue-missing-pragma-once
### **Severity**
warning
### **Type**
regex
### **Pattern**
^(?!.*#pragma once)(?=.*UCLASS|.*USTRUCT|.*UENUM)
### **Message**
Header file missing #pragma once. Can cause duplicate definition errors.
### **Fix Action**
Add #pragma once at the top of the header file
### **Applies To**
  - *.h