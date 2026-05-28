/// Region-based affiliate link tagging service
/// 
/// Generates tagged affiliate links for different Amazon regional stores
/// based on the user's detected or selected region.
library;

enum UserRegion {
  us,
  uk,
  eu,
}

class AffiliateService {
  // Affiliate tags for each region
  static const Map<UserRegion, String> _affiliateTags = {
    UserRegion.us: 'adhdsupplements-20',
    UserRegion.uk: 'adhdsupplements-21',
    UserRegion.eu: 'adhdsupplements-22',
  };

  // Base URLs for each Amazon regional store
  static const Map<UserRegion, String> _amazonBaseUrls = {
    UserRegion.us: 'https://www.amazon.com',
    UserRegion.uk: 'https://www.amazon.co.uk',
    UserRegion.eu: 'https://www.amazon.de', // Default EU to Germany
  };

  /// Generates a tagged affiliate link for the given supplement ID and region.
  /// 
  /// [supplementId] - The unique identifier of the supplement (ASIN or product ID)
  /// [region] - The user's region (US, UK, EU)
  /// [customProductPath] - Optional custom product path override
  /// 
  /// Returns a fully formed affiliate URL with tracking tag
  String getTaggedAffiliateLink({
    required String supplementId,
    required UserRegion region,
    String? customProductPath,
  }) {
    final baseUrl = _amazonBaseUrls[region] ?? _amazonBaseUrls[UserRegion.us]!;
    final tag = _affiliateTags[region] ?? _affiliateTags[UserRegion.us]!;
    
    final productPath = customProductPath ?? '/dp/$supplementId';
    
    return '$baseUrl$productPath?tag=$tag';
  }

  /// Generates affiliate links for all regions at once.
  /// 
  /// Useful for letting users switch regions or for analytics.
  Map<UserRegion, String> getAllRegionLinks(String supplementId) {
    return {
      for (final region in UserRegion.values)
        region: getTaggedAffiliateLink(
          supplementId: supplementId,
          region: region,
        ),
    };
  }

  /// Detects user region based on locale.
  /// 
  /// This is a simplified implementation. In production, consider:
  /// - IP-based geolocation
  /// - User preference storage
  /// - Device locale settings
  UserRegion detectRegionFromLocale(String localeCode) {
    final lowerLocale = localeCode.toLowerCase();
    
    if (lowerLocale.startsWith('en_us') || lowerLocale == 'en') {
      return UserRegion.us;
    } else if (lowerLocale.startsWith('en_gb')) {
      return UserRegion.uk;
    } else if (_euLocales.any((eu) => lowerLocale.startsWith(eu))) {
      return UserRegion.eu;
    }
    
    // Default to US
    return UserRegion.us;
  }

  static const List<String> _euLocales = [
    'de', 'fr', 'es', 'it', 'nl', 'pl', 'pt', 'sv', 'da', 'fi', 'no',
  ];
}
