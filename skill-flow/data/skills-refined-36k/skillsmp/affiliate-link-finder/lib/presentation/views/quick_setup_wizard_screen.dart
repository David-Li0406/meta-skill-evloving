import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';
import '../widgets/medical_disclaimer_widget.dart';
import '../../domain/repositories/settings_repository.dart';

class QuickSetupWizardScreen extends StatefulWidget {
  const QuickSetupWizardScreen({super.key});

  @override
  State<QuickSetupWizardScreen> createState() => _QuickSetupWizardScreenState();
}

class _QuickSetupWizardScreenState extends State<QuickSetupWizardScreen> {
  int _currentStep = -1; // Start at -1 for Disclaimer
  bool _disclaimerAccepted = false;
  String? _selectedGoal;
  String? _selectedStack;

  final _settingsRepo = GetIt.instance<SettingsRepository>();

  final List<Map<String, dynamic>> _goals = [
    {'title': 'Mental Clarity', 'icon': Icons.auto_awesome},
    {'title': 'Better Sleep', 'icon': Icons.bedtime},
    {'title': 'Energy Boost', 'icon': Icons.bolt},
  ];

  final List<Map<String, dynamic>> _prebuiltStacks = [
    {
      'title': 'Focus Stack',
      'description': 'Omega-3, B12, L-Theanine',
      'icon': Icons.psychology,
      'color': Colors.blue,
    },
    {
      'title': 'Sleep Stack',
      'description': 'Magnesium, Melatonin, L-Theanine',
      'icon': Icons.bedtime,
      'color': Colors.indigo,
    },
    {
      'title': 'Energy Stack',
      'description': 'B-Complex, Iron, Vitamin D',
      'icon': Icons.bolt,
      'color': Colors.amber,
    },
  ];

  void _nextStep() {
    if (_currentStep < 2) {
      setState(() => _currentStep++);
    } else {
      _completeSetup();
    }
  }

  Future<void> _completeSetup() async {
    // Persist disclaimer acceptance
    await _settingsRepo.setAcceptedDisclaimer(true);

    if (mounted) {
      Navigator.pushNamedAndRemoveUntil(
        context,
        AppRouter.dashboard,
        (route) => false,
      );
    }
  }

  void _skipSetup() {
    _completeSetup();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor:
          isDark ? const Color(0xFF112117) : const Color(0xFFF6F8F6),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(
          'Quick Setup',
          style: TextStyle(
            color: isDark ? Colors.white : Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
        actions: [
          TextButton(
            onPressed: _skipSetup,
            child: const Text(
              'Skip',
              style: TextStyle(
                color: AppColors.accentGreen,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Progress Indicator
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              child: Row(
                children: [
                  for (int i = -1; i < 3; i++) ...[
                    Expanded(
                      child: Container(
                        height: i == -1
                            ? 0
                            : 4, // Hide bar for disclaimer if preferred, or show it
                        decoration: i == -1
                            ? null
                            : BoxDecoration(
                                color: i <= _currentStep
                                    ? AppColors.accentGreen
                                    : (isDark
                                        ? Colors.grey[800]
                                        : Colors.grey[200]),
                                borderRadius: BorderRadius.circular(2),
                              ),
                      ),
                    ),
                    if (i < 2 && i != -1) const SizedBox(width: 8),
                  ],
                ],
              ),
            ),

            // Content
            Expanded(
              child: _buildStepContent(isDark),
            ),

            // Bottom Action
            Padding(
              padding: const EdgeInsets.all(24),
              child: SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton(
                  onPressed: _canProceed() ? _nextStep : null,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.accentGreen,
                    foregroundColor: const Color(0xFF112117),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    elevation: 4,
                  ),
                  child: Text(
                    _currentStep == 2 ? 'Start Tracking' : 'Next',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  bool _canProceed() {
    switch (_currentStep) {
      case -1:
        return _disclaimerAccepted;
      case 0:
        return _selectedGoal != null;
      case 1:
        return _selectedStack != null;
      case 2:
        return true;
      default:
        return false;
    }
  }

  Widget _buildStepContent(bool isDark) {
    switch (_currentStep) {
      case -1:
        return MedicalDisclaimerWidget(
          isDark: isDark,
          isChecked: _disclaimerAccepted,
          onChecked: (v) => setState(() => _disclaimerAccepted = v ?? false),
        );
      case 0:
        return _buildGoalSelection(isDark);
      case 1:
        return _buildStackSelection(isDark);
      case 2:
        return _buildConfirmation(isDark);
      default:
        return const SizedBox.shrink();
    }
  }

  Widget _buildGoalSelection(bool isDark) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'What\'s your main goal?',
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF111713),
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 12),
          Text(
            'We\'ll recommend the best supplements for you.',
            style: TextStyle(
              color: isDark ? Colors.grey[400] : Colors.grey[500],
              fontSize: 16,
            ),
          ),
          const SizedBox(height: 32),
          Expanded(
            child: ListView.builder(
              itemCount: _goals.length,
              itemBuilder: (context, index) {
                final goal = _goals[index];
                final isSelected = _selectedGoal == goal['title'];
                return Padding(
                  padding: const EdgeInsets.only(bottom: 16),
                  child: InkWell(
                    onTap: () => setState(
                        () => _selectedGoal = goal['title'] as String?),
                    borderRadius: BorderRadius.circular(16),
                    child: Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? AppColors.accentGreen.withValues(alpha: 0.1)
                            : (isDark ? const Color(0xFF1a2920) : Colors.white),
                        border: Border.all(
                          color: isSelected
                              ? AppColors.accentGreen
                              : (isDark
                                  ? Colors.grey[800]!
                                  : Colors.grey[200]!),
                          width: isSelected ? 2 : 1,
                        ),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Row(
                        children: [
                          Container(
                            width: 48,
                            height: 48,
                            decoration: BoxDecoration(
                              color:
                                  AppColors.accentGreen.withValues(alpha: 0.1),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Icon(
                              goal['icon'] as IconData,
                              color: AppColors.accentGreen,
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Text(
                              goal['title'] as String,
                              style: TextStyle(
                                color: isDark ? Colors.white : Colors.black,
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                          if (isSelected)
                            const Icon(
                              Icons.check_circle,
                              color: AppColors.accentGreen,
                            ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStackSelection(bool isDark) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Choose a starter stack',
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF111713),
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 12),
          Text(
            'Pre-built combinations that work well together.',
            style: TextStyle(
              color: isDark ? Colors.grey[400] : Colors.grey[500],
              fontSize: 16,
            ),
          ),
          const SizedBox(height: 32),
          Expanded(
            child: ListView.builder(
              itemCount: _prebuiltStacks.length,
              itemBuilder: (context, index) {
                final stack = _prebuiltStacks[index];
                final isSelected = _selectedStack == stack['title'];
                return Padding(
                  padding: const EdgeInsets.only(bottom: 16),
                  child: InkWell(
                    onTap: () => setState(
                        () => _selectedStack = stack['title'] as String?),
                    borderRadius: BorderRadius.circular(16),
                    child: Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? AppColors.accentGreen.withValues(alpha: 0.1)
                            : (isDark ? const Color(0xFF1a2920) : Colors.white),
                        border: Border.all(
                          color: isSelected
                              ? AppColors.accentGreen
                              : (isDark
                                  ? Colors.grey[800]!
                                  : Colors.grey[200]!),
                          width: isSelected ? 2 : 1,
                        ),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Row(
                        children: [
                          Container(
                            width: 48,
                            height: 48,
                            decoration: BoxDecoration(
                              color: (stack['color'] as Color)
                                  .withValues(alpha: 0.1),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Icon(
                              stack['icon'] as IconData,
                              color: stack['color'] as Color,
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  stack['title'] as String,
                                  style: TextStyle(
                                    color: isDark ? Colors.white : Colors.black,
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  stack['description'] as String,
                                  style: TextStyle(
                                    color: isDark
                                        ? Colors.grey[400]
                                        : Colors.grey[500],
                                    fontSize: 14,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          if (isSelected)
                            const Icon(
                              Icons.check_circle,
                              color: AppColors.accentGreen,
                            ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildConfirmation(bool isDark) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 120,
            height: 120,
            decoration: BoxDecoration(
              color: AppColors.accentGreen.withValues(alpha: 0.1),
              shape: BoxShape.circle,
            ),
            child: const Icon(
              Icons.check_circle,
              size: 60,
              color: AppColors.accentGreen,
            ),
          ),
          const SizedBox(height: 32),
          Text(
            'You\'re all set!',
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF111713),
              fontSize: 32,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 16),
          Text(
            'Your $_selectedStack is ready to track.\nWe\'ll help you stay consistent with reminders.',
            textAlign: TextAlign.center,
            style: TextStyle(
              color: isDark ? Colors.grey[400] : Colors.grey[500],
              fontSize: 16,
              height: 1.5,
            ),
          ),
        ],
      ),
    );
  }
}
