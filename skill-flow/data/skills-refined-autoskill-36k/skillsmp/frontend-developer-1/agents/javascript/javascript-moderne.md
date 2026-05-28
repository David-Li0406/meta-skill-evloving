---
name: JavaScript Moderne
description: Expert en JavaScript ES6+ - async/await, modules, destructuring, patterns modernes
workflows:
  - id: js-creation
    template: wf-creation
    phase: Production
    name: Développement JavaScript
    duration: ongoing
  - id: js-modernization
    template: wf-refonte
    phase: Migration
    name: Modernisation code ES6+
    duration: 2-5 jours
---

# Agent JavaScript Moderne

## Responsabilité

Maîtriser et implémenter les fonctionnalités JavaScript modernes (ES6+) pour écrire du code propre, performant et maintenable.

## Tu NE fais PAS

- ❌ Gérer le typage (TypeScript, interfaces, generics) → `typescript.md`
- ❌ Manipuler le DOM directement (querySelector, events) → `dom-manipulation.md`
- ❌ Appeler des APIs (fetch, REST, WebSockets) → `api-integration.md`
- ❌ Implémenter des hooks React spécifiques → skill `react-expert`

## ES6+ Essentials

### Déclarations de variables

```javascript
// const par défaut
const API_URL = 'https://api.example.com';
const config = { debug: true };

// let seulement si réassignation nécessaire
let count = 0;
count += 1;

// Éviter var (hoisting, scope function)
```

### Arrow Functions

```javascript
// Syntaxe courte
const double = (x) => x * 2;
const add = (a, b) => a + b;

// Avec corps de fonction
const processData = (data) => {
  const result = transform(data);
  return result;
};

// Attention au this (arrow capture le this lexical)
class Counter {
  count = 0;

  // Arrow préserve le this
  increment = () => {
    this.count++;
  };

  // Méthode traditionnelle - this dépend du contexte d'appel
  decrement() {
    this.count--;
  }
}
```

### Destructuring

```javascript
// Objets
const user = { name: 'John', age: 30, city: 'Paris' };
const { name, age } = user;
const { name: userName, ...rest } = user;

// Avec valeurs par défaut
const { role = 'user' } = user;

// Renommage
const { name: fullName } = user;

// Tableaux
const [first, second, ...others] = [1, 2, 3, 4, 5];
const [, , third] = [1, 2, 3]; // Skip elements

// Paramètres de fonction
function createUser({ name, email, role = 'user' }) {
  return { name, email, role };
}
```

### Spread Operator

```javascript
// Fusion d'objets
const defaults = { theme: 'light', lang: 'fr' };
const userPrefs = { theme: 'dark' };
const settings = { ...defaults, ...userPrefs };

// Copie de tableaux
const original = [1, 2, 3];
const copy = [...original];
const extended = [...original, 4, 5];

// Arguments de fonction
const numbers = [1, 2, 3];
Math.max(...numbers);
```

### Template Literals

```javascript
const name = 'World';
const greeting = `Hello, ${name}!`;

// Multiline
const html = `
  <div class="card">
    <h2>${title}</h2>
    <p>${description}</p>
  </div>
`;

// Tagged templates
function highlight(strings, ...values) {
  return strings.reduce((acc, str, i) => {
    return acc + str + (values[i] ? `<mark>${values[i]}</mark>` : '');
  }, '');
}

const result = highlight`Search for ${query} in ${category}`;
```

## Async JavaScript

### Promises

```javascript
// Création
const fetchData = () => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve({ data: 'success' });
    }, 1000);
  });
};

// Chaînage
fetchData()
  .then((result) => transform(result))
  .then((transformed) => save(transformed))
  .catch((error) => console.error(error))
  .finally(() => cleanup());

// Promise.all - parallèle
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);

// Promise.allSettled - toutes, même si erreurs
const results = await Promise.allSettled([
  fetchUsers(),
  fetchPosts()
]);
// results: [{ status: 'fulfilled', value: ... }, { status: 'rejected', reason: ... }]

// Promise.race - première résolue
const fastest = await Promise.race([fetch1(), fetch2()]);

// Promise.any - première réussie (ignore les rejets)
const firstSuccess = await Promise.any([fetch1(), fetch2()]);
```

### Async/Await

```javascript
// Fonction async
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const user = await response.json();
    return user;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}

// Arrow function async
const fetchPosts = async () => {
  const response = await fetch('/api/posts');
  return response.json();
};

// Parallel async
async function loadDashboard() {
  const [users, posts, stats] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchStats()
  ]);

  return { users, posts, stats };
}

// Sequential async (quand ordre importe)
async function processSequentially(items) {
  const results = [];
  for (const item of items) {
    const result = await processItem(item);
    results.push(result);
  }
  return results;
}
```

## Modules ES

### Export

```javascript
// Named exports
export const API_URL = 'https://api.example.com';

export function fetchUsers() {
  return fetch(`${API_URL}/users`);
}

export class UserService {
  // ...
}

// Export groupé
const helper1 = () => {};
const helper2 = () => {};
export { helper1, helper2 };

// Renommage à l'export
export { helper1 as utilHelper };

// Default export (un seul par module)
export default class App {
  // ...
}
```

### Import

```javascript
// Named imports
import { fetchUsers, API_URL } from './api.js';

// Renommage
import { fetchUsers as getUsers } from './api.js';

// Default import
import App from './App.js';

// Tout importer
import * as api from './api.js';
api.fetchUsers();

// Import dynamique (code splitting)
const module = await import('./heavy-module.js');
module.doSomething();

// Import conditionnel
if (condition) {
  const { feature } = await import('./feature.js');
  feature();
}
```

## Patterns Modernes

### Optional Chaining & Nullish Coalescing

```javascript
// Optional chaining (?.)
const city = user?.address?.city;
const firstItem = array?.[0];
const result = obj?.method?.();

// Nullish coalescing (??)
const value = input ?? 'default'; // null ou undefined seulement
const count = data.count ?? 0;

// Différence avec ||
const zero = 0 || 'default';  // 'default' (0 est falsy)
const zero2 = 0 ?? 'default'; // 0 (0 n'est pas null/undefined)
```

### Méthodes de tableau modernes

```javascript
const users = [
  { name: 'Alice', age: 25, active: true },
  { name: 'Bob', age: 30, active: false },
  { name: 'Charlie', age: 35, active: true }
];

// map - transformer
const names = users.map((user) => user.name);

// filter - filtrer
const activeUsers = users.filter((user) => user.active);

// find - trouver un élément
const bob = users.find((user) => user.name === 'Bob');

// findIndex - trouver l'index
const bobIndex = users.findIndex((user) => user.name === 'Bob');

// some - au moins un
const hasActive = users.some((user) => user.active);

// every - tous
const allActive = users.every((user) => user.active);

// reduce - réduire à une valeur
const totalAge = users.reduce((sum, user) => sum + user.age, 0);

// flatMap - map + flatten
const tags = posts.flatMap((post) => post.tags);

// at - accès par index (négatif supporté)
const last = users.at(-1);

// Chaînage
const result = users
  .filter((user) => user.active)
  .map((user) => user.name)
  .sort();
```

### Classes modernes

```javascript
class EventEmitter {
  // Champs privés
  #listeners = new Map();

  // Champs publics avec initialisation
  maxListeners = 10;

  // Champs statiques
  static defaultMaxListeners = 10;

  constructor(options = {}) {
    this.maxListeners = options.maxListeners ?? EventEmitter.defaultMaxListeners;
  }

  // Méthode publique
  on(event, callback) {
    if (!this.#listeners.has(event)) {
      this.#listeners.set(event, []);
    }
    this.#listeners.get(event).push(callback);
    return this;
  }

  // Méthode privée
  #validateEvent(event) {
    if (typeof event !== 'string') {
      throw new TypeError('Event must be a string');
    }
  }

  // Getter
  get listenerCount() {
    let count = 0;
    for (const listeners of this.#listeners.values()) {
      count += listeners.length;
    }
    return count;
  }

  // Méthode statique
  static create(options) {
    return new EventEmitter(options);
  }
}
```

## Bonnes Pratiques

### Immutabilité

```javascript
// Éviter les mutations
// Mauvais
const updateUser = (user, name) => {
  user.name = name;
  return user;
};

// Bon
const updateUser = (user, name) => ({
  ...user,
  name
});

// Pour les tableaux
const addItem = (array, item) => [...array, item];
const removeItem = (array, index) => [
  ...array.slice(0, index),
  ...array.slice(index + 1)
];
```

### Pure Functions

```javascript
// Fonction pure : même entrée = même sortie, pas d'effets de bord
const calculateTotal = (items) => {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
};

// Impure : dépend de l'état externe
let taxRate = 0.2;
const calculateWithTax = (amount) => amount * (1 + taxRate); // Impure
```

## Mots-clés de routage

`JavaScript`, `ES6`, `ES2015`, `ES2020`, `async`, `await`, `Promise`, `modules`, `import`, `export`, `destructuring`, `spread`, `arrow function`, `template literal`, `optional chaining`, `nullish coalescing`

## Livrables

| Livrable | Description |
|----------|-------------|
| Modules JavaScript | Code ES6+ avec imports/exports et structure modulaire |
| Fonctions async | Implémentations async/await pour opérations asynchrones |
| Utilitaires modernes | Helpers réutilisables utilisant les features ES6+ |
