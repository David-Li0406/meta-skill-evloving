import logging
import re
from pathlib import Path
from typing import Any

import click
import yaml
from kgx.prefix_manager import PrefixManager
from kgx.transformer import Transformer
from kgx.validator import Validator

# Configure logging
logger = logging.getLogger(__name__)


# Monkey-patch PrefixManager.is_curie to allow slashes in the local part
# The original regex was r"^[^ <()>:]*:[^/ :]+$"
# We change it to allow slashes: r"^[^ <()>:]*:[^ :]+$"
def loose_is_curie(s: str) -> bool:
    if isinstance(s, str):
        # Allow slashes in local part
        m = re.match(r"^[^ <()>:]*:[^ :]+$", s)
        return bool(m)
    return False


def load_config(config_path: Path) -> Any:
    with config_path.open() as f:
        return yaml.safe_load(f)


@click.command()
@click.option(
    "--nodes",
    type=click.Path(exists=True, path_type=Path),
    default="data/private/static/delaney-media-nodes.tsv",
    help="Path to nodes TSV file",
)
@click.option(
    "--edges",
    type=click.Path(exists=True, path_type=Path),
    default="data/private/static/delaney-media-edges.tsv",
    help="Path to edges TSV file",
)
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    default="config/kgx_validation_config.yaml",
    help="Path to validation configuration YAML file",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default="validation_report.json",
    help="Path to output validation report JSON",
)
def validate(nodes: Path, edges: Path, config: Path, output: Path) -> None:
    """
    Validate KGX files with custom prefix configuration.
    """
    # Configure logging if not already configured
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Apply monkey-patch
    if PrefixManager.is_curie != loose_is_curie:
        PrefixManager.is_curie = loose_is_curie
        logger.info("Monkey-patched PrefixManager.is_curie to allow slashes in CURIEs (e.g. DOIs).")

    conf = load_config(config)
    custom_prefixes = conf.get("custom_prefixes", {})

    # Instantiate Validator
    validator = Validator()

    # Inject custom prefixes into the validator instance
    added_prefixes = []
    for prefix in custom_prefixes:
        if prefix not in validator.prefixes:
            validator.prefixes.add(prefix)
            added_prefixes.append(prefix)

    if added_prefixes:
        logger.info(f"Added custom prefixes to validator: {added_prefixes}")
    else:
        logger.info("No new custom prefixes added (all already present or none specified).")

    # Set input arguments
    input_args = {
        "filename": [
            str(nodes),
            str(edges),
        ],
        "format": "tsv",
    }

    # Run Transformer with our patched validator
    transformer = Transformer(stream=True)

    logger.info("Running validation...")
    transformer.transform(
        input_args=input_args,
        output_args={"format": "null"},
        inspector=validator,
    )

    # Write report
    with output.open("w") as f:
        validator.write_report(f)

    logger.info(f"Validation complete. Report written to {output}")

    # Print summary of errors to stdout
    error_count = 0
    for error_type, messages in validator.errors.items():
        count = sum(len(instances) for instances in messages.values())
        error_count += count
        logger.error(f"Error Type: {error_type} - Count: {count}")
        # Print first few examples
        for msg, instances in list(messages.items())[:3]:
            try:
                if instances and len(instances) > 0:
                    logger.error(f"  - {msg} (e.g. {instances[0]})")
                else:
                    logger.error(f"  - {msg}")
            except (KeyError, IndexError, TypeError):
                logger.error(f"  - {msg}")

    if error_count == 0:
        logger.info("SUCCESS: No validation errors found!")
    else:
        logger.error(f"FAILURE: Found {error_count} errors.")
        exit(1)


if __name__ == "__main__":
    validate()
