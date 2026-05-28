class EducationalArticle {
  final String id;
  final String title;
  final String summary;
  final String content;
  final String imageUrl;
  final String category;
  final List<String> relatedSupplements;
  final List<String> keyTakeaways;
  final String readTime;
  final String author;
  final DateTime publishedDate;

  EducationalArticle({
    required this.id,
    required this.title,
    required this.summary,
    required this.content,
    required this.imageUrl,
    required this.category,
    required this.relatedSupplements,
    required this.keyTakeaways,
    required this.readTime,
    required this.author,
    required this.publishedDate,
  });
}
