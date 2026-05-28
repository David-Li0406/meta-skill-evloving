enum EvidenceQuality { high, moderate, low }

class Study {
  final String id;
  final String title;
  final String authors;
  final int year;
  final String pubmedUrl;
  final String category;
  final EvidenceQuality evidenceQuality;
  final String keyFindings;
  final List<String> relatedSupplements;

  Study({
    required this.id,
    required this.title,
    required this.authors,
    required this.year,
    required this.pubmedUrl,
    required this.category,
    required this.evidenceQuality,
    required this.keyFindings,
    this.relatedSupplements = const [],
  });

  factory Study.fromJson(Map<String, dynamic> json) {
    return Study(
      id: json['id'] as String,
      title: json['title'] as String,
      authors: json['authors'] as String,
      year: json['year'] as int,
      pubmedUrl: json['pubmedUrl'] as String,
      category: json['category'] as String,
      evidenceQuality: EvidenceQuality.values.firstWhere(
        (e) => e.toString().split('.').last == json['evidenceQuality'],
        orElse: () => EvidenceQuality.moderate,
      ),
      keyFindings: json['keyFindings'] as String,
      relatedSupplements: (json['relatedSupplements'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'authors': authors,
      'year': year,
      'pubmedUrl': pubmedUrl,
      'category': category,
      'evidenceQuality': evidenceQuality.toString().split('.').last,
      'keyFindings': keyFindings,
      'relatedSupplements': relatedSupplements,
    };
  }
}
