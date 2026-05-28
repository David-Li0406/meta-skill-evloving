# Supabase Security - Sharp Edges

## Rls Disabled Table

### **Id**
rls-disabled-table
### **Summary**
Table with RLS disabled exposes all data
### **Severity**
critical
### **Situation**
  You create a table and forget to enable RLS. Or you disable it
  for testing and forget to re-enable. Anyone with the anon key
  can now read and write all data in that table.
  
### **Why**
  By default, tables are accessible to anyone. RLS is opt-in.
  The anon key is public (in your frontend bundle). Without RLS,
  that key grants full access to the table.
  
### **Solution**
  -- Enable RLS on EVERY table
  alter table users enable row level security;
  alter table posts enable row level security;
  alter table comments enable row level security;
  
  -- Even for public data, enable RLS with permissive policy
  alter table public_posts enable row level security;
  create policy "Anyone can read" on public_posts
    for select using (true);
  
### **Symptoms**
  - Data visible to unauthenticated users
  - Users can see other users data
  - Data modified without authorization

## Service Role Exposed

### **Id**
service-role-exposed
### **Summary**
Service role key in client-side code
### **Severity**
critical
### **Situation**
  You need to bypass RLS for an admin feature. You use the service
  role key. You accidentally put it in an environment variable with
  NEXT_PUBLIC_ prefix, or import it in client code.
  
### **Why**
  Service role key bypasses ALL security. Anyone can extract it from
  your frontend bundle. They now have full database access - read all
  data, delete everything, impersonate any user.
  
### **Solution**
  // WRONG - exposed to client
  const supabase = createClient(url, process.env.NEXT_PUBLIC_SERVICE_KEY);
  
  // RIGHT - server only
  // In server action or API route:
  const supabaseAdmin = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_SERVICE_ROLE_KEY  // No NEXT_PUBLIC_
  );
  
  // Check your .env files:
  // .env.local should have:
  // SUPABASE_SERVICE_ROLE_KEY=...  (no NEXT_PUBLIC_)
  
### **Symptoms**
  - Service key visible in browser devtools
  - Unauthorized data access
  - Data deletion or corruption

## Policy Missing Auth Check

### **Id**
policy-missing-auth-check
### **Summary**
RLS policy without auth.uid() check
### **Severity**
critical
### **Situation**
  You write a policy that checks a column value but forgets to verify
  the user owns the row. Users can manipulate the query to access
  other users data.
  
### **Why**
  RLS policies must anchor to auth.uid(). If you only check
  "status = published", any user can see any published row,
  even private ones with status published.
  
### **Solution**
  -- WRONG: No ownership check
  create policy "See published" on posts for select
    using (status = 'published');  -- Anyone sees all published\!
  
  -- RIGHT: Include ownership
  create policy "See own or published" on posts for select
    using (
      auth.uid() = author_id OR status = 'published'
    );
  
### **Symptoms**
  - Users see data they should not
  - Private data leaks

## Insert Without User Id

### **Id**
insert-without-user-id
### **Summary**
INSERT policy allows any user_id value
### **Severity**
high
### **Situation**
  Your INSERT policy uses with check (true) or forgets to verify
  user_id matches auth.uid(). Users can insert records as other users.
  
### **Why**
  INSERT policies need with check, not using. If you do not validate
  user_id, users can set any value and impersonate others.
  
### **Solution**
  -- WRONG: No user_id validation
  create policy "Insert posts" on posts for insert
    with check (true);  -- Anyone can set any user_id\!
  
  -- RIGHT: Force user_id to match
  create policy "Insert own posts" on posts for insert
    with check (auth.uid() = user_id);
  
  -- Also validate other fields
  create policy "Insert safe" on posts for insert
    with check (
      auth.uid() = user_id AND
      status in ('draft', 'published')
    );
  
### **Symptoms**
  - Records created with wrong user_id
  - Impersonation attacks

## Update Missing With Check

### **Id**
update-missing-with-check
### **Summary**
UPDATE policy without with check allows privilege escalation
### **Severity**
high
### **Situation**
  Your UPDATE policy only has using() but no with check(). Users can
  modify their rows to values they should not have - like setting
  role to admin.
  
### **Why**
  using() controls which rows are visible. with check() controls what
  values are allowed. Without with check, any value can be written.
  
### **Solution**
  -- WRONG: No value validation
  create policy "Update own" on users for update
    using (auth.uid() = id);  -- Can set role = 'admin'\!
  
  -- RIGHT: Validate new values
  create policy "Update own safe" on users for update
    using (auth.uid() = id)
    with check (
      auth.uid() = id AND
      role = (select role from users where id = auth.uid())
    );
  
### **Symptoms**
  - Users elevate their own privileges
  - Protected fields modified

## Storage Public Bucket

### **Id**
storage-public-bucket
### **Summary**
Storage bucket set to public unintentionally
### **Severity**
high
### **Situation**
  You create a bucket for user uploads and set public = true to make
  URLs work. Now anyone can list and download all files without auth.
  
### **Why**
  Public buckets expose all files via predictable URLs. Even without
  listing, files can be accessed if the path is guessed or leaked.
  
### **Solution**
  -- Create PRIVATE bucket
  insert into storage.buckets (id, name, public)
  values ('uploads', 'uploads', false);  -- public = false\!
  
  -- Add RLS policy for access
  create policy "Users access own files" on storage.objects
    for select using (
      bucket_id = 'uploads' and
      auth.uid()::text = (storage.foldername(name))[1]
    );
  
  -- For downloads, use signed URLs from server
  
### **Symptoms**
  - Files accessible without login
  - Private files exposed publicly

## Policy Performance

### **Id**
policy-performance
### **Summary**
Complex RLS policy causes slow queries
### **Severity**
medium
### **Situation**
  Your policy does a subquery or function call. Every query now takes
  seconds instead of milliseconds. The table grows and it gets worse.
  
### **Why**
  RLS policies run on every row. Complex logic means complex execution
  on every query. No index can help if the policy itself is slow.
  
### **Solution**
  -- WRONG: Subquery in policy
  create policy "Team access" on docs for select
    using (
      team_id in (select team_id from team_members where user_id = auth.uid())
    );  -- Runs subquery for EVERY row\!
  
  -- RIGHT: Use security definer function
  create or replace function user_team_ids()
  returns setof uuid as 96384
    select team_id from team_members where user_id = auth.uid()
  96384 language sql security definer stable;
  
  -- Cache result per query
  create policy "Team access" on docs for select
    using (team_id in (select user_team_ids()));
  
  -- Add index
  create index idx_team_members_user on team_members(user_id);
  
### **Symptoms**
  - Queries take seconds
  - Performance degrades with data growth