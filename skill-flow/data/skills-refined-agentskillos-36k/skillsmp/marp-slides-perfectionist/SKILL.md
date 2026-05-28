---
name: Marp Slides Perfectionist
description: Especialista em refinamento, ajuste de layout e garantia de qualidade visual para apresentações Marp. Foca em evitar overflow e maximizar legibilidade.
---

# 🧐 Skill Marp Slides Perfectionist

Esta skill foca no refinamento cirúrgico de apresentações existentes. O objetivo não é reescrever o conteúdo, mas garantir que ele seja apresentado da forma mais elegante e legível possível.

## 📏 Critérios de Análise (Checklist de Perfeccionismo)

### 1. Prevenção de Overflow (Estouro de Conteúdo)
O erro mais comum em slides é colocar texto demais, fazendo com que o conteúdo saia da área visível ou fique ilegível.
*   **Regra dos 7 Linhas**: Slides com bullet points não devem exceder ~7 itens.
*   **Densidade de Texto**: Parágrafos longos (>40 palavras) devem ser:
    *   Quebrados em tópicos.
    *   Divididos em múltiplos slides.
    *   Transformados em "Speaker Notes" (usando o comentário `<!-- ... -->`).

### 2. Layout e Imagens
*   **Imagens de Fundo**: Se usar `bg`, garanta que o texto tenha contraste.
    *   *Correção*: Adicionar `color: #fff` ou `text-shadow` se o fundo for escuro/complexo.
    *   *Correção*: Usar filtros do Marp na imagem: `![bg brightness:0.5](img.jpg)`.
*   **Alinhamento**: Slides de título devem geralmente usar `class: lead` para centralização perfeita.

### 3. Consistência Visual
*   Variações de fonte e cores devem ser propositais, não acidentais.
*   Verificar se diretivas globais (`paginate`, `theme`) estão configuradas corretamente no início.

## 🔧 Técnicas de Refinamento (Sem perder conteúdo)

### A. Lidando com Texto Demais
⛔ **Ruim**: Diminuir a fonte (`font-size: 10px`) para caber tudo.
✅ **Bom**: Dividir o slide horizontalmente ou em sequência.

**Técnica de Divisão (Split):**
Se um slide tem uma lista gigante, sugira quebrar em dois slides:
"Título (Parte 1)" e "Título (Parte 2)".

### B. Ajuste Fino de Imagens
Se uma imagem está "comendo" o texto em um layout de duas colunas (`bg right`), ajuste a proporção:
De `![bg right](img.jpg)` (50/50)
Para `![bg right:33%](img.jpg)` (dá mais espaço para o texto).

### C. Contraste em Dark Mode/Invert
Se o slide usa `class: invert` (fundo escuro), verifique se emojis ou imagens (logos) têm fundo transparente. Se tiverem fundo branco, fica feio.
*   *Ação*: Sugerir remoção de fundo da imagem ou colocar a imagem dentro de um container branco estilizado.

## 🤖 Instruções para o Agente
Ao usar esta skill para revisar:
1.  **Não assuma deletar**: Se algo parece sobrar, pergunte como reestruturar.
2.  **CSS Scoped**: Para correções pontuais, use `<style scoped>` no slide específico em vez de CSS global.
3.  **Preserve a Semântica**: Não troque `## Título` por `**Título**` apenas por estética, a menos que necessário para layout.
