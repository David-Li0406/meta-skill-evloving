---
name: brand-guidelines
description: Aplica as cores e tipografia oficiais da marca Anthropic a qualquer tipo de artefato que possa se beneficiar da aparência e sensação da Anthropic. Use quando cores da marca ou diretrizes de estilo, formatação visual ou padrões de design da empresa se aplicarem.
license: Termos completos em LICENSE.txt
---

# Estilo da Marca Anthropic

## Visão Geral

Para acessar os recursos oficiais de identidade e estilo da marca Anthropic, use esta habilidade.

**Palavras-chave**: branding, identidade corporativa, identidade visual, pós-processamento, estilo, cores da marca, tipografia, marca Anthropic, formatação visual, design visual

## Diretrizes da Marca

### Cores

**Cores Principais:**

- Escuro: `#141413` - Texto primário e fundos escuros
- Claro: `#faf9f5` - Fundos claros e texto em fundo escuro
- Cinza Médio: `#b0aea5` - Elementos secundários
- Cinza Claro: `#e8e6dc` - Fundos sutis

**Cores de Destaque:**

- Laranja: `#d97757` - Destaque primário
- Azul: `#6a9bcc` - Destaque secundário
- Verde: `#788c5d` - Destaque terciário

### Tipografia

- **Títulos**: Poppins (com fallback para Arial)
- **Texto do Corpo**: Lora (com fallback para Georgia)
- **Nota**: As fontes devem estar pré-instaladas no seu ambiente para melhores resultados

## Recursos

### Aplicação Inteligente de Fontes

- Aplica a fonte Poppins aos títulos (24pt e maiores)
- Aplica a fonte Lora ao texto do corpo
- Reverte automaticamente para Arial/Georgia se fontes personalizadas não estiverem disponíveis
- Preserva a legibilidade em todos os sistemas

### Estilo de Texto

- Títulos (24pt+): Fonte Poppins
- Texto do corpo: Fonte Lora
- Seleção inteligente de cores com base no fundo
- Preserva a hierarquia e formatação do texto

### Forma e Cores de Destaque

- Formas não textuais usam cores de destaque
- Alterna entre destaques laranja, azul e verde
- Mantém interesse visual enquanto permanece dentro da marca

## Detalhes Técnicos

### Gerenciamento de Fontes

- Usa fontes Poppins e Lora instaladas no sistema quando disponíveis
- Fornece fallback automático para Arial (títulos) e Georgia (corpo)
- Nenhuma instalação de fonte necessária - funciona com fontes existentes do sistema
- Para melhores resultados, pré-instale as fontes Poppins e Lora no seu ambiente

### Aplicação de Cores

- Usa valores de cor RGB para correspondência precisa da marca
- Aplicado via classe RGBColor do python-pptx
- Mantém a fidelidade da cor em diferentes sistemas
