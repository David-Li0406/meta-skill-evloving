import { describe, it, expect } from '@jest/globals';
import {
  validateAppleScriptArg,
  validateThingsId,
  sanitizeForUrl
} from '../../src/lib/validation.js';
import { ThingsValidationError } from '../../src/lib/errors.js';

describe('validateAppleScriptArg', () => {
  it('should accept valid alphanumeric strings', () => {
    const valid = ['test', 'Test123', 'my-project', 'my_task', 'task.name', 'user@email.com'];

    valid.forEach(arg => {
      expect(() => validateAppleScriptArg(arg, 'field')).not.toThrow();
      expect(validateAppleScriptArg(arg, 'field')).toBe(arg);
    });
  });

  it('should accept strings with allowed special characters', () => {
    const result = validateAppleScriptArg('Project-2023_v1.0@final', 'field');
    expect(result).toBe('Project-2023_v1.0@final');
  });

  it('should accept empty strings (for optional arguments)', () => {
    expect(validateAppleScriptArg('', 'field')).toBe('');
  });

  it('should throw for strings that are too long', () => {
    const longString = 'a'.repeat(10001);
    expect(() => validateAppleScriptArg(longString, 'field'))
      .toThrow(ThingsValidationError);
  });

  it('should throw for strings with dangerous characters (shell injection)', () => {
    const dangerous = ['test`cmd`', 'test$(whoami)', 'test\x00null'];

    dangerous.forEach(arg => {
      expect(() => validateAppleScriptArg(arg, 'testField'))
        .toThrow(ThingsValidationError);
    });
  });

  it('should allow normal punctuation that is not dangerous', () => {
    // These were previously blocked but are now allowed
    const allowed = ['test;', 'test|pipe', 'test<>', 'test&param', 'test#hash'];

    allowed.forEach(arg => {
      expect(() => validateAppleScriptArg(arg, 'field')).not.toThrow();
      expect(validateAppleScriptArg(arg, 'field')).toBe(arg);
    });
  });
});

describe('validateThingsId', () => {
  it('should accept valid Things ID format', () => {
    const validIds = [
      'aBc123dEf456gHi789JkL',
      'xYz789aBc123dEf456gHi',
      'A1B2C3D4E5F67890ABCD'
    ];

    validIds.forEach(id => {
      expect(() => validateThingsId(id)).not.toThrow();
      expect(validateThingsId(id)).toBe(id);
    });
  });

  it('should throw for invalid ID formats', () => {
    const invalidIds = [
      'not-a-valid-id', // Contains hyphens
      'My Vacation Planning', // Project name with spaces
      'My Project Name', // Contains spaces
      'ABC12345-1234-5678-9ABC-DEF123456789', // UUID format (not Things ID)
      'A1B2C3D4E5F67890ABCDEFGHIJKLMNOP', // Too long (32 chars)
      'Short', // Too short
      '35j1Briqg6XBPzPtBDwZJK!', // Contains special character
      ''
    ];

    invalidIds.forEach(id => {
      expect(() => validateThingsId(id))
        .toThrow(new ThingsValidationError(
          'Invalid Things ID format. Expected: alphanumeric string like "aBc123dEf456gHi789JkL" (20-24 characters). NOT the project name!',
          'id'
        ));
    });
  });
});

describe('sanitizeForUrl', () => {
  it('should return normal strings unchanged', () => {
    expect(sanitizeForUrl('Hello World')).toBe('Hello World');
    expect(sanitizeForUrl('Test-123_ABC')).toBe('Test-123_ABC');
  });

  it('should remove control characters', () => {
    expect(sanitizeForUrl('Hello\x00World')).toBe('HelloWorld');
    expect(sanitizeForUrl('Test\x1FString')).toBe('TestString');
    expect(sanitizeForUrl('\x7FStart')).toBe('Start');
  });

  it('should handle multiple control characters', () => {
    expect(sanitizeForUrl('A\x00B\x1FC\x7FD')).toBe('ABCD');
  });

  it('should preserve regular whitespace', () => {
    expect(sanitizeForUrl('Hello World')).toBe('Hello World');
    expect(sanitizeForUrl('Line 1\nLine 2')).toBe('Line 1\nLine 2');
  });
});
