# NIDM Integration Reference

## NIDM Workflow

The standard NIDM integration follows this sequence:

```
1. Check --skip-nidm flag
   ├─ If true: Skip NIDM processing entirely
   └─ If false: Continue to step 2

2. Locate input NIDM file
   └─ Path: <nidm-input-dir>/[sub-{id}/[ses-{session}/]]<filename>.ttl
   
3. Copy NIDM file to output (if exists)
   ├─ Destination: <output_dir>/<bidsapp_name>/nidm/sub-{id}/[ses-{session}/]<filename>.ttl
   └─ If not found: Log warning and continue

4. Run analysis (unless --skip-<analysis>)
   └─ Output to: <output_dir>/<bidsapp_name>/<analysis>/...

5. Extract metrics from analysis outputs
   └─ Analysis-specific metric extraction

6. Integrate metrics into NIDM file
   ├─ If copied file exists: Overwrite with integrated data
   └─ If no existing file: Create new NIDM file from scratch
```

## NIDM File Naming

### With Sessions
```
sub-{id}/ses-{session}/sub-{id}_ses-{session}.ttl
```
Example: `sub-01/ses-baseline/sub-01_ses-baseline.ttl`

### Without Sessions (Session-less)
```
sub-{id}/sub-{id}.ttl
```
Example: `sub-01/sub-01.ttl`

**Important**: Session-less data uses `sub-01.ttl`, NOT `sub-01_ses-baseline.ttl`

## NIDM File Organization

### Input NIDM Directory Structure

**Option 1: Single file** (for dataset-level NIDM)
```
<nidm-input-dir>/
└── nidm.ttl
```

**Option 2: Per-subject files with sessions**
```
<nidm-input-dir>/
├── sub-01/
│   ├── ses-baseline/
│   │   └── sub-01_ses-baseline.ttl
│   └── ses-followup/
│       └── sub-01_ses-followup.ttl
└── sub-02/
    └── ses-baseline/
        └── sub-02_ses-baseline.ttl
```

**Option 3: Per-subject files without sessions**
```
<nidm-input-dir>/
├── sub-01/
│   └── sub-01.ttl
└── sub-02/
    └── sub-02.ttl
```

### Output NIDM Directory Structure

**With sessions:**
```
<output_dir>/<bidsapp_name>/nidm/
├── dataset_description.json
└── sub-{id}/
    └── ses-{session}/
        └── sub-{id}_ses-{session}.ttl
```

**Without sessions:**
```
<output_dir>/<bidsapp_name>/nidm/
├── dataset_description.json
└── sub-{id}/
    └── sub-{id}.ttl
```

## NIDM File Format

NIDM files use Turtle (.ttl) RDF format. Basic structure:

```turtle
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix nidm: <http://purl.org/nidash/nidm#> .
@prefix freesurfer: <http://purl.org/nidash/freesurfer#> .

# Software Agent
<software/freesurfer> a prov:Agent, prov:SoftwareAgent ;
    prov:type nidm:FreeSurfer ;
    nidm:softwareVersion "8.0.0" .

# Processing Activity
<activity/recon-all> a prov:Activity ;
    prov:wasAssociatedWith <software/freesurfer> ;
    prov:used <input/T1w> ;
    prov:generated <output/segmentation> .

# Metrics
<output/segmentation> a prov:Entity ;
    freesurfer:LeftHippocampalVolume "3847.2"^^xsd:float ;
    freesurfer:RightHippocampalVolume "3912.5"^^xsd:float .
```

## NIDM Copy Implementation

### Copy Function Template

```python
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def copy_nidm_file(nidm_input_dir, output_dir, bidsapp_name, subject_id, session_id=None):
    """
    Copy existing NIDM file to output directory.
    
    If no existing NIDM file is found, logs a warning and returns None.
    The NIDM converter should handle creating a new file from scratch.
    
    Args:
        nidm_input_dir: Path to input NIDM directory
        output_dir: Base output directory
        bidsapp_name: Name of BIDSapp (e.g., 'freesurfer_nidm')
        subject_id: Subject ID without 'sub-' prefix
        session_id: Session ID without 'ses-' prefix (optional, None for session-less)
    
    Returns:
        Path to copied NIDM file in output directory, or None if no input file found
    """
    # Determine input NIDM file path
    input_dir = Path(nidm_input_dir)
    
    # Try per-subject structure
    if session_id:
        # With sessions
        filename = f"sub-{subject_id}_ses-{session_id}.ttl"
        input_file = input_dir / f"sub-{subject_id}" / f"ses-{session_id}" / filename
        if not input_file.exists():
            # Try generic nidm.ttl name
            input_file = input_dir / f"sub-{subject_id}" / f"ses-{session_id}" / "nidm.ttl"
    else:
        # Without sessions - use sub-{id}.ttl
        filename = f"sub-{subject_id}.ttl"
        input_file = input_dir / f"sub-{subject_id}" / filename
        if not input_file.exists():
            # Try generic nidm.ttl name
            input_file = input_dir / f"sub-{subject_id}" / "nidm.ttl"
    
    # Fall back to dataset-level file
    if not input_file.exists():
        input_file = input_dir / "nidm.ttl"
    
    if not input_file.exists():
        logger.warning(
            f"No existing NIDM file found in {nidm_input_dir} for sub-{subject_id}"
            + (f" ses-{session_id}" if session_id else "")
            + ". NIDM conversion will create a new file from scratch."
        )
        return None
    
    # Create output directory
    nidm_output_dir = Path(output_dir) / bidsapp_name / "nidm"
    if session_id:
        subject_nidm_dir = nidm_output_dir / f"sub-{subject_id}" / f"ses-{session_id}"
        output_filename = f"sub-{subject_id}_ses-{session_id}.ttl"
    else:
        # Session-less: sub-{id}.ttl
        subject_nidm_dir = nidm_output_dir / f"sub-{subject_id}"
        output_filename = f"sub-{subject_id}.ttl"
    
    subject_nidm_dir.mkdir(parents=True, exist_ok=True)
    output_file = subject_nidm_dir / output_filename
    
    # Copy file
    shutil.copy2(input_file, output_file)
    logger.info(f"Copied NIDM file from {input_file} to {output_file}")
    
    return output_file
```

## NIDM Integration Implementation

### Integration Function Template

```python
import rdflib
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def integrate_metrics_to_nidm(nidm_file, metrics, software_name, software_version, 
                               subject_id, session_id=None, output_dir=None, 
                               bidsapp_name=None):
    """
    Integrate analysis metrics into NIDM file.
    
    If nidm_file is None (no existing file), creates a new NIDM file from scratch.
    
    Args:
        nidm_file: Path to NIDM .ttl file (can be None)
        metrics: Dictionary of metrics to add
        software_name: Name of analysis software (e.g., 'FreeSurfer')
        software_version: Version of analysis software
        subject_id: Subject ID without 'sub-' prefix
        session_id: Session ID without 'ses-' prefix (optional)
        output_dir: Base output directory (required if nidm_file is None)
        bidsapp_name: BIDSapp name (required if nidm_file is None)
    
    Returns:
        Path to the created/updated NIDM file
    """
    # Determine output file path
    if nidm_file is None:
        if output_dir is None or bidsapp_name is None:
            raise ValueError("output_dir and bidsapp_name required when creating new NIDM file")
        
        # Create new NIDM file
        nidm_output_dir = Path(output_dir) / bidsapp_name / "nidm"
        if session_id:
            subject_nidm_dir = nidm_output_dir / f"sub-{subject_id}" / f"ses-{session_id}"
            output_filename = f"sub-{subject_id}_ses-{session_id}.ttl"
        else:
            subject_nidm_dir = nidm_output_dir / f"sub-{subject_id}"
            output_filename = f"sub-{subject_id}.ttl"
        
        subject_nidm_dir.mkdir(parents=True, exist_ok=True)
        nidm_file = subject_nidm_dir / output_filename
        
        logger.info(f"Creating new NIDM file at {nidm_file}")
        g = rdflib.Graph()
    else:
        # Load existing NIDM graph
        logger.info(f"Loading existing NIDM file from {nidm_file}")
        g = rdflib.Graph()
        g.parse(nidm_file, format='turtle')
    
    # Define namespaces
    PROV = rdflib.Namespace('http://www.w3.org/ns/prov#')
    NIDM = rdflib.Namespace('http://purl.org/nidash/nidm#')
    ANALYSIS = rdflib.Namespace(f'http://purl.org/nidash/{software_name.lower()}#')
    XSD = rdflib.Namespace('http://www.w3.org/2001/XMLSchema#')
    
    # Bind namespaces
    g.bind('prov', PROV)
    g.bind('nidm', NIDM)
    g.bind(software_name.lower(), ANALYSIS)
    g.bind('xsd', XSD)
    
    # Create activity node
    timestamp = datetime.now().isoformat()
    activity_id = rdflib.URIRef(f'activity/{software_name.lower()}-{timestamp}')
    g.add((activity_id, rdflib.RDF.type, PROV.Activity))
    g.add((activity_id, PROV.startedAtTime, rdflib.Literal(datetime.now(), datatype=XSD.dateTime)))
    
    # Create software agent
    software_id = rdflib.URIRef(f'software/{software_name.lower()}')
    g.add((software_id, rdflib.RDF.type, PROV.SoftwareAgent))
    g.add((software_id, NIDM.softwareVersion, rdflib.Literal(software_version)))
    g.add((activity_id, PROV.wasAssociatedWith, software_id))
    
    # Create output entity with metrics
    output_id = rdflib.URIRef(f'output/{software_name.lower()}-result-{timestamp}')
    g.add((output_id, rdflib.RDF.type, PROV.Entity))
    g.add((activity_id, PROV.generated, output_id))
    
    # Add subject/session info
    g.add((output_id, NIDM.subjectID, rdflib.Literal(f"sub-{subject_id}")))
    if session_id:
        g.add((output_id, NIDM.sessionID, rdflib.Literal(f"ses-{session_id}")))
    
    # Add metrics
    for metric_name, metric_value in metrics.items():
        predicate = ANALYSIS[metric_name]
        if isinstance(metric_value, float):
            obj = rdflib.Literal(metric_value, datatype=XSD.float)
        elif isinstance(metric_value, int):
            obj = rdflib.Literal(metric_value, datatype=XSD.integer)
        else:
            obj = rdflib.Literal(metric_value)
        g.add((output_id, predicate, obj))
    
    # Save graph (overwrites if existing, creates if new)
    g.serialize(destination=str(nidm_file), format='turtle')
    logger.info(f"NIDM file saved to {nidm_file}")
    
    return nidm_file
```

## Complete NIDM Processing Workflow

```python
def process_nidm(nidm_input_dir, output_dir, bidsapp_name, subject_id, session_id, 
                 skip_nidm, analysis_outputs, software_name, software_version):
    """
    Complete NIDM processing workflow.
    
    Handles both cases:
    1. Existing NIDM file: Copy → Extract metrics → Integrate (overwrite)
    2. No existing file: Warning → Extract metrics → Create new file
    """
    
    if skip_nidm:
        logger.info("Skipping NIDM processing (--skip-nidm flag set)")
        return
    
    # Step 1: Try to copy existing NIDM file
    nidm_file = copy_nidm_file(nidm_input_dir, output_dir, bidsapp_name, 
                                subject_id, session_id)
    
    # Step 2: Extract metrics from analysis outputs
    logger.info("Extracting metrics from analysis outputs")
    metrics = extract_metrics(analysis_outputs, subject_id, session_id)
    
    # Step 3: Integrate metrics into NIDM file
    # This works whether nidm_file exists or is None
    nidm_file = integrate_metrics_to_nidm(
        nidm_file, 
        metrics, 
        software_name, 
        software_version,
        subject_id,
        session_id,
        output_dir,
        bidsapp_name
    )
    
    logger.info(f"NIDM processing complete: {nidm_file}")
```

## Analysis-Specific Metric Extraction

Each analysis tool requires custom metric extraction. Examples:

### FreeSurfer Metrics

```python
def extract_freesurfer_metrics(freesurfer_dir):
    """Extract metrics from FreeSurfer outputs."""
    metrics = {}
    
    # Read aseg.stats for volumetric measures
    aseg_stats = freesurfer_dir / "stats" / "aseg.stats"
    if aseg_stats.exists():
        # Parse aseg.stats file
        # Extract hippocampal volumes, cortical volumes, etc.
        pass
    
    # Read aparc.stats for cortical measures
    for hemi in ['lh', 'rh']:
        aparc_stats = freesurfer_dir / "stats" / f"{hemi}.aparc.stats"
        if aparc_stats.exists():
            # Parse cortical thickness, surface area, etc.
            pass
    
    return metrics
```

### MRIQC Metrics

```python
def extract_mriqc_metrics(mriqc_output_dir):
    """Extract metrics from MRIQC JSON outputs."""
    import json
    
    metrics = {}
    
    # Find JSON file with IQMs
    json_files = list(mriqc_output_dir.glob("sub-*_T1w.json"))
    if json_files:
        with open(json_files[0]) as f:
            iqms = json.load(f)
        
        # Extract image quality metrics
        metrics['SNR'] = iqms.get('snr_total')
        metrics['CNR'] = iqms.get('cnr')
        metrics['EFC'] = iqms.get('efc')
        # Add more metrics as needed
    
    return metrics
```
