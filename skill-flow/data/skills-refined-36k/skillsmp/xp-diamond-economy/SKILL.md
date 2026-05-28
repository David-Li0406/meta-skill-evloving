---
name: XP & Diamond Economy
description: Implement the XP progression and diamond reward systems
---

# XP & Diamond Economy Skill

## Overview
Manage the virtual economy consisting of XP (progression) and Diamonds (premium currency).

## XP System (Orb #1 DNA)

### XP Sources
| Action | XP Amount |
|--------|-----------|
| Post created | +10 XP |
| Post liked received | +2 XP |
| Comment created | +5 XP |
| Daily login | +25 XP |
| Training game completed | +50-200 XP |
| Correct GTO answer | +10 XP |
| Hand won | +5 XP |

### XP Award Function
```sql
CREATE OR REPLACE FUNCTION award_xp(
  p_user_id UUID,
  p_amount INTEGER,
  p_source TEXT
) RETURNS INTEGER AS $$
DECLARE
  v_new_total INTEGER;
BEGIN
  -- Update profile XP
  UPDATE profiles
  SET xp = xp + p_amount
  WHERE id = p_user_id
  RETURNING xp INTO v_new_total;
  
  -- Log the award
  INSERT INTO social_xp_log (user_id, amount, source, created_at)
  VALUES (p_user_id, p_amount, p_source, NOW());
  
  RETURN v_new_total;
END;
$$ LANGUAGE plpgsql;
```

### XP Tiers
```javascript
const XP_TIERS = [
  { level: 1, minXp: 0, title: 'Novice' },
  { level: 2, minXp: 100, title: 'Beginner' },
  { level: 3, minXp: 500, title: 'Amateur' },
  { level: 4, minXp: 1000, title: 'Student' },
  { level: 5, minXp: 2500, title: 'Enthusiast' },
  { level: 6, minXp: 5000, title: 'Regular' },
  { level: 7, minXp: 10000, title: 'Skilled' },
  { level: 8, minXp: 25000, title: 'Expert' },
  { level: 9, minXp: 50000, title: 'Master' },
  { level: 10, minXp: 100000, title: 'Legend' }
];
```

## Diamond System (Premium Currency)

### Diamond Sources
| Source | Amount |
|--------|--------|
| Daily bonus (VIP) | +10 💎 |
| Level up | +50 💎 |
| Tournament win | +100-1000 💎 |
| Purchase | Variable |
| Referral bonus | +500 💎 |

### Diamond Uses
| Use | Cost |
|-----|------|
| Custom avatar generation | 100 💎 |
| Premium training access | 50 💎/session |
| Tournament buy-in | Variable |
| Cosmetics | 50-500 💎 |

### Diamond Award Function
```sql
CREATE OR REPLACE FUNCTION award_diamonds(
  p_user_id UUID,
  p_amount INTEGER,
  p_source TEXT
) RETURNS INTEGER AS $$
DECLARE
  v_new_total INTEGER;
BEGIN
  -- Update profile diamonds
  UPDATE profiles
  SET diamonds = diamonds + p_amount
  WHERE id = p_user_id
  RETURNING diamonds INTO v_new_total;
  
  -- Log the transaction
  INSERT INTO diamond_ledger (user_id, amount, source, created_at)
  VALUES (p_user_id, p_amount, p_source, NOW());
  
  RETURN v_new_total;
END;
$$ LANGUAGE plpgsql;
```

### Spend Diamonds
```sql
CREATE OR REPLACE FUNCTION spend_diamonds(
  p_user_id UUID,
  p_amount INTEGER,
  p_purpose TEXT
) RETURNS BOOLEAN AS $$
DECLARE
  v_current INTEGER;
BEGIN
  -- Check balance
  SELECT diamonds INTO v_current FROM profiles WHERE id = p_user_id;
  
  IF v_current < p_amount THEN
    RETURN FALSE;
  END IF;
  
  -- Deduct
  UPDATE profiles SET diamonds = diamonds - p_amount WHERE id = p_user_id;
  
  -- Log
  INSERT INTO diamond_ledger (user_id, amount, source, created_at)
  VALUES (p_user_id, -p_amount, p_purpose, NOW());
  
  RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

## UI Components

### XP Progress Bar
```jsx
<div className="xp-bar">
  <div 
    className="xp-fill" 
    style={{ width: `${(xp / nextLevelXp) * 100}%` }}
  />
  <span className="xp-text">{xp} / {nextLevelXp} XP</span>
</div>
```

### Diamond Display
```jsx
<div className="diamond-wallet">
  <span className="diamond-icon">💎</span>
  <span className="diamond-amount">{diamonds.toLocaleString()}</span>
  <button className="add-diamonds">+</button>
</div>
```

## Security

### XP Abuse Prevention
```sql
-- Log suspicious activity
INSERT INTO xp_security_alerts (user_id, reason, details)
SELECT p_user_id, 'RAPID_XP_GAIN', 'Gained > 1000 XP in last hour'
WHERE (
  SELECT SUM(amount) FROM social_xp_log 
  WHERE user_id = p_user_id 
  AND created_at > NOW() - INTERVAL '1 hour'
) > 1000;
```

### Daily Caps
- Max 500 XP per day from social actions
- Max 1000 XP per day from training
- No cap on tournament/event XP
