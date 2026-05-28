import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../config/locator.dart';
import '../../application/view_models/science_hub_view_model.dart';
import '../../domain/entities/article.dart';
import '../../domain/entities/faq_item.dart';
import '../../domain/entities/study.dart';
import '../../domain/entities/educational_article.dart';
import '../../infrastructure/services/url_service.dart';
import '../navigation/app_router.dart';
import '../theme/app_theme.dart';
import '../widgets/unified_bottom_nav.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../widgets/skeleton_loader.dart';

class ScienceHubScreen extends StatefulWidget {
  const ScienceHubScreen({super.key});

  @override
  State<ScienceHubScreen> createState() => _ScienceHubScreenState();
}

class _ScienceHubScreenState extends State<ScienceHubScreen> {
  late ScienceHubViewModel _viewModel;
  bool _isSearchVisible = false;
  final TextEditingController _searchController = TextEditingController();
  final UrlService _urlService = locator<UrlService>();

  @override
  void initState() {
    super.initState();
    _viewModel = locator<ScienceHubViewModel>();
    _viewModel.loadData();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryBlue = Color(0xFF136DEC);
    const bgDark = Color(0xFF101822);
    const bgLight = Color(0xFFF6F7F8);

    return ChangeNotifierProvider.value(
      value: _viewModel,
      child: Scaffold(
        backgroundColor: isDark ? bgDark : bgLight,
        body: Consumer<ScienceHubViewModel>(
          builder: (context, viewModel, child) {
            if (viewModel.isLoading) {
              return _buildSkeleton(context, isDark);
            }
            return CustomScrollView(
              slivers: [
                _buildAppBar(context, isDark),
                SliverToBoxAdapter(
                  child: Padding(
                    padding: const EdgeInsets.only(bottom: 20),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        if (!viewModel.isSearching &&
                            viewModel.articleOfTheDay != null)
                          _buildArticleOfTheDay(context, isDark, primaryBlue,
                              viewModel.articleOfTheDay!),
                        if (!viewModel.isSearching)
                          _buildCategories(isDark, primaryBlue),
                        if (viewModel.isSearching)
                          _buildSearchResultsHeader(viewModel),
                        if (viewModel.articles.isNotEmpty &&
                            !viewModel.isSearching)
                          _buildEvidenceBasedResearch(
                              context, isDark, primaryBlue, viewModel.articles),
                        _buildResearchLibrary(
                            context, isDark, primaryBlue, viewModel),
                        _buildEducationalContent(
                            context, isDark, primaryBlue, viewModel),
                        _buildFaqSection(
                            context, isDark, primaryBlue, viewModel),
                        if (!viewModel.isSearching) ...[
                          _buildAiChemistCard(context, isDark, primaryBlue),
                          _buildSafetyGuides(isDark, primaryBlue),
                          _buildUserInsights(isDark, primaryBlue),
                        ],
                      ],
                    ),
                  ),
                ),
              ],
            );
          },
        ),
        bottomNavigationBar: const UnifiedBottomNav(currentIndex: 3),
      ),
    );
  }

  Widget _buildAppBar(BuildContext context, bool isDark) {
    if (_isSearchVisible) {
      return SliverAppBar(
        backgroundColor: isDark ? const Color(0xFF101822) : Colors.white,
        pinned: true,
        elevation: 0,
        title: TextField(
          controller: _searchController,
          autofocus: true,
          onChanged: (value) => _viewModel.setSearchQuery(value),
          style: GoogleFonts.lexend(
            color: isDark ? Colors.white : Colors.black,
            fontSize: 16,
          ),
          decoration: InputDecoration(
            hintText: 'Search science, studies, FAQs...',
            hintStyle: GoogleFonts.lexend(color: Colors.grey),
            border: InputBorder.none,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.close),
            onPressed: () {
              setState(() {
                _isSearchVisible = false;
                _searchController.clear();
                _viewModel.setSearchQuery('');
              });
            },
          ),
        ],
      );
    }

    return SliverAppBar(
      backgroundColor: isDark
          ? const Color(0xFF101822).withValues(alpha: 0.9)
          : Colors.white.withValues(alpha: 0.9),
      pinned: true,
      elevation: 0,
      leading: IconButton(
        icon: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: isDark
                ? Colors.white.withValues(alpha: 0.05)
                : Colors.black.withValues(alpha: 0.05),
            shape: BoxShape.circle,
          ),
          child: Icon(Icons.arrow_back_ios_new,
              size: 16, color: isDark ? Colors.white : Colors.black),
        ),
        onPressed: () =>
            Navigator.pushReplacementNamed(context, AppRouter.dashboard),
      ),
      title: Text(
        'Science Hub',
        style: GoogleFonts.lexend(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: isDark ? Colors.white : Colors.black,
        ),
      ),
      centerTitle: true,
      actions: [
        Padding(
          padding: const EdgeInsets.only(right: 16),
          child: Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: isDark
                  ? Colors.white.withValues(alpha: 0.05)
                  : Colors.black.withValues(alpha: 0.05),
              shape: BoxShape.circle,
            ),
            child: Icon(Icons.search,
                size: 20,
                color: isDark ? Colors.white : const Color(0xFF111418)),
          ),
        ),
      ],
    );
  }

  Widget _buildArticleOfTheDay(
      BuildContext context, bool isDark, Color primary, Article article) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: GestureDetector(
        onTap: () => Navigator.pushNamed(context, AppRouter.articleDetail,
            arguments: article.id),
        child: Container(
          height: 380,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            image: DecorationImage(
              image: CachedNetworkImageProvider(article.imageUrl),
              fit: BoxFit.cover,
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.2),
                blurRadius: 10,
                offset: const Offset(0, 5),
              ),
            ],
          ),
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(16),
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  Colors.transparent,
                  Colors.black.withValues(alpha: 0.4),
                  Colors.black.withValues(alpha: 0.9),
                ],
                stops: const [0.4, 0.7, 1.0],
              ),
            ),
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.end,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: primary,
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: const Text(
                    'ARTICLE OF THE DAY',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.5,
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                Text(
                  article.title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    fontFamily: 'Serif',
                    height: 1.1,
                  ),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    const Icon(Icons.schedule, color: Colors.white70, size: 16),
                    const SizedBox(width: 4),
                    Text(
                      article.readTime,
                      style:
                          const TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                    const SizedBox(width: 16),
                    const Icon(Icons.verified, color: Colors.yellow, size: 16),
                    const SizedBox(width: 4),
                    const Text(
                      'High Evidence', // Static for now, could be dynamic
                      style: TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildCategories(bool isDark, Color primary) {
    final categories = [
      {'icon': null, 'label': 'All Resources', 'active': true},
      {'icon': Icons.manage_search, 'label': 'Research', 'active': false},
      {'icon': Icons.shield, 'label': 'Safety', 'active': false},
      {'icon': Icons.forum, 'label': 'Success Stories', 'active': false},
    ];

    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: categories.map((cat) {
          final isActive = cat['active'] as bool;
          return Padding(
            padding: const EdgeInsets.only(right: 12),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
              decoration: BoxDecoration(
                color: isActive
                    ? primary
                    : (isDark ? const Color(0xFF1E293B) : Colors.white),
                borderRadius: BorderRadius.circular(24),
                border: isActive
                    ? null
                    : Border.all(
                        color: isDark
                            ? const Color(0xFF334155)
                            : const Color(0xFFE2E8F0),
                      ),
              ),
              child: Row(
                children: [
                  if (cat['icon'] != null) ...[
                    Icon(
                      cat['icon'] as IconData,
                      size: 18,
                      color: isActive
                          ? Colors.white
                          : (isDark
                              ? const Color(0xFFCBD5E1)
                              : const Color(0xFF111418)),
                    ),
                    const SizedBox(width: 8),
                  ],
                  Text(
                    cat['label'] as String,
                    style: TextStyle(
                      color: isActive
                          ? Colors.white
                          : (isDark
                              ? const Color(0xFFCBD5E1)
                              : const Color(0xFF111418)),
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildEvidenceBasedResearch(BuildContext context, bool isDark,
      Color primary, List<Article> articles) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Evidence-Based Research',
                style: TextStyle(
                  color: isDark ? Colors.white : const Color(0xFF111418),
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  fontFamily: 'Serif',
                ),
              ),
              Text(
                'View All',
                style: TextStyle(
                  color: primary,
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          ...articles.map((article) => Padding(
                padding: const EdgeInsets.only(bottom: 16),
                child: _buildResearchCard(
                  context,
                  isDark,
                  primary,
                  'HIGH EVIDENCE', // Mock badge
                  article.readTime,
                  article.title,
                  article.tldr,
                  article.imageUrl,
                  article.id,
                  isEmerging: false,
                ),
              )),
        ],
      ),
    );
  }

  Widget _buildResearchCard(
    BuildContext context,
    bool isDark,
    Color primary,
    String badge,
    String time,
    String title,
    String description,
    String imageUrl,
    String articleId, {
    bool isEmerging = false,
  }) {
    return GestureDetector(
      onTap: () => Navigator.pushNamed(context, AppRouter.articleDetail,
          arguments: articleId),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: isDark ? const Color(0xFF1E293B) : Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.05),
              blurRadius: 4,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: isEmerging
                              ? (isDark
                                  ? const Color(0xFF334155)
                                  : const Color(0xFFF1F5F9))
                              : primary.withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          badge,
                          style: TextStyle(
                            color: isEmerging
                                ? (isDark
                                    ? const Color(0xFF94A3B8)
                                    : const Color(0xFF64748B))
                                : primary,
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        time,
                        style: TextStyle(
                          color: isDark
                              ? const Color(0xFF94A3B8)
                              : const Color(0xFF64748B),
                          fontSize: 10,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    title,
                    style: TextStyle(
                      color: isDark ? Colors.white : const Color(0xFF111418),
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      fontFamily: 'Serif',
                      height: 1.2,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    description,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      color: isDark
                          ? const Color(0xFF94A3B8)
                          : const Color(0xFF64748B),
                      fontSize: 12,
                      height: 1.4,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Text(
                        'Read Full Analysis',
                        style: TextStyle(
                          color: primary,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Icon(Icons.chevron_right, color: primary, size: 16),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(width: 16),
            Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(12),
                image: DecorationImage(
                  image: CachedNetworkImageProvider(imageUrl),
                  fit: BoxFit.cover,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSafetyGuides(bool isDark, Color primary) {
    return Container(
      color: isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Safety & Usage Guides',
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF111418),
              fontSize: 20,
              fontWeight: FontWeight.bold,
              fontFamily: 'Serif',
            ),
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: _buildGuideCard(
                  isDark,
                  Icons.warning_amber,
                  primary,
                  'Dosage Best Practices',
                  'Avoiding tolerance and maximizing efficacy...',
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildGuideCard(
                  isDark,
                  Icons.sync_problem,
                  Colors.red,
                  'Drug Interactions',
                  'Common contraindications to discuss with your MD...',
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildGuideCard(bool isDark, IconData icon, Color iconColor,
      String title, String description) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1E293B) : Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: iconColor, size: 24),
          const SizedBox(height: 12),
          Text(
            title,
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF111418),
              fontSize: 16,
              fontWeight: FontWeight.bold,
              fontFamily: 'Serif',
              height: 1.1,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            description,
            style: TextStyle(
              color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
              fontSize: 12,
              height: 1.3,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildUserInsights(bool isDark, Color primary) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'User Insights',
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF111418),
              fontSize: 20,
              fontWeight: FontWeight.bold,
              fontFamily: 'Serif',
            ),
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: primary.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: primary.withValues(alpha: 0.2),
              ),
            ),
            child: Column(
              children: [
                Text(
                  '"Switching to a magnesium-rich stack completely changed my morning fog. I finally feel like my brain is firing on all cylinders."',
                  style: TextStyle(
                    color: isDark ? Colors.white : const Color(0xFF111418),
                    fontSize: 16,
                    fontStyle: FontStyle.italic,
                    fontFamily: 'Serif',
                    height: 1.4,
                  ),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Container(
                      width: 40,
                      height: 40,
                      decoration: BoxDecoration(
                        color: primary.withValues(alpha: 0.2),
                        shape: BoxShape.circle,
                      ),
                      child: Icon(Icons.person, color: primary, size: 20),
                    ),
                    const SizedBox(width: 12),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Sarah J., Architect',
                          style: TextStyle(
                            color:
                                isDark ? Colors.white : const Color(0xFF111418),
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          'Verified User • Stack: Omega-3 + Mg',
                          style: TextStyle(
                            color: isDark
                                ? const Color(0xFF94A3B8)
                                : const Color(0xFF64748B),
                            fontSize: 10,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchResultsHeader(ScienceHubViewModel viewModel) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 10, 20, 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Search Results',
            style: GoogleFonts.lexend(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'Showing matches for "${viewModel.searchQuery}"',
            style: GoogleFonts.lexend(
              fontSize: 14,
              color: Colors.grey,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildResearchLibrary(BuildContext context, bool isDark, Color primary,
      ScienceHubViewModel viewModel) {
    final categories = [
      'All',
      'Essential Fatty Acids',
      'Vitamins & Minerals',
      'Adaptogens',
      'Nootropics'
    ];

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Research Library',
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF111418),
              fontSize: 20,
              fontWeight: FontWeight.bold,
              fontFamily: 'Serif',
            ),
          ),
          const SizedBox(height: 16),
          // Category filters
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: categories.map((category) {
                final isSelected =
                    viewModel.selectedResearchCategory == category;
                return Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: GestureDetector(
                    onTap: () => viewModel.setResearchCategory(category),
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 8),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? primary
                            : (isDark ? const Color(0xFF1E293B) : Colors.white),
                        borderRadius: BorderRadius.circular(20),
                        border: isSelected
                            ? null
                            : Border.all(
                                color: isDark
                                    ? const Color(0xFF334155)
                                    : const Color(0xFFE2E8F0),
                              ),
                      ),
                      child: Text(
                        category,
                        style: TextStyle(
                          color: isSelected
                              ? Colors.white
                              : (isDark
                                  ? const Color(0xFFCBD5E1)
                                  : const Color(0xFF111418)),
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ),
                );
              }).toList(),
            ),
          ),
          const SizedBox(height: 16),
          // Study items
          ...viewModel.filteredStudies.map((study) => _StudyCard(
                study: study,
                isDark: isDark,
                primary: primary,
                urlService: _urlService,
              )),
        ],
      ),
    );
  }

  Widget _buildEducationalContent(BuildContext context, bool isDark,
      Color primary, ScienceHubViewModel viewModel) {
    final categories = ['All', 'Neuroscience', 'Nutrition', 'Lifestyle'];

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Educational Content',
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF111418),
              fontSize: 20,
              fontWeight: FontWeight.bold,
              fontFamily: 'Serif',
            ),
          ),
          const SizedBox(height: 16),
          // Category filters
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: categories.map((category) {
                final isSelected = viewModel.selectedEduCategory == category;
                return Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: GestureDetector(
                    onTap: () => viewModel.setEduCategory(category),
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 8),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? primary
                            : (isDark ? const Color(0xFF1E293B) : Colors.white),
                        borderRadius: BorderRadius.circular(20),
                        border: isSelected
                            ? null
                            : Border.all(
                                color: isDark
                                    ? const Color(0xFF334155)
                                    : const Color(0xFFE2E8F0),
                              ),
                      ),
                      child: Text(
                        category,
                        style: TextStyle(
                          color: isSelected
                              ? Colors.white
                              : (isDark
                                  ? const Color(0xFFCBD5E1)
                                  : const Color(0xFF111418)),
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ),
                );
              }).toList(),
            ),
          ),
          const SizedBox(height: 16),
          // Article grid/list
          ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: viewModel.filteredEduArticles.length,
            separatorBuilder: (_, __) => const SizedBox(height: 12),
            itemBuilder: (context, index) {
              final article = viewModel.filteredEduArticles[index];
              return _EducationCard(
                article: article,
                isDark: isDark,
                primary: primary,
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildFaqSection(BuildContext context, bool isDark, Color primary,
      ScienceHubViewModel viewModel) {
    final categories = ['All', 'General', 'Safety', 'Dosing'];

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Frequently Asked Questions',
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF111418),
              fontSize: 20,
              fontWeight: FontWeight.bold,
              fontFamily: 'Serif',
            ),
          ),
          const SizedBox(height: 16),
          // Category filters
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: categories.map((category) {
                final isSelected = viewModel.selectedFaqCategory == category;
                return Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: GestureDetector(
                    onTap: () => viewModel.setFaqCategory(category),
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 8),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? primary
                            : (isDark ? const Color(0xFF1E293B) : Colors.white),
                        borderRadius: BorderRadius.circular(20),
                        border: isSelected
                            ? null
                            : Border.all(
                                color: isDark
                                    ? const Color(0xFF334155)
                                    : const Color(0xFFE2E8F0),
                              ),
                      ),
                      child: Text(
                        category,
                        style: TextStyle(
                          color: isSelected
                              ? Colors.white
                              : (isDark
                                  ? const Color(0xFFCBD5E1)
                                  : const Color(0xFF111418)),
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ),
                );
              }).toList(),
            ),
          ),
          const SizedBox(height: 16),
          // FAQ items
          ...viewModel.filteredFaqs.map((faq) => _FaqCard(
                faq: faq,
                isDark: isDark,
                primary: primary,
              )),
        ],
      ),
    );
  }

  Widget _buildAiChemistCard(BuildContext context, bool isDark, Color primary) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: GestureDetector(
        onTap: () => Navigator.pushNamed(context, AppRouter.chemist),
        child: Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: isDark
                  ? [const Color(0xFF1E293B), const Color(0xFF0F172A)]
                  : [const Color(0xFFE2E8F0), Colors.white],
            ),
            borderRadius: BorderRadius.circular(20),
            border:
                Border.all(color: AppColors.primaryGold.withValues(alpha: 0.5)),
            boxShadow: [
              BoxShadow(
                color: AppColors.primaryGold.withValues(alpha: 0.1),
                blurRadius: 10,
                spreadRadius: 2,
              ),
            ],
          ),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.primaryGold.withValues(alpha: 0.2),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.science,
                    color: AppColors.primaryGold, size: 32),
              ),
              const SizedBox(width: 20),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Talk to Dr. Alchemist',
                      style: GoogleFonts.lexend(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: isDark ? Colors.white : Colors.black,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Our AI PhD Chemist is ready for your technical questions.',
                      style: GoogleFonts.lexend(
                        fontSize: 12,
                        color: isDark ? Colors.grey[400] : Colors.grey[700],
                      ),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.arrow_forward_ios,
                  color: AppColors.primaryGold, size: 16),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSkeleton(BuildContext context, bool isDark) {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 16),
              // AppBar placeholder
              const Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  SkeletonLoader(height: 40, width: 40, borderRadius: 20),
                  SkeletonLoader(height: 24, width: 120),
                  SkeletonLoader(height: 40, width: 40, borderRadius: 20),
                ],
              ),
              const SizedBox(height: 24),
              // Article of the day hero
              const SkeletonLoader(height: 380, borderRadius: 16),
              const SizedBox(height: 24),
              // Categories
              Row(
                children: List.generate(
                    3,
                    (index) => const Padding(
                          padding: EdgeInsets.only(right: 12),
                          child: SkeletonLoader(
                              height: 40, width: 100, borderRadius: 20),
                        )),
              ),
              const SizedBox(height: 24),
              // Research list
              const SkeletonLoader(height: 24, width: 200),
              const SizedBox(height: 16),
              const SkeletonLoader(height: 140, borderRadius: 16),
              const SizedBox(height: 16),
              const SkeletonLoader(height: 140, borderRadius: 16),
            ],
          ),
        ),
      ),
    );
  }
}

class _EducationCard extends StatelessWidget {
  final EducationalArticle article;
  final bool isDark;
  final Color primary;

  const _EducationCard({
    required this.article,
    required this.isDark,
    required this.primary,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        Navigator.pushNamed(
          context,
          AppRouter.eduArticleDetail,
          arguments: article,
        );
      },
      child: Container(
        decoration: BoxDecoration(
          color: isDark ? const Color(0xFF1E293B) : Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
          ),
        ),
        clipBehavior: Clip.antiAlias,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Stack(
              children: [
                CachedNetworkImage(
                  imageUrl: article.imageUrl,
                  height: 160,
                  width: double.infinity,
                  fit: BoxFit.cover,
                  placeholder: (context, url) => Container(
                    height: 160,
                    color: isDark ? Colors.black26 : Colors.grey[200],
                    child: const Center(child: CircularProgressIndicator()),
                  ),
                  errorWidget: (context, url, error) => Container(
                    height: 160,
                    color: isDark ? Colors.black26 : Colors.grey[200],
                    child: const Icon(Icons.error),
                  ),
                ),
                Positioned(
                  top: 12,
                  right: 12,
                  child: Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.black.withValues(alpha: 0.6),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      article.category,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.access_time,
                          size: 14,
                          color: isDark
                              ? const Color(0xFF94A3B8)
                              : const Color(0xFF64748B)),
                      const SizedBox(width: 4),
                      Text(
                        article.readTime,
                        style: TextStyle(
                          color: isDark
                              ? const Color(0xFF94A3B8)
                              : const Color(0xFF64748B),
                          fontSize: 12,
                        ),
                      ),
                      const Spacer(),
                      Text(
                        'By ${article.author}',
                        style: TextStyle(
                          color: isDark
                              ? const Color(0xFF94A3B8)
                              : const Color(0xFF64748B),
                          fontSize: 12,
                          fontStyle: FontStyle.italic,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    article.title,
                    style: TextStyle(
                      color: isDark ? Colors.white : const Color(0xFF111418),
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      height: 1.3,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    article.summary,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      color: isDark
                          ? const Color(0xFF94A3B8)
                          : const Color(0xFF64748B),
                      fontSize: 14,
                      height: 1.5,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Text(
                        'Read More',
                        style: TextStyle(
                          color: primary,
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(width: 4),
                      Icon(Icons.arrow_forward, size: 16, color: primary),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _StudyCard extends StatefulWidget {
  final Study study;
  final bool isDark;
  final Color primary;
  final UrlService urlService;

  const _StudyCard({
    required this.study,
    required this.isDark,
    required this.primary,
    required this.urlService,
  });

  @override
  State<_StudyCard> createState() => _StudyCardState();
}

class _StudyCardState extends State<_StudyCard> {
  bool _isExpanded = false;

  Color _getEvidenceColor(EvidenceQuality quality) {
    switch (quality) {
      case EvidenceQuality.high:
        return Colors.green;
      case EvidenceQuality.moderate:
        return Colors.orange;
      case EvidenceQuality.low:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Container(
        decoration: BoxDecoration(
          color: widget.isDark ? const Color(0xFF1E293B) : Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: widget.isDark
                ? const Color(0xFF334155)
                : const Color(0xFFE2E8F0),
          ),
        ),
        child: Column(
          children: [
            InkWell(
              onTap: () {
                setState(() {
                  _isExpanded = !_isExpanded;
                });
              },
              borderRadius: BorderRadius.circular(12),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 8, vertical: 2),
                          decoration: BoxDecoration(
                            color:
                                _getEvidenceColor(widget.study.evidenceQuality)
                                    .withValues(alpha: 0.1),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            widget.study.evidenceQuality
                                .toString()
                                .split('.')
                                .last
                                .toUpperCase(),
                            style: TextStyle(
                              color: _getEvidenceColor(
                                  widget.study.evidenceQuality),
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Text(
                          '${widget.study.year}',
                          style: TextStyle(
                            color: widget.isDark
                                ? const Color(0xFF94A3B8)
                                : const Color(0xFF64748B),
                            fontSize: 12,
                          ),
                        ),
                        const Spacer(),
                        AnimatedRotation(
                          turns: _isExpanded ? 0.5 : 0,
                          duration: const Duration(milliseconds: 200),
                          child: Icon(
                            Icons.keyboard_arrow_down,
                            color: widget.primary,
                            size: 24,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text(
                      widget.study.title,
                      style: TextStyle(
                        color: widget.isDark
                            ? Colors.white
                            : const Color(0xFF111418),
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        height: 1.3,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      widget.study.authors,
                      style: TextStyle(
                        color: widget.isDark
                            ? const Color(0xFF94A3B8)
                            : const Color(0xFF64748B),
                        fontSize: 12,
                        fontStyle: FontStyle.italic,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            AnimatedCrossFade(
              firstChild: const SizedBox.shrink(),
              secondChild: Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Divider(height: 1),
                    const SizedBox(height: 12),
                    Text(
                      'Key Findings:',
                      style: TextStyle(
                        color: widget.isDark ? Colors.white : Colors.black,
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      widget.study.keyFindings,
                      style: TextStyle(
                        color: widget.isDark
                            ? const Color(0xFF94A3B8)
                            : const Color(0xFF64748B),
                        fontSize: 14,
                        height: 1.5,
                      ),
                    ),
                    const SizedBox(height: 12),
                    InkWell(
                      onTap: () => widget.urlService
                          .launchInAppBrowser(widget.study.pubmedUrl),
                      child: Row(
                        children: [
                          Icon(Icons.launch, color: widget.primary, size: 16),
                          const SizedBox(width: 8),
                          Text(
                            'View on PubMed',
                            style: TextStyle(
                              color: widget.primary,
                              fontSize: 14,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                    if (widget.study.relatedSupplements.isNotEmpty) ...[
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children:
                            widget.study.relatedSupplements.map((String supp) {
                          return Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 10, vertical: 4),
                            decoration: BoxDecoration(
                              color: widget.primary.withValues(alpha: 0.1),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              supp,
                              style: TextStyle(
                                color: widget.primary,
                                fontSize: 11,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    ],
                  ],
                ),
              ),
              crossFadeState: _isExpanded
                  ? CrossFadeState.showSecond
                  : CrossFadeState.showFirst,
              duration: const Duration(milliseconds: 200),
            ),
          ],
        ),
      ),
    );
  }
}

class _FaqCard extends StatefulWidget {
  final FaqItem faq;
  final bool isDark;
  final Color primary;

  const _FaqCard({
    required this.faq,
    required this.isDark,
    required this.primary,
  });

  @override
  State<_FaqCard> createState() => _FaqCardState();
}

class _FaqCardState extends State<_FaqCard> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Container(
        decoration: BoxDecoration(
          color: widget.isDark ? const Color(0xFF1E293B) : Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: widget.isDark
                ? const Color(0xFF334155)
                : const Color(0xFFE2E8F0),
          ),
        ),
        child: Column(
          children: [
            InkWell(
              onTap: () {
                setState(() {
                  _isExpanded = !_isExpanded;
                });
              },
              borderRadius: BorderRadius.circular(12),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  children: [
                    Expanded(
                      child: Text(
                        widget.faq.question,
                        style: TextStyle(
                          color: widget.isDark
                              ? Colors.white
                              : const Color(0xFF111418),
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          height: 1.3,
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    AnimatedRotation(
                      turns: _isExpanded ? 0.5 : 0,
                      duration: const Duration(milliseconds: 200),
                      child: Icon(
                        Icons.keyboard_arrow_down,
                        color: widget.primary,
                        size: 24,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            AnimatedCrossFade(
              firstChild: const SizedBox.shrink(),
              secondChild: Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Divider(height: 1),
                    const SizedBox(height: 12),
                    Text(
                      widget.faq.answer,
                      style: TextStyle(
                        color: widget.isDark
                            ? const Color(0xFF94A3B8)
                            : const Color(0xFF64748B),
                        fontSize: 14,
                        height: 1.5,
                      ),
                    ),
                    if (widget.faq.relatedSupplements.isNotEmpty) ...[
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children:
                            widget.faq.relatedSupplements.map((String supp) {
                          return Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 10, vertical: 4),
                            decoration: BoxDecoration(
                              color: widget.primary.withValues(alpha: 0.1),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              supp,
                              style: TextStyle(
                                color: widget.primary,
                                fontSize: 11,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    ],
                  ],
                ),
              ),
              crossFadeState: _isExpanded
                  ? CrossFadeState.showSecond
                  : CrossFadeState.showFirst,
              duration: const Duration(milliseconds: 200),
            ),
          ],
        ),
      ),
    );
  }
}
