# Gameplay Ability System (GAS)

## Contents
- [Define AttributeSet and replication](#define-attributeset-and-replication)
- [Register AttributeSet on character](#register-attributeset-on-character)
- [Listen for attribute changes in AnimInstance](#listen-for-attribute-changes-in-animinstance)
- [Notes](#notes)

## Define AttributeSet and replication

Define a `UAngelscriptAttributeSet` and forward replication callbacks via `OnRep_Attribute`.

```angelscript
namespace UExample_GASAttributes
{
	const FName HealthName = n"Health";
	const FName SpeedName = n"Speed";
}

class UExample_GASAttributes : UAngelscriptAttributeSet
{
	UPROPERTY(BlueprintReadOnly, Category = "Pawn Attributes")
	FAngelscriptGameplayAttributeData Health;

	UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_ReplicationTrampoline, Category = "Pawn Attributes")
	FAngelscriptGameplayAttributeData Speed;

	UExample_GASAttributes()
	{
		Health.Initialize(100.0f);
		Speed.Initialize(1.0f);
	}

	UFUNCTION()
	void OnRep_ReplicationTrampoline(FAngelscriptGameplayAttributeData& OldAttributeData)
	{
		OnRep_Attribute(OldAttributeData);
	}
};
```

## Register AttributeSet on character

Register the attribute set in `AAngelscriptGASCharacter` during `BeginPlay()`.

```angelscript
class AExample_GASCharacter : AAngelscriptGASCharacter
{
	UFUNCTION(BlueprintOverride)
	void BeginPlay()
	{
		AbilitySystem.RegisterAttributeSet(UExample_GASAttributes);
	}
};
```

## Listen for attribute changes in AnimInstance

Use `OnAttributeSetRegistered` to bind attribute callbacks once the set is available.

```angelscript
class UExample_GASAnimInstance : UAnimInstance
{
	private float32 CachedSpeed = 1.0f;

	UFUNCTION(BlueprintOverride)
	void BlueprintBeginPlay()
	{
		Cast<AAngelscriptGASCharacter>(TryGetPawnOwner()).AbilitySystem.OnAttributeSetRegistered(this, n"OnAttributeSetRegistered");
	}

	UFUNCTION()
	void OnAttributeSetRegistered(UAngelscriptAttributeSet NewAttributeSet)
	{
		if (NewAttributeSet.IsA(UExample_GASAttributes::StaticClass()))
		{
			AAngelscriptGASCharacter Character = Cast<AAngelscriptGASCharacter>(OwningActor);
			Character.AbilitySystem.GetAndRegisterCallbackForAttribute(UExample_GASAttributes::StaticClass(), UExample_GASAttributes::SpeedName, CachedSpeed);
			Character.AbilitySystem.OnAttributeChanged.AddUFunction(this, n"OnAttributeChanged");
		}
	}

	UFUNCTION()
	private void OnAttributeChanged(const FAngelscriptModifiedAttribute&in AttributeChangeData)
	{
		if (AttributeChangeData.Name == UExample_GASAttributes::SpeedName)
		{
			CachedSpeed = AttributeChangeData.NewValue;
		}
	}
};
```

## Notes
- Attribute replication requires calling `OnRep_Attribute` in the `ReplicatedUsing` callback.
- `OnAttributeSetRegistered` fires immediately when the set is already registered.
- `GetAndRegisterCallbackForAttribute()` returns the current value and registers updates.
