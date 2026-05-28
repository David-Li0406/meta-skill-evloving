# Referência Técnica Office Open XML para PowerPoint

**Importante: Leia este documento inteiro antes de começar.** Regras críticas de esquema XML e requisitos de formatação são cobertos por toda parte. A implementação incorreta pode criar arquivos PPTX inválidos que o PowerPoint não pode abrir.

## Diretrizes Técnicas

### Conformidade de Esquema

- **Ordenação de elementos em `<p:txBody>`**: `<a:bodyPr>`, `<a:lstStyle>`, `<a:p>`
- **Espaço em branco**: Adicione `xml:space='preserve'` aos elementos `<a:t>` com espaços à esquerda/direita
- **Unicode**: Caracteres de escape no conteúdo ASCII: `"` torna-se `&#8220;`
- **Imagens**: Adicione a `ppt/media/`, referencie no XML do slide, defina dimensões para caber nos limites do slide
- **Relacionamentos**: Atualize `ppt/slides/_rels/slideN.xml.rels` para os recursos de cada slide
- **Atributo sujo**: Adicione `dirty="0"` aos elementos `<a:rPr>` e `<a:endParaRPr>` para indicar estado limpo

## Estrutura da Apresentação

### Estrutura Básica de Slide

```xml
<!-- ppt/slides/slide1.xml -->
<p:sld>
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>...</p:nvGrpSpPr>
      <p:grpSpPr>...</p:grpSpPr>
      <!-- Formas vão aqui -->
    </p:spTree>
  </p:cSld>
</p:sld>
```

### Caixa de Texto / Forma com Texto

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="2" name="Título"/>
    <p:cNvSpPr>
      <a:spLocks noGrp="1"/>
    </p:cNvSpPr>
    <p:nvPr>
      <p:ph type="ctrTitle"/>
    </p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="838200" y="365125"/>
      <a:ext cx="7772400" cy="1470025"/>
    </a:xfrm>
  </p:spPr>
  <p:txBody>
    <a:bodyPr/>
    <a:lstStyle/>
    <a:p>
      <a:r>
        <a:t>Título do Slide</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

### Formatação de Texto

```xml
<!-- Negrito -->
<a:r>
  <a:rPr b="1"/>
  <a:t>Texto em Negrito</a:t>
</a:r>

<!-- Itálico -->
<a:r>
  <a:rPr i="1"/>
  <a:t>Texto em Itálico</a:t>
</a:r>

<!-- Sublinhado -->
<a:r>
  <a:rPr u="sng"/>
  <a:t>Sublinhado</a:t>
</a:r>

<!-- Realçado -->
<a:r>
  <a:rPr>
    <a:highlight>
      <a:srgbClr val="FFFF00"/>
    </a:highlight>
  </a:rPr>
  <a:t>Texto Realçado</a:t>
</a:r>

<!-- Fonte e Tamanho -->
<a:r>
  <a:rPr sz="2400" typeface="Arial">
    <a:solidFill>
      <a:srgbClr val="FF0000"/>
    </a:solidFill>
  </a:rPr>
  <a:t>Arial Colorido 24pt</a:t>
</a:r>

<!-- Exemplo de formatação completa -->
<a:r>
  <a:rPr lang="pt-BR" sz="1400" b="1" dirty="0">
    <a:solidFill>
      <a:srgbClr val="FAFAFA"/>
    </a:solidFill>
  </a:rPr>
  <a:t>Texto formatado</a:t>
</a:r>
```

### Listas

```xml
<!-- Lista com marcadores -->
<a:p>
  <a:pPr lvl="0">
    <a:buChar char="•"/>
  </a:pPr>
  <a:r>
    <a:t>Primeiro ponto</a:t>
  </a:r>
</a:p>

<!-- Lista numerada -->
<a:p>
  <a:pPr lvl="0">
    <a:buAutoNum type="arabicPeriod"/>
  </a:pPr>
  <a:r>
    <a:t>Primeiro item numerado</a:t>
  </a:r>
</a:p>

<!-- Recuo de segundo nível -->
<a:p>
  <a:pPr lvl="1">
    <a:buChar char="•"/>
  </a:pPr>
  <a:r>
    <a:t>Marcador recuado</a:t>
  </a:r>
</a:p>
```

### Formas

```xml
<!-- Retângulo -->
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="3" name="Rectangle"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="1000000" y="1000000"/>
      <a:ext cx="3000000" cy="2000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="FF0000"/>
    </a:solidFill>
    <a:ln w="25400">
      <a:solidFill>
        <a:srgbClr val="000000"/>
      </a:solidFill>
    </a:ln>
  </p:spPr>
</p:sp>

<!-- Retângulo Arredondado -->
<p:sp>
  <p:spPr>
    <a:prstGeom prst="roundRect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:sp>

<!-- Círculo/Elipse -->
<p:sp>
  <p:spPr>
    <a:prstGeom prst="ellipse">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:sp>
```

### Imagens

```xml
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="4" name="Picture">
      <a:hlinkClick r:id="" action="ppaction://media"/>
    </p:cNvPr>
    <p:cNvPicPr>
      <a:picLocks noChangeAspect="1"/>
    </p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="rId2"/>
    <a:stretch>
      <a:fillRect/>
    </a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm>
      <a:off x="1000000" y="1000000"/>
      <a:ext cx="3000000" cy="2000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:pic>
```

### Tabelas

```xml
<p:graphicFrame>
  <p:nvGraphicFramePr>
    <p:cNvPr id="5" name="Table"/>
    <p:cNvGraphicFramePr>
      <a:graphicFrameLocks noGrp="1"/>
    </p:cNvGraphicFramePr>
    <p:nvPr/>
  </p:nvGraphicFramePr>
  <p:xfrm>
    <a:off x="1000000" y="1000000"/>
    <a:ext cx="6000000" cy="2000000"/>
  </p:xfrm>
  <a:graphic>
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">
      <a:tbl>
        <a:tblGrid>
          <a:gridCol w="3000000"/>
          <a:gridCol w="3000000"/>
        </a:tblGrid>
        <a:tr h="500000">
          <a:tc>
            <a:txBody>
              <a:bodyPr/>
              <a:lstStyle/>
              <a:p>
                <a:r>
                  <a:t>Célula 1</a:t>
                </a:r>
              </a:p>
            </a:txBody>
          </a:tc>
          <a:tc>
            <a:txBody>
              <a:bodyPr/>
              <a:lstStyle/>
              <a:p>
                <a:r>
                  <a:t>Célula 2</a:t>
                </a:r>
              </a:p>
            </a:txBody>
          </a:tc>
        </a:tr>
      </a:tbl>
    </a:graphicData>
  </a:graphic>
</p:graphicFrame>
```

### Layouts de Slide

```xml
<!-- Layout de Slide de Título -->
<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="ctrTitle"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- Conteúdo do título -->
</p:sp>

<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="subTitle" idx="1"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- Conteúdo do subtítulo -->
</p:sp>

<!-- Layout de Slide de Conteúdo -->
<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="title"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- Título do slide -->
</p:sp>

<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="body" idx="1"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- Corpo do conteúdo -->
</p:sp>
```

## Atualizações de Arquivo

Ao adicionar conteúdo, atualize estes arquivos:

**`ppt/_rels/presentation.xml.rels`:**

```xml
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
```

**`ppt/slides/_rels/slide1.xml.rels`:**

```xml
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/>
```

**`[Content_Types].xml`:**

```xml
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpg" ContentType="image/jpeg"/>
<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
```

**`ppt/presentation.xml`:**

```xml
<p:sldIdLst>
  <p:sldId id="256" r:id="rId1"/>
  <p:sldId id="257" r:id="rId2"/>
</p:sldIdLst>
```

**`docProps/app.xml`:** Atualizar contagem de slides e estatísticas

```xml
<Slides>2</Slides>
<Paragraphs>10</Paragraphs>
<Words>50</Words>
```

## Operações de Slide

### Adicionando um Novo Slide

Ao adicionar um slide ao final da apresentação:

1. **Crie o arquivo de slide** (`ppt/slides/slideN.xml`)
2. **Atualize `[Content_Types].xml`**: Adicione Override para o novo slide
3. **Atualize `ppt/_rels/presentation.xml.rels`**: Adicione relacionamento para o novo slide
4. **Atualize `ppt/presentation.xml`**: Adicione ID de slide a `<p:sldIdLst>`
5. **Crie relacionamentos de slide** (`ppt/slides/_rels/slideN.xml.rels`) se necessário
6. **Atualize `docProps/app.xml`**: Incremente contagem de slides e atualize estatísticas (se presente)

### Duplicando um Slide

1. Copie o arquivo XML do slide de origem com um novo nome
2. Atualize todos os IDs no novo slide para serem exclusivos
3. Siga as etapas de "Adicionando um Novo Slide" acima
4. **CRÍTICO**: Remova ou atualize quaisquer referências a slides de notas em arquivos `_rels`
5. Remova referências a arquivos de mídia não utilizados

### Reordenando Slides

1. **Atualize `ppt/presentation.xml`**: Reordene elementos `<p:sldId>` em `<p:sldIdLst>`
2. A ordem dos elementos `<p:sldId>` determina a ordem dos slides
3. Mantenha IDs de slide e IDs de relacionamento inalterados

Exemplo:

```xml
<!-- Ordem original -->
<p:sldIdLst>
  <p:sldId id="256" r:id="rId2"/>
  <p:sldId id="257" r:id="rId3"/>
  <p:sldId id="258" r:id="rId4"/>
</p:sldIdLst>

<!-- Depois de mover slide 3 para a posição 2 -->
<p:sldIdLst>
  <p:sldId id="256" r:id="rId2"/>
  <p:sldId id="258" r:id="rId4"/>
  <p:sldId id="257" r:id="rId3"/>
</p:sldIdLst>
```

### Excluindo um Slide

1. **Remover de `ppt/presentation.xml`**: Exclua a entrada `<p:sldId>`
2. **Remover de `ppt/_rels/presentation.xml.rels`**: Exclua o relacionamento
3. **Remover de `[Content_Types].xml`**: Exclua a entrada Override
4. **Excluir arquivos**: Remova `ppt/slides/slideN.xml` e `ppt/slides/_rels/slideN.xml.rels`
5. **Atualizar `docProps/app.xml`**: Decremente contagem de slides e atualize estatísticas
6. **Limpar mídia não utilizada**: Remova imagens órfãs de `ppt/media/`

Nota: Não renumere slides restantes - mantenha seus IDs e nomes de arquivo originais.

## Erros Comuns a Evitar

- **Codificações**: Caracteres de escape unicode em conteúdo ASCII: `"` torna-se `&#8220;`
- **Imagens**: Adicione a `ppt/media/` e atualize arquivos de relacionamento
- **Listas**: Omita marcadores de cabeçalhos de lista
- **IDs**: Use valores hexadecimais válidos para UUIDs
- **Temas**: Verifique todos os temas no diretório `theme` para cores

## Lista de Verificação de Validação para Apresentações Baseadas em Modelo

### Antes de Empacotar, Sempre:

- **Limpe recursos não utilizados**: Remova mídia, fontes e diretórios de notas não referenciados
- **Corrija Content_Types.xml**: Declare TODOS os slides, layouts e temas presentes no pacote
- **Corrija IDs de relacionamento**:
  - Remova referências de incorporação de fonte se não estiver usando fontes incorporadas
- **Remova referências quebradas**: Verifique todos os arquivos `_rels` para referências a recursos excluídos

### Armadilhas Comuns de Duplicação de Modelo:

- Múltiplos slides referenciando o mesmo slide de notas após duplicação
- Referências de imagem/mídia de slides de modelo que não existem mais
- Referências de incorporação de fonte quando as fontes não estão incluídas
- Declarações slideLayout ausentes para layouts 12-25
- Diretório docProps pode não descompactar - isso é opcional
