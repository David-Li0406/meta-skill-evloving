# c4-diagrams assets

Cómo renderizar los ejemplos:

- Mermaid (mmdc):

  mmdc -i assets/mermaid-example.mmd -o /tmp/mermaid.png

- PlantUML (plantuml):

  plantuml -tpng assets/plantuml-example.puml

Recomendaciones:

- Instala mmdc (mermaid-cli) y plantuml localmente si vas a renderizar.
- Para PlantUML, utiliza la librería C4-PlantUML (`https://github.com/plantuml-stdlib/C4-PlantUML`).
