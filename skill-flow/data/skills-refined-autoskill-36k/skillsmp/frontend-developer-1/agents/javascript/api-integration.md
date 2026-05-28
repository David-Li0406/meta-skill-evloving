---
name: API Integration
description: Expert en intégration d'APIs - Fetch, REST, GraphQL et WebSockets
workflows:
  - id: api-integration
    template: wf-creation
    phase: Production
    name: Intégration API
    duration: 1-3 jours
  - id: api-refactor
    template: wf-evolution
    phase: Réalisation
    name: Refactoring couche API
    duration: 1-2 jours
---

# Agent API Integration

## Responsabilité

Intégrer efficacement les APIs externes et internes dans les applications front-end.

## Tu NE fais PAS

- ❌ Créer les APIs backend (Express, Fastify, serveurs) → skill `backend-developer`
- ❌ Gérer le state global des données (caching, synchronisation) → `state-management/server-state.md`
- ❌ Typer les réponses API (interfaces, types) → `typescript.md`
- ❌ Tester les appels API → `testing/`

## Fetch API

### Requêtes de base

```javascript
// GET simple
const response = await fetch('/api/users');
const users = await response.json();

// POST avec JSON
const response = await fetch('/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'John',
    email: 'john@example.com'
  })
});

// PUT
await fetch(`/api/users/${id}`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(userData)
});

// DELETE
await fetch(`/api/users/${id}`, {
  method: 'DELETE'
});

// PATCH
await fetch(`/api/users/${id}`, {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'New Name' })
});
```

### Gestion des erreurs

```javascript
async function fetchWithErrorHandling(url, options = {}) {
  try {
    const response = await fetch(url, options);

    // Vérifier le status HTTP
    if (!response.ok) {
      // Essayer de parser l'erreur du serveur
      let errorMessage;
      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorData.error;
      } catch {
        errorMessage = response.statusText;
      }

      throw new APIError(errorMessage, response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }

    // Erreur réseau
    if (error.name === 'TypeError') {
      throw new NetworkError('Network request failed');
    }

    throw error;
  }
}

// Classes d'erreur personnalisées
class APIError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'APIError';
    this.status = status;
  }
}

class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NetworkError';
  }
}
```

### Options avancées

```javascript
// Timeout avec AbortController
async function fetchWithTimeout(url, options = {}, timeout = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error('Request timeout');
    }
    throw error;
  }
}

// Annulation manuelle
const controller = new AbortController();

// Dans un composant React
useEffect(() => {
  const controller = new AbortController();

  fetch('/api/data', { signal: controller.signal })
    .then((res) => res.json())
    .then(setData)
    .catch((err) => {
      if (err.name !== 'AbortError') {
        setError(err);
      }
    });

  return () => controller.abort();
}, []);
```

## Client API Wrapper

```javascript
class APIClient {
  constructor(baseURL, options = {}) {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      ...options.headers
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;

    const config = {
      ...options,
      headers: {
        ...this.defaultHeaders,
        ...options.headers
      }
    };

    // Ajouter le token si présent
    const token = this.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(url, config);

    if (!response.ok) {
      await this.handleError(response);
    }

    // Gérer les réponses vides (204 No Content)
    if (response.status === 204) {
      return null;
    }

    return response.json();
  }

  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    return this.request(url);
  }

  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async patch(endpoint, data) {
    return this.request(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }

  getToken() {
    return localStorage.getItem('auth_token');
  }

  setToken(token) {
    localStorage.setItem('auth_token', token);
  }

  async handleError(response) {
    const error = await response.json().catch(() => ({}));

    if (response.status === 401) {
      this.setToken(null);
      window.location.href = '/login';
    }

    throw new APIError(error.message || 'Request failed', response.status);
  }
}

// Usage
const api = new APIClient('https://api.example.com');

const users = await api.get('/users', { page: 1, limit: 10 });
const newUser = await api.post('/users', { name: 'John' });
await api.delete(`/users/${id}`);
```

## Upload de fichiers

```javascript
// Upload simple
async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('description', 'My file');

  const response = await fetch('/api/upload', {
    method: 'POST',
    body: formData // Pas de Content-Type header (auto avec boundary)
  });

  return response.json();
}

// Upload avec progression
async function uploadWithProgress(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        const percent = Math.round((event.loaded / event.total) * 100);
        onProgress(percent);
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText));
      } else {
        reject(new Error(`Upload failed: ${xhr.status}`));
      }
    });

    xhr.addEventListener('error', () => reject(new Error('Upload failed')));

    const formData = new FormData();
    formData.append('file', file);

    xhr.open('POST', '/api/upload');
    xhr.send(formData);
  });
}

// Upload multiple
async function uploadMultiple(files) {
  const formData = new FormData();
  files.forEach((file, index) => {
    formData.append(`files`, file);
  });

  return fetch('/api/upload-multiple', {
    method: 'POST',
    body: formData
  });
}
```

## WebSockets

```javascript
class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.listeners = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        resolve();
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket closed:', event.code, event.reason);
        this.handleReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleMessage(data);
        } catch (error) {
          console.error('Failed to parse message:', error);
        }
      };
    });
  }

  handleMessage(data) {
    const { type, payload } = data;
    const callbacks = this.listeners.get(type) || [];
    callbacks.forEach((callback) => callback(payload));
  }

  on(type, callback) {
    if (!this.listeners.has(type)) {
      this.listeners.set(type, []);
    }
    this.listeners.get(type).push(callback);

    // Retourner une fonction pour se désabonner
    return () => {
      const callbacks = this.listeners.get(type);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    };
  }

  send(type, payload) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, payload }));
    } else {
      console.warn('WebSocket not connected');
    }
  }

  handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

      setTimeout(() => {
        this.connect().catch(console.error);
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

// Usage
const ws = new WebSocketClient('wss://api.example.com/ws');
await ws.connect();

const unsubscribe = ws.on('message', (data) => {
  console.log('New message:', data);
});

ws.send('subscribe', { channel: 'updates' });

// Cleanup
unsubscribe();
ws.disconnect();
```

## Server-Sent Events (SSE)

```javascript
class SSEClient {
  constructor(url) {
    this.url = url;
    this.eventSource = null;
    this.listeners = new Map();
  }

  connect() {
    this.eventSource = new EventSource(this.url);

    this.eventSource.onopen = () => {
      console.log('SSE connected');
    };

    this.eventSource.onerror = (error) => {
      console.error('SSE error:', error);
      // EventSource reconnecte automatiquement
    };

    // Message par défaut
    this.eventSource.onmessage = (event) => {
      this.emit('message', JSON.parse(event.data));
    };
  }

  on(eventType, callback) {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, []);

      // Écouter ce type d'événement sur l'EventSource
      this.eventSource?.addEventListener(eventType, (event) => {
        this.emit(eventType, JSON.parse(event.data));
      });
    }

    this.listeners.get(eventType).push(callback);

    return () => {
      const callbacks = this.listeners.get(eventType);
      const index = callbacks.indexOf(callback);
      if (index > -1) callbacks.splice(index, 1);
    };
  }

  emit(eventType, data) {
    const callbacks = this.listeners.get(eventType) || [];
    callbacks.forEach((cb) => cb(data));
  }

  disconnect() {
    this.eventSource?.close();
    this.eventSource = null;
  }
}

// Usage
const sse = new SSEClient('/api/events');
sse.connect();

sse.on('notification', (data) => {
  showNotification(data);
});

sse.on('update', (data) => {
  updateUI(data);
});
```

## Retry et Résilience

```javascript
async function fetchWithRetry(url, options = {}, maxRetries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(url, options);

      if (response.ok) {
        return response;
      }

      // Ne pas retry pour les erreurs client (4xx)
      if (response.status >= 400 && response.status < 500) {
        throw new APIError('Client error', response.status);
      }

      throw new Error(`HTTP ${response.status}`);
    } catch (error) {
      lastError = error;

      if (attempt < maxRetries) {
        // Exponential backoff
        const delay = Math.min(1000 * Math.pow(2, attempt - 1), 10000);
        console.log(`Retry ${attempt}/${maxRetries} after ${delay}ms`);
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}

// Circuit breaker pattern
class CircuitBreaker {
  constructor(threshold = 5, timeout = 30000) {
    this.threshold = threshold;
    this.timeout = timeout;
    this.failures = 0;
    this.state = 'CLOSED';
    this.nextAttempt = Date.now();
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker is OPEN');
      }
      this.state = 'HALF-OPEN';
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
```

## Mots-clés de routage

`fetch`, `API`, `REST`, `HTTP`, `GET`, `POST`, `PUT`, `DELETE`, `GraphQL`, `WebSocket`, `SSE`, `Server-Sent Events`, `upload`, `FormData`, `AbortController`, `retry`

## Livrables

| Livrable | Description |
|----------|-------------|
| Client API | Wrapper Fetch ou Axios avec gestion d'erreurs et interceptors |
| Définitions TypeScript | Interfaces et types pour les réponses API |
| Documentation API | Guide d'utilisation des endpoints et exemples de calls |
