/**
 * BMAP API client for querying BSocial data
 */

const BMAP_API_BASE = "https://bmap-api-production.up.railway.app";

export interface BmapPost {
  tx: { h: string };
  blk?: { t: number; i: number };
  MAP: Array<{ app: string; type: string; [key: string]: string }>;
  B?: Array<{ content: string; "content-type": string; encoding: string }>;
  AIP?: Array<{ address: string; signature: string }>;
}

export interface BmapQuery {
  v: number;
  q: {
    find: Record<string, unknown>;
    sort?: Record<string, number>;
    limit?: number;
    skip?: number;
  };
}

// REST API functions

export async function getPostsByBapId(bapId: string): Promise<BmapPost[]> {
  const response = await fetch(`${BMAP_API_BASE}/social/post/bap/${bapId}`);
  if (!response.ok) throw new Error(`BMAP API error: ${response.status}`);
  return response.json();
}

export async function getFeedByBapId(bapId: string): Promise<BmapPost[]> {
  const response = await fetch(`${BMAP_API_BASE}/social/feed/${bapId}`);
  if (!response.ok) throw new Error(`BMAP API error: ${response.status}`);
  return response.json();
}

export async function searchPosts(query: string): Promise<BmapPost[]> {
  const response = await fetch(`${BMAP_API_BASE}/social/post/search?q=${encodeURIComponent(query)}`);
  if (!response.ok) throw new Error(`BMAP API error: ${response.status}`);
  return response.json();
}

export async function getLikesForPost(txid: string): Promise<BmapPost[]> {
  const response = await fetch(`${BMAP_API_BASE}/social/post/${txid}/like`);
  if (!response.ok) throw new Error(`BMAP API error: ${response.status}`);
  return response.json();
}

export async function getLikesByBapId(bapId: string): Promise<BmapPost[]> {
  const response = await fetch(`${BMAP_API_BASE}/social/bap/${bapId}/like`);
  if (!response.ok) throw new Error(`BMAP API error: ${response.status}`);
  return response.json();
}

export async function getFriendsByBapId(bapId: string): Promise<BmapPost[]> {
  const response = await fetch(`${BMAP_API_BASE}/social/friend/${bapId}`);
  if (!response.ok) throw new Error(`BMAP API error: ${response.status}`);
  return response.json();
}

export async function getMessagesByBapId(bapId: string): Promise<BmapPost[]> {
  const response = await fetch(`${BMAP_API_BASE}/social/@/${bapId}/messages`);
  if (!response.ok) throw new Error(`BMAP API error: ${response.status}`);
  return response.json();
}

export async function getChannelMessages(channelId: string): Promise<BmapPost[]> {
  const response = await fetch(`${BMAP_API_BASE}/social/channels/${channelId}/messages`);
  if (!response.ok) throw new Error(`BMAP API error: ${response.status}`);
  return response.json();
}

// Raw query API (fallback for complex queries)

function encodeQuery(query: BmapQuery): string {
  const json = JSON.stringify(query);
  return btoa(json);
}

export async function queryBmap(collection: string, query: BmapQuery): Promise<BmapPost[]> {
  const encoded = encodeQuery(query);
  const response = await fetch(`${BMAP_API_BASE}/q/${collection}/${encoded}`);

  if (!response.ok) {
    throw new Error(`BMAP API error: ${response.status}`);
  }

  const data = await response.json();
  return data.c || data.u || [];
}

// Query builders for raw query API

export function buildPostsQuery(address: string, limit = 20): BmapQuery {
  return {
    v: 3,
    q: {
      find: {
        "MAP.app": "bsocial",
        "MAP.type": "post",
        "AIP.address": address,
      },
      sort: { "blk.t": -1 },
      limit,
    },
  };
}

export function buildLikesQuery(options: { address?: string; txid?: string }, limit = 20): BmapQuery {
  const find: Record<string, unknown> = {
    "MAP.app": "bsocial",
    "MAP.type": "like",
  };

  if (options.address) {
    find["AIP.address"] = options.address;
  }
  if (options.txid) {
    find["MAP.tx"] = options.txid;
  }

  return {
    v: 3,
    q: {
      find,
      sort: { "blk.t": -1 },
      limit,
    },
  };
}

export function buildFollowsQuery(address: string, limit = 100): BmapQuery {
  return {
    v: 3,
    q: {
      find: {
        "MAP.app": "bsocial",
        "MAP.type": "follow",
        "AIP.address": address,
      },
      sort: { "blk.t": -1 },
      limit,
    },
  };
}

export function buildMessagesQuery(options: { channel?: string; address?: string }, limit = 50): BmapQuery {
  const find: Record<string, unknown> = {
    "MAP.app": "bsocial",
    "MAP.type": "message",
  };

  if (options.channel) {
    find["MAP.context"] = "channel";
    find["MAP.contextValue"] = options.channel;
  }
  if (options.address) {
    find["AIP.address"] = options.address;
  }

  return {
    v: 3,
    q: {
      find,
      sort: { "blk.t": -1 },
      limit,
    },
  };
}

export function buildFriendsQuery(address: string, limit = 100): BmapQuery {
  return {
    v: 3,
    q: {
      find: {
        "MAP.app": "bsocial",
        "MAP.type": "friend",
        "AIP.address": address,
      },
      sort: { "blk.t": -1 },
      limit,
    },
  };
}

// Ingest API for submitting transactions
export async function ingestTransaction(rawTx: string): Promise<{ txid: string }> {
  const response = await fetch(`${BMAP_API_BASE}/ingest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rawTx }),
  });

  if (!response.ok) {
    throw new Error(`BMAP ingest error: ${response.status}`);
  }

  return response.json();
}
