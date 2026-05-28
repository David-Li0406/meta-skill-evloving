import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';
import 'package:cached_network_image/cached_network_image.dart';

class DeveloperHandoffLogicTriggersScreen extends StatelessWidget {
  const DeveloperHandoffLogicTriggersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Determine theme brightness and colors
    final isDark = Theme.of(context).brightness == Brightness.dark;

    // Detailed colors from design
    const Color primaryColor = AppColors.primaryGold;
    final Color bgColor = isDark
        ? AppColors.backgroundPremiumDark
        : AppColors.backgroundPremiumLight;
    final Color cardBgColor = isDark ? const Color(0xFF1E1E1E) : Colors.white;
    final Color borderColor =
        isDark ? Colors.white.withValues(alpha: 0.1) : Colors.grey.shade200;
    final Color mainTextColor = isDark ? Colors.white : Colors.black;
    final Color subTextColor = isDark ? Colors.grey[400]! : Colors.grey[600]!;

    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        backgroundColor: bgColor,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new, color: mainTextColor),
          onPressed: () =>
              Navigator.pushReplacementNamed(context, AppRouter.dashboard),
        ),
        title: Text(
          'LOGIC & TRIGGERS',
          style: GoogleFonts.lexend(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: mainTextColor,
            letterSpacing: 1.5,
          ),
        ),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.ios_share, color: primaryColor),
            onPressed: () {},
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Header Meta Info
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 16, 20, 8),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: primaryColor.withValues(alpha: 0.2),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          'BLUEPRINT',
                          style: GoogleFonts.lexend(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            color: primaryColor,
                            letterSpacing: 1.0,
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        'UPDATED 2H AGO',
                        style: GoogleFonts.lexend(
                          fontSize: 10,
                          fontWeight: FontWeight.w500,
                          color: subTextColor,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Antigravity Core v2.0',
                    style: GoogleFonts.lexend(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: mainTextColor,
                      height: 1.1,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Implementation details for state loops and triage.',
                    style: GoogleFonts.lexend(
                      fontSize: 14,
                      color: subTextColor,
                    ),
                  ),
                ],
              ),
            ),

            // Main Content Scrollable
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Flowchart Visual Placeholder
                    Padding(
                      padding: const EdgeInsets.all(16),
                      child: Container(
                        width: double.infinity,
                        height: 200,
                        decoration: BoxDecoration(
                          color: isDark ? Colors.black : Colors.grey[100],
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: borderColor),
                          image: const DecorationImage(
                            image: CachedNetworkImageProvider(
                                'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=800'),
                            fit: BoxFit.cover,
                            opacity: 0.3,
                          ),
                        ),
                        child: Stack(
                          children: [
                            Padding(
                              padding: const EdgeInsets.all(24),
                              child: Column(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Row(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      _buildNodeIcon(Icons.smartphone),
                                      Expanded(
                                        child: Padding(
                                          padding: const EdgeInsets.symmetric(
                                              horizontal: 8, vertical: 12),
                                          child: Stack(
                                            alignment: Alignment.center,
                                            children: [
                                              Divider(
                                                  color: primaryColor
                                                      .withValues(alpha: 0.3),
                                                  thickness: 2),
                                              Container(
                                                padding:
                                                    const EdgeInsets.symmetric(
                                                        horizontal: 6,
                                                        vertical: 2),
                                                decoration: BoxDecoration(
                                                  color: primaryColor,
                                                  borderRadius:
                                                      BorderRadius.circular(4),
                                                ),
                                                child: Text('ENCRYPTED',
                                                    style: GoogleFonts.lexend(
                                                        color: Colors.black,
                                                        fontWeight:
                                                            FontWeight.bold,
                                                        fontSize: 9)),
                                              )
                                            ],
                                          ),
                                        ),
                                      ),
                                      _buildNodeIcon(Icons.cloud_done_outlined,
                                          isServer: true,
                                          primaryColor: primaryColor),
                                    ],
                                  ),
                                  Row(
                                    children: [
                                      Container(
                                        width: 8,
                                        height: 8,
                                        decoration: const BoxDecoration(
                                            color: Colors.greenAccent,
                                            shape: BoxShape.circle),
                                      ),
                                      const SizedBox(width: 8),
                                      Text('System State: Synchronized',
                                          style: GoogleFonts.lexend(
                                              color: Colors.white70,
                                              fontSize: 12,
                                              fontWeight: FontWeight.w500)),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),

                    // Logic Lists Section
                    Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 20, vertical: 12),
                      child: Text(
                        'CORE STATE TRIGGERS',
                        style: GoogleFonts.lexend(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: primaryColor,
                          letterSpacing: 1.5,
                        ),
                      ),
                    ),

                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      child: Column(
                        children: [
                          _buildLogicCard(
                            isDark: isDark,
                            cardBgColor: cardBgColor,
                            borderColor: borderColor,
                            mainTextColor: mainTextColor,
                            subTextColor: subTextColor,
                            icon: Icons.notifications_active,
                            iconColor: primaryColor,
                            iconBg: primaryColor.withValues(alpha: 0.1),
                            title: 'Nudge Loop',
                            status: 'ACTIVE',
                            statusColor: Colors.greenAccent,
                            code: 'if (idle > 300) -> triggerNudge()',
                            codeColor: primaryColor,
                            description:
                                'Escalates notifications if the user misses the primary intake window.',
                          ),
                          const SizedBox(height: 12),
                          _buildLogicCard(
                            isDark: isDark,
                            cardBgColor: cardBgColor,
                            borderColor: borderColor,
                            mainTextColor: mainTextColor,
                            subTextColor: subTextColor,
                            icon: Icons.health_and_safety,
                            iconColor: Colors.redAccent,
                            iconBg: Colors.redAccent.withValues(alpha: 0.1),
                            title: 'Safety Interlock',
                            status: 'PROTECTED',
                            statusColor: Colors.redAccent,
                            code: 'await validateInteraction(context)',
                            codeColor: Colors.redAccent,
                            description:
                                'Blocks intake logging if a high-risk medication interaction is detected.',
                          ),
                          const SizedBox(height: 12),
                          _buildLogicCard(
                            isDark: isDark,
                            cardBgColor: cardBgColor,
                            borderColor: borderColor,
                            mainTextColor: mainTextColor,
                            subTextColor: subTextColor,
                            icon: Icons.auto_awesome,
                            iconColor: AppColors.primaryGold,
                            iconBg: primaryColor.withValues(alpha: 0.1),
                            title: 'XP Engine',
                            status: 'CALCULATING',
                            statusColor: primaryColor,
                            code: 'totalXp += (onTime ? 20 : 5)',
                            codeColor: primaryColor,
                            description:
                                'Dynamic reward system based on streak length and adherence accuracy.',
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 24),
                  ],
                ),
              ),
            ),

            // Technical Footer
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: isDark ? Colors.black : Colors.grey.shade100,
                border: Border(top: BorderSide(color: borderColor)),
              ),
              child: Column(
                children: [
                  Row(
                    children: [
                      const Icon(Icons.code, color: primaryColor, size: 20),
                      const SizedBox(width: 8),
                      Text(
                        'Protocol Specification',
                        style: GoogleFonts.lexend(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: mainTextColor,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                          child: _buildSpecCard(
                              isDark,
                              cardBgColor,
                              borderColor,
                              subTextColor,
                              mainTextColor,
                              'SYNC',
                              Icons.bolt,
                              primaryColor,
                              'Low Latency',
                              'WebSockets')),
                      const SizedBox(width: 16),
                      Expanded(
                          child: _buildSpecCard(
                              isDark,
                              cardBgColor,
                              borderColor,
                              subTextColor,
                              mainTextColor,
                              'STORAGE',
                              Icons.storage,
                              Colors.orangeAccent,
                              'Encrypted',
                              'SQLite + AES')),
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

  Widget _buildNodeIcon(IconData icon,
      {bool isServer = false, Color? primaryColor}) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: isServer ? primaryColor!.withValues(alpha: 0.9) : Colors.black54,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white24),
        boxShadow: isServer
            ? [
                BoxShadow(
                    color: primaryColor!.withValues(alpha: 0.3), blurRadius: 15)
              ]
            : null,
      ),
      child: Icon(icon, color: Colors.white, size: 22),
    );
  }

  Widget _buildLogicCard({
    required bool isDark,
    required Color cardBgColor,
    required Color borderColor,
    required Color mainTextColor,
    required Color subTextColor,
    required IconData icon,
    required Color iconColor,
    required Color iconBg,
    required String title,
    required String status,
    required Color statusColor,
    required String code,
    required Color codeColor,
    required String description,
  }) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: cardBgColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: borderColor),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 52,
            height: 52,
            decoration: BoxDecoration(
              color: iconBg,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, color: iconColor, size: 26),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(title,
                        style: GoogleFonts.lexend(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: mainTextColor)),
                    Row(
                      children: [
                        Container(
                            width: 6,
                            height: 6,
                            decoration: BoxDecoration(
                                color: statusColor, shape: BoxShape.circle)),
                        const SizedBox(width: 6),
                        Text(status,
                            style: GoogleFonts.lexend(
                                fontSize: 9,
                                fontWeight: FontWeight.w800,
                                color: subTextColor,
                                letterSpacing: 0.5)),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 6),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: codeColor.withValues(alpha: 0.05),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(code,
                      style: GoogleFonts.firaCode(
                          fontSize: 11,
                          fontWeight: FontWeight.w500,
                          color: codeColor)),
                ),
                const SizedBox(height: 8),
                Text(description,
                    style: GoogleFonts.lexend(
                        fontSize: 13, color: subTextColor, height: 1.3)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSpecCard(
      bool isDark,
      Color cardBg,
      Color borderColor,
      Color subText,
      Color mainText,
      String label,
      IconData icon,
      Color iconColor,
      String value,
      String subValue) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: borderColor),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label,
              style: GoogleFonts.lexend(
                  fontSize: 10, fontWeight: FontWeight.bold, color: iconColor)),
          const SizedBox(height: 8),
          Row(
            children: [
              Icon(icon, size: 18, color: iconColor),
              const SizedBox(width: 8),
              Text(value,
                  style: GoogleFonts.lexend(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: mainText)),
            ],
          ),
          const SizedBox(height: 4),
          Text(subValue,
              style: GoogleFonts.lexend(fontSize: 11, color: subText)),
        ],
      ),
    );
  }
}
