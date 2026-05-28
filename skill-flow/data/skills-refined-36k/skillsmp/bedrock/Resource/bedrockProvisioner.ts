import {
  ActionGroupSignature,
  BedrockAgentClient,
  CreateAgentActionGroupCommand,
  CreateAgentAliasCommand,
  CreateAgentCommand,
  PrepareAgentCommand,
  UpdateAgentCommand,
  GetAgentCommand,
  ListAgentsCommand,
  ListAgentAliasesCommand,
} from '@aws-sdk/client-bedrock-agent';

export type ProvisionedAlias = {
  agentAliasId: string;
  agentVersion: string;
};

export type BedrockProvisioningClient = {
  createAgent(args: {
    name: string;
    instruction: string;
    foundationModel: string;
    agentResourceRoleArn: string;
  }): Promise<{ agentId: string }>;

  updateAgent(args: {
    agentId: string;
    name: string;
    agentResourceRoleArn: string;
    instruction: string;
    foundationModel: string;
  }): Promise<void>;

  enableSearchGrounding(args: {
    agentId: string;
    actionGroupName: string;
    description: string;
  }): Promise<void>;

  prepareAgent(args: { agentId: string }): Promise<{ agentVersion: string }>;

  // Wait until agent status is no longer 'CREATING'.
  // onProgress is called each poll with the current status and elapsed ms.
  waitForAgentReady?: (args: {
    agentId: string;
    timeoutMs?: number;
    intervalMs?: number;
    onProgress?: (status: string | undefined, elapsedMs: number) => void;
  }) => Promise<void>;

  createAlias(args: {
    agentId: string;
    agentAliasName: string;
    agentVersion: string;
  }): Promise<ProvisionedAlias>;
  
  // Check if an alias exists in AWS
  aliasExists(args: {
    agentId: string;
    agentAliasId: string;
  }): Promise<boolean>;
  
  // Return the resolved endpoint URL the underlying AWS client will use, if available.
  getResolvedEndpoint?: () => Promise<string | undefined>;
};

function isAwsConflictError(error: unknown): boolean {
  return typeof error === 'object' && error !== null && (error as any).name === 'ConflictException';
}

export function createAwsBedrockProvisioningClient(region: string): BedrockProvisioningClient {
  const client = new BedrockAgentClient({ region });

  return {
    async createAgent({ name, instruction, foundationModel, agentResourceRoleArn }) {
      try {
        const resp = await client.send(
          new CreateAgentCommand({
            agentName: name,
            instruction,
            foundationModel,
            agentResourceRoleArn,
          }),
        );

        const agentId = resp.agent?.agentId;
        if (!agentId) throw new Error('Bedrock CreateAgent returned no agentId.');
        return { agentId };
      } catch (err: any) {
        console.error('[bedrockProvisioner] Error creating agent:', {
          errorName: err?.name,
          errorMessage: err?.message,
          errorCode: err?.code,
          statusCode: err?.$metadata?.httpStatusCode,
        });
        // If agent already exists, try to find it by name and return existing id.
        if (err && err.name === 'ConflictException') {
          try {
            const listResp = await client.send(new ListAgentsCommand({}));
            const anyList: any = listResp as any;
            const found = (anyList.agents || []).find((a: any) => a.agentName === name || a.name === name);
            if (found && found.agentId) return { agentId: found.agentId };
          } catch (listErr) {
            console.error('[bedrockProvisioner] Error listing agents:', listErr);
            // ignore and fall through to parsing the error message
          }

          // Try to parse agent id from the error message: "(id: VOFXHS9B7O)"
          try {
            const msg = String(err.message || err);
            const m = msg.match(/id:\s*([A-Za-z0-9-_]+)/i) || msg.match(/\(id:\s*([A-Za-z0-9-_]+)\)/i);
            if (m && m[1]) return { agentId: m[1] };
          } catch (parseErr) {
            // ignore
          }
        }
        throw err;
      }
    },

    async updateAgent({ agentId, name, agentResourceRoleArn, instruction, foundationModel }) {
      await client.send(
        new UpdateAgentCommand({
          agentId,
          agentName: name,
          agentResourceRoleArn,
          instruction,
          foundationModel,
        }),
      );
    },

    async enableSearchGrounding({ agentId, actionGroupName, description }) {
      try {
        await client.send(
          new CreateAgentActionGroupCommand({
            agentId,
            agentVersion: 'DRAFT',
            actionGroupName,
            description,
            // NOTE: This native tool signature is supported by Bedrock, but not yet typed in the SDK
            // version we're using (ActionGroupSignature enum doesn't include it).
            parentActionGroupSignature: 'AMAZON.SearchGrounding' as unknown as ActionGroupSignature,
            actionGroupState: 'ENABLED',
          }),
        );
      } catch (err) {
        // If the action group already exists, keep going.
        if (isAwsConflictError(err)) return;
        throw err;
      }
    },

    async prepareAgent({ agentId }) {
      const resp = await client.send(new PrepareAgentCommand({ agentId }));
      const agentVersion = resp.agentVersion;
      if (!agentVersion) throw new Error('Bedrock PrepareAgent returned no agentVersion.');
      return { agentVersion };
    },

    async createAlias({ agentId, agentAliasName, agentVersion }) {
      try {
        const resp = await client.send(
          new CreateAgentAliasCommand({
            agentId,
            agentAliasName,
            routingConfiguration: [{ agentVersion }],
          }),
        );

        const agentAliasId = resp.agentAlias?.agentAliasId;
        if (!agentAliasId) throw new Error('Bedrock CreateAgentAlias returned no agentAliasId.');
        return { agentAliasId, agentVersion };
      } catch (err: any) {
        if (err && err.name === 'ConflictException') {
          // try to find existing alias
          try {
            const listResp = await client.send(new ListAgentAliasesCommand({ agentId }));
            const anyList: any = listResp as any;
            const found = (anyList.agentAliases || []).find((a: any) => a.agentAliasName === agentAliasName || a.name === agentAliasName);
            if (found && found.agentAliasId) return { agentAliasId: found.agentAliasId, agentVersion };
          } catch (listErr) {
            // fall through
          }
        }
        throw err;
      }
    },
    
    async aliasExists({ agentId, agentAliasId }) {
      try {
        const listResp = await client.send(new ListAgentAliasesCommand({ agentId }));
        const anyList: any = listResp as any;
        const aliases = anyList.agentAliasSummaries || anyList.agentAliases || [];
        return aliases.some((a: any) => a.agentAliasId === agentAliasId);
      } catch (err) {
        console.error('[bedrockProvisioner] Error checking if alias exists:', err);
        return false;
      }
    },
    
    async waitForAgentReady(args: {
      agentId: string;
      timeoutMs?: number;
      intervalMs?: number;
      onProgress?: (status: string | undefined, elapsedMs: number) => void;
    }) {
      const { agentId, timeoutMs = 120000, intervalMs = 3000, onProgress } = args;
      const start = Date.now();
      // polling loop
      while (true) {
        let status: string | undefined = undefined;
        try {
          const resp = await client.send(new GetAgentCommand({ agentId }));
          // use any to avoid SDK type mismatches across versions
          const anyResp: any = resp as any;
          status = anyResp?.agent?.status || anyResp?.status || undefined;
        } catch (err) {
          // Ignore transient errors; report undefined status
          status = undefined;
        }

        const elapsed = Date.now() - start;
        try {
          onProgress?.(status, elapsed);
        } catch (e) {
          // ignore progress callback errors
        }

        // If status is not 'CREATING' then we're done
        if (!status || String(status).toUpperCase() !== 'CREATING') return;

        if (elapsed > timeoutMs) {
          throw new Error(`Timed out waiting for agent ${agentId} to leave CREATING state`);
        }

        await new Promise((res) => setTimeout(res, intervalMs));
      }
    },
    async getResolvedEndpoint() {
      try {
        // client.config.endpoint may be a provider function
        const epProvider = (client.config as any).endpoint;
        if (!epProvider) return undefined;
        const ep = await epProvider();
        if (!ep) return undefined;
        if (typeof ep === 'string') return ep;
        // ep could be an object with protocol/hostname/port/path
        const proto = ep.protocol || (ep.scheme ? `${ep.scheme}:` : '');
        const host = ep.hostname || ep.host || '';
        const port = ep.port ? `:${ep.port}` : '';
        const path = ep.path || '';
        return `${proto}//${host}${port}${path}`;
      } catch (err) {
        return undefined;
      }
    },
  };
}
