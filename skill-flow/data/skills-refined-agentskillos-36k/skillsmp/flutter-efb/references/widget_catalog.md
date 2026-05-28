# EFB Widget Catalog

Common widgets for Electronic Flight Bag applications.

## Airport Information

### Airport Card

```dart
class AirportCard extends StatelessWidget {
  final Airport airport;
  final VoidCallback? onTap;
  final double? distanceNm;
  final double? bearingDeg;

  const AirportCard({
    super.key,
    required this.airport,
    this.onTap,
    this.distanceNm,
    this.bearingDeg,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              // Airport identifier
              Container(
                width: 60,
                height: 60,
                decoration: BoxDecoration(
                  color: airport.isTowered
                      ? Colors.blue.shade100
                      : Colors.purple.shade100,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Center(
                  child: Text(
                    airport.id,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 12),

              // Airport info
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      airport.name,
                      style: Theme.of(context).textTheme.titleMedium,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      '${airport.city}, ${airport.state}',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                    Text(
                      'Elev: ${airport.elevationFt.round()} ft',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                  ],
                ),
              ),

              // Distance and bearing
              if (distanceNm != null)
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(
                      '${distanceNm!.toStringAsFixed(1)} nm',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    if (bearingDeg != null)
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Transform.rotate(
                            angle: bearingDeg! * pi / 180,
                            child: const Icon(Icons.arrow_upward, size: 16),
                          ),
                          Text('${bearingDeg!.round()}°'),
                        ],
                      ),
                  ],
                ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### Runway Diagram

```dart
class RunwayDiagram extends StatelessWidget {
  final List<Runway> runways;
  final double size;

  const RunwayDiagram({
    super.key,
    required this.runways,
    this.size = 150,
  });

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: Size(size, size),
      painter: RunwayPainter(runways: runways),
    );
  }
}

class RunwayPainter extends CustomPainter {
  final List<Runway> runways;

  RunwayPainter({required this.runways});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final maxRadius = min(size.width, size.height) / 2 - 10;

    // Draw compass rose
    final compassPaint = Paint()
      ..color = Colors.grey.shade300
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1;

    canvas.drawCircle(center, maxRadius, compassPaint);

    // Draw each runway
    for (final runway in runways) {
      final angle = (runway.baseHeading - 90) * pi / 180;
      final length = maxRadius * 0.8;
      final width = 8.0;

      final runwayPaint = Paint()
        ..color = Colors.grey.shade800
        ..style = PaintingStyle.fill;

      final start = Offset(
        center.dx + cos(angle) * length / 2,
        center.dy + sin(angle) * length / 2,
      );
      final end = Offset(
        center.dx - cos(angle) * length / 2,
        center.dy - sin(angle) * length / 2,
      );

      // Draw runway rectangle
      canvas.drawLine(start, end, runwayPaint..strokeWidth = width);

      // Draw runway numbers
      final textPainter = TextPainter(
        text: TextSpan(
          text: runway.baseId,
          style: const TextStyle(color: Colors.black, fontSize: 10),
        ),
        textDirection: TextDirection.ltr,
      )..layout();

      textPainter.paint(canvas, start - Offset(textPainter.width / 2, -10));
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
```

## Weather Display

### METAR Widget

```dart
class MetarDisplay extends StatelessWidget {
  final Metar metar;

  const MetarDisplay({super.key, required this.metar});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Flight category
            Row(
              children: [
                FlightCategoryChip(category: metar.flightCategory),
                const Spacer(),
                Text(
                  _formatAge(metar.observedAt),
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ],
            ),
            const SizedBox(height: 8),

            // Wind
            Row(
              children: [
                const Icon(Icons.air, size: 20),
                const SizedBox(width: 8),
                Text(
                  '${metar.windDirection}° @ ${metar.windSpeed} kt',
                  style: const TextStyle(fontSize: 16),
                ),
                if (metar.windGust != null)
                  Text(' G${metar.windGust}', style: TextStyle(color: Colors.red)),
              ],
            ),
            const SizedBox(height: 4),

            // Visibility
            Row(
              children: [
                const Icon(Icons.visibility, size: 20),
                const SizedBox(width: 8),
                Text('${metar.visibility} SM'),
              ],
            ),
            const SizedBox(height: 4),

            // Ceiling/Clouds
            Row(
              children: [
                const Icon(Icons.cloud, size: 20),
                const SizedBox(width: 8),
                Text(metar.cloudLayers.isNotEmpty
                    ? metar.cloudLayers.map((c) => '${c.type} ${c.altitude}').join(', ')
                    : 'Clear'),
              ],
            ),
            const SizedBox(height: 4),

            // Altimeter
            Row(
              children: [
                const Icon(Icons.speed, size: 20),
                const SizedBox(width: 8),
                Text('${metar.altimeter.toStringAsFixed(2)}" Hg'),
              ],
            ),

            const Divider(),

            // Raw METAR
            Text(
              metar.rawText,
              style: const TextStyle(
                fontFamily: 'monospace',
                fontSize: 12,
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _formatAge(DateTime observedAt) {
    final age = DateTime.now().difference(observedAt);
    if (age.inMinutes < 60) {
      return '${age.inMinutes}m ago';
    }
    return '${age.inHours}h ${age.inMinutes % 60}m ago';
  }
}

class FlightCategoryChip extends StatelessWidget {
  final FlightCategory category;

  const FlightCategoryChip({super.key, required this.category});

  @override
  Widget build(BuildContext context) {
    final (color, label) = switch (category) {
      FlightCategory.vfr => (Colors.green, 'VFR'),
      FlightCategory.mvfr => (Colors.blue, 'MVFR'),
      FlightCategory.ifr => (Colors.red, 'IFR'),
      FlightCategory.lifr => (Colors.purple, 'LIFR'),
    };

    return Chip(
      label: Text(label, style: TextStyle(color: Colors.white)),
      backgroundColor: color,
    );
  }
}
```

## Navigation Instruments

### Heading Indicator

```dart
class HeadingIndicator extends StatelessWidget {
  final double heading;
  final double size;

  const HeadingIndicator({
    super.key,
    required this.heading,
    this.size = 200,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: size,
      height: size,
      child: CustomPaint(
        painter: HeadingIndicatorPainter(heading: heading),
      ),
    );
  }
}

class HeadingIndicatorPainter extends CustomPainter {
  final double heading;

  HeadingIndicatorPainter({required this.heading});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = min(size.width, size.height) / 2 - 10;

    // Rotate canvas for heading
    canvas.save();
    canvas.translate(center.dx, center.dy);
    canvas.rotate(-heading * pi / 180);
    canvas.translate(-center.dx, -center.dy);

    // Draw compass rose
    final circlePaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.fill;

    canvas.drawCircle(center, radius, circlePaint);

    // Draw tick marks
    final tickPaint = Paint()
      ..color = Colors.black
      ..strokeWidth = 2;

    for (var i = 0; i < 360; i += 10) {
      final angle = i * pi / 180;
      final isCardinal = i % 90 == 0;
      final length = isCardinal ? 20.0 : (i % 30 == 0 ? 15.0 : 10.0);

      final start = Offset(
        center.dx + cos(angle - pi / 2) * (radius - length),
        center.dy + sin(angle - pi / 2) * (radius - length),
      );
      final end = Offset(
        center.dx + cos(angle - pi / 2) * radius,
        center.dy + sin(angle - pi / 2) * radius,
      );

      canvas.drawLine(start, end, tickPaint);
    }

    // Draw cardinal labels
    _drawLabel(canvas, center, radius, 'N', 0);
    _drawLabel(canvas, center, radius, 'E', 90);
    _drawLabel(canvas, center, radius, 'S', 180);
    _drawLabel(canvas, center, radius, 'W', 270);

    canvas.restore();

    // Draw aircraft symbol (fixed)
    final planePaint = Paint()
      ..color = Colors.orange
      ..style = PaintingStyle.fill;

    final planePath = Path()
      ..moveTo(center.dx, center.dy - 30)
      ..lineTo(center.dx - 20, center.dy + 20)
      ..lineTo(center.dx, center.dy + 10)
      ..lineTo(center.dx + 20, center.dy + 20)
      ..close();

    canvas.drawPath(planePath, planePaint);
  }

  void _drawLabel(Canvas canvas, Offset center, double radius, String text, int degrees) {
    final angle = (degrees - 90) * pi / 180;
    final offset = Offset(
      center.dx + cos(angle) * (radius - 35),
      center.dy + sin(angle) * (radius - 35),
    );

    final textPainter = TextPainter(
      text: TextSpan(
        text: text,
        style: const TextStyle(
          color: Colors.black,
          fontSize: 18,
          fontWeight: FontWeight.bold,
        ),
      ),
      textDirection: TextDirection.ltr,
    )..layout();

    textPainter.paint(
      canvas,
      offset - Offset(textPainter.width / 2, textPainter.height / 2),
    );
  }

  @override
  bool shouldRepaint(HeadingIndicatorPainter oldDelegate) =>
      heading != oldDelegate.heading;
}
```

## Flight Planning

### Leg Row

```dart
class FlightPlanLegRow extends StatelessWidget {
  final FlightPlanLeg leg;
  final bool isActive;

  const FlightPlanLegRow({
    super.key,
    required this.leg,
    this.isActive = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      color: isActive ? Colors.blue.shade50 : null,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          // Waypoint
          SizedBox(
            width: 80,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  leg.waypoint.id,
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                Text(
                  leg.waypoint.name,
                  style: Theme.of(context).textTheme.bodySmall,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),

          // Course
          SizedBox(
            width: 50,
            child: Text('${leg.course.round()}°'),
          ),

          // Distance
          SizedBox(
            width: 60,
            child: Text('${leg.distanceNm.toStringAsFixed(1)} nm'),
          ),

          // ETE
          SizedBox(
            width: 50,
            child: Text(_formatDuration(leg.ete)),
          ),

          // ETA
          SizedBox(
            width: 60,
            child: Text(_formatTime(leg.eta)),
          ),

          // Fuel
          SizedBox(
            width: 50,
            child: Text('${leg.fuelRequired.toStringAsFixed(1)} gal'),
          ),
        ],
      ),
    );
  }

  String _formatDuration(Duration d) {
    return '${d.inMinutes}m';
  }

  String _formatTime(DateTime t) {
    return '${t.hour.toString().padLeft(2, '0')}:${t.minute.toString().padLeft(2, '0')}Z';
  }
}
```

## Theme Support

### Day/Night Toggle

```dart
class DayNightToggle extends StatelessWidget {
  final bool isNightMode;
  final ValueChanged<bool> onChanged;

  const DayNightToggle({
    super.key,
    required this.isNightMode,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return SegmentedButton<bool>(
      segments: const [
        ButtonSegment(
          value: false,
          icon: Icon(Icons.wb_sunny),
          label: Text('Day'),
        ),
        ButtonSegment(
          value: true,
          icon: Icon(Icons.nightlight),
          label: Text('Night'),
        ),
      ],
      selected: {isNightMode},
      onSelectionChanged: (set) => onChanged(set.first),
    );
  }
}
```
