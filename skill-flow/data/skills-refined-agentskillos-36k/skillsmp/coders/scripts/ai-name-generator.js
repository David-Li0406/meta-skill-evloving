/**
 * AI-powered session name generator using Claude Haiku
 *
 * Generates meaningful 2-4 word slugs from task descriptions.
 * Fast, with graceful fallback on failures.
 */

const HAIKU_MODEL = 'claude-haiku-4-20250414';
const TIMEOUT_MS = 3000; // 3 second timeout for fast responses

/**
 * Generate a session name using Claude Haiku
 *
 * @param {string} taskDescription - The task description to generate a name from
 * @returns {Promise<{slug: string, displayName: string} | null>} Generated names or null on failure
 */
export async function generateAISessionName(taskDescription) {
  const apiKey = process.env.ANTHROPIC_API_KEY;

  if (!apiKey) {
    return null;
  }

  const cleaned = String(taskDescription || '')
    .replace(/^TASK:\s*/i, '')
    .trim();

  if (!cleaned || cleaned.length < 5) {
    return null;
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: HAIKU_MODEL,
        max_tokens: 100,
        messages: [{
          role: 'user',
          content: `Generate a short name for this coding task. Return ONLY a JSON object with two fields:
- "slug": 2-4 word kebab-case identifier (lowercase, hyphens, max 30 chars). Examples: "auth-refactor", "fix-login-bug", "add-dark-mode"
- "displayName": A brief human-readable title (3-6 words, title case). Examples: "Authentication Refactor", "Fix Login Bug", "Add Dark Mode Support"

Task: "${cleaned.substring(0, 200)}"

Return only the JSON object, no explanation.`
        }]
      }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    const content = data.content?.[0]?.text?.trim();

    if (!content) {
      return null;
    }

    // Parse JSON response - handle potential markdown code blocks
    let jsonStr = content;
    const jsonMatch = content.match(/```(?:json)?\s*(\{[\s\S]*?\})\s*```/);
    if (jsonMatch) {
      jsonStr = jsonMatch[1];
    }

    const parsed = JSON.parse(jsonStr);

    // Validate and sanitize the slug
    let slug = String(parsed.slug || '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .substring(0, 30)
      .replace(/-+$/g, '');

    const displayName = String(parsed.displayName || '')
      .substring(0, 60)
      .trim();

    if (!slug || slug.length < 3) {
      return null;
    }

    return {
      slug,
      displayName: displayName || slug
    };

  } catch (error) {
    clearTimeout(timeoutId);
    // Silent failure - caller will use fallback
    return null;
  }
}

/**
 * Generate session name with AI, falling back to regex-based extraction
 *
 * @param {string} tool - The AI tool being used (claude, gemini, etc.)
 * @param {string} taskDescription - The task description
 * @param {boolean} useAI - Whether to attempt AI generation (default: true)
 * @returns {Promise<{sessionName: string, displayName: string}>}
 */
export async function generateSmartSessionName(tool, taskDescription, useAI = true) {
  // Import the fallback generator
  const { generateSessionName } = await import('./session-name.js');

  // Try AI generation first if enabled and API key is set
  if (useAI && process.env.ANTHROPIC_API_KEY) {
    const aiResult = await generateAISessionName(taskDescription);

    if (aiResult) {
      return {
        sessionName: `${tool}-${aiResult.slug}`,
        displayName: aiResult.displayName
      };
    }
  }

  // Fallback to regex-based generation
  const sessionName = generateSessionName(tool, taskDescription);

  // Create a display name from the session name
  const displayName = sessionName
    .replace(/^[a-z]+-/, '') // Remove tool prefix
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');

  return {
    sessionName,
    displayName
  };
}

export default {
  generateAISessionName,
  generateSmartSessionName
};
