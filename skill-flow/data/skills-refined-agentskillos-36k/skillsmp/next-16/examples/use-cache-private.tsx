'use cache: private'

import { cookies } from 'next/headers'
import { cacheLife, cacheTag } from 'next/cache'

// User-specific cached data (allows runtime APIs)
export async function getRecommendations(productId: string) {
  'use cache: private'
  cacheTag(`recs-${productId}`)
  cacheLife({ stale: 60 }) // min 30s required for runtime prefetch

  const session = (await cookies()).get('session')?.value || 'guest'
  return getPersonalizedRecs(productId, session)
}

// Dashboard with user-specific content
export async function DashboardStats() {
  'use cache: private'
  cacheTag('dashboard-stats')
  cacheLife({ stale: 30 })

  const userId = (await cookies()).get('userId')?.value
  return fetchUserStats(userId)
}

async function getPersonalizedRecs(productId: string, session: string) {
  // fetch personalized recommendations
  return []
}

async function fetchUserStats(userId: string | undefined) {
  // fetch user stats
  return {}
}
