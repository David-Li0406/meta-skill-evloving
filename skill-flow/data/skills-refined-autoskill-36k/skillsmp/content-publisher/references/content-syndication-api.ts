/**
 * Content Syndication API - Empathy Ledger Content Hub
 *
 * This module provides the API endpoints for ACT ecosystem projects
 * to consume content from Empathy Ledger.
 *
 * API Routes (for empathy-ledger-v2/src/app/api/v1/content-hub/):
 * - GET /stories - List published stories
 * - GET /stories/:id - Single story with full content
 * - GET /articles - List published articles
 * - GET /articles/:slug - Single article by slug
 * - GET /media/library - Browse media library
 * - GET /themes - Discover content by themes
 * - GET /search - Full-text search
 * - POST /syndicate - Register syndication relationship
 *
 * Copy individual route handlers to their respective files in:
 * empathy-ledger-v2/src/app/api/v1/content-hub/
 */

import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

// Types for API responses
export interface StoryResponse {
  id: string;
  title: string;
  summary?: string;
  content?: string;
  authorName: string;
  authorId: string;
  publishedAt: string;
  themes: string[];
  featuredMediaUrl?: string;
  visibility: 'private' | 'community' | 'public';
  syndicationEnabled: boolean;
}

export interface ArticleResponse {
  id: string;
  title: string;
  slug: string;
  subtitle?: string;
  excerpt?: string;
  content?: string;
  authorName: string;
  articleType: string;
  primaryProject?: string;
  publishedAt: string;
  tags: string[];
  themes: string[];
  featuredImageUrl?: string;
  visibility: 'private' | 'community' | 'public';
}

export interface MediaResponse {
  id: string;
  url: string;
  title?: string;
  altText?: string;
  mediaType: string;
  width?: number;
  height?: number;
  primaryTheme?: string;
  emotionalTone?: string;
  uploaderName?: string;
}

export interface SyndicationRequest {
  contentType: 'article' | 'story' | 'media_asset' | 'gallery';
  contentId: string;
  destinationType: string;
  attributionText: string;
  requestedBy: string;
}

// Visibility tiers for access control
const VISIBILITY_ACCESS = {
  public: ['anonymous', 'community', 'ecosystem'],
  community: ['community', 'ecosystem'],
  private: ['owner']
};

/**
 * Create Supabase client for API routes
 */
function createSupabaseClient() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
  const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  return createClient(supabaseUrl, supabaseKey);
}

/**
 * Validate API key and return access level
 */
async function validateApiKey(
  request: Request
): Promise<{ valid: boolean; accessLevel: string; projectId?: string }> {
  const apiKey = request.headers.get('X-API-Key');
  const authHeader = request.headers.get('Authorization');

  // Public access (no key)
  if (!apiKey && !authHeader) {
    return { valid: true, accessLevel: 'anonymous' };
  }

  // API key validation for ACT projects
  if (apiKey) {
    const supabase = createSupabaseClient();
    const { data } = await supabase
      .from('api_keys')
      .select('project_id, access_level, active')
      .eq('key_hash', hashApiKey(apiKey))
      .single();

    if (data?.active) {
      return {
        valid: true,
        accessLevel: data.access_level,
        projectId: data.project_id
      };
    }
  }

  // Bearer token validation for authenticated users
  if (authHeader?.startsWith('Bearer ')) {
    // Validate JWT and get user
    return { valid: true, accessLevel: 'community' };
  }

  return { valid: false, accessLevel: 'anonymous' };
}

/**
 * Simple hash for API key comparison
 */
function hashApiKey(key: string): string {
  // In production, use proper hashing
  return Buffer.from(key).toString('base64');
}

// ===========================================
// ROUTE HANDLERS
// ===========================================

/**
 * GET /api/v1/content-hub/stories
 * List published stories with pagination
 */
export async function handleGetStories(request: Request): Promise<Response> {
  const { valid, accessLevel } = await validateApiKey(request);
  if (!valid) {
    return NextResponse.json({ error: 'Invalid API key' }, { status: 401 });
  }

  const url = new URL(request.url);
  const page = parseInt(url.searchParams.get('page') || '1');
  const limit = Math.min(parseInt(url.searchParams.get('limit') || '20'), 100);
  const theme = url.searchParams.get('theme');
  const project = url.searchParams.get('project');

  const supabase = createSupabaseClient();

  // Build query
  let query = supabase
    .from('stories')
    .select(`
      id,
      title,
      summary,
      storyteller_id,
      storytellers!inner(name),
      published_at,
      cultural_themes,
      visibility,
      syndication_enabled
    `)
    .eq('status', 'published')
    .order('published_at', { ascending: false });

  // Filter by visibility based on access level
  if (accessLevel === 'anonymous') {
    query = query.eq('visibility', 'public');
  } else if (accessLevel === 'community') {
    query = query.in('visibility', ['public', 'community']);
  }

  // Filter by theme
  if (theme) {
    query = query.contains('cultural_themes', [theme]);
  }

  // Pagination
  const offset = (page - 1) * limit;
  query = query.range(offset, offset + limit - 1);

  const { data, error, count } = await query;

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  const stories: StoryResponse[] = (data || []).map((story: any) => ({
    id: story.id,
    title: story.title,
    summary: story.summary,
    authorName: story.storytellers?.name || 'Anonymous',
    authorId: story.storyteller_id,
    publishedAt: story.published_at,
    themes: story.cultural_themes || [],
    visibility: story.visibility,
    syndicationEnabled: story.syndication_enabled
  }));

  return NextResponse.json({
    stories,
    pagination: {
      page,
      limit,
      total: count || stories.length,
      hasMore: stories.length === limit
    }
  });
}

/**
 * GET /api/v1/content-hub/stories/:id
 * Get single story with full content
 */
export async function handleGetStory(
  request: Request,
  storyId: string
): Promise<Response> {
  const { valid, accessLevel } = await validateApiKey(request);
  if (!valid) {
    return NextResponse.json({ error: 'Invalid API key' }, { status: 401 });
  }

  const supabase = createSupabaseClient();

  const { data: story, error } = await supabase
    .from('stories')
    .select(`
      *,
      storytellers(name, bio),
      media_assets(url, alt_text)
    `)
    .eq('id', storyId)
    .eq('status', 'published')
    .single();

  if (error || !story) {
    return NextResponse.json({ error: 'Story not found' }, { status: 404 });
  }

  // Check visibility access
  if (story.visibility === 'private') {
    return NextResponse.json({ error: 'Access denied' }, { status: 403 });
  }
  if (story.visibility === 'community' && accessLevel === 'anonymous') {
    return NextResponse.json({ error: 'Community access required' }, { status: 403 });
  }

  return NextResponse.json({
    id: story.id,
    title: story.title,
    summary: story.summary,
    content: story.content,
    authorName: story.storytellers?.name || 'Anonymous',
    authorBio: story.storytellers?.bio,
    authorId: story.storyteller_id,
    publishedAt: story.published_at,
    themes: story.cultural_themes || [],
    featuredMediaUrl: story.media_assets?.[0]?.url,
    visibility: story.visibility,
    syndicationEnabled: story.syndication_enabled
  });
}

/**
 * GET /api/v1/content-hub/articles
 * List published articles with pagination
 */
export async function handleGetArticles(request: Request): Promise<Response> {
  const { valid, accessLevel } = await validateApiKey(request);
  if (!valid) {
    return NextResponse.json({ error: 'Invalid API key' }, { status: 401 });
  }

  const url = new URL(request.url);
  const page = parseInt(url.searchParams.get('page') || '1');
  const limit = Math.min(parseInt(url.searchParams.get('limit') || '20'), 100);
  const type = url.searchParams.get('type');
  const project = url.searchParams.get('project');
  const tag = url.searchParams.get('tag');

  const supabase = createSupabaseClient();

  let query = supabase
    .from('articles')
    .select(`
      id,
      title,
      slug,
      subtitle,
      excerpt,
      author_name,
      author_storyteller_id,
      article_type,
      primary_project,
      published_at,
      tags,
      themes,
      visibility,
      syndication_enabled,
      featured_image_id,
      media_assets!featured_image_id(url)
    `)
    .eq('status', 'published')
    .eq('syndication_enabled', true)
    .order('published_at', { ascending: false });

  // Visibility filter
  if (accessLevel === 'anonymous') {
    query = query.eq('visibility', 'public');
  } else if (accessLevel === 'community') {
    query = query.in('visibility', ['public', 'community']);
  }

  // Additional filters
  if (type) query = query.eq('article_type', type);
  if (project) query = query.eq('primary_project', project);
  if (tag) query = query.contains('tags', [tag]);

  // Pagination
  const offset = (page - 1) * limit;
  query = query.range(offset, offset + limit - 1);

  const { data, error, count } = await query;

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  const articles: ArticleResponse[] = (data || []).map((article: any) => ({
    id: article.id,
    title: article.title,
    slug: article.slug,
    subtitle: article.subtitle,
    excerpt: article.excerpt,
    authorName: article.author_name || 'Staff',
    articleType: article.article_type,
    primaryProject: article.primary_project,
    publishedAt: article.published_at,
    tags: article.tags || [],
    themes: article.themes || [],
    featuredImageUrl: article.media_assets?.url,
    visibility: article.visibility
  }));

  return NextResponse.json({
    articles,
    pagination: {
      page,
      limit,
      total: count || articles.length,
      hasMore: articles.length === limit
    }
  });
}

/**
 * GET /api/v1/content-hub/articles/:slug
 * Get single article by slug
 */
export async function handleGetArticle(
  request: Request,
  slug: string
): Promise<Response> {
  const { valid, accessLevel } = await validateApiKey(request);
  if (!valid) {
    return NextResponse.json({ error: 'Invalid API key' }, { status: 401 });
  }

  const supabase = createSupabaseClient();

  const { data: article, error } = await supabase
    .from('articles')
    .select(`
      *,
      storytellers:author_storyteller_id(name, bio),
      media_assets!featured_image_id(url, alt_text)
    `)
    .eq('slug', slug)
    .eq('status', 'published')
    .single();

  if (error || !article) {
    return NextResponse.json({ error: 'Article not found' }, { status: 404 });
  }

  // Check visibility
  if (article.visibility === 'private') {
    return NextResponse.json({ error: 'Access denied' }, { status: 403 });
  }
  if (article.visibility === 'community' && accessLevel === 'anonymous') {
    return NextResponse.json({ error: 'Community access required' }, { status: 403 });
  }

  // Increment view count
  await supabase
    .from('articles')
    .update({ views_count: (article.views_count || 0) + 1 })
    .eq('id', article.id);

  return NextResponse.json({
    id: article.id,
    title: article.title,
    slug: article.slug,
    subtitle: article.subtitle,
    excerpt: article.excerpt,
    content: article.content,
    authorName: article.author_name || article.storytellers?.name || 'Staff',
    authorBio: article.storytellers?.bio,
    articleType: article.article_type,
    primaryProject: article.primary_project,
    relatedProjects: article.related_projects || [],
    publishedAt: article.published_at,
    tags: article.tags || [],
    themes: article.themes || [],
    featuredImageUrl: article.media_assets?.url,
    featuredImageAlt: article.media_assets?.alt_text,
    visibility: article.visibility,
    metaTitle: article.meta_title,
    metaDescription: article.meta_description
  });
}

/**
 * GET /api/v1/content-hub/media/library
 * Browse media library
 */
export async function handleGetMediaLibrary(request: Request): Promise<Response> {
  const { valid, accessLevel } = await validateApiKey(request);
  if (!valid) {
    return NextResponse.json({ error: 'Invalid API key' }, { status: 401 });
  }

  const url = new URL(request.url);
  const page = parseInt(url.searchParams.get('page') || '1');
  const limit = Math.min(parseInt(url.searchParams.get('limit') || '20'), 50);
  const mediaType = url.searchParams.get('type'); // image, video, audio
  const theme = url.searchParams.get('theme');

  const supabase = createSupabaseClient();

  let query = supabase
    .from('media_assets')
    .select(`
      id,
      url,
      title,
      alt_text,
      media_type,
      width,
      height,
      visibility,
      uploader_id,
      storytellers:uploader_id(name),
      media_narrative_themes(primary_theme, emotional_tone)
    `)
    .eq('status', 'active');

  // Visibility filter
  if (accessLevel === 'anonymous') {
    query = query.eq('visibility', 'public');
  } else if (accessLevel === 'community') {
    query = query.in('visibility', ['public', 'community']);
  }

  // Additional filters
  if (mediaType) query = query.eq('media_type', mediaType);
  if (theme) {
    query = query.filter('media_narrative_themes.primary_theme', 'eq', theme);
  }

  // Pagination
  const offset = (page - 1) * limit;
  query = query.range(offset, offset + limit - 1);

  const { data, error } = await query;

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  const media: MediaResponse[] = (data || []).map((item: any) => ({
    id: item.id,
    url: item.url,
    title: item.title,
    altText: item.alt_text,
    mediaType: item.media_type,
    width: item.width,
    height: item.height,
    primaryTheme: item.media_narrative_themes?.[0]?.primary_theme,
    emotionalTone: item.media_narrative_themes?.[0]?.emotional_tone,
    uploaderName: item.storytellers?.name
  }));

  return NextResponse.json({
    media,
    pagination: {
      page,
      limit,
      hasMore: media.length === limit
    }
  });
}

/**
 * GET /api/v1/content-hub/themes
 * Discover content by themes
 */
export async function handleGetThemes(request: Request): Promise<Response> {
  const { valid } = await validateApiKey(request);
  if (!valid) {
    return NextResponse.json({ error: 'Invalid API key' }, { status: 401 });
  }

  const supabase = createSupabaseClient();

  // Get theme statistics
  const { data: themes } = await supabase
    .from('narrative_themes')
    .select('id, name, category, description')
    .order('name');

  // Get counts per theme from media
  const { data: mediaCounts } = await supabase
    .from('media_narrative_themes')
    .select('primary_theme');

  // Calculate counts
  const counts: Record<string, number> = {};
  for (const item of mediaCounts || []) {
    const theme = item.primary_theme;
    counts[theme] = (counts[theme] || 0) + 1;
  }

  // Combine themes with counts
  const themesWithCounts = (themes || []).map((theme: any) => ({
    id: theme.id,
    name: theme.name,
    category: theme.category,
    description: theme.description,
    mediaCount: counts[theme.name] || 0
  }));

  return NextResponse.json({
    themes: themesWithCounts,
    categories: [...new Set(themesWithCounts.map((t: any) => t.category))]
  });
}

/**
 * GET /api/v1/content-hub/search
 * Full-text search across content
 */
export async function handleSearch(request: Request): Promise<Response> {
  const { valid, accessLevel } = await validateApiKey(request);
  if (!valid) {
    return NextResponse.json({ error: 'Invalid API key' }, { status: 401 });
  }

  const url = new URL(request.url);
  const query = url.searchParams.get('q');
  const contentType = url.searchParams.get('type'); // stories, articles, media
  const limit = Math.min(parseInt(url.searchParams.get('limit') || '20'), 50);

  if (!query || query.length < 2) {
    return NextResponse.json({ error: 'Query too short' }, { status: 400 });
  }

  const supabase = createSupabaseClient();
  const results: any = { stories: [], articles: [], media: [] };

  // Search stories
  if (!contentType || contentType === 'stories') {
    const { data: stories } = await supabase
      .from('stories')
      .select('id, title, summary, published_at')
      .eq('status', 'published')
      .eq('visibility', accessLevel === 'anonymous' ? 'public' : 'community')
      .textSearch('search_vector', query)
      .limit(limit);

    results.stories = stories || [];
  }

  // Search articles
  if (!contentType || contentType === 'articles') {
    const { data: articles } = await supabase
      .from('articles')
      .select('id, title, slug, excerpt, published_at')
      .eq('status', 'published')
      .eq('visibility', accessLevel === 'anonymous' ? 'public' : 'community')
      .textSearch('search_vector', query)
      .limit(limit);

    results.articles = articles || [];
  }

  // Search media
  if (!contentType || contentType === 'media') {
    const { data: media } = await supabase
      .from('media_assets')
      .select('id, url, title, alt_text')
      .eq('status', 'active')
      .eq('visibility', accessLevel === 'anonymous' ? 'public' : 'community')
      .textSearch('search_vector', query)
      .limit(limit);

    results.media = media || [];
  }

  return NextResponse.json({
    query,
    results,
    total: results.stories.length + results.articles.length + results.media.length
  });
}

/**
 * POST /api/v1/content-hub/syndicate
 * Register syndication relationship
 */
export async function handleSyndicate(request: Request): Promise<Response> {
  const { valid, accessLevel, projectId } = await validateApiKey(request);
  if (!valid || !projectId) {
    return NextResponse.json({ error: 'API key required for syndication' }, { status: 401 });
  }

  const body: SyndicationRequest = await request.json();

  // Validate required fields
  if (!body.contentType || !body.contentId || !body.destinationType || !body.attributionText) {
    return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
  }

  const supabase = createSupabaseClient();

  // Check if content exists and is syndicatable
  const table = body.contentType === 'article' ? 'articles' : 'stories';
  const { data: content } = await supabase
    .from(table)
    .select('syndication_enabled, visibility')
    .eq('id', body.contentId)
    .single();

  if (!content) {
    return NextResponse.json({ error: 'Content not found' }, { status: 404 });
  }

  if (!content.syndication_enabled) {
    return NextResponse.json({ error: 'Content not available for syndication' }, { status: 403 });
  }

  // Create syndication record
  const { data, error } = await supabase
    .from('content_syndication')
    .insert({
      content_type: body.contentType,
      content_id: body.contentId,
      destination_type: body.destinationType,
      attribution_text: body.attributionText,
      syndication_consent_granted: true, // API key implies consent
      consent_granted_at: new Date().toISOString(),
      syndication_request_by: body.requestedBy,
      status: 'pending'
    })
    .select()
    .single();

  if (error) {
    if (error.code === '23505') {
      return NextResponse.json({ error: 'Already syndicated to this destination' }, { status: 409 });
    }
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({
    syndicationId: data.id,
    status: 'pending',
    message: 'Syndication registered successfully'
  }, { status: 201 });
}

// Export all handlers
export const ContentHubAPI = {
  getStories: handleGetStories,
  getStory: handleGetStory,
  getArticles: handleGetArticles,
  getArticle: handleGetArticle,
  getMediaLibrary: handleGetMediaLibrary,
  getThemes: handleGetThemes,
  search: handleSearch,
  syndicate: handleSyndicate
};

export default ContentHubAPI;
