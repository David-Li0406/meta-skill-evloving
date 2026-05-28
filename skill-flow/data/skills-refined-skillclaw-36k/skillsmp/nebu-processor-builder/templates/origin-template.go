// Package main provides a standalone CLI for the {NAME} processor.
//
// {DESCRIPTION}
package main

import (
	"context"

	"github.com/stellar/go-stellar-sdk/ingest"
	"github.com/stellar/go-stellar-sdk/xdr"
	"github.com/withObsrvr/nebu/pkg/processor"
	"github.com/withObsrvr/nebu/pkg/processor/cli"
)

var version = "0.1.0"

func main() {
	config := cli.OriginConfig{
		Name:        "{NAME}",
		Description: "{DESCRIPTION}",
		Version:     version,
	}

	// For JSON output (simpler)
	cli.RunGenericOriginCLI(config, func(networkPass string) cli.GenericOriginProcessor {
		return NewOrigin(networkPass)
	})

	// OR for protobuf output (type-safe, more complex)
	// cli.RunProtoOriginCLI(config, func(networkPass string) cli.ProtoOriginProcessor[*YourProtoType] {
	//     return NewOrigin(networkPass)
	// })
}

// Origin extracts events from Stellar ledgers
type Origin struct {
	passphrase string
	emitter    *processor.Emitter[map[string]interface{}] // or *YourProtoType
}

func NewOrigin(passphrase string) *Origin {
	return &Origin{
		passphrase: passphrase,
		emitter:    processor.NewEmitter[map[string]interface{}](1024),
	}
}

// Name implements processor.Processor
func (o *Origin) Name() string {
	return "{NAME}"
}

// Type implements processor.Processor
func (o *Origin) Type() processor.Type {
	return processor.TypeOrigin
}

// Out returns the output channel
func (o *Origin) Out() <-chan map[string]interface{} {
	return o.emitter.Out()
}

// Close closes the emitter
func (o *Origin) Close() {
	o.emitter.Close()
}

// ProcessLedger implements processor.Origin
// This is called for each ledger in the range
func (o *Origin) ProcessLedger(ctx context.Context, ledger xdr.LedgerCloseMeta) error {
	// TODO: Extract events from the ledger

	// Example: Process transactions
	reader, err := ingest.NewLedgerTransactionReaderFromLedgerCloseMeta(o.passphrase, ledger)
	if err != nil {
		return err
	}
	defer reader.Close()

	for {
		tx, err := reader.Read()
		if err != nil {
			break // End of transactions
		}

		// TODO: Extract your specific events from tx
		// events := extractEventsFromTx(tx)

		// Example event structure
		event := map[string]interface{}{
			"ledgerSequence": ledger.LedgerSequence(),
			"closedAt":       ledger.LedgerCloseTime(),
			"txHash":         tx.Result.TransactionHash.HexString(),
			"successful":     tx.Result.Successful(),
			// TODO: Add your event-specific fields
		}

		// Emit event
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
			o.emitter.Emit(event)
		}
	}

	return nil
}
