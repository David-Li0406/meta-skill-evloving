# Troubleshooting Guide

## Common Issues

### 0. `session.user.app_metadata`でカスタムクレームが取得できない（最重要）

**症状:**
- Hookは「Hook ran successfully」と表示される
- PostgreSQL関数も正常に動作している（ログでクレーム追加を確認済み）
- しかし、`session.user.app_metadata`にカスタムクレーム（role、company_id等）が含まれていない

**原因:**
Supabase SDKの`session.user.app_metadata`は、Custom Access Token Hookで追加したカスタムクレームを反映しません。

**解決方法:**
JWTトークンを直接デコードして`payload.app_metadata`から取得してください。

```typescript
// ❌ 間違った方法（動作しない）
const { data: { session } } = await supabase.auth.getSession();
const role = session.user.app_metadata?.role; // 取得できない

// ✅ 正しい方法
const { data: { session } } = await supabase.auth.getSession();
const accessToken = session.access_token;
const tokenParts = accessToken.split('.');
const payload = JSON.parse(Buffer.from(tokenParts[1], 'base64').toString());

const role = payload.app_metadata?.role; // 正しく取得できる
const company_id = payload.app_metadata?.company_id;
const current_facility_id = payload.app_metadata?.current_facility_id;
```

**確認方法:**
デバッグAPIを作成してJWTペイロードを確認：
```typescript
// app/api/debug/jwt/route.ts
export async function GET() {
  const supabase = await createClient();
  const { data: { session } } = await supabase.auth.getSession();

  const accessToken = session.access_token;
  const payload = JSON.parse(Buffer.from(accessToken.split('.')[1], 'base64').toString());

  return NextResponse.json({
    user_app_metadata: session.user.app_metadata, // カスタムクレームなし
    jwt_payload: payload, // カスタムクレームあり
  });
}
```

**Hookが正常動作しているか確認:**
PostgreSQL Logsで以下のメッセージを確認：
```
custom_access_token_hook: Adding claims for user_id=..., claims={...}
```

このログが出ているのに`session.user.app_metadata`が空の場合、**JWTデコードが必要**です。

### 1. app_metadata is Empty or Missing

**Symptoms**: JWT token doesn't contain `app_metadata` or the fields are empty.

**Causes**:
- Hook not configured in Supabase Dashboard
- Hook not enabled
- Function returns NULL for the user

**Solutions**:

1. **Verify Hook Configuration**:
   - Go to Supabase Dashboard > Database > Hooks
   - Ensure hook exists with:
     - Event Type: "Custom Access Token (auth.jwt)"
     - Function: `public.custom_access_token_hook`
   - Hook should be enabled (green status)

2. **Test the Function Manually**:
   ```sql
   -- Replace user_id with actual UUID
   SELECT custom_access_token_hook(jsonb_build_object(
     'user_id', 'YOUR-USER-UUID',
     'claims', '{}'::jsonb
   ));
   ```
   - Should return jsonb with claims set
   - If returns NULL, check user exists and is active

3. **Re-login Required**:
   - JWT claims are set at login time
   - Log out and log back in to get new token with claims

### 2. current_facility_id is NULL

**Symptoms**: `role` and `company_id` are present, but `current_facility_id` is NULL.

**Causes**:
- User not assigned to any facility
- No primary facility set
- Facility relationship table missing data

**Solutions**:

1. **Check User-Facility Relationship**:
   ```sql
   SELECT * FROM _user_facility
   WHERE user_id = 'YOUR-USER-UUID'
   AND is_current = true;
   ```
   - Should return at least one row
   - At least one should have `is_primary = true`

2. **Assign User to Facility**:
   ```sql
   INSERT INTO _user_facility (user_id, facility_id, is_current, is_primary)
   VALUES ('USER-UUID', 'FACILITY-UUID', true, true);
   ```

3. **Update Hook Logic** (if using different schema):
   - Modify the function to match your facility assignment logic

### 3. JWT Claims Not Updating After Data Change

**Symptoms**: Changed user role or facility, but JWT still shows old values.

**Cause**: JWT claims are embedded at login time and don't auto-update.

**Solution**:
- Log out and log back in to get fresh JWT
- Or implement token refresh logic in your application

### 4. Permission Denied in API Routes

**Symptoms**: API returns 401/403 even with valid JWT.

**Causes**:
- `getAuthenticatedUserMetadata()` returns NULL
- Role check failing
- Missing required fields in JWT

**Solutions**:

1. **Debug JWT Content**:
   ```typescript
   const supabase = await createClient();
   const { data: { user } } = await supabase.auth.getUser();
   console.log('app_metadata:', user?.app_metadata);
   ```

2. **Check Required Fields**:
   ```typescript
   const metadata = await getAuthenticatedUserMetadata();
   if (!metadata) {
     // Log why it failed
     const { data: { user } } = await supabase.auth.getUser();
     console.error('Missing fields:', {
       role: user?.app_metadata?.role,
       company_id: user?.app_metadata?.company_id,
       current_facility_id: user?.app_metadata?.current_facility_id,
     });
   }
   ```

3. **Verify Role Permissions**:
   ```typescript
   if (!hasPermission(metadata, ['admin', 'staff'])) {
     // User role doesn't match allowed roles
   }
   ```

### 5. Function Execution Error

**Symptoms**: Authentication fails with database error.

**Causes**:
- Function references non-existent tables/columns
- Syntax error in function
- Missing permissions

**Solutions**:

1. **Check Function Exists**:
   ```sql
   SELECT proname, prosecdef
   FROM pg_proc
   WHERE proname = 'custom_access_token_hook';
   ```

2. **Check Function Permissions**:
   ```sql
   SELECT grantee, privilege_type
   FROM information_schema.routine_privileges
   WHERE routine_name = 'custom_access_token_hook';
   ```
   - Should have EXECUTE granted to `authenticated` and `service_role`

3. **Test Function Directly**:
   ```sql
   SELECT custom_access_token_hook(jsonb_build_object(
     'user_id', 'TEST-UUID',
     'claims', '{}'::jsonb
   ));
   ```
   - Check for SQL errors

### 6. Performance Issues

**Symptoms**: Login is slow after implementing JWT hooks.

**Causes**:
- Complex queries in hook function
- Missing database indexes
- N+1 query problems

**Solutions**:

1. **Add Indexes**:
   ```sql
   CREATE INDEX IF NOT EXISTS idx_user_facility_user_current
   ON _user_facility(user_id, is_current, is_primary);

   CREATE INDEX IF NOT EXISTS idx_users_active
   ON m_users(id) WHERE is_active = true AND deleted_at IS NULL;
   ```

2. **Optimize Function**:
   - Minimize number of queries
   - Use efficient WHERE clauses
   - Avoid complex joins

3. **Profile Function**:
   ```sql
   EXPLAIN ANALYZE
   SELECT custom_access_token_hook(jsonb_build_object(
     'user_id', 'YOUR-USER-UUID',
     'claims', '{}'::jsonb
   ));
   ```

## Debugging Checklist

When JWT authentication isn't working, check in this order:

1. ✅ Function exists and has correct code
2. ✅ Function has proper permissions (EXECUTE granted)
3. ✅ Hook is configured in Supabase Dashboard
4. ✅ Hook is enabled
5. ✅ User data exists and is valid (active, not deleted)
6. ✅ User has facility assignment
7. ✅ User logged out and logged back in (to get fresh token)
8. ✅ JWT contains app_metadata with all required fields
9. ✅ API route uses `getAuthenticatedUserMetadata()` correctly

## Getting Help

If issues persist:
1. Check Supabase logs for errors
2. Test function manually with SQL
3. Verify database schema matches function expectations
4. Check browser console for auth errors
5. Inspect JWT token at https://jwt.io
