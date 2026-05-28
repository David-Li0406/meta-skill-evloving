class Article {
  final String id;
  final String title;
  final String author;
  final String authorRole;
  final String authorAvatarUrl;
  final String readTime;
  final String publishDate;
  final String imageUrl;
  final String tldr;
  final String category;
  final String content;
  final List<Article> relatedArticles;

  const Article({
    required this.id,
    required this.title,
    required this.author,
    required this.authorRole,
    required this.authorAvatarUrl,
    required this.readTime,
    required this.publishDate,
    required this.imageUrl,
    required this.tldr,
    required this.category,
    required this.content,
    this.relatedArticles = const [],
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'author': author,
      'authorRole': authorRole,
      'authorAvatarUrl': authorAvatarUrl,
      'readTime': readTime,
      'publishDate': publishDate,
      'imageUrl': imageUrl,
      'tldr': tldr,
      'category': category,
      'content': content,
    };
  }

  factory Article.fromJson(Map<String, dynamic> json) {
    return Article(
      id: json['id'] as String,
      title: json['title'] as String,
      author: json['author'] as String,
      authorRole: json['authorRole'] as String,
      authorAvatarUrl: json['authorAvatarUrl'] as String,
      readTime: json['readTime'] as String,
      publishDate: json['publishDate'] as String,
      imageUrl: json['imageUrl'] as String,
      tldr: json['tldr'] as String,
      category: json['category'] as String,
      content: json['content'] as String,
    );
  }
}
