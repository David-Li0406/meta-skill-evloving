# Mcp Testing - Sharp Edges

## Schema Test Gaps

### **Id**
schema-test-gaps
### **Summary**
Schema tests pass but AI still sends invalid data
### **Severity**
high
### **Situation**
Tests pass, production fails with unexpected AI inputs
### **Why**
  Schema validates syntax, not semantics.
  AI combines valid fields in invalid ways.
  Edge cases not covered by schema.
  
### **Solution**
  // Test semantic combinations, not just syntax
  
  describe('Semantic Validation', () => {
      // Schema allows both, but combination is invalid
      it('rejects conflicting options', async () => {
          const result = await callTool('create_project', {
              name: 'test',
              template: 'minimal',
              features: ['full-auth', 'analytics']  // Invalid for minimal
          });
          expect(result.isError).toBe(true);
      });
  
      // Schema allows, but logic requires order
      it('validates operation order', async () => {
          const result = await callTool('deploy', {
              environment: 'production',
              // Missing required pre-deployment checks
          });
          expect(result.isError).toBe(true);
      });
  
      // Schema allows, but context makes invalid
      it('validates against current state', async () => {
          // First, put system in specific state
          await callTool('set_mode', { mode: 'maintenance' });
  
          // This operation should be blocked in maintenance
          const result = await callTool('create_project', {
              name: 'test'
          });
          expect(result.isError).toBe(true);
          expect(result.content[0].text).toContain('maintenance');
      });
  });
  
### **Symptoms**
  - Tests pass, production has errors
  - AI creates invalid combinations
  - State-dependent bugs
### **Detection Pattern**
describe|it\(|test\(

## Mock Hiding Bugs

### **Id**
mock-hiding-bugs
### **Summary**
Mocked tests pass, integration fails
### **Severity**
high
### **Situation**
Unit tests 100% pass, real connections fail
### **Why**
  Mocks don't replicate real service behavior.
  Network issues, timeouts, rate limits not mocked.
  State changes not propagated to mocks.
  
### **Solution**
  // Use real services in integration tests
  
  describe('Integration with Real Database', () => {
      let testDb: TestDatabase;
  
      beforeAll(async () => {
          // Use real database, not mock
          testDb = await TestDatabase.create();
      });
  
      afterAll(async () => {
          await testDb.cleanup();
      });
  
      it('handles concurrent access', async () => {
          // Real race condition testing
          const promises = [];
          for (let i = 0; i < 10; i++) {
              promises.push(callTool('increment_counter', { id: 'shared' }));
          }
  
          await Promise.all(promises);
          const result = await callTool('get_counter', { id: 'shared' });
          expect(JSON.parse(result.content[0].text).value).toBe(10);
      });
  
      it('handles database timeouts', async () => {
          // Induce slow query
          await testDb.setLatency(5000);
  
          const result = await callTool('slow_query', { timeout: 1000 });
          expect(result.isError).toBe(true);
          expect(result.content[0].text).toContain('timeout');
      });
  });
  
### **Symptoms**
  - Unit tests pass, integration fails
  - Works locally, fails in production
  - Race conditions in production only
### **Detection Pattern**
mock|Mock|jest\.fn|vi\.fn

## Inspector False Confidence

### **Id**
inspector-false-confidence
### **Summary**
MCP Inspector shows success, real clients fail
### **Severity**
medium
### **Situation**
Inspector works, Claude integration fails
### **Why**
  Inspector may be more lenient than real clients.
  Request format differs slightly.
  Timing and ordering not tested.
  
### **Solution**
  // Test with real MCP clients, not just Inspector
  
  describe('Real Client Compatibility', () => {
      it('works with Claude Code transport', async () => {
          // Use the same transport Claude Code uses
          const transport = new StdioClientTransport({
              command: 'node',
              args: ['dist/index.js'],
              env: { ...process.env, MCP_CLIENT: 'claude-code' }
          });
  
          const client = new Client({ name: 'claude-code-test' });
          await client.connect(transport);
  
          // Test real interaction pattern
          const tools = await client.listTools();
          expect(tools.length).toBeGreaterThan(0);
  
          await client.close();
      });
  
      it('handles rapid sequential requests', async () => {
          // Claude can send requests quickly
          for (let i = 0; i < 20; i++) {
              const result = await client.callTool('quick_op', { n: i });
              expect(result.isError).toBeFalsy();
          }
      });
  });
  
### **Symptoms**
  - Inspector works, Claude fails
  - Works in isolation, fails in real use
  - Intermittent failures with real clients
### **Detection Pattern**
Inspector|inspector|Client