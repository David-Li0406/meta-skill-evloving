package adapters

import (
	"context"
	"testing"

	"github.com/Napageneral/cortex/internal/db"
)

func TestCalendarAdapter_EnsureTables(t *testing.T) {
	tmp := t.TempDir()
	t.Setenv("COMMS_DATA_DIR", tmp)
	if err := db.Init(); err != nil {
		t.Fatalf("db.Init: %v", err)
	}
	d, err := db.Open()
	if err != nil {
		t.Fatalf("db.Open: %v", err)
	}
	defer d.Close()

	c, err := NewCalendarAdapter("calendar-test@example.com", "test@example.com")
	if err != nil {
		t.Fatalf("NewCalendarAdapter: %v", err)
	}

	// Ensure it can run ensureCalendarTables without external calls.
	if err := c.ensureCalendarTables(d); err != nil {
		t.Fatalf("ensureCalendarTables: %v", err)
	}

	// Sync with cancelled ctx should return ctx error before making external calls.
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	_, _ = c.Sync(ctx, d, false)
}
