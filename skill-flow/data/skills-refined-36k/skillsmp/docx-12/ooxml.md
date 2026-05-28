# Referência Técnica Office Open XML

**Importante: Leia este documento inteiro antes de começar.** Este documento cobre:

- [Diretrizes Técnicas](#diretrizes-técnicas) - Regras de conformidade de esquema e requisitos de validação
- [Padrões de Conteúdo de Documento](#padrões-de-conteúdo-de-documento) - Padrões XML para cabeçalhos, listas, tabelas, formatação, etc.
- [Biblioteca de Documentos (Python)](#biblioteca-de-documentos-python) - Abordagem recomendada para manipulação OOXML com configuração automática de infraestrutura
- [Alterações Controladas (Redlining)](#alterações-controladas-redlining) - Padrões XML para implementar alterações controladas

## Diretrizes Técnicas

### Conformidade de Esquema

- **Ordenação de elementos em `<w:pPr>`**: `<w:pStyle>`, `<w:numPr>`, `<w:spacing>`, `<w:ind>`, `<w:jc>`
- **Espaço em branco**: Adicione `xml:space='preserve'` aos elementos `<w:t>` com espaços à esquerda/direita
- **Unicode**: Caracteres de escape no conteúdo ASCII: `"` torna-se `&#8220;`
  - **Referência de codificação de caracteres**: Aspas curvas `""` tornam-se `&#8220;&#8221;`, apóstrofo `'` torna-se `&#8217;`, travessão `—` torna-se `&#8212;`
- **Alterações controladas**: Use tags `<w:del>` e `<w:ins>` com `w:author="Claude"` fora dos elementos `<w:r>`
  - **Crítico**: `<w:ins>` fecha com `</w:ins>`, `<w:del>` fecha com `</w:del>` - nunca misture
  - **RSIDs devem ser hexadecimais de 8 dígitos**: Use valores como `00AB1234` (apenas caracteres 0-9, A-F)
  - **Colocação de trackRevisions**: Adicione `<w:trackRevisions/>` após `<w:proofState>` em settings.xml
- **Imagens**: Adicione a `word/media/`, referencie em `document.xml`, defina dimensões para evitar estouro

## Padrões de Conteúdo de Documento

### Estrutura Básica

```xml
<w:p>
  <w:r><w:t>Conteúdo de texto</w:t></w:r>
</w:p>
```

### Cabeçalhos e Estilos

```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="Title"/>
    <w:jc w:val="center"/>
  </w:pPr>
  <w:r><w:t>Título do Documento</w:t></w:r>
</w:p>

<w:p>
  <w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
  <w:r><w:t>Título da Seção</w:t></w:r>
</w:p>
```

### Formatação de Texto

```xml
<!-- Negrito -->
<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t>Negrito</w:t></w:r>
<!-- Itálico -->
<w:r><w:rPr><w:i/><w:iCs/></w:rPr><w:t>Itálico</w:t></w:r>
<!-- Sublinhado -->
<w:r><w:rPr><w:u w:val="single"/></w:rPr><w:t>Sublinhado</w:t></w:r>
<!-- Realçado -->
<w:r><w:rPr><w:highlight w:val="yellow"/></w:rPr><w:t>Realçado</w:t></w:r>
```

### Listas

```xml
<!-- Lista numerada -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>
    <w:spacing w:before="240"/>
  </w:pPr>
  <w:r><w:t>Primeiro item</w:t></w:r>
</w:p>

<!-- Reiniciar lista numerada em 1 - use numId diferente -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>
    <w:spacing w:before="240"/>
  </w:pPr>
  <w:r><w:t>Novo item de lista 1</w:t></w:r>
</w:p>

<!-- Lista com marcadores (nível 2) -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="1"/><w:numId w:val="1"/></w:numPr>
    <w:spacing w:before="240"/>
    <w:ind w:left="900"/>
  </w:pPr>
  <w:r><w:t>Item com marcador</w:t></w:r>
</w:p>
```

### Tabelas

```xml
<w:tbl>
  <w:tblPr>
    <w:tblStyle w:val="TableGrid"/>
    <w:tblW w:w="0" w:type="auto"/>
  </w:tblPr>
  <w:tblGrid>
    <w:gridCol w:w="4675"/><w:gridCol w:w="4675"/>
  </w:tblGrid>
  <w:tr>
    <w:tc>
      <w:tcPr><w:tcW w:w="4675" w:type="dxa"/></w:tcPr>
      <w:p><w:r><w:t>Célula 1</w:t></w:r></w:p>
    </w:tc>
    <w:tc>
      <w:tcPr><w:tcW w:w="4675" w:type="dxa"/></w:tcPr>
      <w:p><w:r><w:t>Célula 2</w:t></w:r></w:p>
    </w:tc>
  </w:tr>
</w:tbl>
```

### Layout

```xml
<!-- Quebra de página antes da nova seção (padrão comum) -->
<w:p>
  <w:r>
    <w:br w:type="page"/>
  </w:r>
</w:p>
<w:p>
  <w:pPr>
    <w:pStyle w:val="Heading1"/>
  </w:pPr>
  <w:r>
    <w:t>Título da Nova Seção</w:t>
  </w:r>
</w:p>

<!-- Parágrafo centralizado -->
<w:p>
  <w:pPr>
    <w:spacing w:before="240" w:after="0"/>
    <w:jc w:val="center"/>
  </w:pPr>
  <w:r><w:t>Texto centralizado</w:t></w:r>
</w:p>

<!-- Mudança de fonte - nível de parágrafo (aplica-se a todas as execuções) -->
<w:p>
  <w:pPr>
    <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/></w:rPr>
  </w:pPr>
  <w:r><w:t>Texto monoespaçado</w:t></w:r>
</w:p>

<!-- Mudança de fonte - nível de execução (específico para este texto) -->
<w:p>
  <w:r>
    <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/></w:rPr>
    <w:t>Este texto é Courier New</w:t>
  </w:r>
  <w:r><w:t> e este texto usa a fonte padrão</w:t></w:r>
</w:p>
```

## Atualizações de Arquivo

Ao adicionar conteúdo, atualize estes arquivos:

**`word/_rels/document.xml.rels`:**

```xml
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>
```

**`[Content_Types].xml`:**

```xml
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
```

### Imagens

**CRÍTICO**: Calcule dimensões para evitar estouro de página e manter a proporção.

```xml
<!-- Estrutura mínima necessária -->
<w:p>
  <w:r>
    <w:drawing>
      <wp:inline>
        <wp:extent cx="2743200" cy="1828800"/>
        <wp:docPr id="1" name="Picture 1"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="image1.png"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="rId5"/>
                <!-- Adicionar para preenchimento de estiramento com preservação de proporção -->
                <a:stretch>
                  <a:fillRect/>
                </a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:ext cx="2743200" cy="1828800"/>
                </a:xfrm>
                <a:prstGeom prst="rect"/>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
```

### Links (Hyperlinks)

**IMPORTANTE**: Todos os hyperlinks (internos e externos) exigem que o estilo Hyperlink seja definido em styles.xml. Sem esse estilo, os links parecerão texto normal em vez de links clicáveis sublinhados em azul.

**Links Externos:**

```xml
<!-- Em document.xml -->
<w:hyperlink r:id="rId5">
  <w:r>
    <w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>
    <w:t>Texto do Link</w:t>
  </w:r>
</w:hyperlink>

<!-- Em word/_rels/document.xml.rels -->
<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
              Target="https://www.example.com/" TargetMode="External"/>
```

**Links Internos:**

```xml
<!-- Link para marcador -->
<w:hyperlink w:anchor="myBookmark">
  <w:r>
    <w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>
    <w:t>Texto do Link</w:t>
  </w:r>
</w:hyperlink>

<!-- Destino do marcador -->
<w:bookmarkStart w:id="0" w:name="myBookmark"/>
<w:r><w:t>Conteúdo de destino</w:t></w:r>
<w:bookmarkEnd w:id="0"/>
```

**Estilo Hyperlink (necessário em styles.xml):**

```xml
<w:style w:type="character" w:styleId="Hyperlink">
  <w:name w:val="Hyperlink"/>
  <w:basedOn w:val="DefaultParagraphFont"/>
  <w:uiPriority w:val="99"/>
  <w:unhideWhenUsed/>
  <w:rPr>
    <w:color w:val="467886" w:themeColor="hyperlink"/>
    <w:u w:val="single"/>
  </w:rPr>
</w:style>
```

## Biblioteca de Documentos (Python)

Use a classe Document de `scripts/document.py` para todas as alterações controladas e comentários. Ela lida automaticamente com a configuração da infraestrutura (people.xml, RSIDs, settings.xml, arquivos de comentário, relacionamentos, tipos de conteúdo). Use apenas manipulação direta de XML para cenários complexos não suportados pela biblioteca.

**Trabalhando com Unicode e Entidades:**

- **Pesquisa**: Tanto a notação de entidade quanto os caracteres Unicode funcionam - `contains="&#8220;Company"` e `contains="\u201cCompany"` encontram o mesmo texto
- **Substituição**: Use entidades (`&#8220;`) ou Unicode (`\u201c`) - ambos funcionam e serão convertidos apropriadamente com base na codificação do arquivo (ascii → entidades, utf-8 → Unicode)

### Inicialização

**Encontre a raiz da habilidade docx** (diretório contendo `scripts/` e `ooxml/`):

```bash
# Procure document.py para localizar a raiz da habilidade
# Nota: /mnt/skills é usado aqui como exemplo; verifique seu contexto para a localização real
find /mnt/skills -name "document.py" -path "*/docx/scripts/*" 2>/dev/null | head -1
# Exemplo de saída: /mnt/skills/docx/scripts/document.py
# Raiz da habilidade é: /mnt/skills/docx
```

**Execute seu script com PYTHONPATH** definido para a raiz da habilidade docx:

```bash
PYTHONPATH=/mnt/skills/docx python your_script.py
```

**Em seu script**, importe da raiz da habilidade:

```python
from scripts.document import Document, DocxXMLEditor

# Inicialização básica (cria automaticamente cópia temporária e configura infraestrutura)
doc = Document('unpacked')

# Personalizar autor e iniciais
doc = Document('unpacked', author="John Doe", initials="JD")

# Habilitar modo de rastreamento de revisões
doc = Document('unpacked', track_revisions=True)

# Especificar RSID personalizado (gerado automaticamente se não fornecido)
doc = Document('unpacked', rsid="07DC5ECB")
```

### Criando Alterações Controladas

**CRÍTICO**: Marque apenas texto que realmente muda. Mantenha TODO o texto inalterado fora das tags `<w:del>`/`<w:ins>`. Marcar texto inalterado torna as edições não profissionais e mais difíceis de revisar.

**Tratamento de Atributos**: A classe Document injeta automaticamente atributos (w:id, w:date, w:rsidR, w:rsidDel, w16du:dateUtc, xml:space) em novos elementos. Ao preservar texto inalterado do documento original, copie o elemento `<w:r>` original com seus atributos existentes para manter a integridade do documento.

**Guia de Seleção de Método**:

- **Adicionando suas próprias alterações ao texto regular**: Use `replace_node()` com tags `<w:del>`/`<w:ins>`, ou `suggest_deletion()` para remover elementos inteiros `<w:r>` ou `<w:p>`
- **Modificando parcialmente a alteração controlada de outro autor**: Use `replace_node()` para aninhar suas alterações dentro de seu `<w:ins>`/`<w:del>`
- **Rejeitando completamente a inserção de outro autor**: Use `revert_insertion()` no elemento `<w:ins>` (NÃO `suggest_deletion()`)
- **Rejeitando completamente a exclusão de outro autor**: Use `revert_deletion()` no elemento `<w:del>` para restaurar conteúdo excluído usando alterações controladas

```python
# Edição mínima - mudar uma palavra: "The report is monthly" → "The report is quarterly"
# Original: <w:r w:rsidR="00AB12CD"><w:rPr><w:rFonts w:ascii="Calibri"/></w:rPr><w:t>The report is monthly</w:t></w:r>
node = doc["word/document.xml"].get_node(tag="w:r", contains="The report is monthly")
rpr = tags[0].toxml() if (tags := node.getElementsByTagName("w:rPr")) else ""
replacement = f'<w:r w:rsidR="00AB12CD">{rpr}<w:t>The report is </w:t></w:r><w:del><w:r>{rpr}<w:delText>monthly</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>quarterly</w:t></w:r></w:ins>'
doc["word/document.xml"].replace_node(node, replacement)

# Edição mínima - mudar número: "within 30 days" → "within 45 days"
# Original: <w:r w:rsidR="00XYZ789"><w:rPr><w:rFonts w:ascii="Calibri"/></w:rPr><w:t>within 30 days</w:t></w:r>
node = doc["word/document.xml"].get_node(tag="w:r", contains="within 30 days")
rpr = tags[0].toxml() if (tags := node.getElementsByTagName("w:rPr")) else ""
replacement = f'<w:r w:rsidR="00XYZ789">{rpr}<w:t>within </w:t></w:r><w:del><w:r>{rpr}<w:delText>30</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>45</w:t></w:r></w:ins><w:r w:rsidR="00XYZ789">{rpr}<w:t> days</w:t></w:r>'
doc["word/document.xml"].replace_node(node, replacement)

# Substituição completa - preservar formatação mesmo ao substituir todo o texto
node = doc["word/document.xml"].get_node(tag="w:r", contains="apple")
rpr = tags[0].toxml() if (tags := node.getElementsByTagName("w:rPr")) else ""
replacement = f'<w:del><w:r>{rpr}<w:delText>apple</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>banana orange</w:t></w:r></w:ins>'
doc["word/document.xml"].replace_node(node, replacement)

# Inserir novo conteúdo (sem atributos necessários - injetado automaticamente)
node = doc["word/document.xml"].get_node(tag="w:r", contains="existing text")
doc["word/document.xml"].insert_after(node, '<w:ins><w:r><w:t>new text</w:t></w:r></w:ins>')

# Excluir parcialmente inserção de outro autor
# Original: <w:ins w:author="Jane Smith" w:date="..."><w:r><w:t>quarterly financial report</w:t></w:r></w:ins>
# Goal: Delete only "financial" to make it "quarterly report"
node = doc["word/document.xml"].get_node(tag="w:ins", attrs={"w:id": "5"})
# IMPORTANTE: Preservar w:author="Jane Smith" no <w:ins> externo para manter autoria
replacement = '''<w:ins w:author="Jane Smith" w:date="2025-01-15T10:00:00Z">
  <w:r><w:t>quarterly </w:t></w:r>
  <w:del><w:r><w:delText>financial </w:delText></w:r></w:del>
  <w:r><w:t>report</w:t></w:r>
</w:ins>'''
doc["word/document.xml"].replace_node(node, replacement)

# Mudar parte da inserção de outro autor
# Original: <w:ins w:author="Jane Smith"><w:r><w:t>in silence, safe and sound</w:t></w:r></w:ins>
# Goal: Change "safe and sound" to "soft and unbound"
node = doc["word/document.xml"].get_node(tag="w:ins", attrs={"w:id": "8"})
replacement = f'''<w:ins w:author="Jane Smith" w:date="2025-01-15T10:00:00Z">
  <w:r><w:t>in silence, </w:t></w:r>
</w:ins>
<w:ins>
  <w:r><w:t>soft and unbound</w:t></w:r>
</w:ins>
<w:ins w:author="Jane Smith" w:date="2025-01-15T10:00:00Z">
  <w:del><w:r><w:delText>safe and sound</w:delText></w:r></w:del>
</w:ins>'''
doc["word/document.xml"].replace_node(node, replacement)

# Excluir execução inteira (use apenas ao excluir todo o conteúdo; use replace_node para exclusões parciais)
node = doc["word/document.xml"].get_node(tag="w:r", contains="text to delete")
doc["word/document.xml"].suggest_deletion(node)

# Excluir parágrafo inteiro (in-place, lida com parágrafos regulares e de lista numerada)
para = doc["word/document.xml"].get_node(tag="w:p", contains="paragraph to delete")
doc["word/document.xml"].suggest_deletion(para)

# Adicionar novo item de lista numerada
target_para = doc["word/document.xml"].get_node(tag="w:p", contains="existing list item")
pPr = tags[0].toxml() if (tags := target_para.getElementsByTagName("w:pPr")) else ""
new_item = f'<w:p>{pPr}<w:r><w:t>New item</w:t></w:r></w:p>'
tracked_para = DocxXMLEditor.suggest_paragraph(new_item)
doc["word/document.xml"].insert_after(target_para, tracked_para)
# Opcional: adicione parágrafo de espaçamento antes do conteúdo para melhor separação visual
# spacing = DocxXMLEditor.suggest_paragraph('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/></w:pPr></w:p>')
# doc["word/document.xml"].insert_after(target_para, spacing + tracked_para)
```

### Adicionando Comentários

```python
# Adicionar comentário abrangendo duas alterações controladas existentes
# Nota: w:id é gerado automaticamente. Pesquise por w:id apenas se você souber da inspeção XML
start_node = doc["word/document.xml"].get_node(tag="w:del", attrs={"w:id": "1"})
end_node = doc["word/document.xml"].get_node(tag="w:ins", attrs={"w:id": "2"})
doc.add_comment(start=start_node, end=end_node, text="Explicação desta alteração")

# Adicionar comentário em um parágrafo
para = doc["word/document.xml"].get_node(tag="w:p", contains="texto do parágrafo")
doc.add_comment(start=para, end=para, text="Comentário neste parágrafo")

# Adicionar comentário em alteração controlada recém-criada
# Primeiro crie a alteração controlada
node = doc["word/document.xml"].get_node(tag="w:r", contains="old")
new_nodes = doc["word/document.xml"].replace_node(
    node,
    '<w:del><w:r><w:delText>old</w:delText></w:r></w:del><w:ins><w:r><w:t>new</w:t></w:r></w:ins>'
)
# Em seguida, adicione comentário nos elementos recém-criados
# new_nodes[0] é o <w:del>, new_nodes[1] é o <w:ins>
doc.add_comment(start=new_nodes[0], end=new_nodes[1], text="Alterado old para new por requisitos")

# Responder a comentário existente
doc.reply_to_comment(parent_comment_id=0, text="Concordo com esta alteração")
```

### Rejeitando Alterações Controladas

**IMPORTANTE**: Use `revert_insertion()` para rejeitar inserções e `revert_deletion()` para restaurar exclusões usando alterações controladas. Use `suggest_deletion()` apenas para conteúdo regular não marcado.

```python
# Rejeitar inserção (envolve em exclusão)
# Use isso quando outro autor inseriu texto que você deseja excluir
ins = doc["word/document.xml"].get_node(tag="w:ins", attrs={"w:id": "5"})
nodes = doc["word/document.xml"].revert_insertion(ins)  # Retorna [ins]

# Rejeitar exclusão (cria inserção para restaurar conteúdo excluído)
# Use isso quando outro autor excluiu texto que você deseja restaurar
del_elem = doc["word/document.xml"].get_node(tag="w:del", attrs={"w:id": "3"})
nodes = doc["word/document.xml"].revert_deletion(del_elem)  # Retorna [del_elem, new_ins]

# Rejeitar todas as inserções em um parágrafo
para = doc["word/document.xml"].get_node(tag="w:p", contains="texto do parágrafo")
nodes = doc["word/document.xml"].revert_insertion(para)  # Retorna [para]

# Rejeitar todas as exclusões em um parágrafo
para = doc["word/document.xml"].get_node(tag="w:p", contains="texto do parágrafo")
nodes = doc["word/document.xml"].revert_deletion(para)  # Retorna [para]
```

### Inserindo Imagens

**CRÍTICO**: A classe Document trabalha com uma cópia temporária em `doc.unpacked_path`. Sempre copie imagens para este diretório temporário, não a pasta descompactada original.

```python
from PIL import Image
import shutil, os

# Inicializar documento primeiro
doc = Document('unpacked')

# Copiar imagem e calcular dimensões de largura total com proporção
media_dir = os.path.join(doc.unpacked_path, 'word/media')
os.makedirs(media_dir, exist_ok=True)
shutil.copy('image.png', os.path.join(media_dir, 'image1.png'))
img = Image.open(os.path.join(media_dir, 'image1.png'))
width_emus = int(6.5 * 914400)  # 6.5" largura utilizável, 914400 EMUs/polegada
height_emus = int(width_emus * img.size[1] / img.size[0])

# Adicionar relacionamento e tipo de conteúdo
rels_editor = doc['word/_rels/document.xml.rels']
next_rid = rels_editor.get_next_rid()
rels_editor.append_to(rels_editor.dom.documentElement,
    f'<Relationship Id="{next_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>')
doc['[Content_Types].xml'].append_to(doc['[Content_Types].xml'].dom.documentElement,
    '<Default Extension="png" ContentType="image/png"/>')

# Inserir imagem
node = doc["word/document.xml"].get_node(tag="w:p", line_number=100)
doc["word/document.xml"].insert_after(node, f'''<w:p>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{width_emus}" cy="{height_emus}"/>
        <wp:docPr id="1" name="Picture 1"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr><pic:cNvPr id="1" name="image1.png"/><pic:cNvPicPr/></pic:nvPicPr>
              <pic:blipFill><a:blip r:embed="{next_rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
              <pic:spPr><a:xfrm><a:ext cx="{width_emus}" cy="{height_emus}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>''')
```

### Obtendo Nós

```python
# Por conteúdo de texto
node = doc["word/document.xml"].get_node(tag="w:p", contains="texto específico")

# Por intervalo de linha
para = doc["word/document.xml"].get_node(tag="w:p", line_number=range(100, 150))

# Por atributos
node = doc["word/document.xml"].get_node(tag="w:del", attrs={"w:id": "1"})

# Por número de linha exato (deve ser o número da linha onde a tag abre)
para = doc["word/document.xml"].get_node(tag="w:p", line_number=42)

# Combinar filtros
node = doc["word/document.xml"].get_node(tag="w:r", line_number=range(40, 60), contains="texto")

# Desambiguar quando o texto aparece várias vezes - adicione intervalo line_number
node = doc["word/document.xml"].get_node(tag="w:r", contains="Section", line_number=range(2400, 2500))
```

### Salvando

```python
# Salvar com validação automática (copia de volta para o diretório original)
doc.save()  # Valida por padrão, gera erro se a validação falhar

# Salvar em local diferente
doc.save('modified-unpacked')

# Pular validação (depuração apenas - precisar disso em produção indica problemas XML)
doc.save(validate=False)
```

### Manipulação Direta DOM

Para cenários complexos não cobertos pela biblioteca:

```python
# Acessar qualquer arquivo XML
editor = doc["word/document.xml"]
editor = doc["word/comments.xml"]

# Acesso direto DOM (defusedxml.minidom.Document)
node = doc["word/document.xml"].get_node(tag="w:p", line_number=5)
parent = node.parentNode
parent.removeChild(node)
parent.appendChild(node)  # Mover para o fim

# Manipulação geral de documentos (sem alterações controladas)
old_node = doc["word/document.xml"].get_node(tag="w:p", contains="texto original")
doc["word/document.xml"].replace_node(old_node, "<w:p><w:r><w:t>texto de substituição</w:t></w:r></w:p>")

# Múltiplas inserções - use valor de retorno para manter a ordem
node = doc["word/document.xml"].get_node(tag="w:r", line_number=100)
nodes = doc["word/document.xml"].insert_after(node, "<w:r><w:t>A</w:t></w:r>")
nodes = doc["word/document.xml"].insert_after(nodes[-1], "<w:r><w:t>B</w:t></w:r>")
nodes = doc["word/document.xml"].insert_after(nodes[-1], "<w:r><w:t>C</w:t></w:r>")
# Resultados em: original_node, A, B, C
```

## Alterações Controladas (Redlining)

**Use a classe Document acima para todas as alterações controladas.** Os padrões abaixo são para referência ao construir strings XML de substituição.

### Regras de Validação

O validador verifica se o texto do documento corresponde ao original após reverter as alterações do Claude. Isso significa:

- **NUNCA modifique texto dentro das tags `<w:ins>` ou `<w:del>` de outro autor**
- **SEMPRE use exclusões aninhadas** para remover inserções de outro autor
- **Toda edição deve ser devidamente rastreada** com tags `<w:ins>` ou `<w:del>`

### Padrões de Alteração Controlada

**REGRAS CRÍTICAS**:

1. Nunca modifique o conteúdo dentro das alterações controladas de outro autor. Sempre use exclusões aninhadas.
2. **Estrutura XML**: Sempre coloque `<w:del>` e `<w:ins>` no nível de parágrafo contendo elementos `<w:r>` completos. Nunca aninhe dentro de elementos `<w:r>` - isso cria XML inválido que quebra o processamento do documento.

**Inserção de Texto:**

```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-07-30T23:05:00Z" w16du:dateUtc="2025-07-31T06:05:00Z">
  <w:r w:rsidR="00792858">
    <w:t>inserted text</w:t>
  </w:r>
</w:ins>
```

**Exclusão de Texto:**

```xml
<w:del w:id="2" w:author="Claude" w:date="2025-07-30T23:05:00Z" w16du:dateUtc="2025-07-31T06:05:00Z">
  <w:r w:rsidDel="00792858">
    <w:delText>deleted text</w:delText>
  </w:r>
</w:del>
```

**Excluindo Inserção de Outro Autor (DEVE usar estrutura aninhada):**

```xml
<!-- Aninhar exclusão dentro da inserção original -->
<w:ins w:author="Jane Smith" w:id="16">
  <w:del w:author="Claude" w:id="40">
    <w:r><w:delText>monthly</w:delText></w:r>
  </w:del>
</w:ins>
<w:ins w:author="Claude" w:id="41">
  <w:r><w:t>weekly</w:t></w:r>
</w:ins>
```

**Restaurando Exclusão de Outro Autor:**

```xml
<!-- Deixe a exclusão deles inalterada, adicione nova inserção após ela -->
<w:del w:author="Jane Smith" w:id="50">
  <w:r><w:delText>within 30 days</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="51">
  <w:r><w:t>within 30 days</w:t></w:r>
</w:ins>
```
