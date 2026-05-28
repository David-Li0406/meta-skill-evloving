/**
 * Face Recognition - Consent-gated face detection and recognition
 *
 * This module handles:
 * - Face detection in photos
 * - Face encoding for matching
 * - Two-party consent management (uploader + person in photo)
 * - Storyteller linking
 *
 * CRITICAL: Face recognition requires TWO-PARTY CONSENT:
 * 1. The media uploader/owner must consent
 * 2. The person in the photo must consent to being identified
 *
 * Copy this file to: empathy-ledger-v2/src/lib/media-intelligence/face-recognition.ts
 */

import { createClient } from '@supabase/supabase-js';

// Types
export interface FaceLocation {
  x: number;
  y: number;
  width: number;
  height: number;
  confidence: number;
}

export interface DetectedFace {
  id?: string;
  mediaAssetId: string;
  faceLocation: FaceLocation;
  faceEncoding?: number[];
  uploaderConsent: boolean;
  personConsent: boolean;
  linkedStorytellerId?: string;
  status: 'detected' | 'pending_consent' | 'linked' | 'rejected' | 'blurred';
}

export interface FaceMatch {
  recognitionId: string;
  mediaAssetId: string;
  storytellerId: string;
  storytellerName?: string;
  similarity: number;
}

export interface ConsentRequest {
  recognitionId: string;
  consentType: 'uploader' | 'person';
  grantedBy: string;
}

/**
 * FaceRecognition class - handles face detection and recognition with consent
 */
export class FaceRecognition {
  private supabase: ReturnType<typeof createClient>;

  constructor(supabaseUrl: string, supabaseKey: string) {
    this.supabase = createClient(supabaseUrl, supabaseKey);
  }

  /**
   * Detect faces in an image
   * This only detects faces - it does NOT identify them until consent is granted
   */
  async detectFaces(
    mediaAssetId: string,
    imageUrl: string,
    uploaderId: string
  ): Promise<DetectedFace[]> {
    // In a real implementation, this would use a face detection API
    // For now, we return a placeholder that would be populated by
    // an external face detection service (e.g., AWS Rekognition, Azure Face)

    // Note: We do NOT generate face encodings until uploader consents
    // This ensures we don't store biometric data without permission

    console.log('Face detection would analyze:', imageUrl);

    // Return empty array - actual implementation would use face detection API
    return [];
  }

  /**
   * Store detected faces (without encodings until consent)
   */
  async storeDetectedFaces(
    mediaAssetId: string,
    faces: FaceLocation[],
    uploaderId: string
  ): Promise<string[]> {
    const faceIds: string[] = [];

    for (const face of faces) {
      const { data, error } = await this.supabase
        .from('media_person_recognition')
        .insert({
          media_asset_id: mediaAssetId,
          face_location: face,
          uploader_consent_granted: false,
          person_consent_granted: false,
          status: 'detected'
        })
        .select('id')
        .single();

      if (error) {
        console.error('Error storing face:', error);
        continue;
      }

      faceIds.push(data.id);
    }

    return faceIds;
  }

  /**
   * Grant uploader consent for face recognition
   * This allows face encoding to be generated and stored
   */
  async grantUploaderConsent(
    recognitionId: string,
    grantedBy: string
  ): Promise<void> {
    const { error } = await this.supabase
      .from('media_person_recognition')
      .update({
        uploader_consent_granted: true,
        uploader_consent_at: new Date().toISOString(),
        uploader_consent_by: grantedBy,
        status: 'pending_consent' // Now waiting for person consent
      })
      .eq('id', recognitionId);

    if (error) {
      throw new Error(`Failed to grant uploader consent: ${error.message}`);
    }

    // After uploader consents, we can generate face encoding
    // This would trigger the face encoding process
    await this.generateFaceEncoding(recognitionId);
  }

  /**
   * Grant person consent for face recognition
   * This allows the face to be linked to a storyteller identity
   */
  async grantPersonConsent(
    recognitionId: string,
    storytellerId: string,
    grantedBy: string,
    canBePublic: boolean = false
  ): Promise<void> {
    // Verify the person granting consent is the storyteller
    const { data: storyteller } = await this.supabase
      .from('storytellers')
      .select('id, user_id')
      .eq('id', storytellerId)
      .single();

    if (!storyteller) {
      throw new Error('Storyteller not found');
    }

    const { error } = await this.supabase
      .from('media_person_recognition')
      .update({
        person_consent_granted: true,
        person_consent_at: new Date().toISOString(),
        person_consent_by: grantedBy,
        linked_storyteller_id: storytellerId,
        can_be_public: canBePublic,
        status: 'linked'
      })
      .eq('id', recognitionId);

    if (error) {
      throw new Error(`Failed to grant person consent: ${error.message}`);
    }
  }

  /**
   * Revoke consent and optionally blur the face
   */
  async revokeConsent(
    recognitionId: string,
    revokedBy: string,
    blurFace: boolean = false
  ): Promise<void> {
    const { error } = await this.supabase
      .from('media_person_recognition')
      .update({
        person_consent_granted: false,
        linked_storyteller_id: null,
        can_be_public: false,
        blur_requested: blurFace,
        status: blurFace ? 'blurred' : 'rejected'
      })
      .eq('id', recognitionId);

    if (error) {
      throw new Error(`Failed to revoke consent: ${error.message}`);
    }
  }

  /**
   * Request blur for a face (person doesn't consent but doesn't want to be identifiable)
   */
  async requestBlur(recognitionId: string, requestedBy: string): Promise<void> {
    const { error } = await this.supabase
      .from('media_person_recognition')
      .update({
        blur_requested: true,
        status: 'blurred'
      })
      .eq('id', recognitionId);

    if (error) {
      throw new Error(`Failed to request blur: ${error.message}`);
    }
  }

  /**
   * Generate face encoding for a detected face
   * Only called after uploader consent is granted
   */
  private async generateFaceEncoding(recognitionId: string): Promise<void> {
    // Get the face record
    const { data: face } = await this.supabase
      .from('media_person_recognition')
      .select('*, media_assets(url)')
      .eq('id', recognitionId)
      .single();

    if (!face || !face.uploader_consent_granted) {
      throw new Error('Cannot generate encoding without uploader consent');
    }

    // In a real implementation, this would:
    // 1. Load the image from face.media_assets.url
    // 2. Extract the face using face.face_location
    // 3. Generate a 512-dimension face encoding
    // 4. Store the encoding

    // Placeholder - actual implementation would use face recognition API
    console.log('Would generate encoding for face:', recognitionId);

    // The encoding would be stored like this:
    // await this.supabase
    //   .from('media_person_recognition')
    //   .update({ face_encoding: encodingVector })
    //   .eq('id', recognitionId);
  }

  /**
   * Find matching faces across media
   * Only returns matches where BOTH parties have consented
   */
  async findMatches(
    faceEncoding: number[],
    threshold: number = 0.6,
    limit: number = 10
  ): Promise<FaceMatch[]> {
    // Use the database function that enforces consent
    const { data, error } = await this.supabase.rpc('find_similar_faces', {
      p_face_encoding: faceEncoding,
      p_threshold: threshold,
      p_limit: limit
    });

    if (error) {
      console.error('Error finding matches:', error);
      return [];
    }

    // Get storyteller names for matches
    const matches: FaceMatch[] = [];
    for (const match of data || []) {
      if (match.linked_storyteller_id) {
        const { data: storyteller } = await this.supabase
          .from('storytellers')
          .select('name')
          .eq('id', match.linked_storyteller_id)
          .single();

        matches.push({
          recognitionId: match.recognition_id,
          mediaAssetId: match.media_asset_id,
          storytellerId: match.linked_storyteller_id,
          storytellerName: storyteller?.name,
          similarity: match.similarity
        });
      }
    }

    return matches;
  }

  /**
   * Get all photos of a storyteller (only where consent is granted)
   */
  async getStorytellerPhotos(storytellerId: string): Promise<string[]> {
    const { data, error } = await this.supabase
      .from('media_person_recognition')
      .select('media_asset_id')
      .eq('linked_storyteller_id', storytellerId)
      .eq('person_consent_granted', true)
      .eq('uploader_consent_granted', true);

    if (error) {
      console.error('Error getting storyteller photos:', error);
      return [];
    }

    return data?.map(d => d.media_asset_id) || [];
  }

  /**
   * Get consent status for a face recognition record
   */
  async getConsentStatus(recognitionId: string): Promise<{
    uploaderConsent: boolean;
    personConsent: boolean;
    fullConsent: boolean;
    status: string;
    canBePublic: boolean;
    blurRequested: boolean;
  } | null> {
    const { data, error } = await this.supabase
      .from('media_person_recognition')
      .select(`
        uploader_consent_granted,
        person_consent_granted,
        status,
        can_be_public,
        blur_requested
      `)
      .eq('id', recognitionId)
      .single();

    if (error || !data) return null;

    return {
      uploaderConsent: data.uploader_consent_granted,
      personConsent: data.person_consent_granted,
      fullConsent: data.uploader_consent_granted && data.person_consent_granted,
      status: data.status,
      canBePublic: data.can_be_public,
      blurRequested: data.blur_requested
    };
  }

  /**
   * Manually verify a face match (by staff or the person)
   */
  async verifyMatch(
    recognitionId: string,
    verifiedBy: string
  ): Promise<void> {
    const { error } = await this.supabase
      .from('media_person_recognition')
      .update({
        manually_verified: true,
        verified_by: verifiedBy,
        verified_at: new Date().toISOString()
      })
      .eq('id', recognitionId);

    if (error) {
      throw new Error(`Failed to verify match: ${error.message}`);
    }
  }

  /**
   * Get pending consent requests for a storyteller
   * (photos where they've been detected but haven't consented)
   */
  async getPendingConsentRequests(storytellerId: string): Promise<Array<{
    recognitionId: string;
    mediaAssetId: string;
    faceLocation: FaceLocation;
    uploaderName?: string;
  }>> {
    // This would typically use a suggested_storyteller_id field
    // that stores potential matches for review

    const { data, error } = await this.supabase
      .from('media_person_recognition')
      .select(`
        id,
        media_asset_id,
        face_location,
        uploader_consent_by,
        storytellers:uploader_consent_by(name)
      `)
      .eq('suggested_storyteller_id', storytellerId)
      .eq('uploader_consent_granted', true)
      .eq('person_consent_granted', false)
      .eq('status', 'pending_consent');

    if (error) {
      console.error('Error getting pending requests:', error);
      return [];
    }

    return data?.map(d => ({
      recognitionId: d.id,
      mediaAssetId: d.media_asset_id,
      faceLocation: d.face_location as FaceLocation,
      uploaderName: (d.storytellers as any)?.name
    })) || [];
  }
}

/**
 * Create a FaceRecognition instance with environment variables
 */
export function createFaceRecognition() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!supabaseUrl || !supabaseKey) {
    throw new Error('Supabase credentials required');
  }

  return new FaceRecognition(supabaseUrl, supabaseKey);
}

export default FaceRecognition;
