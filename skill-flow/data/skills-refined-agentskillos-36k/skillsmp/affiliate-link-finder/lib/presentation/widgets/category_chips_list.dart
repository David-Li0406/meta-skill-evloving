import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class CategoryChipsList extends StatefulWidget {
  const CategoryChipsList({super.key});

  @override
  State<CategoryChipsList> createState() => _CategoryChipsListState();
}

class _CategoryChipsListState extends State<CategoryChipsList> {
  int _selectedIndex = 0;
  final List<Map<String, dynamic>> _categories = [
    {'label': 'All', 'icon': Icons.all_inclusive},
    {'label': 'Focus', 'icon': Icons.track_changes},
    {'label': 'Sleep', 'icon': Icons.bedtime},
    {'label': 'Calm', 'icon': Icons.spa},
    {'label': 'Mood', 'icon': Icons.mood},
  ];

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: List.generate(_categories.length, (index) {
          final isSelected = index == _selectedIndex;
          final category = _categories[index];
          return Padding(
            padding: const EdgeInsets.only(right: 12),
            child: _buildChip(
              context,
              category['label'] as String,
              category['icon'] as IconData,
              isSelected,
              index,
            ),
          );
        }),
      ),
    );
  }

  Widget _buildChip(BuildContext context, String label, IconData icon, bool isSelected, int index) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return InkWell(
      onTap: () => setState(() => _selectedIndex = index),
      borderRadius: BorderRadius.circular(999),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        decoration: BoxDecoration(
          color: isSelected 
              ? AppColors.primary 
              : (isDark ? const Color(0xFF1c2633) : Colors.white),
          borderRadius: BorderRadius.circular(999),
          border: Border.all(
            color: isSelected 
                ? Colors.transparent 
                : (isDark ? Colors.grey[800]! : Colors.grey[200]!),
          ),
          boxShadow: isSelected 
              ? [BoxShadow(color: AppColors.primary.withValues(alpha: 0.2), blurRadius: 8, offset: const Offset(0, 4))] 
              : null,
        ),
        child: Row(
          children: [
            Icon(
              icon,
              size: 20,
              color: isSelected 
                  ? Colors.white 
                  : (isDark ? Colors.grey[400] : Colors.grey[600]),
            ),
            const SizedBox(width: 8),
            Text(
              label,
              style: TextStyle(
                color: isSelected 
                    ? Colors.white 
                    : (isDark ? Colors.grey[400] : Colors.grey[600]),
                fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
                fontSize: 14,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
