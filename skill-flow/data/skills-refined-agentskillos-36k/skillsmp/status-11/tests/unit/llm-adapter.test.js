const path = require('path');

describe('llm-adapter', () => {
  let LLMAdapter;

  beforeEach(() => {
    jest.resetModules();
    // Mock fetch globally
    global.fetch = jest.fn();
    global.AbortController = class {
      constructor() {
        this.signal = {};
      }
      abort() {}
    };
    LLMAdapter = require(path.join(process.cwd(), 'web/demo/js/llm-adapter.js'));
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('constants', () => {
    it('exports DEFAULT_BASE_URL', () => {
      expect(LLMAdapter.DEFAULT_BASE_URL).toBe('https://api.openai.com/v1/chat/completions');
    });

    it('exports DEFAULT_MODEL', () => {
      expect(LLMAdapter.DEFAULT_MODEL).toBe('gpt-4o-mini');
    });

    it('exports DEFAULT_TIMEOUT_MS', () => {
      expect(LLMAdapter.DEFAULT_TIMEOUT_MS).toBe(5000);
    });

    it('exports ErrorType enum', () => {
      expect(LLMAdapter.ErrorType.TIMEOUT).toBe('timeout');
      expect(LLMAdapter.ErrorType.NETWORK).toBe('network');
      expect(LLMAdapter.ErrorType.API_ERROR).toBe('api_error');
      expect(LLMAdapter.ErrorType.RATE_LIMIT).toBe('rate_limit');
      expect(LLMAdapter.ErrorType.INVALID_KEY).toBe('invalid_key');
      expect(LLMAdapter.ErrorType.PARSE_ERROR).toBe('parse_error');
    });
  });

  describe('creativityToTemperature', () => {
    it('maps 0.0 to 0.0', () => {
      expect(LLMAdapter.creativityToTemperature(0)).toBe(0);
    });

    it('maps 0.5 to 1.0', () => {
      expect(LLMAdapter.creativityToTemperature(0.5)).toBe(1.0);
    });

    it('maps 1.0 to 2.0', () => {
      expect(LLMAdapter.creativityToTemperature(1.0)).toBe(2.0);
    });

    it('clamps values below 0', () => {
      expect(LLMAdapter.creativityToTemperature(-0.5)).toBe(0);
    });

    it('clamps values above 1', () => {
      expect(LLMAdapter.creativityToTemperature(1.5)).toBe(2.0);
    });
  });

  describe('parseJsonResponse', () => {
    it('parses valid JSON directly', () => {
      const result = LLMAdapter.parseJsonResponse('{"test": true}');
      expect(result.success).toBe(true);
      expect(result.data).toEqual({ test: true });
    });

    it('extracts JSON from markdown code blocks', () => {
      const input = 'Here is the response:\n```json\n{"test": true}\n```';
      const result = LLMAdapter.parseJsonResponse(input);
      expect(result.success).toBe(true);
      expect(result.data).toEqual({ test: true });
    });

    it('extracts JSON object from mixed text', () => {
      const input = 'Some text before {"test": true} and after';
      const result = LLMAdapter.parseJsonResponse(input);
      expect(result.success).toBe(true);
      expect(result.data).toEqual({ test: true });
    });

    it('returns error for empty input', () => {
      const result = LLMAdapter.parseJsonResponse('');
      expect(result.success).toBe(false);
      expect(result.error).toBe('Empty response');
    });

    it('returns error for null input', () => {
      const result = LLMAdapter.parseJsonResponse(null);
      expect(result.success).toBe(false);
    });

    it('returns error for invalid JSON', () => {
      const result = LLMAdapter.parseJsonResponse('not valid json at all');
      expect(result.success).toBe(false);
      expect(result.error).toBe('No valid JSON found in response');
    });
  });

  describe('generateProposalId', () => {
    it('generates UUID-like strings', () => {
      const id = LLMAdapter.generateProposalId();
      expect(id).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
    });

    it('generates unique IDs', () => {
      const ids = new Set();
      for (let i = 0; i < 100; i++) {
        ids.add(LLMAdapter.generateProposalId());
      }
      expect(ids.size).toBe(100);
    });
  });

  describe('generateProposal', () => {
    it('returns error when API key is missing', async () => {
      const result = await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test'
      });

      expect(result.error).toBe(true);
      expect(result.type).toBe('invalid_key');
    });

    it('returns error when prompts are missing', async () => {
      const result = await LLMAdapter.generateProposal({
        apiKey: 'sk-test-key-12345678901234567890'
      });

      expect(result.error).toBe(true);
      expect(result.message).toContain('prompts are required');
    });

    it('uses default baseUrl when not specified', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-test-key-12345678901234567890'
      });

      expect(global.fetch).toHaveBeenCalledWith(
        'https://api.openai.com/v1/chat/completions',
        expect.any(Object)
      );
    });

    it('uses custom baseUrl when specified', async () => {
      const customUrl = 'http://localhost:11434/v1/chat/completions';
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-test-key-12345678901234567890',
        baseUrl: customUrl
      });

      expect(global.fetch).toHaveBeenCalledWith(
        customUrl,
        expect.any(Object)
      );
    });

    it('includes response_format when useJsonMode is true', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-test-key-12345678901234567890',
        useJsonMode: true
      });

      const fetchCall = global.fetch.mock.calls[0];
      const body = JSON.parse(fetchCall[1].body);
      expect(body.response_format).toEqual({ type: 'json_object' });
    });

    it('omits response_format when useJsonMode is false', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-test-key-12345678901234567890',
        useJsonMode: false
      });

      const fetchCall = global.fetch.mock.calls[0];
      const body = JSON.parse(fetchCall[1].body);
      expect(body.response_format).toBeUndefined();
    });

    it('includes extra headers when specified', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-test-key-12345678901234567890',
        extraHeaders: { 'X-Custom-Header': 'custom-value' }
      });

      const fetchCall = global.fetch.mock.calls[0];
      expect(fetchCall[1].headers['X-Custom-Header']).toBe('custom-value');
    });

    it('uses api-key header for Azure OpenAI endpoints', async () => {
      const azureUrl = 'https://myresource.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-02-15';
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'azure-api-key-12345',
        baseUrl: azureUrl
      });

      const fetchCall = global.fetch.mock.calls[0];
      expect(fetchCall[1].headers['api-key']).toBe('azure-api-key-12345');
      expect(fetchCall[1].headers['Authorization']).toBeUndefined();
    });

    it('uses api-key header for Azure Cognitive Services endpoints', async () => {
      const azureUrl = 'https://myresource.cognitiveservices.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-02-15';
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'azure-api-key-12345',
        baseUrl: azureUrl
      });

      const fetchCall = global.fetch.mock.calls[0];
      expect(fetchCall[1].headers['api-key']).toBe('azure-api-key-12345');
      expect(fetchCall[1].headers['Authorization']).toBeUndefined();
    });

    it('omits model field for Azure endpoints', async () => {
      const azureUrl = 'https://myresource.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-02-15';
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'azure-api-key-12345',
        baseUrl: azureUrl
      });

      const fetchCall = global.fetch.mock.calls[0];
      const body = JSON.parse(fetchCall[1].body);
      expect(body.model).toBeUndefined();
    });

    it('includes model field for non-Azure endpoints', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-test-key-12345678901234567890'
      });

      const fetchCall = global.fetch.mock.calls[0];
      const body = JSON.parse(fetchCall[1].body);
      expect(body.model).toBe('gpt-4o-mini');
    });

    it('uses Bearer token for non-Azure endpoints', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-test-key-12345678901234567890'
      });

      const fetchCall = global.fetch.mock.calls[0];
      expect(fetchCall[1].headers['Authorization']).toBe('Bearer sk-test-key-12345678901234567890');
      expect(fetchCall[1].headers['api-key']).toBeUndefined();
    });

    it('includes endpoint in metadata', async () => {
      const customUrl = 'http://localhost:11434/v1/chat/completions';
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      const result = await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-test-key-12345678901234567890',
        baseUrl: customUrl
      });

      expect(result._meta.endpoint).toBe(customUrl);
    });

    it('handles 401 as invalid key error', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        statusText: 'Unauthorized',
        text: () => Promise.resolve('{"error": "invalid_api_key"}')
      });

      const result = await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-invalid-key-1234567890123456'
      });

      expect(result.error).toBe(true);
      expect(result.type).toBe('invalid_key');
    });

    it('handles 429 as rate limit error', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 429,
        statusText: 'Too Many Requests',
        text: () => Promise.resolve('{}')
      });

      const result = await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-test-key-12345678901234567890'
      });

      expect(result.error).toBe(true);
      expect(result.type).toBe('rate_limit');
    });

    it('handles 500+ as service error', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        text: () => Promise.resolve('{}')
      });

      const result = await LLMAdapter.generateProposal({
        systemPrompt: 'Test',
        userPrompt: 'Test',
        apiKey: 'sk-test-key-12345678901234567890'
      });

      expect(result.error).toBe(true);
      expect(result.type).toBe('api_error');
      expect(result.message).toBe('LLM service error');
    });
  });

  describe('testConnection', () => {
    it('returns success for valid response', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      const result = await LLMAdapter.testConnection('sk-test-key-12345678901234567890');
      expect(result.success).toBe(true);
    });

    it('returns error for failed response', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        statusText: 'Unauthorized',
        text: () => Promise.resolve('{}')
      });

      const result = await LLMAdapter.testConnection('sk-invalid-key-1234567890123456');
      expect(result.success).toBe(false);
      expect(result.error).toBeDefined();
    });

    it('accepts custom baseUrl', async () => {
      const customUrl = 'http://localhost:11434/v1/chat/completions';
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.testConnection('sk-test-key-12345678901234567890', {
        baseUrl: customUrl
      });

      expect(global.fetch).toHaveBeenCalledWith(
        customUrl,
        expect.any(Object)
      );
    });

    it('accepts useJsonMode option', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({
          choices: [{ message: { content: '{"test": true}' } }]
        })
      });

      await LLMAdapter.testConnection('sk-test-key-12345678901234567890', {
        useJsonMode: false
      });

      const fetchCall = global.fetch.mock.calls[0];
      const body = JSON.parse(fetchCall[1].body);
      expect(body.response_format).toBeUndefined();
    });
  });
});
