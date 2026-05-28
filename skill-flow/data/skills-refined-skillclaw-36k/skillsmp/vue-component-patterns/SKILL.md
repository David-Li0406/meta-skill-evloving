---
name: vue-component-patterns
description: Vue.js 2.7 组件开发模式，包含 Element UI 使用、状态管理、表单处理和最佳实践。在创建或修改 Vue 组件时使用。
---

# Vue.js 组件开发模式

## When to Use

- 创建新的 Vue 组件
- 修改现有 Vue 组件
- 处理表单和用户输入
- 管理组件状态
- 与 Element UI 组件交互

## 核心模式

### 组件结构

```vue
<template>
  <div class="component-name">
    <!-- 模板内容 -->
  </div>
</template>

<script>
export default {
  name: 'ComponentName',

  components: {},

  props: {},

  data() {
    return {}
  },

  computed: {},

  watch: {},

  created() {},

  mounted() {},

  methods: {}
}
</script>

<style lang="scss" scoped>
.component-name {
  // 样式
}
</style>
```

### 状态管理

#### 使用 Vuex
```javascript
import { mapState, mapActions } from 'vuex'

export default {
  computed: {
    ...mapState('workorder', ['workorders', 'loading'])
  },

  methods: {
    ...mapActions('workorder', ['fetchWorkorders'])
  }
}
```

#### 本地状态
```javascript
data() {
  return {
    list: [],
    loading: false,
    error: null
  }
}
```

### 表单处理

#### Element UI 表单
```vue
<template>
  <el-form ref="form" :model="form" :rules="rules" label-width="120px">
    <el-form-item label="字段名" prop="field">
      <el-input v-model="form.field" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm">提交</el-button>
      <el-button @click="resetForm">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    return {
      form: {
        field: ''
      },
      rules: {
        field: [
          { required: true, message: '请输入字段', trigger: 'blur' }
        ]
      }
    }
  },

  methods: {
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          // 提交逻辑
        }
      })
    },

    resetForm() {
      this.$refs.form.resetFields()
    }
  }
}
</script>
```

### 表格处理

```vue
<template>
  <el-table :data="tableData" v-loading="loading" border>
    <el-table-column prop="id" label="ID" width="80" />
    <el-table-column prop="name" label="名称" />
    <el-table-column label="操作" width="200">
      <template slot-scope="scope">
        <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
        <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
```

### API 调用

```javascript
import { getWorkorders, createWorkorder } from '@/api/workorder'

export default {
  data() {
    return {
      workorders: [],
      loading: false
    }
  },

  methods: {
    async fetchWorkorders() {
      this.loading = true
      try {
        const res = await getWorkorders()
        this.workorders = res.data
      } catch (error) {
        this.$message.error('获取数据失败')
      } finally {
        this.loading = false
      }
    },

    async createWorkorder(data) {
      try {
        await createWorkorder(data)
        this.$message.success('创建成功')
        this.fetchWorkorders()
      } catch (error) {
        this.$message.error('创建失败')
      }
    }
  }
}
```

## 错误处理

### 统一错误处理
```javascript
// 在 axios 拦截器中处理
this.$message.error(error.message || '操作失败')
```

### 加载状态
```javascript
async fetchData() {
  this.loading = true
  try {
    // API 调用
  } finally {
    this.loading = false
  }
}
```

## 最佳实践

### 1. 组件命名
- 使用 PascalCase：`WorkOrderList.vue`
- 组件 name 属性与文件名一致

### 2. Props 定义
```javascript
props: {
  workorderId: {
    type: Number,
    required: true
  },
  title: {
    type: String,
    default: ''
  }
}
```

### 3. 事件命名
```javascript
// 使用 kebab-case
this.$emit('update-success')
this.$emit('item-change', { id: 1 })
```

### 4. 样式作用域
```vue
<style lang="scss" scoped>
// 始终使用 scoped 避免样式污染
</style>
```

### 5. 空状态处理
```vue
<el-empty v-if="!list.length" description="暂无数据" />
<div v-else>
  <!-- 列表内容 -->
</div>
```

## Element UI 常用组件

### Dialog 对话框
```vue
<el-dialog title="标题" :visible.sync="dialogVisible" width="50%">
  <!-- 内容 -->
  <span slot="footer">
    <el-button @click="dialogVisible = false">取消</el-button>
    <el-button type="primary" @click="handleConfirm">确定</el-button>
  </span>
</el-dialog>
```

### Pagination 分页
```vue
<el-pagination
  @size-change="handleSizeChange"
  @current-change="handleCurrentChange"
  :current-page="page"
  :page-sizes="[10, 20, 50, 100]"
  :page-size="pageSize"
  :total="total"
  layout="total, sizes, prev, pager, next, jumper"
/>
```

### 日期选择器
```vue
<el-date-picker
  v-model="dateRange"
  type="daterange"
  range-separator="至"
  start-placeholder="开始日期"
  end-placeholder="结束日期"
/>
```

## 路由使用

### 路由跳转
```javascript
// 声明式导航
<router-link :to="{ name: 'WorkOrderDetail', params: { id: item.id } }">

// 编程式导航
this.$router.push({ name: 'WorkOrderDetail', params: { id: 1 } })
this.$router.push({ path: '/workorders', query: { status: 'pending' } })
```

### 获取路由参数
```javascript
// 在组件中
const id = this.$route.params.id
const query = this.$route.query

// 在路由守卫中
beforeRouteEnter(to, from, next) {
  next(vm => {
    vm.id = to.params.id
  })
}
```

## 生命周期

```javascript
created() {
  // 组件创建后，可以访问 data、computed
  this.fetchData()
},

mounted() {
  // DOM 挂载后，可以访问 DOM 元素
},

beforeDestroy() {
  // 清理工作（取消事件监听、定时器等）
}
```

## 相关技能

- `django-api-patterns` - 后端 API 开发
- `systematic-debugging` - 调试问题
- `testing-patterns` - 编写测试
