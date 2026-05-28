# Error Handling - localStorage Patterns

**Arquivo Auxiliar da Skill:** localStorage-patterns
**Última Atualização:** 2025-11-19

---

## 📋 Erro Types e Tratamento

### 1. QuotaExceededError

**Quando ocorre:**
- Storage atingiu limite (5-10MB)
- Tentando salvar item >50KB
- Safari modo privado (quota = 0)

**Detecção:**
```javascript
try {
  localStorage.setItem(key, value);
} catch (error) {
  if (error.name === 'QuotaExceededError') {
    // Tratar aqui
  }
}
```

**Estratégias de Mitigação:**

**A) Limpar dados antigos:**
```javascript
function clearOldData(daysThreshold = 90) {
  const now = Date.now();
  Object.keys(localStorage)
    .filter(k => k.startsWith('plataforma-b2b_'))
    .forEach(key => {
      try {
        const data = JSON.parse(localStorage.getItem(key));
        if (data.lastUpdated) {
          const ageInDays = (now - data.lastUpdated) / (1000 * 60 * 60 * 24);
          if (ageInDays > daysThreshold) {
            localStorage.removeItem(key);
          }
        }
      } catch (e) {
        // Ignorar dados inválidos
      }
    });
}
```

**B) Fallback para sessionStorage:**
```javascript
function saveWithFallback(key, value) {
  try {
    localStorage.setItem(key, value);
    return 'localStorage';
  } catch (error) {
    if (error.name === 'QuotaExceededError') {
      try {
        sessionStorage.setItem(key, value);
        return 'sessionStorage';
      } catch (e) {
        return 'memory'; // Última opção: variável em memória
      }
    }
    throw error;
  }
}
```

**C) Comprimir dados:**
```javascript
function compressText(text) {
  // Remover espaços duplicados
  return text.replace(/\s+/g, ' ').trim();
}

function saveCompressed(key, text) {
  const compressed = compressText(text);
  const originalSize = new Blob([text]).size;
  const compressedSize = new Blob([compressed]).size;

  console.log(`Compressão: ${originalSize} → ${compressedSize} bytes (${((1 - compressedSize/originalSize) * 100).toFixed(1)}%)`);

  localStorage.setItem(key, compressed);
}
```

---

### 2. SecurityError

**Quando ocorre:**
- Safari/Firefox modo privado
- Configuração de segurança bloqueou storage
- Iframe cross-origin

**Detecção:**
```javascript
function isLocalStorageAvailable() {
  try {
    const test = '__test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch (error) {
    return error.name !== 'SecurityError';
  }
}
```

**Tratamento:**
```javascript
// Detectar modo privado ao montar app
useEffect(() => {
  const available = isLocalStorageAvailable();

  if (!available) {
    // Avisar usuário
    toast.warning('🔒 Modo privado detectado. Dados não serão salvos permanentemente.');

    // Usar fallback
    setStorageMode('sessionStorage'); // ou 'memory'
  }
}, []);
```

---

### 3. DOMException (Genérico)

**Quando ocorre:**
- Browser muito antigo
- Worker thread (sem acesso a localStorage)
- Contexto inválido

**Tratamento:**
```javascript
function safeOperation(operation, fallback) {
  try {
    return operation();
  } catch (error) {
    if (error instanceof DOMException) {
      console.error('DOMException:', error);
      return fallback;
    }
    throw error;
  }
}

// Uso
const notes = safeOperation(
  () => localStorage.getItem('notes'),
  '' // Valor padrão
);
```

---

## 🛡️ Defensive Programming Patterns

### Pattern 1: Safe Getters

```javascript
function safeGetItem(key, defaultValue = null) {
  try {
    const value = localStorage.getItem(key);
    return value !== null ? value : defaultValue;
  } catch (error) {
    console.error(`Erro ao ler ${key}:`, error);
    return defaultValue;
  }
}

function safeGetJSON(key, defaultValue = null) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : defaultValue;
  } catch (error) {
    console.error(`Erro ao parsear ${key}:`, error);
    // Remover dado corrompido
    localStorage.removeItem(key);
    return defaultValue;
  }
}
```

---

### Pattern 2: Safe Setters

```javascript
function safeSetItem(key, value) {
  try {
    localStorage.setItem(key, value);
    return { success: true, error: null };
  } catch (error) {
    console.error(`Erro ao salvar ${key}:`, error);

    // Classificar erro
    const errorType = error.name === 'QuotaExceededError'
      ? 'quota'
      : error.name === 'SecurityError'
      ? 'security'
      : 'unknown';

    return { success: false, error: errorType };
  }
}

function safeSetJSON(key, data) {
  try {
    const json = JSON.stringify(data);
    return safeSetItem(key, json);
  } catch (error) {
    console.error(`Erro ao stringify ${key}:`, error);
    return { success: false, error: 'stringify_failed' };
  }
}
```

---

### Pattern 3: Retry Logic

```javascript
function saveWithRetry(key, value, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      localStorage.setItem(key, value);
      return true;
    } catch (error) {
      if (error.name === 'QuotaExceededError' && i === 0) {
        // Primeira tentativa: limpar dados antigos
        clearOldData();
        continue;
      }

      if (i === maxRetries - 1) {
        console.error(`Falha após ${maxRetries} tentativas:`, error);
        return false;
      }
    }
  }
}
```

---

## 📊 Error Logging e Monitoring

### Pattern: Structured Error Logging

```javascript
function logStorageError(operation, key, error, context = {}) {
  const errorLog = {
    timestamp: Date.now(),
    operation, // 'read', 'write', 'delete'
    key,
    errorName: error.name,
    errorMessage: error.message,
    context,
    browser: navigator.userAgent,
    storageAvailable: isLocalStorageAvailable()
  };

  console.error('Storage Error:', errorLog);

  // Futuramente: enviar para Sentry, LogRocket, etc.
  // sendToErrorTracking(errorLog);

  return errorLog;
}

// Uso
try {
  localStorage.setItem(key, value);
} catch (error) {
  logStorageError('write', key, error, { valueSize: value.length });
  throw error;
}
```

---

## 🚨 User-Facing Error Messages

```javascript
const ERROR_MESSAGES = {
  quota_exceeded: {
    title: '⚠️ Armazenamento Cheio',
    message: 'Suas notas estão muito grandes. Limite: 50KB por curso.',
    actions: [
      { label: 'Limpar Dados Antigos', handler: clearOldData },
      { label: 'Baixar Backup', handler: downloadBackup }
    ]
  },
  security_blocked: {
    title: '🔒 Modo Privado Detectado',
    message: 'Dados salvos apenas durante esta sessão.',
    actions: [
      { label: 'Entendi', handler: () => {} }
    ]
  },
  unknown: {
    title: '❌ Erro ao Salvar',
    message: 'Tente recarregar a página.',
    actions: [
      { label: 'Recarregar', handler: () => window.location.reload() }
    ]
  }
};

function showErrorToast(errorType) {
  const config = ERROR_MESSAGES[errorType] || ERROR_MESSAGES.unknown;

  toast.error(
    <div>
      <strong>{config.title}</strong>
      <p>{config.message}</p>
      <div className="flex gap-2 mt-2">
        {config.actions.map(action => (
          <button
            key={action.label}
            onClick={action.handler}
            className="btn-sm"
          >
            {action.label}
          </button>
        ))}
      </div>
    </div>,
    { duration: 8000 }
  );
}
```

---

## 📚 Referências

- [MDN - DOMException](https://developer.mozilla.org/en-US/docs/Web/API/DOMException)
- [QuotaExceededError Spec](https://html.spec.whatwg.org/multipage/webstorage.html#dom-storage-setitem)
- [localStorage Skill Principal](../SKILL.md)
