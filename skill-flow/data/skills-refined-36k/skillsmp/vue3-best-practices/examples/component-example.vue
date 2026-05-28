<script setup lang="ts">
/**
 * 递归树形组件示例
 * 展示：组件命名、递归组件、Props/Emits/Slots 最佳实践
 */
import { computed } from 'vue'

// ========== 组件命名 ==========
// 递归组件必须显式命名，否则无法在模板中引用自身
defineOptions({
  name: 'TreeNode'
})

// ========== 类型定义 ==========
export interface TreeItem {
  id: string | number
  label: string
  children?: TreeItem[]
  disabled?: boolean
}

// ========== Props ==========
const props = withDefaults(defineProps<{
  /** 树节点数据 */
  node: TreeItem
  /** 当前层级深度 */
  depth?: number
  /** 展开的节点 ID 集合 */
  expandedKeys?: Set<string | number>
  /** 选中的节点 ID */
  selectedKey?: string | number | null
}>(), {
  depth: 0,
  // 默认值用工厂函数，避免共享引用
  expandedKeys: () => new Set()
})

// ========== Emits ==========
const emit = defineEmits<{
  /** 节点选中事件 */
  select: [node: TreeItem]
  /** 节点展开/收起事件 */
  toggle: [nodeId: string | number, expanded: boolean]
}>()

// ========== Computed ==========
const hasChildren = computed(() => 
  props.node.children && props.node.children.length > 0
)

const isExpanded = computed(() => 
  props.expandedKeys?.has(props.node.id)
)

const isSelected = computed(() => 
  props.selectedKey === props.node.id
)

const nodeStyle = computed(() => ({
  paddingLeft: `${props.depth * 16}px`
}))

// ========== Methods ==========
function handleSelect() {
  if (props.node.disabled) return
  emit('select', props.node)
}

function handleToggle() {
  if (!hasChildren.value) return
  emit('toggle', props.node.id, !isExpanded.value)
}

// 转发子节点事件（保持事件冒泡）
function handleChildSelect(node: TreeItem) {
  emit('select', node)
}

function handleChildToggle(nodeId: string | number, expanded: boolean) {
  emit('toggle', nodeId, expanded)
}
</script>

<template>
  <div class="tree-node">
    <!-- 当前节点 -->
    <div
      :class="[
        'node-content',
        { 
          selected: isSelected,
          disabled: node.disabled,
          expandable: hasChildren
        }
      ]"
      :style="nodeStyle"
      @click="handleSelect"
    >
      <!-- 展开/收起图标 -->
      <span 
        v-if="hasChildren"
        class="toggle-icon"
        @click.stop="handleToggle"
      >
        {{ isExpanded ? '▼' : '▶' }}
      </span>
      <span v-else class="toggle-placeholder" />
      
      <!-- 节点内容插槽 -->
      <slot name="node" :node="node" :depth="depth">
        <span class="node-label">{{ node.label }}</span>
      </slot>
    </div>

    <!-- 递归渲染子节点 -->
    <template v-if="hasChildren && isExpanded">
      <!-- 
        ⭐ 递归组件关键点：
        1. 使用 defineOptions({ name: 'TreeNode' }) 命名
        2. 在模板中用 <TreeNode> 引用自身
        3. 传递 depth + 1 控制缩进层级
      -->
      <TreeNode
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        :depth="depth + 1"
        :expanded-keys="expandedKeys"
        :selected-key="selectedKey"
        @select="handleChildSelect"
        @toggle="handleChildToggle"
      >
        <!-- 透传插槽给子节点 -->
        <template #node="slotProps">
          <slot name="node" v-bind="slotProps" />
        </template>
      </TreeNode>
    </template>
  </div>
</template>

<style scoped>
.tree-node {
  user-select: none;
}

.node-content {
  display: flex;
  align-items: center;
  padding: 6px 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.node-content:hover:not(.disabled) {
  background-color: #f5f5f5;
}

.node-content.selected {
  background-color: #e6f7ff;
  color: #1890ff;
}

.node-content.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.toggle-icon,
.toggle-placeholder {
  width: 16px;
  height: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 4px;
  font-size: 10px;
  color: #999;
}

.toggle-icon:hover {
  color: #1890ff;
}

.node-label {
  flex: 1;
}
</style>
