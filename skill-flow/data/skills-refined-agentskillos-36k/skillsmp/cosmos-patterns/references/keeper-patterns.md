# Keeper Patterns for Cosmos SDK

Keeper implementation patterns for Celestia/Cosmos SDK modules.

## Keeper Structure

```go
package mymodule

import (
    "context"

    "cosmossdk.io/core/store"
    "github.com/cosmos/cosmos-sdk/codec"
    sdk "github.com/cosmos/cosmos-sdk/types"

    "github.com/celestiaorg/celestia-app/x/mymodule/types"
)

// Keeper handles state management for the mymodule module.
type Keeper struct {
    cdc        codec.BinaryCodec
    storeKey   store.KVStoreService
    bankKeeper types.BankKeeper
    authority  string
}

// NewKeeper creates a new Keeper instance.
func NewKeeper(
    cdc codec.BinaryCodec,
    storeKey store.KVStoreService,
    bankKeeper types.BankKeeper,
    authority string,
) Keeper {
    return Keeper{
        cdc:        cdc,
        storeKey:   storeKey,
        bankKeeper: bankKeeper,
        authority:  authority,
    }
}
```

## Message Handlers

```go
// Xxx handles the MsgXxx message.
func (k Keeper) Xxx(ctx context.Context, msg *types.MsgXxx) (*types.MsgXxxResponse, error) {
    // 1. Validate signer
    signer, err := sdk.AccAddressFromBech32(msg.Signer)
    if err != nil {
        return nil, err
    }

    // 2. Business logic
    // ...

    // 3. Update state
    if err := k.SetXxx(ctx, key, value); err != nil {
        return nil, err
    }

    // 4. Emit typed event
    sdkCtx := sdk.UnwrapSDKContext(ctx)
    if err := sdkCtx.EventManager().EmitTypedEvent(&types.EventXxx{
        Signer: msg.Signer,
        Amount: msg.Amount.String(),
    }); err != nil {
        return nil, err
    }

    return &types.MsgXxxResponse{}, nil
}
```

## State Accessors

### Get

```go
// GetXxx retrieves xxx from the store.
func (k Keeper) GetXxx(ctx context.Context, key []byte) (types.Xxx, error) {
    store := k.storeKey.OpenKVStore(ctx)
    bz, err := store.Get(types.GetXxxKey(key))
    if err != nil {
        return types.Xxx{}, err
    }
    if bz == nil {
        return types.Xxx{}, types.ErrXxxNotFound
    }

    var xxx types.Xxx
    if err := k.cdc.Unmarshal(bz, &xxx); err != nil {
        return types.Xxx{}, err
    }

    return xxx, nil
}
```

### Set

```go
// SetXxx stores xxx in the store.
func (k Keeper) SetXxx(ctx context.Context, key []byte, xxx types.Xxx) error {
    store := k.storeKey.OpenKVStore(ctx)
    bz, err := k.cdc.Marshal(&xxx)
    if err != nil {
        return err
    }
    return store.Set(types.GetXxxKey(key), bz)
}
```

### Delete

```go
// DeleteXxx removes xxx from the store.
func (k Keeper) DeleteXxx(ctx context.Context, key []byte) error {
    store := k.storeKey.OpenKVStore(ctx)
    return store.Delete(types.GetXxxKey(key))
}
```

### Iterate

```go
// IterateXxxs iterates over all xxx entries.
func (k Keeper) IterateXxxs(ctx context.Context, cb func(xxx types.Xxx) (stop bool)) error {
    store := k.storeKey.OpenKVStore(ctx)
    iterator, err := store.Iterator(types.KeyXxx, storetypes.PrefixEndBytes(types.KeyXxx))
    if err != nil {
        return err
    }
    defer iterator.Close()

    for ; iterator.Valid(); iterator.Next() {
        var xxx types.Xxx
        if err := k.cdc.Unmarshal(iterator.Value(), &xxx); err != nil {
            return err
        }
        if cb(xxx) {
            break
        }
    }

    return nil
}
```

## Query Handlers

```go
// QueryXxx handles the QueryXxxRequest query.
func (k Keeper) QueryXxx(ctx context.Context, req *types.QueryXxxRequest) (*types.QueryXxxResponse, error) {
    if req == nil {
        return nil, status.Error(codes.InvalidArgument, "empty request")
    }

    xxx, err := k.GetXxx(ctx, []byte(req.Key))
    if err != nil {
        return nil, status.Error(codes.NotFound, err.Error())
    }

    return &types.QueryXxxResponse{Xxx: &xxx}, nil
}

// QueryAllXxx handles the QueryAllXxxRequest query with pagination.
func (k Keeper) QueryAllXxx(ctx context.Context, req *types.QueryAllXxxRequest) (*types.QueryAllXxxResponse, error) {
    if req == nil {
        return nil, status.Error(codes.InvalidArgument, "empty request")
    }

    var xxxs []types.Xxx
    store := k.storeKey.OpenKVStore(ctx)

    pageRes, err := query.Paginate(store, req.Pagination, func(key []byte, value []byte) error {
        var xxx types.Xxx
        if err := k.cdc.Unmarshal(value, &xxx); err != nil {
            return err
        }
        xxxs = append(xxxs, xxx)
        return nil
    })
    if err != nil {
        return nil, status.Error(codes.Internal, err.Error())
    }

    return &types.QueryAllXxxResponse{
        Xxxs:       xxxs,
        Pagination: pageRes,
    }, nil
}
```

## Expected Keepers Pattern

```go
// types/expected_keepers.go
package types

import (
    "context"
    sdk "github.com/cosmos/cosmos-sdk/types"
)

// BankKeeper defines the expected interface for the bank module.
type BankKeeper interface {
    GetBalance(ctx context.Context, addr sdk.AccAddress, denom string) sdk.Coin
    SendCoins(ctx context.Context, from, to sdk.AccAddress, amt sdk.Coins) error
    SendCoinsFromAccountToModule(ctx context.Context, addr sdk.AccAddress, name string, amt sdk.Coins) error
    SendCoinsFromModuleToAccount(ctx context.Context, name string, addr sdk.AccAddress, amt sdk.Coins) error
    MintCoins(ctx context.Context, name string, amt sdk.Coins) error
    BurnCoins(ctx context.Context, name string, amt sdk.Coins) error
}

// AccountKeeper defines the expected interface for the auth module.
type AccountKeeper interface {
    GetAccount(ctx context.Context, addr sdk.AccAddress) sdk.AccountI
}
```

## Typed Events (Required)

```go
// WRONG - Legacy events
ctx.EventManager().EmitEvent(
    sdk.NewEvent(
        "burn",
        sdk.NewAttribute("signer", msg.Signer),
        sdk.NewAttribute("amount", msg.Amount.String()),
    ),
)

// CORRECT - Typed events
sdkCtx := sdk.UnwrapSDKContext(ctx)
sdkCtx.EventManager().EmitTypedEvent(&types.EventBurn{
    Signer: msg.Signer,
    Amount: msg.Amount.String(),
})
```

## Authority Pattern (for governance)

```go
// UpdateParams updates the module parameters.
func (k Keeper) UpdateParams(ctx context.Context, msg *types.MsgUpdateParams) (*types.MsgUpdateParamsResponse, error) {
    // Verify authority
    if msg.Authority != k.authority {
        return nil, sdkerrors.ErrUnauthorized.Wrapf(
            "invalid authority; expected %s, got %s",
            k.authority,
            msg.Authority,
        )
    }

    // Update params
    if err := k.SetParams(ctx, msg.Params); err != nil {
        return nil, err
    }

    return &types.MsgUpdateParamsResponse{}, nil
}
```

## Godoc Requirements

Every exported function needs godoc:

```go
// Package mymodule provides functionality for [description].
package mymodule

// Keeper handles state management for the mymodule module.
// It provides methods for [key functionality].
type Keeper struct { ... }

// NewKeeper creates a new Keeper instance with the provided dependencies.
func NewKeeper(...) Keeper { ... }

// Xxx processes the MsgXxx message by [what it does].
// It validates [what], updates [what state], and emits [what event].
func (k Keeper) Xxx(...) { ... }
```

## Nil Check Pattern

Check required dependencies in NewKeeper, panic if nil:

```go
func NewKeeper(
    cdc codec.BinaryCodec,
    storeService store.KVStoreService,
    bankKeeper types.BankKeeper,  // Required
    optionalKeeper *OtherKeeper,  // Optional - can be nil
) Keeper {
    if bankKeeper == nil {
        panic("bankKeeper cannot be nil")
    }
    // optionalKeeper can remain nil - check in methods if needed
    return Keeper{...}
}
```

Don't scatter nil checks in methods:

```go
// WRONG - nil checks in every method
func (k Keeper) SomeMethod(ctx context.Context) error {
    if k.bankKeeper == nil {
        return ErrNotConfigured
    }
    // ...
}

// CORRECT - panic in constructor, trust in methods
func (k Keeper) SomeMethod(ctx context.Context) error {
    // k.bankKeeper guaranteed non-nil from NewKeeper
    return k.bankKeeper.SendCoins(ctx, ...)
}
```

## Error Code Numbering

```go
// types/errors.go
package types

import "cosmossdk.io/errors"

var (
    // Start from 2 - code 1 is reserved by SDK
    ErrInvalidInput  = errors.Register(ModuleName, 2, "invalid input")
    ErrNotFound      = errors.Register(ModuleName, 3, "not found")
    ErrUnauthorized  = errors.Register(ModuleName, 4, "unauthorized")
)
```

## Collections Prefix Pattern

Use `collections.NewPrefix()` instead of raw byte slices:

```go
// types/keys.go
package types

import "cosmossdk.io/collections"

var (
    // WRONG - raw byte slices
    // ParamsPrefix = []byte{0x01}

    // CORRECT - collections.NewPrefix
    ParamsPrefix = collections.NewPrefix(1)
    ItemsPrefix  = collections.NewPrefix(2)
)
```

## Query Validation Pattern

Query servers should validate preconditions before returning:

```go
func (q queryServer) DeriveAddress(ctx context.Context, req *types.QueryDeriveAddressRequest) (*types.QueryDeriveAddressResponse, error) {
    // 1. Validate request
    if req == nil {
        return nil, status.Error(codes.InvalidArgument, "nil request")
    }

    // 2. Validate preconditions (can the operation succeed?)
    hasRoute, err := q.k.HasRoute(ctx, req.Domain)
    if err != nil {
        return nil, status.Errorf(codes.Internal, "route check failed: %v", err)
    }
    if !hasRoute {
        return nil, status.Errorf(codes.FailedPrecondition, "no route to domain %d", req.Domain)
    }

    // 3. Only then return the result
    addr, err := types.DeriveAddress(req.Domain, req.Recipient)
    if err != nil {
        return nil, status.Errorf(codes.InvalidArgument, "derivation failed: %v", err)
    }

    return &types.QueryDeriveAddressResponse{Address: addr.String()}, nil
}
```
