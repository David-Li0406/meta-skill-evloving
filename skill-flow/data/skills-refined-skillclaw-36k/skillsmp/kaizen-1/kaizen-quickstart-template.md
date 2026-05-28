# Kaizen Quickstart Template

Complete agent template from kaizen-specialist for rapid development.

## Complete Template (Copy-Paste Ready)

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature, InputField, OutputField
from dataclasses import dataclass
from dotenv import load_dotenv

# Load API keys
load_dotenv()

# 1. Define signature
class MySignature(Signature):
    input_field: str = InputField(description="Input description")
    output_field: str = OutputField(description="Output description")

# 2. Create domain config
@dataclass
class MyConfig:
    llm_provider: str = "openai"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000

# 3. Extend BaseAgent
class MyAgent(BaseAgent):
    def __init__(self, config: MyConfig):
        super().__init__(config=config, signature=MySignature())

    def process(self, input_data: str) -> dict:
        result = self.run(input_field=input_data)
        output = self.extract_str(result, "output_field", default="")
        self.write_to_memory(
            content={"input": input_data, "output": output},
            tags=["processing"]
        )
        return result

# 4. Execute
if __name__ == "__main__":
    agent = MyAgent(config=MyConfig())
    result = agent.process("input")
    print(result)
```

## References
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 489-520
