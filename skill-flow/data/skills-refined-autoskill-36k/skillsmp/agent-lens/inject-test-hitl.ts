#!/usr/bin/env bun
/**
 * Test HITL Request Injector for Agent Lens
 *
 * Injects mock HITL requests into the events file for testing the HITL interface.
 * Creates realistic HITL events with different types (permission, question, choice).
 */

import { randomUUID } from 'crypto';
import { appendFileSync } from 'fs';
import { join } from 'path';

const PAI_DIR = process.env.HOME + '/.claude';
const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, '0');
const day = String(today.getDate()).padStart(2, '0');
const eventsFile = join(PAI_DIR, 'history', 'raw-outputs', `${year}-${month}`, `${year}-${month}-${day}_all-events.jsonl`);

console.log('🧪 Injecting test HITL requests into Agent Lens\n');
console.log(`Events file: ${eventsFile}\n`);

const testRequests = [
  {
    type: 'permission',
    question: 'Allow deletion of 15 temporary files in /tmp/build-cache?',
    timeout: 300,
    description: 'Permission request with 5-minute timeout'
  },
  {
    type: 'question',
    question: 'What should be the default timeout for API requests in the new service?',
    timeout: 600,
    description: 'Open question with 10-minute timeout'
  },
  {
    type: 'choice',
    question: 'Which database migration strategy should we use?',
    choices: [
      'Run migrations automatically on deployment',
      'Require manual migration approval',
      'Use blue-green deployment with rollback'
    ],
    timeout: 180,
    description: 'Multiple choice with 3-minute timeout'
  },
  {
    type: 'permission',
    question: 'Execute git push --force to remote branch feature/experimental?',
    timeout: 60,
    description: 'Urgent permission (1 minute) - will show critical styling'
  }
];

// Create UserPromptSubmit parent
const userPromptEventId = randomUUID();
const sessionId = randomUUID();

const userPromptEvent = {
  event_id: userPromptEventId,
  parent_event_id: null,
  source_app: 'qara',
  session_id: sessionId,
  hook_event_type: 'UserPromptSubmit',
  payload: {
    prompt: 'Test HITL interface with various request types'
  },
  timestamp: Date.now(),
  timestamp_aedt: new Date().toLocaleString('en-AU', { timeZone: 'Australia/Sydney' }),
  span_kind: 'internal'
};

console.log('Creating parent UserPromptSubmit event...');
appendFileSync(eventsFile, JSON.stringify(userPromptEvent) + '\n');
console.log(`✅ Event: ${userPromptEventId.substring(0, 8)}\n`);

// Create HITL events
testRequests.forEach((request, index) => {
  const eventId = randomUUID();

  const hitlEvent = {
    event_id: eventId,
    parent_event_id: userPromptEventId,
    source_app: 'qara',
    session_id: sessionId,
    hook_event_type: 'Notification',
    payload: {
      type: 'hitl_request',
      request_id: eventId
    },
    timestamp: Date.now() + index * 100, // Stagger slightly
    timestamp_aedt: new Date(Date.now() + index * 100).toLocaleString('en-AU', { timeZone: 'Australia/Sydney' }),
    span_kind: 'internal',
    humanInTheLoop: {
      question: request.question,
      responseWebSocketUrl: 'ws://localhost:4000/hitl-response',
      type: request.type,
      choices: request.choices,
      timeout: request.timeout,
      requiresResponse: true
    },
    humanInTheLoopStatus: {
      status: 'pending'
    }
  };

  console.log(`[${index + 1}/${testRequests.length}] ${request.description}`);
  console.log(`    Type: ${request.type}`);
  console.log(`    Timeout: ${request.timeout}s`);
  console.log(`    Event ID: ${eventId.substring(0, 8)}`);

  appendFileSync(eventsFile, JSON.stringify(hitlEvent) + '\n');
  console.log(`    ✅ Injected\n`);
});

console.log('━'.repeat(60));
console.log('✅ All test HITL requests injected!\n');
console.log('📊 Next steps:\n');
console.log('1. Check the Agent Lens dashboard at http://localhost:5173');
console.log('2. Click the "HITL" tab - you should see 4 pending requests');
console.log('3. Test the three-action pattern (Approve/Edit/Reject)');
console.log('4. Watch countdown timers for each request');
console.log('5. Notice color changes (green → yellow → red)');
console.log('6. The 1-minute request should show as critical (red)\n');

console.log('💡 Tip: Refresh the dashboard to see the new requests');
console.log('    The hot-reload should pick them up automatically via WebSocket\n');
