import { BedrockAgentRuntimeClient, InvokeAgentCommand } from '@aws-sdk/client-bedrock-agent-runtime';
import { GetCallerIdentityCommand, STSClient } from '@aws-sdk/client-sts';
import { loadAgentConfig } from '../config/loadAgentConfig';

export type BedrockPromptOptions = {
  includeAgents?: boolean;
  timeoutMs: number;
  sessionId: string;
  allowInternet: boolean;
  userId: string;
};

export type BedrockStreamEvent =
  | { type: 'chunk'; text: string }
  | { type: 'trace'; raw: any };

type CredentialStatus = {
  hasCredentials: boolean;
  source: string;
  hasEnvAccessKey: boolean;
  hasEnvSecretKey: boolean;
  hasEnvSessionToken: boolean;
  awsProfile?: string;
};

async function checkCredentials(client: BedrockAgentRuntimeClient): Promise<CredentialStatus> {
  const hasEnvAccessKey = !!process.env.AWS_ACCESS_KEY_ID;
  const hasEnvSecretKey = !!process.env.AWS_SECRET_ACCESS_KEY;
  const hasEnvSessionToken = !!process.env.AWS_SESSION_TOKEN;
  const awsProfile = process.env.AWS_PROFILE || process.env.AWS_DEFAULT_PROFILE;

  try {
    // Try to resolve credentials from the SDK
    const credentials = await client.config.credentials();
    if (credentials?.accessKeyId) {
      const source = hasEnvAccessKey ? 'environment variables' : '~/.aws/credentials or instance role';
      return {
        hasCredentials: true,
        source,
        hasEnvAccessKey,
        hasEnvSecretKey,
        hasEnvSessionToken,
        awsProfile,
      };
    }
    return {
      hasCredentials: false,
      source: 'none',
      hasEnvAccessKey,
      hasEnvSecretKey,
      hasEnvSessionToken,
      awsProfile,
    };
  } catch (error) {
    return {
      hasCredentials: false,
      source: 'error: ' + (error as any).message,
      hasEnvAccessKey,
      hasEnvSecretKey,
      hasEnvSessionToken,
      awsProfile,
    };
  }
}

function getRuntimeClient(region: string) {
  const client = new BedrockAgentRuntimeClient({ region });
  return client;
}

// DEBUG-AUTH-START
async function logAuthDebug(region: string, client: BedrockAgentRuntimeClient): Promise<void> {
  if (process.env.BEDROCK_AUTH_DEBUG !== '1') {
    return;
  }

  try {
    const credentials = await client.config.credentials();
    const accessKeySuffix = credentials?.accessKeyId
      ? credentials.accessKeyId.slice(-4)
      : 'unknown';

    console.log('[bedrockSupervisor] AUTH DEBUG: resolved credentials', {
      accessKeySuffix,
      hasSessionToken: !!credentials?.sessionToken,
      region,
      awsProfile: process.env.AWS_PROFILE || process.env.AWS_DEFAULT_PROFILE,
      credentialsSource: process.env.AWS_ACCESS_KEY_ID ? 'env' : '~/.aws/credentials or instance role',
    });

    const sts = new STSClient({ region, credentials });
    const identity = await sts.send(new GetCallerIdentityCommand({}));
    console.log('[bedrockSupervisor] AUTH DEBUG: caller identity', {
      account: identity.Account,
      arn: identity.Arn,
      userId: identity.UserId,
    });
  } catch (error: any) {
    console.error('[bedrockSupervisor] AUTH DEBUG failed:', error?.message || error);
  }
}
// DEBUG-AUTH-END

export async function verifyBedrockRuntimeAccess(): Promise<void> {
  const { config } = loadAgentConfig();
  const region = config.bedrock?.region || process.env.AWS_REGION || process.env.AWS_DEFAULT_REGION || 'us-east-1';
  const agentId = config.supervisor?.agentId;
  const agentAliasId = config.supervisor?.agentAliasId;

  if (!agentId || agentId.includes('REPLACE_WITH_') || !agentAliasId || agentAliasId.includes('REPLACE_WITH_')) {
    throw new Error('Bedrock supervisor agentId/agentAliasId not configured. Update backend/config/agents.config.json.');
  }

  const client = getRuntimeClient(region);
  const credCheck = await checkCredentials(client);
  console.log('[bedrockSupervisor] Startup access check - credentials:', {
    hasCredentials: credCheck.hasCredentials,
    source: credCheck.source,
    region,
    hasEnvAccessKey: credCheck.hasEnvAccessKey,
    hasEnvSecretKey: credCheck.hasEnvSecretKey,
    hasEnvSessionToken: credCheck.hasEnvSessionToken,
    awsProfile: credCheck.awsProfile,
  });

  // DEBUG-AUTH-START
  await logAuthDebug(region, client);
  // DEBUG-AUTH-END

  if (!credCheck.hasCredentials) {
    throw new Error('AWS credentials not configured. Set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or configure ~/.aws/credentials.');
  }

  const command = new InvokeAgentCommand({
    agentId,
    agentAliasId,
    sessionId: `startup-check-${Date.now()}`,
    inputText: 'health check',
    enableTrace: false,
  });

  const abortController = new AbortController();
  const timeout = setTimeout(() => abortController.abort(), 8000);

  try {
    console.log('[bedrockSupervisor] Startup access check: invoking agent...');
    const response = await client.send(command, { abortSignal: abortController.signal });
    if (!response.completion) {
      throw new Error('Startup access check: no completion in response');
    }

    for await (const event of response.completion) {
      if (event.accessDeniedException || event.internalServerException || event.badGatewayException) {
        const errorEvent = event.internalServerException || event.badGatewayException || event.accessDeniedException;
        throw new Error(`Startup access check failed: ${errorEvent?.message || 'Unknown error'}`);
      }

      if (event.chunk?.bytes) {
        break;
      }
    }

    console.log('[bedrockSupervisor] Startup access check passed.');
  } catch (error: any) {
    const message = error?.message || 'Unknown error';
    throw new Error(`Bedrock runtime access check failed: ${message}`);
  } finally {
    clearTimeout(timeout);
  }
}

export async function* invokeSupervisorStream(prompt: string, options: BedrockPromptOptions): AsyncGenerator<BedrockStreamEvent> {
  const { config } = loadAgentConfig();
  const region = config.bedrock?.region || process.env.AWS_REGION || process.env.AWS_DEFAULT_REGION || 'us-east-1';

  const agentId = config.supervisor?.agentId;
  const defaultAliasId = config.supervisor?.agentAliasId;
  const internetAliasId = (config.supervisor as any)?.agentAliasIdInternet as string | undefined;

  const agentAliasId = options.allowInternet && internetAliasId ? internetAliasId : defaultAliasId;

  console.log('[bedrockSupervisor] Preparing InvokeAgentCommand (Bedrock Agent Runtime):', {
    region,
    agentId: agentId?.substring(0, 10) + '...',
    agentAliasId: agentAliasId?.substring(0, 10) + '...',
    sessionId: options.sessionId,
    allowInternet: options.allowInternet,
    timeoutMs: options.timeoutMs,
    promptLength: prompt.length,
    responseType: 'streaming',
  });

  if (!agentId || agentId.includes('REPLACE_WITH_') || !agentAliasId || agentAliasId.includes('REPLACE_WITH_')) {
    const errorMsg = 'Bedrock supervisor agentId/agentAliasId not configured. Update backend/config/agents.config.json.';
    console.error('[bedrockSupervisor] Configuration error:', errorMsg);
    throw new Error(errorMsg);
  }

  const client = getRuntimeClient(region);
  
  // Check credentials
  const credCheck = await checkCredentials(client);
  console.log('[bedrockSupervisor] AWS Credentials Status:', {
    hasCredentials: credCheck.hasCredentials,
    source: credCheck.source,
    region,
    hasEnvAccessKey: credCheck.hasEnvAccessKey,
    hasEnvSecretKey: credCheck.hasEnvSecretKey,
    hasEnvSessionToken: credCheck.hasEnvSessionToken,
    awsProfile: credCheck.awsProfile,
  });
  
  if (!credCheck.hasCredentials) {
    throw new Error('AWS credentials not configured. Set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or configure ~/.aws/credentials');
  }

  // DEBUG-AUTH-START
  await logAuthDebug(region, client);
  // DEBUG-AUTH-END

  const command = new InvokeAgentCommand({
    agentId,
    agentAliasId,
    sessionId: options.sessionId,
    inputText: prompt,
    enableTrace: !!options.includeAgents,
    sessionState: {
      sessionAttributes: {
        current_user_id: options.userId,
        allow_internet: String(options.allowInternet),
      },
    },
  });

  const abortController = new AbortController();
  const timeout = setTimeout(() => abortController.abort(), options.timeoutMs);

  try {
    console.log('[bedrockSupervisor] Sending InvokeAgentCommand to Bedrock Agent Runtime...');
    const response = await client.send(command, { abortSignal: abortController.signal });
    console.log('[bedrockSupervisor] InvokeAgent accepted. Waiting for stream events...');

    if (!response.completion) {
      console.warn('[bedrockSupervisor] No completion in response from Bedrock');
      return;
    }

    let chunkCount = 0;
    let hasChunk = false;
    let totalChunkChars = 0;
    let finalResponseText: string | undefined;
    for await (const event of response.completion) {
      // Log each event type to see what we're receiving
      console.log('[bedrockSupervisor] Stream event keys:', Object.keys(event));
      
      if (event.chunk?.bytes) {
        const text = Buffer.from(event.chunk.bytes).toString('utf-8');
        if (text) {
          chunkCount++;
          hasChunk = true;
          totalChunkChars += text.length;
          yield { type: 'chunk', text };
        }
      }
      
      if (event.trace) {
        // Log trace details to see if error is inside
        const trace = event.trace as any;
        const traceDetails = {
          hasFailureTrace: !!trace.failureTrace,
          hasOrchestrationTrace: !!trace.orchestrationTrace,
          traceKeys: Object.keys(event.trace || {}),
        };
        console.log('[bedrockSupervisor] Trace event details:', traceDetails);

        if (process.env.BEDROCK_TRACE_DEBUG === '1') {
          console.log('[bedrockSupervisor] Trace event payload:', JSON.stringify(trace, null, 2));
        }

        // Capture final response from trace if provided
        const traceFinalText = trace?.orchestrationTrace?.observation?.finalResponse?.text as string | undefined;
        if (traceFinalText) {
          finalResponseText = traceFinalText;
          if (!hasChunk) {
            console.log('[bedrockSupervisor] No chunk data received; emitting finalResponse text from trace.');
            hasChunk = true;
            chunkCount++;
            totalChunkChars += traceFinalText.length;
            yield { type: 'chunk', text: traceFinalText };
          }
        }
        
        // Check if trace contains failure information
        if (trace.failureTrace) {
          console.error('[bedrockSupervisor] FAILURE TRACE:', JSON.stringify(trace.failureTrace, null, 2));
          const failureReason = trace.failureTrace.failureReason || 'Unknown failure';
          throw new Error(`Bedrock agent failure: ${failureReason}`);
        }
        
        yield { type: 'trace', raw: event };
      }
      
      // Check for error events in the stream
      if (event.internalServerException || event.badGatewayException || event.accessDeniedException) {
        const errorEvent = event.internalServerException || event.badGatewayException || event.accessDeniedException;
        console.error('[bedrockSupervisor] Error event in stream:', JSON.stringify(errorEvent, null, 2));
        throw new Error(`Bedrock stream error: ${errorEvent.message || 'Unknown error'}`);
      }
    }

    const finalLength = finalResponseText?.length ?? 0;
    console.log(`[bedrockSupervisor] Request complete. Received ${chunkCount} chunks (${totalChunkChars} chars). Trace finalResponse length=${finalLength}`);
  } catch (error: any) {
    // Enhanced error logging with more diagnostic info
    const errorInfo = {
      errorName: error?.name || 'Unknown',
      errorMessage: error?.message || 'No error message',
      errorCode: error?.code,
      errorType: error?.__type,
      statusCode: error?.$metadata?.httpStatusCode,
      requestId: error?.$metadata?.requestId,
      region,
      agentId: agentId?.substring(0, 10) + '...',
      sessionId: options.sessionId,
    };
    
    console.error('[bedrockSupervisor] Error invoking Bedrock:', errorInfo);
    console.error('[bedrockSupervisor] Full error object:', JSON.stringify(error, null, 2));
    
    if (error?.stack) {
      console.error('[bedrockSupervisor] Stack trace:', error.stack);
    }
    
    // Add helpful diagnostic messages
    if (!error?.$metadata && !error?.name) {
      console.error('[bedrockSupervisor] DIAGNOSIS: Error has no AWS metadata - likely a credentials, profile, or network issue');
      console.error('[bedrockSupervisor] Check: 1) AWS credentials configured, 2) AWS_PROFILE matches ~/.aws/credentials, 3) Network connectivity, 4) AWS region is correct');
    }
    
    if (error?.name === 'CredentialsProviderError' || error?.message?.includes('credentials')) {
      console.error('[bedrockSupervisor] DIAGNOSIS: Credentials error detected');
      console.error('[bedrockSupervisor] Solution: Configure AWS credentials via environment variables or ~/.aws/credentials');
    }
    
    if (error?.code === 'AccessDeniedException' || error?.name === 'AccessDeniedException') {
      console.error('[bedrockSupervisor] DIAGNOSIS: Access denied by AWS');
      console.error('[bedrockSupervisor] Solution: Ensure your AWS credentials have bedrock:InvokeAgent permission');
      console.error('[bedrockSupervisor] Required IAM policy: { "Effect": "Allow", "Action": "bedrock:InvokeAgent", "Resource": "*" }');
    }
    
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}
