```sql
CREATE TABLE public.profiles (
  id bigint primary key generated always as identity,
  user_id uuid not null references auth.users(id) on delete cascade,
  username text unique not null,
  phone text unique,
  email text not null,
  role text not null default 'user' check (role in ('admin', 'agent', 'user')),
  points_balance numeric not null default 0,
  invited_by bigint references public.profiles(id),
  invite_code text unique not null,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Indexes for performance
CREATE INDEX idx_profiles_user_id ON public.profiles(user_id);
CREATE INDEX idx_profiles_invited_by ON public.profiles(invited_by);
CREATE INDEX idx_profiles_invite_code ON public.profiles(invite_code);
CREATE INDEX idx_profiles_role ON public.profiles(role);
CREATE INDEX idx_profiles_phone ON public.profiles(phone);
CREATE INDEX idx_profiles_email ON public.profiles(email);

-- Table for points transactions
CREATE TABLE public.points_transactions (
  id bigint primary key generated always as identity,
  profile_id bigint not null references public.profiles(id) on delete cascade,
  transaction_type text not null check (transaction_type in ('recharge', 'spend', 'transfer')),
  amount numeric not null,
  balance_after numeric not null,
  description text,
  reference_id text,
  user_input_file_url text,
  ai_response_file_url text,
  is_successful boolean default true,
  created_at timestamp with time zone default now()
);

CREATE INDEX idx_points_transactions_profile_id ON public.points_transactions(profile_id);
CREATE INDEX idx_points_transactions_created_at ON public.points_transactions(created_at);
CREATE INDEX idx_points_transactions_type ON public.points_transactions(transaction_type);

-- Enable RLS on tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.points_transactions ENABLE ROW LEVEL SECURITY;

-- Create views for agent dashboard
CREATE VIEW public.agent_referrals WITH (security_invoker=on) AS
SELECT
  p.id,
  p.username,
  p.points_balance,
  p.created_at,
  count(children.id) as total_downline_count
FROM public.profiles p
LEFT JOIN public.profiles children ON children.invited_by = p.id
WHERE p.role = 'agent'
GROUP BY p.id, p.username, p.points_balance, p.created_at;

CREATE VIEW public.user_referral_tree WITH (security_invoker=on) AS
SELECT
  p.id,
  p.username,
  p.role,
  p.points_balance,
  inviter.username as inviter_username,
  inviter.role as inviter_role
FROM public.profiles p
LEFT JOIN public.profiles inviter ON p.invited_by = inviter.id;
```
