import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class LibrarySearchBar extends StatelessWidget {
  const LibrarySearchBar({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return Container(
      height: 48,
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1c2633) : Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 16),
            child: Icon(
              Icons.search,
              color: Color(0xFF9da8b9),
              size: 24,
            ),
          ),
          Expanded(
            child: TextField(
              decoration: const InputDecoration(
                hintText: 'Search supplements...',
                hintStyle: TextStyle(
                  color: Color(0xFF9da8b9),
                  fontSize: 16,
                ),
                border: InputBorder.none,
                contentPadding: EdgeInsets.only(right: 16),
              ),
              style: TextStyle(
                color: isDark ? Colors.white : AppColors.textPrimaryLight,
                fontSize: 16,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
