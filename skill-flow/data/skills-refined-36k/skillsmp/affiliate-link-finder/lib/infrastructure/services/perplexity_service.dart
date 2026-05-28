import 'dart:convert';
import 'package:http/http.dart' as http;

class PerplexityService {
  final String apiKey;
  final String baseUrl = 'https://api.perplexity.ai/chat/completions';

  // In a real production app, use an environment variable or secure config.
  // For this private request, we use the key provided by the user.
  static const String _defaultApiKey =
      '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';

  PerplexityService({String? apiKey}) : apiKey = apiKey ?? _defaultApiKey;

  static const String chemistSystemPrompt =
      'You are "Dr. Alchemist", a PhD medicinal chemist specialized in neuropharmacology. '
      'You provide deep-dive scientific explanations for ADHD supplements. '
      'Focus on: molecular mechanisms of action, bioavailability, blood-brain barrier penetration, and chemical stability. '
      'Use technical but accessible language. Always cite theoretical chemical interactions and metabolic pathways.';

  Future<String> search(String query, {String? systemPrompt}) async {
    try {
      final response = await http.post(
        Uri.parse(baseUrl),
        headers: {
          'Authorization': 'Bearer $apiKey',
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode({
          'model': 'sonar-reasoning-pro', // Using a high-quality model
          'messages': [
            {
              'role': 'system',
              'content': systemPrompt ??
                  'You are a helpful assistant for an ADHD supplement app. Provide concise, evidence-based information about supplements. Focus on safety, interactions, and benefits for ADHD.'
            },
            {'role': 'user', 'content': query}
          ],
          'max_tokens': 1024,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['choices'][0]['message']['content'] as String;
      } else {
        throw Exception(
            'Failed to load search results: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      throw Exception('Perplexity API Error: $e');
    }
  }

  Future<Map<String, dynamic>> generateDailyArticle() async {
    const systemPrompt = '''
You are an expert neuroscientist and medical editor for an ADHD supplement app.
Generate a high-quality, engaging, and scientifically accurate daily article about a specific supplement, habit, or neuroscience concept relevant to ADHD.
The output MUST be a valid JSON object with the following fields:
- "title": Catchy but accurate title.
- "tldr": A 1-sentence summary.
- "content": A 3-paragaph markdown string. Use headers like ## Mechanism.
- "readTime": e.g. "3 min read".
- "category": One of: "SCIENCE", "FOCUS", "STACKS", "LIFESTYLE".
- "author": "Dr. AI-chemist" or a relevant persona.
- "authorRole": "AI Research Assistant".
- "imageUrl": "https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&q=80&w=1600" // Fallback gradient/abstract
- "authorAvatarUrl": "https://i.pravatar.cc/100?img=11"

Do not include markdown code blocks (like ```json) in the response, just the raw JSON.
''';

    final prompt =
        'Generate the daily article for ${DateTime.now().toIso8601String()}. Focus on something different than standard Magnesium or Caffeine if possible, maybe a lesser known nootropic or behavioral protocol.';

    try {
      final response = await http.post(
        Uri.parse(baseUrl),
        headers: {
          'Authorization': 'Bearer $apiKey',
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode({
          'model': 'sonar-reasoning-pro',
          'messages': [
            {'role': 'system', 'content': systemPrompt},
            {'role': 'user', 'content': prompt}
          ],
          'max_tokens': 2000,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final content = data['choices'][0]['message']['content'] as String;

        // Clean up markdown code blocks if present
        final cleanJson =
            content.replaceAll('```json', '').replaceAll('```', '').trim();

        try {
          return jsonDecode(cleanJson) as Map<String, dynamic>;
        } catch (e) {
          throw Exception('Failed to parse AI response as JSON: $content');
        }
      } else {
        throw Exception(
            'Failed to load daily article: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      throw Exception('Perplexity API Error: $e');
    }
  }
}
