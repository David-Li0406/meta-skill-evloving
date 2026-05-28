import 'package:flutter/material.dart';

class LevelUpScreen extends StatelessWidget {
  const LevelUpScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = Color(0xFFF4C025);
    const bgLight = Color(0xFFF8F8F5);
    const bgDark = Color(0xFF221E10);
    
    return Scaffold(
      backgroundColor: isDark ? bgDark : bgLight,
      body: Stack(
        children: [
          // Background Confetti Pattern
          Positioned.fill(
            child: Opacity(
              opacity: 0.1,
              child: CustomPaint(
                painter: ConfettiPatternPainter(color: primaryGold),
              ),
            ),
          ),
          
          SafeArea(
            child: Column(
              children: [
                // Top Nav
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      IconButton(
                        icon: Icon(Icons.close, color: isDark ? Colors.white : const Color(0xFF181611)),
                        onPressed: () => Navigator.pop(context),
                      ),
                      IconButton(
                        icon: Icon(Icons.help_outline, color: isDark ? Colors.white : const Color(0xFF181611)),
                        onPressed: () {},
                      ),
                    ],
                  ),
                ),
                
                Expanded(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      children: [
                        // Hero Badge Area
                        SizedBox(
                          width: 192,
                          height: 192,
                          child: Stack(
                            alignment: Alignment.center,
                            children: [
                              // Outer Glow
                              Container(
                                width: 192,
                                height: 192,
                                decoration: BoxDecoration(
                                  shape: BoxShape.circle,
                                  color: primaryGold.withValues(alpha: 0.3),
                                  boxShadow: [
                                    BoxShadow(
                                      color: primaryGold.withValues(alpha: 0.3),
                                      blurRadius: 40,
                                      spreadRadius: 10,
                                    ),
                                  ],
                                ),
                              ),
                              // Badge
                              Container(
                                width: 160,
                                height: 160,
                                decoration: BoxDecoration(
                                  shape: BoxShape.circle,
                                  gradient: const LinearGradient(
                                    begin: Alignment.topLeft,
                                    end: Alignment.bottomRight,
                                    colors: [
                                      Color(0xFFF4C025),
                                      Color(0xFFFFF7AD),
                                      Color(0xFFF4C025),
                                    ],
                                  ),
                                  border: Border.all(
                                    color: const Color(0xFFD4A017),
                                    width: 4,
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
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    const Icon(
                                      Icons.military_tech,
                                      size: 48,
                                      color: Color(0xFF6D4C00),
                                    ),
                                    const SizedBox(height: 4),
                                    const Text(
                                      '30',
                                      style: TextStyle(
                                        color: Color(0xFF6D4C00),
                                        fontSize: 40,
                                        fontWeight: FontWeight.w900,
                                        height: 1.0,
                                      ),
                                    ),
                                    Text(
                                      'DAYS',
                                      style: TextStyle(
                                        color: const Color(0xFF6D4C00).withValues(alpha: 0.8),
                                        fontSize: 10,
                                        fontWeight: FontWeight.bold,
                                        letterSpacing: 1.5,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                        
                        const SizedBox(height: 32),
                        
                        Text(
                          "You're a Focus Legend!",
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: isDark ? Colors.white : const Color(0xFF181611),
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            height: 1.1,
                            letterSpacing: -0.5,
                          ),
                        ),
                        
                        const SizedBox(height: 12),
                        
                        Text(
                          "30 days of consistency has changed your brain's potential.",
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: isDark ? Colors.white.withValues(alpha: 0.7) : const Color(0xFF181611).withValues(alpha: 0.7),
                            fontSize: 16,
                            height: 1.5,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                        
                        const SizedBox(height: 32),
                        
                        // Achievement Stats Grid
                        Row(
                          children: [
                            Expanded(child: _buildStatCard(
                              context, 
                              icon: Icons.event_available, 
                              label: 'Days Logged', 
                              value: '30/30', 
                              badgeText: '100% SUCCESS',
                              badgeColor: const Color(0xFF078812),
                            )),
                            const SizedBox(width: 12),
                            Expanded(child: _buildStatCard(
                              context, 
                              icon: Icons.insights, 
                              label: 'Focus Increase', 
                              value: '+22%', 
                              badgeText: 'TOP 5% USERS',
                              badgeColor: const Color(0xFF078812),
                            )),
                          ],
                        ),
                        const SizedBox(height: 12),
                        _buildStatCard(
                          context, 
                          icon: Icons.local_fire_department, 
                          label: 'Broken Streaks', 
                          value: '0', 
                          badgeText: 'PERFECT RUN',
                          badgeColor: isDark ? Colors.white.withValues(alpha: 0.1) : Colors.grey[100]!,
                          badgeTextColor: isDark ? Colors.white.withValues(alpha: 0.6) : Colors.black.withValues(alpha: 0.6),
                          isFullWidth: true,
                        ),
                        
                        const SizedBox(height: 32),
                        
                        // Featured Achievement Card
                        Container(
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: primaryGold.withValues(alpha: isDark ? 0.1 : 0.2),
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(
                              color: primaryGold.withValues(alpha: 0.3),
                            ),
                          ),
                          child: Row(
                            children: [
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: const BoxDecoration(
                                  color: primaryGold,
                                  shape: BoxShape.circle,
                                ),
                                child: const Icon(Icons.auto_awesome, color: Colors.white, size: 20),
                              ),
                              const SizedBox(width: 16),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'New Badge Unlocked',
                                      style: TextStyle(
                                        color: isDark ? Colors.white : const Color(0xFF181611),
                                        fontSize: 14,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    Text(
                                      'Unstoppable: Maintain a 30-day streak.',
                                      style: TextStyle(
                                        color: isDark ? Colors.white.withValues(alpha: 0.7) : const Color(0xFF181611).withValues(alpha: 0.7),
                                        fontSize: 12,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                
                // Bottom Actions
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: isDark ? bgDark.withValues(alpha: 0.9) : Colors.white.withValues(alpha: 0.9),
                    border: Border(
                      top: BorderSide(
                        color: isDark ? Colors.white.withValues(alpha: 0.1) : Colors.black.withValues(alpha: 0.05),
                      ),
                    ),
                  ),
                  child: Column(
                    children: [
                      SizedBox(
                        width: double.infinity,
                        height: 56,
                        child: ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            backgroundColor: primaryGold,
                            foregroundColor: Colors.black,
                            elevation: 8,
                            shadowColor: primaryGold.withValues(alpha: 0.2),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(16),
                            ),
                          ),
                          child: const Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.analytics_outlined),
                              SizedBox(width: 8),
                              Text(
                                'See Your Transformation',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),
                      SizedBox(
                        width: double.infinity,
                        height: 56,
                        child: OutlinedButton(
                          onPressed: () {},
                          style: OutlinedButton.styleFrom(
                            foregroundColor: isDark ? Colors.white : const Color(0xFF181611),
                            side: BorderSide(
                              color: isDark ? Colors.white.withValues(alpha: 0.1) : Colors.black.withValues(alpha: 0.1),
                            ),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(16),
                            ),
                          ),
                          child: const Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.share_outlined),
                              SizedBox(width: 8),
                              Text(
                                'Share My Success',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        'ACHIEVEMENT RECORDED ON APRIL 24, 2024',
                        style: TextStyle(
                          color: isDark ? Colors.white.withValues(alpha: 0.4) : Colors.black.withValues(alpha: 0.4),
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 1.5,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(
    BuildContext context, {
    required IconData icon,
    required String label,
    required String value,
    required String badgeText,
    required Color badgeColor,
    Color? badgeTextColor,
    bool isFullWidth = false,
  }) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = Color(0xFFF4C025);

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark ? Colors.white.withValues(alpha: 0.05) : Colors.white.withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark ? Colors.white.withValues(alpha: 0.1) : const Color(0xFFE6E3DB),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: primaryGold, size: 20),
              const SizedBox(width: 8),
              Text(
                label,
                style: TextStyle(
                  color: isDark ? Colors.white.withValues(alpha: 0.9) : const Color(0xFF181611),
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF181611),
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
            decoration: BoxDecoration(
              color: badgeColor.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(999),
            ),
            child: Text(
              badgeText,
              style: TextStyle(
                color: badgeTextColor ?? badgeColor,
                fontSize: 10,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class ConfettiPatternPainter extends CustomPainter {
  final Color color;

  ConfettiPatternPainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    const gridSize = 50.0;
    
    for (double x = 0; x < size.width; x += gridSize) {
      for (double y = 0; y < size.height; y += gridSize) {
        // Draw varied dots
        if ((x + y) % 2 == 0) {
           canvas.drawCircle(Offset(x, y), 2, paint);
        }
        if ((x * y) % 3 == 0) {
           canvas.drawCircle(Offset(x + 25, y + 25), 1.5, paint);
        }
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
