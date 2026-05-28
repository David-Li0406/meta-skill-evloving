---
name: css-best-practices
description: Regras e boas práticas para organização e uso de CSS
triggers: [css, styles, stylesheet, minify, minification]
---

# CSS Best Practices

**Regras para organização, estrutura e otimização de arquivos CSS.**

---

## Quando Usar

Aplicar esta skill quando:
- Criando ou organizando arquivos CSS
- Configurando build de assets
- Otimizando performance de CSS

---

## Estrutura de Pastas

**SEMPRE usar pasta `styles/` com arquivos separados por tipo:**

```
styles/
├── app.css
├── componentes.css
├── dashboard.css
├── table.css
├── menu.css
└── ...
```

**Organização:**
- `app.css` - Estilos gerais da aplicação
- `componentes.css` - Estilos de componentes reutilizáveis
- `dashboard.css` - Estilos específicos do dashboard
- `table.css` - Estilos de tabelas
- `menu.css` - Estilos de menus/navegação
- Outros arquivos conforme necessário

---

## Versões Minificadas Obrigatórias

**SEMPRE criar versão `.min.css` de cada arquivo:**
- `app.css` → `app.min.css`
- `componentes.css` → `componentes.min.css`
- etc.

**Processo:**
1. Criar arquivo legível (`.css`)
2. Minificar para produção (`.min.css`)
3. Carregar apenas `.min.css` em produção

---

## Carregamento

**Regra crítica:**
- **Produção:** Carregar apenas versões `.min.css`
- **Desenvolvimento:** Pode carregar versões legíveis (opcional)

**NUNCA carregar versão legível em produção:**
- Impacto negativo no carregamento
- Arquivos maiores
- Performance reduzida

---

## Carregamento por Página

**Carregar apenas os arquivos necessários em cada página:**

**Exemplo:**
```html
<!-- Página de dashboard -->
<link rel="stylesheet" href="/styles/app.min.css">
<link rel="stylesheet" href="/styles/dashboard.min.css">

<!-- Página de tabela -->
<link rel="stylesheet" href="/styles/app.min.css">
<link rel="stylesheet" href="/styles/table.min.css">
```

**NÃO carregar todos os arquivos em todas as páginas.**

---

## Django: Static Files

**Desenvolvimento:**
- Servir arquivos estáticos via Django URLs
- Adicionar em `urls.py` principal:

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Produção:**
- Usar `collectstatic` para coletar arquivos
- Servir via nginx (Django não serve estáticos em produção)
- Configurar nginx para servir arquivos estáticos

**Comando:**
```bash
python manage.py collectstatic
```

---

## Minificação

**Ferramentas recomendadas:**
- `cssnano` (via postcss)
- `clean-css`
- `csso`

**Processo:**
1. Manter arquivos legíveis no repositório
2. Minificar durante build/deploy
3. Commitar apenas arquivos legíveis (`.min.css` pode ser gerado)

---

## Organização

**Cada arquivo deve ter responsabilidade única:**
- `app.css` - Reset, variáveis, tipografia, layout geral
- `componentes.css` - Botões, cards, modais, etc.
- `dashboard.css` - Layout específico do dashboard
- `table.css` - Estilos de tabelas e listagens
- `menu.css` - Navegação, sidebar, header

---

## Checklist

- [ ] Arquivos organizados em `styles/`
- [ ] Cada arquivo com responsabilidade única
- [ ] Versões `.min.css` criadas para produção
- [ ] Apenas `.min.css` carregado em produção
- [ ] Carregamento por página (não todos os arquivos)
- [ ] Django `collectstatic` configurado (se aplicável)
- [ ] Nginx configurado para servir estáticos (produção)

---

## Referências

- **Django:** `skills/backend/django/SKILL.md`
- **Templates:** `core/templates/`

---

**Estas regras são obrigatórias para todos os projetos frontend.**

