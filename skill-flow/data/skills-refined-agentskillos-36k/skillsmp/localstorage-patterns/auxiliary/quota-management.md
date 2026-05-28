# Quota Management - localStorage Patterns

**Arquivo Auxiliar da Skill:** localStorage-patterns
**Última Atualização:** 2025-11-19

---

## 📊 Quotas por Browser (2025)

| Browser | Quota | Notas |
|---------|-------|-------|
| Chrome/Edge | 10 MB | Por origem |
| Firefox | 10 MB | Por origem |
| Safari | 5 MB | Mais restritivo! |
| Opera | 10 MB | Por origem |
| Safari Private | 0 MB | Quota zero! |

**Origem:** Protocolo + domínio + porta (ex: `https://plataforma-b2b.com.br:443`)

---

## 🎯 Limites do Projeto Plataforma B2B de treinamento técnico corporativo

```yaml
Notas (5 sistemas):
  - Máximo por nota: 50 KB (25.000 caracteres)
  - Total estimado: 250 KB (5 × 50 KB)

Progresso (227 módulos):
  - Por módulo: ~100 bytes (JSON: id + timestamp)
  - Total estimado: 22 KB

Configurações:
  - Tema, idioma, etc: ~5 KB

Total Estimado: 300 KB (~3% da quota Safari)
Buffer Seguro: 8 MB (80% da quota mínima)
```

---

## 🔍 Verificar Quota Disponível

### API Moderna (Chrome 110+, Firefox 115+)

```javascript
async function getStorageQuota() {
  if (!navigator.storage || !navigator.storage.estimate) {
    return { supported: false };
  }

  try {
    const estimate = await navigator.storage.estimate();

    return {
      supported: true,
      usage: estimate.usage,
      quota: estimate.quota,
      usageMB: (estimate.usage / 1024 / 1024).toFixed(2),
      quotaMB: (estimate.quota / 1024 / 1024).toFixed(2),
      percentUsed: ((estimate.usage / estimate.quota) * 100).toFixed(1),
      available: estimate.quota - estimate.usage,
      availableMB: ((estimate.quota - estimate.usage) / 1024 / 1024).toFixed(2)
    };
  } catch (error) {
    console.error('Erro ao verificar quota:', error);
    return { supported: false };
  }
}

// Uso
const quota = await getStorageQuota();
if (quota.supported) {
  console.log(`Usando ${quota.usageMB} MB de ${quota.quotaMB} MB (${quota.percentUsed}%)`);
  console.log(`Disponível: ${quota.availableMB} MB`);
} else {
  console.warn('Storage API não suportada');
}
```

---

### Fallback (Navegadores Antigos)

```javascript
function estimateLocalStorageSize() {
  let total = 0;

  Object.keys(localStorage).forEach(key => {
    const value = localStorage.getItem(key);
    // UTF-16: ~2 bytes por caractere
    total += (key.length + value.length) * 2;
  });

  return {
    bytes: total,
    kb: (total / 1024).toFixed(2),
    mb: (total / 1024 / 1024).toFixed(2)
  };
}

const size = estimateLocalStorageSize();
console.log(`localStorage usando ~${size.mb} MB`);
```

---

## 🧹 Estratégias de Limpeza

### 1. Limpar por Idade (Time-Based)

```javascript
function clearOldDataByAge(daysThreshold = 90) {
  const now = Date.now();
  const cutoff = now - (daysThreshold * 24 * 60 * 60 * 1000);
  let freedBytes = 0;

  Object.keys(localStorage)
    .filter(key => key.startsWith('plataforma-b2b_'))
    .forEach(key => {
      try {
        const data = JSON.parse(localStorage.getItem(key));

        // Schema com lastUpdated
        if (data.lastUpdated && data.lastUpdated < cutoff) {
          const size = new Blob([localStorage.getItem(key)]).size;
          localStorage.removeItem(key);
          freedBytes += size;
          console.log(`Removido ${key} (idade: ${Math.floor((now - data.lastUpdated) / (24*60*60*1000))} dias)`);
        }
      } catch (error) {
        // Remover dados corrompidos
        localStorage.removeItem(key);
      }
    });

  return (freedBytes / 1024).toFixed(2); // KB liberados
}
```

---

### 2. Limpar por Prioridade (Priority-Based)

```javascript
const STORAGE_PRIORITIES = {
  settings: 1,    // Alta prioridade (nunca limpar)
  progress: 2,    // Média prioridade
  notes: 3        // Baixa prioridade (limpar primeiro)
};

function clearByPriority(targetFreeMB = 2) {
  const targetFreeBytes = targetFreeMB * 1024 * 1024;
  let freedBytes = 0;

  // Ordenar por prioridade (maior = limpar primeiro)
  const keys = Object.keys(localStorage)
    .filter(k => k.startsWith('plataforma-b2b_'))
    .map(key => {
      const type = key.split('_')[1]; // 'notes', 'progress', 'settings'
      return {
        key,
        priority: STORAGE_PRIORITIES[type] || 10,
        size: new Blob([localStorage.getItem(key)]).size
      };
    })
    .sort((a, b) => b.priority - a.priority);

  // Remover até atingir target
  for (const item of keys) {
    if (freedBytes >= targetFreeBytes) break;

    localStorage.removeItem(item.key);
    freedBytes += item.size;
    console.log(`Removido ${item.key} (prioridade ${item.priority})`);
  }

  return (freedBytes / 1024 / 1024).toFixed(2); // MB liberados
}
```

---

### 3. Limpar por Tamanho (Size-Based)

```javascript
function clearLargestItems(count = 5) {
  const items = Object.keys(localStorage)
    .filter(k => k.startsWith('plataforma-b2b_'))
    .map(key => ({
      key,
      size: new Blob([localStorage.getItem(key)]).size
    }))
    .sort((a, b) => b.size - a.size) // Maior primeiro
    .slice(0, count);

  items.forEach(item => {
    localStorage.removeItem(item.key);
    console.log(`Removido ${item.key} (${(item.size / 1024).toFixed(2)} KB)`);
  });

  return items.reduce((sum, item) => sum + item.size, 0);
}
```

---

## ⚠️ Alertas Proativos

### Pattern: Monitoramento Contínuo

```javascript
function useStorageQuotaMonitor(warningThreshold = 80) {
  const [quotaInfo, setQuotaInfo] = useState(null);
  const [showWarning, setShowWarning] = useState(false);

  useEffect(() => {
    async function check() {
      const info = await getStorageQuota();
      setQuotaInfo(info);

      if (info.supported && parseFloat(info.percentUsed) > warningThreshold) {
        setShowWarning(true);
      }
    }

    check();

    // Verificar a cada 5 minutos
    const interval = setInterval(check, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, [warningThreshold]);

  return { quotaInfo, showWarning };
}

// Uso no App.jsx
function App() {
  const { quotaInfo, showWarning } = useStorageQuotaMonitor(80);

  return (
    <div>
      {showWarning && (
        <Toast type="warning">
          ⚠️ Storage quase cheio ({quotaInfo.percentUsed}%)!
          <button onClick={clearOldData}>Limpar Dados Antigos</button>
        </Toast>
      )}
      {/* resto do app */}
    </div>
  );
}
```

---

## 📏 Validação de Tamanho

### Pattern: Pre-Flight Check

```javascript
const MAX_SIZE_BYTES = 50 * 1024; // 50 KB

function validateSize(text) {
  const sizeBytes = new Blob([text]).size;
  const sizeKB = (sizeBytes / 1024).toFixed(2);

  if (sizeBytes > MAX_SIZE_BYTES) {
    return {
      valid: false,
      size: sizeKB,
      limit: '50.00',
      excess: ((sizeBytes - MAX_SIZE_BYTES) / 1024).toFixed(2),
      message: `Nota muito grande (${sizeKB} KB). Excede limite em ${((sizeBytes - MAX_SIZE_BYTES) / 1024).toFixed(2)} KB.`
    };
  }

  return {
    valid: true,
    size: sizeKB,
    percentage: ((sizeBytes / MAX_SIZE_BYTES) * 100).toFixed(1)
  };
}

// Uso em componente
function NotesView() {
  const [notes, setNotes] = useState('');
  const [validation, setValidation] = useState(null);

  useEffect(() => {
    const result = validateSize(notes);
    setValidation(result);
  }, [notes]);

  const handleChange = (e) => {
    const newText = e.target.value;
    const check = validateSize(newText);

    if (!check.valid) {
      alert(check.message);
      return; // Bloquear
    }

    setNotes(newText);
  };

  return (
    <div>
      <textarea value={notes} onChange={handleChange} />

      {validation && (
        <div className="text-sm text-gray-500">
          Tamanho: {validation.size} KB / 50 KB ({validation.percentage}%)
          {parseFloat(validation.percentage) > 80 && (
            <span className="text-yellow-600 ml-2">⚠️ Nota grande</span>
          )}
        </div>
      )}
    </div>
  );
}
```

---

## 💾 Compressão de Dados

### Técnica 1: Remover Espaços Duplicados

```javascript
function compressWhitespace(text) {
  return text
    .replace(/\s+/g, ' ')  // Múltiplos espaços → 1 espaço
    .replace(/\n\s+/g, '\n') // Espaços após \n
    .trim();
}

const original = 'Hello    world\n\n\n   Next line';
const compressed = compressWhitespace(original);

console.log('Original:', new Blob([original]).size, 'bytes');
console.log('Compressed:', new Blob([compressed]).size, 'bytes');
// Redução típica: 10-20%
```

---

### Técnica 2: JSON Compacto

```javascript
// ❌ Verbose (300 bytes)
const verbose = JSON.stringify({
  completedModules: [
    { id: '1.1', completedAt: 1700000000000 },
    { id: '1.2', completedAt: 1700000100000 }
  ]
}, null, 2);

// ✅ Compacto (150 bytes - 50% menor)
const compact = JSON.stringify({
  cm: [
    ['1.1', 1700000000000],
    ['1.2', 1700000100000]
  ]
});

// Decode helper
function parseCompactProgress(data) {
  return {
    completedModules: data.cm.map(([id, ts]) => ({
      id,
      completedAt: ts
    }))
  };
}
```

---

## 📚 Referências

- [Storage API Spec](https://storage.spec.whatwg.org/)
- [Storage for the Web (web.dev)](https://web.dev/storage-for-the-web/)
- [localStorage Skill Principal](../SKILL.md)
