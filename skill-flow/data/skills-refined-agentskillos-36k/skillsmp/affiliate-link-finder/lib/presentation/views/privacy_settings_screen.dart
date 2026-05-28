import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../application/view_models/privacy_view_model.dart';

class PrivacySettingsScreen extends StatefulWidget {
  const PrivacySettingsScreen({super.key});

  static Widget withProvider() {
    return ChangeNotifierProvider(
      create: (_) => PrivacyViewModel(),
      child: const PrivacySettingsScreen(),
    );
  }

  @override
  State<PrivacySettingsScreen> createState() => _PrivacySettingsScreenState();
}

class _PrivacySettingsScreenState extends State<PrivacySettingsScreen> {
  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryBlue = Color(0xFF2B6CEE);
    const bgLight = Color(0xFFF6F6F8);
    const bgDark = Color(0xFF101622);

    return Scaffold(
      backgroundColor: isDark ? bgDark : bgLight,
      appBar: AppBar(
        backgroundColor: isDark ? const Color(0xFF1C222E) : Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: Icon(
            Icons.arrow_back_ios_new,
            color: isDark ? Colors.white : const Color(0xFF111318),
            size: 20,
          ),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'Privacy & Security',
          style: TextStyle(
            color: isDark ? Colors.white : const Color(0xFF111318),
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(1),
          child: Container(
            color: isDark ? const Color(0xFF2D3648) : const Color(0xFFE5E7EB),
            height: 1,
          ),
        ),
      ),
      body: Consumer<PrivacyViewModel>(builder: (context, viewModel, child) {
        if (viewModel.isLoading) {
          return const Center(
              child: CircularProgressIndicator(color: primaryBlue));
        }
        return SingleChildScrollView(
          child: Column(
            children: [
              _buildSectionHeader('Your Health Data', isDark),
              _buildSettingsContainer(
                context,
                children: [
                  _buildToggleTile(
                    context,
                    title: 'Local Storage Only',
                    subtitle:
                        'Keep all supplement logs on this device. Disables cloud sync to our servers.',
                    value: viewModel.localStorageOnly,
                    showInfoIcon: true,
                    onChanged: (val) => viewModel.setLocalStorageOnly(val),
                    isFirst: true,
                  ),
                  _buildToggleTile(
                    context,
                    title: 'Share Analytics',
                    subtitle:
                        'Help us improve by sharing anonymous usage stats.',
                    value: viewModel.analyticsEnabled,
                    onChanged: (val) => viewModel.setAnalyticsEnabled(val),
                  ),
                  _buildToggleTile(
                    context,
                    title: 'Crash Reporting',
                    subtitle: 'Send automatic reports when the app crashes.',
                    value: viewModel.crashReportingEnabled,
                    onChanged: (val) => viewModel.setCrashReportingEnabled(val),
                  ),
                  _buildActionTile(
                    context,
                    icon: Icons.download,
                    iconColor: primaryBlue,
                    title: 'Download My Data',
                    subtitle: 'Export history as CSV or PDF',
                    onTap: () async {
                      await viewModel.downloadData();
                      if (!context.mounted) return;
                      // ignore: use_build_context_synchronously
                      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
                          content: Text('Data export generated (Simulation)')));
                    },
                    isLast: true,
                  ),
                ],
              ),

              // Secure Access Section
              _buildSectionHeader('Secure Access', isDark),
              _buildSettingsContainer(
                context,
                children: [
                  _buildToggleTile(
                    context,
                    title: 'Biometric Lock',
                    subtitle: 'Require FaceID or TouchID',
                    value: viewModel.biometricLockEnabled,
                    onChanged: (val) => viewModel.setBiometricLockEnabled(val),
                    icon: Icons.fingerprint,
                    iconColor: primaryBlue,
                    isFirst: true,
                    isLast: true,
                  ),
                ],
              ),

              // Data Control Section
              _buildSectionHeader('Data Control', isDark),
              Container(
                margin: const EdgeInsets.symmetric(horizontal: 16),
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: isDark ? const Color(0xFF1C222E) : Colors.white,
                  borderRadius: BorderRadius.circular(12),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.05),
                      blurRadius: 2,
                      offset: const Offset(0, 1),
                    ),
                  ],
                ),
                child: Column(
                  children: [
                    Text(
                      'Deleting your data is permanent. This will erase all your supplement tracking history, medication schedules, and profile information from both this device and any synced backups.',
                      style: TextStyle(
                        color: isDark
                            ? const Color(0xFF94A3B8)
                            : const Color(0xFF616F89),
                        fontSize: 14,
                        height: 1.5,
                      ),
                    ),
                    const SizedBox(height: 16),
                    SizedBox(
                      width: double.infinity,
                      child: TextButton.icon(
                        onPressed: () {
                          showDialog<void>(
                              context: context,
                              builder: (ctx) => AlertDialog(
                                    title: const Text('Delete Everything?'),
                                    content: const Text(
                                        'This action cannot be undone.'),
                                    actions: [
                                      TextButton(
                                        onPressed: () => Navigator.pop(ctx),
                                        child: const Text('Cancel'),
                                      ),
                                      TextButton(
                                        onPressed: () async {
                                          Navigator.pop(ctx);
                                          await viewModel.deleteAccount();
                                          if (!context.mounted) return;
                                          Navigator.pushNamedAndRemoveUntil(
                                              context,
                                              '/login',
                                              (route) => false);
                                        },
                                        child: const Text('DELETE',
                                            style:
                                                TextStyle(color: Colors.red)),
                                      ),
                                    ],
                                  ));
                        },
                        icon: const Icon(Icons.delete_forever,
                            color: Color(0xFFDC2626)),
                        label: const Text(
                          'Delete All My Data',
                          style: TextStyle(
                            color: Color(0xFFDC2626),
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        style: TextButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          backgroundColor: const Color(0xFFFEE2E2),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              // Footer
              const SizedBox(height: 40),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.verified_user, color: primaryBlue, size: 20),
                  const SizedBox(width: 8),
                  Text(
                    'Your privacy is our priority',
                    style: TextStyle(
                      color: isDark
                          ? const Color(0xFF94A3B8)
                          : const Color(0xFF616F89),
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Text(
                  'We use end-to-end encryption for all transmitted data. Learn more in our Privacy Policy.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: isDark
                        ? const Color(0xFF94A3B8)
                        : const Color(0xFF616F89),
                    fontSize: 12,
                  ),
                ),
              ),
              const SizedBox(height: 40),
            ],
          ),
        );
      }),
    );
  }

  Widget _buildSectionHeader(String title, bool isDark) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 24, 16, 8),
      child: Align(
        alignment: Alignment.centerLeft,
        child: Text(
          title,
          style: TextStyle(
            color: isDark ? Colors.white : const Color(0xFF111318),
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }

  Widget _buildSettingsContainer(BuildContext context,
      {required List<Widget> children}) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1C222E) : Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 2,
            offset: const Offset(0, 1),
          ),
        ],
      ),
      child: Column(children: children),
    );
  }

  Widget _buildToggleTile(
    BuildContext context, {
    required String title,
    required String subtitle,
    required bool value,
    required ValueChanged<bool> onChanged,
    bool showInfoIcon = false,
    IconData? icon,
    Color? iconColor,
    bool isFirst = false,
    bool isLast = false,
  }) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        border: !isLast
            ? Border(
                bottom: BorderSide(
                  color: isDark
                      ? const Color(0xFF2D3648)
                      : const Color(0xFFF0F2F4),
                ),
              )
            : null,
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          if (icon != null) ...[
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: iconColor?.withValues(alpha: 0.1) ??
                    Colors.grey.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(icon, color: iconColor ?? Colors.grey, size: 24),
            ),
            const SizedBox(width: 16),
          ],
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      title,
                      style: TextStyle(
                        color: isDark ? Colors.white : const Color(0xFF111318),
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    if (showInfoIcon) ...[
                      const SizedBox(width: 6),
                      Icon(
                        Icons.info_outline,
                        size: 16,
                        color: isDark
                            ? const Color(0xFF94A3B8)
                            : const Color(0xFF616F89),
                      ),
                    ],
                  ],
                ),
                Text(
                  subtitle,
                  style: TextStyle(
                    color: isDark
                        ? const Color(0xFF94A3B8)
                        : const Color(0xFF616F89),
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 8),
          Switch(
            value: value,
            onChanged: onChanged,
            activeThumbColor: const Color(0xFF2B6CEE),
          ),
        ],
      ),
    );
  }

  Widget _buildActionTile(
    BuildContext context, {
    required IconData icon,
    required Color iconColor,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
    bool isLast = false,
  }) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return InkWell(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          border: !isLast
              ? Border(
                  bottom: BorderSide(
                    color: isDark
                        ? const Color(0xFF2D3648)
                        : const Color(0xFFF0F2F4),
                  ),
                )
              : null,
        ),
        child: Row(
          children: [
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: iconColor.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(icon, color: iconColor, size: 24),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      color: isDark ? Colors.white : const Color(0xFF111318),
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  Text(
                    subtitle,
                    style: TextStyle(
                      color: isDark
                          ? const Color(0xFF94A3B8)
                          : const Color(0xFF616F89),
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
            Icon(
              Icons.chevron_right,
              color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF616F89),
              size: 24,
            ),
          ],
        ),
      ),
    );
  }
}
