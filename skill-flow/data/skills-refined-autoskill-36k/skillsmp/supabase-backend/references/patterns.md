# Supabase Backend

## Patterns


---
  #### **Name**
Basic RLS Policy
  #### **Description**
Enable RLS and create policies for authenticated access
  #### **When**
Creating any table that users will access
  #### **Example**
    -- Enable RLS (do this on EVERY table)
    alter table posts enable row level security;
    
    -- Users can only see their own posts
    create policy "Users view own posts"
      on posts for select
      using (auth.uid() = user_id);
    
    -- Users can only insert their own posts
    create policy "Users insert own posts"
      on posts for insert
      with check (auth.uid() = user_id);
    

---
  #### **Name**
Public Read, Auth Write
  #### **Description**
Anyone can read, only authenticated users can write
  #### **When**
Public content like blog posts or product listings
  #### **Example**
    -- Anyone can view
    create policy "Public read"
      on posts for select
      using (true);
    
    -- Only authenticated users can insert
    create policy "Auth users insert"
      on posts for insert
      to authenticated
      with check (auth.uid() = author_id);
    

---
  #### **Name**
Server Action with Service Role
  #### **Description**
Use service role for admin operations in Server Actions
  #### **When**
You need to bypass RLS for admin functionality
  #### **Example**
    // app/actions.ts
    'use server'
    import { createClient } from '@supabase/supabase-js'
    
    const supabaseAdmin = createClient(
      process.env.SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    )
    
    export async function adminDeleteUser(userId: string) {
      // This bypasses RLS - use carefully
      await supabaseAdmin.from('users').delete().eq('id', userId)
    }
    

---
  #### **Name**
Realtime with RLS
  #### **Description**
Set up realtime subscriptions that respect RLS
  #### **When**
Building real-time features like chat or notifications
  #### **Example**
    // Client side - RLS filters what you receive
    const channel = supabase
      .channel('messages')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'messages' },
        (payload) => {
          // You'll only receive messages your RLS policy allows
          setMessages(prev => [...prev, payload.new])
        }
      )
      .subscribe()
    

---
  #### **Name**
Storage with RLS
  #### **Description**
Protect storage buckets with RLS policies
  #### **When**
Users upload files that should be private or restricted
  #### **Example**
    -- Create bucket with RLS
    insert into storage.buckets (id, name, public)
    values ('avatars', 'avatars', false);
    
    -- Users can upload to their own folder
    create policy "Users upload own avatar"
      on storage.objects for insert
      with check (
        bucket_id = 'avatars' and
        auth.uid()::text = (storage.foldername(name))[1]
      );
    

## Anti-Patterns


---
  #### **Name**
Disabled RLS
  #### **Description**
Leaving RLS disabled on tables with user data
  #### **Why**
Anyone with the anon key can read/write all data
  #### **Instead**
Always enable RLS, even if policy is permissive

---
  #### **Name**
Service Role on Client
  #### **Description**
Using SUPABASE_SERVICE_ROLE_KEY in client code
  #### **Why**
Exposes full database access to anyone who views page source
  #### **Instead**
Only use service role in server-side code (Server Actions, API routes)

---
  #### **Name**
Complex Policy Logic
  #### **Description**
Writing complex business logic in RLS policies
  #### **Why**
Policies run on every query - complex logic kills performance
  #### **Instead**
Use database functions for complex checks, call from simple policies

---
  #### **Name**
Missing Index on Policy Column
  #### **Description**
RLS policy filters on non-indexed column
  #### **Why**
Every query does a full table scan - gets slow fast
  #### **Instead**
Add index on columns used in policies (especially user_id)

---
  #### **Name**
Trusting Client Data
  #### **Description**
Using client-provided data in RLS decisions
  #### **Why**
Clients can send any data - only trust auth.uid() and auth.jwt()
  #### **Instead**
Always use auth.uid() for user identity, not request data