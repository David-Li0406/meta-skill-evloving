# Feature: [NOME DA FEATURE]

**Data:** YYYY-MM-DD
**Status:** Draft | Em Revisao | Aprovado
**Autor:** [nome]
**Prioridade:** P0 (Critico) | P1 (Alto) | P2 (Medio) | P3 (Baixo)

---

## Contexto

### Problema
[Descreva o problema que esta sendo resolvido]

### Usuarios Afetados
[Quem sera impactado por esta feature]

### Impacto de Nao Resolver
[O que acontece se nao fizermos isso]

---

## Objetivo

[Uma frase clara sobre o que esta feature vai fazer]

---

## Requisitos Funcionais

### RF1: [Nome do Requisito]

**Descricao:** [O que deve acontecer]

**Endpoint:** (se aplicavel)
```
METHOD /api/endpoint
```

**Input:**
```json
{
  "campo1": "tipo",
  "campo2": "tipo"
}
```

**Output (Sucesso):**
```json
{
  "resultado": "tipo"
}
```

**Validacoes:**
- Validacao 1
- Validacao 2

**Erros:**
| Codigo | Condicao | Mensagem |
|--------|----------|----------|
| 400 | Input invalido | "Descricao do erro" |
| 401 | Nao autenticado | "Autenticacao necessaria" |
| 404 | Nao encontrado | "Recurso nao existe" |

---

### RF2: [Nome do Requisito]

[Repetir estrutura acima]

---

## Requisitos Nao-Funcionais

### Performance
- Tempo de resposta: p95 < [X]ms
- Throughput: [Y] requests/segundo

### Seguranca
- [ ] Autenticacao necessaria
- [ ] Autorizacao por role
- [ ] Dados sensiveis criptografados
- [ ] Input sanitizado

### Escalabilidade
- Usuarios simultaneos: [N]
- Volume de dados: [X] registros

### Disponibilidade
- SLA: [99.X]%
- RPO: [X] horas
- RTO: [Y] horas

---

## Database Schema (se aplicavel)

```sql
CREATE TABLE nome_tabela (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campo1 VARCHAR(255) NOT NULL,
  campo2 INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_nome_tabela_campo1 ON nome_tabela(campo1);
```

---

## User Flow

1. Usuario faz [acao 1]
2. Sistema responde com [resposta 1]
3. Usuario faz [acao 2]
4. Sistema [comportamento]

---

## Criterios de Aceitacao

### Funcionais
- [ ] Usuario pode [acao 1]
- [ ] Sistema [comportamento 1]
- [ ] Quando [condicao], entao [resultado]

### Tecnicos
- [ ] Testes unitarios >= 80% coverage
- [ ] Testes de integracao passando
- [ ] Performance dentro do SLA
- [ ] Sem vulnerabilidades criticas

---

## Fora do Escopo (v1)

- [ ] [Funcionalidade futura 1]
- [ ] [Funcionalidade futura 2]

---

## Dependencias

### Features que bloqueiam esta
- [Feature X] - motivo

### Features bloqueadas por esta
- [Feature Y] - motivo

### Dependencias Tecnicas
- [Lib/API externa] - proposito

---

## Riscos

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| Risco 1 | Alta/Media/Baixa | Alto/Medio/Baixo | Como mitigar |

---

## Metricas de Sucesso

- [ ] [Metrica 1]: [valor target]
- [ ] [Metrica 2]: [valor target]

---

## Referencias

- [Link para doc relacionado]
- [Link para wireframe]
- [Link para discussao]

---

## Historico

| Data | Autor | Mudanca |
|------|-------|---------|
| YYYY-MM-DD | Nome | Criacao inicial |
