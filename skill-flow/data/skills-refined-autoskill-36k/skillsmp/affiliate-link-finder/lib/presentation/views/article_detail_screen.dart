import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../../config/locator.dart';
import '../../application/view_models/article_detail_view_model.dart';
import '../theme/app_theme.dart';
import '../../domain/entities/article.dart';
import '../widgets/cached_image.dart';

class ArticleDetailScreen extends StatefulWidget {
  /// Detailed view for a science hub article.
  ///
  /// Features:
  /// - Sliver-based parallax header with article image.
  /// - TL;DR Summary card for quick scanning (ADHD-friendly).
  /// - Author profiles and related reading suggestions.
  /// - Consistent loading/error states using [ArticleDetailViewModel].
  final String articleId;

  const ArticleDetailScreen({
    super.key,
    required this.articleId,
  });

  static Widget withProvider(String articleId) {
    return ChangeNotifierProvider(
      create: (_) => locator<ArticleDetailViewModel>(),
      child: ArticleDetailScreen(articleId: articleId),
    );
  }

  @override
  State<ArticleDetailScreen> createState() => _ArticleDetailScreenState();
}

class _ArticleDetailScreenState extends State<ArticleDetailScreen> {
  @override
  void initState() {
    super.initState();
    // Load article data
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<ArticleDetailViewModel>().loadArticle(widget.articleId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor: isDark ? const Color(0xFF0F172A) : Colors.white,
      body: Consumer<ArticleDetailViewModel>(
        builder: (context, viewModel, child) {
          if (viewModel.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          final article = viewModel.article;
          if (article == null) {
            return Center(
              child: Text(
                'Article not found',
                style: TextStyle(
                  color: isDark ? Colors.white : Colors.black,
                ),
              ),
            );
          }

          return CustomScrollView(
            slivers: [
              // Collapsible App Bar with Image
              SliverAppBar(
                expandedHeight: 280,
                pinned: true,
                backgroundColor:
                    isDark ? const Color(0xFF0F172A) : Colors.white,
                leading: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: CircleAvatar(
                    backgroundColor: isDark
                        ? Colors.black54
                        : Colors.white.withValues(alpha: 0.9),
                    child:
                        BackButton(color: isDark ? Colors.white : Colors.black),
                  ),
                ),
                actions: [
                  Padding(
                    padding: const EdgeInsets.fromLTRB(0, 8, 16, 8),
                    child: CircleAvatar(
                      backgroundColor: isDark
                          ? Colors.black54
                          : Colors.white.withValues(alpha: 0.9),
                      child: IconButton(
                        icon: const Icon(Icons.share, size: 20),
                        color: isDark ? Colors.white : Colors.black,
                        onPressed: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                                content: Text('Sharing article link...')),
                          );
                        },
                      ),
                    ),
                  ),
                ],
                flexibleSpace: FlexibleSpaceBar(
                  background: Stack(
                    fit: StackFit.expand,
                    children: [
                      CachedImage(
                        imageUrl: article.imageUrl,
                        fit: BoxFit.cover,
                      ),
                      Container(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            begin: Alignment.topCenter,
                            end: Alignment.bottomCenter,
                            colors: [
                              Colors.transparent,
                              isDark ? const Color(0xFF0F172A) : Colors.white,
                            ],
                            stops: const [0.6, 1.0],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),

              SliverPadding(
                padding: const EdgeInsets.all(24),
                sliver: SliverList(
                  delegate: SliverChildListDelegate([
                    // Meta Info
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: AppColors.primary.withValues(alpha: 0.1),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            article.category,
                            style: const TextStyle(
                              color: AppColors.primary,
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Text(
                          article.readTime,
                          style: TextStyle(
                              color:
                                  isDark ? Colors.grey[400] : Colors.grey[600],
                              fontSize: 13),
                        ),
                        const Spacer(),
                        Text(
                          article.publishDate,
                          style: TextStyle(
                              color:
                                  isDark ? Colors.grey[400] : Colors.grey[600],
                              fontSize: 13),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),

                    // Title
                    Text(
                      article.title,
                      style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.w900,
                        color: isDark ? Colors.white : const Color(0xFF1E293B),
                        height: 1.1,
                        fontFamily: 'Serif', // Fallback
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Author Profile
                    Row(
                      children: [
                        CircleAvatar(
                          radius: 16,
                          backgroundImage: CachedNetworkImageProvider(
                              article.authorAvatarUrl),
                        ),
                        const SizedBox(width: 12),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              article.author,
                              style: TextStyle(
                                color: isDark
                                    ? Colors.white
                                    : const Color(0xFF1E293B),
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                              ),
                            ),
                            Text(
                              article.authorRole,
                              style: TextStyle(
                                  color: isDark
                                      ? Colors.grey[400]
                                      : Colors.grey[600],
                                  fontSize: 12),
                            ),
                          ],
                        ),
                      ],
                    ),
                    const SizedBox(height: 32),

                    // TL;DR Summary Box
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: isDark
                            ? const Color(0xFF1E293B)
                            : const Color(0xFFF1F5F9),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: isDark ? Colors.grey[700]! : Colors.grey[200]!,
                          width: 1,
                        ),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Row(
                            children: [
                              Icon(Icons.bolt,
                                  color: AppColors.primary, size: 20),
                              SizedBox(width: 8),
                              Text(
                                'TL;DR Summary',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.primary,
                                  letterSpacing: 0.5,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Text(
                            article.tldr,
                            style: TextStyle(
                              fontSize: 16,
                              height: 1.5,
                              color: (isDark
                                      ? Colors.white
                                      : const Color(0xFF1E293B))
                                  .withValues(alpha: 0.9),
                              fontWeight: FontWeight.w500,
                              fontStyle: FontStyle.italic,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 32),

                    // Article Content
                    Text(
                      article.content,
                      style: TextStyle(
                          fontSize: 18,
                          height: 1.6,
                          color:
                              isDark ? Colors.white : const Color(0xFF1E293B)),
                    ),

                    const SizedBox(height: 48),

                    // Related Articles
                    if (viewModel.relatedArticles.isNotEmpty) ...[
                      Text(
                        'Related Reading',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color:
                              isDark ? Colors.white : const Color(0xFF1E293B),
                        ),
                      ),
                      const SizedBox(height: 16),
                      ...viewModel.relatedArticles.map((a) => Padding(
                            padding: const EdgeInsets.only(bottom: 12),
                            child: _buildRelatedArticle(isDark, a),
                          )),
                    ],

                    const SizedBox(height: 48),
                  ]),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildRelatedArticle(bool isDark, Article article) {
    return GestureDetector(
      onTap: () {
        // Push new article screen
        Navigator.push(
          context,
          MaterialPageRoute<void>(
            builder: (_) => ArticleDetailScreen.withProvider(article.id),
          ),
        );
      },
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color:
              isDark ? Colors.white.withValues(alpha: 0.05) : Colors.grey[100],
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          children: [
            CachedImage(
              width: 48,
              height: 48,
              imageUrl: article.imageUrl,
              borderRadius: 8,
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                article.title,
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  color: isDark ? Colors.white : Colors.black87,
                ),
              ),
            ),
            Icon(Icons.chevron_right,
                color: isDark ? Colors.grey : Colors.grey[400]),
          ],
        ),
      ),
    );
  }
}
