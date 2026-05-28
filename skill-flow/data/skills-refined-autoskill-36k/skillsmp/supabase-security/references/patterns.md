# Supabase Security

## Patterns


---
  #### **Name**
RLS Policy Types
  #### **Description**
All four policy types
  #### **When**
Setting up table security
  #### **Example**
    -- SELECT policy
    create policy "Users see own" on profiles for select
      using (auth.uid() = user_id);
    
    -- INSERT policy
    create policy "Users create own" on profiles for insert
      with check (auth.uid() = user_id);
    
    -- UPDATE policy (needs both)
    create policy "Users update own" on profiles for update
      using (auth.uid() = user_id)
      with check (auth.uid() = user_id);
    
    -- DELETE policy
    create policy "Users delete own" on profiles for delete
      using (auth.uid() = user_id);
    

---
  #### **Name**
Role-Based Access Control
  #### **Description**
RBAC using JWT claims
  #### **When**
Different permissions per role
  #### **Example**
    create or replace function is_admin()
    returns boolean as $$
      select coalesce(
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin',
        false
      );
    $$ language sql security definer;
    
    create policy "Admin access" on admin_data for all
      using (is_admin());
    

---
  #### **Name**
Multi-Tenant RLS
  #### **Description**
Isolate data between orgs
  #### **When**
SaaS with multiple organizations
  #### **Example**
    create or replace function user_org_ids()
    returns setof uuid as $$
      select org_id from org_members
      where user_id = auth.uid()
    $$ language sql security definer stable;
    
    create policy "Org access" on projects for select
      using (org_id in (select user_org_ids()));
    
    -- CRITICAL: Index for performance
    create index idx_org_members_user on org_members(user_id);
    

---
  #### **Name**
Storage Security
  #### **Description**
Secure file uploads
  #### **When**
Private file storage
  #### **Example**
    -- Private bucket
    insert into storage.buckets (id, name, public)
    values ('user-files', 'user-files', false);
    
    -- User folder policy: user-files/{user_id}/file.ext
    create policy "Own files" on storage.objects for select
      using (
        bucket_id = 'user-files' and
        auth.uid()::text = (storage.foldername(name))[1]
      );
    

---
  #### **Name**
Service Role vs Anon Key
  #### **Description**
When to use each
  #### **When**
Choosing auth method
  #### **Example**
    // ANON KEY - safe for client, subject to RLS
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
    );
    
    // SERVICE ROLE - BYPASSES RLS, server only\!
    const supabaseAdmin = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_SERVICE_ROLE_KEY  // NO NEXT_PUBLIC_\!
    );
    

---
  #### **Name**
Edge Function Auth
  #### **Description**
Verify tokens in Edge Functions
  #### **When**
Serverless functions
  #### **Example**
    const authHeader = req.headers.get("Authorization");
    const supabase = createClient(url, anonKey, {
      global: { headers: { Authorization: authHeader } }
    });
    const { data: { user } } = await supabase.auth.getUser();
    if (\!user) return new Response("Unauthorized", { status: 401 });
    

---
  #### **Name**
Preventing IDOR
  #### **Description**
Insecure Direct Object Reference
  #### **When**
APIs taking IDs from client
  #### **Example**
    -- Without RLS, client can query any user:
    -- .from("profiles").eq("id", anyUserId)
    
    -- With RLS policy, safe:
    create policy "Own profile" on profiles for select
      using (auth.uid() = id);
    

---
  #### **Name**
Preventing Privilege Escalation
  #### **Description**
Stop role self-elevation
  #### **When**
User profiles with roles
  #### **Example**
    create policy "Update own profile" on users for update
      using (auth.uid() = id)
      with check (
        role = (select role from users where id = auth.uid())
      );
    -- Role must stay unchanged
    

## Anti-Patterns


---
  #### **Name**
RLS Disabled
  #### **Description**
Tables without RLS
  #### **Why**
Anyone can read/write all data
  #### **Instead**
Enable RLS on every table

---
  #### **Name**
Service Role in Client
  #### **Description**
Service key in frontend
  #### **Why**
Full database access exposed
  #### **Instead**
Server only, no NEXT_PUBLIC_

---
  #### **Name**
Trusting Client ID
  #### **Description**
Client-provided user_id
  #### **Why**
Users can impersonate others
  #### **Instead**
Always use auth.uid()

---
  #### **Name**
Complex Policy Logic
  #### **Description**
Business logic in policies
  #### **Why**
Kills performance
  #### **Instead**
Use security definer functions

---
  #### **Name**
Missing Policy Indexes
  #### **Description**
RLS on non-indexed columns
  #### **Why**
Full table scan
  #### **Instead**
Index policy columns