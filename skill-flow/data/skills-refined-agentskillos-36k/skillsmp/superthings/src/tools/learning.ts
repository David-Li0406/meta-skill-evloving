import { z } from 'zod';
import { AbstractToolHandler, ToolDefinition } from '../lib/abstract-tool-handler.js';
import { promises as fs } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

// Schema definitions for patterns
const TitleTransformSchema = z.object({
  match: z.string().describe('Regex pattern to match'),
  transform: z.string().describe('Transform template using {original} placeholder'),
  confidence: z.number().default(0),
  examples: z.array(z.string()).default([]),
  last_used: z.string().optional()
});

const ProjectHintSchema = z.record(z.number()).describe('Project name to confidence count mapping');

const ExactOverrideSchema = z.object({
  title: z.string(),
  project: z.string().optional(),
  confidence: z.number().default(1)
});

const PatternsSchema = z.object({
  title_transforms: z.array(TitleTransformSchema).default([]),
  project_hints: z.record(ProjectHintSchema).default({}),
  exact_overrides: z.record(ExactOverrideSchema).default({}),
  stats: z.object({
    sessions_completed: z.number().default(0),
    items_processed: z.number().default(0),
    patterns_learned: z.number().default(0),
    accuracy_trend: z.array(z.number()).default([])
  }).default({
    sessions_completed: 0,
    items_processed: 0,
    patterns_learned: 0,
    accuracy_trend: []
  })
});

type Patterns = z.infer<typeof PatternsSchema>;
type TitleTransform = z.infer<typeof TitleTransformSchema>;

// Path to patterns file - use claudesync directory for cross-machine sync
const PATTERNS_PATH = join(homedir(), 'claudesync', 'servers', 'super-things', 'data', 'patterns.json');
const HISTORY_PATH = join(homedir(), 'claudesync', 'servers', 'super-things', 'data', 'history.jsonl');

// Tool parameter schemas
const ListPatternsSchema = z.object({});

const SuggestForTaskSchema = z.object({
  title: z.string().describe('The task title to get suggestions for')
});

const LogCorrectionSchema = z.object({
  original_title: z.string(),
  suggested_title: z.string().optional(),
  final_title: z.string(),
  suggested_project: z.string().optional(),
  final_project: z.string().optional(),
  title_accepted: z.boolean().optional(),
  project_accepted: z.boolean().optional()
});

const UpdatePatternSchema = z.object({
  pattern_type: z.enum(['title_transform', 'project_hint', 'exact_override']),
  key: z.string().describe('Pattern key (regex for transforms, keyword for hints, title for overrides)'),
  delta: z.number().optional().describe('Confidence change (+1, -1, etc.)'),
  new_transform: z.string().optional().describe('New transform value (for title_transforms only)')
});

const RemovePatternSchema = z.object({
  pattern_type: z.enum(['title_transform', 'project_hint', 'exact_override']),
  key: z.string().describe('Pattern key to remove'),
  confirm: z.literal(true).describe('Must be true to confirm deletion')
});

const LearnBatchSchema = z.object({
  decisions: z.array(z.object({
    task_id: z.string().optional(),
    original_title: z.string(),
    final_title: z.string(),
    final_project: z.string().optional(),
    title_suggestion_source: z.enum(['pattern', 'agent', 'user', 'none']).optional(),
    title_accepted: z.boolean()
  }))
});

type LearningParams =
  | z.infer<typeof ListPatternsSchema>
  | z.infer<typeof SuggestForTaskSchema>
  | z.infer<typeof LogCorrectionSchema>
  | z.infer<typeof UpdatePatternSchema>
  | z.infer<typeof RemovePatternSchema>
  | z.infer<typeof LearnBatchSchema>;

// Helper functions
async function loadPatterns(): Promise<Patterns> {
  try {
    const content = await fs.readFile(PATTERNS_PATH, 'utf-8');
    const parsed = JSON.parse(content);
    return PatternsSchema.parse(parsed);
  } catch {
    // Return default patterns if file doesn't exist or is invalid
    return PatternsSchema.parse({});
  }
}

async function savePatterns(patterns: Patterns): Promise<void> {
  // Ensure directory exists
  const dir = join(homedir(), 'claudesync', 'servers', 'super-things', 'data');
  await fs.mkdir(dir, { recursive: true });
  await fs.writeFile(PATTERNS_PATH, JSON.stringify(patterns, null, 2));
}

async function appendToHistory(entry: Record<string, unknown>): Promise<void> {
  const dir = join(homedir(), 'claudesync', 'servers', 'super-things', 'data');
  await fs.mkdir(dir, { recursive: true });
  const line = JSON.stringify({ ts: new Date().toISOString(), ...entry }) + '\n';
  await fs.appendFile(HISTORY_PATH, line);
}

interface Suggestion {
  title: string;
  project: string | null;
  confidence: number;
  source: 'exact_override' | 'title_transform' | 'project_hint' | 'none';
  rule: string | null;
  examples: string[];
}

function applyPatterns(title: string, patterns: Patterns): Suggestion {
  // Priority 1: Exact overrides
  const exactMatch = patterns.exact_overrides[title];
  if (exactMatch) {
    return {
      title: exactMatch.title,
      project: exactMatch.project || null,
      confidence: exactMatch.confidence,
      source: 'exact_override',
      rule: `Exact match: "${title}"`,
      examples: []
    };
  }

  // Priority 2: Title transforms (regex patterns)
  for (const transform of patterns.title_transforms) {
    const regex = new RegExp(transform.match, 'i');
    if (regex.test(title)) {
      const newTitle = transform.transform.replace('{original}', title);
      return {
        title: newTitle,
        project: null,
        confidence: transform.confidence,
        source: 'title_transform',
        rule: `Pattern: ${transform.match} → ${transform.transform}`,
        examples: transform.examples
      };
    }
  }

  // Priority 3: Project hints (keyword matching)
  const lowerTitle = title.toLowerCase();
  let bestProject: string | null = null;
  let bestConfidence = 0;
  let matchedKeyword: string | null = null;

  for (const [keyword, projectWeights] of Object.entries(patterns.project_hints)) {
    if (lowerTitle.includes(keyword.toLowerCase())) {
      for (const [project, weight] of Object.entries(projectWeights)) {
        if (weight > bestConfidence) {
          bestConfidence = weight;
          bestProject = project;
          matchedKeyword = keyword;
        }
      }
    }
  }

  if (bestProject) {
    return {
      title: title, // No title change for project hints
      project: bestProject,
      confidence: bestConfidence,
      source: 'project_hint',
      rule: `Keyword "${matchedKeyword}" → ${bestProject}`,
      examples: []
    };
  }

  // No pattern matched
  return {
    title: title,
    project: null,
    confidence: 0,
    source: 'none',
    rule: null,
    examples: []
  };
}

function learnTitlePattern(original: string, final: string): TitleTransform | null {
  // Try to extract a generalizable pattern
  // Common cases: "Fix X" -> "Delegate to Brianna: Fix X"

  // Check if final contains original
  if (final.includes(original)) {
    // Prefix pattern: Something was added before the original
    const prefix = final.substring(0, final.indexOf(original));
    if (prefix.length > 0) {
      // Look for common starting word
      const originalFirstWord = original.split(' ')[0];
      if (originalFirstWord && originalFirstWord.length >= 3) {
        return {
          match: `^${originalFirstWord} `,
          transform: `${prefix}{original}`,
          confidence: 1,
          examples: [original],
          last_used: new Date().toISOString()
        };
      }
    }
  }

  return null;
}

class LearningToolHandler extends AbstractToolHandler<LearningParams> {
  protected definitions: ToolDefinition<LearningParams>[] = [
    {
      name: 'things_list_patterns',
      description: 'List all learned patterns for title transforms and project hints. Use this to see what the learning system has learned from corrections.',
      schema: ListPatternsSchema
    },
    {
      name: 'things_suggest_for_task',
      description: 'Get learned suggestions for a task title with confidence scores. Returns suggested title, project, confidence level, and the pattern that matched.',
      schema: SuggestForTaskSchema
    },
    {
      name: 'things_log_correction',
      description: 'Log a correction to teach the learning system. Call this after a user corrects a suggestion to improve future accuracy.',
      schema: LogCorrectionSchema
    },
    {
      name: 'things_update_pattern',
      description: 'Directly update a pattern\'s confidence or transform value. Use to manually adjust learned patterns.',
      schema: UpdatePatternSchema
    },
    {
      name: 'things_remove_pattern',
      description: 'Remove a learned pattern that is no longer useful. Requires confirm=true.',
      schema: RemovePatternSchema
    },
    {
      name: 'things_learn_batch',
      description: 'Process a batch of triage decisions and update patterns. Use after completing a triage session to learn from all decisions at once.',
      schema: LearnBatchSchema
    }
  ];

  async execute(toolName: string, params: LearningParams): Promise<string> {
    switch (toolName) {
      case 'things_list_patterns':
        return this.listPatterns();
      case 'things_suggest_for_task':
        return this.suggestForTask(params as z.infer<typeof SuggestForTaskSchema>);
      case 'things_log_correction':
        return this.logCorrection(params as z.infer<typeof LogCorrectionSchema>);
      case 'things_update_pattern':
        return this.updatePattern(params as z.infer<typeof UpdatePatternSchema>);
      case 'things_remove_pattern':
        return this.removePattern(params as z.infer<typeof RemovePatternSchema>);
      case 'things_learn_batch':
        return this.learnBatch(params as z.infer<typeof LearnBatchSchema>);
      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  }

  private async listPatterns(): Promise<string> {
    const patterns = await loadPatterns();

    const summary = {
      title_transforms_count: patterns.title_transforms.length,
      project_hints_keywords: Object.keys(patterns.project_hints).length,
      exact_overrides_count: Object.keys(patterns.exact_overrides).length,
      stats: patterns.stats,
      patterns: {
        title_transforms: patterns.title_transforms.map(t => ({
          match: t.match,
          transform: t.transform,
          confidence: t.confidence,
          examples: t.examples.slice(0, 3),
          last_used: t.last_used
        })),
        project_hints: patterns.project_hints,
        exact_overrides: patterns.exact_overrides
      }
    };

    return JSON.stringify(summary, null, 2);
  }

  private async suggestForTask(params: z.infer<typeof SuggestForTaskSchema>): Promise<string> {
    const patterns = await loadPatterns();
    const suggestion = applyPatterns(params.title, patterns);

    return JSON.stringify({
      original: params.title,
      suggested_title: suggestion.title,
      suggested_project: suggestion.project,
      confidence: suggestion.confidence,
      pattern_source: suggestion.source,
      pattern_rule: suggestion.rule,
      examples: suggestion.examples,
      confidence_level: suggestion.confidence >= 10 ? 'high' :
                        suggestion.confidence >= 3 ? 'medium' : 'low',
      recommendation: suggestion.confidence >= 10 ? 'apply_silently' :
                      suggestion.confidence >= 3 ? 'auto_apply_with_indicator' :
                      'ask_user_confirmation'
    }, null, 2);
  }

  private async logCorrection(params: z.infer<typeof LogCorrectionSchema>): Promise<string> {
    const patterns = await loadPatterns();

    // Log to history
    await appendToHistory({
      original_title: params.original_title,
      suggested_title: params.suggested_title,
      final_title: params.final_title,
      suggested_project: params.suggested_project,
      final_project: params.final_project,
      title_accepted: params.title_accepted,
      project_accepted: params.project_accepted
    });

    let learned = false;

    // Update patterns based on feedback
    if (params.title_accepted && params.suggested_title) {
      // Find and increment confidence of matching pattern
      for (const transform of patterns.title_transforms) {
        const regex = new RegExp(transform.match, 'i');
        if (regex.test(params.original_title)) {
          transform.confidence++;
          transform.last_used = new Date().toISOString();
          if (!transform.examples.includes(params.original_title)) {
            transform.examples.push(params.original_title);
          }
          learned = true;
          break;
        }
      }
    } else if (params.final_title !== params.original_title && params.final_title !== params.suggested_title) {
      // User provided a different title - learn new pattern
      const newPattern = learnTitlePattern(params.original_title, params.final_title);
      if (newPattern) {
        // Check if similar pattern already exists
        const existingIndex = patterns.title_transforms.findIndex(t => t.match === newPattern.match);
        if (existingIndex >= 0) {
          // Update existing pattern
          patterns.title_transforms[existingIndex].confidence++;
          if (!patterns.title_transforms[existingIndex].examples.includes(params.original_title)) {
            patterns.title_transforms[existingIndex].examples.push(params.original_title);
          }
        } else {
          // Add new pattern
          patterns.title_transforms.push(newPattern);
          patterns.stats.patterns_learned++;
        }
        learned = true;
      }

      // Also add as exact override for this specific title
      patterns.exact_overrides[params.original_title] = {
        title: params.final_title,
        project: params.final_project,
        confidence: 1
      };
    }

    // Update project hints if project was accepted
    if (params.project_accepted && params.final_project) {
      // Extract keywords from title (simple word extraction)
      const keywords = params.original_title.toLowerCase().split(/\s+/).filter(w => w.length >= 4);
      for (const keyword of keywords) {
        if (!patterns.project_hints[keyword]) {
          patterns.project_hints[keyword] = {};
        }
        patterns.project_hints[keyword][params.final_project] =
          (patterns.project_hints[keyword][params.final_project] || 0) + 1;
        learned = true;
      }
    }

    patterns.stats.items_processed++;
    await savePatterns(patterns);

    return JSON.stringify({
      success: true,
      learned,
      message: learned ? 'Correction logged and patterns updated' : 'Correction logged (no new pattern learned)'
    });
  }

  private async updatePattern(params: z.infer<typeof UpdatePatternSchema>): Promise<string> {
    const patterns = await loadPatterns();

    switch (params.pattern_type) {
      case 'title_transform': {
        const transform = patterns.title_transforms.find(t => t.match === params.key);
        if (!transform) {
          return JSON.stringify({ success: false, error: `No title transform found with match: ${params.key}` });
        }
        if (params.delta !== undefined) {
          transform.confidence += params.delta;
        }
        if (params.new_transform !== undefined) {
          transform.transform = params.new_transform;
        }
        transform.last_used = new Date().toISOString();
        break;
      }
      case 'project_hint': {
        // params.key format: "keyword:project"
        const [keyword, project] = params.key.split(':');
        if (!keyword || !project) {
          return JSON.stringify({ success: false, error: 'Key must be in format "keyword:project"' });
        }
        if (!patterns.project_hints[keyword]) {
          patterns.project_hints[keyword] = {};
        }
        patterns.project_hints[keyword][project] =
          (patterns.project_hints[keyword][project] || 0) + (params.delta || 1);
        break;
      }
      case 'exact_override': {
        const override = patterns.exact_overrides[params.key];
        if (!override) {
          return JSON.stringify({ success: false, error: `No exact override found for: ${params.key}` });
        }
        if (params.delta !== undefined) {
          override.confidence += params.delta;
        }
        if (params.new_transform !== undefined) {
          override.title = params.new_transform;
        }
        break;
      }
    }

    await savePatterns(patterns);
    return JSON.stringify({ success: true, message: 'Pattern updated' });
  }

  private async removePattern(params: z.infer<typeof RemovePatternSchema>): Promise<string> {
    if (!params.confirm) {
      return JSON.stringify({ success: false, error: 'Must set confirm=true to delete pattern' });
    }

    const patterns = await loadPatterns();

    switch (params.pattern_type) {
      case 'title_transform': {
        const index = patterns.title_transforms.findIndex(t => t.match === params.key);
        if (index === -1) {
          return JSON.stringify({ success: false, error: `No title transform found with match: ${params.key}` });
        }
        patterns.title_transforms.splice(index, 1);
        break;
      }
      case 'project_hint': {
        if (!patterns.project_hints[params.key]) {
          return JSON.stringify({ success: false, error: `No project hint found for keyword: ${params.key}` });
        }
        delete patterns.project_hints[params.key];
        break;
      }
      case 'exact_override': {
        if (!patterns.exact_overrides[params.key]) {
          return JSON.stringify({ success: false, error: `No exact override found for: ${params.key}` });
        }
        delete patterns.exact_overrides[params.key];
        break;
      }
    }

    await savePatterns(patterns);
    return JSON.stringify({ success: true, message: `Pattern removed: ${params.pattern_type}/${params.key}` });
  }

  private async learnBatch(params: z.infer<typeof LearnBatchSchema>): Promise<string> {
    const patterns = await loadPatterns();
    let patternsLearned = 0;
    let confidenceUpdates = 0;

    for (const decision of params.decisions) {
      // Log to history
      await appendToHistory({
        original_title: decision.original_title,
        final_title: decision.final_title,
        final_project: decision.final_project,
        title_accepted: decision.title_accepted,
        source: decision.title_suggestion_source
      });

      if (decision.title_accepted && decision.title_suggestion_source === 'pattern') {
        // Find and increment confidence of matching pattern
        for (const transform of patterns.title_transforms) {
          const regex = new RegExp(transform.match, 'i');
          if (regex.test(decision.original_title)) {
            transform.confidence++;
            transform.last_used = new Date().toISOString();
            if (!transform.examples.includes(decision.original_title)) {
              transform.examples.push(decision.original_title);
            }
            confidenceUpdates++;
            break;
          }
        }
      } else if (!decision.title_accepted && decision.final_title !== decision.original_title) {
        // User corrected - learn new pattern
        const newPattern = learnTitlePattern(decision.original_title, decision.final_title);
        if (newPattern) {
          const existingIndex = patterns.title_transforms.findIndex(t => t.match === newPattern.match);
          if (existingIndex >= 0) {
            patterns.title_transforms[existingIndex].confidence++;
            if (!patterns.title_transforms[existingIndex].examples.includes(decision.original_title)) {
              patterns.title_transforms[existingIndex].examples.push(decision.original_title);
            }
            confidenceUpdates++;
          } else {
            patterns.title_transforms.push(newPattern);
            patternsLearned++;
          }
        }

        // Add exact override
        patterns.exact_overrides[decision.original_title] = {
          title: decision.final_title,
          project: decision.final_project,
          confidence: 1
        };
      }

      // Learn project hints from all decisions with projects
      if (decision.final_project) {
        const keywords = decision.final_title.toLowerCase().split(/\s+/).filter(w => w.length >= 4);
        for (const keyword of keywords) {
          if (!patterns.project_hints[keyword]) {
            patterns.project_hints[keyword] = {};
          }
          patterns.project_hints[keyword][decision.final_project] =
            (patterns.project_hints[keyword][decision.final_project] || 0) + 1;
        }
      }
    }

    patterns.stats.items_processed += params.decisions.length;
    patterns.stats.sessions_completed++;
    patterns.stats.patterns_learned += patternsLearned;

    await savePatterns(patterns);

    return JSON.stringify({
      success: true,
      decisions_processed: params.decisions.length,
      patterns_learned: patternsLearned,
      confidence_updates: confidenceUpdates,
      total_patterns: patterns.title_transforms.length,
      total_project_hints: Object.keys(patterns.project_hints).length,
      total_exact_overrides: Object.keys(patterns.exact_overrides).length
    }, null, 2);
  }
}

export const learningToolHandler = new LearningToolHandler();

export const learningTools = learningToolHandler.tools;
export const handleLearning = learningToolHandler.handle.bind(learningToolHandler);
