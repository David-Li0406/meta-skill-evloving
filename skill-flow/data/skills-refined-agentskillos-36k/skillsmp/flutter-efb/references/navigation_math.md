# Aviation Navigation Math

Core calculations for flight planning and navigation in Dart.

## Constants

```dart
import 'dart:math';

// Earth radius in nautical miles
const double EARTH_RADIUS_NM = 3440.065;

// Earth radius in statute miles
const double EARTH_RADIUS_SM = 3958.8;

// Earth radius in kilometers
const double EARTH_RADIUS_KM = 6371.0;

// Conversion factors
const double NM_TO_SM = 1.15078;
const double NM_TO_KM = 1.852;
const double FT_TO_M = 0.3048;
const double KT_TO_MPH = 1.15078;

// Standard atmosphere
const double ISA_SEA_LEVEL_TEMP_C = 15.0;
const double ISA_LAPSE_RATE = 2.0; // degrees C per 1000 ft
const double STANDARD_PRESSURE_INHG = 29.92;
```

## Coordinate Utilities

```dart
double _toRadians(double degrees) => degrees * pi / 180;
double _toDegrees(double radians) => radians * 180 / pi;

/// Normalize angle to 0-360 range
double normalizeAngle(double angle) {
  angle = angle % 360;
  return angle < 0 ? angle + 360 : angle;
}
```

## Distance Calculations

### Haversine Distance

Great circle distance between two coordinates.

```dart
/// Calculate distance between two points in nautical miles
double haversineDistance(
  double lat1, double lon1,
  double lat2, double lon2,
) {
  final dLat = _toRadians(lat2 - lat1);
  final dLon = _toRadians(lon2 - lon1);

  final a = sin(dLat / 2) * sin(dLat / 2) +
            cos(_toRadians(lat1)) * cos(_toRadians(lat2)) *
            sin(dLon / 2) * sin(dLon / 2);

  final c = 2 * atan2(sqrt(a), sqrt(1 - a));

  return EARTH_RADIUS_NM * c;
}

/// Distance in statute miles
double haversineDistanceSM(double lat1, double lon1, double lat2, double lon2) {
  return haversineDistance(lat1, lon1, lat2, lon2) * NM_TO_SM;
}

/// Distance in kilometers
double haversineDistanceKM(double lat1, double lon1, double lat2, double lon2) {
  return haversineDistance(lat1, lon1, lat2, lon2) * NM_TO_KM;
}
```

## Bearing Calculations

### Initial Bearing

True bearing from point A to point B.

```dart
/// Calculate initial (forward) bearing in degrees true
double initialBearing(
  double lat1, double lon1,
  double lat2, double lon2,
) {
  final dLon = _toRadians(lon2 - lon1);
  final lat1Rad = _toRadians(lat1);
  final lat2Rad = _toRadians(lat2);

  final x = sin(dLon) * cos(lat2Rad);
  final y = cos(lat1Rad) * sin(lat2Rad) -
            sin(lat1Rad) * cos(lat2Rad) * cos(dLon);

  return normalizeAngle(_toDegrees(atan2(x, y)));
}

/// Calculate final (reverse) bearing at destination
double finalBearing(
  double lat1, double lon1,
  double lat2, double lon2,
) {
  // Final bearing is initial bearing from B to A, reversed
  return normalizeAngle(initialBearing(lat2, lon2, lat1, lon1) + 180);
}
```

## Wind Calculations

### Wind Correction Angle

Heading adjustment to compensate for wind.

```dart
/// Calculate wind correction angle in degrees
/// Returns positive for right correction, negative for left
double windCorrectionAngle(
  double course,      // True course in degrees
  double windDir,     // Wind direction (from) in degrees true
  double windSpeed,   // Wind speed in knots
  double tas,         // True airspeed in knots
) {
  if (tas <= 0 || windSpeed <= 0) return 0;

  // Wind angle relative to course
  final windAngle = _toRadians(windDir - course);

  // Calculate WCA using crosswind component
  final sinWCA = (windSpeed / tas) * sin(windAngle);

  // Clamp to valid range for asin
  if (sinWCA.abs() > 1) {
    // Wind too strong - can't make course
    return windAngle > 0 ? 90 : -90;
  }

  return _toDegrees(asin(sinWCA));
}

/// Calculate heading to fly given course and wind
double headingForCourse(
  double course,
  double windDir,
  double windSpeed,
  double tas,
) {
  final wca = windCorrectionAngle(course, windDir, windSpeed, tas);
  return normalizeAngle(course + wca);
}
```

### Ground Speed

```dart
/// Calculate ground speed given wind conditions
double groundSpeed(
  double course,      // True course in degrees
  double windDir,     // Wind direction (from) in degrees true
  double windSpeed,   // Wind speed in knots
  double tas,         // True airspeed in knots
) {
  final wca = windCorrectionAngle(course, windDir, windSpeed, tas);
  final wcaRad = _toRadians(wca);
  final windAngle = _toRadians(windDir - course);

  return tas * cos(wcaRad) + windSpeed * cos(windAngle);
}
```

## Altitude Calculations

### Pressure Altitude

```dart
/// Calculate pressure altitude from field elevation and altimeter
double pressureAltitude(
  double fieldElevation,    // Feet MSL
  double altimeterSetting,  // Inches of mercury
) {
  // 1" Hg ≈ 1000 ft
  return fieldElevation + (STANDARD_PRESSURE_INHG - altimeterSetting) * 1000;
}
```

### Density Altitude

```dart
/// Calculate density altitude
double densityAltitude(
  double pressureAlt,  // Feet
  double tempC,        // Celsius
) {
  // ISA temperature at this pressure altitude
  final isaTemp = ISA_SEA_LEVEL_TEMP_C - (pressureAlt / 1000) * ISA_LAPSE_RATE;

  // Temperature deviation from ISA
  final tempDeviation = tempC - isaTemp;

  // Density altitude (120 ft per degree C deviation)
  return pressureAlt + (120 * tempDeviation);
}

/// Full density altitude calculation from field conditions
double densityAltitudeFull(
  double fieldElevation,
  double altimeterSetting,
  double tempC,
) {
  final pa = pressureAltitude(fieldElevation, altimeterSetting);
  return densityAltitude(pa, tempC);
}
```

## Sun Position / Night Detection

```dart
/// Check if it's night (civil twilight - sun 6° below horizon)
bool isNight(double lat, double lon, DateTime utc) {
  final sunAlt = _sunAltitude(lat, lon, utc);
  return sunAlt < -6.0;
}

/// Calculate sun altitude angle in degrees
double _sunAltitude(double lat, double lon, DateTime utc) {
  // Julian date
  final jd = _julianDate(utc);

  // Days since J2000
  final n = jd - 2451545.0;

  // Mean solar longitude
  final L = (280.460 + 0.9856474 * n) % 360;

  // Mean anomaly
  final g = _toRadians((357.528 + 0.9856003 * n) % 360);

  // Ecliptic longitude
  final lambda = _toRadians(L + 1.915 * sin(g) + 0.020 * sin(2 * g));

  // Obliquity of ecliptic
  final epsilon = _toRadians(23.439 - 0.0000004 * n);

  // Sun declination
  final sunDec = asin(sin(epsilon) * sin(lambda));

  // Hour angle
  final ut = utc.hour + utc.minute / 60 + utc.second / 3600;
  final ha = _toRadians((ut - 12) * 15 + lon);

  // Altitude
  final latRad = _toRadians(lat);
  final alt = asin(
    sin(latRad) * sin(sunDec) +
    cos(latRad) * cos(sunDec) * cos(ha)
  );

  return _toDegrees(alt);
}

double _julianDate(DateTime dt) {
  final y = dt.year;
  final m = dt.month;
  final d = dt.day + (dt.hour + dt.minute / 60 + dt.second / 3600) / 24;

  final a = ((14 - m) / 12).floor();
  final y2 = y + 4800 - a;
  final m2 = m + 12 * a - 3;

  return d + ((153 * m2 + 2) / 5).floor() + 365 * y2 +
         (y2 / 4).floor() - (y2 / 100).floor() + (y2 / 400).floor() - 32045;
}
```

## Magnetic Variation

```dart
/// Simplified magnetic variation (use WMM for production)
/// This is a rough approximation for the US only
double magneticVariation(double lat, double lon) {
  // Very rough approximation - use World Magnetic Model in production
  // East is positive, West is negative
  return -14.0 + (lon + 100) * 0.15 + (lat - 40) * 0.1;
}

/// Convert true heading to magnetic
double trueToMagnetic(double trueHeading, double magVar) {
  return normalizeAngle(trueHeading - magVar);
}

/// Convert magnetic heading to true
double magneticToTrue(double magHeading, double magVar) {
  return normalizeAngle(magHeading + magVar);
}
```

## Point Projection

```dart
/// Calculate destination point given start, bearing, and distance
(double lat, double lon) destinationPoint(
  double lat1, double lon1,
  double bearing,    // Degrees true
  double distance,   // Nautical miles
) {
  final lat1Rad = _toRadians(lat1);
  final lon1Rad = _toRadians(lon1);
  final brngRad = _toRadians(bearing);
  final angularDist = distance / EARTH_RADIUS_NM;

  final lat2 = asin(
    sin(lat1Rad) * cos(angularDist) +
    cos(lat1Rad) * sin(angularDist) * cos(brngRad)
  );

  final lon2 = lon1Rad + atan2(
    sin(brngRad) * sin(angularDist) * cos(lat1Rad),
    cos(angularDist) - sin(lat1Rad) * sin(lat2)
  );

  return (_toDegrees(lat2), _toDegrees(lon2));
}
```

## Time/Fuel Calculations

```dart
/// Calculate estimated time enroute
Duration estimatedTimeEnroute(
  double distance,     // Nautical miles
  double groundSpeed,  // Knots
) {
  if (groundSpeed <= 0) return Duration.zero;

  final hours = distance / groundSpeed;
  return Duration(
    hours: hours.floor(),
    minutes: ((hours % 1) * 60).round(),
  );
}

/// Calculate fuel required
double fuelRequired(
  double distance,      // Nautical miles
  double groundSpeed,   // Knots
  double fuelFlow,      // Gallons per hour
  double reserveTime,   // Hours (e.g., 0.75 for 45 min)
) {
  if (groundSpeed <= 0) return 0;

  final flightTime = distance / groundSpeed;
  final totalTime = flightTime + reserveTime;

  return totalTime * fuelFlow;
}
```
