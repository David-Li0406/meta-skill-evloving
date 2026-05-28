<template>
  <div class="skill-usage-panel">
    <div class="panel-header">
      <h3>🛠️ Skill Usage Breakdown</h3>
      <div v-if="hasData" class="summary">
        <span class="total">{{ totalInvocations }} invocations</span>
        <span class="divider">•</span>
        <span class="unique">{{ uniqueSkills }} unique skills</span>
      </div>
    </div>

    <div v-if="hasData" class="skills-container">
      <!-- Skill Cards -->
      <div class="skills-grid">
        <div
          v-for="(skill, i) in sortedSkills"
          :key="`skill-${i}`"
          class="skill-card"
          @mouseenter="onHover(skill, i)"
          @mouseleave="onLeave"
        >
          <div class="skill-header">
            <div class="skill-name">
              <span class="skill-icon">{{ getSkillIcon(skill.name) }}</span>
              <span class="name">{{ skill.name }}</span>
            </div>
            <div class="skill-count">{{ skill.count }}</div>
          </div>

          <div class="skill-bar-wrapper">
            <div
              class="skill-bar"
              :style="{
                width: skill.percentage + '%',
                background: getSkillColor(i)
              }"
            ></div>
          </div>

          <div class="skill-footer">
            <span class="percentage">{{ skill.percentage.toFixed(1) }}%</span>
            <span v-if="skill.averageDuration" class="duration">
              ⏱️ {{ formatDuration(skill.averageDuration) }}
            </span>
          </div>

          <!-- Events List (Expandable) -->
          <div v-if="skill.expanded" class="skill-events">
            <div class="events-header">Recent Invocations:</div>
            <div class="events-list">
              <div
                v-for="(event, j) in skill.events.slice(0, 5)"
                :key="`event-${j}`"
                class="event-item"
              >
                <span class="event-time">{{ formatTime(event.timestamp) }}</span>
                <span class="event-type">{{ event.hook_event_type }}</span>
              </div>
              <div v-if="skill.events.length > 5" class="more-events">
                +{{ skill.events.length - 5 }} more
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Timeline View -->
      <div class="timeline-section">
        <h4>Skill Invocation Timeline</h4>
        <div class="timeline">
          <div
            v-for="(point, i) in timelinePoints"
            :key="`point-${i}`"
            class="timeline-point"
            :style="{
              left: point.position + '%',
              background: point.color
            }"
            :title="`${point.skill} at ${formatTime(point.timestamp)}`"
          ></div>
        </div>
        <div class="timeline-labels">
          <span>{{ formatTime(timelineStart) }}</span>
          <span>{{ formatTime(timelineEnd) }}</span>
        </div>
      </div>
    </div>

    <div v-else class="no-data">
      <p>No skill invocations detected</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { HookEvent } from '../types';

const props = defineProps<{
  events: HookEvent[];
}>();

const hoveredSkill = ref<string | null>(null);

interface SkillData {
  name: string;
  count: number;
  percentage: number;
  events: HookEvent[];
  averageDuration?: number;
  expanded: boolean;
}

// Extract skill data from events
const skillsData = computed<SkillData[]>(() => {
  const skillMap = new Map<string, HookEvent[]>();

  props.events
    .filter(e => e.skill_name)
    .forEach(e => {
      const name = e.skill_name!;
      if (!skillMap.has(name)) {
        skillMap.set(name, []);
      }
      skillMap.get(name)!.push(e);
    });

  const total = props.events.filter(e => e.skill_name).length;

  return Array.from(skillMap.entries()).map(([name, events]) => ({
    name,
    count: events.length,
    percentage: total > 0 ? (events.length / total) * 100 : 0,
    events: events.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0)),
    averageDuration: calculateAverageDuration(events),
    expanded: false
  }));
});

const hasData = computed(() => skillsData.value.length > 0);
const totalInvocations = computed(() => skillsData.value.reduce((sum, s) => sum + s.count, 0));
const uniqueSkills = computed(() => skillsData.value.length);

// Sort by count descending
const sortedSkills = computed(() => {
  return [...skillsData.value].sort((a, b) => b.count - a.count);
});

// Timeline data
const timelineStart = computed(() => {
  const timestamps = props.events
    .filter(e => e.skill_name && e.timestamp)
    .map(e => e.timestamp!);
  return timestamps.length > 0 ? Math.min(...timestamps) : 0;
});

const timelineEnd = computed(() => {
  const timestamps = props.events
    .filter(e => e.skill_name && e.timestamp)
    .map(e => e.timestamp!);
  return timestamps.length > 0 ? Math.max(...timestamps) : 0;
});

const timelinePoints = computed(() => {
  const duration = timelineEnd.value - timelineStart.value;
  if (duration === 0) return [];

  return props.events
    .filter(e => e.skill_name && e.timestamp)
    .map((e, i) => {
      const position = ((e.timestamp! - timelineStart.value) / duration) * 100;
      const skillIndex = sortedSkills.value.findIndex(s => s.name === e.skill_name);
      return {
        skill: e.skill_name!,
        timestamp: e.timestamp!,
        position,
        color: getSkillColor(skillIndex)
      };
    });
});

// Skill icon mapping
function getSkillIcon(skillName: string): string {
  const lowerName = skillName.toLowerCase();
  if (lowerName.includes('search') || lowerName.includes('find')) return '🔍';
  if (lowerName.includes('write') || lowerName.includes('edit')) return '✏️';
  if (lowerName.includes('read') || lowerName.includes('view')) return '📖';
  if (lowerName.includes('test')) return '🧪';
  if (lowerName.includes('build') || lowerName.includes('compile')) return '🔨';
  if (lowerName.includes('deploy')) return '🚀';
  if (lowerName.includes('debug')) return '🐛';
  if (lowerName.includes('analyze') || lowerName.includes('research')) return '📊';
  return '⚙️';
}

// Color palette for skills
const skillColors = [
  '#BBA0FF', // Purple
  '#00D9FF', // Cyan
  '#FF6B9D', // Pink
  '#FFD93D', // Yellow
  '#4ADE80', // Green
  '#FB923C', // Orange
  '#60A5FA', // Blue
  '#F87171'  // Red
];

function getSkillColor(index: number): string {
  return skillColors[index % skillColors.length];
}

function calculateAverageDuration(events: HookEvent[]): number | undefined {
  const durations: number[] = [];
  
  for (const event of events) {
    if (event.children && event.children.length > 0) {
      const lastChild = props.events.find(e => e.event_id === event.children![event.children!.length - 1]);
      if (lastChild?.timestamp && event.timestamp) {
        durations.push(lastChild.timestamp - event.timestamp);
      }
    }
  }

  if (durations.length === 0) return undefined;
  return durations.reduce((a, b) => a + b, 0) / durations.length;
}

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000);
  return `${minutes}m ${seconds}s`;
}

function formatTime(timestamp: number | undefined): string {
  if (!timestamp) return 'N/A';
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

function onHover(skill: SkillData, index: number) {
  hoveredSkill.value = skill.name;
}

function onLeave() {
  hoveredSkill.value = null;
}
</script>

<style scoped>
.skill-usage-panel {
  background: var(--theme-bg-secondary, #141414);
  border-radius: 0.5rem;
  padding: 1.5rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.panel-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.summary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--theme-text-secondary, #B3B3B3);
}

.divider {
  color: var(--theme-text-tertiary, #808080);
}

.total,
.unique {
  font-weight: 600;
}

.skills-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.skill-card {
  background: var(--theme-bg-tertiary, #1E1E1E);
  border: 1px solid var(--theme-border-primary, #2A2A2A);
  border-radius: 0.5rem;
  padding: 1rem;
  transition: all 0.2s;
  cursor: pointer;
}

.skill-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border-color: var(--theme-primary, #BBA0FF);
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.skill-name {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.skill-icon {
  font-size: 1.25rem;
}

.name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
  font-family: 'JetBrains Mono', monospace;
}

.skill-count {
  font-size: 1rem;
  font-weight: 700;
  color: var(--theme-primary, #BBA0FF);
}

.skill-bar-wrapper {
  height: 0.5rem;
  background: var(--theme-bg-primary, #0A0A0A);
  border-radius: 0.25rem;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.skill-bar {
  height: 100%;
  transition: width 0.5s ease;
  border-radius: 0.25rem;
}

.skill-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
}

.percentage {
  color: var(--theme-text-secondary, #B3B3B3);
  font-weight: 600;
}

.duration {
  color: var(--theme-text-tertiary, #808080);
}

.skill-events {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--theme-border-primary, #2A2A2A);
}

.events-header {
  font-size: 0.75rem;
  color: var(--theme-text-secondary, #B3B3B3);
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.event-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: var(--theme-text-tertiary, #808080);
  font-family: 'JetBrains Mono', monospace;
}

.more-events {
  font-size: 0.7rem;
  color: var(--theme-primary, #BBA0FF);
  margin-top: 0.25rem;
  font-style: italic;
}

.timeline-section {
  background: var(--theme-bg-tertiary, #1E1E1E);
  border-radius: 0.5rem;
  padding: 1rem;
  border: 1px solid var(--theme-border-primary, #2A2A2A);
}

.timeline-section h4 {
  margin: 0 0 1rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--theme-text-primary, #F5F5F5);
}

.timeline {
  position: relative;
  height: 2rem;
  background: var(--theme-bg-primary, #0A0A0A);
  border-radius: 1rem;
  margin-bottom: 0.5rem;
  overflow: visible;
}

.timeline-point {
  position: absolute;
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border: 2px solid var(--theme-bg-tertiary, #1E1E1E);
  transition: all 0.2s;
  cursor: pointer;
}

.timeline-point:hover {
  width: 1rem;
  height: 1rem;
  filter: drop-shadow(0 0 6px currentColor);
  z-index: 10;
}

.timeline-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: var(--theme-text-tertiary, #808080);
  font-family: 'JetBrains Mono', monospace;
}

.no-data {
  padding: 4rem 2rem;
  text-align: center;
  color: var(--theme-text-tertiary, #808080);
  font-size: 0.875rem;
}
</style>
