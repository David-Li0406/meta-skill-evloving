# Cosmos SDK Module Structure

Standard directory layout for Cosmos SDK modules.

## Directory Layout

```
x/mymodule/
├── keeper.go              # Keeper struct + msg_server implementation
├── keeper_test.go         # Keeper integration tests
├── module.go              # AppModule + AppModuleBasic
├── genesis.go             # Genesis init/export (if simple)
├── types/
│   ├── codec.go           # RegisterInterfaces + RegisterLegacyAminoCodec
│   ├── errors.go          # Module-specific errors (optional)
│   ├── events.go          # Event helper functions (optional)
│   ├── expected_keepers.go # Interfaces for external keepers
│   ├── genesis.go         # Genesis state types + validation
│   ├── keys.go            # StoreKey, ModuleName, key prefixes
│   ├── msgs.go            # Message types + ValidateBasic
│   └── params.go          # Module parameters (if any)
└── test/
    └── integration_test.go # Full integration tests
```

## Proto Directory

```
proto/celestia/mymodule/v1/
├── tx.proto               # Transaction messages (MsgXxx)
├── query.proto            # Query service definitions
├── types.proto            # Shared types (state objects)
├── events.proto           # Event definitions
├── genesis.proto          # Genesis state proto
└── params.proto           # Parameters proto (if any)
```

## File Responsibilities

### keeper.go
```go
package mymodule

type Keeper struct {
    storeKey   storetypes.StoreKey
    cdc        codec.BinaryCodec
    bankKeeper types.BankKeeper
    authority  string // governance authority address
}

func NewKeeper(...) Keeper { ... }

// Message handlers
func (k Keeper) Xxx(ctx context.Context, msg *types.MsgXxx) (*types.MsgXxxResponse, error) { ... }

// Query handlers
func (k Keeper) QueryXxx(ctx context.Context, req *types.QueryXxxRequest) (*types.QueryXxxResponse, error) { ... }

// State accessors
func (k Keeper) GetXxx(ctx context.Context, key []byte) (types.Xxx, error) { ... }
func (k Keeper) SetXxx(ctx context.Context, key []byte, value types.Xxx) { ... }
```

### module.go
```go
package mymodule

var (
    _ module.AppModule      = AppModule{}
    _ module.AppModuleBasic = AppModuleBasic{}
)

type AppModuleBasic struct{}

func (AppModuleBasic) Name() string { return types.ModuleName }
func (AppModuleBasic) RegisterInterfaces(registry codectypes.InterfaceRegistry) {
    types.RegisterInterfaces(registry)
}
// ... other AppModuleBasic methods

type AppModule struct {
    AppModuleBasic
    keeper Keeper
}

func NewAppModule(keeper Keeper) AppModule { ... }
func (am AppModule) RegisterServices(cfg module.Configurator) {
    types.RegisterMsgServer(cfg.MsgServer(), am.keeper)
    types.RegisterQueryServer(cfg.QueryServer(), am.keeper)
}
// ... other AppModule methods
```

### types/keys.go
```go
package types

const (
    ModuleName = "mymodule"
    StoreKey   = ModuleName
    RouterKey  = ModuleName
)

var (
    KeyXxx = []byte{0x01}
    KeyYyy = []byte{0x02}
)

func GetXxxKey(id uint64) []byte {
    return append(KeyXxx, sdk.Uint64ToBigEndian(id)...)
}
```

### types/expected_keepers.go
```go
package types

import (
    "context"
    sdk "github.com/cosmos/cosmos-sdk/types"
)

type BankKeeper interface {
    GetBalance(ctx context.Context, addr sdk.AccAddress, denom string) sdk.Coin
    SendCoins(ctx context.Context, from, to sdk.AccAddress, amt sdk.Coins) error
    SendCoinsFromAccountToModule(ctx context.Context, addr sdk.AccAddress, name string, amt sdk.Coins) error
    SendCoinsFromModuleToAccount(ctx context.Context, name string, addr sdk.AccAddress, amt sdk.Coins) error
    MintCoins(ctx context.Context, name string, amt sdk.Coins) error
    BurnCoins(ctx context.Context, name string, amt sdk.Coins) error
}
```

### types/msgs.go
```go
package types

import (
    sdk "github.com/cosmos/cosmos-sdk/types"
    sdkerrors "cosmossdk.io/errors"
)

var _ sdk.Msg = &MsgXxx{}

func (msg MsgXxx) ValidateBasic() error {
    if _, err := sdk.AccAddressFromBech32(msg.Signer); err != nil {
        return sdkerrors.ErrInvalidAddress.Wrapf("invalid signer: %s", err)
    }
    // Additional validation...
    return nil
}

func (msg MsgXxx) GetSigners() []sdk.AccAddress {
    signer, _ := sdk.AccAddressFromBech32(msg.Signer)
    return []sdk.AccAddress{signer}
}
```

## Registration in app.go

```go
// In app.go

import (
    "github.com/celestiaorg/celestia-app/x/mymodule"
    mymodulekeeper "github.com/celestiaorg/celestia-app/x/mymodule/keeper"
    mymoduletypes "github.com/celestiaorg/celestia-app/x/mymodule/types"
)

// Add to AppKeepers
type App struct {
    // ...
    MyModuleKeeper mymodulekeeper.Keeper
}

// In NewApp()
app.MyModuleKeeper = mymodulekeeper.NewKeeper(
    appCodec,
    keys[mymoduletypes.StoreKey],
    app.BankKeeper,
    authtypes.NewModuleAddress(govtypes.ModuleName).String(),
)

// Add to module manager
app.ModuleManager = module.NewManager(
    // ...
    mymodule.NewAppModule(app.MyModuleKeeper),
)
```
