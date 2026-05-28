/**
 * 示例 Composable: usePagination
 * 通用分页逻辑封装
 */
import { ref, computed, watch, type Ref } from 'vue'

interface PaginationOptions {
  initialPage?: number
  initialPageSize?: number
  total?: Ref<number> | number
}

interface PaginationReturn {
  currentPage: Ref<number>
  pageSize: Ref<number>
  totalPages: Ref<number>
  hasNext: Ref<boolean>
  hasPrev: Ref<boolean>
  next: () => void
  prev: () => void
  goTo: (page: number) => void
  reset: () => void
}

export function usePagination(options: PaginationOptions = {}): PaginationReturn {
  const {
    initialPage = 1,
    initialPageSize = 10,
    total = 0
  } = options

  const currentPage = ref(initialPage)
  const pageSize = ref(initialPageSize)
  
  // 统一处理 total 为数字或 Ref
  const totalValue = computed(() => 
    typeof total === 'number' ? total : total.value
  )

  const totalPages = computed(() => 
    Math.max(1, Math.ceil(totalValue.value / pageSize.value))
  )

  const hasNext = computed(() => currentPage.value < totalPages.value)
  const hasPrev = computed(() => currentPage.value > 1)

  function next() {
    if (hasNext.value) {
      currentPage.value++
    }
  }

  function prev() {
    if (hasPrev.value) {
      currentPage.value--
    }
  }

  function goTo(page: number) {
    // 夹逼到有效范围
    const validPage = Math.max(1, Math.min(page, totalPages.value))
    currentPage.value = validPage
  }

  function reset() {
    currentPage.value = initialPage
  }

  // 当总页数变化时，确保当前页不超出范围
  watch(totalPages, (newTotal) => {
    if (currentPage.value > newTotal) {
      currentPage.value = newTotal
    }
  })

  return {
    currentPage,
    pageSize,
    totalPages,
    hasNext,
    hasPrev,
    next,
    prev,
    goTo,
    reset
  }
}
