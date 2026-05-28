import 'dotenv/config';

/**
 * Base URL for the Jules API.
 */
const BASE_URL = 'https://jules.googleapis.com/v1alpha';

/**
 * Retrieves the Jules API Key from the environment variables.
 * If the key is missing, it logs a fatal error and exits the process to prevent
 * agents from attempting to use the API without authentication.
 */
function getApiKey(): string {
  const apiKey = process.env.JULES_API_KEY;
  if (!apiKey) {
    console.error('FATAL ERROR: JULES_API_KEY environment variable is not set.');
    console.error('ACTION REQUIRED: Set the JULES_API_KEY environment variable in your .env file or shell session.');
    process.exit(1);
  }
  return apiKey;
}

/**
 * Common headers for all Jules API requests.
 * Includes the API key for authentication and sets Content-Type to JSON.
 */
function getHeaders(apiKey: string): HeadersInit {
  return {
    'x-goog-api-key': apiKey,
    'Content-Type': 'application/json',
  };
}

/**
 * Custom error class for Jules API errors.
 * Provides detailed information to help agents recover or understand why a request failed.
 */
export class JulesApiError extends Error {
  constructor(public status: number, public statusText: string, public body: string) {
    super(`Jules API Error: [${status}] ${statusText} - ${body}`);
    this.name = 'JulesApiError';
  }
}

/**
 * Wrapper around the native fetch API to handle Jules API requests.
 *
 * This function handles:
 * 1. Authentication (automatically injects the API key).
 * 2. constructing the full URL.
 * 3. Error handling (throws verbose JulesApiError on non-2xx responses).
 *
 * @param endpoint - The API endpoint (e.g., '/sessions' or 'sessions/123'). Should not include the base URL.
 * @param options - Standard fetch options (method, body, etc.).
 * @returns The parsed JSON response from the API.
 */
export async function julesFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const apiKey = getApiKey();
  const url = `${BASE_URL}/${endpoint.startsWith('/') ? endpoint.slice(1) : endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...getHeaders(apiKey),
        ...options.headers,
      },
    });

    if (!response.ok) {
      const text = await response.text();
      // Throw a verbose error to help the agent understand what went wrong.
      // 400s usually mean invalid input (prompt too long, bad source context).
      // 401/403 mean auth issues (check API key).
      // 404 means the session or resource was not found.
      // 500s are internal Jules errors (retry might help).
      throw new JulesApiError(response.status, response.statusText, text);
    }

    // Handle 204 No Content (e.g. DELETE)
    if (response.status === 204) {
      return {} as T;
    }

    // Check if content-type is json
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
        return await response.json();
    }

    // Fallback for non-json success (shouldn't happen much in this API but good for safety)
    return {} as T;

  } catch (error) {
    if (error instanceof JulesApiError) {
      console.error(`ERROR: Request to ${endpoint} failed.`);
      console.error(`STATUS: ${error.status} ${error.statusText}`);
      console.error(`DETAILS: ${error.body}`);

      if (error.status === 400) {
        console.error('SUGGESTION: Check your input parameters. Verify the session ID and request body format.');
      } else if (error.status === 401 || error.status === 403) {
        console.error('SUGGESTION: Verify your JULES_API_KEY is valid and has the necessary permissions.');
      } else if (error.status === 404) {
        console.error('SUGGESTION: The requested resource (e.g., session ID) was not found. It might have been deleted or never existed.');
      }
    } else {
        console.error(`FATAL ERROR: Network or unknown error occurred during request to ${endpoint}.`);
        console.error(`DETAILS: ${error}`);
    }
    // We re-throw so the specific script can decide if it needs to do extra cleanup, though usually they will just exit.
    throw error;
  }
}

// ----------------------------------------------------------------------------
// Types Reference | Jules
// ----------------------------------------------------------------------------

// Enums

export type SessionState =
  | 'STATE_UNSPECIFIED'
  | 'QUEUED'
  | 'PLANNING'
  | 'AWAITING_PLAN_APPROVAL'
  | 'AWAITING_USER_FEEDBACK'
  | 'IN_PROGRESS'
  | 'PAUSED'
  | 'FAILED'
  | 'COMPLETED';

export type AutomationMode =
  | 'AUTOMATION_MODE_UNSPECIFIED'
  | 'AUTO_CREATE_PR';

export type ActivityOriginator = 'user' | 'agent' | 'system';

// Main Resources

export interface Session {
  name: string; // Resource name, e.g., "sessions/12345"
  id: string; // Output only. The session ID.
  prompt: string;
  title?: string;
  state: SessionState;
  url: string; // Output only. URL to view the session.
  sourceContext?: SourceContext;
  requirePlanApproval?: boolean;
  automationMode?: AutomationMode;
  outputs?: SessionOutput[];
  createTime: string; // Output only
  updateTime: string; // Output only
}

export interface Activity {
  name: string; // resource name, e.g. "sessions/{session}/activities/{activity}"
  id: string; // Output only. The activity ID.
  originator: ActivityOriginator;
  description: string; // Output only
  createTime: string; // Output only

  // One of the event fields will be populated
  planGenerated?: PlanGenerated;
  planApproved?: PlanApproved;
  userMessaged?: UserMessaged;
  agentMessaged?: AgentMessaged;
  progressUpdated?: ProgressUpdated;
  sessionCompleted?: SessionCompleted;
  sessionFailed?: SessionFailed;

  // Artifacts
  artifacts?: Artifact[];
}

export interface Source {
  name: string; // resource name, e.g. "sources/{source}"
  id: string; // Output only.
  githubRepo: GitHubRepo;
}

// Sub-components

export interface Plan {
  id: string;
  steps: PlanStep[];
  createTime: string;
}

export interface PlanStep {
  id: string;
  index: number;
  title: string;
  description: string;
}

export interface Artifact {
  changeSet?: ChangeSet;
  bashOutput?: BashOutput;
  media?: Media;
}

export interface ChangeSet {
  source: string; // Format: sources/{source}
  gitPatch: GitPatch;
}

export interface GitPatch {
  baseCommitId: string;
  unidiffPatch: string;
  suggestedCommitMessage: string;
}

export interface BashOutput {
  command: string;
  output: string;
  exitCode: number;
}

export interface Media {
  mimeType: string;
  data: string; // base64-encoded
}

export interface GitHubRepo {
  owner: string;
  repo: string;
  isPrivate: boolean;
  defaultBranch: GitHubBranch;
  branches: GitHubBranch[];
}

export interface GitHubBranch {
  displayName: string;
}

export interface GitHubRepoContext {
  startingBranch?: string;
}

export interface SourceContext {
  source: string; // Format: sources/{source}
  githubRepoContext?: GitHubRepoContext;
}

export interface SessionOutput {
  pullRequest?: PullRequest;
}

export interface PullRequest {
  url: string;
  title: string;
  description: string;
}

// Activity Event Types

export interface PlanGenerated {
  plan: Plan;
}

export interface PlanApproved {
  planId: string;
}

export interface UserMessaged {
  userMessage: string;
}

export interface AgentMessaged {
  agentMessage: string;
}

export interface ProgressUpdated {
  title: string;
  description: string;
}

export type SessionCompleted = Record<string, never>; // Empty object

export interface SessionFailed {
  reason: string;
}

// Request/Response Types

export interface CreateSessionRequest {
  prompt: string;
  title?: string;
  sourceContext: SourceContext;
  requirePlanApproval?: boolean;
  automationMode?: AutomationMode;
}

export interface SendMessageRequest {
  prompt: string; // Note: API docs say "prompt" in curl example but "message" in text. Curl example uses 'prompt' key for send message. Let's assume 'prompt' based on previous experience or 'message' if strictly following "The message to send".
  // Re-checking user prompt:
  // "The message to send."
  // Curl: -d '{ "prompt": "Please also..." }'
  // So the key is likely "prompt".
}

export interface SendMessageResponse {
  // Empty
}

export interface ApprovePlanRequest {
  // Empty
}

export interface ApprovePlanResponse {
  // Empty
}

export interface ListSessionsResponse {
  sessions: Session[];
  nextPageToken?: string;
}

export interface ListActivitiesResponse {
  activities: Activity[];
  nextPageToken?: string;
}

export interface ListSourcesResponse {
  sources: Source[];
  nextPageToken?: string;
}
