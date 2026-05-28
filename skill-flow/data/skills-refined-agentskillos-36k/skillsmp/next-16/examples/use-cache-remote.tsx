'use cache: remote'

import { cacheLife, cacheTag } from 'next/cache'

// Shared across serverless instances via external KV storage
// No runtime APIs allowed (same as 'use cache')

export async function getGlobalStats() {
  'use cache: remote'
  cacheTag('global-stats')
  cacheLife({ expire: 60 })

  return db.analytics.aggregate({ users: 'count', revenue: 'sum' })
}

export async function getPopularProducts() {
  'use cache: remote'
  cacheTag('popular-products')
  cacheLife('hours')

  return db.products.findMany({
    orderBy: { views: 'desc' },
    take: 10,
  })
}

// Placeholder for db
declare const db: {
  analytics: { aggregate: (query: object) => Promise<object> }
  products: { findMany: (query: object) => Promise<object[]> }
}
