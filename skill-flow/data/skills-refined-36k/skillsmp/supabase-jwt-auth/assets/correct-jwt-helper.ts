import { createClient } from '@/utils/supabase/server';

/**
 * JWTメタデータの型定義
 */
export interface JWTMetadata {
  role: 'site_admin' | 'company_admin' | 'facility_admin' | 'staff';
  company_id: string;
  current_facility_id: string | null;
}

/**
 * 認証済みユーザーのJWTメタデータを取得
 *
 * 重要: Supabase Auth APIのgetClaims()を使用して、署名検証済みのJWTクレームを取得します。
 * これにより、トークンの改ざんを防ぎ、セキュアな認証を実現します。
 *
 * @returns JWTメタデータまたはnull（認証エラー時）
 */
export async function getAuthenticatedUserMetadata(): Promise<JWTMetadata | null> {
  const supabase = await createClient();

  // getClaimsで署名検証済みのカスタムクレームを取得
  const {
    data: claims,
    error: claimsError,
  } = await supabase.auth.getClaims();

  if (claimsError) {
    console.error('Failed to get JWT claims:', claimsError.message);
    return null;
  }

  if (!claims) {
    return null;
  }

  // app_metadataからカスタムクレームを取得
  const role = claims.app_metadata?.role;
  const company_id = claims.app_metadata?.company_id;
  const current_facility_id = claims.app_metadata?.current_facility_id;

  // 型の検証
  const validRoles = ['site_admin', 'company_admin', 'facility_admin', 'staff'] as const;
  if (!role || typeof role !== 'string' || !validRoles.includes(role as any)) {
    console.error('Invalid or missing role in JWT claims');
    return null;
  }

  // 必須フィールドの検証
  if (typeof company_id !== 'string' || !company_id) {
    console.error('Missing required JWT claims: role or company_id');
    return null;
  }

  if (current_facility_id !== null && typeof current_facility_id !== 'string') {
    console.error('Invalid type for current_facility_id in JWT claims');
    return null;
  }

  // site_admin以外は施設IDが必須
  if (role !== 'site_admin' && !current_facility_id) {
    console.error('Missing required JWT claim: current_facility_id for non-site_admin user');
    return null;
  }

  return {
    role,
    company_id,
    current_facility_id: current_facility_id || null,
  };
}

/**
 * 権限チェック用のヘルパー
 */
export function hasPermission(
  metadata: JWTMetadata,
  allowedRoles: JWTMetadata['role'][]
): boolean {
  return allowedRoles.includes(metadata.role);
}
