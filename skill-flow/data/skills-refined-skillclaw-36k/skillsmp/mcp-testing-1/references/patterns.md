# MCP Testing

## Patterns


---
  #### **Name**
Schema Validation Tests
  #### **Description**
Test that tool schemas are valid and complete
  #### **When**
Any tool definition
  #### **Example**
    import { describe, it, expect } from 'vitest';
    import { validateSchema } from '../src/schema-validator';
    
    describe('Tool Schemas', () => {
        it('all tools have valid inputSchema', () => {
            const tools = getToolDefinitions();
            for (const tool of tools) {
                expect(tool.inputSchema).toBeDefined();
                expect(tool.inputSchema.type).toBe('object');
                expect(validateSchema(tool.inputSchema)).toBe(true);
            }
        });
    
        it('all tools have descriptions', () => {
            const tools = getToolDefinitions();
            for (const tool of tools) {
                expect(tool.description).toBeTruthy();
                expect(tool.description.length).toBeGreaterThan(20);
            }
        });
    
        it('required fields are defined in properties', () => {
            const tools = getToolDefinitions();
            for (const tool of tools) {
                const required = tool.inputSchema.required || [];
                const properties = Object.keys(tool.inputSchema.properties || {});
                for (const field of required) {
                    expect(properties).toContain(field);
                }
            }
        });
    });
    

---
  #### **Name**
Tool Handler Tests
  #### **Description**
Test tool execution with various inputs
  #### **When**
Testing tool implementations
  #### **Example**
    describe('create_project tool', () => {
        it('creates project with valid input', async () => {
            const result = await callTool('create_project', {
                name: 'test-project',
                template: 'web'
            });
    
            expect(result.isError).toBeFalsy();
            expect(result.content[0].text).toContain('created');
        });
    
        it('rejects invalid project name', async () => {
            const result = await callTool('create_project', {
                name: 'Invalid Name!',  // Contains invalid chars
                template: 'web'
            });
    
            expect(result.isError).toBe(true);
            expect(result.content[0].text).toContain('invalid');
        });
    
        it('handles missing required fields', async () => {
            const result = await callTool('create_project', {
                // Missing name and template
            });
    
            expect(result.isError).toBe(true);
        });
    
        it('handles unexpected extra fields', async () => {
            const result = await callTool('create_project', {
                name: 'test-project',
                template: 'web',
                unknownField: 'should be ignored or rejected'
            });
    
            // Depending on strictness
            expect(result.isError).toBe(true);
        });
    });
    

---
  #### **Name**
Integration Tests
  #### **Description**
Test full request/response cycle
  #### **When**
Testing complete MCP server
  #### **Example**
    import { Client } from '@modelcontextprotocol/sdk/client/index.js';
    import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
    
    describe('MCP Server Integration', () => {
        let client: Client;
    
        beforeAll(async () => {
            const transport = new StdioClientTransport({
                command: 'node',
                args: ['dist/index.js']
            });
            client = new Client({ name: 'test-client' });
            await client.connect(transport);
        });
    
        afterAll(async () => {
            await client.close();
        });
    
        it('lists tools successfully', async () => {
            const tools = await client.listTools();
            expect(tools.length).toBeGreaterThan(0);
        });
    
        it('executes tool and returns result', async () => {
            const result = await client.callTool('health_check', {});
            expect(result.content[0].text).toContain('healthy');
        });
    
        it('lists resources successfully', async () => {
            const resources = await client.listResources();
            expect(resources.length).toBeGreaterThan(0);
        });
    
        it('reads resource successfully', async () => {
            const content = await client.readResource('config://settings');
            expect(content.contents[0].text).toBeTruthy();
        });
    });
    

## Anti-Patterns


---
  #### **Name**
Testing Happy Path Only
  #### **Description**
Only testing successful scenarios
  #### **Why**
AI sends unexpected inputs, edge cases are common
  #### **Instead**
Test errors, edge cases, and boundary conditions.

---
  #### **Name**
Mocking Everything
  #### **Description**
Unit tests that mock all dependencies
  #### **Why**
MCP is about integration, mocks hide real issues
  #### **Instead**
Favor integration tests over heavily mocked unit tests.

---
  #### **Name**
No Schema Tests
  #### **Description**
Skipping JSON schema validation tests
  #### **Why**
Invalid schemas cause runtime failures
  #### **Instead**
Test schema validity and completeness first.