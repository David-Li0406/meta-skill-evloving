# Cedar Policies for Amazon Bedrock AgentCore Gateway

This document covers Cedar policy language for implementing fine-grained authorization on AgentCore Gateway, enabling deterministic governance over tool invocations that cannot be bypassed by prompt injection.

## 1. Introduction to Cedar Policies

### What is Cedar?

Cedar is an open-source policy language developed by AWS for defining and enforcing fine-grained permissions. In AgentCore, Cedar policies control which tools an agent can invoke and under what conditions.

### Why Cedar for Agents?

| Challenge | Cedar Solution |
|-----------|----------------|
| LLM unpredictability | Deterministic policy evaluation |
| Prompt injection | External governance layer |
| Audit requirements | Policy-based access logging |
| Compliance | Declarative, reviewable rules |

### Default-Deny Model

Cedar operates on a **default-deny** principle:
- All actions are denied unless explicitly permitted
- `forbid` policies always override `permit` policies
- No implicit permissions - everything must be declared

---

## 2. Policy Syntax

### Basic Structure

Every Cedar policy has three mandatory components:

```cedar
permit|forbid (
  principal [is Type],           -- WHO
  action [== Action::"name"],    -- WHAT
  resource [== Resource::"arn"]  -- WHERE
) [when { conditions }]          -- CONDITIONS (optional)
  [unless { exceptions }];       -- EXCEPTIONS (optional)
```

### Simple Permit Example

```cedar
permit(
  principal,
  action == AgentCore::Action::"FlashcardTarget___generate_flashcards",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-2:377311924364:gateway/faiston-nexo"
);
```

This permits any authenticated principal to invoke the `generate_flashcards` tool on the specified gateway.

### Simple Forbid Example

```cedar
forbid(
  principal,
  action == AgentCore::Action::"AdminTarget___delete_user",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-2:377311924364:gateway/faiston-nexo"
);
```

This denies all principals from invoking `delete_user`, regardless of other permits.

---

## 3. Conditions with `when` and `unless`

### Using `when` Clauses

Add conditions that must be true for the policy to apply:

```cedar
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"RefundTarget___process_refund",
  resource == AgentCore::Gateway::"<gateway-arn>"
) when {
  context.input.amount < 1000
};
```

This permits refunds only when the amount is less than $1000.

### Using `unless` Clauses

Add exceptions - the policy applies unless the condition is true:

```cedar
forbid(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"AdminTarget___update_settings",
  resource == AgentCore::Gateway::"<gateway-arn>"
) unless {
  principal.hasTag("role") &&
  principal.getTag("role") == "admin"
};
```

This forbids updating settings unless the user has the "admin" role.

---

## 4. Context and Claims

### Accessing Tool Input Parameters

Use `context.input` to access the arguments passed to the tool:

```cedar
// Check if a field exists
context.input has amount

// Access field value
context.input.amount < 1000

// String comparison
context.input.category == "standard"

// List contains
["US", "CA", "MX"].contains(context.input.country)
```

### Accessing OAuth Claims

Use `principal.hasTag()` and `principal.getTag()` to access JWT claims:

```cedar
// Check if claim exists
principal.hasTag("role")

// Get claim value
principal.getTag("role") == "admin"

// Check scope (with wildcard)
principal.hasTag("scope") &&
principal.getTag("scope") like "*flashcards:write*"

// Username check
principal.hasTag("username") &&
principal.getTag("username") == "admin@faiston.com"
```

### Pattern Matching with `like`

Use wildcards for flexible string matching:

```cedar
// Prefix match
context.input.category like "premium*"

// Suffix match
context.input.email like "*@faiston.com"

// Contains
principal.getTag("scope") like "*admin*"

// Complex pattern
context.input.resource_id like "course-*-module-*"
```

---

## 5. Common Policy Patterns

### Pattern 1: Amount Limits

```cedar
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"PaymentTarget___process_payment",
  resource == AgentCore::Gateway::"<gateway-arn>"
) when {
  context.input has amount &&
  context.input.amount < 500
};
```

### Pattern 2: Role-Based Access Control

```cedar
// Only managers can approve
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"ApprovalTarget___approve_request",
  resource == AgentCore::Gateway::"<gateway-arn>"
) when {
  principal.hasTag("role") &&
  (principal.getTag("role") == "manager" ||
   principal.getTag("role") == "director")
};
```

### Pattern 3: Multi-Action Permit

```cedar
// Grant read access to multiple tools
permit(
  principal is AgentCore::OAuthUser,
  action in [
    AgentCore::Action::"CourseTarget___get_course",
    AgentCore::Action::"CourseTarget___list_modules",
    AgentCore::Action::"CourseTarget___get_transcription"
  ],
  resource == AgentCore::Gateway::"<gateway-arn>"
);
```

### Pattern 4: Required Field Enforcement

```cedar
// Forbid if required field is missing
forbid(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"FlashcardTarget___generate_flashcards",
  resource == AgentCore::Gateway::"<gateway-arn>"
) unless {
  context.input has transcription &&
  context.input has difficulty
};
```

### Pattern 5: Time-Based Restrictions (via Claims)

```cedar
// Only allow during business hours (enforced via token claim)
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"AdminTarget___batch_update",
  resource == AgentCore::Gateway::"<gateway-arn>"
) when {
  principal.hasTag("access_window") &&
  principal.getTag("access_window") == "business_hours"
};
```

### Pattern 6: Scope-Based Authorization

```cedar
// OAuth scope validation
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"AudioTarget___generate_audio",
  resource == AgentCore::Gateway::"<gateway-arn>"
) when {
  principal.hasTag("scope") &&
  principal.getTag("scope") like "*audio:generate*"
};
```

### Pattern 7: Block Specific User

```cedar
forbid(
  principal is AgentCore::OAuthUser,
  action,
  resource
) when {
  principal.hasTag("username") &&
  principal.getTag("username") == "suspended@faiston.com"
};
```

### Pattern 8: Disable Tool Temporarily

```cedar
// Disable a tool while keeping others operational
forbid(
  principal,
  action == AgentCore::Action::"MindMapTarget___generate_mindmap",
  resource == AgentCore::Gateway::"<gateway-arn>"
);
```

---

## 6. Gateway Integration

### Step 1: Create Policy Engine

```python
from bedrock_agentcore_starter_toolkit.operations.policy.client import PolicyClient

policy_client = PolicyClient(region_name="us-east-2")

# Create or get existing policy engine
engine = policy_client.create_or_get_policy_engine(
    name="FaistonNexoPolicyEngine",
    description="Governance policies for Faiston NEXO AI tools"
)

print(f"Policy Engine ID: {engine['policyEngineId']}")
print(f"Policy Engine ARN: {engine['policyEngineArn']}")
```

### Step 2: Create Cedar Policies

```python
# Define Cedar policy
flashcard_limit_policy = '''
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"FlashcardTarget___generate_flashcards",
  resource == AgentCore::Gateway::"{gateway_arn}"
) when {{
  context.input has num_cards &&
  context.input.num_cards <= 50
}};
'''.format(gateway_arn=gateway["gatewayArn"])

# Create policy
policy = policy_client.create_or_get_policy(
    policy_engine_id=engine["policyEngineId"],
    name="flashcard_limit_policy",
    description="Limit flashcard generation to 50 cards per request",
    definition={"cedar": {"statement": flashcard_limit_policy}}
)

print(f"Policy ID: {policy['policyId']}")
```

### Step 3: Attach Policy Engine to Gateway

```python
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient

gateway_client = GatewayClient(region_name="us-east-2")

# Attach with ENFORCE mode (blocks policy violations)
gateway_client.update_gateway_policy_engine(
    gateway_identifier=gateway["gatewayId"],
    policy_engine_arn=engine["policyEngineArn"],
    mode="ENFORCE"  # or "LOG_ONLY" for testing
)
```

### Enforcement Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `ENFORCE` | Blocks requests that violate policies | Production |
| `LOG_ONLY` | Logs decisions but doesn't block | Testing/Audit |

---

## 7. Testing Policies

### Test Script

```python
import json
import requests
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient

def test_tool_invocation(gateway_url: str, bearer_token: str, tool_name: str, arguments: dict) -> dict:
    """Test a tool invocation against Cedar policies."""

    response = requests.post(
        gateway_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}"
        },
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
    )

    result = response.json()
    print(f"Tool: {tool_name}")
    print(f"Arguments: {json.dumps(arguments, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(result, indent=2)}")
    print("-" * 50)

    return result


# Load configuration
with open("gateway_config.json", "r") as f:
    config = json.load(f)

gateway_url = config["gateway_url"]
gateway_client = GatewayClient(region_name=config["region"])
token = gateway_client.get_access_token_for_cognito(config["client_info"])

# Test 1: Should ALLOW - 10 flashcards (under limit)
test_tool_invocation(
    gateway_url,
    token,
    "FlashcardTarget___generate_flashcards",
    {"transcription": "Test content...", "num_cards": 10, "difficulty": "medium"}
)

# Test 2: Should DENY - 100 flashcards (over limit)
test_tool_invocation(
    gateway_url,
    token,
    "FlashcardTarget___generate_flashcards",
    {"transcription": "Test content...", "num_cards": 100, "difficulty": "medium"}
)

# Test 3: Should DENY - Missing required field
test_tool_invocation(
    gateway_url,
    token,
    "FlashcardTarget___generate_flashcards",
    {"transcription": "Test content..."}  # Missing num_cards and difficulty
)
```

### Expected Responses

**Allowed Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{"type": "text", "text": "{\"flashcards\": [...]}"}]
  }
}
```

**Denied Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Access denied by policy"
  }
}
```

---

## 8. Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| All requests denied | No permit policy for the action | Add explicit permit policy |
| Policy not applying | Wrong action name format | Use `TargetName___tool_name` format |
| Context.input empty | Tool schema missing | Define `inputSchema` in tool target |
| Claims not accessible | Wrong JWT configuration | Verify Cognito/IdP claim mapping |

### Debugging with LOG_ONLY Mode

```python
# Start in LOG_ONLY mode for debugging
gateway_client.update_gateway_policy_engine(
    gateway_identifier=gateway["gatewayId"],
    policy_engine_arn=engine["policyEngineArn"],
    mode="LOG_ONLY"
)

# Check CloudWatch Logs for policy decisions
# Log group: /aws/bedrock-agentcore/gateways/{gateway-id}
```

### CloudWatch Log Entry Example

```json
{
  "timestamp": "2025-12-10T10:30:00Z",
  "gatewayId": "faiston-nexo-gateway",
  "action": "FlashcardTarget___generate_flashcards",
  "principal": "user:admin@faiston.com",
  "decision": "DENY",
  "matchedPolicy": "flashcard_limit_policy",
  "reason": "context.input.num_cards (100) >= 50"
}
```

---

## 9. Faiston NEXO Policy Examples

### Complete Policy Set for Faiston NEXO

```cedar
// =============================================================================
// FAISTON NEXO CEDAR POLICIES
// =============================================================================

// -----------------------------------------------------------------------------
// FLASHCARDS: Limit cards per request, require transcription
// -----------------------------------------------------------------------------
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"FlashcardTarget___generate_flashcards",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-2:377311924364:gateway/faiston-nexo"
) when {
  context.input has transcription &&
  context.input has num_cards &&
  context.input.num_cards <= 50
};

// -----------------------------------------------------------------------------
// MIND MAP: Require transcription and episode title
// -----------------------------------------------------------------------------
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"MindMapTarget___generate_mindmap",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-2:377311924364:gateway/faiston-nexo"
) when {
  context.input has transcription &&
  context.input has episode_title
};

// -----------------------------------------------------------------------------
// NEXO CHAT: Allow all authenticated users
// -----------------------------------------------------------------------------
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"NEXOTarget___chat",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-2:377311924364:gateway/faiston-nexo"
);

// -----------------------------------------------------------------------------
// AUDIO CLASS: Limit to premium users (scope-based)
// -----------------------------------------------------------------------------
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"AudioTarget___generate_audio_class",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-2:377311924364:gateway/faiston-nexo"
) when {
  principal.hasTag("subscription") &&
  (principal.getTag("subscription") == "premium" ||
   principal.getTag("subscription") == "enterprise")
};

// -----------------------------------------------------------------------------
// REFLECTION: Allow with transcription context
// -----------------------------------------------------------------------------
permit(
  principal is AgentCore::OAuthUser,
  action == AgentCore::Action::"ReflectionTarget___analyze_reflection",
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-2:377311924364:gateway/faiston-nexo"
) when {
  context.input has transcription &&
  context.input has reflection
};

// -----------------------------------------------------------------------------
// ADMIN TOOLS: Only admin role
// -----------------------------------------------------------------------------
forbid(
  principal is AgentCore::OAuthUser,
  action in [
    AgentCore::Action::"AdminTarget___delete_user",
    AgentCore::Action::"AdminTarget___reset_data",
    AgentCore::Action::"AdminTarget___export_all"
  ],
  resource == AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-2:377311924364:gateway/faiston-nexo"
) unless {
  principal.hasTag("role") &&
  principal.getTag("role") == "admin"
};
```

---

## 10. References

- [Understanding Cedar Policies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-understanding-cedar.html)
- [Example Policies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/example-policies.html)
- [Common Policy Patterns](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-common-patterns.html)
- [Getting Started with AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-getting-started.html)
- [Cedar Policy Language Reference](https://docs.cedarpolicy.com/policies/syntax-policy.html)
- [AgentCore Policy Blog](https://aws.amazon.com/blogs/aws/amazon-bedrock-agentcore-adds-quality-evaluations-and-policy-controls-for-deploying-trusted-ai-agents/)
