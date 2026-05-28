---
name: web-performance-audit
description: Analisa performance de projetos web, verificando Core Web Vitals, otimizações implementadas e oportunidades de melhoria. Use para auditorias completas de performance.
---

# Web Performance Audit Skill

Quando analisar a performance de um projeto web, siga estas etapas sistematicamente:

## 1. Análise de Core Web Vitals

### Largest Contentful Paint (LCP)

- Meça o tempo de renderização do maior elemento visível
- Meta: < 2.5s (bom), 2.5s-4s (precisa melhorar), > 4s (ruim)
- Identifique o elemento LCP (imagem, vídeo, bloco de texto)
- Verifique otimizações aplicadas ao elemento LCP
- Analise tempo de resposta do servidor
- Confirme uso de CDN para recursos estáticos

### First Input Delay (FID) / Interaction to Next Paint (INP)

- Meça latência na primeira interação do usuário
- Meta FID: < 100ms (bom), 100-300ms (precisa melhorar), > 300ms (ruim)
- Meta INP: < 200ms (bom), 200-500ms (precisa melhorar), > 500ms (ruim)
- Identifique long tasks que bloqueiam a thread principal
- Verifique JavaScript que executa durante carregamento
- Analise event handlers e sua eficiência

### Cumulative Layout Shift (CLS)

- Meça mudanças inesperadas no layout
- Meta: < 0.1 (bom), 0.1-0.25 (precisa melhorar), > 0.25 (ruim)
- Identifique elementos que causam shifts
- Verifique dimensões explícitas em imagens e vídeos
- Confirme espaço reservado para conteúdo dinâmico
- Analise fontes web e seu carregamento

## 2. Análise de Recursos e Assets

### Imagens

- Verifique formatos modernos (WebP, AVIF)
- Confirme compressão adequada (sem perda de qualidade perceptível)
- Avalie uso de responsive images (srcset, sizes)
- Verifique lazy loading (loading="lazy")
- Confirme dimensões corretas (sem redimensionamento via CSS)
- Analise uso de image sprites para ícones
- Verifique CDN para delivery de imagens
- Confirme uso de blur-up ou LQIP (Low Quality Image Placeholder)

### Fontes Web

- Avalie estratégia de carregamento (font-display: swap, optional)
- Verifique formatos modernos (WOFF2)
- Confirme preload de fontes críticas
- Analise número de variantes carregadas
- Verifique subsetting (apenas caracteres necessários)
- Confirme self-hosting vs Google Fonts

### CSS

- Verifique minificação
- Confirme remoção de CSS não utilizado
- Analise critical CSS inline
- Verifique bloqueio de renderização
- Avalie uso de CSS-in-JS e seu impacto
- Confirme concatenação/bundling adequado
- Verifique media queries para carregamento condicional

### JavaScript

- Verifique minificação e uglification
- Confirme tree shaking
- Analise code splitting por rotas/componentes
- Verifique async/defer em scripts
- Avalie tamanho dos bundles
- Confirme remoção de código morto
- Verifique uso de dynamic imports
- Analise polyfills (carregar apenas quando necessário)
- Confirme module/nomodule pattern

## 3. Análise de Carregamento e Rendering

### Critical Rendering Path

- Identifique recursos que bloqueiam renderização
- Verifique ordem de carregamento de recursos
- Confirme priorização de conteúdo above-the-fold
- Analise número de round trips necessários
- Verifique uso de resource hints (preconnect, prefetch, preload)

### Estratégias de Loading

- Confirme lazy loading de imagens e iframes
- Verifique code splitting e chunks dinâmicos
- Analise estratégia de prefetching de rotas
- Confirme streaming de HTML quando possível
- Verifique progressive enhancement

### Server-Side Rendering (SSR) / Static Generation

- Avalie uso de SSR, SSG ou CSR
- Verifique hydration e seu impacto
- Confirme streaming SSR quando aplicável
- Analise tempo de Time to First Byte (TTFB)

## 4. Análise de Rede e Delivery

### HTTP e Protocolo

- Confirme uso de HTTP/2 ou HTTP/3
- Verifique multiplexing de recursos
- Analise server push (quando aplicável)
- Confirme compressão (Gzip, Brotli)
- Verifique headers de cache adequados

### Caching

- Analise estratégia de cache browser (Cache-Control headers)
- Verifique cache de service worker
- Confirme versionamento de assets (cache busting)
- Avalie uso de stale-while-revalidate
- Verifique CDN caching

### CDN e Edge Computing

- Confirme uso de CDN para assets estáticos
- Verifique distribuição geográfica
- Analise edge caching e edge functions
- Confirme failover e redundância

### Conexões e DNS

- Verifique número de domínios diferentes
- Confirme DNS prefetch para domínios externos
- Analise tempo de DNS lookup
- Verifique keep-alive connections
- Confirme preconnect para origens críticas

## 5. Análise de JavaScript Runtime

### Execução e Processamento

- Identifique long tasks (> 50ms)
- Verifique uso da thread principal
- Analise parsing e compilation time
- Confirme uso de Web Workers para tarefas pesadas
- Verifique uso de requestIdleCallback
- Analise uso de requestAnimationFrame

### Frameworks e Bibliotecas

- Avalie tamanho do framework/biblioteca
- Verifique versões (podem ter melhorias de performance)
- Confirme tree shaking de bibliotecas
- Analise alternatives mais leves quando aplicável
- Verifique virtual DOM overhead (se aplicável)

### Third-party Scripts

- Identifique todos os scripts de terceiros
- Avalie impacto de cada script (analytics, ads, widgets)
- Verifique carregamento assíncrono
- Confirme uso de facades para widgets pesados
- Analise alternativas self-hosted

## 6. Análise de Performance Mobile

### Responsividade

- Verifique adaptive loading (serve menos recursos em mobile)
- Confirme uso de media queries para imagens
- Analise touch targets e seu tamanho
- Verifique scroll performance (scroll jank)

### Network Conditions

- Teste em conexões lentas (3G, Slow 4G)
- Verifique uso de Network Information API
- Confirme graceful degradation
- Analise offline capabilities (PWA)

### Device Capabilities

- Teste em dispositivos de baixo custo
- Verifique uso de CPU e memória
- Confirme adaptação a hardware limitado

## 7. Análise de Métricas Adicionais

### Time to First Byte (TTFB)

- Meta: < 600ms (bom), 600ms-1.8s (precisa melhorar), > 1.8s (ruim)
- Verifique tempo de resposta do servidor
- Analise processamento server-side
- Confirme otimizações de database queries

### First Contentful Paint (FCP)

- Meta: < 1.8s (bom), 1.8s-3s (precisa melhorar), > 3s (ruim)
- Verifique primeiro conteúdo renderizado
- Confirme critical CSS inline
- Analise bloqueios de renderização

### Time to Interactive (TTI)

- Meta: < 3.8s (bom), 3.8s-7.3s (precisa melhorar), > 7.3s (ruim)
- Verifique quando a página fica totalmente interativa
- Analise JavaScript que executa após load
- Confirme priorização de interatividade

### Total Blocking Time (TBT)

- Meta: < 200ms (bom), 200-600ms (precisa melhorar), > 600ms (ruim)
- Identifique tempo total de bloqueio
- Verifique long tasks durante carregamento

### Speed Index

- Meta: < 3.4s (bom), 3.4s-5.8s (precisa melhorar), > 5.8s (ruim)
- Avalie velocidade visual de carregamento

## 8. Análise de Build e Bundling

### Build Process

- Verifique configuração de webpack/vite/rollup
- Confirme mode production ativado
- Analise source maps (apenas dev)
- Verifique otimizações do bundler

### Bundle Analysis

- Identifique bundles grandes (> 200KB)
- Verifique duplicação de código
- Confirme vendor splitting adequado
- Analise dependências pesadas
- Verifique moment.js e alternativas (day.js)

## 9. Análise de Monitoramento

### Real User Monitoring (RUM)

- Verifique presença de RUM
- Confirme coleta de Core Web Vitals
- Analise dados por dispositivo/região/navegador

### Synthetic Monitoring

- Confirme testes automatizados de performance
- Verifique Lighthouse CI no pipeline
- Analise performance budgets configurados

---

## Formato do Relatório Final

Ao concluir a análise, forneça um relatório estruturado:

### 📊 Score de Performance Geral

Atribua uma pontuação de 0-100 baseada em:

- Core Web Vitals (30 pontos)
- Otimização de Recursos (25 pontos)
- JavaScript Performance (20 pontos)
- Network e Caching (15 pontos)
- Mobile Performance (10 pontos)

### ✅ Otimizações Implementadas

Liste todas as boas práticas de performance já aplicadas no projeto, organizadas por categoria.

### 🔴 Problemas Críticos

Liste problemas que impactam severamente a performance:

- Descrição do problema
- Impacto medido ou estimado
- Métrica afetada (LCP, CLS, FID/INP, etc.)
- Prioridade: CRÍTICA

### ⚠️ Problemas Moderados

Liste problemas de impacto médio que devem ser corrigidos:

- Descrição do problema
- Impacto estimado
- Prioridade: ALTA ou MÉDIA

### 💡 Oportunidades de Melhoria

Forneça sugestões específicas priorizadas:

**Alta Prioridade** (ganhos significativos):

- Ação recomendada
- Ganho estimado em segundos/pontos
- Esforço de implementação (baixo/médio/alto)

**Média Prioridade** (melhorias incrementais):

- Ação recomendada
- Ganho estimado
- Esforço de implementação

**Baixa Prioridade** (refinamentos):

- Ação recomendada
- Ganho estimado
- Esforço de implementação

### 📈 Métricas Detalhadas

**Core Web Vitals:**

- LCP: [valor] - [status: bom/precisa melhorar/ruim]
- FID/INP: [valor] - [status]
- CLS: [valor] - [status]

**Outras Métricas:**

- TTFB: [valor]
- FCP: [valor]
- TTI: [valor]
- TBT: [valor]
- Speed Index: [valor]

**Recursos:**

- Total de requests: [número]
- Tamanho total da página: [KB/MB]
- JavaScript total: [KB]
- CSS total: [KB]
- Imagens total: [KB]
- Fontes total: [KB]

### 🎯 Plano de Ação Recomendado

Liste as 5-7 ações prioritárias em ordem de implementação:

1. **[Ação]** - Impacto: [alto/médio/baixo] - Esforço: [baixo/médio/alto]
2. **[Ação]** - Impacto: [alto/médio/baixo] - Esforço: [baixo/médio/alto]
3. [...]

### 📱 Performance Mobile vs Desktop

Compare métricas entre mobile e desktop, destacando gaps significativos.

### 🌍 Performance por Região (se dados disponíveis)

Analise variações geográficas de performance.

---

## Diretrizes de Análise

- **Seja baseado em dados**: use métricas reais quando possível (Lighthouse, WebPageTest, Chrome DevTools)
- **Seja específico**: cite números, tamanhos de arquivos, tempos medidos
- **Priorize impacto**: foque em otimizações que trazem maior ganho
- **Considere trade-offs**: nem toda otimização vale o esforço
- **Seja realista**: estime esforço de implementação
- **Pense no usuário**: performance percebida importa tanto quanto métricas
- **Considere o contexto**: e-commerce, blog, SaaS têm necessidades diferentes
- **Forneça benchmarks**: compare com médias da indústria quando relevante
