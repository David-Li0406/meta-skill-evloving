# Vue API Pattern Examples

Concise examples showing key differences between Composition API and Options API.

## Table of Contents

1. [Basic Component](#1-basic-component)
2. [Props and Emits](#2-props-and-emits)
3. [Lifecycle and Data Fetching](#3-lifecycle-and-data-fetching)
4. [Computed Properties and Watchers](#4-computed-properties-and-watchers)
5. [External Logic (Composables vs Mixins)](#5-external-logic-composables-vs-mixins)
6. [Store Integration](#6-store-integration)
7. [Form with Validation](#7-form-with-validation)

**Style Convention**: All components use `scoped lang="scss"` with `@use '@/theme/' as *;`. Styles omitted after first example.

---

## 1. Basic Component

### Composition API

```vue
<template>
  <div class="greeting-card">
    <h2>{{ title }}</h2>
    <p>{{ message }}</p>
    <button @click="updateMessage">Update</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const title = ref('Welcome');
const message = ref('Hello from Composition API');

function updateMessage() {
  message.value = 'Message updated!';
}
</script>

<style scoped lang="scss">
@use '@/theme/' as *;

.greeting-card {
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
}
</style>
```

### Options API

```vue
<template>
  <div class="greeting-card">
    <h2>{{ title }}</h2>
    <p>{{ message }}</p>
    <button @click="updateMessage">Update</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'GreetingCard',
  
  data() {
    return {
      title: 'Welcome',
      message: 'Hello from Options API'
    };
  },
  
  methods: {
    updateMessage() {
      this.message = 'Message updated!';
    }
  }
});
</script>
<!-- Styles same as Composition API -->
```

---

## 2. Props and Emits

### Composition API

```vue
<template>
  <div class="user-card">
    <h3>{{ user.name }}</h3>
    <p>{{ user.email }}</p>
    <button @click="handleEdit" :disabled="readonly">Edit</button>
    <button @click="handleDelete" :disabled="readonly">Delete</button>
  </div>
</template>

<script setup lang="ts">
import type { User } from '@/interfaces/User';

interface Props {
  user: User;
  readonly?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  readonly: false
});

const emit = defineEmits<{
  edit: [userId: string];
  delete: [userId: string];
}>();

function handleEdit() {
  if (!props.readonly) emit('edit', props.user.id);
}

function handleDelete() {
  if (!props.readonly) emit('delete', props.user.id);
}
</script>
```

### Options API

```vue
<template>
  <div class="user-card">
    <h3>{{ user.name }}</h3>
    <p>{{ user.email }}</p>
    <button @click="handleEdit" :disabled="readonly">Edit</button>
    <button @click="handleDelete" :disabled="readonly">Delete</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import type { User } from '@/interfaces/User';

export default defineComponent({
  name: 'UserCard',
  
  props: {
    user: {
      type: Object as PropType<User>,
      required: true
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },
  
  emits: {
    edit: (userId: string) => typeof userId === 'string',
    delete: (userId: string) => typeof userId === 'string'
  },
  
  methods: {
    handleEdit() {
      if (!this.readonly) this.$emit('edit', this.user.id);
    },
    
    handleDelete() {
      if (!this.readonly) this.$emit('delete', this.user.id);
    }
  }
});
</script>
```

---

## 3. Lifecycle and Data Fetching

### Composition API

```vue
<template>
  <div class="data-fetcher">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <ul v-else>
      <li v-for="item in items" :key="item.id">{{ item.name }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { dataService } from '@/services/dataService';
import type { DataItem } from '@/interfaces/DataItem';

const items = ref<DataItem[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
let intervalId: number | null = null;

async function fetchData() {
  loading.value = true;
  error.value = null;
  
  try {
    items.value = await dataService.getAll();
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unknown error';
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchData();
  intervalId = window.setInterval(fetchData, 30000);
});

onBeforeUnmount(() => {
  if (intervalId !== null) clearInterval(intervalId);
});
</script>
```

### Options API

```vue
<template>
  <div class="data-fetcher">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <ul v-else>
      <li v-for="item in items" :key="item.id">{{ item.name }}</li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { dataService } from '@/services/dataService';
import type { DataItem } from '@/interfaces/DataItem';

export default defineComponent({
  name: 'DataFetcher',
  
  data() {
    return {
      items: [] as DataItem[],
      loading: false,
      error: null as string | null,
      intervalId: null as number | null
    };
  },
  
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      
      try {
        this.items = await dataService.getAll();
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Unknown error';
      } finally {
        this.loading = false;
      }
    }
  },
  
  mounted() {
    this.fetchData();
    this.intervalId = window.setInterval(this.fetchData, 30000);
  },
  
  beforeUnmount() {
    if (this.intervalId !== null) clearInterval(this.intervalId);
  }
});
</script>
```

---

## 4. Computed Properties and Watchers

### Composition API

```vue
<template>
  <div class="shopping-cart">
    <input v-model="searchQuery" placeholder="Search products..." />
    <h2>Cart ({{ itemCount }} items)</h2>
    <ul>
      <li v-for="item in filteredCart" :key="item.id">
        {{ item.name }} - ${{ item.price }} x {{ item.quantity }}
      </li>
    </ul>
    <div><strong>Total:</strong> ${{ total.toFixed(2) }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { CartItem } from '@/interfaces/CartItem';

const cart = ref<CartItem[]>([
  { id: '1', name: 'Product A', price: 29.99, quantity: 2 },
  { id: '2', name: 'Product B', price: 49.99, quantity: 1 }
]);

const searchQuery = ref('');

// Computed properties
const itemCount = computed(() => 
  cart.value.reduce((sum, item) => sum + item.quantity, 0)
);

const filteredCart = computed(() => {
  if (!searchQuery.value) return cart.value;
  return cart.value.filter(item => 
    item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const total = computed(() => 
  cart.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
);

// Watcher
watch(total, (newTotal, oldTotal) => {
  console.log(`Total changed from $${oldTotal} to $${newTotal}`);
});
</script>
```

### Options API

```vue
<template>
  <div class="shopping-cart">
    <input v-model="searchQuery" placeholder="Search products..." />
    <h2>Cart ({{ itemCount }} items)</h2>
    <ul>
      <li v-for="item in filteredCart" :key="item.id">
        {{ item.name }} - ${{ item.price }} x {{ item.quantity }}
      </li>
    </ul>
    <div><strong>Total:</strong> ${{ total.toFixed(2) }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { CartItem } from '@/interfaces/CartItem';

export default defineComponent({
  name: 'ShoppingCart',
  
  data() {
    return {
      cart: [
        { id: '1', name: 'Product A', price: 29.99, quantity: 2 },
        { id: '2', name: 'Product B', price: 49.99, quantity: 1 }
      ] as CartItem[],
      searchQuery: ''
    };
  },
  
  computed: {
    itemCount(): number {
      return this.cart.reduce((sum, item) => sum + item.quantity, 0);
    },
    
    filteredCart(): CartItem[] {
      if (!this.searchQuery) return this.cart;
      return this.cart.filter(item => 
        item.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    
    total(): number {
      return this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    }
  },
  
  watch: {
    total(newTotal: number, oldTotal: number) {
      console.log(`Total changed from $${oldTotal} to $${newTotal}`);
    }
  }
});
</script>
```

---

## 5. External Logic (Composables vs Mixins)

### Composition API (Composable)

**Composable: `src/composables/useAuth.ts`**
```typescript
import { ref, computed } from 'vue';
import type { User } from '@/interfaces/User';

export function useAuth() {
  const user = ref<User | null>(null);
  const loading = ref(false);
  
  const isAuthenticated = computed(() => user.value !== null);
  
  async function login(username: string, password: string) {
    loading.value = true;
    try {
      user.value = { id: '1', name: username, email: `${username}@example.com` };
    } finally {
      loading.value = false;
    }
  }
  
  function logout() {
    user.value = null;
  }
  
  return { user, loading, isAuthenticated, login, logout };
}
```

**Component:**
```vue
<template>
  <div class="auth-status">
    <div v-if="isAuthenticated">
      <p>Welcome, {{ user?.name }}</p>
      <button @click="logout">Logout</button>
    </div>
    <button v-else @click="showLogin">Login</button>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '@/composables/useAuth';

const { user, isAuthenticated, logout } = useAuth();

function showLogin() {
  // Show login dialog
}
</script>
```

### Options API (Mixin)

**Mixin: `src/mixins/authMixin.ts`**
```typescript
import { defineComponent } from 'vue';
import type { User } from '@/interfaces/User';

export const authMixin = defineComponent({
  data() {
    return {
      user: null as User | null,
      loading: false
    };
  },
  
  computed: {
    isAuthenticated(): boolean {
      return this.user !== null;
    }
  },
  
  methods: {
    async login(username: string, password: string) {
      this.loading = true;
      try {
        this.user = { id: '1', name: username, email: `${username}@example.com` };
      } finally {
        this.loading = false;
      }
    },
    
    logout() {
      this.user = null;
    }
  }
});
```

**Component:**
```vue
<template>
  <div class="auth-status">
    <div v-if="isAuthenticated">
      <p>Welcome, {{ user?.name }}</p>
      <button @click="logout">Logout</button>
    </div>
    <button v-else @click="showLogin">Login</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { authMixin } from '@/mixins/authMixin';

export default defineComponent({
  name: 'AuthStatus',
  mixins: [authMixin],
  
  methods: {
    showLogin() {
      // Show login dialog
    }
  }
});
</script>
```

---

## 6. Store Integration

### Pinia (Recommended for Vue 3)

**Composition API:**
```vue
<script setup lang="ts">
import { computed } from 'vue';
import { useUserStore } from '@/stores/userStore';

const userStore = useUserStore();
const currentUser = computed(() => userStore.currentUser);
const loading = computed(() => userStore.loading);

async function handleUpdate() {
  await userStore.updateProfile({ name: 'Updated Name' });
}
</script>
```

**Options API:**
```vue
<script lang="ts">
import { defineComponent } from 'vue';
import { mapState, mapActions } from 'pinia';
import { useUserStore } from '@/stores/userStore';

export default defineComponent({
  computed: {
    ...mapState(useUserStore, ['currentUser', 'loading'])
  },
  
  methods: {
    ...mapActions(useUserStore, ['updateProfile']),
    
    async handleUpdate() {
      await this.updateProfile({ name: 'Updated Name' });
    }
  }
});
</script>
```

### Vuex (Vue 2 Legacy)

**Composition API:**
```vue
<script setup lang="ts">
import { computed } from 'vue';
import { useStore } from 'vuex';
import type { RootState } from '@/store';

const store = useStore<RootState>();
const currentUser = computed(() => store.state.user.currentUser);
const loading = computed(() => store.state.user.loading);

async function handleUpdate() {
  await store.dispatch('user/updateProfile', { name: 'Updated Name' });
}
</script>
```

**Options API:**
```vue
<script lang="ts">
import { defineComponent } from 'vue';
import { mapState, mapActions } from 'vuex';

export default defineComponent({
  computed: {
    ...mapState('user', ['currentUser', 'loading'])
  },
  
  methods: {
    ...mapActions('user', ['updateProfile']),
    
    async handleUpdate() {
      await this.updateProfile({ name: 'Updated Name' });
    }
  }
});
</script>
```

---

## 7. Form with Validation

### Composition API

```vue
<template>
  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="username">Username</label>
      <input id="username" v-model="form.username" @blur="validateUsername" />
      <span v-if="errors.username" class="error">{{ errors.username }}</span>
    </div>
    
    <div class="form-group">
      <label for="email">Email</label>
      <input id="email" v-model="form.email" type="email" @blur="validateEmail" />
      <span v-if="errors.email" class="error">{{ errors.email }}</span>
    </div>
    
    <div class="form-group">
      <label for="password">Password</label>
      <input id="password" v-model="form.password" type="password" @blur="validatePassword" />
      <span v-if="errors.password" class="error">{{ errors.password }}</span>
    </div>
    
    <button type="submit" :disabled="!isFormValid || submitting">
      {{ submitting ? 'Submitting...' : 'Register' }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '@/services/authService';

const router = useRouter();

const form = reactive({
  username: '',
  email: '',
  password: ''
});

const errors = reactive({
  username: '',
  email: '',
  password: ''
});

const submitting = ref(false);

const isFormValid = computed(() => {
  return form.username && form.email && form.password &&
         !errors.username && !errors.email && !errors.password;
});

function validateUsername() {
  if (!form.username) {
    errors.username = 'Username is required';
  } else if (form.username.length < 3) {
    errors.username = 'Username must be at least 3 characters';
  } else {
    errors.username = '';
  }
}

function validateEmail() {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!form.email) {
    errors.email = 'Email is required';
  } else if (!emailRegex.test(form.email)) {
    errors.email = 'Invalid email format';
  } else {
    errors.email = '';
  }
}

function validatePassword() {
  if (!form.password) {
    errors.password = 'Password is required';
  } else if (form.password.length < 8) {
    errors.password = 'Password must be at least 8 characters';
  } else {
    errors.password = '';
  }
}

async function handleSubmit() {
  validateUsername();
  validateEmail();
  validatePassword();
  
  if (!isFormValid.value) return;
  
  submitting.value = true;
  try {
    await authService.register(form);
    router.push('/login');
  } catch (err) {
    console.error('Registration failed:', err);
  } finally {
    submitting.value = false;
  }
}
</script>
```

### Options API

```vue
<template>
  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="username">Username</label>
      <input id="username" v-model="form.username" @blur="validateUsername" />
      <span v-if="errors.username" class="error">{{ errors.username }}</span>
    </div>
    
    <div class="form-group">
      <label for="email">Email</label>
      <input id="email" v-model="form.email" type="email" @blur="validateEmail" />
      <span v-if="errors.email" class="error">{{ errors.email }}</span>
    </div>
    
    <div class="form-group">
      <label for="password">Password</label>
      <input id="password" v-model="form.password" type="password" @blur="validatePassword" />
      <span v-if="errors.password" class="error">{{ errors.password }}</span>
    </div>
    
    <button type="submit" :disabled="!isFormValid || submitting">
      {{ submitting ? 'Submitting...' : 'Register' }}
    </button>
  </form>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { authService } from '@/services/authService';

export default defineComponent({
  name: 'RegistrationForm',
  
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: ''
      },
      errors: {
        username: '',
        email: '',
        password: ''
      },
      submitting: false
    };
  },
  
  computed: {
    isFormValid(): boolean {
      return this.form.username && this.form.email && this.form.password &&
             !this.errors.username && !this.errors.email && !this.errors.password;
    }
  },
  
  methods: {
    validateUsername() {
      if (!this.form.username) {
        this.errors.username = 'Username is required';
      } else if (this.form.username.length < 3) {
        this.errors.username = 'Username must be at least 3 characters';
      } else {
        this.errors.username = '';
      }
    },
    
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.form.email) {
        this.errors.email = 'Email is required';
      } else if (!emailRegex.test(this.form.email)) {
        this.errors.email = 'Invalid email format';
      } else {
        this.errors.email = '';
      }
    },
    
    validatePassword() {
      if (!this.form.password) {
        this.errors.password = 'Password is required';
      } else if (this.form.password.length < 8) {
        this.errors.password = 'Password must be at least 8 characters';
      } else {
        this.errors.password = '';
      }
    },
    
    async handleSubmit() {
      this.validateUsername();
      this.validateEmail();
      this.validatePassword();
      
      if (!this.isFormValid) return;
      
      this.submitting = true;
      try {
        await authService.register(this.form);
        this.$router.push('/login');
      } catch (err) {
        console.error('Registration failed:', err);
      } finally {
        this.submitting = false;
      }
    }
  }
});
</script>
```

---

## Summary

**Key Differences**:
- **Composition API**: `<script setup>`, `ref()`, `reactive()`, composables
- **Options API**: `data()`, `methods`, `computed`, mixins

**TypeScript**: Always use `lang="ts"` in script tags and define interfaces for props/data

**Styles**: Always use `scoped lang="scss"` with `@use '@/theme/' as *;`

**Recommendation**: Composition API for new Vue 3 projects (better TypeScript support, code reusability, tree-shaking)
