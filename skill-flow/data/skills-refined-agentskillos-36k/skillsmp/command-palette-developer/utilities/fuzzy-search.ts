// Fuzzy search utilities for command palette filtering

export function fuzzyMatch(query: string, target: string): boolean {
  const queryLower = query.toLowerCase();
  const targetLower = target.toLowerCase();
  let queryIndex = 0;

  for (let i = 0; i < targetLower.length && queryIndex < queryLower.length; i++) {
    if (targetLower[i] === queryLower[queryIndex]) {
      queryIndex++;
    }
  }

  return queryIndex === queryLower.length;
}

export function fuzzyScore(query: string, target: string): number {
  if (!query) return 0;

  const queryLower = query.toLowerCase();
  const targetLower = target.toLowerCase();

  // Exact match gets highest score
  if (targetLower === queryLower) return 1000;

  // Prefix match gets high score
  if (targetLower.startsWith(queryLower)) return 900;

  // Word boundary match
  const words = targetLower.split(/\s+/);
  for (const word of words) {
    if (word.startsWith(queryLower)) return 800;
  }

  // Fuzzy match score based on character matches and gaps
  let score = 0;
  let queryIndex = 0;
  let lastMatchIndex = -1;

  for (let i = 0; i < targetLower.length && queryIndex < queryLower.length; i++) {
    if (targetLower[i] === queryLower[queryIndex]) {
      // Consecutive matches get bonus
      const gap = lastMatchIndex >= 0 ? i - lastMatchIndex : 0;
      score += gap === 1 ? 10 : 5;

      queryIndex++;
      lastMatchIndex = i;
    }
  }

  return queryIndex === queryLower.length ? score : 0;
}

export function highlightMatches(query: string, target: string): React.ReactNode {
  if (!query) return target;

  const queryLower = query.toLowerCase();
  const targetLower = target.toLowerCase();
  const result: React.ReactNode[] = [];

  let queryIndex = 0;
  let lastIndex = 0;

  for (let i = 0; i < target.length && queryIndex < queryLower.length; i++) {
    if (targetLower[i] === queryLower[queryIndex]) {
      // Add text before match
      if (i > lastIndex) {
        result.push(target.substring(lastIndex, i));
      }

      // Add highlighted match
      result.push(<mark key={i}>{target[i]}</mark>);

      queryIndex++;
      lastIndex = i + 1;
    }
  }

  // Add remaining text
  if (lastIndex < target.length) {
    result.push(target.substring(lastIndex));
  }

  return <>{result}</>;
}
