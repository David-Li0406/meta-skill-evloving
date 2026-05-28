---
name: Referral System
description: Invite friends, referral tracking, and reward distribution
---

# Referral System Skill

## Database Schema
```sql
CREATE TABLE referrals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  referrer_id UUID REFERENCES auth.users NOT NULL,
  referred_id UUID REFERENCES auth.users,
  referral_code TEXT UNIQUE NOT NULL,
  status TEXT DEFAULT 'pending', -- pending, completed, rewarded
  reward_amount INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

CREATE INDEX idx_referrals_code ON referrals(referral_code);
CREATE INDEX idx_referrals_referrer ON referrals(referrer_id);

-- Generate unique referral code for user
CREATE OR REPLACE FUNCTION generate_referral_code(user_id UUID)
RETURNS TEXT AS $$
DECLARE
  code TEXT;
BEGIN
  -- Use first 8 chars of UUID + random suffix
  code := UPPER(SUBSTRING(user_id::TEXT, 1, 8)) || SUBSTRING(MD5(RANDOM()::TEXT), 1, 4);
  RETURN code;
END;
$$ LANGUAGE plpgsql;
```

## API Routes

### Get/Create Referral Code
```javascript
// pages/api/referral/code.js
export default async function handler(req, res) {
  const { user } = await getUser(req);
  
  // Check if user has a code
  let { data: referral } = await supabase
    .from('referrals')
    .select('referral_code')
    .eq('referrer_id', user.id)
    .is('referred_id', null)
    .single();
  
  if (!referral) {
    // Create new referral code
    const code = generateCode(user.id);
    const { data } = await supabase
      .from('referrals')
      .insert({ referrer_id: user.id, referral_code: code })
      .select()
      .single();
    referral = data;
  }
  
  res.json({
    code: referral.referral_code,
    url: `https://smarter.poker/join?ref=${referral.referral_code}`
  });
}
```

### Track Referral on Signup
```javascript
// In signup handler
export async function handleSignup(email, password, referralCode) {
  // Create user
  const { data: { user } } = await supabase.auth.signUp({ email, password });
  
  // Process referral if code provided
  if (referralCode) {
    await supabase
      .from('referrals')
      .update({
        referred_id: user.id,
        status: 'completed',
        completed_at: new Date().toISOString()
      })
      .eq('referral_code', referralCode)
      .is('referred_id', null);
    
    // Award referral bonus to referrer
    await awardReferralBonus(referralCode);
  }
  
  return user;
}

async function awardReferralBonus(code) {
  const { data: referral } = await supabase
    .from('referrals')
    .select('referrer_id')
    .eq('referral_code', code)
    .single();
  
  if (referral) {
    await supabase.rpc('add_diamonds', {
      user_id: referral.referrer_id,
      amount: 100 // Referral bonus
    });
    
    await supabase
      .from('referrals')
      .update({ status: 'rewarded', reward_amount: 100 })
      .eq('referral_code', code);
  }
}
```

## React Components

### Share Referral
```jsx
function ReferralShare() {
  const [referral, setReferral] = useState(null);
  
  useEffect(() => {
    fetch('/api/referral/code')
      .then(r => r.json())
      .then(setReferral);
  }, []);
  
  const copyToClipboard = () => {
    navigator.clipboard.writeText(referral.url);
    toast.success('Link copied!');
  };
  
  return (
    <div className="referral-card">
      <h3>Invite Friends, Earn Diamonds! 💎</h3>
      <p>Get 100 diamonds for every friend who joins</p>
      
      <div className="share-section">
        <input value={referral?.url} readOnly />
        <button onClick={copyToClipboard}>Copy Link</button>
      </div>
      
      <div className="share-buttons">
        <ShareButton platform="twitter" url={referral?.url} />
        <ShareButton platform="facebook" url={referral?.url} />
        <ShareButton platform="whatsapp" url={referral?.url} />
      </div>
      
      <QRCode value={referral?.url} size={150} />
    </div>
  );
}
```

### Referral Stats
```jsx
function ReferralStats({ userId }) {
  const { data } = useSWR(`/api/referral/stats?userId=${userId}`);
  
  return (
    <div>
      <Stat label="Total Invites Sent" value={data?.totalSent} />
      <Stat label="Successful Referrals" value={data?.completed} />
      <Stat label="Diamonds Earned" value={data?.totalRewards} />
    </div>
  );
}
```
