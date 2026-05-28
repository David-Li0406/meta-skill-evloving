---
name: Criador de Slides Marp
description: Guia especialista para criar apresentações de alta qualidade e visualmente agradáveis usando Marp (Markdown).
---

# Skill Criador de Slides Marp

Esta skill ajuda você a criar apresentações profissionais e bonitas usando Marp.

## 🚀 Início Rápido

Para ativar o Marp em um arquivo markdown, adicione este frontmatter logo no início:

```markdown
---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
errorMessage: ''
---
```

## 🎨 Conceitos Principais

### 1. Temas
O Marp vem com 3 temas integrados:
- `default`: Fundo branco limpo. Bom para documentação.
- `gaia`: Focado em slides, colorido. Ótimo para palestras. (Suporta `class: lead` para slides de título e centralização).
- `uncover`: Minimalista, conteúdo centralizado. Bom para pontos rápidos e texto grande.

### 2. Diretivas
Configurações globais ou por slide usadas no frontmatter ou comentários HTML.
- `paginate: true` - Adiciona números de página.
- `header: 'Meu Título'` - Adiciona um cabeçalho em todos os slides.
- `footer: 'Confidencial'` - Adiciona um rodapé.
- `backgroundColor: #f0f0f0` - Define a cor de fundo do slide.
- `color: #333` - Define a cor do texto.

### 3. Imagens de Fundo
O Marp possui uma sintaxe poderosa para imagens de fundo.
- `![bg](image.jpg)`: Fundo para o slide.
- `![bg cover](image.jpg)`: Cobre o slide inteiro (padrão).
- `![bg contain](image.jpg)`: Contém a imagem totalmente visível.
- `![bg right](image.jpg)`: Divide a tela, imagem à direita (50%).
- `![bg left:33%](image.jpg)`: Divide a tela, imagem à esquerda (33%).

## 💅 Estilo e Estética (Boas Práticas Visuais)

1.  **Hierarquia Visual**: Use H1 para títulos principais (um por slide), H2 para cabeçalhos de seção.
2.  **Menos é Mais**: Tópicos (bullets) devem ser concisos. Evite paredes de texto. Seja direto.
3.  **Contraste**: Garanta que o texto seja legível contra os fundos. Use `class: invert` no tema Gaia para slides em modo escuro.
4.  **Blocos de Código**: O Marp lida com destaque de sintaxe automaticamente. Ótimo para palestras técnicas.

## 🛠️ Modelos de Slides Comuns

### Slide de Título (Capa - Tema Gaia)
```markdown
---
marp: true
theme: gaia
_class: lead
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# Título da Apresentação
## Subtítulo vai aqui
### Nome do Autor
```

### Layout de Duas Colunas (Imagem à Direita)
```markdown
---
# Nossa Estratégia

- **Ponto 1**: Descrição.
- **Ponto 2**: Descrição.
- **Ponto 3**: Descrição.

![bg right:40%](https://images.unsplash.com/photo-1519389950473-47ba0277781c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80)
```

### Citação / Frase de Impacto
```markdown
<!-- _class: lead -->

> "A única maneira de fazer um ótimo trabalho é amar o que você faz."
>
> — Steve Jobs
```

## 📐 CSS Avançado

Você pode injetar CSS diretamente para ajustes finos:

```markdown
<style>
section {
  font-family: 'Inter', sans-serif;
}
h1 {
  color: #2D3748;
}
</style>
```

Ou escopado para um slide específico:
```markdown
<!-- _class: custom-slide -->

<style scoped>
.custom-slide h1 {
  color: red;
}
</style>
```
