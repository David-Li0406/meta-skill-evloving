import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_theme.dart';

class CustomSupplementForm extends StatefulWidget {
  final void Function(String name, String category, String? dosage,
      String? timeOfDay, List<String> benefits) onSave;

  const CustomSupplementForm({super.key, required this.onSave});

  @override
  State<CustomSupplementForm> createState() => _CustomSupplementFormState();
}

class _CustomSupplementFormState extends State<CustomSupplementForm> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _dosageController = TextEditingController();
  final _benefitsController = TextEditingController();

  String _selectedCategory = 'General';
  String? _selectedTimeOfDay;

  @override
  void dispose() {
    _nameController.dispose();
    _dosageController.dispose();
    _benefitsController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom + 24,
        left: 24,
        right: 24,
        top: 16,
      ),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1E242E) : Colors.white,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Container(
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: Colors.grey.withValues(alpha: 0.3),
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const SizedBox(height: 24),
              Text(
                'Custom Supplement',
                style: GoogleFonts.lexend(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: isDark ? Colors.white : const Color(0xFF0F172A),
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Add your personal vitamins or medications that aren\'t in our database.',
                style: GoogleFonts.lexend(
                  fontSize: 14,
                  color: isDark ? Colors.grey[400] : Colors.grey[500],
                ),
              ),
              const SizedBox(height: 24),

              // Name Field
              _buildLabel('Supplement Name *'),
              TextFormField(
                controller: _nameController,
                style: TextStyle(color: isDark ? Colors.white : Colors.black),
                decoration:
                    _buildInputDecoration('e.g., My Mystery Focus Mix', isDark),
                validator: (v) => (v == null || v.isEmpty) ? 'Required' : null,
              ),

              const SizedBox(height: 16),

              // Category Field
              _buildLabel('Category'),
              DropdownButtonFormField<String>(
                initialValue: _selectedCategory,
                dropdownColor: isDark ? const Color(0xFF2D3748) : Colors.white,
                style: TextStyle(color: isDark ? Colors.white : Colors.black),
                decoration: _buildInputDecoration('', isDark),
                items: [
                  'General',
                  'Vitamin',
                  'Mineral',
                  'Prescription',
                  'Nootropic'
                ]
                    .map((c) => DropdownMenuItem(value: c, child: Text(c)))
                    .toList(),
                onChanged: (v) => setState(() => _selectedCategory = v!),
              ),

              const SizedBox(height: 16),

              // Dosage Field
              _buildLabel('Dosage (Optional)'),
              TextFormField(
                controller: _dosageController,
                style: TextStyle(color: isDark ? Colors.white : Colors.black),
                decoration:
                    _buildInputDecoration('e.g., 500mg, 1 pill', isDark),
              ),

              const SizedBox(height: 16),

              // Time of Day
              _buildLabel('Preferred Routine'),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  _buildTimeChip('morning', '🌅', isDark),
                  _buildTimeChip('afternoon', '☀️', isDark),
                  _buildTimeChip('evening', '🌇', isDark),
                  _buildTimeChip('night', '🌙', isDark),
                ],
              ),

              const SizedBox(height: 24),

              // Save Button
              SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                      final benefits = _benefitsController.text
                          .split(',')
                          .map((e) => e.trim())
                          .where((e) => e.isNotEmpty)
                          .toList();

                      widget.onSave(
                        _nameController.text,
                        _selectedCategory,
                        _dosageController.text.isEmpty
                            ? null
                            : _dosageController.text,
                        _selectedTimeOfDay,
                        benefits,
                      );
                      Navigator.pop(context);
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primaryGold,
                    foregroundColor: Colors.black,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    elevation: 0,
                  ),
                  child: Text(
                    'Save Supplement',
                    style: GoogleFonts.lexend(
                        fontWeight: FontWeight.bold, fontSize: 16),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLabel(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Text(
        text,
        style: GoogleFonts.lexend(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          color: AppColors.primaryGold,
          letterSpacing: 1.0,
        ),
      ),
    );
  }

  InputDecoration _buildInputDecoration(String hint, bool isDark) {
    return InputDecoration(
      hintText: hint,
      hintStyle: TextStyle(color: isDark ? Colors.grey[600] : Colors.grey[400]),
      filled: true,
      fillColor: isDark
          ? const Color(0xFF2D3748).withValues(alpha: 0.5)
          : Colors.grey[100],
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide.none,
      ),
    );
  }

  Widget _buildTimeChip(String value, String emoji, bool isDark) {
    final isSelected = _selectedTimeOfDay == value;
    return GestureDetector(
      onTap: () =>
          setState(() => _selectedTimeOfDay = isSelected ? null : value),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
        decoration: BoxDecoration(
          color: isSelected
              ? AppColors.primaryGold.withValues(alpha: 0.2)
              : (isDark ? Colors.white.withValues(alpha: 0.05) : Colors.white),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected
                ? AppColors.primaryGold
                : (isDark
                    ? Colors.white.withValues(alpha: 0.1)
                    : Colors.grey[300]!),
          ),
        ),
        child: Column(
          children: [
            Text(emoji, style: const TextStyle(fontSize: 20)),
            const SizedBox(height: 4),
            Text(
              value[0].toUpperCase() + value.substring(1),
              style: GoogleFonts.lexend(
                fontSize: 10,
                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                color: isSelected
                    ? AppColors.primaryGold
                    : (isDark ? Colors.white70 : Colors.black54),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
