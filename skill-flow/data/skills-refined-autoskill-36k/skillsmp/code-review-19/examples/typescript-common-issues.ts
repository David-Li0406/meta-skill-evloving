// TypeScript Code Review: Common Issues
// This file demonstrates common issues found in TypeScript code reviews and their fixes.

// =============================================================================
// Issue 1: Using 'any' Type
// =============================================================================

// BAD: Using any loses all type safety
function processDataBad(data: any): any {
  return data.items.map((item: any) => item.value);
}

// GOOD: Proper typing with generics and interfaces
interface DataItem {
  id: string;
  value: number;
}

interface DataResponse {
  items: DataItem[];
  total: number;
}

function processDataGood(data: DataResponse): number[] {
  return data.items.map((item) => item.value);
}

// GOOD: When type is truly unknown, use 'unknown' with type guards
function processUnknown(data: unknown): string {
  if (typeof data === 'string') {
    return data;
  }
  if (typeof data === 'object' && data !== null && 'message' in data) {
    return String((data as { message: unknown }).message);
  }
  return String(data);
}

// =============================================================================
// Issue 2: Null/Undefined Handling
// =============================================================================

// BAD: No null checks
function getUserNameBad(user: { name?: string }): string {
  return user.name.toUpperCase(); // Runtime error if name is undefined
}

// GOOD: Proper null handling
function getUserNameGood(user: { name?: string }): string {
  return user.name?.toUpperCase() ?? 'Unknown';
}

// BAD: Truthy check that fails for valid falsy values
function getValueBad(value: number | undefined): number {
  return value || 0; // Returns 0 for value = 0 too!
}

// GOOD: Explicit undefined check
function getValueGood(value: number | undefined): number {
  return value ?? 0; // Only replaces undefined/null
}

// =============================================================================
// Issue 3: Type Assertions Overuse
// =============================================================================

// BAD: Forcing type with assertion
function parseConfigBad(json: string): Config {
  return JSON.parse(json) as Config; // No runtime validation
}

// GOOD: Runtime validation with type guard
interface Config {
  apiUrl: string;
  timeout: number;
}

function isConfig(value: unknown): value is Config {
  return (
    typeof value === 'object' &&
    value !== null &&
    'apiUrl' in value &&
    typeof (value as Config).apiUrl === 'string' &&
    'timeout' in value &&
    typeof (value as Config).timeout === 'number'
  );
}

function parseConfigGood(json: string): Config | null {
  try {
    const parsed = JSON.parse(json);
    if (isConfig(parsed)) {
      return parsed;
    }
    return null;
  } catch {
    return null;
  }
}

// =============================================================================
// Issue 4: Mutable Default Parameters
// =============================================================================

// BAD: Mutable default parameter
function addItemBad(items: string[] = []) {
  items.push('new'); // Mutates the default array!
  return items;
}

// GOOD: Create new array
function addItemGood(items: string[] = []): string[] {
  return [...items, 'new'];
}

// =============================================================================
// Issue 5: Implicit Any in Callbacks
// =============================================================================

// BAD: Implicit any in callback parameters
const numbers = [1, 2, 3];
const doubledBad = numbers.map((n) => n * 2); // 'n' is implicitly 'any' in some configs

// GOOD: Explicit types
const doubledGood = numbers.map((n: number): number => n * 2);

// Or let TypeScript infer from the array type
const typedNumbers: number[] = [1, 2, 3];
const doubledInferred = typedNumbers.map((n) => n * 2); // n is number

// =============================================================================
// Issue 6: Object Mutation
// =============================================================================

// BAD: Direct mutation
interface State {
  users: User[];
  selectedId: string | null;
}

interface User {
  id: string;
  name: string;
}

function updateStateBad(state: State, user: User): State {
  state.users.push(user); // Mutates original array
  return state;
}

// GOOD: Immutable update
function updateStateGood(state: State, user: User): State {
  return {
    ...state,
    users: [...state.users, user],
  };
}

// =============================================================================
// Issue 7: Promise Handling
// =============================================================================

// BAD: Unhandled promise rejection
async function fetchDataBad(url: string) {
  const response = await fetch(url);
  return response.json(); // No error handling
}

// GOOD: Proper error handling
interface FetchResult<T> {
  data: T | null;
  error: Error | null;
}

async function fetchDataGood<T>(url: string): Promise<FetchResult<T>> {
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json();
    return { data, error: null };
  } catch (error) {
    return {
      data: null,
      error: error instanceof Error ? error : new Error('Unknown error'),
    };
  }
}

// =============================================================================
// Issue 8: Enum Misuse
// =============================================================================

// BAD: Numeric enum (can cause issues)
enum StatusBad {
  Pending, // 0
  Active, // 1
  Inactive, // 2
}
// Problem: StatusBad[0] returns "Pending" (reverse mapping)

// GOOD: String enum or union type
enum StatusEnum {
  Pending = 'pending',
  Active = 'active',
  Inactive = 'inactive',
}

// BETTER: Union type (more idiomatic TypeScript)
type Status = 'pending' | 'active' | 'inactive';

// =============================================================================
// Issue 9: Index Signature Misuse
// =============================================================================

// BAD: Overly permissive index signature
interface ConfigBad {
  [key: string]: any; // Allows anything
}

// GOOD: Specific types with known keys
interface ConfigGood {
  apiUrl: string;
  timeout: number;
  features: Record<string, boolean>;
}

// Or use Record for dynamic keys with specific value type
type FeatureFlags = Record<string, boolean>;

// =============================================================================
// Issue 10: Function Overload Issues
// =============================================================================

// BAD: Union return type is unclear
function parseValueBad(value: string | number): string | number {
  if (typeof value === 'string') {
    return parseInt(value, 10);
  }
  return value.toString();
}

// GOOD: Function overloads for clear type relationships
function parseValue(value: string): number;
function parseValue(value: number): string;
function parseValue(value: string | number): string | number {
  if (typeof value === 'string') {
    return parseInt(value, 10);
  }
  return value.toString();
}

// Usage is now type-safe
const num: number = parseValue('42');
const str: string = parseValue(42);

// =============================================================================
// Issue 11: Async/Await Patterns
// =============================================================================

// BAD: Sequential when parallel is possible
async function loadAllBad(ids: string[]): Promise<User[]> {
  const users: User[] = [];
  for (const id of ids) {
    const user = await fetchUser(id); // Sequential - slow!
    users.push(user);
  }
  return users;
}

// GOOD: Parallel execution
async function loadAllGood(ids: string[]): Promise<User[]> {
  return Promise.all(ids.map((id) => fetchUser(id)));
}

// BETTER: With error handling and concurrency limit
async function loadAllBetter(ids: string[], concurrency = 5): Promise<User[]> {
  const results: User[] = [];

  for (let i = 0; i < ids.length; i += concurrency) {
    const batch = ids.slice(i, i + concurrency);
    const batchResults = await Promise.all(batch.map((id) => fetchUser(id)));
    results.push(...batchResults);
  }

  return results;
}

async function fetchUser(id: string): Promise<User> {
  // Implementation
  return { id, name: 'User' };
}

// =============================================================================
// Issue 12: Event Handler Types
// =============================================================================

// BAD: Using 'any' for event
function handleClickBad(e: any) {
  e.preventDefault();
  console.log(e.target.value);
}

// GOOD: Proper event typing
function handleClick(e: React.MouseEvent<HTMLButtonElement>) {
  e.preventDefault();
  console.log(e.currentTarget.textContent);
}

function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  console.log(e.target.value);
}

function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();
  const formData = new FormData(e.currentTarget);
  console.log(Object.fromEntries(formData));
}

export {
  processDataGood,
  processUnknown,
  getUserNameGood,
  parseConfigGood,
  addItemGood,
  updateStateGood,
  fetchDataGood,
  loadAllGood,
};
