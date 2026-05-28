# Testing Patterns

## Test Structure

```
tests/
├── __init__.py
├── test_<analysis>.py       # Analysis-specific tests
├── test_nidm.py             # NIDM conversion tests
├── test_integration.py      # End-to-end tests
└── fixtures/                 # Test data
    ├── bids_data/           # Minimal BIDS dataset
    └── nidm_data/           # Sample NIDM files
```

## Test Coverage Requirements

1. **CLI Argument Parsing**
   - Valid arguments accepted
   - Invalid arguments rejected
   - Default values correct

2. **BIDS Validation**
   - Valid BIDS datasets accepted
   - Invalid datasets rejected
   - Required files detected

3. **Analysis Execution**
   - Tool runs successfully with valid inputs
   - Error handling for invalid inputs
   - Output files created

4. **NIDM Conversion**
   - Input NIDM file copied correctly
   - Metrics extracted from analysis outputs
   - NIDM file updated with new metrics
   - TTL format valid

5. **Output Structure**
   - Correct directory structure created
   - BIDS-compliant derivatives
   - dataset_description.json files present

## Example Tests

```python
import pytest
from pathlib import Path

def test_cli_args():
    """Test CLI argument parsing."""
    from <package>.run import parse_args
    
    args = parse_args([
        '/data/bids',
        '/data/output',
        'participant',
        '--participant-label', '01',
        '--nidm-input-dir', '/data/nidm'
    ])
    
    assert args.bids_dir == '/data/bids'
    assert args.participant_label == ['01']

def test_nidm_copy(tmp_path):
    """Test NIDM file copying."""
    from <package>.nidm.nidm_converter import copy_nidm_file
    
    # Setup test data
    nidm_input = tmp_path / "nidm_input"
    nidm_input.mkdir()
    (nidm_input / "nidm.ttl").write_text("test nidm content")
    
    # Copy file
    output = tmp_path / "output"
    nidm_file = copy_nidm_file(nidm_input, output, "test_app", "01")
    
    assert nidm_file.exists()
    assert nidm_file.read_text() == "test nidm content"
```

Use pytest fixtures for test data and temporary directories.
