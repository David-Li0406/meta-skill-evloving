export function generateSessionName(tool, taskDesc) {
  const cleaned = String(taskDesc || '')
    .replace(/^TASK:\s*/i, '')
    .trim();

  if (!cleaned) {
    return `${tool}-${Date.now()}`;
  }

  const verbRegex = /^(?:please\s+)?(?:review|build|fix|create|update|implement|analyze|test|debug|investigate|research|refactor|optimi[sz]e|document|improve|add|remove|audit|design|plan|migrate|upgrade|downgrade|setup|configure|integrate|deploy)\s+(?:the|a|an)?\s*(.+)$/i;
  const match = cleaned.match(verbRegex);
  let phrase = (match && match[1]) ? match[1] : cleaned;

  phrase = phrase.split(/[.?!:;]/)[0].trim();
  phrase = phrase.replace(/^(to|please|kindly)\s+/i, '');

  const words = phrase.split(/\s+/).filter(Boolean);
  const trimmedPhrase = words.slice(0, 8).join(' ');

  const slug = trimmedPhrase
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .substring(0, 40)
    .replace(/-+$/g, '');

  if (slug) {
    return `${tool}-${slug}`;
  }

  return `${tool}-${Date.now()}`;
}
