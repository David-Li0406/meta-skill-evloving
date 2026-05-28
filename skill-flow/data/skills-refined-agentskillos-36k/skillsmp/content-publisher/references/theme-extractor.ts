/**
 * Theme Extractor - Connect media to narrative themes and stories
 *
 * This module:
 * - Extracts themes from media using AI analysis
 * - Links media to existing narrative themes
 * - Connects media to related stories
 * - Integrates with ALMA for intervention tracking
 *
 * Copy this file to: empathy-ledger-v2/src/lib/media-intelligence/theme-extractor.ts
 */

import { createClient } from '@supabase/supabase-js';
import Anthropic from '@anthropic-ai/sdk';

// Types
export interface MediaTheme {
  mediaAssetId: string;
  primaryTheme: string;
  secondaryThemes: string[];
  themeConfidence: number;
  emotionalTone: string;
  narrativeRole?: string;
  keywords: string[];
  relatedStoryId?: string;
  storyRelevanceScore?: number;
  almaInterventionId?: string;
  almaEvidenceType?: string;
}

export interface ThemeMatch {
  themeId: string;
  themeName: string;
  category: string;
  similarity: number;
}

// Narrative theme categories (matches Empathy Ledger's theme system)
const THEME_CATEGORIES = {
  identity: ['family', 'heritage', 'language', 'culture', 'belonging', 'country'],
  journey: ['healing', 'growth', 'resilience', 'transformation', 'survival'],
  community: ['connection', 'support', 'unity', 'sharing', 'gathering'],
  trauma: ['loss', 'separation', 'grief', 'injustice', 'displacement'],
  hope: ['dreams', 'aspiration', 'future', 'opportunity', 'education'],
  strength: ['pride', 'determination', 'courage', 'wisdom', 'leadership'],
  culture: ['ceremony', 'tradition', 'art', 'music', 'storytelling', 'country']
};

// Emotional tone options
const EMOTIONAL_TONES = [
  'hopeful', 'reflective', 'celebratory', 'somber', 'joyful',
  'contemplative', 'proud', 'resilient', 'nostalgic', 'peaceful'
];

// Narrative roles for media in stories
const NARRATIVE_ROLES = [
  'establishing', 'character_intro', 'context', 'climax',
  'resolution', 'evidence', 'illustration', 'mood_setting'
];

/**
 * ThemeExtractor class - extracts and links themes from media
 */
export class ThemeExtractor {
  private supabase: ReturnType<typeof createClient>;
  private anthropic: Anthropic;

  constructor(
    supabaseUrl: string,
    supabaseKey: string,
    anthropicApiKey?: string
  ) {
    this.supabase = createClient(supabaseUrl, supabaseKey);

    if (anthropicApiKey) {
      this.anthropic = new Anthropic({ apiKey: anthropicApiKey });
    }
  }

  /**
   * Extract themes from media analysis results
   */
  async extractThemes(
    mediaAssetId: string,
    analysisResults: {
      sceneClassification: string;
      autoTags: string[];
      detectedObjects: Array<{ label: string }>;
      emotionalTone?: string;
    }
  ): Promise<MediaTheme> {
    // Build context from analysis
    const contextText = [
      `Scene: ${analysisResults.sceneClassification}`,
      `Tags: ${analysisResults.autoTags.join(', ')}`,
      `Objects: ${analysisResults.detectedObjects.map(o => o.label).join(', ')}`,
      analysisResults.emotionalTone ? `Tone: ${analysisResults.emotionalTone}` : ''
    ].filter(Boolean).join('. ');

    // Extract themes using Claude
    const themes = await this.classifyThemes(contextText);

    // Find related stories
    const relatedStory = await this.findRelatedStory(themes, mediaAssetId);

    // Build the theme result
    const mediaTheme: MediaTheme = {
      mediaAssetId,
      primaryTheme: themes.primaryTheme,
      secondaryThemes: themes.secondaryThemes,
      themeConfidence: themes.confidence,
      emotionalTone: analysisResults.emotionalTone || themes.emotionalTone,
      narrativeRole: themes.narrativeRole,
      keywords: themes.keywords,
      relatedStoryId: relatedStory?.storyId,
      storyRelevanceScore: relatedStory?.relevanceScore
    };

    // Save to database
    await this.saveThemes(mediaTheme);

    return mediaTheme;
  }

  /**
   * Classify themes using Claude
   */
  private async classifyThemes(contextText: string): Promise<{
    primaryTheme: string;
    secondaryThemes: string[];
    confidence: number;
    emotionalTone: string;
    narrativeRole: string;
    keywords: string[];
  }> {
    if (!this.anthropic) {
      // Fallback to rule-based extraction if no AI
      return this.ruleBasedThemeExtraction(contextText);
    }

    const categoryList = Object.entries(THEME_CATEGORIES)
      .map(([cat, themes]) => `${cat}: ${themes.join(', ')}`)
      .join('\n');

    const toneList = EMOTIONAL_TONES.join(', ');
    const roleList = NARRATIVE_ROLES.join(', ');

    const prompt = `Analyze this media description and extract narrative themes for an Indigenous storytelling platform.

Media Description: ${contextText}

Theme Categories:
${categoryList}

Available Emotional Tones: ${toneList}
Available Narrative Roles: ${roleList}

Extract:
1. Primary theme (single most relevant theme from the categories above)
2. Secondary themes (2-4 additional relevant themes)
3. Emotional tone of the media
4. Narrative role (how this media might be used in a story)
5. Keywords for search (5-10 specific terms)
6. Confidence score (0-1)

Respond in JSON:
{
  "primaryTheme": "theme",
  "secondaryThemes": ["theme1", "theme2"],
  "confidence": 0.8,
  "emotionalTone": "tone",
  "narrativeRole": "role",
  "keywords": ["keyword1", "keyword2"]
}`;

    try {
      const response = await this.anthropic.messages.create({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 1000,
        messages: [{ role: 'user', content: prompt }]
      });

      const text = response.content[0].type === 'text' ? response.content[0].text : '';
      const jsonMatch = text.match(/\{[\s\S]*\}/);

      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
    } catch (error) {
      console.error('Theme extraction error:', error);
    }

    // Fallback
    return this.ruleBasedThemeExtraction(contextText);
  }

  /**
   * Rule-based theme extraction fallback
   */
  private ruleBasedThemeExtraction(text: string): {
    primaryTheme: string;
    secondaryThemes: string[];
    confidence: number;
    emotionalTone: string;
    narrativeRole: string;
    keywords: string[];
  } {
    const lowerText = text.toLowerCase();
    const foundThemes: string[] = [];

    // Check each theme category
    for (const [category, themes] of Object.entries(THEME_CATEGORIES)) {
      for (const theme of themes) {
        if (lowerText.includes(theme)) {
          foundThemes.push(theme);
        }
      }
    }

    // Extract keywords (simple approach)
    const words = text.split(/\s+/).filter(w => w.length > 3);
    const keywords = [...new Set(words)].slice(0, 10);

    return {
      primaryTheme: foundThemes[0] || 'community',
      secondaryThemes: foundThemes.slice(1, 4),
      confidence: foundThemes.length > 0 ? 0.6 : 0.3,
      emotionalTone: 'reflective',
      narrativeRole: 'context',
      keywords
    };
  }

  /**
   * Find stories related to the themes
   */
  private async findRelatedStory(
    themes: { primaryTheme: string; secondaryThemes: string[] },
    mediaAssetId: string
  ): Promise<{ storyId: string; relevanceScore: number } | null> {
    // Search for stories with matching themes
    const { data: stories } = await this.supabase
      .from('stories')
      .select('id, cultural_themes, title')
      .or(`cultural_themes.cs.{${themes.primaryTheme}},cultural_themes.cs.{${themes.secondaryThemes.join(',')}}`)
      .eq('status', 'published')
      .limit(5);

    if (!stories || stories.length === 0) return null;

    // Calculate relevance scores
    let bestMatch = { storyId: '', score: 0 };

    for (const story of stories) {
      const storyThemes = story.cultural_themes || [];
      let score = 0;

      // Primary theme match = 0.5
      if (storyThemes.includes(themes.primaryTheme)) {
        score += 0.5;
      }

      // Secondary theme matches = 0.1 each
      for (const theme of themes.secondaryThemes) {
        if (storyThemes.includes(theme)) {
          score += 0.1;
        }
      }

      if (score > bestMatch.score) {
        bestMatch = { storyId: story.id, score };
      }
    }

    return bestMatch.score > 0.3
      ? { storyId: bestMatch.storyId, relevanceScore: bestMatch.score }
      : null;
  }

  /**
   * Save extracted themes to database
   */
  private async saveThemes(theme: MediaTheme): Promise<void> {
    const { error } = await this.supabase
      .from('media_narrative_themes')
      .upsert({
        media_asset_id: theme.mediaAssetId,
        primary_theme: theme.primaryTheme,
        secondary_themes: theme.secondaryThemes,
        theme_confidence: theme.themeConfidence,
        emotional_tone: theme.emotionalTone,
        narrative_role: theme.narrativeRole,
        keywords: theme.keywords,
        related_story_id: theme.relatedStoryId,
        story_relevance_score: theme.storyRelevanceScore,
        alma_intervention_id: theme.almaInterventionId,
        alma_evidence_type: theme.almaEvidenceType,
        ai_generated: true,
        human_verified: false
      }, {
        onConflict: 'media_asset_id'
      });

    if (error) {
      throw new Error(`Failed to save themes: ${error.message}`);
    }
  }

  /**
   * Link media to ALMA intervention
   */
  async linkToAlmaIntervention(
    mediaAssetId: string,
    interventionId: string,
    evidenceType: 'documentation' | 'outcome' | 'testimony' | 'impact'
  ): Promise<void> {
    const { error } = await this.supabase
      .from('media_narrative_themes')
      .update({
        alma_intervention_id: interventionId,
        alma_evidence_type: evidenceType
      })
      .eq('media_asset_id', mediaAssetId);

    if (error) {
      throw new Error(`Failed to link to ALMA: ${error.message}`);
    }
  }

  /**
   * Get media by theme
   */
  async getMediaByTheme(
    theme: string,
    limit: number = 20
  ): Promise<Array<{ mediaId: string; primaryTheme: string; emotionalTone: string }>> {
    const { data, error } = await this.supabase
      .from('media_narrative_themes')
      .select('media_asset_id, primary_theme, emotional_tone')
      .or(`primary_theme.eq.${theme},secondary_themes.cs.{${theme}}`)
      .order('theme_confidence', { ascending: false })
      .limit(limit);

    if (error) {
      console.error('Error getting media by theme:', error);
      return [];
    }

    return data?.map(d => ({
      mediaId: d.media_asset_id,
      primaryTheme: d.primary_theme,
      emotionalTone: d.emotional_tone
    })) || [];
  }

  /**
   * Get all themes for a story's media
   */
  async getStoryMediaThemes(storyId: string): Promise<MediaTheme[]> {
    const { data, error } = await this.supabase
      .from('media_narrative_themes')
      .select('*')
      .eq('related_story_id', storyId);

    if (error) {
      console.error('Error getting story media themes:', error);
      return [];
    }

    return data?.map(d => ({
      mediaAssetId: d.media_asset_id,
      primaryTheme: d.primary_theme,
      secondaryThemes: d.secondary_themes || [],
      themeConfidence: d.theme_confidence,
      emotionalTone: d.emotional_tone,
      narrativeRole: d.narrative_role,
      keywords: d.keywords || [],
      relatedStoryId: d.related_story_id,
      storyRelevanceScore: d.story_relevance_score,
      almaInterventionId: d.alma_intervention_id,
      almaEvidenceType: d.alma_evidence_type
    })) || [];
  }

  /**
   * Verify human-verified themes
   */
  async verifyThemes(
    mediaAssetId: string,
    verifiedBy: string,
    corrections?: {
      primaryTheme?: string;
      secondaryThemes?: string[];
      emotionalTone?: string;
    }
  ): Promise<void> {
    const updates: Record<string, any> = {
      human_verified: true,
      verified_by: verifiedBy
    };

    if (corrections) {
      if (corrections.primaryTheme) updates.primary_theme = corrections.primaryTheme;
      if (corrections.secondaryThemes) updates.secondary_themes = corrections.secondaryThemes;
      if (corrections.emotionalTone) updates.emotional_tone = corrections.emotionalTone;
    }

    const { error } = await this.supabase
      .from('media_narrative_themes')
      .update(updates)
      .eq('media_asset_id', mediaAssetId);

    if (error) {
      throw new Error(`Failed to verify themes: ${error.message}`);
    }
  }

  /**
   * Get theme statistics
   */
  async getThemeStats(): Promise<Record<string, number>> {
    const { data, error } = await this.supabase
      .from('media_narrative_themes')
      .select('primary_theme');

    if (error) {
      console.error('Error getting theme stats:', error);
      return {};
    }

    const stats: Record<string, number> = {};
    for (const item of data || []) {
      const theme = item.primary_theme;
      stats[theme] = (stats[theme] || 0) + 1;
    }

    return stats;
  }
}

/**
 * Create a ThemeExtractor instance with environment variables
 */
export function createThemeExtractor() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  const anthropicKey = process.env.ANTHROPIC_API_KEY;

  if (!supabaseUrl || !supabaseKey) {
    throw new Error('Supabase credentials required');
  }

  return new ThemeExtractor(supabaseUrl, supabaseKey, anthropicKey);
}

export default ThemeExtractor;
