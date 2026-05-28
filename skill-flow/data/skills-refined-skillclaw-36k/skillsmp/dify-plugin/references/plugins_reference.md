# Dify Official Plugins Reference

Reference guide for officially maintained plugins. Use this when developing new plugins to review existing implementations.

---

## Plugin Types Overview

| Type | Directory Prefix | Purpose |
|------|------------------|---------|
| Models | `models/` | LLM, Embedding, TTS provider integrations |
| Tools | `tools/` | External API and service integrations |
| Extensions | `extensions/` | Platform feature extensions |
| Triggers | `triggers/` | External event workflow triggers |
| Datasources | `datasources/` | External data source integrations |
| Agent Strategies | `agent-strategies/` | Agent reasoning strategies |

---

## Models

| Name | Directory | Description |
|------|-----------|-------------|
| openai | `models/openai` | OpenAI GPT series |
| anthropic | `models/anthropic` | Claude series |
| azure_openai | `models/azure_openai` | Azure OpenAI Service |
| deepseek | `models/deepseek` | DeepSeek models |
| zhipuai | `models/zhipuai` | Zhipu AI |
| tongyi | `models/tongyi` | Alibaba Tongyi Qianwen |
| siliconflow | `models/siliconflow` | SiliconFlow |
| vertex_ai | `models/vertex_ai` | Google Vertex AI |
| volcengine_maas | `models/volcengine_maas` | ByteDance Volcano Engine |
| cohere | `models/cohere` | Cohere models |

---

## Tools

| Name | Directory | Description |
|------|-----------|-------------|
| feishu_base | `tools/feishu_base` | Feishu Bitable |
| feishu_calendar | `tools/feishu_calendar` | Feishu Calendar |
| feishu_message | `tools/feishu_message` | Feishu Messaging |
| feishu_document | `tools/feishu_document` | Feishu Docs |
| e2b | `tools/e2b` | Code sandbox execution |
| lark_spreadsheet | `tools/lark_spreadsheet` | Lark Spreadsheet |
| lark_task | `tools/lark_task` | Lark Tasks |
| lark_message_and_group | `tools/lark_message_and_group` | Lark Messaging & Groups |
| lark_document | `tools/lark_document` | Lark Docs |
| wikipedia | `tools/wikipedia` | Wikipedia search |

---

## Extensions

| Name | Directory | Description |
|------|-----------|-------------|
| slack_bot | `extensions/slack_bot` | Slack Bot integration |
| openai_compatible | `extensions/openai_compatible` | OpenAI-compatible API endpoint |
| oaicompat_dify_model | `extensions/oaicompat_dify_model` | Dify model OpenAI compatibility layer |
| mcp_server | `extensions/mcp_server` | MCP server integration |
| wecom_bot | `extensions/wecom_bot` | WeCom Bot |
| llamacloud | `extensions/llamacloud` | LlamaCloud integration |
| badapple | `extensions/badapple` | Bad Apple demo |
| aws_bedrock_knowledge_base | `extensions/aws_bedrock_knowledge_base` | AWS Bedrock Knowledge Base |

---

## Triggers

| Name | Directory | Description |
|------|-----------|-------------|
| github_trigger | `triggers/github_trigger` | GitHub Webhook events |
| slack_trigger | `triggers/slack_trigger` | Slack events |
| lark_trigger | `triggers/lark_trigger` | Feishu/Lark events |
| linear_trigger | `triggers/linear_trigger` | Linear events |
| telegram_trigger | `triggers/telegram_trigger` | Telegram Bot messages |
| notion_trigger | `triggers/notion_trigger` | Notion change events |
| woocommerce_trigger | `triggers/woocommerce_trigger` | WooCommerce order events |
| zendesk_trigger | `triggers/zendesk_trigger` | Zendesk ticket events |
| gmail_trigger | `triggers/gmail_trigger` | Gmail events |
| outlook_trigger | `triggers/outlook_trigger` | Outlook email events |

---

## Datasources

| Name | Directory | Description | Provider Type | Auth Method |
|------|-----------|-------------|---------------|-------------|
| aws_s3_storage | `datasources/aws_s3_storage` | AWS S3 Storage - Access buckets and objects | `online_drive` | Access Key + Secret |
| azure_blob | `datasources/azure_blob` | Azure Blob Storage - Access containers and blobs with multiple auth methods | `online_drive` | Access Key / SAS Token / Connection String |
| github | `datasources/github` | GitHub Repository - Access repos, issues, PRs, and wiki pages | `online_document` | Personal Access Token / OAuth |
| google_drive | `datasources/google_drive` | Google Drive - Access files and folders | `online_drive` | OAuth |
| notion_datasource | `datasources/notion_datasource` | Notion - Access pages and databases | `online_document` | OAuth / Internal Integration Token |
| confluence_datasource | `datasources/confluence_datasource` | Confluence - Access spaces and pages | `online_document` | API Token / OAuth |
| dropbox_datasource | `datasources/dropbox_datasource` | Dropbox - Access files and folders | `online_drive` | OAuth / Access Token |
| firecrawl_datasource | `datasources/firecrawl_datasource` | Firecrawl - Web crawling and content extraction | `website_crawl` | API Key |
| jina_datasource | `datasources/jina_datasource` | Jina Reader - Web content extraction and parsing | `website_crawl` | API Key |
| onedrive | `datasources/onedrive` | OneDrive - Access files and folders | `online_drive` | OAuth |

## Agent Strategies

| Name | Directory | Description |
|------|-----------|-------------|
| cot_agent | `agent-strategies/cot_agent` | Chain-of-Thought reasoning strategy |

### Agent Strategy Implementation Example

#### cot_agent (`agent-strategies/cot_agent`)
**Strategies:**
- `function_calling` - Uses model's native function calling capability
- `ReAct` - Thought-Action-Observation reasoning pattern

**Key Files:**
- `manifest.yaml` - Plugin metadata with `plugins.agent_strategies`
- `provider/agent.yaml` - Provider config listing strategies
- `strategies/function_calling.yaml` - Strategy parameters definition
- `strategies/function_calling.py` - Strategy implementation

**Strategy Parameters:**
```yaml
parameters:
  - name: model
    type: model-selector
    scope: tool-call&llm
    required: true
  - name: tools
    type: array[tools]
    required: true
  - name: instruction
    type: string
    required: true
  - name: query
    type: string
    required: true
  - name: maximum_iterations
    type: number
    default: 3
    min: 1
    max: 30
```

**Key Implementation Pattern:**
```python
from dify_plugin.interfaces.agent import AgentStrategy

class FunctionCallingStrategy(AgentStrategy):
    def _invoke(self, parameters: dict) -> Generator[AgentInvokeMessage, None, None]:
        model = parameters.get("model")
        tools = self._init_prompt_tools(parameters.get("tools", []))

        for iteration in range(parameters.get("maximum_iterations", 3)):
            # Call LLM with tools
            result = self.session.model.llm.invoke(
                model_config=model,
                prompt_messages=messages,
                tools=tools
            )

            # Execute tool calls if any
            if result.message.tool_calls:
                for tool_call in result.message.tool_calls:
                    tool_result = self.session.tool.invoke(...)
            else:
                yield self.create_text_message(result.message.content)
                break
```

---
