---
name: Jo Terapeuta Capilar Platform
description: Private client tracking platform for hair therapy - Next.js 15 + Supabase
---

# Jo Terapeuta Capilar - Plataforma de Acompanhamento Capilar

## Visão Geral

Plataforma privada de acompanhamento capilar, separada do site principal (Squarespace).

| Item | Valor |
|------|-------|
| **URL Produção** | app.joterapeutacapilar.com |
| **Stack** | Next.js 15 + Supabase + Vercel |
| **Supabase Project** | `cpgophielhqiagfcaabp` |
| **Abordagem** | Mobile-First |

---

## Arquitetura

```
joterapeutacapilar.com     → Squarespace (site + loja)
app.joterapeutacapilar.com → Esta plataforma (Next.js)
```

---

## Tipos de Utilizador

| Role | Descrição |
|------|-----------|
| `admin` | Terapeuta - gere clientes, cria atualizações, posts |
| `client` | Cliente - vê as suas atualizações, feed de conteúdos |

---

## Base de Dados

### Tabelas Principais

1. **profiles** - Perfis de utilizador (extends auth.users)
   - `role`: 'admin' | 'client'
   - `name`, `email`, `phone`, `avatar_url`, `notes`

2. **client_updates** - Atualizações personalizadas
   - Criadas pelo admin para um cliente específico
   - `client_id`, `admin_id`, `title`, `content`

3. **attachments** - Ficheiros anexos às atualizações
   - `file_type`: 'image' | 'pdf'
   - Limite: ~5-10MB por ficheiro

4. **posts** - Conteúdos gerais (feed)
   - Visíveis para todos os autenticados quando `published = true`

### Trigger Automático
- Quando um utilizador faz signup, é criado automaticamente um perfil com role 'client'
- Admin pode alterar o role depois

---

## Decisões de Produto

| Decisão | Escolha |
|---------|---------|
| Registo de clientes | Admin cria conta (não há self-registration) |
| Posts do feed | Só para autenticados |
| Notificações email | Fase 2 (futuro) |
| Ficheiros suportados | Imagens + PDF |

---

## Estrutura de Rotas

```
/login                    → Página de login
/                         → Redirect baseado em role

/admin                    → Dashboard admin
/admin/clientes           → Lista de clientes
/admin/clientes/novo      → Criar cliente
/admin/clientes/[id]      → Detalhes do cliente + atualizações
/admin/conteudos          → Gerir posts

/cliente                  → Dashboard cliente
/cliente/atualizacoes     → Minhas atualizações
/cliente/conteudos        → Feed de conteúdos gerais
```

---

## Design System

### Cores (do site Squarespace existente)
```css
--color-white: #FFFFFF;      /* Background principal */
--color-black: #000000;      /* Texto, botões */
--color-nude: #E5D3C6;       /* Backgrounds secundários */
--color-off-white: #FAFAFA;  /* Fundos alternados */
```

### Tipografia
- **Headings**: Manrope (600-700)
- **Body**: Poppins (400-500)

### UI Components
- **Botões**: Border-radius 0px (cantos retos - marca da cliente)
- **Mobile-first**: Touch targets mínimo 44x44px
- **Bottom navigation** para área cliente

---

## Ficheiros Importantes

```
src/
├── lib/supabase/
│   ├── client.ts     # Browser client
│   ├── server.ts     # Server components
│   └── middleware.ts # Auth helper
├── middleware.ts     # Route protection
└── types/
    └── database.ts   # TypeScript types

supabase/migrations/
├── 001_initial_schema.sql
└── 002_rls_policies.sql
```

---

## Comandos

```bash
# Desenvolvimento
npm run dev

# Build
npm run build

# Deploy
vercel --prod

# Ligar ao Supabase
supabase link --project-ref cpgophielhqiagfcaabp

# Gerar types
supabase gen types typescript --project-id cpgophielhqiagfcaabp > src/types/supabase.ts
```

---

## Regras Importantes

1. **Língua UI**: Português de Portugal (PT-PT)
   - "Utilizador" não "Usuário"
   - "Guardar" não "Salvar"
   - "Terminar sessão" não "Sair"

2. **Mobile-First**: Clientes usam quase exclusivamente telemóvel

3. **Segurança**: RLS ativo - clientes só vêem os seus próprios dados

4. **Simplicidade**: Produto calmo e profissional, não é rede social
