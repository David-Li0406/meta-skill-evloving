/**
 * Photo Analyzer - AI-powered image analysis with consent gates
 *
 * This module provides intelligent photo analysis including:
 * - Object detection
 * - Scene classification
 * - Auto-tagging
 * - Semantic embedding generation
 *
 * CRITICAL: All analysis requires explicit consent before processing.
 * The consent gate is enforced at both application and database level.
 *
 * Copy this file to: empathy-ledger-v2/src/lib/media-intelligence/photo-analyzer.ts
 */

import { createClient } from '@supabase/supabase-js';
import Anthropic from '@anthropic-ai/sdk';
import OpenAI from 'openai';

// Types
export interface PhotoAnalysisRequest {
  mediaAssetId: string;
  storytellerId: string;
  imageUrl: string;
  consentGranted: boolean;
}

export interface DetectedObject {
  label: string;
  confidence: number;
  boundingBox?: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}

export interface PhotoAnalysisResult {
  mediaAssetId: string;
  detectedObjects: DetectedObject[];
  sceneClassification: string;
  sceneConfidence: number;
  autoTags: string[];
  culturalReviewRequired: boolean;
  emotionalTone?: string;
  contentEmbedding?: number[];
}

export interface AnalysisConsent {
  mediaAssetId: string;
  storytellerId: string;
  consentGranted: boolean;
  consentGrantedAt?: Date;
}

// Cultural keywords that trigger review
const CULTURAL_SENSITIVITY_KEYWORDS = [
  'ceremony', 'sacred', 'traditional', 'elder', 'initiation',
  'ritual', 'dreaming', 'songline', 'sorry business', 'smoking ceremony',
  'corroboree', 'burial', 'mourning', 'mens business', 'womens business',
  'restricted', 'secret', 'sacred site', 'totem'
];

// Scene categories for classification
const SCENE_CATEGORIES = [
  'portrait', 'group_photo', 'landscape', 'ceremony', 'event',
  'interview', 'workshop', 'celebration', 'documentation',
  'community_gathering', 'cultural_activity', 'art', 'nature'
];

/**
 * PhotoAnalyzer class - handles AI-powered image analysis with consent gates
 */
export class PhotoAnalyzer {
  private anthropic: Anthropic;
  private openai: OpenAI;
  private supabase: ReturnType<typeof createClient>;

  constructor(
    supabaseUrl: string,
    supabaseKey: string,
    anthropicApiKey?: string,
    openaiApiKey?: string
  ) {
    this.supabase = createClient(supabaseUrl, supabaseKey);

    if (anthropicApiKey) {
      this.anthropic = new Anthropic({ apiKey: anthropicApiKey });
    }

    if (openaiApiKey) {
      this.openai = new OpenAI({ apiKey: openaiApiKey });
    }
  }

  /**
   * Check if consent exists for AI analysis
   */
  async checkConsent(mediaAssetId: string): Promise<AnalysisConsent | null> {
    const { data, error } = await this.supabase
      .from('media_ai_analysis')
      .select('media_asset_id, storyteller_id, ai_consent_granted, consent_granted_at')
      .eq('media_asset_id', mediaAssetId)
      .single();

    if (error || !data) return null;

    return {
      mediaAssetId: data.media_asset_id,
      storytellerId: data.storyteller_id,
      consentGranted: data.ai_consent_granted,
      consentGrantedAt: data.consent_granted_at ? new Date(data.consent_granted_at) : undefined
    };
  }

  /**
   * Grant consent for AI analysis
   * This creates or updates the analysis record with consent
   */
  async grantConsent(
    mediaAssetId: string,
    storytellerId: string,
    grantedBy: string
  ): Promise<void> {
    const { error } = await this.supabase
      .from('media_ai_analysis')
      .upsert({
        media_asset_id: mediaAssetId,
        storyteller_id: storytellerId,
        ai_consent_granted: true,
        consent_granted_at: new Date().toISOString(),
        consent_granted_by: grantedBy,
        processing_status: 'pending'
      }, {
        onConflict: 'media_asset_id'
      });

    if (error) {
      throw new Error(`Failed to grant consent: ${error.message}`);
    }
  }

  /**
   * Revoke consent for AI analysis
   * This clears all AI-generated data
   */
  async revokeConsent(mediaAssetId: string): Promise<void> {
    const { error } = await this.supabase
      .from('media_ai_analysis')
      .update({
        ai_consent_granted: false,
        detected_objects: [],
        scene_classification: null,
        auto_tags: [],
        content_embedding: null,
        processing_status: 'blocked_no_consent'
      })
      .eq('media_asset_id', mediaAssetId);

    if (error) {
      throw new Error(`Failed to revoke consent: ${error.message}`);
    }
  }

  /**
   * Analyze a photo using Claude Vision
   * REQUIRES: consent must be granted before calling this method
   */
  async analyzePhoto(request: PhotoAnalysisRequest): Promise<PhotoAnalysisResult> {
    // CONSENT GATE - Critical check
    if (!request.consentGranted) {
      throw new Error(
        'AI analysis requires explicit consent. Grant consent first using grantConsent().'
      );
    }

    // Verify consent in database
    const consent = await this.checkConsent(request.mediaAssetId);
    if (!consent?.consentGranted) {
      throw new Error(
        'Consent not found in database. Use grantConsent() before analysis.'
      );
    }

    // Update status to processing
    await this.updateProcessingStatus(request.mediaAssetId, 'processing');

    try {
      // Use Claude Vision for analysis
      const analysisPrompt = this.buildAnalysisPrompt();

      const response = await this.anthropic.messages.create({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 2000,
        messages: [
          {
            role: 'user',
            content: [
              {
                type: 'image',
                source: {
                  type: 'url',
                  url: request.imageUrl
                }
              },
              {
                type: 'text',
                text: analysisPrompt
              }
            ]
          }
        ]
      });

      // Parse the response
      const analysisText = response.content[0].type === 'text'
        ? response.content[0].text
        : '';

      const result = this.parseAnalysisResponse(request.mediaAssetId, analysisText);

      // Check for cultural sensitivity
      result.culturalReviewRequired = this.checkCulturalSensitivity(result);

      // Generate embedding for semantic search
      if (this.openai) {
        const embeddingText = [
          result.sceneClassification,
          ...result.autoTags
        ].join(' ');
        result.contentEmbedding = await this.generateEmbedding(embeddingText);
      }

      // Save results to database
      await this.saveAnalysisResults(result);

      return result;
    } catch (error) {
      await this.updateProcessingStatus(
        request.mediaAssetId,
        'failed',
        error instanceof Error ? error.message : 'Unknown error'
      );
      throw error;
    }
  }

  /**
   * Build the analysis prompt for Claude
   */
  private buildAnalysisPrompt(): string {
    const sceneList = SCENE_CATEGORIES.join(', ');
    return `Analyze this image for an Indigenous community storytelling platform.
Your analysis will help with organization and discovery while respecting cultural protocols.

Please provide:
1. OBJECTS: List main objects/subjects visible (people, animals, objects, landmarks)
2. SCENE: Classify the scene type from: ${sceneList}
3. TAGS: Suggest 5-10 descriptive tags for searchability
4. EMOTIONAL TONE: What feeling does this image convey?
5. CULTURAL NOTE: Does this appear to show any cultural/ceremonial content that might need community review?

Respond in this exact JSON format:
{
  "objects": [{"label": "string", "confidence": 0.0-1.0}],
  "scene": "scene_type",
  "sceneConfidence": 0.0-1.0,
  "tags": ["tag1", "tag2"],
  "emotionalTone": "string",
  "culturalNote": "none" | "may_need_review" | "likely_sensitive"
}

Be respectful and avoid assumptions about cultural significance. When in doubt, flag for review.`;
  }

  /**
   * Parse Claude's analysis response
   */
  private parseAnalysisResponse(
    mediaAssetId: string,
    responseText: string
  ): PhotoAnalysisResult {
    try {
      // Extract JSON from response
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        throw new Error('No JSON found in response');
      }

      const parsed = JSON.parse(jsonMatch[0]);

      return {
        mediaAssetId,
        detectedObjects: parsed.objects?.map((obj: any) => ({
          label: obj.label,
          confidence: obj.confidence || 0.8
        })) || [],
        sceneClassification: parsed.scene || 'unknown',
        sceneConfidence: parsed.sceneConfidence || 0.7,
        autoTags: parsed.tags || [],
        culturalReviewRequired: parsed.culturalNote !== 'none',
        emotionalTone: parsed.emotionalTone
      };
    } catch (error) {
      // Return minimal result on parse error
      return {
        mediaAssetId,
        detectedObjects: [],
        sceneClassification: 'unknown',
        sceneConfidence: 0,
        autoTags: [],
        culturalReviewRequired: true // Default to review on error
      };
    }
  }

  /**
   * Check if content needs cultural review based on keywords
   */
  private checkCulturalSensitivity(result: PhotoAnalysisResult): boolean {
    const allText = [
      result.sceneClassification,
      ...result.autoTags,
      ...result.detectedObjects.map(o => o.label),
      result.emotionalTone
    ].join(' ').toLowerCase();

    return CULTURAL_SENSITIVITY_KEYWORDS.some(keyword =>
      allText.includes(keyword.toLowerCase())
    );
  }

  /**
   * Generate semantic embedding using OpenAI
   */
  private async generateEmbedding(text: string): Promise<number[]> {
    if (!this.openai) {
      throw new Error('OpenAI client not configured');
    }

    const response = await this.openai.embeddings.create({
      model: 'text-embedding-3-small',
      input: text,
      dimensions: 1536
    });

    return response.data[0].embedding;
  }

  /**
   * Save analysis results to database
   */
  private async saveAnalysisResults(result: PhotoAnalysisResult): Promise<void> {
    const { error } = await this.supabase
      .from('media_ai_analysis')
      .update({
        detected_objects: result.detectedObjects,
        scene_classification: result.sceneClassification,
        scene_confidence: result.sceneConfidence,
        auto_tags: result.autoTags,
        cultural_review_required: result.culturalReviewRequired,
        cultural_review_status: result.culturalReviewRequired ? 'pending' : 'not_required',
        content_embedding: result.contentEmbedding,
        processing_status: 'completed',
        processed_at: new Date().toISOString(),
        ai_model_version: 'claude-sonnet-4-20250514'
      })
      .eq('media_asset_id', result.mediaAssetId);

    if (error) {
      throw new Error(`Failed to save analysis results: ${error.message}`);
    }
  }

  /**
   * Update processing status
   */
  private async updateProcessingStatus(
    mediaAssetId: string,
    status: string,
    error?: string
  ): Promise<void> {
    await this.supabase
      .from('media_ai_analysis')
      .update({
        processing_status: status,
        processing_error: error
      })
      .eq('media_asset_id', mediaAssetId);
  }

  /**
   * Find visually similar media using embeddings
   */
  async findSimilarMedia(
    mediaAssetId: string,
    limit: number = 10,
    threshold: number = 0.7
  ): Promise<Array<{ mediaId: string; similarity: number }>> {
    // Get the embedding for the source media
    const { data: source } = await this.supabase
      .from('media_ai_analysis')
      .select('content_embedding')
      .eq('media_asset_id', mediaAssetId)
      .single();

    if (!source?.content_embedding) {
      return [];
    }

    // Use RPC to find similar media
    const { data, error } = await this.supabase.rpc('match_media_by_embedding', {
      query_embedding: source.content_embedding,
      match_threshold: threshold,
      match_count: limit
    });

    if (error) {
      console.error('Error finding similar media:', error);
      return [];
    }

    return data?.map((item: any) => ({
      mediaId: item.media_asset_id,
      similarity: item.similarity
    })) || [];
  }

  /**
   * Batch analyze multiple photos (with individual consent checks)
   */
  async batchAnalyze(
    requests: PhotoAnalysisRequest[],
    onProgress?: (completed: number, total: number) => void
  ): Promise<Map<string, PhotoAnalysisResult | Error>> {
    const results = new Map<string, PhotoAnalysisResult | Error>();

    for (let i = 0; i < requests.length; i++) {
      const request = requests[i];

      try {
        // Each request must have consent verified
        const result = await this.analyzePhoto(request);
        results.set(request.mediaAssetId, result);
      } catch (error) {
        results.set(request.mediaAssetId, error as Error);
      }

      onProgress?.(i + 1, requests.length);
    }

    return results;
  }
}

/**
 * Create a PhotoAnalyzer instance with environment variables
 */
export function createPhotoAnalyzer() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  const anthropicKey = process.env.ANTHROPIC_API_KEY;
  const openaiKey = process.env.OPENAI_API_KEY;

  if (!supabaseUrl || !supabaseKey) {
    throw new Error('Supabase credentials required');
  }

  return new PhotoAnalyzer(
    supabaseUrl,
    supabaseKey,
    anthropicKey,
    openaiKey
  );
}

export default PhotoAnalyzer;
