---
name: Hand Evaluator
description: Poker hand ranking, comparison, and equity calculations
---

# Hand Evaluator Skill

## Overview
Evaluate poker hands, determine winners, and calculate equity.

## Hand Rankings (Highest to Lowest)
```javascript
const HAND_RANKS = {
  ROYAL_FLUSH: 10,
  STRAIGHT_FLUSH: 9,
  FOUR_OF_A_KIND: 8,
  FULL_HOUSE: 7,
  FLUSH: 6,
  STRAIGHT: 5,
  THREE_OF_A_KIND: 4,
  TWO_PAIR: 3,
  ONE_PAIR: 2,
  HIGH_CARD: 1
};
```

## Card Representation
```javascript
// Card = { rank: 2-14, suit: 's'|'h'|'d'|'c' }
// 14 = Ace, 13 = King, 12 = Queen, 11 = Jack

function parseCard(str) {
  const ranks = { 'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10 };
  const rank = ranks[str[0]] || parseInt(str[0]);
  const suit = str[1].toLowerCase();
  return { rank, suit };
}

// "As" -> { rank: 14, suit: 's' }
// "Th" -> { rank: 10, suit: 'h' }
```

## Hand Evaluator
```javascript
function evaluateHand(cards) {
  // Sort by rank descending
  const sorted = [...cards].sort((a, b) => b.rank - a.rank);
  
  const isFlush = cards.every(c => c.suit === cards[0].suit);
  const isStraight = checkStraight(sorted);
  const groups = groupByRank(sorted);
  
  // Royal Flush
  if (isFlush && isStraight && sorted[0].rank === 14 && sorted[4].rank === 10) {
    return { rank: HAND_RANKS.ROYAL_FLUSH, name: 'Royal Flush', cards: sorted };
  }
  
  // Straight Flush
  if (isFlush && isStraight) {
    return { rank: HAND_RANKS.STRAIGHT_FLUSH, name: 'Straight Flush', cards: sorted };
  }
  
  // Four of a Kind
  if (groups[0].count === 4) {
    return { rank: HAND_RANKS.FOUR_OF_A_KIND, name: 'Four of a Kind', cards: sorted };
  }
  
  // Full House
  if (groups[0].count === 3 && groups[1].count === 2) {
    return { rank: HAND_RANKS.FULL_HOUSE, name: 'Full House', cards: sorted };
  }
  
  // Flush
  if (isFlush) {
    return { rank: HAND_RANKS.FLUSH, name: 'Flush', cards: sorted };
  }
  
  // Straight
  if (isStraight) {
    return { rank: HAND_RANKS.STRAIGHT, name: 'Straight', cards: sorted };
  }
  
  // Three of a Kind
  if (groups[0].count === 3) {
    return { rank: HAND_RANKS.THREE_OF_A_KIND, name: 'Three of a Kind', cards: sorted };
  }
  
  // Two Pair
  if (groups[0].count === 2 && groups[1].count === 2) {
    return { rank: HAND_RANKS.TWO_PAIR, name: 'Two Pair', cards: sorted };
  }
  
  // One Pair
  if (groups[0].count === 2) {
    return { rank: HAND_RANKS.ONE_PAIR, name: 'One Pair', cards: sorted };
  }
  
  // High Card
  return { rank: HAND_RANKS.HIGH_CARD, name: 'High Card', cards: sorted };
}
```

## Best 5-Card Hand from 7
```javascript
function getBestHand(holeCards, communityCards) {
  const allCards = [...holeCards, ...communityCards];
  const combinations = getCombinations(allCards, 5);
  
  let bestHand = null;
  
  for (const combo of combinations) {
    const hand = evaluateHand(combo);
    if (!bestHand || compareHands(hand, bestHand) > 0) {
      bestHand = hand;
    }
  }
  
  return bestHand;
}
```

## Compare Hands
```javascript
function compareHands(hand1, hand2) {
  // Compare hand ranks first
  if (hand1.rank !== hand2.rank) {
    return hand1.rank - hand2.rank;
  }
  
  // Same rank, compare kickers
  for (let i = 0; i < hand1.cards.length; i++) {
    if (hand1.cards[i].rank !== hand2.cards[i].rank) {
      return hand1.cards[i].rank - hand2.cards[i].rank;
    }
  }
  
  return 0; // Tie
}
```

## Determine Winners
```javascript
function determineWinners(players, communityCards) {
  const results = players.map(player => ({
    player,
    hand: getBestHand(player.holeCards, communityCards)
  }));
  
  results.sort((a, b) => compareHands(b.hand, a.hand));
  
  // Find all winners (can be ties)
  const winners = [results[0]];
  for (let i = 1; i < results.length; i++) {
    if (compareHands(results[i].hand, results[0].hand) === 0) {
      winners.push(results[i]);
    } else {
      break;
    }
  }
  
  return winners;
}
```

## Equity Calculator
```javascript
async function calculateEquity(holeCards, communityCards, numOpponents = 1) {
  const deck = createDeck().filter(c => 
    !holeCards.includes(c) && !communityCards.includes(c)
  );
  
  const simulations = 10000;
  let wins = 0;
  let ties = 0;
  
  for (let i = 0; i < simulations; i++) {
    const shuffled = shuffle([...deck]);
    
    // Deal opponent cards
    const opponentCards = shuffled.slice(0, numOpponents * 2);
    const remainingBoard = shuffled.slice(numOpponents * 2, numOpponents * 2 + (5 - communityCards.length));
    
    const fullBoard = [...communityCards, ...remainingBoard];
    
    const heroHand = getBestHand(holeCards, fullBoard);
    const opponentHand = getBestHand(opponentCards.slice(0, 2), fullBoard);
    
    const comparison = compareHands(heroHand, opponentHand);
    if (comparison > 0) wins++;
    else if (comparison === 0) ties++;
  }
  
  return {
    win: wins / simulations,
    tie: ties / simulations,
    lose: 1 - (wins + ties) / simulations
  };
}
```

## Hand Notation
```javascript
// Convert hand to notation
function handToNotation(cards) {
  const c1 = cards[0], c2 = cards[1];
  const rankNames = { 14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T' };
  
  const r1 = rankNames[c1.rank] || c1.rank;
  const r2 = rankNames[c2.rank] || c2.rank;
  
  if (c1.rank === c2.rank) {
    return `${r1}${r2}`; // Pairs: "AA", "KK"
  }
  
  const suited = c1.suit === c2.suit ? 's' : 'o';
  const [high, low] = c1.rank > c2.rank ? [r1, r2] : [r2, r1];
  
  return `${high}${low}${suited}`; // "AKs", "QJo"
}
```
