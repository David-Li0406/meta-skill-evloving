import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../infrastructure/repositories/perplexity_repository.dart';
import '../../config/locator.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';

class AiSearchScreen extends StatefulWidget {
  const AiSearchScreen({super.key});

  @override
  State<AiSearchScreen> createState() => _AiSearchScreenState();
}

class _AiSearchScreenState extends State<AiSearchScreen> {
  final TextEditingController _controller = TextEditingController();
  final PerplexityRepository _repository = locator<PerplexityRepository>();

  String _response = '';
  bool _isLoading = false;

  Future<void> _performSearch() async {
    if (_controller.text.isEmpty) return;

    setState(() {
      _isLoading = true;
      _response = '';
    });

    try {
      final result = await _repository.search(_controller.text);
      setState(() {
        _response = result;
      });
    } catch (e) {
      setState(() {
        _response = 'Error: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    const primaryGold = AppColors.primaryGold;
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bgColor = isDark
        ? AppColors.backgroundPremiumDark
        : AppColors.backgroundPremiumLight;

    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        title: Text(
          'AI RESEARCH',
          style: GoogleFonts.lexend(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            letterSpacing: 1.5,
            color: isDark ? Colors.white : Colors.black,
          ),
        ),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new,
              color: isDark ? Colors.white : Colors.black),
          onPressed: () =>
              Navigator.pushReplacementNamed(context, AppRouter.dashboard),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24.0),
        child: Column(
          children: [
            const SizedBox(height: 16),
            Container(
              decoration: BoxDecoration(
                color: isDark ? const Color(0xFF2D2616) : Colors.white,
                borderRadius: BorderRadius.circular(32),
                border: Border.all(color: primaryGold.withValues(alpha: 0.2)),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.1),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: TextField(
                controller: _controller,
                style: GoogleFonts.lexend(
                    color: isDark ? Colors.white : Colors.black),
                decoration: InputDecoration(
                  hintText: 'Ask about a supplement...',
                  hintStyle: GoogleFonts.lexend(color: Colors.grey),
                  contentPadding:
                      const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                  border: InputBorder.none,
                  suffixIcon: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: GestureDetector(
                      onTap: _isLoading ? null : _performSearch,
                      child: Container(
                        decoration: const BoxDecoration(
                          color: primaryGold,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.send_rounded,
                            color: Colors.black, size: 20),
                      ),
                    ),
                  ),
                ),
                onSubmitted: (_) => _performSearch(),
              ),
            ),
            const SizedBox(height: 32),
            if (_isLoading)
              const Center(
                child: CircularProgressIndicator(
                  valueColor: AlwaysStoppedAnimation<Color>(primaryGold),
                ),
              )
            else
              Expanded(
                child: SingleChildScrollView(
                  child: Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
                      borderRadius: BorderRadius.circular(24),
                      border:
                          Border.all(color: primaryGold.withValues(alpha: 0.1)),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.05),
                          blurRadius: 20,
                          offset: const Offset(0, 8),
                        ),
                      ],
                    ),
                    child: Text(
                      _response.isEmpty
                          ? 'Results will appear here. Ask about interactions, dosages, or benefits.'
                          : _response,
                      style: GoogleFonts.lexend(
                        fontSize: 16,
                        height: 1.6,
                        color: isDark ? Colors.grey[200] : Colors.black87,
                      ),
                    ),
                  ),
                ),
              ),
            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }
}
