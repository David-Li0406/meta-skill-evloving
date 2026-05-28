import { SimpleParser } from '../core/parser';

describe('SimpleParser', () => {
  test('parses TypeScript symbols correctly', () => {
    const code = `
      import { Foo } from './foo';
      export class MyClass {
        async myMethod(a: string) {}
        static syncMethod() {}
      }
      export async function myFunction() {}
      const myArrow = async (x: number) => x * 2;
      export const exportedArrow = () => {};
      function internalFunc() {}
      export default class DefaultClass {}
    `;
    const result = SimpleParser.parse('test.ts', code);

    expect(result.language).toBe('typescript');
    expect(result.imports).toContainEqual({ path: './foo' });

    // Check class and methods
    const cls = result.symbols.find((s) => s.name === 'MyClass' && s.kind === 'class');
    expect(cls).toBeDefined();
    expect(result.symbols.find((s) => s.name === 'MyClass.myMethod')).toBeDefined();
    expect(result.symbols.find((s) => s.name === 'MyClass.syncMethod')).toBeDefined();

    // Check async function
    const asyncFunc = result.symbols.find((s) => s.name === 'myFunction');
    expect(asyncFunc).toBeDefined();
    expect(asyncFunc?.exported).toBe(true);

    // Check arrows
    expect(result.symbols.find((s) => s.name === 'myArrow')).toBeDefined();
    expect(result.symbols.find((s) => s.name === 'exportedArrow')).toBeDefined();

    // Check default export
    expect(result.symbols.find((s) => s.name === 'DefaultClass' && s.exported)).toBeDefined();
  });

  test('parses Python symbols correctly', () => {
    const code = [
      'from module import Something',
      'class MyPyClass(Base):',
      '    async def async_method(self): pass',
      '    def sync_method(self): pass',
      'async def top_level_async(): pass',
      'def top_level_sync(): pass',
    ].join('\n');
    const result = SimpleParser.parse('test.py', code);

    expect(result.language).toBe('python');
    expect(result.imports).toContainEqual({ path: 'module' });

    const cls = result.symbols.find((s) => s.name === 'MyPyClass');
    expect(cls).toBeDefined();

    expect(result.symbols.find((s) => s.name === 'MyPyClass.async_method')).toBeDefined();
    expect(result.symbols.find((s) => s.name === 'MyPyClass.sync_method')).toBeDefined();
    expect(result.symbols.find((s) => s.name === 'top_level_async')).toBeDefined();
    expect(result.symbols.find((s) => s.name === 'top_level_sync')).toBeDefined();
  });
});