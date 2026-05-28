/**
 * Human-in-the-Loop (HITL) Pattern
 *
 * Demonstrates:
 * - Requiring human approval for tools
 * - Handling interruptions
 * - Approving/rejecting tool calls
 * - Serializing and resuming state
 */

import { z } from 'zod';
import { Agent, Runner, tool, ToolApprovalItem } from '@openai/agents';
import * as readline from 'readline';

// ========================================
// Tools Requiring Approval
// ========================================

const sendEmailTool = tool({
  name: 'send_email',
  description: 'Send an email to a recipient',
  parameters: z.object({
    to: z.string().email(),
    subject: z.string(),
    body: z.string(),
  }),
  execute: async ({ to, subject, body }) => {
    console.log('\n📧 Email sent!');
    return `Email sent to ${to} with subject "${subject}"`;
  },
  requiresApproval: true, // Require human approval
});

const processRefundTool = tool({
  name: 'process_refund',
  description: 'Process a refund for a customer',
  parameters: z.object({
    customerId: z.string(),
    amount: z.number(),
    reason: z.string(),
  }),
  execute: async ({ customerId, amount, reason }) => {
    console.log('\n💰 Refund processed!');
    return `Refunded $${amount} to customer ${customerId}. Reason: ${reason}`;
  },
  requiresApproval: true,
});

const deleteAccountTool = tool({
  name: 'delete_account',
  description: 'Permanently delete a user account',
  parameters: z.object({
    userId: z.string(),
    confirmation: z.string(),
  }),
  execute: async ({ userId }) => {
    console.log('\n🗑️  Account deleted!');
    return `Account ${userId} has been permanently deleted`;
  },
  requiresApproval: true,
});

// ========================================
// Agent with Approval-Required Tools
// ========================================

const customerServiceAgent = new Agent({
  name: 'Customer Service Agent',
  instructions:
    'You help customers with their requests. Use tools when necessary but they will require human approval.',
  tools: [sendEmailTool, processRefundTool, deleteAccountTool],
});

// ========================================
// Helper: Prompt User for Approval
// ========================================

async function promptUserForApproval(toolName: string, args: Record<string, any>): Promise<boolean> {
  console.log('\n' + '='.repeat(60));
  console.log('⚠️  APPROVAL REQUIRED');
  console.log('='.repeat(60));
  console.log('Tool:', toolName);
  console.log('Arguments:', JSON.stringify(args, null, 2));
  console.log('='.repeat(60));

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => {
    rl.question('Approve this action? (y/n): ', (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'y');
    });
  });
}

// ========================================
// Run Agent with Human-in-the-Loop
// ========================================

async function runWithApproval(input: string) {
  console.log('\n🤖 Running agent with human approval...\n');
  console.log('User:', input);

  const runner = new Runner(customerServiceAgent);
  let result = await runner.run(input);

  // Handle interruptions (approval requests)
  while (result.interruption) {
    if (result.interruption.type === 'tool_approval') {
      const approvalItem = result.interruption as ToolApprovalItem;

      console.log(`\n🛑 Agent wants to call: ${approvalItem.toolCall.name}`);

      // Ask user for approval
      const approved = await promptUserForApproval(
        approvalItem.toolCall.name,
        approvalItem.toolCall.arguments
      );

      if (approved) {
        console.log('\n✅ Approved - resuming agent...');
        result = await result.state.approve(approvalItem);
      } else {
        console.log('\n❌ Rejected - agent will find alternative...');
        result = await result.state.reject(approvalItem, {
          reason: 'User rejected the action',
        });
      }
    } else {
      // Handle other interruption types if needed
      console.log('Unexpected interruption type:', result.interruption.type);
      break;
    }
  }

  console.log('\n✅ Agent finished');
  console.log('Final output:', result.output);

  return result;
}

// ========================================
// Example: State Serialization
// ========================================

async function exampleStateSerialization(input: string) {
  console.log('\n🔄 Example: Serializing and Resuming State\n');

  const runner = new Runner(customerServiceAgent);
  let result = await runner.run(input);

  if (result.interruption?.type === 'tool_approval') {
    const approvalItem = result.interruption as ToolApprovalItem;

    console.log('\n💾 Saving state for later...');

    // Serialize state (e.g., save to database)
    const serializedState = JSON.stringify(result.state);
    console.log('State saved (length:', serializedState.length, 'chars)');

    // Simulate delay (user goes away and comes back later)
    console.log('\n⏳ User away...\n');
    await new Promise((resolve) => setTimeout(resolve, 2000));

    console.log('👤 User returned!\n');

    // Deserialize state
    // Note: In real implementation, you'd use RunState.fromString()
    // const restoredState = RunState.fromString(customerServiceAgent, serializedState);

    // For demo, we'll just approve from current state
    const approved = await promptUserForApproval(approvalItem.toolCall.name, approvalItem.toolCall.arguments);

    if (approved) {
      result = await result.state.approve(approvalItem);
    } else {
      result = await result.state.reject(approvalItem);
    }
  }

  console.log('\n✅ Final output:', result.output);
}

// ========================================
// Example Usage
// ========================================

async function main() {
  const examples = [
    'Send an email to customer@example.com saying their order has shipped',
    'Process a $50 refund for customer ABC123 due to defective product',
    'Delete account user-456 permanently',
  ];

  // Interactive mode (uncomment to run)
  // for (const input of examples) {
  //   await runWithApproval(input);
  //   console.log('\n' + '='.repeat(80) + '\n');
  // }

  // State serialization example
  // await exampleStateSerialization(examples[1]);

  console.log('\n💡 Uncomment the code above to run interactive approval demos\n');
}

main();

export { customerServiceAgent, sendEmailTool, processRefundTool, deleteAccountTool, runWithApproval };
