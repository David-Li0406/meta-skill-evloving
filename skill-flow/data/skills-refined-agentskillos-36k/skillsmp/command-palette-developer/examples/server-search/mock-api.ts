/**
 * Mock API for server search demonstration
 * Simulates a real search endpoint with delays, pagination, and errors
 */

export interface SearchResultItem {
  id: string;
  type: 'user' | 'post' | 'product';
  title: string;
  description?: string;
  avatar?: string;
  date?: string;
  tags?: string[];
  relevanceScore?: number;
}

export interface SearchResponse {
  items: SearchResultItem[];
  total: number;
  page: number;
  hasMore: boolean;
  nextCursor?: number;
}

/**
 * Mock dataset (1000 items)
 */
const MOCK_DATA: SearchResultItem[] = generateMockData(1000);

/**
 * Simulated search API endpoint
 * @param query - Search query string
 * @param page - Page number (0-indexed)
 * @param pageSize - Number of items per page (default: 20)
 * @returns Promise resolving to search results
 */
export async function searchApi(
  query: string,
  page: number = 0,
  pageSize: number = 20
): Promise<SearchResponse> {
  // Simulate network delay (200-500ms)
  const delay = Math.random() * 300 + 200;
  await new Promise((resolve) => setTimeout(resolve, delay));

  // Simulate random errors (5% chance)
  if (Math.random() < 0.05) {
    throw new Error('Network error: Unable to reach server');
  }

  // Fuzzy search implementation
  const results = fuzzySearch(query, MOCK_DATA);

  // Pagination
  const start = page * pageSize;
  const end = start + pageSize;
  const paginatedResults = results.slice(start, end);

  return {
    items: paginatedResults,
    total: results.length,
    page,
    hasMore: end < results.length,
    nextCursor: end < results.length ? page + 1 : undefined,
  };
}

/**
 * Fuzzy search with relevance scoring
 */
function fuzzySearch(
  query: string,
  data: SearchResultItem[]
): SearchResultItem[] {
  if (!query || query.length < 3) {
    return [];
  }

  const queryLower = query.toLowerCase();
  const terms = queryLower.split(/\s+/).filter((term) => term.length > 0);

  const scored = data
    .map((item) => {
      const titleLower = item.title.toLowerCase();
      const descriptionLower = item.description?.toLowerCase() || '';
      const tagsLower = item.tags?.join(' ').toLowerCase() || '';
      const searchText = `${titleLower} ${descriptionLower} ${tagsLower}`;

      let score = 0;

      for (const term of terms) {
        // Title exact match (highest score)
        if (titleLower === term) {
          score += 100;
        }
        // Title starts with term
        else if (titleLower.startsWith(term)) {
          score += 50;
        }
        // Title contains term
        else if (titleLower.includes(term)) {
          score += 25;
        }
        // Description contains term
        else if (descriptionLower.includes(term)) {
          score += 10;
        }
        // Tags contain term
        else if (tagsLower.includes(term)) {
          score += 15;
        }
        // Fuzzy match (Levenshtein-like)
        else {
          const fuzzyScore = calculateFuzzyScore(term, titleLower);
          score += fuzzyScore;
        }
      }

      return {
        item: { ...item, relevanceScore: Math.min(score / 100, 1) },
        score,
      };
    })
    .filter((result) => result.score > 0)
    .sort((a, b) => b.score - a.score)
    .map((result) => result.item);

  return scored;
}

/**
 * Simple fuzzy matching score
 */
function calculateFuzzyScore(term: string, text: string): number {
  let score = 0;
  let termIndex = 0;

  for (let i = 0; i < text.length && termIndex < term.length; i++) {
    if (text[i] === term[termIndex]) {
      score += 1;
      termIndex++;
    }
  }

  return termIndex === term.length ? score : 0;
}

/**
 * Generate mock dataset
 */
function generateMockData(count: number): SearchResultItem[] {
  const data: SearchResultItem[] = [];

  const firstNames = [
    'Alice',
    'Bob',
    'Charlie',
    'Diana',
    'Eve',
    'Frank',
    'Grace',
    'Henry',
    'Ivy',
    'Jack',
    'Kate',
    'Leo',
    'Maya',
    'Noah',
    'Olivia',
    'Peter',
    'Quinn',
    'Rose',
    'Sam',
    'Tina',
  ];

  const lastNames = [
    'Smith',
    'Johnson',
    'Williams',
    'Brown',
    'Jones',
    'Garcia',
    'Miller',
    'Davis',
    'Rodriguez',
    'Martinez',
  ];

  const postTitles = [
    'Getting Started with React',
    'TypeScript Best Practices',
    'Building Scalable APIs',
    'Database Design Patterns',
    'Modern CSS Techniques',
    'Testing Strategies',
    'Performance Optimization',
    'Security Best Practices',
    'Cloud Architecture',
    'DevOps Fundamentals',
  ];

  const productNames = [
    'Wireless Headphones',
    'Smart Watch',
    'Laptop Stand',
    'Mechanical Keyboard',
    'USB-C Hub',
    'Monitor Arm',
    'Desk Lamp',
    'Ergonomic Chair',
    'Webcam',
    'Microphone',
  ];

  const techTags = [
    'react',
    'typescript',
    'javascript',
    'node',
    'python',
    'rust',
    'go',
    'docker',
    'kubernetes',
    'aws',
    'azure',
    'frontend',
    'backend',
    'fullstack',
    'api',
    'database',
    'testing',
    'performance',
    'security',
  ];

  for (let i = 0; i < count; i++) {
    const type = ['user', 'post', 'product'][i % 3] as
      | 'user'
      | 'post'
      | 'product';

    if (type === 'user') {
      const firstName = firstNames[i % firstNames.length];
      const lastName = lastNames[Math.floor(i / firstNames.length) % lastNames.length];
      data.push({
        id: `user-${i}`,
        type: 'user',
        title: `${firstName} ${lastName}`,
        description: `Software Engineer specializing in ${techTags[i % techTags.length]}`,
        avatar: `https://i.pravatar.cc/150?img=${(i % 70) + 1}`,
        date: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString(),
        tags: [
          techTags[i % techTags.length],
          techTags[(i + 1) % techTags.length],
        ],
      });
    } else if (type === 'post') {
      const title = postTitles[i % postTitles.length];
      data.push({
        id: `post-${i}`,
        type: 'post',
        title: `${title} ${i > 10 ? `Part ${Math.floor(i / 10)}` : ''}`,
        description: `A comprehensive guide to ${title.toLowerCase()} with practical examples and best practices.`,
        date: new Date(Date.now() - Math.random() * 180 * 24 * 60 * 60 * 1000).toISOString(),
        tags: [
          techTags[i % techTags.length],
          techTags[(i + 2) % techTags.length],
          techTags[(i + 3) % techTags.length],
        ],
      });
    } else {
      const product = productNames[i % productNames.length];
      data.push({
        id: `product-${i}`,
        type: 'product',
        title: `${product} ${i > 10 ? `Pro ${Math.floor(i / 10)}` : ''}`,
        description: `High-quality ${product.toLowerCase()} with premium features and modern design.`,
        date: new Date(Date.now() - Math.random() * 90 * 24 * 60 * 60 * 1000).toISOString(),
        tags: ['electronics', 'tech', 'gadgets'].slice(0, 2),
      });
    }
  }

  return data;
}
