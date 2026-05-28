import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:adhd_supplement_app/application/view_models/article_detail_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/article_repository.dart';
import 'package:adhd_supplement_app/domain/entities/article.dart';

@GenerateMocks([ArticleRepository])
import 'article_detail_view_model_test.mocks.dart';

void main() {
  late ArticleDetailViewModel viewModel;
  late MockArticleRepository mockRepository;

  setUp(() {
    mockRepository = MockArticleRepository();
    viewModel = ArticleDetailViewModel(mockRepository);
  });

  tearDown(() {
    viewModel.dispose();
  });

  const testArticle = Article(
    id: '1',
    title: 'Test Article',
    category: 'Science',
    readTime: '5 min',
    publishDate: '2023-01-15',
    author: 'Dr. Test',
    authorRole: 'Researcher',
    authorAvatarUrl: 'https://example.com/avatar.jpg',
    imageUrl: 'https://example.com/image.jpg',
    tldr: 'Summary of the test article.',
    content: 'Full content of the test article.',
  );

  group('ArticleDetailViewModel', () {
    test('initial state is correct', () {
      expect(viewModel.article, isNull);
      expect(viewModel.relatedArticles, isEmpty);
      expect(viewModel.isLoading, isFalse);
    });

    test('loadArticle success - updates article and related articles',
        () async {
      // Arrange
      when(mockRepository.getArticle('1')).thenAnswer((_) async => testArticle);
      when(mockRepository.getRelatedArticles('1'))
          .thenAnswer((_) async => [testArticle]);

      // Act
      final future = viewModel.loadArticle('1');

      // Assert loading state
      expect(viewModel.isLoading, isTrue);

      await future;

      // Assert final state
      expect(viewModel.isLoading, isFalse);
      expect(viewModel.article, testArticle);
      expect(viewModel.relatedArticles, [testArticle]);
      verify(mockRepository.getArticle('1')).called(1);
      verify(mockRepository.getRelatedArticles('1')).called(1);
    });

    test(
        'loadArticle failed (article not found) - stops loading and article remains null',
        () async {
      // Arrange
      when(mockRepository.getArticle('unknown')).thenAnswer((_) async => null);

      // Act
      await viewModel.loadArticle('unknown');

      // Assert
      expect(viewModel.isLoading, isFalse);
      expect(viewModel.article, isNull);
      expect(viewModel.relatedArticles, isEmpty);
      verify(mockRepository.getArticle('unknown')).called(1);
      verifyNever(mockRepository.getRelatedArticles(any));
    });

    test('loadArticle error - handles exception gracefully', () async {
      // Arrange
      when(mockRepository.getArticle('1'))
          .thenThrow(Exception('Network error'));

      // Act
      await viewModel.loadArticle('1');

      // Assert
      expect(viewModel.isLoading, isFalse);
      expect(viewModel.article, isNull);
      verify(mockRepository.getArticle('1')).called(1);
    });
  });
}
