---
name: Club Arena System
description: Build private poker club management and gameplay
---

# Club Arena System Skill

## Overview
Build private poker clubs with membership, table management, and settlement systems (Orb #2 - Yellow Ball).

## Features

### Club Management
- Create/manage private clubs
- Invite members
- Set club rules and stakes
- Agent management (club hosts)

### Table System
- Multiple tables per club
- Variable stakes
- Waiting lists
- Session tracking

### Settlement
- Club credit system
- Session reports
- Rake tracking
- Agent payouts

## Database Schema

### clubs
```sql
CREATE TABLE clubs (
  id UUID PRIMARY KEY,
  name TEXT,
  owner_id UUID REFERENCES auth.users(id),
  logo_url TEXT,
  description TEXT,
  settings JSONB,  -- Stakes, rules, etc.
  is_public BOOLEAN,
  member_count INTEGER,
  created_at TIMESTAMPTZ
);
```

### club_members
```sql
CREATE TABLE club_members (
  id UUID PRIMARY KEY,
  club_id UUID REFERENCES clubs(id),
  user_id UUID REFERENCES auth.users(id),
  role TEXT,  -- 'owner', 'agent', 'member'
  credits DECIMAL,
  joined_at TIMESTAMPTZ,
  UNIQUE(club_id, user_id)
);
```

### club_tables
```sql
CREATE TABLE club_tables (
  id UUID PRIMARY KEY,
  club_id UUID REFERENCES clubs(id),
  name TEXT,
  stakes TEXT,
  max_players INTEGER,
  current_players INTEGER,
  is_active BOOLEAN
);
```

## Club Creation Flow

```javascript
async function createClub(ownerId, clubData) {
  // 1. Create club
  const { data: club } = await supabase
    .from('clubs')
    .insert({
      name: clubData.name,
      owner_id: ownerId,
      settings: {
        default_stakes: '1/2',
        rake_percent: 5,
        max_buy_in: 200
      }
    })
    .select()
    .single();

  // 2. Add owner as member
  await supabase.from('club_members').insert({
    club_id: club.id,
    user_id: ownerId,
    role: 'owner',
    credits: 0
  });

  return club;
}
```

## Credit System

### Add Credits
```javascript
async function addCredits(clubId, userId, amount, agentId) {
  // Transaction
  await supabase.rpc('add_club_credits', {
    p_club_id: clubId,
    p_user_id: userId,
    p_amount: amount,
    p_agent_id: agentId
  });
}
```

### Settle Session
```javascript
async function settleSession(sessionId) {
  const { data: session } = await getSession(sessionId);
  
  for (const player of session.players) {
    const profit = player.end_stack - player.buy_in;
    await supabase.from('club_members')
      .update({ credits: supabase.sql`credits + ${profit}` })
      .eq('club_id', session.club_id)
      .eq('user_id', player.user_id);
  }
}
```

## UI Components

### ClubLobby.jsx
- Club list/grid
- Create club button
- Search/filter

### ClubDashboard.jsx
- Member list
- Active tables
- Credit management
- Settings

### ClubTable.jsx
- Extends PokerTable
- Club-specific branding
- Credit display

## Integration Points
- **Orb #1 (Social)**: Club chat, announcements
- **Orb #4 (GTO Trainer)**: Training tables within clubs
- **Horse AI**: Fill empty seats with club horses
