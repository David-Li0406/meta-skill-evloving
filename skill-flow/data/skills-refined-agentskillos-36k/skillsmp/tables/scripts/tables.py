#!/usr/bin/env python3
from pathlib import Path
from typing import Literal, Optional
import pandas as pd
import typer
from varro.data.disk_to_db.process_tables import process_fact_table
from varro.data.utils import (
    df_preview,
    df_dtypes,
    create_table_info_dict,
    show_column_values,
)
from varro.config import DATA_DIR
import json
from pydantic_ai import format_as_xml
import pickle

FACTS_DIR = DATA_DIR / "statbank_tables"
DIMENSIONS_DIR = DATA_DIR / "mapping_tables"
DIM_COLS = ["KODE", "NIVEAU", "TITEL"]
DIMENSION_LINKS_DIR = DATA_DIR / "dimension_links"
TABLES_INFO_DIR = DATA_DIR / "metadata" / "tables_info_raw_da"


def look_at_table(
    table_id: str,
    max_rows: int = 10,
    processed: bool = False,
) -> str:
    """Load a parquet table and return a small, pipe-separated preview as text."""

    path = FACTS_DIR / f"{table_id}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Parquet not found: {path}")

    df = pd.read_parquet(path)
    if processed:
        df = process_fact_table(df)

    dtypes_str = df_dtypes(df)
    preview_str = df_preview(df, max_rows=max_rows, name=table_id)
    return f"{dtypes_str}\n\n{preview_str}"


# --- CLI Commands ---
app = typer.Typer(
    add_completion=False,
    help="Preview StatBank fact/dimension tables and read dimension descriptions.",
)


@app.command("view")
def cli_preview(
    table_id: str = typer.Argument(
        ...,
        help="Table ID (e.g. FOLK1A for fact; dimension id folder name for dimension).",
    ),
    rows: int = typer.Option(
        10, "--rows", "-n", min=1, help="Number of rows to preview."
    ),
    db_format: bool = typer.Option(
        False,
        "--db-format",
        "-d",
        help="Process the table for inserting into the database. This will show how the table will look in the database.",
    ),
):
    """Print a small preview of a fact or dimension parquet table."""
    try:
        text = look_at_table(table_id, max_rows=rows, processed=db_format)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    typer.echo(text)


@app.command("info")
def tables_info_cmd(
    table_id: str = typer.Argument(..., help="table ID, e.g. FOLK1A"),
    column: str | None = typer.Option(
        None,
        "--column",
        "-c",
        help="View all values for a given column. Both text and id values are shown.",
    ),
    normalize_col_names: bool = typer.Option(
        False,
        "--normalize-col-names",
        "-n",
        help="Normalize column names so they match the database schema.",
    ),
):
    table_id = table_id.upper()
    with open(TABLES_INFO_DIR / f"{table_id}.pkl", "rb") as f:
        table_info = pickle.load(f)

    table_info_dict = create_table_info_dict(
        table_info, normalize_col_names=normalize_col_names
    )
    if column:
        column = column.lower()
        values = show_column_values(table_info, column)
        typer.echo(values)
        return

    xml = format_as_xml(table_info_dict)
    typer.echo(xml)


if __name__ == "__main__":
    app()
