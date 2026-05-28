"""Data test."""

from pathlib import Path

import pytest
from linkml_runtime.loaders import yaml_loader

import cmm_ai_automation.datamodel.cmm_ai_automation

DATA_DIR_VALID = Path(__file__).parent / "data" / "valid"
DATA_DIR_INVALID = Path(__file__).parent / "data" / "invalid"

VALID_EXAMPLE_FILES = list(DATA_DIR_VALID.glob("*.yaml"))
INVALID_EXAMPLE_FILES = list(DATA_DIR_INVALID.glob("*.yaml"))


@pytest.mark.parametrize("filepath", VALID_EXAMPLE_FILES)
def test_valid_data_files(filepath: Path) -> None:
    """Test loading of all valid data files."""
    target_class_name = filepath.stem.split("-")[0]
    tgt_class = getattr(
        cmm_ai_automation.datamodel.cmm_ai_automation,
        target_class_name,
    )
    obj = yaml_loader.load(str(filepath), target_class=tgt_class)
    assert obj
