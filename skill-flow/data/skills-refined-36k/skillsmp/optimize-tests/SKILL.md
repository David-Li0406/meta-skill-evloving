---
name: optimize-tests
description: Identifies redundant or duplicate test cases, removes them while ensuring test coverage is not reduced.
---
# Optimize Tests

## Instructions

### Phase 1: Initial Assessment

1. **Run initial coverage baseline**:
   ```bash
   make coverage
   ```
   Record the initial coverage percentage as the baseline. Coverage must not drop below this.

2. **Find all test files in the specified directory**:
   ```bash
   find <directory> -name "*_test.go" -type f
   ```
   Create a list of all test files to process.

### Phase 2: Analyze and Optimize Each File

For each test file, perform the following steps:

1. **Read the test file** to understand its structure and test cases.

2. **Identify redundant patterns**:
   - Duplicate test cases (same logic, different names)
   - Tests that cover identical code paths
   - Overlapping table-driven test cases with redundant entries
   - Tests that are subsets of other more comprehensive tests
   - Mock setups that are duplicated across multiple tests
   - Helper functions that duplicate existing test utilities

3. **Analyze test coverage contribution**:
   - Determine which tests are essential for coverage
   - Identify tests that don't add unique coverage value
   - Consider edge cases and error paths

4. **Make targeted edits**:
   - Remove only clearly redundant test cases
   - Consolidate duplicate table-driven test entries
   - Extract common mock setups if beneficial
   - Preserve all tests that contribute unique coverage

5. **Verify coverage after each file**:
   ```bash
   make coverage
   ```
   - If coverage dropped or CRITICAL issue reported: **immediately revert the changes** and try a more conservative approach
   - If coverage is maintained or improved: proceed to commit

6. **Commit the changes**:
   - Stage the modified file: `git add <file>`
   - Create a descriptive commit message:
   ```bash
   git commit -m "refactor(<package>): remove redundant test cases in <filename>

   - Removed N redundant test cases
   - Consolidated duplicate table entries
   - Coverage maintained at X%"
   ```

### Phase 3: Summary

After processing all files, provide a summary:
- Number of files processed
- Number of files optimized
- Test cases removed per file
- Final coverage percentage vs baseline

## Guidelines

### What to Remove
- Exact duplicate tests (same assertions, same setup)
- Table-driven test entries that test identical scenarios
- Tests that are strict subsets of more comprehensive tests
- Commented-out test code
- Unused test helper functions

### What to KEEP
- Tests covering unique code paths
- Edge case tests (nil, empty, boundary values)
- Error handling tests
- Tests with different mock behaviors leading to different outcomes
- Integration-style tests even if unit tests exist for same code
- Any test where removal would reduce coverage

### Safety Rules
- **NEVER reduce test coverage** - this is the primary constraint
- Process ONE file at a time
- Run `make coverage` after EVERY file modification
- If coverage drops, immediately revert and move to the next file
- When in doubt, keep the test
- Create atomic commits (one file per commit)

### Commit Message Standards
- Use conventional commit format: `refactor(<scope>): <description>`
- Scope should be the package name
- Filename should be a part of description
- Description should summarize what was removed
- Body should list specific changes and coverage status
- Do NOT add any co-author credits

## Important Behaviors

- If no redundant tests are found in a file, skip it and move on
- If coverage cannot be maintained after removing tests, keep all tests in that file
- Always show progress: "Processing file X of Y: <filename>"
- Report both successes and skipped files in the final summary
- If the directory doesn't exist or has no test files, inform the user

## Examples

### Example 1: Removing Duplicate Test

From `internal/streamer/remote_stream_test.go`:

**Before** (two tests with identical logic):
```go
func TestRemoteStream_Recv_EventDelivery(t *testing.T) {
	mockStream := &mockGRPCStreamClient{
		recvMsgs: []*pb.StreamerMessage{{
			Payload: &pb.StreamerMessage_Delivery{
				Delivery: &pb.EventDelivery{
					SubscriptionIds: []string{"sub1"},
					Event: &pb.StreamerEvent{
						EventId: "evt1", Database: "database1", Collection: "users",
					},
				},
			},
		}},
	}
	rs := &remoteStream{ctx: context.Background(), grpcStream: mockStream, logger: slog.Default()}
	delivery, err := rs.Recv()
	require.NoError(t, err)
	assert.Equal(t, []string{"sub1"}, delivery.SubscriptionIDs)
	assert.Equal(t, "evt1", delivery.Event.EventID)
}

func TestRemoteStream_Success(t *testing.T) {
	mockStream := &mockGRPCStreamClient{
		recvMsgs: []*pb.StreamerMessage{{
			Payload: &pb.StreamerMessage_Delivery{
				Delivery: &pb.EventDelivery{
					SubscriptionIds: []string{"sub1"},
					Event: &pb.StreamerEvent{
						Database: "database1", Collection: "users", DocumentId: "doc1",
					},
				},
			},
		}},
	}
	rs := &remoteStream{ctx: context.Background(), grpcStream: mockStream, logger: slog.Default()}
	delivery, err := rs.Recv()
	require.NoError(t, err)
	assert.Equal(t, "users", delivery.Event.Collection)
}
```

**After** (keep only one):
```go
func TestRemoteStream_Recv_EventDelivery(t *testing.T) {
	mockStream := &mockGRPCStreamClient{
		recvMsgs: []*pb.StreamerMessage{{
			Payload: &pb.StreamerMessage_Delivery{
				Delivery: &pb.EventDelivery{
					SubscriptionIds: []string{"sub1"},
					Event: &pb.StreamerEvent{
						EventId: "evt1", Database: "database1", Collection: "users",
					},
				},
			},
		}},
	}
	rs := &remoteStream{ctx: context.Background(), grpcStream: mockStream, logger: slog.Default()}
	delivery, err := rs.Recv()
	require.NoError(t, err)
	assert.Equal(t, []string{"sub1"}, delivery.SubscriptionIDs)
	assert.Equal(t, "evt1", delivery.Event.EventID)
}
// TestRemoteStream_Success REMOVED - same code path, same assertions
```

---

### Example 2: Removing Test Subsumed by Another

From `internal/streamer/grpc_adapter_test.go`:

**Before** (two tests, one is subset of the other):
```go
func TestGRPCStream_SubscribeMessage(t *testing.T) {
	// ... setup ...
	mockStream := &mockBidiStream{
		recvMsgs: []*pb.GatewayMessage{{
			Payload: &pb.GatewayMessage_Subscribe{
				Subscribe: &pb.SubscribeRequest{SubscriptionId: "sub1", Database: "db1", Collection: "users"},
			},
		}},
	}
	go func() { done <- internal.GRPCStream(mockStream) }()
	time.Sleep(30 * time.Millisecond)
	cancel()
	<-done
	// Test passes as long as it doesn't hang or panic  <-- NO ASSERTION
}

func TestGRPCAdapter_Subscribe_ManagerError(t *testing.T) {
	// ... setup ...
	mockStream := &mockBidiStream{
		recvMsgs: []*pb.GatewayMessage{
			{Payload: &pb.GatewayMessage_Subscribe{Subscribe: &pb.SubscribeRequest{SubscriptionId: "dup-id", ...}}},
			{Payload: &pb.GatewayMessage_Subscribe{Subscribe: &pb.SubscribeRequest{SubscriptionId: "dup-id", ...}}},
		},
	}
	// ... run stream ...
	// Verify both responses were sent
	require.GreaterOrEqual(t, len(mockStream.sentMsgs), 2)
	resp1 := mockStream.sentMsgs[0].GetSubscribeResponse()
	assert.True(t, resp1.Success)  // <-- HAS ASSERTIONS
	resp2 := mockStream.sentMsgs[1].GetSubscribeResponse()
	assert.False(t, resp2.Success)
}
```

**After** (keep only the one with assertions):
```go
// TestGRPCStream_SubscribeMessage REMOVED - no assertions, subsumed by TestGRPCAdapter_Subscribe_ManagerError

func TestGRPCAdapter_Subscribe_ManagerError(t *testing.T) {
	// ... setup ...
	mockStream := &mockBidiStream{
		recvMsgs: []*pb.GatewayMessage{
			{Payload: &pb.GatewayMessage_Subscribe{Subscribe: &pb.SubscribeRequest{SubscriptionId: "dup-id", ...}}},
			{Payload: &pb.GatewayMessage_Subscribe{Subscribe: &pb.SubscribeRequest{SubscriptionId: "dup-id", ...}}},
		},
	}
	// ... run stream ...
	require.GreaterOrEqual(t, len(mockStream.sentMsgs), 2)
	resp1 := mockStream.sentMsgs[0].GetSubscribeResponse()
	assert.True(t, resp1.Success)
	resp2 := mockStream.sentMsgs[1].GetSubscribeResponse()
	assert.False(t, resp2.Success)
}
```

---

### Example 3: Merging Idempotent Check into Existing Test

From `internal/streamer/remote_stream_test.go`:

**Before** (two separate tests):
```go
func TestRemoteStream_Close(t *testing.T) {
	mockStream := &mockGRPCStreamClient{}
	rs := &remoteStream{ctx: context.Background(), grpcStream: mockStream, logger: slog.Default()}
	err := rs.Close()
	require.NoError(t, err)
	assert.True(t, mockStream.closedSend)
}

func TestRemoteStream_Close_Idempotent(t *testing.T) {
	mockStream := &mockGRPCStreamClient{}
	rs := &remoteStream{ctx: context.Background(), grpcStream: mockStream, logger: slog.Default()}
	err := rs.Close()
	require.NoError(t, err)
	// Second close should be no-op
	err = rs.Close()
	require.NoError(t, err)
}
```

**After** (merged into one):
```go
func TestRemoteStream_Close(t *testing.T) {
	mockStream := &mockGRPCStreamClient{}
	rs := &remoteStream{ctx: context.Background(), grpcStream: mockStream, logger: slog.Default()}

	// First close should work
	err := rs.Close()
	require.NoError(t, err)
	assert.True(t, mockStream.closedSend)

	// Second close should be no-op (idempotent)
	err = rs.Close()
	require.NoError(t, err)
}
```
