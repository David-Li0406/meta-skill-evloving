import 'package:flutter/material.dart';

class SupplementUIHelper {
  static IconData getIconForCategory(String category) {
    switch (category.toLowerCase()) {
      case 'essential fatty acids':
        return Icons.water_drop;
      case 'mineral':
        return Icons.science;
      case 'vitamin':
        return Icons.wb_sunny;
      case 'nootropic':
        return Icons
            .psychology; // Changed from Icons.spa to psychology for focus
      case 'herbal':
        return Icons.spa;
      case 'medication':
        return Icons.medical_services;
      default:
        return Icons.local_pharmacy;
    }
  }

  static Color getColorForCategory(String category) {
    switch (category.toLowerCase()) {
      case 'essential fatty acids':
        return Colors.blue[400]!;
      case 'mineral':
        return Colors.purple[400]!;
      case 'vitamin':
        return Colors.amber[400]!;
      case 'nootropic':
        return Colors.green[400]!;
      case 'herbal':
        return Colors.teal[400]!;
      case 'medication':
        return Colors.red[400]!;
      default:
        return Colors.blueGrey;
    }
  }
}
