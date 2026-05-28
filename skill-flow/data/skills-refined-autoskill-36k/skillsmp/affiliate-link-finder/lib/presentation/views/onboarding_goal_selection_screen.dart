import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../widgets/goal_selection_card.dart';
import '../navigation/app_router.dart';

class OnboardingGoalSelectionScreen extends StatefulWidget {
  const OnboardingGoalSelectionScreen({super.key});

  @override
  State<OnboardingGoalSelectionScreen> createState() =>
      _OnboardingGoalSelectionScreenState();
}

class _OnboardingGoalSelectionScreenState
    extends State<OnboardingGoalSelectionScreen> {
  // Using a Set to allow multiple selections
  final Set<String> _selectedGoals = {'Better Sleep'};

  final List<Map<String, dynamic>> _goals = [
    {
      'title': 'Mental Clarity',
      'description': 'Reduce brain fog and improve focus.',
      'icon': Icons.auto_awesome,
    },
    {
      'title': 'Better Sleep',
      'description': 'Wind down and improve rest quality.',
      'icon': Icons.bedtime,
    },
    {
      'title': 'Emotional Balance',
      'description': 'Manage mood swings and reactivity.',
      'icon': Icons.favorite,
    },
    {
      'title': 'Energy Levels',
      'description': 'Consistent energy throughout the day.',
      'icon': Icons.bolt,
    },
  ];

  void _toggleGoal(String title) {
    setState(() {
      if (_selectedGoals.contains(title)) {
        _selectedGoals.remove(title);
      } else {
        _selectedGoals.add(title);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor:
          isDark ? const Color(0xFF112117) : const Color(0xFFF6F8F6),
      body: SafeArea(
        child: Stack(
          children: [
            Column(
              children: [
                // Header / Progress Indicator
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 24),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        width: 32,
                        height: 8,
                        decoration: BoxDecoration(
                          color: AppColors.accentGreen,
                          borderRadius: BorderRadius.circular(99),
                        ),
                      ),
                      const SizedBox(width: 8),
                      for (int i = 0; i < 4; i++) ...[
                        Container(
                          width: 8,
                          height: 8,
                          decoration: BoxDecoration(
                            color: isDark ? Colors.grey[700] : Colors.grey[200],
                            shape: BoxShape.circle,
                          ),
                        ),
                        if (i < 3) const SizedBox(width: 8),
                      ],
                    ],
                  ),
                ),

                Expanded(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.symmetric(horizontal: 24),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const SizedBox(height: 8),
                        Text(
                          'What\'s your focus today?',
                          style: TextStyle(
                            color:
                                isDark ? Colors.white : const Color(0xFF111713),
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            height: 1.1,
                            letterSpacing: -0.5,
                          ),
                        ),
                        const SizedBox(height: 12),
                        Text(
                          'Pick your primary goals to help us tailor your supplement routine.',
                          style: TextStyle(
                            color: isDark ? Colors.grey[400] : Colors.grey[500],
                            fontSize: 16,
                            height: 1.5,
                          ),
                        ),

                        const SizedBox(height: 32),

                        // Grid layout
                        GridView.builder(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          gridDelegate:
                              const SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: 2,
                            crossAxisSpacing: 16,
                            mainAxisSpacing: 16,
                            childAspectRatio:
                                0.75, // Adjusted to prevent overflow
                          ),
                          itemCount: _goals.length,
                          itemBuilder: (context, index) {
                            final goal = _goals[index];
                            final title = goal['title'] as String;
                            return GoalSelectionCard(
                              title: title,
                              description: goal['description'] as String,
                              icon: goal['icon'] as IconData,
                              isSelected: _selectedGoals.contains(title),
                              onTap: () => _toggleGoal(title),
                            );
                          },
                        ),

                        const SizedBox(height: 100), // Spacing for bottom bar
                      ],
                    ),
                  ),
                ),
              ],
            ),

            // Fixed Bottom Bar
            Positioned(
              left: 0,
              right: 0,
              bottom: 0,
              child: Container(
                padding: const EdgeInsets.fromLTRB(24, 16, 24, 32),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.bottomCenter,
                    end: Alignment.topCenter,
                    colors: [
                      isDark
                          ? const Color(0xFF112117)
                          : const Color(0xFFF6F8F6),
                      (isDark
                              ? const Color(0xFF112117)
                              : const Color(0xFFF6F8F6))
                          .withValues(alpha: 0.9),
                      Colors.transparent,
                    ],
                    stops: const [0.0, 0.7, 1.0],
                  ),
                ),
                child: Column(
                  children: [
                    SizedBox(
                      width: double.infinity,
                      height: 56,
                      child: ElevatedButton(
                        onPressed: () => Navigator.pushNamed(
                            context, '/onboarding/medication-safety'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.accentGreen,
                          foregroundColor: const Color(
                              0xFF112117), // Dark text on green button
                          elevation: 4,
                          shadowColor: Colors.black.withValues(alpha: 0.2),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                        ),
                        child: const Text(
                          'Next',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextButton(
                      onPressed: () => Navigator.pushNamed(
                          context, AppRouter.onboardingMedicationSafety),
                      style: TextButton.styleFrom(
                        foregroundColor:
                            isDark ? Colors.grey[400] : Colors.grey[500],
                      ),
                      child: const Text(
                        'I\'ll choose later',
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          decoration: TextDecoration.underline,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
