---
name: emojis-rules
description: Regras sobre uso de emojis em código e documentação
triggers: [emoji, emojis, unicode, symbols]
---

# Emojis Rules

**Regras sobre uso de emojis em código, documentação e arquivos do projeto.**

---

## Quando Usar

Aplicar esta skill quando:
- Escrevendo código, documentação ou comentários
- Criando arquivos de configuração
- Gerando templates ou exemplos

---

## Regra Geral: Proibição de Emojis

**EM HIPÓTESE NENHUMA usar emojis em:**
- Código-fonte (Python, JavaScript, TypeScript, CSS, HTML, etc.)
- Documentações Markdown dentro dos repositórios (exceto README.md)
- Arquivos de configuração (.toml, .ini, .yaml, .yml, .json, .env, etc.)
- Scripts (.sh, .py, .js, etc.)
- Templates (HTML, Jinja, etc.)
- Arquivos de teste
- Comentários e docstrings em código

---

## Exceções Permitidas

**Emojis são permitidos apenas em:**
1. **Arquivos README.md** - Para melhorar visual e didática
2. **Notebooks Jupyter (.ipynb)** - Apenas para fins de estudos e melhorar apresentação educacional

---

## Regras por Tipo de Projeto

### Projetos de Trabalho/Work

**Zero emojis em qualquer parte:**
- Código-fonte
- Documentação técnica
- Comentários
- Mensagens de commit
- Arquivos de configuração
- Scripts
- Templates

**Exceção:** Nenhuma

### Projetos de Estudos

**Emojis permitidos apenas em:**
- README.md (para visual)
- Notebooks Jupyter (para ensino)

**Proibidos em:**
- Código-fonte
- Documentação técnica (exceto README)
- Scripts
- Testes

---

## Validação

**Antes de commitar:**
- [ ] Verificar se há emojis em código
- [ ] Verificar se há emojis em documentação técnica
- [ ] Garantir que apenas README e notebooks tenham emojis (quando aplicável)

---

## Referências

- **Regras gerais:** `core/agents/programming.mdc`
- **Templates:** `core/templates/`

---

**Esta regra é obrigatória e deve ser seguida por todos os agentes.**

