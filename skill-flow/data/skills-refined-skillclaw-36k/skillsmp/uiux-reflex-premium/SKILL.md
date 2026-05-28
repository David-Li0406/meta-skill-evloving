---
name: UI/UX Reflex Premium
description: Diretrizes de design system, tokens e componentes visuais premium para o ecossistema Biodiagnóstico utilizando Reflex.
---

# Skill: UI/UX Reflex Premium

Esta skill define a identidade visual "Biodiagnóstico 2.0". Ela deve ser utilizada para garantir consistência estética, usabilidade (acessibilidade) e o "feeling" premium em todas as telas da aplicação.

## 🎨 Princípios de Design
1. **Glassmorphism**: Uso de transparências e blur em modais e overlays para profundidade.
2. **Respiro Visual**: Espaçamentos generosos baseados em múltiplos de 4 (utilizando a classe `Spacing`).
3. **Micro-interações**: Botões e elementos clicáveis devem reagir suavemente ao hover e clique (escalonamento, brilho).
4. **Legibilidade**: Contraste alto usando `Color.DEEP` para títulos e `Color.TEXT_PRIMARY` para o corpo.
5. **Motion System**: Animações não devem ser aleatórias. Use `transition_duration="200ms"` para interações rápidas e `300ms` para entradas de página com `transition_timing_function="ease-in-out"`.

## 🛠️ Ferramentas e Tokens
Os tokens estão definidos no arquivo `biodiagnostico_app/biodiagnostico_app/styles.py`.

- **Cores**: `Color.PRIMARY` (#4CAF50), `Color.DEEP` (#1B5E20), `Color.BACKGROUND` (#F8F9FA).
- **Sombras**: `Design.SHADOW_MD` para cards padrão, `Design.SHADOW_LG` para elementos flutuantes.
- **Raio de Borda**: `Design.RADIUS_LG` (12px) é o padrão para inputs e botões.

## 📝 Como Implementar Componentes
Sempre verifique a pasta `examples/` nesta skill para snippets prontos de:
- `glass_card.py`: Cards com efeito de vidro.
- `premium_button.py`: Botões com gradiente e animação.
- `data_table.py`: Tabelas formatadas para leitura de dados médicos.
- `advanced_data_table.py`: Tabela complexa com badges, ações e scroll.
- `metric_card_chart.py`: Card de métrica com gráfico sparkline embutido.
- `pdf_export_template.py`: Modal de configuração para exportação de relatórios.

## 🚨 Regras Inegociáveis
1. **Acessibilidade**: Todo input deve ter `min_height="44px"`.
2. **Consistência**: Nunca use cores hexadecimais soltas; use sempre a classe `Color`.
3. **Animação**: Toda página deve carregar com uma animação de `fadeInUp`.
4. **Layout Oficial**: Novas páginas devem, por padrão, ser integradas ao `authenticated_layout()` ou conter a `navbar()` e o fundo `Color.BACKGROUND` para evitar o aspecto de "página solta".
5. **Harmonia**: O uso de `GLASS_STYLE` deve ser moderado (modais/overlays). Cards de dashboard devem preferir `Color.SURFACE` sólido com `_hover` para profundidade.
6. **Acessibilidade ARIA**: Sempre que usar um ícone como botão sem texto, adicione `aria_label="Descrição da ação"`.

## 🎨 Ferramentas de Design (Scripts)

Use esses "fiscais" para garantir que o app continue lindo e rápido:

1.  **Auditoria Visual** (O Fiscal):
    - Comando: `py .agent/skills/ui-ux-reflex-premium/scripts/auditoria_visual.py`
    - Função: Garante que ninguém usou cores fora do padrão (Hex soltos).

2.  **Alinhador Automático** (O Alinhador):
    - Comando: `py .agent/skills/ui-ux-reflex-premium/scripts/alinhador_auto.py`
    - Função: Verifica se o "respiro" entre os elementos segue os tokens `Spacing`.

3.  **Otimizador de Imagens** (O Otimizador):
    - Comando: `py .agent/skills/ui-ux-reflex-premium/scripts/otimizador_img.py`
    - Função: Diminui o peso das imagens em `assets/` para carregamento instantâneo.

4.  **Verificador de Contraste** (O Verificador):
    - Comando: `py .agent/skills/ui-ux-reflex-premium/scripts/check_contraste.py`
    - Função: Garante que o texto está legível (WCAG AA). ⚠️ A paleta atual pode ter problemas de contraste.

5.  **Gerador de Ícones** (O Artesão):
    - Comando: `py .agent/skills/ui-ux-reflex-premium/scripts/gerador_icones.py`
    - Função: Cria automaticamente favicons e ícones mobile na pasta `assets`.

---

## 👁️ Check de Referência Visual
Antes de entregar, compare o código com as imagens de referência do projeto (Dashboard e Controle de Qualidade):
- O cabeçalho está alinhado?
- A cor de fundo é a correta (#F8F9FA)?
- O respiro (`padding`) condiz com o site real?
