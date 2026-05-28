// New interface for human-in-the-loop requests
export interface HumanInTheLoop {
  question: string;
  responseWebSocketUrl: string;
  type: 'question' | 'permission' | 'choice';
  choices?: string[]; // For multiple choice questions
  timeout?: number; // Optional timeout in seconds
  requiresResponse?: boolean; // Whether response is required or optional
}

// Response interface
export interface HumanInTheLoopResponse {
  response?: string;
  permission?: boolean;
  choice?: string; // Selected choice from options
  hookEvent: HookEvent;
  respondedAt: number;
  respondedBy?: string; // Optional user identifier
}

// Status tracking interface
export interface HumanInTheLoopStatus {
  status: 'pending' | 'responded' | 'timeout' | 'error';
  respondedAt?: number;
  response?: HumanInTheLoopResponse;
}

export interface HookEvent {
  id?: number;

  // Core identification (Agent Lens enhancements)
  event_id: string;                  // NEW: Unique event ID (UUID)
  parent_event_id?: string | null;   // NEW: Parent event for hierarchy
  source_app: string;
  session_id: string;
  hook_event_type: string;
  payload: Record<string, any>;
  chat?: any[];
  summary?: string;
  timestamp?: number;
  timestamp_aedt?: string;           // AEDT timestamp string

  // Hierarchy metadata (Agent Lens)
  span_kind?: string;                // NEW: OpenTelemetry span kind (root/internal/client)
  children?: string[];               // NEW: Computed on server - child event IDs
  depth?: number;                    // NEW: Computed on server - hierarchy depth (0 = root)

  // Context tracking (CC 2.1.6 integration)
  context_used?: number;             // NEW: Context tokens used
  context_remaining?: number;        // NEW: Context tokens remaining
  context_used_percentage?: number;  // NEW: % of context used
  context_remaining_percentage?: number; // NEW: % of context remaining

  // Metrics (Agent Lens)
  model_name?: string;
  estimated_tokens?: number;         // NEW: Estimated token count for this event
  estimated_cost?: number;           // NEW: Estimated cost in USD for this event

  // Skill tracking (Agent Lens)
  skill_name?: string;               // NEW: Skill name if this is a skill invocation

  // HITL data
  humanInTheLoop?: HumanInTheLoop;
  humanInTheLoopStatus?: HumanInTheLoopStatus;
}

export interface FilterOptions {
  source_apps: string[];
  session_ids: string[];
  hook_event_types: string[];
}

export interface WebSocketMessage {
  type: 'initial' | 'event' | 'hitl_response';
  data: HookEvent | HookEvent[] | HumanInTheLoopResponse;
}

export type TimeRange = '1m' | '3m' | '5m' | '10m';

export interface ChartDataPoint {
  timestamp: number;
  count: number;
  eventTypes: Record<string, number>; // event type -> count
  sessions: Record<string, number>; // session id -> count
  apps?: Record<string, number>; // app name -> count (optional for backward compatibility)
}

export interface ChartConfig {
  maxDataPoints: number;
  animationDuration: number;
  barWidth: number;
  barGap: number;
  colors: {
    primary: string;
    glow: string;
    axis: string;
    text: string;
  };
}