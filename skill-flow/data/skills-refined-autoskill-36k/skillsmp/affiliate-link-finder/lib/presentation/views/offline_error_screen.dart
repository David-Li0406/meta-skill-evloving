import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_theme.dart';

class OfflineErrorScreen extends StatelessWidget {
  final VoidCallback? onRetry;
  final VoidCallback? onWorkOffline;

  const OfflineErrorScreen({
    super.key,
    this.onRetry,
    this.onWorkOffline,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    const primaryGold = AppColors.primaryGold;
    const bgLight = AppColors.backgroundLight;
    const bgDark = AppColors.backgroundDark;

    return Scaffold(
      backgroundColor: isDark ? bgDark : bgLight,
      appBar: AppBar(
        backgroundColor: isDark ? bgDark : bgLight,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'Connection Status',
          style: GoogleFonts.lexend(fontWeight: FontWeight.bold, fontSize: 18),
        ),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Illustration with animated background
                    SizedBox(
                      width: 280,
                      height: 280,
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          // Animated background circles
                          Container(
                            width: 250,
                            height: 250,
                            decoration: BoxDecoration(
                              color: primaryGold.withValues(alpha: 0.1),
                              shape: BoxShape.circle,
                            ),
                          ),
                          TweenAnimationBuilder(
                            tween: Tween<double>(begin: 0.9, end: 1.1),
                            duration: const Duration(seconds: 2),
                            curve: Curves.easeInOut,
                            builder: (context, double scale, child) {
                              return Transform.scale(
                                scale: scale,
                                child: Container(
                                  width: 280,
                                  height: 280,
                                  decoration: BoxDecoration(
                                    color: primaryGold.withValues(alpha: 0.05),
                                    shape: BoxShape.circle,
                                  ),
                                ),
                              );
                            },
                            onEnd: () {
                              // Restart animation
                            },
                          ),
                          // Main icon card
                          Container(
                            padding: const EdgeInsets.all(40),
                            decoration: BoxDecoration(
                              color: Colors.white.withValues(alpha: 0.05),
                              borderRadius: BorderRadius.circular(16),
                              border: Border.all(
                                color: Colors.white.withValues(alpha: 0.1),
                              ),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withValues(alpha: 0.2),
                                  blurRadius: 20,
                                  offset: const Offset(0, 10),
                                ),
                              ],
                            ),
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Icon(
                                  Icons.satellite_alt,
                                  size: 96,
                                  color: primaryGold,
                                ),
                                const SizedBox(height: 16),
                                Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    _buildDot(
                                        primaryGold.withValues(alpha: 0.4)),
                                    const SizedBox(width: 8),
                                    _buildDot(
                                        primaryGold.withValues(alpha: 0.6)),
                                    const SizedBox(width: 8),
                                    _buildDot(primaryGold),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: 48),

                    // Text content
                    Text(
                      'Oops, we lost our focus!',
                      textAlign: TextAlign.center,
                      style: GoogleFonts.lexend(
                        fontSize: 28,
                        fontWeight: FontWeight.w800,
                        color: isDark ? Colors.white : const Color(0xFF211811),
                        height: 1.2,
                      ),
                    ),
                    const SizedBox(height: 16),
                    RichText(
                      textAlign: TextAlign.center,
                      text: TextSpan(
                        style: GoogleFonts.lexend(
                          fontSize: 16,
                          color: isDark
                              ? Colors.white.withValues(alpha: 0.7)
                              : const Color(0xFF211811).withValues(alpha: 0.7),
                          height: 1.5,
                        ),
                        children: [
                          const TextSpan(
                            text: 'We can\'t reach the server right now.\n',
                          ),
                          TextSpan(
                            text: 'Your local reminders will still work!',
                            style: GoogleFonts.lexend(
                              fontWeight: FontWeight.w600,
                              color: primaryGold.withValues(alpha: 0.9),
                            ),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: 48),

                    // Action buttons
                    SizedBox(
                      width: double.infinity,
                      height: 56,
                      child: ElevatedButton.icon(
                        onPressed: onRetry ??
                            () {
                              // Default retry logic: close screen and let parent retry
                              Navigator.pop(context);
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                    content: Text('Retrying connection...')),
                              );
                            },
                        icon: const Icon(Icons.refresh),
                        label: const Text('Try Again'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: primaryGold,
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(999),
                          ),
                          textStyle: GoogleFonts.lexend(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                          elevation: 8,
                          shadowColor: primaryGold.withValues(alpha: 0.3),
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    SizedBox(
                      width: double.infinity,
                      height: 56,
                      child: OutlinedButton(
                        onPressed: onWorkOffline ??
                            () {
                              Navigator.pop(context);
                            },
                        style: OutlinedButton.styleFrom(
                          foregroundColor:
                              isDark ? Colors.white : const Color(0xFF211811),
                          side: BorderSide(
                            color: isDark
                                ? Colors.white.withValues(alpha: 0.1)
                                : const Color(0xFF211811)
                                    .withValues(alpha: 0.1),
                          ),
                          backgroundColor: isDark
                              ? Colors.white.withValues(alpha: 0.1)
                              : const Color(0xFF382F29).withValues(alpha: 0.1),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(999),
                          ),
                          textStyle: GoogleFonts.lexend(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        child: const Text('Work Offline'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),

          // Connectivity status indicator
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                SizedBox(
                  width: 8,
                  height: 8,
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      // Ping animation
                      TweenAnimationBuilder(
                        tween: Tween<double>(begin: 0.0, end: 1.0),
                        duration: const Duration(seconds: 1),
                        builder: (context, double value, child) {
                          return Opacity(
                            opacity: 1 - value,
                            child: Transform.scale(
                              scale: 1 + value,
                              child: Container(
                                width: 8,
                                height: 8,
                                decoration: const BoxDecoration(
                                  color: primaryGold,
                                  shape: BoxShape.circle,
                                ),
                              ),
                            ),
                          );
                        },
                        onEnd: () {
                          // Restart animation
                        },
                      ),
                      // Static dot
                      Container(
                        width: 8,
                        height: 8,
                        decoration: const BoxDecoration(
                          color: primaryGold,
                          shape: BoxShape.circle,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  'Attempting to reconnect...',
                  style: GoogleFonts.lexend(
                    fontSize: 12,
                    color: isDark
                        ? Colors.white.withValues(alpha: 0.5)
                        : const Color(0xFF211811).withValues(alpha: 0.5),
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
      // bottomNavigationBar: _buildBottomNav(context, isDark), // Removed custom nav
    );
  }

  Widget _buildDot(Color color) {
    return Container(
      width: 8,
      height: 8,
      decoration: BoxDecoration(
        color: color,
        shape: BoxShape.circle,
      ),
    );
  }
}
