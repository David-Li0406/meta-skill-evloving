import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../../application/view_models/chemist_view_model.dart';
import '../../config/locator.dart';
import '../theme/app_theme.dart';

class ChemistScreen extends StatefulWidget {
  const ChemistScreen({super.key});

  static Widget withProvider() {
    return ChangeNotifierProvider(
      create: (_) => locator<ChemistViewModel>(),
      child: const ChemistScreen(),
    );
  }

  @override
  State<ChemistScreen> createState() => _ChemistScreenState();
}

class _ChemistScreenState extends State<ChemistScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final viewModel = context.watch<ChemistViewModel>();
    const primaryGold = AppColors.primaryGold;

    return Scaffold(
      backgroundColor:
          isDark ? const Color(0xFF0A0E14) : const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: Text(
          'AI CHEMIST',
          style: GoogleFonts.lexend(
            fontWeight: FontWeight.bold,
            letterSpacing: 1.5,
            fontSize: 16,
            color: primaryGold,
          ),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new,
              color: isDark ? Colors.white : Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete_outline, color: primaryGold),
            onPressed: () => viewModel.clearChat(),
          ),
        ],
      ),
      body: Column(
        children: [
          // Persona Header
          Container(
            padding: const EdgeInsets.all(16),
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: primaryGold.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: primaryGold.withValues(alpha: 0.3)),
            ),
            child: Row(
              children: [
                const CircleAvatar(
                  backgroundColor: primaryGold,
                  radius: 20,
                  child: Icon(Icons.science, color: Colors.white, size: 20),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Dr. Alchemist',
                        style: GoogleFonts.lexend(
                          fontWeight: FontWeight.bold,
                          color: isDark ? Colors.white : Colors.black,
                        ),
                      ),
                      Text(
                        'PhD Neuropharmacology Assistant',
                        style: GoogleFonts.lexend(
                          fontSize: 11,
                          color: isDark ? Colors.grey : Colors.grey[700],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Chat Messages
          Expanded(
            child: viewModel.messages.isEmpty
                ? _buildEmptyState(isDark)
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount: viewModel.messages.length,
                    itemBuilder: (context, index) {
                      final message = viewModel.messages[index];
                      final isUser = message['role'] == 'user';
                      return _buildChatBubble(
                          message['content'] ?? '', isUser, isDark);
                    },
                  ),
          ),

          if (viewModel.isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(color: primaryGold),
            ),

          // Input Area
          _buildInputArea(viewModel, isDark, primaryGold),
        ],
      ),
    );
  }

  Widget _buildChatBubble(String text, bool isUser, bool isDark) {
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 16),
        padding: const EdgeInsets.all(16),
        constraints:
            BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
        decoration: BoxDecoration(
          color: isUser
              ? AppColors.primaryGold
              : (isDark ? const Color(0xFF1C2633) : Colors.white),
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(isUser ? 16 : 0),
            bottomRight: Radius.circular(isUser ? 0 : 16),
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.05),
              blurRadius: 5,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Text(
          text,
          style: GoogleFonts.lexend(
            color: isUser
                ? Colors.white
                : (isDark ? Colors.grey[200] : Colors.black87),
            fontSize: 14,
            height: 1.5,
          ),
        ),
      ),
    );
  }

  Widget _buildInputArea(ChemistViewModel viewModel, bool isDark, Color gold) {
    return Container(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF0A0E14) : Colors.white,
        border: Border(
            top:
                BorderSide(color: isDark ? Colors.white12 : Colors.grey[200]!)),
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              style: GoogleFonts.lexend(
                  color: isDark ? Colors.white : Colors.black),
              decoration: InputDecoration(
                hintText: 'Ask about chemical interactions...',
                hintStyle: GoogleFonts.lexend(color: Colors.grey, fontSize: 13),
                filled: true,
                fillColor:
                    isDark ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(24),
                  borderSide: BorderSide.none,
                ),
                contentPadding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
              ),
              onSubmitted: (value) => _sendQuestion(viewModel),
            ),
          ),
          const SizedBox(width: 8),
          CircleAvatar(
            backgroundColor: gold,
            radius: 22,
            child: IconButton(
              icon: const Icon(Icons.send, color: Colors.white, size: 20),
              onPressed: () => _sendQuestion(viewModel),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState(bool isDark) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.science_outlined,
              size: 64, color: AppColors.primaryGold.withValues(alpha: 0.5)),
          const SizedBox(height: 24),
          Text(
            'Ask Dr. Alchemist',
            style: GoogleFonts.lexend(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: isDark ? Colors.white : Colors.black,
            ),
          ),
          const SizedBox(height: 12),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 48),
            child: Text(
              'Get technical deep-dives on supplement mechanisms, bioavailability, and neuro-chemistry.',
              textAlign: TextAlign.center,
              style: GoogleFonts.lexend(
                fontSize: 13,
                color: Colors.grey,
              ),
            ),
          ),
          const SizedBox(height: 32),
          _buildQuickAction('How does Caffeine pass the BBB?'),
          _buildQuickAction('Magnesium Glycinate vs Citrate?'),
        ],
      ),
    );
  }

  Widget _buildQuickAction(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: OutlinedButton(
        onPressed: () {
          _controller.text = text;
        },
        style: OutlinedButton.styleFrom(
          side: const BorderSide(color: AppColors.primaryGold),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        ),
        child: Text(text,
            style:
                GoogleFonts.lexend(fontSize: 12, color: AppColors.primaryGold)),
      ),
    );
  }

  void _sendQuestion(ChemistViewModel viewModel) {
    if (_controller.text.isEmpty) return;
    final text = _controller.text;
    _controller.clear();
    viewModel.askChemist(text).then((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }
}
