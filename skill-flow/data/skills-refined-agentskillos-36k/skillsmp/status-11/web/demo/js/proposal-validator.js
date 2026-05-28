/**
 * Proposal Validator
 *
 * Full policy validation pipeline for AI-generated branch proposals.
 * Implements policy rules, sanitization transforms, and validation reports.
 *
 * @module proposal-validator
 */
(function() {
  "use strict";

  /**
   * Basic profanity word list for content filtering.
   * @const {string[]}
   */
  const PROFANITY_LIST = [
    // Common profanity (intentionally minimal for demo)
    'fuck', 'shit', 'damn', 'ass', 'bitch', 'bastard', 'crap',
    // Masked variants
    'f***', 's***', 'b****',
    // Slurs and hate speech indicators
    'nigger', 'faggot', 'retard', 'cunt',
    // Violence indicators
    'kill yourself', 'suicide', 'murder',
    // Explicit content indicators
    'porn', 'xxx', 'nude', 'naked'
  ];

  const EXPLICIT_CONTENT_LIST = [
    'graphic sex', 'sexual assault', 'rape', 'gore', 'dismembered',
    'blood-soaked', 'torture chamber'
  ];

  const HATE_SPEECH_LIST = [
    'white power', 'heil', 'gas the', 'ethnic cleansing'
  ];

  /**
   * Schema requirements for a valid branch proposal
   * Based on docs/dev/m2-schemas/branch-proposal.json (simplified for inline use)
   */
  const REQUIRED_FIELDS = {
    'choice_text': 'string',
    'content': 'object',
    'content.text': 'string',
    'content.return_path': 'string'
  };

  /**
   * Optional fields with their expected types
   */
  const OPTIONAL_FIELDS = {
    'content.branch_type': 'string',
    'metadata': 'object',
    'metadata.confidence_score': 'number',
    'metadata.thematic_fit': 'number'
  };

  /**
   * Maximum allowed lengths
   */
  const MAX_LENGTHS = {
    choice_text: 100,
    content_text: 2000,
    return_path: 50
  };

  const DEFAULT_RULESET = {
    version: 'v1.0.0',
    actor: 'validation_pipeline_v1',
    rules: {
      schema_validation: { enabled: true, category: 'structural', severity: 'high' },
      profanity_filter: { enabled: true, category: 'policy', severity: 'critical', action: 'sanitize', mode: 'placeholder' },
      explicit_content_filter: { enabled: true, category: 'policy', severity: 'critical', action: 'reject' },
      hate_speech_detector: { enabled: true, category: 'policy', severity: 'critical', action: 'reject' },
      lore_consistency_check: { enabled: true, category: 'content', severity: 'high' },
      character_voice_consistency: { enabled: true, category: 'content', severity: 'high' },
      theme_consistency_check: { enabled: true, category: 'content', severity: 'medium' },
      narrative_pacing_check: { enabled: true, category: 'content', severity: 'medium' },
      ink_syntax_validation: { enabled: true, category: 'structural', severity: 'high' },
      length_limit_check: { enabled: true, category: 'structural', severity: 'medium', maxLength: 2000, warnLength: 1500 },
      encoding_normalization: { enabled: true, category: 'sanitization', severity: 'medium' },
      html_sanitization: { enabled: true, category: 'sanitization', severity: 'medium' },
      whitespace_normalization: { enabled: true, category: 'sanitization', severity: 'low' },
      return_path_reachability_check: { enabled: true, category: 'structural', severity: 'high' },
      return_path_narrative_coherence: { enabled: true, category: 'content', severity: 'high' }
    },
    pacingTargets: {
      exposition: { min: 80, max: 250 },
      slow_buildup: { min: 80, max: 200 },
      climactic: { min: 40, max: 120 },
      resolution: { min: 100, max: 200 }
    }
  };

  const QUICK_RULES = new Set([
    'schema_validation',
    'profanity_filter',
    'explicit_content_filter',
    'hate_speech_detector',
    'length_limit_check',
    'encoding_normalization',
    'html_sanitization',
    'whitespace_normalization',
    'return_path_reachability_check'
  ]);

  const ENDING_PATHS = [
    'rescue_end', 'waiting_end', 'quiet_end', 'lost_end',
    'tower_gathering_end', 'urgent_return_end', 'revelation_end'
  ];

  /**
   * Validation result type
   * @typedef {Object} ValidationResult
   * @property {boolean} valid - Whether the proposal passes validation
   * @property {string[]} errors - Array of error messages
   * @property {string[]} warnings - Array of warning messages
   * @property {Object} [report] - Validation report object
   * @property {Object|null} [sanitizedProposal] - Sanitized proposal if transforms applied
   */

  function deepMerge(target, src) {
    if (!src) return target;
    Object.keys(src).forEach(key => {
      const value = src[key];
      if (value && typeof value === 'object' && !Array.isArray(value) && typeof target[key] === 'object') {
        target[key] = deepMerge(Object.assign({}, target[key]), value);
      } else {
        target[key] = value;
      }
    });
    return target;
  }

  function cloneProposal(proposal) {
    try {
      if (typeof structuredClone === 'function') return structuredClone(proposal);
    } catch (e) {}
    return JSON.parse(JSON.stringify(proposal || {}));
  }

  function loadPolicyRuleset(options = {}) {
    let ruleset = cloneProposal(DEFAULT_RULESET);
    const overrides = options.ruleset || null;

    if (typeof window !== 'undefined') {
      const windowRuleset = window.PolicyRuleset || window.DirectorConfig?.policyRuleset || window.DirectorConfig?.validationRuleset;
      if (windowRuleset) {
        ruleset = deepMerge(ruleset, windowRuleset);
      }
    }

    if (overrides) {
      ruleset = deepMerge(ruleset, overrides);
    }

    if (options.rulesetPath) {
      try {
        const fs = require('fs');
        const raw = fs.readFileSync(options.rulesetPath, 'utf8');
        const parsed = JSON.parse(raw);
        ruleset = deepMerge(ruleset, parsed);
      } catch (e) {
        // ignore missing ruleset path
      }
    }

    return ruleset;
  }

  /**
   * Gets a nested property value from an object using dot notation
   *
   * @param {Object} obj - Object to query
   * @param {string} path - Dot-notation path (e.g., 'content.text')
   * @returns {*} The value at the path or undefined
   */
  function getNestedValue(obj, path) {
    return path.split('.').reduce((current, key) => {
      return current && current[key] !== undefined ? current[key] : undefined;
    }, obj);
  }

  function escapeRegExp(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function findMatches(text, terms) {
    if (!text || typeof text !== 'string') return [];
    const matches = [];
    const lowerText = text.toLowerCase();

    terms.forEach(term => {
      const escaped = escapeRegExp(term.toLowerCase());
      const regex = term.includes(' ')
        ? new RegExp(escaped, 'gi')
        : new RegExp(`\\b${escaped}\\b`, 'gi');
      let match;
      while ((match = regex.exec(lowerText))) {
        matches.push({
          offset: match.index,
          text: text.substr(match.index, match[0].length),
          explanation: `Matches prohibited term "${term}"`
        });
      }
    });

    return matches;
  }

  /**
   * Checks if text contains profanity (case-insensitive)
   *
   * @param {string} text - Text to check
   * @returns {{hasProfanity: boolean, matches: string[]}}
   */
  function checkProfanity(text) {
    const matches = findMatches(text, PROFANITY_LIST).map(match => match.text.toLowerCase());
    return {
      hasProfanity: matches.length > 0,
      matches
    };
  }

  function normalizeUnicode(text) {
    if (!text || typeof text !== 'string') return text;
    try {
      return text.normalize('NFC');
    } catch (e) {
      return text;
    }
  }

  function normalizeWhitespace(text) {
    if (!text || typeof text !== 'string') return text;
    const withoutControls = text.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, ' ');
    const tabsNormalized = withoutControls.replace(/\t+/g, ' ');
    const spacesCollapsed = tabsNormalized.replace(/ {2,}/g, ' ');
    const newlinesCollapsed = spacesCollapsed.replace(/\n{3,}/g, '\n\n');
    return newlinesCollapsed.trim();
  }

  function stripHtml(text) {
    if (!text || typeof text !== 'string') return text;
    return text.replace(/<[^>]*>/g, '');
  }

  function redactProfanity(text, mode = 'placeholder') {
    if (!text || typeof text !== 'string') return text;
    let sanitized = text;

    PROFANITY_LIST.forEach(term => {
      const escaped = escapeRegExp(term);
      const regex = term.includes(' ')
        ? new RegExp(escaped, 'gi')
        : new RegExp(`\\b${escaped}\\b`, 'gi');
      sanitized = sanitized.replace(regex, match => {
        if (mode === 'asterisks') return '*'.repeat(match.length);
        if (mode === 'mild_replacement') return 'darn';
        return '[expletive]';
      });
    });
    return sanitized;
  }

  function generateUuid() {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      return crypto.randomUUID();
    }
    const template = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx';
    return template.replace(/[xy]/g, c => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  function countWords(text) {
    if (!text || typeof text !== 'string') return 0;
    return text.trim().split(/\s+/).filter(Boolean).length;
  }

  function getRuleConfig(ruleset, ruleId) {
    return (ruleset && ruleset.rules && ruleset.rules[ruleId]) || null;
  }

  function shouldRunRule(ruleId, mode) {
    if (mode === 'quick') return QUICK_RULES.has(ruleId);
    return true;
  }

  function buildRuleResult({ ruleId, ruleName, category, result, severity, message, violations, sanitization, metadata }) {
    const payload = {
      rule_id: ruleId,
      rule_name: ruleName,
      category,
      result
    };

    if (severity) payload.severity = severity;
    if (message) payload.message = message;
    if (violations && violations.length) payload.violations = violations;
    if (sanitization) payload.sanitization_applied = sanitization;
    if (metadata) payload.metadata = metadata;
    return payload;
  }

  function applyTextSanitization(sanitizedProposal, updates) {
    if (!sanitizedProposal) return;
    if (updates.choice_text !== undefined) sanitizedProposal.choice_text = updates.choice_text;
    if (updates.content_text !== undefined) {
      sanitizedProposal.content = sanitizedProposal.content || {};
      sanitizedProposal.content.text = updates.content_text;
    }
  }

  function validateSchema(proposal) {
    const errors = [];
    const warnings = [];

    if (!proposal || typeof proposal !== 'object') {
      return {
        valid: false,
        errors: ['Proposal must be an object'],
        warnings: []
      };
    }

    // Check required fields
    for (const [path, expectedType] of Object.entries(REQUIRED_FIELDS)) {
      const value = getNestedValue(proposal, path);

      if (value === undefined || value === null) {
        errors.push(`Missing required field: ${path}`);
      } else if (typeof value !== expectedType) {
        errors.push(`Field ${path} must be ${expectedType}, got ${typeof value}`);
      }
    }

    // Check optional fields if present
    for (const [path, expectedType] of Object.entries(OPTIONAL_FIELDS)) {
      const value = getNestedValue(proposal, path);

      if (value !== undefined && value !== null && typeof value !== expectedType) {
        warnings.push(`Field ${path} should be ${expectedType}, got ${typeof value}`);
      }
    }

    // Check length constraints
    if (proposal.choice_text && proposal.choice_text.length > MAX_LENGTHS.choice_text) {
      warnings.push(`choice_text exceeds recommended length (${proposal.choice_text.length} > ${MAX_LENGTHS.choice_text})`);
    }

    if (proposal.content?.text && proposal.content.text.length > MAX_LENGTHS.content_text) {
      errors.push(`content.text exceeds maximum length (${proposal.content.text.length} > ${MAX_LENGTHS.content_text})`);
    }

    if (proposal.content?.return_path && proposal.content.return_path.length > MAX_LENGTHS.return_path) {
      errors.push(`content.return_path exceeds maximum length`);
    }

    // Validate confidence scores are in range
    if (proposal.metadata?.confidence_score !== undefined) {
      const score = proposal.metadata.confidence_score;
      if (score < 0 || score > 1) {
        warnings.push(`confidence_score should be between 0.0 and 1.0, got ${score}`);
      }
    }

    if (proposal.metadata?.thematic_fit !== undefined) {
      const score = proposal.metadata.thematic_fit;
      if (score < 0 || score > 1) {
        warnings.push(`thematic_fit should be between 0.0 and 1.0, got ${score}`);
      }
    }

    return {
      valid: errors.length === 0,
      errors: errors,
      warnings: warnings
    };
  }

  function validateInkSyntax(proposal) {
    const text = proposal?.content?.text || '';
    const branchType = proposal?.content?.branch_type || 'narrative_delta';
    if (!text || (branchType !== 'ink_fragment' && branchType !== 'ink_knot')) {
      return { valid: true };
    }

    if (typeof inkjs !== 'undefined' && inkjs.Compiler) {
      try {
        let contentToValidate = text;
        if (branchType === 'ink_fragment') {
          contentToValidate = `=== _validation_wrapper ===\n${text}\n-> END`;
        }
        const compiler = new inkjs.Compiler(contentToValidate);
        compiler.Compile();
        return { valid: true };
      } catch (e) {
        return { valid: false, message: e.message };
      }
    }

    const stack = [];
    const pairs = { '{': '}', '[': ']', '(': ')' };
    for (const char of text) {
      if (pairs[char]) stack.push(pairs[char]);
      if (Object.values(pairs).includes(char)) {
        if (stack.pop() !== char) {
          return { valid: false, message: 'Unbalanced Ink syntax tokens' };
        }
      }
    }
    if (stack.length) {
      return { valid: false, message: 'Unbalanced Ink syntax tokens' };
    }
    return { valid: true };
  }

  function validateReturnPath(proposal, validReturnPaths) {
    const errors = [];
    const warnings = [];

    if (!proposal?.content?.return_path) {
      errors.push('No return_path specified');
      return { valid: false, errors, warnings };
    }

    const returnPath = proposal.content.return_path;

    if (validReturnPaths && validReturnPaths.length > 0) {
      if (!validReturnPaths.includes(returnPath)) {
        warnings.push(`Return path "${returnPath}" is not in the recommended list. May cause navigation issues.`);
      }
    }

    if (ENDING_PATHS.includes(returnPath)) {
      errors.push(`Return path "${returnPath}" is an ending - cannot use as return target`);
    }

    return {
      valid: errors.length === 0,
      errors: errors,
      warnings: warnings
    };
  }

  function computeRiskScore(ruleResults) {
    if (!ruleResults.length) return 0;
    const severityWeights = {
      critical: 1.0,
      high: 0.7,
      medium: 0.4,
      low: 0.1,
      info: 0.0
    };
    const resultWeights = {
      failed: 1.0,
      sanitized: 0.6,
      warning: 0.4,
      passed: 0.0
    };
    const total = ruleResults.reduce((acc, rule) => {
      const severity = severityWeights[rule.severity] ?? 0.2;
      const outcome = resultWeights[rule.result] ?? 0.0;
      return acc + (severity * outcome);
    }, 0);
    return Math.min(1, total / ruleResults.length);
  }

  function evaluateNarrativeConsistency(proposal, options) {
    const rules = [];
    const contentText = proposal?.content?.text || '';

    const loreConfig = options.loreBlocklist || [];
    if (loreConfig.length) {
      const violations = findMatches(contentText, loreConfig);
      if (violations.length) {
        rules.push(buildRuleResult({
          ruleId: 'lore_consistency_check',
          ruleName: 'Lore Consistency Check',
          category: 'content',
          result: 'warning',
          severity: 'high',
          message: 'Potential LORE contradiction detected',
          violations
        }));
      } else {
        rules.push(buildRuleResult({
          ruleId: 'lore_consistency_check',
          ruleName: 'Lore Consistency Check',
          category: 'content',
          result: 'passed',
          severity: 'high'
        }));
      }
    }

    const voiceConfig = options.characterVoiceProfiles || null;
    if (proposal?.content?.character_voice && voiceConfig && voiceConfig[proposal.content.character_voice]) {
      const profile = voiceConfig[proposal.content.character_voice];
      const markers = profile.requiredPhrases || [];
      const matches = markers.filter(marker => contentText.toLowerCase().includes(String(marker).toLowerCase()));
      if (markers.length && matches.length === 0) {
        rules.push(buildRuleResult({
          ruleId: 'character_voice_consistency',
          ruleName: 'Character Voice Consistency',
          category: 'content',
          result: 'warning',
          severity: 'high',
          message: 'Character voice markers missing'
        }));
      } else {
        rules.push(buildRuleResult({
          ruleId: 'character_voice_consistency',
          ruleName: 'Character Voice Consistency',
          category: 'content',
          result: 'passed',
          severity: 'high'
        }));
      }
    }

    const storyThemes = options.storyThemes || [];
    if (storyThemes.length) {
      const themeMatches = storyThemes.filter(theme => contentText.toLowerCase().includes(String(theme).toLowerCase()));
      if (themeMatches.length === 0) {
        rules.push(buildRuleResult({
          ruleId: 'theme_consistency_check',
          ruleName: 'Theme Consistency Check',
          category: 'content',
          result: 'warning',
          severity: 'medium',
          message: 'No story theme keywords detected'
        }));
      } else {
        rules.push(buildRuleResult({
          ruleId: 'theme_consistency_check',
          ruleName: 'Theme Consistency Check',
          category: 'content',
          result: 'passed',
          severity: 'medium'
        }));
      }
    }

    if (options.narrativePhase) {
      const phase = options.narrativePhase;
      const wordCount = countWords(contentText);
      const target = options.pacingTargets && options.pacingTargets[phase];
      if (target) {
        if (wordCount < target.min || wordCount > target.max) {
          rules.push(buildRuleResult({
            ruleId: 'narrative_pacing_check',
            ruleName: 'Narrative Pacing Check',
            category: 'content',
            result: 'warning',
            severity: 'medium',
            message: `Narrative pacing out of range (${wordCount} words)`
          }));
        } else {
          rules.push(buildRuleResult({
            ruleId: 'narrative_pacing_check',
            ruleName: 'Narrative Pacing Check',
            category: 'content',
            result: 'passed',
            severity: 'medium'
          }));
        }
      }
    }

    return rules;
  }

  function evaluateSafetyRules(proposal, ruleset, options, sanitizedProposal) {
    const rules = [];
    const results = {
      hasCriticalFailure: false,
      hadSanitization: false
    };

    const choiceText = proposal?.choice_text || '';
    const contentText = proposal?.content?.text || '';
    const profanityConfig = getRuleConfig(ruleset, 'profanity_filter');

    if (profanityConfig?.enabled) {
      const violations = [...findMatches(choiceText, PROFANITY_LIST), ...findMatches(contentText, PROFANITY_LIST)];
      if (violations.length) {
        const mode = profanityConfig.mode || 'placeholder';
        const sanitizedChoice = redactProfanity(choiceText, mode);
        const sanitizedContent = redactProfanity(contentText, mode);
        const sanitization = {
          original_text: contentText,
          sanitized_text: sanitizedContent,
          transform_type: 'redaction'
        };
        if (profanityConfig.action === 'reject') {
          rules.push(buildRuleResult({
            ruleId: 'profanity_filter',
            ruleName: 'Profanity Filter',
            category: profanityConfig.category,
            result: 'failed',
            severity: profanityConfig.severity,
            message: 'Profanity detected in proposal',
            violations
          }));
          results.hasCriticalFailure = true;
        } else {
          applyTextSanitization(sanitizedProposal, {
            choice_text: sanitizedChoice,
            content_text: sanitizedContent
          });
          rules.push(buildRuleResult({
            ruleId: 'profanity_filter',
            ruleName: 'Profanity Filter',
            category: profanityConfig.category,
            result: 'sanitized',
            severity: profanityConfig.severity,
            message: 'Profanity detected and sanitized',
            violations,
            sanitization
          }));
          results.hadSanitization = true;
        }
      } else {
        rules.push(buildRuleResult({
          ruleId: 'profanity_filter',
          ruleName: 'Profanity Filter',
          category: profanityConfig.category,
          result: 'passed',
          severity: profanityConfig.severity
        }));
      }
    }

    const explicitConfig = getRuleConfig(ruleset, 'explicit_content_filter');
    if (explicitConfig?.enabled) {
      const violations = findMatches(contentText, EXPLICIT_CONTENT_LIST);
      if (violations.length) {
        rules.push(buildRuleResult({
          ruleId: 'explicit_content_filter',
          ruleName: 'Explicit Content Filter',
          category: explicitConfig.category,
          result: 'failed',
          severity: explicitConfig.severity,
          message: 'Explicit content detected',
          violations
        }));
        results.hasCriticalFailure = true;
      } else {
        rules.push(buildRuleResult({
          ruleId: 'explicit_content_filter',
          ruleName: 'Explicit Content Filter',
          category: explicitConfig.category,
          result: 'passed',
          severity: explicitConfig.severity
        }));
      }
    }

    const hateConfig = getRuleConfig(ruleset, 'hate_speech_detector');
    if (hateConfig?.enabled) {
      const violations = findMatches(contentText, HATE_SPEECH_LIST);
      if (violations.length) {
        rules.push(buildRuleResult({
          ruleId: 'hate_speech_detector',
          ruleName: 'Hate Speech Detector',
          category: hateConfig.category,
          result: 'failed',
          severity: hateConfig.severity,
          message: 'Hate speech detected',
          violations
        }));
        results.hasCriticalFailure = true;
      } else {
        rules.push(buildRuleResult({
          ruleId: 'hate_speech_detector',
          ruleName: 'Hate Speech Detector',
          category: hateConfig.category,
          result: 'passed',
          severity: hateConfig.severity
        }));
      }
    }

    return { rules, results };
  }

  function evaluateFormatRules(proposal, ruleset, sanitizedProposal) {
    const rules = [];
    let hadSanitization = false;
    const choiceText = sanitizedProposal?.choice_text || proposal?.choice_text || '';
    const contentText = sanitizedProposal?.content?.text || proposal?.content?.text || '';

    const encodingConfig = getRuleConfig(ruleset, 'encoding_normalization');
    if (encodingConfig?.enabled) {
      const normalizedChoice = normalizeUnicode(choiceText);
      const normalizedContent = normalizeUnicode(contentText);
      if (normalizedChoice !== choiceText || normalizedContent !== contentText) {
        applyTextSanitization(sanitizedProposal, {
          choice_text: normalizedChoice,
          content_text: normalizedContent
        });
        rules.push(buildRuleResult({
          ruleId: 'encoding_validation',
          ruleName: 'Encoding Normalization',
          category: encodingConfig.category,
          result: 'sanitized',
          severity: encodingConfig.severity,
          message: 'Normalized unicode encoding',
          sanitization: {
            original_text: contentText,
            sanitized_text: normalizedContent,
            transform_type: 'normalization'
          }
        }));
        hadSanitization = true;
      } else {
        rules.push(buildRuleResult({
          ruleId: 'encoding_validation',
          ruleName: 'Encoding Normalization',
          category: encodingConfig.category,
          result: 'passed',
          severity: encodingConfig.severity
        }));
      }
    }

    const htmlConfig = getRuleConfig(ruleset, 'html_sanitization');
    if (htmlConfig?.enabled) {
      const currentChoice = sanitizedProposal?.choice_text || choiceText;
      const currentContent = sanitizedProposal?.content?.text || contentText;
      const strippedChoice = stripHtml(currentChoice);
      const strippedContent = stripHtml(currentContent);
      if (strippedChoice !== currentChoice || strippedContent !== currentContent) {
        applyTextSanitization(sanitizedProposal, {
          choice_text: strippedChoice,
          content_text: strippedContent
        });
        rules.push(buildRuleResult({
          ruleId: 'html_sanitization',
          ruleName: 'HTML Sanitization',
          category: htmlConfig.category,
          result: 'sanitized',
          severity: htmlConfig.severity,
          message: 'HTML tags stripped',
          sanitization: {
            original_text: currentContent,
            sanitized_text: strippedContent,
            transform_type: 'removal'
          }
        }));
        hadSanitization = true;
      } else {
        rules.push(buildRuleResult({
          ruleId: 'html_sanitization',
          ruleName: 'HTML Sanitization',
          category: htmlConfig.category,
          result: 'passed',
          severity: htmlConfig.severity
        }));
      }
    }

    const whitespaceConfig = getRuleConfig(ruleset, 'whitespace_normalization');
    if (whitespaceConfig?.enabled) {
      const currentChoice = sanitizedProposal?.choice_text || choiceText;
      const currentContent = sanitizedProposal?.content?.text || contentText;
      const normalizedChoice = normalizeWhitespace(currentChoice);
      const normalizedContent = normalizeWhitespace(currentContent);
      if (normalizedChoice !== currentChoice || normalizedContent !== currentContent) {
        applyTextSanitization(sanitizedProposal, {
          choice_text: normalizedChoice,
          content_text: normalizedContent
        });
        rules.push(buildRuleResult({
          ruleId: 'whitespace_normalization',
          ruleName: 'Whitespace Normalization',
          category: whitespaceConfig.category,
          result: 'sanitized',
          severity: whitespaceConfig.severity,
          message: 'Whitespace normalized',
          sanitization: {
            original_text: currentContent,
            sanitized_text: normalizedContent,
            transform_type: 'normalization'
          }
        }));
        hadSanitization = true;
      } else {
        rules.push(buildRuleResult({
          ruleId: 'whitespace_normalization',
          ruleName: 'Whitespace Normalization',
          category: whitespaceConfig.category,
          result: 'passed',
          severity: whitespaceConfig.severity
        }));
      }
    }

    return { rules, hadSanitization };
  }

  function validateProposal(proposal, options = {}) {
    const start = Date.now();
    const mode = options.mode || 'full';
    const ruleset = loadPolicyRuleset(options);
    const sanitizedProposal = cloneProposal(proposal);
    const allErrors = [];
    const allWarnings = [];
    const rules = [];
    let hasCriticalFailure = false;
    let hadSanitization = false;

    if (shouldRunRule('schema_validation', mode)) {
      const schemaResult = validateSchema(proposal);
      if (!schemaResult.valid) {
        hasCriticalFailure = true;
      }
      allErrors.push(...schemaResult.errors);
      allWarnings.push(...schemaResult.warnings);
      const ruleConfig = getRuleConfig(ruleset, 'schema_validation');
      rules.push(buildRuleResult({
        ruleId: 'schema_validation',
        ruleName: 'Schema Validation',
        category: ruleConfig?.category || 'structural',
        result: schemaResult.valid ? 'passed' : 'failed',
        severity: ruleConfig?.severity || 'high',
        message: schemaResult.valid ? 'Schema valid' : schemaResult.errors.join('; ')
      }));
    }

    if (shouldRunRule('ink_syntax_validation', mode)) {
      const ruleConfig = getRuleConfig(ruleset, 'ink_syntax_validation');
      if (ruleConfig?.enabled) {
        const inkResult = validateInkSyntax(proposal);
        if (!inkResult.valid) {
          hasCriticalFailure = true;
          allErrors.push(`Ink syntax error: ${inkResult.message}`);
        }
        rules.push(buildRuleResult({
          ruleId: 'ink_syntax_validation',
          ruleName: 'Ink Syntax Validation',
          category: ruleConfig.category,
          result: inkResult.valid ? 'passed' : 'failed',
          severity: ruleConfig.severity,
          message: inkResult.message
        }));
      }
    }

    if (shouldRunRule('length_limit_check', mode)) {
      const ruleConfig = getRuleConfig(ruleset, 'length_limit_check');
      if (ruleConfig?.enabled) {
        const length = (proposal?.content?.text || '').length;
        if (length > ruleConfig.maxLength) {
          allErrors.push(`content.text exceeds maximum length (${length} > ${ruleConfig.maxLength})`);
          hasCriticalFailure = true;
          rules.push(buildRuleResult({
            ruleId: 'length_limit_check',
            ruleName: 'Length Limit Check',
            category: ruleConfig.category,
            result: 'failed',
            severity: ruleConfig.severity,
            message: 'Content length exceeds limit'
          }));
        } else if (length > ruleConfig.warnLength) {
          allWarnings.push(`content.text near maximum length (${length} > ${ruleConfig.warnLength})`);
          rules.push(buildRuleResult({
            ruleId: 'length_limit_check',
            ruleName: 'Length Limit Check',
            category: ruleConfig.category,
            result: 'warning',
            severity: ruleConfig.severity,
            message: 'Content length near limit'
          }));
        } else {
          rules.push(buildRuleResult({
            ruleId: 'length_limit_check',
            ruleName: 'Length Limit Check',
            category: ruleConfig.category,
            result: 'passed',
            severity: ruleConfig.severity
          }));
        }
      }
    }

    if (shouldRunRule('return_path_reachability_check', mode)) {
      const returnConfig = getRuleConfig(ruleset, 'return_path_reachability_check');
      if (returnConfig?.enabled) {
        const validReturnPaths = options.validReturnPaths || proposal?.validReturnPaths;
        const returnResult = validateReturnPath(proposal, validReturnPaths);
        allErrors.push(...returnResult.errors);
        allWarnings.push(...returnResult.warnings);
        if (!returnResult.valid) {
          hasCriticalFailure = true;
        }
        rules.push(buildRuleResult({
          ruleId: 'return_path_reachability_check',
          ruleName: 'Return Path Reachability',
          category: returnConfig.category,
          result: returnResult.valid ? 'passed' : 'failed',
          severity: returnConfig.severity,
          message: returnResult.errors[0] || returnResult.warnings[0]
        }));
      }
    }

    if (shouldRunRule('return_path_narrative_coherence', mode)) {
      const coherenceConfig = getRuleConfig(ruleset, 'return_path_narrative_coherence');
      if (coherenceConfig?.enabled) {
        const returnPath = proposal?.content?.return_path;
        const invalid = typeof returnPath !== 'string' || returnPath.trim().length === 0;
        if (invalid) {
          allErrors.push('Return path coherence check failed');
          hasCriticalFailure = true;
          rules.push(buildRuleResult({
            ruleId: 'return_path_narrative_coherence',
            ruleName: 'Return Path Coherence',
            category: coherenceConfig.category,
            result: 'failed',
            severity: coherenceConfig.severity,
            message: 'Return path missing or empty'
          }));
        } else {
          rules.push(buildRuleResult({
            ruleId: 'return_path_narrative_coherence',
            ruleName: 'Return Path Coherence',
            category: coherenceConfig.category,
            result: 'passed',
            severity: coherenceConfig.severity
          }));
        }
      }
    }

    if (shouldRunRule('profanity_filter', mode) || shouldRunRule('explicit_content_filter', mode) || shouldRunRule('hate_speech_detector', mode)) {
      const { rules: safetyRules, results } = evaluateSafetyRules(proposal, ruleset, options, sanitizedProposal);
      rules.push(...safetyRules);
      if (results.hasCriticalFailure) hasCriticalFailure = true;
      if (results.hadSanitization) hadSanitization = true;
      safetyRules.forEach(rule => {
        if (rule.result === 'failed' && rule.message) allErrors.push(rule.message);
        if (rule.result === 'sanitized' && rule.message) allWarnings.push(rule.message);
      });
    }

    if (mode !== 'quick') {
      const narrativeRules = evaluateNarrativeConsistency(proposal, {
        loreBlocklist: options.loreBlocklist || [],
        characterVoiceProfiles: options.characterVoiceProfiles || null,
        storyThemes: options.storyThemes || [],
        narrativePhase: options.narrativePhase || null,
        pacingTargets: options.pacingTargets || ruleset.pacingTargets
      });
      rules.push(...narrativeRules);
      narrativeRules.forEach(rule => {
        if (rule.result === 'warning' && rule.message) allWarnings.push(rule.message);
      });
    }

    if (shouldRunRule('html_sanitization', mode) || shouldRunRule('whitespace_normalization', mode) || shouldRunRule('encoding_normalization', mode)) {
      const { rules: formatRules, hadSanitization: formatSanitization } = evaluateFormatRules(proposal, ruleset, sanitizedProposal);
      rules.push(...formatRules);
      if (formatSanitization) hadSanitization = true;
      formatRules.forEach(rule => {
        if (rule.result === 'sanitized' && rule.message) allWarnings.push(rule.message);
      });
    }

    const validationTime = Math.max(0, Date.now() - start);
    const status = hasCriticalFailure ? 'failed' : (hadSanitization ? 'rejected_with_sanitization' : 'passed');
    const overallRiskScore = computeRiskScore(rules);
    const hasHighWarnings = rules.some(rule => rule.result === 'warning' && (rule.severity === 'high' || rule.severity === 'critical'));
    const recommendation = hasCriticalFailure
      ? 'reject'
      : (hadSanitization ? 'approve_with_caution' : (hasHighWarnings ? 'manual_review' : 'approve'));

    const report = {
      id: generateUuid(),
      proposal_id: proposal?.id || proposal?.proposal_id || generateUuid(),
      created_at: new Date().toISOString(),
      status,
      rules,
      overall_risk_score: overallRiskScore,
      recommendation,
      metadata: {
        validation_time_ms: validationTime,
        ruleset_version: ruleset.version,
        actor: ruleset.actor
      }
    };

    if (hadSanitization) {
      report.sanitized_proposal = sanitizedProposal;
    }

    return {
      valid: !hasCriticalFailure,
      errors: allErrors,
      warnings: allWarnings,
      report,
      sanitizedProposal: hadSanitization ? sanitizedProposal : null
    };
  }

  /**
   * Quick validation for real-time use.
   *
   * @param {Object} proposal - The proposal to validate
   * @param {Object} [options] - Validation options
   * @returns {{valid: boolean, reason?: string, sanitizedProposal?: Object}}
   */
  function quickValidate(proposal, options = {}) {
    const result = validateProposal(proposal, Object.assign({}, options, { mode: 'quick' }));
    if (!result.valid) {
      return {
        valid: false,
        reason: result.errors[0] || 'Failed policy validation',
        report: result.report
      };
    }
    return {
      valid: true,
      sanitizedProposal: result.sanitizedProposal,
      report: result.report
    };
  }

  // Export for use in other modules
  const ProposalValidator = {
    validateProposal,
    validateSchema,
    validateReturnPath,
    quickValidate,
    checkProfanity,
    loadPolicyRuleset,
    PROFANITY_LIST,
    MAX_LENGTHS
  };

  // CommonJS export for testing
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProposalValidator;
  }

  // Browser global export
  if (typeof window !== 'undefined') {
    window.ProposalValidator = ProposalValidator;
  }

})();
