# Apple Health & Fitness Development Roadmap

## Implementation Methods

### Method 1: healthexport CLI Tool
```bash
pip3 install healthexport
healthexport ~/health-export/
healthexport --data-type StepCount ~/health-export/
```
Output: CSV files with timestamps and values

### Method 2: Health.app Manual Export
1. Open Health app
2. Profile > Export All Health Data
3. Parse `export.xml` with standard tools

### Method 3: HealthKit Framework (Advanced)
Swift CLI tool with HealthKit framework - requires Xcode.

## Planned Helper Scripts

### health-export
```bash
health-export --days 7 --type steps,heart-rate ~/health-export/
```

### health-query
```bash
health-query ~/health-export/ --metric steps --days 7 --summary
health-query ~/health-export/ --metric heart-rate --date 2025-11-15
```

### fitness-summary
```bash
fitness-summary --week
fitness-summary --month
fitness-summary --workouts 5
```

## Data Types

**Activity**: Steps, Flights, Distance, Energy, Exercise minutes
**Workouts**: Type, Duration, Distance, Calories, Heart rate
**Heart Rate**: Resting, Walking, HRV, Exercise
**Sleep**: Duration, Time asleep, Sleep stages
**Body**: Weight, Height, BMI, Body fat
**Vitals**: Blood pressure, Glucose, Blood oxygen, Respiratory rate

## Development Phases

### Phase 1: Export & Basic Queries
- [ ] Install and test healthexport
- [ ] Create helper scripts
- [ ] Document export process
- [ ] Test with real data

### Phase 2: Common Use Cases
- [ ] Weekly activity summaries
- [ ] Workout tracking
- [ ] Sleep analysis
- [ ] Heart rate monitoring
- [ ] Weight tracking

### Phase 3: Advanced Features
- [ ] Live HealthKit queries
- [ ] Trend analysis
- [ ] Goal tracking
- [ ] Health correlations

## Technical Notes

### Dependencies
- Python 3.x (for healthexport)
- SQLite (for local cache)
- jq (for JSON parsing)

### Alternative: Fitness.app
Better AppleScript support for Activity Ring data:
```applescript
tell application "Fitness"
    -- Query activity rings (current day only)
end tell
```

## Status Updates

**2025-11-12**: Initial skill placeholder created.
