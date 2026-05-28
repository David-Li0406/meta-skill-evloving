class FaqItem {
  final String id;
  final String question;
  final String answer;
  final String category;
  final List<String> relatedSupplements;

  FaqItem({
    required this.id,
    required this.question,
    required this.answer,
    required this.category,
    this.relatedSupplements = const [],
  });

  factory FaqItem.fromJson(Map<String, dynamic> json) {
    return FaqItem(
      id: json['id'] as String,
      question: json['question'] as String,
      answer: json['answer'] as String,
      category: json['category'] as String,
      relatedSupplements: (json['relatedSupplements'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'question': question,
      'answer': answer,
      'category': category,
      'relatedSupplements': relatedSupplements,
    };
  }
}
