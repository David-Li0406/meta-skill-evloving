---
name: "Agent Configuration Architect"
description: "Especialista en configuración de agentes de IA: templates, tools, models, prompts y seed data."
trigger: "agents, agentes, AI, tools, templates, models, prompts, system prompt, wizard"
scope: "AGENTS"
auto-invoke: true
---

# Agent Configuration Architect - Platform AI Solutions

## 1. Concepto: La Fábrica de Agentes

### Filosofía
Nexus **NO tiene un solo bot**. Tiene una **Fuerza Laboral Digital** donde cada agente tiene:
- **Identidad**: Rol específico (Sales, Support, Leads, Fitter)
- **Inteligencia**: Modelo LLM (GPT-5-mini, Gemini 3 Pro)
- **Capacidades**: Tools habilitadas (search_products, rag_search)
- **Personalidad**: System prompt customizado

### Arquitectura Polymorphic
```
Agent Configuration (DB)
    ↓
agent_service → Runtime Assembly
    ↓
LLM Provider (OpenAI/Google) + Tools + RAG
    ↓
Response Generation
```

## 2. Modelos de Datos

### Tabla agents (PostgreSQL)
```sql
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    name TEXT NOT NULL,
    role TEXT DEFAULT 'sales',  -- sales, support, leads, fitter
    model_provider TEXT DEFAULT 'openai',  -- openai, google
    model_version TEXT DEFAULT 'gpt-5-mini',
    temperature FLOAT DEFAULT 0.7,
    system_prompt_template TEXT NOT NULL,
    enabled_tools JSONB DEFAULT '[]',
    channels JSONB DEFAULT '["whatsapp", "instagram", "facebook", "web"]',
    config JSONB DEFAULT '{}',
    template_type VARCHAR(50) DEFAULT 'custom',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Agent Config (JSONB Column)
```json
{
  "reasoning_effort": "medium",  // none, low, medium, high
  "text_verbosity": "concise",  // concise, detailed, bullet_points
  "agent_tone": "Sos una asesora cálida y profesional...",
  "store_website": "https://tienda.com",
  "synonym_dictionary": {
    "mallas": "leotardos",
    "can can": "medias"
  },
  "business_rules": [
    "No dar descuentos sin autorización",
    "Derivar a humano si pregunta por fitting personalizado"
  ]
}
```

## 3. Templates de Agentes

### Sales Agent (Pointe Coach Legacy)
```python
# agent_service/app/core/agent_templates.py

class SalesAgentTemplate(BaseAgentTemplate):
    def get_system_role(self) -> str:
        return "Asistente de ventas experto"
    
    def get_core_instructions(self) -> str:
        return """
Sos una vendedora especializada en danza clásica y ballet.
Usá voseo argentino. Sé cálida y profesional.

REGLAS DE ORO:
1. NUNCA inventar productos que no estén en el catálogo
2. Si no tenés respuesta, ser honesta
3. Derivar a humano si la consulta es muy técnica
"""
    
    def get_default_tools(self) -> List[str]:
        return ["search_products", "check_stock", "rag_search"]
    
    def get_default_temperature(self) -> float:
        return 0.7
```

### Support Agent
```python
class SupportAgentTemplate(BaseAgentTemplate):
    def get_system_role(self) -> str:
        return "Asistente de soporte técnico"
    
    def get_core_instructions(self) -> str:
        return """
Tu objetivo es resolver problemas post-venta:
- Seguimiento de órdenes
- Cambios y devoluciones
- Garantías

Temperatura más baja para respuestas precisas.
"""
    
    def get_default_tools(self) -> List[str]:
        return ["track_order", "check_return_policy", "rag_search"]
    
    def get_default_temperature(self) -> float:
        return 0.5  # Más preciso, menos creativo
```

### Leads Agent (Qualifier)
```python
class LeadsAgentTemplate(BaseAgentTemplate):
    def get_system_role(self) -> str:
        return "Calificador de leads"
    
    def get_core_instructions(self) -> str:
        return """
Tu objetivo es cualificar leads y capturar información:
- Nombre
- Email
- Necesidad específica
- Timeline de compra

NO vender directamente, solo cualificar.
"""
    
    def get_default_tools(self) -> List[str]:
        return ["create_lead", "send_email"]
```

## 4. Crear Agente (Frontend → Backend)

### Frontend: DynamicAgentWizard
```tsx
interface AgentFormData {
  name: string;
  role: string;
  model_provider: 'openai' | 'google';
  model_version: string;
  temperature: number;
  enabled_tools: string[];
  channels: string[];
  config: {
    agent_tone?: string;
    synonym_dictionary?: Record<string, string>;
    business_rules?: string[];
  };
}

const createAgent = async (formData: AgentFormData) => {
  const response = await useApi<Agent>({
    method: 'POST',
    url: '/admin/agents',
    data: formData
  });
  
  return response;
};
```

### Backend: Agent Creation
```python
# orchestrator_service/app/api/v1/endpoints/agents.py

@router.post("/agents", status_code=201)
async def create_agent(
    payload: AgentCreate,
    current_user = Depends(verify_admin_token),
    session: AsyncSession = Depends(get_session)
):
    # Resolver tenant
    tenant_id = await resolve_tenant(current_user.id)
    
    # Validar credenciales del provider existen
    provider_key = await get_tenant_credential(
        tenant_id=tenant_id,
        category=payload.model_provider  # 'openai' o 'google'
    )
    
    if not provider_key:
        raise HTTPException(
            status_code=400,
            detail=f"{payload.model_provider.upper()} API key not configured"
        )
    
    # Crear agente
    agent = Agent(
        tenant_id=tenant_id,
        name=payload.name,
        role=payload.role,
        model_provider=payload.model_provider,
        model_version=payload.model_version,
        temperature=payload.temperature,
        system_prompt_template=payload.system_prompt_template,
        enabled_tools=payload.enabled_tools,
        channels=payload.channels,
        config=payload.config,
        template_type=payload.template_type or 'custom'
    )
    
    session.add(agent)
    await session.commit()
    await session.refresh(agent)
    
    return agent
```

## 5. Tools Registry

### Cargar Tools Disponibles
```typescript
// Frontend
const loadAvailableTools = async () => {
  const tools = await useApi<Tool[]>({
    method: 'GET',
    url: '/admin/tools'
  });
  
  return tools;
};

// Tool interface
interface Tool {
  name: string;
  description: string;
  type: 'http' | 'internal';
  parameters?: Record<string, any>;
}
```

### Backend: Tools Endpoint
```python
@router.get("/tools")
async def get_available_tools():
    """
    Retorna herramientas del sistema disponibles
    """
    # Herramientas internas (agent_service)
    system_tools = [
        {
            "name": "search_products",
            "description": "Busca productos en Tienda Nube",
            "type": "internal"
        },
        {
            "name": "check_stock",
            "description": "Verifica disponibilidad de stock",
            "type": "internal"
        },
        {
            "name": "rag_search",
            "description": "Busca en base de conocimiento (PDFs)",
            "type": "internal"
        },
        {
            "name": "create_lead",
            "description": "Crea lead en CRM",
            "type": "http"
        }
    ]
    
    return system_tools
```

### Crear Nueva Tool (Agent Service)
```python
# agent_service/main.py

from langchain.tools import tool

@tool
async def search_products(
    query: str,
    tenant_id: int,
    category: Optional[str] = None
) -> dict:
    """
    Busca productos en el catálogo de Tienda Nube.
    
    Args:
        query: Término de búsqueda
        tenant_id: ID del tenant (multi-tenant)
        category: Filtro opcional de categoría
    
    Returns:
        Lista de productos encontrados
    """
    # Obtener credenciales de Tienda Nube
    tn_token = await get_tenant_credential(
        tenant_id=tenant_id,
        category="tiendanube"
    )
    
    # Llamar API
    response = await httpx.get(
        f"https://api.tiendanube.com/v1/products/search",
        headers={"Authorization": f"Bearer {tn_token}"},
        params={"q": query, "category": category}
    )
    
    products = response.json()
    
    # Formatear para el agente
    return {
        "products": products,
        "count": len(products)
    }

# Registrar en all_tools
all_tools = [search_products, check_stock, rag_search, create_lead]
```

## 6. Model Selection

### Model Registry
```python
# orchestrator_service/app/core/models.py

MODEL_REGISTRY = {
    "openai": [
        {
            "id": "gpt-5-mini",
            "name": "GPT-5 Mini",
            "tier": "standard",
            "cost_per_1k": 0.0001
        },
        {
            "id": "gpt-5.2",
            "name": "GPT-5.2",
            "tier": "premium",
            "cost_per_1k": 0.001
        }
    ],
    "google": [
        {
            "id": "gemini-3-pro",
            "name": "Gemini 3 Pro",
            "tier": "premium",
            "multimodal": True
        },
        {
            "id": "gemini-3-flash",
            "name": "Gemini 3 Flash",
            "tier": "standard",
            "speed": "fast"
        }
    ]
}
```

### Frontend Model Selector
```tsx
const ModelSelector: React.FC = ({ onChange }) => {
  const [provider, setProvider] = useState<'openai' | 'google'>('openai');
  const [models, setModels] = useState<Model[]>([]);
  
  useEffect(() => {
    // Cargar modelos del provider seleccionado
    const providerModels = MODEL_REGISTRY[provider];
    setModels(providerModels);
  }, [provider]);
  
  return (
    <div>
      <select value={provider} onChange={(e) => setProvider(e.target.value)}>
        <option value="openai">OpenAI</option>
        <option value="google">Google</option>
      </select>
      
      <select onChange={(e) => onChange(e.target.value)}>
        {models.map(model => (
          <option key={model.id} value={model.id}>
            {model.name} ({model.tier})
          </option>
        ))}
      </select>
    </div>
  );
};
```

## 7. Hybrid Prompting (System Prompt Engineering)

### Arquitectura de 3 Capas
```
1. System Prompt Técnico (Core Rules)
   ↓ No editable por usuario
   
2. Personalidad (Agent Tone)
   ↓ Editable en Wizard
   
3. Variables Mágicas (Runtime Injection)
   ↓ {catalog}, {store_name}, {synonym_dictionary}
```

### Construcción Final del Prompt
```python
# agent_service/app/core/prompt_builder.py

def build_final_prompt(
    agent: Agent,
    catalog: List[Product],
    tenant_config: dict
) -> str:
    """
    Construye el prompt final inyectando variables
    """
    # Base técnica (no editable)
    core_rules = """
PROTOCOLO DE SEGURIDAD:
- NUNCA inventar información de productos
- NUNCA dar precios incorrectos
- Derivar a humano si no estás segura
"""
    
    # Personalidad (editable)
    agent_tone = agent.config.get('agent_tone', '')
    
    # Variables mágicas
    catalog_str = json.dumps([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        }
        for p in catalog
    ])
    
    synonym_dict = agent.config.get('synonym_dictionary', {})
    
    # Ensamblaje final
    final_prompt = f"""
{core_rules}

{agent_tone}

CATÁLOGO DISPONIBLE:
{catalog_str}

DICCIONARIO DE SINÓNIMOS:
{json.dumps(synonym_dict)}

TIENDA: {tenant_config['store_name']}
WEB: {agent.config.get('store_website', 'N/A')}
"""
    
    return final_prompt
```

## 8. Channel Management

### Channel Selector (Frontend)
```tsx
const CHANNELS = [
  { id: 'whatsapp', name: 'WhatsApp', icon: MessageCircle },
  { id: 'instagram', name: 'Instagram', icon: Instagram },
  { id: 'facebook', name: 'Facebook', icon: Facebook },
  { id: 'web', name: 'Web Widget', icon: Globe }
];

const ChannelSelector: React.FC = ({ selected, onChange }) => {
  const toggleChannel = (channelId: string) => {
    if (selected.includes(channelId)) {
      onChange(selected.filter(c => c !== channelId));
    } else {
      onChange([...selected, channelId]);
    }
  };
  
  return (
    <div className="grid grid-cols-2 gap-2">
      {CHANNELS.map(channel => (
        <label key={channel.id} className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={selected.includes(channel.id)}
            onChange={() => toggleChannel(channel.id)}
          />
          <channel.icon size={20} />
          <span>{channel.name}</span>
        </label>
      ))}
    </div>
  );
};
```

### Runtime Channel Filtering
```python
# orchestrator_service/app/api/v1/endpoints/chat_handler.py

async def route_incoming_message(message: IncomingMessage):
    """
    Enruta mensaje entrante al agente correcto
    """
    # Buscar agente activo para este tenant y canal
    stmt = select(Agent).where(
        Agent.tenant_id == message.tenant_id,
        Agent.is_active == True,
        Agent.channels.contains([message.channel])  # JSONB filter
    ).order_by(Agent.role)  # Prioridad: sales > support
    
    result = await session.execute(stmt)
    agent = result.scalar_one_or_none()
    
    if not agent:
        # No hay agente para este canal
        return {"error": "No agent configured for this channel"}
    
    # Enviar a agent_service
    return await process_with_agent(agent, message)
```

## 9. Seed Data (Pointe Coach Legacy)

### Pre-configuración al Crear Agente Sales
```python
SALES_AGENT_SEED = {
    "agent_tone": """
Sos una asesora experta en danza clásica y ballet.
Usá voseo argentino. Sé cálida y profesional.
Priorizá la experiencia del cliente sobre la venta.
""",
    "synonym_dictionary": {
        "mallas": "leotardos",
        "can can": "medias",
        "cancanes": "medias",
        "zapatillas de punta": "puntas",
        "zapatillas de media punta": "media punta"
    },
    "business_rules": [
        "Filtros de veracidad absoluta: NO inventar stock",
        "Derivar a humano si pregunta por fitting personalizado",
        "Nunca dar descuentos sin autorización"
    ]
}

# Al crear agente tipo 'sales'
if template_type == 'sales':
    agent.config = SALES_AGENT_SEED
```

## 10. Live Preview & Simulation

### Test Chat (Frontend)
```tsx
const TestChat: React.FC<{ agentId: number }> = ({ agentId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  
  const sendTest = async () => {
    // Simular conversación
    const response = await useApi({
      method: 'POST',
      url: `/admin/agents/${agentId}/simulate`,
      data: {
        message: input,
        context: {
          channel: 'test',
          user_id: 'test_user'
        }
      }
    });
    
    setMessages([
      ...messages,
      { sender: 'user', content: input },
      { sender: 'agent', content: response.message }
    ]);
    
    setInput('');
  };
  
  return (
    <div className="test-chat">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={msg.sender}>
            {msg.content}
          </div>
        ))}
      </div>
      
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendTest()}
      />
    </div>
  );
};
```

### Backend Simulation
```python
@router.post("/agents/{agent_id}/simulate")
async def simulate_agent(
    agent_id: int,
    payload: SimulateRequest,
    session: AsyncSession = Depends(get_session)
):
    # Obtener agente
    agent = await session.get(Agent, agent_id)
    
    # Llamar a agent_service en modo test
    response = await httpx.post(
        "http://agent_service:8004/chat",
        json={
            "agent_config": agent.to_dict(),
            "message": payload.message,
            "context": payload.context,
            "test_mode": True  # No guardar en DB
        }
    )
    
    return response.json()
```

## 11. Checklist de Configuración

### Crear Agente
- [ ] Nombre descriptivo
- [ ] Template/Role seleccionado
- [ ] Model provider y versión
- [ ] Temperatura configurada (0.5-1.0)
- [ ] Tools habilitadas (mínimo 1)
- [ ] Canales seleccionados (mínimo 1)
- [ ] Agent tone personalizado
- [ ] Synonym dictionary (si aplica)
- [ ] Business rules definidas
- [ ] Credenciales del provider configuradas

### Testing
- [ ] Simular chat funciona
- [ ] Tools se invocan correctamente
- [ ] Respuestas coherentes con tone
- [ ] No alucinaciones de productos
- [ ] Derivación a humano funcional

---

**Tip**: Usar temperatura **0.7** para sales agents (balance creatividad/precisión) y **0.5** para support (más preciso).
