<template>
  <div class="hitl-panel">
    <!-- Empty State -->
    <div v-if="pendingRequests.length === 0" class="empty-state">
      <div class="empty-icon">✅</div>
      <h3>No Pending Approvals</h3>
      <p>All human-in-the-loop requests have been handled.</p>
      <div class="empty-help">
        <p class="help-text">HITL requests appear when agents need:</p>
        <ul class="help-list">
          <li>🔐 Permission for operations</li>
          <li>❓ Answers to questions</li>
          <li>🎯 Choice between options</li>
        </ul>
      </div>
    </div>

    <!-- Pending Requests -->
    <div v-else class="requests-list">
      <div class="requests-header">
        <h3>{{ pendingRequests.length }} Pending Request{{ pendingRequests.length === 1 ? '' : 's' }}</h3>
        <span class="urgent-count" v-if="urgentCount > 0">
          {{ urgentCount }} urgent
        </span>
      </div>

      <HITLRequest
        v-for="request in sortedRequests"
        :key="request.hookEvent.event_id"
        :request="request"
        @approve="handleApprove(request)"
        @edit="handleEdit(request)"
        @reject="handleReject(request)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { HookEvent } from '../types';
import HITLRequest from './HITLRequest.vue';

interface HITLRequestData {
  hookEvent: HookEvent;
  receivedAt: number;
}

const props = defineProps<{
  pendingRequests: HITLRequestData[];
}>();

const emit = defineEmits<{
  approve: [request: HITLRequestData];
  edit: [request: HITLRequestData];
  reject: [request: HITLRequestData];
}>();

// Sort by urgency (timeout soon = first)
const sortedRequests = computed(() => {
  return [...props.pendingRequests].sort((a, b) => {
    const timeoutA = a.hookEvent.humanInTheLoop?.timeout || 300;
    const timeoutB = b.hookEvent.humanInTheLoop?.timeout || 300;

    const remainingA = timeoutA - (Date.now() - a.receivedAt) / 1000;
    const remainingB = timeoutB - (Date.now() - b.receivedAt) / 1000;

    return remainingA - remainingB; // Soonest timeout first
  });
});

// Count urgent requests (< 60 seconds remaining)
const urgentCount = computed(() => {
  return props.pendingRequests.filter(req => {
    const timeout = req.hookEvent.humanInTheLoop?.timeout || 300;
    const elapsed = (Date.now() - req.receivedAt) / 1000;
    const remaining = timeout - elapsed;
    return remaining < 60;
  }).length;
});

function handleApprove(request: HITLRequestData) {
  emit('approve', request);
}

function handleEdit(request: HITLRequestData) {
  emit('edit', request);
}

function handleReject(request: HITLRequestData) {
  emit('reject', request);
}
</script>

<style scoped>
.hitl-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  color: var(--theme-text-secondary, #B3B3B3);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.3;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.empty-state > p {
  margin: 0 0 2rem 0;
  font-size: 0.875rem;
  color: var(--theme-text-tertiary, #808080);
}

.empty-help {
  max-width: 400px;
}

.help-text {
  margin: 0 0 0.75rem 0;
  font-size: 0.875rem;
  color: var(--theme-text-secondary, #B3B3B3);
  font-weight: 500;
}

.help-list {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
}

.help-list li {
  padding: 0.5rem 0;
  font-size: 0.875rem;
  color: var(--theme-text-tertiary, #808080);
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.requests-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0 1rem 0;
  border-bottom: 1px solid var(--theme-border-primary, #2A2A2A);
}

.requests-header h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.urgent-count {
  padding: 0.25rem 0.75rem;
  background: var(--theme-error-bg, rgba(248, 113, 113, 0.1));
  color: var(--theme-accent-error, #F87171);
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
</style>
