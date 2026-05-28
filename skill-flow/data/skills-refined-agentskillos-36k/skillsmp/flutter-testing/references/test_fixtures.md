# Aviation Test Fixtures

## Airport Fixtures

```dart
// test/fixtures/airports.dart

import 'package:magentaline/domain/entities/airport.dart';

/// Los Angeles International
final testKLAX = Airport(
  id: 'KLAX',
  icaoId: 'KLAX',
  iataId: 'LAX',
  name: 'Los Angeles International',
  city: 'Los Angeles',
  state: 'CA',
  latitude: 33.942501,
  longitude: -118.408058,
  elevation: 128,
  magneticVariation: 12.5, // East
  timeZone: 'America/Los_Angeles',
  type: AirportType.large,
  towered: true,
  fuel: [FuelType.jet, FuelType.avgas100LL],
);

/// San Francisco International
final testKSFO = Airport(
  id: 'KSFO',
  icaoId: 'KSFO',
  iataId: 'SFO',
  name: 'San Francisco International',
  city: 'San Francisco',
  state: 'CA',
  latitude: 37.621313,
  longitude: -122.378955,
  elevation: 13,
  magneticVariation: 13.5,
  timeZone: 'America/Los_Angeles',
  type: AirportType.large,
  towered: true,
  fuel: [FuelType.jet, FuelType.avgas100LL],
);

/// Small untowered field for VFR testing
final testKCPM = Airport(
  id: 'KCPM',
  icaoId: 'KCPM',
  iataId: null,
  name: 'Compton/Woodley',
  city: 'Compton',
  state: 'CA',
  latitude: 33.889999,
  longitude: -118.244003,
  elevation: 97,
  magneticVariation: 12.5,
  timeZone: 'America/Los_Angeles',
  type: AirportType.small,
  towered: false,
  fuel: [FuelType.avgas100LL],
);

/// Mountain airport for terrain testing
final testKASE = Airport(
  id: 'KASE',
  icaoId: 'KASE',
  iataId: 'ASE',
  name: 'Aspen-Pitkin County',
  city: 'Aspen',
  state: 'CO',
  latitude: 39.223099,
  longitude: -106.868797,
  elevation: 7820,
  magneticVariation: 9.0,
  timeZone: 'America/Denver',
  type: AirportType.medium,
  towered: true,
  fuel: [FuelType.jet, FuelType.avgas100LL],
);
```

## Runway Fixtures

```dart
// test/fixtures/runways.dart

final testRunway25L = Runway(
  airportId: 'KLAX',
  id: '25L',
  length: 12091,
  width: 150,
  surface: SurfaceType.asphalt,
  headingTrue: 249,
  headingMagnetic: 249,
  latitude: 33.9465,
  longitude: -118.4313,
  elevation: 126,
  thresholdDisplaced: 0,
  tdz: 126,
  lighting: RunwayLighting.hirl,
  approachLighting: ApproachLighting.alsf2,
  ilsCategory: ILSCategory.catIII,
);

final testRunway07R = Runway(
  airportId: 'KLAX',
  id: '07R',
  length: 12091,
  width: 150,
  surface: SurfaceType.asphalt,
  headingTrue: 69,
  headingMagnetic: 69,
  latitude: 33.9388,
  longitude: -118.3809,
  elevation: 128,
  thresholdDisplaced: 1000,
  tdz: 130,
  lighting: RunwayLighting.hirl,
  approachLighting: ApproachLighting.malsr,
  ilsCategory: ILSCategory.catI,
);
```

## NAVAID Fixtures

```dart
// test/fixtures/navaids.dart

final testLAXVOR = Navaid(
  id: 'LAX',
  name: 'Los Angeles',
  type: NavaidType.vordme,
  latitude: 33.9333,
  longitude: -118.4333,
  elevation: 130,
  frequency: 113.60,
  magneticVariation: 12.5,
  channel: '83X',
);

final testSLINDB = Navaid(
  id: 'SLI',
  name: 'Seal Beach',
  type: NavaidType.vortac,
  latitude: 33.7833,
  longitude: -118.0500,
  elevation: 30,
  frequency: 115.70,
  magneticVariation: 12.5,
  channel: '104X',
);

final testFIMOuter = Navaid(
  id: 'FIMOM',
  name: 'FIMOM',
  type: NavaidType.outerMarker,
  latitude: 33.8500,
  longitude: -118.5000,
  elevation: 0,
  frequency: 75.0,
  magneticVariation: 12.5,
);
```

## Weather Fixtures

```dart
// test/fixtures/weather.dart

final testMetarKLAX = Metar(
  rawText: 'KLAX 151753Z 25010KT 10SM FEW025 20/12 A3002',
  stationId: 'KLAX',
  observationTime: DateTime.utc(2024, 1, 15, 17, 53),
  wind: Wind(direction: 250, speed: 10, gust: null, variable: false),
  visibility: Visibility(statute: 10.0),
  skyConditions: [SkyCondition(coverage: SkyCoverage.few, base: 2500)],
  temperature: 20,
  dewpoint: 12,
  altimeter: 30.02,
  flightCategory: FlightCategory.vfr,
);

final testMetarIFR = Metar(
  rawText: 'KSFO 151753Z 28015G25KT 2SM BR OVC005 14/12 A2985',
  stationId: 'KSFO',
  observationTime: DateTime.utc(2024, 1, 15, 17, 53),
  wind: Wind(direction: 280, speed: 15, gust: 25, variable: false),
  visibility: Visibility(statute: 2.0),
  skyConditions: [SkyCondition(coverage: SkyCoverage.overcast, base: 500)],
  temperature: 14,
  dewpoint: 12,
  altimeter: 29.85,
  flightCategory: FlightCategory.ifr,
);

final testTafKLAX = Taf(
  rawText: '''KLAX 151730Z 1518/1624 25012KT P6SM FEW025
  FM152200 27008KT P6SM SCT035
  FM160600 VRB03KT P6SM SKC''',
  stationId: 'KLAX',
  issueTime: DateTime.utc(2024, 1, 15, 17, 30),
  validFrom: DateTime.utc(2024, 1, 15, 18, 0),
  validTo: DateTime.utc(2024, 1, 17, 0, 0),
  forecasts: [
    TafForecast(
      from: DateTime.utc(2024, 1, 15, 18, 0),
      to: DateTime.utc(2024, 1, 15, 22, 0),
      wind: Wind(direction: 250, speed: 12),
      visibility: Visibility(statute: 6.0),
      skyConditions: [SkyCondition(coverage: SkyCoverage.few, base: 2500)],
    ),
    // ... more forecasts
  ],
);
```

## Flight Plan Fixtures

```dart
// test/fixtures/flight_plans.dart

final testFlightPlanVFR = FlightPlan(
  departure: testKLAX,
  destination: testKSFO,
  alternate: null,
  route: [
    Waypoint.airport(testKLAX),
    Waypoint.navaid(testLAXVOR),
    Waypoint.fix(Fix(id: 'DINTY', lat: 35.0, lon: -119.5)),
    Waypoint.airport(testKSFO),
  ],
  cruiseAltitude: 8500,
  trueAirspeed: 120,
  fuelBurn: 10.0, // gph
  flightRules: FlightRules.vfr,
  aircraftId: 'N12345',
  aircraftType: 'C172/G',
  estimatedTimeEnroute: const Duration(hours: 2, minutes: 30),
  fuelOnBoard: const Duration(hours: 5),
  departureTime: DateTime.utc(2024, 1, 15, 18, 0),
);

final testFlightPlanIFR = FlightPlan(
  departure: testKLAX,
  destination: testKSFO,
  alternate: testKOAK,
  route: [
    Waypoint.airport(testKLAX),
    Waypoint.departure('LAX7'),
    Waypoint.airway('V23'),
    Waypoint.navaid(testSLINDB),
    Waypoint.airway('V107'),
    Waypoint.arrival('SERFR2'),
    Waypoint.airport(testKSFO),
  ],
  cruiseAltitude: 10000,
  trueAirspeed: 140,
  fuelBurn: 12.0,
  flightRules: FlightRules.ifr,
  aircraftId: 'N54321',
  aircraftType: 'C182/G',
  estimatedTimeEnroute: const Duration(hours: 2, minutes: 15),
  fuelOnBoard: const Duration(hours: 6),
  departureTime: DateTime.utc(2024, 1, 15, 18, 0),
);
```

## Procedure Fixtures

```dart
// test/fixtures/procedures.dart

final testILS25L = Approach(
  id: 'ILS25L',
  airportId: 'KLAX',
  runwayId: '25L',
  type: ApproachType.ils,
  name: 'ILS or LOC RWY 25L',
  finalApproachCourse: 249,
  minimums: [
    Minimum(
      category: AircraftCategory.a,
      decisionAltitude: 276,
      visibility: 0.5,
    ),
    Minimum(
      category: AircraftCategory.b,
      decisionAltitude: 276,
      visibility: 0.5,
    ),
    Minimum(
      category: AircraftCategory.c,
      decisionAltitude: 276,
      visibility: 0.5,
    ),
  ],
  missedApproach: 'Climb to 2000 then climbing right turn to 4000 direct LAX VOR',
  waypoints: [
    ProcedureWaypoint(id: 'HUNDA', lat: 33.8, lon: -118.6, altitude: 2000),
    ProcedureWaypoint(id: 'JETSA', lat: 33.85, lon: -118.55, altitude: 1800),
    // ... more waypoints
  ],
);

final testSIDLAX7 = Departure(
  id: 'LAX7',
  airportId: 'KLAX',
  name: 'Los Angeles Seven',
  transitions: ['SLI', 'VNY', 'GMN'],
  waypoints: [
    ProcedureWaypoint(id: 'LAX', lat: 33.9333, lon: -118.4333, altitude: null),
    ProcedureWaypoint(id: 'DARRK', lat: 33.95, lon: -118.5, altitude: 5000),
    // ... more waypoints
  ],
);
```

## Airspace Fixtures

```dart
// test/fixtures/airspace.dart

final testClassBLAX = Airspace(
  id: 'KLAX_B',
  name: 'Los Angeles Class B',
  type: AirspaceType.classB,
  lowerAltitude: 0,
  upperAltitude: 10000,
  geometry: GeoPolygon([
    GeoPoint(34.1, -118.6),
    GeoPoint(34.1, -118.2),
    GeoPoint(33.7, -118.2),
    GeoPoint(33.7, -118.6),
  ]),
);

final testMOA = Airspace(
  id: 'R2508',
  name: 'Edwards MOA',
  type: AirspaceType.moa,
  lowerAltitude: 0,
  upperAltitude: 50000,
  active: true,
  schedule: 'SR-SS',
  contactFrequency: '124.15',
  geometry: GeoPolygon([/* coordinates */]),
);

final testTFR = Airspace(
  id: 'TFR_12345',
  name: 'Temporary Flight Restriction',
  type: AirspaceType.tfr,
  lowerAltitude: 0,
  upperAltitude: 3000,
  effectiveFrom: DateTime.utc(2024, 1, 15, 12, 0),
  effectiveTo: DateTime.utc(2024, 1, 15, 20, 0),
  notamNumber: '1/2345',
  reason: 'VIP Movement',
  geometry: GeoCircle(center: GeoPoint(34.0, -118.3), radiusNm: 3),
);
```

## Using Fixtures

```dart
import 'package:flutter_test/flutter_test.dart';
import '../fixtures/airports.dart';
import '../fixtures/weather.dart';

void main() {
  group('FlightPlanningService', () {
    test('calculates fuel required', () {
      final service = FlightPlanningService();
      final result = service.calculateFuel(
        from: testKLAX,
        to: testKSFO,
        aircraft: testC172,
        weather: testMetarKLAX,
      );

      expect(result.required, closeTo(25, 2)); // gallons
      expect(result.reserve, equals(4.5)); // 45 min reserve
    });
  });
}
```
