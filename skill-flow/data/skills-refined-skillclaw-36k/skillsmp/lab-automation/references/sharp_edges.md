# Lab Automation - Sharp Edges

## Edge Effects in Multi-Well Plates

### **Id**
edge-effects-plates
### **Severity**
high
### **Summary**
Edge wells have different evaporation rates causing systematic bias
### **Symptoms**
  - Outer wells show different results than inner wells
  - Controls in corners always fail/succeed
  - Assay CV improves when excluding edge wells
### **Why**
  Edge wells have more surface area exposed to air.
  This causes:
  - Faster evaporation (volume decreases)
  - Temperature differences
  - Different gas exchange
  
  In cell assays: edge cells grow differently.
  In enzyme assays: concentrations drift.
  
  The effect is worse for:
  - Long incubations
  - Small volumes
  - Non-sealed plates
  
### **Gotcha**
  # Putting critical controls in A1, A12, H1, H12
  controls = ['A1', 'A12', 'H1', 'H12']  # Worst positions!
  
  # Not accounting for evaporation in kinetic reads
  # First timepoint vs last timepoint: 10% volume difference
  
  # Using edge wells for standard curve
  standard_wells = plate.rows()[0]  # All edge wells!
  
### **Solution**
  # Keep controls and critical samples away from edges
  def get_inner_wells(plate, margin=1):
      """Get non-edge wells for critical samples."""
      return [
          well for well in plate.wells()
          if (margin <= well.row <= 7 - margin and
              margin <= well.column <= 11 - margin)
      ]
  
  # Use edge wells for buffer or non-critical blanks
  edge_wells = ['A1', 'A12', 'H1', 'H12']
  # Fill with media to reduce evaporation
  
  # Seal plates for long incubations
  # Use humidity chambers
  
  # Include edge-effect controls and correct computationally
  

## Cross-Contamination from Tip Reuse

### **Id**
tip-contamination
### **Severity**
critical
### **Summary**
Reusing tips between different samples causes carryover
### **Symptoms**
  - Positive samples in wells that should be negative
  - Gradient of signal across plate
  - PCR shows unexpected bands
### **Why**
  Tips retain residual liquid even after dispensing.
  Carryover is typically 0.01-0.1% of aspirated volume.
  
  For PCR: 0.01% carryover of 10^8 copies = 10^4 copies
  That's enough to give a strong false positive!
  
  For compound screening:
  Potent compound carryover can inhibit neighboring wells.
  
### **Gotcha**
  # Aspirating different samples with same tip
  p300.aspirate(100, sample_a)
  p300.dispense(100, dest_1)
  p300.aspirate(100, sample_b)  # Same tip! Contamination!
  p300.dispense(100, dest_2)
  
  # Reusing tips for "similar" samples
  for sample in samples:
      p300.transfer(100, sample, dest, new_tip='never')
  
### **Solution**
  # Change tips between different samples
  for sample in samples:
      p300.transfer(100, sample, dest, new_tip='always')
  
  # For same reagent to multiple wells, use multi-dispense
  p300.pick_up_tip()
  p300.aspirate(200, reagent)
  for well in wells:
      p300.dispense(25, well)  # Same tip OK for same reagent
  p300.drop_tip()
  
  # For PCR/qPCR: Always new tips, work low-to-high concentration
  # Add positive controls LAST
  

## Dead Volume Causing Insufficient Reagent

### **Id**
dead-volume-loss
### **Severity**
high
### **Summary**
Reservoir dead volume leaves less reagent than calculated
### **Symptoms**
  - Last wells get no reagent
  - Pipette aspirates air
  - Protocol fails at end of run
### **Why**
  Reservoirs have minimum aspiratable volume (dead volume):
  - 12-channel reservoir: 3-5 mL per channel
  - 96-well plate: 20-50 µL per well
  - Tubes: 50-200 µL depending on geometry
  
  If you calculate exactly N × volume needed,
  you'll run out before the last sample.
  
### **Gotcha**
  # Need 100 µL × 96 wells = 9.6 mL
  reagent_needed = 100 * 96  # 9600 µL
  # But reservoir dead volume is 3 mL
  # Actually need: 9600 + 3000 = 12600 µL
  
  # Protocol runs out at well 72!
  
### **Solution**
  def calculate_reagent_with_dead_volume(
      volume_per_well: float,
      num_wells: int,
      dead_volume: float,
      extra_percent: float = 10
  ) -> float:
      """Calculate total reagent needed including dead volume."""
      working_volume = volume_per_well * num_wells
      extra = working_volume * (extra_percent / 100)
      total = working_volume + extra + dead_volume
      return total
  
  # Example
  reagent = calculate_reagent_with_dead_volume(
      volume_per_well=100,
      num_wells=96,
      dead_volume=3000,  # 3 mL reservoir dead volume
      extra_percent=10   # 10% extra for safety
  )
  # Result: 13560 µL needed
  

## Inaccurate Dispensing of Viscous Liquids

### **Id**
viscous-liquid-errors
### **Severity**
high
### **Summary**
Standard settings fail for glycerol, DMSO, or serum
### **Symptoms**
  - Droplet hangs on tip after dispense
  - Short dispense - less volume than expected
  - Inconsistent volumes between wells
### **Why**
  Viscous liquids:
  - Take longer to fill tips (incomplete aspiration)
  - Don't detach from tip easily (short dispense)
  - Have different density (volume vs mass mismatch)
  
  Standard pipetting assumes water-like liquids.
  Using these settings for glycerol causes 10-30% error.
  
### **Gotcha**
  # Dispensing DMSO with standard water settings
  p300.aspirate(100, dmso_stock)  # Too fast, air bubble
  p300.dispense(100, dest)  # Droplet hangs on tip
  
  # Not accounting for density
  # 100 µL glycerol ≈ 126 mg (density 1.26)
  # 100 µL water = 100 mg
  
### **Solution**
  # Slow aspiration for viscous liquids
  VISCOUS_SETTINGS = {
      'aspirate_rate': 50,   # µL/s (vs 150 for water)
      'dispense_rate': 50,
      'delay_after_aspirate': 2.0,  # seconds
      'delay_after_dispense': 2.0,
      'blow_out': True,
      'touch_tip': True
  }
  
  def transfer_viscous(pipette, source, dest, volume):
      pipette.aspirate(volume, source, rate=0.3)
      pipette.delay(seconds=2)
      pipette.touch_tip(source)
      pipette.dispense(volume, dest, rate=0.3)
      pipette.delay(seconds=2)
      pipette.blow_out(dest.top())
      pipette.touch_tip(dest)
  
  # Pre-wet tips for viscous liquids
  # Use reverse pipetting for high accuracy
  

## Temperature-Dependent Volume Changes

### **Id**
temperature-volume-drift
### **Severity**
medium
### **Summary**
Cold reagents have different volume than at calibration temperature
### **Symptoms**
  - Volumes off when using cold reagents
  - Assay results drift as reagents warm up
  - First and last wells differ systematically
### **Why**
  Pipettes are calibrated at room temperature (20-25°C).
  Water expands ~0.02% per °C.
  
  At 4°C vs 25°C: ~0.4% volume difference
  Seems small but compounds across many steps.
  
  Also: Cold air is denser, affects air displacement.
  
### **Solution**
  # Allow reagents to equilibrate before use
  # Note in protocol: "Equilibrate to RT for 30 min"
  
  # For critical applications:
  # - Calibrate pipettes at working temperature
  # - Use gravimetric verification
  
  # Keep reagent plates on temp-controlled deck
  temp_module = protocol.load_module('temperature module gen2', '7')
  temp_module.set_temperature(25)  # Match calibration temp
  

## Barcode Reading Failures Breaking Workflow

### **Id**
barcode-scan-failures
### **Severity**
high
### **Summary**
Smudged or missing barcode stops entire automation
### **Symptoms**
  - Protocol stops waiting for barcode
  - Wrong plate processed (barcode mixup)
  - LIMS records don't match physical plates
### **Why**
  Barcodes fail when:
  - Label is smudged or damaged
  - Plate rotated 180° (barcode on wrong side)
  - Wrong barcode type for reader
  - Condensation obscures barcode
  
  Without fallback, entire workflow stops.
  
### **Solution**
  # Implement retry and fallback
  def scan_with_retry(scanner, max_retries=3):
      for attempt in range(max_retries):
          barcode = scanner.read()
          if barcode:
              return barcode
          # Prompt user
          if attempt == max_retries - 1:
              return prompt_manual_entry()
      return None
  
  # Validate barcode format
  def validate_barcode(barcode, expected_format=r'^[A-Z]{2}\d{6}$'):
      import re
      return re.match(expected_format, barcode) is not None
  
  # Log all scans for audit
  # Cross-check with LIMS before processing
  