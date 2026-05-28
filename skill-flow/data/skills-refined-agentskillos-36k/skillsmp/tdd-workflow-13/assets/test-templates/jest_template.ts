/**
 * Jest 테스트 템플릿
 *
 * Usage:
 *   cp jest_template.ts src/__tests__/<module>.test.ts
 *
 * TDD 규칙:
 *   1. Red Phase: 이 템플릿으로 실패하는 테스트 먼저 작성
 *   2. Green Phase: 테스트 통과하는 최소 구현
 *   3. Refactor Phase: 코드 정리 (테스트 유지)
 */

// import { functionUnderTest, ClassName } from '../module';

describe('ModuleName', () => {
  // === 테스트 설정 ===

  beforeAll(() => {
    // 전체 테스트 전 1회 실행
  });

  afterAll(() => {
    // 전체 테스트 후 1회 실행
  });

  beforeEach(() => {
    // 각 테스트 전 실행
    jest.clearAllMocks();
  });

  afterEach(() => {
    // 각 테스트 후 실행
  });

  // === 정상 케이스 ===

  describe('functionUnderTest', () => {
    it('should return expected value when valid input', () => {
      // Given
      const input = 'test';

      // When
      // const result = functionUnderTest(input);

      // Then
      // expect(result).toBe('expected');
      expect(true).toBe(true); // TODO: 구현 필요
    });

    it('should handle empty input', () => {
      // Given
      const input = '';

      // When
      // const result = functionUnderTest(input);

      // Then
      // expect(result).toBeDefined();
      expect(true).toBe(true); // TODO: 구현 필요
    });
  });

  // === 예외 케이스 ===

  describe('error handling', () => {
    it('should throw error when invalid input', () => {
      // Given
      const invalidInput = null;

      // When / Then
      // expect(() => functionUnderTest(invalidInput)).toThrow('Invalid input');
      expect(() => {
        throw new Error('Invalid input');
      }).toThrow('Invalid input');
    });

    it('should throw TypeError when wrong type', () => {
      // Given
      const wrongTypeInput = 12345;

      // When / Then
      // expect(() => functionUnderTest(wrongTypeInput)).toThrow(TypeError);
      expect(() => {
        throw new TypeError('Wrong type');
      }).toThrow(TypeError);
    });
  });

  // === 경계 케이스 ===

  describe('boundary conditions', () => {
    it.each([
      ['', ''],           // 빈 문자열
      ['a', 'a'],         // 단일 문자
      ['abc', 'abc'],     // 일반 문자열
    ])('should handle input "%s" and return "%s"', (input, expected) => {
      // When
      // const result = functionUnderTest(input);

      // Then
      // expect(result).toBe(expected);
      expect(input).toBe(input); // TODO: 구현 필요
    });
  });

  // === 클래스 테스트 ===

  describe('ClassName', () => {
    let instance: any; // ClassName

    beforeEach(() => {
      // instance = new ClassName();
    });

    it('should create instance', () => {
      // expect(instance).toBeDefined();
      expect(true).toBe(true); // TODO: 구현 필요
    });

    it('should have method', () => {
      // expect(instance.method).toBeDefined();
      expect(true).toBe(true); // TODO: 구현 필요
    });
  });

  // === 비동기 테스트 ===

  describe('async operations', () => {
    it('should resolve with expected value', async () => {
      // Given
      const input = 'test';

      // When
      // const result = await asyncFunction(input);

      // Then
      // expect(result).toBe('expected');
      await expect(Promise.resolve('test')).resolves.toBe('test');
    });

    it('should reject with error', async () => {
      // Given
      const invalidInput = null;

      // When / Then
      // await expect(asyncFunction(invalidInput)).rejects.toThrow('Error');
      await expect(Promise.reject(new Error('Error'))).rejects.toThrow('Error');
    });
  });

  // === Mock 테스트 ===

  describe('with mocks', () => {
    it('should call dependency with correct args', () => {
      // Given
      const mockDependency = jest.fn().mockReturnValue('mocked');

      // When
      // functionWithDependency(mockDependency);

      // Then
      // expect(mockDependency).toHaveBeenCalledWith('expected arg');
      mockDependency('test');
      expect(mockDependency).toHaveBeenCalledWith('test');
    });
  });
});
