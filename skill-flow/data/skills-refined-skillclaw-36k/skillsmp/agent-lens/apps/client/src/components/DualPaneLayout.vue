<template>
  <div class="dual-pane-container">
    <!-- Left Pane: Process Timeline -->
    <div
      class="process-pane"
      :style="{ width: leftPaneWidth + '%' }"
    >
      <div class="pane-header">
        <h2 class="pane-title">Process Timeline</h2>
        <div class="pane-controls">
          <button @click="collapseAll" class="control-btn" title="Collapse all">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M4 6L8 10L12 6" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </button>
          <button @click="expandAll" class="control-btn" title="Expand all">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M4 10L8 6L12 10" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </button>
        </div>
      </div>

      <div class="pane-content" ref="leftScrollContainer">
        <slot name="process-timeline"></slot>
      </div>
    </div>

    <!-- Resizer -->
    <div
      class="pane-resizer"
      @mousedown="startResize"
      @touchstart="startResize"
    >
      <div class="resizer-handle"></div>
    </div>

    <!-- Right Pane: Results & Metrics -->
    <div
      class="results-pane"
      :style="{ width: (100 - leftPaneWidth) + '%' }"
    >
      <div class="pane-header">
        <h2 class="pane-title">Results & Metrics</h2>
        <div class="tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="['tab', { active: activeTab === tab.id }]"
            @click="setActiveTab(tab.id)"
          >
            {{ tab.label }}
            <span v-if="tab.badge && tab.badge > 0" class="tab-badge">
              {{ tab.badge }}
            </span>
          </button>
        </div>
      </div>

      <div class="pane-content" ref="rightScrollContainer">
        <slot :name="'tab-' + activeTab"></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Tab {
  id: string;
  label: string;
  badge?: number;
}

const props = defineProps<{
  tabs: Tab[];
  defaultTab?: string;
  pendingHITLCount?: number;
}>();

const emit = defineEmits<{
  'collapse-all': [];
  'expand-all': [];
  'tab-change': [tabId: string];
}>();

// State
const leftPaneWidth = ref(40); // 40% default
const activeTab = ref(props.defaultTab || (props.tabs[0]?.id ?? 'metrics'));

// Pane resizing
let isResizing = false;

function startResize(e: MouseEvent | TouchEvent) {
  isResizing = true;
  document.addEventListener('mousemove', handleResize);
  document.addEventListener('mouseup', stopResize);
  document.addEventListener('touchmove', handleResize);
  document.addEventListener('touchend', stopResize);
  e.preventDefault();
}

function handleResize(e: MouseEvent | TouchEvent) {
  if (!isResizing) return;

  const container = document.querySelector('.dual-pane-container') as HTMLElement | null;
  if (!container) return;

  const containerRect = container.getBoundingClientRect();
  const clientX = 'touches' in e ? (e.touches[0]?.clientX ?? 0) : e.clientX;
  const newWidth = ((clientX - containerRect.left) / containerRect.width) * 100;

  // Clamp between 25% and 60%
  leftPaneWidth.value = Math.max(25, Math.min(60, newWidth));
}

function stopResize() {
  isResizing = false;
  document.removeEventListener('mousemove', handleResize);
  document.removeEventListener('mouseup', stopResize);
  document.removeEventListener('touchmove', handleResize);
  document.removeEventListener('touchend', stopResize);
}

// Controls
function collapseAll() {
  emit('collapse-all');
}

function expandAll() {
  emit('expand-all');
}

function setActiveTab(tabId: string) {
  activeTab.value = tabId;
  emit('tab-change', tabId);
}
</script>

<style scoped>
.dual-pane-container {
  display: flex;
  height: 100%;
  width: 100%;
  overflow: hidden;
  background: var(--theme-bg-primary, #0A0A0A);
}

.process-pane,
.results-pane {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.pane-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--theme-border-primary, #2A2A2A);
  background: var(--theme-bg-secondary, #141414);
  flex-shrink: 0;
}

.pane-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.pane-controls {
  display: flex;
  gap: 0.5rem;
}

.control-btn {
  padding: 0.375rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
  background: transparent;
  color: var(--theme-text-secondary, #B3B3B3);
  cursor: pointer;
  border-radius: 0.375rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.control-btn:hover {
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-color: var(--theme-primary, #BBA0FF);
  color: var(--theme-text-primary, #F5F5F5);
}

.pane-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 1rem 1.5rem;

  /* Custom scrollbar */
  scrollbar-width: thin;
  scrollbar-color: var(--theme-primary, #BBA0FF) transparent;
}

.pane-content::-webkit-scrollbar {
  width: 8px;
}

.pane-content::-webkit-scrollbar-track {
  background: transparent;
}

.pane-content::-webkit-scrollbar-thumb {
  background: var(--theme-primary, #BBA0FF);
  border-radius: 4px;
}

.pane-content::-webkit-scrollbar-thumb:hover {
  background: var(--theme-primary-hover, #D4C5FF);
}

/* Resizer */
.pane-resizer {
  width: 4px;
  background: var(--theme-border-primary, #2A2A2A);
  cursor: col-resize;
  transition: background 0.2s;
  flex-shrink: 0;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pane-resizer:hover {
  background: var(--theme-primary, #BBA0FF);
}

.resizer-handle {
  position: absolute;
  width: 12px;
  height: 100%;
  cursor: col-resize;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 0.5rem;
}

.tab {
  position: relative;
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: var(--theme-text-secondary, #B3B3B3);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  font-size: 0.875rem;
  font-weight: 500;
}

.tab:hover {
  color: var(--theme-text-primary, #F5F5F5);
}

.tab.active {
  color: var(--theme-text-primary, #F5F5F5);
  border-bottom-color: var(--theme-primary, #BBA0FF);
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.25rem;
  height: 1.25rem;
  padding: 0 0.375rem;
  margin-left: 0.5rem;
  font-size: 0.7rem;
  font-weight: 700;
  color: white;
  background: var(--theme-accent-error, #F87171);
  border-radius: 9999px;
  animation: pulse-badge 2s ease-in-out infinite;
}

@keyframes pulse-badge {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}
</style>
