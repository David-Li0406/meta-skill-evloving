import '../entities/article.dart';

abstract class ArticleRepository {
  Future<Article?> getArticle(String id);
  Future<List<Article>> getRelatedArticles(String articleId);
  Future<List<Article>> getArticles();
  Future<Article?> getArticleOfTheDay();
}
