package tools

import (
	"context"
	"testing"
)

func TestNewRegistry(t *testing.T) {
	r := NewRegistry()
	if r == nil {
		t.Fatal("NewRegistry() returned nil")
	}

	if len(r.adapters) != 0 {
		t.Errorf("new registry should have 0 adapters, got %d", len(r.adapters))
	}
}

func TestRegistryRegisterAndGet(t *testing.T) {
	r := NewRegistry()

	adapter := newMockAdapter(ToolBV, true)
	r.Register(adapter)

	got, ok := r.Get(ToolBV)
	if !ok {
		t.Fatal("Get() returned false for registered adapter")
	}

	if got.Name() != ToolBV {
		t.Errorf("Got adapter name %q, want %q", got.Name(), ToolBV)
	}
}

func TestRegistryGetNotFound(t *testing.T) {
	r := NewRegistry()

	_, ok := r.Get(ToolBV)
	if ok {
		t.Error("Get() should return false for unregistered adapter")
	}
}

func TestRegistryAll(t *testing.T) {
	r := NewRegistry()

	r.Register(newMockAdapter(ToolBV, true))
	r.Register(newMockAdapter(ToolBD, true))
	r.Register(newMockAdapter(ToolCASS, false))

	all := r.All()
	if len(all) != 3 {
		t.Errorf("All() returned %d adapters, want 3", len(all))
	}
}

func TestRegistryDetected(t *testing.T) {
	r := NewRegistry()

	r.Register(newMockAdapter(ToolBV, true))
	r.Register(newMockAdapter(ToolBD, true))
	r.Register(newMockAdapter(ToolCASS, false)) // Not installed

	detected := r.Detected()
	if len(detected) != 2 {
		t.Errorf("Detected() returned %d adapters, want 2", len(detected))
	}
}

func TestRegistryNames(t *testing.T) {
	r := NewRegistry()

	r.Register(newMockAdapter(ToolBV, true))
	r.Register(newMockAdapter(ToolBD, true))

	names := r.Names()
	if len(names) != 2 {
		t.Errorf("Names() returned %d names, want 2", len(names))
	}

	nameSet := make(map[ToolName]bool)
	for _, n := range names {
		nameSet[n] = true
	}

	if !nameSet[ToolBV] || !nameSet[ToolBD] {
		t.Error("Names() missing expected tool names")
	}
}

func TestRegistryGetAllInfo(t *testing.T) {
	r := NewRegistry()

	r.Register(newMockAdapter(ToolBV, true))
	r.Register(newMockAdapter(ToolBD, false))

	ctx := context.Background()
	infos := r.GetAllInfo(ctx)

	if len(infos) != 2 {
		t.Errorf("GetAllInfo() returned %d infos, want 2", len(infos))
	}

	// Check that installed/uninstalled status is correct
	for _, info := range infos {
		switch info.Name {
		case ToolBV:
			if !info.Installed {
				t.Error("ToolBV should be installed")
			}
		case ToolBD:
			if info.Installed {
				t.Error("ToolBD should not be installed")
			}
		}
	}
}

func TestRegistryGetHealthReport(t *testing.T) {
	r := NewRegistry()

	r.Register(newMockAdapter(ToolBV, true))
	r.Register(newMockAdapter(ToolBD, true))
	r.Register(newMockAdapter(ToolCASS, false))

	ctx := context.Background()
	report := r.GetHealthReport(ctx)

	if report.Total != 3 {
		t.Errorf("Total = %d, want 3", report.Total)
	}

	if report.Healthy != 2 {
		t.Errorf("Healthy = %d, want 2", report.Healthy)
	}

	if report.Missing != 1 {
		t.Errorf("Missing = %d, want 1", report.Missing)
	}

	// Check tool states
	if !report.Tools[ToolBV] {
		t.Error("ToolBV should be healthy")
	}
	if !report.Tools[ToolBD] {
		t.Error("ToolBD should be healthy")
	}
	if report.Tools[ToolCASS] {
		t.Error("ToolCASS should not be healthy (missing)")
	}
}

func TestGlobalRegistryFunctions(t *testing.T) {
	// Save current state to restore after test
	oldAdapters := make(map[ToolName]Adapter)
	globalMu.Lock()
	for k, v := range globalRegistry.adapters {
		oldAdapters[k] = v
	}
	globalRegistry.adapters = make(map[ToolName]Adapter)
	globalMu.Unlock()

	// Restore after test
	defer func() {
		globalMu.Lock()
		globalRegistry.adapters = oldAdapters
		globalMu.Unlock()
	}()

	// Test Register
	adapter := newMockAdapter(ToolBV, true)
	Register(adapter)

	// Test Get
	got, ok := Get(ToolBV)
	if !ok {
		t.Fatal("Get() returned false for registered adapter")
	}
	if got.Name() != ToolBV {
		t.Errorf("Got adapter name %q, want %q", got.Name(), ToolBV)
	}

	// Test GetAll
	all := GetAll()
	if len(all) != 1 {
		t.Errorf("GetAll() returned %d adapters, want 1", len(all))
	}

	// Test GetDetected
	detected := GetDetected()
	if len(detected) != 1 {
		t.Errorf("GetDetected() returned %d adapters, want 1", len(detected))
	}

	// Test GetInfo
	ctx := context.Background()
	info, err := GetInfo(ctx, ToolBV)
	if err != nil {
		t.Fatalf("GetInfo() error: %v", err)
	}
	if info.Name != ToolBV {
		t.Errorf("GetInfo() name = %q, want %q", info.Name, ToolBV)
	}

	// Test GetInfo for non-existent tool
	_, err = GetInfo(ctx, ToolCASS)
	if err != ErrToolNotInstalled {
		t.Errorf("GetInfo() for non-existent tool error = %v, want %v", err, ErrToolNotInstalled)
	}

	// Test GetAllInfo
	allInfo := GetAllInfo(ctx)
	if len(allInfo) != 1 {
		t.Errorf("GetAllInfo() returned %d infos, want 1", len(allInfo))
	}

	// Test GetHealthReport
	report := GetHealthReport(ctx)
	if report.Total != 1 {
		t.Errorf("GetHealthReport() Total = %d, want 1", report.Total)
	}

	// Test GlobalRegistry
	if GlobalRegistry() != globalRegistry {
		t.Error("GlobalRegistry() should return globalRegistry")
	}
}
