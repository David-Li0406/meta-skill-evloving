import 'package:flutter/material.dart';
import '../../domain/entities/article.dart';
import '../../domain/repositories/article_repository.dart';
import '../../utils/logger.dart';

/// ViewModel managing the state for a single article's detailed view.
///
/// Orchestrates data fetching from [ArticleRepository] and manages:
/// - Main [article] data.
/// - [relatedArticles] for discovery.
/// - [isLoading] state for UI skeletons/spinners.
class ArticleDetailViewModel extends ChangeNotifier {
  final ArticleRepository _repository;

  ArticleDetailViewModel(this._repository);

  Article? _article;

  /// The currently loaded article. Null if not yet loaded or not found.
  Article? get article => _article;

  List<Article> _relatedArticles = [];

  /// List of articles related to the current one (e.g., same category).
  List<Article> get relatedArticles => _relatedArticles;

  bool _isLoading = false;

  /// True while fetching article or related data.
  bool get isLoading => _isLoading;

  /// Fetches an article by its [id] and subsequently loads related articles.
  ///
  /// Updates [isLoading] and notifies listeners immediately.
  Future<void> loadArticle(String id) async {
    _isLoading = true;
    notifyListeners();

    try {
      _article = await _repository.getArticle(id);
      if (_article != null) {
        _relatedArticles = await _repository.getRelatedArticles(id);
      }
    } catch (e) {
      AppLogger.e('Error loading article', e);
      // Potential extension: Set an error message state
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
