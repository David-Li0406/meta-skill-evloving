---
name: bracket-generator
description: トーナメントブラケット（対戦表）の生成ロジックを実装。ブラケット生成、シード配置、BYE処理、次戦リンク設定時に使用。
allowed-tools: Read, Write, Edit, Grep, Glob
---

# トーナメントブラケット生成スキル

トーナメント対戦表（ブラケット）の生成ロジックを実装するためのガイドです。

## 対応フォーマット

- **single_elimination**: シングルエリミネーション（勝ち抜き）
- **double_elimination**: ダブルエリミネーション（敗者復活）
- **swiss**: スイスドロー
- **round_robin**: ラウンドロビン（総当たり）

## シングルエリミネーションのロジック

### 1. ラウンド数の計算

```typescript
const calculateRounds = (participantCount: number): number => {
  return Math.ceil(Math.log2(participantCount))
}
// 参加者8名 → 3ラウンド
// 参加者12名 → 4ラウンド（16枠）
```

### 2. BYE（不戦勝）の配置

```typescript
const calculateByes = (participantCount: number): number => {
  const totalSlots = Math.pow(2, calculateRounds(participantCount))
  return totalSlots - participantCount
}

// BYE配置ルール:
// - BYEは上位シードに優先的に割り当て
// - 1回戦でBYEを配置し、2回戦から対戦開始
```

### 3. シード配置アルゴリズム

```typescript
// スタンダードシード配置
// 8人の場合: [1,8], [4,5], [2,7], [3,6]
const generateSeeds = (size: number): number[][] => {
  if (size === 2) return [[1, 2]]

  const half = size / 2
  const upper = generateSeeds(half)

  return upper.flatMap((match, i) => [
    match,
    [size + 1 - match[0], size + 1 - match[1]]
  ])
}
```

### 4. マッチ構造

```typescript
interface Match {
  id: string
  tournament_id: string
  round: number          // 1から始まるラウンド番号
  match_number: number   // そのラウンド内の試合番号
  player1_id: string | null
  player2_id: string | null
  player1_score: number | null
  player2_score: number | null
  winner_id: string | null
  status: 'pending' | 'in_progress' | 'completed' | 'bye'
  next_match_id: string | null    // 勝者が進む次の試合
  next_match_slot: 1 | 2 | null   // 次の試合でのスロット位置
}
```

### 5. 次戦リンクの設定

```typescript
// ラウンドNの試合番号Mの勝者は
// ラウンドN+1の試合番号 ceil(M/2) に進む
// スロットは M が奇数なら1、偶数なら2

const calculateNextMatch = (round: number, matchNumber: number, totalRounds: number) => {
  if (round >= totalRounds) return null

  return {
    nextMatchNumber: Math.ceil(matchNumber / 2),
    nextMatchSlot: matchNumber % 2 === 1 ? 1 : 2
  }
}
```

## ブラケット生成の全体フロー

```typescript
const generateBracket = async (
  tournamentId: string,
  participants: Participant[]
) => {
  const count = participants.length
  const rounds = calculateRounds(count)
  const totalSlots = Math.pow(2, rounds)
  const byes = totalSlots - count

  // シードでソート（seed nullは最後）
  const seeded = [...participants].sort((a, b) =>
    (a.seed ?? Infinity) - (b.seed ?? Infinity)
  )

  // 全マッチを生成
  const matches: Match[] = []

  for (let round = 1; round <= rounds; round++) {
    const matchesInRound = Math.pow(2, rounds - round)

    for (let matchNum = 1; matchNum <= matchesInRound; matchNum++) {
      const match: Match = {
        id: crypto.randomUUID(),
        tournament_id: tournamentId,
        round,
        match_number: matchNum,
        player1_id: null,
        player2_id: null,
        status: 'pending',
        ...calculateNextMatch(round, matchNum, rounds)
      }

      // 1回戦のみプレイヤー配置
      if (round === 1) {
        const seeds = generateSeeds(totalSlots)
        const [seed1, seed2] = seeds[matchNum - 1]

        match.player1_id = seeded[seed1 - 1]?.user_id ?? null
        match.player2_id = seeded[seed2 - 1]?.user_id ?? null

        // BYE判定
        if (!match.player1_id || !match.player2_id) {
          match.status = 'bye'
          match.winner_id = match.player1_id || match.player2_id
        }
      }

      matches.push(match)
    }
  }

  // DBに保存
  await supabase.from('matches').insert(matches)

  // BYEの勝者を次戦に進める
  await advanceByeWinners(matches)

  return matches
}
```

## 関連ファイル

- `src/lib/tournament/bracket.ts` - ブラケット生成ロジック
- `src/components/tournament/RealtimeBracket.tsx` - ブラケット表示
- `src/types/tournament.ts` - 型定義
