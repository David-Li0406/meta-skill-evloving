import { createClient } from '@/utils/supabase/server';

/**
 * JWTメタデータの型定義
 * アプリケーションに応じてroleの値をカスタマイズしてください
 */
export interface JWTMetadata {
  role: 'site_admin' | 'company_admin' | 'facility_admin' | 'staff';
  company_id: string;
  current_facility_id: string | null;
  // 必要に応じて追加のフィールドを定義
}

/**
 * 認証済みユーザーのJWTメタデータを取得
 * @returns JWTメタデータまたはnull（認証エラー時）
 */
export async function getAuthenticatedUserMetadata(): Promise<JWTMetadata | null> {
  const supabase = await createClient();

  const {
    data: { user },
    error: authError,
  } = await supabase.auth.getUser();

  if (authError || !user) {
    return null;
  }

  const { role, company_id, current_facility_id } = user.app_metadata || {};

  // 必須フィールドの検証
  if (!role || !company_id || !current_facility_id) {
    return null;
  }

  return {
    role,
    company_id,
    current_facility_id,
  };
}

/**
 * 権限チェック用のヘルパー
 * @param metadata JWTメタデータ
 * @param allowedRoles 許可するロールの配列
 * @returns 権限があればtrue
 */
export function hasPermission(
  metadata: JWTMetadata,
  allowedRoles: JWTMetadata['role'][]
): boolean {
  return allowedRoles.includes(metadata.role);
}
