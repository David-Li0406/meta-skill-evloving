---
name: AI Coaching & Analysis
description: GPT-powered hand analysis, coaching, and personalized feedback
---

# AI Coaching & Analysis Skill

## Overview
Use GPT-4 for hand history analysis, coaching feedback, and personalized learning recommendations.

## Features
| Feature | Description |
|---------|-------------|
| Hand Analysis | Review played hands with GTO feedback |
| Coach Chat | Conversational poker coaching |
| Leak Detection | Identify systematic mistakes |
| Study Plan | Personalized training recommendations |
| Range Review | Validate range constructions |

## Hand Analysis Prompt
```javascript
async function analyzeHand(handHistory) {
  const prompt = `You are a GTO poker coach analyzing a hand. 
  
Hand History:
${JSON.stringify(handHistory, null, 2)}

Provide analysis including:
1. Preflop assessment (was the open/call/3bet correct?)
2. Postflop street-by-street analysis
3. Key decision points and GTO alternatives
4. EV estimate of decisions vs optimal
5. Summary of what to learn

Keep response concise but thorough.`;

  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 1000
  });
  
  return response.choices[0].message.content;
}
```

## Coach Chat System
```javascript
const COACH_SYSTEM_PROMPT = `You are a friendly, expert poker coach with deep GTO knowledge.
You help players improve by:
- Answering strategy questions
- Explaining concepts clearly
- Providing actionable advice
- Encouraging good habits
- Identifying and fixing leaks

Always be supportive but honest. Reference specific percentages and ranges when relevant.
Keep responses conversational but educational.`;

async function coachChat(messages, userContext) {
  const systemMessage = {
    role: 'system',
    content: COACH_SYSTEM_PROMPT + `\n\nUser Context:\n- XP Level: ${userContext.level}\n- Focus Areas: ${userContext.focusAreas.join(', ')}\n- Recent Games: ${userContext.recentGames.length}`
  };
  
  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [systemMessage, ...messages],
    max_tokens: 500
  });
  
  return response.choices[0].message.content;
}
```

## Leak Detection
```javascript
async function detectLeaks(userId) {
  // Get recent training results
  const { data: results } = await supabase
    .from('training_results')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false })
    .limit(100);
  
  // Analyze patterns
  const leaks = [];
  
  // Check preflop mistakes
  const preflopMistakes = results.filter(r => r.street === 'preflop' && !r.is_correct);
  if (preflopMistakes.length / results.length > 0.3) {
    leaks.push({
      type: 'PREFLOP_LEAKS',
      severity: 'high',
      description: 'Frequent preflop mistakes detected',
      recommendation: 'Focus on preflop range training'
    });
  }
  
  // Check position-based leaks
  const positionErrors = groupBy(results.filter(r => !r.is_correct), 'position');
  for (const [position, errors] of Object.entries(positionErrors)) {
    if (errors.length > 10) {
      leaks.push({
        type: 'POSITION_LEAK',
        severity: 'medium',
        description: `Struggles playing from ${position}`,
        recommendation: `Study ${position} ranges and strategies`
      });
    }
  }
  
  return leaks;
}
```

## Study Plan Generator
```javascript
async function generateStudyPlan(userId) {
  const leaks = await detectLeaks(userId);
  const { data: mastery } = await supabase.from('user_mastery').select('*').eq('user_id', userId);
  
  const prompt = `Generate a weekly poker study plan based on:
  
Player Leaks: ${JSON.stringify(leaks)}
Current Mastery: ${JSON.stringify(mastery)}

Create a 7-day plan with specific:
- Training games to play
- Concepts to study
- Time recommendations
- Priority areas

Format as JSON: { days: [{ day: 1, tasks: [...] }] }`;

  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: prompt }],
    response_format: { type: 'json_object' }
  });
  
  return JSON.parse(response.choices[0].message.content);
}
```

## Components
- `HandAnalyzer.jsx` - Hand review interface
- `CoachChat.jsx` - Chat with AI coach
- `LeakReport.jsx` - Weakness analysis
- `StudyPlan.jsx` - Weekly plan display
- `InsightCards.jsx` - Quick tips and insights
