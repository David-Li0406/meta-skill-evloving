# Llm Architect - Validations

## LLM Response Used Without Validation

### **Id**
llm-response-no-validation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - response\.content\[0\]\.text(?!.*try|except|validate|parse)
  - completion\.choices\[0\]\.message\.content(?!.*json\.loads|validate)
  - await.*complete\(.*\)(?!.*try|validate|schema)
### **Message**
LLM response used directly without validation. LLMs return unpredictable text.
### **Fix Action**
Wrap in try/except, validate against schema, or use structured output
### **Applies To**
  - *.py
  - *.ts
  - *.js

## JSON Parse on Raw LLM Output

### **Id**
json-parse-llm-output
### **Severity**
error
### **Type**
regex
### **Pattern**
  - json\.loads\(.*response.*content
  - JSON\.parse\(.*response.*content
  - json\.loads\(.*completion
### **Message**
Parsing JSON directly from LLM output. LLMs often add markdown or malformed JSON.
### **Fix Action**
Use tool use/function calling for structured output, or implement JSON repair
### **Applies To**
  - *.py
  - *.ts
  - *.js

## No Token Count Before LLM Call

### **Id**
missing-token-count-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - messages\.create\((?!.*count_tokens|token.*limit|truncate)
  - chat\.completions\.create\((?!.*tiktoken|count|max_context)
### **Message**
LLM call without token count check. Input may silently truncate.
### **Fix Action**
Count tokens before sending, ensure input fits in context window
### **Applies To**
  - *.py
  - *.ts

## Vector Search Without Relevance Threshold

### **Id**
vector-search-no-threshold
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.search\(.*limit.*\)(?!.*threshold|score|filter)
  - similarity_search\(.*k=(?!.*score_threshold)
### **Message**
Vector search without relevance threshold. Low-quality results may cause hallucinations.
### **Fix Action**
Add minimum score threshold to filter irrelevant results
### **Applies To**
  - *.py
  - *.ts
  - *.js

## RAG Without Reranking

### **Id**
missing-reranking-stage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - search\(.*\)[\s\S]{0,100}messages\.create(?!.*rerank|cross.?encoder)
  - retrieve.*\n.*llm(?!.*rerank)
### **Message**
RAG pipeline without reranking stage. First-stage retrieval has low precision.
### **Fix Action**
Add cross-encoder reranking before passing results to LLM
### **Applies To**
  - *.py
  - **/rag/*.py

## Prompts Hardcoded Inline

### **Id**
prompts-hardcoded-inline
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - system.*=.*"You are(?!.*PROMPT|prompt|template)
  - system.*=.*'You are(?!.*PROMPT|prompt|template)
  - messages\.create\([\s\S]*?content.*=.*"(?!{)[\w\s]{50,}
### **Message**
System prompt hardcoded inline. Prompts should be versioned like code.
### **Fix Action**
Store prompts in separate files or constants, version control them
### **Applies To**
  - *.py
  - *.ts

## Agent Loop Without Iteration Limit

### **Id**
agent-no-max-iterations
### **Severity**
error
### **Type**
regex
### **Pattern**
  - while True[\s\S]*?await.*(?:complete|tool|agent)
  - while.*not.*done[\s\S]*?await.*complete(?!.*max_iter|counter|limit)
### **Message**
Agent loop without max iterations. Can loop infinitely consuming tokens.
### **Fix Action**
Add max_iterations counter and break condition
### **Applies To**
  - *.py
  - *.ts
  - **/agents/*.py

## LLM Calls Without Rate Limit Handling

### **Id**
no-rate-limit-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await.*messages\.create(?![\s\S]{0,200}(?:retry|RateLimit|429|tenacity))
  - await.*completions\.create(?![\s\S]{0,200}(?:retry|RateLimit|429))
### **Message**
LLM API calls without rate limit handling. Production will fail under load.
### **Fix Action**
Add retry with exponential backoff for rate limit errors
### **Applies To**
  - *.py
  - *.ts

## Parsing JSON from Streamed Response

### **Id**
streaming-json-parse
### **Severity**
error
### **Type**
regex
### **Pattern**
  - stream.*=.*True[\s\S]{0,500}json\.loads
  - stream.*:.*true[\s\S]{0,500}JSON\.parse
### **Message**
Parsing JSON from streamed response. Chunks don't respect JSON boundaries.
### **Fix Action**
Buffer complete response before parsing, or use streaming tool use
### **Applies To**
  - *.py
  - *.ts
  - *.js

## Retrieved Content Without Delimiter

### **Id**
context-no-delimiter
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - documents.*\+.*query(?!.*<|>|\[|\]|delimiter|DOCUMENT)
  - context.*=.*docs.*\+.*question(?!.*tag|mark|separate)
### **Message**
Retrieved content mixed with query without clear delimiters. Risk of prompt injection.
### **Fix Action**
Use XML tags or clear delimiters to separate untrusted content
### **Applies To**
  - *.py
  - *.ts

## Embedding Without Model Tracking

### **Id**
embedding-model-not-tracked
### **Severity**
info
### **Type**
regex
### **Pattern**
  - embed\(.*\)[\s\S]{0,100}(?:insert|upsert|store)(?!.*model)
  - embeddings\.create[\s\S]{0,100}vector_store(?!.*model.*version)
### **Message**
Storing embeddings without tracking model version. Model changes break search.
### **Fix Action**
Store embedding model name and version with each vector
### **Applies To**
  - *.py
  - *.ts

## Tool Definition Without Usage Examples

### **Id**
tool-schema-no-examples
### **Severity**
info
### **Type**
regex
### **Pattern**
  - tools.*=.*\[.*"input_schema"(?![\s\S]{0,500}(?:example|Example|EXAMPLE))
  - "name".*"description".*"input_schema"(?![\s\S]{0,300}example)
### **Message**
Tool definition without usage examples. LLM learns patterns from examples.
### **Fix Action**
Add concrete examples in tool description showing proper usage
### **Applies To**
  - *.py
  - *.ts
  - *.js

## Text Chunking Without Overlap

### **Id**
chunking-no-overlap
### **Severity**
info
### **Type**
regex
### **Pattern**
  - chunk_size.*=.*\d+(?![\s\S]{0,100}overlap)
  - RecursiveCharacterTextSplitter\((?!.*chunk_overlap)
  - split.*chunk.*(?!.*overlap)
### **Message**
Chunking without overlap. Context at chunk boundaries is lost.
### **Fix Action**
Add 10-20% chunk overlap to preserve context across boundaries
### **Applies To**
  - *.py
  - *.ts