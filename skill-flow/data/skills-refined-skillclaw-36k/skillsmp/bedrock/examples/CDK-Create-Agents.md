# example of a CDK nodejs file to create Agents using the configuration json file

**user intent** set up system, define Bedrock agents and Multi-Agent Collaberation

**this is JUST an example, must be changed to fit project, report steps taken and status** 

import * as cdk from 'aws-cdk-lib';
import * as bedrock from '@aws-cdk/aws-bedrock-alpha';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as fs from 'fs';
import * as path from 'path';

export class FinanceAssistantStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // 1. Load the Configuration
    const configPath = path.join(__dirname, '../config/agent-configuration.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

    // 2. Define the shared Runtime Role for Agents
    const agentRole = new iam.Role(this, 'FinanceAgentRole', {
      assumedBy: new iam.ServicePrincipal('bedrock.amazonaws.com'),
    });

    // Grant access to Bedrock Models
    agentRole.addToPolicy(new iam.PolicyStatement({
      actions: ['bedrock:InvokeModel', 'bedrock:InvokeModelWithResponseStream'],
      resources: [`arn:aws:bedrock:${config.bedrock.region}::foundation-model/*`],
    }));

    // Grant access to AWS Marketplace (some foundation models require subscription/agreements)
    agentRole.addToPolicy(new iam.PolicyStatement({
      actions: [
        'aws-marketplace:Subscribe',
        'aws-marketplace:ViewSubscriptions',
        'aws-marketplace:GetAgreementTerms',
        'aws-marketplace:ListAgreementApprovalRequests',
        'aws-marketplace:CreateAgreementRequest'
      ],
      resources: ['*'],
    }));

    // Optional: Allow listing received licenses via License Manager if marketplace images use licenses
    agentRole.addToPolicy(new iam.PolicyStatement({
      actions: ['license-manager:ListReceivedLicenses'],
      resources: ['*'],
    }));

    // Allow invoking the Tavily Lambda (so agents/tools can call the function)
    agentRole.addToPolicy(new iam.PolicyStatement({
      actions: ['lambda:InvokeFunction'],
      resources: ['arn:aws:lambda:' + this.region + ':' + this.account + ':function:TavilyLambdaFunction'],
    }));

    // 3. Create the Action Group for Tavily (Lambda-based Web Crawler)
    const tavilyLambda = lambda.Function.fromFunctionName(this, 'TavilyCrawler', 'TavilyLambdaFunction');
    const webCrawlerActionGroup = new bedrock.AgentActionGroup(this, 'WebCrawlerGroup', {
      actionGroupName: 'WebCrawler',
      description: 'Search the web using Tavily',
      executor: bedrock.ActionGroupExecutor.fromLambda(tavilyLambda),
      // Schema would be defined here or imported from a local asset
    });

    // Allow Bedrock service principal to invoke this Lambda (resource-based permission)
    try {
      tavilyLambda.addPermission('AllowBedrockInvoke', {
        principal: new iam.ServicePrincipal('bedrock.amazonaws.com'),
        sourceAccount: this.account,
      });
    } catch (e) {
      // If running as an example or the function is not present during synth, this may throw; ignore for example code
    }

    // 4. Create Agents dynamically from config
    const agentMap: { [key: string]: bedrock.Agent } = {};

    for (const agentKey of ['supervisor', 'coder', 'generic', 'financialAnalysis']) {
      const agentData = config[agentKey];
      
      const agent = new bedrock.Agent(this, agentData.agentId, {
        agentName: agentData.name,
        foundationModel: bedrock.BedrockFoundationModel.fromModelId(agentData.llmModel),
        instruction: agentData.systemPrompt,
        role: agentRole,
        shouldPrepareAgent: true, // Automatically prepares the DRAFT version
      });

      // Attach Tools based on config
      if (agentData.tools.includes('Amazon Code Interpreter')) {
        agent.addCodeInterpreter();
      }
      if (agentData.tools.includes('WebCrawler')) {
        agent.addActionGroup(webCrawlerActionGroup);
      }

      // Create Alias for the Agent
      const alias = agent.addAlias(agentKey + 'Alias', {
        agentAliasName: `${agentKey}-prod`,
      });

      agentMap[agentKey] = agent;
    }

    // 5. Configure Multi-Agent Collaboration (MAC)
    // The Supervisor is designated as the 'Orchestrator'
    const supervisor = agentMap['supervisor'];
    
    // Enabling collaboration on the Supervisor
    // Note: In 2026 CDK, this is managed via the 'collaboration' property or a dedicated method
    (supervisor as any).enableCollaboration({
        collaborationName: 'FinanceAssistantCollaboration',
        collaborators: [
            { agent: agentMap['coder'], name: 'CoderAgent' },
            { agent: agentMap['generic'], name: 'GenericAgent' },
            { agent: agentMap['financialAnalysis'], name: 'FinancialAnalysisAgent' }
        ]
    });
  }
}