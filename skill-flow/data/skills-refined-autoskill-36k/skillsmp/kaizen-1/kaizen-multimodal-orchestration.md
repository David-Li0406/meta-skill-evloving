# Multi-Modal Orchestration

MultiModalAgent, vision+audio+text unified processing.

## MultiModalAgent

```python
from kaizen.agents.multi_modal_agent import MultiModalAgent, MultiModalConfig
from kaizen.signatures.multi_modal import MultiModalSignature, ImageField

class DocumentOCRSignature(MultiModalSignature):
    image: ImageField = InputField(description="Document to extract")
    invoice_number: str = OutputField(description="Invoice number")
    total_amount: str = OutputField(description="Total amount")

config = MultiModalConfig(
    llm_provider="ollama",
    model="bakllava",
    prefer_local=True
)

agent = MultiModalAgent(config=config, signature=DocumentOCRSignature())
result = agent.analyze(image="/path/to/invoice.png")
```

## References
- **Examples**: `apps/kailash-kaizen/examples/8-multi-modal/document-understanding/`
