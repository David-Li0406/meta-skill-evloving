# Vitest Assertions

## Equality

```typescript
expect(value).toBe(expected)           // Strict equality (===)
expect(value).toEqual(expected)        // Deep equality
expect(value).toStrictEqual(expected)  // Deep + same structure
expect(value).toMatchObject(partial)   // Partial match
```

## Truthiness

```typescript
expect(value).toBeTruthy()
expect(value).toBeFalsy()
expect(value).toBeNull()
expect(value).toBeUndefined()
expect(value).toBeDefined()
expect(value).toBeNaN()
```

## Numbers

```typescript
expect(num).toBeGreaterThan(3)
expect(num).toBeGreaterThanOrEqual(3)
expect(num).toBeLessThan(5)
expect(num).toBeLessThanOrEqual(5)
expect(num).toBeCloseTo(0.3, 5)  // Floating point (5 decimal places)
```

## Strings

```typescript
expect(str).toMatch(/regex/)
expect(str).toMatch('substring')
expect(str).toContain('substring')
expect(str).toHaveLength(5)
```

## Arrays

```typescript
expect(arr).toContain(item)
expect(arr).toContainEqual({ id: 1 })  // Deep equality check
expect(arr).toHaveLength(3)
expect(arr).toEqual(expect.arrayContaining([1, 2]))
```

## Objects

```typescript
expect(obj).toHaveProperty('key')
expect(obj).toHaveProperty('nested.key', 'value')
expect(obj).toMatchObject({ key: 'value' })
expect(obj).toEqual(expect.objectContaining({ key: 'value' }))
```

## Exceptions

```typescript
expect(() => fn()).toThrow()
expect(() => fn()).toThrow('message')
expect(() => fn()).toThrow(/regex/)
expect(() => fn()).toThrow(ErrorClass)
expect(async () => fn()).rejects.toThrow()
```

## Promises

```typescript
await expect(promise).resolves.toBe('value')
await expect(promise).rejects.toThrow()
await expect(promise).rejects.toMatchObject({ code: 'ERR' })
```

## Snapshots

```typescript
expect(value).toMatchSnapshot()
expect(value).toMatchInlineSnapshot(`"expected"`)
expect(value).toMatchFileSnapshot('./snapshot.txt')
```

## Negation

```typescript
expect(value).not.toBe(other)
expect(value).not.toContain(item)
```

## Asymmetric Matchers

```typescript
expect.any(Constructor)      // Any instance of type
expect.anything()            // Any non-null/undefined
expect.stringContaining(str)
expect.stringMatching(/regex/)
expect.arrayContaining(arr)
expect.objectContaining(obj)
```
