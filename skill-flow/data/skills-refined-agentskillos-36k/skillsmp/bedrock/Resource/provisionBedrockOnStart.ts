import fs from 'fs';
import path from 'path';
import { AgentConfigFile } from '../config/agentConfig';
import { loadAgentConfig } from '../config/loadAgentConfig';
import {
  getBedrockAgentRoleArn,
  getDefaultBedrockModelId,
  shouldProvisionBedrockOnStart,
} from '../config/provisioningConfig';
import { diffJsonPaths, stableNormalize } from '../utils/configDrift';
import {
  BedrockProvisioningClient,
  createAwsBedrockProvisioningClient,
} from './bedrockProvisioner';

const PLACEHOLDER_PREFIX = 'REPLACE_WITH_';
const SECRET_KEYS = ['agentResourceRoleArn', 'lambdaArn', 'tavilyApiKey', 'serpapiApiKey', 'provisionOnStart'];

function isPlaceholder(value: string | undefined): boolean {
  if (!value) return true;
  return value.trim().toUpperCase().startsWith(PLACEHOLDER_PREFIX);
}

function readJsonOrEmpty(filePath: string): unknown {
  if (!fs.existsSync(filePath)) return {};
  const raw = fs.readFileSync(filePath, 'utf8').trim();
  if (!raw) return {};
  return JSON.parse(raw);
}

function writeJson(filePath: string, value: unknown): void {
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2) + '\n', 'utf8');
}

function resolveAppliedPath(configPath: string): string {
  return path.join(path.dirname(configPath), 'agents.config.applied.json');
}

function isRoleArn(value: string): boolean {
  return /^arn:aws:iam::\d{12}:role\/.+$/i.test(value);
}

export type ProvisionOnStartOptions = {
  clientFactory?: (region: string) => BedrockProvisioningClient;
  logger?: Pick<Console, 'log' | 'warn' | 'error'>;
};

function formatAwsError(err: unknown): string {
  if (!err || typeof err !== 'object') return String(err);
  const anyErr = err as any;
  const parts = [
    `name=${anyErr.name || 'UnknownError'}`,
    `message=${anyErr.message || 'unknown'}`,
    anyErr.$metadata?.requestId ? `requestId=${anyErr.$metadata.requestId}` : null,
    anyErr.$metadata?.httpStatusCode ? `httpStatus=${anyErr.$metadata.httpStatusCode}` : null,
    anyErr.$fault ? `fault=${anyErr.$fault}` : null,
    anyErr.code ? `code=${anyErr.code}` : null,
  ].filter(Boolean);
  return parts.join(' ');
}

async function ensureSupervisor(
  desired: AgentConfigFile,
  client: BedrockProvisioningClient,
  agentResourceRoleArn: string,
  logger: Pick<Console, 'log' | 'warn' | 'error'>,
): Promise<void> {
  const foundationModel = desired.supervisor.modelId || getDefaultBedrockModelId();
  const instruction = desired.supervisor.systemPrompt || '';

  if (isPlaceholder(desired.supervisor.agentId)) {
    logger.log('[bedrock-provision] Creating supervisor agent...');
    const { agentId } = await client.createAgent({
      name: desired.supervisor.name,
      instruction,
      foundationModel,
      agentResourceRoleArn,
    });
    desired.supervisor.agentId = agentId;

    logger.log(`[bedrock-provision] Supervisor created with agentId=${agentId}.`);
    if (client.waitForAgentReady) {
      // Poll every 10s and report status
      const intervalMs = 10000;
      const timeoutMs = 3 * 60 * 1000; // 3 minutes
      // eslint-disable-next-line no-console
      console.log(`[bedrock-provision] Supervisor being created: ${desired.supervisor.name} (${agentId}). Waiting for agent to become ready...`);
      await client.waitForAgentReady({
        agentId,
        intervalMs,
        timeoutMs,
        onProgress(status, elapsed) {
          // eslint-disable-next-line no-console
          console.log(`[bedrock-provision] Supervisor status=${status || 'unknown'} elapsed=${Math.round(elapsed / 1000)}s`);
        },
      });
      logger.log('[bedrock-provision] Supervisor agent is ready.');
    }
  } else {
    // Best-effort: keep agent aligned with desired instruction/model.
    logger.log('[bedrock-provision] Updating supervisor agent instruction/model...');
    await client.updateAgent({
      agentId: desired.supervisor.agentId,
      name: desired.supervisor.name,
      agentResourceRoleArn,
      instruction,
      foundationModel,
    });
  }

  // Create a version with NO SearchGrounding for the default alias.
  if (isPlaceholder(desired.supervisor.agentAliasId)) {
    logger.log('[bedrock-provision] Preparing supervisor (no-internet) version...');
    // Try preparing; if it takes too long, warn but continue.
    try {
      const prepareIntervalMs = 10000;
      const prepareTimeoutMs = 5 * 60 * 1000; // 5 minutes
      const start = Date.now();
      let agentVersion: string | undefined;
      while (!agentVersion) {
        try {
          const resp = await client.prepareAgent({ agentId: desired.supervisor.agentId });
          agentVersion = resp.agentVersion;
          if (agentVersion) break;
        } catch (err) {
          // If agent is still creating, prepare will fail; keep retrying until timeout.
        }

        const elapsed = Date.now() - start;
        // eslint-disable-next-line no-console
        console.log(`[bedrock-provision] Preparing supervisor... elapsed=${Math.round(elapsed / 1000)}s`);
        if (elapsed > prepareTimeoutMs) {
          // warn and stop trying to prepare automatically
          console.warn('[bedrock-provision] Preparing is taking a long time; skipping automatic prepare. You can prepare the agent manually in the AWS Console.');
          agentVersion = undefined;
          break;
        }
        await new Promise((res) => setTimeout(res, prepareIntervalMs));
      }

      if (agentVersion) {
        logger.log('[bedrock-provision] Creating supervisor default alias...');
        const { agentAliasId } = await client.createAlias({
          agentId: desired.supervisor.agentId,
          agentAliasName: 'default',
          agentVersion,
        });
        desired.supervisor.agentAliasId = agentAliasId;
      } else {
        logger.warn('[bedrock-provision] Supervisor not prepared; leaving default alias placeholder for manual prepare.');
      }
    } catch (err) {
      logger.warn('[bedrock-provision] Unexpected error during prepare; leaving alias placeholder.');
    }
  } else {
    // Check if the alias actually exists in AWS
    const aliasExists = await client.aliasExists({
      agentId: desired.supervisor.agentId,
      agentAliasId: desired.supervisor.agentAliasId,
    });
    
    if (!aliasExists) {
      logger.warn(`[bedrock-provision] Supervisor alias ${desired.supervisor.agentAliasId} not found in AWS. Creating new alias...`);
      try {
        const prepareIntervalMs = 10000;
        const prepareTimeoutMs = 5 * 60 * 1000; // 5 minutes
        const start = Date.now();
        let agentVersion: string | undefined;
        while (!agentVersion) {
          try {
            const resp = await client.prepareAgent({ agentId: desired.supervisor.agentId });
            agentVersion = resp.agentVersion;
            if (agentVersion) break;
          } catch (err) {
            // If agent is still creating, prepare will fail; keep retrying until timeout.
          }

          const elapsed = Date.now() - start;
          // eslint-disable-next-line no-console
          console.log(`[bedrock-provision] Preparing supervisor... elapsed=${Math.round(elapsed / 1000)}s`);
          if (elapsed > prepareTimeoutMs) {
            console.warn('[bedrock-provision] Preparing is taking a long time; skipping automatic prepare. You can prepare the agent manually in the AWS Console.');
            agentVersion = undefined;
            break;
          }
          await new Promise((res) => setTimeout(res, prepareIntervalMs));
        }

        if (agentVersion) {
          logger.log('[bedrock-provision] Creating supervisor default alias...');
          const { agentAliasId } = await client.createAlias({
            agentId: desired.supervisor.agentId,
            agentAliasName: 'default',
            agentVersion,
          });
          desired.supervisor.agentAliasId = agentAliasId;
          logger.log(`[bedrock-provision] Supervisor alias created: ${agentAliasId}`);
        } else {
          logger.warn('[bedrock-provision] Supervisor not prepared; cannot create alias.');
        }
      } catch (err) {
        logger.error('[bedrock-provision] Failed to create supervisor alias:', err);
      }
    } else {
      logger.log(`[bedrock-provision] Supervisor alias ${desired.supervisor.agentAliasId} exists in AWS.`);
    }
  }

  // NOTE: SearchGrounding (AMAZON.SearchGrounding) is not supported in the current SDK.
  // Internet alias creation for supervisor is skipped. If needed, configure manually in AWS Console.
  if (desired.supervisor.agentAliasIdInternet && isPlaceholder(desired.supervisor.agentAliasIdInternet)) {
    logger.warn('[bedrock-provision] Supervisor internet alias (agentAliasIdInternet) is not auto-provisioned because SearchGrounding is unsupported. Configure manually if needed.');
  }
}

async function ensureCollaborators(
  desired: AgentConfigFile,
  client: BedrockProvisioningClient,
  agentResourceRoleArn: string,
  logger: Pick<Console, 'log' | 'warn' | 'error'>,
): Promise<void> {
  if (!desired.collaborators || desired.collaborators.length === 0) return;

  for (const collaborator of desired.collaborators) {
    const foundationModel = collaborator.modelId || getDefaultBedrockModelId();
    const instruction = collaborator.description || '';

    if (!collaborator.agentId || isPlaceholder(collaborator.agentId)) {
      logger.log(`[bedrock-provision] Creating collaborator agent: ${collaborator.id}...`);
      const { agentId } = await client.createAgent({
        name: collaborator.name,
        instruction,
        foundationModel,
        agentResourceRoleArn,
      });
      logger.log(`[bedrock-provision] Collaborator ${collaborator.id} created with agentId=${agentId}. Waiting for agent to become ready...`);
      if (client.waitForAgentReady) {
        // eslint-disable-next-line no-console
        console.log(`[bedrock-provision] Collaborator being created: ${collaborator.name} (${agentId})`);
        await client.waitForAgentReady({ agentId });
        logger.log(`[bedrock-provision] Collaborator ${collaborator.id} is ready.`);
      }
      collaborator.agentId = agentId;
    } else {
      logger.log(`[bedrock-provision] Updating collaborator agent: ${collaborator.id}...`);
      await client.updateAgent({
        agentId: collaborator.agentId,
        name: collaborator.name,
        agentResourceRoleArn,
        instruction,
        foundationModel,
      });
    }

    // Default alias - prepare agent with retry logic
    if (!collaborator.agentAliasId || isPlaceholder(collaborator.agentAliasId)) {
      logger.log(`[bedrock-provision] Preparing collaborator ${collaborator.id} version...`);
      try {
        const prepareIntervalMs = 10000;
        const prepareTimeoutMs = 5 * 60 * 1000; // 5 minutes
        const start = Date.now();
        let agentVersion: string | undefined;
        while (!agentVersion) {
          try {
            const resp = await client.prepareAgent({ agentId: collaborator.agentId });
            agentVersion = resp.agentVersion;
            if (agentVersion) break;
          } catch (err) {
            // If agent is still creating, prepare will fail; keep retrying until timeout.
          }

          const elapsed = Date.now() - start;
          // eslint-disable-next-line no-console
          console.log(`[bedrock-provision] Preparing collaborator ${collaborator.id}... elapsed=${Math.round(elapsed / 1000)}s`);
          if (elapsed > prepareTimeoutMs) {
            console.warn(`[bedrock-provision] Preparing collaborator ${collaborator.id} is taking a long time; skipping automatic prepare.`);
            agentVersion = undefined;
            break;
          }
          await new Promise((res) => setTimeout(res, prepareIntervalMs));
        }

        if (agentVersion) {
          logger.log(`[bedrock-provision] Creating collaborator ${collaborator.id} default alias...`);
          const { agentAliasId } = await client.createAlias({
            agentId: collaborator.agentId,
            agentAliasName: 'default',
            agentVersion,
          });
          collaborator.agentAliasId = agentAliasId;
        } else {
          logger.warn(`[bedrock-provision] Collaborator ${collaborator.id} not prepared; leaving default alias placeholder.`);
        }
      } catch (err) {
        logger.warn(`[bedrock-provision] Unexpected error during collaborator ${collaborator.id} prepare; leaving alias placeholder.`);
      }
    } else {
      // Check if the alias actually exists in AWS
      const aliasExists = await client.aliasExists({
        agentId: collaborator.agentId,
        agentAliasId: collaborator.agentAliasId,
      });
      
      if (!aliasExists) {
        logger.warn(`[bedrock-provision] Collaborator ${collaborator.id} alias ${collaborator.agentAliasId} not found in AWS. Creating new alias...`);
        try {
          const prepareIntervalMs = 10000;
          const prepareTimeoutMs = 5 * 60 * 1000; // 5 minutes
          const start = Date.now();
          let agentVersion: string | undefined;
          while (!agentVersion) {
            try {
              const resp = await client.prepareAgent({ agentId: collaborator.agentId });
              agentVersion = resp.agentVersion;
              if (agentVersion) break;
            } catch (err) {
              // If agent is still creating, prepare will fail; keep retrying until timeout.
            }

            const elapsed = Date.now() - start;
            // eslint-disable-next-line no-console
            console.log(`[bedrock-provision] Preparing collaborator ${collaborator.id}... elapsed=${Math.round(elapsed / 1000)}s`);
            if (elapsed > prepareTimeoutMs) {
              console.warn(`[bedrock-provision] Preparing collaborator ${collaborator.id} is taking a long time; skipping automatic prepare.`);
              agentVersion = undefined;
              break;
            }
            await new Promise((res) => setTimeout(res, prepareIntervalMs));
          }

          if (agentVersion) {
            logger.log(`[bedrock-provision] Creating collaborator ${collaborator.id} default alias...`);
            const { agentAliasId } = await client.createAlias({
              agentId: collaborator.agentId,
              agentAliasName: 'default',
              agentVersion,
            });
            collaborator.agentAliasId = agentAliasId;
            logger.log(`[bedrock-provision] Collaborator ${collaborator.id} alias created: ${agentAliasId}`);
          } else {
            logger.warn(`[bedrock-provision] Collaborator ${collaborator.id} not prepared; cannot create alias.`);
          }
        } catch (err) {
          logger.error(`[bedrock-provision] Failed to create collaborator ${collaborator.id} alias:`, err);
        }
      } else {
        logger.log(`[bedrock-provision] Collaborator ${collaborator.id} alias ${collaborator.agentAliasId} exists in AWS.`);
      }
    }

    // NOTE: SearchGrounding is not supported in the current SDK.
    // Internet alias for collaborators (e.g., researcher) must be configured manually in AWS Console.
    if (collaborator.allowInternet) {
      if (!collaborator.agentAliasIdInternet || isPlaceholder(collaborator.agentAliasIdInternet)) {
        logger.warn(`[bedrock-provision] Collaborator ${collaborator.id} requires internet access (allowInternet=true) but SearchGrounding is unsupported. Configure internet alias manually in AWS Console if needed.`);
      }
    }
  }
}

export async function provisionBedrockOnStart(options: ProvisionOnStartOptions = {}): Promise<void> {
  const logger = options.logger ?? console;

  // Always print a console-level start marker so devs see provisioning happening.
  // Use console directly to ensure it's visible even if a custom logger is provided.
  // eslint-disable-next-line no-console
  console.log('[bedrock-provision] Starting provision-on-start...');

  const { config: desiredConfig, configPath } = loadAgentConfig();
  // Determine whether provisioning should run. Priority:
  // 1. explicit `desiredConfig.provisionOnStart` in config file
  // 2. env var `BEDROCK_PROVISION_ON_START` (via shouldProvisionBedrockOnStart)
  const provisionFlagFromConfig = (desiredConfig as any).provisionOnStart;
  if (typeof provisionFlagFromConfig === 'boolean' ? !provisionFlagFromConfig : !shouldProvisionBedrockOnStart()) {
    logger.log('[bedrock-provision] Provision-on-start disabled.');
    return;
  }

  const appliedPath = resolveAppliedPath(configPath);

  const appliedConfig = readJsonOrEmpty(appliedPath);
  const desiredStable = stableNormalize(desiredConfig);
  const appliedStable = stableNormalize(appliedConfig);

  const driftPaths = diffJsonPaths(desiredStable, appliedStable);
  if (driftPaths.length === 0) {
    logger.log('[bedrock-provision] No drift (desired == applied).');
    return;
  }

  logger.warn(`[bedrock-provision] Drift detected (${driftPaths.length} path(s)).`);
  for (const p of driftPaths.slice(0, 25)) logger.warn(`[bedrock-provision] - ${p}`);
  if (driftPaths.length > 25) logger.warn(`[bedrock-provision] (truncated; showing 25/${driftPaths.length})`);

  // Prefer a value stored in the desired config file (config-only mode).
  const agentResourceRoleArnFromConfig = (desiredConfig as any).agentResourceRoleArn;
  const agentResourceRoleArn = agentResourceRoleArnFromConfig || getBedrockAgentRoleArn();
  if (!agentResourceRoleArn) {
    const message = 'Missing BEDROCK_AGENT_ROLE_ARN (env) or agentResourceRoleArn (config); cannot provision agents.';
    logger.error(`[bedrock-provision] ${message}`);
    logger.error('[bedrock-provision] Set BEDROCK_AGENT_ROLE_ARN env var or add `agentResourceRoleArn` to your agents config file.');
    throw new Error(message);
  }
  if (!isRoleArn(agentResourceRoleArn)) {
    const message = `Invalid agentResourceRoleArn: expected an IAM role ARN, got "${agentResourceRoleArn}".`;
    logger.error(`[bedrock-provision] ${message}`);
    logger.error('[bedrock-provision] Example role ARN: arn:aws:iam::123456789012:role/BedrockAgentsRole');
    logger.error('[bedrock-provision] You likely provided a policy ARN (arn:aws:iam::aws:policy/...).');
    throw new Error(message);
  }

  const region = desiredConfig.bedrock?.region || process.env.AWS_REGION || 'us-east-1';
  const clientFactory = options.clientFactory ?? createAwsBedrockProvisioningClient;
  const client = clientFactory(region);

  // Log the resolved endpoint so it's clear if we're hitting LocalStack or real AWS.
  try {
    const resolved = await (client.getResolvedEndpoint ? client.getResolvedEndpoint() : undefined);
    if (resolved) logger.log(`[bedrock-provision] Resolved provisioning endpoint: ${resolved}`);
  } catch (err) {
    // ignore endpoint resolution errors
  }

  // Mutate desiredConfig in-place with provisioned IDs.
  try {
    await ensureSupervisor(desiredConfig, client, agentResourceRoleArn, logger);
    await ensureCollaborators(desiredConfig, client, agentResourceRoleArn, logger);
  } catch (err) {
    logger.error('[bedrock-provision] Provisioning failed.');
    logger.error(`[bedrock-provision] ${formatAwsError(err)}`);
    throw err;
  }

  // Persist: write the desired config (with real IDs) and update the applied snapshot.
  // ALWAYS strip sensitive fields to prevent leaking secrets into version control.
  const configToWrite = { ...desiredConfig };
  for (const key of SECRET_KEYS) {
    delete (configToWrite as any)[key];
  }

  // Write back to the config file ONLY if it's a local file
  const shouldUpdateConfigFile = /agents\.config\.local\.json$/i.test(configPath);
  if (shouldUpdateConfigFile) {
    writeJson(configPath, configToWrite);
  }

  // Always update applied snapshot (without secrets)
  writeJson(appliedPath, configToWrite);
  logger.log('[bedrock-provision] Provisioning complete; config + applied snapshot updated.');

  // Also print a console-level finish marker so devs see provisioning finished.
  // eslint-disable-next-line no-console
  console.log('[bedrock-provision] Finished provision-on-start.');
}
