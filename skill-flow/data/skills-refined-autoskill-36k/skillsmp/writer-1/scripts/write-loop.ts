#!/usr/bin/env npx tsx
import { spawnSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { parseArgs } from 'node:util'
import { query, type Message } from '@anthropic-ai/claude-code'

const templates = {
  post: `<role>Technical blog post writer</role>

<structure>
- Hook: 1-2 sentences that grab attention
- Problem: What issue does this solve?
- Solution: Step-by-step with code examples
- Takeaways: 2-3 bullet points
- Conclusion: Call to action or next steps
</structure>

<format>
- Use ## for main sections
- Use \`\`\` for code blocks with language tags
- Keep paragraphs short (2-3 sentences max)
</format>

<example>
Input: "How to use TypeScript generics for type-safe API calls"
Output:
## Stop Writing Unsafe API Calls

Every API call is a potential runtime error waiting to happen...

## The Problem
When fetching data, TypeScript can't verify the response shape...

## The Solution
\`\`\`typescript
async function fetchApi<T>(url: string): Promise<T> {
  const res = await fetch(url)
  return res.json() as T
}
\`\`\`

## Key Takeaways
- Generics let you define the shape at call-site
- Use type guards for runtime validation
- Combine with zod for full safety

## Next Steps
Try refactoring one API call in your codebase today.
</example>`,

  doc: `<role>Technical documentation writer</role>

<structure>
## Overview
One paragraph explaining what this is and why it matters.

## Installation
\`\`\`bash
# exact commands to install
\`\`\`

## Quick Start
Minimal working example to get started fast.

## API Reference
Functions/methods with params, return types, examples.

## Examples
Real-world usage patterns.
</structure>

<format>
- Use ## for sections, ### for subsections
- Every code block needs a language tag
- Tables for API params: | Param | Type | Description |
</format>

<example>
Input: "Document a useLocalStorage composable"
Output:
## Overview
\`useLocalStorage\` syncs reactive state with localStorage, handling SSR and serialization automatically.

## Installation
\`\`\`bash
npm install @vueuse/core
\`\`\`

## Quick Start
\`\`\`vue
<script setup>
const count = useLocalStorage('counter', 0)
</script>
<template>
  <button @click="count++">{{ count }}</button>
</template>
\`\`\`

## API Reference
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| key | string | required | localStorage key |
| initialValue | T | required | Default value |

## Examples
\`\`\`typescript
// With custom serializer
const user = useLocalStorage('user', null, {
  serializer: { read: JSON.parse, write: JSON.stringify }
})
\`\`\`
</example>`,

  'github-issue': `<role>GitHub issue writer</role>

<structure>
## Problem
What's broken or missing? Be specific.

## Expected Behavior
What should happen instead?

## Current Behavior
What happens now? Include error messages if any.

## Reproduction
Steps or minimal code to reproduce.

## Tasks
Checkbox list of work items.
</structure>

<format>
Output JSON: { "title": "concise title under 60 chars", "body": "markdown body" }
</format>

<example>
Input: "useAsyncData doesn't refresh when key changes"
Output:
{
  "title": "useAsyncData ignores key changes after initial fetch",
  "body": "## Problem\\nChanging the key parameter doesn't trigger a refetch.\\n\\n## Expected Behavior\\nData should refetch when key changes, like React Query.\\n\\n## Current Behavior\\nInitial fetch works, subsequent key changes are ignored.\\n\\n## Reproduction\\n\`\`\`vue\\n<script setup>\\nconst id = ref(1)\\nconst { data } = useAsyncData(\`user-\${id.value}\`, () => fetchUser(id.value))\\nid.value = 2 // doesn't refetch\\n</script>\\n\`\`\`\\n\\n## Tasks\\n- [ ] Add key reactivity\\n- [ ] Add tests\\n- [ ] Update docs"
}
</example>`,
}

const deeplDefaults: Record<string, { style: string, tone: string }> = {
  post: { style: 'business', tone: 'friendly' },
  doc: { style: 'simple', tone: 'confident' },
  'github-issue': { style: 'business', tone: 'diplomatic' },
}

const { values, positionals } = parseArgs({
  args: process.argv.slice(2),
  options: {
    context: { type: 'string', short: 'c' },
    template: { type: 'string', short: 't', default: 'post' },
    'max-iterations': { type: 'string', short: 'm', default: '15' },
    'no-grammar': { type: 'boolean', default: false },
    style: { type: 'string', short: 's' },
    tone: { type: 'string', short: 'o' },
    lang: { type: 'string', short: 'l', default: 'en-US' },
  },
  allowPositionals: true,
})

const template = (values.template || 'post') as keyof typeof templates
const description = positionals.join(' ')
const maxIterations = Number.parseInt(values['max-iterations'] || '5', 10)
const skipGrammar = values['no-grammar'] || false
const templateDefaults = deeplDefaults[template] || deeplDefaults.post
const writingStyle = values.style || templateDefaults.style
const writingTone = values.tone || templateDefaults.tone
const targetLang = values.lang || 'en-US'

if (!description) {
  console.error('Usage: npx tsx write-loop.ts "description" [--template post|doc|github-issue] [--context file.md]')
  process.exit(1)
}

const contextContent = values.context ? readFileSync(values.context, 'utf-8') : ''

async function callGemini(prompt: string, feedback?: string): Promise<string | null> {
  const systemPrompt = templates[template]
  let userPrompt = contextContent
    ? `<context>\n${contextContent}\n</context>\n\n<task>\n${prompt}\n</task>`
    : prompt

  if (feedback) {
    userPrompt += `\n\n<feedback>\nPrevious draft received this feedback. Please revise:\n${feedback}\n</feedback>`
  }

  // Try gemini-cli first
  const result = spawnSync('gemini', [
    '--model', 'gemini-3-pro-preview',
    '-p', `${systemPrompt}\n\n${userPrompt}`,
  ], { encoding: 'utf-8', timeout: 180000 })

  if (result.status === 0 && result.stdout) {
    return result.stdout
  }

  // Fallback to Vercel AI Gateway
  const apiKey = process.env.AI_GATEWAY_API_KEY
  if (!apiKey) {
    console.error('gemini-cli failed and AI_GATEWAY_API_KEY not set')
    return null
  }

  const response = await fetch('https://ai-gateway.vercel.sh/v1/chat/completions', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'google/gemini-2.5-pro',
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt },
      ],
    }),
  })

  if (!response.ok) {
    console.error('Vercel AI Gateway error:', await response.text())
    return null
  }

  const data = await response.json() as { choices: { message: { content: string } }[] }
  return data.choices[0]?.message?.content || null
}

async function reviewWithClaude(draft: string): Promise<{ approved: boolean, feedback?: string }> {
  const reviewPrompt = `Review this draft for quality, clarity, and completeness.

<draft>
${draft}
</draft>

Evaluate:
1. Is the content accurate and well-structured?
2. Is the writing clear and concise?
3. Are code examples (if any) correct?
4. Is anything missing or unclear?

Respond with EXACTLY one of:
- "APPROVED" if the draft is ready to publish
- "FEEDBACK: <your specific feedback>" if revisions needed

Be strict but fair. Only approve if genuinely good.`

  let fullResponse = ''

  for await (const msg of query({
    prompt: reviewPrompt,
    options: {
      maxTurns: 1,
      allowedTools: [],
    },
  })) {
    if (msg.type === 'assistant' && msg.message?.content) {
      for (const block of msg.message.content) {
        if (block.type === 'text') fullResponse += block.text
      }
    }
  }

  const trimmed = fullResponse.trim()
  if (trimmed.startsWith('APPROVED')) {
    return { approved: true }
  }

  const feedbackMatch = trimmed.match(/^FEEDBACK:\s*(.+)/s)
  if (feedbackMatch) {
    return { approved: false, feedback: feedbackMatch[1].trim() }
  }

  // Default to feedback if unclear
  return { approved: false, feedback: trimmed }
}

async function improveWithDeepL(text: string, style: string, tone: string, lang: string): Promise<string | null> {
  const apiKey = process.env.DEEPL_API_KEY
  if (!apiKey) return null

  const response = await fetch('https://api.deepl.com/v2/write/rephrase', {
    method: 'POST',
    headers: { 'DeepL-Auth-Key': apiKey, 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: [text], target_lang: lang.replace('-', '_').toUpperCase(), writing_style: style, tone }),
  })

  if (!response.ok) {
    console.error('DeepL API error:', await response.text())
    return null
  }

  const data = await response.json() as { translations: { text: string }[] }
  return data.translations?.[0]?.text || null
}

async function mergeWithClaude(original: string, deeplOutput: string): Promise<string> {
  const mergePrompt = `Compare these two versions and merge intelligently.

<original>
${original}
</original>

<deepl_improved>
${deeplOutput}
</deepl_improved>

Apply DeepL's grammar/style improvements BUT preserve:
- Code blocks (\`\`\`...\`\`\`) exactly as in original
- Markdown structure (headers, lists, links)
- Technical terms and jargon
- Intentional stylistic choices from original

Output ONLY the merged text, no explanations.`

  let mergedText = ''
  for await (const msg of query({
    prompt: mergePrompt,
    options: { maxTurns: 1, allowedTools: [] },
  })) {
    if (msg.type === 'assistant' && msg.message?.content) {
      for (const block of msg.message.content) {
        if (block.type === 'text') mergedText += block.text
      }
    }
  }

  return mergedText.trim() || original
}

interface IterationLog {
  iteration: number
  status: 'approved' | 'needs_revision' | 'max_reached'
  feedback?: string
}

async function main() {
  console.log(`Writing ${template}: "${description}"`)
  console.log(`Max iterations: ${maxIterations}\n`)

  let feedback: string | undefined
  let finalDraft: string | null = null
  const iterationLogs: IterationLog[] = []

  for (let i = 1; i <= maxIterations; i++) {
    console.log(`--- Iteration ${i}/${maxIterations} ---`)
    console.log('Generating draft with Gemini...')

    const draft = await callGemini(description, feedback)
    if (!draft) {
      console.error('Failed to generate draft')
      process.exit(1)
    }

    console.log('Reviewing with Claude...')
    const review = await reviewWithClaude(draft)

    if (review.approved) {
      console.log('✓ Draft approved!\n')
      iterationLogs.push({ iteration: i, status: 'approved' })
      finalDraft = draft
      break
    }

    console.log(`✗ Feedback: ${review.feedback}\n`)
    iterationLogs.push({ iteration: i, status: 'needs_revision', feedback: review.feedback })
    feedback = review.feedback

    if (i === maxIterations) {
      console.log('Max iterations reached, using last draft.\n')
      iterationLogs[iterationLogs.length - 1].status = 'max_reached'
      finalDraft = draft
    }
  }

  if (finalDraft) {
    // Grammar improvement step
    if (!skipGrammar) {
      if (process.env.DEEPL_API_KEY) {
        console.log('=== GRAMMAR STEP ===')
        console.log(`Style: ${writingStyle}, Tone: ${writingTone}, Lang: ${targetLang}`)
        console.log('Improving with DeepL...')
        const improved = await improveWithDeepL(finalDraft, writingStyle, writingTone, targetLang)
        if (improved) {
          console.log('Merging with Claude...')
          finalDraft = await mergeWithClaude(finalDraft, improved)
          console.log('✓ Grammar step complete\n')
        } else {
          console.log('⚠ DeepL failed, skipping grammar step\n')
        }
      } else {
        console.log('⚠ DEEPL_API_KEY not set, skipping grammar step\n')
      }
    }

    console.log('=== FINAL DRAFT ===\n')
    console.log(finalDraft)
    console.log('\n=== ITERATION SUMMARY ===')
    console.log(`Total iterations: ${iterationLogs.length}/${maxIterations}`)
    const lastLog = iterationLogs[iterationLogs.length - 1]
    console.log(`Final status: ${lastLog.status === 'approved' ? '✓ Approved' : '⚠ Max iterations reached'}`)
    console.log('\nIteration history:')
    for (const log of iterationLogs) {
      const statusIcon = log.status === 'approved' ? '✓' : log.status === 'max_reached' ? '⚠' : '✗'
      const feedbackSummary = log.feedback ? ` - ${log.feedback.slice(0, 100)}${log.feedback.length > 100 ? '...' : ''}` : ''
      console.log(`  ${log.iteration}. [${statusIcon}] ${log.status}${feedbackSummary}`)
    }
    console.log('=========================\n')
  }
}

main().catch(console.error)
