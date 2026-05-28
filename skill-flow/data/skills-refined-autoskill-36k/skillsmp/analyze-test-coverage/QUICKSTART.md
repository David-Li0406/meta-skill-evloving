# Quick Start - Analyze Test Coverage

## TL;DR

Após cada commit, o sistema analisa automaticamente suas mudanças e sugere quais testes criar.

## Primeiro Uso

```bash
# Faça um commit normalmente
git add src/synth_lab/api/routers/my_endpoint.py
git commit -m "Add new endpoint"

# O hook roda automaticamente em background e mostra:
# 🤖 Analisando cobertura de testes...
# 🔴 OBRIGATÓRIO: Contract Test para my_endpoint
# 🟡 RECOMENDADO: E2E Test para my_endpoint
```

## Ver Detalhes e Templates

```bash
# Ver análise completa com templates de código
python scripts/analyze_test_coverage.py --commit HEAD --show-templates

# Copie o template sugerido e ajuste conforme necessário
```

## Uso Manual

```bash
# Analisar qualquer commit
python scripts/analyze_test_coverage.py --commit abc123

# Ver em JSON (útil para scripts)
python scripts/analyze_test_coverage.py --commit HEAD --json
```

## Tipos de Sugestões

| Você mudou | Você precisa criar |
|------------|-------------------|
| Router | Contract Test (obrigatório) |
| Service | Integration Test (obrigatório) |
| Model | Migration (obrigatório) |
| Repository | Integration Test (obrigatório) |
| Frontend Page | E2E Test (recomendado) |

## FAQ

**Q: O hook está travando meu commit?**
A: Não! O hook roda em background (`&`). Seu commit termina imediatamente.

**Q: Como desabilitar temporariamente?**
A: `git commit --no-verify`

**Q: Como ver os templates de código?**
A: `python scripts/analyze_test_coverage.py --commit HEAD --show-templates`

**Q: O que significa OBRIGATÓRIO vs RECOMENDADO?**
A: OBRIGATÓRIO = bloquearia push se configurado no pre-push. RECOMENDADO = fortemente sugerido mas não bloqueia.

**Q: Como desabilitar permanentemente?**
A: `rm .git/hooks/post-commit`

**Q: Como fazer o pre-push bloquear se faltar testes?**
A:
```bash
cat << 'EOF' > .git/hooks/pre-push
#!/bin/bash
if ! python scripts/analyze_test_coverage.py --commit HEAD; then
    echo "❌ Testes OBRIGATÓRIOS faltando!"
    exit 1
fi
EOF
chmod +x .git/hooks/pre-push
```

## Próximos Passos

1. Faça um commit de teste
2. Veja as sugestões aparecerem automaticamente
3. Use `--show-templates` para ver código de exemplo
4. Copie o template e ajuste para seu caso
5. Commit os testes criados

## Documentação Completa

- [README.md](./README.md): Guia completo
- [SKILL.md](./SKILL.md): Documentação técnica
- [docs/TESTING.md](../../../docs/TESTING.md): Guia de testes do projeto
