/**
 * px-branding Skill Matcher (v2.0)
 *
 * Matches user prompts requesting PX Center brand identity application
 * to PowerPoint presentations with visual asset generation.
 */
module.exports = function (context) {
  const prompt = context.prompt.toLowerCase();

  const keywords = [
    'pptx',
    'powerpoint',
    'apresentação',
    'px-branding',
    'branding',
    'deck',
    'gemini',
  ];

  // Count matching keywords
  const matchCount = keywords.filter((keyword) => prompt.includes(keyword)).length;

  // IMPORTANT: All fields are MANDATORY and must not be undefined/null
  return {
    version: '2.0',
    matchCount: matchCount,
    type: 'skill',
  };
};
