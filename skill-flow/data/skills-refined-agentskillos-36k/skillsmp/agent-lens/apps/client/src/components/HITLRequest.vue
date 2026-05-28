<template>
  <div class="hitl-request" :class="{ 'timeout-warning': isNearTimeout, 'timeout-critical': isCritical }">
    <!-- Header with urgency indicator -->
    <div class="request-header">
      <div class="request-type">
        <span class="type-badge" :class="requestTypeLowercase">
          {{ requestTypeIcon }} {{ requestType }}
        </span>
        <span class="request-title">{{ requestTitle }}</span>
      </div>

      <div class="timeout-indicator">
        <svg
          class="countdown-ring"
          width="36"
          height="36"
        >
          <circle
            cx="18"
            cy="18"
            r="16"
            fill="none"
            stroke="var(--theme-border-primary)"
            stroke-width="2.5"
          />
          <circle
            cx="18"
            cy="18"
            r="16"
            fill="none"
            :stroke="timeoutColor"
            stroke-width="2.5"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="countdownOffset"
            transform="rotate(-90 18 18)"
            class="countdown-progress"
          />
        </svg>
        <span class="timeout-text" :class="{ critical: isCritical }">
          {{ formattedTimeRemaining }}
        </span>
      </div>
    </div>

    <!-- Question/Context -->
    <div class="request-body">
      <p class="question">{{ questionText }}</p>

      <!-- Choices (if multiple choice) -->
      <div v-if="hasChoices" class="choices-list">
        <div
          v-for="(choice, index) in choices"
          :key="index"
          class="choice-option"
          :class="{ selected: selectedChoice === choice }"
          @click="selectedChoice = choice"
        >
          <input
            type="radio"
            :id="`choice-${request.hookEvent.event_id}-${index}`"
            :value="choice"
            v-model="selectedChoice"
          />
          <label :for="`choice-${request.hookEvent.event_id}-${index}`">{{ choice }}</label>
        </div>
      </div>

      <!-- Text input (if permission or open question) -->
      <div v-if="requiresTextInput" class="text-input-container">
        <label class="input-label">{{ textInputLabel }}</label>
        <textarea
          v-model="textResponse"
          :placeholder="textPlaceholder"
          class="response-textarea"
          rows="3"
        ></textarea>
      </div>

      <!-- Context/Screenshot (if available) -->
      <div v-if="hasContext" class="context-section">
        <button class="btn-link" @click="showContext = !showContext">
          <span>{{ showContext ? '▼' : '▶' }}</span>
          {{ showContext ? 'Hide' : 'View' }} Context
        </button>
        <div v-if="showContext" class="context-content">
          <pre>{{ contextText }}</pre>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="request-actions">
      <button
        class="btn btn-reject"
        @click="handleReject"
        title="Reject this request"
      >
        <span class="btn-icon">✕</span>
        <span class="btn-label">Reject</span>
      </button>

      <button
        class="btn btn-edit"
        @click="handleEdit"
        :disabled="!canEdit"
        title="Edit and approve with modifications"
      >
        <span class="btn-icon">✏️</span>
        <span class="btn-label">Edit</span>
      </button>

      <button
        class="btn btn-approve"
        @click="handleApprove"
        :disabled="!canApprove"
        title="Approve this request"
      >
        <span class="btn-icon">✓</span>
        <span class="btn-label">Approve</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import type { HookEvent } from '../types';

interface HITLRequestData {
  hookEvent: HookEvent;
  receivedAt: number;
}

const props = defineProps<{
  request: HITLRequestData;
}>();

const emit = defineEmits<{
  approve: [response?: string];
  edit: [response: string];
  reject: [];
}>();

// State
const selectedChoice = ref<string | null>(null);
const textResponse = ref('');
const showContext = ref(false);
const currentTime = ref(Date.now());

// Update current time every second for countdown
let intervalId: number;
onMounted(() => {
  intervalId = window.setInterval(() => {
    currentTime.value = Date.now();
  }, 1000);
});

onUnmounted(() => {
  clearInterval(intervalId);
});

// Computed properties
const hitl = computed(() => props.request.hookEvent.humanInTheLoop);

const requestType = computed(() => {
  const type = hitl.value?.type || 'question';
  return type.charAt(0).toUpperCase() + type.slice(1);
});

const requestTypeLowercase = computed(() => hitl.value?.type || 'question');

const requestTypeIcon = computed(() => {
  const icons: Record<string, string> = {
    permission: '🔐',
    question: '❓',
    choice: '🎯'
  };
  return icons[requestTypeLowercase.value] || '🤖';
});

const questionText = computed(() => hitl.value?.question || 'Approval required');

const requestTitle = computed(() => {
  if (requestTypeLowercase.value === 'permission') return 'Permission Required';
  if (requestTypeLowercase.value === 'choice') return 'Choose an Option';
  return 'Question';
});

const hasChoices = computed(() => {
  return requestTypeLowercase.value === 'choice' && (hitl.value?.choices?.length || 0) > 0;
});

const choices = computed(() => hitl.value?.choices || []);

const requiresTextInput = computed(() => {
  return requestTypeLowercase.value === 'question' || requestTypeLowercase.value === 'permission';
});

const textInputLabel = computed(() => {
  if (requestTypeLowercase.value === 'permission') {
    return 'Conditions or modifications (optional):';
  }
  return 'Your response:';
});

const textPlaceholder = computed(() => {
  if (requestTypeLowercase.value === 'permission') {
    return 'Optional: Provide conditions or modifications...';
  }
  return 'Enter your response here...';
});

const hasContext = computed(() => {
  return props.request.hookEvent.payload !== undefined &&
         Object.keys(props.request.hookEvent.payload).length > 0;
});

const contextText = computed(() => {
  return JSON.stringify(props.request.hookEvent.payload, null, 2);
});

// Timeout calculations
const timeout = computed(() => hitl.value?.timeout || 300); // Default 5 minutes
const elapsedSeconds = computed(() =>
  Math.floor((currentTime.value - props.request.receivedAt) / 1000)
);
const remainingSeconds = computed(() =>
  Math.max(0, timeout.value - elapsedSeconds.value)
);

const formattedTimeRemaining = computed(() => {
  const mins = Math.floor(remainingSeconds.value / 60);
  const secs = remainingSeconds.value % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
});

const isNearTimeout = computed(() => remainingSeconds.value < 60 && remainingSeconds.value >= 30);
const isCritical = computed(() => remainingSeconds.value < 30);

const timeoutColor = computed(() => {
  const ratio = remainingSeconds.value / timeout.value;
  if (ratio > 0.5) return 'var(--theme-accent-success, #4ADE80)';
  if (ratio > 0.2) return 'var(--theme-accent-warning, #FBBF24)';
  return 'var(--theme-accent-error, #F87171)';
});

const circumference = 2 * Math.PI * 16; // 2πr where r=16

const countdownOffset = computed(() => {
  const ratio = remainingSeconds.value / timeout.value;
  return circumference * (1 - ratio);
});

// Validation
const canApprove = computed(() => {
  if (hasChoices.value) {
    return selectedChoice.value !== null;
  }
  // For permissions, can approve without text
  return true;
});

const canEdit = computed(() => {
  if (hasChoices.value) {
    return selectedChoice.value !== null && textResponse.value.trim().length > 0;
  }
  return textResponse.value.trim().length > 0;
});

// Actions
function handleApprove() {
  if (!canApprove.value) return;

  const response = hasChoices.value ? selectedChoice.value! : textResponse.value;
  emit('approve', response || undefined);
}

function handleEdit() {
  if (!canEdit.value) return;

  const response = hasChoices.value
    ? `${selectedChoice.value} (${textResponse.value})`
    : textResponse.value;

  emit('edit', response);
}

function handleReject() {
  emit('reject');
}
</script>

<style scoped>
.hitl-request {
  background: var(--theme-bg-secondary, #141414);
  border: 2px solid var(--theme-primary, #BBA0FF);
  border-radius: 0.75rem;
  padding: 1.5rem;
  animation: slideIn 0.3s ease-out;
  box-shadow: 0 0 20px rgba(187, 160, 255, 0.2);
}

.hitl-request.timeout-warning {
  border-color: var(--theme-accent-warning, #FBBF24);
  box-shadow: 0 0 20px rgba(251, 191, 36, 0.3);
}

.hitl-request.timeout-critical {
  border-color: var(--theme-accent-error, #F87171);
  box-shadow: 0 0 25px rgba(248, 113, 113, 0.4);
  animation: pulse-critical 1.5s ease-in-out infinite, slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse-critical {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.01);
  }
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
  gap: 1rem;
}

.request-type {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.type-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.875rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  border-radius: 0.375rem;
  width: fit-content;
  letter-spacing: 0.05em;
}

.type-badge.permission {
  background: var(--theme-warning-bg, rgba(251, 191, 36, 0.1));
  color: var(--theme-accent-warning, #FBBF24);
  border: 1px solid var(--theme-accent-warning, #FBBF24);
}

.type-badge.question {
  background: rgba(187, 160, 255, 0.1);
  color: var(--theme-primary, #BBA0FF);
  border: 1px solid var(--theme-primary, #BBA0FF);
}

.type-badge.choice {
  background: var(--theme-success-bg, rgba(74, 222, 128, 0.1));
  color: var(--theme-accent-success, #4ADE80);
  border: 1px solid var(--theme-accent-success, #4ADE80);
}

.request-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--theme-text-secondary, #B3B3B3);
}

.timeout-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.375rem;
  flex-shrink: 0;
}

.countdown-ring {
  position: relative;
}

.countdown-progress {
  transition: stroke-dashoffset 1s linear;
}

.timeout-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--theme-text-primary, #F5F5F5);
}

.timeout-text.critical {
  color: var(--theme-accent-error, #F87171);
  animation: blink 1s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.request-body {
  margin-bottom: 1.5rem;
}

.question {
  font-size: 1.0625rem;
  color: var(--theme-text-primary, #F5F5F5);
  margin-bottom: 1.25rem;
  line-height: 1.6;
  font-weight: 500;
}

.choices-list {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  margin-bottom: 1rem;
}

.choice-option {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem 1rem;
  border: 1.5px solid var(--theme-border-primary, #2A2A2A);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--theme-bg-primary, #0A0A0A);
}

.choice-option:hover {
  border-color: var(--theme-primary, #BBA0FF);
  background: var(--theme-bg-tertiary, #1E1E1E);
}

.choice-option.selected {
  border-color: var(--theme-primary, #BBA0FF);
  background: rgba(187, 160, 255, 0.1);
  box-shadow: 0 0 15px rgba(187, 160, 255, 0.3);
}

.choice-option input[type="radio"] {
  cursor: pointer;
  accent-color: var(--theme-primary, #BBA0FF);
}

.choice-option label {
  cursor: pointer;
  flex: 1;
  color: var(--theme-text-primary, #F5F5F5);
  font-size: 0.9375rem;
}

.text-input-container {
  margin-bottom: 1rem;
}

.input-label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: var(--theme-text-secondary, #B3B3B3);
  font-weight: 500;
}

.response-textarea {
  width: 100%;
  padding: 0.875rem;
  border: 1.5px solid var(--theme-border-primary, #2A2A2A);
  border-radius: 0.5rem;
  background: var(--theme-bg-primary, #0A0A0A);
  color: var(--theme-text-primary, #F5F5F5);
  font-family: inherit;
  font-size: 0.9375rem;
  resize: vertical;
  transition: border-color 0.2s, box-shadow 0.2s;
  line-height: 1.5;
}

.response-textarea:focus {
  outline: none;
  border-color: var(--theme-primary, #BBA0FF);
  box-shadow: 0 0 10px rgba(187, 160, 255, 0.3);
}

.response-textarea::placeholder {
  color: var(--theme-text-quaternary, #666666);
}

.context-section {
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--theme-border-primary, #2A2A2A);
}

.btn-link {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0;
  border: none;
  background: transparent;
  color: var(--theme-primary, #BBA0FF);
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.2s;
}

.btn-link:hover {
  color: var(--theme-primary-hover, #D4C5FF);
  text-decoration: underline;
}

.context-content {
  margin-top: 0.75rem;
  padding: 1rem;
  background: var(--theme-bg-primary, #0A0A0A);
  border-radius: 0.5rem;
  max-height: 250px;
  overflow-y: auto;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.context-content pre {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--theme-text-secondary, #B3B3B3);
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'JetBrains Mono', monospace;
}

.request-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9375rem;
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  filter: grayscale(0.5);
}

.btn-icon {
  font-size: 1.125rem;
  line-height: 1;
}

.btn-label {
  font-weight: 600;
}

.btn-reject {
  background: var(--theme-error-bg, rgba(248, 113, 113, 0.1));
  color: var(--theme-accent-error, #F87171);
  border: 1px solid var(--theme-accent-error, #F87171);
}

.btn-reject:hover:not(:disabled) {
  background: var(--theme-accent-error, #F87171);
  color: #0A0A0A;
  box-shadow: 0 0 15px rgba(248, 113, 113, 0.4);
}

.btn-edit {
  background: var(--theme-bg-tertiary, #1E1E1E);
  color: var(--theme-text-primary, #F5F5F5);
  border: 1px solid var(--theme-border-secondary, #3D3D3D);
}

.btn-edit:hover:not(:disabled) {
  background: var(--theme-bg-quaternary, #282828);
  border-color: var(--theme-primary, #BBA0FF);
  box-shadow: 0 0 10px rgba(187, 160, 255, 0.2);
}

.btn-approve {
  background: var(--theme-accent-success, #4ADE80);
  color: #0A0A0A;
  border: 1px solid var(--theme-accent-success, #4ADE80);
}

.btn-approve:hover:not(:disabled) {
  filter: brightness(1.1);
  box-shadow: 0 0 20px rgba(74, 222, 128, 0.5);
  transform: translateY(-1px);
}

.btn-approve:active:not(:disabled) {
  transform: translateY(0);
}
</style>
