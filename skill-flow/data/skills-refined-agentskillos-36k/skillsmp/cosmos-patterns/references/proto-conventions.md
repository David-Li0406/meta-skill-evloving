# Proto Conventions for Cosmos SDK

Protobuf conventions and patterns for Celestia/Cosmos SDK modules.

## File Organization

```
proto/celestia/mymodule/v1/
├── tx.proto        # Transaction messages
├── query.proto     # Query service
├── types.proto     # Shared types
├── events.proto    # Event definitions
└── genesis.proto   # Genesis state
```

## Standard Headers

Every proto file should start with:

```protobuf
syntax = "proto3";
package celestia.mymodule.v1;

option go_package = "github.com/celestiaorg/celestia-app/x/mymodule/types";
```

**Important:** No version suffix in go_package (no `/v6/` etc.)

## Transaction Messages (tx.proto)

```protobuf
syntax = "proto3";
package celestia.mymodule.v1;

option go_package = "github.com/celestiaorg/celestia-app/x/mymodule/types";

import "cosmos/msg/v1/msg.proto";
import "cosmos_proto/cosmos.proto";
import "amino/amino.proto";

// Msg defines the mymodule Msg service.
service Msg {
  option (cosmos.msg.v1.service) = true;

  // Xxx does something.
  // [Detailed description of what this does and any side effects]
  rpc Xxx(MsgXxx) returns (MsgXxxResponse);
}

// MsgXxx defines the message for doing xxx.
message MsgXxx {
  option (cosmos.msg.v1.signer) = "signer";
  option (amino.name) = "celestia/MsgXxx";

  // signer is the address that signs and pays for the transaction.
  string signer = 1 [(cosmos_proto.scalar) = "cosmos.AddressString"];

  // amount is the quantity of tokens to process.
  string amount = 2 [
    (cosmos_proto.scalar) = "cosmos.Int",
    (amino.dont_omitempty) = true
  ];
}

// MsgXxxResponse is the response type for the Xxx RPC.
message MsgXxxResponse {}
```

## Query Service (query.proto)

```protobuf
syntax = "proto3";
package celestia.mymodule.v1;

option go_package = "github.com/celestiaorg/celestia-app/x/mymodule/types";

import "google/api/annotations.proto";
import "cosmos/base/query/v1beta1/pagination.proto";

// Query defines the gRPC querier service.
service Query {
  // Xxx queries for xxx.
  rpc Xxx(QueryXxxRequest) returns (QueryXxxResponse) {
    option (google.api.http).get = "/celestia/mymodule/v1/xxx";
  }

  // XxxAll queries all xxx with pagination.
  rpc XxxAll(QueryAllXxxRequest) returns (QueryAllXxxResponse) {
    option (google.api.http).get = "/celestia/mymodule/v1/xxx/all";
  }
}

// QueryXxxRequest is the request type for the Query/Xxx RPC.
message QueryXxxRequest {
  string key = 1;
}

// QueryXxxResponse is the response type for the Query/Xxx RPC.
message QueryXxxResponse {
  Xxx xxx = 1;
}

// QueryAllXxxRequest is the request type for the Query/XxxAll RPC.
message QueryAllXxxRequest {
  cosmos.base.query.v1beta1.PageRequest pagination = 1;
}

// QueryAllXxxResponse is the response type for the Query/XxxAll RPC.
message QueryAllXxxResponse {
  repeated Xxx xxxs = 1;
  cosmos.base.query.v1beta1.PageResponse pagination = 2;
}
```

## Events (events.proto)

```protobuf
syntax = "proto3";
package celestia.mymodule.v1;

option go_package = "github.com/celestiaorg/celestia-app/x/mymodule/types";

// EventXxx is emitted when xxx occurs.
message EventXxx {
  // signer is the address that initiated the action.
  string signer = 1;

  // amount is the quantity processed.
  string amount = 2;
}
```

**Important:** Event field names should match the corresponding message field names.

## Types (types.proto)

```protobuf
syntax = "proto3";
package celestia.mymodule.v1;

option go_package = "github.com/celestiaorg/celestia-app/x/mymodule/types";

import "cosmos_proto/cosmos.proto";
import "gogoproto/gogo.proto";

// Xxx represents the state of xxx.
message Xxx {
  option (gogoproto.equal) = true;

  uint64 id = 1;
  string owner = 2 [(cosmos_proto.scalar) = "cosmos.AddressString"];
  string value = 3;
}
```

## Genesis (genesis.proto)

```protobuf
syntax = "proto3";
package celestia.mymodule.v1;

option go_package = "github.com/celestiaorg/celestia-app/x/mymodule/types";

import "gogoproto/gogo.proto";

// GenesisState defines the mymodule module's genesis state.
message GenesisState {
  // params defines all the parameters of the module.
  Params params = 1 [(gogoproto.nullable) = false];

  // xxxs is the list of xxx states.
  repeated Xxx xxxs = 2 [(gogoproto.nullable) = false];
}

// Params defines the parameters for the module.
message Params {
  option (gogoproto.equal) = true;
  option (gogoproto.goproto_stringer) = false;

  // enabled indicates if the module is enabled.
  bool enabled = 1;
}
```

## Backwards Compatibility Rules

1. **Never remove fields** - mark as deprecated instead
2. **Never renumber fields** - numbers are part of the wire format
3. **Never change field types** - add new field instead
4. **Reserve removed field numbers:**
   ```protobuf
   message MsgXxx {
     reserved 3, 4;
     reserved "old_field";
   }
   ```

## Common Annotations

```protobuf
// Signer specification (required for Msgs)
option (cosmos.msg.v1.signer) = "signer";

// Address scalar
string address = 1 [(cosmos_proto.scalar) = "cosmos.AddressString"];

// Int/Dec scalars
string amount = 2 [(cosmos_proto.scalar) = "cosmos.Int"];
string rate = 3 [(cosmos_proto.scalar) = "cosmos.Dec"];

// Non-nullable (for genesis states)
Params params = 1 [(gogoproto.nullable) = false];
```

## GetSigners Inference

The `GetSigners()` method is auto-generated from the proto annotation - **DO NOT implement manually**:

```protobuf
// tx.proto
message MsgExecute {
  option (cosmos.msg.v1.signer) = "signer";  // This handles GetSigners()

  string signer = 1 [(cosmos_proto.scalar) = "cosmos.AddressString"];
}
```

```go
// WRONG - Delete this method entirely
func (msg *MsgExecute) GetSigners() []sdk.AccAddress {
    signer, _ := sdk.AccAddressFromBech32(msg.Signer)
    return []sdk.AccAddress{signer}
}

// CORRECT - Don't implement, proto annotation handles it
// The cosmos.msg.v1.signer annotation automatically generates GetSigners()
```

This pattern also applies to messages with multiple signers:

```protobuf
message MsgMultiSig {
  option (cosmos.msg.v1.signer) = "signers";

  repeated string signers = 1 [(cosmos_proto.scalar) = "cosmos.AddressString"];
}
```
